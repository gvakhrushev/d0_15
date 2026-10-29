import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.FiniteMatrixTensorProduct

namespace D0.Gauge

abbrev flatTensor {s a : Type} (A : Matrix s s ℝ) (T : Matrix a a ℝ) :
    Matrix (s × a) (s × a) ℝ :=
  D0.Algebra.finiteMatrixTensorProduct A T

theorem flat_tensor_of_two_skew_is_symmetric {s a : Type}
    (A : Matrix s s ℝ) (T : Matrix a a ℝ)
    (hA : A.transpose = -A) (hT : T.transpose = -T) :
    (flatTensor A T).transpose = flatTensor A T := by
  change (D0.Algebra.finiteMatrixTensorProduct A T).transpose =
    D0.Algebra.finiteMatrixTensorProduct A T
  rw [D0.Algebra.finiteMatrixTensorProduct_transpose, hA, hT]
  ext p q
  simp [D0.Algebra.finiteMatrixTensorProduct, Matrix.kronecker,
    Matrix.kroneckerMap_apply]

/-- No-go: the naive flat (Kronecker) tensor of two skew gauge operators is SYMMETRIC, not skew, so
it cannot itself be a non-abelian curvature (instantiates the proved
`flat_tensor_of_two_skew_is_symmetric`). -/
def naive_flat_tensor_nonabelian_boundary : Prop :=
  ∀ {s a : Type} (A : Matrix s s ℝ) (T : Matrix a a ℝ),
    A.transpose = -A → T.transpose = -T → (flatTensor A T).transpose = flatTensor A T

theorem naive_flat_tensor_nonabelian_boundary_proof :
    naive_flat_tensor_nonabelian_boundary := by
  intro s a A T hA hT
  exact flat_tensor_of_two_skew_is_symmetric A T hA hT

end D0.Gauge
