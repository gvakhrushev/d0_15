import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic

/-!
# D0-FIVE-PRIMITIVE-DEPENDENCE-001 — cross-lane minimality

Five primitives indexed `G,H,L,P1,P2 = 0..4`. `dep i j = true` means primitive `j`'s construction requires
primitive `i`. The only real edge is `P1 → P2`: the coordinate functor (P2) requires the pressure-energy
sector (P1) as input. All other pairs are non-derivation (disjoint carriers / typed-distinct operators). No
merge: `P1, P2` do not fuse (P2 needs P1, not vice versa — asymmetric).
-/

namespace D0.Extensions.FivePrimitiveSemanticDependence

/-- `dep i j` = primitive `j` requires primitive `i`. `G,H,L,P1,P2 = 0..4`. -/
def dep : Fin 5 → Fin 5 → Bool :=
  ![![false, false, false, false, false],
    ![false, false, false, false, false],
    ![false, false, false, false, false],
    ![false, false, false, false, true],
    ![false, false, false, false, false]]

def edgeCount : ℕ :=
  ((List.finRange 5).map (fun i => ((List.finRange 5).map (fun j => if dep i j then 1 else 0)).sum)).sum

theorem one_edge : edgeCount = 1 := by decide
theorem p1_p2_asymmetric : dep 3 4 = true ∧ dep 4 3 = false := by decide
theorem ghl_independent :
    (∀ j, dep 0 j = false) ∧ (∀ j, dep 1 j = false) ∧ (∀ j, dep 2 j = false) ∧
      (∀ i, dep i 0 = false) ∧ (∀ i, dep i 1 = false) ∧ (∀ i, dep i 2 = false) := by decide

/-- **D0-FIVE-PRIMITIVE-DEPENDENCE-001.** One asymmetric edge `P1 → P2`; `G,H,L` fully independent; no merge. -/
theorem five_primitive_dependence :
    edgeCount = 1 ∧ dep 3 4 = true ∧ dep 4 3 = false ∧ (∀ j, dep 0 j = false) :=
  ⟨one_edge, p1_p2_asymmetric.1, p1_p2_asymmetric.2, ghl_independent.1⟩

end D0.Extensions.FivePrimitiveSemanticDependence
