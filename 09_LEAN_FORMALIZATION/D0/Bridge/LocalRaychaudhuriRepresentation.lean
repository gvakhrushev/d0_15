import D0.Gravity.LocalPressureCapacityDynamics
import Mathlib.Tactic

/-!
# Local Raychaudhuri representation and the two-readout dark-sector boundary

The internal D0 law supplies only a signed pressure/capacity acceleration.  This bridge states the
exact additional data needed to read it as local relativistic focusing/defocusing:

* capacity pressure represents self-focusing + shear + active matter focusing;
* feedback pressure represents vorticity + an independently measured dark/archive drive;
* the physical local acceleration readout represents the internal acceleration.

No inhabitant of the representation is asserted.  The bridge therefore does not rename an archive
quantity as measured dark energy.

The second half proves a model-independent identifiability result.  A net readout `dark-matter`
has a common-shift gauge: adding an arbitrary function to both components changes neither the net
field nor any observation that factors through it.  Consequently no algorithm can recover the dark
component from the net field alone.  Supplying the matter/focusing field as a second independent
readout removes the gauge and recovers the dark field uniquely by addition.  This is a structural
reductio, not an enumeration of alternative cosmologies.
-/

namespace D0.Bridge.LocalRaychaudhuriRepresentation

open D0.Gravity.LocalPressureCapacityDynamics

/-- Local focusing load in a timelike Raychaudhuri-shaped normalization.  `activeMatter` denotes
the already unit-normalized `4 pi G (rho + 3p)`-type contribution; this module does not derive that
continuum dictionary. -/
noncomputable def raychaudhuriFocusing
    (theta shearSq activeMatter : ℝ) : ℝ :=
  theta ^ 2 / 3 + shearSq + activeMatter

/-- Local defocusing drive: kinematic vorticity plus the dark/archive response channel. -/
def raychaudhuriDefocusing
    (vorticitySq darkArchiveDrive : ℝ) : ℝ :=
  vorticitySq + darkArchiveDrive

/-- Signed local physical acceleration candidate. -/
noncomputable def raychaudhuriAcceleration
    (theta shearSq activeMatter vorticitySq darkArchiveDrive : ℝ) : ℝ :=
  raychaudhuriDefocusing vorticitySq darkArchiveDrive -
    raychaudhuriFocusing theta shearSq activeMatter

/-- More positive active matter always lowers the local acceleration by the same amount. -/
theorem added_matter_increases_focusing
    (theta shearSq activeMatter vorticitySq darkArchiveDrive delta : ℝ) :
    raychaudhuriAcceleration theta shearSq (activeMatter + delta)
        vorticitySq darkArchiveDrive =
      raychaudhuriAcceleration theta shearSq activeMatter
        vorticitySq darkArchiveDrive - delta := by
  unfold raychaudhuriAcceleration raychaudhuriFocusing raychaudhuriDefocusing
  ring

/-- More dark/archive drive raises the local acceleration by the same amount. -/
theorem added_dark_drive_increases_defocusing
    (theta shearSq activeMatter vorticitySq darkArchiveDrive delta : ℝ) :
    raychaudhuriAcceleration theta shearSq activeMatter
        vorticitySq (darkArchiveDrive + delta) =
      raychaudhuriAcceleration theta shearSq activeMatter
        vorticitySq darkArchiveDrive + delta := by
  unfold raychaudhuriAcceleration raychaudhuriFocusing raychaudhuriDefocusing
  ring

end D0.Bridge.LocalRaychaudhuriRepresentation

namespace D0.Bridge.BridgeAssumption

open D0.Bridge.LocalRaychaudhuriRepresentation

/-- Explicit application interface from the finite D0 pressure/capacity split to independently
registered local physical readouts.  The three representation equalities are data, not axioms or
globally inhabited claims. -/
structure LocalRaychaudhuriRepresentation (X : Type) where
  kappa : ℝ
  kappaPositive : 0 < kappa
  feedbackPressure : X → ℝ
  capacityPressure : X → ℝ
  expansionRate : X → ℝ
  measuredAcceleration : X → ℝ
  shearSq : X → ℝ
  vorticitySq : X → ℝ
  activeMatterFocusing : X → ℝ
  measuredDarkArchiveDrive : X → ℝ
  capacityRepresentsFocusing : ∀ x,
    kappa * capacityPressure x =
      raychaudhuriFocusing (expansionRate x) (shearSq x) (activeMatterFocusing x)
  feedbackRepresentsDefocusing : ∀ x,
    kappa * feedbackPressure x =
      raychaudhuriDefocusing (vorticitySq x) (measuredDarkArchiveDrive x)
  accelerationRepresentsInternal : ∀ x,
    measuredAcceleration x =
      D0.Gravity.LocalPressureCapacityDynamics.expansionAcceleration
        kappa (feedbackPressure x) (capacityPressure x)

