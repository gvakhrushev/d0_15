import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DNilpotentAffineMatterLift

/-!
# Conditional transported-reference mismatch κ_q

Lean-owns the PR #112 edge comparison for a **supplied** source-fibre reference
leg `q`. This module does **not** select an intrinsic `q_N(A,e)`.
The conditional owner is intentionally orthogonal to the research selection problem.

\[
κ_q(A,e;x,r)
=
\operatorname{AffineCartanMap.apply}(A_{x,r},\, q(x+r,r))
-
\operatorname{solderLegVector}(N,e,x,r).
\]

Flat / pure-shift / cancellation / nilpotent-response controls reuse the frozen
`AffineCartanMap` / `solderLegVector` / `nilpotentAffineTranslation` APIs.
-/

namespace D0.Geometry

open D0

/-- Local `LinearOrder Role` for this module only; uniquely named to avoid
collision with `nilpotentAffineRoleLinearOrder` from PR #113. -/
local instance transportedRefMismatchRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {N : ℕ}

/-- ReferenceLegField(N) = X_N → Role → V (= RoleSpace). -/
abbrev ReferenceLegField (N : ℕ) :=
  ArchiveRolePhaseGroup N → Role → RoleSpace

/-- Conditional transported-reference mismatch κ_q(A,e;x,r).
The source site `x+r` is kept literal via `roleTranslatePlus`. -/
def transportedReferenceMismatch
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  AffineCartanMap.apply (A x r) (q (roleTranslatePlus N r x) r)
  - solderLegVector N e x r

/-- Conditional nilpotent matter letter T_κ = nilpotentAffineTranslation(κ_q). -/
def transportedReferenceNilpotentLetter
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  nilpotentAffineTranslation (transportedReferenceMismatch A e q x r)

/-- Constant role-basis reference `q = e_r` (the brief's fixed reference). -/
def archiveRoleBasisReference (N : ℕ) : ReferenceLegField N :=
  fun _ r => archiveRoleBasis r

/-- Pure affine-shift connection: one-link maps with `lin = I` and constant shift `b`. -/
def pureShiftAffineConnection (N : ℕ) (b : RoleSpace) :
    AffineCartanConnection N ℝ RoleSpace :=
  fun _ _ =>
    { lin := LinearEquiv.refl ℝ RoleSpace
      shift := b }

/-! ## 1. Exact expansion -/

theorem transportedReferenceMismatch_eq
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch A e q x r =
      (A x r).shift + (A x r).lin (q (roleTranslatePlus N r x) r)
        - solderLegVector N e x r := by
  simp only [transportedReferenceMismatch, AffineCartanMap.apply]
  abel

/-! ## 2. Flat control -/

theorem transportedReferenceMismatch_flat
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch (flatAffineConnection N) (0 : LocalCoframeField N)
      (archiveRoleBasisReference N) x r = 0 := by
  simp only [transportedReferenceMismatch, archiveRoleBasisReference, flatAffineConnection,
    AffineCartanMap.apply, AffineCartanMap.one_lin, AffineCartanMap.one_shift,
    LinearEquiv.refl_apply, solderLegVector_zero, add_zero, sub_self]

/-! ## 3. Pure affine-shift control -/

theorem transportedReferenceMismatch_pureShift
    (b : RoleSpace) (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch (pureShiftAffineConnection N b)
      (0 : LocalCoframeField N) (archiveRoleBasisReference N) x r = b := by
  simp only [transportedReferenceMismatch, pureShiftAffineConnection,
    archiveRoleBasisReference, AffineCartanMap.apply, LinearEquiv.refl_apply,
    solderLegVector_zero]
  abel

theorem transportedReferenceMismatch_pureShift_witness
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch (pureShiftAffineConnection N nilpotentWitnessShift)
      (0 : LocalCoframeField N) (archiveRoleBasisReference N) x r =
      nilpotentWitnessShift :=
  transportedReferenceMismatch_pureShift nilpotentWitnessShift x r

theorem transportedReferenceMismatch_pureShift_witness_ne_zero
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch (pureShiftAffineConnection N nilpotentWitnessShift)
      (0 : LocalCoframeField N) (archiveRoleBasisReference N) x r ≠ 0 := by
  rw [transportedReferenceMismatch_pureShift_witness]
  exact nilpotentWitnessShift_ne_zero

/-! ## 4. Exact cancellation for trivial linear part -/

theorem transportedReferenceMismatch_cancel
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role)
    (hlin : (A x r).lin = LinearEquiv.refl ℝ RoleSpace)
    (hq : q (roleTranslatePlus N r x) r =
      solderLegVector N e x r - (A x r).shift) :
    transportedReferenceMismatch A e q x r = 0 := by
  simp only [transportedReferenceMismatch, AffineCartanMap.apply, hlin,
    LinearEquiv.refl_apply, hq]
  abel

/-! ## 5. Nonzero fixed-reference under nonzero shift (firewall) -/

theorem transportedReferenceMismatch_fixedRef_shift_ne_zero
    (b : RoleSpace) (hb : b ≠ 0) (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch (pureShiftAffineConnection N b)
      (0 : LocalCoframeField N) (archiveRoleBasisReference N) x r ≠ 0 := by
  rw [transportedReferenceMismatch_pureShift]
  exact hb

/-! ## 6. Nilpotent letter controls (reuse PR #113; do not re-prove nilpotence) -/

theorem transportedReferenceNilpotentLetter_flat
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceNilpotentLetter (flatAffineConnection N)
      (0 : LocalCoframeField N) (archiveRoleBasisReference N) x r = LinearMap.id := by
  simp only [transportedReferenceNilpotentLetter, transportedReferenceMismatch_flat,
    nilpotentAffineTranslation_zero]

theorem transportedReferenceNilpotentLetter_cancel
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role)
    (hlin : (A x r).lin = LinearEquiv.refl ℝ RoleSpace)
    (hq : q (roleTranslatePlus N r x) r =
      solderLegVector N e x r - (A x r).shift) :
    transportedReferenceNilpotentLetter A e q x r = LinearMap.id := by
  simp only [transportedReferenceNilpotentLetter,
    transportedReferenceMismatch_cancel A e q x r hlin hq,
    nilpotentAffineTranslation_zero]

theorem transportedReferenceNilpotentLetter_pureShift
    (b : RoleSpace) (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceNilpotentLetter (pureShiftAffineConnection N b)
      (0 : LocalCoframeField N) (archiveRoleBasisReference N) x r =
      nilpotentAffineTranslation b := by
  simp only [transportedReferenceNilpotentLetter, transportedReferenceMismatch_pureShift]

theorem transportedReferenceNilpotentLetter_ne_id
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role)
    (hκ : transportedReferenceMismatch A e q x r ≠ 0) :
    transportedReferenceNilpotentLetter A e q x r ≠ LinearMap.id := by
  simpa only [transportedReferenceNilpotentLetter] using
    nilpotentAffineTranslation_ne_id _ hκ

/-! ## 7. Firewall: [I, T_κ] = 0 (no fake [H,T_b] mechanism) -/

theorem id_commute_transportedReferenceNilpotentLetter
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    LinearMap.id.comp (transportedReferenceNilpotentLetter A e q x r) -
      (transportedReferenceNilpotentLetter A e q x r).comp LinearMap.id = 0 := by
  simpa only [transportedReferenceNilpotentLetter] using
    id_commute_nilpotentAffineTranslation (transportedReferenceMismatch A e q x r)

end

end D0.Geometry
