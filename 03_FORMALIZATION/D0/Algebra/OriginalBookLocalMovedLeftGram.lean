import D0.Algebra.OriginalBookLocalMovedGram

/-! Candidate left modular counterpart for the original moved-D source.
These proposed statements have not yet passed Lean. -/
open Matrix
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookMovedJuliaLeft
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookLocalMovedRoots
open D0.Algebra.OriginalBookLocalMovedOperand
open D0.Algebra.OriginalBookJuliaLagrange1009
open D0.Algebra.OriginalBookJuliaRightGram1009
open D0.Algebra.OriginalBookLocalMovedGram

namespace D0.Algebra.OriginalBookLocalMovedLeftGram

noncomputable def modMedium : Matrix (Fin 16) (Fin 16) (ZMod 1009) :=
  Matrix.diagonal fun i => if mediumIndex i then 1 else 0
noncomputable def modLarge : Matrix (Fin 16) (Fin 16) (ZMod 1009) :=
  Matrix.diagonal fun i => if largeIndex i then 1 else 0

lemma medium_sq : modMedium * modMedium = modMedium := by
  unfold modMedium
  rw [Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  split_ifs <;> simp

lemma large_sq : modLarge * modLarge = modLarge := by
  unfold modLarge
  rw [Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  split_ifs <;> simp

lemma medium_large_zero : modMedium * modLarge = 0 := by
  unfold modMedium modLarge
  rw [Matrix.diagonal_mul_diagonal]
  ext i j
  by_cases h : i = j
  · subst i
    fin_cases j <;> norm_num [Matrix.diagonal, mediumIndex, largeIndex] <;> decide
  · simp [Matrix.diagonal, h]

lemma large_medium_zero : modLarge * modMedium = 0 := by
  unfold modMedium modLarge
  rw [Matrix.diagonal_mul_diagonal]
  ext i j
  by_cases h : i = j
  · subst i
    fin_cases j <;> norm_num [Matrix.diagonal, mediumIndex, largeIndex] <;> decide
  · simp [Matrix.diagonal, h]

/-- Source 40-times matrix has this exact left Gram, no spectral premise. -/
theorem sourceLeftGramMod_decomposition :
    (9 / 40000 : ZMod 1009) • (modForty * modForty.transpose) =
      (969 : ZMod 1009) • modMedium + (410 : ZMod 1009) • modLarge := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom (ZMod 1009))) fortyMoved_leftGram
  change ((fortyMoved * fortyMoved.transpose).map (Int.castRingHom (ZMod 1009))) =
    movedGramInt.map (Int.castRingHom (ZMod 1009)) at h
  rw [Matrix.map_mul, Matrix.transpose_map] at h
  rw [show modForty * modForty.transpose = movedGramInt.map (Int.castRingHom (ZMod 1009)) from h]
  ext i j
  by_cases h : i = j
  · subst i
    fin_cases j <;>
      norm_num [modMedium, modLarge, movedGramInt, Matrix.diagonal, mediumIndex, largeIndex,
        Matrix.map_apply, Matrix.smul_apply] <;> decide
  · simp [modMedium, modLarge, movedGramInt, Matrix.diagonal, h]

theorem localMoved_leftGram_mod :
    (localMovedOperand * localMovedOperandᴴ).map redPlus =
      (969 : ZMod 1009) • modMedium + (410 : ZMod 1009) • modLarge := by
  rw [Matrix.map_mul, localMovedOperand_dagger_mod,
    localMovedOperand_minus_forty, localMovedOperand_plus_forty]
  simp only [Matrix.transpose_smul, smul_mul_smul]
  rw [← sourceLeftGramMod_decomposition]
  congr 1

theorem leftProjectors_lagrange :
    sourceLagrange ((969 : ZMod 1009) • modMedium + (410 : ZMod 1009) • modLarge) =
      modMovedLeft := by
  rw [sourceLagrange_projectors modMedium modLarge medium_sq large_sq medium_large_zero large_medium_zero]
  ext i j
  by_cases h : i = j
  · subst i
    fin_cases j <;> norm_num [modMedium, modLarge, modMovedLeft, modMovedLeftValue,
      Matrix.diagonal, mediumIndex, largeIndex] <;> decide
  · simp [modMedium, modLarge, modMovedLeft, Matrix.diagonal, h]

theorem localMoved_leftLagrange_mod :
    sourceLagrange ((localMovedOperand * localMovedOperandᴴ).map redPlus) =
      localMovedLeft.map redPlus := by
  rw [localMoved_leftGram_mod, leftProjectors_lagrange, localMovedLeft_mod]

theorem localMoved_leftGram_mod_minus :
    (localMovedOperand * localMovedOperandᴴ).map redMinus =
      (969 : ZMod 1009) • modMedium + (410 : ZMod 1009) • modLarge := by
  rw [Matrix.map_mul, localMovedOperand_dagger_mod_minus,
    localMovedOperand_plus_forty, localMovedOperand_minus_forty]
  simp only [Matrix.transpose_smul, smul_mul_smul]
  rw [← sourceLeftGramMod_decomposition]
  congr 1

theorem localMoved_leftLagrange_mod_minus :
    sourceLagrange ((localMovedOperand * localMovedOperandᴴ).map redMinus) =
      localMovedLeft.map redMinus := by
  rw [localMoved_leftGram_mod_minus, leftProjectors_lagrange, localMovedLeft_mod_minus]

end D0.Algebra.OriginalBookLocalMovedLeftGram
