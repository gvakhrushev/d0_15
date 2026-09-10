import D0.Cosmology.SelfUnfoldingObservableRelations
import Mathlib.Tactic

/-!
# SI duration of a refinement tick: structural scale-gauge boundary

The finite self-unfolding protocol fixes ratios between successive ticks, but contains no number
with units of seconds.  This module makes that boundary constructive instead of declaring it by a
propositional placeholder.

For every positive SI duration `secondsPerTick` there is a valid calibration, and every positive
SI rate `rho` is realised by the reciprocal calibration.  Rescaling the duration leaves every
internal redshift comparison unchanged while changing `rho`.  Hence no SI value of `rho` is
identifiable from the internal comparison protocol alone.  This is one parametric countermodel
family, not an enumeration of possible clocks.
-/

namespace D0.Bridge.RedshiftSITickCalibrationNoGo

open D0.Cosmology.SelfUnfoldingObservableRelations

/-- External assignment of an SI duration to one already-defined refinement tick. -/
structure RefinementSITimeCalibration where
  secondsPerTick : ℝ
  secondsPerTick_pos : 0 < secondsPerTick

/-- SI tick rate associated with a calibration. -/
noncomputable def rho (cal : RefinementSITimeCalibration) : ℝ :=
  1 / cal.secondsPerTick

/-- Common positive rescaling of the external clock section. -/
noncomputable def rescale
    (cal : RefinementSITimeCalibration) (lambda : ℝ) (hlambda : 0 < lambda) :
    RefinementSITimeCalibration where
  secondsPerTick := lambda * cal.secondsPerTick
  secondsPerTick_pos := mul_pos hlambda cal.secondsPerTick_pos

/-- The dimensionless internal comparison is deliberately independent of the SI clock section. -/
noncomputable def calibratedInternalComparison
    (_cal : RefinementSITimeCalibration) (observerDepth emitterDepth : Nat) : ℝ :=
  onePlusInternalRedshift observerDepth emitterDepth

theorem rho_pos (cal : RefinementSITimeCalibration) : 0 < rho cal := by
  exact one_div_pos.mpr cal.secondsPerTick_pos

/-- Clock rescaling cannot change any internal redshift comparison. -/
theorem rescaling_preserves_internal_comparison
    (cal : RefinementSITimeCalibration) (lambda : ℝ) (hlambda : 0 < lambda)
    (observerDepth emitterDepth : Nat) :
    calibratedInternalComparison (rescale cal lambda hlambda) observerDepth emitterDepth =
      calibratedInternalComparison cal observerDepth emitterDepth := by
  rfl

/-- Clock rescaling changes the SI tick rate inversely. -/
theorem rho_rescale
    (cal : RefinementSITimeCalibration) (lambda : ℝ) (hlambda : 0 < lambda) :
    rho (rescale cal lambda hlambda) = rho cal / lambda := by
  unfold rho rescale
  field_simp [ne_of_gt hlambda, ne_of_gt cal.secondsPerTick_pos]

/-- Every positive SI rate is compatible with the same internal protocol. -/
noncomputable def calibrationForRate (rate : ℝ) (hrate : 0 < rate) :
    RefinementSITimeCalibration where
  secondsPerTick := 1 / rate
  secondsPerTick_pos := one_div_pos.mpr hrate

theorem rho_calibrationForRate (rate : ℝ) (hrate : 0 < rate) :
    rho (calibrationForRate rate hrate) = rate := by
  unfold rho calibrationForRate
  field_simp [ne_of_gt hrate]

/-- Two observationally identical internal protocols can carry distinct SI rates. -/
theorem same_internal_protocol_distinct_si_rates
    (cal : RefinementSITimeCalibration) :
    ∃ cal' : RefinementSITimeCalibration,
      (∀ observerDepth emitterDepth,
        calibratedInternalComparison cal' observerDepth emitterDepth =
          calibratedInternalComparison cal observerDepth emitterDepth) ∧
      rho cal' ≠ rho cal := by
  let cal' := rescale cal 2 (by norm_num)
  refine ⟨cal', ?_, ?_⟩
  · intro observerDepth emitterDepth
    exact rescaling_preserves_internal_comparison cal 2 (by norm_num) _ _
  · rw [rho_rescale cal 2 (by norm_num)]
    intro h
    have hp := rho_pos cal
    linarith

/-- **Scale-gauge NO-GO.** No real number can be the SI rate shared by every admissible clock
section.  Selecting one requires an external calibration or an additional dimensionless clock
ratio; the dimensionless refinement protocol cannot supply it. -/
theorem no_si_rho_identifiable_from_internal_protocol (rate : ℝ) :
    ¬ (∀ cal : RefinementSITimeCalibration, rho cal = rate) := by
  intro hall
  let cal1 : RefinementSITimeCalibration := ⟨1, by norm_num⟩
  let cal2 : RefinementSITimeCalibration := ⟨2, by norm_num⟩
  have h1 := hall cal1
  have h2 := hall cal2
  norm_num [rho, cal1, cal2] at h1 h2
  linarith

/-- Capstone: positive-rate surjectivity and rescaling non-identifiability coexist. -/
theorem redshift_si_tick_calibration_nogo :
    (∀ rate : ℝ, 0 < rate →
      ∃ cal : RefinementSITimeCalibration, rho cal = rate) ∧
    (∀ cal : RefinementSITimeCalibration,
      ∃ cal' : RefinementSITimeCalibration,
        (∀ observerDepth emitterDepth,
          calibratedInternalComparison cal' observerDepth emitterDepth =
            calibratedInternalComparison cal observerDepth emitterDepth) ∧
        rho cal' ≠ rho cal) ∧
    (∀ rate : ℝ, ¬ (∀ cal : RefinementSITimeCalibration, rho cal = rate)) :=
  ⟨fun rate hrate => ⟨calibrationForRate rate hrate,
      rho_calibrationForRate rate hrate⟩,
    same_internal_protocol_distinct_si_rates,
    no_si_rho_identifiable_from_internal_protocol⟩

end D0.Bridge.RedshiftSITickCalibrationNoGo
