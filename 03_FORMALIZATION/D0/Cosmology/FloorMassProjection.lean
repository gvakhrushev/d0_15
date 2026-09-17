import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

open scoped BigOperators
open Classical

set_option linter.unusedVariables false

namespace D0.Cosmology

theorem projection_exists_of_feasible {N : Type} [Fintype N] [Nonempty N] (ρ_floor : ℝ) (totalMass : ℝ)
    (h_feas : totalMass ≥ (Fintype.card N : ℝ) * ρ_floor) :
    ∃ x : N → ℝ, (∑ i, x i = totalMass) ∧ (∀ i, x i ≥ ρ_floor) := by
  let C := (totalMass - (Fintype.card N : ℝ) * ρ_floor) / (Fintype.card N : ℝ)
  let x := fun _ : N => ρ_floor + C
  use x
  have h_C_nonneg : C ≥ 0 := by
    have h_num : totalMass - (Fintype.card N : ℝ) * ρ_floor ≥ 0 := by linarith
    have h_den : (Fintype.card N : ℝ) > 0 := Nat.cast_pos.mpr Fintype.card_pos
    exact div_nonneg h_num (le_of_lt h_den)
  have h_each : ∀ i : N, x i ≥ ρ_floor := by
    intro i
    dsimp [x]
    linarith
  have h_sum : (∑ i : N, x i) = totalMass := by
    dsimp [x]
    simp_rw [Finset.sum_add_distrib]
    simp only [Finset.sum_const, nsmul_eq_mul]
    have h_card : (Finset.univ.card : ℝ) = (Fintype.card N : ℝ) := rfl
    rw [h_card]
    have h_card_pos : (Fintype.card N : ℝ) > 0 := Nat.cast_pos.mpr Fintype.card_pos
    have h_card_ne : (Fintype.card N : ℝ) ≠ 0 := ne_of_gt h_card_pos
    dsimp only [C]
    field_simp
    ring
  exact ⟨h_sum, h_each⟩

noncomputable def floorMassProjection {N : Type} [Fintype N] [Nonempty N] (ρ : N → ℝ) (ρ_floor : ℝ) (totalMass : ℝ) : N → ℝ :=
  if h : ∃ x : N → ℝ, (∑ i, x i = totalMass) ∧ (∀ i, x i ≥ ρ_floor) then
    Classical.choose h
  else
    fun _ => totalMass / (Fintype.card N : ℝ)

theorem projection_preserves_mass {N : Type} [Fintype N] [Nonempty N] (ρ : N → ℝ) (ρ_floor : ℝ) (totalMass : ℝ)
    (h_feas : totalMass ≥ (Fintype.card N : ℝ) * ρ_floor) :
    (∑ i, floorMassProjection ρ ρ_floor totalMass i) = totalMass := by
  unfold floorMassProjection
  have h_ex := projection_exists_of_feasible ρ_floor totalMass h_feas
  rw [dif_pos h_ex]
  exact (Classical.choose_spec h_ex).1

theorem projection_preserves_floor {N : Type} [Fintype N] [Nonempty N] (ρ : N → ℝ) (ρ_floor : ℝ) (totalMass : ℝ)
    (h_feas : totalMass ≥ (Fintype.card N : ℝ) * ρ_floor) (i : N) :
    floorMassProjection ρ ρ_floor totalMass i ≥ ρ_floor := by
  unfold floorMassProjection
  have h_ex := projection_exists_of_feasible ρ_floor totalMass h_feas
  rw [dif_pos h_ex]
  exact (Classical.choose_spec h_ex).2 i

end D0.Cosmology
