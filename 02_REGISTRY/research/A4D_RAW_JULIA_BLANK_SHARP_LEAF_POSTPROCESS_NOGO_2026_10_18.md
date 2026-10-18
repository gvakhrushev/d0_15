# D0 → GR: native Julia blank support forbids passive sharp AF-leaf readout

**Date:** 18 October 2026. **Consumer:** existing Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
**Status:** EXACT FINITE POVM THEOREM / NATIVE WEAK-HISTORY APPLICATION / PHYSICAL LEFT ADMISSION OPEN.
No CORE/BOOK/claim promotion, no new action, scalar counterterm, chosen prior, independent matter or Einstein conclusion.

## 1. Exact question and source contract

[Full-source §6.13](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md) constructs an active LEFT recording
\[
J_Y\psi=\sum_iP_i\psi\otimes|c_i\rangle
\]
with the inherited sharp leaf effects \(P_i\), including non-diagonal GNS matrix units and the RIGHT archive. This construction **changes the instrument** by accessing active LEFT wires. It does not prove the *unchanged* Julia128 outcome tape already contains those projectors.

The present question is narrower and decisive: can the finite raw Julia128 classical outcome \(\omega\), perhaps after any classical state-independent randomized decoder \(t(i|\omega)\), replace that active LEFT step and recover the \(d\ge2\) sharp projections \(P_i\) for all admitted preparations? All record outcomes, including blank, remain present. Coherent use of the still-unmeasured data, supplementary gates and state-dependent encoders are outside this theorem.

## 2. General sharp-POVM postprocessing theorem

Let \(H\) be finite-dimensional, \(\{E_\omega\}\) a complete POVM, \(\{P_i\}_{i=1}^d\) a sharp nonzero PVM on \(H\), \(d\ge2\). Suppose \(E_{\omega_*}\succeq sI\) for some \(s>0\).

**Theorem A (support no-go).** No column-stochastic classical kernel \(t(i|\omega)\ge0\), \(\sum_i t(i|\omega)=1\), can satisfy
\[
 P_i=\sum_\omega t(i|\omega)E_\omega\qquad(i=1,\ldots,d).
\tag{A1}
\]
Proof: for \(j\ne i\), compress (A1) by \(P_j\). Positivity of every summand gives \(P_jE_\omega P_j=0\) whenever \(t(i|\omega)>0\). Since \(E_\omega\succeq0\), \(E_\omega^{1/2}P_j=0\), hence \(E_\omega P_j=0\); thus \(E_\omega\) is supported in \(P_iH\). Some \(i\) has \(t(i|\omega_*)>0\), but a strictly positive \(E_{\omega_*}\) cannot be supported in a proper \(P_iH\). Contradiction.

**Theorem B (uniform quantitative no-go).** For any decoder, select a leaf \(j\) minimizing \(t(j|\omega_*)\), so \(t(j|\omega_*)\le1/d\). On every normalized \(\psi\in P_jH\),
\[
\begin{aligned}
1-\Pr_{\rm decoded}(j|\psi)
&\ge (1-t(j|\omega_*))\langle\psi,E_{\omega_*}\psi\rangle\\
&\ge s(1-1/d).
\end{aligned}\tag{A2}
\]
The left side is the total variation distance from the sharp leaf law \(\delta_j\). The bound is minimax sharp for the control POVM \(E_*=sI\), \(E_i=(1-s)P_i\): distribute the blank event uniformly among the \(d\) leaves.

**Scope of preparation.** (A1) also follows when equality of Born distributions is assumed merely on an open neighborhood of one faithful density: linearity forces equality of effects. (A2)'s worst-leaf formulation requires the leaf-supported preparations to be in the tested domain. Neither theorem identifies the physical Julia carrier with AF GNS: if an admitted isometric common-carrier map \(V:H_{\rm AF}\to H_{\rm Julia}\) is supplied, then \(V^\dagger E_*V\succeq sI_{\rm AF}\), and both results hold on its pullback without importing an isomorphism by name.

## 3. Consume the actual native 128-word blank

The actual full original Julia/golden source [§8.19](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md) retains all 128 Kraus outputs, with literal one-round blank amplitude
\[
B_\nu=I-2p^2\nu^2A_0^2,\quad p=\varphi^{-1},\quad A_0=A_0^\dagger,\quad\|A_0\|\le R.
\tag{A3}
\]
The nonblank port1 with blank coefficient-label is **not** the all-blank word. For exactly \(m\) recorded rounds the one all-blank Kraus operator is \(B_\nu^m\); its effect is \(E_*=B_\nu^{2m}\). In the declared strict contraction chart, \(0<2p^2\nu^2R^2<1\), spectral functional calculus yields
\[
E_*\succeq s_{m,\nu,R}I,\qquad
s_{m,\nu,R}:=(1-2p^2\nu^2R^2)^{2m}>0.
\tag{A4}
\]
Tensoring the old reference128 does not remove this floor. Consequently a *passive classical decoder of the unmodified raw tape* cannot implement the sharp inherited LEFT PVM exactly for any finite \(m\).

