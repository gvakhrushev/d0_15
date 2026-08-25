import D0.VNext.AFOneDimensionalReductionClassification

/-!
# AF-reduction exhaustion — the anchor no-go upgraded from witness to the WHOLE su-reduction
# family (no-go-synthesis pass #3, DRAFT)

Claim: `D0-AF-REDUCTION-EXHAUSTION-001` (candidate). Memo:
`_TASKS_CENTER_ATTACK/AF_REDUCTION_EXHAUSTION_MEMO.md`.

The owned no-go (`D0-VNEXT-AF-ONE-DIMENSIONAL-REDUCTION-CLASSIFICATION-001`, Outcome D) shows
the WITNESS mismatch: the canonical trace-zero reduction of `A₃ = M₅ ⊕ M₃` has parts
`(24, 8, 1) ≠ (9, 11, 13)`. This module upgrades the witness to the WHOLE FAMILY, two ways:

1. **The witness exhausts its own class (Diophantine uniqueness).** A two-block algebra
   `M_a ⊕ M_b` has reduced total `a² + b² − 1 = 33` iff `a² + b² = 34`, whose ONLY solution
   with `a ≥ b ≥ 1` is `(5, 3)` (`two_block_dim33_unique`). So `M₅ ⊕ M₃` was never one
   candidate among many — it is the unique two-block algebra at the scene dimension, and it
   fails.
2. **The residue obstruction kills EVERY block list (universal exhaustion).** Every part of a
   canonical trace-zero reduction of `⊕ᵢ M_{dᵢ}` is of the form `dᵢ² − 1` (an `su(dᵢ)`
   summand) or `1` (a `u(1)` from the center minus the trace line). The scene parts avoid BOTH
   forms: `9, 11, 13 ≠ 1`, and `d² − 1 ∈ {9, 11, 13}` would need `d² ∈ {10, 12, 14}` — none a
   square (`scene_parts_avoid_su_lattice`). Hence NO canonical su-type reduction of ANY
   finite-dimensional multi-matrix algebra — ANY number of blocks, ANY sizes — matches the
   scene parts, even as a multiset (`no_su_reduction_matches_scene`). Infinitely many
   candidates die at once on a residue obstruction.

Honest scope: the exhaustion is over the CANONICAL-REDUCTION SHAPE (su-parts + u(1)s — the
reduction grammar the owned no-go itself uses); exotic non-canonical carryings are outside
the class and stay with the no-go's own boundary. The positive/selector face: the scene
fingerprint `(9,11,13) = (L₅−2, L₅, L₅+2)` is separated from the entire su-dimension lattice
`{d²−1}` — the Lucas frame and the su-lattice are disjoint in the scene window, which is WHY
the AF route was never going to carry the scene; the `34→33` near-miss is now located exactly
at the unique Fibonacci two-block `(5,3)`.
-/

namespace D0.VNext.AFReductionExhaustion

open D0.VNext.AFSceneAnchorDimensionAudit

/-- **Diophantine uniqueness of the witness' class.** `a² + b² = 34` with `a ≥ b ≥ 1` has the
unique solution `(5, 3)`: the owned no-go's witness `M₅ ⊕ M₃` exhausts the two-block class at
the scene dimension (`a² + b² − 1 = 33`). -/
theorem two_block_dim33_unique (a b : ℕ) (hab : a ≥ b) (hb : b ≥ 1)
    (h : a * a + b * b = 34) : a = 5 ∧ b = 3 := by
  have ha : a ≤ 5 := by
    rcases Nat.lt_or_ge a 6 with h6 | h6
    · omega
    · have : a * a ≥ 6 * 6 := Nat.mul_le_mul h6 h6
      omega
  interval_cases a <;> interval_cases b <;> omega

/-- **The residue obstruction.** No scene part is `1`, and no scene part is `d² − 1` for any
`d` — the needed squares `10, 12, 14` do not exist. The scene parts avoid the entire
su-dimension lattice. -/
theorem scene_parts_avoid_su_lattice :
    ∀ p ∈ sceneParts, p ≠ 1 ∧ ∀ d : ℕ, p ≠ d * d - 1 := by
  intro p hp
  have hcases : p = 9 ∨ p = 11 ∨ p = 13 := by
    simpa [sceneParts] using hp
  refine ⟨by rcases hcases with rfl | rfl | rfl <;> omega, ?_⟩
  intro d
  rcases Nat.lt_or_ge d 4 with hlt | hge
  · interval_cases d <;> rcases hcases with rfl | rfl | rfl <;> omega
  · have : d * d ≥ 4 * d := Nat.mul_le_mul_right d (by omega)
    have : d * d ≥ 16 := by
      have h4 : 4 * d ≥ 16 := by omega
      omega
    rcases hcases with rfl | rfl | rfl <;> omega

