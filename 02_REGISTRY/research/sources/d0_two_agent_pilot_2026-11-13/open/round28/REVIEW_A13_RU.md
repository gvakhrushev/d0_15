# B28. Независимая ограниченная проверка обратимых selectors A13

**Результат:** существенной ошибки в A13 не обнаружено. На заявленном checkpoint с computational-zero work схемы реализуют точный логический XOR decoder и first-success **меток**, оставляя исходные входные провода неизменными. Builder и checker выполнены в отдельной копии `round12/round13`: все шесть итоговых JSON восстановлены побайтно, оригинальные проверки повторены. Независимо проверены 5 170 таблиц, prefix ranks, граничные случаи, а также **все 52 444 771 логических gates** трёх выдаваемых decoder streams на корректность адресов, счёта и read-only inputs.

Это результат для логического базиса `X/CX/CCX`; он не выдаёт физический native selector. Full source-DAG dispatch, quantum payload routing, полный READY/`alpha_h`, физическое `C` и GR остаются открытыми. `GR_closed=false`.

## 1. Что повторено и что проверено независимо

[ISOLATED_REPLAY.json](ISOLATED_REPLAY.json) фиксирует входные hashes и повтор A13 `build_selector_circuits.py` + `check_selector_circuits.py` во временной копии. Побайтно совпали три selector circuit JSON, first-success JSON, compilation JSON и check JSON. Исходный checker повторил `10 922` equality, `5 704` comparator, `1 024` reduced-selector, `67` actual-prefix, `5 170` row, `500` real-width row и `1 064` first-success проверок. Ни один файл в direct/round13 не изменялся.

[check_a13_independent.py](check_a13_independent.py) отдельно восстанавливает исходную семантику из A12 partitions, не импортируя A13 builder/checker для ожидаемых значений. Он проверил:

* все `5 170` `palette×kind` rows по исходным exact counts; `198` нулевых длин ready-отрезков, все границы непустых интервалов и семь недопустимых binary `j` у internal palette;
* все `67` raw-prefix кодов `n=0,1,6` независимо вычисленным остановом и лексикографическим rank, включая suffix;
* `32` signed-literal truth-table случаях, `2 730` малых equality и `2 852` comparator случаях с произвольным target, а также 72 независимых реальных широких row-случаях;
* полную отдельную synthetic palette на `512` входных `(j,g,f,y)`, включая недопустимый `j`, нулевые интервалы, повторный ненулевой threshold, retained suffix и dirty output; обратный gate word возвращает вход и work;
* все `128` последовательностей READY для обоих настоящих cap7 label widths `2,6`, с четырьмя наборами retained labels и начального output на каждый случай — `1 024` независимых first-success случаев.

Synthetic hostile-control: для cumulative boundaries `[3,3]` и codes `[2,3,0]` нужны **оба** перехода, `1 xor 3 = 2`; отбрасывание одного из одинаковых ненулевых thresholds даёт неверный code. A13 сохраняет оба перехода. В трёх настоящих таблицах встретились нулевые длины, но повторных ненулевых thresholds в данных snapshot не оказалось; fixture проверяет общий случай, а не утверждает, что такая строка реально встретилась. Второй hostile-control: XOR всех успешных меток `1 xor 2=3` отличается от первой успешной метки `1`.

## 2. Структурное доказательство на произвольных колонках

**Signed controls и equality.** Для каждого значения `a,b` точны Boolean тождества

```
(1−a)b = b xor ab,
(1−a)(1−b) = 1 xor a xor b xor ab.
```

Представляющие их `X/CX/CCX` меняют лишь target, не исходные контролирующие биты. Цепь произведений фиксированных literals записывается в чистый work, target XOR-ится последним произведением, затем цепь разворачивается в обратном порядке. При любом target `y` это даёт `y xor [x=pattern]`, вход `x` на каждом gate read-only, work возвращён в zero. Крайние случаи с нулём и одним control отдельные и проверены. Для грязного work эта семантика не заявлена; reverse word остаётся обратным как общая перестановка.

