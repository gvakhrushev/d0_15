<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 06 — Evolution, Forgetting, and Time

> **[Standard Physics Isomorphism].** D0's coined terms in this book read, in mainstream physics, as:
>
> - archive → integrated-out environment / environment bath (open-system trace-out)
> - forgetting map / coarse-graining → Wilsonian coarse-graining / CPTP decoherence channel
> - archive pressure → trace anomaly / entropic backreaction
> - phason → Goldstone mode of broken translation symmetry
> - carrier → representation (state) space
> - readout → measurement outcome (POVM effect)
>
> Genuinely-D0 (kept, defined in-text against the standard notion): the scene `K(9,11,13)`, the M1 admissibility axiom (no obligatory external catalogue), `δ₀`, `φ`, and *forcing* (= reductio ad absurdum against M1). Full crosswalk: the language-normalization Rosetta (`00_LANGUAGE_NORMALIZATION/D0_STANDARD_LANGUAGE_ROSETTA.md`).


> Scope: Time as ordered finite registration, forgetting/coarse-graining, RG transfer, and active-medium bridge discipline.
> Claim discipline: Evolution claims require normalized channels or explicit bridge status.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 06.0 Active time/evolution sector law

Definition. The time arrow in D0 is the ordering induced by normalized coarse-grained feedback channels.

```text
hat Phi_N(rho) = Phi_N(rho) / Tr Phi_N(rho)
```

Entropy monotonicity is a theorem only when the channel is normalized, coarse-grained and entropy-monotone.

```text
c_D0 = 1 tick gauge
```

This is a dimensionless tick gauge, not an SI prediction. Formal owner:

```text
D0.Bridge.finite_causal_tick_section_cone_speed_eq_one
```

Gravity runtime boundary tokens: eta4 terminal signature, δ₀ finite readout cut, heat trace scale is internal, not SI time.

## 06.1 Standard reading of evolution and forgetting

Definition. D0 forgetting is one of the following standard operations, depending on context: conditional expectation onto a retained algebra, partial trace over an environment, Wilsonian coarse-graining, or entropy-selected coupling. The D0 archive is the traced-out complement produced by that operation.

The "standard reading" above is the downstream FACT. The *why* is this: time, the arrow, and the seam that drives forgetting are not external inputs — they are forced by the heat-trace of the scene Laplacian. This section sets out that forcing spine.

### 06.1.1 Heat-trace operator and the forced u↔t bridge

Status: CORE-FORCING [^b06-3].

Phase time on the scene is the dimensionless heat-trace parameter `u`, not a clock. The default operator throughout this sector is

```text
H(u) := Tr e^{-uL},   {lambda_i} = spec(L),
```

with `L` the normalized scene Laplacian (or the full system when stated). Time in D0 is not posited; it is read off the diffusion ∂_u p = -L p — how fast the system loses local information under refinement.

Forcing of the bridge. The exponents `e^{-u lambda}` are only well-typed if `u·lambda` is dimensionless. Since `lambda` carries the spectral dimension of `L`, ANY phenomenological calibration `t ↦ u` is forced to the affine form

```text
u = tau0 · t,
```

with `tau0` the *unique* admissible internal scale — no second dimensionless constant is permitted by dimensional consistency alone. The BRIDGE calibration then fixes `tau0` to the distinguishability tolerance already in the corpus:

```text
tau0 = epsilon^2 = phi^-16,    epsilon = phi^-8,
so   u = epsilon^2 t = phi^-16 t.
```

This introduces NO new constant: it fixes the unit of time through the single internal precision scale `epsilon`. (Note: this `tau0 = phi^-16` is the *internal* heat-trace bridge and is a distinct object from the SI bridge `tau0 = h/(38 m_e c^2)` owned by BOOK_03/BOOK_07 — they must not be conflated.)

Cert status: the four-dimensional periodic archive Laplacian and its factorizing heat trace `Theta_L(u) = (sum_k e^{-u lambda_1d(k)})^4` are checked as a finite object by the heat-trace certificate; the affine-uniqueness of `u = tau0·t` from dimensional typing is [^b06-1].

### 06.1.2 Information time and the arrow as heat-trace monotonicity

Status: CORE-FORCING [^b06-4].

Information time is the return-probability deficit of the diffusion:

```text
P_return(u) := H(u) / |V|,
I(u)        := -ln P_return(u).
```

`I(u)` measures the loss of local information accumulated by phase time `u`. This is the heat-trace channel for the arrow — complementary to, and not replaced by, the normalized-feedback / T-ladder entropy channel of §06.0.

Arrow theorem. Because `L ⪰ 0`, every eigenvalue `lambda_i ≥ 0`, so

```text
H'(u) = -sum_i lambda_i e^{-u lambda_i} ≤ 0.
```

Hence `H(u)` and `P_return(u)` are non-increasing and `I(u) = -ln P_return(u)` is non-decreasing. The arrow of time costs NO separate axiom (COR II.1.4.A): `I(u)` is computable from the finite spectrum `{lambda_i}` of `L`. Time has no independent law — it is a corollary of the scene operator.

Spectral-dimension / RG link. Where the heat-kernel asymptotic applies,

```text
P_return(u) ≍ u^{-d_s/2},   so   I(u) ~ (d_s/2) ln(1/u),
```

with `d_s` the spectral dimension; this is exactly the natural RG-coarsening parameter, tying the forgetting flow of this book to Wilsonian coarse-graining named in the Definition above.

Cert status: heat-trace ↔ spectral (Weyl) dimension on the archive Laplacian, the RG/coarse-graining renormalization under phase projection π (`c_n = 1`, `R_n = 0`), and forced return-window capacity are each discharged by their finite certificates. The monotonicity inequality `H'(u) ≤ 0` itself is elementary from `lambda_i ≥ 0` and needs no separate cert.

### 06.1.3 Spectral asymmetry of gluing — the closure defect that drives forgetting

Status: CORE-FORCING [^b06-5].

The corpus carries an irreducible gluing anomaly `Delta_alpha`: the mismatch between the topological and algebraic expressions for `alpha^-1` (numbers owned by BOOK_02; seam value `alpha_top^-1 = 359/phi^2 - phi^-5`). The forcing here is its *dynamical* reading.

Closure defect. `Delta_alpha ≠ 0` manifests as a structural spectral asymmetry in cycle statistics: a fixed fraction of cycles fails to close after the projection `pi` (the Top↔Alg mismatch). Operationally, on the computable graph dynamics,

```text
P_asym(u) := 1 - Z_closed(u) / Z_all(u),
```

where `Z_all` is the total weight of admissible cycles/paths and `Z_closed` the weight of those returning to the same κ-class under `pi`. ("Asymmetry" = closure defect of the Top↔Alg seam — NOT a flow or loss of substance.)

Quadratic forcing (the symmetry argument). At small seam the natural dimensionless asymmetry scale is forced to be

```text
P_asym = Theta(Delta_alpha^2).
```

The linear term is FORBIDDEN by sign symmetry of the gluing error: `+Delta_alpha` and `-Delta_alpha` are probability-equivalent, so only even powers survive. This is what makes the closure defect a clean second-order observable rather than a tunable first-order one.

Where the mass scale lives. The passage from `P_asym` to a neutrino mass scale (via `m_e` and `Delta_alpha`) is a BRIDGE interpretation and is OWNED downstream by BOOK_03 / BOOK_04 (the neutrino quadratic readout). This section asserts only the forced *structural* result — closure defect, projection-π statistics, and the `Theta(Delta_alpha^2)` law — and cites those books for the quantitative readout; it does not re-derive the mass number here.

Cert status: the closure-defect statistics `P_asym = 1 - Z_closed/Z_all` under projection π and the `Theta(Delta_alpha^2)` symmetry-forcing are [^b06-2]; the seam numbers `alpha_top^-1` and the neutrino readout carry their own certs under BOOK_02/BOOK_03/BOOK_04 ownership and are not duplicated here.
## 06.2 Role of this book

Book 06 is the ordered finite evolution book of D0.  Books 01--02 define the condensed/profinite detector support and the finite proof calculus.  Book 03 defines the action gate and scene dynamics.  Book 04 defines matter and particle-sector finite readouts.  Book 05 defines the verification grammar.  Book 06 explains how a sequence of completed finite registrations becomes time, evolution, phase transport, entropy, classicality and ordered finite evolution transfer.

The central rule is:

```math
\boxed{
\text{evolution is not a background flow; it is an ordered quotient of completed registrations.}
}
```

Time arrow = ordered index induced by normalized or coarse-grained feedback updates whose dephased finite-window entropy is nondecreasing.

Discrete evolution endomorphism and subsystem splits (A|A^c) induce retained asymmetry bias between S3 sectors (scaffold).

The feedback-time statement requires a declared channel discipline: normalize
after measurement outcome, embed the update into an admissible channel, or assign entropy (D0: readout)
only after the specified dephasing/coarse-graining map. Time is not entropy
itself.

For feedback updates the normalized channel form is written

```math
\widehat\Phi_N(\rho)={\Phi_N(\rho)\over\operatorname{Tr}\Phi_N(\rho)}
```

when the denominator is positive. Entropy monotonicity is not claimed for an
unnormalized raw feedback operator.

Equivalently,

```math
\text{time}=\text{ordered closure of registration events}.
```

This book therefore treats time as an invariant structure induced by finite detector completion, not as an external continuum parameter that precedes measurement.

### Why memory needs a distinguishable return (the forced root)

Downstream this book carries a "memory torus", "noncommuting torus shells" and a defect/puncture as RETAINED facts. Those facts are not free: they are forced, by reduction-to-contradiction under M1, from a single demand — that a completed registration leave a return trace the observer can tell apart from no-trace. We state that root here so the rest of the book inherits the *why*, not just the *what*.

Fix a loop `gamma`: a repeatable procedure of length `m` whose frame code returns to its own configuration class, `c_{n+m} ≡_O c_n`. Its holonomy `Hol_gamma(c_n) := c_{n+m}` is just "what `gamma` did to the trace", and the holonomy bit is the distinguishability of that return,

```math
h_\gamma(n) := \Delta\bigl(c_n,\ \mathrm{Hol}_\gamma(c_n)\bigr) \in \{0,1\},
```

with `h=1` reading "returned with a tellable-apart trace".

**[THE 06.2.A] Memory requires a distinguishable return [^b06-6].** Memory is impossible if `h_gamma(n) ≡ 0`. By reduction: suppose `h_gamma(n)=0` for all `n`. Then `Δ(c_before, c_after)=0` — the "before" and "after" states are operationally indistinguishable. Then the observer `O` cannot reconstruct the fact that `gamma` was ever run; an unreconstructable fact is not a memory element, since "happened" cannot be told from "did not happen". But `gamma` was posited to be an element of history — contradiction. Hence a regime with `h_gamma = 1` must exist. The "memory torus" is the minimal carrier that *realizes* this surviving bit; it is not an assumed background.

**[COR 06.2.A.1] Order memory forces noncommutativity [^b06-7].** If two loops satisfy `Hol_{gamma_1} Hol_{gamma_2} ≢_O Hol_{gamma_2} Hol_{gamma_1}`, the observer can distinguish the *order* in which the operations ran. This is the minimal noncommutative carrier of history: order is itself a distinguishable trace, so by THE 06.2.A storing order forces holonomies that do not commute. This is the forced seed under the "noncommuting torus shells" and the defect/puncture (class-change) arguments the later sections develop — those shells noncommute *because* order memory demands it, not by stipulation.

Both claims are M1-failure repairs. The torus and its noncommuting shells follow from `T`-matrix traces, but only once memory is shown to require a distinguishable return. The derivation of the `T`-matrix, the toral support and the defect remain owned by their canonical sections; this section owns only the forcing root above.

## 06.3 Evolution cannot precede registration

A D0 event becomes eligible for evolution only after it has produced a finite record.  Before completion there is support, potential transport and unresolved comparison; after completion there is an ordered active state together with an archive remainder.  The primitive sequence is

```math
\text{support}\longrightarrow\text{finite detector channel}\longrightarrow
R=D^\dagger D\longrightarrow\text{halted record}\longrightarrow\text{ordered update}.
```

The first temporal object is not a smooth parameter `t`; it is the ordering relation on records that survive the halt quotient.

```math
r_i\prec r_j
\quad\Longleftrightarrow\quad
r_i\text{is registered before}\ r_j\text{inside the finite detector history}.
```

The continuum parameter of ordinary dynamics is integrated only after many such ordered records are coarse-grained through stable discrete evolution step conventions.

## 06.4 Active/archive decomposition

The ordered finite evolution state decomposes into an active component and an archive component:

```math
\mathcal H_{total}=\mathcal H_{active}\oplus\mathcal H_{archive}.
```

The active part contains the finite record capable of further transport.  The archive part contains information that has been resolved away by the detector quotient: phase metadata, unresolved address tails, null directions, inaccessible comparison data and dephased correlations.

A ordered finite evolution state may be written schematically as

```math
\psi_{active}(P,u)=P\,H(u)\psi_{support},
```

where `P` is the active projector and `u` is the ordered finite evolution/window parameter inherited from the finite detector depth.

Archive is not metaphysical non-existence.  It is the complement of active readout under a specified finite quotient:

```math
\Pi_{active}+\Pi_{archive}=I,
\qquad
\Pi_{active}\Pi_{archive}=0.
```

## 06.5 Forgetting maps as typed quotients

The D0 forgetting map is a typed quotient:

```math
\Delta:\rho_N\longmapsto\Delta(\rho_N).
```

It removes the information that is not stable under the declared finite readout while preserving the invariant needed for the next registration.

For a finite subsystem `A` the entropy assigned to the dephased finite-window state is

```math
S_A^{D0}=-\operatorname{Tr}_K\!\left(\rho_A^{fw}\log\rho_A^{fw}\right).
```

The classical limit is therefore not a primitive assumption.  It is the regime in which repeated typed quotients stabilize an effectively commuting record algebra.

```math
\Delta(\rho_N)\text{stable under repeated finite records}
\quad\Rightarrow\quad
\text{classical readout algebra}.
```

## 06.6 Finite phi-ordered finite evolution and depth contraction

The foundational split `p+p^2=1` is proved in Books 01--02.  Book 06 uses it as an ordered finite evolution contraction.  If a route or comparison chain has depth `N`, the finite continuation weight takes the form

```math
Q_N=Q_0\varphi^{-N}.
```

The ordered finite evolution contraction is governed by the detector asymmetry quantum

```math
\delta_0=\frac{1}{2\varphi^3}.
```

The derivation of `δ₀=(√5−2)/2=1/(2φ³)` from `φ` (positive root of `p+p²=1`) is owned by BOOK_01; this book re-uses it as a ratio, it does not re-derive it.

A finite-depth update may therefore be represented as

```math
u_{k+1}=\delta_0 u_k,
```

