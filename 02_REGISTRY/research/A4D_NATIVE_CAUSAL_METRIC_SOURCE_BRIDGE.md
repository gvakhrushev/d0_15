# Полный native источник: какая информация определяет Lorentz metric

16 октября 2026. Продолжение Draft #334 на `a1ca6f54`.
Потребитель: [fixed-time finite source limit](A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md)
→ intrinsic Einstein covector [coframe reconstruction](A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md).
Это тот же полный D0→ОТО маршрут; original fixed-g/tau/h^-2 terminal открыт.

**Новый результат.** На ВСЕХ24 connection directions continuum canonical
operator и полная объявленная H+J+R цена точно факторизуются через
positive metric G, coordinate torsion T, measure и тот же matter в форме
дифференциальных форм. При независимом observer остаются три локальные
Lorentz-cone directions, которых эта цена не различает. Предъявлен
периодический curved-cone контроль, включая Einstein source, и показано,
какое уже существующее native чтение различает его. Также конструктивно
решено обратное P1 observer-binding: на настоящем single full16 matter
chart оно восстанавливает g без потери десяти metric slots. Для actual
reference128 этот векторный readout ещё нельзя подставлять без отображения.

Это уточняет, какой native source ещё надо вывести, вместо попытки
переименовать R_G в R_g или бесконечно улучшать точность одного heat trace.

## 1. Входы и отличие от прежнего reflection control

[Full-Lorentz source](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md) фиксирует
forward raising operator, настоящий positive adjoint и все retained
reference/workspace terms одной conditional v8 цены. [Coframe heat bridge](A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md)
уже вычислил его general torsion a2 и связал +omega_LC с exterior d.
[Finite source theorem](A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md) теперь
контролирует spatial/record transition и independent raw covectors при
fixed positive beta. Следовательно, ниже исследуется источник ТОГО
оператора, а не новый удобный continuum ansatz.

[Lorentz reflection owner](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md), §§3–8,
уже доказал exact R_G/R_g identity с observer terms и curved g при flat G;
[complete source](A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md), §§2–3,
показал невидимость O-фактора для конкретной rest-record программы.
Ни один из этих прежних результатов не доказывал факторизацию всего
canonical heat/feedback/matter operator на arbitrary torsion. Именно
этот переход, его source consequence и граница P1 repair нужны здесь.
Прежние finite suites не воспроизводятся заново.

## 2. Точная факторизация на произвольной Lorentz-связи

Пусть `eta=diag(1,-1,-1,-1)`, e=F^-1, `g=e^T eta e`,
`n^T eta n=1`, `h_n=-eta+2(eta n)(eta n)^T`, `G=e^T h_n e`.
Исходные internal coefficients — raised exterior vectors. На всех16
grades введите не новый прибор, а точное изменение представления

```text
B_e=e^T eta, U_e=Lambda(B_e),
Gamma^lambda_(mu nu)=F^lambda_a(partial_mu e^a_nu+Omega^a_(b mu)e^b_nu),
T^lambda_(mu nu)=Gamma^lambda_(mu nu)-Gamma^lambda_(nu mu),
Q_T=sum_(lambda,mu<nu) T^lambda_(mu nu) C(dxmu)C(dxnu)I_(partiallambda).
```

Здесь Omega — произвольная metric-compatible Lorentz connection, не
necessarily Levi–Civita, flat или observer-parallel. Direct calculation:

```text
B_e (eta F_mu^T)=dxmu,
B_e Gamma(Omega_mu) B_e^-1+B_e(partial_mu B_e^-1)
                    =-Gamma_coord,mu^T,
U_e d_Omega U_e^-1=d_ext-Q_T.                             (1)
```

Во второй строке Gamma слева означает exterior infinitesimal lift;
справа та же covector connection, тоже поднятая на exterior algebra.
Последняя строка следует антисимметризацией covariant derivatives.
На k-form каждое из k мест даёт torsion contraction; это ровно Q_T,
без потери tensor16, trace, axial или какой-либо grade.

