import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.ConformalLaplacianTrace
import D0.Geometry.HeatTraceA2Decomposition

open scoped BigOperators

namespace D0.Geometry.SpectralActionLadder

open D0.Geometry
open D0.Geometry.HeatTraceA2Decomposition

noncomputable def conformalLaplacian {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) : Matrix N N ℝ :=
  weightedLaplacian L ρ

noncomputable def spectralTracePower {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) (k : ℕ) : ℝ :=
  Matrix.trace ((conformalLaplacian L ρ)^k)

theorem spectral_action_a0_is_volume_proxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) :
    spectralTracePower L ρ 1 = ∑ i, L i i / ρ i := by
  unfold spectralTracePower conformalLaplacian
  simp only [pow_one]
  exact trace_weighted_laplacian L ρ h_pos

theorem a0_is_volume_proxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) :
    spectralTracePower L ρ 1 = ∑ i, L i i / ρ i :=
  spectral_action_a0_is_volume_proxy L ρ h_pos

theorem spectral_action_a2_is_eh_proxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) (h_symm : ∀ i j, L i j = L j i) :
    spectralTracePower L ρ 2 =
      HeatTraceA2Decomposition.diagonalSquareTerm L ρ
        + 2 * HeatTraceA2Decomposition.discreteEHActionProxy L ρ := by
  unfold spectralTracePower conformalLaplacian
  rw [pow_two]
  exact heat_trace_sq_exact_decomposition L ρ h_pos h_symm

theorem a2_is_eh_proxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) (h_symm : ∀ i j, L i j = L j i) :
    spectralTracePower L ρ 2 =
      HeatTraceA2Decomposition.diagonalSquareTerm L ρ
        + 2 * HeatTraceA2Decomposition.discreteEHActionProxy L ρ :=
  spectral_action_a2_is_eh_proxy L ρ h_pos h_symm

