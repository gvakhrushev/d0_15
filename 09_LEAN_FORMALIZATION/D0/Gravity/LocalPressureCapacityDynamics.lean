import D0.Cosmology.ArchiveHomogeneousState
import D0.Gravity.PressureCapacityBalance
import Mathlib.Tactic

/-!
# Local pressure-capacity dynamics and the packing-bound homogeneity no-go

This module upgrades the three integer examples in `PressureCapacityBalance` to a universal local
real-valued law.  The owned finite statement is deliberately about **acceleration of the local
expansion readout**, not expansion itself:

`nextTheta - theta = kappa * (feedbackPressure - capacityPressure)`.

Thus balance preserves an already existing rate, feedback excess accelerates it, and capacity
excess brakes it.  Sufficient capacity excess reverses the next-step rate.  No FLRW, SI clock,
matter-density or measured-dark-sector identification is made here.

The final block separates two statements often conflated in black-hole language.  A pointwise upper
packing bound does not force a density field to be homogeneous (one parametric counterexample on
`Bool` is enough).  Homogeneity follows only from the stronger premise that every local site
saturates the same bound.  The current D0 black-hole predicate is boundary-capacity saturation, so
it cannot silently supply that stronger bulk-density premise.
-/

namespace D0.Gravity.LocalPressureCapacityDynamics

/-- Signed local imbalance: positive is feedback-dominated, negative is capacity-dominated. -/
def pressureImbalance (feedbackPressure capacityPressure : ℝ) : ℝ :=
  feedbackPressure - capacityPressure

/-- One-step acceleration of the local expansion readout. -/
def expansionAcceleration
    (kappa feedbackPressure capacityPressure : ℝ) : ℝ :=
  kappa * pressureImbalance feedbackPressure capacityPressure

/-- The next local expansion rate after one unit internal step. -/
def nextExpansionRate
    (theta kappa feedbackPressure capacityPressure : ℝ) : ℝ :=
  theta + expansionAcceleration kappa feedbackPressure capacityPressure

/-- Exact balance produces zero acceleration. -/
theorem balanced_acceleration_zero
    (kappa pressure : ℝ) :
    expansionAcceleration kappa pressure pressure = 0 := by
  simp [expansionAcceleration, pressureImbalance]

/-- Balance preserves the current expansion rate; it does not force that rate itself to vanish. -/
theorem balanced_preserves_existing_rate
    (theta kappa pressure : ℝ) :
    nextExpansionRate theta kappa pressure pressure = theta := by
  simp [nextExpansionRate, balanced_acceleration_zero]

/-- Feedback pressure above capacity gives positive local expansion acceleration. -/
theorem feedback_excess_accelerates
    (kappa feedbackPressure capacityPressure : ℝ)
    (hkappa : 0 < kappa) (hdom : capacityPressure < feedbackPressure) :
    0 < expansionAcceleration kappa feedbackPressure capacityPressure := by
  exact mul_pos hkappa (sub_pos.mpr hdom)

/-- Capacity pressure above feedback gives negative acceleration: braking. -/
theorem capacity_excess_brakes
    (kappa feedbackPressure capacityPressure : ℝ)
    (hkappa : 0 < kappa) (hdom : feedbackPressure < capacityPressure) :
    expansionAcceleration kappa feedbackPressure capacityPressure < 0 := by
  exact mul_neg_of_pos_of_neg hkappa (sub_neg.mpr hdom)

/-- A capacity excess larger than the current positive rate reverses the next-step motion. -/
theorem capacity_hypercompensation_reverses
    (theta kappa feedbackPressure capacityPressure : ℝ)
    (hhyper : theta < kappa * (capacityPressure - feedbackPressure)) :
    nextExpansionRate theta kappa feedbackPressure capacityPressure < 0 := by
  unfold nextExpansionRate expansionAcceleration pressureImbalance
  linarith

