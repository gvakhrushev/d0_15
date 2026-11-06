import D0.Algebra.OriginalBookLocalMovedOperand
import D0.Algebra.OriginalBookJuliaRightGram1009

/-! Proposed direct link from the source local moved operand to the exact
fixed-field right Gram. The displayed assertions are candidates pending Lean. -/
open Matrix
open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookMovedJuliaLeft
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookLocalCreators
open D0.Algebra.OriginalBookLocalBoost
open D0.Algebra.OriginalBookLocalStaticRoots
open D0.Algebra.OriginalBookLocalMovedOperand
open D0.Algebra.OriginalBookJuliaRightGram1009
open D0.Algebra.OriginalBookJuliaLagrange1009
open D0.Algebra.OriginalBookLocalMovedRoots

namespace D0.Algebra.OriginalBookLocalMovedGram

lemma localGenerator_source_mod :
    localGenerator.map redPlus = sourceBoostGenerator.map (Int.castRingHom (ZMod 1009)) := by
  rw [localGenerator_mod]
  simp only [localCreator_mod, localCreator_mod_conjugate]
  ext i j
  simp [sourceBoostGenerator, sourceCreatorMatrix, Matrix.mul_apply, Matrix.transpose_apply]

lemma localBoost_forty_mod :
    localBoost.map redPlus = (1 / 40 : ZMod 1009) •
      (fortyBoost.map (Int.castRingHom (ZMod 1009))) := by
  rw [localBoost_mod, localGenerator_source_mod]
  ext i j
  by_cases h : i = j <;>
    simp [fortyBoost, Matrix.mul_apply, Matrix.add_apply, Matrix.smul_apply,
      Matrix.map_apply, Matrix.ofNat_apply, h, div_eq_mul_inv] <;> ring_nf <;> norm_num
  all_goals decide

lemma localCreatorBoost_forty_mod :
    (localCreator D).map redPlus * localBoost.map redPlus =
      (1 / 40 : ZMod 1009) • modForty := by
  rw [localBoost_forty_mod, localCreator_mod]
  ext i j
  simp [modForty, fortyMoved, sourceCreatorMatrix, Matrix.mul_apply,
    Matrix.smul_apply, div_eq_mul_inv, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro x hx
  ring

/-- Both modular operand images are scalar multiples of the actual source fortyMoved. -/
theorem localMovedOperand_plus_forty :
    localMovedOperand.map redPlus = ((469 : ZMod 1009) * (3 / 200)) • modForty := by
  rw [localMovedOperand_mod_plus, localCreatorBoost_forty_mod, smul_smul]
  congr 1

theorem localMovedOperand_minus_forty :
    localMovedOperand.map redMinus = ((540 : ZMod 1009) * (3 / 200)) • modForty := by
  rw [localMovedOperand_mod_minus, localBoost_mod_conjugate]
  rw [localCreator_mod_conjugate, ← localCreator_mod D]
  rw [localCreatorBoost_forty_mod, smul_smul]
  congr 1

/-- Conjugation occurs before the redPlus evaluation, as required by the source. -/
theorem localMoved_rightGram_mod :
    (localMovedOperandᴴ * localMovedOperand).map redPlus = sourceRightGramMod := by
  rw [Matrix.map_mul, localMovedOperand_dagger_mod,
    localMovedOperand_minus_forty, localMovedOperand_plus_forty]
  simp only [Matrix.transpose_smul, smul_mul_smul, sourceRightGramMod]
  congr 1

theorem localMoved_rightGram_mod_minus :
    (localMovedOperandᴴ * localMovedOperand).map redMinus = sourceRightGramMod := by
  rw [Matrix.map_mul, localMovedOperand_dagger_mod_minus,
    localMovedOperand_plus_forty, localMovedOperand_minus_forty]
  simp only [Matrix.transpose_smul, smul_mul_smul, sourceRightGramMod]
  congr 1

/-- The original modular Lagrange polynomial agrees with the local right root. -/
theorem localMoved_rightLagrange_mod :
    sourceLagrange ((localMovedOperandᴴ * localMovedOperand).map redPlus) =
      localMovedRight.map redPlus := by
  rw [localMoved_rightGram_mod, sourceRightGramMod_lagrange, localMovedRight_mod]

theorem localMoved_rightLagrange_mod_minus :
    sourceLagrange ((localMovedOperandᴴ * localMovedOperand).map redMinus) =
      localMovedRight.map redMinus := by
  rw [localMoved_rightGram_mod_minus, sourceRightGramMod_lagrange, localMovedRight_mod_minus]

end D0.Algebra.OriginalBookLocalMovedGram
