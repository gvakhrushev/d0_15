# E-RECON — Typed T4 Response Reconstruction

CONTROL disposition: **ACCEPT AS RESEARCH / T4-TYPED-RECONSTRUCTION-SPEC-REACHED**  
Source memo: `MEMO_29_ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`

## Main result

Pinned Mathlib is sufficient to implement the first fixed-(T^4) comparison layer with actual types and maps.

No proposition-only reconstruction shell is required.

The lowest-debt target is:
[
T^4=(S^1\times S^1)\times(S^1\times S^1)
]
using Mathlib's smooth `Circle` and product manifold instances.

Pointwise symmetric covariant 2-tensors may be represented concretely as symmetric bilinear forms on
[
T_xT^4.
]

A D0 Lorentz metric can mirror the exact data shape of Mathlib's smooth Riemannian bundle metric:
an actual smooth family
[
g_x:T_xT^4\times T_xT^4\to\mathbb R
]
with symmetry, nondegeneracy, and quadratic-form signature
[
(\operatorname{sigPos},\operatorname{sigNeg})=(1,3).
]

## Correct finite sampling type

A literal finite sampler cannot have an ordinary geometric 2-jet as its domain, because it evaluates the metric at nonzero stencil points.

The correct finite map is
[
S_{N,x}^{F}:
\operatorname{SmoothLorentzMetric}(T^4)
\to
\operatorname{RadiusTwoStencil},
]
or the equivalent local metric-germ formulation.

Factorization through an ordinary (J_x^2g) is a later Taylor/consistency theorem.

This distinction is load-bearing and prevents a fake jet wrapper from hiding off-center data.

## Local frame data

A local finite realization should contain actual geometric data:

- a `PartialDiffeomorph` from the model space into (T^4);
- a model-space center;
- an actual linear equivalence
  [
  \mathbb R^{Role}\simeq T4E;
  ]
- a radius-two stencil at mesh
  [
  \varepsilon_N=(N+2)^{-1}.
  ]

The clean periodic no-alias guard for offsets (-2,-1,0,1,2) is
[
N\ge3.
]

## Actual sampling

For a sampled point (z_{N,k}) and chart derivative frame (e_a),
[
S^F_{N,x}g(k)_{ab}
=
g_{\psi_F(z_{N,k})}
((d\psi_F)e_a,(d\psi_F)e_b).
]

This lands in the existing `SymRoleTensor` carrier.

## Actual response reconstruction

Let
[
F_x:\mathbb R^{Role}\simeq T_xT^4
]
be the center frame.

For finite (T\in SymRoleTensor), reconstruct
[
R_x^{F,resp}(T)
=
(F_x^{-1})^*B_T,
]
equivalently
[
R_x^{F,resp}(T)(v,w)
=
\sum_{a,b}T_{ab}
(F_x^{-1}v)^a(F_x^{-1}w)^b.
]

The target can be a concrete symmetric `LinearMap.BilinForm ℝ (TangentSpace T4I x)`.

## Pullback squares

Pinned Mathlib's `PartialDiffeomorph`, `mfderiv` and local derivative equivalence APIs are sufficient to state and prove the first exact functoriality layer:
[
S_N^{\phi^*F}(\phi^*g)=S_N^F(g),
]
[
R_x^{\phi^*F}(T)
=
\phi_x^*R_{\phi(x)}^F(T).
]

These prove metric-plus-frame covariance only.

They do not yet prove frame erasure.

## API status

No blocker was found in:

- smooth fixed (T^4);
- tangent spaces;
- symmetric bilinear target;
- Lorentz-signature metric data;
- local diffeomorphisms;
- pullback derivative equivalences.

No useful pinned manifold `JetBundle` API was found, but this is not a blocker because exact finite sampling should not be defined on an ordinary 2-jet in the first place.

Terminal result:
[
\boxed{\texttt{T4-TYPED-RECONSTRUCTION-SPEC-REACHED}}.
]
