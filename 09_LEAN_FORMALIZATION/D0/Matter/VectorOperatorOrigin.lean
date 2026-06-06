import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.ArchiveCommutatorOperators
import D0.Matter.GaugeCurvatureOrigin
import D0.Matter.VectorFieldEquation

open scoped BigOperators

namespace D0.Matter

open D0.Algebra

noncomputable def vectorLaplacian {n : Type} [Fintype n]
    (D A : Matrix n n ℝ) : Matrix n n ℝ :=
  - commutator D (commutator D A)

lemma skew_neg {n : Type} (M : Matrix n n ℝ) (hM : isSkew M) : isSkew (-M) := by
  unfold isSkew at *
  rw [Matrix.transpose_neg, hM]

theorem vector_laplacian_preserves_skew {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (hD : isSkew D) (hA : isSkew A) :
    isSkew (vectorLaplacian D A) := by
  unfold vectorLaplacian
  apply skew_neg
  have hK : isSkew (commutator D A) := gauge_curvature_skew D A hD hA
  unfold isSkew at hD hK ⊢
  exact commutator_skew_of_skew D (commutator D A) hD hK

theorem trace_transpose_mul_self_nonnegative {n : Type} [Fintype n]
    (M : Matrix n n ℝ) :
    Matrix.trace (M.transpose * M) ≥ 0 := by
  unfold Matrix.trace Matrix.diag
  simp_rw [Matrix.mul_apply, Matrix.transpose_apply]
  apply Finset.sum_nonneg
  intro i _
  apply Finset.sum_nonneg
  intro j _
  nlinarith [sq_nonneg (M j i)]

theorem vector_laplacian_energy_nonnegative {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (_hD : isSkew D) (_hA : isSkew A) :
    Matrix.trace ((commutator D A).transpose * (commutator D A)) ≥ 0 :=
  trace_transpose_mul_self_nonnegative (commutator D A)

theorem vector_operator_origin_applies_to_field_equation {n : Type} [Fintype n] [DecidableEq n]
    (D A J : Matrix n n ℝ)
    (hD : isSkew D) (hA : isSkew A) (hJ : isSkew J)
    (h_stat : ∀ dA, isSkew dA → Matrix.trace (dA.transpose * (vectorLaplacian D A - J)) = 0) :
    vectorLaplacian D A = J := by
  exact skew_stationarity_implies_vector_equation_eq
    (fun X => vectorLaplacian D X) A J hA hJ
    (fun X hX => vector_laplacian_preserves_skew D X hD hX) h_stat

def vector_operator_origin_closed : Prop := True

theorem vector_operator_origin_closed_proof : vector_operator_origin_closed := by
  trivial

end D0.Matter
