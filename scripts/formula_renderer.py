import hashlib
import html
import os
import re
import unicodedata
from pathlib import Path

from matplotlib import mathtext
from matplotlib.font_manager import FontProperties
from PIL import Image, ImageDraw

MATH_DPI = 220
MATH_COLOR = "#222222"
MATH_FONT_SIZE = 18
DISPLAY_MATH_FONT_SIZE = 22
MATRIX_CELL_FONT_SIZE = 22
MATRIX_LABEL_FONT_SIZE = 24

TAG_SPLIT_RE = re.compile(r"(<[^>]+>)")
CJK_RE = re.compile(r"([\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]+)")
SCRIPT_RE = re.compile(r"[\u2070-\u209F\u1D2C-\u1D7Fⱼᵢᵗₜ₁₂₃₄₅₆₇₈₉₀₌₊₋₍₎]")

UNICODE_MATH_REPLACEMENTS = {
    "±": r"\pm",
    "∓": r"\mp",
}


def _init_mathtext():
    import matplotlib

    matplotlib.use("Agg", force=True)
    matplotlib.rcParams["mathtext.fontset"] = "cm"
    matplotlib.rcParams["mathtext.default"] = "it"


_init_mathtext()


def _render_png(expr, path, font_size=MATH_FONT_SIZE, dpi=MATH_DPI, color=MATH_COLOR):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    formula = expr.strip()
    if not formula.startswith("$"):
        formula = f"${formula}$"

    prop = FontProperties(size=font_size)
    mathtext.math_to_image(formula, str(path), prop=prop, dpi=dpi, format="png", color=color)

    with Image.open(path) as img:
        if img.mode in ("RGBA", "LA"):
            alpha = img.getchannel("A")
            bbox = alpha.getbbox()
        else:
            bbox = img.convert("L").point(lambda p: 255 if p < 250 else 0).getbbox()
        if bbox:
            crop_pad = 2
            left = max(bbox[0] - crop_pad, 0)
            top = max(bbox[1] - crop_pad, 0)
            right = min(bbox[2] + crop_pad, img.width)
            bottom = min(bbox[3] + crop_pad, img.height)
            cropped = img.crop((left, top, right, bottom))
            cropped.save(path)

    with Image.open(path) as img:
        return {
            "path": str(path),
            "width_px": img.width,
            "height_px": img.height,
            "width_pt": img.width * 72.0 / dpi,
            "height_pt": img.height * 72.0 / dpi,
        }


def _cache_key(*parts):
    digest = hashlib.md5("||".join(map(str, parts)).encode("utf-8")).hexdigest()
    return digest


def _script_kind(ch):
    name = unicodedata.name(ch, "")
    if "SUBSCRIPT" in name:
        return "_"
    if "SUPERSCRIPT" in name:
        return "^"

    code = ord(ch)
    if 0x2080 <= code <= 0x209F:
        return "_"
    if 0x2070 <= code <= 0x207F:
        return "^"
    if code == 0x2C7C:
        return "_"
    if 0x1D2C <= code <= 0x1D7F:
        return "^"
    return None


def _script_base(ch):
    decomp = unicodedata.normalize("NFKD", ch)
    base = "".join(c for c in decomp if not unicodedata.combining(c))
    if base:
        return base
    fallback = {
        "₊": "+",
        "₋": "-",
        "₌": "=",
        "₍": "(",
        "₎": ")",
        "⁺": "+",
        "⁻": "-",
        "⁼": "=",
        "⁽": "(",
        "⁾": ")",
    }
    return fallback.get(ch, "")


