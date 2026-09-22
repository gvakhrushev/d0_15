# WRK-A4D-SYMROLE-CENTRAL-DIFFERENCE-CARRIER

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
REVIEW

## Objective

Build only the finite algebraic infrastructure required by the next 4D local metric-response theorem.

Do **not** define or name an Einstein/gravity response yet.

The target is a sitewise symmetric Role-tensor field over the actual archive role-phase group, together with canonical role translations and centered finite differences.

## Preferred branch

`work/a4d-symrole-central-diff`

## Baseline owners

Read:

- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseGroup.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseProductCarrier.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveRoleProductLaplacian.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveLocalLaplacianVariation.lean`
- `03_FORMALIZATION/D0/Geometry/FiniteSpin2WaveOperator.lean`
- `02_REGISTRY/research/A4D_LOCAL_GRAVITY_RESPONSE_SEED.md`

Reuse existing `Role` and role-phase group definitions. Do not create a parallel four-direction type.

## Required finite types

Define an honest local symmetric Role tensor, e.g.

`SymRoleTensor`

as a matrix
[
A:Role\times Role\to\mathbb R
]
with
[
A^T=A.
]

Define:

[
LocalSymRoleField(N)
=
ArchiveRolePhaseGroup(N)\to SymRoleTensor.
]

Also define, if useful:

[
LocalRoleVector(N)
=
ArchiveRolePhaseGroup(N)\to(Role\to\mathbb R).
]

## Canonical translations

For each (r:Role), define the unit group step
[
e_r(s)=
\begin{cases}
1,&s=r\\
0,&s\ne r
\end{cases}
]
in the role-phase group.

Define:
[
\tau_r^+x=x+e_r,
\qquad
\tau_r^-x=x-e_r.
]

Prove at minimum:

- plus/minus are inverses;
- translations in different roles commute;
- each translation is a permutation/equivalence of the finite carrier.

## Centered difference

Using
[
L=N+2,
]
define a scaled centered difference
[
D_r f(x)
=
\frac{L}{2}
[f(x+e_r)-f(x-e_r)].
]

A technically cleaner equivalent Lean formulation is allowed, including a generic real-vector-space-valued field, if it reduces duplication.

Keep the (L=2) degeneration explicit: do not assert nontriviality there.

## Required algebra

Prove:

1. linearity of each (D_r);
2. commutation:
   [
   D_rD_s=D_sD_r;
   ]
3. constants are annihilated;
4. finite-sum skew-adjointness for scalar fields:
   [
   \sum_x(D_rf)(x)g(x)
   =
   -\sum_xf(x)(D_rg)(x);
   ]
5. componentwise/tensor corollaries needed for later quadratic actions.

The skew-adjoint proof should use exact finite translation/permutation invariance, not an analytic boundary argument.

## Symmetric gradient

Define the local symmetric gradient
[
(K\xi)_{ab}(x)
=
D_a\xi_b(x)+D_b\xi_a(x).
]

Prove that its value is a `SymRoleTensor` at every site.

If cheap, also define the local divergence of a symmetric Role field:
[
(\operatorname{div}h)_b(x)
=
\sum_aD_a h_{ab}(x).
]

No conservation theorem for a gravity response is requested yet.

## Optional useful support

If it is straightforward, provide:

- trace of a `SymRoleTensor`;
- pointwise inner product;
- global finite inner product over sites and Role indices;
- a theorem lifting scalar skew-adjointness to Role-vector/tensor fields.

These will materially simplify the next formalization.

## Firewalls

Do not assert:

- curvature;
- Einstein tensor;
- Fierz-Pauli action;
- Bianchi identity;
- continuum derivative;
- Lorentz covariance;
- Lovelock antecedent;
- physical stress-energy.

The centered differences are finite translation operators only.

Do not identify this new sitewise Sym²(Role) object with the old seam-derived metric; the seam cross-role no-go remains active.

## Integration

This infrastructure should normally be registered only as formal support for the gravity research frontier unless a pre-existing claim literally matches it.

Run:

- target build;
- `lake build D0.All`;
- repository/work/status/generated-view guards;
- no `sorry` / `admit` / project `axiom` / `sorryAx` scan;
- `#print axioms` for capstones.

Move the task to REVIEW, open a PR, and STOP.

Do not advance CAR-parity or certificate-freshness workers.
