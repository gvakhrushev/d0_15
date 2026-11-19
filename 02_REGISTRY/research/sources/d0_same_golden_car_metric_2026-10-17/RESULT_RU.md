# D0 → полная ОТО: один золотой CAR-носитель для метрики, всех кривизн и наблюдателя

**17 октября 2026 · `gvakhrushev/d0_15` · источник к существующему Draft #334.**

**Класс результата:** `RESEARCH / EXACT LOCAL TWO-JET GEOMETRIC REALIZATION + TYPED OBSERVER SOURCE`. Это **не** `CORE`, не доказанная физическая вынужденность действия, не exact joint-critical solution и не завершение нелинейного refinement. Исходные `H+J+R`, все 16 CAR-компонент, обе золотые ветви, reference128 и строгая конвенция десяти метрических компонент не изменяются.

## 0. Что удалось сцепить, идя назад от ОТО

В прошлой обратной сборке `sources/d0_reverse_einstein_ir_2026-10-17/RESULT_RU.md` была получена точная комбинация четырёхмерного и трёхмерного геометрических Golden-детекторов. Однако **метрика проекторной записи** могла отличаться от **положительной метрики настоящего coframe/observer**, а пространственная часть выглядела как отдельный прибор. Оба вопроса теперь имеют конструктивный алгебраический ответ *на уровне локального метрического 2-jet и геометрического scalar source*:

1. В **первоначальном 16-мерном CAR-пространстве**, с той же двухпортовой золотой изометрией `sqrt(p),p`, задаётся проекторная запись, чей induced metric **в точности** равен `G=e^T h_n e` в любой одной точке, включая все десять независимых первых метрических вариаций и движущегося timelike observer.
2. Десять явных **квадратичных Majorana-поворотов на тех же 16 состояниях** позволяют подобрать все 20 компонент произвольного *алгебраического* Riemann-тензора этого record metric в одной точке, с локально гладкой зависимостью от заданного метрического 2-jet. Доказательство использует правый обратный оператор к Gauss map и положительный элемент её ядра, а не перебор кривизн.
3. Уже доказанное [полное Lorentz reflection](../../A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md), Eq. (5), позволяет **отказаться от отдельного 3D эксперимента вообще**. Для *любого* G-единичного наблюдателя, в том числе с ненулевым twist, Лоренцева кривизна есть отрицательная четырёхмерная positive-record кривизна плюс одна квадратичная форма **всех девяти** компонент производной наблюдателя и точная дивергенция.
4. Эта девятимерная квадратичная форма вычисляется **не новым оператором**, а trace-парой и квадратом `sum C_ij gamma_i hatgamma_j` в том же full16 CAR. Четырёхмерный R_G вычисляется ранее построенным конечным четырёхбуквенным golden Jacobian readout с точным устранением quartic по масштабам `s,2s`.

**Важная граница:** это ещё не одна *физически выбранная программа*. Синтез конструктивно закрывает **локальную algebraic representation/variation-image** проблему. Для целой динамики требуется один global/native history-to-record/coframe map, физически допущенные gates и истинная `Cost−Info` стоимость этого readout вместе с материей, часы и exact refinement. Ни один из этих входов не отождествляется со свободным выбором внешнего прибора.

## 1. Ровно старые CAR и Golden два порта: метрическая изометрия

Пусть `H=Lambda^* R^4`, `dim H=16`; `c_a` и `i_a=c_a^T` — первоначальные creation/annihilation, `gamma_a=c_a-i_a` и `hatgamma_a=c_a+i_a`. Тогда на **всех 16 grades**:

\[
\{\gamma_a,\gamma_b\}=-2\delta_{ab}I_{16},\quad
\{\widehat\gamma_a,\widehat\gamma_b\}=2\delta_{ab}I_{16},\quad
\{\gamma_a,\widehat\gamma_b\}=0,\quad
\operatorname{Tr}_{16}(\gamma_a^T\gamma_b)=16\delta_{ab}.\tag{1}
\]

Пусть `p=(sqrt(5)-1)/2`, `p+p²=1`. Для **одного и того же полного** `U(y)∈SO(16)` используем уже существующую Golden изометрию

\[
J_U=\begin{pmatrix}\sqrt p\,I_{16}\\p\,U\end{pmatrix},
\quad P_U=J_UJ_U^T,
\quad J_U^TJ_U=I_{16},\tag{2}
\]

то есть два порта имеют **ровно** исходные вероятности `p,p²`. `P_U` — ортогональный проектор ранга16 в существующей 2-port×16 реализации; нет нового Fock носителя. Устоявшаяся нормировка record metric из `A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md`:

