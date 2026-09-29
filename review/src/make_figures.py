# -*- coding: utf-8 -*-
"""生成综述中的自绘框架图与数据图（300 dpi PNG，输出到 ../figures/）。

数据来自 research_pack_smart_agriculture/04_data 及本次对原文的核对；
凡是由作者报告数值推算得到的量，图中均标注“推算”或“示意”。
图中文献以 [P13] 这类来源键书写，运行前先执行 `node build_docx.js --refmap-only`
生成 refmap.json，本脚本会把来源键替换成正文中的参考文献编号。
运行：python make_figures.py   （需要 matplotlib；中文字体按 Noto Sans CJK SC / 思源黑体 / 微软雅黑 / 黑体 顺序查找）
"""
import glob
import json
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "figures"))
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- 参考文献编号
_REFMAP_PATH = os.path.join(HERE, "refmap.json")
REFMAP = json.load(open(_REFMAP_PATH, encoding="utf-8")) if os.path.exists(_REFMAP_PATH) else {}
_RUN = re.compile(r"(?:\[[A-Z]\d{2}\])+")


def _compress(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ",".join(str(n) for n in nums[i:j + 1]))
        i = j + 1
    return ",".join(out)


def cite(s):
    """把相邻的 [P13][P15] 来源键替换为 [33,45] 形式的正文编号。"""
    if not isinstance(s, str) or not REFMAP:
        return s

    def repl(m):
        keys = re.findall(r"[A-Z]\d{2}", m.group(0))
        missing = [k for k in keys if k not in REFMAP]
        if missing:
            raise KeyError(f"refmap.json 中缺少 {missing}，请先运行 node build_docx.js --refmap-only")
        return "[" + _compress([REFMAP[k] for k in keys]) + "]"

    return _RUN.sub(repl, s)


_ax_text, _fig_text = Axes.text, Figure.text
Axes.text = lambda self, x, y, s, *a, **k: _ax_text(self, x, y, cite(s), *a, **k)
Figure.text = lambda self, x, y, s, *a, **k: _fig_text(self, x, y, cite(s), *a, **k)

# ---------------------------------------------------------------- 字体
# 可通过环境变量 CJK_FONT_DIR 或 src/fonts/ 目录提供 .otf/.ttf 中文字体（如思源黑体 SC）；
# 否则按下方 font.sans-serif 列表使用系统字体（Windows 下为微软雅黑/黑体）。
for d in (os.environ.get("CJK_FONT_DIR", ""), os.path.join(HERE, "fonts")):
    if d and os.path.isdir(d):
        for f in glob.glob(os.path.join(d, "*.otf")) + glob.glob(os.path.join(d, "*.ttf")):
            font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei", "SimHei",
                                   "WenQuanYi Zen Hei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 8.5

# ---------------------------------------------------------------- 配色（dataviz 参考调色板，浅色模式；已用 validate_palette.js 校验）
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASE, SURF = "#e1e0d9", "#c3c2b7", "#ffffff"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
GREEN, VIOLET, RED = "#008300", "#4a3aa7", "#e34948"
RAMP = {"250": "#86b6ef", "450": "#2a78d6", "650": "#104281"}  # 有序蓝色阶（--ordinal 校验通过）
DPI = 300


def wash(hex_color, a=0.12):
    """把色相按透明度 a 叠加到白底，得到实色浅底。"""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    mix = lambda c: round(255 - (255 - c) * a)
    return "#{:02x}{:02x}{:02x}".format(mix(r), mix(g), mix(b))


def canvas(w_in, h_in, xmax=100.0):
    """等比例坐标画布：x 取 0..xmax，y 取 0..ymax（与图幅同比例）。"""
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ymax = xmax * h_in / w_in
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax, ymax


def box(ax, x, y, w, h, text="", hue=None, fs=8, weight="normal", fc=None, ec=None,
        lw=0.8, tc=INK, r=1.0, ls="-", a=0.12, z=2):
    fc = fc if fc is not None else (wash(hue, a) if hue else SURF)
    ec = ec if ec is not None else (hue if hue else BASE)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
                weight=weight, linespacing=1.3, zorder=z + 1)


def arrow(ax, p1, p2, color=INK2, lw=0.9, ls="-", ms=7, style="-|>", z=4):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
                                 ls=ls, shrinkA=0, shrinkB=0, zorder=z))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, facecolor=SURF)
    plt.close(fig)
    print("saved", path)


