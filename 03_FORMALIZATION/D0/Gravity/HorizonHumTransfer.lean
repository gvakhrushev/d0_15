import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-HORIZON-HUM-TRANSFER-OBSERVABLE-OWNER-001 — horizon-hum target `I_f = log φ` (Lane H2)

Frozen internal target: the horizon information rate `I_f = log φ` (golden Lyapunov/return rate of the
finite feedback geometry). It is a pure dimensionless number with `0 < I_f < 1` and the golden identity
`2·I_f = log(φ+1)` (since `φ² = φ+1`). The empirical use is a TRANSFER-CORRECTED residual protocol
(`D0-HORIZON-HUM-EMPIRICAL-PASSPORT-001`), NOT a raw frequency-ratio hunt and NOT a LIGO confirmation:
no event chooses the target, the time-frequency window is frozen before data, detector-frame `φ` artifacts
are negative controls. EMPIRICAL-PASSPORT, never CORE.
-/

namespace D0.Gravity.HorizonHumTransfer

open D0

theorem one_lt_phi : 1 < phi := by
  have h0 : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h2 : (2 : ℝ) < Real.sqrt 5 := by nlinarith [sqrt_five_sq, h0]
  have : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [this]; linarith

theorem phi_pos : 0 < phi := lt_trans one_pos one_lt_phi

theorem phi_lt_two : phi < 2 := by
  have h0 : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h3 : Real.sqrt 5 < 3 := by nlinarith [sqrt_five_sq, h0]
  have : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [this]; linarith

/-- Golden identity `φ² = φ + 1`. -/
theorem golden : phi ^ 2 = phi + 1 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := sqrt_five_sq
  have : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [this]; nlinarith [h5]

/-- Horizon information rate `I_f = log φ`. -/
noncomputable def Ihum : ℝ := Real.log phi

/-- **The target is positive**: `0 < I_f`. -/
theorem hum_pos : 0 < Ihum := Real.log_pos one_lt_phi

/-- **The target is below one**: `I_f < 1` (since `φ < 2 < e`). -/
theorem hum_lt_one : Ihum < 1 := by
  have h2e : (2 : ℝ) < Real.exp 1 := by
    have := Real.add_one_lt_exp (x := (1 : ℝ)) (by norm_num); linarith
  have hpe : phi < Real.exp 1 := lt_trans phi_lt_two h2e
  have : Real.log phi < Real.log (Real.exp 1) := Real.log_lt_log phi_pos hpe
  rwa [Real.log_exp] at this

/-- **Golden identity for the target**: `2·I_f = log(φ+1)`. -/
theorem hum_double_eq : 2 * Ihum = Real.log (phi + 1) := by
  unfold Ihum
  rw [← golden, Real.log_pow]; push_cast; ring

/-- **The target is the negated log of the inverse rate**: `I_f = −log(φ⁻¹)`. -/
theorem hum_eq_neg_log_inv : Ihum = -Real.log (phi⁻¹) := by
  unfold Ihum; rw [Real.log_inv]; ring

/-- **D0-HORIZON-HUM-TRANSFER-OBSERVABLE-OWNER-001.** The frozen horizon-hum target `I_f = log φ` is a
dimensionless number with `0 < I_f < 1` and the golden identity `2·I_f = log(φ+1)`. -/
theorem horizon_hum_transfer_owner :
    0 < Ihum ∧ Ihum < 1 ∧ 2 * Ihum = Real.log (phi + 1) :=
  ⟨hum_pos, hum_lt_one, hum_double_eq⟩

end D0.Gravity.HorizonHumTransfer
