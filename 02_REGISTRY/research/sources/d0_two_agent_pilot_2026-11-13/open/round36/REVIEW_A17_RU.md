# B36. Независимая проверка общей ten-sign сборки A17

## Вывод и границы

Для исходного `report_assembly.py` SHA-256 `d2f164aa81b45c68e2d64352b53fcf5dd7b264cf008478a9458eaa0d06fbec54`, plan `a7cc6639a5f5200de7c5244bfcaeaa27433e1e6c5458d16d9fa384e4e4401c80` и compilation `303ecd70a75c4a0141098f66533d4f3c57d3d8816d42685d84dc5f016eac5e26` проверенные глобальные адреса, ресурсы, selector/sign inputs и целевой report effect согласуются с A13/A15/A16/B31. Значимых расхождений в проверенном scope не обнаружено.

**Успешное событие — совместное `REPORT1=1` и `all_READY=1`.** Один `report_wire` не включает глобальный READY. Source-bank/SITE preparation, весь физический native stream, RAW birth admission, полный comparator/marks/clock и Cost−Info не построены. `physical_C_closed=false`, `GR_closed=false`.

## 1. Общий SITE, disjoint banks и input roles

[INDEPENDENT_PLAN_CHECK.json](INDEPENDENT_PLAN_CHECK.json) независимо проходит действительные события A15 для обоих корней и восстанавливает локальное распределение A16 без вызова A17 `make_plan`. Затем заново отображает все десять walks и postprocessor в глобальный namespace:

* восемь проводов `SITE[0..7]` идентичны для всех walks; `sigma` — отдельный incoming wire, `0→−1`, `1→+1`;
* два `S` и восемь `T` имеют disjoint private intervals, независимые источники и собственные delta; передача postpalette — именно `[S1,S2,T1..T8,sigma]`;
* 180 Choi copies занимают 3 960 wires, 16 CAR DATA — 192, их 16 RIGHT — 112: всего 4 264 подготовленных external source wires;
* 10 248 262 fair outputs принадлежат разным B31 banks. Для всех fair ranges проведены 22 377 независимых проверок начала/середины/конца, уникальности 143 local wires и READY local85;
* selector/first-success и postprocessor дают ещё 1 065 READY flags; всего на AND поступает 10 249 327 фактических flags.

Интервальная проверка охватывает все отведённые роли без перечисления миллиардов проводов. Она не подтверждает физическое наличие states. [GLOBAL_NATIVE_BINDINGS_CHECK.json](GLOBAL_NATIVE_BINDINGS_CHECK.json) дополнительно сверяет 128 фактических lazy native blocks четырёх глобальных walk и три реальных отображения B31 с port/Spin/aux и protected oldRIGHT; полный native stream не разворачивался.

RAW inventory на один report — **1 486 712 521** новых RAW-v inputs: 21 210 979 для processor ZERO, 76 Golden и 1 465 501 466 = `143·10 248 262` для fair banks, включая их outputs. Преобразование ZERO выполняется принадлежащим owner `G†v=0`; fair output не преобразуется отдельно второй раз. Эта сумма не включает 4 264 уже подготовленных source wires, входной SITE/sigma или происхождение общего port/Spin/aux/oldRIGHT: они являются отдельными входными/admission обязательствами. Алгебраический список не доказывает факт рождения и доступность соответствующих физических стадий.

## 2. Native READY без ложного успеха относительно flags

Для `K=10 249 327` сохранённых flags цепочка использует `K−2` clean AND-work wires и `2K−3=20 498 651` логических CCX-вхождений. Вычисление идёт вперёд, core копирует полную конъюнкцию, обратный проход — **literal adjoints именно фактических native compute blocks**.

Если хотя бы один фактический input flag равен нулю, первый соответствующий CCX имеет нулевой control и в A14 native реализации является **точной identity** даже на произвольных aux/port/Spin. Его новый clean target остаётся нулевым; все следующие prefix targets и core тогда точно неактивны. После истинного обратного прохода все рабочие регистры и произвольное запутанное окружение возвращаются, а изначально нулевой `all_READY` не устанавливается. Этот аргумент действует также на суперпозициях в подпространстве всех неправильных input flag patterns, поскольку flags служат read-only controls.

[EXACT_NATIVE_READY_CHECK.json](EXACT_NATIVE_READY_CHECK.json) независимо исполняет действительные G/CX/SourceI слова над точным кольцом `Z[a]`, `a=sqrt(p)`, `a⁴+a²−1=0`, с буквальным `L_i=diag(J,−J)`. Пройдены все 112 плохих K=3 patterns × arbitrary port/Spin/aux columns и все 64 K=4 cases с нулём в каждой позиции. Hostile повторение forward approximate CCX вместо истинного inverse оставляет рабочий residual. Доказательство no-false-positive относится к **фактическим входным flags**, clean AND work и изначально нулевому output: оно не доказывает, что upstream approximations правильно сформировали flags, и не устанавливает exact scalar ready при all-one flags.

## 3. REPORT, полный effect и подготовка source

