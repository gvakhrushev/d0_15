import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-CKM-EXACT-001 — the generation-overlap matrix is the cyclic permutation (structural)

Python certificate: `05_CERTS/vp_ckm_exact_matrix_certificate.py`.

The up basis vectors are canonical `0,1,2`; the down basis is the cyclic shift `1,2,0`.
The exact overlap matrix `M[i][j] = [up_i = down_j]` is therefore the cyclic permutation
matrix.  This module proves the STRUCTURAL fact (a doubly-stochastic 0/1 = permutation
matrix, det `= 1`); the empirical CKM angles are a separate downstream passport and are
NOT touched here.
-/

namespace D0.Claims

open Matrix

/-- The exact generation-overlap matrix `M[i][j] = [up_i = down_j]` with up `= (0,1,2)`,
down `= (1,2,0)`: column `j` carries its single `1` in row `down_j`. -/
def ckmExact : Matrix (Fin 3) (Fin 3) ℤ := !![0, 0, 1; 1, 0, 0; 0, 1, 0]

/-- Every row sum is `1` (the overlap is stochastic in the up index). -/
theorem ckm_row_sums_one : ∀ i, (∑ j, ckmExact i j) = 1 := by decide

/-- Every column sum is `1` (the overlap is stochastic in the down index). -/
theorem ckm_col_sums_one : ∀ j, (∑ i, ckmExact i j) = 1 := by decide

/-- All entries are `0` or `1` (so unit row/column sums force exactly one `1` each — a
genuine permutation matrix). -/
theorem ckm_entries_boolean : ∀ i j, ckmExact i j = 0 ∨ ckmExact i j = 1 := by decide

/-- `det = 1`: the cyclic 3-shift is an even permutation. -/
theorem ckm_det_one : Matrix.det ckmExact = 1 := by
  simp [Matrix.det_fin_three, ckmExact]

/-- **D0-CKM-EXACT-001 (structural).** The generation-overlap matrix is the cyclic
permutation matrix: doubly-stochastic 0/1, one `1` per row/column, `det = 1`. -/
theorem ckm_exact_matrix :
    (∀ i, (∑ j, ckmExact i j) = 1) ∧ (∀ j, (∑ i, ckmExact i j) = 1) ∧
    Matrix.det ckmExact = 1 :=
  ⟨ckm_row_sums_one, ckm_col_sums_one, ckm_det_one⟩

end D0.Claims
