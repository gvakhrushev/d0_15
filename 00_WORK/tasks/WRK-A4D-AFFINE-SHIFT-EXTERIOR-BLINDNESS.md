# WRK-A4D-AFFINE-SHIFT-EXTERIOR-BLINDNESS

## Class

WORKER

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED on current `main` after merged PR #103 and PR #107.

Read completely:

- `03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean`;
- `02_REGISTRY/research/MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md`;
- `02_REGISTRY/research/MEMO_A4D_PATH_GROUPOID_CROSSED_MATTER_LIFT.md`.

## Objective

Lean-own the exact **affine-shift blindness boundary** of the current 16-state exterior path transport.

PR #103 deliberately lifts only the linear part of the owned affine Cartan path transport. The research packets use the fact that a pure translational affine loop can carry nonzero affine shift while the exterior matter transport is identity.

This task must make that boundary literal in Lean.

## Mandatory results

### 1. Dependence only on the linear path part

Prove that two affine path values with equal linear parts induce equal

`exteriorPathTransport`.

Prefer a theorem stated at the existing `covariantLin` / `affinePath` level rather than inventing a new representation.

### 2. Pure-translation blindness

Prove a scoped statement:

if the affine path value has linear part identity, then the current exterior path transport is identity on the 16-state Fock carrier.

This is a positive theorem about the existing representation, not a no-go for all matter representations.

### 3. Nonzero affine-shift witness

Construct or reuse an exact finite archive witness, preferably at `L=3`, where an affine loop/path has:

```text
linear part = I
affine shift ≠ 0
```

and prove that `exteriorPathTransport` nevertheless evaluates to identity.

The witness must use existing affine Cartan/path owners where possible.

### 4. Pair-of-paths comparison

If convenient, give two same-endpoint paths with the same linear transport but different affine shifts and prove the current exterior transport cannot distinguish them.

### 5. Capstone scope theorem

Package the exact boundary:

```text
current exterior path transport represents linear holonomy
but not affine translational holonomy.
```

Do not phrase this as impossibility of an enlarged, site-aware or path-expression matter response.

## Truth firewall

Do not claim:

- no affine-sensitive matter representation exists;
- translations cannot act on any enlarged carrier;
- the missing site-aware link is impossible;
- the 16-state carrier must be abandoned;
- stress, Einstein, physical time, golden/phi, or constitutive second-jet closure.

The result only classifies the already-owned PR #103 exterior path transport.

## Suggested module

`D0/Geometry/A4DAffineShiftExteriorBlindness.lean`

## Validation

Narrow build first, then one final D0 build and normal repository guards.
No `sorry`, no new axiom.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-AFFINE-SHIFT-EXTERIOR-BLINDNESS`;
3. open Draft PR immediately before source edits;
4. implement and validate;
5. before Ready self-retire the task;
6. set `Lifecycle: REVIEW`;
7. Ready for review;
8. do not self-merge.

## Exit condition

The current 16-state exterior path transport is Lean-proved to depend only on the linear affine path part, with an exact nonzero-translation witness showing that pure affine translational holonomy is invisible to this representation, without promoting the boundary to a universal no-go.
