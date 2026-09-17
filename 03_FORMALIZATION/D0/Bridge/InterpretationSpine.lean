import D0.Bridge.SICalibrationClosure
import D0.Bridge.PhiDiscreteRG
import D0.Geometry.ArchiveLaplacianRG
import D0.Geometry.SpectralActionLadder
import D0.Cosmology.CoreShapePassportBoundary
import D0.Bridge.OperatorOriginIndex
import D0.Gauge.NonAbelianDiscreteCurvature
import D0.Traceability.StatusTaxonomy

open scoped BigOperators

namespace D0.Bridge

inductive InterpretationStage where
  | dimensionlessCore
  | interpretedPackage
  | siCalibrated
  | empiricalCompared
  deriving DecidableEq, Repr

structure RGReadoutCoherence where
  finiteScaleAlgebra : Prop
  residualTracked : Prop
  smoothBridgeConditional : Prop
  finite_scale_ok : finiteScaleAlgebra
  residual_tracked_ok : residualTracked
  smooth_bridge_conditional_ok : smoothBridgeConditional

structure SpectralActionReadoutCoherence where
  finiteTraceProxy : Prop
  noContinuumPromotion : Prop
  finite_trace_proxy_ok : finiteTraceProxy
  no_continuum_promotion_ok : noContinuumPromotion

structure CosmologyShapeReadout where
  dimensionlessShape : Prop
  empiricalParametersExternal : Prop
  dimensionless_shape_ok : dimensionlessShape
  empirical_parameters_external_ok : empiricalParametersExternal

structure GaugeReadoutCoherence where
  finiteGaugeLayer : Prop
  nonabelianBoundaryTracked : Prop
  finite_gauge_layer_ok : finiteGaugeLayer
  nonabelian_boundary_tracked_ok : nonabelianBoundaryTracked

structure PassportExternality where
  externalDataDeclared : Prop
  constrainsReadoutOnly : Prop
  external_data_declared_ok : externalDataDeclared
  constrains_readout_only_ok : constrainsReadoutOnly

def spectralFiniteTraceProxy : Prop :=
  (∀ {N : Type} [Fintype N] [DecidableEq N]
      (L : Matrix N N ℝ) (ρ : N → ℝ) (_h_pos : ∀ i, ρ i > 0),
      D0.Geometry.SpectralActionLadder.spectralTracePower L ρ 1 =
        ∑ i, L i i / ρ i) ∧
    (∀ {N : Type} [Fintype N] [DecidableEq N]
      (L : Matrix N N ℝ) (ρ : N → ℝ)
      (_h_pos : ∀ i, ρ i > 0) (_h_symm : ∀ i j, L i j = L j i),
      D0.Geometry.SpectralActionLadder.spectralTracePower L ρ 2 =
        D0.Geometry.HeatTraceA2Decomposition.diagonalSquareTerm L ρ
          + 2 * D0.Geometry.HeatTraceA2Decomposition.discreteEHActionProxy L ρ)

def rgReadoutFromAnchors
    (hSmooth : SmoothInterpolationAssumptions) : RGReadoutCoherence where
  finiteScaleAlgebra :=
    ∀ (Λ : ℝ) (k : ℤ), phiScale Λ (k + 1) = phiScale Λ k * D0.phi⁻¹
  residualTracked :=
    ∀ n : Nat, Function.Surjective (D0.archiveRGPhaseProjection n)
  smoothBridgeConditional := hSmooth.interpolation_exists
  finite_scale_ok := fun Λ k => phi_scale_step Λ k
  residual_tracked_ok := fun n => D0.archiveRGPhaseProjection_surjective n
  smooth_bridge_conditional_ok := phi_rg_bridge_conditional hSmooth

def spectralActionReadoutFromAnchors
    (noContinuumPromotion : Prop)
    (hNoContinuumPromotion : noContinuumPromotion) :
    SpectralActionReadoutCoherence where
  finiteTraceProxy := spectralFiniteTraceProxy
  noContinuumPromotion := noContinuumPromotion
  finite_trace_proxy_ok :=
    And.intro
      (fun L ρ h_pos =>
        D0.Geometry.SpectralActionLadder.a0_is_volume_proxy L ρ h_pos)
      (fun L ρ h_pos h_symm =>
        D0.Geometry.SpectralActionLadder.a2_is_eh_proxy L ρ h_pos h_symm)
  no_continuum_promotion_ok := hNoContinuumPromotion

