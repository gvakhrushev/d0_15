import D0.Foundation.CascadeCarriedAssembly
import D0.Foundation.DiscriminationKinds
import D0.Foundation.ZoneCountFromRank
import D0.Synthesis.ConcretePhysicalDetectorRepresentation

/-!
# The present M1/cascade grammar does not determine a variable scene count

This module closes the negative route identified by the adversarial scout for
`D0-CASCADE-INSUFFICIENCY-CHAIN-001`.

The countermodel retains, simultaneously:

* the complete theorem currently assembled by `cascade_carried_assembly`;
* the three computed `DatumKind` distinctions;
* both owner propositions used by `SceneCountReduction`;
* the concrete two-sided class-M1 detector representation.

None of these facts contains a map to a variable `SceneCandidate`. Consequently the same package
has models at every positive zone count, in particular at two and four zones. The result is
stronger than saying that one proposed proof fails: the present grammar does not determine any
unique count.

The module also records three exact controls:

* `ZoneAssignmentK` is equivalent to the lower cardinal bound, so it renames rather than derives it;
* deleting injectivity permits two datum kinds to be glued;
* a genuine four-zone complete-multipartite scene has transport rank exactly four, so the rank
  route can close the upper side only after an independent variable-scene rank bound is supplied.

Finally `FaithfulRepairSceneRepresentation` is the minimal typed reopening contract. It contains no
target number: an independently derived finite quotient of mandatory outcome-affecting repairs must
embed faithfully into the zones, and every zone must embed back into that same quotient. The
contract is inhabited on its own canonical carrier and both embeddings have deletion controls. No
theorem below constructs it from the present M1/cascade facts.
-/

namespace D0.Foundation.M1CascadeSceneNoGo

open D0.Foundation
open D0.Foundation.SceneCountReduction
open D0.Foundation.DiscriminationRetyping
open D0.Foundation.DiscriminationKinds
open D0.Foundation.ZoneCountFromRank
open D0.Foundation.DetectionCapabilityBoundary
open D0.Synthesis.ConcretePhysicalDetectorRepresentation
open D0.Foundation.M1ClassAdmissibility

/-- The exact carried-cascade theorem, named as a proposition so it can be retained in a
countermodel without weakening or re-proving any floor. -/
abbrev CarriedCascadeFact : Prop :=
  (∀ s ∈ carriedFloorsExtended, ¬ (s.ObligationBelow ↔ s.ObligationAbove))
    ∧ ((runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0))
        ∧ ¬ OrderEncoded (Multiplicative (ℤ × ℤ)))
    ∧ (OrderEncoded (Equiv.Perm (Fin 3))
        ∧ OrderEncoded (QuaternionGroup 2)
        ∧ (∀ r : ℝ, carrierRealizedRatio (Equiv.Perm (Fin 3)) r → ¬ NonCaptured r)
        ∧ (∀ r : ℝ, carrierRealizedRatio (QuaternionGroup 2) r → ¬ NonCaptured r))
    ∧ (OrderEncoded (Equiv.Perm (Fin 3))
        ∧ (∃ a b : Equiv.Perm (Fin 3), commDefect a b ≠ 1)
        ∧ ¬ (∀ g a b : Equiv.Perm (Fin 3), g * commDefect a b * g⁻¹ = commDefect a b)
        ∧ (∀ g x : Equiv.Perm (Fin 3),
            ConjClasses.mk (g * x * g⁻¹) = ConjClasses.mk x))
    ∧ ((¬ ∀ T : D0.Geometry.TorusParameter,
          ∀ x ∈ ({T.inner, T.core} : Set ℚ),
            D0.Foundation.shellReflection T x ∈ ({T.inner, T.core} : Set ℚ))
        ∧ (∀ T : D0.Geometry.TorusParameter,
          ∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
            D0.Foundation.shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ))
        ∧ (∀ x : ℝ, 0 < x → (x = 1 + 1 / x ↔ x = Real.goldenRatio))
        ∧ NonCaptured ((1 + Real.sqrt 5) / 2))
    ∧ (∀ T : D0.Geometry.TorusParameter,
        ({T.inner, T.core} : Finset ℚ).card = 2
          ∧ (∀ S : Set ℚ, ({T.inner, T.core} : Set ℚ) ⊆ S →
              (∀ x ∈ S, D0.Foundation.shellReflection T x ∈ S) →
              ({T.inner, T.core, T.outer} : Set ℚ) ⊆ S)
          ∧ ({T.inner, T.core, T.outer} : Finset ℚ).card = 3
          ∧ (∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
              D0.Foundation.shellReflection T x ∈
                ({T.inner, T.core, T.outer} : Set ℚ))
          ∧ Fintype.card D0.Geometry.TorusShell = 3)
    ∧ ¬ (CascadeFloorOrientationParity.stepOrientationParity.ObligationBelow ↔
      CascadeFloorOrientationParity.stepOrientationParity.ObligationAbove)

