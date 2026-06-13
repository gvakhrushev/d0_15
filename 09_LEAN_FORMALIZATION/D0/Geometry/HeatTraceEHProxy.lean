import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.ConformalLaplacianTrace

open scoped BigOperators

namespace D0.Geometry

noncomputable def discreteEHActionProxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) : ℝ :=
  ∑ i, ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0

theorem weighted_laplacian_entry {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) (i j : N) :
    (Wρ ρ * L * Wρ ρ) i j = L i j / Real.sqrt (ρ i * ρ j) := by
  unfold Wρ
  rw [Matrix.mul_apply]
  simp_rw [Matrix.mul_apply]
  simp only [Matrix.diagonal_apply, mul_ite, ite_mul, mul_zero, zero_mul, Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_univ, if_true]
  have h_sqrt_mul : Real.sqrt (ρ i * ρ j) = Real.sqrt (ρ i) * Real.sqrt (ρ j) := Real.sqrt_mul (le_of_lt (h_pos i)) (ρ j)
  rw [h_sqrt_mul]
  have h1 : Real.sqrt (ρ i) > 0 := Real.sqrt_pos.mpr (h_pos i)
  have h2 : Real.sqrt (ρ j) > 0 := Real.sqrt_pos.mpr (h_pos j)
  have h1_ne : Real.sqrt (ρ i) ≠ 0 := ne_of_gt h1
  have h2_ne : Real.sqrt (ρ j) ≠ 0 := ne_of_gt h2
  field_simp

theorem trace_square_weighted_laplacian_decomposition {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) (h_symm : ∀ i j, L i j = L j i) :
    Matrix.trace ((Wρ ρ * L * Wρ ρ) * (Wρ ρ * L * Wρ ρ)) =
    (∑ i, (L i i)^2 / (ρ i)^2) + discreteEHActionProxy L ρ := by
  unfold Matrix.trace
  dsimp
  have h_outer : ∀ i, ((Wρ ρ * L * Wρ ρ) * (Wρ ρ * L * Wρ ρ)) i i = ∑ j, (Wρ ρ * L * Wρ ρ) i j * (Wρ ρ * L * Wρ ρ) j i := by
    intro i
    rw [Matrix.mul_apply]
  have h_lhs_unfold : (∑ i, ((Wρ ρ * L * Wρ ρ) * (Wρ ρ * L * Wρ ρ)) i i) = ∑ i, ∑ j, (Wρ ρ * L * Wρ ρ) i j * (Wρ ρ * L * Wρ ρ) j i := by
    apply Finset.sum_congr rfl
    intro i _
    exact h_outer i
  rw [h_lhs_unfold]
  have h_term : ∀ i j, (Wρ ρ * L * Wρ ρ) i j * (Wρ ρ * L * Wρ ρ) j i = (L i j)^2 / (ρ i * ρ j) := by
    intro i j
    rw [weighted_laplacian_entry L ρ h_pos i j, weighted_laplacian_entry L ρ h_pos j i]
    have h_symm_L : L j i = L i j := h_symm j i
    rw [h_symm_L]
    have h_mul_comm : ρ j * ρ i = ρ i * ρ j := mul_comm (ρ j) (ρ i)
    rw [h_mul_comm]
    have h_pos_prod : ρ i * ρ j > 0 := mul_pos (h_pos i) (h_pos j)
    have h_sqrt_sq : Real.sqrt (ρ i * ρ j) * Real.sqrt (ρ i * ρ j) = ρ i * ρ j := Real.mul_self_sqrt (le_of_lt h_pos_prod)
    calc
      (L i j / Real.sqrt (ρ i * ρ j)) * (L i j / Real.sqrt (ρ i * ρ j)) = (L i j * L i j) / (Real.sqrt (ρ i * ρ j) * Real.sqrt (ρ i * ρ j)) := by ring
      _ = (L i j)^2 / (ρ i * ρ j) := by
        rw [h_sqrt_sq]
        ring
  have h_lhs : (∑ i, ∑ j, (Wρ ρ * L * Wρ ρ) i j * (Wρ ρ * L * Wρ ρ) j i) = ∑ i, ∑ j, (L i j)^2 / (ρ i * ρ j) := by
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    exact h_term i j
  rw [h_lhs]
  unfold discreteEHActionProxy
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  have h_split : ∑ j, (L i j)^2 / (ρ i * ρ j) = (L i i)^2 / (ρ i)^2 + ∑ j ∈ Finset.univ.erase i, (L i j)^2 / (ρ i * ρ j) := by
    have h_add := Finset.sum_erase_add Finset.univ (fun j => (L i j)^2 / (ρ i * ρ j)) (Finset.mem_univ i)
    rw [← h_add]
    dsimp
    have h_ii : (L i i)^2 / (ρ i * ρ i) = (L i i)^2 / (ρ i)^2 := by
      rw [sq]
      ring
    rw [h_ii]
    ring
  have h_ite_add : (∑ j ∈ Finset.univ.erase i, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0) + (if i ≠ i then (L i i)^2 / (ρ i * ρ i) else 0) = ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0 :=
    Finset.sum_erase_add Finset.univ (fun j => if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0) (Finset.mem_univ i)
  have h_ite : ∑ j, (if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0) = ∑ j ∈ Finset.univ.erase i, (L i j)^2 / (ρ i * ρ j) := by
    rw [← h_ite_add]
    simp only [ne_eq, not_true_eq_false, ite_false, add_zero]
    apply Finset.sum_congr rfl
    intro x hx
    have hx_ne : i ≠ x := by
      intro h_eq
      rw [h_eq] at hx
      exact Finset.mem_erase.mp hx |>.1 rfl
    rw [if_pos hx_ne]
  rw [h_split]
  rw [h_ite]

theorem offdiag_proxy_nonnegative {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) :
    discreteEHActionProxy L ρ ≥ 0 := by
  unfold discreteEHActionProxy
  apply Finset.sum_nonneg
  intro i _
  apply Finset.sum_nonneg
  intro j _
  split_ifs with h_ne
  · apply div_nonneg
    · exact sq_nonneg (L i j)
    · apply mul_nonneg
      · exact le_of_lt (h_pos i)
      · exact le_of_lt (h_pos j)
  · linarith

theorem regular_graph_diagonal_square_term {N : Type} [Fintype N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (d : ℝ) (h_eq : ∀ i, L i i = d) :
    (∑ i, (L i i)^2 / (ρ i)^2) = d^2 * ∑ i, 1 / (ρ i)^2 := by
  simp_rw [h_eq]
  have h_div : ∀ i, d^2 / (ρ i)^2 = d^2 * (1 / (ρ i)^2) := by
    intro i
    ring
  simp_rw [h_div]
  rw [← Finset.mul_sum]

end D0.Geometry
