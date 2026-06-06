import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith
import D0.Matter.TraceDecompositionSigns

open scoped BigOperators

namespace D0.Matter

def linkPairing {n : Type} [Fintype n] (J A : Matrix n n ℝ) : ℝ :=
  ∑ i : n, ∑ j : n, J i j * A i j

noncomputable def vectorCurrent {n : Type} [Fintype n] [DecidableEq n] (Γ : Matrix n n ℝ) : Matrix n n ℝ :=
  skewPart Γ

theorem skew_trace_pairing_is_negative_link_dot {n : Type} [Fintype n] [DecidableEq n]
    (Γ A : Matrix n n ℝ) (hA : A.transpose = -A) :
    Matrix.trace (skewPart Γ * A) = - linkPairing (skewPart Γ) A := by
  unfold Matrix.trace Matrix.diag linkPairing
  simp_rw [Matrix.mul_apply]
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro j _
  have hA_apply : A j i = - A i j := by
    have h_trans := congr_fun (congr_fun hA j) i
    simp [Matrix.transpose_apply] at h_trans
    linarith
  rw [hA_apply]
  ring

theorem scalar_vector_decoupling {n : Type} [Fintype n] [DecidableEq n]
    (Γ : Matrix n n ℝ) (φ : n → ℝ) :
    Matrix.trace (skewPart Γ * Matrix.diagonal φ) = 0 := by
  unfold Matrix.trace Matrix.diag skewPart
  simp_rw [Matrix.mul_apply, Matrix.diagonal_apply]
  have h_sum : ∀ i : n, (∑ j : n, (if i = j then 0 else (1/2 : ℝ) * (Γ i j - Γ j i)) * (if j = i then φ j else 0)) = 0 := by
    intro i
    rw [Finset.sum_eq_single i]
    · rw [if_pos rfl, if_pos rfl, zero_mul]
    · intro j _ hne
      rw [if_neg hne, mul_zero]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  simp_rw [h_sum, Finset.sum_const_zero]

end D0.Matter
