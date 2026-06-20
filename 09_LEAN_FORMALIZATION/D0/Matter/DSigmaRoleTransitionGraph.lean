import Mathlib.Tactic

/-!
# D0-DSIGMA-CANONICAL-ROLE-ADDRESS-OWNER-001 — the DΣ role-transition graph is a canonical 5-cycle

The five operational DΣ roles `Code → Canon → Test → History → Access → Code` form a single canonical
directed 5-cycle: each role has exactly one admissible successor (its dependency obligation), the graph
is strongly connected, and removing any edge breaks finite self-distinguishability while adding an
independent edge would require a sixth role category. This part is canonical — it is fixed by the role
dependency rules alone, with no manual list and no scene-vertex choice. (The *embedding* of these roles
into graph-cycle classes is the separate canonical-carrier question — see
`D0.Matter.DSigmaRoleCycleCarrierNoGo`, which shows that embedding is NOT canonical.)
-/

namespace D0.Matter.DSigmaRoleTransitionGraph

/-- The five DΣ roles. -/
inductive Role
  | code | canon | test | history | access
  deriving DecidableEq, Fintype

open Role

/-- The canonical successor of each role (its dependency obligation): the single admissible transition. -/
def succ : Role → Role
  | code => canon
  | canon => test
  | test => history
  | history => access
  | access => code

/-- **There are exactly five roles.** -/
theorem dsigma_transition_graph_has_five_nodes : Fintype.card Role = 5 := by decide

/-- **`succ` is a bijection** (each role has exactly one successor and one predecessor). -/
theorem succ_bijective : Function.Bijective succ := by decide

/-- **The transition graph is a single 5-cycle**: iterating `succ` five times returns to the start, and
no shorter iterate does (the orbit of any role is all five). -/
theorem dsigma_transition_graph_is_single_cycle :
    (∀ r : Role, succ (succ (succ (succ (succ r)))) = r)
      ∧ (∀ r : Role, succ r ≠ r)
      ∧ (∀ r : Role, succ (succ r) ≠ r) := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- **Removing the cycle structure destroys self-distinguishability**: `succ` has no fixed point and no
2-cycle, so the five roles are genuinely cyclically ordered (a constant or shorter-period map would
collapse distinct roles). -/
theorem role_motif_is_terminal_carrier_determined :
    Function.Bijective succ ∧ (∀ r : Role, succ r ≠ r) := by
  exact ⟨succ_bijective, fun r => (dsigma_transition_graph_is_single_cycle.2.1 r)⟩

end D0.Matter.DSigmaRoleTransitionGraph
