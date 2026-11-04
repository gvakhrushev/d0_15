import D0.Analysis.MatrixRelativeLogDetBound
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-!
# Log-scale derivative of the return price

The scalar and matrix forms of the fixed-history price/gain identity in §5,
line 199, of the #334 task-faithful source at owner commit
`fd35893d77e4aa5f819bafa0c6428c8e7a8f1812` (source blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`). A positive offset and a
nonnegative finite spectrum suffice; zero eigenvalues are permitted.

This is differentiation along a scalar reference scale with fixed history.
It is not a derivative estimate for an approximate native compiler, an
admission or smoothness statement, or a selection of a physical source.
-/

noncomputable section

namespace D0.Analysis.ReturnPriceLogScaleDerivative

open D0.Analysis.RelativeLogDetScaleBound D0.Analysis
open scoped ComplexOrder

variable {ι : Type*} [Fintype ι]

/-- For a fixed spectrum, minus the price derivative in log scale is the
gain of that same spectrum at that same scale. -/
theorem finiteSpectralPrice_hasDerivAt_logScale
    (a : ℝ) (eigenvalue : ι → ℝ) (t : ℝ)
    (ha : 0 < a) (hvalue : ∀ i, 0 ≤ eigenvalue i) :
    HasDerivAt (fun s => finiteSpectralPrice a eigenvalue (Real.exp s))
      (-finiteSpectralGain a eigenvalue (Real.exp t)) t := by
  classical
  have hterm : ∀ i, HasDerivAt
      (fun s => Real.log (a + Real.exp s * eigenvalue i))
      (Real.exp t * eigenvalue i / (a + Real.exp t * eigenvalue i)) t := by
    intro i
    have hpositive : 0 < a + Real.exp t * eigenvalue i := by
      exact add_pos_of_pos_of_nonneg ha (mul_nonneg (Real.exp_pos t).le (hvalue i))
    have h := ((hasDerivAt_const t a).add
      ((Real.hasDerivAt_exp t).mul_const (eigenvalue i))).log (ne_of_gt hpositive)
    simpa using h
  have hsum := (HasDerivAt.fun_sum (u := Finset.univ) (fun i _ => hterm i)).neg
  simpa only [finiteSpectralPrice, finiteSpectralGain] using hsum

/-- Matrix application: the fixed PSD history, including a singular or zero
history, has exactly the same log-scale price derivative and trace gain. -/
theorem regularizedReturnPrice_hasDerivAt_logScale
    {n : Type*} [Fintype n] [DecidableEq n]
    (S : Matrix n n ℂ) (hS : S.PosSemidef) (a t : ℝ) (ha : 0 < a) :
    HasDerivAt (fun s => regularizedReturnPrice a ((Real.exp s : ℂ) • S))
      (-regularizedReturnGain a ((Real.exp t : ℂ) • S)) t := by
  have h := finiteSpectralPrice_hasDerivAt_logScale a hS.isHermitian.eigenvalues t
    ha hS.eigenvalues_nonneg
  have hp : (fun s => regularizedReturnPrice a ((Real.exp s : ℂ) • S)) =
      (fun s => finiteSpectralPrice a hS.isHermitian.eigenvalues (Real.exp s)) := by
    funext s
    exact regularizedReturnPrice_smul_spectral S hS a (Real.exp s) ha (Real.exp_pos s).le
  rw [hp, regularizedReturnGain_smul_spectral S hS a (Real.exp t) ha (Real.exp_pos t).le]
  exact h

end D0.Analysis.ReturnPriceLogScaleDerivative
