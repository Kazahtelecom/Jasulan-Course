"""Three connected step-by-step Practice coding tasks for Week 3: GoF Patterns & Clean Architecture."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

PRACTICE_TASKS: list[dict[str, Any]] = [
    {
        "id": "w3_task_1",
        "step_number": 1,
        "title": "Задача 1. Строитель смены и Адаптер банка (Builder + Adapter)",
        "difficulty": "Шаг 1 · Порождающий + Структурный GoF",
        "max_score": 0.0,
        "story": (
            "Начнем сборку компонентов Недели 3! По материалам Лабораторной 6 и 7 реализуем два класса: "
            "1) ShiftReportBuilder — строитель отчёта смены автобуса с защитой от пустых полей маршрута/водителя (IncompleteReportError); "
            "2) BankApiAdapter — структурный адаптер к устаревшей банковской системе LegacyBankClient, переводящий тенге в тиыны (amount * 100)."
        ),
        "instructions": [
            "Создайте исключение IncompleteReportError(ValueError).",
            "Реализуйте класс ShiftReportBuilder с Fluent API: .set_shift_info(route_id, driver_id), .add_qr_revenue(amount), .record_incident(description) и .build() -> DailyShiftReport.",
            "Метод .build() должен выбрасывать IncompleteReportError, если route_id или driver_id не заданы.",
            "Реализуйте BankApiAdapter: конструктор принимает external_client и transit_account, а метод charge(card_id, amount: Decimal) переводит тенге в тиыны int(amount * 100), вызывает execute_payment_kzt и возвращает auth_code.",
        ],
        "hint": (
            "Подсказка:\n"
            "В методе build() проверьте:\n"
            "if not self._route_id or not self._driver_id:\n"
            "    raise IncompleteReportError('Route and driver are required')\n\n"
            "В BankApiAdapter.charge():\n"
            "tiyn = int(amount * 100)\n"
            "res = self._client.execute_payment_kzt(card_id, self._account, tiyn)\n"
            "return res['auth_code']"
        ),
        "starter_code": """from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DailyShiftReport:
    route_id: str
    driver_id: str
    total_revenue: Decimal
    incidents: tuple[str, ...] = ()


class IncompleteReportError(ValueError):
    \"\"\"Выбрасывается, когда обязательные поля отчета смены не заполнены.\"\"\"
    pass


class ShiftReportBuilder:
    \"\"\"Порождающий паттерн Builder для финансового отчета смены Avtobys.\"\"\"

    def __init__(self) -> None:
        self._route_id: str | None = None
        self._driver_id: str | None = None
        self._total_revenue: Decimal = Decimal("0")
        self._incidents: list[str] = []

    def set_shift_info(self, route_id: str, driver_id: str) -> "ShiftReportBuilder":
        # Шаг 1: Запомните маршрут и водителя, верните self
        pass

    def add_qr_revenue(self, amount: Decimal) -> "ShiftReportBuilder":
        # Шаг 2: Прибавьте сумму к выручке, верните self
        pass

    def record_incident(self, description: str) -> "ShiftReportBuilder":
        # Шаг 3: Добавьте описание инцидента, верните self
        pass

    def build(self) -> DailyShiftReport:
        # Шаг 4: Проверьте обязательные поля (или IncompleteReportError) и верните DailyShiftReport
        pass


class LegacyBankClient:
    \"\"\"Сторонний банковский клиент с устаревшим интерфейсом.\"\"\"

    def execute_payment_kzt(self, source_pan: str, dest_account: str, amount_tiyn: int) -> dict:
        return {"auth_code": f"AUTH-{source_pan}-{amount_tiyn}"}


class BankApiAdapter:
    \"\"\"Структурный паттерн Adapter: переводит Decimal KZT в целочисленные тиыны.\"\"\"

    def __init__(self, external_client: LegacyBankClient, transit_account: str) -> None:
        self._client = external_client
        self._account = transit_account

    def charge(self, card_id: str, amount: Decimal) -> str:
        # Шаг 5: Переведите Decimal в тиыны (int(amount * 100)) и вызовите execute_payment_kzt
        pass
""",
        "reference_solution": """from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DailyShiftReport:
    route_id: str
    driver_id: str
    total_revenue: Decimal
    incidents: tuple[str, ...] = ()


