import Mathlib.Tactic
import D0.Foundation.CascadeChain
import D0.Foundation.CascadeFloorOrientationParity
import D0.Foundation.CascadeInterlockScale
import D0.Foundation.CascadeFloorDefectClosure
import D0.Foundation.CascadeFloorShellClosure
import D0.Foundation.CascadeTerminalCount

/-!
# The carried cascade, assembled: seven floors, four links, the count leg — one theorem

**Target: `D0-CASCADE-INSUFFICIENCY-CHAIN-001`** (umbrella). Its registered FORMALIZATION
SHAPE asks for "the unifying 'each floor forced by the insufficiency of the previous'
statement". The full statement remains OPEN (the floor↔prose identifications carry their
registered grades; the chain ORDER is the scaffold's; the topological closure reading and
the typed count seam remain with their owners). What EXISTS after the 2026-08-09 session is
substantial and scattered across six modules; this module assembles ALL carried content
into one citable theorem — the umbrella's Lean spine.

**Assembled (everything cited, nothing re-proved):**
* the extended floor list — the scaffold's four carried floors plus the two new floors
  (`stepDefectClosure`, `stepShellClosure`) — with EVERY floor genuine
  (`extended_floors_are_genuine`, via the scaffold's own `step_discriminates`);
* the four links: 4→5→5→6 (scaffold), 5→6→6→7 (scale, shared-object),
  order→defect-closure (shared-object), closure→shell (prose-anchored, its registered
  grade); each cited from its minted module;
* the count leg (`cascade_terminal_count`, every admissible parameter);
* the address-ladder floor as a separate conjunct (`stepOrientationParity` genuine —
  outside the chain order, cited at its own row's grade).

The orientation-parity floor (`D0-CASCADE-FLOOR-ORIENTATION-PARITY-001`,
`stepOrientationParity` — it IS a `CascadeStep`, the registry's "fifth registered floor")
is anchored at the ADDRESS-LADDER prose, not a step of the one-liner chain, so it has no
position in the ORDERED list; it is assembled as a separate seventh conjunct
(`stepOrientationParity_genuine` grade), not inserted into the chain order.

**Honest scope.** This is an ASSEMBLY of carried content — a conjunction of minted
theorems, each at its own registered grade (the prose-anchored fourth link stays
prose-anchored; the proxy grades stay proxy; the seam of `D0-SCENE-COUNT-REDUCTION-001`
stays unconstructed; the umbrella stays OPEN). Its value is citability: one theorem the
umbrella row can point to as "the carried cascade", replacing six scattered pointers.
No new mathematics is claimed; the assembly itself (the conjunction being well-formed and
provable from the six modules with clean axioms) is the content.
-/

namespace D0.Foundation

open D0.Geometry

/-- The extended carried-floor list: the scaffold's four floors plus the two floors added
2026-08-09 (defect-closure, shell-closure), in the scaffold's order with the new floors
inserted at their prose positions (defect after order memory; shell after closure; link 2's
5→6→6→7 adjacency stays owned at the scaffold's own `carriedFloors`, where order-memory and
scale ARE adjacent). -/
def carriedFloorsExtended : List CascadeStep :=
  [stepComparison, stepOneLoop, stepOrderMemory, stepDefectClosure,
   stepShellClosure, stepScaleRatio]

/-- **Every carried floor is genuine** — the obligation below and above never coincide, for
all six floors, by the scaffold's own discriminator. -/
theorem extended_floors_are_genuine :
    ∀ s ∈ carriedFloorsExtended, ¬ (s.ObligationBelow ↔ s.ObligationAbove) :=
  fun s _ => step_discriminates s

/-- **The carried cascade, in one theorem.** Six genuine chain floors + the address-ladder
floor as a separate conjunct; the four links (each at its registered grade); the terminal
count leg. Every conjunct is cited from its minted module; the umbrella stays OPEN. -/
theorem cascade_carried_assembly :
    (∀ s ∈ carriedFloorsExtended, ¬ (s.ObligationBelow ↔ s.ObligationAbove))
      ∧ ((runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0))
          ∧ ¬ OrderEncoded (Multiplicative (ℤ × ℤ)))
      ∧ (OrderEncoded (Equiv.Perm (Fin 3))
          ∧ OrderEncoded (QuaternionGroup 2)
          ∧ (∀ r : ℝ, carrierRealizedRatio (Equiv.Perm (Fin 3)) r → ¬ NonCaptured r)
          ∧ (∀ r : ℝ, carrierRealizedRatio (QuaternionGroup 2) r → ¬ NonCaptured r))
      ∧ (OrderEncoded (Equiv.Perm (Fin 3))
          ∧ (∃ a b : Equiv.Perm (Fin 3), commDefect a b ≠ 1)
          ∧ ¬ (∀ g a b : Equiv.Perm (Fin 3), g * commDefect a b * g⁻¹ = commDefect a b)
          ∧ (∀ g x : Equiv.Perm (Fin 3),
              ConjClasses.mk (g * x * g⁻¹) = ConjClasses.mk x))
      ∧ ((¬ ∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core} : Set ℚ),
            shellReflection T x ∈ ({T.inner, T.core} : Set ℚ))
          ∧ (∀ T : TorusParameter, ∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
              shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ))
          ∧ (∀ x : ℝ, 0 < x → (x = 1 + 1 / x ↔ x = Real.goldenRatio))
          ∧ NonCaptured ((1 + Real.sqrt 5) / 2))
      ∧ (∀ T : TorusParameter,
          ({T.inner, T.core} : Finset ℚ).card = 2
            ∧ (∀ S : Set ℚ, ({T.inner, T.core} : Set ℚ) ⊆ S →
                (∀ x ∈ S, shellReflection T x ∈ S) →
                ({T.inner, T.core, T.outer} : Set ℚ) ⊆ S)
            ∧ ({T.inner, T.core, T.outer} : Finset ℚ).card = 3
            ∧ (∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
                shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ))
            ∧ Fintype.card TorusShell = 3)
      ∧ ¬ (CascadeFloorOrientationParity.stepOrientationParity.ObligationBelow ↔ CascadeFloorOrientationParity.stepOrientationParity.ObligationAbove) :=
  ⟨extended_floors_are_genuine,
    chain_linked_four_five_to_five_six,
    chain_linked_five_six_to_six_seven,
    chain_linked_order_to_defect_closure,
    chain_linked_closure_to_shell,
    cascade_terminal_count,
    step_discriminates CascadeFloorOrientationParity.stepOrientationParity⟩

end D0.Foundation
