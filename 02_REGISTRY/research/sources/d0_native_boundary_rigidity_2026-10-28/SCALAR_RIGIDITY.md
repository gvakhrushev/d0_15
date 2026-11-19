# Scalar-gradient rigidity from the same strong deformation algebra

28 October 2026. Proposed strengthening of the existing conditional
Einstein--scalar classification in #334. This removes its **quadratic
spatial-gradient** and **nondegenerate spatial coefficient** hypotheses
inside the explicitly separated matter class. It does not derive that
class or native deformation generators from D0.

## Statement and domain

Let the spatial dimension be three and let there be two real scalar fields.
On one local canonical field chart take

    H_m[N] = integral N sqrt(q) [F(phi,nu)+G(phi,X)],
    nu_A = p_A/sqrt(q),
    X_AB = (1/2) q^ij (partial_i phi^A)(partial_j phi^B),
    D_m[xi] = integral xi^i p_A partial_i phi^A.

Here `q` is a positive spatial metric; `F,G` are smooth; there are no
derivatives of momenta, no metric derivatives in this matter term, no
additional canonical pairs, and no kinetic/spatial mixing between `nu`
and `X`. The gravity kinetic term is independent of the matter momenta,
as in the existing theorem. No quadratic hypothesis on either `F` or `G`,
and no invertibility or sign hypothesis on their Hessians, is made.

At each fixed field value `phi`, the strong identity is required for all
independent `nu` in a connected open momentum chart and all `X` in a
connected open subset of the positive definite cone `Sym_2^+`. These
variables must range independently: a constraint surface relating them
would not suffice. All positive definite `X` are realizable as Gram
matrices of two independent gradients in three spatial dimensions.

Suppose the strong matter part of the geometric deformation identity is

    {H_m[N],H_m[M]} = D_m[v],
    v^i=q^ij(N partial_j M-M partial_j N),             (1)

for all compactly supported lapses, before imposing the field equations
or constraints. Then a smooth symmetric invertible matrix `D(phi)` and
functions `V(phi),W(phi)` exist such that, on that chart,

    F(phi,nu) = (1/2) nu^T D(phi)^(-1) nu + V(phi),
    G(phi,X)  = D(phi):X + W(phi).                    (2)

Thus the spatial term is forced to be quadratic in first gradients, and
the momentum term has the reciprocal matrix. The combined scalar
potential is `V+W`. The algebra does not select the sign, field-space
metric, scalar potential or Newton normalization.

## Factor convention

Treat `X` as a symmetric matrix and define the symmetric derivative
matrix `D=partial_X G` by the Frobenius pairing

    dG = D:dX = sum_AB D_AB dX_AB.

In three independent coordinates `(X11,X22,X12)`, this means

    D11=partial_(X11)G,
    D22=partial_(X22)G,
    D12=D21=(1/2)partial_(X12)G.

For `G=D0:X`, this derivative is exactly `D0`. The `1/2` in `X` is
cancelled by the two symmetric variations of its two gradients; hence
there is no extra factor of two in the flux below.

## Proof

Write `u_A=partial F/partial nu_A`. The actual canonical derivatives are

    delta H_m[N]/delta p_A = N u_A,

    delta H_m[N]/delta phi^A
      = N sqrt(q) (F_phiA+G_phiA)
        - partial_i [N sqrt(q) D_AB q^ij partial_j phi^B].

The ultralocal terms cancel when antisymmetrizing the Poisson bracket in
`N,M`. The derivatives of `D`, the metric and the field values inside the
flux also cancel, since they multiply the symmetric product `NM`.
Therefore the full bracket is

    {H_m[N],H_m[M]}
      = integral sqrt(q) v^i (D u)_B partial_i phi^B. (3)

This derivation permits arbitrary smooth `G`; in particular `D` may
initially depend on all entries of `X`.

Equality with (1) gives

    integral sqrt(q) v^i (D u-nu)_B partial_i phi^B = 0

