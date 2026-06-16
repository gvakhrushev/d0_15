import D0.Gravity.HorizonJetAndBaryonPole
import Mathlib.Tactic

/-!
# D0-GRAV-005 — optical jet backreaction (emission PSD + axial dominance)

BOOK_07. Python certificate: `05_CERTS/vp_optical_jet_backreaction.py`.

The optical-jet emission operator `Femit = Q Uᴴ P U Q` is symmetric and positive semidefinite (the
conjugate-emission law, reused from `HorizonJetAndBaryonPole`), and the axial backreaction strictly
exceeds the transverse one: `J_axis = s₁² > s₂² = J_trans` whenever the axial rotation `s₁` exceeds the
transverse `s₂ ≥ 0`.

This module machine-checks the symmetric+PSD structure (`U`-generic) and the strict backreaction
inequality (angle-agnostic). The cert's specific angles `θ₁=0.7, θ₂=0.2` and the physical jet
identification stay cert.
-/

namespace D0.Gravity

open Matrix

/-- The emission operator is symmetric (Hermitian over ℝ), being positive semidefinite. -/
theorem optical_emission_symmetric {n : ℕ} (P U : Matrix (Fin n) (Fin n) ℝ)
    (hPh : Pᴴ = P) (hPP : P * P = P) :
    ((1 - P) * Uᴴ * P * U * (1 - P))ᴴ = (1 - P) * Uᴴ * P * U * (1 - P) :=
  (horizon_jet_baryon_pole_layer_cert P U hPh hPP).isHermitian

/-- **Axial dominance:** for `0 ≤ s₂ < s₁`, the axial backreaction `s₁²` strictly exceeds `s₂²`. -/
theorem optical_backreaction_strict (s1 s2 : ℝ) (h2 : 0 ≤ s2) (h21 : s2 < s1) : s2 ^ 2 < s1 ^ 2 := by
  nlinarith [h2, h21]

/-- **D0-GRAV-005.** The optical-jet emission operator is symmetric and PSD (any orthogonal `U`,
projector `P`), and axial backreaction strictly dominates transverse (`s₂² < s₁²` for `0 ≤ s₂ < s₁`). -/
theorem optical_jet_backreaction_cert :
    (∀ {n : ℕ} (P U : Matrix (Fin n) (Fin n) ℝ), Pᴴ = P → P * P = P →
      ((1 - P) * Uᴴ * P * U * (1 - P)).PosSemidef) ∧
    (∀ s1 s2 : ℝ, 0 ≤ s2 → s2 < s1 → s2 ^ 2 < s1 ^ 2) :=
  ⟨fun P U hPh hPP => horizon_jet_baryon_pole_layer_cert P U hPh hPP, optical_backreaction_strict⟩

end D0.Gravity
