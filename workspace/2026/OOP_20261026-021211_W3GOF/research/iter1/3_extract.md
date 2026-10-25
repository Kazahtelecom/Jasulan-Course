# Extract — "What do we NOT see?"
> **Mindset:** Analyst. You have the raw findings. Now build structure. Make combinations visible that nobody proposed.
> **Test:** "Does my configuration space reveal at least one combination that nobody proposed in the Briefing?"
> Parent: [HL-OOP_20261026-021211_W3GOF](../../HL-OOP_20261026-021211_W3GOF.md)
> Goal: Интегрировать заключительный учебный модуль Недели 3 («Паттерны GoF и Чистая Архитектура») на сквозном домене Avtobys с 4 шагами теории, интерактивной SVG UML-диаграммой под лупой 2.5×, 3 задачами тренажёра и 10 сбалансированными вопросами квиза на 20 баллов.
> Producer unit: `antigravity:thread:local:b44e12c6-d392-4cd9-a90a-763aa4936c08`
> Parent Coordinator: `antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb`
> Coordination authority: `HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`

## Configuration Space

Build the full solution space by cross-referencing Gather's dimensions. Use the same dimension names as column headers.

Do NOT evaluate yet — list all combinations that are not obviously contradictory.

| Config | D1: Распределение 4 тем курса (Лаб 6–9) между `WALKTHROUGH_EXAMPLE` и 3 слотами тренажёра (`w3_task_1..3`) | D2: Контракт синтаксической совместимости задач с белым списком `ASTValidator` | D3: Интеграция UI-шаблонов и интерактивной UML-диаграммы Недели 3 | D4: Архитектура банка вопросов квиза `w3_q1..w3_q10` и защита от угадывания |
|--------|-----------------|-----------------|-----------------|-----------------|
| **C1** | **Alt B (Builder в `w3_task_1`):**<br>• `WALKTHROUGH_EXAMPLE`: `TicketIssuer` (`Factory Method`, Лаб 6) + `BankApiAdapter` & `TransitTerminalFacade` (`Adapter` + `Facade`, Лаб 7)<br>• `w3_task_1`: `DailyShiftReport(frozen=True)` + `ShiftReportBuilder` с Fluent API и `IncompleteReportError` (Лаб 6)<br>• `w3_task_2`: `ValidationHandler` (`BlacklistCheckHandler`, `BalanceCheckHandler`) + `TransitTelemetrySubject` (`Observer`, Лаб 8)<br>• `w3_task_3`: `ValidateRideUseCase` + `Money` + `CardRepositoryPort` (Лаб 9) | **Alt A:** Чистый stdlib из `ALLOWED_MODULES` (`abc`, `dataclasses`, `decimal`, `typing`) без `time`/`re`/`__new__`/`__class__` | **Alt A:** Полная синхронизация 4 шаблонов (`header.html`, `uml_viewer.html`, `tab_theory.html`, `tab_practice.html`) + `app.js` | **Alt A + Alt D:** Сбалансированный 4-блочный квиз (2+3+3+2 по Лекциям 6–9) с включением контрольных вопросов защиты Лаб 6–9 |
| **C2** | **Alt C (Adapter в `w3_task_1`):**<br>• `WALKTHROUGH_EXAMPLE`: `TicketIssuer` + `ShiftReportBuilder` (Лаб 6)<br>• `w3_task_1`: `LegacyBankClient` + `BankApiAdapter` (перевод `Decimal` тенге в `int(amount * 100)` тиынов, Лаб 7)<br>• `w3_task_2`: `ValidationHandler` Chain (`BlacklistCheckHandler`, `BalanceCheckHandler`, Лаб 8)<br>• `w3_task_3`: `ValidateRideUseCase` + `CardRepositoryPort` + `PaymentGatewayPort` (Лаб 9) | **Alt A:** Чистый stdlib из `ALLOWED_MODULES` (`abc`, `dataclasses`, `decimal`, `typing`) | **Alt A:** Полная синхронизация 4 шаблонов + `app.js` | **Alt A + Alt D:** Сбалансированный 4-блочный квиз (2+3+3+2) |
| **C3 _(Новая комбинация, выявленная в Extract)_** | **Alt A/B+C (Двойной охват Лаб 6+7 в `w3_task_1` и Лаб 8 в `w3_task_2`):**<br>• `WALKTHROUGH_EXAMPLE`: `TicketIssuer` (`QrTicket`, `NfcTicket`, Лаб 6) + `TransitTerminalFacade` (`Facade`, Лаб 7)<br>• `w3_task_1`: `ShiftReportBuilder` (`DailyShiftReport`, Лаб 6) + `BankApiAdapter` (`LegacyBankClient`, перевод `Decimal` в тиыны `int(amount * 100)`, Лаб 7)<br>• `w3_task_2`: `ValidationHandler` (`BlacklistCheckHandler`, `BalanceCheckHandler`) + `TransitTelemetrySubject` (`attach`, `detach`, `notify`, Лаб 8)<br>• `w3_task_3`: `ValidateRideUseCase` + `Money` + `CardRepositoryPort` + `PaymentGatewayPort` (Лаб 9) | **Alt A + Alt B:** Чистый stdlib из `ALLOWED_MODULES` + явная передача параметров без `time`/`re` | **Alt A:** Полная синхронизация 4 шаблонов + `app.js` | **Alt A + Alt D:** Сбалансированный 4-блочный квиз (2+3+3+2) с концептуальными ловушками из контрольных вопросов Лаб 6–9 |
| **C4** | **Alt D:** Полный `simulator.py` в Walkthrough + `TimingDecorator` в `w3_task_2` | **Alt C:** Расширение `ASTValidator.ALLOWED_MODULES` модулями `time` и `re` | **Alt B:** Изменение только `header.html`, `uml_viewer.html`, `app.js` (без `tab_theory`/`tab_practice`) | **Alt B:** 9 вопросов по GoF + 1 по Clean Architecture |
| **C5** | **Alt B:** Builder в `w3_task_1`, Chain в `w3_task_2`, UseCase в `w3_task_3` | **Alt D:** Только примитивы `int`/`float`/`str` без `Decimal` и `@dataclass` | **Alt C:** Вынос заголовков `tab_theory`/`tab_practice` в новые поля `WeekModule` | **Alt C:** Все 10 вопросов — длинные листинги кода |

