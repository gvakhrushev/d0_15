# Совместная первая поправка: подготовка и полный causal source

17 октября 2026. Тот же Draft #334, исходный SOURCE `caa90af1`.
Потребитель: действительное продолжение совместных полей и подготовки в
[causal source bridge](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md), §7.1.

**Получено.** На прежнем winding cone решено действительное ведущее
уравнение масштаба при неизменных v8-параметрах. Затем полностью решён
вопрос существования первого совместного jet для общей vacuum/top
подготовки: его нет. Амплитудное уравнение допускает явную поправку
связи только для чистой вещественной несбалансированной линии. Полное
полевое уравнение того же действия требует ровно противоположного
условия — баланса двух масс. На этом балансе амплитудная невязка имеет
строго положительную нижнюю границу при любых реальных первых полевых
поправках, любом ранге и комплексной когерентности внутри этой плоскости.

Вместе с [предыдущим E0-результатом](A4D_CONE_REAL_E0_FIELD_CORRECTION.md)
это исключает всю общую вещественную coordinate-form E0 подготовку
данного cone/first-shell семейства с differentiable order-h полями.
Следует прекратить поиск очередного её projector или counterjet.
Другие ведущие состояния/геометрии, межмоментные когерентности,
недифференцируемые по h семейства и физически выведенная иная полная цена
не исключены. Исходный fixed-g/fixed-tau/raw terminal остаётся OPEN.

## 1. Один и тот же оператор, цена и первые уравнения

Используются [полный источник подготовки](A4D_CONE_SOURCE_BALANCED_PREPARATION.md),
[actual first stencil jet](A4D_CONE_PREPARATION_FIRST_CORRECTOR.md),
[второй heat/source remainder](A4D_SECOND_ORDER_HEAT_REMAINDER.md).
Тор имеет период2pi и нормированный объём, y=x2. Пишем

    a0(y)=(cos y,sin y,0,0),
    g=s^2(2a0 a0^T-I), G=s^2 I, coordinate torsion=0,
    D0=(1/s) sum_r gamma_r partial_r,
    Delta0=-sum_r partial_r^2/s^2,
    Sigma={+/-e_r}, P=P_Sigma, epsilon0=1/s^2.

Здесь a0 — координатное направление Lorentz cone; оно отличается от
внутреннего observer n=e0. У настоящего proper-LC forward stencil
Delta_h=Delta0+h A1+O(h^2), A1={D0,D1}. Все16 grades, восемь занятых
momenta, полный thermal trace и reference128 сохраняются.

Общая рассматриваемая подготовка:

    V=span{|0>,|15>},
    sigma=[[r,z],[conjugate(z),1-r]]>=0, Tr sigma=1,
    rho0=(P_Sigma/8) tensor sigma, delta=2r-1.

Она может иметь rank8 или16 на полном128 shell. Фактор1/8 относится
к восьми momenta; rank2 V не заменяет full16 operator или вариации.
Любой C0 с C0 C0*=rho0 имеет полную retained reference реализацию.

Допускаем реальные гладкие первые поправки всех10 G slots, всех24
torsion slots, меры и самой causal геометрии, и произвольный C1:

    Delta_h=Delta0+h(A1+X_v)+o(h),
    C_h=C0+h C1+o(h), epsilon_h=epsilon0+h epsilon1+o(h).

Все expansion/source hypotheses берутся из controlled smooth chart
предыдущих владельцев; в частности это differentiable h-jet, а не
утверждение о любой ограниченной последовательности матриц.
Необходимое амплитудное уравнение:

    (Delta0-epsilon0)C1+(A1+X_v-epsilon1)C0=0.          (J1)

Ни C1 вне shell, ни moving normalizer не меняют его P-проекцию.

## 2. Настоящий ведущий масштаб существует при прежних калибровках

Здесь beta=3-sqrt(5), z_coin=2^-20, M=128. Они не зависят от полей
в рассматриваемых вариациях. Для всех lattice momenta p in Z^4 положим

    lambda_p=|p|^2/s^2, E_p=exp(-beta lambda_p),
    Z=16 sum_p E_p,
    kappa_p=-E_p/Z+M beta z_coin E_p/(1-z_coin+z_coin E_p).

