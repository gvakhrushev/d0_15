import D0.Algebra.OriginalBookLocalMovedRoots

/-! Proposed source operand in local coefficient ring. The Python source uses
phase +i for D; reduction must apply star before redPlus (i -> 540 under the
opposite evaluation). This file is a candidate pending Lean verification. -/
open Matrix
open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.CubicExponential
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookLocalCreators
open D0.Algebra.OriginalBookLocalBoost
open D0.Algebra.OriginalBookLocalStaticRoots

namespace D0.Algebra.OriginalBookLocalMovedOperand

noncomputable def localMovedOperand : LocalOperator :=
  (localI * (3 * localInv5)) • (localCreator D * localBoost)

theorem localMovedOperand_complex :
    localMovedOperand.map localSourceToComplex = sourceAnalyticOperand D := by
  have hc (i j : Fin 16) : localSourceToComplex (localCreator D i j) =
      sourceCreatorComplex D i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localCreator_complex D)
  have hu (i j : Fin 16) : localSourceToComplex (localBoost i j) =
      NormedSpace.exp (sourceTheta • sourceComplexGenerator) i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) localBoost_complex
  ext i j
  simp [localMovedOperand, sourceAnalyticOperand, sourceRolePhase_values.2.1,
    Matrix.mul_apply, hc, hu, localSourceToComplex_generators.2.2, complexInv5, map_ofNat,
    div_eq_mul_inv, mul_assoc]

/-- Both explicit residues retain the distinct conjugate i values. -/
theorem localMovedOperand_mod_plus :
    localMovedOperand.map redPlus =
      ((469 : ZMod 1009) * (3 / 5)) •
        ((localCreator D).map redPlus * localBoost.map redPlus) := by
  have hi : redPlus localI = 469 := by
    simpa [redPair] using congrArg Prod.fst redPair_generators.2.2
  ext i j
  simp [localMovedOperand, Matrix.mul_apply, hi, modInv5, map_ofNat, div_eq_mul_inv]

theorem localMovedOperand_mod_minus :
    localMovedOperand.map redMinus =
      ((540 : ZMod 1009) * (3 / 5)) •
        ((localCreator D).map redMinus * localBoost.map redMinus) := by
  have hi : redMinus localI = 540 := by
    simpa [redPair] using congrArg Prod.snd redPair_generators.2.2
  ext i j
  simp [localMovedOperand, Matrix.mul_apply, hi, modInv5_minus, map_ofNat, div_eq_mul_inv]

theorem localMovedOperand_dagger_mod :
    localMovedOperandᴴ.map redPlus = (localMovedOperand.map redMinus).transpose :=
  localDagger_mod localMovedOperand

theorem localMovedOperand_dagger_mod_minus :
    localMovedOperandᴴ.map redMinus = (localMovedOperand.map redPlus).transpose :=
  localDagger_mod_minus localMovedOperand

end D0.Algebra.OriginalBookLocalMovedOperand
