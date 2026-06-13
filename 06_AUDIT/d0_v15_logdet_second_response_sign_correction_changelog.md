# D0 v15 LogDet Second Response Sign Correction and Integration Changelog

## 1. Second derivative sign corrected
Integrated the correction from Researcher A deliverable. The log-det loop term L(V) = -d_τ log(1 - z + z exp(-κ V)) has L'(V) >0 but L''(V) <0 for the safe resolvent domain 0 < z < 1 (decelerating/saturating response, not accelerating). For z>1, L'' can be positive but only before finite resolvent breakdown at V_* = (1/κ) log(z/(z-1)).

Exact formulas derived symbolically in the new cert.

## 2. Safe-domain log-det response changed from accelerating to saturating/decelerating
- Statuses: LOGDET-FIRST-PRESSURE-RESPONSE-CERT-CLOSED and LOGDET-SECOND-RESPONSE-STABILITY-CERT-CLOSED.
- Description: positive first derivative, negative second derivative, bounded saturation for 0<z<1.
- Saturation limit: lim V→∞ L(V) = -d_τ log(1-z), L'(V)→0 for safe z.
- Domain: 1 - z + z exp(-κ V) >0 exactly; global safe 0<z<1.

## 3. Relative archive acceleration preserved
No contradiction: relative geometry R(V)=exp(κV)-1 has R''(V)>0 (accelerating). The bounded feedback loop response saturates while relative archive/active ratio accelerates. These are distinct observables. Core proves bounded pressure-response mechanism + accelerating relative geometry.

## 4. Book 08 patch corrected
Replaced any lingering wrong "positive first and second derivatives for 0<z<1" with the exact correction:
"The log-det loop pressure term has positive first derivative and negative second derivative in the safe resolvent domain 0<z<1. Thus the finite feedback response is positive but bounded and saturating. This does not contradict internal relative archive acceleration, because R(V)=e^{κV}-1 has R''(V)>0. The core proves a bounded pressure-response mechanism plus accelerating relative geometry; survey comparison remains passport-layer."

## 5. Cert tokens updated
New cert `05_CERTS/vp_logdet_second_response_and_stability.py` (SymPy exact for L', L'', signs, domain) emits:
- PASS_LOGDET_SECOND_DERIVATIVE_COMPUTED
- PASS_LOGDET_SECOND_RESPONSE_SIGN_CONDITION_DERIVED
- PASS_LOGDET_RESPONSE_DECELERATES_SAFE_DOMAIN
- PASS_LOGDET_RESPONSE_SATURATES_SAFE_DOMAIN
- PASS_RESOLVENT_STABILITY_DOMAIN_DERIVED
- PASS_RELATIVE_ACCELERATION_NOT_CONTRADICTED
- PASS_NO_SURVEY_FIT_CLAIM
+ exact FAIL controls (including confuse R accel with L accel, claim L'' positive for safe z, etc.).

## 6. Maps and status
- D0-IM-COSMO-004 added to theory_status_map.csv and CLAIM_TO_LEAN_MAP.csv with LOGDET-SECOND-RESPONSE-STABILITY-CERT-CLOSED (CERT_ONLY for Lean).

## 7. Runner updated
`05_CERTS/run_all_v15_closure_certs.py` now includes vp_logdet_second_response_and_stability.py. Full run emits PASS_RUN_ALL_V15_CLOSURE_CERTS.

All per executable cert evidence. No survey data. No H0 numerical claim. No wrong sign formulas. Previous strong logdet and relative certs remain consistent (first response positive, relative accel separate).
