# Истории → плотность → coframe: единая первая-порядковая сборка

16 октября 2026. SOURCE #310. Научный вход закреплён на
`4c9de03cce23893aa0fbd439122a4dfcef593bd8`.

**Статус:** новое конструктивное чтение золотых историй; точная конечная
теорема о плотности/coframe и всех вариациях; условная полная
Einstein–scalar реализация с явным искривлённым решением. **Это не доказательство,
что новый составной функционал выбран физическими примитивами D0.**
В частности, положительная record-кривизна не заменена Lorentz–Palatini
членом. Старые Lorentz observer, flat-shear, same-program и raw-owner
ограничения не отменяются. Никакой новый физический action/claim не регистрируется.

## 0. Что соединяется и что не надо доказывать повторно

Используются существующие результаты:

- `A4D_NATIVE_GOLDEN_COST_REFINEMENT.md`: действительные F/R-цилиндры,
  веса p и p², полный срез стоимости и буквальное Fibonacci-включение.
- `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`: полный источник
  подготовки, KL-mass и coherent gaps; настоящая Lorentz link; ограничение
  strictly inherited clocks не более чем 16 атомами.
- `A4D_COHERENT_COMPILATION_COST_DESCENT.md`: полноценное сравнение после
  coherent completion, добавочная постоянная кодовая цена, а не бесплатный
  controller; conditional normalized-volume вариант остаётся отдельным.
- `A4D_NATIVE_PREPARATION_STATIONARY_SOURCE.md`: минимум фактической
  терминальной второй AF-цены, не принцип минимизации всей физики.
- `A4D_FULL4D_VERIFIED_INTAKE.md`: буквальный naked-star sector и его
  конечные exact connection sheets, без metric/matter stationarity.
- `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md` и
  `A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md`: ограничения физического применения.

Главное предложение: **не требовать заранее совпадения вероятности историй
с объёмом ранее выбранной метрики.** В первом порядке связь чувствует
плотность обратной метрики. Вес и coframe можно соединить на уровне полного
действия, сохранив Lorentz-связь и все независимые уравнения.

Три типа утверждений ниже различны. (I) Конструкция из существующей меры
при явно заданном новом clock-rule. (II) Общая точная теорема для quadratic
anchor-Palatini сектора. (III) Условный мост к полному действию D0.
Примитивный допуск clock-rule и принадлежность полного price к типу (II)
не объявляются следствиями алгебраической правильности конструкции.

## 1. Конструктивные child-dependent clocks из той же меры

Пусть p=(sqrt(5)-1)/2, p+p²=1. Сохраняем все исходы F и R, стоимости
1 и 2, веса p и p². Начинаем с ориентированного координатного куба [0,1]^4.
Четыре роли уже даны; это не новый вывод физической размерности.

На j-м **сыром** символе меняется координата j mod 4. Если её текущий
интервал [l,l+d], то

    F: [l,l+p d],               R: [l+p d,l+d].                  (1)

Длина R-интервала равна p²d. Все остальные координаты сохраняются.
Таким образом каждому конечному слову w соответствует прямоугольник B_w,

    |B_w|=p^cost(w)=mu(w).                                      (2)

Это буквальное равенство меры цилиндра и координатного объёма адреса.
Оно не использует заданную физическую метрику, оптимизацию распределения,
выбранный гладкий объём или отбрасывание неудачных историй.

Уровень n берётся по **исходному срезу накопленной стоимости**: минимальный
сырой префикс, достигший n. Его стоимость n или n+1. Лист стоимости n
разделяется в следующий раз, ожидающий лист n+1 переносится без исполнения
второго независимого шага. Поэтому набор B_w является полным разбиением
куба на каждом срезе; мера всех адресов равна 1.

Clock X_n — центр B_w. Сохранять в Z[p] можно пару концов либо удвоенный
центр; сам вывод центра — фиксированное линейное чтение. Это не утверждение,
что четыре clock values уже являются конкретными mask-компонентами
engine `Z[a]^16`. Память конечного префикса растёт вместе с глубиной.

Для разделяемого листа прямое вычисление даёт

    p centre(B_wF)+p² centre(B_wR)=centre(B_w).                   (3)