/-- Local pressure fields induce a local acceleration field without a homogeneity premise. -/
def localAccelerationField
    {X : Type} (kappa : ℝ) (feedbackPressure capacityPressure : X → ℝ) : X → ℝ :=
  fun x => expansionAcceleration kappa (feedbackPressure x) (capacityPressure x)

/-- For nonzero response coefficient, unequal local imbalances force unequal accelerations. -/
theorem unequal_imbalance_forces_unequal_acceleration
    {X : Type} (kappa : ℝ) (feedbackPressure capacityPressure : X → ℝ)
    (x y : X) (hkappa : kappa ≠ 0)
    (hne : pressureImbalance (feedbackPressure x) (capacityPressure x) ≠
      pressureImbalance (feedbackPressure y) (capacityPressure y)) :
    localAccelerationField kappa feedbackPressure capacityPressure x ≠
      localAccelerationField kappa feedbackPressure capacityPressure y := by
  intro hacc
  apply hne
  unfold localAccelerationField expansionAcceleration at hacc
  exact (mul_left_cancel₀ hkappa hacc)

/-- A homogeneous imbalance field gives a homogeneous acceleration field. -/
theorem homogeneous_imbalance_gives_homogeneous_acceleration
    {X : Type} (kappa : ℝ) (feedbackPressure capacityPressure : X → ℝ)
    (hhom : D0.Cosmology.isHomogeneous
      (fun x => pressureImbalance (feedbackPressure x) (capacityPressure x))) :
    D0.Cosmology.isHomogeneous
      (localAccelerationField kappa feedbackPressure capacityPressure) := by
  rcases hhom with ⟨c, hc⟩
  refine ⟨kappa * c, ?_⟩
  funext x
  unfold localAccelerationField expansionAcceleration
  rw [congrFun hc x]

/-- A mere pointwise packing ceiling. -/
def BelowPackingLimit {X : Type} (density : X → ℝ) (rhoMax : ℝ) : Prop :=
  ∀ x, density x ≤ rhoMax

/-- The strictly stronger premise that every site saturates one common ceiling. -/
def SaturatesPackingLimitEverywhere
    {X : Type} (density : X → ℝ) (rhoMax : ℝ) : Prop :=
  ∀ x, density x = rhoMax

/-- **Packing-bound homogeneity NO-GO.** A common upper bound does not force homogeneity. -/
theorem packing_limit_does_not_force_homogeneity :
    ∃ density : Bool → ℝ,
      BelowPackingLimit density 1 ∧ ¬ D0.Cosmology.isHomogeneous density := by
  let density : Bool → ℝ := fun x => if x then 1 else 0
  refine ⟨density, ?_, ?_⟩
  · intro x
    cases x <;> simp [density]
  · intro hhom
    rcases hhom with ⟨c, hc⟩
    have hfalse := congrFun hc false
    have htrue := congrFun hc true
    simp [density] at hfalse htrue
    linarith

/-- Uniform saturation of the same local bound really does force homogeneity. -/
theorem everywhere_saturation_forces_homogeneity
    {X : Type} (density : X → ℝ) (rhoMax : ℝ)
    (hsat : SaturatesPackingLimitEverywhere density rhoMax) :
    D0.Cosmology.isHomogeneous density := by
  refine ⟨rhoMax, ?_⟩
  funext x
  exact hsat x

/-- Capstone: the signed local dynamics and the exact logical boundary on density uniformity. -/
theorem local_pressure_capacity_dynamics_and_packing_boundary :
    (∀ kappa pressure : ℝ,
      expansionAcceleration kappa pressure pressure = 0) ∧
    (∀ theta kappa pressure : ℝ,
      nextExpansionRate theta kappa pressure pressure = theta) ∧
    (∃ density : Bool → ℝ,
      BelowPackingLimit density 1 ∧ ¬ D0.Cosmology.isHomogeneous density) :=
  ⟨balanced_acceleration_zero, balanced_preserves_existing_rate,
    packing_limit_does_not_force_homogeneity⟩

end D0.Gravity.LocalPressureCapacityDynamics
