# Второй lattice heat coefficient: количественный остаток и точная граница source

16 октября 2026. Потребитель — §7.1
[causal-metric source bridge](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md).
Здесь не меняются оператор, trace, preparation, measure или action.
Используется полный 16-компонентный true-adjoint stencil из
[finite heat/source owner](A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md).

**Результат.** На явно более гладком controlled классе ниже доказан
fixed-positive-time heat expansion до второго порядка с остатком
`O(h^(9/4))`, в том числе после одной **гладкой** вариации controlled
полей. Это обосновывает H+J coefficient (14), а не существование
стационарной matter continuation. В §7 сформулирован дополнительный
raw-source шаг; §8 доказывает его через exact cyclic rows, pinching и
sampled-kernel estimate. Он относится к H+J, independent coframe,
scaled leftlink и observer rows; matter R остаётся отдельной задачей.

## 1. Пространства и необходимые гипотезы

Тор имеет период 1; замена периода меняет только константы. `h=1/L`,
сеточная норма `h^4 sum_x |psi(x)|^2`, fibre `Lambda R^4` размерности16.
`J_h` — изометрия дискретного Fourier transform в trig space с canonical
частотами `-L/2 <= k_r < L/2`. Она не удаляет ни одной lattice mode.
`P_N` — Fourier projection `|k|_infty<=N`, где `1<=N<L/4`.

Пишем

```text
delta_r=(S_r-I)/h,
Lambda_h=(I+sum_r delta_r* delta_r)^(1/2),
||v||_(H_h^s)=||Lambda_h^s v||_2,
A_h=D_h^2>=0,
D_h=d_h+d_h*,
d_h=sum_r c(u_r(x))(M_(h,r)(x)S_r-I)/h.                    (R1)
```

Звёздочка — настоящий Hilbert adjoint со всеми coefficient shifts.
После actual measure/observer isometries всё рассматривается в этой
фиксированной Hilbert space. Нормы для continuum используют
`Lambda=(I-Delta_flat)^(1/2)`. На embedded grid trig space они равномерно
эквивалентны `H_h^s`: для canonical частоты
`4|k_r| <= |(exp(2pi i h k_r)-1)/h| <= 2pi|k_r|`.

Нужны следующие условия; старых C6 hypotheses недостаточно для данной
количественной оценки.

1. `s_min U>=sigma>0`, где rows U равны u_r. Сохраняется ранее
   доказанный full16 Gårding estimate
   `||D_h v||^2>=c||v||_(H_h^1)^2-C||v||^2`.
2. Коэффициенты первого порядка D_h и его нормированные lower-order
   коэффициенты имеют равномерные spatial `C^192` bounds. В частности,
   это требуется для `(M_h-I)/h`, а не только для M_h. Также требуются
   соответствующие bounds одной parameter variation. Observer, его
   whitening и inverse находятся в fixed compact timelike chart.
3. M_h — exact path transport уже заданного smooth connection, а не
   произвольная семья `I+O(h)`. На smooth core поэтому существуют
   **те же** D0,D1,D2 из (13) bridge-owner, и

   ```text
   D_h f = D0 f+h D1 f+h^2 D2 f+h^3 R_(h,3) f,
   ||R_(h,3)f||_2 <= C||f||_(H^4).                      (R2)
   ```

   То же верно после одной bounded smooth variation. Коэффициенты
   remainder и их нужные derivatives равномерно bounded. Exact path
   transport bounded smooth connection обеспечивает (R2) интегральным
   Taylor remainder для `exp(h nabla_r)`; true-adjoint expansion
   получается из той же formula после переноса shifts. Для LC graph
   bounds должны налагаться на actual coefficients, то есть на исходный
   coframe/angle требуется дополнительная производная connection law.
4. `beta0<=beta<=beta1`, `beta0>0`. Для H+J фиксированы `0<z<1`, M и
   прочие calibrations в каждой field variation. Нет short-time
   uniformity при `beta->0`.

C192 — намеренно консервативный достаточный бюджет. Sobolev orders
в §§1–6 меньше128, а усиленный raw/clock budget §8 меньше160; запас включает
weighted Fourier coefficient summation в размерности4, shifted adjoint
и одну parameter variation. Минимальная регулярность здесь не заявлена.
Для actual independent raw variations в §7 их производные в C192
**не** предполагаются.

## 2. Projected elliptic induction: почему работает именно P A P

`A_(h,N)=P_N A_h P_N` рассматривается на `V_N=ran P_N`. В общем случае
он **не равен** `(P_N D_h P_N)^2`. Ниже используется form
`<v,A_(h,N)v>=||D_h v||^2`, а не такая неверная замена.

Равномерный discrete multiplier commutator estimate имеет вид

```text
||[Lambda_h^k,D_h]v||_2 <= C_k||v||_(H_h^k).              (R3)
```

