# Условная локальная классификация полного faithful v8 critical locus

16 октября 2026. Вход: опубликованный checkpoint
`b1283e9659ae2c4a9855e7b1200c40163eb83481`, полная homogeneous/q0
редукция и все shell-transfer ограничения. Consumer основного
[joint-kernel owner](../../A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md).
Это аналитическое следствие с **ещё не доказанной здесь гипотезой INV**;
оно не является результатом нового расчёта остальных Fourier matrices.

## 1. Утверждение и единственное оставшееся спектральное условие

Фиксируем исходный конечный L8 carrier, N=4096 сайтов, все16 exterior
компонент, reference128, прежнюю цену v8 и counting-site pairing.
Рассматриваем всю регулярную stored-adjoint карту около опубликованного
homogeneous корня, с full-Schmidt-rank128 normalized matter. Обозначим
через P исходный rank128 spectral projector на восемь momenta
Omega={+/-e_r}; complement отделён от epsilon_* исходным ненулевым gap.
Reference-unitary directions и отдельно хранимые affine shifts пока
оставлены за пределами reduced density/field координат.

**INV.** Для каждой ненулевой q вне Omega−Omega полный stationary field
Hessian, после удаления ровно трёх observer representations и трёх
совместных spatial representations, невырожден. Удаление этих шести
направлений включает соответствующее преобразование matter. Требуется
настоящий полный Hessian владельца; first-jet block вне стационарности
или численный спектр rounded root center гипотезу INV не устанавливает.

При INV существует окрестность исходного full-rank joint root, в которой
все reduced density/field critical points образуют гладкое многообразие
размерности40811. Оно состоит **точно** из:

1. постоянного coframe из SO(4)-орбиты исходного coframe с тем же heat Gram;
2. произвольных достаточно малых local Lorentz/observer representations,
   построенных ниже и действующих также на matter;
3. всех положительных плотностей из соответствующего affine source fibre.

В этих координатах критическое многообразие Morse–Bott. Поэтому INV
исключает дополнительные близкие nonflat field roots этой конкретной
faithful L8 задачи; она не конструирует такую ветвь.

## 2. Настоящий гладкий reduced functional

Здесь можно применять обычный normal IFT к градиенту, а не только
считать ядро saddle matrix. Для поля x и epsilon используем точные
Schur-объекты владельца

```text
J=P−Q[Q(Delta−epsilon)Q]^{-1}Q Delta P,
E=J*(Delta−epsilon)J,  G=J*J,
dE=J* dDelta J−d epsilon G.                         (C1)
```

Пусть sigma>0 на P, Tr_P sigma=1. Уравнение
`Tr_P sigma E(x,epsilon)=0` однозначно определяет гладкую
`epsilon_hat(x,sigma)` около корня: его epsilon derivative равна
`−Tr_P sigma G<0`. Положим

```text
N_sigma=Tr_P sigma G,
tau=sigma/N_sigma,
Phi(x,sigma)=F_price(Delta(x))+epsilon_hat(x,sigma). (C2)
```

Сохраняя все производные G и полный normalizer цены, из (C1) получаем

```text
d_x Phi[v] = Tr kappa(Delta) X_v + Tr_P tau J* X_v J,
d_sigma Phi[dot sigma] = Tr_P(dot sigma E)/N_sigma,
Tr dot sigma=0.                                    (C3)
```

Вторая строка равна нулю для всех Hermitian tracezero dot sigma тогда
и только тогда, когда E скалярна; `Tr sigma E=0` затем даёт E=0.
Первая строка — ровно полная field equation владельца. Таким образом
critical points Phi эквивалентны всем близким full-rank normalized joint
solutions после точного Q-elimination и reference quotient. Восстановление
есть `Psi=J sqrt(tau) V`, V unitary из reference128 в P, без удаления
какого-либо exterior grade. Sigma имеет16383 вещественных координат.
Регулярная field-карта имеет65536 координат; размерность reduced domain
равна81919. При корне Hessian Phi конгруэнтен опубликованному reduced KKT.

## 3. Точная базовая SO(4)-семья

Пусть u_r^* — четыре исходных whitened legs, U — матрица их строк,
а R — одна постоянная SO(4) матрица около identity. Положим
`u_r^R=R u_r^*`, observer=e0 и все links=I. Это допустимые **coframe**
изменения: все legs постоянны по своим рёбрам. SO(4)-links не добавляются.
Поскольку `u_r^R dot u_s^R=u_r^* dot u_s^*`, точно сохраняются
`Delta_R=Delta_*`, полный Z, P и epsilon_*. В частности P/128 остаётся
положительной normalized matter density.

Нужна полная стационарность, а не только постоянство цены вдоль R.
Она уже следует из homogeneous source identities владельца. Coframe
rows определяются тем же heat Gram и теми же stationary moments.
Каждая admitted homogeneous link variation имеет spatial generator S_r
с `S_r u_r^R=0`; full16 CAR trace даёт

```text
Tr16[C(u_r^R) iota(u_s^R) Gamma(S_r)]
       =4 (u_s^R)^T S_r u_r^R=0.                   (C4)
```

