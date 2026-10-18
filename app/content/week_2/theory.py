"""Beginner-friendly Theory content and code walkthrough for Week 2: SOLID & Dependency Injection."""
# ruff: noqa: E501

from __future__ import annotations

WEEK2_OVERVIEW = {
    "week_number": 2,
    "badge": "Неделя 2 · SOLID и DI",
    "title": "Принципы SOLID и Dependency Injection: собираем код как LEGO",
    "subtitle": "Пошаговый модуль для начинающих по материалам Лекций 4–5 и Лабораторных 4–5 на примере терминала Avtobys",
    "hero_image": "/static/images/week2_hero.jpg",
    "estimated_time": "Ориентир: 60 + 60 + 60 мин",
    "max_score": 20.0,
    "pass_threshold": 12.0,
    "description": (
        "На первой неделе мы защитили данные внутри одной карты SmartCard. Теперь разберем, как соединять несколько классов так, "
        "чтобы программа не превратилась в хрупкий «Класс-Монстр». На сквозном примере автобусного терминала (обычный тариф 100 ₸, "
        "студенческий StudentFareService = 50 ₸ и оплата через BluetoothPayment) мы изучим 5 принципов SOLID и внедрение зависимостей (DI). "
        "Тренажер в Практике не отнимает баллы и снабжен готовыми решениями, а все 20 баллов начисляются в финальном тесте из 10 вопросов!"
    ),
    "roadmap": [
        {
            "step": "01",
            "tab": "theory",
            "title": "Теория: 5 букв SOLID и DI",
            "desc": "Разберем с нуля метрики Cohesion/Coupling, принципы S, O, L, I, D и передачу компонентов через конструктор __init__ (ориентир ~60 мин).",
            "badge": "4 наглядных шага",
        },
        {
            "step": "02",
            "tab": "practice",
            "title": "Практика (Тренажер · 0 баллов штрафа)",
            "desc": "Построчный разбор TerminalValidator + 3 упражнения (StudentFareService 100/50 ₸, BluetoothPayment и сборка через DI) с кнопкой готового решения (~60 мин).",
            "badge": "Свободная песочница",
        },
        {
            "step": "03",
            "tab": "quiz",
            "title": "Итоговое Тестирование Недели 2",
            "desc": "Финальная самопроверка понимания SOLID и DI: 10 вопросов по 2.0 балла каждый (~60 мин). Оценка хранится независимо от Недели 1!",
            "badge": "20 баллов (Зачет от 12 б.)",
        },
    ],
}

