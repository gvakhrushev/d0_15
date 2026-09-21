# EXP-ATORUS-DIRECT-LORENTZ-CONTINUUM-REALIZATION

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Test a strategic shortcut around the current proposition-only Rieffel/Connes continuum shells.

The archive role-phase carrier is already an explicit cyclic four-coordinate product:
[
X_N=\mathrm{Role}\to \mathrm{Fin}(N+2),
]
with a group shadow
[
(\mathbb Z/(N+2)\mathbb Z)^4.
]

Determine whether this can be realized directly as a refinement of a typed smooth four-torus/testbed with explicit point maps and a typed Lorentz metric structure.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/LORENTZ_CONTINUUM_TYPED_OWNER.md`
- `02_REGISTRY/research/EINSTEIN_ALLY_CHARACTERIZATION_BRIDGE.md`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseProductCarrier.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseGroup.lean`
- `03_FORMALIZATION/D0/Geometry/ArchivePhaseDistance.lean`
- `03_FORMALIZATION/D0/Geometry/ArchivePhaseEdgeMetricScale.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRoleProductLaplacian.lean`
- `03_FORMALIZATION/D0/Geometry/GHPGoldenCauchySequence.lean`
- archive two-limit / product-spectrum / Lorentz-signature owners and assumptions.

## Central idea to test, not assume

Define candidate point maps of the schematic form
[
\iota_N(x)_r = x(r)/(N+2) \pmod 1
]
into
[
T^4=(\mathbb R/\mathbb Z)^4.
]

Audit whether the owned finite metric/scaling is compatible with a concrete torus metric limit.

Then ask whether the finite role-sign data can support an actual smooth Lorentz metric on the same typed (T^4), for example a flat signature ((1,3)) test metric, without confusing a sign label with a smooth tensor field.

## Mandatory questions

1. Is a typed smooth (T^4) available in Mathlib / easily definable from existing quotient/manifold objects?
2. Can explicit (iota_N:X_N\to T^4) be written and shown mesh-dense / metric-consistent?
3. Can the finite normalized cyclic distance be compared to a torus product distance?
4. Can the 4D role-product scalar Laplacian be shown to approximate the flat torus Laplacian, at least modewise?
5. Can one construct a real smooth Lorentz metric (g_L) of signature ((1,3)) on that same (T^4)?
6. Does doing so require a new time-orientation or timelike-vector-field choice?
7. What global pathologies follow from periodic timelike direction (closed timelike curves / lack of global hyperbolicity), and do they matter for using (T^4) only as a local equation-class testbed?
8. Does a flat background metric suffice only to type the continuum target, while Lovelock still requires an operator on the full fixed-signature metric bundle?
9. Can this route bypass Rieffel/Connes for the typed target while leaving them as optional spectral cross-checks?

## Firewalls

A direct four-torus result is a continuum/testbed passport, not proof that physical spacetime globally equals (T^4).

A finite Role sign assignment is not by itself a Lorentz metric.

A fixed flat metric is not the Lovelock natural operator.

Do not erase the need for field/response reconstruction maps.

## Terminal verdict

Return one:

- `DIRECT-T4-TYPED-CONTINUUM-REACHED`
- `DIRECT-T4-METRIC-CONVERGENCE-BRIDGE-OPEN`
- `DIRECT-T4-LORENTZ-REALIZATION-BRIDGE-OPEN`
- `DIRECT-T4-PHYSICAL-GLOBAL-SPACETIME-NOGO-LOCAL-TESTBED-OK`
- `DIRECT-T4-ROUTE-NOT-CHEAPER`

## Deliverable

`MEMO_24_ATORUS_DIRECT_LORENTZ_CONTINUUM_REALIZATION.md`
