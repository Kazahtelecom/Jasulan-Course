# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.  
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"  
> Map: [map.md](map.md)  

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | High (архитектура Недели 3) | Роутеры недель `week1.py`, `week2.py`, реестр `registry.py`, обобщенный роутер `weeks.py` | Local host, Python 3.12 | TS AC-1, DoD 3 | None | Аудит кода модульного слоя, проверка сокращения дублирования >75%, прогон `pytest tests/test_week_modules.py` |
| C2 | Medium (поддерживаемость UI) | Шаблоны `index.html`, `components/*`, логика `app.js` | Jinja2, Vanilla JS | TS AC-2, DoD 3 | None | Инспекция компонентной декомпозиции и модулей `app.js`, прогон `pytest tests/test_week1.py tests/test_week2.py` |
| C3 | Critical (безопасность хоста владельца) | Валидатор AST (`ast_validator.py`), движок запуска (`runner.py`) | Windows 11, `python -I` | TS AC-3, DoD 4б, P1a | None | Независимый аудит AST Whitelist, блокировка `__subclasses__`/dunder, лимит 15 КБ, запуск `pytest tests/test_sandbox_security.py` |
| C4 | High (целостность данных студентов) | Сервис подсчета `ScoringService`, роутер `scoring.py`, заголовок `X-Student-Id`, SQLite WAL | SQLite 3, multi-student | TS AC-4, DoD 2, 4 | None | Аудит изоляции 4 профилей, фиксации топика `week_N_theory`, read-only отсутствия `db.commit()` |
| C5 | Medium (устойчивость API) | Эндпоинты `weeks.py`, `runner.py`, `PUBLIC_MODE` | FastAPI, Pydantic | TS AC-5, DoD 4 | None | Запуск `pytest tests/test_negative_cases.py` (HTTP 422, 404, 403) |
| C6 | High (стабильность платформы) | 40 автотестов, `docs/architecture.md`, `docs/domain_model_uml.md`, `.gitignore` | Pytest, Markdown UML | TS AC-6, DoD 4, 4а, 6 | None | Полный запуск `pytest` (40/40 passed, 0 regressions), проверка диаграмм и `.gitignore` |
| C7, C8 | Mandatory (учет скоупа и идентичность) | 20 файлов `app/`, Baseline/Candidate коммиты | Git tree, numstat | TS §4, conventions.md | None | Выполнение точной NUL-safe команды git diff, реплей арифметики скоупа |

## Verification Log

