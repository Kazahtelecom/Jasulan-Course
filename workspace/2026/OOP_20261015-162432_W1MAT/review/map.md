# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__OOP_20261015-162432_W1MAT.md](../RF__OOP_20261015-162432_W1MAT.md)
> TS: [TS__OOP_20261015-162432_W1MAT.md](../TS__OOP_20261015-162432_W1MAT.md)

## Understanding

Разработан и интегрирован в платформу Web-OOP интерактивный учебный модуль Недели 1 («Основы ООП, инкапсуляция и защита инвариантов») на базе предметной области городской транспортной системы Avtobys. Модуль оформлен в виде единого адаптивного веб-интерфейса с 4 вкладками (`[Лекция]` · `[Квиз]` · `[Практикум]` · `[Лабораторная]`), сохранением черновиков кода в `LocalStorage`, автоматической автопроверкой решений в изолированной песочнице `RunnerService` (с защитой `ASTValidator` и таймаутом 5.0с) и централизованным расчетом суммарного балла (0..20) в SQLite `TopicProgress` (порог сдачи $\ge 12$ баллов) по правилу High-Water Mark ($\max$). Объем модуля строго откалиброван под академическую норму 3 часа учебной нагрузки второкурсника.

## Accepted Claims and Boundaries

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | Теоретический лонгрид лекции: нарратив Chaos → Structure, Rich vs Anemic Domain Model, защита инвариантов и синтаксис `@property` в Python 3.12, 2 диаграммы Mermaid.js (Class Diagram, Sequence Diagram) | Студенты не поймут разницу между процедурным подходом и ООП; непонимание домена Avtobys | `app/content/week_1/lecture.py`, `app/templates/week1.html`, `app/routers/week1.py` | Modern Browser (Tailwind CDN, Mermaid CDN), Python 3.12 | Pytest content check, визуальная проверка структуры | `app/content/week_1/lecture.py@10b8cfb5`, `tests/test_week1_content.py` | yes |
| C2 | VALUE | Интерактивный квиз: 5 концептуальных вопросов с 4 опциями и методическими пояснениями; серверная валидация через `POST /api/week1/quiz/check`; пропорциональное начисление до 3.0 баллов | Студенты спишут ответы через DevTools при клиентской проверке; некорректная оценка теории | `app/content/week_1/quiz.py`, `app/routers/week1.py`, `app/services/scoring.py` | FastAPI TestClient, SQLite DB | HTTP 200 JSON contract, формула баллов 3.0 max | `app/content/week_1/quiz.py@10b8cfb5`, `tests/test_week1_routes.py` | yes |
| C3 | VALUE / ASSURANCE | Практикум `TransitCard`: стартовый шаблон, сьют из 7 автотестов инвариантов (баланс $\ge 0$, пополнение $\ge 100$ ₸, расчет скидки, блокировка, нехватка средств); начисление до 7.0 баллов через RunnerService | Студенты пропустят инварианты состояния; обход правил тарификации; начисление неверных баллов | `app/content/week_1/practice.py`, `app/routers/week1.py`, `app/services/runner.py` | Windows 11, Subprocess Python 3.12, pytest 9.1.1 | Pytest exit codes, runner output | `app/content/week_1/practice.py@10b8cfb5`, `tests/test_week1_routes.py` | yes |
| C4 | VALUE / ASSURANCE | Лабораторная работа №1 `SingleTripTicket` и `Bus`: приватное поле `_is_validated` со свойством readonly `@property is_validated` без сеттера; защита от повторного использования (`TicketAlreadyUsedError`); срок годности 60 мин (`TicketExpiredError`); сьют из 10 автотестов (до 10.0 баллов) | Нарушение инкапсуляции через прямой сеттер `ticket.is_validated = False`; повторный проезд по одному билету; проезд по просроченному билету | `app/content/week_1/lab.py`, `app/routers/week1.py`, `app/services/runner.py` | Windows 11, Subprocess Python 3.12, pytest 9.1.1 | Pytest exit codes, runner output, AttributeError test | `app/content/week_1/lab.py@10b8cfb5`, `tests/test_week1_routes.py` | yes |
| C5 | VALUE | Служба `scoring.py`: суммирование баллов $\text{Total} = \text{Quiz} (0..3) + \text{Practice} (0..7) + \text{Lab} (0..10) \in [0, 20]$; High-Water Mark правило $\max$; статус `is_completed=True` при $\ge 12$ баллах; логирование в `Submission` | Потеря баллов студента при повторной отправке; превышение диапазона 0..20; отсутствие зачета при 12 баллах | `app/services/scoring.py`, `app/models/`, SQLite DB | SQLite 3, SQLAlchemy 2.0 | Юнит-тесты scoring, DB query assertions | `app/services/scoring.py@10b8cfb5`, `tests/test_scoring.py` | yes |
| C6 | VALUE | Zero-Build UI: 4 вкладки на `/week1`, автосохранение черновиков кода в `LocalStorage` (`web_oop_w1_practice_code`, `web_oop_w1_lab_code`), бейдж успеваемости в шапке, карточка модуля Недели 1 на главной странице `/`. Запрет `package.json` и `node_modules` | Потеря написанного студентом кода при закрытии вкладки; нарушение Zero-Build принципа | `app/templates/week1.html`, `app/static/js/week1.js`, `app/templates/index.html` | Современный браузер с CDN | DOM inspection, отсутствие node_modules в git | `app/templates/week1.html@10b8cfb5`, `app/static/js/week1.js` | yes |
| C7 | VALUE / ASSURANCE | Безопасность песочницы RunnerService: ASTValidator блокирует опасные импорты (`os`, `sys`, `subprocess`) и вызовы (`eval`, `open`) со статусом `SECURITY_VIOLATION`; бесконечный цикл прерывается по таймауту 5.0с (`TIMEOUT`) | Выполнение неавторизованного кода на машине преподавателя/студента; зависание сервера | `app/services/runner.py`, `app/services/ast_validator.py` | Windows 11, Subprocess Python 3.12 | AST parse tree, subprocess timeout | `app/services/runner.py@10b8cfb5`, `tests/test_runner.py` | yes |
| C8 | ASSURANCE | Полное тестовое покрытие и качество кода: 30/30 тестов `pytest` проходят (15 ядра + 15 Недели 1), `ruff check .` чист | Регрессии платформенного ядра, дефекты нового контента, скрытые синтаксические ошибки | `tests/`, `pyproject.toml` | pytest 9.1.1, ruff 0.5.0 | Вывод консольных утилит | `tests/@10b8cfb5`, `EV__OOP_20261015-162432_W1MAT.md` | yes |
| C9 | TRACE | Идентичность артефактов и value-bearing accounting: Baseline `6da8e171e758ea7df91a948d7265ec7112f295fa`, Candidate `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac`, селектор `app/`, `docs/`, 13 VALUE-файлов, 2578 LOC | Несоответствие фактических изменений утвержденному ТЗ; неучтенный код | Git repository history | Git CLI | `git diff --numstat` replay | Git log / status @ 10b8cfb5 | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1: Теоретический модуль лекции с визуализацией Rich vs Anemic и Mermaid-диаграммами | RF §1 (42), §3 AC-1 | C1 | ✅ |
| AC-2: Интерактивный квиз по теории с моментальной проверкой (до 3 баллов) | RF §1 (43), §3 AC-2 | C2 | ✅ |
| AC-3: Практикум `TransitCard` с автопроверкой через RunnerService (до 7 баллов) | RF §1 (44), §3 AC-3 | C3 | ✅ |
| AC-4: Лабораторная работа №1 `SingleTripTicket` и `Bus` с автопроверкой (до 10 баллов) | RF §1 (45), §3 AC-4 | C4 | ✅ |
| AC-5: Сервис `scoring.py` и сохранение суммарного балла в SQLite `TopicProgress` (0..20 б.) | RF §1 (46), §3 AC-5 | C5 | ✅ |
| AC-6: Единый многовкладочный Zero-Build UI, LocalStorage и интеграция с дашбордом | RF §1 (48-50, 60), §3 AC-6 | C6 | ✅ |
| AC-7: Безопасность песочницы RunnerService при запуске решений Недели 1 | RF §1, §3 AC-7 | C7 | ✅ |
| AC-8: Интеграционный тестовый сьют и соответствие линтеру | RF §1 (51-53), §3 AC-8, §4 | C8 | ✅ |
| Accounting Contract (TS §4) | RF §1 Accounting Table | C9 | ✅ |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1 | Запуск `pytest tests/test_week1_content.py -k test_lecture_content_structure`, инспекция текста лекции и шаблона `week1.html` на наличие блоков Mermaid.js | Теория формирует концептуальное понимание инкапсуляции | Mermaid CDN требует доступа к сети для визуализации в реальном браузере |
| C2 | Запуск `pytest tests/test_week1_content.py -k test_quiz` и `tests/test_week1_routes.py -k test_quiz_endpoint`, проверка расчета баллов 5/5 -> 3.0 б. | Защита от списывания, корректность методических пояснений | Нет |
| C3 | Запуск `pytest tests/test_week1_content.py -k test_practice` и `tests/test_week1_routes.py -k test_practice_run`, валидация эталонного решения `TransitCard` | Проверка защиты инвариантов состояния в изолированной песочнице | Временные файлы удаляются сразу после выполнения |
| C4 | Запуск `pytest tests/test_week1_content.py -k test_lab` и `tests/test_week1_routes.py -k test_lab_run`, валидация эталонного решения `SingleTripTicket` и `Bus`, проверка отсутствия сеттера `is_validated` | Инженерное ядро модуля: защита от повторного проезда и истечения срока | Мокирование времени через параметр `issued_at` |
| C5 | Запуск `pytest tests/test_scoring.py`, проверка агрегации 0..20 б., порога $\ge 12$ б., правила $\max$ и логирования в `Submission` | Персистентность успеваемости студентов в БД SQLite | SQLite однопоточный файл |
| C6 | Запуск `pytest tests/test_week1_routes.py -k "test_week1_page_render or test_index_dashboard"`, инспекция `week1.js` на ключи LocalStorage и `app/` на отсутствие `package.json` | Прямое требование пользователя по Zero-Build и UX непрерывности | Браузерный LocalStorage изолирован по origin |
| C7 | Запуск `pytest tests/test_runner.py` и `tests/test_week1_routes.py -k test_practice_run_endpoint` (отправка опасного кода и бесконечного цикла) | Безопасность среды выполнения студенческого кода | ASTValidator не защищает от обхода глубокого метапрограммирования, но достаточен для курса |
| C8 | Запуск полного сьюта `pytest -v` (все 30 тестов) и `ruff check .` | Итоговая надежность и регрессионная стабильность | Нет |
| C9 | Выполнение `git diff --name-status` и `git diff --numstat` против Baseline `6da8e171e758ea7df91a948d7265ec7112f295fa` и Candidate `10b8cfb5f6e78b6d02b163c1330d47aa5d9a93ac` | Бухгалтерская строгость TFW и целостность коммитов | Нет |

## Deviations from TS

No deviations. Все 13 файлов VALUE и 3 файла ASSURANCE точно соответствуют спецификации TS §4. Объем строк (2578 LOC) укладывается в утвержденный предел эскалации 2x (до 2760 LOC) без превышения порогов декомпозиции (50 файлов / 5000 LOC).

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
