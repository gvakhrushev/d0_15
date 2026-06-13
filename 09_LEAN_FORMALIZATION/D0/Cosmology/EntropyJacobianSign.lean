import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace D0.Cosmology

noncomputable def conventionSign : ℝ := 1 -- selected convention: positive sign

theorem jacobian_eigenvalue_formula_convention {n : Type} (L : (n → ℝ) → (n → ℝ)) (v : n → ℝ) (μ c η : ℝ)
    (h_ev : L v = μ • v) :
    v + (conventionSign * c * η) • L v = (1 + conventionSign * c * η * μ) • v := by
  unfold conventionSign
  simp only [one_mul]
  rw [h_ev]
  ext i
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem jacobian_eigenvalue_unstable_convention (μ c η : ℝ)
    (hμ : μ > 0) (hc : c > 0) (hη : η > 0) :
    1 + conventionSign * c * η * μ > 1 := by
  unfold conventionSign
  simp only [one_mul]
  have : c * η * μ > 0 := mul_pos (mul_pos hc hη) hμ
  linarith

end D0.Cosmology
