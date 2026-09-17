import D0.Core.Phi
import D0.Bridge.Assumptions.SmoothInterpolation

namespace D0.Bridge

noncomputable def phiScale (Λ : ℝ) (k : ℤ) : ℝ := Λ * D0.phi ^ (-k)

theorem phi_scale_step (Λ : ℝ) (k : ℤ) :
    phiScale Λ (k + 1) = phiScale Λ k * D0.phi⁻¹ := by
  have hphi : D0.phi ≠ 0 := by
    unfold D0.phi
    positivity
  unfold phiScale
  rw [show -(k + 1) = -k + (-1 : ℤ) by ring]
  rw [zpow_add₀ hphi]
  rw [zpow_neg_one]
  ring_nf

theorem phi_rg_bridge_conditional (h : SmoothInterpolationAssumptions) :
    h.interpolation_exists :=
  h.interpolation_valid

end D0.Bridge
