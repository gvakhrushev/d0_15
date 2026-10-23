# D0 → ОТО: конечный относительный clock-cocycle полной истории и типизированная граница Einstein source

17 октября 2026. RESEARCH / ANALYTIC RESULT / NOT PHYSICAL LAW. Consumer: existing Draft #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. Публикация нового независимого аналитического потребителя, без замены native H+J+R, без новой Cost−Info аксиомы, без очереди и claims.

## 0. Фактические входы и цель

Вход: A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md, A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md, A4D_POINTER_HISTORY_FINITE_PART_SOURCE.md, A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md, A4D_LOCAL_GAIN_PROJECTIVITY_RIGIDITY.md и source d0_native_entropy_action_obstruction_2026-10-17/RESULT_RU.md на текущем научном носителе #334. Геометрическая граница: A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md, A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md. Сопоставлены слитые #352, #354, #355, #358.

Задача обратного хода Einstein → D0: найти существующий, а не подогнанный, математический объект, у которого исчезает clock-log, и указать точный недостающий morphism от него к полному native action. Выход ниже — точный chain identity полной маркированной истории и ограниченный continuum test; это НЕ выбор физического action, НЕ отождествление с v8, НЕ stationary joint root и НЕ замыкание исходной all-ten raw h^-2/#216 задачи.

## 1. Теорема о полном native-алфавите: clock-log сокращается в отношении правдоподобий

Оставим native full128 instrument: один blank K_0=B_h=I−eps Delta_h/2 и все 127 nonblank K_alpha=sqrt(eps) ell_alpha, включая label0/port1, 16 exterior grades, 128 reference и retained prefixes. eps=p²h²/64; n=n_h и T_h=n eps. При фиксированной общей clock-programme сравним ДВА имеющихся допустимых семейства полей/подготовок x,y. Для каждого одного и того же буквального префикса omega и z∈{x,y} определим действительное условное состояние rho^z_(j|omega) и

    a^z_alpha(omega)=Tr(rho^z_(j|omega) ell^z_alpha* ell^z_alpha), alpha=1..127,
    r^z(omega)=sum_alpha a^z_alpha(omega),
    p^z_0(omega)=1−eps r^z(omega),
    p^z_alpha(omega)=eps a^z_alpha(omega).

Здесь источник rho включает собственную реальную preparation/field/observer/measure производную и полную историю; состояния после одного и того же omega для x и y могут отличаться. Не заменять их одной frozen rho. Положительная полнота Kraus обеспечивает sum p^z=1.

Пусть Q^x_h,Q^y_h — ПОЛНЫЕ распределения на 128^{n_h} буквальных историй и Q^x_h≪Q^y_h (иначе относительная энтропия равна +∞). Тогда **для каждого конечного h и произвольной памяти**, без iid и без спектрального предела, цепное правило даёт точно

$$
D(Q_h^x\Vert Q_h^y)=
\sum_{j=0}^{n_h-1}\mathbf E_{Q_h^x}
\left[
(1-\varepsilon r^x)\log\frac{1-\varepsilon r^x}{1-\varepsilon r^y}
+\varepsilon\sum_{\alpha=1}^{127}a_\alpha^x\log\frac{a_\alpha^x}{a_\alpha^y}
\right].\tag{R1}
$$

Все интенсивности в скобке оцениваются на одном фактически сохранённом prefix omega. Нули обрабатываются соглашением 0 log(0/b)=0, a>0,b=0→+∞; при полном нуле обоих вклад0. **В (R1) уже на конечном h нет отдельного log eps:** вся общая степень eps сократилась попарно в логарифме mark-вероятностей. Это не subtraction и не смена исходного прибора.

