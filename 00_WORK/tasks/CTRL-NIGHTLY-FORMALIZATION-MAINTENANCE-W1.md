# CTRL-NIGHTLY-FORMALIZATION-MAINTENANCE-W1

Class: `CONTROL`  
Parent: `ROOT`

## Objective

Own one isolated maintenance wave whose only purpose is to reduce accumulated
formalization/engineering debt after the recent A4D research advance, without
changing scientific meaning.

The executable child is:

`WRK-NIGHTLY-FORMALIZATION-DEBT-BURN-W1`

## Control boundary

This control lane does not perform new research, select new physics, change
claim strength, or compete with active A4D star-density / variation /
formalization work.

The child may refactor implementation/proof structure while preserving public
theorem statements and registered scientific semantics.

## Exit condition

The child WORKER PR is merged or terminally rejected with an explicit blocker,
all overlap with concurrently active scientific/formalization PRs has been
avoided, and the main branch is green with the maintenance audit installed.
