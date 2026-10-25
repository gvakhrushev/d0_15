import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Kronecker

/-!
# Generic finite matrix tensor products

This module provides stable D0 names for finite matrix algebra on product
carriers. The tensor constructor delegates to Mathlib's `Matrix.kronecker`;
CAR-specific identities remain here without geometric or physical
interpretation.
-/

namespace D0.Algebra

open BigOperators Matrix

/-- Entrywise tensor product of two finite square matrices, acting on the
product carrier. -/
abbrev finiteMatrixTensorProduct {X Y R : Type*}
    [Mul R]
    (A : Matrix X X R) (B : Matrix Y Y R) :
    Matrix (X × Y) (X × Y) R :=
  Matrix.kronecker A B

/-- Matrix multiplication distributes across the two factors of the finite
matrix tensor product. -/
theorem finiteMatrixTensorProduct_mul {X Y R : Type*}
    [Fintype X] [Fintype Y] [CommSemiring R]
    (A C : Matrix X X R) (B D : Matrix Y Y R) :
    finiteMatrixTensorProduct A B * finiteMatrixTensorProduct C D =
      finiteMatrixTensorProduct (A * C) (B * D) := by
  exact (Matrix.mul_kronecker_mul A C B D).symm

/-- Transposition acts factorwise on the finite matrix tensor product. -/
theorem finiteMatrixTensorProduct_transpose {X Y R : Type*}
    [Fintype X] [Fintype Y] [Mul R]
    (A : Matrix X X R) (B : Matrix Y Y R) :
    (finiteMatrixTensorProduct A B).transpose =
      finiteMatrixTensorProduct A.transpose B.transpose := by
  exact (Matrix.kroneckerMap_transpose (· * ·) A B).symm

/-- Additivity in the second matrix factor. -/
theorem finiteMatrixTensorProduct_add_right {X Y R : Type*}
    [Fintype X] [Fintype Y] [Semiring R]
    (A : Matrix X X R) (B C : Matrix Y Y R) :
    finiteMatrixTensorProduct A (B + C) =
      finiteMatrixTensorProduct A B + finiteMatrixTensorProduct A C := by
  exact Matrix.kronecker_add A B C

/-- Scalar compatibility in the second matrix factor. -/
theorem finiteMatrixTensorProduct_smul_right {X Y R : Type*}
    [Fintype X] [Fintype Y] [CommSemiring R]
    (A : Matrix X X R) (c : R) (B : Matrix Y Y R) :
    finiteMatrixTensorProduct A (c • B) =
      c • finiteMatrixTensorProduct A B := by
  exact Matrix.kronecker_smul c A B

/-- The tensor product of identity matrices is the identity on the product
carrier. -/
theorem finiteMatrixTensorProduct_one {X Y R : Type*}
    [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y] [Semiring R] :
    finiteMatrixTensorProduct (1 : Matrix X X R) (1 : Matrix Y Y R) =
      (1 : Matrix (X × Y) (X × Y) R) := by
  exact Matrix.one_kronecker_one

/-- The trace of `1 ⊗ B` is the first-factor cardinality times the trace of
`B`. This keeps trace calculations on product carriers in the shared tensor
API instead of repeating the coordinate sum in each application. -/
theorem finiteMatrixTensorProduct_trace_one_left {X Y R : Type*}
    [Fintype X] [Fintype Y] [DecidableEq X] [Semiring R]
    (B : Matrix Y Y R) :
    Matrix.trace (finiteMatrixTensorProduct (1 : Matrix X X R) B) =
      Fintype.card X • Matrix.trace B := by
  change Matrix.trace (Matrix.kroneckerMap (· * ·) (1 : Matrix X X R) B) = _
  rw [Matrix.trace_kronecker, Matrix.trace_one]
  simp [nsmul_eq_mul]

/-- If the first-factor matrices commute and the second-factor matrices
anticommute with a Kronecker delta, the double tensor-product sum collapses to
its diagonal. This is a generic finite Clifford-square identity. -/
theorem finiteMatrixTensorProduct_sum_square_eq_diagonal
    {ι X Y : Type*} [Fintype ι] [DecidableEq ι] [Fintype X] [Fintype Y]
    (A : ι → Matrix X X ℝ) (G : ι → Matrix Y Y ℝ)
    (J : Matrix Y Y ℝ)
    (hAcomm : ∀ i j, A i * A j = A j * A i)
    (hGanti : ∀ i j,
      G i * G j + G j * G i = (if i = j then (2 : ℝ) else 0) • J) :
    (∑ i : ι, ∑ j : ι,
      finiteMatrixTensorProduct (A i * A j) (G i * G j)) =
      ∑ i : ι, finiteMatrixTensorProduct (A i * A i) J := by
  let S : Matrix (X × Y) (X × Y) ℝ :=
    ∑ i : ι, ∑ j : ι,
      finiteMatrixTensorProduct (A i * A j) (G i * G j)
  let T : Matrix (X × Y) (X × Y) ℝ :=
    ∑ i : ι, ∑ j : ι,
      finiteMatrixTensorProduct (A i * A j) (G j * G i)
  let Q : Matrix (X × Y) (X × Y) ℝ :=
    ∑ i : ι, finiteMatrixTensorProduct (A i * A i) J
  have hswap : S = T := by
    dsimp [S, T]
    calc
      (∑ i : ι, ∑ j : ι,
        finiteMatrixTensorProduct (A i * A j) (G i * G j)) =
          ∑ j : ι, ∑ i : ι,
            finiteMatrixTensorProduct (A i * A j) (G i * G j) := Finset.sum_comm
      _ = ∑ i : ι, ∑ j : ι,
            finiteMatrixTensorProduct (A i * A j) (G j * G i) := by
        apply Finset.sum_congr rfl
        intro i hi
        apply Finset.sum_congr rfl
        intro j hj
        rw [hAcomm j i]
  have hcombine : S + T =
      ∑ i : ι, ∑ j : ι,
        finiteMatrixTensorProduct (A i * A j) (G i * G j + G j * G i) := by
    dsimp [S, T]
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j hj
    exact (finiteMatrixTensorProduct_add_right (A i * A j)
      (G i * G j) (G j * G i)).symm
  have hreduce :
      (∑ i : ι, ∑ j : ι,
        finiteMatrixTensorProduct (A i * A j) (G i * G j + G j * G i)) =
        2 • Q := by
    dsimp [Q]
    simp_rw [hGanti, finiteMatrixTensorProduct_smul_right]
    simp [Finset.sum_add_distrib, two_smul]
  have hdouble : S + S = 2 • Q := by
    calc
      S + S = S + T := by rw [hswap]
      _ = 2 • Q := hcombine.trans hreduce
  ext i j
  have hentry := congrArg (fun M : Matrix (X × Y) (X × Y) ℝ => M i j) hdouble
  simp only [Matrix.add_apply, two_smul] at hentry
  nlinarith

end D0.Algebra