THEORY_SECTIONS = [
    {
        "id": "w2_step_1_srp",
        "step_badge": "Шаг 1 из 4 · Буква S + Cohesion & Coupling",
        "title": "Принцип единственной ответственности (SRP): почему «Класс-Монстр» разваливается?",
        "image": "/static/images/solid_modular.jpg",
        "image_caption": "Слева — перегруженный искрящийся монолит God Object; справа — чистые независимые модули с высокой сфокусированностью (High Cohesion)",
        "lead": (
            "Представьте, что один человек в автобусе одновременно крутит руль, чинит двигатель на ходу, "
            "проверяет студенческие билеты и печатает бухгалтерские отчеты. Малейшая ошибка — и весь автобус встанет!"
        ),
        "explanation": (
            "В программировании такой перегруженный класс называют антипаттерном «Божественный объект» (God Object или SpaghettiValidator из Лекции 4).\n"
            "• Буква S (Single Responsibility Principle — Принцип единственной ответственности) гласит: у каждого класса должна быть только ОДНА зона ответственности (одна причина для изменения).\n"
            "• В хорошей архитектуре мы стремимся к двум главным метрикам качества из Лекции 4:\n"
            "  1) High Cohesion (Высокое зацепление) — внутри класса собрано только то, что относится к одной четкой задаче (например, StudentFareService считает только цену 50 ₸).\n"
            "  2) Low Coupling (Слабая связанность) — классы общаются через простые вызовы и почти не зависят от внутренней переделки соседей."
        ),
        "anatomy_cards": [
            {
                "term": "God Object (Божественный объект)",
                "analogy": "Швейцарский нож весом в 50 кг",
                "in_python": "class BusValidatorGodObject: # 500 строк всего подряд",
                "meaning": "Антипаттерн: один гигантский класс пытается сам читать чип, считать тарифы, писать SQL и мигать экраном.",
            },
            {
                "term": "SRP (Single Responsibility)",
                "analogy": "Один мастер — одно дело",
                "in_python": "class StudentFareService: def get_fare(self): return 50",
                "meaning": "Каждый класс отвечает только за свою задачу: один считает тариф (100 ₸ / 50 ₸), другой проводит оплату.",
            },
            {
                "term": "High Cohesion (Высокое зацепление)",
                "analogy": "Сфокусированность внутри модуля",
                "in_python": "# Все методы класса работают на одну цель",
                "meaning": "Класс не распыляется на посторонние дела — его легко читать и понимать с первого взгляда.",
            },
            {
                "term": "Low Coupling (Слабая связанность)",
                "analogy": "Сменные блоки на разъемах",
                "in_python": "fare = self.fare_service.get_fare()",
                "meaning": "Если изменится скидка студента с 50 ₸ на 40 ₸, код самого терминала переписывать не придется!",
            },
        ],
        "bad_code_title": "❌ Плохо: нарушение SRP (антипаттерн God Object — всё свалено в одну кучу)",
        "bad_code": """class BusValidatorGodObject:
    def process_everything(self, card_type: str, payment_type: str):
        # 1. Сам считает тарифы (логика цен)
        fare = 50 if card_type == "student" else 100
        # 2. Сам разбирает способы оплаты
        if payment_type == "card":
            print(f"Списано {fare} тг с карты")
        # 3. Сам лезет в базу данных SQL и мигает лампочкой
        print("INSERT INTO trips VALUES (...)")
        print("BEEP! Зеленый свет")""",
        "good_code_title": "✅ Хорошо: соблюдение SRP (расчет тарифа 100 ₸ / 50 ₸ вынесен в отдельные классы)",
        "good_code": """class StandardFareService:
    \"\"\"Отвечает ТОЛЬКО за базовый тариф (100 ₸).\"\"\"
    def get_fare(self) -> int:
        return 100


class StudentFareService:
    \"\"\"Отвечает ТОЛЬКО за льготный студенческий тариф (50 ₸).\"\"\"
    def get_fare(self) -> int:
        return 50""",
        "takeaway": (
            "Запомните букву S (SRP): не лепите всё в один класс-монстр! Выносите расчет тарифа (100 ₸ / 50 ₸) "
            "и способы оплаты в маленькие понятные классы с высокой сфокусированностью (High Cohesion)."
        ),
    },
    {
        "id": "w2_step_2_ocp",
        "step_badge": "Шаг 2 из 4 · Буква O (Open/Closed)",
        "title": "Принцип открытости/закрытости (OCP): как добавить Bluetooth-оплату без 100 строк if/elif?",
        "lead": (
            "Сначала в автобусах Алматы платили только картой. Потом добавили Kaspi QR. "
            "А завтра попросят подключить оплату по Bluetooth (BluetoothPayment) и Apple Pay!"
        ),
        "explanation": (
            "Если внутри терминала написать длинную цепочку условий if type == 'card': ... elif type == 'qr': ..., "
            "то при добавлении каждого нового способа оплаты вам придется снова и снова вскрывать и переписывать уже работающий класс терминала, рискуя сломать старую оплату картой.\n"
            "• Буква O (Open/Closed Principle — Принцип открытости/закрытости) решает эту проблему:\n"
            "  Программный модуль должен быть ОТКРЫТ для расширения (можно легко добавить новый способ оплаты), "
            "но ЗАКРЫТ для изменения (код самого терминала при этом переписывать не нужно!).\n"
            "• Как это сделать на практике? Мы договариваемся об общем контракте — методе pay(amount). "
            "И для каждого нового способа оплаты просто создаем новый класс (CardPayment, KaspiQRPayment, BluetoothPayment)."
        ),
        "anatomy_cards": [
            {
                "term": "Ловушка if / elif",
                "analogy": "Вскрывать корпус терминала паяльником",
                "in_python": 'if mode == "card": ... elif mode == "bluetooth": ...',
                "meaning": "Каждый новый способ оплаты заставляет редактировать старый проверенный код.",
            },
            {
                "term": "OCP (Open/Closed Principle)",
                "analogy": "USB-порт для новых устройств",
                "in_python": "class BluetoothPayment:\n    def pay(self, amount: int) -> str:",
                "meaning": "Хотите добавить Bluetooth-оплату? Просто создайте новый класс с методом pay(amount), не трогая старый код!",
            },
        ],
        "bad_code_title": "❌ Плохо: нарушение OCP (каждый новый способ оплаты заставляет переписывать метод)",
        "bad_code": """class FragilePaymentProcessor:
    def process(self, payment_type: str, amount: int) -> str:
        # При добавлении Bluetooth или ApplePay приходится ломать этот метод!
        if payment_type == "card":
            return f"Оплата картой: {amount} тг"
        elif payment_type == "qr":
            return f"Оплата Kaspi QR: {amount} тг"
        elif payment_type == "bluetooth":
            return f"Оплата Bluetooth: {amount} тг"
        return "Неизвестный способ оплаты\"""",
        "good_code_title": "✅ Хорошо: соблюдение OCP (новый класс BluetoothPayment добавляется без правки старых)",
        "good_code": """class CardPayment:
    def pay(self, amount: int) -> str:
        return f"Card: списано {amount} тг"


class BluetoothPayment:
    # Новый способ оплаты добавлен как отдельный класс с тем же методом pay(amount)!
    def pay(self, amount: int) -> str:
        return f"Bluetooth: списано {amount} тг"


# Терминалу всё равно, КАКОЙ именно объект оплаты ему передали — главное, что есть метод .pay(amount)""",
        "takeaway": (
            "Запомните букву O (OCP): вместо бесконечных веток if/elif выделяйте общий метод-контракт (например, pay(amount)) "
            "и добавляйте новые функции (BluetoothPayment) как отдельные классы."
        ),
    },
    {
        "id": "w2_step_3_lsp_isp",
        "step_badge": "Шаг 3 из 4 · Буквы L и I (Liskov & Interface Segregation)",
        "title": "Честные наследники (LSP) и компактные интерфейсы без лишних кнопок (ISP)",
        "lead": (
            "В середине слова SOLID стоят две буквы про честные договоренности между классами: "
            "L (Принцип подстановки Барбары Лисков) и I (Принцип разделения интерфейса)."
        ),
        "explanation": (
            "1. Буква L — Liskov Substitution Principle (Принцип подстановки Лисков):\n"
            "Дочерний (или сменный) класс должен ЧЕСТНО выполнять обещания базового контракта, не устраивая внезапных аварий. "
            "В Лабораторной №5 показан классический пример нарушения LSP: программист унаследовал бесплатный проездной волонтера "
            "FreeVolunteerPass от карты, но в методе списания написал raise NotImplementedError('У волонтеров нельзя списывать деньги!'). "
            "Когда терминал вызвал этот метод, вся система рухнула! Чтобы соблюсти LSP, льготный или бесплатный тариф должен спокойно возвращать успешный результат (0 ₸ или 50 ₸) без взрыва программы.\n\n"
            "2. Буква I — Interface Segregation Principle (Принцип разделения интерфейса):\n"
            "Не заставляйте класс реализовывать методы, которыми он не пользуется! Если создать один «толстый» интерфейс "
            "ITransitDevice с методом print_paper_receipt() (печать бумажного чека), то маленькому настенному валидатору без принтера "
            "придется писать пустую заглушку pass. Лучше разделить один раздутый интерфейс на компактные и понятные роли."
        ),
        "anatomy_cards": [
            {
                "term": "LSP (Принцип подстановки Лисков)",
                "analogy": "Замена детали без взрыва системы",
                "in_python": "# Любой сервис тарифа честно возвращает int >= 0",
                "meaning": "Подстановка дочернего или сменного класса (StudentFareService / FreePass) не должна ронять терминал с ошибкой.",
            },
            {
                "term": "ISP (Разделение интерфейса)",
                "analogy": "Не требовать принтер от простого сканера",
                "in_python": "class ICardScanner / class IReceiptPrinter",
                "meaning": "Клиенты не должны зависеть от «толстых» интерфейсов и пустых методов-заглушек, которые им не нужны.",
            },
        ],
        "bad_code_title": "❌ Плохо: нарушение LSP (класс-предатель с ошибкой) и ISP (лишний метод чека)",
        "bad_code": """class FreeVolunteerPass(TransportCard):
    def charge(self, amount: int):
        # ❌ Нарушение LSP: терминал ждал оплату, а получил взрыв программы!
        raise NotImplementedError("У волонтеров нельзя списывать деньги!")


class CompactBusValidator(ITransitDevice):
    def print_paper_receipt(self):
        # ❌ Нарушение ISP: у валидатора в автобусе вообще нет бумажного принтера!
        pass""",
        "good_code_title": "✅ Хорошо: соблюдение LSP и ISP (честный контракт без неожиданных исключений)",
        "good_code": """class VolunteerFareService:
    \"\"\"Соблюдает LSP: честно выполняет контракт get_fare(), возвращая 0 ₸ без аварий.\"\"\"
    def get_fare(self) -> int:
        return 0


class StudentFareService:
    \"\"\"Соблюдает LSP: честно возвращает льготный тариф 50 ₸.\"\"\"
    def get_fare(self) -> int:
        return 50""",
        "takeaway": (
            "Буква L (LSP): сменный класс должен работать везде, где ждут общий контракт, без неожиданных ошибок NotImplementedError. "
            "Буква I (ISP): делайте интерфейсы маленькими и не навязывайте классам лишние методы вроде печати бумажных чеков."
        ),
    },
    {
        "id": "w2_step_4_dip_di",
        "step_badge": "Шаг 4 из 4 · Буква D и Dependency Injection",
        "title": "Инверсия зависимостей (DIP) и внедрение через __init__ (Dependency Injection)",
        "image": "/static/images/di_ports.jpg",
        "image_caption": "Dependency Injection: терминал не припаивает внутри себя один тариф или БД, а принимает сменные модули через разъемы в __init__",
        "lead": (
            "Финальная буква D в слове SOLID — Dependency Inversion Principle (Принцип инверсии зависимостей), "
            "и его главный практический прием — Dependency Injection (Внедрение зависимостей)."
        ),
        "explanation": (
            "Представьте, что батарейку намертво припаяли внутри пульта. Когда она сядет или вы захотите поставить аккумулятор, придется ломать весь пульт!\n"
            "• То же самое происходит в коде, когда программист внутри конструктора жестко пишет:\n"
            "  def __init__(self): self.db = PostgresDatabase(); self.fare = StandardFareService()\n"
            "  Такой класс намертво привязан к конкретной базе данных и одному тарифу. Его невозможно легко протестировать на ноутбуке без сервера PostgreSQL.\n"
            "• Буква D (DIP) говорит: бизнес-логика верхнего уровня (наш терминал TerminalValidator) не должна зависеть от конкретных деталей нижнего уровня — оба должны опираться на общие контракты (абстракции).\n"
            "• Как это реализовать в Python? С помощью паттерна Constructor Dependency Injection (DI — Внедрение зависимостей через конструктор)!\n"
            "  Вместо того чтобы создавать объекты внутри себя, терминал принимает готовые компоненты СНАРУЖИ как аргументы __init__(self, fare_service, payment_method)."
        ),
        "anatomy_cards": [
            {
                "term": "Жесткая привязка (Нарушение DIP)",
                "analogy": "Припаянная намертво деталь",
                "in_python": "def __init__(self):\n    self.db = PostgresDatabase()",
                "meaning": "Терминал сам создает конкретный класс внутри себя — заменить его на тестовый невозможно.",
            },
            {
                "term": "Constructor Dependency Injection (DI)",
                "analogy": "Вставить сменный картридж снаружи",
                "in_python": "def __init__(self, fare_service, payment_method):",
                "meaning": "Зависимости передаются снаружи при создании объекта: TerminalValidator(StudentFareService(), BluetoothPayment()).",
            },
        ],
        "bad_code_title": "❌ Плохо: жесткая привязка внутри __init__ (нарушение DIP — нельзя сменить тариф или способ оплаты)",
        "bad_code": """class RigidTerminalValidator:
    def __init__(self):
        # ❌ Намертво прибили обычный тариф 100 ₸ и оплату картой внутри конструктора!
        self.fare_service = StandardFareService()
        self.payment_method = CardPayment()
        self.db = PostgresDatabase()  # Без сервера БД код даже не запустится!""",
        "good_code_title": "✅ Хорошо: Dependency Injection через конструктор __init__ (собираем любую комбинацию!)",
        "good_code": """class TerminalValidator:
    # ✅ Принимаем любые подходящие компоненты снаружи через __init__ (Constructor DI):
    def __init__(self, fare_service, payment_method):
        self.fare_service = fare_service
        self.payment_method = payment_method

    def process_passenger(self) -> str:
        amount = self.fare_service.get_fare()
        return self.payment_method.pay(amount)


# Теперь мы собираем терминал как конструктор LEGO без изменения его кода:
student_bt_terminal = TerminalValidator(StudentFareService(), BluetoothPayment())
print(student_bt_terminal.process_passenger())  # Bluetooth: списано 50 тг""",
        "takeaway": (
            "Поздравляем! Вы разобрали все 5 букв SOLID и паттерн Dependency Injection. "
            "Теперь загляните в «Практику» (тренажер с готовыми ответами без потери баллов) и заберите свои 20 баллов в «Тестировании»!"
        ),
    },
]

