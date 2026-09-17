import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Cosmology.ArchiveHomogeneousState
import D0.Cosmology.EntropyArchiveFlow
import Mathlib.Analysis.SpecialFunctions.Exp

open scoped BigOperators

namespace D0.Cosmology

noncomputable def concreteSoftWeight {N : Type} [Fintype N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (ρ : N → ℝ) (i : N) : ℝ :=
  ρ i * Real.exp (η * L_pinv (centeredDensity ρ) i)

noncomputable def concreteZ {N : Type} [Fintype N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (ρ : N → ℝ) : ℝ :=
  ∑ i, concreteSoftWeight η L_pinv ρ i

noncomputable def concreteFlow {N : Type} [Fintype N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (ρ : N → ℝ) (i : N) : ℝ :=
  totalMass ρ * concreteSoftWeight η L_pinv ρ i / concreteZ η L_pinv ρ

lemma concreteZ_pos {N : Type} [Fintype N] [Nonempty N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (ρ : N → ℝ) (h_pos : ∀ i, ρ i > 0) :
    concreteZ η L_pinv ρ > 0 := by
  unfold concreteZ
  apply Finset.sum_pos
  · intro i _
    unfold concreteSoftWeight
    have h1 : ρ i > 0 := h_pos i
    have h2 : Real.exp (η * L_pinv (centeredDensity ρ) i) > 0 := Real.exp_pos _
    exact mul_pos h1 h2
  · exact Finset.univ_nonempty

theorem softmax_flow_mass_preserving {N : Type} [Fintype N] [Nonempty N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (ρ : N → ℝ) (h_pos : ∀ i, ρ i > 0) :
    totalMass (concreteFlow η L_pinv ρ) = totalMass ρ := by
  unfold totalMass concreteFlow
  have hz_pos := concreteZ_pos η L_pinv ρ h_pos
  have hz_ne : concreteZ η L_pinv ρ ≠ 0 := ne_of_gt hz_pos
  have h_num : (∑ i, totalMass ρ * concreteSoftWeight η L_pinv ρ i / concreteZ η L_pinv ρ) =
      totalMass ρ * (∑ i, concreteSoftWeight η L_pinv ρ i) / concreteZ η L_pinv ρ := by
    rw [← Finset.sum_div, ← Finset.mul_sum]
  rw [h_num]
  change totalMass ρ * concreteZ η L_pinv ρ / concreteZ η L_pinv ρ = totalMass ρ
  rw [mul_div_cancel_right₀ _ hz_ne]

theorem homogeneous_state_maps_to_itself {N : Type} [Fintype N] [Nonempty N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (h_lin : L_pinv 0 = 0) (ρ : N → ℝ) (h_hom : isHomogeneous ρ) (h_pos : ∀ i, ρ i > 0) :
    concreteFlow η L_pinv ρ = ρ := by
  funext i
  unfold concreteFlow
  have hz_pos := concreteZ_pos η L_pinv ρ h_pos
  have hz_ne : concreteZ η L_pinv ρ ≠ 0 := ne_of_gt hz_pos
  obtain ⟨c, hc⟩ := h_hom
  have h_mean : meanDensity ρ = c := by
    unfold meanDensity
    rw [hc]
    dsimp
    simp only [Finset.sum_const, nsmul_eq_mul]
    have h_univ_card : (Finset.univ.card : ℝ) = (Fintype.card N : ℝ) := rfl
    rw [h_univ_card]
    have h_card_pos : (Fintype.card N : ℝ) > 0 := Nat.cast_pos.mpr Fintype.card_pos
    have h_card_ne : (Fintype.card N : ℝ) ≠ 0 := ne_of_gt h_card_pos
    field_simp
  have h_centered : ∀ j, centeredDensity ρ j = 0 := by
    intro j
    unfold centeredDensity
    rw [congr_fun hc j, h_mean, sub_self]
  have h_centered_vec : centeredDensity ρ = 0 := by
    funext j
    exact h_centered j
  have h_phi : L_pinv (centeredDensity ρ) = 0 := by
    rw [h_centered_vec, h_lin]
  have h_weight : ∀ j, concreteSoftWeight η L_pinv ρ j = ρ j := by
    intro j
    unfold concreteSoftWeight
    rw [h_phi]
    simp
  have h_z : concreteZ η L_pinv ρ = totalMass ρ := by
    unfold concreteZ totalMass
    apply Finset.sum_congr rfl
    intro j _
    exact h_weight j
  rw [h_z]
  rw [h_weight i]
  have h_mass_pos : totalMass ρ > 0 := by
    unfold totalMass
    apply Finset.sum_pos
    · intro j _
      exact h_pos j
    · exact Finset.univ_nonempty
  have h_mass_ne : totalMass ρ ≠ 0 := ne_of_gt h_mass_pos
  rw [mul_div_cancel_left₀ (ρ i) h_mass_ne]

theorem positivity_if_initial_positive {N : Type} [Fintype N] [Nonempty N] (η : ℝ) (L_pinv : (N → ℝ) → (N → ℝ)) (ρ : N → ℝ) (h_pos : ∀ i, ρ i > 0) :
    ∀ i, concreteFlow η L_pinv ρ i > 0 := by
  intro i
  unfold concreteFlow
  have h_mass_pos : totalMass ρ > 0 := by
    unfold totalMass
    apply Finset.sum_pos
    · intro j _
      exact h_pos j
    · exact Finset.univ_nonempty
  have h_weight_pos : concreteSoftWeight η L_pinv ρ i > 0 := by
    unfold concreteSoftWeight
    exact mul_pos (h_pos i) (Real.exp_pos _)
  have h_num_pos : totalMass ρ * concreteSoftWeight η L_pinv ρ i > 0 := mul_pos h_mass_pos h_weight_pos
  have hz_pos := concreteZ_pos η L_pinv ρ h_pos
  exact div_pos h_num_pos hz_pos

theorem centered_source_zero_mean {N : Type} [Fintype N] [Nonempty N] (ρ : N → ℝ) :
    totalMass (centeredDensity ρ) = 0 := by
  unfold totalMass centeredDensity meanDensity
  rw [Finset.sum_sub_distrib]
  simp only [Finset.sum_const, nsmul_eq_mul]
  have h_card_pos : (Fintype.card N : ℝ) > 0 := Nat.cast_pos.mpr Fintype.card_pos
  have h_card_ne : (Fintype.card N : ℝ) ≠ 0 := ne_of_gt h_card_pos
  have h_univ_card : (Finset.univ.card : ℝ) = (Fintype.card N : ℝ) := rfl
  rw [h_univ_card]
  field_simp
  ring

end D0.Cosmology