for all lapses. The usual local all-lapse test yields the pointwise
vector identity

    (partial_i phi^B)(D u-nu)_B = 0.                 (4)

For completeness, if a vector density `A^j` obeys
`integral A^j(N partial_j M-M partial_j N)=0` for all compactly
supported `N,M`, integration by parts in `M` yields
`N partial_j A^j+2A^j partial_j N=0`. At a point choose `N=0` with
arbitrary gradient, obtaining `A=0`. The positive metric is invertible,
so the same argument applies to the coefficient of `v`.

On the rank-two gradient chart, the `3 by 2` matrix `partial_i phi^B`
has trivial kernel. Equation (4) is therefore exactly

    D(phi,X) partial_nu F(phi,nu) = nu.              (5)

Differentiate (5) in the independent momentum coordinates:

    D(phi,X) Hess_nu F(phi,nu) = I_2.                (6)

Both factors are square, so (6) **proves** their invertibility. Fix one
momentum point `nu0` in the chart. Since `F` is independent of `X`,

    D(phi,X) = [Hess_nu F(phi,nu0)]^(-1)

for every `X` in the connected allowed chart. Thus `D` is independent of
`X`. Equation (5) then gives `partial_nu F=D^(-1)nu`. Integrating on the
connected momentum chart gives the first formula (2), with no linear
momentum term. Integrating `partial_XG=D` on the connected `X` chart
gives the second formula (2). Smooth dependence on `phi` follows from
smoothness and matrix inversion on the nonsingular chart.

If the supplied smooth Hamiltonian is defined on a neighborhood of the
positive semidefinite cone and (1) holds on all positive definite Gram
matrices, continuity extends (2) to the rank-deficient boundary, including
zero gradients. A theorem tested only on one open positive-definite
subchart does not assert extension to disconnected untested regions.

The metric--matter mixed canonical brackets add no derivative-of-lapse
terms: the metric dependence of the present matter density is
ultralocal. Their remaining `NM` terms cancel. Thus the matter argument
composes directly with the existing gravitational classification.

## Why the Gram form is the complete first-gradient scalar input here

For two gradients in a positive three-dimensional metric and no extra
spatial backgrounds, a locally rotation-invariant scalar can depend on
them only through their Gram matrix. Two independent ordered gradient
pairs with the same Gram matrix are related by an orthogonal map of
their span; extending its action on the one-dimensional normal with the
appropriate sign gives an orientation-preserving three-dimensional
rotation. Thus even specifying spatial orientation adds no independent
pseudoscalar made from only these two gradients. A local Cholesky
representative of every positive definite `X` makes this factorization
smooth. This argument does not cover extra vector fields, higher
derivatives, nonlocal data or preferred spatial backgrounds.

## Necessary scope: mixed kinetic/spatial dependence is a real escape

The separation `F(phi,nu)+G(phi,X)` is essential. For example, on the same
two-scalar canonical carrier define the smooth Hamiltonian density

    Hcal(nu,X)
      = sqrt((1+nu_1^2)(1+2X11)) + (1/2)nu_2^2 + X22,

on `1+2X11>0`. Its Frobenius gradient matrix and momentum derivative are

    D_X Hcal = diag(sqrt((1+nu_1^2)/(1+2X11)), 1),
    partial_nu Hcal
      = (nu_1 sqrt((1+2X11)/(1+nu_1^2)), nu_2).

Their product is exactly `nu`, so the same direct bracket calculation
satisfies (1). This is nonquadratic and nonseparable. It proves that
the new rigidity is a theorem of the declared separated class; it is not
a classification of all diffeomorphism-invariant matter or an automatic
derivation of the matter class from D0.

## Actual gain from the new result

The 28 October classifier previously assumed quadratic scalar spatial
gradients with an invertible matrix. Both assumptions can now be removed
and replaced by smooth local first-gradient dependence plus the already
declared separation of kinetic and spatial variables. The same strong
algebra forces both the quadratic form and invertibility. The native
symplectic/lapse/field-map/refinement obligations remain exactly where
they were; they are not claimed by the algebraic calculation.
