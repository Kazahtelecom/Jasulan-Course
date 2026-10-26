"""Beginner-friendly Theory content and code walkthrough for Week 3: GoF Patterns & Clean Architecture."""
# ruff: noqa: E501

from __future__ import annotations

WEEK3_OVERVIEW = {
    "week_number": 3,
    "badge": "Неделя 3 · Паттерны GoF и Clean Arch",
    "title": "Паттерны проектирования GoF и Чистая Архитектура: экосистема Avtobys",
    "subtitle": "Пошаговый модуль по материалам авторских Лекций 6–9 и Лабораторных 6–9 на сквозном домене транспортной системы",
    "hero_image": "/static/images/week3_hero.jpg",
    "estimated_time": "Ориентир: 60 + 60 + 60 мин",
    "max_score": 20.0,
    "pass_threshold": 12.0,
    "description": (
        "На первой неделе мы освоили инкапсуляцию карты SmartCard, на второй — научились соединять классы по принципам SOLID и DI. "
        "Теперь мы завершаем курс и выходим на уровень промышленной архитектуры! Мы изучим ключевые паттерны Банды Четырёх (GoF): "
        "порождающие (Factory Method, Builder), структурные (Adapter, Decorator, Facade) и поведенческие (Strategy, Observer, Chain of Responsibility), "
        "а затем свяжем их воедино четырьмя слоями Чистой Архитектуры (Clean Architecture). "
        "Тренажер свободен от штрафов (0.0 б.) и снабжен готовыми решениями, а итоговые 20 баллов курса начисляются в сбалансированном финальном тесте!"
    ),
    "roadmap": [
        {
            "step": "01",
            "tab": "theory",
            "title": "Теория: 9 паттернов GoF и Чистая Архитектура",
            "desc": "Разберем за 4 шага фабрики, строители, адаптеры, цепочки проверок, наблюдателей и слои Clean Architecture (ориентир ~60 мин).",
            "badge": "4 наглядных шага",
        },
        {
            "step": "02",
            "tab": "practice",
            "title": "Практика (Тренажер · 0 баллов штрафа)",
            "desc": "Построчный разбор Facade/Factory + 3 задачи (ShiftReportBuilder + BankApiAdapter, ValidationHandler + Observer, Clean Arch Use Case) с кнопкой готового решения (~60 мин).",
            "badge": "Свободная песочница",
        },
        {
            "step": "03",
            "tab": "quiz",
            "title": "Итоговое Тестирование Недели 3",
            "desc": "Финальная аттестация по паттернам GoF и Clean Architecture: 10 вопросов по 2.0 балла (всего 20.0 б., зачет от 12.0 б.) с защитой High-Water Mark (~60 мин).",
            "badge": "20 баллов (Зачет от 12 б.)",
        },
    ],
}

