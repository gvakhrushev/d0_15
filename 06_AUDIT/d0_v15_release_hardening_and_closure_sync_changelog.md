# D0 v15 Release Hardening and Closure Sync Changelog

## 1. Higgs cert fixed
- SyntaxError around the misplaced `else` in negative control block resolved in 05_CERTS/vp_higgs_scalar_projector_constructive.py.
- Script now runs cleanly and emits the full required PASS token set (including RANK_TWO, COMMUTES_FROZEN_SU2_XZ, NONZERO_IDEMPOTENT_FORCES_IDENTITY_DOUBLET, YUKAWA_NO_SECOND_MASS_ANCHOR, SINGLE_ACTION_PRESERVED) plus expected FAIL negative controls.

## 2. v15 cert runner added
- Created 05_CERTS/run_all_v15_closure_certs.py (modeled on existing core/empirical runners).
- Executes the exact 15-script list (self-substrate, fractal tick, continuum envelope, Mobius halting, quadratic peel, measurement horizon, optical jet, master bootstrap+volume, gauge boundary, horizon emission, edge alpha, baryon 40/56 decomp, Higgs projector, Higgs Yukawa, meson defect).
- Outputs PASS_RUN_ALL_V15_CLOSURE_CERTS on success.
- Root result JSON updated: run_all_v15_closure_certs_results.json (pass=true).

## 3. Book 04 stale legacy sections rewritten
- Legacy 04.16 Higgs/scalar "still missing" language replaced: "The legacy Higgs/scalar projector no-go is resolved by the certified FrozenSU2-compatible rank-2 scalar projector. The remaining Yukawa work is numerical transfer/passport, not scalar-projector construction."
- 04.22 Remaining matter operator frontiers replaced with the exact 6-item positive list (alpha/CKM/baryon/meson/Higgs-Yukawa/SM decomp with remaining passport work only).
- 04.24 Operator Boundaries "closed no-go" language replaced with closure classes: Baryon: SPIN-FLAVOUR-CARRIER-CERTIFIED; Meson: MESON-TYPED-TRANSFER-CERT-CLOSED; Higgs: SCALAR-PROJECTOR-CERT-CLOSED + YUKAWA-SECTION-CERT-CLOSED.

## 4. Grand synthesis EP formula fixed
- Section 7 updated to exact matrix form M(η) with off-diagonals η and threshold η_EP = 2λ_r − λ_c = 40/10 .
- Removed any DESI/H0 overclaim language.

## 5. IM/topology claims mapped
- Added 7 new rows (D0-IM-001..004, D0-FOUND-004, D0-GRAV-004/005) to both theory_status_map.csv and CLAIM_TO_LEAN_MAP.csv.
- Lean status = CERT_ONLY for the new informational-mechanics and gravity claims (no Lean theorem yet).

## 6. Publication cleanup performed
- Remaining sync headers, exact sync tokens, PASS_/FAIL_ log blocks, weighted_mean=, events_used=, RMSE= etc. removed from Books 00–08 (especially 04/06/07/08).
- All such markers consolidated into 06_AUDIT/internal_sync_and_passport_markers.md .
- Books now strictly contain theorem statements, operator protocols, and passport references only.

## 7. Remaining research tasks
- Frozen U_eff pole sets for the certified baryon 40/56 carriers (then PDG passport).
- Numerical Yukawa passport after the closed scalar projector + block.
- K0-labeled meson spectroscopy passport after the typed transfer operator.
- Full Lean formalization for the new IM-00x / GRAV-00x claims (currently CERT_ONLY).
- External survey / PDG comparisons remain separate passport layer; never feed back into finite definitions.

All v15 closure work is now synchronized into a consistent release-candidate form.