end D0.Bridge.BridgeAssumption

namespace D0.Bridge.LocalRaychaudhuriRepresentation

open D0.Gravity.LocalPressureCapacityDynamics
open D0.Bridge.BridgeAssumption

/-- The representation eliminates both internal pressures and yields one coupled physical law. -/
theorem represented_local_acceleration_eq_defocusing_sub_focusing
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X) :
    R.measuredAcceleration x =
      raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x) -
        raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
          (R.activeMatterFocusing x) := by
  rw [R.accelerationRepresentsInternal]
  unfold expansionAcceleration pressureImbalance
  rw [mul_sub, R.feedbackRepresentsDefocusing, R.capacityRepresentsFocusing]

/-- Exact balance gives zero physical acceleration. -/
theorem represented_balance_zero_acceleration
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X)
    (hbalance :
      raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x) =
        raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
          (R.activeMatterFocusing x)) :
    R.measuredAcceleration x = 0 := by
  rw [represented_local_acceleration_eq_defocusing_sub_focusing R x, hbalance]
  ring

/-- Defocusing dominance gives positive measured acceleration. -/
theorem represented_defocusing_dominance_accelerates
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X)
    (hdom :
      raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
          (R.activeMatterFocusing x) <
        raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x)) :
    0 < R.measuredAcceleration x := by
  rw [represented_local_acceleration_eq_defocusing_sub_focusing R x]
  exact sub_pos.mpr hdom

/-- Focusing dominance brakes the local expansion readout. -/
theorem represented_focusing_dominance_brakes
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X)
    (hdom :
      raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x) <
        raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
          (R.activeMatterFocusing x)) :
    R.measuredAcceleration x < 0 := by
  rw [represented_local_acceleration_eq_defocusing_sub_focusing R x]
  exact sub_neg.mpr hdom

/-- Sufficient focusing hypercompensation reverses the next-step local rate. -/
theorem represented_focusing_hypercompensation_reverses
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X)
    (hhyper :
      R.expansionRate x <
        raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
            (R.activeMatterFocusing x) -
          raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x)) :
    R.expansionRate x + R.measuredAcceleration x < 0 := by
  rw [represented_local_acceleration_eq_defocusing_sub_focusing R x]
  linarith

/-- With acceleration, focusing and vorticity independently read, the dark/archive drive is fixed. -/
theorem represented_dark_drive_recovered
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X) :
    R.measuredDarkArchiveDrive x =
      R.measuredAcceleration x +
        raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
          (R.activeMatterFocusing x) - R.vorticitySq x := by
  have h := represented_local_acceleration_eq_defocusing_sub_focusing R x
  unfold raychaudhuriDefocusing at h
  linarith

/-- With acceleration and defocusing independently read, the total focusing load is fixed. -/
theorem represented_focusing_recovered
    {X : Type} (R : LocalRaychaudhuriRepresentation X) (x : X) :
    raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
        (R.activeMatterFocusing x) =
      raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x) -
        R.measuredAcceleration x := by
  rw [represented_local_acceleration_eq_defocusing_sub_focusing R x]
  ring

/-- Abstract two-component decomposition behind every net expansion readout. -/
structure ResponseDecomposition (X : Type) where
  darkDrive : X → ℝ
  focusingLoad : X → ℝ

/-- What a single expansion/acceleration channel can observe. -/
def ResponseDecomposition.net {X : Type} (D : ResponseDecomposition X) : X → ℝ :=
  fun x => D.darkDrive x - D.focusingLoad x

/-- Common-shift gauge of the two unobserved components. -/
def ResponseDecomposition.shift {X : Type}
    (D : ResponseDecomposition X) (g : X → ℝ) : ResponseDecomposition X where
  darkDrive := fun x => D.darkDrive x + g x
  focusingLoad := fun x => D.focusingLoad x + g x

