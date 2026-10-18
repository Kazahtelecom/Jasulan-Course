"""Three connected step-by-step Practice coding tasks for Week 1."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

PRACTICE_TASKS: list[dict[str, Any]] = [
    {
        "id": "task_1",
        "step_number": 1,
        "title": "Задача 1. Чертеж карты: __init__, self и метод info()",
        "difficulty": "Легкий старт",
        "max_score": 0.0,
        "story": (
            "Начнем с самого простого шага. Нам нужно создать класс SmartCard (чертеж транспортной карты), "
            "который запоминает имя владельца и начальный баланс, а также умеет красиво выводить информацию о себе."
        ),
        "instructions": [
            "В методе __init__(self, owner, balance) сохраните имя владельца в атрибут self.owner, а баланс — в self.balance.",
            'В методе info(self) верните строку формата: f"Карта {self.owner}: {self.balance} тг".',
        ],
        "hint": (
            'Подсказка: внутри __init__ напишите:\n'
            'self.owner = owner\n'
            'self.balance = balance\n\n'
            'А внутри info(self) напишите:\n'
            'return f"Карта {self.owner}: {self.balance} тг"'
        ),
        "starter_code": """class SmartCard:
    def __init__(self, owner: str, balance: int):
        # Шаг 1: Сохраните owner в self.owner и balance в self.balance
        pass

    def info(self) -> str:
        # Шаг 2: Верните строку вида "Карта Алихан: 500 тг"
        pass
""",
        "reference_solution": """class SmartCard:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self.balance = balance

    def info(self) -> str:
        return f"Карта {self.owner}: {self.balance} тг"
""",
        "test_code": """from solution import SmartCard


def test_create_smart_card_attributes():
    card = SmartCard("Алихан", 500)
    assert card.owner == "Алихан", "Атрибут self.owner должен хранить имя владельца"
    assert card.balance == 500, "Атрибут self.balance должен хранить баланс карты"


def test_two_independent_cards():
    card1 = SmartCard("Алихан", 500)
    card2 = SmartCard("Дина", 1200)
    assert card1.owner == "Алихан" and card1.balance == 500
    assert card2.owner == "Дина" and card2.balance == 1200


def test_info_method_output():
    card = SmartCard("Санжар", 850)
    assert card.info() == "Карта Санжар: 850 тг"
""",
    },
    {
        "id": "task_2",
        "step_number": 2,
        "title": "Задача 2. Инкапсуляция баланса: _balance, @property и top_up()",
        "difficulty": "Шаг 2 · Защита данных",
        "max_score": 0.0,
        "story": (
            "Отлично! Теперь защитим баланс нашей карты от случайного изменения снаружи. "
            "Спрячем деньги в приватное поле self._balance, откроем безопасное чтение через @property "
            "и добавим метод пополнения top_up(amount), который принимает только положительные суммы."
        ),
        "instructions": [
            "В __init__(self, owner, balance) сохраните владельца в self.owner, а баланс — в приватный атрибут self._balance.",
            "В свойстве @property def balance(self) верните значение self._balance.",
            "В методе top_up(self, amount): если amount > 0, прибавьте amount к self._balance и верните True. Иначе ничего не меняйте и верните False.",
        ],
        "hint": (
            "Подсказка:\n"
            "В методе top_up проверьте условие:\n"
            "if amount > 0:\n"
            "    self._balance += amount\n"
            "    return True\n"
            "return False"
        ),
        "starter_code": """class SmartCard:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        # Шаг 1: Сохраните баланс в приватное поле self._balance
        self._balance = balance

    @property
    def balance(self) -> int:
        # Шаг 2: Верните значение self._balance
        pass

    def top_up(self, amount: int) -> bool:
        # Шаг 3: Если amount > 0, увеличьте self._balance на amount и верните True.
        # Иначе верните False.
        pass

    def info(self) -> str:
        return f"Карта {self.owner}: {self.balance} тг"
""",
        "reference_solution": """class SmartCard:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> int:
        return self._balance

    def top_up(self, amount: int) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False

    def info(self) -> str:
        return f"Карта {self.owner}: {self.balance} тг"
""",
        "test_code": """import pytest
from solution import SmartCard


