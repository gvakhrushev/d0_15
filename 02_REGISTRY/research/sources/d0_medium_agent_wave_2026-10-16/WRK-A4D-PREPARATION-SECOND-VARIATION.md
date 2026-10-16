# WRK-A4D-PREPARATION-SECOND-VARIATION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-preparation-second-variation`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_preparation_second_variation_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M09. Полный second jet подготовленной цены

**Потребитель:** Ведущий nonlinear joint reduction и M08; даёт величины, которых нет в одном first-source proof.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md`
- `A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md`
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Derive a noncommuting second-variation/envelope formula and explicit safe-domain bounds for the existing preparation optimum and channel relative-entropy remainder, without claiming stability of the full dynamics.

Минимум sigma*(E) и A*=6−log Z/log(phi) уже доказаны — не повторять как результат. Вычислить D²A*, mixed E/preparation derivatives и Hessian настоящего D(Phi_E sigma||Phi_E sigma*) при faithful coarse output. Использовать Frechet/divided-difference calculus с непрерывными пределами при совпадающих eigenvalues; вне safe spectral margin не заявлять bounded Hessian. Сопоставить Schur/envelope формулу с независимым finite difference как diagnostic, а доказательство — аналитическое. Отдельно исследовать опубликованный rank-birth control: не называть все amplitude-critical branches минимумами.

## Выход и границы записи
Формула second jet, конкретные константы на объявленном safe interval, проверяемый некоммутирующий пример и source-regularity conditions в своём пакете.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_preparation_second_variation_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Замена полного канала commuting shortcut; игнорирование Z; eigenvalue collision ошибочно признан сингулярностью; rank birth ошибочно признан гладким Hessian. Не смешивать stable preparation и hyperbolicity gravity.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-PREPARATION-SECOND-VARIATION`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-PREPARATION-SECOND-VARIATION`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 2; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-PREPARATION-SECOND-VARIATION` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
