# D0 — Exact Results

Every statement below is exact: hypotheses inside the statement, conclusion precise, owner
named. Owners are registry rows (Lean or certificate); a book-section citation (§) marks a
derivation leg whose owner is prose, stated as such in place. Axioms are `propext, Classical.choice, Quot.sound` unless a
statement says otherwise. Nothing here is hedged, because the boundary of each result is
part of its statement. Open problems are collected at the end as named targets, not as
qualifications of the theorems.

Verification: `cd 09_LEAN_FORMALIZATION && lake build D0.All` (green, 0 `sorry`,
4478 jobs) · registry `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (637 claims) ·
gate `tools/` (validate, sync, value ledger, certificates, score — all green).

---

## 1. Quantum mechanics from minimum description length

**T1 (Linearity).** For a mediator subject to M1 (no mandatory external catalogue): its
arity is 2; every interaction term requires a coupling constant, i.e. a catalogue; every
truncation of the resulting series requires a scale catalogue. The unique catalogue-free
evolution has no interaction term — superposition is linear. Lean owns the symplectic-form
leg (`D0-BRANCH-SYMPLECTIC-FORCING-001`); the arity/catalogue derivation's owner is prose,
BOOK_01 §01.6.0.

**T2 (Born rule, including dim 2).** A phase-blind response invariant under the quarter-turn
`J(x,y) = (−y,x)` is proportional to `x² + y²`, and this is the unique such quadratic form.
The hypothesis is J-invariance, not area-preservation: the shear is area-preserving and does
not fix `x² + y²` (machine-checked counterexample,
`D0-BORN-AREA-PRESERVATION-INSUFFICIENT-NOGO-001`). This covers dimension 2, where Gleason's
theorem does not apply. `D0-SYMPLECTIC-GLEASON-001`, `D0-BORN-QUADRATIC-ORIGIN-001`.

**T3 (Role algebra classification).** A role group in which recording *which* conjugate copy
would constitute a catalogue has all subgroups normal; order memory forbids abelian; hence
the group is Hamiltonian, and by Baer's classification every Hamiltonian group is
`Q₈ × B × D` (Baer 1933: external-cited; the Dedekind-minimality-at-order-≤ 8 leg is
kernel-checked). `Q₈` is a forced factor. `D0-Q8-DEDEKIND-MINIMALITY-001`, BOOK_02 §02.18.1.

**T4 (M1's derivability clause is functorial).** The derivability clause (clause 1) of the
exogenous-parameter test transports and reflects along faithful interpretations, with
kernel-checked countermodels showing each direction load-bearing; per-instantiation
preservation is not claimed. The predicate itself and the catalogue reductio are owned
separately. `D0-M1-UNIVERSALITY-001`, `D0-M1-PREDICATE-001`.

**T5 (Arrow of time).** φ expands and its Galois conjugate contracts (`|ψ| < 1`) — the
irreversible direction; both are algebraic integers and φ is Pisot (Lean,
`D0-PISOT-CONTRACTION-TIME-ARROW-001`). The monotonicity of `I(t) = −log P(t)` via heat-trace
decay and the Markov-partition-iff-Pisot reading are owned by prose §06.30a, with the Markov
machinery bridge-graded (`ASSUMP-ADLER-WEISS`).

**T25 (Information connectivity — added 2026-08-14).** Under minimal record semantics
(record relation `Rec`, connectivity = its equivalence closure, contents in `V` with
`Nontrivial V`, admissibility = records copy content faithfully), for an observer at `b`
with observation `obs`: (i) every record-connected domain's value is `M1Forced` with `obs`
as the unique witness — this leg is axiom-free; (ii) for every record-disconnected domain,
EVERY candidate value satisfies `RequiresExternalCatalogue`, by explicit
piecewise-admissible witnesses (load-bearing exactly at `v = obs`: not even the observed
value transfers); (iii) corollary: two record-disconnected observers can force agreement on
no domain. A record-disconnected information domain and an external catalogue are the same
thing. The constraint family is a universal (semantic) constraint, not a finite selector;
carrier: abstract description domains, not the scene graph; applying the license to real
substrates requires identifying `Rec` (bridge step, not discharged).
`D0-INFORMATION-CONNECTIVITY-001`.

## 2. The scene and its geometry

**T6 (Signature).** The equitable quotient of any 3-zone complete multipartite graph has
characteristic polynomial `λ³ − e₂λ − 2e₃`; zero trace and `e₃ > 0` force exactly one
positive and two negative eigenvalues — signature (1,2). Space rank 3 is proved on the literal 33×33 adjacency
matrix (`D0-SIGNATURE-31-SPLIT-001`); the signature lives on the 3×3 equitable quotient; the
generic statement and the converse (the two negative eigenvalues coincide iff the zones are
equal) are owned at `D0-TRIPARTITE-SIGNATURE-GENERAL-001` — the repaired second route to
(1,2). Also `D0-RANK3-METRIC-TRANSPORT-001`, `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001`.

**T7 (Cubic coefficients are the scene).** For K(9,11,13): `e₂ = 359 = |E|`
(`pairwise_is_edgecount`) and `2e₃ = 2574 = 2·9·11·13`. The transport cubic
`λ³ − 359λ − 2574` has positive discriminant `6185264` — three distinct real eigenvalues.

**T8 (Inverse spectral rigidity).** For positive complete tripartite scenes, equality of
`(D, H, M₂)` forces equality of the unordered zone triple; each datum is load-bearing
(counterexamples exhibited for every dropped hypothesis); labels are not recoverable.
`D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001`.

**T9 (Zone count from the multiplicative pair).** `(D,H) = (1287, 960)` has the unique
preimage `(9,11,13)` over all part counts; the additive pair `(V,H)` does not force the
count (witnesses `[3,5,9,16]`, `[2,2,4,5,9,11]`). The over-all-part-counts uniqueness is
carried at assembly grade over the tabulated 11-item factorisation list (exhaustiveness via
`Ω(1287) = 4`, taken as read); the forcing steps and the length bound are Lean.
`D0-ZONE-COUNT-MULTIPLICATIVE-001`.

**T10 (Dark/visible split).** `ker A = std₉ ⊕ std₁₁ ⊕ std₁₃` (blocks 8/10/12); the archive
carries no Aut-invariant vector: the visible/dark division is the invariant/invariant-free
split. Per zone the split is 1 visible + (nᵢ−1) dark, uniquely.
`D0-SCENE-DARK-ARCHIVE-STRUCTURE-001`, `D0-ZONE-IS-GENERATION-001`.

**T11 (Joint commutant).** Centralising both Aut and the adjacency leaves dimension 6 = 3+3
at assembly grade: Lean carries the characteristic polynomial, the 48-divisor no-root sweep
and the count arithmetic; the centraliser-of-Q and isotypic-split steps are standard linear
algebra at docstring grade. `D0-SCENE-JOINT-COMMUTANT-SIX-001`.

**T12 (Heat/zeta layer).** `ζ_L(0) = 32`, `ζ_L(−1) = 718 = 2|E|`, `ζ_L(−2) = 16426`,
`ζ_L(1) = 239/165`; the discrete Einstein–Hilbert action proxy equals `359 = |E|`
(off-diagonal −1 squares are edge indicators). `D0-SCENE-HEAT-KERNEL-001`,
`D0-SCENE-SPECTRAL-ACTION-001`.

**T13 (One invariant, five sectors).** The edge count `359 = e₂(9,11,13)`, owned once at
`D0-SCENE-001`, is the identical object consumed by: the EH action proxy (T12), the α
leading term (`ζ_E(0) = 359`, T17), the metric cubic (T7), the Yukawa non-degeneracy on
that cubic (T15), and the S_DE window product `λ_cλ_r = 359/160` (normalized-Laplacian
eigenvalue product, `D0-SCENE-ACTIVE-EIGENVALUES-001`). Certificate control: on K(9,11,15)
every structural face moves to `e₂ = 399` together (the α face is exempt from this lockstep —
no owned rival-scene formula exists). The two carriers `160x²−480x+359` and
`x³−359x−2574` admit no nonzero intertwiner (integral Bézout certificate `39590739579959`,
reproduced independently by a Sylvester resultant). `D0-EDGE-INVARIANT-CROSS-SECTOR-001`,
`D0-SDE-CUBIC-SPECTRAL-DISJOINTNESS-001`.

## 3. Golden arithmetic and toral dynamics

**T14 (Return-defect calculus).** With `L` the Lucas sequence and `T = [[0,1],[1,−1]]`:
`Tr(Tⁿ) = (−1)ⁿLₙ` for all n; `(φ⁻¹)ⁿ = (−1)ⁿ(Lₙ − φⁿ)` for all n; in particular
`ξ₅ = φ⁻⁵ = φ⁵ − 11` and `φ⁻¹² = 322 − φ¹² = L₁₂ − φ¹²`. The composition law
`L_{m+n} = L_m·L_n − (−1)ⁿ·L_{m−n}` holds for all `n ≤ m` and transports to traces:
`Tr(T^{m+n}) = Tr(T^m)Tr(T^n) − (det T)ⁿTr(T^{m−n})`. At `(m,n) = (12,5)`:
`Tr(T¹⁷) = −3571`, `L₁₇ = L₁₂L₅ + L₇ = 322·11 + 29`, the `+L₇` correction forced by
`det T⁵ = −1`; and `φ⁻¹⁷ = (φ⁵−11)(322−φ¹²)`. `D0-TORAL-COMPOSITION-SEVENTEEN-001`,
`D0-LUCAS-DEFECT-SIGN-001`, `D0-LEFSCHETZ-ZONE-EXCLUSION-001`.

**T15 (Yukawa rigidity on the transport cubic).** The cubic `x³−359x−2574` splits with
three distinct real roots located in `(−13,−12)`, `(−10,−9)`, `(21,22)`; no non-scalar
member of the commutant attains a rational value at any root — rational Yukawa targets are
unattainable exactly. `D0-YUKAWA-COMMUTANT-SPECTRUM-001`.

**T16 (Lefschetz addresses).** `det(Tⁿ ± 1) = (−1)ⁿ ± (−1)ⁿLₙ + 1` for all n; the zone size
13 lies outside both owned toral address families, while `13 = F(3) + F(4)` is the unique
two-term Fibonacci sum at value level. `D0-LEFSCHETZ-ZONE-EXCLUSION-001`.

## 4. The α line

**T17 (Leading term).** `ζ_E(0) = 359` and `ζ_E(−1) = 359φ⁻² − φ⁻⁵ = α_top⁻¹`
(`zetaEdge_zero`, `zetaEdge_neg_one`; exact in ℤ[φ]: the pair `(726, −364)`).
Sweep fact (certificate `vp_alpha_leading_term_sweep.py`, reproduction 2026-08-10): within
`4·10⁻⁴` of `α⁻¹` the family `N·φᵖ + m·φᵠ` (`N ≤ 500`, `|m| ≤ 12`, `|p|,|q| ≤ 20`) contains
THREE distinct values; the D0 term is among them and both rivals lie numerically closer —
the pre-refactor "exactly one value" uniqueness claim is retired as an error of record. The
`~3.7·10⁻⁴` residual is closed by the registered dressing (T18). `D0-EDGE-ALPHA-001`.

**T18 (Dressing form, machine-checked legs).** In
`α⁻¹ = α_top⁻¹ + φ⁻¹⁷(1 + h_KS·sin θ_seam)`: the angle `θ_seam = 12/5` is exact in ℚ(φ)
(`D0-PI0-DISCRETE-ANGLE-001`); the channel is `sin`, forced by `Q₈`, `G² = −I`
(`D0-Q8-SIN-CHANNEL-001`); the seam factor is `ξ₅ = φ⁻⁵` (T14); the linear form is the
parabolic transport `N² = 0` (`D0-ALPHA-HOLONOMY-LINEAR-FORM-001`); seven registered rival
dressings are separated by ≥ 1.6·10⁻⁵. Under hypotheses (α) 12-sector uniformity, (β)
count/product reading, (γ) the total `φ⁻¹⁷ = ξ₅·φ⁻¹²`, the equivariance norm applied to
weights-as-moduli (normative, not derived), and positivity, the per-crossing weight is
exactly `φ⁻¹` and it is the unique positive real 12th root
(`D0-SEAM-CROSSING-WEIGHT-001`).
The 9-digit agreement with CODATA is a registered consequence check
(`D0-ALPHA-HOLONOMY-002`).

**T19 (No spectral origin for φ — full closure).** For the transport cubic
`x³−359x−2574`: no element of quadratic minimal-polynomial degree lies in `ℚ(λ)` for any
single root (degree 3 is prime, `D0-TRANSPORT-FIELD-NO-GOLDEN-001`); and `√5 ∉ K` for the
full splitting field `K = ℚ(λ₁,λ₂,λ₃)` — the discriminant `6185264 = 2⁴·193·2003` is not a
square (mod 9) and `5·6185264` is not a square (mod 7), so `Gal(K/ℚ) = S₃` and the unique
quadratic subfield `ℚ(√Δ) ≠ ℚ(√5)`. Hence no rational-coefficient rational function of all
three transport eigenvalues jointly produces any golden quantity — the class is exhausted by
construction. Positive control: `Δ·386579 = 1546316²` — the same machinery confirms the
field's own kernel. `D0-TRANSPORT-SPLITTING-FIELD-NOGO-001` (S₃ classification step:
Dummit–Foote §14.6–7, hypotheses machine-checked).

**T20 (Origin dichotomy).** Combining T14 and T19: within the exhausted
rational-coefficient spectral class, the φ-power content of the registered total has no
transport-spectral origin; the toral return system is its only owned positive origin —
both factors of `φ⁻¹⁷ = ξ₅·φ⁻¹²` are return defects of one toral automorphism, at returns
5 and 12. Proving rows: `D0-TRANSPORT-SPLITTING-FIELD-NOGO-001`,
`D0-TORAL-COMPOSITION-SEVENTEEN-001`; registered at `D0-ALPHA-SEAM-FORM-FORCED-001`.

## 5. The cascade (the central thesis, carried part)

**T21 (Floors).** Seven insufficiency floors are carried in the registered `CascadeStep`
shape, each with a proved insufficiency and a satisfiable control: comparison (a monopoly
acceptor is constant), one-loop (one ℤ register cannot recover operation history),
order-memory (`π₁(T²) = ℤ×ℤ` is abelian; `S₃`, `Q₈` encode order), defect-closure (the
commutator defect survives the basepoint move only as a conjugacy class — a closed-loop
datum), shell-closure (the interior pair `{R−r, R}` is not closed under the radial
reflection `x ↦ 2R−x`; the triple `{R−r, R, R+r}` is; the equation `x = 1 + 1/x` has the
unique positive solution φ — that this equation IS the shell's scaling is owned by prose
§03.23.5), scale (every rational is captured; φ is not),
orientation-parity (`OrientationClosed k ↔ Even k`). Rows
`D0-CASCADE-FLOOR-*-001`, `D0-CASCADE-CHAIN-SCAFFOLD-001`.

**T22 (Interlock links).** Four links of the form *the repair of floor n is the failing
carrier of floor n+1*: `ℤ×ℤ` fixes one-loop and fails order-memory; the non-commutative
repair realizes only rational (captured) scale ratios; the order repair's defect fails
element-level invariance and forces the class reading; the interior two layers force the
outer shell, whose scale is the scale floor's own survivor φ (this fourth link is
PROSE-ANCHORED on §03.23.5's own two-layer identification — unlike links 1–3 it shares no
formal object with the preceding floor).
`D0-CASCADE-INTERLOCK-SCALE-001`, `D0-CASCADE-FLOOR-DEFECT-CLOSURE-001`,
`D0-CASCADE-FLOOR-SHELL-CLOSURE-001`.

**T23 (Terminal count).** The interior pair has exactly 2 elements; any reflection-closed
superset contains the outer radius; the least reflection-closed completion is exactly the
three-shell set, cardinality 3 — no hypothesis of shape `3 ≤ _` occurs. The three-element
carrier is the owned zone carrier (`Fintype.card TorusShell = 3`, zone sizes 9/11/13).
This is the first derivation of the count three from the closure structure itself; the
three previously recorded dead routes (propositional, pair-indexed, sort-indexed) are on
different carriers and stand. `D0-CASCADE-TERMINAL-COUNT-001`.

**T24 (Assembly).** All of T21–T23 composes into one theorem with clean axioms:
`cascade_carried_assembly`. `D0-CASCADE-CARRIED-ASSEMBLY-001`.

**T26 (Proofreading floor — added 2026-08-14, the first structural import of the
cross-substrate program).** For every discrimination limit `0 < δ < 1`: a single
equilibrium test (wrong/right acceptance ratio bounded by one Boltzmann factor — the
carrier's defining hypothesis, inside the statement) provably cannot reach the proofread
error level `errOf (δ²)`; two tests separated by an irreversible reset (ratios composing
multiplicatively — the reset assumption is ENCODED in the carrier definition, not proved)
reach it exactly; the pair is a genuine `CascadeStep`. The error targets `errOf (δⁿ)`
descend strictly at every depth (levels only — the n-stage carrier family is not
constructed). External anchor: kinetic proofreading (Hopfield 1974, Ninio 1975), cited as
the physical reading of the carrier definitions, not load-bearing in any Lean statement.
Adjacency into the chain is open; no biochemical claim is registered; the frozen R-A2
passport record (committed before the mint) grades any real stage beating its equilibrium
bound as internally multi-test. `D0-CASCADE-FLOOR-PROOFREADING-001`.

## 6. No-go theorems (exact negative results)

**N1.** The scene cannot be reconstructed from transport data: the cubic omits V; two
isospectral pairs are exhibited. `D0-TRANSPORT-SPECTRUM-BLINDNESS-NOGO-001`.

**N2.** No transport eigenvalue lies in ℚ(√5). `D0-TRANSPORT-NOT-GOLDEN-001`; subsumed at
field grade by T19.

**N3.** Every Aut-equivariant operator on the 33-scene is block-diagonal across
active/archive; Feshbach couplings vanish; within the equivariant class the Dixmier
extraction must be external. `D0-EQUIVARIANT-SEAM-NOGO-001`.

**N4.** Equivariant hypercharge carriers: vertex ≤ 3 and symmetric-edge ≤ 3 (both < 5);
directed-edge ≤ 6, and the 6-field convention saturates — the audited carrier classes are
{vertex, symmetric edge, directed edge}. `D0-EQUIVARIANT-HYPERCHARGE-CARRIER-001`.

**N5.** ΛCDM is excluded in the ratio reading by the degeneracies alone: `w = −1` requires
`s = 15`, which is not a subset sum of {8,10,12}. `D0-DARK-EOS-DISCRETE-SET-001`
(unconditional leg).

**N6.** All 25 computed D0 gap-label plateaux lie in Bellissard's module `ℤ + ℤ/φ`, the
module of ANY Fibonacci hull (bridge: `ASSUMP-BELLISSARD-GAP-LABEL`) — a gap-label
measurement agreeing with them cannot discriminate D0. Revival condition: derive a forced
gap-opening subset. `D0-GAP-LABEL-GENERICITY-NOGO-001`.

**N7.** The propositional route to a three-way count caps at two; the pair-indexed zone
typing is uninhabitable; the sort-indexed route's hypothesis is its conclusion. Three exact
dead ends, each with its own carrier (modules under `D0.Foundation`, registered in the
umbrella row).

---

## Open problems (named targets, not qualifications)

**P1 (Second route).** Exhibit a forcing route to φ whose premises are disjoint from
`D0ResponseRoot x := 0 < x ∧ x + x² = 1`. The route audit found 0 of 20 sampled multiplicity
claims independent; two repaired pairs now exist (Hurwitz-class canonization + Jones slot for
φ; the generic tripartite signature route for (1,2)) — proving one more independent route to
any remaining high-load object is the highest-value theorem available.

**P2 (γ).** Derive the total `φ⁻¹⁷ = ξ₅·φ⁻¹²` as a seam statement. Sharpest form after T20:
identify the seam transport with the twelfth toral return. Door 1 (`dim g_light`) is the
live rival and requires an owner decision on the "electroweak" label.

**P3 (Cascade completion).** The each-floor-forced statement over the full prose chain; the
topological (2-cell attachment) reading of shell closure; the typed count seam
(`CascadeCountInterpretation` — a semantic classification theorem, not an instance).

**P4 (Discriminating experiment).** No multi-point discriminating confirmation exists.
Pre-registered candidates: the two-tone SBSL golden-drive protocol (P-SBSL-1, frozen before
data contact), the Keller–Miksis discretization window (width ≤ 2·10⁻³), `w = 3/5 − φ`
against future DESI releases. Current survivors are single-number matches
(`sin²θ_W` 0.23σ, `m_s/m_d = 20` 0.02σ); the SPARC phason-halo kernel is rejected in ~91%
of galaxies (recorded negative); the PMNS δ₀ family and the LIGO φ⁻¹ defect are recorded as
non-discriminating.

**P5 (Attack queue).** The computed work queue (6 items) is
[D0_VALUE_RANKED.md](03_THEORY_MAP/D0_VALUE_RANKED.md); top: `D0-P-INVARIANT-MINIMAL-001`
(60.1), the cascade umbrella (59.5).
