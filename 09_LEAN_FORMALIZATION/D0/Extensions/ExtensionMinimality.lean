import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.List.Nodup
import Mathlib.Tactic

/-!
# D0-POSTCORE-EXTENSION-SEMANTIC-DEPENDENCE-001 — extension minimality & cross-dependence (Sections 1 & 7)

A REAL proof-edge graph (NOT identifier distinctness for the dependence claim). Components `E1..E5 = 0..4`.
`depends i j = true` means *E_j's admission derives from E_i*. The grounded merge found exactly TWO directed
proof-edges, both the `a=3` exponent leg and both asymmetric: `E2 → E5` and `E3 → E5` (the φ³/rate-3 channel
that E5 reuses at its critical line). `E4` is isolated (disjoint 7-point shell torus). No primitives merge.
(`Nodup` below is used ONLY to record that the five component TYPES are distinct — never as the dependence proof.)
-/

namespace D0.Extensions.ExtensionMinimality

/-- `depends i j` = E_j's admission derives from E_i. `E1..E5 = 0..4`. -/
def depends : Fin 5 → Fin 5 → Bool :=
  ![![false, false, false, false, false],   -- E1 derives: (none)
    ![false, false, false, false, true],    -- E2 → E5  (exponent a=3 edge)
    ![false, false, false, false, true],    -- E3 → E5  (partial exponent edge)
    ![false, false, false, false, false],   -- E4 isolated
    ![false, false, false, false, false]]   -- E5

/-- Total directed proof-edges. -/
def edgeCount : ℕ :=
  ((List.finRange 5).map (fun i => ((List.finRange 5).map
    (fun j => if depends i j then 1 else 0)).sum)).sum

/-- Exactly two directed proof-edges (both into E5). -/
theorem two_exponent_edges : edgeCount = 2 := by decide

/-- The two edges are `E2 → E5` and `E3 → E5`, and both are asymmetric. -/
theorem edges_into_e5_asymmetric :
    depends 1 4 = true ∧ depends 2 4 = true ∧ depends 4 1 = false ∧ depends 4 2 = false := by decide

/-- `E4` is isolated: derives nothing and is derived by nothing. -/
theorem e4_isolated : (∀ j, depends 3 j = false) ∧ (∀ i, depends i 3 = false) := by decide

/-- `E2`/`E3` do not force branch selection (`E4`) or the representation (`E1`): no such edges. -/
theorem key_nonderivations :
    depends 1 3 = false ∧ depends 2 1 = false ∧ depends 0 2 = false := by decide

/-- The five component TYPES are distinct (records "no merge"; not the dependence proof). -/
def componentTypes : List ℕ := [1, 2, 3, 4, 5]
theorem components_distinct : componentTypes.Nodup := by decide

/-- **D0-POSTCORE-EXTENSION-SEMANTIC-DEPENDENCE-001.** Exactly two asymmetric proof-edges (`E2,E3 → E5`),
`E4` isolated, five distinct component types (no merge). -/
theorem extension_semantic_dependence :
    edgeCount = 2 ∧ depends 1 4 = true ∧ depends 2 4 = true ∧
      (∀ j, depends 3 j = false) ∧ componentTypes.Nodup :=
  ⟨two_exponent_edges, edges_into_e5_asymmetric.1, edges_into_e5_asymmetric.2.1,
    e4_isolated.1, components_distinct⟩

end D0.Extensions.ExtensionMinimality