\[
q_{\mu\nu}=\frac1{2\cdot16}\operatorname{Tr}_{32}[(\partial_\mu P_U)(\partial_\nu P_U)]
=\frac{p^3}{16}\operatorname{Tr}_{16}[(\partial_\mu U)^T(\partial_\nu U)].\tag{3}
\]

Действительный Lorentz coframe `e`, timelike n с `n^T eta n=1`, `eta=diag(+---)` задают **уже native** observer-positive metric

\[
h_n=-\eta+2(\eta n)(\eta n)^T,
\quad G=e^T h_n e.
\]

Возьмём любую действительную Gram-факторизацию `L^T L=h_n`, положительные coframe columns `v_\mu=L e_\mu`. В координатном центре `y=0` положим

\[
 U(y)=\exp K(y),\qquad U(0)=I,
 \quad \partial_\mu K(0)=p^{-3/2}\gamma(v_\mu).
\tag{4}
\]

Подстановка полного Clifford trace в (3) даёт без аппроксимации:

\[
\boxed{q_{\mu\nu}(0)=v_\mu\cdot v_\nu=G_{\mu\nu}(x).}\tag{5}
\]

Это равенство **одной и той же положительной метрики**, не попытка приравнять её к лоренцеву g или старой 4D positive metric произвольного projector fixture. Для любой coframe-скорости `delta e` и moving n равенство (5) можно дифференцировать: в нём сохранены производные `L(n)`, обеих ветвей Golden и полная референция. При фиксированном n отображение coframe→10 symmetric q slots сюръективно: для произвольной симметричной `delta G`

\[
\boxed{\delta e=\tfrac12 e G^{-1}\delta G}
\quad\Longrightarrow\quad
\delta(e^Th_ne)=\delta G.\tag{6}
\]

Доказательство действует на всех десяти базисных symmetric slots, не только диагонали/trace. Native spatial/own-leg admissibility старого `stored-adjoint` может ограничивать эти скорости; (6) относится к полной **алгебраической coframe chart**, а не автоматически к старому constrained Euler image. Включение reference128 как spectator `J_U ⊗ I_128` умножает числитель и `m=16·128` на одно и то же 128; ни одна физическая колонка этим не удаляется.

## 2. Все 20 компонент тензора Римана из десяти quadratic Majoranas: явная теорема

В G-нормальной ортонормированной рамке в центре `G(0)=I`, `dG(0)=0`. Обозначим `s=p³`, `κ=s^{-1}=2+sqrt(5)` и

\[
T_\mu=s^{-1/2}\gamma_\mu,
\quad\quad
Z_\alpha\in\left\{s^{-1/2}\gamma_i\gamma_j\ (i<j)\right\}_{6}
\cup\left\{s^{-1/2}\widehat\gamma_0\widehat\gamma_1,
 s^{-1/2}\widehat\gamma_0\widehat\gamma_2,
 s^{-1/2}\widehat\gamma_0\widehat\gamma_3,
 s^{-1/2}\widehat\gamma_1\widehat\gamma_2\right\}_{4}.\tag{7}
\]

Все эти десять `Z_α` — **вещественные кососимметричные квадратичные CAR-матрицы на H16**, не свободные `so(16)` directions и не новый carrier. Они удовлетворяют

\[
\frac s{16}\operatorname{Tr}(Z_\alpha^T Z_\beta)=\delta_{\alpha\beta},
\qquad \operatorname{Tr}(Z_\alpha^T T_\mu)=0.\tag{8}
\]

Выберем симметричные 2jet-коэффициенты `B_{mu nu}^α=B_{nu mu}^α` и определим **математическую** локальную Golden программу:

\[
K(y)=y^\mu T_\mu+\frac12 y^\mu y^\nu\sum_{\alpha=1}^{10}B_{\mu\nu}^\alpha Z_\alpha,\quad U(y)=\exp K(y),\quad P(y)=P_{U(y)}.\tag{9}
\]

Настоящая вторая производная унитарного оператора равна

\[
U_{,\mu\nu}(0)=-\kappa\delta_{\mu\nu}I_{16}+\sum_\alpha B_{\mu\nu}^\alpha Z_\alpha.\tag{10}
\]

Первая метрика `q=I` и **все 40** первые metric-jet slots `dq=0`; во втором jet полная normal form `P_{,\mu\nu}` имеет две взаимно ортогональные части — Clifford baseline и ten quadratic normal deformations. Со скалярным произведением `Tr_32/(2·16)`:

