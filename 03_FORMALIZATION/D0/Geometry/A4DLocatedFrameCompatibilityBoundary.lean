import Mathlib.Tactic
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.LinearAlgebra.ExteriorPower.Basic
import D0.Geometry.A4DLocatedTopologicalStar
import D0.Geometry.A4DObserverPositiveExterior
import D0.Geometry.A4DMetricStarSignatureBoundary
import D0.Geometry.A4DPathCovariantHodge
import D0.Geometry.ArchiveAffineCartanConnection

/-!
# Common-fibre exterior evaluation and located-frame anchor boundary

The located `J` implementation is imported unchanged.  The result below only
records naturality on a common finite fibre and the distinct-anchor obstruction
for a sitewise frame field; it does not make `J` into a metric star.
-/

namespace D0.Geometry

open D0

noncomputable section

def archiveExteriorPowerFrameMap (k : ℕ) (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    ⋀[ℝ]^k RoleSpace →ₗ[ℝ] ⋀[ℝ]^k RoleSpace :=
  exteriorPower.map k L.toLinearMap

/-- Common-fibre exterior evaluation identity: the inverse exterior map cancels
the exterior map under evaluation.  This is not the complementary-minor Jacobi
identity for the located star. -/
theorem commonFiberExteriorEvaluation_inverse (k : ℕ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (α : Module.Dual ℝ (⋀[ℝ]^k RoleSpace)) (z : ⋀[ℝ]^k RoleSpace) :
    α (archiveExteriorPowerFrameMap k L
      (archiveExteriorPowerFrameMap k L.symm z)) = α z := by
  change α (((exteriorPower.map k L.toLinearMap).comp
      (exteriorPower.map k L.symm.toLinearMap)) z) = α z
  rw [← exteriorPower.map_comp (n := k) L.symm.toLinearMap L.toLinearMap]
  simp

/-- The nondegenerate common-fibre cofactor identity used at degree one.
This algebraic equality has no shift of the located dual anchor. -/
theorem locatedCommonFiber_cofactor_identity
    (L : Matrix (Fin 4) (Fin 4) ℝ) (hdet : L.det ≠ 0)
    (i j : Fin 4) :
    L.det * (L⁻¹) i j =
      (-1 : ℝ) ^ ((j : ℕ) + (i : ℕ)) *
        (L.submatrix j.succAbove i.succAbove).det :=
  commonFiber_four_cofactor_inverse L hdet i j

/-- The located placement's coface endpoint differs by two role steps. -/
theorem locatedFrame_coface_anchor_shift (N : ℕ)
    (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) (r : Role)
    (h : S r = false) :
    (locatedPrimalToDual (PrimalCell.mk (x + roleStep N r) (insertRole S r))).site =
      (locatedPrimalToDual (PrimalCell.mk x S)).site +
        dualCofaceDisplacement N r :=
  located_coface_corner N x S r h

/-- On the L=3 archive cycle (`N=1`), the two-step anchor shift is nonzero. -/
theorem locatedFrame_twoStep_nonzero (r : Role) :
    dualCofaceDisplacement 1 r ≠ 0 := by
  intro h
  have hc := congrFun h r
  have hne : (2 : ZMod 3) ≠ 0 := by decide
  apply hne
  simpa [dualCofaceDisplacement, roleStep] using hc

def shiftedAnchorFrameWitness (_r : Role) :
    ArchiveRolePhaseGroup 1 → Matrix Role Role ℝ := fun x =>
  if x = 0 then 1 else rationalABBoost

theorem shiftedAnchorFrameWitness_lorentz (r : Role)
    (x : ArchiveRolePhaseGroup 1) :
    IsRoleLorentz (shiftedAnchorFrameWitness r x) := by
  by_cases hx : x = 0
  · subst x
    simp [shiftedAnchorFrameWitness, IsRoleLorentz]
  · simp [shiftedAnchorFrameWitness, hx, rationalABBoost_lorentz]

theorem shiftedAnchorFrameWitness_distinguishes_anchors (r : Role) :
    shiftedAnchorFrameWitness r 0 ≠
      shiftedAnchorFrameWitness r (dualCofaceDisplacement 1 r) := by
  have hshift := locatedFrame_twoStep_nonzero r
  have hneq : dualCofaceDisplacement 1 r ≠ (0 : ArchiveRolePhaseGroup 1) := hshift
  intro h
  have hab := congrArg (fun M : Matrix Role Role ℝ => M A B) h
  have hab' : (0 : ℝ) = 4 / 3 := by
    simpa [shiftedAnchorFrameWitness, hneq, rationalABBoost, A, B] using hab
  norm_num at hab'

/-- No universal sitewise Lorentz frame can be read at both a located primal
anchor and its shifted dual coface anchor as if they were one site. -/
theorem located_naive_twoColor_sameFrame_impossible
    (h : ∀ Λ : ArchiveRolePhaseGroup 1 → Matrix Role Role ℝ,
      (∀ x, IsRoleLorentz (Λ x)) →
      ∀ r : Role, Λ 0 = Λ (dualCofaceDisplacement 1 r)) : False := by
  have heq := h (shiftedAnchorFrameWitness A)
    (shiftedAnchorFrameWitness_lorentz A) A
  exact shiftedAnchorFrameWitness_distinguishes_anchors A heq

/-- Common-fibre contragredient of a pull path.  For a push, the endpoints
swap.  This does not move the located anchors: those remain the obstruction
`located_naive_twoColor_sameFrame_impossible`. -/
theorem locatedPull_contragredient {N : ℕ}
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) (k : ℕ)
    (α : ⋀[ℝ]^k (Module.Dual ℝ RoleSpace)) (z : ⋀[ℝ]^k RoleSpace) :
    exteriorPower.pairingDual ℝ RoleSpace k
        (exteriorPower.map k (covariantLin A steps x).symm.toLinearMap.dualMap α)
        (exteriorPower.map k (covariantLin A steps x).toLinearMap z) =
      exteriorPower.pairingDual ℝ RoleSpace k α z :=
  archiveExteriorPower_pairingDual_frame_natural k (covariantLin A steps x) α z

/-- A sitewise coefficient readout of the centered solder metric cannot recover
the raw one-form tangent along the existing L=2 Nyquist family. This imports
the previously proved boundary verbatim; it does not identify the located
placement with a metric star. -/
theorem centeredPointwiseSolder_no_nyquist_recovery
    (K : (ArchiveRolePhaseGroup 0 → Matrix Role Role ℝ) →
      ArchiveRolePhaseGroup 0 → ℝ)
    (hK : ∀ t x,
      K (fun y => solderMetricMatrix 0 ((t : ℝ) • periodTwoNyquistCoframe) y) x =
        ((t : ℝ) • periodTwoNyquistCoframe) x A A) :
    False :=
  periodTwo_centeredMetric_blind_oneFormTangent K hK

end
end D0.Geometry
