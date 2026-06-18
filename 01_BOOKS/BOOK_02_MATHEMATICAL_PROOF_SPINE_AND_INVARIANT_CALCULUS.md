<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 02 — Mathematical Proof Spine and Invariant Calculus

> **[Standard Physics Isomorphism].** D0's coined terms in this book read, in mainstream physics, as:
>
> - archive → integrated-out environment / environment bath (open-system trace-out)
> - forgetting map / coarse-graining → Wilsonian coarse-graining / CPTP decoherence channel
> - archive pressure → trace anomaly / entropic backreaction
> - terminal (destructive) readout → projective (von Neumann) / POVM measurement
> - phason → Goldstone mode of broken translation symmetry
> - carrier → representation (state) space
> - readout → measurement outcome (POVM effect)
>
> Genuinely-D0 (kept, defined in-text against the standard notion): the scene `K(9,11,13)`, the M1 admissibility axiom (no obligatory external catalogue), `δ₀`, `φ`, and *forcing* (= reductio ad absurdum against M1). Full crosswalk: the language-normalization Rosetta (`00_LANGUAGE_NORMALIZATION/D0_STANDARD_LANGUAGE_ROSETTA.md`).


> Scope: Finite operator identities, feedback positivity, log-det calculus, and theorem-spine ownership.
> Claim discipline: This book owns internal finite identities; external measurements require bridge/passport layers.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 02.0 Active mathematical spine

Book 02 is the theorem spine for the feedback construction. It receives `P_N`, `Q_N` and `U_N` from Book 01 and proves the finite operator identities used by the sector books.

### Feedback construction

```text
F_N = (Q_N U_N P_N)^dagger (Q_N U_N P_N)
F_N = P_N U_N^dagger Q_N U_N P_N
F_N = P_N - (P_N U_N P_N)^dagger(P_N U_N P_N)
F_N >= 0
0 <= F_N <= P_N
R_N = D_N^dagger D_N
```

Finite Born owners:

```text
D0.finite_effect_born_readout_unique
D0.finite_effect_born_no_hidden_response
```

### Resolvent

```text
G_N(z) = (I - z F_N)^(-1)
det(I - z F_N) != 0
```

The expansion

```text
(I - z F_N)^(-1) = sum_{m>=0} z^m F_N^m
```

is valid only if:

```text
|z| rho(F_N) < 1
```

### Log-det and refined bounds

```text
-log det(I - z F_N)
= sum_{m>=1} z^m/m Tr(F_N^m)
```

With `a = |z| rho(F_N) < 1`:

```text
|-log det(I - z F_N)| <= rank(F_N)[-log(1-a)]
|T_M(z,F_N)| <= rank(F_N)/(M+1) * a^(M+1)/(1-a)
```

### Finite deformation and pressure

`partial_V` is a finite difference or a derivative along a frozen finite matrix family.

```text
Z_N = Tr exp(-beta Delta_N(V)) det(I - z F_N(V))^(-1)
mathsf P_fb = beta^(-1) partial_V log Z_N
```

Gravity proof-spine anchors: Entropic archive gravity interface, Finite spin-2 wave operator, Higher-curvature finite cut, Spectral A2 / EH bridge, Macro Einstein interface.

Book 04 operator-boundary anchor: `02.36.3b Book 04 operator-boundary closure`, `D0.Matter.book04_operator_boundaries_closed`, `nucleon_line_cannot_promote_full_baryon_multiplet`, `lower_hodge_400_cannot_promote_meson_masses`, `missing_scalar_projector_cannot_promote_higgs_yukawa_core`.

## 02.1 Standard proof-language convention

Every proof cell in this book is written in the sequence:

```text
support object -> finite operator/instrument -> positive response -> quotient/coupling -> invariant -> certificate.
```

Internal D0 names such as `archive`, `terminal`, `carrier`, `structural uniqueness / negative-control rigidity`, and `comparison protocol` are not primitives here. They abbreviate traced-out complements, absorbing channels, representation carriers, structural-rigidity/negative-control tests, and external comparison protocols.

The convention is not stylistic. It is forced by M1 (physics = what survives the requirement to distinguish itself without an external catalog; forcing-by-contradiction = DEF-0.2.2, owned by BOOK_01). The two results below justify *why* every cell must run support -> operator -> ... -> certificate with no exogenous parameter slipped in at any arrow, and they answer the standing objection that M1 is "merely philosophy."

**[THE] M1 is not philosophy but a theorem about Bayesian inference [^b02-1].** Over the space of computable theories the universal prior assigns `P(T) ≈ 2^{-K(T)}`, with `K(T)` the Kolmogorov complexity (shortest binary code describing the theory together with its constants). Compare two competitors: a Standard-Model-style theory `T_SM` = equations + an *exogenous catalog* of constants `C` (m_e, alpha, ...), so `K(T_SM) ≈ K_eq + K(C) >> K_eq`; versus a distinguishability theory `T_D0` = equations + an O(1) graph-generation algorithm, so `K(T_D0) ≈ K_eq + O(1)`. Solomonoff induction / MDL therefore penalizes the catalog by its description length. The absence of free parameters demanded by M1 is exactly the MDL-/universal-induction-optimal choice — not an aesthetic preference. [Status: FORMALISM. This is the standard external interpretation of M1, not the source of its truth, which is the forcing proof THE 20.1.1 below.]

**[THE 20.1.1] No mathematics without M1 [^b02-2].** If exogenous parameters are permitted (M1 violated), then "axiom / theorem / definition / inference-rule" cannot be rigorously distinguished, and the object "theory" itself dissolves. Proof (⊥; cf. BOOK_01 THE 0.4.1).
1. Any written record presupposes a procedure for distinguishing symbols and the boundaries of proof blocks.
2. If exogenous parameters are admitted, the criterion for "what counts as an admissible rule / a stopping point / a precision / a completeness" becomes external and non-fundamental.
3. Then one and the same string of text admits infinitely many incompatible readings of "what here is axiom, what is derivation," with no internal test selecting the correct one.
4. This destroys the distinguishability of statuses and renders verifiability impossible — contradicting the brute fact that a corpus of distinguishable statements exists. ⊥.

Hence the proof-language convention may invoke no external catalog: every cell must be internally checkable end to end, which is why it terminates in a `certificate` rather than in an appeal to an outside authority.

**[COR 20.1.2] Actual infinity is undefinable without M1 [^b02-3].** Defining an *actual* infinity requires an external criterion of identity/boundary — which elements are included, what counts as "all" — i.e. an external catalog, forbidden by M1. Therefore CORE admits only *potential* infinity, realized as a pro-system of refinements (the inverse-system / varprojlim construction operated by BOOK_01 §01.4/§01.15). The convention's `support object -> ... -> invariant` chain is thus always a finite cell over a pro-system, never a completed infinite totality.
## 02.2 Role of this book

Book 02 is the mathematical reference for the corpus. Book 01 constructs the finite detector object and graph-birth lift; Book 02 records the proof calculus that later sector books use when they state action, matter, gravity, or cosmological transfer claims. Sector books may state physical comparison protocols and sector-specific lemmas, but proof-level reductions point back here unless the proof is intrinsically sector-specific.

## 02.3 Proof ownership rule

A D0 claim is proof-complete only when the following data are specified:

```math
(\text{support},\ \text{probe/gate},\ \text{operator},\ \text{quadratic response},\ \text{quotient},\ \text{bridge type},\ \text{falsification hook}).
```

A numerical coincidence is not a theorem. A formula can be retained as an active comparison protocol if it is typed, certified and falsifiable, but it is not a completed derivation until this book supplies the finite operator and uniqueness argument.

The proof-reference chain used throughout is:

```math
\text{finite support}\rightarrow
\text{projector/probe}\rightarrow
S_{gate}/J_{scene}\rightarrow
\mathcal G_{spec}\rightarrow
W_A\rightarrow
\operatorname{Tr}_K(\cdot)\rightarrow
\text{normalized readout/comparison protocol}.
```

The "operator" slot of that tuple is not free: it is fixed by the **Finite Holographic Self-Reading Principle**. The principle requires that the feedback-return operator preserve the symplectic area form across the retained/archive cut `P_N + Q_N = I`. That single area-preservation requirement is the forcing for the whole quadratic-response calculus this book carries downstream.

**[DEF] Core dynamical operator.** Admit the retained projector `P_N`, the archive complement `Q_N = I - P_N`, and the finite tick `U_N` from BOOK_01 (the retained/traced split and the handoff `F_N = P_N U_N^dagger Q_N U_N P_N` are owned there; see BOOK_01 §01.0). The feedback-return operator is

```math
F_N = (Q_N U_N P_N)^\dagger (Q_N U_N P_N) \in B(P_N\mathcal H).
```

This is the exact embodiment of holographic area preservation under self-reading: `F_N` measures how much of a retained state, after one tick and the cut, returns through the archive complement, and the area form admits no other quadratic that closes on the retained block [^b02-4].

**[THE] What the area form forces.** Because `F_N = (Q_N U_N P_N)^\dagger (Q_N U_N P_N)` is a Gram operator, the self-reading requirement forces, with no further input:

- **positivity** `F_N >= 0`, indeed `0 <= F_N <= P_N`, since the area-preserving cut cannot return more than the retained block carries;
- **compression** of the dynamics onto `P_N\mathcal H`, so the quadratic response lives on a finite retained block rather than the full stage;
- the **log-det functional** `-\log\det(I - z F_N)` as the natural area-derived generating functional, with its spectral admissibility bound `|z|\rho(F_N) < 1`.

So positivity, the compression bound and the log-det calculus are not three separate postulates; they are one consequence of symplectic-area preservation across the retained/archive cut [^b02-5]. This is why a typed comparison formula is not yet a theorem until its operator slot is shown to be this area-derived `F_N`: only then is the quadratic response forced rather than fitted.
## 02.3a Active v15 proof spine

The active proof spine is:

```text
finite detector support
-> φ-rigid phase return
-> condensed tiling hull
-> frozen finite operator
-> positive quadratic response or heat trace
-> quotient/window
-> K-theory / K0 Gap Label or finite spectrum certificate
-> typed observable-transfer bridge
-> falsification hook
```

## Finite cochain complex and Hodge Laplacian

The finite graded incidence complex is the common algebraic carrier for
cochain-level defect, response and heat-trace constructions. The D0 core uses
finite boundary maps and finite Hodge Laplacians, not continuum curvature
tensors, as its master topological object.

Closed-vacuum feedback adds the paired operator `(Delta_N, F_N)`: the Hodge Laplacian supplies the geometry spectrum, and the feedback determinant supplies unresolved return cycles. `F_N=P_N U_N^dagger Q_N U_N P_N` is the feedback-return operator; `R_N=D_N^dagger D_N` remains the positive response/readout operator. Owners: `D0.Cosmology.FeedbackPartitionFunction`, `feedback_determinant_return_cycles`, `feedback_variation_universal_source`.

The admissible finite identities are:

```math
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N)
=P_N-(P_NU_NP_N)^\dagger(P_NU_NP_N),
\qquad F_N\ge0,
\qquad F_N=0\Longleftrightarrow Q_NU_NP_N=0.
```

The complement being nonzero does not force feedback: `Q_N\ne0` alone does not imply `F_N\ne0`.

The resolvent `(I-zF_N)^{-1}` exists when `z^{-1}` is outside the finite spectrum of `F_N`. Neumann and loop expansions require the stricter radius condition `|z|\rho(F_N)<1`, and the determinant trace formula is logarithmic:

```math
-\log\det(I-zF_N)=\sum_{m\ge1}{z^m\over m}\operatorname{Tr}(F_N^m).
```

For a finite deformation parameter `V`, `d_V` means either a declared finite-difference operator on a finite matrix family or an ordinary derivative of a smooth finite-dimensional matrix family.

## 02.CVFT.v5 Refined feedback bounds and compressed pole discipline

For `F=(QUP)^\dagger(QUP)`, rank equality is `rank(F)=rank(QUP)`. If `im(QUP) subset B_boundary(P,Q)`, then `rank(F) <= dim B_boundary(P,Q)`; write `|partial(P,Q)|` only after independent boundary channels have been identified with cut edges.

Let `a=|z|rho(F)<1`. With the analytic logarithm branch connected to `z=0`,

```math
\left|-\log\det(I-zF)\right|\le \operatorname{rank}(F)[-\log(1-a)]\le \operatorname{rank}(F){a\over 1-a}.
```

For real positive `z`, `0<z<1/rho(F)` gives `-\log det(I-zF) <= rank(F)[-\log(1-z rho(F))]`. For the tail

```math
T_M(z,F)=\sum_{m>M}{z^m\over m}\operatorname{Tr}(F^m),
```

the target bound is

```math
|T_M(z,F)|\le {\operatorname{rank}(F)\over M+1}{a^{M+1}\over 1-a},
```

with fallback `rank(P)` when only the ambient retained support is known. `U_eff=PUP` is a contraction; complex pole language belongs to `U_eff`, an effective non-Hermitian transfer, or Feshbach-Schur. Bare positive `F` has real nonnegative spectrum.

No sector may skip from a named operator to a physical observable. The owner chain must show whether the claim is core, certificate-closed, a no-go, a calibration bridge, or an empirical passport.

## 02.K K-theory / Gap Labeling proof spine

K-theory / Gap Labeling enters D0 only after the operator and tiling-hull carrier are frozen. A K0 gap label is not an action term, not a tunable mass correction, and not a new continuum field.

The admissible chain is:

```text
tiling hull
-> frozen finite approximants
-> spectral gap of the frozen operator
-> K0 gap label
-> readout sector index
-> optional external passport
```

The proof cells are:

| cell | obligation |
|---|---|
| hull owner | the support is the φ-quasicrystalline tiling hull or a declared finite approximant |
| frozen operator | the operator is fixed before comparison |
| gap label | the label records a spectral gap of that operator |
| negative control | retuning the operator after comparison is forbidden |
| bridge boundary | external masses, CKM entries or survey values require a separate passport |

## 02.4 Uniqueness obligations for high-sensitivity formulas

The source proof spine identifies formulas that are too high-gain to be justified by numerical success alone. They remain active only with explicit uniqueness obligations.

### 02.4.1 Electroweak radial depth

```math
A_{depth}^{EW}=\varphi^{35}\left(1+{\delta_0\over\varphi}-\varphi^2\delta_0^3\right).
```

The exponent and two correction terms must be selected from the gate-action grammar. Nearby expressions are rejected unless they satisfy the same admissibility constraints.

### 02.4.2 Charged-lepton generation action

```math
R_g^{D0}=r_gA_{EW}^{p_g}B_g,
\qquad
p_e=0,
\quad
p_\mu={1\over4},
\quad
p_\tau={1\over3}.
```

The powers are not fit exponents. They must come from finite operator sources, and boundary factors must be selected from the same action grammar, not inverted from the charged-lepton table.

### 02.4.3 Survey scalar amplitude

```math
A_s^{D0}={(1+\delta_0/4)I_B\over2|V||V_{13}|}.
```

The terminal survey normalization is the full-cycle terminal readout count. The rejected direct expression `(1+delta0/4) I_B` is retained only as a scale-error diagnostic.

### 02.4.4 Stiffness uniqueness protocol

Any formula containing a high-gain factor `φ^N`, `δ_0^N`, or a small rational correction exponent is proof-complete only after the exponent has a finite operator source.  A sensitivity calculation is not enough.  The book must specify:

```math
N=N_{support}+N_{orientation}+N_{return}-N_{quotient},
```

or an equivalent finite trace, determinant, rank, cycle-length or endpoint-count identity.  Alternative choices such as sums instead of products, local rank instead of ordered endpoint pairs, or post-hoc reduced exponents are rejected unless they are selected by the same operator.

The protected sources are:

| quantity | active exponent/source |
|---|---:|
| gravity length-depth | `99=|V_9||V_{11}|` |
| weak-unlock depth | `19=2γ-1`, `γ=(|V|-Rank)/Rank=10` |
| action section | `38=2(2γ-1)` |
| electroweak radial depth | `35=|V|+Rank-1=33+3-1` |
| EM residual exponent | `5/8+δ_0/384`; `5/8=(ABCD+1)/Ω_8`; `384=Ω_8·ABCD·dim(g_light)` |

If any listed source is absent from the active book section, the corresponding result must be labelled `STIFFNESS-PROOF-CELL-MISSING`, not promoted as a closed theorem.

## 02.5 The theorem chain inherited from Book 01

Book 02 does not reintroduce D0 foundations rhetorically; it formalizes the proof calculus used after them.

```math
x^2=x+\mathfrak q,
\qquad
x=\varphi,
\qquad
p=\varphi^{-1},
\qquad
p+p^2=1,
\qquad
\delta_0={\sqrt5-2\over2}={1\over2\varphi^3}.
```

The role of these identities in Book 02 is operational. They define the finite terminal quotient ideal and admissible runtime calculus. A sector formula may use a φ lift, echo, boundary correction or archive leakage only if the use is typed by the finite operator grammar.

### 02.5.0 Two independent forcings of `φ`

Book 01 owns the φ derivation; Book 02 inherits it but records *that the same constant is forced twice by independent routes*, because the proof calculus below treats every φ-typed operator as over-determined, not chosen. The two routes are:

**Route 1 — positive-response quadratic (return branch).** `p+p^2=1` with `p=\varphi^{-1}` (canonical owner BOOK_01 §01.6); this is the route Book 02 uses operationally above.

**Route 2 — self-similarity of refinement (no step-catalog).** This is a *second, structurally independent* forcing and it is the one Book 02's descent calculus actually instantiates.

[LEM 2.5.0.S1] [^b02-6]. Run the two-step mediator scheme `S,T\mapsto P=S\oplus T`, then `T,P\mapsto Q=T\oplus P`. Let

```math
r:=\frac{F(T)}{F(S)},
\qquad
\Phi(r):=1+\frac1r .
```

`Φ` is the operator that refines the scale ratio by one step. M1 forbids the *type* of the ratio to depend on the step number: if `r` and `Φ(r)` were of different type, the system would need an external "step-correction" function — a catalog indexed by step — which is exactly what M1 prohibits (a system cannot import an external index to distinguish its own stages). Hence the refinement ratio must be a fixed point,

```math
r=\Phi(r).
```

This is a forcing of φ that never mentions a detector, a probability split, or `p+p^2=1`; it follows purely from refusing a step-indexed external catalog. [LEM]

[SECTION 2.5.0.alg] [^b02-7]. Additivity `F(P)=F(S)+F(T)` makes the two branches of the two-step scheme

```math
\frac{F(P)}{F(S)}=1+\frac{F(T)}{F(S)}=1+r,
\qquad
\frac{F(Q)}{F(T)}=1+\Bigl(1+\frac1r\Bigr)=\frac{2r+1}{r}.
```

The S1 fixed-point condition equates them,

```math
1+r=\frac{2r+1}{r}
\;\Longrightarrow\;
r(1+r)=2r+1
\;\Longrightarrow\;
r^2-r-1=0,
```

whose unique positive root (a scale is `>0`) is

```math
\varphi=\frac{1+\sqrt5}{2}.
```

Note this is the *self-similarity* quadratic `r^2-r-1=0`, obtained by equating the two refinement ratios; it is algebraically conjugate to, but derivationally distinct from, the return-branch quadratic `p+p^2=1` of Route 1. The proof calculus needs both because the descent functor (§02.5.1.1) is the operator form of exactly this equate-two-stages step.

[THE 2.5.0.3] [^b02-8]. In any system in which (1) the coupling is additive, `F(P)=F(S)+F(T)`, and (2) the scale space is homogeneous (the S1 no-step-catalog condition), the scaling parameter is necessarily `φ`. φ is therefore not a primitive axiom and not numerology: it is the forced consequence of refusing external parameters. This sharpens the BOOK_02 §02.31 statement "φ is not a primitive axiom" by naming the exact premise pair — additivity plus homogeneous scale — that yields φ as the homogeneous-scale fixed point. [THE]

