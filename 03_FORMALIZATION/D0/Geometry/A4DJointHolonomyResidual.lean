import Mathlib.LinearAlgebra.Matrix.Adjugate
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# Joint two-holonomy translational residual

Owns the polynomial residual of merged #185 / #196:

`R_{2|1} = det(I-P₁) t₂ - (I-P₂) adj(I-P₁) t₁`.

Targets:

* inverse-free polynomial definition on an arbitrary commutative ring;
* full affine conjugation covariance `R' = g R` (Fin-4 rational control +
  structural `native_decide` package matching #185/#196);
* Lorentz quadratic invariance and reviewed reversal identities on that control;
* exact flat-holonomy vanishing;
* Cramer/Plücker-chart form of residual components;
* abstract linear-algebra theorem: if `J ∘ D = 0`, `rank D = 4`, `rank J = 12`
  in a 16-dimensional sector, then `ker J = range D`;
* a small typed rational nongauge residual witness.

Concrete sector/global ranks 12 / 192 from the #196 Python certificate are
**not** imported as Lean axioms. Instantiating the abstract completeness
theorem on the homogeneous `L=2` control remains an explicit blocker.

No global nonlinear quotient-completeness claim. No Einstein / torsion-free
interpretation. Zero `sorry`.
-/

namespace D0.Geometry

open Matrix

set_option linter.unusedSimpArgs false

variable {n : Type*} [Fintype n] [DecidableEq n]
variable {R : Type*} [CommRing R]

/-! ## Carrier and polynomial residual -/

/-- Based affine holonomy `(P, t)`. -/
structure AffineHolonomy (n R : Type*) where
  lin : Matrix n n R
  trans : n → R

namespace AffineHolonomy

/-- Conjugation by an invertible linear gauge `g` and node translation `c`.
Uses explicit left/right factors rather than `Invertible`, so Fin-4 controls
remain `native_decide`-friendly. -/
def conjugate (g gInv : Matrix n n R) (c : n → R)
    (H : AffineHolonomy n R) : AffineHolonomy n R where
  lin := g * H.lin * gInv
  trans := g *ᵥ H.trans + (1 - g * H.lin * gInv) *ᵥ c

/-- Affine inverse given an explicit linear inverse matrix. -/
def inverseWith (PInv : Matrix n n R) (H : AffineHolonomy n R) : AffineHolonomy n R where
  lin := PInv
  trans := -(PInv *ᵥ H.trans)

end AffineHolonomy

/-- Fixed-point numerator `q♯ = adj(I-P) t`. -/
def affineFixedPointNumerator (H : AffineHolonomy n R) : n → R :=
  (1 - H.lin).adjugate *ᵥ H.trans

/-- Polynomial joint residual `R_{2|1}` (no inverse / reference section). -/
def jointHolonomyResidual (H1 H2 : AffineHolonomy n R) : n → R :=
  (1 - H1.lin).det • H2.trans -
    (1 - H2.lin) *ᵥ affineFixedPointNumerator H1

/-- Lorentz quadratic readout `Rᵀ η R`. -/
def jointHolonomyLorentzQuadratic (η : Matrix n n R) (H1 H2 : AffineHolonomy n R) : R :=
  let r := jointHolonomyResidual H1 H2
  r ⬝ᵥ (η *ᵥ r)

/-! ## Flat holonomy vanishing (general) -/

theorem jointHolonomyResidual_flat [Nontrivial n] (t1 t2 : n → R) :
    jointHolonomyResidual (⟨(1 : Matrix n n R), t1⟩ : AffineHolonomy n R) ⟨1, t2⟩ = 0 := by
  unfold jointHolonomyResidual affineFixedPointNumerator
  simp [sub_self, det_zero, adjugate_zero]

/-! ## Cramer / Plücker chart -/

-- The componentwise Cramer identity
--   `R_j = det(M₁)·t₂ⱼ - rowⱼ(M₂) ⬝ cramer(M₁,t₁)`
-- is the affine chart of the two-loop Plücker minors. It is owned below on the
-- Fin-4 rational control by `native_decide`, matching the #196 certificate
-- `PLUCKER_CHART_COMPONENT_*` checks.

/-! ## Abstract sector completeness -/

variable {k : Type*} [Field k]

/-- If a residual map kills a gauge map and the ranks are complementary in a
16-dimensional sector, the kernel is exactly the gauge image. -/
theorem ker_eq_range_of_jointResidualRanks
    {V U W : Type*}
    [AddCommGroup V] [Module k V]
    [AddCommGroup U] [Module k U]
    [AddCommGroup W] [Module k W]
    [FiniteDimensional k V] [FiniteDimensional k U] [FiniteDimensional k W]
    (D : V →ₗ[k] U) (J : U →ₗ[k] W)
    (hcomp : ∀ v, J (D v) = 0)
    (hU : Module.finrank k U = 16)
    (hD : Module.finrank k (LinearMap.range D) = 4)
    (hJ : Module.finrank k (LinearMap.range J) = 12) :
    LinearMap.ker J = LinearMap.range D := by
  have hle : LinearMap.range D ≤ LinearMap.ker J := by
    intro x hx
    rcases hx with ⟨v, hv⟩
    change J x = 0
    rw [← hv]
    exact hcomp v
  have hker : Module.finrank k (LinearMap.ker J) = 4 := by
    have hr := LinearMap.finrank_range_add_finrank_ker J
    have : Module.finrank k (LinearMap.range J) + Module.finrank k (LinearMap.ker J) =
        Module.finrank k U := hr
    omega
  have hEq : LinearMap.range D = LinearMap.ker J :=
    Submodule.eq_of_le_of_finrank_eq hle (by simp [hD, hker])
  exact hEq.symm

/-! ## Fin-4 rational control (#185 / #196) -/

noncomputable section Control

def boost : Matrix (Fin 4) (Fin 4) ℚ :=
  !![5/3, 4/3, 0, 0; 4/3, 5/3, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1]

def boostInv : Matrix (Fin 4) (Fin 4) ℚ :=
  !![5/3, -4/3, 0, 0; -4/3, 5/3, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1]

def rCD : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1, 0, 0, 0; 0, 1, 0, 0; 0, 0, 0, 1; 0, 0, -1, 0]

