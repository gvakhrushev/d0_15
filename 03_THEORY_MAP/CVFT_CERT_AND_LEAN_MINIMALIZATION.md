# CVFT Cert and Lean Minimalization

Status: deterministic finite certificates first; Lean targets are deferred under
`09_LEAN_FORMALIZATION/docs/LEAN_DEFERRED_RUN_POLICY.md`.

## Corrected Example A: Full-Rank Crossing

Use `N=4`,

```math
P=diag(1,1,0,0),\qquad Q=I-P.
```

Let `U` swap `e1 <-> e3` and `e2 <-> e4`. Then `QUP` has rank `2` and

```math
F=(QUP)^\dagger(QUP)=P,\qquad rank(F)=rank(QUP)=2,\qquad rho(F)=1.
```

This replaces the flawed 3x3 example, which has rank `1`, not rank `2`.

## Corrected Example B: Boundary Dimension Below Edge Count

Use `N=4`,

```math
P=diag(1,1,1,0),\qquad Q=I-P.
```

Let `U` be the Householder reflection with vector `(1,1,1,1)/2`.  Then the
three retained coordinates leak through one traced boundary coordinate:

```text
edge_count_like = 3
dim(B_partial) = 1
rank(QUP)=1
rank(F)=1
```

The rank is controlled by boundary-channel dimension, not raw edge count.

## Corrected Log-Det Bound

All bounds use

```math
a=|z|rho(F)<1.
```

With the analytic branch at `z=0`,

```math
|-\log det(I-zF)| <= rank(F)[-\log(1-a)] <= rank(F) a/(1-a).
```

Do not use `z/(1-z)` as a theorem statement. For complex `z` it is complex and
cannot upper-bound a real magnitude; for `z=1.5`, `rho(F)=0.5`, the refined
condition has `a=0.75<1` while `z/(1-z)=-3` is negative and unusable.

## Corrected UV Tail Bound

For

```math
T_M(z,F)=sum_{m>M} z^m/m Tr(F^m),
```

the preferred bound is

```math
|T_M(z,F)| <= rank(F)/(M+1) * a^(M+1)/(1-a).
```

Fallback uses `rank(P)` only when the nonzero support of `F` is not isolated.

## Delta12 Discipline

Convergence is controlled by `a<1`.  `delta0^12` is a finite readout tolerance
for tail size.  There are convergent examples with tail above the threshold and
convergent examples with tail below it; therefore it is not a convergence
radius.
