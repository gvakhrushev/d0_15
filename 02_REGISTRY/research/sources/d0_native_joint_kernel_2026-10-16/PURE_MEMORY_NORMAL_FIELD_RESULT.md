# Pure native memory: полный normal-field consumer

16 октября 2026. **VALIDATED: полный40806-dimensional real normal operator
имеет инерцию33954+/6852-/0.** Все488 новых outward interval blocks
прошли на исходном root rectangle; normal и optimized scientific JSON
побайтно одинаковы. Настоящий local critical locus около actual rank8
seed исчерпывается точным57195-dimensional flat amplitude family.
Между faithful и pure подготовками при этом строго необходима потеря
normal invertibility; её nonlinear compatibility остаётся отдельным шагом.

Действуют тот же conditional finite L8 heat root,4096 momenta, full16
carrier, shell128, reference128 и actual native
`chi=(mask1+mask15)/sqrt(2)`. Prepared density имеет rank8:
`rho8=P_Omega/8 tensor |chi><chi|`, `Omega={+/-e_r}`. Исходные action,
g_tau, stored transport, calibration, globalZ и все signed Q gaps
сохраняются. Physical admission/refinement и вывод ОТО не утверждаются.

## 1. Точное равенство, которое оценивает interval consumer

Используем complex mixed symbol `H_ij=partial_(bar z_i)partial_(z_j)`
для q!=0. Пусть `l=k+q`, `J_i(k):k->l`,
`X_i(k)=D_l J_i(k)+J_i(k)D_k`. Обозначим
`r_k=0` на Omega, `r_k=(lambda_k-epsilon)^-1` вне Omega.
`H_old` — прежний полный faithful first-jet symbol, с complete heat/
feedback scalar moments, globalZ derivatives и old source `P/128`.
При **точном owned root** root-specific moment identity даёт
`C_kappa+C_old=0`, где C — contraction настоящего second chart jet.
Это identity прежнего root proof, не правило обнуления curvature
произвольного constrained critical point. Тогда

```text
H8 = H_old + Y_pure - C_old - J128 - DeltaQ_X,              (N1)

J128_ij = (1/128) sum_(k in Omega)
       Tr16[J_i(k)^*J_j(k)+J_j(k-q)J_i(k-q)^*],

DeltaQ_X,ij = (1/8) sum_(k in Omega)
 { r_(k+q) deltaell[X_i(k)^*X_j(k)]
  +r_(k-q) deltaell[X_j(k-q)X_i(k-q)^*] },
deltaell(A)=<chi,A chi>-Tr16(A)/16.                       (N2)
```

Нормировка `1/128=(1/8)*(1/16)` в J128 обязательна. Incoming term
имеет обратный порядок field indices; его Gram транспонируется.
Все signed r сохраняются, включая отрицательный ground contribution.
H_old использует все4096 scalar modes/119 exact energy features;
новые finite terms требуют лишь занятые incoming/predecessor nodes,
не более16 small full16 blocks. Ни matter, ни fullZ не заморожены.

Для восьми Hermitian Majoranas `g_(2j)=c_j+b_j`,
`g_(2j+1)=i(c_j-b_j)` actual chi имеет на even Clifford words ровно
восемь ненулевых expectations:

```text
mask:    0   3   60  63  204 207 240 243
value:   1  -i   -1   i   -1   i  -1   i.
K_IJ=ell_chi(g_I^*g_J)-delta_IJ, I,J of degrees0/2/4.      (N3)
```

Таким образом DeltaQ_X вычисляется точным Hermitian99x99 signed-XOR
K с нулевой диагональю и не более семи Gaussian-unit entries в строке;
`||K||<=7`. Это same-parity Gram identity. Full256 Gram имеет также
cross-parity coherences; они здесь не объявляются нулевыми.

Actual numerical assembler [pure_memory_symbol.py](pure_memory_symbol.py)
также сохраняет отдельно `C_kappa+C_old` midpoint residual, а outward
[pure_memory_interval.py](pure_memory_interval.py) использует (N1)
как analytic root-box extension. Равенство с constrained Hessian
требуется и утверждается в точном stationary root. Endpoint phase
conversion, binary64 assembly/Gram rounding, interval scalar variation
и finite-node errors должны входить в строгую signature-distance bound.

## 2. Full second chart jet, включая exterior curvature

Native regular coordinates: `u_r=(tau_r,rho_r z_r)`, `rho_r>0`,
`z_r in S2`, spatial return in SO3 с literal own-leg transport.
Для mixed row B=conjugate(i), column A=j положим `t=exp(2*pi*i*q_r/L)`,
`beta_A,beta_B` tangent к z, `dr_A,dr_B` radius jets,
`theta_A,theta_B` spin-angle jets. Тогда

