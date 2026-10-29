# TS — OOP_20261030-021700_THEME / Phase B: Template and Script Migration to Semantic Theme Tokens

> **Current filename**: `TS__phase-b__template_and_script_migration_to_semantic_theme_tokens.md`
> **Date**: 2026-10-30
> **Author**: Coordinator (`antigravity:thread:local:d1962507-3018-4f36-b88f-ccb71a3279b4`)
> **Status**: 🟢 APPROVED — Approved by zhasulan 2026-10-30
> **Parent HL**: [HL-OOP_20261030-021700_THEME.md](../HL-OOP_20261030-021700_THEME.md)
> **Predecessor**: Phase A ✅ ([RF Phase A](../phase-a/RF__phase-a__core_design_system_svg_logo_and_settings_panel.md), Candidate `5855e38a94e3293f65efc0ad3bc3a32861c83439`)

---

## 1. Objective

Завершить комплексную миграцию разметки платформы Web-OOP на созданную в Phase A токенизированную дизайн-систему тем: заменить все разрозненные жёсткие классы Tailwind `sky-`, `cyan-`, `amber-` в подшаблонах страниц (`tab_home.html`, `tab_theory.html`, `tab_practice.html`, `tab_quiz.html`, `tab_results.html`), навигационной шапке (`header.html`), странице экзамена (`exam.html`), внешней обвязке и панели управления вьювера диаграмм (`uml_viewer.html`), а также в динамических строковых генераторах HTML в `app/static/js/app.js`. Обеспечить безупречную визуальную целостность интерфейса во всех 4 палитрах (`cyber-gold`, `electric-cyan`, `matrix-emerald`, `synthwave-purple`) и в обоих режимах свечения (`Clean` и `Cyberpunk`) при строгом сохранении функциональных индикаторов тестирования (PASS = `emerald`, FAIL = `rose`) и архитектурных цветов диаграмм классов Clean Architecture.

---

## 2. Scope

### In Scope

- Замена жестких акцентных классов `sky-`, `cyan-`, `amber-` на семантические CSS-переменные/классы темы в компонентах:
  - `app/templates/components/tab_home.html` (карточки обзора, ссылки быстрого старта, бейджи).
  - `app/templates/components/tab_theory.html` (анатомия классов, шаги теории, карточки инвариантов).
  - `app/templates/components/tab_practice.html` (панель редактора кода, переключатели задач, кнопки запуска и подсказок).
  - `app/templates/components/tab_quiz.html` (карточки вопросов, индикаторы прогресса).
  - `app/templates/components/tab_results.html` (итоговые баллы недели, карточки зачета).
  - `app/templates/components/header.html` (пилюли недель `week-pill-active`, подтабы `subtab-active`, бейдж баллов).
  - `app/templates/exam.html` (карточки регламента, инструкция, таймер, контейнеры боевых задач).
  - `app/templates/components/uml_viewer.html` (панель инструментов, кнопки масштабирования, рамка лупы, фоновая сетка).
- Рефакторинг генерации динамической HTML-разметки в `app/static/js/app.js` (индикаторы выбранных вариантов квиза, рамки активных задач, уведомления-тосты).
- Добавление вспомогательных семантических классов в `app/static/css/style.css` (`.theme-accent-text`, `.theme-border`, `.theme-glow-card`) для лаконичной привязки в шаблонах.
- Расширение тестового набора в `tests/test_theme_system.py` проверками отсутствия паразитных жестких акцентных классов и регрессионная верификация всей тестовой базы (67+ тестов).

### Out of Scope

- Изменение внутренних цветов нод и связей классов внутри SVG в `uml_viewer.html` (сохранение международной нотации Clean Architecture).
- Мутация логики верификатора `ASTValidator`, исполнителя `RunnerService` или системы начисления баллов `ScoringService`.
- Изменение функциональных цветов статусов тестов песочницы (`emerald` для успеха, `rose` для ошибок).

---

## 3. Principles Check