Ненулевые Fourier field rows для P/128 исчезают по translation
invariance, observer rows — по точному representation intertwiner.
Следовательно `(u^R,I,e0,P/128)` — точные joint roots против **всех**
допустимых первых вариаций. Это не выводится из SO(4)-симметрии всей
admitted SO(3)-link карты.

## 4. Все shell densities и постоянный ранг151

В базовой точке R определим реальный linear map

```text
T_R(v)=P X_v(R)P−Tr_P(P X_v(R)P) P/128,
K_R=ker T_R^* subset Herm_tracezero(P).             (C5)
```

Все точные matter/field equations при фиксированных полях решаются
плотностями

```text
rho_R=P/128+S,  S in K_R,  rho_R|_(P H)>0.         (C6)
```

Matter equation и normalization очевидны из `Delta_R P=epsilon_* P`.
Отклонение field source от уже стационарной P/128 равно `Tr S X_v`;
оно нулевое для всех v ровно при (C5). Поэтому (C6) — точная affine
семья, а не только infinitesimal solution. Положительность открыта.

Ранг T_R постоянен для всех достаточно малых R. Это требует upper
bounds вне специальной симметрической F-матрицы; одной непрерывности
исходных ненулевых minors недостаточно. Нужные upper bounds таковы.

* При q=0 все16 coframe variations дают scalar-on-Fock shell entries
  `gamma delta(G_E)_rr I16` на паре +/-e_r. После centering их image
  имеет размерность3. Есть ровно четыре homogeneous link angles,
  значит весь rank не превосходит7. При R=I lower bound7 доказан;
  его minor остаётся ненулевым около I.
* При q=+/-2e_i три active angular jets удаляются общей spatial
  representation. Она лежит в ker T_R, поскольку
  `X_rep=[Gamma(S),Delta_R]` имеет нулевой shell-to-shell block.
  Чистые inactive coframes имеют J=0 на единственной shell-паре:
  на inactive ролях оба momentum components равны0. Остаются только
  три inactive stabilizers, так что rank не превосходит3.
* При q=+/-e_i+/-e_j шесть active angular jets modulo общие три
  spatial representations дают не более3 image directions. Чистые
  inactive coframes снова имеют J=0 на обеих shell-парах. Два inactive
  stabilizers добавляют не более2, значит rank не превосходит5.

Эти аргументы используют только ненулевые spatial legs, native transport
и scalar-on-full16 Delta_R; они действуют для всех близких rotated
coframes. Исходные точные lower bounds3/5 для **всех** shell transfers
сохраняются по непрерывности их minors в гладкой полной карте. Частот
конечное число, поэтому выбирается одна общая окрестность R. Никакой
симметрический minor при R!=I не подставляется повторно без основания.

В Herm128 tracezero пространство имеет16383 вещественные размерности.
Его Fourier support исчерпывается Omega−Omega. При q=0 target имеет
2047 real coordinates; остальные q образуют четыре axis conjugate pairs
с complex target256 и двенадцать two-axis pairs с complex target512.
Именно

```text
2047 + 4*2*256 + 12*2*512 =16383,
rank_real T_R =7 +4*2*3 +12*2*5 =151,
dim_real K_R =16383−151 =16232.                    (C7)
```

Constant rank делает K_R гладким vector bundle. В окрестности R=I он
тривиализуется; (C6) — открытая положительная часть гладкого affine
bundle с fibre dimension16232. Kernel fibre может зависеть от R:
произвольные source annihilators не переносятся через SO(4) как через
симметрию полного chart.

## 5. Local representations — точные допустимые поля

Берём произвольные достаточно малые periodic
`H_x in SO^+(1,3)`, независимо на каждом из N сайтов. Зададим

```text
n_x=H_x e0,
v_r(x)=H_x u_r^R,
A_xy=H_x H_y^{-1},  y=x+r.                        (C8)
```

Здесь n_x future unit, A_xy Lorentz, `A_xy n_y=n_x`,
`A_xy v_r(y)=v_r(x)` и `A_xy^T h_x A_xy=h_y` точно. Все regularity и
bounded gate inequalities сохраняются при малых параметрах. Для
канонического whitening L_x имеем
`L_x H_x=diag(1,S_x)`, S_x in SO(3). Поэтому (C8) равносильно всем
3N observer coordinates n_x и всем3N local spatial rotations S_x,
а его whitened links равны `diag(1,S_x S_y^{-1})`. Это actual admitted
representation family, а не формальное интегрирование kernel vectors.

Пусть `K=direct_sum_x exterior(H_x)`. Между соответствующими paired
Hilbert spaces K — unitary isomorphism; Euclidean matrix-unitarity K
при движущемся observer не предполагается. Точный ordered primitive
intertwiner исходного владельца даёт

```text
D_(R,H)=K D_R K^{-1},
Delta_(R,H)=K Delta_* K^{-1},
rho_(R,H,S)=K (P/128+S) K^{-1}.                    (C9)
```

