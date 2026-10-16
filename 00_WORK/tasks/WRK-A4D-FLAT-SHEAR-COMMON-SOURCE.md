# WRK-A4D-FLAT-SHEAR-COMMON-SOURCE

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-flat-shear-common-source`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_flat_shear_common_source_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M10. Плоская сдвиговая проба: совместимые источники без придуманной суммы

**Потребитель:** Наш главный синтез: любой новый full-action кандидат сначала проходит эту пробу; предотвращает повторный обход уже закрытого тупика.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md`
- `A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md`
- `A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md`
- `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Build a typed common-source calculation on the already-owned flat factor shear, consuming its existing theorem and preserving distinct preparations/actions; expose any admissible extra source or a precise unbound operator slot.

Не перепроверять 2,899 старых условий как основной результат. Вход — готовые zero compiled/preparation source, positive heat и zero fixed-gate remainder на V=diag(2,−2,0,0). Сопоставить не более четырёх named remaining-owner источников из prepared-source, canonical active record, observer/reflection и реального chronology owner, разрешённого через source memo. Для каждого указать полный carrier, preparation, tangent, action и map на одну и ту же пробу. Если композиция не определена, оставить конкретную unbound arrow; запрещено складывать производные разных опытов. Выдать единый проверяемый source-row interface для нового native candidate.

## Выход и границы записи
Typed source table с формулами/missing maps и исполняемая проверка композиции. Положительный результат — действительно связанный дополнительный source на той же пробе; отрицательный — конкретное расхождение типов/джетов, которое меняет следующий тест, не общий NO-GO.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_flat_shear_common_source_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Переименовать coarse source в complete source; перенести current derivative на metric shear; отбросить archive compensation; fitted source = minus heat. Проверяющий код должен отвергать эти подмены.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-FLAT-SHEAR-COMMON-SOURCE`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-FLAT-SHEAR-COMMON-SOURCE`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 1; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-FLAT-SHEAR-COMMON-SOURCE` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