**Unsigned threshold.** Начиная с `b0=0`, на i-м bit вычитания постоянного `t` используется

```
t_i=0: b_(i+1)=(1−x_i)b_i,
t_i=1: b_(i+1)=1−x_i+x_i b_i.
```

Это две точные Boolean таблицы исходящего borrow. По индукции по ширине итоговый borrow равен `[x<t]`. Его XOR в arbitrary output и последующее обращение forward pass очищают **все** borrows, не меняя register. `t=0` даёт identity, `t=2^width` — X output. Доказательство не зависит от ширины 94, 1374, 1580 и не требует перечисления `2^1580` входов.

**Prefix и thresholds.** Каждый из конечных исходных Golden words отображается в принадлежащий A12 `(kind,rank)` с правильным знаком порядка; исходные Golden bits и неиспользованный suffix не переписываются. Соединение `rank·2^r+fair` есть лишь назначение адресов bit-register, а не неоплаченная арифметическая операция. Если коды последовательных labels — `c_i`, для интервала позиции `x` обновление

```
y xor= XOR_i ([x<t_i] · (c_i xor c_(i+1)))
```

телескопируется в код единственного непустого интервала. Zero-length interval в общем случае требует сохранить одинаковые границы и оба XOR masks, кроме нулевого threshold, predicate которого всегда false. В каждой row отдельный чистый equality flag выбирает `(j,kind)`; её обратный проход очищает flag и все borrow work. Если `j` не принадлежит palette, не активируется ни одна строка, output не меняется. Обратный prefix после всех rows очищает временные `kind,rank`. Итог на всех data/output inputs при clean work:

```
|j,g,f,y,0_work> -> |j,g,f,y xor decode(j,g,f),0_work>.
```

Это равенство линейно распространяется на суперпозиции и внешние корреляции: оно не требует измерения `j,g,f` и не стирает retained suffix.

**Первая успешная метка.** С `survive_0=1` и чистым work рекурсия

```
chosen_i=survive_i AND ready_i,
survive_(i+1)=survive_i xor chosen_i
```

даёт `survive_i=AND_{k<i}(NOT ready_k)`; следовательно `chosen` one-hot в первом успехе или полностью нулевой. Контролируемые XOR записывают только его label и итоговый READY в произвольный выход, а обратный проход очищает выбранные и survival bits. Все seven attempt labels и flags сохраняются. Это классически-адресная когерентная map на basis labels; она не копирует и не маршрутизирует произвольный неизвестный quantum payload.

## 3. Полный логический поток и counts

[stream_audit.py](stream_audit.py) прошёл каждый выдаваемый `selector_word(plan)` без создания списка gates или состояния размерности полного Hilbert. Для каждого tuple проверены тип/arity, различные провода, диапазон и отсутствие `palette/golden/fair` среди targets. Суммы точны:

| Decoder | `X` | `CX` | `CCX` | Всего |
|---|---:|---:|---:|---:|
| internal | 478 828 | 1 089 222 | 1 089 479 | 2 657 529 |
| top | 3 478 720 | 19 440 642 | 19 454 976 | 42 374 338 |
| report | 691 540 | 3 323 278 | 3 398 086 | 7 412 904 |

Итого просмотрено `52 444 771` логических gates, ноль targets на входных проводах. Это проверка всего **описанного gate stream**, а не применение его ко всем квантовым input states или physical native execution. [FIRST_SUCCESS_COUNT_REVIEW.json](FIRST_SUCCESS_COUNT_REVIEW.json) независимо сверяет оба first-success word и умножение для 1054 slots/cap7/10 top calls: на report `X=3 776 997 052`, `CX=9 400 485 374`, `CCX=9 403 481 772`. Подсчёт касается только фиксированных decoders и label routing, без source stack, payload, factories или clock.

## 4. Дополнение A13/B27 о native zero-work

