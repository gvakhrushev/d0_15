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


## 8. Source-controlled refinement of the ENTIRE moving golden quadrature (not just its mass)

The exact Jacobian (Q3) permits a stronger consequence with no new action. For every actual smooth local scalar **candidate integrand** \(L_\theta(x)\) of one common field/source chart \(\theta\), define its original physical unnormalized density integral and its native-address quadrature:

\[
S_\infty(\theta)=\int_{[0,1]^4}J_\theta(x)L_\theta(x)\,dx,\qquad
S_n(\theta)=V_\theta\sum_{w\in C_n}\mu(w)
             L_\theta(T_{\rho_\theta}(c_w)).
\tag{Q14}
\]

Here \(c_w\) is the **existing centre** of the golden leaf box \(B_w\), \(J_\theta=\sqrt{|\det\widehat g_\theta|}\), \(V_\theta=\int J_\theta\) and \(\rho_\theta=J_\theta/V_\theta\). The factor \(V_\theta\) is **retained and varied**, not silently set to one or subtracted: it is essential for cosmological/volume-source claims. All raw cost cuts, pending leaves, old probabilities and half-density factors remain intact.

By (Q3), this is *exactly* ordinary quadrature of \(F_\theta(u)=V_\theta L_\theta(T_{\rho_\theta}(u))\) against the fixed golden \(du\). The partition owner proves \(\operatorname{diam}B_w\le\delta_n=2p^{\lfloor n/8\rfloor}\). Therefore for every finite multidirectional chart \(\theta\), and every \(j=0,1,2\) for which all parameter jets and their \(u\)-Lipschitz bounds exist uniformly,

\[
\boxed{
 \sup_\theta\|D_\theta^j S_n-D_\theta^j S_\infty\|
 \le \delta_n\,
     \sup_\theta\operatorname{Lip}_u
       \bigl(D_\theta^j[V_\theta L_\theta\circ T_{\rho_\theta}]\bigr).
}
\tag{Q15}
\]

**Proof:** in every \(B_w\), \(|F_\theta(c_w)-F_\theta(u)|\le\operatorname{Lip}(F_\theta)\delta_n\); integrate and sum with the *actual* \(\mu(w)=|B_w|\). The partition is complete and \(\sum_w\mu(w)=1\). Differentiate the identity \(\int F_\theta du=\int J_\theta L_\theta dx\) under the integral. The same argument applies to each derivative, with NO finite leaf-count factor. This is a source theorem and not merely weak convergence of values. No inverse Hessian or metric Einstein equation is assumed.

The first source **explicitly** keeps BOTH moving terms:

\[
DS_n[V]
=DV\sum_w\mu_w L(Tc_w)
+V\sum_w\mu_w
 \bigl[DL[V](Tc_w)+\nabla_xL(Tc_w)\cdot DT[V](c_w)\bigr].
\tag{Q16}
\]

\(DT\) is the already derived inverse-CDF expression (Q6), so the second term is a genuine moving-sample/source contribution. At the continuum limit this is precisely \(D\int JL\,dx\), with the true \(DJ\) and \(DV\) retained. A fixed-cell approximation would omit the \(DT\) term and fail the time-lapse control (Q9).

**Quantitative joint refinement consumer.** If the *actual supplied local field/source* has derivatives satisfying
\(\operatorname{Lip}_u D^j_\theta(VL_\theta\circ T_{\rho_\theta})\le C h^{-q}\), \(j\le2\), then choose the sufficient mathematical depth
\[
n(h)=\left\lceil 8(q+2)\log_\varphi(1/h)\right\rceil,\quad h<1.
\tag{Q17}
\]
Since \(\delta_n\le2p^{-1}p^{n/8}\), (Q15) yields \(O(h^2)\) on values AND all admitted first/second sources, despite actual \(h^{-q}\) singular stencil factors. The depth grows only logarithmically with spatial resolution. This is **not** a physically derived native clock, nor an estimate for the raw #216 response: it requires the actual \(q\) source norm and map to that comparator, including all \(h^{-4}\) site and \(h^{-1}\) relative-solder scalings, to be supplied by their owners. It does not prove that the unmodified old Julia channel has the integrand \(L_\theta\).

**Nonseparable exact source control.** With \(\rho_\epsilon=(1+\epsilon x_0x_1)/(1+\epsilon/4)\) and \(L(x)=x_0^2+x_1x_2\), the *physical normalized* mean is
\[
\int L\rho_\epsilon dx
=\frac{7/12+(5/24)\epsilon}{1+\epsilon/4},
\qquad
\left.\frac d{d\epsilon}\right|_0\int L\rho_\epsilon dx
=\frac1{16}.
\tag{Q18}
\]
The full moving-address first jet from (Q13) on the original golden centres is
\[
\left.\frac d{d\epsilon}\right|_0\sum_w\mu_w L(T_\epsilon c_w)
=\sum_w\mu_w\left[
\tfrac12u_0^2(1-u_0)
+\tfrac12u_0u_2u_1(1-u_1)\right]_{u=c_w}.
\tag{Q19}
\]
It tends to \(1/16\) with (Q15). An independent finite cost-cut enumeration through \(n=18\) checks the full 6765-leaf source; the error is \(2.30\cdot10^{-4}\), versus \(1.02\cdot10^{-2}\) at depth 2. This control is about actual moving-cell calculus, not another fitted gravitational action.

