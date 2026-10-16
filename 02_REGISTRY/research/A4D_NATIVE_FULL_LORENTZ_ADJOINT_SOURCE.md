# Полный Lorentz-источник: прямой оператор, положительный возврат и баланс памяти

16 октября 2026. Продолжение [Draft #334](https://github.com/gvakhrushev/d0_15/pull/334),
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, вход `7883d390`.

**Результат.** Для фиксированного прямого creation/transport построено
явное local full-Lorentz field → matrix-instrument отображение с прежними
32 labels, coefficient qubit, golden port,128 outcomes/round, reference128
и исходной условной v8 scalar price. Вычислены поперечные boost sources.
Прежний faithful root остаётся стационарным в этом расширенном matrix
interface. В однородном классе rho=P_Omega/8 tensor sigma, sigma на E0,
stationary preparations задаются двумя точными occupation balances;
предъявлена чистая rank8 preparation на той же
геометрии. Actual прежний pure seed этим дополнительным Euler rows не
удовлетворяет. Это меняет вход следующей full-Lorentz задачи.

Физическое исполнение новых onsite matrix gates исходными D0 primitives,
вся native controller/archive price и её выбор остаются OPEN. Старый
literal stored Dirac, его bounded SO3 domain и все доказательства его
ядра сохранены. Здесь дана условная положительно-сопряжённая реализация
фиксированного forward channel; её native admission не выводится из
одного существования матриц или совпадения цен на меньшей области.

## 1. Почему прежнего Ward/rotation источника недостаточно

[Observer/holonomy owner](A4D_OBSERVER_HOLONOMY_CLOSURE_SYNTHESIS.md) уже
показал: два старых adjoint условия сохраняют timelike n вдоль каждого
stored edge. При прямом четырёхмерном Levi–Civita чтении и регулярном
smooth limit это ограничивает Ricci-flat сектор плоской геометрией.
Понижение ранга памяти не меняет эту область.

Нужное следующее звено — источник полного Lorentz-переноса. Используем
существующий [positive-adjoint interface](A4D_NATIVE_JOINT_ADJOINT_SOURCE.md)
и literal forward из [полного источника, §§0–0.3](A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md).
На полном H=ell²(sites) tensor Lambda(C4), со всеми16 grades, положим

```text
h_x=-eta+2 eta n_x n_x^T eta, n_x^T eta n_x=1,
G=direct_sum_x Lambda(h_x),
d=ell^-1 sum_r C(v_r(x))[Lambda(A_xy) shift_r-I], y=x+r,
d^sharp=G^-1 d* G, D_can=d+d^sharp.                         (1)
```

A_xy — proper time-oriented Lorentz matrix. Локальная компонента n
выбрана для гладкой карты, физическая стрела времени этим не выводится.
Условий parallel observer и own-leg transport в новой matrix domain нет.
Для фиксированного d,G оператор (1) единственен среди selfadjoint
операторов, имеющих только degree±1 и **тот же заданный raising part d**.
Согласие со старым оператором на меньшем domain само по себе такой
единственности не доказывает; произвольное продолжение цены не выбирается.

Для edge x←y

```text
A^sharp=h_y^-1 A^T h_x,
[C(v_x)Lambda(A)]^sharp
 =Lambda(A^sharp) i_(h_x v_x)
 =i_(h_y A^-1 v_x) Lambda(A^sharp).                        (2)
```

Старый inverse-return совпадает с (2), когда одновременно
E=A^T h_x A-h_y=0 и b=A^-1 v_x-v_y=0. Его transverse difference jet:

```text
delta(d^sharp-ell_stored)_edge
 =i_(h_y delta b)Lambda(A^-1)
  +i_(h_y v_y) Gamma(h_y^-1 delta E)Lambda(A^-1).           (3)
```

Поэтому одно own-leg условие не устраняет boost-source. (3) сохраняет
обе причины старой границы, а не меняет SO3 на SO4 внутри прежней карты.
Под совместным Lorentz gauge S_x имеем d'=U d U^-1,
G'=U^-* G U^-1, U=direct_sum Lambda(S_x); (1) преобразуется так же.

## 2. Локальный матричный прибор с теми же128 исходами

Whitening L_x=sqrt(h_x), I_x=Lambda(L_x) даёт

```text
u_r=L_x v_r, M_xy=L_x A_xy L_y^-1,
C_r=C(u_r), X_r(x)=C(u_r(x))Lambda(M_xy), P_r=X_r shift_r,
hat d=ell^-1 sum_r(P_r-C_r), hat D=hat d+hat d*.            (4)
```

Общий M не обязан быть unitary. Берём открытую область
`max_r,x(||C_r||,||X_r||)<=k<1`. Она содержит окрестность исходного
homogeneous root: там M=I и ||C_r||=sqrt(d)<1. k — оценка области,
не новая калибровка или coupling действия. Неограниченные boosts сюда
автоматически не включаются.

Для любого contraction X Julia matrix

```text
J(X)=[[X,sqrt(I-XX*)],[sqrt(I-X*X),-X*]]                   (5)
```

unitary; равенство X sqrt(I-X*X)=sqrt(I-XX*) X доказывается
functional calculus и не требует normal X. Если P=X shift, то

```text
J(P)=diag(I,shift*) J(X) diag(shift,I).                    (6)
```

Таким образом нужны только onsite16x16 defect roots и прежний bare
shift с coefficient qubit. Порядок coefficient/shift сохранён. Нужды
в global sqrt(Delta) или eigenstate catalogue для этой конструкции нет.

Возьмём для каждой из4 ролей четыре signed unitary words

```text
J(P_r), J(P_r)*, -J(C_r), -J(C_r)*,
```

и повторим каждый дважды. Это32 labels. Uniform preparation/SELECT/
unpreparation Q имеет blank label+coefficient compression

```text
A=<blank|Q|blank>=ell hat D/16,
W=Q*(I-2P_blank)Q,
K0=pI+p^2W, K1=sqrt(p)p(W-I), p+p^2=1,
B=P_blank K0 P_blank=I-2p^2 A*A
 =I-alpha hat D^2, alpha=p^2 ell^2/128.                    (7)
```

||ell hat D||<=16k, поэтому B>p^3 I. Labels32 × coefficient2 × port2
дают прежние128 outcomes; каждый complement остаётся. n rounds с n
fresh retained128-registers дают blank compression B^n, без reset старых
записей. С теми же workspace128^n, reference128 и tested identity action
на аппарате из [v8, §4](sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md)
получаем буквально ту же conditional scalar function:

```text
m=2n, beta=m alpha, Delta=hat D^2, F=(1-z)I+zB^m,
Z=Tr_H B^m, C=128*128^n, M_feedback=128,
S=log(C Z)/beta-M_feedback Tr_H log F+R,
R=Tr(w*Delta w)/N, w=I Psi, N=Tr(w*w).                    (8)
```

При рабочем L8 прежние n8192,z2^-20,ell=1/8 фиксированы. Все4096
thermal modes и16 Fock components входят в Z. Смена SELECT words
сохраняет (8), но не доказывает равенство всех contextual readouts,
controller execution costs или всей физической Cost−Info цены. Onsite
matrix defect roots шире прежних scalar BetaHat/ZetaHat: native generation
именно этих outcome-labelled gates остаётся конкретной missing arrow.

## 3. Настоящие jets и полный источник

При R_L=sqrt(I-XX*) derivative определяется Sylvester equation

```text
R_L delta R_L+delta R_L R_L=-(delta X X*+X delta X*),
R_L R_L,ij+R_L,ij R_L
 =-(X_ij X*+X_i X_j*+X_j X_i*+X X_ij*)
  -(R_L,i R_L,j+R_L,j R_L,i).                            (9)
```

Аналогично для right defect. R_L>=sqrt(1-k²) I, поэтому inverse
Sylvester norm<=1/(2sqrt(1-k²)); Dirac spectral gap не нужен. (9)
переносится на SELECT и все retained Kraus operations обычным product
rule. Output derivative имеет полный вид
`delta(K_a rho K_a*)=delta K_a rho K_a*+K_a delta rho K_a*+K_a rho delta K_a*`.
Томографическая инъективность и commutator-only law для rho не добавляются.

Moving observer и adjoint также дифференцируются:

```text
delta d^sharp=(delta d)^sharp+[d^sharp,G^-1 delta G],
delta u=delta L v+L delta v,
N_e=delta M M^-1
 =a_x+L_x(delta A A^-1)L_x^-1-M a_y M^-1,
a_x=delta L_x L_x^-1, {L_x,delta L_x}=delta h_x.            (10)
```

В mixed jet `{L,L_ij}=h_ij-{L_i,L_j}`; observer variations obey
`n^T eta n_i=0`, `n^T eta n_ij=-n_i^T eta n_j`. Не разрешается заменить
эти3 направления независимыми10 SPD coordinates или заморозить G.

При фиксированных calibrations полный scalar derivative (8) равен

```text
kappa(Delta)=-B^(m-1)/Z
 +M_feedback z beta F^-1 B^(m-1), rho=w w*/N,
E_D={hat D,kappa(Delta)+rho},
delta S=Tr(E_D delta hat D)
 +2 Re Tr[delta w*(Delta-R)w]/N,
delta hat D=delta hat d+delta hat d*, delta w=delta I Psi+I delta Psi.
                                                               (11)
```

Global normalizer Z движется вместе с Delta. (11) есть полная первая
вариация именно (8), включая самостоятельную matter variation. При
втором дифференцировании сохраняются delta Z, все divided differences,
`Delta_ij={D_i,D_j}+{D,D_ij}` и moving N.

Для edge x←y с N_e=delta M M^-1 положим
`Z_e=ell^-1 Lambda(M)(E_D)_(y x) C(u_x)`. Его link source:

```text
J_e(N_e)=2 Re Tr[Z_e Gamma(N_e)],
J_rotation(R)=Tr[(Z_e-Z_e*)Gamma(R)], R*=-R,
J_boost(B)=Tr[(Z_e+Z_e*)Gamma(B)], B*=B.                    (12)
```

Boost и rotation читают разные части covector. Старый skew/Ward row
не определяет (12) по boost. Полная Lorentz Ward identity следует при
совместных вариациях coframe, observer, matter и обоих концов A; ни один
из этих источников не назначается остатком до желаемого Einstein tensor.

## 4. Прежний faithful root сохраняется в новом matrix interface

На исходном homogeneous root A=I,n=e0,u_r=eta F_r^T,
F=(a-b)I+b11^T,a>b>0. Пусть t_r(k)=exp(2pi i k_r/L),
zeta_r=t_r-1, w_k=kappa_k+1_Omega(k)/128. Все eigenvalues Delta_k
скалярны на full16. Полные homogeneous coframe equations старого root
и invertible F дают

```text
M_rs=Re sum_k w_k zeta_r bar(zeta_s)=0.                   (13)
```

Действительно, coframe derivative равна
`32 L² sum_s M_rs u_s`; constant coframe variations принадлежат прежней
области. Ни rounded root, ни новый поиск здесь не используются.
Из (13) следует
`Re sum w_k t_r bar(zeta_s)=M_rs-M_ss/2=0`.
Full16 CAR trace сводит **каждый** новый Lorentz link source к этим же
нулевым моментам. Nonzero Fourier first sources равны нулю по translation
grading. Faithful purification удовлетворяет Delta Psi=epsilon Psi,
что зануляет все normalized matter rows. Observer rows через (10)
также равны нулю. Поэтому тот же faithful point есть exact joint root
(8) на новом full-Lorentz matrix domain. Его старые Hessian/kernel
классификации на дополнительные направления не распространяются.

## 5. Все E0 preparations: два уравнения вместо свободного источника

Пусть sigma>=0,Tr sigma=1 поддержана на **нативном**
E0=span{mask0,mask1,mask14,mask15}; полный carrier и все его вариации
остаются16. Здесь one-body occupations имеют вид
`N=diag(n0,ns,ns,ns)`, anomalous pairs и offdiagonal one-body ожидания
нулевые даже при произвольных complex coherences в E0.

Берём rho=P_Omega/8 tensor sigma. В прежних допустимых stored-domain
coframe/rotation направлениях первый источник прежний. Новые независимые
rotation directions также требуют своего source; ниже balance делает
его равным faithful. Новые12 boost rows при том же root равны

```text
x=n0-1/2, y=ns-1/2, T=sum_s u_s, lambda1=L²(2-sqrt(2)),
J_(r,0j)=lambda1/4 [u_r0(T_j-2u_rj)x
                         +u_rj(T_0-2u_r0)y].             (14)
```

Нормировка lambda1 здесь для L8. Общий L использует
`L²(2-2cos(2pi/L))`. Full CAR anticommutator Delta' действительно
квадратичен: quartic terms сокращаются, поэтому complex four-point
coherences не потеряны. Точные8 shell phases дают (14), а thermal и
feedback вклад фиксирован faithful cancellation (13).

Для spatial r=i,j!=i оба коэффициента (14) равны -b(a+b).
Поэтому J=0 требует x+y=0. Подстановка в time-role row даёт
`-(a-b)(a+3b)x=0`. При всех a>b>0 получаем точную эквивалентность

```text
все12 boost Euler rows равны0  <=>  n0=ns=1/2.              (15)
```

Это следствие уравнений (8), не добавленный selector. Для диагоналей
sigma оно означает p0=p15 и p1=p14; все PSD coherences сохраняются.
Для actual прежнего chi=(mask1+mask15)/sqrt2 имеем x=1/2,y=0.
В частности `J_(0,0j)=-lambda1 a(a+b)/8<0`: данный pure seed не является
root (8) на новом domain, хотя его старый stored-sector theorem верен.

Явный новый witness на той же геометрии:

```text
chi_bal=(mask0+mask1+mask14+mask15)/2,
rho_bal=P_Omega/8 tensor |chi_bal><chi_bal|.                (16)
```

Он удовлетворяет (15). E0 fixed under spatial SO3, а его first quadratic
sources совпадают с faithful, поэтому все field rows равны нулю;
Delta Psi=epsilon Psi сохраняет все preparation rows. (16) даёт exact
rank8 joint root выбранной matrix price с тем же reference128.
Не выводятся autonomous preparation law, engine-orbit stationarity,
старый rank151, inertia или nonlinear completeness у новой подготовки.

## 6. Проверка и следующий реальный переход

[Exact helper](sources/d0_full_lorentz_adjoint_2026-10-16/full_lorentz_boost_source_check.py)
проверил89 новых identities: full16 CAR source, все complex E0 compressions,
8 occupied phases,12 boost polynomials, iff(15), balanced witness и
nonroot hostile control. При F=I/4, fixed own-leg роли2, boost01 и
k=(0,0,2,0) получаем Delta'=8 Gamma(B01). Подготовка
(mask1+mask2)/sqrt2 даёт matter-source8; full heat/feedback trace source0.
Geometric inverse вместо positive adjoint даёт nonselfadjoint first jet.
Это exact nonroot control, не новый физический пример.

Normal/optimized [scientific JSON](sources/d0_full_lorentz_adjoint_2026-10-16/RESULTS.json)
побайтно совпали. [Validation](sources/d0_full_lorentz_adjoint_2026-10-16/VALIDATION.json)
фиксирует исходные definition hashes; старые root/spectral suites и Lean
не повторялись. Julia unitarity/local compiler и faithful stationarity
даны аналитически выше, отдельно от численных экспериментов.

Следующая missing arrow теперь конкретна: исходные допустимые native
generators, actual preparation и controller должны породить именно эти
onsite Julia gates/adjoints/outcomes с полной retained историей и ценой.
Нужны generator/adjoint/outcome/price diagrams; abstract programmability,
равенство blank survival и матричная допустимость их не заменяют.
Интерфейс и (14) задают источник, который такой native процесс должен
воспроизвести. Полный Einstein source, controlled refinement и исходный
fixed-smooth-g/fixed-tau/raw,l1 terminal задачи остаются OPEN.
