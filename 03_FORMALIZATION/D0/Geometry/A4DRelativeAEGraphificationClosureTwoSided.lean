import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic
import D0.Geometry.A4DRelativeAEComparisonSpan

import D0.Geometry.A4DRelativeAEGraphificationClosure
import D0.Geometry.A4DRelativeAEGraphificationClosureRank

/-!
# Graphification closure — horizontal defect / two-sided functionality

Companion to `A4DRelativeAEGraphificationClosure` (§5).
-/

namespace D0.Geometry.A4DRelativeAEGraphificationClosure

open D0
open D0.Geometry.A4DRelativeAEComparisonSpan
open scoped InnerProductSpace

noncomputable section

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

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
