# D0 — v15

**One admissibility axiom, one explicitly constrained finite scene, and a shared arithmetic
readout across sectors.** Every statement is an exact theorem with its hypotheses inside it;
the core is machine-checked in Lean; the frontier is a list of named targets.

Repository: **[github.com/gvakhrushev/d0_15](https://github.com/gvakhrushev/d0_15)** ·
Lean 4 (mathlib) + deterministic Python certificates · `lake build D0.All` green, 0
`sorry`, 4509 jobs · full guard gate green.

**Start here — the one-page argument: [`D0_SYNTHESIS.md`](D0_SYNTHESIS.md).**
**The results, stated exactly: [`D0_EXACT_RESULTS.md`](D0_EXACT_RESULTS.md)** — 52 theorems,
14 no-go theorems, 6 named frontier targets.

---

## The claim in one paragraph

Fix one rule — a law may not carry a mandatory external catalogue — and impose the registered
three-zone, `+2`-ladder and Lucas-window scene criteria. Under those explicit hypotheses the
finite scene is uniquely `K(9,11,13)`. Once selected, its edge count **`359`** is the identical
owned object consumed by the metric cubic, fine-structure leading form, Yukawa structure,
dark-energy window and finite Einstein–Hilbert proxy. The direction is load-bearing:
**scene selection → `359` → sector readouts**. T43 proves that `359` alone has 19 positive
ordered tripartite preimages and therefore cannot select or independently validate the scene;
adding the independent vertex count `V=33` restores uniqueness. The
golden ratio that dresses the electromagnetic coupling has exactly one source — the return
defects of a single toral automorphism — and no other, proved by exhausting the alternative.
D0's strongest current claim is therefore architectural: several registered sector operators
reuse one scene-owned integer, not that this reuse itself proves the scene or physical reality.

## The axiom

Everything descends from one principle, **M1**:

> If two constructions give the same class of distinguishable outcomes, the one requiring an
> extra mandatory external catalogue is inadmissible.

In Kolmogorov terms: an underivable `θ` moves a law from `K(T)` to `K(T) + K(θ|T)` — a
strictly longer minimal description at unchanged predictive content. **M1 is minimum
description length applied to physical laws** ([BOOK_00 §0.3.1](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md)).
The operational reconstruction programme (Hardy 2001; Chiribella–D'Ariano–Perinotti 2011;
Masanes–Müller 2011) derives complex Hilbert space from finite capacity plus tomographic
locality; **D0 reaches the same target from MDL alone, replacing tomographic locality with a
description-length principle.** M1 is a proven predicate whose derivability clause is
grammar-functorial (`D0-M1-PREDICATE-001`, `D0-M1-UNIVERSALITY-001`).

## What is proved (digest — exact forms in the [ledger](D0_EXACT_RESULTS.md))

**Quantum mechanics.** Linearity of superposition: the unique catalogue-free mediator
evolution has no interaction term (T1). The Born quadratic `x²+y²` is the unique phase-blind
form invariant under the quarter-turn `J` — a hypothesis that covers dimension 2, where
Gleason does not apply; the weaker area-preservation hypothesis provably does not suffice
(T2, with machine-checked counterexample). The role algebra: all-subgroups-normal +
non-abelian ⇒ Hamiltonian ⇒ `Q₈` is a forced factor by Baer's classification (T3). The
arrow of time is heat-trace monotonicity of a finite Laplacian; the time layer has dimension
`deg ℚ(φ) = 2`, the unique Pisot-clean choice (T5). Information connectivity: under minimal
record semantics, an observer's record-connected domains have M1-forced values (unique
witness = the observation, axiom-free leg), while for a record-disconnected domain every
candidate value requires an external catalogue, and two record-disconnected observers can
force agreement on nothing — a disconnected information domain and an external catalogue
are the same thing (T25).

**Geometry.** For any 3-zone scene the quotient cubic is `λ³ − e₂λ − 2e₃`, forcing
signature (1,2); on K(9,11,13) the coefficients ARE the scene: `e₂ = 359 = |E|`,
`2e₃ = 2574` (T6–T7). The spectrum data `(D,H,M₂)` determine the zone triple — inverse
spectral rigidity with every hypothesis load-bearing (T8). The multiplicative pair
`(1287, 960)` has the unique preimage `(9,11,13)` over all part counts (T9). The dark
sector is exactly the Aut-invariant-free part of `ker A` (T10).

