# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | High (целостность учебного контента) | `app/content/week_3/`, `app/static/images/` | Python 3.12, локальный веб-сервер | TS §5 AC-1, инспекция файлов | None | Независимая инспекция `app/content/week_3/` и бинарных ассетов в `app/static/images/`, запуск тестов `tests/test_week3.py` |
| C2 | High (маршрутизация и изоляция БД) | `app/modules/registry.py`, `app/services/scoring.py`, `app/routers/week3.py`, `data/web_oop.db` | FastAPI, SQLite WAL | TS §5 AC-2, `tests/test_week3.py`, `tests/test_week_modules.py` | None | Инспекция регистрации в `week_registry` и `WEEK_TASK_IDS[3]`, проверка изоляции прогресса 4 студентов через `pytest tests/test_week_modules.py tests/test_week3.py` |
| C3 | Medium (UI эргономика и векторный UML) | `app/templates/components/`, `app/static/js/app.js` | Jinja2, HTML5/SVG, JS | TS §5 AC-3, `tests/test_uml_viewer.py`, `tests/test_ui_ergonomics.py` | None | Проверка HTML-шаблонов, локального блока `<defs>` в `#svg-week3`, прогон `tests/test_uml_viewer.py` |
| C4, C7 | Critical (Sandbox Security & AST Whitelist) | `app/content/week_3/practice.py`, `app/services/ast_validator.py`, `app/services/runner.py` | Python 3.12 subprocess, pytest | TS §4 HC-1, TS §5 AC-4, `tests/test_ast_validator.py`, `tests/test_sandbox_security.py` | None | Прогон эталонных решений в песочнице, проверка `git diff c0a83bd4 997dfa4 -- app/services/ast_validator.py` (пуст), запуск тестов безопасности |
| C5 | High (Антиугадывательный баланс квиза и регрессии) | `app/content/week_3/quiz.py`, `docs/`, полный набор тестов | pytest 9.1.1 | TS §4 HC-2, TS §5 AC-5, `tests/test_ui_ergonomics.py` | None | Независимый математический расчет длин всех 40 вариантов ответа квиза, полный прогон `pytest -v` (55/55 passed), инспекция `docs/` |
| C6, C8 | High (Учет скоупа, неизменяемый знаменатель, Candidate identity) | Git commits `c0a83bd4`, `997dfa4`, `status.md`, `journal/` | Git revision graph | TS §4 Accounting Contract, conventions.md §6 | None | Запуск NUL-safe diff между Baseline и Candidate по 19 путям `$valuePaths`, проверка неизменности селектора и удержания в лимите 2× эскалации |

## Verification Log

### V1: Claim C1 — Полнота контента Недели 3 и Cyberpunk-иллюстраций
- **Accepted claim / authority:** Пакет `app/content/week_3/` экспортирует `WEEK3_OVERVIEW`, `THEORY_SECTIONS` (4 шага по Лекциям 6–9 с анатомическими карточками), `WALKTHROUGH_EXAMPLE` (разбор `TicketIssuer` и `TransitTerminalFacade`), `PRACTICE_TASKS` (3 задачи тренажера), `QUIZ_QUESTIONS` (10 вопросов) и `evaluate_quiz`. 3 Cyberpunk-иллюстрации присутствуют в `app/static/images/` и имеют ненулевой размер.
- **Subject tuple:** `app/content/week_3/` + `app/static/images/` @ `997dfa43b2a6a9292a3528866230005d06e97e28`, Windows 11 / Python 3.12.9, TS §5 AC-1, clean workdir.
- **Action or evidence:** Проверены файлы в `app/content/week_3/`, подтверждены размеры изображений: `week3_hero.jpg` (147,525 Б), `gof_patterns.jpg` (140,683 Б), `clean_arch_layers.jpg` (138,763 Б). Запущен `pytest tests/test_week3.py -k "page or theory" -v`.
- **Observed:** Все 4 файла контента и 3 иллюстрации валидны, структура данных полностью соответствует спецификации.
- **Limit:** None.
- **Result:** HOLDS

