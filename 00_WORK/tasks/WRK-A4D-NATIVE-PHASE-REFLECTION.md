# WRK-A4D-NATIVE-PHASE-REFLECTION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-native-phase-reflection`
Primary artifact: `02_REGISTRY/research/sources/d0_native_phase_reflection_2026-10-17/RESULT_RU.md`
Execution: `GitHub-first`

## Конечный оператор

Считать строки SELECT и отражение через пустую строку самостоятельно. Не вливать #334 и не писать в его ветку. Не выбирать коэффициент, который приравнивает сдвиг Gram к тензору Эйнштейна. Не называть смену фазы роли 1 сдвигом метрики. Не объявлять `sources_coincide=false` покомпонентным отказом десяти строк: десять компонент не вычисляются.

Язык результата: кандидат. Не объявлять, что native-цена равна геометрическому действию. Не закрывать `D0-HODGE-LINKS-001`. Не добавлять строки в claims.csv.

## Точное обязательство

Для всех вещественных амплитуд при фазах `(I,1,1,1)` записать перекрытие SELECT `t I16` и cross отражения `(1-2f/128) I16`. Для знака роли 1 только у второй конфигурации записать `mu I16 + gamma Q` и сдвиг Gram `2 p^4 gamma^2`. Сохранить `sources_coincide=false`, `ten_metric_components_evaluated=0`, `gr_derived=false`, `equation_20_closed=false`, `equation_28_closed=false`.

## Разрешённая запись

- `02_REGISTRY/research/sources/d0_native_phase_reflection_2026-10-17/`

Только этот путь и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, Lean и ветки других исполнителей.

## Решающая проверка

`python3` и `python3 -O` на `test_native_phase_source.py` дают один JSON и статус PASS. Флаги `gr_derived`, `equation_20_closed`, `equation_28_closed`, `sources_coincide` равны false, а `ten_metric_components_evaluated` равен 0.

## Why delegated

Буквальный 128-рядный cross уже отделён от двухстороннего компаратора. Здесь нужна его точная запись на всей вещественной области амплитуд и на одном знаке роли 1, без подмены десяти метрических слотов.

## GitHub execution contract

После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-NATIVE-PHASE-REFLECTION`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-NATIVE-PHASE-REFLECTION`. Никакого self-merge из ветки исполнителя.

## Chat handoff

Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
