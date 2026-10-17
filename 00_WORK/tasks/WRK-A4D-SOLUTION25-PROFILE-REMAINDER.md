# WRK-A4D-SOLUTION25-PROFILE-REMAINDER

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-solution25-profile-remainder`
Primary artifact: `02_REGISTRY/research/sources/d0_solution25_profile_remainder_2026-10-17/RESULT_RU.md`
Execution: `GitHub-first`

## Конечный оператор

Источник решения (25) и уравнения (28) читать только через `git show e92d4714183aec5b8838906be1dfd23844178042`. Не вливать #334 и не писать в его ветку. Не выбирать `c`, `beta`, `t`, `alpha`. Не назначать остаток разностью до `G`. Не объявлять арифметику `EL+(32/3)Ric_00=0` отождествлением covector.

Язык результата: кандидат. Не объявлять, что native-цена равна геометрическому действию. Не закрывать `D0-HODGE-LINKS-001`. Не добавлять строки в claims.csv.

## Точное обязательство

На профильном касательном `δH=φ(x,y)` решения (25) записать эйлеровы плотности `L2`, скалярного куска и `q` как `-(16/3)s^2/c`, `-(4/3)s^2/c` и `-4 s^2/c`. Профильное спаривание поднятого Риччи с `k k^T` остаётся 0. `gr_derived`, `equation_20_closed` и `equation_28_closed` остаются false. Девять остальных метрических слотов, `C4 dA4`, `dR`, `dRem` и цена v8 в этот результат не входят.

## Разрешённая запись

- `02_REGISTRY/research/sources/d0_solution25_profile_remainder_2026-10-17/`

Только этот путь и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, Lean и ветки других исполнителей.

## Решающая проверка

`python3` и `python3 -O` на `test_remainder.py` дают один JSON и статус PASS. Флаги `gr_derived`, `equation_20_closed`, `equation_28_closed` и `covector_identification` равны false.

## Why delegated

Профильная формула тепла уже записана для общего `H`. Здесь нужна её подстановка в решение (25) и отдельная запись профильного спаривания, а не новый принцип и не поиск калибровки.

## GitHub execution contract

После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-SOLUTION25-PROFILE-REMAINDER`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-SOLUTION25-PROFILE-REMAINDER`. Никакого self-merge из ветки исполнителя.

## Chat handoff

Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
