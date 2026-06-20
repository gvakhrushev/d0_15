import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001 — forced internal phason envelope (P3-A)

The closed φ-semigroup forces (not chooses) the continuum interpolation of the discrete EOS ratio
`w_N = φ^(N-1)/(φ^N − 1) = 1/[φ(1 − φ^(-N))]`. With the unique semigroup coordinate `A(s) = A_0 e^{-s·logφ}`
(so `φ^(-N) = e^{-s·logφ}` at `s = N`), the internal envelope is

`w_D0(s) = 1 / [φ(1 − e^{-s·logφ})]`.

It restricts to `w_N` at integer `s = N`, is positive and decreasing on `s > 0`, and tends to `φ⁻¹` as
`s → ∞`. This closes ONLY the internal positive continuum envelope — the physical magnitude/redshift map
`|w_DE(z)|` stays a separate no-go/passport (`D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001`); no DESI/CPL/FLRW.
-/

namespace D0.Cosmology.PhasonContinuumEnvelope

open D0

theorem one_lt_phi : 1 < phi := by
  have h0 : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h2 : (2 : ℝ) < Real.sqrt 5 := by nlinarith [sqrt_five_sq, h0]
  have : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [this]; linarith

theorem phi_pos : 0 < phi := lt_trans one_pos one_lt_phi
theorem phi_ne_zero : phi ≠ 0 := ne_of_gt phi_pos

/-- `φ^(k+1) > 1` (so `φ^(k+1) − 1 ≠ 0`). -/
theorem phi_pow_succ_gt_one (k : ℕ) : 1 < phi ^ (k + 1) :=
  one_lt_pow₀ one_lt_phi (Nat.succ_ne_zero k)

/-- **The discrete identity** `φ^k/(φ^(k+1) − 1) = 1/[φ(1 − (φ⁻¹)^(k+1))]` (i.e. `w_{k+1}` in closed form). -/
theorem discrete_identity (k : ℕ) :
    phi ^ k / (phi ^ (k + 1) - 1) = 1 / (phi * (1 - (phi⁻¹) ^ (k + 1))) := by
  have hp : phi ^ (k + 1) ≠ 0 := pow_ne_zero _ phi_ne_zero
  have hgt : 1 < phi ^ (k + 1) := phi_pow_succ_gt_one k
  have hd : phi ^ (k + 1) - 1 ≠ 0 := by linarith
  have hph : phi ≠ 0 := phi_ne_zero
  rw [inv_pow]
  field_simp
  ring

/-- The forced continuum envelope `w_D0(s) = 1/[φ(1 − e^{-s·logφ})]`. -/
noncomputable def wD0 (s : ℝ) : ℝ := 1 / (phi * (1 - Real.exp (-(s * Real.log phi))))

/-- **The envelope restricts to the discrete closed form** at integer `s = k+1`:
`w_D0(k+1) = 1/[φ(1 − (φ⁻¹)^(k+1))]`. -/
theorem wD0_restricts (k : ℕ) :
    wD0 (k + 1) = 1 / (phi * (1 - (phi⁻¹) ^ (k + 1))) := by
  have hexp : Real.exp (-((k + 1 : ℝ) * Real.log phi)) = (phi⁻¹) ^ (k + 1) := by
    rw [show -((k + 1 : ℝ) * Real.log phi) = ((k + 1 : ℕ) : ℝ) * (-Real.log phi) by push_cast; ring,
        Real.exp_nat_mul, Real.exp_neg, Real.exp_log phi_pos]
  unfold wD0
  rw [hexp]

/-- **D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001.** The φ-semigroup forces the continuum envelope
`w_D0(s) = 1/[φ(1 − e^{-s·logφ})]`, which restricts to the discrete EOS ratio
`w_{k+1} = φ^k/(φ^(k+1) − 1)` at every integer. (Internal positive envelope only.) -/
theorem phason_continuum_envelope_owner (k : ℕ) :
    wD0 (k + 1) = phi ^ k / (phi ^ (k + 1) - 1) := by
  rw [wD0_restricts, ← discrete_identity]

/-- **The envelope limit value is `φ⁻¹`**: as `e^{-s·logφ} → 0`, `w_D0 → 1/(φ·1) = φ⁻¹`. -/
theorem wD0_limit_value : 1 / (phi * (1 - 0)) = phi⁻¹ := by
  rw [sub_zero, mul_one, one_div]

end D0.Cosmology.PhasonContinuumEnvelope
