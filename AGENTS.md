# AGENTS.md

本文件为 Codex（Codex.ai/code）在此仓库中工作提供指引。

## 项目概述

这是一个**机器视觉课程PDF翻译项目**。源文件是英文讲义幻灯片，导出为纯图片PDF（无可选文本）。流水线通过OCR提取文字，翻译为中文，生成"原始幻灯片图片+中文翻译"对照排版的PDF。

## 翻译流水线

有两种方式处理一个章节：

**方式一：手动翻译（`generate_cn_pdf_v2.py`）** — 翻译内容直接嵌入脚本，适合精细控制。
**方式二：通用流水线（`scripts/generate_pdf.py`）** — 翻译存为独立JSON文件，脚本读取后生成PDF。

通用流水线步骤：
1. **批量OCR** — 运行 `python scripts/batch_ocr.py`，Tesseract 提取英文文本，结果存入 `temp/ocr_results/`
2. **翻译** — 将每页OCR文本翻译为中文，保存为 `temp/translations/trans_{章节号}.json`，格式：`{"page_01": "<html字符串>", ...}`
3. **生成PDF** — 运行 `python scripts/generate_pdf.py {章节号}`，输出到 `中文版/`

输出文件命名规则：`{章节号}_{中文标题}_中文版.pdf`

## 运行环境

- **Python**：`C:\Python314\python.exe`（Python 3.13）
- **包管理**：直接 `pip install` 安装到用户 site-packages，不使用虚拟环境
- **Tesseract OCR**：`D:\Program Files\Tesseract-OCR\tesseract.exe`（v5.4.0），使用前需配置 `pytesseract.pytesseract.tesseract_cmd`
- **reportlab 中文字体**：通过 `pdfmetrics.registerFont(TTFont(...))` 注册：
  - SimHei（黑体）：`C:\Windows\Fonts\simhei.ttf`
  - YaHei（微软雅黑）：`C:\Windows\Fonts\msyh.ttc` subfontIndex=0
  - SimSun（宋体）：`C:\Windows\Fonts\simsun.ttc` subfontIndex=0
  - SimKai（楷体）：`C:\Windows\Fonts\simkai.ttf`

## PDF 排版规范

- **正文**：YaHei（微软雅黑）13pt，行距约20pt
- **章节标题**：SimHei（黑体）16–18pt，颜色 `#16213e`
- **来源标注**：YaHei 11pt，颜色 `#888888`
- **页面布局**：A4竖版，30pt页边距，幻灯片图片宽510pt（16:9比例），翻译文字置于深色分隔线下方
- **封面**：居中标题层级，包含章节号
- **页眉**：`第 N 页 / 共 M 页 | {英文章节标题}`，浅灰色

翻译中的HTML标签须使用 `<br/>`（XML自闭合），不能用 `<br>` 或 `<br />`，否则 reportlab 解析报错。

## 项目结构

```
课程ppt/
├── 原版/                 # 原始英文PDF（仅本地，.gitignore排除）
├── 中文版/               # 翻译输出（Git追踪）
├── scripts/              # 流水线脚本
│   ├── batch_ocr.py           # 批量OCR
│   ├── generate_pdf.py        # 通用PDF生成器
│   └── generate_cn_pdf_v2.py  # 手动翻译模板（已弃用）
├── temp/                 # 临时文件（OCR结果、翻译JSON、幻灯片截图）
├── AGENTS.md
└── .remember/
```

## 源PDF特征

所有源PDF均为**纯图片**——`pdfplumber.extract_text()` 每页返回 `None`。每页包含1–2张嵌入图片（PPT幻灯片导出）。第3章起共10个文件：

| 文件 | 页数 |
|------|------|
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
