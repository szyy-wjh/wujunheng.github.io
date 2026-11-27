import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

INPUT_FILE = "北京市房租分析/北京房租数据.xlsx"
SHEET_NAME = "北京各区租金"
OUTPUT_FILE = "北京市房租分析/北京房租市场数据分析报告.pdf"
IMAGE_DIR = "北京市房租分析/北京房租报告图表"


def find_chinese_font():
    paths = [
        "C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("没有找到中文字体，请确认系统已经安装微软雅黑或黑体。")


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
        raise ValueError(f"{SHEET_NAME} 没有可分析的数据。")
    return data


def set_chart_style(font_path):
    font = font_manager.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "#F8FAFC"
    return font


def create_charts(data, font_path):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    font = set_chart_style(font_path)
    paths = {}

    rent = data.sort_values("平均房租(元/月/㎡)")
    plt.figure(figsize=(10, 7))
    bars = plt.barh(rent["区域"], rent["平均房租(元/月/㎡)"], color="#2878B5")
    plt.title("北京各行政区平均房租排行", fontproperties=font, fontsize=16, pad=14)
    plt.xlabel("元/月/㎡", fontproperties=font)
    plt.yticks(fontproperties=font)
    for bar in bars:
        value = bar.get_width()
        plt.text(value + 0.5, bar.get_y() + bar.get_height() / 2, f"{value:.2f}", va="center", fontsize=8)
    plt.grid(axis="x", alpha=0.2)
    plt.tight_layout()
    paths["rent"] = os.path.join(IMAGE_DIR, "01_行政区平均房租.png")
    plt.savefig(paths["rent"], dpi=180, bbox_inches="tight")
    plt.close()

    change = data.dropna(subset=["环比涨跌幅(%)"]).sort_values("环比涨跌幅(%)")
    paths["change"] = None
    if not change.empty:
        plt.figure(figsize=(10, 7))
        bar_colors = ["#2A9D8F" if value >= 0 else "#D95F59" for value in change["环比涨跌幅(%)"]]
        bars = plt.barh(change["区域"], change["环比涨跌幅(%)"], color=bar_colors)
        plt.axvline(0, color="#667085", linewidth=0.8)
        plt.title("北京各行政区房租环比变化", fontproperties=font, fontsize=16, pad=14)
        plt.xlabel("环比涨跌幅（%）", fontproperties=font)
        plt.yticks(fontproperties=font)
        for bar in bars:
            value = bar.get_width()
            plt.text(value + (0.05 if value >= 0 else -0.05), bar.get_y() + bar.get_height() / 2,
                     f"{value:+.2f}%", va="center", ha="left" if value >= 0 else "right", fontsize=8)
        plt.grid(axis="x", alpha=0.2)
        plt.tight_layout()
        paths["change"] = os.path.join(IMAGE_DIR, "02_行政区环比变化.png")
        plt.savefig(paths["change"], dpi=180, bbox_inches="tight")
        plt.close()

    values = data["平均房租(元/月/㎡)"]
    edges = [values.min() - 0.01, values.quantile(0.33), values.quantile(0.67), values.max() + 0.01]
    levels = pd.cut(values, bins=edges, labels=["低租金区", "中租金区", "高租金区"], include_lowest=True)
    counts = levels.value_counts().reindex(["低租金区", "中租金区", "高租金区"]).fillna(0)
    plt.figure(figsize=(9, 5.5))
    bars = plt.bar(counts.index, counts.values, color=["#2A9D8F", "#2878B5", "#D95F59"])
    plt.title("北京行政区租金梯度分布", fontproperties=font, fontsize=16, pad=14)
    plt.ylabel("行政区数量", fontproperties=font)
    plt.xticks(fontproperties=font)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                 f"{int(bar.get_height())}个", ha="center", fontsize=9)
    plt.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    paths["level"] = os.path.join(IMAGE_DIR, "03_租金梯度分布.png")
    plt.savefig(paths["level"], dpi=180, bbox_inches="tight")
    plt.close()
    return paths


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("ChineseFont", 8)
    canvas.setFillColor(colors.HexColor("#7A8798"))
    canvas.drawCentredString(A4[0] / 2, 0.8 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


def create_pdf(data, font_path, paths):
    pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
    styles = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=styles["Title"], fontName="ChineseFont", fontSize=24,
                           leading=34, textColor=colors.HexColor("#143D59"), alignment=TA_CENTER)
    subtitle = ParagraphStyle("subtitle", parent=styles["BodyText"], fontName="ChineseFont", fontSize=11,
                              leading=19, textColor=colors.HexColor("#6B7C93"), alignment=TA_CENTER)
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="ChineseFont", fontSize=16,
                        leading=24, textColor=colors.HexColor("#143D59"), spaceAfter=10)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontName="ChineseFont", fontSize=10.5,
                          leading=19, textColor=colors.HexColor("#34495E"))
    note = ParagraphStyle("note", parent=body, backColor=colors.HexColor("#EDF6FA"),
                          borderColor=colors.HexColor("#4A90A4"), borderWidth=0.7, borderPadding=10)
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4, rightMargin=1.55 * cm, leftMargin=1.55 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.45 * cm,
                            title="北京各行政区房租数据分析报告")

    highest = data.loc[data["平均房租(元/月/㎡)"].idxmax()]
    lowest = data.loc[data["平均房租(元/月/㎡)"].idxmin()]
    ratio = highest["平均房租(元/月/㎡)"] / lowest["平均房租(元/月/㎡)"]
    month = str(data["数据月份"].dropna().iloc[0]) if "数据月份" in data and data["数据月份"].notna().any() else "页面最新月份"
    trend = data.dropna(subset=["环比涨跌幅(%)"])
    rising = trend.loc[trend["环比涨跌幅(%)"].idxmax()] if not trend.empty else None
    falling = trend.loc[trend["环比涨跌幅(%)"].idxmin()] if not trend.empty else None

    story = [Spacer(1, 2.2 * cm), Paragraph("北京各行政区房租数据分析报告", title),
             Spacer(1, 0.45 * cm), Paragraph(f"数据月份：{month}　｜　仅分析北京各行政区租金数据", subtitle),
             Spacer(1, 1.2 * cm)]
    cover = [["行政区数量", f"{len(data)} 个"], ["最高租金区域", highest["区域"]],
             ["最低租金区域", lowest["区域"]], ["最高与最低租金比", f"{ratio:.2f} 倍"]]
    table = Table(cover, colWidths=[5.2 * cm, 9.2 * cm], rowHeights=0.8 * cm)
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "ChineseFont"),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#143D59")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F4F7FA")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6DEE6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.extend([table, Spacer(1, 0.8 * cm),
                  Paragraph("本报告只分析各行政区平均房租与环比变化，用于比较区域租金差异。", note),
                  PageBreak()])

    story.extend([Paragraph("一、各行政区平均房租排行", h1),
                  Paragraph(f"{highest['区域']}平均房租最高，为 {highest['平均房租(元/月/㎡)']:.2f} 元/月/㎡；"
                            f"{lowest['区域']}最低，为 {lowest['平均房租(元/月/㎡)']:.2f} 元/月/㎡。"
                            f"最高值约为最低值的 {ratio:.2f} 倍。", body),
                  Spacer(1, 0.3 * cm), Image(paths["rent"], width=16.5 * cm, height=11.3 * cm), PageBreak()])

    if paths["change"]:
        text = f"环比涨幅最高的是 {rising['区域']}（{rising['环比涨跌幅(%)']:+.2f}%），变化最低的是 {falling['区域']}（{falling['环比涨跌幅(%)']:+.2f}%）。单月变化不宜直接视为长期趋势。"
        story.extend([Paragraph("二、各行政区环比变化", h1), Paragraph(text, body),
                      Spacer(1, 0.3 * cm), Image(paths["change"], width=16.5 * cm, height=11.3 * cm), PageBreak()])

    story.extend([Paragraph("三、行政区租金梯度", h1),
                  Paragraph("按照行政区平均房租的三分位数划分为低、中、高三个相对梯度，用于观察不同区域的租金层次。", body),
                  Spacer(1, 0.3 * cm), Image(paths["level"], width=16 * cm, height=9.8 * cm), PageBreak()])

    rows = [["排名", "行政区", "平均房租（元/月/㎡）", "环比涨跌幅"]]
    for _, row in data.sort_values("北京排名").iterrows():
        rank = int(row["北京排名"]) if pd.notna(row["北京排名"]) else "-"
        change = f"{row['环比涨跌幅(%)']:+.2f}%" if pd.notna(row["环比涨跌幅(%)"]) else "-"
        rows.append([rank, row["区域"], f"{row['平均房租(元/月/㎡)']:.2f}", change])
    result_table = Table(rows, colWidths=[2.2 * cm, 4 * cm, 5.2 * cm, 4 * cm], repeatRows=1)
    result_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "ChineseFont"), ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D6DEE6")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#143D59")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F7FA")]),
    ]))
    conclusion = f"北京各行政区租金存在明显梯度。预算充足、重视中心区位时可重点了解{highest['区域']}等高租金区域；预算敏感时可优先比较{lowest['区域']}等低租金区域，并同步评估通勤距离。"
    story.extend([Paragraph("四、行政区数据表与结论", h1), result_table,
                  Spacer(1, 0.7 * cm), Paragraph(conclusion, note)])
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"分析完成：行政区 {len(data)} 个")
    print(f"PDF报告已生成：{OUTPUT_FILE}")


def main():
    font_path = find_chinese_font()
    data = load_data()
    paths = create_charts(data, font_path)
    create_pdf(data, font_path, paths)


if __name__ == "__main__":
    main()