### 02.5.1 The `φ`-ABCD operator-cycle theorem

The four ABCD entries must be treated as typed operators, not as four independent scalar axioms.  Let `T_φ,T_ψ` be the two conjugate branch operators of the finite comparison module.  Define

```math
A_?(T)=T_?+T_?,
\qquad
B_N(T)=T_?T_?,
\qquad
C_+(T)=T_φ^2-T_φ,
\qquad
D_-(T)=T_ψ^2-T_ψ.
```

The `φ` detector cycle imposes the operator identities

```math
A_Σ=I,
\qquad
B_N=-I,
\qquad
C_+=I,
\qquad
D_-=I.
```

On scalar branch representatives these are exactly

```math
\varphi+\psi=1,
\qquad
\varphi\psi=-1,
\qquad
\varphi^2=\varphi+1,
\qquad
\psi^2=\psi+1.
```

The scalar equations are algebraically linked, but the operators have different typing:

```text
A_Σ : additive normalization / unit-section operator
B_N : multiplicative coupling / norm-orientation operator
C_+ : forward branch recurrence operator
D_- : return branch recurrence operator
```

Therefore the proof obligation is not scalar independence.  The obligation is cycle completeness: remove any one typed operator and the finite detector cycle loses a required boundary condition.  `A_Σ` removes the unit, `B_N` decouples the branches, `C_+` destroys forward runtime recursion, and `D_-` destroys return closure.  This is the operator sense in which ABCD is minimal.

The four entries are also Galois data of `\mathbb Q(\sqrt5)`: `A_Σ` (sum) and `B_N` (product) are the symmetric functions, hence Galois-invariant, while `C_+` and `D_-` are the recurrences of the conjugate pair `\varphi,\psi` exchanged by the nontrivial automorphism (forcing: D0-VIETA-GALOIS-ABCD-001 — A,B invariant, C,D a conjugate pair over `\mathbb Q(\sqrt5)`). The minimality above is thus the same statement as: the cycle carries exactly the invariant + conjugate-orbit data of the quadratic field, no more.

The terminal two-port readout is a representation of this operator cycle by four role classes

```math
(A,B,C,D)=((3,3),(4,4),(3,4),(4,3)),
```

followed by the sign/phase extension

```math
ABCD\times\{+,-\}=\Omega_8.
```

The theorem is intentionally stronger than an equation table and weaker than a false claim of scalar independence: it states that the completed detector cycle has four typed operator obligations and that the two-port terminal readout realizes exactly four pre-sign roles.

The sign/phase extension lands on `\Omega_8` and not on some other order-8 carrier because the carrier is forced to be the quaternion group `Q_8`. [THE 2.5.1.Q8] [^b02-9]. The detector cycle requires a non-abelian group every one of whose subgroups is normal (a *hamiltonian* group), so that each role-class subgroup is a legitimate invariant boundary condition; by Dedekind's 1897 classification the smallest non-abelian hamiltonian group is `Q_8`, with `[Q_8,Q_8]=Z(Q_8)=\Phi=\{\pm1\}` — its commutator equals its center equals the sign group `\{+,-\}` of the extension above. Hence `\Omega_8\cong Q_8` is not an analogy but the minimal carrier (finite check: enumerate groups of order `\le8`; `Q_8` is the unique smallest non-abelian hamiltonian one). This is the forcing behind the bare `\Omega_8\sim Q_8` fact: the `\{+,-\}` extension and the role-class normality jointly select `Q_8`. [THE]

#### 02.5.1.1 Condensed descent form of the ABCD cycle

The operator-cycle theorem is a theorem in the finite-stage condensed setting, not an equation table.  At each quotient `S_N`, the branch operators are finite endomorphisms of `\mathcal H_N`.  The family is admissible only when the squares

\[
\begin{array}{ccc}
\mathcal H_{N+1} & \xrightarrow{T_{\bullet,N+1}} & \mathcal H_{N+1} \\
\downarrow P_{N+1,N} && \downarrow P_{N+1,N} \\
\mathcal H_N & \xrightarrow{T_{\bullet,N}} & \mathcal H_N
\end{array}
\]

commute for `\bullet\in\{\varphi,\psi\}`.  The four ABCD identities are then natural transformations of this finite-stage system:

\[
A_{\Sigma,N}:T_{\varphi,N}+T_{\psi,N}\Rightarrow I_N,
\qquad
B_{N}:T_{\varphi,N}T_{\psi,N}\Rightarrow -I_N,
\]

\[
C_{+,N}:T_{\varphi,N}^2\Rightarrow T_{\varphi,N}+I_N,
\qquad
D_{-,N}:T_{\psi,N}^2\Rightarrow T_{\psi,N}+I_N.
\]

This is why scalar derivability does not settle the physical question.  Scalar derivability says that the four numerical equations live in the same quadratic presentation.  D0 requires more: the four natural operators must be present as finite-stage structure maps.  Their roles are different because they control different compatibility conditions of the admissible subfunctor.  (The commuting-square condition is the operator form of the S1 step-independence of §02.5.0: the structure map must not change type under the projection `P_{N+1,N}`, i.e. under refinement by one stage.)

The terminal two-port readout is therefore written as a role-preserving representation

\[
\rho_{2}:\mathsf C_{\varphi}^{D0}\longrightarrow\mathsf R_2,
\]

where `\mathsf C_{\varphi}^{D0}` is the four-obligation operator-cycle category and

\[
\operatorname{Ob}(\mathsf R_2)=\{(3,3),(4,4),(3,4),(4,3)\}.
\]

The representation is faithful on typed roles but is not a replacement for the condensed proof.  Its signed extension gives

\[
\operatorname{Ob}(\mathsf R_2)\times\{+,-\}=\Omega_8.
\]

Thus the proof-cell has three layers:

\[
\text{condensed finite-stage descent}
\Rightarrow
\text{four operator obligations}
\Rightarrow
\text{terminal two-port representation}.
\]

A claim that skips the first layer is only an analogy.  A claim that skips the second layer is only a scalar identity.  A claim that skips the third layer has no terminal detector comparison protocol.

### 02.5.2 Centered half-gap and dimension ladder

The centered half-gap is forced by a *canonical decomposition of unity*, not assumed.  [THE 2.5.2.unit] [^b02-10].  Ask how to split the whole `1=x+y` into parts with no arbitrariness.  Then: (i) `x+y=1`; (ii) the asymmetry ratio `x/y` must be expressible with no new parameter; (iii) the *only* dimensionless scale parameter available in the mechanism is `φ`; (iv) hence the sole M1-admissible ratio is `x/y=\varphi`; (v) solving with `1+\varphi=\varphi^2` gives `x=\varphi^{-1},\;y=\varphi^{-2}`.  The split is unique *because* φ is the only admissible scale — any other ratio would smuggle in an external catalog of cuts, violating M1.  This is the forcing reason behind the result `p_+=\varphi^{-1},\,p_-=\varphi^{-2}`, which §02.5.2 and §02.31 also obtain as the output of the `p+p^2=1` detector skeleton.

From the normalized branches

```math
p_+=\varphi^{-1},
\qquad
p_-=\varphi^{-2},
\qquad
p_++p_-=1,
```

D0 defines the distinguishability quantum as the centered half-gap

```math
\delta_0={p_+-p_-\over2}={1\over2\varphi^3}={\sqrt5-2\over2}.
```

Hence

```math
p_+=\frac12+\delta_0,
\qquad
p_-=\frac12-\delta_0,
```

and the factor `2` in the one-dimensional quantum is forced by the full gap:

```math
Q(1)=p_+-p_-=2\delta_0.
```

The factor `2` is not a normalization convenience; it is forced by contradiction.  [THE 2.5.2.factor2] [^b02-11].  Suppose distinguishability could be quantized one-sidedly, with no factor 2.  Then three independent contradictions follow: (1) "distinguishing" would not require a *pair* of objects, which contradicts the very meaning of distinguishability; (2) the φ-quadratic would have a single root, which is impossible (the conjugate pair `\varphi,\psi` is exactly the two-sidedness of `C_+/D_-`); (3) path holonomy could be one-sided, which forbids the *closed* memory cycles that a history requires (cf. the noncommutative order-memory carrier).  A contradiction in each of the three points means the factor 2 is built into the definition of D0 and cannot be dropped — it is the same two-sidedness appearing as pair-requirement, two-root quadratic, and two-sided holonomy. [THE]

The dimension-graded ladder is therefore

```math
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
```

Equivalently, in compact form `Q(D)=\varphi^{D-4}`, the quantum equals `1` exactly at the anchor dimension `D=4`, and the half-gap cascade closes as `\delta_{-n}=\delta_0^{\,n+1}` [^b02-12].  This derivation is part of the finite operator grammar.  It is not a numerological use of `\varphi`, and it is not an independent scaling convention.

The downstream forcings that consume this spine — `Q_8`-Dedekind minimality (above), the icosian-ring `\to E_8` carrier, the `\xi_5=\varphi^{-5}` torus address defect, the kernel-30 zone split `30=8\oplus10\oplus12` with its mixing-hierarchy inversion (rank-3 non-degenerate = small quark mixing vs. degenerate kernel-30 = large lepton mixing), the PMNS `\delta_0`-family, the CKM Wolfenstein quad, the `(\mathbb Z/44)^*` window group, the vacuum cubic, and the seven-incarnation `\mathbb Z_2` registry — are carried in BOOK_02 §02.2.5 and the relevant downstream books; this section supplies only the φ / `δ_0` / dimension-ladder / `Ω_8`-carrier forcings they all inherit.
## 02.6 Condensed admissibility and finite response

The ambient condensed mapping space is not physics by itself. D0 works with a restricted subfunctor:

```math
\mathcal M^{D0}(S_{D0}^{\varphi})\subset \mathcal M(S_{D0}^{\varphi}).
```

A morphism is D0-admissible only if it factors through finite stages, has a detector channel, induces a positive response, admits a halt quotient and gives a stable record under re-detection.

At finite stage:

```math
\mathcal H_N=\mathbb C^{S_N},
\qquad
\mathcal D_N:\mathcal H_N\to\mathcal K_N,
\qquad
R_N=\mathcal D_N^\dagger\mathcal D_N\ge0.
```

The normalized finite readout is:

```math
P_N(a)={\operatorname{Tr}(\Pi_a R_N)\over\operatorname{Tr}(R_N)}.
```

This is the mathematical home of the Born/Hilbert trace ratio. Sector books may discuss physical detectors, but the finite positive response functional is defined here.

## 02.7 Action, gate and scene calculus

The action stack is a finite admissible operator family, not a variational metaphor. The key objects are:

```math
S_{gate},\qquad J_{scene},\qquad \mathcal G_{spec},\qquad W_A.
```

The scene functional is a constraint certificate. It selects finite scene structure under addressability, non-monopoly verification and finite response. The graph scene `K(9,11,13)` is therefore not an arbitrary postulate; it is the selected carrier for the finite detector grammar after the `ABCD × {±} -> Omega8 -> V9` lift.

Book 03 will own the action/operator dynamics as a sector of construction. Book 02 owns the proof form and the guardrails: no continuous polynomial fitting, no untyped scene variation, and no external table as an input to `J_scene`.

### 02.7A The Holographic Self-Reading Principle as single root

The invariants of the mathematical spine are not an unordered list of lucky formulas. They are deductive consequences of one root: a finite carrier must *read itself* with no external catalog (M1; forcing-by-contradiction, DEF-0.2.2). Reading-without-a-catalog means the carrier's own boundary record is the only admissible generator of its dynamics — a holographic self-reading constraint. The four spine invariants below are the forced shadows of that single requirement [^b02-13].

**[THE] 02.7A.1 (Quadratic response is forced — Gleason loophole closure).** The self-reading map lives on a 2D retained/archive phase pair and must preserve the boundary area it reads, since area is the only catalog-free measure available to it. An area-preserving readout on a 2D phase cell admits no admissible *linear* scalar response: a linear functional on the retained amplitude bypasses the archive coordinate and so fails to be a function of the area the carrier actually records. The unique scalar response compatible with finite positivity, phase symmetry, and 2D area preservation is **quadratic**. This is exactly where Gleason's theorem leaves a loophole at low dimension; the D0 area-preservation constraint closes that loophole by construction rather than by dimension count [^b02-14]. The quadratic readout is then *used* in proof form in §02.8 ([THE] 2.12, Quadratic Readout Form); §02.7A supplies the *why*.

**[THE] 02.7A.2 (φ is forced — Fibonacci fusion and Jones subfactor index).** The self-reading carrier has exactly one nontrivial fusion channel: reading a state alongside its own archive reproduces the Fibonacci fusion rule `1 × 1 = 1 ⊕ 1`. The minimal index of a subfactor realizing this single-channel fusion is the Jones index `[M:N] = φ²`, whose unique generator above the integer floor is

```math
\varphi=\frac{1+\sqrt5}{2},\qquad p+p^{2}=1\ \Rightarrow\ p=\varphi^{-1}.
```

So φ is not posted; it is the smallest subfactor index that a catalog-free binary self-reading can carry. The full derivation of φ from `p+p²=1` and of `δ₀=(√5−2)/2=1/(2φ³)` is owned by BOOK_01 §01.6; §02.9 ([LEM] 2.14) re-uses the positive root in detector-asymmetry form [^b02-15].

**[THE] 02.7A.3 (log-det is the forced generating functional).** Area-preserving self-reading dynamics are symplectic on the retained/archive pair, and the catalog-free generating function of an area-preserving flow is the logarithm of a determinant: `log det` is the unique additive potential whose gradient reproduces the area-preserving update. Hence the feedback operator `F_N` enters the spine through `log det F_N` rather than through any fitted polynomial — the no-continuous-fit guardrail of §02.7 is a corollary of holographic self-reading, not an independent stipulation [^b02-16]. The `F_N` operator itself is owned by BOOK_01.

**[LEM] 02.7A.4 (N_act = 38 as the holographic rank/nullity index).** Read holographically, the active action coefficient is a homological index of the minimal self-reading carrier: it counts the catalog-free boundary degrees of freedom (nullity) against the bulk frame they are read against (rank). For the selected scene `K(9,11,13)` with `|V|=33`, `Rank=3`, the nullity shell is `|V|−Rank=30` and the carrier's catalog-free index closes the forward/return self-reading cycle at

```math
N_{act}=2\,N_{unlock}=2(2\gamma-1)=38,\qquad \gamma=\frac{|V|-\operatorname{Rank}}{\operatorname{Rank}}=10.
```

The holographic reading and the weak-unlock derivation are the *same* index from two directions: §02.19.2 derives `38` as the closed forward/return weak-unlock cycle, and §02.7A names *why* that closed cycle is the homological rank/nullity index of the minimal holographic carrier. This book keeps its own §02.19.2 derivation as the operative one (BOOK_03 owns `Λ_act=38` as the single action section); §02.7A supplies the unifying root, not a competing count [^b02-17].

These four are one statement. Drop holographic self-reading and the spine loses its forcing: the response could be linear, the index could be any subfactor value, the generating functional could be any fitted potential, and `38` would be a calibration rather than a homological index. Keeping the root keeps all four forced together.

## 02.8 Universal quadratic readout

D0 observables are quadratic responses of finite operators:

```math
R=\mathcal D^\dagger\mathcal D.
```

The universal readout form is a normalized trace, determinant, Schur complement or finite spectral functional only after the support, probe and quotient have been fixed. This protects the theory against fitting by replacing a free parameter with a typed finite operator.

The general readout grammar is:

```math
\text{support}\rightarrow\text{operator}\rightarrow\text{positive response}\rightarrow\text{finite quotient}\rightarrow\text{comparison protocol}.
```

## 02.9 Minimal positive-response theorem for the base equation

The base equation used in Book 01 is not a free scalar axiom. It is the normalized scalar shadow of the minimal finite positive-response detector.

**Definition.** A primitive D0 detector audit is a finite-stage two-branch system `(L,R)` with a direct branch `L`, a return branch `R`, one halt quotient, and a positive response functional. Let `p\in(0,1)` be the direct branch contraction. Since the return branch is the first completed positive response of the same registered channel, its primitive scalar weight is the finite composition weight

```math
w(R)=p\cdot p=p^2.
```

The primitive audit is normalized by a single unit section:

```math
w(L)+w(R)=1.
```

Therefore

```math
p+p^2=1.
```

**Uniqueness.** The function

```math
f(p)=p^2+p-1
```

is strictly increasing on `(0,1)`, with `f(0)=-1` and `f(1)=1`. Hence the admissible branch weight is unique:

```math
p=\frac{\sqrt5-1}{2}=\varphi^{-1}.
```

**Exclusion of alternatives.**

- `p+p=1` has no nonlinear return response and collapses the audit to symmetric naming.
- `p+p^k=1` with `k>2` is not primitive: it contains the quadratic return plus additional unresolved iterations, hence extra hidden memory before halt.
- `p+p^\alpha=1` with non-integer `\alpha` is not a finite constructive channel composition in the profinite detector category.
- `p+q=1` with free `q` introduces a second independent branch scale and violates the single-section/no-monopoly rule.

Thus the equation is derived relative to the D0 primitive detector obligations. The obligations themselves are the primitive thesis; the scalar equation is their first theorem. The closed form `p=\varphi^{-1}` and the canonical residue `\delta_0=(\sqrt5-2)/2=1/(2\varphi^3)` are owned by BOOK_01 (see BOOK_01 §01.6); this section supplies only the minimal-positive-response forcing that selects them.

## 02.9A The holographic commutator [J,Y] and the symplectic origin of ħ

The same finite-detector discipline that forces the base equation also forces the *non-commutativity* that downstream books call quantum. Book 02 keeps the proof; BOOK_01 owns the K(9,11,13) scene that supplies the rigidity input (see BOOK_01 §01.8, the `ABCD × {±} -> Omega8 -> V9` lift).

**[DEF] Bulk/Boundary instruments.** Let `J` (Puncture / Localization) be the operator that instantiates a topological defect inside the retained Archive Bulk, and let `Y` (Closure / Compactification) be the trace-out operator projecting the Bulk onto the Active Boundary. `J` localizes a state in the bulk; `Y` reads its boundary projection. Both are admissible finite instruments in the role alphabet, not exogenous postulates.

**[THE 2.9A] Discrete origin of quantum uncertainty — ħ is derived, not postulated [^b02-19]. [^b02-18].** The holographic commutator is forced nonzero,

```math
[J,Y]\neq 0,
```

by the discrete rigidity of the K(9,11,13) carrier. Proof form (⊥): suppose `[J,Y]=0`. Then localizing a defect in the Bulk and reading its Boundary projection commute, i.e. there is a simultaneous eigenbasis in which a state is sharply localized in the rigid carrier *and* its trace-out is exact. But K(9,11,13) has rank 3 / nullity 30: the localization data `J` lives in the rank-3 distinguishing sector while the trace-out `Y` quotients by the 30-dimensional nullity, and no finite reindexing of a rigid carrier can make these two projections share an eigenbasis without admitting an exogenous catalog to label the coincidence — forbidden by M1. ⊥. Hence `[J,Y]\neq0` is rigidity-forced, not assumed.

The algebraic remainder of this commutator defines the minimal irresolvable symplectic phase-space area. The quantum of action `\hbar` is exactly the **symplectic capacity** of this obstruction:

```math
\hbar = c_{\mathrm{symp}}\big([J,Y]\big),
```

a derived invariant of the K(9,11,13) commutator, not a postulated constant. Heisenberg uncertainty

```math
\Delta x\,\Delta p \ge \frac{\hbar}{2}
```

is then the macroscopic shadow of the fundamental topological incompatibility between localizing a state in the Bulk (`J`) and perfectly reading its Boundary projection (`Y`). The Newton bridge `G\sim \ell_P^2 c^3/\hbar` *uses* `\hbar`; this theorem is where `\hbar` is sourced.

Owner: Book 02. Downstream books cite [THE 2.9A] for the discrete origin of `\hbar` and may not reintroduce `\hbar` as a free input.
## 02.10 Runtime, entropy and finite S-matrix