More strongly, on a family \(m\nu_m^2\to T\in(0,\infty)\) with one uniform \(R\),
\[
s_{m,\nu_m,R}\longrightarrow e^{-4p^2R^2T}>0,
\qquad
\liminf\sup_{\text{admitted leaf inputs}}
\mathrm{TV}(q_{\rm decoded},q_{\rm leaf})
\ge(1-1/d)e^{-4p^2R^2T}.
\tag{A5}
\]
This rules out **uniform passive approximate leaf recovery** at this finite-\(T\) weak-record scaling, even though the number of raw outcomes \(128^m\) grows. At fixed \(\nu>0\) with \(m\to\infty\), (A4) may instead decay to zero, so (A5) is not a no-go for that separate scaling. No unproved uniform \(R\) across a growing full spatial grid is assumed.

Independent counting control: a classical raw tape with at most \(128^m\) possible labels cannot even have \(d>128^m\) disjoint sharp target outcomes under deterministic postprocessing. The full-support obstruction above is stronger: it remains when \(128^m\ge d\).

## 4. Actual information-source consequence: measuring LEFT adds an indispensable event

Retain the active LEFT copy \(Y\) of [§6.13](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md), then register the original raw tape \(\Omega\). Take the faithful block-diagonal input
\[
\rho_*=\frac1d\sum_i\frac{P_i}{\mathrm{rank}P_i}
\]
on the common-carrier interface. It has \(\Pr(Y=i)=1/d\), and the raw \(\Omega\) marginal is unchanged by the prior sharp PVM because \([\rho_*,P_i]=0\). At the all-blank word,
\[
q(i,\omega_*)=\mathrm{Tr}(\rho_*P_iE_*P_i)\ge s/d.
\]
Since \(q(\omega_*)\le1\), \(q(i|\omega_*)\ge s/d\). Write this conditional law as \(s\,\mathrm{Uniform}_d+(1-s)v\). Entropy concavity and \(q(\omega_*)\ge s\) give the **finite entropy-gap lower bound**
\[
\boxed{H(Y,\Omega)-H(\Omega)=H(Y|\Omega)\ge s^2\log d>0.}
\tag{A6}
\]
No erased failures or assigned KL action occur. The value gap is in natural entropy units; for the declared SAME-history Book \(\mathrm{Cost}-\mathrm{Info}\) expectation, divide by \(\log\varphi\).

This is not automatically a **geometric first-source** difference at every root. There is, however, an explicit source control: if the native Kraus effects are scalar multiples of \(I\) on a preserved leaf subspace, the raw tape is statistically independent of \(Y\). Then
\[
H(Y,\Omega)-H(\Omega)=H(Y).
\tag{A7}
\]
For two leaves with preparation weights \((r,1-r)\) and any admissible tangent \(\delta r\),
\[
D[S_{\rm with\,Y}-S_{\rm without\,Y}]
=\frac{\log((1-r)/r)}{\log\varphi}\,\delta r,
\tag{A8}
\]
which is nonzero at \(r=3/10\), \(\delta r\ne0\). This proves the missing leaf-history source is *not identically zero* as a functional of preparation, while not asserting that an arbitrary \(\delta r\) is a physical metric tangent.

## 5. Parent conclusion: not a GR no-go, but one physical input is mandatory

This result does **not** refute the exact CNOT LEFT realization §6.13; that operation modifies the instrument before registering the tape and retains a new output. It does **not** refute a sufficiently strong coherent quantum decoder acting on retained data, or a separately admitted additional physical measurement, or a different large-time scaling.

It **does** rule out a concrete shorter physical arrow:
\[
\text{unchanged raw Julia128 classical tape}
\ \not\Longrightarrow_{\rm classical\ decode}\
\text{complete sharp inherited LEFT address record}.
\]
Therefore the conditional full-fine stationary profile \(\Gamma=\log\sum_i[1+2e^{h(e_i)}]/\log\varphi\) cannot be declared the unchanged native128 physical price merely by relabeling histories. An actual active LEFT recording programme or a distinct physical decoder is required; its admitted control, preparation, information contract and whole-work source must be carried into the same Euler system. Source-preserving compilation and finite-\(T\) GR recovery cannot bypass this condition by increasing \(m\).

The next **positive** consuming proof is now sharp: provide an admitted *active* LEFT path operation on the real Fibonacci GNS together with full same-history Book normalization and controlled field/work source, and show the profile's preparation variation image actually contains the required leaf contrasts. If this cannot be forced, keep the weighted scalar/Brans-Dicke-like branch rather than promoting conditional vacuum GR.

