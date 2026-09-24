import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.A4DRawSolderFrameAction
import D0.Geometry.ArchiveAffineExteriorLink

/-!
# Affine-origin covariance boundary for transported-reference mismatch

Isolates the exact algebraic fact from PR #112 / memo §§18–21:

* if both the source reference leg and the target solder leg transform as
  affine points under node gauges `h_y`, `h_x`, the transported-reference
  difference is covariant under the linear part of `h_x`;
* if the reference transforms affinely while the solder leg transforms only
  linearly, an uncancelled `h_x.shift` defect remains;
* the owned `rawFullSolderFrameAction` supplies a linear right-frame action
  only — it does not by itself provide that translation term.

This module does **not** claim D0 already owns a full affine solder action,
does **not** choose a physical `q(A,e)`, and leaves that research question
open for `EXP-A4D-SOLDER-REFERENCE-LEG-SECTION`.
-/

namespace D0.Geometry

open D0
open AffineCartanMap

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-! ## 1. Affine conjugation evaluation (point-level) -/

/-- Gauge-conjugated link `A' = h_x * A * h_y⁻¹` evaluates on the affinely
transformed source point exactly as the push of `A` by `h_x`. -/
theorem affineConj_apply_eval
    (h_x A h_y : AffineCartanMap K V) (q : V) :
    apply (h_x * A * h_y⁻¹) (apply h_y q) = apply h_x (apply A q) := by
  have hcancel : h_x * A * h_y⁻¹ * h_y = h_x * A := by
    calc
      h_x * A * h_y⁻¹ * h_y = h_x * A * (h_y⁻¹ * h_y) := by
        simp only [affine_mul_assoc]
      _ = h_x * A * 1 := by rw [affine_inv_mul]
      _ = h_x * A := by simp [affine_mul_one]
  calc
    apply (h_x * A * h_y⁻¹) (apply h_y q)
        = apply ((h_x * A * h_y⁻¹) * h_y) q := by
          rw [← apply_mul]
    _ = apply (h_x * A) q := by rw [hcancel]
    _ = apply h_x (apply A q) := by rw [apply_mul]

/-! ## 2. Difference of affine points is linear -/

/-- For any affine node map, the difference of images is the linear part on
the difference of arguments. -/
theorem affineApply_sub (h : AffineCartanMap K V) (u v : V) :
    apply h u - apply h v = h.lin (u - v) := by
  simp only [apply, map_sub]
  abel

/-! ## 3. Full affine origin/solder covariance -/

/-- When both the reference leg `q` and the solder leg `v` transform as affine
points, the transported-reference difference is covariant under `h_x.lin`. -/
theorem affineOrigin_fullCovariance
    (h_x A h_y : AffineCartanMap K V) (q v : V)
    (q' v' : V) (hq : q' = apply h_y q) (hv : v' = apply h_x v) :
    apply (h_x * A * h_y⁻¹) q' - v' =
      h_x.lin (apply A q - v) := by
  subst hq; subst hv
  rw [affineConj_apply_eval, affineApply_sub]

/-! ## 4. Linear-only solder defect (hostile control) -/

/-- If `q` transforms affinely but the solder leg is transformed only by the
linear part of `h_x`, the residual is the covariant difference plus `h_x.shift`.
Sign follows `apply = lin · + shift`. -/
theorem affineOrigin_linearOnlySolder_defect
    (h_x A h_y : AffineCartanMap K V) (q v : V)
    (q' v' : V) (hq : q' = apply h_y q) (hv : v' = h_x.lin v) :
    apply (h_x * A * h_y⁻¹) q' - v' =
      h_x.lin (apply A q - v) + h_x.shift := by
  subst hq; subst hv
  have h1 := affineConj_apply_eval h_x A h_y q
  -- LHS = apply h_x (apply A q) - h_x.lin v
  --     = (h_x.lin (apply A q) + h_x.shift) - h_x.lin v
  --     = h_x.lin (apply A q - v) + h_x.shift
  calc
    apply (h_x * A * h_y⁻¹) (apply h_y q) - h_x.lin v =
        apply h_x (apply A q) - h_x.lin v := by rw [h1]
    _ = h_x.lin (apply A q) + h_x.shift - h_x.lin v := by
          simp only [apply]
    _ = h_x.lin (apply A q) - h_x.lin v + h_x.shift := by abel
    _ = h_x.lin (apply A q - v) + h_x.shift := by
          rw [← map_sub]