[check_native_zero_content.py](check_native_zero_content.py) выполнил ограниченную независимую проверку позднего дополнения: совпадение source hashes с B27 и native owner, точный logical→native mapping, пустые `Execution.blank_wires`, защищённый oldRIGHT, отсутствие касания `palette/golden/fair` и все **34 122** буквальных gates с правильным 11-call `SWAP; SourceI²; G; SourceI²; SWAP` для `1389/1595/118` output+work targets. Результат — [NATIVE_ZERO_REVIEW.json](NATIVE_ZERO_REVIEW.json). Он композиционно потребляет проверенную в B27 exact all-column identity `G_q^-1 tensor I_port tensor I_Spin`; больших матриц здесь повторно не строили.

Существенное условие сохранено: `Execution.blank_wires` в этом API означает уже введённый computational zero, а не физическое RAW состояние `v=(sqrt(p),p)`. Поэтому поле оставлено пустым; истинный `v` и будущий платный birth/clock ledger указаны отдельно. Доступность одного объявленного порта, необходимые CX routes, неприкосновенность oldRIGHT и реальные рождения являются условиями реализации. Это выданные native **компонентные** слова подготовки zero, не полный native decoder.

## 5. Проверенное дополнение: точный native CZ

Отдельно проверено последующее дополнение A13 к B27. Само точное `CZ` уже принадлежит исходному owner: [§7dk, формула (971)](../../../../A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L89715), где выписан uncancelled word стоимостью `20 CX+5 SourceI`. Проверяемый здесь новый результат — конкретный emitted word и сокращение за счёт общего маршрута до 13/19 вызовов, а не новая теорема существования `CZ`. Для двух обычных битов `c,t` с одним общим SourceI port и quaternion Spin

```
c+t−(c xor t)=2ct,     L_i^(2ct)=(−1)^(ct) I_Spin.
```

Поэтому исходный owner word реализует `CZ(c,t) tensor I_Spin` на всех колонках. При одном из `c,t`, совпадающем с port, counts `8 CX + 5 SourceI = 13`; если оба вне port — `14 CX + 5 SourceI = 19`. Требуются разрешённые маршруты к тому же port и защита oldRIGHT, но не нужны clean resource, measurement или postselection. Равенство конечных операторов не переносит автоматически старую отмеченную историю и её стоимость на сокращённый маршрут: для него нужны собственные реальные стадии, marks и clock. Произвольные port и Spin восстанавливаются на границе полного word; промежуточные состояния и стадии остаются реальными и платными.

[replay_native_cz.py](replay_native_cz.py) скопировал owner compiler и native_execution в отдельную rootlike структуру; исходный `NATIVE_CZ_CHECK.json` воспроизведён побайтно. Отдельный signed-permutation interpreter, не использующий owner matrix executor, проверил все `96` basis columns четырёх заявленных размещений и оба inventory. Подробности — [NATIVE_CZ_REVIEW.json](NATIVE_CZ_REVIEW.json). Это уточняет B27: **CZ уже имеет** предъявленное exact native word при указанных условиях; полные `X/CCX/H` и source processor отсюда не следуют.

## 6. Оставшиеся переходы и воспроизведение

Логические `X/CCX` и адресный controller ещё требуют фактических допустимых native слов; совпадение output probabilities существующих measurement/feedforward H/Toffoli factories не доказывает их all-column coherent H.1 dilation. Остаются независимые физические fair resources, source-DAG stack/offset dispatch, native signed-involution integration, quantum payload routing, все реальные prefix/reader/seal marks и объединённый clock/READY. Все попытки и failure records должны быть сохранены. Поэтому ни `alpha_h`, ни Cost−Info, ни GR этим review не закрываются.

Все собственные checks пишут только в `open/round28`:

```
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round28/replay_a13_isolated.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round28/check_a13_independent.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round28/stream_audit.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round28/check_firstsuccess_totals.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round28/check_native_zero_content.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round28/replay_native_cz.py
```

Они читают input snapshots из direct/round12/round13; первый выполняет запись A13 builder/checker только во временной копии. Контрольные суммы собраны в [RECEIPT.json](RECEIPT.json).
