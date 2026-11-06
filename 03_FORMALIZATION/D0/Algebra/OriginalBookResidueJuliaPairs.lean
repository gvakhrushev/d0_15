import D0.Algebra.OriginalBookLocalJuliaPairs

/-! Executable evaluations of the original Julia row pairs over GF(1009).
The two evaluations differ on the imaginary unit. Taking an adjoint switches
the evaluation before transposing. All run-time entries use finite-field
arithmetic on the original integer creator and projector data. -/

open Matrix D0
open D0.Geometry.OriginalBookCreatorBridge D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookJuliaWords
open D0.Algebra.OriginalBookRadicalLocal D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookLocalCreators D0.Algebra.OriginalBookLocalBoost
open D0.Algebra.OriginalBookLocalStaticRoots D0.Algebra.OriginalBookLocalMovedOperand
open D0.Algebra.OriginalBookLocalMovedRoots D0.Algebra.OriginalBookLocalJuliaPairs

namespace D0.Algebra.OriginalBookResidueJuliaPairs

abbrev ResidueOperator := Matrix (Fin 16) (Fin 16) (ZMod 1009)

private def creator (r : Role) : ResidueOperator := fun i j => sourceCreator (sourceBit r) i j

private def base (r : Role) : ResidueOperator := (3 / 5 : ZMod 1009) • creator r

private def generator : ResidueOperator :=
  creator A * (creator D).transpose + creator D * (creator A).transpose

private def boost : ResidueOperator :=
  1 + (1 / 40 : ZMod 1009) • (generator * generator) + (9 / 40 : ZMod 1009) • generator

private def imaginary (minus : Bool) : ZMod 1009 := if minus then 540 else 469

private def phase (minus : Bool) (r : Role) : ZMod 1009 :=
  if r = A ∨ r = D then imaginary minus else if r = B then -1 else -imaginary minus

private def operand (minus : Bool) (r : Role) : ResidueOperator :=
  if r = D then (imaginary minus * (3 / 5 : ZMod 1009)) • (creator D * boost)
  else phase minus r • base r

private def staticLeft (r : Role) : ResidueOperator :=
  1 - (1 / 5 : ZMod 1009) • (creator r * (creator r).transpose)

private def staticRight (r : Role) : ResidueOperator :=
  1 - (1 / 5 : ZMod 1009) • ((creator r).transpose * creator r)

private def movedRight : ResidueOperator :=
  let boosted := (1 / 1762 : ZMod 1009) • modNumerator
  1 - modRegular - boosted + (4 / 5 : ZMod 1009) • modRegular + (278 : ZMod 1009) • boosted

/-- First or conjugate evaluation of both endpoints, in the source mode/row order. -/
def residueRowPair (minus : Bool) (mode row : Fin 4) : ResidueOperator × ResidueOperator :=
  let r := modeRole mode
  if row = 0 then (operand minus r, if r = D then modMovedLeft else staticLeft r)
  else if row = 1 then ((operand (!minus) r).transpose, if r = D then movedRight else staticRight r)
  else if row = 2 then (-base r, -staticLeft r)
  else (-(base r).transpose, -staticRight r)

private noncomputable def evaluation : Bool → LocalSource →+* ZMod 1009
  | false => redPlus
  | true => redMinus

private theorem creator_image (b : Bool) (r : Role) :
    (localCreator r).map (evaluation b) = creator r := by
  cases b
  · exact localCreator_mod r
  · exact localCreator_mod_conjugate r

private theorem base_image (b : Bool) (r : Role) : (localBase r).map (evaluation b) = base r := by
  have h5 : evaluation b localInv5 = (1 / 5 : ZMod 1009) := by
    cases b
    · exact modInv5
    · exact modInv5_minus
  have hc (i j : Fin 16) := congrArg (fun X : ResidueOperator => X i j) (creator_image b r)
  ext i j
  simp only [Matrix.map_apply] at hc
  simp [localBase, base, h5, hc, div_eq_mul_inv, map_ofNat]

private theorem boost_image (b : Bool) : localBoost.map (evaluation b) = boost := by
  cases b <;> simp only [evaluation, boost, generator, localBoost_mod_conjugate,
    localBoost_mod, localGenerator_mod, localCreator_mod, localCreator_mod_conjugate] <;> rfl

