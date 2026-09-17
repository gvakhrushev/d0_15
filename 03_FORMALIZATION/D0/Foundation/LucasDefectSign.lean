import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Tactic

/-!
# D0-LUCAS-DEFECT-SIGN-001 (THE) — the integer-approximation defect of `φⁿ`

With `φ=(1+√5)/2`, `ψ=(1−√5)/2`, `Lₙ := φⁿ+ψⁿ` (Lucas), the defect of `φⁿ` from its nearest integer `Lₙ` is
`φⁿ − Lₙ = (−1)^{n+1}·(φⁿ)⁻¹`. Hence `sgn(φⁿ−Lₙ) = (−1)^{n+1}`: the defect is **positive iff `n` is odd**, so
it is constant in sign exactly along arithmetic runs of fixed parity. Physics-free (Vieta + `φ>0`); used by the
`+2`-step parity argument (`SceneStepParity`).
-/

namespace D0.Foundation.LucasDefectSign

open Real
open scoped goldenRatio

/-- Lucas-number real form `Lₙ = φⁿ + ψⁿ`. -/
noncomputable def lucasR (n : ℕ) : ℝ := φ ^ n + ψ ^ n

/-- **The defect identity** `φⁿ − Lₙ = (−1)^{n+1}·(φⁿ)⁻¹` (via `ψ = −φ⁻¹`). -/
theorem lucas_defect (n : ℕ) : φ ^ n - lucasR n = (-1) ^ (n + 1) * (φ ^ n)⁻¹ := by
  have hψ : ψ = -φ⁻¹ := by rw [inv_goldenRatio]; ring
  unfold lucasR
  rw [hψ, neg_pow, inv_pow, pow_succ]
  ring

/-- `φⁿ > 0`. -/
theorem phi_pow_pos (n : ℕ) : 0 < φ ^ n := pow_pos goldenRatio_pos n

/-- **The defect sign** `sgn(φⁿ − Lₙ) = (−1)^{n+1}`: the defect is positive iff `n` is odd. -/
theorem lucas_defect_sign (n : ℕ) : 0 < φ ^ n - lucasR n ↔ Odd n := by
  rw [lucas_defect]
  have hpos : 0 < (φ ^ n)⁻¹ := inv_pos.mpr (phi_pow_pos n)
  rw [mul_pos_iff_of_pos_right hpos]
  constructor
  · intro h
    rcases Nat.even_or_odd n with he | ho
    · exfalso; rcases he with ⟨k, hk⟩; subst hk
      have : (-1 : ℝ) ^ (k + k + 1) = -1 := by
        rw [show k + k + 1 = 2 * k + 1 by ring, pow_succ, pow_mul]; norm_num
      rw [this] at h; linarith
    · exact ho
  · intro ho
    rcases ho with ⟨k, hk⟩; subst hk
    have : (-1 : ℝ) ^ (2 * k + 1 + 1) = 1 := by
      rw [show 2 * k + 1 + 1 = 2 * (k + 1) by ring, pow_mul]; norm_num
    rw [this]; norm_num

/-- **D0-LUCAS-DEFECT-SIGN-001.** The defect identity and its parity-keyed sign. -/
theorem lucas_defect_sign_main (n : ℕ) :
    φ ^ n - lucasR n = (-1) ^ (n + 1) * (φ ^ n)⁻¹ ∧ (0 < φ ^ n - lucasR n ↔ Odd n) :=
  ⟨lucas_defect n, lucas_defect_sign n⟩

end D0.Foundation.LucasDefectSign