class IncompleteReportError(ValueError):
    \"\"\"Выбрасывается, когда обязательные поля отчета смены не заполнены.\"\"\"
    pass


class ShiftReportBuilder:
    \"\"\"Порождающий паттерн Builder для финансового отчета смены Avtobys.\"\"\"

    def __init__(self) -> None:
        self._route_id: str | None = None
        self._driver_id: str | None = None
        self._total_revenue: Decimal = Decimal("0")
        self._incidents: list[str] = []

    def set_shift_info(self, route_id: str, driver_id: str) -> "ShiftReportBuilder":
        self._route_id = route_id
        self._driver_id = driver_id
        return self

    def add_qr_revenue(self, amount: Decimal) -> "ShiftReportBuilder":
        self._total_revenue += amount
        return self

    def record_incident(self, description: str) -> "ShiftReportBuilder":
        self._incidents.append(description)
        return self

    def build(self) -> DailyShiftReport:
        if not self._route_id or not self._driver_id:
            raise IncompleteReportError("Route ID and Driver ID are required to build a report")
        return DailyShiftReport(
            route_id=self._route_id,
            driver_id=self._driver_id,
            total_revenue=self._total_revenue,
            incidents=tuple(self._incidents),
        )


class LegacyBankClient:
    \"\"\"Сторонний банковский клиент с устаревшим интерфейсом.\"\"\"

    def execute_payment_kzt(self, source_pan: str, dest_account: str, amount_tiyn: int) -> dict:
        return {"auth_code": f"AUTH-{source_pan}-{amount_tiyn}"}


class BankApiAdapter:
    \"\"\"Структурный паттерн Adapter: переводит Decimal KZT в целочисленные тиыны.\"\"\"

    def __init__(self, external_client: LegacyBankClient, transit_account: str) -> None:
        self._client = external_client
        self._account = transit_account

    def charge(self, card_id: str, amount: Decimal) -> str:
        amount_tiyn = int(amount * 100)
        res = self._client.execute_payment_kzt(card_id, self._account, amount_tiyn)
        return res["auth_code"]
""",
        "test_code": """from decimal import Decimal
import pytest
from solution import BankApiAdapter, DailyShiftReport, IncompleteReportError, LegacyBankClient, ShiftReportBuilder


def test_builder_fluent_assembly():
    builder = ShiftReportBuilder()
    report = (
        builder.set_shift_info(route_id="10A", driver_id="DRV-42")
        .add_qr_revenue(Decimal("15000"))
        .add_qr_revenue(Decimal("7500"))
        .record_incident("Задержка рейса 5 мин")
        .build()
    )
    assert isinstance(report, DailyShiftReport)
    assert report.route_id == "10A"
    assert report.driver_id == "DRV-42"
    assert report.total_revenue == Decimal("22500")
    assert report.incidents == ("Задержка рейса 5 мин",)


def test_builder_incomplete_validation_error():
    builder = ShiftReportBuilder()
    builder.add_qr_revenue(Decimal("5000"))
    with pytest.raises(IncompleteReportError):
        builder.build()


def test_bank_api_adapter_tiyn_conversion():
    legacy = LegacyBankClient()
    adapter = BankApiAdapter(legacy, transit_account="TRANSIT-KZT-99")
    auth = adapter.charge(card_id="CARD-8888", amount=Decimal("120.50"))
    assert auth == "AUTH-CARD-8888-12050"
