# D0→GR: an EXACT and UNIQUE finite-history Book03 vertex-Info binding from original BORN weights and local Shannon gain — solved by a native backward Bellman/Doob potential, with a sharp pathwise-surprisal NO-GO

22 October 2026 · SAME scientific Draft PR #334 / constitutive native programme. **Constructive new foundational/scalar whole-history closure conditional on TWO explicitly testable Book03 operational premises**, not a new free action or entropy fit. It consumes original Book03 §§03.3.0–03.3.0a \(w_\gamma=\varphi^{-\sum(c-I)}\), the original \(p+p^2=1\) exact F/R \(0/10\) costs and normalized CAR16/full128 Julia/Kraus Born process (including genuine nonreset DATA memory), the already OWNED Book source-binding absolute-amplitude/scalar/marker distinctions, the unique Book06 conditional maxentropy observable algebra, and the new original quantum nonreset first-return transfer-log counterexample. **Mathematically the remaining vertex information allocation is now unique on every supplied finite tree. Physically M1/Book03 has NOT yet proved that its absolute scalar history weights must coincide with the independently generated Born law AND that its vertex gain means locally expected Shannon entropy, nor that signed individual information increments are allowed; the compulsory geometry SCENE Hodge, task/cost, controller/oldRIGHT and 42-Euler remain OPEN. \`GR_closed=false\`.**

## 1. Exact whole-tree Book action — two requirements and no fitted weight

Fix ONE physical finite rooted *prefix tree* of complete histories (including STOP/MATCH/FAIL/ABORT leaves), with true native input \(\Omega_y\), normalized strictly positive on its active true output support. Every nonzero branch \(u\to ub\) has its **actual** conditional Born probability
\[
P_y(b\mid u)>0,\qquad \sum_{b\mid u}P_y(b\mid u)=1,
\]
calculated from the ORIGINAL sequential Kraus maps (there is NO iid reset), and its actually declared charge \(c_y(u,b)\) in ORIGINAL Golden units; additional factory/clock/preparation work is not assigned zero by merely declaring a partial port ledger. Write
\[
h_y(u)=-\sum_bP_y(b\mid u)\log_\varphi P_y(b\mid u),\quad
\bar c_y(u)=\sum_bP_y(b\mid u)c_y(u,b).
\]
The original Book03 POSITIVE scalar-history binding and its local "gain in distinguishing a registered outcome" motivate TWO separately stated constraints:

**(BORN)** Normalizing the literal Book03 weights \(W_y(\gamma)=\varphi^{-S_y(\gamma)}\), \(S_y(\gamma)=\sum_{u\to ub\in\gamma}[c_y(u,b)-I_y(u,b)]\), must reproduce the SAME actually generated complete native Born law \(P_y(\gamma)\):
\[
\boxed{P_y(\gamma)=W_y(\gamma)/Z_B(y),\quad
 Z_B(y)=\sum_{\gamma\,{\rm leaf}}W_y(\gamma).}\tag{1}
\]
This is the missing SAME-EXECUTION *absolute scalar-probability* identification, not a consequence of the Hilbert return determinant.

**(GAIN)** The native vertex information is an OUTCOME-DEPENDENT realized quantity whose **conditional expected** gain at EACH actually visited prefix equals the Shannon reduction of its declared fully retained distinguishable next symbol:
\[
\boxed{\sum_bP_y(b\mid u)\,I_y(u,b)=h_y(u).}\tag{2}
\]
This conditional expectation is the precise Shannon reading of Book03's English "a committed choice lowers uncertainty entropy". It does NOT assume the *realized* gain is the ordinary surprisal \(-\log_\varphi P(b\mid u)\); that STRONGER claim is disproved in §4 for actual original Golden nonblank records.

## 2. THEOREM A — unique native Bellman/Doob potential solves ALL Book leaf weights AND EVERY vertex entropy gain

