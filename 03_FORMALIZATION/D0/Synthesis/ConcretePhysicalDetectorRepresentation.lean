import D0.Foundation.M1ClassAdmissibility
import D0.Synthesis.TypedDetectorPrimitiveExhaustion

/-!
# Concrete physical detector representation on the D0 observation carrier

`DetectorM1ClassRepresentation` supplied a generic application interface. This module provides
the requested concrete instance for the actual finite D0 observation model

`Observation = (member : Bool, value : Bool, history : Bool)`.

A binary comparison has two input slots, so the correct external orientation catalogue must
assign histories independently to the left and right arguments. We therefore use

`TwoSidedCatalogue = InputSide → Current → Bool`.

The concrete catalogue system evaluates a full physical comparison after filling the two history
slots from that catalogue. Lean proves:

`M1ClassAdmissible concreteSystem cmp ↔ HistoryInvariant (transportComparison cmp)`.

Thus the explicit physical representation fields are discharged:

* `comparison` = identity on concrete comparison functions;
* `admissible` = full two-sided history invariance;
* `admissible_iff_classM1` = the theorem above;
* `injectivity` = identity.

Every admissible concrete comparison embeds in the typed detector layer, factors through current
data on both arguments, and every primitive capability image is membership-only or value-only.
Membership/value comparisons are positive controls; history equality is rejected.
-/

namespace D0.Synthesis.ConcretePhysicalDetectorRepresentation

open D0.Foundation.M1ClassAdmissibility
open D0.Foundation.CurrentDataFactorization
open D0.Foundation.DetectionCapabilityBoundary
open D0.Foundation.GeneralComparisonGrammar
open D0.Synthesis.TypedDetectorPrimitiveExhaustion

/-- The two argument positions of a binary comparison. -/
inductive InputSide
  | left
  | right
deriving DecidableEq, Fintype

/-- Independent orientation/history assignments for the two comparison inputs. -/
abbrev TwoSidedCatalogue :=
  InputSide → (Bool × Bool) → Bool

/-- Fill the history slot of a concrete observation. -/
def observationOf (c : Bool × Bool) (h : Bool) : Observation :=
  ⟨c.1, c.2, h⟩

/-- The concrete catalogue system on the actual D0 observation comparison type. -/
def concreteDetectorSystem : CatalogueSystem where
  Candidate := Comparison
  Catalogue := TwoSidedCatalogue
  Output := CurrentComparison (Bool × Bool)
  eval cmp o x y :=
    cmp (observationOf x (o .left x))
      (observationOf y (o .right y))

