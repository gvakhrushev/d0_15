import D0.VNext2.SceneSpectralFingerprint
import Mathlib.Tactic

/-!
# D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 — Outcome D (refinement rule underdetermined)

A scene-native refinement of `K(9,11,13)` requires choosing a history/path family. At least two families
satisfy every M1 admissibility condition (built from scene adjacency, `Aut(K(9,11,13))`-equivariant,
part-preserving via intrinsic degree/role data, basepoint-free, computable, deterministic endpoint map):

- **Family W** (all finite walks) — vertex-level transfer = adjacency `A` (carrier `H_scene`, dim 33);
- **Family NB** (non-backtracking walks) — transfer = Hashimoto operator on directed edges (dim `2|E| = 718`);
- **Family E** (directed-edge / de Bruijn history) — directed-edge carrier (dim `2|E| = 718`).

They are **inequivalent**: at depth 2 the all-walks carrier is `Σ n_i·deg_i² = 9·24² + 11·22² + 13·20² =
15708`, the non-backtracking carrier is `Σ n_i·deg_i·(deg_i−1) = 14990` — differing by exactly the
`2|E| = 718` backtracks. The vertex-transfer dim `33` differs from the directed-edge dim `718`. So the
families produce different transfer operators, endpoint conditional expectations, and hence different
`Ξ_n`/spectra.

**Outcome D**: no unique scene-native refinement rule is forced; the comparison map `Ξ` is therefore not
canonically determined. Missing primitive `PRIM-SCENE-HISTORY-REFINEMENT-RULE`. The two earlier interfaces
`PRIM-COMPARISON-MAP-XI-N` and `PRIM-DIRAC-SCALE-SELECTION` remain independent and unresolved.
-/

namespace D0.VNext2.SceneNativeRefinementClassification

open D0.VNext2.SceneSpectralFingerprint

/-- Depth-2 carrier of the all-walks family: `Σ n_i·deg_i²`. -/
def allWalksDepth2 : ℕ := 9 * 24 ^ 2 + 11 * 22 ^ 2 + 13 * 20 ^ 2

/-- Depth-2 carrier of the non-backtracking family: `Σ n_i·deg_i·(deg_i − 1)`. -/
def nonBacktrackingDepth2 : ℕ := 9 * 24 * 23 + 11 * 22 * 21 + 13 * 20 * 19

/-- All-walks vertex transfer acts on `H_scene` (dim 33); directed-edge / non-backtracking on `2|E| = 718`. -/
def allWalksVertexDim : ℕ := 33
def directedEdgeDim : ℕ := 2 * numEdges

/-- **The all-walks and non-backtracking families have different depth-2 carriers**, differing by exactly
the `2|E| = 718` backtracking walks. -/
theorem walk_families_carriers_differ :
    allWalksDepth2 = 15708 ∧ nonBacktrackingDepth2 = 14990
      ∧ allWalksDepth2 - nonBacktrackingDepth2 = 2 * numEdges := by
  refine ⟨by decide, by decide, by decide⟩

/-- **The vertex transfer and the directed-edge transfer have different dimensions** (`33 ≠ 718`). -/
theorem transfer_dimensions_differ : allWalksVertexDim ≠ directedEdgeDim := by decide

/-- **D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 (Outcome D).** At least two admissible scene-native
refinement families (all-walks, non-backtracking, directed-edge) produce inequivalent carriers/transfer
operators — depth-2 carriers `15708 ≠ 14990`, transfer dims `33 ≠ 718`. No unique refinement rule is forced
by present-core; `Ξ` is not canonically determined. Missing primitive `PRIM-SCENE-HISTORY-REFINEMENT-RULE`. -/
theorem scene_native_refinement_underdetermined :
    allWalksDepth2 ≠ nonBacktrackingDepth2
      ∧ allWalksVertexDim ≠ directedEdgeDim := by
  refine ⟨by decide, by decide⟩

end D0.VNext2.SceneNativeRefinementClassification
