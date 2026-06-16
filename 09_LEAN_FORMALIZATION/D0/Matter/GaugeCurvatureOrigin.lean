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

/-- The discrete gauge curvature closes on skew operators: `[D,A]` of two skew (Lie-algebra)
operators is skew (instantiates the proved `gauge_curvature_skew`). -/
def gauge_curvature_origin_closed : Prop :=
  ∀ {n : Type} [Fintype n] [DecidableEq n] (D A : Matrix n n ℝ),
    isSkew D → isSkew A → isSkew (discreteGaugeCurvature D A)

theorem gauge_curvature_origin_closed_proof : gauge_curvature_origin_closed := by
  intro n _ _ D A hD hA
  exact gauge_curvature_skew D A hD hA

/-- The abelian boundary that the non-abelian completion lives past: the abelian curvature
annihilates its own self-interaction, `[A,A] = 0` (`abelian_curvature_annihilates_self_interaction`).
This vanishing self-interaction is exactly why the `½[A,A]` non-abelian completion term is needed. -/
def nonabelian_completion_boundary : Prop :=
  ∀ {n : Type} [Fintype n] (A : Matrix n n ℝ), commutator A A = 0

theorem nonabelian_completion_boundary_proof : nonabelian_completion_boundary := by
  intro n _ A
  exact abelian_curvature_annihilates_self_interaction A

end D0.Matter
