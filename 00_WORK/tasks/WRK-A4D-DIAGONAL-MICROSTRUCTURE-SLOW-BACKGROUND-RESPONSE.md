# WRK-A4D-DIAGONAL-MICROSTRUCTURE-SLOW-BACKGROUND-RESPONSE

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-diagonal-microstructure-slow-background-response`  
Primary artifact: `02_REGISTRY/research/A4D_DIAGONAL_MICROSTRUCTURE_SLOW_BACKGROUND_RESPONSE.md`  
Execution: `GitHub-first`

## Why delegated

PR #232 gives an exact curved joint vacuum of the naked star action at standard solder: the period-4 diagonal `Y`-microstructure satisfies `E_Q(η, K(z)) = 0`. That does not decide whether the same microstructure stays invisible in the metric response once the solder moves on a slow background. The owned smooth branch has raw metric response of order `h^2` after the single normalization `h^{-2}`. A mixed term of order `h` or `h^2` with a nonzero coefficient would be a structural obstruction to Einstein universality; a remainder `o(h^2)` would be the first response-decoupling input.

## Inputs

Use the exact family owned by `a4d_joint_palatini_exact_diagonal_vacuum_check.py` and the metric-partial convention of `A4D_J2_METRIC_RESPONSE_SENSITIVITY.md`. Do not reopen those proofs. Do not add an action channel, Holst term, `varphi`, torsion constraint, or selector.

## Objective

Place the period-4 microstructure on

```text
Q_h = eta + h q1 + h^2 q2 + ...
```

and compare

```text
Delta E_Q = E_Q(Q_h, K_micro) - E_Q(Q_h, K_sm).
```

Decide whether the first nonzero term is `o(h^2)` or a nonzero multiple of `h^2`, and record the actual leading order if it is neither.

## Forbidden shortcuts

No numerical root as an exact zero. No continuum Einstein claim in the positive direction. No replacement of the pointwise metric partial by a cell average unless that average is stated as a separate object.
