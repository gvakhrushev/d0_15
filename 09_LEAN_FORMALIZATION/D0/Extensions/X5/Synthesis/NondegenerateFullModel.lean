import D0.Extensions.X5.Soundness.NondegenerateCompatibility
import D0.Extensions.FivePrimitiveSemanticDependence
import Mathlib.Tactic

/-!
# D0-X5-NONDEGENERATE-FULL-001 — nondegenerate joint model + dependency matrix (Section 8)

The realized joint model is nondegenerate (every slot carries a base→carrier overlap map — not direct-sum
padding), and the X5 dependency matrix has exactly one real construction edge `P1 → P2` (the coordinate functor
consumes the pressure-energy sector), `G,H,L` independent, no merge.
-/

namespace D0.Extensions.X5.Synthesis

open D0.Extensions.X5.Soundness

/-- **D0-X5-NONDEGENERATE-FULL-001.** Nondegenerate joint model (base overlaps on every slot) + one real
dependency edge `P1 → P2`, asymmetric. -/
theorem nondegenerate_full_model :
    realizedJoint.nondegenerate ∧ ¬ paddedJoint.nondegenerate ∧
      D0.Extensions.FivePrimitiveSemanticDependence.edgeCount = 1 ∧
      D0.Extensions.FivePrimitiveSemanticDependence.dep 3 4 = true ∧
      D0.Extensions.FivePrimitiveSemanticDependence.dep 4 3 = false :=
  ⟨realized_nondegenerate, padded_degenerate,
    D0.Extensions.FivePrimitiveSemanticDependence.one_edge,
    D0.Extensions.FivePrimitiveSemanticDependence.p1_p2_asymmetric.1,
    D0.Extensions.FivePrimitiveSemanticDependence.p1_p2_asymmetric.2⟩

end D0.Extensions.X5.Synthesis