Следовательно, X_n — ограниченный martingale именно на cost-cut filtration,
но **не** strictly inherited clock. Дочерние значения действительно меняются.

Сырой префикс данного среза имеет длину не меньше ceil(n/2); каждая роль
обработана не меньше floor(n/8) раз. Поэтому

    diam(B_w) <= delta_n := 2 p^floor(n/8) -> 0.                 (4)

Вложенные прямоугольники определяют X_infinity. Их максимальный диаметр
стремится к нулю, а их объёмы равны вероятностям цилиндров. Для любой
Lipschitz test function f

    |sum_w mu(w) f(X_n(w)) - integral_[0,1]^4 f(x)dx|
            <= Lip(f) delta_n.                                 (5)

Это доказывает (X_infinity)_*mu = Lebesgue([0,1]^4), без статистической
экстраполяции конечной таблицы. Границы прямоугольников имеют нулевую меру.
Имеется конкретное неатомарное чтение тех же историй, не опровергающее
теорему о strictly inherited clocks: её гипотеза здесь намеренно не выполнена.

**Вынужденность ограничена классом:** если потребовать упорядоченные
неперекрывающиеся affine children с длинами, равными тем же вероятностям,
то относительная точка разреза p однозначна. Выбор четырёх ролей, их порядка,
адресного куба и физического допуска этого record-update не выведен из M1.
Это готовый конструктивный вход для M06, а не повтор его общей error-tooling задачи.

При гладком последующем отображении Psi из адресов в наблюдаемый chart
мера есть Psi_*dx и включает настоящий Jacobian и его derivative.
Psi не назначается так, чтобы получить желаемую метрику: его закон остаётся
физическим входом. Пример из §6 использует явную Psi только как контроль.

## 2. Полная цена переносит не только среднюю стоимость

Существующий полный источник для отмеченной AF-подготовки имеет структуру

    A = K + sum_a w_a f_a + D(w||r)/ell + C_coh,
    ell=log(phi),  C_coh=D(Y||pinch_address(Y))/ell.               (6)

K — соответствующая постоянная кодовая часть. Conditional blocks, их
цены и области здесь берутся у исходного владельца. Нельзя произвольно
заменить его полный канал commuting формулой, если нужная блочная
декомпозиция не установлена. Внутри объявленной декомпозиции (6) сохраняет
coherences через последний **определённый** член.

Наши новые геометрические адреса имеют r_a=mu(B_a)=|B_a|. Они не
отождествляются с прежними спектральными setting labels по одному имени;
для реализации локальных conditional programs нужна их явная адресная
композиция. Для любой уже заданной local price f и этих адресов

    w_a^* = r_a exp(-ell f_a)/Z_n,
    A_n^*-K = -log Z_n/ell,
    Z_n=sum_a r_a exp(-ell f_a).                                (7)

При f_a=f(X_n(a)) и достаточной равномерной C1-регулярности

    Z_n -> integral exp(-ell f(x))dx,
    A_n^*-K -> -log integral exp(-ell f(x))dx / ell.              (8)

Оценка (5) применяется к exp(-ell f) и к его полному parameter derivative.
Если |f|<=M, |df[V]|<=B||V||, оба эти поля имеют равномерные Lipschitz
константы, Z_n,Z>=exp(-ell M), то value и envelope-source errors не больше
C delta_n ||V|| с соответствующим C(M,B,Lip f,Lip df). Например,

    dA_n^* = sum_a w_a^* df_a,
    dA^* = integral e^(-ell f) df / integral e^(-ell f).           (9)

Движение Psi даёт grad f · dPsi в df. Moving reference probabilities
добавляют уже принадлежащий source owner член −E_w[dlog r]/ell.
Это реальная контролируемая clock/refinement construction. Она не
устанавливает пространственную raw-norm оценку для исходного #310 без
соответствующего source reconstruction.

Важно: (8) — **free energy, не normalized mean f**. KL-mass term из (6)
нельзя удалить. Полностью непрерывная запись того же классического сектора:

    A=K+integral f dnu +(1/ell) D(nu||eta)+C_coh,                 (10)

где eta — reference measure адресов, nu — действительная probability.
Дальнейшая сборка сохраняет оба поля мер вместо постулата nu=dVol/V.
Полный некоммутирующий source вне commuting address sector остаётся
BKM-формулой исходного владельца.