### V2: Claim C2 — Регистрация в ядре, роутер `/week3`, изоляция 4 студентов
- **Accepted claim / authority:** Модуль Недели 3 зарегистрирован в `week_registry` (`app/modules/registry.py`), `WEEK_TASK_IDS[3] = ("w3_task_1", "w3_task_2", "w3_task_3")` в `app/services/scoring.py`, роутер `week3.py` подключен в `main.py`, прогресс 4 студентов изолирован в SQLite WAL.
- **Subject tuple:** `app/modules/registry.py`, `app/services/scoring.py`, `app/routers/week3.py`, `app/main.py` @ `997dfa43b2a6a9292a3528866230005d06e97e28`, FastAPI / SQLite, TS §5 AC-2, DB test fixtures.
- **Action or evidence:** Запущен `pytest tests/test_week3.py tests/test_week_modules.py -v`.
- **Observed:** 9 тестов пройдены успешно (`test_week_registry_registered_modules`, `test_student_profiles_isolation`, `test_theory_completion_recording`, `test_read_only_progress_does_not_mutate_db`, `test_week3_*`). Прогресс студентов (`zhasulan`, `roman`, `arseniy`, `saubakirov`) изолирован, HWM сохраняется.
- **Limit:** None.
- **Result:** HOLDS

### V3: Claim C3 — UI-шаблоны и SVG UML-диаграмма с лупой 2.5×
- **Accepted claim / authority:** Ссылка в `header.html` активна (`/week3`), в `tab_theory.html` и `tab_practice.html` добавлены контекстные блоки Недели 3, `#svg-week3` в `uml_viewer.html` содержит локальный самодостаточный блок `<defs>` (`shadow-box-w3`, `arrow-dep-w3`, `arrow-impl-w3`), диаграмма открывается по умолчанию на `/week3` и поддерживает лупу 2.5×.
- **Subject tuple:** `app/templates/components/`, `app/static/js/app.js` @ `997dfa43b2a6a9292a3528866230005d06e97e28`, Jinja2 / Browser DOM, TS §5 AC-3 / HC-3, static HTML parser.
- **Action or evidence:** Запущен `pytest tests/test_uml_viewer.py tests/test_ui_ergonomics.py -v`.
- **Observed:** Все 10 тестов пройдены (`test_uml_viewer_rendered_on_all_weeks`, `test_uml_svgs_have_self_contained_defs`, `test_week3_diagram_classes_and_clean_arch`, `test_collapsible_header`, `test_practice_fullscreen_and_splitter`, `test_editor_line_numbers_and_fontsize`). Диаграмма содержит все ключевые сущности Недели 3 (`TransitTerminalFacade`, `ShiftReportBuilder`, `ValidationHandler`, `TransitTelemetrySubject`, `ValidateRideUseCase`, `CardRepositoryPort`, `PaymentGatewayPort`, `BankApiAdapter`, `TransitCard`, `Money`).
- **Limit:** None.
- **Result:** HOLDS

### V4: Claims C4, C7 — Песочница RunnerService, задачи тренажера и безопасность AST
- **Accepted claim / authority:** Эталонные решения `w3_task_1..3` успешно выполняются в песочнице со статусом `PASSED` за время < 5.0 с, тренажер имеет вес `0.0` б., файл `app/services/ast_validator.py` неизменен (`git diff` пуст), в коде отсутствуют опасные вызовы и неразрешенные импорты.
- **Subject tuple:** `app/content/week_3/practice.py`, `app/services/ast_validator.py`, `app/services/runner.py` @ `997dfa43b2a6a9292a3528866230005d06e97e28`, Python 3.12 subprocess, TS §4 HC-1 / TS §5 AC-4 / HL §6 DoF #2 / HL §7 P4, isolated sandbox.
- **Action or evidence:** Выполнен `git diff c0a83bd4 997dfa4 -- app/services/ast_validator.py` (вывод пуст). Запущен `pytest tests/test_runner.py tests/test_sandbox_security.py tests/test_week3.py -k "practice or runner or sandbox" -v`.
- **Observed:** Все 18 тестов песочницы и безопасности пройдены успешно. Эталонные решения `w3_task_1..3` проходят валидацию AST и выполняются за 1.14–1.17 с (норма < 5.0 с).
- **Limit:** None.
- **Result:** HOLDS

