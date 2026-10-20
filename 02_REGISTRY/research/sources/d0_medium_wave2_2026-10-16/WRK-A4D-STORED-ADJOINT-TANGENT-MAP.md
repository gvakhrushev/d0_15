# WRK-A4D-STORED-ADJOINT-TANGENT-MAP

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-stored-tangent`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_stored_tangent_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N05. Полная допустимая касательная карта native stored-adjoint класса

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Derive and implement the complete linearized constraint operator for the owned homogeneous stored-adjoint family, with an explicit real basis or parametrization of its kernel and checked realization of declared symmetry directions; distinguish formal tangent vectors from integrable curves.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) — общий оператор, допустимый класс и все source jets.
- [`02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md) — неизменённая v8 цена и её точное вспомогательное представление.
- [`02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md) — точные adjoint/leg условия.
- [`02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md) — исходный совместный carrier и pairing.

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Использовать именно `A_xy^T h_x A_xy=h_y`, перенос собственной r-leg и настоящие Lorentz/coframe/observer relations первичного owner. Не считать h, native q, observer и ноги независимыми, когда определения их связывают. Из исходных definitions получить полный Jacobian C1 при однородном корне с параметрами d,o в закреплённом интервале. Привести site-форму и Fourier-symbol для произвольной разрешённой lattice phase, с reality/conjugacy conditions.

Программа должна выдавать матрицу/действие C1 и проверяемую parametrization kernel с названными координатами, а не каталог sampled ranks. Для порождающих symmetry curves дать actual нелинейное семейство и derivative. Для прочих formal vectors пометить integrability OPEN и выписать C2 compatibility (без заявления её всеобщей разрешимости). Сохранить affine shifts как отдельные исходные переменные, не придумывать их coupling в v8. Установленные pure-frame directions не равны автоматически всему gauge-kernel. Не решать классификацию kernel полного Euler — это ведущий трек.

## Потребитель
N07 и ведущий: ограничить полный Hessian на действительно правильную вариационную область; исключить повтор прежнего недопустимого conformal first jet.

## Зависимости и запуск
После общей регистрации. Независима от N03/N06. Фиксировать интерфейс C1 с ведущим до первой публикации; не ждать полного CI других агентов.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-STORED-ADJOINT-TANGENT-MAP`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_stored_tangent_2026-10-16/`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Исходный homogeneous curve и известная row-rotation должны проходить C1; прежняя запрещённая conformal curve — отвергаться с точной нарушенной строкой. Проверить full Lorentz tangent, свой r-edge и real Fourier pairing; не только frozen q.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-STORED-ADJOINT-TANGENT-MAP`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-STORED-ADJOINT-TANGENT-MAP`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
