# D0 v16 Claims Register

Status: FINAL-PUBLICATION-GUARDRAIL / CLAIM-CLASS-REGISTER

This register is the publication-facing claim map for D0 v16. It separates finite internal theorems/certificates from bridge protocols, empirical negative controls, and theorem targets. The register is derived from `03_THEORY_MAP/theory_status_map.csv` and should be treated as the first stop before quoting any strong claim.

## Claim-class counts

| Claim class | Count |
|---|---:|
| AUDIT/PUBLICATION | 1 |
| CORE/SECTOR-CERTIFIED | 9 |
| EMPIRICAL-NEGATIVE | 1 |
| LAB-BRIDGE / EMPIRICAL-PASSPORT | 9 |
| NO-GO/AUDIT | 15 |
| SECTOR-CERTIFIED | 3 |
| STATUS-CHECK-REQUIRED | 106 |
| THEOREM-TARGET / FRONTIER | 11 |

## Allowed publication verbs

| Claim class | Allowed verbs | Disallowed shortcut |
|---|---|---|
| CORE/SECTOR-CERTIFIED | proves, derives, certifies, constructs when theorem/cert owner is named | external analogy proves core theorem |
| SECTOR-CERTIFIED | certifies or constructs within declared sector | universal closure outside sector |
| THEOREM-TARGET / FRONTIER | proposes, targets, conjectures, scaffolds | proves, confirms, closes |
| LAB-BRIDGE / EMPIRICAL-PASSPORT | bridges, models, motivates, tests | exact isomorphism, proof of quantum gravity |
| EMPIRICAL-NEGATIVE | rejects this proxy, falsifies this shortcut | hides negative result or converts it into discovery |
| AUDIT/PUBLICATION | documents, guards, organizes | theoremizes |

## High-sensitivity frozen statuses

| Topic | Publication status | Boundary |
|---|---|---|
| Finite retained/archive split and feedback-return operator | internal core spine | publishes only finite-readout algebra, not external empirical validation |
| Log-det pressure response | internal certified response with corrected second derivative sign | first response positive on domain; second response negative for `0 < z < 1`; relative archive ratio accelerates separately |
| Edge alpha / ramification companion constructions | finite algebraic sector constructions | no QED RG or lepton-mass empirical proof unless a separate passport is named |
| Baryon 40/56 projectors and anonymous image poles | finite representation/operator construction | no PDG sorting or physical resonance discovery claim |
| Dusty-plasma bridge | LAB-BRIDGE / TABLETOP-PASSPORT-SEED | external laboratory analogue only; phi predictions are pre-registered tests |
| LIGO/GWOSC V3--V12 | DISCOVERY-NEGATIVE-CONTROL / TRANSFER-MAP-TARGET | raw fixed phi, ramified phi, and fixed alpha proxy claims rejected as evidence |

## Full register

