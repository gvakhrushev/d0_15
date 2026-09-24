import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import Mathlib.Tactic.Module

set_option linter.unusedSimpArgs false

/-!
# Exact two-jet congruence for a quadratic cell energy

`Q(t) = I + t G + t² K / 2` is inverted and multiplied only through order `t²`.
The coefficient

`2 (Gᵀ)² + 2 Gᵀ G + 2 G² - (Kᵀ + K)`

is an algebraic identity for the background `B₀ = I`. A fixed background `B₀`
keeps the weighted form

`2 (Gᵀ)² B₀ + 2 Gᵀ B₀ G + 2 B₀ G² - Kᵀ B₀ - B₀ K`.

`K` is not selected. The exponential law `K = G²` is a specialization of this
identity, not a physical stress tensor. The pairing-forced dual jet is the
inverse transpose; it does not make the placement a metric star.
-/

namespace D0.Geometry

open Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Truncated matter jet `I + t lin + t² quad / 2`. -/
structure TwoJet (ι : Type*) [Fintype ι] [DecidableEq ι] where
  lin : Matrix ι ι ℚ
  quad : Matrix ι ι ℚ

namespace TwoJet

def eval (J : TwoJet ι) (t : ℚ) : Matrix ι ι ℚ :=
  1 + t • J.lin + (t ^ 2 / 2) • J.quad

def mul (J K : TwoJet ι) : TwoJet ι where
  lin := J.lin + K.lin
  quad := J.quad + K.quad + (2 : ℚ) • (J.lin * K.lin)

/-- Formal inverse through order `t²`: `I - t G + t² (2 G² - K) / 2`. -/
def inv (J : TwoJet ι) : TwoJet ι where
  lin := -J.lin
  quad := (2 : ℚ) • (J.lin * J.lin) - J.quad

def transpose (J : TwoJet ι) : TwoJet ι where
  lin := J.linᵀ
  quad := J.quadᵀ

theorem eval_zero (J : TwoJet ι) : J.eval 0 = 1 := by
  simp [eval]

theorem inv_lin (J : TwoJet ι) : J.inv.lin = -J.lin := rfl

theorem inv_quad (J : TwoJet ι) : J.inv.quad = (2 : ℚ) • (J.lin * J.lin) - J.quad := rfl

theorem eval_mul_exact (J K : TwoJet ι) (t : ℚ) :
    J.eval t * K.eval t =
      (J.mul K).eval t +
        (t ^ 3 / 2) • (J.lin * K.quad + J.quad * K.lin) +
        (t ^ 4 / 4) • (J.quad * K.quad) := by
  simp only [eval, mul, add_mul, mul_add, one_mul, mul_one, smul_mul_assoc,
    mul_smul_comm, smul_smul, smul_add, add_smul]
  module

theorem inv_mul_truncates (J : TwoJet ι) :
    (J.inv.mul J).lin = 0 ∧ (J.inv.mul J).quad = 0 := by
  constructor
  · simp [inv, mul]
  · simp only [inv, mul, neg_mul, smul_neg, sub_eq_add_neg]
    module

/-- Second-order coefficient of `Q(t)⁻ᵀ B₀ Q(t)⁻¹`. -/
def weightedCongruence (J : TwoJet ι) (B0 : Matrix ι ι ℚ) : Matrix ι ι ℚ :=
  J.inv.transpose.quad * B0 + B0 * J.inv.quad +
    (2 : ℚ) • (J.inv.transpose.lin * B0 * J.inv.lin)

theorem weightedCongruence_eq (J : TwoJet ι) (B0 : Matrix ι ι ℚ) :
    J.weightedCongruence B0 =
      (2 : ℚ) • ((J.linᵀ * J.linᵀ) * B0) + (2 : ℚ) • (J.linᵀ * B0 * J.lin) +
        (2 : ℚ) • (B0 * (J.lin * J.lin)) - (J.quadᵀ * B0 + B0 * J.quad) := by
  simp only [weightedCongruence, inv, transpose]
  rw [Matrix.transpose_sub, Matrix.transpose_smul, Matrix.transpose_mul, Matrix.transpose_neg]
  simp only [sub_eq_add_neg, add_mul, mul_add, smul_mul_assoc, mul_smul_comm, smul_add,
    add_smul, neg_mul, mul_neg, neg_neg]
  module

/-- Capstone for the identity background `B₀ = I`. -/
def secondOrderCongruenceCoefficient (J : TwoJet ι) : Matrix ι ι ℚ :=
  (2 : ℚ) • (J.linᵀ * J.linᵀ) + (2 : ℚ) • (J.linᵀ * J.lin) +
    (2 : ℚ) • (J.lin * J.lin) - (J.quadᵀ + J.quad)

