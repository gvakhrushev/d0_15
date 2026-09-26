# WRK-A4D-JOINT-DIAGONAL-INVISIBLE-GERM

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-joint-diagonal-invisible-germ`  
Primary artifact: `02_REGISTRY/research/A4D_JOINT_DIAGONAL_INVISIBLE_GERM.md`  
Execution: `GitHub-first`

## Dependency

Consume the exact basis of the four-dimensional diagonal source-invisible sector from `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`. If that basis is not yet merged, stack explicitly on its registration/execution tip and state the dependency in the PR.

## Why delegated

After the linear census isolates the diagonal source-invisible four-space, the remaining calculation is a bounded reduced-germ problem on one owned resonance. It is suitable for a worker because it does not require the global smooth-background theorem; it only decides whether this specific joint vacuum germ is isolated or bifurcates.

## Objective

Determine the first nonzero **joint** zero-source reduced germ on the diagonal quarter-wave source-invisible sector.

The connection-only quartic/Puiseux analysis is not enough. The reduced system must include both:

[
E_K^{\rm red}=0,
qquad
E_Q^{\rm red}=0.
]

At (q=0), range-eliminate the regular connection variables consistently with the existing #216 convention.

## Required gates

1. Reproduce the diagonal kernel and exact invisible four-space.
2. Build the reduced action/response through the first order at which the metric partial is nonzero on that sector.
3. Compute the connection reduced Euler map and metric reduced map from the **same** reduced expansion.
4. Determine whether the joint zero at the origin is:
   - isolated and nondegenerate;
   - isolated but higher-order/degree-controlled;
   - or accompanied by a nontrivial formal/analytic curved joint-vacuum germ.
5. If isolated, give an exact local certificate (Jacobian, degree, Newton ball, or algebraic isolation).
6. If a branch survives, certify nonzero curvature and full joint equations to the order claimed; do not infer a full finite branch from a restricted gradient.
7. Compare with #225/#227:
   - #227 source-visible curve must be cut by (E_Q);
   - #225 slow-background splitting does not by itself decide this invisible sector.

## Preferred terminal

Positive control:

`J2-DIAGONAL-INVISIBLE-JOINT-ZERO-ISOLATED`

Negative:

`J2-DIAGONAL-INVISIBLE-JOINT-VACUUM-GERM-FOUND`

Partial terminals must identify the first missing coefficient/order.

## Forbidden

No new action channel, torsion constraint, (\varphi), or boundary selector. No all-orbit scan. No global Einstein claim.

## GitHub execution contract

Start from the required merged/stacked dependency. Open Draft before substantive edits, keep the dependency explicit, self-retire only at a theorem/no-go terminal, and never self-merge.

## Chat handoff

Return PR, SHA, the invisible basis used, first nonzero joint reduced equations, isolation/branch result, and exact certificate command.
