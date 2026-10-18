# WRK-A4D-LAPSE-REYNOLDS-RESIDUAL

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-lapse-reynolds-residual`
Primary artifact: `02_REGISTRY/research/sources/d0_lapse_reynolds_residual_2026-10-18/RESULT_RU.md`
Execution: `GitHub-first`

## Why delegated
На фиксированном корне \(H+J+R\) приведённый лапсовый коэффициент лежит в интервале \((0.0057230, 0.0057231)\). Нужно проверить, сокращает ли его boundary-jet Reynolds Ward (Q7) при движении ячеек, без подбора коэффициента.

## Точное обязательство
Читать pin `c3ae03b7b735dbde690bf1774fc3761846aff93248` только через `git show`. Если голова ушла вперёд, записать фактический SHA. Не редактировать #334. Взять уже вычисленный интервал из `check_native_scalar_price_response.py` и формулу (Q7) из `A4D_GOLDEN_QUANTILE_CLOCK_SAME_CAR_VOLUME_BRIDGE_2026_10_18.md`. Сравнить их на том же \(\beta=2p^2\), \(z=2^{-20}\), \(M=128\).

Выход — точное сокращение или количественный residual. Не выбирать множитель, чтобы разность стала нулём. Не заменять условную цену новым действием. Не закрывать `D0-HODGE-LINKS-001`. Не писать в `claims.csv`. Не объявлять вывод ОТО. Конечный native Schur-предел этим сравнением не объявляется.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_lapse_reynolds_residual_2026-10-18/`
- `02_REGISTRY/research/A4D_LAPSE_REYNOLDS_RESIDUAL_2026_10_18.md`

Плюс штатные start/retire собственной строки. Язык `RESULT_RU.md` — русский. Статус кандидата.

## Решающая проверка
`python3` и `python3 -O` на проверяющем скрипте пакета оба печатают PASS. Флаг `exact_cancellation` истинен только если residual тождественно нуль. Иначе записан количественный residual и флаг ложен. `coefficient_chosen` ложен. `gr_derived` ложен.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-LAPSE-REYNOLDS-RESIDUAL`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-LAPSE-REYNOLDS-RESIDUAL`, если terminal выполнен. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
