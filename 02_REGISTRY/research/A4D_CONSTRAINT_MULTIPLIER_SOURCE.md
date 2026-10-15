# A constrained tangent residual is not an edge-constraint multiplier

Status: exact variational conclusion for the named two-tick preparation; not a
native source theorem for the whole D0 core.

## The multiplier cannot absorb a tangent response

On the joint carrier, an edge constraint is

```text
C_e(q_s,q_t,D) = D_e q_t D_e^T - q_s = 0.
```

Its actual differential is

```text
dC_e = dD_e q_t D_e^T + D_e dq_t D_e^T
       + D_e q_t dD_e^T - dq_s.
```

If a differentiable price `B` is written with a Lagrange multiplier as

```text
L = B + sum_e <Lambda_e, C_e>,
```

then the constraint contribution to a first variation is
`sum_e <Lambda_e, dC_e>`. It vanishes on every admissible constrained tangent.
The multiplier is a conormal to the constraint surface; it cannot cancel a
nonzero derivative of `B` along that surface. The stationarity equation from
varying `q_s` alone may express `Lambda` using an ambient partial derivative,
but the remaining stationarity equations still require `dB[v]=0` for every
admissible tangent `v` (or require an additional owned action term to supply
the opposite tangent derivative). Identifying that conormal with the physical
Einstein source would conflate different covectors.

## Exact factor-tangent test

Take the existing constant Lorentz factor curve

```text
q(t) = diag(4 exp(2t), -exp(-2t)/4, -1, -1),
D_e(t) = I,  b_e(t) = 0,  m_x(t) = 0.
```

At every edge, `q_s=q_t=q` and `D=I`. Its tangent is
`dq_s=dq_t=V_q=diag(8,1/2,0,0)`, `dD=0`, so `dC_e=V_q-V_q=0` exactly. It
is a genuine tangent of the complete joint metric/link constraint, not an
ambient metric partial. The fixed recorded observer gives the associated
positive pairing curve `Q(t)=diag(4 exp(2t), exp(-2t)/4, 1, 1)`, with
`dQ/dt|_0=diag(8,-1/2,0,0)`.

For the complete owned two-tick bootstrap price `B=H_Q+J` in the fixed-gate
preparation, `J'=0` and the exact full-spectrum heat calculation gives

```text
d/dt B(Q(t))|_0 = 2 (E_1 - E_2) > 1/10000,   beta = log 2, L >= 2.
```

The complete proof and the all-`L` bound are in
[`A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md`](A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md),
equation (15). Independently, the joint matter/metric certificate verifies the
literal `L=2` full-256-cochain value and proves symbolically that every edge
multiplier pairs to zero with this tangent; see
[`A4D_NATIVE_MATTER_OBSERVER_PAIRING.md`](A4D_NATIVE_MATTER_OBSERVER_PAIRING.md),
equation (15), and its exact checker.

Therefore no choice of `Lambda_e` makes this price stationary on the stated
constrained preparation. At the same constant flat metric, the fixed physical
probe covector `rho_0` is zero in all ten packed metric slots. A fixed nonzero
calibration cannot turn the strictly nonzero tangent derivative into that
zero covector. If a same-carrier matter or other price term is present, its
own derivative must contribute `-2(E_1-E_2)` on this tangent for stationarity;
matching all ten slots requires the full ten-component equation, not this one
contraction. Such a term must come from its own action and variations and may
not be fitted to `rho_0`.

## Scope

This rejects one specific escape: relabeling the nonzero heat/source residual
as the multiplier of the metric-compatibility constraint. It does not exclude
another admitted joint action or a non-isospectral preparation with its own
derived tangent response. Physical admission of this price/preparation,
source/Ward, stationarity for the full D0 system, curved solutions, and the
original #310/#202/#317 terminals remain open. No action, selector or physical
postulate is introduced here.