def style_axes(ax, grid_axis="x"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(BASE)
        ax.spines[s].set_linewidth(0.8)
    ax.tick_params(colors=INK2, labelsize=7.2, length=2.5, width=0.6)
    ax.grid(axis=grid_axis, color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)


# ================================================================ 分析框架
def fig_framework():
    fig, ax, H = canvas(6.3, 4.1)
    cw, xs = 29.0, (1.5, 35.5, 69.5)
    heads = ["农业现场约束\n（为什么要把 AI 放到端/边）", "端边智能技术体系\n（第 2 章）", "智慧农业垂直应用\n（第 3 章）"]
    hues = [ORANGE, BLUE, AQUA]
    for x, t, c in zip(xs, heads, hues):
        box(ax, x, H - 11.5, cw, 9.0, t, hue=c, fs=8.0, weight="bold", a=0.20)
    cols = [
        ["作业实时性：喷洒/诱控/避障\n需毫秒—百毫秒级闭环", "广域弱网：田间覆盖不稳，\n不能假设网络始终在线",
         "能源受限：电池/太阳能供电，\n计算与执行器争用功率", "环境恶劣：高低温、粉尘、\n雨雾、振动与光照变化",
         "成本与运维：设备分散、\n人工维护困难、价格敏感", "数据量与数据主权：视频\n难以全量上传，涉及隐私"],
        ["硬件平台：MCU（含 NPU）/\n嵌入式 SoC/边缘 GPU/加速卡", "模型轻量化：量化、剪枝、\n知识蒸馏、轻量网络与 NAS",
         "推理框架与工具链：LiteRT Micro、\nONNX Runtime、TensorRT 等", "嵌入式软件栈：RTOS/Linux、\n实时性、功耗管理、OTA、安全",
         "端—边—云协同：分层分工、\n模型下发与数据回流"],
        ["病虫害识别、告警与诱控", "杂草识别与精准施药/除草", "果实检测、计数与估产",
         "作物健康与环境监测", "植保无人机感知与作业", "农业机器人感知与操作"],
    ]
    y0, gap, ybot = H - 14.0, 1.1, 16.5
    for x, items, c in zip(xs, cols, hues):
        n = len(items)
        bh = (y0 - ybot - gap * (n - 1)) / n
        for i, t in enumerate(items):
            box(ax, x, y0 - (i + 1) * bh - i * gap, cw, bh, t, hue=c, fs=6.8 if c != AQUA else 7.1, a=0.07)
    ymid = (y0 + ybot) / 2
    for xa, lab in ((30.5, "约束\n驱动"), (64.5, "支撑\n闭环")):
        arrow(ax, (xa + 0.3, ymid), (xa + 4.7, ymid), lw=1.2, ms=9)
        ax.text(xa + 2.5, ymid + 1.8, lab, ha="center", va="bottom", fontsize=6.5, color=INK2, linespacing=1.2)
    box(ax, 1.5, 1.2, 97.0, 12.0, "", hue=VIOLET, a=0.07)
    ax.text(3.0, 10.3, "关键权衡与评价（第 4 章）", fontsize=7.8, weight="bold", color=INK, va="center")
    for i, m in enumerate(["时延", "带宽", "功耗", "可靠性", "成本", "隐私与安全", "证据质量"]):
        box(ax, 3.0 + i * 10.3, 2.6, 9.3, 5.2, m, hue=VIOLET, fs=6.9, a=0.16, r=0.8)
    box(ax, 76.5, 2.6, 20.5, 8.8, "挑战与局限（第 5 章）\n发展趋势（第 6 章）", fc=SURF, ec=VIOLET, fs=7.0)
    arrow(ax, (74.4, 5.2), (76.3, 5.2), lw=1.0)
    for x in xs:
        arrow(ax, (x + cw / 2, 15.9), (x + cw / 2, 13.5), lw=0.8, ms=6, color=MUTED)
    save(fig, "fig_framework.png")


# ================================================================ 硬件谱系（标称算力点图 + 口径列）
def fig_hardware():
    rows = [  # (名称, 档位, 值, 精度/说明, 功耗口径)
        ("ESP32-S3", "MCU", None, "无 NPU，依靠向量指令", "未公开统一 AI 负载功耗"),
        ("STM32N6（N657）", "MCU", 0.6, "600 GOPS；精度未逐项标注", "未公开整芯片典型值"),
        ("i.MX 93", "SoC", None, "Ethos-U65：256 MAC/cycle", "未公开统一典型 AI 功耗"),
        ("RK3588", "SoC", 6, "6 TOPS；精度未逐项标注", "未公开统一典型 AI 功耗"),
        ("Raspberry Pi 5", "SoC", None, "板载无 NPU（可外接）", "5 V/5 A 为供电规格，非运行功耗"),
        ("Hailo-8L", "ACC", 13, "13 TOPS；精度未标注", "1.5 W（芯片典型）；Pi 5+Hailo 系统 5.4–7.2 W"),
        ("Jetson Orin Nano Super", "ACC", 67, "67 INT8 TOPS；稀疏口径未充分说明", "7–25 W（功耗模式范围）"),
        ("Jetson Orin NX 16GB", "ACC", ((50, 100), (78, 157)), "INT8：稠密—稀疏；普通 / MAXN_SUPER", "10/15/25/40 W（模块功耗档）"),
    ]
    tier_color = {"MCU": BLUE, "SoC": ORANGE, "ACC": AQUA}
    tier_name = {"MCU": "MCU 级", "SoC": "嵌入式 SoC/板卡", "ACC": "边缘 GPU/专用加速器"}
    fig = plt.figure(figsize=(6.3, 3.45), dpi=DPI)
    ax = fig.add_axes([0.205, 0.13, 0.43, 0.75])
    n = len(rows)
    ys = list(range(n))[::-1]
    ax.set_xscale("log")
    ax.set_xlim(0.1, 400)
    ax.set_ylim(-0.7, n - 0.3)
    style_axes(ax, "x")
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.2, color=INK)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xticks([0.1, 1, 10, 100])
    ax.set_xticklabels(["0.1", "1", "10", "100"])
    ax.set_xlabel("厂商标称 AI 峰值算力（TOPS，对数坐标）", fontsize=7.2, color=INK2)
    for y, (name, tier, val, note, pwr) in zip(ys, rows):
        c = tier_color[tier]
        if val is None:
            ax.text(0.115, y, "— 无统一 TOPS 标称 —", va="center", ha="left", fontsize=6.4, color=MUTED)
        elif isinstance(val, tuple):
            for k, (lo, hi) in enumerate(val):
                yy = y + (0.18 if k == 0 else -0.18)
                ax.plot([lo, hi], [yy, yy], color=c, lw=2, solid_capstyle="round", zorder=3)
                ax.scatter([lo, hi], [yy, yy], s=20, color=c, edgecolor=SURF, linewidth=1.1, zorder=4)
                ax.text(lo / 1.18, yy, "普通 50–100" if k == 0 else "MAXN_SUPER 78–157", va="center", ha="right",
                        fontsize=6.1, color=INK2)
        else:
            ax.scatter([val], [y], s=28, color=c, edgecolor=SURF, linewidth=1.2, zorder=4)
            ax.text(val * 1.25, y, f"{val:g}", va="center", fontsize=6.6, color=INK2)
        yf = ax.transData.transform((1, y))[1] / fig.bbox.height
        fig.text(0.655, yf + 0.013, note, fontsize=6.0, color=INK2, va="center")
        fig.text(0.655, yf - 0.023, "功耗：" + pwr, fontsize=6.0, color=MUTED, va="center")
    for yb in (5.5, 2.5):
        ax.axhline(yb, color=GRID, lw=0.8, zorder=1)
    fig.text(0.655, 0.935, "精度/稀疏口径与功耗边界（须与算力同读）", fontsize=6.7, color=INK, weight="bold", va="center")
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=tier_color[k], markersize=6, label=tier_name[k])
               for k in ("MCU", "SoC", "ACC")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.005, 0.995), ncol=3, frameon=False,
               fontsize=6.6, handletextpad=0.3, columnspacing=1.0)
    save(fig, "fig_hardware_spectrum.png")


