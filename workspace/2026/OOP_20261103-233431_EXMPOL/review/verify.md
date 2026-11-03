# Verify — "Do the material claims hold?"
> **Mindset:** Auditor. RF is a declaration, not a fact. Open files, run necessary checks, compare
> accepted claims with reality, and state the limits.
> **Test:** "Would the evidence establish this claim for this subject, revision and environment without RF?"
> Map: [map.md](map.md)

## Selection Argument

| Claim IDs | Risk / criticality | Affected behavior / dependencies | Environment | Oracle / authority | Evidence gap / limit | Selected verification and why |
|---|---|---|---|---|---|---|
| C1 | High (дизайн-система) | Стили карточек, скроллбаров и режим Clean | Web-браузер, FastAPI | TS AC-1, HL §5 DoD-1, DoD-2 | Нет | Статический аудит `app/static/css/style.css` и `pytest tests/test_theme_system.py -k "css"` |
| C2 | High (UX/UI экзамена) | Вёрстка `/exam`, шапка, палитры | Jinja2, TestClient | TS AC-2, HL §5 DoD-1, DoD-2 | Безголовая среда (нет GUI браузера) | Инспекция разметки `exam.html`, `header.html` и `pytest tests/test_theme_system.py` |
| C3 | Critical (академическая честность) | Режим No-Cheat в песочнице экзамена | JS Runtime | TS AC-3, HL §5 DoD-3, HL §6 DoF-1 | Нет | Аудит ветвления в `app.js` и `pytest tests/test_exam.py -k "ui_integrity"` |
| C4 | Medium (архитектура) | Навигация по 5 UML-диаграммам и лупа | Jinja2, JS | TS AC-4, HL §5 DoD-4, HL §6 DoF-2 | Нет | Инспекция кнопок в `uml_viewer.html`, неизменности `<svg>` и `pytest tests/test_exam.py` |
| C5 | Medium (эргономика квиза) | Счётчик 0/20, защита от HTTP 422, скролл | Fetch API, JS | TS AC-5, HL §5 DoD-5 | Нет | Проверка разметки `exam.html` и логики функций отправки в `app.js` |
| C6 | High (реактивность ведомости) | Живые статусы без перезагрузки F5 | DOM JS | TS AC-6, HL §5 DoD-6, HL §7 P2 | Нет | Проверка наличия всех 10 ID и логики `updateProgressUI` в `app.js` |
| C7 | Critical (качество и целостность) | 73 теста платформы | Pytest 9.1.1 | TS AC-7, HL §5 DoD-7, HL §6 DoF-3 | Время прогона ~44 сек | Полный независимый запуск `python -m pytest -q` |
| C8 | High (трассировка и бюджет) | Бюджет 5 файлов VALUE, 289 LOC | Git | TS §4, conventions.md | Нет | NUL-safe `git diff --numstat` и `--name-status` между `bdbed49` и `822e7ac` |
| C9 | Medium (экономика роли) | Учёт токенов и времени роли | JSONL, SHA-256 | TFW Economics | Нет | Проверка файла `economics/roles/*.jsonl` и сверка хэша SHA-256 |

## Verification Log

### V1: C1 — Ядро стилей `style.css` (токены, скроллбары, `.theme-accent-bg`, режим Clean)
- **Accepted claim / authority:** `style.css` переводит `.cyber-card` и `.overflow-x-auto` на токены темы, добавляет `.theme-accent-bg` и гасит `.exam-clean-no-glow` и `.theme-btn-secondary` в режиме Clean.
- **Subject tuple:** `app/static/css/style.css`, Candidate `822e7ac`, Windows/Python 3.12, TS AC-1 / HL DoD-1 / DoD-2, stable.
- **Action or evidence:** Инспекция `git diff bdbed49...822e7ac -- app/static/css/style.css` и запуск `pytest tests/test_theme_system.py -k "css"`.
- **Observed:** В `.cyber-card` задано `border: 1px solid var(--theme-border);`, в `.overflow-x-auto` ползунок и дорожка используют `var(--theme-border)` и `var(--theme-accent)`. Добавлен класс `.theme-accent-bg { background-color: var(--theme-accent) !important; }`. В `[data-glow="clean"]` добавлены `.theme-btn-secondary` и `.exam-clean-no-glow` с `box-shadow: none !important;`. Тесты `test_css_theme_variables` и `test_css_glow_modes` пройдены (PASSED).
- **Limit:** Визуальное отображение в реальных графических браузерах верифицировано через структурные CSS-свойства и тесты токенов.
- **Result:** HOLDS

