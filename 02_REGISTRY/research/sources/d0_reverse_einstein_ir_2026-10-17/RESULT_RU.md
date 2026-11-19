# D0 → ОТО: обратная сцепка из полного Эйнштейна в 16-grade native carrier

**17 октября 2026.** Репозиторий `gvakhrushev/d0_15`; текущий потребитель — существующий Draft PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Класс: **GEOMETRIC REVERSE THEOREM / FIXED-β IR CONDITIONAL SPECTRAL IDENTIFICATION / SINGLE NATIVE READOUT GATE**. Никакой новый физический action не устанавливается; BOOK, CLAIM, task, README, source receipts остаются неизменными. Входные владельцы: `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`, `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`, `A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md`, `A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md`, `A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md`, `A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md`, `ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`, `A4D_FULL_PRICE_CAUSAL_FORMFACTOR.md`, `A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md` §7. Контроль исходного терминала: фиксированная гладкая не-константная метрика, независимый источник, все10 raw response slots, `h^-2`-норма остаются OPEN.

## 0. Смена направления доказательства

Зададим конечное требование не как «угадай полную цену, потом угадай GR», а как **обратный синтез**:

    полный Einstein–Hilbert в Lorentz metric
    ← точная (не perturbative) 4D-positive minus 2×3D-spatial curvature identity
    ← full16 de-Rham/Hodge heat coefficients на одном и том же 8+8 CAR carrier
    ← leading IR term исходного H+J+R при ФИКСИРОВАННОМ beta
    ← тот же retained programme, ИЗ КОТОРОГО ещё надо вывести relative spatial price/Info

Первые три обратные стрелки ниже закрыты в указанных математических областях. Последняя — **одна точно сформулированная недоказанная физическая source-стрелка**. Это не утверждение, что весь физический GR вывод автоматически завершён, а строгая смена исследовательской цели.

## 1. Нелинейная формула для всех ADM полей: не только линейный symbol

Рассмотрим time-oriented/foliated Lorentz область, arbitrary lapse `N>0`, shift `s^i` и positive spatial metric `h_ij`, все гладкие:

\[
 g_L=N^2dt^2-h_{ij}(dx^i+s^i dt)(dx^j+s^j dt),\qquad
 G=N^2dt^2+h_{ij}(dx^i+s^i dt)(dx^j+s^j dt).
\tag{1}
\]

Обе метрики имеют одну плотность `N sqrt(det h)`. Их induced spatial geometry также одна и та же. При Ricci convention владельца Lorentz reflection, `\mathcal R_3` — positive spatial scalar, `\Delta_h f=\frac1{\sqrt h}\partial_i(\sqrt h h^{ij}\partial_jf)` и `K_ij=(\partial_t h_ij-\mathcal L_s h_ij)/(2N)`:

\[
 R_G=\mathcal R_3-\frac{2}{N}\Delta_hN
    -\frac{2}{N}(\partial_t-\mathcal L_s)K-K_{ij}K^{ij}-K^2,\tag{2}
\]
\[
 R_L=-\mathcal R_3+\frac{2}{N}\Delta_hN
    -\frac{2}{N}(\partial_t-\mathcal L_s)K-K_{ij}K^{ij}-K^2.\tag{3}
\]

Из этих **полных, а не линеаризованных** формул:

\[
\boxed{R_L=R_G-2\mathcal R_3+4N^{-1}\Delta_hN.}\tag{4}
\]

Доказательство можно дать в локальном shift-zero chart (пространственная времезависимая диффеоморфная перепараметризация) и перенести (4) ковариантно; обе стороны скаляры, привязанные к одной foliation. В 4D связь с `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md` — то же exact observer-reflection identity после разложения shear/expansion/twist. При замкнутых пространственных листьях или compactly supported пространственных вариациях последний член интегрально является **строго пространственной границей**:

\[
\int R_L N\sqrt h\,dtd^3x=
\int (R_G-2\mathcal R_3)N\sqrt h\,dtd^3x
 +4\int dt\int_{\partial\Sigma_t}\sqrt{\sigma}\,n^i\partial_iN.
\tag{5}
\]

Знак нормали в граничном интеграле следует из outward spatial convention. На closed \(\Sigma\) граница нулевая. Варьируя (5) **по всем десяти** полям `(N,s^1,s^2,s^3,h_ij)` с корректными граничными условиями, получаем полное Einstein Euler, а не только след или TT-класс. Обратимость 10-slot chart следует из

\[
 h_{ij}=-g_{ij},\quad s^i=-h^{ij}g_{0j},\quad N^2=g_{00}+h_{ij}s^is^j;\quad
 |\det D((N,s,h)\mapsto g_{\mu\nu})|=2N\det h>0.\tag{6}
\]

Этот Jacobian в проверочном `(N,h)=(4,diag(2,3,5))` равен по модулю `240`. Важно: сохранение всех `shift`-вариаций принципиально для momentum constraints. Нельзя получать GR по семи уравнениям с предварительно зафиксированным shift=0.

## 2. Неожиданная равенство коэффициентов на том же full16 CAR

Для стандартного Hodge–de Rham square `D^2=(d+d^†)^2` на **всех** \(2^d\) внешних степенях в dimension `d` local scalar heat coefficient (общий `(4πt)^(-d/2)` вынесен) имеет

\[
 \operatorname{Tr}E=-\sum_{k=0}^d\binom{d-2}{k-1}R=-2^{d-2}R,\quad
 a_2^{(d)}=(2^d/6-2^{d-2})R=-\frac{2^{d-2}}3R.\tag{7}
\]

Это непосредственно Weitzenböck trace, не подбор спектральной константы. Поэтому

\[
 a_2^{4D,16}=-\frac43 R_G,
 \qquad a_2^{3D,8}=-\frac23\mathcal R_3.
\]

**Ключевой шаг:** один timelike observer уже раскладывает прежние 16 наружных компонент по temporal occupation на `8+8`,

\[
\Lambda^*\mathbb R^4\cong\Lambda^*\mathbb R^3\oplus
\big(u^\flat\wedge\Lambda^*\mathbb R^3\big).
\]

У **двух** spatial copies, на том же размерностном бюджете `16`,

\[
 \boxed{a_2^{\Sigma,16}=2a_2^{3D,8}=-\frac43\mathcal R_3.}\tag{8}
\]

Для 3D коэффициента имеется в виду induced Hodge operator `d_Σ+d_Σ^†` на каждом пространственном листе, с его фактическим h-соединением; именно **две** копии по temporal occupation. Простое сжатие полного 4D Dirac без extrinsic/temporal correction **не объявляется этим оператором**. При вычислении пространственной heat density временная плотность/clock `N dt` сохраняется; 3D heat trace не выдаётся за 4D trace с неправильной степенью `t`.

Совмещая (4), (7), (8), на closed spatial leaves:

\[
\boxed{\int R_L dV_L=-\frac34\int\big(a_2^{4D,16}-2a_2^{\Sigma,16}\big)dV_G.}\tag{9}
\]

**Коэффициент `−2` единственен и не является fitted coupling.** На spatially-flat, time-dependent h с `R3=0` коэффициент перед `R_G` обязан совпасть с Einstein. На static product `N=1,shift=0,G=dt²+h` имеем `R_G=R3`, `R_L=−R3`, так что коэффициент spatial readout ровно `−2`. Любое другое число проваливает один из этих двух exact controls. Это обратная **полная нелинейная**, а не weak-field, геометрическая сцепка.

Отличие от произвольного «observer stress» велико: не надо угадывать десять source функций — требуется **одна пространственная относительная 8+8 запись** со строго заданным знаком и весом. Lorentz geometry/Einstein Euler уже следует из (9), когда этот relative source принадлежит тому же выбранному native programme.

