import D0.Geometry.OriginalBookBoost
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Tactic

/-!
The original uniform source `check_uniform_book_source.py`, blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, uses the matrix exponential
of its creator-built generator. The original full128 modular checker,
`check_future_even_algebra_modprime.py`, blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`, specializes
`theta = log(5/4)` and uses a rational polynomial in that generator.
We prove `tanh(theta/2) = 1/9`. Both refs are at commit
eebcb5e467742df3e9cf7fa9702042d7294aa742.

The generic proof derives the exponential of any cubic generator from
the ODE and applies it to both real and complex source matrices. It also
matches all four phased Julia operands. Julia square roots, the 128 Kraus
operators, their future-effect span and physical realization remain open.
-/

open NormedSpace
open scoped Matrix.Norms.Operator

namespace D0.Geometry.CubicExponential

variable {A : Type*} [NormedRing A] [NormedAlgebra ℝ A] [CompleteSpace A]

noncomputable def sh (t : ℝ) : ℝ := (Real.exp t - Real.exp (-t)) / 2
noncomputable def ch (t : ℝ) : ℝ := (Real.exp t + Real.exp (-t)) / 2

lemma sh_derivative (t : ℝ) : HasDerivAt sh (ch t) t := by
  have hp := Real.hasDerivAt_exp t
  have hn := (Real.hasDerivAt_exp (-t)).comp t (hasDerivAt_id t).neg
  convert (hp.sub hn).div_const 2 using 1
  simp [ch]

lemma ch_derivative (t : ℝ) : HasDerivAt ch (sh t) t := by
  have hp := Real.hasDerivAt_exp t
  have hn := (Real.hasDerivAt_exp (-t)).comp t (hasDerivAt_id t).neg
  convert (hp.add hn).div_const 2 using 1
  simp [sh, sub_eq_add_neg]

noncomputable def flow (g : A) (t : ℝ) : A :=
  1 + sh t • g + (ch t - 1) • (g * g)

omit [CompleteSpace A] in
lemma flow_commutes (g : A) (t : ℝ) : g * flow g t = flow g t * g := by
  simp [flow, mul_add, add_mul, mul_assoc]

omit [CompleteSpace A] in
lemma flow_derivative (g : A) (hg : g * g * g = g) (t : ℝ) :
    HasDerivAt (flow g) (flow g t * g) t := by
  have h := ((hasDerivAt_const t (1 : A)).add ((sh_derivative t).smul_const g)).add
    (((ch_derivative t).sub_const 1).smul_const (g * g))
  convert h using 1
  simp only [flow, add_mul, one_mul, smul_mul_assoc, hg]
  module

noncomputable def correction (g : A) (t : ℝ) : A :=
  exp (t • (-g)) * flow g t

lemma correction_derivative (g : A) (hg : g * g * g = g) (t : ℝ) :
    HasDerivAt (correction g) 0 t := by
  have h := (hasDerivAt_exp_smul_const (-g) t).mul (flow_derivative g hg t)
  convert h using 1
  symm
  have hc : (-g) * flow g t + flow g t * g = 0 := by
    rw [neg_mul, flow_commutes]
    exact neg_add_cancel _
  calc
    (exp (t • -g) * -g) * flow g t + exp (t • -g) * (flow g t * g) =
        exp (t • -g) * ((-g) * flow g t + flow g t * g) := by noncomm_ring
    _ = 0 := by rw [hc, mul_zero]

lemma correction_eq_one (g : A) (hg : g * g * g = g) (t : ℝ) :
    correction g t = 1 := by
  have h := is_const_of_deriv_eq_zero
    (fun x => (correction_derivative g hg x).differentiableAt)
    (fun x => (correction_derivative g hg x).deriv) t 0
  simpa [correction, flow, sh, ch] using h

lemma exp_eq_flow (g : A) (hg : g * g * g = g) (t : ℝ) :
    exp (t • g) = flow g t := by
  letI : NormedAlgebra ℚ A := .restrictScalars ℚ ℝ A
  have hc : Commute (t • g) (t • (-g)) :=
    (((Commute.refl g).neg_right).smul_left t).smul_right t
  have hinv : exp (t • g) * exp (t • (-g)) = 1 := by
    rw [← exp_add_of_commute hc]
    simp
  have h := correction_eq_one g hg t
  unfold correction at h
  calc
    exp (t • g) = exp (t • g) * 1 := by simp
    _ = exp (t • g) * (exp (t • (-g)) * flow g t) := by rw [h]
    _ = flow g t := by rw [← mul_assoc, hinv, one_mul]


/-! The source specialization keeps the analytic theta and polynomial boost
separate until the equality below is proved. It does not construct any Kraus
operator or assert a physical realization. -/

noncomputable def sourceTheta : ℝ := Real.log (5 / 4)

lemma source_exp_theta : Real.exp sourceTheta = 5 / 4 := by
  unfold sourceTheta
  rw [Real.exp_log (by norm_num : (0 : ℝ) < 5 / 4)]

lemma source_exp_neg_theta : Real.exp (-sourceTheta) = 4 / 5 := by
  rw [Real.exp_neg, source_exp_theta]
  norm_num

lemma source_sh_theta : sh sourceTheta = 9 / 40 := by
  simp [sh, source_exp_theta, source_exp_neg_theta]
  norm_num

lemma source_ch_theta : ch sourceTheta = 41 / 40 := by
  simp [ch, source_exp_theta, source_exp_neg_theta]
  norm_num

/-- The source parameter is the hyperbolic tangent of the half-angle. -/
theorem source_half_angle : Real.tanh (sourceTheta / 2) = 1 / 9 := by
  have hp : 0 < Real.exp (sourceTheta / 2) := Real.exp_pos _
  have hs : Real.exp (sourceTheta / 2) ^ 2 = 5 / 4 := by
    rw [pow_two, ← Real.exp_add]
    have h : sourceTheta / 2 + sourceTheta / 2 = sourceTheta := by ring
    rw [h, source_exp_theta]
  rw [Real.tanh_eq, Real.exp_neg]
  have hd : Real.exp (sourceTheta / 2) + (Real.exp (sourceTheta / 2))⁻¹ ≠ 0 := by positivity
  field_simp
  nlinarith

open D0.Geometry.OriginalBookBoost

noncomputable def sourceRealGenerator : Matrix (Fin 16) (Fin 16) ℝ :=
  sourceBoostGeneratorRat.map (Rat.castHom ℝ)

lemma sourceRealGenerator_cube :
    sourceRealGenerator * sourceRealGenerator * sourceRealGenerator = sourceRealGenerator := by
  have h := congrArg
    (fun m : Matrix (Fin 16) (Fin 16) ℚ => m.map (Rat.castHom ℝ)) sourceBoostGeneratorRat_cube
  change ((sourceBoostGeneratorRat * sourceBoostGeneratorRat * sourceBoostGeneratorRat).map
    (Rat.castHom ℝ)) = sourceBoostGeneratorRat.map (Rat.castHom ℝ) at h
  rw [Matrix.map_mul, Matrix.map_mul] at h
  exact h

set_option backward.isDefEq.respectTransparency false in
/-- The real matrix exponential is exactly the published rational polynomial. -/
theorem original_boost_exponential :
    exp (sourceTheta • sourceRealGenerator) = sourceRationalBoost.map (Rat.castHom ℝ) := by
  rw [exp_eq_flow sourceRealGenerator sourceRealGenerator_cube sourceTheta]
  simp only [flow, source_sh_theta, source_ch_theta]
  ext i j
  by_cases h : i = j <;>
    simp [sourceRationalBoost, sourceRealGenerator, Matrix.mul_apply, h] <;> ring

noncomputable def sourceComplexGenerator : Matrix (Fin 16) (Fin 16) ℂ :=
  sourceBoostGeneratorRat.map (Rat.castHom ℂ)

lemma sourceComplexGenerator_cube :
    sourceComplexGenerator * sourceComplexGenerator * sourceComplexGenerator =
      sourceComplexGenerator := by
  have h := congrArg
    (fun m : Matrix (Fin 16) (Fin 16) ℚ => m.map (Rat.castHom ℂ)) sourceBoostGeneratorRat_cube
  change ((sourceBoostGeneratorRat * sourceBoostGeneratorRat * sourceBoostGeneratorRat).map
    (Rat.castHom ℂ)) = sourceBoostGeneratorRat.map (Rat.castHom ℂ) at h
  rw [Matrix.map_mul, Matrix.map_mul] at h
  exact h

set_option backward.isDefEq.respectTransparency false in
/-- The same equality in the complex matrix carrier used by the source. -/
theorem original_complex_boost_exponential :
    exp (sourceTheta • sourceComplexGenerator) = sourceRationalBoost.map (Rat.castHom ℂ) := by
  rw [exp_eq_flow sourceComplexGenerator sourceComplexGenerator_cube sourceTheta]
  simp only [flow, source_sh_theta, source_ch_theta]
  ext i j
  by_cases h : i = j <;>
    simp [sourceRationalBoost, sourceComplexGenerator, Matrix.mul_apply, h] <;> ring

/-- The complex generator is precisely the original creator/dagger expression. -/
theorem sourceComplexGenerator_eq_creators :
    sourceComplexGenerator =
      sourceCreatorComplex D0.A * (sourceCreatorComplex D0.D).conjTranspose +
        sourceCreatorComplex D0.D * (sourceCreatorComplex D0.A).conjTranspose := by
  ext i j
  simp [sourceComplexGenerator, sourceBoostGeneratorRat, sourceBoostGenerator,
    sourceCreatorComplex, Matrix.mul_apply, Matrix.conjTranspose_apply]

/-- The analytic source's four Julia operands at the exact checker angle. -/
noncomputable def sourceAnalyticOperand (role : D0.Role) : Matrix (Fin 16) (Fin 16) ℂ :=
  sourceRolePhase role •
    (((3 / 5 : ℂ) • sourceCreatorComplex role) *
      (if role = D0.D then exp (sourceTheta • sourceComplexGenerator) else 1))

/-- Analytic and rational constructions give identical inputs for all roles. -/
theorem sourceAnalyticOperand_eq_polynomial (role : D0.Role) :
    sourceAnalyticOperand role = sourcePolynomialOperand role := by
  simp [sourceAnalyticOperand, sourcePolynomialOperand, original_complex_boost_exponential]

end D0.Geometry.CubicExponential
