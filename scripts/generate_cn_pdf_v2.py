"""
Improved Chinese PDF for 04_edge_detection
Layout: Original slide image (top) + Chinese translation (bottom)
Preserves all diagrams, formulas, and visual content.
"""
import fitz, os, io, json, hashlib
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 PageBreak, HRFlowable, Image, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from PIL import Image as PILImage, ImageDraw, ImageFont
from formula_renderer import normalize_translation_text, render_matrix_asset
from formula_supplements import append_formula_supplement, get_formula_supplement, highlight_translation_text

# ── Setup ──
BASE = r'D:\StudyWorks\3.2\机器视觉\课程ppt'
SRC_DIR = os.path.join(BASE, '原版')       # Original English PDFs
OUT_DIR = os.path.join(BASE, '中文版')      # Translated Chinese PDFs output
TEMP_DIR = os.path.join(BASE, 'temp')       # Working temp files
ORIG_PDF = os.path.join(SRC_DIR, '04_edge detection.pdf')
IMG_DIR = os.path.join(TEMP_DIR, 'slides')
MATRIX_DIR = os.path.join(TEMP_DIR, 'matrix_blocks')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(MATRIX_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Register Chinese fonts
pdfmetrics.registerFont(TTFont('SimHei', r'C:\Windows\Fonts\simhei.ttf'))
pdfmetrics.registerFont(TTFont('SimSun', r'C:\Windows\Fonts\simsun.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('SimKai', r'C:\Windows\Fonts\simkai.ttf'))
pdfmetrics.registerFont(TTFont('YaHei', r'C:\Windows\Fonts\msyh.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('Cambria', r'C:\Windows\Fonts\cambria.ttc', subfontIndex=0))


MATRIX_FONT = r'C:\Windows\Fonts\cambria.ttc'
MATRIX_SCALE = 2


def _load_matrix_font(size):
    return ImageFont.truetype(MATRIX_FONT, size=size, index=0)


def _measure_text(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _draw_bracket(draw, x, top, bottom, side, color, thickness, hook):
    if side == 'left':
        draw.line((x, top, x, bottom), fill=color, width=thickness)
        draw.line((x, top, x + hook, top), fill=color, width=thickness)
        draw.line((x, bottom, x + hook, bottom), fill=color, width=thickness)
    else:
        draw.line((x, top, x, bottom), fill=color, width=thickness)
        draw.line((x - hook, top, x, top), fill=color, width=thickness)
        draw.line((x - hook, bottom, x, bottom), fill=color, width=thickness)


def _matrix_image_path(label, rows):
    signature = label + '|' + '|'.join(' '.join(map(str, row)) for row in rows)
    digest = hashlib.md5(signature.encode('utf-8')).hexdigest()[:12]
    return os.path.join(MATRIX_DIR, f'matrix_{digest}.png')


def matrix_block(label, rows):
    """Render a matrix block using the shared formula renderer."""
    matrix_rows = [row.split() if isinstance(row, str) else list(row) for row in rows]
    asset = render_matrix_asset(label, matrix_rows, TEMP_DIR)
    return Image(asset['path'], width=asset['width_pt'], height=asset['height_pt'])


def add_page_08_content(story):
    """Custom layout for the derivative-kernel page so matrices stay on one page."""
    title_style = ParagraphStyle('P08T', fontName='SimHei', fontSize=16, leading=22,
                                 textColor=HexColor('#16213e'))
    body_style = ParagraphStyle('P08B', fontName='YaHei', fontSize=13, leading=18,
                                textColor=HexColor('#333333'))
    note_style = ParagraphStyle('P08N', fontName='YaHei', fontSize=12, leading=16,
                                textColor=HexColor('#888888'))

    story.append(Paragraph("<b>常用导数近似算子</b>", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Prewitt 算子（3×3）：", body_style))
    story.append(Spacer(1, 4))
    story.append(Table(
        [[
            matrix_block('Mx', ['-1  0  1', '-1  0  1', '-1  0  1']),
            matrix_block('My', ['1  1  1', '0  0  0', '-1 -1 -1']),
        ]],
        colWidths=[245, 245],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ])
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Sobel 算子（3×3，中心加权）：", body_style))
    story.append(Spacer(1, 4))
    story.append(Table(
        [[
            matrix_block('Mx', ['-1  0  1', '-2  0  2', '-1  0  1']),
            matrix_block('My', ['1  2  1', '0  0  0', '-1 -2 -1']),
        ]],
        colWidths=[245, 245],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ])
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Roberts 算子（2×2，对角线）：", body_style))
    story.append(Spacer(1, 4))
    story.append(Table(
        [[
            matrix_block('Mx', ['0  1', '-1 0']),
            matrix_block('My', ['1  0', '0 -1']),
        ]],
        colWidths=[245, 245],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ])
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Sobel 最常用——在中心位置赋予更高权重，对噪声更鲁棒。", body_style))
    supplement = get_formula_supplement('04', 'page_08')
    if supplement:
        story.append(Spacer(1, 6))
        story.append(Paragraph(normalize_translation_text(supplement, TEMP_DIR), body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("（图片来源：K. Grauman）", note_style))

# ── Step 1: Extract all slides as images ──
print("Extracting slides from original PDF...")
doc = fitz.open(ORIG_PDF)
slide_images = []
mat = fitz.Matrix(2, 2)  # 2x zoom

for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(IMG_DIR, f'slide_{i+1:02d}.png')
    pix.save(img_path)
    slide_images.append(img_path)
    print(f"  Slide {i+1}/{len(doc)} saved ({pix.width}x{pix.height})")
doc.close()

# ── Step 2: Translations (same as v1, refined) ──
translations = {
    "page_01": """<font face='SimHei' size='18' color='#16213e'><b>边缘检测</b></font><br/>
<br/>
<font face='YaHei' size='13'>本章介绍计算机视觉中的<b>边缘检测</b>技术，包括图像梯度计算、Canny边缘检测器等核心算法。边缘检测是机器视觉中最基础的特征提取步骤，为后续的分割、识别、跟踪等高层任务提供关键输入。</font>""",

    "page_02": """<font face='SimHei' size='16' color='#16213e'><b>机器视觉技术体系</b></font><br/>
<br/>
<font face='YaHei' size='13'>
本课程涵盖机器视觉的完整技术栈：<br/>
<br/>
• <b>底层特征：</b>边缘与拟合 ← <b>本章重点</b><br/>
• <b>局部特征：</b>角点、斑点、纹理<br/>
• <b>中层处理：</b>分割、聚类<br/>
• <b>高层任务：</b>识别、检测、跟踪<br/>
• <b>几何视觉：</b>相机模型、标定、对极几何、多视图<br/>
<br/>
边缘检测是整个视觉处理流程的<b>第一步</b>，其质量直接影响后续所有处理。</font>""",

    "page_03": """<font face='SimHei' size='16' color='#16213e'><b>边缘检测简介</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>目标：</b>识别图像中像素值的<b>突然变化</b>（不连续性）。<br/>
<br/>
<b>直觉理解：</b>图像中大部分语义和形状信息可以编码在边缘中——比原始像素紧凑得多。<br/>
<br/>
<b>理想状态：</b>像艺术家画的线条一样简洁，但艺术家还使用了物体层面的知识来选择性描绘。<br/>
<br/>
<b>核心优势：</b>边缘大大压缩了数据量，同时保留了关键的形状和结构信息。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：D. Lowe）</font></font>""",

    "page_04": """<font face='SimHei' size='16' color='#16213e'><b>边缘的来源</b></font><br/>
<br/>
<font face='YaHei' size='13'>
边缘由多种物理因素引起：<br/>
<br/>
<table>
<tr><td width="30"><b>①</b></td><td><b>表面法向量不连续</b></td><td>— 物体表面方向突变（如立方体的棱）</td></tr>
<tr><td width="30"><b>②</b></td><td><b>深度不连续</b></td><td>— 前景与背景之间的距离突变</td></tr>
<tr><td width="30"><b>③</b></td><td><b>表面颜色不连续</b></td><td>— 不同颜色或纹理区域的边界</td></tr>
<tr><td width="30"><b>④</b></td><td><b>光照不连续</b></td><td>— 阴影边界或高光区域</td></tr>
</table>
<br/>
<b>共同特征：</b>所有这些不连续性在图像中都表现为亮度的快速变化。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：Steve Seitz）</font></font>""",

    "page_05": """<font face='SimHei' size='16' color='#16213e'><b>边缘的数学特征</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>边缘</b> = 图像亮度函数中<b>快速变化</b>的位置。<br/>
<br/>
考虑图像某一行沿水平方向的亮度函数 f(x)：<br/>
<br/>
• 原始信号在边缘处产生突变<br/>
• <b>一阶导数</b> f'(x) 在边缘处出现<b>极值</b><br/>
• 通过寻找 |f'(x)| 的局部最大值来定位边缘<br/>
<br/>
<b>核心思想：</b>边缘检测 → 计算图像导数 → 寻找极值点。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_06": """<font face='SimHei' size='16' color='#16213e'><b>用卷积计算导数</b></font><br/>
<br/>
<font face='YaHei' size='13'>
对于二维函数 f(x,y)，偏导数的连续定义为：<br/>
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>∂f/∂x = lim(ε→0) [ f(x+ε, y) − f(x, y) ] / ε</b><br/>
<br/>
对于离散图像数据，使用<b>有限差分</b>近似：<br/>
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>∂f(x,y)/∂x ≈ f(x+1, y) − f(x, y)</b><br/>
<br/>
<b>卷积实现：</b>上述运算等价于用滤波器 <b>[-1, 1]</b> 对图像做卷积。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：K. Grauman）</font></font>""",

    "page_07": """<font face='SimHei' size='16' color='#16213e'><b>图像的偏导数</b></font><br/>
<br/>
<font face='YaHei' size='13'>
对图像分别沿 x 和 y 方向求偏导数：<br/>
<br/>
• <b>∂f/∂x：</b>检测<b>垂直边缘</b>——图像在水平方向的变化<br/>
• <b>∂f/∂y：</b>检测<b>水平边缘</b>——图像在垂直方向的变化<br/>
<br/>
观察偏导数图像即可判断：<br/>
→ 哪个滤波器响应垂直边缘？哪个响应水平边缘？<br/>
<br/>
<b>梯度方向与边缘方向垂直</b>是边缘检测中的一个关键关系。</font>""",

    "page_08": """<font face='SimHei' size='16' color='#16213e'><b>常用导数近似算子</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>Prewitt 算子（3×3）：</b><br/>
&nbsp;&nbsp;Mx = <font face='Courier'>[ -1  0  1<br/>&nbsp;&nbsp;&nbsp;&nbsp; -1  0  1<br/>&nbsp;&nbsp;&nbsp;&nbsp; -1  0  1 ]</font><br/>
&nbsp;&nbsp;My = <font face='Courier'>[ 1  1  1<br/>&nbsp;&nbsp;&nbsp;&nbsp; 0  0  0<br/>&nbsp;&nbsp;&nbsp;&nbsp; -1 -1 -1 ]</font><br/>
<br/>
<b>Sobel 算子（3×3，中心加权）：</b><br/>
&nbsp;&nbsp;Mx = <font face='Courier'>[ -1  0  1<br/>&nbsp;&nbsp;&nbsp;&nbsp; -2  0  2<br/>&nbsp;&nbsp;&nbsp;&nbsp; -1  0  1 ]</font><br/>
&nbsp;&nbsp;My = <font face='Courier'>[ 1  2  1<br/>&nbsp;&nbsp;&nbsp;&nbsp; 0  0  0<br/>&nbsp;&nbsp;&nbsp;&nbsp; -1 -2 -1 ]</font><br/>
<br/>
<b>Roberts 算子（2×2，对角线）：</b><br/>
&nbsp;&nbsp;Mx = <font face='Courier'>[ 0  1<br/>&nbsp;&nbsp;&nbsp;&nbsp; -1 0 ]</font>&nbsp;&nbsp;&nbsp;My = <font face='Courier'>[ 1  0<br/>&nbsp;&nbsp;&nbsp;&nbsp; 0 -1 ]</font><br/>
<br/>
<b>Sobel 最常用</b>——在中心位置赋予更高权重，对噪声更鲁棒。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：K. Grauman）</font></font>""",

    "page_09": """<font face='SimHei' size='16' color='#16213e'><b>图像梯度</b></font><br/>
<br/>
<font face='YaHei' size='13'>
图像<b>梯度</b>定义为偏导数向量：<br/>
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b><font face='Cambria'>∇f = [ ∂f/∂x , ∂f/∂y ]</font></b><br/>
<br/>
<b>梯度方向：</b>指向亮度<b>增加最快</b>的方向。<br/>
<b>梯度与边缘的关系：</b>梯度方向 ⊥ 边缘方向。<br/>
<br/>
<b>梯度方向角：</b>&nbsp; <font face='Cambria'>θ = tan⁻¹( (∂f/∂y) / (∂f/∂x) )</font><br/>
<br/>
<b>梯度幅值（边缘强度）：</b><br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b><font face='Cambria'>||∇f|| = √[ (∂f/∂x)² + (∂f/∂y)² ]</font></b><br/>
<br/>
幅值越大 → 该位置越可能是边缘。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Seitz）</font></font>""",

    "page_10": """<font face='SimHei' size='16' color='#16213e'><b>梯度幅值可视化</b></font><br/>
<br/>
<font face='YaHei' size='13'>
分别计算两个方向的导数后合成梯度幅值：<br/>
<br/>
• <b>X方向导数图：</b>突出垂直方向的边缘<br/>
• <b>Y方向导数图：</b>突出水平方向的边缘<br/>
• <b>梯度幅值图：</b>综合所有方向的边缘强度<br/>
<br/>
梯度幅值 = 每个像素位置的"边缘可能性"——亮的像素对应强边缘。</font>""",

    "page_11": """<font face='SimHei' size='16' color='#16213e'><b>噪声对边缘检测的影响</b></font><br/>
<br/>
<font face='YaHei' size='13'>
取图像的一行，将亮度绘制为位置的函数 f(x)：<br/>
<br/>
<b>问题：</b>有噪声时——边缘在哪里？<br/>
<br/>
<b>噪声的影响：</b><br/>
• 噪声在每个像素产生小的随机波动<br/>
• 导数对噪声<b>高度敏感</b>——微小波动被放大<br/>
• 真实边缘的导数值可能被噪声淹没<br/>
<br/>
<b>解决方案：</b>先平滑（滤波），再求导。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Seitz）</font></font>""",

    "page_12": """<font face='SimHei' size='16' color='#16213e'><b>方案：先平滑，再求导</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>流程：</b><br/>
&nbsp;&nbsp;① 对信号 f 用高斯滤波器 g 平滑 → f * g<br/>
&nbsp;&nbsp;② 对平滑后的信号求导 → d/dx (f * g)<br/>
&nbsp;&nbsp;③ 寻找导数的<b>峰值</b> → 峰值位置 = 边缘位置<br/>
<br/>
<b>效果：</b><br/>
• 不滤波直接求导 → 噪声淹没边缘<br/>
• 高斯平滑后求导 → 清晰的边缘检测<br/>
<br/>
<b>关键洞察：</b>平滑消除了高频噪声，同时保留了真正的边缘信号。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Seitz）</font></font>""",

    "page_13": """<font face='SimHei' size='16' color='#16213e'><b>卷积微分定理（Derivative Theorem）</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>关键数学性质：</b>微分是卷积，而卷积满足结合律。<br/>
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>d/dx (f * g) = f * (d/dx g)</b><br/>
<br/>
<b>实践意义——节省一次运算：</b><br/>
• 不需要：先平滑 → 再求导（两次操作）<br/>
• 可以：直接用<b>高斯导数滤波器</b>对原图做一次卷积<br/>
<br/>
<b>结果完全相同，但计算效率更高。</b><br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Seitz）</font></font>""",

    "page_14": """<font face='SimHei' size='16' color='#16213e'><b>高斯导数滤波器</b></font><br/>
<br/>
<font face='YaHei' size='13'>
对高斯函数 G(x,y) 求偏导得到两个滤波器：<br/>
<br/>
• <b>∂G/∂x：</b>x方向高斯导数 → 检测<b>垂直边缘</b><br/>
• <b>∂G/∂y：</b>y方向高斯导数 → 检测<b>水平边缘</b><br/>
<br/>
<b>可分离性：</b>高斯导数滤波器<b>是可分离的</b>——可以分解为两个一维滤波器的级联，大幅降低计算复杂度。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_15": """<font face='SimHei' size='16' color='#16213e'><b>高斯导数：x方向 vs y方向</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>判断规则：</b><br/>
<br/>
• <b>x方向的高斯导数（∂G/∂x）：</b>对<b>水平方向</b>的变化敏感<br/>
  → 检测<b>垂直走向</b>的边缘<br/>
<br/>
• <b>y方向的高斯导数（∂G/∂y）：</b>对<b>垂直方向</b>的变化敏感<br/>
  → 检测<b>水平走向</b>的边缘<br/>
<br/>
<b>记忆技巧：</b>导数的方向 = 边缘的<b>法线方向</b>，垂直于边缘本身。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_16": """<font face='SimHei' size='16' color='#16213e'><b>高斯导数滤波器的尺度选择</b></font><br/>
<br/>
<font face='YaHei' size='13'>
不同 σ（标准差）对应不同检测尺度：<br/>
<br/>
<table>
<tr><td width="60"><b>σ=1 px</b></td><td>检测<b>细小边缘</b></td><td>精确定位</td><td>对噪声敏感</td></tr>
<tr><td width="60"><b>σ=3 px</b></td><td>检测<b>中等边缘</b></td><td>平衡取舍</td><td>常用默认值</td></tr>
<tr><td width="60"><b>σ=7 px</b></td><td>检测<b>粗大边缘</b></td><td>鲁棒性好</td><td>定位精度降低</td></tr>
</table>
<br/>
<b>核心矛盾：</b>小尺度 → 定位准但噪声敏感；大尺度 → 鲁棒但边缘模糊。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：D. Forsyth）</font></font>""",

    "page_17": """<font face='SimHei' size='16' color='#16213e'><b>平滑滤波器 vs 导数滤波器</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>平滑滤波器（高斯）：</b><br/>
• 功能：去除高频成分 → "低通"滤波器<br/>
• 值能否为负？<b>不能</b>——平滑是加权平均，负值无意义<br/>
• 值之和 = <b>1</b>——保证恒定亮度区域不受影响<br/>
<br/>
<b>导数滤波器（高斯导数）：</b><br/>
• 功能：检测亮度变化<br/>
• 值能否为负？<b>能，必须有</b>——正负交替才能检测变化<br/>
• 值之和 = <b>0</b>——恒定区域没有变化，响应为零<br/>
• 在对比度高的位置产生<b>高绝对值</b>响应<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_18": """<font face='SimHei' size='16' color='#16213e'><b>Canny 边缘检测器</b></font><br/>
<br/>
<font face='YaHei' size='13'>
J. Canny (1986) 提出的经典算法，至今仍是<b>最广泛使用的边缘检测器</b>。<br/>
<br/>
<b>三条最优准则：</b><br/>
&nbsp;&nbsp;① <b>好的检测率</b>——不漏检真实边缘，不误报<br/>
&nbsp;&nbsp;② <b>好的定位</b>——检测到的边缘尽可能接近真实边缘位置<br/>
&nbsp;&nbsp;③ <b>单一响应</b>——每个边缘只被标记一次<br/>
<br/>
下面逐一介绍 Canny 检测器的四个核心步骤。</font>""",

    "page_19": """<font face='SimHei' size='16' color='#16213e'><b>Canny 步骤①：计算梯度幅值</b></font><br/>
<br/>
<font face='YaHei' size='13'>
用高斯导数滤波器对图像滤波，计算每个像素的梯度幅值：<br/>
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b><font face='Cambria'>||∇f|| = √[ (∂f/∂x)² + (∂f/∂y)² ]</font></b><br/>
<br/>
<b>结果特征：</b><br/>
• 边缘区域 → 梯度幅值大（亮）<br/>
• 平坦区域 → 梯度幅值小（暗）<br/>
• <b>边缘线条较粗</b> → 需要后续细化处理<br/>
<br/>
此时得到的是一张"边缘强度图"，边缘呈现为宽的亮带。</font>""",

    "page_20": """<font face='SimHei' size='16' color='#16213e'><b>Canny 步骤②：阈值化</b></font><br/>
<br/>
<font face='YaHei' size='13'>
对梯度幅值图像应用阈值，区分边缘和非边缘：<br/>
<br/>
• 高阈值 → 只保留最确定的强边缘<br/>
• 低阈值 → 保留更多但引入噪声<br/>
<br/>
<b>问题：</b>阈值化后的边缘仍然是<b>粗的带</b>（多像素宽），不是我们想要的细曲线。<br/>
<br/>
<b>下一步需要：</b>将粗带细化为单像素宽度的曲线。</font>""",

    "page_21": """<font face='SimHei' size='16' color='#16213e'><b>Canny 需要解决的两个问题</b></font><br/>
<br/>
<font face='YaHei' size='13'>
阈值化后的梯度幅值图存在两个关键问题：<br/>
<br/>
<b>问题 ①：边缘太粗</b><br/>
边缘呈现为多像素宽的"脊"，需要细化为单像素曲线。<br/>
→ 解决方案：<b>非极大值抑制（NMS）</b><br/>
<br/>
<b>问题 ②：边缘断裂</b><br/>
低对比度边缘被阈值切断，强边缘之间失去连接。<br/>
→ 解决方案：<b>滞后阈值（Hysteresis）</b><br/>
<br/>
接下来分别介绍这两个关键技术。</font>""",

    "page_22": """<font face='SimHei' size='16' color='#16213e'><b>非极大值抑制（NMS）</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>目标：</b>将粗边缘细化为单像素宽度。<br/>
<br/>
<b>算法流程：</b><br/>
&nbsp;&nbsp;① 对每个像素，沿其<b>梯度方向</b>检查相邻像素<br/>
&nbsp;&nbsp;② 如果当前像素的梯度幅值 <b>不是</b>梯度方向上的局部最大值<br/>
&nbsp;&nbsp;③ 则将其抑制（置为 0）<br/>
&nbsp;&nbsp;④ 只保留该方向上的最大响应值<br/>
<br/>
<b>结果：</b>原来多像素宽的边缘被压缩为单像素宽的细线。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_23": """<font face='SimHei' size='16' color='#16213e'><b>Canny 完整处理流程</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>原始图像</b><br/>
&nbsp;&nbsp;↓ 高斯导数滤波<br/>
<b>梯度幅值图</b>（边缘粗，含噪声）<br/>
&nbsp;&nbsp;↓ 非极大值抑制（NMS）<br/>
<b>细化后的边缘</b>（单像素宽，仍有假边缘）<br/>
&nbsp;&nbsp;↓ 滞后阈值<br/>
<b>最终边缘图</b>（清晰、连续、单像素宽）<br/>
<br/>
<b>NMS 解决了"粗"的问题，但噪声引起的假边缘仍需阈值处理。</b><br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_24": """<font face='SimHei' size='16' color='#16213e'><b>滞后阈值（Hysteresis Thresholding）</b></font><br/>
<br/>
<font face='YaHei' size='13'>
使用<b>两个阈值</b>而不是一个：<br/>
<br/>
• <b>高阈值 T_high：</b>用于<b>启动</b>（seed）边缘曲线<br/>
  → 只有梯度幅值 &gt; T_high 的点被标记为"确定边缘"<br/>
<br/>
• <b>低阈值 T_low：</b>用于<b>延续</b>（extend）边缘曲线<br/>
  → 从确定边缘点出发，沿边缘方向追踪<br/>
  → 只要梯度幅值 &gt; T_low 就继续延伸<br/>
<br/>
<b>效果：</b>强边缘完整保留，连接在强边缘上的弱边缘被保留，孤立的弱边缘（噪声）被丢弃。<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Seitz）</font></font>""",

    "page_25": """<font face='SimHei' size='16' color='#16213e'><b>滞后阈值——三种阈值效果对比</b></font><br/>
<br/>
<font face='YaHei' size='13'>
同一张原始图像，三种阈值策略的结果：<br/>
<br/>
• <b>仅用高阈值：</b>只有强边缘——可能不完整、断裂<br/>
• <b>仅用低阈值：</b>边缘完整——但包含大量噪声<br/>
• <b>滞后阈值（高+低）：</b>边缘完整且噪声少——<b>最佳效果</b><br/>
<br/>
<b>这是 Canny 检测器超越简单边缘检测方法的关键设计。</b><br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：L. Fei-Fei）</font></font>""",

    "page_26": """<font face='SimHei' size='16' color='#16213e'><b>Canny 边缘检测器——完整算法总结</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>步骤 1：高斯导数滤波</b><br/>
对图像使用高斯导数滤波器 → 同时完成平滑和微分<br/>
<br/>
<b>步骤 2：计算梯度幅值和方向</b><br/>
<font face='Cambria'>||∇f|| = √[(∂f/∂x)² + (∂f/∂y)²]&nbsp;&nbsp;|&nbsp;&nbsp;θ = tan⁻¹(∂y/∂x)</font><br/>
<br/>
<b>步骤 3：非极大值抑制</b><br/>
沿梯度方向只保留局部最大值 → 宽脊变为单像素<br/>
<br/>
<b>步骤 4：滞后阈值</b><br/>
高阈值启动边缘 + 低阈值延续边缘 → 连续且干净的边缘图<br/>
<br/>
<b>MATLAB：</b>edge(image, 'canny')<br/>
<b>OpenCV：</b>cv2.Canny(image, low, high)<br/>
<br/>
<font face='YaHei' size='11' color='#666666'><b>参考文献：</b>J. Canny, "A Computational Approach To Edge Detection", IEEE TPAMI, 8:679-714, 1986.</font></font>""",

    "page_27": """<font face='SimHei' size='16' color='#16213e'><b>边缘检测只是起点……</b></font><br/>
<br/>
<font face='YaHei' size='13'>
边缘检测是通往更高级视觉理解的<b>第一步</b>：<br/>
<br/>
<b>原始图像 → 人工标注 → 分割结果 → 边缘检测</b><br/>
<br/>
边缘信息是以下任务的基础输入：<br/>
• <b>图像分割</b>——基于边缘的轮廓分割<br/>
• <b>物体识别</b>——形状匹配与轮廓分析<br/>
• <b>场景理解</b>——从边缘到语义<br/>
<br/>
<b>Berkeley 分割数据库（BSDS500）：</b><br/>
标准评估基准：http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/segbench/<br/>
<br/>
<font face='YaHei' size='11' color='#888888'>（图片来源：S. Lazebnik）</font></font>""",

    "page_28": """<font face='SimHei' size='17' color='#16213e'><b>本章小结</b></font><br/>
<br/>
<font face='YaHei' size='13'>
<b>1. 边缘</b> = 图像亮度函数的快速变化位置<br/>
<b>2. 图像梯度</b> → 偏导数 → 梯度幅值 = 边缘强度<br/>
<b>3. 噪声问题</b> → 高斯平滑后再求导<br/>
<b>4. 卷积微分定理</b> → 高斯导数滤波器：一次卷积 = 平滑 + 求导<br/>
<b>5. 离散导数算子</b> → Sobel, Prewitt, Roberts<br/>
<b>6. Canny 边缘检测器</b>（四步法）：<br/>
&nbsp;&nbsp;&nbsp;&nbsp;高斯导数滤波 → 梯度幅值/方向 → NMS → 滞后阈值<br/>
<br/>
<b>下一章预告：</b>拟合——将检测到的边缘点拟合成直线、圆等几何形状。</font>"""
}

# ── Step 3: Generate PDF with image + translation layout ──
OUTPUT = os.path.join(OUT_DIR, '04_边缘检测_中文版.pdf')

# Use landscape A4 for better slide image display
page_w, page_h = A4  # portrait: 595.27 x 841.89 points
# We'll use portrait with slide image on top

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=30, leftMargin=30,
    topMargin=25, bottomMargin=25,
    title='边缘检测 (中文版·含原图)',
    author='Machine Vision Course'
)

# Styles
cover_title = ParagraphStyle('CT', fontName='SimHei', fontSize=26, leading=36,
    alignment=TA_CENTER, textColor=HexColor('#0f3460'))
cover_sub = ParagraphStyle('CS', fontName='SimHei', fontSize=14, leading=22,
    alignment=TA_CENTER, textColor=HexColor('#555555'))
slide_title = ParagraphStyle('ST', fontName='SimHei', fontSize=11, leading=16,
    textColor=HexColor('#999999'), alignment=TA_CENTER)
divider_style = ParagraphStyle('DV', fontName='SimHei', fontSize=8, leading=12,
    textColor=HexColor('#cccccc'), alignment=TA_CENTER)

story = []

# ── Cover ──
story.append(Spacer(1, 100))
story.append(Paragraph('机器视觉技术', cover_title))
story.append(Spacer(1, 12))
story.append(Paragraph('第4章：边缘检测', cover_sub))
story.append(Spacer(1, 8))
story.append(Paragraph('Edge Detection — 中文翻译版（含原图）', cover_sub))
story.append(Spacer(1, 50))
story.append(Paragraph('每页包含：原始英文幻灯片截图 + 中文翻译解读',
    ParagraphStyle('note', fontName='YaHei', fontSize=12, leading=18,
    alignment=TA_CENTER, textColor=HexColor('#888888'))))
story.append(Paragraph('翻译时间：2026年6月 | 基于 Tesseract OCR + 人工校对',
    ParagraphStyle('note2', fontName='YaHei', fontSize=10, leading=14,
    alignment=TA_CENTER, textColor=HexColor('#aaaaaa'))))
story.append(PageBreak())

# ── Content pages ──
# Calculate image dimensions to fit on A4 portrait
# A4 portrait: 595.27 x 841.89 points
# Available width: 595.27 - 60 = 535 points
# Image should fit within 535 points width, maintaining aspect ratio
# Slides are 16:9 (e.g., 1920x1080 with 2x zoom)
# Let image width = 520 points, height = 520 * 9/16 = 292.5 points
# Text area takes remaining space

img_width = 510  # points
img_height = img_width * 9 / 16  # 286.875 points for 16:9 slides

margin_bottom_img = 8  # space after image
margin_before_text = 6  # space before text

for i in range(1, 29):
    key = f'page_{i:02d}'
    img_path = os.path.join(IMG_DIR, f'slide_{i:02d}.png')

    if not os.path.exists(img_path):
        continue

    # Page header
    header = Paragraph(f'第 {i} 页 / 共 28 页  |  边缘检测 Edge Detection',
        ParagraphStyle('header', fontName='SimHei', fontSize=8, leading=12,
        textColor=HexColor('#bbbbbb'), alignment=TA_CENTER))
    story.append(header)
    story.append(Spacer(1, 4))

    # Original slide image
    img = Image(img_path, width=img_width, height=img_height)
    story.append(img)
    story.append(Spacer(1, margin_bottom_img))

    # Divider
    story.append(HRFlowable(width="95%", thickness=1, color=HexColor('#0f3460'),
        spaceBefore=2, spaceAfter=4))

    # Chinese translation
    if key in translations:
        if key == 'page_08':
            add_page_08_content(story)
        else:
            trans_style = ParagraphStyle(
                f'trans_{i}', fontName='YaHei', fontSize=13, leading=20,
                textColor=HexColor('#333333'),
            )
            base_translation = highlight_translation_text(translations[key])
            raw_translation = append_formula_supplement('04', key, base_translation)
            translation = normalize_translation_text(raw_translation, TEMP_DIR)
            story.append(Paragraph(translation, trans_style))

    # Bottom divider
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="60%", thickness=0.3, color=HexColor('#dddddd'),
        spaceBefore=2, spaceAfter=2))

    if i < 28:
        story.append(PageBreak())

# Build
doc.build(story)
print(f'\nChinese PDF v2 generated: {OUTPUT}')
print(f'Layout: Original slide image + Chinese translation per page')
print(f'Total slides processed: 28')