| # | HL §7 principle | Enforced by | Gate |
|---|---|---|---|
| P1 | Zero-Build & Native CSS Variables First | AC-1 — AC-6 | Все стили опираются на нативные CSS Custom Properties |
| P2 | Semantic Independence of Functional Statuses | AC-2, AC-3 | Статусы тестов и зачета остаются зелеными/красными |
| P3 | Zero Flash of Unstyled Content (FOUC) | AC-4 | Сохраняется синхронная инициализация из Phase A |
| P4 | Non-Destructive UML Diagram Semantics | AC-5 | Стилизуется только оболочка и лупа вьювера, схемы не ломаются |
| P5 | LocalStorage Isolation & Graceful Fallback | AC-6 | Применяются дефолтные переменные `cyber-gold` |

---

## 4. Affected Files and Value-Bearing Accounting

| File / selector | Action | Class | Semantic reason / required result |
|---|---|---|---|
| `app/templates/components/tab_home.html` | MODIFY | `VALUE` | Миграция жестких классов на семантические токены темы |
| `app/templates/components/tab_theory.html` | MODIFY | `VALUE` | Миграция жестких классов на семантические токены темы |
| `app/templates/components/tab_practice.html` | MODIFY | `VALUE` | Миграция жестких классов на семантические токены темы |
| `app/templates/components/tab_quiz.html` | MODIFY | `VALUE` | Миграция жестких классов на семантические токены темы |
| `app/templates/components/tab_results.html` | MODIFY | `VALUE` | Миграция жестких классов на семантические токены темы |
| `app/templates/components/header.html` | MODIFY | `VALUE` | Миграция активных пилюль недель и табов на токены темы |
| `app/templates/components/uml_viewer.html` | MODIFY | `VALUE` | Миграция тулбара, рамки и лупы вьювера на токены темы |
| `app/templates/exam.html` | MODIFY | `VALUE` | Миграция оформления экзаменационного модуля на токены темы |
| `app/static/js/app.js` | MODIFY | `VALUE` | Миграция строковых генераторов разметки на токены темы |
| `app/static/css/style.css` | MODIFY | `VALUE` | Поддержка токенизированных утилит активных табов и рамок |
| `tests/test_theme_system.py` | MODIFY | `ASSURANCE` | Проверка отсутствия жестких цветов и целостности темы |

### Prospective accounting contract

| Fact | Approved value |
|---|---|
| Subject / exact VALUE selector | `app/templates/components/tab_home.html`, `app/templates/components/tab_theory.html`, `app/templates/components/tab_practice.html`, `app/templates/components/tab_quiz.html`, `app/templates/components/tab_results.html`, `app/templates/components/header.html`, `app/templates/components/uml_viewer.html`, `app/templates/exam.html`, `app/static/js/app.js`, `app/static/css/style.css` |
| Baseline / selector source | `0c5555e5b245563e344b957391a0c2592117955c` (Phase A close commit); this TS at approval commit |
| Candidate rule | First tested Executor commit with required VALUE+ASSURANCE, before EV/RF/REVIEW/final transition; excluded-only later writes do not move it; later VALUE requires a new Candidate and recomputation |
| Logical VALUE files | 10 files |
| Touched text LOC | ~240 additions + ~240 deletions = ~480 total LOC |
| Triggers / disposition | Single-phase budget respected (within trigger ceiling 50 files / 5000 LOC) |
| Multiplier / authority | Owner escalation multiplier 2 (up to 20 files / 960 LOC); pre-work decision |
| Approval epoch / failure | Prospective epoch; missing/mutable/mismatched/late = BLOCKED; metric-only N/A; unresolved phase = INVALID; DEFERRED is non-terminal |

```powershell
git diff --name-status --find-renames=50% -z 0c5555e5b245563e344b957391a0c2592117955c <CANDIDATE_SHA> -- app/templates/components/tab_home.html app/templates/components/tab_theory.html app/templates/components/tab_practice.html app/templates/components/tab_quiz.html app/templates/components/tab_results.html app/templates/components/header.html app/templates/components/uml_viewer.html app/templates/exam.html app/static/js/app.js app/static/css/style.css
git diff --numstat --find-renames=50% -z 0c5555e5b245563e344b957391a0c2592117955c <CANDIDATE_SHA> -- app/templates/components/tab_home.html app/templates/components/tab_theory.html app/templates/components/tab_practice.html app/templates/components/tab_quiz.html app/templates/components/tab_results.html app/templates/components/header.html app/templates/components/uml_viewer.html app/templates/exam.html app/static/js/app.js app/static/css/style.css
```

