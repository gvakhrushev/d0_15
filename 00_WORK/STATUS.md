# Work Queue & Control Status

Runtime execution status lives in GitHub pull requests; the PR number is the execution ID.

## Repository Task Summary

| Class | PLANNED | IN_PROGRESS | BLOCKED | REVIEW | Total Tracked | WIP (Active / Limit) |
|---|---|---|---|---|---|---|
| CONTROL | 0 | 2 | 0 | 0 | 2 | 2 / 2 |
| EXPENSIVE | 0 | 1 | 1 | 0 | 2 | 2 / 3 |
| WORKER | 1 | 0 | 0 | 0 | 1 | 0 / 5 |
| **Total** | **1** | **3** | **1** | **0** | **5** | **4 / 10** |

## Repository Queue / Control Tasks

| ID | Class | State | Parent | Affected Claims |
|---|---|---|---|---|
| CTRL-GRAVITY-DYNAMICS-CLOSURE | CONTROL | IN_PROGRESS | ROOT | D0-HODGE-LINKS-001 |
| CTRL-REVIEW-SEMANTIC-HARDENING | CONTROL | IN_PROGRESS | ROOT | - |
| WRK-A4D-NILPOTENT-AFFINE-LIFT-GRADING-BOUNDARY | WORKER | PLANNED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-HODGE-LINKS-001 |
| EXP-A4D-SOLDER-CARTAN-EDGE-MISMATCH | EXPENSIVE | IN_PROGRESS | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-HODGE-LINKS-001 |
| EXP-A4D-FINITE-GRADED-COFRAME-DRESSING | EXPENSIVE | BLOCKED | CTRL-GRAVITY-DYNAMICS-CLOSURE | D0-HODGE-LINKS-001 |

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
