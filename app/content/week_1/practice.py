"""Practice task for Week 1: TransitCard Encapsulation and Invariant Defense."""

STARTER_CODE = '''from decimal import Decimal

# 1. Определите иерархию исключений
class DomainError(Exception):
    """Базовое исключение домена."""
    pass

class InsufficientFundsError(DomainError):
    """Недостаточно средств на карте."""
    pass

class CardBlockedError(DomainError):
    """Карта заблокирована."""
    pass

class InvalidAmountError(DomainError):
    """Некорректная сумма пополнения или списания."""
    pass


# 2. Реализуйте богатую сущность TransitCard
class TransitCard:
    """Транспортная карта Avtobys с инкапсуляцией баланса и защитой инвариантов."""

    def __init__(
        self,
        card_id: str,
        initial_balance: Decimal = Decimal("0"),
        discount_rate: Decimal = Decimal("0.0"),
    ):
        # TODO: Проверьте инварианты начального баланса (>= 0) и скидки (от 0.0 до 1.0).
        # При нарушении возбуждайте ValueError.
        # Сохраните приватные атрибуты: _card_id, _balance, _discount_rate, _is_blocked.
        pass

    @property
    def balance(self) -> Decimal:
        """Текущий баланс карты (только для чтения)."""
        # TODO: Верните приватный баланс
        pass

    @property
    def is_blocked(self) -> bool:
        """Статус блокировки карты."""
        # TODO: Верните флаг блокировки
        pass

    def top_up(self, amount: Decimal) -> None:
        """Пополнение баланса карты.

        Инварианты:
        - Заблокированную карту пополнять нельзя (CardBlockedError).
        - Минимальная сумма пополнения 100 тенге (InvalidAmountError при amount < 100).
        """
        # TODO: Реализуйте метод с проверкой инвариантов
        pass

    def pay(self, fare: Decimal) -> Decimal:
        """Списание стоимости проезда с учетом скидки.

        Инварианты:
        - Заблокированная карта не может совершать оплату (CardBlockedError).
        - Стоимость проезда должна быть строго больше 0 (InvalidAmountError при fare <= 0).
        - effective_fare = fare * (1 - discount_rate).
        - Баланс не может уйти в минус (InsufficientFundsError при balance < effective_fare).

        Возвращает списанную сумму effective_fare.
        """
        # TODO: Реализуйте списание
        pass

    def block(self) -> None:
        """Блокировка карты."""
        # TODO: Установите _is_blocked = True
        pass

    def unblock(self) -> None:
        """Разблокировка карты."""
        # TODO: Установите _is_blocked = False
        pass
'''

REFERENCE_SOLUTION = '''from decimal import Decimal

class DomainError(Exception):
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

    def block(self) -> None:
        self._is_blocked = True

    def unblock(self) -> None:
        self._is_blocked = False
'''

SECRET_TESTS = '''from decimal import Decimal
import pytest
from solution import (
    CardBlockedError,
    DomainError,
    InsufficientFundsError,
    InvalidAmountError,
    TransitCard,
)


def test_initial_balance_non_negative():
    """Тест 1: Запрет отрицательного баланса при создании карты."""
    card = TransitCard("K1", Decimal("500"))
    assert card.balance == Decimal("500")

    with pytest.raises(ValueError):
        TransitCard("K2", Decimal("-50"))


def test_top_up_valid():
    """Тест 2: Успешное пополнение баланса карты."""
    card = TransitCard("K1", Decimal("200"))
    card.top_up(Decimal("300"))
    assert card.balance == Decimal("500")


def test_top_up_minimum_amount():
    """Тест 3: Защита инварианта минимального пополнения (не менее 100 ₸)."""
    card = TransitCard("K1", Decimal("200"))
    with pytest.raises(InvalidAmountError):
        card.top_up(Decimal("99"))

    with pytest.raises(InvalidAmountError):
        card.top_up(Decimal("-100"))


def test_pay_standard_fare():
    """Тест 4: Успешное списание стандартного тарифа."""
    card = TransitCard("K1", Decimal("500"))
    paid = card.pay(Decimal("100"))
    assert paid == Decimal("100")
    assert card.balance == Decimal("400")


def test_pay_with_discount():
    """Тест 5: Корректный расчет тарифа с учетом скидки карты."""
    card = TransitCard("K1", Decimal("500"), discount_rate=Decimal("0.5"))
    paid = card.pay(Decimal("100"))
    assert paid == Decimal("50.0")
    assert card.balance == Decimal("450.0")


def test_pay_insufficient_funds():
    """Тест 6: Выброс InsufficientFundsError при нехватке средств."""
    card = TransitCard("K1", Decimal("80"))
    with pytest.raises(InsufficientFundsError):
        card.pay(Decimal("100"))
    assert card.balance == Decimal("80")  # Баланс не изменился


def test_blocked_card_operations():
    """Тест 7: Выброс CardBlockedError при операциях с заблокированной картой."""
    card = TransitCard("K1", Decimal("1000"))
    card.block()
    assert card.is_blocked is True

    with pytest.raises(CardBlockedError):
        card.pay(Decimal("100"))

    with pytest.raises(CardBlockedError):
        card.top_up(Decimal("200"))

    card.unblock()
    assert card.is_blocked is False
    card.pay(Decimal("100"))
    assert card.balance == Decimal("900")
'''

PRACTICE_TASK = {
    "title": "Практикум: Разработка класса TransitCard с защитой инвариантов",
    "points": 7,
    "estimated_time": "60 минут",
    "description": (
        "Разработайте богатую сущность `TransitCard` для транспортной системы Avtobys. "
        "Карта обязана инкапсулировать баланс и защищать инварианты целостности данных: "
        "баланс не может уходить в минус, пополнение должно быть не менее 100 тенге, "
        "с заблокированной картой запрещены любые операции, а скидка применяется строго по формуле."
    ),
    "starter_code": STARTER_CODE,
    "reference_solution": REFERENCE_SOLUTION,
    "secret_tests": SECRET_TESTS,
    "test_count": 7,
}
