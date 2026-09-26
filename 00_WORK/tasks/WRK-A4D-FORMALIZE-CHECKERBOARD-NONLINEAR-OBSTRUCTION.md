# WRK-A4D-FORMALIZE-CHECKERBOARD-NONLINEAR-OBSTRUCTION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Start only after PR #187 reaches a stable reviewed terminal.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-checkerboard-nonlinear-obstruction`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DCheckerboardNonlinearObstruction.lean`
Execution: `GitHub-first`

## Why delegated

This worker is dependency-gated on the reviewed terminal of PR #187. The exact second-order obstruction is a strong but finite scoped theorem; formalization should preserve its exact checkerboard scope and avoid physical wave/time interpretations.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-CHECKERBOARD-NONLINEAR-OBSTRUCTION` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize the exact second-order obstruction for the three Lorentz-null
checkerboard physical quotient planes.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DCheckerboardNonlinearObstruction.lean`.

Target theorem shape:

for an exact basis `u,v` of each two-dimensional physical quotient-null
plane and real coefficients `a,b`, the projected quadratic source equals

[
-rac{32}{3}(a^2+b^2),
]

hence vanishes only for `a=b=0`.

Do not call the rank drop a wave mode or physical time effect.
Do not generalize beyond the reviewed finite sector.
