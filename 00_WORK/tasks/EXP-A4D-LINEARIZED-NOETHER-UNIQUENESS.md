# EXP-A4D-LINEARIZED-NOETHER-UNIQUENESS

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Determine whether the first plausible sitewise 4D finite metric response is **uniquely forced up to scale**, rather than inserted as a new arbitrary formula.

The candidate finite carrier is
[
X_N=\operatorname{ArchiveRolePhaseGroup}(N)
]
with local symmetric metric perturbations
[
h:X_N\to\operatorname{Sym}^2(Role;\mathbb R).
]

Repository edits: **NONE**.

## Read first

- `02_REGISTRY/research/A4D_LOCAL_GRAVITY_RESPONSE_SEED.md`
- `02_REGISTRY/research/LOVELOVK_NATURAL_OPERATOR_PASSPORT.md`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseGroup.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRoleProductLaplacian.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveTensorSeamCrossRoleNoGo.lean`
- `03_FORMALIZATION/D0/Geometry/FiniteSpin2WaveOperator.lean`
- `03_FORMALIZATION/D0/Gravity/A2CompensatorNoether.lean`
- current worker brief `WRK-A4D-SYMROLE-CENTRAL-DIFFERENCE-CARRIER.md`.

## Frozen distinction

The sitewise `Sym²(Role)` field and metric-gauge law are not currently derived from old seam data.

This task may classify a **conditional uniqueness theorem**, but must not silently promote the gauge principle itself to CORE.

## Difference algebra

Use commuting translation-invariant centered role differences (D_a) on the finite periodic group.

Keep the small-cycle guard explicit: at (L=2), (+e_a=-e_a) and the centered first difference degenerates. The nontrivial classification may therefore begin at (L\ge3).

## Main classification problem

Classify the most general linear response
[
E:h\mapsto E[h]
]
with all of the following:

1. translation invariant;
2. local with uniformly bounded radius, restricted first to total difference degree exactly two;
3. output in the same local `Sym²(Role)` fibre;
4. self-adjoint with respect to the uniform finite inner product;
5. invariant/equivariant under the actually owned Role symmetry used in the ansatz;
6. no zeroth-order mass/contact term;
7. nontrivial second-difference principal part.

Do **not** assume continuum (O(4)) isotropy if D0 owns only a smaller hypercubic/permutation symmetry.

Audit the exact invariant tensor algebra of the finite symmetry group.

## Five-term continuum-like ansatz

As a controlled subproblem, classify
[
\begin{aligned}
E_{ab}[h]=;&
A\,\Delta h_{ab}
+B(D_a v_b+D_b v_a)
+C D_aD_b t\\
&+D\,\eta_{ab}q
+F\,\eta_{ab}\Delta t,
\end{aligned}
]
where
[
v_b=D^c h_{cb},\qquad
t=h^c{}_c,\qquad
q=D^cD^d h_{cd}.
]

Carry out both:

- the Euclidean contraction appropriate to the positive role-product parent;
- the signature-((1,3)) contraction if `RoleSign` is added as explicit background data.

Do not assume the two classifications are definitionally identical.

## Gauge / Noether conditions

Define the finite symmetric gradient
[
(K\xi)_{ab}=D_a\xi_b+D_b\xi_a.
]

Test:

[
E[K\xi]=0
quad\text{for every }\xi,
]
and the local divergence identity
[
D^aE_{ab}[h]=0
quad\text{for every symmetric }h.
]

For the five-term ansatz, solve the coefficient equations exactly.

The expected continuum-like one-dimensional ray is only a hypothesis to test, not a permitted assumption.

## Exhaustiveness control

The central research question is whether finite hypercubic symmetry allows additional degree-two terms absent from the continuum (O(4))-covariant ansatz.

Use either:

- invariant-tensor classification;
- Fourier-symbol classification;
- exact representation decomposition;

and determine the full dimension of the admissible operator space before and after gauge/Noether constraints.

A result that proves uniqueness only inside a non-exhaustive ansatz is insufficient.

## Lattice-artifact controls

Test whether operators can vanish in the continuum limit but survive at finite (L).

Separate:

- exact degree-two operators;
- higher-difference lattice artifacts;
- operators proportional to finite identities that disappear only asymptotically.

The first theorem target should remain exact at finite (N).

## Relation to action

If (E) is self-adjoint, define
[
S[h]=\frac12\langle h,E[h]\rangle.
]

Classify when the gauge-null condition implies exact action invariance under
[
h\mapsto h+K\xi.
]

## What would count as a major positive result

A theorem of the form:

[
\begin{gathered}
\text{translation invariance}
+\text{degree-two locality}
+\text{finite isotropy}
+\text{self-adjointness}\\
+E\circ K=0
+\operatorname{div}E=0
\\
\Longrightarrow
E=c\,E_{\rm lin}
\end{gathered}
]

with (c\ne0) for the nontrivial branch.

Then D0 would possess a strong conditional uniqueness statement analogous to the linearized Einstein/Fierz-Pauli structure, while still honestly recording that the local metric-gauge principle itself is a new finite primitive unless separately derived.

## Negative outcomes

If extra hypercubic operator moduli survive, give their exact dimension and basis.

If the gauge principle is inconsistent with the chosen centered-difference algebra, exhibit the exact obstruction.

## Terminal verdict

Return exactly one:

- `A4D-LINEARIZED-EINSTEIN-UNIQUE-CONDITIONAL`
- `A4D-HYPERCUBIC-EXTRA-MODULI-SURVIVE`
- `A4D-DEGREE2-LOCAL-NOETHER-NOGO`
- `A4D-CENTERED-DIFFERENCE-DEGENERACY-OBSTRUCTION`
- `A4D-UNIQUENESS-ANSATZ-NOT-EXHAUSTIVE`

## Required final section

State separately:

- full operator-space dimension before constraints;
- symmetry assumptions actually used;
- gauge-null equations;
- divergence equations;
- self-adjointness equations;
- surviving dimension;
- explicit basis/ray;
- whether the result is Euclidean only or Lorentz-signature compatible;
- whether the metric-gauge principle is owned or new;
- exact next Lean theorem package.

## Deliverable

`MEMO_25_A4D_LINEARIZED_NOETHER_UNIQUENESS.md`
