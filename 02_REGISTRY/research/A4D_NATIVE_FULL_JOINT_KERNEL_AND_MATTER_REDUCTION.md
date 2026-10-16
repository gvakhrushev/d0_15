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
внеспектрального amplitude-блока. Полный19-столбцовый полевой символ
на `(3,3,0,0)` решён: инерция12+/1−/6zero, дополнительные нули отсутствуют.
Все ненулевые shell-transfer моды решены в §8: все matter compatibility
rows и reduced density/field saddle blocks классифицированы; непустые
стационарные density families сохранены. §9 замыкает нулевой блок и
локальную однородную critical family: семь Gram directions положительны,
три дополнительные Lorentz-metric directions сохраняются. §11 решает
все остальные Fourier блоки и классифицирует полный близкий faithful
critical locus: он исчерпывается плоской family. Неплоский совместный root, физический допуск программы,
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

## 6. Явная сборка полной Fourier матрицы из первых jets

Ниже используется именно homogeneous root и его maximally mixed shell,
не произвольная точка области (6). Пусть `t_r(k)=exp(2pi i k_r/8)`,
`z_r(k)=t_r(k)-1`, `C(a)` — full16 creator и `iota(a)=sum a_j C_j*`
— **complex-linear** contraction. Для native v_q из (5) положим
`a_r=dot u_r`, `Omega_r=Gamma(diag(0,W_r))`. Тогда ordered operator jet:

```text
A_v(k)=ell^-1 sum_r [z_r(k) C(a_r)+t_r(k) C(u_r) Omega_r],
J_v(k)=(D_v)_(k+q,k)=A_v(k)+A_(bar v)(k+q)*,
X_v(k)=D_(k+q) J_v(k)+J_v(k) D_k.                    (17)
```

В adjoint члене incoming momentum — **k+q**, не k. Эквивалентная
формула J содержит `bar z_r(k+q) iota(a_r)-bar t_r(k+q) Omega_r iota(u_r)`.
При прямом чтении stored backward leg она равна
`(bar t_r(k)-1)iota(a_r)-bar t_r(k+q)iota(u_r)Omega_r`;
равенство использует actual `W_r u_r=(1-t_r(q))a_r`, включая time leg.
Coefficient, exterior return и shift не коммутируются.

### Почему здесь можно сократить только constraint-curvature часть

В данном root `W(k)=chi_k I16`,
`chi_k=1_Omega(k)/128+kappa(lambda_k)`, `chi_-k=chi_k`.
Все десять homogeneous metric Euler rows и invertible frame дают

```text
sum_k chi_k Re[bar z_s(k) z_r(k)]=0  for all r,s.
```

Parity обнуляет imaginary parts, поэтому это комплексное moment
равенство. Тождество `Re z_s=-|z_s|²/2` также даёт

```text
sum_k chi_k bar z_s(k)=0,
sum_k chi_k t_r(k) bar z_s(k)=0  for all r,s.          (18)
```

Каждый actual mixed second jet literal d имеет диагональный Fourier вид
`ell^-1 sum_r[z_r(k) C(b_r)+t_r(k) T_r]`, где b_r — действительный
second coefficient jet, а T_r — независимая от k матрица Fock-grade +1.
В неё входят все coefficient/link products и accelerations карты (4).
Полный CAR trace с D_k видит только creator projection T_r: для
`T` степени+1 существует `p_j=Tr16(C_j* T)/8`, и
`Tr16(D_k T)=8 sum_j bar u_j(k) p_j`, где
`u(k)=ell^-1 sum_r z_r(k) u_r`. Поэтому (18) доказывает точно

```text
Tr_H W {D,D_vw}=0.                                  (19)
```

Здесь использованы реальные stationary metric rows, parity, полный Fock
trace и mixed q/−q support. Это не ambient правило для другой точки,
не удаление Y из (14) и не новая предпосылка о GL-link admission.
**Член `Tr W{D_v,D_w}` остаётся.** Общий finite fixture в §12 специально
показывает ошибку удаления Y без условий этого доказательства.

### Конечная Gram-sum формула

Для ненулевого q положим `l=k+q`, `rho_k=1_Omega(k)/128`,
`r_k=0` на Omega и `r_k=(lambda_k-epsilon0)^-1` вне shell.
При w на частоте −q полная bilinear matrix из (14) равна

```text
H_q(v,w)=sum_ALL_k (chi_k+chi_l) tr16[J_v(k) J_w(l)]
 + sum_ALL_k [f_Z^[1](lambda_l,lambda_k)-rho_k r_l-rho_l r_k]
                                   tr16[X_v(k) X_w(l)]. (20)
```

`J_w(l)` переводит l обратно в k; при `w=bar v` это adjoint J_v(k).
Для обычной coefficient convention `c* H c` элемент `H_ij` записывается
с `tr(J_i* J_j)` и `tr(X_i* X_j)`; это транспонирует bilinear indices
в (20), сохраняя ту же Hermitian quadratic form и инерцию.
Суммы идут по всем4096 k, trace — по всем16 Fock components. Divided
differences берутся с **полным** `Z=16 sum_k B(lambda_k)^m`, включая
нулевой mode, reference и feedback factors в kappa. При `q!=0` оба
`Tr(g X_v)` и `Tr(g X_w)` нулевые по Fourier support, поэтому именно
rank-one contraction из (11) отсутствует в (20). Для `q=0` он должен
быть добавлен; (11) сохраняется в общем операторе. Для реальной пары
`v_q+bar v_-q` contraction удваивается; cosine amplitudes имеют свои1/2.

Таким образом оставшаяся19x19 Hermitian matrix при `(3,3,0,0)`
задана конечной формулой через19 basis columns (5) и actual full16
first jets. Большая dense amplitude matrix для её сборки не нужна.
Формула (20) также определяет аналитическое продолжение на весь owned
root rectangle; со всей stationary Hessian оно совпадает именно в
истинном корне по (18)–(19). Округлённый центр прямоугольника сам по
себе не объявляется точным stationary root.

Три nu-направления при фиксированных u,O имеют J=0. Три совместных
local spatial frame rotations S имеют
`a_r=S u_r`, `Omega_r=(1-t_r(q))Gamma(S)` и точно
`J_v(k)=Gamma(S)D_k-D_l Gamma(S)`.
Они вместе с соответствующей matter variation дают representation
symmetries этой цены. Это предоставляет шесть обязательных Ward-направлений
для контроля сборки; нельзя объявлять все независимые edge angles gauge.
Для physical admission/quotient остаются прежние отдельные требования.

## 7. Решение полного символа на q=(3,3,0,0)

### Результат на исходном полном носителе

В истинном homogeneous v8 stationary root полная19-столбцовая
coframe/link/observer matrix на q=(3,3,0,0) имеет комплексную инерцию

```text
positive=12, negative=1, zero=6.                     (21)
```

