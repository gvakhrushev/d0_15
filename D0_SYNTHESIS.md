# D0 — The Synthesis

*The through-line, stated once, from a single axiom to the constants of physics. Every claim
below is owned by a theorem or certificate in [`D0_EXACT_RESULTS.md`](D0_EXACT_RESULTS.md);
this document is the argument, not a new ledger.*

---

## The thesis

**The constants of physics are not inputs. They are readouts of the arithmetic of one finite
graph — and that graph is forced by a single principle: a law may not carry a mandatory
external catalogue.**

That is the whole of D0 in one sentence. The rest is the demonstration that the sentence is
not a slogan but a chain of exact theorems, and that the chain closes on itself: the same few
numbers keep coming back, from independent directions, because there was only ever one object.

---

## 1. One move

D0 makes exactly one non-standard move. It applies **minimum description length to physical
law itself**. The principle **M1**:

> If two constructions produce the same class of distinguishable outcomes, the one that
> requires an extra mandatory external catalogue is inadmissible.

In Kolmogorov terms an underivable parameter `θ` sends a law from `K(T)` to `K(T)+K(θ|T)`: a
strictly longer minimal description for identical predictive content. M1 discards it. This is
the same target the operational-reconstruction programme reaches (Hardy 2001;
Chiribella–D'Ariano–Perinotti 2011; Masanes–Müller 2011) — complex quantum theory from finite
capacity — but D0 gets there by **description length instead of tomographic locality**. That
substitution is the novelty, and M1 is a proven predicate whose derivability clause is
grammar-functorial, not a philosophical posture (`D0-M1-PREDICATE-001`,
`D0-M1-UNIVERSALITY-001`).

Everything downstream is a consequence of refusing catalogues.

---

## 2. M1 rebuilds quantum mechanics

With no catalogue permitted, the structure of quantum theory is not assumed — it is forced:

- **Superposition is linear** because the unique catalogue-free mediator evolution has no
  interaction term: every interaction term needs a coupling constant, i.e. a catalogue (T1).
- **The Born rule is quadratic** — `x²+y²` is the unique phase-blind form fixed by the
  quarter-turn `J` — and this holds in dimension 2, where Gleason's theorem cannot reach.
  The weaker area-preservation hypothesis provably fails, with a machine-checked
  counterexample (T2).
- **The role algebra contains `Q₈`** as a forced factor: recording which conjugate copy would
  be a catalogue, which forces all-subgroups-normal and non-abelian, hence Hamiltonian, hence
  `Q₈` by Baer's classification (T3).
- **Time has a direction** because φ expands and its Galois conjugate contracts: the arrow is
  Pisot contraction, heat-trace monotone (T5).
- **Information is connectivity.** A record-disconnected domain and an external catalogue are
  the same thing: connected domains have M1-forced values with the observation as unique
  axiom-free witness; disconnected ones require a catalogue for every candidate value,
  including the observed one (T25).

No step here imports a Hilbert space. Each is what remains once catalogues are removed.

---

## 3. The keystone: scene selection and invariant reuse are different theorems

Under the registered three-zone, `+2`-ladder and Lucas-window hypotheses, the scene-selection
theorem uniquely gives `K(9,11,13)`, with 33 vertices and **359 edges**. The full derivation of
every one of those selector hypotheses directly from M1 remains the separately registered
cascade frontier; the uniqueness theorem itself is exact and conditional on its stated inputs.

Once the scene is selected, `359` becomes a particularly important shared readout:

| Sector | Where `359` appears |
|---|---|
| Geometry | the metric cubic `λ³ − 359λ − 2574`; the coefficient `e₂ = 359 = |E|` is the scene (T6–T7) |
| Gravity  | the discrete Einstein–Hilbert action proxy equals `359` (T12) |
| Electromagnetism | the fine-structure leading term `ζ_E(0) = 359`, `ζ_E(−1) = α_top⁻¹` (T17) |
| Mass | Yukawa non-degeneracy on that same cubic (T15) |
| Dark energy | the S_DE window product `λ_c·λ_r = 359/160` (T13) |

It is one invariant owned once (`D0-SCENE-001`) and consumed five times. The ownership is
enforced adversarially: on a rival scene `K(9,11,15)` every
structural face moves to `e₂ = 399` together — the sectors are rigidly locked to the single
number, not tuned independently (T13). The two carriers that meet here, `160x²−480x+359` and
`x³−359x−2574`, admit no nonzero intertwiner (integer Bézout certificate `39590739579959`,
cross-checked by a Sylvester resultant): they are genuinely different structures reading the
same integer.

But this convergence cannot be reversed into scene selection (T43/N12). The equation
`ab+ac+bc=359` has exactly **19** positive ordered solutions. In particular,

```text
E(9,11,13) = E(7,10,17) = 359,
```

while the rival has `V=34` and `T=1190`, not `33` and `1287`. Therefore any selector or α-form
factoring only through `E` accepts both. The minimal repair is one independent scalar:
Lean proves that `(V,E)=(33,359)` uniquely implies `(a,b,c)=(9,11,13)`.

The scene is also over-determined once two readings are available (T44): no single invariant
`V=33`, `E=359` or `T=1287` is selective, but each pair `(V,E)`, `(V,T)`, `(E,T)` uniquely gives
`(9,11,13)`. This removes the one-number cherry-pick objection without pretending the numbers
have already been derived from M1.

T45 then isolates the remaining derivational hinge. In the port-power route, if `n` independent
primitive detector capabilities are admitted, the scene-window condition is exactly

```text
(∀ k≤n, 9+2^k≤13) ↔ n≤2.
```

The current unstratified model has a third history primitive, so `n=3` admits size `8` and zone
`17`. The quotient theorem already proves that current-data comparisons are history-blind. The
single missing theorem is therefore: **every primitive M1-admissible detector comparison factors
through current membership/value data**. That local detector/memory stratification theorem is
now equivalent to the global GAP-E upper-bound closure.

T46 proves the catalogue-independence mathematics: catalogue-free comparisons are exactly lifts
of bare current-data comparisons, while order/history depends on an orientation catalogue. The
canonical M1 connection is subtler. `M1Forced` is a unique-answer predicate, but the
catalogue-free class contains many members. T47/N14 exhibits two and proves no
`M1Forced CatalogueFreeConstraint` witness exists. Thus catalogue-freedom cannot be promoted to
M1 forcing by relabeling.

The typed architecture itself is now closed. T48 constructs

```text
catalogue-free comparisons ≃ bare current comparisons
                           ≃ history-invariant full comparisons.
```

T49 performs the capability exhaustion in the full three-axis ambient: among primitive profiles
with history absent, exactly membership and value survive; an explicit equivalence with `Fin 2`
proves the count is two. History remains a real primitive negative control outside the detector
layer. Through T45, this count seals `zone≤13` **on the typed detector layer**. The remaining
frontier is a class-level M1 representation theorem mapping physical/M1-admissible comparisons
into that layer; the current unique-answer M1 predicate is the wrong interface for that task.

T50–T51 supply exactly that interface. `M1ClassAdmissible` is catalogue-invariance of a candidate
inside a catalogue system; it admits a class of any cardinality. Existing `M1Forced` is preserved
unchanged and proved to be the singleton-witness special case. For detectors, class admissibility
is extensionally identical to catalogue-freedom. A `PhysicalDetectorRepresentation` supplies a
comparison map, an admissibility predicate equivalent to class-M1 invariance, and injectivity on
admissible objects. Lean then constructs

```text
admissible physical comparisons
        ↪ catalogue-free comparisons
        ≃ history-invariant full comparisons
        → current-data concrete comparisons
        → {membership-profile, value-profile}.
```

Thus the formal M1/detector representation seam is closed at interface grade. Instantiating an
external physical formalism requires proving the interface fields for that formalism, just as any
generic representation theorem requires an instance; no unresolved foundational definition
remains in this leg.

T52 supplies the concrete instance for D0's own finite observation model. Because a binary
comparison has two inputs, its orientation catalogue is two-sided:

```text
InputSide → Current → Bool.
```

This detail is load-bearing; one shared orientation function cannot test different histories for
two equal current states. With independent left/right catalogues, Lean proves class-M1
admissibility iff full `HistoryInvariant`, instantiates the physical representation with identity
comparison and injectivity, derives current-data factorization on both inputs, and applies T49.
Thus the detector/M1/GAP-E application chain is closed on the actual in-repo observation
formalization. Other external formalisms merely supply their own instance of the already-proved
generic contract.

And the scene is not loosely specified. Its signature `(1,2)` is forced by zero trace and
`e₃ > 0` (T6); its zone triple is recovered uniquely from the spectrum, every hypothesis
load-bearing (inverse spectral rigidity, T8); the multiplicative pair `(1287, 960)` has
`(9,11,13)` as its unique preimage over all part counts (T9); and the visible/dark division is
exactly the invariant/invariant-free split of the kernel (T10).

**One explicitly selected graph, then one downstream integer reused by several inequivalent
sector operators.** The reuse is real architecture; it is not independent evidence for the
scene and not a proof that the sector interpretations are physical.

### 3a. The sharing is *exactly* the integer (field-independence)

A pattern this strong invites the obvious objection: maybe the five sectors secretly share a
hidden irrational number, and `359` is a side effect. They do not. Each sector's characteristic
irrational lives in a **different** quadratic field, and the three are field-independent:

- α / golden dressing: `ℚ(√5)` (`α_top⁻¹ = 544 − 182√5`)
- dark-energy window: `ℚ(√10)` (active eigenvalues `3/2 ± √10/40`)
- transport / metric cubic: `ℚ(√386579)`, `386579 = 193·2003`

The radicands `{5, 10, 386579}` are multiplicatively independent mod squares, so the compositum
has Galois group `(ℤ/2)³` and the fields are pairwise distinct; and because the transport cubic
is `S₃`, its splitting field has a *unique* quadratic subfield, so it contains **neither** `√5`
**nor** `√10`. The sectors intersect exactly in `ℚ`, and their entire shared content is the
integer `359`. This is the field-theoretic form of the thesis — a single *discrete* cause, not a
shared continuous parameter — and it strictly extends the transport golden no-go (T19) from "no
`√5`" to "no `√5` and no `√10`". Owned result: `D0-SECTOR-FIELD-INDEPENDENCE-001`
(Lean `D0.Synthesis.SectorFieldIndependence`, in `D0.All`, clean axioms, 0 `sorry`). More
strongly, the three characters now have an explicit **eight-dimensional joint algebra** with
three commuting sign involutions and diagonal character table
`(-1,+1,+1)/(+1,-1,+1)/(+1,+1,-1)` — a constructive finite carrier for the `(ℤ/2)³`
architecture. That carrier is now proved internally to be a **genuine field of degree 8 over
`ℚ`**, not merely a free algebra. The Galois closure is now internal too: the eight products of
the three sign involutions exhaust every `ℚ`-automorphism, `|Gal|=8`, and the field is Galois;
every automorphism is a unique three-bit sign choice (`Bool³ ≃ Gal`). The only remaining
field-theory owner edge has been removed: `Gal=S₃`, splitting degree `6`, and the exclusions
`√5,√10∉K` are internal by the Vandermonde and `S₃`-character arguments. Details:
[`03_THEORY_MAP/D0_SECTOR_FIELD_INDEPENDENCE.md`](03_THEORY_MAP/D0_SECTOR_FIELD_INDEPENDENCE.md).
The logically separate selection-direction audit is:
[`03_THEORY_MAP/D0_EDGE359_SELECTION_AUDIT.md`](03_THEORY_MAP/D0_EDGE359_SELECTION_AUDIT.md).

### 3b. The five-sector architecture has rank three

The five consumers of `359` do not define five unrelated field extensions. Their exact
character-incidence matrix on `(√5,√10,√386579)` is

```text
geometry          0 0 1
gravity           0 0 0
electromagnetism  1 0 0
mass              0 0 1
dark energy       0 1 0
```

Lean proves that its readout has **rank 3 and kernel rank 2**. The kernel is precisely the
rational gravity direction together with geometry minus mass; geometry/mass is the unique
collision of two distinct sector rows. Thus the correct synthesis is:

> **five sectors = one rational hub + three independent irrational characters, with the
> transport character necessarily shared by geometry and mass.**

This is `D0-FIVE-SECTOR-FIELD-LEDGER-001` (T31), not a diagrammatic interpretation: the
rank, kernel, collision classification, degree-eight character field, transport `S₃`,
`√5/√10` exclusions, rational EH proxy and Yukawa cubic exclusion are packaged in one
clean-axiom theorem.

### 3c. What the mass sector still cannot select

The transport commutant forces every non-scalar `a+bQ+cQ²` to split the three generations and
to give irrational values. But those two successes do **not** choose `(a,b,c)`. Lean now proves
that every non-scalar triple has the same entire currently-owned equality/rationality profile,
and that the injective rational line `(0,1,t)` lies inside one profile class. Therefore no
selector using only the present Yukawa theorem can have a unique winner (T32/N8).

This is stronger than saying “a selector is missing”: it identifies the exact information
deficit. A successful Yukawa completion must introduce a quantitative functional that is not
constant on profile-equivalent operators, or complete the separate shell/Puiseux/EFT–IR route.
Non-degeneracy and irrationality may certify a chosen operator, but they cannot choose one.

The quantitative version is a clean three-tier ladder (T33): the owned **qualitative** profile
leaves an infinite coefficient fiber; the **unordered spectrum** (characteristic polynomial)
cuts it to at most six; the **labeled** eigenvalue triple pins the coefficients uniquely. So
the entire residual freedom is exactly the `S₃` relabeling of the three roots — the missing
primitive is a canonical generation labeling, nothing more.

And that labeling is now itself pinned (T34): the three roots are distinct reals, so their
strictly-increasing enumeration is **unique**. The combinatorial `S₃` freedom therefore
vanishes using only the order of `ℝ`; the sole remaining external residue is the
order-preserving identification of the ordered roots with `e<μ<τ` (a monotone bridge) together
with the empirical target spectrum. The internal geometry supplies the generation labeling for
free; what stays outside is only the empirical mass input and its monotone reading.

And even that orientation is now measured exactly (T35): the strictly-decreasing enumeration is
the unique antitone one (`R.root ∘ Fin.rev`) and differs from the increasing one, so the entire
remaining combinatorial freedom is a single `ℤ/2` orientation bit. The mass sector is therefore
completely mapped: infinite → ≤6 → order-unique → one bit, with only the empirical mass order
`e<μ<τ` and the target spectrum left outside.

The structural generation carrier removes even that bit (T36). `GenerationPhasonMode` is
definitionally the owned torus-shell carrier, whose radial order is
`innerD9 < coreD11 < outerD13`; there is exactly one order-preserving bridge to the ordered
transport roots. Thus no orientation or permutation choice remains internally. What stays
external is only the physical naming of the ordered structural modes as `electron/muon/tau`,
the winding metric values, and the empirical target spectrum.

The physical branch names are now attached too (T37), without PDG input. The exact Puiseux row
orders them as `electron < muon < tau` (`0 < 1/4 < 1/3`), while the shell carrier is ordered
`innerD9 < coreD11 < outerD13`; there is exactly one map preserving both orders. Therefore

```text
electron → innerD9 → lowest transport root
muon     → coreD11 → middle transport root
tau      → outerD13 → highest transport root
```

is internally unique. What remains outside the theory is now purely numerical: winding gap
sizes, the Green/EFT–IR matching functional and the empirical target spectrum.

T38 resolves the *form* and dimension of that numerical residue. Writing

```text
g = radius(coreD11) − radius(innerD9),
```

Lean proves `g=(a−1)/2>0`, both adjacent gaps equal `g`, and the complete profile is exactly
`(1,1+g,1+2g)`. Conversely every positive rational `g` reconstructs one and only one admissible
`TorusParameter` by `a=1+2g`. Hence the residual metric space is not a vague family of possible
mass geometries: it is a one-dimensional positive ray with fixed affine shape.

This also gives the sharp no-go. The radial-order readout is `(true,true)` at every point of
that ray. Two explicit models, `a=2` (`g=1/2`) and `a=3` (`g=1`), have the same physical-name,
shell and transport-root labeling but different numerical metrics. Therefore no predicate that
factors through the already-owned order can select a unique point. The exact missing object is
now a **gap-sensitive scalar equation**. A Green-resolvent condition, EFT/IR matching functional,
new dynamics or measured passport may provide it; repeating the order argument cannot.

T39 then closes the last possible loophole in this diagnosis: perhaps the qualitative Yukawa
route and the shell-order route could remove each other's ambiguity when combined. They cannot.
On the product candidate space

```text
(non-scalar Yukawa coefficient triple) × (positive shell metric),
```

the combined currently-owned data are still constant. More strongly:

- if a selector remains blind to equal-profile coefficients, no amount of metric sensitivity
  can make the joint candidate unique;
- if it remains blind to same-order metrics, no amount of coefficient sensitivity can make the
  joint candidate unique.

Therefore every successful mass completion has a **two-axis information obligation**:
coefficient-sensitive and gap-sensitive. This need not mean two unrelated parameters — one
cross-coupled Green/EFT–IR functional could discharge both — but its uniqueness proof must be
load-bearing on both axes.

T40 fixes the functional's *shape*. A linear readout `m(s)=α+β·radius(s)` of the affine shell
`(1,1+g,1+2g)` is always equally spaced: its second difference is identically zero and its total
span is exactly twice its first gap, independent of `g, α, β`. So the equal-spacing signature is
a parameter-free structural invariant of any linear map. The owned charged-lepton Puiseux row
`(0,1/4,1/3)` has gaps `1/4` and `1/12` — unequal — hence it is provably not a linear shell
readout. The generation transfer must therefore be nonlinear in the shell radius, exactly the
Green-function/Puiseux behaviour already owned, and never a linear rescaling of the shells.

T41 shows that this lower bound is attained in one and only one minimal way. The intrinsic
coordinate

```text
u = (radius−1)/g
```

is `0,1,2` on inner/core/outer for every admissible metric. On it, the unique quadratic
interpolating the owned Puiseux row is

```text
P(u) = u/3 − u²/12.
```

The exact coefficients are `(0,1/3,−1/12)`; the discrete curvature is `−1/6`, so the transfer
is strictly concave. T40 excludes degree at most one and T41 constructs and uniquely classifies
degree two: the minimal polynomial shell-transfer degree is therefore exactly two. This closes
the interpolation problem, not the dynamical origin problem — the Green resolvent must still
derive this shape rather than merely be fitted to it.

T42 exposes the global law hidden in that unique polynomial:

```text
P(2) − P(u) = (u−2)²/12.
```

The outer shell `u=2` is therefore the unique saturation vertex for every metric. Moreover the
two owned increments are `1/4` and `1/12`; the first is exactly three times the second. So the
generation-exponent ladder has an exact diminishing-return architecture: increasing, concave,
saturating at the outer/tau shell, with parameter-free `3:1` increment compression.

---

## 4. The golden ratio has exactly one home

The other recurring object in physics-scale numbers is φ. D0 does not wave at it — it
localizes it and proves there is nowhere else it can come from.

- **Positive origin.** φ's content is return-defect arithmetic of a single toral automorphism
  `T = [[0,1],[1,−1]]`: `Tr(Tⁿ) = (−1)ⁿLₙ`, `(φ⁻¹)ⁿ = (−1)ⁿ(Lₙ − φⁿ)`, and the depth of the
  α correction factorizes as `φ⁻¹⁷ = (φ⁵−11)(322−φ¹²)` — both factors are returns (at 5 and
  12) of that one automorphism (T14).
- **Uniqueness by exhaustion.** `√5` lies outside the entire splitting field of the transport
  cubic — and this is now **entirely internal**. A direct root-enumeration proof constructs
  the oriented Vandermonde `δ`, proves `δ²=6185264`, and shows the order-3 alternative would
  fix `δ`, making the discriminant rationally square; hence `Gal ≃ S₃` (T29). The `S₃`
  character rigidity (only two homomorphisms `S₃→{±1}`) then turns the `5Δ`, `10Δ` non-square
  facts into Lean theorems `√5 ∉ K` and `√10 ∉ K` (T30) — no external field-theory citation.

Put together (T20): **within the exhausted spectral class, φ has no home except the toral
return system.** This is the shape of a real result — a positive mechanism plus a proof that
the alternatives are empty — not a numerical fit.

The α line then reads cleanly: the leading term `137.0356` is a parameter-free exact identity
in ℤ[φ] (T17); the dressing to the 9-digit CODATA value is itself decomposed into exact
theorems (angle `12/5`, `sin` channel forced by `Q₈`, seam factor `ξ₅`, linear form), with the
per-crossing weight forced to `φ⁻¹` under five named hypotheses (T18). The angle/depth arithmetic
is now rigid too: `12/5` and total depth `17` admit the unique integer return address `(12,5)`,
forcing both toral defects and their product (T28). What remains in **P2** is only the semantic
seam-to-return identification — not the choice of indices.

---

## 5. Why the count is three

The last structural question — why three zones, three generations, the recurring **3** — D0
answers from closure, not from a plugged-in axiom. Seven insufficiency floors each fail for a
named reason and interlock so that the repair of one floor is the failing carrier of the next.
The number **3** then appears as the least reflection-closed completion of the two interior
shell layers `{R−r, R}` under `x ↦ 2R−x` — cardinality exactly 3, with no `3 ≤ _` hypothesis
anywhere — and this three-element carrier is the same one carrying the zone sizes 9/11/13. The
whole cascade composes into a single clean-axiom theorem, `cascade_carried_assembly` (T21–T24).

---

## 6. What makes this a breakthrough

Three things, taken together, are what a strong theory looks like:

1. **Convergence.** Independent sectors — metric, coupling, mass, gravity, dark energy — do
   not each get their own parameter. They collapse onto one integer and one automorphism. A
   theory that keeps reusing the same object is doing the opposite of overfitting.
2. **Machine-checked core.** The load-bearing steps are not prose. `lake build D0.All` is
   green with **0 `sorry`** across 4509 jobs; the certificates are required to be able to fail.
   The results survive because they were attacked on the record, not asserted.
3. **No-go theorems as results.** D0 proves where things cannot come from — no spectral origin
   for φ (T19), transport spectrum blindness (N1), ΛCDM excluded in the ratio reading (N5),
   equivariant seam vanishing (N3). Knowing the empty regions is what turns a pattern into a
   mechanism.

## 7. Where it stands, and where to push

The core is closed and checkable. The frontier is short and named:

- **P1** — a second forcing route to φ with premises disjoint from the detector-equation
  family (the highest-value theorem available).
- **P2** — prove that the physical seam uses the uniquely forced `(12,5)` toral return address;
  the arithmetic factorization itself is closed by T28.
- **P3** — the each-floor-forced cascade over the full chain.
- **P4** — a multi-point discriminating experiment (protocols pre-registered and frozen).
- **P5** — the ranked attack queue.
- **P6** — a coefficient-sensitive Yukawa functional that breaks the profile equivalence of
  T32, or a completed shell Green-function/Puiseux/EFT–IR selector.

And the single sharpest place to press the axiom itself: the M1 squeeze. `N < D` loses
distinguishability (closed); `N > D` needs a significance catalogue — the upper branch rests
on MDL plus canonization. That is the edge of the theory, stated plainly, because a theory
worth anything tells you exactly where to attack it.

---

*Exact statements and owners: [`D0_EXACT_RESULTS.md`](D0_EXACT_RESULTS.md). Verify:
`cd 09_LEAN_FORMALIZATION && lake build D0.All`, then the `tools/` gate.*
