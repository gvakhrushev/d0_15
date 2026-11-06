import D0.Algebra.SavedFutureMatrixPacked
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-! Determinant consumer for the concrete saved numerical matrices only.
The imported inverse theorem uses native computation; no source effect,
modular transport or complex conclusion is asserted here. -/
namespace D0.Algebra.SavedFutureMatrixPacked

theorem saved_matrix_det_ne_zero : A.det ≠ 0 := by
  have hdet : A.det * B.det = 1 := by
    simpa only [Matrix.det_mul, Matrix.det_one] using
      congrArg Matrix.det saved_matrix_right_inverse
  intro hz
  rw [hz, zero_mul] at hdet
  exact (zero_ne_one : (0 : ZMod 1009) ≠ 1) hdet

end D0.Algebra.SavedFutureMatrixPacked

#print axioms D0.Algebra.SavedFutureMatrixPacked.saved_matrix_det_ne_zero
