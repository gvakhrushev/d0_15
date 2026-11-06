import D0.Geometry.OriginalBookJuliaWords
import Mathlib.Analysis.Matrix.Order
import Mathlib.Tactic

/-!
# Source Julia pair normalization

For each of the 32 ordered source pairs, prove the original operator identity
`W₀ W₀† + W₁ W₁† = I` from the actual input and the already proved positive
CFC roots. Source uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
lines 77–87; modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 125–159, at commit eebcb5e467742df3e9cf7fa9702042d7294aa742.
This is a pair identity, not yet Walsh Parseval, Kraus completeness, a rank
claim, or a physical admission statement.
-/
open D0
open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.CubicExponential
open D0.Geometry.OriginalBookStaticRoots
open Matrix
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OriginalBookJuliaRowCompleteness

/-- A positive defect root closes exactly the corresponding operator row. -/
lemma defect_row_complete (x : Operator) (h : (1 - x * xᴴ).PosDef) :
    x * xᴴ + CFC.sqrt (1 - x * xᴴ) * (CFC.sqrt (1 - x * xᴴ))ᴴ = 1 := by
  have hn : 0 ≤ (1 - x * xᴴ) := h.posSemidef.nonneg
  have hs := CFC.sqrt_mul_sqrt_self (1 - x * xᴴ) hn
  have hh : (CFC.sqrt (1 - x * xᴴ))ᴴ = CFC.sqrt (1 - x * xᴴ) :=
    (CFC.sqrt_nonneg (1 - x * xᴴ)).posSemidef.isHermitian
  rw [hh, hs]
  simp

/-- Each actual source row pair has identity left Gram sum. -/
theorem rowPair_complete (mode row : Fin 4) :
    (rowPair mode row).1 * ((rowPair mode row).1)ᴴ +
      (rowPair mode row).2 * ((rowPair mode row).2)ᴴ = 1 := by
  let r := modeRole mode
  have h := source_defects_posDef r
  fin_cases row
  · change sourceAnalyticOperand r * (sourceAnalyticOperand r)ᴴ + liveLeft r * (liveLeft r)ᴴ = 1
    rw [liveLeft_is_source_root]
    exact defect_row_complete _ h.1
  · change (sourceAnalyticOperand r)ᴴ * ((sourceAnalyticOperand r)ᴴ)ᴴ + liveRight r * (liveRight r)ᴴ = 1
    rw [liveRight_is_source_root]
    have hp : (1 - (sourceAnalyticOperand r)ᴴ * ((sourceAnalyticOperand r)ᴴ)ᴴ).PosDef := by
      simpa using h.2.1
    simpa using defect_row_complete (sourceAnalyticOperand r)ᴴ hp
  · change (-sourceBase r) * (-sourceBase r)ᴴ + (-baseLeft r) * (-baseLeft r)ᴴ = 1
    rw [baseLeft_is_source_root]
    simpa using defect_row_complete (sourceBase r) h.2.2.1
  · change (-(sourceBase r)ᴴ) * (-(sourceBase r)ᴴ)ᴴ + (-baseRight r) * (-baseRight r)ᴴ = 1
    rw [baseRight_is_source_root]
    have hp : (1 - (sourceBase r)ᴴ * ((sourceBase r)ᴴ)ᴴ).PosDef := by
      simpa using h.2.2.2
    simpa using defect_row_complete (sourceBase r)ᴴ hp

/-- The source's duplicate/index map carries the identity to all 32 words. -/
theorem sourceWord_complete (word : Fin 32) :
    (sourceWord word).1 * ((sourceWord word).1)ᴴ +
      (sourceWord word).2 * ((sourceWord word).2)ᴴ = 1 := by
  exact rowPair_complete (wordMode word) (wordRow word)

end D0.Geometry.OriginalBookJuliaRowCompleteness


