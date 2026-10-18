# Knowledge record — REC-OOP_20261018-213107_W1MAT-human-beginner-format: Педагогический формат для начинающих (свободный тренажер без штрафов и 20-балльный итоговый квиз в конце воронки)

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261018-213107_W1MAT-human-beginner-format` |
| Publication intent | Зафиксировать утвержденные владельцем педагогические и продуктовые требования к формату обучения для начинающих студентов в `Web-OOP` (`HL §11 S1–S3`) |
| Kind | human knowledge |
| Statement | Курс Web-OOP рассчитан на малую группу студентов, включающую новичков: учебный модуль должен вести студента по связной воронке (простая пошаговая теория на одном сквозном классе $\rightarrow$ разбор готового кода и необязательный тренажер с кнопкой готового решения без требования/снятия баллов $\rightarrow$ финальное тестирование-квиз в самом конце на 20 баллов из 10 вопросов с выбором ответа), а интерфейс оформляется в стиле Dark Cyberpunk / Tech Modern с крупными иллюстрациями без мелких нечитаемых UML-диаграмм на сайте. |
| Applicability | Проект `Web-OOP`, учебные модули курса ООП (`Неделя 1` и последующие недели), целевая аудитория — студенты-новички курса. |
| Grounds and uncertainty | Прямые указания и подтверждения владельца продукта (`owner:zhasulan`), зафиксированные в замороженном контракте `HL-OOP_20261018-213107_W1MAT.md @ cbb06729d3b4a5101bf447385e1fcb52d48481e1` (§1 Vision, §7 Principles P1–P4, §11 S1–S3) и реализованные в Candidate `79b39aedc52ca4e88a9c5a44568b26f4879e364d`. Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261018-213107_W1MAT/HL-OOP_20261018-213107_W1MAT.md @ cbb06729d3b4a5101bf447385e1fcb52d48481e1` (§1, §7, §11) и `workspace/2026/OOP_20261018-213107_W1MAT/REVIEW__OOP_20261018-213107_W1MAT.md @ 001b5bc84bce859d1a85f16a1efd57e60a42c5e9` (Material handover) |
| Originating task and unit | `OOP_20261018-213107_W1MAT`, Coordinator `antigravity:thread:local:1da46223-edb5-410d-bad6-cd3c36954a1f` (provenance: `owner:zhasulan`) |
| Producer | Coordinator `antigravity:thread:local:1da46223-edb5-410d-bad6-cd3c36954a1f` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` (`antigravity:thread:local:1da46223-edb5-410d-bad6-cd3c36954a1f`) via `/tfw-knowledge` |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261018-213107_W1MAT.md @ cbb06729d3b4a5101bf447385e1fcb52d48481e1` & `TS__OOP_20261018-213107_W1MAT.md @ c373aeef251a58b106afc6aa07813972171673c5`) |
| Completed effect or missing decision | Опубликована запись человеческого знания и обновлен раздел `KNOWLEDGE.md §4 Project Facts` (`F5`); открытых решений нет. |
| Relations | Scoped refinement of `KNOWLEDGE.md §4 F1, F2` (`cbb06729d3b4a5101bf447385e1fcb52d48481e1`): уточняет состав учебной группы (наличие новичков) и правило оценивания недели (100% баллов из финального квиза на 20 баллов без штрафов за практику кода). |

## Source and decision context

Владелец проекта (`zhasulan`) после личного прохождения первой версии модуля отверг перегруженную академическую подачу и принудительный кодинг на баллы, указав ключевой контекст, который не мог быть выведен из кода:
1. Курс создается для малой группы (3 человека), где есть новички, для которых написание кода с нуля без предварительного разбора и подсказок вызывает ступор и потерю мотивации.
2. Практика с кодом должна быть обучающим тренажером с построчным разбором (`Passenger`/`Validator`) и кнопкой подстановки готового решения, не требующим баллов.
3. Все 20 баллов недели (`10 вопросов × 2.0 балла`) должны набираться в финальном тестировании (квизе) в конце воронки после изучения теории и практики.
4. Визуальный стиль сайта — Dark Cyberpunk / Tech Modern с кастомными иллюстрациями и без мелких Mermaid UML-диаграмм на веб-странице.

## Relations and current use

Уточняет `KNOWLEDGE.md §4 F1, F2` и добавляет `F5` в `KNOWLEDGE.md`. Обязательно к учету при планировании последующих учебных модулей.

## Retry and continuation

Запись завершена и принята на этапе `KNW -> DONE` задачи `OOP_20261018-213107_W1MAT`.
