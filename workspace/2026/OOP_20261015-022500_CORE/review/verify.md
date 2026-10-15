# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | High (основа API и UI) | `app/main.py`, `app/routers/health.py` | Win32, Python 3.12 | FastAPI TestClient, HTTP 200 JSON | Отсутствие внешнего E2E сетевого теста | Повторный прогон `tests/test_health.py` и ручная инспекция роутов |
| C2 | High (персистентность) | `app/database/`, `app/models/` | SQLite 3, SQLAlchemy 2.0 | Юнит-тесты моделей, SQLite engine | Локальная одиночная БД | Повторный прогон `tests/test_models.py` и инспекция каскадных связей |
| C3 | High (Zero-Build принцип) | `app/templates/index.html`, `app/static/js/app.js` | Web browser, CDN | Наличие CDN скриптов, отсутствие node_modules | CDN требует доступа к сети | Инспекция HTML/JS и проверка отсутствия `package.json` |
| C4 | Critical (безопасность песочницы) | `app/services/runner.py`, `app/services/ast_validator.py` | Subprocess Python 3.12, Windows 11 | AST parsing, timeout handler | Метапрограммирование `__subclasses__` | Прогон `tests/test_runner.py` (pass, fail, timeout, AST injection) |
| C5 | Medium (документация) | `docs/architecture.md`, `docs/domain_model_uml.md` | Markdown | Наличие обязательных разделов и диаграмм | Нет | Проверка полноты и отсутствия плейсхолдеров |
| C6 | High (качество кода) | `tests/`, `pyproject.toml` | pytest 9.1.1, ruff 0.17.0 | Вывод pytest и ruff | Нет | Полный повторный прогон `pytest -v` и `ruff check .` |
| C7 | High (чистота скоупа) | Корень репозитория, `content/` | Файловая система | Отсутствие материалов Недели 1 | Нет | Проверка структуры каталогов |
| C8 | Medium (трассируемость TFW) | Репозиторий git | Git CLI | `git diff --numstat` против Baseline `5724adc3` | Числовые расхождения в тексте RF | Replay diff numstat по селектору `app/`, `docs/` |

## Verification Log

### V1: C1 (FastAPI Server & Health API)
- **Accepted claim / authority:** Эндпоинт `GET /api/health` возвращает статус сервера, БД и раннера; Swagger UI доступен по `/docs`.
- **Subject tuple:** `{app/main.py, app/routers/health.py, Candidate e04ac923, Localhost/Win32 Python 3.12, FastAPI TestClient, Clean DB}`
- **Action or evidence:** Выполнен тест `tests/test_health.py::test_health_check` и `test_swagger_docs`.
- **Observed:** HTTP 200 OK, JSON payload `{"status": "ok", "db": "connected", "runner": "ready"}`. Swagger доступен на `/docs`.
- **Limit:** Проверено через TestClient (in-process transport Starlette).
- **Result:** HOLDS

### V2: C2 (Database Layer & Models)
- **Accepted claim / authority:** Модели `Student`, `TopicProgress`, `Submission` поддерживают CRUD, проверку уникальности и каскадное удаление.
- **Subject tuple:** `{app/models/*, app/database/*, Candidate e04ac923, SQLite 3 / SQLAlchemy 2.1.4, test fixtures, in-memory/file SQLite}`
- **Action or evidence:** Выполнен тестовый модуль `tests/test_models.py`.
- **Observed:** 4 теста прошли успешно. Уникальность `username` гарантируется IntegrityError, удаление студента каскадно очищает `Submission`.
- **Limit:** SQLite однопоточная локальная модель.
- **Result:** HOLDS

### V3: C3 (Zero-Build Frontend Dashboard)
- **Accepted claim / authority:** Zero-Build интерфейс на Tailwind CDN и Mermaid.js CDN; 3 индикатора статуса, smoke-кнопка, диаграмма Avtobys. Отсутствие `package.json` и `node_modules`.
- **Subject tuple:** `{app/templates/index.html, app/static/*, Candidate e04ac923, CDN/Browser, File system inspection, Zero npm}`
- **Action or evidence:** Инспекция `app/templates/index.html`, `app/static/js/app.js`, `app/static/css/style.css`, проверка `Test-Path package.json` и `Test-Path node_modules`.
- **Observed:** `package.json` отсутствует (False), `node_modules` отсутствует (False). CDN-скрипты Tailwind и Mermaid подключены. Индикаторы и smoke-кнопка реализованы на модульном Vanilla JS без транспиляторов.
- **Limit:** Клиент требует доступа к CDN при первом открытии.
- **Result:** HOLDS

