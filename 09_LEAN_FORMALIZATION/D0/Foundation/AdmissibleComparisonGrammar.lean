import D0.Tower.DetectionQuadratic
import Mathlib.Tactic

/-!
# A conclusion-free grammar for the detection comparison kinds

`D0.Tower.DetectionQuadratic` declares the two intended comparison kinds,
`membership` and `value`.  Merely counting the constructors of that declared
type does not prove that they exhaust arbitrary admissible comparisons.

This module starts one level earlier.  A raw comparison is described only by
the two capabilities already named by the detection argument:

* it may inspect membership/category data;
* it may inspect value data.

No target count is placed in the raw type.  The resulting Boolean capability
grammar has four points.  Requiring operational relevance removes only the
empty point and leaves **three** comparisons: membership-only, value-only, and
the hybrid using both capabilities.  Thus operationality alone does not imply
the claimed two-kind exhaustion.

The missing distinction is isolated exactly:

* `Atomic` says that a comparison uses exactly one primitive capability;
* under `Atomic`, and only under it, the raw grammar is equivalent to the
  existing `ComparisonKind`;
* the hybrid is an explicit operational negative control showing atomicity is
  not implied by operationality;
* `Primitive` is the conclusion-free replacement: an operational comparison
  that cannot be decomposed into two strictly smaller operational comparisons.
  In the raw capability lattice, `Primitive ↔ Atomic`, so the primitive atoms
  are exactly the existing two kinds while the hybrid is their composite.

The finite capability-lattice exhaustion is therefore proved here without
putting the target count in an inductive declaration.  Honest residual: this
does not prove that every physical/M1-admissible comparison is represented by
this two-capability grammar.  The remaining theorem must derive that
representation from the actual protocol rather than assume it.
-/

namespace D0.Foundation.AdmissibleComparisonGrammar

open D0.Tower

/-- A comparison before its kind has been classified.  The fields record
capabilities, not a preselected constructor from the desired answer type. -/
@[ext]
structure RawComparison where
  usesMembership : Bool
  usesValue : Bool
deriving DecidableEq, Fintype

/-- A comparison is operational when it examines at least one source of data. -/
def Operational (c : RawComparison) : Prop :=
  c.usesMembership = true ∨ c.usesValue = true

/-- Atomic comparisons use exactly one of the two primitive capabilities. -/
def Atomic (c : RawComparison) : Prop :=
  (c.usesMembership = true ∧ c.usesValue = false) ∨
  (c.usesMembership = false ∧ c.usesValue = true)

/-- Capability inclusion between raw comparisons. -/
def Subcomparison (a b : RawComparison) : Prop :=
  (a.usesMembership = true → b.usesMembership = true) ∧
  (a.usesValue = true → b.usesValue = true)

/-- Strict capability inclusion. -/
def ProperSubcomparison (a b : RawComparison) : Prop :=
  Subcomparison a b ∧ a ≠ b

/-- Combine the capabilities of two comparisons. -/
def join (a b : RawComparison) : RawComparison :=
  ⟨a.usesMembership || b.usesMembership,
   a.usesValue || b.usesValue⟩

/-- A raw comparison is decomposable when it is the join of two strictly
smaller operational comparisons. -/
def Decomposable (c : RawComparison) : Prop :=
  ∃ a b : RawComparison,
    Operational a ∧ Operational b ∧
    ProperSubcomparison a c ∧ ProperSubcomparison b c ∧
    join a b = c

/-- A primitive comparison is operational and cannot be assembled from two
strictly smaller operational comparisons.  Unlike `Atomic`, this definition
does not mention the expected constructors or a target cardinality. -/
def Primitive (c : RawComparison) : Prop :=
  Operational c ∧ ¬ Decomposable c

instance operationalDecidable (c : RawComparison) : Decidable (Operational c) := by
  unfold Operational
  infer_instance

instance atomicDecidable (c : RawComparison) : Decidable (Atomic c) := by
  unfold Atomic
  infer_instance

instance subcomparisonDecidable (a b : RawComparison) : Decidable (Subcomparison a b) := by
  unfold Subcomparison
  infer_instance

instance properSubcomparisonDecidable (a b : RawComparison) :
    Decidable (ProperSubcomparison a b) := by
  unfold ProperSubcomparison
  infer_instance

instance decomposableDecidable (c : RawComparison) : Decidable (Decomposable c) := by
  unfold Decomposable
  infer_instance

