import D0.Geometry.OriginalBookMovedJuliaLeft
import Mathlib.Analysis.Matrix.Order
import Mathlib.Tactic

/-!
Exact moved-D right defect from the original 128-Kraus checker at commit
eebcb5e467742df3e9cf7fa9702042d7294aa742, blobs
`ee8de4635d24c668949ac9a0186616ab7d59f2ed` and
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`.
The matrices below derive from the previously verified original creator and
boost; no spectrum or root is assumed. The actual complex right defect is
strictly positive and has the uniquely determined nonnegative CFC square root.
The exact rational numerator has four signed 2×2 blocks with entries 1681,
±369, 81 and satisfies J²=1762J. No 128 Kraus operator, effect-span result,
or physical admission is derived here.
-/
open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookMovedJuliaLeft
open D0.Geometry.CubicExponential
open Matrix
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OriginalBookMovedJuliaRight

/-- The diagonal projector for four unboosted nonzero modes. -/
def regularInt : SourceMatrix := fun bra ket =>
  if bra = ket ∧ (ket = 0 ∨ ket = 4 ∨ ket = 8 ∨ ket = 12) then 1 else 0

/-- Numerator of the four exact rank-one boosted projectors. -/
def blockNumeratorInt : SourceMatrix := fun bra ket =>
  if bra = ket ∧ (ket = 1 ∨ ket = 5 ∨ ket = 9 ∨ ket = 13) then 1681
  else if bra = ket ∧ (ket = 2 ∨ ket = 6 ∨ ket = 10 ∨ ket = 14) then 81
  else if (bra = 1 ∧ ket = 2) ∨ (bra = 2 ∧ ket = 1) ∨
      (bra = 13 ∧ ket = 14) ∨ (bra = 14 ∧ ket = 13) then 369
  else if (bra = 5 ∧ ket = 6) ∨ (bra = 6 ∧ ket = 5) ∨
      (bra = 9 ∧ ket = 10) ∨ (bra = 10 ∧ ket = 9) then -369
  else 0

set_option maxRecDepth 100000 in
private theorem gram_ket_0 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (0 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (0 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (0 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (0 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_1 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (1 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (1 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (1 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (1 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_2 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (2 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (2 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (2 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (2 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_3 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (3 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (3 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (3 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (3 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_4 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (4 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (4 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (4 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (4 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_5 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (5 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (5 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (5 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (5 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_6 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (6 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (6 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (6 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (6 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_7 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (7 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (7 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (7 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (7 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_8 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (8 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (8 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (8 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (8 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_9 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (9 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (9 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (9 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (9 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_10 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (10 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (10 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (10 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (10 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_11 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (11 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (11 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (11 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (11 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_12 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (12 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (12 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (12 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (12 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_13 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (13 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (13 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (13 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (13 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_14 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (14 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (14 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (14 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (14 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem gram_ket_15 : ∀ bra : Fin 16,
    (sparseFortyMoved.transpose * sparseFortyMoved) bra (15 : Fin 16) =
      ((1600 : ℤ) • regularInt + blockNumeratorInt) bra (15 : Fin 16) ∧
    (blockNumeratorInt * blockNumeratorInt) bra (15 : Fin 16) =
      ((1762 : ℤ) • blockNumeratorInt) bra (15 : Fin 16) := by
  decide

theorem sourceRightGram :
    fortyMoved.transpose * fortyMoved = (1600 : ℤ) • regularInt + blockNumeratorInt := by
  rw [fortyMoved_eq_sparse]
  ext bra ket
  fin_cases ket
  · exact (gram_ket_0 bra).1
  · exact (gram_ket_1 bra).1
  · exact (gram_ket_2 bra).1
  · exact (gram_ket_3 bra).1
  · exact (gram_ket_4 bra).1
  · exact (gram_ket_5 bra).1
  · exact (gram_ket_6 bra).1
  · exact (gram_ket_7 bra).1
  · exact (gram_ket_8 bra).1
  · exact (gram_ket_9 bra).1
  · exact (gram_ket_10 bra).1
  · exact (gram_ket_11 bra).1
  · exact (gram_ket_12 bra).1
  · exact (gram_ket_13 bra).1
  · exact (gram_ket_14 bra).1
  · exact (gram_ket_15 bra).1

theorem blockNumeratorInt_sq :
    blockNumeratorInt * blockNumeratorInt = (1762 : ℤ) • blockNumeratorInt := by
  ext bra ket
  fin_cases ket
  · exact (gram_ket_0 bra).2
  · exact (gram_ket_1 bra).2
  · exact (gram_ket_2 bra).2
  · exact (gram_ket_3 bra).2
  · exact (gram_ket_4 bra).2
  · exact (gram_ket_5 bra).2
  · exact (gram_ket_6 bra).2
  · exact (gram_ket_7 bra).2
  · exact (gram_ket_8 bra).2
  · exact (gram_ket_9 bra).2
  · exact (gram_ket_10 bra).2
  · exact (gram_ket_11 bra).2
  · exact (gram_ket_12 bra).2
  · exact (gram_ket_13 bra).2
  · exact (gram_ket_14 bra).2
  · exact (gram_ket_15 bra).2
set_option maxRecDepth 100000 in
private theorem orthogonal_ket_0 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (0 : Fin 16) = regularInt bra (0 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (0 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (0 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_1 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (1 : Fin 16) = regularInt bra (1 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (1 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (1 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_2 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (2 : Fin 16) = regularInt bra (2 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (2 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (2 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_3 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (3 : Fin 16) = regularInt bra (3 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (3 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (3 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_4 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (4 : Fin 16) = regularInt bra (4 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (4 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (4 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_5 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (5 : Fin 16) = regularInt bra (5 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (5 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (5 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_6 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (6 : Fin 16) = regularInt bra (6 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (6 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (6 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_7 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (7 : Fin 16) = regularInt bra (7 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (7 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (7 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_8 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (8 : Fin 16) = regularInt bra (8 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (8 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (8 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_9 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (9 : Fin 16) = regularInt bra (9 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (9 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (9 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_10 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (10 : Fin 16) = regularInt bra (10 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (10 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (10 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_11 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (11 : Fin 16) = regularInt bra (11 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (11 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (11 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_12 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (12 : Fin 16) = regularInt bra (12 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (12 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (12 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_13 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (13 : Fin 16) = regularInt bra (13 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (13 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (13 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_14 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (14 : Fin 16) = regularInt bra (14 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (14 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (14 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem orthogonal_ket_15 : ∀ bra : Fin 16,
    (regularInt * regularInt) bra (15 : Fin 16) = regularInt bra (15 : Fin 16) ∧
    (regularInt * blockNumeratorInt) bra (15 : Fin 16) = 0 ∧
    (blockNumeratorInt * regularInt) bra (15 : Fin 16) = 0 := by
  decide

theorem regularInt_sq : regularInt * regularInt = regularInt := by
  ext bra ket
  fin_cases ket
  · exact (orthogonal_ket_0 bra).1
  · exact (orthogonal_ket_1 bra).1
  · exact (orthogonal_ket_2 bra).1
  · exact (orthogonal_ket_3 bra).1
  · exact (orthogonal_ket_4 bra).1
  · exact (orthogonal_ket_5 bra).1
  · exact (orthogonal_ket_6 bra).1
  · exact (orthogonal_ket_7 bra).1
  · exact (orthogonal_ket_8 bra).1
  · exact (orthogonal_ket_9 bra).1
  · exact (orthogonal_ket_10 bra).1
  · exact (orthogonal_ket_11 bra).1
  · exact (orthogonal_ket_12 bra).1
  · exact (orthogonal_ket_13 bra).1
  · exact (orthogonal_ket_14 bra).1
  · exact (orthogonal_ket_15 bra).1

theorem regularInt_block_mul_zero : regularInt * blockNumeratorInt = 0 := by
  ext bra ket
  fin_cases ket
  · exact (orthogonal_ket_0 bra).2.1
  · exact (orthogonal_ket_1 bra).2.1
  · exact (orthogonal_ket_2 bra).2.1
  · exact (orthogonal_ket_3 bra).2.1
  · exact (orthogonal_ket_4 bra).2.1
  · exact (orthogonal_ket_5 bra).2.1
  · exact (orthogonal_ket_6 bra).2.1
  · exact (orthogonal_ket_7 bra).2.1
  · exact (orthogonal_ket_8 bra).2.1
  · exact (orthogonal_ket_9 bra).2.1
  · exact (orthogonal_ket_10 bra).2.1
  · exact (orthogonal_ket_11 bra).2.1
  · exact (orthogonal_ket_12 bra).2.1
  · exact (orthogonal_ket_13 bra).2.1
  · exact (orthogonal_ket_14 bra).2.1
  · exact (orthogonal_ket_15 bra).2.1

theorem block_regularInt_mul_zero : blockNumeratorInt * regularInt = 0 := by
  ext bra ket
  fin_cases ket
  · exact (orthogonal_ket_0 bra).2.2
  · exact (orthogonal_ket_1 bra).2.2
  · exact (orthogonal_ket_2 bra).2.2
  · exact (orthogonal_ket_3 bra).2.2
  · exact (orthogonal_ket_4 bra).2.2
  · exact (orthogonal_ket_5 bra).2.2
  · exact (orthogonal_ket_6 bra).2.2
  · exact (orthogonal_ket_7 bra).2.2
  · exact (orthogonal_ket_8 bra).2.2
  · exact (orthogonal_ket_9 bra).2.2
  · exact (orthogonal_ket_10 bra).2.2
  · exact (orthogonal_ket_11 bra).2.2
  · exact (orthogonal_ket_12 bra).2.2
  · exact (orthogonal_ket_13 bra).2.2
  · exact (orthogonal_ket_14 bra).2.2
  · exact (orthogonal_ket_15 bra).2.2

set_option maxRecDepth 100000 in
theorem regularInt_transpose : regularInt.transpose = regularInt := by
  ext bra ket
  revert bra ket
  decide

set_option maxRecDepth 100000 in
theorem blockNumeratorInt_transpose : blockNumeratorInt.transpose = blockNumeratorInt := by
  ext bra ket
  revert bra ket
  decide

end D0.Geometry.OriginalBookMovedJuliaRight


open Matrix
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OrthogonalProjectionRoot
variable {n : Type*} [Fintype n] [DecidableEq n]

noncomputable def coefficient : ℝ := Real.sqrt (12071 / 20000)

lemma coefficient_pos : 0 < coefficient := by
  unfold coefficient
  exact Real.sqrt_pos.2 (by norm_num)

lemma coefficient_sq : coefficient * coefficient = 12071 / 20000 := by
  unfold coefficient
  exact Real.mul_self_sqrt (by norm_num)

omit [DecidableEq n] in
lemma projection_nonneg (p : Matrix n n ℂ) (hh : pᴴ = p) (hp : p * p = p) : 0 ≤ p := by
  have h := (Matrix.posSemidef_conjTranspose_mul_self p).nonneg
  simpa [hh, hp] using h

variable (p q : Matrix n n ℂ)
variable (hp : p * p = p) (hq : q * q = q) (hpq : p * q = 0) (hqp : q * p = 0)
variable (hph : pᴴ = p) (hqh : qᴴ = q)

noncomputable def residual : Matrix n n ℂ := 1 - p - q
noncomputable def rootCandidate : Matrix n n ℂ := residual p q + (4 / 5 : ℝ) • p + coefficient • q
noncomputable def defectCandidate : Matrix n n ℂ := residual p q + (16 / 25 : ℝ) • p + (12071 / 20000 : ℝ) • q

omit [Fintype n] in
lemma residual_hermitian (hph : pᴴ = p) (hqh : qᴴ = q) : (residual p q)ᴴ = residual p q := by
  simp [residual, hph, hqh]

lemma residual_sq (hp : p * p = p) (hq : q * q = q) (hpq : p * q = 0) (hqp : q * p = 0) : residual p q * residual p q = residual p q := by
  calc
    residual p q * residual p q = residual p q + (p * p - p) + (q * q - q) + p * q + q * p := by
      simp only [residual]
      noncomm_ring
    _ = residual p q := by rw [hp, hq, hpq, hqp]; simp

lemma residual_mul_p (hp : p * p = p) (hqp : q * p = 0) : residual p q * p = 0 := by simp [residual, sub_mul, hp, hqp]
lemma p_mul_residual (hp : p * p = p) (hpq : p * q = 0) : p * residual p q = 0 := by simp [residual, mul_sub, hp, hpq]
lemma residual_mul_q (hq : q * q = q) (hpq : p * q = 0) : residual p q * q = 0 := by simp [residual, sub_mul, hq, hpq]
lemma q_mul_residual (hq : q * q = q) (hqp : q * p = 0) : q * residual p q = 0 := by simp [residual, mul_sub, hq, hqp]

lemma root_nonneg (hp : p * p = p) (hq : q * q = q) (hpq : p * q = 0) (hqp : q * p = 0) (hph : pᴴ = p) (hqh : qᴴ = q) : 0 ≤ rootCandidate p q := by
  have hr := projection_nonneg _ (residual_hermitian p q hph hqh) (residual_sq p q hp hq hpq hqp)
  have hP := projection_nonneg p hph hp
  have hQ := projection_nonneg q hqh hq
  exact add_nonneg (add_nonneg hr (smul_nonneg (by norm_num) hP))
    (smul_nonneg (le_of_lt coefficient_pos) hQ)

lemma root_square (hp : p * p = p) (hq : q * q = q) (hpq : p * q = 0) (hqp : q * p = 0) : rootCandidate p q * rootCandidate p q = defectCandidate p q := by
  simp only [rootCandidate, defectCandidate, add_mul, mul_add, smul_mul_assoc, mul_smul_comm,
    residual_sq p q hp hq hpq hqp, residual_mul_p p q hp hqp, p_mul_residual p q hp hpq,
    residual_mul_q p q hq hpq, q_mul_residual p q hq hqp, hp, hq, hpq, hqp,
    smul_zero, zero_add, add_zero, smul_smul, coefficient_sq]
  module

lemma root_identity (hp : p * p = p) (hq : q * q = q) (hpq : p * q = 0) (hqp : q * p = 0) (hph : pᴴ = p) (hqh : qᴴ = q) : CFC.sqrt (defectCandidate p q) = rootCandidate p q :=
  CFC.sqrt_unique (root_square p q hp hq hpq hqp) (root_nonneg p q hp hq hpq hqp hph hqh)

lemma defect_posDef (hp : p * p = p) (hq : q * q = q) (hpq : p * q = 0) (hqp : q * p = 0) (hph : pᴴ = p) (hqh : qᴴ = q) : (defectCandidate p q).PosDef := by
  have hr := (projection_nonneg _ (residual_hermitian p q hph hqh) (residual_sq p q hp hq hpq hqp)).posSemidef
  have hP := (projection_nonneg p hph hp).posSemidef
  have hQ := (projection_nonneg q hqh hq).posSemidef
  have h0 : ((1 / 2 : ℝ) • (1 : Matrix n n ℂ)).PosDef := Matrix.PosDef.one.smul (by norm_num)
  have hsum := ((h0.add_posSemidef (hr.smul (by norm_num : (0:ℝ) ≤ 1/2))).add_posSemidef
    (hP.smul (by norm_num : (0:ℝ) ≤ 7/50))).add_posSemidef
      (hQ.smul (by norm_num : (0:ℝ) ≤ 2071/20000))
  have he : defectCandidate p q = (1 / 2 : ℝ) • (1 : Matrix n n ℂ) +
      (1 / 2 : ℝ) • residual p q + (7 / 50 : ℝ) • p + (2071 / 20000 : ℝ) • q := by
    simp only [defectCandidate, residual]
    module
  rw [he]
  exact hsum

end D0.Geometry.OrthogonalProjectionRoot


open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookMovedJuliaLeft
open D0.Geometry.CubicExponential
open D0.Geometry.OrthogonalProjectionRoot
open Matrix
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OriginalBookMovedJuliaRight

noncomputable def regularC : Matrix (Fin 16) (Fin 16) ℂ := regularInt.map (Int.castRingHom ℂ)
noncomputable def numeratorC : Matrix (Fin 16) (Fin 16) ℂ := blockNumeratorInt.map (Int.castRingHom ℂ)
noncomputable def boostedC : Matrix (Fin 16) (Fin 16) ℂ := (1 / 1762 : ℝ) • numeratorC

lemma regularC_sq : regularC * regularC = regularC := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) regularInt_sq
  change ((regularInt * regularInt).map (Int.castRingHom ℂ)) = regularInt.map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  exact h

lemma numeratorC_sq : numeratorC * numeratorC = (1762 : ℝ) • numeratorC := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) blockNumeratorInt_sq
  change ((blockNumeratorInt * blockNumeratorInt).map (Int.castRingHom ℂ)) =
    ((1762 : ℤ) • blockNumeratorInt).map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  ext i j
  have hij := congrFun (congrFun h i) j
  simpa [numeratorC, Matrix.smul_apply, Matrix.mul_apply, Matrix.ofNat_apply] using hij

lemma boostedC_sq : boostedC * boostedC = boostedC := by
  simp only [boostedC, smul_mul_assoc, mul_smul_comm, smul_smul, numeratorC_sq]
  module

lemma regularC_num_zero : regularC * numeratorC = 0 := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) regularInt_block_mul_zero
  change ((regularInt * blockNumeratorInt).map (Int.castRingHom ℂ)) =
    (0 : SourceMatrix).map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  simpa [regularC, numeratorC] using h

lemma num_regularC_zero : numeratorC * regularC = 0 := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) block_regularInt_mul_zero
  change ((blockNumeratorInt * regularInt).map (Int.castRingHom ℂ)) =
    (0 : SourceMatrix).map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  simpa [regularC, numeratorC] using h

lemma regular_boosted_zero : regularC * boostedC = 0 := by
  simp [boostedC, regularC_num_zero]

lemma boosted_regular_zero : boostedC * regularC = 0 := by
  simp [boostedC, num_regularC_zero]

lemma regularC_hermitian : regularCᴴ = regularC := by
  have h : regularInt.transpose.map (Int.castRingHom ℂ) = regularCᴴ := by
    ext i j
    simp [regularC, Matrix.conjTranspose_apply]
  rw [regularInt_transpose] at h
  exact h.symm

lemma numeratorC_hermitian : numeratorCᴴ = numeratorC := by
  have h : blockNumeratorInt.transpose.map (Int.castRingHom ℂ) = numeratorCᴴ := by
    ext i j
    simp [numeratorC, Matrix.conjTranspose_apply]
  rw [blockNumeratorInt_transpose] at h
  exact h.symm

lemma boostedC_hermitian : boostedCᴴ = boostedC := by
  simp [boostedC, Matrix.conjTranspose_smul, numeratorC_hermitian]

lemma fortyMovedC_rightGram :
    fortyMovedCᴴ * fortyMovedC = (1600 : ℝ) • regularC + numeratorC := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) sourceRightGram
  change ((fortyMoved.transpose * fortyMoved).map (Int.castRingHom ℂ)) =
    ((1600 : ℤ) • regularInt + blockNumeratorInt).map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  have ht : fortyMoved.transpose.map (Int.castRingHom ℂ) = fortyMovedCᴴ := by
    ext i j
    simp [fortyMovedC, Matrix.conjTranspose_apply]
  rw [ht] at h
  ext i j
  have hij := congrFun (congrFun h i) j
  simpa [fortyMovedC, regularC, numeratorC, Matrix.mul_apply, Matrix.smul_apply,
    Matrix.ofNat_apply] using hij

lemma movedAnalytic_rightGram :
    (sourceAnalyticOperand D0.D)ᴴ * sourceAnalyticOperand D0.D =
      (9 / 40000 : ℂ) • (fortyMovedCᴴ * fortyMovedC) := by
  rw [movedAnalytic_eq]
  have hz : -(((3 / 200 : ℂ) * Complex.I) * ((3 / 200 : ℂ) * Complex.I)) = 9 / 40000 := by
    calc
      -(((3 / 200 : ℂ) * Complex.I) * ((3 / 200 : ℂ) * Complex.I)) =
          -((3 / 200 : ℂ) ^ 2) * (Complex.I * Complex.I) := by ring
      _ = 9 / 40000 := by rw [Complex.I_mul_I]; norm_num
  simp [Matrix.conjTranspose_smul, smul_smul]
  rw [← neg_smul, hz]

theorem movedAnalytic_rightDefect :
    1 - (sourceAnalyticOperand D0.D)ᴴ * sourceAnalyticOperand D0.D =
      defectCandidate regularC boostedC := by
  rw [movedAnalytic_rightGram, fortyMovedC_rightGram]
  ext i j
  simp [defectCandidate, D0.Geometry.OrthogonalProjectionRoot.residual, boostedC,
    Complex.real_smul, Matrix.smul_apply]
  ring

theorem movedAnalytic_rightRoot :
    CFC.sqrt (1 - (sourceAnalyticOperand D0.D)ᴴ * sourceAnalyticOperand D0.D) =
      rootCandidate regularC boostedC := by
  rw [movedAnalytic_rightDefect]
  exact root_identity _ _ regularC_sq boostedC_sq regular_boosted_zero boosted_regular_zero
    regularC_hermitian boostedC_hermitian

/-- The explicit source-specific matrix, including all four signed 2×2 blocks. -/
theorem movedAnalytic_rightRoot_explicit :
    CFC.sqrt (1 - (sourceAnalyticOperand D0.D)ᴴ * sourceAnalyticOperand D0.D) =
      1 - (1 / 5 : ℝ) • regularC + (coefficient - 1) • boostedC := by
  rw [movedAnalytic_rightRoot]
  simp only [rootCandidate, D0.Geometry.OrthogonalProjectionRoot.residual]
  module

theorem movedAnalytic_rightDefect_posDef :
    (1 - (sourceAnalyticOperand D0.D)ᴴ * sourceAnalyticOperand D0.D).PosDef := by
  rw [movedAnalytic_rightDefect]
  exact defect_posDef _ _ regularC_sq boostedC_sq regular_boosted_zero boosted_regular_zero
    regularC_hermitian boostedC_hermitian

end D0.Geometry.OriginalBookMovedJuliaRight
