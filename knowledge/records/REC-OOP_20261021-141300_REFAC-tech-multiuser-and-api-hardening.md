# Knowledge record — REC-OOP_20261021-141300_REFAC-tech-multiuser-and-api-hardening: Многопользовательский селектор 4 студентов, режим SQLite WAL, отметка теории и харденинг публичного API

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261021-141300_REFAC-tech-multiuser-and-api-hardening` |
| Publication intent | Зафиксировать архитектурное решение по изоляции прогресса студентов группы, переводу эндпоинтов чтения в read-only режим и закрытию отладочных интерфейсов при внешнем доступе |
| Kind | technical-reference decision |
| Statement | В интерфейс добавлен селектор 4 студентов группы (Zhasulan, Roman, Arseniy, Saubakirov), передающий активный идентификатор через заголовок X-Student-Id. База данных SQLite переведена в режим WAL (PRAGMA journal_mode=WAL;), предотвращающий взаимные блокировки при конкурентных запросах. Эндпоинты чтения прогресса (GET /api/week{N}/progress, GET /api/students/scores) переведены в строгий read-only режим без вызова db.commit(). Добавлен топик week_N_theory и UI-кнопка отметки прочтения лекции. При переменной окружения PUBLIC_MODE=1 эндпоинты Swagger UI (/docs, /redoc) и отладочный раннер (/api/runner/smoke) блокируются (HTTP 403/404), а файл запуска публичного туннеля run_public.bat исключен из репозитория через .gitignore. |
| Applicability | Проект Web-OOP, модуль оценивания и профилей, роутеры API и сервисы данных. |
| Grounds and uncertainty | Подтверждено тестами tests/test_week_modules.py (изоляция студентов, отметка теории), tests/test_negative_cases.py (read-only поведение, HTTP 403 на smoke в public mode, валидация 422), сьютом 40/40 тестов, EV__OOP_20261021-141300_REFAC.md (VERIFIED) и вердиктом REVIEW__OOP_20261021-141300_REFAC.md (APPROVE). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | workspace/2026/OOP_20261021-141300_REFAC/RF__OOP_20261021-141300_REFAC.md @ 1046cf5c0db24bbda8f12e4e983378bfc390a4bb (§1, §2) и workspace/2026/OOP_20261021-141300_REFAC/REVIEW__OOP_20261021-141300_REFAC.md (§2, §4) |
| Originating task and unit | OOP_20261021-141300_REFAC, Executor antigravity:thread:local:794b3c0e-2f24-4cb3-846d-6f0ef33d9a4b / Reviewer antigravity:thread:local:7ff8150d-4da2-4cea-9205-49b86442239b |
| Producer | Coordinator antigravity:thread:local:8fc38498-8a48-43ea-b8a1-eec279b600e1 (zhasulan) |
| Qualifier | Coordinator zhasulan via /tfw-docs |
| Acceptance authority | owner:zhasulan (поправка A1 в TS__OOP_20261021-141300_REFAC.md, HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46) и независимый REVIEW__OOP_20261021-141300_REFAC.md (APPROVE) |
| Completed effect or missing decision | Опубликована запись технического решения, обновлен KNOWLEDGE.md (D10). |
| Relations | Scoped expansion к роутерам и модели данных платформы; устраняет коллизии баллов и блокировки БД при одновременной работе студентов группы. |

## Source and decision context

При публичной демонстрации через туннелирование все студенты ранее разделяли общую сессию, что приводило к перезаписи баллов. Добавление селектора студентов решило задачу без внедрения тяжелых систем аутентификации.

## Relations and current use

Дополняет KNOWLEDGE.md §1 Architecture Map (D10).

## Retry and continuation

Запись завершена и синхронизирована с KNOWLEDGE.md на этапе KNW задачи OOP_20261021-141300_REFAC.
