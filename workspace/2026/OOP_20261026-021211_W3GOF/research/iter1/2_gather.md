# Gather — "What do we NOT know?"
> **Mindset:** Explorer. You're mapping unknown territory. Widen before you narrow. Every assumption is a question.
> **Test:** "Can I name every dimension and its alternatives without checking my sources?"
> Parent: [HL-OOP_20261026-021211_W3GOF](../../HL-OOP_20261026-021211_W3GOF.md)
> Goal: Интегрировать заключительный учебный модуль Недели 3 («Паттерны GoF и Чистая Архитектура») на сквозном домене Avtobys с 4 шагами теории, интерактивной SVG UML-диаграммой под лупой 2.5×, 3 задачами тренажёра и 10 сбалансированными вопросами квиза на 20 баллов.
> Producer unit: `antigravity:thread:local:b44e12c6-d392-4cd9-a90a-763aa4936c08`
> Parent Coordinator: `antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb`
> Coordination authority: `HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`

## Dimensions

Identify the independent decision factors in this problem. Each dimension represents a degree of freedom — a variable the final solution must choose a value for.

For each dimension, list ≥3 alternatives. Do NOT mark any alternative as "recommended" — all options remain open until Challenge.

| Dimension | Alt A | Alt B | Alt C | Alt D _(if any)_ |
|-----------|-------|-------|-------|-----------------|
| **D1: Распределение 4 тем курса (Лаб 6–9) между `WALKTHROUGH_EXAMPLE` и 3 слотами тренажёра (`w3_task_1..3`)** | **Walkthrough:** `Factory Method` (`TicketIssuer` / `QrTicket`, `NfcTicket`) + `Facade` (`TransitTerminalFacade`)<br>**`w3_task_1`:** `ShiftReportBuilder` (Лаб 6) + `BankApiAdapter` (Лаб 7)<br>**`w3_task_2`:** `ValidationHandler` Chain + `TransitTelemetrySubject` Observer (Лаб 8)<br>**`w3_task_3`:** `ValidateRideUseCase` Clean Architecture (Лаб 9) | **Walkthrough:** `TransitTerminalFacade` + `BankApiAdapter` (Лаб 7 — Структурные)<br>**`w3_task_1`:** `ShiftReportBuilder` и `DailyShiftReport` (Лаб 6 — Порождающий Builder с Fluent API)<br>**`w3_task_2`:** `ValidationHandler` (`BlacklistCheckHandler`, `BalanceCheckHandler`) или `TransitTelemetrySubject` (Лаб 8 — Поведенческий)<br>**`w3_task_3`:** `ValidateRideUseCase` с портами `CardRepositoryPort` и `PaymentGatewayPort` (Лаб 9 — Clean Architecture) | **Walkthrough:** `ShiftReportBuilder` + `TicketIssuer` (Лаб 6 — Порождающие)<br>**`w3_task_1`:** `BankApiAdapter` + `LegacyBankClient` (Лаб 7 — Структурный Adapter тиынов KZT)<br>**`w3_task_2`:** `ValidationHandler` Chain of Responsibility (Лаб 8 — Поведенческий конвейер)<br>**`w3_task_3`:** `ValidateRideUseCase` (Лаб 9 — Clean Architecture Use Case) | **Walkthrough:** Полный симулятор `simulator.py` (Лаб 9)<br>**`w3_task_1`:** `TicketIssuer` (Лаб 6)<br>**`w3_task_2`:** `TimingDecorator` + `RetryOnFailureDecorator` (Лаб 7)<br>**`w3_task_3`:** `TransitTelemetrySubject` (Лаб 8) |
| **D2: Контракт синтаксической совместимости задач с белым списком `ASTValidator`** | **Чистый stdlib из `ALLOWED_MODULES`:** использовать только `abc`, `dataclasses`, `decimal`, `typing`, `datetime`, `enum` без `time`/`re` и без обращения к `__class__`/`__new__` | **In-memory инъекция времени/правил:** для задач с таймингом или форматом госномера передавать значения явно аргументами (без `import time` и `import re`) при сохранении `ASTValidator` неизменным | **Расширение `ASTValidator.ALLOWED_MODULES`:** добавить модули `time` и `re` в `app/services/ast_validator.py` | **Без внешних импортов вообще:** писать задачи только на встроенных типах `int`, `float`, `str`, `dict`, `list` без `decimal` и `dataclasses` |
| **D3: Интеграция UI-шаблонов и интерактивной UML-диаграммы Недели 3** | **Полная синхронизация 4 шаблонов + `app.js`:** обновить `header.html` (ссылка `/week3`), `uml_viewer.html` (вкладка и `svg-week3`), `app.js` (`ACTIVE_WEEK === "3"`), а также добавить ветки `{% elif active_week|default(1) == 3 %}` в `tab_theory.html` и `tab_practice.html` | **Строго по исходной формулировке H2:** менять только `header.html`, `uml_viewer.html` и `app.js` без правок в `tab_theory.html` и `tab_practice.html` | **Динамизация заголовков через `WeekModule`:** вынести строки заголовков `tab_theory.html` и `tab_practice.html` в поля `overview` / `walkthrough` контекста `WeekModule` | **Отдельный шаблон `week3.html`:** создать собственный HTML-шаблон для Недели 3 вместо общих компонентов |
| **D4: Архитектура банка вопросов квиза `w3_q1..w3_q10` и защита от угадывания** | **Сбалансированный 4-блочный квиз (2+3+3+2):** 2 вопроса по Лекции 6 (Creational + Singleton trap), 3 по Лекции 7 (Adapter vs Decorator vs Facade vs Proxy), 3 по Лекции 8 (Strategy vs State, Observer isolation, CoR short-circuit), 2 по Лекции 9 (Dependency Rule, Use Cases vs Entities + Code Smells), с проверкой в `test_ui_ergonomics.py` | **Равномерный 9+1 квиз:** по 1 вопросу на каждый из 9 паттернов GoF + 1 вопрос по Clean Architecture | **Практико-ориентированный квиз по коду Лаб 6–9:** все 10 вопросов содержат фрагменты кода из `RF__lab_06..09.pdf` с вопросом «какой паттерн применён / какая строка нарушает контракт» | **Квиз по контрольным вопросам защиты Лаб 6–9:** 10 вопросов, составленных напрямую из разделов «4. Контрольные вопросы для защиты работы» в `RF__lab_06..09.pdf` и `RF__lecture_06..09.pdf` |

