# Knowledge record — REC-OOP_20261021-141300_REFAC-tech-sandbox-ast-whitelist: Изоляция песочницы: строгий синтаксический белый список AST, режим python -I и лимит 15 КБ

> One material claim/decision and its completed or explicitly unresolved disposition.
> Presence is not acceptance. Fill applicable fields; reasoned N/A only when inapplicable.

| Field | Value |
|---|---|
| Record identity | `REC-OOP_20261021-141300_REFAC-tech-sandbox-ast-whitelist` |
| Publication intent | Зафиксировать устранение критической уязвимости песочницы выполнения студенческого кода через замену черного списка на строгий синтаксический белый список AST и запуск процесса в изолированном окружении |
| Kind | technical-reference decision |
| Statement | Уязвимая фильтрация по черному списку строк/модулей заменена на строгий синтаксический белый список узлов и модулей AST (app/services/ast_validator.py), блокирующий системные атрибуты (__class__, __subclasses__, __builtins__, __globals__), опасные вызовы (open, eval, exec, compile, getattr) и неразрешенные импорты. RunnerService запускает пользовательский код во временной директории tempfile.TemporaryDirectory изолированным процессом python -I в очищенном окружении (PYTHONPATH="", безопасные переменные) с ограничением размера исходного кода 15 КБ и таймаутом 5.0 сек. |
| Applicability | Проект Web-OOP, сервисы верификации кода тренажера (/api/runner/run, /api/week{N}/practice/run). |
| Grounds and uncertainty | Подтверждено сьютом тестов безопасности tests/test_sandbox_security.py (постоянные гарды G1-G5: попытки обхода через __subclasses__, dunder, лимит 15 КБ, timeout), 40/40 тестов зеленые, EV__OOP_20261021-141300_REFAC.md (VERIFIED) и вердиктом REVIEW__OOP_20261021-141300_REFAC.md (APPROVE). Решение не требует Docker и стабильно функционирует на Windows-хосте владельца. Неопределенность отсутствует. |
| Disposition | accepted |
| Source | workspace/2026/OOP_20261021-141300_REFAC/RF__OOP_20261021-141300_REFAC.md @ 1046cf5c0db24bbda8f12e4e983378bfc390a4bb (§1, §2) и workspace/2026/OOP_20261021-141300_REFAC/REVIEW__OOP_20261021-141300_REFAC.md (§2, §4) |
| Originating task and unit | OOP_20261021-141300_REFAC, Executor antigravity:thread:local:794b3c0e-2f24-4cb3-846d-6f0ef33d9a4b / Reviewer antigravity:thread:local:7ff8150d-4da2-4cea-9205-49b86442239b |
| Producer | Coordinator antigravity:thread:local:8fc38498-8a48-43ea-b8a1-eec279b600e1 (zhasulan) |
| Qualifier | Coordinator zhasulan via /tfw-docs |
| Acceptance authority | owner:zhasulan (поправка A2 в TS__OOP_20261021-141300_REFAC.md, HL-OOP_20261021-141300_REFAC.md @ 8f06de2cc38aeb001d273e4585f1784607a33e46) и независимый REVIEW__OOP_20261021-141300_REFAC.md (APPROVE) |
| Completed effect or missing decision | Опубликована запись технического решения, обновлен KNOWLEDGE.md (D9, Legacy & Deprecation); обновление факта F4 маршрутизировано в /tfw-knowledge. |
| Relations | Scoped successor к части D3 (Верификатор) в KNOWLEDGE.md: заменяет черный список на белый список AST и изолированный python -I. |

## Source and decision context

В исследовании RES зафиксирована возможность полного обхода старого черного списка через рефлексию (().__class__.__subclasses__()) и вызов системных утилит на хосте разработчика. Разработан ASTValidator, разрешающий только базовые конструкции языка, безопасные математические операции и аннотации типов. Запуск процесса python -I отсекает чтение локальных модулей и пользовательских site-packages.

## Relations and current use

Дополняет KNOWLEDGE.md §1 Architecture Map (D9). Актуализация факта проекта F4 передана на этап /tfw-knowledge.

## Retry and continuation

Запись завершена и синхронизирована с KNOWLEDGE.md на этапе KNW задачи OOP_20261021-141300_REFAC.
