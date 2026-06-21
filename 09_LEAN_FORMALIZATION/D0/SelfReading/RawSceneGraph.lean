import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Finset.Image
import Mathlib.Tactic

/-!
# D0-RAW-SCENE-GRAPH-001 — the raw K(9,11,13) object (no stipulation)

The scene is built from the partition `(9,11,13)` ALONE: `lab : Fin 33 → Fin 3` assigns each vertex its part
by index range, and the adjacency `Aadj i j = 1` iff `i, j` lie in different parts. Every "forced" output the
self-reading skeleton predicted is DERIVED here by `native_decide` from this raw object — not inserted as a
literal:
- degrees `{24, 22, 20}` (raw row sums);
- `2|E| = 718`, hence `|E| = 359`;
- `trace(A²) = 718`;
- commutant dimension `= 12`, computed as the number of `Aut`-orbits of index pairs (since `Aut = S₉×S₁₁×S₁₃`
  acts with distinct part sizes, two pairs `(i,j),(i',j')` are `Aut`-equivalent iff they share
  `(lab i, lab j, [i=j])`). This DE-STIPULATES the prior hand-written isotypic list.
-/

namespace D0.SelfReading.RawSceneGraph

/-- Part label of a vertex, from the partition `(9,11,13)` index ranges. -/
def lab (i : Fin 33) : Fin 3 := if i.val < 9 then 0 else if i.val < 20 then 1 else 2

/-- Raw tripartite adjacency: `1` iff the two vertices lie in different parts. -/
def Aadj (i j : Fin 33) : ℕ := if lab i = lab j then 0 else 1

/-- Raw degree = row sum of the adjacency. -/
def degree (i : Fin 33) : ℕ := ∑ j : Fin 33, Aadj i j

theorem adjacency_symmetric : ∀ i j : Fin 33, Aadj i j = Aadj j i := by decide

/-- Raw degree of part-0 (the 9-block) is `33 − 9 = 24`. -/
theorem degree_part0 : ∀ i : Fin 33, i.val < 9 → degree i = 24 := by native_decide
/-- Raw degree of part-1 (the 11-block) is `33 − 11 = 22`. -/
theorem degree_part1 : ∀ i : Fin 33, 9 ≤ i.val → i.val < 20 → degree i = 22 := by native_decide
/-- Raw degree of part-2 (the 13-block) is `33 − 13 = 20`. -/
theorem degree_part2 : ∀ i : Fin 33, 20 ≤ i.val → degree i = 20 := by native_decide

/-- Raw `2|E| = Σ degrees = 718`. -/
theorem two_edges : (∑ i : Fin 33, degree i) = 718 := by native_decide
/-- Raw `|E| = 359`. -/
theorem edges : (∑ i : Fin 33, degree i) / 2 = 359 := by native_decide
/-- Raw `trace(A²) = Σ_{i,k} A_{ik} A_{ki} = 718`. -/
theorem trace_A_sq : (∑ i : Fin 33, ∑ k : Fin 33, Aadj i k * Aadj k i) = 718 := by native_decide

/-- The `Aut`-class of an index pair: `(lab i, lab j, [i = j])` (a complete invariant of the `S₉×S₁₁×S₁₃` orbit). -/
def pairClass (p : Fin 33 × Fin 33) : Fin 3 × Fin 3 × Bool := (lab p.1, lab p.2, decide (p.1 = p.2))

/-- The commutant dimension = number of `Aut`-orbits of index pairs. -/
def commutantDim : ℕ := (Finset.univ.image pairClass).card

/-- **De-stipulated commutant**: `dim End_Aut(ℂ³³) = 12`, computed as the raw pair-orbit count (`3` diagonal +
`3` same-part off-diagonal + `6` cross-part) — NOT a hand-written list. -/
theorem commutant_dim_raw : commutantDim = 12 := by native_decide

/-- **D0-RAW-SCENE-GRAPH-001.** The forced skeleton outputs are raw graph invariants of `K(9,11,13)`:
degrees `{24,22,20}`, `2|E| = 718`, `trace(A²) = 718`, commutant dim `12` (pair-orbit count). -/
theorem raw_scene_invariants :
    (∀ i : Fin 33, i.val < 9 → degree i = 24) ∧ (∑ i : Fin 33, degree i) = 718 ∧
      (∑ i : Fin 33, ∑ k : Fin 33, Aadj i k * Aadj k i) = 718 ∧ commutantDim = 12 :=
  ⟨degree_part0, two_edges, trace_A_sq, commutant_dim_raw⟩

end D0.SelfReading.RawSceneGraph