def normalize_formula_expr(expr):
    expr = expr.replace("\xa0", " ")
    expr = expr.replace("ȳ", r"\bar{y}")
    for src, dst in UNICODE_MATH_REPLACEMENTS.items():
        expr = expr.replace(src, dst)
    expr = re.sub(r"([A-Za-zα-ωΑ-Ω])\u0304", r"\\bar{\1}", expr)
    out = []
    i = 0
    while i < len(expr):
        kind = _script_kind(expr[i])
        if kind is None:
            out.append(expr[i])
            i += 1
            continue

        j = i
        run = []
        while j < len(expr) and _script_kind(expr[j]) == kind:
            base = _script_base(expr[j])
            if base:
                run.append(base)
            j += 1

        if run:
            payload = "".join(run)
            if len(payload) == 1:
                out.append(f"{kind}{payload}")
            else:
                out.append(f"{kind}{{{payload}}}")
        i = j

    normalized = "".join(out)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def render_math_asset(expr, cache_dir, font_size=MATH_FONT_SIZE, dpi=MATH_DPI, color=MATH_COLOR):
    cache_dir = Path(cache_dir) / "formula_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    expr = normalize_formula_expr(expr)
    key = _cache_key(expr, font_size, dpi, color)
    path = cache_dir / f"{key}.png"
    if not path.exists():
        _render_png(expr, path, font_size=font_size, dpi=dpi, color=color)

    with Image.open(path) as img:
        return {
            "path": str(path),
            "width_px": img.width,
            "height_px": img.height,
            "width_pt": img.width * 72.0 / dpi,
            "height_pt": img.height * 72.0 / dpi,
        }


