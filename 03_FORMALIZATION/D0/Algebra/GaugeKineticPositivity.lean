import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith
import D0.Algebra.GaugeActionSignBridge

namespace D0.Algebra

def gaugeKineticAction {n : Type} [Fintype n] [DecidableEq n] (K : Matrix n n ℝ) (c : ℝ) : ℝ :=
  -c * Matrix.trace (K * K)

theorem gaugeKineticAction_nonnegative {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) (c : ℝ) (hc : c > 0) :
    gaugeKineticAction K c ≥ 0 := by
  unfold gaugeKineticAction
  have h_tr := skew_square_trace_nonpositive K hK
  nlinarith

theorem gaugeKineticAction_eq_zero_iff {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) (c : ℝ) (hc : c > 0) :
    gaugeKineticAction K c = 0 ↔ K = 0 := by
  unfold gaugeKineticAction
  have h_ne : -c ≠ 0 := by linarith
  rw [mul_eq_zero, or_iff_right h_ne]
  exact skew_square_trace_eq_zero_iff K hK

end D0.Algebra
