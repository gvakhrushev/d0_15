import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# D0-IM-COSMO-003 — strong logdet pressure coupling (response positivity)

BOOK_08. Python certificate: `05_CERTS/vp_strong_logdet_pressure_coupling.py` (symbolic).

With the volume ratio `r(V) = 1 − e^{−kV}` and loop term `L(V) = −d_τ·log(1 − z·r(V))`, the closed-form
response is `dL/dV = d_τ·z·k·e^{−kV} / (1 − z·r(V))`. On the resolvent domain (`1 − z·r(V) > 0`) with
positive `d_τ, z` and rate `k = log φ > 0`, this is a quotient of strictly-positive numerator over
strictly-positive denominator, hence `> 0`; at `z = 0` it degenerates to exactly `0` (the cert's
negative control).

This module machine-checks the closed-form positivity (and `k = log φ > 0`). The calculus step that
`dL/dV` equals this closed form, and the resolvent-domain bookkeeping, stay in the cert.
-/

namespace D0.IM

open D0

/-- The contraction rate `κ = log φ > 0`. -/
noncomputable def slpKappa : ℝ := Real.log phi

/-- `κ = log φ > 0` (since `φ > 1`). -/
theorem slpKappa_pos : 0 < slpKappa := Real.log_pos phi_gt_one

/-- Volume ratio `r(V) = 1 − e^{−kV}`. -/
noncomputable def slpR (k V : ℝ) : ℝ := 1 - Real.exp (-(k * V))

/-- Closed-form loop-pressure response `dL/dV`. -/
noncomputable def slpDeriv (k d_tau z V : ℝ) : ℝ :=
  d_tau * z * k * Real.exp (-(k * V)) / (1 - z * slpR k V)

/-- **Response positivity:** on the resolvent domain, `dL/dV > 0` for positive `k, d_τ, z`. -/
theorem slp_derivative_pos (k d_tau z V : ℝ) (hk : 0 < k) (hd : 0 < d_tau) (hz : 0 < z)
    (hdom : 0 < 1 - z * slpR k V) : 0 < slpDeriv k d_tau z V := by
  unfold slpDeriv
  apply div_pos _ hdom
  exact mul_pos (mul_pos (mul_pos hd hz) hk) (Real.exp_pos _)

/-- **Negative control:** at `z = 0` the response degenerates to exactly `0`. -/
theorem slp_z_zero_degenerate (k d_tau V : ℝ) : slpDeriv k d_tau 0 V = 0 := by
  unfold slpDeriv; simp

/-- **D0-IM-COSMO-003.** `κ = log φ > 0`; the closed-form logdet pressure response is strictly positive
on the resolvent domain for positive couplings, and degenerates to `0` at `z = 0`. -/
theorem strong_logdet_pressure_coupling :
    0 < slpKappa ∧
    (∀ k d_tau z V : ℝ, 0 < k → 0 < d_tau → 0 < z → 0 < 1 - z * slpR k V →
      0 < slpDeriv k d_tau z V) ∧
    (∀ k d_tau V : ℝ, slpDeriv k d_tau 0 V = 0) :=
  ⟨slpKappa_pos, slp_derivative_pos, slp_z_zero_degenerate⟩

end D0.IM