# ================================================================ 模型轻量化分类
def fig_compression():
    fig, ax, H = canvas(6.3, 3.35)
    box(ax, 30, H - 7.5, 40, 6.0, "模型轻量化与高效推理", hue=BLUE, fs=8.4, weight="bold", a=0.22)
    cols = [
        ("参数/数值层", VIOLET, ["剪枝：非结构化 / 结构化\n（通道、层）", "量化：PTQ（校准）/ QAT；\nINT8、INT4；逐通道/逐张量",
                             "编码压缩：权值共享、\n霍夫曼编码"], "存储↓  分发流量↓",
         "[P02]\n例：[P10] INT8、[P14] PTQ→HEF"),
        ("知识层", ORANGE, ["知识蒸馏：云端大模型/集成\n作教师，端侧小模型作学生", "软标签携带类别关系；\n可与量化、剪枝叠加",
                         "风险：教师偏差、稀有病虫、\n跨季节迁移"], "同等规模下精度↑", "农业设想：\n云端教师→端侧学生"),
        ("结构层", AQUA, ["轻量网络：深度可分离卷积、\nMobileNetV3、Ghost 模块", "硬件感知 NAS：以目标设备\n时延/内存为约束搜索结构",
                        "TinyNAS：为 MCU 内存\n预算定制网络"], "计算量↓（FLOPs、参数）",
         "[P01][P04]\n例：[P09] MobileNetV2、[P13] Ghost"),
        ("执行/系统层", GREEN, ["图优化与算子融合；\n推理引擎（TensorRT 等）", "内存调度：峰值内存\n（TinyEngine）与张量复用",
                           "优化内核：CMSIS-NN 等；\nCPU/GPU/NPU/DLA 异构调度"], "实测时延↓  峰值内存↓",
         "[P01]\n须在目标硬件上实测"),
    ]
    cw, gx = 23.2, 1.4
    x0 = (100 - 4 * cw - 3 * gx) / 2
    top = H - 10.5
    bh = 6.4
    for i, (title, c, items, gain, ref) in enumerate(cols):
        x = x0 + i * (cw + gx)
        arrow(ax, (50, H - 7.5), (x + cw / 2, top + 0.2), lw=0.8, ms=6, color=MUTED)
        box(ax, x, top - 5.2, cw, 5.2, title, hue=c, fs=7.8, weight="bold", a=0.22)
        for j, t in enumerate(items):
            box(ax, x, top - 6.4 - (j + 1) * bh - j * 0.9, cw, bh, t, hue=c, fs=6.3, a=0.07)
        yb = top - 6.4 - 3 * bh - 2 * 0.9 - 1.2
        box(ax, x, yb - 4.4, cw, 4.4, gain, fc=SURF, ec=c, fs=6.8, weight="bold")
        ax.text(x + cw / 2, yb - 7.3, ref, ha="center", va="center", fontsize=5.7, color=MUTED, linespacing=1.3)
    ax.text(50, 1.6, "注：各层收益作用在不同指标上，不能简单相乘；“文件变小”“FLOPs 变少”不等于目标设备上实测变快，须以同一硬件、同一输入、同一精度复测。",
            ha="center", va="center", fontsize=6.2, color=INK2)
    save(fig, "fig_compression_taxonomy.png")


# ================================================================ 部署工具链与运维闭环
def fig_pipeline():
    fig, ax, H = canvas(6.3, 3.52)
    tw, tg, th = 21.5, 3.33, 8.0
    top_y = H - 2.0 - th
    for i, t in enumerate(["农业数据\n采集·标注·划分\n（跨地块/跨季测试集）", "基线训练\nPyTorch / TensorFlow",
                           "压缩\n剪枝·蒸馏·QAT", "导出中间表示\nONNX / TFLite"]):
        x = 2 + i * (tw + tg)
        box(ax, x, top_y, tw, th, t, hue=VIOLET, fs=6.6, a=0.10)
        if i < 3:
            arrow(ax, (x + tw + 0.3, top_y + th / 2), (x + tw + tg - 0.3, top_y + th / 2))
    ax.text(2, top_y - 1.4, "按目标硬件分支编译（ONNX Runtime 亦可通过 Execution Provider 调用 TensorRT、OpenVINO 或 NPU 后端）",
            fontsize=6.1, color=INK2, va="top")
    xe = 2 + 3 * (tw + tg) + tw / 2
    routes = [
        ("MCU 路线", "例：ESP32-S3 [P12]、STM32N6", BLUE,
         "LiteRT for Microcontrollers：\n模型转 C 数组 + 静态张量工作区", "CMSIS-NN / ESP-NN 优化内核，\n链接进固件（RTOS 任务）"),
        ("NPU-SoC 路线", "例：RK3588、i.MX 93", ORANGE,
         "厂商 NPU 工具链\n（RKNN、eIQ、ST Edge AI 等）", "量化校准 → NPU 模型文件，\n嵌入式 Linux 运行时加载"),
        ("边缘 GPU 路线", "例：Jetson Orin NX [P10]", AQUA,
         "TensorRT 构建引擎\nFP16 / INT8 校准", "序列化 .engine → 反序列化推理\n（CUDA / DLA）"),
        ("专用加速器路线", "例：Pi 5 + Hailo-8L [P14]", GREEN,
         "Hailo Dataflow Compiler\nPTQ 校准 → HEF", "HailoRT + GStreamer\n宿主 CPU 调度"),
    ]
    rh, rg = 5.6, 1.0
    ry_top = top_y - 4.3
    arrow(ax, (xe, top_y - 0.2), (xe, ry_top + 0.3), lw=0.8, ms=6, color=MUTED)
    for k, (name, ex, c, s1, s2) in enumerate(routes):
        y = ry_top - (k + 1) * rh - k * rg
        box(ax, 2, y, 19.0, rh, "", hue=c, a=0.22)
        ax.text(11.5, y + rh * 0.64, name, ha="center", va="center", fontsize=6.9, weight="bold", color=INK)
        ax.text(11.5, y + rh * 0.28, ex, ha="center", va="center", fontsize=5.6, color=INK2)
        box(ax, 23.0, y, 36.0, rh, s1, hue=c, fs=6.2, a=0.07)
        box(ax, 61.0, y, 37.0, rh, s2, hue=c, fs=6.2, a=0.07)
        arrow(ax, (21.1, y + rh / 2), (22.9, y + rh / 2), ms=5, lw=0.7)
        arrow(ax, (59.1, y + rh / 2), (60.9, y + rh / 2), ms=5, lw=0.7)
    r_bot = ry_top - 4 * rh - 3 * rg
    by_top, bh = r_bot - 3.6, 6.6
    steps = [("实机验证\n精度回退·P50/P99 时延\n功耗·峰值内存·温度", RED), ("签名与版本管理\n模型+运行库兼容性检查", VIOLET),
             ("OTA 灰度发布\nA/B 分区·失败回滚", VIOLET), ("运行监测\n置信度·数据漂移·日志", VIOLET)]
    for i, (t, c) in enumerate(steps):
        x = 2 + i * (tw + tg)
        box(ax, x, by_top - bh, tw, bh, t, hue=c, fs=6.2, a=0.09)
        if i < 3:
            arrow(ax, (x + tw + 0.3, by_top - bh / 2), (x + tw + tg - 0.3, by_top - bh / 2))
    # 各路线汇入实机验证
    ax.plot([50, 50, 12.75], [r_bot - 0.2, r_bot - 1.6, r_bot - 1.6], color=INK2, lw=0.9, zorder=3)
    arrow(ax, (12.75, r_bot - 1.6), (12.75, by_top + 0.2), lw=0.9, ms=6)
    ax.text(51.2, r_bot - 1.1, "各路线产物均须在目标设备上复测", fontsize=5.9, color=INK2, va="center")
    # 数据回流（非实时运维闭环）
    yl = by_top - bh - 2.2
    xm = 2 + 3 * (tw + tg) + tw / 2
    dash = (0, (3, 2))
    ax.plot([xm, xm, 0.9, 0.9], [by_top - bh - 0.2, yl, yl, top_y + th / 2], color=MUTED, lw=0.8, ls=dash, zorder=3)
    arrow(ax, (0.9, top_y + th / 2), (1.9, top_y + th / 2), lw=0.8, color=MUTED, ms=6)
    ax.text(50, yl - 1.2, "数据回流：困难样本与新地块数据 → 再标注 → 再训练（虚线表示非实时的运维闭环）",
            fontsize=6.1, color=INK2, ha="center", va="center")
    save(fig, "fig_deployment_pipeline.png")