---

## Findings

### G1: Авторские материалы Лекций 6–9 и Лабораторных 6–9 (`C:\Users\kz444\OneDrive\Desktop\OOP`) — канонические классы и сигнатуры домена Avtobys

Полное чтение 8 PDF-документов курса CS2203 (автор: PhD Санжар Аубакиров, КазНУ им. аль-Фараби) подтвердило гипотезу **H1** в части сквозного домена Avtobys и позволило извлечь точные канонические имена классов, методов и исключений:

1. **Лекция 6 (`RF__lecture_06.pdf`) и Лабораторная №6 (`RF__lab_06.pdf`) — Порождающие паттерны GoF (`Factory Method`, `Abstract Factory`, `Builder`) и антипаттерн `Singleton`:**
   - **Factory Method (Блок 1 Лаб 6 / Лекция 6 §2.1):**
     - Абстрактный билет `Ticket(ABC)` с методами `get_token() -> str` и `calculate_vat() -> Decimal` (расчёт НДС 12%; в Лекции 6 также показан упрощённый `get_payload() -> str`).
     - Конкретные билеты: `QrTicket` (`qr_payload`, TTL 15 мин), `NfcTicket` / `NfcTokenTicket` (серийный номер чипа и криптоподпись), `PaperSlipTicket` (фискальный чек и номер терминала).
     - Абстрактный эмитент `TicketIssuer(ABC)` с фабричным методом `@abstractmethod def create_ticket(self, fare: Decimal) -> Ticket` и шаблонным методом `issue_and_log(self, fare: Decimal) -> Ticket` / клиентской функцией `issue_ticket_to_passenger(issuer: TicketIssuer, fare: Decimal)`.
     - Конкретные фабрики: `QrTicketIssuer`, `NfcTicketIssuer`, `PaperTicketIssuer`.
   - **Abstract Factory (Лекция 6 §2.2):**
     - Мультигородские семейства объектов: семейство «Алматы» (`OnayCard`, `AlmatyValidator`, `AlmatyFareRule`) и семейство «Астана» (`Transcard`, `AstanaValidator`, `AstanaFareRule`).
   - **Builder с Fluent API (Блок 2 Лаб 6 / Лекция 6 §3):**
     - В Лаб 6: иммутабельная модель `@dataclass(frozen=True) class DailyShiftReport` и строитель `ShiftReportBuilder` с текучим интерфейсом (`return self`):
       - `set_shift_info(self, route_id: str, driver_id: str, shift_date: date) -> "ShiftReportBuilder"`
       - `add_qr_revenue(self, amount: Decimal, count: int) -> "ShiftReportBuilder"`
       - `add_card_revenue(self, amount: Decimal, count: int) -> "ShiftReportBuilder"`
       - `add_cash_revenue(self, amount: Decimal, count: int) -> "ShiftReportBuilder"`
       - `record_incident(self, time_str: str, description: str) -> "ShiftReportBuilder"`
       - `build(self) -> DailyShiftReport` — проверяет обязательность `route_id` и `driver_id` (иначе выбрасывает `IncompleteReportError`), проверяет суммарную выручку `>= Decimal("0.00")`.
     - В Лекции 6 показана компактная учебная версия: `DailyTransitReport` и `TransitReportBuilder` (`set_header`, `add_financials`, `log_anomaly`, `build`), решающая проблему антипаттерна **Telescoping Constructor**.
   - **Антипаттерн Singleton (Блок 3 Лаб 6 / Лекция 6 §4):**
     - Легаси-класс `GlobalConfig` порождает 4 проблемы: `Global Mutable State`, скрытые зависимости, падение параллельных тестов (`pytest -n 4`, Flaky Tests) и нарушение SRP. Заменяется на неизменяемый `AppConfig`, передаваемый через Constructor Injection (или DI-контейнер).

