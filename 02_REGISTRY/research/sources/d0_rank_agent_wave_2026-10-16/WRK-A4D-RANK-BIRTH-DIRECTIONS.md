# WRK-A4D-RANK-BIRTH-DIRECTIONS

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-rank-birth`
Primary artifact: `02_REGISTRY/research/sources/d0_rank_birth_directions_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## R09. Ранговый сертификат

Источник `ec45c8cc4085e7bce888d97439251be9e578d4ff` читать через git show. Не вливать #334.
Меморандум `02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md`. Пакет на этом pin: `02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16`.
Источник читать через `git show ec45c8cc4085e7bce888d97439251be9e578d4ff:…`. Не вливать #334 и не писать в его ветку.
`J_r` в поручении — это источники `B_r` меморандума, не новый оператор.
Не решать полевое ядро и не строить нелинейную ветвь. Не объявлять GR/ОТО.
Язык результата: кандидат. Не добавлять строки в claims.csv.

## Точное обязательство
При `k=8` ядро первой density-производной на полной нормированной amplitude sphere имеет размер `30784`: `1984` правых унитарных направлений и `28800` направлений рождения ранга.
Дать точное описание этих `28800`: первая производная плотности нулевая. Не называть их калибровкой и не классифицировать физические степени свободы.
Не утверждать, что вторая производная всегда ненулевая; если это не доказано для всех, оставить квантор «как правило» за пределом сертификата.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_rank_birth_directions_2026-10-16/`

Только эти пути и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, shared .lake и ветки других исполнителей.

## Решающая проверка
Describe exactly the 28800 rank-birth amplitude directions invisible to the first density derivative, without calling them gauge.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужен ограниченный сертификат или инвентарь, а не выбор новой физики и не решение совместного искривлённого уравнения.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-RANK-BIRTH-DIRECTIONS`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python tools/task_lifecycle.py retire WRK-A4D-RANK-BIRTH-DIRECTIONS`, если terminal выполнен. Для Lean-модуля не retire и не снимать черновик, пока CONTROL не внесёт formal_support. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «GR закрыта», когда доказан конечный сертификат.
