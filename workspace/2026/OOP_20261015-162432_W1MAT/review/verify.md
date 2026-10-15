# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | Medium / High | Структура лекции, нарратив Chaos → Structure, Rich vs Anemic, Mermaid UML диаграммы | Modern Browser, Python 3.12 | Pytest content assertions, проверка структуры шаблона | Mermaid CDN требует доступа к сети для визуализации | Запуск `pytest tests/test_week1_content.py -k test_lecture_content_structure`, инспекция текста и шаблона |
| C2 | Medium / High | Банк из 5 вопросов квиза, серверная проверка ответов, начисление до 3.0 баллов | FastAPI TestClient, SQLite | HTTP 200 JSON contract, формула баллов 3.0 max | Нет | Запуск `pytest tests/test_week1_content.py -k test_quiz` и `tests/test_week1_routes.py -k test_quiz_endpoint` |
| C3 | High / Critical | Стартовый шаблон `TransitCard`, сьют из 7 тестов инвариантов, начисление до 7.0 баллов через RunnerService | Subprocess Python 3.12, tempdir, pytest | Pytest exit codes, runner output | Временные файлы удаляются после прогона | Запуск `pytest tests/test_week1_content.py -k test_practice` и `tests/test_week1_routes.py -k test_practice_run` |
| C4 | High / Critical | Спецификация и автотесты `SingleTripTicket` и `Bus`, проверка `@property is_validated` без сеттера, исключения `TicketAlreadyUsedError` и `TicketExpiredError` (до 10.0 баллов) | Subprocess Python 3.12, tempdir, pytest | Pytest exit codes, AttributeError assertion | Мокирование времени через `issued_at` | Запуск `pytest tests/test_week1_content.py -k test_lab` и `tests/test_week1_routes.py -k test_lab_run` |
| C5 | Critical / Core | Служба `scoring.py`: расчет $\text{Total} \in [0, 20]$, порог $\ge 12$ б., High-Water Mark правило $\max$, сохранение в SQLite `TopicProgress` и `Submission` | SQLite 3, SQLAlchemy 2.0 | Юнит-тесты scoring, DB query assertions | SQLite однопоточный файл | Запуск `pytest tests/test_scoring.py` (4 теста) |
| C6 | Medium / High | Zero-Build фронтенд (Tailwind CDN, Mermaid CDN, Vanilla JS), автосохранение черновиков в LocalStorage, дашборд `/`. Запрет сборщиков npm/vite | Браузер, FastAPI templates | DOM inspection, git file tree | LocalStorage изолирован origin | Запуск `pytest tests/test_week1_routes.py -k "test_week1_page_render or test_index_dashboard"`, инспекция `week1.js` и репозитория |
| C7 | Critical / Security | Безопасность RunnerService: блокировка опасных импортов/вызовов через ASTValidator (`SECURITY_VIOLATION`), принудительный таймаут 5.0с (`TIMEOUT`) | Windows 11, Subprocess Python 3.12 | AST parse tree, subprocess timeout | ASTValidator не защищает от обхода через глубокое метапрограммирование, но достаточен для курса | Запуск `pytest tests/test_runner.py` и `tests/test_week1_routes.py` (отправка опасного кода и бесконечного цикла) |
| C8 | High / Assurance | Полное тестовое покрытие: 30 тестов (15 ядра + 15 Недели 1), `ruff check .` с 0 замечаний | pytest 9.1.1, ruff 0.5.0 | Вывод консольных утилит | Нет | Запуск полного сьюта `pytest -v` и линтера `ruff check .` |
| C9 | Critical / Trace | Идентичность артефактов и value-bearing accounting: Baseline `6da8e171`, Candidate `10b8cfb5`, 13 VALUE файлов, 2578 LOC | Git repository history | Git CLI | Нет | Replay `git diff --name-status` и `git diff --numstat` против Baseline `6da8e171` и Candidate `10b8cfb5` |

## Verification Log

### V1: C1 — Теоретический модуль лекции с визуализацией Rich vs Anemic и Mermaid UML
- **Accepted claim / authority:** Страница `/week1` (вкладка `[Лекция]`) и контентный модуль `lecture.py` содержат 5 структурированных разделов и 2 Mermaid.js диаграммы (Class Diagram и Sequence Diagram).
- **Subject tuple:** `app/content/week_1/lecture.py`, `app/templates/week1.html` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, TestClient & pytest, TS §5 AC-1.
- **Action or evidence:** Инспекция `lecture.py` и запуск `pytest tests/test_week1_content.py -k test_lecture_content_structure`.
- **Observed:** PASSED (1 passed). В `LECTURE_DATA` присутствуют разделы `chaos_to_structure`, `identity_state_behavior`, `anemic_vs_rich`, `invariants_and_properties`, `domain_exceptions`, а также валидные Mermaid диаграммы классов и последовательностей.
- **Limit:** Рендеринг SVG диаграмм в браузере зависит от доступности CDN Mermaid.js.
- **Result:** HOLDS

