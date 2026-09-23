import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.Tactic
import D0.Geometry.ArchiveMovingDifferential
import D0.Geometry.ArchivePrimalDualMovingAction
import D0.Geometry.FinitePrimalDualHodgeParent

/-!
# Exact finite and infinitesimal moving parent Ward

The mixed parent
`P⁰ → P¹ → D³ → D⁴`, with constraint `C = S₀ χ - d_D (S₁ (d_P ψ))`,
is invariant when primal equivalences move `d_P` and the pairing forces the dual
equivalences of `d_D`, `S₀`, and `S₁`.

The infinitesimal identity keeps every product-rule term in `δ(d_D S₁ d_P ψ)`.
Freezing `δd_P` and `δd_D` returns the previous chain-intertwining Ward.
A rational witness shows that freezing them is not automatic.

No inverse Hodge is used. Vanishing of this scalar Ward does not delete
independent connection or constitutive Euler terms, and it does not conclude
`∇ · T = 0`.
-/

namespace D0.Geometry

open D0

section FrozenWitness

def wardG0 : Matrix (Fin 3) (Fin 3) ℚ := !![0, 1, 0; 0, 0, 0; 0, 0, 0]

def wardG1 : Matrix (Fin 2) (Fin 2) ℚ := !![0, 1; 0, 0]

def wardDP : Matrix (Fin 2) (Fin 3) ℚ := !![1, 2, -1; 3, 0, 2]

def wardS0 : Matrix (Fin 3) (Fin 3) ℚ := !![2, 0, 0; 0, 3, 0; 0, 0, 5]

def wardS1 : Matrix (Fin 2) (Fin 2) ℚ := !![3, 0; 0, 7]

def wardH4 : Matrix (Fin 3) (Fin 3) ℚ := -wardG0.transpose

def wardH3 : Matrix (Fin 2) (Fin 2) ℚ := -wardG1.transpose

def wardDD : Matrix (Fin 3) (Fin 2) ℚ := wardDP.transpose

def wardDeltaDP : Matrix (Fin 2) (Fin 3) ℚ := wardG1 * wardDP - wardDP * wardG0

def wardDeltaDD : Matrix (Fin 3) (Fin 2) ℚ := wardH4 * wardDD - wardDD * wardH3

def wardDeltaS1 : Matrix (Fin 2) (Fin 2) ℚ := wardH3 * wardS1 - wardS1 * wardG1

def wardKinetic : Matrix (Fin 3) (Fin 3) ℚ := wardDD * wardS1 * wardDP

def wardSixTerm : Matrix (Fin 3) (Fin 3) ℚ :=
  wardDeltaDD * wardS1 * wardDP + wardDD * wardDeltaS1 * wardDP +
    wardDD * wardS1 * wardDeltaDP

def wardCovariantTarget : Matrix (Fin 3) (Fin 3) ℚ :=
  wardH4 * wardKinetic - wardKinetic * wardG0

def wardFrozenTerm : Matrix (Fin 3) (Fin 3) ℚ := wardDD * wardDeltaS1 * wardDP

/-- The six-term kinetic variation matches `H₄ K - K G₀`.
Dropping both differential variations does not. -/
theorem frozenDifferential_movingWard_fails :
    wardSixTerm = wardCovariantTarget ∧ wardFrozenTerm ≠ wardCovariantTarget := by
  native_decide

end FrozenWitness

noncomputable section

open Module

variable {P0 P1 D3 D4 : Type*}
variable [Fintype P0] [Fintype P1] [Fintype D3] [Fintype D4]
variable [DecidableEq P0] [DecidableEq P1] [DecidableEq D3] [DecidableEq D4]

