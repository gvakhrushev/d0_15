import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveExteriorPathTransport
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DTransportedReferenceMismatch

/-!
# Conditional sourced diagonal transport (supplied 𝔍)

Lean-owns the conditional sourced diagonal transport package (PR #120 memo A–F).
Assumes a **supplied** comparison endomorphism `𝔍`; does not construct or select it.
-/

namespace D0.Geometry

open D0
open AffineCartanMap

/-- Local `LinearOrder Role` for this module only. -/
local instance conditionalSourcedDiagRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {N : ℕ}

/-- Supplied comparison endomorphism field `𝔍 : X → End(V)`. Not constructed. -/
abbrev ComparisonEndomorphismField (N : ℕ) :=
  ArchiveRolePhaseGroup N → (RoleSpace →ₗ[ℝ] RoleSpace)

/-- Predecessor site `x = y - r`. -/
def predecessorSite (N : ℕ) (r : Role) (y : ArchiveRolePhaseGroup N) :
    ArchiveRolePhaseGroup N :=
  roleTranslateMinus N r y

/-- Pulled predecessor shift `\bar b_r(y) = L_{x,r}^{-1} b_{x,r}`. -/
def barB (A : AffineCartanConnection N ℝ RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  let x := predecessorSite N r y
  (A x r).lin.symm (A x r).shift

/-- Pulled predecessor solder `\bar v_r(y) = L_{x,r}^{-1} v_r(e,x)`. -/
def barV (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  let x := predecessorSite N r y
  (A x r).lin.symm (solderLegVector N e x r)

/-- Source-fibre affine-shift increment `Δ^b_r(y) = b_{y,r} - \bar b_r(y)`. -/
def deltaB (A : AffineCartanConnection N ℝ RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  (A y r).shift - barB A y r

/-- Source-fibre solder increment `Δ^v_r(y) = v_r(e,y) - \bar v_r(y)`. -/
def deltaV (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  solderLegVector N e y r - barV A e y r

/-- Relative A/e defect `R^{A/e}_r = Δ^v_r - 𝔍_y Δ^b_r`. -/
def relativeDefect (A : AffineCartanConnection N ℝ RoleSpace)
    (e : LocalCoframeField N) (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  deltaV A e y r - J y (deltaB A y r)

/-- Finite diagonal seed `a_r = -\bar b_r - 𝔍_y Δ^b_r`. -/
def diagonalSeed (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  -barB A y r - J y (deltaB A y r)

/-- Tautological predecessor `ρ_r = A^{-1}_{x,r}(v_r(e,x)) - v_r(e,y)`. -/
def predecessorDefect (A : AffineCartanConnection N ℝ RoleSpace)
    (e : LocalCoframeField N) (y : ArchiveRolePhaseGroup N) (r : Role) :
    RoleSpace :=
  let x := predecessorSite N r y
  AffineCartanMap.apply ((A x r)⁻¹) (solderLegVector N e x r)
    - solderLegVector N e y r

/-- Path source `S_p = P_p a(y') - a(y)` with `P_p = covariantLin A p y`. -/
def pathSource (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (p : List ChainStep) (y : ArchiveRolePhaseGroup N) : RoleSpace :=
  let y' := pathEnd N p y
  covariantLin A p y (diagonalSeed A J y' r) - diagonalSeed A J y r

/-- Parallel residual `h := δ - a` along a supplied diagonal section `δ`. -/
def parallelResidual (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role) : RoleSpace :=
  δ y - diagonalSeed A J y r

/-! ## Exact expansions -/

theorem predecessorDefect_eq_barV_sub_barB
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    predecessorDefect A e y r =
      barV A e y r - barB A y r - solderLegVector N e y r := by
  simp only [predecessorDefect, barV, barB, AffineCartanMap.apply,
    AffineCartanMap.inv_lin, AffineCartanMap.inv_shift, map_neg, predecessorSite]
  abel

theorem diagonalSeed_eq
    (A : AffineCartanConnection N ℝ RoleSpace) (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    diagonalSeed A J y r = -barB A y r - J y (deltaB A y r) := rfl

theorem relativeDefect_eq
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N) (y : ArchiveRolePhaseGroup N) (r : Role) :
    relativeDefect A e J y r = deltaV A e y r - J y (deltaB A y r) := rfl

/-! ## 1. Relative increments are source typed + pure-linear covariance -/

/-- `Δ^b` lives in the source fibre `V_y` (definitional typing). -/
theorem deltaB_source_typed
    (A : AffineCartanConnection N ℝ RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    deltaB A y r = (A y r).shift - barB A y r := rfl

/-- `Δ^v` lives in the source fibre `V_y` (definitional typing). -/
theorem deltaV_source_typed
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    deltaV A e y r = solderLegVector N e y r - barV A e y r := rfl

/-- Under explicit pure-linear source-frame hypotheses, `Δ^b` transforms by `g`. -/
theorem deltaB_pureLinear_covariance
    (A A' : AffineCartanConnection N ℝ RoleSpace)
    (g : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role)
    (hy_shift : (A' y r).shift = g (A y r).shift)
    (hbar : barB A' y r = g (barB A y r)) :
    deltaB A' y r = g (deltaB A y r) := by
  simp only [deltaB, hy_shift, hbar, map_sub]

/-- Under explicit pure-linear source-frame hypotheses, `Δ^v` transforms by `g`. -/
theorem deltaV_pureLinear_covariance
    (A A' : AffineCartanConnection N ℝ RoleSpace)
    (e e' : LocalCoframeField N)
    (g : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role)
    (hv : solderLegVector N e' y r = g (solderLegVector N e y r))
    (hbarV : barV A' e' y r = g (barV A e y r)) :
    deltaV A' e' y r = g (deltaV A e y r) := by
  simp only [deltaV, hv, hbarV, map_sub]

/-- Packaged theorem 1: relative increments are source typed and transform by `g`
under the stated hypotheses. -/
theorem relative_increments_source_typed_covariant
    (A A' : AffineCartanConnection N ℝ RoleSpace)
    (e e' : LocalCoframeField N)
    (g : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role)
    (hy_shift : (A' y r).shift = g (A y r).shift)
    (hbar : barB A' y r = g (barB A y r))
    (hv : solderLegVector N e' y r = g (solderLegVector N e y r))
    (hbarV : barV A' e' y r = g (barV A e y r)) :
    deltaB A' y r = g (deltaB A y r) ∧
      deltaV A' e' y r = g (deltaV A e y r) :=
  ⟨deltaB_pureLinear_covariance A A' g y r hy_shift hbar,
    deltaV_pureLinear_covariance A A' e e' g y r hv hbarV⟩

/-! ## 2. Conditional relative defect covariance under conjugacy of 𝔍 -/

/-- If `𝔍' = g 𝔍 g⁻¹` and the increments transform by `g`, then `R' = g R`. -/
theorem relativeDefect_conjugacy_covariance
    (A A' : AffineCartanConnection N ℝ RoleSpace)
    (e e' : LocalCoframeField N)
    (J J' : ComparisonEndomorphismField N)
    (g : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role)
    (hJ : J' y = g.toLinearMap ∘ₗ J y ∘ₗ g.symm.toLinearMap)
    (hΔb : deltaB A' y r = g (deltaB A y r))
    (hΔv : deltaV A' e' y r = g (deltaV A e y r)) :
    relativeDefect A' e' J' y r = g (relativeDefect A e J y r) := by
  simp only [relativeDefect, hΔb, hΔv, hJ, LinearMap.comp_apply,
    LinearEquiv.coe_toLinearMap, LinearEquiv.symm_apply_apply, map_sub]

/-! ## 3. Gauge calibration -/

/-- If `𝔍_y Δ^b = Δ^v`, then `R^{A/e} = 0`. -/
theorem relativeDefect_gauge_calibration
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role)
    (hcal : J y (deltaB A y r) = deltaV A e y r) :
    relativeDefect A e J y r = 0 := by
  simp only [relativeDefect, hcal, sub_self]

/-! ## 4. Finite seed: source typed / covariant + exact expansion -/

theorem diagonalSeed_source_typed
    (A : AffineCartanConnection N ℝ RoleSpace) (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    diagonalSeed A J y r = -barB A y r - J y (deltaB A y r) := rfl

theorem diagonalSeed_pureLinear_covariance
    (A A' : AffineCartanConnection N ℝ RoleSpace)
    (J J' : ComparisonEndomorphismField N)
    (g : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (y : ArchiveRolePhaseGroup N) (r : Role)
    (hbar : barB A' y r = g (barB A y r))
    (hΔb : deltaB A' y r = g (deltaB A y r))
    (hJ : J' y = g.toLinearMap ∘ₗ J y ∘ₗ g.symm.toLinearMap) :
    diagonalSeed A' J' y r = g (diagonalSeed A J y r) := by
  simp only [diagonalSeed, hbar, hΔb, hJ, LinearMap.comp_apply,
    LinearEquiv.coe_toLinearMap, LinearEquiv.symm_apply_apply, map_neg, map_sub]

theorem diagonalSeed_exact_expansion
    (A : AffineCartanConnection N ℝ RoleSpace) (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    diagonalSeed A J y r =
      -barB A y r - J y ((A y r).shift - barB A y r) := by
  simp only [diagonalSeed, deltaB]

/-! ## 5. Predecessor decomposition: ρ = a − R -/

theorem predecessorDefect_eq_seed_sub_relativeDefect
    (A : AffineCartanConnection N ℝ RoleSpace) (e : LocalCoframeField N)
    (J : ComparisonEndomorphismField N)
    (y : ArchiveRolePhaseGroup N) (r : Role) :
    predecessorDefect A e y r =
      diagonalSeed A J y r - relativeDefect A e J y r := by
  simp only [predecessorDefect_eq_barV_sub_barB, diagonalSeed, relativeDefect,
    deltaB, deltaV]
  abel

/-! ## 6–8. Path source, append law, reverse law -/

theorem pathSource_eq
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (p : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    pathSource A J r p y =
      covariantLin A p y (diagonalSeed A J (pathEnd N p y) r)
        - diagonalSeed A J y r := rfl

/-- Append law: `S_{p++q} = S_p + P_p S_q` (repo `covariantLin_append` convention). -/
theorem pathSource_append
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (p q : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    pathSource A J r (p ++ q) y =
      pathSource A J r p y +
        covariantLin A p y (pathSource A J r q (pathEnd N p y)) := by
  simp only [pathSource, pathEnd_append, covariantLin_append, LinearEquiv.trans_apply,
    map_sub]
  abel

/-- Reverse law: `S_{\bar p} = - P_p^{-1} S_p`
(repo reverse = `map reverseStep` then `List.reverse`). -/
theorem pathSource_reverse
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (p : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    pathSource A J r ((p.map reverseStep).reverse) (pathEnd N p y) =
      - (covariantLin A p y).symm (pathSource A J r p y) := by
  simp only [pathSource, pathEnd_reverse, covariantLin_reverse, LinearEquiv.symm_apply_apply]
  -- Goal: P⁻¹ a(y) - a(y') = - P⁻¹ (P a(y') - a(y))
  have h :
      (covariantLin A p y).symm (diagonalSeed A J y r)
          - diagonalSeed A J (pathEnd N p y) r =
        -((covariantLin A p y).symm
            (covariantLin A p y (diagonalSeed A J (pathEnd N p y) r)
              - diagonalSeed A J y r)) := by
    simp only [map_sub, LinearEquiv.symm_apply_apply]
    abel
  exact h

/-! ## 9. Sourced solution characterization -/

/-- Along one labelled path: `P_p δ(y') - δ(y) = S_p` iff `h := δ - a` is parallel. -/
theorem sourced_solution_iff_parallel_along_path
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (p : List ChainStep) (y : ArchiveRolePhaseGroup N) :
    covariantLin A p y (δ (pathEnd N p y)) - δ y = pathSource A J r p y ↔
      covariantLin A p y (parallelResidual A J δ (pathEnd N p y) r) =
        parallelResidual A J δ y r := by
  simp only [pathSource, parallelResidual]
  constructor
  · intro h
    have h' :
        covariantLin A p y (δ (pathEnd N p y))
            - covariantLin A p y (diagonalSeed A J (pathEnd N p y) r) =
          δ y - diagonalSeed A J y r := by
      linear_combination h
    simpa [map_sub] using h'
  · intro h
    have h' :
        covariantLin A p y (δ (pathEnd N p y) - diagonalSeed A J (pathEnd N p y) r) =
          δ y - diagonalSeed A J y r := h
    simp only [map_sub] at h'
    linear_combination h'

/-- Lift: the sourced equation holds for all labelled paths iff `h` is parallel
along every labelled path. -/
theorem sourced_solution_iff_parallel_all_paths
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace) :
    (∀ p y, covariantLin A p y (δ (pathEnd N p y)) - δ y =
        pathSource A J r p y) ↔
      (∀ p y,
        covariantLin A p y (parallelResidual A J δ (pathEnd N p y) r) =
          parallelResidual A J δ y r) := by
  constructor
  · intro h p y
    exact (sourced_solution_iff_parallel_along_path A J r δ p y).mp (h p y)
  · intro h p y
    exact (sourced_solution_iff_parallel_along_path A J r δ p y).mpr (h p y)

/-! ## 10. Loop kernel (no new basepoint selector) -/

/-- For a basepoint loop `γ` (`pathEnd γ o = o`), parallel `h` is fixed:
`P_γ h(o) = h(o)`. -/
theorem parallelResidual_loop_fixed
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (γ : List ChainStep) (o : ArchiveRolePhaseGroup N)
    (hloop : pathEnd N γ o = o)
    (hpar :
      covariantLin A γ o (parallelResidual A J δ (pathEnd N γ o) r) =
        parallelResidual A J δ o r) :
    covariantLin A γ o (parallelResidual A J δ o r) =
      parallelResidual A J δ o r := by
  simpa [hloop] using hpar

/-- Packaged loop kernel: if the sourced law holds for the loop, then
`P_γ h(o) = h(o)`. -/
theorem sourced_loop_kernel
    (A : AffineCartanConnection N ℝ RoleSpace)
    (J : ComparisonEndomorphismField N) (r : Role)
    (δ : ArchiveRolePhaseGroup N → RoleSpace)
    (γ : List ChainStep) (o : ArchiveRolePhaseGroup N)
    (hloop : pathEnd N γ o = o)
    (hsrc :
      covariantLin A γ o (δ (pathEnd N γ o)) - δ o = pathSource A J r γ o) :
    covariantLin A γ o (parallelResidual A J δ o r) =
      parallelResidual A J δ o r := by
  have hpar := (sourced_solution_iff_parallel_along_path A J r δ γ o).mp hsrc
  exact parallelResidual_loop_fixed A J r δ γ o hloop hpar

end

end D0.Geometry
