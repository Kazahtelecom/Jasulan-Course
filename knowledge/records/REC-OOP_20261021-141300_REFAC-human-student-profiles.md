# Knowledge record — REC-OOP_20261021-141300_REFAC-human-student-profiles: Профили малой учебной группы из 4 участников и изоляция прогресса без тяжеловесной авторизации

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261021-141300_REFAC-human-student-profiles` |
| Publication intent | Зафиксировать утвержденные владельцем требования к составу пользователей и модели сохранения прогресса студентов в платформе Web-OOP (`HL §11 S7`, `HL §12 A1`, `RES FC3, SS1`) |
| Kind | human knowledge |
| Statement | Целевая аудитория платформы Web-OOP на этапе учебных недель — фиксированная малая учебная группа из 4 реальных участников: Жасулан Куандыков (`zhasulan`, ведущий разработчик и студент), Роман Иванов (`roman`, студент-тестировщик), Арсений Мухитов (`arseniy`, студент-тестировщик), Санжар Аубакиров (`saubakirov`, преподаватель и ментор курса). Для предотвращения коллизий и затирания баллов при совместной работе через временный Cloudflare-туннель платформа предоставляет переключатель 4 профилей в веб-интерфейсе с сохранением прогресса по ID пользователя в SQLite без усложнения системы тяжеловесной аутентификацией (пароли/JWT). |
| Applicability | Проект `Web-OOP`, все модули учебных недель (`Неделя 1`, `Неделя 2`, `Неделя 3`), режим совместной работы и публичного тестирования. |
| Grounds and uncertainty | Прямые указания и подтверждения владельца продукта (`owner:zhasulan`), зафиксированные в контракте `HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46` (§2, §4 п.4, §11 S7, §12 Amendment A1) и отчете исследования `RES.md` (FC3, SS1), верифицированные автотестами (`tests/test_profiles.py`) и независимым ревью `REVIEW__OOP_20261021-141300_REFAC.md` (`APPROVE`). Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261021-141300_REFAC/HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46` (§11 S7, §12 A1), `workspace/2026/OOP_20261021-141300_REFAC/research/iter1/RES.md` (FC3, SS1), `workspace/2026/OOP_20261021-141300_REFAC/REVIEW__OOP_20261021-141300_REFAC.md @ 57f58c63d109b01fa53df7923b2f9e1e36eb1633` (§1, §2) |
| Originating task and unit | `OOP_20261021-141300_REFAC`, Coordinator `antigravity:thread:local:006f9d80-95a8-48f4-873b-724ef63f3f9a` / `cfedaf89-a3b4-4af7-8baa-3fdea76e4a91` (provenance: `owner:zhasulan`) |
| Producer | Coordinator `antigravity:thread:local:cfedaf89-a3b4-4af7-8baa-3fdea76e4a91` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` (`antigravity:thread:local:cfedaf89-a3b4-4af7-8baa-3fdea76e4a91`) via `/tfw-knowledge` |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46`, поправка A1 и независимый вердикт `REVIEW__OOP_20261021-141300_REFAC.md`) |
| Completed effect or missing decision | Опубликована запись человеческого знания и обновлен раздел `KNOWLEDGE.md §4 Project Facts` (`F6`); открытых решений нет. |
| Relations | Scoped refinement of `KNOWLEDGE.md §4 F1, F5` (`8f06de2cc38aeb001d273e4585f1784607a33e46`): фиксирует поименный состав учебной группы и принцип изоляции оценок в UI/БД. |

## Source and decision context

При проведении аудита и тестирования платформы через публичный Cloudflare-туннель было выявлено, что все запросы выполнялись от имени единого захардкоженного пользователя `zhasulan`. В результате решения задач и прохождение квизов разными участниками приводили к затиранию чужих баллов.
Владелец проекта (`zhasulan`) на обсуждении архитектурных решений утвердил:
1. Реальный круг пользователей платформы — 4 человека (`zhasulan`, `roman`, `arseniy`, `saubakirov`).
2. Внедрение тяжеловесной аутентификации с регистрацией, паролями и JWT для доверенной группы из 4 человек избыточно и создало бы лишние барьеры.
3. Достаточным и надежным решением является переключатель профилей в UI (селектор в шапке) с передачей активного `student_id` в запросах к API и сохранением результатов по композитному ключу `(student_id, topic_id)` в SQLite.

## Relations and current use

Уточняет `KNOWLEDGE.md §4 F1, F5` и добавляет `F6` в `KNOWLEDGE.md`. Должно учитываться при разработке последующих недель (Неделя 3 и финал курса): все сервисы прогресса и представления обязаны поддерживать контекст выбранного студента.

## Retry and continuation

Запись завершена и принята на этапе `KNW` задачи `OOP_20261021-141300_REFAC`.