A13 postdecoder выдаёт `label,post_READY`; ideal extraction записывает

```
report_wire ^= post_READY AND NOT(label).
```

Поэтому при `post_READY=1,label=0` report может стать единицей даже при `all_READY=0`. Требуемый consumer должен проверять **оба** результата. Actual extraction использует approximate CCX: при `post_READY=0` она точно неактивна, но при `post_READY=1,label=1` точного отсутствия неправильной амплитуды не следует. [REPORT_EXTRACTION_CHECK.json](REPORT_EXTRACTION_CHECK.json) показывает эту ненулевую амплитуду на точном k=1 diagnostic; это не оценка настоящего огромного k, а указанная граница exact claim.

Пусть в идеальной схеме `O_i` — A16 selected-source target для десяти disjoint source groups, при фиксированном SITE; `s_i(mask)∈{−1,+1}` — sign bits. Для совместного READY и REPORT1 полный target effect равен

```
E_sigma = Q_pre · Σ_mask β_sigma(mask) · Π_i (I+s_i(mask) O_i)/2.
```

`O_i` действуют на disjoint physical copies и коммутируют; общий SITE входит как один диагональный control. Равенство — операторное и применимо к произвольному, в том числе коррелированному, входу. [REPORT_EFFECT_CHECK.json](REPORT_EFFECT_CHECK.json) самостоятельно восстанавливает в точной `Q(p)` арифметике все 2 048 palette weights, 27 исходных polynomial coefficients на каждое sigma и шесть скалярных product cases.

Чтобы отождествить этот effect с **исходным скаляром** `β_sigma(f_x,q_x)`, достаточно условной по SITE/SAM product-подготовки: должны факторизоваться как source-моменты внутри каждого tensor-DAG, так и десять source groups, причём их моменты должны совпасть с нужными `f_x,q_x`. Одной раздельной адресации и равенства одномерных marginals недостаточно; отдельные коррелированные состояния могут совпасть случайно, но общей гарантии нет. Точный hostile пример с одинаковыми одномерными marginals `S1,S2` и корреляцией `S1=S2` меняет ожидаемое значение на ненулевой исходный коэффициент при `f²`.

После измерения/усреднения одного общего SITE с весами `w_x` скалярная формула имеет вид `Σ_x w_x β_sigma(f_x,q_x)`. Она в общем не равна `β_sigma(Σ_x w_x f_x, Σ_x w_x q_x)`: даже при условно независимых копиях общий SITE порождает корреляцию после усреднения. Это согласуется с B24 и не является новым правилом физического источника.

## 4. Счёт, replay и Spin correction

[INDEPENDENT_RESOURCES_CHECK.json](INDEPENDENT_RESOURCES_CHECK.json) независимо пересчитывает все шесть forward native inventories: A13/A15, A16, B31 banks ровно по одному, RAW-to-zero, READY с paid literal inverses и REPORT extraction. Совпадает также literal raw reverse inventory. Для семи report число известных approximate X/H/CCX macro occurrences равно **162 754 649 904**, условная all-column сумма `<2^-4058`. Это не включает отсутствующие source/SITE loaders, births, comparator, marks, clock или ошибки иных физических операций.

[A17_ISOLATED_REPLAY.json](A17_ISOLATED_REPLAY.json) повторяет builder и актуальный checker `check_report_assembly.py` SHA `7d27bb63a9b9cdaed4ef57b876bef96ad0276f3c0d748653cfa7da217460aa08` в отдельном временном дереве. План побайтно совпал; compilation и check совпали после нормализации путей к клону, поскольку original compilation хранит абсолютные input paths. Оригинальные файлы не менялись.

Во время review обнаружено, что старые **диагностические** A14 `check_native_boolean.py` и B31 `check_small_native_router.py` использовали на Spin сопряжённую модель `diag(J,J)`, тогда как `native_execution.py` задаёт `diag(J,−J)`. Actual native grammar не менялась. Модели точно сопряжены единой `W=diag(1,1,1,−1)` на Spin; G и CX действуют на остальных проводах и коммутируют с W, поэтому прежние утверждения о target `ordinary⊗I_Spin` сохраняются. Тем не менее буквальное соответствие диагностического интерпретатора требовало исправления. A17 checker исправлен владельцем. Независимый [A14_TRUE_SPIN_REPLAY.json](A14_TRUE_SPIN_REPLAY.json) повторяет все 1 536 small-k exact columns и 96 inverse cases с настоящей `diag(J,−J)`; результат совпадает с исходным certificate. [B31_TRUE_SPIN_CHECK.json](B31_TRUE_SPIN_CHECK.json) повторяет 32 small-router columns, численный max L2 `<2.7e−15`. Это не запуск полного cap28 native bank.

Полная исходная `alpha_h` остаётся отдельной: ideal один-component `Q_pre≈0.740683`, а семь независимых таких checkpoints совместно дают `Q_pre^7≈0.122300`; ни одно из этих чисел само по себе не доказывает полную physical alpha. Сохраняются B29 условия actual scalar T6 и полное нормирование/ошибки. `GR_closed=false`.
