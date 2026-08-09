import Mathlib.Tactic
import D0.Cosmology.PhasonFlipEntropy
import D0.VNext2.Rank3CubicSymmetricFunctions

/-!
# Exact spectral separation of the S_DE window and the rank-3 scene quotient

The finite S_DE transfer owner has normalized characteristic polynomial

`P(X) = 160 X² - 480 X + 359`,

while the rank-3 complete-tripartite scene quotient has characteristic polynomial

`Q(X) = X³ - 359 X - 2574`.

This module proves that these two *owned* polynomials are coprime over `ℚ`, by an
explicit integral Bézout certificate.  It then proves the exact linear-algebraic
consequence: operators annihilated by `P` and `Q` admit no nonzero intertwiner.

Scope is deliberately algebraic.  Applying the final theorem to particular
physical carriers still requires actual operator-annihilation and intertwining
hypotheses; coefficient coincidence alone supplies neither.
-/

namespace D0.Synthesis.SDECubicSpectralDisjointness

open D0.Cosmology

/-! ## Scalar certificate -/

/-- The S_DE quadratic, with coefficients owned by `PhasonFlipEntropy`. -/
def sdeQuadratic (x : ℚ) : ℚ :=
  160 * x ^ 2 - 480 * x + 359

/-- The rank-3 scene cubic, with coefficients owned by
`Rank3CubicSymmetricFunctions`. -/
def sceneCubic (x : ℚ) : ℚ :=
  x ^ 3 - 359 * x - 2574

/-- Quadratic coefficient in the integral Bézout certificate. -/
def bezoutA (x : ℚ) : ℚ :=
  -9017440 * x ^ 2 + 66066720 * x + 3455694001

/-- Linear coefficient in the integral Bézout certificate. -/
def bezoutB (x : ℚ) : ℚ :=
  1442790400 * x - 14899046400

/-- The exact (nonzero) resultant of the S_DE quadratic and scene cubic. -/
def spectralResultant : ℚ :=
  39590739579959

/-- The local quadratic is exactly the normalized polynomial from the S_DE owner. -/
theorem sdeQuadratic_eq_owned (x : ℚ) :
    sdeQuadratic x = SDEPolynomial x := by
  rfl

/-- The scene-cubic coefficients are the frozen symmetric functions
`e₂ = 359`, `2e₃ = 2574`. -/
theorem sceneCubic_coefficients_owned :
    D0.VNext2.Rank3CubicSymmetricFunctions.n₁ *
          D0.VNext2.Rank3CubicSymmetricFunctions.n₂ +
        D0.VNext2.Rank3CubicSymmetricFunctions.n₁ *
          D0.VNext2.Rank3CubicSymmetricFunctions.n₃ +
        D0.VNext2.Rank3CubicSymmetricFunctions.n₂ *
          D0.VNext2.Rank3CubicSymmetricFunctions.n₃ = 359 ∧
      2 * (D0.VNext2.Rank3CubicSymmetricFunctions.n₁ *
        D0.VNext2.Rank3CubicSymmetricFunctions.n₂ *
        D0.VNext2.Rank3CubicSymmetricFunctions.n₃) = 2574 :=
  D0.VNext2.Rank3CubicSymmetricFunctions.cubic_coefficients

/-- **Integral Bézout/resultant certificate.**

`A(X)P(X) + B(X)Q(X) = 39,590,739,579,959`.

All coefficients are integers, so the identity is independently checkable by
ring normalization; no root approximation or imported CAS result is trusted.
-/
theorem scalar_bezout_certificate (x : ℚ) :
    bezoutA x * sdeQuadratic x + bezoutB x * sceneCubic x =
      spectralResultant := by
  simp only [bezoutA, bezoutB, sdeQuadratic, sceneCubic, spectralResultant]
  ring

/-- The resultant in the explicit certificate is nonzero. -/
theorem spectralResultant_ne_zero : spectralResultant ≠ 0 := by
  norm_num [spectralResultant]

/-- The owned quadratic and cubic have no common rational root. -/
theorem no_common_rational_root :
    ¬ ∃ x : ℚ, sdeQuadratic x = 0 ∧ sceneCubic x = 0 := by
  rintro ⟨x, hP, hQ⟩
  have h := scalar_bezout_certificate x
  rw [hP, hQ] at h
  exact spectralResultant_ne_zero (by simpa using h.symm)

/-! ## Operator certificate and intertwiner no-go -/

section Operators

variable {V W : Type*}
variable [AddCommGroup V] [Module ℚ V]
variable [AddCommGroup W] [Module ℚ W]

/-- Evaluation of the S_DE quadratic on a rational linear endomorphism. -/
def sdeOperator (T : Module.End ℚ V) : Module.End ℚ V :=
  160 * T ^ 2 - 480 * T + 359

/-- Evaluation of the rank-3 scene cubic on a rational linear endomorphism. -/
def sceneOperator (T : Module.End ℚ V) : Module.End ℚ V :=
  T ^ 3 - 359 * T - 2574

/-- Evaluation of the quadratic Bézout coefficient on an endomorphism. -/
def bezoutAOperator (T : Module.End ℚ V) : Module.End ℚ V :=
  -9017440 * T ^ 2 + 66066720 * T + 3455694001

/-- Evaluation of the linear Bézout coefficient on an endomorphism. -/
def bezoutBOperator (T : Module.End ℚ V) : Module.End ℚ V :=
  1442790400 * T - 14899046400