""",
    },
    {
        "id": "w3_task_2",
        "step_number": 2,
        "title": "Задача 2. Цепочка проверок и Наблюдатель телеметрии (Chain of Responsibility + Observer)",
        "difficulty": "Шаг 2 · Поведенческие GoF",
        "max_score": 0.0,
        "story": (
            "Переходим к поведению системы! По материалам Лабораторной 8 реализуем:\n"
            "1) Цепочку проверок ValidationHandler: если карта в черном списке, BlacklistCheckHandler отклоняет оплату ('Карта в черном списке'); "
            "если не хватает баланса, BalanceCheckHandler отклоняет запрос ('Недостаточно средств');\n"
            "2) TransitTelemetrySubject — издатель событий телеметрии (Observer), который уведомляет подписчиков вызовом .update(event)."
        ),
        "instructions": [
            "Реализуйте базовый класс ValidationHandler с методами set_next(handler) и handle(request) -> ValidationResult.",
            "Реализуйте BlacklistCheckHandler: если request.card_id in request.blacklisted_cards, вернуть ValidationResult(False, 'Карта в черном списке'), иначе передать следующему.",
            "Реализуйте BalanceCheckHandler: если request.balance < request.fare, вернуть ValidationResult(False, 'Недостаточно средств'), иначе передать следующему.",
            "Реализуйте TransitTelemetrySubject: методы attach(observer), detach(observer) и notify(event: str), вызывающий obs.update(event).",
        ],
        "hint": (
            "Подсказка:\n"
            "В BlacklistCheckHandler:\n"
            "if request.card_id in request.blacklisted_cards:\n"
            "    return ValidationResult(is_approved=False, reason='Карта в черном списке')\n"
            "return super().handle(request)\n\n"
            "В TransitTelemetrySubject.notify():\n"
            "for obs in self._observers:\n"
            "    obs.update(event)"
        ),
        "starter_code": """from abc import ABC
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class PaymentRequest:
    card_id: str
    balance: Decimal
    fare: Decimal
    blacklisted_cards: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class ValidationResult:
    is_approved: bool
    reason: str = "OK"


class ValidationHandler(ABC):
    \"\"\"Базовый класс цепочки обязанностей (Chain of Responsibility).\"\"\"

    def __init__(self) -> None:
        self._next: ValidationHandler | None = None

    def set_next(self, handler: "ValidationHandler") -> "ValidationHandler":
        # Шаг 1: Сохраните следующий обработчик и верните его
        pass

    def handle(self, request: PaymentRequest) -> ValidationResult:
        # Шаг 2: Передайте следующему или верните одобрение (is_approved=True)
        pass


class BlacklistCheckHandler(ValidationHandler):
    \"\"\"Проверяет карту на блокировку в черном списке.\"\"\"

    def handle(self, request: PaymentRequest) -> ValidationResult:
        # Шаг 3: Проверьте наличие card_id в blacklisted_cards
        pass


class BalanceCheckHandler(ValidationHandler):
    \"\"\"Проверяет достаточность баланса карты.\"\"\"

    def handle(self, request: PaymentRequest) -> ValidationResult:
        # Шаг 4: Проверьте условие balance < fare
        pass


class TransitTelemetrySubject:
    \"\"\"Издатель событий телеметрии (паттерн Observer).\"\"\"

    def __init__(self) -> None:
        self._observers: list[Any] = []

    def attach(self, observer: Any) -> None:
        # Шаг 5: Добавьте наблюдателя в список
        pass

    def detach(self, observer: Any) -> None:
        # Шаг 6: Удалите наблюдателя из списка
        pass

    def notify(self, event: str) -> None:
        # Шаг 7: Оповестите всех наблюдателей вызовом observer.update(event)
        pass
""",
        "reference_solution": """from abc import ABC
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass
class PaymentRequest:
    card_id: str
    balance: Decimal
    fare: Decimal
    blacklisted_cards: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class ValidationResult:
    is_approved: bool
    reason: str = "OK"


class ValidationHandler(ABC):
    \"\"\"Базовый класс цепочки обязанностей (Chain of Responsibility).\"\"\"

    def __init__(self) -> None:
        self._next: ValidationHandler | None = None

    def set_next(self, handler: "ValidationHandler") -> "ValidationHandler":
        self._next = handler
        return handler

    def handle(self, request: PaymentRequest) -> ValidationResult:
        if self._next:
            return self._next.handle(request)
        return ValidationResult(is_approved=True, reason="OK")


class BlacklistCheckHandler(ValidationHandler):
    \"\"\"Проверяет карту на блокировку в черном списке.\"\"\"

    def handle(self, request: PaymentRequest) -> ValidationResult:
        if request.card_id in request.blacklisted_cards:
            return ValidationResult(is_approved=False, reason="Карта в черном списке")
        return super().handle(request)


class BalanceCheckHandler(ValidationHandler):
    \"\"\"Проверяет достаточность баланса карты.\"\"\"

    def handle(self, request: PaymentRequest) -> ValidationResult:
        if request.balance < request.fare:
            return ValidationResult(is_approved=False, reason="Недостаточно средств")
        return super().handle(request)


