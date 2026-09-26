# WRK-A4D-FORMALIZE-CARTAN-HODGE-TRANSLATION-NOGO

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Science dependency

MERGED: PR #181.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-cartan-hodge-translation-nogo`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DStarTranslationCartanHodgeNoGo.lean`
Execution: `GitHub-first`

## Why delegated

This is a bounded formalization of the already merged PR #181 rank obstruction. The work is independently reviewable because the six-parameter ansatz and hostile exact rational inconsistency can be encoded without touching the active resolved-affine research architecture.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-CARTAN-HODGE-TRANSLATION-NOGO` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize the exact scoped first-Cartan-Hodge translation-rescue obstruction
without broadening it into a universal affine no-go.

Primary new module:
`03_FORMALIZATION/D0/Geometry/A4DStarTranslationCartanHodgeNoGo.lean`.

## Minimum theorem set

- define the six-parameter first Cartan-Hodge correction coefficient space;
- encode the exact finite control matrix abstractly or with typed rational data;
- prove the homogeneous control matrix has rank 6 / trivial coefficient kernel;
- add the hostile inhomogeneous row and prove the augmented system inconsistent;
- expose the exact logical form:
  no coefficient vector in this declared six-parameter class solves all controls;
- state explicitly that higher-curvature/path, observer-dependent,
  non-polynomial and Euler-dependent laws remain outside scope.

Preferred proof style: exact rational linear algebra with an explicit invertible
6x6 minor plus one incompatible row, rather than an opaque computation oracle.

No theorem named as universal translation no-go.
