import D0.Algebra.FiniteGramTangent
import Mathlib.Analysis.Calculus.FDeriv.Linear
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Analysis.Matrix.Normed

/-!
# Fréchet derivative of a finite Gram map

This module adds the generic finite-dimensional calculus API for the algebraic
Gram map. It records the full two-sided first variation and makes no geometric
or physical selection claim.
-/

namespace D0.Algebra

open Matrix
noncomputable section

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

local instance : NormedAddCommGroup (Matrix ι ι ℝ) := Matrix.normedAddCommGroup
local instance : NormedSpace ℝ (Matrix ι ι ℝ) := Matrix.normedSpace
local instance : NormedRing (Matrix ι ι ℝ) := Matrix.frobeniusNormedRing
local instance : NormedAlgebra ℝ (Matrix ι ι ℝ) := Matrix.frobeniusNormedAlgebra

/-- Transpose is an isometry for the Frobenius norm on finite square matrices. -/
def finiteMatrixTransposeIsometry :
    Matrix ι ι ℝ ≃ₗᵢ[ℝ] Matrix ι ι ℝ where
  toLinearEquiv :=
    { toFun := Matrix.transpose
      invFun := Matrix.transpose
      left_inv := by intro M; simp
      right_inv := by intro M; simp
      map_add' := by intro M N; exact Matrix.transpose_add M N
      map_smul' := by intro t M; exact Matrix.transpose_smul t M }
  norm_map' := Matrix.frobenius_norm_transpose

@[simp] theorem finiteMatrixTransposeIsometry_apply (M : Matrix ι ι ℝ) :
    finiteMatrixTransposeIsometry.toContinuousLinearEquiv.toContinuousLinearMap M =
      M.transpose := rfl

/-- The Fréchet derivative of `finiteGram η` at `Θ`, with both source terms
retained explicitly. -/
noncomputable def finiteGramTangent (η Θ : Matrix ι ι ℝ) :
    Matrix ι ι ℝ →L[ℝ] Matrix ι ι ℝ :=
  (Θ * η) •
      finiteMatrixTransposeIsometry.toContinuousLinearEquiv.toContinuousLinearMap +
    MulOpposite.op Θ.transpose •
      (ContinuousLinearMap.mul ℝ (Matrix ι ι ℝ)).flip η

@[simp] theorem finiteGramTangent_apply (η Θ H : Matrix ι ι ℝ) :
    finiteGramTangent η Θ H =
      H * η * Θ.transpose + Θ * η * H.transpose := by
  change ((Θ * η) •
      finiteMatrixTransposeIsometry.toContinuousLinearEquiv.toContinuousLinearMap) H +
    (MulOpposite.op Θ.transpose •
      (ContinuousLinearMap.mul ℝ (Matrix ι ι ℝ)).flip η) H = _
  simp only [ContinuousLinearMap.smul_apply,
    finiteMatrixTransposeIsometry_apply, smul_eq_mul, op_smul_eq_mul,
    ContinuousLinearMap.flip_apply, ContinuousLinearMap.mul_apply']
  noncomm_ring

/-- The generic finite Gram map is Fréchet differentiable at every frame.
The derivative contains both the left and right frame variations. -/
theorem finiteGram_hasFDerivAt (η Θ : Matrix ι ι ℝ) :
    HasFDerivAt (fun X : Matrix ι ι ℝ => finiteGram η X)
      (finiteGramTangent η Θ) Θ := by
  have hmul : HasFDerivAt (fun X : Matrix ι ι ℝ => X * η)
      ((ContinuousLinearMap.mul ℝ (Matrix ι ι ℝ)).flip η) Θ := by
    exact (((ContinuousLinearMap.mul ℝ (Matrix ι ι ℝ)).flip η).hasFDerivAt
      (x := Θ))
  have htranspose : HasFDerivAt (fun X : Matrix ι ι ℝ => X.transpose)
      finiteMatrixTransposeIsometry.toContinuousLinearEquiv.toContinuousLinearMap Θ := by
    exact finiteMatrixTransposeIsometry.toContinuousLinearEquiv.hasFDerivAt
      (x := Θ)
  have hproduct := hmul.mul' htranspose
  have hmap : (fun X : Matrix ι ι ℝ => (X * η) * X.transpose) =
      fun X => finiteGram η X := by
    funext X
    rfl
  rw [← hmap]
  convert hproduct using 1

end

end D0.Algebra
