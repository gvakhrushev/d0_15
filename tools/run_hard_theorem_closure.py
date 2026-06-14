#!/usr/bin/env python3
"""Run hard theorem closure targets using the CSV source of truth."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEAN_ROOT = ROOT / "09_LEAN_FORMALIZATION"
INDEX_MODULE_FULL = "D0.TheoremLedger.HardClosureTheoremIndex"
INDEX_MODULE_ACTIVE = "D0.TheoremLedger.ActiveClosureIndex"
CSV_PATH = LEAN_ROOT / "docs" / "HARD_CLOSURE_TARGETS.csv"

try:
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:
    pass


@dataclass(frozen=True)
class Target:
    module: str
    outcome: str
    theorem_names: list[str]


@dataclass(frozen=True)
class CertTarget:
    script: str
    expected_token: str


@dataclass(frozen=True)
class SlicePreset:
    modules: tuple[str, ...] = ()
    certs: tuple[str, ...] = ()
    guards: tuple[str, ...] = ()


CERT_TARGETS = [

    CertTarget(
        "05_CERTS/vp_higgs_scalar_projector_positive.py",
        "PASS_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE",
    ),
    CertTarget(
        "05_CERTS/vp_higgs_scalar_projector_constructive.py",
        "PASS_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE",
    ),
    CertTarget(
        "05_CERTS/vp_ckm_exact_matrix_certificate.py",
        "PASS_CKM_EXACT_MATRIX_CERTIFICATE",
    ),
    CertTarget(
        "05_CERTS/vp_generation_selector_origin.py",
        "PASS_D0_GENERATION_SELECTOR_ORIGIN",
    ),
    CertTarget(
        "05_CERTS/vp_generation_overlap_response_origin.py",
        "PASS_GENERATION_OVERLAP_RESPONSE_ORIGIN",
    ),
    CertTarget(
        "05_CERTS/vp_ckm_phason_holonomy.py",
        "PASS_CKM_PHASON_HOLONOMY",
    ),
    CertTarget(
        "05_CERTS/vp_torus_core13_geometry_origin.py",
        "PASS_TORUS_CORE13_GEOMETRY_ORIGIN",
    ),
    CertTarget(
        "05_CERTS/vp_toral_automorphism_galois_balance.py",
        "PASS_TORAL_AUTOMORPHISM_GALOIS_BALANCE",
    ),
    CertTarget(
        "05_CERTS/vp_trace_heat_capacity_gravity.py",
        "PASS_TRACE_HEAT_CAPACITY_GRAVITY",
    ),
    CertTarget(
        "05_CERTS/vp_closed_vacuum_feedback_full_wave.py",
        "PASS_CLOSED_VACUUM_FEEDBACK_FULL_WAVE",
    ),
    CertTarget(
        "05_CERTS/vp_internal_feedback_resolvent.py",
        "PASS_INTERNAL_FEEDBACK_RESOLVENT",
    ),
    CertTarget(
        "05_CERTS/vp_feedback_partition_function.py",
        "PASS_FINITE_FEEDBACK_PARTITION_FUNCTION",
    ),
    CertTarget(
        "05_CERTS/vp_finite_feedback_equation_of_state.py",
        "PASS_FINITE_PVT_EQUATION_OF_STATE",
    ),
    CertTarget(
        "05_CERTS/vp_terminal_feedback_modes.py",
        "PASS_TERMINAL_FEEDBACK_MODE_CRITERION",
    ),
    CertTarget(
        "05_CERTS/vp_pressure_capacity_balance.py",
        "PASS_PRESSURE_CAPACITY_BALANCE_REGIMES",
    ),
    CertTarget(
        "05_CERTS/vp_sde_feedback_reduction.py",
        "PASS_SDE_TWO_MODE_FEEDBACK_REDUCTION",
    ),
    CertTarget(
        "05_CERTS/vp_master_evolution_theorem.py",
        "PASS_MASTER_EVOLUTION_THEOREM",
    ),
    CertTarget(
        "05_CERTS/vp_information_quasicrystal_phase_unfolding.py",
        "PASS_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING",
    ),
    CertTarget(
        "05_CERTS/vp_condensed_phi_vacuum_cut_project.py",
        "PASS_CONDENSED_PHI_VACUUM_CUT_PROJECT",
    ),
    CertTarget(
        "05_CERTS/vp_galois_lorentz_signature.py",
        "PASS_GALOIS_LORENTZ_SIGNATURE",
    ),
    CertTarget(
        "05_CERTS/vp_quasi_generation_inflation.py",
        "PASS_QUASI_GENERATION_INFLATION_ORBIT",
    ),
    CertTarget(
        "05_CERTS/vp_archive_phason_dark_matter.py",
        "PASS_DARK_PHASON_STRAIN",
    ),
    CertTarget(
        "05_CERTS/vp_window_offset_chirality.py",
        "PASS_CHIRAL_WINDOW_OFFSET",
    ),
    CertTarget(
        "05_CERTS/vp_phason_flip_inertia.py",
        "PASS_INERTIA_PHASON_FLIP_DRAG",
    ),
    CertTarget(
        "05_CERTS/vp_window_fractional_charge.py",
        "PASS_FRACTIONAL_CHARGE_WINDOW_WEIGHT",
    ),
    CertTarget(
        "05_CERTS/vp_quasicrystal_phenomenology_operator_origin.py",
        "PASS_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN",
    ),
    CertTarget(
        "05_CERTS/vp_phason_flip_entropy_sde.py",
        "PASS_PHASON_FLIP_ENTROPY_SDE_GAP_LABELS",
    ),
    CertTarget(
        "05_CERTS/vp_quasi002_phason_strain_generations_baryon.py",
        "PASS_QUASI002_PHASON_STRAIN_GENERATIONS_BARYON",
    ),
    CertTarget(
        "05_CERTS/vp_phason_domain_wall_mesons.py",
        "PASS_PHASON_DOMAIN_WALL_MESONS_K0_LABELS",
    ),
    CertTarget(
        "05_CERTS/vp_d0_tiling_hull.py",
        "PASS_D0_TILING_HULL",
    ),
    CertTarget(
        "05_CERTS/vp_gap_labeling_d0_tiling_hull.py",
        "PASS_D0_GAP_LABELING_TILING_HULL",
    ),
    CertTarget(
        "05_CERTS/vp_noncommutative_solenoid_gravity.py",
        "PASS_NONCOMMUTATIVE_SOLENOID_GRAVITY",
    ),
    CertTarget(
        "05_CERTS/vp_ckm_phason_holonomy_k0.py",
        "PASS_CKM_PHASON_HOLONOMY_K0",
    ),
    CertTarget(
        "05_CERTS/vp_neutrino_phason_decoherence_passport.py",
        "SKIP_NEUTRINO_PHASON_DECOHERENCE_EXTERNAL_DATA_REQUIRED",
    ),
    CertTarget(
        "05_CERTS/vp_no_go_stress_test_suite.py",
        "PASS_NO_GO_STRESS_TEST_SUITE",
    ),

    CertTarget(
        "05_CERTS/vp_core13_shell_geometry_passport.py",
        "PASS_CORE13_SHELL_GEOMETRY_PASSPORT",
    ),
    CertTarget(
        "05_CERTS/vp_pdg_strict_passport.py",
        "PASS_PDG_STRICT_PASSPORT",
    ),
    CertTarget(
        "05_CERTS/vp_charged_lepton_transfer_certificate.py",
        "PASS_CHARGED_LEPTON_TRANSFER_CERTIFICATE",
    ),
    CertTarget(
        "05_CERTS/vp_baryon_s3_tensor_symmetrizer.py",
        "PASS_BARYON_S3_TENSOR_SYMMETRIZER",
    ),
    CertTarget(
        "05_CERTS/vp_baryon_s3_symmetrizer.py",
        "PASS_BARYON_S3_SYMMETRIZER",
    ),
    CertTarget(
        "05_CERTS/vp_meson_defect_transfer_algebra.py",
        "PASS_MESON_DEFECT_TRANSFER_ALGEBRA",
    ),
    CertTarget(
        "05_CERTS/vp_meson_positive_defect_transfer.py",
        "PASS_MESON_POSITIVE_DEFECT_TRANSFER",
    ),
    CertTarget(
        "05_CERTS/vp_spin2_dof_arithmetic.py",
        "PASS_SPIN2_DOF_ARITHMETIC",
    ),
    CertTarget(
        "05_CERTS/vp_finite_spin2_wave_operator_concrete.py",
        "PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE",
    ),
    CertTarget(
        "05_CERTS/vp_finite_spin2_wave_operator.py",
        "PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE",
    ),
    CertTarget(
        "05_CERTS/vp_entropic_archive_gravity.py",
        "PASS_ENTROPIC_ARCHIVE_GRAVITY",
    ),
    CertTarget(
        "05_CERTS/vp_macro_einstein_interface.py",
        "PASS_MACRO_EINSTEIN_INTERFACE",
    ),
    CertTarget(
        "05_CERTS/vp_born_quadratic_origin.py",
        "PASS_BORN_QUADRATIC_ORIGIN",
    ),
    CertTarget(
        "05_CERTS/vp_book04_centered_full_support_selectors.py",
        "PASS_BOOK04_CENTERED_FULL_SUPPORT_SELECTORS",
    ),
    CertTarget(
        "05_CERTS/vp_archive_heat_trace_weyl_dimension.py",
        "PASS_ARCHIVE_HEAT_TRACE_WEYL_DIMENSION",
    ),
    CertTarget(
        "05_CERTS/vp_spectral_action_eh_coefficient.py",
        "PASS_SPECTRAL_ACTION_EH_ADMISSIBILITY",
    ),
    CertTarget(
        "05_CERTS/vp_archive_heat_trace_expansion_fit.py",
        "PASS_ARCHIVE_HEAT_TRACE_EXPANSION_FIT",
    ),
    CertTarget(
        "05_CERTS/vp_spectral_action_expansion_stability.py",
        "PASS_SPECTRAL_ACTION_EXPANSION_STABILITY",
    ),
    CertTarget(
        "05_CERTS/vp_archive_laplacian_rg_flow.py",
        "PASS_ARCHIVE_LAPLACIAN_RG_FLOW",
    ),
    CertTarget(
        "05_CERTS/vp_archive_seam_curvature_action.py",
        "PASS_ARCHIVE_SEAM_CURVATURE_ACTION",
    ),
    CertTarget(
        "05_CERTS/vp_archive_variational_field_equation.py",
        "PASS_ARCHIVE_VARIATIONAL_FIELD_EQUATION",
    ),
    CertTarget(
        "05_CERTS/vp_archive_subgaussian_hst_admissibility.py",
        "PASS_ARCHIVE_SUBGAUSSIAN_HST_ADMISSIBILITY",
    ),
    CertTarget(
        "05_CERTS/vp_archive_convex_order_domination.py",
        "PASS_ARCHIVE_CONVEX_DOMINATION",
    ),
    CertTarget(
        "05_CERTS/vp_archive_entropy_softmax_coupling.py",
        "PASS_ARCHIVE_ENTROPY_COUPLING",
    ),
    CertTarget(
        "05_CERTS/vp_dm_classicality_guardrail.py",
        "PASS_DM_CLASSICALITY_GUARDRAIL",
    ),
    CertTarget(
        "05_CERTS/vp_qnm_delta0_overtone_ladder.py",
        "NO_GO_QNM_DELTA0_OVERTONE_LADDER",
    ),
    CertTarget(
        "05_CERTS/vp_canonical_operator_search.py",
        "PASS_CANONICAL_OPERATOR_SEARCH",
    ),
    CertTarget(
        "05_CERTS/vp_pi0_branch_defect_generation.py",
        "PASS_PI0_BRANCH_DEFECT_PROJECTIVE_GENERATION",
    ),
    CertTarget(
        "05_CERTS/vp_archive_weak_field_poisson.py",
        "PASS_ARCHIVE_WEAK_FIELD_POISSON",
    ),
    CertTarget(
        "05_CERTS/vp_archive_friedmann_instability.py",
        "PASS_ARCHIVE_FRIEDMANN_INSTABILITY",
    ),
    CertTarget(
        "05_CERTS/vp_cosmology_entropy_flow_likelihood.py",
        "PASS_COSMOLOGY_ENTROPY_FLOW_LIKELIHOOD",
    ),
    CertTarget(
        "05_CERTS/vp_si_calibration_boundary.py",
        "PASS_SI_CALIBRATION_BOUNDARY",
    ),
    CertTarget(
        "05_CERTS/vp_finite_hodge_complex_core.py",
        "PASS_FINITE_HODGE_COMPLEX_CORE",
    ),
    CertTarget(
        "05_CERTS/vp_no_axion_finite_cochain.py",
        "PASS_FINITE_NO_AXION_TOPOLOGICAL_BLOCK",
    ),
]


SLICE_PRESETS: dict[str, SlicePreset] = {
    "closed-vacuum-feedback": SlicePreset(
        modules=(
            "D0.TheoremLedger.ClosedVacuumFeedbackIndex",
        ),
        certs=(
            "05_CERTS/vp_closed_vacuum_feedback_full_wave.py",
            "05_CERTS/vp_internal_feedback_resolvent.py",
            "05_CERTS/vp_feedback_partition_function.py",
            "05_CERTS/vp_finite_feedback_equation_of_state.py",
            "05_CERTS/vp_terminal_feedback_modes.py",
            "05_CERTS/vp_pressure_capacity_balance.py",
            "05_CERTS/vp_sde_feedback_reduction.py",
        ),
        guards=(
            "tools/build_empirical_passport_matrix.py",
            "tools/check_empirical_passport_matrix.py",
            "tools/check_assumption_ledger_ownership.py",
            "tools/check_standard_language_audit_budget.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
            "09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py",
        ),
    ),
    "information-quasicrystal": SlicePreset(
        modules=(
            "D0.Geometry.HurwitzRigidPhaseGenerator",
            "D0.Geometry.PhaseReturnBranchCount",
            "D0.Geometry.PhaseUnfoldingQuasicrystal",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_information_quasicrystal_phase_unfolding.py",),
        guards=(
            "tools/check_v14_information_quasicrystal_phase_unfolding_sync.py",
            "tools/check_v14_toral_automorphism_sync.py",
            "tools/check_v14_trace_heat_capacity_gravity_sync.py",
            "tools/check_v14_torus_core13_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "trace-heat-gravity": SlicePreset(
        modules=(
            "D0.Core.FixedDetectorTimeLadder",
            "D0.Dynamics.TraceHeatLucasCore",
            "D0.Dynamics.TraceHeatCapacityGravity",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_trace_heat_capacity_gravity.py",),
        guards=(
            "tools/check_v14_trace_heat_capacity_gravity_sync.py",
            "tools/check_v14_toral_automorphism_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "master-evolution": SlicePreset(
        modules=(
            "D0.Dynamics.TraceHeatLucasCore",
            "D0.Dynamics.MasterEvolutionTheorem",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_master_evolution_theorem.py",),
        guards=(
            "tools/check_v14_master_evolution_sync.py",
            "tools/check_v14_toral_automorphism_sync.py",
            "tools/check_v14_trace_heat_capacity_gravity_sync.py",
            "tools/check_v14_information_quasicrystal_phase_unfolding_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "toral-automorphism": SlicePreset(
        modules=(
            "D0.Dynamics.ToralAutomorphism",
            "D0.Dynamics.GaloisConjugateBalance",
            "D0.Dynamics.DarkSectorCoarseGrain",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_toral_automorphism_galois_balance.py",),
        guards=(
            "tools/check_v14_toral_automorphism_sync.py",
            "tools/check_v14_clean_corpus.py",
        ),
    ),
    "higgs-scalar": SlicePreset(
        modules=(
            "D0.Matter.HiggsScalarProjectorConstructive",
            "D0.Gauge.SMScalarCompletion",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_higgs_scalar_projector_constructive.py",
            "05_CERTS/vp_higgs_scalar_projector_positive.py",
        ),
        guards=(
            "tools/check_v14_higgs_scalar_projector_constructive_sync.py",
            "tools/check_v14_sm_gauge_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "torus-core13": SlicePreset(
        modules=(
            "D0.Geometry.TorusCore13GeometryOrigin",
            "D0.Matter.GenerationSelectorOrigin",
            "D0.Matter.GenerationOverlapResponseOrigin",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_torus_core13_geometry_origin.py",
            "05_CERTS/vp_generation_selector_origin.py",
            "05_CERTS/vp_generation_overlap_response_origin.py",
        ),
        guards=(
            "tools/check_v14_torus_core13_sync.py",
            "tools/check_v14_ckm_origin_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "ckm-phason-holonomy": SlicePreset(
        modules=(
            "D0.Matter.CKMPhasonHolonomy",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_ckm_phason_holonomy.py",),
        guards=(
            "tools/check_v14_ckm_phason_holonomy_sync.py",
            "tools/check_v14_ckm_origin_sync.py",
            "tools/check_v14_torus_core13_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "quasicrystal-phenomenology": SlicePreset(
        modules=(
            "D0.Condensed.CondensedPhiVacuum",
            "D0.Physics.QuasiGenerationsInflation",
            "D0.Physics.ArchivePhasonDarkMatter",
            "D0.Physics.WindowOffsetChirality",
            "D0.Physics.PhasonFlipInertia",
            "D0.Physics.WindowFractionalCharge",
            "D0.Physics.QuasicrystalPhenomenology",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_quasicrystal_phenomenology_operator_origin.py",
        ),
        guards=(
            "tools/check_v14_quasicrystal_phenomenology_operator_origin_sync.py",
            "tools/check_v14_information_quasicrystal_phase_unfolding_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "condensed-phi-vacuum": SlicePreset(
        modules=(
            "D0.Condensed.CondensedPhiVacuum",
            "D0.Physics.QuasicrystalPhenomenology",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_condensed_phi_vacuum_cut_project.py",),
        guards=(
            "tools/check_v14_condensed_phi_vacuum_cut_project_sync.py",
            "tools/check_v14_information_quasicrystal_phase_unfolding_sync.py",
            "tools/check_v14_quasicrystal_phenomenology_operator_origin_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "phason-flip-entropy-sde": SlicePreset(
        modules=(
            "D0.Cosmology.PhasonFlipEntropy",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_phason_flip_entropy_sde.py",),
        guards=(
            "tools/check_v14_phason_flip_entropy_sde_sync.py",
            "tools/check_v14_quasicrystal_phenomenology_operator_origin_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "galois-lorentz-signature": SlicePreset(
        modules=(
            "D0.Physics.GaloisLorentzSignature",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_galois_lorentz_signature.py",),
        guards=(
            "tools/check_v14_galois_lorentz_signature_sync.py",
            "tools/check_v14_toral_automorphism_sync.py",
            "tools/check_v14_tick_lorentz_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "quasi002-phason-baryon": SlicePreset(
        modules=(
            "D0.Matter.PhasonStrainGenerations",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_quasi002_phason_strain_generations_baryon.py",
        ),
        guards=(
            "tools/check_v14_quasi002_phason_strain_generations_baryon_sync.py",
            "tools/check_v14_torus_core13_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "ktheory-gaplabeling-solenoid": SlicePreset(
        modules=(
            "D0.Topology.TilingHull",
            "D0.Matter.KTheoryGapLabeling",
            "D0.Geometry.NonCommutativeSolenoid",
            "D0.Geometry.NonCommutativeSolenoidGravity",
            "D0.Matter.MesonPhasonDomainWalls",
            "D0.Matter.CKMPhasonHolonomy",
            "D0.Cosmology.PhasonFlipEntropy",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_d0_tiling_hull.py",
            "05_CERTS/vp_gap_labeling_d0_tiling_hull.py",
            "05_CERTS/vp_noncommutative_solenoid_gravity.py",
            "05_CERTS/vp_phason_domain_wall_mesons.py",
            "05_CERTS/vp_ckm_phason_holonomy_k0.py",
            "05_CERTS/vp_phason_flip_entropy_sde.py",
        ),
        guards=(
            "tools/check_condensed_ktheory_module_sync.py",
            "tools/check_book_ktheory_gaplabel_sync.py",
            "tools/check_v14_ckm_phason_holonomy_sync.py",
            "tools/check_v14_meson_phason_domain_walls_sync.py",
            "tools/check_v14_phason_flip_entropy_sde_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "meson-phason-domain-walls": SlicePreset(
        modules=(
            "D0.Matter.MesonPhasonDomainWalls",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_phason_domain_wall_mesons.py",
        ),
        guards=(
            "tools/check_v14_meson_phason_domain_walls_sync.py",
            "tools/check_v14_quasi002_phason_strain_generations_baryon_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "icecube-phason-decoherence": SlicePreset(
        modules=(
            "D0.Matter.NeutrinoPhasonWaves",
            "D0.Passport.IceCubePhasonDecoherence",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_neutrino_phason_decoherence_passport.py",
        ),
        guards=(
            "tools/check_v14_icecube_phason_decoherence_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "nuclear-shell-contact-src": SlicePreset(
        modules=(
            "D0.Matter.NuclearShellContactSRC",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=(
            "05_CERTS/vp_nuclear_shell_contact_src.py",
        ),
        guards=(
            "tools/check_v14_nuclear_shell_contact_src_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
    "no-go-stress-suite": SlicePreset(
        modules=(
            "D0.NoGo.StressTestSuite",
            "D0.Bridge.FinalBridgeIndex",
            "D0.TheoremLedger.HardClosureTheoremIndex",
        ),
        certs=("05_CERTS/vp_no_go_stress_test_suite.py",),
        guards=(
            "tools/check_v14_no_go_stress_test_suite_sync.py",
            "tools/check_v14_higgs_scalar_projector_constructive_sync.py",
            "tools/check_v14_quasi002_phason_strain_generations_baryon_sync.py",
            "tools/check_v14_tick_lorentz_sync.py",
            "tools/check_v14_clean_corpus.py",
            "tools/check_physical_bridge_discipline.py",
        ),
    ),
}


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        normalized = item.replace("\\", "/")
        if normalized not in seen:
            seen.add(normalized)
            out.append(item)
    return out


def resolve_root_path(path: str) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return ROOT / p


def cert_token_for(script: str) -> str | None:
    normalized = script.replace("\\", "/")
    for target in CERT_TARGETS:
        if target.script.replace("\\", "/") == normalized:
            return target.expected_token
    return None


def module_from_lean_path(path: str) -> str | None:
    p = resolve_root_path(path)
    try:
        rel = p.resolve().relative_to(LEAN_ROOT.resolve())
    except ValueError:
        return None
    if rel.suffix != ".lean":
        return None
    parts = rel.with_suffix("").parts
    if not parts or parts[0] != "D0":
        return None
    return ".".join(parts)


def run_lake_build(module: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["lake", "build", module],
            cwd=str(LEAN_ROOT),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError:
        return False, "lake executable not found; run this gate inside the Lean/lake IDE environment"
    return proc.returncode == 0, proc.stdout


def run_python_cert(script: str, expected_token: str) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode == 0 and expected_token in proc.stdout, proc.stdout


def run_script(script_path: Path, args: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(script_path)] + args,
        cwd=str(LEAN_ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return proc.returncode == 0, proc.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description="Run hard theorem closure targets.")
    parser.add_argument(
        "--mode",
        choices=["active", "slice", "full"],
        default="full",
        help=(
            "active: legacy fast index gate; slice: targeted modules/certs/guards; "
            "full: fast full gate. Use full --release for exhaustive module replay."
        ),
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="In full mode, replay every CSV module individually after the hard index build.",
    )
    parser.add_argument(
        "--preset",
        action="append",
        choices=sorted(SLICE_PRESETS),
        default=[],
        help="Targeted validation preset for --mode slice.",
    )
    parser.add_argument(
        "--module",
        action="append",
        default=[],
        help="Lean module to build in --mode slice, for example D0.Geometry.PhaseUnfoldingQuasicrystal.",
    )
    parser.add_argument(
        "--cert",
        action="append",
        default=[],
        help="Python certificate script to run in --mode slice, for example 05_CERTS/vp_x.py.",
    )
    parser.add_argument(
        "--guard",
        action="append",
        default=[],
        help="Sync/check script to run in --mode slice, for example tools/check_v14_x_sync.py.",
    )
    parser.add_argument(
        "--changed",
        action="append",
        default=[],
        help="Changed file path. Lean paths are converted to module builds; cert/guard scripts are run directly.",
    )
    args = parser.parse_args()

    proved: list[str] = []
    no_go: list[str] = []
    certs: list[str] = []
    open_items: list[str] = []
    failed: list[str] = []

    if args.mode == "slice":
        print("D0 HARD THEOREM CLOSURE (slice mode):")
        modules = list(args.module)
        cert_scripts = list(args.cert)
        guard_scripts = list(args.guard)

        for preset_name in args.preset:
            preset = SLICE_PRESETS[preset_name]
            modules.extend(preset.modules)
            cert_scripts.extend(preset.certs)
            guard_scripts.extend(preset.guards)

        for changed in args.changed:
            changed_path = changed.replace("\\", "/")
            mod = module_from_lean_path(changed)
            if mod is not None:
                modules.append(mod)
            elif changed_path.startswith("05_CERTS/") and changed_path.endswith(".py"):
                cert_scripts.append(changed_path)
            elif changed_path.startswith("tools/") and changed_path.endswith(".py"):
                guard_scripts.append(changed_path)

        modules = unique(modules)
        cert_scripts = unique(cert_scripts)
        guard_scripts = unique(guard_scripts)

        if not modules and not cert_scripts and not guard_scripts:
            print("  FAIL: slice mode needs --preset, --module, --cert, --guard, or --changed")
            return 1

        for mod in modules:
            ok, output = run_lake_build(mod)
            print(f"  {'PASS' if ok else 'FAIL'} lake build {mod}")
            if ok:
                proved.append(mod)
            else:
                failed.append(mod)
                open_items.append(f"{mod}: slice module build failed\n{output}")

        for script in cert_scripts:
            expected_token = cert_token_for(script)
            if expected_token is None:
                proc = subprocess.run(
                    [sys.executable, str(resolve_root_path(script))],
                    cwd=str(ROOT),
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                ok = proc.returncode == 0
                output = proc.stdout
            else:
                ok, output = run_python_cert(script, expected_token)
            print(f"  {'PASS' if ok else 'FAIL'} python {script}")
            if ok:
                certs.append(script)
            else:
                failed.append(script)
                open_items.append(f"{script}: slice cert failed\n{output}")

        for script in guard_scripts:
            ok, output = run_script(resolve_root_path(script), [])
            print(f"  {'PASS' if ok else 'FAIL'} guard {script}")
            if not ok:
                failed.append(script)
                open_items.append(f"{script}: slice guard failed\n{output}")

        print(f"  PROVED: {len(proved)}")
        print(f"  NO-GO: {len(no_go)}")
        print(f"  CERTS: {len(certs)}")
        if open_items:
            print(f"  OPEN: {len(open_items)}")
            for item in open_items:
                print(f"    - {item}")
        else:
            print("  OPEN: 0")
        return 1 if failed else 0

    if args.mode == "active":
        print("D0 HARD THEOREM CLOSURE (active mode):")
        # Build Active Closure Index
        idx_ok, idx_output = run_lake_build(INDEX_MODULE_ACTIVE)
        print(f"  {'PASS' if idx_ok else 'FAIL'} lake build {INDEX_MODULE_ACTIVE}")
        if not idx_ok:
            failed.append(INDEX_MODULE_ACTIVE)
            open_items.append(f"{INDEX_MODULE_ACTIVE}: active theorem index build failed")

        # In active mode, build only the v12.39 final bridge index module.
        active_modules = [
            "D0.Bridge.FinalBridgeIndex",
        ]
        for mod in active_modules:
            ok, output = run_lake_build(mod)
            print(f"  {'PASS' if ok else 'FAIL'} lake build {mod}")
            if ok:
                proved.append(mod)
            else:
                failed.append(mod)
                open_items.append(f"{mod}: active module build failed")

        print(f"  PROVED: {len(proved)}")
        print(f"  NO-GO: {len(no_go)}")
        print(f"  CERTS: {len(certs)}")
        if open_items:
            print(f"  OPEN: {len(open_items)}")
            for item in open_items:
                print(f"    - {item}")
        return 1 if failed else 0

    else:
        print("D0 HARD THEOREM CLOSURE:")

        # Read from CSV
        if not CSV_PATH.exists():
            print(f"  FAIL: CSV targets file not found at {CSV_PATH}")
            return 1

        with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            csv_rows = list(reader)

        # Check against HardClosureTheoremIndex.lean
        index_path = LEAN_ROOT / "D0" / "TheoremLedger" / "HardClosureTheoremIndex.lean"
        if not index_path.exists():
            print(f"  FAIL: Index file not found at {index_path}")
            return 1
        index_content = index_path.read_text(encoding="utf-8")

        for row in csv_rows:
            check_str = f"#check D0.{row['theorem_name']}"
            if check_str not in index_content:
                msg = f"Theorem target {row['theorem_name']} is in CSV but missing from Lean index!"
                failed.append(row["theorem_name"])
                open_items.append(msg)
                print(f"  FAIL: {msg}")

        # Build target objects by module
        module_to_theorems: dict[str, list[str]] = {}
        module_to_outcome: dict[str, str] = {}
        for row in csv_rows:
            mod = row["module"]
            kind = row["kind"]
            outcome = "LEAN_NO_GO_PROVED" if kind == "NO_GO" else "LEAN_THEOREM_PROVED"
            module_to_theorems.setdefault(mod, []).append(row["theorem_name"])
            module_to_outcome[mod] = outcome

        targets = [
            Target(mod, module_to_outcome[mod], theorems)
            for mod, theorems in module_to_theorems.items()
        ]

        idx_ok, idx_output = run_lake_build(INDEX_MODULE_FULL)
        print(f"  {'PASS' if idx_ok else 'FAIL'} lake build {INDEX_MODULE_FULL}")
        if not idx_ok:
            failed.append(INDEX_MODULE_FULL)
            open_items.append(f"{INDEX_MODULE_FULL}: theorem index build failed")

        if args.release:
            print("  RELEASE: replaying every CSV module individually")
            for target in targets:
                ok, output = run_lake_build(target.module)
                print(f"  {'PASS' if ok else 'FAIL'} lake build {target.module}")
                if not ok:
                    failed.append(target.module)
                    open_items.append(f"{target.module}: Lean build failed")
                    continue
                joined = f"{target.module}: {', '.join(target.theorem_names)}"
                if target.outcome == "LEAN_NO_GO_PROVED":
                    no_go.append(joined)
                else:
                    proved.append(joined)
        else:
            index_covered = len(targets) if idx_ok else 0
            if idx_ok:
                proved.extend(
                    f"{target.module}: covered by {INDEX_MODULE_FULL}"
                    for target in targets
                    if target.outcome != "LEAN_NO_GO_PROVED"
                )
                no_go.extend(
                    f"{target.module}: covered by {INDEX_MODULE_FULL}"
                    for target in targets
                    if target.outcome == "LEAN_NO_GO_PROVED"
                )
            print(
                "  FAST: skipped per-module CSV replay; "
                f"{index_covered} modules covered by {INDEX_MODULE_FULL}. "
                "Use --release for exhaustive module replay."
            )

        for cert in CERT_TARGETS:
            ok, output = run_python_cert(cert.script, cert.expected_token)
            print(f"  {'PASS' if ok else 'FAIL'} python {cert.script}")
            if ok:
                certs.append(f"{cert.script}: {cert.expected_token}")
            else:
                failed.append(cert.script)
                open_items.append(f"{cert.script}: cert failed")

        # Run no sorry guard and claim map coverage
        no_sorry_ok, no_sorry_out = run_script(
            LEAN_ROOT / "tools" / "check_no_sorry_in_core.py", ["--all-modules"]
        )
        print(f"  {'PASS' if no_sorry_ok else 'FAIL'} check no sorry guard")
        if not no_sorry_ok:
            failed.append("no_sorry_guard")
            open_items.append(f"No-sorry guard failed:\n{no_sorry_out}")

        claim_cov_ok, claim_cov_out = run_script(
            LEAN_ROOT / "tools" / "check_claim_map_coverage.py", []
        )
        print(f"  {'PASS' if claim_cov_ok else 'FAIL'} check claim map coverage")
        if not claim_cov_ok:
            failed.append("claim_map_coverage")
            open_items.append(f"Claim map coverage failed:\n{claim_cov_out}")

        physical_bridge_ok, physical_bridge_out = run_script(
            ROOT / "tools" / "check_physical_bridge_discipline.py", []
        )
        print(f"  {'PASS' if physical_bridge_ok else 'FAIL'} check physical bridge discipline")
        if not physical_bridge_ok:
            failed.append("physical_bridge_discipline")
            open_items.append(f"Physical bridge discipline failed:\n{physical_bridge_out}")

        hardening_sync_ok, hardening_sync_out = run_script(
            ROOT / "tools" / "check_theory_hardening_sync.py", []
        )
        print(f"  {'PASS' if hardening_sync_ok else 'FAIL'} check theory hardening sync")
        if not hardening_sync_ok:
            failed.append("theory_hardening_sync")
            open_items.append(f"Theory hardening synchronization failed:\n{hardening_sync_out}")

        book_rewrite_ok, book_rewrite_out = run_script(
            ROOT / "tools" / "check_book_theory_rewrite.py", []
        )
        print(f"  {'PASS' if book_rewrite_ok else 'FAIL'} check book theory rewrite")
        if not book_rewrite_ok:
            failed.append("book_theory_rewrite")
            open_items.append(f"Book theory rewrite guard failed:\n{book_rewrite_out}")

        v14_clean_ok, v14_clean_out = run_script(
            ROOT / "tools" / "check_v14_clean_corpus.py", []
        )
        print(f"  {'PASS' if v14_clean_ok else 'FAIL'} check v14 clean corpus")
        if not v14_clean_ok:
            failed.append("v14_clean_corpus")
            open_items.append(f"v14 clean corpus guard failed:\n{v14_clean_out}")

        book05_integrated_ok, book05_integrated_out = run_script(
            ROOT / "tools" / "check_book05_integrated_rewrite.py", []
        )
        print(f"  {'PASS' if book05_integrated_ok else 'FAIL'} check Book 05 integrated rewrite")
        if not book05_integrated_ok:
            failed.append("book05_integrated_rewrite")
            open_items.append(f"Book 05 integrated rewrite guard failed:\n{book05_integrated_out}")

        born2_ok, born2_out = run_script(
            ROOT / "tools" / "check_v14_born2_sync.py", []
        )
        print(f"  {'PASS' if born2_ok else 'FAIL'} check v14 born2 sync")
        if not born2_ok:
            failed.append("v14_born2_sync")
            open_items.append(f"v14 Born 2.0 guard failed:\n{born2_out}")

        book04_selectors_ok, book04_selectors_out = run_script(
            ROOT / "tools" / "check_v14_book04_selectors_sync.py", []
        )
        print(f"  {'PASS' if book04_selectors_ok else 'FAIL'} check v14 Book04 selectors sync")
        if not book04_selectors_ok:
            failed.append("v14_book04_selectors_sync")
            open_items.append(f"v14 Book04 selector guard failed:\n{book04_selectors_out}")

        ckm_origin_ok, ckm_origin_out = run_script(
            ROOT / "tools" / "check_v14_ckm_origin_sync.py", []
        )
        print(f"  {'PASS' if ckm_origin_ok else 'FAIL'} check v14 CKM origin sync")
        if not ckm_origin_ok:
            failed.append("v14_ckm_origin_sync")
            open_items.append(f"v14 CKM origin guard failed:\n{ckm_origin_out}")

        ckm_phason_ok, ckm_phason_out = run_script(
            ROOT / "tools" / "check_v14_ckm_phason_holonomy_sync.py", []
        )
        print(f"  {'PASS' if ckm_phason_ok else 'FAIL'} check v14 CKM phason-holonomy sync")
        if not ckm_phason_ok:
            failed.append("v14_ckm_phason_holonomy_sync")
            open_items.append(f"v14 CKM phason-holonomy guard failed:\n{ckm_phason_out}")

        torus_core13_ok, torus_core13_out = run_script(
            ROOT / "tools" / "check_v14_torus_core13_sync.py", []
        )
        print(f"  {'PASS' if torus_core13_ok else 'FAIL'} check v14 Torus/Core13 sync")
        if not torus_core13_ok:
            failed.append("v14_torus_core13_sync")
            open_items.append(f"v14 Torus/Core13 guard failed:\n{torus_core13_out}")

        spin2_ok, spin2_out = run_script(
            ROOT / "tools" / "check_v14_spin2_derivation_sync.py", []
        )
        print(f"  {'PASS' if spin2_ok else 'FAIL'} check v14 spin-2 derivation sync")
        if not spin2_ok:
            failed.append("v14_spin2_derivation_sync")
            open_items.append(f"v14 spin-2 derivation guard failed:\n{spin2_out}")

        spin2_wave_ok, spin2_wave_out = run_script(
            ROOT / "tools" / "check_v14_spin2_wave_operator_sync.py", []
        )
        print(f"  {'PASS' if spin2_wave_ok else 'FAIL'} check v14 spin-2 wave-operator sync")
        if not spin2_wave_ok:
            failed.append("v14_spin2_wave_operator_sync")
            open_items.append(f"v14 spin-2 wave-operator guard failed:\n{spin2_wave_out}")

        sm_gauge_ok, sm_gauge_out = run_script(
            ROOT / "tools" / "check_v14_sm_gauge_sync.py", []
        )
        print(f"  {'PASS' if sm_gauge_ok else 'FAIL'} check v14 SM gauge sync")
        if not sm_gauge_ok:
            failed.append("v14_sm_gauge_sync")
            open_items.append(f"v14 SM gauge guard failed:\n{sm_gauge_out}")

        cosmology_split_ok, cosmology_split_out = run_script(
            ROOT / "tools" / "check_v14_cosmology_split_sync.py", []
        )
        print(f"  {'PASS' if cosmology_split_ok else 'FAIL'} check v14 cosmology split sync")
        if not cosmology_split_ok:
            failed.append("v14_cosmology_split_sync")
            open_items.append(f"v14 cosmology split guard failed:\n{cosmology_split_out}")

        tick_lorentz_ok, tick_lorentz_out = run_script(
            ROOT / "tools" / "check_v14_tick_lorentz_sync.py", []
        )
        print(f"  {'PASS' if tick_lorentz_ok else 'FAIL'} check v14 tick/Lorentz sync")
        if not tick_lorentz_ok:
            failed.append("v14_tick_lorentz_sync")
            open_items.append(f"v14 tick/Lorentz guard failed:\n{tick_lorentz_out}")

        book04_coeff_ok, book04_coeff_out = run_script(
            ROOT / "tools" / "check_v14_book04_coefficient_origin_sync.py", []
        )
        print(f"  {'PASS' if book04_coeff_ok else 'FAIL'} check v14 Book04 coefficient-origin sync")
        if not book04_coeff_ok:
            failed.append("v14_book04_coefficient_origin_sync")
            open_items.append(f"v14 Book04 coefficient-origin guard failed:\n{book04_coeff_out}")

        global_operator_ok, global_operator_out = run_script(
            ROOT / "tools" / "check_v14_global_operator_geometry_sync.py", []
        )
        print(f"  {'PASS' if global_operator_ok else 'FAIL'} check v14 global operator-geometry sync")
        if not global_operator_ok:
            failed.append("v14_global_operator_geometry_sync")
            open_items.append(f"v14 global operator-geometry guard failed:\n{global_operator_out}")

        higgs_scalar_ok, higgs_scalar_out = run_script(
            ROOT / "tools" / "check_v14_higgs_scalar_projector_constructive_sync.py", []
        )
        print(f"  {'PASS' if higgs_scalar_ok else 'FAIL'} check v14 Higgs scalar projector sync")
        if not higgs_scalar_ok:
            failed.append("v14_higgs_scalar_projector_constructive_sync")
            open_items.append(f"v14 Higgs scalar-projector guard failed:\n{higgs_scalar_out}")

        toral_automorphism_ok, toral_automorphism_out = run_script(
            ROOT / "tools" / "check_v14_toral_automorphism_sync.py", []
        )
        print(f"  {'PASS' if toral_automorphism_ok else 'FAIL'} check v14 toral automorphism sync")
        if not toral_automorphism_ok:
            failed.append("v14_toral_automorphism_sync")
            open_items.append(f"v14 toral automorphism guard failed:\n{toral_automorphism_out}")

        trace_heat_capacity_ok, trace_heat_capacity_out = run_script(
            ROOT / "tools" / "check_v14_trace_heat_capacity_gravity_sync.py", []
        )
        print(f"  {'PASS' if trace_heat_capacity_ok else 'FAIL'} check v14 trace-heat-capacity gravity sync")
        if not trace_heat_capacity_ok:
            failed.append("v14_trace_heat_capacity_gravity_sync")
            open_items.append(f"v14 trace-heat-capacity gravity guard failed:\n{trace_heat_capacity_out}")

        information_quasicrystal_ok, information_quasicrystal_out = run_script(
            ROOT / "tools" / "check_v14_information_quasicrystal_phase_unfolding_sync.py", []
        )
        print(f"  {'PASS' if information_quasicrystal_ok else 'FAIL'} check v14 information-quasicrystal phase-unfolding sync")
        if not information_quasicrystal_ok:
            failed.append("v14_information_quasicrystal_phase_unfolding_sync")
            open_items.append(f"v14 information-quasicrystal phase-unfolding guard failed:\n{information_quasicrystal_out}")

        quasicrystal_phenomenology_ok, quasicrystal_phenomenology_out = run_script(
            ROOT / "tools" / "check_v14_quasicrystal_phenomenology_operator_origin_sync.py", []
        )
        print(f"  {'PASS' if quasicrystal_phenomenology_ok else 'FAIL'} check v14 quasicrystal phenomenology operator-origin sync")
        if not quasicrystal_phenomenology_ok:
            failed.append("v14_quasicrystal_phenomenology_operator_origin_sync")
            open_items.append(f"v14 quasicrystal phenomenology operator-origin guard failed:\n{quasicrystal_phenomenology_out}")

        phason_flip_entropy_ok, phason_flip_entropy_out = run_script(
            ROOT / "tools" / "check_v14_phason_flip_entropy_sde_sync.py", []
        )
        print(f"  {'PASS' if phason_flip_entropy_ok else 'FAIL'} check v14 phason-flip entropy S_DE sync")
        if not phason_flip_entropy_ok:
            failed.append("v14_phason_flip_entropy_sde_sync")
            open_items.append(f"v14 phason-flip entropy S_DE guard failed:\n{phason_flip_entropy_out}")

        condensed_phi_ok, condensed_phi_out = run_script(
            ROOT / "tools" / "check_v14_condensed_phi_vacuum_cut_project_sync.py", []
        )
        print(f"  {'PASS' if condensed_phi_ok else 'FAIL'} check v14 condensed phi-vacuum cut-project sync")
        if not condensed_phi_ok:
            failed.append("v14_condensed_phi_vacuum_cut_project_sync")
            open_items.append(f"v14 condensed phi-vacuum cut-project guard failed:\n{condensed_phi_out}")

        galois_lorentz_ok, galois_lorentz_out = run_script(
            ROOT / "tools" / "check_v14_galois_lorentz_signature_sync.py", []
        )
        print(f"  {'PASS' if galois_lorentz_ok else 'FAIL'} check v14 Galois/Lorentz signature sync")
        if not galois_lorentz_ok:
            failed.append("v14_galois_lorentz_signature_sync")
            open_items.append(f"v14 Galois/Lorentz signature guard failed:\n{galois_lorentz_out}")

        icecube_phason_ok, icecube_phason_out = run_script(
            ROOT / "tools" / "check_v14_icecube_phason_decoherence_sync.py", []
        )
        print(f"  {'PASS' if icecube_phason_ok else 'FAIL'} check v14 IceCube phason-decoherence sync")
        if not icecube_phason_ok:
            failed.append("v14_icecube_phason_decoherence_sync")
            open_items.append(f"v14 IceCube phason-decoherence guard failed:\n{icecube_phason_out}")

        master_evolution_ok, master_evolution_out = run_script(
            ROOT / "tools" / "check_v14_master_evolution_sync.py", []
        )
        print(f"  {'PASS' if master_evolution_ok else 'FAIL'} check v14 master evolution sync")
        if not master_evolution_ok:
            failed.append("v14_master_evolution_sync")
            open_items.append(f"v14 master evolution guard failed:\n{master_evolution_out}")

        no_go_stress_ok, no_go_stress_out = run_script(
            ROOT / "tools" / "check_v14_no_go_stress_test_suite_sync.py", []
        )
        print(f"  {'PASS' if no_go_stress_ok else 'FAIL'} check v14 no-go stress-test suite sync")
        if not no_go_stress_ok:
            failed.append("v14_no_go_stress_test_suite_sync")
            open_items.append(f"v14 no-go stress-test suite guard failed:\n{no_go_stress_out}")

        meson_phason_ok, meson_phason_out = run_script(
            ROOT / "tools" / "check_v14_meson_phason_domain_walls_sync.py", []
        )
        print(f"  {'PASS' if meson_phason_ok else 'FAIL'} check v14 meson phason domain-wall sync")
        if not meson_phason_ok:
            failed.append("v14_meson_phason_domain_walls_sync")
            open_items.append(f"v14 meson phason domain-wall guard failed:\n{meson_phason_out}")

        gravity_closure_ok, gravity_closure_out = run_script(
            ROOT / "tools" / "check_v14_gravity_closure_sync.py", []
        )
        print(f"  {'PASS' if gravity_closure_ok else 'FAIL'} check v14 gravity closure sync")
        if not gravity_closure_ok:
            failed.append("v14_gravity_closure_sync")
            open_items.append(f"v14 gravity closure guard failed:\n{gravity_closure_out}")

        print(f"  PROVED: {len(proved)}")
        print(f"  NO-GO: {len(no_go)}")
        print(f"  CERTS: {len(certs)}")
        if open_items:
            print(f"  OPEN: {len(open_items)}")
            for item in open_items:
                print(f"    - {item}")
        else:
            print("  OPEN: 0")
        return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

# v14 combinatorial selector origin guard: check_v14_book04_combinatorial_selector_origins.py
