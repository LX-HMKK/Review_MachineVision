# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库中工作提供指引。

## 项目概述

这是一个**机器视觉课程PDF翻译项目**。源文件是英文讲义幻灯片，导出为纯图片PDF（无可选文本）。流水线通过OCR提取文字，翻译为中文，生成"原始幻灯片图片+中文翻译"对照排版的PDF。对公式页会自动追加课程化的“学习补充”，用于补足参数含义、符号约定和公式直觉；补充内容集中维护在 `scripts/formula_supplements.py`。生成器还会对正文中的重点短语做自动分色，帮助快速定位核心概念、结论和注意项。

## 翻译流水线

有两种方式处理一个章节：

**方式一：手动翻译（`generate_cn_pdf_v2.py`）** — 翻译内容直接嵌入脚本，适合精细控制。
**方式二：通用流水线（`scripts/generate_pdf.py`）** — 翻译存为独立JSON文件，脚本读取后生成PDF。

通用流水线步骤：
1. **批量OCR** — 运行 `python scripts/batch_ocr.py`，Tesseract 提取英文文本，结果存入 `temp/ocr_results/`
2. **翻译** — 将每页OCR文本翻译为中文，保存为 `temp/translations/trans_{章节号}.json`，格式：`{"page_01": "<html字符串>", ...}`
   - 公式相关页的额外讲解不需要手写进每个 JSON，生成器会自动从 `scripts/formula_supplements.py` 读取并拼接到对应页翻译下方。
   - 翻译中可以直接使用 `<b>目标：</b>`、`<b>关键点：</b>` 这类标签；生成器会自动应用颜色强调。
3. **生成PDF** — 运行 `python scripts/generate_pdf.py {章节号}`，输出到 `中文版/`
   - 生成时会调用 `scripts/formula_renderer.py` 对常见数学符号做规范化渲染，例如把 `±` 统一成 `\pm`，避免出现乱码。
   - 章节 `02` 支持无翻译 JSON 的补充型生成；若缺少 `temp/translations/trans_02.json`，会只保留图片并插入学习补充。

输出文件命名规则：`{章节号}_{中文标题}_中文版.pdf`

## 运行环境

- **Python**：`C:\Python314\python.exe`（Python 3.13）
- **包管理**：直接 `pip install` 安装到用户 site-packages，不使用虚拟环境
- **Tesseract OCR**：`D:\Program Files\Tesseract-OCR\tesseract.exe`（v5.4.0），使用前需配置 `pytesseract.pytesseract.tesseract_cmd`
- **pandoc**：`C:\Users\lx_hm\AppData\Local\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.10\pandoc.exe`（Markdown → DOCX，LaTeX → OMML）
- **reportlab 中文字体**：通过 `pdfmetrics.registerFont(TTFont(...))` 注册：
  - SimHei（黑体）：`C:\Windows\Fonts\simhei.ttf`
  - YaHei（微软雅黑）：`C:\Windows\Fonts\msyh.ttc` subfontIndex=0
  - SimSun（宋体）：`C:\Windows\Fonts\simsun.ttc` subfontIndex=0
  - SimKai（楷体）：`C:\Windows\Fonts\simkai.ttf`

## PDF 排版规范

- **正文**：YaHei（微软雅黑）13pt，行距约20pt
- **章节标题**：SimHei（黑体）16–18pt，颜色 `#16213e`
- **来源标注**：YaHei 11pt，颜色 `#888888`
- **学习补充**：YaHei 12pt，颜色 `#666666`，用于解释公式、参数和课程里的默认约定
- **公式字号**：与正文统一为 13pt，避免公式偏小
- **重点配色**：红色强调重点/检测类结论，蓝色强调方法/模型，橙色强调注意与代价，绿色强调直觉与回忆
- **页面布局**：A4竖版，30pt页边距，幻灯片图片宽510pt（16:9比例），翻译文字置于深色分隔线下方
- **封面**：居中标题层级，包含章节号
- **页眉**：`第 N 页 / 共 M 页 | {英文章节标题}`，浅灰色

翻译中的HTML标签须使用 `<br/>`（XML自闭合），不能用 `<br>` 或 `<br />`，否则 reportlab 解析报错。

## DOCX 压缩流水线

有两个脚本处理 DOCX 极致压缩（用于开卷考试材料打印）：