---

## Findings

### E1: Структурирование теоретического блока (`app/content/week_3/theory.py`) — 4 шага `THEORY_SECTIONS` и `WALKTHROUGH_EXAMPLE`

Сопоставление структуры `app/content/week_2/theory.py` с содержанием `RF__lecture_06..09.pdf` даёт точную схему для `app/content/week_3/theory.py`:

1. **`WEEK3_OVERVIEW`:**
   - `week_number`: `3`
   - `badge`: `"Неделя 3 · Паттерны GoF и Clean Architecture"`
   - `title`: `"Паттерны проектирования GoF и Чистая Архитектура: диспетчерский центр Avtobys"`
   - `subtitle`: `"Заключительный модуль по материалам Лекций 6–9 и Лабораторных 6–9 на сквозном домене транспортной системы Avtobys"`
   - `hero_image`: `"/static/images/week3_hero.jpg"`
   - `estimated_time`: `"Ориентир: 60 + 60 + 60 мин"`, `max_score`: `20.0`, `pass_threshold`: `12.0`
   - `roadmap`: 3 карточки (`01` — Теория: 9 паттернов GoF и 4 слоя Clean Architecture; `02` — Практика: Тренажёр · 0 баллов штрафа; `03` — Итоговое Тестирование Недели 3 · 20 баллов).