Шесть нулевых направлений — ровно три observer-frame directions и три
совместных spatial frame directions, доказанных выше. Дополнительного
field kernel в этой моде нет. Для действительной пары q/−q соответствующие
числа равны24/2/12 на38 реальных field coordinates. Это утверждение о
полном линейном символе данной конечной условной цены; отдельно хранимые
affine-shift rows, reference verticals и остальные Fourier q не включены
в число19. Оно не устанавливает physical gauge admission и не доказывает
устойчивость корня: отрицательное направление сохранено.

[Численная диагностика](sources/d0_native_joint_kernel_2026-10-16/full_symbol_diagnostic.py)
собрала все4096 momentum blocks размером16. После трёх тождественно
нулевых observer columns и проверки трёх spatial Ward rows оставшееся
13-мерное ограничение имеет численные eigenvalues от−0.1579467 до931.5811;
минимальное положительное —0.00516478. Эти числа зависят от нормы
коэффициентов карты; доказательство (21) не использует их как строгие
eigenvalue bounds.

### Строгое сравнение на всём исходном прямоугольнике

[full_symbol_interval.py](sources/d0_native_joint_kernel_2026-10-16/full_symbol_interval.py)
использует произвольную фиксированную16x13 матрицу B из конечных
десятичных комплексных чисел. Numerical eigensystem лишь выбирает B;
его корректность не принимается как предпосылка. В опубликованном
[результате](sources/d0_native_joint_kernel_2026-10-16/FULL_SYMBOL_Q3300.json)
сохранены все208 комплексных элементов B, исходные d/o intervals и
каждый член оценки. Для S=diag(−1,+1,...,+1) проверено

```text
sup_theta ||B* H_formula(theta) B - S||_op
 <= max_i sum_j |(B* H_formula(theta) B - S)_ij|
 < 0.000269 < 1.                                    (22)
```

theta пробегает **весь** прежний root rectangle d/o radius10^-12.
При изменении theta изменяются a,b и все16 столбцов native chart;
заморожен лишь произвольный B. Все4096 modes,16 Fock components,
128 reference states, полный Z и signed negative-ground resolvent
сохранены. Равные энергии определяются exact Q(sqrt2) feature equality;
624 таких directed edges используют аналитическую производную.
Для остальных features interval denominator отделён от нуля
более чем0.21296462476181. Нового root solve не выполнялось.

Для полноты привожу перенос ошибок. Для a=J,X обозначим точные
dyadic floating references через Atilde_ai(k), веса через wtilde_a(k),
а строгие upper bounds через

```text
n_ai >= ||Atilde_ai||_HS,
e_ai >= sup_theta ||A_ai(theta)-Atilde_ai||_HS,
delta w_a >= sup_theta |w_a(theta)-wtilde_a|,
W_a >= sup_theta |w_a(theta)|.
```

Ошибка каждого matrix entry ограничена суммой

```text
R_ij + sum_(a,k) [delta w_a n_ai n_aj
                 +W_a(e_ai n_aj+n_ai e_aj+e_ai e_aj)]. (23)
```

R включает complex Gram summation roundoff. Scalar weights и moving
phase coefficients вычислены направленной80-digit interval arithmetic.
Точный корень восьмой степени единицы отдельно сравнивается с его binary64
представителем интервальной оценкой; максимальная комплексная ошибка
`6.835808657661923e-17`. Её вклад явно добавлен в bounds J и D через
не масштабированные суммы норм коэффициентов; он отделён от gamma-оценки
операций float-сборки. Геометрическая оценка J — triangle bound девяти
phase coefficients, включая root-box conversion error. Для X использовано точное CAR равенство
`||D_k||_op=sqrt(lambda_k)` и splitting
`D_true(J_true-J_float)+(D_true-D_float)J_float`; products и sums
floating assembly также включены. Для финального Gram использована
консервативная ошибка `2 gamma_(2^26)`, gamma_n=n*u/(1−n*u),u=2^-53.
Положительные budget sums имеют собственную outward rounding margin;
нет предположения, что обычный double результат сам является interval.
При IEEE binary64 arithmetic без overflow, проверяемых bounds факторов
и явно покрытых subnormal contributions получено (22).

Матрица в (22) Hermitian, поэтому operator norm ограничена maximum row
sum; непрерывный путь от S к ней не пересекает нулевой eigenvalue.
Инерция13-мерного ограничения равна12/1 на всём прямоугольнике.
В истинном stationary root три точных независимых spatial Ward vectors
добавляют kernel dimension>=3 к16-мерной матрице; nonsingular13 restriction
даёт rank>=13, откуда rank=13 и kernel dimension=3. Три observer zeros
завершают (21). **Ровно шесть нулей утверждаются в stationary root**,
а не в произвольной нестационарной точке прямоугольника.

Так как q лежит вне Omega−Omega, T_q=0; shell density tangent не может
добавить missing field row на этой частоте. Поэтому scalar row-wave
obstruction усилено до полного statement: никакая дополнительная
coframe/link/observer скорость этой моды не является совместным
stationary tangent. Это не запрет нелинейных решений с другими модами
и не решение всех saddle blocks (15).

## 8. Все ненулевые shell-transfer моды: решение matter compatibility rows

Для q=(2,0,0,0) ровно одна ordered shell pair имеет l=k+q:
`k=−e0,l=+e0`. Для q=(1,1,0,0) их ровно две:
`−e0 -> +e1` и `−e1 -> +e0`. Здесь T(v) — стек всех full16 blocks
`X_v(k)` этих пар, без удаления matrix entries. Его комплексные target
dimensions равны256 и512; trace condition автоматически выполнено при
ненулевом q. Ни одна shell density direction заранее не отбрасывается.

### Точные ранги, а не численная экстраполяция

Если роль r неактивна (`q_r=0`), то её coefficient jets имеют J=0
между указанными occupied endpoints, поскольку `k_r=l_r=0`.
Это shell invisibility именно coefficient jet, а не его исчезновение
на полном thermal spectrum; её stabilizer angle может давать T!=0.

На q2000 три active-role0 coordinates совпадают с local SO(3) variation
`S=Omega0/kappa0` с точностью до shell-invisible inactive coframe jets.
У Ward jet `P[Gamma(S),Delta]P=0`, поэтому T видит только три inactive
stabilizer angles. Следовательно rank T<=3. На q1100 шесть active
coordinates содержат трёхмерный common spatial Ward subspace; остаются
не более трёх relative-active образов и два inactive stabilizers,
откуда rank T<=5.

[shell_transfer_reduction.py](sources/d0_native_joint_kernel_2026-10-16/shell_transfer_reduction.py)
дополняет эти upper bounds явными ненулевыми minors на **всей** области
`a>b>0`. Номера ниже zero-based, columns — исходный native basis (5),
entries — row-major full16 matrix. На q2000 columns(7,12,17),
entries(3,5,6) единственного block дают

```text
det = 2^19 [(1−sqrt2)+i(−3+2sqrt2)] b^5(a−b)^4 !=0. (24)
```

На q1100 columns(0,1,2,10,15), entries(0,3,5,6,36) первого block дают

