import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import D0.Topology.ArchiveShiftTopology

open scoped BigOperators

namespace D0.Geometry

private def archiveShiftPerm (n : ℕ) [NeZero n] : Equiv.Perm (ZMod n) where
  toFun i := i + 1
  invFun i := i - 1
  left_inv i := by simp
  right_inv i := by simp

def archiveShiftMatrix (n : ℕ) [NeZero n] : Matrix (ZMod n) (ZMod n) ℝ :=
  D0.Topology.shiftMatrix (archiveShiftPerm n)

theorem shift_matrix_mul_right {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ) (i j : ZMod n) :
    (M * archiveShiftMatrix n) i j = M i (j - 1) := by
  simpa [archiveShiftMatrix, archiveShiftPerm] using
    (D0.Topology.shift_matrix_mul_right M (archiveShiftPerm n) i j)

theorem shift_matrix_mul_left {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ) (i j : ZMod n) :
    (archiveShiftMatrix n * M) i j = M (i + 1) j := by
  simpa [archiveShiftMatrix, archiveShiftPerm] using
    (D0.Topology.shift_matrix_mul_left M (archiveShiftPerm n) i j)

theorem commute_with_shift_step {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ)
    (h : M * archiveShiftMatrix n = archiveShiftMatrix n * M) (i : ZMod n) :
    M i i = M (i + 1) (i + 1) := by
  simpa [archiveShiftMatrix, archiveShiftPerm] using
    (D0.Topology.commute_with_shift_step M (archiveShiftPerm n) h i)

private lemma archiveShiftPerm_iterate {n : ℕ} [NeZero n] (i : ZMod n) (k : ℕ) :
    (((archiveShiftPerm n : ZMod n → ZMod n)^[k]) i) = i + (k : ZMod n) := by
  induction k with
  | zero =>
    simp
  | succ k ih =>
    rw [Function.iterate_succ']
    change (((archiveShiftPerm n : ZMod n → ZMod n)^[k]) i) + 1 =
      i + ((Nat.succ k : ℕ) : ZMod n)
    rw [ih]
    push_cast
    ring

lemma commute_with_shift_k {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ)
    (h : M * archiveShiftMatrix n = archiveShiftMatrix n * M) (i : ZMod n) (k : ℕ) :
    M i i = M (i + (k : ZMod n)) (i + (k : ZMod n)) := by
  change M * D0.Topology.shiftMatrix (archiveShiftPerm n) =
    D0.Topology.shiftMatrix (archiveShiftPerm n) * M at h
  simpa only [archiveShiftPerm_iterate] using
    (D0.Topology.commute_with_shift_iterate M (archiveShiftPerm n) h i k)

private def archiveShiftTopology (n : ℕ) [NeZero n] : D0.Topology.ArchiveTopology (ZMod n) where
  shift := archiveShiftPerm n
  is_single_orbit := by
    intro i j
    let k : ℕ := (j - i).val
    refine ⟨k, ?_⟩
    rw [archiveShiftPerm_iterate]
    have h_val : i + (k : ZMod n) = j := by
      dsimp [k]
      rw [ZMod.natCast_val, ZMod.cast_id', id_eq]
      simp
    exact h_val

theorem commute_with_shift_implies_diagonal_constant {n : ℕ} [NeZero n] (M : Matrix (ZMod n) (ZMod n) ℝ)
    (h : M * archiveShiftMatrix n = archiveShiftMatrix n * M) (i j : ZMod n) :
    M i i = M j j := by
  change M * D0.Topology.shiftMatrix (archiveShiftPerm n) =
    D0.Topology.shiftMatrix (archiveShiftPerm n) * M at h
  exact D0.Topology.abstract_shift_commute_implies_diagonal_constant
    M (archiveShiftTopology n) h i j

end D0.Geometry
