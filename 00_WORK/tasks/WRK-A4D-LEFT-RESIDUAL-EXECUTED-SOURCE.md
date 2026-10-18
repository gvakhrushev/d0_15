# WRK-A4D-LEFT-RESIDUAL-EXECUTED-SOURCE

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-left-residual-executed-source`
Primary artifact: `02_REGISTRY/research/sources/d0_left_residual_executed_source_2026-10-18/RESULT_RU.md`
Execution: `GitHub-first`

## Why delegated
Уже принадлежащее LEFT recording word и адресный marginal нужно связать так, чтобы остаточный golden/π₀ defect стал исполненным источником на отождествлённой dressed-метрике. Новый функционал не выбирается. Если принадлежащие объекты этой связи не дают, выход — scoped no-go с именем недостающего примитива.

## Точное обязательство
Прочитать pin `c3ae03b7b735dbde690bf1774fc3761846aff93248` ветки `exp/a4d-joint-response-continuation-2026-10-16` только через `git show` и `git grep`. Если к старту голова ушла вперёд, читать новую голову и записать её SHA. Не сливать и не редактировать PR #334, #363, #322, #323, #317, #202, #342, #353.

Native закон проверки: sampling measure уже принадлежащей записи различает cochain shift, который производит residual defect. Сравнить этот сдвиг с address marginal. Искомое тождество — residual defect равен исполненному тензору источника на \(\widehat g\), где \(\widehat g_x=(\mu_x/\bar\mu)g_x\). Не назначать \(T_{\mu\nu}\) равным тензору Эйнштейна. Не вводить новое действие, меру или гейт. Не закрывать `D0-HODGE-LINKS-001`. Не писать строку в `claims.csv`. Не объявлять вывод ОТО. Уравнения (20) и (28) оставить открытыми.

Учесть уже записанный на том же pin мемо `A4D_ONE_FEEDBACK_NONFLAT_NULL_SCALAR_EINSTEIN_SOURCE_2026_10_18.md`: grade0 null source там построен для одной AF×scene цены и не делает scene effect обязательной программой. Не переписывать эту конструкцию. Проверять именно LEFT word и cochain shift.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_left_residual_executed_source_2026-10-18/`
- `02_REGISTRY/research/A4D_LEFT_RESIDUAL_EXECUTED_SOURCE_2026_10_18.md`

Плюс штатные start/retire собственной строки. Язык `RESULT_RU.md` — русский. Статус кандидата.

## Решающая проверка
`python3` и `python3 -O` на проверяющем скрипте пакета оба печатают PASS. В результате ровно один из флагов `identity_holds` или `scoped_nogo` истинен, и `gr_derived` ложен. Отрицательный контроль обязан уметь уронить заключение, а не только технику проверки.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-LEFT-RESIDUAL-EXECUTED-SOURCE`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-LEFT-RESIDUAL-EXECUTED-SOURCE`, если terminal выполнен. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