Вот необходимое обоснование uniformity. D_h есть сумма first differences
с bounded coefficients и bounded lower-order terms; shifted adjoint
коэффициент содержит лишь normalised first difference u. Для Fourier
multiplier `lambda_h(k)` triangle inequality следует из
`zeta(k)=zeta(l)+exp(2pi i h l)zeta(k-l)`. Поэтому разность
`lambda_h(k)^k-lambda_h(l)^k` bounded величиной
`C_k lambda_h(k-l)(lambda_h(l)^(k-1)+lambda_h(k-l)^(k-1))`.
Convolution/Young estimate использует weighted l1 norm Fourier
коэффициентов. Uniform sampled C bounds дают эту l1 norm: aliases
суммируются до взятия нормы, с четырьмя дополнительными степенями
decay и запасом. Это доказывает (R3) без `h^-1` в C_k. Тот же расчёт
показывает `||D_h v||_(H_h^k)<=C_k||v||_(H_h^(k+1))`.

`P_N` коммутирует с Lambda_h. Для v в V_N точное тождество

```text
<A_(h,N)v,Lambda_h^(2k)v>
 =||D_h Lambda_h^k v||^2
  +<[Lambda_h^k,D_h]v,D_h Lambda_h^k v>
  +<[Lambda_h^k,D_h]D_h v,Lambda_h^k v>                  (R4)
```

следует из selfadjointness D_h и Lambda_h. Для complex inner product
при оценке берётся real part. Оба последних члена bounded
`C_k||v||_(H_h^(k+1))||v||_(H_h^k)` по (R3).
Применяя base Gårding к `Lambda_h^k v`, затем Young inequality,
получаем

```text
Re <A_(h,N)v,Lambda_h^(2k)v>
 >=c_k||v||_(H_h^(k+1))^2-C_k||v||_(H_h^k)^2.
```

С другой стороны, left side не превосходит
`||A_(h,N)v||_(H_h^(k-1))||v||_(H_h^(k+1))`.
Interpolation `H^k` между H^(k+1) и L2 даёт

```text
||v||_(H_h^(k+1))
 <=C_k(||A_(h,N)v||_(H_h^(k-1))+||v||_2).              (R5)
```

Константы независимы от h,N. Та же оценка верна для полного A_h и для
continuum A0. В частности графы `(1+A_(h,N))^m` равномерно эквивалентны
`H_h^(2m) intersect V_N`; это следует итерацией (R5), а не спектральным
утверждением о principal symbol compressed D.

Отсюда для всех требуемых s:

```text
||exp(-t A_(h,N))||_(H_h^s -> H_h^s)<=C_s,
||exp(-t A_(h,N))||_(H_h^s -> H_h^(s+r))<=C_(s,r)t^(-r/2)
                                                  (0<t<=beta1). (R6)
```

Negative s следуют duality, fractional orders — interpolation. Для
одной гладкой variation `dot A`, bounded как `H^(s+1)->H^(s-1)`,
Duhamel formula даёт uniform H^s stability derivative semigroup:

```text
||dot E(t)||_(H^s->H^s)
 <=C integral_0^t (t-v)^(-1/2)v^(-1/2)dv<=C pi.          (R7)
```

Это относится и к compressed `dot A_N=P_N dot A P_N`. Здесь гладкость
variation существенна: для raw rough coframe variation нельзя молча
использовать тот же form bound.

## 3. Uniform trace smoothing без borderline trace assertion

Base form inequality и minmax дают uniform counting
`#{lambda_j(A_(h,N))<=R}<=C(1+R)^2`. Поэтому (R5)–(R6) влекут
uniform weighted heat nuclear norms при положительном времени.
Можно также явно вставить trace-class multiplier:

```text
Tr Lambda_h^(-6)
 =16 sum_(canonical k) (1+sum_r |zeta_r(k)/h|^2)^(-3)
 <=C sum_(k in Z^4)(1+|k|^2)^(-3)<infinity.              (R8)
```

Это равномерно по h, и верно после P_N. `Lambda^-4` в размерности4
**не** является допустимой заменой: это borderline divergent sum.
Из (R6), heat splitting пополам и (R8) следует

```text
||Lambda_h^a E_N(t) Lambda_h^b||_1<=C_(a,b,t0), t>=t0>0. (R9)
```

Например вставляем Lambda^-6 справа и оцениваем
`Lambda^a E_N(t) Lambda^(b+6)` по (R6) и duality.
`dot E_N(t)` имеет ту же положительно-временную smoothing: применяем
`dot E_N(t)=dot E_N(t/2)E_N(t/2)+E_N(t/2)dot E_N(t/2)` и (R7).
Все эти assertions сохраняют полный fibre16 и полный thermal trace.

## 4. Galerkin error: smooth data residual и doubling

Здесь A обозначает либо A_h, либо A0; Lambda и P — соответствующие
Fourier operators, `E(t)=exp(-t A)`, `F(t)=P exp(-t P A P)P`.
Для smooth f положим `u=E(t)f`, `v=exp(-t P A P)P f`.
Тогда w=Pu-v удовлетворяет **точному** уравнению