Это изометрия настоящих positive bundles, а не произвольное similarity,
после которого забывается adjoint:

```text
h_n^-1=eta h_n eta,
B_e^T G^-1 B_e=h_n.
```

Exterior compounds сохраняют равенство на ВСЕХ16 компонентах и с тем же
site measure mu. Поэтому для настоящего adjoint

```text
U_e D_Omega U_e^-1
  =(d_ext-Q_T)+(d_ext-Q_T)^(dagger_(G,mu)).                (2)
```

(2) зависит только от `(G,T,mu)`. В частности при T=0 это weighted
G-Hodge Dirac, независимо от Riemann tensor исходного Lorentz g.
Ни R_G, ни torsion terms не назначены вместо вычисленного оператора.

Ту же изометрию тензорно продолжим identity на reference/workspace и
положим `C_form=(U_e tensor I_aux)C_native`. Тогда ВСЕ traces, истинный
R, его нормировка и moving preparation source сохраняются. Отсюда

```text
S_cont=H+J+R=F_beta,M,z,C[G,T,mu,C_form].                  (3)
```

Field-independent divergent heat/workspace constants сохраняются, как
в finite-source owner. Утверждение (3) относится к объявленной цене;
не устанавливается факторизация всех contextual record observables,
controller/archive costs или ещё не связанного AF action.

## 3. Три Lorentz-cone directions при независимом observer

Положим `a=e^T eta n`. Из определений точно

```text
G=2a a^T-g,  a^T G^-1 a=1,
g=2a a^T-G.                                             (4)
```

При fixed positive G unit covector a имеет три локальные степени
свободы. Они меняют g, а не являются Lorentz frame gauge: g инвариантна
под исходной совместной Lorentz-сменой e,n. При fixed G
`delta g=2(delta a a^T+a delta a^T)`, `a^T G^-1 delta a=0`.

Для каждого такого g и arbitrary coordinate T существует единственная
metric-compatible connection с этим torsion: LC(g) плюс уже решённый
24-component contorsion map. Таким образом (G,T) не определяет a/g.
Measure dV_|g| также не помогает: `det g=-det G` во всём слое.

На гладких germs output map `(e,n,Omega,C_native)->(G,T,C_form)` имеет
локальный правый inverse: выбрать e для G, затем metric-compatible
connection из заданного T и `C_native=U_e^-1 C_form`. В Omega участвует
одна производная e; без этого уточнения не заявляется submersion одной
и той же Ck Banach norm. На smooth fields это полноценная local chart.

Следовательно, (3) и её полный source имеют нулевую pullback-компоненту
в этих трёх направлениях. Если существует critical point output
functional, его полный cone fibre даёт critical points continuum
матрицевой цены. Простая constancy на одном fibre сама по себе НЕ
доказывает criticality; существование такого point не объявляется.

## 4. Полный curved-cone контроль с тем же оператором и материей

Пусть theta=theta(y) гладкая периодическая функция. Возьмём `n=e0`,
`e=s O_01(theta)`, s>1 constant, где первая строка O есть
`(cos theta,sin theta,0,0)`. В исходный Lorentz slot подставим настоящий
`Omega=omega_LC(g)`, определённый из этого e. Тогда

```text
G=s^2 I, T=0,
g=s^2 [[cos(2theta), sin(2theta),0,0],
       [sin(2theta),-cos(2theta),0,0],
       [0,0,-1,0],[0,0,0,-1]], det g=-s^8.               (5)
```

В coordinate-form representation (2) — один и тот же flat scaled
Hodge Dirac для всех theta. Сохраним actual C_form, а не frozen native
components: `C_native(theta)=U_e(theta)^-1 C_form`. Тогда полная
H+J+R и ВСЕ её derivatives вдоль этой семьи постоянны. Matter не
заменена stress-остатком и ни одна из16/ancillary компонент не отброшена.

Но прямой Levi–Civita расчёт, в sphere-positive convention, даёт
(AB означает t,x block)

