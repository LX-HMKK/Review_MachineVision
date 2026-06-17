from __future__ import annotations
import re


ACCENT_RED = "#d32f2f"
ACCENT_BLUE = "#1565c0"
ACCENT_ORANGE = "#ef6c00"
ACCENT_GREEN = "#2e7d32"


def note(*lines: str) -> str:
    body = "<br/>".join(lines)
    return (
        "<font face='YaHei' size='12' color='#666666'>"
        "<b>学习补充：</b><br/>"
        f"{body}"
        "</font>"
    )


def accent(text: str, color: str = ACCENT_RED) -> str:
    return f"<font color='{color}'><b>{text}</b></font>"


def repeat(supplement: str, *page_keys: str) -> dict[str, str]:
    return {page_key: supplement for page_key in page_keys}


INLINE_BOLD_RE = re.compile(r"<b>([^<]+)</b>")
LEADING_LABEL_RE = re.compile(r"(^|<br/>)(\s*[@>•\-—]?\s*)([^<：:=]{2,18}?)(\s*[：:=])")

LABEL_COLORS = {
    "目标：": ACCENT_RED,
    "核心：": ACCENT_BLUE,
    "核心思想：": ACCENT_BLUE,
    "关键：": ACCENT_RED,
    "关键点：": ACCENT_RED,
    "结论：": ACCENT_ORANGE,
    "注意：": ACCENT_ORANGE,
    "直觉理解：": ACCENT_GREEN,
    "直觉：": ACCENT_GREEN,
    "优势：": ACCENT_BLUE,
    "回忆：": ACCENT_GREEN,
    "步骤：": ACCENT_BLUE,
    "问题：": ACCENT_RED,
    "答案：": ACCENT_BLUE,
}

KEYWORD_COLORS = {
    "本章重点": ACCENT_RED,
    "第一步": ACCENT_BLUE,
    "边缘检测": ACCENT_RED,
    "梯度": ACCENT_BLUE,
    "霍夫变换": ACCENT_ORANGE,
    "高斯": ACCENT_BLUE,
    "中值滤波": ACCENT_GREEN,
    "K-means": ACCENT_RED,
    "mean shift": ACCENT_ORANGE,
    "normalized cut": ACCENT_BLUE,
    "Bag-of-features": ACCENT_GREEN,
    "HOG": ACCENT_RED,
    "boosting": ACCENT_ORANGE,
}


def _pick_leading_color(label: str) -> str | None:
    compact = label.strip()
    if not compact:
        return None

    if any(token in compact for token in ("重点", "关键", "问题", "挑战", "误差", "检测", "边缘", "目标")):
        return ACCENT_RED
    if any(token in compact for token in ("模型", "步骤", "方法", "特征", "任务", "表示", "处理", "视觉", "窗口")):
        return ACCENT_BLUE
    if any(token in compact for token in ("注意", "结论", "变换", "少见", "代价", "约束")):
        return ACCENT_ORANGE
    if any(token in compact for token in ("直觉", "回忆", "补充", "理解", "优势")):
        return ACCENT_GREEN
    return None


def highlight_translation_text(text: str) -> str:
    """Add color emphasis to important translation labels and bolded key phrases."""
    if not text:
        return text

    highlighted = text

    for label, color in LABEL_COLORS.items():
        highlighted = highlighted.replace(f"<b>{label}</b>", accent(label, color))

    def _color_bold(match: re.Match[str]) -> str:
        inner = match.group(1)
        if inner in LABEL_COLORS:
            return accent(inner, LABEL_COLORS[inner])
        return accent(inner, ACCENT_BLUE)

    highlighted = INLINE_BOLD_RE.sub(_color_bold, highlighted)

    def _color_leading_label(match: re.Match[str]) -> str:
        prefix, marker, label, delimiter = match.groups()
        color = _pick_leading_color(label)
        if color is None:
            return match.group(0)
        return f"{prefix}{marker}{accent(label.rstrip() + delimiter, color)}"

    highlighted = LEADING_LABEL_RE.sub(_color_leading_label, highlighted)

    for keyword, color in KEYWORD_COLORS.items():
        highlighted = highlighted.replace(keyword, f"<font color='{color}'><b>{keyword}</b></font>")

    return highlighted


PERSPECTIVE_EQUATION = "x' = f x / z, y' = f y / z"


