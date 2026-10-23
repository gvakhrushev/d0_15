# Конечный причинный источник на масштабе h²: точный расчёт и проверка Einstein-ядра

16 октября 2026. Продолжение существующего #334, `gvakhrushev/d0_15`.
Исходный SOURCE: `a4f4d4e86ae63336841337e1a93cd5296eb43792`.

**Получено.** Для одного явно заданного периодического longitudinal cone germ вычислена ПОЛНАЯ вторая вариация прежней конечной H+J цены, включая истинные proper links, все16 CAR-компонент, finite record, восприимчивость и глобальный normalizer. Доказан её предел после усиления h^-2; этот предел строго положителен при исходных фиксированных v8-параметрах. Между тем весь линейный Einstein-ковектор данного metric germ равен нулю. Следовательно, соответствующий finite h² coefficient не является чистым Einstein–Hilbert source с собственной R-материей, даже когда положительный continuum оператор не меняется.

**Область вывода.** Это теорема о втором направленном source-jet на flat background в объявленной canonical-adjoint matrix-программе. Не доказаны ни общий C1 remainder o(h²) для всех переменных полей, ни отсутствие исходных fixed-g/fixed-tau exact roots, ни невозможность D0/ОТО с отдельно выведенной полной стоимостью истории. Начальная геометрия этого контроля не объявляется joint stationary root. Новый action, gauge-fixing, stress-компенсатор, масштабный закон или physical claim не вводится.

## 0. Что используется вместо очередного повторения старого результата

`A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md`, §§2–7, уже доказывает:
полная continuum canonical цена факторизуется через G, coordinate torsion, measure и ту же form-matter; LC cone directions не видны этой функции при фиксированных выходных данных. В §7 сохранена возможность finite h² causal source, её full susceptibility formula и собственный clock. Этот конкретный, ранее не вычисленный коэффициент здесь и проверяется.

`A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md` даёт fixed-positive-time full-source limit, но не разрешает удалить h² после h^-2 amplification. Новый специальный расчёт использует точные Fourier blocks и самостоятельно контролирует их предел; он не объявляется общей extension той теоремы.

Прежние flat-moduli, curved-tensor-a4, memory и observer результаты остаются на своих носителях. Особенно: отличие R_G от R_g не устраняется ни новым названием следа, ни положительностью a4. Метод ниже проверяет одну необходимую линейную тождественность Einstein-источника, а не каталог разных гравитационных теорий.

## 1. Одна действительная гладкая семья и тот же конечный прибор

Координатный тор единичного периода, h=1/L, L чётное, L>=4. Положим Q=2π, u=(0,1,1,0), φ=cos Q(x1+x2), v=(1,1,0). При амплитуде ε зададим единичный Euclidean covector

    a_ε=(cos(√2 εφ), sin(√2 εφ)/√2, sin(√2 εφ)/√2, 0),
    G=s² I4,  g_ε=s²(2 a_ε a_ε^T-I4),  s=2.                  (1)

Coframe e=s O_ε берётся настоящим вращением в плоскости e0,(e1+e2)/√2; raw observer n=e0. Поэтому (1) точно имеет Lorentz signature, det(g)=-s^8, G=e^T h(n)e=s²I. В link-slot используется настоящая LC(g_ε), а не I+hΩ вместо proper transport. Все endpoint dependence и все16 exterior grades сохраняются.

В coordinate-form представлении исходный raising operator равен

    d_h=(s h)^-1 sum_r C_r(P_r(ε,h) S_r-I),
    D_h=d_h+d_h*,   Δ_h=D_h².                                (2)

P_r есть полный backward covector parallel transport LC, поднятый на exterior algebra. Звёздочка — fixed-G Hilbert adjoint, с перенесёнными коэффициентами. При ε=0 P_r=I, и на momentum k

    D0(k)=(s h)^-1 sum_r[C_r(exp(2πihk_r)-1)+adjoint],
    λ_h(k)=4(s h)^-2 sum_r sin²(πh k_r),  Δ0(k)=λ_h(k)I16.    (3)

C_r — actual exterior creators. Использован обычный порядок 0,1,2,3; переход от role order (0,2,3,1) есть тот же фиксированный diagonal-sign isometry на всех16 states. Следы, norms и источники от порядка не меняются.

Прежние параметры НЕ подбираются:

    p=(√5-1)/2, α=p² h²/128, m=256 L², β=mα=2p²,
    z=2^-20, M=128, K_h=(I-αΔ_h)^m,
    S_h=R_h+β^-1 log(C_h Tr K_h)-M Tr log(1-z+zK_h).           (4)

