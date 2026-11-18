# B27. Управляемая подписанная инволюция для реальных Choi/CAR адресов

**Результат:** для любой заранее заданной пары разных известных базисных адресов `a,b` построен конечный gate list в логическом базисе `X,CX,CCX,Z,CZ`. На всех базисных входах данных и произвольных `h,delta`, при нулевых рабочих битах, он точно реализует

```
|h>|delta>|x>|0_work> -> (−1)^[h delta · 1_{x∉{a,b}}]
                         |h>|delta>|x xor (h·1_{x∈{a,b}}·(a xor b))>|0_work>.
```

Следовательно `h=0` даёт identity, а `h=1` управляет именно A12 `V_+=T_ab` при `delta=0` или `V_−=−Z_a Z_b T_ab` при `delta=1`, включая весь complement. Линейность распространяет равенство на произвольные комплексные суперпозиции и entangled `h,delta,data,RIGHT,oldRIGHT`; последние два фактора схема не адресует. Этот результат относится к **чистому scratch checkpoint**. Gate list — обратимая перестановка с фазой на всём увеличенном пространстве, но указанное действие не утверждается для произвольного грязного scratch.

Исходные A11/B25 листья дали `20 480` различных Choi-пар и `512` различных CAR-пар, покрывающих все **72 192** source-leaf occurrences. Списки для конкретных пар уже исполнимы логическим interpreter, но динамический lookup по внешнему SITE и реализация всех логических primitives в H.1 native-профиле ещё не выданы. `GR_closed=false`.

## 1. Алгоритм и почему очистка работает

`n>=3`, `d=a xor b`, выбирается любой set bit `k` в `d` (код берёт младший). Для каждого отличающегося `j!=k` выполняем `CX(k,j)`, остальные data биты не меняем. Тогда на обоих selected addresses получаются одинаковые значения всех `n−1` бит кроме `k`:

```
y_j = x_j xor x_k,  если d_j=1 и j!=k;
y_j = x_j,          если d_j=0.
```

Это обратимое преобразование. Совпадение указанных `n−1` бит с шаблоном даёт ровно две возможности для свободного pivot — именно `a,b`. Нормируем требуемые нули `X`, вычисляем многоуправляемое И цепочкой `CCX` в один clean `m`, очищаем промежуточную цепочку и обращаем нормировку/`CX`. Получаем `m=1_{x∈{a,b}}`, не изменив `x`.

Далее на отдельном clean `q` выполняется

```
CCX(h,delta,q); Z(q); CZ(q,m); CCX(h,delta,q),
CCX(h,m,j) для каждого j с d_j=1.
```

Фаза равна `−1` ровно при `h=delta=1,m=0`. При `h=m=1` условное XOR `d` переставляет `a,b`; иначе data не трогается. Главное: **одно** свойство `x∈{a,b}` сохраняется при этой перестановке. Поэтому повторное применение той же обратимой membership-схемы корректно зануляет `m`, все chain bits и `q`, не меняя `h,delta`.

Hostile fixture из [LOGICAL_CHECK.json](LOGICAL_CHECK.json): если вместо этого запомнить отдельно `eq_a,eq_b`, при `x=a,h=1` переставить на `b` и попытаться очистить прежние флаги теми же equality checks, результат — грязные `(1,1)`. Нельзя подменить наш invariant-flag uncompute этим ошибочным приёмом.

Каждый используемый логический primitive сам себе обратен. Обращение **всего** gate list в обратном порядке является точным inverse на каждой колонке увеличенного пространства, включая произвольный dirty scratch. [check_controlled_involution.py](check_controlled_involution.py) дополнительно проверяет 256 таких произвольных колонок; это отдельное утверждение от clean-scratch target identity.

## 2. Реальная адресация, точные counts и retained факторы

Регистр Choi имеет `n=22`, little-endian logical integer `(address<<10)|(input<<5)|output`: `a=0`, `b=(address,input,output)` из A11. Address занимает 12 бит, input/output по 5; активные `a<2049` и все 2047 padded address blocks остаются частью полного data space. Для CAR `n=12`, integer `(internal_site<<4)|grade`; `a=(site,1)`, `b=(site,0)` или `(site,15)`. Эти восемь site-битов принадлежат **внутреннему** CAR input, а не общему внешнему PF SITE; RIGHT128 и старый RIGHT не входят в адресуемые провода.

Для фиксированной пары обозначим `D=popcount(a xor b)` и `Zc` — число нулей в описанном `n−1`-битном transformed template. При `n>=3` gate inventory точно

```
X    =4 Zc,             CX  =4(D−1),
CCX  =4n−8+D,           Z   =1,        CZ=1,
total=4Zc+5D+4n−10,     clean scratch=n−1.
```

Дополнительно есть `n` data bits и два сохранённых control bits (`h,delta`), всего `2n+1` адресуемых logical wires. Для фактических CAR пар получается `55..93` logical gates и 11 clean scratch; для Choi — `172..227` и 21 clean scratch. Это counts **одного фиксированного logical controlled-V word**, без загрузки labels, births, физического Hadamard test, компиляции или clock. Все реальные пары и их точные counts выписаны в [ACTUAL_PAIR_INVENTORY.jsonl](ACTUAL_PAIR_INVENTORY.jsonl); один буквальный полный word каждой категории — [CHOI_EXAMPLE_GATE_LIST.json](CHOI_EXAMPLE_GATE_LIST.json) и [CAR_EXAMPLE_GATE_LIST.json](CAR_EXAMPLE_GATE_LIST.json).

