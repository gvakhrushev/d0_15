# EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `exp/a4d-joint-palatini-local-uniqueness`  
Primary artifact: `02_REGISTRY/research/MEMO_A4D_JOINT_PALATINI_LOCAL_UNIQUENESS.md`  
Execution: `GitHub-first`

## Why delegated

Merged #227 proves that naked-star connection stationarity alone is not a selector: on the fixed flat metric there is an exact curved family with (E_K=0), nonzero curvature, and a different normalized metric partial. Therefore the old all-sheet elimination/rescue obligation is false.

The Einstein seed itself remains intact on the designated smooth sheet: #201/#216/#223 still give the owned local coefficient (T_1^{[2]}=rac14E_\eta	o-rac12G). The new problem is the genuine Palatini one: analyze the **joint** critical system, not every connection-stationary sheet.

This task must not try to reconstruct a globally single-valued off-shell (K_*(Q)). The primary theorem target is on-shell/joint-critical.

## Mandatory inputs

Read fully:

- #201 physical quotient / Einstein seed;
- #208 corrected polarized nonlinear bridge;
- merged #216 fixed-realization IR/locality memo and certificates;
- merged #223 normal-coordinate locality worker;
- merged #225 slow-background diagonal splitting control;
- merged #226 metric-response sensitivity bound;
- merged #227 exact curved (E_K=0) no-go;
- current #202 only as a lower-wall control; do not edit it;
- the joint-linear-kernel and diagonal-invisible workers when they become available.

## Starting structural facts

For identity links, curvature vanishes for every solder/metric, hence

[
S_\star(Q,I)=0
]

identically in (Q). Therefore at ((\eta,I)),

[
H_{QQ}=0.
]

The linearized joint Palatini Hessian has saddle form

[
\mathcal H_J=
\begin{pmatrix}
0&H_{QA}\\
H_{AQ}&H_{AA}
\end{pmatrix}.
]

At low phase (H_{AA}) is uniformly invertible and the Schur complement is the already-owned metric response route.

At the diagonal quarter wave #216 owns

[
\operatorname{rank}H_{AA}=16,qquad
\dim_\mathbb C\ker H_{AA}=8,
]

while adding the genuine metric source raises the augmented rank to (20). Thus four connection-kernel directions are linearly source-visible and four remain source-invisible. Do not call the latter gauge until the exact quotient/curvature test proves it.

Across the L=4 singular inventory, if (d=r_{\rm aug}-r_H), the linear joint-invisible dimension is

[
(24-r_H)-d.
]

The already-owned rank types therefore imply:

[
(20,24,4)\mapsto0,qquad
(22,24,2)\mapsto0,
]

while only

[
(22,23,1)\mapsto1,qquad
(20,23,3)\mapsto1,qquad
(16,20,4)\mapsto4
]

retain linear connection-null directions after metric pressure.

This reduction is a roadmap, not yet a theorem about the full nonlinear joint system.

## Objective

Prove or exactly obstruct the following scoped statement:

> For exact finite joint-critical sequences ((Q_h,K_h)) in the declared smooth near-flat sector,
> [
> E_K(Q_h,K_h)=0,qquad
> E_Q(Q_h,K_h)=\kappa T_h,
> ]
> every UV/resonant connection component invisible to the designated smooth Palatini branch is eliminated modulo genuine gauge/physical flat directions; the surviving smooth branch has the already-owned continuum response
> [
> E_Q\to -\frac12G+\kappa T.
> ]

This is **not** global uniqueness of all metric solutions. Metric gauge, flat moduli, and physical infrared Einstein modes must be quotiented or retained correctly.

## Required gates

### J1 — exact joint linear census

Use the worker-owned exact character census.

For every singular L=4 orbit type identify:

- (ker H_{AA});
- rank of (H_{QA}) restricted to that kernel;
- the exact source-invisible subspace
  [
  N_0=\ker H_{AA}\cap\ker H_{QA};
  ]
- genuine quotient/gauge status.

The #227 tangent must be identified explicitly as source-visible; its exact curved (E_K=0) family is therefore cut already by the linear metric equation.

### J2 — nonlinear pressure only on residual orbit types

Do not redo all 56 characters.

Only orbit types with (N_0\neq0) require nonlinear joint Lyapunov-Schmidt analysis.

Start with the diagonal four-dimensional invisible sector, then the one-dimensional residual types.

Range-eliminate the regular connection variables and compute the first nonzero **joint** reduced equations, including both:

[
E_K^{\rm red}=0,qquad
E_Q^{\rm red}=0
]

in vacuum.

A connection-only reduced potential is insufficient.

### J3 — vacuum joint isolation or exact no-go

For each residual physical invisible sector, determine whether the joint vacuum zero is isolated modulo actual gauge/flat moduli.

If the linear joint Hessian remains singular, do not invoke ordinary IFT. Use exact nonlinear normal form, local degree, Łojasiewicz, or a direct algebraic isolation/no-go certificate.

An explicit nontrivial curved family with

[
E_K=E_Q=0
]

approaching flat is a terminal obstruction.

### J4 — torsion only as diagnostic

Use the exact discrete Cartan/open-torsion owner to classify the #227 family and residual invisible modes.

Torsion-free may be reported as a property of the designated LC-like branch only if proved. Do not add (T=0) as a new equation by hand and do not introduce (T_{\rm open}^2) as a new action channel; the repository already owns its full-affine limitation.

### J5 — sourced/smooth continuation

Only after vacuum joint isolation is owned, study small smooth metric/matter forcing.

The desired local statement is not a global metric uniqueness theorem. It is a normal theorem around the designated smooth Palatini solution set, modulo metric gauge/physical IR directions.

If the reduced joint map is linearly invertible after quotient, use an IFT. If not, use the certified nonlinear degree/normal form.

### J6 — continuum coefficient

Combine the joint branch control with:

- #216 fixed-realization IR expansion;
- #223 nonlinear normal-coordinate locality;
- #226 polynomial response sensitivity.

On the designated joint-critical smooth branch recover

[
E_{\star,h}[g](x)
=
-\frac12G[g](x)+o(1)
]

with the exact normalization already owned.

Do not promote an off-shell branch-independent J² operator unless separately proved.

## Desired terminals

Positive:

`NAKED-STAR-JOINT-PALATINI-SMOOTH-EINSTEIN-BRANCH-CLOSED`

Negative:

`NAKED-STAR-JOINT-PALATINI-LOCAL-UNIQUENESS-NOGO`

Partial:

`NAKED-STAR-JOINT-PALATINI-PARTIAL-CLOSURE`

with exactly one smallest remaining joint blocker.

## Forbidden

No return to all-sheet (E_K) rescue.

No new gravitational invariant, Holst term, (arphi), filter, or I-channel.

No boundary-condition change used as a “selector”.

No torsion-free postulate unless derived from the existing equations/branch.

No claim that #227 invalidates the #201/#216 designated-sheet seed.

No requirement of a global off-shell (K_*(Q)).

No self-merge.

## GitHub execution contract

Start from fresh current `main` after this registration is merged. Run lifecycle start, open a Draft PR before substantive scientific edits, keep Git-visible task state synchronized with the PR lifecycle, self-retire only at a declared terminal, refresh against current `main` before Ready, and never self-merge.

## Chat handoff

Return the PR number, final SHA, exact joint kernel dimensions, nonlinear residual sectors, terminal, and only the first remaining obstruction.
