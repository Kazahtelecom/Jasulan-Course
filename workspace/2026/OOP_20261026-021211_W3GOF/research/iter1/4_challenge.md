# Challenge — OOP_20261026-021211_W3GOF

> **Parent**: [RES — OOP_20261026-021211_W3GOF](RES.md)
> **Stage**: 4 of 4 (OODA: Decide / Stress-test)
> **Constraint**: Every configuration from Extract MUST be either eliminated with a documented pair or listed in Surviving Configurations.

## Pairwise Incompatibility

| Factor A | Value A | Factor B | Value B | Why incompatible | Source |
|----------|---------|----------|---------|------------------|--------|
| **F5: AST-совместимость песочницы** (`ASTValidator`) | Полный перенос кода Лаб 6–9 без адаптации (**C4**) | **Белый список AST и атрибутов** (`app/services/ast_validator.py`) | `ALLOWED_MODULES` (14 модулей), запрет `__new__` и `.__class__.__name__` | В исходном коде PDF (`RF__lecture_06..09.pdf`, `RF__lab_06..09.pdf`) используются: `import time` (`TimingDecorator`), `import re` (`PlateNumber`), `__new__` (`GlobalConfig`) и `observer.__class__.__name__` (`ValidatorSubject.notify`). Любая из этих 4 конструкций немедленно блокируется `ASTValidator.validate()` со статусом `SECURITY_VIOLATION`. | `app/services/ast_validator.py:13-29`, `122-177`; эмпирический прогон `RunnerService.run_code()` |
| **F6: Шаблоны вкладок UI** (`tab_theory.html`, `tab_practice.html`) | Строгое ограничение правок шаблонов только `header.html` и `uml_viewer.html` (**C5**) | **Корректное отображение Недели 3 при `active_week == 3`** | Контекстный баннер теории GoF и пример кода практики Недели 3 | В `app/templates/components/tab_theory.html:6` и `app/templates/components/tab_practice.html:19,47` зашито бинарное ветвление `{% if active_week|default(1) == 2 %} ... {% else %}`. При `active_week == 3` оба шаблона проваливаются в ветку `{% else %}` Недели 1 (`SmartCard`, `example_avtobys.py`), нарушая целостность интерфейса Недели 3. | `app/templates/components/tab_theory.html:6-27`, `app/templates/components/tab_practice.html:19-107` |
| **F1: Покрытие тем в 3 задачах** (`w3_task_1..3`) | 4 задачи или полный многофайловый каркас Clean Architecture в одной задаче (**C4**) | **Инвариант `WeekModule` и когнитивный порог студента** (`app/services/scoring.py`) | Ровно 3 задачи по 20 баллов (`max_practice_points == 60`), время решения 10–15 минут (25–45 строк) | `calculate_week_score` и `tests/test_week_modules.py` жестко проверяют 3 задачи (`len(w.practice) == 3`, `sum == 60`). Многослойный каркас Лабы 9 (`domain` + `application` + `infrastructure`) в одном редакторе превышает 110 строк и размывает фокус отладки. | `app/services/scoring.py:18-65`, `tests/test_week_modules.py:18-29`, указание владельца/Coordinator в `1_briefing.md` |

## Surviving Configurations

| # | Configuration | Description | Strengths | Risks / Trade-offs | Unexpected? |
|---|--------------|-------------|-----------|-------------------|-------------|
| **C3** *(Selected Winner)* | **Гибридный конвейер GoF + Clean Architecture Ports** + полная синхронизация 4 шаблонов (`header.html`, `uml_viewer.html`, `tab_theory.html`, `tab_practice.html`) | - `w3_task_1`: `ShiftReportBuilder` + `@dataclass(frozen=True) class DailyShiftReport` + `IncompleteReportError` (Лаба 6, порождающий Fluent Builder).<br>- `w3_task_2`: `BankApiAdapter` + `PaymentGateway(Protocol)` + `LegacyBankClient` + `PaymentGatewayError` (Лаба 7 + Лаба 9 Dependency Rule, структурный Adapter).<br>- `w3_task_3`: `ValidationHandler(ABC)` (`BlacklistCheckHandler`, `BalanceCheckHandler`) + `TransitTelemetrySubject` / `MetricsCollectorObserver` (Лаба 8, поведенческий конвейер CoR + Observer).<br>- `w3_q1..w3_q10`: 6 вопросов по GoF + 4 глубоких вопроса по Clean Architecture и Code Smells (Лаба 9). | - 100% сохранение канонических сигнатур из авторских PDF (`RF__lab_06..09.pdf`).<br>- Эмпирически подтвержденное прохождение `ASTValidator` и `RunnerService.run_code()` (`status='PASSED'`, ~0.95 сек на задачу).<br>- Компактный размер эталонных решений: 41, 26 и 41 непустых строк.<br>- Полный охват всех 4 лекций/лабораторных (Лекции 6–9) между практикой и квизом. | Требует аккуратного соблюдения инвариантов длины вариантов ответа в `w3_q1..w3_q10` (`min_len >= 60`, `ratio <= 1.65`) и уникальных ID (`#shadow-w3`, `#arrow-w3`) внутри `<defs>` в `<svg id="svg-week3">`. | **YES** — объединение `Chain of Responsibility` и `Observer` в `w3_task_3` (по образцу `TransitValidationPipeline` из Задания 8.3 `RF__lab_08.pdf`) позволило покрыть оба ключевых поведенческих паттерна без увеличения числа задач свыше 3 и без превышения лимита в 45 строк кода. |
| **C1** | **Классическая триада GoF (1 паттерн на задачу)** + синхронизация 4 шаблонов | `ShiftReportBuilder` (`w3_task_1`), `BankApiAdapter` (`w3_task_2`), только `ValidationHandler` (`w3_task_3`, без `Observer`). | Минимальный объем кода в `w3_task_3` (~30 строк). | Паттерн `Observer` (`TransitTelemetrySubject`) остается только в теории и квизе, не закрепляясь в коде практики. | NO |
| **C2** | **Упор на Clean Architecture Use Case в `w3_task_3`** + синхронизация 4 шаблонов | `ShiftReportBuilder` (`w3_task_1`), `BankApiAdapter` (`w3_task_2`), `ValidateRideUseCase` с 3 портами (`w3_task_3`). | Прямая проверка `ValidateRideUseCase.execute()` из Лабы 9 в коде. | В `w3_task_3` приходится объявлять 3 стаба портов (`CardRepositoryPort`, `PaymentGatewayPort`, `AuditLedgerPort`), а поведенческие паттерны Лабы 8 (`CoR`, `Observer`) полностью выпадают из практики. | NO |

