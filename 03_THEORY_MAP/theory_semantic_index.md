# D0 theory semantic index

Generated from `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` and `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv`.
Purpose: make bridge boundaries, risky physical domains, Lean anchors, certificates, and legacy rows visible to both humans and Graphify.

## Status counts

- `BRIDGE-ASSUMPTIONS-EXPLICIT`: 9
- `BRIDGE-CALIBRATION`: 2
- `CERT-CLOSED`: 72
- `CORE-FORMALIZED`: 92
- `CORE_BRIDGE_SPLIT`: 4
- `DEPRECATED`: 1
- `EMPIRICAL-PASSPORT`: 11
- `EXTERNAL-BACKGROUND`: 1
- `NO-GO`: 8
- `NO_GO_PROVED`: 8
- `PROOF-TARGET`: 12

## Type counts

- `bridge`: 13
- `certificate`: 84
- `core`: 93
- `deprecated`: 2
- `frontier`: 12
- `no-go`: 16

## Domain counts

- `cosmology`: 22
- `empirical_passport`: 18
- `external_background`: 1
- `formal_core`: 131
- `frontier`: 12
- `gauge_bridge`: 17
- `interpretation_spine`: 1
- `rg`: 3
- `si_calibration`: 2
- `smooth_geometry`: 7
- `spectral_action`: 6

## Domain: cosmology

### D0-COSMO-003

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `cosmology`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_boundary_dark_survey_driver_kernel.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] parameter-free internal dark object as additive optical-depth kernel; catalogue is external readout.

### D0-IM-COSMO-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.IM.RelativeArchiveAcceleration`
- theorem: `relative_archive_acceleration_positive_second_difference`
- cert: `vp_relative_archive_acceleration_cosmology_bridge.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Internal relative acceleration; no survey fit. [was:RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED]

### D0-IM-COSMO-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.IM.ArchivePressureCoupling`
- theorem: `relative_pressure_bridge_law`
- cert: `vp_archive_pressure_coupling_from_relative_acceleration.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Weak bridge; strong log-det is primary. [was:RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED]

### D0-IM-COSMO-003

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.IM.StrongLogdetPressure`
- theorem: `strong_logdet_pressure_coupling`
- cert: `vp_strong_logdet_pressure_coupling.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Correct r(V) derivative. [was:LOGDET-PRESSURE-COUPLING-CERT-CLOSED]

### D0-IM-COSMO-004

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.IM.LogdetSecondResponse`
- theorem: `logdet_second_response_stability_sign_corrected`
- cert: `vp_logdet_second_response_and_stability.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: L bounded; Lp->0; Lpp<0 safe domain. [was:LOGDET-SECOND-RESPONSE-STABILITY-CERT-CLOSED]

### D0-COSMO-002

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `cosmology`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_final_survey_likelihood_and_baryon_form_factor_closure_20260522.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] external-survey A_s + baryon form-factor comparison.

### D0-COSMO-CONCRETE-FLOW-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.ConcreteEntropyArchiveFlow`
- theorem: `softmax_flow_mass_preserving;homogeneous_state_maps_to_itself;positivity_if_initial_positive;centered_source_zero_mean`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Concrete entropy-coupled softmax flow properties.

### D0-COSMO-CONFORMAL-TRACE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Geometry.ConformalLaplacianTrace`
- theorem: `trace_weighted_laplacian;regular_trace_volume_proxy;archiveVolume_heat_trace_proxy`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Weighted trace volume proxy proportional to archiveVolume on regular graphs.

### D0-COSMO-CORE-SHAPE-PASSPORT-BOUNDARY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.CoreShapePassportBoundary`
- theorem: `core_shape_independent_of_empirical_parameters;empirical_passport_not_core_closed`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: D0 core shape independent of empirical params and external data not core closed.

### D0-COSMO-ENTROPY-FLOW-FIXED-POINT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.EntropyArchiveFlow`
- theorem: `homogeneous_fixed_point`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Mass-preserving homogeneous entropy-coupled flow fixed point.

### D0-COSMO-FLOOR-PROJECTION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.FloorMassProjection`
- theorem: `projection_preserves_mass;projection_preserves_floor;projection_exists_of_feasible`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Feasible projection preserves mass and floor.

### D0-COSMO-HOMOGENEOUS-FIXED-POINT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.ArchiveHomogeneousState`
- theorem: `homogeneous_total_eq_value;homogeneous_mass_conserving_fixed_point`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Homogeneous state mass conservation fixed point.

### D0-COSMO-INSTABILITY-SATURATION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.InstabilitySaturation`
- theorem: `positive_lower_bound_blocks_eternal_linear_underdensity`
- cert: `vp_archive_friedmann_instability.py`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Lower bound blocks eternal linear underdensity growth.

### D0-COSMO-JACOBIAN-INSTABILITY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.LinearizedEntropyFlow`
- theorem: `jacobian_eigenvalue_formula;jacobian_eigenvalue_unstable_if_mu_positive`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Linearized flow eigenvalue formula and instability.

### D0-COSMO-JACOBIAN-SIGN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.EntropyJacobianSign`
- theorem: `jacobian_eigenvalue_formula_convention;jacobian_eigenvalue_unstable_convention`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Instability audit locks sign and eigenvalue formula.

### D0-COSMO-TICK-GAUGE-EQUIV-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Geometry.ArchiveTickGaugeFixing`
- theorem: `eta_absorbs_into_response`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Tick gauge equivalence holds by parameter absorption.

### D0-COSMO-TRANSIENT-ACCELERATION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.TransientAcceleration`
- theorem: `inverse_density_convex_three_point;underdense_geometric_mode_generates_positive_acceleration`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Geometric underdensity pattern yields transient acceleration in 1/rho.

### D0-COSMO-VOLUME-FLOOR-BOUND-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.ArchiveVolumeBounds`
- theorem: `density_floor_bounds_inverse;density_floor_bounds_archiveVolume;bounded_volume_no_eternal_uniform_acceleration`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Density floor bounds archive volume and prevents eternal acceleration.

### D0-COSMO-WATER-FILLING-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Probability.ArchiveFloorWaterFilling`
- theorem: `waterFill_preserves_floor;waterFill_mass_if_root;feasibility`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Water-filling preserves floor and is feasible when mass is large enough.

### D0-COSMO-ZERO-MEAN-UNDERDENSE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_08`
- module: `D0.Cosmology.ZeroMeanModes`
- theorem: `zero_mean_nonzero_has_negative_component;zero_mean_nonzero_has_positive_component;zero_mean_mode_has_underdense_region`
- cert: `none`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Zero-mean modes must have negative (underdense) and positive components.

### D0-CVFT-001A

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `cosmology`
- book: `BOOK_00/01/02/03`
- module: `D0.Dynamics.InternalFeedbackResolvent;D0.Cosmology.FeedbackPartitionFunction`
- theorem: `Dynamics.internal_feedback_forced_by_split;Dynamics.internal_feedback_resolvent_series;Cosmology.feedback_determinant_return_cycles;Cosmology.feedback_variation_universal_source;Cosmology.feedback_pressure_trace_log`
- cert: `vp_closed_vacuum_feedback_full_wave.py`
- assumptions: `none`
- scope: Formal finite cosmology shape statement; not an observational cosmology fit without certificate/passport data.
- notes: Closed finite feedback operator core F_N=P_N U_N^dagger Q_N U_N P_N with resolvent determinant trace variation and feedback pressure law.

### D0-CVFT-NOGO-001

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `cosmology`
- book: `BOOK_05/08`
- module: `D0.Dynamics.InternalFeedbackResolvent;D0.Cosmology.FiniteFeedbackEquationOfState;D0.Matter.TerminalFeedbackModes;D0.Cosmology.SDEFeedbackReduction`
- theorem: `Dynamics.external_mirror_model_forbidden;Cosmology.ideal_gas_core_postulate_forbidden;Matter.matter_as_arbitrary_eigenvalue_forbidden;Cosmology.desi_root_refit_repair_forbidden;Cosmology.desi_window_refit_repair_forbidden;Cosmology.arbitrary_kernel_repair_not_theorem_grade`
- cert: `vp_closed_vacuum_feedback_full_wave.py`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: External mirror vacuum photon-acceleration interpretation ideal-gas postulate arbitrary-eigenvalue matter and DESI/SPARC root window or arbitrary-kernel repairs are forbidden.


## Domain: empirical_passport

### D0-CVFT-F3

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `empirical_passport`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_cvft_baryon_s3_scaffold.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Finite carrier/symmetrizer scaffold is certified for 27D triple carrier S3 representation 10D symmetric carrier antisymmetric rank-one sector and U_eff^B admissibility; spin/flavour transfer PDG and masses remain open. [was:OPERATOR-SCAFFOLD-CERTIFIED]

### D0-CVFT-F3B

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `empirical_passport`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_cvft_baryon_spin_flavour_40_56.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Finite internal spin/flavour transfer certifies rank-40 fully symmetric separable sector rank-56 diagonal exchange-symmetric carrier and rank40 subset rank56; PDG names masses widths and GeV conversion remain excluded. [was:SPIN-FLAVOUR-TRANSFER-CERTIFIED]

### D0-QUASI008-PHASON-FLIP-ENTROPY-SDE-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `empirical_passport`
- book: `BOOK_07/08`
- module: ``
- theorem: `none`
- cert: `vp_phason_flip_entropy_sde.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Finite formal S_DE owner: archive pressure is phason-flip entropy osmosis and the finite transfer characteristic is 160 lambda^2 - 480 lambda + 359; external BAO/DESI survey comparison is a passport/certificate and not core. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-QUASI009-CKM-PHASON-HOLONOMY-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `empirical_passport`
- book: `BOOK_04/08`
- module: ``
- theorem: `none`
- cert: `vp_ckm_phason_holonomy_k0.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Finite formal origin: non-permutation phason holonomy on the Torus Core-13 shell loop with rational unitary transport and chiral orientation twist; external CKM comparison passport/certificate is not core and no PDG entries are used. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-VACUUM-CUBIC-WINDOW-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `empirical_passport`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_vacuum_cubic_window.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Iter3 §4] HONEST FORK of two catalog-free ownerships of the dark-energy/S_DE archive window. Cert vp_vacuum_cubic_window.py computes the window-center discriminator that the GOLDEN dossier (0940) recorded as never computed: QUADRATIC branch 160l^2-480l+359 (160=2*Omega8*gamma=2*8*10, det=359/160, eigs 3/2-+sqrt10/40) -> ratio (60-sqrt10)/(60+sqrt10)=0.900; CUBIC branch l^3-359l-2574 (e1=0,e2=-359=-|E|,e3=2574=2*1287=2*|triangles|, = the adjacency characteristic poly owned by D0-MIXING-HIERARCHY-INVERSION-001) -> ratio of the two negative roots |9.758|/|12.079|=0.808. Discriminator: cubic 0.808 vs quadratic 0.900 (separable). HONEST: this is a FORK, NOT a decision — DESI DR3 is the empirical decider and is NOT run here; promoting either branch to the sole core form needs that external survey comparison (BRIDGE), kept out of core by the firewall.