2. **Лекция 7 (`RF__lecture_07.pdf`) и Лабораторная №7 (`RF__lab_07.pdf`) — Структурные паттерны GoF (`Adapter`, `Decorator`, `Facade`, `Proxy`):**
   - **Adapter (Блок 1 Лаб 7 / Лекция 7 §1):**
     - Сторонний банковский клиент `LegacyBankClient` с методом `execute_payment_kzt(self, source_pan: str, dest_account: str, amount_tiyn: int) -> dict` (принимает сумму в тиынах: `1 тенге = 100 тиын`, возвращает словарь с `'auth_code'`; в Лекции 7 также показан `LegacyBankXmlClient.execute_transfer_v2`).
     - Внутренний протокол `PaymentGateway(Protocol)` с методом `charge(self, card_id: str, amount: Decimal) -> str`.
     - Адаптер `BankApiAdapter` (в Лекции 7 — `BankSdkAdapter`), который принимает `(external_client: LegacyBankClient, transit_account: str)`, в `charge(self, card_id: str, amount: Decimal) -> str` конвертирует `Decimal` тенге в `int(amount * 100)` тиынов (например, `Decimal("150.50") -> 15050`), вызывает `execute_payment_kzt` и при ошибке оборачивает её в доменное исключение `PaymentGatewayError`.
   - **Decorator (Блок 2 Лаб 7 / Лекция 7 §2):**
     - Базовый шлюз `CoreGateway` / `CorePaymentGateway` (возвращает `f"TX-{card_id[:4]}-SUCCESS"`).
     - Цепочка декораторов («матрёшка»), реализующих тот же контракт `PaymentGateway`: `TimingDecorator` / `TimingAuditDecorator`, `RetryOnFailureDecorator(wrapped, max_retries=3)`, `StopListCacheDecorator`.
   - **Facade (Блок 3 Лаб 7 / Лекция 7 §3):**
     - `TransitTerminalFacade` / `TransitValidationFacade`: принимает в `__init__` подсистемы (`reader: CardReader` / `blacklist: BlacklistRepository`, `gateway: PaymentGateway`, `tariff: TariffEngine`, `hardware: HardwareFeedback`) и предоставляет единый метод `tap(self) -> TapResponse` (или `tap_card(self, card_id: str, bus_id: str) -> bool`).
   - **Proxy (Лекция 7 §4):**
     - `Virtual Proxy` (ленивая загрузка графа из 10 000 остановок), `Protection Proxy` (проверка прав инспектора), `Remote Proxy` (инкапсуляция gRPC/HTTP). Дана сравнительная таблица 4 паттернов-обёрток (`Adapter` и `Facade` меняют интерфейс; `Decorator` и `Proxy` сохраняют тот же интерфейс).

