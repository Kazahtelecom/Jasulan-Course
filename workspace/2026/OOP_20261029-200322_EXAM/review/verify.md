# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | Несбалансированные вопросы, угадывание, сбой скоринга | `app/content/exam/quiz.py`, `app/content/exam/__init__.py` | Python 3.12, pytest 9.1.1 | TS §5 AC-1, `tests/test_exam.py` | Нет | Независимый запуск `test_exam_quiz_balance_and_evaluation` и аудит структуры вопросов |
| C2 | Сбой AST-песочницы, таймаут, нерабочий эталонный код | `app/content/exam/practice.py`, `app/services/runner.py`, `ast_validator.py` | Python 3.12, `python -I` subprocess | TS §5 AC-2, `tests/test_exam.py` | Нет | Независимый запуск `test_exam_practice_tasks_in_sandbox` и проверка белого списка AST |
| C3 | Искажение оценок, регрессия High-Water Mark, выход за 100 б. | `app/services/scoring.py`, `app/routers/scoring.py` | SQLite WAL (`data/web_oop.db`) | TS §5 AC-3, `tests/test_exam.py` | Нет | Независимый запуск `test_scoring_grand_total_100` и проверка граничных условий скоринга |
| C4 | Списывание решений студентами через UI или DOM | `app/templates/exam.html`, `app/templates/components/header.html` | Jinja2, DOM/HTML5 | TS §5 AC-4, `tests/test_exam.py` | Нет | Независимый запуск `test_exam_ui_integrity` и строгий текстовый поиск готовых решений в шаблонах |
| C5 | Взаимное повреждение данных студентов, регрессии недель 1–3 | `tests/`, `data/web_oop.db` | Python 3.12, pytest 9.1.1 | TS §5 AC-5, full pytest suite | Нет | Полный прогон `pytest tests/` (все 60 тестов) |
| C6 | Неучтенные файлы, превышение лимитов декомпозиции | Git repository, `git diff` | Git CLI on Windows | TS §4, EV §2 E-accounting | Нет | Прогон `git diff --numstat` между утвержденным коммитом и Candidate |
| C7 | Нарушение контрактной дисциплины и независимости | `status.md`, `HL`, `TS`, `RF` | TFW protocol | HL §4.1, conventions.md | Нет | Аудит идентификаторов сессии, путей и неизменяемых рефов |

Safety/security, human acceptance authority and accepted-result identity are mandatory floors.
Expand verification when an observed fact changes a mapped claim, dependency, risk or evidence gap;
the existence or count of discrepancies never selects depth by itself.

## Verification Log

### V1: C1 — Теоретический квиз экзамена
- **Accepted claim / authority:** Ровно 20 вопросов, охват Недель 1–3, соотношение длин вариантов `<= 1.65`, ровно по 5 правильных вариантов на каждый индекс 0..3, скоринг 1.0 б./вопрос (20.0 б. макс, порог 12.0 б.).
- **Subject tuple:** `app/content/exam/quiz.py@c2b3ef5a2d436ab0214898310ea5c357be7d2b85`, Python 3.12, TS §5 AC-1, clean state.
- **Action or evidence:** Запуск `pytest tests/test_exam.py -k test_exam_quiz_balance_and_evaluation -v` и инспекция `quiz.py`.
- **Observed:** 20 вопросов загружены. Соотношение длин вариантов `<= 1.120` (лимит `<= 1.65`). Индексы правильных ответов распределены строго равномерно: `{0: 5, 1: 5, 2: 5, 3: 5}`. Оценка 20/20 дает 20.0 б. (`is_passed=True`), 10/20 дает 10.0 б. (`is_passed=False`), 12/20 дает 12.0 б. (`is_passed=True`). Тест PASSED.
- **Limit:** None.
- **Result:** HOLDS