[emit_pair.py](emit_pair.py) выдаёт конкретный gate list на стандартный вывод:

```
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round27/emit_pair.py choi 1 0 1
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round27/emit_pair.py car 255 15
```

Здесь перечисление адресов и график выбранной пары построены для заранее **известных** `a,b`. Когерентный `SITE -> адрес` lookup, selection по `node/copy/leaf`, общий controller A12/A13 и его uncompute требуют собственного действительного слова. Размерности и индексы логического генератора не являются автоматически native wire-map; при передаче в имеющийся native interpreter нужно явно учесть, что он нумерует старший бит первым.

## 3. Независимые проверки

Отдельный [independent_interpreter.py](independent_interpreter.py), не использующий реализацию interpreter внутри генератора, проверил:

* все input columns для 160 пар малых `n=2..6`: **9 824** случая с обоими `h,delta`;
* у всех **20 992** реальных bound pairs оба выбранных адреса и complement, оба значения `h,delta` и два дополнительных spectator-bit settings: **503 808** колонок;
* ещё 84 22-битных случая на границе активного/padded space, максимальном адресе и рядом с выбранным `b`;
* комплексную суперпозицию 28 компонент, включая разные `h,delta` и spectator, с проверкой относительных фаз; 256 произвольных dirty-scratch колонок на точный обратный gate word.

Для остальных 22-битных колонок гарантия следует из обратимого преобразования шаблона и membership-предиката в §1, а не из утверждения, будто мы перебрали `2^22` входов для каждой пары. Проверка и gate-list hashes указаны в [RECEIPT.json](RECEIPT.json).

## 4. Что действительно уже принадлежит native профилю

В исходном `G_CX_SOURCE_I` один объявленный обычный `port` и два Spin-провода заданы физически; Spin имеет dimension 4 и quaternion basis `(1,i,j,k)`. Точная owner convention:

```
p=(sqrt(5)−1)/2,  G=[[sqrt(p),−p],[p,sqrt(p)]],
L_i=[[0,−1,0,0],[1,0,0,0],[0,0,0,−1],[0,0,1,0]],
SourceI=diag(I4,L_i),  L_i²=−I4.
```

Требуется действительная доступность этого **одного** source port и разрешённых CX между ним и `q`; мы не предполагаем индивидуального адресования Spin. Порт или `q` не должны быть запрещённым oldRIGHT. Поэтому **на всех** port/Spin колонках

```
SourceI; SourceI = Z_port tensor I_Spin.
```

Для произвольного обычного `q` выполняем `SWAP(q,port); SourceI²; SWAP(q,port)`, где каждый SWAP — `CX(q,port);CX(port,q);CX(q,port)`. Получаем точный `Z_q`, сохраняющий произвольные port и Spin, с `6 CX + 2 SourceI = 8` физическими вызовами; если `q` уже port — 2 SourceI. [check_native_Z.py](check_native_Z.py) построил настоящий исходный `Execution`, проверил домен и сравнил все 16 колонок с `Z_q tensor I` в точном алгебраическом поле. Правило применимо при действительном разрешении маршрута через один объявленный port и при неприкосновенности oldRIGHT; оно не разрешает трогать защищённый Spin по отдельности.

Там же проверено исходное точное `G^-1=Z G Z`: непосредственно на port — `1 G + 4 SourceI = 5` вызовов; на другом обычном `q` с теми же двумя SWAP — `6 CX + 1 G + 4 SourceI = 11`. На реально свежем RAW-проводе `q` в `v=(sqrt(p),p)` это даёт `|0>` и может подготовить отдельный clean scratch при соблюдении реального RAW birth/адресов и с оплатой рождения и всех 11 этапов. Полное точное равенство маршрутизированного word равно `G_q^−1 ⊗ I_port ⊗ I_Spin`: после SWAP-return произвольные неизвестные port и Spin не изменены, даже если они изначально были коррелированы с другими входами. Если конкретный граф требует вернуть очищенный `q=0` в исходный birth-state `v`, это отдельный оплаченный `G(q)` и реальное продолжение, а не невидимый reset. При последовательной подготовке всех scratch через отдельный общий доступный port это даёт `21·11=231` вызовов плюс 21 RAW birth для Choi и `11·11=121` вызовов плюс 11 RAW births для CAR; эти условные числа не включают сам logical word или финальное восстановление. Проверка сделана на полном пространстве port/Spin, не только на одном Spin input.

Логические `CX` уже входят в грамматику профиля. Для оставшихся `X`, `CCX`, `CZ`, multi-control/lookup, общего условного направления и требуемого Hadamard test **реальный оплаченный native word здесь не выпущен**. Например, `X(q)` через `CX(one,q)` верен на секторе гарантированного чистого `one=1`, но такое знание должно обеспечиваться реальным сохранённым resource/READY; оно не считается бесплатным рождением. Наличие более общего theorem о плотности или measurement/feedforward H/Toffoli не равно здесь выполненной all-column H.1 компиляции и не задаёт маркированные транспорты.

## 5. Воспроизведение и границы

```
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round27/build_leaf_inventory.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round27/check_controlled_involution.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round27/check_native_Z.py
```

Требуются также интеграция с A13 selector/retained first-success, подготовка условно необходимых flags/one, native controller и coherent H-test, реальные prefixes, разрешённые readers/seal и полный gate/clock/READY учёт. `C`, физическая Cost−Info и ОТО этим локальным результатом не закрыты.
