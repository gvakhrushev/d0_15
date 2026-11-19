# Один оплаченный compiler cap: точное совпадение пространственных весов gravity и matter

21 октября 2026. Ограниченное применение существующего #334. Вход `c49ebdb12244943d1ec45ef6d148a0432481141e`; исходники прочитаны в чистом worktree `same-execution-spatial-source/d0_15`. Репозиторий не изменялся. Это первое источниковое тождество **одной уже описанной complete CQ programme при cap N=1**, а не новая физическая цена, Info-конвенция или задача.

## 1. Точный потреблённый programme

`book_source/GOLDEN_EXACT_DETECTOR.md` §§4–5 описывает две исходные 8D-query, независимые 20-bit coherent efficiency registers, 43 Toffoli и шесть дополнительных CNOT; compiler failures, fair signs, retry times, abort, actual clock и условная квантовая работа сохраняются. Никакая измеренная efficiency coin не подставляется вместо coherent registers. На каждый фактический local 8D block b приходится **свой** paid bank и detector. Abort одного local block не является событием global all-ready; остальные local implementations сохраняют свои записи.

Берём уже разрешённый конечный cap **N=1**, с одинаковыми для всех b caps K_pre=9 и L_gate=20. `COMPLETE_COMPILER_COFRAME_EQUIVALENCE.md`, §§3,7, уже потребляет именно эту специализацию. Исходный банк содержит 128 потенциальных fair resources на local block; readiness
\[
 \alpha=[1-(1-2p^3)^9]^{128},\qquad
 \beta=[(1-p^{120})^4(1-(1-16p^9)^{20})]^{43}>0,
 \quad p=\varphi^{-1}.
\tag{1}
\]
Это данные существующего конечного алгоритма, не выбираемые полевые веса.

Пусть C_pre,b,H_pre,b — полные bank cost/entropy; μ_b — действительный ожидаемый stage cost; H_T,b — полный transcript entropy, κ_b=μ_b−H_T,b. Каждый из этих членов сохраняется, включая неудачные и неиспользованные ресурсы. `FULL_PRICE_COMPOSITION.md` (фактический путь `sources/d0_global_result_composition_2026-10-20/FULL_PRICE_COMPOSITION.md`), (1), при N=1 даёт
\[
 S_b=C_{pre,b}-H_{pre,b}+\alpha_b[\kappa_b-\beta_b h_\varphi(r_b)].
\tag{2}
\]
В утверждении о пространственных весах используются **одинаковые значения α_b=α, β_b=β**, обеспеченные одинаковыми bank/gate caps и data-independent success laws исходного compiler. Равенство κ_b между разными адресами НЕ требуется. Routing/query costs могут различаться по b, если выполнена исходная fixed-field-cost interface. Они не объявляются бесплатными; в cap1 они входят в (2) ровно один раз на достигнутый stage и остаются в baseline.

Классическая запись каждого local implementation полна; его условная quantum work state чиста на исходном pure-input chart. При независимых local implementations полная declared CQ цена — сумма (2), плюс только действительно отдельно оплаченные upstream components. Это не вывод product law для коррелированной общей фабрики. Отождествление этой declared CQ valuation с compulsory Book03 Info остаётся отдельным условием.

## 2. Реальные адреса, multiplicities и одна input map

Используем буквальный `A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md`, (1)–(4),(8). Пусть a=(j,i) — оригинальный defining LEFT address, с regular multiplicity D_j. При фиксированном AF depth
\[
 K_{AF}=\sum_jd_jD_j,\quad \pi_a=D_j/K_{AF},\quad
 w_z=\sum_{a\in\mathcal I_z}\pi_a>0,\quad
 \bar w=L^{-4}\sum_z w_z,\quad \rho_z=w_z/\bar w.
\tag{3}
\]
Здесь \(\mathcal I_z\) — существующие READY-projector address sets, не новое разбиение по желаемому источнику. Inactive addresses остаются с zero density. Для обоих исходных полей используется ОДНА карта
\[
 f_a=\rho_z^{-1}\widehat f_z,\qquad
 q_a=\rho_z^{-1}q_z\quad(a\in\mathcal I_z).
\tag{4}
\]
\(\widehat f_z=\rho_z f_z\) — старый degree-two star на density-dressed coframe; q_z — nondensitized original CAR Clifford square на **том же** operational metric. q_z=0 не означает Dq_z=0: ненулевой null matter gradient и его все геометрические/материальные variations остаются. Если сначала записать q_raw на raw metric, то q_z=ρ_z⁻¹ q_raw и q_a=ρ_z⁻² q_raw. Этот двойной inverse относительно raw variable уже содержится в исходной operational-metric карте; это не новая вставленная мера.

