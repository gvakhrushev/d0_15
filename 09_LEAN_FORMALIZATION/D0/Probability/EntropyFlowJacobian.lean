import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Cosmology.ZeroMeanModes

open scoped BigOperators

namespace D0.Probability

open D0.Cosmology

noncomputable def derivativeDirection {N : Type} [Fintype N] (c η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (v : N → ℝ) (i : N) : ℝ :=
  v i + c * η * L_pinv v i

theorem denominator_first_order_cancel {N : Type} [Fintype N] (c η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (v : N → ℝ)
    (h_v : zeroMean v) (h_L : zeroMean (L_pinv v)) :
    ∑ i, (v i + c * η * L_pinv v i) = 0 := by
  unfold zeroMean at h_v h_L
  rw [Finset.sum_add_distrib]
  rw [h_v]
  simp only [zero_add]
  rw [← Finset.mul_sum]
  rw [h_L]
  ring

theorem entropy_flow_linearization_zero_mean {N : Type} [Fintype N] (c η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (v : N → ℝ)
    (h_v : zeroMean v) (h_L : zeroMean (L_pinv v)) :
    (fun i => derivativeDirection c η L_pinv v i) = (fun i => v i + c * η * L_pinv v i) := by
  unfold derivativeDirection
  rfl

end D0.Probability
