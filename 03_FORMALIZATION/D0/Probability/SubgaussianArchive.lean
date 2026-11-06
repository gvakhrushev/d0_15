import D0.Probability.FiniteArchiveMeasure
import Mathlib.Probability.ProbabilityMassFunction.Integrals
import Mathlib.Probability.Moments.SubGaussian

open scoped BigOperators

namespace D0

def archiveMean (mu : FiniteArchiveMeasure) (k : Fin 4) : Rat :=
  Finset.univ.sum (fun i : Fin mu.atomCount => mu.weight i * mu.point i k)

def CenteredFiniteArchiveMeasure (mu : FiniteArchiveMeasure) : Prop :=
  forall k : Fin 4, archiveMean mu k = 0

noncomputable def finiteArchivePMF (mu : FiniteArchiveMeasure) :
    PMF (Fin mu.atomCount) :=
  PMF.ofFintype
    (fun i => ENNReal.ofReal (mu.weight i : ℝ))
    (by
      have hsum : (∑ i : Fin mu.atomCount, (mu.weight i : ℝ)) = 1 := by
        exact_mod_cast mu.total_one
      have hnonneg (i : Fin mu.atomCount) : 0 ≤ (mu.weight i : ℝ) := by
        exact_mod_cast mu.nonneg i
      rw [← ENNReal.ofReal_sum_of_nonneg
        (s := Finset.univ) (f := fun i : Fin mu.atomCount => (mu.weight i : ℝ))]
      · rw [hsum]
        simp
      · intro i hi
        exact hnonneg i)

def finiteArchiveCoordinate (mu : FiniteArchiveMeasure) (k : Fin 4)
    (i : Fin mu.atomCount) : ℝ :=
  (mu.point i k : ℝ)

def finiteArchiveProjection (mu : FiniteArchiveMeasure) (u : Fin 4 → ℝ)
    (i : Fin mu.atomCount) : ℝ :=
  Finset.univ.sum (fun k => u k * finiteArchiveCoordinate mu k i)

/-- The PMF has a support point outside every hyperplane through the origin. -/
def NotHyperplaneSupported (mu : FiniteArchiveMeasure) : Prop :=
  ∀ u : Fin 4 → ℝ, (∃ k, u k ≠ 0) →
    ∃ i, 0 < (mu.weight i : ℝ) ∧ finiteArchiveProjection mu u i ≠ 0

def archiveCrossAxis (i : Fin 8) : Fin 4 :=
  ⟨i.val / 2, by omega⟩

noncomputable def archiveProjectionRadius (u : Fin 4 → ℝ) : NNReal :=
  ⟨(Finset.univ.sum (fun k : Fin 4 => |u k|)) / 5,
    div_nonneg
      (Finset.sum_nonneg fun k (_hk : k ∈ Finset.univ) => abs_nonneg (u k))
      (by norm_num)⟩

def ArchiveBoundedByDelta (mu : FiniteArchiveMeasure) (u : Fin 4 → ℝ)
    (delta : NNReal) : Prop :=
  ∀ i, finiteArchiveProjection mu u i ∈ Set.Icc (-(delta : ℝ)) (delta : ℝ)

noncomputable def archiveHoeffdingVariance (delta : NNReal) : NNReal :=
  ((‖(delta : ℝ) + (delta : ℝ)‖₊ / 2) ^ 2)

def Subgaussian (mu : FiniteArchiveMeasure) : Prop :=
  ∀ u : Fin 4 → ℝ,
    ProbabilityTheory.HasSubgaussianMGF (finiteArchiveProjection mu u)
      (archiveHoeffdingVariance (archiveProjectionRadius u))
      (finiteArchivePMF mu).toMeasure

def ArchiveCovarianceQuadratic (mu : FiniteArchiveMeasure) (u : Fin 4 → ℝ) : ℝ :=
  Finset.univ.sum fun i =>
    (mu.weight i : ℝ) * (finiteArchiveProjection mu u i) ^ 2

def ArchiveCovarianceSlack (mu : FiniteArchiveMeasure) : Prop :=
  ∀ u : Fin 4 → ℝ,
    ArchiveCovarianceQuadratic mu u ≤
      (1 / 4 : ℝ) * Finset.univ.sum (fun k : Fin 4 => (u k) ^ 2)

