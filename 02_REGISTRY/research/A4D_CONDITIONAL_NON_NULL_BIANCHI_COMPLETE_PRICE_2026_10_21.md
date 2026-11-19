# A common nonnull Bianchi I family for the complete continuum price

**Date:** 2026-10-21.  
**Status:** exact full-field solution theorem for the explicitly declared
fixed-measure continuum dictionary below. Identification of that complete
dictionary with the original native D0 carrier remains a separate input;
no exact finite-lattice solution is claimed here.  
**Closure flag:** `GR_closed = false`.

## 1. What the result adds

The [explicit native trace branch](A4D_EXACT_NATIVE_RADIAL_MINIMIZATION_ALL_ORDERS_2026_10_21.md)
gives a small real function \(x=\tau(y)\) satisfying

\[
x r_x(x,y)-y r_y(x,y)=0,
\qquad |y|<2^{-12},\qquad
\operatorname{sgn}\tau(y)=\operatorname{sgn}y.
\tag{1}
\]

A trace solution alone is insufficient to solve the full field equations.
This document supplies an explicit continuum realization in which both
queries are nonzero and constant in spacetime, and every ambient metric,
independent-connection and material equation holds. The same original
metric and material field solve every fixed finite-cap outer valuation
admitted by the stated unit-charge interface.

The family includes anisotropic metrics with both nonzero Ricci curvature
and nonzero Weyl curvature. Its Einstein tensor has the algebraic form of
a pressureless source. This is a statement about the displayed continuum
solution and its derived source; it does not identify that source with
the actual native CAR stress tensor without the original material
dictionary.

The hypotheses preserve the original distinction between a geometric
Palatini density and an **undensitized** material query. In particular,
the coordinate measure in the action is fixed. Replacing this action by
one with a moving volume element outside the nonlinear price changes its
Euler equations and is not covered by this theorem.

## 2. The exact continuum action being solved

Work on an oriented coordinate cylinder
\((t_-,t_+)\times\Omega\), with \(0<t_-<t_+\), fixed measure
\(d^4x\), and Lorentz signature \((+---)\). Variations have compact
support in its interior, or the corresponding original data are held
on a collar. Let \(e^a{}_{\mu}\) be a nondegenerate coframe,
\(\omega^{ab}{}_{\mu}=-\omega^{ba}{}_{\mu}\) an independent Lorentz
connection, and \(\psi\) a complex scalar. Define

\[
g_{\mu\nu}=\eta_{ab}e^a{}_{\mu}e^b{}_{\nu},
\qquad e=\sqrt{|\det g|}>0.
\]

Normalize the Palatini scalar \(R(e,\omega)\) so that the geometric
density is exactly \(eR(e,\omega)\). On a torsion-free connection use

\[
R^\rho{}_{\sigma\mu\nu}
=\partial_\mu\Gamma^\rho_{\nu\sigma}
 -\partial_\nu\Gamma^\rho_{\mu\sigma}
 +\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}
 -\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma},
\quad R_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}.
\tag{2}
\]

Fix \(\eta>0\). The two queries of this theorem are precisely

\[
\boxed{
x=\eta^2 eR(e,\omega),\qquad
y=-\eta^2 q,\qquad
q=g^{\mu\nu}\partial_\mu\overline\psi\,\partial_\nu\psi.
}
\tag{3}
\]

The real expression for \(q\) is equivalently its symmetrized
Hermitian contraction. It contains no factor of \(e\) and no
connection acting on \(\psi\). These specifications are essential;
a spinorial or charged material query can have different independent
connection equations and cannot be substituted without checking them.

Use the same literal native detector as in the trace theorem:

\[
\begin{aligned}
 p&=\varphi^{-1},\quad \varphi=(1+\sqrt5)/2,
       \quad z=2^{-20},\quad \ell(E)=4E(1-E),\\
 B(y)&=4(p+p^2y)^2[1-(p+p^2y)^2],\\
 A_{\rm det}(x,y)&=\ell(p^2(1+x))
       +[1-\ell(p^2(1+x))]B(y),\\
 r(x,y)&=1-[1-zB(y)][1-zA_{\rm det}(x,y)].
\end{aligned}
\tag{4}
\]

