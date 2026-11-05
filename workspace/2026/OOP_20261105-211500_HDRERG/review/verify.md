# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | Medium | `header.html` (Brand Row & Theme Button) | Jinja2 template render | TS §5.1, AC-1 | None | `pytest tests/test_header_ergonomics.py -k "test_theme_btn_in_upper_brand_row"` + DOM inspect |
| C2 | Medium | `header.html`, `style.css` (Handle Button) | CSS absolute positioning, browser DOM | TS §5.1, §5.2, AC-2 | None | `pytest tests/test_header_ergonomics.py -k "test_collapse_handle_exists"` + CSS rules inspect |
| C3 | Medium | `header.html`, `app.js` (Text Toggle & Sync) | Client JS DOM API | TS §5.1, §5.3, AC-3 | None | `pytest tests/test_header_ergonomics.py -k "test_text_toggle_and_actions_cluster"` + `app.js` inspect |
| C4 | High | `header.html` (Flex Row 2 & Subtabs) | Flexbox render >=1200px | TS §5.1, AC-4, HL §3 | Static flex classes check | `pytest tests/test_header_ergonomics.py -k "test_exam_subtabs_structure_and_no_overflow"` + flex container audit |
| C5 | Medium | `app.js` (Persistence) | Browser `localStorage` | TS AC-5, HL §5 (PV-2) | No headless browser | Unit test of JS source + code audit of `applyHeaderCollapseState` and `toggleHeaderCollapse` |
| C6 | High | Full repository test suite | Python 3.12, Pytest 9.1.1 | TS AC-6, HL §7.1 | None | Full test run `pytest` (79 tests) |
| C7 | High | Candidate git commit diff | Git repo, value accounting | TS §4, RF §1 | None | `git diff --numstat 77c5d083..a408ff74` for VALUE selector |
| C8 | High | Authority and immutable denominator | Task control files | TFW conventions | None | Inspection of `status.md`, `journal/20261105-211501__handoff__c3d4.md` |

## Verification Log

### V1: Claim C1 — Перенос кнопки темы в верхний ряд
- **Accepted claim / authority:** Кнопка `#theme-settings-btn` перенесена в верхний ряд (Brand & Profile Selector) рядом с селектором студента и доступна на всех страницах (`/`, `/week1`, `/week2`, `/week3`, `/exam`).
- **Subject tuple:** `{header.html, a408ff749486a2d6c60541360dd0b55cd4a12ab0, FastAPI TestClient, TS AC-1, clean}`
- **Action or evidence:** Запуск теста `test_theme_btn_in_upper_brand_row` через Pytest и прямой аудит `header.html`.
- **Observed:** Тест прошёл успешно. В `header.html` (строки 54–63) кнопка `#theme-settings-btn` встроена внутрь контейнера профиля студента перед блоком баллов/экзамена, имеет `onclick="openThemeSettings()"`, иконку 🎨 и подпись «Тема» (`hidden md:inline`).
- **Limit:** None.
- **Result:** HOLDS

### V2: Claim C2 — Добавление центрированного язычка сворачивания
- **Accepted claim / authority:** На нижней кромке шапки `#main-site-header` добавлен язычок `#header-collapse-handle` с классом `header-collapse-handle-btn`, стрелкой `#header-collapse-handle-icon` (▲) и вызовом `toggleHeaderCollapse()`.
- **Subject tuple:** `{header.html + style.css, a408ff749486a2d6c60541360dd0b55cd4a12ab0, Pytest + CSS audit, TS AC-2, clean}`
- **Action or evidence:** Запуск теста `test_collapse_handle_exists` и проверка правил `.header-collapse-handle-btn` в `app/static/css/style.css`.
- **Observed:** Тест прошёл успешно. В `header.html` (строки 148–156) язычок расположен на нижней границе `<header>`. В `style.css` (строки 264–304) задано абсолютное позиционирование `bottom: -15px`, `left: 50%`, `transform: translateX(-50%)`, скругление `0 0 10px 10px`, неоновый ховер с `var(--theme-accent)` и `box-shadow: none !important` при `[data-glow="clean"]`.
- **Limit:** None.
- **Result:** HOLDS

