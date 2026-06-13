import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveActionFunctional

open scoped BigOperators

namespace D0

def matrixInnerProduct {A B : Type} [Fintype A] [Fintype B]
    (M N : Matrix A B ℝ) : ℝ :=
  ∑ i : A, ∑ j : B, M i j * N i j

def matrixHSSquared {A B : Type} [Fintype A] [Fintype B]
    (M : Matrix A B ℝ) : ℝ :=
  matrixInnerProduct M M

theorem matrixHSSquared_nonnegative {A B : Type} [Fintype A] [Fintype B]
    (M : Matrix A B ℝ) :
    0 ≤ matrixHSSquared M := by
  unfold matrixHSSquared matrixInnerProduct
  apply Finset.sum_nonneg
  intro i _hi
  apply Finset.sum_nonneg
  intro j _hj
  nlinarith [sq_nonneg (M i j)]

def matrixAddScaled {A B : Type} (M N : Matrix A B ℝ) (eps : ℝ) :
    Matrix A B ℝ :=
  fun i j => M i j + eps * N i j

theorem matrix_hs_square_expansion {A B : Type} [Fintype A] [Fintype B]
    (M N : Matrix A B ℝ) (eps : ℝ) :
    matrixHSSquared (matrixAddScaled M N eps) =
      matrixHSSquared M + 2 * eps * matrixInnerProduct M N +
        eps^2 * matrixHSSquared N := by
  unfold matrixHSSquared matrixInnerProduct matrixAddScaled
  calc
    (∑ i : A, ∑ j : B,
        (M i j + eps * N i j) * (M i j + eps * N i j)) =
        ∑ i : A, ∑ j : B,
          (M i j * M i j + 2 * eps * (M i j * N i j) +
            eps^2 * (N i j * N i j)) := by
      apply Finset.sum_congr rfl
      intro i _hi
      apply Finset.sum_congr rfl
      intro j _hj
      ring
    _ =
        (∑ i : A, ∑ j : B, M i j * M i j) +
          2 * eps * (∑ i : A, ∑ j : B, M i j * N i j) +
          eps^2 * (∑ i : A, ∑ j : B, N i j * N i j) := by
      simp_rw [Finset.sum_add_distrib]
      simp_rw [← Finset.mul_sum]

structure LaplacianVariation (n : Nat) where
  dL : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ
  symmetric : MatrixSymmetric dL
  row_sum_zero : ∀ i, ∑ j : archivePhaseIndex n, dL i j = 0
  local_support : Prop

def seamCommutatorVariation (n : Nat) (δ : LaplacianVariation n) :
    Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex n) ℝ :=
  - rectangularMatrixMul (archiveLiftOperator n) δ.dL

def firstVariationSeamAction (n : Nat) (δ : LaplacianVariation n) : ℝ :=
  2 * matrixInnerProduct (seamCommutator n) (seamCommutatorVariation n δ)

def derivative_of_trace_square_form (n : Nat) (δ : LaplacianVariation n) : ℝ :=
  2 * matrixInnerProduct (seamCommutator n) (seamCommutatorVariation n δ)

theorem first_variation_trace_square (n : Nat) (δ : LaplacianVariation n) :
    firstVariationSeamAction n δ = derivative_of_trace_square_form n δ := by
  rfl

def variedSeamCommutator (n : Nat) (δ : LaplacianVariation n) (eps : ℝ) :
    Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex n) ℝ :=
  matrixAddScaled (seamCommutator n) (seamCommutatorVariation n δ) eps

theorem seam_action_variation_quadratic_expansion
    (n : Nat) (δ : LaplacianVariation n) (eps : ℝ) :
    matrixHSSquared (variedSeamCommutator n δ eps) =
      matrixHSSquared (seamCommutator n) +
        eps * firstVariationSeamAction n δ +
        eps^2 * matrixHSSquared (seamCommutatorVariation n δ) := by
  unfold variedSeamCommutator firstVariationSeamAction
  rw [matrix_hs_square_expansion]
  ring

def ArchiveStationary (n : Nat) : Prop :=
  ∀ δ : LaplacianVariation n, firstVariationSeamAction n δ = 0

theorem stationary_iff_first_variation_zero (n : Nat) :
    ArchiveStationary n ↔
      ∀ δ : LaplacianVariation n, firstVariationSeamAction n δ = 0 := by
  rfl

end D0