**One shared downstream invariant, five sectors.** The edge count `359` is the identical owned object in the
discrete Einstein–Hilbert proxy, the α leading term, the metric cubic, the Yukawa
non-degeneracy, and the S_DE window product `359/160` — with a certificate whose control
moves every structural face together on a rival scene, and a proven no-intertwiner ceiling
(Bézout certificate `39590739579959`) (T13). This is convergence after scene selection, not
five independent confirmations: `E=359` alone admits 19 ordered positive triples, including
the rival `(7,10,17)`; `(V,E)=(33,359)` uniquely repairs the selection (T43/N12).
Conversely the scene is not fragile either: no single count `V=33`, `E=359` or `T=1287` selects
it, yet **any two** of them do (T44). The scene is the unique common solution of any pair of
independent readings, so it is over-determined, not cherry-picked.

The remaining upstream scene joint is now localized exactly (T45/N13). Under the port-power
reading, the upper bound `zone≤13` holds **iff** the number of independent primitive detector
capabilities is at most two. The unstratified observation model admits a third history/order
capability, which reopens `2³=8` and the rival zone `17`. Therefore the missing foundational
theorem is singular and typed: primitive detector comparisons must factor through current
membership/value data, with history placed in the later memory layer.

Catalogue-independence is now exact (T46): order/history genuinely consults an orientation
catalogue, while catalogue-free comparisons factor through current data. But T47/N14 proves
this class is not an instance of the repository's canonical `M1Forced` predicate: there are many
distinct catalogue-free comparisons, whereas `M1Forced` requires one unique witness. T48 then
closes the pure layer mathematics by a canonical equivalence
`catalogue-free ≃ history-invariant ≃ current-data comparisons`. Finally T49 classifies primitive
profiles inside the full membership/value/history ambient: exactly membership and value survive,
history is the negative control, and the resulting typed count `2` seals the port-power zone bound
`≤13`. The remaining foundation seam is now precise: construct a **class-level M1 admissibility
bridge** from physical comparisons into this typed detector layer; unique-answer `M1Forced`
cannot serve that role.

That formal seam is now closed (T50–T51). `M1ClassAdmissible` expresses catalogue-independence
for a whole allowed class, while the existing `M1Forced` remains the singleton unique-answer
special case. A generic `PhysicalDetectorRepresentation` embeds every admissible physical
comparison into the catalogue-free/history-invariant detector layer; every primitive image is
membership-only or value-only. The canonical detector model instantiates the contract
non-vacuously and non-singleton. A concrete external physical formalism now has only a normal
application obligation — provide its comparison map and prove the explicit class-admissibility
and injectivity fields — not a missing foundational theorem.

That obligation is now discharged for the actual in-repo
`Observation(member,value,history)` model (T52). A two-sided orientation catalogue independently
fills history for the left and right comparison inputs; Lean proves class-M1 invariance is exactly
full history invariance, supplies the representation with identity comparison/injectivity, proves
factorization through current data on both inputs, and exhausts primitive images to
membership/value. The two-sided catalogue is load-bearing: a one-sided map misses
same-current/different-history dependence.

The field architecture is now exact too: the five sector rows have character rank `3` and
kernel rank `2`. Gravity is the rational hub; electromagnetism and dark energy carry the
`√5` and `√10` characters; geometry and mass are the unique pair sharing the transport
character `√386579`. Thus the synthesis is one rational hub plus three independent irrational
characters, not five hidden fields (T31).

The mass-sector boundary is exact as well: all non-scalar equivariant Yukawa polynomials
`a+bQ+cQ²` have the same currently-owned qualitative profile (three distinct irrational
values). An injective rational line of coefficient triples shares that profile, so no selector
using only those facts can choose a unique Yukawa operator. A quantitative coefficient
functional—or the independent shell/Puiseux completion—is mathematically necessary (T32/N8).

Quantitatively, the mass-sector freedom is an exact ladder (T33): the qualitative profile
leaves an infinite coefficient fiber, the unordered transport spectrum cuts it to at most six,
and the labeled eigenvalue triple is unique. The whole residual is the `S₃` relabeling of the
three roots — a canonical generation labeling is the single missing primitive.