```text
a_A=(dtau_A, dr_A z+rho beta_A),
u_AB=(0,dr_A beta_B+dr_B beta_A-rho(beta_A dot beta_B)z),
omega_A=(1-t) z cross beta_A+theta_A z,
omega_B=(1-bar t) z cross beta_B+theta_B z,
W_A=[omega_A]_cross, W_B=[omega_B]_cross,

k_AB= theta_A(1+bar t) beta_B/2
      +theta_B(1+t) beta_A/2+(t-bar t)(beta_A cross beta_B),
K_AB=diag(0,[k_AB]_cross),
R_AB=K_AB+(W_A W_B+W_B W_A)/2.                            (N4)
```

В последней строке W вложены как spatial skew4x4. K_AB — mixed
logarithmic one-body jet; R_AB — actual mixed matrix jet return.
Если `Gamma=Lambda_*`, то full exterior jet равен

```text
Lambda_AB=Gamma(K_AB)
                 +[Gamma(W_A)Gamma(W_B)+Gamma(W_B)Gamma(W_A)]/2.
F_AB(k)=L sum_r [(t_r(k)-1)c(u_AB,r)
  +t_r(k){c(a_A,r)Gamma(W_B,r)+c(a_B,r)Gamma(W_A,r)
                                      +c(u_r)Lambda_AB,r}],
D2_ij,0(k)=F2_ij(k)+F2_ji(k)^*.                          (N5)
```

Последняя строка меняет **и field indices**, а не берёт entrywise
`F2+F2^*`. Ни K_AB, ни symmetric product Gamma(W_A)Gamma(W_B)
не отбрасываются.

Для независимой full16 trace reduction используем точные exterior
identities; для любого R около I

```text
Tr16 Lambda(R)=det(I4+R),
Tr16 c(v)b(u)Lambda(R)=u^T R adj(I4+R)v,
Tr16 b(u)c(v)Lambda(R)=u^T adj(I4+R)v.                    (N6)
```

Они следуют дифференцированием `det(I+R)` по one-body matrix entry;
adjugate form полиномиальна и не требует inverse R+I. Если R — SO3
return, фиксирующий u, обе последние trace равны
`det(I+R)(u dot v)/2`. В частности stabilizer second derivative даёт
`Tr Gamma(W)^2=-8|omega|^2` и
`Tr c(v)b(u)Gamma(W)^2=-4|omega|^2(u dot v)`.

Дифференцирование (N6) с полными jets (N4) даёт удобную scalar formula:

```text
v_AB,r=-4 W_B,r a_A,r-4 W_A,r a_B,r
        +2u_r Tr(W_A,r W_B,r)-4K_AB,r u_r,
E_ij=sum_r [16 u_r dot u_AB,r+(2u_r-sum_s u_s) dot v_AB,r],
C_old,ij=lambda1/64 [E_ij+conj(E_ji)],
lambda1=L^2(2-sqrt(2)).                                  (N7)
```

Независимо от trace, actual SO3 returns фиксируют весь E0. Поэтому
`D(e_k chi)` имеет точную link-free first-action formula, хотя
`D^2(e_k chi)` и Schur term её не наследуют. Это даёт exact energy
`R_fixed=lambda1/(4 N_sites) sum_(x,r)(tau_r^2+rho_r^2)`,
где `N_sites=L^4=4096` (не full Hilbert dimension65536), и

```text
Y_pure,ij=lambda1/2 sum_(r:q_r=0)
 [conj(dtau_i,r)dtau_j,r+conj(dr_i,r)dr_j,r].              (N8)
```

Formula (N8) включает actual sphere u_AB: orientation contribution
сокращается с u dot u_AB. Для theta-only stabilizer направления
`C_pure=0`, но `C_old=-lambda1(d-3o)|omega|^2/8` ненулевой.
Такой countercontrol исключает замену полного second jet на ноль.
Формулы и positive normalization control находятся в
[PURE_MEMORY_FIELD_HESSIAN_INTERFACE.md](PURE_MEMORY_FIELD_HESSIAN_INTERFACE.md).

## 3. Полный V, shell sections и разрешённое сокращение по симметриям

Source submersion в actual rank8 доказана в
[RANK8_SOURCE_SUBMERSION.md](RANK8_SOURCE_SUBMERSION.md): real rank151.
Поэтому field coupling kernel совпадает с прежним полным kerT,
но field Hessian на этом kernel автоматически не совпадает.
Для nonzero shell transfers complete quotient sections равны pure
inactive coframes:12 complex dimensions при q=+/-2e_i и8 при
q=+/-e_i+/-e_j. Остальные field/link directions определяются source
compatibility, а не удаляются произвольным gauge choice.

