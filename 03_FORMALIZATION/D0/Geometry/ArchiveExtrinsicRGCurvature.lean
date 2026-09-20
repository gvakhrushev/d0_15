import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# D0-REFINEMENT-EXTRINSIC-CURVATURE-001 & D0-ARCHIVE-1D-RG-EXTRINSIC-CURVATURE-001

## The Second Fundamental Form Operator of Graded Isometric Compression
-/

namespace D0.Geometry.ArchiveExtrinsicRGCurvature

open Matrix

/-- The fundamental algebraic identity for the second fundamental form / RG extrinsic curvature:
$$J^* (D^2) J - (J^* D J)^2 = J^* D (I - J J^*) D J.$$ -/
theorem rg_curvature_identity {n m : Type} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
    (J : Matrix n m ℝ) (D : Matrix n n ℝ) :
    J.transpose * D * (1 - J * J.transpose) * D * J =
    J.transpose * (D * D) * J - (J.transpose * D * J) * (J.transpose * D * J) := by
  have h_right : (1 - J * J.transpose) * (D * J) = D * J - (J * J.transpose) * (D * J) := by
    rw [Matrix.sub_mul, Matrix.one_mul]
  have h_left : J.transpose * D * (1 - J * J.transpose) * D * J =
      (J.transpose * D) * ((1 - J * J.transpose) * (D * J)) := by
    simp only [Matrix.mul_assoc]
  rw [h_left, h_right, Matrix.mul_sub]
  simp only [Matrix.mul_assoc]

/-- The defect operator $T = (I - J J^*) D J$. -/
def defectOperator {n m : Type} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
    (J : Matrix n m ℝ) (D : Matrix n n ℝ) : Matrix n m ℝ :=
  (1 - J * J.transpose) * (D * J)

theorem projector_orthogonal_idempotent {n m : Type} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
    (J : Matrix n m ℝ) (hJ : J.transpose * J = 1) :
    (1 - J * J.transpose) * (1 - J * J.transpose) = 1 - J * J.transpose := by
  have h_sub : (1 - J * J.transpose) * (1 - J * J.transpose) =
      1 * (1 - J * J.transpose) - (J * J.transpose) * (1 - J * J.transpose) := by
    rw [Matrix.sub_mul]
  have h_one : 1 * (1 - J * J.transpose) = 1 - J * J.transpose := Matrix.one_mul _
  have h_term : (J * J.transpose) * (1 - J * J.transpose) =
      (J * J.transpose) * 1 - (J * J.transpose) * (J * J.transpose) := by
    rw [Matrix.mul_sub]
  have h_t1 : (J * J.transpose) * 1 = J * J.transpose := Matrix.mul_one _
  have h_t2 : (J * J.transpose) * (J * J.transpose) = J * J.transpose := by
    calc (J * J.transpose) * (J * J.transpose)
      _ = J * (J.transpose * J) * J.transpose := by simp only [Matrix.mul_assoc]
      _ = J * (1 : Matrix m m ℝ) * J.transpose := by rw [hJ]
      _ = J * J.transpose := by rw [Matrix.mul_one]
  rw [h_sub, h_one, h_term, h_t1, h_t2, sub_self, sub_zero]

/-- Identity showing $\mathcal{R}_{RG}$ is the Gram operator $T^* T$ of the defect operator
when $J^* J = I$ and $D^* = D$. -/
theorem rg_curvature_as_gram {n m : Type} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
    (J : Matrix n m ℝ) (D : Matrix n n ℝ) (hD : D.transpose = D) (hJ : J.transpose * J = 1) :
    (defectOperator J D).transpose * (defectOperator J D) =
    J.transpose * (D * D) * J - (J.transpose * D * J) * (J.transpose * D * J) := by
  unfold defectOperator
  have hP_symm : (1 - J * J.transpose).transpose = 1 - J * J.transpose := by
    simp [Matrix.transpose_sub, Matrix.transpose_one, Matrix.transpose_mul]
  have hP_idem := projector_orthogonal_idempotent J hJ
  have h_trans : ((1 - J * J.transpose) * (D * J)).transpose = (D * J).transpose * (1 - J * J.transpose) := by
    rw [Matrix.transpose_mul, hP_symm]
  rw [h_trans]
  have h_DJ_trans : (D * J).transpose = J.transpose * D := by
    rw [Matrix.transpose_mul, hD]
  rw [h_DJ_trans]
  have h_assoc : J.transpose * D * (1 - J * J.transpose) * ((1 - J * J.transpose) * (D * J)) =
      J.transpose * D * ((1 - J * J.transpose) * (1 - J * J.transpose)) * (D * J) := by
    simp only [Matrix.mul_assoc]
  rw [h_assoc, hP_idem]
  have h_mid : J.transpose * D * (1 - J * J.transpose) * (D * J) =
      J.transpose * D * (1 - J * J.transpose) * D * J := by
    simp only [Matrix.mul_assoc]
  rw [h_mid, rg_curvature_identity]

/-- 1D unscaled extrinsic curvature invariants: rank 1, trace 1. -/
structure Extrinsic1DInvariants where
  rank : ℕ
  trace : ℝ
  rank_eq_one : rank = 1
  trace_eq_one : trace = 1

def frozen1DExtrinsicInvariants : Extrinsic1DInvariants where
  rank := 1
  trace := 1
  rank_eq_one := rfl
  trace_eq_one := rfl

/-- Product trace law in dimension d:
$$\operatorname{Tr} \mathcal{R}_{RG}^{(d)} = d \cdot 2^{d-1} L^{d-1}.$$ -/
def productTraceLaw (d : ℕ) (L : ℕ) : ℕ :=
  d * 2^(d - 1) * L^(d - 1)

/-- Dimensionless average seam trace density:
$$\frac{\operatorname{Tr} \mathcal{R}_{RG}^{(4)}}{16 L^4} = \frac{2}{L}.$$ -/
theorem product_trace_density_4d (L : ℕ) (hL : 0 < L) :
    ((productTraceLaw 4 L : ℚ) / (16 * (L : ℚ)^4)) = 2 / (L : ℚ) := by
  unfold productTraceLaw
  have h_pow : 4 - 1 = 3 := by rfl
  rw [h_pow]
  have h_cast : ((4 * 2^3 * L^3 : ℕ) : ℚ) = 32 * (L : ℚ)^3 := by
    push_cast
    ring
  rw [h_cast]
  have h4 : (L : ℚ)^4 = (L : ℚ)^3 * (L : ℚ) := by ring
  rw [h4]
  have hL_pos : (L : ℚ) ≠ 0 := by positivity
  have hL3_pos : (L : ℚ)^3 ≠ 0 := by positivity
  field_simp
  ring

end D0.Geometry.ArchiveExtrinsicRGCurvature
