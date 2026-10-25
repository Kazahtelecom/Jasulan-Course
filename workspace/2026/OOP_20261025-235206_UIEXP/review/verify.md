# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | Medium — шапка ~200 px съедает вертикальное пространство на ноутбуках | `app/templates/components/header.html`, `app/static/js/app.js`, `app/static/css/style.css` | Python 3.12.9, FastAPI `TestClient`, инспекция DOM/JS/CSS | `TS §5 AC-1`, `HL §5 DoD-1` | Headless `TestClient` не измеряет пиксельную высоту в браузере; проверяется CSS-правило `display: none !important` на `#header-collapsible-body` | Чтение `header.html` (строки 1–102), `app.js` (строки 107–130, 626–627), `style.css` (строки 70–82) + прогон `test_collapsible_header` |
| C2 | High — невозможность развернуть задачу на весь экран или изменить ширину условия/кода | `app/templates/components/tab_practice.html`, `app/static/js/app.js`, `app/static/css/style.css` | Python 3.12.9, FastAPI `TestClient`, инспекция DOM/JS/CSS | `TS §5 AC-2`, `HL §5 DoD-2, DoD-3` | Drag-события `mousedown/mousemove/mouseup` проверяются инспекцией обработчиков в `app.js` | Чтение `tab_practice.html` (строки 84–245), `app.js` (строки 205–313, 633–637, 676–680), `style.css` (строки 85–112) + прогон `test_practice_fullscreen_and_splitter` |
| C3 | High — отсутствие номеров строк и риск рассинхронизации при вставке готового решения / сбросе | `app/templates/components/tab_practice.html`, `app/static/js/app.js`, `app/static/css/style.css` | Python 3.12.9, FastAPI `TestClient`, инспекция DOM/JS/CSS | `TS §5 AC-3`, `TS §7 DoF-2`, `HL §5 DoD-4` | Синхронизация вертикального скролла проверяется по совпадению `line-height: 1.65`, `fontSize` и `gutter.scrollTop = textarea.scrollTop` | Чтение `tab_practice.html` (строки 162–221), `app.js` (строки 150–200, 318–339, 640–673), `style.css` (строки 49–67) + прогон `test_editor_line_numbers_and_fontsize` |
| C4 | High (Hard Constraint M1–M6) — угадывание ответов по самому длинному тексту или букве `B` | `app/content/week_1/quiz.py`, `app/content/week_2/quiz.py`, `/api/week1/quiz/check`, `/api/week2/quiz/check` | Python 3.12.9, FastAPI `TestClient`, прямой расчет метрик | `TS §4 M1–M6`, `TS §5 AC-4`, `HL §5 DoD-5`, `HL §6 DoF-3` | None | Полное чтение всех 20 вопросов в `week_1/quiz.py` и `week_2/quiz.py`, независимый скрипт проверки длин и распределения `correct_index` + прогон `test_quiz_balance_and_traps` |
| C5, C6 | Mandatory safety/regression floor — сохранность `RunnerService`, AST-песочницы, `ScoringService`, Zero-Build и детекционной силы тестов | Все модули `app/` и полный тестовый пакет `tests/` (49 тестов) | Локальный запуск `pytest -v` на Windows 11 / Python 3.12.9 | `TS §5 AC-5`, `HL §6 DoF-1..4`, `PV P0, P3` | None | Независимый прогон `python -m pytest -v` (49 тестов) и аудит утверждений в `tests/test_ui_ergonomics.py` |
| C7, C8 | Mandatory authority & identity floor — идентичность `Candidate`, учет `VALUE`, `Exact-path staging`, цитирования знаний и экономика | Git-история `b5be743..37d7f84`, `status.md`, `journal/*`, `HL`, `TS`, `ONB`, `RF`, `EV`, `economics/roles/*.jsonl` | Git CLI, `tfw_economics.py validate`, проверка `%TEMP%` | `owner:zhasulan`, `TS §4`, `conventions.md §4, §6, §7, §10, §15` | None | Независимое воспроизведение NUL-safe `git diff --name-status/-numstat`, проверка `git show --stat 37d7f84`, валидация JSONL экономики и аудит `PV P0–P7` |