class TransitTelemetrySubject:
    \"\"\"Издатель событий телеметрии (паттерн Observer).\"\"\"

    def __init__(self) -> None:
        self._observers: list[Any] = []

    def attach(self, observer: Any) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Any) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: str) -> None:
        for observer in self._observers:
            observer.update(event)
""",
        "test_code": """from decimal import Decimal
from solution import BalanceCheckHandler, BlacklistCheckHandler, PaymentRequest, TransitTelemetrySubject


def test_chain_blacklist_rejection():
    chain = BlacklistCheckHandler()
    chain.set_next(BalanceCheckHandler())

    req = PaymentRequest(
        card_id="BLOCKED-1",
        balance=Decimal("500"),
        fare=Decimal("100"),
        blacklisted_cards={"BLOCKED-1", "STOLEN-9"},
    )
    res = chain.handle(req)
    assert not res.is_approved
    assert res.reason == "Карта в черном списке"


def test_chain_insufficient_balance_rejection():
    chain = BlacklistCheckHandler()
    chain.set_next(BalanceCheckHandler())

    req = PaymentRequest(
        card_id="VALID-1",
        balance=Decimal("40"),
        fare=Decimal("100"),
        blacklisted_cards=set(),
    )
    res = chain.handle(req)
    assert not res.is_approved
    assert res.reason == "Недостаточно средств"


def test_chain_successful_approval():
    chain = BlacklistCheckHandler()
    chain.set_next(BalanceCheckHandler())

    req = PaymentRequest(
        card_id="VALID-2",
        balance=Decimal("350"),
        fare=Decimal("100"),
        blacklisted_cards=set(),
    )
    res = chain.handle(req)
    assert res.is_approved
    assert res.reason == "OK"


def test_observer_telemetry_notifications():
    class TestLogger:
        def __init__(self):
            self.events = []

        def update(self, event: str) -> None:
            self.events.append(event)

    logger = TestLogger()
    subject = TransitTelemetrySubject()
    subject.attach(logger)
    subject.notify("BUS_START")
    subject.notify("PAYMENT_SUCCESS")
    assert logger.events == ["BUS_START", "PAYMENT_SUCCESS"]

    subject.detach(logger)
    subject.notify("BUS_STOP")
    assert logger.events == ["BUS_START", "PAYMENT_SUCCESS"]
""",
    },
    {
        "id": "w3_task_3",
        "step_number": 3,
        "title": "Задача 3. Слой Use Case Чистой Архитектуры (Clean Architecture)",
        "difficulty": "Шаг 3 · Чистая Архитектура",
        "max_score": 0.0,
        "story": (
            "Финальный аккорд курса! По материалам Лабораторной 9 реализуем Use Case регистрации поездки: "
            "1) Value Object Money(amount, currency='KZT') и Entity TransitCard.charge_fare(fare: Money); "
            "2) ValidateRideUseCase — интерактор, координирующий получение карты из репозитория, списание тарифа, "
            "проведение платежа через шлюз и сохранение карты без жесткой привязки к инфраструктуре."
        ),
        "instructions": [
            "Создайте класс TransitCard с методом charge_fare(fare: Money). Если balance < fare.amount, выбрасывать ValueError('Insufficient funds'), иначе уменьшить balance.",
            "Реализуйте класс ValidateRideUseCase(card_repo, payment_gateway).",
            "В методе execute(request: ValidateRideRequest) -> ValidateRideResponse: 1) получить карту repo.get_by_id(request.card_id); 2) списать тариф card.charge_fare(Money(request.fare_amount)); 3) вызвать payment_gateway.charge(card.card_id, request.fare_amount); 4) сохранить repo.save(card); 5) вернуть ValidateRideResponse(True, card.balance, tx_id).",
        ],
        "hint": (
            "Подсказка:\n"
            "В ValidateRideUseCase.execute():\n"
            "card = self._card_repo.get_by_id(request.card_id)\n"
            "fare = Money(request.fare_amount)\n"
            "card.charge_fare(fare)\n"
            "tx_id = self._payment_gw.charge(card.card_id, fare.amount)\n"
            "self._card_repo.save(card)\n"
            "return ValidateRideResponse(success=True, remaining_balance=card.balance, tx_id=tx_id)"
        ),
        "starter_code": """from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "KZT"


@dataclass
class TransitCard:
    card_id: str
    balance: Decimal

    def charge_fare(self, fare: Money) -> None:
        # Шаг 1: Проверьте баланс (или ValueError) и спишите fare.amount
        pass


