import json
import os
import re
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Page
from pyecharts.globals import ThemeType

INPUT_FILE = "北京市房租分析/北京房租数据.xlsx"
SHEET_NAME = "北京各区租金"
OUTPUT_FILE = "北京市房租分析/北京房租可视化分析.html"
COLORS = ["#3B82F6", "#14B8A6", "#F59E0B", "#EF6C78", "#8B5CF6"]


def load_data():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"找不到 {INPUT_FILE}，请先运行01采集程序。")
    data = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    required = ["北京排名", "区域", "平均房租(元/月/㎡)", "环比涨跌幅(%)"]
    missing = [name for name in required if name not in data.columns]
    if missing:
        raise ValueError(f"{SHEET_NAME} 缺少字段：{', '.join(missing)}")
    for name in ["北京排名", "平均房租(元/月/㎡)", "环比涨跌幅(%)"]:
        data[name] = pd.to_numeric(data[name], errors="coerce")
    data = data.dropna(subset=["区域", "平均房租(元/月/㎡)"]).copy()
    if data.empty:
        raise ValueError(f"{SHEET_NAME} 没有可视化数据。")
    return data


def title_options(title, subtitle):
    return opts.TitleOpts(
        title=title, subtitle=subtitle, pos_left="3%", pos_top="3%",
        title_textstyle_opts=opts.TextStyleOpts(color="#1F2937", font_size=18),
        subtitle_textstyle_opts=opts.TextStyleOpts(color="#94A3B8", font_size=11),
    )


def rent_bar(data):
    chart_data = data.sort_values("平均房租(元/月/㎡)")
    return (
        Bar(init_opts=opts.InitOpts(width="900px", height="520px", theme=ThemeType.LIGHT, bg_color="#FFFFFF"))
        .add_xaxis(chart_data["区域"].tolist())
        .add_yaxis("平均房租", chart_data["平均房租(元/月/㎡)"].round(2).tolist(),
                   color=COLORS[0], label_opts=opts.LabelOpts(position="right", formatter="{c}"))
        .reversal_axis()
        .set_global_opts(
            title_opts=title_options("北京各行政区平均房租排行", "单位：元/月/㎡"),
            xaxis_opts=opts.AxisOpts(name="元/月/㎡", splitline_opts=opts.SplitLineOpts(is_show=True)),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
        )
    )


def change_bar(data):
    chart_data = data.dropna(subset=["环比涨跌幅(%)"]).sort_values("环比涨跌幅(%)")
    values = [
        opts.BarItem(
            name=row["区域"],
            value=round(row["环比涨跌幅(%)"], 2),
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[1] if row["环比涨跌幅(%)"] >= 0 else COLORS[3]
            ),
        )
        for _, row in chart_data.iterrows()
    ]
    return (
        Bar(init_opts=opts.InitOpts(width="900px", height="520px", theme=ThemeType.LIGHT, bg_color="#FFFFFF"))
        .add_xaxis(chart_data["区域"].tolist())
        .add_yaxis("环比涨跌幅", values, label_opts=opts.LabelOpts(position="right", formatter="{c}%"))
        .reversal_axis()
        .set_global_opts(
            title_opts=title_options("北京各行政区房租环比变化", "绿色表示上涨，红色表示下降"),
            xaxis_opts=opts.AxisOpts(name="%", splitline_opts=opts.SplitLineOpts(is_show=True)),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
        )
    )


def level_pie(data):
    values = data["平均房租(元/月/㎡)"]
    edges = [values.min() - 0.01, values.quantile(0.33), values.quantile(0.67), values.max() + 0.01]
    levels = pd.cut(values, bins=edges, labels=["低租金区", "中租金区", "高租金区"], include_lowest=True)
    counts = levels.value_counts().reindex(["低租金区", "中租金区", "高租金区"]).fillna(0).astype(int)
    return (
        Pie(init_opts=opts.InitOpts(width="900px", height="500px", theme=ThemeType.LIGHT, bg_color="#FFFFFF"))
        .add("行政区数量", [[name, int(value)] for name, value in counts.items()],
             radius=["38%", "68%"], center=["50%", "57%"],
             label_opts=opts.LabelOpts(formatter="{b}\n{c}个  {d}%"))
        .set_colors([COLORS[1], COLORS[0], COLORS[3]])
        .set_global_opts(
            title_opts=title_options("北京行政区租金梯度分布", "按照行政区平均房租三分位数划分"),
            legend_opts=opts.LegendOpts(pos_top="13%"),
        )
    )


