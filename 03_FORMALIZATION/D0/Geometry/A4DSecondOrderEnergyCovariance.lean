import Mathlib.Tactic
import D0.Geometry.A4DDiscreteEnergyKernel

namespace D0.Geometry

open D0
open scoped BigOperators

/-!
# Exact second-order covariance algebra

The coefficients here are formal two-jets: the third field stores the second
derivative, so a Taylor term is `t^2/2 • second`. No finite matter action or
cell-energy selector is assumed.
-/

abbrev SecondJetMatrix (n : ℕ) := Matrix (Fin n) (Fin n) ℚ

/-- Second derivative coefficient of the formal inverse of `I + tG + t²K/2`. -/
def inverseSecondJetCoeff {n : ℕ} (G K : SecondJetMatrix n) : SecondJetMatrix n :=
  (2 : ℚ) • (G * G) - K

/-- The coefficient of `t²` multiplied by two in the inverse-transpose
congruence `Q(t)^{-T} Q(t)^{-1}` at `Q(0)=I`. -/
def secondOrderCongruenceCoefficient {n : ℕ} (G K : SecondJetMatrix n) :
    SecondJetMatrix n :=
  (inverseSecondJetCoeff G K).transpose +
    (2 : ℚ) • (G.transpose * G) + inverseSecondJetCoeff G K

theorem inverseSecondJetCoeff_right_product {n : ℕ}
    (G K : SecondJetMatrix n) :
    K + (2 : ℚ) • (G * (-G)) + inverseSecondJetCoeff G K = 0 := by
  simp [inverseSecondJetCoeff]
  noncomm_ring

theorem inverseSecondJetCoeff_left_product {n : ℕ}
    (G K : SecondJetMatrix n) :
    inverseSecondJetCoeff G K + (2 : ℚ) • ((-G) * G) + K = 0 := by
  simp [inverseSecondJetCoeff]
  noncomm_ring

/-- Exact second derivative in the quadratic-form covariance identity.
This is a coefficient calculation, not a selection of `K`. -/
theorem secondOrderCongruenceCoefficient_eq {n : ℕ}
    (G K : SecondJetMatrix n) :
    secondOrderCongruenceCoefficient G K =
      (2 : ℚ) • (G.transpose * G.transpose) +
        (2 : ℚ) • (G.transpose * G) +
        (2 : ℚ) • (G * G) - (K.transpose + K) := by
  unfold secondOrderCongruenceCoefficient inverseSecondJetCoeff
  simp only [Matrix.transpose_sub, Matrix.transpose_smul, Matrix.transpose_mul]
  simp only [two_smul]
  noncomm_ring

/-- Algebraic background chain rule for `e(t)=t h+t²a/2` and a supplied
symmetric Hessian `B`; the coefficient is kept independent of any chosen law. -/
def cellEnergySecondJetCoeff {V : Type*} [AddCommMonoid V] [Module ℚ V]
    (H : V →ₗ[ℚ] SecondJetMatrix 1)
    (B : V →ₗ[ℚ] V →ₗ[ℚ] SecondJetMatrix 1) (h a : V) :
    SecondJetMatrix 1 := H a + B h h

theorem backgroundChainRule_secondJetCoeff {V : Type*} [AddCommMonoid V] [Module ℚ V]
    (H : V →ₗ[ℚ] SecondJetMatrix 1)
    (B : V →ₗ[ℚ] V →ₗ[ℚ] SecondJetMatrix 1) (h a : V) :
    cellEnergySecondJetCoeff H B h a = H a + B h h := rfl

/-- Under the exact second-order covariance hypothesis, the background chain
coefficient equals the inverse-transpose congruence coefficient. -/
theorem backgroundChainRule_eq_congruence {V : Type*} [AddCommMonoid V] [Module ℚ V]
    (H : V →ₗ[ℚ] SecondJetMatrix 1)
    (B : V →ₗ[ℚ] V →ₗ[ℚ] SecondJetMatrix 1) (h a : V)
    (G K : SecondJetMatrix 1)
    (hcov : cellEnergySecondJetCoeff H B h a = secondOrderCongruenceCoefficient G K) :
    H a + B h h = secondOrderCongruenceCoefficient G K := hcov

/-- Exponential/additive-one-parameter specialization `K=G²`. This rejects
neither a different groupoid jet nor selects a cell coefficient. -/
theorem exponentialSecondJet_specialization {n : ℕ}
    (G : SecondJetMatrix n) :
    secondOrderCongruenceCoefficient G (G * G) =
      G.transpose * G.transpose +
        (2 : ℚ) • (G.transpose * G) + G * G := by
  rw [secondOrderCongruenceCoefficient_eq]
  rw [Matrix.transpose_mul]
  module

/-- A typed formal second jet of a linear map. The `second` field stores the
second derivative (rather than the coefficient of `t²`). -/
structure LinearTwoJet (V W : Type*) [AddCommGroup V] [Module ℚ V]
    [AddCommGroup W] [Module ℚ W] where
  base : V →ₗ[ℚ] W
  first : V →ₗ[ℚ] W
  second : V →ₗ[ℚ] W

