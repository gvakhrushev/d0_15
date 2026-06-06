import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Probability

noncomputable def waterFill {N : Type} (ρ : N → ℝ) (ν : ℝ) (floor : ℝ) (i : N) : ℝ :=
  max (ρ i - ν) floor

def IsWaterFillingRoot {N : Type} [Fintype N] (ρ : N → ℝ) (M : ℝ) (floor : ℝ) (ν : ℝ) : Prop :=
  ∑ i, waterFill ρ ν floor i = M

theorem waterFill_preserves_floor {N : Type} (ρ : N → ℝ) (ν : ℝ) (floor : ℝ) (i : N) :
    waterFill ρ ν floor i ≥ floor := by
  unfold waterFill
  exact le_max_right (ρ i - ν) floor

theorem waterFill_mass_if_root {N : Type} [Fintype N] (ρ : N → ℝ) (M : ℝ) (floor : ℝ) (ν : ℝ)
    (h_root : IsWaterFillingRoot ρ M floor ν) :
    ∑ i, waterFill ρ ν floor i = M :=
  h_root

theorem feasibility {N : Type} [Fintype N] [Nonempty N] (M floor : ℝ) (h_feas : M ≥ (Fintype.card N : ℝ) * floor) :
    ∃ ρ_new : N → ℝ, (∀ i, ρ_new i ≥ floor) ∧ (∑ i, ρ_new i = M) := by
  let cardN := (Fintype.card N : ℝ)
  have h_card_pos : cardN > 0 := Nat.cast_pos.mpr Fintype.card_pos
  have h_card_ne : cardN ≠ 0 := ne_of_gt h_card_pos
  let diff := (M - cardN * floor) / cardN
  have h_diff_nonneg : diff ≥ 0 := by
    unfold diff
    apply div_nonneg
    · linarith
    · linarith
  let ρ_new := fun (_ : N) => floor + diff
  use ρ_new
  constructor
  · intro i
    dsimp [ρ_new]
    unfold diff
    linarith
  · dsimp [ρ_new]
    simp only [Finset.sum_const, nsmul_eq_mul]
    have h_univ_card : (Finset.univ.card : ℝ) = cardN := rfl
    rw [h_univ_card]
    unfold diff
    field_simp [h_card_ne]
    ring

end D0.Probability
