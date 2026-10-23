# Конечная запись → непрерывный heat/source: настоящий variable-field оператор

16 октября 2026. Потребитель: §6 [coframe/source bridge](A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md)
и [полная положительно-сопряжённая цена](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md).
Исходные определения: `17f6f3dc`, принятые здесь через `bb6a704d`.
Работа относится к тому же Draft #334 и исходной задаче; новый action,
физический heat-law, выбранный running coupling или claim не вводится.

**Результат.** Ошибка конечного числа записей оценена для полной H+J+R
цены и её первых источников на том же конечном операторе. Для гладкой
равномерно невырожденной семьи настоящего full16 stencil доказан
fixed-positive-time переход сетки к continuum heat и всем независимым
coframe/link/observer источникам. Норма источника — сильная L1 плотностей,
эквивалентная unweighted raw sum сеточных Euler rows; вариации coframe
и observer могут быть произвольными по вершинам. Это не исходный
`h^-2` comparator theorem и не равномерный short-time a2/a4 предел.

## 1. Общий carrier и точные гипотезы

Тор `T^4=(R/Z)^4`, `h=1/L`, все L^4 вершин, полный `Lambda R^4` размерности16.
Сеточная норма `||psi||_h^2=h^4 sum_x |psi(x)|^2`. Переход от counting
нормы к этой норме — постоянная изометрия, не замена trace или цены.
Все Nyquist modes сохраняются. Reference и retained workspace не
удаляются из matter; тепловой trace ниже — ровно прежний полный trace
на `H_h`, не только shell или одна grade.

После действительной observer-whitening `I_x` исходного forward:

```text
d_h=sum_r c(u_r(x)) [M_(h,r)(x) S_(h,r)-1]/h,
D_h=d_h+d_h*, Delta_h=D_h^2,
u_r=L(n) eta F_r^T, M_(h,r)=I_x Lambda(A_(x,x+hr)) I_(x+hr)^-1.    (1)
```

Звёздочка — настоящее Hilbert adjoint, включая сдвиг коэффициентов.
Не geometric inverse link и не independently chosen Hodge operator.
Исходные `A` — proper Lorentz links; `M` после whitening вообще не
orthogonal. Существующий conditional matrix instrument реализует (1);
физическая генерация этого инструмента остаётся отдельным обязательством.

Контролируемая семья удовлетворяет следующим явным условиям:

* `u_r` и continuum zero-order coefficient гладкие с равномерными C6
  bounds; real matrix `U=(u_ra)` имеет `s_min(U)>=sigma>0`.
  Исходный observer остаётся в одном controlled compact timelike chart:
  n, L(n), L(n)^-1, их нужные spatial derivatives и tangent maps
  равномерно bounded. То же требуется от coordinate lift F и link chart.
  Иначе bounded u можно получить компенсацией неограниченного boost,
  а source constants для original delta F и xi не будут uniform.
* `M_(h,r)=1+h Omega_r^+ + h^2 R_(h,r)`, с равномерными C6 bounds
  коэффициентов и remainder. В частности `||(M-1)/h||<=B`.
  Whitening сохраняет inhomogeneous connection term. Одной bounded
  Lorentz domain или произвольного `M=1+O(h)` без selected first jet
  недостаточно для названного continuum limit.
* Link variation определяется физическим tangent `delta A=h xi A`,
  `xi(x) in so(1,3)`; его transported first jet имеет ту же uniform
  consistency. Coframe и observer — независимые поля. Результат не
  объявляет их всеми admissible variations старого own-leg stored chart.
* В clock-оценке `alpha=beta/m`, `m>=2`, `B_h=1-alpha Delta_h>=b0>0`,
  `0<z<1`, `M>0`; calibrations фиксированы ВНУТРИ каждой field variation.
  Для actual native schedule дополнительно `alpha=c0 h^2`.

C6 — достаточная техническая регулярность доказательства ниже, не
заявление о её необходимости. Семья может быть компактной; константы
зависят только от перечисленных bounds, sigma и положительного beta.
Гипотезы не доказывают joint stationarity или physical admission.

## 2. Clock error на том же Delta: normalizer и все source rows