[Exact shell restriction](PURE_MEMORY_SHELL_RESTRICTION.md) даёт

```text
Delta H_r=-i lambda1/2 [sum_sigma h_sigma/g_sigma]
                                      (u_r e0^T-e0 u_r^T). (N9)
```

Для opposite spatial q0170 `tau_i=tau_j=b`, сумма равна0. Поэтому
здесь H8 буквально совпадает с прежней trace restriction.
Immutable [result](OPPOSITE_SHELL_TRANSFER_RESULTS.json), SHA256
`ea994fef6edc38f4b01a98eed7379841f6a603dfbb02b641382bfa853f64db75`,
уже даёт strict whole-box inertia `6+/2-/0` после trace-only restricted
S4 congruence. Шесть spatial-opposite frequencies дают real `36+/12-`.
Семь q0 Gram directions строго положительны по существующему homogeneous
consumer; итого наследуются55 directions с inertia `43+/12-/0`.
Другие пять shell classes получают ненулевую rank2/leg correction
и требуют новой проверки суммы, а не переноса старой инерции.

Pure chi выделяет time. Spatial S3 сохраняет native chart и SO3-link
admission. Odd spatial permutation меняет sign top component chi;
CAR parity возвращает chi с точностью до общего знака и коммутирует
со всеми even source/Hessian operators. Поэтому используется S3 с
этим точным восстановлением seed. Global q->-q есть Fourier reality:
`H_-q=conj(H_q)`. Full time-spatial S4 symmetry pure source не требуется.

Nonselfconjugate complex block (p,n,z) даёт real +/-q pair (2p,2n,2z).
Selfconjugate q in {0,4}^4 имеет real polarization и считается один раз.
Все15 nonzero selfconjugate frequencies лежат вне Omega-Omega.
Полное real counting:

```text
outside Omega-Omega:40511,
nonzero shell kerT sections:8*12+24*8=288,
homogeneous Gram normal:7,
V8=40806.                                                (N10)
```

Новый interval consumer проверил483 outside-shell symmetry representatives
и пять оставшихся shell representatives. Это40751 новых real directions;
q0170 и q0 дают55 inherited directions без повторного расчёта.

## 4. Что завершает normal IFT и как считается full amplitude

Пусть все required interval comparisons доказали
`||B_q^* H8(q) B_q-Sigma_q||<=delta_q<1` с fixed exact-decimal square
congruence B_q, включая whole root box, conversions и roundoff.
Тогда inverse bound каждого блока
`||H8(q)^-1||<=||B_q||^2/(1-delta_q)` конечен. Вместе с55 inherited
directions это даёт uniform finite-dimensional normal criterion

```text
(H8^V)^*H8^V >= c^2 I,  c>0.                             (N11)
```

В [полном результате](PURE_MEMORY_FIELD_RESULTS.json) maximum
`delta_q=0.007301662519523286<1`, при q=(4,0,1,2). Его outward
ошибки включают actual root box, exact decimal B, phase conversion,
geometry, full scalar moments и compressed Gram rounding. На всех
nonzero V sections inverse norm в заявленных canonical mean-slice
Fourier coordinates не превосходит целого681252. Spatial mean-section
congruence стоит не более p<=4 по квадрату нормы; composition вычислена
точными Fraction и integer ceiling. Для q0170 отдельная inherited
оценка103; q0 Gram coercivity потребляется отдельно. Это конечная
координатная оценка, не refinement-uniform или исходная raw metric norm.

Exact rank-free [amplitude proof](RANK8_AMPLITUDE_FIBRE.md) использует
shell sphere `||C||=1`,151 source moments `mu_R(C)=0` и не обращает
rho8 или sqrt(rho8). Its source fibre dimension32616 включает все28800
rank-birth directions. Actual local Lorentz/observer representations
и constant SO4 coframe family, с единственным global SO3 overlap,
дают точную flat critical family dimension57195. В ней также остаются
три nongauge homogeneous Lorentz-Gram moduli; linear-link holonomies I.

Если real inertia V8 равна(p,n,z), `p+n+z=40806`,151 source-normal
coordinates и сопряжённых field coordinates добавляют hyperbolic pairs:

```text
raw shell-amplitude/field inertia=(p+151,n+151,57195+z),
dimension98303.                                         (N12)
```

Q-amplitude block `2(Delta_Q-epsilon) tensor I_ref` сохраняет прежние
strict scalar signs, gap и inertia `(16740352,4096,0)`, независимо от
rank C. Поэтому на исходной normalized amplitude domain

