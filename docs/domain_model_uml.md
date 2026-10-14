# UML-модель предметной области Avtobys и схема базы данных

## 1. Контекст предметной области

В качестве сквозной прикладной темы курса ООП выбрана транспортная система **Avtobys** (электронное билетирование, валидаторы в автобусах, учет баланса пассажиров и маршрутов). Эта предметная область интуитивно понятна студентам и идеально иллюстрирует фундаментальные принципы ООП: инкапсуляцию, полиморфизм валидаторов, наследование тарифов и композицию сущностей.

---

## 2. Диаграмма классов (UML Class Diagram)

Вводная диаграмма классов демонстрирует взаимодействие пассажира (`Passenger`) и бортового валидатора (`Validator`):

```mermaid
classDiagram
    class Passenger {
        +int id
        +str full_name
        +str card_id
        +float balance
        +top_up(amount: float) None
        +has_sufficient_balance(fare: float) bool
        +deduct_fare(fare: float) bool
    }

    class Validator {
        +str validator_id
        +str bus_id
        +str route_number
        +float standard_fare
        +validate_ticket(passenger: Passenger) bool
    }

    class ValidationResult {
        +bool is_successful
        +str message
        +float remaining_balance
        +datetime timestamp
    }

    Validator ..> Passenger : проверяет баланс и списывает оплату
    Validator ..> ValidationResult : возвращает статус валидации
```

### Описание сущностей:
- `Passenger`: инкапсулирует данные о балансе транспортной карты пассажира. Предоставляет методы безопасного пополнения и списания средств без прямого неконтролируемого изменения баланса.
- `Validator`: отвечает за логику проверки билета на конкретном маршруте автобуса. Проверяет наличие средств и подтверждает проезд.
- `ValidationResult`: легковесный объект-значение (Value Object), инкапсулирующий результат операции валидации.

---

## 3. Схема базы данных (Entity-Relationship Diagram)

Схема хранения данных мини-LMS в SQLite (`data/web_oop.db`):

```mermaid
erDiagram
    STUDENT ||--o{ TOPIC_PROGRESS : "has"
    STUDENT ||--o{ SUBMISSION : "submits"

    STUDENT {
        int id PK "Автоинкрементный идентификатор"
        string username UK "Уникальный логин студента"
        string full_name "Полное имя (ФИО)"
        datetime created_at "Дата и время регистрации"
    }

    TOPIC_PROGRESS {
        int id PK "Идентификатор записи прогресса"
        int student_id FK "Ссылка на студента"
        string topic_id "Идентификатор учебной темы (напр. week1_encapsulation)"
        boolean is_completed "Флаг завершения темы"
        float score "Набранный балл"
        datetime updated_at "Дата последнего обновления"
    }

    SUBMISSION {
        int id PK "Идентификатор попытки"
        int student_id FK "Ссылка на студента"
        string task_id "Идентификатор задания (напр. w1_task1_passenger)"
        text code "Исходный код решения студента"
        string status "Статус (PASSED, FAILED, TIMEOUT, SECURITY_VIOLATION)"
        text test_output "Лог вывода pytest или AST-ошибки"
        datetime created_at "Время отправки решения"
    }
```

### Отношения и ограничения:
- `STUDENT -> TOPIC_PROGRESS`: отношение «один-ко-многим». Удаление студента каскадно удаляет связанные записи прогресса (`cascade="all, delete-orphan"`).
- `STUDENT -> SUBMISSION`: отношение «один-ко-многим». Фиксирует полную историю попыток сдачи лабораторных работ и тестов.