# ================================================================ 嵌入式软件栈
def fig_stack():
    fig, ax, H = canvas(6.3, 3.9)
    lx, lw_ = 2.0, 72.0
    layers = [
        ("应用任务链", BLUE, ["采集", "预处理", "推理", "后处理", "决策与\n安全约束", "执行", "事件上报"]),
        ("中间件与服务", AQUA, ["MQTT / LoRaWAN\n/ CAN-ISOBUS", "ROS 2 等\n机器人中间件", "本地缓存与\n断网续传", "日志·时间同步\n设备管理"]),
        ("推理运行时", VIOLET, ["LiteRT Micro\n+ CMSIS-NN", "ONNX\nRuntime", "TensorRT", "OpenVINO", "HailoRT", "厂商 NPU\n运行时"]),
        ("操作系统", ORANGE, ["RTOS（FreeRTOS 等）\n确定性调度·任务优先级", "嵌入式 Linux\n多进程·驱动·容器", "异构组合：Linux 做感知\n+ MCU 做控制 [P13]"]),
        ("板级支持与驱动", GREEN, ["BSP / 启动", "相机·ISP", "DMA", "UART/SPI/I²C\nCAN", "GPIO/PWM", "电源管理\nDVFS·休眠"]),
        ("硬件", INK2, ["相机/传感器", "MCU / SoC\nCPU+NPU/GPU", "执行器\n阀·风机·激光", "通信模组\nLoRa/4G/5G", "电源\n电池/太阳能"]),
    ]
    lh, lg = 8.0, 1.2
    ytop = H - 4.2
    ax.text(lx, H - 2.1, "分层结构（自下而上）", fontsize=7.0, weight="bold", color=INK, va="center")
    for i, (name, c, items) in enumerate(layers):
        y = ytop - (i + 1) * lh - i * lg
        box(ax, lx, y, lw_, lh, "", hue=c, a=0.07)
        ax.text(lx + 1.0, y + lh / 2, name, fontsize=6.9, weight="bold", color=INK, va="center", ha="left")
        n = len(items)
        ix0, iw_total, gap = lx + 12.5, lw_ - 13.5, 0.8
        iw = (iw_total - gap * (n - 1)) / n
        for j, t in enumerate(items):
            box(ax, ix0 + j * (iw + gap), y + 1.1, iw, lh - 2.2, t, fc=SURF, ec=c if c != INK2 else BASE,
                fs=5.8, lw=0.7, r=0.6)
    y_last = ytop - 6 * lh - 5 * lg
    sx, sw = 76.5, 21.5
    ax.text(sx, H - 2.1, "横切关注点（贯穿各层）", fontsize=7.0, weight="bold", color=INK, va="center")
    concerns = [("实时性", RED, "任务优先级与截止期\n看门狗·最坏情况时延\n推理与控制路径分离"),
                ("功耗", YELLOW, "事件触发与占空比\n休眠唤醒·DVFS\n算力与执行器功率预算"),
                ("安全", VIOLET, "设备身份·安全启动\n固件/模型签名\n最小权限接口"),
                ("OTA 与运维", BLUE, "A/B 分区·失败回滚\n模型与运行库版本兼容\n灰度发布与状态记录")]
    cg = 1.2
    ch = (ytop - y_last - 3 * cg) / 4
    for i, (t, c, d) in enumerate(concerns):
        y = ytop - (i + 1) * ch - i * cg
        box(ax, sx, y, sw, ch, "", hue=c, a=0.09)
        ax.text(sx + sw / 2, y + ch - 2.2, t, ha="center", va="center", fontsize=7.2, weight="bold", color=INK)
        ax.text(sx + sw / 2, y + ch / 2 - 1.5, d, ha="center", va="center", fontsize=5.9, color=INK2, linespacing=1.35)
    save(fig, "fig_software_stack.png")