/-- The same integral certificate holds in every rational endomorphism ring. -/
theorem operator_bezout_certificate (T : Module.End ℚ V) :
    bezoutAOperator T * sdeOperator T +
        bezoutBOperator T * sceneOperator T =
      (39590739579959 : Module.End ℚ V) := by
  simp only [bezoutAOperator, bezoutBOperator, sdeOperator, sceneOperator]
  noncomm_ring
  norm_num

/-- No nonzero vector can lie simultaneously in the kernels of the two
polynomials of one operator. -/
theorem no_common_annihilated_vector
    (T : Module.End ℚ V) (v : V)
    (hP : sdeOperator T v = 0)
    (hQ : sceneOperator T v = 0) :
    v = 0 := by
  have hcert := congrArg (fun E : Module.End ℚ V => E v)
    (operator_bezout_certificate T)
  change
    (bezoutAOperator T * sdeOperator T +
      bezoutBOperator T * sceneOperator T) v =
        (39590739579959 : Module.End ℚ V) v at hcert
  rw [LinearMap.add_apply, Module.End.mul_apply, Module.End.mul_apply, hP, hQ] at hcert
  simp only [map_zero, add_zero, Module.End.ofNat_apply] at hcert
  have hR := hcert.symm
  rw [← Nat.cast_smul_eq_nsmul ℚ] at hR
  exact (smul_eq_zero.mp hR).resolve_left spectralResultant_ne_zero

/-- **No-nonzero-intertwiner theorem.**

If `T` is annihilated by the S_DE quadratic, `S` is annihilated by the scene
cubic, and `F` intertwines them (`F T = S F`), then `F = 0`.
-/
theorem no_nonzero_intertwiner
    (T : Module.End ℚ V) (S : Module.End ℚ W) (F : V →ₗ[ℚ] W)
    (hP : sdeOperator T = 0)
    (hQ : sceneOperator S = 0)
    (hIntertwines : F.comp T = S.comp F) :
    F = 0 := by
  ext v
  apply no_common_annihilated_vector S (F v)
  · have hTv : F (T v) = S (F v) := by
      exact LinearMap.congr_fun hIntertwines v
    have hT2v : F (T (T v)) = S (S (F v)) := by
      calc
        F (T (T v)) = S (F (T v)) :=
          LinearMap.congr_fun hIntertwines (T v)
        _ = S (S (F v)) := congrArg S hTv
    have hPv : sdeOperator T v = 0 := by
      rw [hP]
      rfl
    have hFPv := congrArg (fun z : V => F z) hPv
    simpa [sdeOperator, pow_two, Module.End.mul_apply, hTv, hT2v] using hFPv
  · rw [hQ]
    rfl

end Operators

/-! ## Concrete owned operators -/

/-- The actual `2 × 2` S_DE transfer matrix, viewed as a rational operator. -/
def ownedSDETransferOperator :
    Module.End ℚ (Fin 2 → ℚ) :=
  Matrix.toLinAlgEquiv' phasonFlipTransferMatrix

/-- The actual rank-3 zone-quotient adjacency matrix
`Bᵢⱼ = nⱼ` for `i ≠ j`. -/
def ownedSceneQuotientMatrix : Matrix (Fin 3) (Fin 3) ℚ :=
  !![0, 11, 13;
     9,  0, 13;
     9, 11,  0]

/-- The scene quotient as a rational operator. -/
def ownedSceneQuotientOperator :
    Module.End ℚ (Fin 3 → ℚ) :=
  Matrix.toLinAlgEquiv' ownedSceneQuotientMatrix

/-- Cayley-Hamilton, checked entrywise, for the concrete S_DE transfer:
`160 T² - 480 T + 359 I = 0`. -/
theorem owned_sde_transfer_annihilated :
    sdeOperator ownedSDETransferOperator = 0 := by
  ext v i
  fin_cases v <;> fin_cases i <;>
    norm_num [sdeOperator, ownedSDETransferOperator,
      Matrix.toLinAlgEquiv'_apply, Matrix.mulVec, dotProduct,
      phasonFlipTransferMatrix, pow_two, Module.End.mul_apply,
      Fin.sum_univ_succ]

/-- Cayley-Hamilton, checked entrywise, for the concrete rank-3 quotient:
`B³ - 359 B - 2574 I = 0`. -/
theorem owned_scene_quotient_annihilated :
    sceneOperator ownedSceneQuotientOperator = 0 := by
  ext v i
  fin_cases v <;> fin_cases i <;>
    norm_num [sceneOperator, ownedSceneQuotientOperator,
      Matrix.toLinAlgEquiv'_apply, Matrix.mulVec, dotProduct,
      ownedSceneQuotientMatrix, pow_succ, Module.End.mul_apply,
      Fin.sum_univ_succ]

/-- **Concrete spectral-disjointness capstone.** Every rational linear map from
the actual S_DE two-mode carrier to the actual rank-3 scene quotient that
intertwines their owned operators is zero. -/
theorem concrete_owned_intertwiner_is_zero
    (F : (Fin 2 → ℚ) →ₗ[ℚ] (Fin 3 → ℚ))
    (hIntertwines :
      F.comp ownedSDETransferOperator =
        ownedSceneQuotientOperator.comp F) :
    F = 0 :=
  no_nonzero_intertwiner
    ownedSDETransferOperator ownedSceneQuotientOperator F
    owned_sde_transfer_annihilated owned_scene_quotient_annihilated hIntertwines

end D0.Synthesis.SDECubicSpectralDisjointness