### D0-CRITICAL-COLLAPSE-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_critical_collapse_dss_echo_lattice.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] pins external arXiv:2601.14358 DSS solutions via hash manifest.

### D0-DUSTY-PLASMA-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_dusty_plasma_d0_mapping.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] self-declared TABLETOP-PASSPORT-SEED; forbids core promotion.

### D0-GRAVASTAR-GW-FALSIFIER-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_09`
- module: ``
- theorem: `none`
- cert: `vp_gravastar_gw_falsifier.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Iter4 Phase1 T1.3] Second GW falsifier beyond I_f=log phi. At C=3/8 the surface R=8M/3 is INSIDE the photon sphere 3M (and outside horizon 2M) -> light-ring cavity -> GW echoes (a BH has no surface/cavity, no echoes). Cert vp_gravastar_gw_falsifier.py: 2M<R_surf<3M, echo delay tau=2[r*(3M)-r*(8M/3)]~2.29M (short-delay), dimensionless in M; BH control has no cavity. PASSPORT TARGET, never core; NOT claimed from current LIGO (Book 09 discipline: predicts-as-target). Echo mechanism standard (Cardoso-Pani).

### D0-PASSPORT-CORE13-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_core13_shell_geometry_passport.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] pinned PDG mass-width diagnostic; no core promotion.

### D0-PASSPORT-DESI-BAO-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_desi_bao_sde_failure_diagnostics.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] honest negative survey diagnostic (FAIL on real data, no refit).

### D0-PASSPORT-ICECUBE-HESE-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_04/08`
- module: ``
- theorem: `none`
- cert: `vp_icecube_hese_baseline_comparison.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] external neutrino-survey baseline comparison.

### D0-PASSPORT-LIGO-CATALOG-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_ligo_merger_mass_defect_current_catalog.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] external GWOSC catalog passport.

### D0-PASSPORT-PDG-STRICT-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_04/05`
- module: ``
- theorem: `none`
- cert: `vp_pdg_strict_passport.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] PDG comparison engine with pinning/holdout/multiple-testing; no operator tuning.

### D0-PASSPORT-SPARC-001

- type: `certificate`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_07/08`
- module: ``
- theorem: `none`
- cert: `vp_sparc_hull_boundary_response_kernel.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] SPARC rotation-curve external-data passport.

### D0-TRACEABILITY-STATUS-TAXONOMY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `empirical_passport`
- book: `BOOK_08`
- module: `D0.Traceability.StatusTaxonomy`
- theorem: `Traceability.external_likelihood_cannot_promote_to_core_closed`
- cert: `none`
- assumptions: `none`
- scope: Passport or empirical interface row; not a D0-core theorem without external data discipline.
- notes: Traceability status taxonomy with promotion guardrails.

### D0-ICECUBE-001

- type: `core`
- release_status: `EMPIRICAL-PASSPORT`
- domain: `empirical_passport`
- book: `BOOK_04/05/08`
- module: `D0.Matter.NeutrinoPhasonWaves;D0.Passport.IceCubePhasonDecoherence`
- theorem: `Matter.neutrino_neutral_leakage_is_bulk_phason_wave;Matter.neutral_phason_wave_has_no_em_coupling;Matter.delta0_over_four_is_phason_birefringence_seed;Matter.phason_wave_decoherence_kernel_positive;Passport.icecube_decoherence_passport_requires_external_manifest;Passport.empty_icecube_manifest_cannot_run`
- cert: `vp_neutrino_phason_decoherence_passport.py`
- assumptions: `none`
- scope: Passport or empirical interface row; not a D0-core theorem without external data discipline.
- notes: Neutrino is a neutral bulk phason leakage mode internally; IceCube decoherence comparison is skipped until a complete external event energy direction response and hash manifest is supplied.

### D0-GEN-MASS-001

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `empirical_passport`
- book: `BOOK_04`
- module: `D0.Spectrum.BranchDefectProjectiveControls`
- theorem: `branch_defect_projective_proof_closed`
- cert: `vp_pi0_branch_defect_generation.py`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Core index is proved; physical masses/Yukawa hierarchy/PDG clustering require additional physical input and are not core theorems.

### D0-GRAV-QNM-001

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `empirical_passport`
- book: `BOOK_07`
- module: `D0.Gravity.BoundaryRelaxationSpectrum`
- theorem: `qnm_passport_requires_preregistered_inputs`
- cert: `vp_qnm_delta0_overtone_ladder.py`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: QNM ladder passport is blocked without preregistered model and extracted modes table.


## Domain: external_background

### D0-EXTERNAL-BACKGROUND-HURWITZ-GLOBAL-CLASSIFICATION-001

- type: `deprecated`
- release_status: `EXTERNAL-BACKGROUND`
- domain: `external_background`
- book: `BOOK_04`
- module: `D0.Algebra.D0InternalDimensionSelector`
- theorem: `Algebra.global_hurwitz_classification_not_core_dependency`
- cert: `none`
- assumptions: `none`
- scope: Deprecated or historical row; not a live promotion path.
- notes: Global normed-division exhaustion is no longer an active D0 core dependency; D0 core uses the finite internal selector.


## Domain: formal_core

### D0-QM-BORN-001

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `formal_core`
- book: `BOOK_02`
- module: `D0.Born`
- theorem: `finite_born_sum_one`
- cert: `none`
- assumptions: `ASSUMP-HST-EXTERNAL`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Finite skeleton under explicit finite response assumptions; no full Gleason claim.

### D0-QM-BORN-002

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `formal_core`
- book: `BOOK_02`
- module: `D0.Born`
- theorem: `finite_born_nonnegative`
- cert: `none`
- assumptions: `ASSUMP-HST-EXTERNAL`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Finite skeleton under explicit finite response assumptions.

### D0-CARRIER-003

- type: `bridge`
- release_status: `CORE_BRIDGE_SPLIT`
- domain: `formal_core`
- book: `D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE`
- module: `D0.Algebra.Clifford`
- theorem: `clifford_relation`
- cert: `vp_v1145_operator_bridge_triple.py`
- assumptions: `ASSUMP-LORENTZ-MACRO`
- scope: Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package.
- notes: Finite Clifford relation is core; Lorentz macro integration is bridge.

### D0-TRACE-HEAT-CAPACITY-GRAVITY-001

- type: `bridge`
- release_status: `CORE_BRIDGE_SPLIT`
- domain: `formal_core`
- book: `BOOK_01/03/06/07/08`
- module: `D0.Core.FixedDetectorTimeLadder;D0.Dynamics.TraceHeatCapacityGravity`
- theorem: `Core.detector_fixed_under_time_ladder;Core.readout_depends_on_time_power;Core.active_archive_trace_readout_integer;Dynamics.heat_moment_T2_eq_even_lucas_trace;Dynamics.heat_moment_eq_even_lucas;Dynamics.lefschetz_spectrum_unfolds_scene;Dynamics.boundary_capacity_is_quarter_cut_weight;Dynamics.saturated_region_forces_boundary_encoding;Dynamics.black_hole_capacity_saturation_rule;Dynamics.heat_trace_entropy_gradient_admits_gravity_interface`
- cert: `vp_trace_heat_capacity_gravity.py`
- assumptions: `none`
- scope: Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package.
- notes: Fixed finite boundary trace-heat capacity block proves T^2 heat moments as even Lucas traces and saturation as boundary encoding while macro gravity stays bridge-scoped through the finite witness.

### D0-COMPACTNESS-LIMIT-001

- type: `certificate`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_gravastar_compactness.py`
- assumptions: `ASSUMP-RANK3-CAUSAL-CONE`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Iter4 Phase1 T1.2] LEM with one NAMED GAP. Cert vp_gravastar_compactness.py: from OS junction 2C=sin^2 chi2, photon threshold chi2=theta*, cycle cos theta*=4C-1 -> -2C(8C-3)=0 -> C_max=3/8 (exact rational, no fit); placement 1/3<3/8<4/9<1/2 (horizonless, falsifiable); structural reading 3/8=rank/|Omega8|=3/8. NAMED GAP (ASSUMP-RANK3-CAUSAL-CONE): rank-3=causal-cone postulated, not M1-forced => LEM, NOT THE. T1.4 attempt to close via Connes distance (BOOK_03 03.1.1): attempted, OPEN. (Supporting algebra module D0.Gravity.CompactnessLimit proves the 3/8 master-equation roots over Q and compiles, but the CLAIM stays bridge-level: the named gap means it is not fully Lean-proved.)

### D0-GRAVASTAR-FORMATION-BRIDGE-001

