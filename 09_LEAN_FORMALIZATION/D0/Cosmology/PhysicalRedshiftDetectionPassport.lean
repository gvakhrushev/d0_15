import D0.Cosmology.SelfUnfoldingObservableRelations
import Mathlib.Tactic

/-!
# Physical redshift detection passport

This module closes the next *conditional* edge after the internal self-unfolding redshift law.
It does not identify an arbitrary positive detector number with a frequency.  Instead it asks what
an independently preregistered two-readout protocol must provide for the standard frequency ratio

`1 + z_phys = nu_em / nu_obs`

to inherit the internal law `1 + z_D0 = phi^(o-e)`.

The protocol is deliberately structural.  Its positive readout is advanced by one constant
contracting multiplier, while the same multiplier must satisfy the already-owned self-return
closure `p + p^2 = 1`.  The multiplier is therefore proved, rather than declared, to be `phi^-1`.
Consequently the unknown absolute frequency normalization cancels between the two independently
registered readouts.

The module also proves the sharp boundary.  A raw pair of positive frequency readouts can realise
*every* positive ratio.  More precisely, every departure from the D0 ratio factors through a
nontrivial relative-calibration defect.  Thus double registration alone does not force redshift;
double registration plus the preregistered self-return covariance does, and any rival needs exactly
one additional outcome-affecting scale datum.  This is a structural factorization/no-go, not an
enumeration of alternative cosmologies.
-/

namespace D0.Cosmology.PhysicalRedshiftDetectionPassport

open D0
open D0.Cosmology
open D0.Cosmology.SelfUnfoldingObservableRelations
open D0.Evolution.PhiFractalTickDynamics
open D0.IM

/-- A positive detector-frequency readout indexed by registered refinement depth.  No relation
between different depths is assumed at this raw layer. -/
structure RawFrequencyProtocol where
  readout : Nat → ℝ
  readout_pos : ∀ n, 0 < readout n

/-- The two typed registrations used in one redshift comparison.  The roles are not inferred after
seeing a value: emission and observation depths are fixed as distinct fields of the protocol. -/
structure FrequencyComparison where
  emitterDepth : Nat
  observerDepth : Nat
  emission_precedes_observation : emitterDepth ≤ observerDepth

/-- Repeat the observation side one refinement tick later while retaining the same emission record. -/
def FrequencyComparison.oneTickLater (c : FrequencyComparison) : FrequencyComparison where
  emitterDepth := c.emitterDepth
  observerDepth := c.observerDepth + 1
  emission_precedes_observation :=
    le_trans c.emission_precedes_observation (Nat.le_succ c.observerDepth)

/-- Standard dimensionless frequency-ratio observable. -/
noncomputable def physicalOnePlusRedshift
    (P : RawFrequencyProtocol) (c : FrequencyComparison) : ℝ :=
  P.readout c.emitterDepth / P.readout c.observerDepth

/-- Additive physical-redshift coordinate associated to the two registered readouts. -/
noncomputable def physicalRedshift
    (P : RawFrequencyProtocol) (c : FrequencyComparison) : ℝ :=
  physicalOnePlusRedshift P c - 1

/-- Calibration inferred at one depth relative to the internally owned active tick ladder. -/
noncomputable def relativeCalibration (P : RawFrequencyProtocol) (n : Nat) : ℝ :=
  P.readout n / ladderAmount n

theorem ladderAmount_pos (n : Nat) : 0 < ladderAmount n := by
  exact pow_pos tick_weight_mem_unit.1 n

theorem relativeCalibration_pos (P : RawFrequencyProtocol) (n : Nat) :
    0 < relativeCalibration P n := by
  exact div_pos (P.readout_pos n) (ladderAmount_pos n)

/-- A frequency protocol frozen before comparison.  Its multiplier is not set to `phi^-1` by
definition: it is constrained only by positivity, contraction, the self-return equation, and the
same one-step law at every depth. -/
structure PreregisteredSelfReturnFrequencyProtocol extends RawFrequencyProtocol where
  tickMultiplier : ℝ
  tickMultiplier_pos : 0 < tickMultiplier
  tickMultiplier_lt_one : tickMultiplier < 1
  selfReturnClosure : tickMultiplier + tickMultiplier ^ 2 = 1
  oneStepCovariance : ∀ n, readout (n + 1) = readout n * tickMultiplier