### V2: C2 — Гармонизация неоновых палитр и режима Clean в `exam.html` и `header.html`
- **Accepted claim / authority:** Каркас `/exam` и шапка подчиняются палитрам темы и режиму Clean, код в IDE использует нейтральный `text-slate-100`, смысловой `amber` сохранён на знаках аттестации.
- **Subject tuple:** `app/templates/exam.html`, `app/templates/components/header.html`, Candidate `822e7ac`, TS AC-2 / HL DoD-1 / DoD-2, stable.
- **Action or evidence:** Инспекция разметки и diff файлов; запуск `pytest tests/test_theme_system.py -k "exam_page_theme_tokens or header_navigation_theme_tokens"`.
- **Observed:** В `exam.html` Hero-блок, кнопки CTA, рамки секций, бейджи и карточка сертификата используют семантические токены (`theme-btn-primary`, `theme-btn-secondary`, `theme-badge`, `theme-border`, `exam-clean-no-glow`). В редакторе кода `text-amber-100` заменён на `text-slate-100`. Смысловой `amber` сохранён на плашке честности `🛡️`, карточке экзаменационного балла и кнопке подсказки `💡`. В `header.html` активная вкладка `/exam` избавлена от конфликтующего жёлто-розового градиента и использует `week-pill-active font-bold`, бейдж `40 б.` использует `theme-badge`, а стартовая подвкладка «Инструкция и Регламент» переведена на `theme-accent-text`. Тесты пройдены (PASSED).
- **Limit:** Безголовая среда (нет GUI браузера).
- **Result:** HOLDS

### V3: C3 — Честный контекстный вердикт песочницы на экзамене (No-Cheat Mode)
- **Accepted claim / authority:** При неудаче запуска кода в песочнице на странице экзамена не выводится совет «попробуйте готовое решение», а предлагается проверить контракты и подсказку `💡`.
- **Subject tuple:** `app/static/js/app.js`, Candidate `822e7ac`, TS AC-3 / HL DoD-3 / DoF-1, stable.
- **Action or evidence:** Анализ ветвления в `runPracticeTask` (`app.js:435–439`) и запуск `pytest tests/test_exam.py -k "ui_integrity"`.
- **Observed:** При `ACTIVE_WEEK === "exam"` выводится строго: `❌ ТЕСТЫ НЕ ПРОЙДЕНЫ (${data.status}) — ПРОВЕРЬТЕ КОНТРАКТЫ И ИНВАРИАНТЫ (СМ. ПОДСКАЗКУ 💡)`. Для обучающих недель (`ACTIVE_WEEK !== "exam"`) сохранён исходный текст с готовым решением. В HTML экзамена нет кнопок или вызовов вставки готового решения. Тест пройден (PASSED).
- **Limit:** None.
- **Result:** HOLDS

### V4: C4 — Доступ ко всем 5 UML-диаграммам курса на `/exam` и семантическая лупа
- **Accepted claim / authority:** На странице `/exam` рендерятся 5 вкладок диаграмм (`week1`, `week2`, `week3`, `arch`, `db`), графы `<svg>` не затронуты, кнопка лупы переведена на токены темы.
- **Subject tuple:** `app/templates/components/uml_viewer.html`, `app/static/js/app.js`, Candidate `822e7ac`, TS AC-4 / HL DoD-4 / DoF-2, stable.
- **Action or evidence:** Инспекция `uml_viewer.html` (строки 100–185) и `app.js` (`currentUmlTab`, `toggleUmlLens`); запуск `pytest tests/test_exam.py -k "ui_integrity"` и `pytest tests/test_theme_system.py -k "app_js"`.
- **Observed:** Блок кнопок переключения вкладок содержит ветку `{% if active_week == 'exam' %}` с 5 кнопками `week1`, `week2`, `week3`, `arch`, `db`. Векторные графы `<svg>` ниже строки 210 не изменялись (`git diff` пуст). В `app.js` переменная `currentUmlTab` инициализируется значением `"week3"` для экзамена, а в `toggleUmlLens()` жёсткий `bg-cyan-500/20` заменён на `theme-glow-card theme-accent-text bg-slate-900`. Тесты пройдены (PASSED).
- **Limit:** None.
- **Result:** HOLDS

