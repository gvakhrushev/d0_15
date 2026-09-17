import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith

open scoped BigOperators

namespace D0.Algebra

theorem skew_square_trace_nonpositive {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) :
    Matrix.trace (K * K) ≤ 0 := by
  unfold Matrix.trace Matrix.diag
  simp_rw [Matrix.mul_apply]
  have h_eq : (∑ i : n, ∑ j : n, K i j * K j i) = - ∑ i : n, ∑ j : n, (K i j)^2 := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro i _
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro j _
    have hK_apply : K j i = - K i j := by
      have h_trans := congr_fun (congr_fun hK j) i
      simp [Matrix.transpose_apply] at h_trans
      linarith
    rw [hK_apply]
    ring
  rw [h_eq]
  have h_nonneg : 0 ≤ ∑ i : n, ∑ j : n, (K i j)^2 := by
    apply Finset.sum_nonneg
    intro i _
    apply Finset.sum_nonneg
    intro j _
    simp only [sq_nonneg]
  linarith

theorem skew_square_trace_eq_zero_iff {n : Type} [Fintype n] [DecidableEq n]
    (K : Matrix n n ℝ) (hK : K.transpose = -K) :
    Matrix.trace (K * K) = 0 ↔ K = 0 := by
  constructor
  · intro h
    ext i j
    unfold Matrix.trace Matrix.diag at h
    simp_rw [Matrix.mul_apply] at h
    have h_eq : (∑ i : n, ∑ j : n, K i j * K j i) = - ∑ i : n, ∑ j : n, (K i j)^2 := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro x _
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro y _
      have hK_apply : K y x = - K x y := by
        have h_trans := congr_fun (congr_fun hK y) x
        simp [Matrix.transpose_apply] at h_trans
        linarith
      rw [hK_apply]
      ring
    rw [h_eq] at h
    have h_sum_zero : (∑ i : n, ∑ j : n, (K i j)^2) = 0 := by linarith
    have h_all_zero : ∀ i : n, (∑ j : n, (K i j)^2) = 0 := by
      have h_nonneg_inner : ∀ i : n, 0 ≤ ∑ j : n, (K i j)^2 := by
        intro i
        apply Finset.sum_nonneg
        intro j _
        exact sq_nonneg (K i j)
      have h_sum_eq := (Finset.sum_eq_zero_iff_of_nonneg (fun x _ => h_nonneg_inner x)).mp h_sum_zero
      intro i
      exact h_sum_eq i (Finset.mem_univ _)
    have h_ij_zero : (K i j)^2 = 0 := by
      have h_sum_i := h_all_zero i
      have h_nonneg_sq : ∀ j : n, 0 ≤ (K i j)^2 := fun j => sq_nonneg (K i j)
      have h_sq_eq := (Finset.sum_eq_zero_iff_of_nonneg (fun y _ => h_nonneg_sq y)).mp h_sum_i
      exact h_sq_eq j (Finset.mem_univ _)
    exact sq_eq_zero_iff.mp h_ij_zero
  · intro h
    subst h
    simp [Matrix.trace_zero]

end D0.Algebra