3. **Лекция 8 (`RF__lecture_08.pdf`) и Лабораторная №8 (`RF__lab_08.pdf`) — Поведенческие паттерны GoF (`Strategy`, `Observer`, `Command`, `State`, `Chain of Responsibility`):**
   - **Chain of Responsibility (Блок 1 Лаб 8 / Лекция 8 §4.2):**
     - Запрос `PaymentRequest` и ответ `ValidationResult(is_approved: bool, reason: str = "", tx_id: str = "")`.
     - Абстрактный узел `ValidationHandler(ABC)` с полем `self._next_handler: ValidationHandler | None = None`, методом `set_next(self, handler: "ValidationHandler") -> "ValidationHandler"` (возвращает `handler` для цепочки `h1.set_next(h2).set_next(h3)`) и `@abstractmethod def handle(self, request: PaymentRequest) -> ValidationResult`.
     - Конкретные обработчики:
       1. `BlacklistCheckHandler` (если `card_id` в стоп-листе → прерывает цепочку Short-circuit с `ValidationResult(is_approved=False, reason="Карта в черном списке")`).
       2. `AntiFraudCooldownHandler` (если повторное прикладывание `< 60` сек → прерывает цепочку).
       3. `BalanceCheckHandler` (если `balance < fare` → прерывает цепочку с ошибкой нехватки средств).
       4. `TransactionExecutionHandler` (финальный узел, списывает баланс и возвращает успешный результат).
   - **Observer (Блок 2 Лаб 8 / Лекция 8 §2):**
     - Событие `TelemetryEvent` / `TransactionEvent`.
     - Издатель `TransitTelemetrySubject` / `ValidatorSubject` с методами `attach(observer)`, `detach(observer)`, `notify(event)`.
     - Наблюдатели: `LocalAuditObserver`, `MetricsCollectorObserver` (счётчики `total_transactions`, `approved_count`, `rejected_count`), `SecurityAlertObserver`.
     - Объединённый движок `TransitValidationPipeline` (Блок 3 Лаб 8): прогоняет `PaymentRequest` через цепочку `ValidationHandler` и публикует `TelemetryEvent` в `TransitTelemetrySubject`.
   - **Strategy, Command, State (Лекция 8 §1, §3, §4.1):**
     - `FraudCheckStrategy` (`LenientFraudStrategy`, `StrictFraudStrategy`), `Command` для офлайн-очереди в тоннеле/степи (`ProcessPaymentCommand` / `SyncTransactionCommand`), `State` для FSM экрана валидатора (`IdleState` → `ReadingState` → `ApprovedState`).