Put \(f_y({\rm leaf})=0\), and at EVERY nonterminal prefix compute the entirely native finite backward recurrence
\[
\boxed{
f_y(u)=2h_y(u)-\bar c_y(u)
       +\sum_bP_y(b\mid u)f_y(ub).
}\tag{3}
\]
Assign the **derived** Book03-style per-edge information
\[
\boxed{
I_y(u,b)=c_y(u,b)+\log_\varphi P_y(b\mid u)
          +f_y(u)-f_y(ub).
}\tag{4}
\]
**Theorem.** (3)–(4) are the ONE AND ONLY REAL solution of (BORN)+(GAIN) on the whole given finite positive probability tree, up to physically unvisited zero-probability branches where no gain is observable.

*Proof of existence.* Summing \(c-I\) along a completed native path \(\gamma\) telescopes every internal f:
\[
S_y(\gamma)=
 -\log_\varphi P_y(\gamma)-f_y(\emptyset).
\]
Thus the entire Book path weight is
\[
\boxed{
W_y(\gamma)=\varphi^{f_y(\emptyset)}P_y(\gamma),
\quad Z_B(y)=\varphi^{f_y(\emptyset)},}
\tag{5}
\]
which proves (BORN) for **ALL completed paths simultaneously** (even when the output law is quantum-history-dependent). At a node, (4) gives
\[
\mathbb E[I\mid u]=
\bar c-h(u)+f(u)-\sum_bP(b|u)f(ub)=h(u)
\]
by (3), proving (GAIN). No hand-picked entropy coefficient or arbitrary Book normalizer is left.

*Proof of uniqueness.* (BORN) implies a GLOBAL common path normalization \(J(y)=\log_\varphi Z_B\). On a rooted tree, any edge assignment yielding the same path action necessarily has a potential \(f\) with leaf boundary \(f({\rm leaf})=0\), \(f(\emptyset)=J\), and is of the form (4): define f(u) from the remaining pathwise telescoping value. (GAIN) forces (3). Backward induction from the terminal f=0 gives a UNIQUE f on every reachable node, and hence a unique I. The previously exposed Book vertex endpoint/coboundary gauge is **fixed by the per-prefix expected-gain condition**; a single expectation only at the ROOT would NOT remove that gauge. The Bellman f is future conditional on the declared actual task, so computing it as a physical per-vertex controller is itself an ADMISSIBILITY/charged-work question, not a free finite graph oracle.

The genuine total joint informational normalization and action satisfy **for the entire complete original measured history**:
\[
\boxed{
\begin{aligned}
f_y(\emptyset)
 &=2H_\varphi(P_y)-\mathbb E_{P_y} C_y,\\
\mathbb E\sum_{\gamma} I_y &=H_\varphi(P_y),\\
\mathbb E_{P_y}S_y
 &=\mathbb E_{P_y}C_y-H_\varphi(P_y),\\
D_y f_y(\emptyset)
 &=2D_yH_\varphi(P_y)-D_y\mathbb E C_y .
\end{aligned}}\tag{6}
\]
Here \(\mathbb E\sum_\gamma I\) denotes expectation of the SUM of the visited vertex increments; \(H_\varphi(P_y)\) is the ENTROPY OF COMPLETE STOPPED FINE LEAF RECORDS, not the one-port marginal or a fresh iid surrogate. These follow from Shannon chain rule and the exact Book root value. For independent truly paid/product programmes, both f(root) and all complete net code prices are additive; the original Book multiplicativity is preserved WITHOUT a fitted new coupling.

**Original full moving source, no field/input loophole.** Each true native \(D_yP(b|u)\) includes the full original \(D K_\alpha\), \(D\Omega\), past conditional quantum filtering and actual label/readout derivatives. Differentiating (3) on every real smooth positive native field chart gives the native backward first-source recursion
\[
\boxed{
\begin{aligned}
D f(u)
=&2D h(u)-D\bar c(u)
 +\sum_b[DP(b|u)\,f(ub)+P(b|u)D f(ub)],\\
D I(u,b)
=&D c(u,b)+\frac{DP(b|u)}{P(b|u)\ln\varphi}
   +D f(u)-D f(ub).
\end{aligned}}\tag{7}
\]
No independent input, controller/clock reaction or Lorentz/CAR component is frozen; no numerical eigenvector gauge is used. Singular birth/dark branches require their ordinary zero-probability support limit (e.g. the separately owned \(r^2\log r\) theorem); do NOT divide by 0 at a rank boundary.

