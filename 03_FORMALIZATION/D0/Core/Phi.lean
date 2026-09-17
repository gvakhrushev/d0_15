import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic

namespace D0

noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2
noncomputable def psi : ℝ := (1 - Real.sqrt 5) / 2
noncomputable def primitiveRoot : ℝ := (Real.sqrt 5 - 1) / 2

lemma sqrt_five_sq : (Real.sqrt 5)^2 = (5 : ℝ) := by
  exact Real.sq_sqrt (by norm_num)

theorem phi_inv_eq_primitiveRoot : phi⁻¹ = primitiveRoot := by
  unfold phi primitiveRoot
  apply inv_eq_of_mul_eq_one_right
  field_simp
  ring_nf
  rw [sqrt_five_sq]
  norm_num

theorem primitive_root_satisfies : primitiveRoot + primitiveRoot^2 = 1 := by
  unfold primitiveRoot
  ring_nf
  rw [sqrt_five_sq]
  norm_num

theorem phi_inv_satisfies_primitive : phi⁻¹ + phi⁻¹^2 = 1 := by
  rw [phi_inv_eq_primitiveRoot]
  exact primitive_root_satisfies

theorem phi_sq : phi^2 = phi + 1 := by
  unfold phi
  ring_nf
  nlinarith [sqrt_five_sq]

theorem psi_sq : psi^2 = psi + 1 := by
  unfold psi
  ring_nf
  nlinarith [sqrt_five_sq]

theorem phi_add_psi : phi + psi = 1 := by
  unfold phi psi
  ring

theorem phi_mul_psi : phi * psi = -1 := by
  unfold phi psi
  ring_nf
  rw [sqrt_five_sq]
  norm_num

theorem primitive_quadratic_unique_pos_root
    {p : ℝ} (hp0 : 0 < p) (_hp1 : p < 1) (hp : p + p^2 = 1) :
    p = primitiveRoot := by
  have hsq : (2 * p + 1)^2 = (Real.sqrt 5)^2 := by
    rw [sqrt_five_sq]
    nlinarith
  have h := sq_eq_sq_iff_eq_or_eq_neg.mp hsq
  cases h with
  | inl hpos =>
      unfold primitiveRoot
      nlinarith
  | inr hneg =>
      have hsqrt_nonneg : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
      have : Real.sqrt 5 = 0 := by nlinarith
      have : (5 : ℝ) = 0 := by
        calc
          (5 : ℝ) = (Real.sqrt 5)^2 := by rw [sqrt_five_sq]
          _ = 0 := by rw [this]; norm_num
      norm_num at this

end D0