def test_private_balance_and_property():
    card = SmartCard("Алихан", 500)
    assert hasattr(card, "_balance"), "Баланс должен храниться в приватном поле self._balance"
    assert card.balance == 500, "Свойство card.balance должно возвращать 500"


def test_balance_cannot_be_overwritten_directly():
    card = SmartCard("Алихан", 500)
    with pytest.raises(AttributeError):
        card.balance = -9999


def test_top_up_positive_amount():
    card = SmartCard("Алихан", 500)
    result = card.top_up(300)
    assert result is True, "Метод top_up(300) должен вернуть True"
    assert card.balance == 800, "После пополнения на 300 баланс должен стать 800"


def test_top_up_invalid_amount_rejected():
    card = SmartCard("Алихан", 500)
    assert card.top_up(0) is False, "Пополнение на 0 должно возвращать False"
    assert card.top_up(-200) is False, "Пополнение на отрицательную сумму должно возвращать False"
    assert card.balance == 500, "При неверном пополнении баланс не должен меняться"
""",
    },
    {
        "id": "task_3",
        "step_number": 3,
        "title": "Задача 3. Финал практики: безопасная оплата проезда pay()",
        "difficulty": "Шаг 3 · Полная защита",
        "max_score": 0.0,
        "story": (
            "Финальный штрих! У нашей карты уже есть защищенный баланс и пополнение. "
            "Осталось научить карту оплачивать проезд через метод pay(self, fare) так, "
            "чтобы баланс ни при каких условиях не мог уйти в минус."
        ),
        "instructions": [
            "В методе pay(self, fare) проверьте два условия: стоимость проезда положительна (fare > 0) И на карте хватает денег (self._balance >= fare).",
            "Если оба условия выполнены — вычтите fare из self._balance и верните True.",
            "Если денег не хватает или передан неверный тариф (fare <= 0) — не меняйте баланс и верните False.",
        ],
        "hint": (
            "Подсказка:\n"
            "if fare > 0 and self._balance >= fare:\n"
            "    self._balance -= fare\n"
            "    return True\n"
            "return False"
        ),
        "starter_code": """class SmartCard:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> int:
        return self._balance

    def top_up(self, amount: int) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False

    def pay(self, fare: int) -> bool:
        # Реализуйте безопасное списание стоимости проезда fare:
        # 1. Проверьте, что fare > 0 и self._balance >= fare
        # 2. Если да — уменьшите self._balance на fare и верните True
        # 3. Иначе — ничего не меняйте и верните False
        pass

    def info(self) -> str:
        return f"Карта {self.owner}: {self.balance} тг"
""",
        "reference_solution": """class SmartCard:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> int:
        return self._balance

    def top_up(self, amount: int) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False

    def pay(self, fare: int) -> bool:
        if fare > 0 and self._balance >= fare:
            self._balance -= fare
            return True
        return False

    def info(self) -> str:
        return f"Карта {self.owner}: {self.balance} тг"
""",
        "test_code": """from solution import SmartCard


def test_successful_fare_payment():
    card = SmartCard("Дина", 500)
    assert card.pay(120) is True, "При достаточном балансе pay(120) должен вернуть True"
    assert card.balance == 380, "После оплаты 120 тг с 500 тг должно остаться 380 тг"


def test_insufficient_funds_protection():
    card = SmartCard("Дина", 100)
    assert card.pay(120) is False, "При нехватке средств pay(120) должен вернуть False"
    assert card.balance == 100, "Баланс не должен уменьшаться при отказе в оплате"


def test_negative_or_zero_fare_rejected():
    card = SmartCard("Дина", 500)
    assert card.pay(0) is False, "Нулевой тариф должен отклоняться (False)"
    assert card.pay(-100) is False, "Отрицательный тариф должен отклоняться (False)"
    assert card.balance == 500, "Баланс должен остаться 500 тг"


def test_full_card_lifecycle():
    card = SmartCard("Алихан", 100)
    assert card.pay(120) is False
    assert card.top_up(200) is True
    assert card.balance == 300
    assert card.pay(120) is True
    assert card.info() == "Карта Алихан: 180 тг"
""",
    },
]


def get_practice_task(task_id: str) -> dict[str, Any] | None:
    """Return a practice task definition by its ID."""
    for task in PRACTICE_TASKS:
        if task["id"] == task_id:
            return task
    return None