## 3. Theorem B — genuine infinite no-reset first-return task has a UNIQUE bounded Bellman VALUE even when DATA histories are correlated

For the REAL unmodified ORIGINAL full128 PORT-first-return controller, fix anchor a and let \(X\) be a quantum DATA density state with the ACTUAL still-retained fine work archive outside the controller's future test. Let
\[
q_\alpha(X)=\operatorname{Tr}K_\alpha X K_\alpha^\dagger,\quad
X_\alpha=K_\alpha X K_\alpha^\dagger/q_\alpha(X)
\]
for positive branches. Define the actual fine one-step conditional information-cost imbalance \(g(X)=2H_\varphi(q(X))-\sum_\alpha q_\alpha(X)c_\alpha\) for the truly declared fine next-symbol charge \(c_\alpha\). For instance \(c_\alpha=1+(\alpha\bmod2)\) is the ORIGINAL literal PORT-only charge, with any additional original fine/factory stage costs separate and still required.

The native infinite-horizon continuation value \(f_a(X)\), **conditioned on having already anchored PORT a**, solves the *nonlinear quantum-filter Bellman equation*
\[
\boxed{
f_a(X)=g(X)+
 \sum_{\alpha:\,b(\alpha)\ne a}q_\alpha(X)f_a(X_\alpha).
}\tag{8}
\]
All actual successful match labels terminate with 0 child value; all original 128 nonmatch fine records are retained on the executed branch. On the true original positive effect chart \(\mathcal I_a^*(I)\succeq\eta_a I\) with \(\eta_a>0\), the operator \(\mathcal B_a\) defined by the RHS contracts the sup norm of bounded real f by at most \(1-\eta_a\), because
\(\sum_{\alpha:b(\alpha)\ne a}q_\alpha(X)\le1-\eta_a\) for EVERY quantum state X. By Banach,
\[
\boxed{
f_a\text{ exists and is UNIQUE among bounded value functions},\quad
\|f_a\|_\infty\le\|g\|_\infty/\eta_a .
}\tag{9}
\]
The full root f for the first (unanchored) trial is
\[
f_{\emptyset}(\rho)=g(\rho)+
  \sum_\alpha q_\alpha(\rho)\,f_{b(\alpha)}(\rho_\alpha),
\]
and, by bounded truncation and the old actual quantum stopping entropy identities, \(f_\emptyset=2H_\varphi(\Gamma_{\rm stopped})-\mathbb EC_{\rm stopped}\). This is a **genuine original all-fine no-reset quantum predictive value**: no exponential-size infinite word list is required to DEFINITELY specify or prove its unique existence. It does NOT assume a finite classical HMM state catalogue; the normalized posterior X traverses a generally infinite quantum-state continuum. Value convergence is state-uniform geometric. Ordinary first-source differentiation on a rank-stable regular chart is computed for finite caps by (7); an infinite-source limit needs the TRUE previously derived \(\eta\)/Kraus-jet C1 bounds and actual fine-history entropy positivity conditions, not naive differentiation of a value-tail statement. In particular the separately proved native harmonic transfer \(-\log(I-\mathcal T_a)\) is a different payoff than g; its source is NOT automatically the entropy Bellman value.

## 4. THEOREM C — choosing ordinary outcome surprisal as Book03 Info DOUBLE-COUNTS native Born probabilities

If instead one makes the superficially obvious stronger pathwise assignment \(I_\gamma=-\log_\varphi P_\gamma\) on a complete leaf, with the TRUE original history charge \(C_\gamma\), the weight would be
\[
W_\gamma=\varphi^{-C_\gamma+I_\gamma}
=\frac{\mu_\gamma}{P_\gamma},\qquad \mu_\gamma=\varphi^{-C_\gamma}.
\]
Requiring Book's NORMALIZED positive scalar weight to equal this same Born law therefore forces
\[
\boxed{
P_\gamma^2=\mu_\gamma/Z_B,\quad
P_\gamma=\frac{\sqrt{\mu_\gamma}}{\sum_\eta\sqrt{\mu_\eta}}
}\tag{10}
\]
and hence generally ERASES real quantum CAR/Born source variation. This is a **foundational mathematical self-consistency no-go for the NAIVE pathwise-surprisal absolute-weight reading**, NOT for all possible Book03 vertex gains. It applies on ANY full fine prefix tree with positive probabilities and original native literal costs. One must distinguish (i) an actual outcome's surprisal \(-\log P\), (ii) the locally EXPECTED entropy reduction, and (iii) a Book absolute path weight/gain rule.

