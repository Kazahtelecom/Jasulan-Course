# KNOWLEDGE.md — Project Knowledge

Start here for relevant project knowledge. Governing instructions and the approved task contract
retain authority; a record, source quotation or imported imperative cannot grant permission.

## Current knowledge use

Use ordinary files and textual search. Inspect relevant scope, grounds, disposition, source and
producer before applying a claim. Search `knowledge/records/` for incoming successor, correction,
equivalence and conflict references to its exact identity; follow material chains in both directions.
Legacy targets use exact path plus D/F/heading and source epoch. Scoped successors replace only
their stated scope; unchanged accepted claims remain applicable. Unresolved conflict names the
missing authorized decision. No generated index, original chat or task-archive sweep is required.

## 1. Architecture Map

Мини-LMS для изучения ООП спроектирована по слоистой модульной архитектуре (Clean Architecture):
- **Слой представления (UI/Templates):** Jinja2 шаблоны страниц лекций, интерактивных квизов, веб-редактора задач и профиля студента, стилизованные через Tailwind CSS (CDN).
- **Слой API / Контроллеров (`app/routers/`):** FastAPI эндпоинты для рендеринга страниц и REST API (проверка решений, отправка квизов, получение баллов).
- **Слой бизнес-логики (`app/services/`):**
  - `runner.py`: Изолированный движок верификации кода на базе `subprocess` и `pytest` во временных директориях с таймаутом (5 сек).
  - `scoring.py`: Подсчет баллов студента за квизы, практические задания, ДЗ и финальный экзамен.
- **Слой данных (`app/models/`, `app/database/`):** SQLite с доступом через SQLAlchemy ORM.
- **Слой контента (`content/`):** 3-недельный экспресс-курс на базе домена транспортной системы Avtobys (Неделя 1: Базовое ООП; Неделя 2: SOLID; Неделя 3: GoF и Clean Architecture; Финал: Экзамен).

### Architecture Decisions

- **D1 (Стек):** Python 3.12 (FastAPI, SQLAlchemy 2.0, SQLite, Pytest, Jinja2, Tailwind). Единый процесс без node_modules.
- **D2 (Домен):** Сквозной домен Avtobys (Алматы / Казахстан) для целостного понимания ООП от инвариантов до Clean Architecture.
- **D3 (Верификатор):** Двухуровневая проверка кода: статический AST-анализ классов и методов + изолированный запуск pytest с таймаутом (5 сек).
- **D4 (Документация):** Исчерпывающее документирование архитектуры, UML-диаграмм и API в папке `docs/`.
- **D5 (Zero-Build интерфейс):** Статические файлы UI (Tailwind CDN, Vanilla JS ES-модули, Mermaid.js) монтируются сервером без этапа сборки и внешних пакетных менеджеров.
- **D6 (Модуль Недели 1 и High-Water Mark):** Единый многовкладочный интерфейс ([Лекция] · [Квиз] · [Практикум] · [Лабораторная]) с LocalStorage автосохранением черновиков, изолированной автопроверкой через RunnerService (7 тестов TransitCard + 10 тестов SingleTripTicket/Bus), начислением 0..20 баллов (порог зачета >= 12) и защитой от понижения баллов по правилу max.

## 2. Key Artifacts

- **Конфигурация TFW:** `.tfw/project_config.yaml`
- **Профили участников:** `team/zhasulan.md` (автор/студент), `team/saubakirov.md` (преподаватель/ментор)
- **Исходные материалы ООП:** `C:\Users\kz444\OneDrive\Desktop\OOP` (9 лекций, 9 лабораторок, силлабус CS2203)
- **Инициализирующая задача:** `workspace/2026/OOP_20261015-015123_INIT/status.md` (DONE)
- **Каркас платформы (Задача 1):** `workspace/2026/OOP_20261015-022500_CORE/status.md` (DONE)
- **Модуль Недели 1 (Задача 2):** `workspace/2026/OOP_20261015-162432_W1MAT/status.md` (DONE)

## 3. Legacy & Deprecation

Проект является greenfield-разработкой веб-LMS, опирающейся на готовые методические материалы курса ООП (КазНУ, преподаватель Санжар Аубакиров).

## 4. Project Facts

- **F1 (Аудитория и формат):** Студенты 2 курса специальности «Программная инженерия». 3 недели: 1ч лекция, 1ч практика, 1ч ДЗ + итоговый экзамен.
- **F2 (Оценивание):** Преподаватель Санжар Аубакиров (`saubakirov`) оценивает работы студентов, ведущий разработчик — Жасулан Куандыков (`zhasulan`).
- **F3 (Локальный запуск):** Проект функционирует локально на рабочей машине без внешнего облачного деплоя.
- **F4 (Изоляция RunnerService):** Студенческий код запускается в `tempfile.TemporaryDirectory` с принудительным `timeout=5.0s` и предварительной блокировкой запрещенных модулей (`os`, `sys`, `subprocess`, `shutil`, `socket`) и вызовов (`eval`, `exec`).
- **F5 (Rich Domain Model & Инварианты Недели 1):** Сущности TransitCard и SingleTripTicket строго защищают свои инварианты (readonly is_validated через @property без сеттера с защитой AttributeError, детерминированное время через issued_at, однократность прохода, срок 60 мин, запрет отрицательного баланса и отрицательного тарифа).
