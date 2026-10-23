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


## 9. Positive minimal escape: one physical cross-block rotation is enough for the missing entropy equation

The conserved-center obstruction admits a sharper **constructive** answer than an unrestricted state-preparation oracle. The exact entropy equations of [full-source (13e–f)](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md) only need enough admissible *preparation tangents* to connect the probability simplex. A spanning tree of real two-leaf rotations suffices.

Use the actual normalized diagonal matrix units \(e_i\) inside the full AF GNS, including both original summands and without deleting off-diagonal matrix units. On the **mathematically supplied** strictly positive pure section
\[
|\Psi(r)\rangle=\sum_{i=1}^{d}\sqrt{r_i}|e_i\rangle,
\qquad r_i>0,\quad\sum_i r_i=1,
\tag{A16}
\]
consider an orthogonal Givens rotation \(U_{ij}(\theta)\) on just the span of \(\{e_i,e_j\}\), identity on the full orthogonal complement. Direct differentiation at \(\theta=0\) gives
\[
\partial_{\theta_{ij}}r
=2\sqrt{r_i r_j}(\mathbf e_i-\mathbf e_j).
\tag{A17}
\]
This is an exact full-Hilbert pure-state tangent; it is NOT an assertion that arbitrary continuous \(U_{ij}(\theta)\) is physically available for free.

Let \(G\) be the undirected graph of pairs for which a genuine smooth preparation variation is admitted with **the same price/source**. At positive \(r\), its tangent matrix is a graph incidence matrix multiplied by nonzero edge coefficients \(2\sqrt{r_i r_j}\). Therefore
\[
\operatorname{rank}D_{\theta}r
=d-c(G),
\tag{A18}
\]
where \(c(G)\) is the number of connected components. At the original complete five-flag vacuum the full SAME-history price, for these preparation directions and with all other actual sources held as specified, is \(S=[H(r)+K]/\ell\). Hence
\[
\boxed{
\partial_{\theta_{ij}}S
=\frac{2\sqrt{r_i r_j}}{\ell}\log\frac{r_j}{r_i}.
}
\tag{A19}
\]
Stationarity along every admitted edge forces \(r_i=r_j\) on each component. **If and only if the admitted mixing graph is connected, these equations force \(r_i=1/d\) for all leaves** (within this strictly positive section and without an independent compensating controller source).

For the actual two AF blocks, an arbitrary spanning tree inside X and another inside Y yield \(c(G)=2\), rank \(d-2\), and leave the relative block mass \(u\) undetermined:
\[
r_i=u/a\quad(i\in X),\qquad r_j=(1-u)/b\quad(j\in Y).
\]
Admitting **one** additional X–Y edge connects the trees, raises the rank to \(d-1\), and enforces the exact missing equation
\[
\frac{u}{a}=\frac{1-u}{b}\quad\Longleftrightarrow\quad
u=\frac{a}{a+b}.
\tag{A20}
\]
No global universal \(SO(d)\) family is necessary for this particular stationary probability consumer: one cross-block Givens direction and enough within-block spanning edges are mathematically sufficient. The checker verifies ranks \(d-2=6\) and \(d-1=7\) for the honest example \((a,b)=(5,3)\), retaining both blocks.

**Operational boundary:** the missing cross-block \(U_{ij}\) does not commute with the original RIGHT center. It is not generated by the old right-preserving recorder or by the already-built LEFT copy. One must **derive its physical admission**, or a genuinely equivalent dynamic preparation variation, along with its complete work/archive transfer and first source. The fixed-width real-operator compiler of §6.14 gives a conditional *approximation* if actual addressable full-state controls are supplied; it does not force a continuous physical Euler direction or remove the controller source. If the real work law has a nonzero derivative along the Givens angle, (A19) acquires that additional term and the uniform root is not automatic.