# ================================================================ 端—边—云协同架构
def fig_architecture():
    fig, ax, H = canvas(6.3, 4.02)
    tiers = [
        ("云", "中心云 / 农业大数据平台", VIOLET,
         ["大模型/教师\n模型训练", "跨地块数据\n汇聚与标注", "农事知识服务\n与决策支持", "模型仓库·版本\nOTA 编排"], "分钟—天级\n全局优化"),
        ("边", "场边网关 / 边缘服务器 / 农机主控", BLUE,
         ["多节点汇聚\n多模态融合", "较大模型推理\n（时序/多目标）", "多机协同\n任务调度", "缓存·断网续传\n联邦聚合*"], "百毫秒—秒级\n区域协同"),
        ("端", "传感节点 / 相机 / 无人机 / 农机终端", AQUA,
         ["采集与预处理", "轻量模型\n实时推理", "控制逻辑\n安全约束", "执行器：喷头\n风机·激光·阀门"], "毫秒—百毫秒级\n断网可自治"),
    ]
    th, tg = 12.6, 6.2
    ytop = H - 5.0
    tx, tw = 2.0, 76.0
    ys = []
    for i, (short, name, c, items, scale) in enumerate(tiers):
        y = ytop - (i + 1) * th - i * tg
        ys.append(y)
        box(ax, tx, y, tw, th, "", hue=c, a=0.08)
        box(ax, tx + 1.0, y + 1.0, 7.0, th - 2.0, short, hue=c, fs=12, weight="bold", a=0.25)
        ax.text(tx + 9.5, y + th - 2.0, name, fontsize=7.1, weight="bold", color=INK, va="center")
        n = len(items)
        iw = (tw - 11.0 - 0.9 * (n - 1)) / n
        for j, t in enumerate(items):
            box(ax, tx + 9.5 + j * (iw + 0.9), y + 1.1, iw, th - 4.7, t, fc=SURF, ec=c, fs=6.2, lw=0.7, r=0.6)
        ax.text(89.0, y + th / 2, scale, ha="center", va="center", fontsize=6.5, color=INK2, linespacing=1.4)
    ax.text(89.0, ytop + 1.6, "典型时间尺度", ha="center", va="center", fontsize=6.8, weight="bold", color=INK)
    for yl in ys[:2]:
        ax.plot([82.5, 95.5], [yl - tg / 2, yl - tg / 2], color=GRID, lw=0.8)
    flows = [("汇总数据、样本、告警（4G/5G/光纤）", "经验证的模型\n版本与策略（OTA）"),
             ("事件摘要、关键帧、特征（LoRa/4G/Wi-Fi）", "下发模型、参数\n与作业处方")]
    for i, (up, down) in enumerate(flows):
        yu, yl = ys[i], ys[i + 1] + th
        arrow(ax, (22, yl + 0.3), (22, yu - 0.3), lw=1.1, ms=7)
        arrow(ax, (58, yu - 0.3), (58, yl + 0.3), lw=1.0, ms=7, ls=(0, (3, 2)))
        ax.text(23.2, (yu + yl) / 2, up, fontsize=6.1, color=INK2, va="center")
        ax.text(59.2, (yu + yl) / 2, down, fontsize=6.1, color=INK2, va="center", linespacing=1.25)
    yb = ys[2]
    arrow(ax, (tx + tw - 1.5, yb + 0.55), (tx + 9.8, yb + 0.55), color=RED, lw=1.2, ms=7)
    ax.text(tx + 9.5 + (tw - 9.5) / 2, yb - 1.4, "本地实时闭环：感知 → 推理 → 控制 → 执行（不依赖网络；置信度低时降级为告警或人工接管）",
            ha="center", va="center", fontsize=6.2, color=RED)
    ax.text(2.0, 1.0, "* 联邦学习聚合在农业中仍以研究为主 [P17]。实线箭头＝实时上行数据流，虚线箭头＝非实时下发/运维流；并非所有任务都需要三层齐全。",
            fontsize=5.8, color=MUTED, va="bottom")
    save(fig, "fig_cloud_edge_device.png")


# ================================================================ 应用全景与证据成熟度
def fig_maturity():
    fig = plt.figure(figsize=(6.3, 3.85), dpi=DPI)
    ax = fig.add_axes([0.215, 0.13, 0.775, 0.74])
    tasks = ["病虫害识别\n告警与诱控", "叶部病害检测\n（端侧部署）", "杂草识别与\n精准施药/除草",
             "果实检测\n计数与估产", "作物健康与\n环境监测", "植保无人机\n感知与作业"]
    levels = ["离线算法 /\n数据集评估", "实机部署测试\n（实验室/数据集）", "短期田间\n试运行", "商业产品 /\n规模应用"]
    ny = len(tasks)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.6, ny - 0.4)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(range(4))
    ax.set_xticklabels(levels, fontsize=6.9, color=INK, linespacing=1.2)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    ax.set_yticks(range(ny))
    ax.set_yticklabels(tasks[::-1], fontsize=6.9, color=INK, linespacing=1.2)
    for k in range(4):
        ax.axvspan(k - 0.5, k + 0.5, color=wash(BLUE, 0.03 + 0.03 * k), zorder=0, lw=0)
        if k:
            ax.axvline(k - 0.5, color=SURF, lw=2, zorder=1)
    for j in range(ny - 1):
        ax.axhline(j + 0.5, color=GRID, lw=0.6, zorder=1)
    pts = [  # (任务行, 成熟度列, 标签, 类型, 纵向偏移)
        (0, 1, "[P09] 树莓派 5 + GSM/GPRS", "R", 0.22),
        (0, 1, "[P13] Xavier NX + ESP32\n识别—诱捕闭环", "R", -0.16),
        (0, 2, "[P12] ESP32-S3 TinyML\n（7 天部署，指标存疑）", "Q", 0.0),
        (1, 1, "[P10] Orin NX，INT8", "R", 0.0),
        (2, 1, "[P14] Pi 5 + Hailo-8L", "R", 0.0),
        (2, 3, "See & Spray（Deere）", "C", 0.18),
        (2, 3, "LaserWeeder G2", "C", -0.18),
        (3, 1, "[P08] Jetson AGX 视频估产", "R", 0.18),
        (3, 1, "[P11] TX2 番茄机器人", "R", -0.18),
        (4, 2, "[P15] Nano + 边缘服务器\n（作者报告半年部署）", "Q", 0.0),
        (5, 3, "极飞 XAG P150", "C", 0.0),
    ]
    style = {"R": ("o", BLUE, BLUE), "Q": ("o", BLUE, SURF), "C": ("s", ORANGE, ORANGE)}
    for row, col, lab, kind, dy in pts:
        y = ny - 1 - row + dy
        x = col - 0.40
        mk, ec, fc = style[kind]
        ax.scatter([x], [y], s=32, marker=mk, facecolor=fc, edgecolor=ec, linewidth=1.3, zorder=4)
        ax.text(x + 0.07, y, lab, va="center", ha="left", fontsize=6.0, color=INK2, linespacing=1.2, zorder=5)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markeredgecolor=BLUE, markersize=6, label="研究原型（作者报告）"),
               Line2D([0], [0], marker="o", color="w", markerfacecolor=SURF, markeredgecolor=BLUE, markeredgewidth=1.3,
                      markersize=6, label="研究系统，关键指标待复核"),
               Line2D([0], [0], marker="s", color="w", markerfacecolor=ORANGE, markeredgecolor=ORANGE, markersize=6, label="商业产品（厂商口径）")]
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.01, 0.0), ncol=3, frameon=False, fontsize=6.5,
               handletextpad=0.3, columnspacing=1.2)
    fig.text(0.02, 0.945, "证据成熟度 →", fontsize=6.8, color=MUTED, va="center")
    save(fig, "fig_application_maturity.png")