Оригинальный ordinary trace имеет \(\nu\,528\,D_j\) копий local **8D** unit на address a. Здесь ν — уже существующая reference multiplicity; 528 — matched scene pairs. Четыре AF tails уже находятся внутри 8D=4×2; два query вычисляют два eigenvalue factors одного local determinant и НЕ дают ещё один multiplicity factor 2. Original complements и inactive modes не удаляются: их F=0/field-independent contribution остаётся на carrier и в действительно исполняемых baseline costs. Неисполненный query не считается выполненным и цена не дублируется.

Для полного compiler programme следуем предписанию владельца: separate paid implementations на всех фактических trace copies. Поэтому суммирование actual local ledger имеет те же integer multiplicities, а не усреднение по произвольной подготовке. Сокращение
\[
 \sum_{a\in\mathcal I_z}\frac{D_j}{\rho_z}
 =\frac{K_{AF}w_z}{\rho_z}=K_{AF}\bar w
\tag{5}
\]
точно и одинаково для каждого покрытого site z, даже при неравных golden descendant counts. Это общий spatial factor обоих source channels.

Важно: π_a здесь определяется **trace multiplicity**, а не произвольно меняющимся Born occupation данного input density. Нельзя заменить D_j полной вероятностью адреса из другого эксперимента. Coherent global scalarization с делением на padded dimension — отдельный owned programme из causal synthesis §2; его normalization/repetitions сюда не импортируются.

## 3. Настоящий local two-density derivative

Обозначим local scaled arguments x=η² f_a, y=ση² q_a, где η — общая исходная query calibration, σ — существующая Golden orientation. При фиксированных p,z₀=2⁻²⁰ исходная двухполосная функция равна
\[
 B(y)=4(p+p^2y)^2[1-(p+p^2y)^2],\quad
 \ell(E)=4E(1-E),\quad E(x)=p^2(1+x),
\]
\[
 A(x,y)=\ell(E(x))+[1-\ell(E(x))]B(y),\qquad
 r(x,y)=1-[1-z_0B(y)][1-z_0A(x,y)].
\tag{6}
\]
Это тот же determinant click probability, восстановленный двумя original 8D queries. При x=y=0 положим
\[
 L_0=4p^3,\quad Q=1-z_0L_0,\quad R=1-z_0L_0(1+p^6),
 \quad d_0=QR,\quad r_0=1-d_0\in(0,1/2).
\]
Непосредственное дифференцирование (6), включая ОБЕ полосы, даёт
\[
 r_x=4z_0Qp^{11},\qquad
 r_y=8z_0p^6(R+Qp^6).
\tag{7}
\]
Следовательно
\[
 Dr_b|_\Sigma=\eta^2(r_x Df_a+\sigma r_y Dq_a),\qquad
 Dj_b=d_0^{-1}Dr_b,
\tag{8}
\]
где \(\Sigma=\{\widehat f_z=q_z=0\ \forall z\}\), а все ambient coframe16+link24+matter2 variations сохраняются. Старый two-query owner §4 доказывает equality FIRST derivatives determinant/two-query при любом off-diagonal tangent у diagonal baseline; поэтому (8) не требует замораживания подвижных eigenvectors по недопустимому упрощению.

