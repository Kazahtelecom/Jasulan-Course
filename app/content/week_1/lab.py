"""Lab task for Week 1: SingleTripTicket and Bus Invariant Defense."""

STARTER_CODE = '''from datetime import datetime, timedelta
from decimal import Decimal
import uuid


# 1. Иерархия исключений
class DomainError(Exception):
    """Базовое исключение домена."""
    pass

class TicketAlreadyUsedError(DomainError):
    """Билет уже был использован ранее."""
    pass

class TicketExpiredError(DomainError):
    """Срок действия билета истек."""
    pass

class InsufficientFundsError(DomainError):
    """Недостаточно средств на карте."""
    pass

class CardBlockedError(DomainError):
    """Карта заблокирована."""
    pass

class InvalidAmountError(DomainError):
    """Некорректная сумма."""
    pass


# 2. Сущность TransitCard (для взаимодействия с Bus)
class TransitCard:
    def __init__(
        self,
        card_id: str,
        initial_balance: Decimal = Decimal("0"),
        discount_rate: Decimal = Decimal("0.0"),
    ):
        if initial_balance < Decimal("0"):
            raise ValueError("Начальный баланс не может быть отрицательным")
        if not (Decimal("0.0") <= discount_rate <= Decimal("1.0")):
            raise ValueError("Скидка должна быть в диапазоне от 0.0 до 1.0")
        self._card_id = card_id
        self._balance = initial_balance
        self._discount_rate = discount_rate
        self._is_blocked = False

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    def top_up(self, amount: Decimal) -> None:
        if self._is_blocked:
            raise CardBlockedError("Нельзя пополнить заблокированную карту")
        if amount < Decimal("100"):
            raise InvalidAmountError("Минимальная сумма пополнения — 100 тенге")
        self._balance += amount

    def pay(self, fare: Decimal) -> Decimal:
        if self._is_blocked:
            raise CardBlockedError("Карта заблокирована")
        if fare <= Decimal("0"):
            raise InvalidAmountError("Стоимость проезда должна быть положительной")
        effective_fare = fare * (Decimal("1.0") - self._discount_rate)
        if self._balance < effective_fare:
            raise InsufficientFundsError("Недостаточно средств на карте")
        self._balance -= effective_fare
        return effective_fare


# 3. Сущность SingleTripTicket
class SingleTripTicket:
    """Одноразовый билет с защитой инвариантов однократности и срока действия."""

    def __init__(
        self,
        price: Decimal = Decimal("120"),
        valid_minutes: int = 60,
        issued_at: datetime | None = None,
    ):
        # TODO: Инициализируйте атрибуты:
        # - ticket_code: уникальная строка (uuid)
        # - price: стоимость билета
        # - issued_at: переданное время или datetime.now()
        # - valid_duration: timedelta(minutes=valid_minutes)
        # - _is_validated: булево приватное поле (начальное значение False)
        pass

    @property
    def is_validated(self) -> bool:
        """Свойство только для чтения (без сеттера!)."""
        # TODO: Верните приватный флаг
        pass

    def validate(self, bus) -> bool:
        """Валидация билета в автобусе.

        Инварианты:
        - Если билет уже валидирован (_is_validated == True) -> TicketAlreadyUsedError.
        - Если datetime.now() - self.issued_at > self.valid_duration -> TicketExpiredError.
        - Успешный вызов переводит _is_validated в True и возвращает True.
        """
        # TODO: Реализуйте проверку инвариантов и валидацию
        pass


# 4. Сущность Bus (автобус с валидатором)
class Bus:
    """Автобус городского маршрута, принимающий оплату картой и билетом."""

    def __init__(self, route_number: str):
        # TODO: Инициализируйте:
        # - route_number: строка номера маршрута
        # - validations: список успешных валидаций (изначально пустой [])
        pass

    def process_payment(self, payment_method) -> bool:
        """Обработка оплаты или валидации.

        - Если передан объект с методом pay (TransitCard):
          вызывает payment_method.pay(Decimal("100")),
          добавляет запись в validations и возвращает True.
        - Если передан объект с методом validate (SingleTripTicket):
          вызывает payment_method.validate(self),
          добавляет запись в validations и возвращает True.
        - Иначе возбуждает TypeError.
        """
        # TODO: Реализуйте полиморфную обработку оплаты
        pass
'''