def render_matrix_asset(label, rows, cache_dir, cell_font_size=MATRIX_CELL_FONT_SIZE,
                        label_font_size=MATRIX_LABEL_FONT_SIZE, dpi=MATH_DPI, color=MATH_COLOR):
    cache_dir = Path(cache_dir) / "formula_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    normalized_rows = [list(map(str, row)) for row in rows]
    key = _cache_key(label, normalized_rows, cell_font_size, label_font_size, dpi, color)
    path = cache_dir / f"matrix_{key}.png"
    if path.exists():
        with Image.open(path) as img:
            return {
                "path": str(path),
                "width_px": img.width,
                "height_px": img.height,
                "width_pt": img.width * 72.0 / dpi,
                "height_pt": img.height * 72.0 / dpi,
            }

    label_asset = render_math_asset(f"{label} =", cache_dir, font_size=label_font_size, dpi=dpi, color=color)
    cell_assets = [
        [render_math_asset(cell, cache_dir, font_size=cell_font_size, dpi=dpi, color=color) for cell in row]
        for row in normalized_rows
    ]

    nrows = len(cell_assets)
    ncols = max((len(row) for row in cell_assets), default=0)
    if nrows == 0 or ncols == 0:
        blank = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        blank.save(path)
        return {
            "path": str(path),
            "width_px": 1,
            "height_px": 1,
            "width_pt": 1 * 72.0 / dpi,
            "height_pt": 1 * 72.0 / dpi,
        }

    cell_gap_x = 14
    cell_gap_y = 10
    cell_w = max(asset["width_px"] for row in cell_assets for asset in row) + 8
    cell_h = max(asset["height_px"] for row in cell_assets for asset in row) + 6
    matrix_w = ncols * cell_w + (ncols - 1) * cell_gap_x
    matrix_h = nrows * cell_h + (nrows - 1) * cell_gap_y

    bracket_hook = max(8, cell_h // 4)
    bracket_thickness = 2
    label_gap = 10
    content_h = max(label_asset["height_px"], matrix_h)
    width = label_asset["width_px"] + label_gap + bracket_hook + 8 + matrix_w + 8 + bracket_hook
    height = content_h + 8

    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    def paste_asset(asset, x, y):
        with Image.open(asset["path"]) as src:
            canvas.alpha_composite(src.convert("RGBA"), (int(x), int(y)))

    label_y = (height - label_asset["height_px"]) // 2
    paste_asset(label_asset, 0, label_y)

    matrix_x = label_asset["width_px"] + label_gap + bracket_hook + 8
    matrix_y = (height - matrix_h) // 2
    left_x = label_asset["width_px"] + label_gap
    right_x = matrix_x + matrix_w + 8

    draw = ImageDraw.Draw(canvas)
    top = matrix_y
    bottom = matrix_y + matrix_h
    draw.line((left_x + bracket_hook, top, left_x, top), fill=color, width=bracket_thickness)
    draw.line((left_x, top, left_x, bottom), fill=color, width=bracket_thickness)
    draw.line((left_x + bracket_hook, bottom, left_x, bottom), fill=color, width=bracket_thickness)
    draw.line((right_x - bracket_hook, top, right_x, top), fill=color, width=bracket_thickness)
    draw.line((right_x, top, right_x, bottom), fill=color, width=bracket_thickness)
    draw.line((right_x - bracket_hook, bottom, right_x, bottom), fill=color, width=bracket_thickness)

    for r, row in enumerate(cell_assets):
        for c, asset in enumerate(row):
            x = matrix_x + c * (cell_w + cell_gap_x) + (cell_w - asset["width_px"]) / 2
            y = matrix_y + r * (cell_h + cell_gap_y) + (cell_h - asset["height_px"]) / 2
            paste_asset(asset, x, y)

    canvas.save(path)
    return {
        "path": str(path),
        "width_px": canvas.width,
        "height_px": canvas.height,
        "width_pt": canvas.width * 72.0 / dpi,
        "height_pt": canvas.height * 72.0 / dpi,
    }


def looks_like_formula(text):
    if not text:
        return False
    if re.search(r"[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]", text):
        return False

    stripped = text.strip()
    if not stripped:
        return False
    if "'" in stripped or '"' in stripped:
        return False
    if SCRIPT_RE.search(stripped):
        return True

    strong = sum(ch in stripped for ch in "=∇∂√×≈±^_/\\[]{}·−–≤≥≠→←")
    has_letter = bool(re.search(r"[A-Za-zα-ωΑ-Ω]", stripped))
    has_digit = bool(re.search(r"\d", stripped))
    if strong >= 1 and (has_letter or has_digit):
        return True
    if re.fullmatch(r"[A-Za-zα-ωΑ-Ω]{1,3}\s*\([^()]+\)", stripped):
        return True
    if re.fullmatch(r"O\s*\([^()]+\)", stripped):
        return True
    if has_letter and any(ch in stripped for ch in "_^"):
        return True
    if has_letter and any(ch in stripped for ch in "·−–≤≥≠→←") and (has_digit or len(stripped) <= 24):
        return True
    if has_letter and has_digit and any(ch in stripped for ch in "(),") and len(stripped) <= 24:
        return True
    if re.match(r"^\s*[A-Za-z]{1,3}\s*=\s*", stripped):
        return True
    if re.match(r"^\s*[\d.]+\s*[×x]\s*[\d.]+\s*$", stripped):
        return True
    return False


def normalize_translation_text(text, cache_dir):
    if not text:
        return text

    text = text.replace("&nbsp;", " ").replace("&amp;nbsp;", " ").replace("&#160;", " ")
    chunks = []
    for token in TAG_SPLIT_RE.split(text):
        if not token:
            continue
        if token.startswith("<") and token.endswith(">"):
            chunks.append(token)
            continue

        plain = html.unescape(token).replace("\xa0", " ")
        for part in CJK_RE.split(plain):
            if not part:
                continue
            if CJK_RE.fullmatch(part):
                chunks.append(html.escape(part))
                continue

            if looks_like_formula(part):
                asset = render_math_asset(part, cache_dir)
                chunks.append(
                    f"<img src='{Path(asset['path']).as_posix()}' "
                    f"width='{asset['width_pt']:.1f}' height='{asset['height_pt']:.1f}' valign='middle'/>"
                )
            else:
                escaped = html.escape(part)
                if escaped.strip():
                    chunks.append(f"<font face='Cambria'>{escaped}</font>")
                else:
                    chunks.append(escaped)

    return "".join(chunks)