instance primitiveDecidable (c : RawComparison) : Decidable (Primitive c) := by
  unfold Primitive
  infer_instance

/-- The membership-only comparison represented in the raw grammar. -/
def membershipOnly : RawComparison := ⟨true, false⟩

/-- The value-only comparison represented in the raw grammar. -/
def valueOnly : RawComparison := ⟨false, true⟩

/-- The comparison that simultaneously uses membership and value data. -/
def hybridComparison : RawComparison := ⟨true, true⟩

/-- The empty comparison, retained as a negative control for operationality. -/
def emptyComparison : RawComparison := ⟨false, false⟩

/-- Every operational raw comparison is one of the two atomic comparisons or
the hybrid.  This is an exhaustive theorem over the raw grammar, not a
constructor count over `ComparisonKind`. -/
theorem operational_exhaustion_three (c : RawComparison) (hc : Operational c) :
    c = membershipOnly ∨ c = valueOnly ∨ c = hybridComparison := by
  rcases c with ⟨m, v⟩
  cases m <;> cases v <;> simp [Operational, membershipOnly, valueOnly, hybridComparison] at hc ⊢

/-- Operational comparisons number three in the conclusion-free capability
grammar.  In particular, operationality does not recover the declared
two-constructor kind. -/
theorem operational_comparison_count_three :
    Fintype.card {c : RawComparison // Operational c} = 3 := by
  native_decide

/-- Atomicity is exactly the statement that the raw comparison is one of the
two existing kinds. -/
theorem atomic_iff_existing_kind (c : RawComparison) :
    Atomic c ↔ c = membershipOnly ∨ c = valueOnly := by
  rcases c with ⟨m, v⟩
  cases m <;> cases v <;> simp [Atomic, membershipOnly, valueOnly]

/-- Decode an existing comparison kind into the conclusion-free grammar. -/
def ofComparisonKind : ComparisonKind → RawComparison
  | .membership => membershipOnly
  | .value => valueOnly

theorem ofComparisonKind_atomic (k : ComparisonKind) : Atomic (ofComparisonKind k) := by
  cases k <;> simp [ofComparisonKind, Atomic, membershipOnly, valueOnly]

/-- Classify a raw comparison once atomicity has actually been proved. -/
def toComparisonKind (c : {c : RawComparison // Atomic c}) : ComparisonKind := by
  rcases c with ⟨⟨m, v⟩, h⟩
  cases m <;> cases v
  · simp [Atomic] at h
  · exact .value
  · exact .membership
  · simp [Atomic] at h

/-- Atomic raw comparisons are precisely the existing two-kind type. -/
def atomicComparisonEquiv : {c : RawComparison // Atomic c} ≃ ComparisonKind where
  toFun := toComparisonKind
  invFun := fun k => ⟨ofComparisonKind k, ofComparisonKind_atomic k⟩
  left_inv := by
    rintro ⟨⟨m, v⟩, h⟩
    cases m <;> cases v
    · simp [Atomic] at h
    · rfl
    · rfl
    · simp [Atomic] at h
  right_inv := by
    intro k
    cases k <;> rfl

theorem atomic_comparison_count_two :
    Fintype.card {c : RawComparison // Atomic c} = 2 := by
  rw [Fintype.card_congr atomicComparisonEquiv]
  exact two_comparison_kinds

/-- The hybrid is operational. -/
theorem hybrid_operational : Operational hybridComparison := by
  simp [Operational, hybridComparison]

/-- The hybrid is not atomic, so it is not represented by either declared
comparison kind. -/
theorem hybrid_not_atomic : ¬ Atomic hybridComparison := by
  simp [Atomic, hybridComparison]

/-- Explicit counterexample to the unproved exhaustivity sentence:
operationality alone does not imply membership-only or value-only. -/
theorem operational_does_not_imply_existing_kind :
    ∃ c : RawComparison,
      Operational c ∧ c ≠ membershipOnly ∧ c ≠ valueOnly := by
  exact ⟨hybridComparison, hybrid_operational, by decide, by decide⟩

/-- Operationality does not imply atomicity. -/
theorem operational_does_not_imply_atomic :
    ¬ ∀ c : RawComparison, Operational c → Atomic c := by
  intro h
  exact hybrid_not_atomic (h hybridComparison hybrid_operational)

/-- Dropping operationality admits the empty comparison, showing that the
operational guard is independently load-bearing. -/
theorem empty_not_operational : ¬ Operational emptyComparison := by
  simp [Operational, emptyComparison]

/-- The hybrid comparison is canonically the join of the two atomic
comparisons. -/
theorem hybrid_decomposition :
    join membershipOnly valueOnly = hybridComparison := by
  rfl

/-- The hybrid is not an independent primitive: both atomic comparisons are
strict operational subcomparisons and their join is the hybrid. -/
theorem hybrid_decomposable : Decomposable hybridComparison := by
  refine ⟨membershipOnly, valueOnly, ?_, ?_, ?_, ?_, hybrid_decomposition⟩
  · simp [Operational, membershipOnly]
  · simp [Operational, valueOnly]
  · constructor
    · simp [Subcomparison, membershipOnly, hybridComparison]
    · decide
  · constructor
    · simp [Subcomparison, valueOnly, hybridComparison]
    · decide

/-- **Conclusion-free primitive classification.** Indecomposability in the raw
capability lattice is equivalent to atomicity.  The result is obtained by
exhausting the four raw capability records, not by enumerating the desired
`ComparisonKind` constructors. -/
theorem primitive_iff_atomic (c : RawComparison) :
    Primitive c ↔ Atomic c := by
  rcases c with ⟨m, v⟩
  cases m <;> cases v <;> native_decide

/-- There are exactly two primitive comparisons in the raw grammar. -/
theorem primitive_comparison_count_two :
    Fintype.card {c : RawComparison // Primitive c} = 2 := by
  native_decide

/-- Every primitive raw comparison is represented by one of the existing
comparison kinds. -/
theorem primitive_classified_by_existing_kind
    (c : RawComparison) (hc : Primitive c) :
    c = membershipOnly ∨ c = valueOnly :=
  (atomic_iff_existing_kind c).mp ((primitive_iff_atomic c).mp hc)

/-- Every operational comparison is either primitive, or is exactly the
canonical hybrid composite of the two primitive comparisons. -/
theorem operational_primitive_or_hybrid
    (c : RawComparison) (hc : Operational c) :
    Primitive c ∨ c = hybridComparison := by
  rcases operational_exhaustion_three c hc with h | h | h
  · left
    rw [h, primitive_iff_atomic]
    simp [Atomic, membershipOnly]
  · left
    rw [h, primitive_iff_atomic]
    simp [Atomic, valueOnly]
  · exact Or.inr h

/-- **Positive primitive-exhaustion theorem.** The raw capability grammar has
exactly two indecomposable operational atoms, and every other operational
comparison is their canonical hybrid join.  This closes the finite
capability-lattice classification; it does not by itself prove that every
physical/M1-admissible comparison is represented by this two-capability raw
grammar. -/
theorem primitive_comparison_exhaustion :
    Fintype.card {c : RawComparison // Primitive c} = 2 ∧
    (∀ c : RawComparison, Primitive c →
      c = membershipOnly ∨ c = valueOnly) ∧
    Decomposable hybridComparison ∧
    join membershipOnly valueOnly = hybridComparison :=
  ⟨primitive_comparison_count_two, primitive_classified_by_existing_kind,
   hybrid_decomposable, hybrid_decomposition⟩

/-- **Boundary bundle.**  The raw grammar has three operational comparison
forms, exactly two primitive atoms, and the hybrid is their decomposable join.
Operationality alone still does not imply atomicity.

Closing `D0-P-DEGREE2-EXHAUSTION-001` therefore requires a new theorem that
maps every physical/M1-admissible comparison into this raw capability grammar
while preserving primitive/decomposable structure. -/
theorem admissible_comparison_grammar_boundary :
    Fintype.card {c : RawComparison // Operational c} = 3 ∧
    Fintype.card {c : RawComparison // Atomic c} = 2 ∧
    Fintype.card {c : RawComparison // Primitive c} = 2 ∧
    Operational hybridComparison ∧
    ¬ Atomic hybridComparison ∧
    Decomposable hybridComparison ∧
    (¬ ∀ c : RawComparison, Operational c → Atomic c) :=
  ⟨operational_comparison_count_three, atomic_comparison_count_two,
   primitive_comparison_count_two, hybrid_operational, hybrid_not_atomic,
   hybrid_decomposable, operational_does_not_imply_atomic⟩

end D0.Foundation.AdmissibleComparisonGrammar
