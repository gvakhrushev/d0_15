# Sector field-independence — the sharing is exactly the integer

*New result (2026-08-21). It sharpens "one invariant, five sectors" (T13,
`D0-EDGE-INVARIANT-CROSS-SECTOR-001`) and strictly extends the transport golden no-go (T19,
`D0-TRANSPORT-SPLITTING-FIELD-NOGO-001`). Owner: `D0-SECTOR-FIELD-INDEPENDENCE-001`, Lean
module `D0.Synthesis.SectorFieldIndependence` (in `D0.All`, clean axioms
`propext, Classical.choice, Quot.sound`, 0 `sorry`), deterministic can-fail certificate
[`../05_CERTS/vp_sector_field_independence.py`](../05_CERTS/vp_sector_field_independence.py).
Status: fully LEAN_PROVED; transport `S₃`, `√5/√10` exclusions, and the five-sector
rank/kernel ledger are internal; all gates green.*

---

## The question T13 left open

T13 proves that the single integer `359 = |E|` is the identical object consumed by five
sectors, and that on a rival scene every structural face moves together. That answers "is the
sharing real?" — yes. It does not answer the dual question: **is the sharing *only* the
integer, or do the sectors secretly share irrational structure too?** If two sectors' irrational
content lived in the same field, the "one invariant" story would be weaker — the coincidence
could be an artefact of a common hidden number. This note closes that gap.

## The three sector irrationalities

Each sector's characteristic irrational is already an owned object; collect them:

| sector | characteristic irrational | field |
|---|---|---|
| α / golden dressing | `α_top⁻¹ = 359φ⁻² − φ⁻⁵ = 544 − 182√5` (T17) | `ℚ(√5)` |
| dark energy (S_DE window) | active eigenvalues `3/2 ± √10/40` (`D0-SCENE-ACTIVE-EIGENVALUES-001`) | `ℚ(√10)` |
| transport / metric cubic | splitting field of `x³ − 359x − 2574`, quadratic subfield `ℚ(√Δ)`, `Δ = 6185264 = 2⁴·193·2003` (T19) | `ℚ(√386579)`, `386579 = 193·2003` |

## Theorem (sector field-independence)

**(A) Three independent fields.** The radicands `{5, 10, 386579}` are each squarefree and
pairwise-multiplicatively-independent modulo squares: no nonempty subset has a perfect-square
product. Hence the three quadratic characters are ℚ-independent, the compositum
`ℚ(√5, √10, √386579)` has degree **8** over ℚ with Galois group `(ℤ/2)³`, and the three
quadratic fields are pairwise distinct.

**(B) Transport is disjoint from both.** The cubic is irreducible with non-square discriminant.
The full group classification `Gal(K/ℚ) = S₃` and `[K:ℚ]=6` is now Lean-proved by
`D0.Synthesis.TransportCubicGaloisS3`: the oriented Vandermonde square root is fixed under the
order-3 alternative, which would make the discriminant rationally square. The exclusions
**`√5 ∉ K` and `√10 ∉ K` are themselves Lean theorems**
(`transport_splitting_excludes_sqrt5_sqrt10`), via the `S₃` character rigidity — no external
unique-quadratic-subfield step remains. Therefore **both
`√5 ∉ K` and `√10 ∉ K`**: the transport sector shares no quadratic irrational with either the
α sector or the dark-energy sector. (This is the strict extension of T19, which established only
`√5 ∉ K`.)

**(C) The intersection is ℚ.** The only object common to the three sectors is the rational
integer `359` — it is the `e₂` coefficient of the metric cubic, the α leading term `ζ_E(0)`, and
the numerator of the S_DE window product `359/160`. No field automorphism of the compositum
carries one sector's characteristic irrational to another's.

**(D) Constructive degree-eight character field.** The pairwise field distinction is now internalized:
for rational `a,b`, Lean proves directly that non-square `a` and non-square `ab` exclude any
`ℚ`-algebra equivalence
`QuadraticAlgebra ℚ a 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ b 0`, then specializes this to all three
sector pairs. A general propagation lemma proves that in `F(√d)` a base scalar `c` can be a
square only if `c` or `cd` was already a square in `F`. Iterating this lemma closes the
conditional field hypothesis at every layer: three successive quadratic adjunctions construct
a genuine field `SectorCharacterAlgebra` of degree **8** over `ℚ`, with no zero divisors. It
carries three explicit commuting
involutions `σ_α`, `σ_DE`, `σ_transport`, each of order two, with exact character table

| | α generator | DE generator | transport generator |
|---|---:|---:|---:|
| `σ_α` | −1 | +1 | +1 |
| `σ_DE` | +1 | −1 | +1 |
| `σ_transport` | +1 | +1 | −1 |

