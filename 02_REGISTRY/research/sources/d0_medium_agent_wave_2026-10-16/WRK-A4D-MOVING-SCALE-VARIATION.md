# WRK-A4D-MOVING-SCALE-VARIATION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-moving-scale-variation`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_moving_scale_variation_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M08. Полевые масштабы, нормировка и наблюдатель: единые вариации

**Потребитель:** Ведущий native full-price→field equations; M06 даёт measure-error term; M09 даёт preparation derivatives.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md`
- `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`
- `A4D_RECORD_NORMAL_VOLUME_SOURCE.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Compute the complete Euler and boundary terms of the already-declared scalar-coefficient curvature, topological-density and observer sectors with moving scale/preparation and normalized aggregation, without selecting a scale law.

Начать с независимых scalar fields c(x), b(x), d(x), observer u и метрики: integral[b+cR+d E4+L_observer]. Сохранить все derivative-of-coefficient terms, полный Lorentz reflection owner и boundary flux. Затем только chain rule к c=gamma alpha_n(X)t(X)^2/2. Для normalized aggregation вывести centered measure source отдельно от local preparation partition Z(E); это два разных нормализатора. Свести к constant coefficients controls. Дискретный индекс n не дифференцировать как гладкое поле; переходы n — отдельная finite change.

## Выход и границы записи
Одна таблица independent-field Euler terms и composite pullbacks, исполняемые tensor/sign controls и точный source-error norm interface. Не подбирать beta(h), t(h), alpha или observer law.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_moving_scale_variation_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Field-dependent Euler density не топологическая константа; постоянный кодовый k в ненормированном integral даёт volume source; normalizing не удаляет observer; не замораживать t лишь в части quotient.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-MOVING-SCALE-VARIATION`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-MOVING-SCALE-VARIATION`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 2; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-MOVING-SCALE-VARIATION` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
