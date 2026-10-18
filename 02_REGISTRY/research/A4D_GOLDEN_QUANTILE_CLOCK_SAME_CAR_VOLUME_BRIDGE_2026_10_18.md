# D0 → ОТО: полный золотой адрес, source-compatible CAR-метрика и единственный треугольный inverse-clock transport

18 октября 2026. Потребитель уже открытого Draft #334, task EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. **Статус:** EXACT GEOMETRIC ADDRESS TRANSPORT / FULL FIRST SOURCE OF MOVING CELLS / PHYSICAL BOOK AND ACTUATION BINDING OPEN. Не добавлены новое действие, закон matter, подгонка объёмной цены, новое измерение, CORE/Book claim или внешняя константа.

**Именно уже принадлежащие входы:** [actual golden cost/refinement](A4D_NATIVE_GOLDEN_COST_REFINEMENT.md), [history-to-density](A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md) §1, [density-dressed full16 source-compatible metric](A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md) (1)–(10), [full nonlinear radial coframe action](A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md), [actual full-source §6.40](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md) and the [full experiment sampling Ward](A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md). Работа устраняет НЕ произвольный «ещё один метрический коэффициент», а оставленный самим integrator один сквозной interface: старый retained F/R address → двигающийся proper-clock sampling → настоящий density/observer/source jet.

## 1. Формулировка обратной теоремы без Einstein в предпосылках

Исходные слова w∈{F,R}*, стоимость c(w) с приращениями1,2 и полная golden reference measure μ(w)=p^{c(w)}, p=φ^-1, p+p²=1, уже задают вложенные Role-ordered boxes B_w⊂[0,1]^4 с |B_w|=μ(w). На настоящем cost-cut они образуют конечное полное разбиение; pending branches НЕ разрезаются вторично и не стираются. Оси выбираются предыдущим literal правилом j mod4, а не новым ориентиром.

Из одних И ТЕХ ЖЕ уже считываемых данных старой AF probability и всех16 CAR raising entries уже получена source-compatible Lorentz metric

    ghat = (μ_x/μbar) g_raw,  Xhat = sqrt(μbar/μ_x) X_native.

Здесь μ_x — mass конкретного сохранённого AF address на физически допущенной PF-prepared branch; в общей подготовке Born qρ(w)≠μ(w), и настоящее равенство qρ=μ НЕ объявляется автоматически. На невырожденном выбранном гладком chart положим

    J(x)=sqrt(|det ghat(x)|)=|det ehat(x)|>0,
    V=∫_[0,1]^4 J(x) dx,    ρ(x)=J(x)/V.

Это **плотность той же source-compatible метрики**, не новый scalar action или prior. Для ориентации и гладкой инверсии требуется ρ∈C^r, r≥1, и 0<m≤ρ≤M<∞ в одном chart.

**Теорема.** Существует ЕДИНСТВЕННАЯ (почти всюду; для smooth positive ρ — обычная smooth) монотонная нижнетреугольная карта R_ρ:[0,1]^4_x→[0,1]^4_u, переводящая ρ(x)dx в du. Её inverse T_ρ=R_ρ^-1 переносит все существующие F/R boxes в физические cells C_w=T_ρ(B_w), и ТОЧНО для каждого w, без предела:

    [∫_(C_w) J dx]/V = |B_w| = μ(w)=p^c(w).              (Q1)

Все leaf codes, cost cuts, complements, failures и вложенные отношения сохраняются; меняется только физический *sampling placement*, не полный исходный Born/Book law. Это не утверждает, что выбранный физический D0 engine уже исполняет T_ρ.

## 2. Явная однозначная 4D формула, а не существование по имени

Для j=0,1,2,3 определим настоящие marginal density:

    m_-1=1,
    m_j(x_0,...,x_j)=∫_[0,1]^(3-j) ρ(x_0,...,x_3) dx_(j+1)...dx_3,
    m_3=ρ.

Все m_j>0. Определим условные CDF:

    R_ρ,j(x_0,...,x_j)
      =∫_0^(x_j) [m_j(x_0,...,x_(j-1),s)/
                  m_(j-1)(x_0,...,x_(j-1))] ds.         (Q2)

Каждая компонента строго возрастает по последней переменной, достигает0,1; поэтому T_ρ вычисляется последовательно четырьмя ОДНОМЕРНЫМИ обратными CDF. Никакого field-dependent matrix inverse or external geodesic oracle не нужно. Нижнетреугольный Jacobian телескопируется:

    det DR_ρ(x) = ∏_(j=0)^3 m_j/m_(j-1)
                =m_3(x)=ρ(x)=J(x)/V,                    (Q3)
    det DT_ρ(u) = V/J(T_ρ(u)).