**Concrete next parent lemma:** verify the actual D0 preparation/verification programme supplies this one X↔Y probability contrast in addition to within-block contrasts, with the same complete history and source. Then (A19–A20), the already owned leaf POVM (13aa–ae), the conditional nonlinear Euler transfer (13p–q) and C² geometric recovery compose without assuming a freely adjustable entire GNS sphere. Independent matter, selected dynamics and the raw all-ten GR limit remain separate.


## 10. New synthesis consuming two-sided GNS unfolding: a constrained center may suffice in the weak source limit

The disjoint [two-sided GNS folding owner](A4D_GNS_TWO_SIDED_PATH_UNFOLDING_AND_ARCHIVE_SOURCE_2026_10_18.md), §§1–4, changes the asymptotic conclusion of §8 **without invalidating it**. Uniform terminal LEFT-only leaves carry a persistent same-moving-level PF-center gap (A14), while the entire matched LEFT×RIGHT GNS pair carrier has \(a_N^2+b_N^2=F_{2N+3}\) labels; its *uniform measured pair law* is exactly the LEFT law of twice the path depth. Its center weight \(u_N^*=a_N^2/(a_N^2+b_N^2)\) now approximates the canonical right-center mass \(u_N=a_Np^{N+1}\) exponentially. This is a distinct measurement with its own RIGHT history and potential decoherence: the effect/source admission from that owner remains conditional.

A new useful mathematical route follows. Suppose the **complete paired classical pointer** is physically measured, with its true five-outcome conditional probabilities \(a_i=a_0+c f_i(y)\), \(c=p^2t^2\), \(z_i=1+2e^{h(a_i)}>0\), and that within each X/Y ending sector its positive preparation tangents are free, while the *unconditional old RIGHT central mass* \(u_N\) stays fixed by the actual retained history. This is the precise preparation image of §8 if its stronger all-pair readout is separately admitted; we do **not** assume a full cross-center mixer.

Let \(I_X,I_Y\) be the real paired-path sets with cardinalities \(a_N^2,b_N^2\), and define
\[
D_X(y)=\sum_{i\in I_X}z_i(y),\quad
D_Y(y)=\sum_{i\in I_Y}z_i(y),\quad D=D_X+D_Y,\quad v_N=1-u_N.
\]
Maximization/stationarity of the **same complete measured Shannon price** along all admitted positive within-sector preparation directions yields
\[
r_i^{\rm constrained}=
\begin{cases}
u_N z_i/D_X,& i\in I_X,\\
v_N z_i/D_Y,& i\in I_Y,
\end{cases}
\]
and the exact reduced value
\[
\boxed{
\ell\Gamma_{\rm fixed}
=h(u_N)+u_N\log D_X+v_N\log D_Y,
\quad \ell=\log\varphi.
}
\tag{A21}
\]
By contrast, free variation also of the single cross-center contrast yields the positive-pair law \(r_i^{\rm free}=z_i/D\) and
\(\ell\Gamma_{\rm free}=\log D\), the already-owned full paired source.

There is an **exact complete-price relation**, not an inserted KL-as-Book action:
\[
\boxed{
\ell(\Gamma_{\rm free}-\Gamma_{\rm fixed})
=D_{\rm KL}\!\left((u_N,v_N)\,\middle\Vert\,
                     (D_X/D,D_Y/D)\right)\ge0.
}
\tag{A22}
\]
KL appears only as the *difference between two optimizations of the same Shannon price*, not as the physical Cost−Info. Every geometric directional first source satisfies the exact defect identity
\[
\boxed{
D_y(\Gamma_{\rm fixed}-\Gamma_{\rm free})
=\frac{u_N-D_X/D}{\ell}
 \left(\frac{D_yD_X}{D_X}-\frac{D_yD_Y}{D_Y}\right).
}
\tag{A23}
\]
The missing physical center Euler direction of the same price is
\[
\partial_u\Gamma_{\rm fixed}
=\ell^{-1}\log\!\frac{(1-u)D_X}{uD_Y},
\tag{A24}
\]
where the derivative formally allows the center mass to move; it vanishes at \(u=D_X/D\), but is not required to vanish on a strictly center-preserving physical variation image.

