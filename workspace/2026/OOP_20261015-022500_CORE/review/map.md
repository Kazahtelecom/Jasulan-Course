# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__OOP_20261015-022500_CORE.md](../RF__OOP_20261015-022500_CORE.md)
> TS: [TS__OOP_20261015-022500_CORE.md](../TS__OOP_20261015-022500_CORE.md)

## Understanding

Создан платформенный каркас локальной мини-LMS по ООП на базе FastAPI, SQLite (SQLAlchemy 2.0) и строгого Zero-Build фронтенда (Tailwind CSS CDN, Vanilla JS, Mermaid.js CDN). Система включает изолированную песочницу RunnerService с двухуровневой защитой (статический анализ AST и таймаут 5.0 секунд) для выполнения студенческих решений, инженерную документацию в `docs/` и полный набор автотестов в `tests/`. Задача строго исключает контент курса Недели 1 и любые локальные зависимости сборщиков Node.js/npm.

## Accepted Claims and Boundaries

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | FastAPI приложение и API здоровья: `/api/health` возвращает статус сервера, БД и раннера; Swagger UI доступен на `/docs` | Невозможность мониторинга состояния системы или взаимодействия через API | `app/main.py`, `app/routers/health.py`, `app/config.py` | Localhost (Win32, Python 3.12) | FastAPI TestClient, HTTP 200 JSON contract | `app/routers/health.py@e04ac923`, `tests/test_health.py` | yes |
| C2 | VALUE | Слой данных SQLite и модели SQLAlchemy 2.0 (`Student`, `TopicProgress`, `Submission`), автоматическое создание схемы при старте | Потеря данных о студентах, прогрессе или сдаче работ; ошибки миграции схемы | `app/database/`, `app/models/`, `data/web_oop.db` | SQLite 3, SQLAlchemy 2.0 | Юнит-тесты моделей, SQLite engine | `app/models/@e04ac923`, `tests/test_models.py` | yes |
| C3 | VALUE | Zero-Build веб-дашборд: страница `/` на CDN Tailwind и Mermaid.js, 3 индикатора статуса, smoke-кнопка, диаграмма Avtobys (`Passenger`, `Validator`). Отсутствие `package.json` и `node_modules` | Нарушение Zero-Build принципа, утяжеление стека для студентов 2 курса, поломка UX | `app/templates/index.html`, `app/static/js/app.js`, `app/static/css/style.css` | Современный браузер с доступом к CDN | Инспекция DOM, отсутствие node-артефактов в git | `app/templates/index.html@e04ac923`, `app/static/js/app.js` | yes |
| C4 | VALUE / ASSURANCE | Песочница RunnerService: безопасный запуск тестов во временном каталоге, блокировка опасных импортов/вызовов через AST, прерывание по таймауту 5.0с | Выполнение вредоносного кода (`os.system`), зависание процесса сервера на `while True` | `app/services/runner.py`, `app/services/ast_validator.py`, `tempfile.TemporaryDirectory` | Windows 11, Subprocess Python 3.12 | Pytest exit codes, AST parse tree, subprocess timeout | `app/services/runner.py@e04ac923`, `tests/test_runner.py` | yes |
| C5 | VALUE | Инженерная документация: `docs/architecture.md` (Clean Architecture и модель угроз) и `docs/domain_model_uml.md` (UML Avtobys и схема БД) | Отсутствие ясности в архитектуре для преподавателя и студентов | `docs/architecture.md`, `docs/domain_model_uml.md` | Markdown reader | Полнота содержания, соответствие D1–D4 | `docs/@e04ac923` | yes |
| C6 | ASSURANCE | Полное тестовое покрытие и качество кода: 15 тестов `pytest` проходят успешно, `ruff check .` чист | Регрессии, дефекты реализации, скрытые ошибки стиля | `tests/`, `pyproject.toml` | pytest 9.1.1, ruff 0.17.0 | Вывод консольных утилит | `tests/@e04ac923`, `EV__OOP_20261015-022500_CORE.md` | yes |
| C7 | VALUE | Non-Goals Isolation: учебный контент Недели 1 отсутствует в кодовой базе | Размытие скоупа архитектурной задачи и преждевременная фиксация учебного контента | Корень репозитория, `content/` | Workspace filesystem | Проверка файловой структуры | Workspace inspection @ e04ac923 | yes |
| C8 | TRACE | Идентичность артефактов и value-bearing accounting: Baseline `5724adc3`, Candidate `e04ac923`, селектор `app/`, `docs/` | Невоспроизводимость сборки, неучтенные изменения кода | Git repository history | Git CLI | `git diff --numstat` replay | Git log / status @ e04ac923 | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1: FastAPI Server & Health API | RF §1 (4, 25), §3 AC-1 | C1 | ✅ |
| AC-2: Database Layer & Models | RF §1 (2, 23), §3 AC-2 | C2 | ✅ |
| AC-3: Zero-Build Frontend Dashboard | RF §1 (5, 26), §3 AC-3 | C3 | ✅ |
| AC-4: RunnerService Sandbox & AST Security | RF §1 (3, 24), §3 AC-4 | C4 | ✅ |
| AC-5: Documentation Deliverables | RF §1 (6, 27), §3 AC-5 | C5 | ✅ |
| AC-6: Automated Testing & Ruff Cleanliness | RF §1 (7, 28), §3 AC-6 | C6 | ✅ |
| AC-7: Non-Goals Isolation | RF §3 AC-7 | C7 | ✅ |
| Accounting Contract (TS §4) | RF §1 Accounting Table | C8 | ⚠️ partial (числовые расхождения в формулировке RF: 1184 vs 991 LOC, 19 vs 21 файлов; функционально селектор и бюджет соблюдены) |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1 | Запуск FastAPI TestClient по эндпоинтам `/api/health`, `/`, `/docs` | Транспортный фундамент системы, критичен для UI | Нет прямого E2E сетевого теста на внешнем порту (запуск через TestClient достаточен) |
| C2 | Проверка создания БД, CRUD-операций и связей моделей `Student`, `TopicProgress`, `Submission` | Персистентность образовательного прогресса | SQLite single-file concurrency (достаточен для локальной работы) |
| C3 | Инспекция шаблона `index.html`, скрипта `app.js`, стилей `style.css`, проверка отсутствия `package.json` | Прямое требование пользователя по Zero-Build | CDN-ресурсы требуют доступности интернета при первом открытии |
| C4 | Запуск тестов песочницы: нормальное решение, провал теста, таймаут `while True`, блокировка опасных импортов/вызовов через AST | Критический рубеж безопасности при локальном запуске кода | AST не защищает от обхода через глубокое метапрограммирование `object.__subclasses__`, но для локального учебного курса защита достаточна |
| C5 | Проверка полноты и структуры документов в `docs/` | Требование к сдаче проекта преподавателю | Нет |
| C6 | Полный прогон `pytest -v` и `ruff check .` | Базовая гарантия надежности кодовой базы | Нет |
| C7 | Сканирование рабочей директории на отсутствие контента Недели 1 | Контрактное ограничение Non-Goal | Нет |
| C8 | Replay `git diff --numstat` против Baseline `5724adc3` и Candidate `e04ac923` | Проверка бухгалтерской дисциплины TFW | Расхождение в декларированном RF числе файлов (19 vs 21) и LOC (1184 vs 991) |

## Deviations from TS

1. **Accounting text discrepancy**:
   - В TS §4 в таблице указано "19 planned files" и "~1200 LOC (+1200 / -0)", хотя в списке выше перечислено 19 файлов в `app/` и 2 файла в `docs/` (итого 21 файл).
   - В RF §1 указано: "19 файлов: ... (в списке перечислено 21 файл)", и заявлено "1184 adds + 0 deletes = 1184 touched text LOC".
   - Фактический вывод команды `git diff --numstat 5724adc3..e04ac923 -- app/ docs/` дает ровно 21 файл и 991 добавленную строку.
   - Это текстовое расхождение не является материальным функциональным дефектом, так как фактический результат полностью укладывается в утвержденный бюджет триггеров (<50 файлов, <5000 LOC).

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