## 3. Положительное движение от настоящей v8 цены без beta→0

Сохраняем ORIGINAL conditional price `S_v8=H+J_program+R`, на full16, M=128, z=2^-20 и fixed `β=2p²=3−sqrt(5)`; исключения `R_matter` здесь не делаем. Для полного positive Hodge Laplacian `Δ_{G_R}` на macroscopic metric `G_R=R²G` и той же proper LC связи,\(r=z/(1-z)<1\), поле-зависимый feedback (точно, ещё до асимптотики):

\[
 J_R=-M\operatorname{Tr}\log[(1-z)I+z e^{-\beta\Delta_{G_R}}]
 =-M\dim\mathcal H\log(1-z)-M\sum_{j\ge1}\frac{(-1)^{j+1}r^j}{j}\operatorname{Tr}e^{-j\beta\Delta_{G_R}}.\tag{10}
\]

Первый term при заданном конечном carrier строго независим от полей; при continuum trace его нужно вести через те же finite comparisons, а не объявить произвольным вычитаемым counterterm. При smooth compact geometry / source charts и standard uniform heat expansion, `Tr exp(−j β Δ_G/R²)` имеет локальные coefficients `a0=16Vol(G)`, `a2=−(4/3)∫R_G`, a4... . В результате **при β>0 неизменном** и `R→∞`:

\[
\boxed{J_R^{field}\;=\;-\lambda_J\operatorname{Vol}(G_R)
  +c_J\int R_{G_R}dV_{G_R}+O_{C^1}(1),}\tag{11}
\]
\[
\lambda_J=\frac{16M}{(4\pi\beta)^2}F_3(r),\quad
c_J=\frac{4M}{3(4\pi)^2\beta}F_2(r),\quad
F_s(r)=\sum_{j\ge1}\frac{(-1)^{j+1}r^j}{j^s}=-\operatorname{Li}_s(-r).\tag{12}
\]

`O_{C1}(1)` означает значение и smooth parameter first source (на фиксированной compact G chart) после умножения на macroscopic volume radius; это стандартный controlled heat-jet premise, не исходный `h^-2` normalized raw sum. При bounded source charts `a4` даёт O(1); более высокие локальные terms подавлены. Для r<1 обоснование суммирования: отделить `j≤C log R` и использовать равномерное малое время, а хвост оценить геометрически `r^j` с полным тепловым trace. Ни один free parameter или новое действие не введены.

Для исходных **неизменённых** v8 чисел:

    beta=0.7639320225002103...
    c_J = 0.00000134919480533112275... >0
    lambda_J = 0.00002119342967326504047... >0
    lambda_J/c_J = 12 F3(r)/(beta F2(r)) = 15.70820580506437...

Это coefficient ratio **в spectral units, не измеренная SI Λ**. Величина `lambda_J` — обязательный volume term этой спектральной price: его нельзя молча отбросить. На фиксированном объёме он не меняет variation; на полной family даёт кандидат космологического члена и требует сопоставления с реальными clock/archive/matter источниками. Любые реально движущиеся `β,z,M,C` добавляют их подлинные derivatives — здесь фиксирована именно прежняя v8 calibration.

Тепловое `H=β^-1 log(C Tr e^-βΔ)` даёт в этом режиме field-dependent `O(log R)` value и `O(1)` source (при volumetric variation), поэтому не отменяет `R²` curvature contribution `J`. Это не разрешение удалить H из полного finite action.

### Почему fixed-beta form-factor/no-go не мешает этой стрелке

Предыдущий `A4D_FULL_PRICE_CAUSAL_FORMFACTOR` доказывал nonrational response на фиксированной размерной форме при произвольных высоких Fourier q. Это **не** запрещает leading local `q sqrt(beta)/R→0` response. Здесь `R` — отношение пространственного macroscopic размера к fixed heat length, а не новая регулируемая beta.