### Prospective scope rulings

None. All deliverables directly implement the agreed Phase B scope.

### Task-local hard constraints

| M1 consequence | M2 object/risk | M3 measure/selector | M4 pre-act check | M5 softer-control gap | M6 change authority |
|---|---|---|---|---|---|
| Потеря различимости тестов при замене цветов | Статусы прохождения тестов песочницы | Классы `emerald-` и `rose-` сохранены для результатов выполнения кода | Тесты в `test_theme_system.py` проверяют семантику PASS/FAIL | Студент не сможет понять, сдан ли тест, если результат окрасится в желтый или фиолетовый | Coordinator / Owner |

**Actions (not budget dimensions):** 10 MODIFY (`VALUE`), 1 MODIFY (`ASSURANCE`).  
**Immutable owner-approved denominator:** 10 VALUE files, 480 touched LOC.

---

## 5. Acceptance Criteria

### AC-1: Миграция подшаблонов «Главная» и «Теория»

В `tab_home.html` и `tab_theory.html` все жесткие классы декоративного акцента (`text-sky-400`, `border-sky-500/20`, `bg-sky-500/10`, `text-cyan-400`) заменены на семантические классы и переменные темы (`var(--theme-accent)`, `var(--theme-border)`, `.theme-accent-text`, `.theme-border`).
Бейджи шагов теории и карточки преимуществ гармонично принимают цвет активной палитры.

Gate: `python -m pytest tests/test_theme_system.py -k test_home_and_theory_theme_tokens`  
Evidence: Проверка шаблонов на отсутствие жестких `sky-` классов в декоративных элементах.

---

### AC-2: Миграция подшаблонов «Практика», «Квиз» и «Результаты»

В `tab_practice.html`, `tab_quiz.html` и `tab_results.html`:
- Рамки редактора кода, активные табы задач, разделитель колонок используют `var(--theme-border)` и `var(--theme-glow)`.
- Кнопки запуска кода и подсказок оформлены через переменные темы.
- Карточки вопросов и активные радио-опции квиза используют акцент темы.
- **Инвариант:** Цвета успешного выполнения (`emerald-500`) и ошибок (`rose-500`) остаются строго неизменными.

Gate: `python -m pytest tests/test_theme_system.py -k test_practice_quiz_theme_tokens`  
Evidence: Проверка шаблонов практики и квиза на соответствие токенам темы.

---

### AC-3: Миграция страницы итогового экзамена (`exam.html`)

В `exam.html`:
- Карточка регламента, инструкция, бейджи частей экзамена и рамки редактора используют семантические переменные темы.
- Бейджи статуса экзамена сохраняют смысловую дифференциацию (золото/янтарь для экзамена, изумруд для 100% зачета курса).
- В режиме `Clean` на странице экзамена отсутствуют неоновые ореолы вокруг кнопок и панелей задач.

Gate: `python -m pytest tests/test_theme_system.py -k test_exam_page_theme_tokens`  
Evidence: Проверка `exam.html` на корректную интеграцию переменных темы.

---

### AC-4: Полная адаптация навигации и пилюль в `header.html`

В `header.html`:
- Стили активных пилюль недель (`.week-pill-active`) используют динамический градиент и рамку из `var(--theme-primary)` и `var(--theme-border)`.
- Активные подтабы (`.subtab-active`) динамически окрашиваются в акцент выбранной темы вместо жесткого синего.
- Селектор студентов и сворачиваемая шапка сохраняют идеальную контрастность во всех 4 палитрах.

Gate: `python -m pytest tests/test_theme_system.py -k test_header_navigation_theme_tokens`  
Evidence: Проверка стилей и классов навигации.

---

### AC-5: Адаптация обвязки и лупы `uml_viewer.html`

