# WRK-A4D-HEAT-E00-COVECTOR

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-heat-e00-covector`
Primary artifact: `02_REGISTRY/research/sources/d0_heat_e00_covector_2026-10-17/RESULT_RU.md`
Execution: `GitHub-first`

## Конечный оператор

Источник читать только через `git show e92d4714183aec5b8838906be1dfd23844178042`. Не вливать #334 и не писать в его ветку. Blob реконструкции: `023444e73d67815c94302767e3ea8163d99f4f95`. Blob теплового моста: `2e8a4b791e1d7adb472acf24c729d42583874a68`.

На фоне `H=x^2+1/4` сравнить эйлеровы плотности геометрического действия и owned heat `L2` вдоль `E_00` и вдоль профиля `k k^T`. Не выбирать `C0`, `C2`, `c`, `beta`, `t`, `alpha`. Не назначать `S_matter` разностью до `G`.

Язык результата: кандидат. Не объявлять, что native-цена равна геометрическому действию. Не закрывать `D0-HODGE-LINKS-001`. Не добавлять строки в claims.csv.

## Точное обязательство

Профильная эйлерова плотность `L2` остаётся `-32/3`, эйлерова плотность Эйнштейна–Гильберта на профиле остаётся 0. Вдоль `E_00` геометрическая эйлерова плотность равна `-1`. Тепловая эйлерова плотность вдоль `E_00` непостоянна. Постоянная калибровка `C0 dA0+C2 dA2` не воспроизводит геометрический covector. `gr_derived` и `equation_20_closed` остаются false.

## Разрешённая запись

- `02_REGISTRY/research/sources/d0_heat_e00_covector_2026-10-17/`

Только этот путь и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, Lean и ветки других исполнителей.

## Решающая проверка

`python3` и `python3 -O` на `test_heat_covector.py` дают один JSON и статус PASS. Оба флага `gr_derived` и `equation_20_closed` равны false.

## Why delegated

Коэффициенты уже фиксированы тепловым мостом и реконструкцией. Здесь нужно сравнение двух covector на двух вариациях, а не новый принцип и не поиск корня.

## GitHub execution contract

После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-HEAT-E00-COVECTOR`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-HEAT-E00-COVECTOR`. Никакого self-merge из ветки исполнителя.

## Chat handoff

Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