# ================================================================ 时延预算与移动作业换算
def fig_latency():
    fig = plt.figure(figsize=(6.3, 3.75), dpi=DPI)
    fig.text(0.06, 0.975, "(a) 害虫诱捕原型的时延构成 [P13]：端到端 36.8 ms，其中闭环控制 14.8 ms（作者报告均值，非 P99/最坏情况）",
             fontsize=6.9, color=INK, weight="bold", va="top")
    bx = fig.add_axes([0.06, 0.845, 0.90, 0.075])
    bx.set_xlim(0, 37.2)
    bx.set_ylim(0, 1)
    bx.axis("off")
    bx.plot([22.0, 22.0, 36.55, 36.55], [0.05, 0.45, 0.45, 0.05], color=RED, lw=0.9)
    bx.text((22.0 + 36.55) / 2, 0.58, "闭环控制时延 14.8 ms", ha="center", va="bottom", fontsize=6.3, color=RED)
    bx.plot([0.0, 0.0, 21.7, 21.7], [0.05, 0.45, 0.45, 0.05], color=MUTED, lw=0.9)
    bx.text(10.9, 0.58, "36.8 − 14.8 ≈ 22.0 ms（推算，含采集与 TensorRT 推理）", ha="center", va="bottom", fontsize=6.2, color=INK2)
    ax = fig.add_axes([0.06, 0.69, 0.90, 0.15])
    segs = [("图像采集+推理+后处理等", 22.0, BLUE, True), ("UART 传输", 4.3, AQUA, False),
            ("ESP32 控制逻辑+继电器", 7.6, ORANGE, False), ("其他系统开销", 2.9, BASE, True)]
    x = 0.0
    for name, v, c, derived in segs:
        fc = wash(c, 0.45) if derived else c
        ax.barh([0], [v - 0.25], left=[x], height=0.62, color=fc, edgecolor="none", zorder=3)
        if v >= 7:
            ax.text(x + (v - 0.25) / 2, 0, f"{v:.1f} ms" + ("（推算）" if derived else ""), ha="center", va="center",
                    fontsize=6.4, color=INK if derived or c != BLUE else SURF, zorder=4)
        else:
            ax.text(x + (v - 0.25) / 2, 0.52, f"{v:.1f}" + ("（推算）" if derived else ""), ha="center", va="bottom",
                    fontsize=6.2, color=INK2)
        ax.text(x + (v - 0.25) / 2, -0.55, name, ha="center", va="top", fontsize=6.0, color=INK2)
        x += v
    ax.set_xlim(0, 37.2)
    ax.set_ylim(-1.1, 1.1)
    ax.axis("off")
    # (b) 分组条形图：不同车速下的位移
    fig.text(0.06, 0.615, "(b) 移动作业中的时延—位移换算（示意）：距离 ＝ 车速 × 时延", fontsize=6.9, color=INK, weight="bold", va="top")
    cx = fig.add_axes([0.235, 0.09, 0.45, 0.46])
    style_axes(cx, "x")
    refs = ["36.8 ms（[P13] 端到端）", "120 ms（[P15] 端侧 LSTM）", "210 ms（[P15] 混合方案）", "980 ms（[P15] 云端）"]
    lat = [36.8, 120, 210, 980]
    speeds = [(6, RAMP["250"], "6 km/h"), (12, RAMP["450"], "12 km/h"), (24, RAMP["650"], "24 km/h（≈15 mph）")]
    ys = list(range(len(lat)))[::-1]
    hgt = 0.24
    for k, (kmh, c, lab) in enumerate(speeds):
        v = kmh / 3.6
        off = (1 - k) * hgt
        vals = [v * t / 1000 for t in lat]
        cx.barh([y + off for y in ys], vals, height=hgt - 0.03, color=c, zorder=3, label=lab)
        if kmh == 24:
            for y, d in zip(ys, vals):
                cx.text(d + 0.08, y + off, f"{d:.2f} m", va="center", fontsize=6.0, color=INK2)
    cx.set_yticks(ys)
    cx.set_yticklabels([cite(r) for r in refs], fontsize=6.4)
    cx.tick_params(axis="y", length=0)
    cx.set_xlim(0, 7.6)
    cx.set_xlabel("时延期间的行进距离（m）", fontsize=6.8, color=INK2)
    cx.legend(loc="upper right", fontsize=6.0, frameon=False, handlelength=1.0, borderaxespad=0.2)
    fig.text(0.715, 0.305, "读图：以约 24 km/h（≈15 mph）行进时，\n每 100 ms 时延对应约 0.67 m 位移，\n喷头须在此之前完成判别与开闭；\n约 1 s 的云端往返对应约 6.5 m，\n难以满足逐株靶向施药。\n\n注：参考时延来自不同系统，\n仅作量级示意，不代表其在\n喷雾场景中的实测表现。",
             fontsize=6.0, color=INK2, va="center", linespacing=1.4)
    save(fig, "fig_latency_budget.png")


# ================================================================ YOLO-PLNet 数值精度权衡
def fig_precision():
    modes = ["FP32", "FP16", "INT8"]
    cols = [RAMP["250"], RAMP["450"], RAMP["650"]]
    data = [("推理延迟（ms）", [32.5, 19.1, 11.8], 40), ("吞吐（FPS）", [15.4, 28.2, 41.3], 50),
            ("功耗（W）", [5.2, 4.1, 3.4], 6.5), ("mAP@0.5（%）", [98.1, 98.0, 97.5], None)]
    fig = plt.figure(figsize=(6.3, 2.5), dpi=DPI)
    for (title, vals, ymax), l in zip(data, [0.06, 0.305, 0.55, 0.795]):
        ax = fig.add_axes([l, 0.30, 0.185, 0.56])
        style_axes(ax, "y")
        ax.set_title(title, fontsize=7.2, color=INK, pad=4)
        if ymax is not None:
            ax.bar(range(3), vals, width=0.55, color=cols, zorder=3)
            ax.set_ylim(0, ymax)
            for i, v in enumerate(vals):
                ax.text(i, v + ymax * 0.02, f"{v:g}", ha="center", va="bottom", fontsize=6.4, color=INK2)
        else:
            ax.plot(range(3), vals, color=GRID, lw=1.0, zorder=2)
            ax.scatter(range(3), vals, s=34, color=cols, edgecolor=SURF, linewidth=1.2, zorder=4)
            ax.set_ylim(97.0, 98.6)
            for i, v in enumerate(vals):
                ax.text(i, v + 0.08, f"{v:.1f}", ha="center", va="bottom", fontsize=6.4, color=INK2)
            ax.text(1, 97.05, "纵轴截断，差异≤0.6 个百分点", ha="center", va="bottom", fontsize=5.7, color=MUTED)
        ax.set_xticks(range(3))
        ax.set_xticklabels(modes, fontsize=6.8)
        ax.set_xlim(-0.6, 2.6)
    fig.text(0.06, 0.035, "注：据文献[P10]表 9（Jetson Orin NX 16GB，640×640，作者报告）。按 1000/延迟换算的帧率为 30.8/52.4/84.7 FPS，与所报 FPS 不一致；\n"
             "同文表 6 与其他检测器比较时另报推理时间 15.6 ms（未注明精度）。计时范围与功耗采样边界未明，本图仅说明量化的方向性收益，不作跨平台比较。",
             fontsize=5.8, color=INK2, va="bottom", linespacing=1.45)
    save(fig, "fig_precision_tradeoff.png")