## 9. The full 4D Diff address cocycle is unavoidable, but the GOLDEN AF tower approximates it without crossing the two cost sectors

There is a clean no-go to shortcut (Q10): for \(\rho=1\), every smooth volume-preserving \(f\) has \(f_*\rho=\rho\). No deterministic map \(T_\rho\) chosen from **the measure alone** can satisfy strict equivariance \(T_{f_*\rho}=f\circ T_\rho\) for all such \(f\), since it would force \(T_1=f\circ T_1\). Taking two orientation-preserving coordinate swaps gives a concrete \(f\ne I\). Thus strict Diff covariance necessarily acts on the **old address** through the real cocycle \(A_{f,\rho}\), or through more extensive relational field data. Calling a Rosenblatt chart itself a full native Diff gauge law would be circular.

The positive result is much stronger than merely assigning \(A_{f,\rho}\) a name. It can be approximated in its *observable probability source topology* by the EXISTING two AF block types, **without any READY↔PENDING mixing**.

### 9.1. Exact Bernoulli–Fibonacci type mixing of every old macro-address

On the cost-\(n\) complete golden cut let \(W_n^R,W_n^P\) be READY and PENDING terminal leaves. Their counts are \(|W_n^R|=F_{n+1}\), \(|W_n^P|=F_n\), their **individual** masses are \(p^n,p^{n+1}\); hence both types are actual nonzero-weight subfamilies, not filters. Under the original binary no-11 encoding, the actual *conditional probability* transition matrix on these two states is

\[
K=\begin{pmatrix}p&p^2\\1&0\end{pmatrix},\quad
\pi=\left(\frac1{1+p^2},\,\frac{p^2}{1+p^2}\right).
\]
It satisfies the **EXACT** operator identity
\[
K^r=\mathbf 1\pi+(-p^2)^r(I-\mathbf1\pi),\qquad r\ge0.
\tag{Q20}
\]
Thus, for every earlier cylinder \(B_v\) at cost \(k<n\), the conditional later READY/PENDING mass is within \(p^{2(n-k)}\) of the **same** vector \(\pi\), independent of its old type. All earlier address/provenance labels and old total probabilities are retained; no raw history is postselected.

Let \(\nu_{n,s}=\sum_{w\in W_n^s}\mu(w)\delta_{c_w}\), and \(m_s(n)=\nu_{n,s}([0,1]^4)\). For the ordinary 1-Wasserstein distance on finite measures of equal mass (the constant mass is \(m_s(n)\)) the exact prefix decomposition, Lipschitz quadrature on old boxes and (Q20) give

\[
\boxed{
W_1\bigl(\nu_{n,s},m_s(n)\,du\bigr)
\le 2\delta_k+4p^{2(n-k)}
=:e_{n,k},\quad s\in\{R,P\}.
}
\tag{Q21}
\]
To prove this, replace all fine centres by their containing old \(B_v\) centre, error \(\le\delta_k\); replace the old prefix's type mass by \(m_s(n)\mu(v)\), error \(\le2p^{2(n-k)}\mu(v)\) times at most diameter 2; and replace the coarse quadrature by \(\int du\), error \(\le\delta_k\). The factors in (Q21) are deliberately conservative. Choose \(k=\lfloor 16n/17\rfloor\); then \(\delta_k=O(p^{k/8})\) and
\[
e_{n,k}=O(p^{2n/17}).                                  \tag{Q22}
\]

### 9.2. A bona fide weight-preserving finite LEFT AF permutation for every smooth 4D Diff

Let \(A:[0,1]^4\to[0,1]^4\) be ANY Lebesgue-preserving Lipschitz map, in particular the induced exact \(A_{f,\rho}\) from (Q10). Then
\[
W_1(\nu_{n,s},A_*\nu_{n,s})
\le(1+\operatorname{Lip}A)e_{n,k}.                     \tag{Q23}
\]
Both atomic measures have **identical lists of weights within each type**: \(p^n\) for READY, \(p^{n+1}\) for PENDING. The finite transport linear programme has a permutation extreme point (Birkhoff/assignment theorem), giving a pair of permutations \(\sigma_{n,R}\in S_{F_{n+1}}\), \(\sigma_{n,P}\in S_{F_n}\) such that

