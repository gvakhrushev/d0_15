import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import D0.Algebra.FiniteMatrixTensorProduct

open scoped BigOperators

/-!
# Finite matrix partial trace

The left-factor partial trace and its interaction with operators on the retained
factor are generic finite matrix identities. They do not select a state,
weight, or physical interpretation.
-/

namespace D0.Algebra

/-- Trace out the first factor of a product-carrier matrix. -/
def finiteMatrixPartialTraceLeft {V N R : Type*} [Fintype V]
    [AddCommMonoid R] (M : Matrix (V × N) (V × N) R) : Matrix N N R :=
  fun i j => ∑ v, M (v, i) (v, j)

/-- Taking the partial trace over the first factor preserves the full trace. -/
theorem finiteMatrixPartialTraceLeft_trace {V N R : Type*}
    [Fintype V] [Fintype N] [AddCommMonoid R]
    (M : Matrix (V × N) (V × N) R) :
    Matrix.trace (finiteMatrixPartialTraceLeft M) = Matrix.trace M := by
  unfold Matrix.trace finiteMatrixPartialTraceLeft Matrix.diag
  dsimp
  rw [Fintype.sum_prod_type]
  rw [Finset.sum_comm]

/-- Tracing out the left factor of a tensor product returns the trace of
that factor times the retained operator. -/
theorem finiteMatrixPartialTraceLeft_tensorProduct
    {V N R : Type*} [Fintype V] [CommSemiring R]
    (A : Matrix V V R) (B : Matrix N N R) :
    finiteMatrixPartialTraceLeft (finiteMatrixTensorProduct A B) =
      Matrix.trace A • B := by
  ext i j
  simp [finiteMatrixPartialTraceLeft, finiteMatrixTensorProduct,
    Matrix.trace, Matrix.diag, Finset.sum_mul]

/-- If a product-carrier operator commutes with `1 ⊗ C`, its partial trace
over the first factor commutes with `C`. -/
theorem finiteMatrixPartialTraceLeft_commutes_rightTensor
    {V N R : Type*} [Fintype V] [DecidableEq V]
    [Fintype N] [CommSemiring R]
    (M : Matrix (V × N) (V × N) R) (C : Matrix N N R)
    (h_comm :
      M * finiteMatrixTensorProduct (1 : Matrix V V R) C =
        finiteMatrixTensorProduct (1 : Matrix V V R) C * M) :
    finiteMatrixPartialTraceLeft M * C = C * finiteMatrixPartialTraceLeft M := by
  ext n1 n3
  unfold finiteMatrixPartialTraceLeft
  have h_eq : ∀ v : V,
      (∑ n2, M (v, n1) (v, n2) * C n2 n3) =
        ∑ n2, C n1 n2 * M (v, n2) (v, n3) := by
    intro v
    have h_comm_v := congr_fun (congr_fun h_comm (v, n1)) (v, n3)
    rw [Matrix.mul_apply, Matrix.mul_apply] at h_comm_v
    change
      (∑ x : V × N,
        M (v, n1) x *
          ((1 : Matrix V V R) x.1 v * C x.2 n3)) =
      (∑ x : V × N,
        ((1 : Matrix V V R) v x.1 * C n1 x.2) * M x (v, n3)) at h_comm_v
    simp only [Matrix.one_apply] at h_comm_v
    have h_lhs :
        (∑ x : V × N,
          M (v, n1) x *
            ((if x.1 = v then (1 : R) else 0) * C x.2 n3)) =
          ∑ n2, M (v, n1) (v, n2) * C n2 n3 := by
      rw [Fintype.sum_prod_type]
      dsimp
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro n2 _
      rw [Finset.sum_eq_single v]
      · simp
      · intro v2 _ hne
        simp [hne]
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    have h_rhs :
        (∑ x : V × N,
          ((if v = x.1 then (1 : R) else 0) * C n1 x.2) * M x (v, n3)) =
          ∑ n2, C n1 n2 * M (v, n2) (v, n3) := by
      rw [Fintype.sum_prod_type]
      dsimp
      rw [Finset.sum_eq_single v]
      · simp
      · intro v2 _ hne
        simp [hne.symm]
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    rw [h_lhs, h_rhs] at h_comm_v
    exact h_comm_v
  rw [Matrix.mul_apply, Matrix.mul_apply]
  have h_sum_comm :
      (∑ n2 : N, (∑ v : V, M (v, n1) (v, n2)) * C n2 n3) =
        ∑ v : V, ∑ n2 : N, M (v, n1) (v, n2) * C n2 n3 := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro v _
    rw [Finset.sum_mul]
  have h_sum_comm2 :
      (∑ n2 : N, C n1 n2 * ∑ v : V, M (v, n2) (v, n3)) =
        ∑ v : V, ∑ n2 : N, C n1 n2 * M (v, n2) (v, n3) := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
  rw [h_sum_comm, h_sum_comm2]
  apply Finset.sum_congr rfl
  intro v _
  exact h_eq v

end D0.Algebra
