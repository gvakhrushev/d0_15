# WRK-A4D-PF-MEASURE-SOURCE-TRANSPORT

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-pf-measure-source-transport`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_measure_source_transport_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M06. Мера историй: оценка переноса значений и первых источников

**Потребитель:** Ведущий вывод собственной пространственной меры; M08 и конечный error budget используют именно эту оценку.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_NATIVE_GOLDEN_COST_REFINEMENT.md`
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`
- `A4D_NATIVE_INHERITED_PATH_RECORD_SETTINGS.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Prove an explicit finite C1 pushforward/source-error bound for supplied history-to-cell maps and normalized weights, including moving partitions; identify the precise native-map input rather than choosing it.

Вход: заданные отдельно finite map pi_N, веса цилиндров, вложения ready/pending, geometric target cell weights w_i(q)>0. Вывести commuting condition для pushforward при реальном AF-включении и полную производную нормированного среднего. Разложить ошибку источника через ошибки весов, их derivatives, local prices и derivatives; указать нижнюю границу Z и нормы. При moving partition показать дополнительный transport term или ограничить theorem фиксированными цилиндрами с явно указанной областью. Принадлежность w_i объёмной мере НЕ постулировать как вывод D0.

## Выход и границы записи
Аналитическая finite C1 bound с константами, точный двух/трёх-cell пример и тесты. Отдельно записать недостающую входную стрелку pi_N(X), которую должен дать главный синтез.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_measure_source_transport_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Совпадающие значения pushforward при разных first jets; одинаковая trace на AF-уровнях без пространственного отображения; равенство normalized/unnormalized sources после неверного удаления dZ. Не смешивать AF depth, t и h.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-PF-MEASURE-SOURCE-TRANSPORT`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-PF-MEASURE-SOURCE-TRANSPORT`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 1; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-PF-MEASURE-SOURCE-TRANSPORT` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
