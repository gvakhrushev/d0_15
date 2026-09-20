# WRK-CERT-ARTIFACT-FRESHNESS

## Class
WORKER

## Objective
Eliminate the stale-artifact write-if-absent loophole in certificates, enforce strict deterministic freshness verification, and add mutation tests.

## Scope
1. Replace the non-verifying `if not ARTIFACT.exists(): ARTIFACT.write_text(expected)` pattern in:
   - `04_CERTIFICATES/vp_d0_redshift_drift_direct.py`
   - `04_CERTIFICATES/vp_feedback_partition_function.py`
   - `04_CERTIFICATES/vp_redshift_drift_expansion_coupled.py`
2. Implement exact deterministic comparison against tracked canonical artifacts (`assert tracked == computed`) without mutating the repository during test runs.
3. Direct transient/generated test outputs exclusively to `.build/` or designated runtime paths.
4. Add mutation controls proving that stale or modified tracked artifacts cause certificate execution to fail immediately.
5. **Boundary:** Do not alter underlying scientific calculations, physics formulas, statistical methods, or decision thresholds.

## Affected Claims
- `D0-DIRECT-REDSHIFT-DRIFT-PASSPORT-001`
- `D0-REDSHIFT-DRIFT-EXPANSION-COUPLED-PASSPORT-001`

## Exit Condition
All three affected certificate paths detect stale tracked artifacts, registered cert execution leaves the tracked tree unchanged, and mutation controls prove stale evidence cannot remain green.
