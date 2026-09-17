import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic

open scoped BigOperators

namespace D0.Geometry

def archiveShiftMatrix (n : ℕ) [NeZero n] : Matrix (ZMod n) (ZMod n) ℝ :=
  fun i j => if j = i + 1 then 1 else 0

theorem shift_matrix_mul_right {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ) (i j : ZMod n) :
    (M * archiveShiftMatrix n) i j = M i (j - 1) := by
  rw [Matrix.mul_apply]
  unfold archiveShiftMatrix
  rw [Finset.sum_eq_single (j - 1)]
  · simp
  · intro k _ hne
    have h_ne_cond : j ≠ k + 1 := by
      intro h_eq
      have h_eq_k : k = j - 1 := by
        rw [h_eq]
        simp
      exact hne h_eq_k
    rw [if_neg h_ne_cond, mul_zero]
  · intro h
    exact False.elim (h (Finset.mem_univ _))

theorem shift_matrix_mul_left {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ) (i j : ZMod n) :
    (archiveShiftMatrix n * M) i j = M (i + 1) j := by
  rw [Matrix.mul_apply]
  unfold archiveShiftMatrix
  rw [Finset.sum_eq_single (i + 1)]
  · simp
  · intro k _ hne
    rw [if_neg hne, zero_mul]
  · intro h
    exact False.elim (h (Finset.mem_univ _))

theorem commute_with_shift_step {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ)
    (h : M * archiveShiftMatrix n = archiveShiftMatrix n * M) (i : ZMod n) :
    M i i = M (i + 1) (i + 1) := by
  have h_comm := congr_fun (congr_fun h i) (i + 1)
  rw [shift_matrix_mul_right, shift_matrix_mul_left] at h_comm
  simp at h_comm
  exact h_comm

lemma commute_with_shift_k {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ)
    (h : M * archiveShiftMatrix n = archiveShiftMatrix n * M) (i : ZMod n) (k : ℕ) :
    M i i = M (i + (k : ZMod n)) (i + (k : ZMod n)) := by
  induction k with
  | zero =>
    simp
  | succ k ih =>
    rw [ih]
    have h_step := commute_with_shift_step M h (i + (k : ZMod n))
    have h_assoc : i + (k : ZMod n) + 1 = i + ((k + 1 : ℕ) : ZMod n) := by
      push_cast
      ring
    rw [h_assoc] at h_step
    exact h_step

theorem commute_with_shift_implies_diagonal_constant {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ)
    (h : M * archiveShiftMatrix n = archiveShiftMatrix n * M) (i j : ZMod n) :
    M i i = M j j := by
  let k : ℕ := (j - i).val
  have h_eq := commute_with_shift_k M h i k
  have h_val : i + (k : ZMod n) = j := by
    dsimp [k]
    rw [ZMod.natCast_val, ZMod.cast_id', id_eq]
    simp
  rw [h_val] at h_eq
  exact h_eq

end D0.Geometry