### V2: C2 — Интерактивный квиз с мгновенной проверкой и начислением до 3.0 баллов
- **Accepted claim / authority:** Вкладка `[Квиз]` содержит 5 концептуальных вопросов с методическими пояснениями; эндпоинт `POST /api/week1/quiz/check` валидирует ответы на сервере и пропорционально начисляет до 3.0 баллов.
- **Subject tuple:** `app/content/week_1/quiz.py`, `app/routers/week1.py` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, TestClient & pytest, TS §5 AC-2.
- **Action or evidence:** Запуск `pytest tests/test_week1_content.py -k test_quiz` и `pytest tests/test_week1_routes.py -k test_quiz_endpoint`.
- **Observed:** PASSED (3 passed). Банк содержит ровно 5 вопросов, каждый вариант ответа сопровождается подробным методическим разбором; при 5/5 верных начисляется 3.0 балла, при 4/5 — 2.4 балла; ответы возвращаются с HTTP 200 JSON.
- **Limit:** Нет.
- **Result:** HOLDS

### V3: C3 — Практикум `TransitCard` с автопроверкой через RunnerService (до 7.0 баллов)
- **Accepted claim / authority:** Практикум содержит стартовый шаблон и сьют из 7 тестов инвариантов `TransitCard`; эндпоинт `POST /api/week1/practice/run` запускает изолированный `RunnerService` и начисляет до 7.0 баллов.
- **Subject tuple:** `app/content/week_1/practice.py`, `app/routers/week1.py`, `app/services/runner.py` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, pytest 9.1.1, TS §5 AC-3.
- **Action or evidence:** Запуск `pytest tests/test_week1_content.py -k test_practice` и `pytest tests/test_week1_routes.py -k test_practice_run`.
- **Observed:** PASSED (2 passed). Все 7 инвариантов (баланс $\ge 0$, пополнение $\ge 100$ ₸, расчет скидки, блокировка, нехватка средств, запрет нулевого/отрицательного тарифа) покрыты тестами; эталонное решение дает 7/7 PASSED (+7.0 баллов) в песочнице.
- **Limit:** Временные файлы песочницы удаляются сразу после завершения теста.
- **Result:** HOLDS

### V4: C4 — Лабораторная работа №1 `SingleTripTicket` и `Bus` с автопроверкой (до 10.0 баллов)
- **Accepted claim / authority:** Лабораторная работа верифицирует readonly `@property is_validated` без сеттера (попытка записи вызывает `AttributeError`), защиту от повторного проезда (`TicketAlreadyUsedError`), срок годности 60 мин (`TicketExpiredError`) и полиморфизм `Bus` с начислением до 10.0 баллов.
- **Subject tuple:** `app/content/week_1/lab.py`, `app/routers/week1.py`, `app/services/runner.py` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, pytest 9.1.1, TS §5 AC-4.
- **Action or evidence:** Запуск `pytest tests/test_week1_content.py -k test_lab` и `pytest tests/test_week1_routes.py -k test_lab_run`.
- **Observed:** PASSED (2 passed). Сьют из 10 автотестов полностью пройден эталонным решением (+10.0 баллов); инкапсуляция строго подтверждена тестом `test_ticket_encapsulation_no_setter`.
- **Limit:** Детерминированное тестирование срока билета обеспечивается передачей опционального `issued_at`.
- **Result:** HOLDS

### V5: C5 — Служба `scoring.py`, расчет 0..20 баллов, порог $\ge 12$ б., правило $\max$ и логирование в SQLite
- **Accepted claim / authority:** `ScoringService` вычисляет сумму $\text{Total} \in [0, 20]$, фиксирует `is_completed=True` при $\ge 12$ баллах, защищает от снижения баллов ($\max$) и логирует каждую посылку в таблицу `Submission`.
- **Subject tuple:** `app/services/scoring.py`, `app/models/` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, SQLite 3, TS §5 AC-5.
- **Action or evidence:** Запуск `pytest tests/test_scoring.py` (4 теста).
- **Observed:** PASSED (4 passed). Правило High-Water Mark корректно удерживает максимальный балл при падении последующих попыток; статус сдачи выставляется строго при $\ge 12.0$ баллах; записи в `Submission` персистентны.
- **Limit:** Нет.
- **Result:** HOLDS