4. **Лекция 9 (`RF__lecture_09.pdf`) и Лабораторная №9 (`RF__lab_09.pdf`) — Чистая Архитектура (`Clean Architecture`), `Code Smells` и рефакторинг:**
   - **4 слоя и The Dependency Rule (Лекция 9 §1–§2 / Лаб 9 Блок 1):**
     - `domain/` (Ядро бизнеса, 0 внешних зависимостей): сущности `Bus`, `Route`, `TransitCard`, `SingleTripTicket`; объекты-значения (`Value Objects`) `Money(amount: Decimal, currency: str = "KZT")`, `PlateNumber(value: str)`, `GeoPoint`; доменные исключения `InsufficientFundsError`, `InvalidRouteError`.
     - `application/` (Сценарии использования — `Use Cases`):
       - `ports/`: абстрактные протоколы `CardRepositoryPort`, `BusRepositoryPort`, `PaymentGatewayPort`, `AuditLedgerPort` / `NotificationPort`.
       - `use_cases/`: `ValidateRideUseCase` (принимает порты в `__init__`, в методе `execute(self, request: ValidateRideRequest) -> ValidateRideResponse` загружает `card` и `bus`, вызывает чистую доменную логику расчёта и списания, сохраняет `card` в репозиторий и возвращает `ValidateRideResponse(success=True, fare=fare)`), а также `IssueTicketUseCase`, `ShiftReportUseCase`.
     - `infrastructure/`: `SqliteCardRepository`, `MemoryLedgerRepository`, `BankSdkAdapter`, `QrPaymentAdapter`, `TerminalBuzzerDriver`.
     - `presentation/`: `simulator.py` (симуляция смены маршрута №32).
   - **Каталог запахов кода Фаулера (Лекция 9 §3):**
     - *Bloaters:* `Long Method` (→ `Extract Method`), `Large Class` (→ `Extract Class`), `Primitive Obsession` (→ `Introduce Value Object`, например `Money` и `PlateNumber`).
     - *OOP Abusers:* `Switch Statements` (→ `Replace Conditional with Polymorphism`), `Refused Bequest` (→ `Replace Inheritance with Delegation`).
     - *Change Preventers:* `Divergent Change` (один класс меняется по разным причинам → декомпозиция по SRP) vs `Shotgun Surgery` (одно изменение требует правок в 15 файлах → `Move Method / Move Field`).
     - *Couplers:* `Feature Envy` (метод постоянно лезет в поля чужого класса → `Move Method`).

---

### G2: Проверка белого списка `ASTValidator` (`app/services/ast_validator.py`) — синтаксические ограничения для `w3_task_1..3`

Инспекция `app/services/ast_validator.py` выявила точные границы безопасности песочницы (`D9`/`F7`):
1. **Разрешённые модули (`ALLOWED_MODULES`, строки 9–24):**
   `{"math", "typing", "abc", "random", "datetime", "decimal", "fractions", "copy", "collections", "itertools", "functools", "string", "enum", "dataclasses"}`.
   - **Следствие 1:** Модули `dataclasses` (`@dataclass(frozen=True)`, `field`), `decimal` (`Decimal`), `abc` (`ABC`, `abstractmethod`), `typing` (`Protocol`, `List`, `Optional`), `datetime` (`date`) **разрешены** и работают из коробки!
   - **Следствие 2:** Модули `time` (использовался в `TimingDecorator` из Лаб 7) и `re` (упоминался для `PlateNumber` в Лаб 9) **отсутствуют в `ALLOWED_MODULES`** и вызовут ошибку `Forbidden module import`. Следовательно, задачи `w3_task_1..3` и `test_code` не должны импортировать `time` или `re`.
