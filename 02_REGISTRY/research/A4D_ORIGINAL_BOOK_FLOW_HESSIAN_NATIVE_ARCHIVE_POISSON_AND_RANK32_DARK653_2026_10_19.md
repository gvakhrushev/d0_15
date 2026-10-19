# D0→GR: exact all-718 Book history Hessian = native archive metric; original future rank32 and dark653 split

2026-10-19. **EXACT ORIGINAL-SCENE OPERATOR BRIDGE / scoped negative against universal rank32 source identification / research in Draft #384.** Native graph: all 33 original K(9,11,13) vertices and all 718 directed edges. Native equal-Cost Perron/Doob owner and original full edge source/target isometries in [\`#334 native archive future self-energy\`](https://github.com/gvakhrushev/d0_15/blob/2a65c4cc433145acb70084abff09882c5112d807/02_REGISTRY/research/A4D_ARCHIVE_FUTURE_CAUSAL_SELF_ENERGY_AND_DETECTOR_TIME_2026_10_19.md). Consume the already-proved [single scalar all-path Book macro-action and full flow Hessian](A4D_ORIGINAL_BOOK_ALL_PATHS_FLOW_PRESSURE_ACTION_AND_EXACT_HISTORY_SCHUR_2026_10_19.md). There is NO added action, physical detector, clock, field, coupling or memory operator. \`GR_closed=false\`.

## 1. First main theorem: original historical Cost−Info Hessian is the norm of the ORIGINAL CURRENT ARCHIVE

For a strongly connected original finite 718-edge positive-on-support Book transfer \(K_{uv}=\varphi^{-s_{uv}}>0\) on original edges, let \(\lambda>0\) be its Perron root, \(P_{uv}=K_{uv}r_v/(\lambda r_u)\) its native Doob chain, \(\pi P=\pi\), \(\pi_u>0\), and \(f^*_{uv}=\pi_uP_{uv}>0\). Write \(E=718\), \(V=33\).

The scalar whole-history Book macro-action **induced by the actual complete path counting** is already owned:
\[
\mathcal A_y(f)=\sum_{uv}f_{uv}s_{uv}(y)
+\sum_{uv}f_{uv}\log_\varphi(f_{uv}/f_u),\quad
f\in\mathscr F,\quad
\sum_e f_e=1,\quad \sum_v f_{uv}=\sum_v f_{vu}.
\]
It has a UNIQUE root \(f^*=\pi P\), and minimum \(A_{\rm eff}=-\log_\varphi\lambda\). Define the original **normalized balanced-flow** tangent space
\[
\mathcal T=\{z\in\mathbb R^E:\ \sum_ez_e=0,\quad\sum_vz_{uv}=\sum_vz_{vu}\},\quad
\dim\mathcal T=E-V=685.
\]
This dimension uses the incidence rank V−1 of the connected native directed scene plus one independent total-mass constraint.

The original full edge Hilbert space \(H_E=\mathbb R^{718}\) and **already-owned current source-view isometry** \(J_0:H_V\to H_E\) are
\[
(J_0)_{(u,v),x}=\delta_{u,x}\sqrt{P_{uv}},\quad J_0^\top J_0=I_{33}.
\]
Let \(Q_A=I_{718}-J_0J_0^\top\) be its ACTUAL current-invisible archive projection; \(\operatorname{rank}Q_A=685\). Put \((Wz)_{uv}=z_{uv}/\sqrt{f^*_{uv}}\). Then the exact original rate-action Hessian is
\[
\boxed{
H_f[z,z]=\frac1{\ln\varphi}
\left(\sum_{uv}\frac{z_{uv}^2}{f^*_{uv}}-\sum_u\frac{z_u^2}{\pi_u}\right)
=\frac1{\ln\varphi}\|Q_AWz\|_{H_E}^2.}\tag{1}
\]
Proof: \((J_0^\top Wz)_u=z_u/\sqrt{\pi_u}\), so the subtraction is literally the orthogonal projector \(Q_A\), not an analogy.

