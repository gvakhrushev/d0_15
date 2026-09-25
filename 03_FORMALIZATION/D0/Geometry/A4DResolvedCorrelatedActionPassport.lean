import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Tactic
import D0.Geometry.A4DRelativeAEComparisonSpan

/-!
# Resolved correlated-action passport

Lean owner for the finite-dimensional algebraic resolved correlated-action
passport isolated by research PR #130
(`MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md`, §§27–32).

Given synthesis maps `B, S : LabelCoeff →ₗ[ℝ] V`, ComparisonSpan already owns

* `K = coefficientKernel B`, `H = coefficientComplement B`,
* canonical correlated action `C = canonicalOnCoeff B S = S ∘ P_H`,
* residual action `D = canonicalResidual B S = S ∘ P_K`,
* and the exact split coming from `id = P_H + P_K`.

An admissible orthogonal resolution lift remembers a lost-direction subspace
`W ≤ K` and uses the incidence projector `Π = P_H + P_W`. The resolved
correlated action is `S ∘ Π`. This module owns the exact identities

* `B ∘ (P_H + P_W) = B`,
* `S ∘ Π - C = D ∘ P_W`,
* intrinsic / maximal specializations,
* Role-residual form of the maximal jump,
* exact-gauge invisibility of the lift,
* coframe-only intrinsic/maximal separation,

and nothing about topology, limits, or sequence continuity.
-/

namespace D0.Geometry.A4DResolvedCorrelatedActionPassport

open D0.Geometry.A4DRelativeAEComparisonSpan
open scoped InnerProductSpace

noncomputable section

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-! ## Projectors and resolved action -/

/-- Orthogonal projector onto a lost-direction subspace `W`. -/
def lostDirectionProjector (W : Submodule ℝ LabelCoeff) :
    LabelCoeff →ₗ[ℝ] LabelCoeff :=
  W.starProjection.toLinearMap

/-- Admissible orthogonal resolution projector `Π = P_H + P_W` for `W ≤ K`. -/
def resolutionProjector (B : LabelCoeff →ₗ[ℝ] V)
    (W : Submodule ℝ LabelCoeff) : LabelCoeff →ₗ[ℝ] LabelCoeff :=
  coefficientRepresentative B + lostDirectionProjector W

/-- Resolved correlated action `Ĉ = S ∘ Π`. -/
def resolvedCorrelatedAction (_B S : LabelCoeff →ₗ[ℝ] V)
    (proj : LabelCoeff →ₗ[ℝ] LabelCoeff) : LabelCoeff →ₗ[ℝ] V :=
  S.comp proj

/-- Role residual seed `R_r = D (EuclideanSpace.single r 1)`. -/
def roleResidual (B S : LabelCoeff →ₗ[ℝ] V) (r : Role) : V :=
  canonicalResidual B S (EuclideanSpace.single r 1)

/-! ## Incidence and jump identities -/

theorem B_lostDirectionProjector
    (B : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) (c : LabelCoeff) :
    B (lostDirectionProjector W c) = 0 := by
  have hc : lostDirectionProjector W c ∈ W := by
    simpa [lostDirectionProjector] using Submodule.starProjection_apply_mem W c
  exact LinearMap.mem_ker.mp (hW hc)

theorem B_resolutionProjector
    (B : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) (c : LabelCoeff) :
    B (resolutionProjector B W c) = B c := by
  simp [resolutionProjector, map_add, B_coefficientRepresentative,
    B_lostDirectionProjector B W hW]

theorem B_comp_resolutionProjector
    (B : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) :
    B.comp (resolutionProjector B W) = B := by
  ext c
  exact B_resolutionProjector B W hW c

theorem lostDirectionProjector_eq_kernelComponent_comp
    (B : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) (c : LabelCoeff) :
    lostDirectionProjector W c =
      kernelComponent B (lostDirectionProjector W c) := by
  have hc : lostDirectionProjector W c ∈ coefficientKernel B :=
    hW (by simpa [lostDirectionProjector] using Submodule.starProjection_apply_mem W c)
  have hPH :
      coefficientRepresentative B (lostDirectionProjector W c) = 0 :=
    coefficientRepresentative_eq_zero_of_mem_kernel B hc
  simp [kernelComponent, hPH]

theorem S_lostDirectionProjector_eq_residual
    (B S : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) (c : LabelCoeff) :
    S (lostDirectionProjector W c) =
      canonicalResidual B S (lostDirectionProjector W c) := by
  rw [canonicalResidual, LinearMap.comp_apply,
    ← lostDirectionProjector_eq_kernelComponent_comp B W hW]

