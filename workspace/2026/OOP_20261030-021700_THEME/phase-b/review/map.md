# Review Map — OOP_20261030-021700_THEME / Phase B

> **Phase**: `phase-b` — Template and Script Migration to Semantic Theme Tokens  
> **Candidate SHA**: `73152acdb5954e2bf1c38c84a69296ad987c91d2`  
> **Baseline SHA**: `0c5555e5b245563e344b957391a0c2592117955c`  
> **TS Ref**: `cac5396ae4f4efafce96df87df60634288b564e9`  
> **Reviewer**: `antigravity:thread:local:d6d0abd2-257b-428e-8e1e-390307d02fbd`  

---

## 1. Claims Map

| Claim ID | Source | Description | Verification Target |
|---|---|---|---|
| C1 | TS AC-1 | `tab_home.html` и `tab_theory.html` используют семантические токены темы | Отсутствие жестких `sky-` в декоративных элементах, работа `.theme-accent-text`, `.theme-border` |
| C2 | TS AC-2 | `tab_practice.html`, `tab_quiz.html`, `tab_results.html` используют токены темы; цвета PASS/FAIL сохранены | Проверка рамок редактора, опций квиза, сплит-ресайзера, неприкосновенность `emerald` и `rose` |
| C3 | TS AC-3 | `exam.html` адаптирован к токенам темы и режимам Clean / Cyberpunk | Регламент, требования, бейджи, сплиттер используют переменные темы |
| C4 | TS AC-4 | `header.html` навигация и активные пилюли адаптированы под все темы | `.week-pill-active`, `.subtab-active`, бейджи статуса |
| C5 | TS AC-5 | `uml_viewer.html` внешняя обвязка и лупа адаптированы; внутренние диаграммы изолированы | Тулбар, рамка `#uml-lens`, изоляция SVG-классов Clean Architecture |
| C6 | TS AC-6 | `app.js` строковые генераторы переведены на семантические классы | Отсутствие жестких классов в динамической генерации табов и квизов |
| C7 | TS AC-7 | Сквозная регрессионная верификация всех тестов (73 теста) | Полный прогон `pytest tests/ -q` без сбоев |
| C8 | TS §4 | Учет добавленной стоимости (VALUE accounting) | 10 файлов VALUE, 267 LOC (бюджет 10 файлов / 480 LOC) |
| C9 | TS §1 | Архитектурные инварианты | Zero-Build сохранен, семантика тестов не нарушена |
| C10 | TS §2 | Доступность и эргономика | Классы эргономики `.header-collapsed`, `.practice-split-resizer` сохранены |

---

## 2. Risks & Dependencies

- **R1: Смешение цветов темы с результатами тестов**. В темах `matrix-emerald` или `cyber-gold` статус теста мог бы слиться с фоном. Митигация: явные инварианты сохранения `text-emerald-400` и `text-rose-400`.
- **R2: Искажение цветов Clean Architecture в UML**. Студенты изучают разделение слоев по цветовому коду Мартина. Митигация: внутренние SVG-диаграммы не модифицировались.
- **R3: Регрессия селекторов автоматических тестов эргономики**. Митигация: селекторы `.header-collapsed`, `.practice-split-resizer`, `.practice-fullscreen-active` сохранены.

---

## 3. Environment & Oracles

- **Python Runtime**: 3.12.9
- **Harness**: pytest 9.1.1
- **Oracles**: 73 автотеста (`tests/`), `git diff --numstat` / `--name-status`, ручной аудит AST/разметки HTML-шаблонов.