### `scripts/compress_docx.py` — 对已有 DOCX 做 XML 级压缩

```bash
# 1. 解包
python scripts/office/unpack.py input.docx temp/unpacked/
# 2. 运行压缩
python scripts/compress_docx.py
# 3. 重新打包
python scripts/office/pack.py temp/unpacked/ output.docx --validate false
```

脚本通过正则直接修改 `styles.xml`、`document.xml`、`numbering.xml`：
- 全字体 6pt（sz=12），微软雅黑
- 双栏等宽 + 中栏竖线（`w:sep="1"`）
- 页边距 0.15"（216 twips），栏间距 108 twips
- 标题用颜色区分（暗红→深蓝→深青→深紫→深棕）
- 所有段落间距归零，编号缩进减半，表格单元格边距归零

### `scripts/md2docx.py` — Markdown 直接转压缩 DOCX

```bash
python scripts/md2docx.py
```

纯 python-docx 方案，处理标题、表格、列表、引用块、行内公式（作为着色斜体文本）。公式渲染为文本格式（非 OMML），适合无 pandoc 环境。如需 OMML 原生公式渲染，先用 pandoc 转换再用 `compress_docx.py` 压缩。

## 项目结构

```
课程ppt/
├── 原版/                 # 原始英文PDF（仅本地，.gitignore排除）
├── 中文版/               # 翻译输出（Git追踪）
├── 试卷/                  # 课程试卷（MD + 压缩 DOCX）
├── docs/                  # 复习资料（MD + 压缩 DOCX）
├── scripts/              # 流水线脚本
│   ├── batch_ocr.py           # 批量OCR
│   ├── generate_pdf.py        # 通用PDF生成器
│   ├── generate_cn_pdf_v2.py  # 手动翻译模板（已弃用）
│   ├── formula_renderer.py    # 公式与数学符号渲染
│   ├── formula_supplements.py # 公式学习补充文案
│   ├── compress_docx.py       # DOCX 极致压缩（双栏/6pt/颜色标题）
│   └── md2docx.py             # Markdown → 压缩 DOCX 直接转换
├── tests/                # 回归测试
├── temp/                 # 临时文件（OCR结果、翻译JSON、幻灯片截图）
├── CLAUDE.md
├── AGENTS.md
└── .remember/
```

## 源PDF特征

所有源PDF均为**纯图片**——`pdfplumber.extract_text()` 每页返回 `None`。每页包含1–2张嵌入图片（PPT幻灯片导出）。当前已纳入第 02 章和第 03 章起的 10 个文件：

| 文件 | 页数 |
|------|------|
| 02_成像与标定.pdf | 83 |
| 03_filter.pdf | 48 |
| 04_edge detection.pdf | 28 |
| 05_1_fitting.pdf | 40 |
| 05_2_Hough transform.pdf | 32 |
| 06_corners.pdf | 35 |
| 07_Blob.pdf | 38 |
| 08_texture.pdf | 61 |
| 09_segmentation.pdf | 51 |
| 10_recognition.pdf | 72 |
| 11_detection.pdf | 57 |

无原始PPTX文件，仅此图片嵌入式PDF。

## 当前生成状态

- `scripts/generate_pdf.py` 负责 `02`、`03`、`05_1`、`05_2`、`06`、`07`、`08`、`09`、`10`、`11`
- `scripts/generate_cn_pdf_v2.py` 当前仍用于 `04` 的手工版生成
- `tests/test_chapter02_support.py` 用于回归校验第 02 章支持、公式字号统一和重点着色逻辑

## Git 规范

**提交信息格式** — 使用 Angular 规范，中文描述：

```
<type>(<scope>): <中文描述>

<详细说明（可选）>
```

类型：`feat` | `fix` | `docs` | `style` | `refactor` | `perf` | `test` | `chore` | `ci` | `build`

示例：
- `chore(项目): 初始化机器视觉PDF翻译项目`
- `feat(翻译): 添加03_filter章节中文翻译`
- `fix(脚本): 修复OCR路径配置错误`

**规则：**
- 禁止 `Co-Authored-By` 署名
- PowerShell 中禁止用 `@'...'@` here-string 传递提交信息（会引入 `@` 字面字符），改用 `git commit -F <.tmpfile>` 文件方式提交
