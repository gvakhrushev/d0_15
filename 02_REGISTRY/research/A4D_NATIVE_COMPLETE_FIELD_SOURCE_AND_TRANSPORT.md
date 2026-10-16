# Полный полевой источник: record, лоренцев перенос и мера подготовки

2026-10-16. Current execution: [Draft #334](https://github.com/gvakhrushev/d0_15/pull/334),
the same registered joint-response task, resumed from accepted main
`add17919b344f0e46115619aa53d2173ecdcf219`. Preserved scientific SOURCE:
`4d19564d2226496eeeda1f43d84e4b57a4f2e817`. Historical #310 was closed
without merge at 2026-10-16T10:11:24Z and remains closed. Publication in
this Draft is not acceptance on main or physical/continuum closure.

SOURCE #310, carried into #334. Вычисляется источник уже заданной record-программы
на **полном** raw chart, а не произвольное продолжение цены с matching
graph. Все16 matter,10 positive-metric и6 orthogonal-frame координат
сохраняются. Физический закон агрегации, допуска и полной динамики не выбран.

В этом же Draft потребляется [точное разворачивание той же v8 цены](A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md),
SOURCE `3a3c9dda`: heat density и feedback precision исключаются как
математические auxiliary variables с сохранением полного source/Schur
члена. Физическая подготовка, полный field kernel и admission этим не
заменяются. Остаточная source-оценка используется при fixed `beta,M`;
движущиеся калибровки требуют полной формулы (7) её владельца.

## 0. Совместная стационарность и действительный операторный вход

[BOOK03 §03.8](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#038-finite-equations-of-motion)
задаёт конечную совместную стационарность, а §03.25 — bootstrap

```text
B=beta^−1 log Tr exp(−beta Delta)−log det(I−z Feedback).
dB=−Tr(rho_beta dDelta)+z Tr[(I−z Feedback)^−1 dFeedback],
rho_beta=exp(−beta Delta)/Tr exp(−beta Delta).
```

Здесь beta,z фиксированы, Delta положительна на её собственном полном
носителе и I−z Feedback>0. rho_beta — вес дифференциала, а не ещё один
закон физической подготовки. Общая вариационная задача не требует, чтобы
один tick вспомогательного record-engine выдавал следующее q. Лемма §3.1
остаётся точным тестом одного предложенного повторного чтения engine-output;
она сама по себе не определяет форму метрических уравнений действия.

На уже вычисленном [матричном интерфейсе](A4D_NATIVE_JOINT_ADJOINT_SOURCE.md#9-joint-covector-the-gram-contribution-and-internal-ward)
G>0, Dirac=d+d^dagger_G, Pi²=Pi=Pi^dagger_G и U^dagger_G U=I
полный первый отклик той же heat/feedback цены имеет вид

```text
Y=rho_beta Dirac, K=G^−1 dG,
dB=−4 Re Tr(Y dd)+Tr(C_G K)
       +Tr(C_Pi dPi)+Tr(J_U U^−1 dU),
C_G=−2[Y,d^dagger_G]=2[Y,d].
```

C_Pi,J_U — именно полные resolvent-covectors владельца, с сохранённым
feedback, а не новые sources. Они должны пройти через тот же actual
native map, как G и d. При наличии ambient covectors A_x=dS/dq_x и
B_e=dS/dD_e положим M_e=B_e(q_s^−1 D_e)ᵀ. На базовом geometric carrier
D_e q_t D_eᵀ=q_s собственные строки стационарности равны

```text
sym[A_x+sum_(s(e)=x) M_e/2
        −sum_(t(e)=x) D_eᵀ M_e D_e/2]=0,
skew M_e=0, E_b=0, E_m=0, E_preparation=0.       (0)
```

Это [существующий constrained pullback](A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md#1-all-joint-variations-and-their-intrinsic-covector),
со всеми10 metric slots/site,6 link slots/edge, shifts и всеми16 matter
компонентами. Дополнительные native-связи требуют ограничения на реальные
совместно допустимые кривые; (0) не позволяет независимо занулить запрещённые
ambient directions. В §4.1 ниже вычислен её нелинейный второй отклик.

Здесь важна точная область уже имеющегося Dirac. Для literal stored
оператора archiveSolderedDirac=d+ell и Lorentz links реализация heat как
квадрата selfadjoint stored Dirac требует одновременно
A_xyᵀ h_x A_xy=h_y и A_xy v_r(y)=v_r(x).
В этом классе positive polar factor link равен I. Ненулевой boost-диагностик
§4 не является дополнительным членом его positive heat по определению.
Общий adjoint completion d+d^dagger_G — отдельный матричный интерфейс;
он не заменяет stored operator без native owner. Аналогично независимый
unit observer в нём не отождествляется автоматически с full-CAR current,
а counting-site trace — с geometric volume.

Для уже заданной v8 цены полный native operator/program pullback,
включая движущегося observer и все source jets, строится в §0.3 ниже.
Следующий физический шаг — вывести допуск этой же программы, подготовки,
retained reference и всей native цены из одного процесса. Ни сумма разных
цен, ни fitted q′, ни замена stored Dirac здесь не выбираются.

### 0.1. Уже существующий same-operator heat и его stored-native реализация

[Record-generated heat v8](sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md)
уже задаёт конкретный условный ответ на часть предыдущей стрелки. Его
положительный символ `G_*=(d−o)I+o 11ᵀ` **не** является native Lorentz q.
Положим n=e0, внутренние Lorentz links A_xy=I и

```text
F_*=sqrt(d−o)(I−11ᵀ/4)+sqrt(d+3o)11ᵀ/4,
q_native=F_* eta F_*ᵀ, h_coordinate=(F_*F_*ᵀ)^−1=G_*^−1,
v_r=eta F_*_rᵀ, ell=1/8.
```

В rest Gram I все16 exterior creators настоящих stored legs после полного
exterior eta и закреплённой ACDB/ABCD sign-conjugacy дают ровно v8 creators
с CAR-pairing G_*. Constant observer/legs удовлетворяют **обоим** stored
adjoint условиям §0. Поэтому на каждом импульсе actual stored operator
имеет квадрат `(z_k*G_*z_k)I16`, где z_r(k)=8(exp(2pi i k_r/8)−1).
Это точная реализация на однородном native классе, не подстановка другого
Dirac. Все10 однородных symmetric G-jets имеют frame lift; из этого не
следует независимый допуск всех local metric jets в stored-adjoint классе.

У v8 тот же D и literal golden instrument дают

```text
Delta=D², alpha=p² ell²/128, B=I−alpha Delta, p³I<=B<=I,
Lambda=−log(B)/alpha, beta=2n alpha, exp(−beta Lambda)=B^(2n),
H=beta^−1 log[128 workspaceDim Tr_H B^(2n)],
J=−128 Tr_H log[(1−z)I+z B^(2n)], R=<Psi,Delta Psi>.
```

Тепло использует Lambda, квадратичная matter — Delta; их нельзя молча
отождествлять при конечном ell. У рабочего root L=8, n=8192, z=2^−20;
workspaceDim=128^8192 и все128 purifying-reference координат сохраняются.
Сертифицированное окно `d=0.0636351915943445350±10^−12`,
`o=0.0040167350432317253±10^−12` и shell-gap >1/2 берутся из
существующего доказательства v8; старый поиск root здесь не повторяется.
Полная matter есть максимальная purification всех128 состояний
`{±e_r} tensor C16`. Её reduced CAR state I16/16, а не raw pure16 vector.

Стационарность v8 переносится на native кривые, чей действительный
whitened jet факторизуется через его local coefficient/linear-link класс:
собственные source rows v8 нулевые, а дополнительный representation
commutator имеет нулевой trace с коммутирующими spectral weights и rho_m.
Это условный homogeneous joint root на данном спектральном секторе.
Affine shifts, physical preparation из pi0, active apparatus, выбор ell/z,
согласованная AF-refinement и полное native действие здесь ещё не выведены.
Обобщённое утверждение «heat и feedback пока вовсе не связаны одним
оператором» больше неприменимо к этому уже построенному классу.

### 0.2. AF survival из данного D: гладкий signed completion и граница следа

Если **данный** selfadjoint D действительно действует из old left AF
algebra и удовлетворяет bound §0.1, один явный four-copy completion имеет

```text
R=B=I−alpha D², C=sqrt(2I−alpha D²),
S=sqrt(alpha) D C, E=S²=2alpha D²−alpha²D^4,
T=[[R,0,−S,0],[0,R,0,−S],[0,S,0,R],[S,0,R,0]].
```

R,S коммутируют и R²+S²=I, поэтому T unitary, right-module линейный;
полный complementary corner имеет identity и сохраняется. Его blank
survival есть тот же B. Functional calculus коммутирует с unital
AF *-inclusion. Это не доказательство, что фактический site/Fock D уже
принадлежит этой left algebra, или что независимо построенный refined D
равен включению старого.

В отличие от principal `sqrt(E)=sqrt(alpha)|D|C`, signed S аналитичен
через рождение нуля D. Для произвольного некоммутирующего delta D

```text
C deltaC+deltaC C=−alpha{D,deltaD},
deltaS=sqrt(alpha)(deltaD C+D deltaC),
C>=sqrt(1+p³)I.
```

Поэтому нулевой Dirac mode не создаёт inverse-gap loss этого gate-jet.
Pointwise conjugacy через sign(D) не служит smooth-family доказательством.
Это **другой coherent channel**, чем principal four-copy completion:
равенство survival не означает равенства всех неоптимизированных цен.
Для actual AF paths commuting сокращение теперь требует `[sigma,S]=0`,
чего одно `[sigma,E]=0` не гарантирует между противоположными D-signs.

При faithful sigma*=mu exp[−ell f(E)]/Z scalar minimum, exact coherent gap
и условная preparation стационарность сохраняются: sigma* коммутирует с S,
а замена знака S лишь переставляет парные ± paths с равными reference
weights. Для fixed mu полный envelope source новой completion равен

```text
delta A*=Tr[sigma* f'(E) deltaE]
        =4alpha Tr[sigma* f'(E) D R deltaD],
deltaE=2alpha{D,deltaD}
       −alpha²[D²{D,deltaD}+{D,deltaD}D²].
```

При moving mu добавляется actual `−Tr(sigma* delta log mu)/ell`.
Crossings отдельных Kraus factors `w_j R±S/sqrt2=0` требуют прежней
осторожности для joint C²-entropy, даже когда сам gate гладкий.
Для density Hessian новой completion достаточно actual neutral paths:
в обоих central sectors есть путь k_j R с k_j²=p³. Из R>=p³I,
`||k_j R V R k_j||_HS>=p^9||V||_HS`. Output density имеет norm<=1,
поэтому Dlog output>=I в HS sense и

```text
M_T,signed >= p^18/ell, norm(M_T,signed^−1)<=ell/p^18.
```

Оценка сохраняет все coherences, не зависит от AF level и относится лишь
к сжатому trace-zero density block. Старую более сильную p^6-оценку
principal positive-plus paths нельзя автоматически переносить на signed
channel или amplitude/field Hessian. Здесь ell в AF цене есть log(phi);
это не length calibration ell из §0.1, их совпадение не предполагается.

Наконец, GNS heat trace — `sum_j d_j Tr_left f(Delta_j)`, с полными
right multiplicities d_j. Это другая величина, чем PF state trace.
Новый identity-survival complement добавляет zero heat modes; изменения
d_j меняют feedback. Их нельзя удалить или заменить reference rank128.
Таким образом AF-naturality одного gate ещё не сохраняет stationary root
или полную цену. AF preparation-price также не прибавляется к v8 действию
без общего native owner.

### 0.3. Полный bounded stored-native класс: один и тот же прибор на всём семействе

Связка §0.1 продолжается за пределы homogeneous точки **без** замены
stored Dirac. Берём ровно полный класс [joint-adjoint owner](A4D_NATIVE_JOINT_ADJOINT_SOURCE.md):
counting-site weight, observer h_x>0, Lorentz A_xy и

```text
A_xy^T h_x A_xy=h_y, A_xy v_r(y)=v_r(x), y=x+r.
L_x=sqrt(h_x)>0, I_x=Lambda(L_x), u_r(x)=L_x v_r(x),
O_xy=L_x A_xy L_y^−1.                                  (0a)
```

Lambda здесь полный exterior lift во всех16 компонентах; фиксированный
ACDB/ABCD sign bridge включается с обеих сторон как в §0.1. Имеем
`I_x*I_x=G_x=Lambda(h_x)`, `O_xy*O_xy=I`, `O_xy u_r(y)=u_r(x)` и точно

```text
I C(v) I^−1=C(Lv), I i_(hv) I^−1=i_(Lv),
T'_r=Lambda(O_xy) shift_r,
d'=ell^−1 sum_r C(u_r)(T'_r−I),
I D_stored I^−1=d'+d'^dagger.                          (0b)
```

Порядок coefficient/shift сохранён. Собственная r-leg переносится по
r-edge; переноса всех четырёх ног по каждому ребру здесь не требуется.
Это полное равенство, а не совпадение frozen symbols. Нет inverse
Dirac-gap и не удаляется ни один mode, observer или exterior grade.

На открытой bounded области `||u_r(x)||²<1` каждый actual coefficient
имеет те же v8 BetaHat/ZetaHat unitary dilations с coefficient-qubit root
`sqrt(1−||u_r||²)`. Полные T'_r unitary. Поэтому его literal 32-word
construction действует и при noncommuting local coefficients, observer
и links: те же alpha, positive survival B, heat generator, actual program
feedback и quadratic matter следуют из (0b). Никакая симметричная
перестановка coefficient и shift не устанавливается.

Более того, primitive diagram доказан на всём этом классе. Для каждого
creator/contraction/link, coefficient dilation, label operation и golden
comparator `V_a I=I U_a`, с I тензорно продолженным identity на всех
apparatus/reference registers. Здесь перечислены primitives **объявленной условной v8 программы**, не
полный список physically admitted D0-core операций. Их существование как
матриц не подменяет remaining native admission. По [foundation-led reduction](A4D_FOUNDATION_FORCING_NOT_CATALOGUE_SEARCH.md#6-аналитическое-следствие-для-сборки-проверять-порождающие-отображения-а-не-все-программы)
это переносится на каждое конечное ordered word; blank P коммутирует с
I, а outcome labels сохраняются отдельно. Для **данного v8 H+J_program+R**
цена и все actual source jets равны при точном преобразовании той же
подготовки. Это не вывод из одного совпавшего эффекта и не добавочная
AF-price или новый price-descent constant.

Для движущегося observer вся производная I сохраняется. Из L²=h получаем

```text
L Ldot+Ldot L=hdot,
L Lddot+Lddot L=hddot−2Ldot²,
a=Ldot L^−1, K=Gamma(a), Idot=K I,
Kdot=Gamma(Lddot L^−1−a²), Iddot=(Kdot+K²)I,
hatDdot=I Ddot I^−1+[K,hatD],
hatDddot=I Dddot I^−1+2[K,I Ddot I^−1]
           +[Kdot,hatD]+[K,[K,hatD]].                    (0c)
```

Gamma — действительная Lie derivative **полного** exterior representation.
K не обязан быть antiadjoint в фиксированном counting frame: I есть
isometry между движущимся и фиксированным Hilbert carrier. Такие же
формулы действуют для Delta и всех equivariant program operators.

Для native matter v=I Psi, N=v*v нормированная hatPsi=v/sqrt(N) имеет
`dot v=K v+I dotPsi` и `dot N=2Re(v*dot v)`; производная нормировки
сохраняется. Если native density operator определён относительно своего
G, то `hat rho=I rho I^−1`, и его representation term `[K,hat rho]`
сокращается с `[K,hat Delta]` в trace **до** on-shell ограничения.
Второй source сокращается дифференцированием того же точного равенства.
Heat/feedback trace similarity сохраняет весь носитель и multiplicities.
Равенства относятся к actual admitted curves, не превращают все formal
linearized solutions singular constraint set в интегрируемые velocities.

Итак, условная field→v8-program/source стрелка для всего bounded
stored-adjoint класса уже построена. Дальше нельзя снова называть её
неизвестным generic operator map. Не выведены physical primitive admission
LCU/controller/preparation, выбор **всей** native Cost−Info цены и её
исторических расходов, pi0, physical ell/z или native AF-refinement.
Foundation forcing требует эти оставшиеся диаграммы из того же ядра;
операторная конструкция не выбирает желаемое Q из каталога действий.

Counting-site условие существенно: при дополнительном weight omega_x
whitening есть `sqrt(omega_x)Lambda(L_x)`, и shift получает factor
`sqrt(omega_x/omega_y)`. Нельзя объявить его unitary в прежнем unweighted
counting пространстве. Адресная PF-мера, geometric volume и эта исходная
операторная мера не отождествлены. Uniform raw conditioning также требует
собственных lower bounds на h; smooth sqrt не даёт их автоматически.

## 1. Actual endpoint-price и все16 rest-source компонент

Используется ровно двенадцатиканальный прибор из
[matter-clock owner](A4D_NATIVE_MATTER_CLOCK_RECORD_BINDING.md), с его
`λ=1`, упорядоченным `k_(ij,±)` и общим retained `C²⁴`:

```text
m0=rho(F)^−1 m,
w_a=p²+(m0_a−m*_a), a=0,...,11,
X^A=m0_(12+A)−m*_(12+A), A=0,...,3,
theta_a=k_a·X,
W_a=[[sqrt(1−w_a),−sqrt(w_a)e^(−i theta_a)],
     [sqrt(w_a)e^(i theta_a),sqrt(1−w_a)]].
```

Полный comparator — `C_yx=W_y*W_x`; feedback и counting logdet-price
принадлежат [price/metric owner](A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md).
Для одного канала обозначим `w=w_a(x)`, `u=w_a(y)`,
`δ=k_a·(X(x)−X(y))`, `v(s)=s(1−s)`. На открытой области
`0<w,u<1/2`, `1−zf_a>0`, при фиксированном allowed `z`,

```text
f_a=w+u−2wu−2sqrt[v(w)v(u)]cosδ,
J_z(x,y)=−Σ_a log(1−z f_a).                         (1)
```

Второй mode каждого канала имеет нулевой leakage и сохранён в полном
определителе; (1) не является postselection. Непосредственная вариация
той же цены даёт

```text
A_a=1−2u−(1−2w)sqrt[v(u)/v(w)]cosδ,
B_a=1−2w−(1−2u)sqrt[v(w)/v(u)]cosδ,
C_a=2sqrt[v(w)v(u)]sinδ,
dJ_z=Σ_a z/(1−z f_a)
       [A_a dw_a(x)+B_a dw_a(y)+C_a k_a·(dX(x)−dX(y))].       (2)
```

Это все16 endpoint-source слотов: первые12 — amplitude derivatives,
последние4 — суммы `k_a C_a` с противоположными знаками на концах.
Фазы не заморожены, matter normalizer не назначен константой и никакие
компоненты `m0` не исключены. Если сам `z` или другие настройки меняются,
их отдельные derivatives также входят в полную цену; (2) относится к
фиксированному `z`.

У actual endpoint-программы оба конца сравниваются в одном заданном
retained instrument frame. В неё не добавлен native spacetime transport.
Иное сравнение с field-dependent transport между концами является
другой программой и требует собственного закона и его source.

## 2. Off-shell raw pullback: десять transverse costates вычислены

В [полном raw chart](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md#8-a-complete-native-kinematic-lift-of-a-prescribed-positive-metric)
`(h,m0,O)` переменные `h>0`, `m0` strict-timelike и `O∈O(4)` независимы.
Здесь `m*=-2ap e_mask0+(2p−1)e_mask1+e_mask13+e_mask14`, `a=√p`.
Пусть `A=rho(F)` и `R_F[δF]=D rho(F)[δF]m0`. Тогда тождественно

```text
δm0=A^−1[δm−R_F(δF)].                              (3)
```

Для фиксированных endpoints их price (1) зависит только от `m0(x),m0(y)`.
Тот же вывод относится к любому уже определённому функционалу этой
программы и её spatial jets, **если** его measure/weights/reference
также зависят только от `m0` или фиксированы. Обозначим его полный
rest Euler-ковектор после всех integration-by-parts через `e0`.
Из (3) следуют точные raw covectors

```text
E_m=A^−T e0,
E_F=−R_F* E_m,
P_F:=E_F+R_F*E_m=0,
E_h=0, E_O=0.                                      (4)
```

Звёздочка в (4) — cotangent adjoint с полными matrix/packed conventions.
Все10 symmetric `h`-направлений и все6 `O`-направлений включены.
При compact test fields boundary terms исчезают; иначе переносится и
полный boundary operator. Зависимость `e0` от пространственных
производных не теряется: при `δm0(x)≡0` неизменны сам `W(x)` и все его
производные. Поэтому никакая скрытая derivative-frame сила не появляется
в уже заданном `W_y*W_x`.

Это **off-graph** тождество actual field→program law. Нулевые transverse
costates не восстановлены из одних значений на graph. Для этого record
сектора full raw stationarity эквивалентна `e0=0`; она зануляет frame
force. Но она не навязывает `h=q_record[m0]`: raw `h,O` остаются
невидимыми данной программе. Full graph stationarity нельзя переносить
на остальные native sectors, link/shift equations или controller costs.

Если реальное действие содержит geometric measure, native transport,
независимый reference или прямые frame/matter terms, они должны быть
добавлены к (4) собственными derivatives. Наличие совпадающего metric
readout не определяет такой закон. В частности, finite endpoint-price
не доказана функционалом только `q_record`: её прямые internal sources
в (2) остаются. Нормальный metric lift не позволяет их выбросить.

## 3. Тот же matching family: flat h и искривлённая native g

Следующий контроль целиком лежит внутри уже построенного smooth family,
а не использует произвольный внешне заданный metric. Положим

```text
m0(x)=m*+Σ_mu x^mu e_mask(12+mu),
w_a=p², X=x, q_record=h=cI4, c=p³/2,
j=(1,r(m0)), H=−eta+2(eta j)(eta j)ᵀ/(1−|r|²),
F=c^−1/2 O(x)H^1/2, m=rho(F)m0,
eta=diag(1,−1,−1,−1).                              (5)
```

В нуле фактическое fullCAR чтение даёт `N=3`, `r=(−2/3,0,0)`;
strict timelike domain сохраняется в окрестности. Полный `k`-frame
удовлетворяет `kᵀk=6I`, поэтому flat `q_record=cI` следует из того же
literal projector/comparator, а не назначается ему независимо.

На всей strict-timelike области `H eta H=eta`. Поскольку `H>0`,
единственный положительный корень удовлетворяет
`H^1/2 eta H^1/2=eta`: это следует из
`eta H eta=H^−1` и единственности principal positive root.
Поэтому полная native ковариантная Lorentz metric в (5) равна

```text
g=F^−T eta F^−1=c O eta Oᵀ.                       (6)
```

Теперь выберем только для этого контроля свободную `O` как Euclidean
rotation угла `θ=k x0` в плоскости01. Это одно подсемейство имеющихся
шести `O`-полей; они не объявляются gauge. Программа `W(m0)`, её полные
endpoint prices и `h` одинаковы для всех `k`. Между тем

```text
g=c[[cos2θ,sin2θ,0,0],
    [sin2θ,−cos2θ,0,0],
    [0,0,−1,0],[0,0,0,−1]],
R_g=4k² cos(2kx0)/c,
Ric_g(0)=diag(2k²,−2k²,0,0),
G_g=diag(0,0,2k²cos(2kx0),2k²cos(2kx0)).           (7)
```

Знак кривизны — sphere-positive, тот же, что у Lorentz reflection owner.
Для доказательства достаточно буквальной Levi-Civita связи первого
2×2 блока: его determinant равен `−c²`, а scalar curvature равна
`4k²cos(2kx0)/c`. Другие два направления образуют плоский постоянный
product. В двух измерениях `Ric=(R/2)g`, что даёт все компоненты (7).

Таким образом, даже **точное** равенство comparator/native positive
metric на общей smooth программе не определяет Lorentz dynamics.
При `k≠0` native Einstein tensor в нуле ненулевой, хотя `h` плоская
и сама record-программа не видит этого изменения. Если curvature sector
переписан через `g`, полные observer-derivative и boundary terms из
[Lorentz source identity](A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md) должны
компенсировать эту зависимость; их нельзя удалить и оставить только
Einstein term.

Это не утверждение full native joint criticality и не admitted curved
vacuum: blank/volume, preparation, controller, link и shift prices
сохранены как отдельные обязательства. Равенство начальных matching
данных также не является доказанным законом их дальнейшей эволюции.
При двух **данных** frames кинематический link `D_st=F_s F_t^−1`
удовлетворяет `D_st q_t D_stᵀ=q_s` для contravariant
`q_t=F_t eta F_tᵀ`; это не его физическое Euler equation.

[Узкий consumer](sources/d0_native_field_transport_2026-10-16/record_frame_source.py)
экспортирует `run(repo=None)`. Он проверяет literal endpoint source,
все16 rest и frame pullbacks, все10 metric и6 rotation costates,
actual matter-clock germ и точную кривизну (7). Он импортирует только
pin-ированные определения и не запускает старые suites/receipts.

## 3.1. Matching/ring-вход и невозможность исправить output сменой frame при fixed q

Есть точка того же family, где matching выполняется и input одновременно
принадлежит буквальному engine-domain. Не меняя wiring или reference `m*`,
возьмём

```text
m†=−2ap e_mask0+p³ e_mask1
    +e_mask12+e_mask13+e_mask14+e_mask15,
X†=(1,0,0,1), w_a=p²,
L=sqrt(2/p³), m0(x)=m†+L Σ_mu x^mu e_mask(12+mu).
```

Здесь `p³=2p−1`, поэтому первые12 координат совпадают с `m*`.
Actual полное CAR-чтение даёт `N=5`, `J=e0`, `H=I` в нуле: вклад
пространственного α₁ равен `2(m12 m15−m13 m14)=0`, остальные два
также нулевые. Из `DX=L I` получается `q_record(0)=I`, и выбор `O(0)=I`
в matching chart даёт `F(0)=I`, `m(0)=m†`, native `q(0)=eta`.
Все16 координат являются элементами `Z[a]`; шесть engine guards равны
нулю, first-grade pairing `p³` положительна.
Это согласование literal raw **точки** и comparator first-jet reading,
а не допуск raw first jet целиком. В точке retained `G_ref=(FFᵀ)^−1=I`
и `h_J=I`, но вдоль matching germ
`dr1=(2L/5)(dx0−dx1−dx2+dx3)`, `dH01=−2dr1`.
При постоянной `O=I` имеем `dF=dH/2` и `dG_ref=−dH`, вообще ненулевые,
хотя `dh_J=dq_record=0` в нуле. Весь germ не является fixed-reference
engine-germ. Норма `N=5` сохранена; деления состояния на `sqrt(5)` нет.
Никакой новый physical AF image этим также не установлен.

Буквальный `engine.step`, а не reset rest coefficients, выбирает `U+`
и выдаёт полный raw output

```text
m′=(5p−4)e_mask0+t e_mask1
    +(a−p)(e_mask12+e_mask14)−(a+p)(e_mask13+e_mask15),
t=a(4p−3)<0,  t²=65p−40.                          (7a)
```

Норма остаётся5, выходная pairing ненулевая, поэтому этот шаг принят
движком. CAR current при retained `F=I` всё ещё равен `e0`; при
произвольном `F′` это равенство не предполагается. Следующее утверждение
сильнее проверки неудачи при одном фиксированном reference.

**Лемма для всех frames.** Сохраним именно output `m′` из (7a), native
contravariant `q=eta` и прежний readout wiring. Пусть `F′` — **любая**
вещественная невырожденная матрица с `F′ eta F′ᵀ=eta`, включая improper
или time-orientation-reversing frames. Exterior action сохраняет grades,
поэтому first grade новых rest coefficients равна

```text
v=(F′)^−1(t e0),
v0²−|v_spatial|²=t²,  |v0|≥|t|.                  (7b)
```

Между тем probability slot1 того же wiring требует

```text
w1=p²+v0−p³∈(0,1/2)
  iff  3p−2<v0<3p−3/2.
```

Оба конца проверяются буквально: нижний даёт `w1=0`, верхний — `w1=1/2`.
Поскольку `p>7/12`, максимальный абсолютный endpoint равен
`b=3p−3/2`. Но

```text
t²−b²=83p−205/4=83(p−205/332)>0,
(205/332)²+205/332−1=−139/332²<0.                 (7c)
```

Последнее даёт строгую нижнюю границу положительного golden root;
верхняя `p<2/3` следует из `(2/3)²+2/3−1=1/9>0`.
Следовательно, даже замкнутый probability interval не пересекает
необходимую область `|v0|≥|t|`. **Никакой** frame при фиксированном
`q=eta` не возвращает этот output в прежний comparator chart.
Смена time orientation также не помогает.

Вход не обязан быть только flat germ. Например, сохраним те же clocks
`X=X†+Lx`, но положим `w_(01,+)=p²+κ(x0)²`, остальные `w=p²`.
Это меняет raw rest scalar на `κ(x0)²` и оставляет ту же входную точку
`m†`. Из literal metric formula (4) matter-clock owner получаем

```text
q_record(0)=I, Dq_record(0)=0,
∂0²q_record(0)=(κ/3)k_(01,+)k_(01,+)ᵀ
                 +κ² e0e0ᵀ/(6p³),
R_q(0)=−κ/3.                                    (7d)
```

В достаточно малой окрестности определены тот же полный comparator и
matching fields, без назначенных свободных generator jets. Лемма
output относится к их общей нулевой точке. Только эта точка здесь
объявляется literal ring-engine input; весь вещественный germ не
объявляется engine-admitted continuum. Не выведен coupled update
`q′,F′,D′,b′`, допускающий изменение `q`, и не доказана невозможность
другого wiring или другого допущенного процесса. Результат — точная
fixed-q граница данного actual engine step и данного same-program chart,
а не global native no-go или full joint root.

### 3.2. Первый действительный curved-coefficient matter jet того же v8

Пусть P — полный128 shell projector §0.1, Q=I−P, epsilon — shell energy,
`R_Q=Q(Delta−epsilon)^−1Q`. По owned gap `norm(R_Q)<=2`, включая
сохранённые zero modes ниже epsilon. Для любой C¹ joint-critical curve
той же matter sphere `(Delta(t)−epsilon(t))Psi(t)=0` full Schmidt rank128
даёт **операторное** необходимое условие, сильнее averaged equation:

```text
P X P=epsilon' P, Q Psi'=−(R_Q tensor I)X Psi, X=Delta'.   (7e)
```

P Psi' содержит настоящие shell/reference kernel directions, не выкинутые
как gauge. При C² и при (7e) остаётся необходимое условие

```text
P(Y−2X R_Q X)P=epsilon'' P, Y=Delta''.                   (7f)
```

Y должен включать actual field second jet, а не искусственно замороженный
program/preparation. Rank128 persists locally; произвольное расщепление
shell несовместимо с такой полной critical preparation.

Непустой local curved coefficient test задаётся без fitted source:
`qwave=(3,3,0,0)`, `phi(x)=cos(2pi qwave.x/8)`,
`G(t,x)=exp(t phi(x))G_*`. Literal v8 map даёт

```text
d(t)=M_exp(t phi/2) d0,
D(t)=M_exp(t phi/2)d0+d0* M_exp(t phi/2).
```

Это именно true-adjoint extension v8. При variable phi он **не** равен
stored `M_exp(t phi/2)D0`; его native admission нельзя вывести из одного
homogeneous совпадения §0.1. В fixed whitened Fourier basis, для l=k±qwave,

```text
d_k=sum_r c_r z_r(k), D_k=d_k+d_k*, D_k²=lambda_k I16,
D1_lk=(d_k+d_l*)/4,
X_lk=D_l D1_lk+D1_lk D_k,
D2_kk=D_k/8,
Y_kk=lambda_k I16/4+2 sum_(l=k±qwave) D1_kl D1_lk,
E2_k=Y_kk−2 sum_(l=k±qwave) X_kl X_lk/(lambda_l−epsilon).
```

qwave и 2qwave не принадлежат shell difference set, поэтому PXP=0 и (7f)
имеет восемь отдельных **полных16** blocks E2_k. Для continued critical
curve все они должны равняться одному epsilon'' I16.
Эта проверка для **данной** exponential curve уже решена аналитически.
Full-CAR identity даёт

```text
Tr16(X_lk* X_lk)=(epsilon²+lambda_l²)/2
                 +2epsilon lambda_l+|z_l*G_*z_k|²,
Tr16 E2_k=6epsilon+lambda_(k+qwave)+lambda_(k−qwave)
           −2 sum_l Tr16(X_lk*X_lk)/(lambda_l−epsilon).
```

При literal z8 и G_*=(d−o)I+o11ᵀ отсюда точно

```text
Tr16 E2_(e0)−Tr16 E2_(e2)
 =−64(d+3o) P_d,o /[(d+o)((7+5sqrt2)d+(11+8sqrt2)o)],
P_d,o=(d−o)[(14+sqrt2)d+(16+3sqrt2)o]+(8−4sqrt2)o²>0.
```

Знак строго отрицателен на всей области d>o>0, включающей actual root
window. Поэтому prescribed exponential second jet нарушает (7f), даже
после правильного matter first response. Это не перенос вывода из
рационального nonroot control. Независимая CAR-normal-form и scalar
four-vector проверка подтверждает обе identity и положительное разложение.

Сильнее, препятствие есть уже **внутри одного** occupied Fock block.
Из CAR на вакууме

```text
X_lk|0>=(2h_l|0>+c_l c_k|0>)/4, h_l=z_l*G_*z_k,
||X_lk|0>||²=(epsilon lambda_l+3|h_l|²)/16
```

и полного16 trace следует

```text
(E2_e0)_00−Tr16(E2_e0)/16
 =sum_(l=e0±qwave) (epsilon lambda_l−|h_l|²)
                            /[4(lambda_l−epsilon)]
 =8sqrt2(d−o)>0.                                         (7h)
```

В обоих слагаемых Gram deficit равен 8192(d²−o²), а gaps равны
`(256+128sqrt2)(d+o)` и `128(1+sqrt2)(d+o)`. Это точный uniform
nonscalar witness на actual root, независимо подтверждённый двумя выводами.
Для **любого** добавочного local creator-coefficient second jet при fixed
returns diagonal-Fourier deltaD_kk Clifford-линеен. Поэтому
`{D_k,deltaD_kk}` — scalar I16 и не меняет (7h). Итак, этот first jet
не продолжается C² critical curve с одними coefficient variations, даже
если изменить их acceleration. Совместные link/observer/operator
направления и другой first jet не исключены; их допуск ещё надо вывести.

Конструктивное уравнение для **добавочного** допустимого second field jet W
теперь задано: `P L_Delta[W] P=epsilon'' P−E2_prescribed`. Его левая часть
должна быть настоящим differential native field map, с оставшимися
linearized field equations, а не назначенным source. В частности, homogeneous G''
меняет каждый shell block только на `(z_k*G''z_k)I16`; этого недостаточно
для nonscalar CAR части (7h). Иной W за пределами coefficient-only класса и совместно движущиеся links
этим результатом не исключены.
 Необходимый
first matter response уже вычислен: для k=e0,l=(4,3,0,0)
`<vac|X_lk|vac>=z_l*G_*z_k/2`, ненулевой при d>o>0. Все связанные l
лежат выше shell, поэтому actual eliminated matter contribution
`−2 Tr(P X R_Q X P)/128` строго отрицателен. Это не знак полного Hessian
и не существование curved joint root.

Для полного второго field source надо сохранить **все4096** momentum
modes, reference128 и workspace. Положим N=8192,
`s(lambda)=1−alpha lambda`, `h(lambda)=1−z+z s(lambda)^(2N)`,
`Z=Tr_H s(Delta)^(2N)`, включая16 Fock multiplicity, и

```text
kappa(lambda)=−s(lambda)^(2N−1)/Z
             +128 beta z s(lambda)^(2N−1)/h(lambda).
```

У этого nonzero Fourier jet deltaZ=0. Поэтому после actual off-shell
matter elimination точный complete second source равен

```text
S''=Tr[(P/128+kappa(Delta))Y]
    +sum_ALL(k,l) kappa^[1](lambda_k,lambda_l)
                    Tr16(X_kl X_lk)
    −2 Tr(P X R_Q X P)/128.                               (7g)
```

Divided difference вычисляется при fixed **полном** Z, а при равных
lambda — через derivative limit. Только matter часть допускает указанные
малые blocks; замена полного thermal sum одними shell modes запрещена.
Новый consumer реализует blocks и (7g), но не повторяет старый root solve.
Его rational F control `F_diag=1/4,F_off=1/125` явно помечен **nonroot**;
перенос универсальных утверждений на actual root использует его owned
interval/gap. Полный affine/physical/root continuation остаётся задачей.

### 3.3. Почему conformal repair нельзя считать native, и полный real-isometric тест

Условия (0a) сами влекут invariant

```text
G_rr(x)=v_r(x)^T h_x v_r(x)=G_rr(x+r).                   (7i)
```

Следовательно непостоянный `dot G=phi G_*` из §3.2 с qwave=(3,3,0,0)
не является stored-native first jet: по r=0,1 он уже нарушает (7i).
Ни observer motion, ни Lorentz link acceleration не исправляют нарушение
первого условия. Это точный domain факт, независимо от matter Hessian.

Даже в более широком real-isometric v8 extension все24 mean link
accelerations `K_r^T=−K_r` не отменяют **полный** conformal E2. На homogeneous
Fourier block их actual contribution имеет вид

```text
delta d_k=8 sum_r exp(i theta_r)c(v_r)Gamma(K_r),
delta D_k=delta d_k+delta d_k*, delta Delta_k={D_k,delta D_k}.
```

Это не произвольный Hermitian source. Для его pair-creation component
положим omega=pi/4, t=exp(i omega), z=8(t−1), `K_sum=sum K_r` и
`Pi_a=I−v_a v_a^T/d`. Matching `E2+delta Delta=scalar` на a=2,3 требует

```text
w_a=kappa z Pi_a(v_0+v_1),
kappa=o(128+64sqrt2)/16 *sum_(l=e_a±qwave)1/(lambda_l−epsilon)>0,
R_a=d Re w_a−(d cos omega−o) Im w_a/sin omega,
o K_sum v_a=R_a.
```

Последнее следует из actual pair coefficient
`8z[A_a+(t−1)B_a]`, где
`A_a=sum_r v_r wedge K_r v_a`, `B_a=v_a wedge K_a v_a`,
и contraction на v_a. Два совместных требования дают

```text
v_2^T R_3+v_3^T R_2=−32kappa o(d−o)²/d<0,
```

в то время как skew K_sum требует ноль. Native Lorentz/parallel-leg
условия для этого более широкого24-direction запрета не использовались.
Один vacuum component отдельно может меняться при произвольной rotation;
это не решает двух полных CAR blocks. Общие64 GL directions не объявлены
isometric/circuit-admitted. Обе small-CAR и scalar-four-vector части
независимо сверены. Этот тест завершает именно прежний conformal adapter;
следующий пункт строит другой, действительно stored-adjoint first jet.

### 3.4. Искривлённая stored-native семья и конструктивный second matter lift

Положим `F_*=(a−b)I+b11^T`, a>b>0, n=e0 и все A_r=I. Возьмём actual
rotation generator `J_23=−1,J_32=1` (остальные entries ноль),
`phi=cos(2pi(3x0+3x1)/8)` и меняем только одну **полную** leg:

```text
v_2(t,x)=sqrt(1+c t²) exp(t phi(x)J) v_2*,
v_r(t,x)=v_r* (r!=2), F_r(t,x)=(eta v_r(t,x))^T.        (7j)
```

Экспоненту можно заменить rational Cayley chart с теми же first/second
jets. Phi не зависит от x2, поэтому каждая собственная leg параллельна
на своём ребре **точно при всех t**, без изменения links или observer.
F остаётся invertible на явном малом интервале: изменение полной строки
ограничено `||Jv_2*|| |t|+|sqrt(1+c t²)−1| ||v_2*||`. Достаточно, чтобы
эта величина была меньше (a−b)/2, поскольку min singular value F_* есть a−b.
Все16 grades, все10 metric slots в общей вариационной задаче и все
остальные field equations сохраняются; (7j) лишь одна проверяемая кривая.

Это не общий local Lorentz gauge: разные роли не вращаются вместе.
На гладком unit-torus interpolation y=x/8 имеем phi=cos(6pi(y0+y1)).
При указанном J sign и стандартном Ricci convention точная линейная
скалярная кривизна равна

```text
dot R_g=−32(6pi)² b³(a+b)/[(a−b)(a+3b)] phi !=0.
```

Opposite J или отдельный naked-star convention меняют sign, не
nonvanishing. Интеграл first scalar-density variation на flat periodic
background нулевой; local curvature не подменяет total stationarity.

В положительном coefficient frame положим s=J F_*_2^T,
`lambda1=128−64sqrt2`, epsilon=lambda1*d. Для l=k±qwave

```text
V_k=z_2(k)s, W_k=gamma_CAR(V_k),
D1_lk=W_k/2,
D2_kk=gamma_CAR(z_2(k)J²F_*_2^T)/2, Y_kk=0 on shell,
X_lk=D_l D1_lk+D1_lk D_k.
```

Только k=±e2 имеют ненулевой first response; остальные шесть shell
momenta аннулируются. Для активных blocks
`X_lk*X_lk=||u_l−u_k||²||V_k||² I16/4`, где u_k=F_*^T z(k).
Поэтому full128 effective matter operator имеет **scalar** blocks

```text
E2_(±e2)=−gamma I16, E2_(other shell)=0,
gamma=lambda1 ||s||² *[(2+sqrt2)(d+o)+o]
                              /[(2+sqrt2)(d+o)+2o]>0.
```

Это другой результат, чем nonscalar (7h). Здесь действительная
homogeneous length acceleration (7j)

```text
c=gamma/(2lambda1*d)                                    (7k)
```

добавляет +gamma I16 только к активным blocks. Все128 second matter
rows становятся scalar0, epsilon'=epsilon''=0, а first preparation jet
есть actual `Q Psi'=−R_Q X Psi`. И X, и все reference/kernel directions
сохраняются. Это конструктивный native second-field jet, а не подбор
источника или добавление к действию. Он не решает остальные Euler rows.

### 3.5. Полный source на той же семье: thermal carrier нельзя заменить shell

Для любого thermal momentum k и l=k±qwave введём

```text
u_k=F_*^T z(k), w_l=u_l−u_k,
b_k=Re(u_k* V_k), b_l=Re(u_l* V_k),
X_lk=b_k I16+gamma_CAR(w_l)gamma_CAR(V_k)/2,
X_lk*X_lk=c_kl I16,
c_kl=||w_l||²||V_k||²/4+b_k b_l.                       (7l)
```

Это CAR identity, в том числе **вне** occupied shell. Поэтому complete
thermal contraction вычисляется8192 scalar directed edges, сохраняя
все4096 modes и factor16. Не нужна большая Fock matrix или повторный
root solve. Для actual stationary root весь direct source Y сокращается:
`Tr C{D,D2}=0` по homogeneous coefficient Euler rows;
`2(D1²)_kk=|z_2|²||s||² I16` сокращается по G_22 Euler row,
где C=P/128+kappa(Delta). Delta Z'=0 по nonzero Fourier support.
Следовательно точное второе действие после actual matter elimination

```text
S''=16 sum_ALL_8192edges kappa^[1](lambda_k,lambda_l)c_kl
     −gamma/4.                                        (7m)
```

Kappa имеет **полный** Z, reference128, n=8192, z=2^−20 как в (7g).
Добавочная length acceleration (7k) не меняет (7m), поскольку первый
полный source на actual root нулевой. Его нельзя использовать для
подбора Hessian после решения одного matter уравнения.

[Новый consumer](sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py)
вычисляет (7m) наружной interval arithmetic **на прежнем certified d/o
rectangle**, а не ищет новый root. Только точно одинаковые Q(sqrt2)
feature pairs группируются; одинаковые энергии используют derivative
limit. Неравные energy intervals, содержащие0 в знаменателе, отвергаются.
Строгий результат на всём ранее доказанном root rectangle:

```text
0.08996033839979331495 < S'' < 0.08996033878441452448,
```

в частности `0.089<S''<0.091`. Отдельные вклады охвачены интервалами:
heat `[0.6783815403877,0.6783815407011]`,
feedback `[−0.003121132334913,−0.003121132333724]`,
matter `[−0.585300069652997,−0.585300069582938]`.
Группировка даёт1061 точный scalar term,8192 directed edges,
из них1248 exact equal-energy и6944 nonzero-gap. Это новый directional
source calculation, не повторение старого470-check root proof.

Положительное S'' исключает C² critical curve **с данным first joint
velocity**, даже после matter second lift и произвольного допускаемого
second acceleration. Если first links/observer или first field direction
меняются, нужно решать полный совместный linearized Euler operator;
обнуления одного quadratic form недостаточно. Ни все curved roots, ни
сам D0/ОТО этим условным v8 результатом не исключены.

## 4. Настоящая Lorentz link: положительная часть не исчезает

Теперь используется другое уже имеющееся данное: пространственная связь
`D`, переводящая target-векторы в source-векторы. При ковариантных метриках
её полное кинематическое ограничение имеет вид

```text
Dᵀ g_s D=g_t.
```

Это эквивалентно `D q_t Dᵀ=q_s` для `q=g⁻¹`. Никакой временной
эволюции `q,D,b,m` этим не назначается. Пусть `u_s,u_t` — единичные
timelike наблюдатели из полного CAR-чтения с его сохранённым reference,
а не автоматически first-grade оси record/engine. Возьмём уже выведенные
положительные observer metrics

```text
h_a=−g_a+2(g_a u_a)(g_a u_a)ᵀ,
M=h_t⁻¹ Dᵀ h_s D,  B=M^1/2,  R=D B⁻¹.            (8)
```

Корень — единственный principal root положительного в `h_t` смысле
оператора. Он не выбирает дополнительный Euclidean frame. Это точная
полярная факторизация **данной** связи `D=R B`, с сохранением обоих
множителей, а не замена связи её унитарной частью.

Для доказательства положим `K_a=g_a⁻¹h_a=2u_a u_aᵀg_a−I`,
`v=D⁻¹u_s`. Тогда `M=K_t K_v`, откуда `Mᵀg_tM=g_t`.
Principal functional calculus и единственность положительного корня дают
`B⁻¹=g_t⁻¹Bᵀg_t`. Поэтому

```text
Bᵀg_t B=g_t,
Rᵀg_s R=g_t,  Rᵀh_s R=h_t.                       (9)
```

Следовательно, `R` совмещает observer **линии**. Если
`c_pair=u_sᵀg_sD u_t`, то `|c_pair|≥1` и
`R u_t=sign(c_pair)u_s`. Положительный pairing сам не выбирает future
orientation. В плоскости `u_t,v` оператор `M` — boost с rapidity
`±2χ`, `χ=arcosh|c_pair|`; на ортогональном двумерном дополнении он единичен.
Поэтому singular values полного переноса, в соответствующих endpoint
pairings, равны

```text
D on vectors:       exp(χ), exp(−χ), 1, 1,
ΛD on ALL grades:   exp(χ) [4], exp(−χ) [4], 1 [8].
```

Все grades `1,4,6,4,1` сохранены. В частности, для полного exterior
Gram `ΛM` получается точное, не зависящее от выбора basis тождество

```text
Tr_16 ΛM=det_4(I+M)=16 c_pair²,
I_boost:=Tr_16 ΛM−16=16(c_pair²−1),
d I_boost=32 c_pair dc_pair.                       (10)
```

В (10) используется обычный полный exterior counting trace, а не
defining AF PF-trace и не одна из зарегистрированных цен.
`I_boost` здесь — диагностическое чтение уже имеющейся связи. Оно не
объявляется новым членом физического действия, тепловой ценой или
chronological feedback. Замена `D` на `R` удаляет именно эту ненулевую
информацию. Один этот скаляр также не определяет всю связь: `R`, boost
direction, holonomies и affine shifts не удаляются и не заменяются им.
При рациональном boost `coshχ=5/4`, `sinhχ=3/4` полярная
часть `B=D`, `R=I`, полный spectrum `ΛM` равен
`4 [4], 1/4 [4], 1 [8]`; `I_boost=9` и его rapidity-производная равна30.

Полная производная сохраняет оба endpoint pairing и саму связь:

```text
dM=−h_t⁻¹ dh_t M
   +h_t⁻¹[dDᵀh_sD+Dᵀdh_sD+Dᵀh_s dD],
B dB+dB B=dM,
dR=dD B⁻¹−R dB B⁻¹,
dc_pair=du_sᵀg_sD u_t+u_sᵀdg_sD u_t
        +u_sᵀg_s dD u_t+u_sᵀg_sD du_t.            (11)
```

Sylvester equation имеет единственное решение: все eigenvalues `B`
положительны. Для actual полного current `J`,
`u=J/sqrt(κ)`, `κ=JᵀgJ`, используются
`dκ=JᵀdgJ+2Jᵀg dJ` и
`du=dJ/sqrt(κ)−J dκ/(2κ^(3/2))`.
Actual `dJ` включает все16 matter, frame/reference и moving-normalizer
слагаемые владельца. На его собственной подготовке `m(s)` при `s=1`,
`D=I`, `u_t=e0` источник (10) равен `768/25`. Замораживание нормировки
материи вместо этого даёт ошибочное `2304/25`.

Если полный exterior pairing содержит site density
`W_a=ω_a Λh_a`, то `ζ=ω_s/ω_t` остаётся в полном Gram:

```text
Tr_16[(ΛD)^sharp ΛD]=16ζ c_pair²,
dTr=16 c_pair² dζ+32ζ c_pair dc_pair.               (12)
```

В частности, `ΛR` удовлетворяет `(ΛR)^sharpΛR=ζI`, а полностью
weighted-unitary часть есть `U=ζ^−1/2ΛR` с положительной частью
`sqrt(ζ)ΛB`. При переменной density нельзя назвать ненормированный
`ΛR` унитарным для полного `W`.
Нормировка half-density является отдельной операцией, которую нужно
задать и продифференцировать. Она не разрешает молча удалить measure/source.
Например, контракты `ω=sqrt(|det g_cov|)` и принадлежащий прежнему
exterior owner `ω=sqrt(|det q_contra|)` при `q=g⁻¹` дают противоположные
log-density jets. Здесь сохранён произвольный `ω`; ни один из этих
контрактов не выбран новым физическим volume law.

Наконец, `u_pair` не отождествляется с `n_record`: нынешний engine
использует first-grade ось, и её совпадение с full-CAR observer не доказано.
Совмещение observer линий в (9) поэтому не означает автоматически
нулевой источник принадлежащего другому владельцу chronological price.
Связь `D` пространственная; её объявление временным record-переносом
также потребовало бы собственного закона.

## 4.1. Exact second jet совместного metric/link carrier

Для уравнений (0) требуется второй отклик на самом constraint, включая
кривизну его вложения. Он уже строится без выбора нового действия.
Пусть q_s,q_t симметричны и невырождены, D q_t Dᵀ=q_s. Для малых
симметричных V_s,V_t и skew K положим

```text
A_a(V_a)=(I+V_a q_a^−1)^(1/2),
D(V_s,V_t,K)=A_s exp(K q_s^−1) D A_t^−1.           (12a)
```

Корень здесь — вещественная аналитическая ветвь около I, заданная
сходящимся power series при малом V. Он q-selfadjoint, а не обязательно
Euclidean symmetric. Поэтому A_a q_a A_aᵀ=q_a+V_a, а skew K даёт
exp(K q_s^−1) q_s exp(K q_s^−1)ᵀ=q_s. Формула (12a) удовлетворяет
constraint точно. На графе одна A_x применяется ко всем рёбрам вершины;
независимые K_e сохраняют все6 link slots на каждом ребре.

Для направлений i,j обозначим L_ai=V_ai q_a^−1, Omega_i=K_i q_s^−1
и {P,Q}=PQ+QP. Их полные first/mixed-second link jets равны

```text
W_i=(L_si/2+Omega_i)D−D L_ti/2,
Z_ij=[−{L_si,L_sj}/8+(L_si Omega_j+L_sj Omega_i)/2
                       +{Omega_i,Omega_j}/2]D
     −(L_si/4+Omega_i/2)D L_tj
     −(L_sj/4+Omega_j/2)D L_ti
     +3D{L_ti,L_tj}/8.                             (12b)
```

Это следует из A=I+L/2−L²/8+O(L³), A^−1=I−L/2+3L²/8+O(L³)
и exp Omega. Никакая коммутативность матриц не используется. При любом
совместимом first jet K=W q_t Dᵀ+(D V_t Dᵀ−V_s)/2 skew; это также
доказывает полноту параметров всех10+10 metric и6 link направлений.

Если уже заданное S имеет ambient link-covector B_e, то

```text
H_chart[i,j]=H_ambient[v_i,v_j]+sum_e Tr(B_eᵀ Z_eij). (12c)
```

Raw b,m и прочие независимые координаты можно оставить линейными;
их вторые производные тогда нулевые, но все mixed ambient rows остаются.
Добавление conormal extension Tr[Lambdaᵀ(D q_t Dᵀ−q_s)] меняет
два слагаемых (12c) противоположно: их сумма точно ноль, поскольку
вторая производная constraint равна нулю на (12a). Ambient Hessian
без B:Z не обладает этой независимостью. В собственном рациональном
noncommuting контроле его ошибочное значение −8140397/307200 сокращается
ровно до0 после добавления B:Z.

Это Hessian pullback выбранного chart. В constrained critical point он
задаёт независимую от chart билинейную форму; вне него смена координат
добавляет first-source term. Basic carrier chart не доказывает stored
Dirac adjointness, parallel-leg, observer/preparation или holonomy
условия §0. Их полные second jets также нужны для native решения.
Функции joint_link_first_jet/joint_link_second_jet реализованы в том же
lorentz_link_transport consumer, без нового operator или receipt.

## 5. Actual PF-подготовка: полная цена содержит measure-source

В этом разделе адрес `a=(j,i)` — **внутренний defining AF address**,
`r_a=p^(n+1+j)`. Это другой domain, чем spatial archive point `x`.
Владелец ещё не задаёт map `a→x` или `a→X(x)`; внутренний PF trace нельзя
отождествить с пространственным объёмом одним переименованием индекса.

Используется actual flagged channel `Y=Φ_Eσ` из
[preparation owner](A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md). В локальном
собственном basis эффекта `E` обозначим `w_a=σ_aa`, а через `P_diag`
pinching на actual fine path/address projections. Для его абсолютных
conditional prices `f_a=f_j(e_a)` точное тождество имеет вид

```text
A=6+Σ_a w_a f_a+D(w||r)/g0+C_out/g0,
C_out=D(Y||P_diag Y),  g0=log(phi).                 (13)
```

Здесь baseline именно6. Канонический blank `B_n` дополнительно содержит
`Σ r_a f_a(blank)` и не может заменить6 при абсолютных `f_a`.
Доказательство (13): relative-entropy pinching identity
`D(Y||μ_f)=D(P_diag Y||μ_f)+D(Y||P_diag Y)`, затем actual diagonal
probabilities `w_a P(fine path|a)` дают первые два слагаемых.
Все fine paths, central sectors и coherences остаются в `Y`.

`C_out≥0` сравнивает coherent вход с его **диагональным** входом.
Это не прежняя, вообще неверная для coherences замена полной цены на
`D(σ||μ)/g0+Tr σ f(E)`: её отличие контролируется другой DPI identity.
Moving pinching/eigenbasis при `dE` также входит в полную производную;
никакой выбор eigenvectors физическим законом не объявляется.

На positive-weight chart `w_a,r_a>0`, при `Σdw=Σdr=0` и в области
дифференцируемости retained coherence gap, полная производная (13) равна

```text
dA=Σ w_a df_a
   +Σ [f_a+log(w_a/r_a)/g0]dw_a
   −Σ w_a dlog(r_a)/g0+dC_out/g0.                  (14)
```

При рождении ранга применяется принадлежащий владельцу C¹ amplitude/support
limit; формальные density derivatives `log(w_a)` при `w_a=0` не используются.

На уже доказанном faithful minimum `w_a*=r_a exp(−g0 f_a)/Z`,
`C_out=0`, получается

```text
A*=6−log Z/g0,
dA*=Σ w_a* df_a−Σ w_a* dlog(r_a)/g0.              (15)
```

При фиксированных native `p,n`, reference и code имеем `dr_a=0`.
Если же тот же закон после пространственного pushforward действительно
даёт moving masses, их source нельзя выбросить.
В частности, normalized mean `M=Σ w_a* f_a` имеет другую производную:

```text
dM=E_w(df)−g0 Cov_w(f,df)+Cov_w(f,dlog r).          (16)
```

Именно KL-mass term в (13) компенсирует covariance term; он не является
подогнанным counterterm. Поэтому даже доказанное в будущем совпадение
`w*` с volume probabilities не превратит эту полную цену в одно `M`.
Это классификация **имеющейся внутренней** агрегации. Она не опровергает
условную normalized spatial extension из coherent-compiler owner:
для её применения нужен собственный spatial measure/aggregation theorem.

Для noncommuting вариаций требуется более полное чтение, чем список
движущихся eigenvalue weights. Пусть впервые задан **действительный**
POVM/readout с test observable `O_φ`, включая его собственную field
зависимость. На том же faithful minimum положим

```text
L=log μ−g0 f(E),  σ*=exp(L)/Z,  ν(φ)=Tr(σ* O_φ).
```

Здесь `μ` — central PF-reference; при фиксированном native контракте она
не движется. Производная trace exponential даёт точное operator identity

```text
dν(φ)=Tr(σ* dO_φ)
 +∫_0^1 Tr[σ*^(1−s)(O_φ−ν(φ)I)σ*^s dL]ds,
dL=dlog μ−g0 Df_E[dE].                            (16a)
```

`Df_E` — полный Fréchet derivative, с divided differences
`f^[1](e_i,e_j)`; заменять его на `f'(E)dE` вне trace envelope нельзя.
При совпадающих eigenvalues используется непрерывный предел `f'`.
Это Kubo–Mori covariance, а не предположение о commuting state или
замороженном собственном basis. Производная `O_φ` сохраняет moving
readout, reference и clocks. Само существование такого алгебраического
чтения не доказывает его primitive admission или spatial interpretation.

Например, для actual n1 effect `E2=diag(9/25,16/25)`,
`dE2=σ_x`, `O_φ=σ_x⊕0` имеем
`dν=2p²(q_1−q_2)/(Z(e_1−e_2))`, где
`q_i=exp(−g0 f_0(e_i))`. Это ненулевой источник той же подготовки,
хотя eigenvalue jets обоих `e_i` равны нулю. Поэтому один classical
score не описывает всю допустимую noncommuting вариацию.

Лишь на commuting fixed-address подсемействе, если actual clock map
`a→X_a` уже задан, (16a) упрощается до

```text
dν(φ)=E_w[gradφ(X)·dX]
      +Cov_w(φ(X), dlog r−g0 df).                  (16b)
```

Это конкретная identity для следующего spatial-measure theorem. На
общей фиксированной области в одних и тех же координатах normalized
geometric volume имеет derivative
`dν_h(φ)=Cov_νh(φ,tr(h⁻¹dh))/2`. Следовательно, identification требует
сопоставить её с (16a), либо с действительно применимой (16b), для
**всех** test functions, с собственными sampling/refinement bounds.
Moving coordinate/domain и boundary terms нужно также перенести.
Ни конечная atomic measure, ни один contraction не объявляются уже
равными гладкому volume limit. Назначение `dVol_h/V` по определению не
выполняет это требование и не доказывает исходный raw-norm terminal.

## 5.1. Некоммутирующий Hessian и равномерный inverse блока подготовки

Рассмотрим **ту же** вторую полную цену
A(E,sigma)=6+D(Phi_E sigma||mu_f)/ell, ell=log(phi), и её faithful minimum
A*=6−log Tr exp(L)/ell, L=log(mu)−ell f(E).
Эффекты лежат внутри (0,I), выбранная область не пересекает нули
minus-факторов actual Kraus paths. Это C²-область; прежние C¹ rank-birth
результаты сохраняются, но не заменяют второй производной на её границе.

Пусть угловые скобки означают Tr(sigma* ·). Полная некоммутирующая
ковариация есть

```text
Cov_BKM(A,B)=integral_0^1 Tr[sigma*^(1−s)(A−<A>I)sigma*^s B] ds.
H*[v,w]=−[<L_vw>+Cov_BKM(L_v,L_w)]/ell.           (16c)
```

Это дифференцирование того же глобального log Z, с полной нормировкой.
Все матрицы jets представлены в base spectral basis, а не в движущихся
диагональных координатах. При фиксированном native reference

```text
H*[v,w]=<D²f_E[E_v,E_w]+Df_E[E_vw]>
            −ell Cov_BKM(Df_E[E_v],Df_E[E_w]).      (16d)
```

Первое слагаемое — direct program response, второе — индуцированный
отклик подготовки. При данном допустимом движении reference добавляются
оба jets log(mu) в L_v,L_vw. ell здесь фиксирована. В частности,
E_vw включает actual field-map second jet и acceleration D из (12b).
Нельзя заменить его нулём по совпадению одного first jet.

Из exact coherent gap владельца
A(E,sigma)=A*(E)+D(Phi_E sigma||Phi_E sigma*(E))/ell
следует полный Schur-разбор в точке минимума. Обозначим
Y*=Phi_E sigma*, J_v=D sigma*[v], T={sum_j Tr S_j=0} и

```text
M=Phi_E* Dlog_(Y*) Phi_E/ell,
M_T=P_T M|T,
H_full[(v,S),(w,T1)]=H*[v,w]+<S−J_v,M_T(T1−J_w)>_HS,
H*=A_EE−A_Esigma M_T^−1 A_sigmaE.                 (16e)
```

P_T — лишь HS/Riesz compression на trace-constraint; M само не обязано
сохранять T. Derivatives Phi_E не заморожены: в разности двух одинаковых
baseline output они сокращаются, оставляя Phi_E(S−J_v).
Именно output metric Phi_E* Dlog_(Y*) Phi_E, а не произвольно подставленная
Dlog_(sigma*), принадлежит полному coherent action.

**Равномерная оценка обратного.** В каждом старом центральном блоке
сохранён собственный plus path
A_j+=w_j sqrt(I−E_j)+sqrt(E_j)/sqrt(2),
w_0²=p³, w_1²=p²<1/2. Functional calculus даёт A_j+>=w_j I,
поскольку sqrt(1−e)+sqrt(e)>=1. Для любого Hermitian S_j, включая
[S_j,E_j]!=0, поэтому
||A_j+ S_j A_j+||_HS²>=w_j⁴||S_j||_HS².
Нормированная Y* имеет eigenvalues<=1, а все divided differences log
на этом интервале не меньше1. Следовательно,

```text
<S,M_T S> >= ||Phi_E S||_HS²/ell
             >= p^6 ||S||_HS²/ell,
||M_T^−1||_(HS→HS) <= ell/p^6.                    (16f)
```

Константа не зависит от уровня n, defining dimension или числа адресов;
межблочные mass jets и все внутренние coherences сохранены. Это оценка
нормы обратного density-блока, а не полного condition number. Верхние
собственные значения M, mixed field-jets и derivatives около нулей paths
могут расти. Оценка не переносится на весь GNS amplitude-Hessian:
tau=Tr(CC*) и sigma=CC*/tau остаются, right-unitary и radial fibers
дают нулевые направления этой цены. Они не объявляются physical gauge,
а другие члены S могут их видеть. Независимый physical допуск подготовки
и выбор именно этой стационарной ветви не следуют из (16e)–(16f).

Для **той же** линеаризованной совместной системы с заданными residuals
r_E,r_sigma это даёт конструктивное исключение density-блока:

```text
S=J_v+M_T^−1 r_sigma,
||S−J_v||_HS <= (ell/p^6)||r_sigma||_HS,
H* v=r_E+J* r_sigma.                              (16g)
```

Residuals здесь — невязки собственных уравнений, а не выбранный source.
Обратимость H* и оценки J ещё не установлены. В частности, нулевые
raw h/O строки прежнего rest-only прибора этим не становятся ненулевыми.

Actual n1 двухпараметрический effect
E0=[[9/25+x,y],[y,16/25]], E1=9/25 даёт в нуле

```text
A*_yy=2p²(q1 f0'(9/25)−q2 f0'(16/25))
                    /[Z(9/25−16/25)] < −93/112,
A*_x > 237/1600,
q_i=exp(−ell f0(e_i)), Z=p²(q1+q2)+p³exp(−ell f1(9/25)).
```

Строгие знаки следуют из собственных рациональных log enclosures,
без numerical exp. При dE/dy=sigma_x first eigenvalue jets равны нулю,
а Hessian ненулевой. На isospectral unitary curve с тем же first dE
добавочный E_yy точно сокращает его; это конкретная необходимость direct
second jet. Негативный H*_yy не является положительной физической metric.
Нескалярный effect этого instrument-fixture также не объявляется
допущенным входом прежнего direct AF-to-CAR engine support fiber.

Наконец, BKM Cauchy–Schwarz и logarithmic mean<=arithmetic mean дают
dimension-free bound
|H*[v,w]|<=(||L_vw||_op+||L_v||_op||L_w||_op)/ell.
Для количественного native решения всё ещё требуются равномерные
оценки actual field/readout/transport jets. Прибор, зависящий только от
m0, остаётся слепым к независимым h,O до всех порядков; минимизация
подготовки не создаёт отсутствующей зависимости. Формулы реализованы
в том же preparation_measure consumer.

## 6. Строго наследуемые clocks не создают spatial volume limit

У actual archive adapter `π_n=archiveProjection` и
`|ArchivePoints(0)|=16`. Если clocks удовлетворяют буквальному закону
`X_(n+1)=X_n∘π_n`, то `X_n=X_0∘toBase`. Для **любой** согласованной
вероятности `(π_n)_*μ_(n+1)=μ_n` её pushforward равен

```text
ν_n=(X_n)_*μ_n=(X_0)_*μ_0.                         (17)
```

Следовательно, это одна и та же мера с не более чем16 атомами при любом
refinement. Полная field-производная на гладкой test function `φ` равна

```text
dν(φ)=Σ_b[dμ_0(b)φ(X_0(b))
            +μ_0(b) gradφ(X_0(b))·dX_0(b)].        (18)
```

Больший архив сам по себе не создаёт новых clock values или гладкой
четырёхмерной volume measure в этом классе. Это не запрет richer
refinements: actual archive также допускает nonatomic projective measures,
а новые fine matter/clock states не обязаны быть strict pullbacks.
Но их создание и влияние на полную цену должны иметь собственный допуск.

Если единственное marginal-условие положительного conditional kernel —
parent mass на actual projection fibre, вариации двух child weights с
противоположными знаками её сохраняют. Pushforward не зависит от **всех**
таких вариаций ровно тогда, когда clock constant на каждом таком fibre.
Если дополнительно фиксируется golden-bit marginal, этот критерий
применяется к `(parent,bit)` subfibres допустимых jets: clocks могут
различать bits, оставаясь невидимыми именно этим kernel variations.
Иначе соответствующий kernel/clock source остаётся в pushforward.
Ни internal AF-address trace, ни compatibility parent marginals не
определяют этот source автоматически и не допускают все такие jets физически.

Конструктивный выход из strict-inheritance класса уже дан параллельным
[history/density/coframe результатом](A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md).
Его новый child-clock rule делит очередной координатный интервал в долях
p,p² по фактическим F/R cost-cut историям, сохраняя pending returns.
Центры дочерних ячеек образуют martingale, размеры не превосходят
2p^floor(n/8), а объёмы равны cylinder weights. Поэтому pushforward
предельного clock есть Lebesgue measure на адресном кубе, с явной
Lipschitz quadrature error. Это не противоречит (17): clocks уже меняются
у children. Допуск нового rule как native material clocks и его связь
со спектральными setting labels не следуют из этого построения.

Тот же результат даёт обратимую density/coframe замену
ehat=sqrt(m/|det e|)e со всеми16 coframe и10 metric вариациями.
Для **условного** quadratic-anchor first-order сектора Phi(ehat,U,psi)
плюс KL точная стационарность эквивалентна stationary Phi и w=r;
приведён искривлённый Einstein–scalar контроль со всеми его уравнениями.
Полный native spectral price не отождествлён с этим сектором, Lorentz
Palatini не подставляется вместо R_h, а настоящие observer/source terms
остаются. Новый §5.1, в отличие от одного commuting KL, использует полный
coherent output Hessian actual AF channel. Совместить эти инструменты
физически можно лишь после source identity одного native action.

### 6.1. Density/coframe transport: точный stored-heat остаток

Предыдущая density substitution сохраняет полные rest matter и record
normalizers, если вместе с `Fhat=aF`, `a=chi^−1/2`, переносить каждую
matter grade k как `mhat^(k)=a^k m^(k)`. Тогда m0 неизменно во всех16
координатах, `Jhat=aJ`, `hhat=chi h`; это не freeze matter. Record,
зависящий только от m0, имеет нулевой compensated density source. Но
native positive pairing меняется, поэтому неизменность такого record не
доказывает comparator/native matching после этой замены.

Literal stored creators и contractions линейны по legs. При сохранённых
internal links и observer Gram действительная операторная замена есть

```text
D_a=M_a D, D_a−D_a^dagger_G=[M_a,D],
([M_a,D])_xy=(a_x−a_y)D_xy.                              (18a)
```

Это вычисленный остаток, не определение через желаемую Einstein source.
Для исходного selfadjoint D в owned counting/rest Gram он исчезает лишь
при constant a на каждой связной component ненулевых edge blocks.
Stored parallel-leg condition даёт то же a_y=a_x. Поэтому произвольный
nonconstant density/coframe lift выходит из **этого** stored heat-domain.
Это не запрет другим pairings и не отрицательность спектра.

Есть точная классификация возможного **скалярного** site-weight repair:
`G_omega=M_omega G` делает тот же D_a selfadjoint ровно при
`[M_(omega a),D]=0`, то есть `omega a=constant` на связном carrier.
Итак G_a=c M_a^−1 G. Similarity

```text
H_a=sqrt(M_a)D sqrt(M_a)=M_a^−1/2 D_a M_a^1/2
```

selfadjoint в старом G, сохраняет все modes и доказывает real spectrum
D_a и nonnegative spectrum D_a². Это conditional algebraic repair, а не
native выбор меры: его scalar factor sqrt(chi) отличается от geometric
volume chi². General matrix/graded pairings этим не классифицированы.

В исходной raw sup норме даже derivative defect не uniform при refinement:
на любом even L, для f_x=(−1)^x и constant vacuum v, actual flat full16
operator даёт `[M_f,D]v=2L f c_0 v`. При chi(t)=1+t f поэтому norm
производной (18a) не меньше L. Все16 grades сохранены. Smooth a с
заранее заданным Lipschitz bound даёт O(Lip(a)) edge defect, но эта
дополнительная регулярность не следует из raw norm родительской задачи.

Если собственный owner оценивает уже заданное heat на D_a², trace
сохраняется similarity с H_a². При fixed beta и исходном D полный
первый source по u=log chi вычисляется непосредственно:

```text
delta H_a=−{M_delta_u,H_a}/4,
delta[beta^−1 log Tr exp(−beta H_a²)]
     =sum_x Tr_fibre[(rho_a H_a²)_xx] delta_u(x),
rho_a=exp(−beta H_a²)/Tr exp(−beta H_a²).
```

Коэффициенты неотрицательны, их сумма — Gibbs mean energy. Здесь нет
нового compensator или утверждения, что это heat старой naked-star цены.
Для native bridge остаётся вывести собственный pairing/measure и actual
shared-face/four-shift operator из child-clock histories. Одной nonatomic
address measure для этого недостаточно.

Полученный параллельно [центральный variational compiler](A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md)
уточняет область предыдущей условной density/coframe сборки. Для своего
нового coherent terminal program он выводит ровно один положительный
множитель **всех** Euler-строк заданного Lorentz Q, включая меньшие ранги
подготовки. Его faithful optimum имеет собственный ready/pending tilt,
а не постулированное w=r; coarse measure и её first-source jets имеют
address-limit с rate O(p^(2c/17)). Это сохранённый результат SOURCE
358ecbb1, не повторный запуск его95 controls. Он не выбирает физически Q,
новые engine primitives, terminal-price вместо всех расходов или native
heat-domain. Поэтому (18a), полные observer terms и различие мер остаются.

## 7. Следующая общая конструкция

Вычислены полный record/preparation source и условная native
operator/program стрелка §0.3 на всём bounded stored-adjoint классе. Имеющийся
comparator слеп к raw frame при фиксированной rest matter; совпадение
его positive metric с native pairing не даёт Lorentz Einstein equation.
Полный actual Lorentz link содержит boost/observer информацию с точной
производной (11)–(12), которую нельзя заменить одной унитарной частью.
Actual preparation несёт собственные KL/normalizer/measure источники
(14)–(18), а не автоматически normalized spacetime average.

§0.3 даёт same-program equality и полные source/observer jets, а не
только homogeneous совпадение. §3.3 устраняет ложный conformal native
adapter. §3.4 строит настоящий искривлённый stored-native curve и second
matter lift; §3.5 показывает, почему полного critical continuation этого
first jet всё ещё нет. §6.1 сохраняет остаток другого density/coframe lift.

Теперь требуются исходный physical primitive admission и полная price map
**того же** процесса, а не ещё один field→heat matrix adapter. Нужно
связать подготовку, child-dependent clocks, actual spatial measure и
controller/archive costs со всеми их источниками. Основания применяются
через primitive/outcome/tensor/refinement diagrams; совпадение текущего
эффекта или произвольно запрограммированного Q их не заменяет. Это не разрешение
добавить `I_boost` или иной compensator к действию. Все остальные
heat, metric, matter, link, shift, controller и archive equations остаются;
временное обновление полей, fixed-source/raw-owner terminal и физическая
ОТО не объявляются замкнутыми.

Свежие результаты того же SOURCE сохранены и потребляются в своих областях.
[Fixed-branch rigidity](A4D_NATIVE_ISOMETRIC_COMMON_PROCESS_METRIC_RIGIDITY.md)
показывает, что общий конечный unitary word и согласованное isometric
embedding сохраняют полный comparator metric; сами по себе они не дают
нового геометрического разрешения.
[Flat factor shear](A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md) имеет нулевой
source исправленной AF preparation price на том же probe, где собственный
положительный heat source ненулевой; дополнительные источники не определены
нужным значением для его отмены.
[Rest-coordinate step](A4D_NATIVE_COMMON_PROCESS_DOMAIN_OBSTRUCTION.md)
выводит именно прямое `m0→U_+m0` за probability domain. Она не подменяет
другую ещё не выведенную raw evolution `m'=U_s m`,
`m0'=rho(F')⁻¹m'`. Эти границы согласованы с (3)–(4): rest coefficients,
raw CAR matter и actual endpoint transport нельзя отождествлять.
Новая точка §3.1 даёт literal raw ring-вход и actual output;
для него исключены **все** frame-исправления при неизменном native `q`.
Это требование к замкнутости данного engine/readout adapter, а не
обязательное временное q′-правило вариационной теории. Её следующий шаг —
совместный linearized Euler kernel на bounded stored-native классе §0.3,
с actual first link/observer velocities и всеми строками (0). Для
конкретной native wave second matter lift уже построен, но (7m)
строго исключает её first velocity из critical kernel. Это меняет
следующий вычисляемый объект, не объявляя все curved roots невозможными.
В (12)–(16g) уже сохранены Gram, constraint-curvature, coherent
preparation и normalizer члены для этого вычисления. Непосредственно
вычислена равномерная оценка обратного блока подготовки, но не обращён
полный field Hessian и не отождествлены разные operator owners.

## 8. Проверка изменённого расчёта и повторное использование прежнего

`certificates/a4d_native_complete_field_source_check.py` содержит единый
вход для пяти consumers: прежние `record_frame_source`,
`lorentz_link_transport`, `preparation_measure`, `record_heat_continuation`
и новый `stored_rotational_wave`.

Прежний полный запуск781 conditions (119/56/376/230) остаётся evidence
публикации713edc1a: normal/optimized outputs были идентичны. В этой
итерации эти расчёты **не повторялись**. Проверены неизменность четырёх
source files и14 их definition pins, в том числе actual native Lean
operator, v8 proof/receipt и actual AF inclusion. Их результаты повторно
потребляются в тех же областях; изменения других main-пакетов их inputs
не затрагивают.

Новый consumer исполняет14 содержательных групп: actual full16 CAR;
whole-class positive bridge с разными endpoint observers; native
rotational/radial jets; все128 matter first/second equations и их repair;
вне-shell full16 identity для scalar thermal reduction; exact feature
carrier/normalizer и полный outward directional Hessian. Normal —1.520s,
optimized —1.461s, scientific JSON побайтно идентичен. Был запущен именно
этот изменённый consumer. Совокупный пяти-consumer запуск заново не
заявляется. General whole-class/jet/range proofs независимо сверены,
finite controls не заменяют их кванторы.

Определения и старый root rectangle закреплены SHA256. Root search,
старые470/781/central95/history925 suites, receipt generators и Lean builds
не повторяются. Accepted main, включая ранее выполненную Lean-работу и
новый рабочий flow, интегрирован. При конечной проверке обнаружено, что
#310 был закрыт без merge во время исходной работы; её checkpoint не
обозначал нового исполнения. После явного разрешения пользователя
продолжение открыто в Draft #334 от актуального main, с сохранённым
SOURCE `4d19564d`. Старый PR остаётся закрытым. Принятые результаты
#330/#332/#333 сохраняются вместе с пакетом; их потребление описано во
[входном синтезе](MEMO_A4D_JOINT_RESPONSE_DECOUPLING_MICROSTRUCTURE.md#accepted-support-at-the-continuation-baseline).
Не регистрируется physical action, новый task или original-parent terminal.


При переносе в #334 сохранены 1218 дополнительных research-файлов SOURCE
и все пять research-файлов нового baseline main. Интеграторские вступления
обновлены; scientific consumers и исходные пользовательские файлы сохранены
побайтно. Старые781 conditions и новый14-group result повторно не запускались:
сверены четыре consumer hashes,14 definition pins и новый consumer hash.
Два перенесённых `04_CERTIFICATES`-скрипта прошли узкий replay. Структурные
проверки, work/views, agent protocol, claim-strength и artifact-freshness
прошли. Узкая проверка двух перенесённых shift-irrelevance Lean-лемм
не завершилась за45s; это DEFERRED, не новый PASS. Полная Lean/затронутая
научная проверка потребуется перед Ready; текущий PR остаётся Draft.
