# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | High (UI navigation & Zero-Build visual contract) | `app/routers/week2.py`, `app/routers/week1.py`, `app/main.py`, `app/templates/index.html`, `app/static/images/{week2_hero,solid_modular,di_ports}.jpg` | Local Python 3.12.9 / FastAPI `TestClient` | `TS §5 AC-1`, `HL §5 DoD-1`, `HL §6 DoF-4` | none | Прямая инспекция шаблона `index.html`, роутеров `week1.py` / `week2.py`, проверка размеров и SHA-256 3 бинарных `.jpg` файлов и перезапуск `pytest tests/test_week2.py -k "test_week2_page"`. |
| C2 | High (Pedagogical integrity & source attribution) | `app/content/week_2/theory.py`, `app/content/week_2/__init__.py` | Local Python 3.12.9 | `TS §5 AC-2`, `HL §5 DoD-2`, `HL §7 P1, P4` | none | Полное чтение `app/content/week_2/theory.py` (355 строк), сверка 4 шагов `THEORY_SECTIONS` (`w2_step_1_srp`..`w2_step_4_dip_di`) и 4 шагов `WALKTHROUGH_EXAMPLE` (`TerminalValidator`), проверка SHA-256 исходных PDF Лекций 4–5 и Лабораторных 4–5 и запуск `test_week2_theory_and_walkthrough`. |
| C3 | Critical (Ungraded trainer & 1-click reference solution floor) | `app/content/week_2/practice.py`, `app/routers/week2.py`, `app/services/scoring.py`, `app/services/runner.py`, `app/static/js/app.js` | Local Python 3.12.9 / `RunnerService` (subprocess pytest) + SQLite | `TS §5 AC-3`, `HL §5 DoD-3`, `HL §6 DoF-2` | none | Полное чтение `app/content/week_2/practice.py` (272 строки) и `app/static/js/app.js`, негативный контроль (`starter_code` падает в `RunnerService`) и позитивный прогон `reference_solution` для `w2_task_1..3` с проверкой `total_score == 0.0` и `tasks_completed == 3`. |
| C4 | Critical (20.0-point quiz grading, High-Water Mark & Week 1 / Week 2 isolation) | `app/content/week_2/quiz.py`, `app/services/scoring.py`, `app/routers/week2.py`, `app/routers/week1.py` | Local Python 3.12.9 / SQLAlchemy 2.0 + SQLite | `TS §5 AC-4`, `HL §2.2`, `HL §5 DoD-4`, `HL §6 DoF-1, DoF-3`, `TS §4 M1–M6` | none | Пословная сверка всех 10 вопросов `QUIZ_QUESTIONS` (`w2_q1..w2_q10`) с утвержденным банком `HL §2.2`, аудит логики `ScoringService` (`WEEK_TASK_IDS`, `week_number: int = 1`) и прогон `test_week2_quiz_grading_hwm_and_week1_independence`. |
| C5, C6 | Mandatory Floor (Safety/Security, Regression & Guard Quality) | `app/`, `tests/` (`test_health.py`, `test_models.py`, `test_runner.py`, `test_week1.py`, `test_week2.py`) | Local Python 3.12.9 / pytest 9.1.1 + ruff | `HL §6 DoF-1`, `KNOWLEDGE.md D3, F4`, `.tfw/workflows/review.md §Step 2` | none | Полный прогон всех 24 автотестов репозитория (`pytest -v`), проверка линтером (`ruff check .`), аудит комментариев и канальных слов в `VALUE` diff. |
| C7 | Mandatory Floor (Accepted-Result Identity, Exact-Path Staging, Prospective Accounting & Economics) | Git range `42ab6ed77da69a08f17a4796701fd32064043b01..619bbc4caa5565f6d922f1dff57e7b6b7d27a575`, `HL §7.2`, `ONB §7`, `economics/roles/*.jsonl` | Local Git & Python 3.12.9 | `.tfw/workflows/review.md §Step 2`, `.tfw/conventions.md`, `.tfw/economics/README.md`, `TS §4` | none | Независимый перезапуск NUL-safe `git diff --name-status` и `git diff --numstat`, проверка `git log --stat`, аудит всех ссылок `HL §7.2` / `ONB §7` по `Project Values (PV)` (P0–P7) и валидация JSONL экономики (`tfw_economics.py validate`). |

