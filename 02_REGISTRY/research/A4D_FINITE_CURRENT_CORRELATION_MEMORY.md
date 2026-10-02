# A4D finite current / correlation memory in matrix-link coordinates

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Input head: \`d7730d1d25619ee3a46bb205c8d0c7dbdc75f1e4\`.  
Status: exact algebraic reduction of the candidate space; not yet a task terminal.

## 1. Why this note

The current task must not become an enumeration of Bloch points or an
unbounded Taylor hierarchy.  Both are avoidable.

The literal naked-star action is finite-stencil and polynomial in the actual
Lorentz link matrices.  The apparent infinite nonlinear hierarchy in
relative-log coordinates is a coordinate artifact of the exponential map.
Using matrix-link increments gives an exact finite-degree problem.

This note records two consequences:

1. the connection Euler equation is exactly the adjoint of a shared-face
   incidence current;
2. after recentering at a fixed comparator, every connection Euler row and
   every metric-response row is a polynomial of degree at most four in the
   matrix increments.

Hence the response/homogenization problem admits a finite correlation-memory
quotient.  At quadratic order the already certified 21-term Laurent support
shows that only 21 two-point matrix moments are visible.

## 2. Exact face momentum and shared-link incidence current

For an oriented based face f=(x;r,s), r<s, write

\[
P_f=g_0g_1g_2g_3
=L_{x,r}L_{x+e_r,s}L_{x+e_s,r}^{-1}L_{x,s}^{-1}
\]

and

\[
\ell_f(S,L)=\langle W_f(S_x),\mathcal R(P_f)\rangle,
\qquad
\mathcal R(P)=\frac12(P-P^{-1}),
\]

where the pairing is the literal star/bivector pairing already owned by the
action.

Define the right plaquette momentum \(\Pi_f\in\mathfrak{so}(1,3)^*\) by

\[
\langle\Pi_f,X\rangle
:=D_P\ell_f[P_fX].
\tag{1}
\]

Let \(T_j=g_{j+1}\cdots g_3\).  If a positive factor \(g_j=L\) is varied by
\(L\mapsto L e^{\epsilon X}\), then

\[
\delta P_f=P_f\,\operatorname{Ad}_{T_j^{-1}}X.
\tag{2}
\]

If \(g_j=L^{-1}\) comes from the same right variation of the underlying link,
then
\[
\delta g_j=-Xg_j,\qquad
\delta P_f=-P_f\,\operatorname{Ad}_{(g_jT_j)^{-1}}X.
\tag{3}
\]

Therefore every literal link Euler covector is exactly

\[
\boxed{
E_K(x,r)=
\sum_{f\ni(x,r)}
\sigma(f,x,r)\,
\operatorname{Ad}^*_{\mathcal T(f,x,r)}\Pi_f .
}
\tag{4}
\]

The sign and tail transport \(\mathcal T\) are the ones in (2)--(3).
Equation (4) is simply the explicit current form of the previously owned
Jacobian-adjoint first variation.  No continuum covariant derivative is being
inserted.

At identity links all tail transports are identity, so (4) reduces to the
ordinary cellular codifferential of the face momenta,

\[
E_K(x,r)=\sum_{s\ne r}
\bigl(\Pi_{rs}(x)-\Pi_{rs}(x-e_s)\bigr)
\tag{5}
\]

with the standard orientation convention.  The temporal-B flux identity
already owned in this PR is an exact nonlinear abelian reduction of (4).

For noncommuting links the transports in (4) depend on the field itself.
Consequently one must not replace (4) globally by an ordinary fixed-coefficient
Hodge divergence.  In particular a naive quotient by ordinary curls is not
licensed away from the flat/commuting reductions.

## 3. The exact polynomial-degree bound

The decisive simplification is the Lorentz inverse:

\[
L^{-1}=\eta L^T\eta .
\tag{6}
\]

Thus both a positive and an inverse face factor are **linear** in the matrix
entries of the underlying Lorentz link.  Every based plaquette and its inverse
are products of four such factors.  Hence, at fixed solder,

\[
\mathcal R(P_f)
\]

is a polynomial of degree at most four in the link-matrix entries.

The metric Euler/readout changes only the complementary solder weight and
therefore has the same link degree.  A right-trivialized connection variation
replaces one factor by either \(LX\) or \(-XL^{-1}\), which is again linear
in that link.  Therefore

\[
\boxed{
\deg_L E_K\le4,\qquad
\deg_L \Xi\le4 .
}
\tag{7}
\]

This is an exact statement about the literal finite action, not a Taylor
estimate.

Now fix any comparator \(K^*\) and use relative Lorentz matrices

\[
R_{x,r}=(K^*_{x,r})^{-1}K_{x,r}=I+U_{x,r}.
\tag{8}
\]

The exact Lorentz constraint is only quadratic,

\[
U^T\eta+\eta U+U^T\eta U=0.
\tag{9}
\]

Because
\[
R^{-1}=\eta R^T\eta=I+\eta U^T\eta,
\]
every positive or inverse candidate factor is affine-linear in \(U\).
Consequently (7) remains true after recentering:

\[
\boxed{
E_K(K^*(I+U))=\sum_{d=0}^4 F^{(d)}[U^{\otimes d}],
\qquad
\Xi(K^*(I+U))=\sum_{d=0}^4 G^{(d)}[U^{\otimes d}]
}
\tag{10}
\]

with **no terms of degree five or higher**.

The coefficients in (10) may depend on the sampled solder and on \(K^*\), but
the degree and stencil do not depend on the lattice size.

This is the key architecture correction: fifth-, sixth-, and higher nonlinear
microstructure gates are not separate physical obligations in matrix-link
coordinates.  Any such terms seen in logarithmic coordinates are
reparameterizations of the finite quartic system (10).

## 4. Exact finite local correlation memory

Each row of (10) sees only the finitely many links in the incident face star.
For a connection row, six incident faces contribute; for a metric row, six
based faces contribute.  Thus there is one finite link-slot set
\(\mathcal S_{\rm loc}\), independent of L, such that all candidate dependence
is through products

\[
U_{\ell_1}\cdots U_{\ell_d},
\qquad
1\le d\le4,\qquad
\ell_j\in\mathcal S_{\rm loc}.
\tag{11}
\]

For any declared averaging/testing operator P, define the finite correlation
memory

\[
\mathfrak C_P(U)
=
\left\{
P\!\left[
(U_{\ell_1})_{a_1b_1}\cdots
(U_{\ell_d})_{a_db_d}
\right]:
1\le d\le4,\ \ell_j\in\mathcal S_{\rm loc}
\right\}.
\tag{12}
\]

Then there are fixed coefficient maps, determined by \(S,K^*\), such that

\[
P E_K=\mathcal F_{S,K^*}(\mathfrak C_P(U)),
\qquad
P\Xi=\mathcal G_{S,K^*}(\mathfrak C_P(U)).
\tag{13}
\]

Therefore two arbitrary microscopic fields with the same memory (12) have
the same averaged connection equations and the same averaged metric response,
regardless of how many different Fourier carriers, sign patterns, envelopes,
or pointwise representatives realize those moments.

Equation (13) is the finite M1-style quotient that the frequency census was
missing.  It is sufficient, not asserted coarsest.

The realizable image of (12) still has constraints:

* the exact quadratic Lorentz relations (9);
* shared-link consistency;
* positivity/Gram constraints on correlation matrices;
* the polynomial Euler equations obtained from (10).

All of these have degree bounded independently of L.

## 5. The quadratic continuum memory is only 21 matrix moments

For the O(h) continuum/microstructure scaling, the leading weak response uses
only the degree-two part.  The literal physical joint symbol has already been
certified to have the exact Laurent support

\[
\Sigma_{21}
=
\{0\}
\cup\{\pm e_r:0\le r<4\}
\cup\{e_r-e_s:r\ne s\},
\qquad |\Sigma_{21}|=21.
\tag{14}
\]

A coframe derivative changes the coefficient matrices but not these link
shifts.  If \(\mu_x(dz)\) is the matrix-valued defect measure of the normalized
leading field, define

\[
M_d(x)=\int_{\mathbb T^4} z^d\,d\mu_x(z),
\qquad d\in\Sigma_{21}.
\tag{15}
\]

Writing
\[
D_QH_g(z)[q]=\sum_{d\in\Sigma_{21}}R_d(g,q)z^d,
\]
the entire quadratic response defect is exactly

\[
\boxed{
\mathcal T_\mu(x)[q]
=
\frac12\sum_{d\in\Sigma_{21}}
\operatorname{tr}\!\left(R_d(g(x),q)M_d(x)\right).
}
\tag{16}
\]

Thus the full frequency measure is **not** response memory.  For the
quadratic continuum readout, its 21 matrix moments are sufficient.

The exact joint support equations can likewise be tested against Laurent
monomials.  One multiplication by the 21-term symbol enlarges the required
shift set only to

\[
\Sigma_{21}+\Sigma_{21},
\]

which contains exactly 131 four-dimensional shifts.  Hence all degree-one
moment consequences of the frozen joint equations that can constrain (16)
live in a 131-shift truncated matrix-moment system, not in an unclassified
continuum of frequencies.

This does not say that those 131 constraints are sufficient for nonlinear
realizability; it says that a positive proof may safely work on this larger
finite relaxation.  If the response functional vanishes on the relaxation,
it vanishes on every realizable defect measure without a torus census.

## 6. Why a single harmonic flux is not enough

The laser/transport analogy is useful only after identifying the correct
carried data.  A single conserved scalar flux is too coarse.

On the exact flat coupled-boost family, changing \(t\) to \(-t\) reverses the
odd plaquette coefficient and hence reverses the packed metric memory

\[
\Xi(-t)=-\Xi(t).
\]

The temporal-B transport factor in the exact current identity is instead

\[
c(t)=\sqrt{1+3z(t)^2},
\]

so it is unchanged under \(t\mapsto-t\).  Thus the scalar conserved B-flux
cannot by itself be a response-sufficient quotient.  The current equation
controls realizability; the odd projected curvature memory \(\Xi\) controls
the metric observation.

The correct finite object is therefore not "harmonic current alone" but the
joint finite constitutive memory (12), with (4) imposing conservation and
\(\Xi\) selecting the observable projection.

## 7. Consequence for the raw owner-sum target

In smooth/volume-normalized testing, \(U=O(h)\) makes the cubic and quartic
parts of (10) lower order after the usual h^-2 normalization.  This recovers
the quadratic defect-measure law and its 21-moment quotient.

The unweighted owner-sum target is much stronger.  The L^4 site count can keep
degree-three and degree-four contributions relevant even when they are
pointwise small.  However the finite-degree theorem still removes the
open-ended proof ladder:

\[
\boxed{
\text{for the exact matrix-link theory only degrees }2,3,4
\text{ can carry a post-linear microstructure defect.}
}
\tag{17}
\]

There is no independent degree-five or higher gate to discover.

Accordingly the remaining strong-topology problem can be organized as three
finite moment layers:

1. quadratic two-point correlation;
2. cubic three-point correlation;
3. quartic four-point correlation;

together with the exact quadratic Lorentz constraints and shared-link
incidence.  These layers should be solved simultaneously as one finite
polynomial realizability problem, not sequentially promoted into new
"theory levels".

## 8. Finite dual-certificate target

A positive non-census closure can now be stated algebraically.

Let \(\mathcal M_{\le4}(S,K^*)\) be the finite set of correlation memories
(12) satisfying all exact moment consequences of

\[
E_K=0,\qquad
(I-P)\Xi=0,
\]

the Lorentz relations (9), shared-link consistency, and the declared source
equations.  Let \(\mathcal D\) be the linear readout extracting the response
difference from those moments.

The desired finite certificate is

\[
\boxed{
\mathcal D(M)=0
\quad\text{for every }M\in\mathcal M_{\le4}(S,K^*).
}
\tag{18}
\]

It is enough to prove (18) by polynomial-ideal, real-radical,
sum-of-squares/PSD moment, or exact elimination identities.  Such a
certificate quantifies over every microscopic realization at once.

A negative terminal instead requires one point of the same finite moment
system that is exactified to shared Lorentz links and has \(\mathcal D(M)\ne0\)
under a source fixed before the field.

This is the appropriate replacement for further Bloch-ratio enumeration.

## 9. Scope

The degree-four theorem is exact for the naked-star action in Lorentz matrix
variables.  The 21-moment statement concerns the quadratic continuum
readout.  The full strong owner-sum closure still requires controlling the
finite cubic and quartic moment layers.

No ordinary Hodge quotient of the nonlinear transported current is claimed;
the field-dependent adjoint transports in (4) are retained.  No connection
uniqueness, spectral filter, new action, selector, BOOK/CORE promotion or
task-level terminal is asserted.

Verdicts:

\[
\boxed{\texttt{A4D-CONNECTION-EULER-IS-EXACT-SHARED-FACE-CURRENT}}
\]

\[
\boxed{\texttt{A4D-MATRIX-LINK-NONLINEARITY-TERMINATES-AT-DEGREE-FOUR}}
\]

\[
\boxed{\texttt{A4D-QUADRATIC-RESPONSE-HAS-21-MOMENT-M1-QUOTIENT}}
\]

The parent response-decoupling task remains open only at the finite
degree-2/3/4 correlation realizability identity (18), not at an unlimited
space of new nonlinear proof levels.
