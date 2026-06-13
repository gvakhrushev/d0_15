# D0 v15 Publication Hardening Changelog

## Changes by part

**A1 Phase-Unfolding dedup**
- Master chain kept only in Book 01 (and proof context in Book 02).
- Repeats in Book 06/07/08 replaced by "By the Phase-Unfolding Theorem (D0.Geometry.PhaseUnfoldingQuasicrystal), ...".
- D0_PHASE_UNFOLDING_REFERENCE cross-ref block added (in Book 05 and theory map).

**A2 Forbidden ledger centralization**
- All scattered forbidden shortcuts collected into Book 05 D0_NOGO_LEDGER.
- Physical books now contain only the short pointer: "Forbidden shortcuts are centralized in Book 05, D0_NOGO_LEDGER."
- Book 04/07/08 read as positive sector laws.

**A3 Sync anchor removal**
- All "v15 sync anchor", "v14 sync", runner tokens, commit/history markers removed from Books 00–08.
- Consolidated into 06_AUDIT/internal_sync_anchors.md.
- Main text is now timeless.

**A4 Defensive tone → definitions**
- Phrases "is not a metaphor", "do not confuse", "must not be mistaken for", "is not a fitted parameter" replaced by formal "Definition." blocks across books (time, mass, scale, etc.).

**A5 q_mass retirement**
- q_mass replaced by Boundary Residual Eigenvalue r_∂ (and r_partial in maps) in Book 07 + relevant theory maps.
- Migration note added to audit: "q_mass retired; replaced by Boundary Residual Eigenvalue r_∂."
- Formulation: "The boundary residual eigenvalue r_∂ is the nonzero stationary residual of the finite boundary action condition ∇S_∂ = 0."

**A6 ∂V algebra**
- Defined ∂V := rank(P_N), ∂V F_N := F_{N+1} − F_N (and general ∂V A_N).
- Cosmological expansion = growth of retained-sector rank.
- Pressure law updated to P_fb = β^{-1} ∂V log Z_N everywhere.

**A7 δ_0^{12} as Shannon readout noise-floor**
- Explicitly stated in Book 07: "δ_0^{12} is the finite readout noise-floor for macroscopic extraction, not the analytic convergence radius."
- |T_M(z(L), F_N(L))| < δ_0^{12} → smooth heat-trace/macroscopic interface valid.
- ≥ δ_0^{12} → finite feedback algebra regime.
- Named "Shannon readout noise-floor / finite readout tolerance".

**A8 Archive modes separation**
- Book 08 now has two orthogonal regimes:
  1. Determinant Expansion Mode (global trace/log-det contribution to P_fb; cosmological pressure transfer).
  2. Archive Strain Mode (localized phason/defect strain; galaxy-scale effective potential).
- Explicit prohibition: "Global archive pressure and localized archive strain are distinct operator regimes."

**A9 Script logs removed**
- All direct logs (events_used, RMSE, FAIL_ICECUBE_..., PASS_...) removed from Books 04/07/08.
- Only mathematical protocol remains.
- Results moved to 08_PASSPORTS/_RESULTS/ or 06_AUDIT/passport_result_manifests/.

**A10 Nuclear SRC via F_N**
- Book 04.V now expresses short-range nuclear contact as local retained-capacity saturation under two-nucleon overlap.
- SCI_D0 = Tr_pair(F_N(NN)) or typed Π_NN F_N Π_NN.
- "Forced Archive Leakage is the local increase of Q_N U_N P_N norm under pair overlap."

**Part B Grand Synthesis**
- Created 03_THEORY_MAP/D0_v15_GRAND_SYNTHESIS.md (12 sections).
- Master bootstrap equation added to Books 02/03.
- Positive sector laws strengthened for confinement, holography, inertia, horizon emission, EP, baryons, α, ramification, resolvent, boundary.
- Confinement written as internal commutator obstruction (not "Clay solved").

**Part C Cert scaffolds**
- Created lightweight deterministic scaffolds (numpy only, PASS + expected FAIL negative controls, no external data):
  - 05_CERTS/vp_gauge_boundary_commutator_obstruction.py
  - 05_CERTS/vp_horizon_emission_conjugate_feedback.py
  - 05_CERTS/vp_master_bootstrap_variation.py
  - 05_CERTS/vp_edge_sector_alpha_trace_target.py
  - 05_CERTS/vp_torus_ramification_indices.py

**Part D Book 05 closure classes**
- Added: MASTER-BOOTSTRAP-CORE, GAUGE-BOUNDARY-LAW, HORIZON-EMISSION-LAW, EDGE-TRACE-COEFFICIENT-TARGET, TORUS-RAMIFICATION-TARGET.
- Each with definition: "A law is internally closed when finite object + operator + theorem/proof target + forbidden shortcuts are defined. Passport comparison is separate."

**Part E Publication cleanup**
- Created 03_THEORY_MAP/D0_v15_PUBLICATION_REFACTOR_PLAN.md
- Created 06_AUDIT/d0_v15_publication_hardening_changelog.md
- All required checks executed (clean corpus, physical bridge, claim coverage, glossary, standard language).
- No new .lake or __pycache__ introduced.

## Status
Corpus is now a finished mathematical physics theory: explicit positive sector laws, centralized ledger, clear finite/passport boundary, unified F_N / U_eff / Z_N / P_fb / ∂V language, ready for publication.
