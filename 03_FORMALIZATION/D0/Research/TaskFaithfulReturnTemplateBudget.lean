import D0.Analysis.ReturnTemplateErrorBudget
import D0.Research.TaskFaithfulReturnContrast

/-!
# A prescribed contrast tolerance for the actual return templates

This consumes the actual two-endpoint return-product theorem, not an assumed
endpoint error estimate. Each endpoint has `M > 0` blocks, with its own actual
word, preparation, effects and scalar corners. A common relative tolerance
`δⱼ ≤ d < 1/2` and the explicit minimum budget below ensure the requested
return-contrast tolerance after division by the actual baseline gain and
`Λ = M λ`.

Source: the finite compiler budget following equation (12) in
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, proof blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.

The hypotheses are sufficient, not optimal. No block count is absorbed into
a constant. Native implementation/admission, additional preparation errors,
heat, clock, work and measurement errors remain outside this return estimate.
-/

noncomputable section

namespace D0.Research

open D0.Analysis
open scoped ComplexOrder

variable {J I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

/-- The source's displayed finite budget achieves tolerance `e` for the
actual return contrast. The number of blocks and the positive per-block
scale `lam` are explicit, and the denominator uses their exact product. -/
theorem taskReturnProduct_template_tolerance_bound
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
    (M : ℕ) (hM : 0 < M) (hlen : ∀ k, (w k).length = M)
    (d : ℝ) (hd0 : 0 ≤ d) (hdhalf : d < 1 / 2)
    (hδd : ∀ k j, j ∈ w k → 2 * ε k j / c k j ≤ d)
    (K : V →L[ℂ] X) (b : OrthonormalBasis n ℂ V)
    (z T0 θ t lam e : ℝ) (q : Bool → ℝ)
    (hz : 0 ≤ z) (hzOne : z < 1) (hT0 : 0 < T0)
    (hq : ∀ k, 0 < q k)
    (hscale : ∀ k, ((w k).map (c k)).prod ^ 2 = q k * T0)
    (hθ : 0 ≤ θ) (hqUpper : ∀ k, q k ≤ Real.exp θ)
    (hgain : 0 < regularizedReturnGain (1 - z)
      (((z * T0 : ℝ) : ℂ) • gramMatrix K.toLinearMap b))
    (ht : t ≠ 0) (hlam : 0 < lam)
    (hbudget : d ≤ min (1 / (2 * (M : ℝ)))
      (e * |t| * lam / (4 * Real.exp (θ + 2)))) :
    let T := fun k => ((w k).map (c k)).prod ^ 2
    let S0 : Matrix n n ℂ := ((z * T0 : ℝ) : ℂ) • gramMatrix K.toLinearMap b
    let S := fun k => (((z * T k : ℝ) : ℂ) • gramMatrix K.toLinearMap b)
    let H := fun k => (z : ℂ) •
      gramMatrix (taskReturnProduct (prepare k) (actual k) (w k) ∘L K).toLinearMap b
    |(regularizedReturnPrice (1 - z) (H true) - regularizedReturnPrice (1 - z) (H false) -
        regularizedReturnPrice (1 - z) (S true) + regularizedReturnPrice (1 - z) (S false)) /
        (2 * t * (regularizedReturnGain (1 - z) S0 * ((M : ℝ) * lam)))| ≤ e := by
  have hMr : 0 < (M : ℝ) := by exact_mod_cast hM
  have hη0 : 0 ≤ 2 * (M : ℝ) * d := by positivity
  have hδ0 : ∀ k j, j ∈ w k → 0 ≤ 2 * ε k j / c k j := by
    intro k j hj
    exact (norm_nonneg (taskReturnRelativeDefect (prepare k j) (actual k j) (c k j))).trans
      (taskReturnRelativeDefect_norm_le (prepare k j) (reference k j) (actual k j)
        (c k j) (ε k j) (hc k j hj) (hcorner k j hj) (heffect k j hj))
  have hsmall : ∀ k j, j ∈ w k → 2 * ε k j / c k j < 1 := by
    intro k j hj
    linarith [hδd k j hj]
  have hηend (k : Bool) :
      perturbationEta (fun j => 2 * ε k j / c k j) (w k) ≤ 2 * (M : ℝ) * d := by
    simpa only [hlen k] using perturbationEta_le_uniform_budget
      (fun j => 2 * ε k j / c k j) (w k) d (hδ0 k) (hδd k) hdhalf
  have hp := taskReturnProduct_price_contrast_bound prepare reference actual c ε w
    hc hcorner heffect hsmall K b z T0 (2 * (M : ℝ) * d) θ t ((M : ℝ) * lam) q
    hz hzOne hT0 hq hscale hη0 hθ hηend hqUpper hgain ht (mul_pos hMr hlam)
  exact hp.trans (returnContrast_le_tolerance_of_min_budget M d (2 * (M : ℝ) * d)
    θ t lam e hM hη0 le_rfl ht hlam hbudget)

end D0.Research

end