**A stronger original-native fact is that**
\[
\boxed{Q_AW:\mathcal T\ \xrightarrow{\ \cong\ }\operatorname{ran}Q_A}\tag{2}
\]
**is a linear ISOMORPHISM onto the entire 685-dimensional real archive.** Indeed, \(Q_AWz=0\) implies \(z_{uv}=f^*_{uv}a_u\) for some source-vertex scalar a. Flow balance forces the left stationary measure \(\pi a\) for irreducible P, hence \(a\) constant. Total normalization \(\sum_ez_e=0\) forces a=0; thus injective. Both spaces have dimension E−V=685. Therefore every original currently invisible edge/archive direction can be represented uniquely as a normalized balanced history-flow tangent, without an added variable or a new coupling.

This ISOMORPHISM refers to the full \(\operatorname{ran}Q_A\), **not** automatically to the rank32 genuinely future-populated channel \(\operatorname{ran}(Q_AJ_1)\).

## 2. Second main theorem: finite native Markov Poisson equation exactly integrates ALL scalar history flow modes

Take ANY real first variation \(d_{uv}=D_Vs_{uv}\) of the ORIGINAL primitive scalar Book Cost−Info prices, with any parameter y and fixed original finite graph. Compute from the ACTUAL normalized native chain:
\[
c=\sum_{uv}f^*_{uv}d_{uv},\qquad
b_u=\sum_vP_{uv}d_{uv}-c,\quad\sum_u\pi_ub_u=0.
\]
The irreducible primitive original P has a UNIQUE zero-\(\pi\)-mean solution
\[
(I-P)\xi=b,\qquad \sum_u\pi_u\xi_u=0.
\]
Define the **original martingale/conditional innovation**
\[
m_{uv}=d_{uv}-c-\xi_u+\xi_v,\qquad
g_{uv}=\sqrt{f^*_{uv}}\,m_{uv}.
\]
By the Poisson equation, \(\sum_vP_{uv}m_{uv}=0\); hence \(J_0^\top g=0\) and \(g\in\operatorname{ran}Q_A\) EXACTLY.

For every normalized balanced-flow variation \(z\in\mathcal T\), the original mixed field-flow response is
\[
R_d(z)=\sum_e z_ed_e=\sum_ez_em_e=\langle Q_AWz,g\rangle.
\]
Constants annihilate the total constraint and vertex coboundaries annihilate balance. Since (2) is ONTO and (1) is the positive flow Hessian, the Schur quadratic form has a closed **finite no-free-inverse** expression:
\[
\boxed{
R_dH_f^{-1}R_d^\top
=\ln\varphi\,\|g\|^2
=\ln\varphi\sum_{uv}\pi_uP_{uv}(d_{uv}-c-\xi_u+\xi_v)^2.}\tag{3}
\]
For two field directions V,W the polarized Schur cross term is \(\ln\varphi\langle g_V,g_W\rangle\). Consequently for the SAME original path-count macro-action:
\[
\boxed{
D_{VV}^2\mathcal A_{\rm eff}
=\sum_ef_e^*D_{VV}^2s_e
-\ln\varphi\sum_ef_e^*m_e^2.}\tag{4}
\]
This proves exact iff source invisibility
\[
R_d=0\ \iff\ g=0\ \iff\ d_{uv}=c+\xi_u-\xi_v
\]
for all 718 native edges. The term is the stationary Markov additive Cost innovation/asymptotic variance; no Feynman or geometric Hessian is inserted.

## 3. POSITIVE complete bridge: the actual original symmetric K9↔K11 Cost source lies ENTIRELY in the owned rank32 FUTURE archive

