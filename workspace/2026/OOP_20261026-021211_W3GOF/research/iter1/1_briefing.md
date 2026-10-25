# Briefing — "What should we investigate?"
> **Mindset:** Strategist. You're planning an investigation, not doing it. Frame what matters. Resist solving.
> **Test:** "Can I explain WHY we're investigating this and what would change our approach?"
> Parent: [HL-OOP_20261026-021211_W3GOF](../../HL-OOP_20261026-021211_W3GOF.md)
> Goal: Интегрировать заключительный учебный модуль Недели 3 («Паттерны GoF и Чистая Архитектура») на сквозном домене Avtobys с 4 шагами теории, интерактивной SVG UML-диаграммой под лупой 2.5×, 3 задачами тренажёра и 10 сбалансированными вопросами квиза на 20 баллов.
> Producer unit: `antigravity:thread:local:b44e12c6-d392-4cd9-a90a-763aa4936c08`
> Parent Coordinator: `antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb`
> Activation / dispatch source: `owner-direct` (`/tfw-research OOP_20261026-021211_W3GOF`) + Coordinator transition/dispatch `journal/20261026-031035__transition__c9f4.md`
> Coordination authority: `HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`
> Originating proposer: `{principal: zhasulan, unit: antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb}`

## Research Plan

### Stage 1: Gather (Сбор фактов и декомпозиция измерений)
- Извлечь структуру, доменные классы, сигнатуры методов, бизнес-правила и примеры кода из 4 авторских лекций (`01_Лекции\RF__lecture_06..09.pdf`) и 4 лабораторных работ (`02_Лабораторные\RF__lab_06..09.pdf`) в `C:\Users\kz444\OneDrive\Desktop\OOP`.
- Проверить белый список узлов, атрибутов, встроенных функций и модулей в `app/services/ast_validator.py` на предмет совместимости конструкций из Лабораторных 6–9 (например, `abc.ABC`, `@abstractmethod`, `dataclasses`, `typing.Protocol`, `Callable`, цепочка вызовов, свойства и паттерн `Builder`).
- Провести аудит точек интеграции Недели 3 в кодовой базе (`app/modules/base.py`, `app/modules/registry.py`, `app/routers/weeks.py`, `app/routers/week2.py`, `app/services/scoring.py`, `app/templates/components/{header,uml_viewer,tab_home,tab_results}.html`, `app/static/js/app.js`, `tests/test_ui_ergonomics.py`, `tests/test_uml_viewer.py`, `tests/test_week_modules.py`).
- Выполнить внешнюю сверку (external research) канонических определений и типичных антипаттернов/ловушек по GoF (`Factory Method`, `Builder`, `Adapter`, `Decorator`, `Facade`, `Strategy`, `Observer`, `Chain of Responsibility`) и `Clean Architecture` (`Dependency Rule`, `Entities` vs `Use Cases` vs `Interface Adapters`) для проектирования дистракторов квиза.
- **Ожидаемые оси решений (Dimensions для декомпозиции в Gather):**
  - *D1 (Доменные контракты тренажёра `w3_task_1..3` и `WALKTHROUGH_EXAMPLE`):* отбор 3 репрезентативных задач из Лабораторных 6–9, покрывающих порождающие/структурные GoF, поведенческие GoF и Clean Architecture Use Case.
  - *D2 (Совместимость с песочницей `ASTValidator`):* допустимый подмножество синтаксиса Python для решений и тестов без ослабления безопасности (`D9`/`F7`).
  - *D3 (Топология SVG UML-схемы `svg-week3` и UI-маршрутизации):* компоновка узлов GoF + Clean Architecture в `uml_viewer.html` и связка вкладок в `app.js` / `header.html`.
  - *D4 (Матрица 10 вопросов квиза `w3_q1..w3_q10`):* распределение тем Лекций 6–9, концептуальных ловушек и ограничений баланса (`min_len >= 60`, `max_len / min_len <= 1.65`, `correct_index` по 2–3 раза).

### Stage 2: Extract (Формирование пространства конфигураций)
- Сопоставить извлечённые из `RF__lab_06..09.pdf` задачи с 3 слотами тренажёра (`w3_task_1`, `w3_task_2`, `w3_task_3`) и `WALKTHROUGH_EXAMPLE`, зафиксировав точные имена классов, сигнатуры методов и инварианты проверочных `test_code`.
- Сформировать конфигурацию 4 шагов `THEORY_SECTIONS` (карточки анатомии, блоки «Плохо / Хорошо», привязка 3 иллюстраций `week3_hero.jpg`, `gof_patterns.jpg`, `clean_arch_layers.jpg`).
- Спроектировать структуру векторной диаграммы `uml-diagram-week3` (`svg-week3`) и точечные изменения в `header.html`, `uml_viewer.html`, `app.js`, `scoring.py`, `registry.py` и `week3.py`.
- Составить спецификацию 10 вопросов квиза (`w3_q1..w3_q10`) с распределением правильных индексов `[0, 1, 2, 3]` и тематических ловушек по Лекциям 6–9.

### Stage 3: Challenge (Стресс-тестирование конфигураций и граничных случаев)
- Проверить кандидатов кода для `w3_task_1..3` (и их `test_code`) против реальных правил `ASTValidator` (`ALLOWED_MODULES`, `ALLOWED_BUILTINS`, запрет dunder-атрибутов кроме `__init__`, лимит 15 КБ) и ограничения когнитивной нагрузки для начинающих (25–45 строк).
- Проверить устойчивость SVG-схемы `svg-week3` к наложению текста и работе интерактивной лупы 2.5× (`initUmlViewer`, `switchUmlDiagram('week3')`).
- Проверить потенциальные граничные случаи в `ScoringService` (`WEEK_TASK_IDS[3]`, `week_3_theory`, `week_3_quiz`), `test_ui_ergonomics.py` и существующих dirty-файлах рабочего дерева (`uml_viewer.html`, `test_uml_viewer.py`).

