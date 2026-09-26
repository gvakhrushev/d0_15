# EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

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
