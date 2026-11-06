import D0.Geometry.OriginalBookWalshParseval
import D0.Geometry.OriginalBookGoldenKraus
import Mathlib.Tactic

/-!
# Completeness bridge for the source Golden Kraus construction

The source v_j = n_j† a use the exact 64 Walsh rows and anchor from pinned
uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed, lines 94–99,
and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a, lines 174–182,
at commit eebcb5e467742df3e9cf7fa9702042d7294aa742. The row Gram identity
is derived from the actual source Julia roots and Walsh signs, not assumed.
The resulting theorem is the exact completeness sum for all 128 actual source
Kraus matrices. No physical admission or span/rank result follows.
-/
open Matrix
open scoped BigOperators
open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.OriginalBookWalsh
open D0.Geometry.OriginalBookWalshParseval
open D0.Geometry.OriginalBookGoldenKraus

namespace D0.Geometry.OriginalBookGoldenCompleteness

/-- The v-family Gram reduces to the source anchor Gram, in source order. -/
theorem sourceV_gram :
    (∑ row : Fin 64, (sourceV row)ᴴ * sourceV row) = sourceAnchorᴴ * sourceAnchor := by
  calc
    _ = sourceAnchorᴴ * (∑ row : Fin 64, sourceWalshRow row * (sourceWalshRow row)ᴴ) * sourceAnchor := by
      simp [sourceV, Matrix.conjTranspose_mul, Matrix.mul_assoc, Finset.mul_sum, Finset.sum_mul]
    _ = _ := by rw [sourceWalshRow_complete]; simp

lemma sourceV_zero_hermitian : (sourceV 0)ᴴ = sourceV 0 := by
  simp [sourceV, sourceAnchor, Matrix.conjTranspose_mul]

/-- The actual two Golden coefficients combine to exactly 4 p². -/
theorem golden_weights :
    (2 * goldenP ^ 2) * (2 * goldenP ^ 2) +
      (2 * goldenP * Real.sqrt goldenP) * (2 * goldenP * Real.sqrt goldenP) = 4 * goldenP ^ 2 := by
  calc
    _ = 4 * goldenP ^ 2 * (goldenP ^ 2 + (Real.sqrt goldenP) ^ 2) := by ring
    _ = 4 * goldenP ^ 2 := by rw [goldenRoot_sq, goldenP_equation]; ring

/-- One row of the source sum away from the anchor. -/
lemma nonanchor_pair_gram (row : Fin 64) (h : row ≠ 0) :
    (sourceGoldenPair row 0)ᴴ * sourceGoldenPair row 0 +
      (sourceGoldenPair row 1)ᴴ * sourceGoldenPair row 1 =
        (4 * goldenP ^ 2) • ((sourceV row)ᴴ * sourceV row) := by
  simp [sourceGoldenPair, h, Matrix.conjTranspose_smul, smul_smul, ← add_smul, golden_weights]

/-- The row containing the source anchor retains its identity and cross terms. -/
lemma anchor_pair_gram :
    (sourceGoldenPair 0 0)ᴴ * sourceGoldenPair 0 0 +
      (sourceGoldenPair 0 1)ᴴ * sourceGoldenPair 0 1 =
        1 - (2 * goldenP ^ 2) • ((sourceV 0)ᴴ + sourceV 0) +
          (4 * goldenP ^ 2) • ((sourceV 0)ᴴ * sourceV 0) := by
  rw [← golden_weights]
  simp [sourceGoldenPair, Matrix.conjTranspose_smul, sub_mul, mul_sub, smul_smul]
  module

lemma pair_gram (row : Fin 64) :
    (sourceGoldenPair row 0)ᴴ * sourceGoldenPair row 0 +
      (sourceGoldenPair row 1)ᴴ * sourceGoldenPair row 1 =
        (if row = 0 then 1 else 0) -
          (2 * goldenP ^ 2) • (if row = 0 then (sourceV 0)ᴴ + sourceV 0 else 0) +
          (4 * goldenP ^ 2) • ((sourceV row)ᴴ * sourceV row) := by
  by_cases h : row = 0
  · subst row
    simpa using anchor_pair_gram
  · simpa [h] using nonanchor_pair_gram row h

/-- Sum of the two ordered source ports over all 64 source Walsh rows. -/
theorem golden_pair_gram_sum :
    (∑ row : Fin 64, ((sourceGoldenPair row 0)ᴴ * sourceGoldenPair row 0 +
      (sourceGoldenPair row 1)ᴴ * sourceGoldenPair row 1)) = 1 := by
  simp_rw [pair_gram]
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.smul_sum, ← Finset.smul_sum]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true, sourceV_gram]
  have hv : sourceAnchorᴴ * sourceAnchor = sourceV 0 := by rfl
  rw [hv, sourceV_zero_hermitian, ← two_smul ℝ (sourceV 0), ← smul_smul]
  module

lemma krausIndex_finProd (row : Fin 64) (port : Fin 2) :
    krausIndex row port = finProdFinEquiv (row, port) := by
  fin_cases row <;> fin_cases port <;> rfl

/-- Completeness of the actual 128 ordered source Kraus matrices. -/
theorem sourceKraus_complete :
    (∑ slot : Fin 128, (sourceKraus slot)ᴴ * sourceKraus slot) = 1 := by
  rw [← (finProdFinEquiv : Fin 64 × Fin 2 ≃ Fin 128).sum_comp]
  rw [Fintype.sum_prod_type]
  simp_rw [← krausIndex_finProd, sourceKraus_order, Fin.sum_univ_two]
  exact golden_pair_gram_sum
end D0.Geometry.OriginalBookGoldenCompleteness
