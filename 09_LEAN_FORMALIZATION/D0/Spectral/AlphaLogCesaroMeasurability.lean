import D0.Spectral.DeltaAlphaResidueBlocked
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001 — ROOT R5

The forced profinite weight is `φ^{-3N}` (`D0-ALPHA-PROFINITE-SPECTRAL-TOWER-OWNER-001`). At the critical
rate `a = 3` the per-block mass is constant (`φ³·φ^{-3} = 1`, `rate_three_eq_one` of the alpha maximality
no-go), so the ordinary log-Cesàro (Dixmier) limit of the singular values is
`lim_{K→∞} (1/log(1+K)) Σ_{j≤K} s_j = 1/(3·log φ)`.

This value is `(log φ)⁻¹/3`, a nonzero `ℚ(φ)`-multiple of `(log φ)⁻¹`, hence transcendental over ℚ
(Lindemann–Weierstrass, the single cited fact `ASSUMP-LINDEMANN-LNPHI`), so it can never equal the rational
moment `μ₂ = 12288/5`. Therefore no frozen carrier realizes the ordinary Dixmier limit `= μ₂`; the positive
realization stays the external `D0-EXTERNAL-DIXMIER-WODZICKI-PASSPORT-001`. This is the a=3 limit-VALUE
transcendence corollary of `D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001`, reusing `D0-CVFT-F1`
(`delta_alpha_residue_route_blocked`); it does not re-derive `rate_three_eq_one` or the transcendence lemmas.
-/

namespace D0.Spectral.AlphaLogCesaroMeasurability

open D0 D0.Spectral

theorem one_lt_phi : (1 : ℝ) < phi := by
  have h2 : (2 : ℝ) < Real.sqrt 5 := by nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]
  rw [show phi = (1 + Real.sqrt 5) / 2 from rfl]; linarith

/-- **D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001.** Given the cited transcendence of `log φ`
(`ASSUMP-LINDEMANN-LNPHI`), the a=3 ordinary log-Cesàro limit `1/(3·log φ)` is never the rational moment
`μ₂ = 12288/5`. -/
theorem alpha_log_cesaro_ne_mu2 (hLW : LindemannLnPhi) :
    (1 : ℝ) / (3 * Real.log phi) ≠ (12288 / 5 : ℝ) := by
  intro h
  have hpos : 0 < Real.log phi := Real.log_pos one_lt_phi
  have hne : Real.log phi ≠ 0 := ne_of_gt hpos
  -- 1/(3 log φ) = 12288/5  ⟹  (log φ)⁻¹ = 36864/5 = 36864/5 + 0·φ ∈ ℚ(φ)
  have e2 : (Real.log phi)⁻¹ = (36864 / 5 : ℝ) := by
    field_simp at h ⊢
    linarith [h]
  have e : (Real.log phi)⁻¹ = ((36864 / 5 : ℚ) : ℝ) + ((0 : ℚ) : ℝ) * phi := by
    push_cast; rw [e2]; ring
  exact delta_alpha_residue_route_blocked hLW (36864 / 5) 0 e

end D0.Spectral.AlphaLogCesaroMeasurability
