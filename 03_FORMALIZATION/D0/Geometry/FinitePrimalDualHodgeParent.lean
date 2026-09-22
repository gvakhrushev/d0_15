import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace D0.Geometry

noncomputable section

/-!
# Abstract finite primal/dual Hodge parent

Pure finite linear algebra for the relevant four graded slots of a mixed primal/dual
parent action.  The constitutive maps star0 and star1 are supplied data; this file does
not assert that D0 owns a physical star = S(e,n,Omega).

The auxiliary field chi is constrained by
  star0 chi = d_D (star1 (d_P psi)),
so no explicit inverse of star is introduced.
-/

abbrev FiniteRealCarrier (ι : Type*) := ι → ℝ

structure FinitePrimalDualHodgeData
    (P0 P1 D3 D4 : Type*)
    [Fintype P0] [Fintype P1] [Fintype D3] [Fintype D4] where
  dP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1
  dD : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4
  star0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4
  star1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3

structure FinitePrimalDualGenerators
    (P0 P1 D3 D4 : Type*)
    [Fintype P0] [Fintype P1] [Fintype D3] [Fintype D4] where
  GP0 : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0
  GP1 : FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier P1
  GD3 : FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D3
  GD4 : FiniteRealCarrier D4 →ₗ[ℝ] FiniteRealCarrier D4

variable {P0 P1 D3 D4 : Type*}
variable [Fintype P0] [Fintype P1] [Fintype D3] [Fintype D4]

/-- Infinitesimal constitutive covariance delta star = G_D star - star G_P. -/
def constitutiveVariation
    (GP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (GD : FiniteRealCarrier D4 →ₗ[ℝ] FiniteRealCarrier D4)
    (star : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4) :
    FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4 :=
  GD.comp star - star.comp GP

@[simp] theorem constitutiveVariation_apply
    (GP : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P0)
    (GD : FiniteRealCarrier D4 →ₗ[ℝ] FiniteRealCarrier D4)
    (star : FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (u : FiniteRealCarrier P0) :
    constitutiveVariation GP GD star u =
      GD (star u) - star (GP u) := by
  rfl

/-- Local parent constraint replacing an explicit inverse-Hodge codifferential. -/
def mixedCodifferentialConstraint
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (psi chi : FiniteRealCarrier P0) :
    FiniteRealCarrier D4 :=
  A.star0 chi - A.dD (A.star1 (A.dP psi))

/-- Mixed finite action.  The pairing is supplied explicitly and no inverse star occurs. -/
def mixedPrimalDualAction
    (pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (psi chi lambda : FiniteRealCarrier P0) : ℝ :=
  (1 / 2 : ℝ) * pairing chi (A.star0 chi) +
    pairing lambda (mixedCodifferentialConstraint A psi chi)

/-- First variation of the auxiliary constraint under field and constitutive variations. -/
def mixedConstraintVariation
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G : FinitePrimalDualGenerators P0 P1 D3 D4)
    (deltaStar0 :
      FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 :
      FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi : FiniteRealCarrier P0) :
    FiniteRealCarrier D4 :=
  (deltaStar0 chi + A.star0 (G.GP0 chi)) -
    A.dD
      (deltaStar1 (A.dP psi) +
        A.star1 (A.dP (G.GP0 psi)))

/-- Exact covariance of the inverse-free auxiliary constraint.

The two chain hypotheses are the pointwise forms of [d_P,G_P]=0 and [d_D,G_D]=0.
-/
theorem mixedConstraintVariation_covariant
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G : FinitePrimalDualGenerators P0 P1 D3 D4)
    (deltaStar0 :
      FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 :
      FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi : FiniteRealCarrier P0)
    (hP : ∀ u, A.dP (G.GP0 u) = G.GP1 (A.dP u))
    (hD : ∀ v, A.dD (G.GD3 v) = G.GD4 (A.dD v))
    (hstar0 :
      deltaStar0 = constitutiveVariation G.GP0 G.GD4 A.star0)
    (hstar1 :
      deltaStar1 = constitutiveVariation G.GP1 G.GD3 A.star1) :
    mixedConstraintVariation A G deltaStar0 deltaStar1 psi chi =
      G.GD4 (mixedCodifferentialConstraint A psi chi) := by
  rw [hstar0, hstar1]
  unfold mixedConstraintVariation mixedCodifferentialConstraint
  simp only [constitutiveVariation_apply]
  rw [hP psi]
  simp only [sub_add_cancel]
  rw [hD]
  exact (G.GD4.map_sub _ _).symm

/-- Infinitesimal Ward variation of the mixed action. -/
def mixedPrimalDualWardVariation
    (pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G : FinitePrimalDualGenerators P0 P1 D3 D4)
    (deltaStar0 :
      FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 :
      FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0) : ℝ :=
  (1 / 2 : ℝ) *
      (pairing (G.GP0 chi) (A.star0 chi) +
        pairing chi
          (deltaStar0 chi + A.star0 (G.GP0 chi))) +
    (pairing (G.GP0 lambda)
        (mixedCodifferentialConstraint A psi chi) +
      pairing lambda
        (mixedConstraintVariation A G deltaStar0 deltaStar1 psi chi))

/-- Exact finite Ward identity for the abstract mixed parent.

No constitutive law is selected here: star0/star1 and their variations are hypotheses/data.
-/
theorem mixedPrimalDualWard_invariant
    (pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ)
    (A : FinitePrimalDualHodgeData P0 P1 D3 D4)
    (G : FinitePrimalDualGenerators P0 P1 D3 D4)
    (deltaStar0 :
      FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (deltaStar1 :
      FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0)
    (hP : ∀ u, A.dP (G.GP0 u) = G.GP1 (A.dP u))
    (hD : ∀ v, A.dD (G.GD3 v) = G.GD4 (A.dD v))
    (hpair : ∀ p d,
      pairing (G.GP0 p) d + pairing p (G.GD4 d) = 0)
    (hstar0 :
      deltaStar0 = constitutiveVariation G.GP0 G.GD4 A.star0)
    (hstar1 :
      deltaStar1 = constitutiveVariation G.GP1 G.GD3 A.star1) :
    mixedPrimalDualWardVariation pairing A G deltaStar0 deltaStar1
      psi chi lambda = 0 := by
  have hchi :
      deltaStar0 chi + A.star0 (G.GP0 chi) =
        G.GD4 (A.star0 chi) := by
    rw [hstar0]
    simp
  have hconstraint :=
    mixedConstraintVariation_covariant A G deltaStar0 deltaStar1
      psi chi hP hD hstar0 hstar1
  unfold mixedPrimalDualWardVariation
  rw [hchi, hconstraint]
  have hk := hpair chi (A.star0 chi)
  have hl := hpair lambda (mixedCodifferentialConstraint A psi chi)
  linarith

end

end D0.Geometry
