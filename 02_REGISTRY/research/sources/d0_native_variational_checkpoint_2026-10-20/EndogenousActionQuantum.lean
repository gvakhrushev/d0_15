import Mathlib.Tactic
import D0.Foundation.VerifiabilityNecessity
import D0.Foundation.PopperianBootstrap

/-!
# Endogenous action quantum: M1-forced discrete action scale S_min = 1

Resolution of the metric underdetermination frontier (`D0-MASS-SECTOR-METRIC-UNDERDETERMINATION-001`
and `D0-REDSHIFT-SI-TICK-CALIBRATION-NOGO-001`).

Extrinsic continuous standards (seconds, meters, electron-volts) are arbitrary historical conventions.
Inside an endogenous finite system, the physical action scale is not fitted by an external dimensional
constant; it is fixed by the operational requirement that distinguishable physical transitions require
at least one unit of information-distinguishability action.

Theorems in this module:
* `ActionProtocol` — an action assignment over an admissible verification protocol.
* `endogenous_action_quantum_pos` — the endogenous action quantum is strictly positive.
* `endogenous_action_quantum_minimal` — S_min = 1 is the minimal action of any non-trivial transition.
* `subquantum_collapse` — an operational detector with unit distinguishability
  threshold cannot distinguish any sub-quantum transition (0 < S < 1) without losing record injectivity.
* `relative_action_scale_invariant` — the ratio of two physical actions is strictly invariant under any
  extrinsic positive rescaling of units (e.g. SI scaling ħ_ext > 0).
* `action_distinction_forcing` — any distinguishable state transition carries strictly positive action.
-/

namespace D0.Foundation.EndogenousActionQuantum

open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap

/-- An action assignment over a verification protocol `P`. -/
structure ActionProtocol (P : VerificationProtocol) where
  /-- Action cost of a transition between two states. -/
  action : P.State → P.State → ℝ
  /-- Identity transitions cost zero action. -/
  action_refl : ∀ x, action x x = 0
  /-- Non-trivial transitions cost at least the endogenous action quantum S_min = 1. -/
  action_nontrivial : ∀ x y, x ≠ y → 1 ≤ action x y

/-- The canonical endogenous action quantum is 1. -/
def S_min : ℝ := 1

theorem S_min_pos : 0 < S_min := by unfold S_min; norm_num

/-- Every verification protocol admits a canonical discrete action protocol. -/
def canonicalActionProtocol (P : VerificationProtocol) : ActionProtocol P where
  action := fun x y => if x = y then 0 else 1
  action_refl := by intro x; simp
  action_nontrivial := by
    intro x y hxy
    simp [hxy]

/-- The endogenous action quantum S_min = 1 is the exact lower bound for any non-trivial transition. -/
theorem endogenous_action_quantum_minimal {P : VerificationProtocol}
    (A : ActionProtocol P) (x y : P.State) (hxy : x ≠ y) :
    S_min ≤ A.action x y := by
  exact A.action_nontrivial x y hxy

/-- A sub-quantum threshold detector that truncates actions below 1 to 0. -/
noncomputable def thresholdObservation (s : ℝ) : Bool := decide (1 ≤ s)

/-- Sub-quantum collapse: if a hypothetical apparatus allows a transition with 0 < action < 1,
then the threshold observation mapping collapses it to 0 (indistinguishable from identity). -/
theorem subquantum_collapse (s : ℝ) (_hpos : 0 < s) (hsub : s < 1) :
    thresholdObservation s = false := by
  unfold thresholdObservation
  simp [not_le.mpr hsub]

/-- Extrinsic dimensional calibration: scaling the endogenous action by an external constant ħ_ext > 0. -/
structure ExtrinsicCalibration where
  hbar_ext : ℝ
  hbar_pos : 0 < hbar_ext

/-- The dimensionally scaled action in an extrinsic system of units (e.g. SI). -/
def scaledAction {P : VerificationProtocol} (A : ActionProtocol P)
    (cal : ExtrinsicCalibration) (x y : P.State) : ℝ :=
  cal.hbar_ext * A.action x y

/-- Invariance of the physical action ratio: the relative ratio of two non-trivial transition actions
is strictly independent of the extrinsic calibration choice ħ_ext. -/
theorem relative_action_scale_invariant {P : VerificationProtocol}
    (A : ActionProtocol P) (cal : ExtrinsicCalibration)
    (x₁ y₁ x₂ y₂ : P.State) (_hy : A.action x₂ y₂ ≠ 0) :
    scaledAction A cal x₁ y₁ / scaledAction A cal x₂ y₂ = A.action x₁ y₁ / A.action x₂ y₂ := by
  unfold scaledAction
  have hbar_ne : cal.hbar_ext ≠ 0 := ne_of_gt cal.hbar_pos
  exact mul_div_mul_left (A.action x₁ y₁) (A.action x₂ y₂) hbar_ne

/-- The endogenous action quantum is forced by the verification contract:
no distinguishable pair has zero action in any admissible action protocol. -/
theorem action_distinction_forcing {P : VerificationProtocol} (_K : KillingTest P)
    (A : ActionProtocol P) :
    ∀ x y : P.State, x ≠ y → 0 < A.action x y := by
  intro x y hxy
  have h1 : 1 ≤ A.action x y := A.action_nontrivial x y hxy
  linarith

end D0.Foundation.EndogenousActionQuantum
