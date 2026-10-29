import D0.Geometry.ArchiveGradedCochainGramTrace

namespace D0.Geometry

open D0
open scoped BigOperators
noncomputable section

/-- Restrict the columns of the actual pullback to one coarse Fock sector;
all fine site × Fock rows remain present. -/
def archiveGradedSectorMatrix (N : ℕ) (S : ArchiveFockState) :
    Matrix (ArchiveCochainBasis (N + 1)) (ArchiveRolePhaseGroup N) ℝ :=
  fun i x => archiveGradedPullbackMatrix N i (x, S)

/-- The sector Gram matrix is the corresponding diagonal block of the
full literal pullback Gram matrix. -/
theorem archive_graded_sector_matrix_gram (N : ℕ) (S : ArchiveFockState) :
    (archiveGradedSectorMatrix N S).transpose * archiveGradedSectorMatrix N S =
      Matrix.diagonal (fun x : ArchiveRolePhaseGroup N => archiveGradedGramWeight N x S) := by
  classical
  ext x y
  have h := congrFun (congrFun (archive_graded_matrix_gram N) (x, S)) (y, S)
  simpa [archiveGradedSectorMatrix, Matrix.mul_apply, Matrix.transpose_apply,
    Matrix.diagonal_apply] using h

/-- Every fixed sector counts all coarse sites, including its occupied
directions. -/
theorem archive_graded_sector_weight_trace_product (N : ℕ) (S : ArchiveFockState) :
    (∑ x : ArchiveRolePhaseGroup N, archiveGradedGramWeight N x S) =
      ∏ r : Role,
        (if S r then (archiveFibers N : ℝ) * archiveCochainScaleRatio (N + 1) ^ 2
          else (archiveFibers N : ℝ) + 1) := by
  classical
  calc
    _ = ∑ x : ArchiveRolePhaseGroup N,
      ∏ r : Role, (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
        archiveGramCoordinateWeight (S r) (x r) := by
          apply Finset.sum_congr rfl
          intro x hx
          exact archive_graded_weight_role_product N x S
    _ = ∏ r : Role, ∑ a : ZMod (archiveFibers N),
      (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
        archiveGramCoordinateWeight (S r) a := by
          simpa only [Fintype.piFinset_univ] using
            (Finset.sum_prod_piFinset (s := Finset.univ)
              (g := fun r a => (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
                archiveGramCoordinateWeight (S r) a))
    _ = _ := by
      apply Finset.prod_congr rfl
      intro r hr
      exact archive_graded_coordinate_weight_sum N (S r)

/-- The number of unoccupied roles is four minus the literal Fock degree. -/
theorem archive_unoccupied_role_count (S : ArchiveFockState) :
    (Finset.univ.filter (fun r : Role => ¬ S r = true)).card = 4 - fockDegree S := by
  classical
  have h := Finset.card_filter_add_card_filter_not
    (s := (Finset.univ : Finset Role)) (fun r => S r = true)
  simp only [Finset.card_univ, card_role] at h
  unfold fockDegree
  omega

/-- Exact scaled counting trace for every fixed Fock occupation state. -/
theorem archive_graded_sector_weight_trace (N : ℕ) (S : ArchiveFockState) :
    (∑ x : ArchiveRolePhaseGroup N, archiveGradedGramWeight N x S) =
      archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
        (archiveFibers N : ℝ) ^ fockDegree S *
          ((archiveFibers N : ℝ) + 1) ^ (4 - fockDegree S) := by
  classical
  rw [archive_graded_sector_weight_trace_product]
  rw [Finset.prod_ite]
  simp only [Finset.prod_const, archive_unoccupied_role_count]
  change ((archiveFibers N : ℝ) * archiveCochainScaleRatio (N + 1) ^ 2) ^ fockDegree S *
      ((archiveFibers N : ℝ) + 1) ^ (4 - fockDegree S) = _
  rw [mul_pow, ← pow_mul]
  ring

/-- Trace of the Gram matrix of the literal pullback restricted to a
single coarse Fock sector. -/
theorem archive_graded_sector_matrix_trace (N : ℕ) (S : ArchiveFockState) :
    Matrix.trace ((archiveGradedSectorMatrix N S).transpose * archiveGradedSectorMatrix N S) =
      archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
        (archiveFibers N : ℝ) ^ fockDegree S *
          ((archiveFibers N : ℝ) + 1) ^ (4 - fockDegree S) := by
  rw [archive_graded_sector_matrix_gram, Matrix.trace_diagonal,
    archive_graded_sector_weight_trace]

end
end D0.Geometry