- type: `certificate`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_gravastar_os_arrest.py`
- assumptions: `ASSUMP-GRAVASTAR-GR-EXTERNAL`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Iter4 Phase1 T1.1] External anchor (PRD 113 L121502 / arXiv:2509.15302): a de Sitter core arrests OS collapse before a horizon forms. Fills a real D0 hole (had static horizon=seam + horizon BIRTH, but no collapse-ARREST). Cert vp_gravastar_os_arrest.py: 3-region dS/shell/Schwarzschild, Israel junction f_in(R)>f_out(R) (sigma>0), horizonless both sides 2M<R<L, seam closes at C=3/8 (f_out=1/4>0); negative control: no dS core -> horizon at C=1/2. BRIDGE: GR junction physics owned externally, D0 owns the finite seam reading. NOT core.

### D0-ALPHA-ZETA-RESIDUE-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_03`
- module: `D0.Spectral.ZetaResidueAlpha`
- theorem: `zeta_residue_alpha_finite`
- cert: `vp_zeta_residue_alpha.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: zeta_D(s)=Tr|D|^-s defined on K(9,11,13) (was ABSENT in v14, golden-0169). Finite spectral moments closed by cert: zeta_E(-1)=359*phi^-2-phi^-5=alpha_top^-1=137.03563, zeta_E(0)=359=|E|, zeta_adj(0)=3=rank; one zeta carries alpha+capacity. phi^-5 seam=xi5 (D0-XI5, proved). HONEST: finite scene has no dimension pole so alpha is the s=-1 MOMENT not a residue; full residue-at-pole (GOLDEN THE 15.4.2) needs profinite limit -> theorem-target. alpha is structural form (~3.7e-4 residual vs 1.5e-10 exp), NOT a precision prediction; Delta_alpha (top-vs-alg ~4e-4) is DISTINCT from phi^-5, analytic 2nd-order owner remains theorem-target.

### D0-ARCHIVE-ACTION-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveActionFunctional`
- theorem: `archiveCurvatureAction_nonnegative;archiveCurvatureAction_zero_iff_all_flat`
- cert: `vp_archive_seam_curvature_action.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Archive action is accumulated seam curvature and vanishes exactly when all included levels are transport-flat.

### D0-ARCHIVE-ENTROPY-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_06/08`
- module: `D0.Probability.EntropyCouplingKernel`
- theorem: `archive_entropy_kernel_exists_if_HST;archive_forgetting_channel_unique`
- cert: `vp_archive_entropy_softmax_coupling.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Entropy-selected archive coupling interface plus finite-stage softmax coupling cert.

### D0-ARCHIVE-FIELD-EQ-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveFieldEquation`
- theorem: `matrix_hs_square_expansion;first_variation_trace_square;seam_action_variation_quadratic_expansion;stationary_iff_first_variation_zero;vacuum_equation_iff_stationary;sourced_equation_variational_form`
- cert: `vp_archive_variational_field_equation.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Finite seam-action variation gives the field-gradient pairing and sourced variational equation.

### D0-ARCHIVE-SEAM-CURVATURE-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveCurvatureDensity`
- theorem: `seamCommutator_zero_iff_operator_transport_flat;seamCurvatureDensity_nonnegative;seamCurvatureDensity_zero_iff_flat`
- cert: `vp_archive_seam_curvature_action.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Curvature is the seam commutator density; cert checks exact rank two and seam support.

### D0-BARYON-POLES-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.BaryonAnonymousPoleSet`
- theorem: `baryon_anonymous_image_poles_cert`
- cert: `vp_baryon_40_56_anonymous_poles.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Image-basis compressed pole cert. [was:BARYON-ANONYMOUS-POLE-CERT-CLOSED]

### D0-BARYON-S3-SYM-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_baryon_s3_tensor_symmetrizer.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] S3 symmetrizer on 27 ordered triples -> decuplet-10 symmetric carrier.

### D0-BH-CAPACITY-A4-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_black_hole_capacity_a4_witness.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] ABCD four-role denominator boundary-cell count -> A/4 entropy witness.

### D0-BOOK04-SELECTORS-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_book04_centered_full_support_selectors.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] selectors over full support 0..2R; zero iff support-symmetry; no inserted indicator.

### D0-BOOK04-SELECTORS-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_book04_combinatorial_selector_origins.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] support radii from upstream D0 formulas (35, 306, 19); no fitted targets.

### D0-CANONICAL-OP-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_canonical_operator_search.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] tripartite-Laplacian canonical generation operator selection.

### D0-CKM-EXACT-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_ckm_exact_matrix_certificate.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] exact integer cyclic-shift orientation; doubly-stochastic permutation witness.

### D0-CKM-K0-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04/08`
- module: ``
- theorem: `none`
- cert: `vp_ckm_phason_holonomy_k0.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: CKM holonomy has a stable K-theory class and CP phase is oriented noncommutative area. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-CLASS5-ALIASING-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_class5_aliasing_cabibbo.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Root C T-C.3] Closes BOOK_05 05.6 third soft joint (class-5 aliasing, formerly formulated-not-formalized). Cert vp_class5_aliasing_cabibbo.py: branch group (Z/44)* order 20, unique 5-Sylow Z5 + unique 2-Sylow Z2xZ2, characteristic subgroup orders {1,4,5,20}, 20=4*5=|ABCD|*D_Sigma. class-4 killed by orientation (owned THE 3.11.B / Z2-cover); CLASS-5 killed by aliasing: |Z5|=5=D_Sigma, winding-5 orbit bijects onto the 5 address classes (pointer collision=hidden memory, M1-forbidden). Survivors {1,20} => m_s/m_d=20. BRIDGE (not promoted): sinθ_C=1/sqrt20=0.22361 vs 0.22501 (0.62%, within GST O(λ²)≈5%). HONEST: class-5 exclusion closed at finite alias level; full hidden-memory M1 contradiction (grammar 01.11C) stays theorem-target, same standing as the class-4 kill.

### D0-CVFT-F4

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_02/05`
- module: ``
- theorem: `none`
- cert: `vp_cvft_uv_feedback_tail_bound_refined.py;vp_cvft_ueff_pole_discipline.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: UV cutoff claims have deterministic finite cert candidates for the refined tail bound under |z|rho(F_N)<1; Lean proof remains open. [was:CERT-CANDIDATE] [8C: linked passing cert]

### D0-CVFT-F7

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_cvft_boundary_channel_rank.py;vp_cvft_refined_logdet_rank_bound.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Boundary-local rank control has deterministic finite cert candidates; it supports localization only and is not an A4 proof. [was:CERT-CANDIDATE] [8C: linked passing cert]

### D0-DM-CLASSICALITY-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_06/08`
- module: `D0.Detector.WeakCouplingClassicalization`
- theorem: `weak_coupling_readout_classical_guardrail`
- cert: `vp_dm_classicality_guardrail.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Weak-coupling/mode-averaging nonclassical signature suppression guardrail.

### D0-EDGE-ALPHA-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Edge.AlphaRamificationConstructive`
- theorem: `edge_alpha_trace_seam_cert`
- cert: `vp_edge_alpha_trace_constructive.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Unitary dilation edge alpha trace cert. [was:EDGE-ALPHA-TRACE-CERT-CLOSED]

### D0-EDGE-RAMIFICATION-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Edge.RamificationFromUeEffCompanion`
- theorem: `ramification_companion_cover_cert`
- cert: `vp_ramification_edge_ueff_companion.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Companion cover cert; physical-edge embedding remains scoped. [was:RAMIFICATION-COMPANION-COVER-CERT-CLOSED]

### D0-EW-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_higgs_anchor_projector.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] Pi_H identity on scalar anchor image; rank.V13=39; delta0-normalized defect.

### D0-FOUND-004

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_02`
- module: `D0.Foundation.QuadraticPeel`
- theorem: `quadratic_peel_born_holography_cert`
- cert: `vp_quadratic_peel_born_holography.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Quadratic peel cert.

### D0-FTHEORY-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_ftheory_lw2016_chiral_recombination_layer.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] published chi_R ledger recombines to absolute 3-generation SM multiplets.

### D0-GRAV-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_single_section_gravity_completion.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] ell_P, G_N from delta0, Omega8, phi^(V9.V11); CODATA G is benchmark.

### D0-GRAV-004

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Gravity.MeasurementHorizonEquivalence`
- theorem: `measurement_horizon_equivalence_cert`
- cert: `vp_measurement_horizon_equivalence.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Measurement seam / horizon law cert. [was:OPERATOR-LAW-CLOSED]

### D0-GRAV-005

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Gravity.OpticalJetBackreaction`
- theorem: `optical_jet_backreaction_cert`
- cert: `vp_optical_jet_backreaction.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Optical jet backreaction law cert. [was:OPERATOR-LAW-CLOSED]

### D0-GRAV-006

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Gravity.HorizonJetAndBaryonPole`
- theorem: `horizon_jet_baryon_pole_layer_cert`
- cert: `vp_horizon_jet_axis_observable.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Horizon closed; jet + baryon image-basis certs present. [was:CERT-SCAFFOLD-CLOSED]

### D0-HEAT-TRACE-FIT-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07/08`
- module: ``
- theorem: `none`
- cert: `vp_archive_heat_trace_expansion_fit.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] Theta(u) ~ u^-2(a0+a1 u+a2 u^2) on the archive Laplacian; finite-object fit.

### D0-HIGGS-YUKAWA-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_higgs_yukawa_section_transfer.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] Y compatible with rank-2 scalar projector; Hermitian; single action section.

### D0-HODGE-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_finite_hodge_complex_core.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] finite cochain complex d.d=0 + finite Hodge Laplacian.

### D0-HODGE-LINKS-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04/07`
- module: ``
- theorem: `none`
- cert: `vp_hodge_matter_gravity_archive_links.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] matter on C1, TT gravity on symmetric C1, shared finite cochain carrier.

### D0-HST-ARCHIVE-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_06/08`
- module: `D0.Probability.HSTExternalInterface`
- theorem: `hst_admissible_from_certificates;entropy_kernel_exists_if_HST`
- cert: `vp_archive_subgaussian_hst_admissibility.py;vp_archive_convex_order_domination.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: HST is external theorem object; D0-side archive hypotheses are cert-backed.

### D0-IM-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_06`
- module: `D0.IM.SelfSubstrateTrace`
- theorem: `self_substrate_trace_principle_cert`
- cert: `vp_self_substrate_trace_principle.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: IM substrate trace cert.

### D0-IM-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_06`
- module: `D0.IM.FractalTick`
- theorem: `fractal_tick_cert`
- cert: `vp_fractal_tick_informational_mechanics.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Fractal tick cert.

### D0-IM-004

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_01/06`
- module: `D0.Topology.WitnessHalting`
- theorem: `witness_halting_cert`
- cert: `vp_mobius_witness_topological_halting.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Möbius witness halting cert.

### D0-KTHEORY-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_00/01/02/04/05/06`
- module: ``
- theorem: `none`
- cert: `vp_gap_labeling_d0_tiling_hull.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Stable K-theory gap labels are countable and topological. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-LEPTON-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_charged_lepton_transfer_certificate.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] frozen e/mu/tau ratios, exponents 0,1/4,1/3.

### D0-MASTER-BOOTSTRAP-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_master_bootstrap_and_volume_derivative.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] V_N=rank(P_N); Z_N=Tr e^{-bD} det(I-zF)^-1; finite pressure split.

### D0-MESON-DEFECT-ALGEBRA-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_meson_defect_transfer_algebra.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] Fin E x Fin Gen carrier; self-adjoint PSD flavour defect.

### D0-MESON-K0-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04/08`
- module: ``
- theorem: `none`
- cert: `vp_phason_domain_wall_mesons.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Meson domain wall tension and spectrum admit stable K0 gap labels. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-METRO-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `METROLOGY`
- module: ``
- theorem: `none`
- cert: `vp_calibration_dag_and_lambda_section_rigidity_20260522.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] parameter-free Lambda_act/tau0/ell0 rigidity certificate.

### D0-MINCUT-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_finite_mincut_holographic_entropy.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] Ford-Fulkerson max-flow/min-cut = A/4-normalized boundary capacity.

### D0-NEUTRON-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_neutron_lifetime_rate_closure.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] downstream of closed lambda_p, lambda_n, Lambda_act, tau0, delta0; no measured lifetime input.

### D0-NOAXION-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_05/08`
- module: ``
- theorem: `none`
- cert: `vp_no_axion_finite_cochain.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] finite topological density + exact/coexact cancellation; no axion zero-mode.

### D0-NONABELIAN-SEAM-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_nonabelian_seam_gap.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] finite positive gap outside the commuting kernel.

### D0-PHASON-FORCING-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_phason_forcing.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Iter4 T5.1] Closes the phason LANGUAGE DEBT by FORCING (not mass-BRIDGE). Owner of the phason concept across ~99 uses. Cert vp_phason_forcing.py: cut-and-project carrier (forced, BOOK_01 01.19a) has perp DOF d_perp=D-d_par=2-1=1 (the phason); phason shift=intercept change preserves the Sturmian factor set (k=1..8) => local isomorphism => zero patch cost => GAPLESS Goldstone; density-preserving relabel => no EM charge => DARK radiation-free mode. Negative control: rational slope differs. Owning section BOOK_08 08.49. HONEST: forces the CONCEPT; downstream K-theory/spectral-triple phason-holonomy (QUASI007/008/009) stay cert-closed with EXTERNAL-GAP, not promoted.

### D0-PROTON-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_proton_terminal_destructive_readout.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] readout-306 terminal formula; 938 MeV is benchmark not input.

### D0-QUANT-MET-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `METROLOGY`
- module: `D0.Metrology.QuantumLimits`
- theorem: `quantum_metrology_limits`
- cert: `vp_quantum_metrology_limits.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: PSD purification inequality (lemma) + conditional φ^{-2} flux + Bragg spectrum targets. [was:OPERATOR-LEMMA-CERT]

