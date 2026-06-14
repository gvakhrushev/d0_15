import D0.Core.Phi

/-!
# D0-DELTA-ALPHA-EXACT-001 — the gluing anomaly Δ_α as an exact element of Q(φ) (Lean)

Python certificate: `05_CERTS/vp_delta_alpha_exact.py`.

Both writings of `α⁻¹` are closed forms over `Q(φ)` with no data input:
`α_top⁻¹ = 359·φ⁻² − φ⁻⁵` and `α_alg⁻¹ = 2¹¹·(6/5)φ²·φ⁻⁸ + (2/3)·(1/2)φ⁻³`. This module
proves, from `φ²=φ+1` alone, their exact values and the exact value of the difference

    Δ_α = α_top⁻¹ − α_alg⁻¹ = −156109/5 + (289442/15)·φ ,

so Δ_α is an EXACT element of `Q(φ)`. (The analytic OWNER deriving the form of `α_alg⁻¹`
from the feedback resolvent — CVFT-F1 — stays the frontier; `m_ν ∝ Δ_α²` stays a BRIDGE.)
-/

namespace D0.Spectral

open D0

private lemma hpos : (0 : ℝ) < phi := by unfold phi; positivity
private lemma hne : phi ≠ 0 := ne_of_gt hpos

/-- `φ⁻¹ = φ − 1`. -/
theorem phi_inv_lin : phi⁻¹ = phi - 1 :=
  inv_eq_of_mul_eq_one_right (by linear_combination phi_sq)

/-- `φ⁻² = 2 − φ`. -/
theorem phi_inv2 : phi⁻¹ ^ 2 = 2 - phi := by
  rw [phi_inv_lin]; linear_combination phi_sq

/-- `φ⁻³ = 2φ − 3`. -/
theorem phi_inv3 : phi⁻¹ ^ 3 = 2 * phi - 3 := by
  have e : phi⁻¹ ^ 3 = phi⁻¹ ^ 2 * phi⁻¹ := by ring
  rw [e, phi_inv2, phi_inv_lin]; linear_combination (-1 : ℝ) * phi_sq

/-- `φ⁻⁵ = 5φ − 8`. -/
theorem phi_inv5 : phi⁻¹ ^ 5 = 5 * phi - 8 := by
  have e : phi⁻¹ ^ 5 = phi⁻¹ ^ 3 * phi⁻¹ ^ 2 := by ring
  rw [e, phi_inv3, phi_inv2]; linear_combination (-2 : ℝ) * phi_sq

/-- `φ⁻⁶ = 13 − 8φ`. -/
theorem phi_inv6 : phi⁻¹ ^ 6 = 13 - 8 * phi := by
  have e : phi⁻¹ ^ 6 = phi⁻¹ ^ 3 * phi⁻¹ ^ 3 := by ring
  rw [e, phi_inv3]; linear_combination (4 : ℝ) * phi_sq

/-- `α_top⁻¹ = 359 φ⁻² − φ⁻⁵ = 726 − 364 φ`. -/
theorem alphaTop_exact : 359 * phi⁻¹ ^ 2 - phi⁻¹ ^ 5 = 726 - 364 * phi := by
  rw [phi_inv2, phi_inv5]; ring

/-- `α_alg⁻¹ = 2¹¹·(6/5)φ²·φ⁻⁸ + (2/3)·(1/2)φ⁻³ = 159739/5 − (294902/15) φ`. -/
theorem alphaAlg_exact :
    2048 * ((6 / 5) * phi ^ 2) * phi⁻¹ ^ 8 + (2 / 3) * ((1 / 2) * phi⁻¹ ^ 3)
      = 159739 / 5 - 294902 / 15 * phi := by
  have h22 : phi ^ 2 * phi⁻¹ ^ 2 = 1 := by
    rw [← mul_pow, mul_inv_cancel₀ hne, one_pow]
  have key : phi ^ 2 * phi⁻¹ ^ 8 = phi⁻¹ ^ 6 := by
    have e8 : phi⁻¹ ^ 8 = phi⁻¹ ^ 2 * phi⁻¹ ^ 6 := by ring
    rw [e8, ← mul_assoc, h22, one_mul]
  have e : 2048 * ((6 / 5) * phi ^ 2) * phi⁻¹ ^ 8 = (12288 / 5) * (phi ^ 2 * phi⁻¹ ^ 8) := by ring
  rw [e, key, phi_inv6, phi_inv3]; ring

/-- **D0-DELTA-ALPHA-EXACT-001.** The gluing anomaly is the exact `Q(φ)` element
`Δ_α = α_top⁻¹ − α_alg⁻¹ = −156109/5 + (289442/15) φ`. -/
theorem delta_alpha_exact :
    (359 * phi⁻¹ ^ 2 - phi⁻¹ ^ 5)
      - (2048 * ((6 / 5) * phi ^ 2) * phi⁻¹ ^ 8 + (2 / 3) * ((1 / 2) * phi⁻¹ ^ 3))
      = -156109 / 5 + 289442 / 15 * phi := by
  rw [alphaTop_exact, alphaAlg_exact]; ring

end D0.Spectral
