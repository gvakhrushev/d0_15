import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic
import D0.Geometry.A4DRelativeAEComparisonSpan

import D0.Geometry.A4DRelativeAEGraphificationClosure

/-!
# Graphification closure — residual-rank / full-rank ⇒ graph

Companion to `A4DRelativeAEGraphificationClosure` (§§3–4).
-/

namespace D0.Geometry.A4DRelativeAEGraphificationClosure

open D0
open D0.Geometry.A4DRelativeAEComparisonSpan
open scoped InnerProductSpace

noncomputable section

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

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

end
end D0.Geometry.A4DRelativeAEGraphificationClosure
