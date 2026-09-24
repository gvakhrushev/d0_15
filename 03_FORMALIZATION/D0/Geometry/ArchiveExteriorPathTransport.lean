import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.A4DObserverPositiveExterior
import D0.Geometry.A4DLocatedFrameCompatibilityBoundary
import D0.Geometry.ArchiveAffineExteriorLink

/-!
# Exterior path transport

`exteriorPathTransport` is the exterior lift of the owned PR #70 linear path
transport.  It is source/target typed by the path word, composes by
concatenation, and inverts under reversal.  It is not the missing constitutive
comparison `C_N`.  Research task `EXP-A4D-PATH-RESOLVED-MATTER-WORD-ACTION`
still owns that comparison.
-/

namespace D0.Geometry

open D0

noncomputable section

variable {N : ℕ}

def exteriorFrameEquiv (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ) :=
  LinearEquiv.ofLinear
    (archiveExteriorFrameLift L)
    (archiveExteriorFrameLift L.symm)
    (archiveExteriorFrameLift_inverse L).1
    (archiveExteriorFrameLift_inverse L).2

/-- Exterior transport of one owned path word.  Later steps act first, as in
`covariantLin`. -/
def exteriorPathTransport (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ) :=
  exteriorFrameEquiv (covariantLin A steps x)

theorem exteriorPathTransport_nil (A : AffineCartanConnection N ℝ RoleSpace)
    (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport A [] x = LinearEquiv.refl ℝ (ArchiveFockState → ℝ) := by
  apply LinearEquiv.toLinearMap_injective
  simp [exteriorPathTransport, exteriorFrameEquiv, covariantLin, archiveExteriorFrameLift_id]

theorem covariantLin_append (A : AffineCartanConnection N ℝ RoleSpace)
    (p q : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    covariantLin A (p ++ q) x =
      (covariantLin A q (pathEnd N p x)).trans (covariantLin A p x) := by
  rw [← affinePath_lin_eq_covariant, affinePath_append, AffineCartanMap.mul_lin,
    affinePath_lin_eq_covariant, affinePath_lin_eq_covariant]

theorem exteriorPathTransport_append (A : AffineCartanConnection N ℝ RoleSpace)
    (p q : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport A (p ++ q) x =
      (exteriorPathTransport A q (pathEnd N p x)).trans (exteriorPathTransport A p x) := by
  ext ψ s
  simp only [exteriorPathTransport, exteriorFrameEquiv, LinearEquiv.ofLinear_apply,
    LinearEquiv.trans_apply, covariantLin_append, LinearMap.comp_apply]
  exact congrFun ((LinearMap.congr_fun
    (archiveExteriorFrameLift_comp (covariantLin A p x)
      (covariantLin A q (pathEnd N p x))) ψ).symm) s

theorem covariantLin_reverse (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    covariantLin A ((steps.map reverseStep).reverse) (pathEnd N steps x) =
      (covariantLin A steps x).symm := by
  rw [← affinePath_lin_eq_covariant, affinePath_reverse, AffineCartanMap.inv_lin,
    affinePath_lin_eq_covariant]

theorem exteriorPathTransport_reverse (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport A ((steps.map reverseStep).reverse) (pathEnd N steps x) =
      (exteriorPathTransport A steps x).symm := by
  apply LinearEquiv.toLinearMap_injective
  simp only [exteriorPathTransport, exteriorFrameEquiv, LinearEquiv.ofLinear_toLinearMap,
    covariantLin_reverse]
  rfl

/-- Exterior image of the owned based relative holonomy. -/
def exteriorRelativeHolonomy (A : AffineCartanConnection N ℝ RoleSpace)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ) :=
  exteriorFrameEquiv (affineBasedHolonomy A r s x).lin

theorem exteriorRelativeHolonomy_eq_paths (A : AffineCartanConnection N ℝ RoleSpace)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    exteriorRelativeHolonomy A r s x =
      (exteriorPathTransport A [ChainStep.fwd s, ChainStep.fwd r] x).symm.trans
        (exteriorPathTransport A [ChainStep.fwd r, ChainStep.fwd s] x) := by
  ext ψ t
  simp only [exteriorRelativeHolonomy, exteriorPathTransport, exteriorFrameEquiv,
    LinearEquiv.ofLinear_apply, LinearEquiv.ofLinear_symm_apply, LinearEquiv.trans_apply,
    affineBasedHolonomy_lin, affineSquareA, affineSquareB, affinePath_lin_eq_covariant,
    LinearMap.comp_apply]
  exact congrFun ((LinearMap.congr_fun
    (archiveExteriorFrameLift_comp (covariantLin A [ChainStep.fwd r, ChainStep.fwd s] x)
      ((covariantLin A [ChainStep.fwd s, ChainStep.fwd r] x).symm)) ψ).symm) t

theorem exteriorPathTransport_gauge (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport (affineGauge h A) steps x =
      (exteriorFrameEquiv (h (pathEnd N steps x)).lin).symm.trans
        ((exteriorPathTransport A steps x).trans (exteriorFrameEquiv (h x).lin)) := by
  ext ψ t
  have hlin := affinePath_gauge h A steps x
  have hlin' := congrArg AffineCartanMap.lin hlin
  simp only [AffineCartanMap.mul_lin, AffineCartanMap.inv_lin, affinePath_lin_eq_covariant] at hlin'
  simp only [exteriorPathTransport, exteriorFrameEquiv, LinearEquiv.ofLinear_apply,
    LinearEquiv.ofLinear_symm_apply, LinearEquiv.trans_apply, hlin']
  rw [← LinearEquiv.trans_assoc]
  have hinner := archiveExteriorFrameLift_comp (covariantLin A steps x)
    ((h (pathEnd N steps x)).lin.symm)
  have houter := archiveExteriorFrameLift_comp (h x).lin
    (((h (pathEnd N steps x)).lin.symm).trans (covariantLin A steps x))
  rw [← LinearMap.congr_fun houter, ← hinner]
  simp [LinearMap.comp_apply]

theorem exteriorPathTransport_observer (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) (n : RoleVector)
    (h : preservesObserverForm (covariantLin A steps x) n) (k : ℕ)
    (z w : ⋀[ℝ]^k RoleSpace) :
    observerExteriorPairing (covariantLin A steps x n) k
        (exteriorPower.map k (covariantLin A steps x).toLinearMap z)
        (exteriorPower.map k (covariantLin A steps x).toLinearMap w) =
      observerExteriorPairing n k z w :=
  observerExteriorPairing_congruence (covariantLin A steps x) n h k z w

/-- Common-fibre contragredient of the path transport.  The located anchors of
the two colors are not this common fibre: the naïve sitewise reading is false. -/
theorem exteriorPathTransport_contragredient (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) (k : ℕ)
    (α : ⋀[ℝ]^k (Module.Dual ℝ RoleSpace)) (z : ⋀[ℝ]^k RoleSpace) :
    exteriorPower.pairingDual ℝ RoleSpace k
        (exteriorPower.map k (covariantLin A steps x).symm.toLinearMap.dualMap α)
        (exteriorPower.map k (covariantLin A steps x).toLinearMap z) =
      exteriorPower.pairingDual ℝ RoleSpace k α z :=
  archiveExteriorPower_pairingDual_frame_natural k (covariantLin A steps x) α z

theorem exteriorPath_located_anchor_obstruction :
    (∀ Λ : ArchiveRolePhaseGroup 1 → Matrix Role Role ℝ,
      (∀ x, IsRoleLorentz (Λ x)) →
        ∀ r : Role, Λ 0 = Λ (dualCofaceDisplacement 1 r)) → False :=
  located_naive_twoColor_sameFrame_impossible

#print axioms archiveExteriorFrameLift_comp
#print axioms archiveExteriorFrameLift_inverse
#print axioms archiveExteriorFrameLift_creator_covariant
#print axioms archiveExteriorFrameLift_contraction_covariant
#print axioms observerMetric_positive
#print axioms observerExteriorPairing_congruence
#print axioms observer_creator_adjoint_covariant
#print axioms observer_contraction_adjoint_covariant
#print axioms preservesObserverForm_lorentz
#print axioms transportedSolderCenter_covariance
#print axioms archiveSolderedForwardDifferential_frame
#print axioms archiveAffineLinkedCreateDifferential_flat
#print axioms archiveAffineLinkedHodgeDirac_flat
#print axioms exteriorPathTransport_append
#print axioms exteriorRelativeHolonomy_eq_paths
#print axioms exteriorPath_located_anchor_obstruction
#print axioms pointwiseCoefficient_cannot_equal_neighborDerivative
#print axioms rawNyquist_is_not_centered_data

end

end D0.Geometry
