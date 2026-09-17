import D0.Core.BornQuadraticOrigin
import D0.Cosmology.PhysicalRedshiftDetectionPassport
import Mathlib.Tactic

/-!
# Finite phase-cycle frequency realization

This module constructs the abstract frequency passport from finite detector data.  A full phase
cycle is four applications of the already-owned quarter-turn `J`.  A preregistered protocol fixes
one positive number of completed cycles and one positive base window before either side is read.
At refinement depth `n` the window is `baseWindow * internalScale n`, and frequency is the finite
cycle count divided by that window.

The construction proves the self-return frequency covariance rather than assuming a frequency
sequence.  It therefore supplies an in-repository realization of
`PreregisteredSelfReturnFrequencyProtocol` and inherits the physical-redshift and drift theorems.
It does not claim that an arbitrary laboratory apparatus realizes this finite phase counter; that
last representation remains an application obligation.

The sharp boundary is also formalized.  For raw registrations with independently variable cycle
counts and windows, every positive ratio is realizable.  More strongly, the exact ratio factors
into the D0 redshift times a count defect and a normalized-window defect.  Consequently any rival
ratio which preserves the registered depths must change at least one of those two data.  This is a
structural reductio, not an enumeration of rival models.
-/

namespace D0.Cosmology.PhaseCycleFrequencyRealization

open D0
open D0.Cosmology
open D0.Cosmology.SelfUnfoldingObservableRelations
open D0.Cosmology.PhysicalRedshiftDetectionPassport
open D0.Evolution.PhiFractalTickDynamics
open D0.IM

/-! ## Finite phase return -/

/-- Four finite quarter-turn registrations return every phase quadrature to itself. -/
theorem phaseQuarterTurn_four (v : PhaseQuadrature) :
    J (J (J (J v))) = v := by
  cases v
  simp [J, phaseQuarterTurn]

/-- Three quarter turns are not already a full cycle; the four-step owner is non-vacuous. -/
theorem phaseQuarterTurn_three_not_full :
    ∃ v : PhaseQuadrature, J (J (J v)) ≠ v := by
  refine ⟨{ re := 1, im := 0 }, ?_⟩
  norm_num [J, phaseQuarterTurn]

/-- Advance through a finite number of completed four-turn cycles. -/
def fullCycleAdvance : Nat → PhaseQuadrature → PhaseQuadrature
  | 0, v => v
  | k + 1, v => fullCycleAdvance k (J (J (J (J v))))

/-- Every finite count accepted by the counter consists of genuine full returns. -/
theorem completed_phase_cycles_are_returns (k : Nat) (v : PhaseQuadrature) :
    fullCycleAdvance k v = v := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp [fullCycleAdvance, phaseQuarterTurn_four, ih]

/-! ## Preregistered finite cycle counter -/

/-- Data frozen before comparing the emitter and observer registrations. -/
structure FixedCycleWindowProtocol where
  completedCycles : Nat
  completedCycles_pos : 0 < completedCycles
  baseWindow : ℝ
  baseWindow_pos : 0 < baseWindow

/-- The same base detector window transported along the internally owned scale ladder. -/
noncomputable def detectorWindow (P : FixedCycleWindowProtocol) (n : Nat) : ℝ :=
  P.baseWindow * internalScale n

/-- Frequency is a finite count of completed four-turn returns divided by the registered window. -/
noncomputable def cycleFrequencyReadout (P : FixedCycleWindowProtocol) (n : Nat) : ℝ :=
  (P.completedCycles : ℝ) / detectorWindow P n

theorem internalScale_pos (n : Nat) : 0 < internalScale n := by
  exact pow_pos (by linarith [phi_gt_one]) n

theorem detectorWindow_pos (P : FixedCycleWindowProtocol) (n : Nat) :
    0 < detectorWindow P n := by
  exact mul_pos P.baseWindow_pos (internalScale_pos n)

theorem completedCycles_cast_pos (P : FixedCycleWindowProtocol) :
    (0 : ℝ) < P.completedCycles := by
  exact_mod_cast P.completedCycles_pos

theorem cycleFrequencyReadout_pos (P : FixedCycleWindowProtocol) (n : Nat) :
    0 < cycleFrequencyReadout P n := by
  exact div_pos (completedCycles_cast_pos P) (detectorWindow_pos P n)

/-- The fixed count cancels and the self-unfolding window forces one-step contraction by `phi^-1`. -/
theorem cycleFrequencyReadout_one_step (P : FixedCycleWindowProtocol) (n : Nat) :
    cycleFrequencyReadout P (n + 1) =
      cycleFrequencyReadout P n * phi⁻¹ := by
  have hphi : phi ≠ 0 := ne_of_gt (lt_trans (by norm_num) phi_gt_one)
  unfold cycleFrequencyReadout detectorWindow internalScale
  rw [pow_succ]
  field_simp [ne_of_gt P.baseWindow_pos,
    ne_of_gt (internalScale_pos n),
    hphi]

