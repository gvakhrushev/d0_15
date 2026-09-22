# EXP-A4D-FINITE-METRIC-PROVENANCE-CARRIER

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Attack the exact missing left-hand provenance arrow identified by E-PROV.

Construct or terminally refute an actual map
[
\Theta_N:
\mathcal M_N^{D0}
\to
LocalSymRoleField(N)
]
from an owned finite D0 geometry/metric state into the ten-component sitewise symmetric Role tensor field used by the Einstein-consistent stencil.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/ATORUS_NORMAL_SAMPLING_PROVENANCE_GAUGE.md`
- `02_REGISTRY/research/ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`
- `02_REGISTRY/research/A4D_LOCAL_GRAVITY_RESPONSE_SEED.md`
- `03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRoleProductLaplacian.lean`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`
- seam/product metric owners and the cross-role curvature no-go;
- finite A1/response/action owners that could plausibly define a metric state.

## Main audit

For every plausible owned finite metric carrier, determine:

1. actual type;
2. local degrees of freedom per site;
3. whether it supplies all ten symmetric Role-pair components;
4. locality;
5. refinement index;
6. action/Euler response;
7. gauge/reparametrization structure;
8. map into `LocalSymRoleField N`;
9. compatibility with the Lorentz response ray;
10. compatibility with the normal metric sampling passport.

## Conductance/Laplacian route

Start with the strongest owned result:
[
EdgeConductanceVariation(N)
\simeq
LocalLaplacianVariation(N).
]

Determine whether one can naturally and injectively recover a general local
[
h_{ab}(x)=h_{ba}(x)
]
from these variations.

Do not confuse:

- site-site matrix symmetry;
- local Role-index symmetry.

If the scalar edge carrier lacks the six cross-Role components, prove the strongest exact dimension/representation obstruction available.

## Possible enlarged existing carriers

Audit whether a richer already-owned object can supply the missing tensor slots without adding arbitrary new data:

- role-pair conductances;
- local Hessian/edge-pair variations;
- product-cell/plaquette variables;
- scene tensor sectors transported into the role-phase tower;
- existing spin-2 carriers;
- action Hessians with declared local tensor indices.

If none exists, classify the minimal enlarged finite metric carrier needed.

## Response factorization

A positive result must do more than map into the test field.

It should identify an actual D0 finite response
[
\mathcal E_N^{D0}
]
and prove or reduce to a theorem:
[
\mathcal E_N^{D0}(m)
=
E_{\eta,N}(\Theta_Nm)
]
up to an explicitly classified scale/convention.

If only the Euclidean ray is currently formalized, separate that fact from the Lorentz response required by E-NJET.

## Gauge provenance

Audit every owned finite symmetry that could generate
[
K_N\xi=D_a\xi_b+D_b\xi_a.
]

Test:

- lattice relabelling;
- local coordinate changes;
- translations;
- Role permutations;
- A1 Stueckelberg symmetry;
- local tick reparametrization;
- additive compensator actions.

A positive theorem must provide an actual action on the finite metric state whose tangent or exact affine action produces `symmetricRoleGradient`.

Do not infer local gauge from the mere existence of (K_N).

## Normal realization compatibility

If (\Theta_N) exists, formulate the weakest theorem sufficient to compose with E-NJET:
[
R_x^FE_{\eta,N}
(\Theta_N(m_N[g,F])-S_N^{g,F}g)(0)
\to0.
]

This theorem may remain downstream, but its type must be clear.

## Terminal verdict

Return exactly one:

- `FINITE-METRIC-PROVENANCE-CARRIER-REACHED`
- `CONDUCTANCE-CARRIER-CROSSROLE-NOGO`
- `FINITE-METRIC-CARRIER-ENLARGEMENT-REQUIRED`
- `FINITE-METRIC-RESPONSE-FACTORIZATION-MISSING`
- `FINITE-METRIC-GAUGE-PROVENANCE-MISSING`

## Deliverable

`MEMO_33_A4D_FINITE_METRIC_PROVENANCE_CARRIER.md`
