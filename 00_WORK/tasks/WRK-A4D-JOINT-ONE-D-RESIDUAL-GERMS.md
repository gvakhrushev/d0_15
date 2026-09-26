# WRK-A4D-JOINT-ONE-D-RESIDUAL-GERMS

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-joint-one-d-residual-germs`  
Primary artifact: `02_REGISTRY/research/A4D_JOINT_ONE_D_RESIDUAL_GERMS.md`  
Execution: `GitHub-first`

## Why delegated

The existing L=4 rank inventory implies that, after genuine metric pressure, two singular rank classes retain only one connection-null direction each: ((22,23,1)) and ((20,23,3)). Once the exact basis is supplied by the joint linear-kernel worker, each class becomes a one-variable nonlinear joint normal-form problem. These are much cheaper than the diagonal four-dimensional sector and can be closed independently in parallel.

## Dependency

Consume the exact representative bases and orbit identification from `WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL`. If that execution is not yet merged, stack explicitly on its tip and record the dependency in the PR.

## Objective

For each singular orbit representative whose source-invisible connection space is exactly one-dimensional, compute the first nonzero reduced **joint** vacuum germ in an amplitude (u):

[
E_K^{\rm red}(u)=0,qquad E_Q^{\rm red}(u)=0.
]

Use the same range-elimination and conjugate-character conventions as #216/#208.

## Required gates

1. Reproduce the exact one-dimensional invisible basis for each relevant orbit class.
2. Range-eliminate all regular connection directions to the first order that can decide the joint zero set.
3. Compute the first nonzero scalar connection reduced equation and every independent reduced metric equation on the same amplitude.
4. Determine whether (u=0) is:
   - linearly cut by a metric component after reduction;
   - higher-order isolated;
   - or accompanied by a nontrivial formal/analytic joint-vacuum branch.
5. If isolated, provide an exact algebraic/degree/Newton certificate sufficient for a local Hölder/Puiseux rescue under (O(h^\infty)) smooth UV forcing.
6. If a branch survives, compute a curvature invariant and verify it is not a genuine gauge/flat direction before reporting a no-go.
7. Do not infer a full smooth continuum theorem from the two one-dimensional controls; hand the result to the EXPENSIVE owner.

## Preferred terminals

`J2-JOINT-ONE-D-RESIDUAL-ORBITS-ISOLATED`

or

`J2-JOINT-ONE-D-RESIDUAL-VACUUM-GERM-FOUND`.

A partial terminal must name the exact remaining coefficient/order.

## Boundaries

No diagonal four-dimensional work. No all-sheet (E_K) rescue. No torsion constraint, new action channel, (\varphi), boundary selector, or #202 edits.

## GitHub execution contract

Start from the required merged/stacked linear-kernel dependency. Open Draft before substantive edits, keep the dependency explicit, self-retire only at an exact terminal, refresh against current main before Ready, and never self-merge.

## Chat handoff

Return PR, SHA, both orbit representatives, exact one-dimensional bases, first nonzero joint reduced equations, isolation/branch verdict for each, and validation commands.