Thus the three-bit `(ℤ/2)³` sign architecture is no longer merely inferred from square classes:
it has an explicit finite field carrier and explicit actions, packaged in the Lean theorems
`sector_character_assembly` and `sector_compositum_degree_eight_field`.

The action is also recorded at the **element level** (`sector_sign_eigen_table`): the three axis
generators are simultaneous eigenvectors of the three involutions with eigenvalues
`σ_α = diag(-1,+1,+1)`, `σ_DE = diag(+1,-1,+1)`, `σ_transport = diag(+1,+1,-1)` — the exact
diagonal character table, definitionally.

**(E) Full Galois closure.** The separate module `D0.Synthesis.SectorGaloisClosure` takes all
eight products of the three signs and proves they are pairwise distinct by evaluating them on
the three axis generators. Hence `|Aut(K₈/ℚ)| ≥ 8`; mathlib's general
`AlgEquiv.card_le` gives `|Aut(K₈/ℚ)| ≤ [K₈:ℚ] = 8`. Therefore the automorphism group has
exactly eight elements, `K₈/ℚ` is Galois (`IsGalois.of_card_aut_eq_finrank`), and every
automorphism is uniquely one of the eight sign choices (`signAut_bijective`,
`Bool³ ≃ Aut(K₈/ℚ)`). This closes the sector-character Galois group as the explicit
three-bit group `(ℤ/2)³` with no external owner edge.

## Proof

(A) `sf(5)=5`, `sf(10)=2·5`, `sf(386579)=193·2003`, all squarefree. Subset products:
`5·10 = 2·5²` (√-part 2), `5·386579 = 5·193·2003`, `10·386579 = 2·5·193·2003`,
`5·10·386579 = 2·5²·193·2003` (√-part `2·193·2003`) — none is a perfect square. By Kummer
theory for multiquadratic extensions, independent square classes give `[ℚ(√a,√b,√c):ℚ] = 8`
with Galois group `(ℤ/2)³`. (B) The transport cubic's `S₃` classification is internal:
`D0-TRANSPORT-CUBIC-GALOIS-S3-001` proves it by the Vandermonde parity obstruction. The
remaining subgroup-lattice step says `S₃` has a single index-2 subgroup, hence a single
quadratic subfield `ℚ(√Δ) = ℚ(√386579)`; any `√5` or `√10` in `K` would be a second, distinct
quadratic subfield — impossible. (C) `359` is rational and `359 ∈ ℚ ⊂ ℚ(√5) ∩ ℚ(√10) ∩ K`;
by (A)–(B) the pairwise field intersections are exactly `ℚ`, so the shared *irrational* content
is empty and `359` is the entire shared structure. ∎

The arithmetic steps are also checked independently in
[`../05_CERTS/vp_sector_field_independence.py`](../05_CERTS/vp_sector_field_independence.py),
which also runs the can-fail controls `{5,10,50}` (dependent: `5·10·50 = 50²`) and `{5,20}`
(`20 = 5·2²`, same field) and requires them to be flagged as dependent.

## Why it matters

This turns "one invariant, five sectors" from a striking pattern into a rigidity statement.
The sectors are not different views of one hidden algebraic number: their irrationalities are
**triply field-independent**, and the *only* thing they share is the combinatorial integer
`359`. That is exactly the shape a genuine unification should have — a single discrete cause,
not a single continuous fudge factor. It also upgrades the transport no-go from "no `√5`" to
"no `√5` and no `√10`", i.e. the metric/gravity sector is provably golden-free *and*
dark-energy-window-free at the field level.

## Status and continuation

- **Done.** Arithmetic legs, pairwise non-isomorphism, the degree-eight character **field**
  (including no zero divisors), its three commuting involutions and their diagonal character
  table, and the full eight-element Galois closure are Lean-proved
  (`D0.Synthesis.SectorFieldIndependence`, in `D0.All`, clean axioms, 0 `sorry`); registered
  as `D0-SECTOR-FIELD-INDEPENDENCE-001` and `D0-SECTOR-GALOIS-CLOSURE-001`;
  `validate_csv`, `check_cert_can_fail`, value-ledger sync, `d0_score --strict` all green. The
  transport group itself is Lean-closed as `Gal=S₃`, and the `√5,√10 ∉ K` exclusions are now
  Lean theorems too (`D0-TRANSPORT-CUBIC-GALOIS-S3-001`), with no external field-theory step.
- **Done (five-sector ledger).** `D0-FIVE-SECTOR-FIELD-LEDGER-001` proves that the five sector
  rows have rank 3 and kernel rank 2: gravity is the rational direction, geometry and mass are
  the unique duplicated transport row, and EM/DE carry the two other independent characters.
  The full T13 field audit is therefore closed.
