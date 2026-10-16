# WRK-A4D-ANISOTROPIC-NORMAL-SOURCE

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-anisotropic-normal-source`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_anisotropic_normal_source_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M07. Неизотропная нормальная мера: полный ковектор остатка

**Потребитель:** Ведущий синтез: решить, допускается ли этот остаток собственной мерой; M08 включает его source при необходимости.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_RECORD_NORMAL_VOLUME_SOURCE.md`
- `A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md`
- `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Derive and check the full first variation of the normal-covariance quadratic coefficient, separating its isotropic curvature term from the genuine anisotropic remainder with moving frame and measure.

Для произвольной симметричной covariance Sigma_AB>=0 вычислить Q2=1/2 sum Sigma_AB[H_A H_B−tr(A_A A_B)]. Разложить Sigma=cI+Sigma_TF при фиксированном полном normal carrier, затем дифференцировать c, Sigma_TF, A и их frame совместно. Выдать операторный shape/measure covector и chain rule к supplied record variations. Получение локального spacetime stress допустимо только после явной factorization; пока это ковектор, не объявленная физическая материя. Не переносить непрерывный fourth-moment law на конечный цилиндровый фильтр.

## Выход и границы записи
Общая формула вариации, invariant-frame тесты и два некоммутирующих shape fixtures; отдельные scalar/isotropic/zero-shape controls в своём пакете.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_anisotropic_normal_source_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Повернуть A без поворота Sigma; заморозить dSigma; удалить нулевые normal-направления с прежними c2/c4; ошибочно принять quartic Q4 за Gauss–Bonnet. Каждый дефект должен выявляться.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-ANISOTROPIC-NORMAL-SOURCE`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-ANISOTROPIC-NORMAL-SOURCE`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 2; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-ANISOTROPIC-NORMAL-SOURCE` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
