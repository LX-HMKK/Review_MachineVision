import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from formula_renderer import normalize_formula_expr


class FormulaRendererTests(unittest.TestCase):
    def test_normalize_formula_expr_maps_plus_minus(self):
        self.assertEqual(normalize_formula_expr("45.3±0.5"), r"45.3\pm0.5")


if __name__ == "__main__":
    unittest.main()
