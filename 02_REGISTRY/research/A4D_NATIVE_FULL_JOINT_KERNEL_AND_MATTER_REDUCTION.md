# Полная совместная система: допустимая карта, точное исключение материи и оператор ядра

2026-10-16. Исполнение: [Draft #334](https://github.com/gvakhrushev/d0_15/pull/334),
задача `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Научный вход — опубликованный `74e62cdc716e10883accba9d34ccf0e21d58eb65`:
[stored-native bridge и curved-wave obstruction](A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md),
[точное разворачивание той же цены](A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md)
и [сертифицированный v8 root](sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md).

**Результат.** Для этой же условной v8 задачи построена полная локальная
карта stored-adjoint полей около существующего корня. В её настоящих
координатах все внеспектральные амплитуды материи исключаются **точно и
нелинейно**, с ограниченным обратным оператором. Резонансная подготовка
сохраняется как положительная матрица, а её нормировка — как собственное
уравнение. Полная линеаризация есть связанная блочная система (15), а не
одно значение второй вариации. Это снимает задачу обращения огромного
внеспектрального amplitude-блока; оставшийся полевой/резонансный блок ещё
нужно решить. Неплоский совместный root, физический допуск программы,
полная native Cost−Info цена и предел ОТО здесь не утверждаются.

## 1. Неизменённая задача и сохраняемые компоненты

Фиксируются прежние `L=8`, `n=8192`, `m=2n`, `alpha=p²/8192`,
`beta=m alpha=2p²`, `z=2^-20`, `M=128`, `C=128 workspaceDim`,
`workspaceDim=128^8192`. На **полном** пространстве
`H=ell²((Z/8)^4) tensor Lambda(C4)`, `N=dim H=65536`, положим

```text
Delta(x)=D(x)², B=I-alpha Delta, K=B^m,
A=(1-z)I+zK, Z=Tr_H K,
F_price(Delta)=log(C Z)/beta-M Tr_H log A,
S(x,Psi)=F_price(Delta(x))+Tr(Psi* Delta(x) Psi),
Psi:H_ref -> H, dim H_ref=r=128, Tr(Psi*Psi)=1.       (1)
```

`D(x)` — actual stored operator, перенесённый полным whitening §0.3
владельца; коэффициенты и shifts не переставляются. `x` включает все
допустимые coframe/link/observer и остальные параметры этой программы.
Affine shifts, отсутствующие в literal CAR operator, не получают новой
цены: их нулевые строки сохраняются, пока другой actual owner не задаст
их зависимость. Ни один из16 exterior grades,4096 momentum modes,
reference или workspace не удалён. Matter использует Delta, тепло —
`Lambda=-log B/alpha`.

Независимая нормированная `Psi` — область **объявленной v8 задачи**.
Это не доказательство, что D0-core физически допускает её независимо
от observer/readout. Если такой процесс связывает подготовку и поля,
вся система ниже требует pullback по **этой связи**, а не её удаления.

## 2. Полная гладкая stored-adjoint карта у данного корня

Внутренняя Lorentz форма `eta=diag(1,-1,-1,-1)`. На локальной компоненте
единичного observer `n=(n0,s)`, `n0=sqrt(1+|s|²)>0`, заданы

```text
h_n=-eta+2 eta n n^T eta,
L_n=[[n0,-s^T],[-s,I+s s^T/(1+n0)]].                 (2)
```

Прямое умножение даёт `L_n eta L_n=eta`, `L_n²=h_n`,
`L_n>0`, `L_n n=e0`. Это каноническое positive whitening, а выбор
локальной компоненты около `e0` не выводит физическую стрелу времени.

Для Lorentz link и обоих stored-adjoint условий владельца

```text
A_xy^T h_x A_xy=h_y, A_xy v_r(y)=v_r(x), y=x+r,
u_r=L_x v_r, O_xy=L_x A_xy L_y^-1,
```

матрица O одновременно ортогональна и Lorentz. Около identity поэтому
`O=diag(1,R)`, **R in SO(3)**. Произвольная SO(4) rotation здесь была бы
лишней, недопустимой вариацией. Разложим полную leg как
`u_r=(tau_r,rho_r z_r)`, `rho_r>0`, `|z_r|=1`. Тогда точные условия равны

```text
tau_r(x+r)=tau_r(x), rho_r(x+r)=rho_r(x),
R_r(x) z_r(x+r)=z_r(x).                              (3)
```

У настоящего корня `F_*=(a-b)I+b11^T`, `a>b>0`,
`v_r=eta F_*r^T`, `n=e0`. Все spatial lengths строго положительны:
`rho_0=sqrt(3)b`, `rho_i=sqrt(a²+2b²)`. Условие `b>0` следует из
прежнего `d>o>0` и положительного square root F. Это регулярная
компонента, отличная от сингулярного теста `F=eta`, где `rho_0=0`.

Полная карта получается так: tau/rho произвольны на каждой r-линии;
каждый `z_r(x)` произволен в своей S²-карте; на каждом ребре есть один
угол theta. Для близких unit vectors a,b положим

```text
v=a cross b, R0(a,b)=I+[v]_cross+[v]_cross²/(1+a dot b),
R_r(x)=exp(theta_r(x)[z_r(x)]_cross) R0(z_r(y),z_r(x)),
A_xy=L_x^-1 diag(1,R_r(x)) L_y, v_r(x)=L_x^-1 u_r(x).  (4)
```

R0 переводит a в b; все SO(3) решения около identity получаются
последующим вращением вокруг b. Поэтому (4) не только поставляет
некоторые допустимые кривые, но параметризует **все** близкие данные.
Невырожденность coframe и bounded gate inequalities — открытые условия,
сохраняемые в достаточно малой окрестности корня.

### Fourier tangent без заморозки observer или links

Для частоты q положим `kappa_r=1-exp(2pi i q_r/8)`,
`dot n=(0,nu)`, `dot u_r=(alpha_r,beta_r)`,
`u_r*=(tau_r,w_r)`. Полная первая карта равна

```text
kappa_r alpha_r=0, kappa_r (w_r dot beta_r)=0,
W_r=kappa_r(beta_r w_r^T-w_r beta_r^T)/|w_r|²
                   +theta_r [w_r/|w_r|]_cross,
dot O_r=diag(0,W_r),
dot A_r=B_boost(kappa_r nu)+diag(0,W_r),
dot v_r=dot u_r+B_boost(nu) v_r*.                     (5)
```

В (5) beta произвольна в двумерном `w_r`-ортогональном пространстве;
её radial часть и alpha свободны только при `q_r=0`. Nu имеет все три
компоненты. После совместимости link boost определяется nu, а не
замораживается. Реальные поля используют сопряжённые q/−q компоненты.
Каждое такое направление интегрируется точной картой (4).

При p ненулевых координатах q число комплексных параметров символа
равно `23-2p`. Для прежней wave `(3,3,0,0)` их19, а не одна leg.
По всем частотам реальная размерность карты равна
`3 L^4+8 L^4+4 L^4+8 L^3=65536`: observer, четыре S²-поля,
четыре edge angles и line-constant tau/rho. Это размерность условного
stored поля до quotient и до отдельно хранимых affine shifts, не счёт
физических степеней свободы. Все10 компоненты метрического отклика
сохраняются и ограничиваются actual differential, а не выбираются
произвольно независимо от (3).

## 3. Точное нелинейное исключение внеспектральной материи

У прежнего stationary root `Delta0` собственное значение
`epsilon0=(128-64sqrt2)d` имеет проектор
`P=1_{Omega}(momentum) tensor I16`, `Omega={+/-e_r}` и rank r=128.
Положим `Q=I-P`. Старое доказательство отделяет остальные положительные
энергии более чем на1/2. Нулевой mode тоже сохраняется: `d>1/16` и
`sqrt2<3/2` дают `epsilon0>2`, поэтому он не портит bound.
Следовательно `dist(epsilon0,spec(Delta0|Q))>1/2`.

Рассмотрим всю область
`||Delta-Delta0||op<1/8`, `|epsilon-epsilon0|<1/8`, сохраняя прежние
positive survival/price conditions. На Q определим

```text
G_Q=[Q(Delta-epsilon I)Q]^-1, ||G_Q||op<4,
J=P-Q G_Q Q Delta P : P H -> H,
E=P(Delta-epsilon I)P-P Delta Q G_Q Q Delta P,
G=J*J=P+P Delta Q G_Q² Q Delta P.                     (6)
```

Обратимость следует из Neumann estimate для selfadjoint Q-блока;
он вообще **не положителен**. Ни ground mode, ни отрицательная сторона
резольвенты не удаляются. Имеем точно

```text
PJ=P, Q(Delta-epsilon I)J=0,
E=J*(Delta-epsilon I)J,
P<=G<(5/4)P, ||J-P||op<1/2.                          (7)
```

Последние оценки следуют из `Q Delta0 P=0` и
`||J-P||<=4||Delta-Delta0||`. G — настоящий движущийся normalizer.
Обращение конструктивно: у `R0=Q(Delta0-epsilon0)^-1Q` уже известны все
Fourier blocks; для `V_Q=Q[(Delta-Delta0)-(epsilon-epsilon0)I]Q`
имеем `t=||R0 V_Q||<1/2` и

```text
G_Q=sum_(j>=0) (-R0 V_Q)^j R0,
||G_Q-sum_(j=0)^k(-R0 V_Q)^j R0||
                   <=||R0|| t^(k+1)/(1-t)<4*2^(-k-1). (7a)
```

Это norm-convergent series одного и того же Q-оператора, включая его
отрицательную spectral часть; она не выбирает другую eigenbranch.
Оценка получается умножением finite geometric identity на residual
resolvent, без коммутирования R0 и V_Q. Для любой field/epsilon вариации
**даже вне E=0**

```text
dE=J* (dDelta) J-G d epsilon.                        (8)
```

Действительно `range(dJ)` лежит в Q, а residual `(Delta-epsilon I)J`
лежит в P, поэтому оба члена с dJ в производной (7) нулевые.

Исходный augmented action на ненормированной амплитуде:

```text
L_orig=F_price(Delta)+epsilon+Tr[Psi*(Delta-epsilon I)Psi].
```

Его Q-amplitude уравнения решены **все**: `Psi=J C0`, где
`C0:H_ref -> P H`. Около полного Schmidt rank корня C0 обратима.
Положим `tau=C0 C0*>0` на P. Точная редукция augmented action есть

```text
L_eff(x,epsilon,tau)=F_price(Delta(x))+epsilon+Tr_P(tau E).
```

Это не новый action и не pointwise равенство нормированной цены вне
её constraint. Его полные stationary equations суть

```text
E=0,
Tr_P(tau G)=1,
Tr_H[kappa(Delta) X_v]+Tr_P[tau J* X_v J]=0  for ALL v,
X_v=dDelta[v].                                      (9)
```

Обратная реконструкция **всех** normalized full-Schmidt-rank решений
в этом energy window:

```text
Psi=J sqrt(tau) V,  V:H_ref -> P H unitary,
rho_m=J tau J*,  Tr rho_m=1.                         (10)
```

При E=0 получаем `(Delta tensor I)Psi=epsilon Psi`. Equation (8)
даёт normalizer и исходный field source в (9). Обратно Q-строки любой
исходной stationary Psi дают (6); полный rank C0 превращает оставшееся
векторное уравнение в E=0. Вариации C0 порождают все Hermitian вариации
tau. Полярное разложение сохраняет весь V. Он — reference degeneracy
**этой цены**, не автоматически physically admitted gauge.

Так исключены `2(N-r)r=16 744 448` **вещественных** Q-amplitude
координат при реальном N=65536,r=128. Сохраняются `r²=16384`
Hermitian координат tau, epsilon, все поля и reference направления.
Это точная локальная эквивалентность стационарных систем, не объявление
их устойчивыми минимумами. Rank-changing preparations и другие energy
windows остаются частью полной программы; эта локальная теорема их
не исключает. G-bound не даёт нижнюю границу на каждый Schmidt weight.

## 4. Полная производная прежнего heat/feedback источника

Для fixed calibrations обозначим `g=B^(m-1)`. Тогда

```text
kappa(lambda)=-(1-alpha lambda)^(m-1)/Z
      +M beta z (1-alpha lambda)^(m-1)
                  /[1-z+z(1-alpha lambda)^m],
dZ[X]=-beta Tr_H(g X),
Dkappa[X]=L_fZ[X]-(beta/Z²) g Tr_H(g X).              (11)
```

`L_fZ` — spectral divided-difference operator scalar kappa при
фиксированном полном Z. На повторных eigenvalues используется derivative
limit. Последний rank-one член — derivative самого Z; его нельзя
удалять для общего field jet. У старой одной nonzero Fourier wave
`dZ=0`, но это не свойство всей совместной задачи. Все spectral sums
в (11) идут по **полным65536** states, с прежними reference/multiplicities.

При движущихся калибровках действует полная формула (7) владельца
unfolding. Здесь они фиксированы, как у самого certified root.
Оценки auxiliary inverse из unfolding не заменяют физический shell block.

## 5. Искомый полный линейный оператор

В настоящей C²-карте (4) положим

```text
rho0=P/r, R_Q=Q(Delta0-epsilon0)^-1Q, ||R_Q||op<=2,
X_v={D,D_v},
Y_vw={D_v,D_w}+{D,D_vw}, W=rho0+kappa(Delta0).        (12)
```

`D_vw` включает кривизну native constraints, link/coefficient products,
observer-whitening и всю фактическую second jet карту. Ambient linear
подстановка вместо него незаконна. R_Q включает eigenvalues с обеих
сторон epsilon0 и обычно неопределён.

Пусть `Psi0=U/sqrt(r)`, `U:H_ref -> P H` — изометрия. Линеаризованное
matter уравнение и нормировка точно эквивалентны

```text
T(v)=P X_v P-Tr(P X_v)P/r=0,
dot epsilon=Tr(P X_v)/r,
dot Psi=-R_Q X_v Psi0+Psi0 A0, ReTr A0=0,
dot rho=S-R_Q X_v rho0-rho0 X_v R_Q,
S=P S P=S*, Tr S=0,
S=U(A0+A0*)U*/r.                                    (13)
```

Любой такой S реализуется `A0=(r/2)U* S U`. Произвольная
anti-Hermitian часть A0 также остаётся — `r²=16384` real reference/phase
направлений. Shell preparation Hessian равна нулю; её нельзя подменить
положительным faithful-AF density block или обратить по этой оценке.

Для **каждой** второй допустимой field variation w оставшаяся строка:

```text
H_red(v,w)+Tr_P[S T(w)]=0,
H_red(v,w)=Tr_H(W Y_vw)+Tr_H(Dkappa[X_v] X_w)
                    -(2/r) ReTr_H(P X_w R_Q X_v P).  (14)
```

Первый член — полный direct source/constraint curvature. Второй
содержит normalizer (11). Третий — ровно исключённая физическая
off-shell matter, не весь спектральный action и не fitted source.
Вывод: дифференцируем исходную field row `Tr[(rho+kappa)X_w]=0` и
подставляем (13). На истинной critical point Hessian карты симметрична.
Поэтому полный coupled kernel, с сохранёнными vertical направлениями, есть

```text
       [ H_red  T* ] [ v ] = 0,
       [ T       0 ] [ S ]                           (15)
```

В конечномерной карте эквивалентный тест полевого направления:

```text
v in ker T and H_red(v,w)=0 for EVERY w in ker T.     (16)
```

Тогда остаток field row лежит в `range T*=(ker T)^annihilator`, и S
восстанавливается, возможно с неоднозначностью ker T*. Это решение
остающейся preparation row, а не назначение внешнего source. Условие
`H_red(v,v)=0` необходимо, но само по себе недостаточно. Положительная
вторая вариация старой row-wave исключает именно то v; другая совместная
скорость может включать все link/observer/preparation направления (5).

### Translation decomposition сохраняет весь shell

Translation invariance корня разбивает (15) по Fourier q. Shell condition
может связывать только `q in Omega-Omega`. При L=8 это ровно33 частоты:
0, восемь `+/-2e_r` и24 `+/-e_r+/-e_s`, r<s. Это support identity,
не отсечение физического spectrum. Для других q имеем T_q=0 и
`(T* S)_q=0`, поэтому нужно решить **всю** field matrix `H_q v_q=0`.
Для остальных33 частот shell matrix S сохраняется полностью.
Например `(3,3,0,0)` лежит вне разностного множества; никакой shell
density tangent не исправит его ненулевые field rows. На этой частоте
осталась полная19-параметрическая native field matrix, а не scalar test.

## 6. Проверки и следующий решаемый объект

[kernel_check.py](sources/d0_native_joint_kernel_2026-10-16/kernel_check.py)
проверяет тождества на самостоятельном exact rational fixture той же
семьи цены. Это C4 identity fixture, не замена full16/L8 носителя.
Его исходная normalized complex-amplitude Jacobian имеет размер33x33,
reduced KKT —19x19; точная эквивалентность ядер включает четыре
anti-Hermitian vertical направления. Ненулевые CY, shell S, оба знака
R_Q, global normalizer и nonlinear moving G проверяются отдельно.
Ожидаемые mathematical evidence не переписываются. Изменённый fixture
исполнил286 exact checks; normal/optimized scientific JSON совпал.
Это проверка общей формулы, а не вычисление оставшегося native kernel.

[native_chart_check.py](sources/d0_native_joint_kernel_2026-10-16/native_chart_check.py)
проверяет actual Lorentz/positive intersection, регулярную карту и её
Fourier basis. Его рациональная frame fixture не называется новым root.
Ранг basis объясняется (3)–(5), а не экстраполяцией численного rank test.
Исполнены51 проверки; общий вход
`certificates/a4d_native_joint_kernel_check.py` дал одинаковый JSON в normal
и optimized режимах. [Validation](sources/d0_native_joint_kernel_2026-10-16/VALIDATION.json)
сохраняет точные source pins, окружение и области этого запуска. Старые
suites, root solve, evidence generators и Lean здесь не запускаются.

Дальнейший конкретный объект — сборка и решение матрицы (14) на полной
карте (5), с удалением только **доказанных** representation symmetries.
Для частот из shell difference set решается весь saddle block (15).
Нелинейное продолжение требует решения оставшихся E/field equations
(9); их local inverse, неплоский root и refinement-uniform estimates
этой редукцией не получены. Исходный fixed-source/raw,l1 terminal,
physical primitive/price admission и полный вывод ОТО остаются OPEN.
