# WRK-A4D-V8-FULL-HESSIAN-APPLY

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-hessian-apply`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_hessian_apply_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N07. Полный Hessian–vector оператор одной v8-цены

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Implement and verify a reusable matrix-free bilinear second-source/Hessian action for the same stored-native v8 price, including mixed link/observer/coefficient/preparation directions, exact multiplicities and auxiliary Schur responses; consume the actual tangent and matter maps before asserting a physical kernel.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) — общий оператор, допустимый класс и все source jets.
- [`02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md) — неизменённая v8 цена и её точное вспомогательное представление.
- [`02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py) — оптимизированный известный full-price Hessian control.
- [`02_REGISTRY/research/sources/d0_medium_preparation_second_variation_2026-10-16/RESULT_RU.md`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/02_REGISTRY/research/sources/d0_medium_preparation_second_variation_2026-10-16/RESULT_RU.md) — принятый #330; другая AF preparation, не прибавлять её к v8.

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Начать с общего operator-jet интерфейса `D, dD[v], dD[w], d²D[v,w]`, actual matter amplitude jets и фиксированных калибровок исходного v8. Вернуть отдельные H, J_program, R contributions и их сумму, затем linear Hessian action в объявленном реальном coordinate chart. Использовать собственные divided differences/limits, не finite differences как доказательство. Не строить гигантский dense workspace `128^8192`; analytic multiplicities остаются явными.

Перенести проверенный Fourier/feature-group механизм старой row-wave на bilinear caller, удерживая все 4096 modes, 16 grades и reference128 в их действительной роли. На некритической точке различать d²S по curve и координатную Hessian: acceleration term не пропадает автоматически. На certified root interval не заменять midpoint точным корнем. Проверить symmetry и analytic versus independent interval evaluation. Сверху принять N05 C1 map и N06 response; до их согласования предоставлять только operator-level evaluator. Не искать самостоятельно все zero modes и не доказывать unqualified curved-root NO-GO.

## Потребитель
Ведущий #334 использует evaluator для полного joint Euler kernel и нелинейного продолжения, а не повторяет вычисление каждого отдельного направления.

## Зависимости и запуск
Базовый operator evaluator можно делать после регистрации независимо. Завершение native-facing API требует принятых интерфейсов N05 и N06 либо их pinned reviewed slices; не молчаливой копии промежуточного файла.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-V8-FULL-HESSIAN-APPLY`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_hessian_apply_2026-10-16/`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Старая положительная directional wave-bound должна воспроизводиться без нового root solve; проверенные actual symmetry paths дают ожидаемые тождества. Совпадение bilinear polarization, coincident eigenvalue limit и direct/Schur forms; mutation, удаляющая off-shell thermal modes, должна обнаруживаться.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-V8-FULL-HESSIAN-APPLY`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-V8-FULL-HESSIAN-APPLY`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