```text
Ric_yy=2(theta')^2,
Ric_AB=theta'' [[-sin(2theta),cos(2theta)],
               [cos(2theta),sin(2theta)]],
Ric_zz=0, R_g=-2(theta')^2/s^2,
Ein_yy=(theta')^2, Ein_zz=-(theta')^2,
Ein_AB=Ric_AB+(theta')^2 g_AB/s^2.                       (6)
```

Поэтому с периодическими/compact boundary conditions

```text
I_EH[g_theta]=-2s^2 integral (theta')^2,
dI_EH[delta theta]=4s^2 integral theta'' delta theta.     (7)
```

Например theta=epsilon cos(2pi y) даёт неплоскую periodic Lorentz
metric с ненулевым full Einstein source, а (3) остаётся theta-independent.
Это проверка источников, а не нулевого scalar action на null-wave ansatz.
Значит нет universal unrescaled source identity
`dS_cont=c dI_EH+dR_actual` с c!=0 на этой независимой-field области:
слева0, actual dR0, а (7) вообще ненулева. То же верно для любой
calibration, являющейся только функцией `(G,T,mu,C_form)` и тех же
spectral/blank data: она неизменна на данном fibre.

Семья не обязана лежать на границе matrix domain. Здесь `||c(u_r)||=1/s`.
На bounded smooth theta proper transports имеют norm `1+O(h)`, поэтому
для достаточно малого h оба local contractions строго меньше1 при
том же s>1. Calibrations не меняются, все proper links сохраняются.
Это matrix kinematics, не physical admission, full finite root или
uniform h^-2 source conclusion.

## 5. Конструктивное закрытие fibre через уже существующий P1 readout

Предыдущий контроль использует независимые n и C_native. На настоящем
single full16 real matter chart [существующее P1 чтение](A4D_NATIVE_MATTER_OBSERVER_PAIRING.md)
даёт более сильную связь, которую нельзя забывать или объявлять уже
доказанной для другой подготовки. Если из ТОЙ ЖЕ matter psi берутся

```text
v=F P1 psi, kappa=(P1 psi)^T eta(P1 psi)>0,
n=P1 psi/sqrt(kappa), alpha=P1(U_e psi)=g v,
```

то `a=alpha/sqrt(kappa)` и точно

```text
kappa=alpha^T G^-1 alpha,
g=-G+2alpha alpha^T/kappa.                              (8)
```

Таким образом при fixed G и fixed SAME form matter alpha Lorentz metric
уже определена. Никакого нового observer section, future orientation
или удаления других15 amplitudes для (8) не требуется. Нулевая/null/
spacelike first grade остаётся в исходном carrier, но вне этой chart.
Выбор P1 есть existing fixed-linear-readout hypothesis, а не универсальная
классификация всех nonlinear/native/reference-dependent readings.
Одна proper Lorentz covariance допускает также P3; ею P1 не выбран.

Полный joint differential, `u=G^-1 alpha`, равен

```text
delta kappa=2u^T delta alpha-u^T delta G u,
delta g=-delta G+2(delta alpha alpha^T+alpha delta alpha^T)/kappa
                          -2alpha alpha^T delta kappa/kappa^2. (9)
```

При fixed alpha десятислотовая metric map — invertible reflection
(involution). При fixed G `delta alpha->delta g` имеет rank3 и ровно
radial kernel `span(alpha)`. Три causal directions переходят в
настоящие matter tests, а не выбрасываются как gauge. Все grades,
normalizer и остальные matter equations остаются в полном source.

Это явный candidate common-field map для физического bridge. Однако
actual v8 preparation с reference128 — матрица amplitudes: P1 даёт
4×128 блок, а не выделенный4-вектор. Нельзя выбирать column, tracing
phase или reference contraction ради удобного observer. Для faithful
reduced density вообще нет preferred coherent amplitude vector.
Следующий native derivation должен дать actual retained readout,
его domain и полный derivative, а затем проверить именно (8)/(9)
или его собственный full-correlation аналог на том же процессе.
Наличие формулы P1 на single16 не выполняет этот переход за reference128.