**The exact ORIGINAL nonblank Golden PORT diagnostic:** The true unchanged native CAR16 full128 j>0 pair has Born \(P=(p^2,p)\) and actual 0/10 code weights \(\mu=(p,p^2)\), with c=(1,2). Plugging the ACTUAL surprisal into (10)'s would-be weights gives
\[
\widetilde P=\frac{(p/p^2,\ p^2/p)}{p/p^2+p^2/p}
=\frac{(1/p,p)}{1/p+p}
\simeq(0.7236067977,\ 0.2763932023),
\]
NOT the genuine original Born \((0.3819660113,\ 0.6180339887)\). The *only* self-consistent fixed-point P under this wrong scheme is \(\sqrt\mu/\sum\sqrt\mu\approx(0.5598629615,0.4401370385)\), also not original Born. The forced relative information gain for the correct scalar-Born binding must instead satisfy
\[
\boxed{
I_1-I_0=(c_1-c_0)+\log_\varphi(P_1/P_0)=2,
}\tag{11}
\]
whereas naive surprisal gives \(I_1-I_0=-1\): a STRICT THREE Golden code-unit contradiction. The older Book scalar vs amplitude vs extra-Kraus marker source-binding theorem independently proves different necessary differences (2, 3/2, 1), respectively; (10)–(11) is the new WHOLE-TREE Bellman selection/anti-double-counting consequence for the absolute scalar law.

For this exact native TERMINAL pair, (3) gives \(f(\emptyset)=3p^2\), \(I_0=3p^2-1\approx0.1458980\), \(I_1=1+3p^2\approx2.1458980\). Both are NONNEGATIVE; their true expected gain is \(2-p\) Golden units, and the normalized Book weights are EXACT original \((p^2,p)\). No new \(\ln q\) coefficient is fitted.

**A sharp admissibility veto on extremely rare native reporters.** For an arbitrary complete binary native report \(P=(1-r,r)\) with the REAL original costs (1,2), the SAME unique Bellman law gives
\[
\boxed{
f(\emptyset)=2h_\varphi(r)-1-r,\quad
I_1=2+\log_\varphi r+f(\emptyset).
}\tag{12}
\]
Since \(h_\varphi(r)\le\log_\varphi2\) and r>0,
\(I_1<1+\log_\varphi r+2\log_\varphi2\).
For EVERY sufficiently rare \(r<\varphi^{-5}\) this is STRICTLY NEGATIVE. The true original cap-one N1 reporter is far below this threshold. Therefore, if Book03/M1 additionally insists on **NONNEGATIVE realized per-branch Info gain for every physically positive original outcome**, then the THREE simultaneous requirements (BORN),(GAIN),pointwise \(I\ge0\) are INCOMPATIBLE with the native rare-Golden N1 report. If signed realized relative gain is admitted, the exact Bellman solution (3)–(4) remains consistent, with conditionally POSITIVE expected information. This is an explicit causal/sign *physical admission gate*, not license to choose another entropy reward by fiat.

## 5. Actual SAME old CAR16/full128 TWO-round no-reset replay — all 16,384 positive/dark slots retained

