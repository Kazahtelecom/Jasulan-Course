"""Lecture content for Week 1: OOP Fundamentals, Encapsulation, and Invariant Defense."""

LECTURE_DATA = {
    "title": "Неделя 1: Основы ООП, инкапсуляция и защита инвариантов",
    "subtitle": "Предметная область: Транспортная система Avtobys (Алматы)",
    "estimated_time": "60 минут",
    "summary": (
        "Изучение перехода от процедурного хаоса к объектно-ориентированной архитектуре. "
        "Разбор понятий Identity, State, Behavior, сравнительный анализ Anemic vs Rich "
        "Domain Model, сокрытие состояния через приватные атрибуты и синтаксис @property "
        "в Python 3.12, а также проектирование инвариантов и типизированных исключений "
        "на реальном домене городского транспорта."
    ),
    "sections": [
        {
            "id": "chaos_to_structure",
            "title": "1. От процедурного хаоса к объектам: Проблема словарей",
            "content": """
В процедурном подходе данные и функции разделены.
Представьте типичную систему оплаты проезда, написанную на словарях:

```python
# Процедурный стиль: данные беззащитны
passenger_card = {
    "card_id": "KZ-7701",
    "balance": 500,
    "is_blocked": False
}

def pay_fare(card, fare):
    card["balance"] -= fare
```

Что произойдет, если в коде возникнет ошибка и баланс уйдет в минус?
Или если сторонний модуль напрямую изменит поле:
`passenger_card["balance"] = -99999`?
Словарь не может защитить свои правила. Любой участок программы в любой момент
может сломать целостность данных. В реальной системе Avtobys это приводит к сбоям
турникетов, финансовым потерям и невозможности отследить источник ошибки.

**Объектно-ориентированное программирование (ООП)** решает эту проблему фундаментально:
данные объединяются с поведением, а прямой доступ к внутренностям объекта закрывается.
""",
        },
        {
            "id": "identity_state_behavior",
            "title": "2. Три кита объекта: Identity, State, Behavior",
            "content": """
Каждый объект в ООП характеризуется тремя фундаментальными аспектами:

1. **Identity (Идентичность):** Уникальность экземпляра, отличающая его от всех остальных,
даже если их свойства совпадают. В Python идентичность проверяется оператором `is`
(по адресу в памяти `id(obj)`), а в доменной модели — уникальным идентификатором
(например, `card_id` или `ticket_code`).
2. **State (Состояние):** Набор внутренних данных объекта в текущий момент времени
(баланс карты, статус блокировки, дата выпуска). Состояние определяет, как объект
отреагирует на внешние воздействия.
3. **Behavior (Поведение):** Набор методов, определяющих, как объект может изменять
свое состояние и взаимодействовать с другими объектами (`top_up()`, `pay()`, `validate()`).
""",
        },
        {
            "id": "anemic_vs_rich",
            "title": "3. Anemic Domain Model vs Rich Domain Model",
            "content": """
Одной из главных ошибок начинающих разработчиков является создание
**анемичной модели (Anemic Domain Model)**:

```python
# АНЕМИЧНАЯ МОДЕЛЬ (Антипаттерн): Класс — это просто структура данных (DTO)
class AnemicCard:
    def __init__(self, balance: float):
        self.balance = balance  # Публичное поле!

# Логика размазана по внешним сервисам
def process_bus_ride(card: AnemicCard, fare: float):
    if card.balance >= fare:
        card.balance -= fare
```

Почему это плохо? Логика проверки баланса дублируется в каждом контроллере,
а сам объект не контролирует свои правила.

**Богатая доменная модель (Rich Domain Model)** помещает всю бизнес-логику внутрь сущности:

```python
# БОГАТАЯ МОДЕЛЬ: Сущность сама управляет своими правилами и состоянием
class RichCard:
    def __init__(self, card_id: str, initial_balance: Decimal):
        if initial_balance < Decimal("0"):
            raise ValueError("Начальный баланс не может быть отрицательным")
        self._card_id = card_id
        self._balance = initial_balance

    def pay(self, fare: Decimal) -> Decimal:
        if self._balance < fare:
            raise InsufficientFundsError("Недостаточно средств")
        self._balance -= fare
        return fare
```
""",
        },
        {
            "id": "invariants_and_properties",
            "title": "4. Защита инвариантов и синтаксис @property в Python 3.12",
            "content": """
**Инвариант** — это условие согласованности бизнес-логики, которое обязано оставаться
истинным на протяжении всей жизни объекта:
- Баланс карты `TransitCard` никогда не может быть отрицательным: `balance >= 0`.
- Одноразовый билет `SingleTripTicket` может быть активирован ровно один раз:
  `validate()` переводит `is_validated` в `True`, а повторный вызов вызывает исключение.
- Билет не может быть валидирован по истечении срока годности (60 минут).

В Python для сокрытия данных используется соглашение с ведущим подчеркиванием
(`_balance`, `_is_validated`) и декоратор `@property`:

```python
class SingleTripTicket:
    def __init__(self, valid_minutes: int = 60):
        self._is_validated = False
        self._valid_minutes = valid_minutes

    @property
    def is_validated(self) -> bool:
        \"\"\"Свойство только для чтения (getter без setter).\"\"\"
        return self._is_validated

    def validate(self, bus) -> bool:
        if self._is_validated:
            raise TicketAlreadyUsedError("Билет уже был использован ранее")
        self._is_validated = True
        return True
```

Если клиентский код попытается выполнить `ticket.is_validated = True`,
интерпретатор Python возбудит `AttributeError`. Это гарантирует абсолютную защиту
инварианта от случайной или намеренной модификации извне.
""",
        },
        {
            "id": "domain_exceptions",
            "title": "5. Типизированная иерархия доменных исключений",
            "content": """
Никогда не возвращайте `False` или `None` при нарушении бизнес-правил — вызывающий код
может забыть проверить возвращаемое значение. Создавайте собственную иерархию исключений:

```python
class DomainError(Exception):
    \"\"\"Базовый класс всех доменных ошибок Avtobys.\"\"\"
    pass

class InsufficientFundsError(DomainError):
    \"\"\"Недостаточно средств для списания тарифа.\"\"\"
    pass

class CardBlockedError(DomainError):
    \"\"\"Операция отклонена: карта заблокирована.\"\"\"
    pass

class InvalidAmountError(DomainError):
    \"\"\"Некорректная сумма операции.\"\"\"
    pass

class TicketAlreadyUsedError(DomainError):
    \"\"\"Попытка повторной валидации билета.\"\"\"
    pass

class TicketExpiredError(DomainError):
    \"\"\"Срок действия билета (60 мин) истек.\"\"\"
    pass
```
""",
        },
    ],
    "mermaid_diagrams": {
        "class_diagram": """
classDiagram
    class DomainError {
        <<Exception>>
    }
    class InsufficientFundsError {
        <<DomainError>>
    }
    class CardBlockedError {
        <<DomainError>>
    }
    class InvalidAmountError {
        <<DomainError>>
    }
    class TicketAlreadyUsedError {
        <<DomainError>>
    }
    class TicketExpiredError {
        <<DomainError>>
    }

    DomainError <|-- InsufficientFundsError
    DomainError <|-- CardBlockedError
    DomainError <|-- InvalidAmountError
    DomainError <|-- TicketAlreadyUsedError
    DomainError <|-- TicketExpiredError

    class TransitCard {
        -str _card_id
        -Decimal _balance
        -Decimal _discount_rate
        -bool _is_blocked
        +balance Decimal
        +is_blocked bool
        +top_up(amount: Decimal) void
        +pay(fare: Decimal) Decimal
        +block() void
        +unblock() void
    }

    class SingleTripTicket {
        +str ticket_code
        +Decimal price
        +datetime issued_at
        +timedelta valid_duration
        -bool _is_validated
        +is_validated bool
        +validate(bus: Bus) bool
    }

    class Bus {
        +str route_number
        +list validations
        +process_payment(payment_method) bool
    }

    Bus ..> TransitCard : charges fare
    Bus ..> SingleTripTicket : validates
""",
        "sequence_diagram": """
sequenceDiagram
    autonumber
    actor Passenger as Пассажир
    participant Bus as Автобус (Маршрут 32)
    participant Ticket as Одноразовый билет
    participant Card as Транспортная карта

    Note over Passenger,Card: Сценарий А: Оплата картой TransitCard
    Passenger->>Bus: Приложить карту к валидатору
    Bus->>Card: pay(fare = 100 ₸)
    alt Баланс достаточен и карта активна
        Card-->>Bus: Списано 100 ₸ (баланс уменьшен)
        Bus-->>Passenger: Зеленый сигнал: Проезд оплачен
    else Карта заблокирована
        Card-->>Bus: CardBlockedError
        Bus-->>Passenger: Красный сигнал: Карта заблокирована!
    else Баланс < 100 ₸
        Card-->>Bus: InsufficientFundsError
        Bus-->>Passenger: Красный сигнал: Пополните баланс!
    end

    Note over Passenger,Ticket: Сценарий Б: Валидация SingleTripTicket
    Passenger->>Bus: Сканировать QR-билет
    Bus->>Ticket: validate(bus)
    alt Первый проход и время <= 60 мин
        Ticket-->>Bus: Успешно (is_validated = True)
        Bus-->>Passenger: Зеленый сигнал: Билет принят
    else Билет уже использован
        Ticket-->>Bus: TicketAlreadyUsedError
        Bus-->>Passenger: Красный сигнал: Повторный проход запрещен!
    else Прошло > 60 мин
        Ticket-->>Bus: TicketExpiredError
        Bus-->>Passenger: Красный сигнал: Срок действия билета истек!
    end
""",
    },
}