\[
\langle \mathcal B_{\mu\nu},\mathcal B_{\rho\sigma}\rangle
=\kappa\delta_{\mu\nu}\delta_{\rho\sigma}
+\sum_{\alpha}B_{\mu\nu}^\alpha B_{\rho\sigma}^\alpha.\tag{11}
\]

Gauss identity для проекторной иммерсии в плоском пространстве самосопряжённых матриц даёт

\[
\boxed{R(q)_{ijkl}=\kappa(\delta_{ik}\delta_{jl}-\delta_{il}\delta_{jk})
+\sum_{\alpha=1}^{10}
 (B_{ik}^\alpha B_{jl}^\alpha-B_{il}^\alpha B_{jk}^\alpha).}\tag{12}
\]

### 2.1 Не поиск B, а явный общий правый обратный Gauss map

Пусть `R*` — **ЛЮБОЙ** алгебраический Riemann-тензор на 4D Euclidean inner product (20 независимых значений; все перестановочные симметрии и первая Bianchi выполнены). Вычтем известный CAR baseline: `T=R*−κ(δ_ikδ_jl−δ_ilδ_jk)`. На десятимерном `Sym²(R4)` с неупорядоченными парами `ij` зададим симметричный Gram candidate

\[
\boxed{M_{(ij),(kl)}=\frac{T_{ikjl}+T_{iljk}}3.}\tag{13}
\]

Bianchi даёт **всю** 256-элементную компонентную тождественность

\[
\boxed{M_{(ik),(jl)}-M_{(il),(jk)}=T_{ijkl}.}\tag{14}
\]

Но `M` может быть неопределённым. Исправляем **только представление**, не искомую кривизну. Возьмём десять вещественных rank-one symmetric forms `f_a=v_av_a^T`, где `v_a=e_i` (4 штуки) и `v_a=e_i+e_j` (6 штук). Их упорядоченные symmetric-vectorization столбцы составляют целочисленную обратимую `10×10` матрицу `V` с `|det V|=1`. Положим

\[
H=VV^T>0,
\qquad H_{ik,jl}-H_{il,jk}=0\quad\text{для всех }i,j,k,l.\tag{15}
\]

Второе равенство следует из `f_a=v_a⊗v_a` — у каждого **нулевая** гауссова квадратичная кривизна. При любом достаточно большом `τ>0` матрица

\[
\mathsf G=M+\tau H>0,\quad
\tau>\|M\|_{op}/\lambda_{min}(H).\tag{16}
\]

Гауссово чтение (14) неизменно. Взяв обычный вещественный квадратный корень или Cholesky `mathsf G=BB^T`, получаем **ровно десять** векторов shapes `B_ij^α` и (12) становится `R(q)(0)=R*` **для всех 20 независимых компонент одновременно**. `τ` здесь не физический coupling: он измеряет только невидимую intrinsic curvature свободу внешнего вложения и может быть выбран детерминированно из ранее заданного R*. На компактной bounded области один фиксированный `τ` с запасом работает для всей ближайшей гладкой семьи, а разложение `G^{1/2}` гладко; поэтому **все первые производные этого равенства по любому заданному R*(t)** тоже точны.

Проверочный общий rational+quadratic fixture имеет строгую оценку `G≥(3599/14553)I` без вычисления приблизительных собственных чисел, и 256 точных component checks для значения и ещё 256 для произвольной определённой curvature source velocity. Никакого 20-параметрического поиска решений не требуется.

**Строгий смысл:** доказана *точечная локальная surjectivity* всех metric-2jets **с точностью до локальной координатной нормализации**. Это не доказывает, что независимо выбранные в каждой точке projector jets интегрируются в **один гладкий глобальный U(x)**. Для этого нужны Gauss–Codazzi–Ricci/holonomic identities вместе с реальной physical coframe→record map. Утверждать глобальный Einstein action только на основании (12)–(16) было бы ошибкой.

### 2.2. Не требуется внешний экспоненциальный оракул: точный рациональный CAR-компилятор того же 2-jet

Предыдущий локальный construction записывал `U(y)=exp K(y)`. Для **всех**
исходных real-skew CAR operators `K(y)` той же области можно заменить его на
точную рациональную ортогональную карту

\[
  \boxed{U_{\rm Cayley}(y)=(I-K(y)/2)^{-1}(I+K(y)/2)\in SO(16).}\tag{16a}
\]

`I-K/2` обратим на всей вещественной кососимметрической области:
`||(I-K/2)v||²=||v||²+||Kv||²/4`. При `K(0)=0` дифференцирование равенства
`(I-K/2)U=I+K/2` даёт **без коммутативности полевых джетов**

