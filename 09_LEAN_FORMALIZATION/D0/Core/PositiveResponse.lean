import D0.Core.Phi

namespace D0

structure PositiveResponseSplit where
  p : ℝ
  positive : 0 < p
  below_one : p < 1
  normalized : p + p^2 = 1

noncomputable def primitivePositiveResponse : PositiveResponseSplit where
  p := primitiveRoot
  positive := by
    unfold primitiveRoot
    have hsq := sqrt_five_sq
    have hnonneg : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
    have h : (1 : ℝ) < Real.sqrt 5 := by
      nlinarith
    nlinarith
  below_one := by
    unfold primitiveRoot
    have hsq := sqrt_five_sq
    have hnonneg : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
    have h : Real.sqrt 5 < (3 : ℝ) := by
      nlinarith
    nlinarith
  normalized := primitive_root_satisfies

theorem positive_response_unique (s : PositiveResponseSplit) :
    s.p = primitiveRoot :=
  primitive_quadratic_unique_pos_root s.positive s.below_one s.normalized

end D0