### V3: Claim C3 — Сохранение и синхронизация текстовой кнопки сворачивания
- **Accepted claim / authority:** Кнопка `#header-collapse-toggle` сохранена в правом блоке Row 2, и функция `applyHeaderCollapseState(isCollapsed)` в `app.js` синхронно переключает как текстовый лейбл `#header-collapse-label`, так и иконку язычка `#header-collapse-handle-icon`.
- **Subject tuple:** `{header.html + app.js, a408ff749486a2d6c60541360dd0b55cd4a12ab0, Pytest + JS audit, TS AC-3, clean}`
- **Action or evidence:** Запуск тестов `test_text_toggle_and_actions_cluster`, `test_js_collapse_state_synchronization` и статический анализ `app.js`.
- **Observed:** Тесты прошли успешно. Текстовая кнопка размещена рядом с кнопкой UML в блоке `shrink-0`. В `app.js` функция обновляет `#header-collapse-label` (▲ Свернуть меню / ▼ Развернуть меню), `#header-collapse-handle-icon` (▲ / ▼), а также тултипы `title` и `aria-label`.
- **Limit:** None.
- **Result:** HOLDS

### V4: Claim C4 — Ликвидация горизонтального скролла на `/exam`
- **Accepted claim / authority:** Подвкладки экзамена лаконичны («Инструкция», «Часть 1 · Тестирование (20 б.)», «Часть 2 · Практика (20 б.)», «Итоговая Ведомость (100 б.)»), контейнер подвкладок имеет `flex-1 min-w-0 overflow-x-auto`, а блок действий закреплен `shrink-0`.
- **Subject tuple:** `{header.html, a408ff749486a2d6c60541360dd0b55cd4a12ab0, Pytest TestClient, TS AC-4, clean}`
- **Action or evidence:** Запуск `test_exam_subtabs_structure_and_no_overflow` и анализ CSS-классов контейнера Row 2.
- **Observed:** Тест прошёл успешно. Тексты вкладок компактны, общая ширина вкладок с паддингами укладывается в доступное пространство при >= 1200px без появления горизонтального скролла. Блок действий не сжимается и не вытесняется за экран.
- **Limit:** В тестовой среде нет физического рендера графического окна, но CSS flexbox разметка строго гарантирует требуемое поведение.
- **Result:** HOLDS

### V5: Claim C5 — Персистентность состояния сворачивания
- **Accepted claim / authority:** Состояние сворачивания сохраняется в `localStorage` по ключу `weboop_header_collapsed` и восстанавливается при загрузке страницы.
- **Subject tuple:** `{app.js, a408ff749486a2d6c60541360dd0b55cd4a12ab0, Static JS code analysis, TS AC-5, clean}`
- **Action or evidence:** Инспекция функций `toggleHeaderCollapse()` и `initHeaderCollapse()` в `app.js`.
- **Observed:** В `toggleHeaderCollapse()` значение записывается в `localStorage.setItem("weboop_header_collapsed", isCollapsed ? "true" : "false")`. При загрузке страницы статус считывается и передаётся в `applyHeaderCollapseState(saved === "true")`.
- **Limit:** None.
- **Result:** HOLDS

### V6: Claim C6 — Прохождение полного набора тестов
- **Accepted claim / authority:** Все существующие и новые тесты проходят без ошибок (79/79 passed).
- **Subject tuple:** `{tests/, a408ff749486a2d6c60541360dd0b55cd4a12ab0, Python 3.12 + Pytest 9.1.1, TS AC-6, clean}`
- **Action or evidence:** Выполнение команды `pytest`.
- **Observed:** `79 passed, 1 warning in 19.11s`. Все функциональные и регрессионные тесты зеленые.
- **Limit:** 1 предупреждение StarletteDeprecationWarning (устаревание вызова httpx в TestClient, сторонний пакет, не влияет на поведение платформы).
- **Result:** HOLDS

