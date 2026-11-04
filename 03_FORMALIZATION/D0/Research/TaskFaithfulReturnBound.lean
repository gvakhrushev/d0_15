import D0.Research.TaskFaithfulReporterEffect

/-!
# Operator error transport for task-faithful return compression

This module supplies the operator-norm input to equation (9) of
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
the existing PR #334 task-faithful return-source package consumed by
`TaskFaithfulReporterEffect`. The proof is pinned at owner commit
`fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, Git blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`, SHA-256
`9f2354817860f9024a597dba4bd14c0580cc021de5c473925740b46b0e8f96e5`.

The exact identity transports an effect difference through the actual fixed
preparation: `C(R,E₁) - C(R,E₂) = -2 R† (E₁-E₂) R`. Its operator norm is at
most `2 ‖R‖² ‖E₁-E₂‖`. An isometric preparation gives the bound `2 ε`,
including when the reference compression is a scalar corner. At a positive
scalar corner `c I`, the relative defect `B = c⁻¹ C - I` therefore satisfies
`‖B‖ ≤ 2 ε / c`, and `C = c (I + B)` holds exactly.

The continuous-linear-map theorem uses the ordinary operator norm and applies
on complex Hilbert spaces. The finite-dimensional adapter below is explicitly
identified with the existing `taskReturnCompression`; no new physical source
or preparation is selected. The noncommuting product, log-determinant price
and relative price bounds (10)--(12) remain outside this module.
-/

noncomputable section

namespace D0.Research

section ContinuousCompression