В `uml_viewer.html`:
- Панель управления (кнопки зума, сброса, переключения схем), рамка лупы `#uml-lens`, фоновая сетка вьювера и модальное окно полноэкранного просмотра используют `var(--theme-accent)` и `var(--theme-border)`.
- **Инвариант:** Внутренние SVG-градиенты и цвета нод классов (синий, зеленый, желтый, пурпурный в Clean Architecture) остаются нетронутыми.

Gate: `python -m pytest tests/test_theme_system.py -k test_uml_viewer_shell_theme_tokens`  
Evidence: Внешняя обвязка вьювера адаптирована, внутренние диаграммы сохранены.

---

### AC-6: Миграция динамической генерации разметки в `app.js`

В `app/static/js/app.js`:
- Классы `text-sky-400`, `bg-sky-500/20`, `border-sky-400` в динамически создаваемых строках HTML (выбор опции квиза, активный подтаб, уведомление о заблокированной неделе) заменены на семантические классы темы или ссылки на переменные.
- Статусные классы `bg-emerald-500/15`, `bg-rose-500/15` сохранены без изменений.

Gate: `python -m pytest tests/test_theme_system.py -k test_app_js_dynamic_theme_tokens`  
Evidence: Проверка кода `app.js` на отсутствие жестких классов `sky-` в динамическом HTML.

---

### AC-7: Сквозная регрессионная верификация всех тестов платформы

- Все тесты из `tests/test_health.py`, `tests/test_ui_ergonomics.py`, `tests/test_exam.py`, `tests/test_week*.py`, `tests/test_theme_system.py` (67+ тестов) успешно проходят со 100% результатом.
- Ни один визуальный или функциональный ассерт не нарушен.

Gate: `pytest tests/ -q`  
Evidence: 100% зелёный результат прогона тестового набора.

---

### Evidence Artifacts

| File | Description |
|---|---|
| `evidence/EV__phase-b__template_and_script_migration_to_semantic_theme_tokens.md` | Структурированный отчёт проверки критериев AC-1 — AC-7 |

---

## 6. Technical Guidance

- В `style.css` дополнить правила:
  ```css
  .theme-accent-text { color: var(--theme-accent); }
  .theme-accent-bg { background-color: var(--theme-primary); }
  .theme-border { border-color: var(--theme-border); }
  .week-pill-active {
      background: linear-gradient(135deg, var(--theme-border), rgba(15, 23, 42, 0.9));
      border: 1px solid var(--theme-accent);
      color: var(--theme-accent);
      box-shadow: var(--theme-glow-shadow);
  }
  .subtab-active {
      background: var(--theme-border);
      border: 1px solid var(--theme-accent);
      color: var(--theme-accent);
      box-shadow: var(--theme-glow-shadow);
  }
  ```
- В `app.js` для динамических кнопок использовать классы `.subtab-active` и `.theme-accent-text` вместо жесткого `text-sky-400`.
- В `tab_practice.html` разделитель колонок `.practice-split-resizer:hover` привязать к `var(--theme-accent)` и `var(--theme-glow)`.

---

## 7. Definition of Failure

- ❌ Наличие остаточных жестких классов `sky-400` в активных табах или обзоре тем.
- ❌ Поломка отображения архитектурных слоев в `uml_viewer.html`.
- ❌ Ошибки тестов эргономики в `test_ui_ergonomics.py`.
- ❌ Слияние цветов PASS/FAIL при тестировании кода студентов.

---

## 8. Phase Risks

| Risk | Mitigation |
|---|---|
| Падение тестов `test_ui_ergonomics.py`, проверяющих точные строки `style.css` | Сохранить совместимость селекторов (`.week-pill-active`, `.subtab-active`, `.cyber-card`) при обновлении их свойств до `var(--theme-*)` |

---

## 9. Cross-Phase Modifications

- Завершающая фаза задачи `OOP_20261030-021700_THEME`. После успешной приёмки Phase B задача переходит к финальной квалификации знаний и закрытию.

---

*TS — OOP_20261030-021700_THEME / Phase B: Template and Script Migration to Semantic Theme Tokens | 2026-10-30*
