# Work Queue & Control Status

Runtime execution status lives in GitHub pull requests; the PR number is the execution ID.

## Repository Task Summary

| Class | PLANNED | IN_PROGRESS | BLOCKED | REVIEW | Total Tracked | WIP (Active / Limit) |
|---|---|---|---|---|---|---|
| CONTROL | 0 | 2 | 0 | 0 | 2 | 2 / 2 |
| EXPENSIVE | 0 | 0 | 1 | 0 | 1 | 1 / 3 |
| WORKER | 4 | 0 | 0 | 0 | 4 | 0 / 5 |
| **Total** | **4** | **2** | **1** | **0** | **7** | **3 / 10** |

## Repository Queue / Control Tasks

| ID | Class | State | Parent | Affected Claims |
|---|---|---|---|---|
| CTRL-GRAVITY-DYNAMICS-CLOSURE | CONTROL | IN_PROGRESS | ROOT | D0-HODGE-LINKS-001 |
| CTRL-REVIEW-SEMANTIC-HARDENING | CONTROL | IN_PROGRESS | ROOT | - |
| EXP-A4D-FINITE-GRADED-COFRAME-DRESSING | EXPENSIVE | BLOCKED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-HODGE-LINKS-001 |
| WRK-A4D-CONDITIONAL-SOURCED-DIAGONAL-TRANSPORT | WORKER | PLANNED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-AFFINE-CARTAN-PATH-CLOSURE-001 |
| WRK-A4D-REGULAR-AE-PASSPORT | WORKER | PLANNED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-AFFINE-CARTAN-PATH-CLOSURE-001 |
| WRK-A4D-ACTIVE-SPAN-EXTENSION-INDEPENDENCE | WORKER | PLANNED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-AFFINE-CARTAN-PATH-CLOSURE-001 |
| WRK-A4D-LABELLED-ENDPOINT-CLASSICAL-DESCENT | WORKER | PLANNED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-AFFINE-CARTAN-PATH-CLOSURE-001 |

## Registry Health & Metrics

- **Assumptions**: 31
- **Legacy Scaffolds Remaining**: 12

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
