import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Cosmology

def zeroMean {n : Type} [Fintype n] (v : n → ℝ) : Prop :=
  ∑ i, v i = 0

theorem zero_mean_nonzero_has_negative_component {n : Type} [Fintype n] (v : n → ℝ)
    (h_mean : zeroMean v) (h_nz : v ≠ 0) :
    ∃ i, v i < 0 := by
  by_contra h_neg
  push Not at h_neg
  have h_all_zero : ∀ i ∈ Finset.univ, v i = 0 := by
    apply (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => h_neg i)).mp
    exact h_mean
  have h_zero : v = 0 := by
    ext i
    dsimp
    exact h_all_zero i (Finset.mem_univ i)
  exact h_nz h_zero

theorem zero_mean_nonzero_has_positive_component {n : Type} [Fintype n] (v : n → ℝ)
    (h_mean : zeroMean v) (h_nz : v ≠ 0) :
    ∃ i, v i > 0 := by
  by_contra h_pos
  push Not at h_pos
  have h_neg_nonneg : ∀ i, -v i ≥ 0 := by
    intro i
    linarith [h_pos i]
  have h_neg_sum_zero : ∑ i, -v i = 0 := by
    rw [Finset.sum_neg_distrib, h_mean, neg_zero]
  have h_all_zero : ∀ i ∈ Finset.univ, -v i = 0 := by
    apply (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => h_neg_nonneg i)).mp
    exact h_neg_sum_zero
  have h_zero : v = 0 := by
    ext i
    have h_neg_i := h_all_zero i (Finset.mem_univ i)
    dsimp
    linarith
  exact h_nz h_zero

theorem zero_mean_mode_has_underdense_region {n : Type} [Fintype n] (v : n → ℝ)
    (h_mean : zeroMean v) (h_nz : v ≠ 0) :
    ∃ i, v i < 0 := by
  exact zero_mean_nonzero_has_negative_component v h_mean h_nz

end D0.Cosmology