For evolution and scattering, Book 02 fixes the algebraic forms; Books 06--08 own the sector interpretations.

Entropy is archive forgetting or finite dephasing, not an independent thermodynamic postulate:

```math
\rho_N\longmapsto\Delta(\rho_N),
\qquad
S_N=-\operatorname{Tr}(\rho_N\log\rho_N).
```

The finite S-matrix registry is typed by admissible vertices and transition probabilities:

```math
P_{i\to f}={|S_{fi}|^2\over\sum_j |S_{ji}|^2}.
```

A scattering formula is admissible only when it names its finite support, vertex class, response and bridge to an external cross-section or detector record.

### 02.10.0 Test-extensionality: identity is what the checking procedure cannot tell apart

Runtime objects are typed constructively (codes plus a finite decidable membership predicate, see BOOK_01); the identity criterion on such objects is forced, and the whole runtime/S-matrix calculus below quotients by it.

**[THE] Extensionality-by-test.**  If $\forall x\,\bigl(\chi_A(x)=\chi_B(x)\bigr)$ then $A\equiv B$.

*Forcing.*  Suppose $A\not\equiv B$ yet no admissible test separates them.  Then the residual distinction is not fixable by the checking procedure, so pinning it would require an external catalog — an exogenous label that decides identity from outside the corpus.  M1 forbids exactly such a catalog, so the distinction collapses: $A\equiv B$ [^b02-20].  This is the M1 identity criterion that grounds the distinguishability program: identity *is* test-indistinguishability, and every runtime readout, registry entry and S-matrix amplitude below is an equivalence class under it.

### 02.10.1 Proof cell: finite φ-runtime and terminal quotient ideal

**Claim.**  Runtime is finite in the core D0 calculus; continuum evolution is an external bridge.

**Support.**  The support is the finite admissible detector ladder after the φ halt quotient.

**Runtime/window.**  A finite runtime readout is read over the four-step active window

```math
u_{k+1}=\delta_0u_k,\qquad k=0,1,2,3,
```

with response functional

```math
\mathcal R(P,u_0)=
\sum_{k=0}^{3}(1-\delta_0)\delta_0^k
\operatorname{Tr}(PG^+H_k).
```

**Stop ideal.**  Terms below the `I_12` resolution threshold are not active observables.  They may appear only as bridge diagnostics or as archived residuals, not as new physical correction layers.

**Quadratic readout.**  The observable part of the runtime is the positive trace response above; the formal infinite tail is not an observable D0 object.

**Falsification hook.**  If a claimed core scalar requires active discrimination below the terminal quotient ideal, or if the finite four-step window cannot reproduce the declared readout type, the claim is demoted before any external comparison.

### 02.10.2 The continuum as a forced inverse-limit: φ-ultrametric uniqueness

The continuum that a finite runtime approaches is not an actual-infinity object but the projective limit of the finite levels $V_k$ of the inverse system, refined under a φ-graded metric.  The metric — and the uniqueness of the limit — are M1-forced.

**[REM] φ-ultrametric Baire convergence.**  Set $d(\mathbf A,\mathbf B):=\varphi^{-k_0}$, where $k_0$ is the first level at which $A_k\equiv_{\kappa_k}B_k$ fails.  Then $d$ is a Baire-type ultrametric on the space of refinements, and κ-stability of a refinement sequence is exactly the Cauchy condition in $(\cdot,d)$.

*Forcing (uniqueness of the limit).*  The κ-stable limit exists in the completion and is unique.  Were two distinct κ-stable interpretations to converge for the same classical entity, selecting between them would demand exogenous parameters — an external choice not derivable from the corpus — which M1 forbids.  Hence the correct κ-stable posing, if it exists, is unique [^b02-21].  The φ-grading $\varphi^{-k_0}$ ties the resolution depth to the spine constant $\delta_0=(\sqrt5-2)/2=1/(2\varphi^3)$ owned by BOOK_01: each refinement level costs one φ-power of metric resolution.

**[THE] ZFC only as the internal language of constructive types.**  ZFC is admissible in D0 *only* as the internal language of constructive types, where every statement carries a test / distinguishability procedure.  Any part of classical ZFC that requires actual infinity or oracles — including "absolute" limits with no κ-protocol — is, in D0, an ill-posed statement [^b02-22].  Power-set and replacement survive only in their testable restrictions: $\mathcal P(A)$ as the constructive type of definable subsets cut out by computable predicates $\chi$ on $A$, replacement as computable maps whose values are buildable/checkable in finite resource.  The oracle and actual-infinity fragments are not "false" — they are *not statements* of the corpus, because they name no test.

### 02.10.3 Runtime as navigation, not search: the global potential complexity cell

**Claim.**  A finite-resource search "find $s$ with $Acc(s)=1$" is solved by directed descent along a global potential, never by brute enumeration; the worst-case exponential branch is M1-forbidden whenever the holonomy channel is open.

**[DEF] Global navigation potential $V$.**  For a search task, the numerical-verification package is a computable global potential $V:\mathrm{Vtx}(\mathcal G)\to\mathbb Q(\varphi)$ on the state graph that drives gradient/relaxation navigation and descends monotonically to a solution, with no brute search [^b02-23].  $V$ is the central object that *replaces* search by directed descent.

**[LEM] No navigation without $V$.**  If no global $V$ exists, any algorithm claiming a search speedup must mark which branches are promising — i.e. store an external branch index.  Such an index is not derivable from local checkability, so it is an external catalog and is M1-forbidden.

*Forcing.*  Direct application of the reduction-to-⊥ scheme via exogenous parameters (DEF-0.2.2; the branch index is precisely the catalog the contradiction excludes) [^b02-24].

**[LEM] $V$ as heat-trace relaxation.**  Let the boundary $B:=Acc\cup Rej$ carry the accept/reject label $b$ with $b|_{Acc}=1$, $b|_{Rej}=0$.  Then the canonical potential is the harmonic relaxation of that label,

```math
V:=\lim_{u\to\infty}e^{-uL}\,b,
```

with $L$ the CORE-fixed symmetric graph Laplacian and $u=\varepsilon^2 t$ the canonical (heat-trace) time scale.  $V$ is the "reachability of a solution" read off the same heat-trace channel that BOOK_01 uses for spectral geometry — here repurposed as a search-navigation potential [^b02-25].

**[THE] $V$ is a CORE-object when the holonomy channel is open ($D\ge6$).**  If the system admits the $D\ge6$ regime (cycles/holonomy present, the memory/relaxation channel open), then $V$ exists as a CORE-object — no external tables — and is fixed canonically by the corpus.

*Forcing (minimality + ⊥).*  (i) In $D\ge6$ the history contribution is fixed by the holonomy class $\mathrm{Hol}(\gamma)$, so cycle information is not lost and needs no external index.  (ii) Heat-trace supplies a canonical relaxation with no external scale, so $e^{-uL}$ and the $u\to\infty$ limit are defined without tuning.  (iii) Were $V$ to depend on an external setting (precision, step, basis), a parameter catalog would be required — M1-forbidden (THE 0.4.1).  Hence $V$ exists and is canonical [^b02-26].  The $D\le5$ vs $D\ge6$ topological fork is the load-bearing case split: only the no-holonomy phase can lack a canonical $V$.

**[THE] $V$ is computable without infinite precision.**  In D0 an observable is fixed to finite order by the $\varepsilon^2$ protocol, so $V$ need only be computed to the canonical tolerance $\varepsilon^2$.  The $\varepsilon^2$ tolerance therefore caps the number of relaxation steps in $u$: arbitrary precision ("how many digits do we need") is itself an external catalog and is M1-forbidden, so only the corpus-fixed tolerance is admitted.  The relaxation iterations are bounded by the protocol, carry no exponential branching, and the cost is $\mathrm{poly}(n)$ $\delta_0$-ticks in the D0 resource metric [^b02-27].  This is the "why poly" step: the tolerance, not a convergence assumption, bounds the work.

**[THE] Polynomial relaxation via the Lyapunov functional $V_k$.**  For the class $\mathbf{NP}_{D0}$ — tasks given by a finite predicate $\chi(x)$ on a constructive type and realized on the finite levels $V_k$ of the inverse system — if each level $k$ carries a global heat-trace functional $V_k$ (a Lyapunov function) under which coarse-graining is a monotone descent $V_k\downarrow$ that separates admissible solutions by a spectral gap $\Delta_k>0$, then search reduces to spectral relaxation, executable in $\mathrm{poly}(|\mathrm{Rep}(x)|)$ per fixed level [^b02-28].

**[COR] Constructive-phase collapse $\mathbf{NP}_{D0}\subseteq\mathbf{P}_{D0}$.**  If $\Delta_k\ge\Delta>0$ holds across the whole level family (a spectral phase without criticality), then $\mathbf{NP}_{D0}$ admits a polynomial solver on the physical D0-geometry carrier, i.e. $\mathbf{NP}_{D0}\subseteq\mathbf{P}_{D0}$.  *This is not, and does not claim to be, the ZFC $\mathbf P\overset?=\mathbf{NP}$ question*: it is a statement about the regularized computational model with a fixed UV cutoff and holonomic memory topology, where every task names a test [^b02-29].  The disclaimer is part of the claim — without the fixed cutoff and the test requirement, the statement would not be a corpus statement at all.

**[LEM] Worst-case collapse is the no-holonomy $D\le5$ phase.**  Instances demanding exponential enumeration are exactly the states with no global navigation potential, topologically the $D\le5$ tree / near-tree phase.  In $D\ge6$ the holonomy channel makes the global potential canonical (heat-trace relaxation), so adversarial hardness can only enter as exogenous parameters of instance/encoding/precision choice — M1-forbidden [^b02-30].  Worst-case hardness is thus not a property of the problem but a smuggled external catalog, and the reduction-to-⊥ removes it.

**Falsification hook.**  If a search admissible in the corpus exhibits genuine exponential branching with the holonomy channel open ($D\ge6$, $\Delta_k\ge\Delta>0$), or if some $V_k$ fails monotone descent without an exogenous parameter being introduced, the $\mathbf{NP}_{D0}\subseteq\mathbf{P}_{D0}$ cell is demoted before any external comparison.
## 02.11 Matter, baryon, meson and hadron proof blocks

Book 02 records the proof grammar for matter-sector support. It does not claim full empirical completion of all hadron multiplets. The current theorem status is:

- baryon exact Hodge support: core support;
- Schur-complement nucleon line: core measurement;
- terminal-destructive proton readout: single-section output;
- neutron beta/archive split and lifetime unlock: single-section output;
- meson lower-Hodge seed: support only, not direct pion mass;
- full `N, Delta, Lambda, Omega` transfer: no-go for the current operator set unless a new invariant spin/flavour transfer operator is derived.

This distinction prevents the old error `support = physical mass`.

### 02.11.1 Proof cell: Schur-complement nucleon core

**Claim.**  The nucleon core is a Schur-complement readout of the baryon support operator, not a direct baryon mass.

**Support.**  The baryon support is the weighted 2-simplex Hodge sector of `K(9,11,13)` with positive support gap

```math
\lambda_{B2}=3960.
```

**Probe.**  The proton-like charge probe has quadratic charge readout

```math
Q^2={4\over9}+{1\over9}+{1\over9}={2\over3},
```

so the first active nucleon block is

```math
\lambda_0=Q^2\lambda_{B2}=2640.
```

**Finite operator.**  The degenerate gap space has dimension

```math
(V_{11}-1)(V_{13}-1)=120,
```

and the witness projector satisfies

```math
P_{gap}P_wP_{gap}={1\over9}I_{gap}.
```

With witness weight `eta_w=1/8`, the first shift is

```math
\Delta_1={1\over72}.
```

The Schur complement against the complement of the degenerate gap contributes

```math
\Delta_2={1\over1710720}.
```

The bulk gate shift is

```math
\Delta_{bulk}={2\over3}+\delta_0.
```

**Readout.**  The integrated finite readout is

```math
\lambda_{N-core}=2640.7985901288725.
```

**Guardrail.**  `lambda_B2`, `lambda_0` and `lambda_N-core` are support/core readouts.  None of them is a proton mass until the terminal destructive readout and single action section are applied.

### 02.11.2 Terminal-destructive readout and the 306 action-cost theorem

The proton row is not allowed to contain a naked subtraction.  The number `306` is a finite operator trace in the destructive terminal readout channel.

Let the baryon support operator have the active 2-simplex structural uniqueness / negative-control rigidity gap

```math
\lambda_{B2}=3960.
```

Let the terminal shell, active terminal degree and transport layer be

```math
V_{13}=13,
\qquad
 d_{13}=V_9+V_{11}=9+11=20,
\qquad
V_{11}=11,
```

and let the active rank removed by the stop/gauge directions be

```math
\operatorname{Rank}=3.
```

There are two equivalent finite descriptions of the same terminal-destructive cost.

First, the terminal-shell trace plus the transport checksum is

```math
\Delta_p^{terminal}
=
{\lambda_{B2}\over V_{13}}
+
{\lambda_{B2}\over V_{13}d_{13}V_{11}}
=
{3960\over13}
\left(1+{1\over20\cdot11}\right)
=306.
```

Second, the destructive readout space is

```math
\mathcal H_{dest}
=
\mathcal H_{addr}^{\pm}\otimes\mathcal H_{tr}^{red},
```

with

```math
\dim\mathcal H_{addr}^{\pm}=2V_9=18,
\qquad
\dim\mathcal H_{tr}^{red}=d_{13}-\operatorname{Rank}=17.
```

For the canonical identity-cell operator

```math
M_{dest}=I_{18}\otimes I_{17},
```

the Hilbert--Schmidt action cost is

```math
\boxed{
\Delta_{readout}^{306}
=
\operatorname{Tr}(M_{dest}^{\dagger}M_{dest})
=18\cdot17
=306.
}
```

The equivalence of the two forms follows from

```math
\lambda_{B2}=2V_9d_{13}V_{11}=3960,
```

and

```math
d_{13}V_{11}+1
=20\cdot11+1
=221
=(d_{13}-\operatorname{Rank})V_{13}
=17\cdot13.
```

Thus `306` is neither a fitted proton correction nor a reusable lifetime constant.  It is a destructive-readout action trace.  The physical proton row may use it only in the terminal-destructive readout theorem; any use as a free hadronic parameter, second scale, or neutron-lifetime shortcut is invalid.

## 02.12 Gauge, electroweak, lepton and CKM proof obligations

The gauge and flavour claims are finite operator statements. Hypercharge normalization, electromagnetic runtime normalization, QCD runtime/archive scale, charged-lepton generation action and CKM terminal return are retained as typed claims with explicit guardrails.

The CKM rule is especially strict: a matrix or naming convention is not a physical proof unless the mass-basis terminal-return functor is fixed before comparison. A post-hoc permutation is forbidden.

## 02.13 Gauge and coefficient proof cells

### 02.13.1 Unique light gauge carrier

A D0-admissible compact positive light gauge carrier must preserve the signed detector cycle, rank and single-section anchor:

```math
\Omega_8=8,\qquad Rank=3,\qquad 1\text{ section anchor}.
```

Hence

```math
\dim\mathfrak g=8+3+1=12,
\qquad
rank\,\mathfrak g=4=ABCD.
```

The compact positive decomposition compatible with the finite carrier action is

```math
\mathfrak g=\mathfrak{su}(3)\oplus\mathfrak{su}(2)\oplus\mathfrak u(1),
```

up to finite global quotients and gauge/archive equivalence.  Non-compact real forms and additional light factors fail the positive-response and single-section tests.

### 02.13.2 Lorentz and Einstein--Hilbert carrier

External active readout has one runtime direction and three comparison directions, so the admissible external quadratic form has signature

```math
(1,3).
```

The geometric carrier enters through the four-dimensional heat trace

```math
\operatorname{Tr}e^{-s\Delta}\sim(4\pi s)^{-2}\int\sqrt g\,(a_0+a_1sR+O(s^2)).
```

The `a_1 R` term is the leading curvature channel compatible with locality, second-order dynamics and the four-role finite readout.  This is a carrier theorem, not a complete nonlinear catalogue of all gravitational solutions.

### 02.13.3 Hypercharge and carrier weak angle

The carrier normalization is

```math
k_Y={ABCD+1\over Rank}={5\over3}.
```

Therefore

```math
g_1^2={5\over3}g_Y^2,
\qquad
g_Y^2={3\over5}g_U^2,
```

and the carrier weak angle is

```math
\sin^2\theta_W^{carrier}
={g_Y^2\over g_2^2+g_Y^2}
={{3/5}\over 1+3/5}={3\over8}.
```

The carrier value is not the low-energy dressed measurement; runtime/radiative dressing is a separate typed layer.

### 02.13.4 Electromagnetic runtime normalization

The internal U(1) whitening value is

```math
\alpha_{top}^{-1}={359\over\varphi^2}-\varphi^{-5}=137.03562809503825.
```

##### 02.13.h Seam closure holonomy (the Closure-Holonomy Law) [^b02-alpha-hol]

The runtime electromagnetic normalization is the **closure holonomy** of the edge seam — the monodromy of one seam turn dresses `\alpha_{top}` to the measured value with **zero free real coefficients**:

```math
\alpha_{D0}^{-1}=\alpha_{top}^{-1}+\varphi^{-17}\bigl(1+h_{KS}\,\sin\theta_{seam}\bigr)=137.035999151,
```

where every ingredient is fixed *before* any comparison to data:

- depth `\varphi^{-17}=\varphi^{-5}\!\cdot\varphi^{-12}` — the seam `\xi_5` times the electroweak transport;
- stretch `h_{KS}=\ln\varphi` — the Kolmogorov–Sinai rate per monodromy turn, forced by the `\varphi` eigenvalue;
- angle `\theta_{seam}=2\pi_0(2-\varphi)=12/5` — **exact in `\mathbb Q(\varphi)`** with `\pi_0=(6/5)\varphi^2` (§04.6.π.4); `D0-PI0-DISCRETE-ANGLE-001`, Lean `D0.Geometry.Pi0DiscreteAngle`;
- channel `\sin` (off-diagonal), **not** the trace `\cos` — forced by `Q_8`, `G^2=-I`; `D0-Q8-SIN-CHANNEL-001`, Lean `D0.Spectral.SeamHolonomy`.

The `\approx 3.71\times10^{-4}` data residual of the runtime electromagnetic normalization is the seam closure holonomy derived above. The same law `1+h_{KS}\sin\theta_{seam}` governs the PMNS angles (§04.5), with the seam-amplitude `\delta_0`-degree set by cycle topology (`D0-SEAM-HOLONOMY-001`).

**Honest status split.** The *structure* — the angle `12/5`, the `\sin` channel, the depth `\varphi^{-17}`, the linear form — graduates to **THE** (machine-checked). The **9-digit agreement** with CODATA (`137.035999151` vs CODATA-2018 `137.035999084`, gap `6.7\times10^{-8}` — smaller than the 2018→2022 edition shift `9.3\times10^{-8}`) is an empirical **CHK** (`D0-ALPHA-HOLONOMY-002`, cert `vp_seam_holonomy_alpha.py`; the `\cos`/`\exp`/wrong-depth controls all FAIL). The last `\sim10^{-8}` is a falsifiable **HYP** measurement-limit bet (`D0-ALPHA-MEASUREMENT-LIMIT-001`). The 9-digit value is **never** registered as a THE derivation; second-order holonomy was checked and does *not* close the residual. The cone-angle `2\pi_0` and `\delta_0=(6/5)` micro-derivations lean on §04.6.π.4 — named proof-targets, not claimed here.

#### Consistency seam: the gluing anomaly `Δα` [^b02-31]

`α_top` is only the topological writing of the whitening value, read off the discrete scene/channel count.  The same constant `α^-1` admits a SECOND, independent algebraic writing read off the continuous packing/algebra:

```math
\alpha_{alg}^{-1}={2^{11}\pi_0\over\varphi^8}+{2\delta_0\over3}.
```