theorem higher_curvature_floor_bound_basic {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (ρ_floor B : ℝ) (h_floor : ∀ i, ρ i ≥ ρ_floor) (h_floor_pos : ρ_floor > 0)
    (h_L_bound : ∀ i j, |L i j| ≤ B) (i j : N) :
    |(conformalLaplacian L ρ) i j| ≤ B / ρ_floor := by
  have h_pos : ∀ k, ρ k > 0 := by
    intro k
    linarith [h_floor k]
  unfold conformalLaplacian weightedLaplacian
  rw [weighted_laplacian_entry L ρ h_pos i j]
  rw [abs_div, abs_of_nonneg (Real.sqrt_nonneg _)]
  have h_sqrt_pos : Real.sqrt (ρ i * ρ j) > 0 := by
    exact Real.sqrt_pos.mpr (mul_pos (h_pos i) (h_pos j))
  have h_prod : ρ_floor * ρ_floor ≤ ρ i * ρ j := by
    nlinarith [h_floor i, h_floor j, le_of_lt h_floor_pos]
  have h_sqrt_mono : ρ_floor ≤ Real.sqrt (ρ i * ρ j) := by
    have h := Real.sqrt_le_sqrt h_prod
    rwa [← sq, Real.sqrt_sq (le_of_lt h_floor_pos)] at h
  have h_B_nonneg : 0 ≤ B := by
    exact le_trans (abs_nonneg (L i j)) (h_L_bound i j)
  calc
    |L i j| / Real.sqrt (ρ i * ρ j)
        ≤ B / Real.sqrt (ρ i * ρ j) := by
          exact div_le_div_of_nonneg_right (h_L_bound i j) (le_of_lt h_sqrt_pos)
    _ ≤ B / ρ_floor := by
      rw [div_le_div_iff₀ h_sqrt_pos h_floor_pos]
      nlinarith

lemma entry_power_bound {N : Type} [Fintype N] [DecidableEq N] (A : Matrix N N ℝ) (C : ℝ) (h_C : 0 ≤ C)
    (h_bound : ∀ i j, |A i j| ≤ C) (k : ℕ) (i j : N) :
    |(A^k) i j| ≤ (Fintype.card N : ℝ)^k * C^k := by
  induction k generalizing i j with
  | zero =>
    simp only [pow_zero, mul_one]
    rw [Matrix.one_apply]
    split_ifs
    · simp
    · simp
  | succ k ih =>
    rw [pow_succ]
    rw [Matrix.mul_apply]
    have h_abs : |∑ x, (A^k) i x * A x j| ≤ ∑ x, |(A^k) i x * A x j| := Finset.abs_sum_le_sum_abs _ _
    have h_term_le : ∀ x, |(A^k) i x * A x j| ≤ (Fintype.card N : ℝ)^k * C^(k+1) := by
      intro x
      rw [abs_mul]
      have h1 := ih i x
      have h2 := h_bound x j
      have h1_nonneg : 0 ≤ (Fintype.card N : ℝ)^k * C^k := by
        apply mul_nonneg
        · positivity
        · exact pow_nonneg h_C k
      have h2_nonneg : 0 ≤ |A x j| := abs_nonneg _
      calc
        |(A ^ k) i x| * |A x j|
            ≤ ((Fintype.card N : ℝ)^k * C^k) * C := by
              exact mul_le_mul h1 h2 h2_nonneg h1_nonneg
        _ = (Fintype.card N : ℝ)^k * C^(k+1) := by
          ring_nf
    have h_sum_le : (∑ x, |(A^k) i x * A x j|) ≤ ∑ x : N, ((Fintype.card N : ℝ)^k * C^(k+1)) := by
      apply Finset.sum_le_sum
      intro x _
      exact h_term_le x
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at h_sum_le
    have h_rhs_eq : (Fintype.card N : ℝ) * ((Fintype.card N : ℝ)^k * C^(k+1)) = (Fintype.card N : ℝ)^(k+1) * C^(k+1) := by
      ring_nf
    rw [h_rhs_eq] at h_sum_le
    linarith

theorem trace_power_bound {N : Type} [Fintype N] [DecidableEq N] (A : Matrix N N ℝ) (C : ℝ) (h_C : 0 ≤ C)
    (h_bound : ∀ i j, |A i j| ≤ C) (k : ℕ) :
    |Matrix.trace (A^k)| ≤ (Fintype.card N : ℝ)^(k+1) * C^k := by
  unfold Matrix.trace
  dsimp
  have h_abs := Finset.abs_sum_le_sum_abs (fun i => (A^k) i i) Finset.univ
  have h_term : ∀ i, |(A^k) i i| ≤ (Fintype.card N : ℝ)^k * C^k := by
    intro i
    exact entry_power_bound A C h_C h_bound k i i
  have h_sum_le : (∑ i, |(A^k) i i|) ≤ ∑ i : N, ((Fintype.card N : ℝ)^k * C^k) := by
    apply Finset.sum_le_sum
    intro i _
    exact h_term i
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at h_sum_le
  have h_rhs : (Fintype.card N : ℝ) * ((Fintype.card N : ℝ)^k * C^k) = (Fintype.card N : ℝ)^(k+1) * C^k := by
    ring_nf
  rw [h_rhs] at h_sum_le
  linarith

theorem higher_powers_floor_bounded {N : Type} [Fintype N] [Nonempty N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (ρ_floor B : ℝ) (k : ℕ) (_hk : k ≥ 3)
    (h_floor : ∀ i, ρ i ≥ ρ_floor) (h_floor_pos : ρ_floor > 0)
    (h_L_bound : ∀ i j, |L i j| ≤ B) :
    |spectralTracePower L ρ k| ≤ (Fintype.card N : ℝ)^(k + 1) * (B / ρ_floor)^k := by
  unfold spectralTracePower
  have hC_nonneg : 0 ≤ B / ρ_floor := by
    have hB : 0 ≤ B := by
      let i : N := Classical.choice inferInstance
      exact le_trans (abs_nonneg (L i i)) (h_L_bound i i)
    exact div_nonneg hB (le_of_lt h_floor_pos)
  have h_entry : ∀ i j, |(conformalLaplacian L ρ) i j| ≤ B / ρ_floor := by
    intro i j
    exact higher_curvature_floor_bound_basic L ρ ρ_floor B h_floor h_floor_pos h_L_bound i j
  exact trace_power_bound (conformalLaplacian L ρ) (B / ρ_floor) hC_nonneg h_entry k

end D0.Geometry.SpectralActionLadder
