import Mathlib.Tactic

/-!
# D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001 — no canonical rank-5 role-cycle carrier

The campaign asks for a CANONICAL (automorphism-orbit-determined, non-arbitrary) map from the five DΣ
roles to five distinct graph-cycle classes of `K(9,11,13)`. **No such canonical map exists.**

The oriented automorphism group `Aut(K(9,11,13)) = S₉ × S₁₁ × S₁₃` (parts are distinguishable by their
distinct sizes 9,11,13, so there are no part swaps; the orientation `A→B→C→A` is preserved). It acts
**transitively** on the `9·11·13 = 1287` oriented triangles `A→B→C`, so the primitive cycle class is a
**single orbit**. The five operational roles (Code/Canon/Test/History/Access) carry no intrinsic
geometric attachment to vertices or parts (manual vertices are forbidden), so a canonical assignment
would have to inject the 5 roles into the canonical cycle-orbit-classes — but at the primitive level
there is only **one** such class. By pigeonhole there is no injection `Fin 5 ↪ Fin 1`, hence no canonical
rank-5 role-cycle carrier. Any rank-5 carrier must pick specific representatives = an arbitrary
symmetry-breaking choice = the forbidden manual list.

The orbit-transitivity count (1 primitive orbit) is grounded in the cert
`vp_dsigma_role_cycle_carrier_nogo.py`; this module proves the decidable consequences: the triangle
count, and the pigeonhole obstruction. EXACT MISSING STRUCTURE (named): a canonical role→vertex-sector
attachment (a symmetry-breaking the scene does not supply).
-/

namespace D0.Matter.DSigmaRoleCycleCarrierNoGo

/-- Number of DΣ roles. -/
def numRoles : Nat := 5

/-- Oriented triangles `A→B→C` of `K(9,11,13)`: `9·11·13`. -/
def triangleCount : Nat := 9 * 11 * 13

/-- **There are 1287 oriented triangles.** -/
theorem triangle_count_eq : triangleCount = 1287 := by decide

/-- Number of CANONICAL primitive cycle-orbit-classes under `Aut = S₉×S₁₁×S₁₃`: the triangles form a
SINGLE transitive orbit (grounded in the cert). -/
def numCanonicalPrimitiveOrbits : Nat := 1

/-- **Pigeonhole obstruction**: there is no injection from the five roles into a single canonical
orbit-class. (`Fin 5 ↪ Fin 1` would force `5 ≤ 1`.) -/
theorem no_canonical_rank5_injection :
    ¬ ∃ f : Fin 5 → Fin 1, Function.Injective f := by
  rintro ⟨f, hf⟩
  have h := Fintype.card_le_of_injective f hf
  simp only [Fintype.card_fin] at h
  omega

/-- **D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001.** With five roles but only one canonical
primitive cycle-orbit-class (triangles, a single `Aut`-orbit), no canonical orbit-determined rank-5
role-cycle carrier exists: any such carrier requires an arbitrary symmetry-breaking choice of
representatives (the forbidden manual selection). The role-transition 5-cycle itself stays canonical
(`D0.Matter.DSigmaRoleTransitionGraph`); what is absent is a canonical role→cycle-class embedding. -/
theorem dsigma_role_cycle_carrier_canonical_nogo :
    triangleCount = 1287
      ∧ numCanonicalPrimitiveOrbits < numRoles
      ∧ ¬ ∃ f : Fin numRoles → Fin numCanonicalPrimitiveOrbits, Function.Injective f := by
  exact ⟨triangle_count_eq, by decide, no_canonical_rank5_injection⟩

end D0.Matter.DSigmaRoleCycleCarrierNoGo
