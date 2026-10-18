# D0 → ОТО: одна метрика из золотой меры, полной CAR16 и вариационного \(\star\)-источника

18 октября 2026 · непосредственное положительное потребление действующего Draft #334. **Тип:** EXACT FINITE DENSITY/COFRAME AND CAR16 SOURCE/METRIC WELD + EXISTING NONFLAT FULL-40-ROW RECOVERY. Ни нового физического действия, ни новой константы, ни нового observer stress, ни смены исходного #216 терминала. Итог относится к собственному сконструированному AF–⋆-геометрическому процессу и его действительным измеренным весам; его буквальная физическая селекция из полного D0 остаётся самостоятельным вопросом.

### Потреблённые входы (без повторного доказательства)

- [Полная искривлённая AF–⋆ семья](A4D_AF_STAR_FULL_LATTICE_STATIONARY_FAMILY_2026_10_17.md), §§2–6: конечная \(\star\)-плотность с независимыми 16 coframe и 24 Lorentz-link строками; точная weighted source reflection (4.3), исходные неравномерные golden counts и явная неплоская pp-wave с \(C^2\) recovery.
- [Полная labelled история](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md), §§6.3–6.10, особенно (13a–m), (13n–q): реальные \(\mu_x\)-preparation variations, свободная \(\chi\)-семья, weighted Palatini и нелинейный source transfer; fine measured-old-history вариант отдельно выбирает свои leaf weights, и **не отождествляется** со свободной пятифлаговой preparation.
- Тот же owner, §§8.4–8.5, (25)–(31): полное восстановление \(u_r,M_r\) из истинного full-Lorentz native forward \(X_r=C(u_r)\Lambda M_r\), включая nonzero-null; собственный CAR/clock Gram \(q^{rs}=u_r^TJu_s\), операционная \(g=q^{-1}\), инверсия настоящего \(F=e^{-1}\).
- [Weighted source/observer](A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md) и [density/Palatini](A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md), §3: moving density/adjoint и точная в размерности четыре density–coframe замена.
- [Full AF Book price/LEFT pointer](A4D_AF_FIXED_POINTER_BOOK_INFORMATION_SOURCE_2026_10_17.md): условная физическая интерпретация same-history \(w=q\), полные исходы и граница native-test admission.

## 1. Прямая конечная теорема: мера и тетрада суть ОДНА гравитационная переменная

Фиксируем один конечный 4-Role carrier и разрешённые собственные **положительные** массы старых событий \(\mu_x>0\) (например, сумму реальных AF-листовых вероятностей, попавших в ячейку \(x\)). Число \(\bar\mu>0\) — **уже фиксированный** общий эталон этого уровня, например средняя canonical golden масса; это не новое вариационное поле и не физическая свободная константа. Пусть все четыре relative-solder ноги \(v_{x,r}\), \(r=0,\ldots,3\), независимы на данном сайте, а \(U\) — те же proper-Lorentz based links, что в исходной \(\star\)-плотности.

Оригинальная плотность \(\mathcal P_{\star,x}(v,U)\) однородна по ВСЕМ четырём ногам **одного** anchor \(x\) ровно степени два:

\[
\mathcal P_{\star,x}(a_xv_x,U)=a_x^2\mathcal P_{\star,x}(v_x,U),\qquad a_x>0.
\]

Определяем **составную тетраду** и её физический кандидат-метрику:

\[
\boxed{\widehat v_{x,r}=\sqrt{\mu_x/\bar\mu}\,v_{x,r},
\qquad
\widehat e_x=\sqrt{\mu_x/\bar\mu}\,e_x,
\qquad
\widehat g_x=\frac{\mu_x}{\bar\mu}\,e_x^T\eta e_x.}
\tag{1}
\]

Тогда на КАЖДОЙ конечной решётке, без приближений, тепловых следов, идеальных метрических вариаций или предположений о плоском фоне:

\[
\boxed{\mathcal P_\mu(v,U):=\sum_x\mu_x\mathcal P_{\star,x}(v,U)
      =\bar\mu\sum_x\mathcal P_{\star,x}(\widehat v,U)
      =\bar\mu\,\mathcal P_\star(\widehat v,U).}
\tag{2}
\]

Это равенство **функций на полном coframe/link/weight chart**, а не только значений на pp-wave. Поэтому оно сразу задаёт их действительные first/second вариации (при любой smooth C² кривой также сохраняется второй chain-rule член). В частности, при произвольном \((\delta\mu,\delta v,\delta U)\)

