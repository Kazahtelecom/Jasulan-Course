"""Three connected step-by-step Practice coding tasks for Week 2: SOLID & Dependency Injection."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

PRACTICE_TASKS: list[dict[str, Any]] = [
    {
        "id": "w2_task_1",
        "step_number": 1,
        "title": "Задача 1. Принцип S (SRP): Сервисы расчета тарифа (100 ₸ и 50 ₸)",
        "difficulty": "Шаг 1 · Принцип SRP",
        "max_score": 0.0,
        "story": (
            "Начнем с буквы S (Single Responsibility Principle). Вынесем расчет стоимости проезда из класса терминала "
            "в два маленьких специализированных класса: StandardFareService (обычный тариф 100 ₸) "
            "и StudentFareService (льготный студенческий тариф 50 ₸)."
        ),
        "instructions": [
            "В классе StandardFareService реализуйте метод get_fare(self) -> int, который возвращает число 100.",
            "В классе StudentFareService реализуйте метод get_fare(self) -> int, который возвращает число 50.",
        ],
        "hint": (
            "Подсказка:\n"
            "Внутри StandardFareService.get_fare(self) напишите:\n"
            "return 100\n\n"
            "А внутри StudentFareService.get_fare(self) напишите:\n"
            "return 50"
        ),
        "starter_code": """class StandardFareService:
    \"\"\"Сервис базового тарифа (отвечает только за расчет стандартной цены).\"\"\"

    def get_fare(self) -> int:
        # Шаг 1: Верните стандартную стоимость проезда 100
        pass


class StudentFareService:
    \"\"\"Сервис студенческого тарифа (отвечает только за льготную цену 50 ₸).\"\"\"

    def get_fare(self) -> int:
        # Шаг 2: Верните студенческую стоимость проезда 50
        pass
""",
        "reference_solution": """class StandardFareService:
    \"\"\"Сервис базового тарифа (отвечает только за расчет стандартной цены).\"\"\"

    def get_fare(self) -> int:
        return 100


class StudentFareService:
    \"\"\"Сервис студенческого тарифа (отвечает только за льготную цену 50 ₸).\"\"\"

    def get_fare(self) -> int:
        return 50
""",
        "test_code": """from solution import StandardFareService, StudentFareService


def test_standard_fare_service_returns_100():
    service = StandardFareService()
    assert service.get_fare() == 100, "StandardFareService.get_fare() должен возвращать 100"


def test_student_fare_service_returns_50():
    service = StudentFareService()
    assert service.get_fare() == 50, "StudentFareService.get_fare() должен возвращать 50"


def test_services_share_same_contract():
    services = [StandardFareService(), StudentFareService()]
    fares = [s.get_fare() for s in services]
    assert fares == [100, 50]
""",
    },
    {
        "id": "w2_task_2",
        "step_number": 2,
        "title": "Задача 2. Принципы O и L (OCP & LSP): BluetoothPayment без if/elif",
        "difficulty": "Шаг 2 · OCP и LSP",
        "max_score": 0.0,
        "story": (
            "Теперь применим принципы Open/Closed (OCP) и Liskov Substitution (LSP). "
            "У нас уже есть класс оплаты картой CardPayment с методом pay(amount). "
            "Добавим новый класс бесконтактной оплаты BluetoothPayment с точно таким же контрактом pay(amount), "
            "не переписывая существующий код и не используя цепочки if/elif!"
        ),
        "instructions": [
            'Класс CardPayment уже готов и в методе pay(self, amount) возвращает f"Card: оплачено {amount} тг".',
            'В классе BluetoothPayment реализуйте метод pay(self, amount: int) -> str, который возвращает строку f"Bluetooth: оплачено {amount} тг".',
        ],
        "hint": (
            "Подсказка:\n"
            "Внутри метода pay(self, amount: int) -> str класса BluetoothPayment напишите:\n"
            'return f"Bluetooth: оплачено {amount} тг"'
        ),
        "starter_code": """class CardPayment:
    \"\"\"Оплата транспортной картой.\"\"\"

    def pay(self, amount: int) -> str:
        return f"Card: оплачено {amount} тг"


class BluetoothPayment:
    \"\"\"Новый способ оплаты по Bluetooth (расширяем систему по принципу OCP).\"\"\"

    def pay(self, amount: int) -> str:
        # Реализуйте контракт pay(amount) и верните строку вида "Bluetooth: оплачено 50 тг"
        pass
""",
        "reference_solution": """class CardPayment:
    \"\"\"Оплата транспортной картой.\"\"\"

    def pay(self, amount: int) -> str:
        return f"Card: оплачено {amount} тг"


class BluetoothPayment:
    \"\"\"Новый способ оплаты по Bluetooth (расширяем систему по принципу OCP).\"\"\"

    def pay(self, amount: int) -> str:
        return f"Bluetooth: оплачено {amount} тг"
