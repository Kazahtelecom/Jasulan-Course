# Map — "What must be true?"
> **Mindset:** Experienced newcomer. Understand the accepted result before judging it.
> **Test:** "Can I name the material claims, harms, boundaries, evidence identities and limits?"
> RF: [RF__OOP_20261103-233431_EXMPOL.md](../RF__OOP_20261103-233431_EXMPOL.md)
> TS: [TS__OOP_20261103-233431_EXMPOL.md](../TS__OOP_20261103-233431_EXMPOL.md)

## Understanding

В задаче `OOP_20261103-233431_EXMPOL` устранены 7 визуальных и UX-дефектов модуля итогового экзамена (`/exam`) и компонентов дизайн-системы: страница экзамена адаптирована под 4 неоновые палитры и строгий режим `Clean` без свечения (при сохранении семантического янтаря `amber` для знаков отличия аттестации и подсказок); устранены ложные упоминания готового решения в песочнице экзамена (No-Cheat); открыты все 5 вкладок UML-диаграмм на `/exam`; добавлен живой счётчик ответов, защита от пустой отправки и автоскролл в квизе; обеспечено 100% реактивное обновление ведомости и сертификата (Zero-F5). Все изменения локализованы в 5 файлах `VALUE` и проверены автотестами в 2 файлах `ASSURANCE` без модификации схемы БД, API бэкенда или Zero-Build архитектуры.

## Accepted Claims and Boundaries

| ID | Layer | Accepted claim / authority boundary | Risk or concrete harm | Affected behavior / dependencies | Relevant environment | Oracle / authority | Evidence identity (`subject@revision`, source) | Required? |
|---|---|---|---|---|---|---|---|---|
| C1 | VALUE | `app/static/css/style.css`: утилита `.theme-accent-bg`, `.cyber-card` и `.overflow-x-auto` привязаны к токенам темы, `[data-glow="clean"]` гасит `.theme-btn-secondary` и `.exam-clean-no-glow` | Визуальный разнобой в темах, утечка неоновых теней в режиме Clean | Глобальные карточки, скроллбары, кнопки и элементы с классом `.exam-clean-no-glow` | Web-браузер, FastAPI статика | TS AC-1, HL §5 DoD-1, DoD-2 | `app/static/css/style.css@822e7ac`, EV E1 | yes |
| C2 | VALUE | `app/templates/exam.html` и `header.html`: каркас `/exam` подчиняется активной теме и режиму `Clean`, `text-slate-100` в редакторе, при сохранении смыслового `amber` на плашке честности и баллах | Нарушение гармонии неоновых тем или регрессия теста `test_exam_page_theme_tokens` | Рендеринг `/exam` и шапки во всех 4 палитрах и обоих режимах свечения | FastAPI Jinja2, TestClient | TS AC-2, HL §5 DoD-1, DoD-2 | `app/templates/exam.html@822e7ac`, `app/templates/components/header.html@822e7ac`, EV E2 | yes |
| C3 | VALUE | `app/static/js/app.js`: в `runPracticeTask` для `ACTIVE_WEEK === "exam"` текст ошибки не содержит слов «готовое решение» (No-Cheat Mode) | Введение студентов в заблуждение, нарушение академической честности F11/D13 | Обработка вердикта неудачного запуска кода песочницы на `/exam` | Браузерный JS runtime | TS AC-3, HL §5 DoD-3, HL §6 DoF-1 | `app/static/js/app.js@822e7ac`, EV E3 | yes |
| C4 | VALUE | `app/templates/components/uml_viewer.html` и `app.js`: на `/exam` рендерятся 5 вкладок диаграмм (`week1`..`week3`, `arch`, `db`), активная лупа использует токены темы | Студенты не могут изучить архитектуру Недель 1 и 2 на экзамене, кнопка лупы жёстко циановая | Вкладки UML-просмотрщика, кнопка лупы | FastAPI Jinja2, Vanilla JS | TS AC-4, HL §5 DoD-4, HL §6 DoF-2 | `app/templates/components/uml_viewer.html@822e7ac`, `app/static/js/app.js@822e7ac`, EV E4 | yes |
| C5 | VALUE | `exam.html` и `app.js`: живой счётчик `#quiz-answered-counter`, защита пустой отправки (0 ответов) без HTTP 422, автоскролл к `#quiz-result-banner` | Ошибки 422 в сети, плохой UX на длинном полотне из 20 вопросов | Выбор вариантов и отправка квиза на экзамене и неделях | Браузерный JS / Fetch API | TS AC-5, HL §5 DoD-5 | `app/templates/exam.html@822e7ac`, `app/static/js/app.js@822e7ac`, EV E5 | yes |
| C6 | VALUE | `exam.html` и `app.js`: 10 реактивных DOM ID, `updateProgressUI` обновляет статусы ведомости, букву оценки и сертификат без перезагрузки (Zero-F5) | Рассинхронизация ведомости и сертификата с реальными баллами до ручного F5 | Отображение итогов сессии в реальном времени | Браузерный JS DOM | TS AC-6, HL §5 DoD-6, HL §7 P2 | `app/templates/exam.html@822e7ac`, `app/static/js/app.js@822e7ac`, EV E6 | yes |
| C7 | ASSURANCE | Тестовый набор расширен и проходит на 100% без регрессий (73/73 passed) | Скрытые функциональные или визуальные поломки в учебных модулях | Все модули платформы: `/week1`, `/week2`, `/week3`, `/exam`, API | Pytest, TestClient | TS AC-7, HL §5 DoD-7, HL §6 DoF-3 | `tests/test_theme_system.py@822e7ac`, `tests/test_exam.py@822e7ac`, EV E7 | yes |
| C8 | TRACE | Знаменатель, учет файлов VALUE (5 файлов, 289 строк < 480 escalation ceiling), Baseline `bdbed49`, Candidate `822e7ac`, неизменный знаменатель | Потеря контроля над скоупом, искажение метрик | Git история, TFW артефакты | Git commit history | TS §4, conventions.md | EV E-accounting, RF §1, ONB §2 | yes |
| C9 | TRACE | Ресурсная экономика роли Исполнителя зафиксирована в task-local JSONL с валидным SHA-256 | Непрозрачность расхода ресурсов, нарушение полноты TFW Economics | Артефакты экономики | Antigravity conversation DB | conventions.md, .tfw/economics/README.md | `economics/roles/aba60efaae92de02ea24626459908ef1447c5a70bf72d3a29f24446e9ca86c0d.jsonl` | yes |