Доказательство. Конечное цепное правило KL есть разложение log(Q^x(omega)/Q^y(omega)) в сумму логарифмов условных вероятностей 128 возможных меток. Затем умножить на Q^x, усреднить по каждому true-prefix и подставить p^z_alpha=eps a^z_alpha. Последнее отношение равно a^x_alpha/a^y_alpha. Никаких discarded ports или reduced reference в этом выводе нет. Когерентные группировки histories с интерференцией НЕ являются исходным буквальным cut и этим доказательством не охвачены.

## 2. Континуумная форма и настоящий первый источник: условия оговорены

Для сравнения на **равной** сетке T_h=n_h eps→T при условной локальной ограниченности 0≤r^z≤R, eps R<1 и интегрируемости a^x log(a^x/a^y), элементарный Taylor blank-части даёт равномерно по prefix

$$
(1-\varepsilon r^x)\log\frac{1-\varepsilon r^x}{1-\varepsilon r^y}
=\varepsilon(r^y-r^x)+O_R(\varepsilon^2).
$$

Поэтому из (R1) строго следует finite-h оценка

$$
D(Q_h^x\Vert Q_h^y)
=\sum_{j=0}^{n_h-1}\varepsilon\mathbf E_{Q_h^x}
\sum_{\alpha=1}^{127}
\left[a_\alpha^x\log\frac{a_\alpha^x}{a_\alpha^y}
-a_\alpha^x+a_\alpha^y\right]
+O_R(T_h\varepsilon).\tag{R2}
$$

Rate functional неотрицателен как сумма скалярных a log(a/b)−a+b. Если дополнительно actual conditional-rate path densities и ожидания сходятся в соответствующем L1 с uniformly integrable logarithmic terms, R2 переходит в

$$
D_T(x\Vert y)=\int_0^T\mathbf E_x
\sum_{\alpha=1}^{127}
\left[a_\alpha^x\log(a_\alpha^x/a_\alpha^y)-a_\alpha^x+a_\alpha^y\right]dt.\tag{R3}
$$

Важная граница: uniform bounded r **сама по себе** не обеспечивает finite KL, uniform L1 на редких нулевых строках или first-source limit. В реальном D0 есть zero-leading words и born ranks; им нужны собственные positivity/support и logarithmic-tail estimates. (R3) — условное следствие, не объявленный native C1 certificate.

**Exact source до любого предела.** Для совместной гладкой деформации x(t),y(t) на общей положительной поддержке:

$$
\frac d{dt}D(Q_h^{x(t)}\Vert Q_h^{y(t)})
=\sum_\omega \dot q_x(\omega)\log\frac{q_x(\omega)}{q_y(\omega)}
-\sum_\omega q_x(\omega)\frac{\dot q_y(\omega)}{q_y(\omega)}.\tag{R4}
$$

Сумма dot q_x равна0. Это содержит ВСЕ реальные source jets обеих подготовок, Kraus, links и прошлых условных состояний; невозможно оставить лишь производную local rate, заморозив закон ожидания Q^x. Если y фиксирован, второй член0. Для обмена производной и continuum limit требуются actual Fisher/log-tail assumptions, а не одна сходимость значений R3.

**Exact Fisher-диагностика.** Возьмём x(t), y=x(0) с общей устойчивой положительной поддержкой. Пусть точка t=0 и точные conditional total jets dot a_alpha(omega), dot r(omega)=sum dot a_alpha включают настоящую фильтрацию состояния после каждого prefix. На конечном h:

$$
\left.\frac{d^2}{dt^2}D(Q_h^{x(t)}\Vert Q_h^{x(0)})\right|_{t=0}
=\sum_{j=0}^{n_h-1}\mathbf E_{Q_h^{x(0)}}
\left[
\varepsilon\sum_{\alpha=1}^{127}\frac{\dot a_\alpha^2}{a_\alpha}
+\frac{\varepsilon^2\dot r^2}{1-\varepsilon r}
\right].\tag{R5}
$$