Это доказывает (Q1) обычной заменой переменных, с полными исходными reference masses, НЕ с необоснованным qρ=μ. Уникальность в классе lower triangular maps с положительными диагоналями следует индукцией из единственности conditional CDF по каждому измерению. В другом классе transport не уникален; его особая triangular ordering является существующим упорядоченным Role/readout contract, который ещё требуется физически допустить.

Если исходные физические proper paths задаются γ_w(u), их настоящий перенос теперь есть T_ρ∘γ_w, а proper Lorentz links вычисляются по полному перенесённому пути, не по хорде. Внешняя операция сдвига sampling не называется новым Dirac и не переносит старые неизмеренные записи без их исходного controller/source.

## 3. Главный потребитель: полный moving-source, а не только совпадение масс

Пусть J_ε — C¹ по ε гладкая положительная coframe density, R_ε её (Q2), T_ε=R_ε^-1. Для КАЖДОГО ε справедливо exact identity

    log det DR_ε(x)=log J_ε(x)-log V_ε.                (Q4)

Следовательно её полный first-jet при фиксированном physical x:

    D_ε log det DR_ε = D_ε log J_ε -D_ε log V_ε.     (Q5)

На исходном reference label u moving physical sample x=T_ε(u) имеет

    D_ε T_ε(u)= -[DR_ε(T_ε(u))]^-1
                  D_ε R_ε(T_ε(u)).                     (Q6)

С тем же μ(w) все физические cells ДВИГАЮТСЯ. Дифференцирование (Q1) даёт истинный Reynolds/source Ward:

    0 = (1/V)∫_(C_w)[D J-J Dlog V] dx
        +(1/V)∫_(∂C_w)J (velocity_boundary·normal)dS.  (Q7)

Нормаль и поверхность берутся в физическом chart; второй boundary term НЕ вправе исчезать при finite sampling. Таким образом D0 проблема §6.40 «fixed word p, moving physical volume» становится одним конкретным source-joint equation, а не подбором density counterterm. В объёмно-сохраняющих family D V=0, и изменение внутренней меры компенсируется ровно boundary-jet. Полный CAR exterior pullback должен использовать все ΛDT_ρ и transported observer J_x: (Q7) сам по себе не доказывает entire native Dirac/Book source equality.

**Важный epistemic boundary:** (Q5)–(Q7) — ТОЧНО вычисленный источник ПРЕДЛОЖЕННОГО совместного readout, не доказательство, что старый raw128 БЕЗ адресного переноса породил его динамически. Совпадение p^cost с новым физическим cell mass — условие *операционного расположения*, а не следствие одного сохранения вероятности исходов.

## 4. Особенно сильный time/lapse consumer: отсутствующий операторный f получается буквально

На одном time-only proper foliation пусть e_ε=c^-1 diag(J_ε(t),1,1,1), J_ε>0, V_ε=∫_0^1 J_ε. Тогда

    R_ε,0(t)=F_ε(t):=[∫_0^t J_ε(s)ds]/V_ε,
    R_ε,i(x)=x_i (i=1,2,3),                            (Q8)
    T_ε,0=F_ε^-1,   Dlog(det e)=Dlog J.

При periodic volume-preserving variation J_ε(t)=1+ε cos(2πt), V_ε=1, первый golden F leaf расположен НЕ по fixed t=p, а по

    t_F(ε)=F_ε^-1(p),
    D_ε t_F|_0=−sin(2πp)/(2π)≠0.                      (Q9)

Old fixed physical interval [0,p] имел бы ошибочную mass
p+ε sin(2πp)/(2π), тогда как истинный moving cell [0,t_F(ε)]
имеет массу ровно p при ВСЕХ малых ε. Это в точности принудительный X_ε=F_ε^-1 X_word из §6.40: без подстановки уравнений Эйнштейна и без замены золотого code/Cost.

При positive inverse-solder Gram G=e^-T e^-1 прежнее операторное measure variation имеет
Dlog|det e|=−(1/2)tr(G^-1 DG), в частности при G=d I и δG00=1
получаем f=−1/(2d). Это ТОТ знак и magnitude, которые в actual
CAR16 continuum source owner восстанавливают lapse Ward
(§6.40(13dn)), вместо вручную назначенного counterterm.
Наш transport производит тот же f из одной и той же измеренной source-compatible геометрии.

## 5. Полная Diff covariance: точное оставшееся представление на истории

