# WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-runner-wiring`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_runner_wiring_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N02. Подключить принятую проверку зависимостей к действительному runner

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Integrate the already accepted conservative certificate-input selector into the existing runner and test routing, preserving immutable evidence, failure behaviour and unknown-dependency fallback; demonstrate real shared-input selection without creating another runner or cache.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/sources/d0_medium_certificate_input_closure_2026-10-16/RESULT_RU.md`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/02_REGISTRY/research/sources/d0_medium_certificate_input_closure_2026-10-16/RESULT_RU.md) — принятый #328; hook ещё не был применён на данном входе.
- [`tools/research_input_closure.py`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/tools/research_input_closure.py) — готовый селектор, не писать новый.
- [`tools/run_research_certs.py`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/tools/run_research_certs.py) — единственный runner.
- [`tools/test_research_input_closure.py`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/tools/test_research_input_closure.py) — контроли и прежняя проверка отсутствия hook.
- [`.github/workflows/guards.yml`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/.github/workflows/guards.yml) — действительный routing.

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Сначала проверить, не подключён ли hook уже новым main: при готовом эквивалентном результате не повторять изменение. Иначе встроить `certificate_paths` на существующей границе выбора. Удалить только устаревшее ожидание теста «hook отсутствует», заменив его положительными integration assertions; не удалять негативные проверки.

Прогнать весь путь CLI → выбор → изолированный worker на маленьком реальном Git-fixture: изменён только общий owner; удалён/переименован pin; динамический import; ошибка парсинга; mismatch SHA; исполняемый сертификат меняет tracked input; failed/skipped scientific step при зелёном job. При неразрешимых зависимостях не сужать replay. Зафиксировать измеренные число выбранных entrypoints и время fixture, отдельно от недоказанного ускорения полной науки. Изменение workflow ограничить включением соответствующего test-suite, без смены Draft/Ready/main семантики, timeouts, permissions, concurrency или кеша.

## Потребитель
Приёмка #334 и всех следующих source-slice: общий изменённый научный вход обязан запускать своих потребителей. Это продолжение уже слитого M02, не его повтор.

## Зависимости и запуск
После регистрации в main, проверки живых PR и назначения одного писателя.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_runner_wiring_2026-10-16/`
- `tools/run_research_certs.py`
- `tools/research_input_closure.py`
- `tools/test_research_input_closure.py`
- `tools/test_run_research_certs.py`
- `.github/workflows/guards.yml`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Смена только импортируемого файла должна реально исполнить оба зависимых сертификата, но не независимый; unknown всегда выбран. Полный существующий runner fixture-suite остаётся зелёным. Отдельно показать nonzero exit и untouched историческую квитанцию.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
