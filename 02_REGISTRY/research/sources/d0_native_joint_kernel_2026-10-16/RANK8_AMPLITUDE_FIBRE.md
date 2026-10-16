# Rank8: гладкий amplitude source level и следующий normal operator

16 октября 2026. Тот же L8 full16/reference128 v8 action, тот же
stored-adjoint chart и исходный heat root. Новый независимый
[rank8 source proof](RANK8_SOURCE_SUBMERSION.md) и
[его exact helper](rank8_source_submersion.py) поставляют rank151,
включая q0 rank7 и все nonzero shell-transfer ranks3/5. Здесь этот
расчёт не повторяется. Этот consumer владеет normal reduction через
сырые амплитуды, constructive second-jet lift и nonlinear family.

**Статус.** Source fibre гладок через actual rank8 preparation и не
требует сохранения ранга. Полная flat amplitude family имеет57195
измерений. Нормальная невырожденность **всей неоднородной rank8 field
задачи ниже остаётся отдельной открытой предпосылкой**. Однородный q0
slice разбирается отдельно и этой предпосылки не требует.

## 1. Source map на sphere, без PSD quotient

Пусть P — прежний rank128 spectral shell на Omega={+/-e_r}, Q=I−P.
Actual native seed chi принадлежит SO(3)-fixed сектору E0 полного16
carrier; его convention и sign bridge берутся из source proof.
Положим `rho8=P_Omega/8 tensor |chi><chi|` и выберем normalized matrix
`C8:H_ref128 -> P H`, `C8 C8*=rho8`. Его rank равен8; reference
по-прежнему имеет128 измерений. Не вводится отдельный восьмимерный
reference или усечённый matter operator.

Для постоянного SO(4)-coframe R около identity Delta_R=Delta_* и
P сохраняются. Полный field source при фиксированном R эквивалентен
151 независимой tracezero Hermitian shell probes A_j(R). Их можно
гладко выбрать из полной native field tangent map:

```text
A_j(R)=P X_(v_j)(R)P−Tr_P(P X_(v_j)(R)P) P/128,
mu_R,j(C)=Tr(C* A_j(R) C),  j=1,...,151,
C in S={C:Tr C*C=1}.                              (R1)
```

Target в (R1) равен **нулю**. Причина — существующая particular root
P/128: heat/feedback source точно отменяет trace part каждого probe.
Остальные field rows являются гладкими линейными комбинациями этих151
rows около R=I, поскольку полный source map имеет constant rank151.
Поэтому mu_R=0 сохраняет все field equations, а не выбранную их часть.

Сфера S имеет real dimension `2*128*128−1=32767`. Она гладка при
любом ненулевом C, независимо от Schmidt rank. Rank8 PSD quotient
сингулярен как quotient, но эта особенность не переносится автоматически
на исходную amplitude sphere.

## 2. Submersion и точный right inverse

Существенный вход source proof есть

```text
rank_R D mu_I(C8)=151.                            (R2)
```

Это actual native rank, в отличие от общей dimension1983 образа
rank8 density tangent. В real HS pairing
`<B,D>=ReTr B*D` при mu_R(C)=0 spherical gradients равны

```text
g_j=2 A_j(R) C,
G_ij=<g_i,g_j>=4 ReTr[C* A_i(R) A_j(R) C].         (R3)
```

Они касательны сфере, поскольку `<C,g_j>=2 mu_j=0`. Из (R2)
G положительно определена. Явный right inverse есть

```text
L_R,C b=sum_i g_i (G^{-1}b)_i,
D mu_R(C) L_R,C=I_151,
<C,L_R,C b>=0.                                   (R4)
```

Здесь обращается только положительная151x151 real Gram, а не C,
rho8, sqrt(rho8) или их нулевые singular values. Формулы (R3)–(R4)
дают exact algebraic right inverse; quantitative conditioning Gram
является отдельным численным вопросом, не предпосылкой этой local IFT.

Ненулевой Gram determinant сохраняется при малых изменениях R,C.
Actual memory rho8 остаётся particular root при каждом малом R:
homogeneous coframe sources скалярны по full16, а stabilizer-link
sources annihilate chi из `Gamma(so3)chi=0`; nonzero Fourier rows
исчезают по momentum trace. Поэтому mu_R(C8)=0. Parameter-dependent
regular-level theorem даёт гладкое семейство

