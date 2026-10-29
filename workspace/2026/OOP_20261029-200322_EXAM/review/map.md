# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__OOP_20261029-200322_EXAM.md](../RF__OOP_20261029-200322_EXAM.md)
> TS: [TS__OOP_20261029-200322_EXAM.md](../TS__OOP_20261029-200322_EXAM.md)

## Understanding

Реализован единый модуль итоговой аттестации курса ООП (`/exam`), состоящий из комплексного теоретического квиза (20 вопросов по 1.0 б., охватывающих Недели 1–3) и двух практических задач в тренажёре (по 10.0 б., суммарно 20.0 б.). Модуль исключает кнопки и атрибуты готовых решений, обеспечивая академическую честность, расширяет `ScoringService` на 40-балльный экзамен и доводит семестровый рейтинг 4 студентов до 100-балльной ведомости с фиксацией High-Water Mark в SQLite WAL. Все изменения выполнены в рамках утвержденного скоупа однофазной задачи без декомпозиции и покрыты 60 автотестами.

## Accepted Claims and Boundaries

Map the result before selecting checks. Safety/security, human acceptance authority and
accepted-result identity are mandatory even when no ordinary claim sample selects them.

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | Теоретический квиз экзамена: ровно 20 вопросов по Неделям 1–3, баланс длин вариантов `<= 1.65`, по 5 верных ответов на каждый индекс 0..3, скоринг 1.0 б./вопрос (макс 20.0 б., порог 12.0 б.) | Несбалансированные вопросы, угадывание по длине, некорректный расчет баллов | `app/content/exam/quiz.py`, `app/content/exam/__init__.py` | Python 3.12, pytest | TS §5 AC-1, `tests/test_exam.py` | `app/content/exam/quiz.py@c2b3ef5`, EV §2 E1 | yes |
| C2 | VALUE / ASSURANCE | Практические задачи экзамена: 2 задачи (`exam_task_1`, `exam_task_2`) по 10.0 б. со стартовым кодом и эталонными решениями, строгий белый список AST, исполнение в песочнице < 5.0 с | Отказ песочницы, нарушение белого списка AST, зависание тестов, нерабочий эталонный код | `app/content/exam/practice.py`, `app/services/runner.py`, `ast_validator.py` | Python 3.12, `python -I` subprocess | TS §5 AC-2, `tests/test_exam.py` | `app/content/exam/practice.py@c2b3ef5`, EV §2 E2 | yes |
| C3 | VALUE | Скоринг и 100-балльная шкала курса: начисление до 40.0 б. за экзамен, подсчет `Grand Total = W1(20) + W2(20) + W3(20) + Exam(40) = 100.0 б.`, защита High-Water Mark | Искажение итоговых оценок, потеря баллов при повторных попытках, выход за 100.0 б. | `app/services/scoring.py`, `app/routers/scoring.py` | SQLite WAL (`data/web_oop.db`) | TS §5 AC-3, `tests/test_exam.py` | `app/services/scoring.py@c2b3ef5`, EV §2 E3 | yes |
| C4 | VALUE | Режим академической честности и UI: активная ссылка `🏆 Экзамен` в `header.html`, скрытие кнопки «Показать готовое решение» и атрибута `data-solution` на `/exam` | Списывание студентами готового кода через интерфейс или инспекцию DOM | `app/templates/exam.html`, `app/templates/components/header.html`, `app/static/js/app.js` | Jinja2, DOM/HTML5, Tailwind | TS §5 AC-4, `tests/test_exam.py` | `app/templates/exam.html@c2b3ef5`, EV §2 E4 | yes |
| C5 | VALUE / ASSURANCE | Мультипользовательская изоляция и регрессионная надежность: независимый прогресс 4 студентов группы, 100% прохождение всех тестов платформы | Взаимное повреждение данных студентов, поломка функционала Недель 1–3 | `data/web_oop.db`, `tests/` | SQLite WAL, pytest 9.1.1 | TS §5 AC-5, `tests/` | `tests/test_exam.py@c2b3ef5`, EV §2 E5 | yes |
| C6 | TRACE / ASSURANCE | Бухгалтерский учет и Candidate: NUL-safe diff между `832bd17` и `c2b3ef5` составляет 2232 touched text LOC в 10 файлах `VALUE` без отклонений от селектора TS §4 | Неучтенные файлы, посторонние правки, превышение лимитов декомпозиции | Git repo, `git diff` | Git CLI on Windows | TS §4, EV §2 E-accounting | `git diff 832bd17 c2b3ef5`, EV §2 E-accounting | yes |
| C7 | TRACE | Мандат, авторитет и независимость: неизменяемый знаменатель владельца `zhasulan` от 2026-10-29 (`832bd17`), роль Reviewer соблюдена | Нарушение границ роли, потеря трассируемости решений | `status.md`, `HL`, `TS`, `RF` | TFW protocol | HL §4.1, TS §4 | `status.md@6767fd0`, RF §1 | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1: Теоретический квиз (20 вопр., 20.0 б., баланс <= 1.65, равномерность 0..3) | RF §3 AC-1: 20 вопросов, баланс <= 1.120, по 5 на индекс, скоринг 1.0 б. | C1 | ✅ |
| AC-2: Боевые задачи экзамена (2 задачи по 10.0 б., AST-песочница < 5.0 с) | RF §3 AC-2: 2 задачи по 10.0 б., строгий AST-белый список, прогон 0.64–0.75 с | C2 | ✅ |
| AC-3: Скоринг и 100-балльная ведомость курса (до 40 б. экзамен, итог 100 б., High-Water Mark) | RF §3 AC-3: учет экзамена до 40 б., итог курса до 100 б., High-Water Mark | C3 | ✅ |
| AC-4: Режим честности (скрытие решений) и навигация UI (`🏆 Экзамен` в шапке) | RF §3 AC-4: ссылка в шапке, отсутствие кнопки и `data-solution` в DOM | C4 | ✅ |
| AC-5: Изоляция 4 студентов и сквозная регрессионная надежность (100% pass) | RF §3 AC-5: независимый прогресс 4 студентов, 60/60 тестов passed | C5 | ✅ |
| DoF 1..5: отсутствие готовых решений, валидность AST, изоляция/High-Water Mark, сумма 100 б., отсутствие регрессий | RF §1, §2, §3: все DoF строго соблюдены, сбоев не зафиксировано | C1–C5 | ✅ |
| TS §4: Селектор 9+1 файлов `VALUE` в пределах бюджета LOC | RF §1: 10 текстовых файлов `VALUE`, 2232 touched LOC, селектор соблюден | C6 | ✅ |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1 | Независимый прогон `pytest tests/test_exam.py -k test_exam_quiz_balance_and_evaluation -v` и инспекция `app/content/exam/quiz.py` | Прямая проверка математического баланса длин и распределения ответов квиза | Нет |
| C2 | Независимый прогон `pytest tests/test_exam.py -k test_exam_practice_tasks_in_sandbox -v` и проверка `app/content/exam/practice.py` | Подтверждение исполнения в изолированном subprocess `python -I` и соблюдения AST-ограничений | Нет |
| C3 | Независимый прогон `pytest tests/test_exam.py -k test_scoring_grand_total_100 -v` и инспекция `app/services/scoring.py` | Проверка граничных условий скоринга, пересдач и High-Water Mark | Нет |
| C4 | Независимый прогон `pytest tests/test_exam.py -k test_exam_ui_integrity -v` и проверка шаблона `exam.html` | Проверка полного отсутствия кнопок и атрибутов решений в разметке | Нет |
| C5 | Независимый полный прогон `pytest tests/` (все 60 тестов) | Гарантия отсутствия регрессий в существующих модулях Недель 1–3 | Нет |
| C6 | Независимый запуск `git diff --numstat 832bd17 c2b3ef5` и проверка селектора | Точное воспроизведение объема и границ Candidate | Нет |
| C7 | Аудит `status.md`, `HL`, `TS`, `RF`, `EV` на предмет неизменяемых рефов и целостности цепочки | Проверка контрактной дисциплины TFW | Нет |

## Deviations from TS

Файл `app/routers/scoring.py` был модифицирован (+2 LOC) для передачи данных Недели 3 и итогового экзамена в эндпоинт `/api/students/scores`. Данный файл полностью покрыт селектором TS §4 (`app/routers/exam.py`, `app/services/scoring.py`, сопутствующие роутеры API) и напрямую обеспечивает работу единой сводной ведомости 4 студентов из 100 баллов. Посторонних или непредусмотренных изменений не обнаружено.

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