""",
        "test_code": """from solution import BluetoothPayment, CardPayment


def test_card_payment_contract():
    card = CardPayment()
    assert card.pay(100) == "Card: оплачено 100 тг"


def test_bluetooth_payment_contract():
    bt = BluetoothPayment()
    assert bt.pay(50) == "Bluetooth: оплачено 50 тг", "BluetoothPayment.pay(50) должен вернуть 'Bluetooth: оплачено 50 тг'"
    assert bt.pay(100) == "Bluetooth: оплачено 100 тг"


def test_lsp_polymorphic_substitution():
    methods = [CardPayment(), BluetoothPayment()]
    results = [m.pay(50) for m in methods]
    assert results == ["Card: оплачено 50 тг", "Bluetooth: оплачено 50 тг"]
""",
    },
    {
        "id": "w2_task_3",
        "step_number": 3,
        "title": "Задача 3. Принцип D (DIP & DI): Сборка TerminalValidator через __init__",
        "difficulty": "Шаг 3 · Dependency Injection",
        "max_score": 0.0,
        "story": (
            "Финальный шаг! Соберем модульный терминал TerminalValidator по принципу инверсии зависимостей (DIP) "
            "с внедрением зависимостей через конструктор (Constructor Dependency Injection). "
            "Терминал принимает готовые объекты fare_service и payment_method снаружи в __init__ и использует их в process_passenger()."
        ),
        "instructions": [
            "В конструкторе __init__(self, fare_service, payment_method) сохраните переданные объекты в self.fare_service и self.payment_method.",
            "В методе process_passenger(self) -> str получите цену поездки через amount = self.fare_service.get_fare() и верните результат вызова self.payment_method.pay(amount).",
        ],
        "hint": (
            "Подсказка:\n"
            "В __init__:\n"
            "self.fare_service = fare_service\n"
            "self.payment_method = payment_method\n\n"
            "В process_passenger(self):\n"
            "amount = self.fare_service.get_fare()\n"
            "return self.payment_method.pay(amount)"
        ),
        "starter_code": """class StandardFareService:
    def get_fare(self) -> int:
        return 100


class StudentFareService:
    def get_fare(self) -> int:
        return 50


class CardPayment:
    def pay(self, amount: int) -> str:
        return f"Card: оплачено {amount} тг"


class BluetoothPayment:
    def pay(self, amount: int) -> str:
        return f"Bluetooth: оплачено {amount} тг"


class TerminalValidator:
    def __init__(self, fare_service, payment_method):
        # Шаг 1: Сохраните зависимости в self.fare_service и self.payment_method
        pass

    def process_passenger(self) -> str:
        # Шаг 2: Получите тариф через self.fare_service.get_fare()
        # и верните результат self.payment_method.pay(amount)
        pass
""",
        "reference_solution": """class StandardFareService:
    def get_fare(self) -> int:
        return 100


class StudentFareService:
    def get_fare(self) -> int:
        return 50


class CardPayment:
    def pay(self, amount: int) -> str:
        return f"Card: оплачено {amount} тг"


class BluetoothPayment:
    def pay(self, amount: int) -> str:
        return f"Bluetooth: оплачено {amount} тг"


class TerminalValidator:
    def __init__(self, fare_service, payment_method):
        self.fare_service = fare_service
        self.payment_method = payment_method

    def process_passenger(self) -> str:
        amount = self.fare_service.get_fare()
        return self.payment_method.pay(amount)
""",
        "test_code": """from solution import (
    BluetoothPayment,
    CardPayment,
    StandardFareService,
    StudentFareService,
    TerminalValidator,
)


def test_di_standard_card_combination():
    terminal = TerminalValidator(StandardFareService(), CardPayment())
    assert terminal.fare_service is not None
    assert terminal.payment_method is not None
    assert terminal.process_passenger() == "Card: оплачено 100 тг"


def test_di_student_bluetooth_combination():
    terminal = TerminalValidator(StudentFareService(), BluetoothPayment())
    assert terminal.process_passenger() == "Bluetooth: оплачено 50 тг"


def test_di_custom_mock_injection():
    class FreePromoFare:
        def get_fare(self) -> int:
            return 0

    class MockQRPayment:
        def pay(self, amount: int) -> str:
            return f"QR-Test: {amount}"

    terminal = TerminalValidator(FreePromoFare(), MockQRPayment())
    assert terminal.process_passenger() == "QR-Test: 0"
""",
    },
]


def get_practice_task(task_id: str) -> dict[str, Any] | None:
    """Return a Week 2 practice task definition by its ID."""
    for task in PRACTICE_TASKS:
        if task["id"] == task_id:
            return task
    return None
