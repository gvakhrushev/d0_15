# Native matter clocks: один гладкий comparator и точное равенство метрик

2026-10-16. SOURCE #310. Явная кинематическая equality-family внутри полного
сырого frame/matter domain. Физический допуск wiring, preparation/controller
cost, выбор Info и исходные parent terminals остаются открытыми.

Здесь построена одна гладкая record-программа, у которой projector metric
тождественно равна фактической native CAR observer pairing на всей
пространственной окрестности. Равенство не назначается внешней метрике и
не получается из одного совпадения two-jets. Вместо этого retained rest
matter управляет реальным двенадцатиканальным comparator, а native поля
задаются на его equality-graph. Материя и moving frame не замораживаются.

Это comparator из [price/metric owner](A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md),
а **не** canonical AF gate W_E из [controlled spectral-price owner](A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md).
Их метрики и полные цены не отождествляются данным построением.

## 1. Явный вход и полный прибор

Используем p+p²=1, s=p³, полную exterior representation rho и actual
full-CAR current из [Lorentz source owner](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md).
В его retained reference/mask basis возьмём фактическое strict-timelike
состояние при параметре s_family=1:

```text
m*=-2 sqrt(p) p e_mask0+(2p-1)e_mask1+e_mask13+e_mask14,
N*=3, r(m*)=(-2/3,0,0), 1-|r(m*)|²=5/9.
```

В следующих формулах s всегда означает p³. Выбирается и сохраняется как
данное контроллера явное wiring lambda=1 всех16 вещественных rest-амплитуд:

```text
w_a=p²+(m0_a-m*_a),                 a=0,...,11,
X^A=m0_(12+A)-m*_(12+A),            A=0,...,3.       (1)
```

Обратная карта аффинна. Все16 компонент m0 свободны; нормировка N=m0^T m0
не заменяется константой. На достаточно малой открытой окрестности
сохраняются N>0, |r(m0)|<1 и 0<w_a<1/2.

Четыре X — материальные **скалярные** clocks, а не независимо назначенные
world-vector components. Используется ровно прежний упорядоченный k-frame
k_(ij,+/-)=e_i+/-e_j; новые направления не подбираются. На каждом канале

```text
theta_a=k_a.X,
J_a=(sqrt(1-w_a),sqrt(w_a) exp(i theta_a))^T,
W_a=[[sqrt(1-w_a),-sqrt(w_a)exp(-i theta_a)],
     [sqrt(w_a)exp(i theta_a),sqrt(1-w_a)]].          (2)
```

Прямая сумма W_a унитарна в C24. Двенадцать первых колонок дают изометрию
J:C12->C24 и P=JJ*. Оба исхода каждого канала сохранены. В частности
построен полный гладкий прибор, а не независимо предписанные generators
или second Taylor coefficients. Равенства mixed partials выполнены самой
формулой (2).

## 2. Метрика того же comparator

Полная endpoint-программа и её цена принадлежат предыдущему владельцу:

```text
C_yx=W_y*W_x,
F_xy=P0 C_yx*(I-P0)C_yx P0,
J_z(x,y)=-log det(I-z F_xy),
q=Hess_y J_z|diagonal/(24z)=Re Tr(dP dP)/24.         (3)
```

Последний след — полный counting trace данного comparator. Он не
подменяет PF trace, defining-block entropy или canonical AF record price.
Из буквальных колонок (2) на шестнадцатимерном target Z=(w12,X4)

```text
gamma=sum_a dw_a²/(48v_a)
         +(1/12)sum_a v_a(k_a.dX)², v_a=w_a(1-w_a),
q[Z]=Z*gamma.                                      (4)
```

Базовый гладкий germ задаётся без обратной метрической задачи:
`m0(x)=m*+sum_A x^A e_(12+A)`. Тогда w=p², X=x и q0=s I4/2.
В sufficiently small C2-окрестности DX обратима, q положительна и
гладкий прибор (2) определён. Все дальнейшие равенства относятся ко
всей этой окрестности actual fields, а не только к их значениям в нуле.

## 3. Feed-forward equality-graph и commutation одного прибора

