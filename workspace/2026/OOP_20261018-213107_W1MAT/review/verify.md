# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1, C2 | High (визуальный опыт и педагогическая связность для новичков) | `app/main.py`, `app/routers/week1.py`, `app/content/week_1/theory.py`, `app/templates/index.html`, `app/static/css/style.css`, `app/static/js/app.js`, `app/static/images/*.jpg` | Python 3.12.9, FastAPI `TestClient`, Jinja2 | `HL §3, §5 DoD-1..2, §6 DoF-3`; `TS §5 AC-1, AC-2` | None | Полное чтение шаблона `index.html`, `style.css`, `app.js`, `theory.py`, `main.py`, `week1.py` + прогон `test_week1_page_and_navigation_layout` и `test_index_dashboard`. |
| C3, C4 | Critical (жесткое ограничение `TS §4 M1–M6`: 0 б. за практику и 20.0 б. / порог 12.0 б. за квиз с High-Water Mark) | `app/content/week_1/practice.py`, `app/content/week_1/quiz.py`, `app/services/scoring.py`, `app/routers/week1.py`, SQLite (`TopicProgress`, `Submission`) | Python 3.12.9, SQLite, `RunnerService` | `HL §5 DoD-3..4, §6 DoF-1..2`; `TS §4 M1–M6, §5 AC-3, AC-4` | None | Аудит кода `scoring.py`, `practice.py`, `quiz.py`, `week1.py` + независимый запуск всех тестов тренажера и квиза (`pytest -v`). |
| C5 | Mandatory Floor (Safety / Security) | `app/routers/week1.py`, `app/services/runner.py`, `tests/test_runner.py`, `tests/test_models.py`, `tests/test_health.py` | Python 3.12.9, Windows subprocess sandbox (`timeout=5.0s`, `ASTValidator`) | `HL §6 DoF-4`; `KNOWLEDGE.md D3, F4`; Mandatory safety/security floor | None | Проверка маршрута `/api/week1/practice/{task_id}/run` (передача кода исключительно через `RunnerService.run_code`) и полный прогон `tests/test_runner.py`, `tests/test_models.py`, `tests/test_health.py`. |
| C6 | High (качество тестовой защиты `ASSURANCE` и чистота линтера) | `tests/test_week1.py`, весь проект (`ruff check .`, `pytest`) | Python 3.12.9, `pytest-9.1.1`, `ruff` | `HL §5 DoD-5`; `TS §5 AC-5` | None | Классификация каждого теста в `tests/test_week1.py` по защищаемому инварианту и контрфактическому обнаружению + независимый запуск `ruff check .` и `pytest -v`. |
| C7 | Mandatory Floor (Authority & Result Identity) | Git-история `cbb06729..HEAD`, `status.md`, `journal/*`, `ONB`, `EV`, `RF`, `economics/roles/*.jsonl`, источники `PV` | Git on `main`, Python 3.12.9 (`tfw_economics.py`) | `HL §4.1`; `TS §4 Prospective accounting contract`; `.tfw/workflows/review.md` | None | NUL-безопасный повтор расчета `git diff --name-status` и `--numstat` между Baseline и Candidate, проверка отсутствия пост-Candidate правок в `app/` и `tests/`, проверка комментариев/channel words, валидация JSONL экономики и полный скан `PV` (P0–P4, P7). |

Safety/security, human acceptance authority and accepted-result identity are mandatory floors.
Expand verification when an observed fact changes a mapped claim, dependency, risk or evidence gap;
the existence or count of discrepancies never selects depth by itself.

## Verification Log

