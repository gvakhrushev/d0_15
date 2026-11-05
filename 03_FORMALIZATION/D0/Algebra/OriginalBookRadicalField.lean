import Mathlib.Algebra.QuadraticAlgebra.Basic
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# Rational quadratic tower for the source radical coefficients

Pinned sources: uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
line 16, and modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a,
lines 22-33 and 97-104 at commit eebcb5e467742df3e9cf7fa9702042d7294aa742.

This builds the characteristic-zero field underlying the proposed ring for
p=(sqrt 5-1)/2, q=sqrt 24142/200, and i. It proves the two real nonsquare
obligations from exact finite arithmetic, then the absence of a square root of
-1 via the actual embedding into the reals. It does not yet construct the
localized integer subring, a finite-field specialization, source coefficient
membership, determinant, or source-effect lower bound.
-/

namespace D0.Algebra.OriginalBookRadicalField

private lemma nonsquare5_nat : ¬ IsSquare (5 : ℕ) := by
  rintro ⟨n, hn⟩
  have hz := congrArg (fun a : ℕ => (a : ZMod 3)) hn
  norm_num at hz
  have h : ∀ x : ZMod 3, x * x ≠ 2 := by decide
  exact h (n : ZMod 3) hz.symm

private lemma nonsquare24142_nat : ¬ IsSquare (24142 : ℕ) := by
  rintro ⟨n, hn⟩
  have hz := congrArg (fun a : ℕ => (a : ZMod 4)) hn
  norm_num at hz
  have h : ∀ x : ZMod 4, x * x ≠ 2 := by decide
  exact h (n : ZMod 4) hz.symm

private lemma nonsquare120710_nat : ¬ IsSquare (120710 : ℕ) := by
  rintro ⟨n, hn⟩
  have hz := congrArg (fun a : ℕ => (a : ZMod 4)) hn
  norm_num at hz
  have h : ∀ x : ZMod 4, x * x ≠ 2 := by decide
  exact h (n : ZMod 4) hz.symm

lemma nonsquare5_rat : ¬ IsSquare (5 : ℚ) := by
  exact Rat.isSquare_natCast_iff.not.mpr nonsquare5_nat

lemma nonsquare24142_rat : ¬ IsSquare (24142 : ℚ) := by
  exact Rat.isSquare_natCast_iff.not.mpr nonsquare24142_nat

lemma nonsquare120710_rat : ¬ IsSquare (120710 : ℚ) := by
  exact Rat.isSquare_natCast_iff.not.mpr nonsquare120710_nat

instance golden_nonsquare : Fact (∀ r : ℚ, r ^ 2 ≠ 5 + 0 * r) := ⟨by
  intro r h
  apply nonsquare5_rat
  exact ⟨r, by simpa [pow_two] using h.symm⟩⟩

abbrev GoldenField := QuadraticAlgebra ℚ (5 : ℚ) 0

/-- The second source radical is not already in Q(sqrt(5)). -/
theorem second_radical_nonsquare : ∀ r : GoldenField, r ^ 2 ≠ 24142 + 0 * r := by
  intro r h
  have hr := congrArg QuadraticAlgebra.re h
  have hi := congrArg QuadraticAlgebra.im h
  simp [pow_two, QuadraticAlgebra.re_ofNat, QuadraticAlgebra.im_ofNat] at hr hi
  have hab : r.re * r.im = 0 := by nlinarith [hi]
  rcases mul_eq_zero.mp hab with ha | hb
  · apply nonsquare120710_rat
    refine ⟨5 * r.im, ?_⟩
    rw [ha] at hr
    nlinarith [hr]
  · apply nonsquare24142_rat
    refine ⟨r.re, ?_⟩
    rw [hb] at hr
    nlinarith [hr]

instance second_nonsquare : Fact (∀ r : GoldenField, r ^ 2 ≠ 24142 + 0 * r) :=
  ⟨second_radical_nonsquare⟩

abbrev RealRadicalField := QuadraticAlgebra GoldenField 24142 0

/-- The real positive root selects the intended source embedding of sqrt(5). -/
noncomputable def goldenToReal : GoldenField →ₐ[ℚ] ℝ :=
  QuadraticAlgebra.lift ⟨Real.sqrt 5, by
    simp [Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 5)]⟩

noncomputable instance : Algebra GoldenField ℝ := goldenToReal.toRingHom.toAlgebra

/-- The second positive root selects the intended real source embedding. -/
noncomputable def realRadicalToReal : RealRadicalField →ₐ[GoldenField] ℝ :=
  QuadraticAlgebra.lift ⟨Real.sqrt 24142, by
    simp only [Algebra.smul_def, map_ofNat, map_zero, zero_mul, add_zero, mul_one]
    exact Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 24142)⟩

