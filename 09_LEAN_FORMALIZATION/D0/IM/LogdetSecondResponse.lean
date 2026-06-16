import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# D0-IM-COSMO-004 — logdet second response and stability (sign-corrected)

BOOK_08. Python certificate: `05_CERTS/vp_logdet_second_response_and_stability.py` (symbolic).

With `L(V) = −d_τ·log(1 − z·r(V))`, `r = 1 − e^{−kV}`, the closed forms are
`L'(V) = d_τ·z·k·e^{−kV} / D` and `L''(V) = d_τ·z·k²·e^{−kV}·(z−1) / D²` with `D = 1 − z + z·e^{−kV}`.
For `0 < z < 1` (and `k, d_τ > 0`): `D > 0` (so the first response is strictly positive), while `L''`
carries the strictly-negative factor `(z−1)` over a positive `D²`, so the second response is strictly
negative — the sign-corrected stability statement.

This module machine-checks both signs from the closed forms; the derivative-identity calculus and the
`V→∞` asymptotics stay in the cert.
-/

namespace D0.IM

open D0

/-- The positive denominator `D = 1 − z + z·e^{−kV}` (`0 < z < 1`). -/
noncomputable def lsrDen (k z V : ℝ) : ℝ := 1 - z + z * Real.exp (-(k * V))

/-- `D > 0` for `0 < z < 1`. -/
theorem lsr_den_pos (k z V : ℝ) (hz0 : 0 < z) (hz1 : z < 1) : 0 < lsrDen k z V := by
  unfold lsrDen
  have he : 0 < z * Real.exp (-(k * V)) := mul_pos hz0 (Real.exp_pos _)
  linarith

/-- **First response strictly positive:** `L'(V) > 0`. -/
theorem lsr_first_response_pos (k d_tau z V : ℝ) (hk : 0 < k) (hd : 0 < d_tau)
    (hz0 : 0 < z) (hz1 : z < 1) :
    0 < d_tau * z * k * Real.exp (-(k * V)) / lsrDen k z V := by
  apply div_pos _ (lsr_den_pos k z V hz0 hz1)
  exact mul_pos (mul_pos (mul_pos hd hz0) hk) (Real.exp_pos _)

/-- **Second response strictly negative (stability, sign-corrected):** `L''(V) < 0`. -/
theorem lsr_second_response_neg (k d_tau z V : ℝ) (hk : 0 < k) (hd : 0 < d_tau)
    (hz0 : 0 < z) (hz1 : z < 1) :
    d_tau * z * k ^ 2 * Real.exp (-(k * V)) * (z - 1) / (lsrDen k z V) ^ 2 < 0 := by
  apply div_neg_of_neg_of_pos
  · have hnum : 0 < d_tau * z * k ^ 2 * Real.exp (-(k * V)) := by positivity
    exact mul_neg_of_pos_of_neg hnum (by linarith)
  · exact pow_pos (lsr_den_pos k z V hz0 hz1) 2

/-- **D0-IM-COSMO-004.** For `0 < z < 1` and positive `k, d_τ`: the first logdet response is strictly
positive and the second response is strictly negative (the sign-corrected stability law). -/
theorem logdet_second_response_stability_sign_corrected :
    (∀ k d_tau z V : ℝ, 0 < k → 0 < d_tau → 0 < z → z < 1 →
      0 < d_tau * z * k * Real.exp (-(k * V)) / lsrDen k z V) ∧
    (∀ k d_tau z V : ℝ, 0 < k → 0 < d_tau → 0 < z → z < 1 →
      d_tau * z * k ^ 2 * Real.exp (-(k * V)) * (z - 1) / (lsrDen k z V) ^ 2 < 0) :=
  ⟨lsr_first_response_pos, lsr_second_response_neg⟩

end D0.IM