```text
det = C b^5(a−b)^4 Q(a,b),
C = (2^32/3)[55−39sqrt2+i(65−46sqrt2)],
Q = b²+[(16−15sqrt2)+i(36+39sqrt2)]ab/97
       +[(27+5sqrt2)−i(12+13sqrt2)]a²/97.           (25)
```

`Im Q=(12+13sqrt2)a(3b−a)/97`. Если imaginary part нулевой при a>b>0,
то a=3b, где Q=4b²>0. Поэтому (25) не обращается в нуль нигде в этой
области, включая настоящий root. Полные exact ranks T равны3 и5.
Положительный рациональный fixture не используется вместо этого довода.

### Все допустимые первые поля после shell equations

На q2000 native field dimension21, ker T dimension18. На q1100 они
равны19 и14. В обеих модах сохраняются три observer directions и три
common spatial representation directions. Их complement в ker T состоит
**ровно** из произвольных inactive-role coefficient jets:

```text
q2000: delta u1,delta u2,delta u3 in C4, dimension12;
q1100: delta u2,delta u3 in C4, dimension8.          (26)
```

У этих представителей active legs и links нулевые как **следствие T=0
и выбора представителя modulo доказанные Ward directions**. Это не
заморозка независимых link variations. Полнота (26) следует из точных
размерностей: pure inactive jets имеют T=0 и не пересекают representation
subspace, поскольку нулевой active-link component заставляет S=0.

Metric images (26) имеют размер9 и7: active-active entries delta q
нулевые. На q1100 matter equations дополнительно навязывают
`delta q01=0` наряду с уже stored conditions `delta q00=delta q11=0`.
Три/одно metric-invisible coefficient directions при этом **сохранены**
в12/8-dimensional field space, а не объявлены physical gauge.

Полная система (15) теперь требует решить H_red на (26), затем вернуть
shell multiplier из `T* S=−H_red v`. Если restricted H невырождена,
то допустимы лишь field representation velocities; S остаётся в
`ker T*`, dimensions253 и507 **комплексных** плотностных направлений
соответственно. Они не равны anti-Hermitian purification verticals и не
называются gauge. Эти S реализуются положительными малыми изменениями
`tau=P/128+S` при фиксированном поле, поскольку оставшиеся field equations
линейны по tau. На q/−q реальная размерность этой семьи удваивается.

Для (26) ordered jet особенно прост: для inactive r имеем t_r(l)=t_r(k),
`J=8 sum_r[(t_r(k)−1)C(delta u_r)+(bar t_r(k)−1)iota(delta u_r)]`.
Ни один full4096 thermal block и matter-resolvent term из (20) не удаляется.
[Численная сборка](sources/d0_native_joint_kernel_2026-10-16/full_shell_transfer_diagnostic.py)
выбирает preconditioners для12x12 и8x8 restrictions. Их строгая
[интервальная проверка](sources/d0_native_joint_kernel_2026-10-16/full_shell_transfer_interval.py)
по той же оценке (23) сохраняет движение D, все веса, coefficient/phase
conversion и complex assembly/Gram roundoff. J на (26) не зависит от
root parameters, но полный D и все scalar weights зависят. Получено
на **всём** исходном root rectangle:

| q | dim restriction | positive/negative/zero | distance to signature upper |
| --- | ---: | --- | ---: |
| (2,0,0,0) | 12 | 9 / 3 / 0 | 5.853e-6 |
| (1,1,0,0) | 8 | 6 / 2 / 0 | 1.702e-5 |

Обе ошибки строго меньше1. Поэтому в этих двух модах полевая часть
совместного stationary tangent состоит только из шести доказанных
representation directions; preparation annihilators253/507 сохранены.

### Полный reduced density/field KKT, а не весь исходный amplitude Hessian

Пусть r_T=rank T, m=dim density target и (p,n) — инерция restriction
на (26). В (15) split `ker T=V+G`, где V=(26), dim G=6.
Если `H_red g` ненулевой вне ker T, он лежит в range T*, поэтому g
поднимается совместным S_g. Elimination невырожденного H_V оставляет
rank-r_T поле, сопряжённое с im T: его saddle block имеет инерцию
`(r_T,r_T,0)`. Density ker T* остаётся нулевым. По congruence полная
комплексная инерция reduced shell-density/field KKT равна

```text
(p+r_T, n+r_T, 6+m−r_T).
q2000: (12 positive,6 negative,259 zero), dimension277;
q1100: (11 positive,7 negative,513 zero), dimension531. (27)
```

Для реальной пары q/−q все числа удваиваются. В (27) **не включены**
исключённые Q-amplitude signs, отдельные purification/reference verticals,
affine-shift zero rows и q=0 epsilon/normalizer equations. Это точный
результат для оставшегося блока (15) после ранее доказанной полной
amplitude reconstruction, а не объявление исходного огромного Hessian
положительным или полностью классифицированным.

Единый новый [consumer](certificates/a4d_native_shell_transfer_check.py)
сводит exact rank theorem и interval restrictions; полный результат
с B, bounds и source hashes сохранён в
[SHELL_TRANSFER_SYMBOLS.json](sources/d0_native_joint_kernel_2026-10-16/SHELL_TRANSFER_SYMBOLS.json).
Остальные shell-transfer constraints решены ниже в §8.1; полный finite
field kernel и его нелинейный consumer завершены в §11.

### 8.1. Единое shell constraint и перенос двух решённых restrictions

Новый [shell_transfer_all_orbits.py](sources/d0_native_joint_kernel_2026-10-16/shell_transfer_all_orbits.py)
замыкает rank/kernel T сразу для всех ненулевых occupied-shell transfers.
С учётом spatial S3 и общей инверсии q это шесть представителей:
q2000,q0200,q1100,q1700,q0110,q0170. Отдельная time role не переставляется
как symmetry полного native SO(3) chart. Аргумент ниже действует при
всех a>b>0, а не только на одном rational fixture или decimal root.

Общее mean-slice разложение из §10 оставляет pure inactive coframes
плюс три inactive stabilizers при q=2e_i; при q=e_i+s e_j остаются
три relative-active angular coordinates и два inactive stabilizers.
Pure inactive coframes не видны occupied endpoints. Для q=2e_i
vacuum-to-bivector readouts stabilizers proportional к
`u_r wedge K_r u_i`, `K_r=diag(0,[w_r]_cross)`. Их minor строк01,02,12
равен `2 b^5(a−b)^4` как для i=0, так и для i=1. Это даёт rank3.

Для q=e_i+s e_j возьмём k=−e_i,l=s e_j, s=+/-1 и mean contrasts
`B_i=W,B_j=−W`. Буквальный stored ordered jet удовлетворяет

```text
J=Gamma(W)D_k+D_l Gamma(W),
T_W=2[D_l Gamma(W)D_k+epsilon Gamma(W)].
```

Здесь Gamma нельзя переставлять через D_k произвольно. Пусть
`t=exp(i*pi/4)`, `alpha=conj(t)−1`, `beta=t^s−1`. Полный scalar+bivector
vacuum readout, divided by64alpha и multiplied слева на
`diag(beta/conj(beta),1,...,1)`, справа на
`diag(1/(2beta),1/(2beta),1/(2beta),1,1)`, равен карте

