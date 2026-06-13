import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace D0

abbrev FinMatrix (n : ℕ) (α : Type) := Matrix (Fin n) (Fin n) α

def diagonalTrace2 (M : FinMatrix 2 ℚ) : ℚ := M 0 0 + M 1 1

theorem diagonalTrace2_add (A B : FinMatrix 2 ℚ) :
    diagonalTrace2 (A + B) = diagonalTrace2 A + diagonalTrace2 B := by
  simp [diagonalTrace2]
  ring

end D0
