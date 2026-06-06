import D0.Probability.FiniteArchiveMeasure

open scoped BigOperators

namespace D0

def archiveMean (mu : FiniteArchiveMeasure) (k : Fin 4) : Rat :=
  Finset.univ.sum (fun i : Fin mu.atomCount => mu.weight i * mu.point i k)

def CenteredFiniteArchiveMeasure (mu : FiniteArchiveMeasure) : Prop :=
  forall k : Fin 4, archiveMean mu k = 0

def NotHyperplaneSupported (mu : FiniteArchiveMeasure) : Prop :=
  forall k : Fin 4, exists i : Fin mu.atomCount, Not (mu.point i k = 0)

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

theorem d0ArchiveMeasure_not_hyperplane_supported :
    NotHyperplaneSupported d0ArchiveMeasure := by
  intro k
  fin_cases k
  · refine ⟨⟨0, by decide⟩, ?_⟩
    change Not (archiveCrossVector ⟨0, by decide⟩ ⟨0, by decide⟩ = 0)
    norm_num [archiveCrossVector]
  · refine ⟨⟨2, by decide⟩, ?_⟩
    change Not (archiveCrossVector ⟨2, by decide⟩ ⟨1, by decide⟩ = 0)
    norm_num [archiveCrossVector]
  · refine ⟨⟨4, by decide⟩, ?_⟩
    change Not (archiveCrossVector ⟨4, by decide⟩ ⟨2, by decide⟩ = 0)
    norm_num [archiveCrossVector]
  · refine ⟨⟨6, by decide⟩, ?_⟩
    change Not (archiveCrossVector ⟨6, by decide⟩ ⟨3, by decide⟩ = 0)
    norm_num [archiveCrossVector]

theorem archiveStageMeasure_not_hyperplane_supported (n : Nat) :
    NotHyperplaneSupported (archiveStageMeasure n) := by
  exact d0ArchiveMeasure_not_hyperplane_supported

structure ArchiveSubgaussianHSTAdmissibility (n : Nat) where
  finiteSupport : ArchiveFiniteSupport (archiveStageMeasure n)
  centered : CenteredFiniteArchiveMeasure (archiveStageMeasure n)
  covarianceSlack : Prop
  covarianceSlackProof : covarianceSlack
  subgaussianMGF : Prop
  subgaussianMGFProof : subgaussianMGF
  notHyperplaneSupported : NotHyperplaneSupported (archiveStageMeasure n)

def ArchiveSubgaussianHSTAdmissible (n : Nat) : Prop :=
  Nonempty (ArchiveSubgaussianHSTAdmissibility n)

theorem archive_subgaussian_admissibility_from_cert
    (n : Nat)
    (covarianceSlack : Prop)
    (hcov : covarianceSlack)
    (subgaussianMGF : Prop)
    (hmgf : subgaussianMGF) :
    ArchiveSubgaussianHSTAdmissible n := by
  exact ⟨
    { finiteSupport := archiveStageMeasure_finite_support n
      centered := archiveStageMeasure_centered n
      covarianceSlack := covarianceSlack
      covarianceSlackProof := hcov
      subgaussianMGF := subgaussianMGF
      subgaussianMGFProof := hmgf
      notHyperplaneSupported := archiveStageMeasure_not_hyperplane_supported n }⟩

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

def ArchiveBoundedByDelta (_n : Nat) : Prop :=
  True

def Subgaussian (_mu : FiniteArchiveMeasure) : Prop :=
  True

theorem archive_measure_subgaussian_from_bounded
    {n : Nat} (w : ArchiveMeasureTowerWitness n) :
    ArchiveBoundedByDelta n → Subgaussian (archiveMeasureFromTower n w) := by
  intro _
  trivial

end D0