### D0-QUANT-MET-002

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `METROLOGY`
- module: `D0.Metrology.PSDPurification`
- theorem: `psd_purification_inequality`
- cert: `vp_quantum_metrology_limits.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Admitted operator lemma F_lab ≽ Π F_N Π. [was:OPERATOR-LEMMA-CERT]

### D0-QUASI007-MESON-PHASON-DOMAIN-WALLS-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_04/08`
- module: ``
- theorem: `none`
- cert: `vp_phason_domain_wall_mesons.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Meson domain walls are six oriented nonzero phason boundaries lifted by generation readout to an 18-state finite carrier while meson transfer still uses the existing Edge by Generation lifted flavour-defect origin. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-SDE-K0-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `vp_phason_flip_entropy_sde.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: S_DE relaxation modes are gap-labeled. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-SOLENOID-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_01/07`
- module: ``
- theorem: `none`
- cert: `vp_noncommutative_solenoid_gravity.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Noncommutative solenoid model is admitted over the tiling hull. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-SPIN2-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_finite_spin2_wave_operator_concrete.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] TT projector on full 10-dim Sym(4) basis; 2 polarizations.

### D0-TIME-MODULAR-FLOW-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `formal_core`
- book: `BOOK_01`
- module: ``
- theorem: `none`
- cert: `vp_quasicrystal_time_sturmian.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [Root B synthesis bonus] Quasicrystal carrier = symbolic dynamics of the golden foliation of the time torus. Cert vp_quasicrystal_time_sturmian.py UPGRADES the prose-only 40-symbol check to EXACT executable: cut-and-project word slope phi^-2 = Fibonacci substitution word a->ab,b->a to N=4000 (exact isqrt floors floor(k phi)=(k+isqrt(5k^2))//2), rare-letter freq=phi^-2, aperiodic, rational-slope negative control. Arrow=Pisot |psi|=phi^-1<1 reuses D0-TIME-2D-PISOT-001 (proved). HONEST: proves EXACT SYMBOLIC coincidence only; full topological conjugacy (phi^-2 rotation = foliation return map; Morse-Hedlund/Vershik) needs ergodic machinery not in Mathlib -> theorem-target; arrow interpretation rests on Adler-Weiss external citation.

### D0-ABCD-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01`
- module: `D0.Core.DyadABCD`
- theorem: `ABCD_cardinality`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: ABCD represented as Dyad x Dyad.

### D0-ARCHIVE-BIANCHI-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveBianchiIdentity`
- theorem: `archiveCanonicalLaplacian_row_sum_zero;archiveLiftOperator_row_sum_one;seamCommutator_row_sum_zero;curvature_gradient_conserved;source_must_be_conserved`
- cert: `vp_archive_variational_field_equation.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Row-sum conservation of the seam curvature gradient forces conserved archive sources.

### D0-ARCHIVE-GAUSSIAN-CHANNEL-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_06/08`
- module: `D0.Probability.ArchiveClassicalGaussianChannel`
- theorem: `archive_macro_channel_classical_gaussian`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Combines HST interface and detector classicalization as typed macro-channel statement.

### D0-ARCHIVE-LAPLACIAN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveLaplacianProperties`
- theorem: `archive_laplacian_symmetric;archive_laplacian_nonnegative;archive_laplacian_zero_mode_control`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite archive Laplacian is symmetric/nonnegative with zero-mode control.

### D0-ARCHIVE-MODE-EXPONENT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07/08`
- module: `D0.Geometry.ArchiveModeExponent`
- theorem: `archive_mode_exponent_eq_abcd;archive_mode_exponent_eq_lorentz_dimension;archive_modes_forced`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Archive exponent 4 forced by ABCD/Lorentz carrier dimension.

### D0-ARCHIVE-PHASE-CURVATURE

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchivePhaseCurvatureObstruction`
- theorem: `phase_flat_iff_zero_curvature_obstruction;NO_GO_PHASE_LAPLACIAN_PROJECTIVE_COMPATIBILITY;NO_GO_PHASE_CURVATURE_OBSTRUCTION`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Nonvanishing curvature obstruction on refined phase fibers.

### D0-ARCHIVE-PHASE-DISTANCE

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_06/07`
- module: `D0.Geometry.ArchivePhaseDistance`
- theorem: `archivePhaseDistance_nonnegative;archivePhaseDistance_symmetric;archivePhaseDistance_zero_iff`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Metric on finite fibers.

### D0-ARCHIVE-RESOLVENT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveResolventCompactness`
- theorem: `finite_stage_resolvent_compact;archive_spectral_tightness_from_mode_growth;d0_archive_profinite_resolvent_compactness`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite-stage compactness/projection/tightness structure for archive tower.

### D0-ARCHIVE-SCALAR-REDUCTION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Active.ScalarPoissonReduction`
- theorem: `scalar_stationarity_implies_archive_poisson`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Stationarity under scalar perturbations reduces to discrete Poisson.

### D0-ARCHIVE-STRESS-CONSERVATION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Frozen.ConservedStressProjection`
- theorem: `constrained_projection_applies_to_archive_gradient`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Constrained representative is symmetric and conserved.

### D0-ARCHIVE-STRESS-REP-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveStressRepresentative`
- theorem: `raw_gradient_equivalent_to_canonical_stress;canonical_stress_symmetric;canonical_stress_conservation_no_go`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Symmetric representative defined and raw gradient equivalent.

### D0-ARCHIVE-TOWER-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_06/07`
- module: `D0.Geometry.ArchiveRefinementTower`
- theorem: `terminal_readout_stable;archive_depth_strictly_increases;spectral_modes_strictly_increase;archive_projection_surjective`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Terminal readout stable while archive/spectral refinement grows.

### D0-ARCHIVE-VARIATION-DUAL-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveVariationDual`
- theorem: `pairing_depends_only_on_symmetric_part;skew_part_annihilates_admissible_variations`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Admissible variation dual properties.

### D0-ARCHIVE-WEAK-FIELD-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07/08`
- module: `D0.Geometry.ArchivePoissonEquation`
- theorem: `poisson_requires_neutral_source;poisson_solution_unique_mod_constant`
- cert: `vp_archive_weak_field_poisson.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Poisson equation has unique solution up to constant.

### D0-BORN-QUADRATIC-ORIGIN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Core.BornQuadraticOrigin`
- theorem: `parallelogram_response_is_quadratic_form;quarter_turn_quadratic_forces_norm_square;born_quadratic_origin_closed`
- cert: `vp_born_quadratic_origin.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite phase quadrature gives quadratic response and unit phase-blind calibration gives norm-square before Born normalization.

### D0-CAPACITY-V11-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Core.FiniteTypes`
- theorem: `card_v11`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: V11 exact cardinality.

### D0-CAPACITY-V13-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Core.FiniteTypes`
- theorem: `card_v13`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: V13 exact cardinality.

### D0-CAPACITY-V9-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Core.FiniteTypes`
- theorem: `card_v9`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: V9 exact cardinality.

### D0-CARRIER-FULL-FORCING-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/03`
- module: `D0.Synthesis.CarrierForcing`
- theorem: `carrier_full_forcing`
- cert: `vp_carrier_full_forcing.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [Root C synthesis] Finite forcing of the carrier. Cert vp_carrier_full_forcing.py: roles ABCD=Dyad×Dyad=Klein four (|.|=4); ORBITAL BLOCK-CONSTANCY proved by exhaustion on the (2,2,2) faithful model (all 64 S_a×S_b×S_c-invariant symmetric loopless relations are block-constant); UNIQUE M1-admissible block pattern (loopless+complete) -> complete tripartite K(9,11,13), |V|=33 |E|=359; tower-stop finite: 3 forced zones->3 rungs [9,11,13], |Tr(T^2)|=3, Lucas impedance I_n=L_n/9n cross-check. Lean L5 CORE-FORMALIZED via D0.Synthesis.CarrierForcing (carrier_full_forcing): roles_card=4, admissible_unique (native_decide over 512 patterns), edge_count_359, address_ladder, Tr(T^2)=3. HONEST: block-constancy by exhaustion on faithful model (general sizes inherit by same transitivity); full M1 NO-EXTENSION theorem stays theorem-target; impedance is convergent cross-check (GOLDEN CHK 61.2), not a closed no-go. Closes BOOK_05 05.6 soft-joint-1 (role=orbit).

### D0-CKM-NONTRIVIAL-FLAVOUR-ALGEBRA-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.CKMNontrivialFlavourAlgebra`
- theorem: `Matter.permutation_witness_has_no_nontrivial_flavour_transfer;Matter.overlap_response_can_force_nonpermutation_transfer;Matter.torus_overlap_generates_nonpermutation_flavour_transfer;Matter.nontrivial_flavour_defect_positive_response;Matter.nontrivial_flavour_defect_admissible_for_meson_transfer`
- cert: `vp_generation_overlap_response_origin.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite flavour defect is sourced by non-permutation overlap and has positive response without physical CKM entries.

### D0-CONDENSED-PHI-VACUUM-CUT-PROJECT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_00/01/02/06/08`
- module: `D0.Condensed.CondensedPhiVacuum;D0.Physics.QuasicrystalPhenomenology`
- theorem: `phi_vacuum_stage_card_eq_two;condensed_phi_vacuum_support_closed;cut_project_quasicrystal_matches_phase_unfolding;Physics.d0_phi_cut_project_matches_condensed_phi_vacuum`
- cert: `vp_condensed_phi_vacuum_cut_project.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Condensed/profinite phi-vacuum support exposes terminal qT=44 branch count 20 electroweak qEW=710 branch count 280 and depth 35 and the physics cut-project readout is tied to this support.

### D0-DIM-LADDER-COMPACT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_06`
- module: `D0.Claims.DimLadderCompact`
- theorem: `dim_ladder_compact_cert`
- cert: `vp_dim_ladder_compact.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Q(D)=phi^(D-4); quantum=1 at D=4=|ABCD|; Q(1)=phi^-3=2delta0; exact Q(phi). Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.DimLadderCompact (dim_ladder_compact_cert); native_decide/decide on the real finite content.

### D0-FINAL-BRIDGE-INDEX-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_08`
- module: `D0.Bridge.FinalBridgeIndex`
- theorem: `Bridge.D0_FINAL_FOUNDATION_INDEX`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Machine-checkable final bridge index over closed D0 foundation groups.

### D0-FOUND-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Core.Phi`
- theorem: `primitive_quadratic_unique_pos_root`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Exact p+p^2=1 positive root uniqueness.

### D0-GEN-INDEX-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Spectrum.BranchDefectProjectiveGeneration`
- theorem: `exactly_three_projective_branch_defect_generations;defectAction_order_three;defect_generation_card`
- cert: `vp_pi0_branch_defect_generation.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Generation index is the projective closure P1(F2) of the minimal two-branch defect plane; masses/Yukawa hierarchy are not included.

### D0-GEOM-HEAT-TRACE-EH-PROXY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_08`
- module: `D0.Geometry.HeatTraceEHProxy`
- theorem: `weighted_laplacian_entry;trace_square_weighted_laplacian_decomposition;offdiag_proxy_nonnegative;regular_graph_diagonal_square_term`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Weighted trace square decomposition and proxy nonnegativity.

