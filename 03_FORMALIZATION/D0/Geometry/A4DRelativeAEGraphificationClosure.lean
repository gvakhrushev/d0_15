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
    verticalDefect B S = ⊥ ↔ ∀ r : Role, roleResidual B S r = 0 := by
  constructor
  · intro h r
    have hr := roleResidual_mem_verticalDefect B S r
    simp [h] at hr
    exact hr
  · intro h
    rw [verticalDefect_eq_span_roleResiduals, Submodule.span_eq_bot]
    intro x hx
    rcases hx with ⟨r, rfl⟩
    exact h r

/-- Hostile control: Role `C` residual vanishes on the duplicate-generator
witness while the vertical defect is nontrivial. -/
theorem one_roleResidual_zero_not_enough :
    roleResidual duplicateB duplicateS C = 0 ∧
      verticalDefect duplicateB duplicateS ≠ ⊥ := by
  constructor
  · have hc :
        EuclideanSpace.single (C : Role) 1 ∈ LinearMap.ker duplicateB := by
      rw [LinearMap.mem_ker]
      simp [duplicateB, coeffRole,
        show C ≠ A by decide, show C ≠ B by decide]
    have hs :
        duplicateS (EuclideanSpace.single (C : Role) 1) = 0 := by
      simp [duplicateS, coeffRole,
        show C ≠ A by decide, show C ≠ B by decide]
    change canonicalResidual duplicateB duplicateS
        (EuclideanSpace.single C 1) = 0
    simp [canonicalResidual,
      kernelComponent_eq_self_of_mem_kernel duplicateB hc, hs]
  · intro h
    exact duplicate_generator_no_strict
      ((spanCalibration_iff_verticalDefect_eq_bot duplicateB duplicateS).mpr h)

/-! ## 3. Residual-rank formula -/

/-- First-factor projection of the generated relation. -/
def relationFst (B S : LabelCoeff →ₗ[ℝ] V) :
    comparisonRelation B S →ₗ[ℝ] V :=
  (LinearMap.fst ℝ V V).comp (comparisonRelation B S).subtype