\[
\delta\widehat v_x
=\sqrt{\mu_x/\bar\mu}
 \left(\delta v_x+\frac{\delta\mu_x}{2\mu_x}v_x\right),
\tag{3}
\]
\[
\boxed{
D\mathcal P_\mu[\delta\mu,\delta v,\delta U]
=\bar\mu D\mathcal P_\star(\widehat v,U)
              [\delta\widehat v,\delta U].
}
\tag{4}
\]

Смена \((v,\mu)\leftrightarrow(\widehat v,\mu)\) обратима в positive interior. **При фиксированной \(\mu\)** все 16 независимых тетрадных и все 24 независимых связевых Euler rows из \(\mathcal P_\mu\) равны нулю ТОГДА И ТОЛЬКО ТОГДА, когда эти строки исходного unweighted \(\star\)-действия равны нулю на \((\widehat v,U)\). При свободных массах (4) также даёт собственные preparation rows; на полном coframe критическом множестве они автоматически исчезают у **этого геометрического функционала**. Самостоятельная энтропийная цена старой истории остаётся своей частью полного действия, её prep equations нельзя удалять.

Рассмотрим finite local operation на weights/legs:

\[
\boxed{
\mu_x\mapsto\mu'_x=\chi_x\mu_x,\quad
v_{x,r}\mapsto v'_{x,r}=\chi_x^{-1/2}v_{x,r},\quad
U\mapsto U,\quad \chi_x>0.
}
\tag{5}
\]

По (1) \(\widehat v'_x=\widehat v_x\), следовательно и \(\widehat g'_x=\widehat g_x\): **это ТОЧНАЯ компенсационная симметрия всего weighted \(\star\)-геометрического функционала**. Её infinitesimal \(D\mu_x=2\sigma_x\mu_x,\ Dv_x=-\sigma_xv_x\) даёт при каждом anchor отдельную конечную Ward identity

\[
\boxed{
2\mu_x\frac{\partial\mathcal P_\mu}{\partial\mu_x}
-\sum_{r,a}v^a_{x,r}\frac{\partial\mathcal P_\mu}{\partial v^a_{x,r}}=0.
}
\tag{6}
\]

Она получается от original quadratic homogeneity, а не объявляется новой Weyl gauge of all D0 histories.

## 2. Решающая сцепка с ОПЕРАЦИОННОЙ метрикой: не только замена переменных действия

В настоящем positive/principal Lorentz chart D0 (§8.4–8.5 source) исходные четыре raising оператора имеют тот же recovered full16 вид

\[
X_{x,r}=C(u_{x,r})\Lambda M_{x,r},\qquad
q^{rs}_x=u_{x,r}^{T}J_xu_{x,s},\qquad g_x=q_x^{-1}.
\tag{7}
\]

Исходная тетрада в этом chart удовлетворяет \(F_x=e_x^{-1}\); поэтому компенсация (5) влечёт
\[
F'_x=\sqrt{\chi_x}\,F_x,\quad
u'_{x,r}=\sqrt{\chi_x}\,u_{x,r},\quad
X'_{x,r}=\sqrt{\chi_x}\,X_{x,r},
\tag{8}
\]
если настоящий Lorentz \(M\), выбранный principal \(J_x\) и его observer transport сохраняются в **той же согласованной** frame. Для other frame choices нужно переносить \(J\), а не замораживать необозначенный observer.

Комбинируем уже существующие **две считываемые величины**: (i) массу полного старого AF-листового события \(\mu_x\), (ii) все 16-grade native raising entries \(X_{x,r}\). Вводим их определённое, без нового experiment, site-normalized reading:

\[
\boxed{
\widehat X_{x,r}
:=\sqrt{\bar\mu/\mu_x}\,X_{x,r},\quad
\widehat u_{x,r}:=\sqrt{\bar\mu/\mu_x}\,u_{x,r},\quad
\widehat q_x^{rs}
=\frac{\bar\mu}{\mu_x}q_x^{rs},\quad
\widehat g_x=(\widehat q_x)^{-1}
=\frac{\mu_x}{\bar\mu}g_x.
}
\tag{9}
\]