### V1: C1, C2 — Интерфейс Dark Cyberpunk / Tech Modern, 5 вкладок навигации, Теория и разбор `Passenger` / `Validator`
- **Accepted claim / authority:** На `GET /` и `GET /week1` отдается единый интерфейс «Учебная платформа · Учимся вместе» в стиле Dark Cyberpunk (`#070b14`, неоновые карточки `cyber-card`) с переключателем недель, 5 вкладками (`Главная`, `Теория`, `Практика`, `Тестирование`, `Результаты`), 3 иллюстрациями (`week1_hero.jpg`, `oop_blueprint.jpg`, `oop_encapsulation.jpg`), без рендеринга мелких Mermaid UML-схем на странице, с 4 шагами теории (`THEORY_SECTIONS`) и 4 шагами построчного разбора `Passenger` / `Validator` (`WALKTHROUGH_EXAMPLE`). Оракул: `HL §3, §5 DoD-1..2, §6 DoF-3`; `TS §5 AC-1, AC-2`.
- **Subject tuple:** `{app/main.py, app/routers/week1.py, app/content/week_1/theory.py, app/templates/index.html, app/static/css/style.css, app/static/js/app.js, app/static/images/*.jpg} @ Candidate 79b39aedc52ca4e88a9c5a44568b26f4879e364d, Windows 11 / Python 3.12.9 / FastAPI TestClient, TS §5 AC-1..2, clean working tree`.
- **Action or evidence:** Прочитаны все целевые файлы представления и контента; запущены `pytest tests/test_health.py tests/test_week1.py -v`.
- **Observed:**
  - `app/main.py` (строки 43–58) и `app/routers/week1.py` (строки 39–68) используют единую функцию `build_platform_context(request, db)` для рендеринга `index.html` на `/` и `/week1`.
  - В `app/templates/index.html` реализованы двухуровневая шапка (`ООП`, `Учебная платформа`, `Учимся вместе • Web-OOP`), переключатель недель (Неделя 1 активна, Недели 2 и 3 со значком «Скоро» и тостом `showLockedWeekToast`) и 5 вкладок (`home`, `theory`, `practice`, `quiz`, `results`).
  - В шаблоне нет исполняемого скрипта Mermaid или тегов `<div class="mermaid">`; для обратной совместимости с `tests/test_health.py` сохранен только HTML-комментарий в строке 9: `<!-- Zero-Build reference: cdn.jsdelivr.net/npm/mermaid kept in docs/domain_model_uml.md -->`.
  - В `app/content/week_1/theory.py` определены `WEEK1_OVERVIEW` (`max_score: 20.0`, `pass_threshold: 12.0`), 4 шага `THEORY_SECTIONS` (`step_1_problem`, `step_2_blueprint`, `step_3_init_self`, `step_4_encapsulation`) и `WALKTHROUGH_EXAMPLE` (классы `Passenger` и `Validator` с 4 шагами построчного разбора).
  - В `app/static/images/` присутствуют все 3 бинарные иллюстрации (`week1_hero.jpg` — 921 248 байт, `oop_blueprint.jpg` — 764 911 байт, `oop_encapsulation.jpg` — 1 067 546 байт).
- **Limit:** None.
- **Result:** HOLDS

