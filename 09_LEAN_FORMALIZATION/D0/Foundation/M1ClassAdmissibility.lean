import D0.Foundation.M1Predicate

/-!
# M1 class admissibility: no-catalogue classes and unique forcing as the singleton case

The canonical `M1Forced Forced a` predicate is intentionally a **unique-answer** contract.
That is the correct interface for a finite selector or a uniquely solved constraint, but not for
an admissible class with many allowed objects.

This module adds the missing complementary interface. A catalogue system consists of:

* candidate objects;
* a possible external catalogue;
* the observable output of a candidate under a catalogue.

A candidate is `M1ClassAdmissible` when its output is invariant under every catalogue change.
This formalizes "no mandatory external catalogue" without requiring one unique candidate.

The two M1 interfaces are compatible, not competing:

* `M1ClassAdmissible` filters a class by catalogue-independence;
* `M1Forced` selects a unique answer when an additional canonical constraint has exactly one
  witness;
* every `M1Forced` constraint has a singleton witness carrier, proved by an explicit equivalence
  with `PUnit`.

This supplies the class-level foundation needed by detector-layer representation while preserving
the exact scope of the existing `D0-M1-PREDICATE-001`.
-/

namespace D0.Foundation.M1ClassAdmissibility

open D0.Foundation

universe u v w

/-- A family of candidate objects evaluated under a possibly external catalogue. -/
structure CatalogueSystem where
  Candidate : Type u
  Catalogue : Type v
  Output : Type w
  eval : Candidate → Catalogue → Output

/-- **Class-level M1 admissibility.** The candidate's observable output is independent of every
external catalogue choice. -/
def M1ClassAdmissible (S : CatalogueSystem) (a : S.Candidate) : Prop :=
  ∀ c c' : S.Catalogue, S.eval a c = S.eval a c'