NOTE_PINHOLE_CAMERA = note(
    f"• {accent('针孔', ACCENT_RED)}让每个物点基本只通过一条光线落到胶片上，因此模糊会明显减轻。",
    f"• 代价是通光量变小，所以画面会更{accent('暗', ACCENT_ORANGE)}；这就是“小孔换清晰”的核心权衡。",
)

NOTE_IMAGE_PLANE = note(
    f"• {accent('f', ACCENT_BLUE)} 是焦距，表示针孔到像平面的距离；{accent('O', ACCENT_RED)} 是光心/摄像机中心。",
    f"• {accent('虚拟像平面', ACCENT_GREEN)} 只是为了避免倒像，推导时把像平面放到相机前方会更方便。",
)

NOTE_PERSPECTIVE = note(
    f"• 透视投影的关键是{accent('按深度 z 缩放', ACCENT_RED)}：{accent('离得越远，像得越小', ACCENT_ORANGE)}。",
    f"• {accent(PERSPECTIVE_EQUATION, ACCENT_BLUE)} 说明像平面坐标不是线性的，而是由三维点除以深度得到的。",
)

NOTE_PIXELS = note(
    f"• {accent('c_x, c_y', ACCENT_BLUE)} 把光心平移到图像中心附近；{accent('α, β', ACCENT_RED)} 把米制坐标换成像素坐标。",
    f"• 记住：{accent('f', ACCENT_ORANGE)} 是物理焦距，{accent('k, l', ACCENT_GREEN)} 是像素尺度，别把单位混在一起。",
)

NOTE_DISTORTION = note(
    f"• {accent('失焦', ACCENT_ORANGE)} 会让点扩散成模糊斑；孔径太小虽然更清晰，但亮度会下降。",
    f"• {accent('径向畸变', ACCENT_RED)} 会让直线在图像边缘变弯，常见两种形态是{accent('桶形', ACCENT_BLUE)}和{accent('枕形', ACCENT_GREEN)}。",
)

NOTE_APERTURE = note(
    f"• 这页的核心是{accent('孔径 / 光圈', ACCENT_RED)}：孔径越小，景深越大，但进光量会下降。",
    f"• 真实成像里，{accent('焦距', ACCENT_BLUE)}、{accent('孔径', ACCENT_ORANGE)}和{accent('对焦距离', ACCENT_GREEN)}会一起影响清晰度。",
)

NOTE_APERTURE_TRADEOFF = note(
    f"• {accent('光圈越小越清晰', ACCENT_RED)}这件事有前提：模糊圈会变小，但{accent('亮度也会下降', ACCENT_ORANGE)}。",
    f"• 这两页想强调的是成像里的基本权衡：{accent('清晰度', ACCENT_BLUE)}、{accent('景深', ACCENT_GREEN)}和{accent('通光量', ACCENT_RED)}不能同时拉满。",
)

NOTE_LENS_FOCUSING = note(
    f"• {accent('透镜', ACCENT_BLUE)}的作用不是简单放大，而是把同一物点来的多条光线重新{accent('汇聚', ACCENT_RED)}到像面上。",
    f"• 它比针孔更亮，但也更依赖{accent('对焦位置', ACCENT_ORANGE)}和{accent('焦距', ACCENT_GREEN)}的控制。",
)

NOTE_PARAXIAL_MODEL = note(
    f"• {accent('近轴近似', ACCENT_RED)}只在小角度、靠近光轴时成立，所以适合做课堂里的简化推导。",
    f"• 这个模型的价值是把复杂折射关系压成可计算的几何关系，便于后面连接到相机成像公式。",
)

NOTE_CAMERA_SKEW = note(
    f"• {accent('θ', ACCENT_RED)} 描述像素坐标轴是否正交；理想相机里通常接近 {accent('90°', ACCENT_BLUE)}。",
    f"• 当坐标轴不完全垂直时，就会出现{accent('偏斜项', ACCENT_ORANGE)}，它会进入内参矩阵 K。",
)

NOTE_PROJECTION_MATRIX = note(
    f"• {accent('M', ACCENT_RED)} 是 3×4 的投影矩阵，作用是把三维点的{accent('齐次坐标', ACCENT_BLUE)}映到图像平面。",
    f"• 看到 {accent('P′ = MP', ACCENT_GREEN)} 时，要立刻想到“先线性映射，再做归一化恢复欧式坐标”。",
)

