import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveNaiveWeightedDegreeLeakageNoGo

Owner: `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001`.

The registered research target concerns the position-dependent operator
`d_w = sqrt(w) d` and whether its square has a nonzero two-direction
cross-term. This file does not currently define that operator, translation
operators, or a CAR-valued differential. Its compiled formal slice is only a
two-value witness (`w₀ = 1`, `w₁ = 4`) that the square roots differ, together
with the cardinality of `Role`. It therefore does not prove nilpotency
failure, form-degree leakage, or that curvature must enter through the Hodge
metric. Those stronger statements remain outside this formal result and need
an exact operator construction and a proved nonzero witness before this file
can support the registered no-go.
-/

/-- The first fixed sample weight used only in the square-root inequality below. -/
def naiveWeight0 : ℝ := 1

/-- The second fixed sample weight used only in the square-root inequality below. -/
def naiveWeight1 : ℝ := 4

theorem sqrt_naive_weights_ne : Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1 := by
  unfold naiveWeight0 naiveWeight1
  have h1 : Real.sqrt 1 = 1 := Real.sqrt_one
  have h4 : Real.sqrt 4 = 2 := by
    have : (2 : ℝ) ^ 2 = 4 := by norm_num
    rw [← this, Real.sqrt_sq]
    linarith
  rw [h1, h4]
  norm_num

/-- Current compiled owner slice: the two fixed sample weights have distinct
square roots and the Role carrier has four elements. This does not formalize
the variable-weight differential or its proposed nilpotency/degree-leakage
obstruction. -/
theorem archive_naive_weighted_car_degree_leakage_nogo_owner :
    (Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1) ∧
    (Fintype.card Role = 4) :=
  ⟨sqrt_naive_weights_ne, card_role⟩

end D0.Geometry