### V5: C5 — Эргономика квиза (счётчик, защита от пустой отправки, автоскролл)
- **Accepted claim / authority:** В нижней панели квиза отображается живой счётчик ответов `#quiz-answered-counter`, при 0 ответов запрос не отправляется, после получения результата страница плавно скроллится к баннеру.
- **Subject tuple:** `app/templates/exam.html`, `app/static/js/app.js`, Candidate `822e7ac`, TS AC-5 / HL DoD-5, stable.
- **Action or evidence:** Инспекция разметки `#quiz-answered-counter` в `exam.html` и логики `selectQuizOption`, `submitExamQuiz`, `submitWeek1Quiz` в `app.js`.
- **Observed:** В `exam.html` добавлен `<span id="quiz-answered-counter" class="text-xs font-mono text-slate-400">Выбрано ответов: 0 / 20</span>`. В `selectQuizOption` динамически пересчитывается количество ответов и обновляется текст/класс счётчика. В обеих функциях отправки квиза при `Object.keys(quizSelections).length === 0` отправка отменяется, в баннере выводится предупреждающее сообщение и вызывается `scrollIntoView({ behavior: "smooth", block: "nearest" })`. При успешной проверке кнопка перехода в ведомость использует `theme-btn-primary` и также вызывается плавный автоскролл.
- **Limit:** None.
- **Result:** HOLDS

### V6: C6 — Реактивность Итоговой Ведомости и Сертификата без F5 (Zero-F5)
- **Accepted claim / authority:** 10 реактивных DOM ID присутствуют в `exam.html` и динамически обновляются в `updateProgressUI` при любом изменении баллов без перезагрузки страницы.
- **Subject tuple:** `app/templates/exam.html`, `app/static/js/app.js`, Candidate `822e7ac`, TS AC-6 / HL DoD-6 / HL P2, stable.
- **Action or evidence:** Проверка DOM ID в `exam.html` и логики обновления в `app.js:805–863`; запуск `pytest tests/test_exam.py -k "ui_integrity"`.
- **Observed:** Все 10 ID (`#results-grade-letter`, `#table-w1-status`, `#table-w2-status`, `#table-w3-status`, `#table-quiz-status`, `#table-tasks-status`, `#table-exam-status`, `#cert-status-badge`, `#cert-grand-total`, `#cert-grade-letter`) присутствуют в шаблоне. Функция `updateProgressUI` обновляет текстовые значения и переключает классы бейджей (`Зачет`/`В процессе`, `Пройден`/`В процессе`, `Сдан (>=20 б.)`/`В процессе`, `ВЕДОМОСТЬ ПОДТВЕРЖДЕНА (100%)`/`ОЖИДАЕТ СДАЧИ ЭКЗАМЕНА`). Тест пройден (PASSED).
- **Limit:** None.
- **Result:** HOLDS

### V7: C7 — Комплексное покрытие автотестами и отсутствие регрессий
- **Accepted claim / authority:** Все существующие и новые тесты проходят со 100% успехом (73 passed).
- **Subject tuple:** Полный репозиторий `web-oop`, Candidate `822e7ac`, Pytest 9.1.1 / Python 3.12.9, TS AC-7 / HL DoD-7 / DoF-3, stable.
- **Action or evidence:** Независимый запуск `python -m pytest -q` в рабочей директории.
- **Observed:** `73 passed, 1 warning in 43.10s`. Полное отсутствие регрессий. Все тестовые сценарии недель 1–3, экзамена, роутеров, сервисов и дизайн-системы завершились успешно.
- **Limit:** Единственное предупреждение относится к устареванию `starlette.testclient` в пользу `httpx2` и не является дефектом кода проекта.
- **Result:** HOLDS