/-- The frequency multiplier is forced by self-return closure; it is not a fit parameter. -/
theorem protocol_tickMultiplier_eq_phi_inv
    (P : PreregisteredSelfReturnFrequencyProtocol) :
    P.tickMultiplier = phi⁻¹ :=
  phi_split_forces_tick_weight
    P.tickMultiplier_pos P.tickMultiplier_lt_one P.selfReturnClosure

/-- Hence the preregistered detector uses the already-owned D0 active-tick covariance. -/
theorem protocol_oneStep_phi_inv
    (P : PreregisteredSelfReturnFrequencyProtocol) (n : Nat) :
    P.readout (n + 1) = P.readout n * phi⁻¹ := by
  rw [P.oneStepCovariance n, protocol_tickMultiplier_eq_phi_inv P]

/-- Iterating the same fixed detector protocol introduces no additional per-depth catalogue. -/
theorem protocol_readout_advance
    (P : PreregisteredSelfReturnFrequencyProtocol) (start steps : Nat) :
    P.readout (start + steps) = P.readout start * (phi⁻¹) ^ steps := by
  induction steps with
  | zero => simp
  | succ steps ih =>
      rw [Nat.add_succ, protocol_oneStep_phi_inv, ih, pow_succ]
      ring

/-- Closed form: the only free value is the single absolute normalization at depth zero. -/
theorem protocol_readout_closed_form
    (P : PreregisteredSelfReturnFrequencyProtocol) (n : Nat) :
    P.readout n = P.readout 0 * ladderAmount n := by
  simpa [ladderAmount] using protocol_readout_advance P 0 n

/-- The absolute normalization is constant across depth and therefore cannot affect a ratio. -/
theorem protocol_relativeCalibration_constant
    (P : PreregisteredSelfReturnFrequencyProtocol) (n : Nat) :
    relativeCalibration P.toRawFrequencyProtocol n = P.readout 0 := by
  rw [relativeCalibration, protocol_readout_closed_form]
  field_simp [ne_of_gt (ladderAmount_pos n)]

/-- Division-free transport law between the two independent registrations. -/
theorem protocol_frequency_transport
    (P : PreregisteredSelfReturnFrequencyProtocol)
    (c : FrequencyComparison) :
    P.readout c.observerDepth *
        onePlusInternalRedshift c.observerDepth c.emitterDepth =
      P.readout c.emitterDepth := by
  let d := c.observerDepth - c.emitterDepth
  have hdepth : c.emitterDepth + d = c.observerDepth := by
    exact Nat.add_sub_of_le c.emission_precedes_observation
  have hread := protocol_readout_advance P c.emitterDepth d
  rw [hdepth] at hread
  have hphi : phi⁻¹ * phi = (1 : ℝ) := by
    exact inv_mul_cancel₀ (ne_of_gt (lt_trans (by norm_num) phi_gt_one))
  have hpowers : (phi⁻¹) ^ d * phi ^ d = (1 : ℝ) := by
    rw [← mul_pow, hphi, one_pow]
  rw [onePlusInternalRedshift, depthGap]
  rw [hread]
  calc
    (P.readout c.emitterDepth * (phi⁻¹) ^ d) * phi ^ d =
        P.readout c.emitterDepth * ((phi⁻¹) ^ d * phi ^ d) := by ring
    _ = P.readout c.emitterDepth := by rw [hpowers]; ring

/-- **Physical passport theorem.** Under the preregistered self-return protocol, the measured
frequency ratio is exactly the internal relative-depth redshift.  Absolute calibration cancels. -/
theorem physicalOnePlusRedshift_eq_internal
    (P : PreregisteredSelfReturnFrequencyProtocol)
    (c : FrequencyComparison) :
    physicalOnePlusRedshift P.toRawFrequencyProtocol c =
      onePlusInternalRedshift c.observerDepth c.emitterDepth := by
  rw [physicalOnePlusRedshift, div_eq_iff
    (ne_of_gt (P.readout_pos c.observerDepth))]
  simpa [mul_comm] using (protocol_frequency_transport P c).symm

