import D0.Synthesis.SceneTraceHeatCapacity
import D0.Synthesis.MassSectorMetricUnderdetermination
import D0.Bridge.RedshiftSITickCalibrationNoGo
import Mathlib.Tactic

/-!
# Finite seam capacity and the typed selector boundary

This owner reuses the frozen co-vertex cut and the existing positive shell-gap and SI tick
calibration APIs. Its selector lemma records only a positive rational coefficient and an unchanged
unit tag. It does not identify either coefficient with a black-hole mass or a Bondi clock.
-/

universe u

namespace D0.Synthesis.SeamSectionBoundary

open D0.Synthesis.SceneTraceHeatCapacity

private def coVertexEquiv : Fin 32 ≃ {v : sceneGraph.V // v ∈ coRegionSet} where
  toFun i := ⟨⟨i.val, by omega⟩, by
    change (⟨i.val, by omega⟩ : Fin 33) ≠ u₀
    intro h
    have hv := congrArg Fin.val h
    simp [u₀] at hv
    omega⟩
  invFun v := ⟨v.val.val, by
    have hne : v.val.val ≠ 32 := by
      intro h
      have hEq : v.val = u₀ := Fin.ext (by simpa [u₀] using h)
      exact v.property hEq
    omega⟩
  left_inv i := by
    apply Fin.ext
    rfl
  right_inv v := by
    apply Subtype.ext
    apply Fin.ext
    rfl

private noncomputable instance coVertexFintype :
    Fintype {v : sceneGraph.V // v ∈ coRegionSet} :=
  Fintype.ofEquiv (Fin 32) coVertexEquiv

/-- The frozen co-vertex region contains exactly 32 of the graph's own vertices. -/
theorem coVertex_card : Fintype.card {v : sceneGraph.V // v ∈ coRegionSet} = 32 := by
  classical
  calc
    Fintype.card {v : sceneGraph.V // v ∈ coRegionSet} = Fintype.card (Fin 32) :=
      Fintype.card_congr coVertexEquiv.symm
    _ = 32 := Fintype.card_fin 32

/-- The co-vertex cut is inherited from the frozen scene owner. -/
theorem coVertex_cut : D0.Gravity.BoundaryCutWeight sceneGraph coRegionSet = 20 :=
  covertex_cut

/-- The existing quarter-cut rule gives capacity five for this co-vertex region. -/
theorem coVertex_boundary_capacity :
    D0.Gravity.BoundaryCapacity sceneGraph coRegionSet = 5 := by
  unfold D0.Gravity.BoundaryCapacity
  rw [coVertex_cut]
  norm_num

/-- Capacity density is measured per vertex of the frozen co-vertex region. -/
noncomputable def coVertexCapacityDensity : ℚ :=
  D0.Gravity.BoundaryCapacity sceneGraph coRegionSet /
    (Fintype.card {v : sceneGraph.V // v ∈ coRegionSet} : ℚ)

/-- The exact frozen co-vertex capacity density is `5/32`. -/
theorem coVertex_capacity_density_eq : coVertexCapacityDensity = 5 / 32 := by
  unfold coVertexCapacityDensity
  rw [coVertex_boundary_capacity]
  rw [coVertex_card]
  norm_num

/-- The positive internal multiplier supplied by the frozen density. -/
noncomputable def frozenInternalMultiplier : ℚ := 1 + coVertexCapacityDensity

theorem frozen_internal_multiplier_eq : frozenInternalMultiplier = 37 / 32 := by
  unfold frozenInternalMultiplier
  rw [coVertex_capacity_density_eq]
  norm_num

/-- A selector carries only a positive dimensionless rational coefficient and a fixed unit tag. -/
structure PositiveTypedSelector (UnitTag : Type u) where
  coefficient : ℚ
  unitTag : UnitTag
  coefficient_pos : 0 < coefficient

/-- Multiply the dimensionless coefficient while retaining its unit tag. -/
def rescaleSelector {UnitTag : Type u} (m : ℚ) (hm : 0 < m)
    (s : PositiveTypedSelector UnitTag) : PositiveTypedSelector UnitTag where
  coefficient := m * s.coefficient
  unitTag := s.unitTag
  coefficient_pos := mul_pos hm s.coefficient_pos

theorem rescaleSelector_ne {UnitTag : Type u} (s : PositiveTypedSelector UnitTag)
    (m : ℚ) (hm : 0 < m) (hm_ne_one : m ≠ 1) : rescaleSelector m hm s ≠ s := by
  intro h
  have hc := congrArg PositiveTypedSelector.coefficient h
  dsimp [rescaleSelector] at hc
  have hc' : m * s.coefficient = 1 * s.coefficient := by simpa using hc
  have hm_eq_one : m = 1 := mul_right_cancel₀ (ne_of_gt s.coefficient_pos) hc'
  exact hm_ne_one hm_eq_one

/-- Positivity and a shared unit tag alone admit a distinct scaled selector. -/
theorem positive_selector_nonunique_from_type_and_sign {UnitTag : Type u}
    (s : PositiveTypedSelector UnitTag) (m : ℚ) (hm : 0 < m) (hm_ne_one : m ≠ 1) :
    ∃ t : PositiveTypedSelector UnitTag,
      t.unitTag = s.unitTag ∧ t.coefficient = m * s.coefficient ∧
      0 < t.coefficient ∧ t ≠ s := by
  refine ⟨rescaleSelector m hm s, rfl, rfl, ?_, rescaleSelector_ne s m hm hm_ne_one⟩
  exact (rescaleSelector m hm s).coefficient_pos

/-- Baseline positive selector with the requested fixed unit tag. -/
def unitSelector {UnitTag : Type u} (tag : UnitTag) : PositiveTypedSelector UnitTag where
  coefficient := 1
  unitTag := tag
  coefficient_pos := by norm_num

/-- The `37/32` density multiplier witnesses nonuniqueness in every fixed selector type. -/
theorem frozen_multiplier_selector_witness {UnitTag : Type u} (tag : UnitTag) :
    ∃ t : PositiveTypedSelector UnitTag,
      t.unitTag = tag ∧ t.coefficient = 37 / 32 ∧ 0 < t.coefficient ∧
      t ≠ unitSelector tag := by
  have hmpos : 0 < frozenInternalMultiplier := by
    rw [frozen_internal_multiplier_eq]
    norm_num
  have hmne : frozenInternalMultiplier ≠ 1 := by
    rw [frozen_internal_multiplier_eq]
    norm_num
  obtain ⟨t, htag, hcoef, hpos, hne⟩ :=
    positive_selector_nonunique_from_type_and_sign
      (unitSelector tag) frozenInternalMultiplier hmpos hmne
  refine ⟨t, htag, ?_, hpos, ?_⟩
  · calc
      t.coefficient = frozenInternalMultiplier * (unitSelector tag).coefficient := hcoef
      _ = 37 / 32 := by simp [unitSelector, frozen_internal_multiplier_eq]
  · exact hne

/-- A selector-fixing equation plus the fixed unit tag determines exactly one selector. -/
theorem selector_fixing_equation_unique {UnitTag : Type u} (tag : UnitTag) :
    ∃! s : PositiveTypedSelector UnitTag, s.coefficient = 1 ∧ s.unitTag = tag := by
  refine ⟨unitSelector tag, ?_, ?_⟩
  · exact ⟨by simp [unitSelector], rfl⟩
  · intro t ht
    rcases t with ⟨c, uTag, hcPos⟩
    have hcoef : (unitSelector tag).coefficient = c := by
      simpa [unitSelector] using ht.1.symm
    have hunit : (unitSelector tag).unitTag = uTag := by
      simpa [unitSelector] using ht.2.symm
    cases hcoef
    cases hunit
    rfl

/-- The frozen scaled witness is excluded by the hostile equation `coefficient = 1`. -/
theorem frozen_multiplier_violates_selector_fixing_equation {UnitTag : Type u} (tag : UnitTag) :
    ¬ (rescaleSelector frozenInternalMultiplier
      (by rw [frozen_internal_multiplier_eq]; norm_num) (unitSelector tag)).coefficient = 1 := by
  change ¬ frozenInternalMultiplier * (1 : ℚ) = 1
  rw [frozen_internal_multiplier_eq]
  norm_num

/-- Existing shell-gap data also admits positive nontrivial rescaling. -/
theorem positive_shell_gap_rescaling_nonunique
    (gap : D0.Synthesis.MassSectorMetricUnderdetermination.PositiveShellGap)
    (m : ℚ) (hm : 0 < m) (hm_ne_one : m ≠ 1) :
    ∃ gap' : D0.Synthesis.MassSectorMetricUnderdetermination.PositiveShellGap,
      gap'.value = m * gap.value ∧ gap' ≠ gap := by
  refine ⟨⟨m * gap.value, mul_pos hm gap.h_pos⟩, rfl, ?_⟩
  intro h
  have hc := congrArg
    D0.Synthesis.MassSectorMetricUnderdetermination.PositiveShellGap.value h
  have hc' : m * gap.value = 1 * gap.value := by simpa using hc
  have hm_eq_one : m = 1 := mul_right_cancel₀ (ne_of_gt gap.h_pos) hc'
  exact hm_ne_one hm_eq_one

/-- The same frozen multiplier rescales an existing SI tick calibration while preserving its
internal comparisons and changing its SI rate. This remains an external tick calibration; it does
not identify that tick with Bondi retarded time. -/
theorem frozen_multiplier_clock_calibration_nonunique
    (cal : D0.Bridge.RedshiftSITickCalibrationNoGo.RefinementSITimeCalibration) :
    ∃ cal' : D0.Bridge.RedshiftSITickCalibrationNoGo.RefinementSITimeCalibration,
      (∀ observerDepth emitterDepth,
        D0.Bridge.RedshiftSITickCalibrationNoGo.calibratedInternalComparison
          cal' observerDepth emitterDepth =
        D0.Bridge.RedshiftSITickCalibrationNoGo.calibratedInternalComparison
          cal observerDepth emitterDepth) ∧
      D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal' ≠
        D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal := by
  let lambda : ℝ := (frozenInternalMultiplier : ℚ)
  have hlam : 0 < lambda := by
    rw [show lambda = (frozenInternalMultiplier : ℚ) by rfl,
      frozen_internal_multiplier_eq]
    norm_num
  have hlam_ne : lambda ≠ 1 := by
    rw [show lambda = (frozenInternalMultiplier : ℚ) by rfl,
      frozen_internal_multiplier_eq]
    norm_num
  let cal' := D0.Bridge.RedshiftSITickCalibrationNoGo.rescale cal lambda hlam
  refine ⟨cal', ?_, ?_⟩
  · intro observerDepth emitterDepth
    exact D0.Bridge.RedshiftSITickCalibrationNoGo.rescaling_preserves_internal_comparison
      cal lambda hlam observerDepth emitterDepth
  · rw [D0.Bridge.RedshiftSITickCalibrationNoGo.rho_rescale cal lambda hlam]
    intro h
    have hrho := D0.Bridge.RedshiftSITickCalibrationNoGo.rho_pos cal
    have hmul :
        D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal =
          lambda * D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal := by
      calc
        D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal =
            (D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal / lambda) * lambda := by
              field_simp [ne_of_gt hlam]
        _ = lambda * D0.Bridge.RedshiftSITickCalibrationNoGo.rho cal := by
              rw [h]
              ring
    have hlambda_eq : (1 : ℝ) = lambda := by
      apply mul_right_cancel₀ (ne_of_gt hrho)
      simpa using hmul
    exact hlam_ne hlambda_eq.symm

end D0.Synthesis.SeamSectionBoundary