Now specialize to the actual original equal-primitive-Cost, Info=0 scene and genuine #334 **original Book edge Cost probe**, \(d_{uv}=1\) on ANY directed K9↔K11 pair, and 0 on the other native cross-zone pairs. This indicator has an **EXACT native zone-vertex decomposition**:
\[
d_{uv}=\alpha_u+\alpha_v,\qquad
\alpha_{K9}=\alpha_{K11}=\tfrac12,\quad
\alpha_{K13}=-\tfrac12.
\]
No coefficient is fitted; this equality holds on EVERY one of the 718 actual edges.

The same #334 owner defines the original target isometry
\[
(J_1)_{(u,v),x}=\delta_{v,x}\sqrt{\pi_uP_{uv}/\pi_v},\quad
T=J_0^\top J_1=\operatorname{diag}(\sqrt\pi)\,P\,\operatorname{diag}(1/\sqrt\pi).
\]
At original equal symmetric Cost, P is reversible and T=Tᵀ. The future-populated archive is \(\mathcal R=Q_AJ_1=J_1-J_0T\), with rank32, and its native feedback is
\[
\mathcal R^\top\mathcal R=F_A=I_{33}-T^2
\]
EXACTLY the previously owned ORIGINAL archive feedback operator, not a newly designed metric.

Let \(\xi\) be the genuine Poisson solution of §2 for THIS native d and define \(\chi=\alpha+\xi\), \(h_u=\sqrt{\pi_u}\chi_u\). Then the original Poisson equation gives the exact **identity on EVERY native directed edge**
\[
m_{uv}=\chi_v-\sum_wP_{uw}\chi_w,
\quad\boxed{g=\mathcal Rh.}\tag{5}
\]
Therefore all 685-dimensional historical Hessian innovation for this native symmetric source belongs to the original **rank32** future-populated archive and
\[
\boxed{
D_{tt}^2\mathcal A_{\rm eff}(0)
=-\ln\varphi\,h^\top F_Ah
=-0.1297284254564436\ldots.}\tag{6}
\]
The first derivative is the original \(\sum f_ed_e=0.2947622241032769\ldots\). Independent full718 checks give \(\|g-\mathcal Rh\|_2<5\cdot10^{-15}\), \(\|J_0^\top g\|_2<2\cdot10^{-15}\), \(\|g\|_2^2=h^\top F_Ah=0.26958694425344865\ldots\), and \(\ln\varphi\|g\|^2=0.1297284254564436\ldots\).

This is a genuine new SAME-ORIGINAL-OPERATORS source theorem:
\[
\text{original Book Cost price}\longrightarrow
\text{all original path-flow Euler/Schur}\longrightarrow
\text{original hidden-to-future archive }F_A.
\]
It is proved for the **scalar macro-action and symmetric native Cost probe**. The resolvent spectral parameter used separately in the prior self-energy owner is NOT inserted here or misidentified with physical time; the present identity uses its canonical F_A only.

## 4. NEGATIVE hostile control: original directed cycle Cost source produces historical curvature wholly invisible to future rank32

At the SAME original symmetric reference transition P, take a directional probe of the EXISTING directed primitive Cost fiber, with \(d^\circlearrowright_{uv}=+1\) on K9→K11, K11→K13, K13→K9, \(-1\) on all reversed directed zone transitions. This is a **probe of original directed edge costs**, NOT an assertion that original full physical D0 allows reversal-odd field variations. Then \(d_{vu}=-d_{uv}\), and original detailed balance \(f_{uv}=f_{vu}\) gives \(c=0\).

The Poisson-corrected innovation is also edge-antisymmetric \(m_{uv}=-m_{vu}\). Its outgoing native conditional means vanish by §2, AND its INCOMING conditional means vanish by edge reversal:
\[
J_0^\top g=J_1^\top g=0.
\]
Thus
\[
\boxed{
g\in\operatorname{ran}Q_A\cap \operatorname{ran}(\mathcal R)^\perp,
\qquad
\mathcal R^\top g=0,\quad g\ne0.}\tag{7}
\]
The native future archive rank32 misses this source entirely, although it is a true historical flow innovation. It is nonzero because the ORIGINAL oriented A→B→C→A 3-edge loop has d-circulation +3, whereas the opposite cycle has −3; no constant-plus-vertex-coboundary can satisfy both.

