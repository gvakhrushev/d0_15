# D0 → GR: физическая сцепка ОДНОЙ полной записи — Perron history → 718 outcomes → predictive information loss → 33-flag Book feedback

19 October 2026. **NEW POSITIVE FINITE MATHEMATICAL/OPERATIONAL THEOREM / original existing scientific PR #334.** This paper directly consumes the official registry/Lean owners and constructs an operationally meaningful positive feedback **from the SAME complete 33-state scene history**, without choosing a 33×33 spectral matrix to resemble Einstein. Its key contributions are (i) the EXACT equivalence of admissible positive real primitive edge prices modulo endpoint information plus common scale to ALL 685 physically distinct stationary Markov transition probabilities; (ii) the actual LEAN-OWNED nonstationary Perron history initialization converges to the endogenous invariant state at an explicit scene spectral gap, rather than requiring an externally assigned new preparation; (iii) a UNIQUE positive predictive-information-loss operator from one complete 718-outcome registered transition; (iv) an EXACT 33-step complete positive event with its all-good probability equal to the ORIGINAL Book03 logdet of that operator, including all failure outcomes, and its genuine complete moving-preparation first source; (v) an intrinsic original-scene 30+2+1 spectral fingerprint derived from the already accepted Lean Hodge/scene split.

**Important claim status:** this constructs ONE plausible native-type complete registered statistical process. It is NOT the claim that its canonical predictive operator equals the existing compulsory Book03 \(F_N\), that the primitive native D0 Cost-Info physically selects the Perron bulk preparation or these 33 real rotations/Cholesky arithmetic at zero cost, or that the response equals all ten Einstein metric rows. The official \`gr_assembly\` still has \`constitutive/native_sector/matter_source_ward/positive_gr\` OPEN; only the scoped \`probe_law\` has an accepted application. Nothing here edits the CONTROL claim ledger, promotes BOOK/CORE or replaces original RAW-216.

## 1. All 718 ORIGINAL scene edges: the exact 685-dimensional Cost−Info/Markov quotient

Use the literal complete tripartite graph \(\mathsf G=K(9,11,13)\), 33 vertices, 718 **directed** edges, 15708 two-step paths, degrees \(d=(24)^9,(22)^{11},(20)^{13}\), as OWNED in \`D0.VNext2.SceneHistoryPerronTrace\` and claims.csv. Let \(p=\varphi^{-1}\), \(\ell=\log\varphi\). Take **one original supplied** positive real net native edge Cost−Info \(s_{uv}\) on EACH legal edge, and the resulting Book positive transfer
\[
K_{uv}=e^{-\ell s_{uv}}>0\quad(u\to v),\qquad K_{uv}=0\ \text{on nonedges}.
\tag{1}
\]
\(K\) is primitive since the original tripartite graph has both 2- and 3-cycles. Its actual simple positive Perron pair \((\lambda,\ell_K,r)\), with \(\ell_K^Tr=1\), gives the original full-support Doob kernel and unique invariant measure
\[
\boxed{
P_{uv}=\frac{K_{uv}r_v}{\lambda r_u},\qquad
\pi_u=\ell_{K,u}r_u,\quad
\sum_vP_{uv}=1,\quad\pi P=\pi.
}
\tag{2}
\]

**Exact quotient theorem, both directions.** On the ENTIRE space of smooth finite positive real edge-price profiles, the map \(s\mapsto P\) is invariant under
\[
\boxed{s'_{uv}=s_{uv}+a+\psi_v-\psi_u,}
\tag{3}
\]
for any real scalar \(a\) and any real vertex function \(\psi\), whenever the profiles remain allowed by their true physical cost floor. Indeed \(K'=\varphi^{-a}D^{-1}KD\) for \(D_{vv}=\varphi^{-\psi_v}\), and the factors cancel from (2). **Conversely** if \(P'=P\), then
\(K=\lambda\operatorname{diag}(r)P\operatorname{diag}(r)^{-1}\),
\(K'=\lambda'\operatorname{diag}(r')P\operatorname{diag}(r')^{-1}\),
which forces precisely (3), with some \(a,\psi\). Thus the kernel is **exactly** 32 independent vertex coboundaries plus one global cost calibration:
\[
\boxed{
718-(33-1)-1=685.
}
\tag{4}
\]
Every strictly positive row-stochastic kernel P on the exact allowed native edges has one real edge-price representative \(s_{uv}=-\log_\varphi P_{uv}\), since K=P has \(\lambda=1,r=\mathbf1\). A common additive cost shift, if required, places all edges above the actual ActionProtocol unit floor without changing P. Hence there is a **surjective and injective-on-quotients** map:
\[
\{\text{positive REAL native edge prices}\}/
\{\text{endpoint coboundaries + global scale}\}
\longleftrightarrow
\{\text{full-support Markov kernels on the SAME 718 edges}\}.
\tag{5}
\]
The dimension of the right side is the ACTUAL 685 row-normalization degrees \(\sum_u(d_u-1)\). This is NOT a statement that integer/minimal Golden WORD costs cover all smooth 685 directions, nor does it make the absolute native Cost, its physical unit, or the unconditioned open-path partition gauge-invariant. The quotient describes precisely the whole LONG stationary probability law, not the full physical protocol objective.

## 2. The real LEAN-OWNED Perron history starts NONSTATIONARY, but selects the bulk state canonically

There is an important typed distinction missed by a naive Markov summary. The OWNED exact all-walks canonical trace in
\`03_FORMALIZATION/D0/VNext2/SceneHistoryPerronTrace.lean\`
has on the ORIGINAL UNWEIGHTED adjacency \(A\), with Perron eigenvalue \(\rho\) and \(\sum_v r_v=1\),
\[
\boxed{\tau_n(v_0\to\cdots\to v_n)=\rho^{-n}r_{v_n}.}
\tag{6}
\]
Its actual depth-zero preparation is \(\mu_0(v)=r_v\), **NOT** the stationary Markov state \(\pi_v=r_v^2/\sum_w r_w^2\). The original Perron transfer
\[
P_{uv}=A_{uv}r_v/(\rho r_u)
\]
reproduces the OWNED complete history law exactly, with no invented prior:
\[
\mu_0(v_0)\prod_{j<n}P_{v_jv_{j+1}}
=r_{v_0}\prod_{j<n}A_{v_jv_{j+1}}r_{v_{j+1}}/(\rho r_{v_j})
=\rho^{-n}r_{v_n}=\tau_n(\gamma).
\tag{7}
\]
The OWNED graph's stationary bulk state is \(\pi\propto r^2\). Since \(A\) is symmetric, this P is reversible in \(\ell^2(\pi)\). Its nontrivial eigenvalues are \(\lambda_2/\rho,\lambda_3/\rho\) and 30 zero modes, where \(\rho,\lambda_2,\lambda_3\) are the THREE roots of
\[
\boxed{t^3-359t-2574=0.}
\tag{8}
\]
Explicitly \(\rho=21.837382401125154\ldots\), \(\lambda_2=-9.758282910230204\ldots\), \(\lambda_3=-12.07909949089495\ldots\). Hence the exact finite **bulk relaxation** theorem is
\[
\boxed{
\|\mu_0 P^n/\pi-\mathbf1\|_{L^2(\pi)}
\le \vartheta^n\|\mu_0/\pi-\mathbf1\|_{L^2(\pi)},\quad
\vartheta=|\lambda_3|/\rho=0.5531386165712143\ldots<1.
}
\tag{9}
\]
Already at n=0 the OLD native zone masses are \((.291853565,.334984070,.373162364)\), while the derived bulk zone masses are \((.311559320,.335821792,.352618888)\). **They are different**, as the original Lean warning that all-walks history counting ≠ iterated naive random walk requires. The stationarity arises in the BULK of that ORIGINAL OWNED Perron history under its true Doob conditional transition; it is NOT a new compulsory initial preparation or a silently replaced simple degree-normalized random walk.

A generic field-dependent K(y) retains the algebraic PF/Doob construction and uniform spectral-gap mixing on compact strictly positive charts, but the original Lean all-walks \(\tau_n\) theorem by itself does NOT select that new field-dependent K(y), its initial preparation or physical clock. Equation (7) is literally OWNED only for the original adjacency, and any physical extension must preserve the same history/cost/source interface.

## 3. One COMPLETE native-type 718-output record uniquely determines its PREDICTIVE information-loss operator

On any supplied actual positive P and stationary \(\pi\) of (2), use the genuine old input Hilbert \(\mathbb R^{33}\) and an ORIGINAL-edge-labelled fresh register \(\mathbb R^{718}\). The explicit full one-step positive recording isometry is
\[
\boxed{
V_P|u\rangle
=\sum_{v:u\to v}\sqrt{P_{uv}}\,|u,v\rangle_{\rm edge}.
}
\tag{10}
\]
It obeys \(V_P^T V_P=I_{33}\) EXACTLY by row completeness and mutually orthogonal original edge labels. Every allowed original directed transition produces a distinct positive outcome, NO postselection, no merged source/target archive. As an isometry it has a real orthogonal completion on a sufficiently large ACTIVE work register; OLD RIGHT/reference128 may be tensored by identity. A corresponding \(\rho=\operatorname{diag}\pi\) preparation measures the complete joint law
\[
\boxed{q_{uv}=\pi_uP_{uv}>0\ \text{on all 718 edges},\quad
\sum_{uv}q_{uv}=1,}
\tag{11}
\]
with every original failure/return edge kept. This proves a genuine complete **finite Naimark/statistical representation** of the stationary transition, not its compulsory execution by the unchanged literal original 128-output v8 round. The active implementation needs its actual field-dependent source, Golden/Julia compiler, input encoding, work and clock COSTS.

Take ANY actual observable \(f\in\mathbb R^{33}\) on the registered FUTURE vertex, and predict it from the kept past vertex u using only the same complete q. The unique least-squares optimal predictor is the ACTUAL conditional expectation
\((Pf)(u)=\sum_vP_{uv}f(v)\). Its UNAVOIDABLE minimum squared error, computed from exactly the registered outcomes, is
\[
\begin{aligned}
\mathcal R_P(f)
&=\sum_{u\to v}q_{uv}\,[f(v)-(Pf)(u)]^2\\
&=\sum_v\pi_v f(v)^2-\sum_u\pi_u(Pf)(u)^2.
\end{aligned}\tag{12}
\]
Define the canonical \(\ell^2(\pi)\) adjoint \(P^\dagger_\pi=\operatorname{diag}(\pi)^{-1}P^T\operatorname{diag}(\pi)\). The UNIQUE symmetric quadratic operator representing (12) by polarization is
\[
\boxed{
F_{\rm pred}=I-P^\dagger_\pi P,\quad
\langle f,F_{\rm pred}f\rangle_\pi=\mathcal R_P(f)\ge0.
}
\tag{13}
\]
No exterior CAR16 eigenvalues, Euclidean signature conversion, phenomenological damping, free stress tensor, Einstein tensor or arbitrary feedback spectrum were supplied to define (13). It follows from the actually normalized conditional FULL history law and the operationally stated task **predict what the next registered event distinguishes using the retained past event**.

**EXACT RANK THEOREM on the ORIGINAL full scene.** Jensen equality in (12) means f(v) is constant across every positive neighbor set \(\mathcal N(u)\). Each of the three original zones has ≥1 vertex, and for any vertices v,w a common predecessor u exists in some other/third zone. Thus all f(v) coincide: constants are the **ONLY** null vectors. On all allowed full-support K:
\[
\boxed{0\preceq F_{\rm pred}\preceq I,\quad
\ker F_{\rm pred}=\operatorname{span}\mathbf1,\quad
\operatorname{rank}F_{\rm pred}=32.}
\tag{14}
\]
The entire rank32 statement is nonperturbative, native 33/718, **independent of Info allocation**, original edge calibration or the field values, as long as all718 original transitions remain strictly positive. In canonical Euclidean coordinates put
\[
T=\Pi^{1/2}P\Pi^{-1/2},\quad\Pi=\operatorname{diag}\pi,\quad
\widehat F=I-T^T T,\quad\ker\widehat F=\operatorname{span}\sqrt\pi.
\tag{15}
\]
The eigendata of \(\widehat F\) are nonnegative real and the operator is determined by ONE complete 718-outcome registered law, not selected afterwards.

## 4. Reconstruct one TRUE COMPLETE Book03 determinant event from the SAME recorded source — 33 binary gates, ALL failures retained

Use the ORIGINAL Book03 \(z=2^{-20}\in(0,1)\), no tunable fugacity, and the already derived canonical operator \(\widehat F\) on the actual 33-dimensional scene:
\[
G_z:=I-z\widehat F=(1-z)I+zT^TT,\quad
(1-z)I\preceq G_z\preceq I.
\tag{16}
\]
The Book03 FUNCTIONAL TYPE (not an independently chosen new action) evaluated on this operationally derived candidate is
\[
J_{\rm pred}=-\operatorname{Tr}\log G_z=-\log\det G_z.
\tag{17}
\]

**Actual finite positive event, no Gaussian Fock or 2^33 CAR assumption.** Fix the ORIGINAL graph vertex order once; take the positive Cholesky \(G_z=LL^T\), and let
\(d_k=L_{kk}^2=\det (G_z)_{1:k,1:k}/\det(G_z)_{1:k-1,1:k-1}\).
Because G_z is strictly positive and ≤I,
\[
\boxed{1-z\le d_k<1\quad(k=1,\ldots,33).}\tag{18}
\]
The upper strictness follows since every original scene vertex basis observable \(e_k\) has strictly positive conditional prediction variance (13), so \((G_z)_{kk}<1\), and each pivot is ≤this diagonal. Thus 33 **complete** sequential real 2-output rotations, with fresh retained success/failure flags and input-dependent but analytic positive probabilities \((d_k,1-d_k)\), define ONE finite test. The full outputs are
\[
\boxed{
\Pr(\text{all success})=\prod_{k=1}^{33}d_k=\det G_z,
\qquad
\Pr(\text{first failure at }k)
 =\left(\prod_{j<k}d_j\right)(1-d_k)>0.
}\tag{19}
\]
There are 34 disjoint COMPLETE positive outcomes and their probabilities sum1 **exactly** by telescoping. Every original future edge label remains in the preparation/record (11), all genuine 33 success/failure flags are retained in the full work archive; no successful branch is renormalized, no failure is discarded. On this one mathematically EXPLICIT complete detector,
\[
\boxed{-\log\Pr(\text{all success})=J_{\rm pred}}\tag{20}
\]
EXACTLY at ANY physical field value of the genuine positive source chart, not just at flat baseline. The Cholesky input \(G_z\) and pivot probabilities depend on the ACTUAL full old-record q; their genuine field derivatives are NOT silently frozen. Flag ordering changes the distribution among the 33 failure locations but NOT the all-good determinant; the complete fine-pointer Shannon can depend on ordering. The more specific [same-good/bad Golden refinement §6.66](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md) may then be applied only to THIS actually admitted all-good event and its real complete fine-failure output, not imported as the action by its name.

**NATIVE ADMISSION SCOPE:** These 33 positive binary rotations and finite Cholesky arithmetic are an EXPLICIT canonical complete abstract instrument, admitting standard real orthogonal/Julia dilations on a sufficiently large fresh ACTIVE workspace. They are NOT proven executable EXACTLY by the unchanged literal GoldenCoherentMemory fullStep, with its limited Golden angle/cost, one-way retained-record constraints, real resource budget or uniform C¹ compiled errors. The original 718 edge test and 33 Cholesky flags are mathematically one complete composite process with all output registers, but **the physical D0 must select/pay for such a process** for (20) to be a statement about the fundamental action.

## 5. SAME real native field source through all moving probabilities, including \(\pi\)

On a fixed strictly positive full-native Cost/Info field chart \(y\), let \(\delta s_{uv}=D_y s_{uv}[V]\), and set \(\delta\log K_{uv}=-\ell\delta s_{uv}\) on all718 actual edges. The Perron source and moving right-eigenvector source are determined with NO inverse-fitted Einstein tensor:
\[
\begin{aligned}
\delta\log\lambda&=\sum_{uv}\pi_uP_{uv}\delta\log K_{uv},\\
(I-P)g&=\sum_vP_{uv}\delta\log K_{uv}-\delta\log\lambda,
\quad g_u=\delta\log r_u,\quad\pi g=0,\\
\boxed{\delta\log P_{uv}=\delta\log K_{uv}
              +g_v-g_u-\delta\log\lambda.}
\end{aligned}\tag{21}
\]
The source equation is solvable since its RHS has zero \(\pi\)-mean, and \(\pi g=0\) fixes its only additive ambiguity. The true \(\delta\pi\) then follows from the already proved stationary-history formula
\[
\boxed{\delta\pi=\pi(\delta P)
             (I-P+\mathbf1\pi)^{-1},\quad\delta\pi\,\mathbf1=0.}\tag{22}
\]
For \(T=\Pi^{1/2}P\Pi^{-1/2}\), with \(H_\pi=\operatorname{diag}(\delta\pi_u/\pi_u)\), the COMPLETE native first source is
\[
\begin{aligned}
\delta T&=\Pi^{1/2}(\delta P)\Pi^{-1/2}
                 +\tfrac12(H_\pi T-T H_\pi),\\
\delta\widehat F&=-(\delta T)^TT-T^T\delta T,\\
\boxed{\delta J_{\rm pred}
=z\operatorname{Tr}[(I-z\widehat F)^{-1}\delta\widehat F]
=-2z\operatorname{Tr}[(I-z\widehat F)^{-1}T^T\delta T].}
\end{aligned}\tag{23}
\]
This differentiates the SAME positive determinant event (19), includes **all moving 33-state preparation probabilities**, correct spectral adjoints and all full edge weights, and has no fitted \(\delta\pi\) or frozen normalizer. In particular adding either a global Cost shift \(\delta s_{uv}=c\) or any endpoint coboundary \(\delta s_{uv}=\psi_v-\psi_u\) makes \(\delta P=\delta\pi=\delta\widehat F=\delta J_{\rm pred}=0\) EXACTLY. Therefore this **physically observable predictive loss** depends on precisely the 685-dimensional native transition-cost quotient (5), not the arbitrary Book endpoint Info convention or an extra scene stationary prior.

**NONZERO actual native-edge contrast, not only a source named by Einstein.** Perturb only one real original allowed edge 0→9 by its true positive unit-gap excess: \(s_{0,9}=1+t\), all other primitive edges remain1. On the genuine full33 graph the same source (23) has a nonzero value
\[
\left.\partial_tJ_{\rm pred}\right|_{t=0,z=2^{-20}}
 \approx-1.3245\times10^{-10}\ne0,
\tag{24}
\]
with moving \(\pi\) derivative magnitude up to \(\sim6.6453\times10^{-4}\). For numerical source discrimination the identical original native programme at a TEST z=.01 gives \(\partial_tJ_{\rm pred}\approx-1.39365\times10^{-6}\); z=.01 is diagnostic only, NOT a changed physical fugacity. These are derivatives of supplied original edge Cost, not an arbitrary variation of F. **They are not Einstein metric Euler components:** one must still derive the actual native coframe/link/CAR→edge Cost/Info source map on the SAME process to pull (23) onto the original 16+24+2 target.

## 6. Exact intrinsic 30+2+1 feedback spectrum from the ALREADY OWNED SCENE, no foreign operator

At the pointwise LEAST admissible real native edge-price reference \(s_{uv}=1\), the transfer is exactly \(K=p A_{\rm native}\), with A the literal undirected complete tripartite adjacency. This is a **reference member of the ActionProtocol admissible fiber**, not the assertion that D0 physically SELECTS the least member in a varying gravitational field. The resulting Perron–Doob P is reversible with \(\pi_v=r_v^2/\|r\|²\). By the ACCEPTED LEAN-OWNED all-walks Perron trace in §2, this is the canonical native bulk of its actual original cylinder measure.

The 33×33 symmetric adjacency has rank3: its 30-dimensional zone-standard kernel is exactly the OWNED 30 archive sector of \`D0.Synthesis.AutomorphismHodgeSDEDecomposition\` AS A REPRESENTATION, but beware that the native \`fullTransport\` in that owner is the **DIFFERENT naive row-degree-normalized random walk**, whose depth-two probabilities the existing \`SceneHistoryPerronTrace\` Lean explicitly proves DIFFER from the Perron all-walks law. Therefore its quoted rational 359/160 active *NORMALIZED-LAPLACIAN* spectrum CANNOT be substituted into the current native all-walks Perron kernel.

Use instead the TRUE native adjacency quotient
\(A_3=\bigl(\begin{smallmatrix}0&11&13\\9&0&13\\9&11&0\end{smallmatrix}\bigr)\).
Its exact characteristic polynomial is
\[
\boxed{\operatorname{charpoly}(A_3;t)=t^3-359t-2574,}
\tag{25}
\]
with positive root \(\rho=21.837382401125154\ldots\), and two negative roots \(\rho_2=-9.758282910230204\ldots\), \(\rho_3=-12.07909949089495\ldots\). The TRUE native Doob P has 30 zero eigenvalues, Perron eigen1 and active eigen \(\rho_2/\rho,\rho_3/\rho\). Since it is reversible, the canonical conditional-variance operator has the EXACT spectrum
\[
\boxed{
\operatorname{spec}\widehat F
=\{0\}^{1}
 \cup\{1\}^{30}
 \cup\{1-(\rho_2/\rho)^2,\ 1-(\rho_3/\rho)^2\}.
}
\tag{26}
\]
This gives a genuinely **EXACT native 30/archive+2/active+1/stationary feedback decomposition** from ONE existing registered graph law (not a fabricated 33-mode spectrum):
\[
\boxed{
\det(I-z\widehat F)
=(1-z)^{30}
\left[
1-\left(3-\frac{718}{\rho^2}\right)z
+\left(3-\frac{1436}{\rho^2}+\frac{359^2}{\rho^4}\right)z^2
\right].
}
\tag{27}
\]
At the original Book03 \(z=2^{-20}\),
\[
\boxed{J_{\rm pred}=0.000030035369315208\ldots,\qquad
\Pr(\text{all-good})=0.99996996508175\ldots .}
\tag{28}
\]
The 30 identical archive terms contribute a fixed \(-30\log(1-z)\) only at the symmetric reference, and the two active terms are explicitly determined by the original Perron cubic. Under *general* field-dependent native costs, the scene symmetry can break: the 30 archive eigenvalues need NOT remain fixed or field-source-inert. Do not promote a 2-mode-only GR source from the frozen reference decomposition.

**Independent hostile control:** the DIFFERENT naive degree-normalized scene random walk has active Laplacian product 359/160 and yields a DIFFERENT predictive feedback value \(0.000030028834189135\ldots\). The difference \(\sim6.535\times10^{-9}\) is real. Treating that rational normalized Hodge spectrum as the original Perron history would violate the existing LEAN exact negative control. This explicitly tests and repairs the native-Perron-versus-row-normalized source typing on the SAME fixed 33 scene.

## 7. Precisely what physical D0→GR gap this closes

The OWNED finite scientific GR route already has full original 16+24+2 coframe/link/CAR curved Einstein stationary families and a general conditional geometric/matter source of the form \(a_hD\sum\widehat f+b_hD\sum q\). What it lacked for a physical whole-source theorem was that "old-record probabilities, stationary preparation, feedback operator, historical information cost" often belonged to DIFFERENT declared mathematical programmes. The present construction produces from ONE specifically declared full scene Cost/Info transition programme, with no exogenous probability prior or operator spectrum:
\[
\boxed{
\text{native old 33/718 edge Cost−Info}
\to \text{actual all-walks Perron/Doob recorded law}
\to \text{endogenous bulk }\pi\text{ and }D\pi
\to \text{complete edge-labelled 718-event isometry}
\to F_{\rm pred}=\text{unique conditional variance}
\to \text{complete 33-flag registered }\det(I-zF_{\rm pred})
\to \text{actual moving first feedback source (23)}.
}
\]
The graph, positive edge prices, probability normalization, prediction-loss operator, its rank and its full source are no longer independent "Einstein-looking" inputs in THIS finite mathematical programme. The predicted operator is not an assigned metric tensor or fitted relative stress.

**Only proper physical promotion test:** prove that the actual compulsory D0 \`ActionProtocol\` with its true accepted physical Cost/Info event and field-dependent native coframe/link/CAR preparation (i) selects THIS specific complete 718-event Perron/Doob long-history programme or its exactly owned replacement, (ii) physically executes/prices the 33-flag complete determinant event (or proves the original Book03 F_N IDENTICAL to F_pred on the very same output/work cut), and (iii) pulls the full real 718-edge Cost/Info first source (23) to precisely the original independent 16+24+2 star/CAR Einstein covector, while cancelling/solving OTHER genuinely selected H+R/history/clock/observer/preparation sources and proving the real joint refining roots. No source equality with GR follows merely from PF or Schur positivity. The current original \`gr_assembly\` has only the scoped probe-law accepted application; \`constitutive\`, \`native_sector\`, \`matter_source_ward\`, \`positive_gr\` and original RAW-216 remain OPEN. Do NOT modify official acceptance or claim physical GR closure by this research.
