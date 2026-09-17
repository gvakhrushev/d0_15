import D0.Extensions.PrimitiveMinimalityAfterSelfReading
import Mathlib.Tactic

/-!
# D0-RAW-PRIMITIVE-MINIMALITY-001 — Track III

Confirmed from the raw functor: `PRIM-CANONICAL-SELF-READING-FUNCTOR` is the CONJUNCTION of the raw-derived
forced skeleton `S₀` and the four semantically-independent primitives — NOT a merge. Decisive: the proof-edge
graph among the four combinatorial frontiers `E1–E4` has zero internal edges (the only two edges target the
separate analytic frontier `E5`).
-/

namespace D0.SelfReading.PrimitiveMinimalityFromRawFunctor

/-- **Track III.** conjunction-of-independent: no internal proof-edge among `E1–E4`; exactly 2 edges (to `E5`). -/
theorem raw_primitive_conjunction_of_independent :
    (∀ i j : Fin 5, i.val < 4 → j.val < 4 → D0.Extensions.ExtensionMinimality.depends i j = false) ∧
      D0.Extensions.ExtensionMinimality.edgeCount = 2 :=
  D0.Extensions.PrimitiveMinimalityAfterSelfReading.primitive_minimality_conjunction_of_independent

end D0.SelfReading.PrimitiveMinimalityFromRawFunctor
