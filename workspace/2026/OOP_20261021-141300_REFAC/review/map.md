# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.  
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"  
> RF: [RF__OOP_20261021-141300_REFAC.md](../RF__OOP_20261021-141300_REFAC.md)  
> TS: [TS__OOP_20261021-141300_REFAC.md](../TS__OOP_20261021-141300_REFAC.md)  

## Understanding

Исполнитель выполнил комплексный предстартовый рефакторинг платформы Web-OOP для подготовки к созданию Недели 3: устранил дублирование роутеров недель через контракт `WeekModule` и реестр `WeekRegistry`, декомпозировал монолитный шаблон `index.html` на 6 Jinja-компонентов, заменил уязвимый черный список AST на строгий белый список синтаксиса с изоляцией `python -I` и лимитом 15 КБ, ввел переключатель 4 профилей студентов с отметкой прочтения лекций и отсутствием мутаций при чтении, закрыл отладочные ручки в `PUBLIC_MODE` и расширил тестовый сьют с 24 до 40 тестов при 100% сохранении обратной совместимости.

## Accepted Claims and Boundaries

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | Устранение дублирования недель через WeekModule и единый реестр WeekRegistry (сокращение >75%) | Копирование кода для недели 3, рассинхронизация логики обработки квизов и задач | Роутеры недель `app/routers/week1.py`, `week2.py`, единый обработчик `weeks.py`, реестр `app/modules/registry.py` | Local host, Python 3.12, FastAPI | TS AC-1, DoD 3 | `app/modules/@57f58c6`, `tests/test_week_modules.py` | yes |
| C2 | VALUE | Декомпозиция монолита `index.html` на 6 Jinja-компонентов и модульный `app.js` | Невозможность поддержки и расширения UI, коллизии разметки | `app/templates/index.html`, `app/templates/components/*`, `app/static/js/app.js` | Jinja2 templates, browser UI | TS AC-2, DoD 3 | `app/templates/@57f58c6`, `tests/test_week1.py` | yes |
| C3 | VALUE | Защита песочницы: строгий AST Whitelist, python -I, лимит 15 КБ, блокировка `__subclasses__` и `getattr` | Выполнение произвольного кода на хосте владельца, утечка данных, зависание процесса | `app/services/ast_validator.py`, `app/services/runner.py` | Windows 11 host (no Docker), subprocess `python -I` | TS AC-3, DoD 4б, P1a | `app/services/@57f58c6`, `tests/test_sandbox_security.py` | yes (mandatory security) |
| C4 | VALUE | Профили 4 студентов (`Zhasulan`, `Roman`, `Arseniy`, `Saubakirov`), отметка теории `week_N_theory`, read-only чтение прогресса | Затирание баллов студентов при общем туннеле, невыполнение требований преподавателя, блокировка БД при GET | `app/services/scoring.py`, `app/routers/scoring.py`, SQLite WAL | SQLite 3, multi-user header `X-Student-Id` | TS AC-4, DoD 2, 4 | `app/services/scoring.py@57f58c6`, `tests/test_week_modules.py` | yes |
| C5 | ASSURANCE | Негативные тесты API: валидация пейлоадов (HTTP 422), 404, 403 на smoke в public mode | Неконтролируемые 500 ошибки при невалидных данных, доступ к отладке извне | `app/routers/runner.py`, `app/main.py`, `tests/test_negative_cases.py` | FastAPI request validation, `PUBLIC_MODE` | TS AC-5, DoD 4 | `tests/test_negative_cases.py@57f58c6` | yes |
| C6 | ASSURANCE / DERIVED | 100% обратная совместимость (0 регрессий), актуализация UML диаграмм и архитектуры, игнорирование `run_public.bat` | Поломка существующих недель 1 и 2, рассинхрон документации с кодом, утечка локального запуска в git | `docs/architecture.md`, `docs/domain_model_uml.md`, `.gitignore`, `tests/` | Pytest suite (40 tests), git tracking | TS AC-6, DoD 4, 4а, 6 | `tests/@57f58c6`, `docs/@d2cfb85`, `.gitignore@d2cfb85` | yes |
| C7 | TRACE | Точное соответствие утвержденному скоупу VALUE: 20 файлов в `app/`, 2443 touched LOC (< 5000 trigger) | Разрастание объема работ без согласования, неконтролируемые сайд-эффекты | Каталог `app/` | Git diff numstat against baseline `8f06de2cc38aeb001d273e4585f1784607a33e46` | TS §4 prospective contract | `app/@57f58c6`, git diff output | yes |
| C8 | TRACE | Идентичность артефактов и независимость: Baseline `8f06de2cc38aeb001d273e4585f1784607a33e46`, Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633` | Нарушение контрактной базы, непроверяемость результатов | Git commit graph, RF, status.md | Git repository history | TS §4, conventions.md | Candidate commit `57f58c6` | yes (mandatory identity) |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1 (WeekModule и реестр) | RF §1 (п. 1), §3 (AC-1) | C1 | ✅ |
| AC-2 (Декомпозиция шаблонов и app.js) | RF §1 (п. 2), §3 (AC-2) | C2 | ✅ |
| AC-3 (Безопасность песочницы AST Whitelist) | RF §1 (п. 3), §3 (AC-3) | C3 | ✅ |
| AC-4 (Профили 4 студентов и отметка теории) | RF §1 (п. 4), §3 (AC-4) | C4 | ✅ |
| AC-5 (Сьют негативных тестов API) | RF §1 (п. 5), §3 (AC-5) | C5 | ✅ |
| AC-6 (Сохранение поведения 100% и docs) | RF §1 (п. 6-7), §3 (AC-6) | C6 | ✅ |
| Prospective Accounting (`app/`, 20 файлов) | RF §1 (Accounting table) | C7 | ✅ |
| Candidate SHA & Baseline SHA | RF §1, §9 (Handover) | C8 | ✅ |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1 | Независимый аудит `app/modules/base.py`, `registry.py`, `app/routers/weeks.py`, `week1.py`, `week2.py` + прогон `pytest tests/test_week_modules.py` | Критично для архитектуры Недели 3: модули должны изолировать контент, а роутер делегировать без дублирования | Нет |
| C2 | Инспекция структуры `app/templates/index.html` и компонентов в `app/templates/components/`, проверка структуры `app.js` | Убедиться в реальной декомпозиции и отсутствии монолитных дубликатов | Нет |
| C3 | Аудит `app/services/ast_validator.py` (разрешенные AST узлы, блокировка dunder-атрибутов), аудит `app/services/runner.py` (флаг `-I`, лимит 15 КБ) + запуск `pytest tests/test_sandbox_security.py` | Обязательная граница безопасности хоста; проверка контрфактических тестов обхода | Нет |
| C4 | Аудит реализации `ScoringService` (`STUDENTS`, чтение без `commit`), эндпоинтов `/api/scoring`, компонентов интерфейса + запуск профильных тестов | Изоляция сессий и отсутствие lock/dirty записей в WAL SQLite | Нет |
| C5 | Аудит `test_negative_cases.py`, проверка ответов 422, 404, 403 в `PUBLIC_MODE` | Надежность API при внешнем публичном туннеле | Нет |
| C6 | Полный независимый прогон сьюта `pytest` (40 тестов), проверка `docs/architecture.md`, `docs/domain_model_uml.md` и `.gitignore` | Гарантия отсутствия регрессий в существующих неделях 1 и 2, актуальность документации | Нет |
| C7, C8 | Проверка `git diff --numstat` и `git diff --name-status` между Baseline `8f06de2cc38aeb001d273e4585f1784607a33e46` и Candidate `57f58c63d109b01fa53df7923b2f9e1e36eb1633` | Независимый аудит учета объема работ и границ фиксации | Нет |

## Deviations from TS

No deviations. Все заявленные в TS артефакты, классы изменений и критерии приемки AC-1..AC-6 реализованы в точности в запланированном объеме.

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
