# B22: независимая проверка A10 private NPS recovery

**Вердикт: A10 подтверждается для собственного указанного native интерфейса и конечного локального примера; существенной ошибки не найдено.** Замена sharp oracle на **весь** noisy NPS square word корректна при заявленных scalar-effect, live-address, canonical-cut и retained-reader условиях. Она снимает прежнюю потребность `K_b=w_b⊗I_Spin` именно для этого способа восстановления: Spin-зависимый обратный оператор может быть возвращён действительным разрешённым `A_N*`, а не недоступным WORK-only вращением. Это не воспроизведение full geometric H.1 и не доказательство physical C. `GR_closed=false`.

Проверяемый пакет: [PRIVATE_NPS_RECOVERY_RU.md](../../../../../../../d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round10/PRIVATE_NPS_RECOVERY_RU.md), `nps_private_recovery.py`, `check_private_recovery.py`, `supported_private_plane.py`, `certify_private_corrections.py` и закреплённые inputs. Скрипт сертификата записывает результат рядом с собой, поэтому для сохранения A без изменений весь пакет запускался из отдельной временной копии. Сгенерированные `CERTIFIED_CORRECTIONS.json` и `PRIVATE_RECOVERY_DAG.json` совпали с оригиналами **побайтово**.

## 1. Noisy oracle, исходный input и контроль записи

Правильный oracle A10 — не исходный sharp `A_f` и не самостоятельная условная Kraus-инверсия, а полный буквальный `A_N`: независимые `A_f,A_b`, NPS pointer-copy/sign, E0 и точное echo, применённые к текущему bank с приватными `r',t'`. Birth-включения не обращаются. Для истинной canonical embedding `i` и каждой доступной внешней coarse ветви `b` проверяется именно

```
i* A_N* Pi_b A_N i=q_b I,
V_b=Pi_b A_N i/sqrt(q_b),
P0 A_N* V_b=sqrt(q_b)i.
```

Приватные `r',t'` физически рождаются в `v`, дважды оплаченно unprepare и заполняются известным coarse bit через `CX(r,r')`; состояние после этого действительно равно условной `V_b` на текущем полном bank, с произвольными связями неизвестного Spin/reference. Это 2 births + 23 calls. Внешний `r` остаётся control-only на каждом literal gate; внешний `t` не адресуется до отдельной bright-correction. Следовательно соответствующие coarse и invalid projectors сохраняются на всех колонках, пока они действительно живы.

На объединённой record-арене `q_0` и `q_1` не объявляются одной константой: equality predicate выбирает свои ветви, и рекурсия применяется к каждой из них. `P0` тестирует только указанный canonical processor WORK, включая private pointer/tail и источник, но не Spin, внешний record, oldRIGHT или фазовый rebit. Настоящая born frame переводится в computational zero через оплаченные G-inverse и затем восстанавливается. Если текущий H.1 input содержит дополнительный mutable DATA или уже запечатанный bank wire, его нельзя включить в этот predicate или replay без отдельного допустимого интерфейса.

## 2. Spin-coupled centre и сохранение failure

В `--spin-coupled` выбран исходный native `A_b=SourceI A_f`, `A_f=G_port³`, а не добавленная локальная Spin-операция. Реальный WORK-профиль на ветвях имеет линейно независимые коэффициенты при `I` и `L_i`; это демонстрирует, что прежнее WORK-only достаточное условие B19 не покрывает такую ветвь. При этом весь разрешённый square word и его raw inverse доступны без индивидуальной адресации Spin. Воспроизведение подтверждает noisy branch, равенство всех четырёх Spin, двух phase и двух внешних record колонок и полную Gram-матрицу **сохранённого** failure complement.

Это не доказывает scalar effect произвольного постулированного full H.1: его `i*A_N*Pi_b A_N i=q_b I`, доступность настоящего `A_N/A_N*` и все live-support/mark условия должны быть отдельно установлены для выбранного field instance. B21 выгрузил исходные геометрические компоненты, но большой seven-bank word и complete reader/seal catalog ещё не сформировал.

## 3. Fixed point, фактические коррекции и стоимость

Используются два раздельных exact native predicates: полный canonical `P0` и `Pi_equal(r,r')`. Указанный owner real phase rebit и common `G^624` удовлетворяют нужному stability interval; это исходные `G/CX/SourceI` последовательности с платной маршрутизацией, а не новый комплексный primitive. Проверяемая хронологическая рекурсия