Safety/security, human acceptance authority and accepted-result identity are mandatory floors.
Expand verification when an observed fact changes a mapped claim, dependency, risk or evidence gap;
the existence or count of discrepancies never selects depth by itself.

## Verification Log

### V1: C1 — Сдвиг / сворачивание верхнего меню (`header.html`, `app.js`, `style.css`)
- **Accepted claim / authority:** На `/week1` и `/week2` рендерятся `#main-site-header`, `#header-collapsible-body` и `#header-collapse-toggle` (`toggleHeaderCollapse()`), переключающие `.header-collapsed` и сохраняющие выбор в `localStorage` (`weboop_header_collapsed`) (`TS §5 AC-1`).
- **Subject tuple:** `{header.html, app.js, style.css @ 37d7f84cd3c154b182d77adc04f0a371e039fa00, Python 3.12.9 / FastAPI TestClient, TS §5 AC-1, clean dependency state}`.
- **Action or evidence:** Прочитаны `app/templates/components/header.html` (строки 2–102), `app/static/js/app.js` (строки 107–130, 626–627), `app/static/css/style.css` (строки 70–82); выполнен `pytest tests/test_ui_ergonomics.py -k "test_collapsible_header" -v`.
- **Observed:** В `header.html` `<header id="main-site-header">` содержит `#header-collapsible-body` (обертка бренда, селектора студентов и пилюль недель) и кнопку `#header-collapse-toggle` (`onclick="toggleHeaderCollapse()"` с `#header-collapse-label`). В `app.js` `toggleHeaderCollapse()` переключает класс `header-collapsed`, меняет подпись (`▲ Свернуть меню` / `▼ Развернуть меню`), пишет `weboop_header_collapsed` в `localStorage` и восстанавливает состояние при `DOMContentLoaded`. В `style.css` правило `#main-site-header.header-collapsed #header-collapsible-body { display: none !important; }` скрывает верхние ряды. Тест проходит (`PASSED`).
- **Limit:** Пиксельная высота шапки в браузере не рендерится в `TestClient`, но гарантируется CSS-скрытием `#header-collapsible-body` и уменьшением `padding-top/bottom` до `0.5rem`.
- **Result:** HOLDS

### V2: C2 — Полноэкранный режим задачи с кодом и изменяемый размер колонок (`tab_practice.html`, `app.js`, `style.css`)
- **Accepted claim / authority:** Для каждой из 6 задач (`task_1..3`, `w2_task_1..3`) работают полноэкранный режим (`#fullscreen-btn-<id>`, `togglePracticeFullscreen`, выход по `Escape`) и регулировка ширины колонок (`#split-layout-<id>`, `#split-resizer-<id>`, `setPracticeSplitRatio`, пресеты `25/75`, `35/65`, `50/50`) (`TS §5 AC-2`).
- **Subject tuple:** `{tab_practice.html, app.js, style.css @ 37d7f84cd3c154b182d77adc04f0a371e039fa00, Python 3.12.9 / FastAPI TestClient, TS §5 AC-2, clean dependency state}`.
- **Action or evidence:** Прочитаны `app/templates/components/tab_practice.html` (строки 85–195), `app/static/js/app.js` (строки 205–313, 633–637, 676–680), `app/static/css/style.css` (строки 85–112); выполнен `pytest tests/test_ui_ergonomics.py -k "test_practice_fullscreen_and_splitter" -v`.
- **Observed:** В `tab_practice.html` каждая карточка `#practice-card-{{ task.id }}` содержит `#split-layout-{{ task.id }}`, левую панель `#task-pane-{{ task.id }}` с кнопками `setPracticeSplitRatio('{{ task.id }}', 25|35|50)`, перетаскиваемый разделитель `#split-resizer-{{ task.id }}`, правую панель `#editor-pane-{{ task.id }}` и кнопку `#fullscreen-btn-{{ task.id }}`. В `style.css` `.practice-fullscreen-active` задает `position: fixed !important; inset: 0 !important; z-index: 90 !important; width: 100vw !important; height: 100vh !important;` (выше `z-50` шапки). В `app.js` реализованы `togglePracticeFullscreen(taskId)`, `exitAllPracticeFullscreen()` по `Escape`, `setPracticeSplitRatio(taskId, ratioPercent)` с ограничением `25%..65%` и сохранением `weboop_split_width`, а также `initPracticeSplitResizers()` с защитой `document.body.style.userSelect = "none"`. Тест проходит (`PASSED`).
- **Limit:** Интерактивное перетаскивание мыши (`mousemove`) верифицировано инспекцией кода обработчика и формулы `(relativeX / rect.width) * 100`.
- **Result:** HOLDS