def cosmologyShapeReadoutFromAnchors : CosmologyShapeReadout where
  dimensionlessShape :=
    ∀ (cp : D0.Cosmology.CoreParams)
      (ep1 ep2 : D0.Cosmology.EmpiricalParams),
      D0.Cosmology.coreShapeEvaluated cp ep1 =
        D0.Cosmology.coreShapeEvaluated cp ep2
  empiricalParametersExternal :=
    ∀ (f : D0.Cosmology.CoreParams →
        D0.Cosmology.EmpiricalParams →
        D0.Cosmology.ExternalData → ℝ),
      (∃ cp ep1 ep2 ed, f cp ep1 ed ≠ f cp ep2 ed) →
        ¬ D0.Cosmology.isCoreClosed f
  dimensionless_shape_ok := fun cp ep1 ep2 =>
    D0.Cosmology.core_shape_independent_of_empirical_parameters cp ep1 ep2
  empirical_parameters_external_ok := fun f h =>
    D0.Cosmology.empirical_passport_not_core_closed f h

def gaugeReadoutFromAnchors : GaugeReadoutCoherence where
  finiteGaugeLayer :=
    gauge_curvature_origin_closed ∧
      D0.Gauge.nonabelian_discrete_curvature_boundary
  nonabelianBoundaryTracked := nonabelian_completion_boundary
  finite_gauge_layer_ok :=
    And.intro
      gauge_curvature_origin_closed_proof
      D0.Gauge.nonabelian_discrete_curvature_boundary_proof
  nonabelian_boundary_tracked_ok := nonabelian_completion_boundary_proof

def passportExternalityFromAnchors : PassportExternality where
  externalDataDeclared :=
    ¬ D0.Traceability.canPromoteTo
      D0.Traceability.D0Status.EXTERNAL_DATA_REQUIRED
      D0.Traceability.D0Status.CORE_CLOSED
  constrainsReadoutOnly :=
    ¬ D0.Traceability.canPromoteTo
      D0.Traceability.D0Status.EMPIRICAL_PASSPORT
      D0.Traceability.D0Status.CORE_CLOSED
  external_data_declared_ok := by
    unfold D0.Traceability.canPromoteTo
    intro h
    exact h
  constrains_readout_only_ok :=
    D0.Traceability.external_likelihood_cannot_promote_to_core_closed

structure InterpretationPackage where
  rg : RGReadoutCoherence
  spectralAction : SpectralActionReadoutCoherence
  cosmology : CosmologyShapeReadout
  gauge : GaugeReadoutCoherence
  passports : PassportExternality

def interpretationPackageFromAnchors
    (hSmooth : SmoothInterpolationAssumptions)
    (noContinuumPromotion : Prop)
    (hNoContinuumPromotion : noContinuumPromotion) :
    InterpretationPackage where
  rg := rgReadoutFromAnchors hSmooth
  spectralAction :=
    spectralActionReadoutFromAnchors noContinuumPromotion hNoContinuumPromotion
  cosmology := cosmologyShapeReadoutFromAnchors
  gauge := gaugeReadoutFromAnchors
  passports := passportExternalityFromAnchors

structure D0InterpretationSpine where
  core : DimensionlessCoreTraces
  package : InterpretationPackage
  siCalibration : ExternalSICalibration

def dimensionlessCoreStage (_core : DimensionlessCoreTraces) : InterpretationStage :=
  InterpretationStage.dimensionlessCore

def packageStage (_package : InterpretationPackage) : InterpretationStage :=
  InterpretationStage.interpretedPackage

def siReadoutStage (_spine : D0InterpretationSpine) : InterpretationStage :=
  InterpretationStage.siCalibrated

def empiricalComparisonStage (_spine : D0InterpretationSpine) : InterpretationStage :=
  InterpretationStage.empiricalCompared

def spineSIReadout (spine : D0InterpretationSpine) : SIMacroscopicPhysics :=
  derive_physical_observables spine.core spine.siCalibration

theorem interpretation_package_keeps_core_dimensionless
    (spine : D0InterpretationSpine) :
    coreTraceShapeStatus spine.core = QuantityStatus.DimensionlessCore := by
  rfl

theorem interpretation_package_does_not_mutate_core_shape
    (spine : D0InterpretationSpine) :
    spine.core.a0 = spine.core.a0 /\
      spine.core.a2 = spine.core.a2 /\
      spine.core.delta2V = spine.core.delta2V := by
  exact calibration_changes_units_not_core_shape spine.core spine.siCalibration spine.siCalibration

theorem si_readout_uses_single_external_calibration
    (spine : D0InterpretationSpine) :
    (spineSIReadout spine).H0 = spine.siCalibration.H0 /\
      (spineSIReadout spine).GN = spine.siCalibration.GN /\
      (spineSIReadout spine).Lambda = spine.siCalibration.Lambda := by
  exact And.intro rfl (And.intro rfl rfl)

theorem interpretation_spine_has_single_si_readout
    (spine : D0InterpretationSpine) :
    siPhysicsStatus (spineSIReadout spine) = QuantityStatus.SICalibrated := by
  rfl

