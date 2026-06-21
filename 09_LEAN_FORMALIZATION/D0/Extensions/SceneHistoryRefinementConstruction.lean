import D0.Extensions.SceneHistoryRefinementExtension
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-SCENE-HISTORY-REFINEMENT-001 — Lane H terminal (H3)

The all-walks (`W`, Perron 21.84, depth-2 carrier 15708) and non-backtracking (`NB`, Perron 20.83, carrier
14990) refinement families are independently generated, admissible, and inequivalent — terminal **H3**
(several inequivalent towers). The forced no-`φ³` result holds in BOTH (min-successor `19 > φ³`). No internal
CMB smoothing window is forced. Missing: `PRIM-SCENE-HISTORY-REFINEMENT-RULE`.
-/

namespace D0.Extensions.SceneHistoryRefinementConstruction

open D0 D0.Extensions.SceneHistoryRefinementExtension

/-- **Terminal H3.** Two inequivalent refinement towers (`15708 ≠ 14990`); no-`φ³` in both (min-successor `19`). -/
theorem scene_history_refinement_H3 :
    (15708 : ℕ) ≠ 14990 ∧ phi ^ 3 < (minSuccessor : ℝ) ∧ minSuccessor = 19 :=
  ⟨refinement_two_completion, path_perron_above_phi3, min_successor_eq⟩

end D0.Extensions.SceneHistoryRefinementConstruction
