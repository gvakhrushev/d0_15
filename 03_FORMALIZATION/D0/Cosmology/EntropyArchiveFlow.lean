import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Cosmology.ArchiveHomogeneousState

open scoped BigOperators

namespace D0.Cosmology

noncomputable def meanDensity {n : Type} [Fintype n] (ρ : n → ℝ) : ℝ :=
  (∑ i, ρ i) / (Fintype.card n : ℝ)

noncomputable def centeredDensity {n : Type} [Fintype n] (ρ : n → ℝ) (i : n) : ℝ :=
  ρ i - meanDensity ρ

noncomputable def archiveVolume {n : Type} [Fintype n] (ρ : n → ℝ) : ℝ :=
  (∑ i, 1 / ρ i) / (Fintype.card n : ℝ)

structure EntropyArchiveFlow (N : Type) [Fintype N] [Nonempty N] where
  F : (N → ℝ) → (N → ℝ)
  mass_preserving : ∀ ρ, totalMass (F ρ) = totalMass ρ
  homogeneous_preserving : ∀ ρ, isHomogeneous ρ → isHomogeneous (F ρ)
  positive_floor : ∀ ρ (_h_pos : ∀ i, ρ i > 0), ∃ M > 0, ∀ i, F ρ i ≥ M

theorem homogeneous_fixed_point {N : Type} [Fintype N] [Nonempty N]
    (flow : EntropyArchiveFlow N) (φ : N → ℝ)
    (hφ : isHomogeneous φ) :
    flow.F φ = φ := by
  exact homogeneous_mass_conserving_fixed_point flow.F φ
    flow.homogeneous_preserving flow.mass_preserving hφ

end D0.Cosmology
