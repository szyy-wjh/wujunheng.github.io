import re
import os
import time
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions

CITY_URL = "https://m.creprice.cn/city/bj.html?type=lease"
OUTPUT_FILE = "北京市房租分析/北京房租数据.xlsx"
DISTRICT_CODES = {
    "西城区": "xc", "海淀区": "hd", "东城区": "dc", "朝阳区": "cy", "丰台区": "ft",
    "石景山区": "sjs", "昌平区": "cp", "大兴区": "dx", "通州区": "tz", "顺义区": "sy",
    "门头沟区": "mtg", "房山区": "fs", "怀柔区": "hr", "密云区": "my", "延庆区": "yq"
}

if not os.path.exists('北京市房租分析'):
    os.makedirs('北京市房租分析', exist_ok=True)

def create_browser():
    options = ChromiumOptions()
    options.set_argument("--start-maximized")
    options.set_argument("--disable-blink-features=AutomationControlled")
    options.set_user_agent("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/131 Mobile Safari/537.36")
    page = ChromiumPage(addr_or_opts=options)
    try:
        page.set.window.max()
    except Exception:
        pass
    return page

def get_page_text(page, url, keyword):
    page.get(url)
    time.sleep(1.8)
    page.scroll.to_bottom()
    time.sleep(0.8)
    body = page.ele("tag:body", timeout=5)
    if not body:
        raise RuntimeError(f"没有找到网页正文：{url}")
    if keyword not in body.text:
        time.sleep(2)
        body = page.ele("tag:body", timeout=5)
    return body.text

def search_number(pattern, text, default=None):
    match = re.search(pattern, text, re.S)
    if not match:
        return default
    return float(match.group(1).replace(",", ""))

def parse_city_month(text):
    month_match = re.search(r"平均房租[\s\S]{0,30}?(20\d{2}年\d{1,2}月)", text)
    return month_match.group(1) if month_match else "页面最新月份"

def parse_districts(text):
    text = text.replace("｜", " ").replace("|", " ").replace("\xa0", " ")
    compact_text = re.sub(r"\s+", " ", text)
    pattern = re.compile(r"(?:^|\s)(\d{1,2})\s+([\u4e00-\u9fa5]+区)\s+(\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s*%")
    data = []
    for rank, district, rent, change in pattern.findall(compact_text):
        if district in DISTRICT_CODES:
            data.append([int(rank), district, float(rent), float(change)])
    if not data:
        raise RuntimeError("没有解析到北京各行政区租金排行。")
    return sorted(data, key=lambda item: item[0])

def crawl_beijing(page):
    print("正在采集北京各行政区租金数据……")
    city_text = get_page_text(page, CITY_URL, "北京房租")
    data_month = parse_city_month(city_text)
    district_rows = parse_districts(city_text)
    district_overviews = []
    for rank, district, average_rent, change in district_rows:
        district_overviews.append({
            "北京排名": rank,
            "区域": district,
            "平均房租(元/月/㎡)": average_rent,
            "环比涨跌幅(%)": change,
            "数据月份": data_month,
            "数据来源": CITY_URL
        })
    print(f"已获取行政区数据 {len(district_overviews)} 条")
    return district_overviews

def save_excel(district_overviews):
    district_df = pd.DataFrame(district_overviews)
    district_df = district_df[[
        "北京排名", "区域", "平均房租(元/月/㎡)",
        "环比涨跌幅(%)", "数据月份", "数据来源"
    ]].sort_values("北京排名")

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        district_df.to_excel(writer, sheet_name="北京各区租金", index=False)
        widths = {"北京各区租金": [12, 16, 24, 18, 16, 52]}
        for sheet_name, column_widths in widths.items():
            sheet = writer.sheets[sheet_name]
            sheet.freeze_panes = "A2"
            for index, width in enumerate(column_widths, 1):
                sheet.column_dimensions[chr(64 + index)].width = width
    print("\n采集完成")
    print(f"行政区租金信息：{len(district_df)} 条")
    print(f"数据文件：{OUTPUT_FILE}")

def main():
    page = None
    try:
        page = create_browser()
        district_overviews = crawl_beijing(page)
        save_excel(district_overviews)
    except Exception as error:
        print(f"采集失败：{error}")
    finally:
        page.quit()

if __name__ == "__main__":
    main()
