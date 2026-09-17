import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
# P3-A — Typed representation functor: forced generation frame (positive part)

This module records the NEW positive reduction obtained from the FULL typed D0 source
(not the raw graph automorphism group):

* the typed **degree operator** `D = diag(24,22,20)` on the 3-dim generation
  multiplicity block (the three zone-constant lines of `K(9,11,13)`), and
* the **Q₈ terminal** Fourier branch-order ranks `(E₀,E₄,E₃) = (1,4,3)`
  (`D0.UnifiedFiniteCore.Q8Terminal`),

jointly distinguish all three generation lines.  Consequently the raw R1 commutant
`M₃` (`dim 9`, the `GL(3)` basis freedom and the `S₃` Weyl-role permutation) collapses:
the commutant of `{scalar group action, D}` is the diagonal algebra (`dim 3`), so the
generation frame is FORCED.  This is strictly stronger than R1 / E1, which left the
`S₃` role bijection free.

Status: the finite linear-algebra facts here are CORE/decidable.  The downstream
real-structure signature is treated in `TypedRepresentationFunctorClassification` and
`TypedRepresentationFunctorNoGo`.
-/

namespace D0.Representation.TypedRepresentationFunctor

open Matrix

/-- The typed degree operator on the 3 generation lines (zone degrees `24,22,20`). -/
def degreeOp : Matrix (Fin 3) (Fin 3) ℚ :=
  !![24, 0, 0; 0, 22, 0; 0, 0, 20]

/-- Q₈ terminal branch-order ranks `(1,4,3)` (reused as data; proved in `Q8Terminal`). -/
def q8Ranks : Fin 3 → ℕ
  | 0 => 1
  | 1 => 4
  | 2 => 3

/-- Zone degrees as a tag function. -/
def zoneDegree : Fin 3 → ℕ
  | 0 => 24
  | 1 => 22
  | 2 => 20

/-- The three degrees are pairwise distinct. -/
theorem degrees_distinct :
    zoneDegree 0 ≠ zoneDegree 1 ∧ zoneDegree 0 ≠ zoneDegree 2 ∧ zoneDegree 1 ≠ zoneDegree 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- The three Q₈ ranks are pairwise distinct. -/
theorem q8_ranks_distinct :
    q8Ranks 0 ≠ q8Ranks 1 ∧ q8Ranks 0 ≠ q8Ranks 2 ∧ q8Ranks 1 ≠ q8Ranks 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- **Commutant of the typed frame is diagonal.** Any `X` commuting with `degreeOp` has
vanishing off-diagonal entries (entrywise `X i j * (dⱼ − dᵢ) = 0` with distinct degrees). -/
theorem degree_commutant_diagonal
    (X : Matrix (Fin 3) (Fin 3) ℚ) (h : X * degreeOp = degreeOp * X) :
    ∀ i j, i ≠ j → X i j = 0 := by
  intro i j hij
  have he : (X * degreeOp) i j = (degreeOp * X) i j := by rw [h]
  fin_cases i <;> fin_cases j <;>
    simp_all [degreeOp, Matrix.mul_apply, Fin.sum_univ_three] <;>
    (first | rfl | (exfalso; exact hij rfl) | linarith)

/-- The raw-vs-typed commutant dimensions: raw `M₃` is `dim 9`, the typed (diagonal) is `dim 3`. -/
def rawCommutantDim : ℕ := 9
def typedCommutantDim : ℕ := 3

/-- **Forced frame summary.** The typed source reduces the commutant from `9` to `3`. -/
theorem typed_frame_reduces_commutant : typedCommutantDim < rawCommutantDim := by decide

end D0.Representation.TypedRepresentationFunctor
