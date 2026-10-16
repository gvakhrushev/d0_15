# WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-primitive-jet-lean`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_primitive_jet_lean_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N04. Lean: перенос всех конечных программ и их первых jets

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Formalize ordered-word intertwining, its exact telescoping residual, and its first-jet version with a moving intertwiner; expose branching/comparison hypotheses explicitly and specialize only to already owned primitive maps.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/A4D_FOUNDATION_FORCING_NOT_CATALOGUE_SEARCH.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_FOUNDATION_FORCING_NOT_CATALOGUE_SEARCH.md) — основания и структура доказательства без каталога.
- [`02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) — §0.3: уже построенные conditional v8 intertwining maps.

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Сначала проверить имеющиеся Lean-теоремы composition/naturality; переиспользовать их и добавить только недостающее. Формализовать для слова w точное разложение `V_w I - I U_w` в сумму одношаговых residuals с сохранением порядка. Первые jets задать как пары value/derivative с правилом произведения (алгебра двойственных чисел либо эквивалентная finite структура). Не убирать `dI` из `dV I+V dI=dI U+I dU`.

Получить индуктивное равенство для любого конечного слова и bound через суммы одношаговых ошибок при заданных norm bounds. Для ветвящихся программ требуется дополнительно доказанное согласование labels/preparations/tests; оформить его отдельной hypothesis, не считать, что теорема о словах автоматически покрывает нормализацию postselection. Один generic theorem вместо перечисления программ. Физический допуск v8 primitive остаётся предметом ведущего и N10.

## Потребитель
Связь BOOK00–01 с finite operator/source spine: доказательство бесконечного семейства конечных опытов через конечное число порождающих равенств. N10 поставляет реальные typed instantiations.

## Зависимости и запуск
После регистрации в main, проверки живых PR и назначения одного писателя.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_primitive_jet_lean_2026-10-16/`
- `03_FORMALIZATION/D0/Research/PrimitiveJetComposition.lean`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Узкий Lean build; некоммутирующие 2×2 матрицы; отрицательный контроль обратного порядка и замороженного dI. Никаких sorry/new axioms; conditional operator theorem не помечать физической вынужденностью.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