На плоских тора́х фиксированной `det G` exact Poisson resummation даёт:

\[
\Theta_{\beta,R}(G)=\sum_{k\in\mathbb Z^4} e^{-4\pi^2\beta k^TGk/R^2}
=\frac{R^4}{(4\pi\beta)^2\sqrt{\det G}}
\sum_{n\in\mathbb Z^4}e^{-R^2 n^TG^{-1}n/(4\beta)}.\tag{13}
\]

На compact family fixed determinant все nonzero dual windings экспоненциально подавлены. То же верно для feedback trace-log, поскольку r<1; разделение циклов `j≤R` и `j>R` даёт `O(poly(R)e^{-cR})+O(poly(R)r^R)` для finite smooth shape derivatives (достаточно для `o(R^{-k})` любого k). В частности глобальный flat-modulus Hessian **может исчезнуть при макроскопическом R→∞ без beta→0**. Положительный fixed-beta at R=1 Hessian из прежнего источника остаётся верен, но не контролирует этот иной IR regime.

Это не обход owned scale-source obstruction `Mz β Z<1` через недоказанный running β: β не меняется. Физическая clock/volume карта R↔native h также не выведена. Однако аналитическая необходимость малого beta для LOCALITY этим опровергнута: достаточно малого отношения `sqrt(beta)/R`.

### Диагональная source-стыковка, без незаконного равномерного inverse

Существующий `A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT` доказывает fixed-positive-time trace и independent coframe/link/observer source convergence на контролируемых smooth charts. Для **каждого фиксированного** R разрешено выбрать finite mesh level `L(R)` достаточно большим, чтобы finite/continuum source error после разделения на R² была меньше, например, `R^-3`; выбор по возрастающей последовательности R — обычная диагональная теорема. Это доказывает существование **операторной** двухшкальной траектории при соблюдении её hypotheses, но НЕ M1 физическую clock-law, NONEMPTY joint solutions, all-grid original h^-2 terminal или uniform estimates на произвольные микроструктуры. Не подменять геометрический IR исходным фиксированным smooth-source экспериментом.

## 4. Конечная «причина, почему мы уже у Эйнштейна»: что именно требуется от Info

На torsion-free/natural-volume/LC positive coframe slice (11) уже даёт

\[
 S_{v8}^{leading}=-\lambda_J\operatorname{Vol}(G_R)+c_J\int R_{G_R}dV_{G_R}.
\]

Точная обратная формула (5) требует от **остальных реально выбранных** retained/observer/spatial источников не абстрактного Einstein counterterm, а строго один

\[
\boxed{D S_{\rm retained}^{(2)}[V]\;=\;-2c_J D\!\left[\int N\sqrt h\,\mathcal R_3\right][V]
\quad \text{for all ten ADM variations } V,}\tag{14}
\]

с учётом natural spatial boundary. После этого **точно**, не order-by-order nonlinear matching:

\[
 -\lambda_J\operatorname{Vol}(G_R)+c_J\int(R_G-2\mathcal R_3)dV_G
 =-\lambda_J\operatorname{Vol}(g_R)+c_J\int R(g_R)dV_{g_R}
 \quad (\mathrm{mod\ boundary}).\tag{15}
\]

При добавлении ДЕЙСТВИТЕЛЬНО выведенного native matter source полная вариация (15) даёт все10 Einstein equations, включая lapse constraint и shift momentum constraints. Не нужно заново строить бесконечную nonlinear Einstein jet tower; (5),(9),(15) точные на всей foliated chart. Метрическая Hessian имеет и настоящий Ward/Bianchi, если все остальные Euler ряды выполнены. Значения `c_J,lambda_J` определены старой price в данной conditional IR, без подбора.

### Где взять пространственную запись без расширения Hilbert carrier