private theorem phase_image (b : Bool) (r : Role) : evaluation b (localPhase r) = phase b r := by
  have hi : evaluation b localI = imaginary b := by
    cases b
    · change redPlus localI = 469
      simpa [redPair] using congrArg Prod.fst redPair_generators.2.2
    · change redMinus localI = 540
      simpa [redPair] using congrArg Prod.snd redPair_generators.2.2
  by_cases had : r = A ∨ r = D
  · simpa only [localPhase, phase, had, if_true] using hi
  · simp only [localPhase, phase, if_neg had]
    by_cases hb : r = B <;> simp only [hb, if_true, if_false, map_neg, map_one, hi]

private theorem operand_image (b : Bool) (r : Role) :
    (localLiveOperand r).map (evaluation b) = operand b r := by
  by_cases hr : r = D
  · subst r
    have hm : localMovedOperand.map (evaluation b) =
        (imaginary b * (3 / 5 : ZMod 1009)) •
          ((localCreator D).map (evaluation b) * localBoost.map (evaluation b)) := by
      cases b
      · exact localMovedOperand_mod_plus
      · exact localMovedOperand_mod_minus
    simp only [localLiveOperand, operand, if_true, hm, creator_image, boost_image]
  · have he (i j : Fin 16) := congrArg (fun X : ResidueOperator => X i j) (base_image b r)
    ext i j
    simp only [Matrix.map_apply] at he
    simp only [localLiveOperand, operand, hr, if_false, Matrix.map_apply, Matrix.smul_apply,
      smul_eq_mul, map_mul, phase_image, he]

private theorem staticLeft_image (b : Bool) (r : Role) :
    (localStaticLeft r).map (evaluation b) = staticLeft r := by
  cases b <;> simp only [evaluation, staticLeft, localStaticLeft_mod, localStaticLeft_mod_minus,
    localCreator_mod, localCreator_mod_conjugate] <;> rfl

private theorem staticRight_image (b : Bool) (r : Role) :
    (localStaticRight r).map (evaluation b) = staticRight r := by
  cases b <;> simp only [evaluation, staticRight, localStaticRight_mod, localStaticRight_mod_minus,
    localCreator_mod, localCreator_mod_conjugate] <;> rfl

private theorem dagger_image (b : Bool) (M : LocalOperator) :
    Mᴴ.map (evaluation b) = (M.map (evaluation (!b))).transpose := by
  cases b
  · exact localDagger_mod M
  · exact localDagger_mod_minus M

private theorem left_image (b : Bool) (r : Role) :
    (localLiveLeft r).map (evaluation b) = if r = D then modMovedLeft else staticLeft r := by
  by_cases h : r = D
  · cases b <;> simp only [localLiveLeft, h, if_true, evaluation,
        localMovedLeft_mod, localMovedLeft_mod_minus]
  · simpa only [localLiveLeft, h, if_false] using staticLeft_image b r

private theorem right_image (b : Bool) (r : Role) :
    (localLiveRight r).map (evaluation b) = if r = D then movedRight else staticRight r := by
  by_cases h : r = D
  · cases b <;> simp only [localLiveRight, h, if_true, evaluation,
        localMovedRight_mod, localMovedRight_mod_minus, movedRight, modMovedRight, modBoosted]
  · simpa only [localLiveRight, h, if_false] using staticRight_image b r

private theorem pair_image (b : Bool) (mode row : Fin 4) :
    ((localRowPair mode row).1.map (evaluation b), (localRowPair mode row).2.map (evaluation b)) =
      residueRowPair b mode row := by
  fin_cases row <;> simp [localRowPair, residueRowPair, operand_image, base_image, dagger_image,
    left_image, right_image, staticLeft_image, staticRight_image, Matrix.map_neg]

theorem localRowPair_mod_plus (mode row : Fin 4) :
    ((localRowPair mode row).1.map redPlus, (localRowPair mode row).2.map redPlus) =
      residueRowPair false mode row := pair_image false mode row

theorem localRowPair_mod_minus (mode row : Fin 4) :
    ((localRowPair mode row).1.map redMinus, (localRowPair mode row).2.map redMinus) =
      residueRowPair true mode row := pair_image true mode row

end D0.Algebra.OriginalBookResidueJuliaPairs