| Claim ID | Book | Domain | Type | Claim class | Release status | Cert/theorem owner | Boundary |
|---|---|---|---|---|---|---|---|
| D0-LEAN-CORE-001 | Lean formalization | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-LEAN-BRIDGE-001 | Lean formalization | rg | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTIONS-EXPLICIT | LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-FOUND-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-PHI-HURWITZ-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ABCD-001 | BOOK_01 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-OMEGA8-001 | BOOK_01 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-CAPACITY-V9-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-CAPACITY-V11-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-CAPACITY-V13-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-SCENE-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-NCG-INDEX-001 | BOOK_02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-PHASE-UNFOLD-002 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-QM-BORN-001 | BOOK_02 | formal_core | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTIONS-EXPLICIT | LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-QM-BORN-002 | BOOK_02 | formal_core | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTIONS-EXPLICIT | LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-CARRIER-003 | D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE | formal_core | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | CORE_BRIDGE_SPLIT | vp_v1145_operator_bridge_triple.py | Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package. |
| D0-GAUGE-MATTER-001 | BOOK_02/04 | gauge_bridge | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTIONS-EXPLICIT | vp_v1132_gauge_matter_ward_anomaly.py | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-GAUGE-MATTER-002 | BOOK_02/04 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_v1132_gauge_matter_ward_anomaly.py | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-RG-001 | D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE | rg | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTIONS-EXPLICIT | vp_v1145_operator_bridge_triple.py | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-SMOOTH-001 | D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE | smooth_geometry | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTIONS-EXPLICIT | vp_v1145_operator_bridge_triple.py | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-PHASE-TOWER-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-PHASE-TOWER-002 | BOOK_01/02 | formal_core | no-go | NO-GO/AUDIT | NO_GO_PROVED | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-ARCHIVE-TOWER-001 | BOOK_06/07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-MODE-EXPONENT-001 | BOOK_07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-HEATTRACE-001 | BOOK_07/08 | spectral_action | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_heat_trace_weyl_dimension.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-LAPLACIAN-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-RESOLVENT-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-SPECTRAL-ACTION-ADMISS-001 | BOOK_07 | spectral_action | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_spectral_action_eh_coefficient.py;vp_spectral_action_expansion_stability.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-HST-ARCHIVE-001 | BOOK_06/08 | formal_core | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_subgaussian_hst_admissibility.py;vp_archive_convex_order_domination.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-ENTROPY-001 | BOOK_06/08 | formal_core | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_entropy_softmax_coupling.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-DM-CLASSICALITY-001 | BOOK_06/08 | formal_core | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_dm_classicality_guardrail.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-GAUSSIAN-CHANNEL-001 | BOOK_06/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-GRAV-QNM-001 | BOOK_07 | empirical_passport | no-go | NO-GO/AUDIT | NO_GO_PROVED | vp_qnm_delta0_overtone_ladder.py | Boundary/no-go row; prevents promotion of this route. |
| D0-GENERATION-RAYS-001 | BOOK_04 | formal_core | no-go | NO-GO/AUDIT | NO_GO_PROVED | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-GEN-INDEX-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_pi0_branch_defect_generation.py | Lean-owned finite/formal D0 core statement. |
| D0-GEN-MASS-001 | BOOK_04 | empirical_passport | no-go | NO-GO/AUDIT | NO_GO_PROVED | vp_pi0_branch_defect_generation.py | Boundary/no-go row; prevents promotion of this route. |
| D0-ARCHIVE-PHASE-DISTANCE | BOOK_06/07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY | BOOK_07 | formal_core | no-go | NO-GO/AUDIT | NO_GO_PROVED | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-ARCHIVE-PHASE-CURVATURE | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-LAPLACIAN-RG | BOOK_07 | rg | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_laplacian_rg_flow.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-SEAM-CURVATURE-001 | BOOK_07 | formal_core | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_seam_curvature_action.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-ACTION-001 | BOOK_07 | formal_core | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_seam_curvature_action.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-FIELD-EQ-001 | BOOK_07 | formal_core | certificate | STATUS-CHECK-REQUIRED | CERT-CLOSED | vp_archive_variational_field_equation.py | Certificate-bounded row; valid only for declared finite inputs and negative controls. |
| D0-ARCHIVE-BIANCHI-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_archive_variational_field_equation.py | Lean-owned finite/formal D0 core statement. |
| D0-MATTER-STRESS-COUPLING-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-VARIATION-DUAL-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-STRESS-REP-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-WEAK-FIELD-001 | BOOK_07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_archive_weak_field_poisson.py | Lean-owned finite/formal D0 core statement. |
| D0-MATTER-SOURCE-NEUTRALITY-001 | BOOK_04/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-MATTER-REP-001 | BOOK_04 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-MATTER-ANOMALY-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-GEOM-OBSTRUCT-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-STRESS-CONSERVATION-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-ARCHIVE-SCALAR-REDUCTION-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-MATTER-LOCALIZATION-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-COSMO-HOMOGENEOUS-FIXED-POINT-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-ZERO-MEAN-UNDERDENSE-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-TRANSIENT-ACCELERATION-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-INSTABILITY-SATURATION-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_archive_friedmann_instability.py | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-ENTROPY-FLOW-FIXED-POINT-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-JACOBIAN-INSTABILITY-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-VOLUME-FLOOR-BOUND-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-CONCRETE-FLOW-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-JACOBIAN-SIGN-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-FLOOR-PROJECTION-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-TICK-GAUGE-EQUIV-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-WATER-FILLING-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-COSMO-CONFORMAL-TRACE-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-GEOM-HEAT-TRACE-EH-PROXY-001 | BOOK_08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-COSMO-CORE-SHAPE-PASSPORT-BOUNDARY-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-GEOM-HEAT-TRACE-A2-DECOMP-001 | BOOK_08 | spectral_action | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_spectral_action_eh_coefficient.py | Finite spectral-action or heat-trace statement; no continuum Einstein-Hilbert promotion by default. |
| D0-GEOM-SPECTRAL-ACTION-LADDER-001 | BOOK_08 | smooth_geometry | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_spectral_action_eh_coefficient.py | Finite/symbolic smooth-geometry proxy; continuum covariance requires declared bridge assumptions. |
| D0-GEOM-HIGHER-CURVATURE-FLOOR-BOUND-001 | BOOK_08 | spectral_action | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_spectral_action_eh_coefficient.py | Finite spectral-action or heat-trace statement; no continuum Einstein-Hilbert promotion by default. |
| D0-TRACEABILITY-STATUS-TAXONOMY-001 | BOOK_08 | empirical_passport | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Passport or empirical interface row; not a D0-core theorem without external data discipline. |
| D0-OPERATOR-GAUGE-CURVATURE-ORIGIN-001 | BOOK_08 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-OPERATOR-VECTOR-LAPLACIAN-ORIGIN-001 | BOOK_08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-OPERATOR-EDGE-STIFFNESS-ORIGIN-001 | BOOK_08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-NO-GO-BARE-ARCHIVE-NONABELIAN-001 | BOOK_08 | formal_core | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-NO-GO-EDGE-STIFFNESS-SCALAR-LEAKAGE-001 | BOOK_08 | formal_core | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-NO-GO-FLAT-TENSOR-NONABELIAN-001 | BOOK_08 | gauge_bridge | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-GAUGE-NONABELIAN-DISCRETE-CURVATURE-001 | BOOK_08 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-GAUGE-BIANCHI-RESIDUAL-BOUNDARY-001 | BOOK_08 | gauge_bridge | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-GAUGE-YANG-MILLS-KILLING-POSITIVITY-001 | BOOK_08 | gauge_bridge | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | BRIDGE-ASSUMPTION | LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS | Conditional bridge row; not a D0-core closure without listed assumptions. |
| D0-FINAL-BRIDGE-INDEX-001 | BOOK_08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-HURWITZ-LOCAL-BOUNDARY-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-EXTERNAL-BACKGROUND-HURWITZ-GLOBAL-CLASSIFICATION-001 | BOOK_04 | external_background | deprecated | STATUS-CHECK-REQUIRED | EXTERNAL-BACKGROUND | DEPRECATED | Deprecated or historical row; not a live promotion path. |
| D0-GAUGE-MATRIX-REP-TRANSFORM-001 | BOOK_05/06 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-NO-GO-ABSTRACT-LIERING-FINITE-TRANSFORM-001 | BOOK_05/06 | gauge_bridge | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-GAUGE-BIANCHI-GRADED-DEPRECATED-001 | BOOK_05/06 | gauge_bridge | deprecated | STATUS-CHECK-REQUIRED | DEPRECATED | DEPRECATED | Deprecated or historical row; not a live promotion path. |
| D0-BRIDGE-SI-CALIBRATION-BOUNDARY-001 | BOOK_08 | si_calibration | bridge | STATUS-CHECK-REQUIRED | BRIDGE-CALIBRATION | vp_si_calibration_boundary.py | Bridge-calibration row; SI or dimensional interpretation requires an explicit external calibration object. |
| D0-HURWITZ-INTERNAL-DIMENSION-SELECTOR-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Lean-owned finite/formal D0 core statement. |
| D0-GAUGE-WILSON-LINK-COVARIANCE-001 | BOOK_05/06 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-NO-GO-NAIVE-LOCAL-GAUGE-COVARIANCE-001 | BOOK_05/06 | gauge_bridge | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-GRADED-BIANCHI-EXACT-001 | BOOK_05/06 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | LEAN_PROVED | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-NO-GO-UNGRADED-BIANCHI-RESIDUAL-001 | BOOK_05/06 | gauge_bridge | no-go | NO-GO/AUDIT | NO-GO | LEAN_PROVED | Boundary/no-go row; prevents promotion of this route. |
| D0-BRIDGE-SI-CALIBRATION-CLOSURE-001 | BOOK_08 | si_calibration | bridge | STATUS-CHECK-REQUIRED | BRIDGE-CALIBRATION | LEAN_PROVED | Bridge-calibration row; SI or dimensional interpretation requires an explicit external calibration object. |
| D0-INTERPRETATION-SPINE-001 | BOOK_00/08 | interpretation_spine | bridge | STATUS-CHECK-REQUIRED | CORE_BRIDGE_SPLIT | LEAN_PROVED | Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package. |
| D0-TORUS-CORE13-GEOMETRY-001 | BOOK_02/03 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_torus_core13_geometry_origin.py | Lean-owned finite/formal D0 core statement. |
| D0-TORUS-GENERATION-SELECTOR-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_generation_selector_origin.py | Lean-owned finite/formal D0 core statement. |
| D0-TORUS-GENERATION-OVERLAP-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_generation_selector_origin.py | Lean-owned finite/formal D0 core statement. |
| D0-BORN-QUADRATIC-ORIGIN-001 | BOOK_01/02 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_born_quadratic_origin.py | Lean-owned finite/formal D0 core statement. |
| D0-CKM-NONTRIVIAL-FLAVOUR-ALGEBRA-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_generation_overlap_response_origin.py | Lean-owned finite/formal D0 core statement. |
| D0-QUASI009-CKM-PHASON-HOLONOMY-001 | BOOK_04/08 | empirical_passport | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_ckm_phason_holonomy_k0.py | Passport or empirical interface row; not a D0-core theorem without external data discipline. |
| D0-MESON-POSITIVE-DEFECT-TRANSFER-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_meson_positive_defect_transfer.py | Lean-owned finite/formal D0 core statement. |
| D0-GRAVITY-ENTROPIC-ARCHIVE-001 | BOOK_07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_entropic_archive_gravity.py | Lean-owned finite/formal D0 core statement. |
| D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001 | BOOK_07 | smooth_geometry | bridge | STATUS-CHECK-REQUIRED | CORE_BRIDGE_SPLIT | vp_macro_einstein_interface.py | Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package. |
| D0-TORAL-AUTOMORPHISM-GALOIS-BALANCE-001 | BOOK_03/06/07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_toral_automorphism_galois_balance.py | Lean-owned finite/formal D0 core statement. |
| D0-TRACE-HEAT-CAPACITY-GRAVITY-001 | BOOK_01/03/06/07/08 | formal_core | bridge | STATUS-CHECK-REQUIRED | CORE_BRIDGE_SPLIT | vp_trace_heat_capacity_gravity.py | Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package. |
| D0-MASTER-EVOLUTION-001 | BOOK_00/01/03/06/07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_master_evolution_theorem.py | Lean-owned finite/formal D0 core statement. |
| D0-INFORMATION-QUASICRYSTAL-PHASE-UNFOLDING-001 | BOOK_00/01/06/07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_information_quasicrystal_phase_unfolding.py | Lean-owned finite/formal D0 core statement. |
| D0-CONDENSED-PHI-VACUUM-CUT-PROJECT-001 | BOOK_00/01/02/06/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_condensed_phi_vacuum_cut_project.py | Lean-owned finite/formal D0 core statement. |
| D0-QUASICRYSTAL-PHENOMENOLOGY-OPERATOR-ORIGIN-001 | BOOK_00/01/02/04/06/07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_quasicrystal_phenomenology_operator_origin.py | Lean-owned finite/formal D0 core statement. |
| D0-QUASI008-PHASON-FLIP-ENTROPY-SDE-001 | BOOK_07/08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_phason_flip_entropy_sde.py | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-QUASI006-GALOIS-LORENTZ-SIGNATURE-001 | BOOK_06/07/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_galois_lorentz_signature.py | Lean-owned finite/formal D0 core statement. |
| D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001 | BOOK_04 | gauge_bridge | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_higgs_scalar_projector_constructive.py | Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear. |
| D0-QUASI002-PHASON-STRAIN-GENERATIONS-BARYON-001 | BOOK_02/04/05/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_quasi002_phason_strain_generations_baryon.py | Lean-owned finite/formal D0 core statement. |
| D0-QUASI007-MESON-PHASON-DOMAIN-WALLS-001 | BOOK_04/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_phason_domain_wall_mesons.py | Lean-owned finite/formal D0 core statement. |
| D0-ICECUBE-001 | BOOK_04/05/08 | empirical_passport | core | STATUS-CHECK-REQUIRED | EMPIRICAL-PASSPORT | vp_neutrino_phason_decoherence_passport.py | Passport or empirical interface row; not a D0-core theorem without external data discipline. |
| D0-NO-GO-STRESS-SUITE-001 | BOOK_02/04/05/06/07 | formal_core | no-go | NO-GO/AUDIT | NO_GO_PROVED | vp_no_go_stress_test_suite.py | Boundary/no-go row; prevents promotion of this route. |
| D0-HULL-001 | BOOK_00/01 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_d0_tiling_hull.py | Lean-owned finite/formal D0 core statement. |
| D0-KTHEORY-001 | BOOK_00/01/02/04/05/06 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_gap_labeling_d0_tiling_hull.py | Lean-owned finite/formal D0 core statement. |
| D0-SOLENOID-001 | BOOK_01/07 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_noncommutative_solenoid_gravity.py | Lean-owned finite/formal D0 core statement. |
| D0-SOLENOID-GRAVITY-001 | BOOK_07 | spectral_action | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_noncommutative_solenoid_gravity.py | Finite spectral-action or heat-trace statement; no continuum Einstein-Hilbert promotion by default. |
| D0-MESON-K0-001 | BOOK_04/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_phason_domain_wall_mesons.py | Lean-owned finite/formal D0 core statement. |
| D0-CKM-K0-001 | BOOK_04/08 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_ckm_phason_holonomy_k0.py | Lean-owned finite/formal D0 core statement. |
| D0-SDE-K0-001 | BOOK_08 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_phason_flip_entropy_sde.py | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-SRC-001 | BOOK_04 | formal_core | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_nuclear_shell_contact_src.py | Lean-owned finite/formal D0 core statement. |
| D0-SRC-NOGO-001 | BOOK_04/05 | formal_core | no-go | NO-GO/AUDIT | NO_GO_PROVED | vp_nuclear_shell_contact_src.py | Boundary/no-go row; prevents promotion of this route. |
| D0-CVFT-001A | BOOK_00/01/02/03 | cosmology | core | STATUS-CHECK-REQUIRED | CORE-FORMALIZED | vp_closed_vacuum_feedback_full_wave.py | Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data. |
| D0-CVFT-001B | BOOK_04/06/07/08 | frontier | frontier | THEOREM-TARGET / FRONTIER | PROOF-TARGET | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-NOGO-001 | BOOK_05/08 | cosmology | no-go | NO-GO/AUDIT | NO_GO_PROVED | vp_closed_vacuum_feedback_full_wave.py | Boundary/no-go row; prevents promotion of this route. |
| D0-CVFT-F1 | BOOK_02/04/08 | frontier | frontier | THEOREM-TARGET / FRONTIER | PROOF-OBLIGATION-EXPOSED | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F2 | BOOK_07/08 | frontier | frontier | THEOREM-TARGET / FRONTIER | THEOREM-TARGET-SHARPENED | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F3 | BOOK_04 | frontier | frontier | THEOREM-TARGET / FRONTIER | OPERATOR-SCAFFOLD-CERTIFIED | vp_cvft_baryon_s3_scaffold.py | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F3B | BOOK_04 | frontier | frontier | THEOREM-TARGET / FRONTIER | SPIN-FLAVOUR-TRANSFER-CERTIFIED | vp_cvft_baryon_spin_flavour_40_56.py | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F4 | BOOK_02/05 | frontier | frontier | THEOREM-TARGET / FRONTIER | CERT-CANDIDATE | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F5 | BOOK_04/08 | frontier | frontier | THEOREM-TARGET / FRONTIER | EMPIRICAL-PASSPORT-CANDIDATE | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F6 | BOOK_04/07 | frontier | frontier | THEOREM-TARGET / FRONTIER | LOWER-BOUND-TARGET | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F7 | BOOK_07 | frontier | frontier | THEOREM-TARGET / FRONTIER | CERT-CANDIDATE | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-F8 | BOOK_08 | frontier | frontier | THEOREM-TARGET / FRONTIER | CERT-CANDIDATE | OPEN | Frontier/proof-target row; not a core closure, certificate pass or empirical passport. |
| D0-CVFT-BOOTSTRAP-001 | BOOK_02/03/08 | formal_core | core | CORE/SECTOR-CERTIFIED | MASTER-BOOTSTRAP-CORE | 05_CERTS/vp_master_bootstrap_and_volume_derivative.py | Finite bootstrap row with rank-volume derivative and no empirical fit. |
| D0-CVFT-GAUGE-BOUNDARY-001 | BOOK_04 | gauge_bridge | sector | SECTOR-CERTIFIED | GAUGE-BOUNDARY-LAW | 05_CERTS/vp_gauge_boundary_commutator_obstruction.py | Internal gauge-boundary leakage law; external Yang-Mills claims remain scoped. |
| D0-CVFT-HORIZON-EMIT-001 | BOOK_07 | gravity_bridge | sector | SECTOR-CERTIFIED | HORIZON-EMISSION-LAW | 05_CERTS/vp_horizon_emission_conjugate_feedback.py | Internal horizon emission law; greybody spectra remain passport scoped. |
| D0-CVFT-EDGE-ALPHA-001 | BOOK_04 | gauge_bridge | frontier | THEOREM-TARGET / FRONTIER | EDGE-TRACE-COEFFICIENT-TARGET | 05_CERTS/vp_edge_sector_alpha_trace_target.py | Edge trace coefficient target; QED RG comparison remains passport scoped. |
| D0-EDGE-ALPHA-001 | BOOK_04 | matter | core | CORE/SECTOR-CERTIFIED | EDGE-ALPHA-TRACE-CERT-CLOSED | vp_edge_alpha_trace_constructive.py | Finite 359-edge trace construction; no QED RG fit. |
| D0-EDGE-RAMIFICATION-001 | BOOK_04 | matter | core | CORE/SECTOR-CERTIFIED | RAMIFICATION-COMPANION-COVER-CERT-CLOSED | vp_ramification_edge_ueff_companion.py | Finite companion cover; physical-edge Ueff embedding scoped. |
| D0-BARYON-POLES-001 | BOOK_04 | matter | core | CORE/SECTOR-CERTIFIED | BARYON-ANONYMOUS-POLE-CERT-CLOSED | vp_baryon_40_56_anonymous_poles.py | Anonymous poles only; PDG passport excluded. |
| D0-HORIZON-JET-001 | BOOK_07 | gravity | sector | SECTOR-CERTIFIED | HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD | vp_horizon_jet_axis_observable.py | Finite observable; no empirical jet fit. |
| D0-IM-PRED-001 | BOOK_06/08 | IM | core | CORE/SECTOR-CERTIFIED | FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED | vp_fractal_continuum_predictions.py | Absolute archive deceleration and relative ratio acceleration split. |
| D0-IM-COSMO-001 | BOOK_08 | cosmology | core | CORE/SECTOR-CERTIFIED | RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED | vp_relative_archive_acceleration_cosmology_bridge.py | Internal relative acceleration; no survey fit. |
| D0-IM-COSMO-002 | BOOK_08 | cosmology | core | CORE/SECTOR-CERTIFIED | RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED | vp_archive_pressure_coupling_from_relative_acceleration.py | Weak finite pressure bridge; no survey fit. |
| D0-IM-COSMO-003 | BOOK_08 | cosmology | core | CORE/SECTOR-CERTIFIED | LOGDET-PRESSURE-COUPLING-CERT-CLOSED | vp_strong_logdet_pressure_coupling.py | Positive logdet first response on resolvent domain. |
| D0-IM-COSMO-004 | BOOK_08 | cosmology | core | CORE/SECTOR-CERTIFIED | LOGDET-SECOND-RESPONSE-STABILITY-CERT-CLOSED | vp_logdet_second_response_and_stability.py | Positive first derivative negative second derivative bounded saturation. |
| D0-PUB-001 | PUBLICATION | publication | audit | AUDIT/PUBLICATION | PUBLICATION-MONOGRAPH-STRUCTURE | PYTHON_CERTIFIED | Audit-only monograph structure. |
| D0-DUSTY-TABLETOP-BRIDGE-001 | BOOK_06/07/08 | lab_analogue | bridge | LAB-BRIDGE / EMPIRICAL-PASSPORT | LAB-BRIDGE / TABLETOP-PASSPORT-SEED | vp_dusty_plasma_d0_mapping.py | external_bridge_guardrail |
| D0-LIGO-DISCOVERY-NEGATIVE-001 | BOOK_07/08 | gwosc_proxy | no-go | EMPIRICAL-NEGATIVE | DISCOVERY-NEGATIVE-CONTROL / TRANSFER-MAP-TARGET | vp_ligo_discovery_negative_control.py | negative_control_guardrail |

## Register rule

A publication sentence may use a strong verb only if its row class permits it and the sentence stays inside the boundary column. Any external-laboratory, LIGO/GWOSC, PDG, survey, or numerical scan language must name its bridge/passport/no-go status.