```text
w'+PAP w = -P A(I-P)u,  w(0)=0.                        (R10)
```

Для `0<=t<=beta1`, используя uniform H4 stability compressed heat и
`A:H^6->H^4`, получаем

```text
||w(t)||_(H^4)
 <=C integral_0^t ||(I-P)E(v)f||_(H^6)dv
 <=C N^(-96)||f||_(H^102).
```

Добавляется `||(I-P)u||_(H^4)<=C N^(-98)||f||_(H^102)`.
Следовательно, для `R(t)=E(t)-F(t)`

```text
||Lambda^4 R(t)Lambda^(-102)||<=C N^(-96),
                                   0<=t<=beta1.         (R11)
```

Это smooth-input estimate, не operator-norm approximation при t=0.
Начальный R(0)=I-P как раз obeys (R11). Одна гладкая derivative
сохраняет (R11): differentiating Duhamel representation (R10)
порождает `dot E_N`, `dot A`, `dot E`; (R7) даёт нужные H^4/H^102
stability без endpoint singularity. `dot A:H^6->H^4` и его higher
Sobolev analogues имеют те же bounds.

Для weighted nuclear norm используем точное doubling identity

```text
R(t)=E(t/2)R(t/2)+R(t/2)F(t/2).                         (R12)
```

R selfadjoint. Если `B=Lambda^4 R Lambda^(-102)`, то
`R=Lambda^(-4)B Lambda^102=Lambda^102 B* Lambda^(-4)`.
Для `0<=a,b<=4` первый член в (R12) поэтому имеет вид

```text
Lambda^a E(t/2)Lambda^102 B* Lambda^(b-4),
```

а второй —

```text
Lambda^(a-4)B Lambda^102 F(t/2)Lambda^b.
```

Положительно-временные factors nuclear по (R8)–(R9), в частности
достаточно smoothing до order108. Получаем строгую лемму

```text
||Lambda^a [E(t)-F(t)]Lambda^b||_1 <= C N^(-96),
                 beta0<=t<=beta1, 0<=a,b<=4.            (R13)
```

Та же оценка верна после одной bounded smooth variation: differentiate
(R12), используй (R11) для R,dot R и (R9) для горячих E,F,dot E,dot F.
Таким образом short-time singularities в исходной Duhamel integral
не интегрируются по отдельности; сначала применяется smooth-input
estimate и doubling. C192 покрывает order108 плюс coefficient/adjoint
padding. В этом доказательстве нет предположения об экспоненциальных
пространственных Fourier tails variable-coefficient eigenfunctions.

## 5. Второе разложение на конечном блоке и бюджет N^24

На V_N через Fourier isometry actual grid operator обозначим A_h,N.
Положим

```text
A0=D0^2,
A1={D0,D1},
A2={D0,D2}+D1^2,
Aj,N=P_N Aj P_N.
```

Из (R2), true adjoints и expansion **квадратичной формы** `||D_h f||^2`
следует

```text
||A_h,N-A0,N-h A1,N-h^2 A2,N|| <= C h^3 N^5,            (R14)
```

и та же оценка для одной bounded smooth derivative. Здесь `hN<=1`.
Проверка orders: remainder D имеет order4, его product с D0 — order5;
`D1 D2` тоже order5. Члены `h^4 D2^2` и products с remainder
поглощаются `h^3 N^5`, поскольку hN<=1. Не требуется cancellation
leading order A1; безопасные bounds —

```text
||A0,N||,||dot A0,N||<=C N^2,
||A1,N||,||dot A1,N||<=C N^3,
||A2,N||,||dot A2,N||<=C N^4.                            (R15)
```

Sampling/alias term в (R14) не пропущен. Для `|m|<=2N<L/2`
sampled coefficient Fourier error есть
`sum_(ell!=0) b_hat(m+L ell)`, bounded `C h^16` при bounded C16.
Row sum на V_N добавляет не более `C N^4`; derivatives plane waves
до нужного order дают безопасный alias bound `C h^16 N^8`.
Он поглощается правой частью (R14). Normalised difference/transport
coefficients actual D_h имеют uniform C16 bounds по §1. Для этого
аргумента нельзя использовать только bound на ненормированный M_h.

Разложим matrix exponential around A0,N. Его первые коэффициенты:

```text
E0,N(t)=exp(-t A0,N),
E1,N(t)=-integral_(s0+s1=t) E0,N(s0) A1,N E0,N(s1),
E2,N(t)=-integral_(s0+s1=t) E0,N(s0) A2,N E0,N(s1)
 +integral_(s0+s1+s2=t) E0,N(s0) A1,N E0,N(s1) A1,N E0,N(s2).
                                                               (R16)
```

