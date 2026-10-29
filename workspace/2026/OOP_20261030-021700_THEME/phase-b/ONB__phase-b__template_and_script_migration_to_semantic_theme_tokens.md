# ONB — OOP_20261030-021700_THEME / Phase B: Template and Script Migration to Semantic Theme Tokens

> **Current filename**: `ONB__phase-b__template_and_script_migration_to_semantic_theme_tokens.md`
> **Date**: 2026-10-30
> **Author**: Executor (`antigravity:thread:local:d6d0abd2-257b-428e-8e1e-390307d02fbd`)
> **Status**: 🟠 ONB — Onboarding recorded
> **Parent HL**: [HL-OOP_20261030-021700_THEME.md](../HL-OOP_20261030-021700_THEME.md)
> **TS**: [TS__phase-b__template_and_script_migration_to_semantic_theme_tokens.md](TS__phase-b__template_and_script_migration_to_semantic_theme_tokens.md)
> **Producer unit**: `antigravity:thread:local:d6d0abd2-257b-428e-8e1e-390307d02fbd`
> **Parent Coordinator**: `antigravity:thread:local:d1962507-3018-4f36-b88f-ccb71a3279b4`
> **Activation / dispatch source**: owner-direct (`/tfw-handoff OOP_20261030-021700_THEME/phase-b`)
> **Coordination authority**: "HL-OOP_20261030-021700_THEME.md @ 91921d22dfbf9a87cc18a0ae194b435b713bcb69"
> **Originating proposer**: `none`

---

## 1. Understanding

Phase B completes the end-to-end migration of the Web-OOP platform markup to the design tokens established in Phase A. All hardcoded decorative Tailwind classes (`sky-`, `cyan-`, `amber-`) in Jinja2 subtemplates (`tab_home.html`, `tab_theory.html`, `tab_practice.html`, `tab_quiz.html`, `tab_results.html`, `header.html`, `exam.html`, and `uml_viewer.html`) and client-side dynamic HTML string generators in `app.js` are migrated to semantic CSS custom properties and helper classes. The functional status colors (PASS = `emerald`, FAIL = `rose`) and internal Clean Architecture class diagram node colors remain strictly isolated and preserved.

## 2. Entry Points

- `app/static/css/style.css`: Add semantic helper classes (`.theme-accent-text`, `.subtab-active`, `.week-pill-active`) to link UI components cleanly to active CSS variables.
- `app/templates/components/header.html`: Refactor active week pills and subtabs to use theme variables instead of fixed sky/blue gradients.
- `app/templates/components/tab_home.html`, `tab_theory.html`, `tab_practice.html`, `tab_quiz.html`, `tab_results.html`: Migrate hardcoded accent classes to semantic theme tokens.
- `app/templates/exam.html`: Migrate accent borders, badges, and layout highlights to theme tokens while preserving exam scoring badges.
- `app/templates/components/uml_viewer.html`: Adapt container shell, toolbar, and lens border to theme variables without altering inner SVG diagram node colors.
- `app/static/js/app.js`: Refactor template string HTML generators to use theme classes.
- `tests/test_theme_system.py`: Add assertion tests covering Phase B criteria AC-1 — AC-6 and verify full regression suite pass.

Task-owned temporary resources: isolated test scratch runs in `%TEMP%\tfw\OOP_20261030-021700_THEME\`.

## 3. Questions (blocking — cannot proceed without answers)

No blocking questions.

## 4. Recommendations (suggestions, not blocking)

1. Retain the semantic classes `.week-pill-active` and `.subtab-active` in `style.css` rather than replacing them with raw inline styles in templates, ensuring full backward compatibility with `test_ui_ergonomics.py`.
2. Use CSS variables directly in SVG stroke/fill attributes (e.g. `stroke="var(--theme-accent)"`) for crisp vector scaling in `uml_viewer.html` controls.

## 5. Risks Found (edge cases, potential issues not in TS)

1. *Ergonomics test sensitivity:* `tests/test_ui_ergonomics.py` checks for the presence of certain class names in `style.css`. Maintaining those class selectors while updating their properties to `var(--theme-*)` prevents false regression failures.

## 6. Inconsistencies with Code (spec vs reality)

None. The codebase is clean, Phase A is completed and accepted at Candidate `5855e38a94e3293f65efc0ad3bc3a32861c83439`, and all 67 tests currently pass.

## 7. Knowledge Citations

| # | HL §7.2 ref | Read? | Applied / N/A | Notes |
|---|-------------|-------|---------------|-------|
| 1 | `README.md` (P0) § Цель и North Star проекта | ✅ | Applied | Guiding visual ergonomics and clean interface for students |
| 2 | `.tfw/README.md` (P1) Success Criteria #ns1, #ns2 | ✅ | Applied | Preserving testable, verifiable, and placeholder-free implementation |
| 3 | `knowledge/philosophy.md` (P2) Zero-Build & Clean Architecture | ✅ | Applied | Zero-Build preserved strictly; no npm/bundler dependencies added |
| 4 | `KNOWLEDGE.md` §1 (P3) D1 (Стек проекта) | ✅ | Applied | FastAPI, Jinja2, Tailwind CDN, Vanilla JS |
| 5 | `KNOWLEDGE.md` §1 (P3) D5 (Zero-Build интерфейс) | ✅ | Applied | Pure CSS variables and Tailwind CDN |
| 6 | `KNOWLEDGE.md` §1 (P3) D6 (Dark Cyberpunk UI) | ✅ | Applied | Dark cyberpunk theme aesthetic maintained across 4 palettes |
| 7 | `KNOWLEDGE.md` §1 (P3) D8 (Декомпозиция шаблонов) | ✅ | Applied | Clean edits across decomposed Jinja2 component files |
| 8 | `KNOWLEDGE.md` §1 (P3) D11 (Эргономика IDE) | ✅ | Applied | High-contrast Clean mode and eye-strain reduction |
| 9 | `KNOWLEDGE.md` §4 (P7) F7 (Нативная изоляция Zero-Build) | ✅ | Applied | Zero-build development environment intact |
| 10 | `KNOWLEDGE.md` §4 (P7) F9 (Педагогический стандарт UX) | ✅ | Applied | Workspace controls and header ergonomics preserved |

### Material handover at this return

- **Producer unit**: `antigravity:thread:local:d6d0abd2-257b-428e-8e1e-390307d02fbd` (Executor)
- **Source / epoch**: TS approval `cac5396`
- **Inspected scope**: `app/static/css/style.css`, `app/templates/components/`, `app/templates/exam.html`, `app/static/js/app.js`, `tests/`
- **Material or justified-none**: Material. Onboarding complete with no blockers.
- **Uncertainty**: None.
- **Continuation**: Immediate continuation to Step 2 (Implement and prove).

---

*ONB — OOP_20261030-021700_THEME / Phase B: Template and Script Migration to Semantic Theme Tokens | 2026-10-30*
