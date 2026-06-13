import D0.Core.Phi

namespace D0

noncomputable def delta0 : ℝ := (phi⁻¹ - phi⁻¹^2) / 2

theorem delta_half_gap : delta0 = (phi⁻¹ - phi⁻¹^2) / 2 := by
  rfl

theorem delta_phi_cubed : delta0 = 1 / (2 * phi^3) := by
  unfold delta0
  have hphi : phi ≠ 0 := by
    unfold phi
    positivity
  field_simp [hphi]
  nlinarith [phi_sq]

noncomputable def Q (D : ℤ) : ℝ := phi ^ (D - 4)

theorem Q_dimension_ladder (D : ℤ) : Q D = phi ^ (D - 4) := by
  rfl

end D0