theorem relationFst_range
    (B S : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.range (relationFst B S) = LinearMap.range B := by
  ext v
  constructor
  · rintro ⟨⟨⟨u, w⟩, ⟨c, hc⟩⟩, rfl⟩
    have hu : u = B c := by
      simpa [pairSynthesis] using (congrArg Prod.fst hc).symm
    exact ⟨c, hu.symm⟩
  · rintro ⟨c, rfl⟩
    refine ⟨⟨(B c, S c), ⟨c, by simp [pairSynthesis]⟩⟩, rfl⟩

/-- The kernel of `relationFst` is linearly equivalent to the vertical defect. -/
noncomputable def kerRelationFstEquivVerticalDefect
    (B S : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.ker (relationFst B S) ≃ₗ[ℝ] verticalDefect B S where
  toFun p := by
    rcases p with ⟨⟨⟨u, w⟩, hw⟩, hk⟩
    have hu : u = 0 := by
      change (LinearMap.fst ℝ V V) ⟨u, w⟩ = 0 at hk
      simpa using hk
    refine ⟨w, (zero_pair_mem_comparisonRelation_iff B S w).mp ?_⟩
    simpa [hu] using hw
  invFun q := by
    rcases q with ⟨w, hw⟩
    refine ⟨⟨(0, w), (zero_pair_mem_comparisonRelation_iff B S w).mpr hw⟩, ?_⟩
    simp [relationFst]
  left_inv := by
    intro p
    apply Subtype.ext
    apply Subtype.ext
    rcases p with ⟨⟨⟨u, w⟩, hw⟩, hk⟩
    have hu : u = 0 := by
      change (LinearMap.fst ℝ V V) ⟨u, w⟩ = 0 at hk
      simpa using hk
    simp [hu]
  right_inv := by
    intro q
    apply Subtype.ext
    rfl
  map_add' := by
    intro x y
    apply Subtype.ext
    rfl
  map_smul' := by
    intro a x
    apply Subtype.ext
    rfl

theorem finrank_verticalDefect
    [FiniteDimensional ℝ V] (B S : LabelCoeff →ₗ[ℝ] V) :
    Module.finrank ℝ (verticalDefect B S) =
      Module.finrank ℝ (LinearMap.range (pairSynthesis B S)) -
        Module.finrank ℝ (LinearMap.range B) := by
  haveI : FiniteDimensional ℝ (comparisonRelation B S) := inferInstance
  have hrn := LinearMap.finrank_range_add_finrank_ker (relationFst B S)
  have hrange :
      Module.finrank ℝ (LinearMap.range (relationFst B S)) =
        Module.finrank ℝ (LinearMap.range B) := by
    rw [relationFst_range]
  have hker :
      Module.finrank ℝ (LinearMap.ker (relationFst B S)) =
        Module.finrank ℝ (verticalDefect B S) :=
    LinearEquiv.finrank_eq (kerRelationFstEquivVerticalDefect B S)
  -- `comparisonRelation = range pairSynthesis` definitionally.
  have hsum :
      Module.finrank ℝ (LinearMap.range (pairSynthesis B S)) =
        Module.finrank ℝ (LinearMap.range B) +
          Module.finrank ℝ (verticalDefect B S) := by
    change Module.finrank ℝ (comparisonRelation B S) =
        Module.finrank ℝ (LinearMap.range B) +
          Module.finrank ℝ (verticalDefect B S)
    calc
      Module.finrank ℝ (comparisonRelation B S)
          = Module.finrank ℝ (LinearMap.range (relationFst B S)) +
              Module.finrank ℝ (LinearMap.ker (relationFst B S)) := hrn.symm
      _ = Module.finrank ℝ (LinearMap.range B) +
              Module.finrank ℝ (verticalDefect B S) := by rw [hrange, hker]
  have hle :
      Module.finrank ℝ (LinearMap.range B) ≤
        Module.finrank ℝ (LinearMap.range (pairSynthesis B S)) := by
    rw [hsum]; exact Nat.le_add_right _ _
  omega

/-! ## 4. Full-rank B implies graph -/

theorem verticalDefect_eq_bot_of_ker_eq_bot
    (B S : LabelCoeff →ₗ[ℝ] V) (h : LinearMap.ker B = ⊥) :
    verticalDefect B S = ⊥ := by
  simp [verticalDefect, h]

theorem spanCalibration_of_ker_eq_bot
    (B S : LabelCoeff →ₗ[ℝ] V) (h : LinearMap.ker B = ⊥) :
    SpanCalibration B S := by
  rw [spanCalibration_iff_verticalDefect_eq_bot]
  exact verticalDefect_eq_bot_of_ker_eq_bot B S h

theorem spanCalibration_of_injective
    (B S : LabelCoeff →ₗ[ℝ] V) (h : Function.Injective B) :
    SpanCalibration B S :=
  spanCalibration_of_ker_eq_bot B S (LinearMap.ker_eq_bot.mpr h)

/-- Optional finite-dimensional full-rank form: equal domain/codomain finrank
bound plus `finrank(range B) = finrank LabelCoeff` forces injectivity. -/
theorem verticalDefect_eq_bot_of_finrank_range
    [FiniteDimensional ℝ V]
    (B S : LabelCoeff →ₗ[ℝ] V)
    (_hle : Module.finrank ℝ LabelCoeff ≤ Module.finrank ℝ V)
    (hrank :
      Module.finrank ℝ (LinearMap.range B) = Module.finrank ℝ LabelCoeff) :
    verticalDefect B S = ⊥ := by
  have hrn := LinearMap.finrank_range_add_finrank_ker B
  have hker0 : Module.finrank ℝ (LinearMap.ker B) = 0 := by
    have : Module.finrank ℝ LabelCoeff =
        Module.finrank ℝ (LinearMap.range B) +
          Module.finrank ℝ (LinearMap.ker B) := by
      simpa using hrn.symm
    omega
  have hker : LinearMap.ker B = ⊥ :=
    (Submodule.finrank_eq_zero).mp hker0
  exact verticalDefect_eq_bot_of_ker_eq_bot B S hker

theorem spanCalibration_of_finrank_range
    [FiniteDimensional ℝ V]
    (B S : LabelCoeff →ₗ[ℝ] V)
    (hle : Module.finrank ℝ LabelCoeff ≤ Module.finrank ℝ V)
    (hrank :
      Module.finrank ℝ (LinearMap.range B) = Module.finrank ℝ LabelCoeff) :
    SpanCalibration B S := by
  rw [spanCalibration_iff_verticalDefect_eq_bot]
  exact verticalDefect_eq_bot_of_finrank_range B S hle hrank

/-! ## 5. Horizontal defect and two-sided functionality -/

/-- Horizontal defect: image of `ker S` under `B`. -/
def horizontalDefect (B S : LabelCoeff →ₗ[ℝ] V) : Submodule ℝ V :=
  (LinearMap.ker S).map B

theorem horizontalDefect_eq_bot_iff
    (B S : LabelCoeff →ₗ[ℝ] V) :
    horizontalDefect B S = ⊥ ↔ LinearMap.ker S ≤ LinearMap.ker B := by
  constructor
  · intro h c hc
    rw [LinearMap.mem_ker]
    have hm : B c ∈ horizontalDefect B S := ⟨c, hc, rfl⟩
    simp [h] at hm
    exact hm
  · intro h
    apply le_antisymm
    · rintro v ⟨c, hc, rfl⟩
      have hb : B c = 0 := LinearMap.mem_ker.mp (h hc)
      simpa [hb]
    · exact bot_le

/-- Forward graph package already owned by the span module, restated. -/
theorem forward_graph_iff
    (B S : LabelCoeff →ₗ[ℝ] V) :
    SpanCalibration B S ↔ verticalDefect B S = ⊥ :=
  spanCalibration_iff_verticalDefect_eq_bot B S

theorem forward_graph_iff_ker_le
    (B S : LabelCoeff →ₗ[ℝ] V) :
    verticalDefect B S = ⊥ ↔ LinearMap.ker B ≤ LinearMap.ker S :=
  verticalDefect_eq_bot_iff B S

/-- Reverse graph on `range S` is a function iff the horizontal defect vanishes. -/
theorem reverse_functional_iff_horizontalDefect_eq_bot
    (B S : LabelCoeff →ₗ[ℝ] V) :
    (∀ {w : V}, w ∈ LinearMap.range S →
        ∃! u : V, (u, w) ∈ comparisonRelation B S) ↔
      horizontalDefect B S = ⊥ := by
  constructor
  · intro h
    rw [horizontalDefect_eq_bot_iff]
    intro c hc
    rw [LinearMap.mem_ker]
    have hw : (0 : V) ∈ LinearMap.range S := ⟨c, LinearMap.mem_ker.mp hc⟩
    rcases (h hw).exists with ⟨u, hu⟩
    have h0 : ((0 : V), (0 : V)) ∈ comparisonRelation B S := ⟨0, by simp [pairSynthesis]⟩
    have hBc : (B c, (0 : V)) ∈ comparisonRelation B S := by
      refine ⟨c, ?_⟩
      ext
      · simp [pairSynthesis]
      · simpa [pairSynthesis] using LinearMap.mem_ker.mp hc
    have hu0 := (h hw).unique hu h0
    have huBc := (h hw).unique hu hBc
    exact (hu0.symm.trans huBc).symm
  · intro hbot w hw
    rw [horizontalDefect_eq_bot_iff] at hbot
    rcases hw with ⟨c, rfl⟩
    refine ⟨B c, ⟨c, by simp [pairSynthesis]⟩, ?_⟩
    intro u hu
    rcases hu with ⟨c', hc'⟩
    have hB : B c' = u := by
      simpa [pairSynthesis] using congrArg Prod.fst hc'
    have hS : S c' = S c := by
      simpa [pairSynthesis] using congrArg Prod.snd hc'
    have hker : c' - c ∈ LinearMap.ker S := by
      rw [LinearMap.mem_ker, map_sub, hS, sub_self]
    have : B (c' - c) = 0 := LinearMap.mem_ker.mp (hbot hker)
    have hBeq : B c' = B c := by
      simpa [map_sub, sub_eq_zero] using this
    exact hB.symm.trans hBeq

theorem both_directions_functional_iff_ker_eq
    (B S : LabelCoeff →ₗ[ℝ] V) :
    verticalDefect B S = ⊥ ∧ horizontalDefect B S = ⊥ ↔
      LinearMap.ker B = LinearMap.ker S := by
  constructor
  · intro ⟨hv, hh⟩
    exact le_antisymm
      ((verticalDefect_eq_bot_iff B S).mp hv)
      ((horizontalDefect_eq_bot_iff B S).mp hh)
  · intro h
    constructor
    · exact (verticalDefect_eq_bot_iff B S).mpr (by rw [h])
    · exact (horizontalDefect_eq_bot_iff B S).mpr (by rw [h])

end
end D0.Geometry.A4DRelativeAEGraphificationClosure