### V3: C3 — IDE-зона кодинга с номерами строк, счетчиком строк, `Tab` и масштабированием шрифта (`tab_practice.html`, `app.js`, `style.css`)
- **Accepted claim / authority:** Каждый редактор снабжен синхронной линейкой `#line-numbers-<id>`, счетчиком `#line-count-label-<id>`, поддержкой `Tab` (4 пробела) и кнопками `changeEditorFontSize(-1/+1)`, а `fillSolutionCode` и `resetTaskCode` вызывают `updateLineNumbers(taskId)` (`TS §5 AC-3`, `TS §7 DoF-2`).
- **Subject tuple:** `{tab_practice.html, app.js, style.css @ 37d7f84cd3c154b182d77adc04f0a371e039fa00, Python 3.12.9 / FastAPI TestClient, TS §5 AC-3 & DoF-2, clean dependency state}`.
- **Action or evidence:** Прочитаны `app/templates/components/tab_practice.html` (строки 162–221), `app/static/js/app.js` (строки 150–200, 318–339, 640–673), `app/static/css/style.css` (строки 49–67); выполнен `pytest tests/test_ui_ergonomics.py -k "test_editor_line_numbers_and_fontsize" -v`.
- **Observed:** В `tab_practice.html` внутри `.code-editor-workspace` расположены `#line-numbers-{{ task.id }}` и `<textarea id="editor-{{ task.id }}">`, в тулбаре — кнопки `changeEditorFontSize(-1)` и `changeEditorFontSize(1)` с `.editor-fontsize-label`, в футере — `#line-count-label-{{ task.id }}`. В `style.css` и `.line-numbers-gutter`, и `.code-editor-textarea` имеют идентичный `font-family` и `line-height: 1.65`. В `app.js` `applyEditorFontSize` синхронно меняет `fontSize` (`12px..20px`) у обоих элементов; `updateLineNumbers(taskId)` вызывается при `DOMContentLoaded`, `input`, `keydown` (`Tab` = 4 пробела), а также в `fillSolutionCode(taskId)` (строка 325) и `resetTaskCode(taskId)` (строка 338); событие `scroll` синхронизирует `gutter.scrollTop = textarea.scrollTop`.
- **Limit:** None.
- **Result:** HOLDS