## 3. Плотность и coframe образуют одну геометрическую переменную

### 3.1. Кинематика в четырёх измерениях

Пусть e — невырожденный Lorentz coframe, g=e^T eta e, eta=diag(1,-1,-1,-1),
nu=m(x)d^4x, m>0. Фиксируем ориентационный chart, v=|det e|>0 и

    chi=m/v,       ehat=sqrt(chi)e,
    ghat=chi g,    vhat=sqrt(|det ghat|)=chi²v.                 (11)

Тогда точно

    m g^-1 = vhat ghat^-1,
    e=sqrt(m/vhat) ehat,      g=(m/vhat) ghat.                   (12)

(11) — гладкая обратимая смена **всех** coframe/measure variables, не
matching graph меньшей размерности. Positive chi сохраняет Lorentz signature
и causal cones; не получается перехода Riemannian→Lorentz заменой знака.

В d>2 соответствующие степени: ehat=chi^(1/(d-2))e,
ghat=chi^(2/(d-2))g. Особая простота d=4 — квадратный корень; d=2
этой обратимостью не покрывается. Число четыре не выведено этой формулой.

### 3.2. То же равенство на буквальном конечном star-sector

В сохранившемся naked-star действии coframe каждого anchor x входит только
квадратично, через wedge(e_u(x),e_v(x)); полная odd plaquette зависит от
четырёх Lorentz links, но не от coframe. В нормировке исходного файла

    P_x(e,U)=sum_(r<s) sign(r,s,u,v)
       wedge(e_u,e_v)^T G2 STAR [(C_rs eta)_ab]_(a<b),
    C_rs=(U_plaquette-eta U_plaquette^T eta)/2.                 (13)

Тот же G2, STAR и все шесть faces сохранены. Поэтому **на любой конечной
сетке, без малости chi, гладкости и expansion по шагу**

    sum_x chi_x P_x(e,U)=sum_x P_x(sqrt(chi_x)e,U).              (14)

Если v_x — геометрический объём ячейки, а w_x её probability mass,
то chi_x=w_x/v_x и левая часть есть sum_x w_x(P_x/v_x).
Координатные cell weights, если они используются в P_x и v_x, фиксируются
одинаково. Нельзя умножить дважды на h^4 или назвать normalized trace raw sum.

Это не назначение нового scalar R. Это полная конечная polynomial identity
существующего **геометрического сектора**, включая every link source.
Она не говорит, что весь spectral/heat/AF action равен этому сектору.

Для coordinate link D_st=e_s^-1 U_st e_t сохраняем тот же внутренний U:

    Dhat_st=sqrt(chi_t/chi_s) D_st,
    Dhat_st^T ghat_s Dhat_st=ghat_t.                            (15)

Все endpoint derivatives сохраняются. Scalar factors телескопируются на
замкнутом цикле: loop holonomy не изменяется. Никакая boost-часть полного
Lorentz transport не заменяется его observer-unitary частью. При полном
CAR exterior lift действует исходная functoriality на всех16 grades.
Это смена геометрического представления, не разрешённый temporal engine-step.

### 3.3. Почему нельзя сначала устранять связь

В continuum first-order tetrad notation (14) становится

    integral m g^(mu nu) R_mu nu(e,omega)
      = integral vhat ghat^(mu nu) R_mu nu(ehat,omega).          (16)

Полный internal Lorentz connection omega остаётся тем же. Порождаемые
coordinate affine connections отличаются scalar projective shift
(1/2) delta^lambda_nu partial_mu log chi, поэтому their antisymmetric
curvature/Ricci contractions and the displayed scalar-density identity
are consistent. Original torsion need not vanish; varying omega sets the
torsion of **ehat**, not of e, to zero when no spin source is present.

Если заранее потребовать omega=Levi-Civita(e), этой вариационной задачи
больше нет: это другая система с производными chi. Тем более (16) не
заменяет уже выведенное R_h=-R_g+observer-terms для positive-record metric h.
У source owner эти terms реальны и сохраняются в любом полном применении.

## 4. Все уравнения, а не только значения действия

