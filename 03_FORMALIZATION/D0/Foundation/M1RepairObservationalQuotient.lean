import D0.Foundation.InformationConnectivity
import D0.Foundation.M1CascadeSceneNoGo
import D0.Foundation.M1Universality

/-!
# M1 repair observational quotient and the canonical variable scene

This module constructs the object isolated by
`D0-M1-CASCADE-SCENE-PARAMETRIC-NOGO-001`.

The quotient is not introduced as a three-element type. It is the quotient of the existing
structural `Discrimination` carrier by equality of its observable repair kind:

`D ~ E ↔ kindOf D = kindOf E`.

The three carried discriminations prove that every observable kind is represented and that the
three resulting classes are distinct. The quotient is therefore equivalent to `DatumKind`, and its
cardinality is computed only after the quotient has been fixed.

The no-extension leg uses the existing M1 information-connectivity theorem. An arbitrary extension
datum `θ` is placed in a genuinely new observation component, disjoint from every current repair
class. Lean proves all four required legs:

1. `θ` is underived in the current repair grammar;
2. changing its value changes a distinguishable admissible outcome while all current observations
   are held fixed;
3. `θ` is not current protocol data;
4. every attempted value at `θ` requires an external catalogue.

Hence no new component can be an M1-resolved mandatory repair. This is universal in the extension
type; it is not a scan through candidate fourth repairs.

Finally the quotient itself generates a variable `SceneCandidate`, and the quotient-to-zone and
zone-to-quotient maps are constructed as embeddings. The resulting count is an output. An arbitrary
external physical scene still has the ordinary application obligation of providing the faithful
representation; every such representation is proved to have the same count.
-/

namespace D0.Foundation.M1RepairObservationalQuotient

open Relation
open scoped Classical

open D0.Foundation
open D0.Foundation.DiscriminationRetyping
open D0.Foundation.DiscriminationKinds
open D0.Foundation.SceneCountReduction
open D0.Foundation.M1CascadeSceneNoGo
open D0.Foundation.M1Universality

/-! ## The observational quotient -/

/-- Two insufficiency records are observationally equivalent when they fail on the same sort of
datum. This is a relation on the structural `Discrimination` carrier, not a declared finite label. -/
def SameRepairObservation (D E : Discrimination) : Prop :=
  kindOf D = kindOf E

/-- The observational equivalence relation. -/
def repairObservationSetoid : Setoid Discrimination where
  r := SameRepairObservation
  iseqv := {
    refl := fun _ => rfl
    symm := fun h => h.symm
    trans := fun h₁ h₂ => h₁.trans h₂
  }

/-- The finite observational quotient sought by the cascade-to-scene seam. -/
abbrev RepairObservationQuotient :=
  Quotient repairObservationSetoid

/-- The class of a structural discrimination. -/
def repairClass (D : Discrimination) : RepairObservationQuotient :=
  Quotient.mk repairObservationSetoid D

/-- Read the observable kind from a quotient class. -/
def repairClassKind : RepairObservationQuotient → DatumKind :=
  Quotient.lift kindOf (by
    intro D E h
    exact h)

/-- One carried structural representative for each computed kind. -/
def representative : DatumKind → Discrimination
  | .reading => discComparison
  | .history => discOneLoop
  | .opPair => discOrderMemory

@[simp] theorem kindOf_representative (k : DatumKind) :
    kindOf (representative k) = k := by
  cases k <;> rfl

/-- The observational quotient is exactly the computed repair-kind space. The equivalence is
derived from `kindOf` and the carried representatives. -/
def repairQuotientEquivDatumKind : RepairObservationQuotient ≃ DatumKind where
  toFun := repairClassKind
  invFun := fun k => repairClass (representative k)
  left_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro D
    apply Quotient.sound
    change kindOf (representative (kindOf D)) = kindOf D
    exact kindOf_representative (kindOf D)
  right_inv := kindOf_representative

noncomputable instance repairObservationQuotientFintype :
    Fintype RepairObservationQuotient :=
  Fintype.ofEquiv DatumKind repairQuotientEquivDatumKind.symm

/-- The quotient cardinality is computed after the structural quotient and equivalence are fixed. -/
theorem repairObservationQuotient_card :
    Fintype.card RepairObservationQuotient = 3 := by
  rw [Fintype.card_congr repairQuotientEquivDatumKind]
  exact card_datumKind

/-- The three carried floors occupy three distinct observational quotient classes. -/
theorem carried_repair_classes_pairwise_distinct :
    repairClass discComparison ≠ repairClass discOneLoop
      ∧ repairClass discComparison ≠ repairClass discOrderMemory
      ∧ repairClass discOneLoop ≠ repairClass discOrderMemory := by
  obtain ⟨h₁₂, h₁₃, h₂₃⟩ := three_distinct_kinds
  refine ⟨?_, ?_, ?_⟩
  · intro h
    exact h₁₂ (congrArg repairClassKind h)
  · intro h
    exact h₁₃ (congrArg repairClassKind h)
  · intro h
    exact h₂₃ (congrArg repairClassKind h)

