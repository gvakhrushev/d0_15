import Mathlib.Tactic

/-!
# General `n`-capability comparison grammar

`D0.Foundation.AdmissibleComparisonGrammar` fixes two detection capabilities
(membership and value) and proves the primitive comparisons number exactly two.
`D0.Foundation.PhysicalComparisonRepresentation` reduces the physical
exhaustion to a representation into that two-capability grammar.  Both, however,
take the number of capabilities to be `2` as an input.  The honest question one
level deeper is: *why two?*  If the count of primitive comparison kinds is what
ultimately stops the zone tower at three, then the number `2` must be traced to
the number of independent detection capabilities, not hidden in a datatype with
two constructors.

This module makes that dependency transparent.  A raw comparison over `n`
capabilities is a Boolean capability vector `Fin n → Bool`; no target count is
built in.  With the same conclusion-free notions — operational, subcomparison,
`join`, decomposable, primitive — the module proves, for **every** `n`:

* `primitive_iff_atomic` — a comparison is indecomposable iff it inspects
  exactly one capability;
* `primitive_card_eq` — the primitive comparisons number **exactly `n`**.

So the count of primitive comparison kinds equals the count of independent
capabilities, with no circular constructor enumeration.  The D0 case is the
instance `n = 2` (`two_capabilities_two_primitives`); the boundary instances
`n = 0, 1, 3` show the count genuinely tracks `n` and is not an artefact of a
two-element type.  In particular, a forced third detection capability would give
three primitive kinds — the exact falsifier the degree-2 exhaustion needs.

Honest boundary: this reduces "exactly two comparison kinds" to "exactly two
independent detection capabilities."  That the detection act has exactly two
capabilities (membership and value) remains the single named external input;
it is not proved here.
-/

namespace D0.Foundation.GeneralComparisonGrammar

/-- A raw comparison over `n` independent detection capabilities: for each
capability, whether the comparison inspects it. -/
abbrev GenComparison (n : ℕ) := Fin n → Bool

variable {n : ℕ}

/-- A comparison is operational when it inspects at least one capability. -/
def Operational (c : GenComparison n) : Prop := ∃ i, c i = true

/-- A comparison is atomic when it inspects exactly one capability. -/
def Atomic (c : GenComparison n) : Prop :=
  ∃ i, c i = true ∧ ∀ j, c j = true → j = i

/-- Capability inclusion. -/
def Subcomparison (a b : GenComparison n) : Prop := ∀ i, a i = true → b i = true

/-- Strict capability inclusion. -/
def ProperSubcomparison (a b : GenComparison n) : Prop := Subcomparison a b ∧ a ≠ b

/-- Combine the capabilities of two comparisons. -/
def join (a b : GenComparison n) : GenComparison n := fun i => a i || b i

/-- A comparison is decomposable when it is the join of two strictly smaller
operational comparisons. -/
def Decomposable (c : GenComparison n) : Prop :=
  ∃ a b, Operational a ∧ Operational b ∧
    ProperSubcomparison a c ∧ ProperSubcomparison b c ∧ join a b = c

/-- A primitive comparison is operational and not decomposable — defined
without naming a target cardinality. -/
def Primitive (c : GenComparison n) : Prop := Operational c ∧ ¬ Decomposable c

/-- The atomic comparison inspecting exactly capability `i`. -/
def atomicOf (i : Fin n) : GenComparison n := fun j => decide (j = i)

theorem atomicOf_atomic (i : Fin n) : Atomic (atomicOf i) := by
  refine ⟨i, by simp [atomicOf], ?_⟩
  intro j hj
  exact of_decide_eq_true (by simpa [atomicOf] using hj)

/-- **Atomic comparisons are primitive.** A one-capability comparison cannot be
the join of two strictly smaller operational comparisons: any operational
subcomparison already carries the single capability, hence equals it. -/
theorem atomic_primitive {c : GenComparison n} (h : Atomic c) : Primitive c := by
  obtain ⟨i, hi, huniq⟩ := h
  refine ⟨⟨i, hi⟩, ?_⟩
  rintro ⟨a, b, ⟨ia, hia⟩, -, ⟨hsa, hnea⟩, -, -⟩
  apply hnea
  have hIaEqI : ia = i := huniq ia (hsa ia hia)
  have hai : a i = true := hIaEqI ▸ hia
  funext k
  rcases Bool.dichotomy (a k) with hak | hak
  · rcases Bool.dichotomy (c k) with hck | hck
    · rw [hak, hck]
    · exfalso
      have hki : k = i := huniq k hck
      rw [hki, hai] at hak
      simp at hak
  · have hck : c k = true := hsa k hak
    rw [hak, hck]

/-- **Primitive comparisons are atomic.** An operational comparison inspecting
two distinct capabilities splits: remove one capability and adjoin its
singleton; the two pieces are strictly smaller, operational, and join to the
original. -/
theorem primitive_atomic {c : GenComparison n} (h : Primitive c) : Atomic c := by
  obtain ⟨hop, hnd⟩ := h
  by_contra hna
  apply hnd
  obtain ⟨i, hi⟩ := hop
  have hnu : ¬ ∀ j, c j = true → j = i := fun huniq => hna ⟨i, hi, huniq⟩
  obtain ⟨j, hj, hji⟩ : ∃ j, c j = true ∧ j ≠ i := by
    by_contra hcon
    apply hnu
    intro j hcj
    by_contra hjne
    exact hcon ⟨j, hcj, hjne⟩
  refine ⟨fun k => if k = j then false else c k, fun k => decide (k = j),
          ?_, ?_, ?_, ?_, ?_⟩
  · -- Operational a (via `i`, since `i ≠ j`)
    exact ⟨i, by simp [Ne.symm hji, hi]⟩
  · -- Operational b (via `j`)
    exact ⟨j, by simp⟩
  · -- a is a strict operational subcomparison
    refine ⟨?_, ?_⟩
    · intro k hk
      by_cases hkj : k = j
      · simp [hkj] at hk
      · simpa [hkj] using hk
    · intro heq
      have h1 := congrFun heq j
      simp [hj] at h1
  · -- b is a strict operational subcomparison
    refine ⟨?_, ?_⟩
    · intro k hk
      by_cases hkj : k = j
      · simp [hkj, hj]
      · simp [hkj] at hk
    · intro heq
      have h2 := congrFun heq i
      simp [Ne.symm hji, hi] at h2
  · -- the join recovers `c`
    funext k
    by_cases hkj : k = j
    · subst hkj; simp [join, hj]
    · simp [join, hkj]

