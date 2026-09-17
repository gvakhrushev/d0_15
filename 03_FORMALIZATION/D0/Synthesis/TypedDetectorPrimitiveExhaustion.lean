import D0.Synthesis.DetectorLayerEquivalence
import D0.Synthesis.DetectionSceneBoundEquivalence

/-!
# Typed detector primitive exhaustion: exactly membership and value

`DetectorLayerEquivalence` identifies the instantaneous detector layer with history-invariant
full comparisons. `DetectionCapabilityBoundary` already supplies the extensional capability
vector `(membership, value, history)` of every concrete comparison.

This module classifies the primitive **capability profiles** available inside the typed detector
layer:

* history invariance forces the history coordinate to `false`;
* primitive means atomic in the general capability grammar;
* the only atomic profiles with history coordinate `false` are membership and value.

Therefore the typed detector layer has exactly two primitive capability kinds — not because a
two-constructor answer type was declared, but by finite classification inside the three-capability
ambient with history retained as a negative control.

This closes the detector-layer capability count and, through T45, seals the port-power zone bound
`≤13` **for the typed detector layer**. The separate M1 question is whether physical admissible
comparisons are represented by this layer; `DetectorM1PredicateBoundary` proves the current
unique-answer M1 predicate does not by itself supply that class-level representation.
-/

namespace D0.Synthesis.TypedDetectorPrimitiveExhaustion

open D0.Foundation.GeneralComparisonGrammar
open D0.Foundation.DetectionCapabilityBoundary
open D0.Synthesis.DetectionSceneBoundEquivalence

