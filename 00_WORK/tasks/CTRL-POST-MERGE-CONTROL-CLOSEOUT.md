# CTRL-POST-MERGE-CONTROL-CLOSEOUT

Class: `CONTROL`  
Parent: `ROOT`

## Objective

Retire lifecycle rows whose execution PRs are already merged, while preserving
their durable scientific/formalization artifacts and keeping the GitHub-first
control plane truthful for cold-start agents.

## Scope

This closeout retires:

- `CTRL-NIGHTLY-FORMALIZATION-MAINTENANCE-W1`, whose worker #177 is merged and whose durable debt audit/non-growth CI guard is on main;
- `CTRL-A4D-STAR-DENSITY-LORENTZ-NONLINEAR-QUOTIENT`, whose execution PR #180 is merged.

No research result, theorem, certificate, Lean source, claim status, release
status, or BOOK/public scientific statement is changed.

## Exit condition

The two completed lifecycle rows and briefs are absent, this closeout task is
the only CONTROL row while its PR is under review, generated status views agree
with the manifest, and GitHub guards pass.
