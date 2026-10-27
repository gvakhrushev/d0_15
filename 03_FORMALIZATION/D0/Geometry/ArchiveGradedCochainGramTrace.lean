import D0.Geometry.ArchiveGradedCochainGram
import Mathlib.LinearAlgebra.Matrix.Trace

namespace D0.Geometry

open D0
open scoped BigOperators
noncomputable section

/-- The actual refinement operator on the standard site × Fock basis. -/
def archiveGradedPullbackMatrix (N : ℕ) :
    Matrix (ArchiveCochainBasis (N + 1)) (ArchiveCochainBasis N) ℝ :=
  fun fine coarse => archiveGradedCochainPullback N
    (fun p => if p = coarse then 1 else 0) fine

/-- Matrix multiplication is literally the graded cochain pullback. -/
theorem archive_graded_matrix_mulVec (N : ℕ) (ψ : ArchiveCochain N) :
    (archiveGradedPullbackMatrix N).mulVec ψ = archiveGradedCochainPullback N ψ := by
  classical
  funext p
  simp [archiveGradedPullbackMatrix, Matrix.mulVec, dotProduct,
    archiveGradedCochainPullback]

/-- The matrix Gram entry is the existing counting pairing of two actual
refined basis cochains. -/
theorem archive_graded_matrix_gram_entry (N : ℕ) (p q : ArchiveCochainBasis N) :
    ((archiveGradedPullbackMatrix N).transpose * archiveGradedPullbackMatrix N) p q =
      cochainPairing (N + 1)
        (archiveGradedCochainPullback N (fun k => if k = p then 1 else 0))
        (archiveGradedCochainPullback N (fun k => if k = q then 1 else 0)) := by
  classical
  simp only [Matrix.mul_apply, Matrix.transpose_apply, archiveGradedPullbackMatrix,
    cochainPairing]
  exact Fintype.sum_prod_type _

/-- The Gram matrix of the literal refinement map is diagonal with the
previously derived full counting weights. -/
theorem archive_graded_matrix_gram (N : ℕ) :
    (archiveGradedPullbackMatrix N).transpose * archiveGradedPullbackMatrix N =
      Matrix.diagonal (fun p : ArchiveCochainBasis N => archiveGradedGramWeight N p.1 p.2) := by
  classical
  ext p q
  rw [archive_graded_matrix_gram_entry, archive_graded_cochain_gram]
  simp only [Matrix.diagonal_apply]
  calc
    _ = ∑ t : ArchiveCochainBasis N, archiveGradedGramWeight N t.1 t.2 *
        ((if t = p then 1 else 0) * (if t = q then 1 else 0)) := by
          exact (Fintype.sum_prod_type
            (fun t : ArchiveCochainBasis N => archiveGradedGramWeight N t.1 t.2 *
              ((if t = p then 1 else 0) * (if t = q then 1 else 0)))).symm
    _ = _ := by
      by_cases hpq : p = q
      · subst q
        simp
      · simp [hpq, eq_comm]

/-- The trace is the sum of the actual diagonal Gram weights. -/
theorem archive_graded_matrix_trace_eq_weight_sum (N : ℕ) :
    Matrix.trace ((archiveGradedPullbackMatrix N).transpose * archiveGradedPullbackMatrix N) =
      ∑ x : ArchiveRolePhaseGroup N, ∑ S : ArchiveFockState,
        archiveGradedGramWeight N x S := by
  rw [archive_graded_matrix_gram, Matrix.trace_diagonal, Fintype.sum_prod_type]

/-- Degree scaling factors into one factor for every occupied role. -/
theorem archive_graded_scale_as_role_product (N : ℕ) (S : ArchiveFockState) :
    archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) =
      ∏ r : Role, (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) := by
  classical
  rw [mul_comm 2, pow_mul]
  simp [fockDegree, Finset.prod_ite, Finset.prod_const]
  rw [← pow_mul, ← pow_mul, Nat.mul_comm]