На chosen cutoff `hN^3->0`; промежуточные matrices
`A0,N+v h A1,N+v^2 h^2 A2,N`, `0<=v<=1`, bounded below by -1
при достаточно малом h. Duhamel remainders поэтому имеют uniform
exponential bounds. Третий derivative содержит либо три A1,
либо A1,A2. Его operator-norm remainder bounded `C h^3 N^9`.
Одна background derivative добавляет максимум `dot A0,N`, то есть
ещё N^2; derivatives insertions A1,A2 сами не увеличивают orders.
Consistency replacement (R14) даёт меньший бюджет `h^3 N^7` после
одной derivative. Значит общий operator bound — `C h^3 N^11`.

Для weighted nuclear norm с a=b=4 rank V_N равен
`16(2N+1)^4<=C N^4`, а два weights дают N^8. Таким образом
получено `C h^3 N^23`; используем более простой upper bound

```text
||Lambda_h^4 [E_h,N-E0,N-h E1,N-h^2 E2,N]Lambda_h^4||_1
 <=C h^3 N^24,                                         (R17)
```

также после одной bounded smooth variation. N^24 здесь имеет
явный budget, а не выбирается по желаемой скорости.

Continuum E1,E2 определяются теми же integrals (R16) без P_N.
Они trace-class со всеми нужными weights. В каждом product не более
двух differential insertions суммарного order6; одна background
derivative добавляет максимум third insertion order2. Среди не более
четырёх heat intervals поэтому один имеет длину не меньше t/4.
Он обеспечивает smoothing, остальные
heat factors bounded в нужных Sobolev spaces. Поэтому нет
nonintegrable endpoint estimate. Telescoping finite/continuum
products использует (R11) для коротких intervals и горячий factor
для nuclear estimate, ровно как (R12). High-frequency tails insertions
контролируются `A1:H^(s+3)->H^s`, `A2:H^(s+4)->H^s`.
Даже с 96 powers tail, двумя order3 и одной order2 insertions, weights4+4,
two-order smooth-input loss и trace-class six-power insertion
максимальный Sobolev order меньше128. Отсюда

```text
||Lambda^4 [Ej,N-Ej]Lambda^4||_1 <= C N^(-96), j=0,1,2,  (R18)
```

после embedding; действует и одна smooth derivative. Это finite
insertion argument, не применение ellipticity к искусственному
fourth-order `A0+epsilon A1+epsilon^2 A2` при fixed epsilon.

Совмещая (R13),(R17),(R18), берём

```text
N=floor(h^(-1/32)),
h^3 N^24+N^(-96) <= C(h^(9/4)+h^3).                    (R19)
```

Это доказывает weighted fixed-time second expansion и его smooth C1
version с `O(h^(9/4))`. Все mesh modes остаются в исходном E_h;
P_N используется лишь для оценки ошибки.

## 6. H+J, moving normalizer, clock и граница matter

Полный Z имеет uniform positive lower bound: constant trial section
имеет bounded `||D_h v||`, поэтому minmax даёт bounded lowest
eigenvalue и `Z_h>=exp(-beta1 C)>0`. Следовательно log Z и его
настоящая derivative допускают то же expansion. Для J отделяется
его exact field-independent dimensional constant. Оставшаяся часть
имеет вид `Tr log(I+c E_h)`, `c=z/(1-z)>0`.
Integral representation

```text
log(I+c E)=integral_0^c E(I+t E)^(-1)dt
```

и resolvent identity дают expansion с тем же остатком; inverses
равномерно bounded. Не требуется расходящийся geometric series при
`z/(1-z)>1`.

Отсюда H+J coefficient есть именно (14) causal bridge-owner, включая
normalizer rank-one term. Нулевой `Tr E A1` на cone graph не удаляет
divided-difference susceptibility. Этот результат не вычисляет K2
заново и не заменяет его a2-fit.

Для exact native clock `alpha=c0 h^2`, uniform `I-alpha A_h>=b0>0`
позволяет Taylor expansion scalar clock с remainder
`C alpha^2 polynomial(lambda) exp(-c beta lambda)`.
Uniform graph/heat trace moments оценивают его trace и одну smooth
variation как `O(h^4)`. Поэтому добавляется ровно (15) owner.
Если integer schedule даёт `beta_h-beta=h^2 eta_h+o(h^2)`, сохраняется
`eta_h partial_beta S0`; limit eta_h не предполагается автоматически.

R не получается из heat theorem. Для его second expansion нужны
actual preparation jets `C_h=C0+h C1+h^2 C2+O(h^3)` в достаточно
сильном Hilbert–Schmidt graph/Sobolev norm, с normalized mass bounded
away from0, и те же bounds actual field dependence. Например uniform
H12 expansion — достаточное консервативное условие для quotient и
его first rows. При наличии такого actual branch formula (16) верна
с сохранением reference/workspace. Прежняя compactness critical
reduced densities даёт лишь o(1), не h^2 corrector. Shell compatibility
и off-shell amplitude equation являются отдельными обязательствами;
их не заменяет trace identity.

