import D0.Algebra.OriginalBookLocalCreators
import D0.Algebra.OriginalBookRadicalSourceConstants
import D0.Geometry.OriginalBookAnalyticBoost
import Mathlib.Tactic

/-!
# Local source CAR boost

The exact source generator G=c_A c_D†+c_D c_A† and boost
I+G²/40+9G/40 are from modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 94–100, and uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
lines 70–80, at eebcb5e467742df3e9cf7fa9702042d7294aa742. The previously
proved analytic correspondence fixes theta=log(5/4). This module builds the
actual source boost in the local coefficient ring, without claiming that
Julia roots, Walsh rows, effects or any rank certificate have been transferred.
-/
open D0
open Matrix
open scoped Matrix.Norms.Operator
open NormedSpace
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookRadicalSourceConstants
open D0.Algebra.OriginalBookLocalCreators
open D0.Geometry.OriginalBookBoost
open D0.Geometry.CubicExponential

namespace D0.Algebra.OriginalBookLocalBoost

/-- Since 40 divides 8810³, its inverse exists in the source local ring. -/
noncomputable def localInv40 : LocalSource := 17094946025 * localInvD ^ 3

lemma complexInv40 : localSourceToComplex localInv40 = (1 / 40 : ℂ) := by
  simp [localInv40, complexInvD, map_ofNat]
  norm_num

lemma modInv40 : redPlus localInv40 = (1 / 40 : ZMod 1009) := by
  simp only [localInv40, map_mul, map_pow, map_ofNat, modInvD]
  decide

/-- The actual source CAR generator over the faithful local ring. -/
def localGenerator : LocalOperator :=
  localCreator A * (localCreator D)ᴴ + localCreator D * (localCreator A)ᴴ

/-- The original fixed rational boost, retaining G² and the correct order. -/
noncomputable def localBoost : LocalOperator :=
  1 + localInv40 • (localGenerator * localGenerator) + (9 * localInv40) • localGenerator

/-- The local generator embeds to the previously proved exact source generator. -/
theorem localGenerator_complex :
    localGenerator.map localSourceToComplex = sourceComplexGenerator := by
  rw [sourceComplexGenerator_eq_creators]
  have hA (i j : Fin 16) : localSourceToComplex (localCreator A i j) = sourceCreatorComplex A i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localCreator_complex A)
  have hD (i j : Fin 16) : localSourceToComplex (localCreator D i j) = sourceCreatorComplex D i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localCreator_complex D)
  ext bra ket
  simp [localGenerator, Matrix.mul_apply, localSourceToComplex_star, hA, hD]

/-- Its two modular source generators are the original transcribed integer creators. -/
theorem localGenerator_mod :
    localGenerator.map redPlus =
      (localCreator A).map redPlus * ((localCreator D).map redMinus).transpose +
        (localCreator D).map redPlus * ((localCreator A).map redMinus).transpose := by
  ext bra ket
  simp [localGenerator, Matrix.mul_apply, redMinus, starRingEnd_apply]

/-- The local exact boost embeds to the actual analytic source exponential. -/
theorem localBoost_complex :
    localBoost.map localSourceToComplex = exp (sourceTheta • sourceComplexGenerator) := by
  rw [original_complex_boost_exponential]
  have hG (i j : Fin 16) : localSourceToComplex (localGenerator i j) = sourceComplexGenerator i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) localGenerator_complex
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localBoost, sourceRationalBoost, sourceComplexGenerator, Matrix.mul_apply,
      complexInv40, hG, h, map_ofNat] <;> ring_nf <;> simp

/-- The prime-field image retains the original rational boost formula. -/
theorem localBoost_mod :
    localBoost.map redPlus = 1 + (1 / 40 : ZMod 1009) •
      (localGenerator.map redPlus * localGenerator.map redPlus) +
      (9 / 40 : ZMod 1009) • localGenerator.map redPlus := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localBoost, Matrix.mul_apply, modInv40, h, map_ofNat] <;> ring_nf <;> simp

/-- The local rational coefficient is real under the faithful source embedding. -/
theorem localInv40_star : star localInv40 = localInv40 := by
  apply localSourceToComplex_injective
  rw [localSourceToComplex_star, complexInv40]
  simp

lemma modInv40_minus : redMinus localInv40 = (1 / 40 : ZMod 1009) := by
  change redPlus (star localInv40) = _
  rw [localInv40_star, modInv40]

/-- The conjugate modular evaluation also applies source dagger before evaluation. -/
theorem localDagger_mod_minus (M : LocalOperator) :
    Mᴴ.map redMinus = (M.map redPlus).transpose := by
  ext bra ket
  simp [Matrix.conjTranspose_apply, redMinus, starRingEnd_apply]

/-- The same explicit generator formula under the conjugate evaluation. -/
theorem localGenerator_mod_minus :
    localGenerator.map redMinus =
      (localCreator A).map redMinus * ((localCreator D).map redPlus).transpose +
        (localCreator D).map redMinus * ((localCreator A).map redPlus).transpose := by
  ext bra ket
  simp [localGenerator, Matrix.mul_apply, redMinus, starRingEnd_apply]

/-- Both evaluations agree here because the source creators are integer-real. -/
theorem localGenerator_mod_conjugate : localGenerator.map redMinus = localGenerator.map redPlus := by
  rw [localGenerator_mod_minus, localGenerator_mod]
  simp [localCreator_mod, localCreator_mod_conjugate]

/-- The conjugate evaluation preserves the same rational source boost formula. -/
theorem localBoost_mod_minus :
    localBoost.map redMinus = 1 + (1 / 40 : ZMod 1009) •
      (localGenerator.map redMinus * localGenerator.map redMinus) +
      (9 / 40 : ZMod 1009) • localGenerator.map redMinus := by
  ext bra ket
  by_cases h : bra = ket <;>
    simp [localBoost, Matrix.mul_apply, modInv40_minus, h, map_ofNat] <;> ring_nf <;> simp

/-- Source U is real here, so the two modular values coincide. -/
theorem localBoost_mod_conjugate : localBoost.map redMinus = localBoost.map redPlus := by
  rw [localBoost_mod_minus, localBoost_mod, localGenerator_mod_conjugate]
end D0.Algebra.OriginalBookLocalBoost
