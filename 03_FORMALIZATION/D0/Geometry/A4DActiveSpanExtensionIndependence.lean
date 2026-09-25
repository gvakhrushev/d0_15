import Mathlib.Tactic
import D0.Geometry.A4DConditionalSourcedDiagonalTransport
import D0.Geometry.A4DRelativeAEComparisonSpan
import D0.Geometry.A4DTransportedReferenceMismatch

/-!
# Active-span extension independence of the sourced diagonal chain

Lean-owns the pressure claim that **full-fibre extension freedom of the relative
A/e comparison is physically irrelevant** to the already-owned sourced diagonal
chain (PR #125), once two full extensions agree on the active affine-increment
span `U` (PR #126).

If `J₁|_U = J₂|_U` and every actual increment `Δb_r` lies in `U`, then `J₁` and
`J₂` produce identical relative defects, seeds, predecessor decompositions, path
sources, sourced solution spaces, and conditional mismatches for a supplied
diagonal `δ`.

A rank-deficient witness (`U = ⊥`) exhibits two distinct full extensions with
identical downstream sourced data. The full-rank corollary `U = ⊤` is stated only
as stronger **identifiability**, not as classicality / a physical requirement.

Firewalls: no new choice of `J`, no finite `F` / E dressing, no `A = A(e)`, no
stress/time/golden, no promoting full rank to classicality.
-/

namespace D0.Geometry

open D0
open A4DRelativeAEComparisonSpan

local instance activeSpanExtRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {N : ℕ}

/-! ## Setup: agreement on the active span -/

/-- Two endomorphism fields agree on a submodule `U` at every site. -/
def AgreeOnActiveSpan (U : Submodule ℝ RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N) : Prop :=
  ∀ y : ArchiveRolePhaseGroup N, ∀ u ∈ U, J₁ y u = J₂ y u

/-- Every Role-increment at every site lands in the active span. -/
def IncrementsInActiveSpan (A : AffineCartanConnection N ℝ RoleSpace)
    (U : Submodule ℝ RoleSpace) : Prop :=
  ∀ y : ArchiveRolePhaseGroup N, ∀ r : Role, deltaB A y r ∈ U

/-- Agreement of two endomorphisms as linear maps on `U`. -/
theorem agreeOnActiveSpan_apply
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (h : AgreeOnActiveSpan U J₁ J₂) (y : ArchiveRolePhaseGroup N) {u : RoleSpace}
    (hu : u ∈ U) : J₁ y u = J₂ y u :=
  h y u hu

/-! ## 1. Generator action independence -/

/-- On every actual increment, `J₁ Δb_r = J₂ Δb_r`. -/
theorem generator_action_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (U : Submodule ℝ RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    J₁ y (deltaB A y r) = J₂ y (deltaB A y r) :=
  hagree y (deltaB A y r) (hΔ y r)

/-! ## 2. Relative-defect independence -/

theorem relativeDefect_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    relativeDefect A e J₁ y r = relativeDefect A e J₂ y r := by
  simp only [relativeDefect, generator_action_independence A U J₁ J₂ hagree hΔ y r]

/-! ## 3. Seed independence -/

theorem diagonalSeed_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (U : Submodule ℝ RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    diagonalSeed A J₁ y r = diagonalSeed A J₂ y r := by
  simp only [diagonalSeed, generator_action_independence A U J₁ J₂ hagree hΔ y r]

/-! ## 4. Predecessor-decomposition independence -/

/-- The exact predecessor identity `ρ = a − R` is compatible with both
extensions, and the resulting `a − R` expressions coincide. -/
theorem predecessor_decomposition_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    predecessorDefect A e y r =
        diagonalSeed A J₁ y r - relativeDefect A e J₁ y r ∧
      predecessorDefect A e y r =
        diagonalSeed A J₂ y r - relativeDefect A e J₂ y r ∧
      diagonalSeed A J₁ y r - relativeDefect A e J₁ y r =
        diagonalSeed A J₂ y r - relativeDefect A e J₂ y r := by
  refine ⟨predecessorDefect_eq_seed_sub_relativeDefect A e J₁ y r,
    predecessorDefect_eq_seed_sub_relativeDefect A e J₂ y r, ?_⟩
  simp only [diagonalSeed_independence A U J₁ J₂ hagree hΔ y r,
    relativeDefect_independence A e U J₁ J₂ hagree hΔ y r]

/-! ## 5. Path-source independence -/

theorem pathSource_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (U : Submodule ℝ RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (r : Role) (p : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    pathSource A J₁ r p y = pathSource A J₂ r p y := by
  simp only [pathSource,
    diagonalSeed_independence A U J₁ J₂ hagree hΔ (pathEnd N p y) r,
    diagonalSeed_independence A U J₁ J₂ hagree hΔ y r]

/-! ## 6. Sourced-solution-space independence -/

/-- The equation `P_p δ(y') − δ(y) = S_p` has the same solution set for both
extensions. -/
theorem sourced_solution_space_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (U : Submodule ℝ RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (r : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (p : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    (covariantLin A p y (δ (pathEnd N p y)) - δ y = pathSource A J₁ r p y) ↔
      (covariantLin A p y (δ (pathEnd N p y)) - δ y = pathSource A J₂ r p y) := by
  rw [pathSource_independence A U J₁ J₂ hagree hΔ r p y]

theorem sourced_solution_all_paths_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (U : Submodule ℝ RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (r : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace) :
    (∀ p y, covariantLin A p y (δ (pathEnd N p y)) - δ y =
        pathSource A J₁ r p y) ↔
      (∀ p y, covariantLin A p y (δ (pathEnd N p y)) - δ y =
        pathSource A J₂ r p y) := by
  constructor <;> intro h p y
  · exact (sourced_solution_space_independence A U J₁ J₂ hagree hΔ r δ p y).mp (h p y)
  · exact (sourced_solution_space_independence A U J₁ J₂ hagree hΔ r δ p y).mpr (h p y)

/-! ## 7. Conditional mismatch independence (supplied δ) -/

/-- Build a `ReferenceLegField` from a supplied Role-diagonal section `δ` for a
fixed Role, via `q = δ + v` on that Role (synthesis §2). -/
def referenceFromSuppliedDiagonal (e : LocalCoframeField N) (r₀ : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace) : ReferenceLegField N :=
  fun y r =>
    if r = r₀ then δ y + solderLegVector N e y r else solderLegVector N e y r

/-- Conditional κ from a supplied diagonal `δ` (independent of any extension). -/
def conditionalMismatchFromSuppliedDelta
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (r₀ : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  transportedReferenceMismatch A e (referenceFromSuppliedDiagonal e r₀ δ) x r

/-- For any **supplied** diagonal `δ`, conditional κ is identical for both
extensions (κ is assembled from `(A,e,δ)` only; the extension agreement
hypothesis records that the comparison fibre is irrelevant). -/
theorem conditionalMismatch_supplied_delta_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (_hagree : AgreeOnActiveSpan U J₁ J₂)
    (_hΔ : IncrementsInActiveSpan A U)
    (r₀ : Role) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    conditionalMismatchFromSuppliedDelta A e r₀ δ x r =
      conditionalMismatchFromSuppliedDelta A e r₀ δ x r :=
  rfl

/-- Seed-derived diagonal reference: `δ := a_r(J)` (zero parallel residual). -/
def seedAsSuppliedDiagonal (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r₀ : Role) :
    ArchiveRolePhaseGroup N → RoleSpace :=
  fun y => diagonalSeed A J y r₀

/-- Conditional κ built from the seed diagonal of an extension. -/
def conditionalMismatchFromSeed
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N) (r₀ : Role)
    (x : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  conditionalMismatchFromSuppliedDelta A e r₀ (seedAsSuppliedDiagonal A J r₀) x r

/-- Seed-derived conditional κ is independent of the full-fibre extension. -/
theorem conditionalMismatch_seed_independence
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U)
    (r₀ : Role) (x : ArchiveRolePhaseGroup N) (r : Role) :
    conditionalMismatchFromSeed A e J₁ r₀ x r =
      conditionalMismatchFromSeed A e J₂ r₀ x r := by
  simp only [conditionalMismatchFromSeed, conditionalMismatchFromSuppliedDelta,
    referenceFromSuppliedDiagonal, seedAsSuppliedDiagonal,
    transportedReferenceMismatch,
    diagonalSeed_independence A U J₁ J₂ hagree hΔ]

/-! ## 8. Quotient / restriction packaging -/

/-- Endomorphisms that vanish on the active span `U`. -/
def vanishesOnActiveSpan (U : Submodule ℝ RoleSpace) :
    Submodule ℝ (RoleSpace →ₗ[ℝ] RoleSpace) where
  carrier := { J | ∀ u ∈ U, J u = 0 }
  zero_mem' := by intro u hu; simp
  add_mem' := by
    intro J₁ J₂ h₁ h₂ u hu
    simp [h₁ u hu, h₂ u hu]
  smul_mem' := by
    intro a J hJ u hu
    simp [hJ u hu]

/-- Agreement on `U` iff the difference vanishes on `U`. -/
theorem agreeOnActiveSpan_iff_diff_vanishes
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) :
    (∀ u ∈ U, J₁ y u = J₂ y u) ↔ J₁ y - J₂ y ∈ vanishesOnActiveSpan U := by
  constructor
  · intro h u hu
    simp [vanishesOnActiveSpan, h u hu]
  · intro h u hu
    have := h u hu
    simpa [vanishesOnActiveSpan, sub_eq_zero] using this

/-- Downstream relative defect factors through the restriction `J|_U`. -/
theorem relativeDefect_depends_only_on_restriction
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (U : Submodule ℝ RoleSpace) (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (hΔ : IncrementsInActiveSpan A U) :
    (fun y r => relativeDefect A e J₁ y r) =
      (fun y r => relativeDefect A e J₂ y r) := by
  funext y r
  exact relativeDefect_independence A e U J₁ J₂ hagree hΔ y r

/-- Packaged quotient statement: seed, path source, and relative defect are
unchanged under adding any map that vanishes on `U`. -/
theorem sourced_diagonal_factors_through_active_span_restriction
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (U : Submodule ℝ RoleSpace) (J : ComparisonEndomorphismField N)
    (Z : ComparisonEndomorphismField N)
    (hZ : ∀ y, Z y ∈ vanishesOnActiveSpan U)
    (hΔ : IncrementsInActiveSpan A U)
    (y : ArchiveRolePhaseGroup N) (r : Role) (p : List ChainStep) :
    relativeDefect A e (fun x => J x + Z x) y r = relativeDefect A e J y r ∧
      diagonalSeed A (fun x => J x + Z x) y r = diagonalSeed A J y r ∧
      pathSource A (fun x => J x + Z x) r p y = pathSource A J r p y := by
  have hagree : AgreeOnActiveSpan U (fun x => J x + Z x) J := by
    intro y' u hu
    have hz := hZ y' u hu
    simp [hz]
  refine ⟨relativeDefect_independence A e U (fun x => J x + Z x) J hagree hΔ y r,
    diagonalSeed_independence A U (fun x => J x + Z x) J hagree hΔ y r,
    pathSource_independence A U (fun x => J x + Z x) J hagree hΔ r p y⟩

/-- When `U = comparisonDomain B` (PR #126 active affine-increment span) and
increments land in that span, downstream data depend only on the restriction. -/
theorem sourced_diagonal_factors_through_comparisonDomain
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (B : LabelCoeff →ₗ[ℝ] RoleSpace)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan (comparisonDomain B) J₁ J₂)
    (hΔ : IncrementsInActiveSpan A (comparisonDomain B))
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    relativeDefect A e J₁ y r = relativeDefect A e J₂ y r ∧
      diagonalSeed A J₁ y r = diagonalSeed A J₂ y r :=
  ⟨relativeDefect_independence A e (comparisonDomain B) J₁ J₂ hagree hΔ y r,
    diagonalSeed_independence A (comparisonDomain B) J₁ J₂ hagree hΔ y r⟩

/-! ## 9. Full-rank corollary (identifiability only — NOT classicality) -/

/-- If `U = ⊤`, agreement on the active span forces the full endomorphisms to
coincide at every site. This is a stronger **identifiability** condition on the
comparison fibre, not a classicality / physical requirement. -/
theorem full_rank_extension_identifiability
    (U : Submodule ℝ RoleSpace) (hU : U = ⊤)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan U J₁ J₂)
    (y : ArchiveRolePhaseGroup N) : J₁ y = J₂ y := by
  apply LinearMap.ext
  intro v
  have hv : v ∈ U := by simp [hU]
  exact hagree y v hv

/-- Packaged: under `U = ⊤` (equivalently `rank B = 4` when `U = range B = ⊤`),
extension freedom vanishes. Stated only as identifiability. -/
theorem full_rank_comparisonDomain_identifiability
    (B : LabelCoeff →ₗ[ℝ] RoleSpace)
    (hU : comparisonDomain B = ⊤)
    (J₁ J₂ : ComparisonEndomorphismField N)
    (hagree : AgreeOnActiveSpan (comparisonDomain B) J₁ J₂)
    (y : ArchiveRolePhaseGroup N) : J₁ y = J₂ y :=
  full_rank_extension_identifiability (comparisonDomain B) hU J₁ J₂ hagree y

/-! ## 10. Rank-deficient exact witness (mandatory) -/

/-- Constant zero comparison field. -/
def rankZeroExtensionZero : ComparisonEndomorphismField N :=
  fun _ => 0

/-- Constant identity comparison field. -/
def rankZeroExtensionId : ComparisonEndomorphismField N :=
  fun _ => LinearMap.id

/-- The two rank-zero witness extensions are distinct as full endomorphisms. -/
theorem rank_zero_extensions_ne :
    (rankZeroExtensionZero : ComparisonEndomorphismField N) ≠
      rankZeroExtensionId := by
  intro h
  have hfun := congrArg (fun J : ComparisonEndomorphismField N =>
    J (0 : ArchiveRolePhaseGroup N) (archiveRoleBasis A)) h
  -- 0 e_A = 0, id e_A = e_A ≠ 0
  have : (0 : RoleSpace) = archiveRoleBasis A := by
    simpa [rankZeroExtensionZero, rankZeroExtensionId] using hfun
  have hcoord := congrArg (fun v : RoleSpace => v A) this
  simp [archiveRoleBasis, Pi.basisFun_apply, Pi.single_eq_same] at hcoord

/-- They agree on the rank-zero active span `U = ⊥`. -/
theorem rank_zero_agree_on_bot :
    AgreeOnActiveSpan (N := N) (⊥ : Submodule ℝ RoleSpace)
      rankZeroExtensionZero rankZeroExtensionId := by
  intro y u hu
  have hu0 : u = 0 := by simpa using hu
  simp [rankZeroExtensionZero, rankZeroExtensionId, hu0]

/-- On the zero span, every increment hypothesis is exactly `Δb = 0`. -/
theorem increments_in_bot_iff_deltaB_eq_zero
    (A : AffineCartanConnection N ℝ RoleSpace) :
    IncrementsInActiveSpan A (⊥ : Submodule ℝ RoleSpace) ↔
      ∀ y r, deltaB A y r = 0 := by
  constructor
  · intro h y r
    have := h y r
    simp only [Submodule.mem_bot] at this
    exact this
  · intro h y r
    simp [h y r]

/-- Rank-zero witness: distinct full extensions, identical generator action on
every increment in `U = ⊥`. -/
theorem rank_zero_generator_action_identical
    (A : AffineCartanConnection N ℝ RoleSpace)
    (hΔ : IncrementsInActiveSpan A (⊥ : Submodule ℝ RoleSpace))
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    rankZeroExtensionZero y (deltaB A y r) =
      rankZeroExtensionId y (deltaB A y r) :=
  generator_action_independence A ⊥ rankZeroExtensionZero rankZeroExtensionId
    rank_zero_agree_on_bot hΔ y r

/-- Rank-zero witness: identical relative defects. -/
theorem rank_zero_relativeDefect_identical
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (hΔ : IncrementsInActiveSpan A (⊥ : Submodule ℝ RoleSpace))
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    relativeDefect A e rankZeroExtensionZero y r =
      relativeDefect A e rankZeroExtensionId y r :=
  relativeDefect_independence A e ⊥ rankZeroExtensionZero rankZeroExtensionId
    rank_zero_agree_on_bot hΔ y r

/-- Rank-zero witness: identical seeds. -/
theorem rank_zero_diagonalSeed_identical
    (A : AffineCartanConnection N ℝ RoleSpace)
    (hΔ : IncrementsInActiveSpan A (⊥ : Submodule ℝ RoleSpace))
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    diagonalSeed A rankZeroExtensionZero y r =
      diagonalSeed A rankZeroExtensionId y r :=
  diagonalSeed_independence A ⊥ rankZeroExtensionZero rankZeroExtensionId
    rank_zero_agree_on_bot hΔ y r

/-- Rank-zero witness: identical path sources. -/
theorem rank_zero_pathSource_identical
    (A : AffineCartanConnection N ℝ RoleSpace)
    (hΔ : IncrementsInActiveSpan A (⊥ : Submodule ℝ RoleSpace))
    (r : Role) (p : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    pathSource A rankZeroExtensionZero r p y =
      pathSource A rankZeroExtensionId r p y :=
  pathSource_independence A ⊥ rankZeroExtensionZero rankZeroExtensionId
    rank_zero_agree_on_bot hΔ r p y

/-- Concrete flat control: `Δb = 0` on the flat connection, so the rank-zero
increment hypothesis holds and all sourced data coincide for `0 ≠ id`. -/
theorem flat_increments_in_bot :
    IncrementsInActiveSpan (N := N) (flatAffineConnection N)
      (⊥ : Submodule ℝ RoleSpace) := by
  intro y r
  -- flat: shift = 0, lin = id ⇒ barB = 0, deltaB = 0
  simp [IncrementsInActiveSpan, deltaB, barB, predecessorSite, flatAffineConnection,
    AffineCartanMap.one_shift, AffineCartanMap.one_lin, map_zero, sub_self]

/-- Packaged mandatory witness: two distinct full extensions on a rank-zero
active span produce identical downstream sourced-diagonal data on the flat
control (and hence whenever `Δb ∈ ⊥`). -/
theorem rank_zero_exact_witness_flat
    (e : LocalCoframeField N) (y : ArchiveRolePhaseGroup N) (r : Role)
    (p : List ChainStep) :
    (rankZeroExtensionZero : ComparisonEndomorphismField N) ≠
        rankZeroExtensionId ∧
      AgreeOnActiveSpan (N := N) (⊥ : Submodule ℝ RoleSpace)
        rankZeroExtensionZero rankZeroExtensionId ∧
      relativeDefect (flatAffineConnection N) e rankZeroExtensionZero y r =
        relativeDefect (flatAffineConnection N) e rankZeroExtensionId y r ∧
      diagonalSeed (flatAffineConnection N) rankZeroExtensionZero y r =
        diagonalSeed (flatAffineConnection N) rankZeroExtensionId y r ∧
      pathSource (flatAffineConnection N) rankZeroExtensionZero r p y =
        pathSource (flatAffineConnection N) rankZeroExtensionId r p y :=
  ⟨rank_zero_extensions_ne,
    rank_zero_agree_on_bot,
    rank_zero_relativeDefect_identical (flatAffineConnection N) e
      flat_increments_in_bot y r,
    rank_zero_diagonalSeed_identical (flatAffineConnection N)
      flat_increments_in_bot y r,
    rank_zero_pathSource_identical (flatAffineConnection N)
      flat_increments_in_bot r p y⟩

/-- Rank-one active span: `ℝ ∙ e_A`. -/
def rankOneActiveSpan : Submodule ℝ RoleSpace :=
  ℝ ∙ archiveRoleBasis A

/-- Rank-one extension that kills everything (zero). -/
def rankOneExtensionZero : ComparisonEndomorphismField N :=
  fun _ => 0

/-- Rank-one extension that is the identity on `span{e_A}` and kills a
complementary Role direction `e_B` differently from zero — realized as the
rank-one projection onto `e_A` along the Role dual. -/
def rankOneProjectionA : RoleSpace →ₗ[ℝ] RoleSpace where
  toFun v := v A • archiveRoleBasis A
  map_add' x y := by
    simp [archiveRoleBasis, Pi.basisFun_apply, add_smul]
  map_smul' a x := by
    simp [archiveRoleBasis, Pi.basisFun_apply, smul_smul, mul_comm]

def rankOneExtensionProj : ComparisonEndomorphismField N :=
  fun _ => rankOneProjectionA

/-- On the rank-one span, projection and zero disagree as full maps but...
wait: projection and zero do NOT agree on span{e_A}. Need two maps that agree
on span{e_A} but differ off it.

Take `J₁ = 0` and `J₂ =` projection onto a complementary direction (e.g. onto
`e_B`), so both kill `e_A` / agree as zero on `ℝ∙e_A`, but `J₂ ≠ 0`. -/
def rankOneComplementProjectionB : RoleSpace →ₗ[ℝ] RoleSpace where
  toFun v := v B • archiveRoleBasis B
  map_add' x y := by
    simp [archiveRoleBasis, Pi.basisFun_apply, add_smul]
  map_smul' a x := by
    simp [archiveRoleBasis, Pi.basisFun_apply, smul_smul, mul_comm]

def rankOneExtensionComplementB : ComparisonEndomorphismField N :=
  fun _ => rankOneComplementProjectionB

theorem rank_one_extensions_ne :
    (rankOneExtensionZero : ComparisonEndomorphismField N) ≠
      rankOneExtensionComplementB := by
  intro h
  have hfun := congrArg (fun J : ComparisonEndomorphismField N =>
    J (0 : ArchiveRolePhaseGroup N) (archiveRoleBasis B)) h
  have hAB : A ≠ B := by decide
  have : (0 : RoleSpace) = archiveRoleBasis B := by
    -- complement projection sends e_B ↦ e_B
    simpa [rankOneExtensionZero, rankOneExtensionComplementB,
      rankOneComplementProjectionB, archiveRoleBasis, Pi.basisFun_apply,
      Pi.single_eq_same] using hfun
  have hcoord := congrArg (fun v : RoleSpace => v B) this
  simp [archiveRoleBasis, Pi.basisFun_apply, Pi.single_eq_same] at hcoord

theorem rank_one_agree_on_spanA :
    AgreeOnActiveSpan (N := N) rankOneActiveSpan
      rankOneExtensionZero rankOneExtensionComplementB := by
  intro y u hu
  -- u ∈ ℝ ∙ e_A ⇒ u = t • e_A ⇒ u B = 0 ⇒ complement projection kills u
  obtain ⟨t, rfl⟩ := Submodule.mem_span_singleton.mp hu
  have hAB : A ≠ B := by decide
  simp [rankOneExtensionZero, rankOneExtensionComplementB,
    rankOneComplementProjectionB, archiveRoleBasis, Pi.basisFun_apply,
    Pi.single_apply, hAB]

/-- Rank-one packaged witness: distinct extensions agreeing on `ℝ∙e_A` give
identical downstream data whenever increments land in that span. -/
theorem rank_one_exact_witness
    (Aconn : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (hΔ : IncrementsInActiveSpan Aconn rankOneActiveSpan)
    (y : ArchiveRolePhaseGroup N) (r : Role) (p : List ChainStep) :
    (rankOneExtensionZero : ComparisonEndomorphismField N) ≠
        rankOneExtensionComplementB ∧
      AgreeOnActiveSpan (N := N) rankOneActiveSpan
        rankOneExtensionZero rankOneExtensionComplementB ∧
      relativeDefect Aconn e rankOneExtensionZero y r =
        relativeDefect Aconn e rankOneExtensionComplementB y r ∧
      diagonalSeed Aconn rankOneExtensionZero y r =
        diagonalSeed Aconn rankOneExtensionComplementB y r ∧
      pathSource Aconn rankOneExtensionZero r p y =
        pathSource Aconn rankOneExtensionComplementB r p y :=
  ⟨rank_one_extensions_ne,
    rank_one_agree_on_spanA,
    relativeDefect_independence Aconn e rankOneActiveSpan
      rankOneExtensionZero rankOneExtensionComplementB
      rank_one_agree_on_spanA hΔ y r,
    diagonalSeed_independence Aconn rankOneActiveSpan
      rankOneExtensionZero rankOneExtensionComplementB
      rank_one_agree_on_spanA hΔ y r,
    pathSource_independence Aconn rankOneActiveSpan
      rankOneExtensionZero rankOneExtensionComplementB
      rank_one_agree_on_spanA hΔ r p y⟩

end

end D0.Geometry
