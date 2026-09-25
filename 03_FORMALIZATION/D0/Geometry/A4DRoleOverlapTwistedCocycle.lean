import Mathlib.Tactic
import D0.Geometry.A4DTransportedReferenceMismatch
import D0.Geometry.A4DReferenceJunctionCompressionBoundary

namespace D0.Geometry

open D0
open AffineCartanMap

local instance roleOverlapTwistedCocycleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {V : Type*} [AddCommGroup V]

def diagonalOverlap (q v : Role → V) (r : Role) : V :=
  q r - v r

def roleOverlap (q v : Role → V) (r s : Role) : V :=
  q r - v s

theorem roleOverlap_eq_solderDiff_add_diagonal
    (q v : Role → V) (r s : Role) :
    roleOverlap q v r s = v r - v s + diagonalOverlap q v r := by
  simp only [roleOverlap, diagonalOverlap]
  abel

theorem overlap_decomposition (q v : Role → V) (r s : Role) :
    roleOverlap q v r s = v r - v s + diagonalOverlap q v r :=
  roleOverlap_eq_solderDiff_add_diagonal q v r s

theorem roleOverlap_solderDiff_compatibility
    (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s - roleOverlap q v r t = v t - v s := by
  simp only [roleOverlap]
  abel

theorem solder_difference_compatibility (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s - roleOverlap q v r t = v t - v s :=
  roleOverlap_solderDiff_compatibility q v r s t

theorem roleOverlap_twisted_cocycle
    (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s + roleOverlap q v s t =
      roleOverlap q v r t + roleOverlap q v s s := by
  simp only [roleOverlap]
  abel

theorem twisted_role_cocycle (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s + roleOverlap q v s t =
      roleOverlap q v r t + roleOverlap q v s s :=
  roleOverlap_twisted_cocycle q v r s t

theorem roleOverlap_diagonal (q v : Role → V) (r : Role) :
    roleOverlap q v r r = diagonalOverlap q v r := by
  rfl

theorem diagonal_identity (q v : Role → V) (r : Role) :
    roleOverlap q v r r = diagonalOverlap q v r :=
  roleOverlap_diagonal q v r

theorem ordinary_cocycle_forces_diagonal_zero
    (q v : Role → V)
    (h : ∀ r s t : Role,
      roleOverlap q v r s + roleOverlap q v s t = roleOverlap q v r t)
    (s : Role) :
    diagonalOverlap q v s = 0 := by
  have hord := h s s s
  have hΩ : roleOverlap q v s s = 0 := by
    have := congrArg (fun z => z - roleOverlap q v s s) hord
    simpa [add_sub_cancel_right] using this
  simpa [roleOverlap_diagonal] using hΩ

theorem ordinary_cocycle_forces_reference_eq_solder
    (q v : Role → V)
    (h : ∀ r s t : Role,
      roleOverlap q v r s + roleOverlap q v s t = roleOverlap q v r t)
    (s : Role) :
    q s = v s := by
  have hδ := ordinary_cocycle_forces_diagonal_zero q v h s
  simpa [diagonalOverlap, sub_eq_zero] using hδ

theorem strict_cocycle_obstruction
    (q v : Role → V)
    (h : ∀ r s t : Role,
      roleOverlap q v r s + roleOverlap q v s t = roleOverlap q v r t) :
    (∀ s : Role, diagonalOverlap q v s = 0) ∧
      (∀ s : Role, q s = v s) :=
  ⟨fun s => ordinary_cocycle_forces_diagonal_zero q v h s,
    fun s => ordinary_cocycle_forces_reference_eq_solder q v h s⟩

theorem reference_reconstruction
    (q v : Role → V) (r s : Role) :
    q r = v s + roleOverlap q v r s := by
  simp only [roleOverlap]
  abel

theorem reference_reconstruction_independent_of_s
    (q v : Role → V) (r s t : Role) :
    v s + roleOverlap q v r s = v t + roleOverlap q v r t := by
  simp only [roleOverlap]
  abel

theorem roleOverlap_determined_by_diagonal
    (q v : Role → V) (r s : Role) :
    roleOverlap q v r s =
      (v r - v s) + diagonalOverlap q v r :=
  roleOverlap_eq_solderDiff_add_diagonal q v r s

theorem roleOverlap_eq_of_same_diagonal
    (q q' v : Role → V)
    (hδ : ∀ r : Role, diagonalOverlap q v r = diagonalOverlap q' v r)
    (r s : Role) :
    roleOverlap q v r s = roleOverlap q' v r s := by
  rw [roleOverlap_eq_solderDiff_add_diagonal, roleOverlap_eq_solderDiff_add_diagonal,
    hδ]

def overlapFromDiagonal (v : Role → V) (δ : Role → V) (r s : Role) : V :=
  (v r - v s) + δ r

theorem overlapFromDiagonal_diagonal (v δ : Role → V) (r : Role) :
    overlapFromDiagonal v δ r r = δ r := by
  simp only [overlapFromDiagonal]
  abel

theorem overlapFromDiagonal_solderDiff (v δ : Role → V) (r s t : Role) :
    overlapFromDiagonal v δ r s - overlapFromDiagonal v δ r t = v t - v s := by
  simp only [overlapFromDiagonal]
  abel

theorem overlapFromDiagonal_twisted_cocycle (v δ : Role → V) (r s t : Role) :
    overlapFromDiagonal v δ r s + overlapFromDiagonal v δ s t =
      overlapFromDiagonal v δ r t + overlapFromDiagonal v δ s s := by
  simp only [overlapFromDiagonal]
  abel

theorem roleOverlap_eq_overlapFromDiagonal
    (q v : Role → V) (r s : Role) :
    roleOverlap q v r s =
      overlapFromDiagonal v (diagonalOverlap q v) r s :=
  roleOverlap_eq_solderDiff_add_diagonal q v r s

theorem minimum_overlap_primitive
    (q v : Role → V) :
    (∀ r s : Role,
        roleOverlap q v r s =
          overlapFromDiagonal v (diagonalOverlap q v) r s) ∧
      (∀ r : Role,
        overlapFromDiagonal v (diagonalOverlap q v) r r =
          diagonalOverlap q v r) :=
  ⟨fun r s => roleOverlap_eq_overlapFromDiagonal q v r s,
    fun r => overlapFromDiagonal_diagonal v (diagonalOverlap q v) r⟩

variable {N : ℕ}

def solderLegAt (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    Role → RoleSpace :=
  fun s => solderLegVector N e x s

def archiveDiagonalOverlap
    (N : ℕ) (e : LocalCoframeField N) (q : ReferenceLegField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  diagonalOverlap (q y) (solderLegAt N e y) r

def archiveRoleOverlap
    (N : ℕ) (e : LocalCoframeField N) (q : ReferenceLegField N)
    (y : ArchiveRolePhaseGroup N) (r s : Role) : RoleSpace :=
  roleOverlap (q y) (solderLegAt N e y) r s

theorem transportedReferenceMismatch_diagonal_form
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    let y := roleTranslatePlus N r x
    transportedReferenceMismatch A e q x r =
      AffineCartanMap.apply (A x r) (solderLegVector N e y r)
        - solderLegVector N e x r
        + (A x r).lin (diagonalOverlap (q y) (fun s => solderLegVector N e y s) r) := by
  intro y
  simp only [transportedReferenceMismatch, AffineCartanMap.apply, diagonalOverlap,
    map_sub]
  abel

theorem mismatch_in_diagonal_variables
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    let y := roleTranslatePlus N r x
    transportedReferenceMismatch A e q x r =
      AffineCartanMap.apply (A x r) (solderLegVector N e y r)
        - solderLegVector N e x r
        + (A x r).lin (diagonalOverlap (q y) (fun s => solderLegVector N e y s) r) :=
  transportedReferenceMismatch_diagonal_form A e q x r

def transportedJunctionVariable
    {K : Type*} [Field K] [Module K V]
    (L : V →ₗ[K] V) (q v : Role → V) (r s : Role) : V :=
  L (roleOverlap q v r s)

theorem transportedJunctionVariable_eq_junction_defect
    {K : Type*} [Field K] [Module K V]
    (L : V →ₗ[K] V) (q v : Role → V) (r s : Role) :
    transportedJunctionVariable L q v r s = L (q r - v s) := by
  rfl

theorem junction_defect_eq_transportedJunctionVariable
    {K : Type*} [Field K] [Module K V]
    (A1 : AffineCartanMap K V) (q1 v2 : V) :
    A1.lin (q1 - v2) =
      transportedJunctionVariable (A1.lin : V →ₗ[K] V)
        (fun _ : Role => q1) (fun _ : Role => v2) A A := by
  simp only [transportedJunctionVariable, roleOverlap]
  rfl

end

end D0.Geometry
