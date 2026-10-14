# Extract — Анализ структуры и конфигурационного пространства
> **Mindset:** Analyst. Building structure and combinations.
> Parent: [status.md](../../status.md)
> Goal: Развернуть TFW Full в проекте и спроектировать архитектуру мини-LMS по ООП

## Configuration Space

| Config | D1: Движок проверки кода | D2: Хранилище данных | D3: Frontend архитектура |
|---|---|---|---|
| **C1** | `pytest` в subprocess + timeout | SQLite (SQLAlchemy / SQLModel) | Jinja2 SSR + Tailwind CSS + Vanilla JS |
| **C2** | AST-валидатор + unit-тесты | SQLite (SQLAlchemy / SQLModel) | Jinja2 SSR + Tailwind CSS + Vanilla JS |
| **C3** | `pytest` в subprocess + timeout | SQLite напрямую (sqlite3) | Jinja2 + HTMX + Tailwind |
| **C4** | `exec()` in-process | JSON файлы | Чистый HTML + CSS |
| **C5** | Pyodide (в браузере) | SQLite (SQLAlchemy) | React / Vite SPA |

## Findings

### E1: Структура директорий проекта (Clean Architecture)
Для максимальной понятности ИИ и человеку проект организуется в чистые слои:
```
Web-OOP/
├── app/
│   ├── core/           # Конфигурация, безопасность, общие утилиты
│   ├── models/         # Модели БД (Student, Module, Lesson, Task, Submission)
│   ├── schemas/        # Pydantic схемы валидации
│   ├── database/       # Подключение к SQLite, сессии
│   ├── services/       # Бизнес-логика: курсы, тесты, проверка кода
│   │   ├── runner.py   # Изолированный запуск pytest для студенческого кода
│   │   └── scoring.py  # Подсчет баллов и прогресса
│   ├── routers/        # FastAPI эндпоинты (страницы + REST API)
│   ├── static/         # CSS, JS, иконки, диаграммы
│   └── templates/      # Jinja2 шаблоны (UI курсов, редактор, прогресс)
├── docs/               # Полная документация архитектуры, стека и UML
├── content/            # Материалы 3-недельного курса (лекции, задачи, тесты)
├── tests/              # Тесты самого веб-приложения (pytest)
└── workspace/          # TFW Full артефакты и трейсы
```

### E2: Гибридный движок проверки решений (C1 + C2)
- Сочетание C1 и C2 дает наилучший эффект:
  1. Сначала быстрый AST-анализ (`ast.parse`) проверяет наличие требуемых классов, методов и защиту инвариантов (например, отсутствие прямого изменения приватных полей `_balance` или наличие протокола).
  2. Затем изолированный запуск `pytest` в subprocess с таймаутом прогоняет тестовый набор предметной области Avtobys и генерирует отчет об успешности.
  3. Результаты тестов и набранные баллы немедленно сохраняются в профиле студента в SQLite.

## Checkpoint

| Found | Remaining |
|---|---|
| Построена матрица архитектурных конфигураций | Верификация несовместимых пар в Challenge |
| Сформирована целевая структура каталогов мини-LMS | Финализация RES-отчета |

**Sufficiency:**
- [x] External source used
- [x] Briefing gap closed
- [x] Configuration Space built from Gather dimensions

Stage complete: YES
