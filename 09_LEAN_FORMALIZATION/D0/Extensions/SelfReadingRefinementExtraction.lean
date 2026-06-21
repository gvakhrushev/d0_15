import D0.Extensions.SceneHistoryRefinementExtension
import D0.Core.Phi
import Mathlib.Tactic

/-!
# Self-reading refinement extraction (Section 2.2)

What `S₀` FORCES on the history side: the negative result `no φ³ Perron carrier` (min-successor
`minDegree − 1 = 19 > φ³`, holding in BOTH the all-walks and non-backtracking families). What it does NOT fix:
the refinement/CMB-window carrier — all-walks depth-2 count `15708 ≠ 14990` non-backtracking. No CMB tilt is
selected (no canonical window without Planck/pivot/width).
-/

namespace D0.Extensions.SelfReadingRefinementExtraction

open D0 D0.Extensions.SceneHistoryRefinementExtension

/-- **2.2 forced vs disputed.** Forced: `φ³ < 19` (no φ³ carrier in either family). Disputed: refinement
carrier `15708 ≠ 14990`. -/
theorem refinement_extraction_forced_vs_disputed :
    phi ^ 3 < (minSuccessor : ℝ) ∧ (15708 : ℕ) ≠ 14990 :=
  ⟨path_perron_above_phi3, refinement_two_completion⟩

end D0.Extensions.SelfReadingRefinementExtraction
