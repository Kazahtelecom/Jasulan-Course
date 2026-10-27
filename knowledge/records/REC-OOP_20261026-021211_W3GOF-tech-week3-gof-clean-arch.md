# Knowledge record — REC-OOP_20261026-021211_W3GOF-tech-week3-gof-clean-arch: Модуль Недели 3 «Паттерны GoF, Чистая архитектура и изолированный векторный UML»

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261026-021211_W3GOF-tech-week3-gof-clean-arch` |
| Publication intent | Зафиксировать техническое решение по интеграции модуля Недели 3 («Паттерны GoF и Чистая архитектура») в модульное ядро `WeekRegistry`, реализации свободного тренажера с AST-whitelist, математической балансировке квиза на 20 баллов и автономности блоков `<defs>` в SVG-диаграммах |
| Kind | technical-reference decision |
| Statement | В рамках расширения LMS интегрирован заключительный модуль Недели 3: (1) декларативная регистрация `WeekModule(week_number=3, ...)` в `app/modules/registry.py` и `WEEK_TASK_IDS[3]` в `app/services/scoring.py` с сохранением изоляции 4 профилей студентов (`X-Student-Id`) в SQLite WAL; (2) тонкий делегирующий роутер `app/routers/week3.py`, подключенный в `app/main.py`; (3) 4 пошаговых раздела теории в `app/content/week_3/theory.py` с карточками анатомии паттернов и построчным разбором `TransitTerminalFacade` и `TicketIssuer`; (4) 3 задачи тренажёра `w3_task_1..3` в `app/content/week_3/practice.py` (`0.0` б., штраф отсутствует) по связкам Builder + Adapter, Chain of Responsibility + Observer и Clean Architecture Use Case (`ValidateRideUseCase`), совместимые с `ASTValidator` без изменения правил безопасности; (5) итоговый квиз на 10 вопросов `w3_q1..w3_q10` в `app/content/week_3/quiz.py` (`20.0` б., порог `12.0` б.) с доказанным балансом длин вариантов (`max_len / min_len <= 1.0674`, все `>= 89` символов) и концептуальными ловушками; (6) векторная интерактивная схема `#svg-week3` с лупой 2.5× и полностью автономным блоком `<defs>` в `app/templates/components/uml_viewer.html` с исправлением изоляции `<defs>` в диаграммах Недели 2 и архитектуры. |
| Applicability | Проект Web-OOP, модуль Недели 3 (`/week3`, `/api/week3/...`), компоненты `header.html`, `tab_theory.html`, `tab_practice.html`, `uml_viewer.html`, `app.js` и тестовый набор `tests/`. |
| Grounds and uncertainty | Подтверждено независимой верификацией `EV__OOP_20261026-021211_W3GOF.md` (6/6 VERIFIED), 100% зеленым прогоном автотестов `pytest` (55/55 passed без регрессий), выполнением критериев приемки AC-1..AC-5 и жестких ограничений HC-1..HC-3, и вердиктом APPROVE в `REVIEW__OOP_20261026-021211_W3GOF.md`. Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261026-021211_W3GOF/RF__OOP_20261026-021211_W3GOF.md @ 997dfa43b2a6a9292a3528866230005d06e97e28` (§1, §2) и `workspace/2026/OOP_20261026-021211_W3GOF/REVIEW__OOP_20261026-021211_W3GOF.md` (§2, §4) |
| Originating task and unit | `OOP_20261026-021211_W3GOF`, Executor `antigravity:thread:local:a0ce43a2-c346-486b-8642-9ebabb0eb398` / Reviewer `antigravity:thread:local:0577307d-2e09-4d15-bba8-95d7ca0f2e57` |
| Producer | Task Coordinator `antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` via `/tfw-docs` (`Closing and record recovery`) |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`, `TS__OOP_20261026-021211_W3GOF.md @ c0a83bd4f1f915427ccc243d64065008d9eb1169`, утверждение знаменателя скоупа) и независимый `REVIEW__OOP_20261026-021211_W3GOF.md` (`APPROVE`) |
| Completed effect or missing decision | Опубликовать запись технического решения, обновить `KNOWLEDGE.md` (`D12`, `1. Architecture Map`), `README.md` (ссылка на текущую задачу) и чек-лист закрытия в `REVIEW §6`. |
| Relations | Расширяет модульную архитектуру `REC-OOP_20261021-141300_REFAC-tech-modular-weeks` (`D8`), эргономику IDE и балансировку квизов `REC-OOP_20261025-235206_UIEXP-tech-ide-ergonomics-and-quiz-balance` (`D11`), опирается на неизменный белый список безопасности `REC-OOP_20261021-141300_REFAC-tech-sandbox-ast-whitelist` (`D9`) и многопользовательскую изоляцию `REC-OOP_20261021-141300_REFAC-tech-multiuser-and-api-hardening` (`D10`). |

## Source and decision context

В рамках интеграции завершающей Недели 3 курса ООП требовалось охватить ключевые порождающие, структурные и поведенческие паттерны GoF и 4 концентрических слоя Clean Architecture. При реализации решены 4 технические проблемы:
1. Гибридная конфигурация задач практики, сочетающая паттерны разных категорий (Builder + Adapter, Chain of Responsibility + Observer, Use Case + Ports) без дублирования сущностей.
2. Исключение запрещенных правилами песочницы конструкций из исходных лабораторных работ (`import time`, `__new__`, `.__class__.__name__`) с сохранением полной неизменности `ast_validator.py`.
3. Устранение взаимных артефактов скрытых SVG-элементов при переключении табов через внедрение полностью самодостаточных локальных блоков `<defs>` в `#svg-week3`, `#svg-week2` и `#svg-arch`.
4. Сбалансированность вариантов ответов в квизе с ловушками, защищающая от эвристического угадывания.

## Relations and current use

Дополняет `KNOWLEDGE.md §1 Architecture Decisions` как решение `D12`. Завершает цикл разработки модулей программы (Недели 1–3). Вся архитектура готова к приему экзаменационного модуля или проведению учебных сессий со студентами.

## Retry and continuation

Запись сформирована на этапе `KNW` задачи `OOP_20261026-021211_W3GOF` для последующей публикации и финализации задачи в `DONE`.