### V6: C6 — Zero-Build фронтенд (Tailwind CDN, Mermaid CDN, Vanilla JS), LocalStorage и карточка на дашборде
- **Accepted claim / authority:** Единая страница `/week1` содержит 4 переключаемые вкладки; черновики сохраняются в `localStorage`; на главной странице `/` отображается карточка Недели 1 с прогресс-баром; в проекте отсутствуют `package.json` и `node_modules`.
- **Subject tuple:** `app/templates/week1.html`, `app/static/js/week1.js`, `app/templates/index.html` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, Browser/DOM, TS §5 AC-6.
- **Action or evidence:** Запуск `pytest tests/test_week1_routes.py -k "test_week1_page_render or test_index_dashboard"`, инспекция файлов `week1.js`, `week1.html`, `index.html` и проверка файловой системы.
- **Observed:** PASSED (2 passed). Роуты возвращают HTTP 200; в `week1.js` присутствуют ключи `web_oop_w1_practice_code` и `web_oop_w1_lab_code` с debounce 300мс; в репозитории отсутствуют какие-либо сборочные файлы Node.js.
- **Limit:** Изоляция LocalStorage в рамках origin браузера.
- **Result:** HOLDS

### V7: C7 — Безопасность песочницы RunnerService при запуске решений Недели 1
- **Accepted claim / authority:** ASTValidator блокирует опасные модули (`os`, `sys`, `subprocess`) и вызовы (`eval`, `open`) со статусом `SECURITY_VIOLATION` (0 баллов); таймаут 5.0с прерывает зависающие процессы со статусом `TIMEOUT`.
- **Subject tuple:** `app/services/runner.py`, `app/services/ast_validator.py` @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, TS §5 AC-7.
- **Action or evidence:** Запуск `pytest tests/test_runner.py` и `pytest tests/test_week1_routes.py -k test_practice_run_endpoint`.
- **Observed:** PASSED (7 тестов runner + 1 тест API). Попытки вредоносного импорта и зависания корректно блокируются без падения сервера.
- **Limit:** ASTValidator не отслеживает глубокое метапрограммирование через рефлексию, но для локального учебного курса защита достаточна.
- **Result:** HOLDS

