# D0 → GR: native Julia blank support forbids passive sharp AF-leaf readout

**Date:** 18 October 2026. **Consumer:** existing Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`.
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

\`python3 02_REGISTRY/research/certificates/a4d_raw_julia_blank_leaf_postprocessing_check.py\`

The script verifies the literal Julia two-leading-row completeness identity in \(\mathbb Q(\sqrt5)\), strict finite blank floors, the nonzero finite-\(T\) limit, the optimal 2-leaf saturating POVM control and the nonzero entropy-source contrast. The analytic proofs above apply to arbitrary finite-dimensional POVMs and every native 128 Kraus word, not just its two-mode diagonal test. No full Lean, huge raw-history enumeration or unrelated GR suite is claimed.