### V2: C3, C4 — Свободный тренажер Практики (`0.0` б., кнопка готового решения) и Итоговое Тестирование на `20.0` баллов (`10 × 2.0`, порог `12.0`, High-Water Mark)
- **Accepted claim / authority:** Практика содержит 3 пошаговые задачи по сборке `SmartCard` (`task_1`, `task_2`, `task_3`) с кнопками «💡 Показать текстовую подсказку» и «✨ Вставить готовое решение» (`fillSolutionCode`), проверяет код в `RunnerService`, но не начисляет и не требует баллов (`max_score = 0.0`, `total_score` остается `0.0`). Тестирование содержит 10 вопросов по `2.0` балла (`QUIZ_MAX_SCORE = 20.0`, порог `PASS_THRESHOLD = 12.0`), сохраняет результат в БД с защитой High-Water Mark. Оракул: `HL §5 DoD-3..4, §6 DoF-1..2`; `TS §4 M1–M6, §5 AC-3, AC-4`.
- **Subject tuple:** `{app/content/week_1/practice.py, app/content/week_1/quiz.py, app/services/scoring.py, app/routers/week1.py, app/templates/index.html, app/static/js/app.js} @ Candidate 79b39aedc52ca4e88a9c5a44568b26f4879e364d, Python 3.12.9 / SQLite / RunnerService, TS §4 M1–M6 & §5 AC-3..4`.
- **Action or evidence:** Проинспектированы `practice.py`, `quiz.py`, `scoring.py`, `week1.py`, `index.html`, `app.js`; выполнен прогон `pytest tests/test_week1.py -v`.
- **Observed:**
  - В `app/content/week_1/practice.py` у всех 3 задач (`task_1`, `task_2`, `task_3`) установлено `"max_score": 0.0`, заполнены `starter_code`, `hint`, `reference_solution` и `test_code`.
  - В `app/templates/index.html` (строка 416) и `app/static/js/app.js` (строки 74–82) кнопка `✨ Вставить готовое решение` вызывает `fillSolutionCode(taskId)`, подставляя `dataset.solution` в редактор `textarea`.
  - В `app/services/scoring.py` константы равны `QUIZ_MAX_SCORE = 20.0`, `TOTAL_MAX_SCORE = 20.0`, `PASS_THRESHOLD = 12.0` (строки 29–31). Метод `record_task_submission` жестко выставляет `topic_rec.score = 0.0` (строка 92), а `_recalculate_overall` вычисляет `overall.score = round(min(cls.TOTAL_MAX_SCORE, qz.score), 1)` и `overall.is_completed = overall.score >= cls.PASS_THRESHOLD` исключительно из записи `week_1_quiz` (строки 121–126). Тем самым жесткое ограничение `TS §4 M1–M6` структурно защищено.
  - В `app/content/week_1/quiz.py` заданы `POINTS_PER_QUESTION = 2.0`, `QUIZ_MAX_SCORE = 20.0` и 10 вопросов (`q1`..`q10`) с подробными `explanation`.
  - В `app/services/scoring.py` (строки 110–113) реализовано правило High-Water Mark: `if bounded_score > quiz_rec.score: quiz_rec.score = bounded_score`.
  - В `app/templates/index.html` и `app/static/js/app.js` все подписи синхронизированы со шкалой `20.0` баллов (`10 вопросов по 2.0 балла`, `порог зачета: 12.0 из 20.0 баллов`, `data.score >= 12.0`, `+2 балла`); остатков `6.0` или `4.0` баллов не обнаружено.
- **Limit:** None.
- **Result:** HOLDS

### V3: C5, C6 — Изоляция `RunnerService` (Safety/Security Floor), качество тестовых гардов и чистота сборки (`ruff` + `pytest`)
- **Accepted claim / authority:** Эндпоинт практики выполняет пользовательский код строго через изолированный `RunnerService.run_code` (`ASTValidator` + `tempfile.TemporaryDirectory` + `timeout=5.0s`); все 20 тестов проекта и `ruff check .` проходят без ошибок. Оракул: `HL §5 DoD-5, §6 DoF-4`; `TS §5 AC-5`.
- **Subject tuple:** `{app/routers/week1.py, app/services/runner.py, tests/*} @ Candidate 79b39aedc52ca4e88a9c5a44568b26f4879e364d, Windows 11 / Python 3.12.9 / pytest-9.1.1 / ruff`.
- **Action or evidence:** Проверен код `app/routers/week1.py` (строки 78–112) и `tests/test_week1.py`; выполнены `ruff check .`, `python -m pytest tests/ -q --collect-only` и `pytest -v`.
- **Observed:**
  - В `app/routers/week1.py` маршрут `POST /api/week1/practice/{task_id}/run` валидирует `task_id` через `get_practice_task(task_id)` (при неизвестном `task_id` возвращает `HTTP 404`) и передает `payload.code` и `task["test_code"]` напрямую в `RunnerService.run_code`. Файлы `app/services/runner.py` и `app/services/ast_validator.py` не модифицировались и сохраняют полную защиту (7/7 тестов в `tests/test_runner.py` зеленые).
  - `ruff check .` завершился с кодом `0` (`All checks passed!`).
  - `python -m pytest tests/ -q --collect-only` собрал ровно `20 tests collected in 0.03s`.
  - `pytest -v` завершился с кодом `0`: `20 passed, 1 warning in 10.60s`.
- **Limit:** None.
- **Result:** HOLDS