/-- The finite phase counter constructs the abstract self-return frequency protocol. -/
noncomputable def phaseCycleFrequencyProtocol (P : FixedCycleWindowProtocol) :
    PreregisteredSelfReturnFrequencyProtocol where
  readout := cycleFrequencyReadout P
  readout_pos := cycleFrequencyReadout_pos P
  tickMultiplier := phi⁻¹
  tickMultiplier_pos := tick_weight_mem_unit.1
  tickMultiplier_lt_one := tick_weight_mem_unit.2
  selfReturnClosure := tick_weight_satisfies_split
  oneStepCovariance := cycleFrequencyReadout_one_step P

/-- The concrete finite counter inherits the physical/internal redshift equality. -/
theorem phase_cycle_frequency_ratio_eq_internal
    (P : FixedCycleWindowProtocol) (c : FrequencyComparison) :
    physicalOnePlusRedshift
        (phaseCycleFrequencyProtocol P).toRawFrequencyProtocol c =
      onePlusInternalRedshift c.observerDepth c.emitterDepth :=
  physicalOnePlusRedshift_eq_internal (phaseCycleFrequencyProtocol P) c

/-- It also inherits the parameter-free one-tick redshift drift relation. -/
theorem phase_cycle_frequency_drift_relation
    (P : FixedCycleWindowProtocol) (c : FrequencyComparison) :
    physicalRedshift
          (phaseCycleFrequencyProtocol P).toRawFrequencyProtocol c.oneTickLater -
        physicalRedshift
          (phaseCycleFrequencyProtocol P).toRawFrequencyProtocol c =
      (phi - 1) *
        (1 + physicalRedshift
          (phaseCycleFrequencyProtocol P).toRawFrequencyProtocol c) :=
  physical_redshift_drift_relation (phaseCycleFrequencyProtocol P) c

/-! ## Raw cycle/window factorization and structural no-go -/

/-- One raw detector registration before count/window covariance has been imposed. -/
structure RawCycleWindowRegistration where
  depth : Nat
  completedCycles : Nat
  completedCycles_pos : 0 < completedCycles
  window : ℝ
  window_pos : 0 < window

/-- Two independently stored raw registrations, with their depth order fixed. -/
structure RawCycleWindowComparison where
  emitter : RawCycleWindowRegistration
  observer : RawCycleWindowRegistration
  emission_precedes_observation : emitter.depth ≤ observer.depth

/-- Raw registered frequency. -/
noncomputable def rawCycleFrequency (r : RawCycleWindowRegistration) : ℝ :=
  (r.completedCycles : ℝ) / r.window

/-- The part of a raw window not explained by the internally owned scale at its depth. -/
noncomputable def normalizedWindow (r : RawCycleWindowRegistration) : ℝ :=
  r.window / internalScale r.depth

/-- Ratio of the two independently registered raw frequencies. -/
noncomputable def rawCycleOnePlusRedshift (c : RawCycleWindowComparison) : ℝ :=
  rawCycleFrequency c.emitter / rawCycleFrequency c.observer

theorem raw_completedCycles_cast_pos (r : RawCycleWindowRegistration) :
    (0 : ℝ) < r.completedCycles := by
  exact_mod_cast r.completedCycles_pos

theorem normalizedWindow_pos (r : RawCycleWindowRegistration) :
    0 < normalizedWindow r := by
  exact div_pos r.window_pos (internalScale_pos r.depth)

/-- Division-free transport of the internal scale between the two registered depths. -/
theorem internalScale_transport (c : RawCycleWindowComparison) :
    internalScale c.emitter.depth *
        onePlusInternalRedshift c.observer.depth c.emitter.depth =
      internalScale c.observer.depth := by
  have hdepth : c.emitter.depth + (c.observer.depth - c.emitter.depth) =
      c.observer.depth := by
    simpa [Nat.add_comm] using
      (Nat.sub_add_cancel c.emission_precedes_observation)
  unfold internalScale onePlusInternalRedshift depthGap
  calc
    phi ^ c.emitter.depth * phi ^ (c.observer.depth - c.emitter.depth) =
        phi ^ (c.emitter.depth + (c.observer.depth - c.emitter.depth)) := by
          rw [pow_add]
    _ = phi ^ c.observer.depth := by rw [hdepth]

theorem internalScale_ratio_eq_internal (c : RawCycleWindowComparison) :
    internalScale c.observer.depth / internalScale c.emitter.depth =
      onePlusInternalRedshift c.observer.depth c.emitter.depth := by
  rw [div_eq_iff (ne_of_gt (internalScale_pos c.emitter.depth))]
  simpa [mul_comm] using (internalScale_transport c).symm

/-- **Exact universal factorization.** Every raw ratio equals the D0 term times exactly two
possible defects: relative cycle count and relative normalized window. -/
theorem raw_cycle_window_defect_factorization (c : RawCycleWindowComparison) :
    rawCycleOnePlusRedshift c =
      ((c.emitter.completedCycles : ℝ) / c.observer.completedCycles) *
        (normalizedWindow c.observer / normalizedWindow c.emitter) *
          onePlusInternalRedshift c.observer.depth c.emitter.depth := by
  rw [← internalScale_ratio_eq_internal c]
  unfold rawCycleOnePlusRedshift rawCycleFrequency normalizedWindow
  field_simp [ne_of_gt c.emitter.window_pos, ne_of_gt c.observer.window_pos,
    ne_of_gt (raw_completedCycles_cast_pos c.emitter),
    ne_of_gt (raw_completedCycles_cast_pos c.observer),
    ne_of_gt (internalScale_pos c.emitter.depth),
    ne_of_gt (internalScale_pos c.observer.depth)]

