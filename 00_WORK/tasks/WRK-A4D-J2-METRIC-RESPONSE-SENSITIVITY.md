# WRK-A4D-J2-METRIC-RESPONSE-SENSITIVITY

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-J2-UNIFORM-COUPLED-NORMAL-RESCUE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-j2-metric-response-sensitivity`  
Primary artifact: `02_REGISTRY/research/A4D_J2_METRIC_RESPONSE_SENSITIVITY.md`  
Execution: `GitHub-first`

## Why delegated

The coupled rescue theorem needs a quantitative bridge from connection-sheet distance to metric-response distance. This is a finite-stencil analytic estimate independent of the existence problem and is therefore suitable for a worker.

## Objective

For the unchanged naked star action in the declared near-flat analytic solder/link chart, certify a local bound for the raw metric partial Euler response under a connection perturbation

[
Amapsto A+Delta A.
]

Use the dimensionless link logarithm convention of #216. Track every explicit power of h and distinguish raw response from the final h^-2 normalized metric response.

Target a theorem of the form

[
|E_Q(Q_h,A+Delta A)-E_Q(Q_h,A)|
le
C h^{-p_{m raw}}|Delta A|
]

in a declared sum/Wiener norm on a compact analytic chart, followed by

[
|h^{-2}Delta E_Q|
le
C h^{-p'}|Delta A|.
]

If the finite formulas contain no negative powers of h before normalization, record the sharpest justified p' rather than assuming it.

## Required gates

1. Fix the exact finite response convention and normalization from the owner memos.
2. Differentiate the literal finite star metric Euler expression with respect to link coordinates.
3. Bound exponentials, inverse links, finite shifts, solder factors and chart Jacobians uniformly on one compact near-flat domain.
4. State the norm and show that lattice size / number of sites does not introduce an uncontrolled factor in the chosen sum norm.
5. Track h powers explicitly.
6. Prove the corollary:
   if (|Delta A_h|=O(h^infty)), then the normalized metric-response difference is O(h^infty) despite any fixed polynomial loss.
7. Include a negative control showing why a bound with an L-dependent hidden constant would be useless.

## Terminal

`J2-METRIC-RESPONSE-POLYNOMIAL-SENSITIVITY-CERTIFIED`

with the certified exponent p' and declared chart/norm.

## Boundaries

This worker does not prove existence of exact stationary sheets, UV isolation, locality, or the Einstein theorem. Do not edit #202. Do not add filters or invariants.

## GitHub execution contract

Start from fresh current `main` after this registration is merged. Run lifecycle start, open a Draft PR before substantive scientific edits, keep Git-visible task state synchronized with the PR lifecycle, self-retire only at a declared terminal, refresh against current `main` before Ready, and never self-merge.

## Chat handoff

Return PR, SHA, exact response convention, norm, p', compact-domain hypotheses, and validation commands.
