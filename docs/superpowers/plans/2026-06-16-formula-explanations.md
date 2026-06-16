# Formula Explanations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add concise learning-oriented explanations to formula-heavy pages in the translated machine-vision course PDFs so parameters, symbols, and assumptions are easier to understand.

**Architecture:** Add a shared supplement layer that appends page-specific explanatory HTML blocks during PDF generation. The general chapter generator and the chapter 04 hand-tuned generator will both call the same helper, so the content stays consistent across the pipeline. Keep the supplements short and page-local so they fit the existing "original slide + translation" layout without changing visual structure.

**Tech Stack:** Python 3.13, ReportLab, PyMuPDF, Pillow, existing `formula_renderer.py`.

---

### Task 1: Create shared formula supplement module

**Files:**
- Create: `scripts/formula_supplements.py`

- [ ] **Step 1: Define the supplement lookup**

Create a nested mapping from chapter id and page key to short HTML fragments. Cover the formula-heavy pages in chapters 03, 04, 05_1, 05_2, 06, 07, 08, and 09.

- [ ] **Step 2: Add a helper function**

Implement a function that appends the supplement block to an existing translated page string and returns the combined HTML.

- [ ] **Step 3: Keep the output short**

Use concise prose, `"<br/>"` line breaks, and no placeholder text so the existing KeepInFrame layout does not collapse too aggressively.

### Task 2: Wire the general PDF generator to the supplement layer

**Files:**
- Modify: `scripts/generate_pdf.py:18-148`

- [ ] **Step 1: Import the supplement helper**

Call the helper immediately after `normalize_translation_text(...)` so every page uses the same supplement behavior.

- [ ] **Step 2: Apply supplements during rendering**

Append the helper output only when a page has an entry in the supplement mapping. Leave all other pages unchanged.

- [ ] **Step 3: Keep the current layout unchanged**

Do not change page size, image placement, or translation box sizing.

### Task 3: Update the chapter 04 hand-tuned generator

**Files:**
- Modify: `scripts/generate_cn_pdf_v2.py:77-657`

- [ ] **Step 1: Reuse the shared supplement helper**

Apply the same supplement logic to the embedded translation dictionary after it is defined, so the hand-tuned chapter 04 PDF gets the same extra explanations.

- [ ] **Step 2: Extend the custom page 08 content**

Add a short explanatory paragraph after the prebuilt matrix-layout content to explain the derivative kernels and sign conventions.

- [ ] **Step 3: Preserve the existing custom layout**

Keep the special matrix table layout and the current page structure intact.

### Task 4: Regenerate PDFs and verify visually

**Files:**
- Modify: `中文版/*.pdf`

- [ ] **Step 1: Regenerate the affected chapters**

Run the chapter 04 hand-tuned generator and the general generator for the remaining chapters that use `temp/translations/*.json`.

- [ ] **Step 2: Render representative pages to PNG**

Use `pdftoppm` on formula-heavy pages from each regenerated PDF to confirm the extra text fits and remains readable.

- [ ] **Step 3: Check for regressions**

Verify that no page overflow, clipped text, or broken formula rendering was introduced.

- [ ] **Step 4: Commit**

Stage the script changes and the regenerated PDFs together so the updated artifacts stay in sync with the source content.
