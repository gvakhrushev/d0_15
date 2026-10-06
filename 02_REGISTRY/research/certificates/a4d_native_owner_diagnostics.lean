import Lean
import D0.Cosmology.FiniteFeedbackEquationOfState
import D0.Algebra.Sedenions
import D0.Geometry.ArchiveCubicalCochainCarrier
import D0.Geometry.ArchiveCubicalCoboundary
import D0.Geometry.Archive1DCochainRefinement
import D0.Geometry.ArchiveRefinementHodgeWeights
import D0.Geometry.ArchiveMetricMeasureHodgeLift
import D0.Geometry.ArchiveNaiveWeightedDegreeLeakageNoGo
import D0.Matter.MatterLocalizationNonuniquenessNoGo
import D0.Matter.ArchiveStressCoupling
import D0.Geometry.ArchiveVariation
import D0.Gravity.A4DParentWardStressDescent
import D0.Gravity.VariationalCarrierAudit
import D0.Geometry.SpectralActionAdmissibility
import D0.Geometry.ArchivePrimalDualMovingAction
import D0.Geometry.FinitePrimalDualHodgeParent
import D0.Geometry.A4DPathWordParentWard
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.ArchiveCovariantCubicalDifferential
import D0.Geometry.ArchiveGradedRefinementChainMap
import D0.Foundation.PhysicalComparisonRepresentation
import D0.Geometry.A4DLocatedMatterCellEnergy

open Lean Elab Command

elab "#audit_decl " requested:str : command => do
  let name := requested.getString.toName
  match (← getEnv).find? name with
  | none => logInfo m!"D0_AUDIT_MISSING {name}"
  | some info => logInfo m!"D0_AUDIT_BOUND {name} : {info.type}"

#audit_decl "D0.Cosmology.feedback_pressure_trace_log"
#audit_decl "D0.Algebra.Sedenions.sedenion_branch_threeset_scaffold_owner"
#audit_decl "D0.Algebra.Sedenions.triality_sedenion_s3_disjointness_guard"
#audit_decl "D0.Geometry.card_cubical_cochain_carrier"
#audit_decl "D0.Geometry.cubical_betti_sum_eq_sixteen"
#audit_decl "D0.Geometry.d_squared_eq_zero"
#audit_decl "D0.Geometry.b1_isometry"
#audit_decl "D0.Geometry.intertwining_d_b0_eq_b1_d"
#audit_decl "D0.Geometry.hodge_mass_trace_sum"
#audit_decl "D0.Geometry.metric_measure_hodge_lift_owner"
#audit_decl "D0.Geometry.archive_naive_weighted_degree_leakage_nogo_owner"
#audit_decl "D0.Matter.matter_neutrality_m1_forced"

#audit_decl "D0.Algebra.Sedenions.branch_label_s3_scaffold"
#audit_decl "D0.Algebra.Sedenions.bare_threeset_insufficient_for_sedenion_realization"
#audit_decl "D0.Geometry.archive_cubical_cochain_carrier_owner"
#audit_decl "D0.Geometry.total_betti_sum"
#audit_decl "D0.Geometry.archive_cubical_coboundary_owner"
#audit_decl "D0.Geometry.archive_1d_cochain_refinement_owner"
#audit_decl "D0.Geometry.total_hodge_gram_trace_sum_eq"
#audit_decl "D0.Geometry.archive_refinement_hodge_weights_owner"
#audit_decl "D0.Geometry.archive_metric_measure_hodge_lift_owner"
#audit_decl "D0.Geometry.archive_naive_weighted_car_degree_leakage_nogo_owner"
#audit_decl "D0.Matter.matter_localization_observable_canonicity_owner"
#audit_decl "D0.Matter.generated_matter_source_zero_if_anomaly_free"
#audit_decl "D0.Gravity.centeredRoleDivergence_zero_of_parentWard"
#audit_decl "D0.Gravity.VariationalCarrierAudit.gravity_variational_carrier_audit_owner"
#audit_decl "D0.d0_archive_satisfies_structural_admissibility"
#audit_decl "D0.Geometry.movingHodge_eq_self_iff_fixed"
#audit_decl "D0.Geometry.dForward_sq_zero"
#audit_decl "D0.Geometry.dConn_sq_eq_curvature"
#audit_decl "D0.Geometry.archive_graded_refinement_chain_map_owner"
#audit_decl "D0.Foundation.PhysicalComparisonRepresentation.physicalPrimitive_card_eq_two"
#audit_decl "D0.Geometry.locatedStar_does_not_select_reference_weight"
#audit_decl "D0.Geometry.mixedPrimalDualAction"

#print axioms D0.Cosmology.feedback_pressure_trace_log
#print axioms D0.Algebra.Sedenions.branch_label_s3_scaffold
#print axioms D0.Geometry.archive_cubical_cochain_carrier_owner
#print axioms D0.Geometry.archive_cubical_coboundary_owner
#print axioms D0.Geometry.archive_1d_cochain_refinement_owner
#print axioms D0.Geometry.archive_refinement_hodge_weights_owner
#print axioms D0.Geometry.archive_metric_measure_hodge_lift_owner
#print axioms D0.Geometry.archive_naive_weighted_car_degree_leakage_nogo_owner
#print axioms D0.Matter.matter_localization_observable_canonicity_owner
#print axioms D0.Matter.generated_matter_source_zero_if_anomaly_free
#print axioms D0.Gravity.centeredRoleDivergence_zero_of_parentWard
#print axioms D0.Gravity.VariationalCarrierAudit.gravity_variational_carrier_audit_owner
#print axioms D0.d0_archive_satisfies_structural_admissibility
#print axioms D0.Geometry.movingHodge_eq_self_iff_fixed
#print axioms D0.Geometry.dForward_sq_zero
#print axioms D0.Geometry.dConn_sq_eq_curvature
#print axioms D0.Geometry.archive_graded_refinement_chain_map_owner
#print axioms D0.Foundation.PhysicalComparisonRepresentation.physicalPrimitive_card_eq_two
#print axioms D0.Geometry.locatedStar_does_not_select_reference_weight