def build_conclusions(data):
    highest = data.loc[data["平均房租(元/月/㎡)"].idxmax()]
    lowest = data.loc[data["平均房租(元/月/㎡)"].idxmin()]
    ratio = highest["平均房租(元/月/㎡)"] / lowest["平均房租(元/月/㎡)"]
    trend = data.dropna(subset=["环比涨跌幅(%)"])
    if trend.empty:
        trend_text = "当前数据没有完整的环比涨跌幅字段。"
    else:
        rising = trend.loc[trend["环比涨跌幅(%)"].idxmax()]
        falling = trend.loc[trend["环比涨跌幅(%)"].idxmin()]
        trend_text = (
            f"{rising['区域']}涨幅最高，为 {rising['环比涨跌幅(%)']:+.2f}%；"
            f"{falling['区域']}变化最低，为 {falling['环比涨跌幅(%)']:+.2f}%。"
        )
    return [
        ("区域价差明显",
         f"{highest['区域']}平均房租最高，为 {highest['平均房租(元/月/㎡)']:.2f} 元/月/㎡；"
         f"{lowest['区域']}最低，为 {lowest['平均房租(元/月/㎡)']:.2f} 元/月/㎡。"
         f"最高值约为最低值的 {ratio:.2f} 倍。",
         "选房建议", "预算有限时可优先比较低租金行政区及地铁沿线房源，并把通勤成本纳入判断。"),
        ("短期变化", trend_text, "分析提示", "单月涨跌可能受到样本结构影响，不应直接视为长期趋势。"),
        ("租金梯度", "按照行政区平均房租的三分位数划分低、中、高三个相对梯度。",
         "使用说明", "梯度用于区域初筛，不是固定预算线，实际选房还需结合面积和通勤距离。"),
    ]


