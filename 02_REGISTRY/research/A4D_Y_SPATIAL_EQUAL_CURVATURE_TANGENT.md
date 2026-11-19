# Surviving Y curvature lives on a different character two-torus

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
This is a geometric compatibility theorem at the flat `z=1` Y vacuum. It
sharpens the scope of the complete spatial-equal two-torus symbol theorem;
it is not a nonlinear curved-response terminal.

## Exact intersection at the linearized curvature level

The spatial-equal sector has characters
`lambda=(mu,mu*r,mu*r,mu*r)`. A smooth metric tangent with Fourier support
in this sector depends only on time and `s=x1+x2+x3`. Its Fourier covector
has the form `k=(k0,ks,ks,ks)`. The owner's spatial two-form is

\[
\beta=dx^1\wedge dx^2-dx^1\wedge dx^3+dx^2\wedge dx^3,
\qquad k_a\beta^{ab}=0.
\]

For an arbitrary symmetric metric tangent `q`, the flat linearized
Riemann tensor at such a Fourier covector is, up to the overall Fourier
sign,

\[
R^{(1)}_{abcd}(k,q)=\tfrac12\bigl(
 k_bk_cq_{ad}+k_ak_dq_{bc}-k_ak_cq_{bd}-k_bk_dq_{ac}\bigr).
\]

Every term contains one contraction of `k` with `beta` in each relevant
antisymmetric pair. Consequently

\[
\boxed{\beta^{ab}\beta^{cd}R^{(1)}_{abcd}(k,q)=0}
\]

for **all ten metric components**, every real/complex `k0,ks`, and every
smooth spatial-equal tangent. The constant mode has zero linearized
curvature as well. In the same coefficient convention,
`beta^{ab}beta_{ab}=6` and the double contraction of
`beta tensor beta` is `36`. Thus

\[
\boxed{\{R^{(1)}[q]:q=q(t,s)\}\cap
       \operatorname{span}\{-\beta\otimes\beta\}=\{0\}.}
\]

The already owned **full phase-resolved smooth-source normal-jet**
certificate at `z=1, Q=eta` leaves precisely the curvature direction
`-Y tensor Y = -beta tensor beta` after connection Fredholm, center,
first-slow metric and phase-erasure conditions. Hence a spatial-equal
metric tangent satisfying those same finite normal-jet conditions has
zero first-order curvature. This is a necessary condition for a regular
joint branch bifurcating from the flat Y vacuum; it neither proves that
such a branch exists nor excludes a branch with curvature first appearing
at higher order in its metric amplitude.

## Differential Bianchi classifies the possible curved tangent

There is a converse location theorem for the surviving tensor, independent
of any connection solve. Suppose a smooth periodic metric tangent has
linearized curvature

\[
R^{(1)}[q](x)=-\kappa(x)\,\beta\otimes\beta.
\]

Because `beta` is constant and decomposable, the differential Bianchi
identity says `d kappa wedge beta=0`. Its coordinate components are
`(partial_0 kappa, -partial_0 kappa, partial_0 kappa,
partial_1 kappa+partial_2 kappa+partial_3 kappa)` in the ordered triples
`(012,013,023,123)`. Thus

\[
\partial_0\kappa=0,\qquad
(\partial_1+\partial_2+\partial_3)\kappa=0.
\]

The curvature amplitude depends only on the two transverse coordinates
`x2-x1,x3-x1`; equivalently its character lies on

\[
\boxed{\mathbb T_Y^{(2)}=
 \{(1,a,b,(ab)^{-1}): |a|=|b|=1\}.}
\]

Every component of `R^(1)[q]` is a second derivative of a periodic field,
so its spatial mean is zero. In particular `mean(kappa)=0`. Conversely,
every smooth mean-zero periodic function of those two transverse
coordinates is geometrically realizable at the linearized metric level:
solve the two-dimensional Poisson equation
`Delta_perp phi=3*kappa` and take `q=2*phi*P_perp`. Direct substitution
gives `R^(1)[q]=-kappa*beta tensor beta`, with no other curvature
components. The certificate checks this Fourier identity for a symbolic
transverse covector `(0,a,b,-a-b)` and all tensor slots.

This is a classification of **metric curvature tangents**, not a claim
that the resulting metric and Y connection satisfy the nonlinear Euler
equations. It points to the transverse two-torus as the first physically
relevant full-joint rank surface: unlike the spatial-equal two-torus, it
contains every possible nonzero curvature tangent that survives the owned
normal-jet conditions. It is also closed under Fourier products and
conjugation. A uniform joint inverse there would be useful, but its rank
on the continuous torus is not certified by the existing finite grids.

In particular, the two-torus inverse is a genuine full-joint estimate in
its symmetry class, but that symmetry class has **no nonzero tangent in
the one curved normal-jet direction**. The compatible product-plane
curvature must use independent spatial ratios. This explains why a proof
confined to the spatial-equal Bloch sector cannot establish the task's
fixed-curved comparison-response limit.

## Independent exact warped-metric control

In coordinates `(t,s,u,v)` adapted so that `u,v` span the Y plane, take
the positive periodic scalar warp

\[
g_f=dt^2-ds^2-f(t,s)^2(du^2+dv^2).
\]

Direct Christoffel differentiation gives, in the convention of the
checker,

\[
R_{tutu}=f f_{tt},\qquad R_{tusu}=f f_{ts},\qquad
R_{susu}=f f_{ss},\qquad
R_{uvuv}=-f^2(f_t^2-f_s^2).
\]

If this **geometric** curvature is entirely in the Y plane, all three
mixed components vanish. Since `f>0`, its base Hessian vanishes. A
periodic affine function is constant, so `g_f` is flat. This exact
geometry check applies at arbitrary warp amplitude. The owner normal-jet
compatibility has only been invoked here at the flat Y vacuum; the
geometric statement must not be substituted for a finite-amplitude
joint-Euler classification.

The [exact checker](certificates/a4d_y_spatial_equal_curvature_tangent_check.py)
uses arbitrary symmetric `q`, symbolic `k0,ks`, and literal Christoffel
formulas. It pins the [result](certificates/a4d_y_spatial_equal_curvature_tangent_results.json).
Replay:

```sh
python3 02_REGISTRY/research/certificates/a4d_y_spatial_equal_curvature_tangent_check.py
```

The transverse and full three-ratio physical Bloch ranks, singular/nonuniform center
branches, exact joint continuation on a fixed nonconstant smooth metric,
and the owner-sum normalized response remain open. No terminal or
claim-status change follows from this tangent theorem.