/-! ## Universal M1 no-extension theorem -/

/-- An arbitrary one-step extension of the present repair domain. No cardinality or list of
extension candidates is assumed. -/
abbrev ExtendedRepairDomain (Θ : Type) :=
  Sum DatumKind Θ

/-- Observable tag of an extended repair: an existing quotient kind or genuinely new data `θ`. -/
def extendedObservation {Θ : Type} :
    ExtendedRepairDomain Θ → Sum DatumKind Θ
  | .inl k => .inl k
  | .inr θ => .inr θ

/-- A record connects repairs exactly when their observable tags agree. -/
def ExtendedRepairRecord {Θ : Type}
    (x y : ExtendedRepairDomain Θ) : Prop :=
  extendedObservation x = extendedObservation y

theorem extendedRepairRecord_equivalence {Θ : Type} :
    Equivalence (@ExtendedRepairRecord Θ) := by
  refine ⟨?_, ?_, ?_⟩
  · intro x
    rfl
  · intro x y h
    exact h.symm
  · intro x y z h₁ h₂
    exact h₁.trans h₂

/-- Every new extension datum is record-disconnected from every current repair. -/
theorem prior_external_disconnected {Θ : Type}
    (k : DatumKind) (θ : Θ) :
    ¬ @SameComponent (ExtendedRepairDomain Θ) (@ExtendedRepairRecord Θ)
      (Sum.inl k) (Sum.inr θ) := by
  intro h
  have hr :=
    (extendedRepairRecord_equivalence (Θ := Θ)).eqvGen_iff.mp h
  cases hr

/-- Current derivability grammar: exactly the structural discriminations already constructed in
the corpus are derivable; extension data are not silently promoted into the grammar. -/
def currentRepairGrammar (Θ : Type) : DescSystem where
  Sent := ExtendedRepairDomain Θ
  derivable x := ∃ k : DatumKind, x = Sum.inl k

/-- Clause 1 of M1: an extension datum is underived in the current repair grammar. -/
theorem external_underived {Θ : Type} (θ : Θ) :
    ¬ (currentRepairGrammar Θ).derivable (Sum.inr θ) := by
  rintro ⟨k, h⟩
  cases h

/-- Current protocol data are precisely data represented by an existing structural
discrimination. -/
def CurrentRepairProtocolData {Θ : Type}
    (x : ExtendedRepairDomain Θ) : Prop :=
  ∃ k : DatumKind, x = Sum.inl k

/-- Clause 3 of M1: a genuinely new extension datum is not unavoidable current protocol data. -/
theorem external_not_protocol {Θ : Type} (θ : Θ) :
    ¬ CurrentRepairProtocolData (Sum.inr θ) := by
  rintro ⟨k, h⟩
  cases h

/-- A target domain affects a distinguishable outcome relative to an observer when two admissible
content assignments agree at the observer but disagree at the target. -/
def OutcomeAffecting {Dom : Type} (Rec : Dom → Dom → Prop)
    (observer target : Dom) : Prop :=
  ∃ c₀ c₁ : Dom → Bool,
    @AdmissibleContent Dom Bool Rec c₀
      ∧ @AdmissibleContent Dom Bool Rec c₁
      ∧ c₀ observer = c₁ observer
      ∧ c₀ target ≠ c₁ target

/-- Clause 2 of M1: every new component carries a distinguishable outcome not determined by any
current repair observer. -/
theorem external_outcome_affecting {Θ : Type}
    (k : DatumKind) (θ : Θ) :
    OutcomeAffecting (@ExtendedRepairRecord Θ)
      (Sum.inl k) (Sum.inr θ) := by
  let c₀ : ExtendedRepairDomain Θ → Bool := fun _ => false
  let c₁ : ExtendedRepairDomain Θ → Bool :=
    fun x =>
      if @SameComponent (ExtendedRepairDomain Θ) (@ExtendedRepairRecord Θ)
        (Sum.inl k) x
      then false else true
  refine ⟨c₀, c₁, ?_, ?_, ?_, ?_⟩
  · intro _ _ _
    rfl
  · exact piecewise_admissible (@ExtendedRepairRecord Θ)
      (Sum.inl k) false true
  · simp [c₀, c₁, SameComponent, EqvGen.refl]
  · simp [c₀, c₁, prior_external_disconnected k θ]

/-- The canonical current observer of each computed repair kind. -/
def priorObserver {Θ : Type} (k : DatumKind) :
    ExtendedRepairDomain Θ :=
  Sum.inl k

