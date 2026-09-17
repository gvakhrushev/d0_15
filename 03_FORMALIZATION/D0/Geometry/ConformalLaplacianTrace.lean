import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Cosmology.EntropyArchiveFlow

open scoped BigOperators

namespace D0.Geometry

open D0.Cosmology

noncomputable def Wρ {N : Type} [Fintype N] [DecidableEq N] (ρ : N → ℝ) : Matrix N N ℝ :=
  Matrix.diagonal (fun i => 1 / Real.sqrt (ρ i))

noncomputable def weightedLaplacian {N : Type} [Fintype N] [DecidableEq N]
    (L : Matrix N N ℝ) (ρ : N → ℝ) : Matrix N N ℝ :=
  Wρ ρ * L * Wρ ρ

theorem trace_weighted_laplacian {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) :
    Matrix.trace (weightedLaplacian L ρ) = ∑ i, L i i / ρ i := by
  unfold weightedLaplacian Matrix.trace
  dsimp
  have h_diag : ∀ i, (Wρ ρ * L * Wρ ρ) i i = L i i / ρ i := by
    intro i
    rw [Matrix.mul_apply]
    simp_rw [Matrix.mul_apply]
    unfold Wρ
    simp only [Matrix.diagonal_apply, mul_ite, ite_mul, mul_zero, zero_mul, Finset.sum_ite_eq, Finset.sum_ite_eq', Finset.mem_univ, if_true]
    have h_sqrt : Real.sqrt (ρ i) * Real.sqrt (ρ i) = ρ i := Real.mul_self_sqrt (le_of_lt (h_pos i))
    calc
      (1 / Real.sqrt (ρ i) * L i i) * (1 / Real.sqrt (ρ i)) = L i i * (1 / (Real.sqrt (ρ i) * Real.sqrt (ρ i))) := by ring
      _ = L i i * (1 / ρ i) := by rw [h_sqrt]
      _ = L i i / ρ i := by ring
  simp only [h_diag]

theorem regular_trace_volume_proxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) (d : ℝ) (h_eq : ∀ i, L i i = d) :
    Matrix.trace (weightedLaplacian L ρ) = d * ∑ i, 1 / ρ i := by
  rw [trace_weighted_laplacian L ρ h_pos]
  simp_rw [h_eq]
  have h_div : ∀ i, d / ρ i = d * (1 / ρ i) := by
    intro i
    ring
  simp_rw [h_div]
  rw [← Finset.mul_sum]

theorem archiveVolume_heat_trace_proxy {N : Type} [Fintype N] [Nonempty N] [DecidableEq N]
    (L : Matrix N N ℝ) (ρ : N → ℝ) (h_pos : ∀ i, ρ i > 0) (d : ℝ) (h_eq : ∀ i, L i i = d)
    (hd : d ≠ 0) :
    archiveVolume ρ = (1 / ((Fintype.card N : ℝ) * d)) * Matrix.trace (weightedLaplacian L ρ) := by
  unfold archiveVolume
  rw [regular_trace_volume_proxy L ρ h_pos d h_eq]
  have h_card_pos : (Fintype.card N : ℝ) > 0 := Nat.cast_pos.mpr Fintype.card_pos
  have h_card_ne : (Fintype.card N : ℝ) ≠ 0 := ne_of_gt h_card_pos
  field_simp
  try ring

end D0.Geometry
