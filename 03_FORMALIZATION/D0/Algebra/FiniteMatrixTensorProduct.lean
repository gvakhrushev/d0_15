import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# Generic finite matrix tensor products

This module owns finite matrix algebra for product carriers. It is independent
of any geometric or physical interpretation; concrete operators may retain
compatibility aliases in their domain modules.
-/

namespace D0.Algebra

open BigOperators Matrix

/-- Entrywise tensor product of two finite square matrices, acting on the
product carrier. -/
def finiteMatrixTensorProduct {X Y R : Type*}
    [Fintype X] [Fintype Y] [Mul R]
    (A : Matrix X X R) (B : Matrix Y Y R) :
    Matrix (X × Y) (X × Y) R :=
  fun ⟨x₁, y₁⟩ ⟨x₂, y₂⟩ => A x₁ x₂ * B y₁ y₂

/-- Matrix multiplication distributes across the two factors of the finite
matrix tensor product. -/
theorem finiteMatrixTensorProduct_mul {X Y R : Type*}
    [Fintype X] [Fintype Y] [CommSemiring R]
    (A C : Matrix X X R) (B D : Matrix Y Y R) :
    finiteMatrixTensorProduct A B * finiteMatrixTensorProduct C D =
      finiteMatrixTensorProduct (A * C) (B * D) := by
  ext ⟨x, f⟩ ⟨y, g⟩
  simp only [Matrix.mul_apply, finiteMatrixTensorProduct]
  have h_sum_split :
      (∑ mid : X × Y, A x mid.1 * B f mid.2 * (C mid.1 y * D mid.2 g)) =
        ∑ a : X, ∑ b : Y, A x a * B f b * (C a y * D b g) := by
    exact Fintype.sum_prod_type
      (fun p : X × Y => A x p.1 * B f p.2 * (C p.1 y * D p.2 g))
  rw [h_sum_split]
  have h_factor :
      (∑ a : X, ∑ b : Y, A x a * B f b * (C a y * D b g)) =
        (∑ a : X, A x a * C a y) * (∑ b : Y, B f b * D b g) := by
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro a _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro b _
    ring
  rw [h_factor]

/-- Additivity in the second matrix factor. -/
theorem finiteMatrixTensorProduct_add_right {X Y R : Type*}
    [Fintype X] [Fintype Y] [Semiring R]
    (A : Matrix X X R) (B C : Matrix Y Y R) :
    finiteMatrixTensorProduct A (B + C) =
      finiteMatrixTensorProduct A B + finiteMatrixTensorProduct A C := by
  ext ⟨x, f⟩ ⟨y, g⟩
  simp [finiteMatrixTensorProduct, mul_add]

/-- Scalar compatibility in the second matrix factor. -/
theorem finiteMatrixTensorProduct_smul_right {X Y R : Type*}
    [Fintype X] [Fintype Y] [CommSemiring R]
    (A : Matrix X X R) (c : R) (B : Matrix Y Y R) :
    finiteMatrixTensorProduct A (c • B) =
      c • finiteMatrixTensorProduct A B := by
  ext ⟨x, f⟩ ⟨y, g⟩
  simp [finiteMatrixTensorProduct, smul_eq_mul, mul_left_comm]

/-- The tensor product of identity matrices is the identity on the product
carrier. -/
theorem finiteMatrixTensorProduct_one {X Y R : Type*}
    [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y] [Semiring R] :
    finiteMatrixTensorProduct (1 : Matrix X X R) (1 : Matrix Y Y R) =
      (1 : Matrix (X × Y) (X × Y) R) := by
  ext ⟨x, y⟩ ⟨x', y'⟩
  by_cases hX : x = x' <;> by_cases hY : y = y' <;>
    simp [finiteMatrixTensorProduct, Matrix.one_apply, hX, hY]

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