theorem physicalRedshift_eq_internal
    (P : PreregisteredSelfReturnFrequencyProtocol)
    (c : FrequencyComparison) :
    physicalRedshift P.toRawFrequencyProtocol c =
      internalRedshift c.observerDepth c.emitterDepth := by
  rw [physicalRedshift, internalRedshift,
    physicalOnePlusRedshift_eq_internal]

/-- The same passport transfers the already-owned parameter-free drift law to two repeated
physical observations of the same emission registration. -/
theorem physical_redshift_drift_relation
    (P : PreregisteredSelfReturnFrequencyProtocol)
    (c : FrequencyComparison) :
    physicalRedshift P.toRawFrequencyProtocol
        c.oneTickLater -
      physicalRedshift P.toRawFrequencyProtocol c =
        (phi - 1) * (1 + physicalRedshift P.toRawFrequencyProtocol c) := by
  let d : RepeatedDepthDetection :=
    { emitterDepth := c.emitterDepth
      firstObserverDepth := c.observerDepth
      emission_precedes_first := c.emission_precedes_observation }
  have hd := internal_redshift_drift_relation d
  rw [physicalRedshift_eq_internal, physicalRedshift_eq_internal]
  simpa [internalRedshiftDrift, d] using hd

/-- The canonical internal ladder itself is a non-vacuous preregistered frequency protocol. -/
noncomputable def canonicalFrequencyProtocol :
    PreregisteredSelfReturnFrequencyProtocol where
  readout := ladderAmount
  readout_pos := ladderAmount_pos
  tickMultiplier := phi⁻¹
  tickMultiplier_pos := tick_weight_mem_unit.1
  tickMultiplier_lt_one := tick_weight_mem_unit.2
  selfReturnClosure := tick_weight_satisfies_split
  oneStepCovariance := ladder_constant_ratio

/-- The internal redshift is exactly the ratio of the canonical active-tick readouts. -/
theorem ladder_ratio_eq_internal (c : FrequencyComparison) :
    ladderAmount c.emitterDepth / ladderAmount c.observerDepth =
      onePlusInternalRedshift c.observerDepth c.emitterDepth := by
  simpa [physicalOnePlusRedshift, canonicalFrequencyProtocol] using
    physicalOnePlusRedshift_eq_internal canonicalFrequencyProtocol c

/-- **Exact defect factorization for every raw detector.** Any observed ratio is the D0 ratio
multiplied by the relative-calibration defect.  This identifies the precise additional information
needed by every rival without enumerating rivals. -/
theorem raw_redshift_calibration_defect_factorization
    (P : RawFrequencyProtocol) (c : FrequencyComparison) :
    physicalOnePlusRedshift P c =
      (relativeCalibration P c.emitterDepth /
        relativeCalibration P c.observerDepth) *
          onePlusInternalRedshift c.observerDepth c.emitterDepth := by
  rw [← ladder_ratio_eq_internal c]
  unfold physicalOnePlusRedshift relativeCalibration
  field_simp [ne_of_gt (P.readout_pos c.observerDepth),
    ne_of_gt (ladderAmount_pos c.emitterDepth),
    ne_of_gt (ladderAmount_pos c.observerDepth)]

/-- Equal calibration across the independently registered sides is sufficient for the D0 ratio. -/
theorem equal_relativeCalibration_forces_internal_redshift
    (P : RawFrequencyProtocol) (c : FrequencyComparison)
    (hcal : relativeCalibration P c.emitterDepth =
      relativeCalibration P c.observerDepth) :
    physicalOnePlusRedshift P c =
      onePlusInternalRedshift c.observerDepth c.emitterDepth := by
  rw [raw_redshift_calibration_defect_factorization, hcal]
  field_simp [ne_of_gt (relativeCalibration_pos P c.observerDepth)]

