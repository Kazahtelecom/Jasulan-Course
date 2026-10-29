# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__phase-a__core_design_system_svg_logo_and_settings_panel.md](../RF__phase-a__core_design_system_svg_logo_and_settings_panel.md)
> TS: [TS__phase-a__core_design_system_svg_logo_and_settings_panel.md](../TS__phase-a__core_design_system_svg_logo_and_settings_panel.md)

## Understanding

Phase A establishes the core design system for Web-OOP: 4 distinct neon palettes (`cyber-gold` default, `electric-cyan`, `matrix-emerald`, `synthwave-purple`) via CSS custom properties in `app/static/css/style.css`, a Clean / Cyberpunk glow switch disabling diffuse glows and radial backgrounds, an adaptive inline SVG isometric cube logo with floating `{ }` brackets in `app/templates/components/header.html`, a theme settings modal with visual swatches in `header.html`, an early synchronous `<head>` script in `index.html` and `exam.html` for zero-FOUC loading from `localStorage`, client-side state handling in `app/static/js/app.js`, and test verification in `tests/test_theme_system.py`.

## Accepted Claims and Boundaries

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C0a | TRACE | Result identity: baseline `91921d22dfbf9a87cc18a0ae194b435b713bcb69` to Candidate `5855e38a94e3293f65efc0ad3bc3a32861c83439` | Untracked foreign diffs, unreviewed commits | Git repository tree and commit ancestry | Git / Windows | Git commit log and diff | `git rev-parse 5855e38a94e3293f65efc0ad3bc3a32861c83439` | yes |
| C0b | VALUE | Authority & Security: owner-direct approval, Zero-Build runtime preserved, safe localStorage handling | Unauthorized scope drift, broken runtime | Python / FastAPI / Jinja2 / Tailwind CDN | Local Zero-Build | Frozen HL §7, TS §3 | `HL-OOP_20261030-021700_THEME.md`, `status.md` | yes |
| C1 | VALUE | AC-1: 4 neon color palettes declared in `style.css` via semantic CSS variables | Incomplete theming, missing tokens, broken styling | `app/static/css/style.css`, all pages | Browser CSS parsing | TS AC-1 | `app/static/css/style.css@5855e38`, `EV §E1` | yes |
| C2 | VALUE | AC-2: Clean / Cyberpunk glow mode toggle rules in `style.css` | Distracting glow in exam mode or broken Clean view | `app/static/css/style.css`, `.cyber-card`, `body` | Browser CSS parsing | TS AC-2 | `app/static/css/style.css@5855e38`, `EV §E2` | yes |
| C3 | VALUE | AC-3: Scalable isometric SVG cube logo with `{ }` in `header.html` | Visual degradation, unscaled raster, broken branding | `app/templates/components/header.html` | SVG renderer in browser | TS AC-3 | `app/templates/components/header.html@5855e38`, `EV §E3` | yes |
| C4 | VALUE | AC-4: Theme settings button and modal dialog in `header.html` | Inaccessible theme selection, layout distortion | `app/templates/components/header.html` | Jinja2 templates, DOM | TS AC-4 | `app/templates/components/header.html@5855e38`, `EV §E4` | yes |
| C5 | VALUE | AC-5: Zero-FOUC synchronous script in `<head>` of `index.html` and `exam.html` | Flash of unstyled content on reload or navigation | `app/templates/index.html`, `app/templates/exam.html` | Client `<head>` parser | TS AC-5, HL DoF-1 | `app/templates/index.html@5855e38`, `app/templates/exam.html@5855e38`, `EV §E5` | yes |
| C6 | VALUE | AC-6: Theme controller in `app.js` with persistence to `localStorage` | Settings lost across reloads, JS errors | `app/static/js/app.js` | Browser JS runtime | TS AC-6 | `app/static/js/app.js@5855e38`, `EV §E6` | yes |
| C7 | ASSURANCE | AC-7: Automated test suite pass (67/67 green, no regressions) | Broken platform features, uncaught regressions | `tests/` test suite | Python 3.12 / pytest | TS AC-7, HL DoD-8 | `tests/test_theme_system.py@5855e38`, `EV §E7` | yes |
| C8 | TRACE | Value accounting: 5 VALUE files, 405 LOC within single-phase budget ceiling | Uncontrolled scope bloat | Changed files diff | Git diff | TS §4 prospective contract | `RF §1` accounting | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1 (4 neon palettes) | §3 AC-1, §1 Actual Accounting | C1 | ✅ |
| AC-2 (Clean / Cyberpunk toggle) | §3 AC-2, §1 Actual Accounting | C2 | ✅ |
| AC-3 (Isometric SVG cube logo) | §3 AC-3, §1 Actual Accounting | C3 | ✅ |
| AC-4 (Settings modal in header) | §3 AC-4, §1 Actual Accounting | C4 | ✅ |
| AC-5 (Zero-FOUC script in head) | §3 AC-5, §1 Actual Accounting | C5 | ✅ |
| AC-6 (Theme controller in app.js) | §3 AC-6, §1 Actual Accounting | C6 | ✅ |
| AC-7 (Regression verification) | §3 AC-7, §4 Verification | C7 | ✅ |
| TS §4 Accounting (5 VALUE files) | §1 Actual Value-Bearing Accounting | C0a, C8 | ✅ |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C0a, C8 | Re-run exact git diff and numstat commands against baseline `91921d22dfbf9a87cc18a0ae194b435b713bcb69` and Candidate `5855e38a94e3293f65efc0ad3bc3a32861c83439` | Confirm exact identity, file set, LOC accounting, and absence of foreign files | None |
| C0b | Verify status.md, journal entries, and Zero-Build conformance (absence of npm/node_modules) | Mandatory safety, authority, and architecture check | None |
| C1, C2 | Inspect `app/static/css/style.css` for all token declarations, fallback values, and glow mode rules | Core design system tokens must match exact specification | None |
| C3, C4 | Inspect `app/templates/components/header.html` for SVG structure, paths, attributes, modal markup, and accessibility | Visual branding and UI controls integrity | None |
| C5 | Inspect `<head>` of `app/templates/index.html` and `app/templates/exam.html` for inline script position and fallback logic | Mandatory anti-FOUC check | None |
| C6 | Inspect `app/static/js/app.js` for theme management methods, event listeners, escape handlers, and localStorage keys | Interactive behavior verification | None |
| C7 | Execute `pytest -q` on full test suite and inspect `tests/test_theme_system.py` | Independent empirical verification of all 67 tests | None |

## Deviations from TS

No deviations. The implemented scope matches the approved TS §2 and §5 criteria.

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