У native full16 есть timelike observer и CAR operations, уже определяющие rank8 проекторы на формы без/с temporal occupation. Induced spatial Levi-Civita connection определяется из уже реконструированного полного coframe/ω через projection; из него однозначно получается `D_Σ=d_Σ+d_Σ†` на том же `8+8` пространстве. Задача **не** в существовании этих геометрических данных (они конструктивно определены), а в том, выбраны ли соответствующий relative-source observable и его стоимость настоящими admitted retained-history правилами. Нельзя бесплатно установить новый spatial trace как физический action.

Сильная гипотеза для последнего morphism: native `Cost−Info` оценивает *избыточную, а не суммарную* стоимость полного temporally conditioned record относительно двух spatial occupancy marginals. Для положительной двухблочной covariance `C` Gaussian identity

\[
I(A:B)=\frac12\log\frac{\det C_{00}\det C_{11}}{\det C}\tag{16}
\]

показывает, что inclusion–exclusion с двумя temporal blocks и коэффициентом 2 **не требует нового множителя**. Но (16) — только кандидат physical selection: actual full record НЕ доказан Gaussian covariance; его блоки не доказаны равными induced spatial heat kernel. Более того, на static-product геометрии full 4D operator может быть block diagonal, тогда обычный Gaussian inter-block mutual information равен0, хотя `\mathcal R_3` и correction (14) ненулевые. **Следовательно, простое объявление (16) готовым GR источником было бы неверно.** Нужна реальная spatial/temporal code-comparison операция с указанным heat source, включая собственный clock, normalization и future tests. Это один конкретный executable theorem, не переписывание будущего ответа как аксиомы.

## 5. Почему старые отрицательные controls не запрещают этот маршрут

1. **Fixed-beta flat shape positive Hessian.** Верен на fixed unit-period/homogeneous physical field family. (13) доказывает другое: IR large R при том же beta; глобальный Casimir-type shape potential исчезает. Это не автоматический вывод D0 physical large-R schedule.
2. **Full conditional price nonlocal form factor at q→∞.** Совместим с local IR: высокий q исследует UV, `R→∞` при fixed smooth shape исследует малое dimensionless q. Оба утверждения могут быть верны.
3. **Stored-adjoint rank5/Einstein invisible source.** ADM rank10 (6) принадлежит большему physical observer/coframe chart; actual native admission этих 10 source rows (P1/reference/readout) ещё должна быть доказана. Прежний counterexample к rank5 на нём не переводится в rank10 no-go.
4. **Physical Cost−Info не выбран.** Ни (9), ни (15) не назначает выбранную программу; (14) — доказательная цель, а не введённый residual `S−EH` в native цене. Нужен её actual source от старого retained процессa и цену выполнения этого reading.
5. **Matter, torsion, measure and joint roots.** Torsionfree/hypersurface-orthogonal/natural-volume здесь геометрическая область, не доказанный native on-shell sector. В реальном действии a2 также содержит `+2|h_T|²−4|v_T−b|²`; их собственные equations и source/coupling to matter не были удалены. Actual normalized R, reference128, clock/Info и preservation остаются. Нельзя считать один posteriori compatible Einstein metric физическим решением без full coupled stationarity/refinement.

## 6. Стратегический критерий завершения (назад от цели)

**Вместо ещё 100 промежуточных certificates проверить один native coefficient/source identity на собственном full16×reference128 процессе:**

> На одной admitted smooth two-scale family с действительным `Cost−Info` и истинными preparation/observer/link/measure equations, равен ли двухпроизводный пространственный relative-source в `8+8`-разложении `−2 c_J d∫N√h R3`, причем его raw Euler remainder контролируется в настоящем source norm?

Если ДА: (15) и ADM chart сразу переводят результат в FULL нелинейный Einstein-source (со всеми10 metric rows); материя/Λ включаются только как прежние реальные native terms; затем остаётся uniform nonempty joint refinement. Если НЕТ: точное расхождение даст одно конкретное primitive-to-price устройство, которое нельзя заменить именем «observer stress». Это структурно лучше, чем требовать поточечное равенство всех спектральных цен любому континуальному Einstein action на конечном масштабе.