Пишем `K=B^m`, `E=exp(-beta Delta)`, `P=B^(m-1)`, `a=1-z`,
`F_K=a+zK`, `F_E=a+zE`, `Z_K=Tr K`, `Z_E=Tr E`. Не коммутируя
`delta Delta` с Delta, цикличность конечного trace даёт ТОЧНО:

```text
d Tr K=-beta Tr(P delta Delta),
dH_K=-Tr(P delta Delta)/Z_K,
dJ_K=Mz beta Tr(P F_K^-1 delta Delta),
H_K=beta^-1 log(C Z_K), J_K=-M Tr log F_K.                     (2)
```

Для heat-цены заменить P на E и K на E. Тот же нормированный
`R=Tr(Cprep* Delta Cprep)/Tr(Cprep* Cprep)` и ВСЕ его field/preparation
производные сокращаются в разности clock-цен точно; R не заморожен.

Для `t=beta lambda`, `b=1-t/m>=b0` имеем

```text
0<=e^-t-b^m <= t^2 e^-t/(2m b0),
|b^(m-1)-e^-t| <= e^-t/m [t/b0+t^2/(2b0^2)].                 (3)
```

Доказательство: `-log(1-x)-x<=x^2/[2(1-x)]`, `x=t/m`;
разложить `b^(m-1)-e^-t=(b^m-e^-t)/b+e^-t(1/b-1)`.
Формула — scalar spectral bound, а не ложная operator derivative rule.
Введём полные moments

```text
M_j(s)=Tr Delta^j exp(-s Delta),
W_j(s)=Tr (1+Delta) Delta^j exp(-s Delta).
```

Если для всякого real spectral f выполнено
`|Tr f(Delta) delta Delta|<=L_delta Tr(1+Delta)|f(Delta)|`, то

```text
0<=delta Z=Z_E-Z_K<=beta^2 M_2(beta)/(2m b0),
0<=H_E-H_K<=delta Z/(beta Z_K),
0<=J_K-J_E<=Mz delta Z/a,

|dH_K-dH_E| <= L_delta/(m Z_K) [
 beta W_1/b0+beta^2 W_2/(2b0^2)
 +beta^2 M_2 W_0/(2b0 Z_E)],

|dJ_K-dJ_E| <= L_delta Mz beta/m [
 beta W_1/(b0 a)+beta^2 W_2/(2b0^2 a^2)].                    (4)
```

Все moments в (4) при beta. Последний член dH — движущийся глобальный
normalizer; его нельзя удалить, даже если исходное состояние однородно.
Для dJ используется exact identity
`P/F_K-E/F_E=(P-E)/F_K+zE(E-K)/(F_K F_E)` и `E<=1`.
Если `epsilon0=beta^2 M_2/(2m b0 Z_E)<1`, то
`Z_K>=(1-epsilon0)Z_E`; иначе сохраняется настоящий положительный Z_K.
Размерность trace и размер retained price не спрятаны в константе.

## 3. Uniform Gårding на ВСЁМ lattice carrier

Пусть `nabla_r^+=(S_r-1)/h`, `T_a=sum_r u_ra nabla_r^+`,
`d_0=sum_a C_a T_a`, `D_0=d_0+d_0*` и `G(psi)^2=sum_r||nabla_r^+psi||^2`.
Full CAR, без предположения о коммутировании T, даёт

```text
D_0^2=sum_a T_a* T_a
 +sum_ab C_a I_b [T_a,T_b*]
 +sum_(a<b) C_a C_b [T_a,T_b]
 +sum_(a<b) I_a I_b [T_a*,T_b*].                            (5)
```

В частности `sum_a||T_a psi||^2>=sigma^2 G(psi)^2` pointwise в x.
Это сохраняет все высокие частоты, а не freezing principal symbol.

Поясним uniform first-order commutator bound. Для `P_a^eps=sum_r u_ra
nabla_r^eps` произведение двух difference operators оставляет
коэффициенты вида `u_ar (S_r u_bs)-u_bs(S_s u_ar)`; commutative
second-order principal часть сокращается, остальные имеют factor h.
Их `h nabla_r nabla_s` norm контролируется `2||nabla_s||`.
Настоящий adjoint имеет добавку