\[
\boxed{
\sum_{w\in W_n}\mu(w)\,
 \bigl|c_{\sigma_n(w)}-A(c_w)\bigr|
\le2(1+\operatorname{Lip}A)e_{n,k}
=O(p^{2n/17}).
}
\tag{Q24}
\]
Here \(\sigma_n\) acts **within each original type**. It therefore exactly preserves each probability \(\mu(w)\), full cost, READY/PENDING totals and all rejected/failure complements, not just their weak limits. It is an actual unitary permutation on the defining AF algebra \(M_{F_{n+1}}\oplus M_{F_n}\); its LEFT multiplication on the regular GNS commutes with the full original RIGHT archive. It does not require the missing cross-block preparation rotation (whose purpose was to produce a different finite uniform distribution).

For any Lipschitz physical scalar test \(F\), (Q24) implies
\[
\biggl|\sum_w\mu(w)F(c_{\sigma_n(w)})
        -\sum_w\mu(w)F(A(c_w))\biggr|
\le \operatorname{Lip}(F)\,2(1+\operatorname{Lip}A)e_{n,k}.
\tag{Q25}
\]
The first finite sum also equals \(\sum_w\mu(w)F(c_w)\) **EXACTLY**, since \(\sigma_n\) preserves the individual masses. Thus the golden AF carrier already has *asymptotically the full measured-volume-preserving address symmetry*: not just its two block dimensions, but explicit finite probability-preserving transformations with quantitative approximation and a preserved RIGHT archive. This is a mathematically valid **value/readout covariance** of scalar address observables. It is NOT yet covariance of derivative-dependent native CAR/link/Palatini operators; those require proper path, coframe, connection, work and source transport on the same real history.

**Independent finite control.** The actual role-ordered 4D boxes were enumerated to cost12 (377 leaves), then matched separately within READY and PENDING by exact-size finite assignment for the nontrivial orientation-preserving volume map \(A(u_0,u_1,u_2,u_3)=(u_1,u_0,u_3,u_2)\). Total weighted transport cost drops from \(\approx0.27850\) at cost4 to \(\approx0.08039\) at cost12. This does not substitute for the proof of (Q21–Q24).

### 9.3. Exact finite NO-GO for an infinitesimal Ward from mere permutations

For each finite \(n\), \(S_{F_{n+1}}\times S_{F_n}\) is discrete. Every continuous \(t\mapsto\sigma_n(t)\) in that finite group is therefore **constant**. The exact finite permutation statement (Q24) CANNOT be differentiated in \(t\) to infer a nonzero Lie/diffeomorphism Ward generator. Neither a pure type-count equivalence nor C⁰ approximation of outcome values is a first-source theorem for moving external geometry. A physical operator flow must use genuine continuous coherent native controls/conditional comparisons (with their full work/price source) or the direct moving-quantile source formula (Q16), whose C¹ error is independently controlled by (Q15).

This resolves a strategic confusion: the old RIGHT-center obstruction does not prevent *asymptotic measured 4D coordinate covariance*, while the finite code cannot by itself guarantee *dynamic 4D refoliation covariance*. The missing input is now a precisely typed **moving control/source** identity, not a new Einstein tensor or an artificial cross-center mixer.

## 10. Immediate GR consumption — two remaining SAME-program arrows, not another scalar root

Combining (Q1–Q25) with the existing nonlinear finite AF/Palatini and density-dressed CAR16 theorem yields an exact **geometric transport/comparison package**:
\[
(\text{old golden }\mu,\ \widehat g[\mu,X_{\rm CAR}])
\to T_{\rho[\widehat g]}
\to \bigl(\text{complete moving clocks, measure and sampling first source}\bigr)
\to \bigl(\text{asymptotic AF address Diff symmetry}\bigr).
\]
This is an independently proved *kinematic and source-quadrature* bridge; it does not identify any physical D0 action with Einstein by decree.

For **the actual physical D0→ОТО**, the two consuming requirements that remain are:
(i) **one native executor/same-history price** admitting the selected old-leaf+CAR16 query, its field-dependent inverse-clock placement and its full controller/work/measure \(Q16\) source (without inserting it only after varying the desired action);
(ii) **one common stationary matter+geometry limit** in which the complete remaining H+J+R/AF-feedback Book price produces independent material stress, its true Ward conservation and all ten Lorentz equations on \(\widehat g\), with proper normal/soft/UV estimates. Nine null equations then reconstruct all Einstein rows including a constant \(\Lambda\).

Neither follows merely from the existence of \(T_\rho\) or probability-preserving AF permutations. The point of the new theorem is to supply a *source-preserving clock/refinement interface* that is already nontrivial and checkable on the original golden partition, rather than leave "proper time/volume" as a free choice. The original raw #216 fixed \(h^{-2}\) and full physical action comparison are not promoted.

A matching [bounded checker](certificates/a4d_golden_quantile_clock_source_check.py) now certifies (Q8–Q9), (Q12–Q13), the exact symbolic source derivative (Q18–Q19), the type-mixing (Q20), cut probabilities and the type-preserving matching on actual 4D boxes. It is a local proof control, not a full native physical readout.