Полный leading radial equation:

    E_scale(s)=s^-2+16 sum_p kappa_p lambda_p=0.        (J2)

Все ведущие10 metric и24 torsion equations для данной momentum-diagonal
семьи следуют из (J2) и равных масс1/4, как доказано в source-balanced
владельце. Это явный ведущий conditional matrix/source фон.

Обозначим Theta(t)=sum_k exp(-t k^2), U(t)=sum_k k^2 exp(-t k^2).
Тогда Z=16 Theta(beta/s^2)^4 и
T_j=Tr Delta0 exp(-j beta Delta0)=64 U(j beta/s^2)Theta(j beta/s^2)^3/s^2.
При R=z_coin/(1-z_coin)<1 получаем тот же полный feedback:

    E_scale=s^-2-T_1/Z
       +M beta z_coin/(1-z_coin) sum_(j>=0)(-R)^j T_(j+1). (J3)

Новый интервальный расчёт даёт единственный корень внутри [12/5,5/2]:

    828378943/335544320 < s_* < 12943421/5242880,
    2.468761631846428 < s_* < 2.468761634826661,
    0.937328249 < M z_coin beta Z(s_*) < 0.937328254 <1.

Знаки E_scale(12/5)<-0.2526, E_scale(5/2)>0.1225 и положительная
производная на16 покрывающих интервал boxes доказывают существование
и уникальность именно в этом интервале. На последнем bracket
3.8430956<E_scale'<3.8430961. Исходные parameters остаются прежними;
решается собственное уравнение масштаба, а не выбирается running coupling.
s_*>1 также даёт strict local Julia domain при достаточно малом h.

Расчёт использует32 Gaussian modes в каждом одномерном моменте, с
геометрически ограниченным хвостом. Для степени d=0,2,4 его отношение
после k=33 не превосходит ((k+1)/k)^d exp[-t(2k+1)]<1.
В feedback оставлены j=0,...,3; абсолютный хвост ограничен
R^4 T_1/(1-R). Для производной используются T_j<=T_1, U2_j<=U2_1,
|T_j'|<=(2/s)(T_1+j beta U2_1), с точными geometric sums.
Полный multiplicity16 и производная глобального Z сохранены.

## 3. Решение ВСЕГО резонансного amplitude system на V

Далее s вынесен явно. В q=0 блоках все metric/epsilon responses
действуют на V и ортогональны two-form outputs. Measure mean равен0,
а настоящий changing-frame commutator [K,Delta0] на shell равен0.
Все реальные24 torsion means остаются, без сокращения до SO3.

Соберём two-form outputs на четырёх отрицательных осях. Пусть t in R24
— constant orthonormal torsion coefficients. Literal full16 CAR дают
точные матрицы M_vac и M_top=M_vac K, где

    M_vac^T M_vac=I24, K=K^T, K^2=I24.

Для фактического A1 forcing существуют u,v in R24:

    u: t^0_02=1/2, t^1_12=1/2,
    v: t^0_13=-1/2, t^1_03=1/2,
    |u|^2=|v|^2=1/2, u.v=0, Ku=-v, Kv=-u.             (J4)

Все остальные их компоненты нулевые. Это координаты полного torsion
image, а не новый выбранный source. Для общей sigma точный вклад q0
two-form rows в квадрат нормированной амплитудной невязки равен

    [t^T(I+2 Re(z)K)t-2 delta t.u+1/2]/(4s^4).         (J5)

Пары +/-momenta дают коэффициент2/8=1/4. Проецирование остальных
выходов только уменьшает norm; complex reference purification не
меняет (J5), поскольку норма равна trace с той же rho0.

При delta=0 positivity sigma даёт |2 Re(z)|<=1. Поэтому

    ||P(A1+X_v-epsilon1)C0||_HS^2 >=1/(8s^4)>0.       (J6)