```text
F_R={C near C8: ||C||_HS=1, mu_R(C)=0},
dim_R F_R=32767−151=32616.                        (R5)
```

Никакая симметрия SO(4)-links для этого не нужна. Constant rank полного
source map на rotated coframes обеспечивают universal upper bounds7/3/5
и root minors continuity из full source owner; submersion (R2)
сохраняется отдельно по непрерывности (R3).

## 3. Constructive second jet и рождения ранга

Пусть B касателен F_R в C: `<C,B>=0`, `D mu_R(C)B=0`. Определим
real vector `nu_j(B)=Tr B* A_j(R) B`. Тогда

```text
C(t)=C+t B+t^2 D/2+O(t^3),
D=−||B||_HS^2 C−2 L_R,C nu(B).                   (R6)
```

Действительно,

```text
(||C(t)||^2)''_0=2<C,D>+2||B||^2=0,
(mu_j(C(t)))''_0=(D mu D)_j+2 nu_j(B)=0.          (R7)
```

Radial term не меняет source second jet, поскольку D mu C=2mu=0.
Regular-level IFT интегрирует (R6) точной гладкой кривой в F_R;
добавлять tangent acceleration можно свободно. Это constructive
source/normalization lift, не решение ненулевого field continuation.

Пусть Pi=ran C8 в P и L=ran C8* в reference, обе dimension8.
Все genuine rank-birth matrices

```text
B=(P−Pi) B (I_ref−L)                              (R8)
```

имеют `<C8,B>=0` и `D mu(C8)B=0`: их linear density variation
`B C8*+C8 B*=0`. Поэтому все `2*120*120=28800` real birth directions
касательны **точному** source level и получают lift (R6).
Они не являются reference-unitary tangents и не должны удаляться.
Если B обратима между двумя120-dimensional kernels, точная кривая
из (R6) имеет full rank128 при достаточно малом t!=0: её determinant
имеет leading factor `t^120 det(C8|_L) det B`.

Таким образом около rank8 имеются точные faithful **flat** stationary
preparations. Это не перенос normal inverse с далёкой maximal density:
при движении вдоль source fibre transverse field spectrum может меняться.

## 4. Rank-free Q-elimination и точный functional

Используем неизменённые Schur E,J,G исходного владельца. Для любого
C на сфере, включая rank8, скалярное уравнение

```text
Tr C* E(x,epsilon) C=0                            (R9)
```

определяет гладкую epsilon_hat: его epsilon derivative равна
`−Tr C*G C<0`. Положим

```text
N_C=Tr C*G C,
Phi_amp(x,C)=F_price(Delta(x))+epsilon_hat(x,C),
Psi=J C/sqrt(N_C).                               (R10)
```

Функция (R10) гладка на field chart и всей amplitude sphere. Её
stationary equations есть точно

```text
E C=0,
Tr kappa(Delta) X_v +Tr[C*J*X_vJ C]/N_C=0 for all v. (R11)
```

Для C-вариаций tangent gradient пропорционален E C; возможный radial
multiplier зануляется уравнением (R9). Условие E=0 здесь **не**
подставляется: при lower rank оно сильнее (R11).

Для строгого amplitude interpretation используем normalized coordinates
`Psi=sqrt(1−||Y||^2) C+Y`, QY=Y, ||C||=1. Форма Q mass равна
`2(Delta_Q−epsilon) tensor I128`, имеет прежний spectral gap и обратима
независимо от rank C. Кандидат `Y=QJ C/sqrt(N_C)` критичен по всем
Y: Q-residual нулевой, а remaining radial contraction равен (R9).
Его значение действия есть Phi_amp. Значит это exact stationary
elimination со всеми mixed terms и normalizer derivatives, а не
построенный после rank quotient surrogate functional.

## 5. Полная flat amplitude family и один global overlap

Берём свободные малые periodic H_x in SO^+(1,3), постоянный R in SO(4)
и C in F_R. Точные native поля и matter задаются

```text
n_x=H_x e0,  v_r(x)=H_x R u_r*,
A_xy=H_x H_y^{-1},
Psi_(H,R,C)=[direct_sum_x exterior(H_x)] C.        (R12)
```

