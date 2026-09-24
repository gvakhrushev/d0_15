# WRK-A4D-SCALAR-ADVECTIVE-GROUPOID-OBSTRUCTION

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Research gate

SATISFIED.

Frozen terminal:

`COMMON-CENTER-CELL-ACTION-NEW-PRIMITIVE-REQUIRED`

Durable packet:

`02_REGISTRY/research/MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md`

Start from the then-current `main`. This task may run concurrently with the second-order Ward and observer/frame workers. Reuse their APIs if already merged, but do not wait for them.

## Objective

Formalize the first new theorem-ready core from the common-center research memo: the exact scalar output-site-local groupoid derivative, its forced matter second jet, and the scoped direct elementary-cell energy obstruction.

Primary module:

`03_FORMALIZATION/D0/Geometry/A4DScalarAdvectiveGroupoidObstruction.lean`

Do not broaden this worker into the full comparison-jet `𝒮` classification or an all-background matter action.

## Frozen scalar model

For a cyclic Role line with period `L ≥ 3`, use the repository's existing finite cyclic matrix conventions wherever possible:

[
\Delta=L(U-I),\qquad
D=\frac L2(U-U^{-1}),
]

[
H_0(h)=\frac12(M_hU+U^{-1}M_h),\qquad
G_\xi=M_\xi D.
]

The owned first-order Ward identity is

[
H_0(\Delta\xi)=-(G_\xi+G_\xi^T).
]

The relevant action-groupoid second-jet condition is already research-frozen. Do not assume a background-independent exponential representation.

## Mandatory formalization

### 1. Scalar commutator identity

Prove the exact finite identity

[
[M_\xi,D]=-H_0(\Delta\xi).
]

Use it as the algebraic source of the forced background derivative.

### 2. Output-site parameter-local class

Represent explicitly the scoped hypothesis

[
(g_\xi(e)\psi)_x=\xi_x(D_e\psi)_x,
\qquad D_0=D.
]

Keep this hypothesis visible in every no-go theorem. It is not a universal property of all matter lifts.

### 3. Forced derivative from the mixed groupoid law

From the mixed two-jet cocycle and the constant parameter `1`, prove

[
(dD_\bullet)_0[h_\xi]
=[M_\xi D,D]
=-H_0(h_\xi)D.
]

Package the resulting particular derivative

[
B_{\rm adv}(\xi,h)=-M_\xi H_0(h)D.
]

Prove that it satisfies the mixed cocycle equation.

### 4. Forced second jet

Prove

[
K_\xi
=
G_\xi^2+B_{\rm adv}(\xi,h_\xi)
=
M_{\xi^2}D^2.
]

This is neither the previously rejected `K=G²` specialization nor `K=0`.

### 5. Exact L=5 controls

For `ξ=δ₀`, prove the complete `K` matrix, not only diagonals.

In cyclic order `(0,+1,+2,-2,-1)` it must agree with the durable memo:

[
K=
\begin{pmatrix}
-25/2&0&25/4&25/4&0\\
0&0&0&0&0\\
0&0&0&0&0\\
0&0&0&0&0\\
0&0&0&0&0
\end{pmatrix}.
]

Using the already-owned or locally reproved second-order congruence identity, prove the complete induced energy Hessian matrix

[
W''=
\begin{pmatrix}
25&0&-25/4&-25/4&0\\
0&25/2&0&0&-25/2\\
-25/4&0&0&0&0\\
-25/4&0&0&0&0\\
0&-25/2&0&0&25/2
\end{pmatrix}.
]

In particular own the nonzero same-axis distance-two entry

[
W''_{+1,-1}=-25/2.
]

Also include one non-delta `L=5` control with `G² ≠ 0`.

### 6. Direct elementary-cell support obstruction

Define the support hypothesis precisely enough to express:

> every direct scalar matter-energy term depends only on matter arguments lying in the closure of one elementary archive cell.

For `L ≥ 5`, prove that such a direct elementary-cell Hessian cannot couple `-1` and `+1` on the same axis.

Combine with the forced Hessian above to obtain a scoped contradiction for the output-site parameter-local class.

Preferred verdict theorem name should make the hypotheses visible, e.g.

`outputSiteLocal_noDirectElementaryCellInvariantEnergy`.

Do not state a universal local-matter no-go.

## Explicitly out of scope

Do NOT formalize in this worker:

- the unrestricted analytic finite cocycle `F_φ` unless a tiny auxiliary lemma is genuinely needed;
- the full comparison-jet classification
  `𝒮 : Sym²(im d_f) → End(C⁰)`;
- the unrestricted dressing `P(e)`;
- the graded pure-gauge benchmark;
- an all-background common-center interpolation;
- observer/Lorentz completion;
- a new metric star;
- nonlinear `Q(e)` selection;
- physical stress;
- Einstein equations;
- BOOK `F_N`.

Do not claim `c=1`, `c=2`, or any other scalar reference law is physically selected.

## Relationship to other active workers

`WRK-A4D-SECOND-ORDER-CELL-ENERGY-WARD` owns the generic second-order algebra and older no-go boundary.

This worker owns the NEW independently derived particular groupoid derivative and its cell-support obstruction.

If the generic congruence theorem has merged, import it. Otherwise prove only the minimal finite matrix specialization needed here. Do not wait.

`WRK-A4D-OBSERVER-FRAME-CAR-LIFT` is orthogonal and must not be used to identify counting with a Lorentz metric.

## Expected verdict

At minimum own theorem-level versions of:

`SCALAR-ADVECTIVE-GROUPOID-DERIVATIVE-OWNED`

`SCALAR-ADVECTIVE-SECOND-JET-OWNED`

`OUTPUT-SITE-LOCAL-DIRECT-CELL-ENERGY-NOGO-OWNED`

while retaining the research terminal

`COMMON-CENTER-CELL-ACTION-NEW-PRIMITIVE-REQUIRED`.

## Validation

- preserve warm Lean/Mathlib cache;
- narrow builds during implementation;
- one incremental `lake build D0.All` before PR;
- run repository guards;
- no `lake clean`;
- no `sorry`, `sorryAx`, or new axioms;
- include `#print axioms` for capstones;
- one branch, one PR, then STOP.