### V4: C4 — Балансировка длины вариантов, распределение ответов и вопросы с ловушками в квизах Недели 1 и 2 (`week_1/quiz.py`, `week_2/quiz.py`)
- **Accepted claim / authority:** Во всех 20 вопросах `max(len(o)) / min(len(o)) <= 1.65`, минимум в 5 из 10 вопросов каждой недели правильный ответ не самый длинный, каждый индекс `0, 1, 2, 3` используется 2–3 раза на неделю, дистракторы содержат реалистичные ловушки ООП/SOLID, а API оценивания начисляет `20.0` б. (`TS §4 M1–M6`, `TS §5 AC-4`).
- **Subject tuple:** `{app/content/week_1/quiz.py, app/content/week_2/quiz.py @ 37d7f84cd3c154b182d77adc04f0a371e039fa00, Python 3.12.9 / FastAPI TestClient, TS §4 M1–M6 & §5 AC-4, clean dependency state}`.
- **Action or evidence:** Прочитаны все 20 вопросов в `app/content/week_1/quiz.py` и `app/content/week_2/quiz.py`; выполнен независимый Python-расчет метрик и `pytest tests/test_ui_ergonomics.py -k "test_quiz_balance_and_traps" -v`.
- **Observed:**
  - **Неделя 1 (`q1..q10`):** распределение `correct_index`: `{0: 3, 1: 2, 2: 3, 3: 2}` (каждый индекс 2–3 раза); коэффициенты `max_len / min_len`: `[1.12, 1.11, 1.12, 1.07, 1.06, 1.10, 1.09, 1.05, 1.03, 1.08]` (все $\le 1.12 \le 1.65$); правильный ответ не является строго самым длинным в `8 из 10` вопросов ($\ge 5$). Дистракторы проверяют реальные ловушки ООП: пропуск `self` (`TypeError`), локальная переменная `owner = owner` в `__init__` (`AttributeError`), копирование ссылки `card3 = card1`, подмена имени `_SmartCard__balance`, запись в `@property` без сеттера, граничное условие `amount >= 0` и мутация `self._balance -= fare` до проверки.
  - **Неделя 2 (`w2_q1..w2_q10`):** распределение `correct_index`: `{0: 2, 1: 3, 2: 2, 3: 3}` (каждый индекс 2–3 раза); коэффициенты `max_len / min_len`: `[1.08, 1.04, 1.09, 1.02, 1.04, 1.09, 1.11, 1.02, 1.08, 1.10]` (все $\le 1.11 \le 1.65$); правильный ответ не является строго самым длинным в `8 из 10` вопросов ($\ge 5$). Дистракторы проверяют тонкие различия между `SRP`, `OCP`, `LSP` (`NotImplementedError` в подклассе), `ISP` (пустая заглушка `pass` в толстом интерфейсе), `DIP` и фиктивным DI (вызов `StudentFareService()` внутри метода в обход `self.fare_service`).
  - API `/api/week1/quiz/check` и `/api/week2/quiz/check` возвращают `20.0 / 20.0` при 10 верных ответах.
- **Limit:** None.
- **Result:** HOLDS

### V5: C5, C6 — Отсутствие регрессий, безопасность песочницы, проверка комментариев и качество тестов (`tests/`)
- **Accepted claim / authority:** Полный набор автотестов проходит на 100%, регрессии отсутствуют, добавленные комментарии соответствуют `conventions.md → Comments` (`TS §5 AC-5`, `HL §6 DoF-1..4`).
- **Subject tuple:** `{Repository @ 37d7f84cd3c154b182d77adc04f0a371e039fa00, Python 3.12.9 / pytest 9.1.1, TS §5 AC-5, clean dependency state}`.
- **Action or evidence:** Выполнен независимый запуск `python -m pytest tests/ -q --collect-only` и `python -m pytest -v`; проверен diff комментариев и канальных слов (`todo`, `legacy`, `old`, `temp`) в `VALUE`-файлах.
- **Observed:** Собрано и успешно пройдено `49 passed, 1 warning in 17.95s` (включая все тесты AST-безопасности, `RunnerService`, изоляции профилей студентов, `test_week1.py`, `test_week2.py`, `test_ui_ergonomics.py`). В diff `VALUE`-файлов отсутствуют слова `todo`, `legacy`, `old`, `temp`, заметки для агентов или закомментированный код; присутствуют только JSDoc-описания функций и структурные комментарии секций шаблонов.
- **Limit:** None.
- **Result:** HOLDS

