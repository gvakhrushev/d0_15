# D0 v15 Executable Cert Repair and Final Status Sync Changelog

## 1. Edge alpha unitary dilation cert
- vp_edge_alpha_trace_constructive.py repaired: explicit F_E = phi^{-2} I_359 - phi^{-5} |w0><w0|, S=sqrt(F_E), C=sqrt(I-F_E), unitary U=[[C,S],[-S,C]], P_E block, Q_E = I-P_E.
- Verifies U†U=I, P_E U† Q_E U P_E = F_E (leakage recovers), Tr exact.
- All required PASS (including LEAKAGE_FROM_U, ALPHA_TRACE) and FAIL negative controls printed.
- Status: EDGE-ALPHA-TRACE-CERT-CLOSED.

## 2. Ramification cover cert
- vp_edge_alpha_ramification_puiseux.py: explicit D_mu(z,lambda)=(z-z_mu)^4 - lambda (degree 4), D_tau^3 (degree 3).
- Branch points and Puiseux 1/4,1/3 verified.
- Status: RAMIFICATION-COVER-CERT-CLOSED.
- RAMIFICATION-FROM-EDGE-UEFF remains THEOREM-TARGET (no companion U_eff,E spectral operator yet).

## 3. Real baryon 40/56 pole cert
- vp_baryon_40_56_anonymous_poles.py: real S3 symmetrizers (flavour base3, spin base2), Pi40= kron, Pi56=avg, image bases B via eigh+QR, isometry checks.
- Deterministic U (fixed integer QR, no random).
- Compress Ueff on image only (B.T PUP B), poles from 40x40/56x56.
- All PASS (IMAGE_RANK, ISOMETRY, COMPRESSED_UEFF, POLE_SET on image, NO_PADDED, NO_PDG) + FAILs.
- Status: BARYON-ANONYMOUS-POLE-CERT-CLOSED.

## 4. Horizon jet observable cert
- vp_horizon_jet_axis_observable.py: valid P+Q=I, PQ=0; deterministic U (QR of fixed); F_Q_emit PSD; explicit capacity/sat/axis/trans masks; orthogonal Pi; J_axis/J_trans computed.
- Prints PASS_COLLIMATION_INEQUALITY_FROZEN_TOY_MODEL (inequality holds in model) or the guard.
- Status: HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD (toy holds).

## 5. Fractal continuum cert
- vp_fractal_continuum_predictions.py: explicit recurrence, Delta B >0, monotone decrease, Delta^2 B_n <0 (absolute decelerate), total B increase, envelope match.
- All required PASS including SECOND_DIFFERENCE_NEGATIVE and note on relative observable.
- Status: FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED.

## 6. Theory status patches
- D0_v15_EDGE_ALPHA_RAMIFICATION_EXECUTABLE_PROOF.md : EDGE-ALPHA-TRACE-CERT-CLOSED, RAMIFICATION-COVER-CERT-CLOSED, RAMIFICATION-FROM-EDGE-UEFF-THEOREM-TARGET.
- D0_v15_BARYON_HORIZON_CONTINUUM_EXECUTABLE_LAYER.md : BARYON-ANONYMOUS-POLE-CERT-CLOSED, HORIZON-EMISSION-PSD-CERT-CLOSED, HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD, FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED.

## 7. Runner update
- run_all_v15_closure_certs.py updated with the 5 repaired/new certs (no duplicates).
- PASS_RUN_ALL_V15_CLOSURE_CERTS on full run.

## 8. Book patches
- Book 04: edge alpha now cert-closed via dilation/seam; ramification cover cert-closed, from-edge target; baryon poles image-basis only (no pad/PDG).
- Book 07: emission PSD cert-closed; jet observable finite/frozen after projectors; no empirical fit.
- Book 08: absolute increments decelerate (Delta^2<0), total increases; relative needs normalized observable; predictions cert-closed.

## 9. Changelog
This document.

All certs now real executable (no token-only, no random, explicit objects). Statuses reflect evidence. Runner green. Hygiene maintained.
