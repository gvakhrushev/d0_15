import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

open Matrix

/-!
# Fixed-carrier trace-volume tangent

For a finite idempotent readout `P`, every first-order variation satisfying
the differentiated idempotency equation has zero trace. This is an algebraic
boundary for continuous changes inside one fixed carrier; it does not identify
an AF refinement or a D0 physical volume with this readout.
-/

namespace D0.Research.RankVolumeTangent

/-- Every tangent to the finite idempotent locus has zero ordinary trace. -/
theorem idempotent_tangent_trace_zero
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (P X : Matrix ι ι ℝ)
    (hP : P * P = P)
    (hX : P * X + X * P = X) :
    Matrix.trace X = 0 := by
  have hleft := congrArg (fun Y : Matrix ι ι ℝ => P * Y) hX
  have he : P * X + P * X * P = P * X := by
    simpa only [Matrix.mul_add, ← Matrix.mul_assoc, hP] using hleft
  have hPXP : P * X * P = 0 :=
    add_left_cancel (show P * X + P * X * P = P * X + 0 by simpa using he)
  have hTracePXP : Matrix.trace (P * X * P) = Matrix.trace (P * X) := by
    calc
      Matrix.trace (P * X * P) = Matrix.trace (P * (X * P)) := by
        rw [Matrix.mul_assoc]
      _ = Matrix.trace ((X * P) * P) := Matrix.trace_mul_comm _ _
      _ = Matrix.trace (X * P) := by simp [Matrix.mul_assoc, hP]
      _ = Matrix.trace (P * X) := Matrix.trace_mul_comm _ _
  have hTraceXP : Matrix.trace (X * P) = 0 := by
    calc
      Matrix.trace (X * P) = Matrix.trace (P * X) := Matrix.trace_mul_comm _ _
      _ = Matrix.trace (P * X * P) := hTracePXP.symm
      _ = 0 := by simp [hPXP]
  have hTracePX : Matrix.trace (P * X) = 0 := by
    rw [Matrix.trace_mul_comm P X, hTraceXP]
  have htrace := congrArg Matrix.trace hX
  rw [Matrix.trace_add] at htrace
  calc
    Matrix.trace X = Matrix.trace (P * X) + Matrix.trace (X * P) := htrace.symm
    _ = 0 := by rw [hTracePX, hTraceXP]; simp

#print axioms idempotent_tangent_trace_zero

end D0.Research.RankVolumeTangent
