import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-!
# Algebraic transport of a moving projector

This module proves only the finite algebraic kinematics of a moving cut.
The tangent relation is a hypothesis: no differentiable projector family,
thermal or log-determinant derivative, physical admission, or GR conclusion
is constructed here. Multiplication need not commute.
-/

namespace D0.Algebra.MovingProjectorTransport

variable {R : Type*} [Ring R]

/-- The commutator on the declared associative unital ring. -/
def comm (A B : R) : R := A * B - B * A

/-- The canonical off-diagonal transport generator for a projector tangent. -/
def generator (P dP : R) : R := comm dP P

/-- The commutator of two self-adjoint elements is anti-self-adjoint.
Neither idempotence nor the projector tangent relation is needed here. -/
theorem generator_star_eq_neg [StarRing R] (P dP : R)
    (hP : star P = P) (hdP : star dP = dP) :
    star (generator P dP) = -generator P dP := by
  simp only [generator, comm, star_sub, star_mul, hP, hdP, neg_sub]

/-- The complementary transfer and its literal product-rule expression. -/
def cut (P U : R) : R := (1 - P) * U * P

def cutTangent (P dP U dU : R) : R :=
  -dP * U * P + (1 - P) * dU * P + (1 - P) * U * dP

/-- Differentiating `P * P = P` algebraically forces the diagonal tangent block
`P * dP * P` to vanish. The tangent equation is supplied, not derived here. -/
theorem tangent_middle_zero (P dP : R)
    (hP : P * P = P) (hT : P * dP + dP * P = dP) :
    P * dP * P = 0 := by
  have h : P * dP + P * dP * P = P * dP := by
    calc
      P * dP + P * dP * P = P * (P * dP + dP * P) := by
        rw [mul_add, ← mul_assoc, hP]
        simp only [mul_assoc]
      _ = P * dP := congrArg (fun x => P * x) hT
  exact add_eq_left.mp h

/-- The canonical generator transports the given tangent: `[[dP,P],P]=dP`. -/
theorem generator_transports (P dP : R)
    (hP : P * P = P) (hT : P * dP + dP * P = dP) :
    comm (generator P dP) P = dP := by
  have hzero := tangent_middle_zero P dP hP hT
  unfold generator comm
  calc
    (dP * P - P * dP) * P - P * (dP * P - P * dP) =
        dP * (P * P) - (P * dP * P) - (P * dP * P) + (P * P) * dP := by
          noncomm_ring
    _ = dP * P + P * dP := by rw [hP, hzero]; noncomm_ring
    _ = dP := by rw [add_comm]; exact hT

/-- For any transport generator with the required commutator, the full
product-rule cut tangent minus common transport equals the relative motion.
No commutativity, unitarity or positivity is assumed. -/
theorem cut_relative_of_transport (P dP U dU K : R)
    (hK : comm K P = dP) :
    cutTangent P dP U dU - comm K (cut P U) =
      (1 - P) * (dU - comm K U) * P := by
  unfold cutTangent cut comm at *
  rw [← hK]
  noncomm_ring

/-- Applying the derived canonical generator gives the moving-cut identity. -/
theorem cut_relative (P dP U dU : R)
    (hP : P * P = P) (hT : P * dP + dP * P = dP) :
    cutTangent P dP U dU - comm (generator P dP) (cut P U) =
      (1 - P) * (dU - comm (generator P dP) U) * P :=
  cut_relative_of_transport P dP U dU (generator P dP)
    (generator_transports P dP hP hT)

/-- Concrete specialization to square complex matrices, with no extra analytic
or self-adjointness hypotheses. -/
theorem complex_matrix_cut_relative {ι : Type*} [Fintype ι] [DecidableEq ι]
    (P dP U dU : Matrix ι ι ℂ)
    (hP : P * P = P) (hT : P * dP + dP * P = dP) :
    cutTangent P dP U dU - comm (generator P dP) (cut P U) =
      (1 - P) * (dU - comm (generator P dP) U) * P :=
  cut_relative P dP U dU hP hT

end D0.Algebra.MovingProjectorTransport