## 7. Что доказано и что ещё нужно для independent raw sources

Этот раздел отделяет исходный raw-source gap от smooth theorem
§§1–6; для controlled H+J он замкнут в §8 в explicit same-grid норме.
Теорема выше даёт smooth C1 estimate: variation контролируется в том
же high-regularity norm, что и background. Она **не** получена
дифференцированием value estimate в rough C0 directions.

Есть полезный exact lowblock факт для independent coframe source.
При fixed M,n variation forward равна
`dot d_h=sum c(dot u_r)(M_r S_r-I)/h`. В bilinear derivative A_h
каждый adjoint variation переносится на smooth neighbouring factor.
Например

```text
<D_h f,dot d_h* g>=<dot d_h D_h f,g>.
```

Поэтому ни одна difference derivative rough dot u не требуется.
Для f,g в V_N expansion этих forms до h^2 использует лишь Taylor
smooth background и f,g. Его remainder bounded
`C h^3 N^5 ||dot u||_infty ||f|| ||g||`. Это raw C0 bound **на
lowblock form**, а не уже полная raw-source theorem.

Для global raw source нужны exact site/edge kernel rows. Coframe row
выражается cyclic diagonal products с `D_h kappa_h` и forward
difference; leftlink row при `dot A=h xi A` не содержит h^-1;
observer row использует commutator `[d_h,{D_h,kappa_h}]` against
bounded pointwise K. После cyclicity variation derivatives не берутся.
Weighted estimate (R13) контролирует необходимые operator products.
Однако для полного принятого raw claim надо явно завершить следующий
шаг для **того же выбранного site/edge convention**:

> Taylor/alias comparison exact finite cyclic diagonals, включая
> coefficient shifts и moving-adjoint terms, с sampled continuum
> coefficient densities j0,j1,j2 должен иметь remainder O(h^(9/4))
> в same-grid l1. Нужно вывести все rows и показать, что kernel
> derivative orders укладываются в proved weighted norms.

Это точная source-kernel lemma, которая ещё не следует из §§1–6.
Её доказательство для H+J дано отдельно в §8. В частности нельзя
молча отождествить leftlink tangent `dot A=h xi A` с вариацией smooth
connection, из которой взята parallel transport. Их conversion есть
covariant edge average, с Bernoulli inverse coefficient1/12; она
принадлежит отдельному link-cotangent consumer. Smooth variations
path law уже покрыты §1–6, independent raw leftlink rows требуют
названного site/edge transfer.

Правильная цель raw comparison имеет вид

```text
sum_(x,a)|E_(h,a)(x)-h^4[j0,a+h j1,a+h^2 j2,a](x)|=o(h^2). (R20)
```

Обе стороны задают covectors на **одном и том же finite grid test
space**. Это не total-variation convergence atomic measure к smooth
continuum measure: такая convergence невозможна. Piecewise-constant
reconstruction также нельзя напрямую сравнивать с j0 до o(h^2),
поскольку сама cell geometry обычно даёт O(h) error. Нужны именно
samples, либо exact cell averages с вычисленными averaging correctors.

Все10 metric slots сохраняются через bounded pointwise coframe lift
на independent raw domain, с прежними doubled offdiagonal packing
factors. Это statement о том, какой source lemma требуется, а не
доказательство всех её rows. LC pullback дополнительно содержит
derivatives connection law; smooth theta tests покрыты настоящей
теоремой, rough LC tests требуют соответствующего adjoint-transfer
estimate и не следуют из одной l1 ошибки independent-link row.

Физическое admission, complete field-to-program binding, actual
prepared branch и stationarity не добавлены как гипотезы по желаемому
ответу. Доказанный progress — quantitative fixed-beta second heat
coefficient на явно controlled smooth классе. §8 ниже завершает H+J
часть (R20); actual matter continuation не предполагается.
Даже полное native h^-2 expansion не завершит original fixed-g/tau terminal:
actual comparator/source equality, physical admission и сопоставление
с полным Einstein source остаются самостоятельными обязательствами.

## 8. Exact raw rows, sampled-kernel lemma и clock covector

### 8.1. Какой raw covector сравнивается

Положим `a=1-z`, `E_h=exp(-beta A_h)`, `Z_h=Tr E_h`,

```text
kappa_h=-E_h/Z_h+M z beta E_h(a+z E_h)^(-1),
Q_h={D_h,kappa_h},
B_(h,r)=(M_(h,r)S_r-I)/h,
W_(h,r)=M_(h,r)S_r.
```

В этом подразделе kappa_h — continuous-clock H+J covector на том же
finite stencil. Actual finite clock добавляется в §8.6. Вся Hilbert
space уже whitening-изометрична actual positive pairing; trace остаётся
полным, multiplicity16 не заменяется scalar trace.

Для любого actual forward variation точное тождество есть