### V8: C8 — Интеграционный тестовый сьют и линтер
- **Accepted claim / authority:** Все 30 тестов сьюта `pytest` успешно проходят без регрессий; линтер `ruff check .` завершается без ошибок.
- **Subject tuple:** Репозиторий @ `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, Win32/Python 3.12, pytest 9.1.1, ruff 0.5.0, TS §5 AC-8.
- **Action or evidence:** Запуск `pytest -v` и `ruff check .`.
- **Observed:** `30 passed, 1 warning (Starlette deprecation) in 6.97s`. `ruff check .` -> `All checks passed!`.
- **Limit:** Нет.
- **Result:** HOLDS

### V9: C9 — Value-bearing accounting replay
- **Accepted claim / authority:** 13 файлов VALUE, 2578 добавленных строк (0 удаленных), укладываются в утвержденный бюджет TS §4 (<2760 LOC 2x лимит, <50 файлов, <5000 LOC).
- **Subject tuple:** Git diff Baseline `6da8e171` -> Candidate `10b8cfb5` @ selector `app/ docs/`, TS §4.
- **Action or evidence:** Запуск `git diff --name-status` и `git diff --numstat`.
- **Observed:** Ровно 13 файлов VALUE, 2578 additions, 0 deletions = 2578 touched LOC. 0 непредусмотренных изменений.
- **Limit:** Нет.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `git diff --name-status 6da8e171e758ea7df91a948d7265ec7112f295fa 10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac -- app/ docs/` | C9 | Exit 0: ровно 13 файлов VALUE, 0 отклонений от утвержденного селектора ТЗ §4 |
| 2 | `git diff --numstat 6da8e171e758ea7df91a948d7265ec7112f295fa 10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac -- app/ docs/` | C9 | Exit 0: 2578 additions, 0 deletions = 2578 touched LOC |
| 3 | `pytest -v` | C1–C8 | Exit 0: 30 passed, 1 warning (StarletteDeprecationWarning) in 6.97s |
| 4 | `ruff check .` | C8 | Exit 0: "All checks passed!" (0 errors, 0 warnings) |
| 5 | `git diff 6da8e171... 10b8cfb5... -- app/ docs/ \| Select-String -Pattern "TODO\|FIXME\|HACK"` | C9 | Exit 0: найдены только комментарии `# TODO:` внутри студенческих стартовых шаблонов (`practice.py`, `lab.py`), являющиеся методическими инструкциями для студентов |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | 5 разделов лекции и 2 диаграммы Mermaid | `app/content/week_1/lecture.py` | `tests/test_week1_content.py::test_lecture_content_structure` | ✅ |
| C2 | 5 вопросов квиза с методическими пояснениями и расчет до 3.0 б. | `app/content/week_1/quiz.py` | `tests/test_week1_content.py::test_quiz_questions_bank` | ✅ |
| C3 | 7 тестов практикума `TransitCard` и начисление до 7.0 б. | `app/content/week_1/practice.py` | `tests/test_week1_content.py::test_practice_secret_tests_and_reference_solution` | ✅ |
| C4 | 10 тестов лабы `SingleTripTicket` и `Bus`, проверка `@property` без сеттера (до 10.0 б.) | `app/content/week_1/lab.py` | `tests/test_week1_content.py::test_lab_secret_tests_and_reference_solution` | ✅ |
| C5 | Шкала 0..20, порог $\ge 12$ б., High-Water Mark ($\max$) | `app/services/scoring.py` | `tests/test_scoring.py` | ✅ |
| C6 | 4 вкладки Zero-Build UI, LocalStorage черновики, дашборд | `app/templates/week1.html`, `app/static/js/week1.js` | `tests/test_week1_routes.py::test_week1_page_render` | ✅ |
| C7 | Песочница: ASTValidator (`SECURITY_VIOLATION`), таймаут 5.0с (`TIMEOUT`) | `app/services/runner.py`, `app/services/ast_validator.py` | `tests/test_runner.py` | ✅ |
| C8 | 30/30 тестов проходят, ruff чист | Репозиторий | Терминальный вывод `pytest` и `ruff` | ✅ |
| C9 | Accounting: 13 файлов VALUE, 2578 LOC | Git commit `10b8cfb5` | `git diff --numstat` против Baseline `6da8e171` | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | Инкапсуляция статуса билета: `@property def is_validated` без сеттера | Попытка внешней подделки статуса билета (`ticket.is_validated = False`) должна пресекаться `AttributeError` | `test_ticket_encapsulation_no_setter` явно проверяет возбуждение `AttributeError` при попытке присваивания | admitted |
| G2 | permanent guard | Инвариант однократности поездки по разовому билету | Повторный вызов `validate(bus)` приводит к повторному проезду без оплаты | `test_ticket_already_used_error` проверяет выброс `TicketAlreadyUsedError` при повторном вызове | admitted |
| G3 | permanent guard | Инвариант срока годности разового билета (60 мин) | Проезд по просроченному билету | `test_ticket_expired_error` проверяет выброс `TicketExpiredError` при времени $\ge 61$ мин | admitted |
| G4 | permanent guard | Инварианты карты `TransitCard`: неотрицательный баланс, минимальное пополнение 100 ₸, защита от блокировки | Нарушение баланса или несанкционированные транзакции | 7 автотестов сьюта `PRACTICE_SECRET_TESTS` проверяют каждое нарушение специализированным исключением | admitted |
| G5 | permanent guard | Защита от потери баллов студента по правилу High-Water Mark ($\max$) | Студент теряет ранее заработанный балл при случайной синтаксической ошибке в новой попытке | `test_scoring_aggregation_and_high_water_mark` симулирует успешную попытку с последующей сбойной и проверяет сохранение максимального балла | admitted |
| G6 | permanent guard | Безопасность песочницы: блокировка вредоносного кода и зависающих циклов | Взлом сервера или зависание процесса на `while True` | `test_runner_security_violation_rejection` и `test_runner_timeout_enforcement` проверяют реакцию на опасный код | admitted |
| G7 | positive control | Доступность и структура контента лекции и квиза | Ошибки рендеринга контента в шаблонах | `test_lecture_content_structure`, `test_quiz_questions_bank` | labelled control |
| G8 | governance assertion | Форматирование кода и объем изменений | Засорение репозитория, неконтролируемый рост LOC | `ruff check .`, `git diff --numstat` replay | governance only |

## Candidate Findings

