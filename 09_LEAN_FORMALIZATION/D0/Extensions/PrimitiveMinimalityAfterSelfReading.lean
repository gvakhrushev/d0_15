import D0.Extensions.ExtensionMinimality
import Mathlib.Tactic

/-!
# D0-PRIMITIVE-MINIMALITY-AFTER-SELF-READING-001 — Section 4

After Outcome D, `PRIM-CANONICAL-SELF-READING-FUNCTOR` is NOT a genuine single derived object that subsumes
the four disputed primitives: it is the CONJUNCTION of the forced skeleton `S₀` (already owned by R1–R5, not a
new primitive) and four SEMANTICALLY-INDEPENDENT primitives. Decisive: the proof-edge graph among the four
combinatorial frontiers `E1,E2,E3,E4` (indices 0..3) has ZERO internal edges — the only two edges (`E2→E5`,
`E3→E5`) point OUT to the separate analytic frontier `E5` (index 4). So no implication merges any two of the
four; the self-reading functor is their conjunction, not their fusion.
-/

namespace D0.Extensions.PrimitiveMinimalityAfterSelfReading

open D0.Extensions.ExtensionMinimality

/-- The four combinatorial frontiers `E1,E2,E3,E4` as `Fin 5` indices `0..3` (E5 = 4 is the separate analytic layer). -/
def isCombinatorial (i : Fin 5) : Prop := i.val < 4

/-- **No merge among the four**: the proof-edge graph has no edge between any two combinatorial frontiers. -/
theorem no_internal_edge_among_four :
    ∀ i j : Fin 5, i.val < 4 → j.val < 4 → depends i j = false := by decide

/-- Both outgoing edges leave the four (they target `E5`): `E2→E5` and `E3→E5`. -/
theorem only_edges_target_e5 : depends 1 4 = true ∧ depends 2 4 = true ∧ edgeCount = 2 := by
  exact ⟨edges_into_e5_asymmetric.1, edges_into_e5_asymmetric.2.1, two_exponent_edges⟩

/-- **D0-PRIMITIVE-MINIMALITY-AFTER-SELF-READING-001.** conjunction-of-independent: no edge merges any two of
the four combinatorial primitives, and the only dependence (2 edges) targets the separate `E5` layer — so
`PRIM-CANONICAL-SELF-READING-FUNCTOR` decomposes into `S₀` + four independent primitives, not a single merge. -/
theorem primitive_minimality_conjunction_of_independent :
    (∀ i j : Fin 5, i.val < 4 → j.val < 4 → depends i j = false) ∧ edgeCount = 2 :=
  ⟨no_internal_edge_among_four, two_exponent_edges⟩

end D0.Extensions.PrimitiveMinimalityAfterSelfReading
