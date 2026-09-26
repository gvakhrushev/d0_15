# WRK-A4D-FORMALIZE-JOINT-HOLONOMY-RESIDUAL

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Start only after #185 and the relevant terminal/completeness result from #186
are merged or CONTROL-approved.

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