For the literal original \(\rho_{\rm DATA}=I_{16}/16\) mathematical input (requires a real paid preparation), real proper boost \(r=1/9\), \(\nu=3/5\), phases \((i,i,-1,-i)\), and the actual complete original 128 Kraus matrices:
\[
P_{\alpha\beta}
=\frac1{16}\|K_\beta K_\alpha\|_F^2,\quad
\sum_{\alpha,\beta}P_{\alpha\beta}=1.
\]
Only the declared **original terminal PORT charges** \(c_\alpha=1+(\alpha\bmod2)\) are placed in this TWO-tick partial Cost ledger; the physically distinct original row/factory/clock/oldRIGHT costs are NOT called zero or erased from the underlying full tape. The exact numerical direct original CAR replay of the finite-tree theorem yields:
\[
\boxed{\begin{array}{ll}
H_\varphi(P_{\alpha\beta})&\simeq0.5701407300473663,\\
\mathbb EC_{\rm port,2}&\simeq2.0260945042476832,\\
f(\emptyset)&\simeq-0.8858130441529515,\\
Z_B=\varphi^{f(\emptyset)}&\simeq0.652944130448109,\\
\mathbb E S_{\rm Book,partial}&\simeq1.455953774200317,\\
\max_{\alpha,\beta}|P_{\alpha\beta}-W_{\alpha\beta}/Z_B|
&<3.4\cdot10^{-16}.
\end{array}}\tag{13}
\]
The full 128×128 complete CORRELATED conditional native tree obeys ALL 64 actually positive first labels, all 4096 positive two-label words, and all 12,288 original zero fine-word slots are retained. At EVERY positive nonterminal native prefix, its expected per-vertex Bellman Info agrees with the exact local conditional Shannon to \(<5\times10^{-16}\); the ENTIRE expected Book Info equals H(P) to roundoff, and the entire partial Cost−Info equals the ACTUAL Cost−measured-Shannon without extra factor. The originally generated native probabilities remain UNCHANGED and the first DATA output is actually propagated to the second (no reset).

**Decisive sign:** Some realized rare full128 edge gains in this consistent Book allocation are about \(-35\) Golden units, even though the mean at EVERY active node equals its positive entropy. It is NOT legitimate to declare this full Info a physical Book03 gain without verifying whether negative realized gains are admitted, nor to assign those rare node values to a different original timing/port programme without its paid controller.

The [pinned original source verifier](sources/d0_native_book_bellman_info_2026-10-22/check_original_book_bellman.py) checks the genuine \(\mathbb Q(\sqrt5)\) one-pair law, the actual two-round original 128×16 matrices, full Bellman recursion, root partition \(Z_B\), all local entropy gains and first independent Lorentz source jets; the mathematical theorem does not depend on the numerical checks or unverified original BOOK03 M1 execution.

## 6. What is really closed and what is NOT — one decisive physical input instead of circular entropy choices

**Mathematical WHOLE-TREE Book info binding CLOSED, conditional on exactly specified (BORN)+(GAIN).** The result directly solves the previously unfixed scalar absolute Book weight/vertex Info relation on every selected original finite history, with no fitted coefficient and the correct actual nonreset quantum conditional Born probabilities. It also proves existence/uniqueness of a nonreset infinite-return finite-DATA quantum Bellman value, with a real contraction bound. No guessed independent-history entropy, Shannon-to-harmonic swap or arbitrary vertex coboundary remains INSIDE that conditional class.

**PHYSICAL original Book03 source still requires a selection**: (i) Does its \(w=\varphi^{-S}\) define the SAME normalized probabilities as the original truly executed CAR/N1 Born instrument (as opposed to a separate abstract history weighting)? (ii) Does "vertex distinguishes a choice and lowers uncertainty entropy" in §03.3.0a mean (GAIN), or a nonnegative *realized* branch gain / ordinary surprisal? These meanings are mathematically incompatible on true rare sources. (iii) Can the history-dependent backward Bellman potential be computed/represented by already admitted G0/M1 programme words with ALL actual clock, oldRIGHT, factory, data preparation and controller work paid and independent source equations checked? (iv) Does compulsory §03.25 select the matched \(P_N\), geometrical SCENE Hodge \(\Delta_N(V)\) and its \(F_N\) with the correct 42-field Einstein-CAR source and uniform genuine PF/raw216 limit?

If the original physical meaning answers YES to the first two BORN+GAIN clauses and permits signed realized Info, it now has a **unique concrete whole-history Info COMPILER TARGET**; there is NO longer a free table of per-vertex Info coefficients. But this alone does NOT equate the original Book03 Hodge+feedback action to the configured original unpadded h0 nonflat all42 root. That operator/gauge/physical writer binding remains the decisive next theorem. \`GR_closed=false\`.

