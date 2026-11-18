# B25. Полные цели подготовки семи исходных банков на периодическом L=4

**Результат:** задана вычислимая параметризованная family семи оригинальных полных Choi/CAR preparation targets `Z_j(Y_b)` на `A=2049`, `S=256` и исходном Fourier128. [targets.py](targets.py) вычисляет все их локальные блоки, один произвольный элемент всей колонки `O_b`, полный site-controlled CAR map и внешний SITE loader. [precision_name.py](precision_name.py) задаёт тот же рецепт через произвольную рабочую точность и умеет потоково перечислить **всю** `2^22`-колонку `O_b`, включая padding. Это матрицы-цели и численные вычисления, не оплаченное native Golden слово.

Центр всех семи банков и условного дополнительного несоставного current-bank материализован как **16 392 полных `32×32` Julia-блока** в [CENTRE_JULIA32_TARGETS.npz](CENTRE_JULIA32_TARGETS.npz), а соответствующие поля — в [CENTRE_FIELDS.npz](CENTRE_FIELDS.npz). Кроме `Y0`, проверены четыре реальные SAM-метки: все нули, все единицы, чередующаяся и one-hot. Центральный `Y0` не является меткой `b=0`: последняя задаёт `Y0−s p²` по каждой chart-координате. Имена и все 2 688 бит каждой метки однозначно записаны в [SAM_SAMPLE_LABELS.json](SAM_SAMPLE_LABELS.json).

Полный physical H.1 gate word, sign/READY factory, физические mark-stage addresses, seal и `alpha_h` ещё не выданы; вычисления ниже не являются доказательством C¹-uniform native compiler, физического `C` или GR. `GR_closed=false`.

## 1. Поля и семь банков

Общий объект: `p=(sqrt(5)−1)/2`, `h=1/4`, `nu=3/5`, точные исходные F/R counts `N_x`, `rho_x=256 N_x/10946`, `w_x=N_x/10946`; `Lambda_h=2^1525` и `epsilon_h=2^-1531` из A11. Внешний общий PF SITE имеет амплитуды `sqrt(w_x)`. При этом каждая внутренняя CAR-копия имеет собственные **равномерный** 256-site, все 16 grades и свежий RIGHT128. Неизвестный старый `D/oldRIGHT` — отдельный точный identity factor.

Свободные координаты — 16 **raw** inverse-coframe entries `u`, 24 proper-link coordinates и 2 matter values на каждом из 64 sites `x2,x3∈{1,2}`; общий `m=2688`. Выбирается `s=2^-30`, `theta_k=s(b_k−p²)`. Для текущего банка

```
u_x(b) = u_x(0) + Delta_u_x(b),
U_x,r(b) = exp(sum_{a<c} theta_x,r,ac eta_null^(-1)(E_ac−E_ca)) U_x,r(0),
Psi_x,A(b) = Psi_x,A(0) + Delta_Psi_x,A(b),  A=0,15.
```

Все остальные site values и PF фиксированы. Точное определение центра, используемое в [precision_name.py](precision_name.py), принадлежит B21/B24: `sigma=1/100`, `A_W=3/100`, исходный `k0` из `p,z=2^-20`, `H(x2h,x3h)=k0 (2π)² sigma²(x²+y²)+A_W(x²−y²)` и исходные forward/backward `K2,K3`. Столбцы `u0=nu eta_null e^(-T)` и `U0=exp(−K2 N2−K3 N3)` включают проверенный постоянный gauge `R=diag(1,1,−1,−1)`. Исходное matter-поле `Psi=sigma·π/(2sqrt2)·(cos(πx0/2),sin(πx0/2))`. Исходные π, p, корни и показательные вычисляются как вычислимые действительные числа, не через округлённые B21 таблицы. `targets.py` — независимый быстрый float evaluator тех же формул.

Для reference определены `s_ref=6`, `chi_h=1`, исходные `F_h=16517734400/162621047169`, `d_h=F_h/(36 k0)` и `a_h=h·6 sqrt(d_h)/2`. Для надёжного соответствия null-frame фиксирован собственный `T` из B24: `T eta_cart T^T=eta_null`, `det T=1`; используется `u_ref=nu sqrt(rho)/6 T eta_cart`, а boost/rotation F2 применяются после сопряжения `T`. Это принципиально: буквальное `e_ref∝I` в null-frame не даёт исходные временной/пространственный signs.

| Вызов | Данные `(u,U,Psi,rho)` |
|---|---|
| `y+` | `(u_ref,I, a_h(−1)^x1 · grade0,rho)` |
| `y−` | `(u_ref,I, a_h(−1)^x0 · grade0,rho)` |
| `f` | `(u_b,U_b,0,rho)` |
| `0` | `(u_ref,I,0,rho)` |
| `x+` | `(u_ref,(T A T^T,T B T^T,I,I),0,rho)` |
| `x−` | `(u_ref,(T A T^T,T B^−1 T^T,I,I),0,rho)` |
| `q` | `(u_b,I,Psi_b,rho)` |

