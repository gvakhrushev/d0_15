import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# The zone count is bounded by the transport rank

`D0.Foundation.SceneCountRouteNoGo.reduction_is_bare_arithmetic` shows that both interpretation
arrows of `SceneCountReduction` are vacuous: their antecedents are theorems, so no construction can
consume them and the reduction degenerates to `3 ≤ n ∧ n ≤ 3`. The content therefore has to come
from a quantity **computed from the scene**, not from a closed proposition.

This module supplies that quantity for the **upper** bound. For any scene whose adjacency is
"different zone ⇒ adjacent" (the complete multipartite shape of `K(9,11,13)`):

* `rank_le_zoneCount` — the adjacency factors through the zone indicator, so `rank ≤ k`;
* `four_zones_forces_rank_four` — if the scene has at least four zones, four representatives span an
  invertible `4×4` hollow submatrix (inverse `(H-2I)/3`, exhibited), so `4 ≤ rank`;
* `zoneCount_le_three_of_rank_le_three` — contrapositive: a scene of transport rank `≤ 3` has at
  most three zones.

The `3` is therefore read off a **computed invariant** (a matrix rank), not declared as a
constructor count. `D0.Claims.Signature31Split.adj31_rank_eq_three` already owns `rank = 3` for the
frozen scene, and reads that `3` as the spatial transport-mode count of the `(3,1)` signature — an
object independent of any zone tally.

**Honest scope.** This is the upper half only, and it is conditional on the rank: it converts
"how many zones?" into "what is the transport rank?", which is progress only because rank is
computed rather than stipulated. It does **not** prove the scene's rank is 3 for a variable
candidate — `adj31_rank_eq_three` proves it for the frozen `K(9,11,13)`, whose zone count is 3 by
construction, so quoting it for a variable scene would be circular and is not done here. The
remaining obligation is exactly: force the transport rank to 3 without presupposing the zone count.
`D0-CASCADE-INSUFFICIENCY-CHAIN-001` and `D0-TOWER-STOP-NOEXT-001` stay proof targets.
-/

namespace D0.Foundation.ZoneCountFromRank

open Matrix

variable {n k : ℕ}

/-- The adjacency of a scene whose vertices carry zone labels: adjacent iff in different zones. -/
def adjOf (z : Fin n → Fin k) : Matrix (Fin n) (Fin n) ℚ :=
  Matrix.of fun i j => if z i = z j then 0 else 1

/-- Zone-membership indicator, `n × k`. -/
def indOf (z : Fin n → Fin k) : Matrix (Fin n) (Fin k) ℚ :=
  Matrix.of fun i c => if z i = c then 1 else 0

/-- Zone-to-vertex pattern, `k × n`. -/
def patOf (z : Fin n → Fin k) : Matrix (Fin k) (Fin n) ℚ :=
  Matrix.of fun c j => if c = z j then 0 else 1

/-- The adjacency factors through the zones. -/
theorem adjOf_factor (z : Fin n → Fin k) : adjOf z = indOf z * patOf z := by
  ext i j
  simp only [adjOf, indOf, patOf, Matrix.mul_apply, Matrix.of_apply]
  rw [Finset.sum_eq_single (z i)]
  · rcases eq_or_ne (z i) (z j) with h | h
    · simp [h]
    · simp [h]
  · intro c _ hc
    simp [Ne.symm hc]
  · intro h; exact absurd (Finset.mem_univ _) h

/-- **Upper bound on the rank.** The transport rank never exceeds the zone count. -/
theorem rank_le_zoneCount (z : Fin n → Fin k) : (adjOf z).rank ≤ k := by
  rw [adjOf_factor]
  calc (indOf z * patOf z).rank ≤ (indOf z).rank := rank_mul_le_left _ _
    _ ≤ k := rank_le_width _

/-- The `4×4` hollow pattern is invertible over `ℚ`: its inverse is `(H - 2I)/3`, exhibited
explicitly, so the fact is arithmetic rather than a determinant expansion. -/
theorem hollow_four_isUnit_det :
    IsUnit (!![(0 : ℚ), 1, 1, 1; 1, 0, 1, 1; 1, 1, 0, 1; 1, 1, 1, 0]).det := by
  apply Matrix.isUnit_det_of_right_inverse
    (B := !![(-2/3 : ℚ), 1/3, 1/3, 1/3; 1/3, -2/3, 1/3, 1/3;
             1/3, 1/3, -2/3, 1/3; 1/3, 1/3, 1/3, -2/3])
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mul_apply, Fin.sum_univ_succ, Matrix.one_apply]

/-- **Four zones force rank at least four.** Representatives of four distinct zones cut out the
hollow `4×4` submatrix, which is invertible, and rank does not drop on submatrices. -/
theorem four_zones_forces_rank_four (z : Fin n → Fin k)
    (hz : Function.Surjective z) (hk : 4 ≤ k) : 4 ≤ (adjOf z).rank := by
  -- four distinct zones
  have h0 : (0 : ℕ) < k := by omega
  obtain ⟨v0, hv0⟩ := hz ⟨0, by omega⟩
  obtain ⟨v1, hv1⟩ := hz ⟨1, by omega⟩
  obtain ⟨v2, hv2⟩ := hz ⟨2, by omega⟩
  obtain ⟨v3, hv3⟩ := hz ⟨3, by omega⟩
  set rep : Fin 4 → Fin n := ![v0, v1, v2, v3] with hrep
  have hsub : (adjOf z).submatrix rep rep =
      !![(0 : ℚ), 1, 1, 1; 1, 0, 1, 1; 1, 1, 0, 1; 1, 1, 1, 0] := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [adjOf, hrep, hv0, hv1, hv2, hv3, Fin.ext_iff] <;> omega
  have hunit : IsUnit ((adjOf z).submatrix rep rep).det := by
    rw [hsub]; exact hollow_four_isUnit_det
  have hrank : ((adjOf z).submatrix rep rep).rank = 4 := by
    have := Matrix.rank_of_isUnit ((adjOf z).submatrix rep rep)
      ((Matrix.isUnit_iff_isUnit_det _).mpr hunit)
    simpa using this
  calc 4 = ((adjOf z).submatrix rep rep).rank := hrank.symm
    _ ≤ (adjOf z).rank := rank_submatrix_le _ _ _

/-- **The upper map, from a computed invariant.** A scene of transport rank at most three has at
most three zones. The bound is read off the rank, not stipulated. -/
theorem zoneCount_le_three_of_rank_le_three (z : Fin n → Fin k)
    (hz : Function.Surjective z) (h : (adjOf z).rank ≤ 3) : k ≤ 3 := by
  by_contra hk
  push_neg at hk
  have h4 : 4 ≤ (adjOf z).rank := four_zones_forces_rank_four z hz (by omega)
  omega

/-- **The zone embedding the upper interpretation asks for**, derived from the rank bound. -/
noncomputable def zoneEmbeddingOfRank (z : Fin n → Fin k)
    (hz : Function.Surjective z) (h : (adjOf z).rank ≤ 3) : Fin k ↪ Fin 3 where
  toFun i := ⟨i.val, lt_of_lt_of_le i.isLt (zoneCount_le_three_of_rank_le_three z hz h)⟩
  inj' := by
    intro a b hab
    exact Fin.ext (congrArg (fun x : Fin 3 => x.val) hab)

end D0.Foundation.ZoneCountFromRank
