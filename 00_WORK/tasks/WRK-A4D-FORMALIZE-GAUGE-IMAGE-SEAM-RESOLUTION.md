# WRK-A4D-FORMALIZE-GAUGE-IMAGE-SEAM-RESOLUTION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Requires merged #188 and a stable terminal from
`EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION`.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-gauge-image-seam-resolution`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DGaugeImageResolution.lean`
Execution: `GitHub-first`

## Why delegated

This worker is intentionally delayed until the graph-closure research selects the intrinsic resolved carrier. Its role is to formalize the finite-dimensional range/incidence/quotient geometry after selection, rather than prematurely freezing one provisional memory interpretation.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-GAUGE-IMAGE-SEAM-RESOLUTION` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize the rank-changing gauge-image resolution.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DGaugeImageResolution.lean`.

Formalize abstract finite-dimensional statements first:

- `U = range D`;
- supplied incidence subspace `I` with `U ≤ I`;
- quotient memory `G = I/U`;
- dimension identities across rank changes;
- first-jet image-resolution theorem selected by research;
- graph-closure/incidence carrier and exceptional-fiber statements that have
  survived review.

Do not encode path-history semantics before the research task proves which
data are intrinsic.