### 5.1. Настоящий causal source уже имеющейся материи вычислен

При P1 binding нельзя сохранять C_form и одновременно вращать a.
Возьмём G=s^2 I, T=0 и actual one-form component

```text
alpha=s f(y)[cos(theta(y))dt+sin(theta(y))dx], f>0.
```

Другие12 amplitudes обозначим beta_k(x) в фиксированном orthonormal
`(s dx)^wedge k` basis и сохраним ВСЕ их вариации. Native inverse
`psi=U_e^-1 psi_form` даёт `P1 psi=f e0`; поэтому n=e0 выполняет
именно тот же P1 law, а не независимо предписанный observer.
Positive norm и полный Rayleigh term точно равны

```text
N=integral[f^2+sum|beta_k|^2],
R=integral[f'^2+f^2 theta'^2+sum|grad beta_k|^2]/(s^2 N),
dS[delta theta]=dR[delta theta]
   =-2 integral (f^2 theta')' delta theta/(s^2 N).          (10)
```

Heat и J постоянны, поскольку G,T не меняются. Это causal source
существующего R с настоящей normalization и всеми grades, не новая
AF цена и не stress, определённый разностью до Einstein tensor.
N не зависит от theta на ЭТОЙ кривой; при delta f или delta beta
его производная обязательно возвращается.

Полная source bookkeeping остаётся существенной. В independent
`(G,T,C_form)` coordinates подготовка имеет equation
`Delta_G C_form=R C_form`. Например f constant, theta=2pi m y и
любые другие grades в том же Laplace shell удовлетворяют этой
coordinate preparation equation. Это не утверждение raw matter EL
при fixed native e,Omega: P1-induced observer/moving-pairing terms
тоже входят по chain rule. Не проверены G/link equations, поэтому
такая winding state не объявляется joint root. Полный differential
потребляет и delta G, delta T, и delta C_form; (10) — его проверенный
pullback вдоль указанной physical-field кривой.

## 6. Уже существующий retained link readout видит этот дефект

[Complete field source](A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md),
§4, eq(10), содержит actual full16 observable

```text
I_boost=Tr16 Lambda(h_t^-1 A^T h_s A)-16
       =16(c_pair^2-1).                                 (11)
```

Owner прямо отличает его от зарегистрированной AF/H+J+R цены. Его
нельзя прибавлять как желаемый torsion/EH source. Но это точный вход,
показывающий, что missing information есть в retained comparison data.

Для (5), в точке theta(y0)=0, LC frame connection имеет
`Omega_x=theta' B02`, `Omega_t=-theta' J12`, `Omega_y=0`.
Вдоль x-edge y постоянно, поэтому настоящий proper transport равен
`A_x=exp(h theta' B02)`. При h_n=I

```text
c_pair=cosh(h theta'),
I_boost=16sinh^2(h theta'),
h^-2 I_boost ->16(theta')^2.                            (12)
```

Constant s не меняет spin connection. В отличие от continuum scalar
H+J+R, этот actual comparison readout различает curved cone и constant
cone. Его источник, коэффициент и полная история ещё должны получиться
из исходной record price. (12) НЕ доказывает EH matching: проверена
одна contraction/семья, не все tensor rows и не full action.

В частности, completed D-functional AF-price сама по себе не даёт
этого causal row. Если D-intertwiner реализован в том же AF block и
сохраняет central PF reference, соответствующие spectral/flagged prices
co-transform. Внешний U_e→AF map и его full-history source пока не
доказаны; нельзя переносить другое ненулевое AF source число на (5).

## 7. Что меняется в исходной h^-2 задаче и native calibration

Fibre blindness (3) — continuum/unrescaled source theorem. Он НЕ
исключает finite h^2 causal source, которое original terminal именно
усиливает h^-2. Actual proper-link stencil и record clock имеют
собственные subleading terms; fixed-beta raw o(1) theorem не даёт
права удалить их. С другой стороны, diagnostic h^-2 limit (12)
не выбирает native action и не доказывает stationary comparator.

