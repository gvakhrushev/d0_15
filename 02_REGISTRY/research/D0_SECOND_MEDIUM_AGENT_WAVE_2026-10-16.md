# Вторая волна: девять ограниченных исполнителей и один CONTROL; основной синтез не останавливается

2026-10-16. Repository: `gvakhrushev/d0_15`.
**Публикация поручений, не запуск агентов и не регистрация в main.** Научный потребитель — действующий #334. N01 проводит краткую штатную регистрацию девяти WORKER; остальные получают обычные Task-ID, не доступ к чату или ZIP.

## Обязательное обновление входов перед запуском
До исполнения прочитать [CURRENT_INPUT_DELTA.md](sources/d0_medium_wave2_2026-10-16/CURRENT_INPUT_DELTA.md). Новый SOURCE `33267713b2e6d3e78af7789547b00f50cdceb43d` уже построил полную регулярную карту и exact off-shell matter reduction. N05/N06 теперь реализуют и проверяют их reusable interfaces, а не выводят заново; N07 собирает оставшийся saddle-operator `[H_red,T*;T,0]`. Это уточнение имеет приоритет над историческими входными формулировками briefs; ID, выходы и границы записи сохранены.

## Что уже сделано первой волной
На снимке main `add17919b344f0e46115619aa53d2173ecdcf219` задачи #325 (transverse matching), #326 (common shear), #327 (measure C1 bound), #328 (input closure selector), #329 (golden filter Lean), #330 (preparation second jet), #332 (anisotropic source), #333 (source reflection Lean) merged. Их результаты — входы, не новые поручения. #331 `WRK-A4D-MOVING-SCALE-VARIATION` остаётся open/IN_PROGRESS. Общий workflow #324 merged; его не перестраиваем. #310 закрыт без merge; единственный successor этой научной задачи — #334, pinned `74e62cdc716e10883accba9d34ccf0e21d58eb65`. #322 и #323 сохраняют свои scope/ownership.

Материалы SOURCE опубликованы, но их приёмка не следует из числа файлов или статуса Draft. В частности, exact auxiliary unfolding не доказывает physical admission или Einstein-предел, а positive directional wave Hessian исключает только указанную first velocity, не все искривлённые решения.

## Что остаётся у ведущего
**Один собственный процесс → одна полная цена → реальные совместные уравнения → искривлённое решение/контролируемый предел.** BOOK00–01, tuple и M1 применяются структурно, от противного и через порождающие операции, а не перебором каталога действий. Средним агентам не поручается выбрать convenient Q, Info, физические scales, gauge, source или заранее желаемую меру.

Текущая фиксированная задача сборки — полный joint linearized Euler kernel того же bounded stored-native v8-сектора, затем его нелинейная разрешимость; параллельно — native primitive/полноценный price допуск. Ведущий выбирает и доказывает физический ход. Агенты предоставляют ограниченные операторы/оценки/формализацию, которые этот ход фактически использует.

## Десять поручений
| № | Работа | Штатный ID |
|---|---|---|
| [N01](sources/d0_medium_wave2_2026-10-16/CONTROL_WAVE2_INTAKE.md) | CONTROL: регистрация, узкая formal intake и приёмка | `CONTROL-PLANE`, без новой scientific task |
| [N02](sources/d0_medium_wave2_2026-10-16/WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING.md) | Подключить принятую проверку зависимостей к действительному runner | `WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING` |
| [N03](sources/d0_medium_wave2_2026-10-16/WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER.md) | Lean: эквивалентность совместного ядра после Schur-исключения | `WRK-A4D-LEAN-SCHUR-STATIONARY-TRANSFER` |
| [N04](sources/d0_medium_wave2_2026-10-16/WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION.md) | Lean: перенос всех конечных программ и их первых jets | `WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION` |
| [N05](sources/d0_medium_wave2_2026-10-16/WRK-A4D-STORED-ADJOINT-TANGENT-MAP.md) | Полная допустимая касательная карта native stored-adjoint класса | `WRK-A4D-STORED-ADJOINT-TANGENT-MAP` |
| [N06](sources/d0_medium_wave2_2026-10-16/WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE.md) | Физическая matter-подготовка: полный shell/reference блок | `WRK-A4D-FULL-REFERENCE-MATTER-RESPONSE` |
| [N07](sources/d0_medium_wave2_2026-10-16/WRK-A4D-V8-FULL-HESSIAN-APPLY.md) | Полный Hessian–vector оператор одной v8-цены | `WRK-A4D-V8-FULL-HESSIAN-APPLY` |
| [N08](sources/d0_medium_wave2_2026-10-16/WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER.md) | Вес пространственных узлов без подмены stored-оператора | `WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER` |
| [N09](sources/d0_medium_wave2_2026-10-16/WRK-A4D-RAW-SOURCE-PRECISION-BUDGET.md) | Единый бюджет точности до исходной raw-нормы | `WRK-A4D-RAW-SOURCE-PRECISION-BUDGET` |
| [N10](sources/d0_medium_wave2_2026-10-16/WRK-A4D-CORE-PRIMITIVE-ADMISSION-SPLICE.md) | Конкретные композиции core-примитивов вместо нового общего аудита | `WRK-A4D-CORE-PRIMITIVE-ADMISSION-SPLICE` |

