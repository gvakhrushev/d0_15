# Волна средних агентов: освободить главный синтез D0 → ОТО

16 октября 2026. Repository: `gvakhrushev/d0_15`.
Governance owner: существующий **#324**, не новый процесс/dispatcher.
Scientific consumer: существующий **#310**.
Статус этого документа: **поручения подготовлены; девять новых WORKER-строк ещё не установлены в main; агенты не запущены**.

## Решение пользователя и разделение труда
Пользователь предлагает вынести в средние модели интеграцию, Lean, CI, refactoring и ограниченные теоретические расчёты, продолжив с сильной моделью основной прорывной синтез. Принято именно это разделение: не десять независимых теорий и не ожидание окончания всей волны.

Полное стратегическое видение, включая минимальное замыкание, pi0, золотую структуру, архив и резонансную материю, сохраняется в [существующем документе](https://github.com/gvakhrushev/d0_15/blob/cd02a65de1c708eae113b03ca63392e1641c427c/02_REGISTRY/research/D0_RESEARCH_STRATEGY_RU.md).
[Общий контракт исполнителей](sources/d0_medium_agent_wave_2026-10-16/EXECUTION_CONTRACT_RU.md) фиксирует потребителей, статусы и пределы ускорения. Оформление можно пакетировать; гипотезу нельзя называть проверенной теоремой.

Пользовательское «закрыто» относится к результатам в объявленных математических классах: геометрия записи, Einstein-ковектор, выбранный полный AF-price, минимум подготовки, корректный coherent compiler. Их не повторяют с нуля. Они пока не означают, что один admitted native процесс уже выводит все уравнения ОТО.

## Десять самостоятельных поручений
M01 исполняется в существующем CONTROL #324. M02–M10 — девять текстовых WORKER briefs для штатной регистрации. Они не меняют классы/терминалы существующих EXPENSIVE #202/#310/#317.

| № | Поручение | Конкретный выход | Немедленный потребитель |
|---|---|---|---|
| [M01](sources/d0_medium_agent_wave_2026-10-16/M01_CONTROL_INTAKE.md) | Регистрация и последовательная приёмка #323/#324/#322 | Согласованная queue, проверенные frozen slices, доставка после независимого review | Следующие чаты и все executors |
| [M02](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-CERTIFICATE-INPUT-CLOSURE.md) | Транзитивные входы research checks | Conservative affected-input selection и failure fixtures | M01 и scientific CI |
| [M03](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-LEAN-GOLDEN-CURVATURE-KERNEL.md) | Lean: golden-cylinder polynomial filter | Общая degree-four теорема и золотые corollaries | Finite curvature/source consumers |
| [M04](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-LEAN-SOURCE-REFLECTION.md) | Lean: source reflection | Dual injectivity, error bound, full symmetric packing | M05 и полный source-lift |
| [M05](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL.md) | Десять transverse matching rows | Явный adjoint/annihilator и условие raw stationarity | Главный native evolution |
| [M06](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-PF-MEASURE-SOURCE-TRANSPORT.md) | PF → spatial source transport | Finite C1 measure/source error bound с moving partition | Главный вывод меры |
| [M07](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-ANISOTROPIC-NORMAL-SOURCE.md) | Анизотропная мера | Полный covariance/shape covector, frame-invariant tests | Решение о retained physical source |
| [M08](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-MOVING-SCALE-VARIATION.md) | Полевые масштабы и observer | Все Euler/boundary/normalizer terms | Общие физические уравнения |
| [M09](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-PREPARATION-SECOND-VARIATION.md) | Некоммутирующий second jet подготовки | Envelope/Hessian и safe-domain bounds | Nonlinear joint reduction |
| [M10](sources/d0_medium_agent_wave_2026-10-16/WRK-A4D-FLAT-SHEAR-COMMON-SOURCE.md) | Общий источник на плоской shear-пробе | Совместимая source-row таблица, не сумма разных опытов | Первый тест новой полной конструкции |

## Что можно отдавать сейчас
Тексты уже самодостаточны для передачи новому агенту. **M01 может сразу взять CONTROL intake**. Независимый read-only review и изучение входов остальных задач тоже не требуют нового рабочего PR.
Для нового исполнения WORKER требуется штатная регистрация, main intake, live-PR проверка и назначенный писатель. Это отдельные события, не сделанные публикацией текста.

Первый набор после регистрации: M02, M03, M05, M06, M10. Одновременно не более пяти WORKER, считая BLOCKED/REVIEW, а не пять новых поверх пяти старых. M04, M07, M08, M09 подключаются по свободным слотам; независимые расчёты не ждут Lean M03/M04. Можно начать с четырёх и оставить один слот для срочной проверки/интеграции.
Все научные входы зафиксированы на SOURCE `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`. Main при подготовке — `fa2b04b9c8aae5a0b8470322d6091712ce56567a`, процесс #324 — `1d0fbb695e4393d01257851337e64bf271fc0c85`. Это снимки, не live heartbeat.

## Регистрация без конкурирующего реестра
[register_wave.py](sources/d0_medium_agent_wave_2026-10-16/register_wave.py) читает девять briefs, добавляет их к существующему manifest и вызывает существующие renderer/validators. Он не создаёт второй registry, не запускает агентов, не пушит и не сливает PR.

```sh
python 02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/register_wave.py --check
python 02_REGISTRY/research/sources/d0_medium_agent_wave_2026-10-16/register_wave.py --apply
```

`--check` read-only. `--apply` разрешён только владельцу ветки #324 на чистых затрагиваемых путях; при ошибке восстанавливаются только его manifest/brief/generated edits. Старые задачи и лимиты сохраняются. Применение после retirement отвергается при наличии прежнего brief в Git history, чтобы не воскресить закрытое исполнение.
M01 проверяет diff и независимую приёмку. После регистрации/слияния обычный запуск:

```text
Repository: gvakhrushev/d0_15
Task: WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL
Read the registered brief on main and execute GitHub-first.
```

## Что остаётся у ведущей модели
Средним агентам не поручается «выбрать» удобный Info, меру или compensator.
Ведущий продолжает один combined synthesis: собственная пространственная мера и first jet; одно физически выбранное полное действие; admitted moving-field update, сохраняющий matching и весь source.

Новый SOURCE требует двух обязательных тестов:
1. [Flat shear](https://github.com/gvakhrushev/d0_15/blob/dfaf7c8df509d5abd83fa60a185ad530feadc9b5/02_REGISTRY/research/A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md): исправленная determinant/AF-price preparation имеет нулевой source на заданной плоской trace-free пробе, heat — ненулевой. Это исключает конкретную сокращённую сумму, а не всю D0.
2. [Matching graph](https://github.com/gvakhrushev/d0_15/blob/dfaf7c8df509d5abd83fa60a185ad530feadc9b5/02_REGISTRY/research/A4D_NATIVE_MATTER_CLOCK_RECORD_BINDING.md): десять transverse equations и прямые matter contributions не следуют из достижимости десяти metric variations на графе.

Итак, доказанная мера сама по себе не объявляется последним автоматическим шагом. Общая конструкция должна одновременно сохранить цену, observer, подготовку и полные уравнения. Это цель главного трека; M05/M06/M08/M09/M10 дают ему проверяемые входы.

## Проверка данной передачи
Локально прошли 14 structural registration tests в обычном и оптимизированном standard-library Python: read-only planning, девять новых строк, idempotence, сохранение live state/лимитов/родителя, collision rejection, успешная локальная транзакция, rollback при fixture-validator failure и отказ записи в чужой ветке.
Транзакционные tests используют явно искусственные renderer/validator fixtures. Это НЕ запуск настоящих repository guards или научных suites. Реальный `--apply`, main registration, dispatch, новые Lean proofs и scientific closure не выполнены этим пакетом.
