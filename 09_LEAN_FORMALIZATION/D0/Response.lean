import D0.Core.MatrixResponse

namespace D0

def responseOperator2 (D : FinMatrix 2 ℚ) : FinMatrix 2 ℚ := D

theorem trace_response_additive (A B : FinMatrix 2 ℚ) :
    diagonalTrace2 (A + B) = diagonalTrace2 A + diagonalTrace2 B :=
  diagonalTrace2_add A B

theorem trace_nonnegative_of_diagonal_nonnegative
    (A : FinMatrix 2 ℚ) (h0 : 0 ≤ A 0 0) (h1 : 0 ≤ A 1 1) :
    0 ≤ diagonalTrace2 A := by
  unfold diagonalTrace2
  linarith

theorem normalization_possible_if_trace_nonzero
    (t : ℚ) (ht : t ≠ 0) : t / t = 1 := by
  field_simp [ht]

end D0