/-- **Primitive iff atomic, for every capability count.** -/
theorem primitive_iff_atomic (c : GenComparison n) : Primitive c ↔ Atomic c :=
  ⟨primitive_atomic, atomic_primitive⟩

/-- The capability inspected by an atomic comparison. -/
noncomputable def atomicIndex {c : GenComparison n} (h : Atomic c) : Fin n := h.choose

theorem atomicIndex_true {c : GenComparison n} (h : Atomic c) :
    c (atomicIndex h) = true := h.choose_spec.1

theorem atomicIndex_uniq {c : GenComparison n} (h : Atomic c) :
    ∀ j, c j = true → j = atomicIndex h := h.choose_spec.2

theorem atomicOf_eq_of_atomic {c : GenComparison n} (h : Atomic c) :
    atomicOf (atomicIndex h) = c := by
  funext k
  rcases Bool.dichotomy (c k) with hck | hck
  · have hne : k ≠ atomicIndex h := by
      intro hk
      rw [hk, atomicIndex_true h] at hck
      simp at hck
    simp [atomicOf, hne, hck]
  · have hk : k = atomicIndex h := atomicIndex_uniq h k hck
    rw [hk, atomicIndex_true h]
    simp [atomicOf]

theorem atomicIndex_atomicOf (i : Fin n) :
    atomicIndex (atomicOf_atomic i) = i :=
  of_decide_eq_true (by simpa [atomicOf] using atomicIndex_true (atomicOf_atomic i))

/-- The primitive comparisons over `n` capabilities are in bijection with the
`n` capabilities themselves. -/
noncomputable def primitiveEquivFin (n : ℕ) :
    {c : GenComparison n // Primitive c} ≃ Fin n where
  toFun c := atomicIndex ((primitive_iff_atomic c.1).mp c.2)
  invFun i := ⟨atomicOf i, (primitive_iff_atomic (atomicOf i)).mpr (atomicOf_atomic i)⟩
  left_inv := by
    rintro ⟨c, hc⟩
    exact Subtype.ext (atomicOf_eq_of_atomic ((primitive_iff_atomic c).mp hc))
  right_inv := by
    intro i
    exact atomicIndex_atomicOf i

/-- **The count of primitive comparison kinds equals the count of independent
detection capabilities.**  No target cardinality is assumed anywhere; the
number `n` emerges as the conclusion. -/
theorem primitive_card_eq (n : ℕ) :
    Nat.card {c : GenComparison n // Primitive c} = n := by
  rw [Nat.card_congr (primitiveEquivFin n), Nat.card_eq_fintype_card, Fintype.card_fin]

/-- Boundary instance: no capabilities ⇒ no primitive comparisons. -/
theorem zero_capabilities_no_primitive :
    Nat.card {c : GenComparison 0 // Primitive c} = 0 := primitive_card_eq 0

/-- Boundary instance: one capability ⇒ exactly one primitive comparison. -/
theorem one_capability_one_primitive :
    Nat.card {c : GenComparison 1 // Primitive c} = 1 := primitive_card_eq 1

/-- The D0 case: the two detection capabilities (membership, value) give exactly
two primitive comparison kinds — the `2` now exposed as the capability count. -/
theorem two_capabilities_two_primitives :
    Nat.card {c : GenComparison 2 // Primitive c} = 2 := primitive_card_eq 2

/-- Falsifier instance: a forced third detection capability would give three
primitive comparison kinds, breaking the degree-2 exhaustion. -/
theorem three_capabilities_three_primitives :
    Nat.card {c : GenComparison 3 // Primitive c} = 3 := primitive_card_eq 3

/-- **D0-GENERAL-COMPARISON-CAPABILITY-COUNT-001.** For every capability count
`n`, indecomposability equals single-capability atomicity and the primitive
comparisons number exactly `n`.  The specific value `2` in the D0 detection
grammar is therefore exactly the number of independent detection capabilities,
not a constructor artefact; the boundary instances `0,1,3` confirm the count
tracks `n`. -/
theorem general_comparison_capability_count :
    (∀ (m : ℕ) (c : GenComparison m), Primitive c ↔ Atomic c) ∧
    (∀ m : ℕ, Nat.card {c : GenComparison m // Primitive c} = m) ∧
    Nat.card {c : GenComparison 0 // Primitive c} = 0 ∧
    Nat.card {c : GenComparison 1 // Primitive c} = 1 ∧
    Nat.card {c : GenComparison 2 // Primitive c} = 2 ∧
    Nat.card {c : GenComparison 3 // Primitive c} = 3 :=
  ⟨fun _ c => primitive_iff_atomic c, primitive_card_eq,
   zero_capabilities_no_primitive, one_capability_one_primitive,
   two_capabilities_two_primitives, three_capabilities_three_primitives⟩

end D0.Foundation.GeneralComparisonGrammar