\[
 U_{,\mu}(0)=K_{,\mu}(0),\qquad
 U_{,\mu\nu}(0)=K_{,\mu\nu}(0)
      +\tfrac12(K_{,\mu}K_{,\nu}+K_{,\nu}K_{,\mu})(0).\tag{16b}
\]

Это ровно первые два джета `exp K`. Поэтому **тот же** `Gauss map`/правый
обратный для всех 20 компонент Римана и всех первых metric/source jets
реализуется без матричной экспоненты, eigenbasis oracle или дополнительного
Fock-пространства. Реализуемость рационального `inverse/response` из
физически допущенных *native* gates, цена этого контроля и source при
движении preparation/controller **не следуют** из алгебраической формулы.
Проверка `check_same_car_twojet.py` предъявляет exact SO16 Cayley для
некоммутирующего Clifford-входа и два настоящих некоммутирующих вторых
джета; это не проверка новой аппаратной реализации.

## 3. Ещё более короткая обратная формула: без отдельного 3D прибора и без twist-free

Для actual `g=e^Tηe` и `G=e^Th_ne` положим `u=e^{-1}n` (`G(u,u)=1`), `ω=G(u,·)`. **Точно** `g=2ω⊗ω−G`, обе плотности объёма совпадают.

Для любого такого наблюдателя (ни zero shift, ни Frobenius integrability не требуются) определим в G-ортонормированной пространственной рамке

\[
C_{ij}=G(\nabla^{G}_{e_i}u,e_j),\quad i,j=1,2,3,
\quad \theta=\operatorname{tr}C,\quad
C=K+\Omega,\ K^T=K,\ \Omega^T=-\Omega.\tag{17}
\]

Уже опубликованное исходное геометрическое тождество
[`A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`, Eq.(5)](../../A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md)
после отделения полного дивергентного члена принимает вид

\[
\boxed{
R(g)=-R(G)+2\big[(\operatorname{tr}C)^2-\operatorname{tr}(C^T C)\big]
             -4\operatorname{div}_G(\theta u).}\tag{18}
\]

Это **не только hypersurface-orthogonal ADM**; антисимметрическая `Ω` сохраняется и входит с верным отрицательным знаком `−2|Ω|²` в источнике. Переход к пространственной `R3` при `Ω≠0` вообще нельзя проводить как к интегрируемому leaf, и новая формула его не делает.

Теперь введём девять **явных, уже CAR-определённых** симметричных матриц

\[
\mathsf O_{ij}=\gamma_i\widehat\gamma_j\quad (1\le i,j\le3),
\quad \mathsf O(C)=\sum_{ij} C_{ij}\mathsf O_{ij},
\quad \mathsf O(I)=\sum_i \mathsf O_{ii}.\tag{19}
\]

На full16 CAR эти девять bilinears удовлетворяют

\[
\frac1{16}\operatorname{Tr}_{16}(\mathsf O_{ij}\mathsf O_{kl})=\delta_{ik}\delta_{jl}.
\]

Отсюда **вне любых уравнений движения**

\[
\boxed{
\mathcal Q_{\rm obs}(C)=
\left[\frac{\operatorname{Tr}_{16}(\mathsf O(C)\mathsf O(I))}{16}\right]^2
-\frac{\operatorname{Tr}_{16}(\mathsf O(C)^2)}{16}
=(\operatorname{tr}C)^2-\operatorname{tr}(C^TC).}\tag{20}
\]

Это не новый state carrier, trace, `Hilbert adjoint` или свободный source — просто quadratic CAR readout всех **девяти** `C_ij` включая twist. Его подлинный полный first source при moving `C`:

\[
\boxed{d\mathcal Q_{obs}=2\theta\operatorname{tr}(dC)-2\operatorname{tr}(C^TdC).}\tag{21}
\]

Движение `e,n,h_n` входит в `dC` через истинную Levi–Civita derivative и projector/frame transport, а изменение объёма не заморожено. Проверка на несимметричном `C` отвергает замену `tr(C^TC)` на `tr(C²)` — такая подмена даёт **неверный twist-source**.

### 3.1. Канонический пространственный split из конечной симметрии D0, а не дополнительный источник

Есть ещё один обратный шаг к физической интерпретации (20). Действительный трёхмерный spatial Role sector уже выделен в принятом
`03_FORMALIZATION/D0/Geometry/ArchiveSpatialHistorySplit.lean`.
Рассмотрим **математически** 24 ориентационно-сохраняющих signed permutations этих трёх осей и их буквальный exterior lift `rho(R)` на том же `Lambda^* R^4` размера16. Каждый `rho(R)` ортогонален и переносит одновременно
`gamma_i -> sum_j R_ji gamma_j`, `hatgamma_i -> sum_j R_ji hatgamma_j`.

