import Mathlib.Tactic
import D0.Geometry.A4DConditionalSourcedDiagonalTransport
import D0.Geometry.A4DRoleOverlapTwistedCocycle

/-!
# Sourced mismatch factorization passport: κ = L(R + h)

Lean-owns the algebraic factorization isolated by research PR #128 / memo
`MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md` §6.1:

\[
\boxed{\kappa(x,r)=L_{x,r}\bigl(R_r(y)+h_r(y)\bigr)}
\]

under the sourced ansatz `δ = a + h`, assembling already-landed owners:

- `#125` `A4DConditionalSourcedDiagonalTransport`: `ρ = a − R`, seed `a`,
  relative defect `R`, parallel residual `h := δ − a`;
- `A4DRoleOverlapTwistedCocycle.transportedReferenceMismatch_diagonal_form`;
- Thin local wrappers (same formulas as `#127` `referenceFromSuppliedDiagonal` /
  `conditionalMismatchFromSuppliedDelta`) assemble κ from a supplied δ without
  importing the full active-span independence module.

## Index / pull-order conventions (memo §5–§6)

- **Predecessor site** `x`; **source site** `y = x + r` via `roleTranslatePlus`,
  equivalently `x = predecessorSite r y` (`roleTranslateMinus`).
- Predecessor bars in `#125` are `L_{x,r}^{-1}`-pulled to the source fibre.
- Path-source append/reverse (`S_{p++q}=S_p+P_p S_q`, …) remain `#125` owners;
  cited only as ambient pull-order context — not re-proved here.

## Firewalls

No new `J` selector; no E/F dressing; no `A=A(e)`; no stress/time/golden;
no classicality / continuum / GR/QFT claims; no transported-mean selector (6.2).
-/

namespace D0.Geometry

open D0
open AffineCartanMap

local instance sourcedMismatchFactorRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {N : ℕ}

/-! ## Index round-trip: predecessor ↔ source -/