2. **Запрещённые dunder-атрибуты и методы (`ALLOWED_MAGIC_METHODS`, строки 70–100, 244–255):**
   - `__init__`, `__str__`, `__repr__`, `__eq__`, `__call__` и арифметические операторы разрешены.
   - Конструктор синглтона `__new__` (Лаб 6 Блок 3) и рефлексия `observer.__class__.__name__` (Лекция 8 §2) **запрещены** (`Forbidden system identifier / attribute access`).
   - Встроенные функции `getattr`, `setattr`, `open`, `eval`, `exec` запрещены (`DISALLOWED_CALLS`).

Таким образом, гипотеза **H1 полностью подтверждается**: канонические классы `ShiftReportBuilder` / `DailyShiftReport` (Лаб 6), `BankApiAdapter` / `LegacyBankClient` / `TransitTerminalFacade` (Лаб 7), `ValidationHandler` / `TransitTelemetrySubject` (Лаб 8) и `ValidateRideUseCase` / `Money` (Лаб 9) реализуются на 100% внутри существующего `ALLOWED_MODULES` без малейшего ослабления `ASTValidator`.

---

### G3: Аудит шаблонов Jinja2, `uml_viewer.html`, `app.js` и `ScoringService` — важные находки по гипотезе `H2`

1. **Частичное опровержение `H2` в шаблонах `tab_theory.html` и `tab_practice.html`:**
   - В `HL §10 (H2)` предполагалось, что шаблоны `tab_theory.html` и `tab_practice.html` вообще не требуют изменений.
   - Однако поиск `Select-String` по `app/templates/components/*.html` выявил 3 жёстких ветвления `{% if active_week|default(1) == 2 %} ... {% else %}`:
     - `app/templates/components/tab_theory.html` (строки 6–16): ветка `{% else %}` выводит `Теория: Основы ООП и Инкапсуляция (с нуля)` и упоминает `SmartCard`.
     - `app/templates/components/tab_practice.html` (строки 19–23): ветка `{% else %}` выводит имя файла `example_avtobys.py — Готовый образец классов Passenger и Validator`.
     - `app/templates/components/tab_practice.html` (строки 47–51): ветка `{% else %}` выводит `Попробуйте собрать класс SmartCard или разберите готовое решение`.
   - **Вывод:** Для корректного отображения Недели 3 необходимо добавить ветку `{% elif active_week|default(1) == 3 %}` в эти 3 места в `tab_theory.html` и `tab_practice.html`! Остальные шаблоны (`tab_home.html`, `tab_quiz.html`, `tab_results.html`) уже полностью универсальны (используют `{{ active_week|default(1) }}` и `{{ overview.* }}`).
2. **Незакоммиченные изменения в рабочем дереве (`git status`):**
   - В рабочем дереве уже есть полезная незакоммиченная правка в `app/templates/components/uml_viewer.html` и `tests/test_uml_viewer.py` (переход от одной кнопки `data-diagram-tab="week"` к отдельным кнопкам `week1` и `week2`), которую нужно сохранить и дополнить кнопкой `data-diagram-tab="week3"` и панелью `#uml-diagram-week3` (`svg-week3`).
   - В `app/static/js/app.js` (строки 691, 732–749, 903–910) необходимо добавить поддержку `ACTIVE_WEEK === "3"` и `tabKey === "week3"` (включая заголовок полноэкранной модалки `openUmlFullscreen()`).
3. **`ScoringService` (`app/services/scoring.py` строки 30–33):**
   - Подтверждено: `WEEK_TASK_IDS` содержит только ключи `1` и `2`. Добавление `3: ("w3_task_1", "w3_task_2", "w3_task_3")` полностью включает изоляцию прогресса Недели 3 (`week_3`, `week_3_theory`, `week_3_quiz`, `week_3_w3_task_1..3`) для всех 4 профилей студентов.

---

### G4: Внешняя верификация концептуальных ловушек GoF и Clean Architecture (External Research)

