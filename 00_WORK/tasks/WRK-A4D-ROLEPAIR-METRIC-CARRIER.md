# WRK-A4D-ROLEPAIR-METRIC-CARRIER

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
IN_PROGRESS

## Objective

Machine-own the exact minimal finite metric carrier classified by E-METPROV.

This task owns carrier algebra only. It does not own a gravity response, gauge principle, continuum metric or Einstein interpretation.

## Preferred branch

`work/a4d-rolepair-metric-carrier`

## Required reading

- `02_REGISTRY/research/A4D_FINITE_METRIC_PROVENANCE_CARRIER.md`
- `D0.Geometry.A4DSymRoleCentralDifference`
- archive role-phase group/carrier
- local Laplacian variation owner
- cubical cell/cochain carrier.

## Required constructions

1. Define/reuse the six unordered distinct Role-pair labels.
2. Prove their cardinality is exactly 6.
3. Define local axis data
   [
   X_N\to(Role\to\mathbb R)
   ]
   and local cross-Role data
   [
   X_N\to(RolePair\to\mathbb R).
   ]
4. Define the 4+6 metric-probe carrier.
5. Build an actual linear equivalence with `LocalSymRoleField N` (or a linearized vector-space wrapper of the same data):
   - diagonal entries from axis variables;
   - off-diagonal entries from unordered pair variables;
   - explicit inverse.
6. Embed the current directional/axis sector as the diagonal locus.
7. Prove the local missing dimension/codimension is six per site; if finrank infrastructure is clean, global codimension (6(N+2)^4).
8. Give a pure off-diagonal witness not in the axis image.
9. Formalize an exterior negative control showing oriented/exterior pair amplitudes cannot be definitionally identified with symmetric pair data.

## Optional

For (N\ge1), prove the positive-step axis-edge labeling/bijection needed to identify undirected nearest-neighbour edges with site×Role.

Keep any conductance-to-metric scale explicit.

## Firewalls

Do not claim:

- physical metric provenance;
- Lorentz signature;
- gauge;
- curvature;
- Einstein tensor;
- action selection;
- continuum realization.

## Integration

Run target build, `lake build D0.All`, guards/generated views, no-sorry scan and capstone `#print axioms`.

Move task to REVIEW, open PR and STOP.
