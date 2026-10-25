# Knowledge record — REC-OOP_20261025-235206_UIEXP-human-quiz-and-ide-ux: Педагогический стандарт квизов с ловушками и эргономики кодинга

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261025-235206_UIEXP-human-quiz-and-ide-ux` |
| Publication intent | Зафиксировать выявленные владельцем при личном прохождении курса педагогические и UX-требования к тренажёру кода и тестовым вопросам (`HL §11 S1–S3`) |
| Kind | human knowledge |
| Statement | По результатам ручного прохождения лекций и практики владельцем (`zhasulan`) установлены обязательные требования к качеству учебных модулей платформы Web-OOP: (1) рабочее место кодинга должно быть свободно масштабируемым (сворачиваемая верхняя шапка, полноэкранный режим задачи с кодом, регулируемая ширина колонок условия/редактора, видимая нумерация строк и увеличение шрифта), чтобы студент не писал код в узком зажатом окне; (2) тестовые вопросы квизов обязаны содержать продуманные концептуальные ловушки (типичные ошибки понимания ООП/SOLID), иметь сбалансированную длину всех 4 вариантов ответа и равномерное распределение правильных букв (`A, B, C, D`), чтобы исключить угадывание правильного ответа по самому длинному тексту. |
| Applicability | Проект Web-OOP, все учебные недели (Неделя 1, Неделя 2 и предстоящая разработка Недели 3). |
| Grounds and uncertainty | Основано на прямом пользовательском опыте и указаниях владельца `zhasulan` в `HL-OOP_20261025-235206_UIEXP.md §11 (S1, S2, S3)` и подтверждено приемкой результата `Candidate 37d7f84cd3c154b182d77adc04f0a371e039fa00` (2026-10-26). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261025-235206_UIEXP/HL-OOP_20261025-235206_UIEXP.md @ b5be743df7bae8c5d538f595a9c969f0d1cebafa` (§11 Strategic Insights S1–S3) и сообщения владельца `zhasulan` в сессии планирования/приемки 2026-10-25..2026-10-26 |
| Originating task and unit | `OOP_20261025-235206_UIEXP`, Task Coordinator `antigravity:thread:local:43c55687-5d64-4647-9012-0331bd386a85` (`owner:zhasulan`) |
| Producer | Task Coordinator `antigravity:thread:local:43c55687-5d64-4647-9012-0331bd386a85` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` via `/tfw-knowledge` (`Closing and record recovery`) |
| Acceptance authority | `owner:zhasulan` (прямое утверждение `HL @ b5be743` и финальная приемка задачи 2026-10-26) |
| Completed effect or missing decision | Опубликована запись человеческого знания, обновлен `KNOWLEDGE.md` (`§4 F9`) и чек-лист закрытия в `REVIEW §6`. |
| Relations | Дополняет `REC-OOP_20261018-213107_W1MAT-human-beginner-format` (`F5` в `KNOWLEDGE.md §4`), уточняя требования к качеству дистракторов в 20-балльных квизах и эргономике свободного тренажёра. |

## Source and decision context

Владелец лично протестировал прохождение курса глазами студента и обнаружил два ключевых барьера: (1) физический дискомфорт при написании кода из-за громоздкой верхней шапки, отсутствия номеров строк, мелкого шрифта и невозможности развернуть условие задачи и редактор во весь экран; (2) педагогическую уязвимость тестов, где правильный ответ всегда легко угадывался просто как самый длинный текст.

## Relations and current use

Закреплен как факт `F9` в `KNOWLEDGE.md §4 Project Facts`. При проектировании банка вопросов Недели 3 (Паттерны GoF) необходимо сразу закладывать концептуальные ловушки и проверять баланс длины опций (`max_len / min_len <= 1.65`) и распределение `correct_index`.

## Retry and continuation

Запись завершена и синхронизирована с `KNOWLEDGE.md` на этапе `KNW` задачи `OOP_20261025-235206_UIEXP`.
