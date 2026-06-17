# Machine Vision Exam Review Markdown Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a printable Markdown review document for the machine vision course that combines high-frequency exam lookup tables with chapter-by-chapter concepts, formulas, workflows, and pitfalls.

**Architecture:** Build one primary Markdown artifact under `docs/` and author it in four passes: front-matter fast lookup, exam answer templates, chapter-by-chapter content, and final condensed appendix. Reuse `试卷/试卷分析及今年预测.md`, `temp/translations/*.json`, and `scripts/formula_supplements.py` as the authoritative source pool for weighting, definitions, and formula explanations.

**Tech Stack:** Markdown, PowerShell, git, existing repo documents and JSON translations

---

## File Structure

- Create: `docs/机器视觉开卷考试复习资料.md`
- Modify: `docs/superpowers/plans/2026-06-17-exam-review-md.md`
- Reference: `docs/superpowers/specs/2026-06-17-exam-review-md-design.md`
- Reference: `试卷/试卷分析及今年预测.md`
- Reference: `temp/translations/trans_03.json`
- Reference: `temp/translations/trans_05_1.json`
- Reference: `temp/translations/trans_05_2.json`
- Reference: `temp/translations/trans_06.json`
- Reference: `temp/translations/trans_07.json`
- Reference: `temp/translations/trans_08.json`
- Reference: `temp/translations/trans_09.json`
- Reference: `temp/translations/trans_10.json`
- Reference: `temp/translations/trans_11.json`
- Reference: `scripts/formula_supplements.py`

### Task 1: Create the review document skeleton

**Files:**
- Create: `docs/机器视觉开卷考试复习资料.md`
- Reference: `docs/superpowers/specs/2026-06-17-exam-review-md-design.md`

- [ ] **Step 1: Write the top-level Markdown skeleton**

```md
# 机器视觉开卷考试复习资料

> 适用范围：Ch02-Ch11
> 使用方式：优先看“高频考点速查”和“题型模板”，再按章节翻查细节

## 一、高频考点速查

## 二、题型作答模板

## 三、分章节完整复习资料

### Ch02 成像与标定

### Ch03 滤波

### Ch04 边缘检测

### Ch05_1 拟合

### Ch05_2 霍夫变换

### Ch06 角点检测

### Ch07 Blob / SIFT

### Ch08 纹理

### Ch09 分割

### Ch10 识别

### Ch11 目标检测

## 四、最后冲刺页
```

- [ ] **Step 2: Save the skeleton with `apply_patch` and verify the headings exist**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern '^#|^##|^###'`
Expected: one document title, four top-level sections, and chapter subsections from `Ch02` through `Ch11`

- [ ] **Step 3: Commit the skeleton**

```bash
git add docs/机器视觉开卷考试复习资料.md
git commit -m "docs(复习): 初始化开卷考试资料框架"
```

### Task 2: Fill the high-frequency lookup section

**Files:**
- Modify: `docs/机器视觉开卷考试复习资料.md`
- Reference: `试卷/试卷分析及今年预测.md`
- Reference: `README.md`

- [ ] **Step 1: Add the exam-weight summary table and priority guidance**

```md
## 一、高频考点速查

### 1. 去年分值与今年复习优先级

| 章节 | 去年分值 | 今年复习级别 | 备注 |
|:--|:--:|:--:|:--|
| Ch03 滤波 | 22 | 最高 | 计算题主战场 |
| Ch04 边缘检测 | 16 | 最高 | Canny 流程高频 |
| Ch06 角点检测 | 11 | 高 | Harris 判据常考 |
| Ch07 Blob / SIFT | 12 | 高 | SIFT 步骤与不变性 |
| Ch08 纹理 | 11 | 高 | 方法论述题 |
| Ch09 分割 | 12 | 高 | 形态学识图题 |
```

- [ ] **Step 2: Add three compact lookup tables**

```md
### 2. 必背公式速查
### 3. 必会流程速查
### 4. 高频辨析速查
```

The formulas table must include at minimum:
- camera projection `P' = K[R|T]P_w`
- convolution output size
- Gaussian kernel and separability
- Harris response
- Hough line equation
- k-means objective

