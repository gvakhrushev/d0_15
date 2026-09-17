import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.SpectralActionLadder
import D0.Geometry.SpectralActionAdmissibility

open scoped BigOperators

namespace D0.Geometry.HigherCurvatureSuppression

open D0.Geometry.SpectralActionLadder

theorem matrix_power_combinatorial_bound {N : Type} [Fintype N] [DecidableEq N]
    (A : Matrix N N ℝ) (B : ℝ) (hB : 0 ≤ B)
    (h_bound : ∀ i j, |A i j| ≤ B) (k : ℕ) (i j : N) :
    |(A ^ (k + 1)) i j| ≤ (Fintype.card N : ℝ)^k * B^(k + 1) := by
  induction k generalizing i j with
  | zero =>
      simpa using h_bound i j
  | succ k ih =>
      rw [pow_succ]
      rw [Matrix.mul_apply]
      have h_abs : |∑ x, (A ^ (k + 1)) i x * A x j| ≤
          ∑ x, |(A ^ (k + 1)) i x * A x j| :=
        Finset.abs_sum_le_sum_abs _ _
      have h_term : ∀ x, |(A ^ (k + 1)) i x * A x j| ≤
          (Fintype.card N : ℝ)^k * B^(k + 2) := by
        intro x
        rw [abs_mul]
        have h1 := ih i x
        have h2 := h_bound x j
        have h1_nonneg : 0 ≤ (Fintype.card N : ℝ)^k * B^(k + 1) := by
          apply mul_nonneg
          · positivity
          · exact pow_nonneg hB (k + 1)
        calc
          |(A ^ (k + 1)) i x| * |A x j|
              ≤ ((Fintype.card N : ℝ)^k * B^(k + 1)) * B := by
                exact mul_le_mul h1 h2 (abs_nonneg _) h1_nonneg
          _ = (Fintype.card N : ℝ)^k * B^(k + 2) := by
                ring_nf
      have h_sum : (∑ x, |(A ^ (k + 1)) i x * A x j|) ≤
          ∑ _x : N, ((Fintype.card N : ℝ)^k * B^(k + 2)) := by
        apply Finset.sum_le_sum
        intro x _
        exact h_term x
      simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at h_sum
      have h_rhs : (Fintype.card N : ℝ) * ((Fintype.card N : ℝ)^k * B^(k + 2)) =
          (Fintype.card N : ℝ)^(k + 1) * B^(k + 2) := by
        ring_nf
      rw [h_rhs] at h_sum
      linarith

theorem conformal_laplacian_entry_bound {N : Type} [Fintype N] [DecidableEq N]
    (L : Matrix N N ℝ) (ρ : N → ℝ) (ρ_floor B : ℝ)
    (h_floor : ∀ i, ρ i ≥ ρ_floor) (h_floor_pos : ρ_floor > 0)
    (h_L_bound : ∀ i j, |L i j| ≤ B) (i j : N) :
    |(conformalLaplacian L ρ) i j| ≤ B / ρ_floor :=
  higher_curvature_floor_bound_basic L ρ ρ_floor B h_floor h_floor_pos h_L_bound i j

theorem higher_curvature_suppression_by_floor {N : Type} [Fintype N] [Nonempty N] [DecidableEq N]
    (L : Matrix N N ℝ) (ρ : N → ℝ) (ρ_floor B : ℝ) (k : ℕ)
    (h_floor : ∀ i, ρ i ≥ ρ_floor) (h_floor_pos : ρ_floor > 0)
    (h_L_bound : ∀ i j, |L i j| ≤ B) :
    |Matrix.trace ((conformalLaplacian L ρ) ^ k)| ≤
      (Fintype.card N : ℝ)^(k + 1) * (B / ρ_floor)^k := by
  have hC_nonneg : 0 ≤ B / ρ_floor := by
    have hB : 0 ≤ B := by
      let i : N := Classical.choice inferInstance
      exact le_trans (abs_nonneg (L i i)) (h_L_bound i i)
    exact div_nonneg hB (le_of_lt h_floor_pos)
  have h_entry : ∀ i j, |(conformalLaplacian L ρ) i j| ≤ B / ρ_floor := by
    intro i j
    exact conformal_laplacian_entry_bound L ρ ρ_floor B h_floor h_floor_pos h_L_bound i j
  exact trace_power_bound (conformalLaplacian L ρ) (B / ρ_floor) hC_nonneg h_entry k

theorem higher_curvature_terms_below_finite_readout_cut :
    D0.HigherCurvatureCutoff D0.delta0 := by
  exact D0.d0_higher_curvature_cutoff

end D0.Geometry.HigherCurvatureSuppression