### V8: C8 — Бухгалтерия скоупа VALUE и знаменатель TS
- **Accepted claim / authority:** Изменены строго 5 файлов `VALUE`, количество затронутых строк укладывается в утверждённый знаменатель и лимиты.
- **Subject tuple:** Git commit history, Baseline `bdbed49`, Candidate `822e7ac`, TS §4, stable.
- **Action or evidence:** Независимый расчет через `git diff --name-status` и `git diff --numstat` для утвержденного селектора `VALUE`.
- **Observed:** Изменены строго 5 файлов: `style.css` (+11, -5), `app.js` (+96, -4), `header.html` (+6, -6), `uml_viewer.html` (+87, -1), `exam.html` (+37, -36). Сумма: 237 добавлений + 52 удаления = 289 затронутых строк LOC. Укладывается в owner escalation multiplier 2x (до 480 строк от плана 240). Базовый коммит `bdbed49`, коммит кандидата `822e7ac`.
- **Limit:** None.
- **Result:** HOLDS

### V9: C9 — Экономика роли Исполнителя
- **Accepted claim / authority:** Зафиксирован валидный JSONL с метриками потребления, хэш SHA-256 совпадает.
- **Subject tuple:** `workspace/2026/OOP_20261103-233431_EXMPOL/economics/roles/aba60efaae92de02ea24626459908ef1447c5a70bf72d3a29f24446e9ca86c0d.jsonl`.
- **Action or evidence:** Проверка существования, чтение строк манифеста и вычисление SHA-256 через `Get-FileHash`.
- **Observed:** SHA-256 равен `ABA60EFAAE92DE02EA24626459908EF1447C5A70BF72D3A29F24446E9CA86C0D`. 4 записи агрегированного потребления (Claude Opus 5.5 и Gemini 3.8 Flash) с `complete: true`.
- **Limit:** None.
- **Result:** HOLDS

## Commands Executed

| # | Command | Claim IDs | Result |
|---|---|---|---|
| 1 | `python -m pytest tests/test_theme_system.py tests/test_exam.py -v` | C1, C2, C3, C4, C6, C7 | Exit 0, 18 passed in 5.45s |
| 2 | `python -m pytest -q` | C7 | Exit 0, 73 passed in 43.10s |
| 3 | `git diff --name-status bdbed49... 822e7ac...` | C8 | Exit 0, 5 файлов VALUE, 2 ASSURANCE, артефакты TRACE |
| 4 | `git diff --numstat bdbed49... 822e7ac... -- $valuePaths` | C8 | Exit 0, 237 additions, 52 deletions = 289 touched LOC |
| 5 | `Get-FileHash ...aba60efaae92...jsonl -Algorithm SHA256` | C9 | Exit 0, SHA256 совпадает с именем файла |

## Claim and Source Checks

| # | Claim / citation | Where | Primary artifact / source | Holds? |
|---|---|---|---|---|
| C1 | `style.css` переведён на токены темы и гасит тени в Clean | RF §1, EV E1 | `app/static/css/style.css` | ✅ Holds |
| C2 | `/exam` каркас подчиняется теме, нейтральный код slate-100 | RF §1, EV E2 | `app/templates/exam.html` | ✅ Holds |
| C3 | No-Cheat режим в вердикте песочницы на экзамене | RF §1, EV E3 | `app/static/js/app.js:435` | ✅ Holds |
| C4 | 5 вкладок UML на `/exam`, SVG не тронуты, лупа в теме | RF §1, EV E4 | `app/templates/components/uml_viewer.html`, `app.js` | ✅ Holds |
| C5 | Живой счётчик квиза, 0-защита, автоскролл к результату | RF §1, EV E5 | `exam.html`, `app.js` | ✅ Holds |
| C6 | 10 реактивных DOM ID ведомости и сертификата (Zero-F5) | RF §1, EV E6 | `exam.html`, `app.js` | ✅ Holds |
| C7 | Полный прогон тестов 73/73 green | RF §4, EV E7 | `python -m pytest -q` | ✅ Holds |
| C8 | Бухгалтерия 5 файлов VALUE, 289 LOC, Baseline `bdbed49`, Candidate `822e7ac` | RF §1, EV E-accounting | `git diff --numstat` | ✅ Holds |
| C9 | JSONL экономики роли зафиксирован с валидным SHA-256 | RF §5, EV §5 | `economics/roles/*.jsonl` | ✅ Holds |