## Hypotheses (from HL §10)

| # | Hypothesis | HL Status |
|---|-----------|-----------|
| **H1** | В исходных PDF-материалах Лекций 6–9 и Лабораторных 6–9 (`C:\Users\kz444\OneDrive\Desktop\OOP`) используется сквозная доменная модель транспортной системы Avtobys (строитель финансовых отчётов / фабрика, адаптер / декоратор / фасад терминала, цепочка обязанностей / наблюдатель мониторинга, Use Case симулятора смены автобуса), из которой можно выделить 3 компактные in-memory задачи тренажёра (`w3_task_1..3`), полностью совместимые с текущим белым списком `ASTValidator` без ослабления безопасности песочницы. | open |
| **H2** | Существующие Jinja2-компоненты (`tab_home.html`, `tab_theory.html`, `tab_practice.html`, `tab_quiz.html`, `tab_results.html`) и клиентский контроллер `app/static/js/app.js` требуют для полной поддержки Недели 3 изменений только в `header.html` (ссылка `/week3`), `uml_viewer.html` (вкладка и SVG `week3`) и `app.js` (инициализация и переключение `currentUmlTab` для `ACTIVE_WEEK === "3"`). | open |

## Scope Intent
- **In scope:**
  - Чтение и извлечение точных доменных классов/методов из `01_Лекции\RF__lecture_06..09.pdf` и `02_Лабораторные\RF__lab_06..09.pdf`.
  - Анализ `app/services/ast_validator.py`, `app/services/scoring.py`, `app/modules/{base,registry}.py`, `app/routers/{weeks,week2}.py`, `app/templates/components/*.html`, `app/static/js/app.js` и тестов `tests/test_*.py`.
  - Внешняя верификация классических инвариантов GoF и Clean Architecture для построения концептуальных ловушек квиза.
  - Подготовка полных спецификаций для `TS` (контракты `w3_task_1..3`, структура 4 шагов теории, `WALKTHROUGH_EXAMPLE`, `svg-week3`, матрица квиза).
- **Out of scope:**
  - Написание продуктового кода в `app/` или тестов в `tests/` (Role Lock: только артефакты `research/`).
  - Разработка финального экзаменационного модуля (выходит за рамки Недели 3).
  - Изменение схемы таблиц SQLite или отказ от нативной песочницы `ASTValidator` (`F7`).

## Guiding Questions
1. **Отбор 3 задач тренажёра (`w3_task_1..3`) на 4 лабораторные работы (Лаб 6–9):** Поскольку в тренажёре 3 слота (`w3_task_1..3`), а лабораторных четыре (Лаб 6 — Порождающие, Лаб 7 — Структурные, Лаб 8 — Поведенческие, Лаб 9 — Clean Architecture), подтверждаете ли вы распределение: одна тема выносится в подробный построчный разбор `WALKTHROUGH_EXAMPLE`, а остальные три идут в задачи `w3_task_1`, `w3_task_2`, `w3_task_3` (с окончательным выбором пар после чтения `RF__lab_06..09.pdf` в Gather)?
2. **Приоритет именования классов:** Должны ли имена классов и сигнатуры методов в `w3_task_1..3` и `WALKTHROUGH_EXAMPLE` на 100% совпадать с именами из `RF__lab_06..09.pdf` (с упрощением только внутренней логики до 25–45 строк для начинающих)?

## User Direction
- Режим исследования подтверждён Координатором: `focused` (`loops_per_stage: 1`).
- **Ответ по Q1 (распределение 4 тем Лаб 6–9):** Подтверждено. Одна тема (или сквозная связка порождающих/структурных паттернов) выносится в построчный разбор `WALKTHROUGH_EXAMPLE`, а 3 слота тренажёра распределяются по `HL §3`: `w3_task_1` (Порождающий / структурный паттерн GoF из Лаб 6/7), `w3_task_2` (Поведенческий паттерн GoF из Лаб 8), `w3_task_3` (Use Case Чистой Архитектуры из Лаб 9).
- **Ответ по Q2 (канонические имена):** Подтверждено. Сохранить точные канонические имена классов и сигнатуры методов из `RF__lab_06..09.pdf` и `RF__lecture_06..09.pdf`, адаптируя только объём внутренней логики (25–45 строк для начинающих по `F5`) и обеспечивая 100% совместимость с белым списком `ASTValidator` (`D9`/`F7`).

### Knowledge Handover (Stage 1 Briefing Checkpoint)
- **Producer / Unit:** Researcher (`antigravity:thread:local:b44e12c6-d392-4cd9-a90a-763aa4936c08`), parent Coordinator (`antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb`).
- **Source / Version:** `HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`, `research/iterations.yaml`, `KNOWLEDGE.md` (`D2, D6–D11, F1–F9`).
- **Inspected Scope:** Управляющие артефакты задачи и база знаний `knowledge/records/REC-*` (входящих конфликтов или непринятых преемников не обнаружено).
- **Material Outcome:** Justified-none на стадии Briefing (сформирован план исследования и декомпозиция осей `D1–D4`, эмпирическое извлечение начнётся на стадии Gather).
- **Remaining Uncertainty:** Содержимое PDF-файлов `RF__lecture_06..09.pdf` и `RF__lab_06..09.pdf` (`H1`) и проверка шаблонов/скриптов UI (`H2`).
- **Continuation:** Ожидание подтверждения Briefing от Координатора (`5e1d1422-f45d-4f89-9d10-9eff76d814cb`) для перехода к стадии `2_gather.md`.

---
Stage complete: YES
