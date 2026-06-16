# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a **machine vision course PDF translation project**. Source PDFs are English lecture slides exported as image-only pages (no selectable text). The pipeline OCR-extracts text, translates to Chinese, and generates new PDFs with the original slide image plus Chinese translation below.

## Translation pipeline

The script `generate_cn_pdf_v2.py` is the reusable template for translating a single chapter. For each new chapter, copy and adapt it:

1. **Extract slides as images** — PyMuPDF (fitz) renders each page at 2x zoom → PNG
2. **OCR** — Tesseract extracts English text from each slide image
3. **Translate** — Claude translates the OCR text into Chinese with domain-aware terminology (machine vision technical terms)
4. **Generate PDF** — reportlab creates A4 portrait pages: original slide image on top, Chinese translation below

Key output filename pattern: `{chapter_number}_{chinese_title}_中文版.pdf`

## Environment

- **Python**: `C:\Python314\python.exe` (Python 3.13)
- **Packages**: installed in user site-packages (`pip install` without venv)
- **Tesseract OCR**: `D:\Program Files\Tesseract-OCR\tesseract.exe` (v5.4.0) — configure with `pytesseract.pytesseract.tesseract_cmd` before use
- **Chinese fonts for reportlab**: register via `pdfmetrics.registerFont(TTFont(...))` at:
  - SimHei (黑体): `C:\Windows\Fonts\simhei.ttf`
  - YaHei (微软雅黑): `C:\Windows\Fonts\msyh.ttc` subfontIndex=0
  - SimSun (宋体): `C:\Windows\Fonts\simsun.ttc` subfontIndex=0
  - SimKai (楷体): `C:\Windows\Fonts\simkai.ttf`

## PDF styling conventions

When generating Chinese PDFs, follow these conventions established in `generate_cn_pdf_v2.py`:

- **Body text**: YaHei (微软雅黑) 13pt, leading ~20pt
- **Section titles**: SimHei (黑体) 16–18pt, color `#16213e`
- **Source credits**: YaHei 11pt, color `#888888`
- **Layout**: A4 portrait, 30pt margins, slide image 510pt wide (16:9), translation below a dark divider line
- **Cover page**: centered title hierarchy with chapter number
- **Page headers**: `第 N 页 / 共 M 页 | {chapter_title_en}` in light gray

## Project structure

```
课程ppt/
├── 原版/                 # Original English PDFs (all 11 chapters)
├── 中文版/               # Translated Chinese PDF outputs
├── scripts/              # Translation pipeline scripts
│   └── generate_cn_pdf_v2.py   # Reusable chapter translator
├── temp/slides/          # Working directory for extracted slide images
├── CLAUDE.md
└── .remember/
```

When adding a new chapter translation, place the source PDF in `原版/`, run the script from project root, and the output lands in `中文版/`.

## Source PDF characteristics

All source PDFs are **image-only** — `pdfplumber.extract_text()` returns `None` on every page. Each page contains 1–2 embedded images (PPT slides exported as pictures). Total corpus from chapter 3 onward:

| File | Pages |
|------|-------|
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

No original PPTX files are available — only these image-embedded PDFs.
