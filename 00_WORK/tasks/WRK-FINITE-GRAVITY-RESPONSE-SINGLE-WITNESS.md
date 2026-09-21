# WRK-FINITE-GRAVITY-RESPONSE-SINGLE-WITNESS

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
PLANNED

Do not start while another ordinary WORKER is active.

## Objective

Package the finite graph-Laplacian gravity response so that all basic finite predicates are explicitly properties of one stored response object
[
E_L:=2L.
]

This is preparation for the Lovelock natural-operator research route, not a continuum theorem.

## Preferred target

`03_FORMALIZATION/D0/Gravity/FiniteGravityResponseSingleWitness.lean`

Reuse `D0.VNext2.SpectralEinsteinResponse`; do not duplicate its algebra.

## Minimum theorem package

Define a structure or equivalent bundled theorem carrying one (L) and one (E_L=2L), then prove on that same (E_L):

1. response identity (E_L=2L);
2. symmetry if (L^T=L);
3. row-sum/archive-divergence zero if (L\mathbf1=0);
4. nontriviality (L\ne0\Rightarrow E_L\ne0);
5. every field/predicate references the same stored response object.

## Firewall

No claim of continuum tensor, Lorentz covariance, diffeomorphism naturality, second differential order, Bianchi identity, TT graviton, or Einstein tensor.

The point is only to eliminate the design defect where macro-signature propositions come from unrelated witnesses.

## Integration

Register only as formal support for the existing bridge claims unless CONTROL explicitly promotes a new claim.

Run target build, `lake build D0.All`, guards, generated-view checks and no-sorry scan.

Stop at REVIEW.
