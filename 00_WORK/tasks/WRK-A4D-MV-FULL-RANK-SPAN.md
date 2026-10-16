# WRK-A4D-MV-FULL-RANK-SPAN

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-mv-full-rank`
Primary artifact: `02_REGISTRY/research/sources/d0_rank_mv_full_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## R01. Ранговый сертификат

Источник `ec45c8cc4085e7bce888d97439251be9e578d4ff` читать через git show. Не вливать #334.
Меморандум `02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md`. Пакет на этом pin: `02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16`.
Источник читать через `git show ec45c8cc4085e7bce888d97439251be9e578d4ff:…`. Не вливать #334 и не писать в его ветку.
`J_r` в поручении — это источники `B_r` меморандума, не новый оператор.
Не решать полевое ядро и не строить нелинейную ветвь. Не объявлять GR/ОТО.
Язык результата: кандидат. Не добавлять строки в claims.csv.

## Точное обязательство
Точная алгебраическая проверка: для эрмитова `M` на 16 координатах условие `Tr(S M)=0` для всех `S=S*`, `Tr S=0`, `Tr(S J_r)=0` эквивалентно `M` в `span{I,J_1,J_2,J_3}`.
Остаток — формула (27) меморандума. Свидетель внутри оболочки и отрицательный контроль вне её.
Не вычислять полевую скорость и не утверждать, что конкретный native `M_v` уже лежит в оболочке.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_rank_mv_full_2026-10-16/`

Только эти пути и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, shared .lake и ветки других исполнителей.

## Решающая проверка
Certify that Tr(S M)=0 for every traceless S orthogonal to J_1,J_2,J_3 is equivalent to M in span{I,J_1,J_2,J_3}, with a witness and a negative control, without using the field kernel.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужен ограниченный сертификат или инвентарь, а не выбор новой физики и не решение совместного искривлённого уравнения.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-MV-FULL-RANK-SPAN`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python tools/task_lifecycle.py retire WRK-A4D-MV-FULL-RANK-SPAN`, если terminal выполнен. Для Lean-модуля не retire и не снимать черновик, пока CONTROL не внесёт formal_support. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «GR закрыта», когда доказан конечный сертификат.
