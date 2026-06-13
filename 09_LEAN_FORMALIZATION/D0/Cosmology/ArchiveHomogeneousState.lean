import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Cosmology

def isHomogeneous {n : Type} (φ : n → ℝ) : Prop :=
  ∃ c : ℝ, φ = fun _ => c

def totalMass {n : Type} [Fintype n] (φ : n → ℝ) : ℝ :=
  ∑ i, φ i

theorem homogeneous_total_eq_value {n : Type} [Fintype n] (φ : n → ℝ) (h : isHomogeneous φ) :
    ∃ c : ℝ, φ = (fun _ => c) ∧ totalMass φ = (Fintype.card n : ℝ) * c := by
  rcases h with ⟨c, rfl⟩
  use c
  constructor
  · rfl
  · unfold totalMass
    simp [Finset.sum_const]

theorem homogeneous_mass_conserving_fixed_point {n : Type} [Fintype n] [Nonempty n]
    (F : (n → ℝ) → (n → ℝ)) (φ : n → ℝ)
    (h_hom : ∀ ψ, isHomogeneous ψ → isHomogeneous (F ψ))
    (h_mass : ∀ ψ, totalMass (F ψ) = totalMass ψ)
    (hφ : isHomogeneous φ) :
    F φ = φ := by
  rcases hφ with ⟨c, rfl⟩
  have hF : isHomogeneous (F (fun _ => c)) := h_hom (fun _ => c) ⟨c, rfl⟩
  rcases hF with ⟨c', hc'⟩
  have h_mass_eq : totalMass (F (fun _ => c)) = totalMass (fun _ => c) := h_mass (fun _ => c)
  rw [hc'] at h_mass_eq
  unfold totalMass at h_mass_eq
  simp [Finset.sum_const] at h_mass_eq
  rw [hc', h_mass_eq]

end D0.Cosmology
