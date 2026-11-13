# A10: конструктивное восстановление noisy NPS через приватную дилатацию

Продолжение A9/B19–B20 на исходных основаниях D0. Новый шаг снимает необходимость общего WORK-only восстановления всего большого банка: используется **настоящий полный NPS square word**, его оплаченный inverse и исходный exact-native fixed-point алгоритм. Это применимо также к реально Spin-зависимому backward word. Произвольное восстановление Spin новым primitive не добавлено.

Для конечной локальной NPS-программы получен явный native DAG с интервальной оценкой ошибки, исходным fine-архивом и положительным **конечным** источником возврата. Это не геометрический H.1 writer. Его выгрузкой занимается B21; физические Cost−Info и GR остаются открытыми. `GR_closed=false`.

## 1. От исходной noisy-ветви к правильному входу восстановления

Пусть `A_N` — square gate list настоящего NPS/E0 плюс точное 36-call echo, со всеми исходными независимыми forward/back словами. Рождения не входят в инвертируемый gate list: их canonical embedding — `i`. Они должны уже существовать на живой арене. При настоящих исходных условиях NPS:

```
A_N i = |0>_(r') |0>_(t') K0 + |1>_(r') |0>_(t') K1,
K_b* K_b=q_b I,   q_0=1-q, q_1=q,   p²<=q<=1/2.
```

Равенство на полном Spin4 input, с любым внешним reference. `A_f,A_b` независимы. В частности, `K0=u A_b* Z A_f i+d A_b* A_f i`, `K1=u A_b* Z A_f i-d A_b* A_f i`; они не обязаны быть `w_b tensor I_Spin`.

В исходном уже исполненном NPS используем **внешние** `r,t` и после echo имеем `t=0`. Их не обращаем. Родить два приватных провода `r',t'` в настоящем `v`, выполнить по одному исходному routed inverse G на каждом и затем `CX(r,r')`. Это 2 births + 23 calls = **25 стадий**. На внешней ветви b состояние processor теперь именно

```
V_b=|b>_(r') |0>_(t') K_b/sqrt(q_b).
```

Это coherent basis copy указателя, не клонирование неизвестного Spin. Все корреляции с внешним r и reference остаются. B20 независимо проверил данный начальный участок. Здесь используется 11-call исходный `native.inverse_word` на off-port G; прежнее уже исполненное B17 echo с его 17-call inverses и 36 calls не сокращается.

Восстановление ниже адресует только живой current bank, приватные `r',t'`, исходный source-port/Spin и новые phase helpers. Внешний `r` — только контроль, внешний `t` до последней bright-correction не адресуется. Поэтому все три прежних coarse projectors, в том числе invalid `|11>`, сохраняются на **всех** колонках. Это не проверка лишь одной вероятности.

## 2. Почему общий fixed-point алгоритм применим именно к noisy NPS

Владелец NR был записан для sharp `A_b* Pi_b A_f`. Его старую отмену backward leg и старые masses здесь не копируем. Вместо этого oracle есть **весь** `A_N`, с новым приватным pointer/tail. Пусть `P0=i i*` фиксирует только canonical processor WORK, а `Pi_equal` проверяет `r'=r`. Он есть сумма двух disjoint patterns `00,11`. На внешней ветви b:

```
P0 A_N* Pi_equal A_N P0=q_b P0,
P0 A_N* V_b=sqrt(q_b)i.
```

Это ровно общая all-input предпосылка исходного A1–A7/NR2. Она следует из полного noisy-effect operator и не требует projective Kraus или real-`I_Spin` центра.

Родить phase rebit h, который `A_N` не трогает. Выбрать исходный native phase `t_phase=c+i s`, `s>0`, `1/2<c<17/32`, common для `P0` и `Pi_equal`. Это не фазовый primitive: выполняются исходные Walsh G/CX/SourceI words. Для `P0` настоящая born frame сначала оплаченно переводится в zero frame, затем выполняется фазовый word, затем frame восстанавливается. Не тестируются ни Spin, ни oldRIGHT, ни внешний r, ни h.

В matrix order:

```
A_0=A_N,
A_(n+1)=A_n R_P0 A_n* R_equal A_n,
execute A_n* as recovery.
```

В хронологическом списке — `A_n;R_equal;native_inverse(A_n);R_P0;A_n`. Каждый inverse разворачивается исходным компилятором; вложенные inverses не сокращаются бесплатно. Внешний r в actual raw list остаётся control-only.

Для каждого b отдельно, при `a0=2(1-c)`, `b0=2c-1`,

