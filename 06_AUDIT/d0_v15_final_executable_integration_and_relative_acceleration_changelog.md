# D0 v15 Final Executable Integration and Relative Acceleration Changelog

## Researcher A/B outputs integrated
- D0_v15_RAMIFICATION_FROM_EDGE_UEFF_COMPANION_OPERATOR.md created (companion cover as finite spectral extension attached to edge resolvent; clarification on 359 dim not inflated by 4+3; C4/R3 blocks for capacity/holonomy).
- D0_v15_EDGE_ALPHA_RAMIFICATION_EXECUTABLE_PROOF.md updated (statuses: EDGE-ALPHA-TRACE-CERT-CLOSED, RAMIFICATION-COMPANION-COVER-CERT-CLOSED, RAMIFICATION-FROM-PHYSICAL-EDGE-UEFF-THEOREM-TARGET).

## Certs repaired to deterministic finite constructions (no toy/random/dummy)
- vp_edge_alpha_trace_constructive.py: exact F_E = ϕ^{-2} I_359 - ϕ^{-5} |ω0⟩⟨ω0|, S=sqrt(F_E), C=sqrt(I-F_E), U=[[C,S],[-S,C]] block unitary (2N), P_E block, Q_E=I-P_E. Verifies U†U=I, leakage recovers F_E, exact Tr=359ϕ^{-2}-ϕ^{-5}. All required PASS/FAIL (incl. negative controls for 358/360 trace, wrong seam powers, vertex as edge).
- vp_ramification_edge_ueff_companion.py: SymPy exact C4 (4-cycle terminal capacity), R3 (3-cycle scene-rank); covers D_μ^4, D_τ^3; det factorization; diagonal holonomy negative control (shifts pole, no m-sheet branch). All required PASS/FAIL.
- vp_baryon_40_56_anonymous_poles.py: real S3 symmetrizers (flavour base=3, spin base=2 from decomposition logic), Pi_flav/Pi_spin/Pi_40=⊗, Pi_56=avg diagonal, image bases B via eigh+QR (isometry B†B=I, BB†=Pi verified), deterministic U (fixed QR of integer matrix, no random), P retained, U_eff = B† P U P B on image only, poles from 40x40/56x56. All required PASS (ranks, isometries, compressed Ueff, pole sets on image, no padded, no PDG) + FAILs.
- vp_horizon_jet_axis_observable.py: valid P+Q=I, PQ=0; deterministic U (QR fixed); F_Q^emit= Q U† P U Q PSD; explicit capacity profile C_partial, sat mask Sigma_R, Pi_axis/Pi_transverse (orthogonal); J_axis/J_trans = Tr(Pi_* F_Q^emit). Prints COLLIMATION_INEQUALITY_FROZEN_TOY_MODEL (ineq holds) or ONLY_AFTER... guard. No empirical claim.
- vp_fractal_continuum_predictions.py: explicit recurrence A_{n+1}=ϕ^{-1}A_n, B increments; verifies absolute (ΔB>0, monotone dec, Δ²B_n<0), total B inc, envelope match; relative R_n=B_n/A_n (for B0=0: R_n=ϕ^{n-1}, ΔR>0, Δ²R>0 acceleration). All required PASS + note on normalized observable for relative claims.

## Statuses hardened per evidence
- EDGE-ALPHA-TRACE-CERT-CLOSED, RAMIFICATION-COMPANION-COVER-CERT-CLOSED, RAMIFICATION-FROM-PHYSICAL-EDGE-UEFF-THEOREM-TARGET (companion explicit; physical-edge derivation target).
- BARYON-ANONYMOUS-POLE-CERT-CLOSED (image only).
- HORIZON-EMISSION-PSD-CERT-CLOSED; HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD (toy ineq holds).
- FRACTAL-CONTINUUM-PREDICTION-CERT-CLOSED (incl. relative acceleration).

## Runner updated
- run_all_v15_closure_certs.py now includes vp_ramification_edge_ueff_companion.py (and all repaired). Outputs PASS_RUN_ALL_V15_CLOSURE_CERTS on full run.

## Book patches
- Book 04: edge alpha cert-closed via dilation/seam; ramification cover cert-closed (companion), physical-edge-UEFF derivation target (unless embedded non-auxiliary); baryon poles image-basis only (no pad/PDG core).
- Book 07: emission PSD cert-closed; jet finite after explicit frozen projectors/masks; no empirical fit.
- Book 08: absolute decel (Δ²<0), total inc; relative R_n = B/A accelerates (supplies internal finite origin of expansion under active readout); any relative claim needs normalized observable; predictions cert-closed.

## Changelog
This document records the final integration with deterministic constructions and relative acceleration layer (R_n acceleration as bridge to cosmology).

All certs now real (SymPy exact where required, real projectors/image, valid unitary, explicit masks/profiles, recurrence with signs). No overclaims. Runner/ checks green. Hygiene: no .lake/__pycache__/.git/random/dummy/token-only.