```text
W -> (u_j dot W u_i, u_j wedge W u_i),
theta_r -> (0,u_r wedge K_r u_i).
```

Её minor строк scalar,01,02,12 и столбцов W0,W1,theta_r,theta_s равен
`+2 b^6(a−b)^4` для (i,j)=(0,1), `−2 b^6(a−b)^4` для (1,2).
Единственное ядро этой7x5 карты — W вокруг w_i, theta=0.
**Только на этом ядре** `W u_i=0`, поэтому `[Gamma(W),D_k]=0` и
`T_W=2(D_l D_k+epsilon)Gamma(W)`. Оставшийся множитель обратим:

```text
(D_l D_k+epsilon)* (D_l D_k+epsilon)
  =2 epsilon(epsilon+h) I16 >0,
h/epsilon=−o/(sqrt2*d) for s=+1, o/d for s=−1,
d=a²+3b², o=2ab+2b², d−o=(a−b)²>0.
```

Ненулевое Gamma(W) потому обнаруживается оставшимися full16 rows.
Это доказывает rank5, а полное mean-slice разложение даёт

| transfer | rank T | dim kerT modulo6 representations | dim kerT* |
| --- | ---: | ---: | ---: |
| +/-2e_i | 3 | 12 inactive coframes | 253 complex |
| +/-e_i+/-e_j, i!=j | 5 | 8 inactive coframes | 507 complex |

Большие численные rank tests здесь не нужны.233 exact checks нового
consumer включают actual21/19 chart columns, phase scaling и необходимый
restricted commutator. Normal/optimized outputs побайтно совпали;
[результат](sources/d0_native_joint_kernel_2026-10-16/ALL_SHELL_TRANSFER_RESULTS.json)
и [validation](sources/d0_native_joint_kernel_2026-10-16/ALL_SHELL_TRANSFER_VALIDATION.json)
сохраняют exact inputs. Сам consumer утверждает constraint rank, не
инерцию полевого гессиана.

Для **pure inactive-coframe restrictions** имеется дополнительная heat/CAR
конгруэнция, не symmetry полного admissible chart. Пусть P — любая
перестановка четырёх roles, `R=eta P eta`, `W=exterior(R)`, и A — матрица
coframe jets. Из `P U=U R` следует при `q'=Pq,A'=P A R^T`

```text
D(Pk)=W D(k) W*,
J_(Pq,A')(Pk)=W J_(q,A)(k) W*,
X_(Pq,A')(Pk)=W X_(q,A)(k) W*.
```

R — signed permutation, а W — ортогональное действие на **всех16**
exterior components, в том числе при detR=−1. Inactive support,
lambda_k, shell128, полный Z и scalar weights (20) сохраняются после
k→Pk. Поэтому `H_(Pq)(A',B')=H_q(A,B)`; изменение inactive coordinates
само является signed permutation, независимой от root. Старые interval
bounds переносятся на весь исходный root rectangle без новых запусков:

| новая q | restriction inertia | reduced complex KKT inertia | исходный bound |
| --- | --- | --- | ---: |
| (0,2,0,0) | 9+ /3− | (12,6,259) | 5.853e−6 |
| (0,1,1,0) | 6+ /2− | (11,7,513) | 1.702e−5 |

Не утверждается, что R — допустимый link/frame gauge: он используется
только для этих restrictions с zero link jets, чья полнота теперь
обеспечена отдельным rank theorem. Opposite-sign q1700 и q0170 также
конгруэнтны друг другу, но не приводятся к same-sign q1100 этим доводом;
их Hessian restriction требует отдельной решённой базы.

Эту базу теперь даёт единственный новый
[opposite_shell_transfer_interval.py](sources/d0_native_joint_kernel_2026-10-16/opposite_shell_transfer_interval.py).
Общий assembler §10 выбирает fixed decimal8x8 B на q1700, затем
неизменённые full16 geometry и arithmetic helpers независимо проверяют
конгруэнцию по всем4096 modes на всём исходном root rectangle. Новый
q-cache независимо содержит469 unordered feature pairs,560 exact-equal
directed edges и ровно две occupied transfers: `+e1 -> +e0` и
`−e0 -> −e1`. Точные равенства energies используют analytic derivative,
а не деление на малый interval. Full Z, feedback и оба знака matter R,
phase conversion, decimal B и floating/Gram budgets сохраняются.
Получено

```text
q1700: restriction inertia (6 positive,2 negative,0 zero),
distance from signature <9.467518e−5<1
throughout the entire owned root rectangle.
```

Нормальный и optimized JSON побайтно совпали. Полный
[результат](sources/d0_native_joint_kernel_2026-10-16/OPPOSITE_SHELL_TRANSFER_RESULTS.json)
и [validation](sources/d0_native_joint_kernel_2026-10-16/OPPOSITE_SHELL_TRANSFER_VALIDATION.json)
сохраняют B и все bounds. Signed permutation переносит ту же оценку на
q0170. Обе reduced complex KKT инерции равны(11,7,513) по (27).

Тем самым **весь ненулевой occupied-shell difference sector** решён.
Его field tangent состоит из шести доказанных representations;253/507
complex density annihilators сохраняются. За Omega−Omega T_q=0, и
остаётся complete field symbol §10. Теперь §11 решает также все эти
блоки одной общей outward оценкой; старый q1240 comparison сам по себе
остаётся отдельной проверкой сборки, а не заменой этой оценки.

## 9. Нулевой блок и точная однородная critical family

Здесь q=0 **вещественный**; density имеет восемь Hermitian16 momentum
blocks с одной общей trace constraint. Это2047 реальных координат,
не2047 комплексных. Отдельные reference-unitary verticals, affine shifts
и nonzero-q density blocks сохраняются за пределами этого счёта.

Пусть U — матрица, строки которой равны `u_r^T`, а
`G_E=U U^T`. Этот Euclidean Gram не отождествляется с Lorentz Gram
`g_L=U eta U^T`. При постоянных полях и identity links

```text
Delta_k=lambda_k(G_E) I16,
lambda_k=ell^-2 sum_(r,s) bar z_r(k) z_s(k) (G_E)_rs. (28)
```

Таким образом все4096 modes и16 Fock grades остаются, но однородный
coframe response скалярен на каждой fibre. Вариации P и Q не смешиваются;
`Q X P=0` во всём однородном секторе, включая link directions. Это точная
momentum-selection identity, а не замена signed resolvent положительным.

### Полный shell constraint имеет rank7

На shell `k=+/-e_r` имеем `X_k=gamma delta(G_E)_rr I16`,
`gamma=128−64sqrt2>0`. После удаления средней энергии coframe часть T0
имеет rank3: все четыре `delta(G_E)_rr` должны совпадать.

Четыре stabilizer-link variations имеют `S_r u_r=0`, где
`S_r=diag(0,xi_r[w_r]_cross)`. Их full16 shell blocks traceless,
поэтому они не могут сократиться со скалярной coframe частью. Если их
комбинация имеет T0=0, её vacuum-to-two-spatial-creation components дают