Рассмотрим следующий **условный consumer** структуры (6):

    S(e,U,w,psi)=Phi(ehat,U,psi)
              +(1/ell) sum_x w_x log(w_x/r_x)+K,
    ehat_x=sqrt(w_x/v_x(e))e_x,  w_x>0, sum_x w_x=1.             (17)

Здесь Phi — заявленный исходный quadratic-anchor density: например P,
либо P плюс quadratic scalar/sigma kinetic density той же степени два по
coframe. В исходных variables первая часть есть sum w_x Phi_x(e)/v_x(e).
**(17) не объявлен уже выбранной полной физической ценой D0.**
Это явный критерий, который должна обеспечить её independently derived
same-program source identity; ниже он доведён до конца, а не оставлен ansatz.

Пусть K,r фиксированы, а остальные источники в Phi не отброшены. При
фиксированном w настоящий differential coframe map:

    delta ehat=sqrt(chi)[delta e-(e/2)Tr(e^-1 delta e)].          (18)

На 4x4 матрицах trace reversal X→X−(Tr X)I/2 является involution.
Следовательно (18) имеет ранг16 и явную обратную. Для covariant metric

    delta ghat=chi[delta g-(g/2)Tr(g^-1 delta g)]                 (19)

также имеется обратная на **всех10** symmetric slots.

Если Ehat — coframe Euler Phi с полным Frobenius pairing, получаем

    E_e=sqrt(chi)[Ehat-(<Ehat,e>/2)e^-T],
    E_U=Ehat_U,
    d_w S = <Ehat,ehat>/(2w)+(log(w/r)+1)/ell.                  (20)

Нормировка даёт один общий multiplier. Из E_e=0 следует Ehat=0,
не только trace-free часть. Тогда геометрический член в последнем
уравнении исчезает **потому, что исполнены полные coframe equations**,
а не потому, что он был заморожен. Probability equation даёт w_x=r_x.

Таким образом на этом faithful sector

    stationary S  <=>  stationary Phi AND w=r.                  (21)

Все link/psi equations из Phi сохраняются. Обратное направление конструктивно:
из любого nondegenerate joint critical point (ehat,U,psi) берём w=r и
получаем e из (12). Отсюда новые probability variables не требуют
выбрасывать metric rows либо выбирать special gauge/source projection.
Метрическое matching с independently defined record-readout этим не доказано.

### Полная Hessian и стабильность подготовки

На critical point full Hessian исходных variables есть congruence pullback
Hessian системы (17) в variables (ehat,U,psi,w). Там блоки geometric Phi
и probability entropy разделены. Для sum delta w=0

    delta² D(w||r)|_(w=r)=sum_x (delta w_x)^2/r_x >0.            (22)

В relative-score coordinates delta w=r delta s, E_r(delta s)=0,
эта форма равна sum r(delta s)^2. Никакой uniform bound на Euclidean
inverse diag(1/r) при r→0 не заявляется: именно Fisher/weighted norm
обеспечивает размерностно-независимую preparation coercivity.

Связанные zero modes/нестабильности Phi не уничтожаются энтропией; она
не превращает indefinite gravitational Hessian в положительный минимум.
На rank-deficient amplitude boundary остаются известные critical branches,
поскольку w-chart здесь требует строго положительных masses.

### Неподвижная кодовая добавка

K→K+k не меняет (20)–(22). Локальный constant price b даёт sum w b=b,
а не b sum v. Поэтому он лишь сдвигает normalisation multiplier и не
создаёт искусственный cosmological source. Это следует из исходного
вероятностного summation, а не из вычитания desired vacuum energy.
Прямой independently present volume term, changing depth k или moving
reference имеет собственные derivatives и остаётся в residual.

## 5. Откуда в этом consumer появляются Einstein equations

Пусть continuum Phi — Lorentz tetradic Palatini плюс connection-independent
massless scalar kinetic term:

    Phi = integral sqrt(|ghat|)
        [c ghat^(mu nu) R_mu nu(omega)
             - (1/2) ghat^(mu nu) partial_mu psi partial_nu psi] d^4x.
                                                                    (23)