Единственная естественная Reynolds-карта на квадратичном observer-блоке имеет вид

\[
\Pi_{\rm iso}(X)=\frac1{24}\sum_{R}\rho(R)X\rho(R)^T.
\]

Точное равенство проверено **на всех девяти матричных единицах** пространственного тензора и на исходном full16 CAR:

\[
\boxed{\Pi_{\rm iso}\mathsf O(C)
=\mathsf O\!\left(\frac{\operatorname{tr}C}{3}I_3\right).}\tag{20a}
\]

Следовательно пространственная trace-компонента и весь anisotropic/twist complement выделены **проекцией, определённой только пространственными ролями**:

\[
\boxed{\mathcal Q_{\rm obs}(C)
=2\|\Pi_{\rm iso}\mathsf O(C)\|_{16}^2
 -\|(I-\Pi_{\rm iso})\mathsf O(C)\|_{16}^2,\quad
\|X\|_{16}^2=\operatorname{Tr}_{16}(X^2)/16.}\tag{20b}
\]

Доказательство: `||Pi O||²=(tr C)²/3`, а ортогональность Reynolds
обеспечивает `||O||²=||Pi O||²+||(I-Pi)O||²`. Подставляя,
`2||Pi O||²-||complement||²=3||Pi O||²-||O||²=(tr C)²-||C||²`.

**Нетривиальное следствие:** интегральный observer source уже допускает описание как **относительный, знаковый баланс invariant-archive** на той же конечной CAR-записи. Это математически канонизирует *само разбиение* и показывает, что не требуется новый девятимерный материал для source. Но сам signed price `+2/-1` не становится физически выбранным автоматически: коэффициенты фиксируются Lorentz reflection, а не одной лишь симметрией или единичной золотой ценой. 24 групповых элемента не объявлены 24 физически исполнимыми контроллерами; равномерный Reynolds trace — алгебраическое среднее, не доказанная модель реально оплаченного раунда. В частности, его нельзя без доказательства отождествить с нативной `Cost−Info`.

`check_spatial_role_twirl.py` буквально строит каждое из 24 exterior matrix lifts,
проверяет сохранение исходных CAR generators, полный `9x9` Reynolds,
ненулевой twist, настоящую производную moving C и ковариантность полного источника при совместной смене frame.

### 3.2. Сильный нелинейный curved witness: плоский positive record, но полный Einstein-тензор из CAR observer

Возьмём обычную положительную **совершенно плоскую** метрику `G=dt²+dx²+dy²+dz²` и `G`-единичного наблюдателя, реально изменяющегося с x:

\[
u=(\cos kx,0,\sin kx,0),\qquad
u^\flat\wedge d u^\flat=k\,dt\wedge dx\wedge dy\ne0\quad(k\ne0).
\]

Следовательно ни zero twist, ни фолиация \(u^\perp\) не разрешены; путь через отдельные пространственные листья здесь непригоден. Однако непосредственный 4D вычислитель Christoffel/Ricci **для полной нелинейной** метрики `g=2u^flat⊗u^flat−G` даёт точно

\[
\boxed{\operatorname{Ric}(g)_{xx}=2k^2,\quad
\operatorname{Ric}(g)_{\mu\nu}=0\ (\mu\nu\ne xx),\quad
R(g)=-2k^2,}
\]
\[
\boxed{G_{\mu\nu}(g)=k^2g_{\mu\nu}+2k^2(dx)_\mu(dx)_\nu\ne0.}\tag{21a}
\]

В G-подвижной ортонормированной пространственной рамке `e_x=∂x`, `e_y=−sin(kx)∂t+cos(kx)∂y`, `e_z=∂z` единственная ненулевая компонента \(C\) из (17) есть \(C_{xy}=k\); \(\theta=0\), \(\mathcal Q_{obs}=-k^2\). Поэтому **та же** quadratic CAR trace (20) даёт

\[
\boxed{-R(G)+2\mathcal Q_{obs}=-2k^2=R(g),\quad
\partial_k(-R_G+2Q_{obs})=-4k=\partial_kR(g).}\tag{21b}
\]

Здесь нет граничного divergence, поскольку \(\theta=0\). Это прямой nonperturbative контроль **всех Ricci и Einstein компонент** и реального вариационного источника; он не использует заранее подставленный классический Einstein equation. Положительный Hodge heat curvature здесь невидим, но observer CAR readout восстанавливает ровно потерянную лоренцеву кривизну. Ранее рассмотренное `4D−2×3D` чтение само по себе не могло пройти этот twist-fixture.

