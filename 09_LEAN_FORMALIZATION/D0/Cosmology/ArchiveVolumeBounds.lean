import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Cosmology.EntropyArchiveFlow

open scoped BigOperators

namespace D0.Cosmology

theorem density_floor_bounds_inverse (y y_floor : ℝ) (h_floor : y ≥ y_floor) (h_pos : y_floor > 0) :
    1 / y ≤ 1 / y_floor := by
  have hy : y > 0 := by linarith
  have h1 : 1 / y_floor - 1 / y = (y - y_floor) / (y * y_floor) := by
    have : y_floor ≠ 0 := ne_of_gt h_pos
    have : y ≠ 0 := ne_of_gt hy
    field_simp
  have h2 : (y - y_floor) / (y * y_floor) ≥ 0 := by
    have h_num : y - y_floor ≥ 0 := by linarith
    have h_den : y * y_floor > 0 := mul_pos hy h_pos
    exact div_nonneg h_num (le_of_lt h_den)
  linarith

theorem density_floor_bounds_archiveVolume {n : Type} [Fintype n] [Nonempty n] (ρ : n → ℝ) (ρ_floor : ℝ)
    (h_bound : ∀ i, ρ i ≥ ρ_floor) (h_pos : ρ_floor > 0) :
    archiveVolume ρ ≤ 1 / ρ_floor := by
  unfold archiveVolume
  have h_each : ∀ i, 1 / ρ i ≤ 1 / ρ_floor := by
    intro i
    exact density_floor_bounds_inverse (ρ i) ρ_floor (h_bound i) h_pos
  have h_sum : ∑ i, 1 / ρ i ≤ (Fintype.card n : ℝ) * (1 / ρ_floor) := by
    calc
      ∑ i, 1 / ρ i ≤ ∑ i : n, 1 / ρ_floor := Finset.sum_le_sum (fun i _ => h_each i)
      _ = (Fintype.card n : ℝ) * (1 / ρ_floor) := by
        simp only [Finset.sum_const, nsmul_eq_mul]
        rfl
  have h_card_pos : (Fintype.card n : ℝ) > 0 := by
    exact Nat.cast_pos.mpr Fintype.card_pos
  rw [div_le_iff₀ h_card_pos]
  linarith

theorem bounded_volume_no_eternal_uniform_acceleration (V : ℕ → ℝ) (U : ℝ) (h_bound : ∀ k, V k ≤ U)
    (ε : ℝ) (hε : ε > 0) (h_acc : ∀ k, V (k + 2) - 2 * V (k + 1) + V k ≥ ε) :
    False := by
  let D := fun k => V (k + 1) - V k
  have h_acc_D : ∀ k, D (k + 1) ≥ D k + ε := by
    intro k
    dsimp [D]
    linarith [h_acc k]
  have h_D_bound : ∀ k, D k ≥ D 0 + (k : ℝ) * ε := by
    intro k
    induction k with
    | zero => simp
    | succ k ih =>
      have h_step := h_acc_D k
      push_cast
      linarith [ih, h_step]
  rcases exists_nat_gt ((1 - D 0) / ε) with ⟨N_0, hN_0⟩
  have h_D_N0 : D N_0 > 1 := by
    have h_pos_eps : ε > 0 := hε
    have h_ineq := (div_lt_iff₀ h_pos_eps).mp hN_0
    have h_D_ineq := h_D_bound N_0
    linarith
  have h_V_grow : ∀ k : ℕ, V (N_0 + k) ≥ V N_0 + (k : ℝ) := by
    intro k
    induction k with
    | zero => simp
    | succ k ih =>
      push_cast
      have h_V_step : V (N_0 + k + 1) = V (N_0 + k) + D (N_0 + k) := by
        dsimp [D]
        ring
      rw [← Nat.add_assoc]
      rw [h_V_step]
      have h_D_large : D (N_0 + k) > 1 := by
        have h_D_ineq := h_D_bound (N_0 + k)
        push_cast at h_D_ineq
        have h_pos_eps : ε > 0 := hε
        have h_ineq := (div_lt_iff₀ h_pos_eps).mp hN_0
        have hk_nonneg : (k : ℝ) * ε ≥ 0 := mul_nonneg (Nat.cast_nonneg k) (le_of_lt hε)
        linarith
      linarith
  rcases exists_nat_gt (U - V N_0) with ⟨k, hk⟩
  have h_Vk := h_V_grow k
  have h_Vk_bound := h_bound (N_0 + k)
  linarith

end D0.Cosmology
