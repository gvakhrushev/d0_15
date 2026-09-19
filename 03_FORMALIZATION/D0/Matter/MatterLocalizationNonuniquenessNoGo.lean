import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Real.Basic
import D0.Foundation.M1Predicate
import D0.Foundation.ObservableCompletionCanonicity
import D0.Geometry.ArchiveRefinementTower

namespace D0.Matter

open D0
open D0.Foundation
open D0.Foundation.ObservableCompletionCanonicity

/-!
# D0.Matter.MatterLocalizationNonuniquenessNoGo

Owners:
- `D0-MATTER-LOCALIZATION-NONUNIQUENESS-NOGO-001`
- `D0-MATTER-LOCALIZATION-OBSERVABLE-CANONICITY-001`

Structural no-go on canonical matter source localization:
The constraint of anomaly neutrality fixes only the TOTAL source:
  ∑_{x} s(x) = R.anomalySum = 0.
This constraint is severely underdetermined at the local point level:
At n = 0 (L = 2, two points 0 and 1):
  s_A = ![1, -1] has sum 0
  s_B = ![2, -2] has sum 0
Yet s_A ≠ s_B (s_A 0 = 1 ≠ 2 = s_B 0).
Therefore, anomaly cancellation does NOT force a unique physical local source.

Synthesis via `ObservableCompletionCanonicity`:
- Raw completion: local source s(x) is non-unique.
- Observable readout: total sum ∑_x s(x) is M1-forced to be 0 for anomaly-free matter.
-/

/-- Source candidate A on Fin 2: s_A = ![1, -1]. -/
def sourceCandidateA : Fin 2 → ℝ := ![1, -1]

/-- Source candidate B on Fin 2: s_B = ![2, -2]. -/
def sourceCandidateB : Fin 2 → ℝ := ![2, -2]

theorem sum_candidate_A_zero : ∑ i : Fin 2, sourceCandidateA i = 0 := by
  unfold sourceCandidateA
  simp [Fin.sum_univ_two]

theorem sum_candidate_B_zero : ∑ i : Fin 2, sourceCandidateB i = 0 := by
  unfold sourceCandidateB
  simp [Fin.sum_univ_two]

theorem candidate_A_ne_B : sourceCandidateA ≠ sourceCandidateB := by
  intro h
  have h0 : sourceCandidateA 0 = sourceCandidateB 0 := by rw [h]
  unfold sourceCandidateA sourceCandidateB at h0
  norm_num at h0

/-- **D0-MATTER-LOCALIZATION-NONUNIQUENESS-NOGO-001 (Owner)**:
Proves that two distinct local matter sources evaluate to the identical zero total anomaly sum. -/
theorem matter_localization_nonuniqueness_nogo_owner :
    (∑ i : Fin 2, sourceCandidateA i = 0) ∧
    (∑ i : Fin 2, sourceCandidateB i = 0) ∧
    (sourceCandidateA ≠ sourceCandidateB) :=
  ⟨sum_candidate_A_zero, sum_candidate_B_zero, candidate_A_ne_B⟩

/-- Admissible neutral source completions on Fin 2. -/
def AdmissibleNeutralSource (s : Fin 2 → ℝ) : Prop :=
  (∑ i : Fin 2, s i) = 0

/-- Observable total charge readout. -/
def totalChargeReadout (s : Fin 2 → ℝ) : ℝ :=
  ∑ i : Fin 2, s i

/-- **D0-MATTER-LOCALIZATION-OBSERVABLE-CANONICITY-001 (Owner)**:
Canonicity of the global neutrality readout:
While the local source function s(x) is non-unique, the total charge readout is M1-forced to be 0. -/
theorem matter_localization_observable_canonicity_owner :
    M1Forced (CompletionForcesReadout AdmissibleNeutralSource totalChargeReadout) 0 := by
  have h0 : AdmissibleNeutralSource (fun _ => 0) := by
    unfold AdmissibleNeutralSource
    simp
  have hconst : ∀ s, AdmissibleNeutralSource s → totalChargeReadout s = totalChargeReadout (fun _ => 0) := by
    intro s hs
    unfold totalChargeReadout
    rw [hs]
    simp
  have h_m1 := constant_readout_m1_forced AdmissibleNeutralSource totalChargeReadout (fun _ => 0) h0 hconst
  have h_val : totalChargeReadout (fun _ => 0) = 0 := by
    unfold totalChargeReadout; simp
  rw [h_val] at h_m1
  exact h_m1

end D0.Matter
