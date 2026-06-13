import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic

open scoped BigOperators

namespace D0.Matter

theorem scalar_coupling_blind_to_off_diagonal {N : Type} [Fintype N] [DecidableEq N]
    (Γ : Matrix N N ℝ) (φ : N → ℝ) :
    Matrix.trace (Γ * Matrix.diagonal φ) = dotProduct (fun i => Γ i i) φ := by
  unfold Matrix.trace Matrix.diag dotProduct
  dsimp
  apply Finset.sum_congr rfl
  intro i _
  rw [Matrix.mul_apply]
  unfold Matrix.diagonal
  dsimp
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hne
    rw [if_neg hne, mul_zero]
  · intro h
    exact False.elim (h (Finset.mem_univ _))

end D0.Matter