@dataclass(frozen=True)
class ValidateRideRequest:
    card_id: str
    fare_amount: Decimal


@dataclass(frozen=True)
class ValidateRideResponse:
    success: bool
    remaining_balance: Decimal
    tx_id: str


class ValidateRideUseCase:
    \"\"\"Прикладной сценарий Use Case в соответствии с Clean Architecture.\"\"\"

    def __init__(self, card_repo, payment_gateway) -> None:
        self._card_repo = card_repo
        self._payment_gateway = payment_gateway

    def execute(self, request: ValidateRideRequest) -> ValidateRideResponse:
        # Шаг 2: Скоординируйте Entity, Gateway и Repository
        pass
""",
        "reference_solution": """from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "KZT"


@dataclass
class TransitCard:
    card_id: str
    balance: Decimal

    def charge_fare(self, fare: Money) -> None:
        if self.balance < fare.amount:
            raise ValueError("Insufficient funds")
        self.balance -= fare.amount


@dataclass(frozen=True)
class ValidateRideRequest:
    card_id: str
    fare_amount: Decimal


@dataclass(frozen=True)
class ValidateRideResponse:
    success: bool
    remaining_balance: Decimal
    tx_id: str


class ValidateRideUseCase:
    \"\"\"Прикладной сценарий Use Case в соответствии с Clean Architecture.\"\"\"

    def __init__(self, card_repo, payment_gateway) -> None:
        self._card_repo = card_repo
        self._payment_gateway = payment_gateway

    def execute(self, request: ValidateRideRequest) -> ValidateRideResponse:
        card = self._card_repo.get_by_id(request.card_id)
        fare = Money(request.fare_amount)
        card.charge_fare(fare)
        tx_id = self._payment_gateway.charge(card.card_id, fare.amount)
        self._card_repo.save(card)
        return ValidateRideResponse(
            success=True,
            remaining_balance=card.balance,
            tx_id=tx_id,
        )
""",
        "test_code": """from decimal import Decimal
import pytest
from solution import Money, TransitCard, ValidateRideRequest, ValidateRideResponse, ValidateRideUseCase


class InMemoryCardRepository:
    def __init__(self, card: TransitCard):
        self.card = card
        self.saved = False

    def get_by_id(self, card_id: str) -> TransitCard:
        if self.card.card_id == card_id:
            return self.card
        raise KeyError("Card not found")

    def save(self, card: TransitCard) -> None:
        self.card = card
        self.saved = True


class MockPaymentGateway:
    def __init__(self):
        self.charge_calls = []

    def charge(self, card_id: str, amount: Decimal) -> str:
        self.charge_calls.append((card_id, amount))
        return f"TX-{card_id}-{amount}"


def test_clean_arch_successful_ride_execution():
    card = TransitCard(card_id="AVT-001", balance=Decimal("500"))
    repo = InMemoryCardRepository(card)
    gw = MockPaymentGateway()

    use_case = ValidateRideUseCase(card_repo=repo, payment_gateway=gw)
    req = ValidateRideRequest(card_id="AVT-001", fare_amount=Decimal("100"))
    res = use_case.execute(req)

    assert isinstance(res, ValidateRideResponse)
    assert res.success is True
    assert res.remaining_balance == Decimal("400")
    assert res.tx_id == "TX-AVT-001-100"
    assert repo.saved is True
    assert gw.charge_calls == [("AVT-001", Decimal("100"))]


def test_clean_arch_insufficient_funds_rejection():
    card = TransitCard(card_id="AVT-002", balance=Decimal("30"))
    repo = InMemoryCardRepository(card)
    gw = MockPaymentGateway()

    use_case = ValidateRideUseCase(card_repo=repo, payment_gateway=gw)
    req = ValidateRideRequest(card_id="AVT-002", fare_amount=Decimal("100"))

    with pytest.raises(ValueError, match="Insufficient funds"):
        use_case.execute(req)
    assert not repo.saved
    assert len(gw.charge_calls) == 0
""",
    },
]


def get_practice_task(task_id: str) -> dict[str, Any] | None:
    """Return a Week 3 practice task definition by its ID."""
    for task in PRACTICE_TASKS:
        if task["id"] == task_id:
            return task
    return None
