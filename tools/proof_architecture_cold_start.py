"""Repeatable cold-start retrieval checks over real D0 cases.

Text matches remain candidates. This runner checks that the expected pinned
owner/application references are surfaced in the bounded result set; it does
not make a semantic acceptance decision.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import proof_architecture as proof


CASES: list[dict[str, Any]] = [
    {
        "id": "labelled-native-raising-inverse",
        "queries": [
            "native raising operator inverse null leg",
            "точное восстановление тетрады из native raising operator при null leg",
            "native raising operator transfer coframe null leg",
            "Перенос и тетрада восстанавливаются из самого native raising operator",
            "all 16 coframe 24 link directions at node not only null pp-wave ansatz variations",
            "все 16 coframe 24 proper Lorentz directions tangent observer jets",
            "AF radial coframe equivalence section 5.1 direct native Julia golden execution cubic Einstein vertex",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
            "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
             "commit": "fe5cf335da04cac14e50407b03f98b96be17dc52",
             "blob": "1c8d59e5533b443d9a015dc4512cfbc160ae7e62",
             "sections": ["8.4", "8.5"], "scope_query_indexes": [0, 1, 2, 3, 4, 5],
             "scope_query_sections": {"0": [], "1": [],
                                      "2": [], "3": [],
                                      "4": ["8.5"], "5": ["8.5"]}},
            {"path": "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
             "commit": "fe5cf335da04cac14e50407b03f98b96be17dc52",
             "blob": "734e21ae6bc04ff3446ad15858936d417fdd2e55",
             "sections": ["5.1"], "scope_query_indexes": [6],
             "scope_query_sections": {"6": ["5.1"]}},
        ],
        "scope_review": "Owner all-jet null-leg inverse and the concrete consumer are distinct; this is not physical price selection.",
    },
    {
        "id": "positive-nonvacuum-recovery",
        "queries": [
            "positive nonvacuum harmonic cubic fixed nonlinear Brinkmann metric",
            "transverseFivePoint_nonvacuumBrinkmannProfile_eq_source harmonicBrinkmannCubic radial quadratic",
            "nonvacuumProfile_source_eq_finiteMidpointMatterNorm finiteMatterForwardGradient_midpointStep twoComponentMatterNormSq",
            "native finite matter midpoint exact energy five point source same interval",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md",
            "03_FORMALIZATION/D0/Geometry/NonvacuumBrinkmannStencil.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_brinkmann_stencil_declarations_2026-10-25.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md",
                "commit": "8b94198c8dfbdf5983ad0b350b058fb30bb68a54",
                "blob": "63c36b18af67fc1f113f9e33deb13cf43ddf4556",
                "sections": ["7.1", "7.2"],
                "scope_query_indexes": [0, 3],
                "scope_query_sections": {"0": ["7.1"], "3": ["7.2"]},
            },
        ],
        "scope_review": (
            "The compiled NonvacuumBrinkmannStencil result proves the exact five-point "
            "harmonic/radial readout and binds its source norm to the same finite midpoint "
            "matter record. This is only the pointwise stencil/source fragment: the original "
            "CAR construction, 40-to-3-to-1 substitution, all 16+24+2 Euler rows, refinement "
            "estimate, and physical native Book/clock/source selection remain separate and open."
        ),
    },
    {
        "id": "proper-lorentz-same-orientation-orbit",
        "queries": [
            "proper Lorentz same determinant orientation complete coframe link orbit coordinates",
            "det=1 same orientation Lorentz orbit русская ориентация",
            "a4d_complete_proper_orbit_coordinates a4dRightProperLorentz_gram_complete finiteGram_right_orbit_complete finiteGram_dressed_transport_compatible finiteMatrix_dressed_transport_frame_invariant a4dDressedLink_frame_invariant finiteMatrix_dressed_transport_eq_iff_frame_action a4dDressedLink_eq_iff_rightAction",
            "a4dRightProperLorentz_gram_complete a4d_complete_proper_orbit_coordinates finiteGram_right_orbit_complete",
        ],
        "required_refs": [
            "02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md",
            "03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean",
            "03_FORMALIZATION/D0/Algebra/FiniteGramTangent.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_orbit_declarations_2026-10-26_fintype_only_core.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_gram_orbit_shared_api_declarations_2026-10-26_fintype_only_core.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/metric_provenance_crosswalk_2026-10-26_fe15cd8c.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md",
                "commit": "77d3ab6059bd1a3ce48637b97b9f30aa8825fc5f",
                "blob": "e5e31819492d670c81fc4a2871e1ef8cfa205c08",
                "scope_query_indexes": [0],
            },
        ],
        "scope_review": (
            "The shared generic finiteGram_right_orbit_complete theorem proves that equal "
            "finite Gram matrices give a right-isometry orbit when the reference frame is "
            "invertible; the Lorentz module specializes it to site coframes and dressed "
            "links. The generic finiteGram_dressed_transport_compatible theorem proves "
            "the endpoint Gram identity from the transport isometry and invertibility of "
            "the target frame; its Lorentz adapter preserves those hypotheses. The generic "
            "finiteMatrix_dressed_transport_frame_invariant theorem factors the two-sided "
            "frame cancellation, and the Lorentz link-invariance theorem consumes it "
            "without requiring target-frame invertibility for this identity. The generic equality iff theorem "
            "then characterizes equality of dressed transports by exactly the corresponding "
            "two-sided link action, and the Lorentz equivalence specializes that result. The proper "
            "field theorem also requires equal determinant orientation "
            "at every site. It leaves time orientation, the selected-action map, physical "
            "source selection, and independent acceptance open."
        ),
    },
    {
        "id": "finite-gram-affine-quadratic-expansion",
        "queries": [
            "finiteGram_add_smul_expand finite Gram expansion arbitrary base frame quadratic remainder",
            "finiteGram_add_smul_difference_quotient exact normalized Gram difference full quadratic remainder",
            "finite_gram_orbit_shared_api_declarations_2026-10-26_fintype_only_core.json finiteGram_add_smul_difference_quotient",
            "finite Gram expansion Theta plus t C two sided linear variation exact quadratic term",
            "A4D Solder Metric Completion finiteGram_add_smul_difference_quotient solderMetric_flat_tangent j2DetectorMetricPath_symmetric_difference_quotient",
        ],
        "required_refs": [
            "03_FORMALIZATION/D0/Algebra/FiniteGramTangent.lean",
            "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_gram_orbit_shared_api_declarations_2026-10-26_fintype_only_core.json",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "scope_review": (
            "finiteGram_add_smul_expand proves the exact finite quadratic Gram identity "
            "at an arbitrary base frame, and finiteGram_add_smul_difference_quotient "
            "retains its full quadratic remainder in the normalized difference. The old "
            "expansion APIs remain specializations; solderMetric_flat_tangent and the J2 "
            "symmetric quotient consume the generic quotient theorem directly. This proves "
            "no physical action, source choice, or continuum curvature law."
        ),
    },
    {
        "id": "finite-gram-frechet-derivative",
        "queries": [
            "finiteGram_hasFDerivAt finiteGramTangent arbitrary finite matrix frame two sided Frechet derivative",
            "finiteGramTangent_apply H eta Theta transpose Theta eta H transpose Frobenius norm",
            "j2DetectorMetricPath_hasFDerivAt_direction j2DetectorMetricPath_hasFDerivAt_flat generic finiteGram derivative through t ↦ 1 + tH and H ↦ 1 + H",
            "производная Фреше отображения Грама на конечных матрицах полный двусторонний касательный оператор",
            "finiteGram_hasFDerivAt metric-provenance crosswalk current D0.Algebra.FiniteGramDerivative",
        ],
        "required_refs": [
            "03_FORMALIZATION/D0/Algebra/FiniteGramDerivative.lean",
            "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
            "02_REGISTRY/gr_assembly/applications.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/metric_provenance_crosswalk_2026-10-26_b1fb6bc7.json",
        ],
        "scope_review": (
            "The generic API proves the full finite-matrix Fréchet derivative of "
            "finiteGram at every frame, with both terms HηΘᵀ + ΘηHᵀ and its "
            "Frobenius-norm continuous-linear realization. The J2 flat-frame "
            "derivative is its specialization through H ↦ 1 + H. The J2 "
            "directional path derivative also composes the generic derivative "
            "with t ↦ 1 + tH; the exact quadratic remainder remains recorded "
            "separately. The solder field consumer composes the generic map "
            "with the finite sitewise coframe map. These are finite "
            "algebra/calculus results only: the "
            "selected-action-to-carrier map, physical source choice, continuum "
            "variation, and independent C0 acceptance remain open."
        ),
    },
    {
        "id": "golden-step-vs-internal-ratio",
        "queries": ["Golden physical metric step internal Perron scale ratio native HJR countercontrol"],
        "required_refs": [
            "A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md",
        ],
        "scope_review": "Physical metric homogeneity and internal Bratteli scale ratio are not interchangeable; native HJR remains a countercontrol.",
    },
    {
        "id": "fixedright-stationary-and-minimum-scopes",
        "queries": [
            "exact curved native preparation original full16 Dirac fixedRIGHT128 R covector",
            "stationary preparation minimum saddle Fredholm cutoff cusp",
        ],
        "required_refs": [
            "A4D_EXACT_CURVED_NATIVE_DIRAC_FIXED_RIGHT_PREPARATION_AND_SOURCE_2026_10_20.md",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/A4D_EXACT_CURVED_NATIVE_DIRAC_FIXED_RIGHT_PREPARATION_AND_SOURCE_2026_10_20.md",
             "commit": "4873b3c245a91bd8c9cb25bceeb82662e9f62944",
             "blob": "6395c736c54d0c0a704d22ffdf046dbfc2c6c84b",
             "sections": ["5"], "scope_query_indexes": [0]},
        ],
        "scope_review": "Stationarity, minimum, saddle, Fredholm continuation, and cutoff cusp require separate owners and conclusions.",
    },
    {
        "id": "same-fields-do-not-fix-price-source",
        "queries": [
            "same history price source composition original 128 history partition",
            "same field coframe different action cut Info clock source equivalence",
            "same-action/source map",
        ],
        "required_refs": [
            "A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md",
             "scope_query_indexes": [0]},
        ],
        "scope_review": "Equality of geometric data does not imply action, cut, Info, clock, or source equivalence.",
    },
    {
        "id": "same-prefix-two-ending-prospective-price",
        "queries": [
            "same-prefix two-ending Julia odds equal continuation partition weights absolute Book anchor",
            "actual Julia Born odds native K-weight continuation partition weights",
        ],
        "required_refs": [
            "A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md",
            "A4D_NATIVE_FOUR_COPY_TO_CURVATURE_APPLICATION_2026_10_20.md",
        ],
        "scope_review": "The prospective identity requires equal full continuation partition weights; it supplies neither an absolute normalizer nor physical source selection.",
    },
    {
        "id": "clock-dirac-incidence-curvature",
        "queries": [
            "chronological clock spatial CAR Dirac paired incidence d2 curvature complement modes",
            "native clock pressure complete price synthesis",
            "native weighted Dirac boundary",
            "native pairing refinement source",
        ],
        "required_refs": [
            "A4D_NATIVE_CLOCK_PRESSURE_AND_COMPLETE_PRICE_SYNTHESIS_2026_10_20.md",
            "A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md",
            "A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md",
        ],
        "scope_review": "Chronological clock, spatial CAR Dirac, paired incidence, and d² curvature/complement modes need their explicit maps.",
    },
    {
        "id": "gain-readiness-vs-trace-multiplicity",
        "queries": [
            "source gain readiness trace multiplicity",
            "four copy curvature application readiness derivative gain",
            "AF scene heat comparison trace multiplicity",
        ],
        "required_refs": [
            "A4D_NATIVE_FOUR_COPY_TO_CURVATURE_APPLICATION_2026_10_20.md",
            "A4D_NATIVE_AF_SCENE_HEAT_COMPARISON.md",
        ],
        "scope_review": "Readiness/source gain and trace multiplicity are separate quantities and claims.",
    },
    {
        "id": "conditional-transfer-does-not-select-execution",
        "queries": ["generic verification theory transfer Bellman optimal premise physical execution"],
        "required_refs": [
            "D0_FOUNDATION_THEORY_TRANSFER_COMPOSITION_2026_10_20.md",
            "MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md",
        ],
        "scope_review": "Generic transfer and Bellman consequences with an optimality premise do not choose physical execution.",
    },
    {
        "id": "verification-kernel-transfer-outside-gr",
        "queries": [
            "verification_core representedRecord complete future kernel",
            "Interpretation.transfer_theorem translated regime premise source_proof",
            "visible_only_memory_cannot_decode_hiddenBit_futures hiddenBit_sufficient_encoder_injective sufficient_memory_reflects_future complete future decoder",
            "sufficient_encoder_injective_of_profile_injective sufficient_memory_cardinality_lower_bound finite future memory decoder profile separation",
            "future_profile_memory_cardinality_declarations_2026-10-25.json sufficient_memory_cardinality_lower_bound declaration axioms",
            "erased_hiddenBit_operation_map_is_impossible step_commutes hidden archive action",
            "verified_visibleFalseReadout_transfers_to_common_execution verifiedStateImageEquiv transfer_theorem",
            "ConnesReconstructionBridge connes_reconstruction_conditional metricEqualsSpectrum supplied witness assumption",
        ],
        "required_refs": [
            "D0_VERIFICATION_CORE_COMPOSITION_2026_10_20.md",
            "03_FORMALIZATION/D0/Foundation/VerificationCore.lean",
            "D0_FOUNDATION_THEORY_TRANSFER_COMPOSITION_2026_10_20.md",
            "03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean",
            "03_FORMALIZATION/D0/Foundation/VerificationTransferApplication.lean",
            "03_FORMALIZATION/D0/Foundation/FutureExecution.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/future_profile_memory_cardinality_declarations_2026-10-25.json",
            "03_FORMALIZATION/D0/Bridge/ConnesReconstructionBridge.lean",
        ],
        "scope_review": (
            "VerificationTransferApplication.visible_only_memory_cannot_decode_hiddenBit_futures "
            "rejects a decoder from visible-only memory through hiddenBit_sufficient_encoder_injective "
            "and the generic sufficient_memory_reflects_future result. The generic "
            "sufficient_encoder_injective_of_profile_injective and "
            "sufficient_memory_cardinality_lower_bound require injective complete profiles, "
            "decoder correctness and, for cardinality, finite state and memory types. "
            "The hidden-bit finite control supplies these conditions and proves its four-state lower bound. "
            "erased_hiddenBit_operation_map_is_impossible rejects the identity-state map that erases "
            "the archive-revealing operation at step_commutes. The positive "
            "verified_visibleFalseReadout_transfers_to_common_execution composes the verified "
            "foundation state with the actual transfer. ConnesReconstructionBridge."
            "connes_reconstruction_conditional remains conditional on supplied ConnesReconstruction "
            "fields. These finite controls do not select a physical execution."
        ),
    },
    {
        "id": "car-scaffolds-vs-hodge-operator-claims",
        "queries": [
            "D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001 D0-ARCHIVE-CAR-DIRAC-SQUARE-001 actual carDirac hoppingCarDirac",
            "D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001 literal claim ID source candidate view",
            "D0-ARCHIVE-CAR-SPECTRUM-AMPLIFICATION-001 D0-ARCHIVE-DIRAC-HEATTRACE-MULTIPLICITY-001 arithmetic spinor decomposition heat trace",
            "car_amplification_times_spinor_eq_sixteen diracHeatTraceMultiplicity_eq_fock_dim",
            "hodgeCarDirac_sq cochainDifferenceLaplacian_eq_backward_forward Hodge square four roles",
            "hodge_difference_diagonal_double_metric_at_l2 oriented graph Laplacian double count",
            "hodgeCarDirac_kernel_finrank constant Fock fibre 16",
            "spatialShellSubmodule_finrank hodgeSquare_on_spatialShell shell rank 96 A invariant",
            "shellEnergy_tendsto_two_pi spatial_shell_rank_l2 L 2 control",
            "carDirac_square_eq_four_id_at_zero carDirac_zero_kernel_trivial_at_zero L 2 exact CAR control",
            "finiteMatrixTensorProduct_sum_square_eq_diagonal finiteMatrixTensorProduct_one "
            "finiteMatrixTensorProduct_transpose tensorProduct_mul "
            "totalParityOperator_symmetric generic finite matrix Clifford square",
            "car_dirac_square_l2_identity_declaration car_dirac_l2_zero_kernel_trivial_declaration",
            "car_hodge_current_declaration_inventory_2026-10-25 current compiled types",
            "car_hodge_transpose_current_declaration_inventory_2026-10-25 current compiled types",
            "car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-25 "
            "compiled diagonal transpose dependencies",
            "car zero mode claim declarations 2026 10 25",
            "hodge car dirac kernel declaration 2026 10 25",
            "car dirac square claim declarations 2026 10 25",
            "car spectrum amplification claim declarations 2026 10 25",
            "dirac heattrace multiplicity claim declarations 2026 10 25",
            "hodge car dirac square declaration 2026 10 25",
            "hodge square backward forward declaration 2026 10 25",
            "hodge car dirac l2 normalization declaration 2026 10 25",
            "hodge spatial shell claim declarations 2026 10 25",
            "hodge shell energy limit declaration 2026 10 25",
            "hodge shell rank l2 control declaration 2026 10 25",
            "ArchiveHodgeCARDirac not carDirac hoppingCarDirac difference operator",
            "BOOK_06 06.spectral actual CAR Dirac square zero mode ClaimMap OPEN",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/claims.csv",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json",
            "03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean",
            "03_FORMALIZATION/D0/Algebra/FiniteMatrixTensorProduct.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveCARDirac.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracSquare.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracKernel.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracShell.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeSpatialShellOperator.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_zero_mode_claim_declarations_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_car_dirac_kernel_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_dirac_square_claim_declarations_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_spectrum_amplification_claim_declarations_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/dirac_heattrace_multiplicity_claim_declarations_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_car_dirac_square_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_square_backward_forward_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_car_dirac_l2_normalization_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_spatial_shell_claim_declarations_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_shell_energy_limit_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/hodge_shell_rank_l2_control_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_dirac_square_l2_no_go_declaration_followup_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_dirac_square_l2_identity_declaration_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_dirac_l2_zero_kernel_trivial_declaration_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_current_declaration_inventory_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_transpose_current_declaration_inventory_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-25.json",
        ],
        "scope_review": (
            "D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001, D0-ARCHIVE-CAR-DIRAC-SQUARE-001, "
            "D0-ARCHIVE-CAR-SPECTRUM-AMPLIFICATION-001, and "
            "D0-ARCHIVE-DIRAC-HEATTRACE-MULTIPLICITY-001 remain OPEN: their mapped "
            "ArchiveCARDirac mapped declarations remain arithmetic constants. The "
            "finite L=2 no-kernel theorem proves D^2=4I for the literal hopping "
            "matrix and excludes a zero mode only on that carrier; it refutes a "
            "16-dimensional kernel reading at L=2 without proving an all-period "
            "kernel theorem or changing the OPEN claim. The scoped L=2 square "
            "does not prove the registered all-period square, spinor decomposition, "
            "continuum modes, or heat trace. Separate "
            "Hodge-cochain results already prove hodgeCarDirac_sq, its four-role oriented "
            "difference formula, the 16-dimensional Hodge kernel, and the L=2 factor-two "
            "graph-diagonal comparison. The spatial shell has rank 96 and square-energy "
            "eigenvalue only under 3 <= L and positive-role-A invariance; its energy tends "
            "to 2*pi, while the L=2 shell rank is 48. These Hodge results have no operator "
            "intertwiner to the hopping matrix. formal_support.csv lists the Hodge modules, "
            "not ArchiveCARDirac. The BOOK_06 06.spectral locator has no exact heading. "
            "The v3 literal-ID source view records no exact claim-ID mention for these four "
            "open CAR rows in the book files; their source-unit mapping remains unresolved. "
            "Compiled narrow inventories preserve types and trust footprints; they do not "
            "accept the open claims, C0, or physical D0."
        ),
    },
    {
        "id": "top-hodge-inverse-spectral-outside-gr",
        "queries": [
            "top Hodge inverse spectral full D H M2 equal unordered positive tripartite zone sizes Vieta roots",
            "равные полные top Hodge D H M2 восстанавливают неупорядоченные положительные размеры трех зон Виета корни",
        ],
        "required_refs": [
            "01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
            "03_FORMALIZATION/D0/Synthesis/TopHodgeInverseSpectralRigidity.lean",
        ],
        "scope_review": "The inverse theorem covers positive complete-tripartite scenes and recovers the unordered zone multiset; it neither chooses zone labels nor extends to arbitrary finite complexes.",
    },
    {
        "id": "dense-operator-scene-reconstruction-outside-gr",
        "queries": [
            "dense operator scene 33 vertices triangle complete tripartite support rank",
            "распознавание dense operator scene 33 vertices triangle complete tripartite support rank",
        ],
        "required_refs": [
            "01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
            "03_FORMALIZATION/D0/Synthesis/DenseOperatorSceneRigidity.lean",
        ],
        "scope_review": "This finite recognition theorem uses the stated 33-vertex, adjacency, rank, and trace hypotheses; it does not assert a physical D0 selector or a general operator-dynamics result.",
    },
    {
        "id": "scoped-nogo-vs-positive-existence",
        "queries": [
            "native affine probe no-go arbitrary smooth probes physical contrast",
            "native realization closure positive existence physical",
        ],
        "required_refs": [
            "A4D_NATIVE_AFFINE_PROBE_NOGO.md",
            "A4D_NATIVE_REALIZATION_CLOSURE.md",
        ],
        "scope_review": "A scoped negative rules out only its declared route and does not discharge positive existence.",
    },
    {
        "id": "finite-affine-carrier-parameter-recovery",
        "queries": [
            "nilpotentAffineRep_injective",
            "exact affine semidirect representation R_nil L b T_b rho",
            "archiveExteriorFrameLift_injective full 16-state frame action faithful",
        ],
        "required_refs": [
            "02_REGISTRY/research/MEMO_A4D_AFFINE_SENSITIVE_SITE_MATTER_LINK.md",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean",
        ],
        "scope_review": "The source owner supplies the affine representation; its compiled finite-carrier application recovers both parameters from equality of complete operators. Search candidates and that algebraic injectivity do not select a physical letter or price.",
    },
    {
        "id": "finite-julia-null-chart-inverse",
        "queries": [
            "archiveJuliaNullBlock_reconstructsAffineFunctional",
            "complete Julia raising query contraction block null inverse equation 28",
            "canonical normalized witness z=b over b transpose b positive square-root branch",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
            "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "03_FORMALIZATION/D0/Geometry/ArchiveJuliaRaisingOperatorReadout.lean",
        ],
        "scope_review": "The finite-carrier inverse retains symmetric endpoint forms, their isometry, a normalized witness, and the positive branch; the canonical witness exists under the stated null and nondegeneracy hypotheses. It does not establish the consumer's physical price, admission, all-jet pullback, or GR selection.",
    },
    {
        "id": "julia-query-principal-frame-coframe-recovery",
        "queries": [
            "principalFrameObservedQueryCoframeRecovery Eq 30a four full query vacuum responses",
            "Fbar equals U_mat transpose eta coframe inverse metric invariant IsRoleLorentz",
            "из четырех Julia query columns восстановление кофрейма и метрики Eq 30a",
            "AF radial coframe equivalence section 5.1 principal frame reconstruction",
            "complete Julia raising query contraction block null inverse equation 28",
            "principalFrameJuliaQueryFamily_open_chart_link_recovery Eq 28 positive branch non-null transverse q",
            "уравнение 28 открытая окрестность null-вектора поперечные q вариации восстановление endpoint map Julia",
            "Eq 27 nonzero Lorentz norm Gamma Clifford volume inverse recover frame from full raising query",
            "archiveJuliaRaisingQuery_nonNull_gamma_recovery chi endpoint covariance q nonzero",
            "уравнение 27 ненулевой лоренцев норм Clifford volume восстановить перенос из полного raising operator",
            "principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage Eq27 Eq28",
            "покрытие всех ненулевых сдвигов через Eq 27 Eq 28 principalFrameJuliaQueryFamily",
            "archiveJuliaSourceCARRaisingQuery_nonNull_recovery_of_proper_roleLorentz IsRoleLorentz",
            "proper row action Lorentz endpoint det one CAR Julia recovery adapter",
            "principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz Eq27 Eq28",
            "правый Lorentz endpoint одновременно CAR Eq 27 и query Eq 28 один recovered endpoint",
            "principalFrameJuliaQueryFamily_recoveredInverseCoframe_hasFDerivAt",
            "principalFrameJuliaQueryFamily_joint_coframe_endpoint_recovery_of_proper_roleLorentz hΓ hΛ",
            "principalFrameJuliaQueryFamily_joint_coframe_all_role_endpoint_chart_coverage_of_proper_roleLorentz hα hShift",
            "archiveJuliaSourceCARRaisingQuery_nonNull_endpoint_map_injective Eq 27 nonzero Lorentz norm q Gamma_x(u) recover U exact CAR raising query all 16 grades",
            "principalFrameJuliaEq26_blind_to_ABSignFlip_links vacuum-column endpoint blindness",
            "archiveJuliaSourceCARRaisingQuery_nonNull_endpoint_map_injective julia_nonnull_endpoint_map_injectivity_declaration_2026-10-26",
            "principalFrameJuliaEq26_blind_to_ABSignFlip_links julia_eq26_link_blindness_declaration_2026-10-26",
            "principalFrameJuliaNonNullQuery_separates_ABSignFlip_links julia_nonnull_query_link_separation_declaration_2026-10-26",
            "archiveJuliaSourceEq27EndpointMapReadout Eq27 endpoint map readout",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
            "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_endpoint_inventory_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_joint_recovery_inventory_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_same_query_coframe_endpoint_recovery_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_all_role_coframe_endpoint_chart_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_nonnull_endpoint_map_injectivity_declaration_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_eq26_link_blindness_declaration_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_nonnull_query_link_separation_declaration_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_eq27_endpoint_map_readout_declaration_2026-10-26.json",
            "03_FORMALIZATION/D0/Geometry/A4DJuliaPrincipalFrameRecovery.lean",
            "03_FORMALIZATION/D0/Geometry/A4DJuliaNonNullGammaRecovery.lean",
            "03_FORMALIZATION/D0/Geometry/A4DJuliaRecoveryComposition.lean",
            "03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveJuliaRaisingOperatorReadout.lean",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
             "commit": "fe5cf335da04cac14e50407b03f98b96be17dc52",
             "blob": "1c8d59e5533b443d9a015dc4512cfbc160ae7e62",
             "sections": ["8.4", "8.5"], "scope_query_indexes": [1, 2, 4, 5, 6, 7, 8, 9, 15, 19],
             "scope_query_sections": {"1": ["8.5"], "2": ["8.5"],
                                      "4": ["8.4"], "5": ["8.4"],
                                      "6": ["8.4"], "7": ["8.4"],
                                      "8": ["8.4"], "9": ["8.4"],
                                      "15": ["8.4"], "19": ["8.4"]}},
            {"path": "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
             "commit": "fe5cf335da04cac14e50407b03f98b96be17dc52",
             "blob": "734e21ae6bc04ff3446ad15858936d417fdd2e55",
             "sections": ["5.1"], "scope_query_indexes": [3],
             "scope_query_sections": {"3": ["5.1"]}},
        ],
        "scope_review": (
            "The general compiled map keeps full-query equality and the inverse-coframe right-inverse explicit; "
            "its canonical query-family specialization removes the external query-equality premise. The Eq. (28) "
            "composition recovers M_r on its full open chart when the observed projected metric covector is "
            "nonzero and the positive square-root branch holds; its null specialization derives those conditions "
            "from nondegeneracy, normalization, and one nonzero null shift. `archiveJuliaSourceCARRaisingQuery_"
            "nonNull_recovery_of_proper_roleLorentz` applies Eq. (27) to the source's row-action `IsRoleLorentz Λ` "
            "convention with `det Λ = 1`: the transposed endpoint map preserves the same source form and has "
            "determinant one. `principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_"
            "roleLorentz` composes this same role-indexed endpoint with Eq. (28), and the CAR decoder, query "
            "decoder, and full exterior lift return that one map on the non-null chart under the explicit source "
            "norm, normalized covector, projected-covector, and positive-branch assumptions. "
            "`principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage` joins the algebraic charts for every "
            "nonzero shift under the explicit endpoint isometry and normalized covector: the non-null branch "
            "retains `det M = 1`, while the null branch derives Eq. (28)'s projected-covector and positive-branch "
            "conditions. A physical application must still bind the admitted endpoint to the row-action matrix "
            "and prove its properness; smoothness of the full inverse or all-jet pullback, physical query admission, "
            "price/source selection, and GR closure remain open. The compiled "
            "`principalFrameJuliaQueryFamily_inverseCoframeReadout_hasFDerivAt` theorem proves the readout "
            "derivative in all 16 inverse-coframe coordinates with the Lorentz link fixed; its "
            "`principalFrameJuliaQueryFamily_recoveredInverseCoframe` application then composes the exact "
            "right-link transport to identity, including the identity derivative. Neither result supplies "
            "the remaining 24 link jets or the joint all-jet identity. "
            "`principalFrameJuliaQueryFamily_joint_coframe_endpoint_recovery_of_proper_roleLorentz` now "
            "pairs that transported Eq. (30a) coframe identity with the Eq. (28) endpoint decoder on the "
            "same concrete query family; the established Eq. (27) and exterior-lift outputs remain in the "
            "companion joint endpoint theorem. `principalFrameJuliaQueryFamily_joint_coframe_all_role_"
            "endpoint_chart_coverage_of_proper_roleLorentz` composes that coframe identity with the existing "
            "non-null Eq. (27)/null Eq. (28) chart disjunction for every role, retaining the normalized "
            "covector and nonzero-shift premises. Both compositions keep the coframe link fixed and do not "
            "fill the 24 link directions. The endpoint-map injectivity theorem reuses the owned Eq. (27) "
            "decoder: on a common non-null source, equality of complete CAR raising queries for two "
            "Lorentz-form-preserving determinant-one endpoint maps forces the maps equal. An explicit diagonal "
            "A/B sign flip has determinant one, preserves the source Lorentz form, and is distinct from identity. "
            "The assembled Eq. (26) vacuum-column matrix is nevertheless identical for those two link families; "
            "the complete non-null CAR query separates them. This is a finite exact countercontrol for using "
            "vacuum columns as a full link inverse, and a scoped application of the existing Eq. (27) decoder. "
            "`archiveJuliaSourceEq27EndpointMapReadout` now names the shared total query-to-endpoint readout; "
            "the non-null recovery theorem supplies the isometry, determinant-one, and source-norm conditions "
            "under which it returns the endpoint. Recovery, injectivity, and chart consumers use this definition. "
            "It does not prove the 24 link derivatives, full `D R D Φ = I`, physical admission, complete "
            "price/source selection, GR closure, or independent C0 acceptance."
        ),
    },
    {
        "id": "finite-hermitian-adjoint-twisted-car-application",
        "queries": [
            "finiteHermitianAdjoint_unique coordinate finite Hermitian pairing conjugate transpose",
            "finiteLinearMap_apply_eq_sum_single finite coordinate basis action",
            "dTwistedAdjoint_eq_finiteHermitianAdjoint unit holonomy CAR annihilation formula",
            "dTwistedLinear_comp_self_eq_zero actual twisted exterior differential",
            "hodgeCarDiracTwisted_eq_finiteHermitianHodgeDirac",
            "hodgeCarDiracTwisted_finiteHermitian_self_adjoint",
            "hodgeCarDiracTwistedLinear_square anticommutator",
            "hodgeCarDiracTwisted_finiteHermitian_square unitary holonomy",
            "dTwistedAdjoint_adjoint compatibility wrapper finiteHermitianPairing_adjoint_right",
            "hodgeCarDiracTwisted_self_adjoint compatibility wrapper generic Hermitian self-adjoint",
            "hodgeCarDiracTwisted_sq generic Hodge anticommutator twistedDifferenceLaplacian",
        ],
        "required_refs": [
            "03_FORMALIZATION/D0/Algebra/FiniteCoordinateBasis.lean",
            "03_FORMALIZATION/D0/Algebra/FiniteHermitianAdjoint.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveTwistedHodgeDirac.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_differential_nilpotency_adapter_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_operator_adapter_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_self_adjoint_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_linear_square_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_pointwise_square_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hermitian_right_adjoint_wrapper_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hermitian_self_adjoint_wrapper_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hodge_laplacian_from_generic_square_2026-10-25.json",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "scope_review": (
            "The actual site×Fock twisted differential is embedded as a compiled finite linear map, its explicit "
            "annihilation formula is identified with the generic Hermitian adjoint, and the generic Hodge self-adjoint "
            "and square laws are applied under the explicit unitary-holonomy premise. Retrieval does not select a "
            "physical holonomy, action, source, or GR application."
        ),
    },
    {
        "id": "real-unit-profile-weighted-hermitian-bridge",
        "queries": [
            "finiteWeightedAdjoint_one_eq_finiteHermitianAdjoint real unit profile",
            "hodgeCarDirac_unit_profile_adjoint_eq_finiteHermitianAdjoint",
            "finiteHermitianHodgeDirac_pairing_self_adjoint",
            "finiteHermitianHodgeDirac_square",
            "cubicalWeightedHodgeDirac_unit_profile_eq_finiteHermitianHodgeDirac",
            "cubicalWeightedHodgeDirac_unit_profile_hermitian_self_adjoint",
            "cubicalWeightedHodgeDirac_unit_profile_square",
            "cochainPairing_eq_finiteHermitianPairing",
            "hodgeCarDirac_finiteHermitianAdjoint_eq_self",
            "hodgeCarDirac_unit_profile_adjoint_eq_self",
            "hodgeCodifferential_smul backwardAnnihilateDirection_smul",
            "finiteHermitianAdjoint_dForwardₗ_eq_hodgeCodifferentialₗ",
            "hodgeCarDiracHermitian_square",
            "hodgeCarDirac_sq generic Hodge anticommutator",
            "hodgeCarDiracₗ_eq_finiteHermitianHodgeDirac",
            "hodgeCarDiracₗ_apply canonical compatibility bridge",
            "hodgeCarDirac_add hodgeCarDirac_smul generic linear map laws",
            "finiteHermitianAdjoint_finiteHermitianHodgeDirac_eq_self",
        ],
        "required_refs": [
            "03_FORMALIZATION/D0/Algebra/FiniteHermitianAdjoint.lean",
            "03_FORMALIZATION/D0/Algebra/FiniteWeightedAdjoint.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveWeightedHodgeDirac.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracSquare.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracKernel.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_weighted_unit_profile_adjoint_bridge_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_weighted_hodge_hermitian_bridge_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_hermitian_hodge_dirac_self_adjoint_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/cubical_unit_profile_hermitian_hodge_equality_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/cubical_unit_profile_hermitian_hodge_self_adjoint_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_hermitian_hodge_dirac_square_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/cubical_unit_profile_hermitian_hodge_square_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/real_counting_pairing_hermitian_adapter_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_hermitian_adjoint_self_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_unit_profile_adjoint_self_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_square_from_generic_hermitian_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_generic_adjoint_self_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_canonical_map_refactor_2026-10-25.json",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "scope_review": (
            "The real unit-profile bilinear adjoint is identified with the standard finite Hermitian adjoint; the "
            "registered real Hodge/CAR operator's own adjoint is proved equal to itself through its existing "
            "counting-pairing theorem. The generic Hermitian Hodge--Dirac self-adjointness and square/anticommutator "
            "laws are applied to the registered nilpotent cubical differential, and the real CAR codifferential is "
            "identified as the standard Hermitian adjoint of its forward differential. The existing function-level "
            "square is then recovered from the generic anticommutator and the owned CAR cross-term Laplacian. A "
            "generic typed adjoint-equality corollary is also consumed by the real Hodge/CAR self-adjoint theorem. "
            "The kernel-facing `hodgeCarDiracₗ` is now the same generic Hermitian map, while a compiled pointwise "
            "bridge preserves the legacy function-level API and its kernel/shell applications. "
            "The concrete profile equality is only at the unit profile: arbitrary nonzero weighted profiles remain "
            "in the bilinear API, and no geometric or physical Hodge profile is selected."
        ),
    },
    {
        "id": "native-weighted-dirac-matrix-application",
        "queries": [
            "weightedDiracMatrix_mulVec typed weighted Hodge Dirac linear map ArchiveCochainBasis",
            "weightedDiracLinear_identity_eq_hodgeCarDirac hodgeCarDiracMatrix_mulVec existing real Hodge CAR operator",
            "weightedDiracMatrix_symmetric_of_finiteHermitianAdjoint_eq_self hodgeCarDiracMatrix_symmetric",
            "spatialNyquist_weightedDirac_matrix_block L=4 flatLorentzWeightedDiracMatrix",
            "actual full-cochain matrix B-singleton vacuum spatial Nyquist positive self-adjoint weighted Dirac Eq. 6",
            "spatialNyquistEven_weightedDirac_matrix_block every even archive period N+2",
            "flatLorentzWeightedDiracEven_no_positive_selfadjoint_pairing",
            "spatial_block_has_no_positive_metric rotationBlock hadj h0 h1 matrix Fin 2",
            "roleWeightedArchiveDifferenceLaplacian_fourier all-size role weighted difference eigenvalue",
            "archiveLorentzianDifferenceLaplacian_fourier roleWeightedArchiveFourierSymbol_lorentzian",
            "archiveLorentzianDifferenceOperator_fourier_mode archiveFourierFockMode archiveLorentzianFourierSymbol",
            "archiveLorentzianCARDirac_square_fourier_mode roleWeightedArchiveCARDirac_square roleWeightedArchiveCodifferential_cross",
            "roleWeightedArchiveCARDirac_fourier_mode roleWeightedArchiveFourierFockAction_square archiveLorentzianCARFourierFockAction_square",
            "archiveLorentzian_full_cochain_kernel_finrank_ge_diagonal_family archiveLorentzian_kernel_finrank_cases archiveLorentzian_nonzero_null_mode_classification",
            "null_mode_kernel_eq_range null_mode_kernel_half_dimension DivisionRing finrank complex fibre",
            "finiteHermitianPairing_weightSquareRoot finiteWeightedConjugate_self_adjoint positive profile",
            "cubicalWeightedHodgeDirac_standard_representative_application cubicalWeightedHodgeDirac_square_degree_preserving",
            "archiveRoleFourierInversion actual archive site scalar field",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md",
            "02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary.lean",
            "03_FORMALIZATION/D0/Research/NativeWeightedDiracLinearOperator.lean",
            "03_FORMALIZATION/D0/Research/NativeWeightedDiracNyquistApplication.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveLorentzianFourierApplication.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveLorentzianCARDiracApplication.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_fourier_module_declarations_2026-10-25.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_car_fourier_fiber_action_declarations_2026-10-25.json",
            "03_FORMALIZATION/D0/Research/NativeWeightedDiracFourierNullModes.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_fourier_null_modes_declarations_2026-10-25.json",
            "03_FORMALIZATION/D0/Algebra/FiniteWeightedAdjoint.lean",
            "03_FORMALIZATION/D0/Geometry/ArchiveWeightedHodgeDirac.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_standard_representative_claim_reuse_2026-10-25.json",
        ],
        "scope_review": (
            "The generic theorem identifies matrix multiplication in the existing ArchiveCochainBasis "
            "with the supplied-weight function operator. The original source pin db3091aded8f6cfe8d39dcd973ccf30ec40dfb08 "
            "contains the isolated 2x2 obstruction; the full-carrier transfer is a separate branch formalization "
            "delta at c3ceba511bab5c435d715fd56382615fc1dc1505. The exact L=4 application proves the vacuum and "
            "B-singleton action equations and applies that conditional transfer. The supplied positive form and "
            "self-adjointness premise are not physically derived. The all-even extension requires an even "
            "archive period N+2 and proves the same full-carrier block and conditional obstruction there; it "
            "is separate from the Eq. (5) Fourier application. The signed scalar second-order operator now has "
            "an all-size character eigenbasis, a complete scalar site Fourier inversion, and an injective "
            "sixteen-label Fock coefficient embedding per momentum. A companion module defines the explicitly "
            "role-signed first-order CAR operator and proves its square equals that operator on the full carrier; "
            "composition gives the Eq. (5) all-size squared-mode law for every Fock profile. Its direct first-order "
            "Fourier action is now an explicit finite CAR map on each Fock profile, and the induced map squares to "
            "the same symbol. This does not make an arbitrary profile a first-order eigenvector; physical "
            "action/source selection and GR closure remain open. The null-mode companion proves the exact "
            "16/8/0 per-fibre dimensions, ker=range on nonconstant null fibres, at least N+1 diagonal null "
            "momenta, and the full-cochain lower bound 16+8(N+1). Exact total root count/kernel, gauge "
            "quotient, broader refinement classification, and physical/source selection remain open. Its "
            "complex-fibre contraction uses the DivisionRing generalization at "
            "a6ff3f2fc7e0e6b94d673c2cd713cb4faeb94004, capsule blob "
            "60de6702e232d6b68fc3b707a058383c4c09b2ff. The positive-profile "
            "standard-Hilbert representative is a separate cubical application for "
            "caller-supplied positive diagonal weights; it does not derive general W, "
            "the Lorentz-induced W_Q, geometry, or physical selection."
        ),
    },
    {
        "id": "archive-phase-shift-reuses-transitive-permutation-theorem",
        "queries": [
            "ArchiveTopology abstract_shift_commute_implies_diagonal_constant shiftMatrix commute_with_shift_iterate",
            "ArchivePartialTrace density_uniform_from_commute commute_with_shift_implies_diagonal_constant",
            "Fin finRotate cyclicShiftMatrix finRotateArchiveTopology partial_trace_density_uniform_under_shift",
            "GenerationTensorExactness flavor_blindness_step_of_commute commute_with_shift_entries kronecker_C_I",
            "GenerationTensorExactness flavor_blindness_step_k_of_commute stage2_flavor_blindness_of_commute stage3_tensor_exactness no h_off",
        ],
        "required_refs": [
            "03_FORMALIZATION/D0/Topology/ArchiveShiftTopology.lean",
            "03_FORMALIZATION/D0/Geometry/ArchivePhaseShift.lean",
            "03_FORMALIZATION/D0/Matter/ArchivePartialTrace.lean",
            "03_FORMALIZATION/D0/Spectrum/GenerationTensorExactness.lean",
        ],
        "required_sources": [
            {"path": "03_FORMALIZATION/D0/Topology/ArchiveShiftTopology.lean",
             "scope_query_indexes": [0]},
            {"path": "03_FORMALIZATION/D0/Geometry/ArchivePhaseShift.lean",
             "scope_query_indexes": [0, 1]},
            {"path": "03_FORMALIZATION/D0/Matter/ArchivePartialTrace.lean",
             "scope_query_indexes": [1, 2]},
            {"path": "03_FORMALIZATION/D0/Spectrum/GenerationTensorExactness.lean",
             "scope_query_indexes": [3, 4]},
        ],
        "scope_review": (
            "For a finite carrier, a transitive permutation, and exact commutation with its shift matrix, "
            "the generic theorem forces constant diagonal; a stronger entrywise covariance theorem handles "
            "the lifted Fin n × N tensor shift; the iterated and cross-generation flavor-blindness "
            "applications also follow without the off-generation-zero premise. ZMod n and Fin n adapters "
            "reuse generic step, iterate and transitivity results while retaining existing public names. "
            "This is an algebraic matrix result only."
        ),
    },
]


def _path_matches(actual: str, expected: str) -> bool:
    actual = actual.replace("\\", "/").casefold()
    expected = expected.replace("\\", "/").casefold()
    return actual == expected or actual.endswith("/" + expected) or expected.endswith("/" + actual)


def _section_refs(hit: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    for evidence in hit.get("evidence_lines", []):
        heading = str(evidence.get("heading", ""))
        for match in re.finditer(r"(?<![\w.])(\d+(?:\.\d+)*)(?=[.)\s:–-]|$)", heading):
            section = match.group(1)
            found.add(section)
            parts = section.split(".")
            found.update(".".join(parts[:index]) for index in range(1, len(parts)))
    return found


def _required_source_status(query_hits: list[tuple[str, list[dict[str, Any]]]],
                            required: dict[str, Any]) -> dict[str, Any]:
    """A path counts only when its own exact source content is searchable."""
    expected_path = str(required.get("path", ""))
    expected_commit = required.get("commit")
    expected_blob = required.get("blob")
    required_sections = [str(value) for value in required.get("sections", [])]
    scope_query_indexes = required.get("scope_query_indexes")
    scope_query_sections = required.get("scope_query_sections", {})
    considered = ([(query, hits) for index, (query, hits) in enumerate(query_hits)
                   if scope_query_indexes is None or index in scope_query_indexes])
    direct_candidates = []
    citation_refs = []
    for query, hits in considered:
        for rank, hit in enumerate(hits, start=1):
            if _path_matches(str(hit.get("source", "")), expected_path):
                if hit.get("direct_content"):
                    direct_candidates.append((query, rank, hit))
            for reference in hit.get("source_refs", []):
                if _path_matches(str(reference.get("path", "")), expected_path):
                    citation_refs.append(reference)
    exact_candidates = []
    for query, rank, hit in direct_candidates:
        commit_ok = expected_commit is None or hit.get("source_commit") == expected_commit
        blob_ok = expected_blob is None or hit.get("source_blob") == expected_blob
        if commit_ok and blob_ok:
            exact_candidates.append((query, rank, hit))
    sections_found: set[str] = set()
    evidence: list[dict[str, Any]] = []
    for _, _, hit in exact_candidates:
        sections_found.update(_section_refs(hit))
        evidence.extend(hit.get("evidence_lines", []))
    missing_sections = sorted(set(required_sections) - sections_found)
    scoped_queries = []
    for index in scope_query_indexes or []:
        if index >= len(query_hits):
            scoped_queries.append({
                "query_index": index, "query": None, "found": False,
                "status": "query_index_out_of_range", "required_sections": [],
                "sections_found": [], "missing_sections": [],
                "candidate_rank": None,
            })
            continue
        query, hits = query_hits[index]
        direct = [(query, rank, hit) for rank, hit in enumerate(hits, start=1)
                  if _path_matches(str(hit.get("source", "")), expected_path)
                  and hit.get("direct_content")]
        exact = [(query, rank, hit) for query, rank, hit in direct
                 if (expected_commit is None or hit.get("source_commit") == expected_commit)
                 and (expected_blob is None or hit.get("source_blob") == expected_blob)]
        query_sections = [str(value) for value in
                          scope_query_sections.get(str(index),
                                                   scope_query_sections.get(index, []))]
        found_for_query: set[str] = set()
        query_evidence: list[dict[str, Any]] = []
        for _, _, hit in exact:
            found_for_query.update(_section_refs(hit))
            query_evidence.extend(hit.get("evidence_lines", []))
        query_missing = sorted(set(query_sections) - found_for_query)
        query_found = bool(exact) and not query_missing
        scoped_queries.append({
            "query_index": index, "query": query, "found": query_found,
            "status": ("found_direct_content" if query_found else
                       "missing_required_section" if exact else
                       "source_pin_mismatch" if direct and
                       (expected_commit is not None or expected_blob is not None) else
                       "not_found"),
            "required_sections": query_sections,
            "sections_found": sorted(found_for_query),
            "missing_sections": query_missing,
            "candidate_rank": exact[0][1] if exact else
                              direct[0][1] if direct else None,
            "evidence_lines": query_evidence[:3],
        })
    scoped_queries_found = (all(item["found"] for item in scoped_queries)
                            if scope_query_indexes is not None else True)
    found = bool(exact_candidates) and not missing_sections and scoped_queries_found
    if found:
        status = "found_direct_content"
        query, rank, hit = exact_candidates[0]
        source_origin = hit.get("source_origin")
    elif exact_candidates and not scoped_queries_found:
        status = "missing_scoped_query"
        query, rank, hit = exact_candidates[0]
        source_origin = hit.get("source_origin")
    elif exact_candidates:
        status = "missing_required_section"
        query, rank, hit = exact_candidates[0]
        source_origin = hit.get("source_origin")
    elif direct_candidates and (expected_commit is not None or expected_blob is not None):
        status = "source_pin_mismatch"
        query, rank, hit = direct_candidates[0]
        source_origin = hit.get("source_origin")
    elif any(ref.get("pin_status") in {"pinned_snapshot", "verified_no_content_match"}
             for ref in citation_refs):
        status, query, rank, source_origin = "pinned_source_loaded_no_content_match", None, None, "pinned_snapshot"
    elif citation_refs:
        status, query, rank, source_origin = "external_reference_only", None, None, "citation_only"
    else:
        status, query, rank, source_origin = "not_found", None, None, None
    # Prefer evidence inside the required sections so the summary shows the
    # passage that justifies its status instead of earlier, unrelated hits.
    prioritized_evidence: list[dict[str, Any]] = []
    for section in required_sections:
        for line in evidence:
            if section in _section_refs({"evidence_lines": [line]}):
                if line not in prioritized_evidence:
                    prioritized_evidence.append(line)
    prioritized_evidence.extend(line for line in evidence
                                if line not in prioritized_evidence)
    return {
        "path": expected_path, "status": status, "found": found,
        "source_origin": source_origin,
        "expected_commit": expected_commit, "expected_blob": expected_blob,
        "required_sections": required_sections,
        "sections_found": sorted(sections_found), "missing_sections": missing_sections,
        "scoped_queries": scoped_queries,
        "candidate_rank": rank, "query": query,
        "evidence_lines": prioritized_evidence[:10],
        "citation_only_refs": citation_refs[:3],
    }


def _case10_change_impact_regression() -> dict[str, Any]:
    """Verify exact source changes alter the linked check input, prose does not."""
    with tempfile.TemporaryDirectory(prefix="d0-proof-impact-") as temp:
        root = pathlib.Path(temp)
        source_rel = "02_REGISTRY/research/native_source.md"
        source_path = root / source_rel
        source_path.parent.mkdir(parents=True)
        source_path.write_text("Declared source normalization premise v1.\n", encoding="utf-8")
        unrelated = root / "unrelated-prose.md"
        unrelated.write_text("Independent historical prose.\n", encoding="utf-8")
        dataset = {
            "root": root,
            "claims": [], "assumptions": [], "formal_support": [], "aliases": [],
            "assembly": {
                "results": [{"id": "native-result", "statement": "Native source application",
                             "evidence": [{"path": source_rel}]}],
                "applications": [{"id": "native-result-to-obligation",
                                  "result": "native-result", "obligation": "native-obligation"}],
                "attempts": [],
            },
            "contract": {"obligations": [], "interfaces": [], "goals": [],
                         "anti_substitutions": [], "synthesis": [],
                         "source_fork_reconciliations": []},
            "presuppositions": {"edges": []},
            "snapshot_commit": "fixture", "source_digests": {},
        }
        before = proof.impact_view(dataset, source_rel)
        before_hash = before["source_snapshot"]["source_sha256"]
        linked = before["declared_impact"][0]["declared_applications"][0]["id"]

        source_path.write_text("Declared source normalization premise v2.\n", encoding="utf-8")
        after_source = proof.impact_view(dataset, source_rel)
        changed_hash = after_source["source_snapshot"]["source_sha256"]

        unrelated.write_text("Edited unrelated historical prose.\n", encoding="utf-8")
        after_unrelated = proof.impact_view(dataset, source_rel)
        unrelated_path = proof.impact_view(dataset, "unrelated-prose.md")
        unchanged_hash = after_unrelated["source_snapshot"]["source_sha256"]
        passed = (before_hash != changed_hash == unchanged_hash and
                  linked == "native-result-to-obligation" and
                  unrelated_path["matches"] == [])
        return {"id": "exact-source-vs-unrelated-prose",
                "status": "pass" if passed else "fail",
                "source_hash_changed": before_hash != changed_hash,
                "unrelated_prose_left_source_hash": changed_hash == unchanged_hash,
                "declared_application": linked}


def run(root: pathlib.Path, limit: int = 5) -> dict[str, Any]:
    queries = [query for case in CASES for query in case["queries"]]
    # Cold-start review needs enough candidates to include verified pinned
    # snapshots behind a top-ranked citation, while the user-facing CLI stays
    # at its smaller default result count.
    all_hits = proof.full_text_search_many(root, queries, max(limit, 18))
    offset = 0
    cases = []
    for case in CASES:
        query_hits = []
        for query in case["queries"]:
            query_hits.append(all_hits[offset])
            offset += 1
        query_pairs = list(zip(case["queries"], query_hits))
        required_status = {}
        for required in case.get("required_sources", []):
            required_status[required["path"]] = _required_source_status(
                query_pairs, required
            )
        for required_path in case["required_refs"]:
            if required_path in required_status:
                continue
            required_status[required_path] = _required_source_status(
                query_pairs, {"path": required_path}
            )
        cases.append({
            "id": case["id"],
            "queries": case["queries"],
            "required_sources": required_status,
            "found_all_required_sources": all(x["found"] for x in required_status.values()),
            "query_results": [
                {"query": query, "top_candidates": [
                    {"path": hit["source"], "matched_terms": hit["matched_terms"],
                     "matched_term_names": hit.get("matched_term_names", []),
                     "query_terms": hit["query_terms"], "source_sha256": hit.get("source_sha256"),
                     "source_origin": hit.get("source_origin"),
                     "direct_content": hit.get("direct_content", False),
                     "source_commit": hit.get("source_commit"),
                     "source_blob": hit.get("source_blob"),
                     "pin_status": hit.get("pin_status"),
                     "evidence_lines": hit.get("evidence_lines", [])[:3],
                     "source_refs": [{"path": ref.get("path"), "commit": ref.get("commit"),
                                      "blob": ref.get("blob"), "pin_status": ref.get("pin_status"),
                                      "section_refs": ref.get("section_refs", [])}
                                     for ref in hit.get("source_refs", [])[:5]]}
                    for hit in hits
                ]}
                for query, hits in zip(case["queries"], query_hits)
            ],
            "scope_review": case["scope_review"],
        })
    dataset = proof.load_dataset(root)
    change_regression = _case10_change_impact_regression()
    return {
        "snapshot_commit": dataset["snapshot_commit"],
        "worktree_dirty": dataset["worktree_dirty"],
        "authority_source_digests": dataset["source_digests"],
        "search_limit": max(limit, 18),
        "search_cases_found_all_sources": sum(c["found_all_required_sources"] for c in cases),
        "search_cases_total": len(cases),
        "benchmark_cases_total": len(cases) + 1,
        "cases": cases,
        "change_impact_regression": change_regression,
        "semantic_scope_review_is_manual": True,
    }


def main() -> int:
    root = proof.ROOT.resolve()
    print(json.dumps(run(root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