## Guard and Check Admission

| # | Kind | Protected behavior / invariant | Failure consequence | Counterfactual detection | Admission |
|---|---|---|---|---|---|
| G1 | permanent guard | `test_exam_ui_integrity`: все 5 вкладок UML, 10 реактивных ID, No-Cheat вердикт | Нарушение академической честности, рассинхронизация ведомости | Негативный контроль: удаление ID или No-Cheat текста роняет тест | Admitted |
| G2 | permanent guard | `test_exam_page_theme_tokens`: семантические классы темы, `text-slate-100`, отсутствие `amber-100` и `border-indigo` | Визуальный хаос при смене неоновых тем | Контроль отсутствия: проверка `not in content` для устаревших классов | Admitted |
| G3 | permanent guard | `test_css_glow_modes`: гашение свечения `.exam-clean-no-glow` и `.theme-btn-secondary` в Clean | Размытые неоновые ореолы в строгом режиме Clean | Проверка наличия селекторов в правиле `[data-glow="clean"]` | Admitted |
| G4 | positive control | `test_multi_student_isolation_and_exam_endpoints`: эндпоинты `/week1`..`/exam` возвращают 200 | Поломка серверного роутинга | Позитивный HTTP-контроль доступности | Labelled control |
| G5 | governance assertion | Бухгалтерский учет строк VALUE (289 LOC < 480 LOC) | Разрастание скоупа задачи | Числовая проверка Git diff | Governance only |

## Candidate Findings

No findings.

## Evidence Verification

| # | EV row | Subject tuple | Repeated or opened? | Establishes the claim? | Limit |
|---|---|---|---|---|---|
| E1 | E1 | `style.css@822e7ac`, Windows/Py3.12, TS AC-1 | Repeated (pytest + inspect) | ✅ Establishes | Безголовая среда |
| E2 | E2 | `exam.html@822e7ac`, `header.html@822e7ac`, TS AC-2 | Repeated (pytest + inspect) | ✅ Establishes | Безголовая среда |
| E3 | E3 | `app.js@822e7ac`, TS AC-3, No-Cheat | Repeated (pytest + inspect) | ✅ Establishes | None |
| E4 | E4 | `uml_viewer.html@822e7ac`, `app.js@822e7ac`, TS AC-4 | Repeated (pytest + inspect) | ✅ Establishes | None |
| E5 | E5 | `exam.html@822e7ac`, `app.js@822e7ac`, TS AC-5 | Repeated (inspect) | ✅ Establishes | None |
| E6 | E6 | `exam.html@822e7ac`, `app.js@822e7ac`, TS AC-6 | Repeated (pytest + inspect) | ✅ Establishes | None |
| E7 | E7 | Полный репозиторий, Candidate `822e7ac`, TS AC-7 | Repeated (pytest -q, 73 passed) | ✅ Establishes | Starlette warning |
| E8 | E-accounting | Git commit history, Baseline `bdbed49`, Candidate `822e7ac` | Repeated (numstat replay) | ✅ Establishes | None |

## Knowledge Citations Verified

