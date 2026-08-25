import D0.Foundation.M1ClassAdmissibility
import D0.Synthesis.DetectorLayerEquivalence
import D0.Synthesis.TypedDetectorPrimitiveExhaustion

/-!
# Class-level M1 detector representation

This module closes the formal seam between class-level M1 admissibility and the typed detector
layer.

1. Instantiate `M1ClassAdmissibility.CatalogueSystem` on detector comparisons:
   candidates are catalogue-dependent comparison functions, catalogues are orientation assignments,
   and outputs are current-pair Boolean tables.
2. Prove class-level M1 admissibility is exactly `CatalogueFree`.
3. Define a representation contract for an arbitrary physical comparison type:
   its admissible objects map injectively to the class-admissible detector system.
4. Construct an embedding of every admissible physical comparison into the canonical
   history-invariant detector layer.
5. Transport the image back to the concrete observation carrier and prove it factors through
   current data; every primitive image therefore has one of the two T49 capability profiles.

The canonical detector system itself instantiates the contract, proving non-vacuity. This is the
requested class-level M1 admissibility/representation theorem. It does not assert that an
arbitrary external physical formalism satisfies the contract; supplying its comparison map and
catalogue-independence proof is the explicit application obligation.
-/

namespace D0.Synthesis.DetectorM1ClassRepresentation

open D0.Foundation.M1ClassAdmissibility
open D0.Foundation.CurrentDataFactorization
open D0.Foundation.DetectionCapabilityBoundary
open D0.Foundation.GeneralComparisonGrammar
open D0.Synthesis.DetectorCatalogueFreedom
open D0.Synthesis.DetectorLayerEquivalence
open D0.Synthesis.TypedDetectorPrimitiveExhaustion

/-- The class-level M1 catalogue system of detector comparisons. -/
def detectorCatalogueSystem (Current : Type*) : CatalogueSystem where
  Candidate := CatalogueComparison Current
  Catalogue := Current → Bool
  Output := Current → Current → Bool
  eval cmp o := cmp o

