# WRK-A4D-SECOND-ORDER-CELL-ENERGY-WARD

## Class

WORKER / FORMALIZATION + INTEGRATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

Do NOT start until all are true:

1. a WORKER slot is free;
2. `WRK-A4D-PRIMAL-DUAL-FLUX-ENERGY-KERNEL` is merged;
3. `WRK-A4D-LOCATED-PRIMAL-DUAL-STAR` is merged or CONTROL explicitly accepts its located-pairing API;
4. `EXP-A4D-SECOND-ORDER-CARTAN-CELL-ENERGY-INTEGRABILITY` has a terminal memo.

This task integrates the research result. It must not guess the research terminal.

## Objective

Formalize the exact second-order covariance algebra of a quadratic cell energy and the scalar Cartan witness that tests nonlinear completion beyond the frozen first jet.

The task connects:

[
J\text{ fixed},
qquad
DW|_0=H,
]

to the first theorem-owned constraint on:

[
D^2W|_0.
]

It does not select a physical Lorentz stress tensor.

## Suggested modules

```text
D0/Geometry/A4DSecondOrderEnergyCovariance.lean
D0/Geometry/A4DSecondOrderCartanWitness.lean
```

Optionally add a thin integration module importing located star + flux kernel if needed.

## Package 0 — reference strict-cell nonlinear laws

Once the flux-energy API is available, formalize the two reference laws from the located-star/cell-action memo on the FULL uncentered coframe:

```math
q_S(x;e) = sum_{r,a} (e_r^a(x))^2  for S=empty,
q_S(x;e) = sum_{r in S,a} (e_r^a(x))^2  otherwise,
```

```math
W_1 = I + H + M_q,
W_2 = I + H + 2 M_q.
```

Suggested additional module: `D0/Geometry/A4DLocatedMatterCellEnergy.lean`.

Own as reference-cochain theorems: same flat value, same complete first jet H, dependence on full uncentered e, degree/parity preservation, strict forward elementary-cell support, L=2 Nyquist matrices, L=3 corner equality and explicit second-order separation.

Do not claim local Lorentz covariance. Do not substitute PR #69's older `I+H+alpha H^2` family; it is a different nonselection witness with longer matter support.

## Package A — generic two-jet congruence algebra

Over a suitable field, formalize:

[
Q(t)=I+tG+\frac{t^2}{2}K,
]

with formal inverse to second order.

For:

[
W(0)=I,
]

derive the second-order coefficient of:

[
Q(t)^{-T}Q(t)^{-1}.
]

Capstone target:

```text
secondOrderCongruenceCoefficient
```

with result:

[
2(G^T)^2+2G^TG+2G^2-(K^T+K).
]

No analytic exponential is required.

## Package B — background-chain rule

Formalize the algebraic two-jet rule:

[
e(t)=th+\frac{t^2}{2}a,
]

[
W(e(t))
=
I+tH(h)+\frac{t^2}{2}
left(H(a)+B(h,h)ight)+O(t^3),
]

where `B` is a supplied symmetric bilinear Hessian.

Provide a theorem equating this coefficient to Package A under covariance hypotheses.

## Package C — exponential specialization

When:

[
K=G^2,
]

derive:

[
H(a)+B(h,h)
=
(G^T)^2+2G^TG+G^2.
]

Name the theorem so it is clearly a specialization, not a physical selection theorem.

## Owned background-gauge specialization

PR #70 already owns the finite flat affine translation background. For the scaled node translation:

```math
e(t)=t d_f xi,
```

so the primary physical specialization has `a=e''(0)=0`.

The unknown `K` is the second jet of the MATTER representation. Keep the generic algebraic `a` theorem as a reusable lemma, but do not present arbitrary `a` as the owned flat affine orbit.

## Package D — exact scalar five-cycle witness

Reuse existing five-cycle infrastructure where possible.

Set:

[
U f(x)=f(x+1),
quad
D=\frac52(U-U^{-1}),
quad
\Delta=5(U-I),
]

[
\xi=\delta_0,
quad
h=\Delta\xi,
quad
G=M_\xi D.
]

Prove structurally:

[
H_0(h)=\frac12(M_hU+U^{-1}M_h)=-(G+G^T).
]

Then prove:

[
G^2=(G^T)^2=0.
]

Extract the relevant diagonal entries of `2G^TG`.

## Package E — memo two-model Hessian family

After the flux kernel API lands, define or abstract the second-order diagonal correction:

[
B_c(h,h)=2cM_{h^2}.
]

Prove that on the scalar sector:

[
\operatorname{diag}H_0(a)=0
]

for every `a`.

## Package F — exponential/zero-second-jet no-go

Prove:

For every real/rational `c` and every second background acceleration `a`,

[
H_0(a)+2cM_{h^2}
\ne
(G^T)^2+2G^TG+G^2.
]

A single diagonal entry at site `+1` should close the proof.

Expected theorem:

```text
deltaCartan_exponentialSecondOrder_noCellDiagonalCompletion
```

Also prove the `K=0` specialization.

This is stronger than only rejecting `c=1` and `c=2`.

## Package G — general K necessary diagonal conditions

For a general second jet `K`, prove the necessary scalar conditions:

[
K_{+1,+1}=\frac{25}{4},
]

[
K_{0,0}=-25c,
]

[
K_{-1,-1}=25\left(\frac14-c\right)
]

for `L=5`.

If the research memo derives a canonical `K`, add the corresponding `c` selection/no-go theorem exactly as stated there.

Do not invent `K` if research leaves it open.

## Package H — moving-d integration boundary

Add theorem/documentation tying the second-order energy calculation to the existing fact that moving `d` has its own quadratic remainder.

Do not suppress moving differential terms in any claimed Ward theorem.

If the EXP memo supplies a full second-order mixed-parent identity, formalize it.

Otherwise stop at the exact algebraic seam.

## Package I — located-pairing integration

Import the located star owner only to record that the pairing/placement is fixed independently of the nonlinear energy Hessian.

Prove no theorem implying that `J` selects `B`.

Keep:

[
S_J=\iota_J^{-1}W.
]

The same `J` may support different `W`.

## Truth boundaries

Do NOT claim:

- finite diffeomorphism group;
- physical Lorentz covariance;
- metric-star selection;
- unique cell energy unless the EXP memo proves it;
- stress conservation;
- Einstein equation;
- BOOK `F_N`.

## Expected verdict

Follow the EXP terminal exactly.

At minimum the formalization should own:

```text
SECOND-ORDER-ENERGY-COVARIANCE-ALGEBRA-OWNED
DELTA-CARTAN-EXPONENTIAL-SECOND-ORDER-NOGO-OWNED
```

If selector remains open, retain:

```text
FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED
```

## Validation / lifecycle

Narrow builds first; one `lake build D0.All` before PR.

No `lake clean`.

No `sorry`, `sorryAx`, or new axioms.

One branch, one PR, report capstones and `#print axioms`, then STOP.
