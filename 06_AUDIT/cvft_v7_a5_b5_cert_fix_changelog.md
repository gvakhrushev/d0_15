# CVFT v7 A5/B5 Cert Fix Changelog

## A5 Accepted

The A5 audit is integrated as `CVFT_CERT_EXAMPLE_AUDIT_AND_FIX.md` and
`vp_cvft_refined_bounds_audit.py`.

## A4 Cert Examples Corrected

The 3x3 cyclic example is audited as rank one. The 4x4 full-rank crossing and
Householder boundary-dimension examples are the active deterministic examples.

## B5 Antisymmetrizer Fixed

The baryon cert now uses `(1/6) sum_sigma sgn(sigma) P_sigma` and checks
idempotence, self-adjointness and rank one.

## B5 Representation Check Made Real

The cert verifies all 36 S3 group-law products and `P_sigma^dagger=P_sigma^-1`
instead of hardcoding the representation token.

## New Cert Tokens

Added `PASS_AUDIT_3X3_CYCLIC_RANK_ONE`,
`PASS_FULL_RANK_CROSSING_EXAMPLE`,
`PASS_BOUNDARY_DIMENSION_LOWER_THAN_EDGE_COUNT`,
`PASS_S3_ANTISYMMETRIZER_IDEMPOTENT` and
`PASS_S3_ANTISYMMETRIZER_SELF_ADJOINT`.

## Book 04/05 Patch Summary

Book 04 keeps the 10D symmetric carrier neutral. Book 05 now forbids fake S3
representation tokens and the wrong antisymmetrizer formula.

## Remaining F3 Obligations

Spin/flavour labels, frozen pole set, mass/width assignment, GeV conversion,
QCD/EFT bridge and external PDG passport remain open.