/-- **Class M1 equals catalogue-freedom on detectors.** This is an extensional theorem, not a
unique-answer assertion. -/
theorem detectorClassAdmissible_iff_catalogueFree
    (Current : Type*) (cmp : CatalogueComparison Current) :
    M1ClassAdmissible (detectorCatalogueSystem Current) cmp ↔
      CatalogueFree cmp := by
  constructor
  · intro h o o' x y
    exact congrFun (congrFun (h o o') x) y
  · intro h o o'
    funext x y
    exact h o o' x y

/-- A physical comparison class faithfully represented in the class-level M1 detector system. -/
structure PhysicalDetectorRepresentation (Phys : Type*) where
  comparison : Phys → CatalogueComparison (Bool × Bool)
  admissible : Phys → Prop
  admissible_iff_classM1 :
    ∀ p, admissible p ↔
      M1ClassAdmissible (detectorCatalogueSystem (Bool × Bool)) (comparison p)
  comparison_injective_on_admissible :
    ∀ {p q}, admissible p → admissible q →
      comparison p = comparison q → p = q

/-- Carrier of admissible physical comparisons. -/
abbrev AdmissiblePhysical {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys) :=
  {p : Phys // R.admissible p}

/-- Every admissible physical comparison becomes a catalogue-free detector comparison. -/
def toCatalogueFreeCarrier {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys)
    (p : AdmissiblePhysical R) :
    CatalogueFreeCarrier (Bool × Bool) :=
  ⟨R.comparison p.1,
    (detectorClassAdmissible_iff_catalogueFree _ _).mp
      ((R.admissible_iff_classM1 p.1).mp p.2)⟩

/-- The physical representation is an embedding into the catalogue-free carrier. -/
def admissiblePhysicalEmbeddingCatalogueFree {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys) :
    AdmissiblePhysical R ↪ CatalogueFreeCarrier (Bool × Bool) where
  toFun := toCatalogueFreeCarrier R
  inj' := by
    intro p q h
    apply Subtype.ext
    apply R.comparison_injective_on_admissible p.2 q.2
    exact congrArg Subtype.val h

/-- Every admissible physical comparison embeds canonically into the history-invariant detector
layer via T48. -/
noncomputable def admissiblePhysicalEmbeddingDetectorLayer {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys) :
    AdmissiblePhysical R ↪ HistoryInvariantCarrier (Bool × Bool) Bool where
  toFun p :=
    catalogueFreeEquivHistoryInvariant (Bool × Bool)
      (toCatalogueFreeCarrier R p)
  inj' := by
    intro p q h
    apply (admissiblePhysicalEmbeddingCatalogueFree R).injective
    exact (catalogueFreeEquivHistoryInvariant (Bool × Bool)).injective h

/-- Transport a history-invariant split comparison back to the concrete D0 observation type. -/
def concreteComparisonOfDetectorLayer
    (cmp : HistoryInvariantCarrier (Bool × Bool) Bool) : Comparison :=
  fun x y => cmp.1 (splitObservation x) (splitObservation y)

/-- Every comparison in the typed detector layer factors through concrete current data. -/
theorem concreteComparisonOfDetectorLayer_factors
    (cmp : HistoryInvariantCarrier (Bool × Bool) Bool) :
    FactorsThroughCurrentData (concreteComparisonOfDetectorLayer cmp) := by
  intro x x' y hm hv
  have hcurrent : currentData x = currentData x' := by
    exact Prod.ext hm hv
  have hinv := cmp.2 (currentData x) (currentData y)
    x.history x'.history y.history y.history
  change cmp.1 (currentData x, x.history) (currentData y, y.history) =
    cmp.1 (currentData x', x'.history) (currentData y, y.history)
  rw [← hcurrent]
  exact hinv

/-- Concrete detector comparison associated to an admissible physical comparison. -/
noncomputable def physicalConcreteComparison {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys)
    (p : AdmissiblePhysical R) : Comparison :=
  concreteComparisonOfDetectorLayer
    (admissiblePhysicalEmbeddingDetectorLayer R p)

/-- Every class-M1-admissible physical comparison factors through current data. -/
theorem physicalConcreteComparison_factors {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys)
    (p : AdmissiblePhysical R) :
    FactorsThroughCurrentData (physicalConcreteComparison R p) :=
  concreteComparisonOfDetectorLayer_factors _

/-- Every primitive admissible physical image has exactly membership-only or value-only capability
profile. -/
theorem physical_primitive_profile_exhaustion {Phys : Type*}
    (R : PhysicalDetectorRepresentation Phys)
    (p : AdmissiblePhysical R)
    (hp : Primitive (capabilityVector (physicalConcreteComparison R p))) :
    capabilityVector (physicalConcreteComparison R p) = atomicOf (0 : Fin 3)
      ∨ capabilityVector (physicalConcreteComparison R p) = atomicOf (1 : Fin 3) :=
  currentData_primitive_profile_exhaustion _
    (physicalConcreteComparison_factors R p) hp

/-- Canonical non-vacuous representation: physical objects are detector comparisons themselves,
and class-level M1 admissibility is catalogue-independence. -/
def canonicalDetectorRepresentation :
    PhysicalDetectorRepresentation (CatalogueComparison (Bool × Bool)) where
  comparison := id
  admissible cmp :=
    M1ClassAdmissible (detectorCatalogueSystem (Bool × Bool)) cmp
  admissible_iff_classM1 := fun _ => Iff.rfl
  comparison_injective_on_admissible := by
    intro p q _ _ h
    exact h

/-- The canonical representation has multiple admissible objects; class-level M1 correctly
preserves the full allowed class. -/
theorem canonical_representation_non_singleton :
    ∃ p q : AdmissiblePhysical canonicalDetectorRepresentation, p ≠ q := by
  let p : AdmissiblePhysical canonicalDetectorRepresentation :=
    ⟨liftCat (fun _ _ => false),
      (detectorClassAdmissible_iff_catalogueFree _ _).mpr
        (liftCat_catalogueFree _)⟩
  let q : AdmissiblePhysical canonicalDetectorRepresentation :=
    ⟨liftCat (fun _ _ => true),
      (detectorClassAdmissible_iff_catalogueFree _ _).mpr
        (liftCat_catalogueFree _)⟩
  refine ⟨p, q, ?_⟩
  intro h
  have hv := congrArg (fun z =>
    z.1 (fun _ => false) (false, false) (false, false)) h
  simp [p, q, liftCat] at hv

/-- Capstone: class-level M1 detector admissibility has a faithful typed-layer representation,
is non-vacuous/non-singleton, and primitive images exhaust to membership/value. -/
theorem detector_M1_class_representation :
    (∀ cmp : CatalogueComparison (Bool × Bool),
      M1ClassAdmissible (detectorCatalogueSystem (Bool × Bool)) cmp ↔
        CatalogueFree cmp)
    ∧ (∀ {Phys : Type} (R : PhysicalDetectorRepresentation Phys)
        (p : AdmissiblePhysical R),
        FactorsThroughCurrentData (physicalConcreteComparison R p))
    ∧ (∀ {Phys : Type} (R : PhysicalDetectorRepresentation Phys)
        (p : AdmissiblePhysical R),
        Primitive (capabilityVector (physicalConcreteComparison R p)) →
        capabilityVector (physicalConcreteComparison R p) = atomicOf (0 : Fin 3)
          ∨ capabilityVector (physicalConcreteComparison R p) = atomicOf (1 : Fin 3))
    ∧ (∃ p q : AdmissiblePhysical canonicalDetectorRepresentation, p ≠ q) :=
  ⟨detectorClassAdmissible_iff_catalogueFree (Bool × Bool),
    fun R p => physicalConcreteComparison_factors R p,
    fun R p hp => physical_primitive_profile_exhaustion R p hp,
    canonical_representation_non_singleton⟩

end D0.Synthesis.DetectorM1ClassRepresentation
