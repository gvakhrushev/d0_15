import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveVariationSpace
import D0.Geometry.ArchiveVariationDual
import D0.Geometry.ArchiveBianchiIdentity


namespace D0

noncomputable def conservedStressProjection {n : Nat}
  (G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
  Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ :=
  let S := symPart G
  let v := fun i => ∑ k : archivePhaseIndex n, S i k
  let N : ℝ := (archiveFibers n : ℝ)
  fun i j => S i j - (1 / N) * (v i + v j)

theorem constrained_projection_symmetric {n : Nat}
  (G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
  MatrixSymmetric (conservedStressProjection G) := by
  intro i j
  unfold conservedStressProjection symPart
  dsimp
  ring

theorem constrained_projection_conserved {n : Nat}
  (G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (hG : archiveDivergence G = 0) :
  archiveDivergence (conservedStressProjection G) = 0 := by
  funext i
  unfold archiveDivergence conservedStressProjection
  dsimp
  have h_fibers : 0 < archiveFibers n := by
    unfold archiveFibers
    omega
  have h_fibers_real : (archiveFibers n : ℝ) ≠ 0 := by
    exact Nat.cast_ne_zero.mpr (ne_of_gt h_fibers)
  let S := symPart G
  let v := fun i => ∑ k, S i k
  let N := (archiveFibers n : ℝ)
  have h_sum_split : (∑ j : archivePhaseIndex n, (S i j - (1 / N) * (v i + v j))) =
    (∑ j, S i j) - (1 / N) * (∑ j, (v i + v j)) := by
    rw [Finset.sum_sub_distrib, Finset.mul_sum]
  rw [h_sum_split]
  have h_v_sum : (∑ j : archivePhaseIndex n, (v i + v j)) = N * v i + (∑ j, v j) := by
    rw [Finset.sum_add_distrib]
    have h_const : (∑ j : archivePhaseIndex n, v i) = N * v i := by
      simp [Finset.sum_const, N]
    rw [h_const]
  rw [h_v_sum]
  have h_v_total : (∑ j : archivePhaseIndex n, v j) = 0 := by
    have h_S_expr : ∀ j, v j = (1 / 2) * (∑ k, G j k) + (1 / 2) * (∑ k, G k j) := by
      intro j
      dsimp [v, S, symPart]
      simp_rw [Finset.mul_sum]
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro k _
      ring
    simp_rw [h_S_expr]
    rw [Finset.sum_add_distrib]
    rw [← Finset.mul_sum, ← Finset.mul_sum]
    have h_row : (∑ j, ∑ k, G j k) = 0 := by
      have h_row_zero : ∀ j, (∑ k, G j k) = 0 := by
        intro j
        exact congr_fun hG j
      simp [h_row_zero]
    rw [h_row, mul_zero]
    rw [Finset.sum_comm]
    have h_col : (∑ k, ∑ j, G k j) = 0 := by
      have h_col_zero : ∀ k, (∑ j, G k j) = 0 := by
        intro k
        exact congr_fun hG k
      simp [h_col_zero]
    rw [h_col, mul_zero, add_zero]
  rw [h_v_total, add_zero]
  have h_S_vi : (∑ j, S i j) = v i := rfl
  rw [h_S_vi]
  have h_cancel : (1 / N) * N = 1 := by
    exact one_div_mul_cancel h_fibers_real
  rw [← mul_assoc, h_cancel, one_mul, sub_self]

theorem constrained_projection_pairing_equivalent {n : Nat}
  (G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (δ : AdmissibleLaplacianVariation n) :
  variationPairing (conservedStressProjection G) δ = variationPairing G δ := by
  unfold variationPairing conservedStressProjection matrixInnerProduct
  dsimp
  let S := symPart G
  let v := fun i => ∑ k, S i k
  let N := (archiveFibers n : ℝ)
  have h_split : (∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, (S i j - (1 / N) * (v i + v j)) * δ.dL i j) =
    (∑ i, ∑ j, S i j * δ.dL i j) - (1 / N) * (∑ i, ∑ j, (v i + v j) * δ.dL i j) := by
    have h_term : ∀ i j, (S i j - (1 / N) * (v i + v j)) * δ.dL i j = S i j * δ.dL i j - 1 / N * ((v i + v j) * δ.dL i j) := by
      intro i j
      ring
    simp_rw [h_term]
    simp_rw [Finset.sum_sub_distrib, Finset.mul_sum]
  rw [h_split]
  have h_zero : (∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, (v i + v j) * δ.dL i j) = 0 := by
    have h_term : ∀ i j, (v i + v j) * δ.dL i j = v i * δ.dL i j + v j * δ.dL i j := by
      intro i j
      ring
    simp_rw [h_term, Finset.sum_add_distrib]
    have h_sum1 : (∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, v i * δ.dL i j) = 0 := by
      simp_rw [← Finset.mul_sum]
      have h_row_sum_zero : ∀ i, (∑ j, δ.dL i j) = 0 := fun i => δ.row_sum_zero i
      simp [h_row_sum_zero]
    have h_sum2 : (∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, v j * δ.dL i j) = 0 := by
      rw [Finset.sum_comm]
      simp_rw [← Finset.mul_sum]
      have h_col_sum_zero : ∀ j, (∑ i, δ.dL i j) = 0 := by
        intro j
        have h_symm : (∑ i, δ.dL i j) = (∑ i, δ.dL j i) := by
          apply Finset.sum_congr rfl
          intro i _
          rw [δ.symmetric i j]
        rw [h_symm]
        exact δ.row_sum_zero j
      simp [h_col_sum_zero]
    linarith
  rw [h_zero, mul_zero, sub_zero]
  have h_eq : (∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, S i j * δ.dL i j) = variationPairing G δ := by
    exact (pairing_depends_only_on_symmetric_part G δ).symm
  exact h_eq

theorem constrained_stress_projection_symmetric_conserved_equivalent
  (n : Nat)
  (G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (hG : archiveDivergence G = 0) :
  let T := conservedStressProjection G
  MatrixSymmetric T ∧
  archiveDivergence T = 0 ∧
  (∀ δ : AdmissibleLaplacianVariation n,
    variationPairing T δ = variationPairing G δ) := by
  intro T
  refine ⟨constrained_projection_symmetric G, constrained_projection_conserved G hG, ?_⟩
  intro δ
  exact constrained_projection_pairing_equivalent G δ

theorem constrained_projection_applies_to_archive_gradient (n : Nat) :
  let T := conservedStressProjection (archiveCurvatureGradient n)
  MatrixSymmetric T ∧
  archiveDivergence T = 0 ∧
  (∀ δ : AdmissibleLaplacianVariation n,
    variationPairing T δ = variationPairing (archiveCurvatureGradient n) δ) := by
  intro T
  exact constrained_stress_projection_symmetric_conserved_equivalent n (archiveCurvatureGradient n) (curvature_gradient_conserved n)

end D0
