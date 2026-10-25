# Knowledge record — REC-OOP_20261025-235206_UIEXP-tech-ide-ergonomics-and-quiz-balance: Эргономичный Zero-Build IDE-тренажёр и математическая балансировка квизов

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261025-235206_UIEXP-tech-ide-ergonomics-and-quiz-balance` |
| Publication intent | Зафиксировать техническое решение по реализации полноэкранного IDE-слоя тренажёра (сворачивание шапки, сплиттер, линейка номеров строк, масштабирование шрифта) на нативном JS/CSS и инварианты балансировки вариантов ответа в квизах |
| Kind | technical-reference decision |
| Statement | В шаблонах `header.html` и `tab_practice.html`, контроллере `app.js` и стилях `style.css` без нарушения принципа Zero-Build (D5) реализованы: (1) сворачивание фиксированной шапки (`#header-collapse-toggle`, `.header-collapsed`, сохранение в `localStorage`); (2) полноэкранный режим задачи с кодом (`#fullscreen-btn-<task_id>`, `.practice-fullscreen-active` `100vw × 100vh`, `z-index: 90`, выход по кнопке и `Escape`); (3) перетаскиваемый разделитель ширины колонок (`#split-resizer-<task_id>`, диапазон `25%..65%` и пресеты `25/75`, `35/65`, `50/50`); (4) IDE-контейнер `.code-editor-workspace` с синхронной колонкой номеров строк `#line-numbers-<task_id>` (`1..N`, синхронизация `scrollTop` и `fontSize`), счетчиком `#line-count-label-<task_id>`, отступами по `Tab` (4 пробела) и масштабированием шрифта `12px–20px` (`changeEditorFontSize`). В банках вопросов `app/content/week_1/quiz.py` и `app/content/week_2/quiz.py` внедрен проверяемый автотестами (`tests/test_ui_ergonomics.py`) инвариант: соотношение длины вариантов `max_len / min_len <= 1.65` (фактически `<= 1.12`), правильный ответ не является самым длинным минимум в 50% вопросов недели (фактически в `8/10`), а `correct_index` распределен по всем индексам `0..3` по 2–3 раза на неделю. |
| Applicability | Проект Web-OOP, все модули практики и тестирования (Неделя 1, Неделя 2 и последующая Неделя 3). |
| Grounds and uncertainty | Подтверждено прохождением `49/49` автотестов (`tests/test_ui_ergonomics.py`, `tests/test_week1.py`, `tests/test_week2.py`), доказательствами `EV__OOP_20261025-235206_UIEXP.md` (`6/6 VERIFIED`) и независимым вердиктом `REVIEW__OOP_20261025-235206_UIEXP.md` (`APPROVE`). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261025-235206_UIEXP/RF__OOP_20261025-235206_UIEXP.md @ 72171312657e8b0155c62a177d9c9ce8d5b9c501` (§1, §2) и `workspace/2026/OOP_20261025-235206_UIEXP/REVIEW__OOP_20261025-235206_UIEXP.md @ 6dd91ae3c36a3693e2ceab06173db8f8f477139e` (§2, §4) |
| Originating task and unit | `OOP_20261025-235206_UIEXP`, Executor `antigravity:thread:local:22ef7c4c-5377-408c-a2a5-338eb364cdfe` / Reviewer `antigravity:thread:local:858b7ee2-5983-4d22-ac16-8613a49fd9c4` |
| Producer | Task Coordinator `antigravity:thread:local:43c55687-5d64-4647-9012-0331bd386a85` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` via `/tfw-docs` (`Closing and record recovery`) |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261025-235206_UIEXP.md @ b5be743df7bae8c5d538f595a9c969f0d1cebafa`, `TS__OOP_20261025-235206_UIEXP.md @ 646ca95f703e53d2e9d38d95d855f8034ac9067f`, явное подтверждение приемки владельцем 2026-10-26) и независимый `REVIEW__OOP_20261025-235206_UIEXP.md` (`APPROVE`) |
| Completed effect or missing decision | Опубликована запись технического решения, обновлены `KNOWLEDGE.md` (`D11`, `Key Artifacts`), `README.md` и чек-лист закрытия в `REVIEW §6`. |
| Relations | Расширяет `REC-OOP_20261018-213107_W1MAT-tech-week1-funnel` (`D6`), `REC-OOP_20261018-222800_W2SOL-tech-week2-multiweek` (`D7`) и `REC-OOP_20261021-141300_REFAC-tech-modular-weeks` (`D8`), добавляя полноэкранный IDE-функционал и инварианты балансировки квизов без изменения маршрутов API и 20-балльной шкалы оценивания. |

## Source and decision context

При прохождении курса выявлено, что фиксированная трехрядная шапка (~200 px) и узкая жесткая сетка карточек задач (`5/12` и `7/12`) без номеров строк затрудняли написание кода, а в квизах Недели 1 и Недели 2 правильный ответ всегда был в 2–3 раза длиннее дистракторов и стоял преимущество под индексом `1` (`B`). Реализован нативный Zero-Build IDE-слой и математически проверенная балансировка всех 20 вопросов.

## Relations and current use

Дополняет `KNOWLEDGE.md §1 Architecture Decisions (D11)`. Поскольку шаблон `tab_practice.html` является общим для всех недель, подключенная в будущем Неделя 3 автоматически унаследует полноэкранный режим, сплиттер, нумерацию строк и масштабирование шрифта.

## Retry and continuation

Запись завершена и синхронизирована с `KNOWLEDGE.md` на этапе `KNW` задачи `OOP_20261025-235206_UIEXP`.
