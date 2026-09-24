import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.ArchiveHodgeCARDirac
import D0.Geometry.A4DRawSolderFrameAction
import D0.Geometry.A4DObserverPositiveExterior

/-!
# Exterior transport along affine Cartan pull links

Only the linear part of a pull link acts on the CAR fibre.  The affine shift
continues to act on the coframe through the existing affine connection API.
The finite covariant forward differential reduces exactly to the owned
`dForward` at the flat link.  No continuum connection limit is asserted.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

variable {N : ℕ}

abbrev ArchiveRoleLinearEquiv := RoleSpace ≃ₗ[ℝ] RoleSpace

/-- The admissible Lorentz subclass of affine pull links.  The translation
component is intentionally absent: only the linear part acts on CAR fibres. -/
def IsLorentzAffineExteriorConnection
    (A : AffineCartanConnection N ℝ RoleSpace) : Prop :=
  ∀ x r, IsRoleLorentz
    (LinearMap.toMatrix archiveRoleBasis archiveRoleBasis (A x r).lin.toLinearMap)

theorem flatAffineExteriorConnection_isLorentz :
    IsLorentzAffineExteriorConnection (flatAffineConnection N) := by
  intro x r
  simp [flatAffineConnection, IsRoleLorentz]

/-- A PR #70 affine connection together with the pointwise Lorentz condition
on its linear pull links.  Affine translations remain unconstrained because
they act on the coframe channel, not on the CAR fibre. -/
def LorentzAffineExteriorConnection (N : ℕ) :=
  {A : AffineCartanConnection N ℝ RoleSpace // IsLorentzAffineExteriorConnection A}

/-- Exterior action of the linear part of a stored affine pull link. -/
def archiveAffineExteriorLink (A : AffineCartanConnection N ℝ RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveExteriorFrameLift (A x r).lin

/-- The fibre lift restricted to the accepted Lorentz subclass. -/
def archiveLorentzAffineExteriorLink (A : LorentzAffineExteriorConnection N)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveAffineExteriorLink A.1 x r

/-- The link intertwines creation with the same CAR fibre at its two ends.
The moving vector is the linear transport of the source vector. -/
theorem archiveAffineExteriorLink_creator_intertwine
    (A : AffineCartanConnection N ℝ RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role)
    (v : RoleSpace) (ψ : ArchiveFockState → ℝ) :
    archiveAffineExteriorLink A x r (archiveExteriorCreator v ψ) =
      archiveExteriorCreator ((A x r).lin v)
        (archiveAffineExteriorLink A x r ψ) :=
  archiveExteriorFrameLift_creator_covariant (A x r).lin v ψ

/-- The affine link also preserves the perfect pairing between the dual and
vector exterior fibres when covectors use the contragredient link.  This is
the dual-pairing expression of contraction transport. -/
theorem archiveAffineExteriorLink_dualPairing_intertwine
    (A : AffineCartanConnection N ℝ RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) (k : ℕ)
    (α : ⋀[ℝ]^k (Module.Dual ℝ RoleSpace))
    (z : ⋀[ℝ]^k RoleSpace) :
    exteriorPower.pairingDual ℝ RoleSpace k
      (exteriorPower.map k ((A x r).lin.symm.toLinearMap.dualMap) α)
      (exteriorPower.map k (A x r).lin.toLinearMap z) =
    exteriorPower.pairingDual ℝ RoleSpace k α z :=
  archiveExteriorPower_pairingDual_frame_natural k (A x r).lin α z

theorem archiveAffineExteriorLink_shift_irrelevant
    (A B : AffineCartanConnection N ℝ RoleSpace)
    (h : ∀ x r, (A x r).lin = (B x r).lin) (x : ArchiveRolePhaseGroup N)
    (r : Role) : archiveAffineExteriorLink A x r = archiveAffineExteriorLink B x r := by
  simp [archiveAffineExteriorLink, h x r]

/-- Gauge transformed exterior pull link is the node-frame intertwiner on the
two endpoint fibres. -/
theorem archiveAffineExteriorLink_gauge
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    archiveAffineExteriorLink (affineGauge h A) x r =
      (archiveExteriorFrameLift (h x).lin).comp
        ((archiveAffineExteriorLink A x r).comp
          (archiveExteriorFrameLift (h (roleTranslatePlus N r x)).lin.symm)) := by
  rw [archiveAffineExteriorLink, affineGauge_lin, archiveAffineExteriorLink]
  rw [archiveExteriorFrameLift_comp, archiveExteriorFrameLift_comp]
  congr 1

/-- Exterior-fibre pull of the next-site value along the stored linear link. -/
def archiveAffinePullFiber (A : AffineCartanConnection N ℝ RoleSpace)
    (r : Role) (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N) :
    ArchiveFockState → ℝ :=
  archiveAffineExteriorLink A x r
    (fun s => ψ (roleTranslatePlus N r x, s))

/-- Nodewise linear frame action on the existing site/Fock cochain carrier.
Affine translations do not act on the CAR fibre. -/
def archiveAffineCoChainGauge (h : AffineNodeGauge N ℝ RoleSpace)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => archiveExteriorFrameLift (h p.1).lin
    (fun s => ψ (p.1, s)) p.2

/-- Pulling the gauge-transformed endpoint section through the transformed
link is the same as transforming the original pulled section at the base site. -/
theorem archiveAffinePullFiber_gauge
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (ψ : ArchiveCochain N) (r : Role) (x : ArchiveRolePhaseGroup N) :
    archiveAffinePullFiber (affineGauge h A) r (archiveAffineCoChainGauge h ψ) x =
      archiveExteriorFrameLift (h x).lin (archiveAffinePullFiber A r ψ x) := by
  unfold archiveAffinePullFiber archiveAffineCoChainGauge
  rw [archiveAffineExteriorLink_gauge]
  simp only [LinearMap.comp_apply]
  have hinv := (archiveExteriorFrameLift_inverse (h (roleTranslatePlus N r x)).lin).2
  have hcancel (v : ArchiveFockState → ℝ) :
      archiveExteriorFrameLift (h (roleTranslatePlus N r x)).lin.symm
          (archiveExteriorFrameLift (h (roleTranslatePlus N r x)).lin v) = v := by
    simpa only [LinearMap.comp_apply, LinearMap.id_apply] using
      congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) => T v) hinv
  rw [hcancel]

