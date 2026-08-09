import Mathlib.Tactic
import D0.Claims.Signature31Split

/-!
# D0-SCENE-CHROMATIC-THREE-NOGO-001 — the colouring route forces 3, not 4, and the scene has no `K₄`

## The claim this kills

BOOK_07 §07.21.4C offers a **second, independent forcing** of the ABCD capacity `4`:

> "the boundary automaton must assign each cell a phase identifier such that no two adjacent cells
> share a state … by the Four-Colour Theorem any contiguous planar map needs *exactly four* distinct
> identifiers … The four terminal detector roles `ABCD` are precisely that minimal four-colouring."

Two things are wrong with it, and the second is fatal on the corpus's own object.

**(1) Sufficiency read as necessity.** The Four-Colour Theorem says four colours *suffice* for every
planar map. It never says four are *needed* — most planar maps need fewer, and a map needs four only
when it contains a non-3-colourable configuration. "Any contiguous planar map needs exactly four" is
false as written. The section already records that no certificate exists for this route.

**(2) On the only graph the corpus owns, the colouring argument returns 3.** This module proves it.
The scene `K(9,11,13)` is complete tripartite, so:

* the zone map is a proper colouring with three colours — three **suffice**;
* a triangle exists (one vertex per zone) — three are **necessary**;
* and, decisively, the scene contains **no `K₄` at all**: any four vertices put two in the same zone
  by pigeonhole, and same-zone vertices are non-adjacent.

So the aliasing/no-adjacent-collision requirement, applied to the scene, forces exactly `3` — the
zone count — and cannot reach `4` by any colouring argument, because the obstruction that would make
four necessary provably does not exist here.

## What survives

The ABCD capacity `4` keeps its other owner (the symplectic phase-quotient / min-cut count of
§07.21). What it loses is the *second* route, and with it the multiplicity that made `4` look
antifragile. Restoring a genuine second forcing now requires exhibiting a concrete boundary graph —
distinct from the scene — together with a proof that it is non-3-colourable. Until such a graph is
named, the correct status of the four-colour route is: it forces "four suffice", which forces
nothing.

Honest scope: this is a statement about the scene graph `K(9,11,13)`. It does not by itself refute a
claim about some other, unspecified "boundary graph" — it removes the only concrete object the route
could have been about, and shifts the burden to naming that graph.
-/

namespace D0.Combinatorics

open D0.Claims

/-- Scene adjacency: two vertices are adjacent iff they lie in different zones. -/
def sceneAdj (i j : Fin 33) : Prop := zone31 i ≠ zone31 j

instance : DecidableRel sceneAdj := fun i j => by
  unfold sceneAdj; infer_instance

/-- **Three colours suffice.** The zone map is a proper colouring: adjacent vertices get different
colours, by the definition of adjacency. -/
theorem zone_is_proper_colouring (i j : Fin 33) (h : sceneAdj i j) : zone31 i ≠ zone31 j := h

/-- **Three colours are necessary.** A triangle exists — one vertex from each zone, pairwise
adjacent — so no proper colouring uses fewer than three. -/
theorem triangle_exists :
    sceneAdj 0 9 ∧ sceneAdj 9 20 ∧ sceneAdj 0 20 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- **Pigeonhole on the zones.** Among any four vertices two share a zone. -/
theorem two_share_a_zone (a b c d : Fin 33) :
    zone31 a = zone31 b ∨ zone31 a = zone31 c ∨ zone31 a = zone31 d ∨
    zone31 b = zone31 c ∨ zone31 b = zone31 d ∨ zone31 c = zone31 d := by
  by_contra h
  push Not at h
  obtain ⟨hab, hac, had, hbc, hbd, hcd⟩ := h
  -- four values in `Fin 3`, pairwise distinct — impossible
  have : ∀ x : Fin 3, x = 0 ∨ x = 1 ∨ x = 2 := by decide
  rcases this (zone31 a) with ha | ha | ha <;>
  rcases this (zone31 b) with hb | hb | hb <;>
  rcases this (zone31 c) with hc | hc | hc <;>
  rcases this (zone31 d) with hd | hd | hd <;>
  simp_all

/-- **The scene has no `K₄`.** Four pairwise-adjacent vertices would need four pairwise-distinct
zones, and there are only three. This is the configuration whose existence is what would make four
colours *necessary* — it is absent. -/
theorem no_K4 (a b c d : Fin 33) :
    ¬(sceneAdj a b ∧ sceneAdj a c ∧ sceneAdj a d ∧
      sceneAdj b c ∧ sceneAdj b d ∧ sceneAdj c d) := by
  rintro ⟨hab, hac, had, hbc, hbd, hcd⟩
  unfold sceneAdj at hab hac had hbc hbd hcd
  rcases two_share_a_zone a b c d with h | h | h | h | h | h <;> simp_all

/-- **D0-SCENE-CHROMATIC-THREE-NOGO-001.** On the scene the colouring requirement forces exactly
three identifiers: the zone map is proper (3 suffice), a triangle exists (3 are necessary), and no
`K₄` exists (so nothing forces a fourth). The four-colour route to the ABCD capacity `4` therefore
does not apply to `K(9,11,13)`, and cannot be a second independent forcing of `4` without first
naming a different, non-3-colourable boundary graph. -/
theorem scene_chromatic_three_nogo :
    (∀ i j : Fin 33, sceneAdj i j → zone31 i ≠ zone31 j) ∧
    (sceneAdj 0 9 ∧ sceneAdj 9 20 ∧ sceneAdj 0 20) ∧
    (∀ a b c d : Fin 33,
      ¬(sceneAdj a b ∧ sceneAdj a c ∧ sceneAdj a d ∧
        sceneAdj b c ∧ sceneAdj b d ∧ sceneAdj c d)) :=
  ⟨zone_is_proper_colouring, triangle_exists, no_K4⟩

end D0.Combinatorics
