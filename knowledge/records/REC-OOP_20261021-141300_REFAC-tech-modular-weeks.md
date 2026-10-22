# Knowledge record — REC-OOP_20261021-141300_REFAC-tech-modular-weeks: Модульная архитектура недель платформы (WeekModule, WeekRegistry) и декомпозиция фронтенда

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261021-141300_REFAC-tech-modular-weeks` |
| Publication intent | Зафиксировать переход от дублирования кода недель к абстрактному контракту WeekModule, единому реестру WeekRegistry и декомпозиции монолитного шаблона на Jinja-компоненты |
| Kind | technical-reference decision |
| Statement | Дублирование кода между Неделей 1 и Неделей 2 устранено более чем на 75% посредством введения абстрактного контракта WeekModule (app/modules/base.py) и централизованного реестра WeekRegistry (app/modules/registry.py). Маршрутизаторы week1.py и week2.py делегируют валидацию и обработку обобщенному роутеру weeks.py. Монолитный index.html (607 строк) декомпозирован на 6 переиспользуемых Jinja-компонентов в app/templates/components/ (header.html, tab_home.html, tab_theory.html, tab_practice.html, tab_quiz.html, tab_results.html), сократив объем корневого файла до 33 строк (>90% сокращения). Логика клиентского app.js реорганизована в 8 модулей. |
| Applicability | Проект Web-OOP, все текущие и последующие учебные недели (начиная с Недели 3). |
| Grounds and uncertainty | Подтверждено прохождением автотестов test_week_modules.py, общим результатом 40/40 тестов без регрессий (15.51s), EV__OOP_20261021-141300_REFAC.md (7/7 VERIFIED), независимым вердиктом REVIEW__OOP_20261021-141300_REFAC.md (APPROVE). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | workspace/2026/OOP_20261021-141300_REFAC/RF__OOP_20261021-141300_REFAC.md @ 1046cf5c0db24bbda8f12e4e983378bfc390a4bb (§1, §2) и workspace/2026/OOP_20261021-141300_REFAC/REVIEW__OOP_20261021-141300_REFAC.md (§2, §4) |
| Originating task and unit | OOP_20261021-141300_REFAC, Executor antigravity:thread:local:794b3c0e-2f24-4cb3-846d-6f0ef33d9a4b / Reviewer antigravity:thread:local:7ff8150d-4da2-4cea-9205-49b86442239b |
| Producer | Coordinator antigravity:thread:local:8fc38498-8a48-43ea-b8a1-eec279b600e1 (zhasulan) |
| Qualifier | Coordinator zhasulan via /tfw-docs |
| Acceptance authority | owner:zhasulan (HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46, TS__OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46) и независимый REVIEW__OOP_20261021-141300_REFAC.md (APPROVE) |
| Completed effect or missing decision | Опубликована запись технического решения, обновлены KNOWLEDGE.md (D8, Key Artifacts, Legacy & Deprecation) и чек-лист закрытия в REVIEW. |
| Relations | Scoped successor к REC-OOP_20261018-222800_W2SOL-tech-week2-multiweek (D7): заменяет прямое дублирование роутеров и монолитный шаблон на реестр модулей и компонентную верстку без изменения внешнего API и поведения недель 1 и 2. |

## Source and decision context

В ходе аудита выявлено, что создание Недели 3 путем дальнейшего копирования роутеров создало бы критический техдолг. Создан абстрактный класс WeekModule с интерфейсом get_theory_steps(), get_practice_tasks(), get_quiz_questions() и реестр WeekRegistry. Обобщенный роутер app/routers/weeks.py централизует эндпоинты страниц и API (/week{N}, /api/week{N}/theory, /practice, /quiz), а week1.py и week2.py содержат тонкие делегирующие вызовы.

## Relations and current use

Дополняет KNOWLEDGE.md §1 Architecture Map (D8). Неделя 3 подключается декларативно созданием класса Week3Module и регистрацией в WeekRegistry.

## Retry and continuation

Запись завершена и синхронизирована с KNOWLEDGE.md на этапе KNW задачи OOP_20261021-141300_REFAC.