Задача для того же integrator #334: состыковать `A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE`/actual P1/reference128, `A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE` и `A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER` с (14). Не запускать старые expensive root/census. Тот же full16 CAR, same 128 ref, same clock beta, same original price; не добавлять второй физический action, free spatial coupling, mass fit, arbitrary subtraction. В перспективе подключить normal-jet estimator `ATORUS_NORMAL_JET_EINSTEIN_BRIDGE` как независимый геометрический control, а не постулат поля.

## 7. Проверка

`check_reverse_ir.py` независимо строит Riemann/Ricci из metric jets на двух полных4D ADM fixtures с ненулевыми lapse, shift, spatial curvature и variable temporal h; проверяет все10 ADM directions, Hodge Weitzenbock trace identities, fixed-beta original v8 polylog coefficients, Poisson equality двух 4D thermal representations и падение global flat-shape response при growing R. Отрицательный scope: это **не** Lean proof физической primitive admission, не replay expensive root, не C² full native UV/stationary theorem. `python -O` и обычный Python дают один deterministic JSON с теми же source parameters; он поддерживает аналитический синтез, но не заменяет его.

## 8. Сильная обратная сцепка, найденная после сборки: пространственный носитель УЖЕ в accepted `main`

Это уже не предложение построить новый 3D носитель. В **принятом main** файл `03_FORMALIZATION/D0/Geometry/ArchiveSpatialHistorySplit.lean` (Git blob `e019851589ad7e750e183ff1098c24283a093d19`) формализует:

- `SpatialRole := {r : Role // r ≠ A}`, `spatialRole_card_three = 3`;
- `archiveRolePhase_timeSpatialEquiv`: точную факторизацию **циклической** Role-A-координаты и трёх spatial Role координат;
- `axisInvariantCochainEquivSpatial`: A-инвариантный подноситель с сохранением **всех 16 CAR grades**;
- `spatialCochainPullback_hodgeSquare` и `axisInvariant_hodgeSquare_equiv_spatialLaplacian`: буквальный интертвининг уже существующего квадрата Hodge-CAR на A-инвариантном секторе с **трёхмерным пространственным Laplacian**.

Следовательно, в исходном D0 уже физически *не* приходится выдумывать 3D граф/новую многокомпонентную Fock оболочку ради (8). Размерностная, flat finite-Hodge и spatial-cochain часть обратной стрелки имеет **принятых владельцев**. Но это **не** равенство curved spatial `a2=-4R3/3`, не полная 3D Levi–Civita на произвольном coframe, не выбор его физической цены и не автоматическое распараллеливание настоящего такта.

`HistoryIndex` в том же Lean-модуле сознательно берёт **отдельный** Feshbach history grammar. Старое направление "приравнять Role A-phase к настоящему времени" не разрешено: `A4D_CAUSAL_TIME_ROLE_INTERTWINER.md` уже показывает, что конечная циклическая трансляция не может быть сопряжена гиперболическому Pisot-flow. Нужны **same-axis/orientation bridge** и временная распаковка \(\mathbb R\times T^3\) — не новая непрерывная масса/константа. Для GR требуется настоящее поле lapse/shift и его source, а не имя `A`.

### Теперь точный минимальный native consumer

Вместо десятков новых независимых «первых шагов» нужно взять **вместе** четыре уже имеющихся входа:

1. `ArchiveSpatialHistorySplit.lean`: spatial 3D Hodge square / all16 readout в accepted main;
2. `A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md`: полный full16 curved positive Hodge +omega_LC с источником;
3. `A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md` плюс `A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md`: recover g from observer/coframe и true moving density/clock;
4. `A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md` вместе с `A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md`: фактическая native retained full-price/Info и его полный первый источник.