/-- Link-covariant forward site difference on the existing cochain carrier. -/
def archiveAffineForwardSite (A : AffineCartanConnection N ℝ RoleSpace)
    (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => forwardDifferenceScale N *
    (archiveAffinePullFiber A r ψ p.1 p.2 - ψ p)

/-- The finite pull-difference is gauge covariant on the site/Fock cochain
carrier. This theorem concerns the exterior-transported difference itself;
it does not assert covariance after applying a fixed CAR creator. -/
theorem archiveAffineForwardSite_gauge
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (ψ : ArchiveCochain N) (r : Role) :
    archiveAffineForwardSite (affineGauge h A) r (archiveAffineCoChainGauge h ψ) =
      archiveAffineCoChainGauge h (archiveAffineForwardSite A r ψ) := by
  funext p
  simp only [archiveAffineForwardSite, archiveAffineCoChainGauge,
    archiveAffinePullFiber_gauge]
  let L := archiveExteriorFrameLift (h p.1).lin
  let a : ArchiveFockState → ℝ := archiveAffinePullFiber A r ψ p.1
  let b : ArchiveFockState → ℝ := fun s => ψ (p.1, s)
  have hsub := L.map_sub a b
  have hsub_eval := congrArg (fun f : ArchiveFockState → ℝ => f p.2) hsub
  have hsub_eval' : L (a - b) p.2 = L a p.2 - L b p.2 := by
    change L (a - b) p.2 = L a p.2 - L b p.2 at hsub_eval
    exact hsub_eval
  have hpoint : (fun s => forwardDifferenceScale N * (a s - b s)) =
      forwardDifferenceScale N • (a - b) := by
    funext s
    simp [Pi.smul_apply]
  change forwardDifferenceScale N * (L a p.2 - L b p.2) =
    L (fun s => forwardDifferenceScale N * (a s - b s)) p.2
  rw [← hsub_eval', hpoint, L.map_smul]
  simp [Pi.smul_apply]

/-- Same-fibre fixed CAR creation followed by the affine transported forward
difference.  Full covariance of this fixed-creator composite is not asserted. -/
def archiveAffineForwardCreateDirection
    (A : AffineCartanConnection N ℝ RoleSpace) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ ket : ArchiveFockState,
    carCreate r p.2 ket *
      (forwardDifferenceScale N *
        (archiveAffinePullFiber A r ψ p.1 ket - ψ (p.1, ket)))

def archiveAffineLinkedCreateDifferential
    (A : AffineCartanConnection N ℝ RoleSpace) (ψ : ArchiveCochain N) :
    ArchiveCochain N :=
  fun p => ∑ r : Role, archiveAffineForwardCreateDirection A r ψ p

theorem archiveAffineForwardCreateDirection_flat (ψ : ArchiveCochain N)
    (r : Role) :
    archiveAffineForwardCreateDirection (flatAffineConnection N) r ψ =
      forwardCreateDirection N r ψ := by
  funext p
  simp [archiveAffineForwardCreateDirection, archiveAffinePullFiber,
    archiveAffineExteriorLink, flatAffineConnection,
    archiveExteriorFrameLift, archiveFockExteriorEquiv, forwardCreateDirection,
    forwardDifference, forwardDifferenceScale]

theorem archiveAffineLinkedCreateDifferential_flat (ψ : ArchiveCochain N) :
    archiveAffineLinkedCreateDifferential (flatAffineConnection N) ψ = dForward N ψ := by
  funext p
  simp [archiveAffineLinkedCreateDifferential, dForward,
    archiveAffineForwardCreateDirection_flat]

/-- The backward fibre value is pulled from the preceding node to the
current node using the inverse linear link. -/
def archiveAffinePullPreviousFiber (A : AffineCartanConnection N ℝ RoleSpace)
    (r : Role) (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N) :
    ArchiveFockState → ℝ :=
  archiveExteriorFrameLift (A (roleTranslateMinus N r x) r).lin.symm
    (fun s => ψ (roleTranslateMinus N r x, s))

def archiveAffineBackwardAnnihilateDirection
    (A : AffineCartanConnection N ℝ RoleSpace) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ ket : ArchiveFockState,
    carAnnihilate r p.2 ket *
      (forwardDifferenceScale N *
        (ψ (p.1, ket) - archiveAffinePullPreviousFiber A r ψ p.1 ket))

def archiveAffineLinkedHodgeCodifferential
    (A : AffineCartanConnection N ℝ RoleSpace) (ψ : ArchiveCochain N) :
    ArchiveCochain N :=
  fun p => ∑ r : Role, -archiveAffineBackwardAnnihilateDirection A r ψ p

def archiveAffineLinkedHodgeDirac
    (A : AffineCartanConnection N ℝ RoleSpace) (ψ : ArchiveCochain N) :
    ArchiveCochain N :=
  archiveAffineLinkedCreateDifferential A ψ +
    archiveAffineLinkedHodgeCodifferential A ψ

theorem archiveAffinePullPreviousFiber_flat (r : Role)
    (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N) :
    archiveAffinePullPreviousFiber (flatAffineConnection N) r ψ x =
      fun s => ψ (roleTranslateMinus N r x, s) := by
  simp [archiveAffinePullPreviousFiber, flatAffineConnection,
    archiveExteriorFrameLift_id]

theorem archiveAffineBackwardAnnihilateDirection_flat (ψ : ArchiveCochain N)
    (r : Role) :
    archiveAffineBackwardAnnihilateDirection (flatAffineConnection N) r ψ =
      backwardAnnihilateDirection N r ψ := by
  funext p
  simp [archiveAffineBackwardAnnihilateDirection,
    archiveAffinePullPreviousFiber_flat, backwardAnnihilateDirection_eq,
    backwardDifference]

theorem archiveAffineLinkedHodgeCodifferential_flat (ψ : ArchiveCochain N) :
    archiveAffineLinkedHodgeCodifferential (flatAffineConnection N) ψ =
      hodgeCodifferential N ψ := by
  funext p
  simp [archiveAffineLinkedHodgeCodifferential, hodgeCodifferential,
    archiveAffineBackwardAnnihilateDirection_flat]

/-- The corrected finite Hodge/CAR operator is exactly the flat limit of the
linked forward/backward construction.  This identity alone does not assert
rotating-frame covariance of the fixed creator and annihilator indices. -/
theorem archiveAffineLinkedHodgeDirac_flat (ψ : ArchiveCochain N) :
    archiveAffineLinkedHodgeDirac (flatAffineConnection N) ψ =
      hodgeCarDirac N ψ := by
  simp [archiveAffineLinkedHodgeDirac, hodgeCarDirac,
    archiveAffineLinkedCreateDifferential_flat,
    archiveAffineLinkedHodgeCodifferential_flat]

/-- Translation data remain visible in the existing coframe channel even
though they do not enter exterior CAR transport. -/
theorem affineTranslation_flat_coframe_unchanged (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    (affineGauge (translationGauge N xi) (flatAffineConnection N) x r).shift a =
      forwardGaugeCoframe N xi x r a :=
  affineTranslation_flat_eq_forwardGaugeCoframe xi x r a

/-- Parallel transport of a raw solder row along one link, with its ordinary
finite difference recorded separately from the link's square curvature. -/
def archiveAffineSolderParallelDefect
    (A : AffineCartanConnection N ℝ RoleSpace)
    (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N)
    (r a : Role) : ℝ :=
  (A x r).lin (fun b => e (roleTranslatePlus N r x) r b) a - e x r a

theorem archiveAffineSolderParallelDefect_flat
    (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N)
    (r a : Role) :
    archiveAffineSolderParallelDefect (flatAffineConnection N) e x r a =
      e (roleTranslatePlus N r x) r a - e x r a := by
  simp [archiveAffineSolderParallelDefect, flatAffineConnection]

theorem flatAffineExteriorConnection_curvature_zero (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    affineOpenCurvature (flatAffineConnection N) r s x = 0 := by
  simp [affineOpenCurvature, affineSquareA_eq, affineSquareB_eq,
    flatAffineConnection]

/-- Flat links can have a nonparallel raw solder field.  The existing L=2
Nyquist witness makes the distinction explicit on the A edge. -/
theorem flat_link_nonparallel_rawNyquist :
    archiveAffineSolderParallelDefect (flatAffineConnection 0)
      periodTwoNyquistCoframe 0 A A = 4 := by
  norm_num [archiveAffineSolderParallelDefect_flat,
    periodTwoNyquistCoframe, roleTranslatePlus, roleTranslate, roleStep,
    A, archiveFibers]
  rw [if_neg (by decide : (1 : ZMod (archiveFibers 0)) ≠ 0)]
  norm_num

/-- Internal leg `v_r(x) = η E_r(x)ᵀ` of the uncentered solder. -/
def solderLegVector (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  roleLorentzMetric.mulVec (fun a => rawSolderMatrix N e x r a)

theorem solderLegVector_zero (x : ArchiveRolePhaseGroup N) (r : Role) :
    solderLegVector N (0 : LocalCoframeField N) x r = archiveRoleBasis r := by
  ext a
  simp only [solderLegVector, rawSolderMatrix, Pi.zero_apply, add_zero, roleLorentzMetric,
    Matrix.mulVec_diagonal, Matrix.diagonal_apply, archiveRoleBasis, Pi.basisFun_apply,
    Pi.single_apply]
  by_cases h : a = r
  · subst h
    simp [roleLorentzSign_mul_self]
  · simp [h, Ne.symm h]

/-- Moving creator `C†(v_r(x))` on the pulled forward difference. -/
def archiveSolderedCreateDirection
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    archiveExteriorCreator (solderLegVector N e p.1 r)
      (fun s => forwardDifferenceScale N *
        (archiveAffinePullFiber A r ψ p.1 s - ψ (p.1, s))) p.2

def archiveSolderedForwardDifferential
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, archiveSolderedCreateDirection A e r ψ p

theorem archiveSolderedCreateDirection_flat (ψ : ArchiveCochain N) (r : Role) :
    archiveSolderedCreateDirection (flatAffineConnection N) (0 : LocalCoframeField N) r ψ =
      fun p => archiveExteriorCreator (archiveRoleBasis r)
        (fun s => forwardDifference N r (fun x => ψ (x, s)) p.1) p.2 := by
  funext p
  have hpull : archiveAffinePullFiber (flatAffineConnection N) r ψ p.1 =
      fun s => ψ (roleTranslatePlus N r p.1, s) := by
    simp [archiveAffinePullFiber, archiveAffineExteriorLink, flatAffineConnection,
      archiveExteriorFrameLift_id]
  simp [archiveSolderedCreateDirection, solderLegVector_zero, hpull, forwardDifference,
    forwardDifferenceScale]

theorem archiveSolderedForwardDifferential_flat (ψ : ArchiveCochain N) :
    archiveSolderedForwardDifferential (flatAffineConnection N) (0 : LocalCoframeField N) ψ =
      fun p => ∑ r : Role, archiveExteriorCreator (archiveRoleBasis r)
        (fun s => forwardDifference N r (fun x => ψ (x, s)) p.1) p.2 := by
  funext p
  simp [archiveSolderedForwardDifferential, archiveSolderedCreateDirection_flat, Finset.sum_apply]

theorem archiveAffineExteriorLink_parallel_leg
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r : Role) (ψ : ArchiveFockState → ℝ)
    (hpar : (A x r).lin (solderLegVector N e (roleTranslatePlus N r x) r) =
      solderLegVector N e x r) :
    archiveAffineExteriorLink A x r
        (archiveExteriorCreator (solderLegVector N e (roleTranslatePlus N r x) r) ψ) =
      archiveExteriorCreator (solderLegVector N e x r)
        (archiveAffineExteriorLink A x r ψ) := by
  rw [archiveAffineExteriorLink_creator_intertwine, hpar]

def archiveSolderedAnnihilateDirection
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (n : ArchiveRolePhaseGroup N → RoleVector) (r : Role)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    archiveExteriorContraction (observerFlat (n p.1) (solderLegVector N e p.1 r))
      (fun s => forwardDifferenceScale N *
        (ψ (p.1, s) - archiveAffinePullPreviousFiber A r ψ p.1 s)) p.2

def archiveSolderedCodifferential
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (n : ArchiveRolePhaseGroup N → RoleVector) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, -archiveSolderedAnnihilateDirection A e n r ψ p

def archiveSolderedDirac
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (n : ArchiveRolePhaseGroup N → RoleVector) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  archiveSolderedForwardDifferential A e ψ + archiveSolderedCodifferential A e n ψ

theorem archiveSolderedAnnihilateDirection_flat (ψ : ArchiveCochain N) (r : Role) :
    archiveSolderedAnnihilateDirection (flatAffineConnection N) (0 : LocalCoframeField N)
        (fun _ => restObserver) r ψ =
      fun p => archiveExteriorContraction (archiveRoleBasis.coord r)
        (fun s => backwardDifference N r (fun x => ψ (x, s)) p.1) p.2 := by
  funext p
  have hpull := archiveAffinePullPreviousFiber_flat r ψ p.1
  simp [archiveSolderedAnnihilateDirection, solderLegVector_zero, observerFlat_rest_basis,
    hpull, backwardDifference, forwardDifferenceScale]

theorem archiveSolderedCodifferential_flat (ψ : ArchiveCochain N) :
    archiveSolderedCodifferential (flatAffineConnection N) (0 : LocalCoframeField N)
        (fun _ => restObserver) ψ =
      fun p => ∑ r : Role, -archiveExteriorContraction (archiveRoleBasis.coord r)
        (fun s => backwardDifference N r (fun x => ψ (x, s)) p.1) p.2 := by
  funext p
  simp [archiveSolderedCodifferential, archiveSolderedAnnihilateDirection_flat, Finset.sum_apply]

theorem archiveSolderedDirac_flat (ψ : ArchiveCochain N) :
    archiveSolderedDirac (flatAffineConnection N) (0 : LocalCoframeField N)
        (fun _ => restObserver) ψ =
      archiveSolderedForwardDifferential (flatAffineConnection N) (0 : LocalCoframeField N) ψ +
        archiveSolderedCodifferential (flatAffineConnection N) (0 : LocalCoframeField N)
          (fun _ => restObserver) ψ := by
  simp [archiveSolderedDirac]

/-- The moving creator on a gauge-transformed leg and section is the node-frame
transport of the original directional creator. -/
theorem archiveSolderedCreateDirection_frame
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (e e' : LocalCoframeField N) (r : Role) (ψ : ArchiveCochain N)
    (hleg : ∀ x, solderLegVector N e' x r = (h x).lin (solderLegVector N e x r)) :
    archiveSolderedCreateDirection (affineGauge h A) e' r
        (archiveAffineCoChainGauge h ψ) =
      archiveAffineCoChainGauge h (archiveSolderedCreateDirection A e r ψ) := by
  funext p
  let L := (h p.1).lin
  let diff : ArchiveFockState → ℝ := fun s =>
    forwardDifferenceScale N *
      (archiveAffinePullFiber A r ψ p.1 s - ψ (p.1, s))
  have hdiff :
      (fun s => forwardDifferenceScale N *
        (archiveAffinePullFiber (affineGauge h A) r (archiveAffineCoChainGauge h ψ) p.1 s -
          archiveAffineCoChainGauge h ψ (p.1, s))) =
      archiveExteriorFrameLift L diff := by
    funext s
    have hpull := congrFun (archiveAffinePullFiber_gauge h A ψ r p.1) s
    have hsub := congrFun ((archiveExteriorFrameLift L).map_sub
      (archiveAffinePullFiber A r ψ p.1) (fun t => ψ (p.1, t))) s
    have hsm := congrFun ((archiveExteriorFrameLift L).map_smul
      (forwardDifferenceScale N)
      (archiveAffinePullFiber A r ψ p.1 - fun t => ψ (p.1, t))) s
    simp only [archiveAffineCoChainGauge, Pi.sub_apply, Pi.smul_apply] at hpull hsub hsm
    change forwardDifferenceScale N *
        (archiveAffinePullFiber (affineGauge h A) r (archiveAffineCoChainGauge h ψ) p.1 s -
          archiveExteriorFrameLift L (fun t => ψ (p.1, t)) s) =
      archiveExteriorFrameLift L diff s
    rw [hpull, ← hsub]
    have hscale :
        forwardDifferenceScale N *
            (archiveExteriorFrameLift L)
              (archiveAffinePullFiber A r ψ p.1 - fun t => ψ (p.1, t)) s =
          (archiveExteriorFrameLift L)
            (forwardDifferenceScale N •
              (archiveAffinePullFiber A r ψ p.1 - fun t => ψ (p.1, t))) s := by
      simpa [Pi.smul_apply] using hsm.symm
    rw [hscale]
    apply congrArg (fun f => (archiveExteriorFrameLift L) f s)
    funext t
    simp [diff, Pi.smul_apply, Pi.sub_apply]
  have hcreator := archiveExteriorFrameLift_creator_covariant L
    (solderLegVector N e p.1 r) diff
  calc
    archiveSolderedCreateDirection (affineGauge h A) e' r
        (archiveAffineCoChainGauge h ψ) p =
        archiveExteriorCreator (solderLegVector N e' p.1 r)
          (archiveExteriorFrameLift L diff) p.2 := by
            simp [archiveSolderedCreateDirection, hdiff]
    _ = archiveExteriorCreator (L (solderLegVector N e p.1 r))
          (archiveExteriorFrameLift L diff) p.2 := by rw [hleg]
    _ = archiveExteriorFrameLift L
          (archiveExteriorCreator (solderLegVector N e p.1 r) diff) p.2 := by
            rw [← hcreator]
    _ = archiveAffineCoChainGauge h (archiveSolderedCreateDirection A e r ψ) p := by
            simp [archiveAffineCoChainGauge, archiveSolderedCreateDirection, diff, L]

theorem archiveSolderedForwardDifferential_frame
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (e e' : LocalCoframeField N) (ψ : ArchiveCochain N)
    (hleg : ∀ r x, solderLegVector N e' x r = (h x).lin (solderLegVector N e x r)) :
    archiveSolderedForwardDifferential (affineGauge h A) e'
        (archiveAffineCoChainGauge h ψ) =
      archiveAffineCoChainGauge h (archiveSolderedForwardDifferential A e ψ) := by
  funext p
  let L := (h p.1).lin
  have hsum :
      (fun s => archiveSolderedForwardDifferential A e ψ (p.1, s)) =
        ∑ r : Role, fun s => archiveSolderedCreateDirection A e r ψ (p.1, s) := by
    funext s
    simp [archiveSolderedForwardDifferential, Finset.sum_apply]
  calc
    archiveSolderedForwardDifferential (affineGauge h A) e'
        (archiveAffineCoChainGauge h ψ) p =
        ∑ r : Role, archiveSolderedCreateDirection (affineGauge h A) e' r
          (archiveAffineCoChainGauge h ψ) p := by
            rfl
    _ = ∑ r : Role, archiveAffineCoChainGauge h
          (archiveSolderedCreateDirection A e r ψ) p := by
            refine Finset.sum_congr rfl ?_
            intro r _
            exact congrFun (archiveSolderedCreateDirection_frame h A e e' r ψ
              (fun x => hleg r x)) p
    _ = ∑ r : Role, archiveExteriorFrameLift L
          (fun s => archiveSolderedCreateDirection A e r ψ (p.1, s)) p.2 := by
            simp [archiveAffineCoChainGauge, L]
    _ = archiveExteriorFrameLift L
          (∑ r : Role, fun s => archiveSolderedCreateDirection A e r ψ (p.1, s)) p.2 := by
            rw [map_sum]
            rfl
    _ = archiveAffineCoChainGauge h (archiveSolderedForwardDifferential A e ψ) p := by
            simp [archiveAffineCoChainGauge, hsum, L]

end
end D0.Geometry