/-- **M1-shaped reductio.** If a rival ratio differs while the same two-readout protocol is kept,
the two registrations necessarily carry different relative calibrations: an additional mandatory
outcome-affecting scale datum. -/
theorem rival_redshift_requires_relativeCalibration_defect
    (P : RawFrequencyProtocol) (c : FrequencyComparison)
    (hrival : physicalOnePlusRedshift P c ≠
      onePlusInternalRedshift c.observerDepth c.emitterDepth) :
    relativeCalibration P c.emitterDepth ≠
      relativeCalibration P c.observerDepth := by
  intro hcal
  exact hrival (equal_relativeCalibration_forces_internal_redshift P c hcal)

/-- Unit-depth comparison used by the raw-protocol universality/no-go theorem. -/
def unitDepthComparison : FrequencyComparison where
  emitterDepth := 0
  observerDepth := 1
  emission_precedes_observation := by omega

/-- A raw positive detector can realise an arbitrary positive ratio at the two fixed depths. -/
noncomputable def rawProtocolForRatio (r : ℝ) (hr : 0 < r) : RawFrequencyProtocol where
  readout n := if n = 0 then r else 1
  readout_pos n := by
    split_ifs
    · exact hr
    · norm_num

/-- Raw double registration is ratio-surjective: positivity alone cannot select `phi`. -/
theorem raw_double_detection_realises_every_positive_ratio
    (r : ℝ) (hr : 0 < r) :
    physicalOnePlusRedshift (rawProtocolForRatio r hr) unitDepthComparison = r := by
  simp [physicalOnePlusRedshift, rawProtocolForRatio, unitDepthComparison]

/-- **Sharp NO-GO.** Two positive independently stored readouts, without the preregistered
self-return covariance, do not force the D0 redshift even on the first depth step. -/
theorem raw_double_detection_does_not_force_redshift :
    ∃ P : RawFrequencyProtocol, ∃ c : FrequencyComparison,
      physicalOnePlusRedshift P c ≠
        onePlusInternalRedshift c.observerDepth c.emitterDepth := by
  let P := rawProtocolForRatio 1 (by norm_num)
  refine ⟨P, unitDepthComparison, ?_⟩
  rw [raw_double_detection_realises_every_positive_ratio]
  norm_num [onePlusInternalRedshift, depthGap, unitDepthComparison]
  exact ne_of_lt phi_gt_one

/-- Capstone: the bridge, drift transfer, structural rival factorization, and raw no-go coexist.
The positive statement is conditional on a preregistered detector representation; the negative
statement proves why that condition cannot be deleted. -/
theorem physical_redshift_detection_passport :
    (∀ P : PreregisteredSelfReturnFrequencyProtocol,
      P.tickMultiplier = phi⁻¹) ∧
    (∀ P : PreregisteredSelfReturnFrequencyProtocol, ∀ c : FrequencyComparison,
      physicalOnePlusRedshift P.toRawFrequencyProtocol c =
        onePlusInternalRedshift c.observerDepth c.emitterDepth) ∧
    (∀ P : PreregisteredSelfReturnFrequencyProtocol, ∀ c : FrequencyComparison,
      physicalRedshift P.toRawFrequencyProtocol
          c.oneTickLater -
        physicalRedshift P.toRawFrequencyProtocol c =
          (phi - 1) * (1 + physicalRedshift P.toRawFrequencyProtocol c)) ∧
    (∀ P : RawFrequencyProtocol, ∀ c : FrequencyComparison,
      physicalOnePlusRedshift P c =
        (relativeCalibration P c.emitterDepth /
          relativeCalibration P c.observerDepth) *
            onePlusInternalRedshift c.observerDepth c.emitterDepth) ∧
    (∃ P : RawFrequencyProtocol, ∃ c : FrequencyComparison,
      physicalOnePlusRedshift P c ≠
        onePlusInternalRedshift c.observerDepth c.emitterDepth) :=
  ⟨protocol_tickMultiplier_eq_phi_inv,
    physicalOnePlusRedshift_eq_internal,
    physical_redshift_drift_relation,
    raw_redshift_calibration_defect_factorization,
    raw_double_detection_does_not_force_redshift⟩

end D0.Cosmology.PhysicalRedshiftDetectionPassport