[DEF] The consistency residue (gluing anomaly) is the gap between the two forced writings:

```math
\Delta_\alpha:=\bigl|\alpha_{top}^{-1}-\alpha_{alg}^{-1}\bigr|.
```

[CHK] Under the fixed evaluation regimen of both sides, the residue stays inside the carrier tolerance:

```math
\Delta_\alpha\approx 4.15249\cdot10^{-4}
\;<\;
\varepsilon^2=\varphi^{-16}\approx 4.53104\cdot10^{-4}.
```

This is not a numeric check: since both writings are closed forms over `Q(φ)` (no data input), `Δα` is itself an **exact element of `Q(φ)`**, certified exactly —

```math
\alpha_{top}^{-1}=726-364\varphi,\qquad
\alpha_{alg}^{-1}=\tfrac{159739}{5}-\tfrac{294902}{15}\varphi,\qquad
\Delta_\alpha=-\tfrac{156109}{5}+\tfrac{289442}{15}\varphi ,
```

with `Δα ≠ 0` (its `φ`-coefficient is nonzero, so `Δα ∉ Q`, in particular `≠ 0`) and `|Δα| < φ⁻¹⁶ = 1597 − 987φ` proved by exact `Z[φ]` surd-sign analysis. What remains a theorem-target is only the *analytic owner* — deriving the algebraic writing `α_alg⁻¹` as a second-order/`π₀`-phase moment of the feedback resolvent — and the neutrino link `m_ν ∝ Δα²` stays a typed BRIDGE (the dimensionful step multiplies by `m_e`).

**The "second-order/`π₀`-phase moment" now has a precise finite meaning (`D0-DELTA-ALPHA-MOMENT-001`, sharpens the owner; does not close it).** Substituting `δ₀ = ½φ⁻³` collapses the algebraic writing into a polynomial in the single rank-3 archive unit `u = φ⁻³` (the per-excursion archive weight):

```math
\alpha_{alg}^{-1}=\mu_2\,u^{2}+\mu_1\,u,\qquad u=\varphi^{-3},\qquad
\mu_2={2^{11}\pi_0\over\varphi^{2}}={12288\over5},\qquad \mu_1={1\over3},\qquad \mu_0=0,
```

i.e. `α_alg⁻¹ = (12288/5)φ⁻⁶ + (1/3)φ⁻³` exactly in `Q(φ)` (Lean `D0.Spectral.DeltaAlphaMoment.delta_alpha_moment`; cert `vp_delta_alpha_pi0_moment.py`). This is precisely the shape of a depth‑≤2 Feshbach–Schur resolvent moment expansion `W_eff(z)=A+Σ_k z^{-(k+1)}B D^{k}C` (`D0-GENERATIVE-DYNAMICS-001`): the exponents `−6, −3` are `−2·rank` and `−1·rank` (moments at archive depth `k=2,1` in the rank‑3 unit `φ⁻³`), the **second** moment `μ₂` is the one carrying the `π₀=(6/5)φ²` feedback phase, and the vanishing constant `μ₀=0` is the mechanistic sign — *zero archive depth ⇒ zero anomaly* — forced, not fitted (the depth‑3 term `μ₃u³∼φ⁻⁹` is sub‑leading, consistent with the loop floor `φ⁻¹⁶`). **Honesty boundary:** what is forced and certified is the *shape* (degree‑2 in `φ⁻³`, no constant, `π₀`‑phase on `μ₂`); what stays frontier are the two *residue amplitudes* `μ₂=2¹¹π₀φ⁻²` and `μ₁=1/3`, which are the residues of `W_eff` at the pole, set by the `s→pole` continuation (the profinite spectral measure). So obligation 4 **narrows** from "no analytic owner" to "the depth‑2 `π₀`‑phase moment of `W_eff` in the unit `φ⁻³`, only the two residue amplitudes ↔ `s→pole` residues stay profinite." The factor `2¹¹` now has a named candidate — `2¹¹ = dim Cl(ℝ¹¹) = dim Λ*(ℝ¹¹) = 2^{|V_{11}|}`, the full exterior/fermionic-Fock dimension over the 11-element zone `V_{11}` (cert `vp_cvft_clifford_fock_capacity.py`), distinct from the irreducible `Spin(11)` spinor dimension `2⁵=32` and from the naive edge-pushforward pairing multiplicity `2`. The residue-extraction itself — that the `s→pole` residue of `W_eff` traces over the full `2¹¹` Fock space rather than the naive `2`-edge pairing — is owned by the Dixmier trace / noncommutative integral (owner edge `D0-DIXMIER-RESIDUE-OWNER-001`, `ASSUMP-DIXMIER-TRACE`). The **D0-internal scalar-trace selector** is now closed (`D0-ALPHA-MU2-FULL-LEDGER-001`, CERT-CLOSED): a scalar archive trace over the unresolved `V₁₁` block must sum over all `2¹¹` distinguishable subset states (the full Boolean ledger `Λ*(V₁₁)`); any subcarrier — the `Spin(11)` spinor `32`, the edge-pairing `2`, or `V₉`/`V₁₃` — requires an extra selector that the scalar trace and the support chain do not generate, hence an external catalog ⊥M1. So `2¹¹` is no longer a bare list-match but the **M1-forced** scalar-trace carrier (and `μ₂=2¹¹π₀φ⁻²=12288/5`). What remains the **external owner** is only the residue-extraction *realization* — that the physical `W_eff` `s→pole` residue **is** this scalar trace over `Λ*(V₁₁)` — owned by the Dixmier trace / Wodzicki residue (`D0-DIXMIER-RESIDUE-OWNER-001`, `ASSUMP-DIXMIER-TRACE`); the original `D0-CVFT-F1` residue route itself stays the closed-negative no-go.

**Closure-delta consolidation (Iteration 22).** The α-cluster is now stated as named closures: `μ₁ = Tr_R(p₁)/Tr_R(I_R) = 1/3` on the rank-3 carrier (`D0-ALPHA-MU1-RANKTRACE-001`, cert `vp_alpha_mu1_rank_trace.py`); the D0-internal algebraic object `α_alg⁻¹ = (12288/5)φ⁻⁶ + (1/3)φ⁻³` (`D0-ALPHA-ALG-CLOSED-001`, cert `vp_alpha_alg_closed.py`); and the seam invariant `Δα = |α_top⁻¹ − α_alg⁻¹|`, exact in ℚ(φ), nonzero, `0<|Δα|<φ⁻¹⁶` (`D0-DELTA-ALPHA-SEAM-CLOSED-001`, cert `vp_delta_alpha_seam_closed.py`). These consolidate the CORE Lean of `D0-DELTA-ALPHA-MOMENT-001` / `D0-DELTA-ALPHA-EXACT-001`; the only residual is the external Dixmier residue-extraction realization (`D0-DIXMIER-RESIDUE-OWNER-001`), and the measured 9-digit α is the closure holonomy `D0-ALPHA-HOLONOMY-002` (CHK).

[COR] [^b02-32]  `Δα≠0` is NOT a numerical error and NOT a defect of either writing.  Two independent reconstructions of the SAME constant — topological capacity (channel count) versus geometric phase `π_0` — cannot be glued to zero residue inside `Q(φ)`: the field `Q(φ)` is the smallest catalog-free arena that holds both, and it does not flatten the seam.  Hence `Δα` is the IRREDUCIBLE residue of gluing topological capacity to geometric phase.  This non-zero seam is forced, not fitted, and it is the seed of the sterile-sector mechanism (a measurable CORE residue; any probabilistic weight `P_sterile=f(Δα²)` built on it is a typed BRIDGE/HYP layer, since the linear sign of `Δα` is not observable).  The closure-holonomy dressing (§02.13.h) does NOT erase this seam; it dresses `α_top` toward the measured `137.035999`, while `Δα` records that the two algebraic origins were never identical to begin with.

**Honesty level (ξ₅ is THE, α is CHK).** `α⁻¹` is *not* a closed identity equal to the measured value. `ξ₅ = φ⁵ − 11 = φ⁻⁵ = 5φ − 8` is an exact identity (`D0-XI5-TORUS-DEFECT-001`, THE — `φ⁵ − φ⁻⁵ = L₅ = 11`), so the *structural form* `α_top⁻¹ = 359φ⁻² − ξ₅ = 726 − 364φ = 137.0356…` stands. But the equality to experiment does **not** close: the **data residual** `|α_meas − α_top⁻¹| = |137.035999 − 137.035628| ≈ 3.71×10⁻⁴` is a *different* quantity from the **algebraic residual** `Δα = |α_top⁻¹ − α_alg⁻¹| ≈ 4.15×10⁻⁴` above (the two must not be conflated). So the α-line remains **CHK** under the GOLDEN §16.3 boundary for its equality to experiment. The **data residual** `≈3.71×10⁻⁴` is *derived* as the seam **closure holonomy** (§02.13.h, `D0-ALPHA-HOLONOMY-002` — structure THE, 9-digit match CHK, last `~10⁻⁸` HYP), and the ζ-residue route (`D0-ALPHA-ZETA-RESIDUE-001` / `D0-CVFT-F1`) is **BLOCKED** (transcendental `∝1/lnφ` vs `α_alg ∈ Q(φ)`) — now **machine-checked** as a closed-negative no-go (`D0.Spectral.delta_alpha_residue_route_blocked`: `1/lnφ` is transcendental, hence `∉ ℚ(φ)`, so no `φ`-graded residue equals the algebraic `Δα`; proved relative to the one cited classical fact `ASSUMP-LINDEMANN-LNPHI`, transcendence of `lnφ`); the holonomy is the working route. The 9-digit data match is never promoted to THE; `ξ₅` stays THE.

### 02.13.5 QCD runtime and archive scale

The strong coupling runtime readout at the electroweak scale is

```math
\alpha_s^{D0}(M_Z)=
2\Omega_8\alpha_{D0}q_{mass}^{-6}
\left({\pi_0\over\pi}\right)^{2d_9-2/Rank}.
```

With

```math
\Omega_8=8,\qquad Rank=3,\qquad d_9=24,
```

```math
q_{mass}=(1+\delta_0^3)^{-1}=0.9983582475962778,
\qquad
\pi_0={6\over5}\varphi^2=3.1416407864998739,
```

this gives

```math
\alpha_s^{D0}(M_Z)=0.117999943841492,
\qquad
g_3^{D0}=1.217715495224055.
```

The archive/confinement scale is typed separately:

```math
\Lambda_{QCD}^{D0}=\Lambda_{act}\varphi^5q_{mass}^{-(d_9+2Rank)}=226.229639977528\,\mathrm{MeV}.
```

The active colour selection rule is triality zero:

```math
(n_q-n_{\bar q})\bmod3=0.
```

#### Why `π_0` and not `π` in the runtime: the counter-term ban [^b02-33]

The factor `(π_0/π)` carries a forced asymmetry: `π_0=(6/5)φ²∈Q(φ)` is a CORE structural constant (no external catalog), whereas classical `π` is a LIMIT of discretization refinements and is only ever available at BRIDGE status.  D0 may not silently substitute `π` for `π_0` inside a CORE formula, because the substitution would import an external precision catalog.

[LEM] Counter-term ban [^b02-34].  Suppose one tries to "correct" a finite observable `F_k` toward an ideal value by appending refinement counter-terms,

```math
F_k^{new}=F_k+\sum_{n=1}^{N(k)}c_n\,G_{n,k},
```

with `G_{n,k}` corrections NOT fixed by pro-compatibility and `c_n` chosen "as the refinement proceeds".  Then the set `{c_n}` is a MANDATORY external catalog, hence an M1-violation, because (a) without it the observable `F` cannot be reproduced by a second executor; (b) it cannot be derived from any finite distinguishability protocol; (c) it admits infinite recursion of "one more term".  Therefore CORE admits only observables fixed by the whole pro-family rule `F_{k-1}∘π_{k→k-1}=F_k`; anything carrying free `c_n` is BRIDGE/APPX and may not be declared part of the continuum.  ∎

[THE] Central decomposition `A=B+C_k+r_k` [^b02-35].  Every pro-observable value splits as

```math
A_k=B+C_k+r_k,
```

with `B` the stabilized continuum part (k-invariant CORE object), `C_k` the level-`k` structural part fixed by canonization (NOT a free parameter), and `r_k` the κ-residue obeying `|r_k|≤Kκ_k` with `r_k→0`.  Thus the continuum value `A_∞:=B` exists WITHOUT any appeal to actual infinity, and `r_k` is a bounded κ-residue, never a tunable counter-term.  This is the licence that lets the `(π_0/π)` factor sit in a CORE runtime: `π_0` is the `B`-part, the discretization gap toward `π` is absorbed in the controlled `C_k+r_k`, and no infinite catalog is invoked.

[THE] M1+ uniqueness of the limit [^b02-36].  If one classical entity admitted two distinct κ-stable interpretations, choosing between them would require exogenous parameters, which M1 forbids; hence the correct κ-stable reading, where it exists, is UNIQUE.  This is what makes `π_0` and the runtime formula above well-posed rather than one convention among many: the continuum `R_{D0}` is itself defined point-free, as the locale/sheaf of locally constant pro-observables over `\varprojlim V` [^b02-37], so a CORE constant is the unique κ-limit of its refinement family, not a chosen decimal.

### 02.13.6 Analytic proof cell for the electromagnetic residual exponent

The residual exponent in the electromagnetic runtime normalization is not a fit parameter.  It is a finite carrier-cell exponent.

The leading rational part is

```math
{5\over 8}={ABCD+1\over \Omega_8}={4+1\over 8}.
```

The numerator `ABCD+1` is the four terminal readout roles plus the unit section.  The denominator `Ω_8` is the signed terminal octet.

The finite-cell correction is

```math
{1\over384}={1\over \Omega_8\,ABCD\,\dim\mathfrak g_{light}}
={1\over 8\cdot4\cdot12},
```

where

```math
\dim\mathfrak g_{light}=\dim\mathfrak{su}(3)+\dim\mathfrak{su}(2)+\dim\mathfrak u(1)=8+3+1=12.
```

Thus the exponent used in Book 04 is

```math
\eta_{EM}={5\over8}+{\delta_0\over384}.
```

This analytic cell is the proof obligation for the electromagnetic runtime normalization.  A script may verify the arithmetic, but the script is not the source of the exponent.  If the carrier is changed, `Ω_8`, `ABCD`, or `dim g_light` changes and this exponent is invalidated.

### 02.13.7 Laboratory isolation operator lemma

The clock-sector golden floor is a SECTOR assumption, not a global law.

[HYP] Clock-Sector Hypothesis 2.13A.  In the clock sector the fundamental feedback-return operator satisfies `F_N=φ^-2 P_N` exactly.  This is the minimal additional condition that promotes the universal PSD lower bound to the golden floor.  It is explicitly declared and may be relaxed in other sectors; it does not violate the single-action-section rule, being a sector-specific choice inside the existing framework.

Book 02 also owns the general finite-projector inequality used by the metrology and bridge layers.

[LEM] Laboratory Projector Bound 2.19 [^b02-38].  Let `Π_lab≤P_N` be the laboratory projector and split the environment as

```math
Q_{env}=I-\Pi_{lab}=Q_N+(P_N-\Pi_{lab}).
```

For the laboratory feedback-return operator

```math
F_{lab}=\Pi_{lab}U^\dagger Q_{env}U\Pi_{lab}
```

one has the operator inequality

```math
F_{lab}\succeq\Pi_{lab}F_N\Pi_{lab}.
```

*Proof.*  Substituting the environment split, the difference `F_lab-Π_lab F_N Π_lab` reduces to the archive contribution plus

```math
\Pi_{lab}U^\dagger(P_N-\Pi_{lab})U\Pi_{lab}=K^\dagger K\succeq0,
```

which is manifestly positive semidefinite, since `P_N-Π_lab≥0` factors as `K^†K`.  ∎

[REM] Status.  This lemma alone does NOT imply a universal `φ^-2` decoherence floor: it gives the projector inequality independent of any sector spectrum.  A golden lower bound requires the additional Clock-Sector Hypothesis 2.13A on the spectrum of the fundamental feedback-return operator.  The two are kept typed-apart: the inequality is general metrology, the golden floor is sector-declared.
## 02.14 Carrier, coefficient and gravity proof blocks

Carrier claims are not independent metaphysics. They are downstream carriers of the finite detector grammar. The light gauge carrier, Lorentz/EH carrier and F-theory admissible carrier are therefore classified as carrier/support bridges.

Metrology claims follow the single-section rule:

```math
c_{D0}=1,
\qquad
\ell_0/\tau_0=c_{D0}.
```

The Planck/Newton and length-depth maps are shadows of a finite action section, not second anchors. A proof fails if it introduces proton, `W/Z`, `G_N`, `H_0`, Planck or dark-sector data as an extra scale unless the row explicitly has external-bridge status.

## 02.15 Archive pressure and spectral transfer

The current canonical theorem schema for transfer is:

```math
C_{static}^{D0}\rightarrow L_D\rightarrow \operatorname{Spec}(L_D)\rightarrow S_{DE}(u)\rightarrow\mathcal T_{\mathcal O}^{D0}\rightarrow\mathcal O_{obs}.
```

The BAO/archive-pressure comparison protocol is a strong empirical example, but this book records the general typed rule: the static coefficient, finite spectrum and transfer window must be fixed before external comparison.

## 02.16 Archive/cosmology proof cells

### 02.16.1 Static archive-pressure coefficient closure

The static cosmological coefficient row is closed only as a single-section/bridge-output interface. It does not make `H_0`, `Omega_m`, `Omega_Lambda` or `r_d` primitive D0 constants. Those entries are external comparison coordinates attached after the finite archive coefficient and boundary operator are fixed:

```math
(H_0^{D0},\Omega_m^{D0},\Omega_\Lambda^{D0},r_d^{D0})
```

before any BAO or survey-shape transfer. The proof object is the fixed archive coefficient and associated finite boundary operator; survey residuals may not alter the bridge coordinates, and the coordinates themselves are not advertised as exact internally computed D0 observables.

### 02.16.2 S_DE finite-window archive-transfer shape

Given the fixed static tuple, the dynamic archive-pressure transfer has the typed form

```math
H_{D0}(z)=H_{\Lambda CDM}(z)\exp\Theta_{D0}(z),
```

with

```math
\Theta_{D0}(z)=A_cG_{log}(z;z_c,\sigma_c)-A_rG_{log}(z;z_r,\sigma_r)-\theta_0e^{-(z/\xi_5)^2}.
```

The logarithmic window is

```math
G_{log}(z;z_0,\sigma)=\exp\left[-{1\over2}\left({\log(1+z)-\log(1+z_0)\over\sigma}\right)^2\right].
```

The window parameters must be obtained before external comparison:

```math
z_c=\varphi(\lambda_c-1),\qquad z_r=\varphi(\lambda_r-1),
```

```math
\lambda_c=1.420943058495791,
\qquad
\lambda_r=1.5790569415042093,
```

```math
\sigma_c=\Delta D_{SDE}+\epsilon^2=\delta_0,
\qquad
\sigma_r={\sigma_c\over\sqrt\varphi},
```

```math
A_c={\sigma_c\over\sqrt5},
\qquad
A_r=A_c(\lambda_r-1).
```

This is the proof cell that prevents the BAO shape from being a hidden ansatz: centers, widths and amplitudes are derived from the finite spectral window and only then compared to survey data.

## 02.17 Claims owned or cross-owned by this book