### V4: C4 (RunnerService Sandbox & AST Security)
- **Accepted claim / authority:** Изолированный запуск pytest во временной директории, таймаут 5.0с для `while True`, блокировка опасных импортов (`os`, `sys`, `subprocess`, `shutil`, `socket`) и вызовов (`eval`, `exec`, `__import__`).
- **Subject tuple:** `{app/services/runner.py, app/services/ast_validator.py, Candidate e04ac923, Windows 11 / Subprocess, pytest exit codes, AST visitor}`
- **Action or evidence:** Выполнен сьют `tests/test_runner.py` (7 тестов).
- **Observed:** Все 7 тестов прошли: безопасный ООП-код валидируется; опасные импорты блокируются со статусом `SECURITY_VIOLATION`; бесконечный цикл прерывается ровно по таймауту со статусом `TIMEOUT`; нормальный код выполняется с `PASSED` и таймингом в миллисекундах.
- **Limit:** Защита ориентирована на сценарии локального курса программирования; глубокие векторы через `object.__subclasses__()` не эмулировались.
- **Result:** HOLDS

### V5: C5 (Documentation Deliverables)
- **Accepted claim / authority:** В наличии полные инженерные документы `docs/architecture.md` и `docs/domain_model_uml.md`.
- **Subject tuple:** `{docs/architecture.md, docs/domain_model_uml.md, Candidate e04ac923, Markdown, D1–D4 decisions}`
- **Action or evidence:** Инспекция файлов `docs/architecture.md` (106 строк) и `docs/domain_model_uml.md` (89 строк).
- **Observed:** Документы содержат описание Clean Architecture, модели угроз песочницы, UML диаграмму классов Avtobys (`Passenger`, `Validator`, `ValidationResult`) и ERD схемы БД. Плейсхолдеров нет.
- **Limit:** None
- **Result:** HOLDS

### V6: C6 (Automated Testing & Ruff Cleanliness)
- **Accepted claim / authority:** 100% тестов проходят успешно, линтер `ruff` не выдает замечаний.
- **Subject tuple:** `{tests/*, app/*, Candidate e04ac923, pytest 9.1.1, ruff 0.17.0, pyproject.toml}`
- **Action or evidence:** Запуск `pytest -v` и `ruff check .`.
- **Observed:** 15 passed in 4.21s, 0 failures; `All checks passed!` в ruff.
- **Limit:** None
- **Result:** HOLDS

### V7: C7 (Non-Goals Isolation)
- **Accepted claim / authority:** Учебный контент Недели 1 отсутствует.
- **Subject tuple:** `{Workspace root, Candidate e04ac923, File system, TS §2 Out of Scope}`
- **Action or evidence:** Сканирование рабочей директории и проверка отсутствия каталога `content/` или файлов лекций Недели 1.
- **Observed:** Каталог `content/` отсутствует, лекционные материалы не добавлены.
- **Limit:** None
- **Result:** HOLDS