C_h=128·128^(m/2) — прежняя field-independent workspace/reference multiplicity. Она не удаляет ни одно состояние; её ε-производные равны нулю. Достаточно малого фиксированного |ε|, чтобы все onsite matrix contractions находились в строгой Julia-domain. При s=2 это следует из ||C_r/s||=1/2, P_r=I+O(h), ||D_h||<=8.4/h, откуда αΔ_h<=0.211<1, например при ||P_r||<=1.1. Невырожденный ε-domain получается из bounded LC coefficients. Физическая генерация этой программы engine остаётся отдельной гипотезой.

## 2. Правильный Einstein-тест не равен одному значению скалярной кривизны

В ε=0

    dot g_01=dot g_02=2s² φ, остальные dot g=0.

Это чистая infinitesimal coordinate variation плоской метрики:
`dot g=L_ξ(s²η)`, ξ^0=2 sin Q(x1+x2)/Q, ξ^i=0. Поэтому линейный Einstein-ковектор vanishes во ВСЕХ10 строках, не только в выбранной contraction.

Независимая прямая проверка: для общего h_0i=2v_i cos(q.x), на flat metric

    δG_0i=q_i(q_sp·v)-|q_sp|² v_i,
    I_EH''=2s²[(q_sp·v)²-|q_sp|²|v|²].                    (5)

Остальные строки также нулевые при q0=0 и v parallel q_sp. У нашей u все условия выполнены, так что I_EH''=0. Volume постоянен ТОЧНО по (1); любой фиксированный Λ-volume также даёт0. Полная конечная ε-семья не объявляется flat coordinate orbit: для второго EH-jet хватает flat stationarity и pure-gauge первой скорости.

Собственная материя R_h сохраняется. Для самого чистого численного контроля можно взять constant scalar vacuum: D_h 1=0 точно, следовательно R_h=0. Это не P1 timelike chart. Для P1-compatible сравнения берётся fixed native first-grade e0 (или owned balanced E0 vector) tensor любой фиксированный нормированный reference vector; её P1-line задаёт ровно n=e0, C_form меняется вместе с e. Её R_h НЕ заморожен. При проверке identity `S_h=c EH+ΛV+R_actual+remainder` тот же R_actual сокращается по обеим сторонам алгебраически. Это не новая subtraction в физическом действии. Всё reference пространство и остальные grades остаются на носителе.

## 3. Proper-link first jets: один CAR-моном вместо скалярного oracle

Обозначим Γ(A)=sum_ab A_ab C_a I_b. Принимаем convention P_r S_r=exp(h∇_r), ∇_r=∂_r-Γ_coord,r^T. По точной LC-формуле первого metric jet для (1):

    dot M0=dot M3=0,
    dot M1=dot M2=-2 φ_y Γ((e1+e2)e0^T), y=x1+x2.           (6)

В (6) φ_y=-Q sin(Qy). Обозначим B=C1 C2 I0. У B²=0, ||B||HS²=2; никакая из16 компонент не удалена. Proper path integral, не endpoint approximation, даёт для перехода k→l=k+u:

    a_h(k)=-(exp(iQh)-1)(exp(iξ1h)-exp(iξ2h))/(s h),
    E_h(k):=dot D_(l,k)=a_h B-conj(a_h) B^T,
    ||E_h(k)||HS²=4|a_h(k)|².                               (7)

Здесь ξ_r=2π k_r. Обратный momentum block есть adjoint E_h. Σ C_r dot M_r=0, что реализует прежнюю continuum cone blindness; E_h=O(h), а не нулевой конечный оператор.

Вторая LC connection variation имеет coefficients proportional φ φ_y, с нулевой spatial mean. У first-connection matrix в (6) square0; все second ordered products на одном edge также0. Поэтому diagonal momentum block ddot D_(k,k)=0 ТОЧНО. Off-diagonal ±2u blocks не удалены из оператора, но не входят в этот first spectral trace at the flat base. Следовательно diagonal ddot Δ возникает только из 2 dot D². Замена proper links линейной аппроксимацией не использована.

## 4. Полная конечная цена и восприимчивость

Пусть `b(λ)=1-αλ`, `P=b^(m-1)`, `K=b^m`, `F=1-z+zK`,
`Z_h=16 sum_k K(λ_h(k))`. Действительный полный spectral gradient:

    κ_h(λ)=-P/Z_h+Mzβ P/F.                                  (8)

Тогда, с Σ по ВСЕМ L^4 momentum,

    (H_h+J_h)''(0)
     =2Σ_k [κ_h(λk)+κ_h(λl)] ||E_h(k)||HS²
      +2Σ_k κ_h^[1](λk,λl)
                  ||D0(l)E_h(k)+E_h(k)D0(k)||HS².            (9)

