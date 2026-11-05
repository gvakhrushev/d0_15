import D0.Algebra.OriginalBookRadicalMod1009
import D0.Geometry.OriginalBookGoldenKraus
import D0.Geometry.OriginalBookMovedJuliaRight
import Mathlib.Tactic

/-!
# Exact local representatives of the two source real constants

The source uses p=(sqrt(5)-1)/2 and q=sqrt(12071/20000). In the already
verified local model s²=5, t²=24142, both are represented with denominators
made invertible by localizing away from 8810. The complex embedding uses the
positive roots, and redPlus uses the source mod-1009 split values.

This is a scalar bridge only: membership of the source 16×16 matrices and
all effects, rank certificates, and physical admission are not asserted.
-/
open D0.Algebra.OriginalBookRadicalField
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Geometry.OriginalBookGoldenKraus

namespace D0.Algebra.OriginalBookRadicalSourceConstants

/-- Explicit base map into the top of the three-stage local quadratic tower. -/
def baseIntoSource : LocalBase →+* LocalSource :=
  (algebraMap LocalReal LocalSource).comp
    ((algebraMap LocalGolden LocalReal).comp (algebraMap LocalBase LocalGolden))

/-- The actual inverse of the localization denominator. -/
noncomputable def localInvD : LocalSource :=
  baseIntoSource (IsLocalization.Away.invSelf (8810 : ℤ))

lemma localInvD_spec : (8810 : LocalSource) * localInvD = 1 := by
  have h := congrArg baseIntoSource
    (IsLocalization.Away.mul_invSelf (S := LocalBase) (8810 : ℤ))
  simpa [localInvD, baseIntoSource, map_ofNat] using h

lemma complexInvD : localSourceToComplex localInvD = (1 / 8810 : ℂ) := by
  have h := congrArg localSourceToComplex localInvD_spec
  simp only [map_mul, map_ofNat, map_one] at h
  apply (eq_div_iff (by norm_num : (8810 : ℂ) ≠ 0)).2
  simpa [mul_comm] using h

lemma modInvD : redPlus localInvD = (1 / 8810 : ZMod 1009) := by
  have h := congrArg redPlus localInvD_spec
  simp only [map_mul, map_ofNat, map_one] at h
  apply (eq_div_iff (by decide : (8810 : ZMod 1009) ≠ 0)).2
  simpa [mul_comm] using h

/-- 1/2 = 4405/8810 and 1/200 = 3418989205/8810³. -/
noncomputable def localP : LocalSource := (localS - 1) * (4405 * localInvD)
noncomputable def localQ : LocalSource := localT * (3418989205 * localInvD ^ 3)

/-- Both elements map to the exact source real constants in C. -/
theorem localSourceConstants_complex :
    localSourceToComplex localP = (goldenP : ℂ) ∧
      localSourceToComplex localQ = (D0.Geometry.OrthogonalProjectionRoot.coefficient : ℂ) := by
  have hs := localSourceToComplex_generators.1
  have ht := localSourceToComplex_generators.2.1
  have hq := sourceJuliaRoot_eq_radicalT
  constructor
  · simp [localP, hs, complexInvD, goldenP, map_ofNat]
    ring
  · rw [show D0.Geometry.OrthogonalProjectionRoot.coefficient = Real.sqrt (12071 / 20000 : ℝ) by rfl]
    rw [hq]
    simp [localQ, ht, complexInvD, map_ofNat]
    ring

/-- Their mod-1009 images are the same p and q as the source fixture. -/
theorem localSourceConstants_mod : redPlus localP = 626 ∧ redPlus localQ = 278 := by
  have hs : redPlus localS = 244 := by
    simpa [redPair] using congrArg Prod.fst redPair_generators.1
  have ht : redPlus localT = 105 := by
    simpa [redPair] using congrArg Prod.fst redPair_generators.2.1
  constructor
  · simp only [localP, map_mul, map_sub, map_one, map_ofNat, hs, modInvD]
    decide
  · simp only [localQ, map_mul, map_pow, map_ofNat, ht, modInvD]
    decide

/-- Both source constants are fixed by the actual model conjugation. -/
theorem localSourceConstants_star : star localP = localP ∧ star localQ = localQ := by
  constructor
  · apply localSourceToComplex_injective
    rw [localSourceToComplex_star, localSourceConstants_complex.1]
    simp
  · apply localSourceToComplex_injective
    rw [localSourceToComplex_star, localSourceConstants_complex.2]
    simp

/-- Both conjugate specializations preserve the source real parameters. -/
theorem localSourceConstants_redPair :
    redPair localP = (626, 626) ∧ redPair localQ = (278, 278) := by
  simp [redPair, redMinus, starRingEnd_apply, localSourceConstants_star.1,
    localSourceConstants_star.2, localSourceConstants_mod.1, localSourceConstants_mod.2]
end D0.Algebra.OriginalBookRadicalSourceConstants