REFERENCE_SOLUTION = '''from datetime import datetime, timedelta
from decimal import Decimal
import uuid


class DomainError(Exception):
    pass

class TicketAlreadyUsedError(DomainError):
    pass

class TicketExpiredError(DomainError):
    pass

class InsufficientFundsError(DomainError):
    pass

class CardBlockedError(DomainError):
    pass

class InvalidAmountError(DomainError):
    pass


class TransitCard:
    def __init__(
        self,
        card_id: str,
        initial_balance: Decimal = Decimal("0"),
        discount_rate: Decimal = Decimal("0.0"),
    ):
        if initial_balance < Decimal("0"):
            raise ValueError("Начальный баланс не может быть отрицательным")
        if not (Decimal("0.0") <= discount_rate <= Decimal("1.0")):
            raise ValueError("Скидка должна быть в диапазоне от 0.0 до 1.0")
        self._card_id = card_id
        self._balance = initial_balance
        self._discount_rate = discount_rate
        self._is_blocked = False

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    def top_up(self, amount: Decimal) -> None:
        if self._is_blocked:
            raise CardBlockedError("Нельзя пополнить заблокированную карту")
        if amount < Decimal("100"):
            raise InvalidAmountError("Минимальная сумма пополнения — 100 тенге")
        self._balance += amount

    def pay(self, fare: Decimal) -> Decimal:
        if self._is_blocked:
            raise CardBlockedError("Карта заблокирована")
        if fare <= Decimal("0"):
            raise InvalidAmountError("Стоимость проезда должна быть положительной")
        effective_fare = fare * (Decimal("1.0") - self._discount_rate)
        if self._balance < effective_fare:
            raise InsufficientFundsError("Недостаточно средств на карте")
        self._balance -= effective_fare
        return effective_fare


class SingleTripTicket:
    def __init__(
        self,
        price: Decimal = Decimal("120"),
        valid_minutes: int = 60,
        issued_at: datetime | None = None,
    ):
        self.ticket_code = str(uuid.uuid4())
        self.price = price
        self.issued_at = issued_at if issued_at is not None else datetime.now()
        self.valid_duration = timedelta(minutes=valid_minutes)
        self._is_validated = False

    @property
    def is_validated(self) -> bool:
        return self._is_validated

    def validate(self, bus) -> bool:
        if self._is_validated:
            raise TicketAlreadyUsedError("Билет уже был использован")
        if datetime.now() - self.issued_at > self.valid_duration:
            raise TicketExpiredError("Срок действия билета истек")
        self._is_validated = True
        return True


class Bus:
    def __init__(self, route_number: str):
        self.route_number = route_number
        self.validations: list[dict] = []

    def process_payment(self, payment_method) -> bool:
        if hasattr(payment_method, "pay"):
            payment_method.pay(Decimal("100"))
            self.validations.append({"type": "card", "time": datetime.now()})
            return True
        elif hasattr(payment_method, "validate"):
            payment_method.validate(self)
            self.validations.append({"type": "ticket", "time": datetime.now()})
            return True
        else:
            raise TypeError("Неподдерживаемый способ оплаты")
'''

