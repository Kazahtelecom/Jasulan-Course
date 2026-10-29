# TS — OOP_20261030-021700_THEME / Phase A: Core Design System, SVG Logo, and Settings Panel

> **Current filename**: `TS__phase-a__core_design_system_svg_logo_and_settings_panel.md`
> **Date**: 2026-10-30
> **Author**: Coordinator (`antigravity:thread:local:d1962507-3018-4f36-b88f-ccb71a3279b4`)
> **Status**: 🟢 APPROVED — Approved by zhasulan 2026-10-30
> **Parent HL**: [HL-OOP_20261030-021700_THEME.md](../HL-OOP_20261030-021700_THEME.md)

---

## 1. Objective

Реализовать архитектурное ядро дизайн-системы платформы Web-OOP: 4 фирменные неоновые палитры (`cyber-gold` по умолчанию, `electric-cyan`, `matrix-emerald`, `synthwave-purple`), тумблер свечения `Clean / Cyberpunk` на базе CSS-переменных, векторный адаптивный SVG-логотип в виде изометрического куба со скобками `{ }`, панель настроек оформления (модальное окно / выпадающее меню) в `header.html`, ранний инлайн-скрипт предотвращения FOUC в `<head>` страниц `index.html` и `exam.html`, а также модуль сохранения настроек в `localStorage` и набор автотестов в `tests/test_theme_system.py`.

---

## 2. Scope

### In Scope

- Объявление CSS Custom Properties в `app/static/css/style.css` для селекторов `[data-theme="..."]` и `[data-glow="..."]`.
- Замена базового синего квадрата «ООП» в `app/templates/components/header.html` на масштабируемый векторный SVG-логотип изометрического куба со скобками `{ }`, грани которого стилизуются через переменные темы.
- Внедрение кнопки открытия настроек (🎨 / ⚙️) и панели выбора темы (модальное окно с карточками-свотчами 4 палитр и тумблером Clean/Cyberpunk) в `header.html`.
- Интеграция микро-скрипта в `<head>` шаблонов `index.html` и `exam.html`, синхронно считывающего `weboop_theme` и `weboop_glow` до первого рендеринга `<body>` для исключения эффекта FOUC.
- Модуль управления темами в `app/static/js/app.js` (`initThemeSystem`, `switchTheme`, `setGlowMode`, привязка событий клика и синхронизация состояния).
- Написание набора автотестов `tests/test_theme_system.py` для проверки CSS-контрактов, разметки логотипа, панели настроек и FOUC-скрипта.

### Out of Scope

- Массовая замена 139 строк жестких классов Tailwind (`sky-`, `cyan-`) во всех внутренних подшаблонах `tab_*.html` (выделена в отдельную Phase B).
- Изменение логики подсчета баллов или контента задач в `app/content/` и `app/services/`.
- Добавление внешних сборщиков (`npm`, `webpack`) — строгое сохранение Zero-Build.

---

## 3. Principles Check

| # | HL §7 principle | Enforced by | Gate |
|---|---|---|---|
| P1 | Zero-Build & Native CSS Variables First | AC-1, AC-2 | Использование стандартных CSS Custom Properties без препроцессоров |
| P2 | Semantic Independence of Functional Statuses | AC-7 | Индикаторы тестов (Pass/Fail) сохраняют зелёный/красный цвет |
| P3 | Zero Flash of Unstyled Content (FOUC) | AC-5 | Инлайн-скрипт в `<head>` до рендера `<body>` |
| P4 | Non-Destructive UML Diagram Semantics | Out of Scope | Внутренности UML не затрагиваются в Phase A |
| P5 | LocalStorage Isolation & Graceful Fallback | AC-6 | При отсутствии ключей дефолт: `cyber-gold` и `cyberpunk` |

---

## 4. Affected Files and Value-Bearing Accounting

