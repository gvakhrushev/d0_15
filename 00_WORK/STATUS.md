# Work Queue & Control Status

Runtime execution status lives in GitHub pull requests; the PR number is the execution ID.

## Repository Task Summary

| Class | PLANNED | IN_PROGRESS | BLOCKED | REVIEW | Total Tracked | WIP (Active / Limit) |
|---|---|---|---|---|---|---|
| CONTROL | 1 | 0 | 0 | 0 | 1 | 0 / 2 |
| EXPENSIVE | 1 | 0 | 0 | 0 | 1 | 0 / 3 |
| WORKER | 0 | 1 | 0 | 0 | 1 | 1 / 5 |
| **Total** | **2** | **1** | **0** | **0** | **3** | **1 / 10** |

## Repository Queue / Control Tasks

| ID | Class | State | Parent | Affected Claims |
|---|---|---|---|---|
| CTRL-A4D-VARIATIONAL-FRONTIER | CONTROL | PLANNED | ROOT | - |
| EXP-A4D-ROLE-BIVECTOR-INSERTION-UNIQUENESS | EXPENSIVE | PLANNED | CTRL-A4D-VARIATIONAL-FRONTIER | D0-AFFINE-CARTAN-PATH-CLOSURE-001, D0-LOCATED-PRIMAL-DUAL-CELL-001, D0-LOCATED-PRIMAL-DUAL-STAR-001, D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001 |
| WRK-A4D-AFFINE-CURVATURE-CERT | WORKER | IN_PROGRESS | CTRL-A4D-VARIATIONAL-FRONTIER | D0-AFFINE-CARTAN-PATH-CLOSURE-001 |

## Registry Health & Metrics

- **Assumptions**: 31
- **Legacy Scaffolds Remaining**: 0

### Claims by Exact `release_status`

| Exact `release_status` | Count |
|---|---|
| BRIDGE-ASSUMPTIONS-EXPLICIT | 30 |
| BRIDGE-CALIBRATION | 3 |
| CERT-CLOSED | 193 |
| CORE-FORMALIZED | 390 |
| CORE_BRIDGE_SPLIT | 17 |
| DEPRECATED | 5 |
| EMPIRICAL-PASSPORT | 13 |
| EXTERNAL-BACKGROUND | 1 |
| FORMALISM | 4 |
| NO-GO | 133 |
| NO_GO_PROVED | 6 |
| PASSPORT-CLOSED | 20 |
| PROOF-TARGET | 74 |
| **Total** | **889** |
