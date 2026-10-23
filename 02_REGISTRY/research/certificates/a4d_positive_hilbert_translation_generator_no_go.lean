import Mathlib.Tactic

/-!
# Lorentz-covariant linear data cannot have a finite positive Hilbert norm

This capsule proves a direct infinite-carrier extension of the positive
quadratic obstruction. A real-linear map from Minkowski translation data into
a positive Hilbert space, whose norm is invariant under the owned rational
boost and spatial quarter-turns, must vanish. For Hilbert-Schmidt generators,
the target norm is the Hilbert-Schmidt norm and unitary Lorentz conjugation
provides the required isometry.
-/

namespace D0.Research.PositiveHilbertTranslationGeneratorNoGo

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The linear readout determined by its four Minkowski basis values. -/
def linearReadout (A B C D : E) (t x y z : ℝ) : E :=
  t • A + x • B + y • C + z • D

private theorem norm_sq_smul (r : ℝ) (x : E) :
    ‖r • x‖ ^ 2 = r ^ 2 * ‖x‖ ^ 2 := by
  simp [norm_smul, Real.norm_eq_abs, mul_pow]

private theorem norm_sq_smul_add (r s : ℝ) (x y : E) :
    ‖r • x + s • y‖ ^ 2 =
      r ^ 2 * ‖x‖ ^ 2 + 2 * r * s * inner ℝ x y + s ^ 2 * ‖y‖ ^ 2 := by
  rw [norm_add_sq_real, norm_sq_smul, real_inner_smul_left,
    real_inner_smul_right, norm_sq_smul]
  ring

/-- A positive-norm linear readout of a Lorentz vector cannot be
Lorentz-invariant unless it is zero. `hboost` is invariance under the exact
`(5/3,4/3)` boost; applying it at the inverse-boosted basis vector supplies
the opposite sign as well. The two quarter-turns move the spatial basis
vectors into the boosted direction. -/
theorem lorentz_invariant_positive_readout_eq_zero
    (A B C D : E)
    (hboost : ∀ t x y z,
      ‖linearReadout A B C D ((5*t+4*x)/3) ((4*t+5*x)/3) y z‖ =
        ‖linearReadout A B C D t x y z‖)
    (hquarterZ : ∀ t x y z,
      ‖linearReadout A B C D t (-y) x z‖ =
        ‖linearReadout A B C D t x y z‖)
    (hquarterY : ∀ t x y z,
      ‖linearReadout A B C D t z y (-x)‖ =
        ‖linearReadout A B C D t x y z‖) :
    A = 0 ∧ B = 0 ∧ C = 0 ∧ D = 0 := by
  have hplus := congrArg (fun r : ℝ => r ^ 2) (hboost 1 0 0 0)
  have hminus := congrArg (fun r : ℝ => r ^ 2) (hboost (5/3) (-4/3) 0 0)
  have hplus' :
      ‖(5/3 : ℝ) • A + (4/3 : ℝ) • B‖ ^ 2 = ‖A‖ ^ 2 := by
    simpa [linearReadout] using hplus
  have hminus' :
      ‖(5/3 : ℝ) • A + (-4/3 : ℝ) • B‖ ^ 2 = ‖A‖ ^ 2 := by
    have ht : ((5*(5/3 : ℝ)+4*(-4/3 : ℝ))/3) = 1 := by norm_num
    have hx : ((4*(5/3 : ℝ)+5*(-4/3 : ℝ))/3) = 0 := by norm_num
    simpa [linearReadout, ht, hx] using hminus.symm
  have hplus_eq :
      (5/3 : ℝ)^2 * ‖A‖^2 + 2*(5/3:ℝ)*(4/3:ℝ)*inner ℝ A B +
        (4/3:ℝ)^2 * ‖B‖^2 = ‖A‖^2 := by
    simpa [norm_sq_smul_add] using hplus'
  have hminus_eq :
      (5/3 : ℝ)^2 * ‖A‖^2 + 2*(5/3:ℝ)*(-4/3:ℝ)*inner ℝ A B +
        (-4/3:ℝ)^2 * ‖B‖^2 = ‖A‖^2 := by
    simpa [norm_sq_smul_add] using hminus'
  have hA2 : ‖A‖^2 = 0 := by nlinarith [hplus_eq, hminus_eq]
  have hB2 : ‖B‖^2 = 0 := by nlinarith [hplus_eq, hminus_eq]
  have hA : A = 0 := norm_eq_zero.mp (by nlinarith [sq_nonneg (‖A‖)])
  have hB : B = 0 := norm_eq_zero.mp (by nlinarith [sq_nonneg (‖B‖)])
  have hCnorm : ‖C‖ = 0 := by
    have h := hquarterZ 0 1 0 0
    simpa [linearReadout, hB] using h
  have hDnorm : ‖D‖ = 0 := by
    have h := hquarterY 0 1 0 0
    simpa [linearReadout, hB] using h
  have hC : C = 0 := norm_eq_zero.mp hCnorm
  have hD : D = 0 := norm_eq_zero.mp hDnorm
  exact ⟨hA, hB, hC, hD⟩

#check lorentz_invariant_positive_readout_eq_zero
#print axioms lorentz_invariant_positive_readout_eq_zero

end D0.Research.PositiveHilbertTranslationGeneratorNoGo