```text
(M−tr(M)I3) w_a=0 for a=1,2,3,
M=sum_r xi_r w_r w_r^T.                              (29)
```

Общий ненулевой scalar phase в каждом occupied block не меняет вывод.
Для `c=a−b>0`, `w0=−b*1`, `wi=−b*1−c*ei` determinant трёх spatial
legs равен `−c²(a+2b) !=0`, следовательно M−tr(M)I=0 и M=0.
Четыре readouts `M12−M13,M12−M23,M11−M12,M12` имеют determinant
`b^4 c^4>0` по xi0..xi3. Отсюда все xi нулевые. Это analytic rank4
на всей области a>b>0, с actual full16 CAR interpretation (29).

Итак, rank T0=7, ker T0 имеет dimension16:13 coframe directions с
равными diagonal Gram jets и3 observer directions; все link jets нулевые.
Остаются7 Gram directions,6 internal Euclidean-frame directions и3
observer directions. Density ker T0* имеет2040 реальных направлений.
[zero_mode_constraint_check.py](sources/d0_native_joint_kernel_2026-10-16/zero_mode_constraint_check.py)
проверяет actual CAR identity и малые analytic determinants; большая
2070-dimensional matrix для этого не нужна.

### Положительность семи Gram directions с полным normalizer

В (28) lambda линейна по всем10 symmetric slots G_E. Для вариации f_k
положим `e_k=B_k^m`, `w_k=16 e_k/Z`, `y_k=f_k/B_k`,
`A_k=1−z+z e_k`, `c_m=(m−1)alpha=beta(1−1/m)`.
Полный finite-power price Hessian равен точно

```text
F_price''[f,f] = c_m E_w(y²) − beta(E_w y)²
 − M beta z c_m Z E_w(y²/A)
 + M beta² z² Z E_w(e y²/A²).                        (30)
```

Здесь второй член — именно retained global-normalizer response. В отличие
от nonzero-q formula (20), он **не нулевой**. Matter price при identity
links линейна по G_E; её coupling к density остаётся в KKT через T0.

Ground mode даёт f0=0 и w0=16/Z. Weighted Cauchy на остальных modes:
`(E_w y)² <=(1−w0) E_w(y²)`. При `delta=M beta z Z/(1−z)` и A>=1−z
последний член (30) неотрицателен, поэтому

```text
F_price'' >= beta[w0−1/m−(1−1/m)delta] E_w(y²)
          > (3 beta/10) E_w(y²).                     (31)
```

Для этого используются actual interval Z<50, beta<1, M=128,z=2^-20,
m=16384: `w0>8/25`, `delta<6400/(2^20−1)<1/100`, `1/m<1/10000`.
Точный coarse gap `3099/10000` больше3/10; actual bracket на root
rectangle больше0.3196384165. Нулевой mode и его16-fold multiplicity
существенны для этой оценки. Это fixed-L8 bound, не refinement-uniform
estimate и не новое physical heat law.

Моды e_r и e_r+e_s определяют все10 Gram slots: их probe determinant
равен `64 gamma^10 !=0`. Следовательно (31) строго положительно для
любой ненулевой Gram variation, в частности для семи admissible
directions. [homogeneous_price_convexity.py](sources/d0_native_joint_kernel_2026-10-16/homogeneous_price_convexity.py)
сверяет (30) независимой symbolic derivative и подставляет native full-Z
intervals. Малый symbolic fixture проверяет формулу, не заменяет lattice.

### Девять field zeros и три дополнительные Lorentz-metric directions

Пусть R — **одна постоянная** SO(4) rotation всех coframes,
`u_r -> R u_r`, при observer e0 и links=I. G_E и каждый Delta_k точно
сохраняются; подготовка P/128 тоже может остаться прежней. Это допустимая
однородная field curve по (3), **не SO(4)-link variation**.

Restricted price invariance сама по себе не доказывает полной field
стационарности. Здесь недостающие строки проверяются отдельно:

```text
Tr16[C(u_r) iota(u_s) Gamma(S_r)]=4 u_s^T S_r u_r=0,
S_r u_r=0.                                          (32)
```

Поэтому все admitted homogeneous stabilizer-link source rows нулевые.
Coframe source moments зависят от того же G_E и остаются нулевыми;
ненулевые Fourier rows исчезают по translation invariance. Matter
equations сохраняются с тем же Delta и normalized full128 preparation.
Таким образом это точные joint roots полной объявленной v8 задачи,
стационарные и относительно неоднородных первых вариаций.

Пространственные SO(3) rotations уже входили в representation directions.
Ещё три directions меняют Lorentz Gram:

```text
g_L(R)=U R^T eta R U^T=−G_E+2(U n)(U n)^T,
n=R^T e0, n^T n=1.                                 (33)
```

Его differential имеет rank3; эти направления не лежат в шести ранее
доказанных representation directions. Они не отбрасываются как physical
gauge. Любой более широкий physical coordinate quotient требовал бы
своего admission theorem. Все метрики этой семьи постоянны и плоские;
неплоский или continuum Einstein root отсюда не следует.

Инерция реального reduced shell-density/field q0 KKT из (15) теперь

```text
(14 positive,7 negative,2049 zero), dimension2070.   (34)
```

Это7 положительных Gram directions, rank7/7 saddle pairing и9 field
zeros плюс2040 density annihilators. В отличие от q/−q в §8, эти числа
**не удваиваются**. Excluded Q-amplitude/reference/affine components
перечислены выше; полный исходный amplitude Hessian не классифицирован.

### Локальная нелинейная классификация однородных roots

В достаточно малой окрестности рассматриваются translation-invariant
fields и translation-invariant reduced density. Для любых homogeneous
links P и Q не смешиваются по momentum, поэтому matter equation равна
`E=P Delta P−epsilon P=0`. Её derivative имеет8 независимых normal rows:
четыре link angles, три diagonal Gram differences и `e=epsilon−gamma*d`.
Здесь d — свободная общая диагональ, так что именно e, а не epsilon,
является normal coordinate с нулевым значением. Когда link
angles и diagonal differences нулевые, epsilon=gamma*d решает все E
тождественно при произвольных остальных coordinates. IFT для этих
выбранных8 строк поэтому заставляет любой близкий full solution иметь
именно links=I и G_E диагональ d*I. Остальные matter rows не удаляются:
они автоматически выполнены на найденном normal-zero solution.

Пусть m_r — суммарная density mass пары +/-e_r, sum m_r=1. Coframe
Euler rows дают6 off-diagonal уравнений F_price и4 diagonal equations
`partial F_price/partial(G_E)_rr+gamma*m_r=0`.
Их сумма и шесть off-diagonal rows — critical equations для
`V(d,offdiag)=F_price(G_E diag=d)+gamma*d`. Из (31), по continuity в
малой convex neighbourhood с Z<50 и B>0, V строго convex. Существующий
G_E* потому является единственным близким critical Gram. Individual
diagonal rows затем задают m_r=1/4; четыре link rows линейны по density.