```
A_previous; R_equal; native_inverse(A_previous); R_P0; A_previous
```

соответствует указанному matrix-order `A_(n+1)`. Рекурсия добивается восстановления на истинном input, не удаляет неудачные выходы и учитывает branch-dependent good phase. Две phase corrections и bright-tail target применяются к реальным born helper wires. Signed-plane primitives проверены на **всех 128** dirty port/Spin/control/target колонках для четырёх различных буквальных fixtures; Fourier-level checker отдельно перебирает все ordered planes и оба selector values. Это не полная символьная матрица trillion-call программы.

Подсчёт raw inverse корректно различает две semantics: рекурсивный `native.inverse_word` разворачивает каждую физическую вложенную inverse-операцию, тогда как логический SO3 inverse разворачивается в последовательность signed letters **до** назначения каждому из них собственной native plane-схемы. Из исходных `(G,CX,SourceI,G_off)` следуют сохранённые A10 recurrence и инвентаризация на нижних реально исполненных уровнях.

Трёх командный replay с `python3 -B -W error` дал:

| Проверка | Результат | Что фактически выполнено |
|---|---|---|
| `check_private_recovery.py` | PASS, 23 проверки | rounds 0–2; наибольший реальный word `131325` calls |
| `check_private_recovery.py --spin-coupled` | PASS, 25 проверок | rounds 0–2; наибольший реальный word `131550` calls |
| `certify_private_corrections.py` | PASS, 12568 проверок | 320-bit outward interval DAG, исходные literal small macros и целые count recurrences |

`n=12` fixture имеет `951278222451` стадий, включая действительные births, original outer NPS, private recovery и six-copy archive; это **заданный и пересчитанный конечный DAG**, а не выполненный gate-by-gate replay. Интервальная all-input state-error bound `≤8.65351877654·10^-23`, а полная длина times error `<8.232·10^-11`. Пять private и шесть archive births, старый и новый cut и вся failure поддержка остаются; никаких бесплатных нулевых blank или измерений не вставлено.

## 4. Истинный конечный q-gain и независимые строки

Сертификатор вычисляет finite cold конкретных слов при фиксированных correction words, а не подставляет идеальный предел. На его локальном fixture `q=p²+16p^12` и collar радиуса `2^-30` сохранены целые interval endpoints для `c_actual>0`, `c'_actual<0`; приведённая в A10 расширенная десятичная оценка корректно содержит результаты. Для фиксированного `0<z<1` это даёт положительный конечный

```
−2 r z c_actual c'_actual /(1−z+z c_actual²).
```

Это (q)-source на **generated-copy chart**, где повторно используемый recovery действительно строится из соответствующих копий A. Он не равен автоматически всем самостоятельным исходным gate-occurrence derivatives и не доказывает их точную стационарность: для последних необходимы собственные N·error, допустимые нормы/reader transport, comparison steps и right lifts. A10 сохраняет эту границу и не дифференцирует дискретный индекс native word. Положительный диагностический gain не является вычисленным геометрическим gain H.1.

На проверенной layout формулы `D=974108908297084`, `d_final=65536`, `L=132`, `425D` учитывают staged births. Независимая сверка константной части по реальным pre-stage widths даёт `28 + 60·32 + 992 + 23·1024 + 63·1024 + 132·65536 = 8741756`, поэтому `D=8741756+1024 N_recovery`. Переносить эти числа на 7-bank H.1 нельзя без нового literal schedule и всех дополнительных reader/mark stages.

## 5. Итоговая область и проверка неизменности

Численные replay corner errors для rounds 0–2 в обоих случаях `<9·10^-13`; существенно более строгая bound `8.65·10^-23` относится к **интервально сертифицированному n12 DAG**, а не к direct replay n12. Проверены исходные hashes snapshots, результаты команд и совпадение повторно сгенерированного DAG/certificate; hash/receipt находятся рядом с этим отзывом. Все скрипты были выполнены в копии, исходные A-файлы не правились.

Для полного приложения нужны actual H.1 bank square word, canonical input и связанные forward/back slots, подтверждённые positive all-input branch laws, физически live адреса, все старые marks и будущие оплаченные readers, полный independent-source norm и original Cost−Info/Book aggregation. В B21 найдены и выпущены истинный SC6, оригинальные F/R адреса, конкретный конечный chart и численные Julia targets, но эти части ещё не заменяют полный seven-bank word. A10 не заявляет и этот review не устанавливает выведение ОТО.