```
epsilon_0=1-q_b,    z_0=sqrt(q_b),
epsilon_(n+1)=epsilon_n (b0+a0 epsilon_n)^2,
z_(n+1)=z_n t_phase (t_phase+a0 epsilon_n),
P0 A_n* V_b=conjugate(z_n(q_b)) i,
||(I-P0) A_n* V_b||=sqrt(epsilon_n(q_b)).
```

Результат uniform на всех неизвестных input/reference колонках и на **всём** phase-rebit пространстве. В real implementation complex coefficient означает его реальную двумерную матрицу на h; состояния `|+i>` не готовятся. Неуспешные компоненты сохраняются физически. Одинаковый phase не означает одинаковый `q_0,q_1`: обе ветви вычисляются отдельно.

## 3. Снято ограничение WORK-only recovery, проверен Spin-зависимый случай

B19 правильно требовал `K_b=w_b tensor I_Spin` для старого real WORK-only SO compiler. Здесь эту предпосылку заменяет уже имеющийся **реальный доступ к A_N и его inverse** в профиле `G_CX_SOURCE_I`. Если `A_N` взаимодействует со Spin, его разрешённые операции воспроизводятся, но отдельные opaque Spin bits не адресуются.

`check_private_recovery.py --spin-coupled` использует настоящий независимый backward centre `A_b=SourceI A_f`, `A_f=G_port^3`. Его две ветви имеют линейно независимые WORK-коэффициенты при `I` и `L_i`. WORK-only преобразование не может привести их к `w tensor I`: соответствующий Gram determinant строго положителен. При этом новый алгоритм на всех 4 Spin × 2 phase × 2 exterior-record входах действительно даёт ровно требуемый `conjugate(z_n) I` на born processor cut с сохранённым полным failure complement.

Для rounds 0,1,2 реально выполнены все raw gates. Максимальный проверенный Spin-coupled word содержит **131 550 вызовов**; в real-centre варианте — **131 325**. Остаток численного сравнения полного input corner в обоих случаях меньше `9e-13`. Это replay конечных gate lists; точное общее равенство обеспечивает предыдущий all-input вывод. Проверочная scalar branch не подменяет геометрический H.1.

## 4. Настоящие фазовые поправки и целевой fine-хвост

После `A_n*` требуется отменить good phase. На центральных реальных `q_b` вычислить `arg z_n(q_b)` из настоящего recurrence. Две conditional corrections действуют на h и двух дополнительных **рождённых и сохраняемых** helpers. Перед fine-архивом bright-only tail correction переводит внешний `t=0` в

```
w_J=(1,p²)/sqrt(1+p^4),    u_J=p^4/(1+p^4),
```

и тождественна на `r=1`. Всего приватных births пять: `r',t',h,helper,helper`. Их целевое состояние в bank recovery — прежний canonical product; их born masses равны1, а не удалены из cut.

`supported_private_plane.py` строит только исходные positive G/CX/SourceI sequences. На трёх helper/target bits с внешним r-контролем parity-Walsh сумма даёт ровно `32 theta_G` на одной заданной паре basis states и ноль на остальных. Selector r может быть0 или1. Каждая последовательность сохраняет r, source и все Spin-колонки точно на endpoint. Четыре существенно разные signed-plane recipes независимо воспроизведены **точно в Q(sqrt(p)) на всех128 колонках**, включая dirty source и Spin.

Сохранение support у готовой bright-correction относится к endpoint полного макроса. Его промежуточные raw gates могут временно вывести хвост из прежнего кода; обязательный reader или измерение внутри такого макроса здесь не постулируется. Если фактический task требует такую внутреннюю отметку, её допустимый transport остаётся отдельной обязанностью.

Исходный target-specific SO(3) compiler возвращает явный конечный signed DAG. Каждый single-bit rotation на трёхбитной арене есть четыре disjoint plane rotations; каждой соответствует свой embedded SO(3) word. Никакая произвольная rotation не объявлена primitive. `CORRECTION_WORDS.json` содержит найденные последовательности, а `PRIVATE_RECOVERY_DAG.json` — их физические bindings и raw recipes.

Две inverse semantics различены явно: в amplifier `raw_inverse` применяется к полной уже определённой raw последовательности, без отмены nested inverses. В отдельном SO(3) DAG сначала разворачиваются signed letters; group-inverse переворачивает их порядок и знаки, после чего каждый знак получает собственный заново заданный native plane recipe с собственной полной стоимостью. Это не сокращение ранее выполненной истории. Integer Walsh-проверка охватывает все ordered planes, оба значения selector и все basis columns.

Численный поиск не является сертификатом. `certify_private_corrections.py` независимо вычисляет каждый узел DAG из исходной Golden G через **320-bit outward integer intervals**, включая сами цели из `q=p²+16p^12` и exact stable phase `G^624`. Напечатанные quaternion/angle/error из поиска не используются. Измеряется полная 8-column ошибка каждой физической correction, не только overlap с подготовленным состоянием.