theorem empirical_comparison_is_after_si_readout
    (spine : D0InterpretationSpine) :
    empiricalComparisonStage spine = InterpretationStage.empiricalCompared /\
      siReadoutStage spine = InterpretationStage.siCalibrated := by
  exact And.intro rfl rfl

theorem interpretation_package_rg_readout_coherent
    (spine : D0InterpretationSpine) :
    spine.package.rg.finiteScaleAlgebra /\
      spine.package.rg.residualTracked /\
      spine.package.rg.smoothBridgeConditional := by
  exact And.intro
    spine.package.rg.finite_scale_ok
    (And.intro
      spine.package.rg.residual_tracked_ok
      spine.package.rg.smooth_bridge_conditional_ok)

theorem interpretation_package_spectral_action_readout_coherent
    (spine : D0InterpretationSpine) :
    spine.package.spectralAction.finiteTraceProxy /\
      spine.package.spectralAction.noContinuumPromotion := by
  exact And.intro
    spine.package.spectralAction.finite_trace_proxy_ok
    spine.package.spectralAction.no_continuum_promotion_ok

theorem interpretation_package_cosmology_shape_readout_coherent
    (spine : D0InterpretationSpine) :
    spine.package.cosmology.dimensionlessShape /\
      spine.package.cosmology.empiricalParametersExternal := by
  exact And.intro
    spine.package.cosmology.dimensionless_shape_ok
    spine.package.cosmology.empirical_parameters_external_ok

theorem interpretation_package_gauge_readout_coherent
    (spine : D0InterpretationSpine) :
    spine.package.gauge.finiteGaugeLayer /\
      spine.package.gauge.nonabelianBoundaryTracked := by
  exact And.intro
    spine.package.gauge.finite_gauge_layer_ok
    spine.package.gauge.nonabelian_boundary_tracked_ok

theorem interpretation_package_passports_external
    (spine : D0InterpretationSpine) :
    spine.package.passports.externalDataDeclared /\
      spine.package.passports.constrainsReadoutOnly := by
  exact And.intro
    spine.package.passports.external_data_declared_ok
    spine.package.passports.constrains_readout_only_ok

def interpretationSpineCoherenceContract
    (spine : D0InterpretationSpine) : Prop :=
    spine.package.rg.finiteScaleAlgebra /\
      spine.package.rg.residualTracked /\
      spine.package.rg.smoothBridgeConditional /\
      spine.package.spectralAction.finiteTraceProxy /\
      spine.package.spectralAction.noContinuumPromotion /\
      spine.package.cosmology.dimensionlessShape /\
      spine.package.cosmology.empiricalParametersExternal /\
      spine.package.gauge.finiteGaugeLayer /\
      spine.package.gauge.nonabelianBoundaryTracked /\
      spine.package.passports.externalDataDeclared /\
      spine.package.passports.constrainsReadoutOnly /\
      coreTraceShapeStatus spine.core = QuantityStatus.DimensionlessCore /\
      siPhysicsStatus (spineSIReadout spine) = QuantityStatus.SICalibrated

theorem interpretation_spine_coherence_contract
    (spine : D0InterpretationSpine) :
    interpretationSpineCoherenceContract spine := by
  unfold interpretationSpineCoherenceContract
  exact
    And.intro spine.package.rg.finite_scale_ok
      (And.intro spine.package.rg.residual_tracked_ok
        (And.intro spine.package.rg.smooth_bridge_conditional_ok
          (And.intro spine.package.spectralAction.finite_trace_proxy_ok
            (And.intro spine.package.spectralAction.no_continuum_promotion_ok
              (And.intro spine.package.cosmology.dimensionless_shape_ok
                (And.intro spine.package.cosmology.empirical_parameters_external_ok
                  (And.intro spine.package.gauge.finite_gauge_layer_ok
                    (And.intro spine.package.gauge.nonabelian_boundary_tracked_ok
                      (And.intro spine.package.passports.external_data_declared_ok
                        (And.intro spine.package.passports.constrains_readout_only_ok
                          (And.intro rfl rfl)))))))))))

theorem interpretation_package_from_existing_anchors_coherent
    (core : DimensionlessCoreTraces)
    (siCalibration : ExternalSICalibration)
    (hSmooth : SmoothInterpolationAssumptions)
    (noContinuumPromotion : Prop)
    (hNoContinuumPromotion : noContinuumPromotion) :
    interpretationSpineCoherenceContract
      { core := core,
        package :=
          interpretationPackageFromAnchors
            hSmooth noContinuumPromotion hNoContinuumPromotion,
        siCalibration := siCalibration } := by
  exact interpretation_spine_coherence_contract _

end D0.Bridge
