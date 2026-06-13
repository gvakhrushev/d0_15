import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.GaugeActionSignBridge

namespace D0.Algebra

noncomputable def commutator {n : Type} [Fintype n] (X Y : Matrix n n ℝ) : Matrix n n ℝ :=
  X * Y - Y * X

theorem commutator_self_zero {n : Type} [Fintype n] (A : Matrix n n ℝ) :
    commutator A A = 0 := by
  unfold commutator
  simp

theorem commutator_skew_of_skew {n : Type} [Fintype n] [DecidableEq n]
    (X Y : Matrix n n ℝ) (hX : X.transpose = -X) (hY : Y.transpose = -Y) :
    (commutator X Y).transpose = - commutator X Y := by
  unfold commutator
  rw [Matrix.transpose_sub, Matrix.transpose_mul, Matrix.transpose_mul, hX, hY]
  ext i j
  simp [Matrix.sub_apply, Matrix.neg_apply]

theorem skew_square_trace_nonpositive_reexport {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) :
    Matrix.trace (K * K) ≤ 0 :=
  skew_square_trace_nonpositive K hK

theorem minus_trace_square_nonnegative {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) :
    - Matrix.trace (K * K) ≥ 0 := by
  have h := skew_square_trace_nonpositive K hK
  linarith

theorem minus_c_trace_square_nonnegative {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) (c : ℝ) (hc : c > 0) :
    -c * Matrix.trace (K * K) ≥ 0 := by
  have h := skew_square_trace_nonpositive K hK
  nlinarith

end D0.Algebra
