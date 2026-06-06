import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith

open scoped BigOperators

namespace D0.Geometry

def isSymmOffDiag {n : Type} (M : Matrix n n ℝ) : Prop :=
  M.transpose = M ∧ ∀ i, M i i = 0

theorem trace_transpose_mul_self_eq_zero_iff {n : Type} [Fintype n] [DecidableEq n]
    (M : Matrix n n ℝ) :
    Matrix.trace (M.transpose * M) = 0 ↔ M = 0 := by
  constructor
  · intro h
    ext i j
    unfold Matrix.trace Matrix.diag at h
    simp_rw [Matrix.mul_apply] at h
    have h_eq : (∑ i : n, ∑ j : n, M.transpose i j * M j i) = ∑ i : n, ∑ j : n, (M j i)^2 := by
      apply Finset.sum_congr rfl
      intro x _
      apply Finset.sum_congr rfl
      intro y _
      simp [Matrix.transpose_apply]
      ring
    rw [h_eq] at h
    have h_sum_zero : (∑ i : n, ∑ j : n, (M j i)^2) = 0 := h
    have h_all_zero : ∀ y : n, (∑ x : n, (M x y)^2) = 0 := by
      have h_nonneg_inner : ∀ y : n, 0 ≤ ∑ x : n, (M x y)^2 := by
        intro y
        apply Finset.sum_nonneg
        intro x _
        exact sq_nonneg (M x y)
      have h_sum_eq := (Finset.sum_eq_zero_iff_of_nonneg (fun y _ => h_nonneg_inner y)).mp h_sum_zero
      intro y
      exact h_sum_eq y (Finset.mem_univ _)
    have h_ij_zero : (M i j)^2 = 0 := by
      have h_sum_j := h_all_zero j
      have h_nonneg_sq : ∀ x : n, 0 ≤ (M x j)^2 := fun x => sq_nonneg (M x j)
      have h_sq_eq := (Finset.sum_eq_zero_iff_of_nonneg (fun x _ => h_nonneg_sq x)).mp h_sum_j
      exact h_sq_eq i (Finset.mem_univ _)
    exact sq_eq_zero_iff.mp h_ij_zero
  · intro h
    subst h
    simp [Matrix.trace_zero]

lemma symmOffDiag_orthogonal_to_all_symmOffDiag_is_zero {n : Type} [Fintype n] [DecidableEq n]
    (M : Matrix n n ℝ) (hM_symm : isSymmOffDiag M)
    (h_orth : ∀ dH : Matrix n n ℝ, isSymmOffDiag dH → Matrix.trace (dH.transpose * M) = 0) :
    M = 0 := by
  have h_orth_M := h_orth M hM_symm
  exact (trace_transpose_mul_self_eq_zero_iff M).mp h_orth_M

theorem symmOffDiag_stationarity_implies_edge_equation {n : Type} [Fintype n] [DecidableEq n]
    (E_stiff : Matrix n n ℝ → Matrix n n ℝ)
    (H T : Matrix n n ℝ)
    (hH : isSymmOffDiag H)
    (hT : isSymmOffDiag T)
    (hE : ∀ X, isSymmOffDiag X → isSymmOffDiag (E_stiff X))
    (h_stat : ∀ dH, isSymmOffDiag dH → Matrix.trace (dH.transpose * (E_stiff H - T)) = 0) :
    E_stiff H - T = 0 := by
  have h_res_symm : isSymmOffDiag (E_stiff H - T) := by
    unfold isSymmOffDiag at hH hT ⊢
    have hE_H := hE H hH
    rcases hE_H with ⟨hE_trans, hE_diag⟩
    rcases hT with ⟨hT_trans, hT_diag⟩
    constructor
    · rw [Matrix.transpose_sub, hE_trans, hT_trans]
    · intro i
      rw [Matrix.sub_apply, hE_diag i, hT_diag i, sub_zero]
  exact symmOffDiag_orthogonal_to_all_symmOffDiag_is_zero (E_stiff H - T) h_res_symm h_stat

theorem symmOffDiag_stationarity_implies_edge_equation_eq {n : Type} [Fintype n] [DecidableEq n]
    (E_stiff : Matrix n n ℝ → Matrix n n ℝ)
    (H T : Matrix n n ℝ)
    (hH : isSymmOffDiag H)
    (hT : isSymmOffDiag T)
    (hE : ∀ X, isSymmOffDiag X → isSymmOffDiag (E_stiff X))
    (h_stat : ∀ dH, isSymmOffDiag dH → Matrix.trace (dH.transpose * (E_stiff H - T)) = 0) :
    E_stiff H = T := by
  have h_res := symmOffDiag_stationarity_implies_edge_equation E_stiff H T hH hT hE h_stat
  exact sub_eq_zero.mp h_res

end D0.Geometry
