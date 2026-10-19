# A4D diagonal microstructure connection-stationary slow lift

**Task:** `WRK-A4D-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-SLOW-LIFT`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Owners pinned:** #232 merge `caa1e65087ddf15cda35325189ebfcbf51a56592`; #241 merge `9f9a4da468f89eea4becd931f15c3814b009babd`. Normalization is the single final factor from #226. No discrete Levi-Civita comparison is computed.
**Certificate:** `02_REGISTRY/research/certificates/a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS}}
\]

The #232 microstructure admits an exact order-\(h\) connection-stationary lift on the #241 valued slow background. After that lift the pointwise metric partial has no order-\(h\) term. Its order-\(h^2\) jet is divisible by \(z\), so

\[
h^{-2}\Delta E_Q \to 0
\]

at both \(z_h=h\) and \(z_h=h^2\). This is connection stationarity only. It is not a same-source joint solution.

## 1. Reproduced inputs

The connection is the period-4 family of #232, \(Y=J_{12}-J_{13}+J_{23}\), role-0 links \((U,I,U^{-1},I)\). At standard solder every one of the \(4\times4\times6\) connection components vanishes. The Gram lift is \(H(q)=\tfrac12 q\eta\). On

\[
Q=\eta+h\alpha+h^2 x_0\beta,
\qquad
\alpha=E_{12}+E_{21},\quad
\beta=E_{01}+E_{10},
\]

the uncorrected order-\(h\) metric partial is the #241 vector. Its \((0,1)\) entry is \(-\sigma(p)\,hz/(4+3z^2)\), with \(\sigma=(+1,+1,-1,-1)\).

## 2. Order-\(h\) connection forcing

With links held at \(K(z)\) and solder \(\eta+h\alpha\), the connection Euler is zero at order \(h^0\). The order-\(h\) forcing is supported on two phases and two boosts:

\[
\begin{aligned}
E_K(\text{phase }1,\text{role }0,b_{01}) &= h\,\frac{2z}{3z^2+4},\\
E_K(\text{phase }1,\text{role }0,b_{02}) &= -h\,\frac{2z}{3z^2+4},\\
E_K(\text{phase }3,\text{role }0,b_{01}) &= -h\,\frac{2z}{3z^2+4},\\
E_K(\text{phase }3,\text{role }0,b_{02}) &= h\,\frac{2z}{3z^2+4}.
\end{aligned}
\]

All other phase/role/generator components are zero through order \(h\). The carrier for this bidegree is the \(96\)-dimensional space of phase-uniform link corrections, four phases times four roles times six Lorentz generators. Right multiplication is the tangent convention.

## 3. The lift

The forcing is solved by a correction only on the curved role-0 edges, phases \(0\) and \(2\):

\[
\begin{aligned}
\delta A_0 &= h\Bigl(-\frac{z(z+2)}{3z^2+4}J_{12}-\frac{2z^2}{3z^2+4}J_{23}\Bigr),\\
\delta A_2 &= h\Bigl(\frac{z(z+2)}{3z^2+4}J_{12}-\frac{2z^2}{3z^2+4}J_{13}\Bigr).
\end{aligned}
\]

The \(96\times4\) Jacobian of these modes carries the forcing, and the residual on all \(96\) equations is the zero vector in \(\mathbb Q(z)\). The lift is not obtained by discarding a phase average: every one of the \(96\) components is solved.

## 4. Corrected metric partial

Substitute the lift through the quadratic piece of the exponential, and keep the slow solder through \(h^2\). Every order-\(h\) metric component vanishes at every phase. The order-\(h^2\) jet is

\[
\begin{aligned}
\Delta E_Q[E_{01}] &= -\sigma(p)\,h^2\frac{z^2(z-2)}{2(3z^2+4)^2},\\
\Delta E_Q[E_{02}] &= \sigma(p)\,h^2\frac{z^2(z-2)}{2(3z^2+4)^2},
\end{aligned}
\]

together with slope entries \(\pm\sigma(p)\,h^2 x_0 z/(3z^2+4)\) on \((12,13,22,33)\). Both families are divisible by \(z\). Therefore

\[
h^{-2}\Delta E_Q\Big|_{z=h}\to 0,
\qquad
h^{-2}\Delta E_Q\Big|_{z=h^2}\to 0.
\]

The four-phase sum of each of these expressions is zero as well. The pointwise cancellation is stronger than that average: the order-\(h\) term is zero at each phase, not merely after summation.

At \(z=0\) the lift is zero and every connection component of the identity-link Euler vanishes through \(h^2\). The order-\(h^2\) connection remainder of the lifted family is therefore not a \(z\)-independent source of a normalized finite term at the two scalings.

## 5. Scope

\(E_K=0\) through the order that carried the #241 normalized obstruction. This is not an exact same-source joint solution, and it does not identify a continuum Einstein tensor. No new density, Holst term, torsion constraint, or selector is introduced.

### Full-carrier correction of the next slope coefficient

The first-order lift leaves a definite next coefficient on the same valued
slow profile. In the 96 connection Euler rows, the \(h^2 z x_0\) slope source
is supported only on role 0 at phases 1 and 3:

\[
\begin{array}{c|rrr}
 & J_{12} & J_{13} & J_{23}\\\hline
p=1 & -\tfrac12 & \tfrac12 & 1\\
p=3 & \tfrac12 & -\tfrac12 & -1
\end{array}
\]

The four modes used for the first-order lift do not span this source. The
complete phase × role × Lorentz-link Jacobian has exact rational rank 80; when
the six-component source is appended, its rank remains 80. The exact RREF
therefore supplies a second-order link correction on the full 96-dimensional
carrier, and substituting it makes all 96 \(h^2 z x_0\) Euler coefficients
zero. The checker also verifies that the restricted four-mode augmented rank
increases, so the added roles and link directions are doing real work.

The curvature-only coefficient \(h^2z^2\), computed with the full rational
first-order lift, is also in range. Its only nonzero connection rows are
\(E_K(p=1,\mathrm{role}=0,b_{01})=-1/8\),
\(E_K(p=1,\mathrm{role}=0,b_{02})=1/8\), and the opposite pair at phase 3.
The full-carrier correction is
\[
\delta A_0=\tfrac18 h^2z^2J_{12},\qquad
\delta A_2=-\tfrac18 h^2z^2J_{12}.
\]
Exact substitution cancels all 96 coefficients. This is a second bidegree
coefficient, separate from the \(h^2zx_0\) slope correction above.

The same \(h^2z^2\) coefficient is now tested against the complete metric
source. Here the solder is constant over the period-four cell; the identity-
link flat control has zero in all ten metric Euler rows. Stack all 40 metric
rows with the 96 connection rows, using
the same complete phase × role × Lorentz-link correction carrier. The
136-by-96 coefficient matrix and augmented matrix both have exact rational
rank 88. The correction remains supported only on role 0 at phases 0 and 2,
with coefficients \(+\tfrac18J_{12}\) and \(-\tfrac18J_{12}\). Direct
substitution verifies all 96 finite connection rows and all 40 finite metric
rows vanish at \(h^2z^2\). Thus this coefficient also gives no vacuum
joint-lift obstruction. The calculation does not rebuild the full discrete
#216 smooth comparator even on this flat profile.

An independent direct substitution on the original connection-only
representative also gives zero in all 40 metric rows.

These are isolated formal Taylor coefficients, not an all-orders root. They
do not show that the 16-dimensional Jacobian kernel is gauge, solve higher
connection coefficients, or give a uniformly controlled correction on
expanding grids. In particular they do not discharge the parent requirement
for an exact joint-critical sequence containing #232.

### Joint metric compatibility of the \(h^2 z x_0\) coefficient

The same mixed slope coefficient has now been tested against all ten
symmetric metric probes, with the complete phase × role × Lorentz-link
carrier. Stack the 96 connection equations with the 30 phase differences of
the ten metric outputs. The exact rational coefficient matrix and augmented
matrix both have rank 88, leaving eight homogeneous directions; the source is
compatible. One sparse solution adds only to role-0 links at phases 0 and 2:

\[
\delta K_{0,0}=\tfrac12h^2zx_0(G_{02}-G_{03}),\qquad
\delta K_{0,2}=-\tfrac12h^2zx_0(G_{02}-G_{03}),
\]

where \(G_{02},G_{03}\) are the certificate's symmetric boost generators.
Direct coefficient substitution makes all 96 connection rows and all 40
phase/component metric coefficients zero at \(h^2zx_0\). Thus this
coefficient yields no phase-common metric source after the joint lift; it is
not an obstruction to the #232 continuation. The exact replay is part of
`a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py`.

This is still only the first amplitude coefficient of one local slow jet. It
does not test finite \(z\), actual neighbor-dependent solder data, exact
periodic roots, or a normalized response gap. The separate \(h^2z^2\)
coefficient has its own full joint connection/metric check above, but the
constant-solder cell does not by itself compare against a curved #216 branch.

### First-amplitude joint continuation through \(h^3zx_0\)

The next mixed layer was solved without freezing the earlier kernel
representatives. Write the first-amplitude link tangent as
\[
V_{p,r}=Y_{p,r}+hA_{p,r}+h^2x_0B_{p,r}+h^3x_0C_{p,r},
\]
where the full 96 phase × role × generator entries of each of \(A,B,C\) are
unknown, and take the exact \(z\)-derivative of the original plaquette
operators at \(z=0\). The 388 equations comprise all 96 connection rows at
orders \(h,h^2x_0,h^3x_0\), all 40 metric rows at order \(h\), and the 30
phase differences of the ten metric rows at each of \(h^2x_0,h^3x_0\).
The coefficient matrix and augmented matrix both have exact rational rank
264, leaving 24 free directions. The z-linear formulas are cross-checked
against the full plaquette formulas on all 96 connection and all 40 metric
components for the pinned first lift.

One sparse joint solution uses role-0 links at phases 0 and 2 only:
\[
\begin{aligned}
A_{0,0}&=\tfrac12(-J_{13}+J_{23}),&
A_{2,0}&=-A_{0,0},\\
B_{0,0}&=\tfrac12(G_{02}-G_{03}),&
B_{2,0}&=-B_{0,0},\\
C_{0,0}&=-\tfrac14G_{01},&
C_{2,0}&=-C_{0,0}.
\end{aligned}
\]
All other coefficients in this representative are zero. Thus the #232
first-amplitude slow jet admits joint connection stationarity and phase-common
metric readout through \(h^3x_0\). Keeping all 24 free directions in the
parametric solution shows that both ten-component common metric coefficient
vectors, at \(h^2x_0\) and \(h^3x_0\), are identically zero throughout this
formal solution family. These are the native \(E_Q\) coefficients; this
jet calculation by itself does not identify their difference from the
independently prescribed smooth comparator source; that comparison is below.

This remains a local formal jet: it omits the \(h^2\) value (non-slope)
equations, higher amplitude powers, actual neighbor-dependent solder values,
an exact periodic root, and the normalized same-source response comparison.
The same-profile comparison below finds no response gap at the two displayed
mixed bidegrees. Its local continuum extension has a nonzero Einstein tensor
at finite \(h\), beginning at order \(h^2\), but tends to the flat metric; it
is not a fixed nonconstant refinement family.

### Same-profile comparison with the designated #216 smooth sheet

This comparison keeps the metric input fixed while varying the fast
connection amplitude. The sampled solder is
\[
S_h(x_0)=I+hA+h^2x_0B,
\qquad A=(\alpha\eta/2)^T,\quad B=(\beta\eta/2)^T,
\]
so its Gram metric \(Q_h=S_h^T\eta S_h\) is independent of the microstructure
parameter \(z\). The designated #216 smooth sheet is constructed from this
sampled metric and its smooth derivatives,
\(A_h^{\rm sm}=\sum_{j\ge1}h^jA_j[Q_h]\); its value is not fitted to the
candidate connection. Consequently the complete comparator metric response
\(E_Q(Q_h,K_h^{\rm sm}(Q_h))\) has no positive powers of \(z\), regardless of
the values of its other coefficients.

The pinned 24-dimensional joint #232 calculation gives zero in all ten metric
slots for both \(h^2zx_0\) and \(h^3zx_0\), throughout its full formal solution
family. The #216 comparator has zero coefficients at those same bidegrees by
its independent dependence on \(Q_h\). Therefore the same-profile response
difference is exactly zero there in all ten slots, including after the
owner's \(h^{-2}\) normalization. This local jet is not a nonzero response-gap
witness.

As a separate continuum check on what this shrinking profile represents, set
the physical coordinate \(X=h x_0\) and extend the same coframe as
\(S_h(X)=I+hA+hXB\). Direct symbolic curvature gives
\[
G[g_h]=h^2\operatorname{diag}(0,0,\tfrac14,\tfrac14)
-\tfrac{h^3}{4}(E_{12}+E_{21})+O(h^4)
\]
in the standard covariant component convention. This confirms local
nonflatness at finite \(h\), while the metric tends to \(\eta\); it is an
\(h\)-dependent slow profile, not the fixed nonconstant metric family required
by the #334 terminal. The exact 11-check same-profile comparison is
[`a4d_diagonal_microstructure_same_profile_comparator_check.py`](certificates/a4d_diagonal_microstructure_same_profile_comparator_check.py).
It uses the #216 smooth-sheet theorem as a pinned input and does not compute a
discrete Levi-Civita branch or an exact finite smooth root.

### Curved designated #216 same-source first-slow test

The exact check
[a4d_y232_designated_warp_same_source_firstslow_check.py](certificates/a4d_y232_designated_warp_same_source_firstslow_check.py)
uses the fixed smooth warp
\[
f(y)=1+\frac{\sin(2\pi y)}{100\pi},\qquad
S(y)=\operatorname{diag}(1,1,f(y),f(y)).
\]
At \(y=0\), \(f=1\), \(f'=1/50\), \(f''=0\), and the scalar curvature
is \(1/1250\ne0\). The designated #216 first smooth connection coefficient
is the pinned \(A_1=-f'J_{12}\) on role 2 and \(A_1=-f'J_{13}\) on role 3.
The same comparator is multiplied by the actual finite #232 wave
\(W=(U,I,U^{-1},I)\), where \(U=I+4Y/7+2Y^2/7\) and
\(Y=J_{12}-J_{13}+J_{23}\).

At order \(h\), all 96 connection rows must vanish and all 40 metric rows
must equal the #216 smooth source, whose coefficient at this order is zero.
The unknowns include every phase/role/Lorentz-link correction and both slow
derivatives of the exact flat-center fiber (the Cayley amplitude and
boost-dual center). The complete \(136\times98\) matrix has exact rank 97,
while its source-augmented matrix has rank 98. An exact left-null witness has
support 97 and pairs with the source by \(4105021481/2353113600\ne0\).
Therefore this specified #232 leading state has no regular first-slow
same-source lift on this curved profile.

This is a local formal obstruction, not a theorem excluding every exact
branch. It assumes the pinned finite #232 leading wave and a regular
expansion through order \(h\); nonregular scalings, an order-one change to
the leading state, and exact finite-mesh branches remain open. The #334
terminal is still unresolved: the next useful result must address one of
those remaining branches and its normalized response, or derive the
compulsory physical price that selects the source.

## 6. Validation

Review baseline: `880c8284454b072219f470982963d8dc041957c9`.

```bash
python3 02_REGISTRY/research/certificates/a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py
python3 02_REGISTRY/research/certificates/a4d_diagonal_microstructure_same_profile_comparator_check.py
python3 02_REGISTRY/research/certificates/a4d_y232_designated_warp_same_source_firstslow_check.py
```