/-- A real subfield has no square root of -1. -/
theorem minus_one_nonsquare : ∀ r : RealRadicalField, r ^ 2 ≠ -1 + 0 * r := by
  intro r h
  have hh : (realRadicalToReal r) ^ 2 = -1 := by
    simpa using congrArg realRadicalToReal h
  nlinarith [sq_nonneg (realRadicalToReal r)]

instance third_nonsquare : Fact (∀ r : RealRadicalField, r ^ 2 ≠ -1 + 0 * r) :=
  ⟨minus_one_nonsquare⟩

abbrev SourceRadicalField := QuadraticAlgebra RealRadicalField (-1) 0

noncomputable instance : Algebra RealRadicalField ℂ :=
  (Complex.ofRealHom.comp realRadicalToReal.toRingHom).toAlgebra

/-- Complex evaluation uses the real positive radical branches and i. -/
noncomputable def sourceRadicalToComplex : SourceRadicalField →ₐ[RealRadicalField] ℂ :=
  QuadraticAlgebra.lift ⟨Complex.I, by simp [Algebra.smul_def]⟩

/-- The characteristic-zero model embeds faithfully into the actual complex field. -/
theorem sourceRadicalToComplex_injective : Function.Injective sourceRadicalToComplex :=
  RingHom.injective sourceRadicalToComplex.toRingHom

/-- Named generators in the actual three-stage rational tower. -/
def radicalS : SourceRadicalField :=
  algebraMap RealRadicalField SourceRadicalField
    (algebraMap GoldenField RealRadicalField (QuadraticAlgebra.omega : GoldenField))

def radicalT : SourceRadicalField :=
  algebraMap RealRadicalField SourceRadicalField (QuadraticAlgebra.omega : RealRadicalField)

def radicalI : SourceRadicalField := QuadraticAlgebra.omega

/-- Complex evaluation chooses the same positive real roots and i as the source. -/
theorem sourceRadicalToComplex_generators :
    sourceRadicalToComplex radicalS = (Real.sqrt 5 : ℂ) ∧
    sourceRadicalToComplex radicalT = (Real.sqrt 24142 : ℂ) ∧
    sourceRadicalToComplex radicalI = Complex.I := by
  constructor
  · simp only [radicalS, AlgHom.commutes]
    change (realRadicalToReal (algebraMap GoldenField RealRadicalField
      (QuadraticAlgebra.omega : GoldenField)) : ℂ) = _
    rw [realRadicalToReal.commutes]
    change (goldenToReal (QuadraticAlgebra.omega : GoldenField) : ℂ) = _
    simp [goldenToReal, QuadraticAlgebra.lift, QuadraticAlgebra.omega]
    change ((0 : ℚ) : ℝ) + (1 : ℚ) • Real.sqrt 5 = Real.sqrt 5
    simp
  constructor
  · simp only [radicalT, AlgHom.commutes]
    change (realRadicalToReal (QuadraticAlgebra.omega : RealRadicalField) : ℂ) = _
    simp [realRadicalToReal, QuadraticAlgebra.lift, QuadraticAlgebra.omega]
  · simp [radicalI, sourceRadicalToComplex, QuadraticAlgebra.lift, QuadraticAlgebra.omega]
/-- The positive source Julia coefficient is the second tower radical divided by 200. -/
theorem sourceJuliaRoot_eq_radicalT :
    Real.sqrt (12071 / 20000 : ℝ) = Real.sqrt 24142 / 200 := by
  have h1 := Real.sq_sqrt (show (0 : ℝ) ≤ 12071 / 20000 by norm_num)
  have h2 := Real.sq_sqrt (show (0 : ℝ) ≤ 24142 by norm_num)
  have hn1 := Real.sqrt_nonneg (12071 / 20000 : ℝ)
  have hn2 := Real.sqrt_nonneg (24142 : ℝ)
  nlinarith

/-- The two real source constants in the rational field model. -/
noncomputable def sourceP : SourceRadicalField := (radicalS - 1) / 2
noncomputable def sourceQ : SourceRadicalField := radicalT / 200

/-- Complex images match the source Golden parameter and the positive Julia root. -/
theorem sourceRadicalToComplex_sourceConstants :
    sourceRadicalToComplex sourceP = (((Real.sqrt 5 - 1) / 2 : ℝ) : ℂ) ∧
    sourceRadicalToComplex sourceQ = (Real.sqrt (12071 / 20000 : ℝ) : ℂ) := by
  have hs := sourceRadicalToComplex_generators.1
  have ht := sourceRadicalToComplex_generators.2.1
  constructor
  · simp [sourceP, hs, map_ofNat]
  · rw [sourceJuliaRoot_eq_radicalT]
    simp [sourceQ, ht, map_ofNat]
end D0.Algebra.OriginalBookRadicalField