2. **`THEORY_SECTIONS` (4 шага, соответствующие Лекциям 6, 7, 8, 9):**
   - **Шаг 1 (`w3_step_1_creational`, Лекция 6):**
     - *Заголовок:* Порождающие паттерны GoF (`Factory Method`, `Abstract Factory`, `Builder`) и почему `Singleton` — антипаттерн.
     - *Иллюстрация:* `/static/images/week3_hero.jpg` (фабричный конвейер билетов и пошаговый сборщик отчёта рейса).
     - *Карточки анатомии (`anatomy_cards`, 4 шт.):* `Factory Method` (`TicketIssuer.create_ticket()`), `Abstract Factory` (семейства `AlmatyValidator` vs `AstanaValidator`), `Builder + Fluent API` (`ShiftReportBuilder().set_shift_info(...).build()` против `Telescoping Constructor`), `Антипаттерн Singleton` (`GlobalConfig` и 4 проблемы в `pytest -n 4` → замена на `AppConfig` + DI).
     - *Код «Плохо / Хорошо»:* жёсткое инстанциирование `QrTicket` и 12-аргументный конструктор отчёта vs `TicketIssuer` и `ShiftReportBuilder` с валидацией в `build()`.
   - **Шаг 2 (`w3_step_2_structural`, Лекция 7):**
     - *Заголовок:* Структурные паттерны GoF (`Adapter`, `Decorator`, `Facade`, `Proxy`): паттерны-обёртки без наследования.
     - *Иллюстрация:* `/static/images/gof_patterns.jpg` (схема адаптера банковского шлюза, матрёшки декораторов и единого фасада терминала).
     - *Карточки анатомии (4 шт.):* `Adapter` (`BankApiAdapter`: перевод `Decimal` тенге в тиыны `amount * 100` для `LegacyBankClient`, **меняет интерфейс**), `Decorator` (`TimingDecorator(RetryOnFailureDecorator(gateway))`, **сохраняет интерфейс**), `Facade` (`TransitTerminalFacade.tap()`, **упрощает интерфейс** к подсистемам), `Proxy` (`Virtual/Protection/Remote Proxy`, **сохраняет интерфейс** и контролирует доступ).
     - *Код «Плохо / Хорошо»:* прямой вызов несовместимого `LegacyBankClient.execute_payment_kzt` в тиынах прямо из терминала vs чистый `BankApiAdapter` и `TransitTerminalFacade`.
   - **Шаг 3 (`w3_step_3_behavioral`, Лекция 8):**
     - *Заголовок:* Поведенческие паттерны GoF (`Strategy`, `Observer`, `Chain of Responsibility`, `Command`, `State`).
     - *Иллюстрация:* `/static/images/gof_patterns.jpg`.
     - *Карточки анатомии (4 шт.):* `Chain of Responsibility` (`ValidationHandler`: `BlacklistCheckHandler` → `AntiFraudCooldownHandler` → `BalanceCheckHandler` с прерыванием Short-circuit), `Observer / Pub-Sub` (`TransitTelemetrySubject.notify()` + изоляция ошибок подписчиков `MetricsCollectorObserver`, `SecurityAlertObserver`), `Strategy vs State` (`FraudCheckStrategy` выбирается клиентом vs `IdleState → ReadingState` меняется самим автоматом), `Command` (`SyncTransactionCommand` для офлайн-очереди в тоннеле).
     - *Код «Плохо / Хорошо»:* вложенный спагетти-блок из 4 `if` и жёстких вызовов логгеров vs модульная цепочка `ValidationHandler` и `TransitTelemetrySubject`.
   - **Шаг 4 (`w3_step_4_clean_arch`, Лекция 9):**
     - *Заголовок:* Чистая Архитектура (`Clean Architecture`), Правило зависимостей (`The Dependency Rule`) и запахи кода (`Code Smells`).
     - *Иллюстрация:* `/static/images/clean_arch_layers.jpg` (4 концентрических слоя Clean Architecture с направлением зависимостей внутрь).
     - *Карточки анатомии (4 шт.):* `The Dependency Rule` (зависимости `import` направлены только внутрь к `Domain`), `Domain (Entities & Value Objects)` (`TransitCard`, `Bus`, иммутабельные `Money` и `PlateNumber` против `Primitive Obsession`), `Application (Use Cases & Ports)` (`ValidateRideUseCase`, `CardRepositoryPort`, `PaymentGatewayPort`), `Code Smells (Фаулер)` (`Divergent Change` vs `Shotgun Surgery`, `Feature Envy`, `Refused Bequest`).
     - *Код «Плохо / Хорошо»:* Use Case с прямым `import sqlite3` и сырым `float` vs чистый `ValidateRideUseCase`, опирающийся на протоколы портов и доменный `Money`.

