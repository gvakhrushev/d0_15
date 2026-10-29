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
COLD_START_MIN_RESULT_WINDOW = 18
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
            "principalFrameJuliaEndpointChartReadout_hasDerivAt_of_properRoleLorentzPath pathwise link derivative Eq27 Eq28 Julia",
            "principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzPath simultaneous coframe link derivative Julia",
            "jointCoframeAndLorentzPath julia_joint_coframe_link_path_derivative_declarations_2026-10-26",
            "principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzTangent exponential tangent proper Lorentz path",
            "jointCoframeAndLorentzTangent julia_joint_coframe_lorentz_tangent_derivative_declarations_2026-10-26",
            "principalFrameJuliaEndpointChartReadoutAlongLorentzTangent_hasFDerivAt hasFDerivAt_pi",
            "roleLorentzTangentEndpointFDeriv_apply julia_joint_coframe_lorentz_frechet_derivative_declarations_2026-10-26",
            "roleLorentzTangentParameters_finrank roleLorentzTangent_finrank four Julia links 24 coordinates",
            "principalFrameJuliaJointCoframeEndpointReadoutAlongLorentzTangent_hasDerivAt principalFrameJuliaEndpointChartReadoutAlongLorentzTangentInCoordinates_hasFDerivAt roleLorentzTangentParametersEquivCoordinates same Julia query family 16 coframe 24 Lorentz endpoint RolePair coordinates",
            "principalFrameJuliaJointCoframeEndpointReadoutInCoordinates_hasFDerivAt julia_joint_coframe_local_frechet_derivative_declarations_2026-10-26_julia_base_link_frechet_v2",
            "principalFrameJuliaJointCoframeEndpointReadoutAtBaseInCoordinates_hasFDerivAt julia_joint_coframe_base_link_frechet_declarations_2026-10-26_v2",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
            "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "03_FORMALIZATION/D0/Geometry/A4DJuliaLinkPathDifferential.lean",
            "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_endpoint_link_path_derivative_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_joint_coframe_link_path_derivative_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_joint_coframe_lorentz_tangent_derivative_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_joint_coframe_lorentz_frechet_derivative_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_joint_coframe_local_frechet_derivative_declarations_2026-10-26_julia_base_link_frechet_v2.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_joint_coframe_base_link_frechet_declarations_2026-10-26_v2.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_lorentz_tangent_dimension_reuse_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/julia_joint_coframe_tangent_path_declarations_2026-10-26.json",
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
        "scope_review": ("Owner all-jet null-leg inverse and the concrete consumer are distinct. The compiled pathwise derivative composes its Eq. (27)/(28) endpoint readout with proper-Lorentz link paths on the finite CAR carrier. Its joint-path specialization allows coframe, column data and normalized covector to vary pointwise; exact recovery removes the need to assume differentiability of those paths. The tangent corollary integrates each rolewise Lorentz tangent by an exponential path, proves det = 1 along that path, and gives the endpoint derivative at t = 0. The Fréchet specialization proves the full derivative on the product of the four role-indexed Lorentz tangent subspaces, with its action exposed role by role. It reuses the canonical six-dimensional tangent coordinates from A4DSolderMetricCompletion and proves that the four-factor parameter has real dimension 24. A concrete linear equivalence identifies that parameter with Role → RolePair → ℝ, and the coordinate-form Fréchet derivative states the reconstructed generator's transpose action at each role. The new paired path theorem composes exact Eq. (30a) coframe recovery with all four Eq. (27)/(28) endpoint readouts on the same constructed Julia query family: an arbitrary coframe derivative H and a 24-coordinate tangent direction q produce derivative (H, endpoint(q)). The fixed principal-frame Lorentz map and the normalized-covector/nonzero-shift chart conditions remain explicit at every path parameter. This is a joint directional derivative only. The local product theorem proves a full Fréchet derivative on the 16 coframe matrix entries and 24 canonical Lorentz tangent coordinates, conditional on the normalized-covector and nonzero-shift chart conditions throughout a coframe neighborhood. It combines exact coframe recovery with the exact endpoint readout identity, so the covector section need not be differentiable. The new base-link application right-translates those same tangent coordinates to any supplied proper rolewise Lorentz link and gives the derivative after the base-link endpoint action; the base link retains both Lorentz isometry and determinant-one hypotheses. This remains a tangent differential at supplied links, not a claim that the exponential is a global chart. None of these results differentiates a selected Book/action/source, selects a physical price or execution, establishes the variational pullback (31), or closes GR."),
    },
    {
        "id": "positive-nonvacuum-recovery",
        "queries": [
            "positive nonvacuum harmonic cubic fixed nonlinear Brinkmann metric",
            "transverseFivePoint_nonvacuumBrinkmannProfile_eq_source harmonicBrinkmannCubic radial quadratic",
            "nonvacuumProfile_source_eq_finiteMidpointMatterNorm finiteMatterForwardGradient_midpointStep twoComponentMatterNormSq",
            "finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm finiteMatterMidpointHistory chronological rate same two-component stencil source",
            "finiteMatterMidpointHistory_eq_base_add_rateSum chronological midpoint record finite sum endpoint",
            "twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum complete finite history gradient rate energies",
            "finiteMatterMidpointHistory_error_le_refinementBound local midpoint defect sum M h^3 over 24 global O(h^2) uniform mesh points",
            "D0.Analysis.MidpointQuadrature midpointQuadrature_error_abs_le_of_thirdDerivative_bound",
            "sampledMatterMidpointLocalDefect_abs_le sampledMatterMidpointHistory_error_le_refinementBound componentwise uniform mesh C3",
            "native finite matter midpoint exact energy five point source same interval",
            "nonvacuumCubicMidpointSource_matches_record cubicMatterMidpointSample_eq_profile_sub_cubic_error cubicMatterMidpointSample_error_bound",
            "cubic nonvacuum midpoint cumulative matter record componentwise O(h^2) bound",
            "D0.Analysis.sampledVectorMidpointHistory_error_le_refinementBound vector norm Euclidean error duration M h^2 over 24",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorMargin Eq.24 delta over 2 same two-component CAR recurrence Euclidean lift",
            "Eq.24 max u_j in I Psi_j^(h) - Psi(u_j) |I| sup_I Psi''' h^2 / 24 compound midpoint quadrature integral of Psi' fixed small normalized CAR slack survives for all sufficiently fine h",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes h duration over N exists N0 delta over 2 every uniform refinement",
            "sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval ContDiffAt C3 local regularity sampled interval",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_of_pointwiseMargin",
            "D0.Geometry.nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource cubicMatterCoefficientNorm cubicMatterMidpointSample finiteMatterForwardGradient transverseFivePointLaplacian",
            "D0.Geometry.nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource_and_refinement cubicMatterMidpointSample_euclideanError_eq_remainder cubicMatterMidpointSample_euclideanError_le_refinementBound exact Euclidean O(h^2) error same recursive record CAR complement five-point stencil source",
            "nonvacuum_brinkmann_stencil_midpoint_refinement_declarations_2026-10-26.json twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md",
            "03_FORMALIZATION/D0/Geometry/NonvacuumBrinkmannStencil.lean",
            "03_FORMALIZATION/D0/Analysis/MidpointQuadrature.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_brinkmann_stencil_midpoint_refinement_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_brinkmann_stencil_midpoint_c3_error_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_brinkmann_stencil_midpoint_c3_refactor_declarations_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_vector_norm_car_margin_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_vector_norm_uniform_mesh_2026-10-26.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_interval_local_car_refinement_2026-10-27.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_compact_pointwise_margin_2026-10-27.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_cubic_profile_car_margin_2026-10-27.json",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_cubic_profile_same_record_euclidean_refinement_2026-10-27.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md",
                "commit": "8b94198c8dfbdf5983ad0b350b058fb30bb68a54",
                "blob": "63c36b18af67fc1f113f9e33deb13cf43ddf4556",
                "sections": ["7.1", "7.2"],
                "scope_query_indexes": [0, 4, 9],
                "scope_query_sections": {"0": ["7.1"], "4": ["7.2"], "9": ["7.2"]},
            },
            {
                "path": "02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md",
                "commit": "fe5cf335da04cac14e50407b03f98b96be17dc52",
                "blob": "67531a343a0ae707ff0a3830c0e2c9cf2bbc8213",
                "sections": ["7.2"],
                "scope_query_indexes": [14],
                "scope_query_sections": {"14": ["7.2"]},
            },
            {
                "path": "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_compact_pointwise_margin_2026-10-27.json",
                "commit": "a2c20a4dc9feeb5446b41e9e49ea8094bd14f40b",
                "blob": "82574aafa3ea94c61ca28ad9e08980c2974d4b22",
                "scope_query_indexes": [17],
            },
            {
                "path": "03_FORMALIZATION/D0/Geometry/NonvacuumBrinkmannStencil.lean",
                "commit": "423ec9a87553a14c6f484e429a6d3309eeae256a",
                "blob": "07a988011a77ee87aa13d5d816680920d51a3007",
                "scope_query_indexes": [18, 19],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_cubic_profile_car_margin_2026-10-27.json",
                "commit": "119c31ba6df9f02a4b8b491e7658de2e7432a797",
                "blob": "9cfb08a3cbe8ef09d5f1311b6b96ea27378ab611",
                "scope_query_indexes": [18],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_cubic_profile_same_record_euclidean_refinement_2026-10-27.json",
                "commit": "de9fc93ff5a159486a8404ba945ab3e3655f0729",
                "blob": "40171d8756ccf09c1b0627c20bca03a91637b56c",
                "scope_query_indexes": [19],
            },
        ],
        "scope_review": (
            "The compiled NonvacuumBrinkmannStencil result proves the exact five-point "
            "harmonic/radial readout and binds its source norm to the same recursively constructed "
            "midpoint matter record. The time-indexed extension proves that each natural-indexed "
            "history step supplies the exact rate used by that site's profile and proves endpoint "
            "rate-sum and finite-history energy identities. The explicit two-component cubic "
            "family has its exact accumulated midpoint error and componentwise bound. The defect "
            "composition proves a uniform componentwise O(h^2) bound. The shared D0.Analysis Taylor "
            "theorem derives its O(h^3) defect from C^3 regularity and an explicit uniform bound "
            "on the sampled interval; the geometry specialization composes it with the sampled-"
            "history result. The vector-valued Taylor/remainder composition now proves the same "
            "dimension-free constant in Euclidean norm. Its half-margin CAR application is "
            "transported through an isometric Euclidean lift and proved equal to the existing "
            "two-component finite recurrence. C^3 regularity at each point of the sampled interval, vector third-derivative and "
            "envelope bounds remain supplied hypotheses for the local API. The pointwise-margin "
            "corollary assumes global C^3 and pointwise strict chart inclusion, then uses compactness "
            "to derive the uniform derivative and envelope bounds and their positive uniform margin. "
            "The cubic-profile application bounds the Euclidean profile by the sum of its four "
            "coefficient norms on [0,1], derives the pointwise chart margin from that strict "
            "coefficient bound, and composes one eventual CAR threshold with the exact stencil "
            "source on the same recursive matter record. It returns the nonzero initial rate, "
            "but remains a finite-dimensional subset of the source's smooth matter family, not "
            "a reconstruction or selection of the original CAR preparation. "
            "The new uniform-mesh theorem derives an "
            "N0 threshold from the same delta-over-two estimate and proves the existing CAR "
            "complement positive for every N >= N0 with h=duration/N. Section 7.2 supplies the "
            "finite-step Eq. (24) error and states that fixed small normalized CAR slack survives "
            "for sufficiently fine h; the Lean result makes this eventual refinement claim "
            "explicit under the supplied analytic bounds. The actual CAR preparation "
            "and generator are not reconstructed. The exact signed cubic remainder is now lifted "
            "to the Euclidean vector of this same recursive record, with a dimension-free "
            "duration-times-third-derivative-coefficient-times-h-squared over 24 bound. A stronger "
            "cubic corollary returns this error bound together with CAR positivity and the exact "
            "five-point source at every site of every sufficiently fine uniform mesh. "
            "The original CAR construction, 40-to-3-to-1 substitution, all 16+24+2 Euler rows, "
            "and physical native Book/clock/source selection remain separate and open."
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
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_gram_orbit_shared_api_declarations_2026-10-26_julia_base_link_frechet_v2.json",
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
            "finite_gram_orbit_shared_api_declarations_2026-10-26_julia_base_link_frechet_v2.json finiteGram_add_smul_difference_quotient",
            "finite Gram expansion Theta plus t C two sided linear variation exact quadratic term",
            "A4D Solder Metric Completion finiteGram_add_smul_difference_quotient solderMetric_flat_tangent j2DetectorMetricPath_symmetric_difference_quotient",
        ],
        "required_refs": [
            "03_FORMALIZATION/D0/Algebra/FiniteGramTangent.lean",
            "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/finite_gram_orbit_shared_api_declarations_2026-10-26_julia_base_link_frechet_v2.json",
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
            "C_port Z_n Phi_t mixed field cost source Julia recycling",
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
            "actual full-CAR full16 Julia raising entries null u-leg coframe proper links",
        ],
        "required_refs": [
            "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
            "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "03_FORMALIZATION/D0/Geometry/ArchiveJuliaRaisingOperatorReadout.lean",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
                "commit": "fe5cf335da04cac14e50407b03f98b96be17dc52",
                "blob": "734e21ae6bc04ff3446ad15858936d417fdd2e55",
                "scope_query_indexes": [3],
                "scope_query_sections": {"3": ["5.1"]},
            },
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
            "principal frame open chart q null vector transverse variations proper Lorentz endpoint",
            "уравнение 28 открытая окрестность null-вектора поперечные q вариации восстановление endpoint map Julia",
            "Eq 27 nonzero Lorentz norm Gamma Clifford volume inverse recover frame from full raising query",
            "archiveJuliaRaisingQuery_nonNull_gamma_recovery chi endpoint covariance q nonzero",
            "уравнение 27 ненулевой лоренцев норм Clifford volume восстановить перенос из полного raising operator",
            "principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage Eq27 Eq28",
            "покрытие всех ненулевых сдвигов через Eq 27 Eq 28 principalFrameJuliaQueryFamily",
            "archiveJuliaSourceCARRaisingQuery_nonNull_recovery_of_proper_roleLorentz IsRoleLorentz",
            "proper row action Lorentz endpoint det one CAR Julia recovery adapter",
            "principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz",
            "правый Lorentz endpoint одновременно CAR Eq 27 и query Eq 28 один recovered endpoint null leg native raising operator inverse coframe",
            "principalFrameJuliaQueryFamily_recoveredInverseCoframe_hasFDerivAt",
            "principalFrameJuliaQueryFamily_joint_coframe_endpoint_recovery_of_proper_roleLorentz hΓ hΛ",
            "principalFrameJuliaQueryFamily_joint_coframe_all_role_endpoint_chart_coverage_of_proper_roleLorentz hα hShift",
            "archiveJuliaSourceCARRaisingQuery_nonNull_endpoint_map_injective Eq 27 nonzero Lorentz norm q Gamma_x(u) recover U exact CAR raising query all 16 grades",
            "principalFrameJuliaEq26_blind_to_ABSignFlip_links vacuum-column endpoint blindness",
            "archiveJuliaSourceCARRaisingQuery_nonNull_endpoint_map_injective julia_nonnull_endpoint_map_injectivity_declaration_2026-10-26",
            "principalFrameJuliaEq26_blind_to_ABSignFlip_links julia_eq26_link_blindness_declaration_2026-10-26",
            "principalFrameJuliaNonNullQuery_separates_ABSignFlip_links julia_nonnull_query_link_separation_declaration_2026-10-26",
            "archiveJuliaSourceEq27EndpointMapReadout Eq27 endpoint map readout",
            "proper_role_lorentz_joint_recovery_inventory_2026-10-25 principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz",
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
            "ArchivePhaseShift commute_with_shift_implies_diagonal_constant archiveShiftTopology density_uniform_from_commute",
            "Fin finRotate cyclicShiftMatrix finRotateArchiveTopology partial_trace_density_uniform_under_shift",
            "GenerationTensorExactness flavor_blindness_step_of_commute commute_with_shift_entries kronecker_C_I",
            "GenerationTensorExactness flavor_blindness_step_k_of_commute stage2_flavor_blindness_of_commute stage3_tensor_exactness no h_off Nat.add_mod_right Nat.mod_eq_of_lt Fin.ext",
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
    {
        "id": "fixed-sine-weak-readout-c0-pilot",
        "queries": [
            "archive_doubling_sine_weak_pairing_tendsto",
            "one-step estimates composed fixed-torus failure fixed sample sine weak 2/pi",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md",
            "03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementWeakTest.lean",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
             "scope_query_indexes": [0]},
            {"path": "03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementWeakTest.lean",
             "scope_query_indexes": [0]},
            {"path": "02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md",
             "scope_query_indexes": [1]},
        ],
        "scope_review": (
            "The named Lean result proves that the normalized four-role counting pairing of the "
            "specific composed frozen pullback error with the fixed sampled sine tends to 2/pi. "
            "This is a scoped weak-convergence obstruction for that component and sampling convention. "
            "It does not rule out other readouts or establish physical refinement/admission. "
            "The exact public declaration is resolved separately with `show --lean`; its compiled "
            "type, proof dependencies, and trust footprint are preserved in the current declaration "
            "inventory. The #310 owner pin remains in the primary source review and C0 pilot."
        ),
    },
    {
        "id": "cyclic-af-return-without-extra-blank-flag",
        "queries": [
            "7dl cyclic AF original canonical regular input without extra blank flag 88 paired-profile calls 26G 2CX 60SourceI",
            "L=U R U R actual positive loop gain 4 gamma c Herm X two independently varied word occurrences",
            "completed protected Spin identity failure nonscalar scalar cold corner negative control",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "scope_query_indexes": [0, 1, 2],
            },
        ],
        "scope_review": (
            "The pinned #334 §7dl result removes the extra blank-flag resource premise "
            "for one configured cyclic AF source under its full protected-Spin identity, "
            "positive-gain and addressed-profile assumptions. Its 88-call recipe and "
            "operator-source map retain the actual clock/heat debt. Physical AF port "
            "admission, binary-wire completeness, the full old-cut/source transport, "
            "the actual same-execution map into X_N, and selected price rows remain open; "
            "this does not establish physical GR or change GR_closed=false."
        ),
    },
    {
        "id": "canonical-af-tower-source-transport",
        "queries": [
            "canonical AF tower source transport through every earlier cut positive unital P_i",
            "check_tower.py exact Golden transfer 519 checks full defining block GNS contraction 512 cuts",
            "delta_j K source history s over C_j P chain protected Spin ordinary Book trace",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 1, 2],
            },
            {
                "path": "02_REGISTRY/research/A4D_CANONICAL_AF_TOWER_SOURCE_TRANSPORT_2026_10_28.md",
                "commit": "48500384e9a25b25a6a0f54911f5af50c2bc1625",
                "blob": "d8a4c467c225587e88525b2d42dcb785e381b38d",
                "scope_query_indexes": [0],
            },
        ],
        "scope_review": (
            "The exact positive unital map transports every variation of the declared "
            "canonical copy-uniform profile through earlier AF cuts and retains its full "
            "operator source before the ordinary Book trace. The proof consumes the §7dl "
            "word and does not replay the 88-call device. It does not establish physical AF "
            "actuation, all-physical-X_N variation completeness, transport from another "
            "parked past, Lean formalization, or GR closure; GR_closed=false."
        ),
    },
    {
        "id": "nontrivial-canonical-prefix-source-correction",
        "queries": [
            "7dm retain nontrivial original prefix canonical AF old cut source correction DJ/w 0.00378462083186945",
            "K_xi Delta_a Z_j full matrix history source sum Y_(j,a) Delta retained prefix",
            "guard history debt 7.653 Bxi Lambda 133 checks two SourceI 52 columns",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 1, 2],
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "commit": "d8d4e15488e483992fa63d6acc5d8053c2752ef5",
                "blob": "c79e6019579f716c2935aee8de9314d0607b3a1a",
                "scope_query_indexes": [0],
            },
        ],
        "scope_review": (
            "The pinned #334 §7dm result retains the actual nontrivial prefix and its "
            "matrix-past source term for the declared canonical copied-port profile. "
            "It proves neither physical admission of that profile nor completeness over "
            "all X_N variations; no Lean/CI run or selector is added, and GR_closed=false."
        ),
    },
    {
        "id": "canonical-binary-af-endpoint-and-finite-source",
        "queries": [
            "binary AF common inventory G CX SourceI 107529216 1154 132 original regular modes 33448 65536",
            "Literal Golden CX SourceI synthesis canonical AF loop endpoint run-length encoded ordinary primitive words high-precision powers",
            "complete compiled endpoint orthogonality 512 columns binary RLE native words",
            "binary AF loop actual finite source contrast exact source estimate full heat bound 33448 65536",
            "existing literal native prefix strict nonzero source zero source canonical identity prefix",
            "binary word receipt RLE files user archive ordinary optimized repeat results byte identical",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 1, 2, 3, 4],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_binary_af_actuation_2026-10-28/check_binary_af.py",
                "commit": "9f5b757f699d7310ea69c0c889037f614533b4f7",
                "blob": "dafb228c94468ff83b73f62e0d5792eba832b948",
                "scope_query_indexes": [1],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_binary_af_actuation_2026-10-28/result.json",
                "commit": "9f5b757f699d7310ea69c0c889037f614533b4f7",
                "blob": "52a9dd556782263ca64b9210c2a9d32cb5df045e",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_binary_af_actuation_2026-10-28/RUN_RECEIPT.json",
                "commit": "56672c24a78d95c3a13a095223a18fc7ad84811a",
                "blob": "e6673d32966dec54ed7712e0070d367495f41b16",
                "scope_query_indexes": [5],
            },
            {
                "path": "02_REGISTRY/research/A4D_BINARY_AF_LOOP_FINITE_SOURCE_2026_10_28.md",
                "commit": "5a6d10031efc97dd7d02c43cf9568201dbc2ab85",
                "blob": "dba92719a208aed5245329060b2aadc6c08c3dbe",
                "scope_query_indexes": [3],
                "scope_query_sections": {"3": ["5"]},
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "commit": "3ba25a162a7160c9a5c7692f19e5d8a8b9bf52e9",
                "blob": "363dee64772769eee25888a184b5edbdf64e83e9",
                "scope_query_indexes": [4],
                "scope_query_sections": {"4": ["1000"]},
            },
        ],
        "scope_review": (
            "The pinned #334 result emits RLE words from the declared binary G/CX/SourceI "
            "grammar and checks endpoint and finite-price controls. The later canonical-loop "
            "source proves a scoped finite source contrast on the explicit binary extension; "
            "the retained-marker result applies only when phase addresses vary independently "
            "after a nontrivial prefix, with zero source at the canonical identity prefix. "
            "Neither proves physical binary-interface admission, physical input preparation, "
            "all raw-gate source faults, or the full intermediate future-test domain; "
            "GR_closed=false."
        ),
    },
    {
        "id": "paid-binary-input-full-same-execution-book-price",
        "queries": [
            "generated binary input literal forward words complete Book price",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "commit": "7c079c0180de6e6e12edbd8e79c4628f5048deae",
                "blob": "7cc94351706b15859d1719aed7160b77314ac4ca",
                "scope_query_indexes": [0],
                "scope_query_sections": {"0": ["1012"]},
            },
        ],
        "scope_review": (
            "The pinned #334 result constructs a finite positive binary input and binds its "
            "paid preparation, loop, inverse, generated cuts, full heat and feedback price "
            "on one declared X_run sector. The input approximation does not prove source-jet "
            "equality or exact archive-law membership. Physical blank supply, compulsory "
            "execution admission, complete physical Cost-Info selection, the all-42 source "
            "norm, common GR refinement and Lean formalization remain open; GR_closed=false."
        ),
    },
    {
        "id": "native-stationary-recording-seed-whole-word-source",
        "queries": [
            "native stationary recording seed whole word source full Book 496 real skew directions",
            "full word cotangent actual stage suffix transport stationary prefix positive return source matrix endpoint",
            "full_Book_price five_point_full_price_error full_modes 578 stationary seed result",
            "ancestral marker pullback zero return source scalar future T QUERY positive saddle",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/A4D_NATIVE_STATIONARY_RECORDING_SEED_2026_10_28.md",
            "02_REGISTRY/research/sources/d0_native_stationary_seed_2026-10-28/check_seed.py",
            "02_REGISTRY/research/sources/d0_native_stationary_seed_2026-10-28/result.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 1, 2, 3],
            },
            {
                "path": "02_REGISTRY/research/A4D_NATIVE_STATIONARY_RECORDING_SEED_2026_10_28.md",
                "commit": "d9ef0b0558fcabbc097ecf2024a10b31ec0b5852",
                "blob": "1766cb44e82a276d14a5546257b85a59beeab506",
                "scope_query_indexes": [1],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native_stationary_seed_2026-10-28/check_seed.py",
                "commit": "aeb722a162c008e5e23a7fde39479eb62e3296cf",
                "blob": "789dfebea5efa1e0b7fda64dfce8cb8c4ee8797b",
                "scope_query_indexes": [0, 1],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native_stationary_seed_2026-10-28/result.json",
                "commit": "24ca8e86271c1139e6386387ec1818890fe42549",
                "blob": "561f4a3b7a5ce1a058e6b380705e3ea60a96bc7f",
                "scope_query_indexes": [2],
            },
        ],
        "scope_review": (
            "The exact five-call nonidentity seed has zero full-word matrix source on its fixed "
            "rank/stage/clock/scene chart and preserves zero ancestral return source under a "
            "scoped scalar future with positive gain. It removes the stationary-prefix premise "
            "only for this alternative initial execution; it does not repair the prior recorded "
            "history, replay the large 7do preparation, select physical actuation, resolve the "
            "future QUERY source, identify geometry, or derive the full physical variation "
            "domain. The seed is a saddle; local and published numeric measurements differ by "
            "at most 4.66e-12 in absolute value. No Lean/CI or GR closure is claimed; "
            "GR_closed=false."
        ),
    },
    {
        "id": "canonical-af-stationary-family-archive-seed",
        "queries": [
            "canonical Fibonacci AF tower A2 M3 M2 to A5 M13 M8 stationary reflection archive exact Z[p] GNS rank104",
            "PASS_CANONICAL_AF_STATIONARY_REFLECTIONS 1970 checks 233 complex left directions 128 archive matrix units",
            "nonscalar future cold product A K0 prefix source [A* A, K0 K0*] commute returned escaping",
            "fixed A0 archive even kernel parity per inherited label no G CX SourceI native word GR_closed=false",
            "exact native stationary recording seed whole-word source scalar-return future 496 real skew directions",
            "original A0 archive 7do preparation source matched-preparation memo 185ab21c",
            "existing task brief original A0 archive 7do preparation-source parent work key application checkpoint",
            "PASS_CANONICAL_AF_STATIONARY_REFLECTIONS canonical stationary reflections",
            "complex_left_directions_checked protected_archive_units_checked PASS_CANONICAL_AF_STATIONARY_REFLECTIONS",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/A4D_NATIVE_STATIONARY_RECORDING_SEED_2026_10_28.md",
            "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
            "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
            "02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/check_canonical_seed.py",
            "02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/result.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 1, 2, 3],
            },
            {
                "path": "02_REGISTRY/research/A4D_NATIVE_STATIONARY_RECORDING_SEED_2026_10_28.md",
                "commit": "d9ef0b0558fcabbc097ecf2024a10b31ec0b5852",
                "blob": "1766cb44e82a276d14a5546257b85a59beeab506",
                "scope_query_indexes": [4],
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "commit": "185ab21cb165cbf420291a6d8a2056dc366e5275",
                "blob": "98c80d9aea2377d3a40dc2b381f644a0ca2e896b",
                "scope_query_indexes": [5],
            },
            {
                "path": "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
                "commit": "185ab21cb165cbf420291a6d8a2056dc366e5275",
                "blob": "ad5b4a9bb8e376bd689d3e951b5d5afe308c170e",
                "scope_query_indexes": [6],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/PROOF_RU.md",
                "commit": "8cf4c25b4d3e34a3ce9e7e457049aacc918388d0",
                "blob": "f8675130936e45d9718781d38ef5b762ebaf0eba",
            },
            {
                "path": "02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/check_canonical_seed.py",
                "commit": "6415f5c8e106e48dd20c2bf72d625b33f52b2360",
                "blob": "49d89fa52015c55e7fb0b31dbdef6e158b552e1d",
                "scope_query_indexes": [7],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_canonical_stationary_family_2026-10-28/result.json",
                "commit": "d200d411bce62fe42fe93096d1b36319936561db",
                "blob": "e34f7444fb743d230b0a01b878c927f584d42306",
                "scope_query_indexes": [8],
            },
        ],
        "scope_review": (
            "The pinned #334 proof replaces the binary boundary only for mathematical "
            "stationary-family existence on the original canonical Fibonacci AF tower: "
            "A2=M3+M2 to A5=M13+M8, canonical GNS rank 104, and exact Z[p] expectation "
            "onto C=(diag(0,1,0),I2). Its inherited AF inclusions retain the same return "
            "corner and the fixed original A0 archive, with an even-kernel parity criterion "
            "per old central type and, for the stronger archive law, per inherited label. "
            "The exact commuting-block future criterion applies to a factored cold product "
            "AK0 and the prefix return term only; future heat/source and arbitrary "
            "interference remain live. The 1970-check result does not prove a native "
            "G/CX/SourceI word, physical canonical preparation, spacetime refinement, "
            "all-42 source transport, Lean/CI, or field-equation selection. It is a separate "
            "boundary from the five-call binary seed; GR_closed=false."
        ),
    },
    {
        "id": "archive-preserving-binary-seed-full-query-source",
        "queries": [
            "archive-preserving seed CX(6,12) original A0 archive complete Spin oldRIGHT 16-wire boundary rank16",
            "43-call words A B inventory 25 CX 4 G 14 SourceI full 65536 carrier paired Hodge modes",
            "scalar future all five seed occurrence sources zero positive gain 38 future occurrence sources 16g dual 608g",
            "A report effect p squared B zero same inventory full H+J price gap 7.2042261899642877793",
            "nonscalar future M diag (2p6-1)^2 I8 I8 cold product commutes Q0 prefix sources zero",
            "literal 41-call C 36 future occurrences local dual 16 gC full independent dual 576 gC true N41 full price",
            "native reentry countercontrol repeated CX full corner I16 cold product diag I8 0 arbitrary continuation",
            "434 explicit checks PASS checker SHA256 published receipt SHA256 Python 3.9.6 SymPy 1.14.0 mpmath 1.3.0",
            "reporter controls actual field task control graph physical X_N selected full Cost-Info all42 source map GR_closed false",
            "same #334 existing task checkpoint no new research task canonical AF nonscalar theorem preserved",
            "canonical archive stationary family AF proof and native binary actuation distinct primitive interfaces",
            "archive-preserving-binary-query-replay-2026-10-28-b728 exact stdout stderr source blobs replay manifest",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
            "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": list(range(12)),
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "commit": "b728d85246c6bcf75b84dadaef294e91f5f50b15",
                "blob": "a5fc2aafd237ab41a315633227d44153d144e27a",
                "scope_query_indexes": [2],
            },
        ],
        "scope_review": (
            "The pinned b728d852 continuation changes the binary seed placement to CX(6,12), "
            "preserving the original A0 archive and full Spin/oldRIGHT algebra on the stated "
            "16-wire boundary. For the literal 43-call A/B pair, the paid QUERY is on right11; "
            "A has zero return source on its five actual seed occurrences and positive gain, "
            "but its 38 future occurrences have nonzero local source and exact independent "
            "stage-max dual 608g. Fully stationary B changes the all-input report effect from "
            "p^2 to zero and is not a substitute for the required report; the exact complete "
            "H+J price gap is retained. A separate literal 41-call word applies the incoming "
            "nonscalar commuting-block criterion under a proved cold-product factorization: "
            "the old prefix rows vanish while all 36 future occurrence sources remain. The "
            "reentry control blocks extension to arbitrary futures. Exact checker and receipt "
            "replay 434/434 in ordinary and optimized Python and match published bytes. This "
            "does not derive the field/task/control pullback, physical X_N norm, autonomous "
            "controller, selected full Cost-Info, all42 map, continuous gates, or GR refinement; "
            "no Lean/CI or physical admission is claimed, and GR_closed=false."
        ),
    },
    {
        "id": "canonical-af-original-julia-source-lift",
        "queries": [
            "four-level canonical AF lift original Julia return source Hermitian zero-Walsh row E4 V(a) paired weight p^3",
            "ordered noncommuting history corner K_n C_n all jets same original retained return logdet 16384 histories",
            "A2->A5 seed E(W*)=Q full action -6d log(1-zeta)+7 J_DATA per spectator",
            "DATA channel not original full128 normalized Choi distance diamond norm O(nu^4) fixed boost collar fine-record observations",
            "status PASS_AF_ORIGINAL_JULIA_RETURN_SOURCE_TRANSPORT new_checks",
            "G/CX/SourceI word physical admission full-history law full heat all-42 Einstein source Lean CI GR_closed=false",
            "check_history_source.py original CAR Julia Walsh Golden retained multi-tick tape",
            "Четыре уровня исходной AF-башни воспроизводят исходный Julia-источник",
            "EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE existing owner task checkpoint",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/A4D_CANONICAL_AF_ORIGINAL_JULIA_SOURCE_LIFT_2026_10_28.md",
            "02_REGISTRY/research/sources/d0_af_native_julia_source_lift_2026-10-28/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_af_native_julia_source_lift_2026-10-28/check_af_julia_lift.py",
            "02_REGISTRY/research/sources/d0_af_native_julia_source_lift_2026-10-28/result.json",
            "02_REGISTRY/research/sources/d0_original_retained_history_source_2026-10-28/check_history_source.py",
            "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": list(range(9)),
            },
            {
                "path": "02_REGISTRY/research/A4D_CANONICAL_AF_ORIGINAL_JULIA_SOURCE_LIFT_2026_10_28.md",
                "commit": "a8635c65a6af41c8fbafc605f7c43d0713b4591f",
                "blob": "6ab2096af0b622e36e2ce15d9a03533c4c32b071",
                "scope_query_indexes": [0, 1, 3],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_af_native_julia_source_lift_2026-10-28/PROOF_RU.md",
                "commit": "3821e4035cae1c723daed8cf3c59dbeb99890ba8",
                "blob": "d4e9c4e5e4e707612a7b368f5bc80f69ef31cfe2",
                "scope_query_indexes": [7],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_af_native_julia_source_lift_2026-10-28/check_af_julia_lift.py",
                "scope_query_indexes": [4],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_af_native_julia_source_lift_2026-10-28/result.json",
                "scope_query_indexes": [4],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_original_retained_history_source_2026-10-28/check_history_source.py",
                "scope_query_indexes": [6],
            },
            {
                "path": "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
                "commit": "b728d85246c6bcf75b84dadaef294e91f5f50b15",
                "blob": "ace7b08c708cbdda03a27faf8610edbb8f5de37f",
                "scope_query_indexes": [8],
            },
        ],
        "scope_review": (
            "The existing #334 owner derives exact original-row return-source and all-jet "
            "transport through a four-level canonical AF inclusion and composes it with the "
            "owned A2-to-A5 stationary seed. This removes the product-of-cold-blocks premise "
            "for these actual nested lifts only; a repeated-seed reentry control rejects "
            "arbitrary coherent continuation. All 233 old-left return rows vanish under the "
            "proved commutant condition, while the future source remains nonzero with true "
            "multiplicity. The unconditioned DATA channel differs from original full128; only "
            "the stated DATA-only diamond bound applies. No native G/CX/SourceI word, physical "
            "admission, full-history law, full heat map, all42 Einstein source, Lean/CI, or GR "
            "closure is established; GR_closed=false."
        ),
    },
    {
        "id": "canonical-af-full-heat-geometric-source",
        "queries": [
            "canonical AF full H+J source exact positive scalar times calibrated direct-click reporter c(P) Gamma",
            "homogeneous internal clock K(9,11,13) heat derivative ratio 1/64 N >= 4 359 harmonics",
            "233 independently varied old-left A5 full return and thermal source zero even when new field changes heat",
            "Hermitian DATA-corner delta C operator apparatus remainder C3 horizontal raw-vertical norm",
            "PASS_CANONICAL_AF_FULL_HEAT_SCALAR_SOURCE 3625 checks pointwise field heat",
            "42 coordinate pointwise Palatini jet all33 scene eigenvalues 297731200 full Hodge modes source-chain error",
            "original full128 a=N0 remains unidentified no native G/CX/SourceI compiler no fine-record equivalence GR_closed=false",
            "Каноническая AF-реализация прежнего полевого отчёта: точный источник ВСЕЙ цены",
            "check_full_heat_source.py PASS_CANONICAL_AF_FULL_HEAT_SCALAR_SOURCE status CHECKS",
            "EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE existing #334 task checkpoint owner",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/A4D_CANONICAL_AF_FULL_HEAT_GEOMETRIC_SOURCE_2026_10_29.md",
            "02_REGISTRY/research/sources/d0_af_full_heat_geometric_source_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_af_full_heat_geometric_source_2026-10-29/check_full_heat_source.py",
            "02_REGISTRY/research/sources/d0_af_full_heat_geometric_source_2026-10-29/result.json",
            "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": list(range(10)),
            },
            {
                "path": "02_REGISTRY/research/A4D_CANONICAL_AF_FULL_HEAT_GEOMETRIC_SOURCE_2026_10_29.md",
                "commit": "bbbc85281b1569be229d1b9869fdea7bdfa6780b",
                "blob": "551636b9d6670490a980b59912548f07216f4fe7",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_af_full_heat_geometric_source_2026-10-29/PROOF_RU.md",
                "commit": "9e1577a2d5b2663001ac94220aea28c41f038005",
                "blob": "53651843f89ccd7d1f2dd8e64c663703f9acedd2",
                "scope_query_indexes": [7],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_af_full_heat_geometric_source_2026-10-29/check_full_heat_source.py",
                "scope_query_indexes": [8],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_af_full_heat_geometric_source_2026-10-29/result.json",
                "scope_query_indexes": [4],
            },
            {
                "path": "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
                "commit": "b728d85246c6bcf75b84dadaef294e91f5f50b15",
                "blob": "ace7b08c708cbdda03a27faf8610edbb8f5de37f",
                "scope_query_indexes": [9],
            },
        ],
        "scope_review": (
            "The exact full H+J cotangent now equals a positive scalar times the owned "
            "calibrated direct-click field reporter on its declared canonical AF graph; "
            "full heat is retained, not discarded. A rational bound gives relative thermal "
            "correction below 1/64 for the fixed homogeneous K(9,11,13) internal clock, "
            "N>=4 and the stated c range. All 233 old-left A5 variations have zero full "
            "return-plus-heat source, while matrix DATA-corner and pointwise 42-coordinate "
            "jets are checked. The reporter remains distinct from original full128 a=N0. "
            "No native G/CX/SourceI compiler, physical admission, full fine-record law, "
            "full42 mesh root, physical comparison-domain theorem, Lean/CI, or GR closure "
            "is established; GR_closed=false."
        ),
    },
    {
        "id": "canonical-af-native16-retained-report-fibre",
        "queries": [
            "native16 retained joint-record effect full INTERNAL H+J source actual 16-call positive G CX SourceI word",
            "d0_native16_retained_report_fibre_2026-10-29 288 checks c20bd627 source checker expected receipt replay manifest",
            "actual retained report wire10 seed-copy12 wire12 oldRIGHT15 M p Q_return Delta zero endpoint tangent",
            "same terminal WORK isometry low27 complete endpoint involution all16 input columns 16 paid calls",
            "full H+J first source actual native G stage15 7.41376417151667 fixed effect return minimum not global",
            "16 primitive occurrence pullbacks same actual joint effect no linked inverse legs full heat source",
            "next compute P M K Delta D Delta existing field report compiler upstream rows all42 norm gain heat",
            "EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE 4b30fcb4 same owner PR334 no new task assembly node",
            "Native16 полный источник совместной записи физическое admission Cost-Info GR_closed false",
            "check_native16.py d5c987f4 native_full_source_completion PINS DomainMatrix Path.cwd",
            "expected_receipt.json old_w_interval pair_future_charpoly native_full_source_completion",
            "7dq ARCHIVE SEED QUERY RECEIPT 7do PAID BINARY INPUT RECEIPT exact upstream receipt fixture",
            "source_manifest.json d0-native16-retained-report-fibre-intake-v1 c07286147ba90464ca89e5d47ae42f36633f44ec",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/upstream_section_7dr.md",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/check_native16.py",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/expected_receipt.json",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/inputs/upstream_receipts.md",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/replay_native16.py",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/replay_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/source_manifest.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/PROOF_RU.md",
                "scope_query_indexes": [8],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/upstream_section_7dr.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/check_native16.py",
                "scope_query_indexes": [9],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/expected_receipt.json",
                "scope_query_indexes": [10],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/inputs/upstream_receipts.md",
                "scope_query_indexes": [11],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/replay_native16.py",
                "scope_query_indexes": [1],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/replay_manifest.json",
                "scope_query_indexes": [1],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_retained_report_fibre_2026-10-29/source_manifest.json",
                "scope_query_indexes": [12],
            },
        ],
        "scope_review": (
            "The exact 16-call G/CX/SourceI completion realizes a retained joint record and, "
            "for its actual effect E_M, proves Delta=E_M-K* K=0 and the full fixed INTERNAL "
            "H+J source pullback on every endpoint unitary direction. This removes the "
            "independent return-source obstruction for this execution while retaining its "
            "unrestricted nonzero source and full absolute price; the global H+J minimum is "
            "not proved. The 27/32-call controls "
            "remain valid for their own executions; their obstruction is not universal over "
            "all implementations. No physical admission, autonomous controller/task choice, "
            "complete selected Cost-Info, boundary/clock equations, all42 refinement, Lean/CI "
            "or GR closure is established; GR_closed=false."
        ),
    },
    {
        "id": "canonical-af-native16-return-record-compiler",
        "queries": [
            "native return record compiler C_R W C_R actual joint record effect original corner Delta zero paid copy layers",
            "0f2e421fda2029df92b174c39f594160ce31294f 279 checks 5ca575b8 ordinary optimized repeat same receipt",
            "existing 31-call 37-call 25CX 2G 10SourceI A=(0,11,12) R=(7,8,9) 1030553600 modes",
            "RETURN RECORD COMPILER CHECKER complete_return_record native_execution",
            "expected_receipt.json actual_B37_minus_B31_interval independent_upstream 0.000000401477956345875",
            "field_compiler_source.md 7cq direct-click read-once compiler original nonlinear field Bernstein kernel errors",
            "7dr RETAINED REPORT FIBRE RECEIPT 7do PAID BINARY INPUT RECEIPT exact source fixture",
            "source_manifest.json d0-native16-return-record-compiler-intake-v1 c1417beeb828773482bda67b6e9db146a5ce04d9",
            "native_execution.py GOLDEN_FIELD G_LOCAL SOURCE_I_LOCAL complete_return_record validate_execution",
            "Native16 оплаченная компиляция полного return-record independent upstream preparation физическая admission GR_closed false",
            "replay_return_record.py replay_outputs_byte_identical runtime_matches_published_receipt stderr_empty_for_all_runs",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/upstream_section_7ds.md",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/check_return_record.py",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/expected_receipt.json",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/inputs/field_compiler_source.md",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/inputs/upstream_receipts.md",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/replay_return_record.py",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/replay_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/source_manifest.json",
            "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/PROOF_RU.md",
                "scope_query_indexes": [9],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/upstream_section_7ds.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/check_return_record.py",
                "scope_query_indexes": [3],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/expected_receipt.json",
                "scope_query_indexes": [4],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/inputs/field_compiler_source.md",
                "scope_query_indexes": [5],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/inputs/upstream_receipts.md",
                "scope_query_indexes": [6],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/replay_return_record.py",
                "scope_query_indexes": [10],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/replay_manifest.json",
                "scope_query_indexes": [10],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_return_record_compiler_2026-10-29/source_manifest.json",
                "scope_query_indexes": [7],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py",
                "scope_query_indexes": [8],
            },
        ],
        "scope_review": (
            "The same-owner continuation applies the 7dr gap calculation to a declared binary "
            "native compiler by surrounding the existing word with two paid CX record-copy "
            "layers using already initialized, untouched reserve wires. It proves the old "
            "return corner is preserved and the joint zero-record effect equals K* K exactly; "
            "at a full reflection endpoint the complete fixed INTERNAL H+J source is its real "
            "record source. Original control rows and absolute price are retained, and the "
            "actual new-clock heat source remains for nonreflection endpoints. A paid 37/55-call "
            "application and independent upstream-preparation identity are checked with hostile "
            "partial-copy controls. It does not establish physical admission or reserve supply "
            "for every larger "
            "field compiler, selected Cost-Info, all42 refinement, Lean/CI or GR closure; "
            "GR_closed=false."
        ),
    },
    {
        "id": "record-saturated-native-field-stencils",
        "queries": [
            "fixed Golden native source stencils with an actual retained record all expanded calls positive G CX SourceI large repeats specified not iterated or claimed run on hardware 42 variable test local Palatini jet not a lattice GR root or a runtime quantum field decoder",
            "check_record_saturated_field.py PASS_NATIVE_RECORD_SATURATED_42_SOURCE_STENCILS 867 checks",
            "fixed Golden native16 16-call word actual active wires 0 6 10 11 12 13 14 full source rank 16",
            "exact endpoint cotangent identity all 16 primitive occurrence pullbacks actual stage15 G source",
            "42 pointwise coframe connection matter coordinate stencil interval derivative full recorded source h 1/1000",
            "positive-word-with-exact-repetitions finite fully unrolled repetitions compact notation seed Z_query I_G I_Z word_template same_inventory expanded_calls_per_word",
            "result.json max_coordinate_error dual_max_norm_error proved bound native source true 42 rows",
            "same full carrier reflection heat contrast exactly zero oldRIGHT inactive blank factor 256",
            "PROOF_RU local NumPy RuntimeWarning divide by zero overflow invalid cause unresolved stderr preserved",
            "replay_record_saturated_field.py ordinary optimized repeat output byte identical captured warnings",
            "replay_manifest.json numpy scipy python runtime warning categories warning resolved false",
            "source_manifest.json owner commit 418afd58 blob 81d78ce6 input commit 4b30fcb4 SHA256",
            "D0_PROOF_ARCHITECTURE_AND_FORMALIZATION supporting finite calculation GR_closed false no Lean CI",
            "owner source pin check_record_saturated_field.py commit 418afd58c741713a60036a90f8246060d774fd56 blob 81d78ce6ebcc3e9d98bceaacbd61ed0328943da9 actual retained record fixed Golden source stencils",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/check_record_saturated_field.py",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/result.json",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/programmes.json",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/replay_record_saturated_field.py",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/replay_manifest.json",
            "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/source_manifest.json",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 12],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/PROOF_RU.md",
                "scope_query_indexes": [8],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/check_record_saturated_field.py",
                "commit": "418afd58c741713a60036a90f8246060d774fd56",
                "blob": "81d78ce6ebcc3e9d98bceaacbd61ed0328943da9",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/result.json",
                "scope_query_indexes": [6],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/programmes.json",
                "scope_query_indexes": [5],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/replay_record_saturated_field.py",
                "scope_query_indexes": [9],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/replay_manifest.json",
                "scope_query_indexes": [10],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_record_saturated_native_field_2026-10-29/source_manifest.json",
                "scope_query_indexes": [11],
            },
        ],
        "scope_review": (
            "The newest #334 addition is a pinned executable checker for one fixed native16 "
            "record-saturated word and 42 pointwise coframe/connection/matter stencils. Its "
            "local ordinary, -O and repeat outputs agree and report 867 checks, but each run "
            "emits captured NumPy RuntimeWarnings during matrix multiplication; their cause "
            "is unresolved, so the replay is not described as warning-free or as proving the "
            "warnings harmless. The 85 Golden word descriptions are compact and the largest "
            "word is not executed as hardware. This does not prove the physical variation "
            "domain, runtime field compiler, a 42-row finite-mesh root, selected Cost-Info, "
            "Lean/CI or GR closure; GR_closed=false."
        ),
    },
    {
        "id": "native16-whole-book-price-graph",
        "queries": [
            "owner memo source pin path A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md commit 22b4e3f430ddb7d8dd7af6e734f5e63225edd056 blob 1e81dd0151eea362fedacc008293bcf4f0c7d806 one terminal record layer literal full Book price independent preparation 93 exact checks",
            "check_one_sided_price.py changed native post-record compiler complete literal Book price actual Golden CX SourceI words",
            "source_manifest.json d0-native16-whole-book-price-graph-intake-v1 integrated_artifacts checker_inputs upstream memo_blob task_blob",
            "B37_minus_B34 B52_alt_minus_B52_base whole_price post34 old_two_sided37",
            "Q_gap logdet D_E logdet D_K positive gap zeta over a trace Delta complete original feedback price",
            "actual same initial isometry 34 call 37 call full price saving paid shorter clock 0.11068705792869126234",
            "52 call preparation alternative same inventory changes retained report complete price decrease 0.0000072042261899642877793",
            "all512 active columns all34 actual suffixes 93 exact checks full physical rank16 thermal dimension65536",
            "literal Book03.25 H+J no additional Shannon von Neumann fitted Info term correction 7ds",
            "ordinary optimized repeat byte identical published receipt stderr empty replay manifest Python 3.9.6",
            "source_manifest.json d0-native16-whole-book-price-graph-intake-v1 inputs/upstream_receipts.md d6dbe367a71f4e0aff666aad2eb963134296d0ba18f99821539ba27e476173a4 frozen_receipt_inputs",
            "A1_34 estimate corrected exact rational bound 1.92095 whole heat remains 93 checks full endpoint cotangents all34 suffix pullbacks",
            "D0_PROOF_ARCHITECTURE_AND_FORMALIZATION supporting compiler price graph physical admission X_N Cost-Info Lean CI GR_closed false",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/upstream_section_7dt.md",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/upstream_task_7dt.md",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/check_one_sided_price.py",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/expected_receipt.json",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/inputs/upstream_receipts.md",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/replay_whole_book_price.py",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/replay_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/source_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/replay/ordinary_stdout.json",
            "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
            "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [12],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/PROOF_RU.md",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/upstream_section_7dt.md",
                "scope_query_indexes": [3, 4, 5, 6, 8],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/upstream_task_7dt.md",
                "scope_query_indexes": [11],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/check_one_sided_price.py",
                "scope_query_indexes": [1],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/expected_receipt.json",
                "scope_query_indexes": [3],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/replay_whole_book_price.py",
                "scope_query_indexes": [9],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/replay_manifest.json",
                "scope_query_indexes": [9],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/source_manifest.json",
                "scope_query_indexes": [2, 10],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_native16_whole_book_price_graph_2026-10-29/replay/ordinary_stdout.json",
                "scope_query_indexes": [3],
            },
            {
                "path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
                "commit": "22b4e3f430ddb7d8dd7af6e734f5e63225edd056",
                "blob": "1e81dd0151eea362fedacc008293bcf4f0c7d806",
                "scope_query_indexes": [0],
            },
            {
                "path": "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md",
                "commit": "22b4e3f430ddb7d8dd7af6e734f5e63225edd056",
                "blob": "6f34289104bb71b593e53c6440d827e3182a249f",
                "scope_query_indexes": [0],
            },
        ],
        "scope_review": (
            "The latest #334 source composes a fixed one-sided terminal record layer with the "
            "literal complete Book03.25 H+J price. It removes the reflection requirement for "
            "saturation of the declared graph, keeps positive Q_gap for changed records, and "
            "corrects §7ds: the literal H+J definition has no extra Info summand. The exact "
            "93-check source and receipt replay byte-identically with empty stderr. Physical "
            "admission of reserve/initial-boundary resources, the full physical X_N, selected "
            "task/record/Cost-Info, independent clock/boundary equations, larger-field "
            "refinement, Lean/CI and GR closure remain unproved; GR_closed=false. "
            "Its frozen 7ds/7do fixture remains a required reference and is retrieved "
            "through the source manifest's exact artifact hash because those receipt "
            "blocks recur in later packets."
        ),
    },
    {
        "id": "native16-record-implementation-fibre",
        "queries": [
            "owner memo A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md commit f23f9149c470051b35acc3fac42f3fecdba084ab blob 21e07fc00279bd897baeefceba8317b1e898107a 7du Admit implementations by their full recording map",
            "Cal(D) D j=C j finite recording implementation predicate actual complete operation all input coherences equation 1085 7du",
            "D=C T completion fibre T identity on ran(j) arbitrary unitary on orthogonal complement full heat feedback derivative zero horizontal field source unchanged",
            "three copied bits minimum three cross CX Schmidt rank 8 unique operator C all unoccupied columns",
            "two 35-call native words same 23 CX 2 G 10 SourceI same all 64 ready columns prepared prefixes terminal state different full operator",
            "full512 first spectral character difference 2048u strict rational complete Book heat price separation all higher windings bounded",
            "negative recorder fault pointer effects and rereading unchanged outside Cal positive return gap full price increases",
            "checker_sha256 66a8f56d93358668c39f357c71c47fed4ad6075c1c40c39b7602adb971b3dc6f receipt 104 checks 2048u",
            "upstream_receipts.md 7ds RETURN RECORD COMPILER RECEIPT 7dt ONE SIDED PRICE GRAPH RECEIPT 7do PAID BINARY INPUT RECEIPT frozen json exact hashes",
            "replay_record_implementation_fibre.py _check_upstream_snapshot d0-native16-record-implementation-fibre-replay-v1 ordinary optimized repeat exact_published_receipt_match",
            "D0_PROOF_ARCHITECTURE_AND_FORMALIZATION supporting same-operation recorder fibre physical X_N selection Lean CI GR_closed false",
            "фиксирует состояние после записи и сохранённые когерентности а не только вероятности указателя",
            "complete recording specification fixes new control domain without fixing field response task brief 29 October",
            "source_manifest.json d0-native16-record-implementation-fibre-intake-v1 integrated_artifacts upstream memo_blob checker_inputs frozen_receipt_inputs",
            "replay_manifest.json d0-native16-record-implementation-fibre-replay-v1 104 exact_published_receipt_match outputs_byte_identical stderr_empty_for_all_runs",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/upstream_section_7du.md",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/upstream_task_7du.md",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/check_record_implementation_fibre.py",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/expected_receipt.json",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/inputs/upstream_receipts.md",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/replay_record_implementation_fibre.py",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/replay_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/source_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/replay/ordinary_stdout.json",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
             "scope_query_indexes": [0]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/PROOF_RU.md",
             "scope_query_indexes": [11]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/upstream_section_7du.md",
             "scope_query_indexes": [1]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/upstream_task_7du.md",
             "scope_query_indexes": [12]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/check_record_implementation_fibre.py",
             "scope_query_indexes": [7]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/expected_receipt.json",
             "scope_query_indexes": [7]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/inputs/upstream_receipts.md",
             "scope_query_indexes": [8]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/replay_record_implementation_fibre.py",
             "scope_query_indexes": [9]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/source_manifest.json",
             "scope_query_indexes": [13]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/replay_manifest.json",
             "scope_query_indexes": [14]},
            {"path": "02_REGISTRY/research/sources/d0_native16_record_implementation_fibre_2026-10-29/replay/ordinary_stdout.json",
             "scope_query_indexes": [7]},
        ],
        "scope_review": (
            "§7du defines the same complete recording operation by Cal(D): D j = C j, "
            "which fixes the post-state and retained coherences on every ready input. The "
            "completion fibre D=C T is classified exactly; within it the feedback derivative "
            "vanishes but the full heat and original horizontal field source remain. For the "
            "fixed native16 profile, a Schmidt-rank witness proves three CX calls are necessary "
            "and the three-call recorder has only the full operator C. Two 35-call, same-inventory "
            "implementations agree on every prepared prefix, terminal ready-state test and pointer "
            "effect, yet differ on the unprepared operator and have a strict positive separation "
            "in the complete Book price. The 104-check exact checker and owner receipt replay "
            "byte-identically in ordinary, -O and repeat runs with empty stderr. This supplies a "
            "finite same-operation recorder-domain application, not physical selection: admission "
            "of the recorder/reserves, the full physical X_N, selected Book/task/Cost-Info, "
            "clock/boundary equations, field refinement, Lean/CI and GR closure remain open; "
            "GR_closed=false."
        ),
    },
    {
        "id": "native16-paid-golden-calibration",
        "queries": [
            "D0_PROOF_ARCHITECTURE_AND_FORMALIZATION paid Golden calibration §7dv integration 109 checks",
            "d0_native16_paid_golden_calibration_2026-10-29 PROOF_RU.md оплаченная калибровка Golden неверная запись дороже правильной полной цене",
            "upstream_section_7dv.md 825d3773423d5ac8e19a9ace4d198629301b72f5aac4e15593be66c4c1301d2d 7dv real Golden calibration echo independent controls",
            "upstream_task_7dv.md algebraic condition Dj=Cj actual test own control reference price New7dv constructs native Golden return echo",
            "check_paid_golden_calibration.py joint_map faithful_probe actual input rank16 21 59 exact corners",
            "expected_receipt.json d4d24dc76b92377a21a9b40fa19a8fb90e71c2c8c1c33df4a71077060685ed4e strict_differences whole_bad_bad_minus_good_good",
            "inputs/upstream_receipts.md 7ds RETURN RECORD COMPILER RECEIPT 7du RECORD IMPLEMENTATION FIBRE RECEIPT 7do PAID BINARY INPUT RECEIPT",
            "replay_paid_golden_calibration.py exact #334 §7dv ordinary optimized repeat exact_published_receipt_match",
            "replay_manifest.json d0-native16-paid-golden-calibration-replay-v1 109 outputs_byte_identical_across_modes stderr_empty_for_all_runs",
            "source_manifest.json d0-native16-paid-golden-calibration-intake-v1 owner_commit 9e80e0c015a8b8dc804ec55a837eda91164201fe",
            "replay/ordinary_stdout.json strict_differences cal_bad_minus_good whole_bad_bad_minus_good_good 1388118016",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/PROOF_RU.md",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/upstream_section_7dv.md",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/upstream_task_7dv.md",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/check_paid_golden_calibration.py",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/expected_receipt.json",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/inputs/upstream_receipts.md",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/replay_paid_golden_calibration.py",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/replay_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/source_manifest.json",
            "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/replay/ordinary_stdout.json",
        ],
        "required_sources": [
            {"path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
             "scope_query_indexes": [0]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/PROOF_RU.md",
             "scope_query_indexes": [1]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/upstream_section_7dv.md",
             "scope_query_indexes": [2]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/upstream_task_7dv.md",
             "scope_query_indexes": [3]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/check_paid_golden_calibration.py",
             "scope_query_indexes": [4]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/expected_receipt.json",
             "scope_query_indexes": [5]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/inputs/upstream_receipts.md",
             "scope_query_indexes": [6]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/replay_paid_golden_calibration.py",
             "scope_query_indexes": [7]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/replay_manifest.json",
             "scope_query_indexes": [8]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/source_manifest.json",
             "scope_query_indexes": [9]},
            {"path": "02_REGISTRY/research/sources/d0_native16_paid_golden_calibration_2026-10-29/replay/ordinary_stdout.json",
             "scope_query_indexes": [10]},
        ],
        "scope_review": (
            "§7dv consumes the §7du complete-map recorder condition and implements a real "
            "21-call Golden return test plus a 59-call complete native16 Book programme. The "
            "test and later use remain independent control positions; the unchanged full H+J "
            "price retains all heat modes and actual clocks. Exact interval replay shows that "
            "the faulty recorder is dearer in the standalone test but cheaper when tested and "
            "used in the complete programme; a successful test also fails to constrain an "
            "independently changed later use. Therefore unconstrained total-price minimization "
            "does not derive the faithful-recording condition. This is a scoped negative on that "
            "proposed parent substitution, not a physical no-go for a correctly constrained "
            "task. Deriving the native task/continuation law, admitting SourceI and physical X_N, "
            "retaining preparation and original GR transport/refinement, Lean/CI and GR closure "
            "remain open; GR_closed=false."
        ),
    },
    {
        "id": "canonical-archive-law-and-variation-domain",
        "queries": [
            "canonical archive law compatibility variation domain full old effect relative commutant",
            "GNS conditional expectation Phi_U old effects",
            "identity-fibre Phi_U archive tangent",
            "finite archive algebra domain original Fibonacci inclusions",
            "canonical_AF_source true_GNS_leakage_norm physical_query_law_selected",
            "checker_sha256 result_sha256 normal_optimized_repeat_byte_identical GR_closed",
        ],
        "required_refs": [
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
        ],
        "required_sources": [
            {
                "path": "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
                "scope_query_indexes": [0, 1, 2, 3, 4, 5],
            },
            {
                "path": "02_REGISTRY/research/A4D_CANONICAL_ARCHIVE_LAW_AND_VARIATION_DOMAIN_2026_10_28.md",
                "commit": "dc3d8bad99eb55250dd0db24d96ed8a6992c2a16",
                "blob": "7b835491a6fbc58d81af295d0c6d61a235395a61",
                "scope_query_indexes": [0],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_archive_naturality_domain_2026-10-28/PROOF_RU.md",
                "commit": "f7f005c75b06914998d39d85586b6f2e1f3ae9a8",
                "blob": "8cd1e3d5bd8f952be1ca157b3e8c1c2612323b8b",
                "scope_query_indexes": [1, 2],
                "scope_query_sections": {"1": ["2"], "2": ["5"]},
            },
            {
                "path": "02_REGISTRY/research/sources/d0_archive_naturality_domain_2026-10-28/check_archive_domain.py",
                "commit": "d5a32be3b7d7bab8006c5af588a0ea4e21dce6c3",
                "blob": "5664d79a7a241b1373fb45e4065e78888301b361",
                "scope_query_indexes": [3],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_archive_naturality_domain_2026-10-28/result.json",
                "commit": "edf02f60b12f288c19f10499e26e86e8015bf496",
                "blob": "df924905849e10d38e37808ce2e5d5cb6e9738e8",
                "scope_query_indexes": [4],
            },
            {
                "path": "02_REGISTRY/research/sources/d0_archive_naturality_domain_2026-10-28/RUN_RECEIPT.json",
                "commit": "0f0278787612f34c0bad6ea5cbd93a9f164df756",
                "blob": "1e571ca6a4362b6816735d6d48619f8a9ee58ff5",
                "scope_query_indexes": [5],
            },
        ],
        "scope_review": (
            "On the original canonical AF/GNS input, full old-effect preservation is equivalent "
            "to the relative-commutant condition. The first-law jet does not characterize its "
            "tangent; a second-order archive jet and explicit source-error budget are retained. "
            "The reversible SourceI control changes a coherent old effect, and even exact full "
            "archive compatibility leaves a nonzero new-query source. The domain is not shown "
            "physically selected; the 88-call heat word was consumed but not replayed, and "
            "Lean/CI were not run. No physical query law or GR closure follows; GR_closed=false."
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
    all_hits = proof.full_text_search_many(
        root, queries, max(limit, COLD_START_MIN_RESULT_WINDOW)
    )
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
            key = required["path"]
            if key in required_status:
                pin = required.get("commit") or required.get("blob") or str(len(required_status))
                key = f"{key}@{pin}"
            required_status[key] = _required_source_status(query_pairs, required)
        for required_path in case["required_refs"]:
            if any(item["path"] == required_path
                   for item in case.get("required_sources", [])):
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
        "search_limit": max(limit, COLD_START_MIN_RESULT_WINDOW),
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
