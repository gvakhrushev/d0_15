# One global golden AF record: an endogenous curvature integral WITHOUT an extensive vacuum baseline


**Physical-action correction (17 October, after the actual Book likelihood check).** This note computes the relative/PF-KL old-AF readout with source \(+0.0763194856457\,d\int f\), but that is **NOT** automatically the Book \`Cost−Info\` action on the same recorded probability law. Under the existing branch cocycle \(w=q\), the expected physical path action is Shannon \(H_\varphi(q)\), whereas the PF KL is expected path \`Info\`. A **fixed AF pointer test** and the corresponding Book-compatible second-active entropy source have now been explicitly constructed in [A4D_AF_FIXED_POINTER_BOOK_INFORMATION_SOURCE_2026_10_17.md](A4D_AF_FIXED_POINTER_BOOK_INFORMATION_SOURCE_2026_10_17.md): the correct conditional Book coefficient is \(-0.114397462642\) per normalized \(\int f\), not the KL number. Both share ONE field-independent AF baseline; neither can be silently substituted into the unchanged literal v8 \`H+J+R\`, as the [flat Dirac-zero full-instrument obstruction](A4D_AF_V8_FLAT_ZERO_MODE_INTERTWINER_BOUNDARY_2026_10_17.md) proves. The physical full-D0 GR claim still requires the actual newly admitted AF transition, the original retained v8 price/cut binding, Lorentz observer/spatial source and exact joint roots.

17 October 2026. A bounded proof consumer for Draft #334. **Goal: answer the genuine full-action cosmological-volume obstruction**, not construct a new auxiliary Einstein-looking operator. This combines existing complete native F/R cost cuts, existing 4D golden coordinate readout, and the already derived SECOND ACTIVE AF record price. One physically executed geometry-controlled AF gate and a full Lorentz/ADM readout remain explicit admission gates.

**Owners read directly:** A4D_NATIVE_GOLDEN_COST_REFINEMENT.md (p^cost, Fibonacci AF trace, full cuts); A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md §1 (four-coordinate nested golden boxes and their actual volume pushforward); A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md §§1–6 (complete four-copy AF record, exact second-price source, disjoint equal-cost Q_i, f_0 and intrinsic curvature Jacobian); A4D_RECORD_NORMAL_VOLUME_SOURCE.md (Gauss/Parseval curvature and true metric jets); A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md (full second-active record versus first-record zero covector); sources/d0_reverse_einstein_ir_2026-10-17/RESULT_RU.md (Lorentz/ADM target); A4D_IR_STATIONARITY_AND_TWO_CLOCK_FULL_GR_SOURCE_2026_10_17.md (original v8 volume-root obstruction).

## 1. Exact-cost words have NONZERO limiting total Born probability

Let \(p=\varphi^{-1}\), \(p+p^2=1\). An actual F costs one, an actual R costs two, and the literal raw cylinder weight is \(p^{\mathrm{cost}(w)}\). Let

\[
{\cal W}_n=\{w\in\{F,R\}^{*}:\mathrm{cost}(w)=n\}.
\]

The count \(c_n=|{\cal W}_n|\) obeys \(c_0=c_1=1\), \(c_n=c_{n-1}+c_{n-2}\); therefore \(c_n=F_{n+1}\). The words are prefix-free because all letter costs are positive. Their total UNNORMALIZED probability in the original golden infinite-history measure is

\[
a_n:=\sum_{w\in{\cal W}_n}\mu(w)
       =F_{n+1}p^n
       =a_\infty+\frac{(-1)^n}{\sqrt5\,\varphi^{2n+1}},
\quad a_\infty=\frac{\varphi}{\sqrt5}=0.723606797749979\ldots>0.
\tag{1}
\]

This is not the FULL cost-n stopping cut: the complementary overshooting histories of cost n+1 stay in the retained experiment and carry the remaining \(1-a_n\). No word is deleted to make the whole tape normalize; (1) is a **selected family of genuine positive subevents** within a complete cut.

Numerically at n=12 the exact-cost family has 233 words, total mass 0.723609463528..., and at n=20 it has 10946 words, mass 0.723606798958.... Its weight is nonzero at arbitrary depth. The previous *fixed-(k,r) binomial-subfamily* has asymptotic relative mass O(n^-1/2); it is NOT sufficient as the sole carrier of a nonzero continuum coupling. Use the entire exact-cost family, with varied RAW word lengths but the same actual cost.

## 2. Stronger than a counting coincidence: the selected addresses converge to Lebesgue

Use the ALREADY OWNED native address map X from A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md §1: each next raw F/R letter splits coordinate j mod 4, with child interval lengths p and p². Write X_w for the centre of the 4D box belonging to finite w, and X_infinity for its unique nested infinite-history limit. The proved full-law pushforward is \((X_\infty)_*\mu=\mathrm{Leb}_{[0,1]^4}\).

Define the positive SUBPROBABILITY measures, with no independent choice of site weights,

\[
\nu_n=\sum_{w\in{\cal W}_n}p^n\delta_{X_w}.
\tag{2}
\]

**Theorem (exact-cost renewal equidistribution).** For every bounded continuous \(f:[0,1]^4\to\mathbb R\),

\[
\boxed{\lim_{n\to\infty}\sum_{w\in{\cal W}_n}p^n f(X_w)
      =\frac{\varphi}{\sqrt5}\int_{[0,1]^4}f(x)\,d^4x.}
\tag{3}
\]

Proof, including a quantitative Lipschitz error, with no statistical/ergodic independence assumption:

* If v is a fixed prefix of raw length k and cost c(v), the exact hitting event at cost n (>2k) has probability conditioned on v **exactly** \(a_{n-c(v)}\). Thus
  \(\mu(A_n\cap[v])=p^{c(v)}a_{n-c(v)}\).
* Formula (1) gives the uniform mixing error
  \(|a_{n-c(v)}-a_\infty|\le (\varphi\sqrt5)^{-1}p^{2(n-2k)}\).
  Summing over all k-prefixes with total probability 1 proves that **every cylinder test depending on the first k letters** has selected expectation tending to \(a_\infty\) times its unconditional expectation, with exactly this bound.
* Each k-prefix box has diameter at most \(2p^{\lfloor k/4\rfloor}\). For n>2k, every exact-cost-n word extends a k-prefix. Both the selected centre X_w and the infinite endpoint share that box. Approximate a Lipschitz f by any value on each k-prefix box.
* Consequently, for \(L=\operatorname{Lip}(f)\), \(B=\|f\|_\infty\) and any \(2k<n\),

\[
\left|\int f\,d\nu_n-a_\infty\int f\,dx\right|
 \le 4L p^{\lfloor k/4\rfloor}
   +\frac{B}{\varphi\sqrt5}\,p^{2(n-2k)}.            \tag{4}
\]

Choosing \(k=\lfloor n/4\rfloor\) gives a uniform explicit geometric bound \(O(p^{n/16})\) for bounded Lipschitz families. Replacing f by a genuine smooth field derivative df gives the SAME C¹ convergence. Bounded continuous tests follow by uniform approximation.

The result is **not** a claim that the selected subprobability (2) alone is a complete recording: it has total mass a_n. Dividing by the ACTUAL computable hit probability a_n yields a normalized conditional empirical spatial measure, converging to Lebesgue without fitting a density.

Four-coordinate exact finite controls from direct weighted enumeration:

| Cost n | Count F_(n+1) | E[x_0 given exact hit] | E[x_0²] | E[x_0 x_1] |
|---|---:|---:|---:|---:|
| 8 | 34 | 0.4967219 | 0.3206100 | 0.2351376 |
| 12 | 233 | 0.4908399 | 0.3212103 | 0.2417979 |
| 16 | 1597 | 0.4962472 | 0.3292365 | 0.2471890 |
| 20 | 10946 | 0.4983187 | 0.3313064 | 0.2474902 |
| 24 | 75025 | 0.4985168 | 0.3317396 | 0.2481661 |

Limits are 1/2, 1/3, 1/4, respectively. This small finite control checks the *new renewal proof*, not a physical gravitational result.

## 3. One ACTUAL second AF complete price has a constant baseline, not B times the number of cells

At equal raw cost n the words w have varying numbers of raw F/R letters, but their *encoded Fibonacci path length is exactly n*, and every w terminates at a complete ready (state-0) encoded boundary. Therefore the pair of suffixes wFR, wRF has cost n+3, comprises two distinct complete ready leaves and the terminal type-0 block used in A4D_NATIVE_JACOBIAN_CONTROLLED_RECORD_SOURCE.md §3. Their cylinder projections

\[
Q_w=1_{wFR}+1_{wRF},\quad
Q_wQ_{w'}=0\;(w\ne w'),\quad \tau(Q_w)=2p^{n+3}
\tag{5}
\]

are defined in ONE old AF record algebra; all other terminal ready/pending states remain. The same diagonal functional calculus as §3 of that owner then permits the following **equal-COST (not equal raw letter count) extension** of its one-effect construction:

\[
E_n(\mathbf u)=p^2\left[I+\sum_{w\in{\cal W}_n}u_wQ_w\right],\qquad |u_w|\le\delta,
\tag{6}
\]

with delta inside the owner's stated uniform positivity/analyticity corridor. The total activated projection has trace
\(2p^{n+3}F_{n+1}\to 2p^3a_\infty=0.341640786499874\ldots<1\);
the original full complement never disappears.

**Finite second-price identity, in this exact equal-cost ready-block class:** the pinned f_0-coarse eigen-probability formula for the canonical second ACTIVE AF record gives

\[
\boxed{
A_{\mathrm{AF},n}(\mathbf u)=B_n+
 2p^{n+3}\sum_{w\in{\cal W}_n}
   [f_0(p^2(1+u_w))-f_0(p^2)].}
\tag{7}
\]

The argument is the same as for the owner's fixed-(k,r) family: (i) all Q_w are orthogonal in the same ready/type-0 defining block; (ii) each has exactly the same PF trace weight because cost, not word spelling, sets the canonical trace; (iii) the f_0 functional acts independently on the diagonal eigen-probabilities. No additional additive independent-test law is assumed—(7) is ONE full operator price of ONE AF program. This equal-cost extension is an ANALYTIC RESEARCH LEMMA consumed from the owner's spectrum, **not yet Lean-compiled or an independent reproduced full large-AF matrix calculation**. Physical preparation of the selected W_E remains the owner's separate admission obligation.

Here \(B_n=6+x_n f_0(p^2)+(1-x_n)f_1(p^2)\), the **single complete blank price**, fixed by the canonical trace seed and tower at the specified cut. It is independent of all u_w. Adding 1000 new inactive cells (u_w=0) changes NO field derivative of B_n. **It is mathematically incorrect to replace this ONE complete operator baseline by B_n times the number of addresses**. A term \(B_n\operatorname{Vol}(g)\) arises only if one independently selects a different action consisting of a sum of separately prepared programmes per spatial cell; that is NOT (7).

For a bounded real C¹ field f on the address cube, choose the safe geometric control

\[
u_w=t^2 f(X_w),\qquad
\kappa_{\rm AF}:=2p^5 f_0'(p^2)
              =0.105470935158494\ldots>0.
\tag{8}
\]

Taylor expansion of the same **one** f_0 price and \(\sum_w p^n=a_n\le1\) prove the uniform C¹ source expansion

\[
A_{\mathrm{AF},n}(t,f)-B_n
   =\kappa_{\rm AF}t^2\sum_{w\in{\cal W}_n}p^n f(X_w)
      +O_{C^1}(t^4)
\]
\[
\boxed{
\lim_{n\to\infty}(A_{\mathrm{AF},n}-B_n)
=\kappa_{\rm AF}a_\infty t^2\int f(x)\,d^4x+O_{C^1}(t^4),
\quad
\kappa_{\rm AF}a_\infty=0.0763194856457334\ldots .}
\tag{9}
\]

The \(O_{C^1}(t^4)\) is uniform at bounded f and df, and the n-limit is after fixing sufficiently small t; the error is NOT silently promoted to zero at fixed t. No independent geometric integration *weight* has been inserted. Crucially, the **zeroth-order vacuum part has identically ZERO metric/source jet for every finite n**, unlike the unweighted v8 feedback's O(s⁴) volume term. This is a genuine alternative native-priced **operator family**, not an illicit assertion that the old v8 H+J+R equals (7).

### 3.1. Quantitative simultaneous curvature-source and refinement limit

The two uniform C¹ estimates in §§2–3 compose without requiring a staged limit. For a bounded smooth family f and its genuine field derivatives, put

\[
{\mathscr E}_{n,t}[f]=t^{-2}(A_{\mathrm{AF},n}(t,f)-B_n).
\]

Equations (4) and (9), including the moving f-source but a fixed **address-coordinate** golden grammar, give the explicit dual C¹-chart bound

\[
\boxed{\|d{\mathscr E}_{n,t}
 -\kappa_{\rm AF}a_\infty\,d\int f(x)\,d^4x\|
 \le C\bigl(t^2+p^{\lfloor n/16\rfloor}\bigr).}
\tag{10}
\]

The same estimate holds for the value, and also when f includes a **physically derived moving geometric Jacobian** and its field source, provided its pulled-back smooth norm is uniformly bounded. Every diagonal choice \(t_n\to0,\ n\to\infty\) closes this *smooth source* bridge. To make the pure sampling remainder \(o(h^2)\), for example, it suffices to take \(n_h \ge 16(2+\gamma)\log_\varphi(1/h)\), \(\gamma>0\), up to the harmless floor factor; the tube remainder separately requires \(t_h^2=o(h^2)\). This is **not** the original unweighted raw h^-2 ten-row norm: that transfer requires a proved map from smooth source duals to the full raw metric row l1 norm, including all local high-frequency directions. No missing norm factor is silently declared one.

When the already-owned normal-volume and two-sided spatial record operator actually supplies a non-fitted f with
\(\int f\,dx=\int R_L\,dV_L\) modulo controlled boundary, (10) reads

\[
d{\mathscr E}_{n,t}\longrightarrow
\kappa_{\rm AF}a_\infty\,dS_{\rm EH}[g_L]
\]

on **all ten actual admissible ADM chart directions**. This is the precise consuming mathematical conclusion; the physical field→AF-gate admission, independent matter and exact stationary roots remain distinct.

## 4. Why this is a DIRECT Einstein consumer, not a generic scalar coincidence

The owner A4D_RECORD_NORMAL_VOLUME_SOURCE.md already gives a full 4D normal-Parseval shape-family whose \( \sum_A e_2(A_A)=R_G/2 \) (with a finite exact Jacobian and fourth-order remainder). Its source is an actual positive projector-record geometric invariant, NOT an oracle taking an arbitrary Einstein tensor as input. The owner A4D_HISTORY_DENSITY_PALATINI_SYNTHESIS.md already gives the moving native four-coordinate map and the true Jacobian for its pushforward to a physical chart.

Thus the immediate integrator substitution for (8) is **not** "set f=R_L by hand". Instead:

* encode in the SAME one AF effect the supplied 4D full-normal geometric Jacobian data at each golden address, retaining all normal settings and the time/spatial volume Jacobian, then apply (9) and the existing Gauss identity to get a positive \(\int R_G dV_G\) with NO \(B_n\,\mathrm{Vol}\) runaway;
* use the already-owned TWO-ENDPOINT normalized record comparison and curved 8+8 spatial Hodge references to derive, rather than decree, the coefficient \(-2\) for the spatial datum, with the genuine (N,shift,h) pullback and all ten first ADM sources;
* compose those derived geometric data as field-dependent controls of the ONE full AF record, keep its actual full cost/retained reference/controller/clock/preparation derivatives, and then test one nonstatic ADM chart before promoting it.

If that last admission/source equality holds, the Einstein coefficient is the **nonzero computed** \(\kappa_{\rm AF}a_\infty\) times the existing normal-Jacobian coefficient, and the extensive vacuum Euler is absent at the finite-price level rather than fitted away. Combined with the exact nonlinear ADM identity, the leading source would be \(c_{\rm AF}D\int R_L dV_L\) on **all ten metric slots** and not merely a TT sector.

**Remaining hard gate (not closed by this theorem):** can the literal D0 active/retained primitive class physically generate and CHOOSE the geometry-dependent old-AF effect W_(E_n), including old-record addressability, all complete complement records, its programme length/source, observer/coframe and reference128? A4D_NATIVE_RETAINED_RECORD_ADMISSION.md has a real one-way old-record translation invariant obstruction; existence of a right-module AF unitary is not execution permission. The spatial comparison/CAR matter/24 link equations, nonempty curved EXACT joint roots, full original unweighted ten-row h^-2 #216 and original physical Cost−Info selection remain open. Do not write "D0 derives GR" until these are discharged.

## 5. Replace the next GR work's false bottleneck

The previous "four long clocks vs one short clock" construct from A4D_IR_STATIONARITY_AND_TWO_CLOCK_FULL_GR_SOURCE_2026_10_17.md is a sharp **alternative analytic volume-free comparator**, not proof that its signs/copies are native selected. The new result (1)–(9) demonstrates a more native-priced way to evade the SAME cosmological obstruction: global trace-normalized AF reference appears ONCE and golden exact-cost addresses intrinsically carry the integral. Therefore, if the geometry-controlled SECOND AF gate can be admitted at source level, do NOT multiply its baseline by cell count or introduce a hand-subtracted volume counterterm.

**Single consuming experiment on existing integrator #334:** physically compile/deny exactly ONE geometry-controlled global AF complete record on full16 plus retained reference, and differentiate its true cost on (i) global scale/lapse trace row, (ii) nonstatic shift/shear row. The test must retain every canonical ready/pending complement and the full code/cut clock; no separate free spatial action. Only a positive admission with correct sources earns the full nonlinear Einstein conclusion. On failure, retire this route for a concrete missing primitive rather than building more unrelated curvature comparators.