Внешний поиск и сопоставление с контрольными вопросами из `RF__lecture_06..09.pdf` и `RF__lab_06..09.pdf` выделили главные концептуальные ловушки для 10 вопросов квиза (`w3_q1..w3_q10`):
1. **Factory Method vs Simple Static Factory:** Фабричный метод опирается на полиморфизм и переопределение в подклассах (`TicketIssuer` → `QrTicketIssuer`), соблюдая `OCP`, тогда как статическая фабрика с `if/elif` требует модификации при добавлении нового типа билета.
2. **Builder vs Telescoping Constructor:** Строитель (`ShiftReportBuilder`) оправдан для пошаговой сборки сложных объектов с отложенной проверкой инвариантов в `build()`, но избыточен для простых DTO с 2–3 фиксированными полями.
3. **Singleton vs DI Lifecycle:** Проблема `Singleton` не в том, что объект один в памяти, а в глобальном разделяемом состоянии (`Global Mutable State`) и скрытых зависимостях, ломающих изоляцию параллельных тестов (`pytest -n 4`).
4. **Adapter vs Decorator vs Facade vs Proxy («Паттерны-обёртки»):**
   - `Adapter` **меняет** несовместимый интерфейс стороннего класса (`LegacyBankClient` в тиынах → `PaymentGateway` в тенге).
   - `Decorator` **сохраняет тот же** интерфейс (`PaymentGateway`), позволяя оборачивать объект рекурсивно («матрёшкой») для динамического добавления обязанностей (тайминг, retry, кэш).
   - `Facade` вводит **новый упрощённый** интерфейс (`TransitTerminalFacade.tap()`) поверх группы сложных подсистем.
   - `Proxy` **сохраняет тот же** интерфейс, но контролирует доступ или управляет жизненным циклом/ленивой загрузкой объекта.
5. **Strategy vs State:** При схожих UML-диаграммах `Strategy` выбирается и подменяется извне клиентом как взаимозаменяемый алгоритм расчёта/проверки, тогда как в `State` переходы между состояниями (`IdleState` → `ReadingState` → `ApprovedState`) определяются жизненным циклом самого автомата.
6. **Observer Isolation & Chain of Responsibility Short-circuiting:**
   - В `Observer` издатель (`Subject`) не должен зависеть от конкретных классов подписчиков и обязан изолировать их сбои, чтобы падение одного логгера не прервало оповещение остальных.
   - В `Chain of Responsibility` для финансовой валидации критично прерывание на первой ошибке (`Short-circuiting`: если карта в стоп-листе в `BlacklistCheckHandler`, узлы `BalanceCheckHandler` и списания не вызываются вовсе).
7. **Clean Architecture (`The Dependency Rule`) и `Code Smells` Фаулера:**
   - Стрелки зависимостей исходного кода (`import`) направлены строго **внутрь** (`Infrastructure` → `Interface Adapters` → `Use Cases` → `Domain Entities`); внутренний слой `Domain` ничего не знает о БД SQLite, FastAPI или внешних SDK, а пересечение границ наружу решается через инверсию зависимостей (порты `CardRepositoryPort`, `PaymentGatewayPort`).
   - Ловушка `Divergent Change` vs `Shotgun Surgery`: `Divergent Change` — один класс страдает от множества разнородных изменений; `Shotgun Surgery` — одно бизнес-изменение заставляет править множество разных классов.

---

## Checkpoint