c nonzero и convention зафиксированы. Это **условный first-order sector**,
не новая физическая постулированная модель D0. Его геометрический компонент
имеет исходного naked-star/smooth-Palatini владельца, но соответствие
полного spectral price этому source остаётся недоказанным.

В оригинальных variables kinetic term также имеет степень два по coframe,
поскольку sqrt(|g|)g^-1 имеет степень d−2=2. Одна и та же density map,
а не разные калибровки, переносит и его, и gravitation.

Полная вариация omega, ehat, psi даёт

    omega=Levi-Civita spin connection(ehat),
    2c G_mu nu(ghat)=partial_mu psi partial_nu psi
                       -(1/2)ghat_mu nu |dpsi|²_ghat,
    Box_ghat psi=0.                                             (24)

Вероятность и clocks несут собственные equations из §4 и ниже. Получена
вся nonlinear система данного consumer, не только leading flat symbol.
Spin-coupled CAR matter может дать torsion/hypermomentum; его нельзя
подменить скаляром и объявить из (24) pure GR для всей native материи.

Для n scalar/sigma полей с target metric G_AB(psi), независимой от coframe,
тот же аргумент сохраняет единственную density map. Target metric может
быть вычисленной информационной формой прежних внутренних record modes;
то, что её quadratic form уже известна, ещё не выбирает её физическим
kinetic action. Potential density (degree0 scalar L), gauge density degree2
in inverse metric и higher-curvature residual не имеют того же scaling law.
Они не удаляются; их exact pullback должен быть дифференцирован отдельно.

Если reference measure представлена genuine clock density
eta=r_X d^4x, r_X=|det DX|/Z_X, то variation X также не отбрасывается.
В случае (17), при w=r_X log(w/r_X)=0, first reference variation
−sum w dlog r/ell=−sum dr/ell=0. Поэтому полная matched prior решает
clock/reference equation при фиксированной total mass, с включённым
normalizer/boundary derivative. Это не превращает arbitrary mathematical
clock germ в допущенный native update.

## 6. Явная совместная неплоская реализация, не только условие существования

На local finite coordinate domain (u,v,x,y) зададим

    dshat² = 2 du dv + H du² −dx²−dy²,
    H=(s²/(4c)+a)x²+(s²/(4c)−a)y²,
    psi=s u.                                                   (25)

Непосредственное вычисление всех Christoffel/Ricci components даёт

    det ghat=−1,
    Ric_uu=s²/(2c), R=0,
    |dpsi|²=0, Box psi=0,
    2c G=T.                                                    (26)

При s=0,a≠0 это curved Ricci-flat vacuum: Riemann не равен нулю.
При s≠0 сохраняется настоящий ненулевой matter source T_uu=s².
Это классический pp-wave тип; новизна общей pp-wave формы не приписывается D0.
Здесь он проверяет **все** уравнения conditional measure/first-order сборки.

Возьмём на x∈[0,1]

    r(x)=1+epsilon(2x−1), |epsilon|<1,
    X²=(1−epsilon)x+epsilon x²,

остальные clocks — identity. Это положительный нормированный Jacobian:
X²(0)=0, X²(1)=1, dX²/dx=r. Golden address measure из §1 переносится
inverse clock map именно в r(x)d^4x. Положим w=r и

    g=r ghat, v_g=r², chi=1/r.                                 (27)

Здесь **мера w не совпадает с объёмом исходной g**. Тем не менее (12),
(21) и (26) дают полное решение (17),(23), включая density, reference,
metric, scalar и independent connection equations. Локальный on-shell
cost cR−|dpsi|²/2=0; code constant компенсируется только multiplier
нормировки, а не curvature/source fit.

Используются compact variations либо согласованные boundary data.
Это не глобальное решение всех топологических/каузальных условий,
не exact native finite-lattice root и не представление (25) через
engine-admitted Z[a]^16 на всех уровнях. В частности, это не новый
terminal исходного fixed smooth source / raw-norm question #310.

## 7. Как это применяется к настоящей полной цене, не заменяя её

Для ЛЮБОЙ реально заданной native S(e,U,w,m,...) можно выполнить
обратимую замену (11) и сохранить все source terms. Наличие отдельно
известного Einstein-like чтения не устанавливает (17).