## 5. Явный конечный пример с полной стоимостью

Это локальный подлинный NPS с `A_f=A_b=G_port^3`, `q=p²+16p^12≈0.4316559314923749`; его square NPS/E0/echo содержит60 calls. Для12 recovery rounds:

```
native A_12 inverse:              950 276 648 206 calls,
all phase/bright corrections:      1 001 574 016 calls,
private preparation:                          23 calls,
complete fixture + all births
and literal six-copy archive:    951 278 222 451 stages.
```

Огромное слово **не выполнялось целиком**. Оно задано конечным DAG, исходными literal leaves и проверенной raw-inverse semantics; его стоимость получена точной integer recurrence. Нижние rounds0–2 выполнены напрямую и совпали с ней. Физическая последовательность не выдаётся за практически дешёвую.

Сертификат даёт all-input state-map ошибку `<=8.65351877654e-23` до правильного идеального восстановленного архива. Произведение **полной** длины и этой bound меньше `8.232e-11`. Все 5 приватных и6 архивных births присутствуют в исходном cut; полный clock fixture имеет

```
D=974108908297084,
d_final=65536,
L=132,
full heat modes=425D.
```

При подсчёте используется staged birth order, не финальная ширина во всех старых стадиях. Нельзя пересчитать эти числа на весь H.1 по одному совпадению q.

У actual finite words сертификат отдельно фиксирует corrections и вычисляет **их собственный** cold как функцию q. Для `|q-q_center|<=2^-30`:

```
0.15435474140822 <= c_actual(q) <= 0.15435475849454,
-0.06117193613814 <= d c_actual/dq <= -0.06117186939040.
```

Здесь десятичные границы расширены наружу; точные целочисленные endpoints и denominator `2^320` сохранены в сертификате. Поэтому для любого исходного `0<z<1` настоящий конечный J q-source

```
-2 r z c_actual c_actual' / (1-z+z c_actual²) >0.
```

Не использован ideal limiting gain; физическое z и geometric `g` не выбирались. Эта exact q-only compression относится к **generated-copy** chart, в котором recovery действительно использует копии указанного NPS word. Самостоятельно варьируемые новые occurrence rows не отождествляются с этими копиями: для них остаётся полный near-optimum residual и настоящие `N epsilon`, norm/basis/right-lift bounds. Для native finite comparisons нужны реальные q±/step; производная дискретного индекса native word не вводится.

## 6. Ресурсная сходимость и граница применения

С исходным raw inverse compile для counts `(G,CX,SI,G_off)`:

```
G_next=3G+P_G,
CX_next=3CX+6G_off+P_CX,
SI_next=5SI+4G+P_SI,
G_off,next=2G_off+P_off.
```

Каждый новый current word конечен и использует те же заранее рождённые ресурсы. На `q_b>=p²` есть uniform finite warmup; далее исходные NR6–8 дают `sqrt(epsilon)<=C_h 12^-k`, а raw length `<=C_h5^k`. Small-arena phase/tail errors выбираются `<=12^-k` через прежний supported compact-group compiler с polylog length. Следовательно полный `N_k epsilon_k→0`. Его константы, M, фактический physical gain и остальные source terms не удаляются. Настоящие CX-pairs после последнего рождения дают прежний full-clock factorial контроль с пересчитанными ages и всеми modes.

Новый метод снимает конкретную прежнюю предпосылку — WORK-only восстановление произвольного большого Spin-зависимого банка. Он не снимает доступность square replay на **живых** адресах, actual source-port, полный текущий task, все marks и reader transport. B20 показал: для заданного live reader перенос через inverse/suffix существует и оплачивается; sealed address нельзя использовать таким образом. Список реальных обязательных readers должен быть состыкован с concrete H.1 word до physical application.

Полный geometric H.1 source, joint stationary system и исходное Book03/Cost−Info aggregation binding не получаются из локального fixture. Никакая новая Info или выбранный ради совпадения коэффициент не вводились. Работа B21 должна предоставить настоящий geometric operand, к которому применим этот конструктор; если его допуск не подтверждён, пример не заменяет требуемый вывод ОТО.

## Независимая проверка

[B22](../../open/round22/INDEPENDENT_REVIEW_A10_RU.md) повторил оба конечных replay и интервальный сертификатор из отдельной копии: 23, 25 и 12568 проверок соответственно. DAG и сертификат совпали побайтово. После review добавлено только явное уточнение выше об endpoint bright-макроса; математические формулы и проверенные программы не менялись. Отдельный root-check данных B21 закреплён в `ROOT_CHECK_B21.json`; он проверяет экспортированные компоненты, не весь H.1.
