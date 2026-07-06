---
name: accessibility-audit
description: "A skill to audit accessibility of a codebase."
---

When invoked, audit the target codebase for accessibility issues and produce a structured report. Follow these steps:

## 1. Determine scope
- If the user gave a path or repository, use it; otherwise audit the current working directory.
- Find UI-bearing files: `*.html`, `*.jsx`, `*.tsx`, `*.vue`, `*.svelte`, plus CSS/SCSS for contrast-related rules. Skip `node_modules`, `dist`, `build`, `.venv`, `venv`.

## 2. Check each of the following (WCAG 2.1 AA-oriented)
- **Images & media**: `<img>` without `alt` (or meaningless `alt="image"`), decorative images missing `alt=""`, `<video>`/`<audio>` without captions or transcripts.
- **Forms**: inputs without an associated `<label>` (or `aria-label`/`aria-labelledby`), missing fieldset/legend for grouped controls, no visible error messaging tied to the field via `aria-describedby`.
- **Semantic structure**: div/span used where a semantic element (`button`, `nav`, `header`, `main`, `table`) belongs, non-sequential heading hierarchy (e.g. `h1` → `h3`), missing `lang` attribute on `<html>`.
- **Keyboard & focus**: click handlers on non-interactive elements without a matching `keydown`/`keypress` handler or `tabindex`, positive `tabindex` values, removed focus outlines (`outline: none`) without a visible replacement, no visible focus-trap handling in modals/dialogs.
- **ARIA usage**: ARIA roles/attributes that duplicate or contradict native semantics, `aria-hidden="true"` on focusable content, missing `role="alert"`/`aria-live` for dynamic status messages.
- **Color & contrast**: color used as the only signal (e.g. red/green without icon or text), hardcoded low-contrast color pairs in CSS (check against a 4.5:1 text / 3:1 large-text or UI-component ratio).
- **Interactive components**: custom widgets (dropdowns, tabs, accordions, carousels) missing the expected ARIA pattern (role, `aria-expanded`, `aria-controls`) and keyboard interactions (Arrow keys, Escape, Enter/Space).

## 3. Compile the report
For each finding, record:
- The affected file(s) and line/element.
- A severity: `élevé` (blocks assistive tech / WCAG failure), `moyen` (degrades UX for some users), `faible` (best-practice polish).
- A concrete, actionable recommendation (the fix, not just the problem).

Group findings by category (Images & media, Forms, Semantic structure, Keyboard & focus, ARIA, Color & contrast, Interactive components).

## 4. Optional roadmap
If the user asks for a roadmap, prioritize fixes: all `élevé` findings first (grouped by shared root cause where possible), then `moyen`, then `faible`.

## 5. Output
Write the report as Markdown by default. Emit JSON alongside it only if the user asks for machine-readable output. Do not invent findings — if a category has no issues, state that explicitly rather than omitting it silently.