For a fixed finite cap \(N\), fixed internal parameters and fixed
actual price data, let

\[
\begin{aligned}
g_N(r)&=\alpha[\kappa-\beta h_\varphi(r)]E_N(\beta r),\\
E_N(t)&=\sum_{j=0}^{N-1}t^j,\\
\alpha&>0,\qquad 0<\beta\le1,\qquad\kappa>53.
\end{aligned}
\tag{5}
\]

These are the explicit unit-charge premises consumed from the prior
compiler packet. Their source-interface attribution has not been
freshly replayed in this environment. Different finite caps may have
different constant parameters satisfying (5).

The continuum action solved here is

\[
\boxed{
S_N[e,\omega,\psi]
 =\int g_N(r(x,y))\,d^4x.
}
\tag{6}
\]

Subtracting the constant \(g_N(r(0,0))\), or adding a term independent
of these fields, does not change the following field equations.
An additional term with a nonzero field source must be retained and
need not vanish on this family. Internal parameters are fixed in this
theorem; their own equations are not being asserted.

## 3. Full source at a spacetime-constant pair of queries

Suppose \(x=x_*\), \(y=y_*\) are spacetime constant and let
\(r_*=r(x_*,y_*)\). At that configuration, for all ambient variations,

\[
\delta S_N
=\eta^2g_N'(r_*)\int
\left[r_x(x_*,y_*)\,\delta(eR)
      -r_y(x_*,y_*)\,\delta q\right]d^4x.
\tag{7}
\]

The coefficients in this first variation are constants in spacetime.
No restriction to homogeneous variations, to trace variations, or to
variations keeping \(x,y\) constant has been made. In particular,
there are no omitted derivatives of these coefficients when integrating
by parts at the displayed background.

The independent Lorentz-connection equation is therefore the ordinary
nondegenerate Palatini equation, multiplied by a nonzero constant:

\[
\epsilon_{abcd}\,D_\omega(e^a\wedge e^b)=0.
\tag{8}
\]

The torsion-free Levi-Civita spin connection satisfies all its 24
component equations. The material query in (3) has no additional
connection source.

After evaluating at that torsion-free connection, the ten independent
inverse-metric equations are

\[
\boxed{
r_x eG_{\mu\nu}
 -r_y\partial_{(\mu}\overline\psi\,
              \partial_{\nu)}\psi=0.
}
\tag{9}
\]

For the real solution below, the second term is simply
\(r_y\partial_\mu\psi\partial_\nu\psi\). There is no
\(-\tfrac12g_{\mu\nu}q\) term in this material variation: that term
would arise from inserting a moving volume density into the material
query, which (3) does not do. The two real material equations are
equivalent to

\[
\boxed{\partial_\mu(g^{\mu\nu}\partial_\nu\psi)=0}
\tag{10}
\]

and its complex conjugate at a constant query pair. The coframe and
connection action is internally Lorentz invariant. With (8) imposed,
the six antisymmetric coframe equations follow from that identity;
together with the ten metric equations, all sixteen coframe equations
are satisfied. Thus (8)--(10) are a test of the full independent
Palatini/coframe/material source, not an ansatz-reduced variational
problem.

## 4. The explicit family

Choose any

\[
-2^{-12}<y_*<0,\qquad x_*=\tau(y_*)<0,
\tag{11}
\]

where \(\tau\) is the explicit native trace root. The trace theorem
establishes \(r_x,r_y>0\), \(z<r_*<2z\), and

\[
x_*r_x=y_*r_y.
\tag{12}
\]

Choose \(t_0>0\), positive constants \(A_1,A_2,A_3\), and real
Kasner exponents \(\nu_1,\nu_2,\nu_3\) obeying

\[
\sum_i\nu_i=1,\qquad \sum_i\nu_i^2=1,
\qquad
\boxed{A_1A_2A_3=-\frac{3x_*}{4\eta^2}>0.}
\tag{13}
\]

Set

\[
\begin{aligned}
a_i(t)&=A_i\,t^{\nu_i}(t+t_0)^{2/3-\nu_i},\\
ds^2&=dt^2-\sum_{i=1}^3a_i(t)^2(dx^i)^2,\\
\psi(t)&=c_\psi t+\psi_0,
\qquad c_\psi=\frac{\sqrt{-y_*}}{\eta},
\end{aligned}
\tag{14}
\]

