# WRK-A4D-CERTIFICATE-INPUT-CLOSURE

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-certificate-input-closure`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_certificate_input_closure_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M02. Замыкание зависимостей проверок без повторного CI всей истории

**Потребитель:** M01 приёмка конкретных срезов и любой scientific commit #310; освобождает ведущую модель от повторных полных прогонов.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md`
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Implement a conservative changed-input consumer selector for research certificates, with exact pinned-input provenance, unknown-dependency fallback and isolated-runner tests; do not weaken existing checks.

Существующий runner и Ready/Draft routing из #324 — вход, не переписывать их. Построить read-only индекс непосредственных и транзитивных входов из явных INPUTS/VALIDATION/pin-списков и imports. Динамически неразрешимый вход помечать UNKNOWN и включать соответствующие проверки консервативно, а не пропускать. Изменение общего исходника без изменения entrypoint должно включать его потребителей. Старые квитанции остаются неизменными. Отдельно выдавать результат выбора и результат исполнения; green skipped не считается replay.

## Выход и границы записи
`tools/research_input_closure.py`, `tools/test_research_input_closure.py` и отчёт в собственном пакете. Подключение к общему runner — отдельный малый patch владельцу #324/M01, не параллельная запись в workflow.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_certificate_input_closure_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Мутации: изменён только imported owner; несовпавший SHA; удалённый вход; динамический import; тест записывает в tracked файл; workflow SUCCESS с пропущенным scientific step. Все должны выявляться без затирания исторической квитанции.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-CERTIFICATE-INPUT-CLOSURE`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-CERTIFICATE-INPUT-CLOSURE`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 1; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-CERTIFICATE-INPUT-CLOSURE` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
