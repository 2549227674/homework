// 由 content.md + tables.js + references.js 生成综述 Word 文档。
// 用法：
//   node build_docx.js --refmap-only   # 只计算参考文献编号，写出 refmap.json（供 make_figures.py 使用）
//   node build_docx.js                 # 生成 ../嵌入式端边智能赋能智慧农业综述.docx
// 依赖：npm 包 docx（v9）。
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  BorderStyle, AlignmentType, HeadingLevel, TableOfContents, Header, Footer, PageNumber,
  NumberFormat, VerticalAlign, ShadingType, LineRuleType,
} = require("docx");

const REFS = require("./references.js");
const TABLES = require("./tables.js");
const HERE = __dirname;
const FIG_DIR = path.join(HERE, "..", "figures");
const OUT_DOCX = path.join(HERE, "..", "嵌入式端边智能赋能智慧农业综述.docx");

const SONG = "宋体", HEI = "黑体", TNR = "Times New Roman";
const font = (east, latin = TNR) => ({ ascii: latin, hAnsi: latin, eastAsia: east, cs: latin });
const TEXT_W = 9070; // 版心宽度（twip）：A4 宽 11906 − 左右边距各 1418

// ------------------------------------------------------------------ 解析 content.md
const raw = fs.readFileSync(path.join(HERE, "content.md"), "utf8");
const sec = {};
let cur = null;
for (const line of raw.split(/\r?\n/)) {
  const m = line.match(/^%%\s*(\w+)/);
  if (m) { cur = m[1]; sec[cur] = []; continue; }
  if (cur) sec[cur].push(line);
}
const meta = (k) => sec[k].join("\n").trim();

