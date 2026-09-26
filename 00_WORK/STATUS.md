# Work Queue & Control Status

Runtime execution status lives in GitHub pull requests; the PR number is the execution ID.

## Repository Task Summary

| Class | PLANNED | IN_PROGRESS | BLOCKED | REVIEW | Total Tracked | WIP (Active / Limit) |
|---|---|---|---|---|---|---|
| CONTROL | 1 | 0 | 0 | 1 | 2 | 1 / 2 |
| EXPENSIVE | 0 | 0 | 0 | 0 | 0 | 0 / 3 |
| WORKER | 1 | 0 | 0 | 0 | 1 | 0 / 5 |
| **Total** | **2** | **0** | **0** | **1** | **3** | **1 / 10** |

## Repository Queue / Control Tasks

| ID | Class | State | Parent | Affected Claims |
|---|---|---|---|---|
| CTRL-NIGHTLY-FORMALIZATION-MAINTENANCE-W1 | CONTROL | PLANNED | ROOT | - |
| WRK-NIGHTLY-FORMALIZATION-DEBT-BURN-W1 | WORKER | PLANNED | CTRL-NIGHTLY-FORMALIZATION-MAINTENANCE-W1 | D0-TRACEABILITY-STATUS-TAXONOMY-001, D0-FINAL-BRIDGE-INDEX-001 |
| CTRL-A4D-STAR-DENSITY-LORENTZ-NONLINEAR-QUOTIENT | CONTROL | REVIEW | ROOT | - |

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
