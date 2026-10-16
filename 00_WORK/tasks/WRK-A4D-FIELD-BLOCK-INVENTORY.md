# WRK-A4D-FIELD-BLOCK-INVENTORY

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-field-inventory`
Primary artifact: `02_REGISTRY/research/sources/d0_rank_field_inventory_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## R06. Ранговый сертификат

Источник `ec45c8cc4085e7bce888d97439251be9e578d4ff` читать через git show. Не вливать #334.
Меморандум `02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md`. Пакет на этом pin: `02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16`.
Источник читать через `git show ec45c8cc4085e7bce888d97439251be9e578d4ff:…`. Не вливать #334 и не писать в его ветку.
`J_r` в поручении — это источники `B_r` меморандума, не новый оператор.
Не решать полевое ядро и не строить нелинейную ветвь. Не объявлять GR/ОТО.
Язык результата: кандидат. Не добавлять строки в claims.csv.

## Точное обязательство
Прочитать joint kernel на том же pin: `02_REGISTRY/research/A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md` и `02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/`.
Выход — список ненулевых field-only блоков вне `Omega-Omega`: имя, ранг, носитель. Не закрывать их и не запускать новый root solve.
Если блок уже обнулён опубликованным решением, записать это как факт инвентаря, не как новое закрытие.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_rank_field_inventory_2026-10-16/`

Только эти пути и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, shared .lake и ветки других исполнителей.

## Решающая проверка
List the nonzero field-only blocks outside Omega-Omega in the current joint kernel, with ranks and supports, without closing them.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужен ограниченный сертификат или инвентарь, а не выбор новой физики и не решение совместного искривлённого уравнения.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-FIELD-BLOCK-INVENTORY`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python tools/task_lifecycle.py retire WRK-A4D-FIELD-BLOCK-INVENTORY`, если terminal выполнен. Для Lean-модуля не retire и не снимать черновик, пока CONTROL не внесёт formal_support. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «GR закрыта», когда доказан конечный сертификат.
