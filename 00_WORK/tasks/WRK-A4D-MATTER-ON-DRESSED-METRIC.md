# WRK-A4D-MATTER-ON-DRESSED-METRIC

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-matter-on-dressed-metric`
Primary artifact: `02_REGISTRY/research/sources/d0_matter_on_dressed_metric_2026-10-18/RESULT_RU.md`
Execution: `GitHub-first`

## Why delegated
Нужно проверить, сидит ли метрический отклик уже принадлежащих CAR16/Fock и хронологического feedback на density-dressed \(\widehat g\), а не на сырой \(g(v_\chi)\), и даёт ли residual defect ненулевой источник именно на этой метрике.

## Точное обязательство
Читать pin `c3ae03b7b735dbde690bf1774fc3761846aff93248` только через `git show`. Если голова ушла вперёд, записать фактический SHA. Не редактировать #334. Мемо `A4D_ONE_FEEDBACK_NONFLAT_NULL_SCALAR_EINSTEIN_SOURCE_2026_10_18.md` уже строит grade0 null source одной AF×scene цены на source-compatible \(\widehat g\). Не передоказывать его. Проверить, следует ли тензор источника из уже принадлежащих корреляторов CAR16/Fock и хронологии, включая спин, а не только grade0. Если спиновый отклик отсутствует, это scoped no-go, а не отождествление всей материи с grade0.

Не определять \(T_{\mu\nu}\) как тензор Эйнштейна. Не добавлять действие \(\int\sqrt{|g|}(\partial\psi)^2\). Не выбирать меру. Не закрывать `D0-HODGE-LINKS-001`. Не писать в `claims.csv`. Не объявлять вывод ОТО.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_matter_on_dressed_metric_2026-10-18/`
- `02_REGISTRY/research/A4D_MATTER_ON_DRESSED_METRIC_2026_10_18.md`

Плюс штатные start/retire собственной строки. Язык `RESULT_RU.md` — русский. Статус кандидата.

## Решающая проверка
`python3` и `python3 -O` на проверяющем скрипте пакета оба печатают PASS. Либо записано явное выражение источника через принадлежащие корреляторы и `stress_on_dressed_metric` истинен, либо `scoped_nogo` истинен. `stress_defined_as_einstein` ложен. `gr_derived` ложен.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-MATTER-ON-DRESSED-METRIC`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-MATTER-ON-DRESSED-METRIC`, если terminal выполнен. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
