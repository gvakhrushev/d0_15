import D0.Foundation.AdmissibleComparisonGrammar
import Mathlib.Tactic

/-!
# Representation contract for physical comparison systems

`D0.Foundation.AdmissibleComparisonGrammar` proves that the raw
membership/value capability lattice has exactly two primitive atoms.  Its
honest residual is the representation step: a physical comparison system must
map into that raw grammar without losing the distinction between primitive and
composite comparisons.

This module makes that residual a typed interface rather than a prose request.
It does **not** assume that a comparison is primitive merely because its image
is one of the desired atoms.  Instead a representation supplies:

* the physical admissibility and operational predicates;
* a physical subcomparison relation and physical composition;
* a capability map into the raw grammar;
* preservation/reflection of operationality and subcomparison;
* compatibility of physical composition with raw `join`;
* injectivity on admissible physical comparisons;
* realization of every proper operational raw subcomparison lying below the
  image of an admissible physical comparison.

The realization clause is the substantive completeness condition.  It prevents
an interaction-only comparison from looking physically primitive merely
because its membership-only and value-only components were omitted from the
physical candidate class.

From these fields Lean proves:

* physical decomposability iff raw decomposability;
* physical primitiveness iff raw primitiveness;
* every physical primitive injects into the existing `ComparisonKind`;
* therefore every finite represented physical system has at most two
  admissible primitive comparison kinds.

Two negative controls identify the load-bearing fields:

* duplicating one raw atom gives three physical names unless capability
  injectivity is required;
* a hybrid-only system omits both proper raw subcomparisons, so the hybrid
  falsely appears primitive unless the realization clause is required.

The raw grammar itself instantiates the contract and has exactly two physical
primitive comparisons, proving the interface is non-vacuous.  What remains open
is constructing this representation from the actual M1/detection protocol.
-/

namespace D0.Foundation.PhysicalComparisonRepresentation

open D0.Foundation.AdmissibleComparisonGrammar
open D0.Tower

/-- Data and laws required for a physical comparison system to be faithfully
represented in the raw membership/value capability grammar. -/
structure Representation (α : Type*) where
  admissible : α → Prop
  operational : α → Prop
  subcomparison : α → α → Prop
  combine : α → α → α
  capability : α → RawComparison

  operational_iff :
    ∀ {a}, admissible a →
      (operational a ↔ Operational (capability a))

  subcomparison_iff :
    ∀ {a b}, admissible a → admissible b →
      (subcomparison a b ↔ Subcomparison (capability a) (capability b))

  combine_admissible :
    ∀ {a b}, admissible a → admissible b → admissible (combine a b)

  capability_combine :
    ∀ a b, capability (combine a b) =
      AdmissibleComparisonGrammar.join (capability a) (capability b)

  capability_injective_on_admissible :
    ∀ {a b}, admissible a → admissible b →
      capability a = capability b → a = b

  realize_proper_subcomparison :
    ∀ {c} (r : RawComparison), admissible c →
      Operational r →
      ProperSubcomparison r (capability c) →
      ∃ a, admissible a ∧ capability a = r

/-- Strict physical subcomparison inside a represented system. -/
def PhysicalProperSubcomparison {α : Type*}
    (R : Representation α) (a c : α) : Prop :=
  R.subcomparison a c ∧ a ≠ c

/-- A physical comparison is decomposable when it is the composition of two
strictly smaller admissible operational comparisons. -/
def PhysicalDecomposable {α : Type*}
    (R : Representation α) (c : α) : Prop :=
  ∃ a b,
    R.admissible a ∧ R.admissible b ∧
    R.operational a ∧ R.operational b ∧
    PhysicalProperSubcomparison R a c ∧
    PhysicalProperSubcomparison R b c ∧
    R.combine a b = c

/-- A physical primitive is admissible, operational, and not physically
decomposable. -/
def PhysicalPrimitive {α : Type*}
    (R : Representation α) (c : α) : Prop :=
  R.admissible c ∧ R.operational c ∧ ¬ PhysicalDecomposable R c

