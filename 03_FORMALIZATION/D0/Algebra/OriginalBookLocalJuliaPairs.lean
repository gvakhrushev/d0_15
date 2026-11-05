import D0.Algebra.OriginalBookLocalMovedOperand
import D0.Algebra.OriginalBookLocalMovedRoots
import D0.Geometry.OriginalBookJuliaWords

/-! Candidate local pair layer. No theorem here is validated until narrow Lean. -/
open Matrix
open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.CubicExponential
open D0.Geometry.OriginalBookStaticRoots
open D0.Geometry.OriginalBookJuliaWords
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookLocalCreators
open D0.Algebra.OriginalBookLocalBoost
open D0.Algebra.OriginalBookLocalStaticRoots
open D0.Algebra.OriginalBookLocalMovedRoots
open D0.Algebra.OriginalBookLocalMovedOperand

namespace D0.Algebra.OriginalBookLocalJuliaPairs

noncomputable def localPhase (r : Role) : LocalSource :=
  if r = A ∨ r = D then localI else if r = B then -1 else -localI

noncomputable def localBase (r : Role) : LocalOperator := (3 * localInv5) • localCreator r

noncomputable def localLiveOperand (r : Role) : LocalOperator :=
  if r = D then localMovedOperand else localPhase r • localBase r

noncomputable def localLiveLeft (r : Role) : LocalOperator :=
  if r = D then localMovedLeft else localStaticLeft r
noncomputable def localLiveRight (r : Role) : LocalOperator :=
  if r = D then localMovedRight else localStaticRight r

noncomputable def localRowPair (mode row : Fin 4) : LocalOperator × LocalOperator :=
  let r := modeRole mode
  if row = 0 then (localLiveOperand r, localLiveLeft r)
  else if row = 1 then ((localLiveOperand r)ᴴ, localLiveRight r)
  else if row = 2 then (-localBase r, -localStaticLeft r)
  else (-(localBase r)ᴴ, -localStaticRight r)

theorem localPhase_complex (r : Role) : localSourceToComplex (localPhase r) = sourceRolePhase r := by
  simp only [localPhase, sourceRolePhase]
  split_ifs <;> simp [localSourceToComplex_generators.2.2]

theorem localBase_complex (r : Role) : (localBase r).map localSourceToComplex = sourceBase r := by
  have hc (i j : Fin 16) : localSourceToComplex (localCreator r i j) = sourceCreatorComplex r i j := by
    exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localCreator_complex r)
  ext i j
  simp [localBase, sourceBase, complexInv5, hc, map_ofNat, div_eq_mul_inv, mul_assoc]

theorem localLiveOperand_complex (r : Role) :
    (localLiveOperand r).map localSourceToComplex = sourceAnalyticOperand r := by
  by_cases h : r = D
  · subst r
    exact localMovedOperand_complex
  · have hb (i j : Fin 16) : localSourceToComplex (localBase r i j) = sourceBase r i j := by
      exact congrArg (fun M : Matrix (Fin 16) (Fin 16) ℂ => M i j) (localBase_complex r)
    ext i j
    simp [localLiveOperand, h, sourceAnalyticOperand, sourceBase, localPhase_complex, hb,
      Matrix.mul_apply, mul_assoc]

theorem localLiveLeft_complex (r : Role) : (localLiveLeft r).map localSourceToComplex = liveLeft r := by
  by_cases h : r = D
  · subst r; exact localMovedLeft_complex
  · simpa [localLiveLeft, h] using localStaticLeft_live r h

theorem localLiveRight_complex (r : Role) : (localLiveRight r).map localSourceToComplex = liveRight r := by
  by_cases h : r = D
  · subst r; exact localMovedRight_complex
  · simpa [localLiveRight, h] using localStaticRight_live r h

theorem localRowPair_complex (mode row : Fin 4) :
    ((localRowPair mode row).1.map localSourceToComplex,
      (localRowPair mode row).2.map localSourceToComplex) = rowPair mode row := by
  fin_cases row <;> simp [localRowPair, rowPair, localLiveOperand_complex, localLiveLeft_complex,
    localLiveRight_complex, localBase_complex, localStaticLeft_complex, localStaticRight_complex,
    localDagger_complex, Matrix.map_neg]

end D0.Algebra.OriginalBookLocalJuliaPairs