## TS ↔ RF Alignment

| TS requirement | RF claim | Claim IDs | Aligned? |
|---|---|---|---|
| AC-1 (Ядро стилей style.css) | RF §1, §3 AC-1, §5 E1 | C1 | ✅ Aligned |
| AC-2 (Гармонизация exam.html и header.html) | RF §1, §3 AC-2, §5 E2 | C2 | ✅ Aligned |
| AC-3 (No-Cheat вердикт песочницы на экзамене) | RF §1, §3 AC-3, §5 E3 | C3 | ✅ Aligned |
| AC-4 (5 вкладок UML и лупа в теме) | RF §1, §3 AC-4, §5 E4 | C4 | ✅ Aligned |
| AC-5 (Счётчик квиза, 0-защита, автоскролл) | RF §1, §3 AC-5, §5 E5 | C5 | ✅ Aligned |
| AC-6 (Zero-F5 реактивность ведомости и сертификата) | RF §1, §3 AC-6, §5 E6 | C6 | ✅ Aligned |
| AC-7 (Комплексное покрытие автотестами) | RF §1, §3 AC-7, §4, §5 E7 | C7 | ✅ Aligned |
| TS §4 Accounting (5 файлов VALUE, лимиты строк) | RF §1 Actual Accounting, EV E-accounting | C8 | ✅ Aligned |
| DoD-1..DoD-7 | RF §1, §3, §4, §5 | C1–C7 | ✅ Aligned |
| DoF-1..DoF-4 | RF §1, §2, §4, §5 | C1–C7 | ✅ Aligned |

## Verification Selection

| Claim IDs | Planned check or reusable evidence | Why this depth | Known gap or limit |
|---|---|---|---|
| C1 | Независимый статический аудит `app/static/css/style.css` и повторный прогон `pytest tests/test_theme_system.py -k "css"` | Критично для всех страниц и палитр темы | Браузерный рендеринг проверяется через CSS селекторы и токены |
| C2 | Независимый аудит `app/templates/exam.html` и `header.html`, запуск `pytest tests/test_theme_system.py` | Проверка гармонии темы, отсутствия `amber-100`, сохранения смыслового `amber` | Безголовая среда (нет GUI браузера) |
| C3 | Аудит ветвления `ACTIVE_WEEK === "exam"` в `app/static/js/app.js` и запуск `pytest tests/test_exam.py -k "ui_integrity"` | Инвариант академической честности (No-Cheat, D13/F11) | Нет |
| C4 | Проверка разметки кнопок в `app/templates/components/uml_viewer.html`, неизменности графов `<svg>` и `currentUmlTab` в `app.js` | Исключить регрессию SVG и гарантировать доступ ко всем 5 схемам | Нет |
| C5 | Проверка `#quiz-answered-counter` в `exam.html`, логики `selectQuizOption`, `submitExamQuiz` и `submitWeek1Quiz` в `app.js` | UX тестирования и предотвращение ошибок 422 | Нет |
| C6 | Проверка наличия всех 10 реактивных ID в `exam.html` и логики `updateProgressUI` в `app.js` | Гарантия Zero-F5 реактивности без рассинхронизации DOM | Нет |
| C7 | Независимый запуск полного набора автотестов `pytest` в репозитории | Подтверждение отсутствия регрессий во всех 73 тестах | Занимает ~45 секунд |
| C8 | Независимый расчет git diff (`--name-status` и `--numstat`) между Baseline `bdbed49` и Candidate `822e7ac` | Проверка соблюдения границ скоупа и неизменного знаменателя TS | Нет |
| C9 | Проверка наличия JSONL экономики, соответствия хэша SHA-256 и полноты записей | Требование TFW Economics | Нет |

## Deviations from TS

No deviations.
Реализация строго соответствует спецификации TS. Исполнитель добросовестно зафиксировал наблюдение по строке 7 `uml_viewer.html` (инлайновая тень вне разрешённого TS диапазона строк), не став самовольно выходить за утверждённые границы правок.

## Checkpoint

**Self-check:**
- [x] Read RF §§1–5, governing TS AC/DoF, HL purpose/principles, ONB and referenced predecessors?
- [x] Mapped every material accepted claim and the mandatory safety/security, authority and result-identity boundaries?
- [x] Bound each claim to affected behavior/dependencies, environment, oracle/authority and exact evidence identity?
- [x] Recorded a replayable verification selection and every known gap or limit?
- [x] Avoided classifying by filename, discrepancy count or artifact volume?

Stage complete: YES