Нижняя граница едина для pure/mixed states, любой комплексной фазы,
всех реальных первых полевых jets и reference128. Для нормированного
Euler coefficient 2(Delta-R)C квадрат границы равен1/(2s^4).

Более того, весь q0 system совместен ровно для real rank1 sigma
с delta!=0. При |2 Re(z)|<1 минимум (J5) равен

    [det sigma+(Im z)^2]/[2s^4(1-4(Re z)^2)].          (J7)

Граничные |2 Re(z)|=1 — balanced GHZ signs, уже исключённые (J6).
Для real normalized line chi=A|0>+B|15>, A^2!=B^2, решение q0 явно:

    t0=[(A^2+B^2)u+2ABv]/(A^2-B^2).                  (J8)

Это решение не повышено до совместного field root. Ненулевые forced
resonant Fourier blocks тоже решены, а не отброшены:

    t^2_02(q=+/-2e2)=-1/4,
    t^2_12(q=+/-2e2)=+1/4,
    H_metric=measure=epsilon1=0.                      (J9)

В пространстве это t^2_02=-(1/2)cos(2y), t^2_12=+(1/2)cos(2y).
Они отменяют оба forced offdiagonal A1 blocks на ВСЕЙ V. На остальных
разностях Sigma-Sigma forcing на V равен0. Следовательно (J8),(J9)
решают все резонансные first-amplitude rows для каждой unbalanced real
pure line. Off-shell C1, если нужно, определяется signed resolvent
Q(Delta0-epsilon0)^-1Q, с сохранением ground modes.

## 4. Полное causal field equation исключает ровно эти unbalanced решения

Ключевое новое соединение — первая вариация ТОЙ ЖЕ цены, включая H,J,R.
На fixed positive G и coordinate torsion0 continuum action точно
не зависит от causal direction a. Это существующее operator factorization
в координатах (G,T,a,C_form,mu). Поэтому на causal test w

    X_w=0, Y_vw=0 для любого первого v,
    первый полный field residual = d_w S1,
    S1=Tr kappa(Delta0) A1+Tr rho0 A1.                 (J10)

Все terms с C1, moving normalizer и ведущей Hessian исчезают здесь по
этому точному factorization и собственному первому amplitude equation.
Это не предположение, что прочие field equations уже решены.
alpha=c0 h^2 и beta-rounding O(h^2) впервые входят на следующем порядке,
поэтому не дают потерянного order-h clock source.

Пусть M_r=-Gamma_coord,r^T — настоящие coordinate proper-link generators
из LC(g). Они tracefree, потому что det g постоянен. Из literal L1 и
его true adjoint, на полном16 для diagonal Fourier block получаем

    Tr16 A1_pp=-(16/s^2)sum_(t,r) p_t p_r mean(M_r)^t_r,
    <vac,A1_pp vac>=0,
    <top,A1_pp top>=-(2/s^2)sum_(t,r) p_t p_r mean(M_r)^t_r,
    <vac,A1_pp top>=0.                                (J11)

Член H_r^2 сохранён; его real coefficient даёт чисто imaginary
antisymmetric trace и не меняет эти диагональные выражения. Periodic
derivative_r H_r в mean интегрируется в0. Ни top expectation, ни full16
trace нельзя заменить vacuum expectation: это потеряло бы источник R.

Из isotropy и (J2)

    tau=sum_p kappa_p p_0^2=-1/64.

Положим I(a)=mean sum_r Gamma^r_rr[g_a]. Тогда ВСЯ первая цена на
рассматриваемой causal fibre равна

    S1=(16 tau+(1-r)/2)I(a)/s^2
      =-delta I(a)/(4s^2).                            (J12)

Выберем настоящую гладкую periodic variation

    a_epsilon(y)=(cos(epsilon)cos y, sin y,
                   sin(epsilon)cos y,0).

Это unit vector для каждого epsilon. Он допускает smooth orthogonal
coframe lift e=sO_epsilon и настоящие proper LC links; positive G,
coordinate T, counting measure и form-state остаются фиксированными.
Его Christoffel calculation даёт

    dI(a_epsilon)/d epsilon|0=-1/2,
    dS1/d epsilon|0=delta/(8s^2).                     (J13)

