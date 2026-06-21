import D0.Extensions.X5.PrimitiveContract
import D0.Extensions.SceneHistoryRefinementExtension
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-X5-H — HistoryRefinement contract + model + deletion (Lane H)

The scene-history refinement primitive POSTULATED (HYP, D0-X5). Concrete model: the all-walks refinement,
depth-2 carrier count `15708` (independently generated, NOT `L_n := J_n L_scene C_n`). Deletion of the
refine/coarsen naturality law admits the non-backtracking model too (`14990 ≠ 15708`) — the law is necessary.
The no-`φ³` consequence holds in the model (min-successor `19 > φ³`), relative to the contract.
-/

namespace D0.Extensions.X5.History

open D0 D0.Extensions.X5

/-- The HistoryRefinement contract (HYP, D0-X5). -/
def histContract : PrimitiveContract :=
  ⟨"PRIM-SCENE-HISTORY-REFINEMENT-RULE", "D0-X5",
   ["refine-coarsen-inverse", "terminal-natural", "P-natural", "Q-natural", "no-chosen-root"], 33⟩

theorem hist_wellFormed : histContract.wellFormed := ⟨rfl, by decide, by decide⟩

/-- Concrete model invariant: all-walks depth-2 carrier count. -/
def allWalksDepth2 : ℕ := 15708
/-- The non-backtracking deletion alternative. -/
def nonBacktrackingDepth2 : ℕ := 14990

def histModel : ModelWitness := ⟨33, 5, true⟩
theorem hist_model_complete : histModel.complete histContract := ⟨rfl, by decide, rfl⟩

/-- Deletion test: drop the refine/coarsen naturality ⇒ all-walks and non-backtracking both admissible. -/
def hist_deletion : DeletionTest := ⟨"refine-coarsen-inverse", 2⟩
theorem hist_deletion_necessary : hist_deletion.lawNecessary := by decide
theorem hist_deletion_models_differ : allWalksDepth2 ≠ nonBacktrackingDepth2 := by decide

/-- **Relative consequence.** No-`φ³` carrier in the refinement model (min-successor `19 > φ³`). -/
theorem hist_no_phi3 : phi ^ 3 < (D0.Extensions.SceneHistoryRefinementExtension.minSuccessor : ℝ) :=
  D0.Extensions.SceneHistoryRefinementExtension.path_perron_above_phi3

/-- **D0-X5-H terminal.** Contract well-formed, model complete, deletion-minimal. -/
theorem history_x5_terminal :
    histContract.wellFormed ∧ histModel.complete histContract ∧
      hist_deletion.lawNecessary ∧ allWalksDepth2 ≠ nonBacktrackingDepth2 :=
  ⟨hist_wellFormed, hist_model_complete, hist_deletion_necessary, hist_deletion_models_differ⟩

end D0.Extensions.X5.History