NOTE_INTRINSIC_DOF = note(
    f"• 这页问的是{accent('K 有多少自由度', ACCENT_RED)}，标准答案是 {accent('5 DOF', ACCENT_BLUE)}。",
    f"• 它们通常对应{accent('两个尺度', ACCENT_ORANGE)}、{accent('主点坐标', ACCENT_GREEN)}和{accent('偏斜', ACCENT_RED)}。",
)

NOTE_CAMERA_GEOMETRY = note(
    f"• 完整模型可以压成 {accent('P′ = K[R|T]P_w', ACCENT_RED)}：{accent('K', ACCENT_BLUE)} 管成像，{accent('[R|T]', ACCENT_ORANGE)} 管位姿。",
    f"• 这就是后面标定和参数分解的起点，所有求解基本都围着这条式子展开。",
)

NOTE_SVD_CALIBRATION = note(
    f"• 把标定写成 {accent('Pm = 0', ACCENT_RED)} 后，本质上是在找一个非零向量 m，使残差尽量小。",
    f"• {accent('SVD', ACCENT_BLUE)} 会把这个问题转成“取最小奇异值对应的右奇异向量”，这是线性标定里最常见的套路。",
)

NOTE_PARAMETER_EXTRACTION = note(
    f"• 这里是在把求出的 {accent('M = [A\\ b]', ACCENT_RED)} 继续拆成 {accent('K、R、T', ACCENT_BLUE)} 三部分。",
    f"• 记忆顺序最好固定成：先从 {accent('A', ACCENT_ORANGE)} 恢复内参与旋转，再从 {accent('b', ACCENT_GREEN)} 恢复平移。",
)

NOTE_PROJECTION_THEOREM = note(
    f"• 这类定理页不是让你硬背全部条件，而是告诉你：{accent('什么样的 3×4 矩阵', ACCENT_RED)} 才能合法表示透视相机。",
    f"• 复习时先抓住 {accent('Det(A) ≠ 0', ACCENT_BLUE)} 和矩阵可分解性，再回头看其余约束。",
)

NOTE_NONLINEARITY = note(
    f"• {accent('P 到 P′ 不是线性变换', ACCENT_RED)}，因为中间要做一次除以深度 z 的透视除法。",
    f"• 这也是为什么要引入{accent('齐次坐标', ACCENT_BLUE)}：先把投影写成矩阵，再在最后恢复欧式坐标。",
)

NOTE_HOMOGENEOUS = note(
    f"• 齐次坐标把“除法投影”改写成更方便的矩阵形式，便于把投影看成线性代数问题。",
    f"• 最后再做一次{accent('归一化', ACCENT_BLUE)}（除以最后一维），就能回到欧式坐标。",
)

NOTE_INTRINSIC_EXTRINSIC = note(
    f"• {accent('K', ACCENT_BLUE)} 描述内参，{accent('[R|T]', ACCENT_RED)} 描述外参；合起来才是完整的相机投影模型。",
    f"• 这一步的核心是：先把世界坐标变到相机坐标，再用内参映射到像素坐标。",
)

NOTE_ORTHOGRAPHIC = note(
    f"• 正交投影把透视里的深度缩放近似成 1，因此{accent('不再有近大远小', ACCENT_ORANGE)}。",
    f"• 它更适合远距离目标或深度变化很小的场景，但会损失透视信息。",
)

NOTE_CALIBRATION = note(
    f"• 标定的目标是从已知的 3D-2D 对应点里求出相机的{accent('内参', ACCENT_BLUE)}和{accent('外参', ACCENT_RED)}。",
    f"• 这种问题通常写成最小化 {accent('Pm = 0', ACCENT_ORANGE)}，再用奇异值分解或等价的线性代数方法求解。",
)

NOTE_DECOMPOSITION = note(
    f"• 看到 {accent('ρ[Ab] = K[R|T]', ACCENT_RED)} 时，要立刻想到：左边是投影矩阵分解，右边是在恢复内参与外参。",
    f"• 右下角的 {accent('T = ρK⁻¹b', ACCENT_BLUE)} 说明平移项可以在分解后单独恢复。",
)

NOTE_DEGENERACY = note(
    f"• {accent('所有标定点不能共面', ACCENT_RED)}，否则解会退化，内外参会变得不稳定。",
    f"• 这页的重点不是具体数值，而是提醒你：标定数据要有足够的{accent('三维几何约束', ACCENT_ORANGE)}。",
)