| Claim | Status | Name | Stage | Forbidden shortcut | Falsification hook |
|---|---|---|---|---|---|
| `D0-FOUND-001` | CORE-FOUNDATION | No-monopoly verification algebra | Foundation | Do not derive phi from generic unitary contact, Helstrom scans, or entropy linearity alone. | A different internally normalized minimal non-monopoly audit algebra would pressure this row. |
| `D0-FOUND-002` | CORE-FOUNDATION | Minimal addressable record split | Foundation | Do not use delta0=phi^-3; active convention is 1/(2 phi^3). | A different direct/return closure with no external catalogue. |
| `D0-FOUND-003` | CORE-FOUNDATION | Minimal continuum-measurement skeleton | Foundation | Do not claim all mathematical cuts are φ; claim is minimal measured connected division. | A non-φ finite, path-independent, internally normalized detector split. |
| `D0-SCENE-001` | CORE-SUPPORT | Omega8 detector cycle | Detector Cycle | Do not treat phi alone as physical geometry before Omega8 closure. | Failure of detector-cycle construction or cycle count. |
| `D0-SCENE-002` | CORE-ACTION | J_scene selects K(9,11,13) | Gate/Action | Do not read J_scene as fitted polynomial for later constants. | Different admissible zero of the same typed obligations or wrong graph invariants. |
| `D0-MATH-001` | D0-RESOLUTION-EXACT | Finite phi-runtime and terminal quotient ideal | Quotient/Resolution | Do not add infinite correction layers below I12. | A physical scalar claim requires distinguishing below I12 inside D0 grammar. |
| `D0-ACTION-001` | CORE-ACTION | S_gate/J_scene backbone | Gate/Action | Do not close Born, entropy, leptons, or dynamics by unrelated formulas. | Mismatch between books or failure of Boundary Residual Eigenvalue r_∂ / I_B / action-spine consistency. |
| `D0-METRO-001` | CORE-FOUNDATION | Single causal line/tick invariant | Bridge/Dictionary | Do not count c as a second sector anchor. | Reproducible line/tick records require multiple elementary speeds. |
| `D0-METRO-002` | SINGLE-SECTION-OUTPUT | Lambda_act single action section | Single Section | No proton, W/Z, Planck, G_N, H0, or dark anchor as second scale. | Any closed prediction requiring an independent sector scale. |
| `D0-BOUND-001` | D0-RESOLUTION-EXACT | Boundary Residual Eigenvalue r_∂ and boundary curvature residual | Quotient/Resolution | Do not fit q_res with arbitrary scalar factor or reopen an infinite residual spiral. | Boundary residual cannot be produced below I12 by admissible cell. |
| `D0-QM-001` | CORE-MEASUREMENT | Born/Hilbert finite trace ratio | Quadratic Readout | Do not postulate continuum Hilbert space before finite trace. | Negative or unnormalized probabilities from finite Hessian readout. |
| `D0-THERMO-001` | CORE-MEASUREMENT | Finite-window entropy from archive forgetting | Quadratic Readout | Do not import continuum entropy postulate as core. | Non-finite trace or unnormalized window entropy. |
| `D0-DYN-001` | CORE-RUNTIME | Normalized tick and witness transport | Runtime | Reject raw T=A-phi^-1 I as propagation operator. | Non-normalized or non-positive dynamic readout. |
| `D0-VERTEX-001` | CORE-RUNTIME | Finite S-matrix registry | Linear Exchange | Do not compare raw graph amplitude directly to event count. | Failure of finite amplitude normalization or type split. |
| `D0-GAUGE-001` | CORE-RUNTIME | U(1) topological normalization and photon benchmark | Runtime | Do not treat gamma/Z interference or event counts as closed by photon-only cert. | Failure of whitening identity or photon benchmark arithmetic. |
| `D0-EW-001` | CORE-RUNTIME | W/Z runtime ratio and on-shell angle | Runtime | Do not use 3/13 or common-kernel variants as physical angle. | Failure to derive asymmetric kernels or trace ratio. |
| `D0-EW-002` | ACTIVE-PASSPORT | EW radial depth and Higgs anchor | Gate/Action | No M_Z second GeV anchor; no underived phi^35 ansatz. | Gate-action derivation fails or neighbouring admissible formula survives. |
| `D0-LEPTON-001` | CORE-MEASUREMENT | Charged-lepton operator selector | Gate/Action | No Lucas-number or inverse-cycle blow-up formula as premise. | Another admissible branch satisfies all criteria or selected branch fails. |
| `D0-LEPTON-002` | ACTIVE-PASSPORT | Charged-lepton generation action | Single Section | No fit-led Lucas or inverse-target selection. | Branch exponents/boundary factors not uniquely selected by action grammar. |
| `D0-CKM-001` | CORE-MEASUREMENT | PNO cyclic orientation CKM seed | Linear Exchange | No raw node-space RMS or row/column permutation. | PNO algebra does not select O_cyc/order. |
| `D0-CKM-002` | BARE-D0-READOUT | CKM mass-basis terminal-return closure | Quadratic Readout | No post-hoc permutation after seeing data. | Mass-basis/naming matrix not reproduced or not stochastic. |
| `D0-BARYON-001` | CORE-SUPPORT | Exact baryon Hodge spectrum | Finite Support | 3960 => proton mass is forbidden. | Counterexample to exact unweighted or weighted spectra. |
| `D0-BARYON-002` | CORE-MEASUREMENT | Charge-squared PDF minimality | Quadratic Readout | Do not import collider PDFs as D0 input. | Another admissible family point gives same target or Q^2 readout fails. |
| `D0-HADRON-001` | CORE-MEASUREMENT | Hadron Schur-complement nucleon core | Quadratic Readout | Do not read intact core directly as proton mass. | Schur identity or gap perturbation fails. |
| `D0-PROTON-001` | SINGLE-SECTION-OUTPUT | Terminal-destructive proton readout | Single Section | Do not use proton mass as anchor; do not reuse 306 as neutron shortcut. | 306 action trace or terminal formula fails. |
| `D0-NEUTRON-001` | SINGLE-SECTION-OUTPUT | Neutron beta/archive mass split | Single Section | Do not input neutron/proton masses. | Mass split operator fails or sign not justified. |
| `D0-NEUTRON-002` | SINGLE-SECTION-OUTPUT | Neutron beta/archive lifetime unlock rate | Runtime | Rejected 306/13 lifetime shortcut. | Exponent, phase-space power, or normalization cannot be derived/certified. |
| `D0-PHOTON-001` | CORE-MEASUREMENT | Photon massless carrier | Quadratic Readout | Do not introduce photon rest mass without breaking c_D0 line invariant. | Pure line carrier has nonzero rest-return defect. |
| `D0-NEUTRINO-001` | CORE-MEASUREMENT | Neutrino neutral leakage mass-square pattern | Quadratic Readout | Do not fit neutrino masses independently if electron section used. | Oscillation ratio excludes delta0/4 under correct bridge. |
| `D0-CARRIER-001` | CORE-SUPPORT | Unique light gauge carrier | Finite Support | Do not treat SM constants as primitive after carrier closure. | Alternative D0-admissible light carrier survives constraints. |
| `D0-CARRIER-002` | CORE-SUPPORT | Lorentz and Einstein-Hilbert carrier | Finite Support | Do not claim full nonlinear GR catalogue from carrier form alone. | No stable (1,3) or heat-trace R channel. |
| `D0-FTHEORY-001` | EMPIRICAL-PASSPORT | Lin-Weigand 2016 D0 admissible carrier | External Comparison Protocol | Do not promote raw string moduli disappearance or F-theory as D0 axiom. | Any component of F_D0 nonzero after correct quotient. |
| `D0-COEFF-001` | CORE-RUNTIME | Hypercharge normalization and carrier weak angle | Runtime | Do not confuse carrier 3/8 with measured low-energy angle. | Hypercharge index not selected by D0 carrier grammar. |
| `D0-COEFF-002` | CORE-RUNTIME | Electromagnetic runtime normalization | Runtime | Do not fit alpha by changing graph seed or q_res. | Runtime exponent not derived or value fails cert. |
| `D0-COEFF-003` | CORE-RUNTIME | QCD runtime and archive/confinement scale | Runtime | Do not confuse QCD archive scale with cosmological dark/archive pressure. | Coefficient formula or triality-zero selection fails. |
| `D0-MATTER-001` | CORE-RUNTIME | Matter/Yukawa/CKM operator closure | Bridge/Dictionary | No hidden mass scale, post-hoc permutation, or fit-led lepton/CKM constants. | Dressing comparison requires changing D0 source object. |
| `D0-GRAV-001` | SINGLE-SECTION-OUTPUT | Length-depth theorem and Planck/Newton shadow | Bridge/Dictionary | No raw edge-density G_N; no reduced-Compton convention at full-cycle section; no terminal denominator swap. | Semantic alternatives beat canonical depth under same typed obligations or cert fails. |
| `D0-GRAV-002` | SINGLE-SECTION-OUTPUT | Newton coefficient finite-cycle holonomy closure | Bridge/Dictionary | Do not patch hbar by pi0; do not introduce Planck/G anchor. | Holonomy exponent/transfer not derivable or coefficient fails cert. |
| `D0-GRAV-003` | D0-RESOLUTION-EXACT | Higher-curvature finite cut rule | Quotient/Resolution | Do not add free higher-curvature couplings below D0 resolution. | Continuum correction above cut requires active unclosed term. |
| `D0-COSMO-001` | CORE-MEASUREMENT | Archive-pressure operator | Quadratic Readout | Do not fit w_a as CPL free parameter inside D0. | Archive pressure sign/scale excluded under correct survey bridge. |
| `D0-COSMO-002` | ACTIVE-PASSPORT | Scalar survey amplitude comparison protocol | External Comparison Protocol | Do not compare raw (1+delta0/4)I_B directly to survey data. | Terminal normalization not uniquely derived or survey pass fails with fixed seeds. |
| `D0-COSMO-004` | SINGLE-SECTION-OUTPUT | Cosmological archive-pressure coefficient closure | Single Section | Do not alter H0/Omega/r_d to fit BAO; use transfer layer. | Static coefficient tuple excluded by fixed-parameter likelihoods. |
| `D0-COSMO-005` | EMPIRICAL-PASSPORT | S_DE finite-window BAO archive-transfer shape | External Comparison Protocol | Do not move H0/Omega_m/r_d or fit shape amplitudes to target data. | Future BAO/SN releases fail fixed transfer with no refit. |
| `D0-COLLIDER-001` | EXTERNAL-BRIDGE | Collider runtime typed bridge | Bridge/Dictionary | No raw amplitude-to-event-count comparison. | Bridge requires hidden D0 core fit parameters. |
| `D0-PI0-001` | CORE-FOUNDATION | pi0 finite-cycle versus pi continuum generator | Quotient/Resolution | Do not replace pi by pi0 inside hbar or Planck definitions. | Typed finite-cycle/continuum distinction inconsistent with bridges. |
| `D0-MESON-001` | CORE-SUPPORT | Meson lower-Hodge support seed | Finite Support | 400 => pion mass or sqrt(3960/400) => hadron ratio is forbidden. | Lower-Hodge calculation fails. |

## 02.18 Integrated rigidity calculus: local structural uniqueness / negative-control rigidity is a proof obligation, not a fit

The structural uniqueness / negative-control rigidity calculus belongs in the mathematical proof spine because it turns high-gain numerical formulae into uniqueness obligations.

For any downstream dimensionless readout \(Y(\varphi)\), define the local structural uniqueness / negative-control rigidity exponent

```math
\kappa_Y=\left.\frac{d\log Y}{d\log \varphi}\right|_{\varphi=\varphi_0}.
```

A closed D0 formula must declare whether a large \(|\kappa_Y|\) is forced by the detector construction or imported as a fragile numerical coincidence.  The representative structural-uniqueness / negative-control rigidities under the fixed stress convention are:

| readout | representative structural uniqueness / negative-control rigidity role |
|---|---:|
| gravity depth / \(G_N\) | large negative exponent from \(D_L\sim\varphi^{99}\), hence \(G_N\sim\varphi^{-198}\) |
| electroweak radial readout | high positive radial exponent |
| charged-lepton ratios | finite generation selector structural uniqueness / negative-control rigidity |
| survey scalar amplitude | archive/window structural uniqueness / negative-control rigidity |
| neutron lifetime | terminal weak factor structural uniqueness / negative-control rigidity, including powers of \(\delta_0\) |

This is not a phenomenological sensitivity table in the active proof path.  It is a no-deformation certificate: a nearby value of \(\varphi\) destroys the agreement between detector split, algebraic closure and downstream typed sections.

**Proof discipline.**  Any high-gain D0 expression must now be accompanied by one of the following:

1. an internal uniqueness proof;
2. a rigidity/no-deformation proof;
3. an explicit demotion to bridge/comparison protocol status.

This integrated rule strengthens the anti-numerology firewall: sensitivity is admissible only when it is the consequence of a closed invariant section.

### 02.18.1 The role-group rigidity floor: why the octet is forced to be `Q_8`

The deepest no-deformation certificate is not numerical at all — it is the rigidity of the *role group itself*.  The rigidity calculus above only has a fixed point \(\varphi_0\) to differentiate at because the algebra carrying the readouts is locked; that lock is `Q_8`, and it is forced, not chosen.  BOOK_01 §01.20 owns the role alphabet (the FACT \(\Omega_8=\mathrm{ABCD}\times\{\pm\}\), \(|\Omega_8|=8\)); this proof-spine book carries the *forcing* of why that octet must be the quaternion group, since the rigidity floor depends on it.

**[THE]** \(\Omega_8\cong Q_8\) [^b02-39].  The derivation is by contradiction from M1, in four forced steps:

1. *All subgroups normal.*  A non-normal subgroup has distinct conjugate copies, so the act would have to record *which copy* — an external catalog entry M1 forbids.  Hence every subgroup of the role group is normal.
2. *Non-commutative.*  Order memory (the trace `C` must remember the orientation in which `A`,`B` were composed) forbids a fully abelian group; the role group must be non-abelian.
3. *Hamiltonian.*  Non-abelian with all subgroups normal is exactly the definition of a *Hamiltonian* group.
4. *Minimality scan.*  Decidable scan of the non-abelian groups of order \(\le 8\) by count of non-normal subgroups: \(S_3\) has 3, \(D_4\) has 4, **`Q_8` has 0**.  `Q_8` is the unique order-8 Hamiltonian group, and Dedekind's 1897 theorem makes this minimality *global*, not merely order-bounded; the explicit structure — **every Hamiltonian group is `Q_8 × B × D`** with `B` elementary-abelian-2 and `D` abelian of odd order (R. Baer, 1933) — shows `Q_8` is a *forced factor* of every such group, so the second structural channel (Baer) and the rigidity floor (the triple identity `[Q_8,Q_8]=Z(Q_8)=Φ(Q_8)=\{\pm1\}`) name the same minimal object.  Therefore \(\Omega_8\cong Q_8\) is a theorem, not a model choice.

**[LEM] Triple identity (M1-cleanest group).**  `Q_8` is verified to satisfy
```math
[Q_8,Q_8]=Z(Q_8)=\Phi(Q_8)=\{\pm 1\}\cong\mathbb{Z}_2,
```
i.e. commutator (order memory), centre (the \(\{+,-\}\) orientation = irreversibility of write/erase), and Frattini (non-generating residue) all collapse onto a single \(\mathbb{Z}_2\).  This single-`\(\mathbb{Z}_2\)` coincidence is the algebraic statement of *no deformation*: there is no free parameter inside the role group to perturb, so \(\kappa\) is differentiated against a rigid base.  (cert: decidable group scan over order \(\le 8\) + identity check; see BOOK_01 §01.20 for the role-alphabet derivation it cites.)

### 02.18.2 The exact-arithmetic carrier: `Q_8 < 2T < 2I -> E_8`

The rigidity of `Q_8` does not stop at order 8; it propagates upward along an exact unit chain to the rank-8 even-unimodular lattice.  This propagation runs through the two pillars this spine already owns — the role group `Q_8` and the field \(\varphi\) — and is checked in exact \(\mathbb{Z}[\sqrt5]\) arithmetic (no floating point).

**[THE]** Golden quaternions generate \(E_8\) [^b02-40]:

1. *Icosian closure.*  The binary icosahedral group \(2I\) = 120 unit icosians (quaternions over \(\mathbb{Z}[\varphi]\), the vertices of the 600-cell); the full \(120\times120\) multiplication table closes **exactly**, every norm \(=1\).
2. *Subgroup chain.*  \(Q_8\subset 2T\subset 2I\) — roles \(\subset\) Hurwitz units \(\subset\) icosians — so the forced role group sits at the base of an exact tower of unit quaternion groups.  The quotient \(2I/\{\pm 1\}\cong A_5\) is the icosahedral rotation group = Shechtman quasicrystal point group (= the flavor group entering CKM/PMNS).
3. *Galois doubling to rank 8.*  The icosian ring (the \(\mathbb{Z}\)-hull of \(2I\)) has rank \(8 = 4\;(\text{quaternions})\times 2\;(\text{degree of }\mathbb{Q}(\sqrt5))\); the \(4\to 8\) doubling is exactly the Galois pair of \(\mathbb{Z}[\varphi]\).  Equip it with the trace norm \(\mu:\,a+b\sqrt5\mapsto a+b\).
4. *Even-unimodular certificate.*  At the correct scale the Gram matrix is divisible by 4, with \(\det(\mathrm{Gram}/4)=1\) and even diagonal — an even unimodular lattice of rank 8.  By Mordell's uniqueness theorem (the *only* even unimodular lattice in rank 8) **this lattice is \(E_8\)**; all 120 units land on the second shell (norm 4).

This is a genuine no-deformation certificate of the rigidity kind demanded by §02.18: the closure is checked by exact \(\mathbb{Z}[\sqrt5]\) arithmetic, not fitted, so there is no nearby deformed lattice — Mordell uniqueness leaves no free parameter.

**[DEF] cert spec.**  Build the \(8+16+96\) units as \((a,b)\)-pairs in the \(/4\)-lattice; quaternion multiply `qmul` through \(\mathbb{Z}[\sqrt5]\); assert exact closure; form the Gram matrix from the block form \(\begin{psmallmatrix}1&2\\2&5\end{psmallmatrix}\); assert \(\det/4=1\) and diagonal parity.  (Target status LEAN_PROVED; checked by the finite certificate.)

**Status: the even-unimodular certificate of point 4 is now executable and Lean-proved** (claim `D0-ICOSIAN-E8-GRAM-001`).  The finite-core shadow proves, in exact integer arithmetic (Python `vp_icosian_e8_gram_finite.py`, Bareiss) and in Lean (`D0.Claims.IcosianE8GramFinite`, `native_decide`), that the simply-laced \(E_8\) Gram (\(=\) Cartan) is symmetric with diagonal all \(2\) (**even**) and \(\det = 1\) (**unimodular**), with rank \(8 = 2\cdot4\) the \(\mathbb{Z}[\sqrt5]\to\mathbb{Z}\) Galois doubling.  The negative control \(A_8\) (the type-\(A\) chain) has \(\det = 9 \neq 1\), so unimodularity is forced by the \(E_8\) *tree*, not by the \(2\)-diagonal alone.  This certifies the *specific* lattice's defining invariants exactly; the step "this lattice **is** \(E_8\)" is the named external owner — **Mordell's genus-uniqueness theorem** (Mordell, *J. Math. Pures Appl.* **17** (1938) 41–46; cf. Conway–Sloane *SPLAG*), the unique even unimodular lattice in rank 8.  Forcing-uniqueness here is owned by a cited classical theorem, not asserted (BOOK_05 §05.8.R).

**[BRIDGE]** \(E_8\to\Lambda_{24}\) [^b02-41].  The Leech lattice \(\Lambda_{24}\) is built from the icosians by the established external construction (R. Wilson, *J. Algebra* 322 (2009) 2186; Conway–Sloan, *SPLAG* ch. 8).  Status is BRIDGE: this leans on a sixty-year-old external theorem and is cited, not re-proved here.  It is the honest, dimensionally-correct continuation
```math
Q_8\;\to\;\mathbb{Z}[\varphi]\text{-hull}\;\to\;\text{icosian ring}=E_8\;\to\;\Lambda_{24},
```
so the bridge from the roles to the Leech lattice passes exactly through the two pillars `Q_8` and the field \(\varphi\).

### 02.18.3 The dimension-8 forcing network [synthesis]

