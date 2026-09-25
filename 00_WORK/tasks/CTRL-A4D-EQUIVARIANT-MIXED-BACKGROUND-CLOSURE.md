# CTRL-A4D-EQUIVARIANT-MIXED-BACKGROUND-CLOSURE

## Class
CONTROL

## State
IN_PROGRESS

## Parent
ROOT

## Why this control exists

The previous `CTRL-GRAVITY-DYNAMICS-CLOSURE` fixed-level constitutive seam is closed by the landed sequence through PR #130 and PR #134:

- relative A/e relation/span and sourced transport are owned;
- active-span extension and labelled endpoint descent are separated and Lean-owned;
- rank-transition continuity is classified, including the projector-incidence / holonomy-kernel resolution and the unresolved global-continuity no-go;
- finite graded coframe dressing is terminally classified: bare representatives exist, but the canonical coframe-only frame-equivariant selection does not follow from the landed data;
- the exact pure-gauge dressing is a right orthogonal constant-potential torsor, not a single-valued function of the coframe.

The new seam is therefore not "find another local J" and not "pick a polar representative".

It is the first genuinely **joint background** layer.

## Frozen inputs

Treat as frozen:

- PR #123 / #126: rank-stratified relative A/e relation, canonical active-span comparison, vertical defect;
- PR #125 / #127: sourced diagonal transport and active-span extension independence;
- PR #128 / #129: classical interface pressure and independent labelled endpoint-locality boundary;
- PR #130: selected rank-transition continuity criterion, local projector-incidence resolution, global fixed-kernel resolution, stable/resolved domain split, and the no-go for an unrestricted continuous unresolved selector preserving the raw controls;
- PR #134: finite graded dressing moduli classification, constant-potential torsor, carrier-correct transverse skew freedom, single-site exponential boundary, and the coframe-only equivariance obstruction reconciled with #130;
- the landed affine-sensitive nilpotent matter letter `T_kappa`.

Do not reopen these as generic searches.

## Exact frontier

The remaining finite-N question is whether the classified pieces assemble into one exact covariant object.

The admissible input is now explicitly one of

[
(A,e)inmathfrak A_{m stable}
]

or

[
(A,e,Xi),
qquad
Xi=((Pi_y)_y,Q_o),
]

where (Xi) retains the local rank-transition and global holonomy-kernel continuation data.

The dressing itself may have to be torsor/groupoid-valued because

[
F_{phi+c}=F_phi R_c
]

with nontrivial orthogonal constant-potential isotropy.

## Active research lanes

1. `EXP-A4D-RESOLUTION-MEMORY-FUNCTORIALITY-MINIMALITY`
   — decide exactly what (Xi) is as a transportable datum and whether any smaller datum preserves the mandatory controls.

2. `EXP-A4D-EQUIVARIANT-JOINT-BACKGROUND-DRESSING-GROUPOID`
   — construct or obstruct the exact frame-covariant torsor/groupoid dressing on the stable/resolved background category.

3. `EXP-A4D-CROSSED-DRESSING-MISMATCH-MATTER-ACTION`
   — determine whether the remaining dressing/resolution moduli survive as genuinely different affine-sensitive matter actions after coupling to (T_kappa).

These lanes may run in parallel. None may assume the answer of another.

## Pressure rule

Every proposed compression/quotient/selection must be tested on:

- flat;
- constant pure shift;
- exact translation gauge including rank drop;
- L=2 Nyquist;
- L=3 corner/curl;
- harmonic raw coframe;
- the #130 rank-jump mismatch witness;
- post-source fixed-kernel dimension jump;
- trivial and nontrivial labelled holonomy.

A repair that makes the map continuous by erasing one of these required distinctions is not a closure.

## Firewalls

Do not start:

- second-order Hessian selection;
- stress tensor / Einstein dynamics;
- continuum-limit claims;
- physical time;
- golden/AF refinement;
- (k=n).

Those remain downstream until this joint-background seam is closed.

## Exit condition

This CONTROL may close only after:

1. (Xi) is functorially/minimally classified;
2. the equivariant finite dressing/groupoid law is constructed or terminally obstructed on a precisely typed domain;
3. the crossed (T_kappa) coupling is classified for dependence on all surviving moduli;
4. all mandatory hostile controls survive literally.