У triangular R_ρ есть физически значимое достоинство и граница. При произвольной orientation-preserving smooth diffeo f и преобразованной физической мере ρ'=f_*ρ рассмотрим

    A_(f,ρ)=T_(ρ')^-1 ∘ f ∘ T_ρ
            =R_(ρ')∘f∘T_ρ.                             (Q10)

Тогда A_(f,ρ) сохраняет EXACT исходную равномерную золотую Lebesgue
measure du; это следует композиционной pushforward identity, не предположению
о квантовых гейтах. Более того,

    A_(g∘f,ρ)=A_(g,f_*ρ)∘A_(f,ρ).                       (Q11)

То есть весь Diff действует на данном разложении через ТОЧНЫЙ address
volume-preserving cocycle. Он в общем НЕ равен identity: triangular map
не обязан быть строго equivariant при произвольном f. Полное gauge
D0 → GR требует доказать, что в refined native archive допустим
этот induced address automorphism со всеми его order/holonomy и рабочими
ценами, либо доказать отсутствие его влияния на физические источники.
Из одной конечной site permutation этого не следует; конечная группа
сама не реализует полный непрерывный Diff.

Именно (Q10) — наиболее узкая общая missing arrow от уже принадлежащего
operational Gold/PF clock к полному нелинейному coordinate Ward. Для
time-only monotone f с подходящей нормировкой A может быть identity, что
объясняет доказанный special lapse result. Переход к arbitrary 4D
refoliation требует не новой Einstein-плотности, а физической
релабеллируемости/сравнимости старой непрерывно уточняемой истории.

## 6. Нетривиальный 4D контроль на той же фиксированной мере

Для положительной НЕРАЗДЕЛИМОЙ density
ρ(x)=[1+ε x0 x1]/[1+ε/4], |ε|<1, следует из (Q2) точно:

    R0(x0)= [x0+ε x0²/4]/[1+ε/4],
    R1(x0,x1)= [x1+ε x0 x1²/2]/[1+ε x0/2],
    R2=x2, R3=x3,                                     (Q12)
    det DR=ρ(x).

Все four Rolle fields сохранены. На первой golden F границе u0=p
physical x0=s является ПОЛОЖИТЕЛЬНЫМ корнем
s+ε s²/4=p(1+ε/4). На следующем F по u1=p физическая граница x1
ЗАВИСИТ от x0 через R1(x0,x1)=p — физические cells не обязан
быть rectangular, но их full density-probability точно равна
p² для FF и p³ для FR. Считать вторую границу fixed x1=p
— настоящий неверный code/volume source.

При ε=0 полный first-jet (Q12) даёт

    dotR0=(x0²−x0)/4,
    dotR1=x0(x1²−x1)/2,
    dotR2=dotR3=0,
    div(dotR)=x0 x1−1/4=dot(log ρ).                    (Q13)

Это прямая проверка moving density/shape source на 4D
нефакторизованном поле; не использовано ни δG=Einstein, ни
зарегистрированное уже готовое volume-normalized readout.

## 7. Что это закрывает в единой ОТО, а что реально НЕ закрыто

Этот owner **закрывает конструктивную математическую стрелку**
(conditional positive-PF old-history probabilities + recovered
source-compatible CAR16 metric) → UNIQUE triangular monotone
proper-clock placement + exact Jacobian/source + full Diff address cocycle.
Он конкретно снимает неопределённость функции X_e *в указанном классе
упорядоченных физических readout maps*. Это сильнее произвольного
постулата X_e и сохраняет все source jets и реальные F/R code weights.

Чтобы полная физическая D0→ОТО следовала отсюда, нужны **не три новых
действия**, а один общий native execution/source contract:
1) реальное old-leaf qρ=μ на выбранной PF/critical branch;
2) акт sampling соответствует (Q2) или эквивалентной вариационно
совместимой карте с учётом её operation/controller cost;
3) полный proper CAR16/observer/connection/H+J+R или AF-J2 source
действует на transported tuple и удовлетворяет SAME Book action law,
включая independent matter/spin и clock; затем настоящий controlled
joint h→0 limit и существование решений.

Здесь (1)–(3) перечислены как один интерфейс одной программы,
а не как уже выполненные владельцем доказательства. Конструктивное
наличие и единственность map НЕ вынуждают физический gate selection.
Тем более нельзя объявить physical \widehat g Einstein vacuum
исключительно из Q1–Q13: динамика остаётся владельцем ранее
закрытого геометрического AF/Palatini subprogramme и его собственных
remaining-price/matter constraints. Original raw h^-2/#216 не
подменяется этой плотностной геометрией.

**Decisive test:** on the SAME admitted native programme compare
its true moving sampling effect/costate with the (Q6–Q7) conditional
Jacobian source for a nonconstant proper lapse and one shearing 4D
density; reject physical identification if their difference survives
on an admitted metric/matter tangent. The existing [full experiment Ward]
(A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md) provides the tensorial
transport theorem once the actual X_ε is supplied.

**Reproducible mathematical checker:**
[quantile-clock checker](certificates/a4d_golden_quantile_clock_source_check.py).
It verifies the explicit 1D lapse Born/volume mismatch, the correct
moving first derivative, the nonseparable 4D conditional CDF/Jacobian,
and the source identity (Q13). It does NOT run a full native128
physical gate, read an unknown field without preparation, or claim the
entire Einstein system.