/-- The contribution of one role after summing its coarse sites. -/
theorem archive_graded_coordinate_weight_sum (N : ℕ) (b : Bool) :
    (∑ a : ZMod (archiveFibers N),
      (if b then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
        archiveGramCoordinateWeight b a) =
      if b then (archiveFibers N : ℝ) * archiveCochainScaleRatio (N + 1) ^ 2
      else (archiveFibers N : ℝ) + 1 := by
  classical
  cases b
  · simp only [Bool.false_eq_true, ↓reduceIte, one_mul, archiveGramCoordinateWeight]
    have h : ∀ a : ZMod (archiveFibers N),
        (if a = 0 then (2 : ℝ) else 1) = 1 + (if a = 0 then 1 else 0) := by
      intro a
      split_ifs <;> norm_num
    simp_rw [h, Finset.sum_add_distrib]
    simp [ZMod.card]
  · simp [archiveGramCoordinateWeight, ZMod.card]

/-- The literal diagonal weight factors over the four roles. -/
theorem archive_graded_weight_role_product (N : ℕ) (x : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) :
    archiveGradedGramWeight N x S =
      ∏ r : Role, (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
        archiveGramCoordinateWeight (S r) (x r) := by
  rw [archiveGradedGramWeight, archive_graded_scale_as_role_product,
    ← Finset.prod_mul_distrib]

/-- The complete site × Fock counting trace of the degree-scaled weight. -/
theorem archive_graded_weight_trace (N : ℕ) :
    (∑ x : ArchiveRolePhaseGroup N, ∑ S : ArchiveFockState,
      archiveGradedGramWeight N x S) =
      (((archiveFibers N : ℝ) + 1) + (archiveFibers N : ℝ) *
        archiveCochainScaleRatio (N + 1) ^ 2) ^ 4 := by
  classical
  calc
    _ = ∑ S : ArchiveFockState, ∑ x : ArchiveRolePhaseGroup N,
        ∏ r : Role, (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
          archiveGramCoordinateWeight (S r) (x r) := by
            rw [Finset.sum_comm]
            apply Finset.sum_congr rfl
            intro S hS
            apply Finset.sum_congr rfl
            intro x hx
            exact archive_graded_weight_role_product N x S
    _ = ∑ S : ArchiveFockState, ∏ r : Role,
        ∑ a : ZMod (archiveFibers N),
          (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
            archiveGramCoordinateWeight (S r) a := by
              apply Finset.sum_congr rfl
              intro S hS
              simpa only [Fintype.piFinset_univ] using
                (Finset.sum_prod_piFinset (s := Finset.univ)
                  (g := fun r a => (if S r then archiveCochainScaleRatio (N + 1) ^ 2 else 1) *
                    archiveGramCoordinateWeight (S r) a))
    _ = ∑ S : ArchiveFockState, ∏ r : Role,
        (if S r then (archiveFibers N : ℝ) * archiveCochainScaleRatio (N + 1) ^ 2
          else (archiveFibers N : ℝ) + 1) := by
            apply Finset.sum_congr rfl
            intro S hS
            apply Finset.prod_congr rfl
            intro r hr
            exact archive_graded_coordinate_weight_sum N (S r)
    _ = ∏ r : Role, ∑ b : Bool,
        (if b then (archiveFibers N : ℝ) * archiveCochainScaleRatio (N + 1) ^ 2
          else (archiveFibers N : ℝ) + 1) := by
            simpa only [Fintype.piFinset_univ] using
              (Finset.sum_prod_piFinset (s := (Finset.univ : Finset Bool))
                (g := fun (_ : Role) b =>
                  (if b then (archiveFibers N : ℝ) * archiveCochainScaleRatio (N + 1) ^ 2
                    else (archiveFibers N : ℝ) + 1)))
    _ = _ := by simp [Finset.prod_const, add_comm]

/-- Closed trace of the Gram matrix of the actual refinement operator. -/
theorem archive_graded_matrix_trace (N : ℕ) :
    Matrix.trace ((archiveGradedPullbackMatrix N).transpose * archiveGradedPullbackMatrix N) =
      (((archiveFibers N : ℝ) + 1) + (archiveFibers N : ℝ) *
        archiveCochainScaleRatio (N + 1) ^ 2) ^ 4 := by
  rw [archive_graded_matrix_trace_eq_weight_sum, archive_graded_weight_trace]

/-- The first archive level follows from the general trace formula. -/
theorem archive_graded_matrix_trace_level_zero :
    Matrix.trace ((archiveGradedPullbackMatrix 0).transpose * archiveGradedPullbackMatrix 0) =
      (50625 : ℝ) / 16 := by
  rw [archive_graded_matrix_trace, archive_role_refinement_scale]
  norm_num [archiveFibers]

end
end D0.Geometry