/-- Keeping both the count and normalized window fixed is sufficient for the D0 ratio. -/
theorem same_count_and_normalizedWindow_forces_internal
    (c : RawCycleWindowComparison)
    (hcount : c.emitter.completedCycles = c.observer.completedCycles)
    (hwindow : normalizedWindow c.emitter = normalizedWindow c.observer) :
    rawCycleOnePlusRedshift c =
      onePlusInternalRedshift c.observer.depth c.emitter.depth := by
  rw [raw_cycle_window_defect_factorization, hcount, hwindow]
  field_simp [ne_of_gt (raw_completedCycles_cast_pos c.observer),
    ne_of_gt (normalizedWindow_pos c.observer)]

/-- **Structural reductio.** A rival ratio under the same depth protocol must alter the cycle
count or the normalized detector window.  There is no third hidden case in this carrier. -/
theorem rival_requires_count_or_normalizedWindow_defect
    (c : RawCycleWindowComparison)
    (hrival : rawCycleOnePlusRedshift c ≠
      onePlusInternalRedshift c.observer.depth c.emitter.depth) :
    c.emitter.completedCycles ≠ c.observer.completedCycles ∨
      normalizedWindow c.emitter ≠ normalizedWindow c.observer := by
  by_contra h
  push Not at h
  exact hrival (same_count_and_normalizedWindow_forces_internal c h.1 h.2)

/-- Raw positive count/window registrations can realize an arbitrary positive ratio. -/
noncomputable def rawCycleComparisonForRatio (r : ℝ) (hr : 0 < r) :
    RawCycleWindowComparison where
  emitter :=
    { depth := 0
      completedCycles := 1
      completedCycles_pos := by omega
      window := 1
      window_pos := by norm_num }
  observer :=
    { depth := 1
      completedCycles := 1
      completedCycles_pos := by omega
      window := r
      window_pos := hr }
  emission_precedes_observation := by norm_num

theorem raw_cycle_window_realises_every_positive_ratio (r : ℝ) (hr : 0 < r) :
    rawCycleOnePlusRedshift (rawCycleComparisonForRatio r hr) = r := by
  simp [rawCycleOnePlusRedshift, rawCycleFrequency, rawCycleComparisonForRatio]

/-- Raw cycle counting without a fixed count/window law does not force the D0 ratio. -/
theorem raw_cycle_window_does_not_force_redshift :
    ∃ c : RawCycleWindowComparison,
      rawCycleOnePlusRedshift c ≠
        onePlusInternalRedshift c.observer.depth c.emitter.depth := by
  let c := rawCycleComparisonForRatio 1 (by norm_num)
  refine ⟨c, ?_⟩
  rw [raw_cycle_window_realises_every_positive_ratio]
  norm_num [onePlusInternalRedshift, depthGap, c, rawCycleComparisonForRatio]
  exact ne_of_lt phi_gt_one

/-- Capstone: finite return, concrete frequency realization, redshift transfer, exact defect
factorization, and the raw no-go coexist in one theorem. -/
theorem finite_phase_cycle_frequency_realization :
    (∀ v : PhaseQuadrature, J (J (J (J v))) = v) ∧
    (∀ k : Nat, ∀ v : PhaseQuadrature, fullCycleAdvance k v = v) ∧
    (∀ P : FixedCycleWindowProtocol, ∀ c : FrequencyComparison,
      physicalOnePlusRedshift
          (phaseCycleFrequencyProtocol P).toRawFrequencyProtocol c =
        onePlusInternalRedshift c.observerDepth c.emitterDepth) ∧
    (∀ c : RawCycleWindowComparison,
      rawCycleOnePlusRedshift c =
        ((c.emitter.completedCycles : ℝ) / c.observer.completedCycles) *
          (normalizedWindow c.observer / normalizedWindow c.emitter) *
            onePlusInternalRedshift c.observer.depth c.emitter.depth) ∧
    (∀ c : RawCycleWindowComparison,
      rawCycleOnePlusRedshift c ≠
          onePlusInternalRedshift c.observer.depth c.emitter.depth →
        c.emitter.completedCycles ≠ c.observer.completedCycles ∨
          normalizedWindow c.emitter ≠ normalizedWindow c.observer) ∧
    (∃ c : RawCycleWindowComparison,
      rawCycleOnePlusRedshift c ≠
        onePlusInternalRedshift c.observer.depth c.emitter.depth) :=
  ⟨phaseQuarterTurn_four,
    completed_phase_cycles_are_returns,
    phase_cycle_frequency_ratio_eq_internal,
    raw_cycle_window_defect_factorization,
    rival_requires_count_or_normalizedWindow_defect,
    raw_cycle_window_does_not_force_redshift⟩

end D0.Cosmology.PhaseCycleFrequencyRealization