### D0-GEOM-OBSTRUCT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveCurvatureObstruction`
- theorem: `flat_archive_iff_zero_curvature_obstruction`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Flat archive iff zero curvature obstruction.

### D0-GRAVITY-ENTROPIC-ARCHIVE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Gravity.EntropicArchiveInterface`
- theorem: `Gravity.boundary_capacity_nonnegative;Gravity.graph_laplacian_symmetric;Gravity.conserved_flux_no_creation;Gravity.entropic_tension_energy_nonnegative;Gravity.entropic_archive_interface_closure`
- cert: `vp_entropic_archive_gravity.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite graph cut capacity heat-trace observable archive flux conservation and nonnegative entropic tension are formal D0 objects.

### D0-HULL-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_00/01`
- module: `D0.Topology.TilingHull`
- theorem: `Topology.d0_hull_has_finite_local_complexity;Topology.d0_hull_has_phi_cut_project_origin;Topology.d0_hull_is_nonperiodic;Topology.d0_hull_has_long_range_order;Topology.d0_hull_supports_gap_labeling`
- cert: `vp_d0_tiling_hull.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: D0 tiling hull is aperiodic and repetitive with finite local complexity.

### D0-HURWITZ-INTERNAL-DIMENSION-SELECTOR-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Algebra.D0InternalDimensionSelector`
- theorem: `Algebra.d0_internal_dimension_value;Algebra.d0_internal_dimension_value_mem;Algebra.d0_admissible_dimension_iff;Algebra.d0_admissible_internal_dimension_iff;Algebra.octonion_witness_not_associative_matrix_algebra;Algebra.d0_selector_closes_core_internal_dimension`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: D0 core dimension selection is finite and internal; octonion witness is finite composition data not an associative Matrix 8 8 algebra.

### D0-HURWITZ-LOCAL-BOUNDARY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Algebra.HurwitzLocalBoundary`
- theorem: `Algebra.dim_one_admissible;Algebra.dim_two_admissible;Algebra.dim_four_admissible;Algebra.dim_eight_admissible;Algebra.dim_one_has_local_finite_witness;Algebra.dim_two_has_local_finite_witness;Algebra.dim_four_has_local_finite_witness;Algebra.dim_eight_has_local_finite_witness;Algebra.hurwitz_local_boundary_split`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Local finite admissibility and table witnesses are internal D0 theorems for dimensions 1/2/4/8.

### D0-INFORMATION-QUASICRYSTAL-PHASE-UNFOLDING-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_00/01/06/07/08`
- module: `D0.Geometry.HurwitzRigidPhaseGenerator;D0.Geometry.PhaseReturnBranchCount;D0.Geometry.PhaseUnfoldingQuasicrystal`
- theorem: `Geometry.phi_phase_is_nonperiodic;Geometry.phi_continued_fraction_all_ones;Geometry.hurwitz_rigid_low_denominator_bound;Geometry.finite_return_modulus_unfolds_branches;Geometry.toral_runtime_supplies_quasicrystal_order;Geometry.quasicrystal_order_not_periodic_lattice`
- cert: `vp_information_quasicrystal_phase_unfolding.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite tick order plus irrational phi^-2 phase plus return quotients yields ordered aperiodic readout-generated branch geometry without a primitive lattice.

### D0-KERNEL-ZONE-SPLIT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/04`
- module: `D0.Claims.KernelZoneSplit`
- theorem: `kernel_zone_split`
- cert: `vp_kernel_zone_split.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: ker(adj K(9,11,13))=30=8+10+12; rank 3 = space; exact integer LA. Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.KernelZoneSplit (kernel_zone_split); native_decide/decide on the real finite content.

### D0-LEAN-CORE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `Lean formalization`
- module: `D0.TheoremLedger.ReleaseStatus`
- theorem: `lean_core_release_candidate`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Release-candidate core status backed by build and CI.

### D0-MASTER-EVOLUTION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_00/01/03/06/07/08`
- module: `D0.Dynamics.MasterEvolutionTheorem`
- theorem: `Dynamics.T_squared_plus_T_minus_identity_eq_zero;Dynamics.det_T_pow_square_eq_one;Dynamics.lucas_heat_moment_bridge;Dynamics.detector_is_fixed_under_ladder;Dynamics.d0_phi_quasicrystal_vacuum_support;Dynamics.master_evolution_theorem`
- cert: `vp_master_evolution_theorem.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Single finite evolution package closes T quadratic identity signed Lucas traces Lefschetz scene counts determinant-square balance dark even-window cancellation heat-Lucas moments fixed detector ladder and phi-quasicrystal support without external data.

### D0-MATTER-ANOMALY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.GenerationAnomalyPreservation`
- theorem: `Matter.anomaly_sum_triples;Matter.anomaly_zero_preserved`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Generational anomaly sum structure.

### D0-MATTER-LOCALIZATION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Active.NonzeroMatterSourceNeutrality`
- theorem: `Matter.localized_matter_source_neutral_if_anomaly_free`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Conditional matter source neutrality under localization assumption.

### D0-MATTER-SOURCE-NEUTRALITY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04/08`
- module: `D0.Matter.GeneratedMatterSource`
- theorem: `Matter.generated_matter_source_neutral_if_anomaly_free;Matter.NO_GO_MATTER_SOURCE_NEUTRALITY`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Generated-source neutrality closes the minimal base interface; nonzero localized sources are handled by D0-MATTER-LOCALIZATION-001.

### D0-MATTER-STRESS-COUPLING-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.ArchiveStressCoupling`
- theorem: `Matter.matterStressMatrix_symmetric;Matter.matterStressMatrix_conserved;Matter.generated_matter_source_conserved_if_anomaly_free;Matter.generated_matter_source_zero_if_anomaly_free`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Generation/anomaly layer defines a symmetric conserved archive stress source; anomaly-free reps give zero source in this minimal coupling.

### D0-MESON-POSITIVE-DEFECT-TRANSFER-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.MesonDefectTransferOrigin`
- theorem: `Matter.meson_support_projector_idempotent;Matter.flavour_defect_positive_response;Matter.meson_positive_defect_transfer_admissible`
- cert: `vp_meson_positive_defect_transfer.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Meson transfer uses the typed Edge by Generation carrier and lifted flavour defect rather than a direct sum of unrelated spaces.

### D0-MIXING-HIERARCHY-INVERSION-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Claims.MixingHierarchyInversion`
- theorem: `mixing_hierarchy_inversion`
- cert: `vp_mixing_hierarchy_inversion.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [8D Tier-1 forced] rank-3 nondegenerate (CKM small) vs nullity-30 degenerate (PMNS large); cubic lambda^3-359lambda-2574. Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.MixingHierarchyInversion (mixing_hierarchy_inversion); native_decide/decide on the real finite content.

### D0-NCG-INDEX-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_02`
- module: `D0.Combinatorics.Tripartite`
- theorem: `no_3_simplices_clique_complex`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: No four-partite clique guardrail.

### D0-OMEGA8-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01`
- module: `D0.Core.DyadABCD`
- theorem: `omega8_cardinality`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Omega8 represented as Role x Bool.

### D0-OPERATOR-EDGE-STIFFNESS-ORIGIN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_08`
- module: `D0.Geometry.EdgeStiffnessOrigin`
- theorem: `Geometry.capacityCore_symmetric;Geometry.capacityCore_psd;Geometry.symmOffDiag_projection_trace_transparent;Geometry.edge_stiffness_preserves_symmOffDiag;Geometry.edge_stiffness_energy_nonnegative;Bridge.edge_stiffness_origin_closed`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Edge stiffness origin with symm-offdiag projection.

### D0-OPERATOR-VECTOR-LAPLACIAN-ORIGIN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_08`
- module: `D0.Matter.VectorOperatorOrigin`
- theorem: `Matter.vector_laplacian_preserves_skew;Matter.vector_laplacian_energy_nonnegative;Matter.vector_operator_origin_applies_to_field_equation;Bridge.vector_operator_origin_closed`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Vector operator origin via negative double commutator.

### D0-PHASE-TOWER-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Combinatorics.PhaseTowerMinimality`
- theorem: `terminalWindow_minimal;fullOrientedWindow_minimal;fullOrientedWindow_C0_minimal`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Forced windows are minimal synchronization moduli, not post-hoc choices.

### D0-PHASE-UNFOLD-002

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Phase`
- theorem: `forced_terminal_window;terminal_window_totient;forced_ew_window;ew_window_totient;ew_depth`
- cert: `vp_v1143_forced_return_windows_capacity.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Exact 44 and 710 forced-window arithmetic. [8C: linked passing cert]

### D0-PHI-HURWITZ-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.NumberTheory.HurwitzMinimaxPhi`
- theorem: `HURWITZ_MINIMAX_D0_CLASS_PROVED`
- cert: `vp_v1142_hurwitz_phi_phase_rigidity.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: D0 admissible period-one quadratic phase class proved; full global Lagrange spectrum remains external mathematical background. [8C: linked passing cert]

### D0-Q8-DEDEKIND-MINIMALITY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01`
- module: `D0.Claims.Q8DedekindMinimality`
- theorem: `q8_dedekind_minimality`
- cert: `vp_q8_dedekind_minimality.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [8D Tier-1 forced] unique minimal Hamiltonian non-abelian group <=8 (Dedekind 1897); [Q8,Q8]=Z=Phi={+-1}. Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.Q8DedekindMinimality (q8_dedekind_minimality); native_decide/decide on the real finite content.

### D0-QUASI002-PHASON-STRAIN-GENERATIONS-BARYON-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_02/04/05/08`
- module: `D0.Matter.PhasonStrainGenerations`
- theorem: `Matter.phason_mode_card_eq_three;Matter.generation_phason_mode_card_eq_three;Matter.baryon_phason_triple_card_eq_27;Matter.baryon_phason_symmetric_sector_dim_eq_ten;Matter.phason_s3_symmetrizer_admits_baryon_decuplet_transfer;Matter.full_baryon_multiplet_requires_phason_s3_symmetrizer;Matter.phason_strain_generations_baryon_closure`
- cert: `vp_quasi002_phason_strain_generations_baryon.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Phason modes are the three torus-shell roles ordered baryon triples have dimension 27 the S3 symmetric sector has decuplet dimension 10 and nucleon-line extrapolation remains forbidden without the phason S3 symmetrizer.

### D0-QUASI006-GALOIS-LORENTZ-SIGNATURE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_06/07/08`
- module: `D0.Physics.GaloisLorentzSignature`
- theorem: `Physics.galois_lorentz_signature_closed`
- cert: `vp_galois_lorentz_signature.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Active/archive Galois trace layers and determinant-square balance are integrated with the terminal role signature (1,3) while Euclidean and split exports remain blocked.

### D0-QUASICRYSTAL-PHENOMENOLOGY-OPERATOR-ORIGIN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_00/01/02/04/06/07/08`
- module: `D0.Physics.QuasiGenerationsInflation;D0.Physics.ArchivePhasonDarkMatter;D0.Physics.WindowOffsetChirality;D0.Physics.PhasonFlipInertia;D0.Physics.WindowFractionalCharge;D0.Physics.QuasicrystalPhenomenology`
- theorem: `Physics.quasi_generation_inflation_orbit;Physics.archive_phason_strain_em_dark_metric_visible;Physics.window_offset_forces_chiral_readout;Physics.phason_flip_drag_positive_cost;Physics.fractional_charge_window_weights;Physics.quasicrystal_phenomenology_operator_origin`
- cert: `vp_quasicrystal_phenomenology_operator_origin.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: One D0PhiCutProject finite cut-and-project owner yields generation inflation classes archive phason dark metric response window-offset chirality phason-flip rewrite inertia and fractional window-sector charge weights.

### D0-SCENE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Combinatorics.Tripartite`
- theorem: `vertex_count_K_9_11_13;edge_count_K_9_11_13;triangle_count_K_9_11_13`
- cert: `none`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Tripartite counts 33/359/1287.