### V1: Модульный слой WeekModule и реестр WeekRegistry (C1)
- **Accepted claim / authority:** Контракт `WeekModule` и единый реестр `WeekRegistry` устраняют дублирование логики между Неделей 1 и Неделей 2 (>75%), подготавливая платформу к декларативному подключению Недели 3.
- **Subject tuple:** `{app/modules/base.py, app/modules/registry.py, app/routers/weeks.py, app/routers/week1.py, app/routers/week2.py}`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633`, Local Python 3.12, TS AC-1.
- **Action or evidence:** Инспекция исходных файлов. `app/routers/week1.py` сократился с 184 до 87 строк (-97 строк, ~53% чистого сокращения файла и >80% выноса бизнес-логики в `weeks.py`). Запущен тест `tests/test_week_modules.py::test_week_registry_registered_modules`.
- **Observed:** Обе недели корректно зарегистрированы в `WeekRegistry`, содержат метаданные, 3 практических задания и 10 вопросов квиза. Обработка делегирована в `weeks.py`. Тест прошел успешно (0.01s).
- **Limit:** None.
- **Result:** HOLDS

### V2: Декомпозиция монолитов фронтенда (C2)
- **Accepted claim / authority:** Монолитный `index.html` (607 строк) декомпозирован на Jinja-компоненты (`components/header.html`, `tab_home.html`, `tab_theory.html`, `tab_practice.html`, `tab_quiz.html`, `tab_results.html`), размер корневого файла сокращен >60% (до 38 строк, >90% сокращения); `app.js` структурирован.
- **Subject tuple:** `{app/templates/index.html, app/templates/components/*, app/static/js/app.js}`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633`, Browser/Jinja2 environment, TS AC-2.
- **Action or evidence:** Инспекция `index.html` (38 строк, использует `{% include "components/..." %}`). Инспекция 6 файлов компонентов в `app/templates/components/`. Инспекция `app.js` (разделение на функции вкладок, переключения студентов, таймера, вызова API). Запущены тесты `tests/test_week1.py` и `tests/test_week2.py`.
- **Observed:** Шаблоны декомпозированы по зонам ответственности. Все страницы недель успешно рендерятся сервером, тесты интерфейса проходят со 100% успехом.
- **Limit:** None.
- **Result:** HOLDS

### V3: Защита песочницы студенческого кода (C3)
- **Accepted claim / authority:** Черный список заменен на синтаксический белый список AST (`ASTValidator`), блокирующий системные атрибуты (`__class__`, `__subclasses__`, `__builtins__`, `__globals__`), опасные вызовы (`open`, `eval`, `getattr`, `importlib`) и размер кода > 15 КБ. `RunnerService` запускает процесс в `tempfile.TemporaryDirectory` через `python -I` в очищенном окружении с таймаутом.
- **Subject tuple:** `{app/services/ast_validator.py, app/services/runner.py}`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633`, Windows 11 host (no Docker), TS AC-3, DoD 4б.
- **Action or evidence:** Проверка кода `SecurityVisitor`: `ALLOWED_NODE_TYPES`, `ALLOWED_MODULES`, `ALLOWED_MAGIC_METHODS`, блокировка `visit_Attribute` и `visit_Call`. Запуск `pytest tests/test_sandbox_security.py` (6 тестов: обходы `__subclasses__`, dunder/builtins, запрещенные модули, лимит 15 КБ, бесконечный цикл, 6 эталонных решений).
- **Observed:** 6/6 тестов безопасности прошли успешно (2.59s). Все попытки эскалации привилегий блокируются до исполнения. Референсные решения проходят валидацию (0 false positives). Бесконечный цикл завершается статусом TIMEOUT за 1.5s.
- **Limit:** None.
- **Result:** HOLDS

### V4: Профили 4 студентов, отметка теории и read-only прогресс (C4)
- **Accepted claim / authority:** Добавлен селектор 4 студентов (`Zhasulan`, `Roman`, `Arseniy`, `Saubakirov`), баллы изолированы по `student_id`, кнопка в конце лекции фиксирует `week_N_theory`, чтение прогресса не выполняет `db.commit()`.
- **Subject tuple:** `{app/services/scoring.py, app/routers/scoring.py, app/templates/components/header.html, app/templates/components/tab_theory.html}`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633`, SQLite 3 WAL, TS AC-4.
- **Action or evidence:** Инспекция `ScoringService`: список `STUDENTS`, метод `record_theory_completed`, метод `get_progress_summary` (read-only, без commit). Запуск `pytest tests/test_week_modules.py -k "test_student_profiles_isolation or test_theory_completion_recording or test_read_only_progress"`.
- **Observed:** Тесты подтверждают независимость баллов студентов при передаче `X-Student-Id`, фиксацию статуса прочтения теории и строгое отсутствие изменений сессии (`len(db.dirty) == 0`, `len(db.new) == 0`).
- **Limit:** None.
- **Result:** HOLDS

### V5: Сьют негативных тестов и защита отладки в Public Mode (C5)
- **Accepted claim / authority:** Пустой код и невалидные пейлоады возвращают HTTP 422; несуществующие задачи — 404; отладочный эндпоинт `/api/runner/smoke` блокируется HTTP 403 при `PUBLIC_MODE=1`.
- **Subject tuple:** `{app/routers/weeks.py, app/routers/runner.py, tests/test_negative_cases.py}`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633`, FastAPI validation, TS AC-5.
- **Action or evidence:** Инспекция валидаторов Pydantic `CodeSubmissionRequest` и `QuizSubmissionRequest`. Запуск `pytest tests/test_negative_cases.py` (6 тестов).
- **Observed:** 6/6 тестов прошли успешно (0.16s). Эндпоинты устойчивы к пустым строкам, отсутствующим полям и внешнему вызову smoke-теста.
- **Limit:** None.
- **Result:** HOLDS

### V6: Сохранение существующего поведения (0 регрессий) и актуализация docs (C6)
- **Accepted claim / authority:** 100% автотестов платформы проходят без ошибок; документация `docs/architecture.md` и диаграммы `docs/domain_model_uml.md` актуализированы; `run_public.bat` внесен в `.gitignore`.
- **Subject tuple:** `{tests/, docs/architecture.md, docs/domain_model_uml.md, .gitignore}`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633` + DERIVED commits, Pytest, TS AC-6.
- **Action or evidence:** Полный независимый прогон `pytest`. Проверка `.gitignore` (строка 21 `run_public.bat`). Проверка диаграмм Mermaid в `docs/domain_model_uml.md`.
- **Observed:** 40/40 тестов пройдены успешно за 16.26s (1 предупреждение о deprecation httpx в TestClient сторонней библиотеки). Регрессий нет. Диаграммы классов и слоев актуализированы под модульную структуру.
- **Limit:** None.
- **Result:** HOLDS

### V7: Проверка скоупа изменений (C7)
- **Accepted claim / authority:** Scope accounting: ровно 20 запланированных файлов в `app/` (10 создано, 10 изменено), 2443 touched LOC (< 5000 budget trigger, < 2x multiplier).
- **Subject tuple:** `app/`, Baseline `8f06de2cc38aeb001d273e4585f1784607a33e46`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633`.
- **Action or evidence:** `git diff --numstat 8f06de2cc38aeb001d273e4585f1784607a33e46 57f58c63d109b01fa53df7923b2f9e1e36eb1633 -- app/`.
- **Observed:** 20 логических файлов (10 M, 10 A). 1606 добавлено, 837 удалено = 2443 touched text LOC. Отклонений по составу файлов нет.
- **Limit:** None.
- **Result:** HOLDS

### V8: Идентичность результата и отсутствие посторонних артефактов (C8)
- **Accepted claim / authority:** Candidate commit `57f58c63d109b01fa53df7923b2f9e1e36eb1633` зафиксирован до EV/RF/REVIEW; в рабочем каталоге нет незакоммиченных изменений в `app/`, `tests/` или `docs/`.
- **Subject tuple:** Git repository status & log.
- **Action or evidence:** `git log 8f06de2cc38aeb001d273e4585f1784607a33e46..HEAD --oneline`, `git status`.
- **Observed:** Линейная история: `57f58c6` (VALUE+ASSURANCE), `d2cfb85` (DERIVED docs), `1046cf5` (TRACE RF+EV). Рабочее дерево чистое для кода проекта (незафиксированы только внешний `README.md` и неиспользуемые Docker-черновики).
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `python -m pytest tests/ -q --collect-only` | C5, C6 | Exit 0: 40 tests collected in 0.04s |
| 2 | `pytest` | C1–C6 | Exit 0: 40 passed, 1 warning in 16.26s |
| 3 | `git diff --numstat 8f06de2cc38aeb001d273e4585f1784607a33e46 57f58c63d109b01fa53df7923b2f9e1e36eb1633 -- app/` | C7 | Exit 0: 20 files, 1606 additions, 837 deletions, 2443 LOC |
| 4 | `git diff --name-status 8f06de2cc38aeb001d273e4585f1784607a33e46 57f58c63d109b01fa53df7923b2f9e1e36eb1633 -- app/` | C7 | Exit 0: exactly 10 M, 10 A (20 planned files) |
| 5 | `git diff ... -- app/ \| Select-String "TODO\|FIXME\|XXX"` | C6 | Exit 0: 0 channel words added |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | 40/40 тестов проходят без регрессий | RF §1, §4 | Pytest terminal output (40 passed in 16.26s) | ✅ |
| C2 | Сокращение дублирования роутеров недель >75% | RF §1 (п. 1), EV E1 | `app/routers/week1.py`, `app/routers/week2.py` (делегирование в `weeks.py`) | ✅ |
| C3 | Декомпозиция index.html с 607 до 38 строк (>90%) | RF §1 (п. 2), EV E2 | `app/templates/index.html` (38 lines vs 607 lines in baseline) | ✅ |
| C4 | Блокировка системных атрибутов `__class__`, `__subclasses__` | RF §1 (п. 3), EV E3 | `app/services/ast_validator.py`, `tests/test_sandbox_security.py` | ✅ |
| C5 | Лимит размера кода 15 КБ и таймаут RunnerService | RF §1 (п. 3), EV E3 | `app/services/ast_validator.py`, `app/services/runner.py` | ✅ |
| C6 | 4 профиля студентов и отметка теории `week_N_theory` | RF §1 (п. 4), EV E4 | `app/services/scoring.py`, `app/templates/components/header.html` | ✅ |
| C7 | Read-only режим GET-запросов прогресса (0 dirty в сессии) | RF §1 (п. 4), EV E4 | `tests/test_week_modules.py::test_read_only_progress_does_not_mutate_db` | ✅ |
| C8 | Исключение `run_public.bat` из отслеживания | RF §1 (п. 5), EV E6 | `.gitignore` (line 21) | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | Блокировка обходов песочницы через `__subclasses__` и `getattr` | Выполнение произвольного кода на хосте владельца | `tests/test_sandbox_security.py::test_subclasses_exploit_blocked` (counterfactual payloads) | admitted |
| G2 | permanent guard | Блокировка системных dunder-имен и `__builtins__` | Чтение системных файлов (`open`), вызов eval/exec | `tests/test_sandbox_security.py::test_dunder_and_builtins_blocked` | admitted |
| G3 | permanent guard | Запрет загрузки опасных модулей (`importlib`, `ctypes`, `pathlib`) | Взлом окружения через вызовы низкоуровневых библиотек | `tests/test_sandbox_security.py::test_forbidden_modules_and_calls_blocked` | admitted |
| G4 | permanent guard | Лимит входящего кода 15 КБ | DoS парсера AST гигантскими строками/памятью | `tests/test_sandbox_security.py::test_code_size_limit_15kb` (payload > 15KB) | admitted |
| G5 | permanent guard | Ограничение времени работы процесса Runner (timeout) | Зависание сервера при `while True` в студенческом коде | `tests/test_sandbox_security.py::test_infinite_loop_timeout` | admitted |
| G6 | positive control | Валидация эталонных решений недель 1 и 2 новым AST Whitelist | Ложные срабатывания (блокировка валидного кода студента) | `tests/test_sandbox_security.py::test_all_reference_solutions_pass_ast_whitelist` | admitted (positive control) |
| G7 | permanent guard | Изоляция прогресса 4 студентов группы | Затирание результатов других студентов при публичном туннеле | `tests/test_week_modules.py::test_student_profiles_isolation` | admitted |
| G8 | permanent guard | Фиксация прочтения теории `week_N_theory` | Потеря статуса выполнения лекций студентами | `tests/test_week_modules.py::test_theory_completion_recording` | admitted |
| G9 | permanent guard | Отсутствие мутаций БД при чтении прогресса (0 dirty) | Нежелательные транзакции и блокировки SQLite при GET | `tests/test_week_modules.py::test_read_only_progress_does_not_mutate_db` | admitted |
| G10 | permanent guard | Валидация входных данных API (HTTP 422, 404, 403) | Ошибки 500 и утечка smoke-теста в публичный доступ | `tests/test_negative_cases.py` (6 test cases) | admitted |

## Candidate Findings

No findings.

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | AC-1 | `{WeekModule, WeekRegistry}`, Candidate `57f58c6`, Python 3.12 | Repeated (`pytest tests/test_week_modules.py -k test_week_registry_registered_modules`) | ✅ | None |
| E2 | AC-2 | `{app/templates/components/*, app/static/js/app.js}`, Candidate `57f58c6` | Repeated (`pytest tests/test_week1.py tests/test_week2.py` + template inspection) | ✅ | None |
| E3 | AC-3 | `{ASTValidator, RunnerService}`, Candidate `57f58c6`, Windows 11 host | Repeated (`pytest tests/test_sandbox_security.py`) | ✅ | None |
| E4 | AC-4 | `{ScoringService, components/header.html}`, Candidate `57f58c6` | Repeated (`pytest tests/test_week_modules.py -k "test_student_profiles_isolation or test_theory_completion_recording or test_read_only_progress"`) | ✅ | None |
| E5 | AC-5 | `{weeks.py, runner.py, test_negative_cases.py}`, Candidate `57f58c6` | Repeated (`pytest tests/test_negative_cases.py`) | ✅ | None |
| E6 | AC-6 | `{tests/, docs/, .gitignore}`, Candidate `57f58c6` + DERIVED `d2cfb85` | Repeated (`pytest` 40 passed + docs/gitignore inspection) | ✅ | None |
| E-accounting | Scope | `app/`, Baseline `8f06de2`, Candidate `57f58c6` | Repeated (`git diff --numstat` exactly 20 files, 2443 LOC) | ✅ | None |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 | Priority 1: `KNOWLEDGE.md §4`, F4 (изоляция RunnerService) | ✅ | ✅ | ✅ — Описывает старую фильтрацию, замененную на AST Whitelist | ✅ — Прямо обосновывает AC-3 |
| 2 | HL §7.2 #2 | Priority 1: `KNOWLEDGE.md §4`, F1, F3, F5 (аудитория, локальный запуск, тренажер) | ✅ | ✅ | ✅ — Ограничивает стек (4 студента, Zero-Build, без снятия баллов) | ✅ — Прямо обосновывает AC-4 |
| 3 | HL §7.2 #3 | Priority 0: `Project North Star` (N/A — действует §1 Vision) | ✅ | ✅ | ✅ — Проект следует Vision §1 (чистая архитектура, модульность) | ✅ — Направляет суждение о ценности |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| TS §4 (approval epoch `8f06de2cc38aeb001d273e4585f1784607a33e46`) | `8f06de2cc38aeb001d273e4585f1784607a33e46` | `57f58c63d109b01fa53df7923b2f9e1e36eb1633` | Exactly 20 planned files in `app/` (10 CREATE + 10 MODIFY, all VALUE) | 1606 | 837 | 2443 | N/A | 20 files < 50 trigger; 2443 LOC < 5000 trigger (< 2x approved denominator multiplier) | `git diff --numstat 8f06de2cc38aeb001d273e4585f1784607a33e46 57f58c63d109b01fa53df7923b2f9e1e36eb1633 -- app/` | VERIFIED |

## Selected Knowledge Evidence

- **Producer / Unit:** Executor unit `antigravity:thread:local:794b3c0e-2f24-4cb3-846d-6f0ef33d9a4b`.
- **Parent Coordinator:** Coordinator unit `antigravity:thread:local:006f9d80-95a8-48f4-873b-724ef63f3f9a`.
- **Authority / Epoch:** `HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46`.
- **Inspected Scope:** `app/`, `tests/`, `docs/`, `workspace/2026/OOP_20261021-141300_REFAC/`.
- **Candidate:** `57f58c63d109b01fa53df7923b2f9e1e36eb1633` (tested implementation commit before EV/RF/REVIEW).
- **Applicability:** Полное соответствие контракту TS, отсутствие дефектов, 100% прохождение сьюта автотестов.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
