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
Две shell-transfer моды также решены в §8: все matter compatibility rows
и reduced density/field saddle blocks классифицированы; непустые
стационарные density families сохранены. Остальные Fourier блоки ещё
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
**Член `Tr W{D_v,D_w}` остаётся.** Общий finite fixture в §9 специально
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

## 8. Две shell-transfer моды: решение всех matter compatibility rows

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
В остальных частотах kernel и нелинейное неплоское продолжение OPEN.

## 9. Проверки и следующий решаемый объект

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

Дальнейший конкретный объект — остальные Fourier matrices (14) на полной
карте (5), с удалением только **доказанных** representation symmetries.
Для остальных частот из shell difference set решается весь saddle block (15).
Нелинейное продолжение требует решения оставшихся E/field equations
(9); их local inverse, неплоский root и refinement-uniform estimates
этой редукцией не получены. Исходный fixed-source/raw,l1 terminal,
physical primitive/price admission и полный вывод ОТО остаются OPEN.
