import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import formula_renderer
import formula_supplements
import generate_pdf


class Chapter02SupportTests(unittest.TestCase):
    def test_formula_renderer_uses_body_sized_formula_defaults(self):
        self.assertEqual(formula_renderer.MATH_FONT_SIZE, 13)
        self.assertEqual(formula_renderer.DISPLAY_MATH_FONT_SIZE, 13)
        self.assertEqual(formula_renderer.MATRIX_CELL_FONT_SIZE, 13)
        self.assertEqual(formula_renderer.MATRIX_LABEL_FONT_SIZE, 13)

    def test_generate_pdf_registers_chapter_02(self):
        self.assertIn("02", generate_pdf.CHAPTERS)
        meta = generate_pdf.CHAPTERS["02"]
        self.assertEqual(meta["title"], "成像与标定")
        self.assertEqual(meta["out"], "02_成像与标定.pdf")

    def test_chapter_02_supplements_use_color_emphasis(self):
        supplement = formula_supplements.get_formula_supplement("02", "page_09")
        self.assertTrue(supplement)
        self.assertIn("学习补充", supplement)
        self.assertIn("#", supplement)

    def test_highlight_translation_text_colors_bold_labels_and_keywords(self):
        source = "<b>目标：</b>理解本章重点和边缘检测。"
        highlighted = formula_supplements.highlight_translation_text(source)
        self.assertIn("color=", highlighted)
        self.assertIn("目标：", highlighted)
        self.assertIn("本章重点", highlighted)
        self.assertIn("边缘检测", highlighted)

    def test_highlight_translation_text_colors_leading_plain_labels(self):
        source = "> 滑动窗口 = 数万个位置/尺度的评估<br/>@ 目标模型：生成式 vs 判别式"
        highlighted = formula_supplements.highlight_translation_text(source)
        self.assertIn("<b>滑动窗口 =</b>", highlighted)
        self.assertIn("<b>目标模型：</b>", highlighted)
        self.assertIn("color=", highlighted)


if __name__ == "__main__":
    unittest.main()