THEORY_SECTIONS = [
    {
        "id": "w3_step_1_creational",
        "step_badge": "Шаг 1 из 4 · Порождающие паттерны GoF (Factory Method, Builder)",
        "title": "Порождающие паттерны: убираем хаос создания объектов и строим сложные отчеты",
        "image": "/static/images/week3_hero.jpg",
        "image_caption": "Киберпанк-депо Avtobys: централизованная фабрика выпускает цифровые билеты, а пошаговый Строитель собирает финансовый отчет смены",
        "lead": (
            "Когда код напрямую вызывает конструкторы вроде QrTicket() или NfcTicket() по всей программе через бесконечные if/elif, "
            "любое добавление нового типа билета превращается в кошмар. Порождающие паттерны изолируют процесс создания от использования."
        ),
        "explanation": (
            "По материалам Лекции 6 и Лабораторной 6 мы изучаем два фундаментальных порождающих паттерна:\n"
            "• Factory Method (Фабричный метод) — объявляет абстрактный метод create_ticket() в базовом классе TicketIssuer. Подклассы (QrTicketIssuer, NfcTicketIssuer) сами решают, какой конкретный билет создавать. Код валидатора работает только с абстракцией Ticket!\n"
            "• Builder (Строитель) — решает проблему «Телескопического конструктора» (Telescoping Constructor). Вместо конструктора с 10 аргументами класс ShiftReportBuilder пошагово через Fluent API (.set_shift_info(), .add_qr_revenue()) накапливает данные и проверяет обязательные поля перед созданием неизменяемого DailyShiftReport.\n"
            "• Рефакторинг Singleton — в Лекции 6 показано, почему глобальный Singleton GlobalConfig часто превращается в антипаттерн с неявным состоянием, и почему его заменяют на инъекцию конфигурации AppConfig через DI."
        ),
        "anatomy_cards": [
            {
                "term": "Factory Method (Фабричный метод)",
                "analogy": "Печать билетов в автомате",
                "in_python": "class TicketIssuer(ABC):\n    @abstractmethod\n    def create_ticket(self) -> Ticket: ...",
                "meaning": "Делегирует создание конкретного объекта дочерним классам-фабрикам, избавляя клиентский код от жесткой привязки.",
            },
            {
                "term": "Builder (Строитель)",
                "analogy": "Пошаговая сборка бургера или чека",
                "in_python": "builder.set_shift_info('10A', 'D-1').add_qr_revenue(1500).build()",
                "meaning": "Пошагово конструирует сложный объект, позволяя собирать разные представления одного и того же продукта без гигантских аргументов.",
            },
            {
                "term": "Telescoping Constructor (Антипаттерн)",
                "analogy": "Конструктор с 12 позиционными аргументами",
                "in_python": "DailyShiftReport('10A', 'D-1', 0, 0, 0, None, True, False, 12, ...)",
                "meaning": "Запутанный конструктор, где программист легко путает порядок аргументов одного типа (например, route_id и driver_id).",
            },
            {
                "term": "Fluent Interface (Текучий интерфейс)",
                "analogy": "Цепочка действий без повтора имени переменной",
                "in_python": "def add_qr(self, amt):\n    self._qr += amt\n    return self",
                "meaning": "Каждый метод настройки строителя возвращает self, позволяя вызывать методы по цепочке builder.step1().step2().build().",
            },
        ],
        "bad_code": """# ПЛОХО: Прямое создание и раздутый конструктор
def issue_ticket(ticket_type: str, fare: Decimal) -> Ticket:
    if ticket_type == "qr":
        return QrTicket(fare=fare, hash="...")
    elif ticket_type == "nfc":
        return NfcTicket(fare=fare, card_uid="...")
    raise ValueError("Неизвестный тип")

# Телескопический конструктор: легко перепутать аргументы
report = DailyShiftReport("10A", "D-01", Decimal("45000"), None, 0, True)""",
        "good_code": """# ХОРОШО: Factory Method и пошаговый Builder
class TicketIssuer(ABC):
    @abstractmethod
    def create_ticket(self, fare: Decimal) -> Ticket:
        \"\"\"Фабричный метод создания билета.\"\"\"
        pass


class QrTicketIssuer(TicketIssuer):
    def create_ticket(self, fare: Decimal) -> Ticket:
        return QrTicket(fare=fare, qr_payload=f"QR-{fare}")


# Builder гарантирует валидность перед сборкой
report = (
    ShiftReportBuilder()
    .set_shift_info(route_id="10A", driver_id="D-01")
    .add_qr_revenue(Decimal("45000"))
    .build()
)""",
        "summary": "Используйте Factory Method, когда клиентский код не должен зависеть от конкретных классов создаваемых продуктов, и Builder, когда сборка сложного объекта состоит из нескольких шагов с обязательной валидацией.",
    },
    {
        "id": "w3_step_2_structural",
        "step_badge": "Шаг 2 из 4 · Структурные паттерны GoF (Adapter, Decorator, Facade)",
        "title": "Структурные паттерны: адаптация внешних API, оборачивание функционала и единый фасад",
        "image": "/static/images/gof_patterns.jpg",
        "image_caption": "Схема бортового терминала: Адаптер переводит тенге в тиыны банка, Декораторы замеряют тайминги, а Фасад прячет подсистему за одной кнопкой tap()",
        "lead": (
            "В реальной жизни терминал Avtobys не работает в изоляции. Ему приходится общаться со старыми банковскими шлюзами, "
            "замерять время отклика каждого платежа и скрывать сложность десятка сервисов от экрана водителя."
        ),
        "explanation": (
            "По материалам Лекции 7 и Лабораторной 7 мы изучаем три структурных паттерна:\n"
            "• Adapter (Адаптер) — переводит интерфейс одного класса в интерфейс, ожидаемый клиентом. Внешний LegacyBankClient требует суммы в тиынах (amount_tiyn: int) и номер счёта. Класс BankApiAdapter оборачивает его и предоставляет чистый метод charge(card_id, amount: Decimal), автоматически умножая тенге на 100!\n"
            "• Decorator (Декоратор) — динамически добавляет объекту новые обязанности без правки самого класса. TimingDecorator замеряет длительность транзакции, RetryOnFailureDecorator повторяет сбойные вызовы, оборачивая базовый сервис.\n"
            "• Facade (Фасад) — предоставляет простой высокоуровневый интерфейс к сложной подсистеме. Вместо того чтобы вызывать по очереди валидацию карты, списание тарифа, запись в лог и отправку телеметрии, внешний роутер вызывает один метод TransitTerminalFacade.tap(card_id)."
        ),
        "anatomy_cards": [
            {
                "term": "Adapter (Адаптер / Wrapper)",
                "analogy": "Переходник с евровилки на британскую розетку",
                "in_python": "tiyn = int(amount * 100)\nreturn self.legacy_client.pay(tiyn)",
                "meaning": "Соединяет два несовместимых интерфейса, выполняя преобразование форматов данных и типов параметров.",
            },
            {
                "term": "Decorator (Декоратор)",
                "analogy": "Чехол для телефона с фонариком и подставкой",
                "in_python": "class TimingDecorator:\n    def charge(self, card, amt):\n        # замер времени до и после вызова",
                "meaning": "Оборачивает целевой объект тем же интерфейсом, прозрачно добавляя поведение до и после вызова основного метода.",
            },
            {
                "term": "Facade (Фасад)",
                "analogy": "Кнопка «Старт» на приборной панели автомобиля",
                "in_python": "terminal.tap(card_id) # внутри: проверка + списание + лог",
                "meaning": "Скрывает сложную группу взаимодействующих классов за одним простым и понятным методом.",
            },
            {
                "term": "Adapter vs Facade",
                "analogy": "Переходник кабеля против пульта управления",
                "in_python": "Adapter меняет интерфейс одного; Facade упрощает работу со многими",
                "meaning": "Адаптер делает так, чтобы старый класс подошёл к новому контракту; фасад создает совершенно новый простой вход в систему.",
            },
        ],
        "bad_code": """# ПЛОХО: Клиентский код вручную управляет конвертацией валют и кучей подсистем
tiyn = int(fare_amount * 100) # Программист может забыть умножить на 100!
bank_res = legacy_bank.execute_payment_kzt("PAN-1", "TRANSIT-ACC", tiyn)
if bank_res["auth_code"]:
    audit.log_event("SUCCESS")
    display.show_green_screen()
    gate.open_turnstile()""",
        "good_code": """# ХОРОШО: Адаптер скрывает детали банка, а Фасад объединяет подсистему
class BankApiAdapter:
    def __init__(self, client: LegacyBankClient, transit_acc: str):
        self._client = client
        self._acc = transit_acc

    def charge(self, card_id: str, amount: Decimal) -> str:
        tiyn = int(amount * 100)
        res = self._client.execute_payment_kzt(card_id, self._acc, tiyn)
        return res["auth_code"]


# Клиент вызывает лишь одну команду фасада
facade.tap(card_id="CARD-777", fare=Decimal("100"))""",
        "summary": "Используйте Adapter для интеграции сторонних и устаревших библиотек, Decorator для наложения сквозной функциональности (логи, тайминги, повторы), и Facade для создания дружелюбного API к сложной группе сервисов.",
    },
    {
        "id": "w3_step_3_behavioral",
        "step_badge": "Шаг 3 из 4 · Поведенческие паттерны GoF (Strategy, Observer, Chain of Responsibility)",
        "title": "Поведенческие паттерны: цепочки валидации и событийная реакция диспетчера",
        "image": "/static/images/gof_patterns.jpg",
        "image_caption": "Поведенческие связи: запрос на оплату идет по цепочке обработчиков (Blacklist -> Balance), а Наблюдатель мгновенно рассылает события телеметрии",
        "lead": (
            "Как проверить право на проезд, если правил много (черный список, нехватка баланса, истекший срок) и они постоянно меняются? "
            "И как уведомить диспетчера и аналитику о проезде автобуса, не превращая валидатор в спам-машину?"
        ),
        "explanation": (
            "По материалам Лекции 8 и Лабораторной 8 мы изучаем поведенческие паттерны:\n"
            "• Chain of Responsibility (Цепочка обязанностей) — организует последовательную обработку запроса PaymentRequest цепочкой независимых звеньев ValidationHandler. BlacklistCheckHandler проверяет карту на блокировку: если карта заблокирована, цепочка немедленно прерывается с ошибкой. Иначе запрос передается в BalanceCheckHandler. Добавить проверку тарифа выходного дня можно в одно действие, не меняя существующие классы!\n"
            "• Observer (Наблюдатель / Publish-Subscribe) — определяет зависимость «один-ко-многим». Класс TransitTelemetrySubject хранит список подписчиков. При валидации билета он вызывает self.notify(event), и все зарегистрированные слушатели (MetricsCollector, DispatcherDashboard) синхронно получают обновление.\n"
            "• Strategy (Стратегия) vs State (Состояние) — Стратегия выбирает алгоритм снаружи (например, алгоритм расчета динамического тарифа), тогда как Состояние меняется изнутри самого объекта при переходах жизненного цикла (Смена открыта -> В пути -> Смена закрыта)."
        ),
        "anatomy_cards": [
            {
                "term": "Chain of Responsibility (Цепочка обязанностей)",
                "analogy": "Прохождение таможни и паспортного контроля",
                "in_python": "handler.set_next(next_handler).handle(request)",
                "meaning": "Передает запрос по цепочке потенциальных обработчиков, пока один из них не обработает его или не отклонит с причиной.",
            },
            {
                "term": "Observer (Наблюдатель)",
                "analogy": "Подписка на Telegram-канал новостей маршрута",
                "in_python": "subject.attach(observer)\nsubject.notify('RIDE_VALIDATED')",
                "meaning": "Позволяет объектам-подписчикам динамически реагировать на события, происходящие в издателе (Subject).",
            },
            {
                "term": "Strategy (Стратегия)",
                "analogy": "Выбор маршрута в навигаторе (быстрый, короткий, без пробок)",
                "in_python": "fare_calculator.set_strategy(NightFareStrategy())",
                "meaning": "Инкапсулирует семейство взаимозаменяемых алгоритмов и позволяет переключать их во время выполнения программы.",
            },
            {
                "term": "Short-Circuiting (Прерывание цепочки)",
                "analogy": "Шлагбаум опускается при первой же неисправности",
                "in_python": "if failed:\n    return ValidationResult(False, reason)",
                "meaning": "Если один обработчик в цепочке забраковал запрос, последующие тяжелые проверки (например, обращение к БД) не выполняются.",
            },
        ],
        "bad_code": """# ПЛОХО: Один монструозный метод с вложенными if и ручным вызовом всех аналитик
def validate_and_notify(card, fare):
    if card.id in BLACKLIST:
        return "BLOCKED"
    if card.balance < fare:
        return "NO_MONEY"
    if not card.is_active:
        return "EXPIRED"
    card.balance -= fare
    # Жесткая зависимость от конкретных систем аналитики!
    stats_server.send(...)
    dispatcher_cloud.send(...)""",
        "good_code": """# ХОРОШО: Цепочка обработчиков и независимый Наблюдатель
chain = BlacklistCheckHandler()
chain.set_next(BalanceCheckHandler())

result = chain.handle(payment_request)
if result.is_approved:
    telemetry.notify("PASSENGER_BOARDED")""",
        "summary": "Используйте Chain of Responsibility для построения многоступенчатых фильтров и проверок бизнес-правил, а Observer — для слабосвязанной отправки событий множеству заинтересованных служб.",
    },
    {
        "id": "w3_step_4_clean_arch",
        "step_badge": "Шаг 4 из 4 · Чистая Архитектура (Clean Architecture & The Dependency Rule)",
        "title": "Чистая Архитектура: концентрические слои и Правило Зависимостей в домене Avtobys",
        "image": "/static/images/clean_arch_layers.jpg",
        "image_caption": "Круги Чистой Архитектуры Роберта Мартина: зависимости направлены строго внутрь, от внешней инфраструктуры к ядру Entities и Use Cases",
        "lead": (
            "Фреймворки устаревают, базы данных меняются с SQLite на PostgreSQL, а протоколы переходят с REST на gRPC. "
            "Чистая Архитектура (Clean Architecture Роберта Мартина) гарантирует, что бизнес-логика транспорта проживет десятки лет без изменений."
        ),
        "explanation": (
            "По материалам Лекции 9 и Лабораторной 9 мы изучаем 4 концентрических слоя Чистой Архитектуры:\n"
            "1. Entities (Сущности) — центр вселенной. Бизнес-модели ядра: Value Object Money(amount, currency='KZT') и Entity TransitCard.charge_fare(). В них нет ни строчки о базах данных, FastAPI или JSON!\n"
            "2. Use Cases (Сценарии использования) — прикладные сценарии системы. ValidateRideUseCase.execute() координирует проверку карты, списание тарифа и вызов шлюза через абстрактные интерфейсы-порты.\n"
            "3. Interface Adapters (Адаптеры интерфейсов) — порты CardRepositoryPort, PaymentGatewayPort и их реализация BankApiAdapter, переводящие структуры Use Case в форматы внешних API.\n"
            "4. Frameworks & Drivers (Инфраструктура) — внешний мир: SQLite, FastAPI роутеры, UI-шаблоны Jinja2.\n"
            "• The Dependency Rule (Правило Зависимостей): стрелки зависимостей направлены СТРОГО СНАРУЖИ ВНУТРЬ. Внутренние слои (Entities, Use Cases) ничего не знают о внешних (FastAPI, SQLite)!\n"
            "• Запахи кода Фаулера: избавляемся от Primitive Obsession с помощью Money, предотвращаем Divergent Change и Shotgun Surgery четким разделением слоев."
        ),
        "anatomy_cards": [
            {
                "term": "The Dependency Rule (Правило зависимостей)",
                "analogy": "Стены средневекового замка: внешние стражники видят замок, но ядро защищено",
                "in_python": "domain <- application <- adapters <- infrastructure",
                "meaning": "Исходный код внутреннего слоя никогда не должен импортировать или упоминать элементы внешнего слоя.",
            },
            {
                "term": "Entities (Сущности бизнес-ядра)",
                "analogy": "Законы физики и базовые правила математики",
                "in_python": "@dataclass\nclass TransitCard:\n    card_id: str\n    balance: Decimal",
                "meaning": "Объекты предметной области, инкапсулирующие наиболее общие и фундаментальные правила бизнеса.",
            },
            {
                "term": "Use Cases (Интеракторы / Сценарии)",
                "analogy": "Регламент действий диспетчера при регистрации рейса",
                "in_python": "class ValidateRideUseCase:\n    def execute(self, req: Request) -> Response: ...",
                "meaning": "Сценарии, определяющие логику конкретного пользовательского процесса и связывающие сущности с портами.",
            },
            {
                "term": "Primitive Obsession (Запах кода Фаулера)",
                "analogy": "Хранение денег простым числом float без указания валюты",
                "in_python": "price = 100.0 # ПЛОХО\nfare = Money(Decimal('100'), 'KZT') # ХОРОШО",
                "meaning": "Антипаттерн использования примитивных типов вместо компактных специализированных объектов предметной области.",
            },
        ],
        "bad_code": """# ПЛОХО: Сущность напрямую зависит от SQLite и фреймворка FastAPI
from fastapi import HTTPException
import sqlite3

class TransitCard:
    def charge_and_save(self, amount: float):
        # Бизнес-модель знает SQL и сетевой фреймворк!
        conn = sqlite3.connect("prod.db")
        conn.execute("UPDATE cards SET balance = balance - ?", (amount,))
        raise HTTPException(status_code=400, detail="SQL Error")""",
        "good_code": """# ХОРОШО: Чистая Архитектура — бизнес-ядро независимо от инфраструктуры
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


class ValidateRideUseCase:
    def __init__(self, card_repo: CardRepositoryPort, payment_gw: PaymentGatewayPort):
        self._repo = card_repo
        self._gw = payment_gw

    def execute(self, req: ValidateRideRequest) -> ValidateRideResponse:
        card = self._repo.get_by_id(req.card_id)
        card.charge_fare(Money(req.fare_amount))
        tx = self._gw.charge(card.card_id, req.fare_amount)
        self._repo.save(card)
        return ValidateRideResponse(True, card.balance, tx)""",
        "summary": "Чистая Архитектура делает вашу систему независимой от фреймворков, баз данных и внешних API. Тестировать Use Cases можно за миллисекунды в оперативной памяти без поднятия базы данных и сети!",
    },
]

