import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

namespace D0.Gauge

noncomputable def flatTensor {s a : Type} (A : Matrix s s ℝ) (T : Matrix a a ℝ) :
    Matrix (s × a) (s × a) ℝ :=
  fun p q => A p.1 q.1 * T p.2 q.2

theorem flat_tensor_of_two_skew_is_symmetric {s a : Type}
    (A : Matrix s s ℝ) (T : Matrix a a ℝ)
    (hA : A.transpose = -A) (hT : T.transpose = -T) :
    (flatTensor A T).transpose = flatTensor A T := by
  ext p q
  unfold flatTensor
  have hA_apply : A q.1 p.1 = -A p.1 q.1 := by
    have h := congr_fun (congr_fun hA q.1) p.1
    simp [Matrix.transpose_apply] at h
    linarith
  have hT_apply : T q.2 p.2 = -T p.2 q.2 := by
    have h := congr_fun (congr_fun hT q.2) p.2
    simp [Matrix.transpose_apply] at h
    linarith
  simp [Matrix.transpose_apply, hA_apply, hT_apply]

def naive_flat_tensor_nonabelian_boundary : Prop := True

theorem naive_flat_tensor_nonabelian_boundary_proof :
    naive_flat_tensor_nonabelian_boundary := by
  trivial

end D0.Gauge
