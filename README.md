# 机器视觉课程 PDF 翻译项目

> 将英文机器视觉讲义（图片型 PDF）通过 OCR → 翻译 → 排版，生成为「原图 + 中文翻译」对照的双语 PDF，并自动补充公式讲解与重点分色。

## ✨ 功能

- **批量 OCR** — Tesseract 自动提取英文 PDF 中每页幻灯片的文字
- **中英翻译** — 将 OCR 文本翻译为中文，保存为结构化 JSON
- **PDF 生成** — reportlab 生成 A4 竖版 PDF：幻灯片原图在上，中文翻译在下
- **公式补充** — 对公式页自动追加课程化学习说明，补足参数含义、符号约定和直觉理解
- **重点分色** — 自动对正文中的目标、关键点、方法、注意项和课程重点做多色强调
- **数学符号规范化** — 生成时统一处理常见 Unicode 数学符号，避免公式渲染乱码
- **统一字号** — 正文与公式统一使用 13pt，避免公式偏小
- **11 个章节覆盖** — 成像与标定、滤波、边缘检测、拟合、Hough 变换、角点、Blob、纹理、分割、识别、检测
- **开卷考试 DOCX 导出** — Markdown 复习资料 → 双栏压缩 DOCX，LaTeX 公式 → OMML 原生渲染，6pt 全字号 + 颜色区分标题

## 📋 环境要求

| 依赖 | 版本 |
|------|------|
| Python | 3.13+ |
| Tesseract OCR | v5.4.0+ |
| 中文字体 | SimHei、YaHei、SimSun、SimKai（Windows 系统字体） |

Python 包（`pip install` 安装到用户 site-packages）：

```
pytesseract, pdfplumber, reportlab, Pillow, python-docx, markdown
```

可选依赖：
- **pandoc** — Markdown → DOCX 转换（LaTeX 公式渲染为 OMML）

## 🚀 快速开始

### 方式一：通用流水线（推荐）

```bash
# 1. 批量 OCR
python scripts/batch_ocr.py

# 2. 翻译（手动编辑 temp/translations/trans_{章节号}.json）
#    格式：{"page_01": "<html 字符串>", ...}

# 3. 生成 PDF
python scripts/generate_pdf.py {章节号}
```

输出文件：`中文版/{章节号}_{中文标题}_中文版.pdf`

如果某页需要补充公式解释或参数说明，统一修改 `scripts/formula_supplements.py` 即可，生成器会自动拼接到对应页的翻译下方。

如果翻译正文里使用了 `<b>目标：</b>`、`<b>关键点：</b>` 这类标签，或者出现“本章重点”“边缘检测”“目标模型”等高频课程关键词，生成器会自动应用颜色强调。

### 方式二：手动翻译模板

```bash
python scripts/generate_cn_pdf_v2.py
```

翻译内容直接嵌入脚本，适合精细控制。

当前 `04` 章仍使用这条手工流水线；其余章节统一走 `scripts/generate_pdf.py`。

### 方式三：导出压缩 DOCX（开卷考试用）

```bash
# Markdown → 压缩双栏 DOCX（LaTeX 公式自动渲染为 OMML）
pandoc --from markdown --to docx --mathml -o temp/raw.docx docs/复习资料.md
python scripts/compress_docx.py  # 对已有 DOCX 做极致压缩
```

压缩规格：全 6pt 微软雅黑 | 双栏等宽 + 中栏竖线 | 0.15" 页边距 | 颜色区分标题层级 | 零段落间距。

也提供直接转换脚本：
```bash
python scripts/md2docx.py  # 纯 python-docx 方案（无需 pandoc，公式为纯文本）
```

## 📁 项目结构

```
课程ppt/
├── 原版/                  # 原始英文 PDF（仅本地，.gitignore 排除）
├── 中文版/                # 翻译输出（Git 追踪）
├── 试卷/                  # 课程试卷及推测补全
├── scripts/               # 流水线脚本
│   ├── batch_ocr.py            # 批量 OCR
│   ├── generate_pdf.py         # 通用 PDF 生成器
│   ├── generate_cn_pdf_v2.py   # 手动翻译模板（当前用于 04 章）
│   ├── formula_renderer.py     # 公式渲染工具
│   ├── formula_supplements.py  # 课程公式补充文案与重点分色规则
│   ├── compress_docx.py        # DOCX 极致压缩（双栏/6pt/颜色标题）
│   ├── md2docx.py              # Markdown → 压缩 DOCX 直接转换
│   └── ...
├── docs/                  # 复习资料（MD + 压缩版 DOCX）
├── 试卷/                   # 课程试卷及推测补全（MD + 压缩版 DOCX）
├── tests/                   # 回归测试
├── temp/                  # 临时文件（OCR 结果、翻译 JSON、幻灯片截图）
├── CLAUDE.md              # Claude Code 项目指引
├── AGENTS.md              # Codex 项目指引
└── README.md
```

## 📄 源 PDF

所有源 PDF 均为纯图片（无可选文本），每页含 1–2 张 PPT 幻灯片截图。

| 章节 | 文件 | 页数 |
|------|------|------|
| 02 | 成像与标定 | 83 |
| 03 | 滤波 | 48 |
| 04 | 边缘检测 | 28 |
| 05_1 | 拟合 | 40 |
| 05_2 | Hough 变换 | 32 |
| 06 | 角点 | 35 |
| 07 | Blob 检测 | 38 |
| 08 | 纹理 | 61 |
| 09 | 图像分割 | 51 |
| 10 | 目标识别 | 72 |
| 11 | 目标检测 | 57 |

## 📐 排版规范

- **正文**：微软雅黑 13pt，行距 20pt
- **公式**：与正文统一为 13pt
- **标题**：黑体 16–18pt
- **页面**：A4 竖版，30pt 页边距，幻灯片宽 510pt
- **HTML 标签**：须使用 `<br/>`（XML 自闭合），不能用 `<br>` 或 `<br />`
- **学习补充**：YaHei 12pt、灰色，用于解释公式、参数和课程默认约定
- **重点配色**：红色强调重点/检测类结论，蓝色强调方法/模型，橙色强调注意与代价，绿色强调直觉与回忆

## 📄 许可证

MIT