/-- Class-level catalogue independence is exactly full two-sided history invariance. -/
theorem concreteClassM1_iff_historyInvariant (cmp : Comparison) :
    M1ClassAdmissible concreteDetectorSystem cmp ↔
      HistoryInvariant (Bool × Bool) Bool (transportComparison cmp) := by
  constructor
  · intro h c₁ c₂ h₁ h₁' h₂ h₂'
    let o : TwoSidedCatalogue :=
      fun side _ => match side with
        | .left => h₁
        | .right => h₂
    let o' : TwoSidedCatalogue :=
      fun side _ => match side with
        | .left => h₁'
        | .right => h₂'
    have heq := h o o'
    have hp := congrFun (congrFun heq c₁) c₂
    simpa [concreteDetectorSystem, o, o', observationOf,
      transportComparison, splitObservation] using hp
  · intro h o o'
    funext x y
    exact h x y (o .left x) (o' .left x)
      (o .right y) (o' .right y)

/-- The concrete physical representation instance requested by the class-level interface. -/
def concretePhysicalRepresentation :
    ClassRepresentation concreteDetectorSystem Comparison where
  candidate := id
  admissible cmp :=
    HistoryInvariant (Bool × Bool) Bool (transportComparison cmp)
  admissible_iff := by
    intro cmp
    exact (concreteClassM1_iff_historyInvariant cmp).symm
  candidate_injective_on_admissible := by
    intro p q _ _ h
    exact h

/-- Concrete admissible comparison carrier. -/
abbrev ConcreteAdmissible :=
  AdmissiblePhysical concretePhysicalRepresentation

/-- The generic class-level representation embedding, now instantiated on the concrete D0
observation system. -/
def concreteClassEmbedding :
    ConcreteAdmissible ↪ M1AdmissibleCarrier concreteDetectorSystem :=
  classRepresentationEmbedding concretePhysicalRepresentation

/-- Direct embedding of concrete admissible comparisons into the typed history-invariant layer. -/
def concreteDetectorLayerEmbedding :
    ConcreteAdmissible ↪
      {cmp : FullComparison (Bool × Bool) Bool //
        HistoryInvariant (Bool × Bool) Bool cmp} where
  toFun p := ⟨transportComparison p.1, p.2⟩
  inj' := by
    intro p q h
    apply Subtype.ext
    funext x y
    have hp := congrFun
      (congrFun (congrArg Subtype.val h)
        (splitObservation x)) (splitObservation y)
    simpa [transportComparison] using hp

/-- Full current-data factorization on both arguments. -/
def FactorsThroughBothCurrentData (cmp : Comparison) : Prop :=
  ∀ x x' y y' : Observation,
    currentData x = currentData x' →
    currentData y = currentData y' →
    cmp x y = cmp x' y'

/-- Full two-sided current-data factorization is equivalent to history invariance. -/
theorem factorsBoth_iff_historyInvariant (cmp : Comparison) :
    FactorsThroughBothCurrentData cmp ↔
      HistoryInvariant (Bool × Bool) Bool (transportComparison cmp) := by
  constructor
  · intro h c₁ c₂ h₁ h₁' h₂ h₂'
    exact h (observationOf c₁ h₁) (observationOf c₁ h₁')
      (observationOf c₂ h₂) (observationOf c₂ h₂')
      (by rfl) (by rfl)
  · intro h x x' y y' hx hy
    have hi := h (currentData x) (currentData y)
      x.history x'.history y.history y'.history
    change cmp x y = cmp x' y'
    have hxobs : x =
        observationOf (currentData x) x.history := by
      cases x
      rfl
    have hx'obs : x' =
        observationOf (currentData x') x'.history := by
      cases x'
      rfl
    have hyobs : y =
        observationOf (currentData y) y.history := by
      cases y
      rfl
    have hy'obs : y' =
        observationOf (currentData y') y'.history := by
      cases y'
      rfl
    rw [hxobs, hx'obs, hyobs, hy'obs, ← hx, ← hy]
    simpa [transportComparison, splitObservation, observationOf] using hi

/-- Every concrete class-M1-admissible comparison factors through current data on both inputs. -/
theorem concrete_admissible_factors_both (p : ConcreteAdmissible) :
    FactorsThroughBothCurrentData p.1 :=
  (factorsBoth_iff_historyInvariant p.1).2 p.2

/-- Hence every concrete admissible comparison satisfies the one-sided detector condition used
by the capability extractor. -/
theorem concrete_admissible_factors_current (p : ConcreteAdmissible) :
    FactorsThroughCurrentData p.1 := by
  intro x x' y hm hv
  apply concrete_admissible_factors_both p x x' y y
  · exact Prod.ext hm hv
  · rfl

/-- Every primitive concrete admissible comparison has membership-only or value-only profile. -/
theorem concrete_primitive_profile_exhaustion
    (p : ConcreteAdmissible)
    (hp : Primitive (capabilityVector p.1)) :
    capabilityVector p.1 = atomicOf (0 : Fin 3)
      ∨ capabilityVector p.1 = atomicOf (1 : Fin 3) :=
  currentData_primitive_profile_exhaustion p.1
    (concrete_admissible_factors_current p) hp

/-- Simpler proof that membership and value are admissible, and history is not. -/
theorem concrete_controls :
    concretePhysicalRepresentation.admissible membershipComparison
      ∧ concretePhysicalRepresentation.admissible valueComparison
      ∧ ¬ concretePhysicalRepresentation.admissible historyComparison := by
  refine ⟨?_, ?_, history_transport_not_invariant⟩
  · change HistoryInvariant (Bool × Bool) Bool
      (transportComparison membershipComparison)
    rw [← membership_transport_factors]
    exact liftCurrent_historyInvariant _ _ _
  · change HistoryInvariant (Bool × Bool) Bool
      (transportComparison valueComparison)
    rw [← value_transport_factors]
    exact liftCurrent_historyInvariant _ _ _

/-- Capstone: the actual finite observation comparison system supplies every field of the generic
class-level representation, embeds into the detector layer, factors through both current inputs,
and exhausts primitive profiles to membership/value. -/
theorem concrete_physical_detector_representation :
    (∀ cmp : Comparison,
      concretePhysicalRepresentation.admissible cmp ↔
        M1ClassAdmissible concreteDetectorSystem cmp)
    ∧ Nonempty (ConcreteAdmissible ↪
        M1AdmissibleCarrier concreteDetectorSystem)
    ∧ Nonempty (ConcreteAdmissible ↪
        {cmp : FullComparison (Bool × Bool) Bool //
          HistoryInvariant (Bool × Bool) Bool cmp})
    ∧ (∀ p : ConcreteAdmissible, FactorsThroughBothCurrentData p.1)
    ∧ (∀ (p : ConcreteAdmissible),
        Primitive (capabilityVector p.1) →
        capabilityVector p.1 = atomicOf (0 : Fin 3)
          ∨ capabilityVector p.1 = atomicOf (1 : Fin 3))
    ∧ concretePhysicalRepresentation.admissible membershipComparison
    ∧ concretePhysicalRepresentation.admissible valueComparison
    ∧ ¬ concretePhysicalRepresentation.admissible historyComparison :=
  ⟨concretePhysicalRepresentation.admissible_iff,
    ⟨concreteClassEmbedding⟩,
    ⟨concreteDetectorLayerEmbedding⟩,
    concrete_admissible_factors_both,
    concrete_primitive_profile_exhaustion,
    concrete_controls.1, concrete_controls.2.1, concrete_controls.2.2⟩

end D0.Synthesis.ConcretePhysicalDetectorRepresentation
