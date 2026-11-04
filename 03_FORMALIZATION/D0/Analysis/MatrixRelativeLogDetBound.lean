import D0.Analysis.PositiveMatrixLogDet
import D0.Analysis.RelativeLogDetScaleBound

/-!
# Relative logdet error from a full Gram-operator sandwich

The perturbed operator need not commute with the reference. Both are compared
in positive-semidefinite order; only the two scalar bounds are diagonalized
in the reference's spectral basis. The coefficient is the actual resolvent
trace of that reference. Singular and zero reference operators are allowed.
-/

noncomputable section

namespace D0.Analysis

open PositiveMatrixLogDet RelativeLogDetScaleBound
open scoped ComplexOrder

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The original negative log determinant with a positive identity offset. -/
def regularizedReturnPrice (a : ℝ) (S : Matrix n n ℂ) : ℝ :=
  -Real.log ((affinePencil S a 1).det.re)

/-- The gain of the same price and the same reference operator. -/
def regularizedReturnGain (a : ℝ) (S : Matrix n n ℂ) : ℝ :=
  ((S * (affinePencil S a 1)⁻¹).trace).re

theorem regularizedReturnPrice_smul_spectral
    (S : Matrix n n ℂ) (hS : S.PosSemidef) (a q : ℝ)
    (ha : 0 < a) (hq : 0 ≤ q) :
    regularizedReturnPrice a ((q : ℂ) • S) =
      finiteSpectralPrice a hS.isHermitian.eigenvalues q := by
  have hp : affinePencil ((q : ℂ) • S) a 1 = affinePencil S a q := by
    simp [affinePencil]
  simp only [regularizedReturnPrice, hp, affinePencil_logdet S hS ha hq,
    finiteSpectralPrice]

theorem regularizedReturnGain_smul_spectral
    (S : Matrix n n ℂ) (hS : S.PosSemidef) (a q : ℝ)
    (ha : 0 < a) (hq : 0 ≤ q) :
    regularizedReturnGain a ((q : ℂ) • S) =
      finiteSpectralGain a hS.isHermitian.eigenvalues q := by
  have hp : affinePencil ((q : ℂ) • S) a 1 = affinePencil S a q := by
    simp [affinePencil]
  simpa only [regularizedReturnGain, hp, finiteSpectralGain] using
    affinePencil_trace_resolvent S hS ha hq

/-- Scalar comparison of the actual matrix price and its actual trace gain. -/
theorem regularizedReturnPrice_exp_bound
    (S : Matrix n n ℂ) (hS : S.PosSemidef) (a t η : ℝ)
    (ha : 0 < a) (hη : 0 ≤ η) (ht : |t| ≤ 2 * η) :
    |regularizedReturnPrice a ((Real.exp t : ℂ) • S) - regularizedReturnPrice a S| ≤
      (Real.exp (2 * η) - 1) * regularizedReturnGain a S := by
  have hp := regularizedReturnPrice_smul_spectral S hS a 1 ha (by norm_num)
  have hg := regularizedReturnGain_smul_spectral S hS a 1 ha (by norm_num)
  simp only [Complex.ofReal_one, one_smul] at hp hg
  rw [regularizedReturnPrice_smul_spectral S hS a (Real.exp t) ha (Real.exp_pos _).le,
    hp, hg]
  exact finiteSpectralPrice_exp_bound a _ t η ha hS.eigenvalues_nonneg hη ht

/-- Full noncommuting matrix price error, from the Gram-operator inequalities.
No inverse or spectral gap of `S` is used. -/
theorem regularizedReturnPrice_sandwich_bound
    (S H : Matrix n n ℂ) (hS : S.PosSemidef) (hH : H.PosSemidef)
    (a η : ℝ) (ha : 0 < a) (hη : 0 ≤ η)
    (hlower : (H - (Real.exp (-2 * η) : ℂ) • S).PosSemidef)
    (hupper : ((Real.exp (2 * η) : ℂ) • S - H).PosSemidef) :
    |regularizedReturnPrice a H - regularizedReturnPrice a S| ≤
      (Real.exp (2 * η) - 1) * regularizedReturnGain a S := by
  have hlow := logdet_mono_of_posDef
    (affinePencil_posDef S hS ha (Real.exp_pos (-2 * η)).le)
    (B := affinePencil H a 1) (by
      simpa [affinePencil, add_sub_add_left_eq_sub] using hlower)
  have hupp := logdet_mono_of_posDef
    (affinePencil_posDef H hH ha (show (0 : ℝ) ≤ 1 by norm_num))
    (B := affinePencil S a (Real.exp (2 * η))) (by
      simpa [affinePencil, add_sub_add_left_eq_sub] using hupper)
  have hlowB := regularizedReturnPrice_exp_bound S hS a (-2 * η) η ha hη (by
    rw [show -2 * η = -(2 * η) by ring, abs_neg, abs_of_nonneg (by positivity)])
  have huppB := regularizedReturnPrice_exp_bound S hS a (2 * η) η ha hη (by
    rw [abs_of_nonneg (by positivity)])
  have hpencil (q : ℝ) : affinePencil ((q : ℂ) • S) a 1 = affinePencil S a q := by
    simp [affinePencil]
  simp only [regularizedReturnPrice, hpencil] at hlowB huppB ⊢
  have hb1 := (abs_le.mp hlowB).2
  have hb2 := (abs_le.mp huppB).1
  exact abs_le.mpr ⟨by linarith, by linarith⟩

end D0.Analysis

end
