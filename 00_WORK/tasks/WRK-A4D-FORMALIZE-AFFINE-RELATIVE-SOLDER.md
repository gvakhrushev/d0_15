# WRK-A4D-FORMALIZE-AFFINE-RELATIVE-SOLDER

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Do not start until PR #184 is merged or a CONTROL review declares its exact
structural statements stable.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-affine-relative-solder`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DAffineRelativeSolderCompletion.lean`
Execution: `GitHub-first`

## Why delegated

This worker is dependency-gated because the relative-solder completion is still an unmerged research result. Once the science lands, the algebraic transform law, lambda selector and factor-through overquotient statement form a bounded Lean package with clear ownership.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-AFFINE-RELATIVE-SOLDER` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize observer-completed affine relative solder algebra.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DAffineRelativeSolderCompletion.lean`.

Targets:

- observer metric congruence under the owned Lorentz action;
- typed affine shift/link law;
- `ThetaHat^lambda = Theta - lambda b^T h_n`;
- exact transform
  [
  widehatTheta'^{(lambda)}
  =
  widehatTheta^{(lambda)}g^{-1}
  +(1-lambda)	au^T h_{n'};
  ]
- uniqueness of `lambda=1` under a nonzero translation witness;
- pure linear covariance at `lambda=1`;
- abstract matched-edge diagonal invariance of any functional factoring only
  through `ThetaHat`.

The 192-dimensional L=2 overquotient rank may remain a separate finite theorem
if full rank formalization is too expensive; do not assert it without proof.