`A` — исходный boost 02 с `t=h/2=1/8`, `B` — rotation 12 с `v=h/20=1/80`. Все site shifts в полях/reader являются periodic `mod 4`. Под `current_mark` отдельно поддерживается `(u_b,U_b,Psi_b,rho)` для оригинального несоставного current mark, если он требуется: это **не восьмой вызов** компаратора, и число его рабочих copies не угадывается.

## 2. Full-column Choi, CAR и SITE

[Каталог A=2049](../round24/TORUS_CHOI_ADDRESSES.jsonl) фиксирует identity anchor `a=0`, 1024 raw-coframe и 1024 proper-link адреса. На каждом адресе

```
J_a = [[ C, sqrt(I−CC*) ], [ sqrt(I−C*C), −C* ]],
C_coframe = sum_i u_i c_i^dagger,
C_link    = Lambda(U)/2.
```

CAR порядок `(0,2,3,1)` и все степени exterior сохранены. Для вещественного coframe точная CAR identity даёт корни без спектрального выбора: `sqrt(I−CC*)=I−CC*/(1+sqrt(1−||u||²))`, аналогично справа. Для link используется положительный матричный корень; strict defect из §4 обеспечивает его существование.

Полный вектор и все колонки его SO-продолжения (879) заданы как

```
b[a,i,j] = J_a[j,i]/sqrt(32·2049)     для a<2049, иначе 0,
r=(0,0,0), c=1/sqrt(65568), K=|b><r|−|r><b|,
O_b=I+K+K²/(1+c).
```

Активных координат `2049·32²=2 098 176`, полный native register имеет `2^22=4 194 304` входных и выходных колонок; padding нормировку не меняет и фиксируется на каждом комплементарном базисном векторе. `precision_name.O_entry(...)` вычисляет произвольный элемент, `precision_name.choi_column(...)` лениво отдаёт всю колонку, не строя `2^22 × 2^22` матрицу. Выбор `nonzero_only=False` включает явные нули; ускоряющая проверка нуля в mpmath численная, а не algebraic zero-test. При RAW births все 22 Choi-wire имеют состояние `v`, поэтому фактическая **целевая** full-column рамка макроса — `O_b (G^⊗22)^T`, а не просто `O_b`. `targets.raw_choi_column` вычисляет любую такую колонку в пространстве `2^22`, храня только конечные векторы. [check_raw_frame.py](check_raw_frame.py) проверил нетривиальную колонку и превращение `v` в `|0>`; ошибка нормы `<1.3e−14`. Следует различать: `O_b` фиксирует padding, но предварительное `(G^⊗22)^T` вообще смешивает его, поэтому полная RAW-колонка не обязана быть identity на padding. Это target рамка, не список native gates. Неизвестные состояния не клонируются: каждая требуемая копия должна быть заново подготовлена на настоящих RAW births.

Материальный target на каждом внутреннем site:

```
m_x=sqrt(p)|1>+Psi_x,0|0>+sqrt(1−p−||Psi_x||²)|14>+Psi_x,15|15>,
m_*=sqrt(p)|1>+p|14>,
M=sum_x |x><x| tensor [O_mx O_m*^T] tensor I_RIGHT.
```

`precision_name.car_column` отдаёт все 16 выходных grades любой колонки при неизменном внутреннем site и RIGHT, а полный оператор дополнительно действует как `I_oldRIGHT`. Исходная вакуумная подготовка и Fourier128 prefix должны выполняться и оплачиваться отдельно; map `M` не переустанавливает неизвестный RIGHT. `chi_ref(x,r)` из `targets.py` точно задаёт исходную разрешённую 64-парную Fourier128 секцию, а target-амплитуда `m_x[grade] chi_ref(x,r)` сохраняет неиспользованные grades и внутренние site/RIGHT корреляции.

Внешний SITE target — `O_chi (G^⊗8)^T` на всех 256 колонках, где `chi_x=sqrt(N_x/10946)`, `G=[[sqrt(p),−p],[p,sqrt(p)]]`. Вход — действительные восемь рождённых `v=(sqrt(p),p)` wires, не подставной чистый `|0>`; отдельный обратный SITE macro обязателен. `precision_name.site_entry` вычисляет произвольный его элемент. Точный integer Fourier-контроль даёт `F^T F=128I` и RIGHT Gram `I/128`; повторный hostile-test фиксирует, что домножение внутреннего Fourier-site на PF веса ломает этот Gram.

## 3. Адреса источников, марки и checkpoint