| Found | Remaining |
|-------|-----------|
| Извлечены все канонические классы, методы и сценарии из `RF__lecture_06..09.pdf` и `RF__lab_06..09.pdf` (`TicketIssuer`, `ShiftReportBuilder`, `DailyShiftReport`, `BankApiAdapter`, `LegacyBankClient`, `TransitTerminalFacade`, `ValidationHandler`, `TransitTelemetrySubject`, `ValidateRideUseCase`, `Money`). | На стадии **Extract** (`3_extract.md`) сформировать конкретные конфигурации 4 шагов теории, `WALKTHROUGH_EXAMPLE`, 3 задач тренажёра `w3_task_1..3`, SVG-диаграммы `svg-week3` и 10 вопросов квиза `w3_q1..w3_q10`. |
| Подтверждена гипотеза **H1**: задачи Лаб 6–9 полностью укладываются в `ASTValidator.ALLOWED_MODULES` (`abc`, `dataclasses`, `decimal`, `typing`, `datetime`, `enum`), если исключить `time`, `re`, `__new__` и `__class__.__name__`. | На стадии **Challenge** (`4_challenge.md`) проверить длину и исполняемость эталонных решений `w3_task_1..3` и баланс вариантов квиза. |
| Уточнена (частично опровергнута) гипотеза **H2**: помимо `header.html`, `uml_viewer.html` и `app.js`, в `tab_theory.html` (1 место) и `tab_practice.html` (2 места) есть жёсткие `{% if active_week|default(1) == 2 %} ... {% else %}`, куда нужно добавить ветку `== 3`. | Зафиксировать это уточнение как `Refinement` к свободному разделу `HL §2 / §10` и `Single-Phase Deliverables` на этапе синтеза `RES.md`. |

**Sufficiency:**
- [x] External source used?
- [x] Briefing gap closed?
- [x] Dimensions identified? _(4 independent dimensions D1–D4 with ≥3 alternatives each)_

### Knowledge Handover (Stage 2 Gather Checkpoint)
- **Producer / Unit:** Researcher (`antigravity:thread:local:b44e12c6-d392-4cd9-a90a-763aa4936c08`), parent Coordinator (`antigravity:thread:local:5e1d1422-f45d-4f89-9d10-9eff76d814cb`).
- **Source / Version:** `HL-OOP_20261026-021211_W3GOF.md @ e31342f75d719eb67ab978fc7d1c3bd5265701a4`, `C:\Users\kz444\OneDrive\Desktop\OOP\01_Лекции\RF__lecture_06..09.pdf`, `C:\Users\kz444\OneDrive\Desktop\OOP\02_Лабораторные\RF__lab_06..09.pdf`, `app/services/{ast_validator,scoring}.py`, `app/modules/registry.py`, `app/routers/week2.py`, `app/templates/components/{header,uml_viewer,tab_theory,tab_practice}.html`, `app/static/js/app.js`.
- **Inspected Scope:** 8 PDF-файлов курса (Лекции 6–9 и Лаб 6–9), 9 файлов кодовой базы `app/`, 1 внешний веб-поиск по GoF + Clean Architecture.
- **Material Outcome:** Извлечены канонические контракты классов для Недели 3; подтверждена `H1` (выявлены запрещённые в `ASTValidator` конструкции `time`, `re`, `__new__`, `__class__.__name__`); уточнена `H2` (обнаружены 3 жёстких `if active_week == 2 ... else` в `tab_theory.html` и `tab_practice.html`).
- **Remaining Uncertainty:** Выбор оптимальной комбинации альтернатив по осям `D1–D4` на стадии `3_extract.md` и их стресс-проверка на стадии `4_challenge.md`.
- **Continuation:** Ожидание решения Координатора (`5e1d1422-f45d-4f89-9d10-9eff76d814cb`) для перехода к стадии **Extract** (`3_extract.md`).

Stage complete: YES
→ User decision: Подтверждено закрытие стадии Gather и переход к Extract (`3_extract.md`). Q1: Включить `tab_theory.html` и `tab_practice.html` (добавление веток `{% elif active_week|default(1) == 3 %}`) в конфигурацию D3 (refinement свободных секций `HL §2 / §4 / §10 H2`). Q2: В Extract сопоставить связки `Alt B` и `Alt C` для `WALKTHROUGH_EXAMPLE` + `w3_task_1..3` с 100% покрытием Лаб 6–9 и порогом 25–45 строк для начинающих.