| File / selector | Action | Class | Semantic reason / required result |
|---|---|---|---|
| `app/static/css/style.css` | MODIFY | `VALUE` | CSS-переменные 4 тем, тумблера Clean/Cyberpunk, стили панели настроек |
| `app/templates/components/header.html` | MODIFY | `VALUE` | Векторный SVG-логотип изометрического куба, кнопка и модалка настроек темы |
| `app/templates/index.html` | MODIFY | `VALUE` | Инлайн-скрипт в `<head>` для чтения `localStorage` и предотвращения FOUC |
| `app/templates/exam.html` | MODIFY | `VALUE` | Инлайн-скрипт в `<head>` для чтения `localStorage` и предотвращения FOUC |
| `app/static/js/app.js` | MODIFY | `VALUE` | Модуль переключения тем, обработчики событий и сохранение в `localStorage` |
| `tests/test_theme_system.py` | CREATE | `ASSURANCE` | Комплексные автотесты разметки, FOUC-скриптов и CSS-токенов |

### Prospective accounting contract

| Fact | Approved value |
|---|---|
| Subject / exact VALUE selector | `app/static/css/style.css`, `app/templates/components/header.html`, `app/templates/index.html`, `app/templates/exam.html`, `app/static/js/app.js` |
| Baseline / selector source | `91921d22dfbf9a87cc18a0ae194b435b713bcb69`; this TS at approval commit |
| Candidate rule | First tested Executor commit with required VALUE+ASSURANCE, before EV/RF/REVIEW/final transition; excluded-only later writes do not move it; later VALUE requires a new Candidate and recomputation |
| Logical VALUE files | 5 files |
| Touched text LOC | ~310 additions + ~35 deletions = ~345 total LOC |
| Triggers / disposition | 50 files / 5000 LOC trigger (current: 5 files / ~345 LOC — within single-phase budget) |
| Multiplier / authority | Owner escalation multiplier 2 (up to 10 files / 690 LOC); pre-work decision |
| Approval epoch / failure | Prospective epoch; missing/mutable/mismatched/late = BLOCKED; metric-only N/A; unresolved phase = INVALID; DEFERRED is non-terminal |

```powershell
git diff --name-status --find-renames=50% -z 91921d22dfbf9a87cc18a0ae194b435b713bcb69 <CANDIDATE_SHA> -- app/static/css/style.css app/templates/components/header.html app/templates/index.html app/templates/exam.html app/static/js/app.js
git diff --numstat --find-renames=50% -z 91921d22dfbf9a87cc18a0ae194b435b713bcb69 <CANDIDATE_SHA> -- app/static/css/style.css app/templates/components/header.html app/templates/index.html app/templates/exam.html app/static/js/app.js
```

### Prospective scope rulings

None. All deliverables protect named value and necessary assurance.

### Task-local hard constraints

| M1 consequence | M2 object/risk | M3 measure/selector | M4 pre-act check | M5 softer-control gap | M6 change authority |
|---|---|---|---|---|---|
| FOUC при переходе между страницами | Опыт студента при навигации | Проверка наличия синхронного скрипта в `<head>` до тега `<body>` | Тест `test_theme_system.py` проверяет AST/HTML `<head>` | Отсутствие скрипта приводит к заметному миганию интерфейса | Coordinator / Owner |

**Actions (not budget dimensions):** 5 MODIFY, 1 CREATE.  
**Immutable owner-approved denominator:** 5 VALUE files, 345 touched LOC.

---

## 5. Acceptance Criteria

### AC-1: Реализация 4 неоновых палитр в `style.css`

В `app/static/css/style.css` объявлены CSS Custom Properties для селекторов:
- `:root, [data-theme="cyber-gold"]` (дефолтная тема):
  - `--theme-primary: #f59e0b;`
  - `--theme-accent: #fbbf24;`
  - `--theme-glow: rgba(245, 158, 11, 0.45);`
  - `--theme-border: rgba(245, 158, 11, 0.35);`
  - `--theme-bg-gradient`: радиальные янтарные градиенты.
- `[data-theme="electric-cyan"]`:
  - `--theme-primary: #00f0ff;`
  - `--theme-accent: #38bdf8;`
  - `--theme-glow: rgba(0, 240, 255, 0.45);`
  - `--theme-border: rgba(56, 189, 248, 0.35);`
  - `--theme-bg-gradient`: радиальные цианово-синие градиенты.
