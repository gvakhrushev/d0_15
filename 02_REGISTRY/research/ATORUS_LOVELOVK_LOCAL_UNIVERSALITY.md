# E-T4NAT — Fixed-Torus Lovelock Local Universality

CONTROL disposition: **ACCEPT AS RESEARCH / T4-FIXED-MANIFOLD-LOVELOCK-SUFFICIENT**  
Source memo: `MEMO_26_ATORUS_LOVELOVK_LOCAL_UNIVERSALITY.md`

## External theorem scope

The audited Navarro formulation fixes one smooth manifold (X), the bundle of pseudo-Riemannian metrics of one fixed signature over (X), and defines a second-order tensor as a bundle morphism
[
E:J^2\operatorname{Met}_{(1,3)}(X)\to S^2T^*X.
]

Naturality is required under diffeomorphisms between open subsets of that same fixed (X).

Therefore D0 does **not** need a natural family on all four-manifolds before invoking the four-dimensional characterization on explicit (T^4).

For (dim X=4), a metric-only smooth second-order locally natural divergence-free symmetric two-tensor lies in the Einstein/cosmological class
[
E=aG+b,g.
]

Genuine second-order dependence excludes the pure (a=0) branch.

## Local jet universality of T4

Every formal Lorentzian metric 2-jet at a point of (T^4) can be realized by a global smooth Lorentz metric on (T^4):

1. choose a constant global Lorentz background with the desired zero-order value;
2. insert the desired first/second derivatives using a local polynomial;
3. multiply by a bump function equal to one near the point;
4. shrink support so the perturbation stays inside the open fixed-signature cone.

Thus torus topology does not restrict the local 2-jets needed by the characterization theorem.

## Critical frame/grid issue

The finite D0 construction carries distinguished Role directions and a periodic grid.

An honest continuum limit may therefore initially have type
[
\widetilde E:
J^2\operatorname{Met}_{(1,3)}(T^4)\times \mathcal F_{grid}
\to S^2T^*T^4.
]

Lovelock/Navarro requires descent to
[
E:
J^2\operatorname{Met}_{(1,3)}(T^4)
\to S^2T^*T^4.
]

The exact frame-erasure condition is:
[
\widetilde E(j^2g,F)=\widetilde E(j^2g,F')
]
for every admissible frames/grids (F,F') over the same metric jet.

Transforming the frame together with the metric proves covariance of a metric-plus-frame theory, not metric-only naturality.

## Strong negative control

A response
[
\widetilde E[g;q_{grid}]
=
G[g]+\alpha R[g]q_{grid}
]
can be local, symmetric, genuinely second order and covariant under grid-preserving transformations, yet fail local-diffeomorphism naturality under a local transformation that does not preserve (q_{grid}).

Thus finite grid symmetry is not a substitute for Navarro naturality.

## Causal firewall

The flat Lorentz torus has closed timelike curves and is not a realistic global causal spacetime.

Those CTCs are irrelevant to the Lovelock/Navarro local jet theorem, whose hypotheses do not require chronology or global hyperbolicity.

Therefore explicit (T^4) is sufficient as a local equation-class testbed but requires a later passport to a globally physical spacetime.

## Critical path

The shortest continuum route is now
[
\text{finite D0}
\to
T^4
\to
\text{all Lorentz metrics on }T^4
\to
\text{metric-only }J^2\text{ response}
\to
\text{local Diff naturality}
\to
\nabla^aE_{ab}=0
\to
\text{Navarro/Lovelock}
\to
aG+bg.
]

Arbitrary-manifold reconstruction is no longer required before local equation-class identification.

Terminal result:
[
\boxed{\texttt{T4-FIXED-MANIFOLD-LOVELOCK-SUFFICIENT}}.
]