WALKTHROUGH_EXAMPLE = {
    "title": "Разбор перед практикой: Фасад терминала с Фабричным Методом (GoF + Clean Arch)",
    "subtitle": "Посмотрите, как фабричный метод TicketIssuer и структурный фасад TransitTerminalFacade организуют оплату",
    "code": """from abc import ABC, abstractmethod
from decimal import Decimal


class Ticket(ABC):
    \"\"\"Абстрактный цифровой билет Avtobys.\"\"\"
    def __init__(self, fare: Decimal):
        self.fare = fare


class QrTicket(Ticket):
    \"\"\"Билет по динамическому QR-коду приложения.\"\"\"
    def __init__(self, fare: Decimal, qr_hash: str):
        super().__init__(fare)
        self.qr_hash = qr_hash


class TicketIssuer(ABC):
    \"\"\"Порождающий паттерн Factory Method (Фабричный метод).\"\"\"
    @abstractmethod
    def create_ticket(self, fare: Decimal) -> Ticket:
        pass


class QrTicketIssuer(TicketIssuer):
    \"\"\"Конкретная фабрика выпуска QR-билетов.\"\"\"
    def create_ticket(self, fare: Decimal) -> Ticket:
        return QrTicket(fare, f"QR-AUTH-{fare}")


class TransitTerminalFacade:
    \"\"\"Структурный паттерн Facade (Фасад терминала).\"\"\"
    def __init__(self, issuer: TicketIssuer):
        self._issuer = issuer

    def tap(self, fare_kzt: Decimal) -> str:
        ticket = self._issuer.create_ticket(fare_kzt)
        return f"OK: Билет выпущен на сумму {ticket.fare} KZT"
""",
    "steps": [
        {
            "line_ref": "Строки 5–18 (Абстракция продукта Ticket)",
            "title": "1. Иерархия продуктов: абстрактный Ticket и конкретный QrTicket",
            "text": "Класс Ticket задает общий контракт для любых видов билетов (QR, NFC, SMS). Конкретный QrTicket расширяет его хэшем авторизации.",
        },
        {
            "line_ref": "Строки 21–30 (Порождающий паттерн Factory Method)",
            "title": "2. Фабрика выпуска билетов TicketIssuer",
            "text": "Абстрактный класс TicketIssuer объявляет фабричный метод create_ticket(). Подкласс QrTicketIssuer сам решает, как именно инстанцировать QrTicket.",
        },
        {
            "line_ref": "Строки 33–36 (Структурный паттерн Facade)",
            "title": "3. Фасад TransitTerminalFacade объединяет зависимости",
            "text": "Терминал получает фабрику билетов через внедрение зависимостей и скрывает детали создания за простым интерфейсом.",
        },
        {
            "line_ref": "Строки 38–41 (Единая точка входа tap)",
            "title": "4. Высокоуровневая операция в одно действие",
            "text": "Метод tap() принимает лишь сумму тарифа Decimal, вызывает фабрику и возвращает подтверждение оплаты в читаемом формате.",
        },
    ],
}
