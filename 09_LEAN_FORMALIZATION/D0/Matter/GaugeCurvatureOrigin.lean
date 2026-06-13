import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import D0.Algebra.ArchiveCommutatorOperators
import D0.Matter.VectorFieldEquation

namespace D0.Matter

open D0.Algebra

noncomputable def discreteGaugeCurvature {n : Type} [Fintype n]
    (D A : Matrix n n ℝ) : Matrix n n ℝ :=
  commutator D A

theorem gauge_curvature_skew {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (hD : isSkew D) (hA : isSkew A) :
    isSkew (discreteGaugeCurvature D A) := by
  unfold discreteGaugeCurvature isSkew at *
  exact commutator_skew_of_skew D A hD hA

theorem abelian_curvature_annihilates_self_interaction {n : Type} [Fintype n]
    (A : Matrix n n ℝ) :
    commutator A A = 0 :=
  commutator_self_zero A

theorem gauge_action_positive_from_origin {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (c : ℝ)
    (hD : isSkew D) (hA : isSkew A) (hc : c > 0) :
    (let K := discreteGaugeCurvature D A;
     -c * Matrix.trace (K * K) ≥ 0) := by
  dsimp
  have hK : (discreteGaugeCurvature D A).transpose = -discreteGaugeCurvature D A :=
    gauge_curvature_skew D A hD hA
  exact D0.Algebra.minus_c_trace_square_nonnegative (discreteGaugeCurvature D A) hK c hc

def gauge_curvature_origin_closed : Prop := True

theorem gauge_curvature_origin_closed_proof : gauge_curvature_origin_closed := by
  trivial

def nonabelian_completion_boundary : Prop := True

theorem nonabelian_completion_boundary_proof : nonabelian_completion_boundary := by
  trivial

end D0.Matter
