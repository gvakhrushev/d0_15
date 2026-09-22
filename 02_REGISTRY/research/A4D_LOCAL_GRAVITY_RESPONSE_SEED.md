# E-SEED — 4D Local Finite Gravity Response Seed

CONTROL disposition: **ACCEPT AS RESEARCH / A4D-LOCAL-RESPONSE-TENSOR-FIBRE-MISSING**  
Source memo: `MEMO_23_A4D_LOCAL_GRAVITY_RESPONSE_SEED.md`

## Post-memo truth update

The memo's first literal implementation gap has now been closed by PR #51.

`D0-ARCHIVE-LOCAL-LAPLACIAN-VARIATION-ISOMORPHISM-001` is again honestly CORE-FORMALIZED: Lean owns the explicit undirected nearest-neighbour edge conductance space, the forward linear map to symmetric row-sum-zero supported local Laplacian variations, the recovery map, two-sided inverse theorems, and an actual `LinearEquiv`.

Therefore the remaining terminal verdict is now cleaner:

[
\boxed{\texttt{A4D-LOCAL-RESPONSE-TENSOR-FIBRE-MISSING}}.
]

## Owned positive base

D0 owns:

- (X_N=\mathrm{ArchiveRolePhasePoint}(N)) with (|X_N|=(N+2)^4);
- the role-phase group shadow ((\mathbb Z/L\mathbb Z)^{Role});
- directional role translations and scalar role-product Laplacians;
- the internal metric scale (L^2=(N+2)^2);
- a literal local conductance/local-Laplacian variation equivalence.

## Why existing response candidates still fail

### (2L)

One matrix owns response identity, symmetry, row sums and nontriviality. But site-site symmetry is not local Role-tensor symmetry, row sums are not a tensor divergence, and (E[L]=2L) has no second finite differences of a sitewise metric tensor field.

### Raw weighted A2

It has action provenance, but the accepted finite divergence obstruction remains active. It also lives on the wrong carrier and contains extra weight data.

### A1 compensator

It has a genuine finite action and Ward identity, but (B_+) is the unsigned Weyl/trace operator rather than tensor divergence, and eliminating the compensator is a global solve.

### Conserved archive stress projection

It is the strongest same-object symmetric/conserved variational precursor, but it is a 1D phase object and the projection is generically global.

### Seam-derived 4D metric

The existing seam-to-product route is terminally restricted by
`D0-ARCHIVE-TENSOR-SEAM-CROSS-ROLE-CURVATURE-NOGO-001`:
[
g_{rr}(x)=m(x_r),\qquad \Delta_s g_{rr}=0\quad(s\ne r).
]
Hence it cannot supply general cross-role metric variation.

## Missing finite object

The first structural object now missing is a sitewise local symmetric Role tensor:
[
m_N:X_N\to\operatorname{Sym}^2(Role;\mathbb R).
]

A viable repair blueprint uses commuting centered role differences (D_a) and a radius-two linearized metric response of the schematic form
[
E_{ab}[h]
=
\frac12[
\partial_c\partial_a h_{cb}
+\partial_c\partial_b h_{ca}
-\Delta h_{ab}
-\partial_a\partial_b h
-\delta_{ab}(\partial_c\partial_d h_{cd}-\Delta h)
]
]
with every derivative replaced by exact finite centered differences.

The memo shows algebraically that such a finite operator can have:

- local Role-index symmetry;
- exact finite gauge nullity (E[K\xi]=0);
- exact local divergence identity;
- a self-adjoint quadratic action;
- radius at most two;
- nontrivial second metric differences.

But the local Sym²(Role) field and the finite metric-gauge principle are **new modelling primitives**, not presently selected by CORE.

## Next question

The correct next expensive question is not merely “can we write this formula?” but:

> Is this linearized response uniquely forced up to overall scale by translation invariance, degree-two locality, Role isotropy, self-adjointness and finite metric-gauge/Noether identities?

That is the purpose of `EXP-A4D-LINEARIZED-NOETHER-UNIQUENESS`.