При coincident eigenvalues берётся κ_h'. Global normalizer derivative в общем Hessian — `-β(Tr P dotΔ)^2/Z_h²`; здесь он равен0 потому, что u≠0 и dotΔ имеет только off-diagonal momentum blocks. Z_h при этом полный и меняющийся с background; нормализация не заморожена. Второе слагаемое (9) обычно НЕ нулевое. Именно его пропуск делает неправильным следующий h² coefficient.

(9) выведено из точного finite-dimensional spectral calculus и actual power derivatives. Внешние multiplicities сохранены в (8); внутри матричных норм учтены все16 CAR-states. Matter jets присутствуют в R_h отдельно и отменяются только в названном сравнении одного и того же R.

## 5. Предел на правильном h^-2 масштабе доказан для этого полного второго джета

При фиксированном k положим l=k+u, λk=|ξ|²/s², E_k=exp(-βλk),
Z=16Σ_(Z4)E_k, F_k=1-z+zE_k и κ(λ)=-exp(-βλ)/Z+Mzβ exp(-βλ)/F.
Полные16 CAR identities дают

    e_k²:=lim ||E_h(k)/h||HS²=4Q²(ξ1-ξ2)²/s²,
    U_k=ξ0²+ξ1²+ξ2²+Q(ξ1+ξ2)+Q²,
    n_k²:=lim ||dotΔ_(l,k)/h||HS²=(2U_k/s²)e_k².              (10)

Поэтому

    L:=lim_(h→0) h^-2(H_h+J_h)''(0)
      =2Σ_(k in Z4) e_k²[κ(λk)+κ(λl)+(2U_k/s²)κ^[1](λk,λl)]. (11)

Нормы в (10) вычислены аналитически, не fitted из L=8,16.

**Обоснование перестановки предела.** На centered Brillouin cube λ_h(k)>=16|k|²/s². ||D0(k)||<=2π|k|/s и (7) даёт uniform `||E_h(k)/h||<=C(1+|k|)`. Следовательно normalized dotΔ norm bounded C(1+|k|)². На B>=b0, m>=2 функции |κ_h| и |κ_h'| bounded константой times exp(-βλ/2); Z_h>=16. Для divided difference применяем интеграл derivative между λk и λl. Поскольку wrap-around сдвиг меняет |k| не более √2, все члены (9)/h² ограничены одной summable функцией

    C(1+|k|)^4 exp[-c(|k|-√2)_+²].                           (12)

Это сохраняет весь carrier и все high modes. Dominated convergence даёт (11) и convergence самого Z_h. Finite clock поправка κ_h-κ=O(α) на каждом spectral block, её вклад в (11) исчезает, поскольку (9) уже O(h²); это не разрешает удалять clock из других metric rows.

Доказана именно convergence второго ε-джета at ε=0. Общая uniform C1 или C2 expansion в finite ε здесь не заявляется. Исходный theorem о fixed nonconstant g и first-source h^-2 comparator этим не опровергается автоматически. Но любой proposed C2 h² action/source coefficient, согласованный на данной семье, обязан иметь (11).

## 6. Строгий знак всего бесконечного ряда, не доверие float-положительности

Положим x=βQ²/s². Достаточные условия ниже: x>=2 и

    μ=Mzβ Z/(1-z)<1/4.                                      (13)

Для e_k≠0 имеем integer d=k1-k2≠0, v=k1+k2+1 и
u=k0²+k1²+k2²+k1+k2+1=(v²+d²+1)/2+k0².
Отсюда u>=1 и u>=3|v|/2 при v≠0, поскольку
`(|v|-1)(|v|-2)>=0` для неотрицательного целого |v|.

Если b=2U_k/s² и Δλ=λl-λk, то

    b(E_k-E_l)/[Δλ(E_k+E_l)]
       =xu tanh(xv)/(xv) >=4/3.                            (14)

Для v=0 это xu>=2; для v≠0 используем u/|v|>=3/2 и tanh(2)>8/9. Ни degeneracy, ни opposite Dirac eigenvalues не исключены.

Heat-часть квадратной скобки (11) есть `[b Ediv-(E_k+E_l)]/Z`.
Feedback может иметь противоположный знак, но точное difference identity
`(E_k/F_k-E_l/F_l)=(1-z)(E_k-E_l)/(F_k F_l)` даёт нижнюю границу

    bracket >= (E_k+E_l)/Z * [(1-μ)*4/3-1]
             = (1-4μ)(E_k+E_l)/(3Z)>0.                     (15)

Хотя отдельные floating values на огромных k могут стать signed underflow,
знак общего exact series следует из (15), а не из численного вывода.