```text
dot S_(H+J)=Tr kappa_h {D_h,dot D_h}
           =2 Re Tr Q_h dot d_h.                        (R21)
```

Q selfadjoint, поскольку D и kappa selfadjoint. Никакого дополнительного
factor2 из full16 trace здесь нет. Exact independent rows:

```text
coframe: dot d_h=sum_r dot C_r B_(h,r),
         T_(h,r)^u=B_(h,r) Q_h;

leftlink: dot A_r=h xi_r A_r,
         dot d_h=sum_r C_r Gamma_x(xi_r) W_(h,r),
         T_(h,r)^link=W_(h,r) Q_h C_r;

observer: K_x=dot I_x I_x^(-1), dot d_h=[K,d_h],
          T_h^obs=d_h Q_h-Q_h d_h.                      (R22)
```

Здесь `C_r=c(u_r)`, `Gamma_x=I_x Gamma I_x^(-1)` в actual retained
basis. Source pairings равны соответственно `2 Re Tr T^u dot C`,
`2 Re Tr T^link Gamma_x(xi)` и `2 Re Tr T^obs K`.
В observer row original forward не зависит от independent observer,
а вся его зависимость после whitening действительно есть conjugation;
поэтому commutator включает moving endpoints, а не frozen M.

Coframe formula в (R22) выписана при fixed whitening I. Если actual
pairing/measure law даёт `I_total=sqrt(mu) I_n` и `mu=mu(F)`, то
`K_total=K_n+(1/2)dot(log mu) I`: к coframe pullback добавляется тот же
exact cyclic row `2 Re Tr T^obs K_mu`. Independent measure row
получается той же формулой. Никакая actual measure dependency здесь
не замораживается; другие явно заданные measure/calibration dependencies
цены сохраняются отдельным chain rule. В (R21) calibrations фиксированы
внутри field variation, а actual clock schedule учтён в §8.6.

Все variation operators справа после cyclicity являются multiplication
operators. Их C0 norm контролируется в fixed compact field chart.
Ни `delta_r dot u`, ни `delta_r xi`, ни `delta_r K` не берутся.
Норма link test — `||xi||_infty` при **scaled physical tangent**
`dot A=h xi A`. Для unscaled `||dot A||_infty` источник имеет
дополнительный h^-1; соответствующая o(h^2) теорема здесь не заявлена.

В scaled grid Hilbert space diagonal blocks операторной matrix
обозначим `[T]_(xx)`. Они уже содержат h^4 continuum kernel factor.
Block pinching даёт

```text
sum_x ||[T]_(xx)||_(S1(fibre16))<=||T||_(S1(H_h)).        (R23)
```

Это contraction S1 conditional expectation на site blocks. Отсюда
следует same-grid l1 error всех компонент row, с фиксированным
finite-dimensional factor для выбранного real component basis.
Это не comparison atomic measure с continuum measure.

### 8.2. Рациональный kappa и actual operators вне P_N

Обозначим `E_(h,N)=P_N exp(-beta A_(h,N))P_N` и определим kappa_(h,N)
той же rational formula, с Z_(h,N)=Tr E_(h,N). Inverse на complement
равен a^-1, но kappa_(h,N) там равна0. Uniform positive lower bounds
Z,Z_N следуют §6.

Для `R_E=(a+z E)^(-1)` точное тождество

```text
R_E=a^(-1)I-z a^(-1) E R_E
```

показывает uniform boundedness R_E на всех нужных positive Sobolev
spaces: L2 norm не превосходит a^-1, а E при fixed beta smoothing.
Negative spaces следуют selfadjoint duality. То же верно для E_N.
Кроме того,

```text
E R_E-F R_F=a R_E(E-F)R_F.
```

Поэтому (R13) переносится на kappa в weighted nuclear norms.
Усилим q=96 в smooth-input argument до q=112. Это меняет H102 на
H118 при output H4, а hot smoothing — на H124. С конечными
insertions и clock-polynomial padding максимальный используемый
Sobolev order можно взять меньше160; C192 сохраняется. Таким образом

```text
||Lambda_h^4(kappa_h-kappa_(h,N))Lambda_h^4||_1
 <=C N^(-112).                                        (R24)
```

Каждый actual B_h,d_h,D_h имеет uniform order1 bounds на Sobolev
spaces, W_h — order0. Поэтому (R24) и (R23) контролируют ошибки
(R22) при замене kappa_h на kappa_(h,N): в каждом product не более
двух **actual first-order** insertions. Например

```text
B_h {D_h,delta kappa}
=B_h D_h delta kappa+B_h delta kappa D_h,
```

а обе nuclear norms bounded constant times weighted norm (R24).
Точно так же оценивается `[d_h,{D_h,delta kappa}]`.
Здесь B_h,d_h,D_h стоят **вне P_N**. Замена их на P_N D_h P_N
не используется и в общем случае дала бы другие source diagonals.