/-- The canonical trace-zero reduction parts of a multi-matrix algebra `⊕ᵢ M_{dᵢ}`
(blocks `dᵢ ≥ 1`): one `su(dᵢ)` part of size `dᵢ² − 1` per block WITH `dᵢ ≥ 2` (su(1) is
0-dimensional and contributes NO part — the `filter (0 < ·)`, skeptic #22 R1; `d = 0` is not
a block), plus `k − 1` `u(1)` parts of size `1` (center minus the trace line). This is the
faithful standard rendering of the reduction grammar the owned no-go uses at its witness,
stated for an arbitrary block list; it reproduces the owned tower levels correctly
(`A₀ = ℂ⊕ℂ ↦ [1]`, `A₁ = M₂⊕ℂ ↦ [3,1]`). -/
def reductionParts (ds : List ℕ) : List ℕ :=
  ((ds.map (fun d => d * d - 1)).filter (0 < ·)) ++ List.replicate (ds.length - 1) 1

/-- Sanity: at the owned witness `(5,3)` the general grammar reproduces the owned parts. -/
theorem reduction_parts_witness : reductionParts afBlocks = [24, 8, 1] := by decide

/-- **Anchor-by-theorem (skeptic #22 R2).** The general grammar equals the OWNED
`reducedParts` at the witness — the import is load-bearing, the anchor is a theorem. -/
theorem reduction_parts_witness_owned :
    reductionParts afBlocks =
      D0.VNext.AFOneDimensionalReductionClassification.reducedParts := by decide

/-- Faithful-grammar checks at the owned tower's low levels: su(1) blocks contribute no part. -/
theorem reduction_parts_tower_levels :
    reductionParts [1, 1] = [1] ∧ reductionParts [2, 1] = [3, 1] := by decide

/-- **Universal exhaustion.** For EVERY block list `ds` — any number of blocks, any sizes —
the canonical reduction parts do NOT match the scene parts, even as multisets: `9` is a scene
part but can never appear among the reduction parts (`9 ≠ 1` and `9 ≠ d² − 1` for all `d`).
The owned witness no-go holds across the whole su-reduction family at once. -/
theorem no_su_reduction_matches_scene (ds : List ℕ) :
    ¬ ((reductionParts ds : Multiset ℕ) = (sceneParts : Multiset ℕ)) := by
  intro h
  have h9scene : (9 : ℕ) ∈ (sceneParts : Multiset ℕ) := by decide
  have h9red : (9 : ℕ) ∈ (reductionParts ds : Multiset ℕ) := by
    rw [h]; exact h9scene
  have h9mem : (9 : ℕ) ∈ reductionParts ds := by
    simpa using h9red
  unfold reductionParts at h9mem
  rcases List.mem_append.mp h9mem with hmap | hrep
  · have hmem : (9 : ℕ) ∈ ds.map (fun d => d * d - 1) := List.mem_of_mem_filter hmap
    obtain ⟨d, -, hd⟩ := List.mem_map.mp hmem
    have := (scene_parts_avoid_su_lattice 9 (by decide)).2 d
    omega
  · have := List.eq_of_mem_replicate hrep
    omega

/-- **AF-reduction exhaustion (bundle).** The witness' class is Diophantine-unique
(`{5,3}` is the only two-block solution at the scene dimension), the scene parts avoid the
entire su-dimension lattice, the general grammar reproduces the owned witness parts, and no
block list whatsoever yields the scene parts. The owned Outcome-D no-go is thereby
family-wide, not witness-bound. -/
theorem af_reduction_exhaustion :
    (∀ a b : ℕ, a ≥ b → b ≥ 1 → a * a + b * b = 34 → a = 5 ∧ b = 3) ∧
    (∀ p ∈ sceneParts, p ≠ 1 ∧ ∀ d : ℕ, p ≠ d * d - 1) ∧
    reductionParts afBlocks = [24, 8, 1] ∧
    (∀ ds : List ℕ, ¬ ((reductionParts ds : Multiset ℕ) = (sceneParts : Multiset ℕ))) :=
  ⟨two_block_dim33_unique, scene_parts_avoid_su_lattice,
   reduction_parts_witness, no_su_reduction_matches_scene⟩

end D0.VNext.AFReductionExhaustion
