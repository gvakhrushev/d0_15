import D0.Algebra.OriginalBookRadicalField
import Mathlib.RingTheory.Localization.Away.Basic
import Mathlib.Algebra.Ring.Prod
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Local source radical model and faithful complex embedding

The exact source constants come from pinned uniform blob
 ee8de4635d24c668949ac9a0186616ab7d59f2ed and modular blob
 d111c5bfeae3c384a4fe725f4a6d19277ea0005a at commit
 eebcb5e467742df3e9cf7fa9702042d7294aa742.

This is the local coefficient ring over Z[1/8810] with quadratic generators
s²=5, t²=24142, z²=-1. We prove its embedding in the previously verified
rational field tower; this by itself does not show that the source effects lie
in the ring or that any effect determinant is nonzero.
-/
open D0.Algebra.OriginalBookRadicalField

namespace D0.Algebra.OriginalBookRadicalLocal

/-- Functorial map of quadratic algebras with explicitly mapped coefficients. -/
def quadraticMap {R S : Type*} [CommRing R] [CommRing S] (f : R →+* S)
    (a b : R) (a' b' : S) (ha : f a = a') (hb : f b = b') :
    QuadraticAlgebra R a b →+* QuadraticAlgebra S a' b' where
  toFun x := ⟨f x.re, f x.im⟩
  map_one' := by ext <;> simp [QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  map_mul' x y := by ext <;> simp [← ha, ← hb]
  map_zero' := by ext <;> simp
  map_add' x y := by ext <;> simp

/-- Coordinatewise lifting preserves a genuinely injective coefficient map. -/
theorem quadraticMap_injective {R S : Type*} [CommRing R] [CommRing S]
    (f : R →+* S) (hf : Function.Injective f) (a b : R) (a' b' : S)
    (ha : f a = a') (hb : f b = b') :
    Function.Injective (quadraticMap f a b a' b' ha hb) := by
  intro x y h
  apply QuadraticAlgebra.ext
  · apply hf
    exact congrArg QuadraticAlgebra.re h
  · apply hf
    exact congrArg QuadraticAlgebra.im h

abbrev LocalBase := Localization.Away (8810 : ℤ)
abbrev LocalGolden := QuadraticAlgebra LocalBase 5 0
abbrev LocalReal := QuadraticAlgebra LocalGolden 24142 0
abbrev LocalSource := QuadraticAlgebra LocalReal (-1) 0

/-- The actual integer localization maps to Q because 8810 is nonzero. -/
noncomputable def localBaseToRat : LocalBase →+* ℚ :=
  IsLocalization.Away.lift (8810 : ℤ) (g := Int.castRingHom ℚ) (by norm_num)

theorem localBaseToRat_injective : Function.Injective localBaseToRat := by
  apply (IsLocalization.lift_injective_iff _).2
  intro x y
  constructor
  · intro h
    have hh := congrArg localBaseToRat h
    simpa [localBaseToRat] using hh
  · intro h
    apply congrArg (algebraMap ℤ LocalBase)
    exact (Int.cast_injective : Function.Injective (Int.cast : ℤ → ℚ)) h

noncomputable def localGoldenToField : LocalGolden →+* GoldenField :=
  quadraticMap localBaseToRat 5 0 5 0 (by simp [map_ofNat]) (by simp)

noncomputable def localRealToField : LocalReal →+* RealRadicalField :=
  quadraticMap localGoldenToField 24142 0 24142 0 (by simp [map_ofNat]) (by simp)

noncomputable def localSourceToField : LocalSource →+* SourceRadicalField :=
  quadraticMap localRealToField (-1) 0 (-1) 0 (by simp) (by simp)

/-- Every stage is injective; no injection premise is postulated. -/
theorem localSourceToField_injective : Function.Injective localSourceToField := by
  apply quadraticMap_injective
  apply quadraticMap_injective
  apply quadraticMap_injective
  exact localBaseToRat_injective

/-- The local model therefore embeds in the actual complex radical tower. -/
noncomputable def localSourceToComplex : LocalSource →+* ℂ :=
  sourceRadicalToComplex.toRingHom.comp localSourceToField

theorem localSourceToComplex_injective : Function.Injective localSourceToComplex :=
  sourceRadicalToComplex_injective.comp localSourceToField_injective

end D0.Algebra.OriginalBookRadicalLocal