- `[data-theme="matrix-emerald"]`:
  - `--theme-primary: #10b981;`
  - `--theme-accent: #34d399;`
  - `--theme-glow: rgba(16, 185, 129, 0.45);`
  - `--theme-border: rgba(16, 185, 129, 0.35);`
  - `--theme-bg-gradient`: радиальные изумрудные градиенты.
- `[data-theme="synthwave-purple"]`:
  - `--theme-primary: #d946ef;`
  - `--theme-accent: #c084fc;`
  - `--theme-glow: rgba(217, 70, 239, 0.45);`
  - `--theme-border: rgba(217, 70, 239, 0.35);`
  - `--theme-bg-gradient`: радиальные пурпурные градиенты.

Gate: `python -m pytest tests/test_theme_system.py -k test_css_theme_variables`  
Evidence: CSS содержит все 4 селектора и токены.

---

### AC-2: Тумблер режимов свечения Clean / Cyberpunk

В `style.css` объявлены правила для режимов свечения:
- `[data-glow="cyberpunk"]` (дефолт):
  - Карточки `.cyber-card` и активные табы имеют свечение `box-shadow` с использованием `var(--theme-glow)`.
  - Фоновые радиальные градиенты активны на `body`.
- `[data-glow="clean"]`:
  - Отключает размытые неоновые тени (`box-shadow: none !important;` или минимальная контрастная тень).
  - Отключает цветные радиальные градиенты фона (`background-image: none !important;`).
  - Обеспечивает строгий высококонтрастный вид карточек без визуального шума.

Gate: `python -m pytest tests/test_theme_system.py -k test_css_glow_modes`  
Evidence: Наличие правил для `[data-glow="clean"]` и `[data-glow="cyberpunk"]`.

---

### AC-3: Векторный изометрический SVG-логотип в `header.html`

В блоке бренда `header.html` вместо квадратного градиентного блока с текстом `ООП` интегрирован масштабируемый инлайновый SVG:
- Изометрический куб с 3 видимыми гранями (верхняя, левая, правая), отрисованными векторными путями `<path>`.
- Центральный элемент: парящие фигурные скобки `{ }` внутри куба с неоновой подсветкой.
- Грани и скобки куба используют `stroke="var(--theme-accent)"`, `fill="var(--theme-primary)"` или классы, привязанные к переменным темы, и динамически меняют цвет при переключении палитры.
- Размер блока: компактный (12×12 или 14×14 в Tailwind, 48–56px), адаптивный.

Gate: `python -m pytest tests/test_theme_system.py -k test_svg_logo_present`  
Evidence: Тест находит `<svg id="header-logo-cube"` со структурой изометрических граней и `{}`.

---

### AC-4: Кнопка и модальное окно настроек в `header.html`

В `header.html` реализован элемент управления внешним видом:
- Кнопка вызова настроек темы с иконкой (🎨 или ⚙️) и подписью в правой части шапки рядом с переключателем студентов или кнопкой сворачивания меню.
- Панель настроек (модальное окно или выпадающий оверлей с ID `theme-settings-modal`):
  - Заголовок «Настройки оформления».
  - Сетка/список 4 палитр (с визуальными цветными кружками-свотчами для каждой темы).
  - Радио-переключатель или сегментированный тумблер выбора режима свечения: `Clean (Строгий)` vs `Cyberpunk (Неон)`.
  - Кнопка закрытия модального окна (крестик и клик по оверлею/Escape).

Gate: `python -m pytest tests/test_theme_system.py -k test_theme_settings_modal_markup`  
Evidence: Проверка наличия элементов управления и атрибутов в HTML.

---

### AC-5: Предотвращение мигания темы (Zero FOUC) в `<head>`

В `<head>` файлов `index.html` и `exam.html` добавлен синхронный микро-скрипт (до любого рендеринга `<body>`):
```javascript
<script>
  (function() {
    var savedTheme = localStorage.getItem('weboop_theme') || 'cyber-gold';
    var savedGlow = localStorage.getItem('weboop_glow') || 'cyberpunk';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-glow', savedGlow);
  })();
</script>
```

Gate: `python -m pytest tests/test_theme_system.py -k test_zero_fouc_script_present`  
Evidence: Проверка наличия скрипта в `<head>` обоих главных HTML-файлов.