В каждом brief есть точный terminal, SHA, носитель/источник, write fence, named consumer, решающая проверка, запреты и self-contained handoff. Во избежание десяти несовместимых файлов все источники читаются с фиксированных входов. Новое принятое решение обновляет потребителя через ведущего, а не молчаливой заменой SHA.

## Общий математический интерфейс
Основной операторный путь использует **существующую** v8 цену

    S=Tr(rho_m Delta)+log(C Tr K)/beta-M Tr log A,
    Delta=D_stored^2, B=I-alpha Delta, K=B^m,
    A=(1-z)I+zK, beta=m alpha,
    sigma_aux=K/Tr K, X_aux=A^-1.

M=128 и полный workspace C сохраняются в их собственном типе. `rho_m` — physical matter with retained reference; auxiliary sigma/X не объявляются новой подготовкой или динамическими материальными полями. AF-terminal price, normal-volume Einstein reading и v8 H+J_program+R — различные владельцы, не три слагаемых одной цены.

Сохраняются actual stored-adjoint constraints, Lorentz links, observer, normalization, rank domains, all16 grades, полный физический shell/reference и все тепловые modes. Адресная PF probability, counting-site Hilbert weight и geometric volume не отождествляются без стрелки. Для родительского #334 остаются 10 packed metric rows/site, h=1/L, исходная unweighted raw-l1 сумма и независимо фиксированный source/comparator. `h^-2 * L^4` нельзя забыть. Внутреннее unitary/frame symmetry не объявляется nonlinear diffeomorphism symmetry.

## Параллельность и зависимости
Существующий лимит — пять live WORKER с учётом REVIEW/BLOCKED; на снимке один слот занимает #331. Первая отправка после регистрации: **N02, N05, N06, N10**. N03/N04/N08 можно выполнять независимо в освобождённых слотах. N07 строит operator evaluator на pinned формулах, но его native-facing завершение потребляет N05/N06. N09 получает совместимые quantitative interfaces, а не складывает ошибки разных теорий.

Ни один Lean worker не задерживает аналитическую работу ведущего: результат можно использовать в declared research scope до формальной приёмки, но нельзя менять его статус на Lean-proved. Один писатель на ветку и отдельный `.lake`/worktree. Общее изменение workflow принадлежит только N02; N01 не правит этот файл параллельно. Общие formal_registry/views изменяет CONTROL после согласованного narrow build, не два Lean-агента одновременно.

## Что считать завершением
**Результат = вычисленный/доказанный вход родителя + место подстановки**, а не красивый обзор, число PASS или список возможных исследований. N05 даёт пространство допустимых вариаций; N06 — настоящую matter response; N07 — полный bilinear Euler operator. Ведущий сам решает kernel/curved continuation и физическую интерпретацию. Нулевой отдельный covariance/source не означает исчезновения полного источника.

Изолированные конечные примеры помечаются как controls, общие тождества доказываются с их кванторами. Неразрешённая техническая проверка передаётся конкретным type/command/residual; длительный новый поиск меняет класс/план только через CONTROL. Восемь завершённых задач первой волны не возвращаются в manifest. Приёмка всего #334 не является prerequisite для чтения этих закреплённых research inputs.

## Регистрация и перенос в новый чат
N01 использует [тонкий адаптер](sources/d0_medium_wave2_2026-10-16/register_wave2.py) существующей транзакции первой волны. Он не создаёт новый registry/dispatcher, не пушит, не мерджит и не запускает агентов. До завершения registration/main intake новый agent может только читать/обсуждать входы, не открывать дубликат execution.

Первый переносимый запрос:

    Repository: gvakhrushev/d0_15
    Role: CONTROL intake N01, second medium wave 2026-10-16
    Read 02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md
    and sources/d0_medium_wave2_2026-10-16/CONTROL_WAVE2_INTAKE.md
    on the published #334 branch. Resolve live governance ownership first.
    Register this wave through the existing manifest and normal PR acceptance;
    preserve #331 and the single #334 scientific writer. No self-merge.

После регистрации передавать отдельному агенту Repository, exact `Task: WRK-...` из таблицы и указание читать штатный brief на main. Детали не копировать вручную из чата.

## Проверка самой передачи
Это организационно-научные briefs, не новые теоремы. Проверить уникальность IDs, непересечение write fences, согласованность parent/terminal, сохранение WIP и именованных dependencies. Адаптер обязан проверять SHA старого helper до его импорта. Обычная регистрация отдельно вызывает настоящие renderer/validators; локальные fixture-tests этой передачи не выдаются за проверку всего репозитория.

Локально выполнены 14 структурных tests в обычном и оптимизированном Python. Проверены новые brief IDs, потребители и непересекающиеся пути; read-only план даёт девять строк, сохраняет старую live state, parent и WIP. Входной helper восстановлен из прочитанных GitHub bytes и совпал с его точным Git blob. Fixture manifest/claims и исторические brief-заглушки служат только изоляции загрузки; это не настоящий main checkout. Реальный --apply, новые task rows на main, dispatch и научные/Lean проверки этой публикацией не выполнены.