При фиксированном coframe/observer admissible densities образуют открытую
положительную часть affine fibre dimension2040. Rank7 сохраняется в
окрестности по найденному ненулевому minor. В частности P/128 является
положительной точкой fibre для всей SO(4) orbit по (32). Получается
локальная гладкая critical family dimension `6+3+2040=2049` в данном
translation-invariant density/field sector. Все её точки стационарны
против полных local first variations по translation invariance. Другие
nonzero-q density fibres и reference unitaries этим не исключены.

Это точная локальная однородная классификация условной цены, а не
физический выбор из семейства (33). Она меняет следующий consumer:
native preparation/observer pullback должен быть получен из actual D0
transition; positive heat geometry не выбирает Lorentz Gram сама.

### Actual native memory не снимает эти три Lorentz-Gram направления

Новый [memory-source owner](A4D_NATIVE_MEMORY_SOURCE_FIBRE.md) сохраняет
ту же full-price задачу и actual closed engine. Его собственная whole-blank
орбита лежит в SO(3)-fixed sector
`E0=span{1,e0,e1 wedge e2 wedge e3,volume}` полного16 carrier. Для её
нормированной sigma_j имеем `Gamma(S)sigma_j=sigma_j Gamma(S)=0`
при любом spatial S. Это не замена full16 operator четырьмя компонентами.

Зафиксируем любую из этих sigma_j и подготовку
`rho_j=P_Omega/8 tensor sigma_j` (rank8, reference всё ещё128).
Для **каждого** близкого constant SO4-coframe R из (33), observer e0 и
identity links остаются joint roots с той же rho_j. Matter equation
сохраняется, поскольку весь occupied block равен epsilon I16, а coframe
jets Delta скалярны и зависят только от неизменного G_E. Для любого
homogeneous admitted stabilizer S_r u_r=0 actual ordered link jet равен

```text
J_r(k)=8[t_r C(u_r)−bar(t_r) iota(u_r)]Gamma(S_r).
```

Здесь Gamma(S_r) коммутирует с обоими own-leg operators; поэтому
`J_r sigma_j=sigma_j J_r=0` и весь matter link source
`Tr sigma_j {D_k,J_r(k)}` нулевой. Heat/feedback source по-прежнему
нулевой по (32); неоднородные first rows исчезают по momentum trace.
Одновременное exterior-eta изменение convention сохраняет E0 и этот довод.

Таким образом даже **фиксированная actual native memory preparation**
не выбирает Lorentz Gram из (33) в объявленной условной цене. Нужен
дальнейший native joint transition/action/readout consumer. Существование
этой rank8 family не переносит real inertia (34) или локальную полноту
faithful density classification на boundary низкого ранга: там сохраняется
rank-free equation `E C0=0`, а не автоматически E=0.

## 10. Общая сборка ненулевого символа через257 фазовых моментов

Следующий consumer — общий inverse/kernel estimate оставшихся неоднородных
блоков (15), а не независимый каталог численных ranks. Новый
[nonzero_symbol_algebra.py](sources/d0_native_joint_kernel_2026-10-16/nonzero_symbol_algebra.py)
собирает любой q!=0 на том же полном native carrier, сохраняя все члены
(20). Он заменяет повторное умножение4096 полных16x16 matrices конечной
Clifford/Laurent algebra; исходный action или набор вариаций не меняется.

### Полный явный quotient без подобранного projector

Пусть I={r:q_r!=0}, p=|I| и kappa_r=1−t_r(q). На active legs положим
`B_r=Omega_r/kappa_r`, `a_r=B_r u_r`. Общая spatial representation
добавляет один S ко всем B_r и `S u_r` к inactive a_r. Единственный
представитель с `sum_(r in I) B_r=0` получается вычитанием среднего.
Три компоненты каждого из p−1 contrasts `B_r=e_j,B_last=−e_j`
дают весь active complement. На каждом inactive leg остаются четыре
произвольных a_r и stabilizer `Omega_r=theta_r[w_r]_cross`. Поэтому

```text
dim field quotient = 3(p−1)+5(4−p)=17−2p.           (35)
```

Три observer directions уже выделены как representation zeros. В (35)
удалены только доказанные spatial representations; matter со-преобразуется
при переходе к этому представителю. Это не новый physical gauge theorem.
Контрастная параметризация не делит на kappa; обратное восстановление
из исходного jet делит. На фиксированном L8
`|kappa_r|>=sqrt(2−sqrt2)` для active r; refinement-uniform bound этим
не установлен. При self-conjugate q real dimension (35) не удваивается.

### Точное сокращение операторов, сохраняющее full16 trace

Восемь Majorana generators задают256 ортогональных Clifford monomials:
`Tr16(A*B)=16 sum_I conjugate(a_I)b_I`. Для J достаточно64 coefficients
степеней1,3; для X —99 coefficients степеней0,2,4. Это координаты
полных операторов на всех16 Fock components, а не ограничение материи.

J имеет девять Laurent phases `0,+/-e_r`. У X потенциальные `+/-2e_r`
сокращаются **точно** по CAR и own-leg transport. Например, creator
коэффициент proportional к
`t_r(q) C(u_r)(C(a_r)+C(u_r)Gamma(Omega_r))`
`+(C(a_r)+C(u_r)Gamma(Omega_r))C(u_r)` равен нулю из
`Omega_r u_r=kappa_r a_r`; inactive case следует из stabilizer equation.
Численный threshold для удаления coefficients не используется. Остаются

```text
supp X subset {0,+/-e_r,+/-e_r+/-e_s:r<s}, size33;
|(supp X)−(supp X)|=257.                            (36)
```

Взвешенные Gram sums в (20) теперь являются contractions этих
coefficients с257 exact-phase moments весов X и соответствующими
моментами J. Scalar weights по-прежнему используют все4096 momenta,
full Z, feedback, signed matter resolvent и occupied reference128.
Весь спектр имеет119 exact Q(sqrt2) features. Различные features
интервально отделены на полном исходном root rectangle более чем
0.0035540733963332876;7140 общих scalar divided differences, включая
analytic diagonal values, переиспользуются для всех q.

Только при stationary moments (18) J-часть дополнительно сводится к

```text
H_J(v,w)=sum_k chi_k *
 [Tr16 J_v(0)*J_w(0)+Tr16 J_v(−q)*J_w(−q)].         (37)
```

Creator/annihilator cross traces исчезают по Fock charge; оставшиеся
phase differences —0,+/-e_r,e_r−e_s, чьи chi-moments равны sum chi.
По умолчанию API считает полный weighted J Gram. Вне stationary root
он даёт first-jet block (20), а полный constrained Hessian дополнительно
требует `Tr W{D,D_vw}`; shortcut (37) там не применяется. Даже при root
на q in Omega−Omega необходимо отдельно наложить T=0 и вернуть density
rows: общий assembler сам их не удаляет и не решает.

