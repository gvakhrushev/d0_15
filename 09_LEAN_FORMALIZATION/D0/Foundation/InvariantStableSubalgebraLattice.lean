import D0.Foundation.PartitionAlgebra
import D0.Foundation.InvariantAlgebraDegree
import Mathlib.Tactic

/-!
# Setwise-stable observable algebras: the equivariant partition bridge

DRAFT module for `_TASKS_CENTER_ATTACK/INVARIANT_STABLE_LATTICE_MEMO.md`. No registry row is
minted here.

`D0.Foundation.InvariantMinimal` works with a **pointwise-fixed classifier**
`c (g x) = c x`. A setwise GraphAut-stable subalgebra is a larger and different object: GraphAut
may permute the algebra's induced partition blocks. The earlier editorial audit
`INVARIANT_MINIMAL_DOMAIN_MEMO.md` computed eight degree-containing stable partition algebras but
left the load-bearing equivariant correspondence open.

This module supplies the missing theorem-grade bridge on the frozen `K(9,11,13)` carrier:

* `insep_graphAut_invariant_iff` — a setwise-stable unital subalgebra induces a GraphAut-invariant
  inseparability relation (both directions, with the inverse action explicit);
* `insep_imp_same_zone` — containing the computed degree confines every class to one zone;
* `within_zone_dichotomy` — full within-zone transpositions leave only two possibilities in each
  zone: one whole class or equality. A partially resolved zone is impossible;
* `stable_degree_relation_classification` — the induced relation is therefore determined by three
  independent booleans, one per zone. The exact compute companion independently enumerates the
  resulting `2^3 = 8` partition algebras and their dimensions `3,11,13,15,21,23,25,33`.

Honest scope: this is finite rational function algebra on the already frozen scene. It does not
derive the scene, the degree observable, physical generation names, or an M1 licensing principle.
The eight-algebra cardinality and finrank formula remain computation-grade in the companion script
until the explicit canonical subalgebras are formalized; the Lean capstone classifies the induced
relations without importing those computed counts as hypotheses.
-/

namespace D0.Foundation.InvariantStableSubalgebraLattice

open D0.Foundation.InvariantMinimal
open D0.Foundation.InvariantAlgebraDegree
open D0.Foundation.PartitionAlgebra

abbrev Vertex := Fin 33
abbrev Functions := Vertex → ℚ

/-- Pullback of a vertex function along a full graph automorphism. -/
def act (σ : GraphAut) (f : Functions) : Functions := fun i => f (σ i)

@[simp] theorem act_apply (σ : GraphAut) (f : Functions) (i : Vertex) :
    act σ f i = f (σ i) := rfl

@[simp] theorem act_id (f : Functions) : act (1 : GraphAut) f = f := by
  funext i
  rfl

@[simp] theorem act_trans_symm (σ : GraphAut) (f : Functions) :
    act σ.symm (act σ f) = f := by
  funext i
  simp [act]

@[simp] theorem act_symm_trans (σ : GraphAut) (f : Functions) :
    act σ (act σ.symm f) = f := by
  funext i
  simp [act]

/-- A unital observable algebra is setwise stable when pullback by every graph automorphism keeps
all of its members in the algebra. -/
def IsStable (A : Subalgebra ℚ Functions) : Prop :=
  ∀ σ : GraphAut, ∀ f : Functions, f ∈ A → act σ f ∈ A

/-- The computed degree observable, rational-valued. -/
def degreeQ : Functions := fun i => (deg i : ℚ)

/-! ## The missing equivariant subalgebra/partition bridge -/

/-- Stability transports inseparability forward. This is the missing equivariant direction of the
finite subalgebra/partition correspondence: the relation, not a chosen classifier, is invariant. -/
theorem insep_graphAut_forward {A : Subalgebra ℚ Functions} (hA : IsStable A)
    (σ : GraphAut) {i j : Vertex} (hij : Insep A i j) : Insep A (σ i) (σ j) := by
  intro f hf
  have hback : act σ.symm f ∈ A := hA σ.symm f hf
  have h := hij (act σ.symm f) hback
  simpa [act] using h

/-- **Equivariant bridge (both directions).** A setwise-stable subalgebra's induced partition
relation is invariant under the full graph automorphism group. -/
theorem insep_graphAut_invariant_iff {A : Subalgebra ℚ Functions} (hA : IsStable A)
    (σ : GraphAut) (i j : Vertex) :
    Insep A (σ i) (σ j) ↔ Insep A i j := by
  constructor
  · intro h
    have := insep_graphAut_forward hA σ.symm h
    simpa using this
  · exact insep_graphAut_forward hA σ

/-! ## Degree confines classes to zones -/

/-- If the algebra contains the computed degree, inseparable vertices have equal degree. -/
theorem insep_imp_same_degree {A : Subalgebra ℚ Functions} (hdeg : degreeQ ∈ A)
    {i j : Vertex} (hij : Insep A i j) : deg i = deg j := by
  have h := hij degreeQ hdeg
  exact_mod_cast h

/-- If the algebra contains degree, every induced partition class lies inside one zone. -/
theorem insep_imp_same_zone {A : Subalgebra ℚ Functions} (hdeg : degreeQ ∈ A)
    {i j : Vertex} (hij : Insep A i j) : zoneOf i = zoneOf j :=
  (degree_eq_iff_zone i j).mp (insep_imp_same_degree hdeg hij)

/-! ## Full symmetric action leaves no partial zone refinement -/