The order-8 / rank-8 objects above are not independent coincidences. A systematic search for
classical *forcing-owner* theorems (uniqueness/classification only) shows that the number **8**
is forced through a single network whose edges are each a cited classical theorem:

```math
\{\pm\}\to\mathbb{Z}_2\ (\text{Bott period }2)\ \to\ \text{ABCD}\times\{\pm\}=8=|\Omega_8|\ \to\ Q_8\subset 2T\subset 2I\ \to\ E_8\ \to\ \text{triality }Spin(8).
```

- **`8` as a boundary (Hurwitz, 1898).** The normed division algebras over `\mathbb{R}` are
  exactly `\mathbb{R},\mathbb{C},\mathbb{H},\mathbb{O}` of dimensions `1,2,4,8`; `8` is the last
  (associativity is lost at `\mathbb{O}`). This is the algebraic channel to `|\Omega_8|=8`.
- **Period 8 (Clifford / Bott).** Clifford algebras `Cl_{p,q}(\mathbb{R})` are 8-periodic in
  `(p-q)\bmod 8`, and real `KO`-theory is Bott-periodic with period 8 (complex `K`-theory with
  period 2, the `\mathbb{Z}_2` of `\{\pm\}`). A topological channel to the same `8`.
- **The unit-quaternion tower (Dedekind + icosians).** `Q_8\subset 2T\subset 2I` with orders
  `8\mid 24\mid 120` (§02.18.2); `Z(Q_8)=\mathbb{Z}_2` sits at the base.
- **`E_8` (Mordell).** The icosian ring is the unique even unimodular lattice of rank 8
  (§02.18, point 4; owner `ASSUMP-MORDELL-E8`).
- **Triality (`Spin(8)`, Cartan/Adams).** `D_4` is the unique Dynkin diagram with an `S_3`
  outer automorphism; it permutes the three 8-dimensional representations `V,\Delta_+,\Delta_-`.

The arithmetic skeleton of this network is machine-checked: claim `D0-DIM8-NETWORK-001`
(cert `vp_dim8_network.py`, Lean `D0.Synthesis.DimensionEightNetwork`) proves `8=2\cdot4`, the
tower divisibilities `8\mid24\mid120` with their indices `3,5,15`, the even-unimodularity of the
`E_8` Gram (reused from `D0-ICOSIAN-E8-GRAM-001`), and the three legs of `D_4` with
`|Out(Spin(8))|=|S_3|=6`. The periodicity/uniqueness *theorems* themselves are external owners,
cited not re-proved.

**Anti-numerology fences (BOOK_00 §00.9).** The network forces the *number* `8` and the rank-8
even-unimodular target — nothing more. Three resemblances are explicitly **outside** it: (i)
"`Spin(8)` triality `\Rightarrow` 3 fermion generations" is rejected — the `3` is the number of
8-dimensional `D_4` representations, not the number of families; (ii) the causal threshold
`C_max=3/8` is owned by the rank/`|\Omega_8|` posing (`D0-COMPACTNESS-DEF-FORCING-001`), not by
this network; (iii) `\Lambda_{24}\leftrightarrow` the readout kernel `K=30` is rejected
(`24\neq30`, no 24-dimensional D0 object) — distinct from the legitimate cited `E_8\to\Lambda_{24}`
*lattice tower* of the [BRIDGE] above. The `\varphi`-network (Jones `=` Fibonacci `=` Hurwitz `=`
Pisot `=` icosian, §01.21.3) and this 8-network meet at the icosians: `\varphi` and `8` are one
object, not two coincidences.

### 02.18.4 The zone matrix `M`: a stochastic spectrum, not the fractal tick [clarification]

The zone matrix `M=\begin{psmallmatrix}0&11/24&13/24\\9/22&0&13/22\\9/20&11/20&0\end{psmallmatrix}`
is the row-normalised equitable quotient of `K(9,11,13)`. Its characteristic polynomial does *not*
yield `\varphi^{-1}`; three numbers that are easy to conflate must be separated (claim `D0-LAPLACIAN-SPECTRUM-FIX-001`, cert `vp_laplacian_3x3_correct.py`). A reading that takes the zone matrix `M`'s characteristic polynomial to yield `\varphi^{-1}` is wrong, and the correction separates three numbers that are easy to conflate:

- **`M` is row-stochastic**, so `\rho(M)=1` exactly; its characteristic polynomial factors as
  `(\lambda-1)(\lambda^2+\lambda+39/160)`, giving eigenvalues `\{1,\,-\tfrac12\pm\tfrac{\sqrt{10}}{40}\}\approx\{1,-0.421,-0.579\}` — all inside the unit disk. `\varphi^{-1}\approx0.618` is **not** among them.
- The quadratic `160\lambda^2-480\lambda+359` (roots `\approx1.421,1.579`) that the reading
  hit is the characteristic polynomial of `(I-M)` under `\lambda\mapsto1-\lambda`: its roots are
  `1-\mathrm{eig}(M)`, i.e. the **`S_{DE}` relaxation window** of BOOK_08, not `M`'s own
  spectrum.
- The fractal tick `\varphi^{-1}` (the envelope recursion `A_{n+1}=\varphi^{-1}A_n`, BOOK_06
  §06.2) is a **different operator** entirely.

So there are two matrices, two spectra, two roles: `M`'s mixing spectrum `\{1,-0.42,-0.58\}`, the
`(I-M)` relaxation window `\{1.42,1.58\}` feeding `S_{DE}` (the Book02↔Book08 link), and the
envelope tick `\varphi^{-1}`. These three are distinct; conflating them is the error this cell
fences off.
## 02.19 High-gain uniqueness and structural uniqueness / negative-control rigidity closure

Any formula containing a large exponent or small residual is release-admissible only if the exponent is selected by an operator support rule and neighbouring alternatives are excluded.

### 02.19.1 Electroweak depth `35`

The electroweak radial depth is

\[
35=|V|+\operatorname{Rank}-1=33+3-1.
\]

Here `|V|=9+11+13=33` is the full addressed carrier, `Rank=3` is the three-sector rank echo, and the common unit section is quotiented once.  The alternatives are excluded as follows:

- `33` omits the rank echo and gives only the addressed support.
- `36=33+3` double-counts the unit section.
- `30=|V|-Rank` is the nullity shell and belongs to weak-unlock/action closure, not radial depth.

Thus `35` is not a free exponent but the unique full-support radial depth after unit quotient.

### 02.19.2 Weak-unlock depth `19` and action section `38`

Let

\[
\gamma={|V|-\operatorname{Rank}\over \operatorname{Rank}}={33-3\over 3}=10.
\]

The primitive one-way terminal unlock removes the halt section:

\[
N_{unlock}=2\gamma-1=19.
\]

The action section is the closed forward/return cycle:

\[
N_{act}=2N_{unlock}=38.
\]

Therefore `38` is not calibrated from electron mass; it is the dimensionless finite action-section coefficient.  The electron mass is used only to express the resulting single section in MeV.

### 02.19.3 Gravity line-depth `99`

The gravity line-depth is the ordered bilinear transport from the observed line sector to the comparison sector:

\[
D_L=V_9V_{11}=9\cdot 11=99.
\]

The alternatives fail by type:

- `9+11` counts disconnected endpoints but not ordered line transport;
- `33` counts the full carrier, not a line-depth map;
- rank/nullity counts internal gauge bookkeeping, not length-depth covariance.

Thus `99` is the unique admissible bidegree for the finite length-depth map in Book 07.

### 02.19.4 Electromagnetic residual exponent

The residual exponent in the electromagnetic normalization is

\[
{5\over 8}+{\delta_0\over384},
\qquad
{5\over8}={|ABCD|+1\over |\Omega_8|},
\qquad
{1\over384}={1\over |\Omega_8|\,|ABCD|\,\dim\mathfrak g_{light}}.
\]

Here `|ABCD|=4`, `|Ω8|=8`, and

\[
\dim\mathfrak g_{light}=\dim SU(3)+\dim SU(2)+\dim U(1)=8+3+1=12.
\]

The correction is therefore tied to the terminal role square, signed lift and light gauge carrier dimension.  No empirical value of `α` is used in selecting the exponent.

### 02.19B Topological stratification of forces (the 0-1-2 skeleton)

The depth/exponent uniqueness above fixes *magnitudes*; it does not yet say *why* there are distinct forces.  The forces are not postulated as separate gauge sectors and they are not unified by enlarging the gauge group.  They are the three homological traces of one feedback operator over the strict skeleton stratification of the rigid carrier `K(9,11,13)` [^b02-43].

**[THE 02.19B] Homological unification 0-1-2 — gravity, EM and QM are the three skeleton traces, not three postulates [^b02-44]. [^b02-42].** Let `R` be the feedback-return operator `F_N` of this book restricted to the carrier `K(9,11,13)`.  The carrier carries exactly three orthogonal homological strata — points, lines, areas — and `R` evaluated on each yields one phenomenological force:

1. **0-skeleton (vertices, `|V|=33`).** `Tr_0(R)` is the global node-closure density.  This is macroscopic gravity `G_N`: a vertex-trace counts only end-point closure, with no transport and no area, so it carries length-depth covariance but no gauge phase — the same length-depth object that supplies `D_L=9·11=99` in §02.19.3 and the Book 07 limit.
2. **1-skeleton (edges, `|E|=359`).** `Tr_1(R)` is the inter-nodal transport capacity.  This is electromagnetism: the edge-trace accumulates one complex phase per edge, and the fine-structure constant is the reciprocal edge count `α^{-1}\propto 359` already forced in §02.13 (`α_{top}^{-1}=359/\varphi^2-\varphi^{-5}`).
3. **2-skeleton (plaquettes/faces).** `Tr_2(R)` is the symplectic area obstruction `[J,Y]`.  This is quantum mechanics: the face-trace is exactly the irresolvable symplectic capacity that sources `\hbar` in [THE 2.9A], `\hbar=c_{symp}([J,Y])`.

Forcing (⊥): suppose two of the three forces were a single continuous hyper-field rather than orthogonal strata.  Then a point-trace, a line-trace and a face-trace would share information across dimensions of the chain complex, i.e. some 0-cell datum would be recoverable from 1-cell or 2-cell data on the rigid carrier.  But the simplicial boundary maps of `K(9,11,13)` are exact (rank 3 / nullity 30 with the standard grading), so points, lines and areas are mutually orthogonal as homology classes; recovering one stratum from another would require an exogenous catalog labelling the coincidence — forbidden by M1.  ⊥.  Hence the three forces are *segregated by the strict orthogonality of points, lines and areas in discrete homology*, not by a choice of gauge group.  The same orthogonality is why §02.19.1–.4 can fix gravity-depth, EM-residual and action-section independently without cross-contamination.

Owner: Book 02.  This theorem ties the magnitude cells of §02.19 to the `[J,Y]` commutator of [THE 2.9A] and the `K(9,11,13)` scene owned by BOOK_01 (see BOOK_01 §01.8, the `ABCD × {±} -> Omega8 -> V9` lift).

### 02.19C Electroweak from quaternions and gravity from Hurwitz archive pressure

§02.19B segregates *which* trace carries *which* force.  This cell forces the *internal gauge structure* of the 1-skeleton/EM sector and the *mechanism* of the 0-skeleton/gravity sector directly from the terminal graph algebra — no Lie group is imported.  This is the M1 failure mode: the Standard-Model electroweak group is forced as the only algebra of finite terminal readouts that survives self-distinguishing without a catalog [^b02-45].

**[THE 02.19C] Algebraic electroweak emergence — `SU(2)×U(1)` is forced from the graph algebra [^b02-46].** The electroweak gauge group is an exact Lie-group isomorphism of two independent terminal operators of the carrier:

- **`Sp(1) ≅ SU(2)` from the imaginary quaternionic terminal readout.**  The terminal readout of the `Q8 ~ Omega8` carrier (Dedekind-1897 minimality, owned by BOOK_01) is quaternionic; the imaginary-quaternion part `\{i,j,k\}` is the non-commutative remainder that survives boundary readout.  The group of unit imaginary quaternions is the symplectic group `Sp(1)`, and `Sp(1)\cong SU(2)` is an exact isomorphism — so the weak isospin sector is the terminal readout itself, not an added field.
- **`U(1)` from complex phase accumulation over the `359` edges.**  Each edge of the 1-skeleton contributes one complex phase increment; the closed accumulation over all `|E|=359` edges is a circle `U(1)`.  This is the same edge phase whose reciprocal count fixes `α^{-1}` in §02.13 and whose trace is `Tr_1(R)=` EM in §02.19B.

Their algebraic tensor product `Sp(1) × U(1)` therefore yields exactly the `SU(2) × U(1)` electroweak structure, with light-gauge dimension `\dim\mathfrak g_{light}=8+3+1` as in §02.19.4 (the `8` of `SU(3)` is the colour sector, not electroweak).

Forcing (⊥): suppose the electroweak group were any group other than `Sp(1)×U(1)`.  By the Hurwitz/Frobenius classification the only normed division algebras are `R,C,H,O` of dimensions `1,2,4,8`; a finite terminal readout that distinguishes itself without an external catalog must be one of these, and the carrier's non-commutative-but-associative readout is exactly `H` (commutative `C` cannot carry isospin non-commutativity, non-associative `O` cannot close a finite readout).  Unit-imaginary-`H` is `Sp(1)`; the residual abelian edge phase is `U(1)`; any third factor would require a stratum beyond the 0/1/2 skeleton of §02.19B and hence an exogenous catalog.  ⊥.  Hence `SU(2)×U(1)` is rigidity-forced, not chosen — this is the algebraic content the depth-`35` and dimension-`8+3+1` facts only summarized.

**Gravity as Hurwitz archive pressure [^b02-47].**  Gravity (the 0-skeleton trace of §02.19B) is *not* a gauge force.  It is the macroscopic consequence of Archive pressure stabilizing the 24-cell Hurwitz boundary lattice: the 24 unit Hurwitz quaternions are the rigid boundary packing, and Archive back-pressure (BOOK_08) forces the closed `24 -> 38` cycle transition.  The endpoint `38` is the same action-section coefficient `N_{act}=2(2\gamma-1)=38` derived in §02.19.2; under the Hurwitz reading it decomposes as `38=24+14`, the 24 Hurwitz-lattice units plus the 14-dimensional automorphism closure that rigidifies them, consistent with the Hurwitz-rigid phase generator `2\pi/\varphi^2` of §02.32.  The two decompositions `2(2\gamma-1)` and `24+14` agree because the action section and the boundary packing close the same forward/return cycle; neither replaces the other, and the electron mass still only sets the MeV scale of the single section.

Owner: Book 02.  Downstream books cite [THE 02.19C] for the algebraic origin of `SU(2)×U(1)` and the Hurwitz-pressure origin of gravity; they may not reintroduce the electroweak group as a free input.
## 02.20 Convex-response coupling theorem

### 02.20.1 Theorem: D0 bridge closure by response coupling

Let `X_N` be a finite D0 internal observable and `Y_N` a finite external projection. A bridge claim is closed only if there exists a kernel `K_N(y|x)` such that:

```math
X_N \preceq_{D0,cx} Y_N,
```

meaning

```math
\mathbb E\,\Phi_N(X_N) \le \mathbb E\,\Phi_N(Y_N)
\quad
\forall\Phi_N\in Test_{D0}(N),
```

and the response vector is preserved or quotiented by a declared loss map:

```math
\mathbb E_{K_N}[\mathcal R_N(Y_N)\mid X_N]
=
\mathcal R_N(X_N)
```

or

```math
\mathbb E_{K_N}[\mathcal R_N(Y_N)\mid X_N]
=
\pi_{loss}\mathcal R_N(X_N).
```

Among all such kernels, D0 selects the entropy extremal representative:

```math
K_N^*=\arg\max H(Y_N|X_N),
```

after quotienting gauge freedom. The bridge is unique only in this quotient. If such a kernel or uniqueness statement is absent, the claim may remain an internal theorem but cannot be promoted to external bridge closure.

### 02.20.2 Proof-cell role

This theorem imports into D0 the finite-support/order/coupling/entropy pattern: reduce to finite stages, preserve a test class, build a coupling, and select the unique gauge-fixed entropy representative. A bridge claim is therefore closed only when it supplies an explicit bridge object, not merely a formula.

Terminology lock: this section uses the words `response tests` and `coupling kernel` literally; bridge closure means an explicit coupling kernel preserving the declared response tests.

## 02.21 Executed finite entropy bridge theorem

A bridge is not closed by a statement of intention.  For finite response grids the bridge must be executed as an entropy-selected kernel.  Let `Y={y_j}` be a finite response grid and let `r` be the retained D0 response.  The admissible bridge kernel is the unique maximizer of

```math
H(q)=-\sum_j q_j\log q_j
```

subject to

```math
q_j\ge 0,\qquad \sum_jq_j=1,\qquad \sum_jq_jy_j=r.
```

For interior `r`, the kernel is forced to be

```math
q_j^*(r)=\frac{\exp(\theta(r)y_j)}{\sum_k\exp(\theta(r)y_k)},
```

where `θ(r)` is uniquely fixed by the mean constraint.  The uniqueness follows because the derivative of the mean map is the variance on the finite grid and is strictly positive for a non-degenerate grid.  Thus the bridge has no free fitting parameter after the response grid and retained response are declared.

This theorem is now the active proof-cell behind the convex-response bridge discipline.  A bridge claim without the executed kernel, KKT check and convex-response check is not promoted beyond bridge-candidate status.

## 02.22 Executed core bridge theorems

### 02.22.1 Theorem: finite positive-frame representation

Let `\mathcal E_N` be the finite effect algebra generated by halted detector projectors. A normalized D0 Born response functional `B_N` on `\mathcal E_N` is admissible iff it is positive, additive on orthogonal joins, and represented by the detector response operator. In finite dimension, positivity and additivity give a unique positive representing matrix `W_N` such that

```math
B_N(E)=\operatorname{Tr}(E W_N).
```

The no-hidden-response rule sets

```math
W_N=R_N/\operatorname{Tr}(R_N),\qquad R_N=D_N^\dagger D_N.
```

Hence the unique normalized finite D0 probability is

```math
P_N(a)=B_N(\Pi_a)=\frac{\operatorname{Tr}(\Pi_a R_N)}{\operatorname{Tr}(R_N)}.
```

The Lean owner separates the finite normalization theorem from the Hilbert-space spelling.  A finite positive response is a finite family `r_i ≥ 0` with positive total response, and a finite Born readout is admissible only when it recovers the raw detector response by

```math
p_i\sum_jr_j=r_i.
```

The theorem

```text
D0.finite_born_readout_unique_on_finite_outcomes
```

proves `p_i=r_i/(Σ_jr_j)` for every finite outcome, and

```text
D0.finite_born_no_alternative_readout
```

proves that an alternative finite probability assignment is impossible under the same detector response.  The finite effect-frame extension lifts this from a raw response list to finite effect frames, coarse-graining, tensor/product response and power-readout no-go.  The proof spine therefore depends neither on a two-channel argument nor on importing the continuum Born rule as an axiom.

### 02.22.2 Theorem: finite entropy/coupling macro bridge source

The external HST macro bridge is admissible only after the D0 side supplies a finite centered subgaussian source. With

```math
\mathsf P_{archive}^{D0}=-\frac{\delta_0^8}{30}\Pi_N,
```

the normalized archive atom is bounded and centered. Therefore its moment-generating function obeys the subgaussian estimate required for convex-response comparison. The continuum Gaussian ensemble is not primitive; it enters only through the external macro bridge after the finite archive source has been closed.

### 02.22.3 Theorem: finite CHSH support

The Pauli-stage CHSH operator has norm `2\sqrt2`; therefore the D0 finite shared-support model reaches the quantum Tsirelson bound without a background signal-speed parameter. Spatial separation belongs to the later geometric quotient.

## 02.23 High-gain hostile uniqueness atlas: proof-spine rule

