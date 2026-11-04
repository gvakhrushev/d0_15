import D0.Algebra.MovingProjectorPositiveChart
import Mathlib.LinearAlgebra.Matrix.SchurComplement

/-!
# Rectangular clock embedding and the feedback determinant

The determinant reduction used in the clock construction is valid for every
finite rectangular isometry and every small square matrix. The specialized form
uses the defect `1 - Cᴴ * C` and keeps the scalar `z` explicit.

This is an algebraic transport only: the construction and admission of the
owner's `J_f` and `F_clock`, their identification with these matrices, and
physical field variations and maps remain separate premises.
-/

namespace D0.Algebra.IsometricClockDeterminant

open scoped Matrix

variable {κ ι R : Type*} [Fintype κ] [DecidableEq κ] [Fintype ι] [DecidableEq ι]

/-- Determinant transport along a rectangular split embedding. -/
theorem det_one_sub_split_embedding [CommRing R]
    (J : Matrix κ ι R) (L : Matrix ι κ R) (D : Matrix ι ι R)
    (h : L * J = 1) :
    (1 - J * D * L).det = (1 - D).det := by
  calc
    (1 - J * D * L).det = (1 - L * (J * D)).det :=
      Matrix.det_one_sub_mul_comm (J * D) L
    _ = (1 - D).det := by rw [← Matrix.mul_assoc, h, Matrix.one_mul]

/-- An isometric clock embedding preserves the feedback determinant. -/
theorem det_one_sub_isometric_embedding
    (J : Matrix κ ι ℂ) (D : Matrix ι ι ℂ) (hJ : Jᴴ * J = 1) :
    (1 - J * D * Jᴴ).det = (1 - D).det :=
  det_one_sub_split_embedding J Jᴴ D hJ

/-- The `F_clock = J (1 - Cᴴ C) Jᴴ` determinant, with the parameter included. -/
theorem det_clock_defect
    (J : Matrix κ ι ℂ) (C : Matrix ι ι ℂ) (z : ℂ) (hJ : Jᴴ * J = 1) :
    (1 - z • (J * (1 - Cᴴ * C) * Jᴴ)).det =
      ((1 - z) • (1 : Matrix ι ι ℂ) + z • (Cᴴ * C)).det := by
  have h := det_one_sub_isometric_embedding J (z • (1 - Cᴴ * C)) hJ
  have hleft : J * (z • (1 - Cᴴ * C)) * Jᴴ = z • (J * (1 - Cᴴ * C) * Jᴴ) := by
    simp only [Matrix.mul_smul, Matrix.smul_mul]
  have hright : (1 : Matrix ι ι ℂ) - z • (1 - Cᴴ * C) =
      (1 - z) • (1 : Matrix ι ι ℂ) + z • (Cᴴ * C) := by
    simp only [smul_sub, sub_smul, one_smul]
    abel
  rw [hleft, hright] at h
  exact h

/- A concrete 2-by-1 non-isometry: the determinant transport fails. -/
private def nonisometricJ : Matrix (Fin 2) (Fin 1) ℂ := !![2; 0]
private def nonisometricD : Matrix (Fin 1) (Fin 1) ℂ := !![1]

example : nonisometricJᴴ * nonisometricJ ≠ 1 ∧
    (1 - nonisometricJ * nonisometricD * nonisometricJᴴ).det = -3 ∧
    (1 - nonisometricD).det = 0 := by
  constructor
  · intro h
    have hh := congrArg (fun M : Matrix (Fin 1) (Fin 1) ℂ => M 0 0) h
    norm_num [nonisometricJ, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Fin.sum_univ_two, map_ofNat] at hh
  · norm_num [nonisometricJ, nonisometricD, Matrix.det_fin_one, Matrix.det_fin_two,
      Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_one, Fin.sum_univ_two,
      Matrix.vecMul, dotProduct, map_ofNat]

end D0.Algebra.IsometricClockDeterminant