/-- The already-closed concrete class-M1 detector seam, restricted to its load-bearing
admissibility equivalence. -/
abbrev ConcreteClassM1Fact : Prop :=
  ∀ cmp : Comparison,
    concretePhysicalRepresentation.admissible cmp ↔
      M1ClassAdmissible concreteDetectorSystem cmp

/-- Every present semantic premise used by the attempted cascade-to-scene route. -/
structure PresentM1CascadeFacts where
  carriedCascade : CarriedCascadeFact
  ownerFacts : CascadeOwnerFact ∧ NoExtensionOwnerFact
  computedKinds :
    DistinctKind discComparison discOneLoop
      ∧ DistinctKind discComparison discOrderMemory
      ∧ DistinctKind discOneLoop discOrderMemory
  concreteDetector : ConcreteClassM1Fact

/-- The present grammar attached to a variable scene. The only scene-dependent datum available is
the non-emptiness already contained in `SceneCandidate.zoneCount_pos`; there is no semantic map. -/
structure PresentM1CascadeSceneModel (S : SceneCandidate)
    extends PresentM1CascadeFacts where
  zoneNonempty : Nonempty (Fin S.zoneCount)

/-- The canonical present fact package, citing every existing owner. -/
def presentFacts : PresentM1CascadeFacts where
  carriedCascade := cascade_carried_assembly
  ownerFacts := SceneCountReduction.owner_facts
  computedKinds := three_distinct_kinds
  concreteDetector := concrete_physical_detector_representation.1

/-- **Count-parametric countermodel.** Every positive scene count supports the complete present
M1/cascade package because no current premise relates those facts to the scene. -/
def presentModel (S : SceneCandidate) : PresentM1CascadeSceneModel S where
  toPresentM1CascadeFacts := presentFacts
  zoneNonempty := ⟨⟨0, S.zoneCount_pos⟩⟩

theorem present_model_at_every_positive_count (S : SceneCandidate) :
    Nonempty (PresentM1CascadeSceneModel S) :=
  ⟨presentModel S⟩

private def twoZoneScene : SceneCandidate := ⟨2, by omega⟩
private def fourZoneScene : SceneCandidate := ⟨4, by omega⟩

/-- Explicit scout witnesses: all present premises survive at both two and four zones. -/
theorem two_and_four_zone_countermodels :
    Nonempty (PresentM1CascadeSceneModel twoZoneScene)
      ∧ Nonempty (PresentM1CascadeSceneModel fourZoneScene) :=
  ⟨present_model_at_every_positive_count twoZoneScene,
   present_model_at_every_positive_count fourZoneScene⟩

/-- **No-go capstone.** The present M1/cascade grammar determines no unique zone count at all. -/
theorem present_grammar_does_not_determine_zoneCount :
    ¬ ∃ k : ℕ, ∀ S : SceneCandidate,
      Nonempty (PresentM1CascadeSceneModel S) → S.zoneCount = k := by
  rintro ⟨k, hk⟩
  have h₂ := hk twoZoneScene (present_model_at_every_positive_count twoZoneScene)
  have h₄ := hk fourZoneScene (present_model_at_every_positive_count fourZoneScene)
  simp [twoZoneScene] at h₂
  simp [fourZoneScene] at h₄
  omega

/-! ## Exact controls for the killed routes -/

/-- Structural indexing of the three already-computed datum kinds. Used only to prove that the
`ZoneAssignmentK` hypothesis is exactly the desired lower cardinal bound. -/
def datumKindEmbedding : DatumKind ↪ Fin 3 where
  toFun
    | .reading => 0
    | .history => 1
    | .opPair => 2
  inj' := by
    intro a b h
    cases a <;> cases b <;> simp_all

/-- The sort-indexed repair is circular: its inhabitance is equivalent to `3 ≤ zoneCount`. -/
theorem zoneAssignmentK_iff_bound (S : SceneCandidate) :
    Nonempty (ZoneAssignmentK S) ↔ 3 ≤ S.zoneCount := by
  constructor
  · rintro ⟨Z⟩
    exact three_le_zoneCount_of_kinds S Z
  · intro h
    exact ⟨{
      zoneOf := datumKindEmbedding.trans (finEmbeddingOfLE h)
      zoneOf_injective := (datumKindEmbedding.trans (finEmbeddingOfLE h)).injective
    }⟩

/-- If the load-bearing injectivity requirement is deleted, two different repair kinds can be
glued into one of two zones. -/
def gluedKindToTwo : DatumKind → Fin 2
  | .reading => 0
  | .history => 1
  | .opPair => 1

theorem gluedKindToTwo_collision :
    gluedKindToTwo .history = gluedKindToTwo .opPair := by
  simp [gluedKindToTwo]