```text
T_a*=-P_a^- -B_a,
B_a=sum_r (nabla_r^- u_ra) S_-r.
```

Коммутаторы `[P,B]` остаются bounded: difference B требует вторую
производную u, а `h nabla` bounded. Пусть
`K_j=max_(r,a,|gamma|=j)||partial^gamma u_ra||_infty`, j=0,1,2.
Для каждого из трёх видов commutator в (5) достаточно

```text
||comm psi|| <= Lc G(psi)+Mc||psi||,
Lc=48 K0 K1, Mc=96(K0 K2+K1^2).
```

В (5) 16+6+6=28 CAR terms, каждый creation/contraction имеет norm1.
Young inequality и `||D_h-D_0||<=8kB`, `k=max|u_r|`, дают

```text
||D_h psi||^2 >= (sigma^2/4) G(psi)^2-C||psi||^2,
C=Cbase/2+(8kB)^2,
Cbase=28Mc+(28Lc)^2/(2sigma^2).                            (6)
```

Константы намеренно неграничные; они независимы от h и от количества
вершин. В частности d_h и d_h* bounded из graph `sqrt(1+Delta_h)` в H_h.
Это следует также прямо из (1), `T_a*` выше и (6).

Через minmax (6) и full16 Fourier Laplacian:

```text
N_h(E)<=C'(1+E)^2,
Tr exp(-t Delta_h)<=C'' exp(Ct)(1+t^-2),
Tr Delta_h^j exp(-t Delta_h)
 <=[2j/(e t)]^j Tr exp(-t Delta_h/2), j>=1.                (7)
```

На Brillouin cube `4h^-2 sum sin^2(pi h k_r)>=16|k|^2`.
Ни Weyl law, ни continuum heat expansion не используются для (7).

## 4. Почему source bound допускает негладкие вариации

В фиксированном whitened Hilbert space положим
`V=I delta d_original I^-1`, `Kobs=delta I I^-1`. ТОЧНО

```text
delta D=V+V*+[Kobs,d]+[Kobs,d]*,
Tr f(Delta) delta Delta=2 Re Tr D f(Delta) delta D.          (8)
```

`eta_delta=||delta F||_infty+||xi||_infty+||delta n||_infty`.
Из (1),(6) для настоящего V получаем
`||V(1+Delta)^-1/2||<=C_V eta_delta`, без derivative delta F.
Также `||Kobs||<=C_K eta_delta`, по smooth local square-root/exterior map.
Не утверждается graph bound для полного `[Kobs,d]`: производная rough
observer может быть сколь угодно велика. Вместо этого цикличность даёт

```text
Tr Df[Kobs,d]=Tr Kobs(d Df-Df d),
|Tr f delta Delta|<=4 eta_delta
 [C_V+C_K(C_d+C_dstar)] Tr(1+Delta)|f|.                    (9)
```

Для доказательства `||d Df||_1<=C_d Tr sqrt(1+Delta)|D||f|`
и аналогично для d*, а `sqrt(1+Delta)|D|<=1+Delta`.
(9) верно и для sign-changing f и некоммутирующих вариаций.
Здесь нет производных ни delta F, ни delta n. Для original unscaled
link tangent вместо xi norm в eta входит `h^-1||delta A||`.

## 5. Spatial norm-resolvent: настоящее finite-difference доказательство

Пусть J_h — точная Fourier изометрия H_h в trigonometric subspace
L2(T4;C16), на всём half-open Brillouin cube, и P_h=J_h J_h*.
Её adjoint `J_h* phi` — sampling **P_h phi**, не unrestricted sampling.
Для latter alias error `||S_h phi-J_h*phi||_h<=C_s h^s||phi||_Hs`, s>2.
Так как `||D_h||<=C/h`, alias не нарушает следующий core bound:

```text
D=sum_r [c(u_r)partial_r-partial_r i(u_r)]
       +sum_r [c(u_r)Omega_r^+ +Omega_r^{+*}i(u_r)],
||D_h J_h*phi-J_h* Dphi||_h<=Ch||phi||_H5.                 (10)
```