## 6. Exact reproducibility and negative controls

`python3 02_REGISTRY/research/certificates/a4d_raw_julia_blank_leaf_postprocessing_check.py`

The script verifies the literal Julia two-leading-row completeness identity in \(\mathbb Q(\sqrt5)\), strict finite blank floors, the nonzero finite-\(T\) limit, the optimal 2-leaf saturating POVM control and the nonzero entropy-source contrast. The analytic proofs above apply to arbitrary finite-dimensional POVMs and every native 128 Kraus word, not just its two-mode diagonal test. No full Lean, huge raw-history enumeration or unrelated GR suite is claimed.


## 7. Stronger same-AF theorem: the old bimodule recorder cannot see noncentral LEFT leaves

The previous blank theorem addresses the raw **Julia128** tape and requires a stated common-carrier pullback. There is a distinct, stronger exact obstruction already on the **native Fibonacci AF/GNS carrier**, with no Julia/AF identification.

In [A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md](A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md), §2–3, the four native maps \(V_j\) intertwine *both* old left and old right matrix multiplication. Their range projection \(R=VV^\dagger\) therefore reduces the two old represented *-algebras. The actual full working-operator maps are
\[
W=V(U\otimes I)V^\dagger+(I-R),\qquad
P_f=V(P\otimes I)V^\dagger,\qquad
B_f=V(B_0\otimes I)V^\dagger .
\tag{A9}
\]
Consequently all three operators commute with the entire old LEFT algebra \(L(A_n)\) **and** old RIGHT algebra \(R(A_n)\). So does every finite word or instrument effect built solely from them and apparatus-only controls that also commute with the old LEFT action. This is exact for every number of rounds, not an IR statement.

For \(A_n=M_a(\mathbb C)\oplus M_b(\mathbb C)\), consider two distinct diagonal minimal projections \(P_i,P_j\) in one simple block of size at least two, transported into the fine GNS. Choose the old LEFT unitary \(U_{ij}=L(\mathrm{swap}_{ij})\). It exchanges their subspaces:
\[
U_{ij}P_iU_{ij}^\dagger=P_j,\qquad P_iP_j=0.
\]
Any effect \(F_i\) constructed by classical postprocessing of the neutral recorder satisfies \([F_i,U_{ij}]=0\). The operator norm therefore obeys
\[
\boxed{
1=\|P_i-P_j\|_{\rm op}
\le\|P_i-F_i\|_{\rm op}+\|F_i-P_j\|_{\rm op}
=2\|P_i-F_i\|_{\rm op}.
}
\tag{A10}
\]
Thus
\[
\boxed{\|F_i-P_i\|_{\rm op}\ge\tfrac12}
\]
for **every** old-bimodule-neutral recording protocol, no matter how many neutral rounds are executed. Some normalized input then differs in the target Born probability by at least \(1/2\). This is a stronger obstruction than (A5), but applies to the narrower, genuinely old-bimodule-neutral AF apparatus class. It does not prohibit measuring central block projectors, which already commute with all old LEFT operators; it requires a noncentral leaf and thus a block with dimension at least two.

This identifies the minimal algebraic type of an admissible repair without demanding new physics by notation. A real LEFT-addressing operation \(C_Y=\sum_iP_i\otimes X^{c_i}\), with distinct codes, satisfies
\[
[C_Y,R(A_n)\otimes I_Y]=0,\qquad
[C_Y,L(A_n)\otimes I_Y]\ne0.                             \tag{A11}
\]
It is **RIGHT-linear but not LEFT-neutral**. Exactly this class is realized *conditionally on active LEFT wire addressability* by [full-source §6.13](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md). The canonical unmodified \(W,P_f,B_f\) cannot substitute for it; the full right-module endomorphism algebra permits the operation mathematically but does not select its physical performance or whole-work price.

**Strategic fork:** the remaining execution/admission lemma is no longer “does Fibonacci memory exist?” or “does Julia have enough outcomes?”. It is the specific operational forcing/admission of a **RIGHT-preserving, LEFT-sensitive** test, plus the actual SAME-history price and its stationary preparation. If D0 only admits old-bimodule-neutral record operations, its full fine-leaf source (13n) is not physically derivable by passive recording, and the non-Einstein \(\chi\) branch remains. If such an active test is admitted and physically selected, the previously proved source-preserving construction supplies the needed next conditional step; matter and global GR still remain.

**Independent exact control:** on \(H=\mathbb C^2\otimes\mathbb C^2\) set \(P_i=|i\rangle\langle i|\otimes I\), \(U=X\otimes I\), \(F=I\otimes D\), \(0\preceq D\preceq I\). Then \([F,U]=0\), \(UP_0U^\dagger=P_1\) and \(\|F-P_0\|_{\rm op}\ge1/2\), with equality at \(D=I/2\). This is a finite control of (A10), not a replacement for the general bimodule intertwining already proved upstream.


