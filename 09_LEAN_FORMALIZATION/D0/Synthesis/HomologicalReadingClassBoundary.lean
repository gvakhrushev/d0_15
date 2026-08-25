import Mathlib.Tactic

/-!
# The homological scene reading is sharply class-relative: an out-of-class rival

`D0.Synthesis.M1HomologicalSceneReading` proves that the coordinate pair

    |V| = 33 ,   β_top = 960

has exactly one preimage in the ordered complete-**tripartite** class, namely
`(p,q,r) = (8,10,12)`, i.e. zone sizes `(9,11,13)`. It states its own scope, verbatim:

> "Honest scope: this is a reconstruction theorem inside the ordered canonical positive
> complete-tripartite class."

Both of its negative controls, however, live *inside* that class: `(7,10,13)` matches the vertex
count alone and `(8,8,15)` matches the Betti number alone. Nothing there exhibits what happens if
the tripartite restriction is dropped — so the scope caveat has no witness, and a reader cannot
tell whether it is a formality or the whole content.

This module supplies the missing witness. For a complete multipartite scene on `k` parts of sizes
`n₁,…,n_k` the two coordinates are

    |V| = ∑ nᵢ ,   β_top = ∏ (nᵢ − 1)

(the second because the `k`-fold join of discrete sets of sizes `nᵢ` is homotopy equivalent to a
wedge of `∏ (nᵢ − 1)` spheres of dimension `k−1`; for `k = 3` this is the `pqr` the source module
computes). Under those coordinates:

* `tripartite_witness` — `(9,11,13)` realises `(33, 960)` with three parts;
* `fourpartite_rival` — `(3,5,9,16)` realises `(33, 960)` with **four**;
* `part_count_not_determined` — hence the pair does not determine the number of parts.

**Consequence, stated precisely.** The reading forces the zone *sizes* given that there are three
zones; it does not force *three*. Removing the class restriction removes the uniqueness, and the
rival is explicit rather than hypothetical. Anyone reading the source theorem as an argument for
the zone count is reading past its class declaration.

There are further rivals — the pair `(33, 960)` is realised at every part count from `3` to `10`;
`(3,5,9,16)` is exhibited here as the smallest departure, and `sixpartite_rival` is included so the
phenomenon is visibly not an accident of `k = 4`.
-/

namespace D0.Synthesis.HomologicalReadingClassBoundary

/-- The vertex coordinate of a multipartite scene: the sum of the zone sizes. -/
def vertexCount (sizes : List ℕ) : ℕ := sizes.sum

/-- The top Betti coordinate of a multipartite scene: `∏ (nᵢ − 1)`. For three parts this is the
`pqr` of `D0.Topology.GenericTripartiteHomology`. -/
def topBetti (sizes : List ℕ) : ℕ := (sizes.map (fun n => n - 1)).prod

/-- The source scene: three parts. -/
def tripartite : List ℕ := [9, 11, 13]

/-- A four-part scene with the same two coordinates. -/
def fourpartite : List ℕ := [3, 5, 9, 16]

/-- A six-part scene with the same two coordinates, to show `k = 4` is not special. -/
def sixpartite : List ℕ := [2, 2, 4, 5, 9, 11]

theorem tripartite_witness :
    vertexCount tripartite = 33 ∧ topBetti tripartite = 960 ∧ tripartite.length = 3 := by
  refine ⟨by decide, by decide, by decide⟩

theorem fourpartite_rival :
    vertexCount fourpartite = 33 ∧ topBetti fourpartite = 960 ∧ fourpartite.length = 4 := by
  refine ⟨by decide, by decide, by decide⟩

theorem sixpartite_rival :
    vertexCount sixpartite = 33 ∧ topBetti sixpartite = 960 ∧ sixpartite.length = 6 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **The two coordinates do not determine the part count.** Two scenes share `(33, 960)` and have
different numbers of parts, so no function of those coordinates can return the part count. -/
theorem part_count_not_determined :
    ∃ s t : List ℕ,
      vertexCount s = vertexCount t ∧ topBetti s = topBetti t ∧ s.length ≠ t.length := by
  refine ⟨tripartite, fourpartite, ?_, ?_, ?_⟩ <;> decide

/-- **The uniqueness is exactly class-relative.** Inside the three-part class the coordinates pin
the scene; drop the class and they do not even pin how many parts there are. -/
theorem uniqueness_is_class_relative :
    (vertexCount tripartite = 33 ∧ topBetti tripartite = 960 ∧ tripartite.length = 3) ∧
    (vertexCount fourpartite = 33 ∧ topBetti fourpartite = 960 ∧ fourpartite.length = 4) ∧
    (vertexCount sixpartite = 33 ∧ topBetti sixpartite = 960 ∧ sixpartite.length = 6) :=
  ⟨tripartite_witness, fourpartite_rival, sixpartite_rival⟩

/-- Sanity control: the coordinates are not blind — a scene with a different vertex count is
distinguished, so the rivals above agree for a reason and not because `vertexCount` is trivial. -/
theorem coordinates_are_not_blind :
    vertexCount [9, 11, 14] ≠ vertexCount tripartite ∧
    topBetti [9, 11, 14] ≠ topBetti tripartite := by
  refine ⟨by decide, by decide⟩

end D0.Synthesis.HomologicalReadingClassBoundary
