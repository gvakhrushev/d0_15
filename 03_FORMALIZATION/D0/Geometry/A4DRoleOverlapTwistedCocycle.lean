import Mathlib.Tactic
import D0.Geometry.A4DTransportedReferenceMismatch
import D0.Geometry.A4DReferenceJunctionCompressionBoundary

/-!
# Role-labelled overlap algebra and twisted cocycle

Lean-owns the algebraic relation between a **supplied** Role-labelled reference
section `q`, solder legs `v`, diagonal overlaps `δ`, and Role-labelled overlaps
`Ω` (PR #117 / synthesis frontier).

At one site / fibre:

\[
δ_r = q_r - v_r,
\qquad
Ω_{rs} = q_r - v_s.
\]

This module does **not** choose a physical diagonal law `δ(A,e,n)`, does not
impose the ordinary cocycle as a physical law, and does not start finite E
dressing. The off-diagonal solder-difference algebra determines `Ω` once the
diagonal `δ` and the solder legs `v` are given; the repo does not select that
diagonal here.
-/

namespace D0.Geometry

open D0
open AffineCartanMap

/-- Local `LinearOrder Role` for this module only; uniquely named to avoid
collision with `referenceJunctionRoleLinearOrder`,
`transportedRefMismatchRoleLinearOrder`, `nilpotentAffineRoleLinearOrder`. -/
local instance roleOverlapTwistedCocycleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' Role.toFin Role.toFin_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {V : Type*} [AddCommGroup V]

/-! ## Mandatory definitions (one site / fibre) -/

/-- Diagonal overlap `δ_r = q_r - v_r`. -/
def diagonalOverlap (q v : Role → V) (r : Role) : V :=
  q r - v r

/-- Role-labelled overlap `Ω_rs = q_r - v_s`. -/
def roleOverlap (q v : Role → V) (r s : Role) : V :=
  q r - v s

/-! ## 1. Overlap decomposition -/

/-- `Ω_rs = v_r - v_s + δ_r`. -/
theorem roleOverlap_eq_solderDiff_add_diagonal
    (q v : Role → V) (r s : Role) :
    roleOverlap q v r s = v r - v s + diagonalOverlap q v r := by
  simp only [roleOverlap, diagonalOverlap]
  abel

/-- Alias matching the brief name `overlap_decomposition`. -/
theorem overlap_decomposition (q v : Role → V) (r s : Role) :
    roleOverlap q v r s = v r - v s + diagonalOverlap q v r :=
  roleOverlap_eq_solderDiff_add_diagonal q v r s

/-! ## 2. Solder-difference compatibility -/

/-- `Ω_rs - Ω_rt = v_t - v_s`. -/
theorem roleOverlap_solderDiff_compatibility
    (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s - roleOverlap q v r t = v t - v s := by
  simp only [roleOverlap]
  abel

/-- Alias matching the brief name `solder_difference_compatibility`. -/
theorem solder_difference_compatibility (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s - roleOverlap q v r t = v t - v s :=
  roleOverlap_solderDiff_compatibility q v r s t

/-! ## 3. Twisted Role cocycle -/

/-- Exact twisted Role cocycle: `Ω_rs + Ω_st = Ω_rt + Ω_ss`. -/
theorem roleOverlap_twisted_cocycle
    (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s + roleOverlap q v s t =
      roleOverlap q v r t + roleOverlap q v s s := by
  simp only [roleOverlap]
  abel

/-- Alias matching the brief name `twisted_role_cocycle`. -/
theorem twisted_role_cocycle (q v : Role → V) (r s t : Role) :
    roleOverlap q v r s + roleOverlap q v s t =
      roleOverlap q v r t + roleOverlap q v s s :=
  roleOverlap_twisted_cocycle q v r s t

/-! ## 4. Diagonal identity -/

/-- `Ω_rr = δ_r`. -/
theorem roleOverlap_diagonal (q v : Role → V) (r : Role) :
    roleOverlap q v r r = diagonalOverlap q v r := by
  rfl

/-- Alias matching the brief name `diagonal_identity`. -/
theorem diagonal_identity (q v : Role → V) (r : Role) :
    roleOverlap q v r r = diagonalOverlap q v r :=
  roleOverlap_diagonal q v r

/-! ## 5. Strict-cocycle obstruction -/

/-- If the ordinary cocycle `Ω_rs + Ω_st = Ω_rt` holds for **all** labels, then
for every fixed `s` one has `δ_s = 0` (hence `q_s = v_s`). Ordinary cocycle is
too strong for generic nonzero diagonal overlap. -/
theorem ordinary_cocycle_forces_diagonal_zero
    (q v : Role → V)
    (h : ∀ r s t : Role,
      roleOverlap q v r s + roleOverlap q v s t = roleOverlap q v r t)
    (s : Role) :
    diagonalOverlap q v s = 0 := by
  -- Ordinary cocycle at (s,s,s): Ω_ss + Ω_ss = Ω_ss ⇒ Ω_ss = 0.
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

/-- Packaged obstruction: ordinary cocycle implies `δ_s = 0` and `q_s = v_s`
for every `s`. -/
theorem strict_cocycle_obstruction
    (q v : Role → V)
    (h : ∀ r s t : Role,
      roleOverlap q v r s + roleOverlap q v s t = roleOverlap q v r t) :
    (∀ s : Role, diagonalOverlap q v s = 0) ∧
      (∀ s : Role, q s = v s) :=
  ⟨fun s => ordinary_cocycle_forces_diagonal_zero q v h s,
    fun s => ordinary_cocycle_forces_reference_eq_solder q v h s⟩

/-! ## 6. Reference reconstruction -/

/-- For any `s`: `q_r = v_s + Ω_rs`. -/
theorem reference_reconstruction
    (q v : Role → V) (r s : Role) :
    q r = v s + roleOverlap q v r s := by
  simp only [roleOverlap]
  abel

/-- Reconstructed value is independent of the auxiliary label `s`, via
solder-difference compatibility. -/
theorem reference_reconstruction_independent_of_s
    (q v : Role → V) (r s t : Role) :
    v s + roleOverlap q v r s = v t + roleOverlap q v r t := by
  simp only [roleOverlap]
  abel

/-! ## 8. Minimum primitive: overlap determined by diagonal and solder difference -/

/-- Once the off-diagonal solder-difference law is fixed, the overlap field
is recovered from its diagonal `δ` and the solder legs `v`:
`Ω_rs = (v_r - v_s) + δ_r`. This does **not** claim the repo selects `δ`. -/
theorem roleOverlap_determined_by_diagonal
    (q v : Role → V) (r s : Role) :
    roleOverlap q v r s =
      (v r - v s) + diagonalOverlap q v r :=
  roleOverlap_eq_solderDiff_add_diagonal q v r s

/-- Two overlap fields with the same diagonal (same solder legs) agree. -/
theorem roleOverlap_eq_of_same_diagonal
    (q q' v : Role → V)
    (hδ : ∀ r : Role, diagonalOverlap q v r = diagonalOverlap q' v r)
    (r s : Role) :
    roleOverlap q v r s = roleOverlap q' v r s := by
  rw [roleOverlap_eq_solderDiff_add_diagonal, roleOverlap_eq_solderDiff_add_diagonal,
    hδ]

/-- Reconstruction map `δ ↦ Ω` for fixed solder legs `v`:
`Ω_rs = (v_r - v_s) + δ_r`. -/
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

/-- Equivalence statement: `roleOverlap q v` equals the unique solder-compatible
extension of its diagonal via `overlapFromDiagonal`. -/
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

/-! ## 7. Mismatch in diagonal variables (archive specialization) -/

variable {N : ℕ}

/-- Site-wise solder leg map at a fixed archive site. -/
def solderLegAt (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    Role → RoleSpace :=
  fun s => solderLegVector N e x s

/-- Archive diagonal overlap at site `y`: `δ_r(y) = q(y,r) - v_r(e,y)`. -/
def archiveDiagonalOverlap
    (N : ℕ) (e : LocalCoframeField N) (q : ReferenceLegField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  diagonalOverlap (q y) (solderLegAt N e y) r

/-- Archive Role-labelled overlap at site `y`: `Ω_rs(y) = q(y,r) - v_s(e,y)`. -/
def archiveRoleOverlap
    (N : ℕ) (e : LocalCoframeField N) (q : ReferenceLegField N)
    (y : ArchiveRolePhaseGroup N) (r s : Role) : RoleSpace :=
  roleOverlap (q y) (solderLegAt N e y) r s

/-- Conditional mismatch in diagonal variables: for `y = x + r`,
`κ_q(A,e;x,r) = A_{x,r}(v_r(e,y)) - v_r(e,x) + L_{x,r} δ_r(y)`.

Uses affine linearity `A(v+δ) = A(v) + L δ`. -/
theorem transportedReferenceMismatch_diagonal_form
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    let y := roleTranslatePlus N r x
    transportedReferenceMismatch A e q x r =
      AffineCartanMap.apply (A x r) (solderLegVector N e y r)
        - solderLegVector N e x r
        + (A x r).lin (diagonalOverlap (q y) (fun s => solderLegVector N e y s) r) := by
  intro y
  -- Unfold κ and the diagonal; expand affine apply on both sides.
  simp only [transportedReferenceMismatch, AffineCartanMap.apply, diagonalOverlap,
    map_sub]
  abel

/-- Alias matching the brief naming for theorem 7. -/
theorem mismatch_in_diagonal_variables
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (q : ReferenceLegField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    let y := roleTranslatePlus N r x
    transportedReferenceMismatch A e q x r =
      AffineCartanMap.apply (A x r) (solderLegVector N e y r)
        - solderLegVector N e x r
        + (A x r).lin (diagonalOverlap (q y) (fun s => solderLegVector N e y s) r) :=
  transportedReferenceMismatch_diagonal_form A e q x r

/-! ## Optional: transported junction variable (link to PR #118) -/

/-- Transported junction variable `J_rs = L Ω_rs` for a supplied linear map `L`. -/
def transportedJunctionVariable
    {K : Type*} [Field K] [Module K V]
    (L : V →ₗ[K] V) (q v : Role → V) (r s : Role) : V :=
  L (roleOverlap q v r s)

/-- Relates `J_rs` at a junction to the PR #118 defect term `L₁(q₁ - v₂)`. -/
theorem transportedJunctionVariable_eq_junction_defect
    {K : Type*} [Field K] [Module K V]
    (L : V →ₗ[K] V) (q v : Role → V) (r s : Role) :
    transportedJunctionVariable L q v r s = L (q r - v s) := by
  rfl

/-- Specialization: the junction-defect summand in `referenceJunction_eq` is
exactly `L₁ Ω` for `Ω = q₁ - v₂`. -/
theorem junction_defect_eq_transportedJunctionVariable
    {K : Type*} [Field K] [Module K V]
    (A1 : AffineCartanMap K V) (q1 v2 : V) :
    A1.lin (q1 - v2) =
      transportedJunctionVariable (A1.lin : V →ₗ[K] V)
        (fun _ : Role => q1) (fun _ : Role => v2) Role.A Role.A := by
  simp only [transportedJunctionVariable, roleOverlap]
  rfl

end

end D0.Geometry