3. **`WALKTHROUGH_EXAMPLE` (построчный разбор на 4 шага):**
   - Охватывает `TicketIssuer` (`Factory Method`, Лаб 6) + `TransitTerminalFacade` (`Facade`, Лаб 7), чтобы все 4 лабораторные работы (Лаб 6–9) были представлены в коде модуля!

---

### E2: Сопоставление конфигураций `C1`, `C2`, `C3` для 3 задач тренажёра (`app/content/week_3/practice.py`)

Анализ конфигураций `C1` (`Alt B`), `C2` (`Alt C`) и гибридной `C3` показывает, что **конфигурация `C3`** (где `WALKTHROUGH_EXAMPLE` разбирает `Factory Method` + `Facade`, а в 3 задачах тренажёра студент последовательно собирает:
- **`w3_task_1`:** `ShiftReportBuilder` и `DailyShiftReport` из Лаб 6 **плюс** `BankApiAdapter` и `LegacyBankClient` из Лаб 7,
- **`w3_task_2`:** конвейер `ValidationHandler` (`BlacklistCheckHandler`, `BalanceCheckHandler`) **плюс** издатель `TransitTelemetrySubject` из Лаб 8,
- **`w3_task_3`:** доменный `Money`, `TransitCard` и сценарий `ValidateRideUseCase` из Лаб 9)
обеспечивает **100% покрытие канонических классов всех четырёх лабораторных работ (Лаб 6, Лаб 7, Лаб 8, Лаб 9)** и при этом удерживает объём каждой задачи в пределах **30–44 строк кода**!

Точные сигнатуры классов и методов в `C3` (полностью совпадающие с `RF__lab_06..09.pdf`):
- **Задача 1 (`w3_task_1` — Лаб 6 Builder + Лаб 7 Adapter):**
  - `@dataclass(frozen=True) class DailyShiftReport`: поля `route_id: str`, `driver_id: str`, `total_revenue: Decimal`, `incidents: tuple[str, ...] = ()`.
  - `class IncompleteReportError(ValueError): pass`
  - `class ShiftReportBuilder`:
    - `set_shift_info(self, route_id: str, driver_id: str) -> "ShiftReportBuilder"` (возвращает `self`)
    - `add_qr_revenue(self, amount: Decimal) -> "ShiftReportBuilder"` (прибавляет `amount` к выручке, возвращает `self`)
    - `record_incident(self, description: str) -> "ShiftReportBuilder"` (добавляет описание инцидента, возвращает `self`)
    - `build(self) -> DailyShiftReport` (если `not self._route_id or not self._driver_id` → выбрасывает `IncompleteReportError`; иначе возвращает `DailyShiftReport(...)`).
  - `class LegacyBankClient`: `execute_payment_kzt(self, source_pan: str, dest_account: str, amount_tiyn: int) -> dict` (возвращает `{"auth_code": f"AUTH-{source_pan}-{amount_tiyn}"}`).
  - `class BankApiAdapter`: `__init__(self, external_client: LegacyBankClient, transit_account: str)` и `charge(self, card_id: str, amount: Decimal) -> str` (переводит тенге в тиыны `amount_tiyn = int(amount * 100)`, вызывает `execute_payment_kzt` и возвращает `res["auth_code"]`).
- **Задача 2 (`w3_task_2` — Лаб 8 Chain of Responsibility + Observer):**
  - `@dataclass class PaymentRequest`: `card_id: str`, `balance: Decimal`, `fare: Decimal`, `blacklisted_cards: set[str] = field(default_factory=set)`.
  - `@dataclass(frozen=True) class ValidationResult`: `is_approved: bool`, `reason: str = "OK"`.
  - `class ValidationHandler(ABC)`: `set_next(self, handler: "ValidationHandler") -> "ValidationHandler"`, `handle(self, request: PaymentRequest) -> ValidationResult`.
  - `class BlacklistCheckHandler(ValidationHandler)`: если `request.card_id in request.blacklisted_cards`, возвращает `ValidationResult(is_approved=False, reason="Карта в черном списке")`, иначе передаёт `super().handle(request)`.
  - `class BalanceCheckHandler(ValidationHandler)`: если `request.balance < request.fare`, возвращает `ValidationResult(is_approved=False, reason="Недостаточно средств")`, иначе передаёт `super().handle(request)`.
  - `class TransitTelemetrySubject`: `attach(self, observer) -> None`, `detach(self, observer) -> None`, `notify(self, event: str) -> None` (вызывает `observer.update(event)` для всех активных подписчиков).