/-- Physical decompositions map to raw decompositions. -/
theorem physicalDecomposable_implies_rawDecomposable
    {α : Type*} (R : Representation α) {c : α}
    (hc : R.admissible c)
    (h : PhysicalDecomposable R c) :
    Decomposable (R.capability c) := by
  rcases h with ⟨a, b, ha, hb, hoa, hob, ⟨hac, hane⟩, ⟨hbc, hbne⟩, hab⟩
  have hrawa : Operational (R.capability a) :=
    (R.operational_iff ha).mp hoa
  have hrawb : Operational (R.capability b) :=
    (R.operational_iff hb).mp hob
  have hsuba : Subcomparison (R.capability a) (R.capability c) :=
    (R.subcomparison_iff ha hc).mp hac
  have hsubb : Subcomparison (R.capability b) (R.capability c) :=
    (R.subcomparison_iff hb hc).mp hbc
  have hcapane : R.capability a ≠ R.capability c := by
    intro heq
    exact hane (R.capability_injective_on_admissible ha hc heq)
  have hcapbne : R.capability b ≠ R.capability c := by
    intro heq
    exact hbne (R.capability_injective_on_admissible hb hc heq)
  refine ⟨R.capability a, R.capability b, hrawa, hrawb,
    ⟨hsuba, hcapane⟩, ⟨hsubb, hcapbne⟩, ?_⟩
  rw [← R.capability_combine a b, hab]

/-- Every raw proper component below an admissible physical comparison is
realized by an admissible physical comparison and is physically below it. -/
theorem realize_physical_proper_subcomparison
    {α : Type*} (R : Representation α) {c : α}
    (hc : R.admissible c) {r : RawComparison}
    (hrOp : Operational r)
    (hrSub : ProperSubcomparison r (R.capability c)) :
    ∃ a,
      R.admissible a ∧
      R.operational a ∧
      PhysicalProperSubcomparison R a c ∧
      R.capability a = r := by
  obtain ⟨a, ha, hcap⟩ :=
    R.realize_proper_subcomparison r hc hrOp hrSub
  have hop : R.operational a :=
    (R.operational_iff ha).mpr (by simpa [hcap] using hrOp)
  have hsub : R.subcomparison a c :=
    (R.subcomparison_iff ha hc).mpr (by simpa [hcap] using hrSub.1)
  have hne : a ≠ c := by
    intro hac
    subst hac
    exact hrSub.2 hcap.symm
  exact ⟨a, ha, hop, ⟨hsub, hne⟩, hcap⟩

/-- Raw decompositions lift to physical decompositions.  This is where
realization of proper raw subcomparisons and injectivity are load-bearing. -/
theorem rawDecomposable_implies_physicalDecomposable
    {α : Type*} (R : Representation α) {c : α}
    (hc : R.admissible c)
    (h : Decomposable (R.capability c)) :
    PhysicalDecomposable R c := by
  rcases h with ⟨ra, rb, hraOp, hrbOp, hraSub, hrbSub, hj⟩
  obtain ⟨a, ha, hoa, hac, hca⟩ :=
    realize_physical_proper_subcomparison R hc hraOp hraSub
  obtain ⟨b, hb, hob, hbc, hcb⟩ :=
    realize_physical_proper_subcomparison R hc hrbOp hrbSub
  have habAdm : R.admissible (R.combine a b) :=
    R.combine_admissible ha hb
  have habCap : R.capability (R.combine a b) = R.capability c := by
    rw [R.capability_combine, hca, hcb, hj]
  have hab : R.combine a b = c :=
    R.capability_injective_on_admissible habAdm hc habCap
  exact ⟨a, b, ha, hb, hoa, hob, hac, hbc, hab⟩

/-- **Representation theorem for decomposability.** -/
theorem physicalDecomposable_iff_rawDecomposable
    {α : Type*} (R : Representation α) {c : α}
    (hc : R.admissible c) :
    PhysicalDecomposable R c ↔ Decomposable (R.capability c) :=
  ⟨physicalDecomposable_implies_rawDecomposable R hc,
   rawDecomposable_implies_physicalDecomposable R hc⟩

/-- **Representation theorem for primitive comparisons.** -/
theorem physicalPrimitive_iff_rawPrimitive
    {α : Type*} (R : Representation α) (c : α) :
    PhysicalPrimitive R c ↔
      R.admissible c ∧ Primitive (R.capability c) := by
  constructor
  · rintro ⟨hc, hop, hnot⟩
    refine ⟨hc, (R.operational_iff hc).mp hop, ?_⟩
    intro hraw
    exact hnot ((physicalDecomposable_iff_rawDecomposable R hc).mpr hraw)
  · rintro ⟨hc, hrawOp, hrawNot⟩
    refine ⟨hc, (R.operational_iff hc).mpr hrawOp, ?_⟩
    intro hphys
    exact hrawNot ((physicalDecomposable_iff_rawDecomposable R hc).mp hphys)