NOTE_CONVOLUTION = note(
    "• 卷积可以理解为把一个局部模板放到图像上滑动，对邻域像素做加权求和。",
    "• 核里的正负权重决定它更偏向平滑还是增强边缘，不同符号约定不会改变“看哪里变快”这个核心意思。",
    "• 边界处的 full / same / valid 只是保留输出范围不同，重点是输出尺寸和边缘补齐方式。",
)

NOTE_FILTER_PROPERTIES = note(
    "• 结合律、分配律的意义是：多个小滤波器可以合成更高效的等价滤波。",
    "• 单位脉冲相当于卷积里的“什么都不改”，所以它常被拿来说明卷积的基本性质。",
)

NOTE_BOUNDARY_HANDLING = note(
    "• 这一页强调的是边界处理，不是公式本身变了。",
    "• full / same / valid 的区别在于卷积核碰到图像边缘时，输出要不要保留那些不完整的重叠位置。",
    "• 记住：尺寸变化来自边界，内容变化来自卷积核。",
)

NOTE_GAUSSIAN_KERNEL = note(
    "• 高斯核本质上是在做“按距离递减”的平滑，离中心越远权重越小。",
    "• σ 越大，平滑越强，保留细节越少；σ 越小，结果越接近原图。",
)

NOTE_KERNEL_WIDTH = note(
    "• 经验上核半宽取到约 3σ，已经能覆盖大部分能量。",
    "• 核太窄会截断高斯尾部，核太宽则计算开销变大。",
)

NOTE_SEPARABILITY = note(
    "• 二维高斯可拆成两个一维高斯，因此先做横向再做纵向会更快。",
    "• 可分离的真正价值是把二维卷积拆成两个一维卷积，复杂度大幅下降。",
)

NOTE_SEPARABILITY_AND_MEDIAN = note(
    "• 这类页面想说明的是：不同滤波器之间可以对比“平滑强度”和“是否保细节”。",
    "• Box filter 更像粗略平均，高斯更平滑自然，中值滤波更适合压制椒盐噪声。",
)

NOTE_GAUSSIAN_AND_NOISE = note(
    "• 高斯平滑的作用是压低高频噪声，但代价是会变模糊。",
    "• 图像里越细的结构越容易被大尺度平滑抹掉，所以 σ 不能一味加大。",
)

NOTE_MEDIAN_FILTER = note(
    "• 中值滤波对椒盐噪声特别有效，因为它不看平均值，而是看排序后的中间值。",
    "• 代价是细线和尖锐结构可能被削弱，所以它更适合处理脉冲噪声，而不是一切模糊问题。",
)

NOTE_SHARPENING_AND_UNSHARP = note(
    "• 锐化通常是把细节分量加回原图，因此会让边缘更突出。",
    "• Unsharp mask 其实就是“原图 + 细节增强”的一种标准做法。",
)

NOTE_EDGE_INTRO = note(
    "• 边缘本质上就是亮度函数发生快速变化的位置。",
    "• 真实图像里通常先平滑再求导，否则噪声会把导数放大。",
)

NOTE_DERIVATIVE_AND_GRADIENT = note(
    "• 图像可以看成亮度函数，偏导数描述某个方向上的变化速度。",
    "• x 方向导数更容易响应竖直边，y 方向导数更容易响应水平边。",
    "• 梯度向量指向变化最快的方向，而边缘方向与梯度方向垂直。",
)

NOTE_FINITE_DIFFERENCE_KERNELS = note(
    "• Prewitt、Sobel、Roberts 都是在用离散差分近似导数。",
    "• Sobel 在中间行/列加了更高权重，所以比 Prewitt 更抗噪；Roberts 用 2×2 对角差分，响应更敏感。",
)

NOTE_SMOOTH_FIRST = note(
    "• 先平滑再求导是边缘检测里最重要的稳健化步骤之一。",
    "• 原因很简单：求导会放大高频分量，而噪声本身就是高频。",
)

NOTE_DERIVATIVE_OF_GAUSSIAN = note(
    "• 先对图像做高斯平滑，再求导，等价于直接使用高斯导数核。",
    "• 这样可以把“平滑”和“求导”合并成一步，同时保留边缘、压制噪声。",
)

