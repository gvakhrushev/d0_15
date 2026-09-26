# CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE

Class: `CONTROL`  
Parent: `ROOT`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `control/a4d-resolved-affine-program-wave`  
Execution: `GitHub-first`

## Objective

Integrate the current resolved-affine A4D frontier into the repository as a
durable research/formalization program.

This control task does not prove new science. It:

- records the strongest current frontier with source PR provenance;
- registers the next EXPENSIVE research tasks without exceeding active research WIP;
- registers Lean WORKER tasks with explicit science dependencies;
- launches only those Lean tasks whose scientific premises are already merged;
- retires stale completed control-plane rows;
- keeps moving research and formalization lanes collision-free.

## Scope discipline

Do not promote claims, releases or BOOK text.
Do not merge scientific EXPENSIVE PRs as part of this control task.
Do not formalize statements that remain only in unmerged research PRs except
behind an explicit dependency gate.
Do not self-merge execution PRs.

## Exit condition

The integration memo and task briefs are in the repository, stale control
tracking is retired, repository status views agree, and at least the two
formalization tasks based only on merged #180/#181 are launch-ready.
