import D0.Geometry.ArchiveFieldEquation

open scoped BigOperators

namespace D0

theorem archiveCanonicalLaplacian_row_sum_zero (n : Nat)
    (i : archivePhaseIndex n) :
    ∑ j : archivePhaseIndex n, archiveCanonicalLaplacian n i j = 0 := by
  have h := congr_fun (archiveCanonicalLaplacian_constant_zero n 1) i
  unfold Matrix.mulVec dotProduct at h
  simpa using h

theorem archiveLiftOperator_row_sum_one (n : Nat)
    (i : archivePhaseIndex (n+1)) :
    ∑ j : archivePhaseIndex n, archiveLiftOperator n i j = 1 := by
  unfold archiveLiftOperator
  rw [Finset.sum_eq_single (archiveRGPhaseProjection n i)]
  · simp
  · intro j _hj hne
    rw [if_neg]
    exact fun h => hne h.symm
  · intro hmem
    exact False.elim (hmem (Finset.mem_univ _))

theorem seamCommutator_row_sum_zero (n : Nat)
    (i : archivePhaseIndex (n+1)) :
    ∑ j : archivePhaseIndex n, seamCommutator n i j = 0 := by
  unfold seamCommutator seamFineTransport seamLiftedCoarseTransport rectangularMatrixMul
  change (∑ j : archivePhaseIndex n,
      ((∑ x : archivePhaseIndex (n+1),
          archiveCanonicalLaplacian (n+1) i x * archiveLiftOperator n x j) -
        (∑ x : archivePhaseIndex n,
          archiveLiftOperator n i x * archiveCanonicalLaplacian n x j))) = 0
  rw [Finset.sum_sub_distrib]
  have hfine :
      (∑ j : archivePhaseIndex n,
        ∑ x : archivePhaseIndex (n+1),
          archiveCanonicalLaplacian (n+1) i x * archiveLiftOperator n x j) = 0 := by
    rw [Finset.sum_comm]
    simp_rw [← Finset.mul_sum]
    simp_rw [archiveLiftOperator_row_sum_one n]
    simp [archiveCanonicalLaplacian_row_sum_zero (n+1) i]
  have hcoarse :
      (∑ j : archivePhaseIndex n,
        ∑ x : archivePhaseIndex n,
          archiveLiftOperator n i x * archiveCanonicalLaplacian n x j) = 0 := by
    rw [Finset.sum_comm]
    simp_rw [← Finset.mul_sum]
    simp_rw [archiveCanonicalLaplacian_row_sum_zero n]
    simp
  rw [hfine, hcoarse]
  simp

theorem curvature_gradient_conserved (n : Nat) :
    archiveDivergence (archiveCurvatureGradient n) = 0 := by
  funext i
  unfold archiveDivergence archiveCurvatureGradient
  change (∑ j : archivePhaseIndex n,
      -2 * ∑ a : archivePhaseIndex (n+1),
        archiveLiftOperator n a i * seamCommutator n a j) = 0
  calc
    (∑ j : archivePhaseIndex n,
      -2 * ∑ a : archivePhaseIndex (n+1),
        archiveLiftOperator n a i * seamCommutator n a j)
        = -2 * ∑ j : archivePhaseIndex n,
            ∑ a : archivePhaseIndex (n+1),
              archiveLiftOperator n a i * seamCommutator n a j := by
      rw [Finset.mul_sum]
    _ = -2 * ∑ a : archivePhaseIndex (n+1),
            ∑ j : archivePhaseIndex n,
              archiveLiftOperator n a i * seamCommutator n a j := by
      rw [Finset.sum_comm]
    _ = -2 * ∑ a : archivePhaseIndex (n+1),
            archiveLiftOperator n a i *
              ∑ j : archivePhaseIndex n, seamCommutator n a j := by
      simp_rw [← Finset.mul_sum]
    _ = 0 := by
      simp [seamCommutator_row_sum_zero n]

def ArchiveStressSourceConserved {n : Nat} (T : ArchiveStressSource n) : Prop :=
  archiveDivergence T.T = 0

theorem source_must_be_conserved (n : Nat) (T : ArchiveStressSource n) :
    SourcedArchiveEquation n T → ArchiveStressSourceConserved T := by
  intro h
  unfold ArchiveStressSourceConserved
  rw [← h]
  exact curvature_gradient_conserved n

end D0
