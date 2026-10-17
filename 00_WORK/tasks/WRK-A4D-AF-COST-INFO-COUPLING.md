# WRK-A4D-AF-COST-INFO-COUPLING

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-af-cost-info-coupling`
Primary artifact: `02_REGISTRY/research/sources/d0_af_cost_info_coupling_2026-10-17/RESULT_RU.md`
Execution: `GitHub-first`

## Конечный оператор

Сравнить частные производные владеемой цены второй AF-записи с внутренним источником Эйнштейна–Гильберта на лапсе, на постоянном сдвиге и на амплитуде материи. Не вливать и не редактировать #334 и #363. Не выбирать коэффициент, который приравнивает пробный источник к тензору Эйнштейна. Не объявлять материю равной тензору Эйнштейна. Не умножать базовую стоимость на число ячеек, чтобы убрать объём. Не строить новый геометрический функционал.

Язык результата: кандидат. Не объявлять, что ОТО выведена. Не закрывать `D0-HODGE-LINKS-001`. Не добавлять строки в claims.csv.

## Точное обязательство

Записать, что цена проб `u` имеет нулевые частные производные по лапсу, сдвигу и материи, пока эти величины не входят в её аргументы. Записать ненулевое свёртывание Эйнштейна `-2/(N a²)` на произведении плоскости и сферы и свёртывание сдвига `-2ε/(a²(N²+ε²))`. Сохранить `coupling_holds=false`, `sources_coincide=false`, `gr_derived=false`, `equation_20_closed=false`, `equation_28_closed=false`.

## Разрешённая запись

- `02_REGISTRY/research/sources/d0_af_cost_info_coupling_2026-10-17/`
- `02_REGISTRY/research/A4D_AF_RECORD_COST_INFO_COUPLING_GAP_2026_10_17.md`

Только эти пути и штатные start/retire собственной строки. Не менять общий source, цену, BOOK, claims, Lean и ветки других исполнителей.

## Решающая проверка

`python3` и `python3 -O` на `test_af_cost_info_coupling.py` дают один статус PASS. Флаги `coupling_holds`, `gr_derived`, `equation_20_closed`, `equation_28_closed`, `sources_coincide` равны false.

## Why delegated

Объёмный дефект старой цены и золотая мера уже записаны в черновике #334. Здесь нужна отдельная проверка, даёт ли цена этой AF-записи лоренцев источник вместе с независимой материей.

## GitHub execution contract

После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-AF-COST-INFO-COUPLING`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-AF-COST-INFO-COUPLING`. Никакого self-merge из ветки исполнителя.

## Chat handoff

Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