NOTE_SCALE_SPACE_AND_BLOBS = note(
    "• 多尺度的核心是：同一个结构在不同尺度下的响应不一样，不能只看单一尺寸。",
    "• 对 blob 来说，关键不是“有没有响应”，而是“在哪个尺度上响应最强”。",
)

NOTE_CANNY_PIPELINE = note(
    "• Canny 不是简单阈值法，而是一条完整流水线：平滑、求梯度、细化、连接。",
    "• 它想要的是“细、稳、连贯”的边缘，而不是一堆粗糙的高响应点。",
)

NOTE_NMS = note(
    "• 非极大值抑制沿梯度方向做比较，只保留局部峰值。",
    "• 目的不是找“更大的数”，而是把边缘细化成单像素宽。",
)

NOTE_HYSTERESIS = note(
    "• 双阈值的作用是把“可信边缘”和“可能边缘”分开。",
    "• 低阈值像是候选池，高阈值像是锚点；只有连到锚点的弱响应才会被保留。",
)

NOTE_CANNY_RECAP = note(
    "• 这页是在总结 Canny 的思想：先把边缘找出来，再把边缘变细，再把断裂边缘连起来。",
    "• 这比单纯看阈值稳定得多，也更符合人眼对边缘的理解。",
)

NOTE_LSQ_LINE = note(
    "• 直线模型里，斜率决定倾斜程度，截距决定与 y 轴的交点。",
    "• 最小二乘要做的是让所有点到直线的误差平方和最小，因此会得到正规方程。",
)

NOTE_TOTAL_LSQ_AND_MLE = note(
    "• 当 x/y 两个方向都存在测量误差时，单纯看竖直残差就不够合理，应该改用正交距离。",
    "• 从概率角度看，若噪声近似服从高斯分布，最大似然通常会导向最小二乘。",
)

NOTE_ROBUST_ESTIMATORS = note(
    "• 鲁棒估计的目的，是让少数离群点不要把整体模型带偏。",
    "• 和普通最小二乘相比，它会弱化大残差点的影响，因此对异常值更稳。",
)

NOTE_RANSAC = note(
    "• RANSAC 的核心不是一次算出完美模型，而是反复随机抽最小样本，找“支持者最多”的模型。",
    "• s 是最小样本数，d 是内点阈值，N 是重复次数；这些参数共同控制鲁棒性和计算量。",
)

NOTE_HOUGH_LINES = note(
    "• 霍夫变换把“图像空间中的点”转换成“参数空间中的一条候选曲线”。",
    "• 累加器里的峰值不是某个像素，而是很多边缘点共同支持的参数组合。",
    "• 用 ρ/θ 表示直线比 m/b 更稳定，因为竖直线也能自然表示。",
)

NOTE_HOUGH_ACCUM_AND_GRADIENT = note(
    "• 累加器里的每个格子代表一个参数区间，投票越多，说明越可能是真实几何结构。",
    "• 利用梯度方向可以把投票范围缩小，减少无效投票和噪声干扰。",
)

NOTE_HOUGH_CIRCLES = note(
    "• 圆检测比直线检测更贵，因为参数维度更高，投票空间更大。",
    "• 已知边缘法线方向时，可以把中心候选限制在更小范围内，从而降低计算量。",
)

NOTE_GENERALIZED_HOUGH = note(
    "• 广义霍夫不是只找直线或圆，而是找任意模板的稳定几何配置。",
    "• 参考点和投票表的作用，是把复杂形状转成可搜索的参数空间模式。",
)

NOTE_HARRIS_MATRIX = note(
    "• Harris 检测器会把一个窗口里的梯度平方项和交叉项汇总成二阶矩阵。",
    "• 这个矩阵描述的是：窗口在各个方向上“变化有多大”。",
)

NOTE_HARRIS_EIGEN_AND_RESPONSE = note(
    "• 两个特征值都小，说明局部很平；一个大一个小，说明像边；两个都大，才像角点。",
    "• 响应值把“两个方向都强”与“只有一个方向强”分开，所以角点会更突出。",
)

NOTE_HARRIS_INVARIANCE = note(
    "• 角点检测希望对平移、旋转、尺度变化尽量稳定。",
    "• 这也是后面尺度空间和仿射适配要解决的问题：同一个结构在不同变换下仍然要找到。",
)

NOTE_BLOB_SCALE = note(
    "• Blob 的关键不是单一响应，而是在不同尺度上找最强响应。",
    "• 尺度归一化的作用，是让不同尺度下的响应可以公平比较。",
)