const blocks = [];
for (const line of sec.body) {
  const t = line.trim();
  if (!t) continue;
  let m;
  if ((m = t.match(/^(#{1,3})\s+(.*)$/))) blocks.push({ type: "h", level: m[1].length, text: m[2] });
  else if (t.startsWith("FIG|")) {
    const [, key, file, caption, note, width] = t.split("|");
    blocks.push({ type: "fig", key, file, caption, note, width: parseFloat(width) || 16 });
  } else if (t.startsWith("TABLE|")) blocks.push({ type: "table", key: t.split("|")[1] });
  else blocks.push({ type: "p", text: t });
}

// ------------------------------------------------------------------ 图表编号与参考文献编号
const figNum = {}, tabNum = {};
for (const b of blocks) {
  if (b.type === "fig") figNum[b.key] = Object.keys(figNum).length + 1;
  if (b.type === "table") {
    if (!TABLES[b.key]) throw new Error("未定义的表格：" + b.key);
    tabNum[b.key] = Object.keys(tabNum).length + 1;
  }
}
const refNum = {}, refOrder = [];
const CITE_RE = /\[([@#])([^\]]+)\]/g;
const keysOf = (inner) => inner.split(";").map((s) => s.replace(/^[@#]/, "").trim()).filter(Boolean);
function scan(text) {
  for (const m of String(text).matchAll(CITE_RE)) {
    for (const k of keysOf(m[2])) {
      if (!REFS[k]) throw new Error("未知参考文献键：" + k);
      if (!refNum[k]) { refOrder.push(k); refNum[k] = refOrder.length; }
    }
  }
}
for (const b of blocks) {
  if (b.type === "p" || b.type === "h") scan(b.text);
  else if (b.type === "fig") { scan(b.caption); scan(b.note); }
  else if (b.type === "table") {
    const t = TABLES[b.key];
    scan(t.caption); t.header.forEach(scan); t.rows.forEach((r) => r.forEach(scan)); scan(t.note || "");
  }
}
const unused = Object.keys(REFS).filter((k) => !refNum[k]);
if (unused.length) console.log(`另有 ${unused.length} 条资料未列入 Word 参考文献，完整条目写入 完整来源清单.md`);

// 检查图片脚本中出现的文献键均已在正文中编号
const figScript = fs.readFileSync(path.join(HERE, "make_figures.py"), "utf8");
const figKeys = [...new Set([...figScript.matchAll(/\[([A-Z]\d{2})\]/g)].map((m) => m[1]))];
const missing = figKeys.filter((k) => !refNum[k]);
if (missing.length) throw new Error("图片中引用了正文未引用的文献：" + missing.join(", "));

fs.writeFileSync(path.join(HERE, "refmap.json"), JSON.stringify(refNum, null, 1));

// 完整来源清单：Word 参考文献只列核心学术文献，其余资料在正文中以机构、文件名、产品名或标准号指明；
// 这里保留全部来源条目，便于核对正文数据的出处。
{
  const groups = [["R", "统计与报告"], ["S", "政策与标准"], ["H", "芯片与硬件官方资料"],
    ["O", "官方技术文档与企业发布"], ["P", "学术论文（通用方法与背景，正文未单独编号）"]];
  const lines = ["# 完整来源清单", "",
    `Word 版参考文献只列 ${refOrder.length} 篇核心学术文献（正文中按作者、模型或研究对象具体讨论的论文）。` +
    "其余资料在正文中已以机构、文件名、产品名或标准号直接指明，下面列出完整条目，便于核对数据出处。", "",
    `## 一、已列入 Word 参考文献（${refOrder.length} 条，按正文编号）`, ""];
  refOrder.forEach((k, i) => lines.push(`[${i + 1}] ${REFS[k]}`, ""));
  lines.push(`## 二、未列入参考文献、在正文中以名称指明的资料（${unused.length} 条）`, "");
  for (const [prefix, title] of groups) {
    const ks = unused.filter((k) => k.startsWith(prefix));
    if (!ks.length) continue;
    lines.push(`### ${title}`, "");
    ks.forEach((k) => lines.push(`- ${REFS[k]}`));
    lines.push("");
  }
  fs.writeFileSync(path.join(HERE, "..", "完整来源清单.md"), lines.join("\n"));
}
fs.writeFileSync(path.join(HERE, "figmap.json"), JSON.stringify(
  { figures: blocks.filter((b) => b.type === "fig").map((b) => ({ n: figNum[b.key], key: b.key, file: b.file, caption: b.caption })),
    tables: Object.keys(tabNum).map((k) => ({ n: tabNum[k], key: k, caption: TABLES[k].caption })) }, null, 1));
console.log(`参考文献 ${refOrder.length} 条，图 ${Object.keys(figNum).length} 幅，表 ${Object.keys(tabNum).length} 个`);
if (process.argv.includes("--refmap-only")) process.exit(0);

// ------------------------------------------------------------------ 行内排版
function compress(nums) {
  const s = [...new Set(nums)].sort((a, b) => a - b);
  const out = [];
  for (let i = 0; i < s.length;) {
    let j = i;
    while (j + 1 < s.length && s[j + 1] === s[j] + 1) j++;
    if (j - i >= 2) out.push(`${s[i]}–${s[j]}`);
    else for (let k = i; k <= j; k++) out.push(String(s[k]));
    i = j + 1;
  }
  return out.join(",");
}
function run(text, o = {}) {
  const opt = { text };
  if (o.font) opt.font = o.font;
  if (o.size) opt.size = o.size;
  if (o.bold) opt.bold = true;
  if (o.italics) opt.italics = true;
  if (o.color) opt.color = o.color;
  if (o.superScript) opt.superScript = true;
  return new TextRun(opt);
}
const TOKEN_RE = /(\[[@#][^\]]+\]|\{(?:fig|tab):[a-z_]+\}|\*\*[^*]+\*\*)/g;
function inline(text, o = {}) {
  const out = [];
  let last = 0;
  for (const m of text.matchAll(TOKEN_RE)) {
    if (m.index > last) out.push(run(text.slice(last, m.index), o));
    const tok = m[0];
    if (tok.startsWith("[")) {
      const sup = tok[1] === "@" && o.citeSuper !== false;
      const nums = keysOf(tok.slice(2, -1)).map((k) => refNum[k]);
      out.push(run(`[${compress(nums)}]`, { ...o, superScript: sup }));
    } else if (tok.startsWith("{")) {
      const [kind, key] = tok.slice(1, -1).split(":");
      const n = kind === "fig" ? figNum[key] : tabNum[key];
      if (!n) throw new Error("未定义的交叉引用：" + tok);
      out.push(run((kind === "fig" ? "图" : "表") + n, o));
    } else out.push(run(tok.slice(2, -2), { ...o, bold: true }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(run(text.slice(last), o));
  return out;
}

// ------------------------------------------------------------------ 段落构件
const para = (children, o = {}) => new Paragraph({ children, ...o });
const bodyPara = (text) => para(inline(text), {
  alignment: AlignmentType.JUSTIFIED, indent: { firstLine: 480 }, spacing: { line: 400, lineRule: LineRuleType.EXACT, before: 0, after: 0 },
});
const spacer = (twip) => para([run("")], { spacing: { before: 0, after: twip, line: 240, lineRule: LineRuleType.AUTO } });

function imageSize(buf) {
  if (buf[0] === 0x89 && buf[1] === 0x50) return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  let i = 2;
  while (i < buf.length) {
    if (buf[i] !== 0xff) { i++; continue; }
    const mk = buf[i + 1];
    const len = buf.readUInt16BE(i + 2);
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(mk))
      return { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) };
    i += 2 + len;
  }
  throw new Error("无法识别的图片格式");
}

function figure(b) {
  const file = path.join(FIG_DIR, b.file);
  const buf = fs.readFileSync(file);
  const { w, h } = imageSize(buf);
  const wpx = (b.width / 2.54) * 96;
  const n = figNum[b.key];
  const capFont = { font: font(HEI), size: 21, citeSuper: false };
  const out = [
    para([new ImageRun({
      type: file.endsWith(".png") ? "png" : "jpg", data: buf,
      transformation: { width: Math.round(wpx), height: Math.round((wpx * h) / w) },
      altText: { title: `图${n}`, description: b.caption.replace(/\[[@#][^\]]+\]/g, ""), name: b.key },
    })], { alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 160, after: 60, line: 240, lineRule: LineRuleType.AUTO } }),
    para([run(`图${n}  `, capFont), ...inline(b.caption, capFont)], {
      alignment: AlignmentType.CENTER, keepNext: Boolean(b.note), keepLines: true,
      spacing: { before: 40, after: b.note ? 20 : 200, line: 300, lineRule: LineRuleType.EXACT }, indent: { left: 420, right: 420 },
    }),
  ];
  if (b.note) out.push(para(inline(b.note, { size: 18, color: "595959", citeSuper: false }), {
    alignment: AlignmentType.CENTER, keepLines: true, spacing: { before: 0, after: 220, line: 270, lineRule: LineRuleType.EXACT }, indent: { left: 420, right: 420 },
  }));
  return out;
}

function table(key) {
  const t = TABLES[key];
  const n = tabNum[key];
  const capFont = { font: font(HEI), size: 21, citeSuper: false };
  const thick = { style: BorderStyle.SINGLE, size: 12, color: "000000" };
  const mid = { style: BorderStyle.SINGLE, size: 6, color: "000000" };
  const hair = { style: BorderStyle.SINGLE, size: 2, color: "BFBFBF" };
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const sum = t.widths.reduce((a, b) => a + b, 0);
  if (sum !== TEXT_W) throw new Error(`表 ${key} 列宽之和 ${sum} ≠ ${TEXT_W}`);
  const nr = t.rows.length;
  const cell = (text, ci, header, ri) => new TableCell({
    width: { size: t.widths[ci], type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 45, bottom: 45, left: 70, right: 70 },
    borders: {
      top: header ? thick : ri === 0 ? mid : hair,
      bottom: header ? mid : ri === nr - 1 ? thick : hair,
      left: none, right: none,
    },
    shading: header ? { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" } : undefined,
    children: [para(inline(text, { size: 18, font: header ? font(HEI) : undefined, citeSuper: false }), {
      alignment: header || t.center.includes(ci) ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { line: 250, lineRule: LineRuleType.EXACT, before: 0, after: 0 },
    })],
  });
  const rows = [
    new TableRow({ tableHeader: true, cantSplit: true, children: t.header.map((x, ci) => cell(x, ci, true, -1)) }),
    ...t.rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((x, ci) => cell(x, ci, false, ri)) })),
  ];
  const out = [
    para([run(`表${n}  `, capFont), ...inline(t.caption, capFont)], {
      alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 200, after: 80, line: 300, lineRule: LineRuleType.EXACT },
    }),
    new Table({
      width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: t.widths,
      borders: { top: thick, bottom: thick, left: none, right: none, insideHorizontal: none, insideVertical: none },
      rows,
    }),
  ];
  if (t.note) out.push(para(inline("注：" + t.note, { size: 18, color: "595959", citeSuper: false }), {
    alignment: AlignmentType.JUSTIFIED, spacing: { before: 60, after: 220, line: 270, lineRule: LineRuleType.EXACT },
  }));
  return out;
}

// ------------------------------------------------------------------ 封面、摘要、目录
const [titleMain, titleSub] = meta("title_cn").split("：");
const center = AlignmentType.CENTER;
function infoRun(label) {
  return para([
    new TextRun({ text: label, font: font(HEI), size: 28 }),
    new TextRun({ text: "_".repeat(26), font: font(SONG), size: 28 }),
  ], { alignment: center, spacing: { before: 0, after: 260, line: 360, lineRule: LineRuleType.AUTO } });
}

const cover = [
  spacer(1300),
  para([run("《嵌入式软件》课程综述报告", { font: font(HEI), size: 30 })], { alignment: center, spacing: { after: 700 } }),
  para([run(titleMain, { font: font(HEI), size: 44, bold: true })], { alignment: center, spacing: { after: 240, line: 400, lineRule: LineRuleType.AUTO } }),
  para([run("——" + titleSub, { font: font(HEI), size: 32 })], { alignment: center, spacing: { after: 360, line: 400, lineRule: LineRuleType.AUTO } }),
  para([run(meta("title_en"), { font: font(SONG, TNR), size: 24, italics: true })], { alignment: center, indent: { left: 600, right: 600 }, spacing: { after: 1500, line: 320, lineRule: LineRuleType.AUTO } }),
  infoRun("姓　　名："), infoRun("学　　号："), infoRun("专业班级："), infoRun("指导教师："),
  spacer(900),
  para([run("2026年9月", { font: font(SONG), size: 28 })], { alignment: center, pageBreakBefore: false }),
];

const abstractPart = [
  para([run("摘　要", { font: font(HEI), size: 32 })], { alignment: center, pageBreakBefore: true, spacing: { after: 300, line: 360, lineRule: LineRuleType.AUTO } }),
  para(inline(meta("abstract_cn")), { alignment: AlignmentType.JUSTIFIED, indent: { firstLine: 480 }, spacing: { line: 400, lineRule: LineRuleType.EXACT } }),
  para([run("关键词：", { font: font(HEI), size: 24 }), run(meta("keywords_cn"))], { spacing: { before: 200, after: 600, line: 360, lineRule: LineRuleType.AUTO } }),
  para([run("Abstract", { font: font(HEI, TNR), size: 32, bold: true })], { alignment: center, pageBreakBefore: true, spacing: { after: 300, line: 360, lineRule: LineRuleType.AUTO } }),
  para([run(meta("abstract_en"), { font: font(SONG, TNR) })], { alignment: AlignmentType.JUSTIFIED, indent: { firstLine: 480 }, spacing: { line: 400, lineRule: LineRuleType.EXACT } }),
  para([run("Keywords: ", { font: font(SONG, TNR), bold: true }), run(meta("keywords_en"), { font: font(SONG, TNR) })], { spacing: { before: 200, line: 360, lineRule: LineRuleType.AUTO } }),
];

const tocPart = [
  para([run("目　录", { font: font(HEI), size: 32 })], { alignment: center, pageBreakBefore: true, spacing: { after: 300, line: 360, lineRule: LineRuleType.AUTO } }),
  new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-2" }),
];

// ------------------------------------------------------------------ 正文与参考文献
const HEAD = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };
const body = [];
for (const b of blocks) {
  if (b.type === "h") body.push(para(inline(b.text, { citeSuper: true }), { heading: HEAD[b.level] }));
  else if (b.type === "p") body.push(bodyPara(b.text));
  else if (b.type === "fig") body.push(...figure(b));
  else if (b.type === "table") body.push(...table(b.key));
}
body.push(para([run("参考文献")], { heading: HeadingLevel.HEADING_1, pageBreakBefore: false }));
refOrder.forEach((k, i) => {
  body.push(para([run(`[${i + 1}] `, { size: 20 }), run(REFS[k], { size: 20 })], {
    alignment: AlignmentType.LEFT, indent: { left: 460, hanging: 460 }, spacing: { before: 0, after: 40, line: 300, lineRule: LineRuleType.EXACT },
  }));
});

// ------------------------------------------------------------------ 文档
const headingStyle = (id, name, size, before, after, level) => ({
  id, name, basedOn: "Normal", next: "Normal", quickFormat: true,
  run: { font: font(HEI), size, bold: false, color: "000000" },
  paragraph: { spacing: { before, after, line: 360, lineRule: LineRuleType.AUTO }, keepNext: true, keepLines: true, outlineLevel: level },
});
const tocStyle = (id, name, indentLeft, size) => ({
  id, name, basedOn: "Normal", next: "Normal",
  run: { font: font(SONG), size },
  paragraph: { indent: { left: indentLeft }, spacing: { before: 0, after: 0, line: 330, lineRule: LineRuleType.EXACT } },
});
const pageBase = { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1418, right: 1418, header: 851, footer: 851 } };

const doc = new Document({
  creator: "嵌入式软件课程综述",
  title: meta("title_cn"),
  description: "嵌入式端边智能与智慧农业综述",
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: font(SONG), size: 24 }, paragraph: { spacing: { line: 360, lineRule: LineRuleType.AUTO } } } },
    paragraphStyles: [
      headingStyle("Heading1", "Heading 1", 32, 480, 240, 0),
      headingStyle("Heading2", "Heading 2", 28, 300, 150, 1),
      headingStyle("Heading3", "Heading 3", 24, 200, 100, 2),
      tocStyle("TOC1", "toc 1", 0, 24),
      tocStyle("TOC2", "toc 2", 420, 22),
      tocStyle("TOC3", "toc 3", 840, 22),
    ],
  },
  sections: [
    { properties: { page: pageBase }, children: [...cover, ...abstractPart, ...tocPart] },
    {
      properties: { page: { ...pageBase, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } },
      headers: {
        default: new Header({ children: [para([run("《嵌入式软件》课程综述　|　嵌入式端边智能赋能智慧农业", { size: 18, color: "595959" })], {
          alignment: AlignmentType.RIGHT, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "A6A6A6", space: 4 } },
        })] }),
      },
      footers: {
        default: new Footer({ children: [para([new TextRun({ children: ["— ", PageNumber.CURRENT, " —"], size: 18 })], { alignment: center })] }),
      },
      children: body,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT_DOCX, buf);
  console.log("已生成", OUT_DOCX, (buf.length / 1024 / 1024).toFixed(2), "MB");
});
