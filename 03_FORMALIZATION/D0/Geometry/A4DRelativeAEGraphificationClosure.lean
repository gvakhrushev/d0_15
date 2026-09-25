import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic
import D0.Geometry.A4DRelativeAEComparisonSpan

/-!
# Graphification / residual / two-sided functional closure

Lean owner for the residual-range, Role-basis residual criterion, residual-rank
formula, full-rank ⇒ graph corollary, and two-sided functional package that
research PR #128 proved on top of `A4DRelativeAEComparisonSpan` (Lean #126).

Reuses the span API without forking. No finite graded F, continuum, GR, QFT,
action, stress, or physical-time claim. One-sided graph is not identified with
a reversible change of variables.
-/

namespace D0.Geometry.A4DRelativeAEGraphificationClosure

open D0
open D0.Geometry.A4DRelativeAEComparisonSpan
open scoped InnerProductSpace

noncomputable section

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-! ## Kernel component is the identity on `ker B` -/

theorem kernelComponent_eq_self_of_mem_kernel
    (B : LabelCoeff →ₗ[ℝ] V) {c : LabelCoeff}
    (hc : c ∈ LinearMap.ker B) :
    kernelComponent B c = c := by
  simp [kernelComponent, coefficientRepresentative_eq_zero_of_mem_kernel B hc]

/-! ## 1. Residual range equals vertical defect -/

theorem range_canonicalResidual_eq_verticalDefect
    (B S : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.range (canonicalResidual B S) = verticalDefect B S := by
  apply le_antisymm
  · rintro _ ⟨c, rfl⟩
    exact canonicalResidual_mem_vertical B S c
  · rintro v ⟨c, hc, rfl⟩
    refine ⟨c, ?_⟩
    simp [canonicalResidual, kernelComponent_eq_self_of_mem_kernel B hc]

/-! ## 2. Role-basis residuals -/

/-- Canonical residual on the Role basis vector `EuclideanSpace.single r 1`. -/
def roleResidual (B S : LabelCoeff →ₗ[ℝ] V) (r : Role) : V :=
  canonicalResidual B S (EuclideanSpace.single r 1)

theorem roleResidual_mem_verticalDefect
    (B S : LabelCoeff →ₗ[ℝ] V) (r : Role) :
    roleResidual B S r ∈ verticalDefect B S :=
  canonicalResidual_mem_vertical B S _

private theorem labelCoeff_eq_sum_singles (c : LabelCoeff) :
    c = ∑ r : Role, c r • EuclideanSpace.single r (1 : ℝ) := by
  classical
  simpa [EuclideanSpace.basisFun_apply, EuclideanSpace.basisFun_repr] using
    ((EuclideanSpace.basisFun Role ℝ).sum_repr c).symm

theorem verticalDefect_eq_span_roleResiduals
    (B S : LabelCoeff →ₗ[ℝ] V) :
    verticalDefect B S =
      Submodule.span ℝ (Set.range (roleResidual B S)) := by
  rw [← range_canonicalResidual_eq_verticalDefect]
  apply le_antisymm
  · rintro v ⟨c, rfl⟩
    have hc := labelCoeff_eq_sum_singles c
    rw [hc, map_sum]
    exact sum_mem fun r _ => by
      rw [map_smul]
      exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨r, rfl⟩)
  · apply Submodule.span_le.mpr
    rintro _ ⟨r, rfl⟩
    exact ⟨EuclideanSpace.single r 1, rfl⟩

theorem verticalDefect_eq_iSup_span_roleResidual
    (B S : LabelCoeff →ₗ[ℝ] V) :
    verticalDefect B S = ⨆ r : Role, ℝ ∙ roleResidual B S r := by
  rw [verticalDefect_eq_span_roleResiduals, Submodule.span_range_eq_iSup]

theorem verticalDefect_eq_bot_iff_forall_roleResidual_eq_zero
    (B S : LabelCoeff →ₗ[ℝ] V) :
    verticalDefect