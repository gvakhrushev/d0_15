# WRK-A4D-FORMALIZE-RESOLVED-ENERGY-VARIATION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Requires merged #189 and the stable resolved-carrier contract.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-resolved-energy-variation`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DResolvedAffineEnergy.lean`
Execution: `GitHub-first`

## Why delegated

This worker is dependency-gated because the resolved-energy first variation depends on the final carrier contract. Once stabilized, positivity, distance-to-subspace, zero-locus, covariance and separating Euler variations form a coherent finite-dimensional Lean package.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-RESOLVED-ENERGY-VARIATION` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize the resolved quadratic quotient energy and its first variation.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DResolvedAffineEnergy.lean`.

Targets:

- observer-positive inner product on edge cochains;
- orthogonal projection onto a supplied finite-dimensional incidence subspace;
- `E_I(b)=dist(b,I)^2`;
- zero-locus theorem `E_I=0 ↔ b∈I`;
- frame/full-affine invariance under transported `I`;
- projector/Grassmannian derivative under the selected constrained contract;
- separating-variation theorem sufficient to establish independence of the
  star and resolved-energy Euler channels if the research hypotheses are
  exactly met.

Do not formalize `d_P=2` until the physical quotient task proves it.