/-- Chain rule for typed linear-map two-jets, retaining the mixed term. -/
def LinearTwoJet.comp {U V W : Type*} [AddCommGroup U] [Module ℚ U]
    [AddCommGroup V] [Module ℚ V] [AddCommGroup W] [Module ℚ W]
    (F : LinearTwoJet V W) (G : LinearTwoJet U V) : LinearTwoJet U W where
  base := F.base.comp G.base
  first := F.first.comp G.base + F.base.comp G.first
  second := F.second.comp G.base + (2 : ℚ) • (F.first.comp G.first) +
    F.base.comp G.second

/-- Second derivative of a typed three-factor mixed parent. All six terms are
retained, including every pairwise first-derivative cross term. -/
theorem movingMixedParentSecondJet
    {V₀ V₁ V₂ V₃ : Type*}
    [AddCommGroup V₀] [Module ℚ V₀] [AddCommGroup V₁] [Module ℚ V₁]
    [AddCommGroup V₂] [Module ℚ V₂] [AddCommGroup V₃] [Module ℚ V₃]
    (D : LinearTwoJet V₂ V₃) (S : LinearTwoJet V₁ V₂)
    (P : LinearTwoJet V₀ V₁) :
    ((D.comp S).comp P).second =
      D.second.comp (S.base.comp P.base) +
      D.base.comp (S.second.comp P.base) +
      D.base.comp (S.base.comp P.second) +
      (2 : ℚ) • D.first.comp (S.first.comp P.base) +
      (2 : ℚ) • D.first.comp (S.base.comp P.first) +
      (2 : ℚ) • D.base.comp (S.first.comp P.first) := by
  simp [LinearTwoJet.comp, LinearMap.comp_assoc, LinearMap.add_comp,
    LinearMap.comp_add, LinearMap.smul_comp, LinearMap.comp_smul]
  module

/-- The exact second derivative of `Q₁(t) d Q₀(t)⁻¹` in typed primal-to-dual
coordinates. The quadratic inverse remainder remains explicit. -/
theorem movingDifferentialSecondJet
    {V₀ V₁ : Type*} [AddCommGroup V₀] [Module ℚ V₀]
    [AddCommGroup V₁] [Module ℚ V₁]
    (G₀ K₀ : V₀ →ₗ[ℚ] V₀) (G₁ K₁ : V₁ →ₗ[ℚ] V₁)
    (d : V₀ →ₗ[ℚ] V₁) :
    ((({ base := (LinearMap.id : V₁ →ₗ[ℚ] V₁), first := G₁, second := K₁ } :
        LinearTwoJet V₁ V₁).comp
      ({ base := d, first := (0 : V₀ →ₗ[ℚ] V₁), second := 0 } :
        LinearTwoJet V₀ V₁)).comp
      ({ base := (LinearMap.id : V₀ →ₗ[ℚ] V₀), first := -G₀,
         second := (2 : ℚ) • (G₀.comp G₀) - K₀ } : LinearTwoJet V₀ V₀)).second =
      K₁.comp d - (2 : ℚ) • ((G₁.comp d).comp G₀) +
        d.comp ((2 : ℚ) • (G₀.comp G₀) - K₀) := by
  simp [LinearTwoJet.comp, LinearMap.comp_assoc, sub_eq_add_neg]

/-- Single-parameter action-groupoid coefficient equation: when the mixed
background/parameter term `Dg[h]` is retained, the groupoid composition
coefficient gives `K = G² + Dg[h]`. This does not choose that derivative. -/
theorem actionGroupoid_secondJet_from_composition
    {n : ℕ} (G K Dg : SecondJetMatrix n)
    (hcomp : (2 : ℚ) • K = K + G * G + Dg) : K = G * G + Dg := by
  calc
    K = (2 : ℚ) • K - K := by module
    _ = (K + G * G + Dg) - K := by rw [hcomp]
    _ = G * G + Dg := by noncomm_ring

/-- Mixed action-groupoid composition coefficient. Comparing the two orders
of the same translation pair yields the background-derivative cancellation
of the tangent commutator. -/
theorem actionGroupoid_mixed_cocycle_from_composition
    {n : ℕ} (Dgζhξ Dgξhζ Gξ Gζ : SecondJetMatrix n)
    (hcoeff : Dgζhξ + Gζ * Gξ = Dgξhζ + Gξ * Gζ) :
    Dgζhξ - Dgξhζ + (Gζ * Gξ - Gξ * Gζ) = 0 := by
  calc
    Dgζhξ - Dgξhζ + (Gζ * Gξ - Gξ * Gζ) =
        (Dgζhξ + Gζ * Gξ) - (Dgξhζ + Gξ * Gζ) := by noncomm_ring
    _ = 0 := sub_eq_zero.mpr hcoeff

end D0.Geometry