(10) получается Taylor remainder second differences и exact shifted
adjoint coefficients; C6/transport bounds §1 обеспечивают uniform
sampling bounds. Continuum D — selfadjoint elliptic closure на H1:
его principal Clifford symbol имеет norm |U^T k|, нижние коэффициенты
именно limit (1), а не выбраны по желаемому curvature source.

Покажем operator-norm convergence при z=+i и -i. (6) и
`|2pi k|<=(pi/2)|(exp(2pi i h k)-1)/h|` дают uniform H1 graph
для embedded resolvent. Пусть Fourier cutoff Q_N имеет |k|<=N.
Elliptic regularity `||(D-z)^-1 Q_N f||_H5<=C N^4||f||` и (10)
дают low-input resolvent error `ChN^4+Ch`. Input tail обоих resolvents
ограничен `C/N`: для этого применить H1 bound к ADJOINT resolvent,
затем взять adjoint. При `N~h^-1/5` получаем

```text
||J_h(D_h-z)^-1 J_h*-(D-z)^-1||<=C h^(1/5).                (11)
```

Nyquist modes не выброшены из оператора: Q_N используется только в
оценке. Внешнее zero extension finite resolvent сравнивается с compact
continuum resolvent. Rate достаточен для spectral convergence, не
выдаётся за sharp. Для вариаций не требуется дифференцировать (11).

