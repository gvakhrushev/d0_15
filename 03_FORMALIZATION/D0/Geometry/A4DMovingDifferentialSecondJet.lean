import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import Mathlib.Tactic.Module
import D0.Geometry.A4DSecondOrderCartanCongruence
import D0.Geometry.ArchiveMovingDifferential

set_option linter.unusedSimpArgs false

/-!
# Second derivative of a moving differential

`movingDifferential_infinitesimal` keeps the quadratic remainder of
`(I + G₁) d (I - G₀)`. For jets `Q_k(t) = I + t G_k + t² K_k / 2`, the moved
differential `d(t) = Q₁(t) d Q₀(t)⁻¹` has second derivative

`d'' = K₁ d - 2 G₁ d G₀ + 2 d G₀² - d K₀`.

The mixed parent `C = d_D S d_P` has the six-term second derivative. Moving
`d` is not set to zero. No sourced stress or Lorentz covariance is claimed.
-/

namespace D0.Geometry

open Matrix

/-- The first-order identity already owned by `movingDifferential_infinitesimal`.
Its quadratic remainder is what the second-jet formula completes. -/
theorem movingDifferential_firstOrder_remainder
    {V0 V1 : Type*} [AddCommGroup V0] [Module ℚ V0] [AddCommGroup V1] [Module ℚ V1]
    (G0 : V0 →ₗ[ℚ] V0) (G1 : V1 →ₗ[ℚ] V1) (d : V0 →ₗ[ℚ] V1) :
    ((LinearMap.id : V1 →ₗ[ℚ] V1) + G1).comp
        (d.comp ((LinearMap.id : V0 →ₗ[ℚ] V0) - G0)) =
      d + movingDifferentialVariation G0 G1 d - (G1.comp d).comp G0 :=
  movingDifferential_infinitesimal G0 G1 d

variable {α β γ δ : Type*}
variable [Fintype α] [Fintype β] [Fintype γ] [Fintype δ]
variable [DecidableEq α] [DecidableEq β] [DecidableEq γ] [DecidableEq δ]

/-- Second-order coefficient of `Q₁(t) d Q₀(t)⁻¹` on one carrier.
Rectangular grade slots use the same algebra; this owner is the compiled
square-carrier identity `TwoJet.constitutiveSecondDerivative`. -/
theorem movingDifferential_secondDerivative
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (G0 K0 G1 K1 d : Matrix ι ι ℚ) (t : ℚ) :
    ((TwoJet.mk G1 K1).eval t) * d * ((TwoJet.mk G0 K0).inv.eval t) =
      d + t • (G1 * d - d * G0) +
        (t ^ 2 / 2) •
          (K1 * d - (2 : ℚ) • (G1 * d * G0) + d * ((2 : ℚ) • (G0 * G0) - K0)) +
        (t ^ 3 / 2) •
          (G1 * d * ((2 : ℚ) • (G0 * G0) - K0) - K1 * d * G0) +
        (t ^ 4 / 4) • (K1 * d * ((2 : ℚ) • (G0 * G0) - K0)) :=
  TwoJet.constitutiveSecondDerivative G1 K1 G0 K0 d t

/-- The degree-one coefficient is the first variation retained by
`movingDifferential_infinitesimal`. -/
theorem movingDifferential_secondDerivative_linear
    (G0 : Matrix α α ℚ) (G1 : Matrix β β ℚ) (d : Matrix β α ℚ) :
    G1 * d - d * G0 = G1 * d + -(d * G0) := by
  abel

/-- Second derivative of `C = d_D S d_P`. Every monomial of the three jets is
retained, left-associated as `(d_D S) d_P`. The six cross terms sit in the
`t²` summands `(t * t) • ((dD1 * S1) * dP0)`, `(t * t) • ((dD1 * S0) * dP1)`
and `(t * t) • ((dD0 * S1) * dP1)`. -/
theorem mixedParent_secondDerivative
    (dD0 dD1 dD2 : Matrix δ γ ℚ) (S0 S1 S2 : Matrix γ β ℚ)
    (dP0 dP1 dP2 : Matrix β α ℚ) (t : ℚ) :
    (dD0 + t • dD1 + (t ^ 2 / 2) • dD2) * (S0 + t • S1 + (t ^ 2 / 2) • S2) *
        (dP0 + t • dP1 + (t ^ 2 / 2) • dP2) =
      (dD0 * S0) * dP0 +
        t • ((dD0 * S0) * dP1) +
        (t ^ 2 / 2) • ((dD0 * S0) * dP2) +
        t • ((dD0 * S1) * dP0) +
        (t * t) • ((dD0 * S1) * dP1) +
        (t * (t ^ 2 / 2)) • ((dD0 * S1) * dP2) +
        (t ^ 2 / 2) • ((dD0 * S2) * dP0) +
        ((t ^ 2 / 2) * t) • ((dD0 * S2) * dP1) +
        ((t ^ 2 / 2) * (t ^ 2 / 2)) • ((dD0 * S2) * dP2) +
        t • ((dD1 * S0) * dP0) +
        (t * t) • ((dD1 * S0) * dP1) +
        (t * (t ^ 2 / 2)) • ((dD1 * S0) * dP2) +
        (t * t) • ((dD1 * S1) * dP0) +
        ((t * t) * t) • ((dD1 * S1) * dP1) +
        ((t * t) * (t ^ 2 / 2)) • ((dD1 * S1) * dP2) +
        (t * (t ^ 2 / 2)) • ((dD1 * S2) * dP0) +
        ((t * (t ^ 2 / 2)) * t) • ((dD1 * S2) * dP1) +
        ((t * (t ^ 2 / 2)) * (t ^ 2 / 2)) • ((dD1 * S2) * dP2) +
        (t ^ 2 / 2) • ((dD2 * S0) * dP0) +
        ((t ^ 2 / 2) * t) • ((dD2 * S0) * dP1) +
        ((t ^ 2 / 2) * (t ^ 2 / 2)) • ((dD2 * S0) * dP2) +
        ((t ^ 2 / 2) * t) • ((dD2 * S1) * dP0) +
        (((t ^ 2 / 2) * t) * t) • ((dD2 * S1) * dP1) +
        (((t ^ 2 / 2) * t) * (t ^ 2 / 2)) • ((dD2 * S1) * dP2) +
        ((t ^ 2 / 2) * (t ^ 2 / 2)) • ((dD2 * S2) * dP0) +
        (((t ^ 2 / 2) * (t ^ 2 / 2)) * t) • ((dD2 * S2) * dP1) +
        (((t ^ 2 / 2) * (t ^ 2 / 2)) * (t ^ 2 / 2)) • ((dD2 * S2) * dP2) := by
  simp only [Matrix.add_mul, Matrix.mul_add, Matrix.smul_mul, Matrix.mul_smul, smul_smul,
    smul_add, add_smul]
  module

end D0.Geometry