- [ ] **Step 3: Verify all three lookup tables exist**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern '必背公式速查|必会流程速查|高频辨析速查'`
Expected: exactly three matching subsection headings

- [ ] **Step 4: Commit the lookup section**

```bash
git add docs/机器视觉开卷考试复习资料.md
git commit -m "docs(复习): 补充高频考点速查"
```

### Task 3: Fill the answer-template section

**Files:**
- Modify: `docs/机器视觉开卷考试复习资料.md`
- Reference: `试卷/试卷分析及今年预测.md`

- [ ] **Step 1: Add templates for choice and judgment questions**

```md
## 二、题型作答模板

### 1. 选择题 / 判断题

- 先判断题干在问“定义、性质、步骤、适用场景”中的哪一种。
- 若出现“唯一、一定、总是、完全不受影响”等绝对化措辞，优先怀疑为错。
- 若题干比较两个方法，先写出两者的核心目标，再看噪声、复杂度、不变性、是否线性。
```

- [ ] **Step 2: Add templates for calculation, workflow, and essay questions**

```md
### 2. 计算题
1. 先写输入尺寸、核尺寸、padding、stride。
2. 再写输出尺寸公式。
3. 再写单个输出像素的乘法/加法次数。
4. 最后写总复杂度或可分离优化。

### 3. 流程题
- 按“输入 -> 核心步骤 -> 每步作用 -> 输出效果”写。

### 4. 论述题
- 先写方法目标。
- 再写核心思想。
- 再写关键步骤或公式。
- 最后写优点、缺点、适用场景。
```

- [ ] **Step 3: Verify the section contains all four template subsections**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern '^### 1\\. 选择题 / 判断题|^### 2\\. 计算题|^### 3\\. 流程题|^### 4\\. 论述题'`
Expected: four matches

- [ ] **Step 4: Commit the answer-template section**

```bash
git add docs/机器视觉开卷考试复习资料.md
git commit -m "docs(复习): 补充题型作答模板"
```

### Task 4: Write the chapter content for Ch02-Ch05_2

**Files:**
- Modify: `docs/机器视觉开卷考试复习资料.md`
- Reference: `scripts/formula_supplements.py`
- Reference: `试卷/试卷分析及今年预测.md`
- Reference: `temp/translations/trans_03.json`
- Reference: `temp/translations/trans_05_1.json`
- Reference: `temp/translations/trans_05_2.json`

- [ ] **Step 1: Fill Ch02 and Ch03 using the fixed per-chapter template**

```md
### Ch02 成像与标定

#### 本章核心考点
#### 关键概念
#### 关键公式与符号意义
#### 高频比较与易错点
#### 可能出题方式

### Ch03 滤波

#### 本章核心考点
#### 卷积、边界处理与输出尺寸
#### 高斯滤波、中值滤波与锐化
#### 关键公式与符号意义
#### 计算题答题框架
#### 高频比较与易错点
```

Ch03 must explicitly include:
- `full/same/valid`
- Gaussian vs box vs median
- unsharp masking
- separability and complexity

- [ ] **Step 2: Fill Ch04, Ch05_1, and Ch05_2**

```md
### Ch04 边缘检测
#### Canny 五步
#### NMS、双阈值与滞后连接

### Ch05_1 拟合
#### 最小二乘、全最小二乘、RANSAC

### Ch05_2 霍夫变换
#### 点到参数空间的映射
#### ρ-θ 直线表示
#### 圆霍夫与广义霍夫
```

- [ ] **Step 3: Verify these five chapters contain formula blocks and pitfalls**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern '符号解释|常见误区|Harris|ρ = x cosθ \\+ y sinθ|full / same / valid|RANSAC'`
Expected: matches across Ch02-Ch05_2 content, not only in the front lookup section

- [ ] **Step 4: Commit the first half of chapter content**

```bash
git add docs/机器视觉开卷考试复习资料.md
git commit -m "docs(复习): 完成前五章考试资料整理"
```

### Task 5: Write the chapter content for Ch06-Ch11

**Files:**
- Modify: `docs/机器视觉开卷考试复习资料.md`
- Reference: `scripts/formula_supplements.py`
- Reference: `试卷/试卷分析及今年预测.md`
- Reference: `temp/translations/trans_06.json`
- Reference: `temp/translations/trans_07.json`
- Reference: `temp/translations/trans_08.json`
- Reference: `temp/translations/trans_09.json`
- Reference: `temp/translations/trans_10.json`
- Reference: `temp/translations/trans_11.json`

- [ ] **Step 1: Fill Ch06-Ch08**

```md
### Ch06 角点检测
#### Harris 二阶矩阵与响应函数
#### 特征值判据
#### 与 Moravec 的比较