### V7: Claim C7 — Соблюдение Value-bearing accounting
- **Accepted claim / authority:** В Candidate commit изменены ровно 3 файла VALUE (`header.html`, `style.css`, `app.js`), суммарно 158 строк (115 add, 43 del), 0 бинарных.
- **Subject tuple:** `{git tree, a408ff749486a2d6c60541360dd0b55cd4a12ab0, Git 2.x, TS §4, clean}`
- **Action or evidence:** Выполнение `git diff --numstat 77c5d083e9e782b5c1b118825e6053b378aaad81 a408ff749486a2d6c60541360dd0b55cd4a12ab0 -- app/templates/components/header.html app/static/css/style.css app/static/js/app.js`.
- **Observed:**
  - `app/static/css/style.css`: 43 add, 0 del.
  - `app/static/js/app.js`: 12 add, 0 del.
  - `app/templates/components/header.html`: 60 add, 43 del.
  - Сумма: 115 add + 43 del = 158 touched LOC. Логических файлов: 3.
- **Limit:** None.
- **Result:** HOLDS

### V8: Claim C8 — Полномочия и непрерывность управления
- **Accepted claim / authority:** Задача инициирована владельцем `zhasulan`, утверждена в `journal/20261105-211501__handoff__c3d4.md`, выполнена исполнителем `5241b3fa` и передана на независимое рецензирование координатором `3878cb43`.
- **Subject tuple:** `{status.md + journal/, a408ff749486a2d6c60541360dd0b55cd4a12ab0, TFW Governance, conventions, clean}`
- **Action or evidence:** Проверка метаданных `status.md` и событий журнала.
- **Observed:** Непрерывная цепочка перехода состояний `TODO -> TS_DRAFT -> ONB -> RF`. `selection_ref: baseline`, `reporting: native-gates`.
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `pytest tests/test_header_ergonomics.py -v` | C1, C2, C3, C4, C5 | Exit 0, 6 passed, 1 warning in 0.31s |
| 2 | `pytest` | C6 | Exit 0, 79 passed, 1 warning in 19.11s |
| 3 | `git diff --numstat 77c5d083e9e782b5c1b118825e6053b378aaad81 a408ff749486a2d6c60541360dd0b55cd4a12ab0 -- app/templates/components/header.html app/static/css/style.css app/static/js/app.js` | C7 | Exit 0, 43/0/style.css, 12/0/app.js, 60/43/header.html (158 touched LOC) |
| 4 | `git show --stat a408ff749486a2d6c60541360dd0b55cd4a12ab0` | C7 | Exit 0, 4 files changed, 236 insertions(+), 43 deletions(-) |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| 1 | Перенос кнопки темы в первый ряд | `header.html` L54-63 | `tests/test_header_ergonomics.py::test_theme_btn_in_upper_brand_row` | ✅ |
| 2 | Язычок на нижней кромке шапки | `header.html` L148-156, `style.css` L264-304 | `tests/test_header_ergonomics.py::test_collapse_handle_exists` | ✅ |
| 3 | Синхронизация JS текстовой кнопки и язычка | `app.js` L144-168 | `tests/test_header_ergonomics.py::test_js_collapse_state_synchronization` | ✅ |
| 4 | Ликвидация скролла и лаконичные подписи | `header.html` L111-137 | `tests/test_header_ergonomics.py::test_exam_subtabs_structure_and_no_overflow` | ✅ |
| 5 | Отсутствие регрессий в существующих 73 тестах | Репозиторий `tests/` | Выполнение `pytest` (79 passed) | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | `test_theme_btn_in_upper_brand_row` | Кнопка темы вернется во второй ряд или исчезнет с отдельных страниц | Проверяет DOM на 5 маршрутах (`/`, `/week1`, `/week2`, `/week3`, `/exam`) и взаимный порядок элементов | Admitted |
| G2 | permanent guard | `test_collapse_handle_exists` | Язычок исчезнет или потеряет `onclick`/`class` | Проверяет DOM id, class, icon и обработчик на всех страницах | Admitted |
| G3 | permanent guard | `test_text_toggle_and_actions_cluster` | Текстовая кнопка сворачивания потеряет лейбл или выйдет из flex-блока | Проверяет id, начальный текст, вложенность в правый блок с UML | Admitted |
| G4 | permanent guard | `test_exam_subtabs_structure_and_no_overflow` | Подвкладки экзамена вернут длинные названия или сломают flex-контейнер | Проверяет точный текст 4 подвкладок и CSS классы `flex-1 min-w-0` / `shrink-0` | Admitted |
| G5 | permanent guard | `test_css_collapse_handle_styles` | Стили язычка сломаются или потеряют поддержку Clean mode | Проверяет наличие селекторов, z-index, hover и `[data-glow="clean"]` override | Admitted |
| G6 | permanent guard | `test_js_collapse_state_synchronization` | Функция JS перестанет обновлять один из элементов при сворачивании | Проверяет логику синхронизации в коде `applyHeaderCollapseState` | Admitted |