/-- One nontrivial inseparable pair in a zone forces every distinct pair in that zone to be
inseparable. The proof conjugates the named pair to the target pair by at most two genuine graph
automorphisms (within-zone transpositions), then uses transitivity of `Insep`. -/
theorem one_pair_forces_zone_indiscrete {A : Subalgebra ℚ Functions} (hA : IsStable A)
    {a b : Vertex} (habZone : zoneOf a = zoneOf b) (habNe : a ≠ b)
    (hab : Insep A a b) :
    ∀ i j : Vertex, zoneOf i = zoneOf a → zoneOf j = zoneOf a → Insep A i j := by
  intro i j hi hj
  by_cases hij : i = j
  · subst j
    exact insep_refl A i
  have hia : zoneOf i = zoneOf a := hi
  have hib : zoneOf i = zoneOf b := hi.trans habZone
  have hja : zoneOf j = zoneOf a := hj
  have hjb : zoneOf j = zoneOf b := hj.trans habZone
  by_cases hiaEq : i = a
  · subst i
    have hσ := (insep_graphAut_invariant_iff hA
      (swapGraphAutOfSameZone b j (hib.symm.trans hjb)) a b).2 hab
    simpa [swapGraphAutOfSameZone, habNe, hij] using hσ
  by_cases hibEq : i = b
  · subst i
    have hσ := (insep_graphAut_invariant_iff hA
      (swapGraphAutOfSameZone a j (habZone.trans hja)) a b).2 hab
    have hsymm := insep_symm hσ
    simpa [swapGraphAutOfSameZone, habNe, hij] using hsymm
  · have hai : Insep A a i := by
      have hσ := (insep_graphAut_invariant_iff hA
        (swapGraphAutOfSameZone b i (habZone.symm.trans hi.symm)) a b).2 hab
      simpa [swapGraphAutOfSameZone, hiaEq, hibEq] using hσ
    by_cases hjaEq : j = a
    · subst j
      exact insep_symm hai
    by_cases hjbEq : j = b
    · subst j
      exact insep_trans (insep_symm hai) hab
    · have haj : Insep A a j := by
        have hσ := (insep_graphAut_invariant_iff hA
          (swapGraphAutOfSameZone b j (habZone.symm.trans hj.symm)) a b).2 hab
        simpa [swapGraphAutOfSameZone, hjaEq, hjbEq] using hσ
      exact insep_trans (insep_symm hai) haj

/-- **Within-zone dichotomy.** On each zone, a stable algebra's induced relation is either the
whole zone or equality. This exhausts the class quantified over; no intermediate partition is
silently omitted. -/
theorem within_zone_dichotomy {A : Subalgebra ℚ Functions} (hA : IsStable A) (z : Fin 3) :
    (∀ i j : Vertex, zoneOf i = z → zoneOf j = z → Insep A i j) ∨
    (∀ i j : Vertex, zoneOf i = z → zoneOf j = z → Insep A i j → i = j) := by
  classical
  by_cases hpair : ∃ a b : Vertex,
      zoneOf a = z ∧ zoneOf b = z ∧ a ≠ b ∧ Insep A a b
  · rcases hpair with ⟨a, b, ha, hb, habNe, hab⟩
    left
    intro i j hi hj
    exact one_pair_forces_zone_indiscrete hA (ha.trans hb.symm) habNe hab i j
      (hi.trans ha.symm) (hj.trans ha.symm)
  · right
    intro i j hi hj hij
    by_contra hne
    exact hpair ⟨i, j, hi, hj, hne, hij⟩

/-! ## Three-bit classification of the induced relation -/

/-- `Resolved A z` means the stable algebra separates every two vertices in zone `z`. -/
def Resolved (A : Subalgebra ℚ Functions) (z : Fin 3) : Prop :=
  ∀ i j : Vertex, zoneOf i = z → zoneOf j = z → Insep A i j → i = j

/-- Relation determined by three booleans: resolved zones use equality; unresolved zones use the
whole zone relation. -/
def BitRelation (r : Fin 3 → Prop) (i j : Vertex) : Prop :=
  zoneOf i = zoneOf j ∧ (r (zoneOf i) → i = j)

/-- Every stable degree-containing algebra induces exactly its three-bit relation. -/
theorem insep_iff_bitRelation {A : Subalgebra ℚ Functions} (hA : IsStable A)
    (hdeg : degreeQ ∈ A) (i j : Vertex) :
    Insep A i j ↔ BitRelation (Resolved A) i j := by
  constructor
  · intro hij
    refine ⟨insep_imp_same_zone hdeg hij, ?_⟩
    intro hresolved
    exact hresolved i j rfl (insep_imp_same_zone hdeg hij) hij
  · rintro ⟨hzone, hresolve⟩
    by_cases hres : Resolved A (zoneOf i)
    · rw [hresolve hres]
      exact insep_refl A j
    · rcases within_zone_dichotomy hA (zoneOf i) with hall | hsep
      · exact hall i j rfl hzone
      · exact False.elim (hres hsep)

/-- **Lean capstone.** Setwise stability plus the degree observable exhausts the induced relations
by three booleans. This is the theorem-grade content behind the independently computed Boolean
`2^3` lattice; no universality over other carriers is claimed. -/
theorem stable_degree_relation_classification :
    ∀ A : Subalgebra ℚ Functions, IsStable A → degreeQ ∈ A →
      ∃ r : Fin 3 → Prop, ∀ i j : Vertex, Insep A i j ↔ BitRelation r i j := by
  intro A hA hdeg
  exact ⟨Resolved A, insep_iff_bitRelation hA hdeg⟩

/-- The killed uniqueness reading has a precise logical boundary: the capstone classifies a
three-bit family; it does not assert the family has one member. -/
theorem classification_has_eight_boolean_addresses : Fintype.card (Fin 3 → Bool) = 8 := by
  decide

end D0.Foundation.InvariantStableSubalgebraLattice
