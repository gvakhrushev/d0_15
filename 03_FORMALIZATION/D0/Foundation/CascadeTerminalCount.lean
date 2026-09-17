import Mathlib.Tactic
import D0.Foundation.CascadeFloorShellClosure

/-!
# The terminal count at proxy grade: two interior layers + forced closure = exactly three

**Target: `D0-CASCADE-INSUFFICIENCY-CHAIN-001`** (umbrella). The cascade's terminal prose
step is `three insufficiencies = three zones ⇒ carrier K(9,11,13)`. THREE routes to this
step are RECORDED DEAD and are not re-attacked here — each obituary is named and the present
route differentiated:

1. `SceneCountRouteNoGo.propositional_route_caps_at_two` /
   `no_three_pairwise_inequivalent_props`: propositions up to equivalence cap at TWO — the
   propositional route cannot even state a three-way count. THIS route's count lives on
   SET CARDINALITY of radii in `ℚ`, not on propositions.
2. `DiscriminationRetyping.zoneAssignment_is_uninhabitable`: the pair-indexed typing is
   provably empty. No `ZoneAssignment` occurs here.
3. `DiscriminationKinds` (`Nonempty (ZoneAssignmentK S) ↔ 3 ≤ S.zoneCount`): the
   sort-indexed route is CIRCULAR — its hypothesis is its conclusion. THIS route is
   non-circular by construction: the INPUTS are the two interior radii (the defect layer and
   the circulation core, §03.23.5's own identification) and the reflection move; the number
   THREE enters as the proved cardinality of the exhibited-and-proved-least completion —
   no hypothesis of shape `3 ≤ _` occurs anywhere.

**What is proved (all at the reflection-proxy grade of
`D0-CASCADE-FLOOR-SHELL-CLOSURE-001`, on the owned shell geometry, every admissible
parameter):**

* the interior pair has exactly TWO elements (`interior_card_two`);
* any reflection-closed superset of the interior pair must contain the outer radius
  (`closed_superset_contains_outer`) — the closure FORCES a third element;
* the three-shell set is the LEAST reflection-closed superset of the interior pair
  (`three_shells_least_closed`, with closedness owned at `shells_reflection_closed`);
* the least completion is EXHIBITED as the triple, PROVED least
  (`three_shells_least_closed`) and closed (`shells_reflection_closed`, cited), and its
  cardinality is proved exactly THREE (`closure_card_three`) — `ρ` swaps inner↔outer and
  fixes the core, so no fourth element is ever generated;
* the three-element carrier is the OWNED zone-attachment carrier — the carrier count is
  cited, not re-proved: `D0-TORUS-CORE13-GEOMETRY-001` owns `torus_shell_card_eq_three`,
  and the zone sizes 9/11/13 ride the owned attachment (`carrier_card_three`).

**Honest scope (pre-registered).**
1. This carries the COUNT half of the terminal step, at reflection-proxy grade: two interior
   insufficiency layers + the forced closure = exactly three shells. The zone SIZES
   {9,11,13} are NOT derived here — the multiplicative-pair owner is
   `D0-ZONE-COUNT-MULTIPLICATIVE-001`, and the attachment's `zoneSize` is definitional in
   the owned geometry module; both cited.
2. The identification "two interior layers = the defect and circulation insufficiencies" is
   §03.23.5's own prose (FORCED status), carried at prose grade — same grade as the shell
   floor's fourth link.
3. The prose phrase "THREE insufficiencies" is not re-interpreted: at proxy grade the
   arithmetic carried is `2 + 1` — two interior layers plus the one closure-forced layer;
   whether that matches the prose's own enumeration of insufficiencies stays at prose grade.
4. THE TYPED SEAM IS NOT DISCHARGED: `SceneCountReduction`'s two interpretation records
   (`CascadeCountInterpretation`, `NoExtensionCountInterpretation` — the `Fin 3 ↪ zoneCount`
   maps) remain UNCONSTRUCTED; this count lives on the radius/shell carrier, not on
   `SceneCandidate.zoneCount`, so `D0-SCENE-COUNT-REDUCTION-001` stays PROOF-TARGET.
5. The umbrella stays OPEN: the topological/2-cell reading of closure⇒shell and the full
   chain assembly remain; this module adds the count leg the three dead routes could not
   reach.
-/

namespace D0.Foundation

open D0.Geometry

/-- The interior (defect + circulation) pair has exactly two elements, for every admissible
parameter — the strict radial order separates them. -/
theorem interior_card_two (T : TorusParameter) :
    ({T.inner, T.core} : Finset ℚ).card = 2 := by
  have h := (torusShell_radius_strictMono T).1
  rw [torusShell_radius_inner, torusShell_radius_core] at h
  rw [Finset.card_eq_two]
  exact ⟨T.inner, T.core, ne_of_lt h, rfl⟩

/-- **The closure forces a third element**: any reflection-closed superset of the interior
pair contains the outer radius. -/
theorem closed_superset_contains_outer (T : TorusParameter) (S : Set ℚ)
    (hsub : ({T.inner, T.core} : Set ℚ) ⊆ S)
    (hclosed : ∀ x ∈ S, shellReflection T x ∈ S) :
    T.outer ∈ S := by
  have hi : T.inner ∈ S := hsub (by simp)
  have hstep := hclosed T.inner hi
  have heq : shellReflection T T.inner = T.outer := by
    show (2 : ℚ) * T.core - T.inner = T.outer
    show (2 : ℚ) * ((T.a + 1) / 2) - 1 = T.a
    ring
  rwa [heq] at hstep

/-- **The three-shell set is the least reflection-closed completion of the interior pair.**
(Its own closedness is owned at `shells_reflection_closed`.) -/
theorem three_shells_least_closed (T : TorusParameter) (S : Set ℚ)
    (hsub : ({T.inner, T.core} : Set ℚ) ⊆ S)
    (hclosed : ∀ x ∈ S, shellReflection T x ∈ S) :
    ({T.inner, T.core, T.outer} : Set ℚ) ⊆ S := by
  intro x hx
  rcases hx with h | h | h
  · exact h ▸ hsub (by simp)
  · exact h ▸ hsub (by simp)
  · exact h ▸ closed_superset_contains_outer T S hsub hclosed

/-- **The completion has exactly three elements** — the orbit closes at three, for every
admissible parameter. -/
theorem closure_card_three (T : TorusParameter) :
    ({T.inner, T.core, T.outer} : Finset ℚ).card = 3 := by
  have h1 := (torusShell_radius_strictMono T).1
  have h2 := (torusShell_radius_strictMono T).2
  rw [torusShell_radius_inner, torusShell_radius_core] at h1
  rw [torusShell_radius_core, torusShell_radius_outer] at h2
  have h13 : T.inner < T.outer := lt_trans h1 h2
  rw [Finset.card_eq_three]
  exact ⟨T.inner, T.core, T.outer, ne_of_lt h1, ne_of_lt h13, ne_of_lt h2, rfl⟩

/-- The three-element completion carrier is the OWNED zone-attachment carrier. The carrier
count is NOT new here: `Fintype.card TorusShell = 3` is owned at
`D0-TORUS-CORE13-GEOMETRY-001` (`D0.Geometry.torus_shell_card_eq_three`) and is CITED, with
the zone sizes 9/11/13 read off the owned attachment (`torusShellEquivShell3`,
`TorusShell.zoneSize`). -/
theorem carrier_card_three :
    Fintype.card TorusShell = 3
      ∧ TorusShell.zoneSize .innerD9 = 9
      ∧ TorusShell.zoneSize .coreD11 = 11
      ∧ TorusShell.zoneSize .outerD13 = 13 :=
  ⟨torus_shell_card_eq_three, rfl, rfl, rfl⟩

/-- **The terminal count at proxy grade** (assembly): two interior layers, the closure
forces the third, the least completion has exactly three elements and is itself closed, and
the three-element carrier is the owned zone-attachment carrier. The zone sizes and the
topological closure reading remain with their own owners; the three dead count-routes are
untouched (different carriers, see module docstring). -/
theorem cascade_terminal_count (T : TorusParameter) :
    ({T.inner, T.core} : Finset ℚ).card = 2
      ∧ (∀ S : Set ℚ, ({T.inner, T.core} : Set ℚ) ⊆ S →
          (∀ x ∈ S, shellReflection T x ∈ S) →
          ({T.inner, T.core, T.outer} : Set ℚ) ⊆ S)
      ∧ ({T.inner, T.core, T.outer} : Finset ℚ).card = 3
      ∧ (∀ x ∈ ({T.inner, T.core, T.outer} : Set ℚ),
          shellReflection T x ∈ ({T.inner, T.core, T.outer} : Set ℚ))
      ∧ Fintype.card TorusShell = 3 :=
  ⟨interior_card_two T, three_shells_least_closed T, closure_card_three T,
    shells_reflection_closed T, carrier_card_three.1⟩

end D0.Foundation