Safety/security, human acceptance authority and accepted-result identity are mandatory floors.
Expand verification when an observed fact changes a mapped claim, dependency, risk or evidence gap;
the existence or count of discrepancies never selects depth by itself.

## Verification Log

### V1: C1 — Навигация Недели 2 (`/week2`), переключатель недель, 5 вкладок Dark Cyberpunk UI и 3 локальные иллюстрации без `mermaid.min.js`
- **Accepted claim / authority:** `GET /week2` возвращает HTTP 200, рендерит переключатель `/week1` («Неделя 1 · Инкапсуляция») и `/week2` («Неделя 2 · SOLID и DI») с `data-active-week="2"`, 5 вкладок (`Главная`, `Теория`, `Практика`, `Тестирование`, `Результаты`), кнопку «✨ Вставить готовое решение», 3 локальные иллюстрации (`week2_hero.jpg`, `solid_modular.jpg`, `di_ports.jpg` `> 10 KB`) и не содержит `mermaid.min.js` (`TS §5 AC-1`, `HL §5 DoD-1`, `HL §6 DoF-4`).
- **Subject tuple:** `{app/routers/week2.py, app/routers/week1.py, app/main.py, app/templates/index.html, app/static/images/*.jpg} @ Candidate 120f4bab124360860918d45e683b0f3f92b7bf16`, Windows 11 / Python 3.12.9 / FastAPI `TestClient`, `TS §5 AC-1`.
- **Action or evidence:** Прочитаны `app/routers/week2.py`, `app/routers/week1.py`, `app/main.py`, `app/templates/index.html`; проверены размеры и SHA-256 3 изображений в `app/static/images/`; выполнен прогон `tests/test_week2.py::test_week2_page_and_navigation_layout`.
- **Observed:** `GET /week2` возвращает HTTP 200; в `index.html` (строка 12) установлено `<body data-active-week="{{ active_week|default(1) }}">`, в строках 53–58 рендерятся ссылки `<a href="/week1">` и `<a href="/week2">` с активным классом `week-pill-active`; присутствуют все 5 секций (`panel-home`, `panel-theory`, `panel-practice`, `panel-quiz`, `panel-results`) и кнопка `fillSolutionCode` («✨ Вставить готовое решение»); подстрока `mermaid.min.js` отсутствует (сохранен только HTML-комментарий Zero-Build для совместимости с `test_index_dashboard`). Размеры и SHA-256 иллюстраций: `week2_hero.jpg` = `782 231 B` (`b4f3691f...`), `solid_modular.jpg` = `734 340 B` (`46912eb5...`), `di_ports.jpg` = `784 562 B` (`2997f5d7...`), все отдают HTTP 200.
- **Limit:** none
- **Result:** HOLDS