### 7.1. Нужный finite coefficient определён с normalizer и clock

Для actual backward proper parallel transport в coordinate forms
`P_r(h)S_r=exp(h nabla_r)` на smooth core, где
`nabla_r=partial_r-Gamma_coord,r^T` с exterior lift. Поэтому

```text
d_h=d_ext+h L1+h^2 L2+O(h^3),
L1=(1/2)sum_r C(dx_r)nabla_r^2,
L2=(1/6)sum_r C(dx_r)nabla_r^3,
D1=L1+L1^dagger, D2=L2+L2^dagger,
Delta_h=Delta0+h A1+h^2 A2+...,
A1={D0,D1}, A2={D0,D2}+D1^2.                            (13)
```

В частности, конечные links для всего cone примера определены явно.
Пусть p=theta_y, Eab — elementary4x4 matrix, R01=E01-E10. В
coordinate covector slot

```text
M0=p[sin(2theta)E02-cos(2theta)E12+E21],
M1=p[-cos(2theta)E02-sin(2theta)E12-E20],
M2=p R01, M3=0.
```

Соответствующие coordinate transports равны
`Lambda exp(h M0(y))`, `Lambda exp(h M1(y))`,
`Lambda exp((theta(y+h)-theta(y))R01)`, I. Это conjugates настоящих
proper native LC links, не объявление I+hOmega точной Lorentz-матрицей.
В y-link сохраняется весь moving endpoint theta(y+h).

Adjoints берутся в ТОМ ЖЕ fixed G=s^2I, mu, включая все coefficient
shifts/derivatives. (13) — smooth-core expansion, а не уже uniform
heat/source remainder на всех mesh modes.

На конкретной cone family(5) `tr Gamma_coord,r=0` и
`(Gamma_coord,r)^r_r=0` для каждого r. Full16 CAR trace и even Fourier
weights дают `Tr f(Delta0) A1=0` для любой scalar spectral f:
terms с тремя momentum нечетны; оставшиеся two-momentum terms имеют
r≠a и зануляются symmetry либо diagonal coefficient, равный0.
Следовательно, формальный order-h вклад H и J здесь равен0.
Но A1 НЕ нулевой operator. При theta=0 его coefficient при partial_1^2
равен `2theta_y Gamma(B02)/s^2`. Действительно, M1=-pB02,
Gamma(B02) Hermitian и коммутирует с C1,I1. При scale1 first-derivative
часть D1 равна `-p Gamma(B02)gamma1 partial1`; её anticommutator
с gamma1 partial1 даёт +2p Gamma(B02) partial1^2. Поэтому A1
susceptibility в (14) нельзя выбросить по нулевому trace.
Произвольная matter rho не является full16 trace: `Tr rho A1`
не разрешается занулить тем же аргументом.

Обозначим E=exp(-beta Delta0), Z=Tr E, Fz=1-z+zE и
`kappa0(lambda)=-E/Z+Mz beta E/Fz`. Точное finite-cutoff second
Fréchet differentiation даёт кандидат order-h^2 coefficient
field-dependent H+J terms. Exact field-independent C_h и dimensional
J constants сохраняются отдельно, а не добавляются как counterterm:


```text
K2=Tr kappa0 A2
  +(1/2)sum_ij kappa0^[1](lambda_i,lambda_j)|A1_ij|^2
  -beta(Tr E A1)^2/(2Z^2).                              (14)
```

В divided difference Z фиксируется только внутри функции kappa0;
его настоящая производная есть последний член. При совпадающих
lambda используется kappa0'. На cone family последний член равен0
по доказанному trace identity, а не потому, что normalizer заморожен.
(14) следует из derivative exp по Duhamel и derivative log Z;
сходимость соответствующих polynomially weighted heat traces есть,
но uniform lattice/source expansion до этого порядка ещё требуется.

Native clock `alpha=c0 h^2`, `m alpha=beta` добавляет в этот coefficient