| # | Artifact | Priority + exact citation | Resolves? | Item exists? | Meaning matches? | Relevant? |
|---|---|---|---|---|---|---|
| 1 | HL §7.2 #1 | PV Priority 0 — `README.md § Цель и North Star проекта` | ✅ | ✅ | ✅ — цель: локальная интерактивная мини-LMS с 40-балльным экзаменом | ✅ — подтверждает целевое назначение экзамена и ведомости |
| 2 | HL §7.2 #2 | PV Priority 1 — `.tfw/README.md #ns1, #ns2, #methodology-values` | ✅ | ✅ | ✅ — принцип Сент-Экзюпери, Candor Over Flattery, Structural Enforcement | ✅ — точечные правки без дублирования, закрепление инвариантов тестами |
| 3 | HL §7.2 #3 | PV Priority 2 — `knowledge/philosophy.md` | ✅ | N/A (отсутствует) | ✅ — зафиксировано в HL как N/A | ✅ — отражено как N/A |
| 4 | HL §7.2 #4 | PV Priority 3 — `KNOWLEDGE.md §1 D5, D11` | ✅ | ✅ | ✅ — Zero-Build архитектура, эргономичный IDE-тренажёр | ✅ — нейтральный `slate-100`, сохранение Vanilla JS/CSS |
| 5 | HL §7.2 #5 | PV Priority 3 — `KNOWLEDGE.md §1 D13` + `REC-OOP_20261029-200322_EXAM-tech-*` | ✅ | ✅ | ✅ — No-Cheat Mode, 100-балльная шкала аттестации | ✅ — устранение ложного готового решения на экзамене |
| 6 | HL §7.2 #6 | PV Priority 3 — `KNOWLEDGE.md §1 D14` + `REC-OOP_20261030-021700_THEME-tech-*` | ✅ | ✅ | ✅ — 4 палитры, режим Clean/Cyberpunk, неприкосновенность PASS/FAIL | ✅ — гармонизация `/exam` с токенами `--theme-*` |
| 7 | HL §7.2 #7 | PV Priority 4 — `.tfw/conventions.md §3, §6, §7, §15` | ✅ | ✅ | ✅ — Role Lock, правила классификации VALUE/ASSURANCE/TRACE, знаменатель | ✅ — соблюдение Role Lock Reviewer, учет строк Git |
| 8 | HL §7.2 #8 | PV Priority 5–7 — `KNOWLEDGE.md §4 F9, F11` + `REC-...-human-*` | ✅ | ✅ | ✅ — педагогический стандарт квизов, итоговая аттестация | ✅ — доступ ко всем UML, живой счётчик, Zero-F5 ведомость |

## Accounting Replay

| Approval / authority | Baseline | Candidate | Literal VALUE membership / actions / classes / reasons | Adds | Deletes | Touched LOC | Binary | Trigger disposition | Exact NUL-safe command | Verdict |
|---|---|---|---|---:|---:|---:|---|---|---|---|
| TS §4 @ `9f70024`, Journal `7b2a` | `bdbed49103f62960b5e73655b5a25ec4b764c464` | `822e7ac01cfd6ac14a06386dba5b4d8d5b67ca4c` | `app/static/css/style.css`, `app/templates/exam.html`, `app/templates/components/header.html`, `app/templates/components/uml_viewer.html`, `app/static/js/app.js` (5 MODIFY, VALUE) | 237 | 52 | 289 | N/A | Пороги 50/5000 соблюдены (>90% запас), укладывается в 2x multiplier (480 LOC) | `git diff --numstat bdbed49... 822e7ac... -- $valuePaths` | VERIFIED |

## Selected Knowledge Evidence

- Исполнитель добросовестно выполнил все предписания спецификации `TS`, не допустив расширения списка файлов `VALUE`.
- Выявленное Исполнителем наблюдение по строке 7 `uml_viewer.html` зафиксировано в RF §6 без нарушения границ скоупа.
- Все 8 пунктов EV подтверждены независимым аудитом и повторными прогонами.

## Checkpoint

**Self-check:**
- [x] Replayed the Map selection and verified all mandatory safety/security, authority and identity floors?
- [x] Established evidence applicability and ran every TS-required or dependency-affected check?
- [x] Recorded explicit limits instead of substituting file, discrepancy, test, commit or artifact counts?
- [x] Classified guards and controls by protected behavior, consequence and counterfactual detection?
- [x] Recorded every candidate finding with the complete item contract and material consequence test?
- [x] Verified RF AC claims, evidence references, citations and immutable accounting against actual artifacts?

Stage complete: YES
