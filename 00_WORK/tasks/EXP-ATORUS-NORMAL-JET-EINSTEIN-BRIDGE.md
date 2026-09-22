# EXP-ATORUS-NORMAL-JET-EINSTEIN-BRIDGE

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Test the strongest concrete finite-to-continuum shortcut now visible in the research.

In metric normal coordinates, the centered-difference Lorentz linearized response should converge to the second-jet expression of the Einstein tensor at the base point.

Determine whether this can be made into a theorem-ready D0 bridge without circularly assuming the Einstein field equation.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/ATORUS_FRAME_ERASURE_LOCAL_DIFF_NATURALITY.md`
- `02_REGISTRY/research/A4D_ANISOTROPIC_RAYS_NATURALITY_SELECTOR.md`
- `02_REGISTRY/research/A4D_LINEARIZED_NOETHER_UNIQUENESS.md`
- `02_REGISTRY/research/ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`
- active finite response worker brief.

Use standard differential-geometric identities only as explicit external background/bridge statements.

## Core observation to verify

For a Lorentz metric (g), choose (g)-normal coordinates at (x):
[
g_{ab}(x)=\eta_{ab},
\qquad
\partial_cg_{ab}(x)=0.
]

At the center, all terms in (G[g](x)) quadratic in first derivatives vanish.

The remaining second-derivative expression should match, up to convention/scale, the continuum limit of the finite Lorentz degree-two ray (E_\eta).

Verify the formula exactly; do not rely on the memo's assertion if a sign/factor is wrong.

## Finite stencil consistency

For (arepsilon=(N+2)^{-1}), derive exact Taylor error estimates for:

[
D_af(0),
qquad
D_aD_bf(0),
qquad
D_a^2f(0)
]

using the actual D0 centered-difference normalization, including the two-step diagonal stencil.

State the minimum smoothness and the clean (L\ge5) local-stencil guard.

## Tensor response consistency

Apply those estimates to arbitrary smooth Lorentz metric components in normal coordinates.

Determine whether the reconstructed finite response satisfies
[
R_x^{F,resp}E_{\eta,N}[S_N^Fg]
=
c\,G[g](x)+O(\varepsilon^2)
]
for one exact nonzero constant (c).

If the correct target is only the principal linearized response rather than the full (G[g](x)), say so and explain precisely why.

## Circularity audit

Distinguish:

1. using the standard geometric identity for the Einstein tensor in normal coordinates;
2. assuming the Einstein **field equation**;
3. invoking Lovelock/Navarro characterization.

Only (2) would be circular for the intended route.

Classify what is being imported as EXTERNAL-BACKGROUND versus what D0 is proving.

## Frame independence

Normal coordinates depend on an orthonormal frame.

Use E-RAYSEL to test whether the isotropic Lorentz ray (E_\eta) yields the same reconstructed tensor under two normal frames related by (O(1,3)).

A positive bridge must not retain the preferred Role frame.

## Nonlinear significance

If the local estimator really converges to (cG[g](x)) for arbitrary metric jets, explain whether this already gives a direct continuum Einstein-tensor bridge stronger than the Lovelock route, or whether it is merely a consistency check because the target (G) was inserted externally.

Do not overclaim.

## Divergence issue

Even if pointwise convergence to (G) is established, distinguish:

- conservation inherited because the target is already identified as (G);
- deriving covariant divergence from finite Noether via an intertwining theorem.

These are epistemically different.

## Relation to cosmological term

A second-difference estimator cannot by itself select the (b,g) cosmological term.

State exactly what remains unfixed.

## Terminal verdict

Return exactly one:

- `NORMAL-JET-EINSTEIN-ESTIMATOR-REACHED`
- `NORMAL-JET-ONLY-LINEARIZED-PRINCIPAL-REACHED`
- `NORMAL-JET-FRAME-ERASURE-BRIDGE-OPEN`
- `NORMAL-JET-RECONSTRUCTION-MISSING`
- `NORMAL-JET-EINSTEIN-IDENTIFICATION-CIRCULAR`

## Deliverable

`MEMO_30_ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`