That labeling is then pinned internally (T34): the three transport roots are distinct reals, so
their strictly-increasing enumeration is unique — the `S₃` freedom vanishes using only the real
order. The only genuinely external residue is the order-preserving identification of the ordered
roots with the physical generations `e<μ<τ`, plus the empirical target spectrum.

And that orientation is itself measured (T35): the decreasing enumeration is the unique antitone
labeling and differs from the increasing one, so the whole remaining combinatorial freedom is a
single `ℤ/2` orientation bit. The mass-sector determination map is fully quantified —
infinite → ≤6 → order-unique → one bit — leaving only the empirical mass order and target spectrum.

On the actual generation carrier even that bit disappears (T36):
`GenerationPhasonMode = TorusShell` already has the owned radial order
`innerD9 < coreD11 < outerD13`, and exactly one bridge preserves it into the ordered transport
roots. Only the physical names `electron/muon/tau`, winding gap sizes and empirical target
spectrum remain external.

The names are then attached internally as well (T37): the owned Puiseux order
`electron<muon<tau` is uniquely matched to the owned shell order
`innerD9<coreD11<outerD13`. The full typed chain is therefore
`electron/muon/tau → inner/core/outer → low/middle/high root`, with no PDG mass input.

The numerical residue is now classified exactly (T38), rather than left as “unknown metric
data.” Every admissible shell profile is

```text
(inner, core, outer) = (1, 1+g, 1+2g),   g > 0,
```

and `TorusParameter ≃ {g : ℚ // 0 < g}`. Thus the mass-sector shell geometry has **one**
positive metric modulus, not three free radii. The owned order code is identical for every
`g`; Lean proves that no selector using only that order can choose a unique metric. Any unique
completion must therefore be gap-sensitive. Because the residual is one-dimensional, one scalar
equation has the right arity, but existence and uniqueness of its selected root must still be
proved. Names, order, orientation, profile shape and the number of metric degrees of freedom are
no longer external.

Nor can the coefficient and metric routes hide each other's ambiguity (T39). On the joint
candidate space `(Yukawa coefficients) × (shell metric)`, the currently-owned qualitative
Yukawa profile and radial-order code are simultaneously constant. Lean proves two independent
necessity results: a unique completion must distinguish equal-profile coefficient triples
**and** same-order metrics. A metric-sensitive rule alone leaves the coefficient fiber; a
coefficient-sensitive rule alone leaves the positive-gap fiber. One cross-coupled functional
may break both, but the final mass problem now has an exact two-axis information contract rather
than an open-ended request for “more data.”

Finally, the *shape* of that missing functional is fixed too (T40). A linear readout of the
shell radii is provably equally spaced — its second difference vanishes and its span is exactly
twice its first gap for every `g, α, β`. The owned Puiseux row `(0, 1/4, 1/3)` is not equally
spaced, so it cannot be a linear shell readout: the generation transfer is genuinely nonlinear,
matching the Green/Puiseux route rather than a linear map.

That lower bound is attained uniquely (T41). Normalizing the shells by
`u=(radius−1)/g` sends them to `0,1,2` for every metric, and the unique quadratic matching the
owned exponent row is

```text
P(u) = u/3 − u²/12.
```

Its curvature is negative (`c₂=−1/12`), and no affine transfer exists, so the minimal
polynomial degree is exactly two. The remaining frontier is no longer the transfer's minimal
shape; it is the Green-resolvent origin of that shape and the EFT/IR map from exponents to masses.

The same quadratic carries a saturation law (T42):
`P(2)−P(u)=(u−2)²/12`. Thus the outer/tau shell is the unique vertex, while successive exponent
increments are `1/4` and `1/12`, an exact `3:1` compression. The structural hierarchy is therefore
not merely ordered: it is concave, saturating and quantitatively diminishing.

**Golden/toral calculus.** `Tr(Tⁿ) = (−1)ⁿLₙ`; `(φ⁻¹)ⁿ = (−1)ⁿ(Lₙ − φⁿ)`; the composition
law `L_{m+n} = L_mL_n − (−1)ⁿL_{m−n}` transports to traces; at `17 = 12+5`:
`L₁₇ = L₁₂L₅ + L₇` with the correction forced by `det T⁵ = −1`, and
`φ⁻¹⁷ = (φ⁵−11)(322−φ¹²)` — both factors of the α depth are return defects of one toral
automorphism (T14).

