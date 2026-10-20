# WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-weighted-source`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_weighted_source_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N08. Вес пространственных узлов без подмены stored-оператора

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Derive the exact fixed-carrier value, adjoint and first-source transport under a supplied positive moving site weight, retain the endpoint weight factors and observer derivatives, and identify precisely when the literal stored operator belongs to that weighted class.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) — общий оператор, допустимый класс и все source jets.
- [`02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md) — неизменённая v8 цена и её точное вспомогательное представление.
- [`02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md) — ранее известная weighted boundary, не повторять общий NO-GO.
- [`02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) — §0.3: counting-site условие и фактор sqrt(omega_x/omega_y).

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Пусть omega_x>0 — данное поле весов, не выведенная PF/geometric мера. Начать с actual native inner product и I_x=sqrt(omega_x) Lambda(sqrt(h_x)). Получить conjugated shift с обоими endpoint factors, его истинный adjoint, derivative dlog omega, observer commutators и full trace/source transformation. Сравнить буквальный stored D с его conjugate, а не автоматически заменить его d+d†.

Из первичных edge equations вывести необходимые и достаточные условия selfadjointness на фиксированном finite carrier; где они уже доказаны, потребить формулу и добавить недостающий полный source-jet. Отдельно: similarity/change of representation и изменение самого физического weight law — разные операции. Не переназначать counting trace как PF; не утверждать unitary return в unweighted пространстве без проверки. Проверить нормированные probabilities, raw sums и полный C,M bookkeeping. Scalar measure/stress выбор остаётся ведущему; #331 moving curvature-scale calculus не повторять.

## Потребитель
Главный мост «мерa историй → фактическое операторное чтение»: заранее известен точный дополнительный source, который нельзя потерять при использовании N09 бюджетов.

## Зависимости и запуск
После регистрации в main, проверки живых PR и назначения одного писателя.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_weighted_source_2026-10-16/`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Двухузловая неоднородная weight-проба, actual adjoint equality, истинное unitary transport в правильных Gram spaces; total simultaneous frame transformation сохраняет scalar price. Односторонняя заморозка веса и неверный unweighted-unitary тезис должны отвергаться.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