### V2: C2 — 4 последовательных шага Теории SOLID & DI и 4-шаговый разбор `WALKTHROUGH_EXAMPLE`
- **Accepted claim / authority:** `THEORY_SECTIONS` в `app/content/week_2/theory.py` содержит 4 шага (`w2_step_1_srp`, `w2_step_2_ocp`, `w2_step_3_lsp_isp`, `w2_step_4_dip_di`) с примерами `bad_code` и `good_code`, карточками `anatomy_cards` и явным указанием источников Лекций 4–5 и Лабораторных 4–5 (а также пометкой ориентировочного времени `Ориентир: 60 + 60 + 60 мин`), а `WALKTHROUGH_EXAMPLE` содержит 4-шаговый разбор `TerminalValidator` с внедрением зависимостей через `__init__` (`TS §5 AC-2`, `HL §7 P1, P4`).
- **Subject tuple:** `app/content/week_2/theory.py @ Candidate 120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9, `TS §5 AC-2` & `HL §2.1`.
- **Action or evidence:** Прочитан `app/content/week_2/theory.py` целиком (строки 1–355); проверены SHA-256 4 исходных PDF в `C:\Users\kz444\OneDrive\Desktop\OOP`; выполнен тест `tests/test_week2.py::test_week2_theory_and_walkthrough`.
- **Observed:** `WEEK2_OVERVIEW` указывает `week_number: 2`, `max_score: 20.0`, `pass_threshold: 12.0`, `estimated_time: "Ориентир: 60 + 60 + 60 мин"` и ссылку на Лекции 4–5 и Лабораторные 4–5. Все 4 шага `THEORY_SECTIONS` (`w2_step_1_srp`, `w2_step_2_ocp`, `w2_step_3_lsp_isp`, `w2_step_4_dip_di`) содержат бытовые аналогии, `anatomy_cards`, блоки `bad_code` / `good_code` и `takeaway`. `WALKTHROUGH_EXAMPLE` разбирает `StandardFareService` (`100 ₸`), `StudentFareService` (`50 ₸`), `CardPayment`, `BluetoothPayment` и `TerminalValidator.__init__(self, fare_service, payment_method)` в 4 шагах. SHA-256 всех 4 PDF-первоисточников (`RF__lecture_04.pdf`, `RF__lecture_05.pdf`, `RF__lab_04.pdf`, `RF__lab_05.pdf`) побайтово совпадают с `HL §2.1`.
- **Limit:** none
- **Result:** HOLDS

### V3: C3 — Свободный Тренажер Практики (`w2_task_1..3`) без снятия баллов и с кнопкой готового решения
- **Accepted claim / authority:** `PRACTICE_TASKS` в `app/content/week_2/practice.py` содержит 3 связанные задачи (`w2_task_1`: `StandardFareService` 100 / `StudentFareService` 50; `w2_task_2`: `CardPayment` / `BluetoothPayment`; `w2_task_3`: `TerminalValidator` с Constructor DI), каждая имеет `max_score == 0.0`, `starter_code` (падает до решения) и `reference_solution` (проходит через `POST /api/week2/practice/{task_id}/run` со статусом `PASSED`, отмечая `tasks_completed == 3` и сохраняя `total_score == 0.0`) (`TS §5 AC-3`, `HL §5 DoD-3`, `HL §6 DoF-2`).
- **Subject tuple:** `{app/content/week_2/practice.py, app/routers/week2.py, app/services/scoring.py, app/static/js/app.js} @ Candidate 120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9 / `RunnerService` + SQLite, `TS §5 AC-3`.
- **Action or evidence:** Прочитаны `app/content/week_2/practice.py` и `app/static/js/app.js`; выполнен тест `tests/test_week2.py::test_week2_practice_trainer_and_zero_score`.
- **Observed:** Для всех 3 задач (`w2_task_1`, `w2_task_2`, `w2_task_3`) `starter_code` содержит `pass` и возвращает `passed: False` при запуске в `RunnerService`; `reference_solution` проходит все `pytest`-проверки в песочнице со статусом `PASSED` (`passed: True`). После прохождения всех 3 задач `GET /api/week2/progress` возвращает `tasks_completed: 3`, `total_score: 0.0`, `is_completed: False`. В `app/static/js/app.js` `fillSolutionCode(taskId)` подставляет `dataset.solution` и сохраняет черновик с изолированным префиксом `weboop_w${ACTIVE_WEEK}_draft_${taskId}`.
- **Limit:** none
- **Result:** HOLDS

