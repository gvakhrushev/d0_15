import D0.Geometry.ArchivePoissonEquation
import D0.Interface.ScalarPoissonReduction
import D0.Geometry.ArchiveCanonicalLaplacian
import Mathlib.Data.Real.Basic

open scoped BigOperators

namespace D0

def residual (n : Nat) (φ : ArchivePotential n) (ρ_seam : archivePhaseIndex n → ℝ) :
    archivePhaseIndex n → ℝ :=
  fun i => Matrix.mulVec (archiveCanonicalLaplacian n) φ i - ρ_seam i

def SeamStationarity (n : Nat) (φ : ArchivePotential n) (ρ_seam : archivePhaseIndex n → ℝ) : Prop :=
  ScalarSectorStationary n φ ρ_seam

def phaseInnerProduct {n : Nat} (u v : archivePhaseIndex n → ℝ) : ℝ :=
  ∑ i : archivePhaseIndex n, u i * v i

noncomputable def effectiveEnergy (n : Nat) (φ : ArchivePotential n) (ρ : archivePhaseIndex n → ℝ) : ℝ :=
  (1 / 2 : ℝ) * phaseInnerProduct φ (Matrix.mulVec (archiveCanonicalLaplacian n) φ) -
    phaseInnerProduct ρ φ

theorem seam_stationarity_residual_constant
    (n : Nat) (φ : ArchivePotential n) (ρ_seam : archivePhaseIndex n → ℝ)
    (h_stat : SeamStationarity n φ ρ_seam) :
    ∃ c : ℝ, residual n φ ρ_seam = constantPotential c := by
  let i0 : archivePhaseIndex n := ⟨0, by unfold archiveFibers; omega⟩
  use residual n φ ρ_seam i0
  funext i
  unfold residual constantPotential
  exact scalar_stationarity_implies_constant_difference n φ ρ_seam h_stat i i0

theorem neutral_constantPotential_coeff_zero {n : Nat} (c : ℝ)
    (h_neutral : NeutralSource (constantPotential (n := n) c)) :
    c = 0 := by
  unfold NeutralSource constantPotential at h_neutral
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at h_neutral
  have h_fibers : 0 < archiveFibers n := by
    unfold archiveFibers
    omega
  have h_fibers_real : (archiveFibers n : ℝ) ≠ 0 := by
    exact Nat.cast_ne_zero.mpr (ne_of_gt h_fibers)
  exact (mul_eq_zero.mp h_neutral).resolve_left h_fibers_real

theorem neutral_residual_constant_coeff_zero
    {n : Nat} {φ : ArchivePotential n} {ρ_seam : archivePhaseIndex n → ℝ} {c : ℝ}
    (h_const : residual n φ ρ_seam = constantPotential c)
    (h_neutral : NeutralSource (residual n φ ρ_seam)) :
    c = 0 := by
  rw [h_const] at h_neutral
  exact neutral_constantPotential_coeff_zero c h_neutral

theorem residual_neutral_of_neutral_source
    (n : Nat) (φ : ArchivePotential n) (ρ_seam : archivePhaseIndex n → ℝ)
    (hρ : NeutralSource ρ_seam) :
    NeutralSource (residual n φ ρ_seam) := by
  unfold NeutralSource residual
  rw [Finset.sum_sub_distrib, archiveCanonicalLaplacian_sum_zero, hρ]
  ring

theorem seam_stationarity_neutral_source_implies_poisson
    (n : Nat) (φ : ArchivePotential n) (ρ_seam : archivePhaseIndex n → ℝ)
    (h_stat : SeamStationarity n φ ρ_seam)
    (hρ : NeutralSource ρ_seam) :
    ArchivePoissonEquation φ ρ_seam := by
  obtain ⟨c, h_const⟩ := seam_stationarity_residual_constant n φ ρ_seam h_stat
  have h_res_neutral := residual_neutral_of_neutral_source n φ ρ_seam hρ
  have hc : c = 0 := neutral_residual_constant_coeff_zero h_const h_res_neutral
  unfold ArchivePoissonEquation
  funext i
  have hi := congr_fun h_const i
  unfold residual constantPotential at hi
  rw [hc] at hi
  exact sub_eq_zero.mp hi

theorem effectiveEnergy_eq_neg_half_source_pairing_of_poisson
    (n : Nat) (φ : ArchivePotential n) (ρ : archivePhaseIndex n → ℝ)
    (h : ArchivePoissonEquation φ ρ) :
    effectiveEnergy n φ ρ = -(1 / 2 : ℝ) * phaseInnerProduct ρ φ := by
  change Matrix.mulVec (archiveCanonicalLaplacian n) φ = ρ at h
  have h_inner :
      phaseInnerProduct φ (Matrix.mulVec (archiveCanonicalLaplacian n) φ) =
        phaseInnerProduct ρ φ := by
    unfold phaseInnerProduct
    rw [h]
    apply Finset.sum_congr rfl
    intro i _
    ring
  unfold effectiveEnergy
  rw [h_inner]
  ring

theorem SeamScalarSource (n : Nat) (φ : ArchivePotential n) (ρ_seam : archivePhaseIndex n → ℝ)
    (h_stat : SeamStationarity n φ ρ_seam)
    (hρ : NeutralSource ρ_seam) :
    ArchivePoissonEquation φ ρ_seam :=
  seam_stationarity_neutral_source_implies_poisson n φ ρ_seam h_stat hρ

theorem SeamSourceUniqueness (n : Nat) (ρ_seam : archivePhaseIndex n → ℝ) (hρ : NeutralSource ρ_seam)
    (φ1 φ2 : ArchivePotential n)
    (h1 : ArchivePoissonEquation φ1 ρ_seam)
    (h2 : ArchivePoissonEquation φ2 ρ_seam) :
    ∃ c : ℝ, φ1 - φ2 = constantPotential c :=
  poisson_solution_unique_mod_constant ρ_seam hρ φ1 φ2 h1 h2

theorem ScalarOffDiagonalDecoupling (n : Nat) (φ : ArchivePotential n) :
  (∑ i : archivePhaseIndex n, (Matrix.mulVec (archiveCanonicalLaplacian n) φ) i) = 0 :=
  archiveCanonicalLaplacian_sum_zero n φ

theorem EffectiveEnergyPositivity (n : Nat) (φ : ArchivePotential n) (ρ : archivePhaseIndex n → ℝ)
    (h : ArchivePoissonEquation φ ρ) :
    0 ≤ - effectiveEnergy n φ ρ := by
  rw [effectiveEnergy_eq_neg_half_source_pairing_of_poisson n φ ρ h]
  have h_eq : - (-(1 / 2 : ℝ) * phaseInnerProduct ρ φ) = (1 / 2 : ℝ) * phaseInnerProduct ρ φ := by ring
  rw [h_eq]
  have hL : Matrix.mulVec (archiveCanonicalLaplacian n) φ = ρ := h
  have h_inner : phaseInnerProduct ρ φ = matrixQuadraticForm (archiveCanonicalLaplacian n) φ := by
    rw [← hL]
    unfold phaseInnerProduct matrixQuadraticForm Matrix.mulVec dotProduct
    dsimp
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro x _
    ring
  rw [h_inner]
  have h_nonneg := archiveCanonicalLaplacian_nonnegative n φ
  positivity

end D0