Следуя (8), \(\widehat X'=\widehat X\), \(\widehat q'=\widehat q\), \(\widehat g'=\widehat g\) **точно на всей finite site family (5)**. Таким образом метрика, выбранная *weighted gravitational source* (1)–(4), **совпадает с составной метрикой, считываемой из настоящего полного CAR16 и настоящих old-history probabilities после (единственной) site-normalization (9)**. Её не нужно объявлять равной внешне выбранной metric g и не требуется добавлять ten correction components к Einstein.

**Полные действительные first jets (без frozen site weights).** При любом движущемся \(\mu\), coframe, Lorentz \(M\), observer \(J\) и подготовке, с фиксированным \(\bar\mu\), обычное chain rule даёт
\[
\boxed{
D\widehat X[V]=\sqrt{\bar\mu/\mu}
       \left(DX[V]-\tfrac12 X\,D\log\mu[V]\right),}
\]
\[
\boxed{
D\widehat q^{rs}[V]=\frac{\bar\mu}{\mu}
   \left(Dq^{rs}[V]-q^{rs}D\log\mu[V]\right),\quad
D\widehat g_{rs}[V]=\frac{\mu}{\bar\mu}
   \left(Dg_{rs}[V]+g_{rs}D\log\mu[V]\right).
}\tag{9a}
\]
Здесь \(Dq\) включает **оба** полных \(Du\) и \(DJ\); \(DX\) содержит \(\Lambda(DM)\), а не лишь frozen-Riemannian metric variation. Эти формулы сохраняют весовой edge-jet и его moving-preparation часть при подстановке настоящего источника. Если \(\bar\mu\) сам меняется физически, добавляется \(\tfrac12D\log\bar\mu\) в \(D\widehat X/\widehat X\); обозначение «фиксированный \(\bar\mu\)» является частью этого source chart.

**Все десять метрических вариаций остаются реальными.** При невырожденном \(\widehat e\), линейная карта \(\delta\widehat e\mapsto\delta\widehat g\) имеет прежнюю явную правую обратную
\[
W_{\widehat e}(V)=\frac12\widehat e\,\widehat g^{-1}V,
\qquad
D_{\widehat e}\widehat g[W_{\widehat e}(V)]=V
\]
для любой симметричной \(V_{\mu\nu}\) (из-за \(e^T\eta e\)). При фиксированной \(\mu\) требуемая \(\delta e=\sqrt{\bar\mu/\mu}\,W_{\widehat e}(V)\) реализует такой \(V\), поэтому \(\chi\)-компенсатор не уничтожает lapse/shift или одну из шести пространственных metric rows. Он только отделяет лишнее **представление** одного gravitational source от десяти действительных ковекторов. Физический native image этих тестов требует собственного readout/admission contract, как и в исходном owner.

**Уникальность показателя.** В классе local density-power normalizations \(Y_x=\mu_x^\alpha X_x\) точная компенсационная инвариантность при ВСЕХ \(\chi_x>0\) требует \(\chi_x^{\alpha+1/2}=1\), значит \(\alpha=-1/2\) **однозначно**. Глобальный \(\sqrt{\bar\mu}\) фиксирует исходную normalization convention этого golden cost cut; он НЕ fit Newton constant и не добавляется в физическое действие. Источник выбрал scale weight \(1/2\), а не удобное после-факта metric dressing.

Ещё сильнее: на полном 16-grade CAR, пусть
\(\widehat\Gamma_{x,r}=C(\widehat u_{x,r})+\iota_{J_x\widehat u_{x,r}}\).
Тогда буквально из исходных CAR соотношений
\[
\boxed{\{\widehat\Gamma_{x,r},\widehat\Gamma_{x,s}\}
=2\widehat q_x^{rs}I_{16}.}\tag{10}
\]

Это точная кинематическая **universality of the principal symbol**: та же \(\widehat g\) управляет ведущим Clifford/CAR оператором, который доступен из нормированных native coefficients, и гравитационной \(\star\)-вариацией. Никакой независимый metric tensor, spinor coupling или Einstein stress здесь не вставлен. Для настоящего wave/matter propagation требуются полные native dynamics, subprincipal/clock/connection jets и физический выбор такого reading; (10) их не выдаёт.

Конкретный физический measurement contract теперь сведен к проверяемой паре: один действительно сохранённый old-leaf AF probability \(\mu_x\) и один его собственный (properly transported) native raising \(X_x\) должны быть доступны **в одном общем эксперименте**. Их измеренные значения позволяют вычислить (9) как постобработку, без физического gate \(\widehat X\) и без eigenvector oracle. Отдельные marginal experiments, не сохраняющие общую reference/preparation, ещё не доказывают этот контракт.

### 2.1. Весь edge/adjoint оператор и его собственный density-jet, не только site metric

Чтобы (9) не осталось поточечным именем метрики, рассмотрим **на том же уже существующем полном lattice×CAR16 носителе** его настоящий counting representation и derived positive weighted representation. Пусть \(\mathscr D_{\widehat X}\) — любое конечное операторное expression из одетых \(\widehat X_{x,r}\), proper Lorentz \(\Lambda M\), их настоящего exterior adjoint и фиксированных ориентированных shift-перестановок, **полностью определённое этими данными** в \(\ell^2(\mathrm{sites})\otimes\Lambda^*\). Оно может быть прежним true-adjoint Dirac construction, когда все его operator/source inputs представлены в этом chart; мы не объявляем другой Dirac уже физически выбранным.

Натуральное weighted скалярное произведение для той же старой вероятностной меры:
\[
\langle\psi,\phi\rangle_\mu
 =\sum_x\frac{\mu_x}{\bar\mu}\langle\psi_x,\phi_x\rangle_{\Lambda^*},
\qquad
(\mathcal U_\mu\psi)_x
=\sqrt{\mu_x/\bar\mu}\,\psi_x .
\]
\(\mathcal U_\mu:\mathcal H_\mu\to\mathcal H_{\rm counting}\) — точная **унитарная** карта, с full16 на каждом сайте, без исключения ни одной grade. Определим не новую независимую динамику, а её *однозначно сопряжённое представление*
\[
\boxed{\mathscr D_\mu
=\mathcal U_\mu^{-1}\mathscr D_{\widehat X}\mathcal U_\mu.}
\tag{10a}
\]
Если оператор в counting chart самосопряжён, \(\mathscr D_\mu\) самосопряжён именно в \(\mathcal H_\mu\), хотя не обязан быть Hermitian при ошибочно зафиксированном counting adjoint. Для ориентированного edge \(y\to x\), исходящего из базовой matrix \(\widehat X_{xy}\), элемент (10a) равен
\[
\boxed{(\mathscr D_\mu)_{xy}
=\sqrt{\mu_y/\mu_x}\,(\mathscr D_{\widehat X})_{xy}.}
\tag{10b}
\]
**Ориентация здесь указана явно:** для обратного edge \(x\to y\) endpoint-фактор инвертируется. Это ровно half-density перенос; его derivative нельзя заменить frozen coframe jet.

При той же \(\chi\)-компенсации (5) имеем \(\widehat X'=\widehat X\), значит \(\mathscr D'_{\widehat X}=\mathscr D_{\widehat X}\) как operator в общем counting chart. Пусть
\(T_\chi=\mathcal U_\mu^{-1}\mathcal U_{\mu'}=\operatorname{diag}_x\sqrt{\chi_x}\).
Тогда **точно на конечной сетке**:
\[
\boxed{
\mathscr D_{\mu'}=T_\chi^{-1}\mathscr D_\mu T_\chi,\quad
(\mathscr D_{\mu'})_{xy}
=\sqrt{\chi_y/\chi_x}\,(\mathscr D_\mu)_{xy}.
}
\tag{10c}
\]
При \(\chi_x(s)=e^{2s\sigma_x}\) из того же exact family следует весь первый field-jet
\[
\boxed{
\dot{\mathscr D}_\mu=[\mathscr D_\mu,\Sigma],\quad
(\dot{\mathscr D}_\mu)_{xy}=(\sigma_y-\sigma_x)(\mathscr D_\mu)_{xy}
=\tfrac12(\dot{\log\mu_y}-\dot{\log\mu_x})(\mathscr D_\mu)_{xy},
\quad\Sigma=\operatorname{diag}(\sigma_x).
}
\tag{10d}
\]

То есть endpoint-jet является **внутренним commutator-jet точной движущейся Hilbert representation**, а не добавленным observer/matter stress. Для каждого полинома \(F\) на этом конечном carrier
\[
\operatorname{Tr}_{\mathcal H_{\mu'}}F(\mathscr D_{\mu'})
=\operatorname{Tr}_{\rm counting}F(\mathscr D_{\widehat X})
=\operatorname{Tr}_{\mathcal H_\mu}F(\mathscr D_\mu).
\tag{10e}
\]
Аналогичное spectral statement верно для любых regular matrix functions от \(\mathscr D_\mu^2\), если они определены в общем positive carrier. В первом источнике trace commutator исчезает цикличностью, с настоящими \(\dot\mu\), \(\dot X\) и transported adjoint. Поэтому **на compensator orbit не появляется независимый density-source в самом таком CAR spectrum**.

Вместе (2), (9), (10a–e) дают более сильное точное склеивание:
\[
\boxed{
\text{старые AF вероятности } \mu
+\text{ genuine full16 raising } X
\ \longrightarrow\
(\widehat g,\mathscr D_{\widehat X})
}
\]
и **одна** пара \((\widehat g,\mathscr D_{\widehat X})\) одновременно управляет weighted-star вакуумной геометрией, Clifford principal symbol (10) и полным positive CAR spectral carrier (10e) в рассматриваемом representation class. Чтобы потребить это как настоящий материальный source самого D0, необходимо доказать, что **реально выбранный native operator/clock/full price** — именно данная совместно нормированная репрезентация, а не иная positive weighted completion. Но *endpoint factors, their variations and same-carrier spectral consistency* теперь вычислены, а не названы.

## 3. Вся реальная Book-цена: точная причина, почему это nonlinear Einstein SOURCE, а не только Weyl-переименование

Сконструированная полная AF Book-prepared geometric component в прежних owners имеет действительный finite form
\[
\mathcal A_{\mu,t}
=\sum_x\mu_x\,\Phi_t(f_x(v,U)),\quad
f_x=h^{-4}\mathcal P_{\star,x}(v,U),\quad
\Phi_t(0)=0,\quad \Phi'_t(0)=c_t\ne0,                 \tag{11}
\]
с общими factors внутри \(\mu\), \(c_t\) и полным фиксированным blank baseline, и exact nonlinear radial source transformation §6.10/(13p) при полной old-fine-leaf stationary section. Функция \(\Phi_t\) здесь **действительная аналитическая оконная функция пятиисходного Book-отклика**, а не новый gravitational coupling.

Относительно компенсации (5) \(\mathcal A_{\mu,t}\) в общем **НЕ off-shell Weyl invariant**. Однако его НЕИНВАРИАНТНАЯ часть вычисляется **точно** из исходного \(\Phi_t\):
\[
D_\sigma\mathcal A_{\mu,t}
=2\sum_x\sigma_x\mu_x[\Phi_t(f_x)-f_x\Phi'_t(f_x)].
\tag{12}
\]
При \(|f_x|\le\delta\) и \(\sup_{|s|\le\delta}|\Phi_t''(s)|\le M_2\)
\[
|D_\sigma\mathcal A_{\mu,t}|
\le M_2\sum_x|\sigma_x|\mu_x|f_x|^2.                \tag{13}
\]
**На полном \(f_x=0\) корне** справа ноль и её первый variation по ЛЮБОМ полевому направлению тоже ноль. Вся геометрическая first source того же Book-прибора равна
\[
\boxed{
D\mathcal A_{\mu,t}\big|_{f=0}
=c_t D\mathcal P_\mu
=c_t\bar\mu D\mathcal P_\star(\widehat v,U).
}
\tag{14}
\]
Таким образом ВСЕ самостоятельные coframe/link/weight Euler rows одного finite Book geometry-source на этой branch переходят к известной unweighted star системе на \(\widehat v\), без t→0, без добавления Cartan или Einstein term и без подгонки зануляющей \(\chi\) массы. Вдоль критической подготовительной \(\chi\)-орбиты \(\widehat g\) остаётся одной и той же.

На полном geometric joint critical set \(D\mathcal A=0\) из дифференцирования (12) следует, что compensator tangent \(W_\sigma=(2\sigma\mu,-\sigma v,0)\) лежит в kernel **полного geometric Hessian**:
\[
\boxed{D^2\mathcal A_{\mu,t}[V,W_\sigma]=0\quad
       \text{при } f=0,\ D\mathcal A=0.}             \tag{15}
\]
При доказательстве необходимо учесть field dependence \(W_\sigma\) в тождестве \(D\mathcal A[W_\sigma]\); соответствующий добавочный член пропорционален \(D\mathcal A=0\). Это критическая-орбитная нуль-мода, не утверждение exact off-shell gauge invariance всей native цены.

Если старая полная Y-история включена в ту же цену, её настоящий entropy \(H(\mu)\) имеет дополнительные prep rows и может выбрать одну \(\chi\) в каждой orbit (см. source §6.7). Это НЕ меняет геометрический source/metric (14)/(9) выбранной точки; но не следует называть (15) нуль-модой полной Y-inclusive Hessian. Таким образом D0 допускает как свободную, так и выбранную preparation branch **без изменения выводимых vacuum gravitational equations для \(\widehat g\)**.

## 4. Результат на уже построенной НЕПЛОСКОЙ полной40-row семье

Потребляем без повторного поиска [explicit pp-wave](A4D_AF_STAR_FULL_LATTICE_STATIONARY_FAMILY_2026_10_17.md), §3–6:
\[
g_{\rm pp}=2du\,dv+[A(x^2-y^2)+2Bxy]du^2-dx^2-dy^2,\quad
(A,B)\ne(0,0).
\]
Её exact finite full40 interior Euler roots с истинными golden counts используют \(\bar\mu\) и sitewise \(\rho_{n,x}=\mu_{n,x}/\bar\mu\); исходная finite coframe есть \(v_{n,x}=\rho_{n,x}^{-1/2}\bar v_{n,x}\). Поэтому наша (1) даёт **тождественно, а не только по пределу**,
\[
\boxed{\widehat v_{n,x}=\bar v_{n,x},\qquad
\widehat e_{n,x}=h_n^{-1}\bar v_{n,x},\qquad
\widehat g_{n,x}=g(h_n^{-1}\bar v_{n,x})}.\tag{16}
\]
На том же owner \(C^2\) recovery \(\widehat g_n\to g_{\rm pp}\), с точными finite interior 40 Euler rows. Нулевая плотность \(f_x=0\) уже сохраняется во ВСЕХ ячейках из его native null-bivector контрольного продолжения.

Теперь разрешим одну из реальных положительных prep-мод source §6.5:
\[
\mu_{n,x}^{(\chi)}=\chi_x\mu_{n,x},\quad
v_{n,x}^{(\chi)}=\chi_x^{-1/2}v_{n,x},
\]
с сохранённым полным complement mass и \(\chi=1\) на collar. На её **собственных** exact finite stationary roots (для five-cut/free preparation ветви) имеем
\[
\boxed{
\widehat g_n^{(\chi)}
 =\frac{\mu_{n,x}^{(\chi)}}{\bar\mu}
     g(v_{n,x}^{(\chi)})
 =\widehat g_n
 \xrightarrow[C^2]{}g_{\rm pp}.
}\tag{17}
\]

Это сильнее прежнего утверждения «существует хотя бы одна подходящая pp-wave подготовка»: **целая непрерывная \(\chi\)-семья точно стационарных неравномерных подготовок даёт ОДНО И ТО ЖЕ вакуумное решение Эйнштейна для единственного source-compatible операционного метрического чтения (9)**. Её raw \(g(v_\chi)\) может иметь \(G_{\mu\nu}\ne0\), как в конечном примере с \(\chi=e^{2ku}\); но \(\widehat g\) точно invariant и Ricci-flat в пределе. Это не новый физический скалярный stress: в ведущем geometric sector изменение \(\chi\) — изменение представления одной связанной density/coframe переменной, с настоящей старой подготовкой сохранённой отдельно.

**Граница:** full D0 может иметь отличающие \(\chi\) аппаратные/matter/clock наблюдаемые; (17) не делает их gauge всего D0. Для материи с независимо выведенной source law надо проверить, что истинные CAR/Dirac propagation/metric readout сцеплены с нормировкой (9), а не с raw \(g(v)\). Ваккумный Einstein sector composite-gravity этим замкнут на неплоской local recovery family, а физическая универсальность — конкретный следующий потребитель.

## 5. Следующее положительное сцепление в том же PR

Вместо новых curvature readouts или arbitrary Einstein actions нужно взять **уже принадлежащую полную native operator-to-geometry реконструкцию** (§8.4–8.5) и вывести, что действительный допустимый общий AF/Julia эксперимент считывает в одном cut имеют данные \((X_{x,r},\mu_x)\) при совместно стационарной подготовке. Тогда (9) не является свободной метрикой: это единственное source-compatible homogeneous normalized CAR чтение, все10 ADM variations и principal Clifford symbol следуют автоматически из (1)–(10). Остаются реальная execution/price и independently derived spin/matter sources, а оригинальная all-site raw \(h^{-2}\) #216 оценка не подменяется этим finite smooth-C² утверждением.

**Статус:** PROVED FINITE GEOMETRIC SOURCE/CAR16 COMPENSATION ON DECLARED CARRIER; EXISTING FULL40 NONFLAT RECOVERY CONSUMED. Not a claim of the literal unchanged v8 physical programme or a complete D0⇒GR theorem. No new physics parameter, no BOOK/Claim promotion, no new PR or task.