- **Задача 3 (`w3_task_3` — Лаб 9 Clean Architecture Use Case):**
  - `@dataclass(frozen=True) class Money`: `amount: Decimal`, `currency: str = "KZT"`.
  - `@dataclass class TransitCard`: `card_id: str`, `balance: Decimal`, метод `charge_fare(self, fare: Money) -> None` (если `self.balance < fare.amount` → `raise ValueError("Insufficient funds")`, иначе уменьшает `self.balance -= fare.amount`).
  - `@dataclass(frozen=True) class ValidateRideRequest`: `card_id: str`, `fare_amount: Decimal`.
  - `@dataclass(frozen=True) class ValidateRideResponse`: `success: bool`, `remaining_balance: Decimal`, `tx_id: str`.
  - `class ValidateRideUseCase`: `__init__(self, card_repo, payment_gateway)` и `execute(self, request: ValidateRideRequest) -> ValidateRideResponse` (1. получает карту `card = self._card_repo.get_by_id(request.card_id)`, 2. создаёт `fare = Money(request.fare_amount)`, 3. списывает `card.charge_fare(fare)`, 4. проводит платёж `tx_id = self._payment_gateway.charge(card.card_id, fare.amount)`, 5. сохраняет `self._card_repo.save(card)`, 6. возвращает `ValidateRideResponse(success=True, remaining_balance=card.balance, tx_id=tx_id)`).

---

### E3: Архитектура SVG-схемы `svg-week3` и точек интеграции UI/API

1. **Точки интеграции в бэкенде:**
   - `app/content/week_3/__init__.py`: экспортирует `WEEK3_OVERVIEW`, `THEORY_SECTIONS`, `WALKTHROUGH_EXAMPLE`, `PRACTICE_TASKS`, `QUIZ_QUESTIONS`, `evaluate_quiz`.
   - `app/modules/registry.py`: регистрирует `WeekModule(week_number=3, title="Паттерны GoF и Чистая Архитектура", ...)`.
   - `app/services/scoring.py`: дополняет `WEEK_TASK_IDS` записью `3: ("w3_task_1", "w3_task_2", "w3_task_3")`.
   - `app/routers/week3.py`, `app/routers/__init__.py`, `app/main.py`: делегирующий роутер `/week3` и `/api/week3/{progress,practice/{task_id}/run,quiz/check,quiz/evaluate,theory/complete}` по образцу `week2.py`.
