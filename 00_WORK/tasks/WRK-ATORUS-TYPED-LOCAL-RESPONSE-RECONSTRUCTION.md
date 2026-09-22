# WRK-ATORUS-TYPED-LOCAL-RESPONSE-RECONSTRUCTION

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
PLANNED

Do not start while another ordinary WORKER is active.

## Objective

Implement the first actual typed fixed-(T^4) comparison layer from E-RECON.

This task owns only concrete geometry/sampling/reconstruction infrastructure.

It does **not** prove convergence, frame erasure, local-Diff naturality of a limit, covariant divergence, Lovelock, or the Einstein equation.

## Preferred branch

`work/atorus-typed-local-response-reconstruction`

## Required reading

- `02_REGISTRY/research/ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`
- `02_REGISTRY/research/ATORUS_FRAME_ERASURE_LOCAL_DIFF_NATURALITY.md`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseGroup.lean`

## Module split

Prefer focused modules:

- `D0.Bridge.T4TypedGeometry`
- `D0.Bridge.T4LocalRoleFrame`
- `D0.Bridge.T4ResponseReconstruction`

A fourth pullback module is acceptable if the file becomes too large.

## Typed smooth T4

Implement the fixed torus using pinned Mathlib's smooth `Circle`:

[
T4=(Circle\times Circle)\times(Circle\times Circle).
]

Provide the model aliases and compile checks for:

- `ChartedSpace`;
- `IsManifold ... ω T4`.

Do not use a proposition asserting that T4 is smooth.

## Pointwise tensor type

Represent a covariant 2-tensor at (x) concretely as:

`LinearMap.BilinForm ℝ (TangentSpace T4I x)`.

Define a small structure/subtype for symmetry with an actual bilinear-form field and proof of literal symmetry.

## Actual Lorentz metric type

Implement a D0 structure whose load-bearing field is an actual smooth dependent family

[
g_x:T_xT4\to_L(T_xT4\to_L\mathbb R)
]

with:

- symmetry;
- nondegeneracy;
- `sigPos = 1`;
- `sigNeg = 3`;
- smooth bundle-section field patterned after Mathlib's `Bundle.ContMDiffRiemannianMetric`.

Do not create:

`isLorentz : Prop`

as a semantic placeholder with no actual metric data.

## Local Role frame

Define:

[
RoleVec=Role\to\mathbb R.
]

Implement a local frame at (x:T4) carrying actual data:

- model→T4 `PartialDiffeomorph`;
- model center;
- proof center lies in source;
- proof chart(center)=x;
- `RoleVec ≃L[ℝ] T4E`.

Use explicit Role→four-coordinate correspondence.

## Radius-two stencil

Define offsets with coordinates (-2,-1,0,1,2), mesh

[
\varepsilon_N=1/(N+2),
]

stencil coordinates and a concrete `StencilAdmissible` predicate.

Also define the map into `ArchiveRolePhaseGroup N` and prove the clean periodic no-alias theorem:

[
N\ge3
\Longrightarrow
\text{radius-two offset map is injective}.
]

## Tangent frame

Using:

- `NormedSpace.fromTangentSpace`;
- `PartialDiffeomorph.isLocalDiffeomorphAt`;
- `mfderivToContinuousLinearEquiv`;

define the actual Role frame at every admissible stencil point and the center frame

[
RoleVec\simeq_L T_xT4.
]

## Finite metric sampling

Define:

[
RadiusTwoStencil
=
RadiusTwoOffset\to SymRoleTensor.
]

Then define the actual sampler:

[
sampleMetric(N,F,g)
]

whose components are:

[
g_{\psi(z_k)}
((d\psi)A e_a,(d\psi)A e_b).
]

Domain must be the full smooth Lorentz metric / local metric representative.

Do **not** define exact finite samples as a function of an ordinary 2-jet.

## Response reconstruction

Convert `SymRoleTensor` into a finite Role bilinear form and define:

[
reconstructResponse:
SymRoleTensor\to SymCov2At(x)
]

by pulling that bilinear form through the inverse center frame.

Prove the literal formula:

[
R_x^F(T)(v,w)
=
\sum_{a,b}
T_{ab}
(F_x^{-1}v)^a
(F_x^{-1}w)^b.
]

## Pullback support

At minimum implement:

- pointwise pullback of a symmetric covariant tensor by a local diffeomorphism;
- pulled local frame at the center;
- center-frame derivative compatibility;
- `reconstructResponse_pullback`.

If scope remains manageable, also close the full finite metric sampling square:

[
S_N^{\phi^*F}(\phi^*g)=S_N^F(g).
]

If that proof materially expands scope, stop after all objects plus reconstruction pullback are owned and leave sampling pullback as the next explicit worker.

## Firewalls

Do not claim:

- frame erasure;
- finite→continuum convergence;
- J² locality of a limit;
- local-Diff naturality of the descended limit;
- covariant divergence;
- Einstein tensor;
- Lovelock theorem.

These modules establish only actual finite/local typed comparison maps and metric-plus-frame covariance.

## Integration

Register as formal support for the active gravity continuum bridge.

Do not upgrade bridge claims to CORE unless their literal wording exactly matches the implemented finite/local statement.

Run:

- target builds;
- `lake build D0.All`;
- repository/work/generated guards;
- no `sorry` / `admit` / project `axiom` / `sorryAx`;
- `#print axioms` on capstones.

Move task to REVIEW, open PR and STOP.

Do not start the extra-ray worker or legacy planned workers.
