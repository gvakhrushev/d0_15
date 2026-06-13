# D0 v15 — LogDet Second Response Final Repair Changelog

## Scope

Final repair applied to the log-det second-response layer before release-candidate packaging.

## Changes

- Corrected safe-domain asymptotic limit:
  - `L(V) -> -d_tau log(1-z)` for `0 < z < 1`.
  - `L'(V) -> 0` for `0 < z < 1`.
- Preserved corrected sign:
  - `L'(V) > 0` in the safe domain.
  - `L''(V) < 0` in the safe domain.
- Updated interpretation:
  - finite log-det feedback response is positive, bounded and saturating;
  - relative archive geometry still accelerates via `R''(V)>0`;
  - no runaway feedback is claimed in the safe resolvent domain.
- Replaced the heavy edge-alpha cert with a fast exact-diagonal unitary-dilation cert.
- Replaced the log-det second-response cert with a symbolic final-repair cert.
- Parallelized `run_all_v15_closure_certs.py` with bounded workers and forced single-thread BLAS env to avoid release-runner timeouts.
- Cleaned malformed claim/status CSV rows and re-added v15 closure rows with valid `PYTHON_CERTIFIED`/`OPEN` statuses.
- Fixed the Book 08 malformed equation marker.

## Verified checks

- `PASS_RUN_ALL_V15_CLOSURE_CERTS`
- `PASS_RUN_ALL_CORE_CERTS`
- `PASS_RUN_ALL_BRIDGE_CERTS`
- `PASS: physical bridge discipline (160 claims checked)`
- `PASS_STANDARD_LANGUAGE_AUDIT_BUDGET flagged=117 max=125`
- `PASS` from `09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py`

## Remaining boundary

Survey cosmology remains passport-layer. No H0, DESI, SPARC, CMB, IceCube or LIGO numerical claim is promoted into core by this repair.
