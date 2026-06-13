# D0 v15 Research Output Hardening and Status Integration Changelog

## Researcher outputs integrated
- D0_v15_EDGE_ALPHA_RAMIFICATION_FULL_CONSTRUCTION.md created with hardened statuses (EDGE-ALPHA-TRACE-CONSTRUCTION-TARGET, TORUS-RAMIFICATION-CONSTRUCTION-TARGET).
- D0_v15_BARYON_HORIZON_CONTINUUM_PREDICTIVE_LAYER.md created with status split (HORIZON-EMISSION-LAW-CLOSED, HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD, BARYON-ANONYMOUS-POLE-CERT-CLOSED, FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED, PDG PASSPORT-LAYER).

## Overclaiming statuses corrected
- Applied strict rules: only CERT-CLOSED when explicit finite objects + cert computes identities; OPERATOR-LAW-CLOSED for finite laws without empirical proof; CERT-SCAFFOLD-CLOSED for construction+negatives without full matrix proof; THEOREM-TARGET for declared targets relying on invariants; PASSPORT-LAYER for external data.

## Edge alpha seam/ramification gates added
- vp_edge_alpha_trace_constructive.py: explicit F_E (359), S_seam matrices; verifies PASS_EDGE_SECTOR_DIMENSION_359, PASS_SEAM_OPERATOR_CONSTRUCTED, PASS_EDGE_ALPHA_TRACE_359_PHI_MINUS_TWO_MINUS_PHI_MINUS_FIVE etc.
- vp_edge_alpha_ramification_puiseux.py: explicit spectral cover polynomials, branch roots for indices 4/3; verifies PASS_SPECTRAL_COVER_CONSTRUCTED, PASS_PUISEUX_RAMIFICATION_INDICES_1_4_AND_1_3 etc.
- Statuses remain TARGET until full (current certs provide construction but per rules hardened).

## Baryon image-basis pole cert added
- vp_baryon_40_56_anonymous_poles.py: constructs 216D, projectors, image bases B40/B56 via QR on eigh support, compresses Ueff = B^T PUP B on image only, extracts poles from 40D/56D images.
- Verifies all PASS_BARYON_IMAGE_BASIS_RANK_*, COMPRESSED_UEFF, ANONYMOUS_POLE_SET on image, NO_ZERO_PADDED, NO_PDG.
- FAILs for padded, PDG before frozen, etc.

## Horizon jet observable cert added
- vp_horizon_jet_axis_observable.py: explicit P/Q/U, F_Q_emit = Q U† P U Q (PSD verified), C_partial, Sigma mask, Pi_axis/transverse (orthogonal), J_axis/transverse observables.
- Verifies PASS_CONJUGATE_EMISSION_OPERATOR_PSD, PASS_*_PROJECTOR_DEFINED, PASS_AXIS_AND_TRANSVERSE_ORTHOGONAL, PASS_J_*_OBSERVABLE, PASS_COLLIMATION_INEQUALITY_ONLY_AFTER_PROJECTORS_FROZEN.

## Fractal continuum prediction sign corrected
- vp_fractal_continuum_predictions.py: explicit recurrence A_{n+1}=q A_n, B increment; verifies PASS_CONSTANT_LOG_GRADIENT..., PASS_ARCHIVE_SECOND_DIFFERENCE_NEGATIVE (Delta^2 B_n <0 absolute), PASS_CONTINUUM_ENVELOPE_MATCHES....
- Note on relative acceleration requiring separate observable.

## Runner updated
- run_all_v15_closure_certs.py now includes the 5 new/hardened certs + previous 18; executes all, produces PASS_RUN_ALL_V15_CLOSURE_CERTS and results JSON (pass=true).

## Book patches
- Book 04: coefficient-origin notes seam S_seam and target status; baryon section emphasizes image-basis only, no zero-pad/PDG in core.
- Book 07: jet section emphasizes closed conjugate law + inequality after frozen projectors.
- Book 08: continuum notes monotone decrease of absolute increments (Delta^2 <0) and requirement for normalized observable on relative claims.

## Maps updated
- theory_status_map.csv and CLAIM_TO_LEAN_MAP.csv appended with D0-EDGE-ALPHA-001 (TARGET), D0-EDGE-RAMIFICATION-001 (TARGET), D0-BARYON-POLES-001 (CERT-CLOSED), D0-HORIZON-JET-001 (SCAFFOLD), D0-IM-PRED-001 (CERT-CLOSED) + owners, certs, hardened statuses.

All per executable evidence; no overclaim.
