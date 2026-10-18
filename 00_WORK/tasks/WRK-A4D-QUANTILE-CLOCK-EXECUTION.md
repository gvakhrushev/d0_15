# WRK-A4D-QUANTILE-CLOCK-EXECUTION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-quantile-clock-execution`
Primary artifact: `02_REGISTRY/research/sources/d0_quantile_clock_execution_2026-10-18/RESULT_RU.md`
Execution: `GitHub-first`

## Why delegated
Мемо `A4D_GOLDEN_QUANTILE_CLOCK_SAME_CAR_VOLUME_BRIDGE_2026_10_18.md` на pin `c3ae03b7` строит нижнетреугольную карту часов. Нужно проверить, исполняет ли её уже принадлежащий recording/engine без нового гейта, и совпадает ли moving Jacobian source (Q6)–(Q7) с настоящим moving sampling effect на одном непостоянном лапсе и одной сдвиговой 4D-плотности.

## Точное обязательство
Читать pin только через `git show` и `git grep`. Если голова #334 ушла вперёд, записать фактический SHA. Не сливать и не редактировать PR #334 и соседние запрещённые черновики. Цитируемый там `certificates/a4d_golden_quantile_clock_source_check.py` на `cd077973` отсутствовал; проверить заново и не считать зелёный CI прогоном отсутствующего файла.

Сравнить (Q6)–(Q7) с эффектом и costate уже принадлежащего движка. Выход — pass или fail на допущенном metric/matter касании и явный residual, если источники не совпали. Не добавлять гейт, чтобы карта стала исполненной. Не объявлять `qρ=μ`, если владеемый коцикл по-прежнему `qρ(w)=μ(w)Tr(ρ M_w)`. Не закрывать `D0-HODGE-LINKS-001`. Не писать в `claims.csv`. Не объявлять вывод ОТО.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_quantile_clock_execution_2026-10-18/`
- `02_REGISTRY/research/A4D_QUANTILE_CLOCK_EXECUTION_2026_10_18.md`

Плюс штатные start/retire собственной строки. Язык `RESULT_RU.md` — русский. Статус кандидата.

## Решающая проверка
`python3` и `python3 -O` на проверяющем скрипте пакета оба печатают PASS. Флаги `engine_executes_map` и `sources_coincide` истинны только если сравнение на обоих касаниях дало ноль. Иначе записан явный residual и оба флага ложны. `gr_derived` ложен.

## GitHub execution contract
После регистрации на main создать из текущего main указанную ветку; `python3 tools/task_lifecycle.py start WRK-A4D-QUANTILE-CLOCK-EXECUTION`; открыть Draft до содержательной записи. Перед Ready выполнить решающую проверку; затем `python3 tools/task_lifecycle.py retire WRK-A4D-QUANTILE-CLOCK-EXECUTION`, если terminal выполнен. Никакого self-merge или поднятия WIP.

## Chat handoff
Repository, PR и SHA; точный результат; команды и фактически выполненные проверки; один оставшийся blocker. Не писать «ОТО выведена», когда доказан конечный сертификат.