**Exact golden smallness of the missing center direction.** At vacuum \(f_i=0\),
\[
\frac{u_N^*}{u_N}
 =\frac{1-(-p^2)^{N+2}}{1-(-p^2)^{2N+3}},
\quad
|u_N-u_N^*|\le
u_N\frac{p^{2N+4}+p^{4N+6}}{1-p^{4N+6}}
=O(p^{2N}).
\tag{A25}
\]
This is precisely the doubling result (F6) with \(k=N\), NOT the persistent LEFT-only gap of (A14). If \(f_i\) and their declared smooth \(y\)-jets are uniformly bounded, \(a_i\) remain in an interior compact set, and \(c\to0\), then \(D_X/D=u_N^*+O(c)\) uniformly in the number of GNS pairs, and \((D_yD_X/D_X-D_yD_Y/D_Y)=O(c)\). Consequently
\[
\boxed{
|\partial_u\Gamma_{\rm fixed}|=O(p^{2N}+c),
\qquad
|D_y(\Gamma_{\rm fixed}-\Gamma_{\rm free})|
=O\bigl(c(p^{2N}+c)\bigr).
}
\tag{A26}
\]
After the already declared *mathematical* leading geometric normalization by \(c>0\), the difference is only \(O(p^{2N}+t^2)\). On vacuum, this follows also directly from the exact source:
\[
D_y(\Gamma_{\rm fixed}-\Gamma_{\rm free})\big|_{f=0}
=\frac{cz'(a_0)}{\ell z(a_0)}(u_N-u_N^*)
  \left(\overline{D_y f}_X-\overline{D_y f}_Y\right).
\tag{A27}
\]
In particular the inability of right-preserving dynamics to change the center **does not by itself force a persistent Einstein-source error** if the real, resource-priced **two-sided** full GNS readout is admitted and \(N\to\infty,t_N^2\to0\) with the needed smooth control. It rules out exact finite *free-center* criticality from a fixed different central input, while the full center Euler defect and normalized geometric source gap may vanish in this controlled limit. This is a positive alternative to physically forcing an exact cross-block rotation on every level.

**New decisive physical test:** distinguish (i) genuinely measured matched LEFT×RIGHT classical pair outcomes, with the additional \(H(R|L,J)\) and archive work source, from (ii) an untouched coherent RIGHT matrix algebra, for which (A21–A27) are *not* the native complete price. The two-sided owner proves preservation of commuting geometric first sources under RIGHT dephasing, but NOT universal non-disturbance or equality of the full Book source. The remaining source estimate must include that complete recording work and be multiplied by the real spatial reconstruction/inverse constants before any GR promotion. Neither \(N\to\infty\) nor a free small \(t\) is asserted to be physically selected.

**Exact independent control:** symbolically
\(D\Gamma_{\rm fixed}-D\Gamma_{\rm free}=(u-D_X/D)(D D_X/D_X-D D_Y/D_Y)/\ell\) and
\(\ell(\Gamma_{\rm free}-\Gamma_{\rm fixed})=D_{\rm KL}(u\|D_X/D)\). The checker verifies both algebraically and the exact Fibonacci ratio (A25) for levels \(N=0,\dots,11\). This is a real source-composition lemma, not a second matter stress or another 40-row root catalogue.


## 11. Concrete fixed, field-independent REAL preparation on the full paired GNS: shift seed instead of a \(\Psi(g)\) oracle

The doubled-GNS §10 suggests a stronger **positive mathematical preparation**: produce the *canonical-right-center, uniform-within-center paired law* by a finite controlled **LEFT permutation**, retaining a coherent work seed. This uses no cross-center mixer, no independent matter copy and no field-dependent state preparation. It closes the within-center probability-accessibility problem on the supplied addressed real controller class; native physical gate/seed admission and cost remain open.

### 11.1. Right marginal exactly unchanged, all pair labels active

On one actual block of size \(a\), let \(H_a=\mathbb C^a_L\otimes\mathbb C^a_R\), with canonical trace vector
\[
|\Omega_a\rangle=a^{-1/2}\sum_{j=0}^{a-1}|j\rangle_L|j\rangle_R.
\]
For \(s\in\mathbb Z/a\mathbb Z\), let \(V_s|j\rangle_L=|j+s\bmod a\rangle_L\); \(V_s\) is a REAL permutation. Prepare one \(\lceil\log_2a\rceil\)-bit work seed in the state \(a^{-1/2}\sum_s|s\rangle_W\), apply the controlled LEFT shift \(V_s\otimes I_R\), and **retain** the work seed:
\[
|\Xi_a\rangle=\frac1{\sqrt a}\sum_{s=0}^{a-1}
  |s\rangle_W\otimes(V_s\otimes I_R)|\Omega_a\rangle.
\tag{A28}
\]
Both maps are isometries of the **full** matrix-unit GNS carrier plus work (complete them on invalid seed words, rather than discarding those words). The RIGHT reduced state is still \(I_a/a\) exactly, because every conditional \(V_s\) acts only on LEFT.

Measuring BOTH original path indices \((i,j)\) in their common block gives
\[
\boxed{\Pr(i,j)=a^{-2}\quad\text{for all }i,j=0,\ldots,a-1.}
\tag{A29}
\]
This is not the unjustified assumption of a real Hadamard with all entries equal magnitude: it is a **recorded mixture of cyclic permutations**. Indeed every pair \((i,j)\) corresponds to the **unique** seed \(s=i-j\bmod a\). Thus, even if the work seed is read as an additional complete classical word, it is a deterministic function of \((i,j)\):
\[
H(S,i,j)=H(i,j),\qquad H(S|i,j)=0.                  \tag{A30}
\]
The work *execution/preparation price* has not been shown field-independent or free; (A30) is solely a fact about the true measured same-history Shannon partition.

Do the same in the X and Y blocks using the **one existing canonical AF trace vector** with center amplitudes \(\sqrt{u_N}\), \(\sqrt{v_N}\), \(u_N=a_Np^{N+1}\), \(v_N=b_Np^{N+2}\). The block-controlled seed carries its block type, and no cross-block operator is used. On the original full paired GNS the resulting field-independent **measured probabilities** are
\[
r_i^0=
\begin{cases}
u_N/a_N^2, & i=(\alpha,\beta)\in I_X,\\
v_N/b_N^2, & i=(\alpha,\beta)\in I_Y.
\end{cases}\tag{A31}
\]
The entire noncommutative RIGHT marginal stays the canonical one until the physical paired readout. The latter dephases RIGHT path coherences; the independent [two-sided owner (F14–F15)](A4D_GNS_TWO_SIDED_PATH_UNFOLDING_AND_ARCHIVE_SOURCE_2026_10_18.md) proves that the already identified **commuting LEFT geometric effects and their derivatives** are source-preserved under this complete RIGHT readout. There is no claim of full right-archive non-disturbance.

This replaces the false shortcut “a right-linear REAL orthogonal on the original maximally entangled GNS cyclic vector can produce arbitrary new left probabilities”: a *single unconditioned right-linear unitary* on \(H_a\) preserves the maximally mixed LEFT marginal \(I_a/a\). The recorded seed in (A28) instead generates the required uniform **paired matrix-unit outcomes**, keeping that LEFT marginal uniform while activating all right indices. Field-independent preparation needs no \(\Psi(g)\) oracle.

### 11.2. Fixed preparation already has the correct leading geometric first source

Keep the **actual geometry-dependent AF effect** \(a_i=a_0+c f_i(y)\) in the already owned five-outcome terminal programme; \(a_0=p^2\), \(c=p^2t^2\). Fix the success preparation at its flat-vacuum balanced value
\[
s_*=\frac{2e^{h(a_0)}}{1+2e^{h(a_0)}},\qquad
b_*=1/2,
\]
rather than assuming a field-dependent preparation solver. Under the conditional physical registration of the paired leaves, the complete measured **Book SAME-history Shannon** price of this explicitly fixed input is
\[
\boxed{
\ell S_{\rm seed}(y)
 =H(r^0)+h(s_*)+s_*\log2
 +s_*\sum_i r_i^0 h(a_0+c f_i(y)),
\quad \ell=\log\varphi.
}
\tag{A32}
\]
All failure and four success flags, the real work seed, and both AF blocks remain registered; by (A30), the seed does not add an *independent measured word entropy* after the complete pair record. Other true programme/controller costs cannot be dropped by this identity.

For every smooth field tangent \(V\), **without differentiating any prepared state**,
\[
\boxed{
D_VS_{\rm seed}
=\frac{s_*c}{\ell}\sum_i r_i^0 h'(a_i)D_V f_i.
}
\tag{A33}
\]
The free fully stationary paired-history source from [two-sided (F9–F10)](A4D_GNS_TWO_SIDED_PATH_UNFOLDING_AND_ARCHIVE_SOURCE_2026_10_18.md) is
\[
D_V\Gamma_{\rm pair}
=\frac c\ell\sum_i\frac{z(a_i)}{\sum_jz(a_j)}
s(a_i)h'(a_i)D_V f_i,\quad
s(a)=\frac{2e^{h(a)}}{z(a)},\quad z(a)=1+2e^{h(a)}.
\tag{A34}
\]
At \(f_i=0\), \(s_*h'(a_0)=s_*\ell\), and the only source difference is the small canonical-vs-uniform paired-center defect (A25). On a common compact field chart with uniformly bounded \(|f_i|,|D_V f_i|\) and \(a_i\) in an interior positive interval, bounded derivatives of \(z,h',s\) and the normalized pair probabilities imply
\[
\boxed{
|D_V(S_{\rm seed}-\Gamma_{\rm pair})|
\le C_V\,c\bigl(p^{2N}+c\bigr),
}
\tag{A35}
\]
where \(C_V\) is independent of the number \(a_N^2+b_N^2\) of paired GNS outcomes. After the already owned positive geometric *source-comparison normalization* by \(c\), the difference is \(O(p^{2N}+t^2)\). This is a **positive explicit, field-independent state and preparation recipe**, not a statement of exact finite joint-criticality: at nonzero \(f_i\), frozen \(r_i,s_*\) do not solve all preparation Euler equations. Their positive-probability stationary contrasts are \(O(p^{2N}+c)\); source-controlled GR recovery must still keep the complete work/factory rows and their inverse/reconstruction factors.

This route therefore does NOT require either a physically exact cross-block mixer at every \(N\) or an external \(\Psi_*(g)\) preparation oracle to approximate the **geometric** source on the declared two-sided readout class. It requires physical **admission and source-priced compilation** of (A28), the actual LEFT+RIGHT classical pair readout and the same-history Book binding, and independent matter/clock equations. Importantly the work register can no longer be described as “free”: (A30) addresses pointer entropy alone, not the energetic/ActionProtocol execution cost.

### 11.3. Decisive checks, not a new catalogue

The local exact combinatorial control runs on the original block sizes \(a_N=F_{N+2},b_N=F_{N+1}\), \(N=1,\ldots,7\): every shift/pair relation is bijective, \(\sum r_i^0=1\), every RIGHT marginal equals the canonical one, and the work seed is determined by the measured pair. It then compares (A33) to (A34) for small, bounded inhomogeneous sources and verifies the \(\delta_N+c\) source budget. This verifies a **fixed-state, full paired-pointer** source result; it is not a C² theorem across invalid-word rank births, an exact physical native gate synthesis, or an Einstein-with-matter theorem.

**Next physical consumer:** find an admitted addressable implementation of the controlled LEFT shift on the *legal path-code*, prepare and retain the uniform finite seed without smuggling a new prior, and compute its actual complete work/source under the same Book cost. The existing full-operator REAL compiler can approximate supplied controls but does not authorize LEFT wires or select the seed. If those source terms vanish or are controlled in the normalized joint limit, consume (A35) together with the full-lattice C² geometric recovery; otherwise this mathematically successful route must remain conditional.