/-- Primitive capability profiles whose history coordinate is absent. -/
abbrev DetectorPrimitiveProfile :=
  {c : GenComparison 3 // Primitive c ∧ c 2 = false}

/-- Finite classification inside the full three-capability ambient: every primitive,
history-blind profile is exactly membership or value. -/
theorem primitive_historyBlind_classification
    (c : GenComparison 3) (hp : Primitive c) (hh : c 2 = false) :
    c = atomicOf (0 : Fin 3) ∨ c = atomicOf (1 : Fin 3) := by
  have ha : Atomic c := (primitive_iff_atomic c).mp hp
  generalize hidx : atomicIndex ha = i
  fin_cases i
  · left
    simpa [hidx] using (atomicOf_eq_of_atomic ha).symm
  · right
    simpa [hidx] using (atomicOf_eq_of_atomic ha).symm
  · exfalso
    have hc : c = atomicOf (2 : Fin 3) := by
      simpa [hidx] using (atomicOf_eq_of_atomic ha).symm
    simp [hc, atomicOf] at hh

/-- Membership realizes the first detector primitive profile. -/
def membershipDetectorProfile : DetectorPrimitiveProfile :=
  ⟨atomicOf (0 : Fin 3), by
    constructor
    · exact (primitive_iff_atomic _).2 (atomicOf_atomic 0)
    · simp [atomicOf]⟩

/-- Value realizes the second detector primitive profile. -/
def valueDetectorProfile : DetectorPrimitiveProfile :=
  ⟨atomicOf (1 : Fin 3), by
    constructor
    · exact (primitive_iff_atomic _).2 (atomicOf_atomic 1)
    · simp [atomicOf]⟩

@[simp] theorem membershipDetectorProfile_val :
    membershipDetectorProfile.1 = atomicOf (0 : Fin 3) := rfl

@[simp] theorem valueDetectorProfile_val :
    valueDetectorProfile.1 = atomicOf (1 : Fin 3) := rfl

theorem atomicOf_one_ne_zero :
    atomicOf (1 : Fin 3) ≠ atomicOf (0 : Fin 3) := by decide

theorem membershipDetectorProfile_ne_valueDetectorProfile :
    membershipDetectorProfile ≠ valueDetectorProfile := by
  decide

/-- Encode membership as `0`, value as `1`. -/
noncomputable def detectorProfileToFin2 (c : DetectorPrimitiveProfile) : Fin 2 :=
  if c.1 = atomicOf (0 : Fin 3) then 0 else 1

/-- Decode the two detector primitive labels. -/
def fin2ToDetectorProfile (i : Fin 2) : DetectorPrimitiveProfile :=
  if i = 0 then membershipDetectorProfile else valueDetectorProfile

@[simp] theorem detectorProfileToFin2_membership :
    detectorProfileToFin2 membershipDetectorProfile = 0 := by
  simp [detectorProfileToFin2]

@[simp] theorem detectorProfileToFin2_value :
    detectorProfileToFin2 valueDetectorProfile = 1 := by
  simp [detectorProfileToFin2, atomicOf_one_ne_zero]

@[simp] theorem fin2ToDetectorProfile_zero :
    fin2ToDetectorProfile 0 = membershipDetectorProfile := by
  simp [fin2ToDetectorProfile]

@[simp] theorem fin2ToDetectorProfile_one :
    fin2ToDetectorProfile 1 = valueDetectorProfile := by
  simp [fin2ToDetectorProfile]

theorem fin2ToDetectorProfile_detectorProfileToFin2
    (c : DetectorPrimitiveProfile) :
    fin2ToDetectorProfile (detectorProfileToFin2 c) = c := by
  rcases primitive_historyBlind_classification c.1 c.2.1 c.2.2 with h0 | h1
  · have hc : c = membershipDetectorProfile := Subtype.ext h0
    rw [hc]
    simp
  · have hc : c = valueDetectorProfile := Subtype.ext h1
    rw [hc]
    simp

theorem detectorProfileToFin2_fin2ToDetectorProfile (i : Fin 2) :
    detectorProfileToFin2 (fin2ToDetectorProfile i) = i := by
  fin_cases i <;> simp

/-- Explicit equivalence: the typed detector primitive profiles are exactly a two-element
carrier. -/
noncomputable def detectorPrimitiveProfileEquivFin2 :
    DetectorPrimitiveProfile ≃ Fin 2 where
  toFun := detectorProfileToFin2
  invFun := fin2ToDetectorProfile
  left_inv := fin2ToDetectorProfile_detectorProfileToFin2
  right_inv := detectorProfileToFin2_fin2ToDetectorProfile

/-- There are exactly two primitive detector capability profiles. -/
theorem detectorPrimitiveProfile_card :
    Nat.card DetectorPrimitiveProfile = 2 := by
  rw [Nat.card_congr detectorPrimitiveProfileEquivFin2,
    Nat.card_eq_fintype_card, Fintype.card_fin]

/-- Every concrete primitive comparison in the current-data detector layer has membership-only
or value-only capability profile. -/
theorem currentData_primitive_profile_exhaustion
    (cmp : Comparison)
    (hcurrent : FactorsThroughCurrentData cmp)
    (hprimitive : Primitive (capabilityVector cmp)) :
    capabilityVector cmp = atomicOf (0 : Fin 3)
      ∨ capabilityVector cmp = atomicOf (1 : Fin 3) := by
  have hnot : ¬ UsesHistory cmp :=
    current_data_factorization_excludes_history cmp hcurrent
  have hh : capabilityVector cmp 2 = false := by
    simp [capabilityVector, hnot]
  exact primitive_historyBlind_classification (capabilityVector cmp) hprimitive hh

/-- The history comparison is not a typed detector primitive profile: it has history coordinate
`true` and lies outside current-data factorization. -/
theorem history_not_detector_profile :
    ¬ (capabilityVector historyComparison = atomicOf (0 : Fin 3)
      ∨ capabilityVector historyComparison = atomicOf (1 : Fin 3)) := by
  rw [history_capability_vector]
  decide

/-- Exact two-kind capability count seals the T45 port-power bound for the typed detector layer. -/
theorem typed_detector_seals_zone13 :
    Zone13BoundAtCapabilityCount (Nat.card DetectorPrimitiveProfile) := by
  rw [detectorPrimitiveProfile_card]
  exact two_capabilities_seal_zone13

/-- Capstone: the classification is performed in the full three-capability ambient, membership and
value realize both survivors, history is excluded, and the resulting count seals the zone bound. -/
theorem typed_detector_primitive_exhaustion :
    Nat.card DetectorPrimitiveProfile = 2
      ∧ membershipDetectorProfile ≠ valueDetectorProfile
      ∧ (∀ (cmp : Comparison),
          FactorsThroughCurrentData cmp →
          Primitive (capabilityVector cmp) →
          capabilityVector cmp = atomicOf (0 : Fin 3)
            ∨ capabilityVector cmp = atomicOf (1 : Fin 3))
      ∧ ¬ (capabilityVector historyComparison = atomicOf (0 : Fin 3)
            ∨ capabilityVector historyComparison = atomicOf (1 : Fin 3))
      ∧ Zone13BoundAtCapabilityCount (Nat.card DetectorPrimitiveProfile) :=
  ⟨detectorPrimitiveProfile_card,
    membershipDetectorProfile_ne_valueDetectorProfile,
    currentData_primitive_profile_exhaustion,
    history_not_detector_profile,
    typed_detector_seals_zone13⟩

end D0.Synthesis.TypedDetectorPrimitiveExhaustion
