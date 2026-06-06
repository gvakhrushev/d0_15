import D0.Geometry.ArchiveBianchiIdentity
import D0.Matter.GenerationAnomalyPreservation

open scoped BigOperators

namespace D0.Matter

noncomputable def matterStressMatrixFromRepWithGenerations
    (n : Nat) (R : MatterRep) :
    Matrix (D0.archivePhaseIndex n) (D0.archivePhaseIndex n) ℝ :=
  fun i j => (R.anomalySum : ℝ) * D0.archiveCanonicalLaplacian n i j

theorem matterStressMatrix_symmetric
    (n : Nat) (R : MatterRep) :
    D0.MatrixSymmetric (matterStressMatrixFromRepWithGenerations n R) := by
  intro i j
  unfold matterStressMatrixFromRepWithGenerations
  rw [D0.archiveCanonicalLaplacian_symmetric n i j]

theorem matterStressMatrix_conserved
    (n : Nat) (R : MatterRep) :
    D0.archiveDivergence (matterStressMatrixFromRepWithGenerations n R) = 0 := by
  funext i
  unfold D0.archiveDivergence matterStressMatrixFromRepWithGenerations
  rw [← Finset.mul_sum]
  rw [D0.archiveCanonicalLaplacian_row_sum_zero n i]
  simp

noncomputable def matterStressFromRepWithGenerations
    (n : Nat) (R : MatterRep) : D0.ArchiveStressSource n where
  T := matterStressMatrixFromRepWithGenerations n R
  symmetric := matterStressMatrix_symmetric n R
  conserved := matterStressMatrix_conserved n R

theorem generated_matter_source_conserved_if_anomaly_free
    (n : Nat) (R : MatterRep) (_h : R.anomalySum = 0) :
    D0.ArchiveStressSourceConserved (matterStressFromRepWithGenerations n R) := by
  exact (matterStressFromRepWithGenerations n R).conserved

theorem generated_matter_source_zero_if_anomaly_free
    (n : Nat) (R : MatterRep) (h : R.anomalySum = 0) :
    (matterStressFromRepWithGenerations n R).T = 0 := by
  ext i j
  unfold matterStressFromRepWithGenerations matterStressMatrixFromRepWithGenerations
  simp [h]

end D0.Matter
