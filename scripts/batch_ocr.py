"""Batch OCR all remaining chapters and save text for translation."""
import pytesseract, fitz, os, json
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

BASE = r'D:\StudyWorks\3.2\机器视觉\课程ppt'
SRC = os.path.join(BASE, '原版')
OUT = os.path.join(BASE, 'temp', 'ocr_results')
os.makedirs(OUT, exist_ok=True)

# Remaining chapters (skip 04 - already done)
chapters = [
    ('03_filter.pdf', '03'),
    ('05_1_fitting.pdf', '05_1'),
    ('05_2_Hough transform.pdf', '05_2'),
    ('06_corners.pdf', '06'),
    ('07_Blob.pdf', '07'),
    ('08_texture.pdf', '08'),
    ('09_segmentation.pdf', '09'),
    ('10_recognition.pdf', '10'),
    ('11_detection.pdf', '11'),
]

for filename, ch_id in chapters:
    path = os.path.join(SRC, filename)
    if not os.path.exists(path):
        print(f'SKIP {filename} - not found')
        continue

    print(f'\n{"="*60}')
    print(f'Processing: {filename}')
    print(f'{"="*60}')

    doc = fitz.open(path)
    results = {}
    total_chars = 0

    for i in range(len(doc)):
        page = doc[i]
        mat = fitz.Matrix(3, 3)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(BytesIO(pix.tobytes('png')))
        text = pytesseract.image_to_string(img, lang='eng', config='--psm 6').strip()
        chars = len(text)
        total_chars += chars
        results[f'page_{i+1:02d}'] = {'chars': chars, 'text': text}
        print(f'  Page {i+1:02d}/{len(doc):02d}: {chars} chars')

    doc.close()

    # Save
    json_path = os.path.join(OUT, f'ocr_{ch_id}.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Also save plain text for easy reading
    txt_path = os.path.join(OUT, f'ocr_{ch_id}.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        for k in sorted(results.keys()):
            t = results[k]['text']
            if t:
                f.write(f'--- {k} ---\n{t}\n\n')

    print(f'  => Saved {json_path} ({total_chars} total chars)')

print('\nAll OCR complete!')