SECRET_TESTS = '''from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from solution import (
    Bus,
    DomainError,
    InsufficientFundsError,
    SingleTripTicket,
    TicketAlreadyUsedError,
    TicketExpiredError,
    TransitCard,
)


def test_ticket_initialization():
    """Тест 1: Инициализация билета с ценой, кодом и временем выпуска."""
    ticket = SingleTripTicket(price=Decimal("120"), valid_minutes=60)
    assert ticket.ticket_code is not None
    assert len(ticket.ticket_code) > 0
    assert ticket.price == Decimal("120")
    assert isinstance(ticket.issued_at, datetime)
    assert ticket.valid_duration == timedelta(minutes=60)


def test_ticket_initial_not_validated():
    """Тест 2: Новый билет изначально не валидирован."""
    ticket = SingleTripTicket()
    assert ticket.is_validated is False


def test_ticket_validate_success():
    """Тест 3: Первый вызов validate(bus) переводит is_validated в True."""
    bus = Bus("32")
    ticket = SingleTripTicket()
    result = ticket.validate(bus)
    assert result is True
    assert ticket.is_validated is True


def test_ticket_already_used_error():
    """Тест 4: Повторная валидация возбуждает TicketAlreadyUsedError."""
    bus = Bus("32")
    ticket = SingleTripTicket()
    ticket.validate(bus)

    with pytest.raises(TicketAlreadyUsedError):
        ticket.validate(bus)


def test_ticket_valid_within_60_min():
    """Тест 5: Билет, созданный 30 минут назад, успешно валидируется."""
    past_time = datetime.now() - timedelta(minutes=30)
    ticket = SingleTripTicket(issued_at=past_time, valid_minutes=60)
    bus = Bus("12")
    assert ticket.validate(bus) is True
    assert ticket.is_validated is True


def test_ticket_expired_error():
    """Тест 6: Билет, созданный 65 минут назад, выбрасывает TicketExpiredError."""
    expired_time = datetime.now() - timedelta(minutes=65)
    ticket = SingleTripTicket(issued_at=expired_time, valid_minutes=60)
    bus = Bus("12")

    with pytest.raises(TicketExpiredError):
        ticket.validate(bus)
    assert ticket.is_validated is False  # Статус не должен стать True при ошибке


def test_ticket_encapsulation_no_setter():
    """Тест 7: Сокрытие данных: попытка прямой записи в is_validated вызывает AttributeError."""
    ticket = SingleTripTicket()
    with pytest.raises(AttributeError):
        ticket.is_validated = True


def test_bus_initialization():
    """Тест 8: Инициализация автобуса с номером маршрута и пустым журналом."""
    bus = Bus("Route-79")
    assert bus.route_number == "Route-79"
    assert isinstance(bus.validations, list)
    assert len(bus.validations) == 0


def test_bus_accepts_transit_card():
    """Тест 9: Автобус успешно списывает оплату с TransitCard."""
    bus = Bus("Route-32")
    card = TransitCard("C-100", initial_balance=Decimal("500"))
    result = bus.process_payment(card)
    assert result is True
    assert card.balance == Decimal("400")
    assert len(bus.validations) == 1


def test_bus_accepts_single_ticket():
    """Тест 10: Автобус успешно валидирует SingleTripTicket."""
    bus = Bus("Route-32")
    ticket = SingleTripTicket()
    result = bus.process_payment(ticket)
    assert result is True
    assert ticket.is_validated is True
    assert len(bus.validations) == 1

    # Повторная оплата тем же билетом вызывает TicketAlreadyUsedError
    with pytest.raises(TicketAlreadyUsedError):
        bus.process_payment(ticket)
'''

LAB_TASK = {
    "title": "Лабораторная работа №1: Проектирование классов SingleTripTicket и Bus",
    "points": 10,
    "estimated_time": "60 минут",
    "description": (
        "Спроектируйте одноразовый билет `SingleTripTicket` и транспортное средство `Bus`. "
        "Билет обязан защищать два строгих инварианта: однократность использования "
        "(повторный проход вызывает `TicketAlreadyUsedError`) и ограничение по времени "
        "действия (60 минут, после чего возбуждается `TicketExpiredError`). "
        "Поле `is_validated` должно быть реализовано строго через `@property` без сеттера."
    ),
    "starter_code": STARTER_CODE,
    "reference_solution": REFERENCE_SOLUTION,
    "secret_tests": SECRET_TESTS,
    "test_count": 10,
}