**Ограничение:** метрика (21a) является геометрическим свидетелем с ненулевым Einstein source, **не** решением исходного native стационарного действия без дополнительно полученного источника материи. Сам факт его вычисления не выбирает физическую стоимость (20).

`check_twisting_cone_witness.py` независимо собирает полную 4D LC-связь из `g`, Ricci, scalar и tensor Einstein; его exact normal/optimized checks отвергают случайно нулевой observer либо twist-подмену.

### 3.3. Глобально интегрируемая flat-G/curved-Lorentz ветвь с одним и тем же U на первоначальных CAR (новый результат)

Предыдущая теорема §2 воспроизводит заданный геометрический 2-jet в **одной**
точке; это не глобальное theorem. Для конкретного неплоского Lorentz семейства
есть более сильная **полностью глобальная** реализация без дополнительных
`SO(16)` степеней свободы. Возьмём четыре CAR quadratic generators

\[
 J_0=\gamma_0\gamma_1,\quad J_1=\gamma_2\gamma_3,\quad
 J_2=\hat\gamma_0\hat\gamma_1,\quad J_3=\hat\gamma_2\hat\gamma_3.
\]

Все четыре вещественно кососимметричны, `J_mu²=-I`, **попарно коммутируют**,
`Tr16(J_mu^T J_nu)=16 delta_mu nu`. Поэтому единая гладкая запись

\[
 U(x)=\prod_{\mu=0}^3 e^{x^\mu J_\mu}\in SO(16),\quad
 U(x+2\pi e_\mu)=U(x),\quad
 q_{\mu\nu}(x)=\frac{p^3}{16}\operatorname{Tr}(J_\mu^T J_\nu)
      =p^3\delta_{\mu\nu}\quad \forall x                                  \tag{24b}
\]

имеет **глобальную**, не jet-only, метрику `q=p³ I` на
`R × T³` (сама 16-компонентная запись периодична также по real time,
но физический timelike coordinate не компактифицируется). Оба золотых
порта фиксированы одним `p+p²=1` и никакой extra CAR carrier нет.

Пусть `s²=p³`, `theta(x)=A sin(x¹)` — периодическое наблюдательное
вращение в Euclidean `0,2`-плоскости, `n=e0`, а coframe
`e(x)=s R_02(theta(x))`. Тогда по всему пространству

\[
 G=e^Te=s²I=q,\quad
 g=e^T\eta e,
 \quad u=s^{-1}(\cos\theta,0,\sin\theta,0),
 \quad R(G)=0,\quad
 \boxed{R(g)=-2s^{-2}A^2\cos^2 x^1}.                     \tag{24c}
\]

Сигнатура лоренцева, `g` гладкая и глобально определённая; observer twist
ненулевой при `A cos x¹ !=0`. В G-ортонормированном пространственном frame
одна компонента `C` равна `A cos x¹/s`, θ_expansion=0,
`Qobs=-(A cos x¹/s)²`. Таким образом формула (23) даёт **всю** Lorentz
scalar со всеми moving observer terms, в отличие от pure positive-record
heat. По пространственному 3-тору периода `2π` и конечному временному
окну `T` получаем

\[
 \int_{[0,T]\times T^3}\!R(g)dV_G
    =-8\pi^3 T\,p^3 A^2,\quad
 \boxed{\left.\partial_A^2 \int R(g)dV_G\right|_{A=0}
           =-16\pi^3T\,p^3\ne0}.                         \tag{24d}
\]

Это **более сильный, чем точечный** метрический контроль: одна и та же
периодическая GOLDEN CAR-запись `U(x)` сохраняет `q=G` при всех `x,A`, тогда
как лоренцево действие имеет ненулевое второе полевое изменение. Он не
объявляет `A` физически выбранной native amplitude или эту coframe
совместным stationarity root. Сама математическая запись `U` здесь задана
из исходных CAR operators, но её допуск, источники аппаратной стоимости,
действительный global functor `e(x) -> U(x)` и физический выбор
signed observer-CAR price по-прежнему **открыты**. Поскольку равенство
`q=G` доказано только для данной глобальной ветви, оно не заменяет
общего global isometric embedding theorem на произвольном кривом фоне.

`check_global_flat_record.py` проверяет полный 16×16 CAR на 4 generators,
все коммутаторы, exact global Golden Gram, независимый Ricci scalar
при **произвольной** гладкой `theta(x¹)`, затем непрерывное periodic
`theta=A sin x¹` и полный ненулевой Einstein–Hilbert second variation.
Проверка не постулирует внешний физический action.