Проверка альтернативы по литературе: Mikami–Nakamura–Tadano,
[Theorem2.5](https://arxiv.org/pdf/2307.08894), доказывает related
norm-resolvent limit для variable-coefficient scalar divergence stencil.
Он не импортируется как theorem для нашего matrix16/torus/true-adjoint
operator; (5)–(11) дают нужное отдельное сопоставление.

## 6. Fixed beta: полные источники сходятся в сильной raw sum норме

Из (7),(11) получаем при каждом фиксированном beta>0

```text
Z_h=Tr exp(-beta Delta_h) -> Z=Tr exp(-beta D^2)>0.          (12)
```

Не выводим derivative convergence только из сходимости значений.
Нужны реальные source densities. На любом конечном D-spectral block
(11) даёт согласованные orthonormal bases, включая multiplicities.
Если `Dpsi=nu psi`, соответствующий сеточный vector имеет
`(D_h-nu)psi_h->0`, `J_h psi_h->psi`. Применим (6) к
`psi_h-J_h*psi`, а затем (10). Получаем сильную H1 сходимость,
включая все difference derivatives. При degeneracy работают целые
spectral projections; вращение basis внутри блока не меняет сумму.

Теперь в trace-source (8) перенесём adjoint с variation. Для V
каждый coframe/link row — сумма произведений `D_h psi_h`,
`nabla_h psi_h`, `M_h S_h psi_h`, `psi_h` и гладких background matrices.
Для observer после cyclic transfer в (9) остаются только произведения
`psi_h`, `d_h psi_h`, `d_h* psi_h`, умноженные на Kobs.
Ни derivative rough variation, ни derivative heat kernel не требуется.
Strong L2 convergence каждого фактора даёт strong L1 convergence этих
плотностей. Piecewise-constant reconstruction согласована с Fourier:
сравнение со smooth sampled limit и exact grid L2 norm переносит
strong convergence даже для difference derivatives.

Остаток за finite spectral cutoff контролируется UNIFORMLY во всех
site variations с `eta_delta<=1`, по (9) и (7):
`Tr_(Delta>R)(1+Delta)exp(-beta Delta)->0` при R->infty,
равномерно по h. Low blocks плюс этот tail доказывают сильную L1
сходимость источников Z, H и J. Для J его spectral source weight
`Mz beta E/(1-z+zE)` bounded постоянной times E, поэтому series не
нужен. Z bounded away from0 делает moving normalizer непрерывным.

Точная норма: если `dS_h=sum_(x,a) E_(h,a)(x) delta q_a(x)`, то
`j_(h,a)=E_(h,a)/h^4` на cell x. Для smooth continuum source j:

```text
sum_(x,a)|E_(h,a)(x)-h^4 j_a(x)| -> 0.                    (13)
```

Это эквивалентно L1(piecewise constant j_h-j) с исчезающей sampling
ошибкой; сумма по components — packed, off-diagonal conventions
фиксируются выбранным field chart. В частности bounded smooth
coframe lift `delta e=(1/2)e g^-1 delta g` переносит (13) на ВСЕ10
независимых metric slots при фиксированной независимой connection.
Нельзя переносить его автоматически на forbidden stored directions
или на LC pullback: `delta omega_LC[e]` содержит derivatives delta e.

Для finite-record source при native `alpha=c0 h^2`, fixed beta,
`m=beta/(c0 h^2)` (или integer schedule beta_h->beta>0), (4),(7),(12)
дают O(1/m) raw-source clock error. В сумме с (13) это actual
finite-B → continuum first-source theorem на контролируемой семье.
Оценка spatial error o(1) не превращается в o(h^2); исходный
`h^-2` response/comparator terminal по-прежнему не следует.

## 7. Matter, field-independent constants и short-time boundary

R не удалён из полной цены. Clock difference (2)–(4) сохраняет его
ТОЧНО. Для arbitrary spatial preparation нельзя вывести R-source
convergence только из thermal estimates. Достаточно common isometric
embedding всех reference/workspace spaces, `||C||_HS>0` и strong graph
convergence ОБОИХ C_h и D_h C_h: нужны C_h, nabla_h C_h, D_h C_h,
nabla_h(D_h C_h), Delta_h C_h в соответствующих Hilbert–Schmidt L2
нормах. Тогда R_h, его field-source densities и amplitude source
`2(Delta_h-R_h)C_h/||C_h||^2` сходятся. Второй graph condition нужен
уже field-source: перенос adjoint variation даёт derivative D_h C_h.
Observer содержит также moving-preparation term
`2 Re <Kobs C_h,(Delta_h-R_h)C_h>/||C_h||^2`; он сохраняется.
Это sufficient criterion, не новый закон подготовки.

### 7.1. На настоящей joint-critical последовательности matter компактна

Для exact full-amplitude critical sequence дополнительную graph
гипотезу можно ВЫВЕСТИ, без фиксации matter rank и без компактности
огромного ancillary amplitude. Условия: все hypotheses §1, fixed
beta_h->beta>0, native alpha=c0 h^2 (m_h->infty), общие fixed M,z,
genuine coframe-dilation equation и
полная preparation stationarity. Последняя даёт ровно

```text
Delta_h Cprep_h=R_h Cprep_h,
rho_h=Tr_aux(Cprep_h Cprep_h*)/||Cprep_h||^2,
rho_h>=0, Tr rho_h=1, (Delta_h-R_h)rho_h=0.                (15)
```

Partial trace здесь точен для D-observables, действующих тождественно
на retained auxiliary spaces. Он не выкидывает reference/workspace,
не доказывает physical equivalence иных archive observables и не
заменяет actual preparation новым состоянием.

Полная coframe dilation с неизменными calibrations уже даёт

```text
0=-(Tr Delta_h B_h^(m-1))/Z_K
   +Mz beta Tr(Delta_h B_h^(m-1) F_K^-1)+R_h.
```

Все terms после первого неотрицательны. При B>=b0 и fixed beta,
(7),(12),(4) обеспечивают

```text
0<=R_h<=Tr Delta_h B_h^(m-1)/Z_K<=R_*<infty.               (16)
```

Таким образом rho_h лежит в РАВНОМЕРНО конечномерном spectral window.
Выбрать cutoff выше R_* вне spectrum continuum D^2; (11) согласует
его finite blocks. Trace-one positive matrices в этом общем конечном
блоке компактны. По подпоследовательности `rho_h->rho` в trace norm,
`R_h->R`, и `rho>=0`, `Tr rho=1`, `(D^2-R)rho=0`.
Rank rho может измениться; никаких grades или off-diagonal coherences
в ±sqrt(R) eigenspaces не удаляется.

В D-eigenbasis полный matter matrix равен
`Q^m_ij=(nu_i+nu_j)rho_ij`. В частности [D,rho]=0 НЕ требуется:
coherences между +sqrt(R) и -sqrt(R) сохраняются. Его coframe density
есть `2 Re sum_ij Q^m_ij phi_j* c_a B_r phi_i`; observer density после
cyclic transfer использует те же phi, dphi и d*phi.

На finite block D_h и Delta_h uniformly bounded; Gårding и (10)
дают strong graph convergence как basis vectors, так и D_h basis
vectors. Поэтому полный matter covector `{D_h,rho_h}` имеет strong
L1 field-source limit тем же product proof. Moving observer amplitude
term выше равен ТОЧНО0 в силу (15). Следовательно, на такой
joint-critical подпоследовательности **ВСЕ H+J+R field sources** сходятся
в raw sum норме (13), с actual matter rho. Нулевые finite Euler rows
переходят в нулевые independent continuum rows этой же heat/feedback/
Rayleigh цены. Этим не доказываются существование такой controlled
неплоской последовательности, выбор rho нативным процессом или
Einstein identity. Компактность purification/ancillary history не
утверждается и не нужна для данного field-source consumer.

C_h в `log(C_h Z_h)` и `-M dim(H_h) log(1-z)` могут расти с L.
Они field independent при фиксированных calibrations. Доказывается
сходимость field sources; сходимость самих невычтенных price values
не заявляется. При clock/record/calibration variations их производные
надо вернуть. Новый physical counterterm этим замечанием не вводится.

Для small beta (7) вместе с ранее доказанным `Z>=c beta^-2` в
нативном resolved window даёт из (4) sufficient errors

```text
||dH_K-dH_E|| <= C/(m beta),
||dJ_K-dJ_E|| <= C Mz/(m beta^2).                           (14)
```

Если лишь проверяется mathematically controlled schedule `Mz=O(beta)`,
для разрешения O(1) A2-source достаточно `m beta->infty`, а O(beta)
A4-source — `m beta^2->infty`. Это необходимые для ЭТОЙ достаточной
clock-оценки separation conditions, не derived physical calibration.
При `alpha=c0 h^2` последнее требует `h=o(beta^(3/2))`.
Spatial small-time source error этим не оценён; фиксированный positive
Mz уже встречает независимое scale obstruction прежнего owner.

Существующий `HeatA2LimitInterchange.lean` принимает bounded remainder
при всех 0<t<=t0 для каждого fixed N. Literal finite heat trace при
fixed N стремится к dim H_N, поэтому такая expansion с ненулевым
`a0_N/t^2` невозможна. Это корректный conditional Lean theorem,
не применимый без нового two-scale window или последовательных limits.
Новый fixed-beta theorem не использует эту невыполнимую подстановку.
Для feedback short-time series надо разделять `r beta<=t0` и tail;
нельзя распространять локальную expansion на все r.

## 8. Потребление и граница результата

Снят прежний общий пробел «даже fixed-positive-time finite-B и первые
variable-field источники не связаны с continuum». Теперь оператор
(1) с настоящим adjoint имеет доказанный bridge (3)–(13), включая raw
coframe/observer rows. Это даёт строго определённый continuum H+J
source для следующего сравнения с Einstein, вместо формального a2 fit.

Остаются: physical generation/полная retained цена; actual matter
convergence вне выведенного joint-critical shell; admissible variation image; источник всей цены при
выбранном native clock/measure law; joint nonflat roots и исходный
fixed-g/fixed-tau `h^-2` comparator. В частности новый ambient theorem
не отменяет [stored variation-image obstruction](sources/d0_native_gr_source_image_2026-10-16/RESULT_RU.md):
ранги10/9/8/7/5, Bianchi-compatible остаток и exact exceptional mode,
где обычная conformal trace row не устраняет его. Нельзя получить
полный Einstein source одним скалярным endpoint weight.

Проверка нового finite algebra: [helper и результаты](sources/d0_finite_heat_source_limit_2026-10-16/).
Аналитические (5)–(13) проверяются изложенным доказательством и
независимым review; finite tests не объявляются доказательством limits.
Старые root/kernel/Lean suites повторно не запускаются.