```text
full inertia=(p+16740503,n+4247,57195+z),
dimension16842751.                                      (N13)
```

Reference, source и rank-birth zeros уже входят в57195; отдельные16384
reference zeros повторно не добавляются. Если (N11) установлен, z=0,
normal IFT делает эту **уже построенную точную** flat family полным
локальным critical locus около rank8 seed, включая births of rank.
Одна лишь линейная нулевая мода при z>0 не доказывает новую ветвь.
Не утверждаются boundary/global completeness, новая physical preparation,
microscopic word selection, refinement law, continuum limit или ОТО.

| Aggregate field result | Статус этого документа |
|---|---|
| Full V8 real inertia (p,n,z) |33954+/6852-/0|
| Nonzero canonical normal inverse |<=681252; q0 strict coercivity separately|
| Exact inherited q0 + q0170 |55 directions,43+/12-/0|
| Raw shell-amplitude/field inertia |34105+/7003-/57195zero; dimension98303|
| Full normalized amplitude inertia |16774457+/11099-/57195zero; dimension16842751|
| Complete pure local Morse--Bott conclusion |Established at this conditional finite seed|

## 5. Строгая внутренняя потеря обратимости, а не готовая curved branch

Пусть Pi=Omega tensor |chi><chi|. На том же root x* весь путь

```text
rho_t=(1-t)P/128+t Pi/8, 0<=t<=1,
C_t=[sqrt(1+15t) Pi+sqrt(1-t)(P-Pi)]/sqrt(128)              (N14)
```

даёт exact joint critical preparations. Matter eigen-equation выполняется
на всём P, а field source аффинен по rho и равен нулю на обоих концах.
Reference остаётся128. C_t full rank и analytic при t<1; continuity
при t=1 достаточна, производная квадратного корня там не используется.

На одном фиксированном V=kerT/flat_field при x* истинный оператор равен

```text
H_t^V=(1-t)H_faithful^V+t H_pure^V.                       (N15)
```

И raw matter second jet, и signed-Q Schur contraction линейны по rho;
thermal/fullZ часть не меняется. kerT постоянен для faithful interior,
а equality с rank8 endpoint доказана source theorem. Source submersion
rank151 сохраняется на всём пути. Гиперболические151+/151- и signed Q
mass blocks поэтому не создают недосчитанных index changes.

Существующий [faithful result](FIELD_INVERSE_RESULTS.json) даёт на этом
V инерцию39464+/1342-/0; pure результат выше —33954+/6852-/0. Следовательно
net real spectral flow к отрицательной стороне равен5510, с учётом
multiplicity и возможных обратных переходов. Это не5510 различных t
или nonlinear branches. Determinant — polynomial, nonzero на концах,
поэтому множество singular t конечно и лежит внутри(0,1).

Уже q=(3,3,0,0) даёт самостоятельный строгий consumer. Старый
[full symbol](FULL_SYMBOL_Q3300.json) имеет quotient inertia12+/1-;
новый pure блок11+/2- получается из canonical q=(3,0,0,3) точной spatial
S3 congruence. Поэтому some t* in(0,1) имеет дополнительное ядро в
13-dimensional quotient. q3300 не входит в Omega-Omega: PX_vP=0.
Ненулевой v из этого ядра поднимается в полную joint linearization:

```text
delta C=0, delta epsilon=0,
delta Psi_Q=-R_Q X_v Psi_(t*).                            (N16)
```

P/Q orthogonality сохраняет normalization, все shell matter rows
E1(v)C=0, а reduced field rows равны H_t v=0. Пара q/-q даёт не менее
двух real normal nullvectors сверх flat family. Это не только frozen
field zero: все linearized preparation equations сохранены.

Нелинейное продолжение требует `E2 C+2E1 C1=0` и source-neutral M_v
condition из [rank-aware owner](../../A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md).
Существование linearized kernel само этого не даёт: даже функция
f(t,x)=t*x^2 имеет index change, но её полные stationary equations
вынуждают x=0. Floating location t~0.43036 и grade-four witness pairing
сохраняют диагностический статус до строгой локализации и bound.
Таким образом endpoint theorem прекращает nearby curved search при
этом pure seed, а interior theorem задаёт точный следующий consumer.

[Entrypoint](../../certificates/a4d_native_pure_field_check.py),
[validation](PURE_MEMORY_FIELD_VALIDATION.json) и
[full16 comparison](PURE_MEMORY_SYMBOL_RESULTS.json) сохраняют границу
между outward theorem и численной проверкой assembler. Старые root/
full-matrix suites и Lean builds не повторялись. Вывод или selection
исходного g/tau, physical preparation admission и ОТО остаются OPEN.
