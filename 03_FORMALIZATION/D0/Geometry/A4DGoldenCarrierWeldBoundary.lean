import D0.Geometry.A4DGoldenRolePhaseRGDefect
import D0.Geometry.ArchiveFlatProductBondingNoGo
import D0.Geometry.ArchiveTwoLimitSeparation
import D0.Geometry.ArchiveRolePhaseProductCarrier

/-!
# Carrier-weld boundary for the golden RG interface

Tower A record bonding and Tower B role-phase bonding remain the owned `6 ≠ 16`
separation. Tower C contributes the scalar probe `goldenScaleProbe`, whose
source is a depth index. The supplied comparison package has fields only for a
period, a Bratteli depth, a finite-set comparison, and a scalar assignment.
It does not instantiate a carrier map, a located star, a Hodge-Dirac intertwiner,
or a flux-energy transport.
-/

namespace D0.Geometry

open D0
open D0.Geometry.ArchiveFlatProductBondingNoGo
open D0.Geometry.ArchiveTwoLimitSeparation
open D0.Geometry.ArchiveRolePhaseProductCarrier

/-- Supplied data `(period, depth, comparison, sigma, probe)`.
`period` and `bratteliDepth` are independent. `sigma` transports a real number only. -/
structure SuppliedScalarDefectPackage (C : Type) where
  period : ℕ
  bratteliDepth : ℕ
  comparison : archivePhaseIndex (period + 1) → archivePhaseIndex period
  sigma : C → ℝ
  probe : C

noncomputable def suppliedOperatorResidual {C : Type} (S : SuppliedScalarDefectPackage C) :
    Matrix (archivePhaseIndex (S.period + 1)) (archivePhaseIndex (S.period + 1)) ℝ :=
  rgOperatorResidual S.period S.comparison (S.sigma S.probe)

theorem suppliedOperatorResidual_zero_iff {C : Type} (S : SuppliedScalarDefectPackage C) :
    suppliedOperatorResidual S = 0 ↔
      RenormalizedProjectiveCompatibility S.period S.comparison (S.sigma S.probe) :=
  rg_operator_curvature_zero_iff_renormalized_compatibility
    S.period S.comparison (S.sigma S.probe)

/-- The two role-phase point abbrevs are the same function type `Role → archivePhaseIndex n`. -/
theorem rolePhasePoint_carriers_agree (n : ℕ) :
    D0.ArchiveRolePhasePoint n =
      D0.Geometry.ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint n := rfl

theorem record_rolePhase_firstStep_fibers :
    flatZeroFiber.card = 6 ∧ productZeroFiberCard = 16 :=
  ⟨card_flat_zero_fiber, product_zero_fiber_card_eq_sixteen⟩

theorem record_rolePhase_bonding_separation :
    flatZeroFiber.card ≠ productZeroFiberCard :=
  flat_ne_product_fiber_card

theorem record_rolePhase_two_limit_separation :
    DefinesProfiniteObject archiveProfiniteSystem ∧
      flatZeroFiber.card = 6 ∧
      productZeroFiberCard = 16 ∧
      flatZeroFiber.card ≠ productZeroFiberCard :=
  archive_two_limit_separation_owner

theorem towerC_scale_probe_eq_phi (k : ℕ) : goldenScaleProbe k = phi :=
  goldenScaleProbe_eq_phi k

end D0.Geometry