**Требование на одну композицию:** построить из **этих входов без новых полей** spatially restricted curved Hodge readout на A-инвариантной/observer-spatial карте и показать, что тот же actual `Cost−Info` выбирает её relative coefficient `−2` с правильным `Ndt` clock density, **включая все derivative jets**. Его lead two-derivative covector должен совпасть с (14), что затем даёт (15) и все10 Einstein equations без отдельного nonlinear symbol search. Если physical clock/restricted likelihood уже содержит подходящий conditioning, установить точную equivalence/Schur; если нет — фиксировать одну конкретную неподставляемую стрелку, не писать произвольный Einstein residual.

Это сужает настоящую открытую часть: 3D spatial support и плоский Hodge-square уже являются **принятым математическим input**, а не новой гипотезой. Переход от flat spatial readout к curved physical relative price остаётся источником, который надо получить; доказательство GR ещё не объявляется завершённым.

## 9. Более короткий обратный путь: конечный золотой 4D−2×3D Einstein readout БЕЗ heat asymptotic

Это отдельный, ещё более сильный математический consumer. Исходные `A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md`, `A4D_RECORD_NORMAL_VOLUME_SOURCE.md`, `A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md`, `A4D_GOLDEN_DETERMINANT_COMPILER.md` и `A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md` уже содержат конечную проекторную метрику, нормальную форму и золотой детерминантный компилятор. Ниже — их **новая** совместная пространственная специализация; физический выбор этого composed programme остаётся отдельно.

### 9.1 Один и тот же полный golden cylinder имеет очень разные 4D и 3D исходы

Примитивные двухбуквенные истории `FF, FR, RF, RR` имеют **исходные** веса `(p²,p³,p³,p⁴)` и signed character `epsilon=(0,+1,−1,0)`. Они дают `E epsilon=E epsilon³=0`, `E epsilon²=E epsilon⁴=2p³`. Ни один исход не отброшен.

Для гладкой positive four-dimensional record immersion \(P:M^4\to E\) с metric \(G=P^*\langle,\rangle\) и полным Parseval normal-family self-adjoint shape matrices \(A_j^{(4)}\) предыдущий owner доказал точный **полином степени четыре**:

\[
M_4(u)=D_4+p^3u^2R_G+2p^3u^4Q_4,\qquad Q_4=\sum_j\det A_j^{(4)}.\tag{17}
\]

Здесь D4 — фактическая сумма baseline установок, не заменённая числом1, и Q4 не объявлена topological. У него уже есть законная трёхмасштабная отмена quartic:

\[
\boxed{R_G=\frac{16[M_4(u)-D_4]-[M_4(2u)-D_4]}{12p^3u^2}.}\tag{18}
\]

Теперь **не вводя новую геометрию**, ограничим тот же P на пространственный срез \(\Sigma_t\); его induced metric h из (1) совпадает с spatial G. Normal space для **3D immersion** — ортогональное дополнение трёх spatial касательных в том же E, оно включает дополнительные нормали, которые могли быть касательными к полной 4D immersion. Их нельзя пропускать. Пусть \(A_j^{(3)}\) — настоящие трехмерные shape matrices, построенные из того же P и h. Gauss identity для их полного Parseval normal-family даёт

\[
\sum_j[(\operatorname{tr}A_j^{(3)})^2-\operatorname{tr}(A_j^{(3)2})]=\mathcal R_3.
\]

В 3D \(\det(I-u\epsilon A_j^{(3)})\) **только кубический**, поэтому симметрия FR/RF сразу устраняет все нечётные степени, а quartic **отсутствует тождественно**:

\[
\boxed{M_3(u)=D_3+p^3u^2\mathcal R_3,\qquad
\mathcal R_3=\frac{M_3(u)-D_3}{p^3u^2}.}\tag{19}
\]

