import D0.CondensedAnchor.DetectorSupportGoldenWeight
import D0.Representation.GoldenCoherentMemory
import Mathlib.Tactic

/-!
# One-step golden memory source and the two-tick boundary

The already-owned `fullStep` and golden cylinder measure agree exactly on the two branch
probabilities of a blank one-tick record. This does not identify the law of repeated physical
readouts. The second result gives a strictly positive, normalized two-tick table with the same
one-tick marginals as the owned cylinder law but a different joint probability. Thus an admitted
multi-tick refinement map is still required; independence is not inferred from the one-step gate.

This is a scoped bridge/boundary result. It defines no total D0 action, selector, or physical
multi-tick evolution.
-/

open scoped goldenRatio
open Real

namespace D0.Research.GoldenCylinderOneStepBridge

/-- The actual output of the existing golden full-step on a blank system/record input. -/
def blankGateOutput (a p : ℝ) : Fin 4 → ℝ :=
  (D0.Representation.GoldenCoherentMemory.fullStep a p).mulVec ![1, 0, 0, 0]

theorem blankGateOutput_eq (a p : ℝ) :
    blankGateOutput a p = ![a, 0, 0, p] := by
  simpa [blankGateOutput] using
    D0.Representation.GoldenCoherentMemory.blank_record_evolution a p 1 0

/-- The owned gate closure and orthogonal parameterization force the branch parameter to be
`φ⁻¹`; this identifies the one-step source without a fitted probability. -/
theorem gate_parameter_eq_inv_golden {a p : ℝ}
    (ha : a ^ 2 = p) (hp : p + p ^ 2 = 1) :
    p = φ⁻¹ := by
  have hp_nonneg : 0 ≤ p := by nlinarith [sq_nonneg a, ha]
  have hp_pos : 0 < p := by
    by_contra h
    have hp_le : p ≤ 0 := le_of_not_gt h
    have hp_zero : p = 0 := le_antisymm hp_le hp_nonneg
    rw [hp_zero] at hp
    norm_num at hp
  have hgold : (φ⁻¹ : ℝ) + (φ⁻¹ : ℝ) ^ 2 = 1 :=
    D0.CondensedAnchor.inv_gold_closure
  have hfactor : (p - φ⁻¹) * (p + φ⁻¹ + 1) = 0 := by
    nlinarith [hp, hgold]
  have hphi_pos : 0 < (φ⁻¹ : ℝ) := by positivity
  have hsum_pos : 0 < p + φ⁻¹ + 1 := by linarith
  rcases mul_eq_zero.mp hfactor with h | h
  · linarith
  · linarith

/-- Squared amplitudes of the two recorded branches after the actual one-tick gate. -/
def directBranchMass (a p : ℝ) : ℝ := (blankGateOutput a p 0) ^ 2
def returnBranchMass (a p : ℝ) : ℝ := (blankGateOutput a p 3) ^ 2

/-- The actual one-tick branch masses are `p` and `p²` before identifying `p` with `φ⁻¹`. -/
theorem blank_gate_masses_eq_parameters (a p : ℝ) (ha : a ^ 2 = p) :
    directBranchMass a p = p ∧ returnBranchMass a p = p ^ 2 := by
  simp [directBranchMass, returnBranchMass, blankGateOutput_eq, ha]

/-- The existing blank-record evolution realizes exactly the owned one-letter cylinder weights. -/
theorem blank_gate_matches_one_step_cylinders (a p : ℝ)
    (ha : a ^ 2 = p) (hp : p + p ^ 2 = 1) :
    directBranchMass a p = D0.CondensedAnchor.cylWeight [true] ∧
    returnBranchMass a p = D0.CondensedAnchor.cylWeight [false] := by
  have hstate := blankGateOutput_eq a p
  have hgold := gate_parameter_eq_inv_golden ha hp
  unfold directBranchMass returnBranchMass
  rw [hstate]
  constructor <;> simp [D0.CondensedAnchor.cylWeight, hgold, ha]

/-- A two-tick joint table with a positive correlation perturbation of the product cylinder law.
Its four entries are ordered by `(first readout, second readout)`. -/
noncomputable def correlatedTwoStepMass (p : ℝ) : Bool × Bool → ℝ
  | (true, true) => p ^ 2 + p ^ 4 / 2
  | (true, false) => p ^ 3 - p ^ 4 / 2
  | (false, true) => p ^ 3 - p ^ 4 / 2
  | (false, false) => p ^ 4 + p ^ 4 / 2