def inject_dashboard(path, data):
    highest = data.loc[data["平均房租(元/月/㎡)"].idxmax()]
    lowest = data.loc[data["平均房租(元/月/㎡)"].idxmin()]
    sorted_data = data.sort_values("平均房租(元/月/㎡)").reset_index(drop=True)
    middle = sorted_data.iloc[len(sorted_data) // 2]
    average = data["平均房租(元/月/㎡)"].mean()
    month = str(data["数据月份"].dropna().iloc[0]) if "数据月份" in data and data["数据月份"].notna().any() else "页面最新月份"

    header = f'''<header class="header"><h1>北京各行政区房租分析</h1><div class="en">Beijing District Rental Analysis</div><p>仅使用“北京各区租金”工作表，比较行政区平均房租、环比变化和租金梯度。</p></header><section class="summary"><div class="metric"><strong>{len(data)}</strong><span>行政区数量</span></div><div class="metric"><strong>{average:.2f}</strong><span>区级均值 / 元·月·㎡</span></div><div class="metric"><strong>{highest['区域']}</strong><span>最高租金区域</span></div><div class="metric"><strong>{lowest['区域']}</strong><span>最低租金区域</span></div></section><main class="container" id="analysis-container"></main>'''
    notes = []
    for index, (title, content, tip_title, tip) in enumerate(build_conclusions(data), 1):
        notes.append(f'''<aside class="conclusion-card"><div class="number">{index:02d}</div><h3>分析结论<span>Analysis Conclusion</span></h3><div class="cn-title">{title}</div><p>{content}</p><div class="line"></div><div class="en-title">{tip_title}</div><p>{tip}</p></aside>''')
    final = f'''<section class="final-section"><div class="final-title"><h2>北京租房区域建议</h2><p>RENTAL AREA RECOMMENDATIONS</p></div><div class="recommend-list"><article class="recommend-card premium"><b>品质优先</b><h3>{highest['区域']}</h3><strong>{highest['平均房租(元/月/㎡)']:.2f} 元/月/㎡</strong><p>适合预算较充足、优先考虑中心区位与生活资源的人群。</p></article><article class="recommend-card balanced"><b>均衡选择</b><h3>{middle['区域']}</h3><strong>{middle['平均房租(元/月/㎡)']:.2f} 元/月/㎡</strong><p>可作为价格与通勤平衡的区域参考，仍需结合具体工作地点判断。</p></article><article class="recommend-card budget"><b>预算优先</b><h3>{lowest['区域']}</h3><strong>{lowest['平均房租(元/月/㎡)']:.2f} 元/月/㎡</strong><p>适合预算敏感或能够接受较长通勤距离的人群。</p></article></div><div class="final-summary"><h3>最终总结</h3><p>北京各行政区平均房租呈现明显梯度。当前数据只适合行政区初筛，最终选房仍需结合实际房源、租住面积和通勤时间。</p></div></section><footer>北京各行政区房租分析 ｜ {month} ｜ 数据来源：中国房价行情网</footer>'''
    style = '''<style>*{box-sizing:border-box}body{margin:0!important;background:#f4f7fb!important;color:#1f2937;font-family:"Microsoft YaHei","PingFang SC",Arial,sans-serif}.header{padding:38px 6%;background:#fff;border-bottom:1px solid #e5e7eb}.header h1{margin:0;font-size:30px}.header .en{margin-top:6px;color:#64748b}.header p{margin:16px 0 0;color:#64748b}.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:24px 6%}.metric,.chart-card,.conclusion-card,.recommend-card{background:#fff;border:1px solid #edf2f7;border-radius:16px;box-shadow:0 4px 20px rgba(15,23,42,.06)}.metric{padding:20px}.metric strong{display:block;font-size:25px;margin-bottom:8px}.metric span{font-size:13px;color:#64748b}.container{width:90%;margin:0 auto 40px}.analysis-row{display:grid;grid-template-columns:minmax(0,2.15fr) minmax(300px,.85fr);gap:18px;margin-bottom:22px}.chart-card{padding:12px;overflow:hidden}.chart-container{width:100%!important;margin:0!important}.conclusion-card{position:relative;padding:30px;display:flex;flex-direction:column;justify-content:center}.number{position:absolute;right:22px;top:14px;font-size:46px;font-weight:800;color:#eef2f7}.conclusion-card h3{margin:0 0 22px}.conclusion-card h3 span{display:block;color:#94a3b8;font-size:11px;font-weight:400}.cn-title,.en-title{font-size:13px;font-weight:700;color:#2563eb;margin-bottom:8px}.en-title{color:#7c3aed}.conclusion-card p{margin:0;line-height:1.9;font-size:14px;color:#334155}.line{height:1px;background:#e5e7eb;margin:20px 0}.final-section{width:90%;margin:55px auto 45px}.final-title{text-align:center;margin-bottom:28px}.final-title h2{margin:0;font-size:30px}.final-title p{color:#94a3b8}.recommend-list{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.recommend-card{padding:26px;border-top:5px solid #3b82f6}.recommend-card.premium{border-top-color:#f59e0b}.recommend-card.budget{border-top-color:#14b8a6}.recommend-card h3{font-size:23px;margin:16px 0 8px}.recommend-card p{color:#64748b;line-height:1.8}.final-summary{margin-top:25px;background:linear-gradient(135deg,#172033,#273753);border-radius:20px;padding:30px 34px;color:#d9e2ef}.final-summary h3{margin-top:0;color:#fff}.final-summary p{line-height:1.9;margin-bottom:0}footer{text-align:center;padding:0 0 32px;color:#94a3b8;font-size:12px}@media(max-width:1000px){.summary{grid-template-columns:repeat(2,1fr)}.analysis-row,.recommend-list{grid-template-columns:1fr}}@media(max-width:600px){.summary{grid-template-columns:1fr}.container,.final-section{width:94%}}</style>'''

    with open(path, "r", encoding="utf-8") as file:
        html = file.read()
    notes_json = json.dumps(notes, ensure_ascii=False)
    final_json = json.dumps(final, ensure_ascii=False)
    script = f'''<script>window.addEventListener('load',function(){{var container=document.getElementById('analysis-container'),notes={notes_json},charts=Array.from(document.querySelectorAll('.chart-container'));charts.forEach(function(chart,index){{var row=document.createElement('section');row.className='analysis-row';var card=document.createElement('div');card.className='chart-card';container.appendChild(row);row.appendChild(card);card.appendChild(chart);var holder=document.createElement('div');holder.innerHTML=notes[index]||'';if(holder.firstElementChild)row.appendChild(holder.firstElementChild);var instance=echarts.getInstanceByDom(chart);if(instance)setTimeout(function(){{instance.resize();}},60);}});container.insertAdjacentHTML('afterend',{final_json});}});</script>'''
    html, body_count = re.subn(r"(<body\b[^>]*>)", lambda match: match.group(1) + style + header, html, count=1, flags=re.I)
    html, end_count = re.subn(r"</body\s*>", script + "</body>", html, count=1, flags=re.I)
    if not body_count or not end_count:
        raise RuntimeError("没有找到HTML的body标签，无法插入页面布局。")
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)


def main():
    data = load_data()
    page = Page(page_title="北京各行政区房租可视化分析", layout=Page.SimplePageLayout)
    page.add(rent_bar(data), change_bar(data), level_pie(data))
    page.render(OUTPUT_FILE)
    inject_dashboard(OUTPUT_FILE, data)
    print(f"可视化网页已生成：{OUTPUT_FILE}")
    print("网页仅使用“北京各区租金”工作表。")


if __name__ == "__main__":
    main()