### Ch07 Blob / SIFT
#### 尺度空间、LoG、DoG
#### SIFT 的关键步骤与不变性

### Ch08 纹理
#### 统计纹理
#### 滤波器组、LBP、GLCM
```

- [ ] **Step 2: Fill Ch09-Ch11**

```md
### Ch09 分割
#### k-means、mean shift、graph cuts、normalized cut
#### 形态学识图题判断口诀

### Ch10 识别
#### 生成式 vs 判别式
#### Bag-of-Features 与空间金字塔

### Ch11 目标检测
#### 滑动窗口与 NMS
#### boosting、Viola-Jones、HOG
```

- [ ] **Step 3: Verify all high-frequency chapter anchors and expected keywords exist**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern 'Moravec|LoG|DoG|LBP|GLCM|normalized cut|Bag-of-Features|Viola-Jones|HOG|积分图'`
Expected: at least one match for each keyword family in the relevant chapter section

- [ ] **Step 4: Commit the second half of chapter content**

```bash
git add docs/机器视觉开卷考试复习资料.md
git commit -m "docs(复习): 完成后六章考试资料整理"
```

### Task 6: Add the final sprint page and perform end-to-end verification

**Files:**
- Modify: `docs/机器视觉开卷考试复习资料.md`
- Reference: `docs/superpowers/specs/2026-06-17-exam-review-md-design.md`

- [ ] **Step 1: Add the final condensed appendix**

```md
## 四、最后冲刺页

### 1. 高频公式总表
### 2. 高频方法步骤总表
### 3. 高频错误说法总表
```

The final appendix must include explicit wrong-statement examples such as:
- `Harris 具有尺度不变性`
- `中值滤波是线性滤波`
- `Hough 直线表示中的 θ 是直线方向角`

- [ ] **Step 2: Run structural verification on headings and chapter coverage**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern '^## |^### Ch'`
Expected: sections `一` through `四`, plus chapter headings from `Ch02` through `Ch11`

- [ ] **Step 3: Run content verification for spec coverage**

Run: `Select-String -Path 'docs/机器视觉开卷考试复习资料.md' -Pattern '符号解释|常见考法|常见误区|计算题答题框架|形态学识图题判断口诀|最后冲刺页'`
Expected: all six patterns match

- [ ] **Step 4: Inspect the final diff for accidental omissions or duplicated placeholders**

Run: `git diff -- docs/机器视觉开卷考试复习资料.md`
Expected: no placeholder text such as `TODO`, `TBD`, `待补`, or empty chapter subsections

- [ ] **Step 5: Commit the final review document**

```bash
git add docs/机器视觉开卷考试复习资料.md
git commit -m "feat(复习): 完成机器视觉开卷考试资料"
```

## Self-Review

### Spec coverage

- High-frequency lookup section: covered by Task 2
- Answer-template section: covered by Task 3
- Chapter-by-chapter full review: covered by Tasks 4 and 5
- Final sprint page: covered by Task 6
- Formula field standard (`公式 / 符号解释 / 物理或算法含义 / 常见考法 / 常见误区`): enforced in Tasks 4, 5, and 6 verification
- Chapter weighting strategy from exam analysis: integrated in Tasks 2, 4, and 5

No spec sections are left without a corresponding task.

### Placeholder scan

Plan contains no `TODO`, `TBD`, `implement later`, or unresolved file references. All output paths are explicit.

### Type consistency

- Final document path is consistently `docs/机器视觉开卷考试复习资料.md`
- Spec path is consistently `docs/superpowers/specs/2026-06-17-exam-review-md-design.md`
- Plan uses the same four-section document structure throughout