# ================================================================ 本地/云端/混合方案对比（P15 表1）
def fig_hybrid():
    methods = ["阈值法", "端侧 LSTM\n（Jetson Nano）", "云端 PINN", "混合方案\n（端 LSTM + 边缘修正）"]
    f1_soy, f1_cit = [0.61, 0.72, 0.85, 0.89], [0.55, 0.68, 0.79, 0.83]
    err_soy, err_cit = [0, 0, 0, 0.02], [0, 0, 0, 0.03]
    lat, ene = [50, 120, 980, 210], [0.8, 3.2, 18.7, 5.1]
    fig = plt.figure(figsize=(6.3, 2.65), dpi=DPI)
    ys = list(range(4))[::-1]
    ax = fig.add_axes([0.175, 0.26, 0.27, 0.58])
    style_axes(ax, "x")
    h = 0.36
    ax.barh([y + h / 2 for y in ys], f1_soy, height=h - 0.05, color=BLUE, zorder=3, label="大豆")
    ax.barh([y - h / 2 for y in ys], f1_cit, height=h - 0.05, color=ORANGE, zorder=3, label="柑橘")
    for y, v, e in zip(ys, f1_soy, err_soy):
        ax.text(v + e + 0.02, y + h / 2, f"{v:.2f}" + (f"±{e:.2f}" if e else ""), va="center", fontsize=5.9, color=INK2)
    for y, v, e in zip(ys, f1_cit, err_cit):
        ax.text(v + e + 0.02, y - h / 2, f"{v:.2f}" + (f"±{e:.2f}" if e else ""), va="center", fontsize=5.9, color=INK2)
    ax.errorbar([f1_soy[3]], [ys[3] + h / 2], xerr=[[0.02], [0.02]], fmt="none", ecolor=INK2, elinewidth=0.8, capsize=1.5, zorder=4)
    ax.errorbar([f1_cit[3]], [ys[3] - h / 2], xerr=[[0.03], [0.03]], fmt="none", ecolor=INK2, elinewidth=0.8, capsize=1.5, zorder=4)
    ax.set_xlim(0, 1.25)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_yticks(ys)
    ax.set_yticklabels(methods, fontsize=6.6, linespacing=1.2)
    ax.tick_params(axis="y", length=0)
    ax.set_title("胁迫预测 F1", fontsize=7.2, color=INK, pad=12)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=2, fontsize=6.0, frameon=False, handlelength=1.0,
              borderaxespad=0.0, columnspacing=1.0)
    for pos, vals, title, xmax, fmt, dx in ((0.49, lat, "端到端时延（ms）", 1200, "{:g}", 22), (0.745, ene, "能量（J/次预测）", 23, "{:g}", 0.4)):
        bx = fig.add_axes([pos, 0.26, 0.225, 0.58])
        style_axes(bx, "x")
        bx.barh(ys, vals, height=0.5, color=BLUE, zorder=3)
        for y, v in zip(ys, vals):
            bx.text(v + dx, y, fmt.format(v), va="center", fontsize=6.2, color=INK2)
        bx.set_xlim(0, xmax)
        bx.set_yticks(ys)
        bx.set_yticklabels([])
        bx.tick_params(axis="y", length=0)
        bx.set_title(title, fontsize=7.2, color=INK, pad=12)
    fig.text(0.02, 0.03, "注：据文献[P15]表 1（5 次独立运行均值，作者报告）。各方案的模型、硬件（Jetson Nano / A100 边缘服务器 / 云）与网络同时改变，差异不能归因于部署位置本身；\n"
             "能量是否计入服务器与通信、LoRaWAN 平均 2.3 KB 载荷下 210 ms 端到端时延如何实现，原文未充分说明（见 4.2 节）。",
             fontsize=5.7, color=INK2, va="bottom", linespacing=1.45)
    save(fig, "fig_edge_cloud_hybrid.png")


# ================================================================ Hailo 杂草研究：量化精度损失与计时口径（P14 表1）
def fig_hailo_quant():
    rows = [("YOLOv8n", 0.50, 0.29, 4.1, 9.3), ("YOLOv10n", 0.46, 0.33, 4.0, 10.2), ("YOLOv10s", 0.47, 0.33, 3.9, 18.9),
            ("YOLOv10b", 0.49, 0.42, 2.8, 41.6), ("YOLOv10x", 0.51, 0.46, 2.6, 58.8), ("YOLOv11n", 0.55, 0.36, 4.2, 10.5),
            ("YOLOv11s", 0.51, 0.36, 3.9, 26.5), ("YOLOv11m", 0.56, 0.49, 2.6, 47.8), ("YOLOv11l", 0.52, 0.40, 2.9, 49.6),
            ("YOLOv11x", 0.47, 0.36, 2.0, 58.8)]
    fig = plt.figure(figsize=(6.3, 3.2), dpi=DPI)
    ax = fig.add_axes([0.105, 0.2, 0.36, 0.64])
    style_axes(ax, "x")
    ys = list(range(len(rows)))[::-1]
    for y, (name, pt, hef, _, _) in zip(ys, rows):
        ax.plot([hef, pt], [y, y], color=GRID, lw=2.2, solid_capstyle="round", zorder=2)
        ax.scatter([pt], [y], s=24, color=RAMP["250"], edgecolor=SURF, linewidth=1.0, zorder=3)
        ax.scatter([hef], [y], s=24, color=RAMP["650"], edgecolor=SURF, linewidth=1.0, zorder=4)
        ax.text(hef - 0.012, y, f"−{pt - hef:.2f}", ha="right", va="center", fontsize=5.8, color=INK2)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=6.4)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0.18, 0.62)
    ax.set_xlabel("mAP@0.5（独立测试集）", fontsize=6.8, color=INK2)
    ax.set_title("(a) 量化编译前后的精度", fontsize=7.2, color=INK, pad=16, loc="left", weight="bold")
    hd = [Line2D([0], [0], marker="o", color="w", markerfacecolor=RAMP["250"], markersize=6, label="PyTorch（FP32）"),
          Line2D([0], [0], marker="o", color="w", markerfacecolor=RAMP["650"], markersize=6, label="HEF（Hailo-8L，PTQ）")]
    ax.legend(handles=hd, loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=2, frameon=False, fontsize=6.0,
              handletextpad=0.2, columnspacing=0.8, borderaxespad=0.1)
    bx = fig.add_axes([0.585, 0.2, 0.39, 0.64])
    style_axes(bx, "y")
    bx.scatter([r[4] for r in rows], [r[3] for r in rows], s=28, color=BLUE, edgecolor=SURF, linewidth=1.1, zorder=3)
    bx.text(13.0, 4.45, "n 版本（9–11 MB）：4.0–4.2 ms", fontsize=5.9, color=INK2, va="center")
    bx.text(57.5, 1.72, "YOLOv11x（58.8 MB）：2.0 ms", fontsize=5.9, color=INK2, va="center", ha="right")
    bx.text(40.5, 3.12, "b/m/l/x：2.6–2.9 ms", fontsize=5.9, color=INK2, va="center", ha="left")
    bx.set_xlim(0, 65)
    bx.set_ylim(0, 5)
    bx.set_xlabel("HEF 模型文件大小（MB）", fontsize=6.8, color=INK2)
    bx.set_ylabel("报告的中位延迟（ms）", fontsize=6.8, color=INK2)
    bx.set_title("(b) 模型越大，报告延迟反而越短", fontsize=7.2, color=INK, pad=16, loc="left", weight="bold")
    bx.text(64, 0.25, "计时起点：已处理的帧缓冲进入应用回调\n（推理与 NMS 已在此前完成）", ha="right", va="bottom",
            fontsize=5.9, color=INK2, linespacing=1.35)
    fig.text(0.02, 0.02, "数据：文献[P14]表 1（作者报告）。(a) 中数字为 mAP@0.5 的绝对下降量；(b) 中延迟与模型规模呈反向关系，提示所测时间主要为后处理与结果解析。",
             fontsize=5.8, color=INK2, va="bottom")
    save(fig, "fig_hailo_quant_timing.png")


