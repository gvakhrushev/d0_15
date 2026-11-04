import D0.Research.TaskFaithfulReturnPrice

/-!
# Two-endpoint contrast for actual task-faithful return products

This is the concrete finite-execution consumer of equation (12) in
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, proof blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.

The two endpoint prices come from their actual ordered return products after
one common retained-history map K. Each error follows from full-input effect
errors and exact scalar reference corners through taskReturnProduct_price_bound;
no endpoint price-error or matrix-sandwich premise is supplied. The exact
bindings T_k=q_k T0 compare the actual endpoint gains to the baseline gain.
Only q_k<=exp(theta) is needed; the owner's absolute logarithmic displacement
condition is stronger. Singular retained history is allowed. Positive baseline
gain, nonzero comparison step and positive Lambda remain explicit because the
contrast divides by them.

This estimates the return-price contrast only. It does not turn value tolerance
into a derivative bound or remove separate heat, clock, work, preparation or
measurement errors. Physical task and execution admission remain unselected.
-/

noncomputable section

namespace D0.Research

open D0.Analysis D0.Analysis.RelativeLogDetScaleBound
open scoped ComplexOrder

variable {J I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

/-- Equation (12), with both price errors derived for the actual endpoint
products. `true` and `false` denote the plus and minus endpoints. -/
theorem taskReturnProduct_price_contrast_bound
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : Bool → J → X →ₗᵢ[ℂ] I)
    (reference actual : Bool → J → I →ₗ[ℂ] I)
    (c ε : Bool → J → ℝ) (w : Bool → List J)
    (hc : ∀ k j, j ∈ w k → 0 < c k j)
    (hcorner : ∀ k j, j ∈ w k →
      taskReturnCompression (prepare k j).toLinearMap (reference k j) = (c k j : ℂ) • 1)
    (heffect : ∀ k j, j ∈ w k →
      ‖(actual k j - reference k j).toContinuousLinearMap‖ ≤ ε k j)
    (hsmall : ∀ k j, j ∈ w k → 2 * ε k j / c k j < 1)
    (K : V →L[ℂ] X) (b : OrthonormalBasis n ℂ V)
    (z T0 η θ t Λ : ℝ) (q : Bool → ℝ)
    (hz : 0 ≤ z) (hzOne : z < 1) (hT0 : 0 < T0)
    (hq : ∀ k, 0 < q k)
    (hscale : ∀ k, ((w k).map (c k)).prod ^ 2 = q k * T0)
    (hη : 0 ≤ η) (hθ : 0 ≤ θ)
    (hηend : ∀ k, perturbationEta (fun j => 2 * ε k j / c k j) (w k) ≤ η)
    (hqUpper : ∀ k, q k ≤ Real.exp θ)
    (hgain : 0 < regularizedReturnGain (1 - z)
      (((z * T0 : ℝ) : ℂ) • gramMatrix K.toLinearMap b))
    (ht : t ≠ 0) (hΛ : 0 < Λ) :
    let T := fun k => ((w k).map (c k)).prod ^ 2
    let S0 : Matrix n n ℂ := ((z * T0 : ℝ) : ℂ) • gramMatrix K.toLinearMap b
    let S := fun k => (((z * T k : ℝ) : ℂ) • gramMatrix K.toLinearMap b)
    let H := fun k => (z : ℂ) •
      gramMatrix (taskReturnProduct (prepare k) (actual k) (w k) ∘L K).toLinearMap b
    |(regularizedReturnPrice (1 - z) (H true) - regularizedReturnPrice (1 - z) (H false) -
        regularizedReturnPrice (1 - z) (S true) + regularizedReturnPrice (1 - z) (S false)) /
        (2 * t * (regularizedReturnGain (1 - z) S0 * Λ))| ≤
      Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * Λ) := by
  let a := 1 - z
  let T := fun k => ((w k).map (c k)).prod ^ 2
  let S0 : Matrix n n ℂ := ((z * T0 : ℝ) : ℂ) • gramMatrix K.toLinearMap b
  let S := fun k => (((z * T k : ℝ) : ℂ) • gramMatrix K.toLinearMap b)
  let H := fun k => (z : ℂ) •
    gramMatrix (taskReturnProduct (prepare k) (actual k) (w k) ∘L K).toLinearMap b
  change |(regularizedReturnPrice a (H true) - regularizedReturnPrice a (H false) -
      regularizedReturnPrice a (S true) + regularizedReturnPrice a (S false)) /
      (2 * t * (regularizedReturnGain a S0 * Λ))| ≤
    Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * Λ)
  have ha : 0 < a := sub_pos.mpr hzOne
  have hS0 : S0.PosSemidef :=
    (gramMatrix_posSemidef K.toLinearMap b).smul
      (Complex.zero_le_real.mpr (mul_nonneg hz hT0.le))
  have hSscale (k : Bool) : (q k : ℂ) • S0 = S k := by
    dsimp only [S0, S, T]
    rw [smul_smul, hscale k]
    congr 1
    simp only [Complex.ofReal_mul]
    ring
  have hbound (k : Bool) :
      |regularizedReturnPrice a (H k) - finiteSpectralPrice a hS0.isHermitian.eigenvalues (q k)| ≤
        (Real.exp (2 * η) - 1) * finiteSpectralGain a hS0.isHermitian.eigenvalues (q k) := by
    have hp := taskReturnProduct_price_bound (prepare k) (reference k) (actual k)
      (c k) (ε k) (w k) (hc k) (hcorner k) (heffect k) (hsmall k) K b z hz hzOne
    change |regularizedReturnPrice a (H k) - regularizedReturnPrice a (S k)| ≤
      (Real.exp (2 * perturbationEta (fun j => 2 * ε k j / c k j) (w k)) - 1) *
        regularizedReturnGain a (S k) at hp
    rw [← hSscale k, regularizedReturnPrice_smul_spectral S0 hS0 a (q k) ha (hq k).le,
      regularizedReturnGain_smul_spectral S0 hS0 a (q k) ha (hq k).le] at hp
    have hcoef :
        Real.exp (2 * perturbationEta (fun j => 2 * ε k j / c k j) (w k)) - 1 ≤
          Real.exp (2 * η) - 1 :=
      sub_le_sub_right (Real.exp_le_exp.mpr
        (mul_le_mul_of_nonneg_left (hηend k) (by norm_num))) 1
    exact hp.trans (mul_le_mul_of_nonneg_right hcoef
      (finiteSpectralGain_nonneg a hS0.isHermitian.eigenvalues (q k)
        ha hS0.eigenvalues_nonneg (hq k).le))
  have hg := regularizedReturnGain_smul_spectral S0 hS0 a 1 ha (by norm_num)
  simp only [Complex.ofReal_one, one_smul] at hg
  have hgainSpectral : 0 < finiteSpectralGain a hS0.isHermitian.eigenvalues 1 := by
    rw [← hg]
    exact hgain
  rw [← hSscale true, ← hSscale false,
    regularizedReturnPrice_smul_spectral S0 hS0 a (q true) ha (hq true).le,
    regularizedReturnPrice_smul_spectral S0 hS0 a (q false) ha (hq false).le, hg]
  exact finiteSpectralPrice_contrast_bound a hS0.isHermitian.eigenvalues
    (q true) (q false) (regularizedReturnPrice a (H true)) (regularizedReturnPrice a (H false))
    η θ t Λ ha hS0.eigenvalues_nonneg (hq true) (hq false) hη hθ
    (hqUpper true) (hqUpper false) hgainSpectral ht hΛ (hbound true) (hbound false)

end D0.Research

end