/-- Main jump identity: `Ĉ - C = D ∘ P_W`. -/
theorem resolvedCorrelatedAction_sub_canonical
    (B S : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) :
    resolvedCorrelatedAction B S (resolutionProjector B W) -
        canonicalOnCoeff B S =
      (canonicalResidual B S).comp (lostDirectionProjector W) := by
  ext c
  have hS := S_lostDirectionProjector_eq_residual B S W hW c
  simp [resolvedCorrelatedAction, resolutionProjector, canonicalOnCoeff,
    map_add, LinearMap.sub_apply, LinearMap.comp_apply, hS]

theorem resolvedCorrelatedAction_sub_canonical_apply
    (B S : LabelCoeff →ₗ[ℝ] V) (W : Submodule ℝ LabelCoeff)
    (hW : W ≤ coefficientKernel B) (c : LabelCoeff) :
    resolvedCorrelatedAction B S (resolutionProjector B W) c -
        canonicalOnCoeff B S c =
      canonicalResidual B S (lostDirectionProjector W c) := by
  simpa [LinearMap.sub_apply, LinearMap.comp_apply] using
    congrArg (fun f : LabelCoeff →ₗ[ℝ] V => f c)
      (resolvedCorrelatedAction_sub_canonical B S W hW)

/-! ## Intrinsic and maximal lifts -/

/-- Intrinsic lift: `W = ⊥` recovers the canonical correlated action. -/
theorem resolvedCorrelatedAction_intrinsic
    (B S : LabelCoeff →ₗ[ℝ] V) :
    resolvedCorrelatedAction B S
        (resolutionProjector B (⊥ : Submodule ℝ LabelCoeff)) =
      canonicalOnCoeff B S := by
  have hW : (⊥ : Submodule ℝ LabelCoeff) ≤ coefficientKernel B := bot_le
  ext c
  have hjump := resolvedCorrelatedAction_sub_canonical_apply B S ⊥ hW c
  have hP : lostDirectionProjector (⊥ : Submodule ℝ LabelCoeff) c = 0 := by
    simp [lostDirectionProjector]
  simpa [hP, sub_eq_zero] using hjump

private theorem resolutionProjector_maximal_apply
    (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    resolutionProjector B (coefficientKernel B) c = c := by
  -- P_H + P_K = id
  change
      (coefficientComplement B).starProjection c +
        (coefficientKernel B).starProjection c = c
  simpa [coefficientComplement, coefficientKernel, add_comm] using
    (Submodule.starProjection_add_starProjection_orthogonal
      (K := LinearMap.ker B) c)

/-- Maximal lift: `W = K` yields `Π = id`, so `Ĉ = S`. -/
theorem resolvedCorrelatedAction_maximal
    (B S : LabelCoeff →ₗ[ℝ] V) :
    resolvedCorrelatedAction B S
        (resolutionProjector B (coefficientKernel B)) =
      S := by
  ext c
  simp [resolvedCorrelatedAction, resolutionProjector_maximal_apply]

/-- Maximal jump equals the residual action `D`. -/
theorem resolvedCorrelatedAction_maximal_sub_canonical
    (B S : LabelCoeff →ₗ[ℝ] V) :
    resolvedCorrelatedAction B S
        (resolutionProjector B (coefficientKernel B)) -
        canonicalOnCoeff B S =
      canonicalResidual B S := by
  rw [resolvedCorrelatedAction_maximal]
  ext c
  simp [canonicalOnCoeff, canonicalResidual, kernelComponent, map_sub,
    LinearMap.sub_apply, LinearMap.comp_apply]

/-! ## Role residual specialization -/

theorem roleResidual_maximal_jump
    (B S : LabelCoeff →ₗ[ℝ] V) (r : Role) :
    resolvedCorrelatedAction B S
        (resolutionProjector B (coefficientKernel B))
        (EuclideanSpace.single r 1) -
      canonicalOnCoeff B S (EuclideanSpace.single r 1) =
      roleResidual B S r := by
  simpa [roleResidual, LinearMap.sub_apply] using
    congrArg (fun f : LabelCoeff →ₗ[ℝ] V => f (EuclideanSpace.single r 1))
      (resolvedCorrelatedAction_maximal_sub_canonical B S)

/-! ## Exact-gauge invisibility -/

theorem resolvedCorrelatedAction_exact_gauge
    (B : LabelCoeff →ₗ[ℝ] V) (T : V →ₗ[ℝ] V)
    (proj : LabelCoeff →ₗ[ℝ] LabelCoeff)
    (hProj : B.comp proj = B) :
    resolvedCorrelatedAction B (T.comp B) proj = T.comp B := by
  ext c
  have hB : B (proj c) = B c := by
    simpa [LinearMap.comp_apply] using
      congrArg (fun f : LabelCoeff →ₗ[ℝ] V => f c) hProj
  simp [resolvedCorrelatedAction, hB]

theorem resolvedCorrelatedAction_exact_gauge_resolution
    (B : LabelCoeff →ₗ[ℝ] V) (T : V →ₗ[ℝ] V)
    (W : Submodule ℝ LabelCoeff) (hW : W ≤ coefficientKernel B) :
    resolvedCorrelatedAction B (T.comp B) (resolutionProjector B W) =
      T.comp B :=
  resolvedCorrelatedAction_exact_gauge B T _
    (B_comp_resolutionProjector B W hW)

/-! ## Coframe-only boundary `B = 0` -/

theorem coefficientRepresentative_zero :
    coefficientRepresentative (0 : LabelCoeff →ₗ[ℝ] V) = 0 := by
  ext c
  -- ker 0 = ⊤ ⇒ (ker 0)ᗮ = ⊥ ⇒ starProjection = 0
  simp [coefficientRepresentative, coefficientComplement, coefficientKernel]

theorem resolutionProjector_zero_intrinsic :
    resolutionProjector (0 : LabelCoeff →ₗ[ℝ] V)
      (⊥ : Submodule ℝ LabelCoeff) = 0 := by
  ext c
  simp [resolutionProjector, coefficientRepresentative_zero, lostDirectionProjector]

theorem resolvedCorrelatedAction_zero_B_intrinsic
    (S : LabelCoeff →ₗ[ℝ] V) :
    resolvedCorrelatedAction (0 : LabelCoeff →ₗ[ℝ] V) S
        (resolutionProjector (0 : LabelCoeff →ₗ[ℝ] V)
          (⊥ : Submodule ℝ LabelCoeff)) = 0 := by
  rw [resolutionProjector_zero_intrinsic]
  ext c
  simp [resolvedCorrelatedAction]

theorem coefficientKernel_zero :
    coefficientKernel (0 : LabelCoeff →ₗ[ℝ] V) = ⊤ := by
  simp [coefficientKernel]

theorem resolutionProjector_zero_maximal (c : LabelCoeff) :
    resolutionProjector (0 : LabelCoeff →ₗ[ℝ] V) ⊤ c = c := by
  have htop : (⊤ : Submodule ℝ LabelCoeff).starProjection c = c :=
    Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_top : c ∈ (⊤ : Submodule ℝ LabelCoeff))
  simp [resolutionProjector, lostDirectionProjector, coefficientRepresentative_zero, htop]