### V4: C4 — Финальное Тестирование Недели 2 (`10 × 2.0 = 20.0` б.), High-Water Mark и полная изоляция от Недели 1
- **Accepted claim / authority:** `QUIZ_QUESTIONS` в `app/content/week_2/quiz.py` содержит 10 утвержденных вопросов (`w2_q1..w2_q10`) из `HL §2.2` по `2.0` балла (`20.0` макс., порог зачета $\ge 12.0$), `ScoringService` защищает лучший балл по правилу High-Water Mark и хранит прогресс Недели 2 (`week_2*`) независимо от Недели 1 (`week_1*`) (`TS §5 AC-4`, `HL §2.2`, `HL §6 DoF-1, DoF-3`, `TS §4 M1–M6`).
- **Subject tuple:** `{app/content/week_2/quiz.py, app/services/scoring.py, app/routers/week2.py, app/routers/week1.py} @ Candidate 120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9 / SQLite, `TS §5 AC-4`.
- **Action or evidence:** Выполнена пословная сверка `app/content/week_2/quiz.py` с `HL §2.2`; проверена реализация `ScoringService` (`app/services/scoring.py`); выполнен тест `tests/test_week2.py::test_week2_quiz_grading_hwm_and_week1_independence`.
- **Observed:** Все 10 вопросов (`w2_q1..w2_q10`), варианты ответов и правильные индексы (`correct_index == 1` во всех 10 вопросах, соответствующие варианту `b)` в `HL §2.2`) полностью совпадают с замороженным `HL §2.2`. При 5/10 верных ответах начисляется `10.0` б. (`is_completed: False`, `50%`); при 6/10 — `12.0` б. (`is_completed: True`, `60%`); при повторной отправке 2/10 (`4.0` б.) сохраняется `total_score: 12.0` (High-Water Mark); при 10/10 — `20.0` б. (`100%`). При этом `/api/week1/progress` остается `0.0` б., а отправка квиза Недели 1 на `14.0` б. не затрагивает `20.0` б. Недели 2.
- **Limit:** none
- **Result:** HOLDS

### V5: C5, C6 — Safety/Security, Baseline Regression & Guard Admission
- **Accepted claim / authority:** Отсутствие регрессий в Неделе 1 и ядре платформы (`tests/test_health.py`, `tests/test_models.py`, `tests/test_runner.py`, `tests/test_week1.py`), сохранность AST-песочницы `RunnerService`, чистота `ruff check .` и соблюдение правил комментариев в `VALUE` diff.
- **Subject tuple:** `Repository @ HEAD 619bbc4caa5565f6d922f1dff57e7b6b7d27a575 (Candidate 120f4bab124360860918d45e683b0f3f92b7bf16)`, Python 3.12.9 / pytest 9.1.1 / ruff.
- **Action or evidence:** Запущены `python -m pytest -v`, `python -m ruff check .` и скрипт проверки канальных слов (`todo`, `legacy`, `old`, `temp`) в добавленных строках `VALUE` diff.
- **Observed:** `24 passed in 16.30s` (все 20 существующих тестов и 4 новых теста Недели 2 зеленые); `ruff check .` -> `All checks passed!`; запрещенных канальных слов (`todo`, `legacy`, `old`, `temp`) в добавленном `VALUE` коде обнаружено `0` (`[]`). Все комментарии и docstrings в `app/content/week_2/*`, `app/routers/week2.py`, `app/services/scoring.py`, `app/static/js/app.js` и `app/templates/index.html` несут прямую читательскую или учебную ценность.
- **Limit:** none
- **Result:** HOLDS

### V6: C7 — Accepted-Result Identity, Exact-Path Staging, Prospective Accounting & Economics Verification
- **Accepted claim / authority:** Candidate `120f4bab124360860918d45e683b0f3f92b7bf16` зафиксирован до `EV`/`RF` с соблюдением `Exact-path staging`; пересчет по `TS §4` (`app/`) дает 13 логических файлов (`10` текстовых + `3` бинарных `.jpg`) и `1107 + 72 = 1179` затронутых текстовых LOC (`WITHIN_BUDGET` относительно `13 файлов / 1600 LOC` из `TS @ 8782364c17f85ef19425121fb9f4ae0d7bdc3eb3`); JSONL файлы экономики проходят валидацию.
- **Subject tuple:** `Git history 42ab6ed77da69a08f17a4796701fd32064043b01..619bbc4caa5565f6d922f1dff57e7b6b7d27a575`, Python 3.12.9, `TS §4` & `.tfw/economics/README.md`.
- **Action or evidence:** Выполнен аудит `git log --stat`, перезапущены NUL-safe команды `git diff --name-status` и `git diff --numstat`, выполнен `python .tfw/economics/tfw_economics.py validate` для обоих файлов в `economics/roles/`.
- **Observed:** Все коммиты Исполнителя (`91daf8f4`, `a6d77b1a`, `120f4bab`, `619bbc4c`) содержат только целевые пути своих стадий без посторонних файлов. Candidate `120f4bab124360860918d45e683b0f3f92b7bf16` содержит ровно 13 `VALUE` файлов в `app/` и 1 `ASSURANCE` файл `tests/test_week2.py`. Валидатор экономики подтвердил корректность обоих файлов: `5c4f8547...jsonl` (Coordinator interim, 2 rows) и `f8b4ec75...jsonl` (Executor complete, 2 rows).
- **Limit:** none
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `python -m pytest -v` | C1, C2, C3, C4, C5, C6 | Exit `0`: `24 passed, 1 warning in 16.30s` (`test_health.py` 4/4, `test_models.py` 4/4, `test_runner.py` 7/7, `test_week1.py` 5/5, `test_week2.py` 4/4). |
| 2 | `python -m ruff check .` | C5 | Exit `0`: `All checks passed!`. |
| 3 | `git log --stat 42ab6ed77da69a08f17a4796701fd32064043b01..HEAD` | C7 | Exit `0`: Проверена линейная история коммитов от заморозки `HL` (`42ab6ed7`), утверждения `TS` (`8782364c`), записи `ONB` (`91daf8f4`, `a6d77b1a`), реализации Candidate (`120f4bab`) до записи `EV`/`RF` (`619bbc4c`). |
| 4 | `git diff --name-status --find-renames=50% -z 42ab6ed77da69a08f17a4796701fd32064043b01 120f4bab124360860918d45e683b0f3f92b7bf16 -- app/` & `--numstat` | C7 | Exit `0`: Ровно 13 файлов (`8 A`, `5 M`), `1107` добавлений + `72` удаления = `1179` затронутых текстовых LOC + 3 бинарных `.jpg` (`- / -` `N/A`). |
| 5 | `python .tfw/economics/tfw_economics.py validate workspace/2026/OOP_20261018-222800_W2SOL/economics/roles/*.jsonl` | C7 | Exit `0`: Оба JSONL файла (`5c4f8547...` и `f8b4ec75...`) валидны по схеме v1. |
| 6 | Скрипт проверки SHA-256 PDF и `.jpg` + проверка канальных слов (`todo`, `legacy`, `old`, `temp`) в `VALUE` diff | C1, C2, C5 | Exit `0`: Все 4 PDF-хеша совпадают с `HL §2.1`; 3 `.jpg` файла > 730 КБ; канальных слов в добавленном `VALUE` коде `0`. |

## Claim and Source Checks

1. Spot-check key claims or sources by material reliance, not convenience.
2. Confirm every citation resolves to a real, relevant artifact.
3. Verify data claims against a primary source where reachable.

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | SHA-256 хеши 4 исходных PDF (`RF__lecture_04.pdf`, `RF__lecture_05.pdf`, `RF__lab_04.pdf`, `RF__lab_05.pdf`) | `HL §2.1` | Файлы в `C:\Users\kz444\OneDrive\Desktop\OOP\01_Лекции\` и `02_Лабораторные\` | ✅ (`a5d93e29...`, `2cb6f657...`, `5145063b...`, `f524c894...` совпадают побайтово) |
| C2 | Размеры 3 иллюстраций Недели 2 (`week2_hero.jpg` = 782 231 B, `solid_modular.jpg` = 734 340 B, `di_ports.jpg` = 784 562 B, сумма 2 301 133 B) | `RF §1`, `EV E1` | `app/static/images/{week2_hero,solid_modular,di_ports}.jpg` | ✅ (782 231 + 734 340 + 784 562 = 2 301 133 B) |
| C3 | 10 вопросов квиза Недели 2 (`w2_q1..w2_q10`) по 2.0 балла = 20.0 баллов, порог зачета 12.0 баллов | `RF §1`, `RF §3 AC-4`, `app/content/week_2/quiz.py` | Замороженный банк вопросов в `HL-OOP_20261018-222800_W2SOL.md §2.2` | ✅ (100% совпадение формулировок, вариантов и правильных ответов) |
| C4 | Accounting: `1107 + 72 = 1179` touched text LOC across 13 `VALUE` files under `app/` | `RF §1`, `EV E-accounting` | `git diff --numstat --find-renames=50% -z 42ab6ed7... 120f4bab... -- app/` | ✅ (`16 + 271 + 241 + 354 + 3 + 1 + 134 + 67 + 19 + 73 = 1179`) |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | `test_week2_page_and_navigation_layout` (`tests/test_week2.py`): рендеринг `/week2`, переключатель `/week1` и `/week2`, 5 панелей вкладок, кнопка `Вставить готовое решение`, отдача 3 `.jpg` (`> 10 KB`) и отсутствие `mermaid.min.js`. | Поломка маршрута `/week2`, исчезновение переключателя недель, битые иллюстрации или возврат мелких Mermaid-схем (`HL §6 DoF-4`). | Прямая проверка наличия/отсутствия DOM-маркеров и HTTP 200 / размера байтов каждого `.jpg`. | admitted |
| G2 | permanent guard | `test_week2_theory_and_walkthrough` (`tests/test_week2.py`): полнота 4 шагов теории (`w2_step_1_srp`..`w2_step_4_dip_di`) с непустыми `bad_code`/`good_code` и 4-шагового разбора `WALKTHROUGH_EXAMPLE` (`TerminalValidator`). | Пропуск шага теории или потеря примеров кода `Плохо / Хорошо`. | Проверка точного списка ID и непустоты полей каждого шага. | admitted |
| G3 | permanent guard | `test_week2_practice_trainer_and_zero_score` (`tests/test_week2.py`): негативный контроль `starter_code` (`passed: False`), прохождение `reference_solution` всех 3 задач (`w2_task_1..3`) в `RunnerService` (`PASSED`) и инвариант `total_score == 0.0` при `tasks_completed == 3`. | Ложноположительное прохождение пустого шаблона, поломка эталонного решения или начисление/требование баллов за тренажер (`HL §6 DoF-2`). | Встроенный негативный контроль: `RunnerService.run_code(starter_code)` обязан вернуть `passed is False`, а `reference_solution` — `passed is True` с `total_score == 0.0`. | admitted |
| G4 | permanent guard | `test_week2_quiz_grading_hwm_and_week1_independence` (`tests/test_week2.py`): шкала `10 × 2.0 = 20.0` б., порог зачета (`10.0 -> False`, `12.0 -> True`), защита High-Water Mark (`4.0` после `12.0` сохраняет `12.0`) и двусторонняя изоляция прогресса Недели 1 и Недели 2 в SQLite. | Неверный расчет баллов, потеря зачета при повторной попытке или перезапись баллов Недели 1 баллами Недели 2 (`HL §6 DoF-1, DoF-3`, `TS §4 M1–M6`). | Последовательная отправка граничных комбинаций (`5/10`, `6/10`, `2/10`, `10/10`) и перекрестная проверка `/api/week1/progress` и `/api/week2/progress`. | admitted |

## Candidate Findings

No findings.

## Evidence Verification

`evidence/` holds only EV files; no verdict rests on working material.

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | `E1` (AC-1) | `GET /week2` & `/static/images/{week2_hero,solid_modular,di_ports}.jpg` @ `120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9 `TestClient` | ✅ Repeated | ✅ | none |
| E2 | `E2` (AC-2) | `app/content/week_2/theory.py` (`THEORY_SECTIONS`, `WALKTHROUGH_EXAMPLE`) @ `120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9 | ✅ Repeated | ✅ | none |
| E3 | `E3` (AC-3) | `POST /api/week2/practice/{w2_task_1..3}/run` & `GET /api/week2/progress` @ `120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9 + `RunnerService` + SQLite | ✅ Repeated | ✅ | none |
| E4 | `E4` (AC-4) | `POST /api/week2/quiz/check` & `GET /api/week1/progress` @ `120f4bab124360860918d45e683b0f3f92b7bf16`, Python 3.12.9 + SQLite (`24 passed`, `ruff` clean) | ✅ Repeated | ✅ | none |
| E5 | `E-accounting` (TS §4) | `git diff --name-status` & `--numstat -z 42ab6ed7... 120f4bab... -- app/` | ✅ Repeated | ✅ | none |

## Knowledge Citations Verified

Scan PV priorities 0–4 in full and 5–7 by relevance. Verify every HL §7.2 and ONB §7 citation for
resolution, item existence, semantic match, currentness and relevance. Check priority 0 purpose and
priority 1 methodology separately even when one file contains both.

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #P0 / ONB §7 #1 | **P0:** [README.md](../../../../README.md) `§ Цель и North Star проекта` | ✅ | ✅ | ✅ — Определяет программу Недели 2 («Принципы проектирования SOLID, связанность и зацепление Cohesion & Coupling, Dependency Injection») на базе сквозного домена Avtobys. | ✅ — Прямо задает тематическое ядро модуля Недели 2. |
| 2 | HL §7.2 #P1 / ONB §7 #2 | **P1:** [.tfw/README.md](../../../../.tfw/README.md) `Methodology values` and `Success Criteria` | ✅ | ✅ | ✅ — Требует проверяемых приемочных критериев, отсутствия заглушек (`free of placeholders`), честных доказательств и трассируемости решений (проверено отдельно от P0). | ✅ — Обеспечивает полноту контента Недели 2 и доказательной базы `EV`. |
| 3 | HL §7.2 #P2 / ONB §7 #3 | **P2:** `knowledge/philosophy.md` (отсутствует в репозитории) | ✅ (отсутствие подтверждено) | N/A | ✅ — Честно задокументировано отсутствие файла; принципы зафиксированы в `HL §7` (`P1–P4`). | ✅ — Исключает выдумывание несуществующих ссылок. |
| 4 | HL §7.2 #P3 / ONB §7 #4 | **P3:** [KNOWLEDGE.md](../../../../KNOWLEDGE.md) `§1 Architecture Decisions (D1–D6)` & [REC-OOP_20261018-213107_W1MAT-tech-week1-funnel.md](../../../../knowledge/records/REC-OOP_20261018-213107_W1MAT-tech-week1-funnel.md) | ✅ | ✅ | ✅ — Закрепляет стек FastAPI + SQLite + Jinja2 (`D1`), домен Avtobys (`D2`), AST-песочницу `RunnerService` (`D3`), хранение UML в `docs/` (`D4`), Zero-Build UI (`D5`) и пятисекционный паттерн с 20-балльным квизом и High-Water Mark (`D6`). | ✅ — Архитектура Недели 2 напрямую переиспользует этот фундамент без дублирования шаблонов. |
| 5 | HL §7.2 #P4 / ONB §7 #5 | **P4:** [.tfw/conventions.md](../../../../.tfw/conventions.md) `HL (High Level)`, `Design Rules`, `Anti-patterns (prohibited)`, `Exact-path staging`, `Closed message catalogue` | ✅ | ✅ | ✅ — Управляет разделением ролей, бюджетами `VALUE`, `Exact-path staging` и закрытым каталогом сообщений. | ✅ — Соблюдено при планировании, исполнении и ревью. |
| 6 | HL §7.2 #P5–P6 / ONB §7 #6 | **P5–P6:** `knowledge/convention.md`, `knowledge/process.md` (отсутствуют в репозитории) | ✅ (отсутствие подтверждено) | N/A | ✅ — Честно отмечено отсутствие файлов; применяются правила `AGENTS.md` и `.tfw/conventions.md`. | ✅ — Корректная фиксация состояния базы знаний. |
| 7 | HL §7.2 #P7 / ONB §7 #7 | **P7:** [KNOWLEDGE.md](../../../../KNOWLEDGE.md) `§4 Project Facts (F1–F5)` & [REC-OOP_20261018-213107_W1MAT-human-beginner-format.md](../../../../knowledge/records/REC-OOP_20261018-213107_W1MAT-human-beginner-format.md) | ✅ | ✅ | ✅ — Закрепляет утвержденный владельцем формат для группы с новичками (`F5`): простая пошаговая теория, тренажер без снятия баллов с кнопкой готового решения и 20-балльный квиз из 10 вопросов в конце воронки. | ✅ — Полностью реализовано в модуле Недели 2 (`/week2`). |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| `TS__OOP_20261018-222800_W2SOL.md @ 8782364c17f85ef19425121fb9f4ae0d7bdc3eb3` (immutable pre-work denominator: `13` VALUE files, `1600` touched text LOC; `owner_escalation_multiplier: 2`) | `42ab6ed77da69a08f17a4796701fd32064043b01` | `120f4bab124360860918d45e683b0f3f92b7bf16` | 13 `VALUE` files under `app/`: `app/content/week_2/__init__.py` (`A`, `16+0=16`), `app/content/week_2/practice.py` (`A`, `271+0=271`), `app/content/week_2/quiz.py` (`A`, `241+0=241`), `app/content/week_2/theory.py` (`A`, `354+0=354`), `app/main.py` (`M`, `2+1=3`), `app/routers/week1.py` (`M`, `1+0=1`), `app/routers/week2.py` (`A`, `134+0=134`), `app/services/scoring.py` (`M`, `42+25=67`), `app/static/images/di_ports.jpg` (`A`, binary `N/A`), `app/static/images/solid_modular.jpg` (`A`, binary `N/A`), `app/static/images/week2_hero.jpg` (`A`, binary `N/A`), `app/static/js/app.js` (`M`, `10+9=19`), `app/templates/index.html` (`M`, `36+37=73`) | 1107 | 72 | 1179 | 3 `.jpg` files (`N/A` LOC, 2 301 133 B total) | `WITHIN_BUDGET` (`13` files < `50` trigger, `1.00x` of `13`; `1179` LOC < `5000` trigger, `0.74x` of `1600`, well below `2.0x` escalation) | `git diff --name-status --find-renames=50% -z 42ab6ed77da69a08f17a4796701fd32064043b01 120f4bab124360860918d45e683b0f3f92b7bf16 -- app/` & `git diff --numstat --find-renames=50% -z 42ab6ed77da69a08f17a4796701fd32064043b01 120f4bab124360860918d45e683b0f3f92b7bf16 -- app/` | VERIFIED |

## Selected Knowledge Evidence

- **Квалифицированные записи базы знаний (`KNOWLEDGE.md` & `knowledge/records/`):** Проверены обе действующие записи предшествующей задачи `OOP_20261018-213107_W1MAT` — [REC-OOP_20261018-213107_W1MAT-tech-week1-funnel.md](../../../../knowledge/records/REC-OOP_20261018-213107_W1MAT-tech-week1-funnel.md) (`disposition: accepted`, техническое решение пятисекционной воронки Dark Cyberpunk, `ScoringService` с 20-балльным квизом и `RunnerService` без снятия баллов) и [REC-OOP_20261018-213107_W1MAT-human-beginner-format.md](../../../../knowledge/records/REC-OOP_20261018-213107_W1MAT-human-beginner-format.md) (`disposition: accepted`, человеческое знание о формате обучения для группы с новичками). Конфликтующих или отменяющих записей в `knowledge/records/` нет.
- **Передача знаний от ролей текущей задачи (`HL §11`, `ONB`, `RF`):**
  - В `HL-OOP_20261018-222800_W2SOL.md §11` (`Producer: Coordinator 1da46223...`, `Source: owner:zhasulan & референсный HL WEEK2`) зафиксирован `Strategic Insight S1` о сквозном учебном кейсе Недели 2 (`StudentFareService` 100/50 ₸ + `BluetoothPayment` + `TerminalValidator` с DI через `__init__`).
  - В `ONB__OOP_20261018-222800_W2SOL.md` и `RF__OOP_20261018-222800_W2SOL.md` (`Producer: Executor 5aed77d4...` по диспатчу `20261018-230410__role_dispatched__Executor__9d31.md`) зафиксировано `Material or justified-none: justified-none` для новых человеческих `Fact Candidates` во время исполнения, при этом в `RF §2` задокументировано техническое решение по мульти-недельной параметризации `ScoringService` (`week_number`, `WEEK_TASK_IDS`) и `index.html` / `app.js` (`data-active-week`), подлежащее отражению Координатором на этапе `KNW` (`/tfw-docs` / `/tfw-knowledge`).

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