---

### AC-6: Клиентский модуль управления темами в `app.js`

В `app/static/js/app.js` реализован модуль:
- `initThemeSystem()`: считывает текущую тему и режим свечения, синхронизирует состояние кнопок/свотчей в модалке настроек, навешивает слушатели кликов.
- `switchTheme(themeId)`: обновляет атрибут `data-theme` на `document.documentElement`, сохраняет в `localStorage.setItem('weboop_theme', themeId)`, обновляет подсветку активной темы в модалке.
- `setGlowMode(mode)`: обновляет атрибут `data-glow` на `document.documentElement`, сохраняет в `localStorage.setItem('weboop_glow', mode)`, обновляет визуальное положение тумблера.
- Функции открытия/закрытия панели настроек `openThemeSettings()` и `closeThemeSettings()`.

Gate: `python -m pytest tests/test_theme_system.py -k test_theme_js_functions`  
Evidence: Синтаксический анализ `app.js` подтверждает наличие функций и ключей `weboop_theme`, `weboop_glow`.

---

### AC-7: Регрессионная верификация тестов платформы

- Создан файл автотестов `tests/test_theme_system.py` с проверкой всех аспектов Phase A.
- Все существующие тесты платформы (`tests/test_health.py`, `tests/test_ui_ergonomics.py`, `tests/test_exam.py`, `tests/test_week*.py` — 60+ тестов) проходят со 100% успехом без падений.

Gate: `pytest tests/ -q`  
Evidence: Все тесты (60 существующих + новые тесты тем) зелёные.

---

### Evidence Artifacts

| File | Description |
|---|---|
| `evidence/EV__phase-a__core_design_system_svg_logo_and_settings_panel.md` | Структурированный отчёт проверки критериев AC-1 — AC-7 |

---

## 6. Technical Guidance

1. **Изометрический SVG куб:**
   Для угла 30° стандартные изометрические координаты в `viewBox="0 0 64 64"`:
   - Верхняя грань (светлая): `d="M32 6 L54 18 L32 30 L10 18 Z"`
   - Левая грань (средняя): `d="M10 18 L32 30 L32 56 L10 44 Z"`
   - Правая грань (темная/контрастная): `d="M32 30 L54 18 L54 44 L32 56 Z"`
   - Центральные символы скобок `{ }`: `<text x="32" y="38" text-anchor="middle" font-family="monospace" font-weight="900" font-size="16" fill="var(--theme-accent)">{ }</text>`
2. **Модальное окно настроек:**
   Реализовать как фиксированный оверлей (`fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm hidden`) с карточкой `.cyber-card max-w-md w-full p-6 rounded-2xl`.

---

## 7. Definition of Failure

- ❌ Появление мигания стилей (FOUC) при перезагрузке страницы.
- ❌ Падение любого из существующих 60 автотестов платформы.
- ❌ Ошибки JavaScript в консоли браузера при вызове модального окна настроек.
- ❌ Несохранение выбранной темы или режима свечения в `localStorage`.

---

## 8. Phase Risks

| Risk | Mitigation |
|---|---|
| Специфичность селекторов Tailwind CDN перекрывает CSS-переменные | Использование точных селекторов `[data-theme="..."]` и классов-оберток в `style.css` |
| Закрытие модального окна блокирует прокрутку страницы | Корректное переключение класса `hidden` без мутации `overflow` body |

---

## 9. Cross-Phase Modifications (multi-phase only)

| File | Also modified in | Coordination note |
|---|---|---|
| `app/templates/components/header.html` | Phase B | В Phase A добавляются логотип и модалка настроек; в Phase B мигрируются оставшиеся жесткие цвета навигационных табов |
| `app/static/js/app.js` | Phase B | В Phase A добавляется модуль тем; в Phase B рефакторятся цвета динамической разметки |
| `app/static/css/style.css` | Phase B | В Phase A создаются базовые токены; в Phase B добавляются вспомогательные семантические утилиты при необходимости |

---

*TS — OOP_20261030-021700_THEME / Phase A: Core Design System, SVG Logo, and Settings Panel | 2026-10-30*