### V5: Claim C5 — Математический баланс квиза, полный прогон pytest и документация
- **Accepted claim / authority:** Вопросы `w3_q1..w3_q10` удовлетворяют ограничениям `min_len >= 60`, `max_len / min_len <= 1.65`, распределению правильных ответов по 2–3 на индекс `0..3`, не менее 5 из 10 правильных ответов не строго самые длинные; полный прогон `pytest -v` дает 100% (55/55); документация актуализирована.
- **Subject tuple:** `app/content/week_3/quiz.py`, `docs/`, `tests/` @ `997dfa43b2a6a9292a3528866230005d06e97e28`, Python 3.12.9 / pytest 9.1.1, TS §4 HC-2 / TS §5 AC-5 / HL §5 DoD #4, complete repo.
- **Action or evidence:** Выполнен независимый скрипт расчета длин и пропорций вариантов ответа; запущен `pytest -v` по всему репозиторию; проверены диффы в `docs/domain_model_uml.md` (+142 LOC) и `docs/architecture.md` (+5 / -4 LOC).
- **Observed:** Длины вариантов ответа лежат в диапазоне 89–106 символов (все >= 60); макс. отношение `max_len / min_len = 1.0674` (строго <= 1.65); распределение правильных индексов: `{2: 3, 0: 2, 1: 3, 3: 2}` (все по 2–3 раза); не строго самые длинные ответы: 6 из 10 (>= 5/10). Полный прогон `pytest -v` дал 55 пройденных тестов из 55 (0 failed) за 28.90 с.
- **Limit:** None.
- **Result:** HOLDS

