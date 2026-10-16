# WRK-A4D-LEAN-GOLDEN-CURVATURE-KERNEL

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-lean-golden-curvature-kernel`
Primary artifact: `02_REGISTRY/research/sources/d0_medium_lean_golden_curvature_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## M03. Lean: конечный золотой фильтр кривизны

**Потребитель:** Конечная часть cylinder-source и последующие differentiated/finite-refinement consumers.

## Inputs
Research SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` — исследовательский снимок, не accepted main. Пути ниже находятся в `02_REGISTRY/research/` на этом SHA:
- `A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md`
- `A4D_NATIVE_GOLDEN_COST_REFINEMENT.md`

Прочитать также `AGENTS.md`, `00_WORK/README.md` и общий контракт пакета
`02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md`.
Этот контракт сохраняет стратегию пользователя и различия математического результата, физического допуска и принятия.

## Точное обязательство
Formalize the finite four-cylinder moment identities and calibrated degree-four coefficient extraction generically in Lean, then specialize the existing golden parameters without assuming curvature or GR.

Использовать действующий `DetectorSupportGoldenWeight.cylWeight`, не вводить второе определение меры. Доказать моменты функции FF/RR→0, FR→1, RF→−1 и общий трёхточечный фильтр для F(t)=b+a*t^2+c*t^4. Доказать отмену b,c и коэффициент a при допустимом lambda, затем золотую специализацию. Отдельная лемма: совместное добавление spectators/blank не меняет reading. Это скалярная алгебра, не формализация континуальной ОТО или теоремы Гаусса.

## Выход и границы записи
Новый узкий `03_FORMALIZATION/D0/Research/GoldenCurvatureKernel.lean`, импортирующий фактический owner; вывод `#print axioms`, компилируемые corollaries и карта соответствия формулам оригинала. Общий All.lean/ClaimMap не править параллельно.

Свой каталог: `02_REGISTRY/research/sources/d0_medium_lean_golden_curvature_2026-10-16/`.
Прочие научные источники, общие реестры, README/AGENTS, CI и чужие ветки — read-only.
Shared patch отдаётся M01; собственные lifecycle/generated изменения выполняются штатными инструментами.
Не изменять физический action, trace, норму, input hypotheses или reference ради PASS.

## Решающий контроль
Отдельные доказуемые counterexamples: удаление RR, замороженный blank, неверный lambda-коэффициент. Нельзя использовать ложную гипотезу в theorem statement, sorry или axiom результата.

## Why delegated
Это конечный independently reviewable выход с фиксированным интерфейсом. Выбор общего физического действия, меры и native допуска остаётся у ведущего синтеза. Не расширять задачу до самостоятельной теории; при такой необходимости вернуть точную missing premise, не создавать child tasks.

## GitHub execution contract
До M01 registration intake это **registration candidate**, не запущенный агент.
После строки в main: `python tools/task_dispatch.py WRK-A4D-LEAN-GOLDEN-CURVATURE-KERNEL`; проверить live PR и уникального писателя.
Затем `python tools/task_lifecycle.py start WRK-A4D-LEAN-GOLDEN-CURVATURE-KERNEL`, Draft PR на указанной ветке, отдельный worktree; не писать в #310.
Приоритет волны 1; сохраняется общий лимит 5 WORKER, включая REVIEW/BLOCKED. Lean cache изолировать/сериализовать.
Narrow checks в итерации, применимые acceptance checks перед Ready; выполнить `python tools/task_lifecycle.py retire WRK-A4D-LEAN-GOLDEN-CURVATURE-KERNEL` в том же PR только при выполненном terminal.
Не self-merge и не закрывать #310/#202/#317. Применимость результата подтверждает ведущий.

## Chat handoff
PR/SHA, точный вывод и scope, место использования в родительской теореме, один blocker.
Аналитическое доказательство, exact/interval и numeric diagnostic различать. Не считать объём кода научным результатом.