### V8: C8 (Accounting Replay & Trace Integrity)
- **Accepted claim / authority:** Точное соответствие Baseline `5724adc3` и Candidate `e04ac923` утвержденному контракту учета.
- **Subject tuple:** `{Git repository, Candidate e04ac923, Baseline 5724adc3, TS §4, RF §1, EV E-accounting}`
- **Action or evidence:** Выполнена команда `git diff --numstat 5724adc3..e04ac923 -- app/ docs/`.
- **Observed:** Ровно 21 файл под селектором `app/`, `docs/`, 991 добавленная строка, 0 удалений. В тексте RF §1 и EV ошибочно указано "19 файлов" и "1184 adds". Бюджет триггеров (<50 файлов, <5000 LOC) полностью соблюден.
- **Limit:** Текстовая неточность в отчете RF §1 зафиксирована как наблюдение (F1).
- **Result:** FINDING (Observation, non-material TRACE)

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `pytest -v` | C1, C2, C4, C6 | Exit 0: 15 passed in 4.21s |
| 2 | `ruff check .` | C6 | Exit 0: All checks passed! |
| 3 | `git diff --numstat 5724adc39f0aee0482737670040d00bf5d339f32..e04ac9239a3b9ec2d9edf6ce657574242a709e2d -- app/ docs/` | C8 | Exit 0: 21 files, 991 additions, 0 deletions |
| 4 | `Test-Path package.json; Test-Path node_modules` | C3 | Exit 0: False, False |
| 5 | `git diff 5724adc3..e04ac923 -- app/ docs/ \| Select-String -Pattern "TODO\|FIXME\|HACK"` | C6 | Exit 0: 0 matches (no debt markers) |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | FastAPI + Health monitoring JSON | RF §3 AC-1, TS §5 AC-1 | `app/routers/health.py` | ✅ |
| C2 | SQLite models with cascade | RF §3 AC-2, TS §5 AC-2 | `app/models/` | ✅ |
| C3 | Zero-Build UI without node_modules | RF §3 AC-3, TS §5 AC-3 | `app/templates/index.html`, git | ✅ |
| C4 | RunnerService with AST & 5s timeout | RF §3 AC-4, TS §5 AC-4 | `app/services/runner.py`, `app/services/ast_validator.py` | ✅ |
| C5 | Documentation in `docs/` | RF §3 AC-5, TS §5 AC-5 | `docs/architecture.md`, `docs/domain_model_uml.md` | ✅ |
| C6 | 15 passing tests & clean ruff | RF §4, EV E10 | `pytest`, `ruff check .` | ✅ |
| C7 | Non-goals: no Week 1 content | RF §3 AC-7, TS §5 AC-7 | Workspace root | ✅ |
| C8 | Accounting baseline & candidate | RF §1, EV E-accounting | `git log`, `git diff` | ⚠️ (текстовая неточность в RF: заявлено 1184/19, фактически 991/21) |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | Блокировка опасных модулей `os`, `sys`, `subprocess`, `shutil`, `socket` и вызовов `eval`/`exec` | Компрометация хоста студента или внедрение системных команд | Отрицательный контроль: 8 сниппетов запрещенных импортов и 3 сниппета вызовов отклоняются с `is_safe=False` | admitted |
| G2 | permanent guard | Принудительное завершение бесконечного цикла по таймауту | Зависание дочернего процесса python.exe и блокировка раннера | Отрицательный контроль: `while True: pass` прерывается ровно по таймауту со статусом `TIMEOUT` | admitted |
| G3 | permanent guard | Уникальность логина студента `username` | Нарушение целостности учетных записей в БД | Отрицательный контроль: вставка дубликата вызывает `IntegrityError` | admitted |
| G4 | permanent guard | Каскадное удаление посылок студента (`Submission`) при удалении `Student` | Появление записей-сирот в SQLite базе | Отрицательный контроль: проверка `sub_after is None` после `db_session.delete(student)` | admitted |
| G5 | positive control | Эндпоинт `/api/health` возвращает статус готовности | Скрытый отказ одного из компонентов платформы | Проверка статуса 200 и полей JSON | labelled control |
| G6 | positive control | Эндпоинт `/api/runner/smoke` проводит smoke-тест | Нарушение сквозного пути от API к песочнице | Проверка статуса 200 и `passed=True` | labelled control |
| G7 | positive control | Корректное решение задачи проходит проверку песочницы | Ложные срабатывания раннера на валидном коде | Прогон валидного решения Calculator.add со статусом `PASSED` | labelled control |
| G8 | governance assertion | Линтер `ruff` и автотесты `pytest` | Снижение качества кода, скрытые синтаксические дефекты | Прогон `pytest` и `ruff check .` | governance only |

## Candidate Findings

