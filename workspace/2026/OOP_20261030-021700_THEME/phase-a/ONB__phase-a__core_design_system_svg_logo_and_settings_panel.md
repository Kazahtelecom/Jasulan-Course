# ONB — OOP_20261030-021700_THEME / Phase A: Core Design System, SVG Logo, and Settings Panel

> **Current filename**: `ONB__phase-a__core_design_system_svg_logo_and_settings_panel.md`
> **Date**: 2026-10-30
> **Author**: Executor (`antigravity:thread:local:29d073ad-cf42-4504-9212-4aaa7e0ef202`)
> **Status**: 🟠 ONB — Onboarding recorded
> **Parent HL**: [HL-OOP_20261030-021700_THEME.md](../HL-OOP_20261030-021700_THEME.md)
> **TS**: [TS__phase-a__core_design_system_svg_logo_and_settings_panel.md](TS__phase-a__core_design_system_svg_logo_and_settings_panel.md)
> **Producer unit**: `antigravity:thread:local:29d073ad-cf42-4504-9212-4aaa7e0ef202`
> **Parent Coordinator**: `antigravity:thread:local:d1962507-3018-4f36-b88f-ccb71a3279b4`
> **Activation / dispatch source**: owner-direct (`/tfw-handoff OOP_20261030-021700_THEME/phase-a`)
> **Coordination authority**: "HL-OOP_20261030-021700_THEME.md @ 91921d22dfbf9a87cc18a0ae194b435b713bcb69"
> **Originating proposer**: `none`

---

## 1. Understanding

В рамках Phase A реализуется архитектурный фундамент мульти-темовой дизайн-системы платформы Web-OOP: 4 фирменные палитры (`cyber-gold` по умолчанию, `electric-cyan`, `matrix-emerald`, `synthwave-purple`), переключатель интенсивности свечения `Clean / Cyberpunk` на нативных CSS-переменных, векторный адаптивный SVG-логотип в виде изометрического куба со скобками `{ }`, реагирующий на активную палитру, модальная панель настроек внешнего вида в навигационной шапке сайта (`header.html`), синхронный инлайн-микроскрипт предотвращения FOUC в `<head>` страниц `index.html` и `exam.html`, логика персистентности в `localStorage` (`weboop_theme`, `weboop_glow`) в `app.js`, а также комплект регрессионных автотестов `tests/test_theme_system.py`.

## 2. Entry Points

- `app/static/css/style.css`: объявление CSS-токенов палитр (`--theme-primary`, `--theme-accent`, `--theme-glow`, `--theme-border`, `--theme-bg-gradient`), правил `[data-glow="clean"]` / `[data-glow="cyberpunk"]`, стилей модалки настроек и SVG-куба.
- `app/templates/components/header.html`: замена устаревшего блока логотипа на изометрический SVG куб, добавление кнопки вызова настроек оформления и разметки модального окна `theme-settings-modal`.
- `app/templates/index.html` & `app/templates/exam.html`: внедрение синхронного инлайн-скрипта в `<head>` перед `<body>` для исключения FOUC.
- `app/static/js/app.js`: функции `initThemeSystem`, `switchTheme`, `setGlowMode`, `openThemeSettings`, `closeThemeSettings` и привязка событий.
- `tests/test_theme_system.py`: тесты на наличие токенов CSS, селекторов режимов свечения, структуры SVG логотипа, разметки панели настроек и FOUC-скриптов.

Временные ресурсы и утилизация: временные файлы тестов и вывод утилит изолируются в `%TEMP%\tfw\OOP_20261030-021700_THEME\`; в репозиторий попадают только проверенные файлы артефактов и исходного кода.

## 3. Questions (blocking — cannot proceed without answers)

No blocking questions.

## 4. Recommendations (suggestions, not blocking)

1. Обработать закрытие модального окна настроек не только по клику на кнопку закрытия и оверлей, но и по нажатию клавиши `Escape`.
2. Предусмотреть защиту от всплытия событий клика внутри карточки модального окна (`event.stopPropagation()`), чтобы клик по опциям не закрывал модалку.
3. Обеспечить корректный fallback при недоступности `localStorage` (например, в режиме Private Browsing с заблокированным хранилищем).

## 5. Risks Found (edge cases, potential issues not in TS)

1. Специфичность селекторов Tailwind CDN: инлайн-стили или утилиты с `!important` могут конфликтовать со свойствами `[data-glow="clean"]`. Решение: точечное переопределение `box-shadow` и фоновых градиентов для классов `.cyber-card`, `.week-pill-active`, `.subtab-active` и `body`.

## 6. Inconsistencies with Code (spec vs reality)

Несоответствий не обнаружено. Структура шаблонов, `style.css` и `app.js` полностью соответствует описанию в TS.

## 7. Knowledge Citations

| # | HL §7.2 ref | Read? | Applied / N/A | Notes |
|---|-------------|-------|---------------|-------|
| 1 | `README.md` (P0) | ✅ | Applied | Соблюдение педагогических стандартов и современного вида платформы Web-OOP. |
| 2 | `.tfw/README.md` (P1) | ✅ | Applied | Реализация без заглушек, 100% прохождение автотестов (AC-7). |
| 3 | `knowledge/philosophy.md` (P2) | ✅ | Applied | Zero-Build архитектура: CSS Custom Properties без препроцессоров и сборщиков. |
| 4 | `KNOWLEDGE.md` §1 (P3) D1 | ✅ | Applied | Соответствие стеку FastAPI, Jinja2, Tailwind CDN, Vanilla JS. |
| 5 | `KNOWLEDGE.md` §1 (P3) D5 | ✅ | Applied | Zero-Build: прямое монтирование статики FastAPI. |
| 6 | `KNOWLEDGE.md` §1 (P3) D6 | ✅ | Applied | Развитие киберпанк-стилистики с 4 темами и контрастным Clean-режимом. |
| 7 | `KNOWLEDGE.md` §1 (P3) D8 | ✅ | Applied | Точечная модификация декомпозированного `header.html`. |
| 8 | `KNOWLEDGE.md` §1 (P3) D11 | ✅ | Applied | Эргономика интерфейса и поддержка Clean режима для снижения усталости глаз. |
| 9 | `KNOWLEDGE.md` §4 (P7) F7 | ✅ | Applied | Сохранение Zero-Build изоляции окружения хоста. |
| 10 | `KNOWLEDGE.md` §4 (P7) F9 | ✅ | Applied | Сохранение доступности селектора студентов и кнопки сворачивания шапки. |

### Material handover at this return

- **Producer unit**: `antigravity:thread:local:29d073ad-cf42-4504-9212-4aaa7e0ef202`
- **Source / epoch**: `91921d22dfbf9a87cc18a0ae194b435b713bcb69` / `e7864cf`
- **Inspected scope**: `app/static/css/style.css`, `app/templates/components/header.html`, `app/templates/index.html`, `app/templates/exam.html`, `app/static/js/app.js`, `tests/`
- **Material or justified-none**: Material. Онбординг пройден успешно, блокирующих вопросов нет, приступаем к реализации Phase A.
- **Uncertainty**: None.
- **Continuation**: Реализация AC-1 — AC-7, подготовка Candidate commit, формирование EV и RF.

---

*ONB — OOP_20261030-021700_THEME / Phase A: Core Design System, SVG Logo, and Settings Panel | 2026-10-30*