Таким образом first full field equation требует delta=0. Ни произвольная
первая поправка связи/метрики, ни C1 на shell или вне shell не отменяет
эту строку (J10). Невырожденность отдельного homogeneous Schur block
не отменяет этот **непостоянный** causal test.

## 5. Совместный вывод и его точная граница

Предположим существование полного controlled differentiable joint h-jet
с общей sigma на V. Полевое уравнение (J13) требует sigma00=sigma1515.
Тогда амплитудное уравнение нарушает (J6). Следовательно такого jet нет.
Обе возможности проверены полностью: balanced sigma нарушает amplitude,
а её единственные unbalanced amplitude solutions нарушают field source.

Имеется и uniform consumer для меняющихся ranks/states. Если евклидова
норма24 постоянных orthonormal torsion means из (J5) удовлетворяет
|t|<=L, L>=1, то из (J5)

    amplitude_residual^2 >=[1/2-sqrt(2)|delta|L]/(4s^4).

При |delta|<=1/[4sqrt(2)L] это не меньше1/(16s^4).
В противоположном случае квадрат настоящей causal-строки (J13)
не меньше1/(2048 L^2 s^4). Поэтому для этих ДВУХ явно определённых
остатков, без их переименования в исходный packed raw norm,

    max(amplitude_residual^2, |d_w S1|^2)
                  >=1/(2048 L^2 s^4)>0.              (J14)

Так preparation/rank limit не приближает обе строки к0 при bounded
first counterjets. Unbounded или fractional-order corrections требуют
другого анализа, а не подстановки в эту границу.

Для общей REAL momentum-diagonal E0 density предыдущий real-leakage
результат сначала принуждает поддержку к V. Новая теорема затем
исключает и V. Это закрывает данный real E0 first-jet маршрут целиком.
Не требуется новый перебор ranks, phases или projectors этой семьи.

Утверждение использует common sigma на всех восьми momenta. Для
независимых sigma_r старый E0 результат ограничивал только axis1;
для межмоментных когерентностей нет использованной диагональной
reference-column редукции. Complex E0 за пределами V не классифицирован.
Также не исключены иная leading geometry/shell, иной фактически
выведенный процесс или семейства без bounded differentiable h-jet,
включая дробные порядки при вырожденном совместном kernel.

Физическая admission и полная native Cost−Info цена остаются отдельной
стрелкой. [Конструктивный preparation-domain анализ](sources/d0_ghz_joint_first_jet_2026-10-17/PREPARATION_DOMAIN.md)
разделяет точную finite-word недостижимость, word closure и executor input
domain. Golden words сохраняют low/high charge; их vacuum/top limits
balanced и подпадают под (J6). Однако arbitrary sign-word closure плотен,
а принятые ring inputs vacuum-top+p^N time действительно приближают GHZ.
Глобального отделения engine domain от этой границы нет. Их admitted
подготовка/история/цена и uniform source law этим не установлены.

P1=P3=0 на V. Настоящий correlated CAR current здесь J=n и требует
сохранённого observer; norm-centering имеет rank0. Нельзя заменить его
несуществующим P1 axis или вывести physical observer из GHZ симметрии.

## 6. Проверка и использование в общем синтезе

Новый [source packet](sources/d0_ghz_joint_first_jet_2026-10-17/) содержит
полные exact matrix images, general-density residual, constructive
amplitude corrections, реальный causal source и interval scale solution.
Обычные и optimized outputs сохраняются отдельно с их input identities.
Проверяется новая математика; прежние roots, spectra и Lean не повторяются.

Результат меняет следующий consuming route: поиск ещё одной common real
E0 first correction на этом cone завершён. Дальнейшая совместная ветвь
требует действительно иного admitted leading preparation/geometry или
контроля иного scaling; её цена и все field/matter rows остаются теми же
до отдельно доказанного native action map. Ни этот scoped obstruction,
ни новый leading scale не подменяют исходный independently fixed source
и unweighted raw h^-2 comparator; общий вывод ОТО не объявлен закрытым.