theorem resolvedCorrelatedAction_zero_B_maximal
    (S : LabelCoeff →ₗ[ℝ] V) :
    resolvedCorrelatedAction (0 : LabelCoeff →ₗ[ℝ] V) S
        (resolutionProjector (0 : LabelCoeff →ₗ[ℝ] V)
          (coefficientKernel (0 : LabelCoeff →ₗ[ℝ] V))) =
      S := by
  rw [coefficientKernel_zero]
  ext c
  simp [resolvedCorrelatedAction, resolutionProjector_zero_maximal]

/-! ## Hostile controls -/

/-- Nonzero residual yields a distinct maximal resolved action. -/
theorem maximal_ne_canonical_of_residual_ne_zero
    (B S : LabelCoeff →ₗ[ℝ] V) (hD : canonicalResidual B S ≠ 0) :
    resolvedCorrelatedAction B S
        (resolutionProjector B (coefficientKernel B)) ≠
      canonicalOnCoeff B S := by
  intro h
  apply hD
  have hsub := resolvedCorrelatedAction_maximal_sub_canonical B S
  simpa [h, sub_eq_zero, eq_comm] using hsub

/-- Coframe-only: intrinsic and maximal resolutions differ when `S ≠ 0`. -/
theorem zero_B_intrinsic_ne_maximal
    (S : LabelCoeff →ₗ[ℝ] V) (hS : S ≠ 0) :
    resolvedCorrelatedAction (0 : LabelCoeff →ₗ[ℝ] V) S
        (resolutionProjector (0 : LabelCoeff →ₗ[ℝ] V)
          (⊥ : Submodule ℝ LabelCoeff)) ≠
      resolvedCorrelatedAction (0 : LabelCoeff →ₗ[ℝ] V) S
        (resolutionProjector (0 : LabelCoeff →ₗ[ℝ] V)
          (coefficientKernel (0 : LabelCoeff →ₗ[ℝ] V))) := by
  rw [resolvedCorrelatedAction_zero_B_intrinsic,
    resolvedCorrelatedAction_zero_B_maximal]
  exact Ne.symm hS

end

end D0.Geometry.A4DResolvedCorrelatedActionPassport