theorem secondOrderCongruenceCoefficient_eq (J : TwoJet ι) :
    J.weightedCongruence 1 = J.secondOrderCongruenceCoefficient := by
  rw [weightedCongruence_eq, secondOrderCongruenceCoefficient]
  simp

theorem secondOrderCongruenceCoefficient_formula (G K : Matrix ι ι ℚ) :
    (TwoJet.mk G K).secondOrderCongruenceCoefficient =
      (2 : ℚ) • (Gᵀ * Gᵀ) + (2 : ℚ) • (Gᵀ * G) + (2 : ℚ) • (G * G) - (Kᵀ + K) := by
  simp [secondOrderCongruenceCoefficient]

/-- Exponential specialization `K = G²`, not a selection of `K`. -/
theorem exponentialSecondJet_specialization (G : Matrix ι ι ℚ) :
    (TwoJet.mk G (G * G)).secondOrderCongruenceCoefficient =
      Gᵀ * Gᵀ + (2 : ℚ) • (Gᵀ * G) + G * G := by
  rw [secondOrderCongruenceCoefficient_formula]
  simp only [Matrix.transpose_mul, sub_eq_add_neg, add_smul, smul_add]
  module

/-- Chain-rule jet `I + t H(h) + t²/2 (H(a) + B(h,h))`. `B` is supplied. -/
def backgroundSecondJet (Hh Ha Bhh : Matrix ι ι ℚ) (t : ℚ) : Matrix ι ι ℚ :=
  1 + t • Hh + (t ^ 2 / 2) • (Ha + Bhh)

/-- If covariance identifies the background second jet with the congruence
coefficient, the supplied Hessian stays that coefficient. -/
theorem backgroundJet_eq_congruence (G K hessian : Matrix ι ι ℚ)
    (hcov : hessian = (TwoJet.mk G K).secondOrderCongruenceCoefficient) :
    hessian =
      (2 : ℚ) • (Gᵀ * Gᵀ) + (2 : ℚ) • (Gᵀ * G) + (2 : ℚ) • (G * G) - (Kᵀ + K) := by
  rw [hcov, secondOrderCongruenceCoefficient_formula]

theorem exponential_background_specialization (G Ha Bhh : Matrix ι ι ℚ)
    (hcov : Ha + Bhh =
      (TwoJet.mk G (G * G)).secondOrderCongruenceCoefficient) :
    Ha + Bhh = Gᵀ * Gᵀ + (2 : ℚ) • (Gᵀ * G) + G * G := by
  rw [hcov, exponentialSecondJet_specialization]

/-- Dual reading of the inverse jet. It does not make the pairing a metric star. -/
theorem dualInverseTranspose_lin (J : TwoJet ι) :
    J.inv.transpose.lin = -J.linᵀ := by
  simp [inv, transpose, Matrix.transpose_neg]

theorem dualInverseTranspose_quad (J : TwoJet ι) :
    J.inv.transpose.quad = (2 : ℚ) • (J.linᵀ * J.linᵀ) - J.quadᵀ := by
  simp only [inv, transpose, Matrix.transpose_neg, Matrix.transpose_sub,
    Matrix.transpose_mul, Matrix.transpose_smul]

/-- Typed constitutive product `S(t) = R(t) S₀ Q(t)⁻¹` through order `t²`.
`S₀` is supplied. No constitutive law is constructed. -/
theorem constitutiveSecondDerivative
    (HD KD GP KP S0 : Matrix ι ι ℚ) (t : ℚ) :
    ((TwoJet.mk HD KD).eval t) * S0 * ((TwoJet.mk GP KP).inv.eval t) =
      S0 + t • (HD * S0 - S0 * GP) +
        (t ^ 2 / 2) •
          (KD * S0 - (2 : ℚ) • (HD * S0 * GP) + S0 * ((2 : ℚ) • (GP * GP) - KP)) +
        (t ^ 3 / 2) •
          (HD * S0 * ((2 : ℚ) • (GP * GP) - KP) - KD * S0 * GP) +
        (t ^ 4 / 4) • (KD * S0 * ((2 : ℚ) • (GP * GP) - KP)) := by
  simp only [eval, inv, add_mul, mul_add, mul_sub, one_mul, mul_one, smul_mul_assoc,
    mul_smul_comm, smul_smul, smul_add, add_smul, smul_sub, sub_eq_add_neg, mul_neg, neg_mul,
    neg_neg, mul_assoc]
  module

end TwoJet

end D0.Geometry
