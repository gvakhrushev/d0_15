import D0.Algebra.OriginalBookRadicalLocal
import Mathlib.Algebra.Star.Basic
import Mathlib.Tactic

/-!
# Two conjugate mod-1009 specializations of the local radical model

The original source blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a, at
commit eebcb5e467742df3e9cf7fa9702042d7294aa742, lines 22–33 and 64–74,
uses (sqrt5,p,sqrtp,q,i)=(244,626,226,278,469) modulo 1009. The local
model uses s=sqrt5, t=200q and z=i, hence residues s=244, t=105, z=469.
Conjugation is performed in the source model before evaluation. A second
ordinary field hom evaluates the conjugate at z=540; the pair exchanges under
star. This does not use a fictitious conjugating star on F1009 and does not
assert source coefficient membership or any rank result.
-/

open D0.Algebra.OriginalBookRadicalLocal

namespace D0.Algebra.OriginalBookRadicalMod1009

instance prime1009 : Fact (Nat.Prime 1009) := ⟨by norm_num⟩

/-- The source denominator is invertible in the specified prime field. -/
noncomputable def localBaseToMod : LocalBase →+* ZMod 1009 :=
  IsLocalization.Away.lift (8810 : ℤ) (g := Int.castRingHom (ZMod 1009)) (by
    apply isUnit_iff_ne_zero.mpr
    decide)

/-- Evaluate one quadratic extension using an actual root in a target ring. -/
noncomputable def quadraticEval {R S : Type*} [CommRing R] [CommRing S]
    (f : R →+* S) (a b : R) (u : S) (hu : u * u = f a + f b * u) :
    QuadraticAlgebra R a b →+* S := by
  letI : Algebra R S := f.toAlgebra
  exact (QuadraticAlgebra.lift ⟨u, by simpa [Algebra.smul_def] using hu⟩).toRingHom

/-- The evaluation formula, recorded for checking source generators and star. -/
theorem quadraticEval_apply {R S : Type*} [CommRing R] [CommRing S]
    (f : R →+* S) (a b : R) (u : S) (hu : u * u = f a + f b * u)
    (x : QuadraticAlgebra R a b) :
    quadraticEval f a b u hu x = f x.re + f x.im * u := by
  change f x.re * 1 + f x.im * u = _
  simp

noncomputable def localGoldenToMod : LocalGolden →+* ZMod 1009 :=
  quadraticEval localBaseToMod 5 0 244 (by
    simp only [map_ofNat, map_zero, zero_mul, add_zero]
    decide)

noncomputable def localRealToMod : LocalReal →+* ZMod 1009 :=
  quadraticEval localGoldenToMod 24142 0 105 (by
    simp only [map_ofNat, map_zero, zero_mul, add_zero]
    decide)

/-- The plus map is the original specialization i ↦ 469. -/
noncomputable def redPlus : LocalSource →+* ZMod 1009 :=
  quadraticEval localRealToMod (-1) 0 469 (by
    simp only [map_neg, map_one, map_zero, zero_mul, add_zero]
    decide)

/-- The second map evaluates after taking the actual model conjugate. -/
noncomputable def redMinus : LocalSource →+* ZMod 1009 :=
  redPlus.comp (starRingEnd LocalSource)

noncomputable def redPair : LocalSource →+* ZMod 1009 × ZMod 1009 :=
  redPlus.prod redMinus

/-- The exact swap law for the pair, not an identity-star map to one field. -/
theorem redPair_star (x : LocalSource) : redPair (star x) = (redPair x).swap := by
  simp [redPair, redMinus, starRingEnd_apply]

/-- Standard quadratic generator in each source-local stage. -/
def localS : LocalSource := algebraMap LocalReal LocalSource
  (algebraMap LocalGolden LocalReal (QuadraticAlgebra.omega : LocalGolden))

def localT : LocalSource := algebraMap LocalReal LocalSource (QuadraticAlgebra.omega : LocalReal)
def localI : LocalSource := QuadraticAlgebra.omega

