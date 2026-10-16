# От native coframe и полной связи к настоящему геометрическому источнику

16 октября 2026. Продолжение [Draft #334](https://github.com/gvakhrushev/d0_15/pull/334),
SOURCE `158ae7858352c5c7ece44f565f6da0463b2e646a`.
Потребитель: равенство native price/source и реконструированного Einstein
source, с настоящими observer/matter/measure equations, не скалярный fit.

**Получено.** Реконструированная Lorentz-связь действительно входит в
существующий forward operator: при правильном знаке и representation она
даёт полный exterior differential на всех16 grades. На общей связи
вычислен настоящий traced heat coefficient a2, включая кручение и меру.
Его24 connection rows имеют rank8: tensor16 не исчезает из оператора.
Для всех этих16 направлений определён следующий a4-source на плоском
coframe; во всём constant tensor sector его единственный critical point
есть T=0. Явный curved witness имеет a2=0 и a4=4lambda^4/3.
Ниже эти коэффициенты включены в **тот же** H+J+R через точное spectral
разложение feedback. Новое действие или fitted stress не вводятся.

## 1. Проверка присланного соединения: scalar edge jet не равен contorsion

[Исходная передача пользователя](sources/d0_coframe_heat_source_2026-10-16/USER_INPUT_RU.txt)
сохранена побайтно. Её предложение о проверке источников потребляется;
утверждения о уже доказанном совпадении коэффициентов требуют проверки.

Weighted transport сохраняет `sqrt(omega_x/omega_y)` и
`(dlog omega_x-dlog omega_y)/2`. Это scalar endpoint datum.
[Coframe dressing](MEMO_A4D_FINITE_GRADED_COFRAME_DRESSING.md), §0,
прямо помещает skew modulus в CAR/group-algebra operator carrier,
**не** в gl4/so4; прежний такой dimension count там отозван.
Свобода skew при fixed DW не доказывает чувствительность полной цены
к этому skew и не отождествляет его с Lorentz contorsion.

Есть exact counterexample к предлагаемому scalar отождествлению.
В [pp-wave reconstruction](A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md), §5,
`e=I+HN`, `det e=1`, `A=I`, `n=e0`. Можно взять постоянный site weight1.
Тогда оба endpoint factors и их jets постоянны, scalar edge jet равен0,
но при Hx!=0 или Hy!=0 восстановленные C и omega_LC ненулевые.
Следовательно, ни линейное, ни квадратичное совпадение с L_T из такого
edge jet не следует. Оно не было закрыто даже «по одному направлению».
Это не отсутствие остальных полей: полный forward из следующего раздела
уже читает coframe и Lorentz-связь, а scalar weight читает отдельный канал.

## 2. Явное соединение с уже существующим native operator

Обозначим C_a exterior creation, I_a=C_a*, eta=diag(1,-1,-1,-1),
F=e^-1, `v_mu=eta F_mu^T`. У continuum first jet той же положительно-
сопряжённой [full-Lorentz реализации](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md)

```text
d_Omega=sum_mu C(v_mu)(partial_mu+Gamma(Omega_mu)),
D_Omega=d_Omega+d_Omega^sharp.                            (1)
```

Здесь `A_(x,x+ell mu)=I+ell Omega_mu+O(ell^2)` — first jet реального
proper Lorentz transport. Для exact links нужен parallel transport или
exp(ell Omega), а не объявление I+ell Omega точной Lorentz-матрицей.
Формула (1) фиксирует differential candidate; finite-to-continuum source
estimate из одного Taylor jet не выводится.

При `Omega=omega_LC(e)` имеем точное continuum intertwining

```text
U d_omega U^-1=d_exterior, U=Lambda(eta),
U C(eta F_mu^T)U^-1=C(F_mu^T),
eta omega eta=-omega^T.                                  (2)
```

Доказательство: covector coefficients обычной формы имеют connection
`-omega^T`; поднятие всех внутренних индексов eta превращает её в +omega.
Cartan torsion-free identity даёт exterior differential во всех степенях.
Следовательно, **+omega_LC в исходном native slot**, а не -omega_LC^T,
воспроизводит требуемый lower-order term. Это оценка имеющихся link
переменных на заданном графе, не замена literal stored operator и не
доказательство, что его независимые Euler rows выбирают этот граф.

Положительная pairing наблюдателя даёт positive covariant metric G.
В observer-adapted frame n=e0 это `G=e^T e`; вообще
`G=e^T h_n e`. При `mu=dV_G` истинный adjoint в (1) даёт обычный
G-Hodge Dirac на графе (2). При другой мере это weighted adjoint:
меру нельзя автоматически переименовать в геометрический объём.
Moving observer требует полной смены frame, connection и torsion;
его derivative не заморожен этим локальным вычислением.
Например, при L=sqrt(h_n) это `theta'=L theta`,
`Omega'=L Omega L^-1-dL L^-1`, `T'=L T`; (5),(6) используют именно
positive-frame компоненты. Inhomogeneous connection term сохраняется.

Эти differential examples не обязаны оставаться вне открытого matrix
window. На ограниченном patch возьмём `||v_mu||<=K` и
`||Omega_mu||<=W`. Proper parallel transports длины ell<=ell0 имеют
`||Lambda(A)||<=exp(4ell0 W)` на full16. Постоянное изменение поля
`F->sF`, `e->e/s`, `0<s<exp(-4ell0 W)/K` даёт строгие contractions
и для creation, и для transported creation. Omega_LC при таком
постоянном масштабе не меняется. Тем самым поля и их exact proper links
попадают в Julia domain; price calibrations не меняются. Это доказывает
матричную кинематическую допустимость, не native primitive generation
или joint stationarity. Original inverse-return вне stored class не
подменяется истинным adjoint этим масштабированием.

## 3. Все24 connection-компоненты: источник a2 вычислен

Работаем в positive orthonormal frame, `gamma_i=C_i-I_i`,
`{gamma_i,gamma_j}=-2delta_ij`. T обозначает coframe torsion исходной
связи, с `T^a_bc=-T^a_cb`. На всех16 компонентах

```text
d_Omega=d_exterior-Q_T,
Q_T=sum_(a,b<c) T^a_bc C_b C_c I_a,
Z=-(Q_T+Q_T*), D_Omega=D_Hodge+Z.                         (3)
```

При фиксированном e Lorentz Cartan map между24 connection differences
и24 T-компонентами обратим. Поэтому вычисление по всем T не теряет
независимые link rows. Нормы в формулах ниже positive-frame norms,
не Lorentz eta contractions.

Используем Laplace convention `P=-(nabla^2+E)`. Для того же principal
metric и Clifford-compatible Hodge connection добавка Z меняет
connection на `W_i=-{gamma_i,Z}/2`. Полный trace даёт

```text
Tr(E-E_H)=-Tr Z^2-(1/4)sum_i Tr{gamma_i,Z}^2.             (4)
```

Производные сокращаются **точечно**:
`Tr[-gamma^i nabla_i Z+(1/2)nabla_i{gamma^i,Z}]=0`,
поскольку `nabla gamma=0`. Они не удалены как неизвестный boundary term.
Для full exterior bundle в4D `Tr E_H=-4R_G` и
`Tr(E_H+R_G/6)=-4R_G/3`.
Стандартные Laplace-type определения и heat formula —
[Vassilevich, (2.2)–(2.4), (4.27)–(4.28)](https://arxiv.org/pdf/hep-th/0306138).
Расчёт (3),(4) относится к actual native difference, а не к назначенной
Hodge-модели вместо него.

Определим четыре trace и четыре cyclic компоненты

```text
v_c=sum_a T^a_ac,
h_abc=T^a_bc+T^b_ca+T^c_ab, a<b<c.
```

Full16 CAR вычисление (4) на ВСЕХ24 направлениях даёт

```text
q(T)=2sum_(a<b<c) h_abc^2-4sum_c v_c^2.                  (5)
```

Оно также следует из Clifford разложения: видимы pure gamma^3 и
одиночные hatgamma=C+I; mixed gamma hatgamma hatgamma имеет нулевую
quadratic form. В координатной норме `sum_(a,b<c)(T^a_bc)^2`:

| SO4 sector | Dimension | Gram eigenvalue |
| --- | ---: | ---: |
| trace |4| -12 |
| three-form |4| 6 |
| tracefree, cyclic-zero tensor |16| 0 |

Это полный bilinear kernel, не только множество q=0. Образ этих16
направлений в Z также имеет rank16: сами операторы меняются.
Leading connection Euler `dq=0` фиксирует v=h=0, но не T=0.
Поэтому вывод LC из одного ведущего curvature coefficient неверен.

### Настоящий scalar measure channel

Пусть `mu=w dV_G`, `b=dlog w`. После unitary multiplication sqrt(w)
weighted operator имеет добавку `Z_eff=Z-hatgamma(b)/2`. Exact CAR traces
дают

```text
L2=Tr(E+R_G/6)=-4R_G/3+2sum h^2-4|v-b|^2.               (6)
```

Это coefficient density относительно dV_G. Если heat kernel записан
относительно mu, его diagonal coefficient делится на w; произведение
на mu снова даёт (6)dV_G. Нельзя писать (6)mu без этого преобразования.
При fixed e,w leading link rows требуют `h=0, v=b`, оставляя tensor16.
Для counting density dx имеем `w=1/|det e|`, а не произвольный новый
weight law; тогда `b=-dlog|det e|`. Все его coframe derivatives остаются.
Вот конкретное место scalar density derivative в **реальном** источнике.
Он не является всем C и не устанавливает коэффициенты L_T по одному edge.
Формула относится к полному положительному adjoint (1); старый literal
stored D под произвольным новым weight остаётся в своём прежнем domain.

## 4. Проверка на coframe из реконструкции

При `a=(t+z)/sqrt2`, `bcoord=(t-z)/sqrt2` имеем

```text
theta_a=da, theta_b=dbcoord+H da, theta_x=dx, theta_y=dy,
E_a=partial_a-H partial_b, E_b=partial_b,
G=da^2+(dbcoord+H da)^2+dx^2+dy^2, det G=1.
```

Здесь переменная bcoord отличается от measure covector b в (6).
При исходной связи A=I настоящий оператор

```text
D0=gamma_a E_a+gamma_b E_b+gamma_x partial_x+gamma_y partial_y,
P0=-(E_a^2+E_b^2+partial_x^2+partial_y^2)-K partial_b,
K=sum_(i=x,y) H_i gamma_i gamma_a, K^2=-|grad H|^2 I16.
```

Contracted Christoffel равен0; unique Laplace completion:
`omega=K(dbcoord+H da)/2`, `E=|grad H|^2 I16/4`,
`R_G=-|grad H|^2/2`. Следовательно,

```text
L2(A=I)=8|grad H|^2/3,
L2(Omega=omega_LC)=2|grad H|^2/3.                          (7)
```

Разность2|grad H|² — ровно q(T), а не потерянная мера: обе volume
densities и counting dx здесь совпадают. Native raising при A=I имеет
`d0^2=-sum H_i C_i C_a partial_b`, вообще ненулевой. Подстановка (2)
порождает существующими Lorentz link variables **ровно**
`Q=sum H_i C_i C_a I_b`; `d0+Q` становится exterior differential.
Добавление Q вручную не предлагается.
Более того, для исходной Lorentz reconstruction на этом же ansatz
`C=omega_LC=W(dt+dz)`, `C wedge C=0`, `B=Sigma wedge C=0` и `L_T=0`
тождественно. Ненулевая положительная heat-разность в (7) не является
этим Lorentz L_T. Таким образом проверено и опровергнуто заявленное
в передаче квадратичное отождествление, а не только подсчитаны размерности.

Для общего профиля и compact/periodic profile variations
`delta int L2(A=I)/delta H=-(16/3)(Hxx+Hyy)`.
Lorentz R(g) равен0 на ВСЁМ этом ansatz, поэтому restricted EH derivative
по H равен0 даже вне vacuum. Это явный source mismatch, а не просто
сравнение значений curvature. При harmonic vacuum профильный L2 source
тоже нулевой: это не доказывает остальные metric rows и не опровергает
все curved roots. LC Hodge coefficient всё ещё относится к G, а его
переписывание через g сохраняет уже выведенный
[observer source](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md).

## 5. Оставшиеся16 направлений: следующий coefficient уже имеет источник

На flat positive coframe и natural measure любой tensor-kernel Z имеет
точное представление

```text
Z=sum_i gamma_i B_i,
B_i=-{gamma_i,Z}/2, B_i*=-B_i, [B_i,gamma_j]=0.
```

Таким образом D — Dirac того же principal metric с right-Clifford
connection. При `F_ij=partial_i B_j-partial_j B_i+[B_i,B_j]`
standard a4 formula и full16 trace дают

```text
L4=-(1/6)Tr16 sum_(i,j) F_ij^2 >= 0.                     (8)
```

Здесь `E=-sum_(i<j)gamma_i gamma_j F_ij`, `Tr E=0`,
`Tr E^2=-(1/2)Tr sum F_ij^2`; traced derivative term также равен0.
Это следующий coefficient ТОГО ЖЕ square, не добавленная Yang–Mills цена.
Для допустимых tensor variations, `delta B_j=L_j(delta T)`,

```text
delta int L4=(2/3)int Tr sum_j(sum_i D_i F_ij)delta B_j.
```

Здесь variations periodic/compactly supported; иначе boundary term
после integration by parts также должен остаться.

Получен projected connection source по всем16 tensor directions,
а не требование unrestricted24 right-connection rows. На кривом G нужны
также исходная Hodge curvature и её mixed terms; flat formula не объявлена
полным curved-source theorem.

### Полная классификация constant tensor critical points этого coefficient

При постоянном T из tensor16 все B_i постоянны, и (8) есть
`(1/6)sum||[B_i,B_j]||_HS^2`. Если L4=0, все B_i коммутируют.
При этом `Q_T vac=Q_T* vac=0`, значит `Z vac=0`.
Из `D^2=-sum(partial_i+B_i)^2` при нулевой curvature и постоянного
vacuum section получаем `sum||B_i vac||^2=0`. Каждый B_i коммутирует
со всеми gamma_j, а16 различных gamma-words на vacuum дают полную
occupation basis. Следовательно, все B_i=0, Z=0. Его raising part
Q_T=0, но `Q_T theta^a=T^a`, поэтому T=0.

Итак, L4(T)>0 для любого ненулевого **постоянного** tensor T.
Quartic homogeneity даёт `dL4_T[T]=4L4(T)>0`: никакой ненулевой constant
tensor не решает все16 Euler rows A4. Это классификация всего данного
блока без census или выбора одного удачного witness. Для переменного
B(x) curvature включает derivatives; вывод T=0 из этого доказательства
не следует. Полная цена использует также коэффициент и остальные
источники из (11).

Явный exact witness `T^0_12=T^1_02=lambda`, остальные0, лежит в полном
kernel (5), но

```text
Z=(lambda/2)(gamma0 hatgamma1 hatgamma2+gamma1 hatgamma0 hatgamma2),
B0=lambda hatgamma1 hatgamma2/2, B1=lambda hatgamma0 hatgamma2/2,
F01=lambda^2 hatgamma0 hatgamma1/2,
L2=0, L4=4lambda^4/3, dL4/dlambda=16lambda^3/3.           (9)
```

Его нельзя назвать flat flavour holonomy или удалить как невидимый оператор:
curvature ненулевая и `Tr Z^2=8lambda^2`. a4 уже различает эту скорость.
Стационарность одной L4 вдоль данного witness требует lambda=0;
стационарность полного H+J+R этим ещё не заменена.

## 6. Включение в полную неизменённую цену

При `qz=z/(1-z)<1`, `N_H=dim H`, exact finite-B identity:

```text
J=-M N_H log(1-z)
  -M sum_(r>=1) (-1)^(r+1) qz^r Tr B^(mr)/r.             (10)
```

Это convergent log series той же (8) full-Lorentz owner price. Внешние
reference/workspace не удалены; первый член field-independent только на
фиксированном carrier и fixed z. Дискретная смена числа rounds не является
полным гладким field derivative.

Чтобы применить coefficients выше к finite price, требуется uniform trace
**и first-source** approximation `Tr B^(mr)` с достаточным контролем r.
Она здесь не подменяется формальным continuum Taylor jet. Если этот
отдельный переход установлен и

```text
Z(t)=(4pi t)^-2[A0+t A2+t^2 A4+O(t^3)],
A0=int16 dV_G, A2=int L2 dV_G, A4=int L4 dV_G,
Phi_s(qz)=sum_(r>=1)(-1)^(r+1)qz^r/r^s,
```

Для общего curved G здесь A4 означает **полный** actual coefficient
с curvature/mixed terms. Формула (8) вычисляет его только в указанном
flat tensor sector, а не заменяет общий A4.

то полный fixed-calibration source до данного порядка равен

```text
dS=C0 dA0+C2 dA2+C4 dA4+dR+dRem,
C0=1/(beta A0)-A2/A0^2-beta A4/A0^2+beta A2^2/A0^3
                         -M Phi3/[(4pi)^2 beta^2],
C2=1/A0-beta A2/A0^2-M Phi2/[(4pi)^2 beta],
C4=beta/A0-M Phi1/(4pi)^2.                               (11)
```

В (11) сохраняются global log normalizer, nonlinear A2² term, feedback
и actual matter R. При moving calibrations нужны полные derivatives
[unfolding (7)](A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md).
В tensor flat sector `dA0=dA2=0`: actual next source есть
`C4 dA4+dR+dRem`, с вычисленным (8), а не произвольно назначенный YM.
Нельзя объявить только dA4=0 полными native equations или считать C4
ненулевым без его actual calibration. Fixed-Mz beta->0 stationary route
уже ограничен [scale/minmax theorem](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md#7-полный-масштабный-баланс-и-препятствие-small-heat-refinement).

Таким образом, геометрическое восстановление теперь соединено с настоящим
дифференциальным оператором, всеми24 ведущими link rows, scalar measure
channel и следующим источником16 оставшихся направлений. Полный
finite-price/source limit и собственный native generation/preparation law
остаются необходимыми: коэффициенты нельзя выбирать для равенства Einstein.
Исходный fixed-smooth-g/fixed-tau/raw-l1 terminal не изменён.

## Проверка и публикация

Полные exact Gram/kernel, LC-sign/pp-wave identities, density shift и
curved tensor a4 witness находятся в
[source folder](sources/d0_coframe_heat_source_2026-10-16/).
Проверяется изменённая математика; прежние L8 root/kernel suites,
65/89/211-check packets и Lean не воспроизводятся заново.
Из присланной переписки сохранён исходный текст, а не приняты её
невычисленные утверждения о совпадении scalar jet и C.