Для любого такого m0 и любого гладкого O(x) в O(4) положим

```text
j=(1,r(m0)), H=-eta+2(eta j)(eta j)^T/(1-|r|²),
F=q[Z]^-1/2 O H^1/2,
m=rho(F)m0.                                        (5)
```

Все square roots — единственные положительные корни. Это частный случай
сырого chart из §8 Lorentz source owner. Он теперь применяется к метрике,
которую действительно породил прибор (2), а не к внешнему h_target.

**Доказательство commutation.** Из представления exterior algebra
`rho(F)^-1 m=m0`. Следовательно, record law, запущенный на том же native
входе `(F,m)`, сначала получает то же rest matter, затем по (1),(2) —
ровно тот же P. Его метрика равна q[Z]. Actual CAR covariance даёт

```text
J_native=Fj,
h_native=F^-T H F^-1=q[Z],
m^T W(F)m=m0^T m0.                                 (6)
```

Это точное тождество гладких функций. Поэтому совпадают все их
пространственные jets и все derivatives вдоль любых гладких семей этой
конструкции. Движутся rho, current, pairing, normalizer и matrix roots;
они не объявлены независимыми или замороженными.

Здесь отсутствует fixed point: m0 -> Z -> P,q -> F,m — явный feed-forward
порядок. Это параметризация совместных начальных данных, не предписание
reset после record transition. Эквивалентно, на всём raw domain record
law задан через `m0=rho(F)^-1m`; (5) явно параметризует его matching locus.

Он имеет16 m0-полей и6 O-полей. В raw chart `(h,m0,O)` из32 полей равенство
`h=q[Phi(m0)]` задаёт differential graph с10 matching equations. Поэтому
получено22-полевое семейство, а не весь32-полевой raw domain. Ни O(4), ни
ядра чтения не объявляются native gauge. При world-coordinate/frame
смене rest coefficients и X — scalar controls, а (4) трансформируется как
ковариантная метрика. Выбор wiring (1) в retained reference не является
доказанным Lorentz-gauge selector или вынужденным физическим readout.

## 4. Все десять metric tests внутри того же гладкого family

В target (4) положим T_mu=partial_mu Z. Векторы

```text
N_a=partial_(w_a)-T_mu q^(mu nu)gamma(T_nu,partial_(w_a))
```

образуют12 target-normal fields, поскольку DX обратима. Для нормального
eta, гладкого вдоль всего Z, metric compatibility даёт
`Dq[eta]_mu nu=-2gamma(B_mu nu,eta)`. B здесь относится к16-target (4),
а не к полному евклидову normal complement Herm(C24).

Для полной нормы удобнее не оценивать только коэффициенты в N_a.
Определим непосредственно16×16 оператор на **всём** eta=(eta_w,eta_X):

```text
F_Z eta=(gamma(T_mu,eta),
         -2gamma(B_mu nu,eta) in packed upper order,
         Dchi[eta]),
chi=(K^T K)^-1 K^T(v-s1).                            (7)
```

K — прежние matching-профили; никаких новых внутренних modes не вводится.
Consumer получает (7) из прежней24-coordinate coefficient definition
подстановкой `iota(delta w,delta X)=(delta w,k delta X)`. Вторая форма
вложения16-target в24-target ортогональна iota(eta), поэтому её вклад в
данный metric contraction нулевой; normality и chi также ограничиваются
буквальной подстановкой. Target geometry не заменяется другим pairing.
В базе для RHS `(a4,V10,b2)` его обратная равна

```text
eta_X=2a/s,
eta_w,a=[3k_a^T V k_a-Tr(V)+(Kb)_a]/s.              (8)
```

Metric row sum этого inverse равна максимум12/s, добавка Kb — максимум2/s,
а normality block — 2/s. Поэтому полная induced max-норма inverse равна
14/s. При `||F_Z-F0||_infinity<=s/28` Neumann bound даёт

```text
eta=F_Z^-1(0_4,V_packed,b),
D(q,chi) eta=(V,b), ||eta||_infinity<=28/s max(||V||,||b||).   (9)
```