Для N=1 из (2)
\[
 DS_b|_\Sigma=D\mathcal B_b-\alpha\beta h'_\varphi(r_0)Dr_b,
\quad \mathcal B_b=C_{pre,b}-H_{pre,b}
       +\alpha_b[\kappa_b-\beta_b h_\varphi(r_0)].
\tag{9}
\]
D𝓑_b означает полный derivative actual baseline, включая все независимые setup variables. При fixed setup он равен нулю в field directions. Поскольку \(h'_\varphi(r_0)=\log_\varphi[(1-r_0)/r_0]>0\), множитель
\[
 \gamma_1=-\alpha\beta d_0 h'_\varphi(r_0)<0
\tag{10}
\]
строго ненулевой, независимо от κ_b и без lower bound/целочисленного допущения о цене gate.

## 4. Полное пространственное тождество на Σ

Суммируем (9) один раз по actual local copies. Положим \(\mathcal B\) равным сумме всех 𝓑_b с их действительными multiplicities плюс настоящие дополнительные upstream terms, которые не вошли в local ledger. Из (5),(7),(8) получаем
\[
 \boxed{
 DS_{CQ,full}|_\Sigma=D\mathcal B+
 a_h D\sum_z\widehat f_z+b_h D\sum_zq_z,
 }
\tag{11}
\]
\[
 a_h=-\alpha\beta h'_\varphi(r_0)\eta^2\nu528K_{AF}\bar w\,4z_0Qp^{11},
\]
\[
 b_h=-\alpha\beta h'_\varphi(r_0)\eta^2\nu528K_{AF}\bar w\,\sigma8z_0p^6(R+Qp^6).
\tag{12}
\]
Таким образом, gravity и matter имеют **одну и ту же пространственную константу** на каждом z. Их физически значимое относительное значение не назначается:
\[
 \frac{b_h}{a_h}=\frac{2\sigma}{p^5}\left(\frac RQ+p^6\right)
 =\Lambda_\sigma(2^{-20}).
\tag{13}
\]
При σ=−1 это прежнее \(\Lambda_-\approx-23.416406751884\). Ненулевой a_h при η≠0, положительных multiplicities и readiness даёт нужную source interface. Эквивалентная запись:
\[
 DS_{CQ,full}|_\Sigma=D\mathcal B+\gamma_1 DJ_{2,loc}|_\Sigma.
\tag{14}
\]
Это не новый J2 и не подгонка Info. J2 только именует уже заданный геометрический/source comparator; S_CQ задана (2) до сравнения.

Никакого site-dependent деления на число blocks не сделано. Отображение \(S/(\nu K_{AF})\) допустимо лишь как отображённая глобально нормированная формула при фиксированных discrete data; physical programme исполняет ненормированную sum price. Независимое деление каждого site на \(M_z=\sum_{a\in\mathcal I_z}D_j\) дало бы вместо (5) множитель \(1/\rho_z\), вообще не постоянный. При неравных M_z оно нарушает этот source transport. Также paid single-address random sampling является другой programme с собственной полной law адреса; она здесь не подразумевается.

### Positive same-execution application to all 42 field directions

On the owner's **fixed-cost/stationary-delay interface**, p, z0, N=1, K_pre, L_gate, integer multiplicities and LEFT address projections are fixed. The actual paid query/routing/report prices and all compiler transcript laws are genuinely independent of those 42 fields, as specified by the consumed owner. For the complete compiler price (2), the baseline is exactly the sum of its paid local baselines and already included field-independent idle/preparation terms. Thus D_42 B=0 numerically on this interface; no compensating residual is being assumed. Consequently
\[
 \boxed{D_{42}S_{CQ,full}|_\Sigma=\gamma_1 D_{42}J_{2,loc}|_\Sigma,
 \qquad\gamma_1<0.} \tag{17}
\]
This is equality of the **complete** compiler CQ source, not merely its report part. It preserves the actual matter rows and independently varied link rows on Sigma. It does not establish independently selectable upstream preparation equations.

The fixed query states psi+ and psi- here are **generated**, not frozen freely selectable unknown eigenvectors. `DETERMINANT_PREPARATION_BANK.md` sections 2-3 prepares them from computational blanks by the actual G/CNOT parity gadgets, retains every failed trial and success clock, pays the known-one echo for minus, and routes the result into canonical slots. Every ready transcript delivers the same states and independent coherent efficiency resources. This is a consequence of the paid finite bank; its intermediate generated states can use the existing causal-adjoint elimination without losing their price.

The complete oldRIGHT/archive with required purifying spectators remains in the owner's pure-input convention. The compiler transcript law is data-independent for arbitrary pure data, including external entanglement; the entire quantum work is pure conditional on the full measured tape. No extra dephasing or entropy erasure is inserted. A moving initial mixed record without its retained purifier, an independently selectable upstream preparation, a new physical sampling-time dependence, or an additional genuinely priced H/R/normalizer component outside this declared ledger needs its own actual derivative. Such a component is NOT put in B and then declared field-independent. Neither (17) nor the paid-bank construction proves foundational admission of the moving-field query/fixed-cost interface or selects CQ as the compulsory Book Info.

## 5. Moving preparation и точная остающаяся граница

Тождество не держится на замораживании скрытого \(D\rho_z\). Дифференцирование (4) даёт
\[
 Df_a=\rho_z^{-1}D\widehat f_z-
       \rho_z^{-1}\widehat f_z D\log\rho_z,
 \qquad
 Dq_a=\rho_z^{-1}Dq_z-
       \rho_z^{-1}q_z D\log\rho_z.
\tag{15}
\]
На Σ вторые члены действительно равны нулю **по значению плотностей**, не потому что Dρ объявлен нулевым. Это не удаляет зависимость operational metric/matter от ρ внутри полных Dfhat,Dq. В literal original fixed AF carrier D_j, K_AF,READY partition и hence regular ρ дискретно фиксированы; произвольно меняющийся initial density — другой input variable. Если закон physical preparation меняется, его actual entropy/cost/source надо добавить в D𝓑 или в существующие genuine query maps; (15) не делает его бесплатно stationary.

Полный baseline differential при фиксированных p,z₀ и r₀:
\[
 D\mathcal B_b=D(C_{pre,b}-H_{pre,b})+
 [\kappa_b-\beta_b h_\varphi(r_0)]D\alpha_b
 +\alpha_b D\kappa_b-\alpha_b h_\varphi(r_0)D\beta_b.
\tag{16}
\]
В частности, реальное moving address loading, query clock, preparation law, conditional mixed-input entropy или дополнительная H/R цена не исчезают из полной цены. Если исходная готовая программа имеет independently selectable preparation variables, надо решить их действительные уравнения D𝓑=0 или иной выведенный coupled stationary law. Causal elimination промежуточных состояний из parent synthesis сохраняет (11); оно не доказывает stationarity upstream state.

Общие значения α,β,η важны. Если фактические local ready factors различаются, spatial coefficient становится \(\rho_z^{-1}\sum_{a\in\mathcal I_z}D_j\alpha_a\beta_a\eta_a^2\), и его равенство по sites требует отдельного доказательства. Здесь одинаковые caps и та же query calibration задают их общность на actual owned interface. Это не предположение одинакового κ_a.

Для N≥2 старый owner действительно нуждается в другом условии: уже при N=2
\[
 \partial_r S_b=\alpha\beta\{\kappa_b-\beta h_\varphi(r)-h'_\varphi(r)(1+\beta r)\},
\]
поэтому \(\partial_{\kappa_b}\partial_rS_b=\alpha\beta\ne0\). Unequal real address costs могут менять source weights. Мы не присваиваем им искусственные значения, а применяем cap1, уже входящий в исходный конечный programme и разрешающий эту конкретную parent premise без требования common loading price.

**Доказано:** на одной данной paid cap1 programme spatial-weight matching и оригинальный gravity/matter ratio следуют из её полного CQ ledger, настоящих trace multiplicities и исходной inverse-PF карты. Равенство не требует uniform Born probabilities и не нарушает all42 first variation. **Не доказано этим:** compulsory selection CQ Info/continuation; native moving-field input admission; actual upstream stationary root; исчезновение полной иной физической residual; physical GR closure. Это точная подстановка spatial/source premise существующего all40+2 consumer, с D𝓑 оставленным явно.
