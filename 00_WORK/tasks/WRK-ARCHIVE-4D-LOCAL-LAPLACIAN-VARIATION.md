# WRK-ARCHIVE-4D-LOCAL-LAPLACIAN-VARIATION

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
IN_PROGRESS

## Objective

Truth-repair and actually prove the theorem currently advertised by
`D0-ARCHIVE-LOCAL-LAPLACIAN-VARIATION-ISOMORPHISM-001`.

The current file proves only dimension/count arithmetic. Replace that overclaim with a literal typed linear equivalence between nearest-neighbor undirected edge conductance variations and the corresponding symmetric row-sum-zero nearest-neighbor-supported Laplacian variations on the 4D role-product carrier.

## Baseline owners

Read:

- `03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseProductCarrier.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseGroup.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRoleProductLaplacian.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveProductLaplacian.lean`

Reuse existing adjacency/role-coordinate definitions where possible.

## Required typed objects

1. An undirected nearest-neighbor edge type or quotient on `ArchiveRolePhasePoint n`.
2. Conductance variations as a real vector space on those edges.
3. A declared subspace/structure of matrices satisfying:
   - symmetry;
   - row-sum zero;
   - off-diagonal support only on nearest-neighbor edges;
   - diagonal determined by the off-diagonal row sum.
4. A linear map
   [
   \delta w\mapsto\delta L.
   ]
5. An inverse/recovery map extracting each edge conductance from the corresponding off-diagonal matrix entry.

## Required theorems

At minimum:

- forward map is symmetric;
- forward map has zero row sums;
- forward map respects nearest-neighbor support;
- diagonal formula;
- recovery after forward map;
- forward after recovery on the declared local variation subspace;
- injectivity;
- surjectivity;
- an actual `LinearEquiv` or equivalent pair of inverse linear maps.

If the metric (L^2=(n+2)^2) scale is included, state it explicitly and ensure the inverse divides by that nonzero scale.

## Boundary

Do not claim:

- a gravity tensor;
- continuum locality;
- Lovelock antecedent;
- Bianchi identity;
- curvature;
- physical stress-energy.

This task only owns the local finite variation space needed by the next gravity-response seed.

## Registry

On success, restore `D0-ARCHIVE-LOCAL-LAPLACIAN-VARIATION-ISOMORPHISM-001` from PROOF-TARGET to honest Lean-owned status with theorem names matching the actual bijection.

Run:

- target build;
- `lake build D0.All`;
- repository/work/status/generated-view guards;
- no-sorry/admit/axiom scan.

Move task to REVIEW and stop. Do not advance any other worker.

## Preferred branch

`work/archive-4d-local-laplacian-variation`
