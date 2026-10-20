# WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-w2-schur-lean`
Primary artifact: `02_REGISTRY/research/sources/d0_w2_schur_lean_2026-10-16/RESULT_RU.md`
Execution: `GitHub-first`

## N03. Lean: эквивалентность совместного ядра после Schur-исключения

Прочитать `AGENTS.md`, `00_WORK/README.md` и общий вход
`02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md` на опубликованном SOURCE.
Главная цель — вынужденный вывод ОТО снизу вверх из BOOK00–01, без каталога альтернативных действий.
Это ограниченное поручение; его конечный результат не заменяет физический вывод родителя.

## Точное обязательство
Formalize a generic finite-dimensional Schur kernel equivalence and congruence for an invertible auxiliary block, retaining direct source residuals, then specialize it to the stated same-price unfolding interface without assuming the physical block invertible.

## Закреплённые входы
Main при подготовке: `add17919b344f0e46115619aa53d2173ecdcf219`. Научный SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Main содержит принятые вспомогательные результаты; SOURCE содержит опубликованную, но ещё не принятую исследовательскую сборку. Исторический #310 закрыт без merge, #324 уже merged. Не писать в их ветки.

- [`02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`](https://github.com/gvakhrushev/d0_15/blob/74e62cdc716e10883accba9d34ccf0e21d58eb65/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md) — §§3–5, точное представление и Schur.
- [`03_FORMALIZATION/D0/Research/SourceReflectionKernel.lean`](https://github.com/gvakhrushev/d0_15/blob/add17919b344f0e46115619aa53d2173ecdcf219/03_FORMALIZATION/D0/Research/SourceReflectionKernel.lean) — принятый #333, не повторять pullback injectivity.

Входы читать по указанным SHA. Если их нет в main, получить отдельный read-only checkout точного SOURCE, не вливать весь #334 в WORKER. Программа результата может читать подтверждённый input tree через явно указанный параметр; сохранить точные содержательные хеши. Никакого обязательного ZIP или доступа к истории чата.

## Работа и научные границы
Для линейного блочного оператора [[A,B],[C,D]] при доказанной invertibility D формализовать явный изоморфизм `ker(A-B D⁻¹ C) ≃ ker H`, восстановление auxiliary component `-D⁻¹ C x` и обратное направление. Для adjoint/symmetric случая доказать блочную congruence; показать соответствие билинейных форм и норму reconstruction при supplied norm bounds. Inertia — только если имеющаяся библиотека позволяет её установить без нового большого спектрального проекта; это не обязательный terminal.

Сохранить прямые внутренние источники и показать, где они входят в правую часть reduced equation. Аналитические Gibbs/logdet теоремы не переносить в Lean через недоказанные axioms: специализация получает именно уже объявленные матричные hypotheses. Не формализовать заново 79 scalar controls и не требовать inverse всего физического H.

## Потребитель
Главный #334: использовать auxiliary elimination при построении полного joint Euler kernel, а не объявлять его ядро пустым из обратимости статистических блоков.

## Зависимости и запуск
После регистрации в main, проверки живых PR и назначения одного писателя.
Перед новым Draft выполнить `python tools/task_dispatch.py WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER`. Найденное исполнение продолжить с его владельцем, а не создавать второе. PLANNED на main не означает отсутствие работающего агента. Все девять новых tasks независимы по месту записи, но не все независимы по математическим входам.

## Разрешённая запись
- `02_REGISTRY/research/sources/d0_w2_schur_lean_2026-10-16/`
- `03_FORMALIZATION/D0/Research/SchurStationaryTransfer.lean`

Только эти научные/инструментальные пути и штатное start/retire собственной строки. Не менять общий source, цену, исходные квитанции, BOOK, claims, shared `.lake`, рабочие ветки других исполнителей или общий маршрут. Изменения общих Lean views/формального реестра — через CONTROL после узкого build и проверки импортируемой области; не оставлять доказательство сиротским к окончательной приёмке.

## Решающая проверка
Узкий Lean build, actual `#check/#print axioms` ключевых лемм, контрпример при необратимом D и пример с ненулевым reduced kernel. Изменение знака `-BD⁻¹C` должно нарушить конечный контроль.

## Why delegated
Интерфейс и потребитель уже определены. Здесь нужна ограниченная независимо проверяемая реализация/формализация, а не выбор новой физики или общий поиск искривлённых решений. Ведущий освобождается для вынужденности исходной программы и полной совместной динамики.

## GitHub execution contract
После разрешения запуска создать из текущего main указанную ветку; `python tools/task_lifecycle.py start WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER`; открыть Draft до содержательной записи. Несколько локальных расчётов объединять в один полезный checkpoint. Перед Ready выполнить проверки затронутых входов по существующей матрице; затем `python tools/task_lifecycle.py retire WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER`, регенерировать штатные views, сохранить результат вне удаляемого brief. Если научный terminal не выполнен, не retire ради зелёного статуса. Никакого self-merge или поднятия WIP. Полный CI не нужен после каждого промежуточного вычисления; он нужен при приёмке затронутого среза.

## Chat handoff
Repository, PR и SHA; точный результат; какой вход родителя теперь обеспечен; команды и фактически выполненные проверки; один оставшийся blocker. Подробные доказательства и логи — в Git. Не писать «GR закрыта», когда доказана конечная условная лемма.