Новая проверка q=(1,2,4,0), dimension11, сравнивает **всю** матрицу с
независимой full4096x16 сборкой. Maximum entry error <1.6e−13 для
weighted и stationary-two-point вариантов. Точные CAR, generic
same-axis cancellation и arbitrary-kappa quotient identities проверены
отдельно. Hostile nonstationary fixture отвергает (37), сохраняя полный
weighted Gram. Численный положительный спектр новой частоты сам по себе
не является interval inertia certificate; общий строгий inverse дан в §11.

Численный `owned_root_center` в API не доказывает exact stationarity:
(37) используется как аналитическая гипотеза истинного root, а finite
comparison исполняется на его указанном decimal centre. Возвращённый
H_q — complex symbol; real block пары q/−q получается realification
с сопряжённой базой. У self-conjugate q берутся только real amplitudes.

## 11. Полный конечный inverse и локальная классификация joint roots

Оставшаяся полевая задача теперь решена на **всём** исходном root
rectangle. Новый [общий validator](sources/d0_native_joint_kernel_2026-10-16/uniform_symbol_bounds.py)
проверяет fixed decimal square B для каждой из483 disjoint spatial-S3/
global-negation classes вне Omega−Omega. Они покрывают все4063 частоты;
размерность полного real quotient равна40511. Численный выбор B
сохранён отдельно в [FIELD_INVERSE_CHOICES.json](sources/d0_native_joint_kernel_2026-10-16/FIELD_INVERSE_CHOICES.json)
и сам доказательством не является.

### Одна общая outward оценка вместо повторных full16 matrix runs

Все119 feature energies и7140 scalar pair weights из (20) заключаются
в интервалы один раз. У каждого q exact feature indices дают все4096
outgoing pairs;41 J-moments и257 X-moments собираются независимо.
Signed ground resolvent, full Z, feedback и reference128 сохранены.
Матрица B объявлена точной finite-decimal complex matrix; native
coefficient formulas, a/b root variation, kappa phases и conversion
в binary64 охвачены interval scalar arithmetic и Clifford norm bounds.

Для каждого preconditioned coefficient column положим
`c_i=sum_phase ||x_i,phase||_2` и пусть e_i — верхняя граница aggregate
coefficient error. Для moment reference максимум M и error deltaM
получена entrywise ошибка

```text
16[deltaM*c_i*c_j+(M+deltaM)
   *(e_i*c_j+c_i*e_j+e_i*e_j)].                     (38)
```

Она включает все cross terms. Умножение degree-one Clifford operator
имеет норму `||D J||_2<=||D||_1||J||_2`; это позволяет ограничить X
без повторного формирования4096 матриц16x16. Exact cancellation (36)
сохраняется для любой точной B, численный sparsity threshold не применяется.
Phase conversion и moment summation покрываются отдельно; compressed
33x33x99 Gram имеет дополнительный бюджет `2 gamma_(2^22)` на entry.
Positive majorant sums вычисляются outward по неизменённой arithmetic
библиотеке. Строгая проверка каждой матрицы даёт

```text
||B_q* H_q(d,o) B_q−S_q||_op <=delta_q,
max_q delta_q <0.001184<1,                         (39)
S_q diagonal with entries +/-1.
```

Самый большой bound равен0.0011831559043778055 на q=(0,0,3,4).
Оценка row sum контролирует operator norm **точной Hermitian matrix**;
временный float reference не объявляется Hermitian без error budget.
На прямоугольнике проверяется analytic extension (20); её равенство
native Hessian и точные representation kernels утверждаются в истинном
stationary root по прежней curvature lemma, не по rounded centre.

Spatial permutations сохраняют observer time role. Их internal O(3)
matrix, включая det−1, нормализует admitted SO(3), действует на angular
vectors как axial `det(R)R`, а на inactive stabilizer coordinate даёт
соответствующий знак. Поэтому это точная congruence полного данного
conditional chart; перестановка time/spatial roles здесь не используется.
Mean-slice contrasts переставляются через полный zero-mean active tuple.
Если p — число active roles, то
`||x||²<=sum_r||B_r||²<=p||x||²`, так что оба contrast-coordinate maps
имеют норму<=sqrt(p), p<=4. Общая инверсия q даёт complex conjugation.
У self-conjugate q real amplitudes считаются один раз.

Из (39) B_q обратима, и inverse конструктивно задан Neumann series

```text
E_q=B_q* H_q B_q−S_q,
H_q^{-1}=B_q sum_(j>=0)(−S_q E_q)^j S_q B_q*.
```

Во всех canonical mean-slice Fourier coordinates, включая condition p
при переносе orbit, получена строгая integer bound
`||H_q^{-1}||<=1094698`. Integer ceiling вычислена из точных dyadic
outward bounds без округляющего float multiplication. Это fixed-L8
coordinate norm, **не** refinement-uniform estimate и не исходный raw,l1
metric-response norm.

Новый [entrypoint](certificates/a4d_native_field_inverse_check.py) прошёл
в normal/optimized режимах с побайтно одинаковыми483 orbit records.
[Полный результат](sources/d0_native_joint_kernel_2026-10-16/FIELD_INVERSE_RESULTS.json)
и [validation](sources/d0_native_joint_kernel_2026-10-16/FIELD_INVERSE_VALIDATION.json)
сохраняют все row bounds, exact B и input hashes. После этого исправлена
только integer composition общей norm-bound: оба режима повторили её
на тех же483 проверенных records, без matrix replay. Исходный полный
execution закреплён отдельным Git checkpoint в validation.

### Весь reduced kernel и его нелинейный consumer

Вне Omega−Omega real field quotient имеет инерцию39241+/1270−/0.
Добавляя уже решённые q0 и все shell saddle blocks, получаем **полную**
real reduced density/field KKT инерцию

```text
(39615 positive,1493 negative,40811 zero),
domain dimension81919, normal rank41108.            (40)
```

Числа (40) не включают reference-unitary verticals, исключённые Q
amplitudes или отдельно хранимые affine shifts. Density Herm128
tracezero dimension16383, rank всего T равен
`7+4*2*3+12*2*5=151`, поэтому density annihilator имеет16232 real
dimensions. Их не отбрасывают как gauge.

[Полное аналитическое следствие](sources/d0_native_joint_kernel_2026-10-16/LOCAL_CRITICAL_LOCUS_CONSUMER.md)
использует настоящий smooth reduced functional, а не только nullity.
При sigma>0, Tr sigma=1 уравнение `Tr sigma E(x,epsilon)=0` задаёт
epsilon_hat по derivative `−Tr sigma G<0`. Тогда

```text
Phi(x,sigma)=F_price(Delta(x))+epsilon_hat(x,sigma),
tau=sigma/Tr(sigma G), Psi=J sqrt(tau)V.            (41)
```

Его stationary equations ровно E=0, normalization и все field rows (9).
Точная critical family состоит из constant SO4-coframe R, всех малых
local Lorentz/observer representations H_x с преобразованием matter и
всех positive densities в соответствующем affine source fibre. Единственный
global SO3 overlap вычитается: `6N+6−3+16232=40811`, N=4096.
Constant rank151 около R=I следует из универсальных upper bounds7/3/5
и непрерывности исходных exact minors, а не из предположенной SO4-link
symmetry. Family tangent совпадает со всем kernel (40). Normal IFT
поэтому доказывает, что **все** близкие faithful joint critical points
лежат именно в ней; normal Hessian невырожден, то есть locus Morse–Bott.