### V6: C7, C8 — Идентичность `Candidate`, учет `VALUE`, `Exact-path staging`, цитирования знаний и экономика
- **Accepted claim / authority:** Соблюдены границы `Baseline b5be743` → `Candidate 37d7f84`, селектор из 6 `VALUE`-файлов (`877 LOC` $\le$ `1000 LOC`), правило `Exact-path staging`, `ROLE LOCK`, валидность `HL §7.2` / `ONB §7`, валидность JSONL экономики `Executor` и очистка `%TEMP%`.
- **Subject tuple:** `{Git history b5be743..37d7f84 & task trace files, Git CLI & tfw_economics.py, TS §4 & conventions.md}`.
- **Action or evidence:** Выполнены `git show --stat 37d7f84cd3c154b182d77adc04f0a371e039fa00`, NUL-safe `git diff --name-status` и `git diff --numstat`, `python .tfw/economics/tfw_economics.py validate ...`, `Test-Path "$env:TEMP\tfw\OOP_20261025-235206_UIEXP"`.
- **Observed:** Коммит `37d7f84cd3c154b182d77adc04f0a371e039fa00` включает ровно 6 `VALUE`-файлов, 1 `ASSURANCE`-файл (`tests/test_ui_ergonomics.py`) и 3 `TRACE`-файла (`status.md` и 2 файла `journal/`), не захватив ни одного из посторонних грязных файлов рабочего дерева (`uml_viewer.html`, `Dockerfile` и др.). Сумма `VALUE` LOC: `636 + 241 = 877 LOC` (`6` файлов). Валидатор `tfw_economics.py validate` подтвердил корректность `a4930c48063c1ebb7cc6c81f329e2be8adbd917aa91d5264754349f05974fb1a.jsonl` (`rows: 2`). Временная папка `%TEMP%\tfw\OOP_20261025-235206_UIEXP` отсутствует (`False`).
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `python -m pytest tests/ -q --collect-only; python -m pytest -v` | C1, C2, C3, C4, C5, C6 | `exit 0`: `49 tests collected`, `49 passed, 1 warning in 17.95s` |
| 2 | `git show --stat 37d7f84cd3c154b182d77adc04f0a371e039fa00` | C7 | `exit 0`: 10 files in commit (6 VALUE, 1 ASSURANCE, 3 TRACE); no foreign dirty files staged |
| 3 | `git diff --name-status --find-renames=50% -z b5be743df7bae8c5d538f595a9c969f0d1cebafa 37d7f84cd3c154b182d77adc04f0a371e039fa00 -- app/templates/components/header.html app/templates/components/tab_practice.html app/static/js/app.js app/static/css/style.css app/content/week_1/quiz.py app/content/week_2/quiz.py` | C7 | `exit 0`: 6 `M` (`MODIFY`) files matching exact approved selector |
| 4 | `git diff --numstat --find-renames=50% -z b5be743df7bae8c5d538f595a9c969f0d1cebafa 37d7f84cd3c154b182d77adc04f0a371e039fa00 -- app/templates/components/header.html app/templates/components/tab_practice.html app/static/js/app.js app/static/css/style.css app/content/week_1/quiz.py app/content/week_2/quiz.py` | C7 | `exit 0`: `106+76=182`, `72+73=145`, `59+0=59`, `241+6=247`, `72+57=129`, `86+29=115` → `636 + 241 = 877` touched LOC |
| 5 | `python -c "from collections import Counter; from app.content.week_1 import QUIZ_QUESTIONS as W1; from app.content.week_2 import QUIZ_QUESTIONS as W2 ..."` | C4 | `exit 0`: `W1 {0: 3, 1: 2, 2: 3, 3: 2} [1.12..1.03] non_longest: 8`; `W2 {0: 2, 1: 3, 2: 2, 3: 3} [1.08..1.1] non_longest: 8` |
| 6 | `git diff b5be743... 37d7f84... -- <VALUE paths> \| Select-String -Pattern '^\+.*(//\|/\*\|<!--\|#\s\|todo\|legacy\|old\|temp)'` | C5 | `exit 0`: только валидные JSDoc и секционные заголовки; 0 слов `todo/legacy/old/temp` |
| 7 | `python .tfw/economics/tfw_economics.py validate workspace/2026/OOP_20261025-235206_UIEXP/economics/roles/a4930c48063c1ebb7cc6c81f329e2be8adbd917aa91d5264754349f05974fb1a.jsonl; Test-Path "$env:TEMP\tfw\OOP_20261025-235206_UIEXP"` | C8 | `exit 0`: JSONL valid (`rows: 2`, SHA-256 matches); `Test-Path = False` |

## Claim and Source Checks