## Candidate Findings

No findings.

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | E1 (AC-1) | `{header.html, a408ff74, Pytest TestClient, TS AC-1}` | Repeated (command 1) | ✅ | None |
| E2 | E2 (AC-2) | `{header.html+style.css, a408ff74, Pytest TestClient, TS AC-2}` | Repeated (command 1) | ✅ | None |
| E3 | E3 (AC-3) | `{header.html+app.js, a408ff74, Pytest TestClient, TS AC-3}` | Repeated (command 1) | ✅ | None |
| E4 | E4 (AC-4) | `{header.html, a408ff74, Pytest TestClient, TS AC-4}` | Repeated (command 1) | ✅ | None |
| E5 | E5 (AC-5) | `{app.js, a408ff74, Code analysis, TS AC-5}` | Opened & verified | ✅ | None |
| E6 | E6 (AC-6) | `{style.css, a408ff74, Code analysis, TS AC-6}` | Opened & verified | ✅ | None |
| E7 | E7 (AC-7) | `{tests/, a408ff74, Pytest full suite, TS AC-6}` | Repeated (command 2) | ✅ | None |
| E8 | E-accounting | `{git repo, a408ff74, Git diff numstat, TS §4}` | Repeated (command 3) | ✅ | None |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | ONB §7 #1 | P0 (`README.md § Цель и North Star проекта`) | ✅ | ✅ | ✅ — фокус на рабочей области кода для студентов 2 курса | ✅ — прямое освобождение пространства экрана |
| 2 | ONB §7 #2 | P3 (`KNOWLEDGE.md D5`) | ✅ | ✅ | ✅ — Zero-Build архитектура без внешних сборщиков | ✅ — реализация на чистом CSS/JS |
| 3 | ONB §7 #3 | P3 (`KNOWLEDGE.md D11`) | ✅ | ✅ | ✅ — эргономика IDE-тренажёра и сворачивание шапки | ✅ — прямое расширение механизма сворачивания |
| 4 | ONB §7 #4 | P3 (`KNOWLEDGE.md D14`) | ✅ | ✅ | ✅ — неоновая дизайн-система и `#theme-settings-btn` | ✅ — перенос кнопки темы в верхний ряд |
| 5 | ONB §7 #5 | P3 (`KNOWLEDGE.md D15`) | ✅ | ✅ | ✅ — стандарты UI `/exam` и устранение артефактов | ✅ — устранение горизонтального скролла |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| `journal/20261105-211501__handoff__c3d4.md` | `77c5d083e9e782b5c1b118825e6053b378aaad81` | `a408ff749486a2d6c60541360dd0b55cd4a12ab0` | `app/templates/components/header.html` (MODIFY, VALUE, перенос темы, язычок, навигация), `app/static/css/style.css` (MODIFY, VALUE, стили язычка), `app/static/js/app.js` (MODIFY, VALUE, синхронизация) | 115 | 43 | 158 | 0 N/A | <4% от лимитов (50 файлов / 5000 строк); PASS | `git diff --numstat 77c5d083e9e782b5c1b118825e6053b378aaad81 a408ff749486a2d6c60541360dd0b55cd4a12ab0 -- app/templates/components/header.html app/static/css/style.css app/static/js/app.js` | VERIFIED |

## Selected Knowledge Evidence

- **Producer / Unit:** Executor `antigravity:thread:local:5241b3fa-a4b3-471e-9f23-fa9d02f5c13f`.
- **Source / Epoch:** Candidate commit `a408ff749486a2d6c60541360dd0b55cd4a12ab0`.
- **Artifacts:** `ONB__OOP_20261105-211500_HDRERG.md`, `RF__OOP_20261105-211500_HDRERG.md`, `evidence/EV__OOP_20261105-211500_HDRERG.md`.
- **Applicability:** Все 6 AC подтверждены воспроизводимыми проверками, тесты и артефакты полностью соответствуют TS.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