/-- M1-admissible mandatoriness: a repair is mandatory only if some existing observer forces a
unique value for it from the current record code. -/
def M1ResolvedByCurrentRepairs {Θ : Type}
    (d : ExtendedRepairDomain Θ) : Prop :=
  ∃ k : DatumKind, ∃ v : Bool,
    M1Forced
      (@ForcedValue (ExtendedRepairDomain Θ) Bool (@ExtendedRepairRecord Θ)
        (priorObserver k) false d) v

/-- Every current structural repair class is M1-resolved by its own quotient observer. -/
theorem current_repair_resolved {Θ : Type} (k : DatumKind) :
    M1ResolvedByCurrentRepairs (Θ := Θ) (Sum.inl k) := by
  refine ⟨k, false, ?_⟩
  have hcomp :
      @SameComponent (ExtendedRepairDomain Θ) (@ExtendedRepairRecord Θ)
        (priorObserver k) (Sum.inl k) := by
    apply (extendedRepairRecord_equivalence (Θ := Θ)).eqvGen_iff.mpr
    rfl
  exact reachable_value_m1_forced (@ExtendedRepairRecord Θ)
    (priorObserver k) false hcomp

/-- Clause 4: relative to every current repair observer, every proposed value of a new component
requires an external catalogue. -/
theorem external_every_value_needs_catalogue {Θ : Type}
    (k : DatumKind) (θ : Θ) (v : Bool) :
    RequiresExternalCatalogue
      (@ForcedValue (ExtendedRepairDomain Θ) Bool (@ExtendedRepairRecord Θ)
        (priorObserver k) false (Sum.inr θ)) v := by
  apply unreachable_every_value_needs_catalogue
    (@ExtendedRepairRecord Θ) (priorObserver k) false
  exact prior_external_disconnected k θ

/-- No new observation component can be an M1-resolved mandatory repair. -/
theorem external_not_resolved_by_current_repairs {Θ : Type} (θ : Θ) :
    ¬ M1ResolvedByCurrentRepairs (Sum.inr θ) := by
  rintro ⟨k, v, hv⟩
  exact external_every_value_needs_catalogue k θ v hv.forced

/-- Exact classification: the M1-resolved repair domain is precisely the current structural
carrier. -/
theorem resolved_iff_current_repair {Θ : Type}
    (d : ExtendedRepairDomain Θ) :
    M1ResolvedByCurrentRepairs d ↔
      ∃ k : DatumKind, d = Sum.inl k := by
  cases d with
  | inl k =>
      exact ⟨fun _ => ⟨k, rfl⟩,
        fun _ => current_repair_resolved k⟩
  | inr θ =>
      constructor
      · intro h
        exact False.elim (external_not_resolved_by_current_repairs θ h)
      · rintro ⟨k, h⟩
        cases h

/-- **Universal fourth-class M1 reductio.** Any proposed new repair class is underived,
outcome-affecting, non-protocol, requires an external catalogue for every value relative to every
current class, and therefore cannot be mandatory in an M1-admissible repair theory. -/
theorem fourth_class_forbidden_by_M1 {Θ : Type} (θ : Θ) :
    (¬ (currentRepairGrammar Θ).derivable (Sum.inr θ))
      ∧ (∀ k : DatumKind,
          OutcomeAffecting (@ExtendedRepairRecord Θ)
            (priorObserver k) (Sum.inr θ))
      ∧ (¬ CurrentRepairProtocolData (Sum.inr θ))
      ∧ (∀ (k : DatumKind) (v : Bool),
          RequiresExternalCatalogue
            (@ForcedValue (ExtendedRepairDomain Θ) Bool (@ExtendedRepairRecord Θ)
              (priorObserver k) false (Sum.inr θ)) v)
      ∧ ¬ M1ResolvedByCurrentRepairs (Sum.inr θ) :=
  ⟨external_underived θ,
   fun k => external_outcome_affecting k θ,
   external_not_protocol θ,
   fun k v => external_every_value_needs_catalogue k θ v,
   external_not_resolved_by_current_repairs θ⟩

/-- The required selection-proof shape, stated as a reductio: assuming a new class is mandatory
produces its underivability, outcome effect, non-protocol status and catalogue requirement, then
contradicts its alleged M1 resolution. -/
theorem mandatory_fourth_class_reductio {Θ : Type} (θ : Θ)
    (hMandatory : M1ResolvedByCurrentRepairs (Sum.inr θ)) :
    (¬ (currentRepairGrammar Θ).derivable (Sum.inr θ))
      ∧ (∀ k : DatumKind,
          OutcomeAffecting (@ExtendedRepairRecord Θ)
            (priorObserver k) (Sum.inr θ))
      ∧ (¬ CurrentRepairProtocolData (Sum.inr θ))
      ∧ (∀ (k : DatumKind) (v : Bool),
          RequiresExternalCatalogue
            (@ForcedValue (ExtendedRepairDomain Θ) Bool (@ExtendedRepairRecord Θ)
              (priorObserver k) false (Sum.inr θ)) v)
      ∧ False := by
  refine ⟨external_underived θ,
    fun k => external_outcome_affecting k θ,
    external_not_protocol θ,
    fun k v => external_every_value_needs_catalogue k θ v,
    ?_⟩
  exact external_not_resolved_by_current_repairs θ hMandatory