### V2: C2 — Практические задачи экзамена в песочнице AST
- **Accepted claim / authority:** 2 связанные задачи (`exam_task_1`, `exam_task_2`) по 10.0 б. со стартовым кодом и эталонными решениями, строгий белый список AST, исполнение в песочнице < 5.0 с.
- **Subject tuple:** `app/content/exam/practice.py@c2b3ef5a2d436ab0214898310ea5c357be7d2b85`, Python 3.12 `python -I` subprocess, TS §5 AC-2, clean state.
- **Action or evidence:** Запуск `pytest tests/test_exam.py -k test_exam_practice_tasks_in_sandbox -v` и проверка `ASTValidator.validate`.
- **Observed:** Обе задачи строго удовлетворяют белому списку AST (`is_safe=True, error=None`). В песочнице тесты выполняются со статусом `PASSED`: `exam_task_1` (5 тестов passed за ~0.75с), `exam_task_2` (3 теста passed за ~0.64с). Время запуска < 5.0с. Тест PASSED.
- **Limit:** None.
- **Result:** HOLDS

### V3: C3 — Скоринг и 100-балльная шкала курса
- **Accepted claim / authority:** `ScoringService` начисляет до 40.0 б. за экзамен, рассчитывает `Grand Total = W1(20) + W2(20) + W3(20) + Exam(40) = 100.0 б.`, защита High-Water Mark при повторных попытках.
- **Subject tuple:** `app/services/scoring.py@c2b3ef5a2d436ab0214898310ea5c357be7d2b85`, SQLite 3 WAL, TS §5 AC-3, clean state.
- **Action or evidence:** Запуск `pytest tests/test_exam.py -k test_scoring_grand_total_100 -v`.
- **Observed:** Исходное состояние: 0.0 б. При сдаче Недель 1-3: 58.0 / 60.0 б. При сдаче Экзамена: Задачи 20.0 б. + Квиз 18.0 б. = 38.0 / 40.0 б. Итоговый балл: 96.0 / 100.0 б. (`A (Отлично)`, `is_course_completed=True`). Повторные сдачи с меньшими баллами (10.0 б. квиз, упавший код задачи) не снижают зафиксированный балл. Тест PASSED.
- **Limit:** None.
- **Result:** HOLDS

### V4: C4 — Режим академической честности и UI
- **Accepted claim / authority:** Активная ссылка `🏆 Экзамен` в `header.html`, полное скрытие кнопки «Показать готовое решение» и атрибута `data-solution` на `/exam`.
- **Subject tuple:** `app/templates/exam.html@c2b3ef5a2d436ab0214898310ea5c357be7d2b85`, Starlette TestClient / Jinja2, TS §5 AC-4, clean state.
- **Action or evidence:** Запуск `pytest tests/test_exam.py -k test_exam_ui_integrity -v` и текстовый поиск `fillSolutionCode` / `data-solution` в `app/templates/exam.html`.
- **Observed:** GET `/exam` возвращает HTTP 200 OK. В шапке присутствует акцентная вкладка `<a href="/exam">🏆 Экзамен</a>`. В разметке `exam.html` полностью отсутствуют кнопка «Вставить готовое решение», функция `fillSolutionCode` и атрибуты `data-solution` в полях textarea. Сводная ведомость отображает компоненты семестра и экзамена. Тест PASSED.
- **Limit:** None.
- **Result:** HOLDS

### V5: C5 — Изоляция 4 студентов и сквозная регрессионная надежность
- **Accepted claim / authority:** Независимый прогресс для 4 студентов (`zhasulan`, `roman`, `arseniy`, `saubakirov`) в SQLite WAL, 100% прохождение всех тестов платформы.
- **Subject tuple:** Full repository test suite, Python 3.12, SQLite WAL, TS §5 AC-5, clean state.
- **Action or evidence:** Запуск `pytest tests/test_exam.py -k test_multi_student_isolation_and_exam_endpoints -v` и полный прогон `pytest tests/`.
- **Observed:** Тест изоляции студентов успешно подтвердил независимость прогресса каждого студента. Полный прогон тестового набора дал **60 passed из 60 тестов (100% pass)** за 20.21с без единого сбоя.
- **Limit:** None.
- **Result:** HOLDS