or, for an error/tail amplitude,

```math
\delta^{(k+1)}=\delta_0\,\delta^{(k)}.
```

This does not introduce a new physical parameter.  It is the ordered finite evolution use of the same finite-verification split that defines the detector foundation.

### 06.6.A — Why the step weights are forced to `(φ⁻¹, φ⁻²)`

The contraction above moves a route forward one tick, but it does not by itself say *how a single step splits* between moving and remembering.  Every event has two projections: an **external** share `W_ext` (change of address in the graph — "where am I?", a step across the scene) and an **internal** share `W_int` (the path-memory write — phase/holonomy, "who am I?").  D0 does not get to tune these two weights by hand; M1 forbids an exogenous catalog of coefficients, so the pair must be forced.

**[THE 6.1.2] Golden split of the evolution step — `W_ext=φ⁻¹`, `W_int=φ⁻²` [^b06-10]. [^b06-8].**
There exist two structural step weights `W_ext, W_int ∈ ℚ(φ)`, consistent with the BOOK_01 base, satisfying exactly two demands:

1. **Binary split, no catalog:** `W_ext + W_int = 1` (the step is exhausted by its two projections; no third bin is allowed without an exogenous label).
2. **Memory is the square of the external step:** `W_int = W_ext²` (the path-memory write costs the external step *recursively applied to itself* — one step's holonomy is one step seen through one step).

Then the unique solution is

```math
W_{ext}=\varphi^{-1},\qquad W_{int}=\varphi^{-2}.
```

*Proof (⊥).*  Substituting `W_int = W_ext²` into `W_ext + W_int = 1` gives `W_ext + W_ext² = 1`, i.e. `W_ext² + W_ext − 1 = 0` — the same defining quadratic of the φ-split that BOOK_01 forces from `p+p²=1`.  Its positive root is `W_ext = φ⁻¹`, whence `W_int = W_ext² = φ⁻²`.  Any other pair `(W_ext, W_int)` solving demand (1) but not (2) requires choosing the coefficients from outside `φ` — an exogenous catalog of weights ⇒ M1 violated.  □

So the same scalar that contracts the chain (`φ⁻¹` per tick) is *also* the external share of one step, and its square is the memory share: the depth contraction `Q_N = Q_0 φ⁻ᴺ` is just `W_ext` applied `N` times.  This closes the gap between "the step has two parts" and "the parts are golden" without ever importing a free weight.

### 06.6.B — Finite depth: the observer stop-protocol replaces actual infinity

The contraction `δ^{(k+1)} = δ₀ δ^{(k)}` runs "inward" forever as a formal limit: refining a distinction by one more level multiplies the resolution by `δ₀` again.  D0 admits infinity only as an *ideal* limit — any actual verification must halt at a finite depth.  The cutoff is not a tuning knob; it is fixed by the observer's own resolution floor.

The δ-ladder inward is the sequence of distinguishability levels

```math
\delta_{-1}=\delta_0^{2},\quad \delta_{-2}=\delta_0^{3},\quad\dots,\quad \delta_{-n}=\delta_0^{\,n+1},
\qquad \frac{\delta_{-(n+1)}}{\delta_{-n}}=\delta_0,
```

a discrete scale flow with constant ratio `δ₀` (a discrete RG flow, `δ₀` the fixed step).

**[DEF 54.2] Observer stop-protocol — finite cutoff depth `κ` at the floor `ε²=φ⁻¹⁶` [^b06-11]. [^b06-9].**
The observer cannot refine without bound; the resolution floor is

```math
\varepsilon^2:=\varphi^{-16}\approx 4.531038537848\times 10^{-4}.
```

Define `κ` as the minimal inward depth at which the ladder crosses the floor:

```math
\kappa:=\min\{\,n\ \mid\ \delta_0^{\,\kappa+1}\le\varepsilon^2\,\}.
```

This is the operational replacement of "actual infinity" by a finite distinguishability protocol: every check is obliged to run in the `κ`-truncation defined by `ε²`, and `κ` is a *physical* UV cutoff read off the observer floor, not a free setting [^b06-12].

The `ε²=φ⁻¹⁶` floor is the observer's distinguishability floor that *terminates the inward ladder* and so bounds the depth `N` in `Q_N = Q_0 φ⁻ᴺ`.

**Closure-sprint integration (Iteration 22).** The φ-ladder is the **first D0 continuum**: the discrete tick `A_{n+1}=φ⁻¹A_n` (golden split `p+p²=1`, `W_ext=φ⁻¹`, `W_int=φ⁻²`) has the unique continuous semigroup envelope `A(s)=A₀e^{−s logφ}` with `A(s+t)=A(s)A(t)/A₀` — `D0-PHI-LADDER-SEMIGROUP-001` (cert `vp_phi_ladder_semigroup.py`; the envelope cocycle is Lean-proved in `D0.IM.ContinuumFromFractalTick`, `env_cocycle`/`env_restricts_to_ladder`). On the golden-subshift cylinder tower the unique normalized shift-invariant trace is exactly this golden split `(φ⁻¹,φ⁻²)` — the unique left Perron eigenvector of `M=[[1,1],[1,0]]`; any other trace differing on a finite cylinder needs an external *which-frequency* catalog (⊥M1) — `D0-PHI-CYLINDER-TRACE-UNIQUE-001` (cert `vp_phi_cylinder_trace_unique.py`). The external operator-algebra reading — the crossed-product `C(X_φ)⋊ℤ` unique trace — is closed as a **passport**, not a D0 theorem: `D0-PHI-CSTAR-PASSPORT-001` (`PASSPORT-CLOSED`). The smooth-manifold limit is *not* this continuum; it stays the downstream Rieffel/GHP + Connes macro-shadow (`D0-SMOOTH-MANIFOLD-PASSPORT-001`). The finite cylinder-LANGUAGE equivalence (the golden word avoids `bb`, has Sturmian complexity `p(L)=L+1`, and its letter frequencies are the same golden split) is `D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001` (cert `vp_phi_sturmian_cylinder_conjugacy.py`); the full topological/measure conjugacy stays the external owner `D0-ADLER-WEISS-PARTITION-OWNER-001`. Beyond the finite language, the **profinite code-extensional** conjugacy is also internal: two independent codings agreeing on every finite cylinder window (language and frequency) are the same D0 profinite object by extensionality — `D0-PHI-STURMIAN-PROFINITE-CODE-CONJUGACY-001` (cert `vp_phi_sturmian_profinite_code_conjugacy.py`); only the classical smooth/measure Adler-Weiss conjugacy stays the external passport.
## 06.7 Time as invariant registration and the causal section

The D0 internal units may be represented by the normalized section

```math
\ell_0^{D0}=1,\qquad \tau_0^{D0}=1,\qquad c_{D0}=\frac{\ell_0^{D0}}{\tau_0^{D0}}=1.
```

This is not a claim that laboratory SI units are trivial.  It is the internal statement that one line-step and one discrete evolution step-step form a single causal section before external metrology is attached.  The Lean owner records the internal cone speed as a dimensionless invariant of the normalized kinematic gauge.  SI light speed is therefore a metrological export, not a fitted D0 core parameter.

The physical export of the discrete evolution step convention is handled by the matter/metrology books. The terminal relation

```math
\tau_0=\frac{h}{38m_ec^2},
```

enters Book 06 only as a cross-reference: the coefficient `38` (the action cycle `Lambda_act`) belongs to the terminal matter/readout analysis (BOOK_03-owned) and the SI-length/Newton shadow belongs to Book 07.

### The arrow is forced, not assumed

The causal section above orders registrations but does not yet say *why* the order has a preferred direction. In D0 the arrow of time is not a phenomenological postulate added on top of the section; it is forced. Three independent routes converge on the same direction, and the convergence is the point — no single one is fitted.

**Route 1 — unique reproducible assembly order [^b06-15].** The observable scene is assembled from two non-commuting role operators: `Y` (compactification / shell-fold of the outer scene into the effective 4D projection) and `J` (defect localization). The composites differ. Applying `Y` then `J` localizes the defect *inside* an already-fixed boundary structure, so the observer gets reproducible "objects": `Y∘J` is a repeatable assembly procedure. Applying `J` then `Y` localizes "out of boundary context" and the subsequent fold turns the result into noise: `J∘Y` is not reproducible.

The arrow is the M1 consequence of this asymmetry [^b06-16]. M1 admits only what can distinguish itself without an external catalog; a *reproducible* assembly procedure is exactly a registration that re-derives the same scene without importing an external order-key. Only `Y∘J` qualifies. Therefore the forward direction of time is identified with the unique catalog-free assembly order `Y∘J`, and its reverse `J∘Y` is structurally excluded — not improbable, but inadmissible. The `[J,Y]≠0` non-commutativity is thus not a convention; it is the algebraic seat of the arrow. [^b06-13]

**Route 2 — non-invertibility of the Fibonacci fusion [^b06-17].** The Finite Holographic Self-Reading Principle forbids hidden states / external memory, which forces the readout to obey the minimal non-trivial topological fusion rule `τ⊗τ = 1⊕τ` (this isolates `phi` as the minimal Jones-subfactor quantum dimension; the fusion/`phi` ownership is BOOK_01). The fundamental symmetry of the D0 scene is therefore a **non-invertible categorical symmetry**: the readout role `τ` has *no algebraic inverse*.

Standard continuous (Lie) symmetries admit inverses and hence unitary, time-reversible dynamics with Noether currents. D0 has none of that at the structural level: with no inverse for `τ`, time-reversibility is broken algebraically, not statistically. The arrow of time and the Second Law are then exact algebraic inevitabilities of the non-invertible fusion that governs holographic readout, *not* artifacts of large numbers. Unitarity is recovered only as an approximate, emergent low-energy shadow. M1 failure mode: a *reversible* fundamental readout would require an inverse role `τ^{-1}` reconstructing the pre-readout state — i.e. an external memory background storing what was traced away — which the no-hidden-state principle forbids. ⊥. So irreversibility is forced. [^b06-14]

**Route 3 — toral modular flow eigenvalue split.** This route is already certified by the finite signature-split certificate. The single modular flow is the toral time operator `T=[[0,1],[1,-1]]`, with `det = -1` and characteristic polynomial `lambda^2 + lambda - 1`. Its two real eigenvalues split: one root in `(0,1)` (contracting) and one in `(-2,-1)` (expanding, `|.|>1`). A single hyperbolic (Pisot) flow with one expanding and one contracting direction *is* an arrow: forward = the expanding/coarse-graining direction. The cert checks the split in exact integer arithmetic. The `(3,1)` signature pairs this single time flow against the rank-3 reversible spatial transport of `K(9,11,13)`, so "3 space, 1 time-with-arrow" never conflict.

The three routes agree on a single direction. Route 1 fixes the arrow as the unique reproducible registration order, Route 2 fixes *why no reverse exists* (non-invertible readout, no external memory), and Route 3 supplies the certified eigenvalue mechanism on the toral flow. The feedback-time / nondecreasing dephased-window-entropy statement of §06.2 is the entropic reading of the same arrow: entropy monotonicity is the coarse-grained shadow of the expanding eigendirection and of the irreversible trace-out, not an independent assumption.

## 06.8 Normalized discrete evolution step operator

The finite time-transition operator has a separate integer toral-automorphism layer:

```text
T = [[0,1],[1,-1]]
chi_T(lambda)=lambda^2+lambda-1
spec(T)={phi^-1,-phi}
det(T)=-1
Tr(T^n)=(-1)^n L_n
```

The determinant-square theorem `toral_volume_conservation_square` records the finite volume-balance invariant, and `trace_T_pow_eq_signed_lucas` records the integer signed-Lucas trace law without importing analytic roots as Lean primitives. Both facts are certified by the finite certificates: they check `|det(T^n)|=1` (volume conservation) and `Tr(T^n)=(-1)^n L_n` for tested `n`. What those certify is the *identity*; the forcing welds below say *why* this particular `T` is THE time generator.

### 06.8.W det(T) IS the Vieta invariant B — the cause of orientation reversal per tick

The bare fact `det(T)=-1` and the trace law `Tr(T^n)=(-1)^n L_n` are present, but the FORCING WELD is that `det(T)` is not a free sign — it is the canonical Vieta invariant.

**[THE 06.8.W] One time step reverses orientation because `det(T) = -1 = B` [^b06-22].** The product of the roots of the minimal equation `chi_T(lambda)=lambda^2+lambda-1` is the determinant of time. That product is exactly the Vieta invariant `B: phi*psi = -1`, owned by BOOK_01 01.7 in the ABCD role alphabet. So:

- `det(T) = -1 = B` ⇒ a single tick `T` reverses orientation. The sign of `det(T)` is the *seventh incarnation* of the canonical Z2 (the orientation register), not an incidental minus.
- `T^2` then has `det(T^2) = +1` and `spec(T^2) = {phi^-2, phi^2}` — the orientation-PRESERVING square. This `+2` step is literally THE 3.11.B: the even step of the spine is the passage to the orientation-preserving square of the time operator. The "why an even step" derivation is therefore not a separate postulate but a direct reading of `det T = B`.

The `|det(T^n)|=1` half is cert-backed by the finite certificate; the *identification* `det(T) = Vieta-B = orientation cause* is a structural weld onto the owned invariant `B`. [^b06-18].

### 06.8.M The toral automorphism T IS the modular-time generator (Tomita-Takesaki)

The FACTS are fixed — `T=[[0,1],[1,-1]]`, `chi_T=lambda^2+lambda-1`, `spec={phi^-1,-phi}`, the signed-Lucas trace, and active contraction / archive expansion as eigen-branches of one toral automorphism. What remains to state is the *algebraic WHY* time emerges at all from the active/archive restriction.

**[THE 06.8.M] Time is the Tomita-Takesaki modular flow; `T^n` is its discrete realization [^b06-23].** D0 admits no background temporal parameter `t` — there is no external clock to distinguish, ⊥M1. Time is forced as follows:

- Whenever the holographic carrier is split into the retained/active sector `P_N` and the traced/archive sector `Q_N` (the split owned by BOOK_01), the restriction of the pure topological state to the active boundary is a highly entangled thermal density matrix `rho_active`. By Tomita-Takesaki, this state uniquely defines a modular operator `Delta` and a one-parameter automorphism group `sigma_s(O) = Delta^{is} O Delta^{-is}`. Time IS this modular flow; ordered finite registration is merely the discrete spectrum of `Delta`.
- The integer toral automorphism `T` generates that flow explicitly: `T^n` is the modular flow, and the active-sector decay and archive-trace accumulation are the two eigen-branches of the SAME discrete automorphism. Time is thus the invariant trace sequence `Tr(T^n)=(-1)^n L_n` of a deterministic, non-invertible Fibonacci fusion process.
- The fractal tick `A_{n+1} = phi^{-1} A_n` (owned by 06.40) is then not a fitted decay rule but the rigorous algebraic consequence of `Delta` transporting symplectic area into the archive. Time does not "pass"; time is the thermodynamic effort to hold the holographic boundary against the growing entanglement entropy of the bulk.
- GOLDEN REM 51.6 gives the same origin algebraically: the modular group `sigma_t^omega` is induced by the pair `(A, omega)`, and the non-commutativity `[J, Y] != 0` (local insertion `J` vs trace-out `Y`) is the incompatibility that *makes* temporal ordering algebraic — a structure of the observable algebra and the choice of `omega`, never an external metric. The intrinsic-time conclusion (time from the toral automorphism `T`, not from a metric) is the same conclusion; this weld supplies the modular-operator mechanism behind it.

[^b06-19]. No modular/Tomita-Takesaki certificate exists yet, so this claim carries no finite-cert backing of its own. The trace-sequence backbone `Tr(T^n)=(-1)^n L_n` is the cert-backed handle.

### 06.8.K I_f = log phi is the KS entropy of the memory-torus automorphism

**[THE 06.8.K] `I_f = h_KS(T) = log phi` [^b06-24].** The Kolmogorov-Sinai entropy of the toral dynamics is `h_KS = log|lambda_max| = log phi`. The Book-09 GW target `I_f ≈ log phi` (the 35–85 Hz "horizon hum" frequency ladder) then ceases to be a bare passport number: it is the entropy comb of the canonical automorphism of the memory torus. [^b06-20].

### 06.8.F Phenomenological time as the Feshbach-Schur archive-circulation delay

Feshbach-Schur enters here as a *time* mechanism, not merely as the matter-pole / effective-transfer tool it serves elsewhere. The derivation below ties the archive nullity-30 directly to temporal flow and is load-bearing.

**[THE 06.8.F] Time is the Neumann-series index `k` of phase circulating in the 30-dim archive before return [^b06-25].** The global state of the finite holographic carrier is static under the unitary `U_N`. Time emerges *only* for an observer restricted to the active transport boundary `P_N`. Evaluating the effective active-sector evolution requires tracing over the 30-dimensional sterile archive `Q_N` (the rank-3 / nullity-30 scene `K(9,11,13)` owned by BOOK_01); the solution is strictly the Feshbach-Schur complement

```math
\mathcal W_{\mathrm{eff}}
= P_N U_N P_N
+ P_N U_N Q_N\,(I - Q_N U_N Q_N)^{-1}\,Q_N U_N P_N .
```

Expanding the traced-out-complement resolvent as a Neumann series exposes the discrete structure of temporal flow:

```math
\mathcal W_{\mathrm{eff}}
= P_N U_N P_N
+ \sum_{k=0}^{\infty} (P_N U_N Q_N)\,(Q_N U_N Q_N)^{k}\,(Q_N U_N P_N).
```

The phenomenological "passage of time" is algebraically identical to the discrete index `k`: time is the algorithmic delay caused by phase information circulating inside the sterile archive `(Q U Q)^k` before its eventual observable return to the active boundary. This welds the archive nullity-30 to the temporal index. [^b06-21]. This is now cert-closed by `D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001` and `D0-ARCHIVE-NEUMANN-TICK-OWNER-001` (Lean `D0.Evolution.FeshbachSchurTimeDelayOwner`: the order-`k` Neumann term carries exactly `k` archive circulations, `k=0` being the direct `P U P` channel), and folded into the combined `D0-STATIC-TO-DYNAMICS-OWNER-001`.

The archive increment of a finite state `rho_N` is measured schematically by

```math
\Delta B_N(\rho_N) = \operatorname{Tr}(F_N\,\rho_N),
```

with the feedback-return operator `F_N = (Q_N U_N P_N)^\dagger (Q_N U_N P_N)` owned by BOOK_02, subject to the sector-specific normalization and quotient rules of BOOK_05. Completed readout increases the archive ledger associated with the declared split — this is the time direction of trace accumulation.

### Finite graph dynamics: the normalized step

For finite graph dynamics, background time is replaced by a normalized discrete evolution step operator.  If `A` is the finite adjacency/action operator and `D` its degree/normalization operator, the canonical discrete evolution step form is

```math
T_{discrete evolution step}^{D0}=D^{-1/2}AD^{-1/2},\qquad \rho(T_{discrete evolution step}^{D0})=1.
```

The condition `rho(T_discrete evolution step)=1` is the finite stability condition for ordered finite evolution propagation.  It prevents the discrete evolution step from being either a hidden expansion parameter or an unbounded background evolution.

A witness transport along a finite route `gamma` is represented as

```math
\mathcal U_\gamma^{D0}:
\mathcal H_{active}(a)\longrightarrow\mathcal H_{active}(b),
```

and the corresponding transition probability takes the finite response form

```math
P(b|a,\gamma)=
\frac{\operatorname{Tr}(\Pi_b\,\mathcal U_\gamma R_a\mathcal U_\gamma^\dagger)}
{\operatorname{Tr}(R_a)}.
```

## 06.8.S Static-to-dynamics closure

Dynamics in D0 is not a primitive input; it is forced by finite self-readout. The chain has three linked owners, each a proved finite fact (combined owner `D0-STATIC-TO-DYNAMICS-OWNER-001`, Lean `D0.Evolution.StaticToDynamicsOwner`; cert `vp_static_to_dynamics_owner.py`):

```
static finite scene -> self-readout -> [J,Y] != 0 -> ordered registration
   -> Feshbach archive delay index k -> phi-tick weight phi^-1 -> continuous semigroup envelope
```

**Block I — order obstruction (the time arrow).** The localization defect-shift `J` (nilpotent on the rank-3 localization block, `J^3=0`) and the boundary-closure readout `Y` (idempotent, `Y*Y=Y`) do not commute: `[J,Y]` is nonzero already on the archive-to-localization channel. A self-readout whose operations commuted would be order-blind and could recover its own event order only from an external catalogue — which M1 forbids. So registration is forced ordered, and that ordered registration is the time arrow (`D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001`, `D0-TIME-ARROW-ORDERED-SELF-READOUT-001`, Lean `D0.Evolution.JYNoncommutativeOrderObstruction`, wired to the proven M1 selector spine; cert `vp_jy_noncommutative_order_obstruction.py`). This is the Lean owner of the BOOK_02 §02.9A commutator obstruction, which previously had no Lean. Honest residual: the UNIVERSAL claim that *every* commuting self-readout on *any* carrier erases order is not proven — it is the named PROOF-TARGET `JY-UNIVERSAL-COMMUTING-READOUT-OBSTRUCTION`; the owner proves the specific D0 `(J,Y)` witness and the binary-selector M1 reductio.

**Block II — Feshbach archive delay is the tick.** For an observer restricted to the retained sector `P_N`, the active evolution is the Feshbach–Schur complement `W_eff = P U P + P U Q (I - Q U Q)^{-1} Q U P`; expanding the archive resolvent `(I - Q U Q)^{-1} = Σ_k (Q U Q)^k`, the order-`k` term carries exactly `k` internal archive circulations before observable return. The Neumann index `k` IS the discrete time tick (`D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001`, `D0-ARCHIVE-NEUMANN-TICK-OWNER-001`). Honest residual: the tick identity is closed on the resolvent/convergence domain (spectral radius of `Q U Q < 1`).

**Block III — φ tick weight and continuous envelope.** Each archive-delay tick multiplies the active amplitude by `φ⁻¹`, the unique root of the detector self-return split `p+p²=1` in `(0,1)`; hence `A_{k+1}=φ⁻¹A_k`, and the unique continuous envelope is `A(s)=A₀·exp(−s·log φ)` with cocycle `A(s+t)=A(s)A(t)/A₀` (`D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001`, `D0-CONTINUOUS-TIME-SEMIGROUP-ENVELOPE-001`, Lean `D0.Evolution.PhiFractalTickDynamics`, reusing the existing ladder/envelope owners `D0-IM-003` and `D0-PHI-LADDER-SEMIGROUP-001`). No primitive time, external clock, or SI unit (`c`, `h`, `ħ`, seconds) enters the chain; the combined `D0-DYNAMICS-NOT-PRIMITIVE-CERT-CLOSED-001` records that the order and the tick weight are both derived.

**[Constrained Hamiltonian embedding bridge].** The retained/archive Feshbach–Schur delay has a standard non-reciprocal-dynamics analogue: a constrained Hamiltonian embedding with auxiliary variables. The D0 archive is NOT identified with the article's auxiliary bath; rather, the bridge says effective non-reciprocal active dynamics can be represented by a Hamiltonian/symplectic enlarged system plus a constraint preserved by the flow, with the active dynamics on the constraint submanifold (`D0-FESHBACH-CONSTRAINT-SUBMANIFOLD-BRIDGE-001`, `D0-FLOQUET-NONRECIPROCAL-DYNAMICS-BRIDGE-001`, PASSPORT-CLOSED; Nature Physics 2026 `s41567-026-03317-0`). FORMALISM, never CORE confirmation.

**[Reheating energy pointer].** The heat-trace time parameter `u` also owns the finite reheating energy functional used in BOOK_08: `E(u) = −∂_u log H(u)` (`D0-REHEATING-ENERGY-BUDGET-OWNER-001`). This is phase-time heat energy over the discrete archive tick, not SI time or an external clock.## 06.9 Phase transport and quantum emergence

Quantum evolution appears when the finite active record is transported without being immediately forced into a commuting classical quotient.  The finite-stage transport has the standard unitary-looking form

```math
\rho_N\mapsto U_N\rho_NU_N^\dagger,
```

but its interpretation is D0-specific: `U_N` is a finite transport of an already addressed detector support.  It does not presuppose an infinite background Hilbert space.

The bridge to quantum mechanics is therefore

```math
\mathcal F_Q:D0\to QM,
```

where the target quantum formalism is the continuum completion of finite detector transport.  The bridge is valid only when the D0 finite-window protocol has been declared.

## 06.9a Tiling-hull ordered finite evolution

Time evolution over the D0 vacuum is represented as translation dynamics on the φ-quasicrystalline tiling hull. The ordered discrete evolution step chain supplies the ordered finite evolution order; the irrational φ phase supplies non-periodic transport; finite quotient windows produce stable detector-visible averages.

```text
fixed detector support
-> ordered discrete evolution step transport
-> φ-quasicrystal hull translation
-> finite quotient window
-> smooth macro-ordered finite evolution shadow
```

The hull, its φ cut-and-project origin, its non-periodicity and its support for gap labeling are carried by the Lean tiling-hull owner and discharged by the finite tiling-hull certificate.

## 06.10 Uncertainty as a finite-window protocol

Uncertainty is not imported as an independent metaphysical postulate.  It is the finite cost of resolving non-commuting readout channels inside one detector window.  The source notation records this as

```math
\Delta_J\Delta_\partial\ge 1.
```

Here `J` denotes action/scene resolution and `partial` denotes boundary/derivative resolution.  Book 06 reads this as a protocol inequality: increasing precision in one finite channel consumes the detector window available to the conjugate channel.

## 06.11 Evolution of scales: selection, not new knobs

Evolution may change which quotient is active, which transfer window is used, and which sector bridge is allowed.  It may not introduce a new scale by convenience.

The active scale discipline is inherited from Book 03:

```math
\Lambda_{act}
```

and sector consequences are downstream projections:

```math
\Lambda_{act}
\longrightarrow
\text{matter dressing},\text{ordered finite evolution coefficients},\text{scattering windows},\text{boundary response of the traced-out sector}.
```

This rule is essential.  Without it, evolution would become a place to hide fitted constants.

## 06.12 Runtime coefficient readout sequence

Several ordered finite evolution coefficient shadows are not independent derivations inside Book 06; they are read as a sequence of typed readouts from already-defined books:

```math
\pi_0\text{-holonomy}\to G_N,
```

```math
q_{res}\text{ electromagnetic ordered finite evolution dressing}\to\alpha,
```

```math
T_W/T_Z\text{ ordered finite evolution ratio}\to\theta_W,
```

```math
V_9\text{ two-way color holonomy}\to\alpha_s,
```

```math
\Lambda_{act}\varphi^5q_{mass}^{-(d_9+2Rank)}\to\Lambda_{QCD}.
```

The proof locations are Books 02--04 and the metrological export is Book 07.  Book 06 keeps the ordering principle: coefficients become observed through ordered finite evolution quotients and transfer windows, not through free empirical anchoring.

## 06.13 Tick-to-scattering comparison protocol

Scattering is the experimental form of finite ordered finite evolution.  The Book 06 contract is

```math
\text{finite support}\to T_{discrete evolution step}^{D0}\to\mathcal U_\gamma^{D0}\to P(b|a,\gamma)\to\sigma_{exp}.
```

The discrete evolution step-to-scattering expression is

```math
\sigma_{D0\to exp}=\ell_0^2\,\mathcal J_{exp}\,P_{D0},\qquad
\ell_0=\frac{h}{38m_ec}.
```

The important discipline is that the finite transition probability `P_D0` must be fixed before the experimental Jacobian `J_exp` is attached.

## 06.14 Archive-pressure ordered finite evolution kernel

Archive pressure is an ordered finite evolution effect of the active/archive split.  The finite ordered finite evolution space has the form

```math
\mathcal H_{ordered finite evolution}=\mathcal H_A\oplus\mathcal H_N,
```

and the detector cut may be written schematically as

```math
\mathcal C_{det}=\delta_0^8I.
```

The archive-pressure operator belongs to Book 06 as an ordered finite evolution kernel, but its cosmological empirical use belongs to Book 08.  This prevents a common error: using survey likelihoods to define the traced-out complement operator.

The allowed direction is

```math
\text{detector archive/ordered finite evolution split}
\longrightarrow
\text{archive-pressure operator}
\longrightarrow
\text{S_DE or survey transfer comparison protocol}.
```

The forbidden direction is

```math
\text{survey residual}
\longrightarrow
\text{invent boundary response of the traced-out sector}.
```

## 06.15 Saturation, horizons and the gravity cross-reference

Finite ordered finite evolution can saturate, in horizon language and Einstein-side heat-trace language. Book 06 records the ordered finite evolution principle:

```math
\sigma(R)\to1
\quad\Rightarrow\quad
\text{saturated finite readout}.
```

Detailed gravity statements, including the length-depth theorem, Newton/Planck shadows, Einstein heat trace and horizon archive interpretation, are assigned to Book 07.  Book 06 only fixes the ordered finite evolution boundary: saturation is a finite detector condition before it is a spacetime interpretation.

## 06.16 Falsification rules for evolution claims

An evolution claim fails if any of the following occurs:

1. it uses a background continuum time before finite registration;
2. it introduces a new scale outside the single-section discipline;
3. it hides a fitted coefficient in an ordered finite evolution window;
4. it uses cosmological, scattering or matter data to define the operator that is later claimed to predict them;
5. it erases the distinction between active state and archive quotient;
6. it moves a gravity or cosmology result into Book 06 to avoid its sector comparison protocol.

The positive test is:

```math
\text{finite record}\to\text{typed forgetting}\to\text{normalized discrete evolution step}\to
\text{sector transfer}\to\text{falsifiable comparison protocol}.
```

## 06.17 Claims inherited from the theorem database

**Canonical source: the claim registry** (`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` / generated `03_THEORY_MAP/theory_status_map.csv`) is the single source of truth for claim IDs and `release_status`. This table is the **Book 06 sector view** — the `Book 06 role` column is its only sector-specific content; the statuses mirror the registry and are not edited here independently. The parallel gravity-sector view is §07.16.

| Claim ID | Domain | Status | Claim | Book 06 role |
|---|---|---|---|---|
| `D0-FOUND-002` | Foundation | `CORE-FOUNDATION` | Minimal addressable record split | foundation/metrology reference |
| `D0-FOUND-003` | Continuum Measurement | `CORE-FOUNDATION` | Minimal continuum-measurement skeleton | foundation/metrology reference |
| `D0-SCENE-002` | Detector Scene | `CORE-ACTION` | J_scene selects K(9,11,13) | action-ordering reference |
| `D0-ACTION-001` | Action Spine | `CORE-ACTION` | S_gate/J_scene backbone | action-ordering reference |
| `D0-METRO-001` | Metrology | `CORE-FOUNDATION` | Single causal line/discrete evolution step invariant | foundation/metrology reference |
| `D0-METRO-002` | Metrology | `SINGLE-SECTION-OUTPUT` | Lambda_act single action section | foundation/metrology reference |
| `D0-QM-001` | Quantum Readout | `CORE-MEASUREMENT` | Born/Hilbert finite trace ratio | ordered finite evolution/theorem use |
| `D0-THERMO-001` | Entropy | `CORE-MEASUREMENT` | Finite-window entropy from archive forgetting | ordered finite evolution/theorem use |
| `D0-DYN-001` | Dynamics | `CORE-RUNTIME` | Normalized discrete evolution step and witness transport | ordered finite evolution/theorem use |
| `D0-VERTEX-001` | Vertex/Scattering | `CORE-RUNTIME` | Finite S-matrix registry | ordered finite evolution/theorem use |
| `D0-LEPTON-002` | Charged Leptons | `ACTIVE-PASSPORT` | Charged-lepton generation action | matter evolution consequence |
| `D0-PHOTON-001` | Photon/Neutrino | `CORE-MEASUREMENT` | Photon massless carrier | matter evolution consequence |
| `D0-NEUTRINO-001` | Photon/Neutrino | `CORE-MEASUREMENT` | Neutrino neutral leakage mass-square pattern | matter evolution consequence |
| `D0-COEFF-003` | QCD | `CORE-RUNTIME` | QCD ordered finite evolution and archive/confinement scale | matter evolution consequence |
| `D0-GRAV-001` | Gravity | `SINGLE-SECTION-OUTPUT` | Length-depth theorem and Planck/Newton shadow | gravity cross-reference |
| `D0-COSMO-001` | Cosmology/Archive | `CORE-MEASUREMENT` | Archive-pressure operator | archive-ordered finite evolution cross-reference to cosmology |
| `D0-COSMO-003` | Dark/Archive | `ACTIVE-PASSPORT` | Boundary dark survey-driver kernel | archive-ordered finite evolution cross-reference to cosmology |
| `D0-COLLIDER-001` | Collider | `EXTERNAL-BRIDGE` | Collider ordered finite evolution typed bridge | ordered finite evolution/theorem use |
| `D0-PI0-001` | Cycle/Holonomy | `CORE-FOUNDATION` | pi0 finite-cycle versus pi continuum generator | foundation/metrology reference |

## 06.18 Cross-book boundary summary

| Topic | Book 06 treatment | Final proof/comparison protocol location |
|---|---|---|
| `p+p^2=1`, `delta0`, `ABCD` | ordered finite evolution use only | Books 01--02 |
| `S_gate`, `J_scene`, `Lambda_act` | ordering and scale discipline | Book 03 |
| photon/electron/neutrino/QCD coefficients | evolution consequences | Book 04 |
| verification and promotion statuses | referenced | Book 05 |
| discrete evolution step, forgetting, entropy, phase transport | normative | Book 06 |
| `pi0`, SI length, Newton/Planck, Einstein heat trace | boundary cross-reference | Book 07 |
| boundary response of the traced-out sector in BAO and survey likelihood | ordered finite evolution kernel only | Book 08 |

## 06.19 Integrated causal-information invariants

A compact causal-information invariant layer belongs in the evolution book because it explains why time is not an external parameter but a stable ordering of finite records.

A D0 evolution step is admissible only if it preserves:

```text
addressability,
finite registration,
quadratic response,
causal ordering,
archive/active separation.
```

The invariant content of a finite history is therefore not the continuum path between records but the ordered class of registered transitions:

```math
\mathcal H_N=\big((a_0,R_{a_0}), (a_1,R_{a_1}),\ldots,(a_k,R_{a_k})\big)/\sim_{D0}.
```

Forgetting is a quotient on this history, not destruction of the finite event:

```math
\Delta(\rho_N)=\sum_a \Pi_a\rho_N\Pi_a,
```

with the discarded off-diagonal data entering the traced-out complement sector. This block is the evolution-side counterpart of Book 01's condensed detector halt.

## 06.20 Wilsonian RG as a typed forgetting map

Definition. The D0 forgetting map is a typed finite quotient on recorded metadata. Its Wilsonian bridge is the comparison dictionary that maps this quotient to external coarse-graining above a declared scale.

At the D0 level, forgetting is a typed quotient:

```math
\Delta_N:\rho_N \longmapsto \Delta_N(\rho_N),
```

where finite address, phase or high-depth metadata are moved from the active record to the traced-out complement.  At the QFT/EFT bridge level, Wilsonian coarse-graining integrates or quotients modes above a declared comparison scale.  The bridge dictionary is therefore:

```math
\Delta_N
\quad\leadsto\quad
\mathcal R_{\mathrm{SM}}^{\mathsf S}(\mu \leftarrow \Lambda_{\mathrm{act}}),
```

not as an identity of theories, but as a typed comparison map between the finite D0 active sector and the infrared scheme used by an experimental observable.

The admissible diagram is:

```math
O_{\mathrm{D0}}^{\mathrm{bare}}
\longrightarrow
O_{\mathrm{SM}}^{\mathsf S}(\Lambda_{\mathrm{act}})
\longrightarrow
O_{\mathrm{SM}}^{\mathsf S}(\mu),
```

with the first arrow being the declared dressing dictionary and the second arrow being the standard EFT/RG evolution in the declared scheme.

The guardrail is strict.  RG evolution is not allowed to repair a failed D0 invariant by adding new degrees of freedom.  It may only transport a fixed finite boundary object through an explicitly declared external evolution law.

### Why the bridge is a forgetting map (the forcing)

The bridge above is correct as a discipline object, but a guardrail alone does not show the forcing that makes the guardrail necessary. The forcing is that RG running is *itself* the same typed quotient `Delta_N`, viewed at the QFT level — not a separate dynamical law that happens to look like forgetting. Three M1-failure repairs establish this.

**[LEM 06.20.A] A Feynman loop IS a closed light-cycle, and D0 loops create mass and charge [^b06-26].** A "quantum loop" in a Feynman diagram is not a drawing on paper. A diagram in D0 is an equivalence class `[gamma]_~` of histories sharing one topology (loop count, branch vertices, exits), so a loop in that class is literally a closed light-cycle `P` of the kind BOOK_04 owns from the cycle/holonomy structure. The consequence is a sign flip against standard QFT: in QFT loops give *corrections* to mass and charge; in D0 loops *create* mass and charge (the mass/charge themselves are cycle/holonomy facts, owned downstream by BOOK_04). The two readings are not interchangeable, and the difference is exactly what the next lemma localizes.

**[COR 06.20.A.1] UV divergences are the artifact of pointlike loops; D0 loops have finite size kappa_k [^b06-27].** Standard QFT's divergences (the infinities that renormalization is built to absorb) arise precisely *because* a loop is treated as pointlike: integrating an unbounded internal momentum over a structureless point has no cutoff to stop it. In D0 there is nothing to diverge: every loop is a closed light-cycle with a finite structural size, the refinement-level limit `kappa_k`. The cutoff is not imposed by hand to regulate an integral; it is the resolution floor of the level, so the "infinity" never forms. By reduction under M1: a genuinely pointlike loop would require resolving structure below `kappa_k`, i.e. reading a distinction the level cannot record — an appeal to detail outside the active catalog, which M1 forbids. Hence loops carry finite size, and divergence is a bridge artifact of the pointlike idealization, not a fact of the D0 object.

**[THE 06.20.B] Running couplings are an information-compression artifact of the projection; the RG equation is information conservation across scale [^b06-28].** Fix two refinement levels `k` (coarse) and `k+1` (fine), with the typed projection `pi_{k+1 -> k}` — the same forgetting quotient as `Delta_N`, indexed by scale. At level `k+1` the graph shows detailed topology: many small cycles, fine braiding of edges. Applying `pi_{k+1 -> k}` collapses that structure into effective node parameters:

```math
\pi_{k+1\to k}:\ (\text{fine cycle at }k{+}1)\ \longmapsto\ (\text{node ``mass'' at }k),\qquad
(\text{edge braid})\ \longmapsto\ (\text{effective interaction}).
```

So a coupling that "runs" with scale is not a constant acquiring energy dependence; it is the shadow of how much cycle structure the projection at that level discards. The standard RG equation, read in D0, is therefore the statement that information is *conserved* under the change of level: nothing is created or destroyed by re-scaling, only re-typed between the retained record and the traced-out complement (the retained/traced split is owned by BOOK_01). This is why the Wilsonian bridge of 06.20 must be a forgetting map and not an extra law — RG running and `Delta_N` are the same quotient seen at two resolutions.

**[CHK 06.20.B.1] No free counter-terms: the effective parameter is fixed by the projection alone [^b06-29].** The effective coupling at level `k` is

```math
g(k) := \pi_{k+1\to k}\bigl(g(k+1)\bigr) + r_k,
```

with `r_k` the bounded `kappa`-residue of the level (the coarse-graining error, capped by the refinement protocol). There are no additional free counter-terms in CORE. By reduction under M1: a free counter-term not fixed by `pi_{k+1 -> k}` would be an entry the theory must store as an exogenous parameter — an external catalog of interaction strength, which M1 forbids exactly as it forbids a coupling constant `lambda` not equal to `1` or a power of `phi`. Hence the effective charge `g(k)` is a function of the graph statistics `G_k`, measured on the graph, not inserted by hand. This is the CORE-side reason the guardrail above is strict: RG may transport the boundary object through `pi`, but it may not smuggle in a new degree of freedom, because there is no slot to store one.

These four repairs do not re-derive the bridge dictionary, the `Lambda_act` boundary or the retained/traced split — those stay owned by their canonical sections (BOOK_03 owns `Lambda_act`; BOOK_01 owns the `F_N` feedback operator and the retained/traced split; BOOK_04 owns mass/charge from cycle/holonomy). They supply the *why*: that Wilsonian RG is a typed forgetting map because running, divergence and loop-generated mass are all readings of one scale-indexed projection `pi`, and any deviation from it would require an external catalog M1 rules out. The graph-Laplacian RG-flow direction is checked at cert level by the finite Laplacian RG-flow certificate. The forcing-by-contradiction discipline itself is DEF-0.2.2.
## 06.21 Claim-level RG bridge guardrail

The RG/forgetting identification is a typed bridge, not a licence to import arbitrary continuum structure.  A Wilsonian step is admissible only when it is presented as a forgetting morphism from a declared finite D0 source object:

```math
O_{SM}^{\mathcal S}(\mu)
=\mathfrak D_{SM}^{D0}(\mathcal S,\mu,\Lambda_{act})[O_{D0}^{bare}].
```

The bridge must keep the field content, beta-functions, threshold conventions and scheme explicit.  A hidden new particle, new threshold, or scheme change is an external hypothesis and cannot repair a D0 residual.  This is the operational form of the traced-out complement/forgetting interpretation of RG flow.

## 06.22 RG/coarse-graining as typed forgetting

The Wilsonian interpretation of D0 is not a rhetorical analogy.  A typed forgetting map is a finite-to-effective comparison morphism:

\[
\Delta_{RG}:\operatorname{Obs}^{D0}_{active}\longrightarrow
\operatorname{Obs}^{scheme}_{IR}(\mu),
\]

where the target is scheme-labelled.  `Δ_RG` may integrate out, trace out or coarse-grain finite metadata, but it may not introduce new fields, new scales or new beta functions unless the status is explicitly changed from D0 bridge to a different physical model.

Thus RG dressing is allowed only as external comparison calculus:

\[
O_{bare}^{D0}\neq O_{PDG},
\qquad
O_{PDG}=\Delta_{RG}^{scheme}(O_{bare}^{D0}).
\]

This prevents the Standard Model from being used as a hidden source of D0 invariants while still allowing it to be used as the correct infrared comparison engine.

---

## 06.23 Scheme-specific RG/PDG comparison protocol closure

Scheme-specific comparison with PDG or collider conventions is a typed bridge, not a core theorem.  The bridge file must declare:

```text
bare_d0_object
renormalization_scheme
scale_mu
matching_scale_Lambda_act
field_content
beta_functions
threshold_conventions
observable
external_table
forbidden_parameters
falsification_hook
```

A bridge comparison protocol is closed when these fields are fixed before numerical comparison.  It is not closed by reproducing a table after choosing a convenient scheme.  The release includes such comparison templates for the coefficient, lepton, CKM, QCD and BAO-facing rows.

## 06.24 Forgetting as entropy-selected coupling

The D0 forgetting map is a finite entropy-selected coupling, not a metaphorical archive projection. Given retained response tests `Test_D0(N)`, the forgetting bridge is the kernel

```math
K_N^* = \arg\max_{K_N}\ H(Y_N|X_N)
```

subject to the declared retained response constraints and loss quotient. This matches the Wilsonian intuition of coarse-graining: high-resolution metadata are not arbitrarily discarded, but are integrated out by the unique maximum-entropy representative compatible with retained finite responses.

Consequently, an RG bridge is closed only after specifying:

```text
retained response tests;
forgotten coordinates;
loss quotient;
entropy/gauge representative;
flow scheme.
```

This makes the RG/forgetting layer a constructive finite bridge rather than a continuum smoothing ansatz.

Terminology lock: RG/forgetting is a `convex-response` bridge and must expose a `coupling kernel` preserving retained response tests before loss quotient.

## 06.25 RG/forgetting as an executed finite entropy bridge

The forgetting map is not an informal loss of information.  At a finite stage it is represented by a conditional kernel selected by maximum entropy under retained D0 response constraints.  Given a finite response grid `Y` and retained response `r`, the forgetting channel is

```math
K^*(y_j\mid r)=\frac{\exp(\theta(r)y_j)}{\sum_k\exp(\theta(r)y_k)},
```

with `θ(r)` uniquely fixed by `\sum_jK^*(y_j\mid r)y_j=r`.  This is the finite D0 analogue of Wilsonian coarse-graining: discarded metadata are not arbitrary; the retained response fixes the unique maximum-entropy representative in the quotient.

The executable finite-entropy certificate verifies this construction for the BAO/S_DE response windows and supplies the model for RG/PDG bridge kernels.

## 06.26 Executed macro-forgetting source

The archive-to-continuum bridge begins with a finite source. A unit archive act is represented by the bounded centered operator

```math
\mathsf A_k \in [-a,a],\qquad a=\delta_0^8/30,
```

after active-sector centering. The normalized archive atom `Z_k=\mathsf A_k/a` obeys

```math
\mathbb E\exp(tZ_k)\le \exp(t^2/2).
```

Therefore

```math
X_N=N^{-1/2}\sum_{k=1}^N Z_k
```

is a finite subgaussian archive vector before any continuum Gaussian comparison is made. This supplies the D0 side of the HST-style macro bridge. The bridge is a comparison functor from finite archive statistics to macro Gaussian modelling, not an ambient-continuum primitive.

## 06.27 Lepton magnetic moment as RG/forgetting bridge

In standard QFT, the anomalous magnetic moment is scheme-dependent and receives QED, electroweak, hadronic vacuum-polarization and hadronic light-by-light contributions. In D0 this is represented as an external RG/forgetting bridge from a finite ABCD holonomy in the lepton support shell to a continuum comparison scheme:

\[
a_\ell^{D0,S}(\mu)=a_\ell^{S,baseline}(\mu)+K_{g-2}^{D0}(\mu)\mathcal R_{residual}^{D0,S}.
\]

The term \(K_{g-2}^{D0}\) is finite and single-section locked. The residual trace \(\mathcal R_{residual}^{D0,S}\) is not allowed to introduce new fields or modified beta functions. This turns `g−2` into a scheme comparison protocol rather than a free new-physics knob.

## 06.28 Tick-to-space unfolding

The ordered finite evolution discrete evolution step does not merely order events. When paired with a cyclic phase quotient it generates a branch foliation. A near-return modulus `q` turns the one-dimensional discrete evolution step line into residue branches; admissibility filters select which branches survive as observable geometry. This is the finite mechanism by which ordered registration can unfold into spatial structure before any smooth manifold is invoked.

## 06.29 Phase-unfolding master chain

**Canonical mechanism: §01.19** (phase-unfolding master chain — the map `U_τ(n)=(n, n mod τ)` turns an ordered finite registration into a branch foliation; the residue classes mod `q` are the coherent branches, an admissibility filter selects the visible ones). Owned there, not re-derived. The time/evolution-sector content recorded here is what *supplies* that ordered finite evolution:

The time operator supplies the non-periodic ordered finite evolution.  The integer toral
automorphism `T=[[0,1],[1,-1]]` orders the active/archive ladder through
`Tr(T^n)=(-1)^n L_n`, while the phase owner fixes the return increment
`alpha_D0=phi^-2` (§01.21).  Tick order is therefore not a periodic clock embedded in a
background lattice; it is an ordered finite evolution whose detector-visible branches are
created only by finite return quotients.

The terminal and electroweak return windows reached by this ordered-evolution quotient — `q_T=44`, `m_T=7`, `φ_E(44)=20=d₁₃`; `q_EW=710`, `m_EW=113`, `φ_E(710)=280=|Ω₈|·35 ⇒ D_EW=35` — and their M1-forcing are owned by **§01.22 / §07.23**; they are not re-derived here.

## 06.30 Hurwitz-rigid phase generator and non-resonant spatial unfolding

**Canonical derivation: §01.21** (Hurwitz-rigid phase generator — `α_D0 = p² = φ⁻²` is the maximally non-resonant rotation; `φ⁻²` irrational rotation ⇒ non-resonant archive smoothing, finite return modulus `q` ⇒ residue branch geometry). Owned there, not re-derived. The time/evolution-sector consequence recorded here:

By the Phase-Unfolding Theorem (D0.Geometry.PhaseUnfoldingQuasicrystal):

```text
toral_ordered finite evolution_supplies_quasicrystal_order;
quasicrystal_order_not_periodic_lattice.
```

## 06.30a Time evolution over the φ-quasicrystalline hull

Time evolution over the D0 vacuum is represented as translation dynamics on the $\varphi$-quasicrystalline tiling hull. The continuous flow on this hull projects the discrete phase steps into smooth invariant averages under the cut-and-project setup. The hull, its φ cut-and-project origin, its non-periodicity and its support for gap labeling are carried by the Lean tiling-hull owner; verification is performed by the finite tiling-hull and gap-labeling certificates.

### Why the hull-flow has a canonical phase↔time scale (no external coefficient)

The translation flow needs a scale to convert *scene phase time* $u$ (the dimensionless heat-kernel / diffusion parameter on the scene) into *dynamic time* $t$. That scale is not chosen — it is forced. The minimal scene step is $\varepsilon$, the $\delta_0$-bridge gap; phase time runs at the *square* of the step because diffusion is second order in the step. So the unique dimensionless link carrying **no external number** is

$$
u = \varepsilon^2\, t = \varphi^{-16}\, t .
$$

Forcing argument: any alternative $k\varepsilon$ or $m\varepsilon^2$ with $k,m\neq 1$ smuggles an external coefficient $k$ or $m$ into the phase↔time map. M1 (physics = what survives self-distinguishability without an external catalog) forbids importing an external number, so $k=m=1$ is the only admissible normalization, and $u=\varepsilon^2 t=\varphi^{-16}t$ is unique. **Status: FORCED** [^b06-30]. This is the canonical-scale closure of the earlier remark that the heat-trace scale is internal (and of $\xi_5=\varphi^{-5}$, the torus-address integerization defect, discharged by the finite ξ5 torus-defect certificate): both are scene-internal because both refuse external coefficients.

### Connectivity defect and the fiber factorization (heat-trace building blocks)

Let $\{\widehat\lambda_i\}_{i=1}^N$ be the **traced** (quenched) spectrum (BOOK_01 owns the retained/traced split). Define the heat trace and the D0 connectivity defect

$$
\mathrm{HeatTrace}(u)=\sum_i e^{-u\widehat\lambda_i},
\qquad
D(u)=1-\frac{1}{N}\sum_i e^{-u\widehat\lambda_i}.
$$

$D(u)$ is the fraction of the scene **unreachable by diffusion** in phase time $u$ — the operational meaning of "not yet distinguished". The hull flow factorizes over the fiber: the generator is the direct sum of the spatial and scene generators rescaled by the canonical scale,

$$
G_{\mathrm{fib}} = G_{\mathrm{space}} \;\oplus\; \big(\varepsilon^2\, G_{\mathrm{scene}}\big),
\qquad u=\varepsilon^2 t ,
$$

so the heat traces multiply and the spectral dimension is additive:

$$
P_{\mathrm{fib}}(t)=P_{\mathrm{space}}(t)\cdot P_{\mathrm{scene}}(\varepsilon^2 t),
\qquad
d_{\mathrm{fib}}(t)=d_{\mathrm{space}}(t)+d_{\mathrm{scene}}(\varepsilon^2 t).
$$

These are the load-bearing pieces of heat-trace time, not Weyl asymptotics added by hand. **Status: FORCED** [^b06-31]. Spectral-dimension / Weyl scaling of the factorized heat trace is checked by the finite heat-trace Weyl-dimension and heat-capacity certificates.

### Heat-Trace Time: the arrow is a corollary, not a postulate

Define information time $I_{\mathrm{fib}}(t):=-\log P_{\mathrm{fib}}(t)$. The exact factorization above gives **additivity**

$$
I_{\mathrm{fib}}(t)=I_{\mathrm{space}}(t)+I_{\mathrm{scene}}(\varepsilon^2 t).
$$

So "time" in D0 is accumulated diffusion information over the graph spectrum — fixed without any external coefficient, the only translation into phase time being $u=\varepsilon^2 t$ (LEM II.2.LEG18.0.2). **Status: FORCED** [^b06-32]. The arrow of time is then a *corollary*: heat-trace decays as $t$ grows (diffusion spreads across modes), hence $I_{\mathrm{fib}}(t)$ is monotone increasing. Directionality of time follows from heat-trace decay — **no separate time-arrow postulate is needed** [^b06-33]. This strengthens the earlier "time arrow = ordered registration with entropy monotonicity": ordered registration *is* monotone $I_{\mathrm{fib}}$.

The spectral dimension is evaluated by the **analytic** spectral formula — no numerical differentiation of $\log P(t)$ with respect to $\log t$ —

$$
d_S(t)=2\,t\cdot\frac{\sum_i \widehat\lambda_i\, e^{-t\widehat\lambda_i}}{\sum_i e^{-t\widehat\lambda_i}}
\qquad(\texttt{d0/spectrum.py::spectral\_dimension\_analytic}).
$$

**Status: FORCED** [^b06-34].

The threshold **κ-epochs** are the solutions of $D(u)=\kappa$ for $\kappa\in\{\varepsilon^2,\varepsilon,\xi_5,\delta_0\}$, an internal grid (no external times). On the verification lattice $S_L$ at $L=129$ over the scene $K(9,11,13)$ these land, via $u=\varepsilon^2 t$, at stable D0-times $t$:

| $\kappa$ | $t$ (D0-time) | reading |
|---|---|---|
| $\varepsilon^2$ | $\approx 1.6184$ | first touch of distinguishability (start of physical time) |
| $\varepsilon$ | $\approx 76.8719$ | primary structure (nuclear / primary synthesis in BRIDGE) |
| $\xi_5=\varphi^{-5}$ | $\approx 338.1960$ | observer horizon (recombination / CMB in BRIDGE) |
| $\delta_0$ | $\approx 449.8500$ | full distinguishability (transition to galactic structure in BRIDGE) |

**Status: FORCED-grid** [^b06-35]. The grid is forced because $\{\varepsilon^2,\varepsilon,\xi_5,\delta_0\}$ are exactly the scene-internal scales already on the spine; no epoch time is fitted.

### The hull is two-dimensional because Q(φ) has degree 2 — time is a layer, not a world

The hull-flow lives on a **2-torus** $T^2$, and this dimension is forced, not chosen. The self-description $p+p^2=1$ is quadratic, so the minimal M1-admissible field is $\mathbb{Q}(\varphi)$ of **degree 2** (a degree-1 rational field would be capture — a closed external coordinate — which M1 forbids). The time layer therefore has dimension $=\deg\mathbb{Q}(\varphi)=2$, i.e. $T^2$. **Status: FORCED** [^b06-36].

This is a feature, not a risk. By Adler–Weiss (PNAS 57 (1967) 1573) a smooth Markov partition of a toral automorphism exists **iff** the spectrum is Pisot. In degree 2 the golden number is Pisot: its conjugate $\psi=1-\varphi=-0.618\ldots$ has $|\psi|<1$, so the toral Markov partition on $T^2$ is **smooth** and the symbolic dynamics is clean (the Fibonacci word codes the golden foliation without pathology). The Bowen / Kenyon–Vershik non-smoothness only bites for $n\ge 3$ — i.e. it would only afflict an attempt to make *time* multidimensional, which D0 never does. A three-dimensional time would hit non-Pisot pathology; D0 requires two-dimensional time and lands exactly in the clean zone. **Status: FORCED** [^b06-37].

### Side synthesis: (3,1) signature from two independent objects

The Lorentz signature $(3,1)$ is forced by **two distinct mechanisms**, which is why $3$ and $2$ do not conflict (space-rank and time-layer-degree count different things):

- **"3"** $=\operatorname{rank}(\text{adjacency of }K(9,11,13))$ — three non-zero transport modes = reversible **space** (BOOK_01 owns the $K(9,11,13)$ scene, rank 3 / nullity 30);
- **"1"** $=$ one modular flow, the toral time operator $T=\begin{psmallmatrix}0&1\\1&-1\end{psmallmatrix}$ with $\operatorname{spec}=\{\varphi^{-1},-\varphi\}$ — a single Pisot contraction = **time**.

Space (graph spectrum) and time (torus automorphism) are different objects, so rank-3 and a single modular flow coexist without tension; the terminal involution $\eta_4=\operatorname{diag}(1,-1,-1,-1)$ stamps the $(1,3)$ signature. The Lorentzian asymmetry has a candidate mechanism: three non-Pisot directions (space, reversible) versus one Pisot flow (time, with an arrow via $|\psi|<1$) — **the arrow of time is the Pisot contraction of the conjugate**. **Status: FORCED** [^b06-38].

**The causal partition is now forced (closes BOOK_07 §07.51.3).** The "candidate mechanism" above is upgraded to a theorem (`D0-RANK3-CAUSAL-CONE-FORCING-001`, Lean `D0.Synthesis.RankCausalConeForcing`): a Lorentzian `(3,1)` form has exactly one timelike axis and three spacelike, the counts match the one Pisot arrow (`|\psi|<1`) and the three reversible real-spectrum rank-3 modes (discriminant `6\,185\,264>0`), and a Euclidean `(4,0)` is excluded — so the arrow-direction **is** the timelike axis and the rank-3 modes **are** the spacelike sector. This grounds `C_max=3/8=\operatorname{rank}/|\Omega_8|` (BOOK_07 §07.51.3); the only residual is the cone-speed/smooth metric, the Connes-owned unit.

**Named external owner of "modular flow".** The word *modular* here is not borrowed loosely: its classical owner is **Tomita–Takesaki modular theory** (Tomita 1967; Takesaki, LNM 128, 1970), under which a von Neumann algebra with a cyclic–separating vector carries a *canonical* one-parameter modular automorphism group, unique up to inner automorphism (Connes' Radon–Nikodym cocycle) — the "thermal time" of Connes–Rovelli. That time is fixed by the (algebra, state) pair, **not** read from an external clock-catalogue — exactly the M1-compatible content D0 needs. This is recorded as the forcing-owner edge `D0-TIME-MODULAR-FLOW-OWNER-001` (assumption `ASSUMP-TOMITA-TAKESAKI`, Lean `D0.Bridge.TomitaTakesakiBridge`). Honest scope: D0 proves only the *Pisot/symbolic* structure of the single time flow above; identifying that flow with the Tomita–Takesaki modular automorphism is the named external owner, cited not re-derived (BOOK_05 §05.8.R).

**Time and flavor share the SL(2,ℤ) modular group [LEM].** There is a second, *distinct* sense in which time is "modular" — and it links time to **flavor**. The D0 flavor group `A_5 = 2I/\{\pm1\}` (from the icosians → `E_8`, BOOK_02 §02.18) is exactly the **level-5 finite modular group**: `\overline{\Gamma}_5 = \mathrm{PSL}(2,\mathbb{Z})/\Gamma(5) = \mathrm{PSL}(2,5) \cong A_5` (the modular flavor symmetry of Feruglio; Ding–Everett–Stuart, *Nucl. Phys. B* **857**, 219; arXiv:1110.1688). The toral time generator `T=\begin{psmallmatrix}0&1\\1&-1\end{psmallmatrix}` is a golden/hyperbolic element of `\mathrm{GL}(2,\mathbb{Z})` (det `-1`, `h_{KS}=\log\varphi`). So **time (a `GL(2,ℤ)` element) and flavor (the level-5 quotient `A_5`) both live in the `SL(2,ℤ)` modular-group structure** (claim `D0-MODULAR-TIME-FLAVOR-001`, cert `vp_modular_time_flavor.py`). This also fixes the solar mixing: `\sin^2\theta_{12} = \tfrac13 - 2\delta_0^2 = 0.3055`, closest to NuFIT 6.0 (`0.307`) and beating the classical golden-ratio predictions GRA (`0.276`) and GRB (`0.346`). **Crucial distinction (mechanism filter):** this `SL(2,ℤ)` *modular group* is **NOT** the Tomita–Takesaki *modular automorphism* of the previous paragraph — the word "modular" carries two different mathematical meanings, and they are kept apart here, not conflated. **Status MECH-LIMIT** (time↔flavor identification): the real shared structure is the modular group; the full identification "the golden time element and the `A_5` level-5 quotient are one modular object" is the named open gap. The rate `h_{KS}=\log\varphi` here is *exactly* the closure-holonomy stretch per monodromy turn (§02.13.h, `D0-SEAM-HOLONOMY-001`); and `\sin^2\theta_{12}=\tfrac13-2\delta_0^2` is the **closed-loop (`δ₀²`) member** of the *derived* seam-topology rule (`D0-PMNS-SEAM-TOPOLOGY-001`, §04.5): the angle is derived (rule THE / value CHK, <0.5σ vs JUNO-2026); only the time↔flavor modular identification stays the named gap.

**CKM ↔ PMNS: not mutual inverses, but complementary.** A proposed relation `V_{CKM} U_{PMNS}^{T} = I_3` is **false** (claim `D0-CKM-PMNS-COMPLEMENTARITY-001`, cert `vp_ckm_pmns_orthogonality.py`): `V_{CKM} U_{PMNS}^{T}=I` would force `V_{CKM}=U_{PMNS}` (i.e. CKM `=` PMNS), but CKM angles are **small** and PMNS **large** — in the 1–2 sector `R(\theta_C)R(\theta_{12})^{T}=R(\theta_C-\theta_{12})\approx R(-20.6^\circ)\neq I`. The salvaged, experimentally real content is **quark–lepton complementarity**: `\theta_C + \theta_{12} \approx 13.04^\circ + 33.6^\circ = 46.6^\circ \approx 45^\circ` (a `\sim1.6^\circ` near-coincidence). Status **HYP** — an approximate relation, not an exact identity; the strong orthogonality is rejected, the weaker complementarity kept.

**Internal Lucas–Voronoi Markov partition (`D0-LUCAS-VORONOI-MARKOV-PARTITION-001`).** The toral time generator `T = \begin{psmallmatrix}0&1\\1&-1\end{psmallmatrix}` is read not via an *imported* Adler–Weiss theorem but through an **internal** partition built from integer Lucas-trace data: `Tr(Tⁿ) = (−1)ⁿ Lₙ` gives explicit boundary cuts `L₂ = 3, L₃ = 4, L₅ = 11`; the map is volume-preserving (`det(Tⁿ)² = 1`) and **κ-stable** (the Pisot contraction `|ψ| < 1` forces finite refinement) — Lean `D0.Geometry.LucasVoronoiMarkovPartition`, cert `vp_lucas_voronoi_markov_partition.py`. This is OPERATOR-SCAFFOLD-CERTIFIED: the explicit Lucas-boundary partition + κ-stability are owned; the Voronoi-cell-exact Markov property (`D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001`, PROOF-TARGET) and the full topological conjugacy `T ≅` golden SFT (`D0-TORAL-TIME-MARKOV-CONJUGACY-001`, PROOF-TARGET — needs an explicit Williams shift-equivalence) stay open. The D0-internal profinite-code conjugacy is already closed (`D0-PHI-STURMIAN-PROFINITE-CODE-CONJUGACY-001`); classical Adler–Weiss stays the cited external owner `D0-ADLER-WEISS-PARTITION-OWNER-001`, not re-derived.

**[Iter22 eight-front]** The shift-equivalence question for the D0 toral time operator now has a precisely-scoped internal closure (D0-WILLIAMS-SHIFT-EQUIVALENCE-OWNER-001, CERT-CLOSED). Over the integers we prove: charpoly(T)=X^2+X-1 and charpoly(M)=X^2-X-1 for the Fibonacci companion M=[[1,1],[1,0]] (from trace/determinant); an explicit GL(2,Z) similarity U*(-T)=M*U with U=[[0,1],[-1,0]] and det U=+1, exhibiting N=-T and M as conjugate over Z; and agreement of the two classical shift-equivalence invariants — equal nonzero spectrum (charpoly(N)=charpoly(M), the Galois sign-flip r<->-r of charpoly(T)) and equal Bowen-Franks group Z^2/(I-A)Z^2 (the Smith normal form of both I-M and I-N is diag(1,1), so both groups are trivial), each witnessed by explicit unimodular reductions P*(I-A)*Q=I. This is exactly the necessary-condition layer: the shift-equivalence invariants agree, but they are necessary not sufficient for conjugacy. Full TOPOLOGICAL conjugacy of the toral time-map with the golden SFT, and full Williams strong-shift-equivalence, remain EXTERNAL (Adler-Weiss/Williams, ASSUMP-ADLER-WEISS) — owners D0-TORAL-TIME-MARKOV-CONJUGACY-001 and D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001 stay PROOF-TARGET. The cert `vp_toral_shift_equivalence.py` enforces this boundary with reachable controls rejecting (i) upgrading agreeing invariants to a conjugacy claim, (ii) a wrong companion matrix, and (iii) a non-golden/non-Lucas boundary matrix.
## 06.31 φ-discrete RG as a typed forgetting step

The renormalization bridge is a typed forgetting map over the D0 scale ladder. At level `k`, the comparison scale is

```text
μ_k = Λ_act φ^{-k}.
```

A coupling `g_k` is transported by a finite-difference beta operator

```text
β_φ(g_k) = (g_{k+1}-g_k)/(-log φ).
```

The continuous RG equation is the interpolation shadow of this ladder. The bridge is valid only relative to an explicitly declared scheme, threshold convention and field content. Changing the beta coefficients or thresholds after comparison is a hidden external repair and invalidates the comparison protocol.

## 06.31a Gap-labeled RG bands

The φ-discrete RG ladder may be read as a sequence of frozen operator bands. Spectral gaps in these bands are admissible only when they carry hull/K0 labels.

The requirement that gap labels live on a frozen operator and form a countable set is carried by the Lean K-theory gap-labeling owner, and discharged by the finite gap-labeling certificate.

## 06.32 Canonical cyclic phase distance and forgetting geometry

The forgetting geometry on finite fibers of size $N$ is equipped with a canonical cyclic phase distance:
\[
d_{phase}(i, j) = \frac{\min((i - j) \bmod N, (j - i) \bmod N)}{N}.
\]
This cyclic distance defines the metric on finite archive fibers, ensuring nonnegativity, symmetry, and identity of indiscernibles. It is verified in Lean core, providing the structural basis for forgetting phase transport without relying on ambient-continuum coordinates.

## 06.32.1 Boundary status for Hurwitz, Bianchi and gauge transformations

The local D0 phase class and the D0 internal dimensions 1/2/4/8 are Lean-owned through `D0.Algebra.D0InternalDimensionSelector`. Global Hurwitz exhaustion is external mathematical background, not an active core dependency for forgetting/phase transport.

The non-abelian layer is also a boundary layer. The flat tensor no-go shows that a naive tensor product of two skew sectors leaves the skew/vector sector, the non-abelian curvature module records the corrected finite skew-preserving construction, and the Bianchi module records the residual expansion only:

```text
D0.Gauge.FlatTensorNoGo
D0.Gauge.NonAbelianDiscreteCurvature
D0.Gauge.BianchiResidual
D0.Gauge.YangMillsKillingPositivity
D0.Gauge.MatrixRepGaugeTransform
```

The exact Bianchi statement is closed on the graded incidence complex by `D0.Gauge.GradedBianchiIdentity`; the flat ungraded matrix residual remains a `NO-GO`. Finite gauge covariance is closed on the Wilson-link model by `D0.Gauge.WilsonLinkGaugeCovariance`. This closure is group-level and requires an associative `[Group G]` link carrier. Octonions are non-associative and cannot serve directly as the connection group; D0 uses the GaugeGroupDerivable boundary, meaning a derived associative automorphism group or matrix representation group.

## 06.33 Renormalized archive Laplacian as finite forgetting

The phase-canonical archive Laplacian is local on each cyclic fiber, but strict pullback compatibility under refinement is too strong. The correct finite forgetting statement is RG-type:

```text
L_{n+1}
  -> coarse-grain by the traced-out complement phase projection B
  -> B^T L_{n+1} B
  -> compare with L_n by scale plus residual.
```

Lean records the strict operator no-go, while the finite RG certificate checks the effective quadratic-form flow. For the canonical phase projection the projected residual is zero with scale `1`; the strict pullback commutator remains a rank-2 seam defect. This is now the ordered finite evolution meaning of archive curvature in the forgetting layer: not deletion, but the measured failure of strict flat pullback transport.

## 06.34 Refinement seam as archive forgetting boundary

The current seam layer makes the forgetting boundary explicit. Energy descends exactly across the traced-out complement phase projection, but the lifted operator transport has a localized commutator:

```text
C_n = L_{n+1} B_n - B_n L_n.
```

The seam is the finite boundary where one additional refined phase point is folded back into the coarser archive cycle. The finite seam-curvature certificate verifies that this defect is rank `2`, supported on four seam entries, and has HS density `4`. Thus the traced-out complement forgetting boundary is not an uncontrolled loss term; it is the finite seam where curvature is measured.

### Why the seam cannot close: the gluing anomaly forces residual dynamics

The non-vanishing commutator `C_n` is not an artifact of one particular lift; it is the carrier of a CORE obstruction. The seam glues a finer refinement layer onto the coarser archive cycle, and that gluing carries a non-zero anomaly: the seam defect cannot be transported away by any choice of `B_n`. Write `Δα` for this gluing anomaly — the algebraic-minus-topological mismatch measured at the seam [^b06-40]. The forcing runs by contradiction against M1 (DEF-0.2.2):

- CORE: `Δα ≠ 0`. The seam commutator `C_n` is the witness — rank `2`, HS density `4`, certified by the finite seam-curvature certificate. A vanishing anomaly would require `C_n ≡ 0`, i.e. `L_{n+1} B_n = B_n L_n`, which the certificate falsifies.
- Suppose, for contradiction, the system could relax fully — drive the residual seam curvature to zero. Full relaxation means the refined layer folds back into the archive cycle with no leftover defect, i.e. the seam is closed exactly. But closing a seam with `Δα ≠ 0` requires an external object that supplies the missing gluing data — an external catalog against which the refinement could be re-indexed without paying the anomaly.
- M1 forbids exactly such an external catalog: physics is what survives the requirement to distinguish itself *without* an external catalog. So no catalog is available; the seam cannot be closed; full relaxation is impossible.
- Therefore an inevitable residual remains at every seam. This residual is not noise to be eliminated — it is the **origin of dynamics**: because the seam never closes, the lifted transport must keep moving, and that forced motion is what time and evolution are in D0 [^b06-41].

[^b06-39] — the finite seam-curvature certificate discharges the CORE leg (`Δα ≠ 0` via `C_n` rank `2`, HS density `4`); the M1 no-catalog step and the "origin of dynamics" lift remain a cert obligation open at the BRIDGE level. `Δα` as a named CORE invariant is owned downstream (BOOK_03); this section cites it as the seam-local anomaly and does not re-derive it.

This reframes the forgetting boundary one level deeper. §06.34's first half showed the seam is where curvature is *measured* (finite, rank-2, not an uncontrolled loss). The gluing-anomaly forcing shows *why there is a seam to measure at all*: a closable seam would need an M1-forbidden external catalog, so the finite defect `C_n` — and with it the descent of energy across the traced-out complement — is structurally inevitable rather than incidental.

### 06.34a Generative dynamics: D0 is a generator, not a static classifier [LEM]

The seam anomaly above is the seed of a larger closure: it answers the standing question *is D0
a static classifier of a finite scene, or a generator of dynamics?* The answer is **generator**,
and the mechanism is **Feshbach–Schur** on the forced active/archive split (claim
`D0-GENERATIVE-DYNAMICS-001`). The previously open cert obligation of `[^b06-39]` (the M1
no-catalog step + "origin of dynamics" lift) is discharged at the finite level by the
certificates below; the only residual is the continuum-limit step, held honestly at MECH-LIMIT.

1. **Effective dynamics (Feshbach–Schur).** Split the carrier into the active block `P` (the
   rank-3 non-zero spectrum of `K(9,11,13)`) and the archive block `Q` (the 30-fold kernel).
   Integrating out `Q` gives the effective operator on the visible block,
   `W_eff(z) = A - B (D - zI)^{-1} C`, and the **Schur determinant identity**
   `det(M - zI) = det(D - zI)·det(W_eff(z) - zI)` (verified exactly,
   `vp_feshbach_schur_dynamics.py`) shows the resonances (masses/widths) are precisely the poles
   of `W_eff`. The Feshbach series `W_eff = A + Σ_{k≥0} z^{-(k+1)} B D^k C` indexes archive
   excursions by `k`: the depth `k` *is* the D0 algorithmic time. Dynamics is generated by
   integrating out the traced-out complement (D0: archive) — not imposed.

2. **Time = the seam that cannot close.** The non-intertwining `C_n = L_{n+1}B - B L_n ≠ 0` is
   machine-checked: the Galerkin restriction `Bᵀ L_{n+1} B = L_n` holds (the Laplacian is
   preserved under coarsening) yet `C_n ≠ 0` (Lean `D0.Claims.GluingAnomalyTime`, `native_decide`;
   `vp_gluing_anomaly_time.py`). A vanishing `C_n` would need `B` aligned to the eigenbasis of
   `L_{n+1}` — an external spectral catalogue M1 forbids. The scalar gluing anomaly is the
   already-certified `Δα` (`D0-DELTA-ALPHA-EXACT-001`).

3. **Loop floor: finite cycles, no UV divergence.** The excursion series truncates at the
   structural floor `ε² = φ^{-16} = (2207 - 987√5)/2 ≈ 4.531×10⁻⁴` (`vp_loop_floor_epsilon.py`):
   the branch weight `φ^{-2k}` drops below it at exponent 16, so a "loop" is a finite memory
   cycle, not an integral to infinity. **Honest named gap:** `ε² ≈ 4.53×10⁻⁴` is close in order
   to the gluing anomaly `Δα ≈ 3.71×10⁻⁴` but is **not** equal to it — the two exact `ℚ(φ)`
   numbers are kept distinct, not identified.

4. **RG = typed forgetting (develops §06.20).** Coarse-graining is a forgetting map
   `g(k) = π_{k+1→k}(g(k+1)) + r_k` with `|r_k| ≤ δ₀`; `π` conserves total weight exactly
   (`p + p² = 1`), and the running coupling is the accumulated residual, whose smooth envelope is
   the Callan–Symanzik `β = c/\log φ` (`vp_rg_forgetting.py`). The bare β-function is the cost of
   re-packing metadata as resolution drops.

**Status MECH-LIMIT (honest).** The mechanism is written and finite-certified: D0 *generates* a
scattering dynamics whose resonances, time index, finite loops, and running couplings all follow
from the active/archive Feshbach–Schur split. The one open step to THE is an explicit S-matrix
simulation of the D0 automaton (`D0.Bridge.ColliderRuntimeTypedBridge`), which would show the
continuum QFT is the thermodynamic *envelope* of the finite automaton. Until that simulation
exists, "QFT = shadow of the D0 automaton" is a strong MECH-LIMIT, cited not over-claimed.
## 06.35 Internal cone speed and the role of time

c_D0 = 1 is the invariant causal propagation bound of finite hull dynamics. It means one admissible discrete evolution step cannot cross more than one finite adjacency layer. The SI value of light speed is unit printing, not the invariant.

Three statements must be kept apart and not conflated:

1. D0 internal length discrete evolution step: the primitive finite propagation section has one line unit and one discrete evolution step unit.
2. Internal cone invariant: `internal_cone_speed_eq_one` states `c_D0 = 1` as a dimensionless cone-speed normalization.
3. SI metrology: `299792458 m/s` is the external unit conversion fixed by the SI definition of metre and second.

Therefore D0 does not fit the speed of light.  It fixes the internal causal cone before SI units are attached.  Any later physical comparison must preserve this separation; changing a unit convention cannot change the D0 causal section.

This also sharpens the time claim: time is not an extra continuum substance added to the graph.  It is the invariant registration order of finite propagation, and the smooth time coordinate is a large-scale language for that order.

**Deep-stitch closure (Iteration 22): connectivity spectral gap (Fiedler λ₂=20) and the internal cone speed as a unit gauge.** The Fiedler value (smallest nonzero Laplacian eigenvalue) of `K(9,11,13)` is `λ₂=20>0` (connected; the edgeless carrier has `λ₂=0`), established from explicit real 33×33 ℚ-eigenvectors. The internal cone speed `c_{D0}=ℓ₀/τ₀=1` is one edge per discrete Floquet step — honestly a **unit-fixing gauge** (`ℓ₀=τ₀=1`), NOT a derivation; the SI speed of light is neither input nor output (rejected control). Owners: `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001` and `D0-C-LIGHTCONE-PERCOLATION-OWNER-001` (both CERT-CLOSED), Lean `D0.Cosmology.CLightconePercolationOwner`, certs `vp_connectivity_spectral_gap_speed.py` / `vp_c_lightcone_percolation_owner.py`. Full spectrum-completeness and an exact Cheeger bound stay PROOF-TARGET.
## 06.36 Finite discrete evolution step-gauge closure

Discrete evolution step-gauge closure: a finite record is admissible as an internal kinematic gauge only when the line readout and the time readout are two faces of one common causal section.

The active formulation replaces the shorthand `length discrete evolution step = time discrete evolution step` with a finite causal section. The owner is

```text
D0.Bridge.FiniteCausalTickSection
```

A finite record is admissible as an internal kinematic gauge only when the line discrete evolution step and the time discrete evolution step are two readouts of one common section discrete evolution step.  Lean owners:

```text
D0.Bridge.finite_causal_tick_section_forces_same_tick
D0.Bridge.finite_causal_tick_section_cone_speed_eq_one
D0.Bridge.common_tick_rescaling_preserves_internal_cone_speed
D0.Bridge.asymmetric_ticks_not_internal_gauge
```

Thus `c_D0=1` is a theorem-level finite section invariant.  It is not the SI number `299792458 m/s`; that number belongs to external metrology and fixes the human unit convention.  Common rescaling of line and discrete evolution step units preserves the invariant; asymmetric rescaling is an SI/export operation and cannot become a D0 core gauge.

The Lorentz-facing owner

```text
D0.Bridge.FiniteLorentzTickGaugeClosure
```

adds the terminal role signature `(1,3)` through

```text
D0.Bridge.finite_lorentz_tick_gauge_signature_closed
D0.Bridge.finite_lorentz_tick_gauge_no_euclidean_export
D0.Bridge.finite_lorentz_tick_gauge_no_split_export
```

The macroscopic Lorentz bridge may integrate this finite carrier into smooth spacetime kinematics, but it may not change the core cone speed, add a second elementary speed, or export Euclidean/split signature as the D0 internal geometry.

### 06.36.1 — Why signature (1,3) and not (4,0), (2,2): the 3+1 split is forced (not posted)

The carrier above states the signature (1,3) as a closed FACT; the forcing of *why* (1,3) is the only admissible split is recorded here. The "3" and the "1" are two DIFFERENT objects, which is exactly why there is no 3-vs-2 conflict [^b06-43]:

- **"3" = rank of the K(9,11,13) scene adjacency** — the 3 non-zero transport modes (space = graph spectrum). Scene ownership is BOOK_01 (K(9,11,13), rank 3 / nullity 30); cite, do not re-derive. These 3 directions are non-Pisot and reversible: reversible space.
- **"1" = a single toral time flow** — one modular automorphism of the time torus T = [[0,1],[1,-1]] on T^2. This is one object, not a fourth spatial mode, so the "3" (rank) and the "2" (degree of the minimal M1-admissible field Q(phi)) do not collide.

The Lorentzian asymmetry (3,1) is therefore: **3 non-Pisot reversible space directions vs 1 Pisot time flow**. This is a strictly stronger forcing than deriving the time arrow only as feedback-channel ordering (a non-Pisot, weaker statement). The upgrade:

```text
arrow of time = Pisot contraction of the Galois conjugate (|psi| < 1)
```

Because phi is Pisot in degree 2 (|psi| = (sqrt5 - 1)/2 = 0.618 < 1), the Galois conjugate psi of the toral spectrum contracts under forward iteration of T. That contraction is the time arrow: it is intrinsic to the Pisot spectrum of T, not added by hand, and it does not touch the 3 non-Pisot space directions (which stay reversible). The feedback-channel ordering of the earlier formulation survives as a *consequence* of this contraction, not as its source.

Status: FORCED, discharged by the finite Galois–Lorentz signature certificate (Galois trace layers ActiveArchiveTrace(2,3,5) = 3, -4, -11; det(T^n)^2 = 1; roleSignature = (1,3), no Euclidean/split export). [^b06-44]

The spin-2 wave operator uses the same terminal discrete evolution step/Lorentz carrier in concrete
finite form:

```text
eta4 = diag(1,-1,-1,-1)
k4   = (1,1,0,0)
u4   = (1,0,0,0)
```

This is a dimensionless `c_D0=1` carrier.  No SI calibration of `G_N` is
introduced here.

### 06.36A — Lorentz factor and time dilation from the discrete causal budget

The carrier and the (1,3) signature fix the geometry; they do not yet say *why* a moving memory cycle reads less proper time. That is the time-dilation forcing, and in D0 it is budget thermodynamics, not curvature of an ambient Minkowski manifold. Special relativity is not posted; it is the algebraic consequence of the finite information budget of one holographic readout tick.

**Forcing (Discrete Lorentz Factor).** A fundamental causal tick carries a normalized unit budget of symplectic area, `C = 1`. For a massive state — a stable topological memory cycle — that single tick-budget partitions into two orthogonal actions:

1. external transport `dx` — changing address on the active boundary;
2. internal holonomy `ds` — advancing the phase of the internal memory cycle.

Orthogonality is symplectic-area preservation, and it enforces the Pythagorean budget constraint on the one unit discrete evolution endomorphism:

```text
|dx|^2 + |ds|^2 = 1.
```

Define the external transport velocity `v := |dx|` in [0,1]. The proper time the internal cycle experiences is exactly the *residual* budget left over after transport spends its share:

```text
dtau := |ds| = sqrt(1 - v^2),     gamma = dt/dtau = 1/sqrt(1 - v^2).
```

The Lorentz factor `gamma = 1/sqrt(1 - v^2)` is then automatic. Time dilation is the strict thermodynamic rationing of a finite readout cycle: a cycle that spends more of its unit budget on external transport has less left to advance its own phase, so it ages less. Negative control: any update rule that violates symplectic-area preservation immediately loses relativistic invariance — the `|dx|^2 + |ds|^2 = 1` partition is what *is* the invariance.

[^b06-42]. This is a core M1-style derivation (budget-rationing, not geometry); the symplectic-area-budget certificate has not yet landed. [^b06-45]

Gravity ordered finite evolution exports remain internal until a bridge is declared:

```text
c_D0 = 1 discrete evolution step gauge
eta4 terminal signature
```

DSS echoing (critical gravitational collapse) is the log-time recurrence counterpart of finite ordered finite evolution recurrence at a capacity boundary. It is not ordinary smooth evolution; it is discrete self-similar log-periodic readout at the horizon threshold (see Book 07 07.49).

Finite horizon capacity saturation is an ordered finite evolution halt: Cost_R(∂) → ∞ for external active extension. The archive quotient renders information inaccessible without deletion (cross-ref Book 07 07.50).

δ₀ finite readout cut: heat trace scale is internal, not SI time.
## 06.37 φ⁵ torus invariant and ordered finite evolution quasicrystal geometry (Phi^5 Torus Invariant)

The D0 memory torus uses a dimensionless internal geometry invariant:

```text
a = phi^5
xi5 = phi^-5
R/r = (1 + xi5) / (1 - xi5)
```

The shell normalization is

```text
R-r = 1
R+r = a
```

so the three shell boundaries are `R-r`, `R`, and `R+r`. This ordered finite evolution quasicrystal geometry is connected with the cut-and-project vacuum support and noncommuting torus shells. This introduces no SI length scale and no external mass unit; SI calibration remains a bridge layer.

The torus address is `(R+r)/(R-r) = phi^5`, read in the GOLDEN §52 zone language as "11 + xi5": an integer address `11` plus a residual `xi5`. The sections below show xi5 is not a tuned residual but a forced object — the integerization defect of that address.

### 06.37.1 ξ₅ is the integer-defect of the torus address (forced, not tuned)

Status: THE / CERT-CLOSED [^b06-46].

For odd `n` the golden ratio obeys the exact identity `phi^n = L_n + phi^-n` (Lucas number `L_n`, the integer part; `phi^-n`, the irrational excess). At `n = 5` this reads

```text
phi^5 = 11 + phi^-5         (L_5 = 11)
xi5  := phi^-5 = phi^5 - 11 = phi^5 - L_5
```

So the torus address `phi^5` splits *exactly* into its integer address `11` and the defect `xi5`. `xi5` is therefore the integerization defect of the memory-torus address — owned, not fitted. This welds three facts that otherwise sit apart: the `xi5 = phi^-5` invariant (this section), the `|Tr(T^5)| = 11` time-return (06.37.1 below; BOOK_06 03.23 echo), and the "11 + xi5" address language.

The same `xi5` then drives the α-form as a derived term, not an inserted one:

```text
alpha^-1 = 359/phi^2 - (phi^5 - 11) = 359/phi^2 - xi5
```

read as **channel capacity of the scene (`359/phi^2`) minus the integer-defect of the torus address (`xi5 = phi^5 - 11`)**. The correction `xi5` is not a tuned member: it is the Lucas error at the fifth time-return, `Tr(T^5) = -L_5 = -11` (cf. 06.37.1). [^b06-47]

Status boundary (per GOLDEN §16.3, unchanged): the numeric line `alpha^-1 = 359/phi^2 - xi5 = 137.0356...` against experiment `137.035999084` leaves a residual `Delta_alpha ~ 3.7e-4` that remains **CHK** — a declared gluing anomaly, not promoted to THE until `Delta_alpha` receives an analytic second-order owner. The structural α-form is forced; the experimental-precision prediction of α is not (α is known to `~1.5e-10`, seven orders below this residual). This same `Delta_alpha` is the seed of the neutrino scale `Sigma m_nu = Delta_alpha^2 * m_e`.

### 06.37.2 Certificate: the Z[φ] witness

Status: THE / CERT-CLOSED.

The promotion of `xi5` from tuned correction to owned defect is machine-closed by the finite ξ5 torus-defect certificate — exact arithmetic in `Z[phi]` (elements `a + b*phi` with `phi^2 = phi + 1`), zero floats:

```text
(i)   phi^5 = 11 + phi^-5  exactly:   3 + 5*phi = 11 + (-8 + 5*phi)
      since phi^5 = 3 + 5*phi  and  phi^-5 = -8 + 5*phi
(ii)  L_5 = phi^5 + psi^5 = 11 = |V_11|   (psi = 1 - phi; Galois trace lands on the torus address)
      => xi5 = phi^5 - L_5 = -psi^5 = phi^-5
(iii) Tr(T^5) = -11  for T = [[0,1],[1,-1]]  (chi_T = x^2 + x - 1)
      the fifth time-return sits exactly on the torus address
```

The witness `3 + 5*phi = 11 + (-8 + 5*phi)` is the entire content of "`xi5` is the torus-address defect" reduced to integer bookkeeping in `Z[phi]`. The cert carries the §16.3 status boundary forward unchanged: it closes (i)–(iii) at THE, and explicitly leaves `Delta_alpha` at CHK.

### 06.37.3 Trace-heat time ladder

The same fixed time matrix controls the trace-heat ordered finite evolution:

```text
T = [[0,1],[1,-1]]          chi_T = x^2 + x - 1
Tr(T^n) = (-1)^n L_n
Delta_T = T^2
Tr((Delta_T)^m) = Tr(T^(2m)) = L_(2m)
```

Thus heat moments of `T^2` are even Lucas traces. A fixed detector reads `T^n` layers while the detector itself is unchanged; the changing object is the finite time-ladder state, not a retuned observer.

The odd-`n` traces are the time-side image of the address split above: `Tr(T^5) = -L_5 = -11` is exactly the integer address `11` of the torus, sat on by the fifth time-return, with `xi5 = phi^-5` the residual excess the integer trace discards. The carrier (φ⁵ torus / quasicrystal) and time (toral automorphism `T`) are one object read two ways — geometrically as the address `phi^5 = 11 + xi5`, dynamically as the time-return `Tr(T^5) = -11`. [^b06-48]
## 06.39 Phason flips and finite rewrite inertia

The ordered finite evolution transport layer now has an operator-origin reading inside the
φ-quasicrystalline support.  Runtime transport through aperiodic support — i.e. ordered finite-evolution transport over the support
requires phason flips under acceleration; inertia is the finite rewrite cost of
maintaining admissible support.

The finite owner is `D0.Physics.PhasonFlipInertia`:

```text
PhasonFlipCount
InertialCost
phason_flip_drag_positive_cost
```

The finite phason-flip-inertia certificate checks that uniform admissible
phase transport has the minimal flip count, acceleration increases
window-crossing events, and the excess flip count is a scale-free rewrite cost
before any SI calibration.

## 06.40 Time as completed trace production

Time is the ordered index of stable trace production. A clock tick is the completed \(\Omega_8\to V_9\) detector closure. For \(p=\varphi^{-1}\), the retained/archive recursion is

\[
A_{t+1}=pA_t,
\qquad
B_{t+1}=B_t+p^2A_t.
\]

Therefore

\[
A_t=p^tA_0,
\qquad
B_t=(1-p^t)A_0
\]

when \(B_0=0\). The retained component never vanishes in finite time. The continuum parameter is the logarithmic coordinate of this self-similar trace ladder.

### The tick fraction is inherited, not postulated

The retained fraction \(p=\varphi^{-1}\) is **not** a free parameter of the time layer. It is forced by the Book 01 detector asymmetry: the positive self-return condition \(p+p^2=1\) has the unique admissible root \(p=\varphi^{-1}\), so the per-tick decay law \(A_{t+1}=\varphi^{-1}A_t\) is the temporal image of that primitive. The tick envelope is inherited from the primitive detector, not declared here. Status: FORCED (owner BOOK_01 — \(p+p^2=1\), \(\varphi\)-from-detector; cited, not re-derived). [^b06-49]

Equivalently the per-tick archive increment is \(B_{t+1}=B_t+(1-\varphi^{-1})A_t=B_t+\varphi^{-2}A_t\), which is why the increment coefficient above is exactly \(p^2=\varphi^{-2}\): the two retained-asymmetry channels of \(p+p^2=1\) are the retained share \(p\) and the archived share \(p^2\). Nothing in the time layer is tuned.

### Relative archive ratio and archive acceleration

Define the relative archive ratio after \(t\) ticks,

\[
R_t=\frac{B_t}{A_t}=\frac{(1-\varphi^{-t})A_0}{\varphi^{-t}A_0}=\varphi^{t}-1 .
\]

In a continuum envelope parameter \(s\) (the logarithmic tick coordinate) this is \(A(s)=A_0e^{-s\log\varphi}\), \(R(s)=e^{s\log\varphi}-1\), so

\[
R''(s)=(\log\varphi)^2\,e^{s\log\varphi}>0 .
\]

The active component decays exponentially in finite tick depth; the *relative* archive ratio **accelerates**, because its denominator is the shrinking retained component, not because anything is added externally. This strictly positive second derivative is the time-layer origin of the internal cosmological mechanism that Book 08 carries to the continuum — Book 08 inherits this convexity, it does not re-postulate an acceleration. Status: FORCED (convexity is algebraic in \(\varphi\)); the archive-measure convex-order domination underpinning the Book 08 transfer is discharged by the finite convex-order-domination certificate.

### Why the time layer is two-dimensional (toral, forced)

The clock is not a scalar parameter; it is the modular flow of the **toral time operator**

\[
T=\begin{pmatrix}0&1\\1&-1\end{pmatrix},
\qquad
\chi_T(\lambda)=\lambda^2+\lambda-1,
\qquad
\operatorname{spec}(T)=\{\varphi^{-1},-\varphi\},
\qquad
\det T=-1 .
\]

This is forced, not chosen. The minimal M1-admissible field is \(\mathbb{Q}(\varphi)\), of degree 2 over \(\mathbb{Q}\): the self-return law \(p+p^2=1\) is **quadratic**, and a degree-1 (rational) field would be external rational capture, which contradicts M1. Hence

\[
\dim(\text{time layer})=\deg\big(\text{minimal M1-field}\big)=\deg\mathbb{Q}(\varphi)=2,
\]

so the time layer is \(T\) acting on the 2-torus and the first orientation-preserving return is the squared operator \(T^2\). Status: FORCED (degree of the minimal M1-field), discharged by the finite 2D-Pisot time certificate. [^b06-50]

**Feature, not bug — smooth symbolic dynamics.** In degree 2, \(\varphi\) is Pisot: its Galois conjugate \(\psi\) satisfies \(|\psi|=\varphi^{-1}=0.618<1\). Pisot spectrum is exactly the condition for a **smooth Adler–Weiss Markov partition** of the toral automorphism, so the symbolic dynamics of the clock is perfect (no boundary pathology). *cite:* Adler–Weiss, PNAS 57 (1967) 1573. Status: FORCED (Pisot \(\Rightarrow\) Adler–Weiss). [^b06-51]

**Scope guard.** The statement "golden \(=\) last torus" (Greene/MacKay KAM) is a **2D-only** fact. In 3-frequency systems the last torus is spiral-mean (\(\sigma^3=\sigma+1\)), not \(\varphi\). D0 keeps time strictly 2-dimensional; \(\varphi\)-universality is **not** to be extended into higher-dimensional time. Any non-smoothness (Bowen / Kenyon–Vershik) in \(n\ge 3\) would concern a multidimensional *time*, which D0 does not build — extending it would be the bug. Status: SCOPE-GUARD (do-not-extend).

### Toral arithmetic of the clock (signed Lucas, det-square)

The trace law of the clock is the **signed Lucas** sequence,

\[
\operatorname{Tr}(T^n)=(-1)^n L_n
\qquad(\text{verified } n=1{,}\dots{,}10),
\]

the Galois-balanced trace with sign. One time step reverses orientation, \(\det T=-1=\varphi\psi\) (Viète invariant \(B\)); two steps restore it, \(\det T^2=+1\) with \(\operatorname{spec}(T^2)=\{\varphi^{-2},\varphi^2\}\) and even Lucas traces — the orientation-preserving square advance \(t\mapsto t+2\). The Kolmogorov–Sinai entropy of the clock is fixed by the dominant eigenvalue,

\[
h_{\mathrm{KS}}=\log|\lambda_{\max}|=\log\varphi .
\]

Status: FORCED / certified by the finite toral-automorphism Galois-balance certificate; the address defect \(\xi_5=\varphi^{-5}\) of this torus is separately discharged by the finite ξ5 torus-defect certificate. [^b06-52] The entropy comb \(I_f=\log\varphi=h_{\mathrm{KS}}(T)\) is the owner of the Book 09 GW passport target; that ownership is recorded there, not re-derived here.

### Apparent running of constants is a finite-resolution projection artefact

A standing puzzle: D0's structural constants are topologically fixed (e.g. the K(9,11,13) interzonal channel count \(N_{\text{paths}}=359\)), yet observed couplings appear to "run" with energy. The resolution is that running is an **artefact of finite observer resolution**, not new physics:

1. The true constant lives at the \(k=\infty\) level and is fixed by topology.
2. A finite observer sits at level \(k\) and sees the projection \(\pi(G)\) of the graph, not the clean graph.
3. Under projection some channels **merge** and some cycles average out.
4. This changes only the *effective* channel count \(N_{\mathrm{eff}}(k)\) — the visible graph complexity at resolution \(k\).

Hence the apparent flow is

\[
g(k)=g_0\,\big(1+O(\varphi^{-k})\big),
\]

where the \(O(\varphi^{-k})\) coefficients are computed from the projection/spectral statistics at level \(k\) — **with no new constants introduced**. The \(\varphi^{-k}\) suppression is the same self-similar tick ladder that drives \(A_t=\varphi^{-t}A_0\): running and forgetting are one mechanism viewed at one resolution. Status: FORCED (running \(=\) projection statistics, not external \(\beta\)-functions); the projected effective Laplacian renormalizes exactly under the canonical phase projection \(x\mapsto x\bmod(n{+}2)\), discharged by the finite Laplacian RG-flow certificate. The QFT \(\beta\)-function scheme passports for SM-comparison remain strict passport work under their own certificate. [^b06-53]

----

## D0_v16 Dusty-plasma active-medium bridge

Status: `LAB-BRIDGE / TABLETOP-PASSPORT-SEED`.

Electron-beam dusty-plasma experiments are admitted as an external bridge for the Book 06 claim that a finite readout medium is active rather than passive. In the bridge dictionary, the electron beam is a directed readout, dust grains are archive-capacity sinks, and the measured plasma channel is co-produced by beam propagation and archive loading. The laboratory fact that dust loading changes beam deposition, density profiles, and plasma-cloud geometry supports the finite-readout principle at the level of an external analogue.

This bridge does not close a core theorem. In particular, the golden mass-loss and acoustic log-φ proposals remain external experimental targets, not Book 06 proofs.


## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b06-1]: open obligation — cert obligation open
[^b06-2]: open obligation — cert obligation open
[^b06-3]: forcing: GOLDEN THE II.1.1, BRIDGE II.1.2
[^b06-4]: forcing: GOLDEN DEF II.1.3, THE II.1.4, COR II.1.4.A
[^b06-5]: forcing: GOLDEN REM II.1.10, COR II.1.11, DEF II.1.12, LEM II.1.13
[^b06-6]: forcing: GOLDEN THE 3.2.A, BOOK-I-ARCHITECTURE
[^b06-7]: forcing: GOLDEN COR 3.2.A.1, BOOK-I-ARCHITECTURE
[^b06-8]: open obligation — cert obligation open
[^b06-9]: open obligation — cert obligation open
[^b06-10]: forcing: GOLDEN THE 6.1.2, BOOK-III-SPECTRUM; ⊥-proof
[^b06-11]: forcing: GOLDEN DEF 54.2 / THE 54.1, BOOK-VI-EXTENSIONS
[^b06-12]: forcing: GOLDEN REM 54.3/54.4, BOOK-VI-EXTENSIONS
[^b06-13]: open obligation — cert obligation open
[^b06-14]: open obligation — cert obligation open
[^b06-15]: forcing: GOLDEN BOOK-VI-EXTENSIONS THE 77.1 + COR 77.2
[^b06-16]: forcing: GOLDEN BOOK-VI-EXTENSIONS COR 77.2
[^b06-17]: forcing: BOOK-00-ENTRY-CONTRACT-AND-ADMISSIBILITY 00.2A
[^b06-18]: open obligation — cert obligation open — the existing cert checks the magnitude, not the `det = B` identity
[^b06-19]: open obligation — cert obligation open
[^b06-20]: open obligation — cert obligation open — the existing toral cert checks `det`/trace, not the KS-entropy identity
[^b06-21]: open obligation — cert obligation open
[^b06-22]: forcing: D0-CKM-INTERFACE-ITERATION-REPORT §32, verified n=1..10
[^b06-23]: forcing: BOOK_06 §06.2/§06.8a; GOLDEN REM 51.6, BOOK-VI-EXTENSIONS
[^b06-24]: forcing: D0-CKM-INTERFACE-ITERATION-REPORT §33
[^b06-25]: forcing: BOOK_06 Theorem 06.2E
[^b06-26]: forcing: GOLDEN LEM II.3.APPX8.4.2, BOOK-II-MECHANISM
[^b06-27]: forcing: GOLDEN LEM II.3.APPX8.4.2, BOOK-II-MECHANISM
[^b06-28]: forcing: GOLDEN THE II.3.APPX8.5.2, BOOK-II-MECHANISM
[^b06-29]: forcing: GOLDEN CHK II.3.APPX8.5.2A, BOOK-II-MECHANISM
[^b06-30]: forcing: GOLDEN LEM II.2.LEG18.0.2
[^b06-31]: forcing: GOLDEN DEF II.2.LEG18.1.1 + LEM II.2.LEG18.1.1.A
[^b06-32]: forcing: GOLDEN THE II.2.LEG18.1.1.D
[^b06-33]: forcing: GOLDEN COR II.2.LEG18.1.1.E
[^b06-34]: forcing: GOLDEN REM 11.dS.A; numerical differentiation of $\log P$ is prohibited so the dimension is read off the spectrum directly
[^b06-35]: forcing: GOLDEN THE II.2.LEG18.1.2 + VER II.2.LEG18.1.3
[^b06-36]: forcing: D0-RESEARCH-ADDENDUM-cosmology-sterile-2D §A; cert `05_CERTS/vp_time_2d_pisot.py`, `PASS_TIME_2D_PISOT`
[^b06-37]: forcing: D0-RESEARCH-ADDENDUM §A, Adler–Weiss/Pisot smoothness
[^b06-38]: forcing: D0-RESEARCH-ADDENDUM §A; certs `05_CERTS/vp_signature_31_split.py`, `PASS_SIGNATURE_31_SPLIT`, and `05_CERTS/vp_galois_lorentz_signature.py`
[^b06-39]: open obligation — cert obligation open
[^b06-40]: forcing: GOLDEN THE 61.10
[^b06-41]: forcing: GOLDEN THE 61.10
[^b06-42]: open obligation — cert obligation open
[^b06-43]: forcing: D0-SIGNATURE-31-SPLIT-001
[^b06-44]: forcing: D0-SIGNATURE-31-SPLIT-001; time-as-T^2 minimality: D0-TIME-2D-PISOT-001
[^b06-45]: forcing: GOLDEN BOOK_06 06.36A/06.36B Discrete Lorentz Factor, Finite Holographic Self-Reading Principle
[^b06-46]: forcing: GOLDEN THE 36, 40
[^b06-47]: forcing: GOLDEN THE 36; cite BOOK_02 02.13.4 for the α-form ownership, BOOK_01 for the `359/phi^2` capacity term.
[^b06-48]: forcing: GOLDEN THE 40.
[^b06-49]: forcing: GOLDEN THE 1.x via v17 BOOK_06 §06.6.
[^b06-50]: forcing: GOLDEN THE — D0-TIME-2D-PISOT-001, dossier §VI.1.
[^b06-51]: forcing: GOLDEN dossier §VI.1.
[^b06-52]: forcing: GOLDEN THE — D0-TORAL-AUTOMORPHISM-GALOIS-BALANCE-001, dossier §III.1.
[^b06-53]: forcing: GOLDEN THE 9.5.1 "RG as illusion", BOOK-III-SPECTRUM §III.1.H.