WALKTHROUGH_EXAMPLE = {
    "title": "Разбор перед практикой: модульный терминал TerminalValidator (SOLID + DI в действии)",
    "subtitle": "Посмотрите, как сервис тарифа (100 ₸ / 50 ₸) и способ оплаты (Card / Bluetooth) подключаются к терминалу через __init__",
    "code": """class StandardFareService:
    def get_fare(self) -> int:
        return 100  # Обычный тариф: 100 ₸


class StudentFareService:
    def get_fare(self) -> int:
        return 50   # Студенческий тариф: 50 ₸


class CardPayment:
    def pay(self, amount: int) -> str:
        return f"Card: оплачено {amount} тг"


class BluetoothPayment:
    def pay(self, amount: int) -> str:
        return f"Bluetooth: оплачено {amount} тг"


class TerminalValidator:
    # Dependency Injection: получаем зависимости снаружи через конструктор
    def __init__(self, fare_service, payment_method):
        self.fare_service = fare_service
        self.payment_method = payment_method

    def process_passenger(self) -> str:
        amount = self.fare_service.get_fare()
        return self.payment_method.pay(amount)
""",
    "steps": [
        {
            "line_ref": "Строки 1–8 (Принцип S — SRP)",
            "title": "1. Отдельные сервисы расчета тарифа (100 ₸ и 50 ₸)",
            "text": "Классы StandardFareService (100 ₸) и StudentFareService (50 ₸) отвечают только за цену поездки. У них общий метод get_fare() -> int.",
        },
        {
            "line_ref": "Строки 11–18 (Принципы O и L — OCP & LSP)",
            "title": "2. Сменные способы оплаты без цепочек if/elif",
            "text": "CardPayment и BluetoothPayment реализуют один и тот же метод pay(amount) -> str. Чтобы добавить новый способ оплаты, мы просто создаем новый класс!",
        },
        {
            "line_ref": "Строки 21–25 (Паттерн Dependency Injection)",
            "title": "3. Внедрение зависимостей через конструктор __init__",
            "text": "TerminalValidator не создает тариф или оплату внутри себя. Он принимает готовые объекты fare_service и payment_method как параметры __init__.",
        },
        {
            "line_ref": "Строки 27–29 (Принцип D — DIP в методе process_passenger)",
            "title": "4. Работа через контракты без привязки к деталям",
            "text": "Метод process_passenger() узнает цену через self.fare_service.get_fare() и передает её в self.payment_method.pay(amount), не зная конкретных классов!",
        },
    ],
}
