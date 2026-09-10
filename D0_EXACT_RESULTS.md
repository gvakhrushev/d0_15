# D0 — Exact Results

Every statement below is exact: hypotheses inside the statement, conclusion precise, owner
named. Owners are registry rows (Lean or certificate); a book-section citation (§) marks a
derivation leg whose owner is prose, stated as such in place. Axioms are `propext, Classical.choice, Quot.sound` unless a
statement says otherwise. Nothing here is hedged, because the boundary of each result is
part of its statement. Open problems are collected at the end as named targets, not as
qualifications of the theorems.

Verification: `cd 09_LEAN_FORMALIZATION && lake build D0.All` (green, 0 `sorry`,
4558 jobs) · registry `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (695 claims) ·
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

**T43 / N12 (Edge `359` is not a scene selector — added 2026-08-22).** The source scene and
the ordered positive rival `(7,10,17)` have the same complete-tripartite edge count:

```text
E(9,11,13)=E(7,10,17)=359,
```

but their vertex counts are `33` and `34`, and their triangle counts are `1287` and `1190`.
Lean proves that every selector factoring only through `E` and accepting the source must accept
the rival. The deterministic certificate gives the complete classification: exactly 19 positive
ordered triples solve `ab+ac+bc=359`. The positive boundary is sharp: among ordered natural
triples, Lean proves `(V,E)=(33,359)` uniquely implies `(a,b,c)=(9,11,13)`. Therefore the
cross-sector occurrence of `359`, including the α leading form, is downstream reuse of a
scene-owned integer and cannot independently select or validate the scene.
`D0-EDGE359-SCENE-SELECTION-NOGO-001`.

**T44 (Scene invariant over-determination — added 2026-08-22).** The counterpart to T43. For the
ordered tripartite invariants `V=a+b+c`, `E=ab+ac+bc`, `T=abc`, no single count selects the
scene: `V=33` has 91 ordered solutions, `E=359` has 19, `T=1287` has 10, each exhibited with an
explicit rival. But **every pair is selective** and Lean-proved: `(V,E)`, `(V,T)` and `(E,T)`
each force `(9,11,13)` uniquely (the `(E,T)` leg via the bounds `a³ ≤ abc = 1287` and
`b² ≤ abc`). So the scene is over-determined — it is the unique common solution of any two
independent readings — and no single cherry-picked invariant is load-bearing. This is internal
consistency and rigidity of the counts; deriving the counts themselves from M1 remains the
upstream cascade frontier. `D0-SCENE-INVARIANT-OVERDETERMINATION-001`.

**T45 / N13 (Detector capability count is exactly the GAP-E scene bound — added 2026-08-22).**
Let `n` be the number of independent primitive detector capabilities and admit port-power
extensions `2^k`, `1≤k≤n`. Lean proves the exact equivalence

```text
(∀k≤n, 9+2^k≤13)  ↔  n≤2.
```

The general comparison grammar independently proves that primitive-comparison count equals
capability count. In the current unstratified observation model, history/order is a third
operational primitive; therefore `n=3` re-admits `2³=8` and the rival zone `9+8=17`. Conversely,
the current-data quotient theorem proves that every comparison factoring through
membership/value data is history-blind. Thus the entire GAP-E upper-bound problem reduces to
one local typed obligation: every primitive M1-admissible **detector-layer** comparison factors
through current data, placing history in the memory layer. Until that theorem is proved,
`portCap=2` is not exhaustive. `D0-DETECTION-SCENE-BOUND-EQUIVALENCE-001`.

**T46 (Detector catalogue-freedom — added 2026-08-22, scope corrected 2026-08-24).**
Model a detector comparison as one that may consult an external orientation catalogue
`o : Current → Bool`. Lean proves: catalogue-free ⇔ the comparison is the lift of a bare
current-data comparison (hence order/history-blind); the order comparison
`decide (o x = o y)` is **not** catalogue-free (the constant catalogue equates two observations
the identity catalogue separates), and every catalogue-free comparison factors through current
data. This is a catalogue-independence/factorization theorem. It is **not** by itself an instance
of the repository's unique-answer `M1Forced` predicate; T47 owns that exact boundary.
`D0-DETECTOR-CATALOGUE-FREEDOM-001`.

**T47 / N14 (Catalogue-free class is not a unique M1-forced answer — added 2026-08-24).**
The canonical predicate `M1Forced Forced a` requires `a` to be the unique witness of `Forced`.
Catalogue-free detector comparisons form a class, not a singleton: constant-false and
constant-true comparisons are distinct and both catalogue-free. Lean therefore proves
`¬∃cmp, M1Forced CatalogueFreeConstraint cmp`. Order/history still satisfies the canonical
relative statement `RequiresExternalCatalogue CatalogueFreeConstraint orderComparison`, but the
load-bearing M1 reductio cannot be invoked because no forced witness exists. The missing formal
object is class-level M1 admissibility (or a finite obligation on capability kinds), not another
unique comparison selector. `D0-DETECTOR-M1-PREDICATE-BOUNDARY-001`.

**T48 (Canonical detector-layer equivalence — added 2026-08-24).** Bare current-data comparisons
are equivalent to catalogue-free comparisons. For nonempty history, they are also equivalent to
history-invariant full comparisons via `liftCurrent/descendAt`. Composing gives a canonical
equivalence between catalogue-free and history-invariant carriers. Membership and value lie
inside; history equality lies outside. This closes the detector/current/memory layer mathematics
without making an M1-forcing claim. `D0-DETECTOR-LAYER-EQUIVALENCE-001`.

**T49 (Typed detector primitive exhaustion — added 2026-08-24).** Work inside the full
three-capability ambient `(membership,value,history)`. A primitive profile is atomic; imposing
history coordinate `false` leaves exactly the membership and value atoms. Lean constructs an
explicit equivalence of this detector primitive carrier with `Fin 2`, proves cardinality exactly
two, classifies every primitive current-data comparison into one of those profiles, and retains
history as the excluded primitive control. Through T45 the typed count two proves the
port-power zone bound `≤13` on the typed detector layer. The remaining seam is only the
class-level physical/M1 representation into this layer.
`D0-TYPED-DETECTOR-PRIMITIVE-EXHAUSTION-001`.

**T50 (M1 class admissibility — added 2026-08-24).** A `CatalogueSystem` consists of candidates,
possible external catalogues and observable outputs. `M1ClassAdmissible` means a candidate's
output is invariant under every catalogue change; unlike `M1Forced`, the admissible carrier may
contain many objects. Lean proves the interfaces are compatible: every `M1Forced` constraint has
a witness carrier equivalent to `PUnit` and cardinality one, while any class with two distinct
allowed witnesses cannot be one `M1Forced` answer. M1 therefore has a rigorous two-stage form:
class-level catalogue-independence filters allowed candidates; unique forcing applies only when an
additional canonical constraint has one witness. `D0-M1-CLASS-ADMISSIBILITY-001`.

**T51 (Class-level M1 physical detector representation — added 2026-08-24).** Instantiate the
class interface on detector comparisons and orientation catalogues. Lean proves class-M1
admissibility is exactly catalogue-freedom. For any physical comparison type supplying
`PhysicalDetectorRepresentation` — comparison map, admissibility iff class invariance, and
injectivity on admissible objects — every admissible object embeds into the catalogue-free and
history-invariant detector carriers, descends to a concrete current-data comparison, and every
primitive image has membership-only or value-only capability profile. The canonical detector
system itself is a non-singleton instance. This closes the requested formal representation seam;
a concrete external formalism must only instantiate the explicit interface fields.
`D0-DETECTOR-M1-CLASS-REPRESENTATION-001`.

**T52 (Concrete D0 physical detector representation — added 2026-08-24).** Instantiate T51 on
the actual finite `Observation(member,value,history)` comparison type. A binary comparison needs
a two-sided orientation catalogue `InputSide→Current→Bool`, independently filling history for
left/right inputs. Lean proves class-level M1 catalogue invariance iff full
`HistoryInvariant (transportComparison cmp)`, defines the concrete representation with
comparison `id`, this equivalence as `admissible_iff`, and identity injectivity, and constructs
embeddings into the M1-admissible and typed detector carriers. It proves full factorization
through current data on both inputs, primitive profile exhaustion to membership/value, and the
controls membership/value admissible versus history rejected. The certificate exhausts all
`2^16` Boolean full-comparison tables on the reduced mirror and shows one-sided catalogues miss
a same-current/different-history dependence that two-sided catalogues detect. The in-repo
application obligation is therefore closed. `D0-CONCRETE-PHYSICAL-DETECTOR-REPRESENTATION-001`.

**T53 (Verifiable theory versus unverifiable story — added 2026-09-10).** An empirical theory is
`OperationallyVerifiable` when a correct protocol represents its canonical observational
quotient; its exact complement is `UnverifiableStory`. The protocol compares persistent records
of observational states, has at least two distinguishable states and two registered verification
lines, and must return the same equality/difference truth for every catalogue value. Lean proves
the partition exhaustive and exclusive and constructs a concrete non-vacuous Boolean instance.
The states may already be observational equivalence classes: no claim is made that operational
tests recover microscopic distinctions outside the chosen empirical interface.
`D0-VERIFIABILITY-CLASS-001`.

**T54 (Verifiability forces the functional tuple and strengthens T25 — added 2026-09-10).** From
the verification contract Lean derives the three functions rather than postulating them:
distinction exists; the record map is injective; comparison separates equal from unequal records;
and two registered lines agree across all catalogue values. The retention proof is a reductio:
if two distinct states shared one record, comparing that record with itself would have to return
both `same` and `different`. On a verified carrier, record equality is therefore state equality,
and the equivalence closure of the record relation adds no spurious identifications. This is the
precise new link to T25: information connectivity remains record connectivity, while verification
forces the record itself to preserve every distinction it claims to test.
`D0-VERIFIABILITY-FORCES-FUNCTIONAL-TUPLE-001`.

**T55 (Operational MDL role minimality — added 2026-09-10).** The semantic role carrier is the
inductive three-element type `{distinction, retention, comparison}`. For an arbitrary vocabulary,
operational cost is the cardinality of the semantic image of its active names. Lean proves every
functionally complete vocabulary has that full image and cost exactly three; the canonical
vocabulary is deletion-minimal; every bijective renaming has the same image. A four-name control
duplicates `comparison`: deleting the duplicate preserves completeness, so it is not minimal.
This proves minimality of functions under equal verification capability, not a claim that an
apparatus must contain three separate hardware components.
`D0-OPERATIONAL-MDL-ROLE-MINIMALITY-001`.

**T56 (M1 is forced by public verifiability — added 2026-09-10).** For each registered verification
line, correctness fixes its output to the same checkable truth for every catalogue. Equality
through that truth proves `M1ClassAdmissible`; catalogue-independence is a conclusion, not an
extra protocol axiom. Conversely, Lean constructs a comparator that distinguishes Boolean states
when a privileged catalogue bit is `true` but fails when it is `false`: it is outcome-affecting,
not class-M1, and cannot be verifiable. Every verified line embeds into the class-M1 admissible
carrier. This is the upstream necessity theorem behind T50–T52; their physical representation and
finite detector specialization remain separate, explicit application theorems. Once such a map is
supplied, the result composes with T51, T46–T49 and T45 to send primitive verified comparisons to
the membership/value profiles and then to the port-power bound.
`D0-M1-AS-VERIFIABILITY-NECESSITY-001`.

**T57 (Regress closure and empirical factorization — added 2026-09-10).** A verified protocol's
full operational signature is injective, and its empirical quotient is equivalent to its verified
state carrier. Any empirical theory supplied with such a representation therefore embeds into its
complete catalogue/test/outcome signature layer. The capstone derives both the functional tuple
and M1 from that single verification contract, so applying M1 to the discourse does not require a
second catalogue-removal postulate. Four independent mutations remove distinction, retention,
comparison or the second registered line; each makes verification impossible. The result is a
universal property of operationally verifiable descriptions, not a theorem that every imagined
ontology has a physical realization. `D0-M1-REGRESS-CLOSURE-VIA-VERIFIABILITY-001`.

**T58 (Independent verification forces a provenance archive — added 2026-09-10).** Distinct
registered verification lines must return the same public truth. Lean therefore proves that the
map from line identity to its complete catalogue/state outcome table is non-injective: the bare
detector result necessarily forgets which independent line produced it. Adding the line as a
provenance coordinate restores injectivity. The statement is stronger for an arbitrary auxiliary
memory: if `(outcome,memory)` is injective, then `memory` itself must be injective because the
outcome coordinate is constant across verified lines. For finite carriers this forces
`card(lines) ≤ card(memory)`; a one-value archive is an explicit failing control. Thus repeated
verification simultaneously requires agreement in the detector layer and preserved difference in
the archive layer. `D0-INDEPENDENT-VERIFICATION-PROVENANCE-ARCHIVE-001`.

**T26 (Sector field-independence — added 2026-08-21).** The single invariant `359 = |E|` is the
*only* object the sectors share: their characteristic quadratic irrationals lie in three
multiplicatively-independent quadratic fields — α in `ℚ(√5)` (`α_top⁻¹ = 544 − 182√5`, T17), the
dark-energy S_DE window in `ℚ(√10)` (active eigenvalues `3/2 ± √10/40`, radicand `10` from the
window discriminant `640 = 2⁶·10`), and the transport/metric cubic in `ℚ(√386579)`
(`386579 = 193·2003`, T19). The radicands `{5, 10, 386579}` are pairwise-multiplicatively-
independent mod squares (no nonempty subset product is a square), so `ℚ(√5,√10,√386579)` has
degree 8 with Galois group `(ℤ/2)³`; and since `Gal(K/ℚ) = S₃` the transport splitting field has a
*unique* quadratic subfield, whence **both `√5 ∉ K` and `√10 ∉ K`** — the strict extension of T19.
The sectors meet only in `ℚ`. Pairwise field separation is constructive in Lean: the three
concrete quadratic algebras admit no pairwise `ℚ`-algebra equivalence. Their joint character
carrier is an explicit **degree-eight field over `ℚ`** (no zero divisors, fully internal) with
three commuting involutions and
diagonal sign table `(-1,+1,+1)`, `(+1,-1,+1)`, `(+1,+1,-1)` on three explicit generators
(`sector_character_assembly`, `sector_compositum_degree_eight_field`). Clean axioms, 0 `sorry`;
the full sector Galois group is internal at T27, while the transport `S₃` classification and
the `√5,√10 ∉ K` exclusions are internal at T29–T30. No external field-theory owner remains.
Can-fail certificate `vp_sector_field_independence.py`.
`D0-SECTOR-FIELD-INDEPENDENCE-001`.

**T27 (Full sector Galois closure — added 2026-08-21).** Let
`K₈ = ℚ(√5,√10,√386579)` be the degree-eight sector-character field of T26. The eight products
of the three sign involutions `σ_α`, `σ_DE`, `σ_transport` are pairwise distinct
`ℚ`-automorphisms (distinguished by their action on the three explicit axis generators), so
`|Aut(K₈/ℚ)| ≥ 8`. The general field bound gives `|Aut(K₈/ℚ)| ≤ [K₈:ℚ] = 8`; hence the
automorphism group has exactly 8 elements and `K₈/ℚ` is Galois. Every automorphism is uniquely
one of the eight three-bit sign choices: `Bool³ ≃ Aut(K₈/ℚ)`. Thus the sector-character Galois
group is exactly the explicit elementary three-bit sign group `(ℤ/2)³`, not merely a commuting
subgroup. Fully Lean-proved (clean axioms, 0 `sorry`), no bridge or external theorem owner.
`D0-SECTOR-GALOIS-CLOSURE-001`.

**T31 (Five-sector field ledger — added 2026-08-21).** The phrase “one invariant in five
sectors” now has an exact field-incidence theorem. On the three independent irrational axes
`(√5, √10, √386579)`, the sector rows are

```text
geometry          (0,0,1)
gravity           (0,0,0)
electromagnetism  (1,0,0)
mass / Yukawa     (0,0,1)
dark energy       (0,1,0).
```

The resulting linear readout from the five-dimensional formal sector space to the
three-dimensional character space is surjective, hence has **rank 3 and kernel rank 2**.
The kernel is exactly
`electromagnetism=0`, `darkEnergy=0`, `geometry+mass=0`, with gravity free. Thus the two and
only two redundancies are the rational gravity direction and the geometry-minus-mass transport
relation. `sectorCharacter_eq_iff` proves geometry/mass is the unique collision between
distinct sector rows. An intrinsic intersection theorem additionally proves that no transport
element can carry a nonzero `ℚ(√5)` or `ℚ(√10)` coordinate. Therefore the exact architecture is
not “five hidden fields”: it is **one rational hub plus three independent irrational
characters, with one forced duplication of the transport character by geometry and mass**.
`D0-FIVE-SECTOR-FIELD-LEDGER-001`.

**T32 / N8 (Yukawa qualitative-selector no-go — added 2026-08-22).** For a coefficient triple
`k=(a,b,c)∈ℚ³`, let `Y_k(λ)=a+bλ+cλ²` on the three transport roots. The full presently-owned
universal profile records (i) which generation values are equal and (ii) whether any value is
rational. For every non-scalar triple `(b,c)≠(0,0)`, the values are pairwise distinct and each
is irrational; Lean now proves that **all non-scalar triples have exactly the same complete
owned profile**. Moreover, the family

\[
k_t=(0,1,t),\qquad t\in\mathbb Q,
\]

is injective and lies wholly inside this single profile class. Consequently any selector
factoring only through the currently owned equality/rationality data is constant on an
infinite rational family and cannot select a unique non-scalar Yukawa operator.
`unique_selector_requires_new_information` gives the exact positive boundary: every unique
selector must distinguish two operators with identical current profiles, so it requires a new
coefficient-sensitive quantitative functional. This does not rule out a selector in principle
and does not refute the separate shell/Puiseux route; it proves that non-degeneracy and
irrationality alone contain zero coefficient-selection information.
`D0-YUKAWA-QUALITATIVE-SELECTOR-NOGO-001`.

**T33 (Yukawa selection ladder — added 2026-08-22).** The three present-core data layers
determine the equivariant Yukawa coefficients `(a,b,c)` to exactly measurable precision. On a
transport root frame with labeled eigenvalue map `orderedEig k i = a+bλᵢ+cλᵢ²`:

1. **Labeled spectrum ⇒ unique.** `orderedEig` is injective in `(a,b,c)` (Vandermonde on the
   three distinct roots).
2. **Unordered spectrum ⇒ ≤ 6.** Two triples share the eigenvalue multiset iff their labeled
   images differ by a root permutation, so each spectral fiber injects into `Perm(Fin 3)`;
   `spectral_fiber_finite` and `spectral_fiber_card_le_six` give a fiber of size at most `6`.
3. **Qualitative profile ⇒ infinite.** `qualitative_fiber_infinite` exhibits the injective
   family `(0,1,t)` inside one profile class.

So the spectral (characteristic-polynomial) data is **strictly** stronger than the qualitative
profile — it cuts an infinite fiber down to at most six — but a unique labeled coefficient
triple still requires exactly one missing datum: a canonical ordering (generation labeling) of
the three transport roots. This turns N8 from "profile insufficient" into a quantitative fiber
measurement that names the residual primitive precisely. `D0-YUKAWA-SPECTRAL-FIBER-LADDER-001`.

**T34 (Canonical generation labeling — added 2026-08-22).** The `S₃` residue of T33 is resolved
by the intrinsic real order. The three transport roots are distinct reals, so they admit a
*unique* strictly-increasing enumeration: any strictly-monotone `g : Fin 3 → ℝ` hitting the same
three-element root set equals the canonical one (`Finset.orderEmbOfFin_unique`). On this ordered
frame the labeled Yukawa map is injective. Hence the combinatorial `S₃` labeling freedom is not
free at all — the reals canonically order the roots — and the only genuinely external residue is
the order-preserving identification of the ordered roots with the physical generations `e<μ<τ`
(a single monotone bridge, the already-flagged winding order `W(e)<W(μ)<W(τ)`), plus the external
empirical target spectrum. This does not select the numerical coefficients; it removes the
combinatorial ambiguity entirely and downgrades the missing primitive from an `S₃` choice to one
monotone identification. `D0-TRANSPORT-ROOT-LABELING-CANONICAL-001`.

**T35 (Mass-sector residual = one orientation bit — added 2026-08-22).** After the real order
pins the labeling (T34), the strictly-*antitone* enumeration of the three roots is also unique
and equals `R.root ∘ Fin.rev` (derived from the monotone uniqueness through the order-reversing
involution `Fin.rev`), and it differs from the increasing one. Hence the generation
identification retains **exactly two** candidates — the increasing and decreasing labelings — a
genuine `ℤ/2` orientation bit, not an `S₃` choice. Combining T32–T35, the mass-sector
determination map is fully measured: qualitative profile ⇒ infinite; unordered spectrum ⇒ ≤6;
real order ⇒ labeling unique up to orientation; orientation ⇒ `ℤ/2`. The only external inputs
left are that orientation bit (the empirical mass order `e<μ<τ` / the winding bridge
`W(e)<W(μ)<W(τ)`) and the empirical target spectrum. `D0-MASS-SECTOR-ORIENTATION-BIT-001`.

**T36 (Structural generation-root order bridge — added 2026-08-22).** The orientation bit of
T35 is fixed internally on the actual structural generation carrier. In Lean,
`GenerationPhasonMode` is definitionally `TorusShell`; the attachment theorem owns the radial
order `innerD9 < coreD11 < outerD13`; T34 owns the unique increasing transport-root order. The
canonical map `generationRootBridge R s = R.root (torusShellEquivShell3 s)` therefore sends
inner/core/outer to low/middle/high root. Any map to the same three-root set preserving the
owned shell order is proved equal to it. Hence the structural generation frame and transport
frame have **one and only one order-preserving identification**: no orientation bit remains
internally. The only external residue is now the physical *naming* of the ordered structural
modes as `electron/muon/tau`, plus winding metric values and the empirical target spectrum; no
ordering or permutation choice remains. `D0-GENERATION-ROOT-ORDER-BRIDGE-001`.

**T37 (Charged-lepton structural naming — added 2026-08-22).** The physical branch names are
attached uniquely to the structural shells using only two already-owned orders. The charged-lepton
Puiseux row gives `electron < muon < tau` as `0 < 1/4 < 1/3`, with electron independently the
unique terminal calibration register; the structural carrier has
`innerD9 < coreD11 < outerD13` for every admissible torus parameter. The only map preserving
these orders is `electron→innerD9`, `muon→coreD11`, `tau→outerD13`; Lean proves any increasing
branch→shell map equals it, without even assuming bijectivity. Combined with T36, this gives the
full typed chain `electron/muon/tau → inner/core/outer → low/middle/high transport root`. No PDG
mass enters. What remains external is numerical winding/metric data, the Green/EFT–IR matching
functional and the empirical target spectrum — not names, order, orientation or permutations.
`D0-CHARGED-LEPTON-SHELL-BRIDGE-001`.

**T38 (Exact mass-metric modulus and order-only no-go — added 2026-08-22).** Define the adjacent
shell gap
`g = radius(coreD11) − radius(innerD9)`. Lean proves `g=(a−1)/2>0`, the outer-core gap is the
same `g`, and every admissible shell profile is exactly `(1,1+g,1+2g)`. Conversely
`a=1+2g` reconstructs a unique `TorusParameter`; an explicit equivalence
`TorusParameter ≃ PositiveShellGap` proves that the entire shell metric has exactly one positive
rational modulus. The composed branch-to-root map is parameter-free:
`electron→root 0`, `muon→root 1`, `tau→root 2`. Nevertheless the owned radial-order code is
constant on the whole metric family. The concrete witnesses `a=2` (`g=1/2`) and `a=3` (`g=1`)
have identical naming/order and different metrics, and Lean proves that no selector factoring
only through radial order can select a unique admissible parameter. Thus the remaining primitive
is no longer “some mass data”: it is one gap-sensitive scalar condition. A dynamical equation,
Green-resolvent/EFT–IR functional or measured passport can supply it; order alone cannot.
`D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001`.

**T39 (Joint mass-completion two-axis no-go — added 2026-08-22).** Let a mass candidate be a
pair `(k,T)` of a Yukawa coefficient triple and a shell metric. The current-data equivalence
combines the owned qualitative Yukawa profile of `k` with the radial-order code of `T`. Lean
proves that every pair of non-scalar candidates is equivalent under these combined data.
Consequently their combination still cannot support a unique selector. Two stronger theorems
separate the obstruction: coefficient-profile blindness prevents uniqueness even for an
arbitrarily metric-sensitive selector, and radial-order blindness prevents uniqueness even for
an arbitrarily coefficient-sensitive selector. Therefore every unique non-scalar mass
completion must introduce information on **both** residual axes — it must distinguish
equal-profile coefficients and same-order metrics. A single cross-coupled functional may satisfy
both requirements; the theorem does not require two independent imports. It proves that present
non-degeneracy/irrationality and shell-order data cannot close the mass sector, separately or
together. `D0-MASS-SECTOR-COMPLETION-NOGO-001`.

**T40 (Affine shell readout is equally spaced — the transfer must be nonlinear — added
2026-08-22).** On the affine shell metric `(1,1+g,1+2g)` a linear readout
`m(s) = α + β·radius(s)` has both adjacent gaps equal to `β·g`. Lean proves that its discrete
second difference is identically zero and its total span is exactly twice its first gap, for
every `g, α, β` — a parameter-free structural invariant. Consequently any target triple with
unequal spacing is unreachable by every affine readout and every admissible torus parameter.
The owned charged-lepton Puiseux row `(0, 1/4, 1/3)` has gaps `1/4` and `1/12`, so it is not
equally spaced and, by the theorem, is not an affine shell readout. The generation transfer is
therefore genuinely nonlinear in the shell radius — this pins the *functional class* of the
object T38/T39 showed to be necessary, without importing any PDG number.
`D0-AFFINE-SHELL-READOUT-NOGO-001`.

**T41 (Canonical normalized Puiseux transfer — minimal degree exactly two — added
2026-08-22).** Normalize the shell metric by
`u(s)=(radius(s)−1)/g`. For every admissible torus parameter this gives the same intrinsic
coordinates `inner/core/outer = 0/1/2`. The quadratic

```text
P(u) = u/3 − u²/12
```

then maps those shells exactly to the owned Puiseux row `(0,1/4,1/3)`, independently of the free
metric modulus. Lean proves coefficient uniqueness: any quadratic `c₀+c₁u+c₂u²` matching the
row has `(c₀,c₁,c₂)=(0,1/3,−1/12)`. Its discrete curvature is `−1/6` and its quadratic
coefficient is strictly negative, so the canonical transfer is concave. Together with T40,
which excludes every affine readout, this proves that the minimal polynomial degree in the
intrinsic normalized shell coordinate is exactly two. This is a unique interpolation/shape
theorem on the three owned shells, not yet a construction of the Green resolvent or the
EFT/IR map to physical masses. `D0-CANONICAL-PUISEUX-SHELL-TRANSFER-001`.

**T42 (Puiseux transfer saturation and threefold compression — added 2026-08-22).** The unique
T41 transfer has the completed-square identity

```text
P(2) − P(u) = (u−2)²/12.
```

Therefore `u=2` is its unique global maximum over `ℚ`. Since the normalized shells are
`0,1,2`, the outer/tau shell is the unique saturation point for every torus metric. The exact
increments are `P(1)−P(0)=1/4` and `P(2)−P(1)=1/12`, so the inner→core increment is exactly
three times the core→outer increment. The canonical exponent transfer is thus a saturating
concave law with a parameter-free `3:1` diminishing-increment structure. This concerns
Puiseux exponents, not physical mass differences. `D0-PUISEUX-TRANSFER-SATURATION-001`.

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

**T17 (Leading term).** The fine-structure constant's leading term is an exact identity in
ℤ[φ]: `ζ_E(0) = 359` and `ζ_E(−1) = 359φ⁻² − φ⁻⁵ = α_top⁻¹` (`zetaEdge_zero`,
`zetaEdge_neg_one`; the ℤ[φ] pair `(726, −364)`), numerically `137.0356`, parameter-free. This
identity — not any numerical-search uniqueness — is the owned content: the sweep certificate
`vp_alpha_leading_term_sweep.py` (reproduction 2026-08-10) records that within `4·10⁻⁴` of
`α⁻¹` the family `N·φᵖ + m·φᵠ` (`N ≤ 500`, `|m| ≤ 12`, `|p|,|q| ≤ 20`) contains three distinct
values, so the leading term stands on the identity alone, and an earlier "exactly one value"
claim is kept as a corrected row of record. The `~3.7·10⁻⁴` residual is closed by the
registered dressing (T18). `D0-EDGE-ALPHA-001`.

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

**T28 (Seam-return address rigidity — added 2026-08-21).** The owned discrete seam angle is the
reduced rational `12/5` (T18), and the owned toral total has depth `17 = 12+5` (T14). Define an
integer return address `(m,n)` by `n>0`, `m/n=12/5`, and `m+n=17`. Then `(m,n)=(12,5)`
uniquely: there is no rival integer return pair compatible with both owned quantities.
Consequently every compatible address forces the fifth-return seam defect
`φ⁻⁵=φ⁵−11`, the twelfth-return transport defect `φ⁻¹²=322−φ¹²`, and their product
`φ⁻¹⁷=(φ⁵−11)(322−φ¹²)`. Fully Lean-proved, clean axioms, no bridge. Scope: this is arithmetic
address rigidity; it does not assert the remaining semantic rule that the physical seam
transport uses the reduced-angle numerator/denominator as toral return addresses.
`D0-SEAM-RETURN-ADDRESS-RIGIDITY-001`.

**T29 (Transport cubic full Galois closure — added 2026-08-21).** For
`P(x)=x³−359x−2574`, Lean now proves the full group classification
`Gal(P/ℚ) ≃ S₃` and `[SplittingField(P):ℚ]=6`, without importing the usual theorem
`Gal ⊆ Aₙ ↔ discr(P) is a square`. The proof enumerates the three roots, derives their
elementary symmetric functions directly from the cubic equations, and constructs the oriented
Vandermonde
`δ=(r₁−r₀)(r₂−r₀)(r₂−r₁)`. It proves
`δ²=Polynomial.discr(P)=6185264`. If `|Gal|=3`, every induced root permutation has cube one
and hence sign `+1`; the determinant permutation law then fixes `δ` under the full Galois
group. Fixed-field descent puts `δ` in `ℚ`, contradicting the Lean theorem that the
discriminant is not a rational square. Thus the order-3 branch is impossible, the faithful
root action is bijective onto `Perm(Fin 3)`, and the group is exactly `S₃`.
`D0-TRANSPORT-CUBIC-GALOIS-S3-001`.

**T30 (√5 and √10 excluded internally — added 2026-08-21).** With `Gal ≃ S₃` internal (T29),
the last field-theory owner edge of T19 is now discharged in Lean without any external
unique-quadratic-subfield citation. First, `perm3_hom_eq_one_or_sign` proves that the only group
homomorphisms `S₃ → {±1}` are the trivial one and the sign character (the abelianization
`S₃ᵃᵇ = ℤ/2`, via *all transpositions are conjugate* and *transpositions generate*). Then, for a
rational `d` that is a non-square with `d·6185264` also a non-square, `K` contains no square root
of `d`: any `s` with `s² = d` yields the character `σ ↦ σs/s : Gal → {±1}`, which is either
trivial (forcing `d` a rational square) or the sign character (forcing `s = q·δ` with `δ` the
Vandermonde root, whence `d·6185264 = (q·6185264)²`). Both contradict the non-square hypotheses.
Instantiating at `d = 5` and `d = 10` gives **`√5 ∉ K` and `√10 ∉ K` as Lean theorems**
(`transport_splitting_excludes_sqrt5_sqrt10`), clean axioms, 0 `sorry`. This closes the T19/T26
field-exclusion edge entirely inside Lean. `D0-TRANSPORT-CUBIC-GALOIS-S3-001`.

**T19 (No spectral origin for φ — full closure).** For the transport cubic
`x³−359x−2574`: no element of quadratic minimal-polynomial degree lies in `ℚ(λ)` for any
single root (degree 3 is prime, `D0-TRANSPORT-FIELD-NO-GOLDEN-001`); and `√5 ∉ K` for the
full splitting field `K = ℚ(λ₁,λ₂,λ₃)` — the discriminant `6185264 = 2⁴·193·2003` is not a
square (mod 9) and `5·6185264` is not a square (mod 7), so `Gal(K/ℚ) = S₃` and the unique
quadratic subfield `ℚ(√Δ) ≠ ℚ(√5)`. Hence no rational-coefficient rational function of all
three transport eigenvalues jointly produces any golden quantity — the class is exhausted by
construction. Positive control: `Δ·386579 = 1546316²` — the same machinery confirms the
field's own kernel. The classification is now **fully internal, with no external citation left**:
`D0-TRANSPORT-CUBIC-GALOIS-CONFINEMENT-001` proves `|Gal|∈{3,6}`, T29 eliminates the order-3
branch by a Vandermonde fixed-field contradiction (`Gal≃S₃`, degree `6`), and T30 turns the
`S₃` character rigidity plus the `5Δ`/`10Δ` non-square certificates into the Lean theorems
`√5∉K` and `√10∉K` (`transport_splitting_excludes_sqrt5_sqrt10`). The original owner-edge
reliance on Dummit–Foote §14.6–7 is removed.

**T20 (Origin dichotomy).** Combining T14 and T19: within the exhausted
rational-coefficient spectral class, the φ-power content of the registered total has no
transport-spectral origin; the toral return system is its only owned positive origin —
both factors of `φ⁻¹⁷ = ξ₅·φ⁻¹²` are return defects of one toral automorphism, at returns
5 and 12. Proving rows: `D0-TRANSPORT-SPLITTING-FIELD-NOGO-001`,
`D0-TORAL-COMPOSITION-SEVENTEEN-001`; registered at `D0-ALPHA-SEAM-FORM-FORCED-001`.

## 5. The cascade — the central thesis

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

**P2 (γ).** Derive the total `φ⁻¹⁷ = ξ₅·φ⁻¹²` as a seam statement. T28 closes the arithmetic
address problem: angle `12/5` plus depth `17` uniquely forces the return pair `(12,5)` and both
toral defects. The remaining content is purely semantic: prove that the physical seam uses this
reduced-angle/depth address, equivalently identify its transport with the twelfth toral return.
Door 1 (`dim g_light`) remains the live rival and requires an owner decision on the
"electroweak" label.

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
