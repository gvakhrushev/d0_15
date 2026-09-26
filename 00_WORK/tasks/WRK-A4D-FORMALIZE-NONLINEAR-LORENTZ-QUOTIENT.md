# WRK-A4D-FORMALIZE-NONLINEAR-LORENTZ-QUOTIENT

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Science dependency

MERGED: PR #180.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-nonlinear-lorentz-quotient`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean`
Execution: `GitHub-first`

## Why delegated

This is a bounded formalization of already merged science from PR #180. The worker can strengthen the finite Lorentz layer independently by proving general cell covariance, quotient invariants and stabilizer facts without reopening affine translations or changing scientific scope.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-NONLINEAR-LORENTZ-QUOTIENT` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize the finite nonlinear site-dependent proper-Lorentz action and the
structural quotient facts used by the selected star density.

Primary new module:
`03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean`.

Reuse:
- `A4DRawSolderFrameAction`;
- `A4DSolderMetricCompletion`;
- existing finite link/path transport and exterior/Hodge modules.

## Minimum theorem set

1. typed sitewise link conjugation and raw-solder right action;
2. covariance of based plaquette curvature under the base-site frame;
3. covariance of complementary solder bivectors;
4. invariance of the relevant degree-two pairing / star density cell under a
   supplied proper-Lorentz frame;
5. invariance of site Gram data;
6. invariance of dressed links on nondegenerate solder;
7. structural theorem: an invertible solder has trivial point stabilizer under
   the right frame action;
8. explicit degenerate zero-solder/flat-link nontrivial stabilizer witness.

Do not hard-code the Python 96-cell check as an axiom. Prefer a general cell
invariance theorem from which the finite check is an instance.

No affine translations in this worker.
No claim/release/BOOK promotion.
