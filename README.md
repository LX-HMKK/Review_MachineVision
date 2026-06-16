# 机器视觉课程 PDF 翻译项目

> 将英文机器视觉讲义（图片型 PDF）通过 OCR → 翻译 → 排版，生成为「原图 + 中文翻译」对照的双语 PDF。

## ✨ 功能

- **批量 OCR** — Tesseract 自动提取英文 PDF 中每页幻灯片的文字
- **中英翻译** — 将 OCR 文本翻译为中文，保存为结构化 JSON
- **PDF 生成** — reportlab 生成 A4 竖版 PDF：幻灯片原图在上，中文翻译在下
- **11 个章节覆盖** — 滤波、边缘检测、拟合、Hough 变换、角点、Blob、纹理、分割、识别、检测

## 📋 环境要求

| 依赖 | 版本/路径 |
|------|----------|
| Python | 3.13（`C:\Python314\python.exe`） |
| Tesseract OCR | v5.4.0（`D:\Program Files\Tesseract-OCR\tesseract.exe`） |
| 中文字体 | SimHei、YaHei、SimSun、SimKai（Windows 系统字体） |

Python 包（`pip install` 安装到用户 site-packages）：

```
pytesseract, pdfplumber, reportlab, Pillow
```

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

### 方式二：手动翻译模板

```bash
python scripts/generate_cn_pdf_v2.py
```

翻译内容直接嵌入脚本，适合精细控制。

## 📁 项目结构

```
课程ppt/
├── 原版/                  # 原始英文 PDF（仅本地，.gitignore 排除）
├── 中文版/                # 翻译输出（Git 追踪）
├── 试卷/                  # 课程试卷及推测补全
├── scripts/               # 流水线脚本
│   ├── batch_ocr.py            # 批量 OCR
│   ├── generate_pdf.py         # 通用 PDF 生成器
│   ├── generate_cn_pdf_v2.py   # 手动翻译模板
│   └── formula_renderer.py     # 公式渲染工具
├── temp/                  # 临时文件（OCR 结果、翻译 JSON、幻灯片截图）
├── CLAUDE.md              # Claude Code 项目指引
└── README.md
```

## 📄 源 PDF

所有源 PDF 均为纯图片（无可选文本），每页含 1–2 张 PPT 幻灯片截图。

| 章节 | 文件 | 页数 |
|------|------|------|
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
- **标题**：黑体 16–18pt
- **页面**：A4 竖版，30pt 页边距，幻灯片宽 510pt
- **HTML 标签**：须使用 `<br/>`（XML 自闭合），不能用 `<br>` 或 `<br />`

## 📄 许可证

MIT
