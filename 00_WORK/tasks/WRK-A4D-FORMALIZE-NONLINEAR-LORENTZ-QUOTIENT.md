# WRK-A4D-FORMALIZE-NONLINEAR-LORENTZ-QUOTIENT

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Science dependency

MERGED: PR #180.

## Objective

Formalize the finite nonlinear site-dependent proper-Lorentz action and the
structural quotient facts used by the selected star density.

Primary new module:
`03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean`.

Reuse:
- `A4DRawSolderFrameAction`;
- `A4DSolderMetricCompletion`;
- existing finite link/path transport and exterior/Hodge modules.

## Minimum theorem set

1. typed sitewise link conjugation and raw-solder right action;
2. covariance of based plaquette curvature under the base-site frame;
3. covariance of complementary solder bivectors;
4. invariance of the relevant degree-two pairing / star density cell under a
   supplied proper-Lorentz frame;
5. invariance of site Gram data;
6. invariance of dressed links on nondegenerate solder;
7. structural theorem: an invertible solder has trivial point stabilizer under
   the right frame action;
8. explicit degenerate zero-solder/flat-link nontrivial stabilizer witness.

Do not hard-code the Python 96-cell check as an axiom. Prefer a general cell
invariance theorem from which the finite check is an instance.

No affine translations in this worker.
No claim/release/BOOK promotion.