/-- Exact original split-field values and the conjugate value of i. -/
theorem redPair_generators :
    redPair localS = (244, 244) ∧ redPair localT = (105, 105) ∧
      redPair localI = (469, 540) := by
  simp [redPair, redPlus, redMinus, quadraticEval_apply, localGoldenToMod,
    localRealToMod, localS, localT, localI, QuadraticAlgebra.omega,
    starRingEnd_apply, QuadraticAlgebra.re_star, QuadraticAlgebra.im_star,
    QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  decide

/-- The ordinary field evaluation cannot itself preserve source conjugation. -/
theorem redPlus_not_star_invariant : redPlus (star localI) ≠ redPlus localI := by
  have hp : redPlus localI = 469 := by
    simpa [redPair] using congrArg Prod.fst redPair_generators.2.2
  have hm : redMinus localI = 540 := by
    simpa [redPair] using congrArg Prod.snd redPair_generators.2.2
  have hstar : redPlus (star localI) = redMinus localI := by
    simpa [redPair] using congrArg Prod.fst (redPair_star localI)
  rw [hstar, hm, hp]
  decide

/-- The exact source p/q residues match the pinned modular fixture. -/
theorem source_residue_relations :
    (2 : ZMod 1009) * 626 + 1 = redPlus localS ∧
      (200 : ZMod 1009) * 278 = redPlus localT ∧
      (226 : ZMod 1009) ^ 2 = 626 := by
  have hs : redPlus localS = 244 := by
    simpa [redPair] using congrArg Prod.fst redPair_generators.1
  have ht : redPlus localT = 105 := by
    simpa [redPair] using congrArg Prod.fst redPair_generators.2.1
  rw [hs, ht]
  decide

/-- The local-to-rational embedding preserves the model's conjugation. -/
theorem localSourceToField_star (x : LocalSource) :
    localSourceToField (star x) = star (localSourceToField x) := by
  apply QuadraticAlgebra.ext <;>
    simp [localSourceToField, quadraticMap, QuadraticAlgebra.re_star, QuadraticAlgebra.im_star]

/-- The complex map evaluates a + b i with the proven real embedding of a,b. -/
theorem sourceRadicalToComplex_apply (x : D0.Algebra.OriginalBookRadicalField.SourceRadicalField) :
    D0.Algebra.OriginalBookRadicalField.sourceRadicalToComplex x =
      (D0.Algebra.OriginalBookRadicalField.realRadicalToReal x.re : ℂ) +
        (D0.Algebra.OriginalBookRadicalField.realRadicalToReal x.im : ℂ) * Complex.I := by
  simp [D0.Algebra.OriginalBookRadicalField.sourceRadicalToComplex,
    QuadraticAlgebra.lift, Algebra.smul_def]
  rfl

/-- The target complex star is the actual source model conjugation. -/
theorem localSourceToComplex_star (x : LocalSource) :
    localSourceToComplex (star x) = star (localSourceToComplex x) := by
  change D0.Algebra.OriginalBookRadicalField.sourceRadicalToComplex
      (localSourceToField (star x)) =
      star (D0.Algebra.OriginalBookRadicalField.sourceRadicalToComplex (localSourceToField x))
  rw [localSourceToField_star, sourceRadicalToComplex_apply, sourceRadicalToComplex_apply]
  simp [QuadraticAlgebra.re_star, QuadraticAlgebra.im_star]
/-- The local generators map to exactly the named rational-tower generators. -/
theorem localSourceToField_generators :
    localSourceToField localS = D0.Algebra.OriginalBookRadicalField.radicalS ∧
      localSourceToField localT = D0.Algebra.OriginalBookRadicalField.radicalT ∧
      localSourceToField localI = D0.Algebra.OriginalBookRadicalField.radicalI := by
  simp [localS, localT, localI, localSourceToField, localRealToField, localGoldenToField,
    quadraticMap, QuadraticAlgebra.omega, QuadraticAlgebra.algebraMap_eq,
    QuadraticAlgebra.re_one, QuadraticAlgebra.im_one,
    D0.Algebra.OriginalBookRadicalField.radicalS, D0.Algebra.OriginalBookRadicalField.radicalT,
    D0.Algebra.OriginalBookRadicalField.radicalI]
  repeat' constructor

/-- The same local generators embed as positive source radicals and complex i. -/
theorem localSourceToComplex_generators :
    localSourceToComplex localS = (Real.sqrt 5 : ℂ) ∧
      localSourceToComplex localT = (Real.sqrt 24142 : ℂ) ∧
      localSourceToComplex localI = Complex.I := by
  simpa [localSourceToComplex, localSourceToField_generators.1,
    localSourceToField_generators.2.1, localSourceToField_generators.2.2] using
      D0.Algebra.OriginalBookRadicalField.sourceRadicalToComplex_generators
end D0.Algebra.OriginalBookRadicalMod1009
