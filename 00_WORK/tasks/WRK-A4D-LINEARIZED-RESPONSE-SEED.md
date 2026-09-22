# WRK-A4D-LINEARIZED-RESPONSE-SEED

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
IN_PROGRESS

## Objective

Formalize one explicit finite degree-two local symmetric Role-tensor response on top of
`D0.Geometry.A4DSymRoleCentralDifference`.

This is an existence/identity theorem package only.

Do **not** claim uniqueness, physical Einstein status, Lorentz covariance, continuum naturality or Lovelock.

## Preferred branch

`work/a4d-linearized-response-seed`

## Required owner

Create a focused module such as

`03_FORMALIZATION/D0/Gravity/A4DLinearizedMetricResponse.lean`

reusing:

- `SymRoleTensor`;
- `LocalSymRoleField`;
- `LocalRoleVector`;
- `centeredDifference`;
- `centeredDifference_comm`;
- `centeredDifference_skew_adjoint`;
- `symmetricRoleGradient`.

Do not duplicate those definitions.

## Euclidean finite operations

Define on a local symmetric Role field:

- trace
  [
  t(x)=\sum_c h_{cc}(x);
  ]
- divergence
  [
  v_b(x)=\sum_cD_ch_{cb}(x);
  ]
- scalar double divergence
  [
  q(x)=\sum_{c,d}D_cD_dh_{cd}(x);
  ]
- scalar/tensor Laplacian using (\sum_cD_cD_c).

Then define the normalized finite response
[
\begin{aligned}
(E_\delta h)_{ab}
={}&
\Delta h_{ab}
-(D_av_b+D_bv_a)
+D_aD_bt\\
&+\delta_{ab}q
-\delta_{ab}\Delta t.
\end{aligned}
]

An overall factor such as (1/2) is unnecessary.

## Required theorems

1. output is a `SymRoleTensor` at every site;
2. exact gauge nullity:
   [
   E_\delta(K\xi)=0;
   ]
3. define local finite tensor divergence and prove:
   [
   \operatorname{div}E_\delta(h)=0;
   ]
4. prove the finite adjoint relation needed for the action, preferably
   [
   K^*=-2\operatorname{div}
   ]
   or the exact componentwise identity sufficient for the response;
5. prove self-adjointness of (E_\delta) under the global finite Role/site inner product;
6. define
   [
   S[h]=\frac12\langle h,E_\delta h\rangle;
   ]
7. prove the exact quadratic first-variation identity;
8. derive exact gauge invariance of (S);
9. keep the stencil radius bound explicit: all evaluations use sites at role-group distance at most two.

## Small-cycle boundary

The existing carrier proves:
[
D_a=0
]
at (N=0), (L=2).

Record the corresponding response degeneration explicitly.

Do not make a nontriviality statement there.

For (N\ge1), if reasonably short, add one explicit field/control proving that a second-difference term and (E_\delta) are nonzero.

If that control becomes disproportionately expensive, leave it as a named follow-up theorem rather than weakening the exact gauge/divergence/action package.

## Firewalls

Do not call this object:

- the Einstein tensor;
- a Lovelock tensor;
- a continuum tensor;
- Lorentz covariant;
- unique;
- selected by D0.

The accepted research result explicitly says another finite ray survives under owned (S_4) symmetry.

The safe interpretation is:

> one explicit local finite metric-response seed with exact gauge/Noether/action algebra.

## Integration

Register as formal support for the active gravity research frontier only, unless an existing claim literally matches the implemented theorem.

Run target build, `lake build D0.All`, all guards/generated views, no-sorry scan and `#print axioms` on capstones.

Move task to REVIEW, open PR and STOP.

Do not advance CAR-parity or certificate-freshness workers.
