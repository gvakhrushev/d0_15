import D0.Matter.CKMBasisOrigin
import Mathlib.Tactic

namespace D0.Matter

/--
A frozen CKM transfer is not an arbitrary numerical matrix.  It is exactly the
matrix read from a frozen finite basis origin.  External PDG/RG comparison may
only be attached after this object is fixed.
-/
structure FrozenCKMMatrixTransfer where
  origin : CKMBasisOrigin 3 CKMFlavorOperator
  origin_is_concrete : origin = concreteCKMBasisOrigin
  matrix : Matrix (Fin 3) (Fin 3) ℚ
  matrix_eq : matrix = ckmOriginMatrix origin

/-- Concrete exact finite CKM transfer object. -/
def concreteFrozenCKMMatrixTransfer : FrozenCKMMatrixTransfer where
  origin := concreteCKMBasisOrigin
  origin_is_concrete := rfl
  matrix := ckmOriginMatrix concreteCKMBasisOrigin
  matrix_eq := rfl

/-- Every admissible frozen CKM transfer has the concrete D0 origin matrix. -/
theorem frozen_ckm_matrix_forced
    (T : FrozenCKMMatrixTransfer) :
    T.matrix = ckmOriginMatrix concreteCKMBasisOrigin := by
  have ho : T.origin = concreteCKMBasisOrigin := T.origin_is_concrete
  simpa [ho] using T.matrix_eq

/-- A different matrix cannot be installed at the same frozen CKM origin. -/
theorem frozen_ckm_no_external_matrix_knob
    (T : FrozenCKMMatrixTransfer)
    (M : Matrix (Fin 3) (Fin 3) ℚ)
    (hM : M ≠ ckmOriginMatrix concreteCKMBasisOrigin) :
    T.matrix ≠ M := by
  intro h
  apply hM
  rw [← h]
  exact frozen_ckm_matrix_forced T

/-- RG/passport comparison has no authority to change the finite CKM matrix. -/
structure CKMComparisonPassport where
  frozen : FrozenCKMMatrixTransfer
  comparisonMatrix : Matrix (Fin 3) (Fin 3) ℚ
  comparison_is_readout : comparisonMatrix = frozen.matrix

/-- Every admissible CKM comparison reads the frozen matrix. -/
theorem ckm_comparison_passport_reads_frozen_matrix
    (P : CKMComparisonPassport) :
    P.comparisonMatrix = ckmOriginMatrix concreteCKMBasisOrigin := by
  rw [P.comparison_is_readout]
  exact frozen_ckm_matrix_forced P.frozen

end D0.Matter