/-- Carrier of all class-admissible candidates. It may contain zero, one, or many objects. -/
abbrev M1AdmissibleCarrier (S : CatalogueSystem) :=
  {a : S.Candidate // M1ClassAdmissible S a}

/-- A catalogue-independent candidate remains admissible under any reindexing of catalogues. -/
theorem admissible_under_catalogue_map
    (S : CatalogueSystem) (a : S.Candidate)
    (h : M1ClassAdmissible S a)
    {C' : Type*} (f : C' → S.Catalogue) :
    ∀ x y : C', S.eval a (f x) = S.eval a (f y) := by
  intro x y
  exact h (f x) (f y)

/-- A candidate constant in the catalogue argument is class-admissible. -/
theorem constant_catalogue_admissible
    {A C O : Type*} (out : A → O) (a : A) :
    M1ClassAdmissible
      ⟨A, C, O, fun x _ => out x⟩ a := by
  intro _ _
  rfl

/-- A faithful representation of an arbitrary physical candidate class in a class-level M1
catalogue system. -/
structure ClassRepresentation (S : CatalogueSystem) (Phys : Type*) where
  candidate : Phys → S.Candidate
  admissible : Phys → Prop
  admissible_iff :
    ∀ p, admissible p ↔ M1ClassAdmissible S (candidate p)
  candidate_injective_on_admissible :
    ∀ {p q}, admissible p → admissible q →
      candidate p = candidate q → p = q

/-- Carrier of physically admissible objects in a class representation. -/
abbrev AdmissiblePhysical {S : CatalogueSystem} {Phys : Type*}
    (R : ClassRepresentation S Phys) :=
  {p : Phys // R.admissible p}

/-- Every class representation gives a canonical embedding of admissible physical objects into
the M1-admissible carrier. -/
def classRepresentationEmbedding
    {S : CatalogueSystem} {Phys : Type*}
    (R : ClassRepresentation S Phys) :
    AdmissiblePhysical R ↪ M1AdmissibleCarrier S where
  toFun p :=
    ⟨R.candidate p.1, (R.admissible_iff p.1).mp p.2⟩
  inj' := by
    intro p q h
    apply Subtype.ext
    apply R.candidate_injective_on_admissible p.2 q.2
    exact congrArg Subtype.val h

/-- The witness carrier of a canonical constraint. -/
abbrev ForcedCarrier {α : Type} (Forced : α → Prop) :=
  {a : α // Forced a}

/-- **Unique-answer forcing is the singleton special case of class admissibility.** If `a` is
`M1Forced` by `Forced`, then the entire witness carrier of `Forced` is equivalent to `PUnit`. -/
def m1ForcedCarrierEquivPUnit
    {α : Type} {Forced : α → Prop} {a : α}
    (h : M1Forced Forced a) :
    ForcedCarrier Forced ≃ PUnit.{0} where
  toFun _ := PUnit.unit
  invFun _ := ⟨a, h.forced⟩
  left_inv := by
    intro b
    apply Subtype.ext
    exact (h.unique b.1 b.2).symm
  right_inv := by
    intro u
    cases u
    rfl

/-- Consequently the canonical forced-answer carrier has cardinality one whenever it is finite. -/
theorem m1ForcedCarrier_card_one
    {α : Type} {Forced : α → Prop} {a : α}
    (h : M1Forced Forced a) :
    Nat.card (ForcedCarrier Forced) = 1 := by
  letI : Nonempty (ForcedCarrier Forced) := ⟨⟨a, h.forced⟩⟩
  letI : Subsingleton (ForcedCarrier Forced) :=
    ⟨fun x y => Subtype.ext
      ((h.unique x.1 x.2).trans (h.unique y.1 y.2).symm)⟩
  exact Nat.card_unique

/-- A non-singleton admissible class cannot be represented as one `M1Forced` answer under that
same class predicate. -/
theorem non_singleton_class_not_M1Forced
    {α : Type} (Allowed : α → Prop)
    {x y : α} (hx : Allowed x) (hy : Allowed y) (hne : x ≠ y) :
    ¬ ∃ a : α, M1Forced Allowed a := by
  rintro ⟨a, ha⟩
  have hxa : x = a := ha.unique x hx
  have hya : y = a := ha.unique y hy
  exact hne (hxa.trans hya.symm)

theorem class_with_two_witnesses_not_M1Forced
    {α : Type} (Allowed : α → Prop)
    (h : ∃ x y : α, Allowed x ∧ Allowed y ∧ x ≠ y) :
    ¬ ∃ a : α, M1Forced Allowed a := by
  rcases h with ⟨x, y, hx, hy, hne⟩
  exact non_singleton_class_not_M1Forced Allowed hx hy hne

/-- Two-stage M1 capstone: class admissibility handles catalogue-independence; unique forcing,
when present, is exactly the singleton witness case. -/
theorem m1_class_admissibility_boundary :
    (∀ (S : CatalogueSystem) (a : S.Candidate),
      M1ClassAdmissible S a ↔
        ∀ c c' : S.Catalogue, S.eval a c = S.eval a c')
    ∧ (∀ {α : Type} {Forced : α → Prop},
        (∃ a : α, M1Forced Forced a) →
        Nat.card (ForcedCarrier Forced) = 1)
    ∧ (∀ {α : Type} (Allowed : α → Prop),
        (∃ x y : α, Allowed x ∧ Allowed y ∧ x ≠ y) →
        ¬ ∃ a : α, M1Forced Allowed a)
    ∧ (∀ (S : CatalogueSystem) (Phys : Type*)
        (R : ClassRepresentation S Phys),
        Nonempty (AdmissiblePhysical R ↪ M1AdmissibleCarrier S)) :=
  ⟨fun _ _ => Iff.rfl,
    fun ⟨_, h⟩ => m1ForcedCarrier_card_one h,
    class_with_two_witnesses_not_M1Forced,
    fun _ _ R => ⟨classRepresentationEmbedding R⟩⟩

end D0.Foundation.M1ClassAdmissibility
