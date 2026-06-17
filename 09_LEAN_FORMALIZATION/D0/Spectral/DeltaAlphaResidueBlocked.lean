import D0.Core.Phi
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.RingTheory.Algebraic.Integral
import Mathlib.Tactic

/-!
# D0-CVFT-F1 — the ζ-residue route to `Δα` is closed-negative (transcendental obstruction)

The CVFT-F1 program proposed to obtain the algebraic gluing anomaly `Δα ∈ ℚ(φ)` as the `s→pole`
residue of a `φ`-graded spectral zeta function. A `φ`-graded residue carries `ln φ`
(`Res ∝ 1/ln φ`). This module proves that route **cannot** close: `1/ln φ` is transcendental over
ℚ, whereas every element `a + b·φ` of `ℚ(φ)` — where `Δα` and `α_alg` live — is algebraic. Hence
no `φ`-graded residue can equal the algebraic anomaly, and the residue route is a closed-negative
no-go. The working route to the 9-digit `α` is the closure holonomy (`D0-ALPHA-HOLONOMY-002`).

## The one cited external fact (ASSUMP-LINDEMANN-LNPHI)

The transcendence of `ln φ` over ℚ is the Lindemann–Weierstrass theorem (for an algebraic `φ ≠ 1`,
`ln φ` is transcendental). Mathlib 4.30 formalizes only the **analytic part** of L–W
(`Mathlib.NumberTheory.Transcendental.Lindemann.AnalyticalPart`, `exp_polynomial_approx`); the full
theorem is not assembled. So this is carried as one explicit, named **hypothesis**
(`LindemannLnPhi`), threaded into every theorem below — never as a global `axiom`. Everything else
(`φ` algebraic, `ℚ(φ)` algebraic, inverse-transcendence) is proved here from `φ² = φ + 1`.

Cert: `05_CERTS/vp_feshbach_residue_amplitudes.py` (BLOCKED block).
-/

namespace D0.Spectral

open D0 Polynomial

/-- **ASSUMP-LINDEMANN-LNPHI** — the single cited classical fact: `ln φ` is transcendental over ℚ
(Lindemann–Weierstrass). Carried as an explicit hypothesis, not a global axiom; Mathlib 4.30 has
only the analytic half of L–W. -/
def LindemannLnPhi : Prop := Transcendental ℚ (Real.log phi)

/-- `φ` is algebraic over ℚ: it is a root of the nonzero polynomial `X² − X − 1` (`φ² = φ + 1`). -/
theorem isAlgebraic_phi : IsAlgebraic ℚ phi := by
  refine ⟨X ^ 2 - X - 1, ?_, ?_⟩
  · intro hzero
    apply_fun (fun p => Polynomial.coeff p 2) at hzero
    simp [coeff_X_pow, coeff_X, coeff_one] at hzero
  · simp only [map_sub, map_pow, aeval_X, map_one]
    linear_combination phi_sq

/-- Every element `a + b·φ` of `ℚ(φ)` is algebraic over ℚ (rationals + `φ` are integral over ℚ,
and integral elements are closed under `+` and `*`). -/
theorem qphi_isAlgebraic (a b : ℚ) : IsAlgebraic ℚ ((a : ℝ) + b * phi) := by
  have hphi : IsIntegral ℚ phi := isAlgebraic_phi.isIntegral
  have ha : IsIntegral ℚ ((a : ℝ)) := (isAlgebraic_rat ℚ a).isIntegral
  have hb : IsIntegral ℚ ((b : ℝ)) := (isAlgebraic_rat ℚ b).isIntegral
  exact (ha.add (hb.mul hphi)).isAlgebraic

/-- Given the cited transcendence of `ln φ`, the residue value `1/ln φ` is itself transcendental
over ℚ (algebraicity is preserved by inversion, so `(ln φ)⁻¹` algebraic would force `ln φ`
algebraic). -/
theorem inv_log_phi_transcendental (hLW : LindemannLnPhi) :
    Transcendental ℚ (Real.log phi)⁻¹ := by
  have h : ¬ IsAlgebraic ℚ (Real.log phi) := hLW
  exact IsAlgebraic.inv_iff.not.mpr h

/-- **D0-CVFT-F1 — closed-negative.** A `φ`-graded ζ-residue carries the transcendental factor
`1/ln φ`, so it is never equal to any `a + b·φ ∈ ℚ(φ)`; the algebraic anomaly `Δα ∈ ℚ(φ)` therefore
cannot be obtained from such a residue. Proved relative to the one cited fact
`ASSUMP-LINDEMANN-LNPHI`; the working route to `α` is the closure holonomy (D0-ALPHA-HOLONOMY-002). -/
theorem delta_alpha_residue_route_blocked (hLW : LindemannLnPhi) (a b : ℚ) :
    (Real.log phi)⁻¹ ≠ (a : ℝ) + b * phi := by
  intro heq
  have htr : Transcendental ℚ (Real.log phi)⁻¹ := inv_log_phi_transcendental hLW
  rw [heq] at htr
  exact htr (qphi_isAlgebraic a b)

end D0.Spectral
