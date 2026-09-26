# EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `exp/a4d-resolved-affine-physical-quotient`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PHYSICAL_QUOTIENT.md`
Execution: `GitHub-first`

## Why delegated

This is an expensive nonlinear quotient classification that must combine the selected resolved carrier, affine gauge-image strata, Euler-channel independence and stabilizer/reconstruction tests. It cannot be delegated as routine Lean work because d_P remains a research conclusion, not an implementation detail.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

After the resolved carrier is selected, compute the true full-affine physical
quotient and decide the fate of the two-channel action family

[
S_{m trial}=alpha S_{widehatstar}+eta E_{mathcal I}.
]

## Dependencies

Requires a stable terminal from
`EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION` and the relevant landed results
from #184/#185/#186/#188/#189.

## Required gates

- distinguish actual node-gauge tangent `im D_L` from limiting incidence
  directions stored in `mathcal I_*`;
- prove quotient coordinates/reconstruction on generic and seam strata;
- classify stabilizers;
- compute `d_A`, the coefficient-to-Euler map and `d_E`;
- test whether both Euler channels remain nontrivial after the true quotient;
- state `d_P` only if quotient survival is proved;
- verify generic 192-dimensional and flat 196-dimensional quotient charts are
  reconciled by the resolved structure rather than identified by fiat.

## Desired terminal

A scoped exact statement for
`d_{P,aff,res}`, including whether the two-channel family remains
two-dimensional physically.

No continuum/Einstein/diffeomorphism interpretation.
