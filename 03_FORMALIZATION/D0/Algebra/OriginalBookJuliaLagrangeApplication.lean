import D0.Algebra.OriginalBookJuliaLagrange1009
import D0.Algebra.OriginalBookLocalMovedRoots
import Mathlib.Tactic

/-! The generic pinned interpolation applied to the concrete moved-D right
projectors. This does not itself identify their weighted sum with the source
Gram or execute the Python implementation. -/
open Matrix
open D0.Algebra.OriginalBookLocalMovedRoots
open D0.Algebra.OriginalBookJuliaLagrange1009
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookMovedJuliaRight

namespace D0.Algebra.OriginalBookJuliaLagrangeApplication

lemma regular_mod_sq : modRegular * modRegular = modRegular := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom (ZMod 1009))) regularInt_sq
  change ((regularInt * regularInt).map (Int.castRingHom (ZMod 1009))) =
    regularInt.map (Int.castRingHom (ZMod 1009)) at h
  rw [Matrix.map_mul] at h
  exact h

lemma numerator_mod_sq : modNumerator * modNumerator = (1762 : ZMod 1009) • modNumerator := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom (ZMod 1009))) blockNumeratorInt_sq
  change ((blockNumeratorInt * blockNumeratorInt).map (Int.castRingHom (ZMod 1009))) =
    ((1762 : ℤ) • blockNumeratorInt).map (Int.castRingHom (ZMod 1009)) at h
  rw [Matrix.map_mul] at h
  ext i j
  have hij := congrFun (congrFun h i) j
  simpa [modNumerator, Matrix.smul_apply, Matrix.mul_apply, Matrix.ofNat_apply] using hij

lemma regular_mod_num_zero : modRegular * modNumerator = 0 := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom (ZMod 1009))) regularInt_block_mul_zero
  change ((regularInt * blockNumeratorInt).map (Int.castRingHom (ZMod 1009))) =
    (0 : SourceMatrix).map (Int.castRingHom (ZMod 1009)) at h
  rw [Matrix.map_mul] at h
  simpa [modRegular, modNumerator] using h

lemma num_mod_regular_zero : modNumerator * modRegular = 0 := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom (ZMod 1009))) block_regularInt_mul_zero
  change ((blockNumeratorInt * regularInt).map (Int.castRingHom (ZMod 1009))) =
    (0 : SourceMatrix).map (Int.castRingHom (ZMod 1009)) at h
  rw [Matrix.map_mul] at h
  simpa [modRegular, modNumerator] using h

lemma boosted_mod_sq : modBoosted * modBoosted = modBoosted := by
  simp only [modBoosted, smul_mul_smul, numerator_mod_sq, smul_smul]
  congr 1

lemma regular_boosted_mod_zero : modRegular * modBoosted = 0 := by
  simp [modBoosted, regular_mod_num_zero]

lemma boosted_regular_mod_zero : modBoosted * modRegular = 0 := by
  simp [modBoosted, num_mod_regular_zero]

theorem right_projectors_lagrange :
    sourceLagrange ((969 : ZMod 1009) • modRegular + (410 : ZMod 1009) • modBoosted) =
      modMovedRight := by
  rw [sourceLagrange_projectors modRegular modBoosted regular_mod_sq boosted_mod_sq
    regular_boosted_mod_zero boosted_regular_mod_zero]
  unfold modMovedRight
  have h : (4 / 5 : ZMod 1009) = 808 := by decide
  rw [h]

end D0.Algebra.OriginalBookJuliaLagrangeApplication
