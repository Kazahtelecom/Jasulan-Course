# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__OOP_20261026-021211_W3GOF.md](../RF__OOP_20261026-021211_W3GOF.md)
> TS: [TS__OOP_20261026-021211_W3GOF.md](../TS__OOP_20261026-021211_W3GOF.md)

## Understanding

В рамках задачи `OOP_20261026-021211_W3GOF` в платформу Web-OOP интегрирован заключительный 3-й учебный модуль («Паттерны GoF и Чистая архитектура») на сквозном домене Avtobys, завершающий 3-недельную программу курса ООП для второкурсников. Модуль включает 4 пошаговых раздела лекционной теории с анатомическими карточками, интерактивную векторную UML-схему `#svg-week3` с лупой 2.5× и локальным `<defs>`, 3 задачи тренажёра (`w3_task_1..3`, `0.0` б.) с готовым решением без потери баллов, и итоговый квиз на 10 вопросов (`20.0` б., порог `12.0` б.) с доказанным математическим балансом вариантов ответа (`<= 1.65`). Реализация охватывает 19 логических файлов `VALUE` (16 текстовых + 3 бинарных Cyberpunk-иллюстрации), 4 тестовых файла `ASSURANCE` (55/55 тестов пройдено без регрессий) с соблюдением нативной безопасности `ASTValidator` и изоляцией 4 профилей студентов в SQLite WAL.

## Accepted Claims and Boundaries