### 8.3. Все product jets выписаны до sampling

На smooth core actual proper transport даёт

```text
b_r,j=(1/(j+1)!) nabla_r^(j+1), j=0,1,2,
w_r,j=(1/j!) nabla_r^j,
d_j=sum_r C_r b_r,j,
D_j=d_j+d_j^dagger.                                   (R25)
```

Forward и shifted true adjoint имеют order-h^3 remainder H4->L2,
также при применении к smooth plane-wave factors. Это тот же
integral Taylor argument (R2), применённый к d и d^dagger отдельно.

Пусть E0,E1,E2 — (R16), `Z_j=Tr E_j`. Kappa jets определяются
**полной** rational map, не freezing Z. Для ясности:

```text
R0=(a+z E0)^(-1),
R1=-z R0 E1 R0,
R2=-z R0 E2 R0+z^2 R0 E1 R0 E1 R0;

kappa0^H=-E0/Z0,
kappa1^H=-E1/Z0+E0 Z1/Z0^2,
kappa2^H=-E2/Z0+E1 Z1/Z0^2+E0 Z2/Z0^2-E0 Z1^2/Z0^3,
kappa_j^J=M z beta sum_(l+m=j) E_l R_m.
```

Ставим `kappa_j=kappa_j^H+kappa_j^J` и

```text
Q_j=sum_(l+m=j) {D_l,kappa_m};

T_r,j^u   =sum_(l+m=j) b_r,l Q_m,
T_r,j^link=sum_(l+m=j) w_r,l Q_m C_r,
T_j^obs   =sum_(l+m=j) (d_l Q_m-Q_m d_l).                (R26)
```

Суммы j=0,1,2 конечны. Все coefficient shifts/derivatives на right
kernel leg задаются указанными genuine adjoints, а не независимо
выбранным geometric inverse. Plain second-order source product имеет
total differential order не более4: coframe b_l D_i даёт l+i+2<=4,
observer d_l D_i — то же, link w_l D_i — не более3.

Эти formulas непосредственно определяют **raw leftlink** coefficients.
Их нельзя отождествлять с Euler covector path connection. Conversion
с covariant edge average, named pairing и inverse coefficient1/12
доказана в [raw link cotangent owner](A4D_RAW_LINK_COTANGENT_JET.md).
Для arbitrary grid tests никакая inverse series не применяется.

### 8.4. Почему finite kernel действительно даёт те же grid samples

Пусть K_N имеет matrix K_kl на V_N. Его exact continuum kernel
содержит конечную сумму

```text
K_N(x,y)=sum_(k,l in V_N) exp(2pi i kx) K_kl exp(-2pi i ly).
```

Grid matrix того же operator через J_h равна `h^4 K_N(x,y)` в grid
points. Применяя actual B_h,d_h на left kernel variable и adjoint
operators на right variable, получаем **точные** source matrix rows.
Taylor expansion каждого smooth factor в x±h даёт (R25)–(R26),
после чего ставятся y=x и actual sampled smooth coefficients.
Ни coefficient multiplier, ни его shift не проецируется через P_N.
Source density в общем случае не является trig polynomial: она
finite plane-wave kernel с smooth coefficient multipliers. Это не
мешает exact identity с sampled continuum differential kernel jets.

Осталось количественно сравнить finite kappa_j,N с continuum kappa_j.
Rational identities и finite insertion argument (R18), с q=112,
дают

```text
||kappa_j,N-P_N kappa_j P_N||_1<=C N^(-112), j=0,1,2.    (R27)
```

Для finite plane space явная Bernstein evaluation bound есть

```text
||eval_x partial^alpha |_V_N||_(L2->C)<=C_alpha N^(2+|alpha|).
```

Применим SVD конечной matrix difference (R27). Kernel diagonal с
derivative orders alpha,beta поэтому bounded в sup norm величиной
`C N^(4+|alpha|+|beta|)||difference||_1`. Для (R26) теряется максимум
N^8. Smooth coefficient multipliers и их указанные derivatives bounded
uniformly. Значит sampled source density error здесь не более
`C N^(-104)`. Для continuum Fourier tails вне P_N тот же conclusion
следует из Sobolev evaluation с projection tail, например left weight
`98+|alpha|` даёт N^-96, а right weight `>2+|beta|` делает evaluation
bounded. Нужные weighted trace bounds kappa_j следуют fixed-time
smoothing; order budget остаётся меньше160. Для всех трёх rows
безопасно сохраняем общий upper bound `C N^-96`.

Так point evaluation доказывается отдельно; оно не выводится из
одной unweighted trace norm. Умножение ошибки sup density на h^4
и суммирование по всем L^4 sites сохраняет ту же оценку.

### 8.5. Конечный Taylor remainder raw row и окончательная норма

На V_N конечномерное exponential/rational expansion имеет remainder
из (R17). Для row estimate не дифференцируем его в rough direction;
подставляем его в exact products (R22) и используем (R23)–(R24).
Для остальных Taylor products достаточно следующих explicit bounds:

* `||kappa_j,N||<=C N^(3j)`, j=0,1,2, из (R16) и rational jets;
* differential factor order m на plane subspace и его adjoint имеет
  norm `<=C N^m`; smooth multipliers остаются actual multipliers;
* при total omitted h-degree3 два stencil factors имеют combined
  order не более5; с kappa2,N безопасный operator budget — N^9;
* все products с finite kappa имеют rank не более `C N^4`.
  Right unbounded difference оценивается adjoint-on-V_N, а не его
  полным O(h^-1) norm. Поэтому stencil/product omitted terms имеют
  nuclear bound `C h^3 N^13`.

Heat/rational remainder в W4 из (R17) даёт более крупный, но уже
доказанный budget `C h^3 N^24` после actual insertions. Alias bound
из (R14) меньше этих terms. С запасом для всех named row products
используем `C h^3 N^30`; ни одна оценка не берёт derivative rough
variation. При

```text
N=floor(h^(-1/40)),
h^3 N^30+N^(-96)<=C(h^(9/4)+h^(12/5)).                  (R28)
```

Пусть j_r,a,j — diagonal continuum coefficient densities (R26),
tested против c(e_a), Gamma_x basis или actual K chart. Тогда

```text
sum_(x,a)|E_(h,a)(x)
 -h^4[j0,a(x)+h j1,a(x)+h^2 j2,a(x)]|<=C h^(9/4).       (R29)
```

Это uniform dual estimate **на одном finite grid test space** для
`||dot u||_infty+||xi||_infty+||K||_infty<=1`, с фиксированным finite
component norm. Она сохраняет all16, observer endpoints и actual
unprojected link factors. Bounded pointwise map от всех10 metric
slots к dot u и K переносит (R29) на independent metric rows,
включая прежние doubled offdiagonal packed factors. Никакой metric
slot не заморожен. Bound не переносится автоматически на unscaled
link matrix tangent или на невыбранную field-dependent preparation.

### 8.6. Actual finite-clock source: необходим global Z term

Здесь alpha=c0 h^2, `m alpha=beta`, `B=I-alpha A_h>=b0>0`,
`K=B^m`, `P=B^(m-1)`. Точный native clock covector есть

```text
kappa_native=-P/Tr K+M z beta P(a+z K)^(-1).
```

Scalar expansion, с сохранением normalizer, даёт

```text
kappa_native(A)=kappa0(A)+h^2 kappa_c(A)+O(h^4),
kappa_c=c0[A kappa0+(1/2) A^2 kappa0_prime
                 -(beta/2) M2_heat E/Z^2],
M2_heat=Tr A^2 E.                                     (R30)
```

Prime — scalar derivative по eigenvalue при fixed Z. Последний term
является global normalizer derivative; его нельзя удалить.
M2_heat — heat moment; он отличается от coefficient Z2=Tr E2 в §8.3.
Эквивалентно (R30) следует из

```text
P=E+alpha(A-beta A^2/2)E+O(alpha^2),
K=E-(beta alpha/2)A^2 E+O(alpha^2).
```

Uniform strict B>0 и fixed beta дают scalar remainder bounded
`C alpha^2 polynomial(lambda) exp(-c beta lambda)`.
Graph/heat moments переводят это в weighted nuclear O(h^4).
В second source jets поэтому заменяем только

```text
kappa2 <- kappa2+kappa_c(A0),
Q2 <- Q2+{D0,kappa_c(A0)}.                              (R31)
```

Переход kappa_c(A_h) к kappa_c(A0) требует лишь first-order spatial
consistency, так как уже умножен на h^2. На finite block наибольший
clock insertion A^2 имеет order4. Консервативный finite-block count:
first-order exponential difference даёт hN^3, два Lambda^4 weights —
N^8, rank — N^4, clock A^2 — N^4, ещё две row insertions — N^2.
После умножения на h^2 это `h^3 N^21<=h^3 N^27`, меньше (R28).
Здесь row insertions с запасом посчитаны ещё раз, хотя weighted norm
уже позволяет их поглотить. Для clock tails
используются те же q112 estimates с двумя дополнительными A insertions:
даже total kernel derivative order6 теряет не более N^10 при sampling,
что оставляет N^-102. Все graph/trace orders с padding меньше160.
Это объясняет, почему обычной O(1/m) clock estimate для данного
coefficient/source consumer было бы недостаточно.

Если beta_h имеет h^2 rounding correction, добавляются actual
`eta_h partial_beta` coefficient и его rows, при fixed schedule в
field variation. Integer m не дифференцируется.

Таким образом (R29) с (R31) замыкает **H+J** raw same-grid second
source estimate на §1 controlled классе. Это не утверждает actual
matter corrector, link/observer Euler equations, nonempty stationary
branch, physical admission или исходное Einstein/comparator equality.