[MARK_OUTPUT_CATALOG.json](MARK_OUTPUT_CATALOG.json) и локальная неизменённая копия A11 [SOURCE_LEAF_BINDING.json](SOURCE_LEAF_BINDING.json) содержат настоящий конечный mapping: `282` source leaves на каждом из 256 внешних sites (272 Choi matrix-entry moments, 10 CAR moments), `72 192` адреса на одну source-схему и `505 344` соответствия на семь вызовов. Для каждого leaf сохранены конкретные `(site,base/shift,direction,input,output,anchor multiplier)` и настоящие периодические адреса A11. Один такой mapping не подразумевает клонирование экземпляра.

[mark_catalogue.py](mark_catalogue.py) вычисляет конкретный именованный элемент по `(bank, SITE index, leaf index)` и при необходимости потоково перечисляет все 505 344 адреса, не создавая физические stage ordinals.

[COPY_SLOTS.jsonl](COPY_SLOTS.jsonl) содержит разные **верхние пределы слотов** `7×(180 Choi+16 CAR)` с отдельными `S1,S2,T1..T8` для исходного degree-82/degree-(2,2) процессора. Паддинг monomial degree сохраняется; это не утверждение, что уже существуют все физические births и примитивные gates.

Зафиксирован целевой логический порядок: реальные RAW births и vacuum/Fourier prefix → подготовка одного внешнего SITE → по каждому `b` регенерация настоящих source copies → исходные sign/selector/READY/report resources с сохранением всех failure branches → оригинальный семивызовный компаратор и pre-sign mark → оплаченные обратные макросы и все требуемые transports до seal. SAM — designated incoming control; shared SITE не является ни SAM, ни внутренним CAR site, ни неизвестным старым RIGHT. Таблица описывает **доступные source operands и output roles**, а не выданные physical stage ordinals. Собственный список реальных `O_t`, канонический полновременной birth/mark order, gate addresses и reader/seal transport ещё требуют исходного native writer; эти отсутствующие объекты не подменены generic labels.

## 4. Проверки и строгая область

[check_targets.py](check_targets.py) на каждом из 5 labels проверяет все 8×2049 Julia targets и полные 16×16 CAR maps на каждом из 256 внутренних sites. Для семи вызовов и optional current mark:

* минимум численной coframe Julia-defect `>0.639`, link defect `>0.5867`, material slack `>0.3818`; максимальная ошибка `J^T J=I` `<2.7e−15`, CAR map `<4.5e−16`, Lorentz `<4.5e−16`;
* исходный B21 центр воспроизведён по всем 256 sites: max ошибки raw `u`, `U`, `Psi` соответственно `3.47e−18`, `5.21e−18`, `2.05e−18`;
* весь SITE `256×256` сохраняет born input с ошибкой `<10^-15`; исходный Fourier Gram проверен целочисленно; сохранение RIGHT проверено на произвольной колонке;
* [check_bound_leaves.py](check_bound_leaves.py) независимо связал все A11 source-leaves с готовыми локальными Julia и полными CAR/RIGHT amplitudes: для центра и one-hot sample проверено `2·7·256·282=1 010 688` моментов, max абсолютная ошибка `5.21e−18`; inverse PF на этом шаге не применяется повторно;
* для всех семи банков центр и one-hot sample сверены с независимой 40-digit `mpmath` реализацией. Отдельно проверен sample с неединичным proper link через произвольную точность `sqrtm`, один элемент full-column `O_b`, а также identity padding. Это сравнение не есть interval certificate.

Строгий положительный запас для **всего** SAM cube получен объединением точного B21 chart envelope и отдельного рационального [STRICT_SLACK.json](STRICT_SLACK.json) для неизменяемых references: `||u_ref,column||²<1/50`, минимальное singular value `>2/25`, coframe Julia defect `>49/50`, link defect `>=115/196`, material slack `>1/3`. Для последней оценки используются исходные точные неравенства `F_h<1/8`, `k0>20`, `309/500<p<619/1000`. Для boost точная норма exterior после деления на два — `9/14`; для rotations и identity — `1/2`. Этот запас доказывает допустимость target-формул, а не правильность невыданной native компиляции.

## 5. Воспроизведение

Из корня checkout:

```
OPENBLAS_NUM_THREADS=1 python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round25/check_targets.py
OPENBLAS_NUM_THREADS=1 python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round25/check_raw_frame.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round25/certify_reference_slack.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round25/build_mark_catalogue.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round25/mark_catalogue.py
OPENBLAS_NUM_THREADS=1 python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round25/check_bound_leaves.py
```

`check_targets.py` перезаписывает только артефакты этой папки; для построения каталога читается локальный A11 `direct/round11/PERIODIC_SOURCE_BINDING.json`, не изменяя его. Реестр checks и содержимое входов/выходов скреплены [RECEIPT.json](RECEIPT.json). Оставшиеся обязательные шаги — compiled fixed signs/READY, полный физический checkpoint и prefix/seal map, униформные ошибки/цена, реальный `C` и его источник. Эти задачи не следуют из одного совпадения target-columns.