/-- Every common local shift is invisible to the net readout. -/
theorem common_shift_preserves_net
    {X : Type} (D : ResponseDecomposition X) (g : X → ℝ) :
    (D.shift g).net = D.net := by
  funext x
  simp [ResponseDecomposition.net, ResponseDecomposition.shift]

/-- Any nonzero common shift gives a distinct decomposition with exactly the same observation. -/
theorem nonzero_common_shift_gives_observational_twin
    {X : Type} (D : ResponseDecomposition X) (g : X → ℝ) (x : X)
    (hg : g x ≠ 0) :
    D.shift g ≠ D ∧ (D.shift g).net = D.net := by
  constructor
  · intro heq
    have hdark := congrFun (congrArg ResponseDecomposition.darkDrive heq) x
    simp [ResponseDecomposition.shift] at hdark
    exact hg hdark
  · exact common_shift_preserves_net D g

/-- **Net-only NO-GO.** No universal algorithm recovers the dark component from the net field. -/
theorem no_dark_component_identifiable_from_net
    {X : Type} [Nonempty X] :
    ¬ ∃ recoverDark : (X → ℝ) → (X → ℝ),
      ∀ D : ResponseDecomposition X, recoverDark D.net = D.darkDrive := by
  intro hrecover
  rcases hrecover with ⟨recoverDark, hrecovers⟩
  let zeroD : ResponseDecomposition X :=
    ⟨fun _ => 0, fun _ => 0⟩
  let oneD : ResponseDecomposition X :=
    ⟨fun _ => 1, fun _ => 1⟩
  have hnet : zeroD.net = oneD.net := by
    funext x
    simp [ResponseDecomposition.net, zeroD, oneD]
  have hz := hrecovers zeroD
  have ho := hrecovers oneD
  obtain ⟨x⟩ := ‹Nonempty X›
  have hpoint : zeroD.darkDrive x = oneD.darkDrive x := by
    rw [← congrFun hz x, ← congrFun ho x, hnet]
  simp [zeroD, oneD] at hpoint

/-- The missing second readout is sufficient: net plus focusing recovers dark response pointwise. -/
theorem dark_component_recovered_from_net_and_focusing
    {X : Type} (D : ResponseDecomposition X) (x : X) :
    D.darkDrive x = D.net x + D.focusingLoad x := by
  unfold ResponseDecomposition.net
  ring

/-- Net plus the independently registered focusing field makes the dark component unique. -/
theorem same_net_and_focusing_forces_same_dark
    {X : Type} (A B : ResponseDecomposition X)
    (hnet : A.net = B.net) (hfocus : A.focusingLoad = B.focusingLoad) :
    A.darkDrive = B.darkDrive := by
  funext x
  rw [dark_component_recovered_from_net_and_focusing A x,
    dark_component_recovered_from_net_and_focusing B x, hnet, hfocus]

/-- At fixed net response, a changed focusing field structurally forces a changed dark field. -/
theorem same_net_distinct_focusing_forces_distinct_dark
    {X : Type} (A B : ResponseDecomposition X)
    (hnet : A.net = B.net) (hfocus : A.focusingLoad ≠ B.focusingLoad) :
    A.darkDrive ≠ B.darkDrive := by
  intro hdark
  apply hfocus
  funext x
  have hn := congrFun hnet x
  have hd := congrFun hdark x
  unfold ResponseDecomposition.net at hn
  linarith

/-- Conditional bridge capstone plus its exact two-readout information boundary. -/
theorem local_raychaudhuri_representation_coupling
    {X : Type} [Nonempty X] (R : LocalRaychaudhuriRepresentation X) :
    (∀ x, R.measuredAcceleration x =
      raychaudhuriDefocusing (R.vorticitySq x) (R.measuredDarkArchiveDrive x) -
        raychaudhuriFocusing (R.expansionRate x) (R.shearSq x)
          (R.activeMatterFocusing x)) ∧
    (¬ ∃ recoverDark : (X → ℝ) → (X → ℝ),
      ∀ D : ResponseDecomposition X, recoverDark D.net = D.darkDrive) :=
  ⟨represented_local_acceleration_eq_defocusing_sub_focusing R,
    no_dark_component_identifiable_from_net⟩

end D0.Bridge.LocalRaychaudhuriRepresentation