/-- The finite carrier of admissible physical primitive comparisons. -/
abbrev PhysicalPrimitiveCarrier {α : Type*}
    (R : Representation α) :=
  {c : α // PhysicalPrimitive R c}

/-- Every physical primitive has one of the two existing comparison kinds. -/
noncomputable def physicalPrimitiveEmbedding
    {α : Type*} (R : Representation α) :
    PhysicalPrimitiveCarrier R ↪ ComparisonKind where
  toFun c :=
    atomicComparisonEquiv
      ⟨R.capability c.1,
       (primitive_iff_atomic (R.capability c.1)).mp
         ((physicalPrimitive_iff_rawPrimitive R c.1).mp c.2).2⟩
  inj' := by
    intro a b hab
    apply Subtype.ext
    apply R.capability_injective_on_admissible
    · exact ((physicalPrimitive_iff_rawPrimitive R a.1).mp a.2).1
    · exact ((physicalPrimitive_iff_rawPrimitive R b.1).mp b.2).1
    · exact Subtype.ext_iff.mp (atomicComparisonEquiv.injective hab)

/-- If the represented physical system realizes both raw atoms as physical
primitive comparisons, then it has at least two primitive comparison kinds. -/
theorem two_le_physicalPrimitive_card
    {α : Type*} (R : Representation α)
    [Fintype (PhysicalPrimitiveCarrier R)]
    (hm : ∃ m, PhysicalPrimitive R m ∧
      R.capability m = membershipOnly)
    (hv : ∃ v, PhysicalPrimitive R v ∧
      R.capability v = valueOnly) :
    2 ≤ Fintype.card (PhysicalPrimitiveCarrier R) := by
  obtain ⟨m, hmPrimitive, hmCap⟩ := hm
  obtain ⟨v, hvPrimitive, hvCap⟩ := hv
  let e : Fin 2 ↪ PhysicalPrimitiveCarrier R :=
    ⟨fun i => if i = 0 then ⟨m, hmPrimitive⟩ else ⟨v, hvPrimitive⟩, by
      intro i j hij
      fin_cases i <;> fin_cases j
      · rfl
      · exfalso
        have hmv : m = v := Subtype.ext_iff.mp hij
        have : membershipOnly = valueOnly := by
          rw [← hmCap, ← hvCap, hmv]
        exact (by decide : membershipOnly ≠ valueOnly) this
      · exfalso
        have hvm : v = m := Subtype.ext_iff.mp hij
        have : valueOnly = membershipOnly := by
          rw [← hvCap, ← hmCap, hvm]
        exact (by decide : valueOnly ≠ membershipOnly) this
      · rfl⟩
  simpa using Fintype.card_le_of_injective e e.injective

/-- **Finite upper bound.** Every finite physical comparison system satisfying
the representation contract has at most two admissible primitive comparison
kinds. -/
theorem physicalPrimitive_card_le_two
    {α : Type*} (R : Representation α)
    [Fintype (PhysicalPrimitiveCarrier R)] :
    Fintype.card (PhysicalPrimitiveCarrier R) ≤ 2 := by
  simpa [two_comparison_kinds] using
    Fintype.card_le_of_injective
      (physicalPrimitiveEmbedding R)
      (physicalPrimitiveEmbedding R).injective

/-- Exact two-kind closure when both primitive capabilities are physically
realized. -/
theorem physicalPrimitive_card_eq_two
    {α : Type*} (R : Representation α)
    [Fintype (PhysicalPrimitiveCarrier R)]
    (hm : ∃ m, PhysicalPrimitive R m ∧
      R.capability m = membershipOnly)
    (hv : ∃ v, PhysicalPrimitive R v ∧
      R.capability v = valueOnly) :
    Fintype.card (PhysicalPrimitiveCarrier R) = 2 :=
  Nat.le_antisymm
    (physicalPrimitive_card_le_two R)
    (two_le_physicalPrimitive_card R hm hv)

/-! ## Non-vacuous canonical model -/

/-- The raw capability grammar represented by itself. -/
def rawRepresentation : Representation RawComparison where
  admissible := Operational
  operational := Operational
  subcomparison := Subcomparison
  combine := AdmissibleComparisonGrammar.join
  capability := id
  operational_iff := by
    intro a _
    rfl
  subcomparison_iff := by
    intro a b _ _
    rfl
  combine_admissible := by
    rintro ⟨am, av⟩ ⟨bm, bv⟩ ha hb
    cases am <;> cases av <;> cases bm <;> cases bv <;>
      simp [Operational, AdmissibleComparisonGrammar.join] at ha hb ⊢
  capability_combine := by
    intro a b
    rfl
  capability_injective_on_admissible := by
    intro a b _ _ h
    exact h
  realize_proper_subcomparison := by
    intro c r _ hr _
    exact ⟨r, hr, rfl⟩

/-- In the self-representation, the physical primitive carrier is the raw
primitive carrier itself. -/
def rawPhysicalPrimitiveEquiv :
    PhysicalPrimitiveCarrier rawRepresentation ≃
      {c : RawComparison // Primitive c} where
  toFun c :=
    ⟨c.1, ((physicalPrimitive_iff_rawPrimitive rawRepresentation c.1).mp c.2).2⟩
  invFun c :=
    ⟨c.1, (physicalPrimitive_iff_rawPrimitive rawRepresentation c.1).mpr
      ⟨c.2.1, c.2⟩⟩
  left_inv := by
    intro c
    rfl
  right_inv := by
    intro c
    rfl

noncomputable instance rawPhysicalPrimitiveFintype :
    Fintype (PhysicalPrimitiveCarrier rawRepresentation) :=
  Fintype.ofEquiv
    {c : RawComparison // Primitive c}
    rawPhysicalPrimitiveEquiv.symm

/-- The canonical raw model has exactly two physical primitive comparisons. -/
theorem rawRepresentation_primitive_count_two :
    Fintype.card (PhysicalPrimitiveCarrier rawRepresentation) = 2 := by
  rw [Fintype.card_congr rawPhysicalPrimitiveEquiv]
  exact primitive_comparison_count_two

/-! ## Load-bearing negative controls -/

/-- Three physical names, two of which duplicate the same raw primitive atom. -/
inductive DuplicatedPrimitive
  | membershipA
  | membershipB
  | value
deriving DecidableEq, Fintype

def duplicatedCapability : DuplicatedPrimitive → RawComparison
  | .membershipA => membershipOnly
  | .membershipB => membershipOnly
  | .value => valueOnly

/-- Without injectivity on admissible physical comparisons, three physical
primitive names can collapse to only two raw atoms. -/
theorem duplicatedCapability_not_injective :
    ¬ Function.Injective duplicatedCapability := by
  intro h
  have : DuplicatedPrimitive.membershipA =
      DuplicatedPrimitive.membershipB :=
    h rfl
  cases this

theorem all_duplicated_capabilities_are_raw_primitive :
    ∀ c : DuplicatedPrimitive, Primitive (duplicatedCapability c) := by
  intro c
  cases c <;> native_decide

/-- A physical candidate class containing only the hybrid cannot realize its
membership-only proper raw component. -/
inductive HybridOnly
  | sole
deriving DecidableEq, Fintype

def hybridOnlyCapability : HybridOnly → RawComparison
  | .sole => hybridComparison

theorem hybridOnly_omits_membership_component :
    ¬ ∃ c : HybridOnly, hybridOnlyCapability c = membershipOnly := by
  rintro ⟨c, h⟩
  cases c
  cases h

theorem hybridOnly_image_is_raw_decomposable :
    Decomposable (hybridOnlyCapability HybridOnly.sole) := by
  simpa [hybridOnlyCapability] using hybrid_decomposable

/-- **D0-PHYSICAL-COMPARISON-REPRESENTATION-REDUCTION-001.** Bundle of the
representation theorem, the finite two-kind upper bound, the canonical
non-vacuous model, and the two load-bearing controls. -/
theorem physical_comparison_representation_reduction :
    (∀ {α : Type*} (R : Representation α) (c : α),
      PhysicalPrimitive R c ↔
        R.admissible c ∧ Primitive (R.capability c)) ∧
    (∀ {α : Type*} (R : Representation α)
      (_inst : Fintype (PhysicalPrimitiveCarrier R)),
      @Fintype.card (PhysicalPrimitiveCarrier R) _inst ≤ 2) ∧
    (∀ {α : Type*} (R : Representation α)
      (_inst : Fintype (PhysicalPrimitiveCarrier R)),
      (∃ m, PhysicalPrimitive R m ∧
        R.capability m = membershipOnly) →
      (∃ v, PhysicalPrimitive R v ∧
        R.capability v = valueOnly) →
      @Fintype.card (PhysicalPrimitiveCarrier R) _inst = 2) ∧
    Fintype.card (PhysicalPrimitiveCarrier rawRepresentation) = 2 ∧
    (¬ Function.Injective duplicatedCapability) ∧
    (¬ ∃ c : HybridOnly, hybridOnlyCapability c = membershipOnly) := by
  refine ⟨?_, ?_, ?_, rawRepresentation_primitive_count_two,
    duplicatedCapability_not_injective,
    hybridOnly_omits_membership_component⟩
  · intro α R c
    exact physicalPrimitive_iff_rawPrimitive R c
  · intro α R inst
    letI : Fintype (PhysicalPrimitiveCarrier R) := inst
    exact physicalPrimitive_card_le_two R
  · intro α R inst hm hv
    letI : Fintype (PhysicalPrimitiveCarrier R) := inst
    exact physicalPrimitive_card_eq_two R hm hv

end D0.Foundation.PhysicalComparisonRepresentation
