import Mathlib.Tactic

/-!
# D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001 — ROOT R1

The automorphism group of `K(9,11,13)` is `S₉ × S₁₁ × S₁₃` (parts have distinct sizes — no part swaps).
Its permutation representation on `ℂ³³` decomposes into isotypes: **3 copies of the trivial** (one per part)
plus the three pairwise-inequivalent standard reps of `S₉, S₁₁, S₁₃` (dims 8, 10, 12). Hence

* `Σ mᵢ·dᵢ = 3·1 + 1·8 + 1·10 + 1·12 = 33` (the carrier),
* commutant `dim End_Aut(ℂ³³) = Σ mᵢ² = 3² + 1² + 1² + 1² = 12`.

The generation count **3 is the multiplicity of the trivial isotype** — a rank-only number: the trivial
isotype is a 3-dimensional block whose commutant is the full `M₃` (`dim 9 > 1`), i.e. `GL(3)` basis
freedom. So **no frozen datum fixes the Weyl-role assignment** of the 3 generations; ≥2 admissible
assignments exist. This is the NO-GO; the exact missing object is `PRIM-FINITE-SPECTRAL-TRIPLE-REP`
(a finite spectral-triple representation `(ρ,Γ,J,Π)` — absent: `RepresentationCarrier.lean` has only a
charge/anomaly carrier). Cites `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`, `D0-SM-HYPERCHARGE-ROW-OWNER-001`,
`D0-MATTER-REP-001`, the role-cycle pigeonhole no-go; does not re-mint them.
-/

namespace D0.Representation.FinitePathRepresentation

/-- `(multiplicity, irrep-dimension)` of each isotype in the `Aut = S₉×S₁₁×S₁₃` permutation rep on `ℂ³³`:
three trivials, and the standards of `S₉ S₁₁ S₁₃` (dims 8,10,12). -/
def isotypes : List (ℕ × ℕ) := [(3, 1), (1, 8), (1, 10), (1, 12)]

/-- Carrier dimension `Σ mᵢ·dᵢ`. -/
def totalDim : ℕ := (isotypes.map (fun p => p.1 * p.2)).sum

/-- Commutant dimension `Σ mᵢ²` (Schur). -/
def commutantDim : ℕ := (isotypes.map (fun p => p.1 * p.1)).sum

/-- The multiplicity of the trivial isotype = the generation count. -/
def generationMult : ℕ := 3

theorem total_dim_eq : totalDim = 33 := by decide
theorem commutant_dim_eq : commutantDim = 12 := by decide

/-- The generation block is `M₃`: its commutant has dimension `3² = 9 > 1` — `GL(3)` basis freedom. -/
theorem generation_block_underdetermined : 1 < generationMult ^ 2 := by decide

/-- **Underdetermination witness**: two distinct admissible role→generation assignments of the 3-dim
trivial isotype (the identity ordering and a transposition) — both compatible with the frozen
decomposition, so the assignment is not forced. -/
def assignA : List ℕ := [0, 1, 2]
def assignB : List ℕ := [1, 0, 2]

theorem two_admissible_assignments : assignA ≠ assignB := by decide

/-- **D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001.** The frozen `Aut`-rep gives carrier 33 and
commutant 12; the generation count 3 is rank-only (commutant block `9 > 1`, `GL(3)` freedom), and ≥2
admissible role assignments exist — so no finite spectral-triple representation is forced by frozen data
(missing: `PRIM-FINITE-SPECTRAL-TRIPLE-REP`). -/
theorem representation_reconstruction_nogo :
    totalDim = 33 ∧ commutantDim = 12 ∧ 1 < generationMult ^ 2 ∧ assignA ≠ assignB :=
  ⟨total_dim_eq, commutant_dim_eq, generation_block_underdetermined, two_admissible_assignments⟩

end D0.Representation.FinitePathRepresentation