with \(\psi_0\) a constant complex offset and \(c_\psi\) real.
Take the diagonal coframe \(e^0=dt\), \(e^i=a_i dx^i\), and its
torsion-free spin connection.

> **Conditional-dictionary nonnull continuum theorem.** Under the
> exactly specified action (3)--(6), the fields (13)--(14) solve all
> independent coframe, Lorentz-connection and material equations for
> every fixed finite cap satisfying (5). Both queries are nonzero.
> The same original coframe and material field work for every such
> cap. For the anisotropic choice below, the Ricci and Weyl curvatures
> are both nonzero.

The conditioning is on the continuum dictionary and fixed internal
parameters, not on an unverified cancellation of a residual source.
The proof is the following explicit computation.

## 5. Curvature and every remaining equation

Write

\[
D(t)=t(t+t_0),\qquad A_*=A_1A_2A_3.
\]

The volume density and directional Hubble rates are

\[
e=A_*D,
\qquad
H_i=\frac{\dot a_i}{a_i}
  =\frac{(2/3)t+\nu_i t_0}{D},
\qquad
\Theta=\sum_iH_i=\frac{2t+t_0}{D}.
\tag{15}
\]

The Kasner identities give

\[
\sum_i(H_i-\Theta/3)^2
=\frac{2t_0^2}{3D^2},
\qquad
\sum_{i<j}H_iH_j=\frac4{3D},
\qquad
\dot H_i+\Theta H_i=\frac2{3D}.
\tag{16}
\]

For example, the last equality follows by differentiating the numerator
of \(H_i\) and using \(\Theta=\dot D/D\). These identities yield

\[
R_{00}=\frac2{3D},\qquad
R^i{}_i=-\frac2{3D}\quad(\text{no sum}),
\qquad R=-\frac4{3D},
\tag{17}
\]

and therefore

\[
\boxed{
G_{00}=\frac4{3D},\qquad G_{0i}=0,
\qquad G_{ij}=0.
}
\tag{18}
\]

The original densities are exactly

\[
\eta^2eR=-\frac{4\eta^2A_*}{3}=x_*\ne0,
\qquad
-\eta^2q=-\eta^2c_\psi^2=y_*\ne0.
\tag{19}
\]

Thus the constant-query premise of (7) is verified, rather than imposed
on the variations. The only nontrivial component of (9) is

\[
\begin{aligned}
r_xeG_{00}-r_yc_\psi^2
 &=r_x\frac{4A_*}{3}-r_y\frac{-y_*}{\eta^2}\\
 &=\frac{-x_*r_x+y_*r_y}{\eta^2}=0,
\end{aligned}
\tag{20}
\]

by (12). Every other metric component vanishes individually. The
material equation is

\[
\partial_\mu(g^{\mu\nu}\partial_\nu\psi)
=\partial_t c_\psi=0.
\tag{21}
\]

In particular the time-dependent spatial scale factors do not generate
a hidden volume derivative in (21), because the original material
query and coordinate measure are exactly those in (3), (6).
The imaginary material equation also vanishes. The chosen connection
is torsion free, so (8) already holds.

