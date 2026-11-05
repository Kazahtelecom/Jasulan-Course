# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__OOP_20261105-211500_HDRERG.md](../RF__OOP_20261105-211500_HDRERG.md)
> TS: [TS__OOP_20261105-211500_HDRERG.md](../TS__OOP_20261105-211500_HDRERG.md)

## Understanding

Реализована оптимизация эргономики шапки Web-OOP: перенос кнопки настроек темы `#theme-settings-btn` в верхний ряд к профилю студента, внедрение комбо-сворачивания (интерактивный центрированный язычок `#header-collapse-handle` на нижней кромке шапки + текстовая кнопка `#header-collapse-toggle`), разделение навигационного ряда Row 2 на независимый контейнер подвкладок и закреплённый правый блок действий (`shrink-0`), а также лаконичные подписи вкладок экзамена, ликвидирующие появление горизонтальной полосы прокрутки при ширине экрана >= 1200px. Изменения затрагивают 3 файла VALUE (`header.html`, `style.css`, `app.js`), 1 файл ASSURANCE (`tests/test_header_ergonomics.py`) и полностью соответствуют утверждённой спецификации TS без модификации серверных API или роутов.

## Accepted Claims and Boundaries

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | Кнопка «🎨 Тема» перенесена в верхний ряд хедера рядом с селектором студента и доступна на всех страницах (`/week1`, `/week2`, `/week3`, `/exam`) | Кнопка останется во втором ряду или пропадёт с отдельных маршрутов, блокируя смену темы | `app/templates/components/header.html` (DOM Brand Row) | FastAPI Jinja2 template rendering | TS AC-1; HL §7.1 | `header.html@a408ff74` via `pytest tests/test_header_ergonomics.py` | yes |
| C2 | VALUE | На нижней кромке шапки `#main-site-header` добавлен язычок `#header-collapse-handle` со стрелкой-индикатором (`▲`/`▼`) и `onclick="toggleHeaderCollapse()"` | Студент в IDE-редакторе лишен быстрого 1-клик сворачивания шапки | `header.html`, `style.css`, DOM `#main-site-header` | Десктопные браузеры, CSS absolute positioning | TS AC-2; HL §7.1 | `header.html@a408ff74`, `style.css@a408ff74` | yes |
| C3 | VALUE | Текстовая кнопка `#header-collapse-toggle` сохранена в правом блоке Row 2 и синхронизирована с состоянием язычка | Нарушение доступности и десинхронизация лейблов/стрелок при сворачивании | `header.html`, `app.js:applyHeaderCollapseState` | Браузерный JS DOM API | TS AC-3; HL §7.1 | `header.html@a408ff74`, `app.js@a408ff74` | yes |
| C4 | VALUE | В Row 2 блок действий закреплен (`shrink-0`), а подвкладки экзамена лаконичны, исключая горизонтальный скролл при ширине экрана >= 1200px | Кнопки действий уезжают вправо за экран, мешая доступу к UML и сворачиванию | `header.html`, Flexbox layout Row 2 | Chrome/Firefox/Safari flex layout >=1200px | TS AC-4; HL §3, §7.1 | `header.html@a408ff74` | yes |
| C5 | VALUE | Состояние сворачивания сохраняется в `localStorage` (`weboop_header_collapsed`) и восстанавливается без FOUC | Сброс состояния шапки при переходе между страницами | `app.js`, `localStorage` API | Браузерный клиентский рантайм | TS AC-5; HL §5 (PV-2) | `app.js@a408ff74` | yes |
| C6 | ASSURANCE | Полный набор тестов репозитория проходит успешно (79 passed, 0 failed, 6 новых тестов) | Регрессия в существующем поведении страниц или функционале шапки | Модули `tests/` репозитория | Python 3.12, Pytest 9.1.1 | TS AC-6; HL §7.1 | Candidate commit `a408ff74` | yes |
| C7 | TRACE | Идентичность Candidate commit `a408ff74` и соблюдение границ VALUE селектора (3 файла, 158 строк) | Внесение непредусмотренных изменений или искажение учета бюджета | Git index, рабочий каталог | Git 2.x, репозиторий проекта | TS §4; RF §1 | Git diff numstat `77c5d083..a408ff74` | yes |
| C8 | TRACE | Полномочия и неизменный знаменатель: утверждение TS владельцем `zhasulan` в `journal/20261105-211501__handoff__c3d4.md` | Выполнение несанкционированных задач без одобрения владельца | `status.md`, `journal/` | TFW Governance conventions | HL §4.1; TS §4; status.md | `status.md`, `journal/` | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1: Перенос кнопки темы в верхний ряд | RF §1 (п. 1), §3 (AC-1) | C1 | ✅ |
| AC-2: Добавление язычка `#header-collapse-handle` | RF §1 (п. 2), §3 (AC-2) | C2 | ✅ |
| AC-3: Текстовая кнопка сохранена и синхронизирована | RF §1 (п. 3, 5), §3 (AC-3) | C3 | ✅ |
| AC-4: Устранение горизонтального скролла на `/exam` | RF §1 (п. 4), §3 (AC-4) | C4 | ✅ |
| AC-5: Персистентность в `localStorage` | RF §1 (п. 5), §3 (AC-5) | C5 | ✅ |
| AC-6: 74+ тестов зелёные (фактически 79) | RF §1 (п. 6), §3 (AC-6), §4 | C6 | ✅ |
| TS §4: VALUE accounting (3 файла VALUE, 1 ASSURANCE) | RF §1 Actual Accounting | C7, C8 | ✅ |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1–C4 | Rerun `pytest tests/test_header_ergonomics.py -v` + инспекция разметки `header.html` и стилей `style.css` | Непосредственная проверка соответствия DOM-структуры и CSS спецификации TS §5 | Тест проверяет разметку на стороне сервера; визуальный рендеринг стилей оценивается статически |
| C5 | Статический аудит `app.js` (`applyHeaderCollapseState`, `toggleHeaderCollapse`, чтение `localStorage`) | Клиентский JS выполняется в браузере; unit-тест проверяет исходник функции | Нет встроенного headless-браузера (Playwright/Selenium), но проверка JS логики исчерпывающая |
| C6 | Полный прогон `pytest` по всем 79 тестам | Подтверждение отсутствия любых регрессий в проекте | Нет |
| C7 | Независимый расчет `git diff --numstat` между baseline `77c5d083` и candidate `a408ff74` | Контроль целостности изменений и соблюдения Value-bearing accounting | Нет |
| C8 | Проверка статуса, журнала и неизменности утвержденного знаменателя | Проверка авторизации и непрерывности цепочки управления | Нет |

## Deviations from TS

No deviations. Все заявленные в TS требования выполнены в точности в указанных файлах без превышения скоупа.

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
