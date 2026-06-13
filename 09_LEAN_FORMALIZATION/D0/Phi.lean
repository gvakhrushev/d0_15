import D0.Core.Phi

namespace D0

noncomputable abbrev φ : ℝ := phi
noncomputable abbrev p : ℝ := phi⁻¹

theorem p_unit_closure : p + p^2 = 1 := phi_inv_satisfies_primitive

theorem p_positive : 0 < p := by
  unfold p phi
  positivity

theorem p_unique_positive :
    ∀ x : ℝ, 0 < x → x + x^2 = 1 → x = p := by
  intro x hx hclosure
  rw [show p = primitiveRoot by exact phi_inv_eq_primitiveRoot]
  exact primitive_quadratic_unique_pos_root hx (by nlinarith [hclosure]) hclosure

end D0
