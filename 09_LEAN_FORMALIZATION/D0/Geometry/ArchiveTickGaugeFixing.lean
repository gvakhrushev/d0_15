import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic

namespace D0.Geometry

theorem eta_absorbs_into_response {N : Type} (η : ℝ) (hη : η > 0)
    (L_pinv : (N → ℝ) → (N → ℝ)) (L_scaled : (N → ℝ) → (N → ℝ))
    (h_scaled : L_scaled = η • L_pinv) (x : N → ℝ) (i : N) :
    Real.exp (η * (L_pinv x i)) = Real.exp (L_scaled x i) := by
  rw [h_scaled]
  rfl

end D0.Geometry
