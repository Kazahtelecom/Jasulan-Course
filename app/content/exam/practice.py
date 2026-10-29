"""Two connected comprehensive Practice coding tasks for Final Exam (2 x 10.0 = 20.0 points).

Task 1 (exam_task_1): Core Domain Model, Invariants & Dependency Injection (10.0 points).
Task 2 (exam_task_2): GoF Design Patterns & Clean Architecture Terminal Facade (10.0 points).
Strictly compliant with ASTValidator whitelist and executed in sandbox.
"""

from __future__ import annotations

from typing import Any

PRACTICE_TASKS: list[dict[str, Any]] = [
    {
        "id": "exam_task_1",
        "step_number": 1,
        "title": "Экзаменационная задача 1. Доменная модель, инварианты и Dependency Injection (SOLID)",
        "difficulty": "10.0 баллов · Core Domain & SOLID",
        "max_score": 10.0,
        "story": (
            "Спроектируйте ядро доменной модели тарификации и оплаты проезда в транспортной системе Avtobys. "
            "Система должна строго контролировать доменные инварианты, соблюдать принципы SOLID и использовать "
            "Dependency Injection через конструктор для подстановки стратегий расчета тарифа."
        ),
        "instructions": [
            "1. Создайте исключения: InvalidAmountError(ValueError) и InsufficientFundsError(ValueError).",
            "2. Реализуйте неизменяемый Value Object Money(amount: Decimal, currency: str = 'KZT') с проверкой amount >= 0 (иначе InvalidAmountError).",
            "3. Реализуйте сущность SmartCard(card_id: str, balance: Decimal = Decimal('0'), is_active: bool = True): свойство balance, методы top_up(amount: Decimal) и deduct(amount: Decimal). При deduct проверьте: если карта неактивна — ValueError('Card is inactive'); если amount <= 0 — InvalidAmountError; если balance < amount — InsufficientFundsError.",
            "4. Объявите абстрактный интерфейс ITariffStrategy(ABC) с методом calculate_fare(base_fare: Decimal, passenger_type: str) -> Decimal.",
            "5. Реализуйте StandardTariffStrategy(ITariffStrategy): для passenger_type == 'student' тариф равен 50.0 ₸; для 'child' — 45.0 ₸; для остальных типов — base_fare.",
            "6. Реализуйте класс TransitFareManager: принимает strategy: ITariffStrategy в конструкторе (Constructor Injection). Метод process_payment(card: SmartCard, passenger_type: str, base_fare: Decimal = Decimal('90.0')) -> Decimal рассчитывает тариф через стратегию, списывает сумму с карты методом card.deduct() и возвращает списанную сумму.",
        ],
        "hint": (
            "Подсказка по контрактам:\n"
            "- В Money.__post_init__() проверьте: if self.amount < Decimal('0'): raise InvalidAmountError(...)\n"
            "- В SmartCard используйте приватное поле _balance: Decimal\n"
            "- В TransitFareManager: fare = self.strategy.calculate_fare(base_fare, passenger_type); if fare > Decimal('0'): card.deduct(fare); return fare"
        ),
        "starter_code": '''from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


class InvalidAmountError(ValueError):
    """Выбрасывается при попытке передачи отрицательной или нулевой суммы."""
    pass


class InsufficientFundsError(ValueError):
    """Выбрасывается при нехватке средств на балансе карты."""
    pass


@dataclass(frozen=True)
class Money:
    """Неизменяемый Value Object денежной суммы."""
    amount: Decimal
    currency: str = "KZT"

    def __post_init__(self) -> None:
        # TODO: проверьте, что amount >= Decimal("0"), иначе InvalidAmountError
        pass


class SmartCard:
    """Сущность транспортной карты Avtobys с инкапсулированным балансом."""

    def __init__(self, card_id: str, balance: Decimal = Decimal("0"), is_active: bool = True) -> None:
        self.card_id = card_id
        self._balance = balance
        self.is_active = is_active

    @property
    def balance(self) -> Decimal:
        return self._balance

    def top_up(self, amount: Decimal) -> None:
        # TODO: если amount <= 0, выбросить InvalidAmountError. Иначе пополнить _balance
        pass

    def deduct(self, amount: Decimal) -> None:
        # TODO:
        # 1. Если не self.is_active: raise ValueError("Card is inactive")
        # 2. Если amount <= 0: raise InvalidAmountError("Deduction amount must be positive")
        # 3. Если self._balance < amount: raise InsufficientFundsError("Not enough funds")
        # 4. self._balance -= amount
        pass


class ITariffStrategy(ABC):
    """Абстрактный контракт стратегии тарифа (OCP / DIP)."""

    @abstractmethod
    def calculate_fare(self, base_fare: Decimal, passenger_type: str) -> Decimal:
        pass


class StandardTariffStrategy(ITariffStrategy):
    """Стандартная тарифная сетка: студенты 50 ₸, дети 45 ₸, остальные base_fare."""

    def calculate_fare(self, base_fare: Decimal, passenger_type: str) -> Decimal:
        # TODO: вернуть Decimal("50.0") для "student", Decimal("45.0") для "child", иначе base_fare
        pass


class TransitFareManager:
    """Сервис тарификации и оплаты проезда (DIP через Constructor Injection)."""

    def __init__(self, strategy: ITariffStrategy) -> None:
        self.strategy = strategy

    def process_payment(
        self,
        card: SmartCard,
        passenger_type: str,
        base_fare: Decimal = Decimal("90.0"),
    ) -> Decimal:
        # TODO: рассчитать тариф, списать с карты через card.deduct(), вернуть сумму
        pass
''',
        "reference_solution": '''from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


class InvalidAmountError(ValueError):
    """Выбрасывается при попытке передачи отрицательной или нулевой суммы."""
    pass


class InsufficientFundsError(ValueError):
    """Выбрасывается при нехватке средств на балансе карты."""
    pass


@dataclass(frozen=True)
class Money:
    """Неизменяемый Value Object денежной суммы."""
    amount: Decimal
    currency: str = "KZT"

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise InvalidAmountError("Money amount cannot be negative")


class SmartCard:
    """Сущность транспортной карты Avtobys с инкапсулированным балансом."""

    def __init__(self, card_id: str, balance: Decimal = Decimal("0"), is_active: bool = True) -> None:
        self.card_id = card_id
        self._balance = balance
        self.is_active = is_active

    @property
    def balance(self) -> Decimal:
        return self._balance

    def top_up(self, amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise InvalidAmountError("Top up amount must be positive")
        self._balance += amount

    def deduct(self, amount: Decimal) -> None:
        if not self.is_active:
            raise ValueError("Card is inactive")
        if amount <= Decimal("0"):
            raise InvalidAmountError("Deduction amount must be positive")
        if self._balance < amount:
            raise InsufficientFundsError("Not enough funds on card")
        self._balance -= amount


class ITariffStrategy(ABC):
    """Абстрактный контракт стратегии тарифа (OCP / DIP)."""

    @abstractmethod
    def calculate_fare(self, base_fare: Decimal, passenger_type: str) -> Decimal:
        pass


class StandardTariffStrategy(ITariffStrategy):
    """Стандартная тарифная сетка: студенты 50 ₸, дети 45 ₸, остальные base_fare."""

    def calculate_fare(self, base_fare: Decimal, passenger_type: str) -> Decimal:
        clean_type = passenger_type.lower().strip()
        if clean_type == "student":
            return Decimal("50.0")
        if clean_type == "child":
            return Decimal("45.0")
        return base_fare


class TransitFareManager:
    """Сервис тарификации и оплаты проезда (DIP через Constructor Injection)."""

    def __init__(self, strategy: ITariffStrategy) -> None:
        self.strategy = strategy

    def process_payment(
        self,
        card: SmartCard,
        passenger_type: str,
        base_fare: Decimal = Decimal("90.0"),
    ) -> Decimal:
        fare = self.strategy.calculate_fare(base_fare, passenger_type)
        if fare > Decimal("0"):
            card.deduct(fare)
        return fare
''',
        "test_code": '''import pytest
from decimal import Decimal
from solution import (
    InvalidAmountError,
    InsufficientFundsError,
    Money,
    SmartCard,
    ITariffStrategy,
    StandardTariffStrategy,
    TransitFareManager,
)


def test_money_invariants():
    m = Money(Decimal("100.5"), "KZT")
    assert m.amount == Decimal("100.5")
    assert m.currency == "KZT"

    zero_m = Money(Decimal("0.0"))
    assert zero_m.amount == Decimal("0.0")

    with pytest.raises(InvalidAmountError):
        Money(Decimal("-10.0"))


def test_smart_card_lifecycle():
    card = SmartCard("CARD-001", Decimal("200.0"))
    assert card.balance == Decimal("200.0")

    card.top_up(Decimal("300.0"))
    assert card.balance == Decimal("500.0")

    with pytest.raises(InvalidAmountError):
        card.top_up(Decimal("-50.0"))

    card.deduct(Decimal("100.0"))
    assert card.balance == Decimal("400.0")

    with pytest.raises(InsufficientFundsError):
        card.deduct(Decimal("1000.0"))

    inactive_card = SmartCard("CARD-INACTIVE", Decimal("500.0"), is_active=False)
    with pytest.raises(ValueError, match="inactive"):
        inactive_card.deduct(Decimal("50.0"))


def test_standard_tariff_strategy():
    strat = StandardTariffStrategy()
    base = Decimal("90.0")

    assert strat.calculate_fare(base, "student") == Decimal("50.0")
    assert strat.calculate_fare(base, "child") == Decimal("45.0")
    assert strat.calculate_fare(base, "regular") == Decimal("90.0")
    assert strat.calculate_fare(base, "STUDENT") == Decimal("50.0")


def test_transit_fare_manager_payment():
    strat = StandardTariffStrategy()
    manager = TransitFareManager(strat)

    card = SmartCard("CARD-STD", Decimal("150.0"))
    paid = manager.process_payment(card, "student")
    assert paid == Decimal("50.0")
    assert card.balance == Decimal("100.0")

    # Regular ride
    paid2 = manager.process_payment(card, "adult")
    assert paid2 == Decimal("90.0")
    assert card.balance == Decimal("10.0")

    # Now insufficient funds for next ride
    with pytest.raises(InsufficientFundsError):
        manager.process_payment(card, "adult")


def test_ocp_custom_tariff_strategy():
    class SeniorTariffStrategy(ITariffStrategy):
        def calculate_fare(self, base_fare: Decimal, passenger_type: str) -> Decimal:
            return Decimal("0.0")

    manager = TransitFareManager(SeniorTariffStrategy())
    card = SmartCard("CARD-SENIOR", Decimal("10.0"))
    paid = manager.process_payment(card, "senior")
    assert paid == Decimal("0.0")
    assert card.balance == Decimal("10.0")
''',
    },
    {
        "id": "exam_task_2",
        "step_number": 2,
        "title": "Экзаменационная задача 2. Паттерны GoF и Чистая Архитектура терминала (Builder, Adapter, Facade)",
        "difficulty": "10.0 баллов · GoF Patterns & Clean Architecture",
        "max_score": 10.0,
        "story": (
            "Соберите терминал оплаты смены автобуса Avtobys, объединив три ключевых паттерна GoF и Чистую Архитектуру:\n"
            "1) Порождающий паттерн Builder (DailyShiftReportBuilder) для аккуратного формирования финансового отчета смены;\n"
            "2) Структурный паттерн Adapter (BankGatewayAdapter) для интеграции устаревшего внешнего банковского клиента LegacyBankClient (перевод тенге в тиыны);\n"
            "3) Структурный паттерн Facade (TerminalFacade) для координации оплат по транспортной и банковской карте и закрытия смены."
        ),
        "instructions": [
            "1. Создайте исключение IncompleteReportError(ValueError).",
            "2. Создайте неизменяемый dataclass DailyShiftReport(route_id: str, bus_number: str, total_revenue: Decimal, validations_count: int).",
            "3. Реализуйте DailyShiftReportBuilder с Fluent API: .set_shift_info(route_id: str, bus_number: str), .add_revenue(amount: Decimal), .record_validation() (увеличивает счетчик валидаций на 1), .build() -> DailyShiftReport. Если route_id или bus_number не заданы, build() выбрасывает IncompleteReportError.",
            "4. Объявите абстрактный интерфейс IBankGateway(ABC) с методом charge(card_id: str, amount: Decimal) -> str.",
            "5. Реализуйте BankGatewayAdapter(IBankGateway): принимает client: LegacyBankClient в конструкторе. Метод charge переводит Decimal-сумму в целые тиыны int(amount * 100), вызывает client.execute_payment(card_id, amount_tiyn) и возвращает auth_code из ответа.",
            "6. Реализуйте TerminalFacade(fare_manager, bank_adapter, report_builder):",
            "   - process_smart_card_ride(card, passenger_type): списывает проезд через fare_manager.process_payment, добавляет выручку и валидацию в report_builder, возвращает {'status': 'SUCCESS', 'fare': fare, 'card_balance': card.balance};",
            "   - process_bank_card_ride(card_id, amount=Decimal('90.0')): списывает через bank_adapter.charge, добавляет сумму и валидацию в report_builder, возвращает {'status': 'SUCCESS', 'fare': amount, 'auth_code': auth_code};",
            "   - close_shift() -> DailyShiftReport: вызывает report_builder.build() и возвращает финальный отчет смены.",
        ],
        "hint": (
            "Подсказка:\n"
            "- В BankGatewayAdapter.charge(card_id, amount):\n"
            "    tiyn = int(amount * 100)\n"
            "    resp = self.client.execute_payment(card_id, tiyn)\n"
            "    return resp['auth_code']\n"
            "- В DailyShiftReportBuilder методы возвращают self для цепочки вызовов (Fluent Interface)."
        ),
        "starter_code": '''from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


class IncompleteReportError(ValueError):
    """Выбрасывается, если смена закрывается без указания маршрута или автобуса."""
    pass


@dataclass(frozen=True)
class DailyShiftReport:
    """Неизменяемый результат закрытия смены терминала."""
    route_id: str
    bus_number: str
    total_revenue: Decimal
    validations_count: int


class DailyShiftReportBuilder:
    """Порождающий паттерн Builder для сборки финансового отчета смены."""

    def __init__(self) -> None:
        self._route_id: str | None = None
        self._bus_number: str | None = None
        self._total_revenue: Decimal = Decimal("0")
        self._validations_count: int = 0

    def set_shift_info(self, route_id: str, bus_number: str) -> "DailyShiftReportBuilder":
        # TODO: сохранить маршрут и номер автобуса, вернуть self
        pass

    def add_revenue(self, amount: Decimal) -> "DailyShiftReportBuilder":
        # TODO: прибавить сумму к _total_revenue, вернуть self
        pass

    def record_validation(self) -> "DailyShiftReportBuilder":
        # TODO: увеличить _validations_count на 1, вернуть self
        pass

    def build(self) -> DailyShiftReport:
        # TODO: если _route_id или _bus_number не заданы, raise IncompleteReportError
        # иначе вернуть DailyShiftReport
        pass


class LegacyBankClient:
    """Устаревший внешний API банка (принимает тиыны)."""

    def execute_payment(self, card_id: str, amount_tiyn: int) -> dict[str, str]:
        return {"status": "PAID", "auth_code": f"AUTH-{card_id[-4:]}-{amount_tiyn}"}


class IBankGateway(ABC):
    """Целевой доменный контракт банковского шлюза."""

    @abstractmethod
    def charge(self, card_id: str, amount: Decimal) -> str:
        pass


class BankGatewayAdapter(IBankGateway):
    """Структурный паттерн Adapter: тенге Decimal -> тиыны int для LegacyBankClient."""

    def __init__(self, client: LegacyBankClient) -> None:
        self.client = client

    def charge(self, card_id: str, amount: Decimal) -> str:
        # TODO: перевести в тиыны (int(amount * 100)), вызвать client.execute_payment, вернуть auth_code
        pass


class TerminalFacade:
    """Паттерн Facade: единая точка входа для валидации поездок и закрытия смены."""

    def __init__(
        self,
        fare_manager: Any,
        bank_adapter: IBankGateway,
        report_builder: DailyShiftReportBuilder,
    ) -> None:
        self.fare_manager = fare_manager
        self.bank_adapter = bank_adapter
        self.report_builder = report_builder

    def process_smart_card_ride(self, card: Any, passenger_type: str) -> dict[str, Any]:
        # TODO: списать проезд через fare_manager.process_payment,
        # обновить report_builder (.add_revenue, .record_validation)
        # вернуть словарь с результатами
        pass

    def process_bank_card_ride(self, card_id: str, amount: Decimal = Decimal("90.0")) -> dict[str, Any]:
        # TODO: списать через bank_adapter.charge(card_id, amount),
        # обновить report_builder (.add_revenue, .record_validation)
        # вернуть словарь с результатами
        pass

    def close_shift(self) -> DailyShiftReport:
        # TODO: вернуть report_builder.build()
        pass
''',
        "reference_solution": '''from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


class IncompleteReportError(ValueError):
    """Выбрасывается, если смена закрывается без указания маршрута или автобуса."""
    pass


@dataclass(frozen=True)
class DailyShiftReport:
    """Неизменяемый результат закрытия смены терминала."""
    route_id: str
    bus_number: str
    total_revenue: Decimal
    validations_count: int


class DailyShiftReportBuilder:
    """Порождающий паттерн Builder для сборки финансового отчета смены."""

    def __init__(self) -> None:
        self._route_id: str | None = None
        self._bus_number: str | None = None
        self._total_revenue: Decimal = Decimal("0")
        self._validations_count: int = 0

    def set_shift_info(self, route_id: str, bus_number: str) -> "DailyShiftReportBuilder":
        self._route_id = route_id
        self._bus_number = bus_number
        return self

    def add_revenue(self, amount: Decimal) -> "DailyShiftReportBuilder":
        self._total_revenue += amount
        return self

    def record_validation(self) -> "DailyShiftReportBuilder":
        self._validations_count += 1
        return self

    def build(self) -> DailyShiftReport:
        if not self._route_id or not self._bus_number:
            raise IncompleteReportError("Route ID and bus number are required to build shift report")
        return DailyShiftReport(
            route_id=self._route_id,
            bus_number=self._bus_number,
            total_revenue=self._total_revenue,
            validations_count=self._validations_count,
        )


class LegacyBankClient:
    """Устаревший внешний API банка (принимает тиыны)."""

    def execute_payment(self, card_id: str, amount_tiyn: int) -> dict[str, str]:
        return {"status": "PAID", "auth_code": f"AUTH-{card_id[-4:]}-{amount_tiyn}"}


class IBankGateway(ABC):
    """Целевой доменный контракт банковского шлюза."""

    @abstractmethod
    def charge(self, card_id: str, amount: Decimal) -> str:
        pass


class BankGatewayAdapter(IBankGateway):
    """Структурный паттерн Adapter: тенге Decimal -> тиыны int для LegacyBankClient."""

    def __init__(self, client: LegacyBankClient) -> None:
        self.client = client

    def charge(self, card_id: str, amount: Decimal) -> str:
        amount_tiyn = int(amount * 100)
        res = self.client.execute_payment(card_id, amount_tiyn)
        return res["auth_code"]


class TerminalFacade:
    """Паттерн Facade: единая точка входа для валидации поездок и закрытия смены."""

    def __init__(
        self,
        fare_manager: Any,
        bank_adapter: IBankGateway,
        report_builder: DailyShiftReportBuilder,
    ) -> None:
        self.fare_manager = fare_manager
        self.bank_adapter = bank_adapter
        self.report_builder = report_builder

    def process_smart_card_ride(self, card: Any, passenger_type: str) -> dict[str, Any]:
        fare = self.fare_manager.process_payment(card, passenger_type)
        self.report_builder.add_revenue(fare)
        self.report_builder.record_validation()
        return {
            "status": "SUCCESS",
            "fare": fare,
            "card_balance": card.balance,
        }

    def process_bank_card_ride(self, card_id: str, amount: Decimal = Decimal("90.0")) -> dict[str, Any]:
        auth_code = self.bank_adapter.charge(card_id, amount)
        self.report_builder.add_revenue(amount)
        self.report_builder.record_validation()
        return {
            "status": "SUCCESS",
            "fare": amount,
            "auth_code": auth_code,
        }

    def close_shift(self) -> DailyShiftReport:
        return self.report_builder.build()
''',
        "test_code": '''import pytest
from decimal import Decimal
from solution import (
    IncompleteReportError,
    DailyShiftReport,
    DailyShiftReportBuilder,
    LegacyBankClient,
    IBankGateway,
    BankGatewayAdapter,
    TerminalFacade,
)


def test_shift_report_builder_fluent():
    b = DailyShiftReportBuilder()
    with pytest.raises(IncompleteReportError):
        b.build()

    b.set_shift_info("R-32", "BUS-777")
    b.add_revenue(Decimal("90.0")).add_revenue(Decimal("50.0"))
    b.record_validation().record_validation()

    report = b.build()
    assert report.route_id == "R-32"
    assert report.bus_number == "BUS-777"
    assert report.total_revenue == Decimal("140.0")
    assert report.validations_count == 2


def test_bank_gateway_adapter():
    legacy = LegacyBankClient()
    adapter = BankGatewayAdapter(legacy)

    code = adapter.charge("4400123456789999", Decimal("90.0"))
    assert code == "AUTH-9999-9000"


def test_terminal_facade_coordination():
    # Setup dependencies
    class DummyFareManager:
        def process_payment(self, card, ptype):
            card.balance -= Decimal("50.0")
            return Decimal("50.0")

    class DummyCard:
        def __init__(self):
            self.balance = Decimal("200.0")

    builder = DailyShiftReportBuilder()
    builder.set_shift_info("R-12", "BUS-101")
    legacy = LegacyBankClient()
    adapter = BankGatewayAdapter(legacy)

    facade = TerminalFacade(
        fare_manager=DummyFareManager(),
        bank_adapter=adapter,
        report_builder=builder,
    )

    card = DummyCard()
    r1 = facade.process_smart_card_ride(card, "student")
    assert r1["status"] == "SUCCESS"
    assert r1["fare"] == Decimal("50.0")
    assert r1["card_balance"] == Decimal("150.0")

    r2 = facade.process_bank_card_ride("9999111122223333", Decimal("90.0"))
    assert r2["status"] == "SUCCESS"
    assert r2["fare"] == Decimal("90.0")
    assert "AUTH-3333-9000" in r2["auth_code"]

    final_report = facade.close_shift()
    assert final_report.route_id == "R-12"
    assert final_report.bus_number == "BUS-101"
    assert final_report.total_revenue == Decimal("140.0")
    assert final_report.validations_count == 2
''',
    },
]