### D0-SIGNATURE-31-SPLIT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_06/07`
- module: `D0.Claims.Signature31Split`
- theorem: `signature_31_split`
- cert: `vp_signature_31_split.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [8D Tier-1 forced] 3=rank(adj) space + 1 Pisot modular flow time; distinct objects. Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.Signature31Split (signature_31_split); native_decide/decide on the real finite content.

### D0-SRC-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.NuclearShellContactSRC`
- theorem: `Matter.same_shell_contact_index_zero_for_unmatched_valence_protons;Matter.same_shell_contact_turns_on_for_matched_valence_pn;Matter.src_contact_requires_shell_projector_overlap;Matter.nuclear_shell_contact_src_closure`
- cert: `vp_nuclear_shell_contact_src.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: SRC contact is a finite shell-projector overlap readout through an angular-momentum shell-contact selector.

### D0-SYMPLECTIC-GLEASON-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01`
- module: `D0.Synthesis.CarrierForcing`
- theorem: `symplectic_form_unique`
- cert: `vp_symplectic_gleason_uniqueness.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [Root C T-C.4] Closes the UNIQUENESS leg of the Gleason-2D loophole. Cert vp_symplectic_gleason_uniqueness.py: quarter-turn J(x,y)=(-y,x) in SL(2,Z) (det=1, J^2=-I); x^2+y^2 is J-invariant; ANY J-invariant quadratic a x^2+b xy+c y^2 forces a=c, b=0 => unique up to scale. Lean L5 CORE-FORMALIZED via symplectic_form_unique (a=c and b=0 from h 1 0/h 1 1). EXISTENCE (x^2+y^2 is the phase-blind response) owned by D0-BORN-QUADRATIC-ORIGIN-001 (proved). HONEST: categorical Ostrik/Ising uniqueness (tau⊗tau=1⊕tau unique 2-object fusion) needs fusion-category machinery not in kernel -> theorem-target.

### D0-TORAL-AUTOMORPHISM-GALOIS-BALANCE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_03/06/07/08`
- module: `D0.Dynamics.ToralAutomorphism;D0.Dynamics.GaloisConjugateBalance;D0.Dynamics.DarkSectorCoarseGrain`
- theorem: `Dynamics.trace_evolution_unfolds_d0_geometry;Dynamics.det_T;Dynamics.det_T_pow;Dynamics.toral_volume_conservation_square;Dynamics.trace_T_pow_eq_signed_lucas;Dynamics.generationTrace_eq_three;Dynamics.abcdTrace_eq_four;Dynamics.memoryTorusTrace_eq_eleven;Dynamics.dark_sector_even_window_readout_zero`
- cert: `vp_toral_automorphism_galois_balance.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Fixed finite integer time matrix T yields signed Lucas trace layers 3/4/11 determinant-square volume balance and exact even-window archive sign cancellation without external-data input.

### D0-TORUS-CORE13-GEOMETRY-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_02/03`
- module: `D0.Geometry.TorusCore13GeometryOrigin`
- theorem: `Geometry.torus_shell_card_eq_three;Geometry.TorusParameter.outer_inner_ratio;Geometry.TorusParameter.major_minor_ratio;Geometry.TorusParameter.equator_ratio;Geometry.radial_hopping_phase_drift_commutator_01;Geometry.radial_hopping_phase_drift_noncommute`
- cert: `vp_torus_core13_geometry_origin.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Finite torus shell owner proves three-shell carrier and noncommuting radial hopping versus phase drift without data input.

### D0-TORUS-GENERATION-OVERLAP-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.GenerationOverlapResponseOrigin`
- theorem: `Matter.torus_shell_noncommutativity_forces_nonpermutation_overlap_source`
- cert: `vp_generation_selector_origin.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Overlap origin is tied to torus shell noncommutativity while physical CKM entries remain downstream passport data.

### D0-TORUS-GENERATION-SELECTOR-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Matter.GenerationSelectorOrigin`
- theorem: `Matter.torus_geometry_forces_generation_selector_noncommute`
- cert: `vp_generation_selector_origin.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: Generation selector noncommutativity is sourced from finite torus shell geometry rather than a detached fixture selector.

### D0-VIETA-GALOIS-ABCD-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Claims.VietaGaloisAbcd`
- theorem: `vieta_galois_abcd`
- cert: `vp_vieta_galois_abcd.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: ABCD = Vieta=Galois data of x^2-x-1; delta0=1/(2phi^3) forced; exact Q(phi). Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.VietaGaloisAbcd (vieta_galois_abcd); native_decide/decide on the real finite content.

### D0-WINDOW44-GROUP-SPECTRUM-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_01/04`
- module: `D0.Claims.Window44GroupSpectrum`
- theorem: `window44_group_spectrum`
- cert: `vp_window44_group_spectrum.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [8D Tier-1 forced] (Z/44)*=Z2xZ2xZ5, |.|=20=d13, char subgroups {1,4,5,20}, 20=4x5. Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.Window44GroupSpectrum (window44_group_spectrum); native_decide/decide on the real finite content.

### D0-XI5-TORUS-DEFECT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_03/06`
- module: `D0.Claims.Xi5TorusDefect`
- theorem: `xi5_torus_defect`
- cert: `vp_xi5_torus_defect.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: xi5=phi^-5 torus-address defect: phi^5=11+phi^-5, L5=11, Tr(T^5)=-11; exact Z[phi]. Lean L5 CORE-FORMALIZED via D0.Claims.Xi5TorusDefect (xi5_torus_defect, native_decide; reuses D0.Dynamics.ToralAutomorphism trace_T_pow_eq_signed_lucas). alpha-row stays CHK.

### D0-Z2-SPINOR-COVER-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `formal_core`
- book: `BOOK_02/03`
- module: `D0.Synthesis.Z2SpinorCover`
- theorem: `z2_spinor_cover`
- cert: `vp_z2_spinor_cover.py`
- assumptions: `none`
- scope: Lean-owned finite/formal D0 core statement.
- notes: [Root B synthesis] One Z2=Z(Q8), seven incarnations unified machine-checked. Cert vp_z2_spinor_cover.py (exact Z[sqrt5]+Q8 table): [Q8,Q8]=Z(Q8)=Phi(Q8)={+-1} |Z|=2 (#3); Galois phi+psi=1 phi*psi=-1 g(x)=1-x involution (#1); Lucas L_n=phi^n+psi^n eps_n=phi^n-L_n=-psi^n chi(n)=(-1)^n (#2); det(T^n)=(-1)^n=chi(n) (#5,#6); 2-sheet+rank-doubling (#4,#7). JOINT A: signedLucasTrace n=det(T^n)*L_n and det T=-1=phi*psi (parity=det=Galois-norm). JOINT B: det(T^{n+2})=det(T^n) (+2 fixes sheet), det(T^{n+1})=-det(T^n) (+1 flips, banned by M1). Lean L5 CORE-FORMALIZED via D0.Synthesis.Z2SpinorCover (z2_spinor_cover), >=4/7 projections sorry-free. HONEST: cert verifies cover ALGEBRA; the M1-uniqueness of orientation=Gal(Q(sqrt5)/Q) stays GOLDEN forcing prose. Note: BOOK_02 02.34 prose sign typo eps_n=L_n-phi^n corrected to phi^n-L_n=-psi^n (matches 03.23.6).

### D0-NO-GO-BARE-ARCHIVE-NONABELIAN-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `formal_core`
- book: `BOOK_08`
- module: `D0.Bridge.OperatorOriginIndex`
- theorem: `Bridge.nonabelian_completion_boundary`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Nonabelian completion remains outside bare archive operator.

### D0-NO-GO-EDGE-STIFFNESS-SCALAR-LEAKAGE-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `formal_core`
- book: `BOOK_08`
- module: `D0.Geometry.EdgeStiffnessOrigin`
- theorem: `Geometry.edge_projection_prevents_scalar_leakage`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Bare HP+PH can leak scalar diagonal without symmOffDiag projection.

### D0-NOGO-LIGO-DISCOVERY-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `formal_core`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_ligo_discovery_negative_control.py`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: [8C orphan-harvest] freezes V3-V12 negative discovery scans; blocks proxy promotion.

### D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `formal_core`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveLaplacianPhaseNaturality`
- theorem: `NO_GO_ARCHIVE_PHASE_LOCAL_UNIQUENESS`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Naturality alone does not uniquely fix the operator without further phase structure.

### D0-GENERATION-RAYS-001

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `formal_core`
- book: `BOOK_04`
- module: `D0.Spectrum.GenerationSpectralRays`
- theorem: `NO_GO_GENERATION_RAYS_UNDEFINED`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Bare K(9,11,13) spectral cluster generation route is no-go. Core generation index is instead D0-GEN-INDEX-001 via projective branch-defect rays.

### D0-NO-GO-STRESS-SUITE-001

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `formal_core`
- book: `BOOK_02/04/05/06/07`
- module: `D0.NoGo.StressTestSuite`
- theorem: `NoGo.no_go_rank_one_higgs_scalar_projector;NoGo.no_go_isolated_phason_generation_carrier;NoGo.no_go_isolated_phason_baryon_s3_sector;NoGo.no_go_euclidean_signature_export;NoGo.no_go_stress_test_suite_closed`
- cert: `vp_no_go_stress_test_suite.py`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Negative-control suite blocks rank-one Higgs scalar projectors isolated one-phason generation or baryon closure and Euclidean signature export.

### D0-PHASE-TOWER-002

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `formal_core`
- book: `BOOK_01/02`
- module: `D0.Combinatorics.InfinitePhaseTower`
- theorem: `capacity_recursion_total;forced_terminal_window_all;current_recursion_stabilizes_at_shell_two`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Formal tower exists but current terminal recursion stabilizes; direct Einstein tower is not derived here.

### D0-SRC-NOGO-001

- type: `no-go`
- release_status: `NO_GO_PROVED`
- domain: `formal_core`
- book: `BOOK_04/05`
- module: `D0.Matter.NuclearShellContactSRC`
- theorem: `Matter.mass_number_alone_cannot_determine_src_contact;Matter.neutron_excess_alone_cannot_determine_src_contact`
- cert: `vp_nuclear_shell_contact_src.py`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: A-only and N/Z-only SRC scalar promotion fails on the finite Ca/Fe shell-contact witness.


## Domain: frontier

