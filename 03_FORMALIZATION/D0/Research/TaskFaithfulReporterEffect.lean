import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.LinearMap

/-!
# Finite task-faithful reporter-effect tomography

This research module formalizes one finite operator slice of the existing
Draft #334 source at commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`:
`02_REGISTRY/research/A4D_TASK_FAITHFUL_RETURN_SOURCE_2026_10_28.md`, Git blob
`be76ea1e008648cf2d12b7b9ced7714233e2addd`, SHA-256
`559a7a9a4c5517fb7a0f61d5bf0f4df687d88879b64c512f5980421af27c0161`.

On finite-dimensional complex inner-product spaces, the pullback of a fixed
output readout through an input preparation and reporter is determined by its
quadratic statistics on unit input vectors. Equal statistics therefore give
equal reporter effects. The same effect yields exactly the same compressed
return operator for every further preparation map.

The module does not formalize mixed-density-matrix trace representation, the
relative finite-error estimate, the full noncommuting return price or its
derivative, and it establishes no physical task/primitive admission.
-/

noncomputable section

namespace D0.Research

open scoped ComplexConjugate
local notation "⟪" x ", " y "⟫_ℂ" => inner ℂ x y

variable {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V]

/-- A complex-linear endomorphism is determined by its quadratic form on
unit input vectors. -/
theorem endomorphism_eq_of_unit_quadratic
    (S T : V →ₗ[ℂ] V)
    (h : ∀ x, ‖x‖ = 1 → ⟪S x, x⟫_ℂ = ⟪T x, x⟫_ℂ) : S = T := by
  apply (ext_inner_map S T).mp
  intro x
  by_cases hx : x = 0
  · simp [hx]
  · have hxpos : 0 < ‖x‖ := norm_pos_iff.mpr hx
    let c : ℂ := ((‖x‖⁻¹ : ℝ) : ℂ)
    have hcNorm : ‖c‖ = ‖x‖⁻¹ := by
      simp [c, Complex.norm_real]
    have hcNe : c ≠ 0 := by
      dsimp [c]
      exact_mod_cast (inv_ne_zero (ne_of_gt hxpos))
    have hunit : ‖c • x‖ = 1 := by
      rw [norm_smul, hcNorm]
      exact inv_mul_cancel₀ (ne_of_gt hxpos)
    have hprobe := h (c • x) hunit
    have hscaled :
        (star c * c) * ⟪S x, x⟫_ℂ =
          (star c * c) * ⟪T x, x⟫_ℂ := by
      have hexpanded :
          c * (star c * ⟪S x, x⟫_ℂ) =
            c * (star c * ⟪T x, x⟫_ℂ) := by
        simpa only [map_smul, inner_smul_left, inner_smul_right] using hprobe
      calc
        (star c * c) * ⟪S x, x⟫_ℂ =
            c * (star c * ⟪S x, x⟫_ℂ) := by ac_rfl
        _ = c * (star c * ⟪T x, x⟫_ℂ) := hexpanded
        _ = (star c * c) * ⟪T x, x⟫_ℂ := by ac_rfl
    have hfactor : star c * c ≠ 0 :=
      mul_ne_zero (star_ne_zero.mpr hcNe) hcNe
    exact mul_left_cancel₀ hfactor hscaled

section ReporterEffect

variable {I M O : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup M] [InnerProductSpace ℂ M] [FiniteDimensional ℂ M]
  [NormedAddCommGroup O] [InnerProductSpace ℂ O] [FiniteDimensional ℂ O]

/-- The input-space effect induced by a preparation, reporter and fixed output
readout: `i† T† Π T i`. -/
def taskReporterEffect
    (prepare : I →ₗ[ℂ] M) (report : M →ₗ[ℂ] O) (readout : O →ₗ[ℂ] O) :
    I →ₗ[ℂ] I :=
  LinearMap.adjoint prepare ∘ₗ
    (LinearMap.adjoint report ∘ₗ (readout ∘ₗ (report ∘ₗ prepare)))