Это оценка всей16-компонентной eta, следовательно и delta m0 при lambda=1,
в указанных Euclidean component max norms. Её нельзя без коэффициентов
переносить на физическую W-норму или refinement limit. Коэффициенты F_Z
зависят от Z,DZ,D2Z; Ck-оценки требуют соответствующих higher jets базы.
Компактность support test fields сохраняется.

Для гладкого eta настоящий конечный тест — Z_epsilon=Z+epsilon eta с
повторным вычислением (5). Равенство (6) сохраняется при каждом достаточно
малом epsilon. Никакой ODE по бесконечномерному inverse flow и никакая
Banach implicit-function theorem к оператору с derivative loss не применяются.
Тем самым реализуются все10 метрических test fields, но не утверждается
существование section для произвольной заранее заданной h(x).

Остальные8 phase-направлений исходного24-target лежат вне выбранной
clock-программы. Они не объявлены gauge или исчезнувшими equations всего D0.

## 5. Искривлённый control и literal native pairing

Пусть X=x, w_(01,+)=p²+kappa(x0)², остальные w=p², kappa=1/1000.
Это настоящий гладкий germ (1),(2), определённый на полной окрестности.
В нуле m0=m*, q0=sI/2, Dq=0 и

```text
partial_0²q=(kappa s/6)k_(01,+)k_(01,+)^T
              +(kappa²/(6s))e0 e0^T,
R_q(0)=-2kappa/(3s) != 0.                           (10)
```

Последнее следует непосредственно из scalar-curvature formula при
q0=cI,Dq=0: `R=c^-2[partial_mu partial_nu q_mu nu-Delta Tr q]`.
Это не замена curvature theorem численным rank witness.

В (7) perturbation от плоской базы — только entry
`(metric00,amplitude_(01,+))=-kappa/(12s)`. Она внутри s/28 tube;
consumer использует точный Sherman–Morrison inverse и проверяет полную
производную метрики. Если заморозить spatial clock jets нормального поля,
эта проверка отвергает полученный результат.

Для native equality не нужно собирать гигантский symbolic F. В whitened
координатах фактического m* положительный root H имеет блок
`[[3,2],[2,3]]/sqrt(5)` и два единичных направления. Буквальные определения
full CAR дают `current(B,rho(B)m*)=(sqrt(5)/3,0,0,0)` и native pairing I.
Обратное whitening даёт (6). Полный tangent check оставляет16 matter,
10 symmetric metric и6 skew O-jets; derivatives roots определены
Sylvester equation, а не замороженными eigenvectors.

## 6. Полный source на differential graph

Функциональная chain rule особенно важна, поскольку F зависит от Dm0.
Пусть полная независимо заданная native price уже проварьирована с
правильными normalizer, archive и boundary terms; обозначим её Euler
densities E_F,E_m. Иные retained поля имеют собственные слагаемые.
Для delta m=rho(F)delta m0+R_F[delta F], где
`R_F[delta F]=D rho_F[delta F]m0`, положим

```text
P_F=E_F+R_F* E_m,
E_q=F_q* P_F,
e_0=rho(F)* E_m+F_m0* P_F,
e_O=F_O* P_F.                                      (11)
```

Звёздочка здесь означает соответствующую cotangent pullback, а не
переименование native pairing. После подстановки (1),(5)

```text
delta S=<E_q,Dq[eta]>+<e_0,eta>+<e_O,delta O>
           + actual direct record/other-field terms.          (12)
```

Общий Euler на Z содержит **formal differential adjoint** Dq*, включая
spatial derivatives коэффициентов и E_q. Зависимость от Dm0 не теряется.
Для нормальных test-полей (9), Dq eta=V точно, и к metric source E_q
добавляется `W_Z* (e_0+e_record,direct)`. Internal b, O и остальные
retained sources также остаются. Boundary operator должен быть перенесён
целиком; компактные test fields устраняют его в этом локальном выводе.

Стационарность на22-полевом equality-graph не доказывает полного native
Euler system:10 поперечных matching-variations им не проверяются.
Даже достижимость всех metric V не разрешает выкинуть прямое matter
слагаемое в (12), другие link/shift equations или controller/archive cost.