Finally, the trace theorem proves \(g_1'(r_*)<0\) and
\(g_N'(r_*)>0\) for \(N\ge2\) under (5). Hence the common
prefactor in (7) is nonzero for every admitted fixed finite cap. No
special choice of \(\alpha,\beta,\kappa\) or cap was used in the
metric, material field or cancellation (20).

### 5.1 The lapse equation was not removed

The use of \(g_{00}=1\) in (14) specifies a solution; it is not a
restriction on the action's variations. To check this directly, permit
a lapse \(N(t)\) with \(g_{00}=N^2\) during variation and then
evaluate at \(N=1\). There
\(\delta g^{00}=-2\delta N\) and
\(\delta q=-2c_\psi^2\delta N\). The coefficient of \(\delta N\)
in the full first variation (7) is

\[
2\eta^2g_N'(r_*)\left[-r_xeG_{00}+r_yc_\psi^2\right],
\tag{22}
\]

which vanishes by (20). Thus the Hamiltonian/lapse component is
explicitly included. Fixing the lapse before varying would not
constitute a proof of this theorem.

## 6. Nonzero Weyl curvature, explicitly

Choose

\[
(\nu_1,\nu_2,\nu_3)=(-1/3,2/3,2/3).
\]

Then

\[
a_1=A_1(t+t_0)t^{-1/3},\qquad
a_2=A_2t^{2/3},\qquad a_3=A_3t^{2/3}.
\tag{23}
\]

In the orthonormal coframe of (14), the electric Weyl components in
the curvature convention (2) are

\[
\boxed{
\left(C_{0101},C_{0202},C_{0303}\right)
=\frac{t_0}{9tD}(4,-2,-2).
}
\tag{24}
\]

For instance,
\(C_{0202}=\dot H_2+H_2^2+2/(9D)
=-2/(9t^2)+2/(9D)=-2t_0/(9tD)\).
The magnetic Weyl tensor vanishes for this diagonal Bianchi I metric,
and

\[
C_{abcd}C^{abcd}
=\frac{64t_0^2}{27t^2D^2}>0.
\tag{25}
\]

The Ricci scalar in (17) is also nonzero. Hence this is a genuinely
curved, nonnull, anisotropic family, not a null plane wave or a flat
representative. The limit \(t_0=0\) gives the spatially flat
\(a_i\propto t^{2/3}\) isotropic family and makes the Weyl tensor
vanish, while retaining the nonzero query pair.

Equation (9) can be written for these fields as

\[
G_{\mu\nu}=\rho(t)u_\mu u_\nu,
\qquad u_\mu=(dt)_\mu,
\qquad \rho(t)=\frac4{3D}>0.
\tag{26}
\]

This is the pressureless algebraic form of the derived source. It does
not replace the actual field equations (8)--(10) with a separately
postulated fluid, and no additional fluid field has been introduced.

## 7. Relation to the all-order normal form and to minimality

The [complete-price stationary normal form](A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md)
and its explicit continuation apply to the same nonzero query pair.
The original-frame solution is common to all caps, but the transformed
normal-form coframe is

\[
\widetilde e_N=\sqrt{u_N(y_*)}\,e,
\qquad
u_N(y_*)=
\frac{g_N'(r_*)r_x(x_*,y_*)}
     {g_N'(r_0)r_x(0,0)}.
\tag{27}
\]

This is a positive spacetime-constant scale and may depend on the cap.
The transformed queries are
\(X_N=u_Nx_*\), \(Y_N=y_*/u_N\), preserving \(X_NY_N=x_*y_*\).
One must not confuse the common original metric with the cap-dependent
coframe coordinates of the reduced description.

The solution uses \(y_*<0\). Its radial second variation therefore
has the sign of \(g_N'(r_*)y_*\): it is a radial minimum for \(N=1\)
and a radial maximum for \(N\ge2\). This is a common **stationary**
family, not a common all-cap minimizing execution. No claim is made
about positivity of its remaining physical Hessian.

## 8. Exact remaining interface obligations

The theorem solves a definite continuum action and all its ambient
field equations. To identify it with a native D0 result, one must
establish that the original dictionary has precisely the normalization
and fixed measure in (3), the connection-independent Hermitian scalar
query used here, and the complete price (6) on the same field sector.
If the original matter has an independent spin-connection source,
additional interactions, a different volume density, or moving
normalizations, those sources must be included explicitly.

The clock, preparation, reference, writer and other internal equations
are not solved by freezing their parameters in this continuum theorem.
If their dictionary moves, the full internal source retains its
derivatives just as in the prior complete-price theorem. A fresh
repository interface replay was unavailable for this continuation,
so none of those identifications is reported as completed.

In addition, no lattice discretization or all-mesh identity for this
Bianchi family has been proved here. The result is exact in the
declared continuum model; its finite-cap universality concerns the
complete outer price, not a finite-spacing approximation. The fixed
coordinate measure also does not supply a proof of full
diffeomorphism covariance of the nonlinear complete price.

Subject to these precise limits, the positive extension is explicit:
the same complete-price mechanism supports a nonzero, constant pair
of geometric and material queries with a fully solved anisotropic
Palatini geometry, including the lapse equation, nonzero Ricci and
Weyl curvature, and every fixed finite cap.