theorem correlatedTwoStepMass_positive (p : ℝ)
    (hp : p + p ^ 2 = 1) (hp_pos : 0 < p) :
    ∀ w, 0 < correlatedTwoStepMass p w := by
  have hp_lt_one : p < 1 := by nlinarith [sq_pos_of_pos hp_pos]
  have hfactor_pos : 0 < 1 - p / 2 := by linarith
  have hmixed : 0 < p ^ 3 - p ^ 4 / 2 := by
    rw [show p ^ 3 - p ^ 4 / 2 = p ^ 3 * (1 - p / 2) by ring]
    positivity
  intro w
  rcases w with ⟨b₁, b₂⟩
  cases b₁ <;> cases b₂
  · simp [correlatedTwoStepMass]
    positivity
  · simpa [correlatedTwoStepMass] using hmixed
  · simpa [correlatedTwoStepMass] using hmixed
  · simp [correlatedTwoStepMass]
    positivity

theorem correlatedTwoStepMass_marginals (p : ℝ)
    (hp : p + p ^ 2 = 1) :
    correlatedTwoStepMass p (true, true) + correlatedTwoStepMass p (true, false) = p ∧
    correlatedTwoStepMass p (false, true) + correlatedTwoStepMass p (false, false) = p ^ 2 ∧
    correlatedTwoStepMass p (true, true) + correlatedTwoStepMass p (false, true) = p ∧
    correlatedTwoStepMass p (true, false) + correlatedTwoStepMass p (false, false) = p ^ 2 := by
  have hp1 : p ^ 2 + p ^ 3 = p := by
    nlinarith [congrArg (fun t : ℝ => t * p) hp]
  have hp2 : p ^ 3 + p ^ 4 = p ^ 2 := by
    nlinarith [congrArg (fun t : ℝ => t * p ^ 2) hp]
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [correlatedTwoStepMass] <;>
    nlinarith [hp1, hp2]

/-- Both coordinates of the correlated two-tick witness have exactly the actual one-tick gate
marginals, while its joint law differs from the product cylinder. -/
theorem correlatedTwoStepMass_marginals_are_gate_marginals (a p : ℝ)
    (ha : a ^ 2 = p) (hp : p + p ^ 2 = 1) :
    correlatedTwoStepMass p (true, true) + correlatedTwoStepMass p (true, false) =
        directBranchMass a p ∧
    correlatedTwoStepMass p (false, true) + correlatedTwoStepMass p (false, false) =
        returnBranchMass a p ∧
    correlatedTwoStepMass p (true, true) + correlatedTwoStepMass p (false, true) =
        directBranchMass a p ∧
    correlatedTwoStepMass p (true, false) + correlatedTwoStepMass p (false, false) =
        returnBranchMass a p := by
  have hm := correlatedTwoStepMass_marginals p hp
  have hg := blank_gate_masses_eq_parameters a p ha
  simpa [hg.1, hg.2] using hm

theorem correlatedTwoStepMass_total (p : ℝ)
    (hp : p + p ^ 2 = 1) :
    correlatedTwoStepMass p (true, true) +
      correlatedTwoStepMass p (true, false) +
      correlatedTwoStepMass p (false, true) +
      correlatedTwoStepMass p (false, false) = 1 := by
  have hm := correlatedTwoStepMass_marginals p hp
  calc
    _ = (correlatedTwoStepMass p (true, true) +
          correlatedTwoStepMass p (true, false)) +
        (correlatedTwoStepMass p (false, true) +
          correlatedTwoStepMass p (false, false)) := by ring
    _ = p + p ^ 2 := by rw [hm.1, hm.2.1]
    _ = 1 := hp

/-- The one-tick branch law fixes both two-tick marginals but does not force the product
cylinder joint: the positive table above assigns a different mass to the `true,true` history. -/
theorem one_step_marginals_do_not_force_product_history (a p : ℝ)
    (ha : a ^ 2 = p) (hp : p + p ^ 2 = 1) :
    correlatedTwoStepMass p (true, true) ≠
      D0.CondensedAnchor.cylWeight [true, true] := by
  have hp_pos : 0 < p := by
    by_contra h
    have hp_nonneg : 0 ≤ p := by nlinarith [sq_nonneg a, ha]
    have hp_le : p ≤ 0 := le_of_not_gt h
    have hp_zero : p = 0 := le_antisymm hp_le hp_nonneg
    rw [hp_zero] at hp
    norm_num at hp
  have hgold := gate_parameter_eq_inv_golden ha hp
  have hprod : D0.CondensedAnchor.cylWeight [true, true] = p ^ 2 := by
    simp [D0.CondensedAnchor.cylWeight, ← hgold]
    ring
  rw [hprod]
  simp [correlatedTwoStepMass]
  have hpos : 0 < p ^ 4 / 2 := by positivity
  linarith

end D0.Research.GoldenCylinderOneStepBridge