### D0-CVFT-001B

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_04/06/07/08`
- module: ``
- theorem: `none`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Sector projection package points to CVFT-F1 through CVFT-F8 and may not close matter gravity cosmology horizon gauge or empirical passport rows automatically.

### D0-CVFT-F1

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_02/04/08`
- module: ``
- theorem: `none`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Residue/coefficient origin must be derived from the feedback resolvent trace program before any physical coefficient promotion. [was:PROOF-OBLIGATION-EXPOSED]

### D0-CVFT-F2

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_07/08`
- module: ``
- theorem: `none`
- cert: `vp_horizon_emission_conjugate_feedback.py`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Horizon emission and greybody leakage remain frontier until the boundary operator and observable passport are frozen. [was:THEOREM-TARGET-SHARPENED] [8C: linked passing cert]

### D0-CVFT-F5

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_04/08`
- module: ``
- theorem: `none`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: IceCube dynamic feedback is an external passport candidate until data manifest response and frozen operator are pinned. [was:EMPIRICAL-PASSPORT-CANDIDATE]

### D0-CVFT-F6

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_04/07`
- module: ``
- theorem: `none`
- cert: `vp_gauge_boundary_commutator_obstruction.py`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Yang-Mills leakage/mass-gap language requires a gauge-boundary commutator obstruction theorem. [was:LOWER-BOUND-TARGET] [8C: linked passing cert]

### D0-CVFT-F8

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_08`
- module: ``
- theorem: `none`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: S_DE exceptional-point algebra is an effective two-mode transfer candidate only; not DESI pass H0 theorem or cosmology closure. [was:CERT-CANDIDATE]

### D0-EDGE-001

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_04`
- module: `D0.Edge.AlphaRamificationConstructive`
- theorem: `edge_alpha_trace_target`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Guardrail target retained.

### D0-EDGE-002

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_04`
- module: `D0.Edge.AlphaRamificationConstructive`
- theorem: `torus_ramification_puiseux_target`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Guardrail target retained.

### D0-HORIZON-JET-001

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `BOOK_07`
- module: `D0.Gravity.HorizonJetAndBaryonPole`
- theorem: `horizon_jet_observable_cert`
- cert: `vp_horizon_jet_axis_observable.py`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Finite observable cert; empirical jets passport. [was:HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD]

### D0-PUB-001

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `PUBLICATION`
- module: `D0.Publication.MonographStructure`
- theorem: `release_monograph_structure_audit`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Audit-only publication structure. [publication-structure meta; deferred; was:PUBLICATION-MONOGRAPH-STRUCTURE]

### D0-QUANT-MET-003

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `METROLOGY`
- module: `D0.Metrology.Phi2Flux`
- theorem: `phi2_purification_flux_target`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: φ^{-2} flux is sector hypothesis / prediction target. [was:CONDITIONAL-THEOREM-TARGET]

### D0-QUANT-MET-004

- type: `frontier`
- release_status: `PROOF-TARGET`
- domain: `frontier`
- book: `METROLOGY`
- module: `D0.Metrology.PhasonBragg`
- theorem: `phason_bragg_line_spectrum_target`
- cert: `none`
- assumptions: `none`
- scope: Frontier/proof-target row; not a core closure, certificate pass or empirical passport.
- notes: Analog residual Bragg frequencies f_m = m φ^{-2} mod 1 as metrology target. [was:METROLOGY-PREDICTION-TARGET]


## Domain: gauge_bridge

### D0-GAUGE-MATTER-001

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `gauge_bridge`
- book: `BOOK_02/04`
- module: `D0.Topology.BoundaryBoundary`
- theorem: `boundary_boundary_zero`
- cert: `vp_v1132_gauge_matter_ward_anomaly.py`
- assumptions: `ASSUMP-HST-EXTERNAL`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Boundary skeleton conditional on declared incidence pair.

### D0-GAUGE-YANG-MILLS-KILLING-POSITIVITY-001

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `gauge_bridge`
- book: `BOOK_08`
- module: `D0.Gauge.YangMillsKillingPositivity`
- theorem: `Gauge.discreteYangMillsAction_nonnegative_of_killing_nonpos`
- cert: `none`
- assumptions: `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Yang-Mills positivity follows from assumed negative semidefinite Killing form. [was:BRIDGE-ASSUMPTION]

### D0-FTHEORY-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `gauge_bridge`
- book: `BOOK_04`
- module: ``
- theorem: `none`
- cert: `vp_ftheory_lw2016_d0_filter.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] structural filter: dim, gauge rank, 3-generation chiral count, light exotics, terminal shell.

### D0-GAUGE-MATRIX-REP-TRANSFORM-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.MatrixRepGaugeTransform`
- theorem: `Gauge.gaugeTransformFinite_well_typed;Gauge.discreteMaurerCartan_well_typed;Gauge.matrixRepCurvature_well_typed;Gauge.gaugeTransformFinite_preserves_skew_of_orthogonal;Gauge.matrixRepCurvature_preserves_skew;Gauge.matrix_rep_yang_mills_action_nonnegative_of_skew`
- cert: `none`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Finite matrix-representation Yang-Mills layer is closed without asserting abstract graded Bianchi.

### D0-GAUGE-MATTER-002

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_02/04`
- module: `D0.Gauge.AnomalySums`
- theorem: `grav_U1_anomaly_sum;U1_cubic_anomaly_sum;SU2_SU2_U1_anomaly_sum;SU3_SU3_U1_anomaly_sum`
- cert: `vp_v1132_gauge_matter_ward_anomaly.py`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Exact rational one-generation anomaly sums.

### D0-GAUGE-NONABELIAN-DISCRETE-CURVATURE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_08`
- module: `D0.Gauge.NonAbelianDiscreteCurvature`
- theorem: `Gauge.spatialCommutator_preserves_skew;Gauge.spatialWedge_preserves_skew;Gauge.nonabelian_curvature_preserves_skew;Gauge.nonabelian_discrete_curvature_boundary`
- cert: `none`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Nonabelian curvature package preserves the skew sector after adding the wedge layer.

### D0-GAUGE-WILSON-LINK-COVARIANCE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.WilsonLinkGaugeCovariance`
- theorem: `Gauge.wilson_loop_covariance`
- cert: `none`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Finite gauge covariance is closed on group-valued Wilson links by path rewriting and inverse cancellation.

### D0-GRADED-BIANCHI-EXACT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.GradedBianchiIdentity`
- theorem: `Topology.graded_nilpotency;Topology.discrete_exact_bianchi;Topology.graded_bianchi_exact;Gauge.abelian_bianchi_exact;Gauge.graded_bianchi_exact`
- cert: `none`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Bianchi is exact on a graded incidence complex by boundary nilpotency.

### D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_04`
- module: `D0.Matter.HiggsScalarProjectorConstructive`
- theorem: `Matter.commutes_XZ_forces_scalar_matrix;Matter.nonzero_gauge_idempotent_eq_identity;Matter.rank1_scalar_projector_breaks_su2_gauge_compatibility;Matter.rank2_scalar_projector_exists;Matter.minimal_positive_scalar_projector_rank_two;Matter.minimal_positive_scalar_projector_unique;Matter.higgs_yukawa_core_promotion_valid`
- cert: `vp_higgs_scalar_projector_constructive.py`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Frozen rational SU2 doublet compatibility forces the unique nonzero idempotent scalar projector to be identity trace-rank two without external scalar constants.

### D0-MATTER-REP-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_04`
- module: `D0.Matter.GenerationMultiplicity`
- theorem: `Matter.rep_with_generations_card;Matter.generation_index_does_not_change_gauge_charge;Matter.matter_rep_generation_multiplicity_three`
- cert: `none`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Matter generation multiplicity is exactly three.

### D0-OPERATOR-GAUGE-CURVATURE-ORIGIN-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `gauge_bridge`
- book: `BOOK_08`
- module: `D0.Matter.GaugeCurvatureOrigin`
- theorem: `Algebra.commutator_self_zero;Algebra.commutator_skew_of_skew;Algebra.minus_trace_square_nonnegative;Matter.gauge_curvature_skew;Matter.abelian_curvature_annihilates_self_interaction;Matter.gauge_action_positive_from_origin;Bridge.gauge_curvature_origin_closed`
- cert: `none`
- assumptions: `none`
- scope: Gauge-sector statement; physical Yang-Mills interpretation remains bridge-scoped when assumptions appear.
- notes: Linear/abelian gauge curvature origin closed from archive commutators.

### D0-GAUGE-BIANCHI-GRADED-DEPRECATED-001

- type: `deprecated`
- release_status: `DEPRECATED`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.MatrixRepGaugeTransform`
- theorem: `Gauge.exact_bianchi_identity_replaced_by_graded_incidence_closure`
- cert: `none`
- assumptions: `none`
- scope: Deprecated or historical row; not a live promotion path.
- notes: Replaced by D0-GRADED-BIANCHI-EXACT-001; exact Bianchi is closed on the graded incidence complex.

### D0-GAUGE-BIANCHI-RESIDUAL-BOUNDARY-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `gauge_bridge`
- book: `BOOK_08`
- module: `D0.Gauge.BianchiResidual`
- theorem: `Gauge.residual_expands_by_definitions;Gauge.exact_residual_graph_anomaly_boundary`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Residual expansion is exact by definition; flat ungraded residual is NO-GO while graded incidence Bianchi is closed.

### D0-NO-GO-ABSTRACT-LIERING-FINITE-TRANSFORM-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.MatrixRepGaugeTransform`
- theorem: `Gauge.abstract_lieRing_finite_transform_requires_associative_representation`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Finite transform cannot be stated in bare abstract LieRing form without an associative matrix representation.

### D0-NO-GO-FLAT-TENSOR-NONABELIAN-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `gauge_bridge`
- book: `BOOK_08`
- module: `D0.Gauge.FlatTensorNoGo`
- theorem: `Gauge.flat_tensor_of_two_skew_is_symmetric;Gauge.naive_flat_tensor_nonabelian_boundary`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Naive flat tensor of two skew sectors is symmetric and leaves the skew/vector sector.

### D0-NO-GO-NAIVE-LOCAL-GAUGE-COVARIANCE-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.WilsonLinkGaugeCovariance`
- theorem: `Gauge.naive_local_gauge_covariance_counterexample_fin3`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Old naive flat matrix local transform has a concrete Fin 3 counterexample.

### D0-NO-GO-UNGRADED-BIANCHI-RESIDUAL-001

- type: `no-go`
- release_status: `NO-GO`
- domain: `gauge_bridge`
- book: `BOOK_05/06`
- module: `D0.Gauge.GradedBianchiIdentity`
- theorem: `Gauge.ungraded_bianchi_residual_counterexample_fin2`
- cert: `none`
- assumptions: `none`
- scope: Boundary/no-go row; prevents promotion of this route.
- notes: Flat ungraded commutator graph has a concrete Fin 2 residual counterexample.


## Domain: interpretation_spine

### D0-INTERPRETATION-SPINE-001

