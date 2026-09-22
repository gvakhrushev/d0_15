# EXP-A4D-ANISOTROPIC-RAYS-NATURALITY-SELECTOR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Use the continuum metric-only/local-diffeomorphism criterion to classify the exact extra finite rays found by E-LIN.

Do **not** add a new finite symmetry just to remove them.

Repository edits: **NONE**.

## Required reading

- `02_REGISTRY/research/A4D_LINEARIZED_NOETHER_UNIQUENESS.md`
- `02_REGISTRY/research/ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`
- `02_REGISTRY/research/ATORUS_DIRECT_LORENTZ_CONTINUUM_REALIZATION.md`
- `03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean`

## Frozen finite result

At literal Euclidean Role-permutation symmetry:
[
\mathcal E_{S_4}^{(2)}
=
\operatorname{span}\{E_\delta,E_\perp\}.
]

With explicit ((1,3)) signature and signed signature-preserving hypercubic symmetry:
[
\mathcal E_{Lor}^{(2)}
=
\operatorname{span}\{E_\eta,E_{sp}\}.
]

The extra rays are exact degree-two operators and do not vanish merely under lattice refinement.

## Main question

Suppose a refinement sequence of these finite responses has a nontrivial continuum limit on fixed (T^4).

Can a nonzero coefficient of (E_\perp) or (E_{sp}) survive if the limit must descend to a metric-only (J^2) operator natural under all local diffeomorphisms?

Equivalently, is the extra finite modulus killed by the **correct continuum target type** rather than by an arbitrary finite selector?

## E_perp audit

(E_\perp) uses the preferred vector
[
u=(1,1,1,1)
]
and projector
[
P=I-\frac14uu^T.
]

Determine the corresponding continuum background structure produced by a Role frame.

Construct two frames/grids representing the same Euclidean/local metric jet for which the induced projectors differ.

Show whether a nonzero (E_\perp) coefficient changes the reconstructed response.

If yes, prove that frame erasure forces its continuum coefficient to vanish.

## E_sp audit

(E_{sp}) depends on a preferred time/spatial split.

A Lorentz metric alone does not canonically select one unit timelike vector or one spatial projector.

Use an explicit local Lorentz boost or equivalent local diffeomorphism/frame change to compare two decompositions of the same metric jet.

Determine whether
[
E_{sp}
]
changes while (E_\eta) transforms naturally.

If yes, identify the exact metric-plus-frame datum retained by (E_{sp}).

## Coefficient scaling loophole

Audit sequences
[
c_N E_{extra}
]
with (c_N\to0).

Distinguish:

- frame erasure because the coefficient is forced to zero by a theorem;
- an externally tuned (N)-dependent suppression;
- an extra ray with genuinely nonzero continuum limit.

Do not call arbitrary (c_N\to0) a selector.

## Metric-only naturality criterion

Formulate the result as descent through the forgetful map from framed jets to ordinary metric jets.

A strong positive result would be:

> any convergent degree-two family whose continuum limit is metric-only and locally Diff-natural has zero coefficient on the anisotropic ray, so the surviving principal symbol is proportional to the Einstein/Fierz-Pauli ray.

This is a **conditional continuum selector**, not a finite CORE selector.

## Relation to Lovelock

If the extra rays are eliminated by metric-only local naturality, explain precisely how this interacts with the downstream Navarro theorem.

Do not claim full nonlinear GR from the linearized ray alone.

## Terminal verdict

Return exactly one:

- `A4D-EXTRA-RAYS-ERASED-BY-METRIC-NATURALITY`
- `A4D-EXTRA-RAY-SURVIVES-METRIC-ONLY-LIMIT`
- `A4D-RAY-SELECTOR-REQUIRES-NEW-CONTINUUM-ASSUMPTION`
- `A4D-RAY-CONTINUUM-COMPARISON-MISSING`

## Deliverable

`MEMO_28_A4D_ANISOTROPIC_RAYS_NATURALITY_SELECTOR.md`