Lorentz Gram этой семьи постоянен:
`g_rs(x)=(u_r*)^T R^T eta R u_s*`. Linear links равны H_x H_y^{-1},
их holonomies I. Следовательно nearby nonflat root в этом regular
faithful finite sector **исключён**, а не построен обращением Hessian.
Три global Lorentz-Gram directions сохраняются сверх доказанных
representations. При rank8 boundary, дальних roots и refinement эта
локальная классификация не применяется.

### Полный normalized-amplitude Hessian, включая Q и reference

[Точная amplitude congruence](sources/d0_native_joint_kernel_2026-10-16/AMPLITUDE_INERTIA_CONSUMER.md)
теперь возвращает ранее исключённые направления. На unit HS sphere
положительные shell-density coordinates, Q-amplitudes Y и V in U128
задают точную локальную карту
`Psi=[sqrt(1−||Y||²)sqrt(sigma)+Y]V`. Pure Q Hessian равен
`2(Delta_Q−epsilon*) tensor I128`. Выполненный scalar-only interval
intake всех119 feature groups строго даёт1 momentum below occupied
shell (ground),8 на shell и4087 выше на всём root rectangle.
Следовательно Q-amplitude inertia равна
`(16740352 positive,4096 negative,0 zero)`; Hessian inverse в raw HS
norm меньше0.230124192441809157. Для resolvent без множителя2 имеем
`||G_Q||<0.460249`, что усиливает прежний достаточный bound4.

Exact Q-stationary elimination в этой normalized карте даёт именно
Phi из (41), со всеми mixed terms и normalization derivatives. Поэтому
Sylvester congruence, а не простое сложение несвязанных Hessians, даёт
полную constrained real inertia

```text
(16779967 positive,5589 negative,57195 zero),
normalized domain dimension16842751.               (42)
```

К (40) добавлены все16744448 real Q-amplitudes и16384 reference-unitary
zeros. Общий phase уже входит в U128 и не вычитается дважды. В (42)
не добавлены radial norm direction, epsilon multiplier или separately
stored affine shifts. Никакая большая amplitude matrix не строилась;
подсчитаны строгие scalar mass signs и использована точная редукция.
Эти57195 нулей — tangent восстановленной полной local critical family.

## 12. Проверки и следующий решаемый объект

[kernel_check.py](sources/d0_native_joint_kernel_2026-10-16/kernel_check.py)
проверяет тождества на самостоятельном exact rational fixture той же
семьи цены. Это C4 identity fixture, не замена full16/L8 носителя.
Его исходная normalized complex-amplitude Jacobian имеет размер33x33,
reduced KKT —19x19; точная эквивалентность ядер включает четыре
anti-Hermitian vertical направления. Ненулевые CY, shell S, оба знака
R_Q, global normalizer и nonlinear moving G проверяются отдельно.
Ожидаемые mathematical evidence не переписываются. Изменённый fixture
исполнил286 exact checks; normal/optimized scientific JSON совпал.
Это проверка общей формулы; native q3300 kernel решён отдельно в §7.

[native_chart_check.py](sources/d0_native_joint_kernel_2026-10-16/native_chart_check.py)
проверяет actual Lorentz/positive intersection, регулярную карту и её
Fourier basis. Его рациональная frame fixture не называется новым root.
Ранг basis объясняется (3)–(5), а не экстраполяцией численного rank test.
Исполнены51 проверки; общий вход
`certificates/a4d_native_joint_kernel_check.py` дал одинаковый JSON в normal
и optimized режимах. [Validation](sources/d0_native_joint_kernel_2026-10-16/VALIDATION.json)
сохраняет точные source pins, окружение и области этого запуска. Старые
suites, root solve, evidence generators и Lean здесь не запускаются.

[ordered_operator_check.py](sources/d0_native_joint_kernel_2026-10-16/ordered_operator_check.py)
проверяет (17) на всех19 столбцах карты и полном16-мерном exterior carrier.
Прямая stored-backward формула сверяется с независимым forward+adjoint;
неверный incoming momentum и перестановка creator/return отвергаются.
Три observer-frame направления имеют ненулевые исходные field jets,
а три spatial frame directions проверяют Ward-intertwiner. Эти76 checks
поддерживают API сборки; решение матрицы следует из отдельной оценки (22).

Общий вход теперь исполняет эти413 exact identity checks и новый полный
q3300 interval calculation. Normal и optimized scientific JSON побайтно
совпали, включая явные bounds и decimal B; из сравнения исключено только
время исполнения. [Validation](sources/d0_native_joint_kernel_2026-10-16/VALIDATION.json)
связывает этот запуск с source hashes и опубликованным (22). Вся старая
история root/thermal/central suites повторно не запускалась.

Отдельный [q0 consumer](certificates/a4d_native_zero_mode_check.py)
исполнил268 новых exact checks; его normal/optimized scientific JSON
побайтно совпал. [Результат](sources/d0_native_joint_kernel_2026-10-16/ZERO_MODE_RESULTS.json)
и [validation](sources/d0_native_joint_kernel_2026-10-16/ZERO_MODE_VALIDATION.json)
сохраняют аналитические q0 bounds, real dimensions и exact input hashes.
Нелинейная homogeneous classification — доказательство §9, использующее
эти identities и обычный локальный IFT, а не numerical root search.

Общий nonzero assembler прошёл11 новых focused groups, включая новую
независимую full16 матрицу. Его
[результат](sources/d0_native_joint_kernel_2026-10-16/NONZERO_ALGEBRA_RESULTS.json)
и [validation](sources/d0_native_joint_kernel_2026-10-16/NONZERO_ALGEBRA_VALIDATION.json)
отделяют exact algebra от numerical comparison. Normal/optimized
scientific JSON совпал после удаления только времён исполнения.
Старые три interval-symbol runs не повторялись: их source hashes
проверены, а owner дополнен новым потребителем без изменения расчётов.

Следующий конкретный объект — rank-free native preparation interface
из memory-source owner и полные совместные equations `E C0=0` вместе
с field/source rows. Простое nearby nonflat continuation исходного
faithful root прекращается по §11. Frozen-sigma field Hessian или его
нулевой eigenvalue сами по себе не доказывают joint bifurcation: должны
сохраняться все preparation Euler rows. Физический допуск нативного
joint transition/action и refinement-uniform estimates ещё нужны.
Конкретный [rank-aware consumer](A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md)
даёт `T_k`, вторую eigenjet-строку `E2 C0+2 E1 C1=0` и `M_v`
neutrality test для rank boundary либо удалённой preparation. Его точная
трёхмерная homogeneous connection-source capacity не заменяет полный
field inverse или совместный branch; проверенный midpoint crossing
сам по себе не удовлетворяет полному memory-neutrality scout.
Исходный fixed-source/raw,l1 terminal,
physical primitive/price admission и полный вывод ОТО остаются OPEN.
