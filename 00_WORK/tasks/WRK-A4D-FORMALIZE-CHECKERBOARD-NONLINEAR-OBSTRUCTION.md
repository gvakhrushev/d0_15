# WRK-A4D-FORMALIZE-CHECKERBOARD-NONLINEAR-OBSTRUCTION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Start only after PR #187 reaches a stable reviewed terminal.

## Objective

Formalize the exact second-order obstruction for the three Lorentz-null
checkerboard physical quotient planes.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DCheckerboardNonlinearObstruction.lean`.

Target theorem shape:

for an exact basis `u,v` of each two-dimensional physical quotient-null
plane and real coefficients `a,b`, the projected quadratic source equals

[
-rac{32}{3}(a^2+b^2),
]

hence vanishes only for `a=b=0`.

Do not call the rank drop a wave mode or physical time effect.
Do not generalize beyond the reviewed finite sector.