## 4. Одно точное Golden+CAR reading полного Lorentz scalar

Четыре исходных двубуквенных Golden-исхода `FF,FR,RF,RR` сохраняются с весами `(p²,p³,p³,p⁴)` и знаком `ε=(0,+1,−1,0)`. Для *той же* rank16 projector immersion P и полного normal Parseval-family (как в `A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md`) обозначим матричные determinant ожидания `M_4(t)`. Тогда

\[
M_4(t)=D_4+p^3t^2R(G)+2p^3t^4Q_4,
\]

где `Q4` — настоящая quartic density той же записи. Ровно один двухмасштабный контраст стирает её **алгебраически**, не в пределе:

\[
\boxed{\mathcal R_{gold}(G;t)=
\frac{16[M_4(t)-D_4]-[M_4(2t)-D_4]}{12p^3t^2}=R(G).}\tag{22}
\]

Значит из (18)–(22) появляется **единое условное геометрическое чтение, на одном полном 16-CAR+Golden carrier**:

\[
\boxed{\begin{aligned}
\mathcal C_{Ein}(x;t)=&-\mathcal R_{gold}(G;t)\\
&+2\left[\left(\frac{\operatorname{Tr}(\mathsf O(C)\mathsf O(I))}{16}\right)^2
-\frac{\operatorname{Tr}(\mathsf O(C)^2)}{16}\right]\\
=&\;R(g)+4\operatorname{div}_G(\theta u).
\end{aligned}}\tag{23}
\]

Для замкнутого 4D объёма или variations с корректной пространственно-временной границей

\[
\boxed{\int\mathcal C_{Ein}\,dV_G=\int R(g)\,dV_{|g|}}
\quad\text{mod }4\int_{\partial M}\theta G(u,n_\partial)d\Sigma.\tag{24}
\]

При гипотезе **ОДНОГО глобального допустимого isometric record map** `q_P=G` на всей допустимой coframe семье дифференцирование (24) даёт полный нелинейный Einstein Euler-ковектор по **всем 10** компонентам Lorentz metric, а не только scalar equality в стационарной точке. В отличие от прежней `4D−2×3D` конструкции, здесь не нужен второй 3D shape detector и не постулируется hypersurface orthogonality.

Однако точечная теорема (5)–(16) **не** доказывает эту глобальную гипотезу. И даже её доказательство не заставило бы исходную `Cost−Info` выбирать именно signed scalar (23). Этот выбор — конкретная физическая/operational задача, а не следствие алгебраического программирования желаемого результата.

### 4.1. Сцепка с уже существующей *одной* полной AF-программой — условное полное Einstein-уравнение

Применим не новый action, а уже установленную theorem-схему из
[`A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md`](../../A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md)
и её full pointer descent [`A4D_BACKWARD_EINSTEIN_SOURCE_COMPLETION.md`](../../A4D_BACKWARD_EINSTEIN_SOURCE_COMPLETION.md). Пусть **один и тот же** native прибор действительно реализует на общей допустимой семье (включая matter/preparation/observer)

\[
\mathcal Q(X)=\int\mathcal C_{Ein}(X)\,dV_G+\mathcal S_{m}(X),\quad
z(X)=p^2+\lambda\mathcal Q(X),\quad
\frac25<a(z,\sigma)<\frac52,
\]

со всеми controller/reference costs, а не получает \(\mathcal Q\) как внешний числовой oracle. Тогда уже доказанная точная полная chain rule для central `E=zI` даёт

\[
\boxed{d_X\mathcal A_{AF}=\lambda a(z,\sigma)\,d_X\mathcal Q.}\tag{24a}
\]

Здесь **один общий положительный множитель** относится к *геометрии и той же материи*: нельзя умножать только Einstein term и потом произвольно подставлять чужой \(T\). В любой полной stationary preparation, действительно достижимой из native-процесса, \(\lambda a>0\) означает эквивалентность **всех десяти** coframe/metric Euler-нулей `d_X A_AF=0 iff d_X Q=0`. При одной глобальной source-preserving isometric карте (а не просто локальных jet witnesses) тождество (24) переписывает их как полные нелинейные Einstein–matter equations с выбранным физически coefficient sign/convention. Дополнительные links/preparation equations надо решать одновременно.

