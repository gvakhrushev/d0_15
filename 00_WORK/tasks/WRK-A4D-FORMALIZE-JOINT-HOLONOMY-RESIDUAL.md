# WRK-A4D-FORMALIZE-JOINT-HOLONOMY-RESIDUAL

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Start only after #185 and the relevant terminal/completeness result from #186
are merged or CONTROL-approved.

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-joint-holonomy-residual`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DJointHolonomyResidual.lean`
Execution: `GitHub-first`

## Why delegated

This worker is dependency-gated on the two-loop residual research. After that result stabilizes, the polynomial adjugate/determinant residual and its affine covariance are algebraic and suitable for an isolated Lean module independent of later physical-quotient selection.

## GitHub execution contract

Start only from current `main`; run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-JOINT-HOLONOMY-RESIDUAL` before implementation, open a Draft PR before substantive edits, keep changes on the declared branch and primary artifact, obey dependency gates and collision fences, validate narrow targets first, refresh the branch against current main before Ready, self-retire the executable task when required by repository lifecycle, and never self-merge.

## Chat handoff

Return the PR number, final commit SHA, strongest exact theorem or formalization blocker, validation commands/results, and one smallest remaining dependency. A fresh agent must be able to continue from GitHub/task artifacts alone without relying on hidden chat context.


## Objective

Formalize the first surviving two-based-loop affine translational residual.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DJointHolonomyResidual.lean`.

Targets:

[
q_1^#=operatorname{adj}(I-P_1)t_1,
]

[
R_{2|1}=det(I-P_1)t_2-(I-P_2)q_1^#.
]

Prove:

- exact covariance `R' = g R` under affine conjugation;
- Lorentz/observer quadratic invariance;
- anchor/target reversal identities where stable;
- a typed exact nongauge edge witness if the finite carrier infrastructure
  supports it;
- no single-loop translation-sensitive continuous scalar theorem only at the
  exact level justified by the landed research result.

Do not claim full quotient completeness unless #186 closes it.