/-- Deletion control: if the new datum is forcibly connected to the existing record component,
it becomes M1-resolved. Disconnection is load-bearing. -/
def collapsedObservation {Θ : Type} (anchor : DatumKind) :
    ExtendedRepairDomain Θ → DatumKind
  | .inl k => k
  | .inr _ => anchor

def CollapsedRepairRecord {Θ : Type} (anchor : DatumKind)
    (x y : ExtendedRepairDomain Θ) : Prop :=
  collapsedObservation anchor x = collapsedObservation anchor y

theorem connection_deletion_control {Θ : Type}
    (k : DatumKind) (θ : Θ) :
    M1Forced
      (@ForcedValue (ExtendedRepairDomain Θ) Bool
        (CollapsedRepairRecord k)
        (Sum.inl k) false (Sum.inr θ)) false := by
  apply reachable_value_m1_forced
    (CollapsedRepairRecord k)
  apply EqvGen.rel
  rfl

/-! ## Faithful representation in the variable quotient scene -/

/-- The variable scene generated by the observational quotient. Its count is not an input. -/
noncomputable def quotientScene : SceneCandidate :=
  ⟨Fintype.card RepairObservationQuotient,
    Fintype.card_pos_iff.mpr ⟨repairClass discComparison⟩⟩

/-- Faithful quotient-to-zone and zone-to-quotient representation for the generated variable
scene. -/
noncomputable def quotientSceneRepresentation :
    FaithfulRepairSceneRepresentation quotientScene RepairObservationQuotient where
  repairToZone :=
    (Fintype.equivFin RepairObservationQuotient).toEmbedding
  zoneToRepair :=
    (Fintype.equivFin RepairObservationQuotient).symm.toEmbedding

/-- The selected quotient scene has three zones as an output of the quotient computation. -/
theorem quotientScene_zoneCount :
    quotientScene.zoneCount = 3 := by
  exact repairObservationQuotient_card

/-- Every external variable scene that faithfully represents the derived quotient has the same
zone count. This is the exact remaining application interface for a concrete physical scene. -/
theorem faithful_scene_zoneCount
    (S : SceneCandidate)
    (R : FaithfulRepairSceneRepresentation S RepairObservationQuotient) :
    S.zoneCount = 3 := by
  rw [zoneCount_eq_repairCard R]
  exact repairObservationQuotient_card

/-- The three carried classes map injectively to three distinct zones of the generated scene. -/
noncomputable def carriedRepairZone (D : Discrimination) :
    Fin quotientScene.zoneCount :=
  quotientSceneRepresentation.repairToZone (repairClass D)

theorem carried_repair_zones_pairwise_distinct :
    carriedRepairZone discComparison ≠ carriedRepairZone discOneLoop
      ∧ carriedRepairZone discComparison ≠ carriedRepairZone discOrderMemory
      ∧ carriedRepairZone discOneLoop ≠ carriedRepairZone discOrderMemory := by
  obtain ⟨h₁₂, h₁₃, h₂₃⟩ := carried_repair_classes_pairwise_distinct
  exact ⟨fun h => h₁₂ (quotientSceneRepresentation.repairToZone.injective h),
    fun h => h₁₃ (quotientSceneRepresentation.repairToZone.injective h),
    fun h => h₂₃ (quotientSceneRepresentation.repairToZone.injective h)⟩

/-- Capstone: derived observational quotient, universal M1 no-fourth-class theorem, faithful
variable-scene representation, and exact count. -/
theorem m1_repair_observational_quotient_scene :
    Fintype.card RepairObservationQuotient = 3
      ∧ (repairClass discComparison ≠ repairClass discOneLoop
        ∧ repairClass discComparison ≠ repairClass discOrderMemory
        ∧ repairClass discOneLoop ≠ repairClass discOrderMemory)
      ∧ (∀ {Θ : Type} (θ : Θ), ¬ M1ResolvedByCurrentRepairs (Sum.inr θ))
      ∧ Nonempty
        (FaithfulRepairSceneRepresentation quotientScene RepairObservationQuotient)
      ∧ quotientScene.zoneCount = 3 :=
  ⟨repairObservationQuotient_card,
   carried_repair_classes_pairwise_distinct,
   fun θ => external_not_resolved_by_current_repairs θ,
   ⟨quotientSceneRepresentation⟩,
   quotientScene_zoneCount⟩

end D0.Foundation.M1RepairObservationalQuotient