NOTE_BLOB_CHARACTERISTIC = note(
    "• 特征尺度就是响应达到峰值时对应的那一层尺度。",
    "• 这让同一个 blob 在不同分辨率下仍然能被稳定定位。",
)

NOTE_KMEANS = note(
    "• k-means 反复做两件事：把点分给最近中心，再用新分组更新中心。",
    "• 它的目标是让组内距离尽量小，所以特别依赖初始中心和特征尺度。",
)

NOTE_TEXTURE_STATISTICS = note(
    "• 纹理特征通常不是看单个像素，而是看一组响应的统计分布。",
    "• 均值描述典型值，协方差描述各维变化的相关性和方向性。",
)

NOTE_FILTER_BANKS = note(
    "• filter bank 的思想是用一组不同尺度、不同方向的滤波器一起描述纹理。",
    "• 单个滤波器往往不够，真正有用的是整组响应的组合模式。",
)

NOTE_MEANSHIFT = note(
    "• mean shift 会反复把窗口中心移动到局部密度更高的位置。",
    "• 带宽决定“看多大范围”，太小会碎，太大会把不同模式混在一起。",
)

NOTE_GRAPH_CUTS = note(
    "• 图像分割里，亲和度越高，说明两个像素越应该被放在同一组。",
    "• 把图像看成图之后，分割问题就变成了“怎样切图更合理”。",
)

NOTE_NORMALIZED_CUT = note(
    "• normalized cut 不只看切口大小，还看切开后两边各自保留了多少内部连接。",
    "• 归一化的作用，是避免算法偏爱切出很小但代价看起来很低的碎片。",
)

NOTE_STATISTICAL_VIEWPOINT = note(
    "• 分类可以直接学“给定图像属于某类的概率”，也可以先学“某类如何生成图像”。",
    "• 判别模型更关注决策边界，生成模型更关注数据分布本身。",
)

NOTE_GENERATIVE_MODELS = note(
    "• 生成模型会为每个类别建立一个数据生成假设，再比较哪一类更可能产生当前图像。",
    "• 这类模型更容易解释，但对建模假设的要求也更强。",
)

NOTE_BOOSTING = note(
    "• boosting 会把多个弱分类器按顺序组合起来，后面的分类器更关注前面分错的样本。",
    "• 它的目标不是让单个分类器特别强，而是让一串“还不错”的分类器合起来很强。",
)

NOTE_VIOLA_JONES = note(
    "• Viola-Jones 的关键是把检测做快：积分图让矩形求和很快，级联让大多数负样本尽早退出。",
    "• 它特别适合滑动窗口检测，因为每个窗口都要被快速评估。",
)

NOTE_BAG_OF_FEATURES = note(
    "• Bag-of-features 先把局部特征量化成“视觉词”，再统计词频。",
    "• 它会丢掉很多精确位置，但换来更稳定的整体表示。",
)

NOTE_HOG = note(
    "• HOG 统计的是局部梯度方向分布，重点放在轮廓和形状。",
    "• 做完归一化之后，它对光照变化会更稳，所以常用于行人检测。",
)

NOTE_OBJECT_DETECTION = note(
    "• 目标检测比分类更难，因为它要同时回答“是什么”和“在哪里”。",
    "• 滑动窗口、特征提取和非极大值抑制通常要配合使用。",
)

NOTE_PED_DET = note(
    "• 行人检测通常会把 HOG 特征和一个线性分类器结合起来，再对整张图做窗口扫描。",
    "• 效果很依赖训练数据是否覆盖了常见的尺度、姿态和遮挡变化。",
)