2. **Точки интеграции в UI-шаблонах и JS:**
   - `app/templates/components/header.html` (строки 60–63): замена `<button onclick="showLockedWeekToast(...)">` на `<a href="/week3" class="{% if active_week|default(1) == 3 %}week-pill-active font-bold{% else %}...{% endif %} ...">Неделя 3 · Паттерны GoF</a>`.
   - `app/templates/components/tab_theory.html` (строка 6) и `app/templates/components/tab_practice.html` (строки 19, 47): добавление ветки `{% elif active_week|default(1) == 3 %}` с описанием паттернов GoF и Clean Architecture (`example_gof_clean_arch.py`, `ShiftReportBuilder`, `ValidationHandler`, `ValidateRideUseCase`).
   - `app/templates/components/uml_viewer.html`:
     - Добавление кнопки вкладки `data-diagram-tab="week3"` (`onclick="switchUmlDiagramTab('week3')"`, `🚀 Неделя 3: GoF & Clean Architecture`), активной при `active_week == 3`.
     - Добавление панели `<div id="uml-diagram-week3" class="uml-diagram-pane w-full {% if active_week|default(1) != 3 %}hidden{% endif %}">` с векторной схемой `<svg id="svg-week3" viewBox="0 0 1120 560" ...>`.
     - Строго автономный блок `<defs>` внутри `svg-week3` (`shadow-box-w3`, `g-header-domain-w3`, `g-header-usecase-w3`, `g-header-gof-w3`, `arrow-dep-w3`, `arrow-impl-w3`), чтобы пройти проверку `test_uml_svgs_have_self_contained_defs` в `tests/test_uml_viewer.py`!
     - Компоновка `svg-week3` без пересечений координат (4 колонки по горизонтали `x = 30..1090`):
       1. *Слой Presentation / Facade (`x=30..270`):* `TransitTerminalFacade` + `ShiftReportBuilder` (Лаб 6–7).
       2. *Слой Behavioral Pipeline (`x=310..560`):* `ValidationHandler` (`BlacklistCheck`, `BalanceCheck`) + `TransitTelemetrySubject` (`Observer`, Лаб 8).
       3. *Слой Application Use Cases & Ports (`x=600..850`):* `ValidateRideUseCase` + `<<interface>> CardRepositoryPort` + `<<interface>> PaymentGatewayPort` (Лаб 9).
       4. *Слой Domain Entities & Infrastructure Adapters (`x=880..1095`):* вверху `Domain: TransitCard & Money` (`0 внешних зависимостей`), внизу `BankApiAdapter -> LegacyBankClient` (Лаб 7/9, реализует `PaymentGatewayPort` по `The Dependency Rule`).
   - `app/static/js/app.js`:
     - Строка 691: `let currentUmlTab = ACTIVE_WEEK === "3" ? "week3" : (ACTIVE_WEEK === "2" ? "week2" : "week1");`
     - В `switchUmlDiagramTab(tabKey)`: обработка `else if (tabKey === "week3")` и `ACTIVE_WEEK === "3"`.
     - В `openUmlFullscreen()`: заголовок для `week3` (`"UML-диаграмма классов: Неделя 3 (Паттерны GoF и Clean Architecture)"`).

---

### E4: Спецификация матрицы 10 вопросов квиза (`app/content/week_3/quiz.py`)

Для гарантированного прохождения `test_quiz_balance_and_traps` (`tests/test_ui_ergonomics.py`) матрица 10 вопросов строится со следующими параметрами:
- **Распределение `correct_index`:**
  - Индекс `0` (`A`): 2 раза (`w3_q2`, `w3_q7`)
  - Индекс `1` (`B`): 3 раза (`w3_q3`, `w3_q6`, `w3_q9`)
  - Индекс `2` (`C`): 3 раза (`w3_q1`, `w3_q5`, `w3_q10`)
  - Индекс `3` (`D`): 2 раза (`w3_q4`, `w3_q8`)
  *(Все индексы `0..3` встречаются от 2 до 3 раз — строго в рамках `2 <= count <= 3`)*.
- **Тематическое распределение и концептуальные ловушки по Лекциям 6–9:**
  - `w3_q1` (Лекция 6 · `Factory Method` vs `Static Factory`): полиморфный `TicketIssuer.create_ticket()` и соблюдение `OCP` (`correct_index: 2`).
  - `w3_q2` (Лекция 6 · `Builder` + `Fluent API`): пошаговая сборка иммутабельного `DailyShiftReport(frozen=True)` через `ShiftReportBuilder` и валидация в `build()` против `Telescoping Constructor` (`correct_index: 0`).
  - `w3_q3` (Лекция 6 · Антипаттерн `Singleton`): почему глобальный мутабельный `GlobalConfig` вызывает случайные падения параллельных тестов (`pytest -n 4`) и как это решается через `AppConfig` + DI (`correct_index: 1`).
  - `w3_q4` (Лекция 7 · `Adapter` vs `Decorator`): ключевое отличие `BankApiAdapter` (меняет интерфейс `LegacyBankClient` в тиынах под `PaymentGateway` в тенге) от `TimingDecorator` (сохраняет тот же интерфейс) (`correct_index: 3`).
  - `w3_q5` (Лекция 7 · `Decorator` vs Наследование): сборка цепочки `TimingDecorator(RetryOnFailureDecorator(CoreGateway))` как «матрёшки» без комбинаторного взрыва подклассов (`correct_index: 2`).
  - `w3_q6` (Лекция 7 · `Facade` vs `God Object`): как `TransitTerminalFacade.tap()` упрощает вызов подсистем без переноса внутрь себя их бизнес-логики (`correct_index: 1`).
  - `w3_q7` (Лекция 8 · `Chain of Responsibility` Short-circuiting): прерывание цепочки `ValidationHandler` в `BlacklistCheckHandler` без вызова `BalanceCheckHandler` и списания (`correct_index: 0`).
  - `w3_q8` (Лекция 8 · `Observer` & изоляция подписчиков): слабая связанность `TransitTelemetrySubject` и почему сбой в одном наблюдателе не должен ломать публикацию транзакции (`correct_index: 3`).
  - `w3_q9` (Лекция 8 · `Strategy` vs `State`): отличие выбора алгоритма `FraudCheckStrategy` клиентом от переходов состояний `IdleState -> ReadingState` внутри FSM терминала (`correct_index: 1`).
  - `w3_q10` (Лекция 9 · `Clean Architecture` & `The Dependency Rule` + `Code Smells`): направление зависимостей внутрь к `Domain` (`ValidateRideUseCase` → `CardRepositoryPort` ← `SqliteCardRepository`) и устранение `Primitive Obsession` через `Money` (`correct_index: 2`).

