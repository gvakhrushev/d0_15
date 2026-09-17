import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace D0.Cosmology

theorem jacobian_eigenvalue_formula {n : Type} (L : (n → ℝ) → (n → ℝ)) (v : n → ℝ) (μ c η : ℝ)
    (h_ev : L v = μ • v) :
    v + (c * η) • L v = (1 + c * η * μ) • v := by
  rw [h_ev]
  ext i
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem jacobian_eigenvalue_unstable_if_mu_positive (μ c η : ℝ)
    (hμ : μ > 0) (hc : c > 0) (hη : η > 0) :
    1 + c * η * μ > 1 := by
  have : c * η * μ > 0 := mul_pos (mul_pos hc hη) hμ
  linarith

end D0.Cosmology