Intertwiner владельца переносит полный ordered Dirac, pairing,
normalization и source equations. Поэтому (R12) — actual full joint
roots, а не только направления Hessian kernel. Все linear-link
holonomies равны I, Lorentz Gram постоянен
`(u_r*)^T R^T eta R u_s*`. Три moduli вне spatial SO3 меняют этот
Gram и не отбрасываются как physical gauge.

Существует ровно один global spatial SO3 overlap:
`H_x -> H_x K^{-1}`, `R -> K R`, `C -> exterior(K) C`.
Других field stabilizers нет из invertibility coframe. После выбора
локальной section SO3\SO4 это гладкая family размерности

```text
6*4096+6−3+32616=57195.                           (R13)
```

Никакой U128 quotient здесь не берётся. При rank8 right U128 action
имеет U120 stabilizer; его orbit dimension1984, а rank8 density stratum
имеет dimension1983. Их сумма3967 плюс28800 birth directions равна
32767 — всей shell sphere. Добавлять reference orbit повторно к (R13)
или переносить faithful density coordinates через sqrt(rho8) нельзя.

Образ этого уровня в density variables есть affine PSD section
`{rho>=0,Tr rho=1,Tr rho A_j=0}`. Она стратифицирована по rank, а не
является гладким многообразием одной размерности. Submersion через
амплитуды означает surjectivity source derivative и на каждом близком
fixed-rank density stratum: reference tangents не влияют на rho. Для
rank k>=8 его local dimension равна
`2*128*k−k^2−1−151=256k−k^2−152`. В частности, это1832 при k=8 и
16232 при k=128. При k=8 fixed-rank amplitude stratum имеет
`1832+1984=3816` измерений; остальные28800 tangent directions гладкого
level (R5) выходят в большие ранги. Эта граница quotient не создаёт
сама по себе дополнительного normal field kernel.

## 6. Точный оставшийся field-normal criterion

В (R10) ambient dimension равна `65536+32767=98303`. Полная flat family
уже даёт57195 tangent kernel directions. Source submersion (R2)
имеет ещё одно существенное следствие: linear amplitude coupling имеет
тот же field kernel, что прежний полный T. Иначе ненулевой linear
combination A_j действовала бы как spherical scalar на C8, что
противоречило бы независимости151 gradients (R3).

Пусть G_field —24579-dimensional tangent поля из (R12), а

```text
V =ker T / G_field,  dim_R V=65536−151−24579=40806.
H8^V = actual field Hessian of Phi_amp restricted to V.     (R14)
```

Представители quotient можно выбрать фиксированной гладкой section.
Его quadratic form определён корректно: если symmetry field tangent
имеет amplitude lift, contraction mixed source block с ker T нулевой.
**Normal premise:** существует c>0, для которого

```text
(H8^V)^* H8^V >= c^2 I_V.                         (R15)
```

Это finite-dimensional indefinite invertibility criterion, а не
положительность H8^V. После151 source-normal amplitude coordinates и
151 сопряжённых field directions точная normal congruence имеет вид

```text
H_normal congruent H8^V direct_sum hyperbolic(151,151).
dim normal=40806+302=41108.                        (R16)
```

Field/source cross blocks не изменяют (R14): inverse hyperbolic block
имеет нулевой field-field corner. Поэтому (R15) эквивалентно отсутствию
дополнительного shell/field kernel сверх tangent (R13). Если (R15)
доказана, normal IFT даёт local Morse–Bott completeness через rank8;
точный Q-block добавляет прежние positive/negative masses без нулей.
Все близкие roots тогда лежат в flat family (R12), включая рождения
ранга. **Здесь (R15), full rank8 inertia и shared-normal kernel не решены.**

Следующий экономный consumer — bound (R15) на field quotient, а не
огромная full-amplitude KKT. В частности, при том же поле

```text
H_rho(v,w)=H_heat(v,w)+Tr rho N_vw,
N_vw=P[Y_vw−X_v R_Q X_w−X_w R_Q X_v]P.            (R17)
```

Все second jets и signed R_Q сохраняются. Разница с faithful form
линейна по `rho8−P/128`. Один строгий signature-distance bound для
preconditioned (R17) может дать (R15); простая близость состояния не
предполагается. Нельзя переносить faithful field inertia только из
того, что source kernels совпали: actual matter curvature в (R17)
может зависеть от preparation.

