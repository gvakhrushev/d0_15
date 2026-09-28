# EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Affected claim: `D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001` (research boundary only; no claim-status change)

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `exp/a4d-resonance-divisor-stratification`  
Primary artifact: `02_REGISTRY/research/A4D_RESONANCE_DIVISOR_STRATIFICATION.md`  
Execution: `GitHub-first`

## Why delegated

A finite exact stratification of the multivariable Laurent determinant and its kernel ranks is genuinely uncertain: the proposed phase-count law has an exact counterexample, while diagonal Smith data do not determine the off-diagonal divisor. The result needs symbolic factorization plus exact rank certificates on irreducible components and exceptional intersections, beyond a small deterministic control edit.

## Runtime / collision gate

At task start, use current `main`, verify this row is still `PLANNED`, and search open GitHub PRs for this exact task ID. If an execution already exists, continue it instead of creating another. Pin the launch SHA and the current merged heads/statuses of PRs #314 and #315. The expected inputs are #314's exact counterexample to the proposed phase-count formula and #315's diagonal determinant/Smith certificate. Do not recompute those outputs except for narrow consistency checks. This task concerns the holomorphic square symbol `A(z)` only; it is separate from PR #310's response/uniformity question.

## Objective

Classify the exact rank-drop locus of the owned holomorphic symbol

\[
 A(z):\quad z=(z_0,z_1,z_2,z_3)\in(\mathbb C^\times)^4,
 \qquad \det A(z)\in\mathbb Q[z_0^{\pm1},z_1^{\pm1},z_2^{\pm1},z_3^{\pm1}].
\]

Produce the determinant as an exact Laurent polynomial and factor it over `Q` up to Laurent units. For each irreducible codimension-one component, determine its generic kernel dimension and determinant multiplicity over that component's function field. Determine the exact equations and ranks on higher-codimension intersections wherever the rank drops further, sufficient to give a complete constructible rank/nullity stratification of the complex torus. State the stratum dimensions/codimensions and distinguish determinant multiplicity from matrix Smith exponents.

The phase-count formula proposed before PR #314 is already refuted and must not be revived. The goal is its exact replacement (or a proof that no formula depending only on those counts can classify the owned `A` rank), with the actual algebraic rank strata recorded.

## Required checks

1. Pin the exact source owner, coordinate ordering, and matrix convention for `A`; derive the Laurent determinant from that owner rather than importing an archive or a floating scan.
2. Verify the diagonal specialization
   \[
   \det A(z,z,z,z)=\frac{(z^2+1)^{12}}{16z^{12}}
   \]
   and the exact local diagonal data at `z=i` from #315.
3. Reproduce the #314 hostile point `(-1,-1,i,i)` over `Q(i)` with exact rank 22/nullity 2, and use it as a negative control against the rejected even-count rule.
4. Give executable exact certificates for factorization, generic component ranks, and every claimed exceptional rank-drop stratum. Include hostile points or ideal-membership checks that would fail if a component or rank stratum were omitted.
5. Report which results are global algebraic identities and which are only exact point controls. Floating scans may guide discovery but cannot certify the classification.

## Scope guard

Do not replace the full symbol by a phase-count rule, a diagonal-only restriction, numerical determinant samples, or coordinate-column pole histograms. Do not infer matrix kernel dimensions from `det A` multiplicities alone. Keep the holomorphic symbol `[A(z)|C(z)]` distinct from the physical conjugated slot `[A(z)|C(bar z)]`; this task proves no result about the latter. No metric response, residue, stationary-sheet continuation, continuum limit, physical carrier, Lean owner, claim/release-status promotion, or downstream-task creation is in scope.

## Exit condition

Close with `A4D-LAURENT-RESONANCE-STRATA-CLASSIFIED` only when the exact Laurent factorization and a reproducible exact certificate establish the generic rank on every irreducible divisor component and the complete higher-codimension rank/nullity strata of `A` on `(C^×)^4`, with the phase-count rule explicitly rejected. Otherwise keep the execution Draft/Blocked and name the first missing exact ideal, rank, or factorization step; do not present a finite sample table as completion.

## GitHub execution contract

Start from current `main`; run `python tools/task_lifecycle.py start EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION` as the first task-branch change; open a Draft PR before substantive research; write the memo and executable certificate directly into that PR; run exact certificates and repository guards; refresh against current `main`; run `python tools/task_lifecycle.py retire EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION` before Ready; mark the PR Ready with `Lifecycle: REVIEW`. CONTROL reviews and merges; do not self-merge.

## Chat handoff

Return the execution PR number, the exact factorization/rank-strata verdict, the certificate and guard results, and the single smallest remaining blocker if the task cannot close. Keep global algebraic claims separate from finite exact controls.