/-! ## 5. Pure translation witness -/

/-- Pure node translation `h_x = (I, c)` leaves residual exactly `c` under the
linear-only solder law. -/
theorem affineOrigin_pureTranslation_residual
    (A h_y : AffineCartanMap K V) (q v c : V) :
    let h_x : AffineCartanMap K V := ⟨LinearEquiv.refl K V, c⟩
    apply (h_x * A * h_y⁻¹) (apply h_y q) - h_x.lin v =
      h_x.lin (apply A q - v) + c := by
  intro h_x
  simpa using
    affineOrigin_linearOnlySolder_defect h_x A h_y q v _ _ rfl rfl

/-- Concrete nonzero Role-basis residual under pure translation on `Role → ℝ`. -/
theorem affineOrigin_pureTranslation_roleBasis_nonzero (r : Role) :
    let c : RoleSpace := archiveRoleBasis r
    let h_x : AffineCartanMap ℝ RoleSpace := ⟨LinearEquiv.refl ℝ RoleSpace, c⟩
    let A : AffineCartanMap ℝ RoleSpace := 1
    let h_y : AffineCartanMap ℝ RoleSpace := 1
    let q : RoleSpace := 0
    let v : RoleSpace := 0
    apply (h_x * A * h_y⁻¹) (apply h_y q) - h_x.lin v = c ∧ c ≠ 0 := by
  intro c h_x A h_y q v
  have hres :
      apply (h_x * A * h_y⁻¹) (apply h_y q) - h_x.lin v =
        h_x.lin (apply A q - v) + c :=
    affineOrigin_pureTranslation_residual A h_y q v c
  have hsimp :
      apply (h_x * A * h_y⁻¹) (apply h_y q) - h_x.lin v = c := by
    simp [h_x, A, h_y, q, v, apply, one_lin, one_shift, map_zero, sub_zero,
      add_zero] at hres ⊢
  refine ⟨hsimp, ?_⟩
  intro hc
  have hcoord := congrArg (fun w : RoleSpace => w r) hc
  simp [c, archiveRoleBasis, Pi.basisFun_apply] at hcoord

/-! ## 6. Pure-linear subgroup recovery -/

