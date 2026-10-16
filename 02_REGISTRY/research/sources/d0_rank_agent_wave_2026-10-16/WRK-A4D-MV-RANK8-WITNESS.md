# WRK-A4D-MV-RANK8-WITNESS

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-mv-rank8`
Primary artifact: `02_REGISTRY/research/sources/d0_rank_mv_rank8_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## R02. Ранговый сертификат

Источник `ec45c8cc4085e7bce888d97439251be9e578d4ff` читать через git show. Не вливать #334.
Меморандум `02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md`. Пакет на этом pin: `02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16`.
Источник читать через `git show ec45c8cc4085e7bce888d97439251be9e578d4ff:…`. Не вливать #334 и не писать в его ветку.
`J_r` в поручении — это источники `B_r` меморандума, не новый оператор.
Не решать полевое ядро и не строить нелинейную ветвь. Не объявлять GR/ОТО.
Язык результата: кандидат. Не добавлять строки в claims.csv.

## Точное обязательство
На чистом `chi` проверить (28): `M chi = lambda chi + sum beta_r J_r chi` с вещественными коэффициентами.
Явный оператор `M=|chi><chi|-I/16` обязан проходить (28) и падать на полноранговом (26): спаривание с нейтральным `S` равно `15/16`.
Независимо от R01: не импортировать его пакет. Не утверждать, что этот `M` реализован полевой скоростью.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_rank_mv_rank8_2026-10-16/`

Только эти пути и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, shared .lake и ветки других исполнителей.

## Решающая проверка
Certify that M chi = lambda chi + sum beta_r J_r chi is strictly weaker than the full-rank span condition, with an explicit operator that passes on chi and fails at full rank.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужен ограниченный сертификат или инвентарь, а не выбор новой физики и не решение совместного искривлённого уравнения.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-MV-RANK8-WITNESS`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python tools/task_lifecycle.py retire WRK-A4D-MV-RANK8-WITNESS`, если terminal выполнен. Для Lean-модуля не retire и не снимать черновик, пока CONTROL не внесёт formal_support. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «GR закрыта», когда доказан конечный сертификат.
