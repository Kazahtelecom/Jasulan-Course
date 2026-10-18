# Knowledge record — REC-OOP_20261018-222800_W2SOL-tech-week2-multiweek: Мультинедельная архитектура платформы и модуль Недели 2 (SOLID и DI)

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261018-222800_W2SOL-tech-week2-multiweek` |
| Publication intent | Зафиксировать техническое решение по обслуживанию нескольких недель курса единым шаблоном и сервисом оценивания (`app/content/week_2/`, `app/routers/week2.py`, `app/services/scoring.py`, `app/templates/index.html`, `app/static/js/app.js`) |
| Kind | technical-reference decision |
| Statement | Неделя 1 (`/week1`) и Неделя 2 (`/week2`) используют один шаблон `app/templates/index.html` и один скрипт `app/static/js/app.js`; активная неделя передается через `data-active-week` на `<body>` (`active_week` в контексте роутера), а клиент обращается к `/api/week{N}/...` и хранит черновики кода под ключом `weboop_w{N}_draft_`. `ScoringService` принимает `week_number: int = 1` и реестр `WEEK_TASK_IDS` (`1: task_1..3`, `2: w2_task_1..3`), поэтому прогресс недель изолирован префиксами `topic_id` (`week_1*`, `week_2*`) без миграции схемы БД; каждая неделя оценивается только по квизу (`10 × 2.0 = 20.0` б., порог `12.0` б., High-Water Mark), тренажер дает `0.0` б. Новая неделя добавляется пакетом `app/content/week_N/` (`theory`, `practice`, `quiz`), роутером `weekN.py` и записью в `WEEK_TASK_IDS`. |
| Applicability | Проект `Web-OOP`, модули Недели 1 и Недели 2, начиная с Candidate `120f4bab124360860918d45e683b0f3f92b7bf16`; применять при проектировании Недели 3. |
| Grounds and uncertainty | Подтверждено 24 автотестами (`pytest -v`, включая `tests/test_week2.py` с негативным контролем тренажера, границами `10.0 / 12.0` и двусторонней изоляцией недель), `ruff check .`, `EV__OOP_20261018-222800_W2SOL.md` (`5/5 VERIFIED`) и независимым ревью `REVIEW__OOP_20261018-222800_W2SOL.md @ a815df79b998d7ffe3375635bd7d882a5daa0da9` (`APPROVE`, `0 findings`). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261018-222800_W2SOL/RF__OOP_20261018-222800_W2SOL.md @ 619bbc4caa5565f6d922f1dff57e7b6b7d27a575` (§1, §2) и `workspace/2026/OOP_20261018-222800_W2SOL/REVIEW__OOP_20261018-222800_W2SOL.md @ a815df79b998d7ffe3375635bd7d882a5daa0da9` (§2, §4) |
| Originating task and unit | `OOP_20261018-222800_W2SOL`, Executor `antigravity:thread:local:5aed77d4-7d1f-4fab-86a0-98a05917871c` / Reviewer `antigravity:thread:local:63e77ece-bb55-4133-9266-efddbfa3111c` |
| Producer | Coordinator `antigravity:thread:local:1da46223-edb5-410d-bad6-cd3c36954a1f` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` (`antigravity:thread:local:1da46223-edb5-410d-bad6-cd3c36954a1f`) via `/tfw-docs` |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261018-222800_W2SOL.md @ 42ab6ed77da69a08f17a4796701fd32064043b01`, `TS__OOP_20261018-222800_W2SOL.md @ 8782364c17f85ef19425121fb9f4ae0d7bdc3eb3`) и независимый `REVIEW__OOP_20261018-222800_W2SOL.md @ a815df79b998d7ffe3375635bd7d882a5daa0da9` |
| Completed effect or missing decision | Опубликована запись технического решения и обновлены `KNOWLEDGE.md` (`D7`, `Key Artifacts`) и `CHANGELOG.md`; открытых решений нет. |
| Relations | Scoped expansion of `REC-OOP_20261018-213107_W1MAT-tech-week1-funnel` (`KNOWLEDGE.md D6`): обобщает одномодульный шаблон Недели 1 до параметризованного по неделе; поведение Недели 1 не изменено. |

## Source and decision context

Для Недели 2 вместо дублирования `index.html` и `app.js` выбрана параметризация по номеру недели: значение по умолчанию `week_number = 1` сохранило обратную совместимость всех тестов Недели 1. Строка `mermaid.min.js` отсутствует в HTML, а комментарий со ссылкой на `docs/domain_model_uml.md` оставлен для совместимости с `tests/test_health.py`. Сквозной кейс Недели 2 — терминал Avtobys: `StandardFareService` (`100 ₸`) и `StudentFareService` (`50 ₸`), `CardPayment` и `BluetoothPayment` с общим контрактом `pay(amount)`, `TerminalValidator(fare_service, payment_method)` с Constructor Injection.

## Relations and current use

Дополняет `KNOWLEDGE.md §1 Architecture Map` (`D6`, `D7`). Для Недели 3 следует добавить `app/content/week_3/`, `app/routers/week3.py` и запись в `WEEK_TASK_IDS`, не меняя шаблон и логику недель 1–2.

## Retry and continuation

Запись завершена и синхронизирована с `KNOWLEDGE.md` на этапе закрытия `KNW -> DONE` задачи `OOP_20261018-222800_W2SOL`.
