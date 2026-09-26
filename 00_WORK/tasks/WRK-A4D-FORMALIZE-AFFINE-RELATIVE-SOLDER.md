# WRK-A4D-FORMALIZE-AFFINE-RELATIVE-SOLDER

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Do not start until PR #184 is merged or a CONTROL review declares its exact
structural statements stable.

## Objective

Formalize observer-completed affine relative solder algebra.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DAffineRelativeSolderCompletion.lean`.

Targets:

- observer metric congruence under the owned Lorentz action;
- typed affine shift/link law;
- `ThetaHat^lambda = Theta - lambda b^T h_n`;
- exact transform
  [
  widehatTheta'^{(lambda)}
  =
  widehatTheta^{(lambda)}g^{-1}
  +(1-lambda)	au^T h_{n'};
  ]
- uniqueness of `lambda=1` under a nonzero translation witness;
- pure linear covariance at `lambda=1`;
- abstract matched-edge diagonal invariance of any functional factoring only
  through `ThetaHat`.

The 192-dimensional L=2 overquotient rank may remain a separate finite theorem
if full rank formalization is too expensive; do not assert it without proof.
