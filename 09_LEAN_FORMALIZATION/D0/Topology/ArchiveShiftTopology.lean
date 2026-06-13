import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Logic.Function.Iterate

open scoped BigOperators

namespace D0.Topology

structure ArchiveTopology (N : Type) where
  shift : Equiv.Perm N
  is_single_orbit : ∀ i j : N, ∃ k : ℕ, ((shift : N → N)^[k]) i = j

def shiftMatrix {N : Type} [Fintype N] [DecidableEq N] (f : Equiv.Perm N) : Matrix N N ℝ :=
  fun i j => if j = f i then 1 else 0

theorem shift_matrix_mul_right {N : Type} [Fintype N] [DecidableEq N] (M : Matrix N N ℝ) (f : Equiv.Perm N) (i j : N) :
    (M * shiftMatrix f) i j = M i (f.symm j) := by
  rw [Matrix.mul_apply]
  unfold shiftMatrix
  rw [Finset.sum_eq_single (f.symm j)]
  · simp
  · intro k _ hne
    have h_ne_cond : j ≠ f k := by
      intro h_eq
      have h_eq_k : k = f.symm j := by
        rw [h_eq]
        simp
      exact hne h_eq_k
    rw [if_neg h_ne_cond, mul_zero]
  · intro h
    exact False.elim (h (Finset.mem_univ _))

theorem shift_matrix_mul_left {N : Type} [Fintype N] [DecidableEq N] (M : Matrix N N ℝ) (f : Equiv.Perm N) (i j : N) :
    (shiftMatrix f * M) i j = M (f i) j := by
  rw [Matrix.mul_apply]
  unfold shiftMatrix
  rw [Finset.sum_eq_single (f i)]
  · simp
  · intro k _ hne
    rw [if_neg hne, zero_mul]
  · intro h
    exact False.elim (h (Finset.mem_univ _))

theorem commute_with_shift_step {N : Type} [Fintype N] [DecidableEq N] (M : Matrix N N ℝ) (f : Equiv.Perm N)
    (h : M * shiftMatrix f = shiftMatrix f * M) (i : N) :
    M i i = M (f i) (f i) := by
  have h_comm := congr_fun (congr_fun h i) (f i)
  rw [shift_matrix_mul_right, shift_matrix_mul_left] at h_comm
  rw [Equiv.symm_apply_apply] at h_comm
  exact h_comm

lemma commute_with_shift_iterate {N : Type} [Fintype N] [DecidableEq N] (M : Matrix N N ℝ) (f : Equiv.Perm N)
    (h : M * shiftMatrix f = shiftMatrix f * M) (i : N) (k : ℕ) :
    M i i = M (((f : N → N)^[k]) i) (((f : N → N)^[k]) i) := by
  induction k with
  | zero =>
    rfl
  | succ k ih =>
    rw [ih]
    rw [Function.iterate_succ']
    exact commute_with_shift_step M f h (((f : N → N)^[k]) i)

theorem abstract_shift_commute_implies_diagonal_constant {N : Type} [Fintype N] [DecidableEq N]
    (M : Matrix N N ℝ) (topo : ArchiveTopology N)
    (h : M * shiftMatrix topo.shift = shiftMatrix topo.shift * M) (i j : N) :
    M i i = M j j := by
  obtain ⟨k, hk⟩ := topo.is_single_orbit i j
  have h_eq := commute_with_shift_iterate M topo.shift h i k
  rw [hk] at h_eq
  exact h_eq

end D0.Topology