On all original718 edges, independent matrix arithmetic verifies
\[
\boxed{
D_{tt}^2\mathcal A_{\rm eff}(0)
=-\ln\varphi\|g\|^2
=-0.4763744515526456\ldots<0, \quad
\|\operatorname{Proj}_{\mathrm{ran}\mathcal R}g\|^2<10^{-25}.
}\tag{8}
\]
The original present-only archive has rank 685; the future-populated \(\mathcal R\) has rank32; therefore this genuine currently-invisible but future-\(\mathcal R\)-dark subspace has dimension \(685-32=653\).

**Do not promote (6) to a universal equality between whole scalar Book history relaxation and the 32-dimensional F_A energy.** It fails exactly on (7)–(8) IF reversal-odd directed Cost directions are admitted. A true physical selector must EITHER prove a source-domain restriction excluding these odd probes, OR retain/source-balance the remaining 653-dimensional original archive. Dropping them in a signed GR variation without a Ward/theorem is invalid. The difference is mathematical and exact, not a numerical rounding effect.

## 5. What has actually been closed, and the single missing physical binding

**PROVED from the real scene/cost operators:** full historical Hessian = original full archive squared norm (1) and isomorphism (2); exact general finite Poisson innovation Schur (3)–(4); real original symmetric AB edge-Cost second source IDENTICAL to original rank32 native feedback (5)–(6); and an exact reversal-odd source family completely outside that rank32 feedback (7)–(8). These are independent of adding an action or deciding a G, Λ or matter coefficient.

**Still OPEN:** deriving from original actual executed and paid D0 verification/Book programme WHICH 4D coframe16+Lorentz24+CAR+preparation+clock variations induce WHICH original \(d_{uv}\), whether reversal-odd Cost probes are physically admissible, and which full noncommutative memory/coherent Book action is selected. There is no actual proof that its same-action full \(G_{ab}-T_{ab}\) tensor source equals zero, nor that the original microstructure selector/RAW-216 gap is removed. **GR_closed=false.**

A sharp two-outcome physical theorem gate now replaces more census: identify the original field→directed primitive Cost source map \(V\mapsto d_V\); either its image in the native Poisson archive is proved to live in \(\operatorname{ran}\mathcal R\) (then scalar history Schur is exactly the existing F_A on every admitted field tangent), or it has a nonzero component in the 653 dark archive (which is a necessary additional native physical source, unless an independently proved same-programme cancellation removes it). Both are finite operator checks. The full noncommutative Book memory-price gate remains separate and unavoidable.

