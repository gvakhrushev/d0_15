import D0.Geometry.OriginalBookWalshOrthogonality
import D0.Geometry.OriginalBookJuliaRowCompleteness
import Mathlib.Tactic

/-!
# Walsh Gram and Parseval for the source's exact 32 signs

The signs are those of the source rows, with the orthogonality already proved
from five-bit parity. This section establishes the scalar bilinear Parseval
identity and applies the 1/32 normalization to prove the left Gram sum of the
64 actual source rows equals identity. No 128-Kraus completeness or physical
admission is assumed here.
-/

open Matrix
open scoped BigOperators
open D0.Geometry.OriginalBookWalsh
open D0.Geometry.OriginalBookWalshOrthogonality
open D0.Geometry.OriginalBookJuliaRowCompleteness

namespace D0.Geometry.OriginalBookWalshParseval

/-- Exact sign matrix used before the source's division by 32. -/
noncomputable def signMatrix : Matrix (Fin 32) (Fin 32) ℂ :=
  fun label word => (walshSign label word : ℂ)

/-- The original finite Walsh signs are orthogonal as a complex matrix. -/
theorem signMatrix_gram : signMatrixᵀ * signMatrix = (32 : ℂ) • 1 := by
  ext j k
  have h := walsh_orthogonal j k
  have hc : (∑ label : Fin 32, (walshSign label j : ℂ) * (walshSign label k : ℂ)) =
      if j = k then 32 else 0 := by
    exact_mod_cast h
  simpa [Matrix.mul_apply, signMatrix, Matrix.one_apply] using hc

/-- Bilinear Parseval without conjugation, for arbitrary complex vectors. -/
theorem signMatrix_parseval (u v : Fin 32 → ℂ) :
    (signMatrix *ᵥ u) ⬝ᵥ (signMatrix *ᵥ v) = (32 : ℂ) * (u ⬝ᵥ v) := by
  rw [Matrix.dotProduct_mulVec, ← Matrix.mulVec_transpose, Matrix.mulVec_mulVec, signMatrix_gram]
  rw [Matrix.smul_mulVec, Matrix.one_mulVec, smul_dotProduct]
  rfl

/-- The source normalization is exactly one factor of 1/32 after Parseval. -/
theorem normalized_vector_parseval (u v : Fin 32 → ℂ) :
    (∑ label : Fin 32, ((1 / 32 : ℂ) * (signMatrix *ᵥ u) label) *
      ((1 / 32 : ℂ) * (signMatrix *ᵥ v) label)) =
      (1 / 32 : ℂ) * ∑ word : Fin 32, u word * v word := by
  have h := signMatrix_parseval u v
  unfold dotProduct at h
  calc
    _ = ((1 / 32 : ℂ) ^ 2) * ∑ label : Fin 32,
        (signMatrix *ᵥ u) label * (signMatrix *ᵥ v) label := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = ((1 / 32 : ℂ) ^ 2) * ((32 : ℂ) * ∑ word : Fin 32, u word * v word) := by rw [h]
    _ = _ := by ring_nf

/-- Entrywise form of the actual source's pair row. -/
lemma pairRow_entry (label : Fin 32) (endpoint : Fin 2) (a b : Fin 16) :
    walshPairRow label endpoint a b =
      (1 / 32 : ℂ) * (signMatrix *ᵥ fun word => wordEndpoint word endpoint a b) label := by
  simp only [walshPairRow, Matrix.smul_apply, Matrix.sum_apply]
  simp [signMatrix, Matrix.mulVec, dotProduct, zsmul_eq_mul]
lemma pairRow_star_entry (label : Fin 32) (endpoint : Fin 2) (a b : Fin 16) :
    star (walshPairRow label endpoint a b) =
      (1 / 32 : ℂ) * (signMatrix *ᵥ fun word => star (wordEndpoint word endpoint a b)) label := by
  rw [pairRow_entry]
  simp [signMatrix, Matrix.mulVec, dotProduct]

/-- Each actual scalar entry inherits normalized Parseval, including conjugation. -/
theorem pairRow_entry_parseval (endpoint : Fin 2) (a b k : Fin 16) :
    (∑ label : Fin 32, walshPairRow label endpoint a k *
      star (walshPairRow label endpoint b k)) =
      (1 / 32 : ℂ) * ∑ word : Fin 32,
        wordEndpoint word endpoint a k * star (wordEndpoint word endpoint b k) := by
  simp_rw [pairRow_star_entry]
  simp_rw [pairRow_entry]
  exact normalized_vector_parseval (fun word => wordEndpoint word endpoint a k)
    (fun word => star (wordEndpoint word endpoint b k))
/-- Parseval as an identity of 16×16 operator matrices, for each endpoint. -/
theorem pairRow_gram (endpoint : Fin 2) :
    (∑ label : Fin 32, walshPairRow label endpoint * (walshPairRow label endpoint)ᴴ) =
      (1 / 32 : ℂ) • ∑ word : Fin 32, wordEndpoint word endpoint * (wordEndpoint word endpoint)ᴴ := by
  ext a b
  simp only [Matrix.sum_apply, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Matrix.smul_apply, smul_eq_mul]
  rw [Finset.sum_comm]
  simp_rw [pairRow_entry_parseval]
  rw [← Finset.mul_sum, Finset.sum_comm]
/-- The source flattening is the standard finite-product enumeration. -/
lemma rowIndex_finProd (label : Fin 32) (endpoint : Fin 2) :
    rowIndex label endpoint = finProdFinEquiv (label, endpoint) := by
  fin_cases label <;> fin_cases endpoint <;> rfl

/-- The 64 actual source Walsh rows have the required left Gram sum. -/
theorem sourceWalshRow_complete :
    (∑ row : Fin 64, sourceWalshRow row * (sourceWalshRow row)ᴴ) = 1 := by
  rw [← (finProdFinEquiv : Fin 32 × Fin 2 ≃ Fin 64).sum_comp]
  rw [Fintype.sum_prod_type]
  simp_rw [← rowIndex_finProd, sourceWalshRow_order, Fin.sum_univ_two,
    Finset.sum_add_distrib, pairRow_gram, ← smul_add, ← Finset.sum_add_distrib]
  have h (word : Fin 32) :
      wordEndpoint word 0 * (wordEndpoint word 0)ᴴ +
        wordEndpoint word 1 * (wordEndpoint word 1)ᴴ = 1 := by
    simpa [wordEndpoint] using sourceWord_complete word
  simp_rw [h]
  simp [← Nat.cast_smul_eq_nsmul ℂ, smul_smul]
end D0.Geometry.OriginalBookWalshParseval
