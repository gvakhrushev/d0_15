# WRK-A4D-GOLDEN-RG-DEFECT-INTERFACE

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED.

Primary durable packet:

`02_REGISTRY/research/MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD.md`.

Required existing owners:

- `D0.Geometry.ArchiveLaplacianRG`;
- `D0.Geometry.ArchiveRolePhaseCarrier`;
- `D0.Geometry.FibonacciBratteliRefinement`;
- `D0.Spectral.CanonicalRefinementScaleFlow`;
- `D0.Geometry.ArchiveFlatProductBondingNoGo`;
- `D0.Geometry.ArchiveTwoLimitSeparation`.

## Objective

Lean-own the **defect-bearing scalar renormalization interface** identified by PR #86, while preserving the terminal

`GOLDEN-SCALE-WELD-OWNED-CARRIER-WELD-MISSING`.

The worker must make the typed positive statement stronger without inventing a Tower-C -> Tower-B carrier map.

Target terminal:

`GOLDEN-RG-DEFECT-INTERFACE-LEAN-OWNED-CARRIER-WELD-MISSING`.

## Mandatory package

### 1. `A4DGoldenRolePhaseRGDefect.lean`

Use the literal current types.

#### Role-phase coordinate bridge

Prove explicitly that the coordinatewise Role-phase projection is built from the same one-dimensional map used by the RG prototype:

```text
archiveRolePhaseProjection n x r
  = archiveRGPhaseProjection n (x r)
```

and prove its natural equivariance under Role permutation/precomposition.

This is a typed coordinate bridge, not a 4D operator-intertwining theorem.

#### Scalar-only golden assignment

Define a scalar assignment from the already-owned Perron scale flow, with a separate Bratteli-depth parameter `k`, for example

```text
goldenScaleProbe k = Lambda (k+1) / Lambda k
```

and prove

```text
goldenScaleProbe k = phi
```

and level-independence.

The Bratteli index `k` and Role-phase period `n` must remain separate arguments.

#### Defect-bearing residual

Define the golden scalar probe of the existing RG residual, schematically:

```text
goldenRGResidual n k P
  := rgOperatorResidual n P (goldenScaleProbe k)
```

and prove, using the existing owner,

```text
goldenRGResidual n k P = 0
  ↔ RenormalizedProjectiveCompatibility n P phi
```

after rewriting the scale probe.

Also expose the generic scalar-assignment version if it improves the API:

```text
sigma : C -> Real
R_N(sigma c)
```

but keep `C` abstract: the scalar assignment transports no Tower-C state or carrier.

#### Operator versus energy residual

Keep separate:

- `rgOperatorResidual` / entrywise compatibility;
- `rgCurvatureCorrection` / energy compatibility.

Package both zero-residual equivalences without identifying them.

#### Negative controls

Re-export or package, with exact scope:

- `exact_projective_compatibility_fails` for the literal nearest-neighbor prototype;
- record/profinite vs Role-phase bonding separation;
- the first-step 6-versus-16 fiber mismatch.

Do **not** derive a stronger “golden residual never vanishes” theorem unless it is actually proved. The existing exact-projective failure and the entrywise renormalized residual are distinct statements.

### 2. `A4DGoldenCarrierWeldBoundary.lean`

Provide a compact theorem-level firewall combining existing owners:

- Tower A record bonding is not Tower B Role-phase bonding;
- Tower C golden scale data are scalar/trace data internal to that tower;
- the current formal interface contains no Fock/`J`/`D_H`/`H(e)` transport theorem.

Formalize only positive type separation or existing no-go owners.
Do not attempt to prove “no canonical map exists” merely from absence in the repository.

If an abstract interface structure is useful, it may package:

```text
(B_N, p_N, L_N^B, pb, sigma_C)
```

as supplied data, but the worker must not instantiate a canonical Tower-C -> Tower-B carrier map.

## Exact capstones

At minimum:

- coordinate bridge theorem;
- Role-permutation equivariance of coordinatewise projection;
- `goldenScaleProbe_eq_phi`;
- scale-probe level independence;
- golden operator residual zero iff renormalized entrywise compatibility;
- generic scalar-assignment specialization theorem if introduced;
- energy residual zero iff exact energy compatibility;
- exact-projective negative control remains separate;
- record/Role-phase bonding separation capstone.

Add `#print axioms` or repository-equivalent checks for the principal new capstones.

## Non-overlap

This worker must not edit or claim ownership of:

- the fixed-N path-word constitutive law `C_N`;
- observer/frame/path transport modules;
- located `J` naturality;
- corrected `D_H` inter-level intertwining;
- `H(e)` inter-level transport;
- Tower-C state/word/measure pushforward.

Those remain missing exactly as PR #86 states.

## Truth firewall

Keep distinct:

- Bratteli depth `k`;
- Role-phase period `n/N`;
- record/profinite depth;
- history tick;
- observer;
- physical time.

Do not identify a scalar equality `c = phi` with a carrier weld.

Do not promote scalar Laplacian residuals to CAR/`D_H` intertwiners.

## Lean throughput / lifecycle

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-GOLDEN-RG-DEFECT-INTERFACE`;
3. immediately open Draft PR before Lean edits;
4. narrow builds during iteration;
5. one final `python tools/lean_task_build.py final`;
6. repository validators + no-sorry + generated views;
7. self-retire task in the same PR;
8. Ready / `Lifecycle: REVIEW`;
9. do not self-merge.

No `lake clean`, `sorry`, `sorryAx`, or new axioms.

## Exit condition

The scalar golden/RG defect interface and its typed Role-phase coordinate bridge are Lean-owned while the missing carrier/operator weld remains explicit and unclaimed.