Для исходных p,β,s,z,M условие x>=2 очевидно из β>3/4 и π>3.
Кроме того,

    Z=16(Σ_(n in Z)exp(-x n²))^4
     <=16[1+2 exp(-2)/(1-exp(-6))]^4 <50.

Последнее можно проверить только рационалами из exp(2)>7 и exp(6)>343.
Значит μ<6400/(2^20-1)<1/4. Уже k=(0,-1,0,0) имеет e_k>0.
Таким образом **L>0 строго**. Численно, не как интервальный сертификат
всех десятичных знаков,

    Z=16.0681474139169...,
    L=2.91075271055528....                                  (16)

Это вторая ε-производная. Если цену пишут `S(ε)=S(0)+ε² c+...`, её
коэффициент равен L/2 после h^-2. Факториал не следует менять между владельцами.

## 7. Что именно исключено и какие дополнительные поля не исключены

Для данного actual proper-link canonical programme на этой семье

    lim h^-2 d²_ε[H_h+J_h]|0=L>0,
    d²_ε EH[g_ε]|0=0,  d²_ε V[g_ε]|0=0.                    (17)

Никакая scalar constant c не превращает левый coefficient в Einstein
Hessian. Это также не устраняется добавлением того же actual R по обеим
сторонам либо одной общей ненулевой перенормировкой цены. Для данного
необходимого metric test нельзя назвать любой ненулевой h² causal signal
доказательством Einstein-source. Longitudinal pure-gauge kernel обязателен.

Но (17) НЕ говорит, что весь совместный field/preparation germ — gauge:
observer, lattice address and reference records могут содержать физически
различимые данные. Тогда его реальный source принадлежит дополнительному
clock/observer/retained сектору. Его цена и coupling должны быть выведены
из того же native процесса, не объявлены равными разности до нужного G.
Он не обязательно совпадает с уже имеющимся Rayleigh R.

Не исключаются другой доказанный physical programme, coupled reference law,
существенно иной joint scale limit, общий stress, exact-root-only comparator
или состояния вне объявленной области. Не доказано, что данный R-вакуум
kinematically/generatively выбран D0-core. Это проверка текущего обещанного
scalar-price/Einstein identification, а не no-go всей проверяемой теории.

## 8. Положительная информация: найден реальный источник и критерий его отбора

Раньше было неизвестно, сохраняет ли proper finite stencil хоть какую-то
Lorentz-cone информацию после continuum factorization. Ответ теперь да:
его actual h²-price/source знает изменение cone, и (9) задаёт конечный
вычисляемый оператор с сохранённой восприимчивостью. Этот ответ не выбран
под desired EH и не получен из дополнительно добавленного boost observable.

Однако он одновременно различает указанное longitudinal направление, где
чистая геометрическая Einstein-часть молчит. Поэтому главный consumer
должен разделить **собственную цену сохранённого эксперимента** и
универсальную metric source: нельзя продолжать поиск только ещё более
точных коэффициентов той же scalar-price с обещанием, что из них сам собой
возникнет чистый EH. Это один конкретный necessary test, а не каталог Q.

Прежние canonical coframe→LC→Einstein reconstruction и P1 SAME-matter map
остаются правильными в своих областях; (17) не подменяет их ложной
идентификацией операторной цены. Фундаментальный missing input теперь
должен уточнить full experiment/action binding, а не очередную настройку
коэффициента кривизны. Для запроса «закрыть всё сразу» это реальная граница
полученного вывода; объявления полного GR closure нет.

## 9. Воспроизводимость и независимые контроли

`check_exact.py` выводит CAR/LC identities, формулы (10), all-slot linear
Einstein zero, spectral second-derivative formulas и рациональные границы
(13)–(15). `finite_symbol.py` независимо суммирует полные finite Fourier
second jets, строя actual full16 products. Для L=4,8,16 используются ВСЕ
L^4 momentum. Большие L в иллюстративной таблице используют указанный
cutoff; (12), а не эта таблица, доказывает предел.

`dense_check.py` независимо строит LC из метрики, интегрирует proper
parallel transports, поднимает их exterior minors и диагонализует все
полные16L блоки двух малых решёток. Это floating verification, не proof
через finite differences. Другие зависимости: Python, SymPy, NumPy, SciPy.
Ни один old root/Lean/research suite не запускается.

Основной доказательный input — сам pinned D0 causal owner и изложенные
выше прямые вычисления. Стандартный внешний контекст linearized Einstein
and diffeomorphism kernel: S.M. Carroll, *Lecture Notes on General Relativity*,
arXiv:gr-qc/9712019. Его equations не заменяют native dynamic premises.
