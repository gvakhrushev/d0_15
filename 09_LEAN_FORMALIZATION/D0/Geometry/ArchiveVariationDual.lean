import D0.Geometry.ArchiveVariationSpace

open scoped BigOperators

namespace D0

lemma symmetric_matrix_sum_comm {I : Type} [Fintype I]
  (A : Matrix I I ℝ) (D : Matrix I I ℝ) (hD : MatrixSymmetric D) :
  (∑ i : I, ∑ j : I, A j i * D i j) = ∑ i : I, ∑ j : I, A i j * D i j := by
  rw [Finset.sum_comm]
  have h_eq : ∀ x x_1 : I, A x x_1 * D x_1 x = A x x_1 * D x x_1 := by
    intro x x_1
    rw [hD x_1 x]
  simp_rw [h_eq]

theorem pairing_depends_only_on_symmetric_part {n : Nat}
  (A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (δ : AdmissibleLaplacianVariation n) :
  variationPairing A δ =
  variationPairing (symPart A) δ := by
  unfold variationPairing symPart matrixInnerProduct
  dsimp only
  have h_split : (∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, ((A i j + A j i) / 2) * δ.dL i j) =
      (1 / 2 : ℝ) * (∑ i, ∑ j, A i j * δ.dL i j) + (1 / 2 : ℝ) * (∑ i, ∑ j, A j i * δ.dL i j) := by
    rw [Finset.mul_sum, Finset.mul_sum]
    simp_rw [Finset.mul_sum]
    rw [← Finset.sum_add_distrib]
    simp_rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [h_split]
  rw [symmetric_matrix_sum_comm A δ.dL δ.symmetric]
  ring

theorem skew_part_annihilates_admissible_variations {n : Nat}
  (A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (hSkew : SkewSymmetric A)
  (δ : AdmissibleLaplacianVariation n) :
  variationPairing A δ = 0 := by
  have hSymZero : symPart A = 0 := by
    ext i j
    unfold symPart
    rw [hSkew j i]
    dsimp
    ring
  rw [pairing_depends_only_on_symmetric_part A δ, hSymZero]
  unfold variationPairing matrixInnerProduct
  dsimp
  simp

end D0
