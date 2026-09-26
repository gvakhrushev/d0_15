# WRK-A4D-FORMALIZE-GAUGE-IMAGE-SEAM-RESOLUTION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Requires merged #188 and a stable terminal from
`EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION`.

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
