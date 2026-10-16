# WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-transverse-matching-residual`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_transverse_matching_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M05. Десять поперечных уравнений вне matching-графа

**Потребитель:** Ведущий синтез: точная система, которую должен сохранять собственный переход. M04 используется после приёмки, но вычисление не ждёт Lean.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_NATIVE_MATTER_CLOCK_RECORD_BINDING.md`
- `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`
- `A4D_NATIVE_JOINT_FIELD_QUOTIENT.md`
- `A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Construct the explicit tangent and annihilator maps for the owned comparator/native equality graph and expose all ten omitted transverse Euler rows, without inventing a transverse dynamics or counterterm.

Взять настоящий 22-полевой equality graph владельца и raw 32-полевой frame/matter chart. Вычислить differential embedding, его полный adjoint с пространственными производными и десятикомпонентный annihilator. Дать необходимое и достаточное алгебраическое условие, когда graph-stationarity действительно является raw stationarity. Для ещё не связанного полного действия оставить raw Euler entries именованными, а не назначить их нулём. Предъявить один точный bounded fixture на опубликованном germ и независимый тест S(q,c)=q*c.

## Выход и границы записи
Явные матрицы/операторы pullback и transverse residual, программа и краткая теорема в своём пакете. Не решать глобальную нелинейную native динамику, не менять равенства владельца.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_transverse_matching_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Полный rank10 metric lift при ненулевом annihilator-source обязан оставлять десять непроверенных строк. Проверить двусторонние касательные, variation of normalizer и boundary terms.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 1; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
