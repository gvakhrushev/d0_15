import D0.Analysis.MatrixRelativeLogDetBound

/-!
# Two-endpoint relative matrix logdet contrast

This is the matrix contrast step (12) of the existing #334 task-faithful
return-source proof,
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, proof blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.

Both endpoint price errors are derived from their positive-semidefinite
matrix sandwiches. The endpoints need not commute with the common reference
or with one another. The denominator uses the actual reference resolvent
trace, not a normalized surrogate. Singular reference matrices are allowed;
positive reference gain and nonzero contrast step are explicit hypotheses.

The matrix sandwiches must come from the actual execution being compared.
This theorem does not choose that execution or its physical task and does
not remove independent heat, clock, work, preparation, or measurement errors.
It is a finite contrast bound, not a derivative bound obtained from value
tolerances.
-/

noncomputable section

namespace D0.Analysis

open RelativeLogDetScaleBound
open scoped ComplexOrder

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Equation (12) for two full matrix prices, with both endpoint errors
proved from Gram-order sandwiches and normalization by the actual trace gain. -/
theorem regularizedReturnPrice_contrast_bound
    (S HPlus HMinus : Matrix n n ℂ)
    (hS : S.PosSemidef) (hHPlus : HPlus.PosSemidef) (hHMinus : HMinus.PosSemidef)
    (a qPlus qMinus η θ t Λ : ℝ)
    (ha : 0 < a) (hqPlus : 0 < qPlus) (hqMinus : 0 < qMinus)
    (hη : 0 ≤ η) (hθ : 0 ≤ θ)
    (hqPlusUpper : qPlus ≤ Real.exp θ) (hqMinusUpper : qMinus ≤ Real.exp θ)
    (hgain : 0 < regularizedReturnGain a S) (ht : t ≠ 0) (hΛ : 0 < Λ)
    (hPlusLower : (HPlus - (Real.exp (-2 * η) : ℂ) • ((qPlus : ℂ) • S)).PosSemidef)
    (hPlusUpper : ((Real.exp (2 * η) : ℂ) • ((qPlus : ℂ) • S) - HPlus).PosSemidef)
    (hMinusLower : (HMinus - (Real.exp (-2 * η) : ℂ) • ((qMinus : ℂ) • S)).PosSemidef)
    (hMinusUpper : ((Real.exp (2 * η) : ℂ) • ((qMinus : ℂ) • S) - HMinus).PosSemidef) :
    |(regularizedReturnPrice a HPlus - regularizedReturnPrice a HMinus -
        regularizedReturnPrice a ((qPlus : ℂ) • S) +
        regularizedReturnPrice a ((qMinus : ℂ) • S)) /
        (2 * t * (regularizedReturnGain a S * Λ))| ≤
      Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * Λ) := by
  have hqSPlus : ((qPlus : ℂ) • S).PosSemidef :=
    hS.smul (Complex.zero_le_real.mpr hqPlus.le)
  have hqSMinus : ((qMinus : ℂ) • S).PosSemidef :=
    hS.smul (Complex.zero_le_real.mpr hqMinus.le)
  have hp := regularizedReturnPrice_sandwich_bound ((qPlus : ℂ) • S) HPlus
    hqSPlus hHPlus a η ha hη hPlusLower hPlusUpper
  have hm := regularizedReturnPrice_sandwich_bound ((qMinus : ℂ) • S) HMinus
    hqSMinus hHMinus a η ha hη hMinusLower hMinusUpper
  rw [regularizedReturnPrice_smul_spectral S hS a qPlus ha hqPlus.le,
    regularizedReturnGain_smul_spectral S hS a qPlus ha hqPlus.le] at hp
  rw [regularizedReturnPrice_smul_spectral S hS a qMinus ha hqMinus.le,
    regularizedReturnGain_smul_spectral S hS a qMinus ha hqMinus.le] at hm
  have hg := regularizedReturnGain_smul_spectral S hS a 1 ha (by norm_num)
  simp only [Complex.ofReal_one, one_smul] at hg
  have hgainSpectral : 0 < finiteSpectralGain a hS.isHermitian.eigenvalues 1 := by
    rw [← hg]
    exact hgain
  rw [regularizedReturnPrice_smul_spectral S hS a qPlus ha hqPlus.le,
    regularizedReturnPrice_smul_spectral S hS a qMinus ha hqMinus.le, hg]
  exact finiteSpectralPrice_contrast_bound a hS.isHermitian.eigenvalues
    qPlus qMinus (regularizedReturnPrice a HPlus) (regularizedReturnPrice a HMinus)
    η θ t Λ ha hS.eigenvalues_nonneg hqPlus hqMinus hη hθ
    hqPlusUpper hqMinusUpper hgainSpectral ht hΛ hp hm

end D0.Analysis

end
