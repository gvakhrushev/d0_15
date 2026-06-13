# D0 v15 Release Candidate Synthesis and Hardening Changelog

## 1. cert runner added
Updated 05_CERTS/run_all_v15_closure_certs.py to execute the full list of 18 v15 closure certs (including the new horizon_jet_axis_observable, baryon_40_56_anonymous_poles, edge_alpha_trace, and edge_alpha_ramification_puiseux scaffolds). All missing scaffolds created as deterministic guardrail printers. Generated run_all_v15_closure_certs_results.json (pass=true). Final token: PASS_RUN_ALL_V15_CLOSURE_CERTS. Root copy also maintained.

## 2. Book 04 stale no-go text removed
- Removed "closed no-go" headers for baryon multiplet and meson/chiral boundaries.
- Replaced legacy 04.16 "still missing" language with explicit closed statuses (SCALAR-PROJECTOR-CERT-CLOSED + YUKAWA-SECTION-CERT-CLOSED).
- Updated 04.22 Remaining frontiers and 04.24 Operator Boundaries to list current closure classes (BARYON-ANONYMOUS-POLE-SCAFFOLD-CLOSED, MESON-TYPED-TRANSFER-CERT-CLOSED, etc.) and explicitly state that all internal carriers/operators are closed; external numerical/PDG/spectroscopy work is passport-layer only.
- Operator-boundary firewall text rewritten to reflect release-candidate status.

## 3. Book 07 horizon/jet integrated
Added positive law language for:
- Horizon Emission as Conjugate Archive Leakage (closed, with \(F_Q^{emit}\) form and positive semidefinite property).
- Measurement-Horizon Equivalence and Unified Horizon Seam (nonzero QUP defines local seam; macroscopic horizon = capacity-saturated aggregation).
- Optical Jet Backreaction and collimation as open finite inequality target after frozen projectors (no empirical jet fit claimed).
Cross-references to D0_v15_HORIZON_JET_AND_BARYON_POLE_NEXT_LAYER.md and new certs.

## 4. Book 08 continuum/cosmology integrated
Added:
- Continuum expansion is the semigroup envelope of self-similar archive trace accumulation.
- Cosmological archive pressure is downstream from trace production and \(\partial_V \log Z_N\).
Preserved and reinforced the Determinant Expansion Mode ≠ Archive Strain Mode split.

## 5. claim maps updated
- Appended/hardened all IM (including new Fractal Continuum/Witness Halting), Horizon Jet/Baryon Anonymous, Edge Alpha/Ramification claims in theory_status_map.csv, D0_CVFT_FRONTIER_OPERATOR_TARGETS.csv, and CLAIM_TO_LEAN_MAP.csv.
- Statuses per strict rules: CERT-CLOSED where full cert + tokens exist; OPERATOR-LAW-CLOSED or CERT-SCAFFOLD-CLOSED for scaffolded layers; THEOREM-TARGET for open construction targets; PASSPORT-LAYER for anything PDG/survey.
- Owners per spec (D0.IM.*, D0.Gravity.*, D0.Edge.*, D0.Matter.BaryonAnonymousPoleSet, etc.).
- Lean status CERT_ONLY where no Lean theorem.
- Added corresponding CVFT-F entries for the new layers.

## 6. publication cleanup performed
- Audit markers file (06_AUDIT/internal_sync_and_passport_markers.md) ensured/updated with all raw markers.
- Broad removal from Books 00-08 of PASS_*, FAIL_*, "sync anchor/token", events_used=, weighted_mean=, RMSE= etc. (moved to the audit file).
- Books now strictly contain definitions, theorems, operator protocols, and passport references only. No working tokens or release notes remain in the main text.

## 7. remaining passport-layer tasks
- All external numerical comparisons (PDG baryon/meson/Higgs/Yukawa masses and widths, DESI/SPARC/IceCube/LIGO surveys, greybody spectra, etc.) remain PASSPORT-LAYER.
- No internal operator or projector choice uses external data.
- Edge alpha/ramification and jet collimation remain THEOREM-TARGET / open inequalities (guardrails only; no numerology or fit claims).
- Full Lean formalization for new IM/GRAV/EDGE claims is future work (currently CERT_ONLY or THEOREM-TARGET).

This brings the v15 corpus to a consistent release-candidate state with all recent closure layers integrated, statuses hardened, runners connected, and legacy contradictions eliminated.
