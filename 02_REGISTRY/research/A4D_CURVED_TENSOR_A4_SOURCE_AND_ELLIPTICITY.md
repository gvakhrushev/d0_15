# Искривлённый a4 и шестнадцать тензорных направлений: полный источник, эллиптичность и локальная изоляция

16 октября 2026. Существующий SOURCE #334, `gvakhrushev/d0_15`.
Вход: `a1ca6f547b9b6876c4e31801665573a1734aa65f`.

**Итог.** Вычислен полный кривой a4 того же continuum Dirac в унаследованном tensor16-классе, включая исходную Hodge-кривизну и её смешанный член. Его tensor-source при нулевом torsion vanishes на Einstein-метрике положительного G; полный metric pullback a4 там тоже stationary. Главный символ шестнадцати tensor equations строго эллиптичен: eigenvalues 4/3 (10) и4/9 (6) для quadratic energy, в точной tensor norm. На плоском четырёхторе доказана локальная единственность T=0 среди ВСЕХ достаточно малых пространственно-переменных critical points данного a4, а не только constant tensors. Это не закрытие full H+J+R или физической Lorentz-ОТО.

## 0. Действительные входы и границы

Потребляются (не объявляются новыми):

- `A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md`: finite-record/variable-grid fixed-positive-time source theorem, including actual matter on controlled joint-critical sequences. Его доказательство не превращается в small-time expansion и не утверждает LC-source pullback.
- `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`, §§3,5,6: actual full16 CAR torsion map, a2 kernel16, right-Clifford B(T), flat a4 и classification constant tensors; actual C0,C2,C4 coefficients всей цены.
- `A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md`: full positive-adjoint matrix domain and scale condition. Original stored inverse-return не заменяется.
- `A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md`: Lorentz reconstruction; g и G не отождествляются.

Здесь G — ПОЛОЖИТЕЛЬНАЯ principal metric, measure=dV_G. У source owner это объявленный natural-measure slice. Если actual measure=w dV_G, его `b=dlog w` и shifted trace equations остаются отдельными; ниже w не выбирается законом физики. Тем более, fixed coordinate counting measure не переименовывается в dV_G. Для closed results manifold закрыт; для local variations можно использовать compact support. Boundary terms иначе сохраняются.

Ни physical Info, ни z(beta), ни desired matter tensor не выбираются. Положительный/эллиптический operator результат не есть Lorentz hyperbolicity.

## 1. Тот же tensor16 — не произвольный Yang–Mills потенциал

В positive orthonormal frame на всех16 exterior components:

    gamma_i=C_i-I_i, hatgamma_i=C_i+I_i,
    Q_T=sum_(a,b<c) T^a_bc C_b C_c I_a,
    Z_T=-(Q_T+Q_T*),
    sum_a T^a_ac=0,
    T^a_bc+T^b_ca+T^c_ab=0.                               (1)

Условия (1) дают rank16 vector bundle V. Полная норма:

    |T|²=sum_(a,b<c)(T^a_bc)².

Именно в этом подпространстве прежний owner доказал

    Z_T=sum_i gamma_i B_i,
    B_i=-{gamma_i,Z_T}/2,
    B_i*=-B_i, [B_i,gamma_j]=0.                            (2)

Каждый B_i лежит в real span {hatgamma_a hatgamma_b:a<b}, не во всём commutant и не в independently selected gauge field. В curved frame B — разность двух right-Clifford connections. Совместное преобразование под frame changes сохранено; dB в дальнейших формулах заменяется ковариантной производной.

Локально разложим Hodge connection на left spin и right spin части. Это алгебра на exterior bundle; глобальная spin-структура для trace-формул не требуется. При curvature convention прежнего owner:

    Omega^L_ij=-(1/4)sum_ab R_ijab gamma_a gamma_b,
    F^0_ij=(1/4)sum_ab R_ijab hatgamma_a hatgamma_b.

Для same D=D_Hodge+Z_T:

    F^R=F^0+mathcal K,
    mathcal K=D^0 B+B wedge B.                            (3)

Лоренцевы исходные connection variables и полное coframe-to-T отображение должны оставаться в области исходного heat theorem; (3) не вводит новое physical action.

## 2. Полный a4 на неплоском G

