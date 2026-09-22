# EXP-ATORUS-FRAME-ERASURE-LOCAL-DIFF-NATURALITY

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Attack the decisive continuum bridge identified by E-T4NAT.

Construct or terminally classify the descent
[
\text{finite framed/grid response}
\longrightarrow
E:J^2\operatorname{Met}_{(1,3)}(T^4)\to S^2T^*T^4
]
where the continuum response is metric-only, smooth, local, natural under all local diffeomorphisms of fixed (T^4), and covariantly divergence-free for every Lorentz metric.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`
- `02_REGISTRY/research/ATORUS_DIRECT_LORENTZ_CONTINUUM_REALIZATION.md`
- `02_REGISTRY/research/A4D_LINEARIZED_NOETHER_UNIQUENESS.md`
- `02_REGISTRY/research/A4D_LOCAL_GRAVITY_RESPONSE_SEED.md`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`
- direct role-phase carrier/group/product-Laplacian files;
- relevant continuum bridge assumptions.

Use Navarro/Lovelock primary sources only for the external theorem scope.

## Frozen theorem shortcut

A fixed smooth (T^4) is sufficient for Navarro once D0 has on that (T^4):

1. the full fixed-signature Lorentz metric bundle;
2. one smooth (J^2) response operator;
3. metric-only descent;
4. local-diffeomorphism naturality;
5. covariant divergence zero for every metric.

Do not reopen arbitrary-manifold reconstruction unless the fixed-manifold theorem audit is found incorrect.

## Honest finite input

The finite response may initially depend on:

- Role labels;
- a global Role frame;
- grid embedding;
- finite sampling/reconstruction choices;
- centered-difference stencil.

Represent that honestly as extra data:
[
E_N[m;F_N].
]

Do not write (E_N[m]) until frame independence is proved.

## Frame-erasure test

Formulate a precise comparison between two admissible finite grid/frame realizations (F_N,F_N') sampling the same continuum Lorentz metric jet.

A positive theorem must imply
[
R_N^{resp}E_N[S_N^{F}g;F_N]
-
R_N^{resp}E_N[S_N^{F'}g;F_N']
\to0
]
in a declared topology/norm.

Identify the minimum family of frame changes needed. It must go beyond the finite Role-permutation/hypercubic subgroup and test smooth local frame/diffeomorphism changes.

## Sampling/reconstruction audit

Determine the minimal actual data required for:

- sampling arbitrary smooth Lorentz metrics on (T^4);
- reconstructing finite local symmetric tensors into (S^2T^*T^4);
- comparing two different grid/frame choices;
- expressing response convergence at fixed local 2-jets.

If current D0 cannot even state these maps, identify that as the first exact bridge.

## Locality / J2 descent

Show what theorem would establish:
[
j_x^2g=j_x^2h
\Longrightarrow
E[g](x)=E[h](x).
]

If the finite stencil plus consistency is enough, derive the needed locality estimate.

If not, state the missing theorem.

## Local-Diff naturality

Target the literal fixed-(T^4) condition:
for every local diffeomorphism
[
\phi:U\to V
]
between open subsets,
[
E[\phi^*g]=\phi^*E[g].
]

Do not replace this with:

- grid symmetry;
- global translations;
- Role permutations;
- covariance of metric-plus-frame data.

## Divergence intertwining

Finite centered-difference divergence is not continuum covariant divergence.

State the minimum consistency/intertwining theorem needed to infer
[
\nabla^aE_{ab}[g]=0
]
for every smooth Lorentz metric from finite identities.

Test whether exact finite gauge/Noether identities plus convergence are sufficient or whether connection/volume-form approximation is additional data.

## Strong negative control

Use a grid/frame-dependent continuum law such as
[
\widetilde E[g;q]=G[g]+\alpha R[g]q
]
to verify that your proposed frame-erasure/naturality test rejects background-structured theories.

## Desired positive endpoint

One theorem-ready object:
[
E_{T4}:J^2\operatorname{Met}_{(1,3)}(T^4)\to S^2T^*T^4
]
with metric-only descent, local naturality and covariant conservation.

If this endpoint is reached conditionally on explicit comparison assumptions, list every assumption and classify it as BRIDGE/PASSPORT rather than CORE.

## Terminal verdict

Return exactly one:

- `ATORUS-METRIC-ONLY-LOCAL-NATURAL-RESPONSE-REACHED`
- `ATORUS-GRID-FRAME-SURVIVES-CONTINUUM`
- `ATORUS-RESPONSE-RECONSTRUCTION-MISSING`
- `ATORUS-DIVERGENCE-INTERTWINING-MISSING`
- `ATORUS-NATURALITY-BRIDGE-UNDERDETERMINED`

## Deliverable

`MEMO_27_ATORUS_FRAME_ERASURE_LOCAL_DIFF_NATURALITY.md`
