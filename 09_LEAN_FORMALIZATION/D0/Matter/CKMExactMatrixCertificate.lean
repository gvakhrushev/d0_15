import D0.Matter.CKMExactTransfer
import Mathlib.Tactic

namespace D0.Matter

/-- Explicit matrix read from the concrete finite CKM basis-origin witness. -/
def concreteCKMExactMatrix : Matrix (Fin 3) (Fin 3) ℚ :=
  fun i j =>
    if i = 0 ∧ j = 2 then 1 else
    if i = 1 ∧ j = 0 then 1 else
    if i = 2 ∧ j = 1 then 1 else 0

/-- The concrete CKM origin evaluates to the exact finite permutation matrix. -/
theorem concrete_ckm_matrix_entries_closed :
    ckmOriginMatrix concreteCKMBasisOrigin = concreteCKMExactMatrix := by
  native_decide

/-- The frozen CKM transfer matrix is the exact matrix above. -/
theorem frozen_ckm_exact_matrix_closed
    (T : FrozenCKMMatrixTransfer) :
    T.matrix = concreteCKMExactMatrix := by
  rw [frozen_ckm_matrix_forced T]
  exact concrete_ckm_matrix_entries_closed

/-- The exact finite CKM matrix has one unit readout in each row. -/
theorem concrete_ckm_exact_matrix_row_support_closed :
    (concreteCKMExactMatrix 0 2 = 1) ∧
      (concreteCKMExactMatrix 1 0 = 1) ∧
        (concreteCKMExactMatrix 2 1 = 1) := by
  norm_num [concreteCKMExactMatrix]

end D0.Matter