Таким образом, **условный геометрический конец доказательства уже закончен алгебраически и без малости кривизны**. Недостающий шаг — вовсе не вывод формулы Эйнштейна: он состоит в **операционном** утверждении, что реальная native Cost−Info программа именно это \(\mathcal Q\) исполняет и оплачивает; плюс в её глобальном field/readout/source-refinement intertwiner. Программируемость \(E=zI\) не доказывает физическую вынужденность этой программы. Исходное v8 `H+J+R` нельзя тихо заменить \(\mathcal A_{AF}\): для такого перехода требуется отдельная same-native price/source theorem, с уже зарегистрированными fixed-β и history-normalization hostile controls.

## 5. Что теперь остаётся для настоящей ОТО, если идти строго назад

Оригинальная цель — не просто вычислить кривизну: она требует **вынужденно выбранного** полного `S_native` на одном native process, независимой материи, настоящих field/preparation/observer Euler equations и точных nonlinear joint roots с `h^-2` raw refinement. Представленный ход убирает математическую необходимость искать новый metric carrier, новый нормальный detector и ещё одно приближение к Einstein tensor. Следующее решающее утверждение теперь должно иметь вид:

\[
\boxed{
D S_{\rm native,h}(X)
=c_h D\!\sum_x w_{h,x}\,\mathcal C_{Ein,h}(X)
+D S_{\rm matter,h}(X)+r_h(X),
}\tag{25}
\]

где **все** terms справа — pullbacks **того же** native retained-history cost, а не определение `r_h` вычитанием по желаемому Einstein. В частности:

* От исходных native CAR/golden operations надо получить **единое admissible изменение** `U(x)` со всеми десятью quadratic Majorana 2jet components и с **совместным observer/metric/source intertwiner**. То, что они принадлежат матричной CAR алгебре, не означает, что реальная программа исполняет любые `exp(K)` бесплатно.
* Нужно вывести full cost выбора signed-contrast (23), включая обе Golden ветви, normal Parseval settings, истинный controller/decoder, reference128, память, `Info`, clock и moving нормировщики. Монотонное AF-вложение `A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md` сохраняет вариационные корни **уже заданного Q**; это не доказательство, что native физика выбирает именно наш Q.
* Для перехода от локальных 2jet-кодировок к одной реальной записи необходимо проверить **интегрируемость/holonomy/Gauss–Codazzi–Ricci** и covariance под moving local Lorentz/observer frame. Отдельные pointwise exact matches недостаточны.
* Должно быть обеспечено ненулевое gravitational coefficient, настоящий материальный source и nonlinear joint-critical refinement в исходной норме `h^-2 sum_x |ten rows|`, а не в более слабой averaged norm. Прежние fixed-beta v8 и normalised-pointer энтропийные отрицательные контроли при этом сохраняются.

**Названный потребитель:** `MORPH_NATIVE_COFRAME_TO_SAME_GOLDEN_CAR_2JET_AND_PRICE` в существующем #334. Следующий сильный proof — именно **один исходный аппарат и цена (25)**, а не новые топологические или Fourier-блоки и не публикация ещё одного условно красивого Лагранжиана. В частности, пока source owner не выбирает (23), ОТО остаётся **OPEN**.

## 6. Исполняемая проверка и scope

`check_same_car_twojet.py`, `check_spatial_role_twirl.py`, `check_twisting_cone_witness.py` и `check_global_flat_record.py`:

- на **всех16** CAR masks собирает исходные `c_a`, `i_a`, `gamma_a`, `hatgamma_a`, проверяет Clifford и `J_U` с исходным `p+p²=1`;
- проверяет сохранение Golden-weights и **всех10** coframe Gram/source slots с движущимся рациональным timelike observer и ненулевыми off-diagonal смешанными вариациями;
- конструирует именно **10** независимых quadratic-Majorana normal generators, все их Clifford/trace/source relations;
- проверяет общую **полную 256-компонентную** Gauss map right-inverse (14) и её 256 первых source-джетов для generic смешанного curvature fixture;
- предъявляет положительный Gauss-null Gram с `det=1`, явный bounded strict SPD margin, полное восстановление заданной кривизны и некоммутирующий quadratic нормальный контроль;
- проверяет **9** observer CAR bilinears, полный nonsymmetric `C`, правильный twist sign, moving observer derivative, одно Golden двухмасштабное устранение quartic и общий Lorentz-integrand source.

`python check_same_car_twojet.py` и `python -O check_same_car_twojet.py` дают одинаковый строго воспроизводимый JSON. Это доказательные проверки **алгебраических утверждений**, не компиляция Lean и не физическое admission/Cost−Info theorem. Старые Lean/root/CI suites для неизменённых владельцев здесь не повторялись.
