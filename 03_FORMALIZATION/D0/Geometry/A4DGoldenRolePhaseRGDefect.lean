import Mathlib.Data.Matrix.Basic
import D0.Geometry.ArchiveLaplacianRG
import D0.Geometry.ArchiveRolePhaseCarrier
import D0.Spectral.CanonicalRefinementScaleFlow

/-!
# Defect-bearing golden / Role-phase RG interface

The Role-phase projection is the coordinatewise one-dimensional map
`archiveRGPhaseProjection`. The golden value enters only as the scalar probe
`Λ_(k+1)/Λ_k`, where `k` is a Bratteli depth and `n` is a Role-phase period.
Those indices are separate arguments.

Zero operator residual is entrywise renormalized compatibility. Zero energy
residual is Dirichlet compatibility. The nearest-neighbor exact projective
failure stays a separate negative control and is not a theorem that the golden
residual never vanishes.

No Tower-C state, word, or measure is transported, and this file does not build
a located-star, Hodge-Dirac, or flux-energy intertwiner.
-/

namespace D0.Geometry

open D0
open D0.Spectral.CanonicalRefinementScaleFlow

/-- Scalar assignment `σ(k) = Λ_(k+1)/Λ_k` from the owned Perron scale flow.
The source is a depth index, not a Tower-C carrier. -/
noncomputable def goldenScaleProbe (k : ℕ) : ℝ :=
  Lambda (k + 1) / Lambda k

theorem goldenScaleProbe_eq_phi (k : ℕ) : goldenScaleProbe k = phi :=
  scale_ratio_forced k

/-- The probe is the same real number at every Bratteli depth. -/
theorem goldenScaleProbe_level_independent (k m : ℕ) :
    goldenScaleProbe k = goldenScaleProbe m := by
  rw [goldenScaleProbe_eq_phi, goldenScaleProbe_eq_phi]

/-- Literal coordinate bridge: each role coordinate uses `archiveRGPhaseProjection`. -/
theorem archiveRolePhaseProjection_eq_archiveRGPhaseProjection
    (n : ℕ) (x : ArchiveRolePhasePoint (n + 1)) (r : Role) :
    archiveRolePhaseProjection n x r = archiveRGPhaseProjection n (x r) := rfl

/-- Precomposition by a role relabelling commutes with the coordinatewise projection.
This is finite-set equivariance, not equivariance of a translation or cochain operator. -/
theorem archiveRolePhaseProjection_precomp
    (n : ℕ) (x : ArchiveRolePhasePoint (n + 1)) (σ : Role → Role) :
    archiveRolePhaseProjection n (x ∘ σ) = archiveRolePhaseProjection n x ∘ σ := by
  funext r
  rfl

theorem archiveRolePhaseProjection_perm
    (n : ℕ) (x : ArchiveRolePhasePoint (n + 1)) (σ : Equiv.Perm Role) :
    archiveRolePhaseProjection n (x ∘ σ) = archiveRolePhaseProjection n x ∘ σ :=
  archiveRolePhaseProjection_precomp n x σ

/-- Operator residual of an arbitrary phase comparison at the golden scalar probe. -/
noncomputable def goldenRGResidual (n k : ℕ)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    Matrix (archivePhaseIndex (n + 1)) (archivePhaseIndex (n + 1)) ℝ :=
  rgOperatorResidual n P (goldenScaleProbe k)

theorem goldenRGResidual_zero_iff (n k : ℕ)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    goldenRGResidual n k P = 0 ↔ RenormalizedProjectiveCompatibility n P phi := by
  unfold goldenRGResidual
  rw [goldenScaleProbe_eq_phi]
  exact rg_operator_curvature_zero_iff_renormalized_compatibility n P phi

/-- Generic scalar probe. `C` carries no Tower-C state; only `sigma c : ℝ` is used. -/
noncomputable def scalarAssignmentResidual {C : Type} (n : ℕ) (sigma : C → ℝ) (c : C)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    Matrix (archivePhaseIndex (n + 1)) (archivePhaseIndex (n + 1)) ℝ :=
  rgOperatorResidual n P (sigma c)

theorem scalarAssignmentResidual_zero_iff {C : Type} (n : ℕ) (sigma : C → ℝ) (c : C)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    scalarAssignmentResidual n sigma c P = 0 ↔
      RenormalizedProjectiveCompatibility n P (sigma c) :=
  rg_operator_curvature_zero_iff_renormalized_compatibility n P (sigma c)

theorem goldenRGResidual_eq_scalarAssignment (n k : ℕ)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    goldenRGResidual n k P = scalarAssignmentResidual n goldenScaleProbe k P := rfl

/-- Energy residual at the same scalar probe. It is not the operator residual. -/
noncomputable def goldenEnergyCorrection (n k : ℕ)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n)
    (f : archivePhaseIndex n → ℝ) : ℝ :=
  rgCurvatureCorrection n P (goldenScaleProbe k) f

theorem goldenEnergyCorrection_zero_iff (n k : ℕ)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    (∀ f, goldenEnergyCorrection n k P f = 0) ↔ ExactEnergyCompatibility n P phi := by
  unfold goldenEnergyCorrection
  rw [goldenScaleProbe_eq_phi]
  exact rg_curvature_zero_iff_exact_compatibility n P phi

noncomputable def scalarAssignmentEnergy {C : Type} (n : ℕ) (sigma : C → ℝ) (c : C)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n)
    (f : archivePhaseIndex n → ℝ) : ℝ :=
  rgCurvatureCorrection n P (sigma c) f

theorem scalarAssignmentEnergy_zero_iff {C : Type} (n : ℕ) (sigma : C → ℝ) (c : C)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    (∀ f, scalarAssignmentEnergy n sigma c P f = 0) ↔
      ExactEnergyCompatibility n P (sigma c) :=
  rg_curvature_zero_iff_exact_compatibility n P (sigma c)

/-- Both zero-residual equivalences, kept as a pair of distinct statements. -/
theorem operator_and_energy_zero_residuals (n k : ℕ)
    (P : archivePhaseIndex (n + 1) → archivePhaseIndex n) :
    (goldenRGResidual n k P = 0 ↔ RenormalizedProjectiveCompatibility n P phi) ∧
      ((∀ f, goldenEnergyCorrection n k P f = 0) ↔ ExactEnergyCompatibility n P phi) :=
  ⟨goldenRGResidual_zero_iff n k P, goldenEnergyCorrection_zero_iff n k P⟩

/-- Negative control for the literal nearest-neighbor prototype at scale `1`.
This does not say that `goldenRGResidual` is nonzero. -/
theorem nearestNeighbor_exactProjective_fails (n : ℕ) (hn : 1 < n) :
    ¬ ExactProjectiveCompatibility n (archiveRGPhaseProjection n) :=
  exact_projective_compatibility_fails n hn

end D0.Geometry