Содержательное следующее утверждение должно иметь вид

    d S_native = D(ehat,U,w,...)^* d[Phi + KL/ell + R_actual]
                     + r_refinement,                          (28)

где R_actual вычислен из действительного собственного процесса:
observer, preparations, controllers, heat, anisotropic measure, interactions,
and archive terms, а не определён как разность до желаемого Einstein tensor.
Допустима доказанная source equivalence; не требуется совпадение всех
нефизических представлений action.

Если коэффициенты chi и coframes остаются в compact nondegenerate domain,
(18) и его обратная имеют uniform pointwise bounds. Их dual maps тогда
ограничены также в ненормированных raw l1 суммах без множителя числа узлов.
Так transfer ошибки имеет реального потребителя. Но measure quadrature
из (5),(9) сама по себе не даёт нужного r_refinement для полных native
Euler rows: нужна spatial/action reconstruction и её derivative.

### Что новый ход действительно снимает

Для first-order sector не требуется сначала доказывать nu=dVol_g/V_g,
затем separately выбирать density coupling, затем выкидывать extra scalar
уравнение. Probability density и coframe образуют одну плотность обратной
метрики; связь и полный coframe variation определяют её геометрию,
а preparation/source equation остаётся независимо проверяемым.

Clock construction показывает, что конечные фиксированные атомы не являются
неизбежным следствием самой golden tower. Full coupled control показывает,
что независимая мера не исключает nonlinear Einstein dynamics или matter.
Это два конкретных снятых препятствия **в объявленном конструктивном классе**.

### Что нельзя скрыть этим синтезом

1. Native physical Info и terminal versus sum-of-stages action не выбраны.
2. Clock rule (1) ещё не выведен как admitted combined m/q/D/b evolution.
3. R_h positive-record curvature, его observer correction и native Lorentz
   Palatini sector остаются различными. Density rescaling не меняет signature
   и не устраняет реальный leading observer source.
4. Corrected AF-price flat-shear source остаётся нулевым при ненулевом heat.
   Ни KL equilibrium, ни перепараметризация не создают недостающую силу из нуля.
5. Никакая faithful minimizing density не объявляется автоматически physically
   preparable или attractive под действием реального engine.
6. Actual normalization, rank births, full16 matter, shifts и spatial refinement
   не заменяются конечным числами checks или новым выбором gauge.

Таким образом это не повтор normalized-GR предложения. В нём делили весь
geometric action на V и получали глобальное consistency condition.
Здесь сохраняется **локальная independent probability field и first-order
connection**, а coframe преобразуется до исключения connection. Это другой
conditional consumer с другой системой уравнений. Их физический выбор должен
решать actual native price, не стратегическое предпочтение автора.

## 8. Проверка и границы интеграции

`check_density_palatini.py` воспроизводит construction cost cuts 1…9,
all branch volumes, martingale clock laws, exact centroid moments; faithful
probability/source/Hessian controls; literal Lorentz star contractions,
all16 coframe и24 one-site periodic-link tangent checks, all10 symmetric
metric inverses, full coordinate-link constraints; all10 Einstein–scalar
rows, scalar Euler, nonflat vacuum member и nonconstant measure/clock example.

Общие всеуровневые и вариационные теоремы доказываются выше; конечные checks
их не заменяют. Ordinary и optimized output совпадают. Четыре реально
изменённые формулы отвергнуты на математике: повторное исполнение pending
return, неверная степень density scaling, замороженная volume derivative,
неправильный коэффициент coupled wave. Изменённые tests исполняют только
соответствующую часть того же кода, не старые suites и не JSON-only checks.

Существующие owner bytes не изменены. Нет нового Lean доказательства,
самостоятельной независимой научной приёмки, full old-certificate replay,
нового рабочего task/agent или physical/CORE/GR promotion.

Математический контекст: independent-measure first-order models рассмотрены
Guendelman–Kaganovich, gr-qc/9611046 и gr-qc/9702058. Они не импортируются как
physical axioms D0. Их наличие показывает, что самостоятельная мера не
обязана прежде совпасть с metric volume, чтобы возникла Einstein frame.
Вклад этого продолжения — конкретные golden child clocks, полный finite
star/coframe/source consumer и явное соединение с retained entropy/control
ограничениями именно текущей D0 цепочки.