Adjoints, normalization, reference и полная цена переносятся тем же
isomorphism. Все source jets также переносятся: field- и preparation-
derivatives K не отбрасываются. Поскольку local representation действует
на **всю** admissible карту, (C9) переводит полные joint critical points
в полные joint critical points, а не только делает цену постоянной на
одной кривой. В fixed-P Schur coordinates эта семья остаётся гладкой:
её occupied subspace близко к P и имеет обратимую P-проекцию.

## 6. Размерность без двойного счёта и геометрия

Параметры H_x дают6N измерений, постоянный R даёт6. Ровно одна
трёхмерная redundancy возникает из постоянного
`K0 in SO(4) intersect SO^+(1,3)=diag(1,SO(3))`:

```text
H_x -> H_x K0^{-1},  R -> K0 R,
rho_R -> exterior(K0) rho_R exterior(K0)^*.        (C10)
```

После (C10) все исходные поля и плотность совпадают. Обратно, равенство
coframes двух таких представлений и invertibility четырёх legs дают
`H_x'^{-1}H_x=R'R^{-1}`, независимо от x; эта матрица лежит в указанном
intersection. Других непрерывных стабилизаторов нет. Можно выбрать
локальную трёхмерную section SO(3)\SO(4), после чего local action
свободно. Field family имеет размерность `6N+3=24579`, а вместе с (C7)

```text
dim critical family =6*4096+3+16232 =40811.         (C11)
```

Local representations сохраняют Lorentz Gram **точно**:

```text
g_L,rs(x) =v_r(x)^T eta v_s(x)
          =(u_r^*)^T R^T eta R u_s^*.              (C12)
```

Он постоянен по lattice. Три R-moduli меняют этот Gram с rank3
differential; они не удаляются как physical gauge. Все linear-link
holonomies (C8) тождественны, включая periodic loops. Следовательно
эта семья имеет постоянную flat Lorentz-Gram geometry, хотя её frame и
observer coordinates могут зависеть от сайта. Про separately stored
affine shifts, translation holonomy или affine torsion это утверждения
не делает.

## 7. Почему INV даёт полноту, а не только найденную семью

В q0 опубликованный reduced KKT kernel имеет9 field directions
(6 representations плюс3 R-moduli) и2040 real density annihilators.
В каждом ненулевом shell-transfer секторе строгая restricted inertia
вместе с полным rank T оставляет только6 field representations и
соответствующие density annihilators. За Omega−Omega нет shell-density
coordinates; INV оставляет там ровно6 representations. С учётом
реальности сопряжённых Fourier pairs полный real kernel имеет размер

```text
6N+3+(16383−151)=40811.                            (C13)
```

Все эти направления являются касательными точной critical family (C6),
(C8), (C9). Независимость следует из свободной field parameterization
после (C10) и из vertical density fibre; её tangent тем самым равен
всему Hessian kernel Phi. Если выбранная symmetry section создаёт
смешанные density/field компоненты, это гладкая замена координат, а не
дополнительное null direction.

Выберем координаты `(t,z)`, в которых построенная family равна z=0.
Hessian Phi на любом transverse complement невырожден в исходной
точке, поскольку его полное ядро — tangent family. Normal IFT решает
`partial_z Phi(t,z)=0` единственным z около0. Но все `(t,0)` уже
critical, поэтому единственное решение равно z=0. Любая близкая full
critical point обязана удовлетворять этим normal equations и потому
лежит в найденной family. По непрерывности normal Hessian сохраняет
невырожденность в меньшей окрестности family: это Morse–Bott locus.

## 8. Область применения и изменение следующего consumer

Утверждение условно до доказательства INV для всех оставшихся частот.
Оно относится к fixed L8 regular full-rank/reference128 задаче и её
точному v8 action. Faithful positivity, Schur gap, positive survival и
bounded gates сохраняются в достаточно малой открытой окрестности.
Никакой refinement-uniform размер этой окрестности не получен.

Reference unitaries восстанавливаются отдельно: U(128) добавляет16384
real vertical parameters к normalized full-amplitude critical family;
эти направления не входят в40811. Affine shifts здесь не считаются.
Результат не распространяется на boundary меньшего Schmidt rank,
далёкие roots, другое L, другой action или physical preparation pullback,
который меняет саму задачу допустимых совместных вариаций.

Если INV выполнена, попытка получить близкий nonflat root простым
нелинейным продолжением этого faithful finite root прекращается: рядом
есть ровно (C6)–(C12). Следующий научный шаг должен использовать actual
дополнительный kernel/bifurcation, иной доказанный режим или исходный
physical preparation/admission, а не объявлять normal inverse
конструкцией curvature.

Исходные g_tau/g_τ, fixed-source comparator и h^{-2} raw,l1 terminal
остаются прежними. g_L в (C12) не переопределяет исходный metric readout;
условная flat-family classification не является bound для исходного raw
residual и не доказывает physical primitive/price admission либо ОТО.
Ни нового физического Cost−Info, ни выбранного источника здесь нет.

Новых scientific runs, receipt writers или изменений старых helpers для
этого аналитического consumer не выполнялось.