/-- Source site from predecessor: `y = x + r`. -/
abbrev sourceSiteFromPredecessor (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :
    ArchiveRolePhaseGroup N :=
  roleTranslatePlus N r x

/-- Predecessor of a source site recovers `x` after a forward Role step. -/
theorem predecessorSite_sourceSiteFromPredecessor
    (r : Role) (x : ArchiveRolePhaseGroup N) :
    predecessorSite N r (sourceSiteFromPredecessor N r x) = x := by
  simp only [predecessorSite, sourceSiteFromPredecessor, roleTranslateMinus_apply,
    roleTranslatePlus_apply, add_sub_cancel]

/-- Forward Role step after predecessor recovers the source site. -/
theorem sourceSiteFromPredecessor_predecessorSite
    (r : Role) (y : ArchiveRolePhaseGroup N) :
    sourceSiteFromPredecessor N r (predecessorSite N r y) = y := by
  simp only [predecessorSite, sourceSiteFromPredecessor, roleTranslatePlus_apply,
    roleTranslateMinus_apply, sub_add_cancel]

/-! ## Thin supplied-δ κ wrappers (same formulas as #127; not re-proving independence) -/

/-- Build a `ReferenceLegField` from a supplied Role-diagonal section `δ` for a
fixed Role, via `q = δ + v` on that Role (synthesis §2 / #127). -/
def passportReferenceFromSuppliedDiagonal (e : LocalCoframeField N) (r₀ : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace) : ReferenceLegField N :=
  fun y r =>
    if r = r₀ then δ y + solderLegVector N e y r else solderLegVector N e y r

/-- Conditional κ from a supplied diagonal `δ` (independent of any extension). -/
def passportConditionalMismatchFromSuppliedDelta
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r₀ : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  transportedReferenceMismatch A e (passportReferenceFromSuppliedDiagonal e r₀ δ) x r

/-! ## Predecessor torsion τ = −L ρ -/

/-- Predecessor torsion at edge `(x,r)` with source `y = x + r`:
`τ = b_{x,r} + L_{x,r} v_r(y) − v_r(x)`. -/
def predecessorTorsion
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  let y := sourceSiteFromPredecessor N r x
  (A x r).shift + (A x r).lin (solderLegVector N e y r) - solderLegVector N e x r

/-- Exact identity `τ_r = − L_{x,r} ρ_r(y)` with `y = x + r` and
`ρ` the `#125` predecessor defect at the **source** site. -/
theorem predecessorTorsion_eq_neg_lin_predecessorDefect
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    let y := sourceSiteFromPredecessor N r x
    predecessorTorsion A e x r =
      - (A x r).lin (predecessorDefect A e y r) := by
  intro y
  have hx : predecessorSite N r y = x :=
    predecessorSite_sourceSiteFromPredecessor r x
  -- ρ = A⁻¹(v(x)) − v(y) = L⁻¹ v(x) − L⁻¹ b − v(y)
  simp only [predecessorTorsion, predecessorDefect, AffineCartanMap.apply,
    AffineCartanMap.inv_lin, AffineCartanMap.inv_shift, hx, map_sub, map_neg,
    LinearEquiv.apply_symm_apply]
  abel

/-! ## Conditional κ from supplied sourced diagonal -/

/-- Conditional κ assembled from a Role-diagonal section `δ` on Role `r`
via `#127` `referenceFromSuppliedDiagonal` /
`conditionalMismatchFromSuppliedDelta`.
Indices: predecessor `x`, source `y = x + r`, evaluated on matching Role `r`. -/
def sourcedConditionalMismatch
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) : RoleSpace :=
  passportConditionalMismatchFromSuppliedDelta A e r δ x r

/-- On the matching Role, supplied-δ reference is `q_r(y) = δ(y) + v_r(y)`. -/
theorem passportReferenceFromSuppliedDiagonal_matching_role
    (e : LocalCoframeField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (y : ArchiveRolePhaseGroup N) :
    passportReferenceFromSuppliedDiagonal e r δ y r =
      δ y + solderLegVector N e y r := by
  simp only [passportReferenceFromSuppliedDiagonal, if_pos rfl]

/-- Diagonal overlap of the supplied-δ reference equals `δ` on the matching Role. -/
theorem diagonalOverlap_passportReferenceFromSuppliedDiagonal
    (e : LocalCoframeField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (y : ArchiveRolePhaseGroup N) :
    diagonalOverlap (passportReferenceFromSuppliedDiagonal e r δ y)
        (fun s => solderLegVector N e y s) r = δ y := by
  simp only [diagonalOverlap, passportReferenceFromSuppliedDiagonal_matching_role]
  abel

/-- Reuse the landed diagonal-form owner: `κ = A(v(y)) − v(x) + L δ(y)`. -/
theorem sourcedConditionalMismatch_diagonal_expansion
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) :
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x =
      AffineCartanMap.apply (A x r) (solderLegVector N e y r)
        - solderLegVector N e x r
        + (A x r).lin (δ y) := by
  intro y
  -- Specialize `transportedReferenceMismatch_diagonal_form` to supplied-δ reference.
  have hform := transportedReferenceMismatch_diagonal_form A e
      (passportReferenceFromSuppliedDiagonal e r δ) x r
  -- Replace diagonal overlap by δ on the matching Role.
  simp only [sourcedConditionalMismatch, passportConditionalMismatchFromSuppliedDelta,
    sourceSiteFromPredecessor, diagonalOverlap_passportReferenceFromSuppliedDiagonal] at hform ⊢
  exact hform

/-- κ = τ + L δ (memo §5 conditional-mismatch row / §6 prelude). -/
theorem sourcedConditionalMismatch_eq_torsion_add_lin_delta
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) :
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x =
      predecessorTorsion A e x r + (A x r).lin (δ y) := by
  intro y
  simp only [sourcedConditionalMismatch_diagonal_expansion, predecessorTorsion,
    sourceSiteFromPredecessor, AffineCartanMap.apply]
  abel

/-- Intermediate form `κ = L(δ − ρ)` (no dynamics). -/
theorem sourcedConditionalMismatch_eq_lin_delta_sub_predecessorDefect
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) :
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x =
      (A x r).lin (δ y - predecessorDefect A e y r) := by
  intro y
  rw [sourcedConditionalMismatch_eq_torsion_add_lin_delta,
    predecessorTorsion_eq_neg_lin_predecessorDefect]
  simp only [map_sub]
  abel

/-! ## Passport: κ = L(R + h) under δ = a + h -/

/-- Definitional sourced ansatz: `δ = a + h` for `h := parallelResidual`. -/
theorem sourced_ansatz_delta_eq_seed_add_parallelResidual
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (y : ArchiveRolePhaseGroup N) :
    δ y = diagonalSeed A J y r + parallelResidual A J δ y r := by
  simp only [parallelResidual]
  abel

/-- **Passport theorem (memo §6.1 / boxed `κ = L(R+h)`).**

For any supplied comparison endomorphism field `J` and any diagonal section `δ`,
writing `a = diagonalSeed`, `R = relativeDefect`, `h = parallelResidual = δ − a`
(so `δ = a + h` definitionally) and using source/predecessor indices
`y = x + r`, one has

\[
\kappa(x,r)=L_{x,r}\bigl(R_r(y)+h_r(y)\bigr).
\]