**The α line.** On the selected scene, the fine-structure leading form is an exact identity in ℤ[φ]:
`ζ_E(0) = 359` and `ζ_E(−1) = 359φ⁻² − φ⁻⁵ = α_top⁻¹` (T17), parameter-free and equal to
`137.0356`. This identity does not select the scene and is not a precision prediction: the
former sweep-uniqueness claim failed reproduction and is retired in the canonical registry.
The dressing that carries the form to the 9-digit CODATA value is decomposed into exact
theorems — angle `12/5`, `sin` channel forced by `Q₈`, seam factor `ξ₅`, linear form — and
under the five named hypotheses of T18 the per-crossing weight is exactly `φ⁻¹`. The origin of
that golden content is settled by a **full-closure no-go**: `√5` lies outside the entire
splitting field of the transport cubic (`Gal = S₃`, discriminant certificates mod 9 and
mod 7). The `S₃` classification is now itself Lean-owned: an explicit Vandermonde square-root
argument eliminates the order-3 branch and identifies the faithful root action with
`Perm(Fin 3)`; the `√5 ∉ K` and `√10 ∉ K` exclusions are then Lean theorems via the `S₃`
character rigidity. Thus no rational-coefficient function of the transport eigenvalues can produce it — the
φ-power mechanism has exactly one home, the toral return system (T19–T20).

**The cascade** — the central thesis: seven insufficiency floors, each with a proved
insufficiency and a satisfiable control; four interlock links of the exact shape *the repair
of floor n is the failing carrier of floor n+1*; and the count **3** derived from the closure
structure itself (the least reflection-closed completion of the two interior layers — with no
`3 ≤ _` hypothesis anywhere). The whole chain composes into one clean-axiom theorem, T24
(`cascade_carried_assembly`) (T21–T24).

**No-go theorems** are exact results, not caveats: transport spectrum blindness, ΛCDM
excluded by degeneracies alone in the ratio reading, gap-label genericity (the 25 computed
plateaux all lie in the module of any Fibonacci hull — such a measurement cannot
discriminate D0; revival condition: a forced gap-opening subset), equivariant seam
vanishing, three dead count routes, and the Yukawa qualitative-selector obstruction
(N1–N8; reopening conditions live in the registry rows).

## The frontier — named targets ([ledger](D0_EXACT_RESULTS.md#open-problems-named-targets-not-qualifications))

These are not qualifications of the results above; they are the highest-value theorems D0 has
not yet closed, each stated sharply enough to be worked or refuted.

- **P1** — a second forcing route to φ with premises disjoint from the detector equation
  family (one repaired pair exists: Hurwitz-class canonization + Jones slot; the route audit
  found 0/20 sampled multiplicity claims independent — proving one more is the
  highest-value theorem available).
- **P2** — identify the physical seam with the uniquely forced `(12,5)` toral return address.
  The angle/depth arithmetic is now closed: `12/5` plus total depth `17` admits no other integer
  pair and forces `φ⁻¹⁷ = ξ₅·φ⁻¹²` (T28). Door 1 (`dim g_light`) is the live rival awaiting
  an owner decision.
- **P3** — cascade completion: the each-floor-forced statement over the full chain, the
  2-cell reading of shell closure, the typed count seam.
- **P4** — a discriminating experiment. Pre-registered candidates: two-tone SBSL
  golden-drive (frozen before data contact), the Keller–Miksis window (≤ 2·10⁻³),
  `w = 3/5 − φ` vs future DESI.
- **P5** — the [computed attack queue](03_THEORY_MAP/D0_VALUE_RANKED.md) (6 items).

## Contact with data (from the [external-data scoreboard](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md))

D0 keeps every empirical contact — hits and misses — on one honest ledger. The strongest
matches:

| test | result |
|---|---|
| `sin²θ_W` on-shell | **0.23σ** |
| `m_s/m_d = 20` | **0.02σ** (bridge) |
| α leading term | **exact identity** (T17), `137.0356`, parameter-free |
| Coldea `φ` (CoNb₂O₆) | corroborates (not discriminating) |
| DESI DR2 | consistent with evolving dark energy |