- type: `bridge`
- release_status: `CORE_BRIDGE_SPLIT`
- domain: `interpretation_spine`
- book: `BOOK_00/08`
- module: `D0.Bridge.InterpretationSpine`
- theorem: `Bridge.interpretation_package_keeps_core_dimensionless;Bridge.interpretation_package_does_not_mutate_core_shape;Bridge.si_readout_uses_single_external_calibration;Bridge.interpretation_spine_has_single_si_readout;Bridge.empirical_comparison_is_after_si_readout;Bridge.interpretation_package_rg_readout_coherent;Bridge.interpretation_package_spectral_action_readout_coherent;Bridge.interpretation_package_cosmology_shape_readout_coherent;Bridge.interpretation_package_gauge_readout_coherent;Bridge.interpretation_package_passports_external;Bridge.interpretation_spine_coherence_contract;Bridge.interpretation_package_from_existing_anchors_coherent`
- cert: `none`
- assumptions: `none`
- scope: Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package.
- notes: Unified dimensionless interpretation spine: RG/spectral/cosmology/gauge coherence is a typed readout package assembled from existing anchors and SI readout uses one ExternalSICalibration without mutating core shape.


## Domain: rg

### D0-LEAN-BRIDGE-001

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `rg`
- book: `Lean formalization`
- module: `D0.TheoremLedger.ReleaseStatus`
- theorem: `lean_bridge_assumptions_explicit`
- cert: `none`
- assumptions: `ASSUMP-HURWITZ-GOLDEN;ASSUMP-RG-SMOOTH-INTERP;ASSUMP-LORENTZ-MACRO;ASSUMP-SMOOTH-COVARIANCE;ASSUMP-SMOOTH-HEATTRACE;ASSUMP-HST-EXTERNAL`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Bridge assumptions isolated from core.

### D0-RG-001

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `rg`
- book: `D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE`
- module: `D0.Bridge.PhiDiscreteRG`
- theorem: `phi_rg_bridge_conditional`
- cert: `vp_v1145_operator_bridge_triple.py`
- assumptions: `ASSUMP-RG-SMOOTH-INTERP`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Scale algebra plus explicit smooth interpolation assumption.

### D0-ARCHIVE-LAPLACIAN-RG

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `rg`
- book: `BOOK_07`
- module: `D0.Geometry.ArchiveLaplacianRG`
- theorem: `archiveRGPhaseProjection_surjective;rg_curvature_zero_iff_exact_compatibility;rg_operator_curvature_zero_iff_renormalized_compatibility;rg_flat_curvature_zero_iff_exact_flat_compatibility;exact_projective_compatibility_fails`
- cert: `vp_archive_laplacian_rg_flow.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Nearest-neighbor phase Laplacian is not strictly projective; RG residual/curvature obstruction is tracked by scale-fit cert.


## Domain: si_calibration

### D0-BRIDGE-SI-CALIBRATION-BOUNDARY-001

- type: `bridge`
- release_status: `BRIDGE-CALIBRATION`
- domain: `si_calibration`
- book: `BOOK_08`
- module: `D0.Bridge.SICalibrationBoundary`
- theorem: `Bridge.c0_c2_scale_action_values_only;Bridge.c0_c2_cannot_alter_a0_a2_trace_shapes;Bridge.si_calibration_belongs_to_bridge_calibration_status;Bridge.si_calibration_cannot_promote_to_core_closed`
- cert: `vp_si_calibration_boundary.py`
- assumptions: `none`
- scope: Bridge-calibration row; SI or dimensional interpretation requires an explicit external calibration object.
- notes: c0/c2/G_N/H0 are bridge calibration symbols and cannot mutate core a0/a2 trace shapes.

### D0-BRIDGE-SI-CALIBRATION-CLOSURE-001

- type: `bridge`
- release_status: `BRIDGE-CALIBRATION`
- domain: `si_calibration`
- book: `BOOK_08`
- module: `D0.Bridge.SICalibrationClosure`
- theorem: `Bridge.core_traces_are_dimensionless;Bridge.calibration_changes_only_action_scaling;Bridge.calibration_changes_units_not_core_shape;Bridge.no_si_observable_without_external_calibration;Bridge.h0_gn_lambda_are_not_core_observables;Bridge.si_observables_require_external_calibration`
- cert: `none`
- assumptions: `none`
- scope: Bridge-calibration row; SI or dimensional interpretation requires an explicit external calibration object.
- notes: D0 core computes dimensionless traces; H0/GN/Lambda require an explicit ExternalSICalibration object.


## Domain: smooth_geometry

### D0-SMOOTH-001

- type: `bridge`
- release_status: `BRIDGE-ASSUMPTIONS-EXPLICIT`
- domain: `smooth_geometry`
- book: `D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE`
- module: `D0.Bridge.SmoothMetricBridge`
- theorem: `smooth_metric_bridge_conditional`
- cert: `vp_v1145_operator_bridge_triple.py`
- assumptions: `ASSUMP-SMOOTH-COVARIANCE;ASSUMP-SMOOTH-HEATTRACE`
- scope: Conditional bridge row; not a D0-core closure without listed assumptions.
- notes: Smooth geometry remains conditional.

### D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001

- type: `bridge`
- release_status: `CORE_BRIDGE_SPLIT`
- domain: `smooth_geometry`
- book: `BOOK_07`
- module: `D0.Gravity.MacroEinsteinInterface`
- theorem: `Gravity.spectral_a2_eh_bridge_closed;Gravity.finite_gravity_macro_constraints_closed;Gravity.macro_tension_einstein_hilbert_interface_closed;Gravity.finite_gravity_witness_yields_einstein_hilbert_interface`
- cert: `vp_macro_einstein_interface.py`
- assumptions: `none`
- scope: Core/bridge split row; the formal spine is proved while physical coherence remains an explicit package.
- notes: Finite witness yields symmetric divergence-free second-order TT-compatible macro interface; no continuum Einstein-Hilbert primitive is imported into core.

### D0-IM-003

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `smooth_geometry`
- book: `BOOK_06`
- module: `D0.IM.ContinuumFromFractalTick`
- theorem: `continuum_from_fractal_tick_cert`
- cert: `vp_continuum_from_fractal_tick.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Continuum envelope cert.

### D0-IM-005

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `smooth_geometry`
- book: `BOOK_01/02/06`
- module: `D0.IM.FractalContinuumAndWitnessHalting`
- theorem: `fractal_continuum_witness_halting_corrected`
- cert: `vp_continuum_from_fractal_tick.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Corrected continuum/witness halting layer.

### D0-IM-PRED-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `smooth_geometry`
- book: `BOOK_06/08`
- module: `D0.IM.FractalContinuumPredictions`
- theorem: `fractal_continuum_predictions_cert`
- cert: `vp_fractal_continuum_predictions.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Absolute/relative sign corrected. [was:FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED]

### D0-GEOM-SPECTRAL-ACTION-LADDER-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `smooth_geometry`
- book: `BOOK_08`
- module: `D0.Geometry.SpectralActionLadder`
- theorem: `spectral_action_a0_is_volume_proxy;spectral_action_a2_is_eh_proxy;higher_curvature_floor_bound_basic;trace_power_bound;a0_is_volume_proxy;a2_is_eh_proxy;higher_powers_floor_bounded`
- cert: `vp_spectral_action_eh_coefficient.py`
- assumptions: `none`
- scope: Finite/symbolic smooth-geometry proxy; continuum covariance requires declared bridge assumptions.
- notes: Finite spectral-action ladder and bounds; no continuum EH promotion.

### D0-TIME-2D-PISOT-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `smooth_geometry`
- book: `BOOK_06`
- module: `D0.Claims.Time2DPisot`
- theorem: `time_2d_pisot`
- cert: `vp_time_2d_pisot.py`
- assumptions: `none`
- scope: Finite/symbolic smooth-geometry proxy; continuum covariance requires declared bridge assumptions.
- notes: [8D Tier-1 forced] phi Pisot => deg Q(phi)=2 => time layer T^2; Adler-Weiss smooth partition. Lean L4 queued. Lean L5 CORE-FORMALIZED via D0.Claims.Time2DPisot (time_2d_pisot); native_decide/decide on the real finite content.


## Domain: spectral_action

### D0-ARCHIVE-HEATTRACE-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `spectral_action`
- book: `BOOK_07/08`
- module: `D0.Geometry.ArchiveHeatTrace`
- theorem: `heat_trace_positive;heat_trace_projection_compatible`
- cert: `vp_archive_heat_trace_weyl_dimension.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Lean structural heat trace skeleton plus Weyl dimension cert.

### D0-SOLENOID-GRAVITY-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `spectral_action`
- book: `BOOK_07`
- module: ``
- theorem: `none`
- cert: `vp_noncommutative_solenoid_gravity.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: Spectral triple heat trace and TT sector are compatible with noncommutative solenoid geometry. [Phase L honesty] Lean = EXTERNAL-GAP: K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30; the prior leanCoreProved theorem was a placeholder identity (stmt)(h):=h and was removed. Finite content stays cert-closed by the python_cert; the Lean structures-scaffold remains in the module for the Bridge index, not as a proof.

### D0-SPECTRAL-ACTION-ADMISS-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `spectral_action`
- book: `BOOK_07`
- module: `D0.Geometry.SpectralActionAdmissibility`
- theorem: `d0_archive_satisfies_structural_admissibility`
- cert: `vp_spectral_action_eh_coefficient.py;vp_spectral_action_expansion_stability.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: D0-side admissibility and coefficient/cutoff certs; external analytic theorem not internalized.

### D0-SPECTRAL-EINSTEIN-001

- type: `certificate`
- release_status: `CERT-CLOSED`
- domain: `spectral_action`
- book: `BOOK_07/08`
- module: ``
- theorem: `none`
- cert: `vp_spectral_action_einstein_tensor_response.py`
- assumptions: `none`
- scope: Certificate-bounded row; valid only for declared finite inputs and negative controls.
- notes: [8C orphan-harvest] finite spectral-action A2 response.

### D0-GEOM-HEAT-TRACE-A2-DECOMP-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `spectral_action`
- book: `BOOK_08`
- module: `D0.Geometry.HeatTraceA2Decomposition`
- theorem: `heat_trace_sq_exact_decomposition;discrete_eh_proxy_nonnegative;offdiag_double_count_guard;double_count_factor_guard`
- cert: `vp_spectral_action_eh_coefficient.py`
- assumptions: `none`
- scope: Finite spectral-action or heat-trace statement; no continuum Einstein-Hilbert promotion by default.
- notes: Heat trace exact decomposition with factor 1/2 and double-count guard.

### D0-GEOM-HIGHER-CURVATURE-FLOOR-BOUND-001

- type: `core`
- release_status: `CORE-FORMALIZED`
- domain: `spectral_action`
- book: `BOOK_08`
- module: `D0.Geometry.HigherCurvatureSuppression`
- theorem: `Geometry.HigherCurvatureSuppression.matrix_power_combinatorial_bound;Geometry.HigherCurvatureSuppression.conformal_laplacian_entry_bound;Geometry.HigherCurvatureSuppression.higher_curvature_suppression_by_floor`
- cert: `vp_spectral_action_eh_coefficient.py`
- assumptions: `none`
- scope: Finite spectral-action or heat-trace statement; no continuum Einstein-Hilbert promotion by default.
- notes: Higher curvature trace powers are bounded by the conformal density floor estimate.