/-- If `h_x.shift = 0`, the linear-only defect theorem reduces to homogeneous
vector covariance (Lean boundary matching PR #112's pure-linear frame result). -/
theorem affineOrigin_pureLinear_recovery
    (h_x A h_y : AffineCartanMap K V) (q v : V)
    (hshift : h_x.shift = 0)
    (q' v' : V) (hq : q' = apply h_y q) (hv : v' = h_x.lin v) :
    apply (h_x * A * h_y⁻¹) q' - v' =
      h_x.lin (apply A q - v) := by
  have hdef :=
    affineOrigin_linearOnlySolder_defect h_x A h_y q v q' v' hq hv
  simpa [hshift] using hdef

/-- Equivalent form: when `h_x` is pure-linear, full affine covariance for the
linear solder law coincides with the affine-point covariance identity. -/
theorem affineOrigin_pureLinear_matches_full
    (h_x A h_y : AffineCartanMap K V) (q v : V)
    (hshift : h_x.shift = 0) :
    apply (h_x * A * h_y⁻¹) (apply h_y q) - h_x.lin v =
      apply (h_x * A * h_y⁻¹) (apply h_y q) - apply h_x v := by
  -- apply h_x v = h_x.lin v + 0
  simp [apply, hshift]

/-! ## 7. Separation from raw solder owner -/

/-- Explicit-hypothesis separation: the owned raw full-solder frame action is a
**linear** right multiplication on the uncentered solder matrix. Under the
hypothesis that a would-be affine solder/origin law must also supply the
translation term `h_x.shift` appearing in the full covariance identity of
theorem 3, that action alone does not provide it.

This is not a universal no-go: it records the typed gap between the existing
linear right-frame owner and the affine-point law of theorem 3. -/
theorem rawFullSolderFrameAction_is_linear_right_action
    (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x =
      rawSolderMatrix N e x * Λ x :=
  rawFullSolderFrameAction_matrix N e Λ x

/-- Scoped corollary: a pure node translation `c ≠ 0` leaves residual `c` under
the linear-only solder law of theorem 4, while `rawFullSolderFrameAction`
transforms solder rows only by right matrix multiplication (no additive shift
term of type `RoleSpace`). Hence that owner does not by itself cancel the
translation defect required by theorem 3. -/
theorem rawFullSolderFrameAction_misses_affine_translation_term
    (c : RoleSpace) (hc : c ≠ 0) :
    (∃ (A h_y : AffineCartanMap ℝ RoleSpace) (q v : RoleSpace),
      let residual :=
        apply (⟨LinearEquiv.refl ℝ RoleSpace, c⟩ * A * h_y⁻¹) (apply h_y q) -
          (⟨LinearEquiv.refl ℝ RoleSpace, c⟩ : AffineCartanMap ℝ RoleSpace).lin v
      residual = c ∧ residual ≠ 0) ∧
    (∀ (N : ℕ) (e : LocalCoframeField N)
        (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
        (x : ArchiveRolePhaseGroup N),
      rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x =
        rawSolderMatrix N e x * Λ x) := by
  refine ⟨?_, rawFullSolderFrameAction_is_linear_right_action⟩
  refine ⟨1, 1, 0, 0, ?_⟩
  dsimp
  have h :=
    affineOrigin_pureTranslation_residual (1 : AffineCartanMap ℝ RoleSpace) 1 0 0 c
  have hres :
      apply
          ((⟨LinearEquiv.refl ℝ RoleSpace, c⟩ : AffineCartanMap ℝ RoleSpace) * 1 * (1 : AffineCartanMap ℝ RoleSpace)⁻¹)
          (apply (1 : AffineCartanMap ℝ RoleSpace) 0) -
        (⟨LinearEquiv.refl ℝ RoleSpace, c⟩ : AffineCartanMap ℝ RoleSpace).lin 0 = c := by
    simpa [apply, one_lin, one_shift, map_zero, sub_zero, add_zero] using h
  exact ⟨hres, hres ▸ hc⟩

/-! ## Optional abstract interface (uninstantiated) -/

/-- Abstract interface for a future affine solder/origin action: target solder
legs and source reference legs would both transform as affine points. Not
instantiated physically in this worker. -/
structure AffineSolderOriginAction (N : ℕ) (K V : Type*)
    [Field K] [AddCommGroup V] [Module K V] where
  /-- Affine-point law on target solder legs at site `x`. -/
  transformSolderLeg :
      AffineNodeGauge N K V →
        (ArchiveRolePhaseGroup N → Role → V) →
          (ArchiveRolePhaseGroup N → Role → V)
  /-- Affine-point law on source reference legs at site `y`. -/
  transformReferenceLeg :
      AffineNodeGauge N K V →
        (ArchiveRolePhaseGroup N → Role → V) →
          (ArchiveRolePhaseGroup N → Role → V)
  /-- Target solder legs transform by the full affine node map at `x`. -/
  solder_affine_point :
      ∀ (h : AffineNodeGauge N K V) (v : ArchiveRolePhaseGroup N → Role → V)
        (x : ArchiveRolePhaseGroup N) (r : Role),
        transformSolderLeg h v x r = apply (h x) (v x r)
  /-- Source reference legs transform by the full affine node map at `y`. -/
  reference_affine_point :
      ∀ (h : AffineNodeGauge N K V) (q : ArchiveRolePhaseGroup N → Role → V)
        (y : ArchiveRolePhaseGroup N) (r : Role),
        transformReferenceLeg h q y r = apply (h y) (q y r)

end D0.Geometry