### V6: C6 — Бухгалтерский учет и Candidate
- **Accepted claim / authority:** NUL-safe diff между утвержденным коммитом и Candidate составляет ровно утвержденные файлы в рамках бюджета LOC.
- **Subject tuple:** Git commit `832bd170327d47637565efa574d2ac1145e23774` -> `c2b3ef5a2d436ab0214898310ea5c357be7d2b85`, Git CLI, TS §4, clean state.
- **Action or evidence:** Запуск `git diff --numstat 832bd170327d47637565efa574d2ac1145e23774 c2b3ef5a2d436ab0214898310ea5c357be7d2b85`.
- **Observed:** 10 файлов `VALUE` (2228 add / 4 del = 2232 touched LOC), 1 файл `ASSURANCE` (333 LOC), 1 файл `TRACE` (74 LOC ONB). Все пути строго соответствуют селектору TS §4. Объем 2232 LOC существенно ниже триггера декомпозиции (5000 LOC, 50 файлов).
- **Limit:** None.
- **Result:** HOLDS

### V7: C7 — Мандат, авторитет и независимость
- **Accepted claim / authority:** Неизменяемый знаменатель владельца задачи `zhasulan` соблюден, роль Reviewer сохранена, переходы состояний зафиксированы в journal.
- **Subject tuple:** `status.md`, `HL-OOP_20261029-200322_EXAM.md`, `TS__OOP_20261029-200322_EXAM.md`, `journal/`.
- **Action or evidence:** Аудит контрольных файлов и журналов перехода.
- **Observed:** Задача инициирована владельцем `zhasulan` (`owner-direct`), HL заморожен на `aeaab61`, TS утвержден на `832bd17`, переход в `RF` оформлен записью `20261029-205436__transition__b4d9.md`. Reviewer действует независимо.
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `python -m pytest tests/test_exam.py -v` | C1, C2, C3, C4, C5 | 5 passed, 1 warning in 2.23s (exit 0) |
| 2 | `python -m pytest tests/` | C5 | 60 passed, 1 warning in 20.21s (exit 0) |
| 3 | `git rev-parse 832bd17 aeaab61 c2b3ef5 6767fd0` | C6, C7 | Exit 0. Resolved full SHAs: `832bd170327d47637565efa574d2ac1145e23774`, `aeaab61f557a754d8e4a6bd0534eb532e8a6d061`, `c2b3ef5a2d436ab0214898310ea5c357be7d2b85`, `6767fd0fd2c4c61378e61ded2275ca30b0490df5` |
| 4 | `git diff --numstat 832bd170327d47637565efa574d2ac1145e23774 c2b3ef5a2d436ab0214898310ea5c357be7d2b85` | C6 | Exit 0. 2228 add / 4 del (2232 touched text LOC across 10 VALUE files) |
| 5 | `git diff 832bd17 c2b3ef5 \| Select-String -Pattern "(TODO\|FIXME\|XXX\|HACK\|temp\|legacy)"` | C6 | Exit 0. All matched comments are instructional TODO prompts in student starter code or Adapter pattern domain classes; zero deferred agent notes |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | 20 вопросов, баланс длин `<= 1.65`, по 5 на каждый индекс 0..3 | RF §3, EV E1 | `app/content/exam/quiz.py` | ✅ |
| C2 | 2 задачи по 10.0 б., AST-песочница < 5.0 с | RF §3, EV E2 | `app/content/exam/practice.py` | ✅ |
| C3 | Экзамен 40.0 б., общий итог курса 100.0 б., High-Water Mark | RF §3, EV E3 | `app/services/scoring.py` | ✅ |
| C4 | Скрытие готовых решений и атрибута `data-solution` на `/exam` | RF §3, EV E4 | `app/templates/exam.html` | ✅ |
| C5 | Изоляция 4 студентов, 100% pass полного набора тестов (60/60) | RF §3, EV E5 | `tests/test_exam.py`, `tests/` | ✅ |
| C6 | Фактический объем 2232 LOC в 10 файлах VALUE | RF §1, EV E-accounting | `git diff --numstat 832bd17 c2b3ef5` | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | Инвариант баланса опций квиза (`max_len / min_len <= 1.65` и ровно по 5 на индекс 0..3) | Студенты могут угадывать ответы по длине или преобладающему индексу | `test_exam_quiz_balance_and_evaluation` падает с assertion error при дисбалансе длин или индексов | admitted |
| G2 | permanent guard | Белый список AST и ограничение среды исполнения (`ASTValidator` + `RunnerService`) | Выполнение небезопасного кода, инъекции, зависание сервера | `test_exam_practice_tasks_in_sandbox` и `tests/test_sandbox_security.py` проверяют отлов запрещенных импортов и таймауты | admitted |
| G3 | permanent guard | Инвариант High-Water Mark при скоринге экзаменационных попыток | Повторная неудачная попытка студента снижает ранее заработанные баллы | `test_scoring_grand_total_100` явно проверяет отправку заведомо худших результатов (10 б. вместо 18 б., падение теста задачи) | admitted |
| G4 | permanent guard | Режим академической честности на странице экзамена (`exam.html`) | Списывание студентами эталонного кода через UI или инспекцию DOM | `test_exam_ui_integrity` проверяет отсутствие кнопки решения и атрибута `data-solution` | admitted |
| G5 | permanent guard | Изоляция 4 студентов группы в SQLite WAL | Перекрестное загрязнение оценок между студентами | `test_multi_student_isolation_and_exam_endpoints` проверяет независимость баллов 4 профилей | admitted |
| G6 | governance assertion | Бюджет декомпозиции (< 5000 LOC, < 50 файлов) | Необоснованное разрастание однофазной задачи | NUL-safe diff accounting replay | governance only |