Для **математической совместимости с уже построенным four-dimensional golden matrix compiler** достаточно вкладывать `A_j^(3) -> diag(0,A_j^(3))` в его исходный четырехмерный вход: \(\det_4(I-u\epsilon\operatorname{diag}(0,A_3))=\det_3(I-u\epsilon A_3)\). Это тот же размер4 вход, все golden returns/failures сохранены и никакой 3D determinant oracle не нужен. Но естественные 3D shape matrices и их управляемое изменение из действительного D0 engine требуют собственного допуска.

### 9.2 Точная конечная формула для integrated Lorentz Einstein–Hilbert

Объединяя (4),(18),(19), получаем **из конечных исходов того же golden-кода** функцию

\[
\boxed{\begin{aligned}
\mathcal C_{\rm GR}(x;u)=&\;
\frac{16[M_4(u)-D_4]-[M_4(2u)-D_4]}{12p^3u^2}\\
&-\frac{2[M_3(u)-D_3]}{p^3u^2}
=R_G(x)-2\mathcal R_3(x).
\end{aligned}}\tag{20}
\]

На closed spatial leaves **точно** (не только при `u→0`):

\[
\boxed{\int\mathcal C_{\rm GR}\,N\sqrt h\,dt\,d^3x
=\int R(g_L)dV_{g_L}.}\tag{21}
\]

Здесь `u` — малый **пробный параметр золотого determinant readout**, а не timelike observer `u^a`; он выбирается в едином admissible positive window у всех shape matrices. Масштабы u,2u — две сравниваемые настройки ОДНОЙ программы для удаления quartic, а не два независимых физических coupling. У каждой настройке должен учитываться её настоящий контроллерный/code cost.

**Стратегический выигрыш:** ни heat/short-time theorem, ни бесконечная nonlinear Einstein expansion для (20)–(21) вообще не нужны. Геометрическое nonlinear действие воспроизводится конечными **четырьмя** оригинальными golden outcomes, 4D normal estimator и его 3D spatial restriction. Его **первый source** также совпадает с δEH при всех 10 ADM variations автоматически, если все матричные/нормальные/observer/frame changes перенесены совместно и прочитаны в одном физическом действии. Здесь не постулируются ещё не имеющиеся physical native variations.

**Сопоставление с `A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md`.** Предыдущий `W_E` центральный AF terminal уже доказал, что для любого **независимо заданного** знакового геометрического скаляра Q в его declared window можно построить условную программу с `d_A A=\lambda a(z,\sigma)dQ`, \(\lambda a>0\), включая moving preparation. Формулы (20)–(21) теперь задают Q как **конечный вычислимый golden-geometric readout**, а не неизвестный Einstein oracle. Это сильная конструктивная компоновка, но ещё не доказательство, что native D0 физически выбирает именно такую composed программу или что её архивный код/контроллер бесплатны. Нельзя заменить исходную физическую v8 цену новым Q без typed primitive-to-program law.

### 9.3 Два решающих контроля

1. В пространственном static-product образце positive 4D normal shape есть `diag(0,A3)`, поэтому `R_G=R3`; Lorentz `R_L=−R3`. (20) даёт ровно этот знак. Требование `R_G+cR3=R_L` вынуждает `c=−2`, без вариантов.
2. Для **настоящей generic** 4D normal shape quartic term Q4 ненулевой. Попытка заменить (18) одним M4(u) даёт ложный R4; это проверено на двух некоммутирующих рациональных shape matrices и их moving source. Для 3D quartic отсутствует алгебраически, поэтому (19) не требует такого дополнительного измерения.

Код `check_finite_golden_spatial.py` и `GOLDEN_RESULTS.json` проверяют 24 точных symbolic контролей, включая полный moving first source, spatial zero-mode embedding, негативный quartic-control и static-product Lorentz sign. Это новая **finite geometry + readout identity**, а не новый physically selected action.