# ================================================================ 技术与政策演进时间线
def fig_timeline():
    def pos(yr):
        return yr if yr <= 2028.4 else {2030: 2029.35, 2035: 2030.35}[int(yr)]

    fig = plt.figure(figsize=(6.3, 3.9), dpi=DPI)
    ax = fig.add_axes([0.115, 0.08, 0.875, 0.84])
    ax.set_xlim(2014.4, 2030.9)
    ax.set_ylim(0, 3)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE)
    yrs = list(range(2015, 2029)) + [2030, 2035]
    ax.set_xticks([pos(y) for y in yrs])
    ax.set_xticklabels([str(y) for y in yrs], fontsize=6.3, color=INK2)
    ax.tick_params(axis="x", length=2.5, width=0.6)
    ax.set_yticks([])
    ax.text(2028.85, -0.02, "//", ha="center", va="center", fontsize=8, color=MUTED, clip_on=False)
    lanes = [(2.5, "方法与工具", BLUE), (1.5, "硬件平台", ORANGE), (0.5, "农业应用\n与政策", AQUA)]
    for y, name, c in lanes:
        ax.axhspan(y - 0.5, y + 0.5, color=wash(c, 0.05), lw=0, zorder=0)
        ax.text(2014.3, y, name, ha="right", va="center", fontsize=7.0, weight="bold", color=INK, linespacing=1.2)
    for yb in (1, 2):
        ax.axhline(yb, color=SURF, lw=2, zorder=1)
    for y in yrs:
        ax.axvline(pos(y), color=GRID, lw=0.5, zorder=0.5)
    ev = [  # (年份, 泳道, 标签, 纵向偏移, 是否目标, 水平对齐)
        (2015.2, 2.5, "知识蒸馏", 0.24, False, "center"),
        (2015.8, 2.5, "Deep Compression[P02]", -0.24, False, "center"),
        (2017.95, 2.5, "INT8 整数推理", 0.24, False, "center"),
        (2019.35, 2.5, "MobileNetV3[P04]", -0.24, False, "center"),
        (2020.5, 2.5, "MCUNet[P01]", 0.24, False, "center"),
        (2023.0, 2.5, "LiteRT/ONNX Runtime/TensorRT\n等工具链持续演进", -0.26, False, "center"),
        (2025.4, 2.5, "轻量 LLM 边缘部署探索[P18]", 0.24, False, "center"),
        (2020.99, 1.5, "ESP32-S3", 0.24, False, "center"),
        (2021.85, 1.5, "i.MX 93", -0.24, False, "center"),
        (2022.7, 1.5, "RK3588", 0.24, False, "center"),
        (2023.55, 1.5, "Hailo-8L（至迟）", 0.40, False, "center"),
        (2023.74, 1.5, "Raspberry Pi 5", -0.24, False, "center"),
        (2024.94, 1.5, "STM32N6\nOrin Nano Super", 0.24, False, "left"),
        (2021.0, 0.5, "See & Spray 推出", 0.24, False, "center"),
        (2023.3, 0.5, "果园挂果量边缘估测[P08]", -0.24, False, "center"),
        (2024.72, 0.5, "See & Spray\n超 100 万英亩", 0.24, False, "right"),
        (2024.85, 0.5, "指导意见/行动计划", 0.42, False, "center"),
        (2025.5, 0.5, "[P09][P10][P11] 端侧部署研究", -0.34, False, "left"),
        (2026.45, 0.5, "[P12][P13][P14][P15]\n闭环/协同研究", 0.24, False, "center"),
        (2026.95, 0.5, "信息化率≥30%", -0.20, True, "center"),
        (2028.0, 0.5, "≥32%", 0.24, True, "center"),
        (2030, 0.5, "≈35%", -0.20, True, "center"),
        (2035, 0.5, "≥40%", 0.24, True, "center"),
    ]
    lane_color = {2.5: BLUE, 1.5: ORANGE, 0.5: AQUA}
    for yr, y, lab, dy, target, ha in ev:
        x = pos(yr)
        c = lane_color[y]
        ax.plot([x, x], [y, y + dy * 0.8], color=c, lw=0.7, zorder=2)
        ax.scatter([x], [y], s=24, marker="o", facecolor=SURF if target else c, edgecolor=c, linewidth=1.2, zorder=4)
        tx = x + {"center": 0, "left": -0.12, "right": 0.12}[ha]
        ax.text(tx, y + dy + (0.015 if dy > 0 else -0.015), lab, ha=ha, va="bottom" if dy > 0 else "top",
                fontsize=5.8, color=INK2, linespacing=1.15, zorder=5)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=INK2, markeredgecolor=INK2, markersize=5, label="已发生（论文/发布/文件）"),
               Line2D([0], [0], marker="o", color="w", markerfacecolor=SURF, markeredgecolor=INK2, markeredgewidth=1.2, markersize=5,
                      label="政策目标（非实绩）")]
    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.995, 1.0), ncol=2, frameon=False, fontsize=6.3,
               handletextpad=0.3, columnspacing=1.0)
    save(fig, "fig_timeline.png")


if __name__ == "__main__":
    if not REFMAP:
        print("警告：未找到 refmap.json，图中文献将显示为来源键。")
    fig_framework()
    fig_hardware()
    fig_compression()
    fig_pipeline()
    fig_stack()
    fig_architecture()
    fig_maturity()
    fig_latency()
    fig_precision()
    fig_hybrid()
    fig_hailo_quant()
    fig_timeline()