Map the result before selecting checks. Safety/security, human acceptance authority and
accepted-result identity are mandatory even when no ordinary claim sample selects them.

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | Пакет `app/content/week_3/` (`__init__.py`, `theory.py`, `practice.py`, `quiz.py`) и 3 Cyberpunk-иллюстрации в `app/static/images/` полно и корректно представляют программу Лекций 6–9 и Лабораторных 6–9 | Битые ссылки, пустые разделы теории, отсутствие разбора кода или 404 на изображениях | `app/content/week_3/`, `app/static/images/` | Python 3.12, локальный веб-сервер | TS §5 AC-1, структура данных контента | `E1` in `EV__OOP_20261026-021211_W3GOF.md@997dfa4` | yes |
| C2 | VALUE | Модуль Недели 3 зарегистрирован в `WeekRegistry`, задачи добавлены в `ScoringService.WEEK_TASK_IDS[3]`, роутер `week3.py` смонтирован, прогресс 4 студентов изолирован в SQLite WAL | Ошибка 404 на `/week3` и `/api/week3/...`, откат на задачи Недели 1 в подсчете баллов, перезапись чужого прогресса | `app/modules/registry.py`, `app/services/scoring.py`, `app/routers/week3.py`, `data/web_oop.db` | FastAPI, SQLite WAL | TS §5 AC-2, `tests/test_week3.py`, `tests/test_week_modules.py` | `E2` in `EV__OOP_20261026-021211_W3GOF.md@997dfa4` | yes |
| C3 | VALUE | UI-шаблоны (`header`, `tab_theory`, `tab_practice`) и интерактивный просмотрщик с лупой 2.5× (`uml_viewer.html`, `app.js`) поддерживают Неделю 3 и имеют самодостаточный блок `<defs>` | Заблокированная кнопка в шапке, отображение SmartCard из Недели 1, исчезновение стрелок и теней в `#svg-week3` при скрытых вкладках | `app/templates/components/`, `app/static/js/app.js` | Браузер / Jinja2 SSR | TS §5 AC-3, `tests/test_uml_viewer.py`, `tests/test_ui_ergonomics.py` | `E3` in `EV__OOP_20261026-021211_W3GOF.md@997dfa4` | yes |
| C4 | VALUE / ASSURANCE | Эталонные решения `reference_solution` для `w3_task_1..3` успешно проходят нативную песочницу `RunnerService` (`python -I -m pytest`), тренажер имеет вес `0.0` б., а `ASTValidator` не изменялся | Падение задач в песочнице, блокировка по таймауту (>5 с), RCE-уязвимость или ослабление белого списка AST | `app/content/week_3/practice.py`, `app/services/ast_validator.py`, `app/services/runner.py` | Python 3.12 subprocess, pytest | TS §4 HC-1, TS §5 AC-4, `tests/test_week3.py`, `tests/test_ast_validator.py` | `E4` in `EV__OOP_20261026-021211_W3GOF.md@997dfa4` | yes |
| C5 | VALUE / ASSURANCE | Вопросы квиза `w3_q1..w3_q10` удовлетворяют строгим математическим инвариантам баланса (`min_len >= 60`, `max_len / min_len <= 1.65`, правильные индексы по 2–3 раза, >=5/10 не самые длинные), весь тестовый набор `pytest` проходит (55/55), а документация актуализирована | Угадывание ответов студентами по длине, регрессии функциональности Недель 1 и 2, рассинхронизация архитектурной документации | `app/content/week_3/quiz.py`, `docs/domain_model_uml.md`, `docs/architecture.md`, `tests/` | pytest 9.1.1 | TS §4 HC-2, TS §5 AC-5, `tests/test_ui_ergonomics.py` | `E5` in `EV__OOP_20261026-021211_W3GOF.md@997dfa4` | yes |
| C6 | TRACE / ACCOUNTING | Бухгалтерский учет `VALUE`: ровно 19 логических файлов (16 текстовых + 3 бинарных), Baseline commit `c0a83bd4`, Candidate commit `997dfa4`, 2588 затронутых строк `VALUE` (в пределах 2× эскалации 4360 LOC), однофазное исполнение | Выход за рамки утвержденного скоупа, недостоверность Candidate, скрытые сторонние изменения | Репозиторий Git, NUL-safe diff | Git revision graph, TS §4, conventions.md §6 | `E-accounting` in `EV__OOP_20261026-021211_W3GOF.md@997dfa4` | yes |
| C7 | MANDATORY BOUNDARY (Security) | Строгая нативная безопасность песочницы: отсутствие `import time`, `import re`, `__new__`, `.__class__.__name__` в задачах, неизменность `ASTValidator`, сохранение Zero-Build | Побег из песочницы, DoS-атака или нарушение чистоты развертывания | `app/services/ast_validator.py`, код задач Недели 3 | AST parser, pytest | HL §6 DoF #2, HL §7 P4, TS §4 HC-1 | `tests/test_sandbox_security.py`, `tests/test_ast_validator.py` | yes |
| C8 | MANDATORY BOUNDARY (Human Authority & Result Identity) | Утверждение владельцем `zhasulan` спецификации TS и знаменателя бюджета на коммите `c0a83bd4`; фиксация `Candidate` `997dfa4` до создания EV/RF; соблюдение Role Lock | Неавторизованные изменения контрактов, искажение границ ответственности ролей | Git history, `status.md`, `journal/` | Git log, TFW convention | Commits `c0a83bd4`, `997dfa4`, `f5e9254` | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1 (Контент Недели 3 и иллюстрации) | RF §1 New Files, §3 AC-1, §5 Evidence E1 | C1 | ✅ Aligned |
| AC-2 (Регистрация, роутинг, изоляция 4 студентов) | RF §1 Modified Files, §3 AC-2, §5 Evidence E2 | C2 | ✅ Aligned |
| AC-3 (UI-шаблоны и SVG UML с лупой 2.5×) | RF §1 Modified Files, §3 AC-3, §5 Evidence E3 | C3 | ✅ Aligned |
| AC-4 (Исполняемость задач тренажера и `ASTValidator`) | RF §1, §2 Key Decisions, §3 AC-4, §5 Evidence E4 | C4, C7 | ✅ Aligned |
| AC-5 (Баланс квиза, полный прогон `pytest`, документация) | RF §3 AC-5, §4 Verification, §5 Evidence E5 | C5 | ✅ Aligned |
| TS §4 Accounting Contract (19 файлов, Baseline/Candidate, LOC) | RF §1 Actual Value-Bearing Accounting, E-accounting | C6 | ✅ Aligned |
| TS §7 DoF / Hard Constraints (HC-1, HC-2, HC-3) | RF §2 Key Decisions, §3 AC-1..AC-5 | C3, C4, C5, C7 | ✅ Aligned |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1, C2, C3 | Независимая инспекция кода `app/content/week_3/`, шаблонов, роутеров, а также запуск `pytest tests/test_week3.py tests/test_week_modules.py tests/test_uml_viewer.py -v` | Проверка целостности контента, корректности монтирования роутов и изоляции профилей | None |
| C4, C7 | Независимый прогон тестов песочницы `pytest tests/test_runner.py tests/test_sandbox_security.py tests/test_ast_validator.py -v` и инспекция `git diff c0a83bd4 997dfa4 -- app/services/ast_validator.py` | Обязательный рубеж безопасности: подтверждение неизменности белого списка и защиты от побега из песочницы | None |
| C5 | Независимый запуск `pytest tests/test_ui_ergonomics.py -v` и полный прогон `pytest -v` по всему репозиторию; инспекция `docs/domain_model_uml.md` и `docs/architecture.md` | Математическая верификация длин вариантов ответа (порог `<= 1.65`) и подтверждение 0 регрессий | None |
| C6, C8 | Независимый запуск PowerShell NUL-safe diff проверки Baseline (`c0a83bd4`) -> Candidate (`997dfa4`) по 19 путям `$valuePaths`, проверка `git log`, `status.md` и журнала | Верификация отсутствия дрифта скоупа и соблюдения неизменяемого знаменателя бюджета | None |

## Deviations from TS

No deviations. (Все 19 файлов `VALUE` соответствуют утвержденному селектору TS §4; фактический объем 2588 LOC находится внутри утвержденного лимита эскалации 4360 LOC).

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