Например, если уже имеется точная square congruence B на V и signature
Sigma с `||B*H_faithful^V B−Sigma||<=delta<1`, достаточно одной оценки
`||B*(H8^V−H_faithful^V)*B||<1−delta`. Это достаточный comparison test,
не установленный bound: его неуспех не доказывает singularity H8^V и
не разрешает ослабить actual second jet.

Если появляется дополнительный field kernel v, первый nonlinear
consumer — полные eigenjet equations
`E1 C8=0`, `E2 C8+2E1 C1=0` и cubic compatibility со всем kernel.
Для чистой nonzero Fourier field speed вне Omega−Omega, с её решённым
Q-response и без дополнительной shell speed, stationary amplitude fibre
даёт один необходимый matrix-action test

```text
[N_vv−lambda P−sum_j beta_j A_j] C8=0,
lambda,beta_j real.                              (R18)
```

Это Lagrange multiplier consequence submersion и normalization:
градиент `Tr C*N_vv C` должен быть normal к F_R. Оно включает
rank-aware memory neutrality и не объявляет kernel решённым. Для
смешанных shell/field speeds нужны все bilinear jets, не только N_vv.
Birth directions невидимы linear density map, поэтому (R18) не заменяет
их последующие eigenjet constraints и не гарантирует curved branch.

## 7. Завершённый q0 consumer с fixed reference momentum grading

Здесь ограничиваем **одновременно** поля homogeneous chart и amplitude
slice

```text
C=direct_sum_(k in Omega) C_k,  C_k: C16_ref,k -> C16_work,k.
dim_R normalized slice =8*(2*16*16)−1=4095.        (R19)
```

Reference momentum grading фиксирована. Это не вся U128 orbit и не
утверждение о произвольном inhomogeneous shell C. Rank8 source proof
даёт q0 submersion rank7 на (R19). Поэтому q0 amplitude source level
имеет dimension4088, включая свои rank births.

Его field kernel T8 равен прежним16 directions: четыре link angles
исключаются; остаются семь equal-diagonal Gram directions, шесть SO4
frame directions и три observer directions. На representatives с
identity links весь оператор имеет

```text
Delta_k=lambda_k(G_E) I16,
lambda_k linear in G_E,
Q Delta P=0.                                     (R20)
```

Matter contribution на shell — scalar linear Gram functional с pair
masses; при equal-diagonal variations он равен gamma*d независимо от
internal preparations. Поэтому на семи field-normal Gram directions
сохраняется прежняя строгая positive Hessian
`F_price(G_diag=d,offdiag)+gamma*d`, с полным global Z normalizer.
Она не требует переноса arbitrary rank8 matter Hessian за пределами
особого coframe/identity-link семейства (R20).

Normal form есть positive7 плюс hyperbolic(7,7); consequently

```text
q0 constrained shell-amplitude/field inertia:
(14 positive,7 negative,4097 zero),
domain dimension23+4095=4118,
critical family dimension9+4088=4097.             (R21)
```

Все эти zeros интегрируются homogeneous вариантом (R12) и source level.
Normal IFT доказывает локальную полноту в slice (R19): остаются точно
identity linear links, прежний heat Gram и homogeneous Lorentz/observer
frames, с положенным source-neutral amplitude fibre, при любом близком
ранге. Первая строка source по nonzero Fourier q при этом нулевая по
momentum trace, так что найденные точки удовлетворяют полной системе.

В (R19) допустимая reference subgroup — U16^8; её fullrank orbit имеет
dimension2048, а при rank1 каждом momentum block — dimension248 и
stabilizer U15^8. Эти числа уже содержатся в4095 raw coordinates и
не добавляются повторно. (R21) не является full inhomogeneous rank8
inertia и не закрывает (R15).

## 8. Границы

Все результаты относятся к той же конечной условной v8 программе,
исходному reference128 и full16 operator. Primitive physical admission,
общее observer/matter update, continuum/refinement inverse, affine
shifts, исходный g_tau readout и h^{-2} raw,l1 terminal не изменены.
Source regularity через rank8 и homogeneous flatness не являются
доказательством ОТО или отрицанием иных режимов исходной задачи.
Новые old-suite runs, root solves, receipt writers или изменения прежних
owners для этого аналитического consumer не выполнялись.