variable {I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [CompleteSpace I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [CompleteSpace X]

/-- The bounded-operator version of `R† (1 - 2E) R`. -/
def taskReturnCompressionL (prepare : X →L[ℂ] I) (effect : I →L[ℂ] I) :
    X →L[ℂ] X :=
  prepare.adjoint ∘L ((1 - (2 : ℂ) • effect) ∘L prepare)

/-- The full effect difference is transported through the same preparation. -/
theorem taskReturnCompressionL_sub
    (prepare : X →L[ℂ] I) (effect₁ effect₂ : I →L[ℂ] I) :
    taskReturnCompressionL prepare effect₁ - taskReturnCompressionL prepare effect₂ =
      (-2 : ℂ) • (prepare.adjoint ∘L ((effect₁ - effect₂) ∘L prepare)) := by
  ext x
  simp [taskReturnCompressionL, smul_sub]
  module

/-- Operator error propagation retains the actual preparation norm. -/
theorem taskReturnCompressionL_norm_sub_le
    (prepare : X →L[ℂ] I) (effect₁ effect₂ : I →L[ℂ] I) :
    ‖taskReturnCompressionL prepare effect₁ - taskReturnCompressionL prepare effect₂‖ ≤
      2 * ‖prepare‖ ^ 2 * ‖effect₁ - effect₂‖ := by
  rw [taskReturnCompressionL_sub, norm_smul]
  have hadj : ‖prepare.adjoint‖ = ‖prepare‖ :=
    ContinuousLinearMap.adjoint.norm_map prepare
  calc
    ‖(-2 : ℂ)‖ * ‖prepare.adjoint ∘L ((effect₁ - effect₂) ∘L prepare)‖ ≤
        2 * (‖prepare‖ * (‖effect₁ - effect₂‖ * ‖prepare‖)) := by
      norm_num only [norm_neg, Complex.norm_ofNat]
      apply mul_le_mul_of_nonneg_left _ (by norm_num)
      calc
        ‖prepare.adjoint ∘L ((effect₁ - effect₂) ∘L prepare)‖ ≤
            ‖prepare.adjoint‖ * ‖(effect₁ - effect₂) ∘L prepare‖ :=
          ContinuousLinearMap.opNorm_comp_le _ _
        _ ≤ ‖prepare‖ * (‖effect₁ - effect₂‖ * ‖prepare‖) := by
          rw [hadj]
          exact mul_le_mul_of_nonneg_left
            (ContinuousLinearMap.opNorm_comp_le _ _) (norm_nonneg _)
    _ = 2 * ‖prepare‖ ^ 2 * ‖effect₁ - effect₂‖ := by ring

/-- Isometric preparation cannot amplify an effect error beyond the factor two.
The statement also covers a zero-dimensional protected input space. -/
theorem taskReturnCompressionL_norm_sub_le_of_isometry
    (prepare : X →ₗᵢ[ℂ] I) (effect₁ effect₂ : I →L[ℂ] I) :
    ‖taskReturnCompressionL prepare.toContinuousLinearMap effect₁ -
        taskReturnCompressionL prepare.toContinuousLinearMap effect₂‖ ≤
      2 * ‖effect₁ - effect₂‖ := by
  apply (taskReturnCompressionL_norm_sub_le _ _ _).trans
  have hnorm := prepare.norm_toContinuousLinearMap_le
  have hnonneg := norm_nonneg prepare.toContinuousLinearMap
  have hsq : ‖prepare.toContinuousLinearMap‖ ^ 2 ≤ 1 := by nlinarith
  nlinarith [norm_nonneg (effect₁ - effect₂)]

end ContinuousCompression

section FiniteCompression

variable {I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

local instance : CompleteSpace I := FiniteDimensional.complete ℂ I
local instance : CompleteSpace X := FiniteDimensional.complete ℂ X

/-- The bounded version is exactly the existing finite return compression. -/
theorem taskReturnCompression_toContinuousLinearMap
    (prepare : X →ₗ[ℂ] I) (effect : I →ₗ[ℂ] I) :
    (taskReturnCompression prepare effect).toContinuousLinearMap =
      taskReturnCompressionL prepare.toContinuousLinearMap effect.toContinuousLinearMap := by
  rfl

/-- The exact difference identity in the existing finite linear-map interface. -/
theorem taskReturnCompression_sub
    (prepare : X →ₗ[ℂ] I) (effect₁ effect₂ : I →ₗ[ℂ] I) :
    taskReturnCompression prepare effect₁ - taskReturnCompression prepare effect₂ =
      (-2 : ℂ) • (prepare.adjoint ∘ₗ ((effect₁ - effect₂) ∘ₗ prepare)) := by
  ext x
  simp [taskReturnCompression, smul_sub, map_sub, map_smul]

/-- Finite return error in the operator norm, not a coordinatewise matrix norm. -/
theorem taskReturnCompression_norm_sub_le
    (prepare : X →ₗ[ℂ] I) (effect₁ effect₂ : I →ₗ[ℂ] I) :
    ‖(taskReturnCompression prepare effect₁ -
        taskReturnCompression prepare effect₂).toContinuousLinearMap‖ ≤
      2 * ‖prepare.toContinuousLinearMap‖ ^ 2 *
        ‖(effect₁ - effect₂).toContinuousLinearMap‖ := by
  simpa only [map_sub, taskReturnCompression_toContinuousLinearMap] using
    taskReturnCompressionL_norm_sub_le prepare.toContinuousLinearMap
      effect₁.toContinuousLinearMap effect₂.toContinuousLinearMap

/-- A full-input effect tolerance gives the stated `2 ε` compression tolerance. -/
theorem taskReturnCompression_norm_sub_le_of_isometry
    (prepare : X →ₗᵢ[ℂ] I) (effect₁ effect₂ : I →ₗ[ℂ] I)
    {ε : ℝ} (heffect : ‖(effect₁ - effect₂).toContinuousLinearMap‖ ≤ ε) :
    ‖(taskReturnCompression prepare.toLinearMap effect₁ -
        taskReturnCompression prepare.toLinearMap effect₂).toContinuousLinearMap‖ ≤
      2 * ε := by
  have hbound := taskReturnCompressionL_norm_sub_le_of_isometry prepare
    effect₁.toContinuousLinearMap effect₂.toContinuousLinearMap
  have hfinite :
      ‖(taskReturnCompression prepare.toLinearMap effect₁ -
          taskReturnCompression prepare.toLinearMap effect₂).toContinuousLinearMap‖ ≤
        2 * ‖(effect₁ - effect₂).toContinuousLinearMap‖ := by
    simpa only [map_sub, taskReturnCompression_toContinuousLinearMap] using hbound
  exact hfinite.trans (mul_le_mul_of_nonneg_left heffect (by norm_num))

/-- Equation (9)'s initial error estimate at a supplied scalar reference corner.
The corner identity is a hypothesis; it is not inferred from one input statistic. -/
theorem taskReturnCompression_scalarCorner_error_le
    (prepare : X →ₗᵢ[ℂ] I) (effect actualEffect : I →ₗ[ℂ] I)
    (c : ℂ) (hcorner : taskReturnCompression prepare.toLinearMap effect = c • 1)
    {ε : ℝ} (heffect : ‖(actualEffect - effect).toContinuousLinearMap‖ ≤ ε) :
    ‖(taskReturnCompression prepare.toLinearMap actualEffect - c • 1).toContinuousLinearMap‖ ≤
      2 * ε := by
  rw [← hcorner]
  exact taskReturnCompression_norm_sub_le_of_isometry prepare actualEffect effect heffect

/-- The relative defect needed by the noncommuting-product estimate has norm
at most `δ = 2 ε / c`. No invertibility of a retained-history operator is used. -/
theorem taskReturnCompression_scalarCorner_relative_error_le
    (prepare : X →ₗᵢ[ℂ] I) (effect actualEffect : I →ₗ[ℂ] I)
    (c : ℝ) (hc : 0 < c)
    (hcorner : taskReturnCompression prepare.toLinearMap effect = (c : ℂ) • 1)
    {ε : ℝ} (heffect : ‖(actualEffect - effect).toContinuousLinearMap‖ ≤ ε) :
    ‖((c : ℂ)⁻¹) •
        (taskReturnCompression prepare.toLinearMap actualEffect).toContinuousLinearMap - 1‖ ≤
      2 * ε / c := by
  have hcC : (c : ℂ) ≠ 0 := by exact_mod_cast ne_of_gt hc
  have hrelative :
      ((c : ℂ)⁻¹) •
          (taskReturnCompression prepare.toLinearMap actualEffect).toContinuousLinearMap - 1 =
        ((c : ℂ)⁻¹) •
          (taskReturnCompression prepare.toLinearMap actualEffect -
            (c : ℂ) • 1).toContinuousLinearMap := by
    rw [map_sub, map_smul, smul_sub, smul_smul, inv_mul_cancel₀ hcC, one_smul]
    rfl
  rw [hrelative, norm_smul]
  simp only [norm_inv, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hc]
  calc
    c⁻¹ * ‖(taskReturnCompression prepare.toLinearMap actualEffect -
        (c : ℂ) • 1).toContinuousLinearMap‖ ≤ c⁻¹ * (2 * ε) :=
      mul_le_mul_of_nonneg_left
        (taskReturnCompression_scalarCorner_error_le prepare effect actualEffect
          (c : ℂ) hcorner heffect) (inv_nonneg.mpr hc.le)
    _ = 2 * ε / c := by rw [div_eq_mul_inv]; ring

/-- The same relative defect gives the exact factorization `C = c (I + B)`.
The estimate above, rather than this algebraic identity alone, controls `B`. -/
theorem taskReturnCompression_relative_factorization
    (prepare : X →ₗ[ℂ] I) (effect : I →ₗ[ℂ] I)
    (c : ℝ) (hc : 0 < c) :
    (taskReturnCompression prepare effect).toContinuousLinearMap =
      (c : ℂ) • (1 + (((c : ℂ)⁻¹) •
        (taskReturnCompression prepare effect).toContinuousLinearMap - 1)) := by
  have hcC : (c : ℂ) ≠ 0 := by exact_mod_cast ne_of_gt hc
  rw [← add_sub_assoc, add_sub_cancel_left, smul_smul, mul_inv_cancel₀ hcC, one_smul]

end FiniteCompression

end D0.Research

end