Reuses `#125` `ρ = a − R` and does not construct or select `J`. -/
theorem sourced_mismatch_factors_as_lin_relativeDefect_add_parallelResidual
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) :
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x =
      (A x r).lin
        (relativeDefect A e J y r + parallelResidual A J δ y r) := by
  intro y
  -- κ = L(δ − ρ) and ρ = a − R ⇒ δ − ρ = R + (δ − a) = R + h
  have hρ := predecessorDefect_eq_seed_sub_relativeDefect A e J y r
  rw [sourcedConditionalMismatch_eq_lin_delta_sub_predecessorDefect, hρ]
  simp only [parallelResidual]
  abel

/-- Alias matching the memo boxed name `κ = L(R+h)`. -/
theorem kappa_eq_lin_relativeDefect_add_parallelResidual
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) :
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x =
      (A x r).lin
        (relativeDefect A e J y r + parallelResidual A J δ y r) :=
  sourced_mismatch_factors_as_lin_relativeDefect_add_parallelResidual A e J r δ x

/-- Packaged form with an explicit `δ = a + h` witness (always available). -/
theorem sourced_mismatch_factors_of_sourced_ansatz
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N)
    (_h : ∀ y, δ y =
        diagonalSeed A J y r + parallelResidual A J δ y r) :
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x =
      (A x r).lin
        (relativeDefect A e J y r + parallelResidual A J δ y r) :=
  sourced_mismatch_factors_as_lin_relativeDefect_add_parallelResidual A e J r δ x

/-! ## Thin controls (no classicality claims) -/

/-- Flat control: κ = 0 on flat A, zero coframe, zero diagonal. -/
theorem sourced_mismatch_factor_flat_zero
    (r : Role) (x : ArchiveRolePhaseGroup N) :
    sourcedConditionalMismatch (flatAffineConnection N) (0 : LocalCoframeField N) r
        (fun _ => (0 : RoleSpace)) x = 0 := by
  simp only [sourcedConditionalMismatch, passportConditionalMismatchFromSuppliedDelta,
    transportedReferenceMismatch, passportReferenceFromSuppliedDiagonal,
    flatAffineConnection, AffineCartanMap.apply, AffineCartanMap.one_lin,
    AffineCartanMap.one_shift, LinearEquiv.refl_apply, solderLegVector_zero]
  abel

/-- Pure-shift sanity: with `δ = 0` on pure shift / zero coframe the mismatch
equals the shift `b`, while `R = 0` and `h = b` under zero comparison, so the
passport recovers `κ = b = L(0 + b)`. Rejects reading `R = 0 ⇒ κ = 0`
(memo §6 / §9.1). -/
theorem sourced_mismatch_factor_pureShift_zeroDelta
    (b : RoleSpace) (r : Role) (x : ArchiveRolePhaseGroup N) :
    let A := pureShiftAffineConnection N b
    let e : LocalCoframeField N := 0
    let J : ComparisonEndomorphismField N := fun _ => 0
    let δ : ArchiveRolePhaseGroup N → RoleSpace := fun _ => 0
    let y := sourceSiteFromPredecessor N r x
    sourcedConditionalMismatch A e r δ x = b ∧
      relativeDefect A e J y r = 0 ∧
      parallelResidual A J δ y r = b ∧
      sourcedConditionalMismatch A e r δ x =
        (A x r).lin (relativeDefect A e J y r + parallelResidual A J δ y r) := by
  intro A e J δ y
  have hκ : sourcedConditionalMismatch A e r δ x = b := by
    simp only [sourcedConditionalMismatch, passportConditionalMismatchFromSuppliedDelta,
      transportedReferenceMismatch, passportReferenceFromSuppliedDiagonal,
      pureShiftAffineConnection, AffineCartanMap.apply, LinearEquiv.refl_apply,
      solderLegVector_zero]
    abel
  have hR : relativeDefect A e J y r = 0 := by
    simp only [relativeDefect, deltaV, deltaB, barV, barB, predecessorSite,
      pureShiftAffineConnection, solderLegVector_zero, map_zero, sub_zero,
      zero_sub, sub_self, LinearMap.zero_apply]
  have hh : parallelResidual A J δ y r = b := by
    -- a = −barB − J Δb = −L⁻¹ b = −b (lin = id); h = δ − a = b
    simp only [parallelResidual, diagonalSeed, deltaB, barB, predecessorSite,
      pureShiftAffineConnection, LinearEquiv.refl_apply, map_zero, sub_zero,
      zero_sub, LinearMap.zero_apply]
    abel
  refine ⟨hκ, hR, hh, ?_⟩
  simpa [hκ, hR, hh, pureShiftAffineConnection, LinearEquiv.refl_apply] using
    (sourced_mismatch_factors_as_lin_relativeDefect_add_parallelResidual
      A e J r δ x)

end

end D0.Geometry
