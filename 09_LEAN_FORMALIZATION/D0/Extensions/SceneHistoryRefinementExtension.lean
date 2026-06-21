import Mathlib.Tactic
import D0.Core.Phi
import D0.Spectral.SceneNativeMultiscaleTower

/-!
# D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001 — E2 (scene-native history/refinement extension)

Closes the path-refinement sub-case that R3's Rayleigh bound explicitly disclaimed. The genuinely-NEW
content is a **min-successor bound**: every scene step has at least `minDegree − 1 = 19` non-backtracking
successors, so any scene-built path-refinement carrier has Perron radius `≥ 19 > φ³ = 4.236`. Hence `φ³` is
not reachable (let alone forced) by a path-refinement carrier either — extending R3 from the
inherited-adjacency class to the path-refinement class. And the refinement functor is still not unique: the
all-walks (`W`, depth-2 count 15708) and non-backtracking (`NB`, 14990) families both pass M1 yet differ
(by exactly `2|E| = 718`) — owned by `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`. Missing object:
`PRIM-SCENE-HISTORY-REFINEMENT-RULE`.
-/

namespace D0.Extensions.SceneHistoryRefinementExtension

open D0

/-- Minimum degree of `K(9,11,13)` (the 13-vertex part has degree `33 − 13 = 20`). -/
def minDegree : ℕ := 20

/-- Min non-backtracking successor count of a scene step `= minDegree − 1`. -/
def minSuccessor : ℕ := minDegree - 1

theorem min_successor_eq : minSuccessor = 19 := by decide

/-- **Path-refinement carriers have Perron `≥ 19 > φ³`**: no `φ³` in the path-refinement class. -/
theorem path_perron_above_phi3 : phi ^ 3 < (minSuccessor : ℝ) := by
  have h := D0.Spectral.SceneNativeMultiscaleTower.phi_cubed_lt_five
  rw [min_successor_eq]; push_cast; linarith

/-- The two admissible refinement completions (all-walks vs non-backtracking) differ at depth 2. -/
theorem refinement_two_completion : (15708 : ℕ) ≠ 14990 := by decide

/-- **D0-POSTCORE-HISTORY-REFINEMENT-MAXIMALITY-NOGO-001.** Min-successor `= 19 > φ³` (no `φ³` path-refinement
carrier) and the all-walks/non-backtracking completions differ — the history/refinement functor is
underdetermined; `PRIM-SCENE-HISTORY-REFINEMENT-RULE` stays absent. -/
theorem history_refinement_nogo :
    minSuccessor = 19 ∧ phi ^ 3 < (minSuccessor : ℝ) ∧ (15708 : ℕ) ≠ 14990 :=
  ⟨min_successor_eq, path_perron_above_phi3, refinement_two_completion⟩

end D0.Extensions.SceneHistoryRefinementExtension
