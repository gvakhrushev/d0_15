# WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-matter-response`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N06. Физическая matter-подготовка: полный shell/reference блок

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Provide a reusable exact first- and second-order matter response solver on the owned 128-state shell with the complete reference, including kernel compatibility and all normalizer terms, while leaving thermal and feedback traces on their full carriers.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) — общий оператор, допустимый класс и все source jets.
- [`02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md) — неизменённая v8 цена и её точное вспомогательное представление.
- [`02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py) — положительный/отрицательный known-wave controls.
- [`02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md) — фиксированный root и shell gap.

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Из уже имеющихся P, Q=I-P, R_Q и полной purification составить callable интерфейс: на входе actual Delta', Delta'' и допустимые параметры shell/reference; на выходе projected compatibility, normal matter response, оставшиеся kernel coordinates и вклад в первый/второй source. Использовать `P Delta' P=epsilon' P` лишь в тех полных Schmidt-rank условиях, где это доказано; нельзя навязать операторное равенство произвольной rank-one подготовке.

Не переобъявлять свободные right/reference directions gauge: описать их математическую избыточность относительно конкретного чтения. Отделить настоящую matter Psi от auxiliary sigma*=K/TrK и X*=A^-1 из unfolding. Новизна — общий reusable solver и точный интерфейс к N07, а не ещё один расчёт старой wave. Удостоверить uniform inverse bound на normal shell complement только из старого certified gap; не оценивать полный field inverse. Если ограничения истинного engine у́же full sphere, вывести restriction отдельно.

## Потребитель
N07 и главный joint critical construction: устранить только разрешимую normal matter часть, сохранив все obstructing shell/reference уравнения.

## Зависимости и запуск
После регистрации в main, проверки живых PR и назначения одного писателя.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Воспроизвести известную row-wave repair и nonscalar conformal obstruction как разные scopes. Ввести изменение первого jet Delta, отслеживаемое вне shell, и проверить, что оно не исчезает из thermal/feedback source по ошибке. False pure16 reduction и frozen normalization должны быть отвергнуты.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