## Stress-Test Findings (Empirical Verification of C3)

1. **Эмпирический прогон `w3_task_1..3` через `ASTValidator` и `RunnerService.run_code()`:**
   - Все 3 эталонных решения (`reference_solution`) и их `pytest`-сьюты (`test_code` с `from solution import ...`) протестированы на реальном `RunnerService.run_code()`:
     - `w3_task_1` (`ShiftReportBuilder` / `DailyShiftReport` / `IncompleteReportError`): `ASTValidator.validate() == (True, None)`, `RunnerService.run_code().passed == True` (`status='PASSED'`, 41 непустая строка, 920 мс).
     - `w3_task_2` (`BankApiAdapter` / `LegacyBankClient` / `PaymentGateway` / `PaymentGatewayError`): `ASTValidator.validate() == (True, None)`, `RunnerService.run_code().passed == True` (`status='PASSED'`, 26 непустых строк, 950 мс).
     - `w3_task_3` (`ValidationHandler` / `BlacklistCheckHandler` / `BalanceCheckHandler` / `MetricsCollectorObserver` / `TransitTelemetrySubject`): `ASTValidator.validate() == (True, None)`, `RunnerService.run_code().passed == True` (`status='PASSED'`, 41–51 строка в зависимости от форматирования `@dataclass`, 1075 мс).
   - **Важный нюанс `RunnerService`:** `RunnerService.run_code()` записывает студенческий код в `solution.py`, а `test_code` — в `test_solution.py` и запускает `pytest -o pythonpath=. test_solution.py -v`. При этом `ASTValidator.validate(code)` вызывается только для `code` (студенческого решения), тогда как `test_code` должен импортировать тестируемые классы через `from solution import ...` и оформлять проверки как функции `def test_*():`.
2. **Стресс-тест ограничений квиза (`test_quiz_balance_and_traps` в `tests/test_week_modules.py`):**
   - Автотест проверяет каждый модуль в `list_weeks()` (включая Неделю 3 после её регистрации в `WEEK_MODULES`):
     1. У каждого из 10 вопросов (`w3_q1..w3_q10`) ровно 4 варианта ответа (`len(q["options"]) == 4`).
     2. Минимальная длина любого варианта ответа — **не менее 60 символов** (`min_len >= 60`).
     3. Отношение длины самого длинного варианта к самому короткому в пределах одного вопроса — **не более 1.65** (`max_len / min_len <= 1.65`).
     4. Распределение индексов правильных ответов (`0, 1, 2, 3`) по 10 вопросам: каждый индекс встречается **2 или 3 раза** (`2 <= counts.get(idx, 0) <= 3`, например `[3, 2, 3, 2]`).
     5. Не менее чем в **5 из 10 вопросов** правильный ответ **не является строго самым длинным** (`len(correct) < max_len` или есть дистрактор такой же максимальной длины).
3. **Стресс-тест SVG-изоляции (`test_uml_svgs_have_self_contained_defs` в `tests/test_uml_viewer.py`):**
   - Каждый корневой `<svg id="svg-week*">` в `app/templates/components/uml_viewer.html` парсится через `re.findall` на предмет всех ссылок `url(#...)` в атрибутах `filter` и `marker-end`.
   - Если `<svg id="svg-week3">` использует `filter="url(#shadow)"` (определенный только внутри `<svg id="svg-week1">`), тест `test_uml_svgs_have_self_contained_defs` немедленно падает с `AssertionError: SVG #svg-week3 references undefined local defs`.
   - Следовательно, `<svg id="svg-week3">` обязан содержать собственный блок `<defs>` со всеми используемыми фильтрами и маркерами (`#shadow-w3`, `#arrow-w3`, `#arrow-arch-w3`).

## Challenge Checkpoint

> Pre-authorized by Coordinator (`5e1d1422-f45d-4f89-9d10-9eff76d814cb`) during Extract review to complete `4_challenge.md` and proceed directly to `RES.md`.

**Presented to user:**
- Eliminated configurations: **C4** (unmodified PDF code violates `ASTValidator` and 3-task `WeekModule` contract), **C5** (omitting `tab_theory.html` and `tab_practice.html` causes Week 3 UI to fall back to Week 1 banners/examples).
- Surviving configurations: **C3** (Selected Hybrid GoF + Clean Architecture pipeline), **C1** (Pure 1-pattern-per-task GoF), **C2** (Use Case in Task 3).
- Empirical verification: All 3 tasks in **C3** pass `ASTValidator.validate()` and `RunnerService.run_code()` (`status='PASSED'`).

→ **User decision:** Одобрена конфигурация **C3** и переход к финальному синтезу `RES.md` (сообщение Coordinator `5e1d1422-f45d-4f89-9d10-9eff76d814cb` от 2026-10-25T22:28:02Z).

**Stage complete:** YES