Доказательство: score full history есть сумма mean-zero conditional score increments; ортогональность мартингальных разностей убивает cross terms. Mark и blank Fisher-термы вычисляются отдельно. При исчезающих labels нужна отдельная пограничная формула, деление на a=0 не разрешено. (R5) положительно полуопределён и не равен автоматически Hessian Einstein–Hilbert (последний на unrestricted metric directions не является Fisher-формой).

## 3. Decisive actual radial native consumer: конечная comparison price, расходящаяся absolute price

Сохраняем homogeneous coframe trajectory из источника d0_native_entropy_action_obstruction_2026-10-17/RESULT_RU.md: G(t)=(1+t)G_*, P_Omega/128 с полным reference128, fixed eps_L=p²/(64L²), n=128L², beta=n eps=2p², gamma_L=4L² sin²(pi/L), d>0 прежнего certified rectangle. На всех восьми momentum shell16 grades точный общий exit-bit marginal full128 event:

$$
q_L(t)=\varepsilon_L(1+t)\gamma_L d
\left[1-\varepsilon_L(1+t)\gamma_L d/4\right].
$$

Это результат суммирования 127 настоящих marks, не утверждение о равенстве entropy coarse и full.

Для полной native истории уже доказано

$$
\frac{dH(Q_{L,t})/dt|_{0}}{\log(1/\varepsilon_L)}
\longrightarrow\beta\,4\pi^2d>0.
$$

Но ДВА native exact exit-bit marginal processes на одной сетке имеют самостоятельную finite divergence

$$
D_{\rm bit,L}(t\Vert0)=n_L D_{\rm Bern}(q_L(t)\Vert q_L(0))
\longrightarrow
\beta\,4\pi^2d\,[(1+t)\log(1+t)-t].\tag{R6}
$$

Точно