def rBC : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1, 0, 0, 0; 0, 0, 1, 0; 0, -1, 0, 0; 0, 0, 0, 1]

def eta : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1, 0, 0, 0; 0, -1, 0, 0; 0, 0, -1, 0; 0, 0, 0, -1]

/-- Loxodromic #185 anchor `Boost * R_CD`. -/
def P1 : Matrix (Fin 4) (Fin 4) ℚ := boost * rCD

/-- Target `R_BC * Boost * R_BC⁻¹` with `R_BC⁻¹ = R_BCᵀ`. -/
def P2 : Matrix (Fin 4) (Fin 4) ℚ := rBC * boost * rBC.transpose

def P1Inv : Matrix (Fin 4) (Fin 4) ℚ := rCD.transpose * boostInv
def P2Inv : Matrix (Fin 4) (Fin 4) ℚ := rBC * boostInv * rBC.transpose

def t1 : Fin 4 → ℚ := ![1, 2, 0, -1]
def t2 : Fin 4 → ℚ := ![0, -1, 3, 2]

def H1 : AffineHolonomy (Fin 4) ℚ := ⟨P1, t1⟩
def H2 : AffineHolonomy (Fin 4) ℚ := ⟨P2, t2⟩

def gConj : Matrix (Fin 4) (Fin 4) ℚ := rBC * boost
def gConjInv : Matrix (Fin 4) (Fin 4) ℚ := boostInv * rBC.transpose
def cShift : Fin 4 → ℚ := ![1/2, -1, 2/3, 1]

/-! ### Flat vanishing on the control -/

theorem jointHolonomyResidual_flat_control :
    jointHolonomyResidual (n := Fin 4) (R := ℚ) ⟨1, t1⟩ ⟨1, t2⟩ = 0 := by
  native_decide

/-! ### Full affine conjugation covariance `R' = g R` -/

theorem jointHolonomyResidual_affineConjugation_control :
    jointHolonomyResidual
        (H1.conjugate gConj gConjInv cShift)
        (H2.conjugate gConj gConjInv cShift) =
      gConj *ᵥ jointHolonomyResidual H1 H2 := by
  native_decide

/-! ### Lorentz quadratic invariance under affine conjugation -/

theorem jointHolonomyLorentzQuadratic_affineConjugation_control :
    jointHolonomyLorentzQuadratic eta
        (H1.conjugate gConj gConjInv cShift)
        (H2.conjugate gConj gConjInv cShift) =
      jointHolonomyLorentzQuadratic eta H1 H2 := by
  native_decide

/-! ### Target-loop reversal identities -/

theorem jointHolonomyResidual_targetReversal_control :
    jointHolonomyResidual H1 (H2.inverseWith P2Inv) =
      -(P2Inv *ᵥ jointHolonomyResidual H1 H2) := by
  native_decide

theorem jointHolonomyLorentzQuadratic_targetReversal_control :
    jointHolonomyLorentzQuadratic eta H1 (H2.inverseWith P2Inv) =
      jointHolonomyLorentzQuadratic eta H1 H2 := by
  native_decide

/-! ### Anchor reversal of the fixed-point numerator -/

theorem affineFixedPointNumerator_anchorReversal_control :
    affineFixedPointNumerator (H1.inverseWith P1Inv) =
      affineFixedPointNumerator H1 := by
  native_decide

/-! ### Nongauge residual witness -/

theorem jointHolonomyResidual_nongaugeWitness_ne_zero :
    jointHolonomyResidual H1 H2 ≠ 0 := by
  native_decide

theorem jointHolonomyLorentzQuadratic_nongaugeWitness :
    jointHolonomyLorentzQuadratic eta H1 H2 ≠ 0 := by
  native_decide

/-! ### Cramer chart on the control -/


/-- Two-loop Plücker chart: residual components match the #196 minor identity
`det(C[0,1,2,3,4+j; :]) = R_j` on the rational control (via Cramer form). -/
theorem jointHolonomyResidual_pluckerCramerChart_control :
    let M1 := (1 : Matrix (Fin 4) (Fin 4) ℚ) - H1.lin
    let M2 := (1 : Matrix (Fin 4) (Fin 4) ℚ) - H2.lin
    let R := jointHolonomyResidual H1 H2
    (∀ j : Fin 4,
      R j = M1.det * H2.trans j - (M2 j) ⬝ᵥ (cramer M1 H1.trans)) := by
  native_decide


end Control

/-!
### Explicit blocker (not an axiom)

#196 certifies `rank J_χ = 12` and global rank `192` on declared generic
homogeneous `L=2` controls. Those ranks are not Lean axioms here. Concrete
instantiation of `ker_eq_range_of_jointResidualRanks` on that control remains
certified-only until a separate Lean rank proof lands.
-/

theorem jointHolonomyResidual_concreteRanks_certifiedOnly_blocker : True :=
  trivial

end D0.Geometry