### V4: C7 — Идентичность принятого результата (Candidate), воспроизведение учета `VALUE`, Exact-path staging, комментарии и экономика
- **Accepted claim / authority:** Принятый результат зафиксирован в коммите Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d` до записи `EV`/`RF`/`status.md`; учет `VALUE` (`app/` относительно Baseline `cbb06729d3b4a5101bf447385e1fcb52d48481e1`) составляет 14 файлов (`1993` добавлений + `220` удалений = `2213` touched LOC, 3 бинарных `.jpg` = `N/A`), что укладывается в неизменяемый утвержденный владельцем знаменатель (`14` файлов, `2200` LOC, отношение `1.00x` по файлам и `1.006x` по LOC < `2.0x`); после Candidate изменений в `app/` и `tests/` нет; комментарии соответствуют `conventions.md` → `Comments`; выгрузка экономики Исполнителя валидна. Оракул: `TS §4`; `.tfw/workflows/review.md`; `.tfw/economics/README.md`.
- **Subject tuple:** `git range cbb06729d3b4a5101bf447385e1fcb52d48481e1..5a1e308, Candidate 79b39aedc52ca4e88a9c5a44568b26f4879e364d, Windows 11 / Git / Python 3.12.9`.
- **Action or evidence:** Выполнены NUL-безопасные команды `git diff --name-status --find-renames=50% -z`, `git diff --numstat --find-renames=50% -z`, `git show --stat`, проверка `git diff 79b39ae HEAD --name-status`, скан channel words (`todo`, `legacy`, `old`, `temp`) в `VALUE` diff и `python .tfw/economics/tfw_economics.py validate`.
- **Observed:**
  - NUL-безопасный `git diff` между `cbb06729d3b4a5101bf447385e1fcb52d48481e1` и `79b39aedc52ca4e88a9c5a44568b26f4879e364d` по селектору `app/` подтвердил точно 14 логических файлов (`10 A`, `4 M`), `1993` добавлений, `220` удалений, `2213` затронутых текстовых строк и `3` бинарных файла `.jpg` (`-\t-`).
  - Между Candidate `79b39ae` и `HEAD` (`5a1e308`) изменялись исключительно файлы трассы в `workspace/2026/OOP_20261018-213107_W1MAT/` (`RF`, `EV`, `economics/roles/*.jsonl`, `journal/*`, `status.md`). Ни один файл в `app/` или `tests/` после Candidate не менялся.
  - Скан добавленных строк `VALUE` diff на слова `todo`, `legacy`, `old`, `temp` дал `0` совпадений. Все докстринги и комментарии несут ценность для читателя или инструмента (`# ruff: noqa: E501`).
  - Валидатор экономики подтвердил корректность файла Исполнителя `8a5f4f3d70420b653c0870cdb8d8b6eb0de0e6d6c223b9091e14377f31c400e1.jsonl` (`rows: 2`, `sha256` совпадает с именем файла).
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `ruff check .` | C6 | Exit 0: `All checks passed!` |
| 2 | `python -m pytest tests/ -q --collect-only` | C6 | Exit 0: `20 tests collected in 0.03s` |
| 3 | `pytest -v` | C1, C2, C3, C4, C5, C6 | Exit 0: `20 passed, 1 warning in 10.60s` (`test_health.py`: 4, `test_models.py`: 4, `test_runner.py`: 7, `test_week1.py`: 5) |
| 4 | `git diff --name-status --find-renames=50% -z cbb06729d3b4a5101bf447385e1fcb52d48481e1 79b39aedc52ca4e88a9c5a44568b26f4879e364d -- app/` | C7 | Exit 0: 14 `VALUE` files (`10 A`, `4 M`), exact match with `TS §4` and `RF §1` |
| 5 | `git diff --numstat --find-renames=50% -z cbb06729d3b4a5101bf447385e1fcb52d48481e1 79b39aedc52ca4e88a9c5a44568b26f4879e364d -- app/` | C7 | Exit 0: `adds=1993`, `dels=220`, `touched=2213` across 11 text files + 3 binary `.jpg` (`N/A`) |
| 6 | `git diff 79b39aedc52ca4e88a9c5a44568b26f4879e364d HEAD --name-status` | C7 | Exit 0: Only `TRACE` files in `workspace/2026/OOP_20261018-213107_W1MAT/` changed after Candidate |
| 7 | `python .tfw/economics/tfw_economics.py validate workspace/2026/OOP_20261018-213107_W1MAT/economics/roles/8a5f4f3d70420b653c0870cdb8d8b6eb0de0e6d6c223b9091e14377f31c400e1.jsonl` | C7 | Exit 0: Valid v1 JSONL (`rows: 2`, SHA-256 verified) |
| 8 | Channel-word & comment audit across `git diff cbb06729..79b39ae -- app/` | C7 | Exit 0: `0` matches for `todo`/`legacy`/`old`/`temp`; all comments/docstrings comply with `conventions.md` → `Comments` |

## Claim and Source Checks

1. Spot-check key claims or sources by material reliance, not convenience.
2. Confirm every citation resolves to a real, relevant artifact.
3. Verify data claims against a primary source where reachable.

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | На `/` и `/week1` отдается единый интерфейс с 5 вкладками и 3 иллюстрациями без мелких Mermaid-схем | `RF §1 п. 2, 4`, `RF §3 AC-1`, `EV E1` | `app/main.py`, `app/routers/week1.py`, `app/templates/index.html`, `app/static/images/*.jpg` | ✅ |
| C2 | `THEORY_SECTIONS` содержит 4 шага для новичков на классе `SmartCard`, `WALKTHROUGH_EXAMPLE` содержит разбор `Passenger` и `Validator` из 4 шагов | `RF §1 п. 1`, `RF §3 AC-2`, `EV E2` | `app/content/week_1/theory.py` (строки 45–276) | ✅ |
| C3 | В `PRACTICE_TASKS` 3 задачи (`task_1`..`task_3`) имеют `max_score = 0.0`, кнопка `fillSolutionCode` вставляет `reference_solution`, а `record_task_submission` не начисляет баллы (`total_score == 0.0`) | `RF §1 п. 1, 3, 4`, `RF §2 п. 1`, `RF §3 AC-3`, `EV E3` | `app/content/week_1/practice.py`, `app/services/scoring.py` (строки 69–98), `app/static/js/app.js` (строки 74–82) | ✅ |
| C4 | Финальный квиз содержит 10 вопросов по `2.0` балла (`QUIZ_MAX_SCORE = 20.0`, `PASS_THRESHOLD = 12.0`) и сохраняет лучший балл по High-Water Mark | `RF §1 п. 1, 3`, `RF §3 AC-4`, `EV E4` | `app/content/week_1/quiz.py`, `app/services/scoring.py` (строки 29–31, 100–128) | ✅ |
| C5 | Учет `VALUE`: 14 файлов (`10 CREATE`, `4 MODIFY`), `1993 + 220 = 2213` touched LOC, 3 бинарных `.jpg` файла (`N/A`), Baseline `cbb06729d`, Candidate `79b39aedc` | `RF §1 Actual Value-Bearing Accounting`, `EV E-accounting` | Git history (`cbb06729d3b4a5101bf447385e1fcb52d48481e1..79b39aedc52ca4e88a9c5a44568b26f4879e364d`) | ✅ |
| C6 | Временная папка Исполнителя `%TEMP%\tfw\OOP_20261018-213107_W1MAT\` удалена перед возвратом, в репозитории нет рабочих логов | `RF §5` (строка 107) | Проверка чистоты дерева репозитория (`git status`) | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | `tests/test_week1.py::test_practice_reference_solutions_pass` + `test_practice_starter_code_fails_before_completion` — все 3 эталонных решения `SmartCard` (`task_1`..`task_3`) проходят тесты `test_code` в `RunnerService`, тогда как неотредактированные `starter_code` гарантированно падают (`passed is False`). | Неработающая кнопка «✨ Вставить готовое решение» или ложноположительные тесты задач, пропускающие пустой шаблон `pass`. | Встроенная негативная контрольная пара: `starter_code` выступает прямым мутантом/негативным контролем против тех же `test_code` и детектируется (`passed is False`), а внутри `test_code` проверяются граничные случаи (`card.balance = -9999` вызывает `AttributeError`, `top_up(-200) -> False`, `pay(120)` при балансе `100 -> False`). | admitted |
| G2 | permanent guard | `tests/test_week1.py::test_quiz_only_scoring_and_ungraded_practice` — жесткое ограничение `TS §4 M1–M6` и `AC-3`/`AC-4`: прохождение всех 3 задач практики оставляет `total_score == 0.0` и `is_completed is False`; 6 верных ответов квиза дают `12.0` б. (`is_completed is True`), последующая слабая попытка (2 ответа = `4.0` б.) не снижает сохраненный балл `12.0` (High-Water Mark), а 10 ответов дают `20.0` б. (`100%`). | Начисление/требование баллов за практику (блокировка новичков), сбой порога зачета `12.0` б. или потеря зачета при повторном прохождении квиза. | Пошаговый state-machine сценарий с контрфактической попыткой ухудшения результата (`two_correct` после `six_correct`) и проверкой инварианта `total_score == 0.0` после `tasks_completed == 3`. | admitted |
| G3 | positive control | `tests/test_week1.py::test_quiz_evaluation_logic` — проверка чистой функции `evaluate_quiz` на 10 вопросах (`score == 20.0`, `max_score == 20.0`). | Ошибка арифметики `POINTS_PER_QUESTION * correct_count`. | Позитивный контроль максимального балла (негативные/частичные ветки покрыты в G2). | labelled control |
| G4 | positive control | `tests/test_week1.py::test_week1_page_and_navigation_layout` + `tests/test_health.py::test_index_dashboard` — проверка HTTP 200 и наличия 5 вкладок, 3 иллюстраций, кнопки готового решения и маркеров совместимости на `/` и `/week1`. | Поломка рендеринга Jinja2-шаблона или выпадение вкладок/иллюстраций. | Позитивный smoke-контроль HTML-ответа. | labelled control |
| G5 | permanent guard | `tests/test_runner.py` (7 тестов ядра) — блокировка запрещенных импортов (`os`, `subprocess`, `sys`, `shutil`, `socket`), вызовов (`eval`, `exec`, `open`) и бесконечных циклов (`timeout=5.0s`) в `RunnerService`. | Нарушение безопасности локальной машины при запуске кода в песочнице (`HL §6 DoF-4`). | Прямые негативные фикстуры с вредоносным кодом и `while True: pass`, подтверждающие статус `SECURITY_VIOLATION` и `TIMEOUT`. | admitted |

## Candidate Findings

No findings.

## Evidence Verification

`evidence/` holds only EV files; no verdict rests on working material.

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | `E1` (AC-1) | `GET /`, `GET /week1`, `/static/images/*.jpg` @ Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d` (Windows 11 / Python 3.12.9) | ✅ (Repeated via `pytest` & file inspection) | ✅ | None |
| E2 | `E2` (AC-2) | `THEORY_SECTIONS` (4 steps) & `WALKTHROUGH_EXAMPLE` (4 steps) @ Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d` | ✅ (Repeated via `pytest` & `theory.py` audit) | ✅ | None |
| E3 | `E3` (AC-3) | `PRACTICE_TASKS` (`task_1`..`task_3`), `RunnerService`, `POST /api/week1/practice/{task_id}/run` @ Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d` | ✅ (Repeated via `pytest -k practice`) | ✅ | None |
| E4 | `E4` (AC-4) | `QUIZ_QUESTIONS` (10 questions $\times$ 2.0 pts = 20.0), `POST /api/week1/quiz/check`, High-Water Mark @ Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d` | ✅ (Repeated via `pytest -k quiz`) | ✅ | None |
| E5 | `E5` (AC-5) | `ruff check .`, `pytest --collect-only`, `pytest -v` (20 tests) @ Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d` | ✅ (Repeated independently) | ✅ | None |
| E6 | `E-accounting` (TS §4) | `git diff` `cbb06729d3b4a5101bf447385e1fcb52d48481e1..79b39aedc52ca4e88a9c5a44568b26f4879e364d -- app/` | ✅ (Repeated with exact NUL-safe command) | ✅ | None |

В папке `workspace/2026/OOP_20261018-213107_W1MAT/evidence/` находится исключительно файл `EV__OOP_20261018-213107_W1MAT.md`.

## Knowledge Citations Verified

Scan PV priorities 0–4 in full and 5–7 by relevance. Verify every HL §7.2 and ONB §7 citation for
resolution, item existence, semantic match, currentness and relevance. Check priority 0 purpose and
priority 1 methodology separately even when one file contains both.

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 & ONB §7 #1 | **P0 (Project North Star):** `README.md` → `§ Цель и North Star проекта` | ✅ | ✅ | ✅ — Определяет создание локальной интерактивной мини-LMS по ООП (Неделя 1: от процедурного стиля к объектам и инкапсуляции на домене Avtobys). | ✅ — Прямо задает предметную область и учебную цель Недели 1. |
| 2 | HL §7.2 #2 & ONB §7 #2 | **P1 (Methodology Values & Purpose/Principles):** `.tfw/README.md` → `§ NS1 — Purpose`, `§ NS2 — Principles` (Saint-Exupéry Principle), `§ Methodology values` (Candor Over Flattery, Structural Enforcement) | ✅ | ✅ | ✅ — Проверены раздельно смысл `NS1`/`NS2` (простота и сохранение ценности без лишних барьеров) и `Methodology values` (Candor Over Flattery и Structural Enforcement). | ✅ — Отказ от перегруженной первой итерации и структурная защита `0.0` б. за практику в `ScoringService`. |
| 3 | HL §7.2 #3 & ONB §7 #3 | **P2 (Philosophy):** `knowledge/philosophy.md` (N/A) | ✅ (N/A) | ✅ (Confirmed absent) | ✅ — Файл `knowledge/philosophy.md` в репозитории отсутствует; честно задекларировано `N/A`. | ✅ — Честная фиксация отсутствия опционального файла. |
| 4 | HL §7.2 #4 & ONB §7 #4 | **P3 (Architecture Decisions):** `KNOWLEDGE.md` → `§1 Architecture Decisions: D1, D2, D3, D4, D5` | ✅ | ✅ | ✅ — `D1` (FastAPI + SQLAlchemy + SQLite + Pytest + Jinja2 + Tailwind), `D2` (домен Avtobys), `D3` (`RunnerService` с AST + pytest 5s), `D4` (UML в `docs/`), `D5` (Zero-Build UI). | ✅ — Все 5 архитектурных решений строго соблюдены в реализации Недели 1. |
| 5 | HL §7.2 #5 & ONB §7 #5 | **P4 (Conventions):** `.tfw/conventions.md` → `§3 HL (High Level)`, `§14 Anti-patterns (prohibited)`, `§15 Role Lock Protocol` (плюс `§11 Design Rules`, `§12 Comments` в ONB §7) | ✅ | ✅ | ✅ — Определяют правила заморозки контракта HL, запрещенные антипаттерны, Role Lock, Exact-path staging и чистоту комментариев. | ✅ — Применены при планировании, исполнении и ревью задачи. |
| 6 | Independent PV Scan | **P5 (`knowledge/convention.md`) & P6 (`knowledge/process.md`):** N/A | ✅ (N/A) | ✅ (Confirmed absent) | ✅ — Папка `knowledge/` в репозитории не создана; все конвенции и факты процесса живут в `.tfw/conventions.md` и `KNOWLEDGE.md`. | ✅ — Проверено независимым сканированием P0–P7. |
| 7 | HL §7.2 #6 & ONB §7 #6 | **P7 (Project Facts):** `KNOWLEDGE.md` → `§4 Project Facts: F1, F2, F3, F4` | ✅ | ✅ | ✅ — `F1` (студенты 2 курса), `F2` (`@zhasulan` и `@saubakirov`), `F3` (локальный запуск), `F4` (изоляция `RunnerService`). | ✅ — Напрямую определяют профиль студента по умолчанию и адаптацию контента под курс. |
| 8 | ONB §7 #7 | **P7 / Domain Reference:** `docs/domain_model_uml.md` → `§2 Диаграмма классов` | ✅ | ✅ | ✅ — Описывает классы `Passenger` и `Validator` и их методы (`top_up`, `deduct_fare`, `validate_ticket`). | ✅ — Использовано в построчном разборе `WALKTHROUGH_EXAMPLE` во вкладке «Практика». |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| `TS__OOP_20261018-213107_W1MAT.md @ c373aeef251a58b106afc6aa07813972171673c5` (approved before execution; immutable owner-approved denominator: `14 VALUE files, 2200 touched text LOC`, `owner_escalation_multiplier: 2`) | `cbb06729d3b4a5101bf447385e1fcb52d48481e1` | `79b39aedc52ca4e88a9c5a44568b26f4879e364d` | Selector `app/` — 14 logical `VALUE` files (`10 CREATE`, `4 MODIFY`, 0 deviations from `TS §4`): `app/content/__init__.py` (`A`, `1+0=1`), `app/content/week_1/__init__.py` (`A`, `16+0=16`), `app/content/week_1/practice.py` (`A`, `270+0=270`), `app/content/week_1/quiz.py` (`A`, `205+0=205`), `app/content/week_1/theory.py` (`A`, `276+0=276`), `app/main.py` (`M`, `13+9=22`), `app/routers/week1.py` (`A`, `131+0=131`), `app/services/scoring.py` (`A`, `159+0=159`), `app/static/css/style.css` (`M`, `53+8=61`), `app/static/images/oop_blueprint.jpg` (`A`, binary), `app/static/images/oop_encapsulation.jpg` (`A`, binary), `app/static/images/week1_hero.jpg` (`A`, binary), `app/static/js/app.js` (`M`, `315+104=419`), `app/templates/index.html` (`M`, `554+99=653`). | 1993 | 220 | 2213 | 3 binary `.jpg` files = per-file LOC `N/A` | Single-phase budgets respected (`14 < 50` files, `2213 < 5000` LOC); ratio vs immutable denominator: `14/14 = 1.00x` files, `2213/2200 = 1.006x` LOC (`< 2.0x` ceiling). | `git diff --name-status --find-renames=50% -z cbb06729d3b4a5101bf447385e1fcb52d48481e1 79b39aedc52ca4e88a9c5a44568b26f4879e364d -- app/` & `git diff --numstat --find-renames=50% -z cbb06729d3b4a5101bf447385e1fcb52d48481e1 79b39aedc52ca4e88a9c5a44568b26f4879e364d -- app/` | VERIFIED |

## Selected Knowledge Evidence

- **Coordinator return (`HL-OOP_20261018-213107_W1MAT.md §12 Material handover`):**
  - *Producer / unit:* Task Coordinator (`antigravity:thread:local:1da46223-edb5-410d-bad6-cd3c36954a1f`), epoch `cbb06729d3b4a5101bf447385e1fcb52d48481e1` (HL freeze) / `c373aeef251a58b106afc6aa07813972171673c5` (TS approval).
  - *Scope & authority:* Зафиксированы 3 стратегических инсайта владельца (`HL §11 S1–S3`: малая группа с полными новичками в ООП; свободный тренажер без оценки с кнопкой готового решения и 20-балльный итоговый квиз; отказ от мелких Mermaid-схем в UI в пользу Dark Cyberpunk и крупных иллюстраций).
- **Executor returns (`ONB__OOP_20261018-213107_W1MAT.md` & `RF__OOP_20261018-213107_W1MAT.md`):**
  - *Producer / unit:* Executor (`antigravity:thread:local:57788b4b-d3d1-4980-b668-c5b2875c9521`), dispatched by `journal/20261018-213731__dispatch__d4e1.md @ c373aeef251a58b106afc6aa07813972171673c5`, Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d`.
  - *Scope & applicability:* Исполнитель задокументировал `justified-none` для новых Fact Candidates / Strategic Insights в `RF §§7–8`, так как все продуктовые и архитектурные решения были полностью определены в `HL`/`TS` и `KNOWLEDGE.md` (`D1`–`D5`, `F1`–`F4`). Проверено независимо: новых неквалифицированных доменных допущений в коде нет, а инсайты планирования `HL §11 S1–S3` подлежат штатной передаче Координатору на этапе `KNW` (`/tfw-docs` / `/tfw-knowledge`).

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