| ID | Class | Subject | Affected claim / authority | Observed fact + oracle | Concrete harm | Material consequence or named absence | Owner | Observable completion | Route / rung | Candidate effect | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | TRACE | Текстовое расхождение учета в RF §1 и EV | TS §4 Accounting Contract vs RF §1 | В RF §1 и EV заявлено "19 файлов, 1184 adds", тогда как команда `git diff --numstat 5724adc3..e04ac923 -- app/ docs/` дает 21 файл и 991 adds | Неточность в текстовой декларации RF | Отсутствует функциональный вред: все 21 файл соответствуют плану TS §4, бюджет триггеров (<50 файлов, <5000 LOC) соблюден | Reviewer / Coordinator | Фиксация наблюдения в REVIEW §5; правка RF задним числом запрещена Role Lock | Observation in REVIEW | unchanged | observation |

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | E1 (FastAPI Health API) | `{app/routers/health.py, Candidate e04ac923, Localhost, TestClient}` | Repeated (`pytest`) | ✅ | None |
| E2 | E2 (Swagger UI) | `{app/main.py, Candidate e04ac923, Localhost, TestClient}` | Repeated (`pytest`) | ✅ | None |
| E3 | E3 (Database Layer & Models) | `{app/models/*, Candidate e04ac923, SQLite, pytest}` | Repeated (`pytest`) | ✅ | None |
| E4 | E4 (Zero-Build Dashboard) | `{app/templates/index.html, Candidate e04ac923, Browser, pytest}` | Repeated (`pytest` + inspection) | ✅ | None |
| E5 | E5 (Runner Smoke API) | `{app/routers/runner.py, Candidate e04ac923, Localhost, TestClient}` | Repeated (`pytest`) | ✅ | None |
| E6 | E6 (Runner Sandbox Execution) | `{app/services/runner.py, Candidate e04ac923, Subprocess, pytest}` | Repeated (`pytest`) | ✅ | None |
| E7 | E7 (Runner Timeout) | `{app/services/runner.py, Candidate e04ac923, Subprocess, pytest}` | Repeated (`pytest`) | ✅ | None |
| E8 | E8 (AST Security Inspection) | `{app/services/ast_validator.py, Candidate e04ac923, AST, pytest}` | Repeated (`pytest`) | ✅ | None |
| E9 | E9 (Documentation Deliverables) | `{docs/*, Candidate e04ac923, File system, inspection}` | Opened (file inspection) | ✅ | None |
| E10 | E10 (Automated Testing & Ruff) | `{tests/*, Candidate e04ac923, pytest/ruff, shell}` | Repeated (`pytest` & `ruff`) | ✅ | None |
| E11 | E11 (Non-Goals Isolation) | `{Workspace root, Candidate e04ac923, File system}` | Opened (file inspection) | ✅ | None |
| E-acc | E-accounting | `{Git diff, Candidate e04ac923, Baseline 5724adc3, git}` | Repeated (`git diff --numstat`) | ⚠️ | Зафиксировано текстовое расхождение (F1: 21 файл / 991 LOC) |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 | Priority 0: `README.md` § 1. Миссия и цели проекта | ✅ | ✅ | ✅ — Локальная мини-LMS для изучения ООП студентами | ✅ — Задает цель и рамки каркаса |
| 2 | HL §7.2 #2 | Priority 1: `.tfw/README.md` Methodology values | ✅ | ✅ | ✅ — TFW трассируемость, независимое ревью | ✅ — Обеспечивает соблюдение процесса |
| 3 | HL §7.2 #3 | Priority 3: `KNOWLEDGE.md` § 1. Architecture Map | ✅ | ✅ | ✅ — Слои Clean Architecture (routers, services, models, database) | ✅ — Прямое соответствие структуре `app/` |
| 4 | HL §7.2 #4 | Priority 3: `KNOWLEDGE.md` D1 (Стек) | ✅ | ✅ | ✅ — Python 3.12, FastAPI, SQLite, Tailwind CDN, Vanilla JS, Mermaid | ✅ — Технический стек платформы |
| 5 | HL §7.2 #5 | Priority 3: `KNOWLEDGE.md` D2 (Домен) | ✅ | ✅ | ✅ — Сквозной домен Avtobys (Passenger, Validator) | ✅ — Визуализация в UI и документации |
| 6 | HL §7.2 #6 | Priority 3: `KNOWLEDGE.md` D3 (Верификатор) | ✅ | ✅ | ✅ — AST-анализ + запуск pytest с таймаутом 5с | ✅ — Реализация в RunnerService |
| 7 | HL §7.2 #7 | Priority 3: `KNOWLEDGE.md` D4 (Документация) | ✅ | ✅ | ✅ — Создание `docs/architecture.md` и `docs/domain_model_uml.md` | ✅ — Документация создана и заполнена |
| 8 | HL §7.2 #8 | Priority 4: `.tfw/conventions.md` § 3. HL Contract | ✅ | ✅ | ✅ — Правила заморозки контракта HL | ✅ — Контракт HL зафиксирован на baseline |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| zhasulan (TS @ c67c6aa6) | `5724adc39f0aee0482737670040d00bf5d339f32` | `e04ac9239a3b9ec2d9edf6ce657574242a709e2d` | `app/__init__.py`, `app/config.py`, `app/database/__init__.py`, `app/database/base.py`, `app/database/session.py`, `app/main.py`, `app/models/__init__.py`, `app/models/progress.py`, `app/models/student.py`, `app/models/submission.py`, `app/routers/__init__.py`, `app/routers/health.py`, `app/routers/runner.py`, `app/services/__init__.py`, `app/services/ast_validator.py`, `app/services/runner.py`, `app/static/css/style.css`, `app/static/js/app.js`, `app/templates/index.html`, `docs/architecture.md`, `docs/domain_model_uml.md` (21 файл) | 991 | 0 | 991 | N/A | 21 файлов < 50, 991 LOC < 5000 (в рамках бюджета) | `git diff --numstat 5724adc39f0aee0482737670040d00bf5d339f32..e04ac9239a3b9ec2d9edf6ce657574242a709e2d -- app/ docs/` | VERIFIED |

## Selected Knowledge Evidence

- Исполнитель (Executor) выполнил реализацию строго в рамках замороженного контракта HL и спецификации TS.
- Применена утвержденная архитектура Clean Architecture и Zero-Build подход.
- Домен Avtobys корректно интегрирован в визуализацию и документацию.
- Никаких скрытых зависимостей или несанкционированных изменений не обнаружено.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