---

## Checkpoint

| Found | Remaining |
|-------|-----------|
| Построено пространство из 5 конфигураций (`C1–C5`), включая новую гибридную конфигурацию **`C3`**, которая объединяет в 3 задачах тренажёра + Walkthrough все 4 лабораторные работы (Лаб 6–9). | На стадии **Challenge** (`4_challenge.md`) протестировать конфигурацию `C3` (и альтернативы `C1`/`C2`) против реального `ASTValidator.validate()`, `pytest` в песочнице и математических ограничений `test_ui_ergonomics.py`. |
| Детализированы точные контракты всех 4 шагов теории, `WALKTHROUGH_EXAMPLE`, 3 задач тренажёра (`w3_task_1..3`), SVG-схемы `svg-week3` и матрицы 10 вопросов квиза (`w3_q1..w3_q10`). | В `4_challenge.md` отсеять слабые конфигурации (`C4`, `C5`) и зафиксировать выжившую конфигурацию для синтеза в `RES.md`. |

**Sufficiency:**
- [x] External source used?
- [x] Briefing gap closed?
- [x] Configuration Space built from Gather dimensions?

### Knowledge Handover (Stage 3 Extract Checkpoint)
- **Producer / Unit:** Researcher (`antigravity:thread:local:b44e12c6-d392-4cd9-a90a-763aa4936c08`), parent Coordinator (`antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb`).
- **Source / Version:** `HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`, `2_gather.md`, `app/content/week_2/{theory,practice,quiz}.py`, `tests/{test_ui_ergonomics,test_uml_viewer,test_week_modules}.py`, `app/modules/base.py`, `app/main.py`.
- **Inspected Scope:** 8 файлов кодовой базы и тестов + 1 внешний веб-поиск по Fluent Builder (`dataclass(frozen=True)`), Chain of Responsibility и Clean Architecture Ports (`typing.Protocol`).
- **Material Outcome:** Сформировано пространство конфигураций `C1–C5`; выявлена гибридная конфигурация `C3`, обеспечивающая 100% покрытие Лаб 6–9 при сохранении компактного размера задач (30–44 строк); спроектирована 4-колоночная топология `svg-week3` с автономным `<defs>` и матрица квиза `w3_q1..w3_q10`.
- **Remaining Uncertainty:** Эмпирическая верификация кода `w3_task_1..3` и баланса вариантов квиза на стадии **Challenge** (`4_challenge.md`).
- **Continuation:** Ожидание подтверждения Координатора (`5e1d1422-f45d-4f89-9d10-9eff76d814cb`) для перехода к стадии **Challenge** (`4_challenge.md`).

Stage complete: YES
→ User decision: Подтверждено закрытие стадии Extract и переход к Challenge (`4_challenge.md`) с приоритетным стресс-тестированием гибридной конфигурации `C3` против `C1`/`C2`/`C4`/`C5`.
