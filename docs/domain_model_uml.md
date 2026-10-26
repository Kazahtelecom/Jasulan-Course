# UML-модель предметной области Avtobys, модульная структура и схема базы данных

## 1. Контекст предметной области

В качестве сквозной прикладной темы курса ООП выбрана транспортная система **Avtobys** (электронное билетирование, валидаторы в автобусах, учет баланса пассажиров и маршрутов). Эта предметная область интуитивно понятна студентам и идеально иллюстрирует фундаментальные принципы ООП: инкапсуляцию, полиморфизм валидаторов, наследование тарифов, композицию сущностей и принципы SOLID (разделение интерфейсов и внедрение зависимостей).

---

## 2. Диаграмма модульной архитектуры платформы (WeekModule & Registry)

Модульная архитектура платформы обеспечивает расширяемость и устраняет дублирование кода между учебными неделями:

```mermaid
classDiagram
    class WeekModule {
        +int week_number
        +str title
        +dict overview
        +list theory_sections
        +dict walkthrough
        +list practice_tasks
        +list quiz_questions
        +Callable evaluate_quiz_fn
        +get_practice_task(task_id: str) dict
        +evaluate_quiz(answers: dict) dict
        +build_context(student, progress, request) dict
    }

    class WeekRegistry {
        -dict _modules
        +register(module: WeekModule) None
        +get(week_number: int) WeekModule
        +get_all() list
    }

    class ScoringService {
        +list STUDENTS
        +get_or_create_student(db, username) Student
        +record_task_submission(...) dict
        +record_theory_completed(...) dict
        +record_quiz_submission(...) dict
        +get_progress_summary(...) dict
    }

    class RunnerService {
        +run_code(code, test_code, timeout) RunResult
    }

    class ASTValidator {
        +validate(code) tuple
    }

    WeekRegistry o-- WeekModule : регистрирует модули недель
    WeekModule ..> ScoringService : привязка прогресса
    RunnerService ..> ASTValidator : предварительный аудит безопасности
```

---

## 3. Диаграмма классов предметной области (UML Class Diagram)

Взаимодействие пассажира (`Passenger`), транспортной карты (`SmartCard`), сервисов тарифа (`FareService`) и бортового валидатора (`TerminalValidator`):

```mermaid
classDiagram
    class SmartCard {
        +str owner
        +int balance
        +info() str
    }

    class Passenger {
        +int id
        +str full_name
        +SmartCard card
        +top_up(amount: int) None
    }

    class IFareService {
        <<interface>>
        +get_fare() int
    }

    class StandardFareService {
        +get_fare() int
    }

    class StudentFareService {
        +get_fare() int
    }

    class IPaymentMethod {
        <<interface>>
        +pay(amount: int) str
    }

    class CardPayment {
        +pay(amount: int) str
    }

    class BluetoothPayment {
        +pay(amount: int) str
    }

    class TerminalValidator {
        -IFareService fare_service
        -IPaymentMethod payment_method
        +__init__(fare_service, payment_method)
        +process_passenger() str
    }

    IFareService <|.. StandardFareService : implements
    IFareService <|.. StudentFareService : implements
    IPaymentMethod <|.. CardPayment : implements
    IPaymentMethod <|.. BluetoothPayment : implements
    TerminalValidator o-- IFareService : DI
    TerminalValidator o-- IPaymentMethod : DI
    Passenger *-- SmartCard : composition
```

---

## 3.1. Паттерны GoF и Чистая архитектура Недели 3 (Week 3 UML Class Diagram)

В Неделе 3 рассматриваются порождающие, структурные и поведенческие паттерны GoF, а также инверсия зависимостей Clean Architecture:

```mermaid
classDiagram
    %% Порождающий паттерн: Builder
    class DailyShiftReport {
        +str date
        +str bus_id
        +int passenger_count
        +Decimal total_revenue
        +list errors
    }

    class ShiftReportBuilder {
        -str _date
        -str _bus_id
        -int _passenger_count
        -Decimal _total_revenue
        -list _errors
        +set_date(date: str) ShiftReportBuilder
        +set_bus(bus_id: str) ShiftReportBuilder
        +set_metrics(passengers: int, revenue: Decimal) ShiftReportBuilder
        +add_error(error_msg: str) ShiftReportBuilder
        +build() DailyShiftReport
    }

    ShiftReportBuilder ..> DailyShiftReport : creates

    %% Структурный паттерн: Adapter
    class PaymentRequest {
        +str card_id
        +Decimal amount
    }

    class LegacyBankClient {
        +charge_tiyn(card_token: str, tiyn: int) dict
    }

    class BankApiAdapter {
        -LegacyBankClient _legacy_client
        +__init__(legacy_client: LegacyBankClient)
        +process_payment(request: PaymentRequest) dict
    }

    BankApiAdapter o-- LegacyBankClient : adapts
    BankApiAdapter ..> PaymentRequest : accepts

    %% Поведенческий паттерн: Chain of Responsibility
    class ValidationResult {
        +bool is_valid
        +str reason
    }

    class ValidationHandler {
        <<abstract>>
        -ValidationHandler _next_handler
        +set_next(handler: ValidationHandler) ValidationHandler
        +handle(card: TransitCard, amount: Money) ValidationResult
    }

    class FormatValidationHandler {
        +handle(card: TransitCard, amount: Money) ValidationResult
    }

    class CardActiveHandler {
        +handle(card: TransitCard, amount: Money) ValidationResult
    }

    class BalanceHandler {
        +handle(card: TransitCard, amount: Money) ValidationResult
    }

    ValidationHandler <|-- FormatValidationHandler : inherits
    ValidationHandler <|-- CardActiveHandler : inherits
    ValidationHandler <|-- BalanceHandler : inherits
    ValidationHandler --> ValidationHandler : next

    %% Поведенческий паттерн: Observer
    class ITelemetryObserver {
        <<interface>>
        +update(event: str, data: dict) None
    }

    class AuditLogObserver {
        +update(event: str, data: dict) None
    }

    class DisplayObserver {
        +update(event: str, data: dict) None
    }

    class TransitTelemetrySubject {
        -list _observers
        +attach(observer: ITelemetryObserver) None
        +detach(observer: ITelemetryObserver) None
        +notify(event: str, data: dict) None
    }

    ITelemetryObserver <|.. AuditLogObserver : implements
    ITelemetryObserver <|.. DisplayObserver : implements
    TransitTelemetrySubject o-- ITelemetryObserver : notifies

    %% Clean Architecture: Use Case & Entities
    class Money {
        +Decimal amount
        +str currency
    }

    class TransitCard {
        +str card_id
        +Money balance
        +bool is_active
    }

    class CardRepository {
        <<protocol>>
        +get_by_id(card_id: str) TransitCard
        +save(card: TransitCard) None
    }

    class NotificationGateway {
        <<protocol>>
        +notify_passenger(card_id: str, message: str) None
    }

    class ValidateRideUseCase {
        -CardRepository _card_repo
        -NotificationGateway _notifier
        +__init__(card_repo, notifier)
        +execute(card_id: str, fare: Money) dict
    }

    ValidateRideUseCase o-- CardRepository : dependency inversion
    ValidateRideUseCase o-- NotificationGateway : dependency inversion
    ValidateRideUseCase ..> TransitCard : uses
    TransitCard *-- Money : value object
```

---

## 4. Схема базы данных (Entity-Relationship Diagram)

Схема хранения данных мини-LMS в SQLite (`data/web_oop.db`):

```mermaid
erDiagram
    STUDENT ||--o{ TOPIC_PROGRESS : "has"
    STUDENT ||--o{ SUBMISSION : "submits"

    STUDENT {
        int id PK "Автоинкрементный идентификатор"
        string username UK "Уникальный логин студента (zhasulan, roman, arseniy, saubakirov)"
        string full_name "Полное имя (ФИО студента)"
        datetime created_at "Дата и время регистрации"
    }

    TOPIC_PROGRESS {
        int id PK "Идентификатор записи прогресса"
        int student_id FK "Ссылка на студента"
        string topic_id "Идентификатор топика (week_1, week_1_quiz, week_1_theory, week_1_task_1)"
        boolean is_completed "Флаг завершения темы"
        float score "Набранный балл (0.0 .. 20.0)"
        datetime updated_at "Дата последнего обновления"
    }

    SUBMISSION {
        int id PK "Идентификатор попытки"
        int student_id FK "Ссылка на студента"
        string task_id "Идентификатор задания (напр. week_1_task_1)"
        text code "Исходный код решения студента"
        string status "Статус (PASSED, FAILED, TIMEOUT, SECURITY_VIOLATION)"
        text test_output "Лог вывода pytest или AST-ошибки"
        datetime created_at "Время отправки решения"
    }
```

### Отношения и ограничения:
- `STUDENT -> TOPIC_PROGRESS`: отношение «один-ко-многим». Обеспечивает полную изоляцию баллов между 4 участниками группы.
- `STUDENT -> SUBMISSION`: отношение «один-ко-многим». Фиксирует историю запусков кода в тренажере.
