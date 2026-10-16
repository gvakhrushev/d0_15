# WRK-A4D-LEAN-SOURCE-REFLECTION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-lean-source-reflection`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_lean_source_reflection_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M04. Lean: полнота уравнений при подъёме вариаций

**Потребитель:** M05 — десять поперечных matching-уравнений; общий native-source lift без потери matter terms.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md`
- `A4D_NATIVE_GEOMETRIC_READING_INTERFACE.md`
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Formalize a generic finite-dimensional right-inverse/dual-source reflection theorem and explicit internal-source correction, with a norm bound and symmetric packed-pairing specialization.

Для L:X→Y и W:Y→X, L∘W=id, доказать инъективность pullback ковектора. Для residual equation a=L*e+r вывести e=W*(a−r) и оценку. Прямые внутренние ковекторы не выбрасывать: если цена a=L*e+d, условие a=0 даёт e=−W*d, а не e=0. Отдельно формализовать packing симметричного 4×4 тензора с двойными off-diagonal коэффициентами. Функционально-аналитический/физический допуск W не объявлять следствием этой конечной леммы.

## Выход и границы записи
`03_FORMALIZATION/D0/Research/SourceReflectionKernel.lean`, небольшой finite consumer и evidence аксиом/компиляции; общий импорт меняет M01 после независимой приёмки.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_lean_source_reflection_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Rank-deficient L; удалённый direct covector; неправильный вес off-diagonal; right-inverse перепутан с left-inverse. Свести ошибки к явным конечным примерам.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-LEAN-SOURCE-REFLECTION`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-LEAN-SOURCE-REFLECTION`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 2; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-LEAN-SOURCE-REFLECTION` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