/-- The pulled-back effect's quadratic form is the output readout statistic. -/
theorem taskReporterEffect_quadratic
    (prepare : I →ₗ[ℂ] M) (report : M →ₗ[ℂ] O) (readout : O →ₗ[ℂ] O)
    (ψ : I) :
    ⟪taskReporterEffect prepare report readout ψ, ψ⟫_ℂ =
      ⟪readout (report (prepare ψ)), report (prepare ψ)⟫_ℂ := by
  simp [taskReporterEffect, LinearMap.coe_comp, Function.comp_apply,
    LinearMap.adjoint_inner_left]

/-- Two reporters have the same statistics on every unit input vector for the
same preparation and output readout. -/
def sameUnitReporterStatistics
    (prepare : I →ₗ[ℂ] M) (report₁ report₂ : M →ₗ[ℂ] O)
    (readout : O →ₗ[ℂ] O) : Prop :=
  ∀ ψ, ‖ψ‖ = 1 →
    ⟪readout (report₁ (prepare ψ)), report₁ (prepare ψ)⟫_ℂ =
      ⟪readout (report₂ (prepare ψ)), report₂ (prepare ψ)⟫_ℂ

/-- Same-task unit-vector statistics characterize the complete pulled-back
reporter effect. Equality on a normalized pure-state subset is already enough;
no equality at one chosen input or only in a classical basis is assumed. -/
theorem taskReporterEffect_eq_iff_sameUnitStatistics
    (prepare : I →ₗ[ℂ] M) (report₁ report₂ : M →ₗ[ℂ] O)
    (readout : O →ₗ[ℂ] O) :
    taskReporterEffect prepare report₁ readout =
        taskReporterEffect prepare report₂ readout ↔
      sameUnitReporterStatistics prepare report₁ report₂ readout := by
  constructor
  · intro heq ψ hψ
    calc
      ⟪readout (report₁ (prepare ψ)), report₁ (prepare ψ)⟫_ℂ =
          ⟪taskReporterEffect prepare report₁ readout ψ, ψ⟫_ℂ :=
            (taskReporterEffect_quadratic prepare report₁ readout ψ).symm
      _ = ⟪taskReporterEffect prepare report₂ readout ψ, ψ⟫_ℂ := by rw [heq]
      _ = ⟪readout (report₂ (prepare ψ)), report₂ (prepare ψ)⟫_ℂ :=
            taskReporterEffect_quadratic prepare report₂ readout ψ
  · intro hstats
    apply endomorphism_eq_of_unit_quadratic
    intro ψ hψ
    calc
      ⟪taskReporterEffect prepare report₁ readout ψ, ψ⟫_ℂ =
          ⟪readout (report₁ (prepare ψ)), report₁ (prepare ψ)⟫_ℂ :=
            taskReporterEffect_quadratic prepare report₁ readout ψ
      _ = ⟪readout (report₂ (prepare ψ)), report₂ (prepare ψ)⟫_ℂ :=
            hstats ψ hψ
      _ = ⟪taskReporterEffect prepare report₂ readout ψ, ψ⟫_ℂ :=
            (taskReporterEffect_quadratic prepare report₂ readout ψ).symm

end ReporterEffect

section ReturnCompression

variable {I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

/-- Exact return compression `R† (1 - 2E) R` for a fixed input-space effect. -/
def taskReturnCompression (prepare : X →ₗ[ℂ] I) (effect : I →ₗ[ℂ] I) :
    X →ₗ[ℂ] X :=
  LinearMap.adjoint prepare ∘ₗ ((1 - (2 : ℂ) • effect) ∘ₗ prepare)

/-- Equality of complete reporter effects implies equality of the return
compression for every fixed preparation map. -/
theorem taskReturnCompression_eq_of_effect_eq
    (prepare : X →ₗ[ℂ] I) (effect₁ effect₂ : I →ₗ[ℂ] I)
    (heffect : effect₁ = effect₂) :
    taskReturnCompression prepare effect₁ =
      taskReturnCompression prepare effect₂ := by
  rw [heffect]

end ReturnCompression

end D0.Research

end