## 7. Полученный результат и оставшийся допуск

Получена точная гладкая **comparator/native-pairing** commutation family
с конкретным readout wiring и искривлённым germ. Она не опирается на
произвольные заданные generator jets или внешний desired metric.
Это продвигает algebraic same-program вопрос дальше поточечного rank10.

AF canonical W_E имеет собственную state/isometry и метрику; предыдущая
спектральная цена его второго active record не стала ценой comparator (2).
Не доказаны ни равенство этих двух metric readings, ни price-preserving
native compiler между ними. Положительный matrix dilation сам этого не даёт.

В частности, для diagonal controls фактической AF isometry
`J_E=V0 sqrt(1-E)+V3 sqrt(E)` её counting-input metric равна
`q_E=Tr[(E(1-E))^-1 dE tensor dE]/(4d)`. На rank-one shape обе величины
e2 и det нулевые: E_eff постоянна, q_E=0, хотя graph-return
`U=diag(exp(i x_mu))` имеет q_U=p³I4/4. Метрики одного оператора нельзя
переносить на другой только по совпадению scalar effect. Полная auxiliary
exterior carrier из [determinant compiler](A4D_GOLDEN_DETERMINANT_COMPILER.md)
имеет256 мод и не является нынешним native четырёхкопийным AF module.
Prepared polar intertwiner зависит от полей; он сам не сохраняет actual
coarse-left density и [second-active price](A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md).

Есть и явная multiplicity/cost граница полного compiler-программы. При
`A=counts(n)_0,B=counts(n)_1`, n>=1, нынешний working H_(n+3) имеет
old-right multiplicities `(13A+8B,8A+5B)<=(21A,21B)`. Полный256-mode
auxiliary carrier вместе со всем старым input требует `(256A,256B)`,
поэтому целиком в этот module не помещается. На regular H_(n+k) требуется
`counts(n+2k)_j>=256 counts(n)_j` для обоих блоков. Минимально k=6:
при k<=5 оба отношения не больше144, а при k=6 не меньше305, используя
`3/2<=A/B<=2` и Fibonacci recurrence. Полная первая operator-price при
том же canonical PF seed и pure auxiliary тогда равна12, вместо6
нынешнего трёхшагового record. Prepared-column polar factorization не
обходит это условие на полный carrier и не доказывает сохранение цены.

Физическая граница wiring имеет уже конкретный engine-control:
[AF/CAR role-orbit owner](A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md)
показывает, что inherited level1 M2-image пересекает named engine support
лишь по identity-line с нулевой first-grade pairing. Активированная
каноническая подготовка согласует AF/engine transitions четыре шага и
различается на пятом. Поэтому открытое вещественное16-полевое family (1)
не объявляется engine-admitted continuum. Это scoped interface boundary,
а не запрет других подготовок.

Не выведены выбор wiring (1), его primitive admission, физический смысл
четырёх clocks, complete controller/preparation/archive price, volume law,
выбор native Info или on-shell transverse equations. Native dynamics не
обязана сохранять matching graph без отдельного доказательства. Граница
Lorentz action остаётся точной формулой observer-derivative owner; observer
kinetics нельзя удалить этим связыванием. Физическая ОТО и parent остаются
открытыми.
Формулы задают семейство полных унитарных приборов, параметризованное
полевыми амплитудами. Они не доказывают существование фиксированного
линейного quantum channel, считывающего неизвестные амплитуды m0.

[Узкий consumer](sources/d0_native_preparation_stationary_2026-10-16/matter_clock_binding.py)
импортирует pin-ированные k/metric/current definitions, не их старые suites.
Он не пишет JSON/receipt, не запускает Lean и не делает новых публичных claims.
В объединённом новом consumer эта часть проходит80 точных условий, соседняя
задача подготовки —42; весь122-условный вывод обычного и оптимизированного
Python совпадает побайтно. Общие smooth/source-доказательства проверены
независимо; конечные controls не заменяют эти доказательства.