### V6: Claims C6, C8 — Бухгалтерский учет скоупа и Candidate identity
- **Accepted claim / authority:** Изменения `VALUE` охватывают ровно утвержденные 19 логических файлов (16 текстовых + 3 бинарных `.jpg`), число затронутых строк `VALUE` (2588 LOC) не превышает лимит эскалации 2× (4360 LOC), Baseline SHA `c0a83bd4`, Candidate SHA `997dfa4`, однофазная реализация без декомпозиции.
- **Subject tuple:** Git repository @ `c0a83bd4` .. `997dfa4`, Git / PowerShell, TS §4 Prospective accounting contract.
- **Action or evidence:** Выполнены команды `git diff --name-status` и `git diff --numstat` с селектором `$valuePaths` между коммитами `c0a83bd4` и `997dfa4`.
- **Observed:** Ровно 19 логических файлов (8 CREATE, 11 MODIFY). Добавлено 2568 LOC, удалено 20 LOC, суммарно затронуто 2588 текстовых строк LOC (включая предшествующий дифф `uml_viewer.html` по правилу приоритета §6). 3 бинарных `.jpg` файла = `N/A`. Объем 2588 LOC укладывается в утвержденный предел эскалации 4360 LOC. Candidate `997dfa4` предшествует созданию артефактов EV/RF.
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `git diff --name-status c0a83bd4 997dfa4 -- $valuePaths` | C6 | Exit 0: 8 A, 11 M = 19 logical VALUE files |
| 2 | `git diff --numstat c0a83bd4 997dfa4 -- $valuePaths` | C6 | Exit 0: 2568 additions, 20 deletions = 2588 touched text LOC; 3 binary files |
| 3 | `git diff c0a83bd4 997dfa4 -- app/services/ast_validator.py` | C4, C7 | Exit 0: empty output (whitelist unchanged) |
| 4 | `pytest -v` | C1..C5, C7 | Exit 0: 55 passed, 1 warning in 28.90s |
| 5 | `Get-Item app/static/images/{week3_hero,gof_patterns,clean_arch_layers}.jpg` | C1 | Exit 0: 3 valid JPG files (147 KB, 140 KB, 138 KB) |
| 6 | Независимый скрипт расчета баланса `QUIZ_QUESTIONS` | C5 | Exit 0: max ratio 1.0674 <= 1.65, min len 89 >= 60, dist {0:2, 1:3, 2:3, 3:2}, 6/10 not longest |
| 7 | Поиск служебных/запрещенных слов в диффе `VALUE` | C6, C7 | Exit 0: нет `TODO`, `FIXME` или временных пометок; вхождения относятся к доменному `LegacyBankClient` |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | 4 шага лекционной теории и разбор кода | `app/content/week_3/theory.py` | Лекции 6–9 и Лабораторные 6–9 в `research/iter1/RES.md` | ✅ |
| C2 | Конфигурация задач C3 (Builder+Adapter, Chain+Observer, UseCase) | `app/content/week_3/practice.py` | `TS §6 Technical Guidance`, `3_extract.md E2` | ✅ |
| C3 | Автономность `<defs>` в `#svg-week3` | `app/templates/components/uml_viewer.html` | `tests/test_uml_viewer.py::test_uml_svgs_have_self_contained_defs` | ✅ |
| C4 | Неизменность синтаксического белого списка AST | `app/services/ast_validator.py` | `git diff c0a83bd4 997dfa4 -- app/services/ast_validator.py` (пуст) | ✅ |
| C5 | Математический баланс вариантов ответа квиза `<= 1.65` | `app/content/week_3/quiz.py` | `tests/test_ui_ergonomics.py::test_quiz_balance_and_traps` | ✅ |
| C6 | 19 логических файлов `VALUE` и 2588 LOC | Git commit `997dfa4` | `git diff --numstat c0a83bd4 997dfa4 -- $valuePaths` | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | `tests/test_uml_viewer.py::test_uml_svgs_have_self_contained_defs` | Пропадание стрелок и фильтров в SVG при переключении вкладок | Релевантный негативный контроль: любая ссылка `url(#id)` вне локального `<defs>` проваливает тест | admitted |
| G2 | permanent guard | `tests/test_ui_ergonomics.py::test_quiz_balance_and_traps` | Угадывание студентами ответов по длине варианта | Релевантный негативный контроль: превышение отношения длин > 1.65 или длины < 60 символов валит тест | admitted |
| G3 | permanent guard | `tests/test_sandbox_security.py::test_all_reference_solutions_pass_ast_whitelist` | Падение студенческого эталонного кода в песочнице | Контрфактический контроль: запрещенный импорт (`time`, `re`) или dunder-атрибут блокируются AST | admitted |
| G4 | permanent guard | `tests/test_week_modules.py::test_student_profiles_isolation` | Перезапись прогресса между 4 студентами в SQLite WAL | Контрфактический контроль: мутация прогресса под одним `X-Student-Id` не затрагивает другие профили | admitted |
| G5 | governance assertion | NUL-safe diff и сверка 19 файлов `$valuePaths` | Выход за рамки скоупа TS / неавторизованные мутации | Сверка хэшей коммитов Baseline и Candidate по селектору | governance only |

## Candidate Findings