Обозначаем L4 локальный traced coefficient БЕЗ общего (4pi)^-2, как в исходном owner. Laplace convention: D²=-(nabla²+E). Clifford identities дают

    E=-(R/4)I-sum_(i<j) gamma_i gamma_j F^R_ij,
    Tr16 E=-4R,
    Tr16 E²=R²-(1/2)Tr16 sum_(i,j)(F^R_ij)²,
    Tr16 sum_(i,j)Omega_ij²=-2|Riem|²
                                 +Tr16 sum_(i,j)(F^R_ij)².     (4)

В частности, curvature разных Clifford факторов нельзя смешать либо считать нулевой при B=0. Полная формула a4 стандартного Laplace-type оператора (Vassilevich, hep-th/0306138, (4.28), PDF p.40) и (4) дают

    L4(G,T)= R²/18 -(4/45)|Ric|² -(7/90)|Riem|²
       -(1/6)Tr16 sum_(i,j)(F^R_ij)² -(2/15)laplacian_G R.     (5)

Производные здесь не выкинуты: Tr nabla²E=-4 laplacian R. Trace right-curvature Clifford term тождественно нулевой, поэтому отдельный derivative B term в traced divergence не потерян.

При B=0, Tr16 sum(F^0_ij)²=-2|Riem|². Получаем

    L4_H=(23/90)|Riem|²-(4/45)|Ric|²+R²/18
                                         -(2/15)laplacian R.  (6)

В частности, точная РАЗНОСТЬ — не только positive square новой кривизны:

    A4(G,T)-A4(G,0)
       =-(1/6)int Tr16 sum_(i,j)
                    [2 F^0_ij mathcal K_ij+mathcal K_ij²]dV_G. (7)

Смешанный член принципиален. Приёмка только flat witness ничего о нём не доказывала. У нас (4)–(7) проверены на generic rational algebraic curvature с ненулевой Ricci и Weyl частями и произвольной real right curvature; вычисление использует все16 components. General formula доказана trace identities, не этим конечным fixture.

## 3. Неплоский Einstein-фон совместим с настоящими tensor-строками a4

При fixed G полная tensor variation:

    delta A4=(2/3)int Tr16 sum_j
                    (nabla^{R,i}F^R_ij) delta B_j dV_G,
    delta B=L_G(delta T), delta T in V.                       (8)

Это projected16 source, а не добавленные unrestricted24 equations. Formula сохраняет настоящий connection в covariant derivative. У variable prefactor или boundary появляются соответствующие дополнительные члены.

На T=0 source (8) определяется curvature исходной Hodge right connection. Contracted differential Bianchi identity:

    nabla^i R_ijab=nabla_a Ric_jb-nabla_b Ric_ja

с соответствующим соглашением знака индексов. Поэтому при `Ric(G)=Lambda G`, Lambda constant,

    delta_T A4(G,0)=0                                        (9)

для всех16 разрешённых вариаций. Это не требует flat Riemann: Weyl может быть ненулевым. Обратное неверно: harmonic-curvature metrics шире Einstein metrics. Ни (8), ни (9) самостоятельно не выводят Einstein.

### Метрический a4 не добавляет отдельного тензорного уравнения на этом фоне

В4D на closed manifold (6) эквивалентен

    A4_H=int [(7/15)|Weyl|²-(19/90)Euler4+R²/9]dV_G.          (10)

Euler integral топологичен. Первая вариация Weyl² — Bach tensor; он нулевой на Einstein metric: divergence Weyl=0 и Ricci contraction of Weyl=0. Первая вариация R² также нулевая, поскольку R constant и 2R Ric-(R²/2)G=0 в4D. Следовательно полный geometric pullback

    delta_G A4_H=0                                           (11)

при Einstein G, со всеми10 metric tests, не только масштабной вариацией. Имеются nonflat controls S4 и S2×S2 equal-radius; в последнем случае Weyl не нулевой. Exact integrated density на S2(a)×S2(b), без общего volume constant:

    A4_H=(16/15)(b²/a²+a²/b²)+4/9.

Оба radius sources нулевые при a=b и не нулевые в общем случае. Это finite control (11), не доказательство всех его компонент.

**Что снято:** tensor16 не обязан создавать дополнительный источник на Einstein-фоне просто потому, что его operator directions не были видны в a2. Следующий coefficient действительно совместим с ним, с кривизной и всеми cross terms.