Standalone replay: [\`check_native_book_archive_poisson_exact_source.py\`](sources/d0_physical_binary_return_2026-10-19/check_native_book_archive_poisson_exact_source.py). It builds the original all718 P,π,J0,J1 from native canonical Cost=1, computes unique Poisson solutions, checks original α/χ identity and archive norms, and verifies the exactly signed antisymmetric cycle dark-channel witness. This is a 33+718 finite calculation, NOT a native 4D Einstein action computation.


## 6. NEW stronger terminal: even reversal-SYMMETRIC original Cost sources are future-dark unless they come from vertex sums

The directed cyclic counterexample §4 could in principle be excluded if the physical Cost law forced \(d_{uv}=d_{vu}\). This DOES **NOT** remove the problem. We now prove an exact necessary-and-sufficient visibility theorem on the actual connected reversible original scene.

**Theorem.** At the existing equal-cost symmetric K(9,11,13) reference, for ANY original real symmetric primitive edge Cost variation \(d_{uv}=d_{vu}\), with Poisson innovation \(g\) of §2 and original rank32 future channel \(\mathcal R=Q_AJ_1\):
\[
\boxed{
g\in\operatorname{ran}\mathcal R
\quad\Longleftrightarrow\quad
\exists\alpha:V\to\mathbb R,\ \forall(u,v)\in E,\ 
d_{uv}=\alpha_u+\alpha_v.}\tag{9}
\]
The **if** direction is §3: take \(\chi=\alpha+\xi\), use the Poisson equation and obtain \(m_{uv}=\chi_v-(P\chi)_u\), i.e. \(g=\mathcal R(\sqrt\pi\chi)\).

For **only if**, if \(g=\mathcal R h\), define \(\chi_v=h_v/\sqrt{\pi_v}\). Then \(m_{uv}=\chi_v-(P\chi)_u\), and the recovered original Cost derivative is
\[
d_{uv}=c+\xi_u-\xi_v+\chi_v-(P\chi)_u
      =a_u+b_v,\quad
a_u=c+\xi_u-(P\chi)_u,\quad b_v=\chi_v-\xi_v.
\]
Symmetry \(d_{uv}=d_{vu}\) on each actual original bidirectional edge gives \(a_u-b_u=a_v-b_v\). Connectivity of ORIGINAL K(9,11,13) forces a common constant \(k\), so \(d_{uv}=b_u+b_v+k=(b_u+k/2)+(b_v+k/2)\), precisely the asserted vertex sum. No continuum assumption, gauge, controller, extra field or nonoriginal graph is used.

**Hostile original REVERSAL-SYMMETRIC local Cost pair:** increase \(s_{0,9}\) and \(s_{9,0}\) by t, with ALL other primitive directed-edge prices unchanged. This is a genuine *probe of the existing primitive Cost fiber*, preserves edge reversal symmetry, but is NOT proven to be an admitted fundamental coframe/Lorentz field direction. It violates vertex-sum representability on the original induced 2×2 rectangle: \(d_{0,9}+d_{1,10}-d_{0,10}-d_{1,9}=1\ne0\). Therefore a nonzero dark653 historical Schur term is **forced analytically**, without relying on a floating-point result.

Full original all718 replay (using the exact existing S,J1, Perron pi,P and the UNIQUE Poisson solution) gives:
\[
\begin{aligned}
c_{\{0,9\}}&=0.0029773962030634022\ldots,\\
-\mathcal A_{\rm eff}''(0)
&=0.0015498046181079107\ldots,\\
\ln\varphi\,\|\operatorname{Proj}_{\mathrm{ran}\mathcal R}g\|^2
&=0.0002498010821445919\ldots,\\
\boxed{\ln\varphi\,\|\operatorname{Proj}_{\mathrm{dark653}}g\|^2
&=0.0013000035359633177\ldots>0.}
\end{aligned}\tag{10}
\]
Thus 83.8817694% of the relaxation curvature in this particular local symmetric source is outside the native 32 future-feedback operator. The projector is computed with the mathematically justified rank32 singular spectral gap (discarding the exact stationary zero singular value); an unrestricted floating-point pseudoinverse across this zero mode would be invalid.

**Stronger finite physical two-outcome gate:** even a claim that **all reversal-even** original Book Cost sources can be integrated using ONLY current 33-visible→future rank32 \(F_A\) is FALSE. To obtain that reduction on an actual 4D/coframe/CAR tangent domain, independently prove the stronger **vertex-sum factorization**
\[
D_Vs_{uv}=\alpha_V(u)+\alpha_V(v)
\quad\text{for every original physical field tangent }V,
\]
or else include and physically price the proven dark archive term. Imposing only \(D_Vs_{uv}=D_Vs_{vu}\) is not enough. The requisite physical 4D field→original edge-cost ownership and full Book03 noncommutative history/action selection are STILL OPEN; therefore this is not an Einstein or global D0 no-go. \`GR_closed=false\`.

The finite companion script now includes this reversal-even hostile case, its original 2×2 rectangle violation, and the stable rank32/dark653 orthogonal Schur split.
