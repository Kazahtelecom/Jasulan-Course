# Knowledge record — REC-OOP_20261021-141300_REFAC-human-ai-policy-boundary: Граница применения методического правила «без ИИ»: студенты vs разработка платформы

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261021-141300_REFAC-human-ai-policy-boundary` |
| Publication intent | Зафиксировать разъяснение владельца о разграничении образовательного регламента прохождения курса студентами и процесса инженерной разработки LMS (`HL §11 S4`) |
| Kind | human knowledge |
| Statement | Учебное правило ментора «писать код только руками, без использования ИИ» действует строго в отношении обучающихся студентов (включая студентов-тестировщиков Мухитова Арсения и Иванова Романа, которые проходят тренажер и квизы вручную для поиска багов и верификации UX). На инженерную разработку самой платформы Web-OOP с привлечением автономных ИИ-агентов в рамках методологии Trace-First Workflow (TFW: Coordinator, Researcher, Executor, Reviewer) данное методическое ограничение не распространяется. |
| Applicability | Проект `Web-OOP`, правила прохождения студентами и регламент разработки платформы. |
| Grounds and uncertainty | Прямое разъяснение владельца (`owner:zhasulan`), зафиксированное в `HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46` (§11 S4). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261021-141300_REFAC/HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46` (§11 S4) |
| Originating task and unit | `OOP_20261021-141300_REFAC`, Coordinator `antigravity:thread:local:006f9d80-95a8-48f4-873b-724ef63f3f9a` / `cfedaf89-a3b4-4af7-8baa-3fdea76e4a91` (provenance: `owner:zhasulan`) |
| Producer | Coordinator `antigravity:thread:local:cfedaf89-a3b4-4af7-8baa-3fdea76e4a91` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` (`antigravity:thread:local:cfedaf89-a3b4-4af7-8baa-3fdea76e4a91`) via `/tfw-knowledge` |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46` §11 S4) |
| Completed effect or missing decision | Опубликована запись человеческого знания и обновлен раздел `KNOWLEDGE.md §4 Project Facts` (`F8`); открытых решений нет. |
| Relations | Scoped refinement of `KNOWLEDGE.md §4 F1, F2` (`8f06de2cc38aeb001d273e4585f1784607a33e46`): разграничивает роли участников и правила использования инструментов в учебном процессе и разработке. |

## Source and decision context

В ходе коммуникации с ментором (`saubakirov`) было озвучено жесткое требование: студенты должны писать код исключительно вручную, без подсказок нейросетей, чтобы выработать моторику и глубокое понимание принципов ООП.
Для исключения двусмысленности при взаимодействии с ИИ-агентами TFW владелец проекта (`zhasulan`) зафиксировал четкую демаркационную линию:
1. Запрет на ИИ распространяется на процесс обучения: студенты курса и проверяющие (Мухитов А., Иванов Р.) проходят модули и пишут решения самостоятельно.
2. Проектирование, программирование и сопровождение самой веб-системы `Web-OOP` выполняется с полноценным использованием ИИ-агентов под контролем TFW.

## Relations and current use

Уточняет `KNOWLEDGE.md §4 F1, F2` и добавляет `F8` в `KNOWLEDGE.md`. Предотвращает ложные срабатывания ограничений при постановке технических задач ИИ-агентам разработки.

## Retry and continuation

Запись завершена и принята на этапе `KNW` задачи `OOP_20261021-141300_REFAC`.