**Что не снято:** A4 может менять global coefficients C0,C2 полного log-normalizer, даже если dA4=0 в этой точке. Источники A0,A2, actual matter, higher heat coefficients и observer/weight все остаются. Доказана совместимость положительного G, а не равенство этого G Lorentz g. Метрика, являющаяся Einstein для g, не обязана быть Einstein для G.

## 4. Главный символ: шестнадцать компонент перестают быть произвольной слепой зоной

На flat G=I и natural measure исходный owner дал

    A4(T)=-(1/6)int Tr16 sum_(i,j)F_ij²
         =(1/3)int sum_(i<j)||F_ij||HS²,
    F_ij=partial_i B_j-partial_j B_i+[B_i,B_j].                (12)

Вектор T всегда ограничен V. Для principal frequency xi и fixed T:

    q_xi(T)=(1/3)sum_(i<j)||xi_i B_j(T)-xi_j B_i(T)||HS².

На всех16 tensor directions имеем точные тождества

    sum_i||B_i(T)||HS²=4|T|²,
    (4/9)|xi|²|T|² <= q_xi(T) <= (4/3)|xi|²|T|².             (13)

При единичном xi generalized eigenvalues в объявленной |T|² norm:

    4/3: multiplicity10; 4/9: multiplicity6.                 (14)

Доказательство: O(4)-equivariance позволяет взять xi=e0. Исходная CAR-карта и nullspace восьми trace/cyclic rows дают явные rational matrices N: R16→V, M=N^T N и Q. Прямо `(M^-1 Q-4I/3)(M^-1 Q-4I/9)=0`, trace=16 и symmetry в M фиксируют (14), hence (13). Script воспроизводит N и все матрицы из24 actual T-coordinates; никакого sampled rank census. Дополнительный rational xi=(3/5,4/5,0,0) проверяет covariance.

### Почему привычная gauge-нулевая мода здесь отсутствует

Если xi wedge B=0, то B_i=xi_i A. Но (1) даёт `Z_T vac=0`, то есть `gamma(xi) A vac=0`. При xi!=0 Clifford gamma(xi) обратима, значит A vac=0. A коммутирует со всеми gamma; sixteen gamma-words на vacuum порождают весь full16 carrier. Значит A=0 и T=0. Это показывает injectivity символа без перебора.

Это НЕ утверждение об отсутствии gauge freedom во всей native theory. Generic pure-gauge right connection не принадлежит данному tensor16 slice; другие coframe/observer/gauge equations не изменяются. Hessian principal symbol (12) вдвое больше (14): 8/3 и8/9. Эллиптичность сохраняется на curved positive G, но lower-order curvature terms могут менять kernel и stability.

## 5. Глобальный нуль и локальная классификация переменных полей на торе

### 5.1. Нулевую curvature нельзя спрятать в непостоянном tensor-field

Для любого smooth periodic tensor T на flat T4 vacuum 1 — глобальный unit section. По (1) `D_T vac=0`. Lichnerowicz identity интегрированно даёт

    0=int sum_i||B_i vac||²
            +int <vac,sum_(i<j)gamma_i gamma_j F_ij vac>.

В real right-bivector representation:

    sum_i||B_i vac||²=|T|²/4,
    ||F_ij||HS²=16||F_ij vac||².

Cauchy–Schwarz на шести парах даёт без малости T:

    A4(T) >= ||T||L2^4 / [18 Vol(T4)].                        (15)

Значит `A4=0` iff T=0 даже для переменного поля. Это существенно сильнее прежнего constant-field доказательства; оно не говорит, что every critical point has zero energy. Boundary terms или меняющийся positive measure требуют отдельной формулы.

### 5.2. В достаточно малой окрестности все critical fields всё же нулевые

Фиксируем flat unit torus. Возьмём Sobolev s>2 и smooth nonlinear Euler map
`E: H^(s+2)(V)→H^s(V)` functional (12). Разложим `T=c+u`, c constant tensor, mean(u)=0. В нуле Hessian L — constant-coefficient strongly elliptic operator из (13). На mean-zero subspace он обратим. На самом низком ненулевом momentum:

    <u,Lu> >= (32pi²/9)||u||L2².                            (16)

Поскольку E(c) пространственно постоянна, её mean-zero проекция равна0 для КАЖДОГО малого c. IFT по u даёт единственное малое решение `u(c)=0` этого projected equation. Остаётся ровно finite constant equation E(c)=0. Прежний owner уже доказал A4(c)>0 для c!=0. Quartic homogeneity `dA4_c[c]=4A4(c)` исключает любое такое constant critical point. Итак,

    существует H^(s+2)-окрестность0, где dA4(T)=0 iff T=0.     (17)