And the recorded negatives, kept on the same ledger because a falsifiable theory earns its
credibility from them: the SPARC phason-halo kernel is rejected in ~91% of galaxies; the
PMNS `δ₀` family and the LIGO `φ⁻¹` defect are post-hoc, non-discriminating; the DESI thawing
corner is not yet confirmed. **The one thing not yet on the board is a multi-point
discriminating confirmation — that is target P4, and its protocols are pre-registered and
frozen.**

## Verify it yourself

```bash
pip install -r requirements.txt
python tools/validate_csv.py            # registry integrity (663 claims)
python tools/d0_logic_chain.py          # derivation chain + block hashes
python tools/d0_value_model.py          # value ledger + ranking
python tools/d0_score.py --strict       # scoreboard (75.5%, 0 integrity demotions)
```

```bash
cd 09_LEAN_FORMALIZATION && lake build D0.All   # 4509 jobs, 0 sorry
python 09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py
```

**How to kill it** (D0 is built to be attackable, and tells you exactly where): refute one of
27 named bridge assumptions ([ledger](09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv),
each with a written failure condition); exhibit a second object against any uniqueness row;
break a certificate (every cert is required to be able to fail — `check_cert_can_fail.py`
enforces it); or press the root M1 squeeze (`N < D` loses distinguishability, `N > D` needs a
significance catalogue — the lower branch is closed; the upper branch rests on MDL plus
canonization, and that is the sharpest open edge). Naming the attack surface this precisely is
the point: nothing here hides behind vagueness.

## Repository layout

| Path | Contents |
|---|---|
| [`D0_SYNTHESIS.md`](D0_SYNTHESIS.md) | **the one-page argument — the through-line from M1 to the constants** |
| [`D0_EXACT_RESULTS.md`](D0_EXACT_RESULTS.md) | **the theorem ledger — start here** |
| [`01_BOOKS/`](01_BOOKS/) | the theoretical spine — `BOOK_00` entry contract; `BOOK_01`–`09` mathematics and physics |
| [`03_THEORY_MAP/`](03_THEORY_MAP/) | [value ranking](03_THEORY_MAP/D0_VALUE_RANKED.md), [derivation chain](03_THEORY_MAP/D0_LOGIC_CHAIN.json), architecture, route inventory |
| [`05_CERTS/`](05_CERTS/) | deterministic `vp_*.py` certificates with reachable FAIL controls |
| [`08_PASSPORTS/`](08_PASSPORTS/) | curated external data (PDG, DESI, CMB, LIGO, SPARC…) + SHA256 manifests + real-data scoreboard |
| [`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/) | the Lean 4 package; canonical registry + [value ledger](09_LEAN_FORMALIZATION/docs/D0_VALUE_LEDGER.csv) |
| [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/) | Rosetta stone: every D0 mnemonic in conventional terms |
| [`tools/`](tools/) | guard scripts, registry sync, value model, chain builder |

## Registry, by the numbers

663 claims — 470 `LEAN_PROVED` (+31 with named bridge assumptions), 111 python-certified,
49 open, 2 deprecated; 251 core-formalized, 169 cert-closed, **104 no-go theorems** (97
NO-GO + 7 NO_GO_PROVED), 62 proof-targets. Derivation chain: 522 of 663 chained, 226
genesis blocks, max depth 10 — the structure is wide, not deep, because the results converge
on shared objects rather than stacking into a fragile tower. What each result is *worth* is
ranked separately in the [value ledger](03_THEORY_MAP/D0_VALUE_RANKED.md).

## Method

Every claim passes an adversarial forcing loop before it is registered: registry pre-flight →
exact computation with can-fail certificates → a memo with a pre-registered attack surface →
an independent skeptic mandated to kill it by naming a second object or a precise gap →
repairs accepted as errors of record. Kills, retractions and corrected grades are themselves
first-class registered results — 2 deprecated rows, a quarantine ledger and accepted-kill
records — which is why a survived claim here means more than an asserted one: it has already
been attacked on the record.

## License / status

Private research snapshot (**v15**). Contact the author for usage or collaboration.
