import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith
import D0.Matter.TraceDecompositionSigns

open scoped BigOperators

namespace D0.Matter

def edgePairing {n : Type} [Fintype n] (T H : Matrix n n ℝ) : ℝ :=
  ∑ i : n, ∑ j : n, T i j * H i j

noncomputable def edgeStress {n : Type} [Fintype n] [DecidableEq n] (Γ : Matrix n n ℝ) : Matrix n n ℝ :=
  symmOffDiagPart Γ

theorem symmOffDiag_trace_pairing_is_positive_edge_dot {n : Type} [Fintype n] [DecidableEq n]
    (Γ H : Matrix n n ℝ) (hH : H.transpose = H) (_hH_diag : ∀ i, H i i = 0) :
    Matrix.trace (symmOffDiagPart Γ * H) = edgePairing (symmOffDiagPart Γ) H := by
  unfold Matrix.trace Matrix.diag edgePairing
  simp_rw [Matrix.mul_apply]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  have hH_apply : H j i = H i j := by
    have h_trans := congr_fun (congr_fun hH j) i
    simp [Matrix.transpose_apply] at h_trans
    exact h_trans.symm
  rw [hH_apply]

theorem scalar_edge_decoupling {n : Type} [Fintype n] [DecidableEq n]
    (Γ : Matrix n n ℝ) (φ : n → ℝ) :
    Matrix.trace (symmOffDiagPart Γ * Matrix.diagonal φ) = 0 := by
  unfold Matrix.trace Matrix.diag symmOffDiagPart
  simp_rw [Matrix.mul_apply, Matrix.diagonal_apply]
  have h_sum : ∀ i : n, (∑ j : n, (if i = j then 0 else (1/2 : ℝ) * (Γ i j + Γ j i)) * (if j = i then φ j else 0)) = 0 := by
    intro i
    rw [Finset.sum_eq_single i]
    · rw [if_pos rfl, if_pos rfl, zero_mul]
    · intro j _ hne
      rw [if_neg hne, mul_zero]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  simp_rw [h_sum, Finset.sum_const_zero]

end D0.Matter
