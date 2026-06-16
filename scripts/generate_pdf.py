"""
Generalized Chinese PDF generator for any chapter.
Usage: python generate_pdf.py <chapter_id>
Reads OCR JSON from temp/ocr_results/ocr_<id>.json
Reads translations from temp/translations/trans_<id>.json
Outputs to 中文版/<filename>.pdf
"""
import fitz, os, json, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Config ──
BASE = r'D:\StudyWorks\3.2\机器视觉\课程ppt'
SRC_DIR = os.path.join(BASE, '原版')
OUT_DIR = os.path.join(BASE, '中文版')
TEMP_DIR = os.path.join(BASE, 'temp')
OCR_DIR = os.path.join(TEMP_DIR, 'ocr_results')
TRANS_DIR = os.path.join(TEMP_DIR, 'translations')
os.makedirs(TRANS_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Chapter metadata
CHAPTERS = {
    '03': {'src': '03_filter.pdf', 'out': '03_滤波_中文版.pdf', 'title': '图像滤波', 'en_title': 'Image Filtering'},
    '04': {'src': '04_edge detection.pdf', 'out': '04_边缘检测_中文版.pdf', 'title': '边缘检测', 'en_title': 'Edge Detection'},
    '05_1': {'src': '05_1_fitting.pdf', 'out': '05_1_拟合_中文版.pdf', 'title': '拟合', 'en_title': 'Fitting'},
    '05_2': {'src': '05_2_Hough transform.pdf', 'out': '05_2_霍夫变换_中文版.pdf', 'title': '霍夫变换', 'en_title': 'Hough Transform'},
    '06': {'src': '06_corners.pdf', 'out': '06_角点检测_中文版.pdf', 'title': '角点检测', 'en_title': 'Corner Detection'},
    '07': {'src': '07_Blob.pdf', 'out': '07_斑点检测_中文版.pdf', 'title': '斑点检测', 'en_title': 'Blob Detection'},
    '08': {'src': '08_texture.pdf', 'out': '08_纹理_中文版.pdf', 'title': '纹理分析', 'en_title': 'Texture Analysis'},
    '09': {'src': '09_segmentation.pdf', 'out': '09_分割_中文版.pdf', 'title': '图像分割', 'en_title': 'Image Segmentation'},
    '10': {'src': '10_recognition.pdf', 'out': '10_识别_中文版.pdf', 'title': '图像识别', 'en_title': 'Image Recognition'},
    '11': {'src': '11_detection.pdf', 'out': '11_目标检测_中文版.pdf', 'title': '目标检测', 'en_title': 'Object Detection'},
}

# Register Chinese fonts
pdfmetrics.registerFont(TTFont('SimHei', r'C:\Windows\Fonts\simhei.ttf'))
pdfmetrics.registerFont(TTFont('YaHei', r'C:\Windows\Fonts\msyh.ttc', subfontIndex=0))

def generate_pdf(ch_id):
    """Generate Chinese PDF for a chapter given its translations."""

    if ch_id not in CHAPTERS:
        print(f'Unknown chapter: {ch_id}')
        return

    meta = CHAPTERS[ch_id]
    trans_file = os.path.join(TRANS_DIR, f'trans_{ch_id}.json')

    if not os.path.exists(trans_file):
        print(f'Translations not found: {trans_file}')
        print('Run translation step first!')
        return

    with open(trans_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    orig_pdf = os.path.join(SRC_DIR, meta['src'])
    if not os.path.exists(orig_pdf):
        print(f'Source PDF not found: {orig_pdf}')
        return

    output = os.path.join(OUT_DIR, meta['out'])
    img_dir = os.path.join(TEMP_DIR, 'slides', ch_id)
    os.makedirs(img_dir, exist_ok=True)

    # ── Extract slides ──
    print(f'Extracting slides for chapter {ch_id}...')
    doc = fitz.open(orig_pdf)
    total = len(doc)
    mat = fitz.Matrix(2, 2)

    for i in range(total):
        pix = doc[i].get_pixmap(matrix=mat)
        pix.save(os.path.join(img_dir, f'slide_{i+1:02d}.png'))
    doc.close()

    # ── Build PDF ──
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=30, leftMargin=30,
                           topMargin=25, bottomMargin=25,
                           title=f'{meta["title"]} - 中文版')

    # Styles
    cover_title = ParagraphStyle('CT', fontName='SimHei', fontSize=26, leading=36,
        alignment=TA_CENTER, textColor=HexColor('#0f3460'))
    cover_sub = ParagraphStyle('CS', fontName='SimHei', fontSize=14, leading=22,
        alignment=TA_CENTER, textColor=HexColor('#555555'))
    body = ParagraphStyle('body', fontName='YaHei', fontSize=13, leading=20,
        textColor=HexColor('#333333'))
    footer = ParagraphStyle('ft', fontName='SimHei', fontSize=8, leading=12,
        textColor=HexColor('#bbbbbb'), alignment=TA_CENTER)

    story = []

    # Cover
    story.append(Spacer(1, 100))
    story.append(Paragraph('机器视觉技术', cover_title))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'{meta["title"]}', cover_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f'{meta["en_title"]} — 中文翻译版（含原图）', cover_sub))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f'共 {total} 页 | 翻译时间：2026年6月',
        ParagraphStyle('note', fontName='YaHei', fontSize=10, leading=16,
        alignment=TA_CENTER, textColor=HexColor('#888888'))))
    story.append(PageBreak())

    # Content
    img_w = 510
    img_h = img_w * 9 / 16

    for i in range(1, total + 1):
        key = f'page_{i:02d}'
        img_path = os.path.join(img_dir, f'slide_{i:02d}.png')

        if not os.path.exists(img_path):
            continue

        # Header
        story.append(Paragraph(f'第 {i} 页 / 共 {total} 页 | {meta["en_title"]}', footer))
        story.append(Spacer(1, 4))

        # Slide image
        story.append(Image(img_path, width=img_w, height=img_h))
        story.append(Spacer(1, 8))

        # Divider
        story.append(HRFlowable(width="95%", thickness=1, color=HexColor('#0f3460'),
            spaceBefore=2, spaceAfter=4))

        # Translation
        if key in translations:
            story.append(Paragraph(translations[key], body))

        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="60%", thickness=0.3, color=HexColor('#dddddd'),
            spaceBefore=2, spaceAfter=2))

        if i < total:
            story.append(PageBreak())

    doc.build(story)
    print(f'Generated: {output}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_pdf(sys.argv[1])
    else:
        print('Usage: python generate_pdf.py <chapter_id>')
        print('Available:', ', '.join(CHAPTERS.keys()))