```text
K2_clock=(c0/2)Tr kappa0 Delta0^2
 =c0/2[-Tr Delta0^2 E/Z+Mz beta Tr Delta0^2 E/Fz].          (15)
```

Это следует из `B^m=E-(beta alpha/2)Delta0^2 E+O(alpha^2)` на том же
операторе. (15) theta-independent на cone fibre, но НЕ нулевой во
всех transverse metric rows. Для actual normalized matter
`rho_h=rho0+h rho1+h^2 rho2+...` дополнительно

```text
R1=Tr rho0 A1+Tr rho1 Delta0,
R2=Tr rho0 A2+Tr rho1 A1+Tr rho2 Delta0.                 (16)
```

В такой coefficient convention factorials уже включены в rho2,A2.
Все preparation jets и reference correlations должны быть actual.
Даже `Tr rho0 A1=0` для faithful full-shell density не доказывает
зануления каждого preparation Euler row этого порядка.

Для source, а не одного значения цены, на fixed-G cone нужно также
сохранять ordered jets `delta nabla_r=Gamma(delta M_r)`:

```text
delta L1=(1/2)sum C_r(delta nabla_r nabla_r+nabla_r delta nabla_r),
delta L2=(1/6)sum C_r(delta nabla_r nabla_r^2
             +nabla_r delta nabla_r nabla_r+nabla_r^2 delta nabla_r).
```

В true adjoints применяются те же jets. Для transverse metric tests
добавляются delta C_r, delta G/measure и moving adjoint terms, как в
full-source owner. Exact exponentials имеют ordered derivative integral,
y-link — `delta theta(y+h)-delta theta(y)`. Freezing endpoint неверно.
Перед переносом nonlinear preparation надо решить actual shell condition
`P A1 P C0=epsilon1 C0` и off-shell first amplitude equation. Даже
faithful trace zero не доказывает эту matrix equation. Если beta_h
отличается от beta на O(h^2), сохраняется также его source coefficient
через полное calibration unfolding; integer-clock derivative не выдумывается.

Таким образом ближайшая finite source задача теперь имеет явный
предмет: доказать C1 remainder o(h^2) для (13)–(16) в declared raw
norm на actual admitted branch и вычислить source K2+K2_clock+R2.
Нельзя заменить эту задачу одним smooth-core Taylor polynomial или
G-Hodge curvature coefficient. Link/observer/matter equations, original
fixed-source comparator и независимый physical coefficient сохраняются.

### 7.2. Calibration остаётся свойством того же процесса

У v8 alpha=p^2 h^2/128, m=2n и beta=m alpha выведены из данного
32-label/coefficient/golden-port circuit и его blank-event probability.
Выбор n(L)=128L^2, reference128, spectator apparatus и diagnostic z=2^-20
был входом experiment. После выбора reference/workspace их множители
`C=128*128^n`, `M=128` точны и не удаляются. Ни old chronology, ни
существующий golden gate не выводят z(h) или stationary `Mz=O(beta)`.
Moving calibration требует полного [source unfolding](A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md),
§3(7); integer m и changing workspace не имеют ordinary field derivative.

Итак, следующий consumer имеет конкретный тип: actual common native
observer/reference readout + complete comparison/history price должны
определить causal/source rows либо нужный finite h^2 coefficient при
сохранённых equations. Для этого доступны (8)/(9), actual matter source(10) и readout(11)/(12).
Нельзя завершить bridge одним переименованием positive Einstein source,
выбором z(h), новым action term или ещё одним старым root replay.

## Проверка

[Новый bounded packet](sources/d0_causal_cone_source_2026-10-16/)
содержит independent full16 Cartan/adjoint/Gram algebra, exact symbolic
curvature всех10 rows, P1 inverse/differential и boost readout controls.
Analytical factorization и source conclusion следуют из (1)–(12); (13)–(16) фиксируют следующий coefficient с явно указанной remainder obligation, а не
из finite sampling. Native physical admission, controlled nonflat joint
roots и original terminal этим не объявляются закрытыми.