theorem gluedKindToTwo_not_injective :
    ¬ Function.Injective gluedKindToTwo := by
  intro h
  have hk : DatumKind.history = DatumKind.opPair :=
    h gluedKindToTwo_collision
  cases hk

/-- A four-zone complete-multipartite control has rank exactly four. Thus the rank invariant is
capable of detecting the fourth slot; what is absent is a present owner forcing the variable-scene
rank to be at most three. -/
def fourZoneLabels : Fin 4 → Fin 4 := id

theorem four_zone_rank_eq_four :
    (adjOf fourZoneLabels).rank = 4 := by
  apply le_antisymm
  · simpa using rank_le_zoneCount fourZoneLabels
  · apply four_zones_forces_rank_four fourZoneLabels
    · intro c
      exact ⟨c, rfl⟩
    · omega

/-! ## Minimal typed reopening contract -/

/-- A variable scene faithfully represents an independently derived finite quotient of mandatory
outcome-affecting repair classes. No cardinal is named: both directions must be constructed from
semantics, and their injectivity is checked by Lean. -/
structure FaithfulRepairSceneRepresentation
    (S : SceneCandidate) (RepairClass : Type*) [Fintype RepairClass] where
  repairToZone : RepairClass ↪ Fin S.zoneCount
  zoneToRepair : Fin S.zoneCount ↪ RepairClass

/-- A faithful representation forces equality with the independently derived quotient cardinality,
without naming that cardinality in the contract. -/
theorem zoneCount_eq_repairCard
    {S : SceneCandidate} {RepairClass : Type*} [Fintype RepairClass]
    (R : FaithfulRepairSceneRepresentation S RepairClass) :
    S.zoneCount = Fintype.card RepairClass := by
  have h₁ : Fintype.card RepairClass ≤ S.zoneCount := by
    simpa using Fintype.card_le_of_injective R.repairToZone R.repairToZone.injective
  have h₂ : S.zoneCount ≤ Fintype.card RepairClass := by
    simpa using Fintype.card_le_of_injective R.zoneToRepair R.zoneToRepair.injective
  omega

/-- The contract is non-vacuous on the quotient's own canonical finite carrier. Its structure is
fixed before `card_datumKind` computes the resulting number. -/
noncomputable def datumKindScene : SceneCandidate :=
  ⟨Fintype.card DatumKind, Fintype.card_pos_iff.mpr ⟨DatumKind.reading⟩⟩

noncomputable def datumKindRepresentation :
    FaithfulRepairSceneRepresentation datumKindScene DatumKind where
  repairToZone := (Fintype.equivFin DatumKind).toEmbedding
  zoneToRepair := (Fintype.equivFin DatumKind).symm.toEmbedding

theorem datumKindRepresentation_nonvacuous :
    Nonempty (FaithfulRepairSceneRepresentation datumKindScene DatumKind) :=
  ⟨datumKindRepresentation⟩

/-- Deleting the repair-to-zone leg admits a two-zone scene. -/
def twoZonesIntoDatumKind : Fin 2 ↪ DatumKind where
  toFun
    | ⟨0, _⟩ => .reading
    | ⟨1, _⟩ => .history
  inj' := by
    intro a b h
    fin_cases a <;> fin_cases b <;> simp_all

theorem deleting_lower_leg_allows_two :
    Nonempty (Fin twoZoneScene.zoneCount ↪ DatumKind)
      ∧ twoZoneScene.zoneCount ≠ Fintype.card DatumKind := by
  refine ⟨⟨twoZonesIntoDatumKind⟩, ?_⟩
  simp [twoZoneScene, card_datumKind]

/-- Deleting the zone-to-repair leg admits a four-zone scene. -/
def datumKindIntoFour : DatumKind ↪ Fin fourZoneScene.zoneCount :=
  datumKindEmbedding.trans (finEmbeddingOfLE (by simp [fourZoneScene]))

theorem deleting_upper_leg_allows_four :
    Nonempty (DatumKind ↪ Fin fourZoneScene.zoneCount)
      ∧ fourZoneScene.zoneCount ≠ Fintype.card DatumKind := by
  refine ⟨⟨datumKindIntoFour⟩, ?_⟩
  simp [fourZoneScene, card_datumKind]

/-- The current facts cannot uniformly construct even the sort-indexed representation: the
two-zone countermodel preserves all present premises but violates the representation cardinality. -/
theorem no_uniform_datumKind_representation_from_present_facts :
    ¬ ∀ S : SceneCandidate, Nonempty (PresentM1CascadeSceneModel S) →
      Nonempty (FaithfulRepairSceneRepresentation S DatumKind) := by
  intro h
  obtain ⟨R⟩ := h twoZoneScene
    (present_model_at_every_positive_count twoZoneScene)
  have hc := zoneCount_eq_repairCard R
  simp [twoZoneScene, card_datumKind] at hc

end D0.Foundation.M1CascadeSceneNoGo
