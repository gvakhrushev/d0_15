# WRK-CERT-ARTIFACT-FRESHNESS

## Queue state
**REVIEW.** Rehomed under `CTRL-REVIEW-SEMANTIC-HARDENING`; CONTROL promotion is satisfied; implementation is ready for review. It is independent of the active gravity closure sequence.

Repository: https://github.com/gvakhrushev/d0_15

When promoted, start from a fresh then-current `origin/main` and treat tracked artifacts as immutable test inputs.

## Class
WORKER

## Parent
CTRL-REVIEW-SEMANTIC-HARDENING

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


- `D0-TYPED-ROLE-OPPOSITE-CUT-WELD-001`
- `D0-DIAGONAL-ROLE-HODGE-SYMMETRY-001`
- `D0-HODGE-GRADING-SYMMETRY-001`
- `D0-SPATIAL-HODGE-SHELL-OPERATOR-001`
- `D0-MOVING-GRADED-DIFFERENTIAL-001`
- `D0-PRIMAL-DUAL-MOVING-ACTION-001`
- `D0-PATH-HODGE-STABILIZER-001`
- `D0-MOVING-D-PARENT-WARD-001`
- `D0-RADIUS-ONE-WARD-KERNEL-001`
- `D0-CONSTITUTIVE-KERNEL-FAMILY-001`
- `D0-CONSTITUTIVE-HOLONOMY-COMPATIBILITY-001`
- `D0-AFFINE-CARTAN-PATH-CLOSURE-001`## Exit Condition
All three affected certificate paths detect stale tracked artifacts, registered cert execution leaves the tracked tree unchanged, and mutation controls prove stale evidence cannot remain green.

## Gravity/recent-core boundary

Include the fresh CORE owners from PRs #66–#70 in freshness/semantic regression coverage so stale artifacts cannot silently re-promote superseded gravity wording.

Fresh claim IDs are listed in manifest `affected_claims` for this task.

Boundary: this task must NOT require, invent, or refresh a certificate for BOOK `F_N`, and must not treat `spatialShellFluxCompression` as BOOK `F_N` evidence.

A reverse-star no-go artifact must not be interpreted as evidence against the located two-color `J`.


## Deterministic JSON freshness contract

Tracked JSON artifacts are compared semantically: structure and non-floating values are exact; float fields use fixed `rel_tol = abs_tol = 1e-12` to ignore only platform/runtime roundoff. This tolerance is many orders below the registered scientific decision thresholds.

Permanent regressions live in `tools/test_cert_artifact_freshness.py` and do not depend on transient active-work task files. Meaningful numerical mutations and stale/missing artifacts remain hard failures.

No BOOK `F_N` certificate is introduced.
