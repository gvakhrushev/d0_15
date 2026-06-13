namespace D0

inductive ClaimStatus where
  | leanCoreProved
  | leanBridgeAssumptionsExplicit
  | pythonCertRequired
  | pythonCertClosed
  | empiricalDataRequired
  | leanNoGoProved
  | openObligation
  | deprecated
  | notInLeanScope
  deriving DecidableEq, Repr

structure ClaimMapEntry where
  claimId : String
  moduleName : String
  theoremName : String
  status : ClaimStatus

def claimMap : List ClaimMapEntry :=
  [
    { claimId := "D0-LEAN-CORE-001", moduleName := "D0.TheoremLedger.ReleaseStatus",
      theoremName := "lean_core_release_candidate", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-LEAN-BRIDGE-001", moduleName := "D0.TheoremLedger.ReleaseStatus",
      theoremName := "lean_bridge_assumptions_explicit", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-FOUND-001", moduleName := "D0.Core.Phi",
      theoremName := "primitive_quadratic_unique_pos_root", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-PHI-HURWITZ-001", moduleName := "D0.NumberTheory.HurwitzMinimaxPhi",
      theoremName := "HURWITZ_MINIMAX_D0_CLASS_PROVED", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ABCD-001", moduleName := "D0.Core.DyadABCD",
      theoremName := "ABCD_cardinality", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-OMEGA8-001", moduleName := "D0.Core.DyadABCD",
      theoremName := "omega8_cardinality", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-CAPACITY-V9-001", moduleName := "D0.Core.FiniteTypes",
      theoremName := "card_v9", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-CAPACITY-V11-001", moduleName := "D0.Core.FiniteTypes",
      theoremName := "card_v11", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-CAPACITY-V13-001", moduleName := "D0.Core.FiniteTypes",
      theoremName := "card_v13", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-SCENE-001", moduleName := "D0.Combinatorics.Tripartite",
      theoremName := "vertex_count_K_9_11_13;edge_count_K_9_11_13;triangle_count_K_9_11_13", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-NCG-INDEX-001", moduleName := "D0.Combinatorics.Tripartite",
      theoremName := "no_3_simplices_clique_complex", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-PHASE-UNFOLD-002", moduleName := "D0.Phase",
      theoremName := "forced_terminal_window;terminal_window_totient;forced_ew_window;ew_window_totient;ew_depth", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-QM-BORN-001", moduleName := "D0.Born",
      theoremName := "finite_born_sum_one", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-QM-BORN-002", moduleName := "D0.Born",
      theoremName := "finite_born_nonnegative", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-CARRIER-003", moduleName := "D0.Algebra.Clifford",
      theoremName := "clifford_relation", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-GAUGE-MATTER-001", moduleName := "D0.Topology.BoundaryBoundary",
      theoremName := "boundary_boundary_zero", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-GAUGE-MATTER-002", moduleName := "D0.Gauge.AnomalySums",
      theoremName := "grav_U1_anomaly_sum;U1_cubic_anomaly_sum;SU2_SU2_U1_anomaly_sum;SU3_SU3_U1_anomaly_sum", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-RG-001", moduleName := "D0.Bridge.PhiDiscreteRG",
      theoremName := "phi_rg_bridge_conditional", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-SMOOTH-001", moduleName := "D0.Bridge.SmoothMetricBridge",
      theoremName := "smooth_metric_bridge_conditional", status := ClaimStatus.leanBridgeAssumptionsExplicit },
    { claimId := "D0-PHASE-TOWER-001", moduleName := "D0.Combinatorics.PhaseTowerMinimality",
      theoremName := "terminalWindow_minimal;fullOrientedWindow_minimal;fullOrientedWindow_C0_minimal", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-PHASE-TOWER-002", moduleName := "D0.Combinatorics.InfinitePhaseTower",
      theoremName := "capacity_recursion_total;forced_terminal_window_all;current_recursion_stabilizes_at_shell_two", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-ARCHIVE-TOWER-001", moduleName := "D0.Geometry.ArchiveRefinementTower",
      theoremName := "terminal_readout_stable;archive_depth_strictly_increases;spectral_modes_strictly_increase;archive_projection_surjective", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-MODE-EXPONENT-001", moduleName := "D0.Geometry.ArchiveModeExponent",
      theoremName := "archive_mode_exponent_eq_abcd;archive_mode_exponent_eq_lorentz_dimension;archive_modes_forced", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-HEATTRACE-001", moduleName := "D0.Geometry.ArchiveHeatTrace",
      theoremName := "heat_trace_positive;heat_trace_projection_compatible", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-LAPLACIAN-001", moduleName := "D0.Geometry.ArchiveLaplacianProperties",
      theoremName := "archive_laplacian_symmetric;archive_laplacian_nonnegative;archive_laplacian_zero_mode_control", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-RESOLVENT-001", moduleName := "D0.Geometry.ArchiveResolventCompactness",
      theoremName := "finite_stage_resolvent_compact;archive_spectral_tightness_from_mode_growth;d0_archive_profinite_resolvent_compactness", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-SPECTRAL-ACTION-ADMISS-001", moduleName := "D0.Geometry.SpectralActionAdmissibility",
      theoremName := "d0_archive_satisfies_structural_admissibility", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-HST-ARCHIVE-001", moduleName := "D0.Probability.HSTExternalInterface",
      theoremName := "hst_admissible_from_certificates;entropy_kernel_exists_if_HST", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-ENTROPY-001", moduleName := "D0.Probability.EntropyCouplingKernel",
      theoremName := "archive_entropy_kernel_exists_if_HST;archive_forgetting_channel_unique", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-DM-CLASSICALITY-001", moduleName := "D0.Detector.WeakCouplingClassicalization",
      theoremName := "weak_coupling_readout_classical_guardrail", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-GAUSSIAN-CHANNEL-001", moduleName := "D0.Probability.ArchiveClassicalGaussianChannel",
      theoremName := "archive_macro_channel_classical_gaussian", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GRAV-QNM-001", moduleName := "D0.Gravity.BoundaryRelaxationSpectrum",
      theoremName := "qnm_passport_requires_preregistered_inputs", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-GENERATION-RAYS-001", moduleName := "D0.Spectrum.GenerationSpectralRays",
      theoremName := "NO_GO_GENERATION_RAYS_UNDEFINED", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-GEN-INDEX-001", moduleName := "D0.Spectrum.BranchDefectProjectiveGeneration",
      theoremName := "exactly_three_projective_branch_defect_generations;defectAction_order_three;defect_generation_card", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GEN-MASS-001", moduleName := "D0.Spectrum.BranchDefectProjectiveControls",
      theoremName := "branch_defect_projective_proof_closed", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-MATTER-REP-001", moduleName := "D0.Matter.GenerationMultiplicity",
      theoremName := "Matter.rep_with_generations_card;Matter.generation_index_does_not_change_gauge_charge;Matter.matter_rep_generation_multiplicity_three", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-MATTER-ANOMALY-001", moduleName := "D0.Matter.GenerationAnomalyPreservation",
      theoremName := "Matter.anomaly_sum_triples;Matter.anomaly_zero_preserved", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GEOM-OBSTRUCT-001", moduleName := "D0.Geometry.ArchiveCurvatureObstruction",
      theoremName := "flat_archive_iff_zero_curvature_obstruction", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-PHASE-DISTANCE", moduleName := "D0.Geometry.ArchivePhaseDistance",
      theoremName := "archivePhaseDistance_nonnegative;archivePhaseDistance_symmetric;archivePhaseDistance_zero_iff", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY", moduleName := "D0.Geometry.ArchiveLaplacianPhaseNaturality",
      theoremName := "NO_GO_ARCHIVE_PHASE_LOCAL_UNIQUENESS", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-ARCHIVE-PHASE-CURVATURE", moduleName := "D0.Geometry.ArchivePhaseCurvatureObstruction",
      theoremName := "phase_flat_iff_zero_curvature_obstruction;NO_GO_PHASE_LAPLACIAN_PROJECTIVE_COMPATIBILITY;NO_GO_PHASE_CURVATURE_OBSTRUCTION", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-LAPLACIAN-RG", moduleName := "D0.Geometry.ArchiveLaplacianRG",
      theoremName := "archiveRGPhaseProjection_surjective;rg_curvature_zero_iff_exact_compatibility;rg_operator_curvature_zero_iff_renormalized_compatibility;rg_flat_curvature_zero_iff_exact_flat_compatibility;exact_projective_compatibility_fails", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-SEAM-CURVATURE-001", moduleName := "D0.Geometry.ArchiveCurvatureDensity",
      theoremName := "seamCommutator_zero_iff_operator_transport_flat;seamCurvatureDensity_nonnegative;seamCurvatureDensity_zero_iff_flat", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-ACTION-001", moduleName := "D0.Geometry.ArchiveActionFunctional",
      theoremName := "archiveCurvatureAction_nonnegative;archiveCurvatureAction_zero_iff_all_flat", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-FIELD-EQ-001", moduleName := "D0.Geometry.ArchiveFieldEquation",
      theoremName := "matrix_hs_square_expansion;first_variation_trace_square;seam_action_variation_quadratic_expansion;stationary_iff_first_variation_zero;vacuum_equation_iff_stationary;sourced_equation_variational_form", status := ClaimStatus.pythonCertClosed },
    { claimId := "D0-ARCHIVE-BIANCHI-001", moduleName := "D0.Geometry.ArchiveBianchiIdentity",
      theoremName := "archiveCanonicalLaplacian_row_sum_zero;archiveLiftOperator_row_sum_one;seamCommutator_row_sum_zero;curvature_gradient_conserved;source_must_be_conserved", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-MATTER-STRESS-COUPLING-001", moduleName := "D0.Matter.ArchiveStressCoupling",
      theoremName := "Matter.matterStressMatrix_symmetric;Matter.matterStressMatrix_conserved;Matter.generated_matter_source_conserved_if_anomaly_free;Matter.generated_matter_source_zero_if_anomaly_free", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-VARIATION-DUAL-001", moduleName := "D0.Geometry.ArchiveVariationDual",
      theoremName := "pairing_depends_only_on_symmetric_part;skew_part_annihilates_admissible_variations", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-STRESS-REP-001", moduleName := "D0.Geometry.ArchiveStressRepresentative",
      theoremName := "raw_gradient_equivalent_to_canonical_stress;canonical_stress_symmetric;canonical_stress_conservation_no_go", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-WEAK-FIELD-001", moduleName := "D0.Geometry.ArchivePoissonEquation",
      theoremName := "poisson_requires_neutral_source;poisson_solution_unique_mod_constant", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-MATTER-SOURCE-NEUTRALITY-001", moduleName := "D0.Matter.GeneratedMatterSource",
      theoremName := "Matter.generated_matter_source_neutral_if_anomaly_free;Matter.NO_GO_MATTER_SOURCE_NEUTRALITY", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-STRESS-CONSERVATION-001", moduleName := "D0.Frozen.ConservedStressProjection",
      theoremName := "constrained_projection_applies_to_archive_gradient", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-ARCHIVE-SCALAR-REDUCTION-001", moduleName := "D0.Active.ScalarPoissonReduction",
      theoremName := "scalar_stationarity_implies_archive_poisson", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-MATTER-LOCALIZATION-001", moduleName := "D0.Active.NonzeroMatterSourceNeutrality",
      theoremName := "Matter.localized_matter_source_neutral_if_anomaly_free", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GEOM-HEAT-TRACE-A2-DECOMP-001", moduleName := "D0.Geometry.HeatTraceA2Decomposition",
      theoremName := "heat_trace_sq_exact_decomposition;discrete_eh_proxy_nonnegative;offdiag_double_count_guard;double_count_factor_guard", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GEOM-SPECTRAL-ACTION-LADDER-001", moduleName := "D0.Geometry.SpectralActionLadder",
      theoremName := "spectral_action_a0_is_volume_proxy;spectral_action_a2_is_eh_proxy;higher_curvature_floor_bound_basic;trace_power_bound;a0_is_volume_proxy;a2_is_eh_proxy;higher_powers_floor_bounded", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GEOM-HIGHER-CURVATURE-FLOOR-BOUND-001", moduleName := "D0.Geometry.HigherCurvatureSuppression",
      theoremName := "Geometry.HigherCurvatureSuppression.matrix_power_combinatorial_bound;Geometry.HigherCurvatureSuppression.conformal_laplacian_entry_bound;Geometry.HigherCurvatureSuppression.higher_curvature_suppression_by_floor", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-TRACEABILITY-STATUS-TAXONOMY-001", moduleName := "D0.Traceability.StatusTaxonomy",
      theoremName := "Traceability.external_likelihood_cannot_promote_to_core_closed", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-OPERATOR-GAUGE-CURVATURE-ORIGIN-001", moduleName := "D0.Matter.GaugeCurvatureOrigin",
      theoremName := "Algebra.commutator_self_zero;Algebra.commutator_skew_of_skew;Algebra.minus_trace_square_nonnegative;Matter.gauge_curvature_skew;Matter.abelian_curvature_annihilates_self_interaction;Matter.gauge_action_positive_from_origin;Bridge.gauge_curvature_origin_closed", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-OPERATOR-VECTOR-LAPLACIAN-ORIGIN-001", moduleName := "D0.Matter.VectorOperatorOrigin",
      theoremName := "Matter.vector_laplacian_preserves_skew;Matter.vector_laplacian_energy_nonnegative;Matter.vector_operator_origin_applies_to_field_equation;Bridge.vector_operator_origin_closed", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-OPERATOR-EDGE-STIFFNESS-ORIGIN-001", moduleName := "D0.Geometry.EdgeStiffnessOrigin",
      theoremName := "Geometry.capacityCore_symmetric;Geometry.capacityCore_psd;Geometry.symmOffDiag_projection_trace_transparent;Geometry.edge_stiffness_preserves_symmOffDiag;Geometry.edge_stiffness_energy_nonnegative;Bridge.edge_stiffness_origin_closed", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-NO-GO-BARE-ARCHIVE-NONABELIAN-001", moduleName := "D0.Bridge.OperatorOriginIndex",
      theoremName := "Bridge.nonabelian_completion_boundary", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-NO-GO-EDGE-STIFFNESS-SCALAR-LEAKAGE-001", moduleName := "D0.Geometry.EdgeStiffnessOrigin",
      theoremName := "Geometry.edge_projection_prevents_scalar_leakage", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-NO-GO-FLAT-TENSOR-NONABELIAN-001", moduleName := "D0.Gauge.FlatTensorNoGo",
      theoremName := "Gauge.flat_tensor_of_two_skew_is_symmetric;Gauge.naive_flat_tensor_nonabelian_boundary", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-GAUGE-NONABELIAN-DISCRETE-CURVATURE-001", moduleName := "D0.Gauge.NonAbelianDiscreteCurvature",
      theoremName := "Gauge.spatialCommutator_preserves_skew;Gauge.spatialWedge_preserves_skew;Gauge.nonabelian_curvature_preserves_skew;Gauge.nonabelian_discrete_curvature_boundary", status := ClaimStatus.leanCoreProved },
    { claimId := "D0-GAUGE-BIANCHI-RESIDUAL-BOUNDARY-001", moduleName := "D0.Gauge.BianchiResidual",
      theoremName := "Gauge.residual_expands_by_definitions;Gauge.exact_residual_graph_anomaly_boundary", status := ClaimStatus.leanNoGoProved },
    { claimId := "D0-GAUGE-YANG-MILLS-KILLING-POSITIVITY-001", moduleName := "D0.Gauge.YangMillsKillingPositivity",
      theoremName := "Gauge.discreteYangMillsAction_nonnegative_of_killing_nonpos", status := ClaimStatus.leanBridgeAssumptionsExplicit }
    ,
    { claimId := "D0-HURWITZ-LOCAL-BOUNDARY-001", moduleName := "D0.Algebra.HurwitzLocalBoundary",
      theoremName := "Algebra.dim_one_admissible;Algebra.dim_two_admissible;Algebra.dim_four_admissible;Algebra.dim_eight_admissible;Algebra.dim_one_has_local_finite_witness;Algebra.dim_two_has_local_finite_witness;Algebra.dim_four_has_local_finite_witness;Algebra.dim_eight_has_local_finite_witness;Algebra.hurwitz_local_boundary_split", status := ClaimStatus.leanCoreProved }
    ,
    { claimId := "D0-EXTERNAL-BACKGROUND-HURWITZ-GLOBAL-CLASSIFICATION-001", moduleName := "D0.Algebra.D0InternalDimensionSelector",
      theoremName := "Algebra.global_hurwitz_classification_not_core_dependency", status := ClaimStatus.notInLeanScope }
    ,
    { claimId := "D0-GAUGE-MATRIX-REP-TRANSFORM-001", moduleName := "D0.Gauge.MatrixRepGaugeTransform",
      theoremName := "Gauge.gaugeTransformFinite_well_typed;Gauge.discreteMaurerCartan_well_typed;Gauge.matrixRepCurvature_well_typed;Gauge.gaugeTransformFinite_preserves_skew_of_orthogonal;Gauge.matrixRepCurvature_preserves_skew;Gauge.matrix_rep_yang_mills_action_nonnegative_of_skew", status := ClaimStatus.leanCoreProved }
    ,
    { claimId := "D0-NO-GO-ABSTRACT-LIERING-FINITE-TRANSFORM-001", moduleName := "D0.Gauge.MatrixRepGaugeTransform",
      theoremName := "Gauge.abstract_lieRing_finite_transform_requires_associative_representation", status := ClaimStatus.leanNoGoProved }
    ,
    { claimId := "D0-GAUGE-BIANCHI-GRADED-DEPRECATED-001", moduleName := "D0.Gauge.MatrixRepGaugeTransform",
      theoremName := "Gauge.exact_bianchi_identity_replaced_by_graded_incidence_closure", status := ClaimStatus.deprecated }
    ,
    { claimId := "D0-BRIDGE-SI-CALIBRATION-BOUNDARY-001", moduleName := "D0.Bridge.SICalibrationBoundary",
      theoremName := "Bridge.c0_c2_scale_action_values_only;Bridge.c0_c2_cannot_alter_a0_a2_trace_shapes;Bridge.si_calibration_belongs_to_bridge_calibration_status;Bridge.si_calibration_cannot_promote_to_core_closed", status := ClaimStatus.pythonCertClosed }
    ,
    { claimId := "D0-HURWITZ-INTERNAL-DIMENSION-SELECTOR-001", moduleName := "D0.Algebra.D0InternalDimensionSelector",
      theoremName := "Algebra.d0_internal_dimension_value;Algebra.d0_internal_dimension_value_mem;Algebra.d0_admissible_dimension_iff;Algebra.d0_admissible_internal_dimension_iff;Algebra.octonion_witness_not_associative_matrix_algebra;Algebra.d0_selector_closes_core_internal_dimension", status := ClaimStatus.leanCoreProved }
    ,
    { claimId := "D0-GAUGE-WILSON-LINK-COVARIANCE-001", moduleName := "D0.Gauge.WilsonLinkGaugeCovariance",
      theoremName := "Gauge.wilson_loop_covariance", status := ClaimStatus.leanCoreProved }
    ,
    { claimId := "D0-NO-GO-NAIVE-LOCAL-GAUGE-COVARIANCE-001", moduleName := "D0.Gauge.WilsonLinkGaugeCovariance",
      theoremName := "Gauge.naive_local_gauge_covariance_counterexample_fin3", status := ClaimStatus.leanNoGoProved }
    ,
    { claimId := "D0-GRADED-BIANCHI-EXACT-001", moduleName := "D0.Gauge.GradedBianchiIdentity",
      theoremName := "Topology.graded_nilpotency;Topology.discrete_exact_bianchi;Topology.graded_bianchi_exact;Gauge.abelian_bianchi_exact;Gauge.graded_bianchi_exact", status := ClaimStatus.leanCoreProved }
    ,
    { claimId := "D0-NO-GO-UNGRADED-BIANCHI-RESIDUAL-001", moduleName := "D0.Gauge.GradedBianchiIdentity",
      theoremName := "Gauge.ungraded_bianchi_residual_counterexample_fin2", status := ClaimStatus.leanNoGoProved }
    ,
    { claimId := "D0-BRIDGE-SI-CALIBRATION-CLOSURE-001", moduleName := "D0.Bridge.SICalibrationClosure",
      theoremName := "Bridge.core_traces_are_dimensionless;Bridge.calibration_changes_only_action_scaling;Bridge.calibration_changes_units_not_core_shape;Bridge.no_si_observable_without_external_calibration;Bridge.h0_gn_lambda_are_not_core_observables;Bridge.si_observables_require_external_calibration", status := ClaimStatus.leanCoreProved }
    ,
    { claimId := "D0-INTERPRETATION-SPINE-001", moduleName := "D0.Bridge.InterpretationSpine",
      theoremName := "Bridge.interpretation_package_keeps_core_dimensionless;Bridge.interpretation_package_does_not_mutate_core_shape;Bridge.si_readout_uses_single_external_calibration;Bridge.interpretation_spine_has_single_si_readout;Bridge.empirical_comparison_is_after_si_readout;Bridge.interpretation_package_rg_readout_coherent;Bridge.interpretation_package_spectral_action_readout_coherent;Bridge.interpretation_package_cosmology_shape_readout_coherent;Bridge.interpretation_package_gauge_readout_coherent;Bridge.interpretation_package_passports_external;Bridge.interpretation_spine_coherence_contract;Bridge.interpretation_package_from_existing_anchors_coherent", status := ClaimStatus.leanBridgeAssumptionsExplicit }
    ,
    { claimId := "D0-FINAL-BRIDGE-INDEX-001", moduleName := "D0.Bridge.FinalBridgeIndex",
      theoremName := "Bridge.D0_FINAL_FOUNDATION_INDEX", status := ClaimStatus.leanCoreProved }
  ]

theorem claimMap_nonempty : claimMap ≠ [] := by
  decide

end D0
