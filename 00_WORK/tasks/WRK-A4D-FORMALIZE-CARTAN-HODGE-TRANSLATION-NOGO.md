# WRK-A4D-FORMALIZE-CARTAN-HODGE-TRANSLATION-NOGO

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Science dependency

MERGED: PR #181.

## Objective

Formalize the exact scoped first-Cartan-Hodge translation-rescue obstruction
without broadening it into a universal affine no-go.

Primary new module:
`03_FORMALIZATION/D0/Geometry/A4DStarTranslationCartanHodgeNoGo.lean`.

## Minimum theorem set

- define the six-parameter first Cartan-Hodge correction coefficient space;
- encode the exact finite control matrix abstractly or with typed rational data;
- prove the homogeneous control matrix has rank 6 / trivial coefficient kernel;
- add the hostile inhomogeneous row and prove the augmented system inconsistent;
- expose the exact logical form:
  no coefficient vector in this declared six-parameter class solves all controls;
- state explicitly that higher-curvature/path, observer-dependent,
  non-polynomial and Euler-dependent laws remain outside scope.

Preferred proof style: exact rational linear algebra with an explicit invertible
6x6 minor plus one incompatible row, rather than an opaque computation oracle.

No theorem named as universal translation no-go.
