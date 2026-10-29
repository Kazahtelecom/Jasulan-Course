# Knowledge record — REC-OOP_20261029-200322_EXAM-tech-final-exam-module: Модуль итогового экзамена курса ООП (100-балльная шкала, режим честности и 2 боевые задачи в песочнице AST)

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261029-200322_EXAM-tech-final-exam-module` |
| Publication intent | Зафиксировать техническое решение по разработке и интеграции модуля итогового экзамена курса ООП (`/exam`), объединяющего теоретический квиз на 20 вопросов (20.0 б.), 2 комплексные практические задачи в песочнице AST (20.0 б.), режим академической честности без готовых решений в DOM, расширение `ScoringService` до классической 100-балльной шкалы (60 б. за недели 1–3 + 40 б. за экзамен) с сохранением High-Water Mark в SQLite WAL для 4 студентов группы. |
| Kind | technical-reference decision |
| Statement | В платформу интегрирован полнофункциональный модуль итоговой аттестации курса ООП: (1) контентный пакет `app/content/exam/` (`quiz.py`, `practice.py`, `__init__.py`), включающий 20 концептуальных вопросов-ловушек по материалам всех 3 недель с доказанным антиугадывательным балансом (`ratio <= 1.120`, по 5 правильных индексов `0..3`, 1.0 б./вопрос) и 2 боевые задачи по 10.0 б. в домене Avtobys (Задача 1: Core Domain & SOLID с DI и инвариантами; Задача 2: Clean Architecture & GoF Facade/Builder/Adapter), строго удовлетворяющие белому списку `ASTValidator` и выполняющиеся в изолированной песочнице `python -I` за < 1.0 с; (2) режим академической честности (No-Cheat Mode): в шаблоне `exam.html` полностью исключена кнопка «✨ Вставить готовое решение», а в `textarea` задач не передаётся атрибут `data-solution`, защищая экзамен от подсмотра решения через DevTools; (3) ядро оценивания `ScoringService`: добавлены константы экзамена (`EXAM_QUIZ_MAX = 20.0`, `EXAM_TASKS_MAX = 20.0`, `EXAM_TOTAL_MAX = 40.0`, `COURSE_TOTAL_MAX = 100.0`, порог сдачи экзамена `20.0` б., порог курса `50.0` б.) с независимой фиксацией топиков `exam_quiz`, `exam_task_1`, `exam_task_2`, `exam_overall` в SQLite WAL и защитой от ухудшения ранее набранных баллов (High-Water Mark); (4) специализированный роутер `app/routers/exam.py`, подключенный в `app/main.py`, и акцентная золотая вкладка `🏆 Экзамен` в `header.html`; (5) расширение клиентского `app.js` поддержкой режима `ACTIVE_WEEK === "exam"` и живой синхронизацией 100-балльного рейтинга; (6) 60 автотестов (включая 5 новых в `tests/test_exam.py`), проходящих со 100% успехом. |
| Applicability | Проект Web-OOP, модуль Экзамена (`/exam`, `/api/exam/...`), сервис `ScoringService`, шаблон `exam.html`, компонент `header.html`, клиентский `app.js` и тестовый набор `tests/`. |
| Grounds and uncertainty | Подтверждено выполнением всех критериев приёмки AC-1 — AC-5 в `EV__OOP_20261029-200322_EXAM.md` (6/6 VERIFIED), 100% зеленым прогоном автотестов `pytest` (60/60 passed), неизменяемым коммитом Candidate `c2b3ef5a2d436ab0214898310ea5c357be7d2b85` и вердиктом APPROVE в `REVIEW__OOP_20261029-200322_EXAM.md`. Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261029-200322_EXAM/RF__OOP_20261029-200322_EXAM.md @ c2b3ef5a2d436ab0214898310ea5c357be7d2b85` (§1, §2) и `workspace/2026/OOP_20261029-200322_EXAM/REVIEW__OOP_20261029-200322_EXAM.md` (§2, §4) |
| Originating task and unit | `OOP_20261029-200322_EXAM`, Executor `antigravity:thread:local:12f97fb2-4520-4e67-944b-5743e89747a4` / Reviewer `antigravity:thread:local:58fb2692-2db0-4872-a489-18219b8e72a0` |
| Producer | Task Coordinator `antigravity:thread:local:7dc123a4-589f-4ee8-b43d-a035a4018225` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` via `/tfw-docs` (`Closing and record recovery`) |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261029-200322_EXAM.md @ aeaab61f557a754d8e4a6bd0534eb532e8a6d061`, `TS__OOP_20261029-200322_EXAM.md @ 832bd170327d47637565efa574d2ac1145e23774`) и независимый `REVIEW__OOP_20261029-200322_EXAM.md` (`APPROVE`) |
| Completed effect or missing decision | Опубликовать запись технического решения, обновить `KNOWLEDGE.md` (`D13`, `F11`, `1. Architecture Map`), `README.md` (статус экзамена) и чек-лист закрытия в `REVIEW §6`. |
| Relations | Опирается на модульную архитектуру `WeekRegistry` (`D8`), правила безопасности песочницы AST Whitelist (`D9`), профили 4 студентов в SQLite WAL (`D10`), эргономику редактора кода IDE (`D11`) и контент Недели 3 (`D12`). Завершает формирование полного учебного цикла платформы Web-OOP. |

## Source and decision context

В рамках итоговой аттестации курса ООП требовалось создать завершающий экзаменационный модуль, связывающий концепции всех 3 недель:
1. Синтез 20 теоретических вопросов с концептуальными ловушками и математическим антиугадывательным балансом.
2. Проектирование 2 боевых задач со сквозным доменным сюжетом Avtobys, требующих самостоятельного написания чистого объектно-ориентированного кода.
3. Обеспечение честности сдачи через исключение кнопок и скрытых атрибутов готового решения из клиентского кода.
4. Доведение итоговой шкалы курса до 100 баллов (60 баллов за 3 недели + 40 баллов за экзамен).

## Relations and current use

Дополняет `KNOWLEDGE.md §1 Architecture Decisions` как решение `D13` и `§4 Project Facts` как факт `F11`. Полностью закрывает целевой скоуп экспресс-курса ООП для 4 студентов группы.

## Retry and continuation

Запись сформирована на этапе `KNW` задачи `OOP_20261029-200322_EXAM` для финализации задачи и перевода в `DONE`.