No findings. (Все обязательные рубежи безопасности, контрактные требования TS, инварианты эргономики и баланса квиза строго выполняются; дефектов не обнаружено).

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | E1 in `EV__OOP_20261026-021211_W3GOF.md` | `app/content/week_3/` + images @ `997dfa4`, Python 3.12 | ✅ Repeated | ✅ Establishes C1 | None |
| E2 | E2 in `EV__OOP_20261026-021211_W3GOF.md` | `WeekRegistry`, `scoring.py`, `week3.py` @ `997dfa4`, FastAPI/SQLite | ✅ Repeated | ✅ Establishes C2 | None |
| E3 | E3 in `EV__OOP_20261026-021211_W3GOF.md` | `uml_viewer.html`, `app.js`, templates @ `997dfa4`, Jinja2/DOM | ✅ Repeated | ✅ Establishes C3 | None |
| E4 | E4 in `EV__OOP_20261026-021211_W3GOF.md` | `practice.py`, `ast_validator.py`, `runner.py` @ `997dfa4`, Python 3.12 | ✅ Repeated | ✅ Establishes C4, C7 | None |
| E5 | E5 in `EV__OOP_20261026-021211_W3GOF.md` | `quiz.py`, `docs/`, `tests/` @ `997dfa4`, pytest 9.1.1 | ✅ Repeated | ✅ Establishes C5 | None |
| E6 | E-accounting in `EV__OOP_20261026-021211_W3GOF.md` | 19 `$valuePaths` @ `c0a83bd4..997dfa4`, Git revision graph | ✅ Repeated | ✅ Establishes C6, C8 | None |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 | PV Priority 0: `README.md § Цель и North Star проекта` (Неделя 3: паттерны GoF и основы чистой архитектуры) | ✅ | ✅ | ✅ Завершение 3-недельного курса на домене Avtobys | ✅ Прямое назначение задачи |
| 2 | HL §7.2 #2 | PV Priority 1: `.tfw/README.md` (`#ns2`, `#methodology-values`, `#success-criteria`) | ✅ | ✅ | ✅ Отсутствие плейсхолдеров, проверка автотестами | ✅ Методологический стандарт качества |
| 3 | HL §7.2 #3 | PV Priority 2: `knowledge/philosophy.md` | ✅ (N/A) | ❌ | ✅ Файл отсутствует; отражено в `README.md` / `KNOWLEDGE.md` | ✅ Допустимое N/A |
| 4 | HL §7.2 #4 | PV Priority 3: `KNOWLEDGE.md` (`D2`, `D6`, `D7`, `D8`, `D9`, `D10`, `D11`) | ✅ | ✅ | ✅ Архитектура `WeekModule`, изоляция 4 студентов, баланс квиза, белый список AST | ✅ Архитектурный каркас |
| 5 | HL §7.2 #5 | PV Priority 4: `.tfw/conventions.md` (`§3`, `§6`, `§7`, `§11`, `§12`, `§14`, `§15`) | ✅ | ✅ | ✅ Role Lock, учет бюджета, отсутствие мусора в репозитории | ✅ Контрактные правила исполнения |
| 6 | HL §7.2 #6 | PV Priorities 5–6: `knowledge/convention.md` & `knowledge/process.md` | ✅ (N/A) | ❌ | ✅ Файлы отсутствуют; консолидированы в `KNOWLEDGE.md` | ✅ Допустимое N/A |
| 7 | HL §7.2 #7 | PV Priority 7: `KNOWLEDGE.md §4` (`F5`, `F7`, `F9`, технические записи REC) | ✅ | ✅ | ✅ Сквозной домен Avtobys, 0.0 б. за тренажер, 20.0 б. за квиз, нативная песочница | ✅ Доменные и педагогические требования |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| Owner `zhasulan` via `c0a83bd4f1f915427ccc243d64065008d9eb1169` | `c0a83bd4f1f915427ccc243d64065008d9eb1169` | `997dfa43b2a6a9292a3528866230005d06e97e28` | Ровно 19 логических файлов `VALUE` (8 CREATE, 11 MODIFY: пакет `app/content/week_3/`, роутер `week3.py`, регистрация в `registry.py` и `scoring.py`, шаблоны `header`, `tab_theory`, `tab_practice`, `uml_viewer`, `app.js`, доки `domain_model_uml.md`, `architecture.md`, 3 JPG-картинки) | 2568 | 20 | 2588 | 3 JPG (N/A) | Однофазная реализация (2588 LOC <= 4360 LOC 2× лимита) | `git diff --numstat c0a83bd4f1f915427ccc243d64065008d9eb1169 997dfa43b2a6a9292a3528866230005d06e97e28 -- $valuePaths` | VERIFIED |

## Selected Knowledge Evidence

- **Baseline commit / epoch:** `c0a83bd4f1f915427ccc243d64065008d9eb1169` (Owner approval of TS and value denominator).
- **Candidate commit / epoch:** `997dfa43b2a6a9292a3528866230005d06e97e28` (Executor implementation).
- **Inspected Scope:** 19 логических файлов `VALUE`, 4 файла `ASSURANCE` (`tests/`), артефакты `EV__OOP_20261026-021211_W3GOF.md` и `RF__OOP_20261026-021211_W3GOF.md`.
- **Authority / Lineage:** Мандат выдан владельцем `zhasulan` в `HL-OOP_20261026-021211_W3GOF.md @ e31342f7`, исполнение зафиксировано в `RF` исполнителя `antigravity:thread:local:a0ce43a2-c346-486b-8642-9ebabb0eb398`.
- **Applicability:** Все доказательства применимы непосредственно к Candidate revision `997dfa43b2a6a9292a3528866230005d06e97e28`.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