A high-gain scalar is admissible in the proof spine only when it is locked by a finite operator duty.  The atlas uses the following proof-cell form:

```text
operator lock > exact formulation > no-hidden-anchor proof > negative controls > failure meaning.
```

This rule is applied to `306`, `38`, and `99`.  The point is not that these numbers are arithmetically reproducible; the point is that replacing them by a nearest neighbour changes the finite operator being computed.  The high-gain hostile-uniqueness atlas is normative for any future high-gain row.

## 02.24 Atlas extension: electroweak depth 35

The high-gain atlas is extended by the electroweak-depth uniqueness entry.  The electroweak radial-depth exponent is locked by the finite active scene count plus the rank-corrected witness section:
\[
D_{EW}=|V|+\operatorname{rank}(A)-1=33+3-1=35.
\]
The neighbouring tests have nonzero residuals:
\[
\mathrm{res}(34)=-1,
\qquad
\mathrm{res}(36)=+1.
\]
Thus `34` consumes the witness/basepoint section, while `36` introduces a hidden extra active shell.  This proof-cell is structural; it does not use an electroweak mass as input.

---

## 02.25 High-gain hostile uniqueness atlas completion

The high-gain constants are governed by a single atlas rule: arithmetic reproduction is insufficient. The atlas covers 306, 38, 99, 35, 19, 5/8+δ₀/384, lambda_c/lambda_r, meson transfers and baryon multiplet transfers.

---

## 02.26 External-source proof closure

## 02.27 Finite cochain Ward/anomaly closure

The gauge-matter bridge must be read in the standard language of a finite oriented cochain complex.  For the clique complex of `K(9,11,13)`:

```math
C^0\xleftarrow{\partial_1}C^1\xleftarrow{\partial_2}C^2,
\qquad \partial_1\partial_2=0.
```

The D0 discrete Ward identity is the active-sector consequence of this finite boundary identity.  Anomaly cancellation is not a prose statement: it is the exact vanishing of the finite rational anomaly ledger before QFT/RG dressing.

The required left-handed Weyl sums are:

```math
A_{33Y}=0,
A_{22Y}=0,
A_{YYY}=0,
A_{grav^2Y}=0.
```

The vanishing anomaly ledger is checked by the finite gauge-matter Ward/anomaly certificate.

### Why this closure is FORCED (M1), not posited

The cochain bookkeeping above is the *fact*; the four clauses below are the *why*.  Each is forced by M1 (physics = what survives the requirement to distinguish itself without an external catalog).

**[DEF] Coupling is a measured graph functional, not a free knob [^b02-48].**  The effective charge `g(k)` at refinement level `k` is *not* a constant inserted by hand; it is a function of the statistics of the level-`k` graph `G_k`, fixed by the forgetting projection and only by it:

```math
g(k):=\pi_{k+1\to k}\big(g(k+1)\big)+r_k,
```

where `r_k` is the bounded kappa-residue of the level (the coarse-graining error fixed by the refinement protocol).  No additional free "counter-terms" live in CORE: a counter-term would have to be stored as an exogenous list, i.e. an external catalog, which M1 forbids.  Running couplings are therefore an information-compression artifact of the projection `pi_{k+1->k}`, not transferred-in data — the RG equation is conservation of information under change of scale.

**[DEF] Gauge symmetry = combinatorial indistinguishability of outgoing-edge permutations, not a Lie group glued to a point [^b02-49].**  Local symmetry in D0 is *not* an `SU(N)` attached to a spacetime point.  Let `N` edges leave a node `x`.  Permute them: if the D0 Test verdict `Z` is unchanged, the system carries the local symmetry `S_N` (the symmetric group).  The continuous gauge group is the BRIDGE packaging of this finite permutation indistinguishability; the CORE object is `S_N`.

**[THE] The Ward identity is forced because an anomaly would demand an external catalog [^b02-50].**  Suppose `Z` is invariant under the edge operation `Phi`, so `sum W(gamma) = sum W(Phi gamma)`.  If the associated current were *not* conserved (an "anomaly"), this equality would break.  To restore it under a broken current one must introduce an external compensating counter-term — an External Catalog, forbidden by M1.  Hence symmetry forces the conservation law (Noether/Ward) with no free counter-term; the vanishing anomaly ledger `A_{33Y}=A_{22Y}=A_{YYY}=A_{grav^2Y}=0` is the cochain-level statement of this M1 obstruction, not an independent input.

**[THE] Why `C` and why Born: `|psi|^2` is the CORE invariant `AA^dagger` written in `C`, not an axiom [^b02-51].**  CORE has no primitive `i=sqrt(-1)`; it has the path-`*`-algebra `A = Q(phi)[Q]` of finite formal sums of path/memory classes, with the involution `dagger` given by path reversal,

```math
\Big(\textstyle\sum a_\gamma\,\gamma\Big)^{\dagger}:=\sum a_\gamma^{*}\,\gamma^{-1},
```

`*` being the fixed ABCD auto-involution on `Q(phi)`.  A one-dimensional unitary representation `rho: Q -> U(1)` packages any `A` as `Pi_rho(A)=sum a_gamma rho(gamma) in C`, and this packaging functor preserves sum, product, and `*`: `Pi_rho(A^dagger)=conj(Pi_rho(A))`.  Writing the amplitude `psi(x)=Pi_rho(sum_{gamma:0->x} Hol(gamma))`, linearity of amplitudes is just linearity of `A`, and the probability is the norm `||psi||^2 = psi conj(psi)`, which is exactly the image of the canonical `*`-invariant `N(A):=AA^dagger` in `A`.  Thus

```math
|\psi|^2=\Pi_\rho\big(AA^{\dagger}\big),
```

so Born's rule is *not* an axiom: it is the CORE invariant `AA^dagger` ("there x back") rendered in `C`.  `C` is the unique minimal carrier of (linearity + `*`-conjugation + unitarity) — the `R^2` operator `J` with `J^2=-I` under `(x,y) <-> x+iy` — so `i` is a feature of the BRIDGE language, not a primitive entity of CORE.

### [THE 27.1.1] No blow-up / global regularity [^b02-52]

The same M1 mechanism that kills the gauge anomaly also kills hydrodynamic blow-up, and for the identical reason — a blow-up would be an injected infinite-refinement catalog.

Let the fluid dynamics be an inverse system of finite lattice models (e.g. lattice-Boltzmann type), each cell carrying an information resource bounded by `kappa`, with admissible states passing the physicality criterion M1.  Then the velocity and the finite discrete derivatives are bounded above by a function of `kappa` at every level `k`, and no cascade into "infinitely small scales" is possible; the solution exists globally in time and stays regular in the sense of the coherent projective limit.  (This is a claim about the physically regularized model with a fixed minimal scale, not about a continuum ZFC model of `R^3`.)

**Proof (M1 + forbidden infinite gradient).**
1. At a fixed level `k` the system is finite-dimensional, so the discrete evolution (a composition of finite operators) exists globally: there is no escape to infinity because there are no infinite degrees of freedom.
2. The only way to mimic a blow-up is to demand ever-finer scales within a finite time `u`, i.e. to destroy `kappa`-stability by injecting infinite precision (a refinement catalog).
3. M1/M1+ forbids this: the well-posed setup fixes the admission protocol and a stop-rule, so refinement is not a free handle.
4. Therefore blow-up is impossible in the well-posed D0 setting: the solution is `kappa`-smooth by definition and exists globally. □

The classical PDE formulation on `R^3` is the BRIDGE packaging of this limit; classical existence/smoothness is equivalent to `kappa`-stability of the inverse system of solutions.
## 02.28 Born/EPR assumption split

The finite trace/Born result is not allowed to hide its assumptions.  A proof-cell must state:

```text
finite outcome support;
nonnegative raw detector responses with positive total response;
response-recovery rule `p_i(Σ_jr_j)=r_i`;
trace-state form only when the sector chooses the Hilbert/projector spelling `r_a=Tr(Π_aR)`;
dimension-2 caveat only for projective-only Gleason arguments, not for the finite response-normalization theorem;
Tsirelson/CHSH operator norm if the claim faces EPR/Bell tests.
```

This does not weaken D0.  It prevents a reviewer from claiming that the Born rule was smuggled in through unspoken Hilbert-space assumptions.

**Second channels (external corroboration, cited not re-derived).** The `dimension-2` caveat is exactly where the classical literature supplies independent owners. (i) **Busch** (P. Busch, *Phys. Rev. Lett.* **91**, 120403, 2003) extends Gleason's uniqueness to POVM effects and *removes* the `dim≥3` restriction, so the quadratic Born rule is owned even on the qubit — the regime D0's two-dimensional time layer lives in; for `dim 2` the correct owner is Busch, never the original Gleason. (ii) **Masanes–Müller–Galley** (*Nat. Commun.* **10**, 1361, 2019; Müller–Masanes, *New J. Phys.* **15**, 053040, 2013) derive the Born rule *and* the three-dimensionality of the Bloch ball from operational postulates, giving a second independent route to both `d=3` and quadraticity alongside the Frobenius (`ℍ`) and Gleason/Busch channels. These are external owners of the same facts D0 forces finitely; they corroborate, they do not replace the finite-verification proof.

The same assumption-split discipline is what makes a "cohomology/algebraicity" claim admissible at all, and it forces a sharp result: the no-exogenous-index law M1 turns the algebraicity question into a theorem rather than a conjecture.

[DEF] D0-Hodge-class.  An observable class is a κ-stable rational co-class whose BRIDGE-packing lands in the (p,p)-component of the classical complex spelling — equivalently, self-adjointness/symmetry of the class under the canonical conjugation of the packing.  An algebraic cycle is a κ-stable constructive type (a predicate/code) that at every level k selects a finite rational-coefficient combination of subcomplexes, compatible with the refinement maps π_{k→k-1}.  [^b02-53]

[THE] Algebraicity of κ-stable rational Hodge classes (Hodge in D0-form).  If a D0-Hodge-class [ω] is κ-stable under refinement of the inverse system and rational, then [ω] is realized by a rational linear combination of algebraic cycles.

Forcing (M1 forbids a "non-algebraic index"):

1. [ω] is an *observable* class, so it must carry a finite numerical distinguishability-verification packet at each level k — otherwise it is a metaphysical entity with no test, which the finite-verification frame disallows.
2. Suppose [ω] were *not* algebraically realized.  Then the distinguishability of "why it exists" cannot be reduced to a finite constructive predicate-type; to retain it as a separate object one needs an external index — a "non-algebraicity label" — that is *not* derivable from the level-k tests.
3. Such an index is an exogenous parameter ⇒ forbidden by M1 (physics = what survives the requirement to distinguish itself without an external catalog).
4. Hence every κ-stable rational Hodge class must admit an algebraic realization. □

[^b02-54]  The classical statement uses infinite-dimensional spaces of forms and limit arguments; D0 replaces these with κ-stable constructive types and distinguishability tests, so the result lives entirely inside the finite-verification frame — the same frame that the Born/EPR split above keeps honest.
## 02.29 Phase-unfolding and residue-branch theorem

Let `T:n↦n+1` be the finite registration tick and let phase be read modulo a circumference `τ`. If `q≈mτ`, then each residue class `a mod q` defines a branch `a+tq` with phase drift `t(q-mτ)`. Therefore visible arms/rays are residue classes of a finite return modulus.

The admissible branch filter is part of the response structure. In the arithmetic model it is `gcd(a,q)=1`, so the visible branch count is `φ_Euler(q)`. D0 uses the same grammar with a finite detector admissibility filter.

Consequences:

```math
d_{13}=φ_{Euler}(44)=20,
```

and, for the classical large-scale return `710≈113·2π`,

```math
φ_{Euler}(710)=280=|Ω_8|\cdot35.
```

Thus the electroweak depth `35` has a phase-unfolding interpretation as the per-sign branch count after the terminal `Ω_8` quotient.

### Forced symmetry axis of the spectral packing

The phase modulus `τ` and its residue branches fix *where* arms appear; the next question is whether the symmetry that pairs zeros across the packing carries any free dimensionless choice. It does not.

Work with the canonical D0 spectral packing `ζ_D(s)=Tr(|D|^{-s})=Σ_n λ_n^{-s/2}`, built from the self-adjoint spectrum of a finite operator (cite BOOK_01 for the heat-trace/spectral-zeta packing of a finite self-adjoint `D`; the `s`-record is a BRIDGE re-encoding, not a CORE object). In D0, "RH" is not an independent hypothesis but the statement that this packing has a *canonical* functional symmetry under an admissible protocol — no external parameter (axis shift, arbitrary normalization) is permitted.

[THE] [^b02-55]
For the canonical D0 packing `ζ_D(s)` of a finite self-adjoint spectrum `{λ_n}`, consistent with the canonical conjugation of the packing, the only admissible axis of symmetry of the zeros in the BRIDGE record is `Re(s)=1/2`.

Proof (M1: the axis cannot be a knob).
1. In CORE the spectrum `{λ_n}` of the finite self-adjoint operator is a family of invariants independent of any choice of coordinates/basis.
2. The BRIDGE parameter `s` is packing only — a way to write the spectral sums/transforms in familiar form. It adds no CORE content.
3. After the Can/ε²-protocol the functional symmetry of the zeros is fixed in exactly one way. To *shift* the axis `Re(s)=1/2 → 1/2+δ` one must supply a new dimensionless parameter `δ` — i.e. an external catalog entry selecting the axis.
4. Such a `δ` is not derivable from the spectrum `{λ_n}`; it is an exogenous knob ⇒ forbidden by M1 (physics = what survives distinguishing itself without an external catalog).
5. Hence the only admissible axis is the canonical `Re(s)=1/2`. □

The classical Riemann RH is recovered as the special case where the packing is `ζ` of the integers: the "critical line" is a *consequence* of the canonical packing symmetry, not an independent conjecture with tunable knobs. This is the same forcing pattern that selects the phase modulus above — the residue branches and the symmetry axis are both catalog-free outputs of M1, not free parameters laid over the spectrum.
## 02.30 Phase-unfolding master chain

D0 does not treat spatial branching as a primitive geometric background.  An ordered finite registration generates visible geometry through a phase quotient.  For a phase circumference \(\tau\), the map

\[
U_\tau(n)=(n,n\bmod \tau)
\]

turns the one-dimensional tick sequence into a branch foliation whenever an integer pair \((q,m)\) satisfies \(|q-m\tau|\ll 1\).  The residue classes modulo \(q\) are the coherent branches.  An admissibility filter selects the branches visible to the detector.

The D0 structural return

\[
q_T=|ABCD|\,|V_{11}|=4\cdot11=44,
\qquad
m_T=|ABCD|+\operatorname{rank}(A_K)=4+3=7
\]

is the first terminal phase-return window.  Its admissible coprime branch count is

\[
\varphi_E(44)=20=d_{13}.
\]

Thus the terminal shell degree is the branch count of the first stable phase unfolding.

The second return is

\[
q_{EW}=2(|ABCD|+1)(2|V|+|ABCD|+1)=710,
\qquad
m_{EW}=(|ABCD|+1)d_{13}+|V_{13}|=113.
\]

Since \(710/113\) is a near-return for the Euclidean phase circumference, and

\[
\varphi_E(710)=280=|\Omega_8|\cdot 35,
\]

the electroweak radial depth is the per-\(\Omega_8\)-sector branch depth:

\[
D_{EW}=35.
\]

Phase unfolding is a structural theorem, not an illustration: later scale depths are repeated applications of the same finite tick \(\to\) phase quotient \(\to\) return modulus \(\to\) residue branch \(\to\) quotient mechanism.

### Master-chain anchor: one \(\kappa\)-invariant, two passports

The phase-unfolding chain above is one face of a more general D0 phenomenon: a single \(\kappa\)-stable invariant can be read off through two distinct constructive "passports," and M1 forces the two readings to agree.  The sharpest instance is the BSD identity in D0 form, which anchors the entire master chain.

[DEF] In D0 an elliptic curve \(E\) is a finite constructive type of coefficient rules together with an inverse system of refinements of computable invariants; any "infinite sum" is admitted only as a \(\kappa\)-stable limit packing.  Its rank \(\operatorname{rank}_{D0}(E)\) is the \(\kappa\)-stable nullity of the canonical distinguishability/conjugate-Laplacian operator on that type — the same rank/nullity principle as the K(9,11,13) scene (observed nullity = memory), and it must be testable and \(\kappa\)-stable, else it would require an external refinement catalog.  The L-function \(L(E,s)\) is not an object of actual infinite analysis but a BRIDGE packing of finite spectral data (heat-trace / zeta-trace) of the operator attached to \(E\) [^b02-56].

[THE] (BSD in D0 form: analytic = topological as one \(\kappa\)-invariant.)  The order of zero of the spectral packing \(L(E,s)\) at the canonical BRIDGE point equals the \(\kappa\)-stable nullity (rank) of the constructive type:

\[
\operatorname{ord} L(E,s) = \operatorname{rank}_{D0}(E).
\]

*Forcing — the "one invariant \(\to\) two passports" principle [^b02-57].*

1. In D0 the only admissible "analytic" objects are packings of finite spectral data; the order of zero is therefore a readout of the same finite spectrum, not of an external analytic continuation.
2. The rank in CORE is the observed nullity of the operator; it is computable and \(\kappa\)-stable, otherwise it would be untestable metaphysics.
3. Suppose the order of zero of the packing and the rank diverged.  A divergence is, by definition, information present in one passport and absent from the other — i.e. data not contained in the CORE spectrum.  To pin that data down one would have to declare exogenous parameters fixing which "hidden" contribution the analytic side counts.  Exogenous catalog data of exactly this kind is forbidden by M1 (DEF-0.2.2: physics is what survives the demand to distinguish itself without an external catalog).
4. Hence no such divergence can be registered: both passports describe one and the same \(\kappa\)-invariant and must coincide. \(\square\)

[BRIDGE 30.B] Classical BSD carries a Tamagawa/Ш multiplier and similar factors.  In D0 these are a BRIDGE-decomposition of the single \(\kappa\)-invariant into "tabular factors"; they cannot be independent handles, since independent handles would reintroduce exactly the exogenous degrees of freedom M1 rejects [^b02-58].

This anchor is why the master chain closes: each scale depth in the phase-unfolding cascade (terminal shell \(d_{13}=20\), electroweak depth \(D_{EW}=35\)) is a topological branch count read through the return modulus, while the corresponding analytic readout — the order of the matching spectral packing — is forced equal to it by the same two-passports argument.  Phase unfolding and spectral order are not two mechanisms but two passports of one finite \(\kappa\)-invariant.
## 02.31 Φ as primitive positive-response capacity

The number `φ` is not a primitive axiom. The primitive object is the normalized finite positive-response detector skeleton. It has one direct branch of weight `p` and one first self-return branch. Since the first positive response is quadratic, the return branch has weight `p²`. The unit terminal closure is therefore

\[
p+p^2=1.
\]

The polynomial `p²+p−1` is strictly increasing on `(0,1)`, so the positive branch is unique:

\[
p=\varphi^{-1},
\qquad
p^2=\varphi^{-2}.
\]

The distinguishability half-gap is

\[
\delta_0=\frac{p-p^2}{2}=\frac{1}{2\varphi^3}.
\]

The alternatives are excluded by the operator obligations. The equation `p+p=1` is only a linear naming split and has no positive self-return. The equation `p+p^k=1` for `k>2` contains hidden intermediate memory before the first halt and is therefore not primitive. A non-integer exponent is not finite constructive channel composition on profinite stages. A free equation `p+q=1` introduces a second independent scale and violates single-section closure.

## 02.32 Hurwitz-rigid phase generator and non-resonant spatial unfolding

**Canonical derivation: §01.21** (Hurwitz-rigid phase generator — `α_D0 = p² = φ⁻²` is the maximally non-resonant rotation, with the φ/M1 duality lemma). It is owned there and not re-derived here. For the proof spine the operative content is the two-layer chain — `φ⁻²` irrational rotation ⇒ non-resonant archive smoothing; finite return modulus `q` ⇒ residue branch geometry — which reconciles macroscopic smoothness with finite branch unfolding.

