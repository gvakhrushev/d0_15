import Mathlib.Tactic
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.GroupTheory.SpecificGroups.Quaternion

/-!
# D0-CASCADE-FLOOR-ORDER-MEMORY-001 — the torus floor fails order-memory (cascade floor 5→6)

First formalized floor of `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (BOOK_01 §01.6.1c). The cascade's
content is in the **insufficiency**: each level exists because the one below it *provably fails* a
named distinguishability obligation. This module carries one such step end to end, in the shape the
chain claim fixes:

```
Floor        the two-loop memory carrier: π₁(T²) = ℤ × ℤ
Obligation   ORDER MEMORY — the record must distinguish "write then read" from "read then write"
insufficient ¬ OrderEncoded (ℤ × ℤ)          -- the load-bearing lemma
control      OrderEncoded (Equiv.Perm (Fin 3))  -- the obligation IS satisfiable, so not vacuous
minimal      any fix must be non-commutative; commutativity alone already decides the failure
```

The step being formalized (BOOK_03 §03.23.4, BOOK_01 §01.6.1c): *"on a pure torus the fundamental
group `π₁(T²) = ℤ²` is abelian — any two base loops commute. Then 'Write then Read' and 'Read then
Write' lie in the same path class: the order of the two operations is not encoded."* Hence a defect
is forced, as the minimal injection of non-commutativity.

**Why the control is the point.** `insufficient` alone could be vacuous — an obligation no structure
whatever satisfies forces nothing, since the next floor would not satisfy it either. Exhibiting a
group in which order *is* encoded shows the obligation is a real requirement that some structures
meet and the torus does not. This is `check_cert_can_fail` discipline applied to the spine rather
than to a certificate, and it is what makes a floor a theorem instead of a definition.

Honest scope: this owns the *group-theoretic* content of the floor — that an abelian carrier cannot
encode operation order and that non-abelian carriers can. The identification of "write/read
composition" with the group operation, and of "one defect" with the minimal non-commutative
injection, are the reading, owned by BOOK_03 §03.23.4.
-/

namespace D0.Foundation

/-- **The obligation.** A carrier encodes operation order when some pair of operations composes
differently in the two orders — otherwise the record of `a then b` is literally the record of
`b then a`, and the order left no trace. -/
def OrderEncoded (G : Type*) [Mul G] : Prop := ∃ a b : G, a * b ≠ b * a

/-- **The floor fails, for every abelian carrier.** Stated at full generality, so the failure is a
property of commutativity itself and not an accident of `ℤ × ℤ`. -/
theorem abelian_not_orderEncoded (G : Type*) [CommMonoid G] : ¬ OrderEncoded G := by
  rintro ⟨a, b, hab⟩
  exact hab (mul_comm a b)

/-- **`insufficient` — the two-loop torus carrier cannot encode order.** `π₁(T²) = ℤ × ℤ` is
abelian, so "write then read" and "read then write" land in the same class. -/
theorem torus_insufficient : ¬ OrderEncoded (Multiplicative (ℤ × ℤ)) :=
  abelian_not_orderEncoded _

/-- Two permutations of `Fin 3` that do not commute: the transpositions `(0 1)` and `(1 2)`. -/
def s01 : Equiv.Perm (Fin 3) := Equiv.swap 0 1
def s12 : Equiv.Perm (Fin 3) := Equiv.swap 1 2

/-- **`control` — the obligation is satisfiable, so the insufficiency is not vacuous.** In the
symmetric group on three letters the two transpositions compose differently in the two orders, so
order *is* recoverable from the record there. -/
theorem control_orderEncoded : OrderEncoded (Equiv.Perm (Fin 3)) := by
  refine ⟨s01, s12, ?_⟩
  unfold s01 s12
  decide

/-- **`control` (second witness, the corpus's own role algebra).** `Q₈` also encodes order —
`i * j ≠ j * i` — so the minimal non-commutative repair is realized by the object BOOK_01 already
forces as the role group, not by an arbitrary group. -/
theorem control_quaternion_orderEncoded : OrderEncoded (QuaternionGroup 2) := by
  refine ⟨QuaternionGroup.a 1, QuaternionGroup.xa 0, ?_⟩
  decide

/-- **`minimal` — commutativity alone decides the floor.** Any repair of the torus floor must be
non-commutative: a commutative carrier fails the obligation whatever else is added to it, so the
minimal admissible fix is exactly an injection of non-commutativity. -/
theorem repair_must_be_noncommutative (G : Type*) [CommMonoid G] :
    ¬ OrderEncoded G := abelian_not_orderEncoded G

/-- **D0-CASCADE-FLOOR-ORDER-MEMORY-001.** The torus floor of the cascade, complete: the obligation
fails on every abelian carrier and in particular on `π₁(T²) = ℤ × ℤ`; it is satisfiable, witnessed
twice (`S₃` and `Q₈`), so the failure is a real obstruction and not a vacuous demand; and any repair
must be non-commutative. This is the first floor of `D0-CASCADE-INSUFFICIENCY-CHAIN-001` carried in
the shape the chain claim fixes. -/
theorem cascade_floor_order_memory :
    (¬ OrderEncoded (Multiplicative (ℤ × ℤ))) ∧
    OrderEncoded (Equiv.Perm (Fin 3)) ∧
    OrderEncoded (QuaternionGroup 2) ∧
    (∀ G : Type, ∀ _ : CommMonoid G, ¬ OrderEncoded G) :=
  ⟨torus_insufficient, control_orderEncoded, control_quaternion_orderEncoded,
   fun G _ => abelian_not_orderEncoded G⟩

end D0.Foundation