No findings.

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | E1 | `app/content/week_1/lecture.py` @ `10b8cfb5` | Repeated (`pytest`) | ✅ Establishes C1 | Нет |
| E2 | E2 | `app/content/week_1/quiz.py` @ `10b8cfb5` | Repeated (`pytest`) | ✅ Establishes C2 | Нет |
| E3 | E3 | `app/content/week_1/practice.py` @ `10b8cfb5` | Repeated (`pytest`) | ✅ Establishes C3 | Нет |
| E4 | E4 | `app/content/week_1/lab.py` @ `10b8cfb5` | Repeated (`pytest`) | ✅ Establishes C4 | Нет |
| E5 | E5 | `app/services/scoring.py` @ `10b8cfb5` | Repeated (`pytest`) | ✅ Establishes C5 | Нет |
| E6 | E6 | `app/templates/week1.html`, `app/static/js/week1.js` @ `10b8cfb5` | Repeated (`pytest` + inspection) | ✅ Establishes C6 | Нет |
| E7 | E7 | `app/services/runner.py` @ `10b8cfb5` | Repeated (`pytest`) | ✅ Establishes C7 | Нет |
| E8 | E8 | Репозиторий @ `10b8cfb5` | Repeated (`pytest` + `ruff`) | ✅ Establishes C8 | Нет |
| E9 | E-accounting | Git diff Baseline `6da8e171` -> Candidate `10b8cfb5` | Repeated (Git CLI) | ✅ Establishes C9 | Нет |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 | Priority 0 (`README.md` § Цель и North Star проекта) | ✅ | ✅ | ✅ Соответствует: интерактивная веб-LMS по ООП для студентов 2 курса | ✅ Прямое руководство |
| 2 | HL §7.2 #2 | Priority 1 (`.tfw/README.md` Methodology values) | ✅ | ✅ | ✅ Соответствует: Trace-First Workflow, строгое следование ролям и артефактам | ✅ Прямое руководство |
| 3 | HL §7.2 #3 | Priority 2 (`KNOWLEDGE.md` §1 D1 — Стек проекта) | ✅ | ✅ | ✅ Соответствует: Python 3.12, FastAPI, SQLite (SQLAlchemy), Pytest, Tailwind CSS CDN | ✅ Прямое руководство |
| 4 | HL §7.2 #4 | Priority 2 (`KNOWLEDGE.md` §1 D2 — Домен Avtobys) | ✅ | ✅ | ✅ Соответствует: транспортная система Алматы как сквозной учебный домен | ✅ Прямое руководство |
| 5 | HL §7.2 #5 | Priority 2 (`KNOWLEDGE.md` §1 D3 — Верификатор RunnerService) | ✅ | ✅ | ✅ Соответствует: двухфакторная проверка студенческих решений (AST + pytest) | ✅ Прямое руководство |
| 6 | HL §7.2 #6 | Priority 2 (`KNOWLEDGE.md` §1 D5 — Zero-Build интерфейс) | ✅ | ✅ | ✅ Соответствует: запрет node_modules, работа через CDN | ✅ Прямое руководство |
| 7 | HL §7.2 #7 | Priority 4 (`KNOWLEDGE.md` §4 F1 — Аудитория: 2 курс, 3 часа) | ✅ | ✅ | ✅ Соответствует: 1ч теория, 1ч практика, 1ч лаба | ✅ Прямое руководство |
| 8 | HL §7.2 #8 | Priority 4 (`KNOWLEDGE.md` §4 F4 — Изоляция RunnerService) | ✅ | ✅ | ✅ Соответствует: tempfile, таймаут 5.0с, запрет опасных модулей | ✅ Прямое руководство |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| `TS__OOP_20261015-162432_W1MAT.md @ approved` (zhasulan 2026-10-15) | `6da8e171e758ea7df91a948d7265ec7112f295fa` | `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac` | Ровно 13 файлов VALUE в селекторе `app/content/**`, `app/services/scoring.py`, `app/routers/week1.py`, `app/main.py`, `app/templates/week1.html`, `app/templates/index.html`, `app/static/js/week1.js`, `docs/week1_domain_guide.md` | 2578 | 0 | 2578 | 0 | 13 файлов < 50; 2578 LOC < 5000 LOC; < 2760 LOC (лимит 2x) | `git diff --numstat 6da8e171e758ea7df91a948d7265ec7112f295fa 10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac -- app/ docs/` | VERIFIED |

## Selected Knowledge Evidence

- **Producer unit:** `antigravity:thread:local:executor`
- **Source / epoch:** `Candidate 10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`
- **Inspected scope:** Полный учебный модуль Недели 1 (контент, роуты FastAPI, сервис оценивания scoring, Zero-Build UI на 4 вкладках, тесты, документация).
- **Lineage:** Зафиксировано утверждение ТЗ владельцем `@zhasulan` (коммит `832e32bf` / `fc551052`), онбординг Исполнителя (`f99b2af` / `6e945a9`), реализация в коммите `10b8cfb5` и сдача RF в коммите `e5419e9`. Цепочка непрерывна и аудируема.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