Это локальная классификация всех smooth variable tensor fields, не только одного sinusoidal profile. В ней не обращается geometric Hessian, не выкидываются другие native modes, и не утверждается невозможность distant nonlinear critical points. Неизвестные IFT radius/physical scales не объявлены uniform in h,beta.

В качестве конечного контроля для одного actual tensor basis и f=epsilon cos(qx0) средняя (12) равна `2epsilon² q²/3+epsilon^4/2`. Производная и commutator terms сохраняются, никакой равный нулю a2 не выдаётся за полный stationarity test.

## 6. Подстановка в настоящую цену и следующий потребитель

Параллельный finite-source owner снял fixed-beta grid/record и independent field-source approximation на своей C6 uniformly elliptic domain. Это потребляется как установленный отдельный этап. Он сам сохраняет small-time и LC-pullback ограничения. Настоящие finite covectors нельзя заменить dA4 только на основании сходимости при beta>0.

Там, где доказана соответствующая two-scale source expansion, прежний full-price owner даёт

    dS=C0 dA0+C2 dA2+C4 dA4+dR_m+dRem,
    C4=beta/A0-M Phi1(z/(1-z))/(4pi)^2.

Все коэффициенты, reference multiplicity, global normalizer и real matter взяты от него. C4 не выбран ради ellipticity, не предполагается ненулевым/положительным без проверки актуального clock-law. При variable calibration нужно возвращать её derivatives. Обозначение R_m здесь — исходный Rayleigh price, не скалярная кривизна.

Полученные (5),(8),(13) заполняют именно отсутствующий curved/tensor вход A4. На Einstein G, T=0, fixed natural measure геометрический dA4 pullback и tensor16 source vanish; но dA0,dA2 и coefficient dependence остаются. Например, если independently retained matter source отсутствует, reduced metric row в этой coefficient expansion требует `8C0-(4/3)Lambda C2=0`, а не позволяет произвольно выбрать Lambda или забыть A4-зависимость C0,C2. Другие восемь torsion directions и higher coefficients должны читаться из полного price, не объявляются решёнными (9).

Главный практический эффект: 16 оставшихся направлений теперь имеют собственный elliptic operator и определённую кривую source, а не статус «невидимой материи». На flat slice их small-field coefficient-level elimination обоснована (17); на Einstein curved slice их нулевой источник обоснован (9). Для полной теории остаются actual matter response, higher/fixed-time source, Lorentz/observer/measure identification, primitive admission и точные nonflat native stationary sequences. Ничего из этого не определяется разностью до желаемого Einstein tensor.

Предлагаемый immediate consumer — один основной #334 integrator и matrix-free source implementer: использовать (8) с полным F^0 и ограниченным tensor-map; реализовать elliptic principal block (14) и actual curvature lower-order terms. Не запускать новый каталог форм кручения и не повторять flat witness как новый результат.

## 7. Воспроизводимость

`check_curved_tensor.py`: полный16 CAR порядок (0,2,3,1) из закреплённого primary creator. Он непосредственно строит 24 T coordinates, восемь constraints, N и B; воспроизводит 427 exact conditions, большинство — commutant/constraint identities, не427 физических теорем. Generic curved a4/cross terms, all-grade sphere и unequal sphere-product controls, principal matrix polynomial и внеосевая проверка включены. O(4), Bianchi, elliptic IFT и global integral proofs изложены выше; finite fixtures их не заменяют.

Обычный и оптимизированный запуски дали одинаковый JSON. Четыре действительно изменённые программы отвергнуты: удалённая trace-constraint, половинный principal coefficient, потерянная исходная Hodge-кривизна, неверный вес полного connection-curvature trace. Старые suites и Lean не запускались. Нет независимой приёмки или physical/claim promotion.

Математический внешний вход: D.V. Vassilevich, *Heat kernel expansion: user's manual*, hep-th/0306138v3, formula(4.28). Использована общая формула a4, не её вывод как закона D0. Тождество contracted Bianchi и свойства quadratic curvature actions — стандартные geometric ingredients; новые для данного source-chain результаты — явный full16 curved coefficient, точный tensor symbol и его переменно-полевой consumer.
