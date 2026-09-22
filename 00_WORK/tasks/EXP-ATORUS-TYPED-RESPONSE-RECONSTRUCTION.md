# EXP-ATORUS-TYPED-RESPONSE-RECONSTRUCTION

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Turn the first missing E-FRAME bridge into actual Lean-ready typed objects.

The task is **not** to prove the full continuum limit yet.

It is to determine the lowest-debt concrete Mathlib/D0 implementation of:

1. a fixed smooth (T^4) target;
2. local Role-labelled chart/frame realizations;
3. arbitrary smooth Lorentz metric sampling onto finite local stencil data;
4. pointwise reconstruction
   [
   Sym^2(Role)\to S^2T_x^*T^4;
   ]
5. exact pullback/functoriality squares.

Repository edits: **NONE**.

## Read first

- `02_REGISTRY/research/ATORUS_FRAME_ERASURE_LOCAL_DIFF_NATURALITY.md`
- `02_REGISTRY/research/ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`
- `02_REGISTRY/research/ATORUS_DIRECT_LORENTZ_CONTINUUM_REALIZATION.md`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`
- direct role-phase group/product carrier files.

Inspect the pinned Mathlib APIs actually available in this repository.

## Non-negotiable rule

Do not solve the task by creating structures whose important fields are arbitrary `Prop` placeholders.

Return actual types/functions/maps, or identify the first concrete API/type obstacle.

## Typed T4 audit

Determine the cheapest actual Lean representation of the continuum torus, for example a product of additive circles or an equivalent smooth manifold already supported by Mathlib.

For the chosen representation, identify:

- point type;
- manifold instance;
- tangent/cotangent type;
- local chart API;
- smooth maps / local diffeomorphism API;
- tensor/symmetric bilinear form representation suitable for a Lorentz metric.

If a fully typed smooth T4 is unexpectedly expensive in pinned Mathlib, identify the exact blocker rather than hiding it.

## Local grid/frame object

Give a Lean-ready definition of a local grid/frame realization at (x:T^4).

It should contain actual data such as:

- local chart / local equivalence around (x);
- Role-labelled tangent frame;
- dual coframe or an explicit linear equivalence
  [
  Role\to\mathbb R
  \simeq
  T_xT^4;
  ]
- finite radius-two stencil map at mesh (arepsilon_N=(N+2)^{-1}).

Determine whether this should be a structure over a chart, over a local equivalence with (mathbb R^4), or over a global parallelization of the torus.

## Sampling map

Produce the exact proposed type and formula for
[
S_{N,x}^{F}g(k)_{ab}
=
(\psi_F^*g)_{\varepsilon_Nk}(\partial_a,\partial_b).
]

Decide how the full smooth Lorentz metric should be typed in Lean.

The finite result should land in existing `SymRoleTensor` / local stencil component data.

## Response reconstruction

Produce the exact Lean-ready map
[
R_x^{F,resp}:
SymRoleTensor\to S^2T_x^*T^4
]
or the closest concrete tensor representation supported by Mathlib.

It must use the actual coframe/frame data, not a proposition stating that reconstruction exists.

## Pullback squares

For a local diffeomorphism (phi:U\to V), formulate the exact type-level pullback of a local grid/frame and prove or reduce to library lemmas:

[
S_N^{\phi^*F}(\phi^*g)=S_N^F(g),
]

[
R^{\phi^*F}(T)=\phi^*R^F(T).
]

These equalities are the first machine-checkable layer of the E-FRAME theorem.

## Local-only simplification

Exploit the fact that the finite response stencil has radius at most two.

The first reconstruction bridge may use only a local stencil near one point; do not require a global interpolation or spectral reconstruction theorem unless genuinely necessary.

State the clean large-(N) guard needed to avoid periodic aliasing of offsets (pm1,pm2).

## Deliverable quality

The memo must end with a proposed Lean module split, exact definitions, imports, theorem signatures and the smallest implementable worker task.

If pinned Mathlib prevents a direct formulation, identify the exact API/type obstruction and propose the least invasive bridge representation.

## Terminal verdict

Return exactly one:

- `T4-TYPED-RECONSTRUCTION-SPEC-REACHED`
- `T4-SMOOTH-MANIFOLD-API-BLOCKER`
- `T4-TANGENT-COFRAME-API-BLOCKER`
- `T4-LORENTZ-METRIC-TYPE-BLOCKER`
- `T4-PULLBACK-FUNCTORIALITY-API-BLOCKER`

## Deliverable

`MEMO_29_ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`