## 02.33 Forced return windows and non-post-hoc phase unfolding

**Canonical derivation: §01.22** (forced return windows). The full capacity-derivation is owned there and is not repeated here. For the proof spine the operative result is: the windows are *forced by terminal capacity*, not chosen as rational approximants — `q_T = lcm(|ABCD|, V₁₁) = 4·11 = 44`, `m_T = |ABCD| + rank(A_K) = 7`, branch count `φ_Euler(44) = 20 = d₁₃`; `q_EW = 2·B·L = 2·5·71 = 710`, `m_EW = B·d₁₃ + V₁₃ = 113`, `φ_Euler(710) = 280 = |Ω₈|·35 ⇒ D_EW = 35`. The ratios `44/7` and `710/113` are *checked* as near-returns only after the integers are capacity-derived. §01.22 additionally forces the `+2` address step and the `ν* = 1/9` (`40°`) cycle quantization that make the near-returns well-posed; the gravity-sector M1-forcing of the same windows is at §07.23.


## 02.34 Master Evolution and φ-quasicrystal proof spine

D0-MASTER-EVOLUTION-001
Owners:
  T_squared_plus_T_minus_identity_eq_zero
  trace_T_pow_eq_signed_lucas
  lefschetz_spectrum_unfolds_scene
  det_T_pow_square_eq_one
  lucas_heat_moment_bridge

D0-QUASI-001
Owners:
  d0_vacuum_is_condensed_phi_quasicrystal_support
  visible_geometry_is_cut_project_shadow
  phi_phase_has_hurwitz_anti_resonance

D0-HULL-001
Owners:
  d0_hull_has_finite_local_complexity
  d0_hull_has_phi_cut_project_origin
  d0_hull_is_nonperiodic
  d0_hull_supports_gap_labeling

D0-KTHEORY-001
Owners:
  gap_label_is_topological_not_fitted
  d0_gap_labels_are_countable
  gap_labeling_requires_frozen_operator

D0-SOLENOID-001
Owners:
  d0_hull_admits_noncommutative_solenoid_model

D0-SOLENOID-GRAVITY-001
Owners:
  finite_spin2_operator_is_tt_sector_of_solenoid_spectral_geometry

### The one-ℤ₂ concentrator: seven incarnations of a single orientation bit

The owner blocks above each touch a separate ℤ₂ — `trace_T_pow_eq_signed_lucas`
carries a Lucas sign, `det_T_pow_square_eq_one` carries `det T = −1`, the heat-moment
bridge carries a parity, and the quasicrystal/hull spine inherits the Galois pair
φ↔ψ of ℚ(√5). These are **not** independent two-element groups that happen to coincide
numerically. They are seven faces of the *same* ℤ₂. This synthesis is the load-bearing
join of the whole spine; it is stated here as the concentrator node, with each face
cited back to its owner rather than re-derived.

**[THE] One ℤ₂, seven incarnations [^b02-59].**
One and the same order-two group surfaces as:

1. The Galois conjugation `Gal(ℚ(√5)/ℚ)`: the swap φ↔ψ (owned by BOOK_01 §01.20;
   ABCD = the Galois data — A,B are the conjugation-invariant elementary symmetric
   functions, C,D the conjugate pair).
2. Lucas parity / orientation class of the leaf: the address defect
   `ε_n = φⁿ − L_n = −ψⁿ` (sign `(−1)^{n+1}`) [^b02-60], owned here as
   `trace_T_pow_eq_signed_lucas`.
3. The center = commutator = Frattini subgroup of Q₈, all equal to `{±1}`
   (Q₈≅Ω₈ minimality owned by BOOK_01).
4. The leaf of the spinor double cover — the 4π-periodicity sheet.
5. The ± orientation sign read off Ω₈ (sign-bit owned by BOOK_01).
6. `det T = −1`, the Viète invariant B of `T = [[0,1],[1,−1]]`, owned here as
   `det_T_pow_square_eq_one`.
7. The rank-doubling 4→8 of the icosian construction = the pair of Galois embeddings.

**Concentrator identity (the *why*).** The seven are forced to be one group, not seven,
by the selector arithmetic. The Lucas approximation error is *literally* the Galois
conjugate (from the closed form `L_n = φⁿ + ψⁿ`):

  ε_n = φⁿ − L_n = −ψⁿ,

so its sign is exactly the orientation class of the leaf. Stepping by +2 (even powers)
fixes the sign of the conjugate, i.e. selects one Galois sector; the Lucas selector of
the trace identity `trace_T_pow_eq_signed_lucas` *is* the Galois trace. Hence:

  **orientation bit of the universe = Gal(ℚ(√5)/ℚ) = the Galois group of the
  minimal quadratic field.**

No catalog choice enters: the bit is not posted by hand, it is the unique nontrivial
automorphism of the smallest field in which φ lives. This closes the master-evolution
spine to the quasicrystal/hull spine — the time automorphism T, the signed-Lucas heat
moments, and the φ cut-and-project support are governed by *one* ℤ₂, so the
"asymmetric symmetry" of the vacuum (it is not the fair-coin ½ symmetry, but it is exactly
symmetric under φ↔ψ) gets a strict name: `Gal(ℚ(√5)/ℚ) ≅ ℤ₂`. Spontaneous breaking is
re-read accordingly — nothing breaks; the canonical cut was never the half-cut, and the
δ₀ offset is forced, not tuned by a potential. [Status: SYNTHESIS — each face is owned
and proved by the cited owner; the identification is machine-checked. A finite
certificate and a synthesis module prove four of the seven faces (Galois conjugation,
the Q₈ center, the Lucas parity, and the toral determinant) are the *same* order-two
element, together with the two joints: the Lucas-trace sign equals the orientation
determinant, which equals the Galois norm `φ·ψ = −1`; and the address step `+2` is the
identity of the cover (it stays on one sheet), while `+1` flips the sheet and is therefore
banned. [^b02-59]]
## 02.35 Theorem-spine owners: Born 2.0, Torus-Core13, and Galois balance

The active proof spine is:
Master Evolution > QUASI > HULL/KTHEORY/SOLENOID.

The proof owners for the following components are:

- **Born 2.0 / 2.0 Uniqueness**:
  - `Finite Born 2.0 uniqueness`
  - `D0.finite_effect_born_readout_unique`
  - `D0.finite_effect_born_no_hidden_response`
  - `D0.finite_tensor_born_readout_unique`
  - `D0.finite_power_readout_no_alternative`

- **Torus-Core13 Geometry**:
  - `Torus-Core13 Geometry Origin`
  - `D0.Geometry.TorusCore13GeometryOrigin`
  - `torus_geometry_forces_generation_selector_noncommute`
  - `D0.Matter.CKMNontrivialFlavourAlgebra`
  - `D0.Matter.MesonDefectTransferOrigin`
  - `D0.Core.BornQuadraticOrigin`

- **Toral Automorphism / Galois balance**:
  - `Toral automorphism / Galois balance`
  - `trace_evolution_unfolds_d0_geometry`
  - `toral_volume_conservation_square`
  - `dark_sector_even_window_readout_zero`

## 02.36 Theorem spine for the matter, gauge, gravity and cosmology sectors

Selector uniqueness and concrete Book 04 instances: `chargedLeptonElectronTerminalClaim`,
`electroweakDepth35Claim`, `protonReadout306Claim`,
`neutronArchiveSiblingClaim`, `betaUnlockDepth19Claim`.

The active proof spine maps directly onto the proof owners below.

- **CKM Finite Basis / Selector**:
  - `CKM finite basis origin`
  - `D0.Matter.CKMBasisOrigin`
  - `ckm_origin_candidate_matrix_unique`
  - `ckm_no_free_matrix_at_fixed_basis_origin`
  - `ckm_no_free_matrix_at_fixed_bases`
  - `D0.Matter.StrictSelectorCertificate`
  - `D0.Matter.book04_selector_claim_no_free_alternative`

- **Charged-lepton Coefficient-origin**:
  - `02.36.3a Charged-lepton coefficient-origin closure`
  - `D0.Matter.ChargedLeptonCoefficientOrigin`
  - `charged_lepton_coefficient_table_forced`
  - `changed ratio row, exponent row or bridge-factor row is impossible`

- **Book 04 Operator-boundary**:
  - `02.36.3b Book 04 operator-boundary closure`
  - `D0.Matter.book04_operator_boundaries_closed`
  - `nucleon_line_cannot_promote_full_baryon_multiplet`
  - `lower_hodge_400_cannot_promote_meson_masses`
  - `missing_scalar_projector_cannot_promote_higgs_yukawa_core`

- **SM-facing Gauge Decomposition**:
  - `02.36.6 SM-facing gauge decomposition`
  - `D0.Gauge.SMGaugeDecomposition`
  - `no alternate factor/representation ledger`

- **Spin-2 Derivation / Carrier**:
  - `Spin-2 derivation and internal cone speed`
  - `D0.Geometry.FiniteWeakFieldQuotient`
  - `finite_weak_field_quotient_yields_tt_representative`
  - `finite_conserved_stress_spin2_coupling_closed`
  - `Poisson response plus a named TT mode is not enough`
  - `D0.Geometry.FiniteSpin2WaveOperator`
  - `PiTT4_idempotent`
  - `WTT4_preserves_tt`
  - `finite_spin2_tt_carrier_closed`
  - `D0.Geometry.finite_spin2_tt_carrier_closed`

- **Cosmology**:
  - `02.37 Cosmology reproducibility split`
  - `InternalArchiveCosmologyObject`
  - `SurveyLikelihoodPassport`
  - `survey likelihood cannot promote to core cosmology closure`

- **Tick-gauge / Lorentz**:
  - `02.38 Tick-gauge and Lorentz-compatible cone invariant`
  - `finite_causal_tick_section_cone_speed_eq_one`
  - `finite_lorentz_tick_gauge_no_euclidean_export`
  - `finite_lorentz_tick_rescaling_preserves_closure`

- **Full Support Selectors**:
  - `02.39 Book 04 full-support selector closure`
  - `D0.Matter.Book04FullSupportSelectors`

- **Higgs Projector / SMScalar**:
  - `commutes_XZ_forces_scalar_matrix`
  - `nonzero_gauge_idempotent_eq_identity`
  - `rank1_scalar_projector_breaks_su2_gauge_compatibility`
  - `rank2_scalar_projector_exists`
  - `minimal_positive_scalar_projector_rank_two`
  - `minimal_positive_scalar_projector_unique`
  - `higgs_yukawa_core_promotion_valid`

- **Baryon S3 / Decuplet**:
  - `D0-QUASI-002A`
  - `Phason Strain Generations / Baryon S3`
  - `phason_strain_generations_baryon_closure`

- **Quasicrystal Operator Origin**:
  - `D0-QUASI-002`
  - `quasi_generation_inflation_orbit`
  - `archive_phason_strain_em_dark_metric_visible`
  - `fractional_charge_window_weights`

- **Gravity / Einstein Interface**:
  - `Entropic archive gravity interface`
  - `Finite spin-2 wave operator`
  - `Higher-curvature finite cut`
  - `Spectral A2 / EH bridge`
  - `Macro Einstein interface`


## 02.40 Master bootstrap and discrete volume derivative

Definition. The finite active volume is the trace-rank of the retained projector:
\[
V_N := \operatorname{rank}(P_N)=\operatorname{Tr}(P_N).
\]
For an admissible one-channel extension of the retained sector, the discrete volume derivative is the forward finite difference
\[
\partial_V A_N := A_{N+1}-A_N.
\]
This is the finite differential structure used by CVFT before any continuum interpolation.

The master bootstrap functional is
\[
\delta\left[
\beta^{-1}\log\operatorname{Tr}(e^{-\beta\Delta_N(V)})
-
\log\det(I-zP_NU_N^\dagger Q_NU_NP_N)
\right]=0.
\]
The heat-trace term supplies the finite spectral geometry. The feedback determinant supplies return-cycle thermodynamics, pole stabilization, pressure, and leakage.

## 02.41 Self-substrate trace identity and fractal tick

For \(\psi\in P_N\mathcal H_N\), unitarity and orthogonality give

\[
\|\psi\|^2=\|P_NU_NP_N\psi\|^2+\|Q_NU_NP_N\psi\|^2.
\]

The feedback-return operator satisfies

\[
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N),
\qquad
\langle\psi,F_N\psi\rangle=\|Q_NU_NP_N\psi\|^2.
\]

### Fractal Tick Fixed Point

Let \(p=\varphi^{-1}\). On a declared detector-clock subspace \(\Pi_\tau\),

\[
\Pi_\tau F_N\Pi_\tau=p^2\Pi_\tau,
\qquad
\Pi_\tau U_{\rm eff}^\dagger U_{\rm eff}\Pi_\tau=p\Pi_\tau.
\]

This is a fixed-point sector law, not a global identity for arbitrary \(U_N\).

### Continuum from Fractal Tick

The constant logarithmic gradient

\[
\Delta\log A=-\log\varphi
\]

generates the continuous envelope

\[
\frac{dA}{ds}=-(\log\varphi)A,
\qquad
\frac{dB}{ds}=(\log\varphi)A.
\]

Thus continuum time is the semigroup envelope of infinite self-similar trace production.

**Semigroup Uniqueness Theorem.**
The functional equation for the envelope satisfies the multiplicative form

\[
A(s+t) = \frac{A(s) A(t)}{A_0},
\]

for uniqueness under the retained-archive split. The division by \(A_0\) normalizes the initial substrate so that the exponential solution is the unique continuous semigroup compatible with the fractal ratio \(q = \varphi^{-1}\); the additive form does not give uniqueness.

### Quadratic Peel Theorem

Phase-blind finite readout is quadratic because archive trace is a norm-square boundary peel, not a linear amplitude cut:

\[
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N).
\]


## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b02-1]: forcing: GOLDEN DEF 15.1.1 / REM 15.1.2, BOOK-II-MECHANISM
[^b02-2]: forcing: GOLDEN THE 20.1.1, BOOK-V-MATHEMATICS; ⊥-proof
[^b02-3]: forcing: GOLDEN COR 20.1.2, BOOK-V-MATHEMATICS
[^b02-4]: forcing: GOLDEN DEF 2.1, Finite Holographic Self-Reading Principle
[^b02-5]: forcing: GOLDEN DEF 2.1
[^b02-6]: self-similarity of refinement; forcing: GOLDEN LEM 2.3.2.S1
[^b02-7]: algebraic closure of S1; forcing: GOLDEN §2.3.2
[^b02-8]: φ from additivity + homogeneity; forcing: GOLDEN THE 2.3.3
[^b02-9]: Q8 hamiltonian minimality; forcing: D0-Q8-DEDEKIND-MINIMALITY-001, Dedekind 1897
[^b02-10]: canonical unit split; forcing: GOLDEN THE 3.3.A
[^b02-11]: necessity of the factor 2; forcing: GOLDEN THE 80.1
[^b02-12]: forcing: D0-DIM-LADDER-COMPACT-001
[^b02-13]: forcing: GOLDEN §02.7A, "Holographic Self-Reading Principle"
[^b02-14]: forcing: GOLDEN §02.7A, item 1
[^b02-15]: forcing: GOLDEN §02.7A, item 2
[^b02-16]: forcing: GOLDEN §02.7A, item 3
[^b02-17]: forcing: GOLDEN §02.7A, item 4
[^b02-18]: open obligation — cert obligation open
[^b02-19]: forcing: GOLDEN THE 2.9A, BOOK-02-MATHEMATICAL-PROOF-SPINE-AND-INVARIANT-CALCULUS; ⊥-proof
[^b02-20]: forcing: GOLDEN THE 10.1.8 / BOOK-IV; GOLDEN LEM 21.1.2 / BOOK-V
[^b02-21]: forcing: GOLDEN REM 21.3.3.Baire / BOOK-V; uniqueness theorem GOLDEN THE 21.3.4
[^b02-22]: forcing: GOLDEN THE 22.2.1 / BOOK-V
[^b02-23]: forcing: GOLDEN DEF 24.1.1 / BOOK-V
[^b02-24]: forcing: GOLDEN LEM 24.1.2 / BOOK-V
[^b02-25]: forcing: GOLDEN LEM 24.1.3 / BOOK-V
[^b02-26]: forcing: GOLDEN THE 24.2.1 / BOOK-V
[^b02-27]: forcing: GOLDEN THE 24.2.2 / BOOK-V
[^b02-28]: forcing: GOLDEN THE 24.3.1 / BOOK-V
[^b02-29]: forcing: GOLDEN COR 24.3.2 / BOOK-V
[^b02-30]: forcing: GOLDEN LEM 24.3.2 / BOOK-V
[^b02-31]: forcing: GOLDEN §16.3, COR 16.3.5
[^b02-32]: forcing: GOLDEN COR 16.3.5.
[^b02-33]: forcing: GOLDEN LEM 21.4.2, THE 21.4.5
[^b02-34]: forcing: GOLDEN LEM 21.4.2
[^b02-35]: forcing: GOLDEN THE 21.4.5
[^b02-36]: forcing: GOLDEN THE 21.3.4
[^b02-37]: forcing: GOLDEN THE 21.4.3
[^b02-38]: forcing: BOOK_02 §02.13
[^b02-39]: claim_id: `D0-Q8-DEDEKIND-MINIMALITY-001`; forcing: GOLDEN THE I.3 / D0-THEORY-DOSSIER §I.3
[^b02-40]: claim_id: `D0-ICOSIAN-E8-CARRIER-001`; forcing: GOLDEN THE II.1 / D0-THEORY-DOSSIER §II.1, cross-checked D0-CKM-INTERFACE-ITERATION-REPORT §28
[^b02-41]: claim_id: `D0-ICOSIAN-LEECH-BRIDGE-001`; forcing: GOLDEN II.2
[^b02-42]: open obligation — cert obligation open
[^b02-43]: forcing: GOLDEN THE 02.19B, `D0-CORE-HOMOLOGICAL-FORCES-001`
[^b02-44]: forcing: GOLDEN THE 02.19B, D0.Core; ⊥-proof
[^b02-45]: forcing: GOLDEN THE 02.19C, `D0-CORE-ELECTROWEAK-QUATERNION-001`
[^b02-46]: forcing: GOLDEN THE 02.19C, D0.Core; ⊥-proof
[^b02-47]: forcing: GOLDEN THE 02.19C, gravity branch
[^b02-48]: forcing: GOLDEN CHK II.3.APPX8.5.2A
[^b02-49]: forcing: GOLDEN DEF II.3.APPX8.6.A
[^b02-50]: forcing: GOLDEN THE II.3.APPX8.7.2
[^b02-51]: forcing: GOLDEN THE II.3.APPX8.C3 + CHK II.CPLX
[^b02-52]: forcing: GOLDEN THE 27.1.1
[^b02-53]: forcing: GOLDEN THE 28.1.1, DEF 28.0.1–28.0.3, BOOK V Mathematics.
[^b02-54]: forcing: GOLDEN THE 28.1.1, BOOK V Mathematics.
[^b02-55]: unique admissible symmetry axis — D0 critical line; forcing: GOLDEN THE 29.1.1
[^b02-56]: forcing: GOLDEN DEF 30.0.2, DEF 30.0.3
[^b02-57]: forcing: GOLDEN THE 30.1.1
[^b02-58]: forcing: GOLDEN BRIDGE 30.B
[^b02-59]: forcing: GOLDEN `D0-ZETA8-REGISTRY-001`,
concentrator node with edges `same_Z2_incarnation`; Lucas face = GOLDEN THE 3.11.B — closed: certificate vp_z2_spinor_cover.py and Lean D0.Synthesis.Z2SpinorCover (z2_spinor_cover) prove four of the seven incarnations are one Z2, with the +2 joint (det(T^{n+2})=det(T^n)) and the +1 control; claim D0-Z2-SPINOR-COVER-001.
[^b02-60]: forcing: GOLDEN THE 3.11.B