FORMULA_SUPPLEMENTS = {
    "02": {
        **repeat(NOTE_PINHOLE_CAMERA, "page_06"),
        **repeat(NOTE_IMAGE_PLANE, "page_07"),
        **repeat(NOTE_APERTURE_TRADEOFF, "page_11", "page_12"),
        **repeat(NOTE_LENS_FOCUSING, "page_13", "page_14"),
        **repeat(NOTE_PARAXIAL_MODEL, "page_15"),
        **repeat(NOTE_CAMERA_SKEW, "page_27", "page_28"),
        **repeat(NOTE_PROJECTION_MATRIX, "page_29", "page_30"),
        **repeat(NOTE_INTRINSIC_DOF, "page_31", "page_32"),
        **repeat(NOTE_CAMERA_GEOMETRY, "page_33", "page_34", "page_37"),
        **repeat(NOTE_PERSPECTIVE, "page_09", "page_35"),
        **repeat(NOTE_PIXELS, "page_10", "page_19", "page_20"),
        **repeat(NOTE_DISTORTION, "page_16", "page_17"),
        **repeat(NOTE_APERTURE, "page_18"),
        **repeat(NOTE_NONLINEARITY, "page_21"),
        **repeat(NOTE_HOMOGENEOUS, "page_22", "page_23", "page_24", "page_30"),
        **repeat(NOTE_INTRINSIC_EXTRINSIC, "page_25", "page_26", "page_36"),
        **repeat(NOTE_ORTHOGRAPHIC, "page_40", "page_45", "page_46", "page_47", "page_48"),
        **repeat(NOTE_CALIBRATION, "page_60", "page_70"),
        **repeat(NOTE_SVD_CALIBRATION, "page_71", "page_72", "page_73"),
        **repeat(NOTE_PARAMETER_EXTRACTION, "page_74", "page_75", "page_76", "page_77", "page_78", "page_79"),
        **repeat(NOTE_PROJECTION_THEOREM, "page_41"),
        **repeat(NOTE_DECOMPOSITION, "page_80", "page_81"),
        **repeat(NOTE_DEGENERACY, "page_82", "page_83"),
    },
    "03": {
        **repeat(NOTE_CONVOLUTION, "page_10"),
        **repeat(NOTE_FILTER_PROPERTIES, "page_11", "page_12"),
        **repeat(NOTE_BOUNDARY_HANDLING, "page_13", "page_14", "page_15"),
        **repeat(NOTE_SEPARABILITY_AND_MEDIAN, "page_27", "page_28", "page_33", "page_34", "page_41", "page_42", "page_45"),
        **repeat(NOTE_GAUSSIAN_KERNEL, "page_29", "page_30"),
        **repeat(NOTE_KERNEL_WIDTH, "page_31", "page_32"),
        **repeat(NOTE_SEPARABILITY, "page_35", "page_36", "page_37"),
        **repeat(NOTE_GAUSSIAN_AND_NOISE, "page_38", "page_39", "page_40"),
        **repeat(NOTE_MEDIAN_FILTER, "page_43", "page_44"),
        **repeat(NOTE_SHARPENING_AND_UNSHARP, "page_46", "page_47", "page_48"),
    },
    "04": {
        **repeat(NOTE_EDGE_INTRO, "page_05"),
        **repeat(NOTE_DERIVATIVE_AND_GRADIENT, "page_06", "page_07", "page_09", "page_10"),
        **repeat(NOTE_FINITE_DIFFERENCE_KERNELS, "page_08"),
        **repeat(NOTE_SMOOTH_FIRST, "page_11", "page_12"),
        **repeat(NOTE_DERIVATIVE_OF_GAUSSIAN, "page_13", "page_14", "page_15"),
        **repeat(NOTE_SCALE_SPACE_AND_BLOBS, "page_16", "page_17"),
        **repeat(NOTE_CANNY_PIPELINE, "page_18", "page_19", "page_20", "page_21"),
        **repeat(NOTE_NMS, "page_22", "page_23"),
        **repeat(NOTE_HYSTERESIS, "page_24", "page_25"),
        **repeat(NOTE_CANNY_RECAP, "page_26"),
    },
    "05_1": {
        **repeat(NOTE_LSQ_LINE, "page_07", "page_08"),
        **repeat(NOTE_TOTAL_LSQ_AND_MLE, "page_09", "page_10", "page_11", "page_12", "page_13", "page_14", "page_15"),
        **repeat(NOTE_ROBUST_ESTIMATORS, "page_18"),
        **repeat(NOTE_RANSAC, "page_23", "page_35", "page_38", "page_39"),
    },
    "05_2": {
        **repeat(NOTE_HOUGH_LINES, "page_04", "page_05", "page_06", "page_07", "page_08", "page_09", "page_10", "page_11"),
        **repeat(NOTE_HOUGH_ACCUM_AND_GRADIENT, "page_12", "page_17", "page_18", "page_19", "page_20", "page_21", "page_22", "page_23"),
        **repeat(NOTE_HOUGH_CIRCLES, "page_24", "page_25"),
        **repeat(NOTE_GENERALIZED_HOUGH, "page_26", "page_27", "page_28", "page_29"),
        **repeat(NOTE_OBJECT_DETECTION, "page_30", "page_31", "page_32"),
    },
    "06": {
        **repeat(NOTE_HARRIS_MATRIX, "page_10", "page_11", "page_12", "page_13", "page_14", "page_15"),
        **repeat(NOTE_HARRIS_EIGEN_AND_RESPONSE, "page_16", "page_17", "page_18", "page_19", "page_20", "page_21", "page_22", "page_23", "page_24"),
        **repeat(NOTE_HARRIS_INVARIANCE, "page_31", "page_32", "page_33", "page_34", "page_35"),
    },
    "07": {
        **repeat(NOTE_SCALE_SPACE_AND_BLOBS, "page_05", "page_06", "page_08", "page_09", "page_10", "page_11", "page_12"),
        **repeat(NOTE_BLOB_SCALE, "page_13", "page_14", "page_18", "page_24", "page_26", "page_27"),
        **repeat(NOTE_BLOB_CHARACTERISTIC, "page_15", "page_16", "page_17", "page_29"),
    },
    "08": {
        **repeat(NOTE_TEXTURE_STATISTICS, "page_30", "page_55"),
        **repeat(NOTE_FILTER_BANKS, "page_31", "page_32", "page_33", "page_34", "page_35", "page_36", "page_37"),
        **repeat(NOTE_BAG_OF_FEATURES, "page_44", "page_45", "page_46", "page_47", "page_48", "page_49", "page_50", "page_51", "page_52", "page_53", "page_54", "page_57", "page_58", "page_59", "page_60", "page_61"),
    },
    "09": {
        **repeat(NOTE_KMEANS, "page_13", "page_14", "page_15", "page_16", "page_17"),
        **repeat(NOTE_MEANSHIFT, "page_18", "page_19", "page_20", "page_21", "page_22", "page_23", "page_24", "page_25"),
        **repeat(NOTE_GRAPH_CUTS, "page_30", "page_31", "page_32", "page_33"),
        **repeat(NOTE_NORMALIZED_CUT, "page_34", "page_35", "page_36", "page_37", "page_38", "page_39", "page_40", "page_41", "page_50"),
        **repeat(NOTE_OBJECT_DETECTION, "page_44", "page_45", "page_46", "page_47", "page_48", "page_49", "page_51"),
    },
    "10": {
        **repeat(NOTE_STATISTICAL_VIEWPOINT, "page_31", "page_32", "page_33"),
        **repeat(NOTE_GENERATIVE_MODELS, "page_35", "page_36", "page_37", "page_38"),
        **repeat(NOTE_BAG_OF_FEATURES, "page_43", "page_44", "page_46", "page_47", "page_48", "page_49", "page_50", "page_51", "page_52", "page_53", "page_54", "page_55", "page_63", "page_64", "page_65", "page_66", "page_67", "page_68", "page_69", "page_70", "page_71", "page_72"),
        **repeat(NOTE_KMEANS, "page_56", "page_57", "page_58", "page_59", "page_60", "page_61", "page_62"),
    },
    "11": {
        **repeat(NOTE_BOOSTING, "page_13", "page_16", "page_17", "page_18", "page_19", "page_20", "page_21", "page_22", "page_23", "page_24", "page_25"),
        **repeat(NOTE_VIOLA_JONES, "page_26", "page_27", "page_28", "page_29", "page_30", "page_31", "page_32", "page_33", "page_34", "page_35", "page_36", "page_37", "page_38", "page_39", "page_40", "page_41", "page_42", "page_43", "page_44"),
        **repeat(NOTE_OBJECT_DETECTION, "page_45", "page_49", "page_50", "page_57"),
        **repeat(NOTE_HOG, "page_47", "page_48", "page_52"),
        **repeat(NOTE_PED_DET, "page_53", "page_54", "page_55"),
    },
}


def get_formula_supplement(chapter_id: str, page_key: str) -> str:
    return FORMULA_SUPPLEMENTS.get(chapter_id, {}).get(page_key, "")


def append_formula_supplement(chapter_id: str, page_key: str, text: str) -> str:
    supplement = get_formula_supplement(chapter_id, page_key)
    if not supplement:
        return text
    if not text:
        return supplement
    return f"{text}<br/><br/>{supplement}"