## Candidate Findings

| ID | Class | Subject | Affected claim / authority | Observed fact + oracle | Concrete harm | Material consequence or named absence | Owner | Observable completion | Route / rung | Candidate effect | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | TRACE | Хэш коммита согласования TS в RF §1 | Идентичность артефакта согласования TS | В таблице RF §1 указано `832bd17135e5d1ec5cf08a0d7f384a2ca4df9bc4`, тогда как полный SHA коммита `832bd17` равен `832bd170327d47637565efa574d2ac1145e23774` (опечатка в суффиксе хэша после 7 символа). Оракул: `git rev-parse 832bd17`. | Вреда для продукта нет: коммит `832bd17` однозначно разрешается в Git, Candidate `c2b3ef5a2d436ab0214898310ea5c357be7d2b85` и Baseline `aeaab61f557a754d8e4a6bd0534eb532e8a6d061` совпадают посимвольно. | Нематериальное замечание к отчету RF, не влияющее на валидность кода или тестов. | Executor / Coordinator | Фиксация замечания в REVIEW; исправление опечатки при необходимости. | carrier observation | unchanged | observation |

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | E1 | `app/content/exam/quiz.py@c2b3ef5`, Python 3.12, TS §5 AC-1, clean | Repeated (`pytest tests/test_exam.py -k test_exam_quiz_balance_and_evaluation -v`) | ✅ Да, подтверждает 20 вопросов, баланс <= 1.120, равномерность 0..3 и шкалу 20 б. | None |
| E2 | E2 | `app/content/exam/practice.py@c2b3ef5`, Python 3.12, TS §5 AC-2, clean | Repeated (`pytest tests/test_exam.py -k test_exam_practice_tasks_in_sandbox -v`) | ✅ Да, подтверждает выполнение 2 задач в песочнице AST за < 1.0с | None |
| E3 | E3 | `app/services/scoring.py@c2b3ef5`, SQLite 3 WAL, TS §5 AC-3, clean | Repeated (`pytest tests/test_exam.py -k test_scoring_grand_total_100 -v`) | ✅ Да, подтверждает скоринг до 40 б., итог курса до 100 б. и High-Water Mark | None |
| E4 | E4 | `app/templates/exam.html@c2b3ef5`, Jinja2 / DOM, TS §5 AC-4, clean | Repeated (`pytest tests/test_exam.py -k test_exam_ui_integrity -v` + шаблон) | ✅ Да, подтверждает скрытие кнопки решения и `data-solution`, наличие вкладки | None |
| E5 | E5 | Full suite, Python 3.12, SQLite WAL, TS §5 AC-5, clean | Repeated (`pytest tests/`) | ✅ Да, подтверждает 60 passed из 60 (100% pass) и изоляцию 4 студентов | None |
| E6 | E-accounting | `832bd17` -> `c2b3ef5`, Git CLI, TS §4, clean | Repeated (`git diff --numstat`) | ✅ Да, подтверждает 2232 touched text LOC в 10 файлах VALUE | None |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 | Priority 0: `README.md § Цель и North Star проекта` | ✅ | ✅ | ✅ Завершение 3-недельного курса ООП итоговым экзаменом | ✅ Сквозная аттестация курса |
| 2 | HL §7.2 #2 | Priority 1: `.tfw/README.md #ns1 · #ns2 · #ns3` | ✅ | ✅ | ✅ Трассируемость решений и проверяемость автотестами | ✅ Трассировка артефактов и тесты |
| 3 | HL §7.2 #3 | Priority 3: `KNOWLEDGE.md D1, D2` | ✅ | ✅ | ✅ Стек FastAPI/SQLite/Tailwind и сквозной домен Avtobys | ✅ Стек и домен экзамена |
| 4 | HL §7.2 #4 | Priority 3: `KNOWLEDGE.md D9` | ✅ | ✅ | ✅ Белый список AST и песочница `RunnerService` | ✅ Безопасность задач экзамена |
| 5 | HL §7.2 #5 | Priority 3: `KNOWLEDGE.md D10` | ✅ | ✅ | ✅ Многопользовательская изоляция 4 студентов в SQLite WAL | ✅ Изоляция профилей экзамена |
| 6 | HL §7.2 #6 | Priority 3: `KNOWLEDGE.md D11` | ✅ | ✅ | ✅ Эргономика IDE и баланс квизов (`max_len/min_len <= 1.65`) | ✅ IDE тренажера и баланс квиза |
| 7 | HL §7.2 #7 | Priority 7: `KNOWLEDGE.md F1, F5, F10` | ✅ | ✅ | ✅ 3 недели обучения по 20 б. + итоговый экзамен до 100 б. | ✅ 100-балльная шкала курса |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| `832bd170327d47637565efa574d2ac1145e23774` (approved TS) | `aeaab61f557a754d8e4a6bd0534eb532e8a6d061` | `c2b3ef5a2d436ab0214898310ea5c357be7d2b85` | 10 файлов VALUE (`app/content/exam/**`, `app/services/scoring.py`, `app/routers/exam.py`, `app/routers/scoring.py`, `app/main.py`, `app/templates/**`, `app/static/js/app.js`) | 2228 | 4 | 2232 | N/A | 2232 LOC < 5000 LOC, 10 файлов < 50 файлов; декомпозиция не требуется | `git diff --numstat 832bd170327d47637565efa574d2ac1145e23774 c2b3ef5a2d436ab0214898310ea5c357be7d2b85` | VERIFIED |

Candidate является первым протестированным коммитом реализации перед созданием EV/RF (`c2b3ef5a2d436ab0214898310ea5c357be7d2b85`). Последующий коммит `6767fd0fd2c4c61378e61ded2275ca30b0490df5` содержит исключительно артефакты `TRACE` (EV, RF, journal, status).

## Selected Knowledge Evidence

- **Producer unit:** `antigravity:thread:local:12f97fb2-4520-4e67-944b-5743e89747a4` (Executor)
- **Source epoch:** Candidate commit `c2b3ef5a2d436ab0214898310ea5c357be7d2b85`
- **Applicability:** Все изменения строго соответствуют утвержденному TS, обеспечивают 100% прохождение 60 автотестов платформы и сохраняют полную независимость профилей 4 студентов.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
