# CVFT Cert Example Audit and Fix

Status: accepted A5 audit; deterministic cert correction only. No frontier
promotion to core or certificate-closed status.

## 3x3 Cyclic Audit

The cyclic example

```math
P=diag(1,1,0),\qquad
U=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}
```

has `rank(F)=1`, not `2`, for `F=(QUP)^dagger(QUP)`.

## Correct 4x4 Full-Rank Crossing

Use `P=diag(1,1,0,0)` and let `U` swap `e1<->e3` and `e2<->e4`. Then

```math
rank(QUP)=2,\qquad F=P,\qquad rho(F)=1.
```

## Boundary Dimension Below Edge Count

For `P=diag(1,1,1,0)`, a Householder reflection can couple three retained
coordinates into one traced-out boundary coordinate. Then

```text
edge_count_like = 3
dim(B_partial) = 1
rank(QUP)=1
rank(F)=1
```

The controlling object is boundary-channel dimension, not raw edge count.

## Correct Negative Controls

The naive `z/(1-z)` bound is not a valid theorem statement:

- for complex `z`, `z/(1-z)` is complex and cannot upper-bound a real magnitude;
- for `z=1.5`, `rho(F)=0.5`, `a=|z|rho(F)=0.75<1` but `z/(1-z)=-3`.

Convergence is controlled by `a=|z|rho(F)<1`.  `delta0^12` is a readout
tolerance threshold for tail size, not a convergence radius.
