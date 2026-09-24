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
4. Research terminal is frozen as `FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED`.

Current main satisfies all four start gates: the flux kernel is merged via PR #75, the located primal/dual star is merged via PR #76, a WORKER slot is free, and the research terminal is frozen.

Durable research packets:

- `02_REGISTRY/research/MEMO_A4D_SECOND_ORDER_CARTAN_CELL_ENERGY_INTEGRABILITY.md`
- `02_REGISTRY/research/MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md`

This task integrates that verdict. It must not guess `K`, choose `c`, or repair a negative research result by inventing a different finite action.

## Three-star dictionary — keep these objects distinct

| Name | Meaning |
|---|---|
| `J` | Two-color center-matched primal/dual placement/pairing. Topological complement sign `(-1)^(k*(4-k))`. In 4D it preserves Fock parity. It is not a metric constitutive selector. |
| `h_n` / metric `*_eta` | Observer/Lorentz metric structure. The Lorentzian double-star carries the additional signature exponent `q=3`. This is not cell placement. |
| scalar reverse-star | A one-color local inverse/reverse stencil used only in the scoped two-sided-locality no-go. It is neither `J` nor the Lorentz metric star and it does not select `Q(e)`. |

Never transfer a theorem or no-go from one row to another without an explicit typed bridge.

## Frozen research terminal

`FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED`

Do not choose `c` and do not invent a canonical `K`.

The accepted research handoff adds these mandatory results:

- exact two-jet congruence identity;
- generic `L≥3` delta witness and the full symmetric block, not only the three diagonals;
- at `L=5`, the mixed condition `K_{+,-}+K_{-,+}=-25/2` in addition to the diagonal conditions;
- scoped no-go: no background-independent differentiable representation of the owned abelian pure-translation subgroup has all tangents `G_ξ=M_ξD`;
- under the explicit hypothesis `Q(t) 1 = 1`, both displayed positive coefficients `c=1,2` are rejected; within that diagonal ansatz constants preservation forces `c=0`, but this is NOT a completed physical action;
- action-groupoid identities `K_ξ=G_ξ²+(D_e g_ξ)[d_f ξ]` and the mixed cocycle equation;
- second derivative of the moving differential and the six-term second derivative of the mixed parent;
- transverse Hessian freedom outside `im d_f`, with plaquette-curl witness.

The research nonlocal energy-engineered countermodel is a logical hostile control only. Do not formalize it as a candidate physical matter lift.

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
D0/Geometry/A4DScalarAdvectiveGroupoidObstruction.lean
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
I+tH(h)+\frac{t^2}{2}\left(H(a)+B(h,h)\right)+O(t^3),
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

Use `L=5` exactly as frozen by the EXP memo unless that memo explicitly replaces the witness by a proved generic-`L` theorem. The constants `25/4`, `25 c`, etc. are the `L=5` specialization of the generic `L^2/4` formula.

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


## Package J — integrated scalar advective groupoid obstruction

This package absorbs the theorem-ready core of
`MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md`.
Do NOT create a separate worker for it.

The package is deliberately scoped to the scalar class with **output-site parameter locality**

\[
(g_\xi(e)\psi)_x=\xi_x(D_e\psi)_x,\qquad D_0=D.
\]

Every no-go theorem below must expose that hypothesis. It is not a theorem about all background-dependent matter lifts.

### J1. Commutator and forced background derivative

Prove

\[
[M_\xi,D]=-H_0(\Delta\xi).
\]

Use the mixed action-groupoid two-jet law with the constant parameter \(\mathbf 1\) to derive

\[
(dD_\bullet)_0[h_\xi]
=
[M_\xi D,D]
=
-H_0(h_\xi)D.
\]

Define the particular mixed-cocycle derivative

\[
B_{\rm adv}(\xi,h)
=
-M_\xi H_0(h)D
\]

and prove that it satisfies the complete mixed cocycle equation.

### J2. Forced matter second jet

Prove

\[
K_\xi
=
G_\xi^2+B_{\rm adv}(\xi,h_\xi)
=
M_{\xi^2}D^2.
\]

This is a **derived particular second jet inside the explicit output-site-local class**.
It does not replace the generic `K` in Packages A--I and does not select a universal matter representation.

### J3. Complete L=5 delta matrix

For \(\xi=\delta_0\), in cyclic order
\((0,+1,+2,-2,-1)\), own the complete matrix

\[
K_\xi=
\begin{pmatrix}
-25/2&0&25/4&25/4&0\\
0&0&0&0&0\\
0&0&0&0&0\\
0&0&0&0&0\\
0&0&0&0&0
\end{pmatrix}.
\]

Using the generic congruence package, own the induced energy Hessian

\[
D^2W_0[h,h]=
\begin{pmatrix}
25&0&-25/4&-25/4&0\\
0&25/2&0&0&-25/2\\
-25/4&0&0&0&0\\
-25/4&0&0&0&0\\
0&-25/2&0&0&25/2
\end{pmatrix}.
\]

In particular prove the nonzero same-axis distance-two entry

\[
(D^2W_0[h,h])_{+1,-1}=-25/2.
\]

Also include the durable memo's non-delta `L=5` control with \(G^2\ne0\). Do not generalize delta nilpotence to that case.

### J4. Scoped direct elementary-cell obstruction

Define the support assumption literally:

> each direct scalar matter-energy term uses matter arguments contained in the closure of one elementary archive cell.

For \(L\ge5\), prove that a direct elementary-cell Hessian cannot couple the same-axis sites \(-1\) and \(+1\). Combine this with J3 to prove the scoped contradiction.

Preferred theorem semantics:

`outputSiteLocal_noDirectElementaryCellInvariantEnergy`.

This is **not**:

- a universal local-matter no-go;
- a no-go for an inverse-free local parent with auxiliary variables;
- a no-go for larger patches;
- a no-go for a generator carrying the comparison correction
  \(\mathcal S(h_\xi,h)\).

### J5. Handoff boundary to the active EXP

Record, without trying to solve it in Lean here, that unrestricted flat mixed-cocycle solutions may differ from `B_adv` by

\[
\mathcal S:
\operatorname{Sym}^2(\operatorname{im}d_f)\to\operatorname{End}(C^0),
\]

symmetric in its two coframe arguments.

The construction/integration of this comparison jet belongs to
`EXP-A4D-ENDPOINT-COMPARISON-JET-OVERLAP-LAW`.
Do not invent \(\mathcal S\) in this worker.

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
SCALAR-ADVECTIVE-GROUPOID-DERIVATIVE-OWNED
SCALAR-ADVECTIVE-SECOND-JET-OWNED
OUTPUT-SITE-LOCAL-DIRECT-CELL-ENERGY-NOGO-OWNED
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

## Research-terminal theorem package

Preferred theorem/module decomposition from the accepted memo:

- `A4DSecondOrderCartanCongruence`
- `A4DScalarDeltaSecondJet`
- `A4DAffineMatterLiftObstruction`
- `A4DActionGroupoidSecondJet`
- `A4DMovingDifferentialSecondJet`
- `A4DCellHessianTransverseModulus`
- `A4DScalarAdvectiveGroupoidObstruction`

Keep every no-go scoped to its explicit representation/constant-preservation hypotheses.
