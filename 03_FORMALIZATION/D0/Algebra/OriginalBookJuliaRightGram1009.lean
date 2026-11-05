import D0.Algebra.OriginalBookJuliaLagrangeApplication

/-! The original integer fortyMoved right Gram mapped to F1009. The factor
9/40000 is the source operand magnitude (3/5)/40 squared; identifying this
with both star-sensitive local operand evaluations is a separate task. -/
open Matrix
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookMovedJuliaLeft
open D0.Geometry.OriginalBookMovedJuliaRight
open D0.Algebra.OriginalBookLocalMovedRoots
open D0.Algebra.OriginalBookJuliaLagrange1009
open D0.Algebra.OriginalBookJuliaLagrangeApplication

namespace D0.Algebra.OriginalBookJuliaRightGram1009

def modForty : Matrix (Fin 16) (Fin 16) (ZMod 1009) :=
  fortyMoved.map (Int.castRingHom (ZMod 1009))

theorem modForty_transpose_mul :
    modForty.transpose * modForty = (1600 : ZMod 1009) • modRegular + modNumerator := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom (ZMod 1009))) sourceRightGram
  change ((fortyMoved.transpose * fortyMoved).map (Int.castRingHom (ZMod 1009))) =
    ((1600 : ℤ) • regularInt + blockNumeratorInt).map (Int.castRingHom (ZMod 1009)) at h
  rw [Matrix.map_mul, Matrix.transpose_map] at h
  ext i j
  have hij := congrFun (congrFun h i) j
  simp only [Matrix.map_apply, Matrix.add_apply, Matrix.smul_apply, map_add, map_zsmul] at hij
  simpa only [modForty, modRegular, modNumerator, Matrix.smul_apply, Matrix.add_apply,
    Matrix.map_apply, zsmul_eq_mul, smul_eq_mul, Int.cast_ofNat] using hij

def sourceRightGramMod : Matrix (Fin 16) (Fin 16) (ZMod 1009) :=
  (9 / 40000 : ZMod 1009) • (modForty.transpose * modForty)

theorem sourceRightGramMod_decomposition :
    sourceRightGramMod = (969 : ZMod 1009) • modRegular + (410 : ZMod 1009) • modBoosted := by
  rw [sourceRightGramMod, modForty_transpose_mul]
  simp only [smul_add, smul_smul, modBoosted]
  match_scalars <;> decide

theorem sourceRightGramMod_lagrange : sourceLagrange sourceRightGramMod = modMovedRight := by
  rw [sourceRightGramMod_decomposition, right_projectors_lagrange]

end D0.Algebra.OriginalBookJuliaRightGram1009
