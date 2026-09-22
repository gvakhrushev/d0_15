# E-LIN — Finite Linearized Noether Classification

CONTROL disposition: **ACCEPT AS RESEARCH / A4D-HYPERCUBIC-EXTRA-MODULI-SURVIVE**  
Source memo: `MEMO_25_A4D_LINEARIZED_NOETHER_UNIQUENESS.md`

## Exact finite classification

For
[
X_N=\mathrm{ArchiveRolePhaseGroup}(N),
\qquad L=N+2\ge3,
]
let (D_a) be the centered role differences and let
[
h:X_N\to\operatorname{Sym}^2(Role;\mathbb R).
]

The degree-two monomials (D_aD_b), (a\le b), are linearly independent as finite operators for every (L\ge3). Thus the operator classification is not hiding finite-(L) polynomial identities.

For the continuum-like five-term Euclidean ansatz
[
E_{ab}
=
A\Delta h_{ab}
+B(D_av_b+D_bv_a)
+C D_aD_b t
+D\delta_{ab}q
+F\delta_{ab}\Delta t,
]
gauge nullity, divergence and self-adjointness give exactly
[
(A,B,C,D,F)=c(1,-1,1,1,-1).
]

The same coefficient ray holds for the explicit ((1,3)) contraction with (eta), although the resulting operator is different because the contractions differ.

## Exhaustive owned-symmetry result

The literally owned Role symmetry is (S_4=\mathrm{Perm}(Role)).

The exhaustive Euclidean degree-two coefficient dimensions are:

- before constraints: 59;
- self-adjoint: 38;
- gauge-null only: 13;
- divergence-free only: 13;
- self-adjoint + gauge-null + divergence-free: **2**.

A basis is
[
\boxed{\{E_\delta,E_\perp\}}.
]

Here (E_\delta) is the ordinary four-dimensional Euclidean linearized response, while (E_\perp) is the embedded three-dimensional response on the (S_4)-invariant sum-zero Role subspace
[
u^\perp,\qquad u=(1,1,1,1).
]

Thus after overall scale one genuine selector ratio survives.

## Stronger finite symmetry

If independent coordinate reflections are added so that the finite symmetry becomes
[
B_4=(\mathbb Z_2)^4\rtimes S_4,
]
then the raw degree-two space has dimension 12, the self-adjoint space dimension 9, and the constrained space exactly one ray:
[
E=cE_\delta.
]

This is a mathematically exact conditional uniqueness theorem, but reflection covariance of the new tensor response is not currently an owned selector principle.

## Explicit Lorentz signature

After adding the independent ((+---)) signature datum, the finite signature-preserving signed hypercubic symmetry still leaves a two-dimensional constrained space:
[
\boxed{\operatorname{span}\{E_\eta,E_{\rm sp}\}}.
]

(E_{\rm sp}) is a purely spatial three-dimensional response and is not proportional to the full Lorentzian ray.

Therefore discrete signature-preserving hypercubic symmetry alone does not recover Lorentzian uniqueness.

## Gauge/action relation

With the finite symmetric gradient (K),
[
K^*=-2\,\mathrm{div}.
]

Hence for self-adjoint (E),
[
EK=0\Longleftrightarrow \mathrm{div}E=0.
]

Then
[
S_E[h]=\frac12\langle h,Eh\rangle
]
is exactly gauge invariant.

The metric-gauge principle itself remains a new finite modelling principle; the classification is conditional on adopting it.

## Strategic consequence

Do not add finite symmetry ad hoc merely to select the Einstein-like ray.

The more principled next test is whether the extra rays (E_\perp) and (E_{\rm sp}) necessarily retain a preferred Role/frame structure and therefore fail to descend to a metric-only locally diffeomorphism-natural continuum operator.

Terminal result:
[
\boxed{\texttt{A4D-HYPERCUBIC-EXTRA-MODULI-SURVIVE}}.
]