1. Spot-check key claims or sources by material reliance, not convenience.
2. Confirm every citation resolves to a real, relevant artifact.
3. Verify data claims against a primary source where reachable.

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | SHA-256 исходных файлов в `HL §2.1` и замечание в `ONB §6` о рабочей копии `app.js` | `HL §2.1`, `ONB §6` | `app/templates/components/header.html`, `tab_practice.html`, `app.js`, `style.css`, `week_1/quiz.py`, `week_2/quiz.py` | ✅ |
| C2 | В `RF §1`: коэффициенты `max_len / min_len` не превышают `1.12`, в `8 из 10` вопросов каждой недели правильный ответ не самый длинный | `RF §1 п. 5`, `EV E4` | `app/content/week_1/quiz.py`, `app/content/week_2/quiz.py` (проверено скриптом #5) | ✅ |
| C3 | В `RF §1`: `fillSolutionCode` и `resetTaskCode` вызывают `updateLineNumbers(taskId)` | `RF §1 п. 4`, `RF §3 AC-3` | `app/static/js/app.js` (строки 325 и 338) | ✅ |
| C4 | В `RF §1`: арифметика `VALUE` составляет `636 + 241 = 877` LOC по 6 файлам между `b5be743` и `37d7f84` | `RF §1 Accounting`, `EV E-accounting` | Git repository history (`b5be743..37d7f84`, команда #4) | ✅ |
| C5 | В `RF §5`: валидированный вклад экономики `Executor` с `range: 0..51` и `sha256: a4930c48...` | `RF §5` | `workspace/2026/OOP_20261025-235206_UIEXP/economics/roles/a4930c48063c1ebb7cc6c81f329e2be8adbd917aa91d5264754349f05974fb1a.jsonl` | ✅ |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | `test_quiz_balance_and_traps` (`tests/test_ui_ergonomics.py:112`): инвариант `max_len / min_len <= 1.65`, `min_len >= 60`, распределение `correct_index` по `2..3` на каждый индекс `0..3` и `not_strictly_longest_count >= 5` + `20.0` б. в API | Возврат возможности угадывать правильный ответ в тестах Недели 1 и 2 по самому длинному тексту или выбору варианта `B` | На базовой ревизии `b5be743` этот тест гарантированно падает (`correct_index=1` встречался 7/10 раз в W1 и 10/10 раз в W2, а `max_len/min_len` достигал `2.5–3.5 > 1.65`) | admitted |
| G2 | permanent guard | `test_collapsible_header`, `test_practice_fullscreen_and_splitter`, `test_editor_line_numbers_and_fontsize` (`tests/test_ui_ergonomics.py:19–110`): наличие всех обязательных ID, вызовов `toggleHeaderCollapse`, `togglePracticeFullscreen`, `setPracticeSplitRatio`, `updateLineNumbers`, `changeEditorFontSize` и CSS-селекторов на `/week1` и `/week2` | Потеря кнопок сворачивания шапки, полноэкранного режима, сплиттера или линейки номеров строк при правке шаблонов | На базовой ревизии `b5be743` все 3 теста падают (`AssertionError`), так как ни один из контролов не существовал в DOM/JS/CSS | admitted |
| G3 | permanent guard | Существующие тесты безопасности и регрессии (`tests/test_sandbox_security.py`, `tests/test_runner.py`, `tests/test_week1.py`, `tests/test_week2.py`, `tests/test_week_modules.py`) | Нарушение изоляции AST-песочницы, поломка выполнения эталонных решений `SmartCard`/`TerminalValidator` или формулы оценивания | Негативные фикстуры в `test_sandbox_security.py`, `test_negative_cases.py` и `test_practice_starter_code_fails_before_completion` | admitted |

## Candidate Findings

No findings.

## Evidence Verification

`evidence/` holds only EV files; no verdict rests on working material.

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | `E1` (AC-1) | `{header.html, app.js, style.css @ 37d7f84, FastAPI TestClient, AC-1}` | ✅ Repeated & opened | ✅ | Проверка через `TestClient` + CSS/JS без реального браузерного рендера |
| E2 | `E2` (AC-2) | `{tab_practice.html, app.js, style.css @ 37d7f84, FastAPI TestClient, AC-2}` | ✅ Repeated & opened | ✅ | Drag-resizer проверен через DOM-структуру и код обработчиков `mousedown/mousemove/mouseup` |
| E3 | `E3` (AC-3) | `{tab_practice.html, app.js, style.css @ 37d7f84, FastAPI TestClient, AC-3}` | ✅ Repeated & opened | ✅ | None |
| E4 | `E4` (AC-4) | `{week_1/quiz.py, week_2/quiz.py @ 37d7f84, Python 3.12 / TestClient, AC-4 & M1–M6}` | ✅ Repeated & opened | ✅ | None |
| E5 | `E5` (AC-5) | `{Full test suite @ 37d7f84, pytest 9.1.1, AC-5}` | ✅ Repeated (`49 passed`) | ✅ | None |
| E6 | `E-accounting` (TS §4) | `{b5be743..37d7f84, Git CLI NUL-safe diff, TS §4}` | ✅ Repeated | ✅ | None |

## Knowledge Citations Verified

Scan PV priorities 0–4 in full and 5–7 by relevance. Verify every HL §7.2 and ONB §7 citation for
resolution, item existence, semantic match, currentness and relevance. Check priority 0 purpose and
priority 1 methodology separately even when one file contains both.

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 & ONB §7 #1 | **PV P0:** `README.md § Цель и North Star проекта` | ✅ | ✅ (`README.md:5–14`) | ✅ — определяет Web-OOP как локальную интерактивную мини-LMS по ООП на домене Avtobys с чистым веб-интерфейсом и автопроверкой кода | ✅ — задача напрямую улучшает эргономику тренажера и качество квизов Недели 1 и 2 |
| 2 | HL §7.2 #2 & ONB §7 #2 | **PV P1:** `.tfw/README.md #methodology-values` и `#success-criteria` | ✅ | ✅ (`.tfw/README.md:92–101, 135–144`) | ✅ — требует структурного принуждения (`Structural Enforcement` через проверяемые автотесты) и полной готовности результата без заглушек | ✅ — инварианты баланса квизов (`max/min <= 1.65`) и UI-контролов закреплены структурными гейтами в `tests/test_ui_ergonomics.py` |
| 3 | HL §7.2 #3 & ONB §7 #3 | **PV P3:** `KNOWLEDGE.md §1 D5 (Zero-Build интерфейс)` и `D8 (Декомпозиция UI)` + `REC-OOP_20261021-141300_REFAC-tech-modular-weeks.md` | ✅ | ✅ (`KNOWLEDGE.md:34, 37`) | ✅ — `D5` фиксирует отказ от сборщиков/npm, `D8` (актуальный преемник `D7` по структуре шаблонов) фиксирует декомпозицию на Jinja-компоненты `header.html`, `tab_practice.html` и модульный `app.js` | ✅ — все правки внесены в модульные компоненты `header.html` и `tab_practice.html` на чистом Vanilla JS/CSS |
| 4 | HL §7.2 #4 & ONB §7 #4 | **PV P3, P7:** `KNOWLEDGE.md §1 D6, D7` и `§4 F5 (Педагогическая воронка и 20-балльный квиз)` + `REC-OOP_20261018-213107_W1MAT-human-beginner-format.md` | ✅ | ✅ (`KNOWLEDGE.md:35–36, 67`) | ✅ — фиксирует бесплатный тренажер (`0.0` б.) с кнопкой готового решения `fillSolutionCode` и 20-балльный квиз (`10 × 2.0 = 20.0` б., порог `12.0` б., High-Water Mark) | ✅ — кнопка готового решения сохранена и интегрирована с `updateLineNumbers`, шкала `20.0` б. сохранена |
| 5 | HL §7.2 #5 & ONB §7 #5 | **PV P4:** `.tfw/conventions.md §3 HL`, `§11 Design Rules`, `§14 Anti-patterns` | ✅ | ✅ (`.tfw/conventions.md:48–120, 1451–1564`) | ✅ — фиксирует правила заморозки HL, запрет на комментарии-оправдания, соблюдение Role Lock и точечного стейджинга | ✅ — соблюдены при исполнении и коммите `Candidate` |
| 6 | Independent PV scan (P2, P5, P6, P7) | **PV P2, P5, P6:** `knowledge/philosophy.md`, `knowledge/convention.md`, `knowledge/process.md` (отсутствуют в проекте); **PV P7:** `KNOWLEDGE.md §4 F6, F7, F8` и записи в `knowledge/records/` | ✅ | ✅ (`KNOWLEDGE.md:68–70`) | ✅ — `F6` (4 профиля студентов), `F7` (нативная песочница без Docker / `run.bat`), `F8` (граница правила «без ИИ») проверены на отсутствие конфликтов и регрессий | ✅ — селектор 4 студентов в `header.html` и нативная песочница полностью сохранены |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| `TS__OOP_20261025-235206_UIEXP.md @ 646ca95f703e53d2e9d38d95d855f8034ac9067f` (approved by `owner:zhasulan` prior to execution; immutable denominator: `6` VALUE files, `1000` LOC; multiplier `2`) | `b5be743df7bae8c5d538f595a9c969f0d1cebafa` | `37d7f84cd3c154b182d77adc04f0a371e039fa00` | 6 logical `VALUE` files (`6 MODIFY`, `0 deviations`):<br>1. `app/templates/components/header.html` (`+72/-57 = 129`)<br>2. `app/templates/components/tab_practice.html` (`+86/-29 = 115`)<br>3. `app/static/js/app.js` (`+241/-6 = 247`)<br>4. `app/static/css/style.css` (`+59/-0 = 59`)<br>5. `app/content/week_1/quiz.py` (`+106/-76 = 182`)<br>6. `app/content/week_2/quiz.py` (`+72/-73 = 145`) | 636 | 241 | 877 | N/A (0 binary files) | `6 < 50` files (`decomposition_trigger_files`), `877 < 5000` LOC (`decomposition_trigger_loc`), within immutable plan (`6 <= 6`, `877 <= 1000`) — no trigger fired | `git diff --name-status --find-renames=50% -z b5be743df7bae8c5d538f595a9c969f0d1cebafa 37d7f84cd3c154b182d77adc04f0a371e039fa00 -- app/templates/components/header.html app/templates/components/tab_practice.html app/static/js/app.js app/static/css/style.css app/content/week_1/quiz.py app/content/week_2/quiz.py` & `git diff --numstat --find-renames=50% -z ...` | VERIFIED |

## Selected Knowledge Evidence

- **Lineage & contributors inspected:**
  1. **Task Coordinator (`antigravity:thread:local:43c55687-5d64-4647-9012-0331bd386a85`):** выпустил `HL-OOP_20261025-235206_UIEXP.md @ b5be743df7bae8c5d538f595a9c969f0d1cebafa` (содержит `Strategic Insights S1–S3` от `owner:zhasulan` и `Material handover`) и `TS__OOP_20261025-235206_UIEXP.md @ 646ca95f703e53d2e9d38d95d855f8034ac9067f`.
  2. **Executor (`antigravity:thread:local:22ef7c4c-5377-408c-a2a5-338eb364cdfe`):** активирован через `journal/20261025-235818__dispatch__c4d8.md`, выпустил `ONB__OOP_20261025-235206_UIEXP.md @ aee59c56dec164cbb0eaf0965db865903e93a7c0`, `Candidate @ 37d7f84cd3c154b182d77adc04f0a371e039fa00`, `EV` и `RF @ 72171312657e8b0155c62a177d9c9ce8d5b9c501` с заполненным блоком `Material handover at this return` и обоснованным `justified-none` для новых `Fact Candidates` (поскольку наблюдения владельца `S1–S3` уже зафиксированы в `HL §11`).
- **Applicability & qualification status:** Архитектурное решение о полноэкранном IDE-тренажере (сдвиг шапки, сплиттер, линейка номеров строк, масштабирование шрифта) и математической балансировке дистракторов квизов Недели 1–2 (`max_len/min_len <= 1.65`, равномерное распределение `0..3`) подлежит отражению Координатором на этапе `KNW` (`/tfw-docs` / `/tfw-knowledge`) перед закрытием задачи в `DONE`.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
