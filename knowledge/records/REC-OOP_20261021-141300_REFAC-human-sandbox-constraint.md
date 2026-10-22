# Knowledge record — REC-OOP_20261021-141300_REFAC-human-sandbox-constraint: Ограничение хоста: нативная изоляция песочницы Python без Docker Desktop и сохранение Zero-Build

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261021-141300_REFAC-human-sandbox-constraint` |
| Publication intent | Зафиксировать утвержденное владельцем ограничение рабочего окружения и стратегическое решение по обеспечению безопасности песочницы стандартными средствами Python без Docker (`HL §11 S8`, `HL §12 A2`, `RES FC1, SS2`) |
| Kind | human knowledge |
| Statement | На рабочей машине владельца и хостах студентов отсутствует Docker Desktop / средства контейнеризации (утилита `docker` отсутствует в PATH). Платформа Web-OOP обязана строго сохранять архитектурный принцип Zero-Build и запускаться нативно одной командой `run.bat`. Поэтому безопасность песочницы запуска студенческого кода гарантируется исключительно средствами стандартной библиотеки Python: синтаксический белый список AST (`ASTValidator`), запуск изолированного подпроцесса через `python -I` в отдельной временной папке с таймаутом (5.0 с) и жестким лимитом размера кода (15 КБ). Прежняя схема фильтрации черным списком модулей признана уязвимой и полностью выведена из эксплуатации. |
| Applicability | Проект `Web-OOP`, сервис верификации кода `RunnerService` (`app/services/runner.py`, `app/services/ast_validator.py`), регламент запуска платформы на машине разработчика и студентов. |
| Grounds and uncertainty | Аудит окружения в RES (команда `docker --version` завершилась ошибкой `CommandNotFoundException`), решение владельца по поправке A2 (`HL §12 A2`), подтверждение контрфактическими тестами обхода песочницы (гарды G1–G5, G7–G10) и независимым ревью `REVIEW__OOP_20261021-141300_REFAC.md`. Неопределенность отсутствует. |
| Disposition | accepted |
| Source | `workspace/2026/OOP_20261021-141300_REFAC/HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46` (§11 S8, §12 A2), `workspace/2026/OOP_20261021-141300_REFAC/research/iter1/RES.md` (FC1, SS2), `workspace/2026/OOP_20261021-141300_REFAC/REVIEW__OOP_20261021-141300_REFAC.md @ 57f58c63d109b01fa53df7923b2f9e1e36eb1633` (§2, §3, Contradictions table) |
| Originating task and unit | `OOP_20261021-141300_REFAC`, Coordinator `antigravity:thread:local:006f9d80-95a8-48f4-873b-724ef63f3f9a` / `cfedaf89-a3b4-4af7-8baa-3fdea76e4a91` (provenance: `owner:zhasulan`) |
| Producer | Coordinator `antigravity:thread:local:cfedaf89-a3b4-4af7-8baa-3fdea76e4a91` (`zhasulan`) |
| Qualifier | Coordinator `zhasulan` (`antigravity:thread:local:cfedaf89-a3b4-4af7-8baa-3fdea76e4a91`) via `/tfw-knowledge` |
| Acceptance authority | `owner:zhasulan` (`HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46`, поправка A2 и независимый вердикт `REVIEW__OOP_20261021-141300_REFAC.md`) |
| Completed effect or missing decision | Опубликована запись человеческого знания и обновлен раздел `KNOWLEDGE.md §4 Project Facts` (`F7`), выступающий scoped successor / correction к устаревшему описанию в `F4`; открытых решений нет. |
| Relations | Scoped successor / correction to `KNOWLEDGE.md §4 F4` (`8f06de2cc38aeb001d273e4585f1784607a33e46`): исправляет и заменяет описание механизма изоляции `RunnerService` (замена неэффективного черного списка модулей на синтаксический белый список AST, `python -I` и лимит 15 КБ). |

## Source and decision context

В ходе исследования задачи `OOP_20261021-141300_REFAC` была обнаружена критическая уязвимость в `app/services/ast_validator.py`: фильтрация по черному списку модулей легко обходилась через рефлексию `__subclasses__()`, позволяя получить доступ к модулю `os` и выполнять произвольные команды на хосте.
При обсуждении вариантов изоляции владелец (`zhasulan`) зафиксировал жесткое контекстное ограничение: на его рабочей машине и машинах студентов отсутствует Docker Desktop (требующий WSL2 и прав администратора). Установка контейнеризации нарушила бы базовый принцип доступности и легкости развертывания («Zero-Build, старт в один клик через `run.bat`»).
Владелец утвердил поправку A2: отказ от Docker в пользу нативной трехуровневой защиты стандартными средствами Python:
1. Строгий синтаксический белый список узлов AST (`ast.ClassDef`, `ast.FunctionDef`, базовые операции) с полным запретом dunder-атрибутов (`__subclasses__`, `__class__`, `__builtins__`) и любых вызовов `import`/`eval`/`open`.
2. Запуск подпроцесса с флагом `python -I` (изолированный режим: игнорирование переменных окружения и пользовательских путей `site-packages`) в чистой временной директории.
3. Ограничение размера входного скрипта до 15 КБ и тайм-аут 5.0 секунд.

## Relations and current use

Является scoped successor / correction к `KNOWLEDGE.md §4 F4` и дополняет `KNOWLEDGE.md §4 F7`. При любых будущих доработках сервиса проверки решений (`RunnerService`) строго запрещено возвращаться к черным спискам или вводить тяжелые внешние зависимости, требующие установки стороннего ПО сверх базового интерпретатора Python 3.12.

## Retry and continuation

Запись завершена и принята на этапе `KNW` задачи `OOP_20261021-141300_REFAC`.