## 8. Exact remaining preparation rank: right-center conservation prevents choosing both AF block masses

The sharper joint consequence is **not** just that the old instrument cannot measure a noncentral LEFT leaf: its fully retained *right-module* dynamics cannot **prepare** the full stationary leaf simplex from an arbitrary prior right-sector marginal. This identifies a single additional independent physical weight direction.

At level \(N\), [the tower owner](A4D_NATIVE_AF_TRACE_PREPARATION.md) has
\[
A_N=M_{a_N}(\mathbb C)\oplus M_{b_N}(\mathbb C),\quad
a_N=F_{N+2},\ b_N=F_{N+1},\ d_N=a_N+b_N.
\]
The two block-central projections \(Z_X=(I_{a_N},0)\), \(Z_Y=(0,I_{b_N})\) act identically from LEFT and RIGHT on the respective GNS direct-sum sectors. In particular \(Z_X\in R(A_N)\). Every complete instrument with Kraus operators \(K_\omega\in R(A_N)'\) obeys
\[
\begin{aligned}
\mathcal T^*(Z_X)
&=\sum_\omega K_\omega^\dagger Z_X K_\omega\\
&=Z_X\sum_\omega K_\omega^\dagger K_\omega=Z_X.
\end{aligned}\tag{A12}
\]
Thus its **unconditional** \(X/Y\) masses are exact conserved quantities. All work/failure exits must be included for (A12). Conditional success marginals may differ, but their failure complement carries the missing mass and source; it cannot be silently erased. A passive neutral recorder and the active controlled LEFT-label copy \(C_Y\) from §6.13 both commute with these centers, so neither *alone* changes the two block populations.

This matters immediately for [the full-source preparation equation (13f)](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md). Compare its exact *uniform terminal leaf* stationary state \(\zeta_N\) to the compatible **canonical tracial** cyclic state \(\Omega_N\), at the **same** level \(N\):
\[
\begin{array}{c|cc}
 &X\text{-block mass}&Y\text{-block mass}\\
\hline
\Omega_N &a_Np^{N+1}&b_Np^{N+2}\\
\zeta_N&a_N/d_N&b_N/d_N
\end{array}
\tag{A13}
\]
where \(p=\varphi^{-1}\). Both are legitimate normalized states, but these probabilities differ at every finite level. From Binet asymptotics,
\[
\boxed{
\lim_{N\to\infty}\mathrm{TV}
\bigl(\Omega_N|_{\mathrm{center}},
      \zeta_N|_{\mathrm{center}}\bigr)
=\frac{\varphi}{\sqrt5}-\varphi^{-1}
=1-\frac{2}{\sqrt5}
\approx0.105572809.
}\tag{A14}
\]
This is a persistent **moving-level central-sector** mismatch, not a contradiction with §6.7's separately proved convergence of the uniform *fine descendant* law to the PF trace on every **fixed earlier** level \(k\) as \(N-k\to\infty\). Fixed-\(k\) and moving-\(N\) claims have different quantifiers.

Therefore a physically imposed canonical RIGHT-center preparation at level \(N\), followed only by complete right-linear dynamics/copies preserving that center, cannot reach the exact uniform-fine-leaf stationary preparation of (13f); refinement by merely increasing \(N\) does not remove its center-TV gap. No right-unitary symmetry or left-CNOT readout is a center-population selector.

**Exact tangent implication.** If both block masses are preserved, the admissible real leaf-probability variations satisfy
\[
\sum_{i\in X}\delta r_i=0,\qquad
\sum_{i\in Y}\delta r_i=0.
\tag{A15}
\]
Even after introducing *all* right-linear LEFT mixers within each block, their image has dimension at most
\((a_N-1)+(b_N-1)=d_N-2\). The entropy derivation (13f) assumes the entire normalized leaf simplex of dimension \(d_N-1\). Hence at least **one cross-block contrast** and its physical source/preparation permission remain indispensable. The original old-neutral recorder has even smaller image (zero for all old leaf populations). This dimension count is for fixed level and fixed RIGHT centers, not a no-go for a dynamic refinement that truly changes its retained center/provenance or for an independently admitted initial preparation with the stationary masses already present.

**Shortest constructive route:** the known active LEFT copy provides the measurement. For physical preparation selection, supply an admitted right-preserving within-block mixing programme **and** either an actual center-changing, fully recorded cross-block preparation/refinement operation, or prove the required block masses are supplied by an independently selected admissible initial state. Count the center transfer and its whole-work source. This replaces a vague all-state preparation oracle with one identified missing block-contrast equation; it does **not** assume that the existing Fibonacci inclusion automatically performs this change.
