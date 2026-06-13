# D0 v15 Strong Log-Det and Monograph Integration Changelog

## 1. Strong log-det pressure coupling integrated
Created `03_THEORY_MAP/D0_v15_STRONG_LOGDET_PRESSURE_COUPLING.md` with corrected r(V) = 1 - e^{-κV} (not the wrong derivative), explicit clock-sector model, loop term, and positive derivative on the resolvent domain (0 < z < 1 safe). Status LOGDET-PRESSURE-COUPLING-CERT-CLOSED. Guardrail preserved: dimensionless internal response only; no H0/survey/FLRW claims.

## 2. r(V) derivative corrected
All prior documents, certs, and book text updated to use the correct ∂_V r(V) = κ e^{-κV} > 0 and the corresponding log-det derivative d_τ * [z κ e^{-κV} / (1 - z(1 - e^{-κV}))] > 0. Wrong formulas explicitly rejected in negative controls.

## 3. Book 08 pressure wording hardened
Replaced loose language with the exact strong statement: "D0 core proves internal relative archive acceleration and its positive log-det loop-pressure response. ... This is an internal dimensionless pressure-response theorem. Survey comparison remains passport-layer." Inserted the full equations for R(V), r(V), and the derivative.

## 4. Monograph structure added
Created `06_AUDIT/d0_v15_release_monograph_structure.md` with target chapter organization and hardened status table (risks noted as medium where full 359 construction or companion embedding is not yet complete; passport boundaries explicit).

## 5. Claim maps updated
Appended D0-IM-COSMO-001 (RELATIVE-ARCHIVE-ACCELERATION-CERT-CLOSED), D0-IM-COSMO-002 (RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED), D0-IM-COSMO-003 (LOGDET-PRESSURE-COUPLING-CERT-CLOSED), and D0-PUB-001 (PUBLICATION-MONOGRAPH-STRUCTURE) to both theory_status_map.csv and CLAIM_TO_LEAN_MAP.csv with correct owners, cert refs, and CERT_ONLY / AUDIT_ONLY notes.

## 6. Runner updated
`05_CERTS/run_all_v15_closure_certs.py` now includes vp_strong_logdet_pressure_coupling.py and the two pressure/relative certs. Full run emits PASS_RUN_ALL_V15_CLOSURE_CERTS.

## 7. Passport boundary preserved
Every new document, cert, book patch, and map entry explicitly states that survey data (DESI, SPARC, H0, IceCube, LIGO, etc.), numerical fits, and physical FLRW interpretations are PASSPORT-LAYER only. No core theorem selects, tunes, or claims agreement with external values. Forbidden shortcuts extended in Book 05 (wrong derivative, retuning z/c_R, confusing R_n with FLRW scale, etc.).

All per executable cert evidence. No survey data used. No H0 numeric claims. No wrong derivative formulas.
