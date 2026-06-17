"""Compress exam docx: tighter margins, indentation, column gap, tables."""
import re
from pathlib import Path

BASE = Path(r"D:\StudyWorks\3.2\机器视觉\课程ppt\temp\exam_auto\word")

# ── document.xml ──
doc = BASE / "document.xml"
text = doc.read_text(encoding="utf-8")

# Page margins: 288/432 → 144 (0.1" all around)
text = re.sub(r'w:top="\d+"', 'w:top="216"', text)
text = re.sub(r'w:bottom="\d+"', 'w:bottom="216"', text)
text = re.sub(r'w:left="\d+"', 'w:left="216"', text, count=1)  # first is pgMar
text = re.sub(r'w:right="\d+"', 'w:right="216"', text, count=1)

# Column gap
text = re.sub(r'w:space="\d+"', 'w:space="108"', text)

# Remove any leftover inline paragraph spacing (w:after / w:before on pPr)
text = re.sub(r'<w:spacing w:after="\d+" w:before="\d+"/>', '', text)
text = re.sub(r'w:spacing w:after="\d+" w:before="\d+"', 'w:spacing w:after="0" w:before="0"', text)

doc.write_text(text, encoding="utf-8")
print(f"[OK] document.xml: margins→144, col_gap→72, spacing cleaned")

# ── styles.xml ──
styles = BASE / "styles.xml"
text = styles.read_text(encoding="utf-8")

# BlockText/FootnoteBlockText indent: 480→120
text = text.replace('w:left="480" w:right="480"', 'w:left="120" w:right="120"')

# Table cell margins: 36→0
text = text.replace('w:left w:type="dxa" w:w="36"', 'w:left w:type="dxa" w:w="0"')
text = text.replace('w:right w:type="dxa" w:w="36"', 'w:right w:type="dxa" w:w="0"')

# Table cell top/bottom already 0, but ensure
text = text.replace('w:top w:type="dxa" w:w="0"', 'w:top w:type="dxa" w:w="0"')  # no-op

# Zero any remaining paragraph spacing in styles
text = re.sub(r'w:spacing w:after="[1-9]\d*"', 'w:spacing w:after="0"', text)
text = re.sub(r'w:spacing w:before="[1-9]\d*"', 'w:spacing w:before="0"', text)

styles.write_text(text, encoding="utf-8")
print(f"[OK] styles.xml: BlockText indent→120, table_margins→0, spacing→0")

# ── numbering.xml ──
num = BASE / "numbering.xml"
text = num.read_text(encoding="utf-8")

# Halve all left indents (720→360, 1440→720, ...)
text = re.sub(r'w:left="(\d+)"', lambda m: f'w:left="{int(m.group(1))//2}"', text)
# Halve hanging indents (360→180)
text = re.sub(r'w:hanging="(\d+)"', lambda m: f'w:hanging="{int(m.group(1))//2}"', text)

num.write_text(text, encoding="utf-8")
print(f"[OK] numbering.xml: all indents halved")

print("\nDone. Ready to pack.")