/-- All six product-rule terms in `δ(S₀ χ - d_D S₁ d_P ψ)`. -/
def mixedMovingConstraintVariation
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (deltaDP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (deltaDD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi : FiniteRealCarrier P0) : FiniteRealCarrier D4 :=
  (deltaStar0 chi + A.star0 (G0 chi)) -
    (deltaDD (A.star1 (A.dP psi)) +
      A.dD (deltaStar1 (A.dP psi)) +
      A.dD (A.star1 (deltaDP psi)) +
      A.dD (A.star1 (A.dP (G0 psi))))

theorem mixedMovingConstraintVariation_covariant
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (G1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier P1)
    (H3 : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D3)
    (H4 : FiniteRealCarrier D4 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaDP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (deltaDD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi : FiniteRealCarrier P0)
    (hδP : deltaDP = movingDifferentialVariation G0 G1 A.dP)
    (hδD : deltaDD = movingDifferentialVariation H3 H4 A.dD)
    (hS0 : deltaStar0 = movingDifferentialVariation G0 H4 A.star0)
    (hS1 : deltaStar1 = movingDifferentialVariation G1 H3 A.star1) :
    mixedMovingConstraintVariation A G0 deltaDP deltaDD deltaStar0 deltaStar1 psi chi =
      H4 (mixedCodifferentialConstraint A psi chi) := by
  rw [hδP, hδD, hS0, hS1]
  unfold mixedMovingConstraintVariation mixedCodifferentialConstraint
  simp only [movingDifferentialVariation_apply, map_sub]
  abel

/-- Scalar variation of the inverse-free mixed action, with field and operator variations. -/
def mixedMovingPrimalDualWardVariation
    (pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (deltaDP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (deltaDD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0) : ℝ :=
  (1 / 2 : ℝ) *
      (pairing (G0 chi) (A.star0 chi) +
        pairing chi (deltaStar0 chi + A.star0 (G0 chi))) +
    (pairing (G0 lambda) (mixedCodifferentialConstraint A psi chi) +
      pairing lambda
        (mixedMovingConstraintVariation A G0 deltaDP deltaDD deltaStar0 deltaStar1 psi chi))

theorem mixedMovingPrimalDualWard_invariant
    (pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (G1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier P1)
    (H3 : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D3)
    (H4 : FiniteRealCarrier D4 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaDP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (deltaDD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0)
    (hpair : ∀ p d, pairing (G0 p) d + pairing p (H4 d) = 0)
    (hδP : deltaDP = movingDifferentialVariation G0 G1 A.dP)
    (hδD : deltaDD = movingDifferentialVariation H3 H4 A.dD)
    (hS0 : deltaStar0 = movingDifferentialVariation G0 H4 A.star0)
    (hS1 : deltaStar1 = movingDifferentialVariation G1 H3 A.star1) :
    mixedMovingPrimalDualWardVariation pairing A G0 deltaDP deltaDD deltaStar0 deltaStar1
      psi chi lambda = 0 := by
  have hchi : deltaStar0 chi + A.star0 (G0 chi) = H4 (A.star0 chi) := by
    rw [hS0]
    simp [movingDifferentialVariation_apply]
  have hC := mixedMovingConstraintVariation_covariant A G0 G1 H3 H4 deltaDP deltaDD
    deltaStar0 deltaStar1 psi chi hδP hδD hS0 hS1
  unfold mixedMovingPrimalDualWardVariation
  rw [hchi, hC]
  have hk := hpair chi (A.star0 chi)
  have hl := hpair lambda (mixedCodifferentialConstraint A psi chi)
  linarith

/-- Vanishing differential variations reduce the moving laws to the fixed-chain intertwiners. -/
theorem movingWard_specializes_fixedWard
    (pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (G1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier P1)
    (H3 : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D3)
    (H4 : FiniteRealCarrier D4 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaDP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (deltaDD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0)
    (hδP0 : deltaDP = 0)
    (hδD0 : deltaDD = 0)
    (hδP : deltaDP = movingDifferentialVariation G0 G1 A.dP)
    (hδD : deltaDD = movingDifferentialVariation H3 H4 A.dD)
    (hS0 : deltaStar0 = movingDifferentialVariation G0 H4 A.star0)
    (hS1 : deltaStar1 = movingDifferentialVariation G1 H3 A.star1)
    (hpair : ∀ p d, pairing (G0 p) d + pairing p (H4 d) = 0) :
    mixedPrimalDualWardVariation pairing A
      { GP0 := G0, GP1 := G1, GD3 := H3, GD4 := H4 }
      deltaStar0 deltaStar1 psi chi lambda = 0 := by
  have hinterP : ∀ u, A.dP (G0 u) = G1 (A.dP u) := by
    intro u
    have hzero := congrFun (congrArg DFunLike.coe (hδP.symm.trans hδP0)) u
    rw [movingDifferentialVariation_apply, LinearMap.zero_apply] at hzero
    exact (sub_eq_zero.mp hzero).symm
  have hinterD : ∀ v, A.dD (H3 v) = H4 (A.dD v) := by
    intro v
    have hzero := congrFun (congrArg DFunLike.coe (hδD.symm.trans hδD0)) v
    rw [movingDifferentialVariation_apply, LinearMap.zero_apply] at hzero
    exact (sub_eq_zero.mp hzero).symm
  apply mixedPrimalDualWard_invariant pairing A
    { GP0 := G0, GP1 := G1, GD3 := H3, GD4 := H4 }
    deltaStar0 deltaStar1 psi chi lambda
  · intro u
    simpa using hinterP u
  · intro v
    simpa using hinterD v
  · exact hpair
  · simpa [constitutiveVariation] using hS0
  · simpa [constitutiveVariation] using hS1

def movedPrimalDifferential
    (Q0 : FiniteRealCarrier P0 ≃ₗ[ℝ] FiniteRealCarrier P0)
    (Q1 : FiniteRealCarrier P1 ≃ₗ[ℝ] FiniteRealCarrier P1)
    (dP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1) :
    FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1 :=
  movingDifferential Q0 Q1 dP

def movedDualDifferential
    (R3 : FiniteRealCarrier D3 ≃ₗ[ℝ] FiniteRealCarrier D3)
    (R4 : FiniteRealCarrier D4 ≃ₗ[ℝ] FiniteRealCarrier D4)
    (dD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4) :
    FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4 :=
  movingDifferential R3 R4 dD

def movedStar
    {P D : Type*} [Fintype P] [Fintype D]
    (R : FiniteRealCarrier D ≃ₗ[ℝ] FiniteRealCarrier D)
    (Q : FiniteRealCarrier P ≃ₗ[ℝ] FiniteRealCarrier P)
    (S : FiniteRealCarrier P →ₗ[ℝ] FiniteRealCarrier D) :
    FiniteRealCarrier P →ₗ[ℝ] FiniteRealCarrier D :=
  movingHodge R S Q

theorem mixedConstraint_transform
    (e0 : FiniteRealCarrier P0 ≃ₗ[ℝ] Dual ℝ (FiniteRealCarrier D4))
    (e1 : FiniteRealCarrier P1 ≃ₗ[ℝ] Dual ℝ (FiniteRealCarrier D3))
    (Q0 : FiniteRealCarrier P0 ≃ₗ[ℝ] FiniteRealCarrier P0)
    (Q1 : FiniteRealCarrier P1 ≃ₗ[ℝ] FiniteRealCarrier P1)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (psi chi : FiniteRealCarrier P0) :
    let R4 := dualAction e0 Q0
    let R3 := dualAction e1 Q1
    let A' : FinitePrimalDualHodgeData P0 P1 D3 D4 :=
      { dP := movedPrimalDifferential Q0 Q1 A.dP
        dD := movedDualDifferential R3 R4 A.dD
        star0 := movedStar R4 Q0 A.star0
        star1 := movedStar R3 Q1 A.star1 }
    mixedCodifferentialConstraint A' (Q0 psi) (Q0 chi) =
      R4 (mixedCodifferentialConstraint A psi chi) := by
  intro R4 R3 A'
  simp [A', mixedCodifferentialConstraint, movedPrimalDifferential, movedDualDifferential,
    movedStar, movingDifferential, movingHodge]

theorem mixedAction_transform
    (e0 : FiniteRealCarrier P0 ≃ₗ[ℝ] Dual ℝ (FiniteRealCarrier D4))
    (e1 : FiniteRealCarrier P1 ≃ₗ[ℝ] Dual ℝ (FiniteRealCarrier D3))
    (Q0 : FiniteRealCarrier P0 ≃ₗ[ℝ] FiniteRealCarrier P0)
    (Q1 : FiniteRealCarrier P1 ≃ₗ[ℝ] FiniteRealCarrier P1)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (psi chi lambda : FiniteRealCarrier P0) :
    let R4 := dualAction e0 Q0
    let R3 := dualAction e1 Q1
    let A' : FinitePrimalDualHodgeData P0 P1 D3 D4 :=
      { dP := movedPrimalDifferential Q0 Q1 A.dP
        dD := movedDualDifferential R3 R4 A.dD
        star0 := movedStar R4 Q0 A.star0
        star1 := movedStar R3 Q1 A.star1 }
    let pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ :=
      fun p d => e0 p d
    mixedPrimalDualAction pairing A' (Q0 psi) (Q0 chi) (Q0 lambda) =
      mixedPrimalDualAction pairing A psi chi lambda := by
  intro R4 R3 A' pairing
  have hC := mixedConstraint_transform e0 e1 Q0 Q1 A psi chi
  have hstar : A'.star0 (Q0 chi) = R4 (A.star0 chi) := by
    simp [A', movedStar, movingHodge]
  have hpair_chi : e0 (Q0 chi) (A'.star0 (Q0 chi)) = e0 chi (A.star0 chi) := by
    rw [hstar]
    simpa using pairing_dualAction e0 Q0 chi (A.star0 chi)
  have hC' : mixedCodifferentialConstraint A' (Q0 psi) (Q0 chi) =
      R4 (mixedCodifferentialConstraint A psi chi) := by
    simpa [A', R3, R4] using hC
  have hpair_lam :
      e0 (Q0 lambda) (mixedCodifferentialConstraint A' (Q0 psi) (Q0 chi)) =
        e0 lambda (mixedCodifferentialConstraint A psi chi) := by
    rw [hC']
    simpa using pairing_dualAction e0 Q0 lambda (mixedCodifferentialConstraint A psi chi)
  simp only [mixedPrimalDualAction, pairing]
  rw [hpair_chi, hpair_lam]

/-- Conditional promotion. The four transformation identities are hypotheses about an
independently named background action and its symmetry. They are not fields of a
structure presented as physical geometry, and this theorem does not construct `S`. -/
theorem physicalMovingWard_of_constitutiveAction
    {Background : Type*}
    (geometryAction : Background → ℝ)
    (symmetry : Background → Background)
    (b : Background)
    (e0 : FiniteRealCarrier P0 ≃ₗ[ℝ] Dual ℝ (FiniteRealCarrier D4))
    (e1 : FiniteRealCarrier P1 ≃ₗ[ℝ] Dual ℝ (FiniteRealCarrier D3))
    (Q0 : FiniteRealCarrier P0 ≃ₗ[ℝ] FiniteRealCarrier P0)
    (Q1 : FiniteRealCarrier P1 ≃ₗ[ℝ] FiniteRealCarrier P1)
    (dPof : Background → FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (dDof : Background → FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (S0of : Background → FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (S1of : Background → FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0)
    (hDerived :
      geometryAction (symmetry b) = geometryAction b ∧
      dPof (symmetry b) = movedPrimalDifferential Q0 Q1 (dPof b) ∧
      dDof (symmetry b) =
        movedDualDifferential (dualAction e1 Q1) (dualAction e0 Q0) (dDof b) ∧
      S0of (symmetry b) = movedStar (dualAction e0 Q0) Q0 (S0of b) ∧
      S1of (symmetry b) = movedStar (dualAction e1 Q1) Q1 (S1of b)) :
    let pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ := fun p d => e0 p d
    let A : FinitePrimalDualHodgeData P0 P1 D3 D4 :=
      { dP := dPof b, dD := dDof b, star0 := S0of b, star1 := S1of b }
    let A' : FinitePrimalDualHodgeData P0 P1 D3 D4 :=
      { dP := dPof (symmetry b), dD := dDof (symmetry b),
        star0 := S0of (symmetry b), star1 := S1of (symmetry b) }
    mixedPrimalDualAction pairing A' (Q0 psi) (Q0 chi) (Q0 lambda) =
      mixedPrimalDualAction pairing A psi chi lambda := by
  intro pairing A A'
  rcases hDerived with ⟨_, hdP, hdD, hS0, hS1⟩
  have hdata : A' =
      { dP := movedPrimalDifferential Q0 Q1 A.dP
        dD := movedDualDifferential (dualAction e1 Q1) (dualAction e0 Q0) A.dD
        star0 := movedStar (dualAction e0 Q0) Q0 A.star0
        star1 := movedStar (dualAction e1 Q1) Q1 A.star1 } := by
    simp [A, A', hdP, hdD, hS0, hS1]
  simpa [hdata, pairing] using
    mixedAction_transform e0 e1 Q0 Q1 A psi chi lambda

/-- A parent scalar identity that has already cancelled does not remove independent
connection or constitutive Euler terms. This is not a divergence theorem. -/
theorem movingWard_keeps_independentFieldEuler
    (parentScalar connectionEuler constitutiveEuler : ℝ)
    (hNoether : parentScalar + connectionEuler + constitutiveEuler = 0)
    (hParent : parentScalar = 0) :
    connectionEuler + constitutiveEuler = 0 := by
  linarith

end

end D0.Geometry