$$
\left.\partial_t D_{\rm bit,L}(t\Vert0)\right|_0=0,\quad
\left.\partial_t^2 D_{\rm bit,L}(t\Vert0)\right|_0
=\frac{n_L[q_L'(0)]^2}{q_L(0)(1-q_L(0))}
\longrightarrow\beta\,4\pi^2d.\tag{R7}
$$

При положительном источнике это не исчезающая тривиализация: наблюдаемый quadratic response конечен и ненулевой. Numeric midpoint d≈0.063635191594344535 даёт coefficient≈1.919162760216 и для t=0.1 limit D_bit≈0.009291046503. Это coarse lower bound для FULL native D(Q^t||Q^0) по data processing, а НЕ утверждение, что полный KL уже имеет тот же limit: межметочная структура и zero-leading support может дать дополнительные источники.

Negative control: сравнение q_L с q_ref≈eps_L² lambda (несогласованные часы) вновь даёт коэффициент beta 4pi²d log(1/eps_L). Одинаковый native clock/labels — содержательная структурная предпосылка, не косметика.

## 4. Condensed mathematics: допустимая оболочка, не физический селектор

Clausen–Scholze, Lectures on Condensed Mathematics (2026 stable arXiv 2605.03658) развивают sheaf formalism на profinite/extremally disconnected test spaces, а solid modules используются для линейно-топологических задач. Для фиксированного tick law finite-prefix spaces Omega_n={0,...,127}^n и забывающие projections образуют inverse system с compact profinite limit Omega. Consistent full-cut q_n дают cylinder measure на Omega; relative likelihoods L_n=dQ^x_n/dQ^y_n образуют Q^y-мартингал:

$$
\mathbf E_{Q^y}[L_{n+1}\mid \mathcal F_n]=L_n.\tag{R8}
$$

Это непосредственный consequence of projectivity, а не следствие выбора «condensed» языка. Возможна sheaf/condensed упаковка натурализованных endpoint/comparison data и finite source families по всем profinite probes, если построен конкретный functor и proven descent. НО смена eps или числа временных ячеек НЕ является автоматически тем же inverse limit, и sheafification не выбирает физические Book weights, nontrivial N, Lorentz connection или stress.

Таким образом condensed mathematics полезна для корректной склейки носителей, но на данном конечном шаге (R1)–(R8) стандартная вероятность сильнее и достаточна. Не заменять доказательство физического map названием нового аппарата.

## 5. Следующий Einstein-квадрат должен быть типизирован: что уже известно и чего нет

Цель первого порядка должна различать источник тетрады tau_a (3-form), спиновый источник sigma_ab (3-form) и coframe e^a (1-form). Типизированное материальное вариационное тождество:

$$
\delta S_m=\int(\delta e^a\wedge\tau_a+\delta\omega^{ab}\wedge\sigma_{ab})+\text{matter Euler}+\text{boundary}.\tag{R9}
$$

Фраза «tau_a=T_ab e^b» из присланного обратного синтеза даёт 1-form, НЕ 3-form. При локальном симметричном metric stress правильный Hodge-тип: tau_a=T_a{}^b\,\star e_b (с convention factors). В Einstein–Cartan соединение torsion-free только при нулевом spin source и невырожденном coframe; общий spinful matter требует Cartan torsion equation с sigma_ab. Нельзя заявить torsion-free из dim ker H=2. Bianchi/Ward — четыре локальных diffeo identities (с другими retained Euler terms), тогда как ker dimension2 отдельного конечного H(z=1) НЕ является их доказательством.

Слитый #354 установил ker D rho dimension30784=1984 правых unitary +28800 rank-birth directions, не 30784 независимых metric variations. #352 сохраняет настоящий saddle с zero lower block; его нельзя заменить положительным тепловым гессианом. Слитый #358 дал induced coframe на одном non-vacuum pp-wave и Ricci cross-check, но не native stress. T_k(X_V)=0 (из A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md) означает, что занятой compression X_V scalar, а occupied-empty offdiagonal0. Число eps'(V)=Tr(Pi X_V)/k — линейный covector на REAL admitted field velocities; без построенного native S_m и локального coframe pullback он НЕ превращается автоматически в tau_a. У pp-wave scalar R=0 при Ricci≠0, поэтому совпадение scalar actions на one-profile family не заменяет all-ten Euler test.

Обратный требуемый квадрат (все стрелки на одном common carrier):

    (native complete action / actual branch Info / admitted cut)
        → exact normalized-field variation with real retained equations
        → independently derived (tau_a, sigma_ab) with Lorentz/metric Ward
        → full Palatini/EH covector including torsion and Lambda
        → nonempty exact joint root family + quantitative raw h^-2/#216 refinement.

(R1)–(R8) строят конечный, позитивный candidate comparative observable. Они **не доказывают первую физическую стрелку**. Fisher-positive KL не может по одному переименованию стать signed native H+J+R; это должно быть проверено на true source, а не выбрано ради ОТО.

## 6. Единственный ближайший решающий эксперимент/теорема

Не добавлять raw normalizer по требуемому коэффициенту. На SAME admitted family native instrument построить (i) фактическую comparison reference из уже принятого Book/scene/M1, если она существует, (ii) exact field-level source и реальные all128 support/zero-word controls, (iii) сравнить с native H+J+R *одного и того же* clock, preparation, memory and source. Если тождество не следует — зафиксировать новый finite comparative observable как separate reading, не переписав физический action. Параллельно для подлинного h²-log section нужен полный коэффициент m2+beta_birth и его источник; selected six labels дают только r2, а matched-time strips не объявляются births.

На ветви stationary memory с rank8 вычислять настоящий оператор M_v из (24) memory owner и тест (26)/(28), не обращая zero saddle block. Лишь kernel velocity, выдержавшая matter memory source, физическую admission, full source and second-jet compatibility, идёт к нелинейному корню.

**Outcome этой работы:** exact full128 relative-likelihood chain rule, matched-clock cancellation, finite native radial bit limit/Fisher, explicit source type rules и строгая карта GR consumer. **Status:** NEW RESEARCH / NO GR CLAIM / no main acceptance.