theorem finiteArchivePMF_integral_coordinate (mu : FiniteArchiveMeasure)
    (k : Fin 4) :
    (∫ i, finiteArchiveCoordinate mu k i ∂(finiteArchivePMF mu).toMeasure) =
      (archiveMean mu k : ℝ) := by
  rw [PMF.integral_eq_sum]
  have hweight (i : Fin mu.atomCount) :
      ((finiteArchivePMF mu) i).toReal = (mu.weight i : ℝ) := by
    simp [finiteArchivePMF, ENNReal.toReal_ofReal, mu.nonneg i]
  simp_rw [hweight, finiteArchiveCoordinate, smul_eq_mul]
  simp only [archiveMean, Rat.cast_sum, Rat.cast_mul]

theorem finiteArchivePMF_integral_projection (mu : FiniteArchiveMeasure)
    (u : Fin 4 → ℝ) :
    (∫ i, finiteArchiveProjection mu u i ∂(finiteArchivePMF mu).toMeasure) =
      Finset.univ.sum (fun k => u k * (archiveMean mu k : ℝ)) := by
  rw [PMF.integral_eq_sum]
  have hweight (i : Fin mu.atomCount) :
      ((finiteArchivePMF mu) i).toReal = (mu.weight i : ℝ) := by
    simp [finiteArchivePMF, ENNReal.toReal_ofReal, mu.nonneg i]
  simp_rw [hweight, smul_eq_mul]
  simp_rw [finiteArchiveProjection, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro k hk
  calc
    Finset.univ.sum (fun i => (mu.weight i : ℝ) *
        (u k * finiteArchiveCoordinate mu k i)) =
        u k * Finset.univ.sum (fun i => (mu.weight i : ℝ) *
          finiteArchiveCoordinate mu k i) := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro i hi
            ring
    _ = u k * (archiveMean mu k : ℝ) := by
      have hcoord :
          Finset.univ.sum (fun i => (mu.weight i : ℝ) *
            finiteArchiveCoordinate mu k i) = (archiveMean mu k : ℝ) := by
        have h := finiteArchivePMF_integral_coordinate mu k
        rw [PMF.integral_eq_sum] at h
        simpa [hweight, smul_eq_mul] using h
      rw [hcoord]

theorem finiteProbability_hasSubgaussianMGF_of_centered_range
    {alpha : Type} [Fintype alpha] [MeasurableSpace alpha]
    [MeasurableSingletonClass alpha] (p : PMF alpha) (X : alpha → ℝ)
    {a b : ℝ}
    (hcenter : (∫ x, X x ∂p.toMeasure) = 0)
    (hrange : ∀ x, X x ∈ Set.Icc a b) :
    ProbabilityTheory.HasSubgaussianMGF X ((‖b - a‖₊ / 2) ^ 2) p.toMeasure := by
  apply ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
  · fun_prop
  · filter_upwards [] with x
    exact hrange x
  · exact hcenter

theorem archive_measure_subgaussian_from_bounded
    (mu : FiniteArchiveMeasure) (u : Fin 4 → ℝ) (delta : NNReal)
    (hcenter : CenteredFiniteArchiveMeasure mu)
    (hbounded : ArchiveBoundedByDelta mu u delta) :
    ProbabilityTheory.HasSubgaussianMGF (finiteArchiveProjection mu u)
      (archiveHoeffdingVariance delta) (finiteArchivePMF mu).toMeasure := by
  have hmean :
      (∫ i, finiteArchiveProjection mu u i ∂(finiteArchivePMF mu).toMeasure) = 0 := by
    rw [finiteArchivePMF_integral_projection]
    apply Finset.sum_eq_zero
    intro k hk
    rw [hcenter k]
    ring
  have hmgf := finiteProbability_hasSubgaussianMGF_of_centered_range
    (finiteArchivePMF mu) (finiteArchiveProjection mu u)
    (a := -(delta : ℝ)) (b := (delta : ℝ)) hmean hbounded
  simpa [archiveHoeffdingVariance] using hmgf

theorem d0ArchiveMeasure_centered :
    CenteredFiniteArchiveMeasure d0ArchiveMeasure := by
  intro k
  change
    Finset.univ.sum
      (fun i : Fin 8 => archiveCrossWeight i * archiveCrossVector i k) = 0
  fin_cases k <;>
    simp [Fin.sum_univ_succ, archiveCrossWeight, archiveCrossVector] <;>
    norm_num

theorem archiveStageMeasure_centered (n : Nat) :
    CenteredFiniteArchiveMeasure (archiveStageMeasure n) := by
  exact d0ArchiveMeasure_centered

theorem d0ArchiveMeasure_projection_axis (u : Fin 4 → ℝ) (i : Fin 8) :
    ∃ k : Fin 4,
      finiteArchiveProjection d0ArchiveMeasure u i = u k / 5 ∨
        finiteArchiveProjection d0ArchiveMeasure u i = -u k / 5 := by
  fin_cases i
  · exact ⟨0, Or.inl (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨0, Or.inr (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨1, Or.inl (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨1, Or.inr (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨2, Or.inl (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨2, Or.inr (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨3, Or.inl (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩
  · exact ⟨3, Or.inr (by simp [finiteArchiveProjection, finiteArchiveCoordinate,
      d0ArchiveMeasure, archiveCrossVector, Fin.sum_univ_succ]; ring)⟩

theorem d0ArchiveMeasure_positive_axis_projection (u : Fin 4 → ℝ) (k : Fin 4) :
    finiteArchiveProjection d0ArchiveMeasure u
      ⟨2 * k.val, by simp [d0ArchiveMeasure]; omega⟩ = u k / 5 := by
  fin_cases k <;>
    simp [finiteArchiveProjection, finiteArchiveCoordinate, d0ArchiveMeasure,
      archiveCrossVector, Fin.sum_univ_succ] <;> ring

theorem d0ArchiveMeasure_projection_square (u : Fin 4 → ℝ) (i : Fin 8) :
    (finiteArchiveProjection d0ArchiveMeasure u i) ^ 2 =
      (u (archiveCrossAxis i)) ^ 2 / 25 := by
  fin_cases i <;>
    simp [finiteArchiveProjection, finiteArchiveCoordinate, d0ArchiveMeasure,
      archiveCrossVector, archiveCrossAxis, Fin.sum_univ_succ] <;> ring

theorem d0ArchiveMeasure_projection_bounded (u : Fin 4 → ℝ) :
    ArchiveBoundedByDelta d0ArchiveMeasure u (archiveProjectionRadius u) := by
  intro i
  obtain ⟨k, hprojection | hprojection⟩ := d0ArchiveMeasure_projection_axis u i
  · have hsum : |u k| ≤ Finset.univ.sum (fun j : Fin 4 => |u j|) :=
      Finset.single_le_sum (fun j _ => abs_nonneg (u j)) (Finset.mem_univ k)
    have hbound : |u k / 5| ≤ (archiveProjectionRadius u : ℝ) := by
      change |u k / 5| ≤ (Finset.univ.sum (fun j : Fin 4 => |u j|)) / 5
      rw [abs_div, abs_of_pos (by norm_num : (0 : ℝ) < 5)]
      exact (div_le_div_iff_of_pos_right (by norm_num : (0 : ℝ) < 5)).2 hsum
    rw [Set.mem_Icc, hprojection]
    exact abs_le.mp hbound
  · have hsum : |u k| ≤ Finset.univ.sum (fun j : Fin 4 => |u j|) :=
      Finset.single_le_sum (fun j _ => abs_nonneg (u j)) (Finset.mem_univ k)
    have hbound : |u k / 5| ≤ (archiveProjectionRadius u : ℝ) := by
      change |u k / 5| ≤ (Finset.univ.sum (fun j : Fin 4 => |u j|)) / 5
      rw [abs_div, abs_of_pos (by norm_num : (0 : ℝ) < 5)]
      exact (div_le_div_iff_of_pos_right (by norm_num : (0 : ℝ) < 5)).2 hsum
    rw [Set.mem_Icc, hprojection]
    have hinterval := abs_le.mp hbound
    constructor <;> linarith

theorem archiveStageMeasure_projection_bounded (n : Nat) (u : Fin 4 → ℝ) :
    ArchiveBoundedByDelta (archiveStageMeasure n) u (archiveProjectionRadius u) := by
  exact d0ArchiveMeasure_projection_bounded u

theorem archiveStageMeasure_subgaussian (n : Nat) :
    Subgaussian (archiveStageMeasure n) := by
  intro u
  exact archive_measure_subgaussian_from_bounded
    (archiveStageMeasure n) u (archiveProjectionRadius u)
    (archiveStageMeasure_centered n) (archiveStageMeasure_projection_bounded n u)

theorem d0ArchiveMeasure_not_hyperplane_supported :
    NotHyperplaneSupported d0ArchiveMeasure := by
  intro u hu
  obtain ⟨k, hk⟩ := hu
  refine ⟨⟨2 * k.val, by simp [d0ArchiveMeasure]; omega⟩, ?_, ?_⟩
  · change 0 < (archiveCrossWeight (⟨2 * k.val, by omega⟩ : Fin 8) : ℝ)
    norm_num [archiveCrossWeight]
  · rw [d0ArchiveMeasure_positive_axis_projection]
    exact div_ne_zero hk (by norm_num)

theorem archiveStageMeasure_not_hyperplane_supported (n : Nat) :
    NotHyperplaneSupported (archiveStageMeasure n) := by
  exact d0ArchiveMeasure_not_hyperplane_supported

theorem d0ArchiveMeasure_covariance_formula (u : Fin 4 → ℝ) :
    ArchiveCovarianceQuadratic d0ArchiveMeasure u =
      (1 / 100 : ℝ) * Finset.univ.sum (fun k : Fin 4 => (u k) ^ 2) := by
  change Finset.univ.sum (fun i : Fin 8 =>
      (archiveCrossWeight i : ℝ) * (finiteArchiveProjection d0ArchiveMeasure u i) ^ 2) =
    (1 / 100 : ℝ) * Finset.univ.sum (fun k : Fin 4 => (u k) ^ 2)
  simp_rw [d0ArchiveMeasure_projection_square]
  simp_rw [Fin.sum_univ_succ]
  norm_num [archiveCrossWeight, archiveCrossAxis]
  have h2 : (⟨2, by decide⟩ : Fin 4) = (2 : Fin 4) := by
    apply Fin.ext
    rfl
  have h3 : (⟨3, by decide⟩ : Fin 4) = Fin.succ (2 : Fin 3) := by
    apply Fin.ext
    rfl
  simp [h2, h3]
  ring

theorem d0ArchiveMeasure_covariance_slack :
    ArchiveCovarianceSlack d0ArchiveMeasure := by
  intro u
  rw [d0ArchiveMeasure_covariance_formula]
  have hsum : 0 ≤ Finset.univ.sum (fun k : Fin 4 => (u k) ^ 2) :=
    Finset.sum_nonneg fun _ _ => sq_nonneg _
  nlinarith

theorem archiveStageMeasure_covariance_slack (n : Nat) :
    ArchiveCovarianceSlack (archiveStageMeasure n) := by
  exact d0ArchiveMeasure_covariance_slack

structure FiniteArchiveHSTSourceAdmissibility (n : Nat) where
  finiteSupport : ArchiveFiniteSupport (archiveStageMeasure n)
  centered : CenteredFiniteArchiveMeasure (archiveStageMeasure n)
  covarianceSlack : ArchiveCovarianceSlack (archiveStageMeasure n)
  subgaussianMGF : Subgaussian (archiveStageMeasure n)
  notHyperplaneSupported : NotHyperplaneSupported (archiveStageMeasure n)

def FiniteArchiveHSTSourceAdmissible (n : Nat) : Prop :=
  Nonempty (FiniteArchiveHSTSourceAdmissibility n)

theorem finiteArchive_hst_source_admissibility (n : Nat) :
    FiniteArchiveHSTSourceAdmissibility n :=
  { finiteSupport := archiveStageMeasure_finite_support n
    centered := archiveStageMeasure_centered n
    covarianceSlack := archiveStageMeasure_covariance_slack n
    subgaussianMGF := archiveStageMeasure_subgaussian n
    notHyperplaneSupported := archiveStageMeasure_not_hyperplane_supported n }

theorem finiteArchive_hst_source_admissible (n : Nat) :
    FiniteArchiveHSTSourceAdmissible n :=
  ⟨finiteArchive_hst_source_admissibility n⟩

structure ArchiveMeasureTowerWitness (n : Nat) where
  measure : FiniteArchiveMeasure
  atomCount_eq : measure.atomCount = archiveFibers n
  centered : CenteredFiniteArchiveMeasure measure

def archiveMeasureFromTower (n : Nat) (w : ArchiveMeasureTowerWitness n) : FiniteArchiveMeasure :=
  w.measure

theorem archive_measure_support_matches_fibers (n : Nat) (w : ArchiveMeasureTowerWitness n) :
  supportCard (archiveMeasureFromTower n w) = archiveFibers n :=
  w.atomCount_eq

theorem archive_measure_centered_from_active_archive_split (n : Nat) (w : ArchiveMeasureTowerWitness n) :
  CenteredFiniteArchiveMeasure (archiveMeasureFromTower n w) :=
  w.centered

end D0
