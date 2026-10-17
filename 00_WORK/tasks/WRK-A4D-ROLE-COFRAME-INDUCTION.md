# WRK-A4D-ROLE-COFRAME-INDUCTION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-role-coframe-induction`
Primary artifact: `02_REGISTRY/research/sources/d0_role_coframe_induction_2026-10-17/RESULT_RU.md`
Execution: `GitHub-first`

## Конечный оператор

Источник реконструкции читать только через `git show e92d4714183aec5b8838906be1dfd23844178042`. Не вливать #334 и не писать в его ветку. Blob checker: `0b11d34f2f982a62616722feeb110f10fa55f2e6`.

Построить один типизированный оператор: симметричная вариация с индексами Role индуцирует вариацию coordinate coframe на семействе pp-wave. Сравнить источник, посчитанный из кривизны этого coframe, с независимым Christoffel-источником на одном невакуумном джете. Скалярная плотность на этом семействе нулевая.

Язык результата: кандидат. Не объявлять, что полная native-цена равна геометрическому действию. Не отождествлять источник с архивным anomaly-stress. Не добавлять строки в claims.csv. Не выбирать β, t, α и не решать совместное полевое ядро.

## Точное обязательство

На семействе `e = I + H N` оператор `δe = e g^{-1} V / 2` для симметричной `V`. Для профильной вариации `V = k k^T` подъём равен `N` и сидит на строках 0 и 3. На джете `H = x^2 + 1/4` в нуле probe `V = E_00` читает 1, а Ricci равен `k k^T`. Отрицательные контроли: heat-зазор, row-wave `gamma`, endpoint factor и нулевая архивная матрица не равны этому probe. Левое лоренцево действие сохраняет метрику и двигает coframe.

## Разрешённая запись

- `02_REGISTRY/research/sources/d0_role_coframe_induction_2026-10-17/`

Только этот путь и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, Lean и ветки других исполнителей.

## Решающая проверка

`python3` и `python3 -O` на `test_role_induction.py` дают один JSON и статус PASS. Оба источника Ricci совпадают на невакуумном джете. Ни один отрицательный контроль не объявлен этим источником.

## Why delegated

Интерфейс уже написан: coframe, реконструкция и материальные модули на других носителях. Здесь нужен один оператор и сравнение коэффициентов, а не новый принцип и не поиск корня.

## GitHub execution contract

После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-ROLE-COFRAME-INDUCTION`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-ROLE-COFRAME-INDUCTION`. Никакого self-merge из ветки исполнителя.

## Chat handoff

Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
