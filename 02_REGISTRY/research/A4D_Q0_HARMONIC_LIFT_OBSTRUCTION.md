# A4D q0 nonlinear harmonic lift: exact second forcing and restricted rays

**Execution:** CONTROL PR #296  
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Status:** exact finite research certificate; no Lean/claim/BOOK promotion  
**Terminal:** `A4D-Q0-HARMONIC-LIFT-SECOND-JET-EXACT`  
**Certificate:** [a4d_q0_harmonic_lift_obstruction_check.py](certificates/a4d_q0_harmonic_lift_obstruction_check.py)

## 1. Result and carrier

The linear identity `C(d) vec_sym(dd^T)=0` does not continue to all metric
amplitude orders merely by repeating `d wedge d=0`. A finite Gram lift
generates a second Fourier harmonic, whose backward difference is

\[
d(z^2)=2d(z)+d(z)\odot d(z).
\]

In the symmetric Gram slice at flat solder, with raw Lorentz links held at
the identity and zero first connection tangent, the complex-component
connection Euler coefficient is exactly

\[
\boxed{
F_2(z)=-\frac{d^T\eta d}{4}\,
C(d\odot d)\operatorname{vec}_{\rm sym}(dd^T).
}
\tag{1}
\]

`F_2` is the coefficient of `eps^2 chi_z^2`; the second derivative is
`N_2=2 F_2`. This is forcing at unchanged links, not a metric stress and not
an obstruction to every possible connection continuation.

Inputs are the accepted star density, middle-degree `G2 star`, and the merged
[metric-null symbol owner](A4D_METRIC_NULL_HESSIAN_COMPLEX.md). The latter
proves rank C=9 and ker C=span{dd^T} for **every** d != 0. Coordinate zeros
of d are not rank-drop walls; the
[topology audit](A4D_KERNEL_LINE_TOPOLOGY_AUDIT.md) remains in force.

All formulae here use the ten covariant symmetric coordinates
`(00,01,02,03,11,12,13,22,23,33)` and `eta=diag(1,-1,-1,-1)`.

## 2. Exact finite Gram lift

First take an auxiliary complex component, not a real physical metric:

\[
Q_\varepsilon(x)=\eta+\varepsilon\chi_z(x)dd^T,
\quad \sigma=d^T\eta d,
\quad R=dd^T\eta.
\]

Since `R^2=sigma R`, set

\[
\Theta=I+a(t)R,\qquad t=\varepsilon\chi_z(x),
\]

\[
a(t)=\frac{t}{1+\sqrt{1+\sigma t}},\qquad
2a+\sigma a^2=t.
\tag{2}
\]

The square root is the analytic branch through 1. Near t=0 this is a
nondegenerate frame and

\[
\Theta\eta\Theta^T=\eta+tdd^T,
\qquad \det\Theta=1+\sigma a.
\tag{3}
\]

For `sigma=0`, (2) is `a=t/2` exactly. Otherwise

\[
a(t)=\sum_{n\ge1}\binom{1/2}{n}\sigma^{n-1}t^n
=\tfrac12t-\tfrac18\sigma t^2+O(t^3).
\tag{4}
\]

This series is convergent in a neighborhood of the flat point. No formal
Taylor truncation is used as an all-order existence theorem.

## 3. Why the area remains linear but the Euler does not

Let `E_r=theta.row(r)^T`, `v=eta d`. Then

\[
E_r=e_r+a d_rv,
\]

\[
E_u\wedge E_v
=e_u\wedge e_v+a v\wedge(d_u e_v-d_v e_u).
\tag{5}
\]

The area term quadratic in a is zero. However a itself contains powers of
the site character. At identity links the differential of
`R(P)=(P-P^-1)/2` is the identity. A based face (r,s) has the literal edge
incidences

\[
(x,r):+1,\quad (x+r,s):+1,\quad
(x+s,r):-1,\quad (x,s):-1.
\]

Consequently an area coefficient at character w contributes factors
`1-w_s^-1` in Role r and `w_r^-1-1` in Role s. This independent edge-Euler
construction reproduces the accepted C(w), including the sign and metric
lift factor 1/2.

Using (4)-(5), the exact nth coefficient on the complex ray is

\[
F_n(z)=2\binom{1/2}{n}\sigma^{n-1}
C(d(z^n))\operatorname{vec}_{\rm sym}(dd^T),\quad n\ge1.
\tag{6}
\]

For n=1 the consumed null identity cancels it. For n=2,

\[
F_2=-\tfrac14\sigma C(d(z^2))\operatorname{vec}_{\rm sym}(dd^T).
\]

Linearity of C and `d(z^2)=2d+d odot d` give (1). The certificate compares
all 24 polynomial entries, not sampled ranks. Nonzero entries of (1) are
homogeneous of degree six in d. This degree is not an identification with
the separate #260 connection-amplitude degree-six gate.

## 4. Exact classification of the auxiliary complex identity-link ray

Assume d != 0.

- If sigma=0, a=t/2. Equation (6) has no n>=2 contributions, so the
  identity-link connection equation vanishes exactly on this complex ray.
- If sigma!=0, the identity-link ray is stationary exactly when all active
  role characters z_r are equal. Zero components d_r are permitted.

Proof of the second statement: stationarity implies F_2=0. If d(z^2)!=0,
the accepted pointwise kernel theorem forces d(z^2) parallel to d; if
d(z^2)=0 the same parallelism minors vanish automatically. Those minors are

\[
d_i d_j(z^2)-d_j d_i(z^2)=d_i d_j(d_j-d_i).
\tag{7}
\]

Thus all nonzero d_i have one common value c, equivalently all active z_i
have one common value. Conversely, write d=c v with v a nonempty 0/1
support vector. For every n,

\[
d(z^n)=((1+c)^n-1)v.
\tag{8}
\]

Linearity of C and its rank-one null identity make every coefficient (6)
zero, including harmonics that return to character one. The convergent lift
(2) is therefore an exact local complex solution of the connection equation.

The proof is all-order because of (8), not because finitely many jets were
tested. The certificate independently verifies the arbitrary harmonic-scalar
identity on all 15 nonempty role supports.

## 5. Real conjugate-pair path and harmonic collisions

The physical path is

\[
Q_\varepsilon(x)=\eta+\varepsilon h(x),\qquad
h=dd^T\chi_z+\overline{dd^T\chi_z}.
\tag{9}
\]

Its symmetric real frame two-jet is

\[
\Theta=I+\tfrac12\varepsilon h\eta
-\tfrac18\varepsilon^2(h\eta)^2+O(\varepsilon^3).
\tag{10}
\]

At second order the constant conjugate-product area has zero identity-link
Euler by the literal periodic incidence cancellation. The remaining forcing is

\[
F_{2,\mathbb R}(x)
=F_2(z)\chi_z^2+\overline{F_2(z)\chi_z^2}.
\tag{11}
\]

If z^2=z^-2, these contributions occupy the **same** character and must be
added before checking vanishing. One cannot classify physical rays by
checking the two complex coefficients separately.

### Quarter-wave example

For z=(i,i,-i,-i), sigma=4i and z^2=(-1,-1,-1,-1). The real matrix

\[
\sigma dd^T+\overline{\sigma dd^T}
\]

has rank two, whereas the kernel generator at z^2 has rank one. Equation
(11) is therefore nonzero. The certificate also evaluates the actual
position-space edge Euler on all four site phases and proves that (11) is
its complete order-two coefficient; its complete order-one coefficient is zero.

The hostile frozen-character substitution C(z) for C(z^2) incorrectly gives
zero and is rejected by this direct comparison.

### Exact physical null example

For z=(-1,1,-1,1), d=(-2,0,-2,0) is real and sigma=0. With chi=+/-1,

\[
\Theta=I+\varepsilon\chi dd^T\eta,
\quad \Theta\eta\Theta^T=\eta+2\varepsilon\chi dd^T,
\quad\det\Theta=1.
\tag{12}
\]

The factor two is required by the path (9); it must not be lost when
writing the frame. The frame and its area have finite polynomial degree, so
the checked zero first and second Euler coefficients exhaust the full
connection Euler. It is exactly stationary at identity links for every real
eps. Congruence by the real invertible frame preserves Lorentz signature
for every real eps.

### General real common-character family

If all active z_r equal z_*, then d=c v and the real metric path is
`eta+f(x) vv^T`, where

\[
f=\varepsilon(c^2\chi+\bar c^2\bar\chi),\qquad
\nu=v^T\eta v.
\]

Use the real branch `b=f/(1+sqrt(1+nu f))` and
`Theta=I+b vv^T eta`. It is valid while `1+nu f>0`; if nu=0 it is valid
for every real amplitude. On a finite periodic character group b has an
exact finite Fourier decomposition into powers of chi. Each such harmonic
has backward difference proportional to v, or zero. Equations (5),(8)
therefore prove exact connection stationarity for the entire family.

The condition sigma=0 on an arbitrary complex d alone does **not** justify
the same physical assertion. For example z=(i,i,i,-i) has sigma=0 but
`dd^T+conjugate(dd^T)` has rank two. The certificate preserves this guard;
it does not claim a nonlinear failure on that real example.

## 6. Raw links, quotient variables and metric partials

The identity in this memo means raw Lorentz links L=I in the declared Gram
slice. It does not mean that the intrinsic quotient coordinate

\[
K_{x,r}=\Theta_x L_{x,r}\Theta_{x+r}^{-1}
\]

is I when Theta varies. Changing between the two coordinate systems changes
a fixed-connection metric partial by a connection-Euler chain-rule term.

At L=I the raw solder partial is zero because every curvature is zero.
This is not a physical off-shell zero-stress theorem. On the exact
connection-stationary families established above, the chain-rule term is
zero too, so the descended metric Euler is zero. Those families are exact
flat-center joint vacua, with the vacuum source fixed.

No analogous metric conclusion is made for the off-shell quarter-wave ray.

## 7. Two separate continuation gates

On a prescribed metric path, choose zero first link tangent and seek
`L=I+eps^2 p_2+...`. Let A_w be the direct physical connection-Euler block
and B_w the direct connection-to-metric block from the same real action.
For every generated harmonic w,

\[
A_w p_2(w)=-F_2(w),\qquad T_2(w)=B_w p_2(w).
\tag{13}
\]

The first equation is a connection-lift gate. The second is its actual
metric-response gate. A nonzero p_2 can have T_2=0.

Because the metric path is fixed, the allowed range in the first gate is
im A_w, not im[A_w|C_w]. The latter would allow changing the prescribed
metric jet. All adjoints/transposes must be transported through the owned
real conjugate-pair convention before replacing B_w by an adjoint notation.

This certificate does **not** solve (13). If the first-order A has a kernel,
nonzero first link tangents can change the higher forcing; (1) must not be
advertised as an obstruction to those different branches.

After an order-two repair, a real order-four character returns to z and
z^-1 at order three. The next selected-branch test is the complete third
forcing projected into the physical cokernels, followed by the metric Euler
of the same corrected branch. It belongs to the existing q0 execution.

## 8. Relation to the Einstein limit

For z=exp(i h k) at fixed k, d=O(h). Equation (1) is O(h^6) for fixed eps
in the **raw** q0 normalization, where q0 itself is O(h^2). This bound is
not uniform under rescaling q0 to a fixed nonzero metric amplitude. It is
not a normalized metric-response estimate after eliminating the connection.

The accepted leading IR identification remains

\[
-C_1(k)^T A_0^{-1}C_1(k)=-\tfrac12K_{G^{(1)}}(k),
\]

owned by [the direct Schur-Einstein check](A4D_SCHUR_EINSTEIN_DIRECT_IDENTIFICATION.md).
The finite harmonic gate (13) and the refinement-uniform smooth stationary
response theorem are different obligations.

The local response target after reducing regular variables to one action
Phi(Q,alpha) remains: on the admissible fixed-source stationary class,
`partial_alpha Phi=0` should imply normalized response agreement with the
designated sheet, with a uniform remainder. The
[reduced-action Ward programme](A4D_REDUCED_ACTION_WARD_STRESS_MECHANISM.md)
provides the appropriate variational framework. An integrated lattice
divergence cancellation alone must not be promoted to pointwise Einstein
response.

## 9. Task and closure map

| Obligation | Disposition after this packet | Existing execution |
|---|---|---|
| General identity-link second forcing, normalization and real harmonic collision | Exact finite certificate passed; bounded CONTROL result ready for acceptance | PR #296 |
| Restricted all-order complex rays and physical common-character rays | Analytic proof plus exact defining algebra and incidence certificate | PR #296 |
| Solved connection-stationary quarter-wave path and its metric stress | Not closed by this packet; preserve existing ownership and source convention | [Draft #285](https://github.com/gvakhrushev/d0_15/pull/285), `EXP-A4D-Q0-STATIONARY-SHEET-STRESS` |
| Full microstructure response decoupling | Remains open; no task retirement or global claim | #240, #260, #275 |

No duplicate worker, new task ID, altered source, or artificial rank-drop
stratum is introduced. The bounded result is recorded here and linked from
the existing programme; acceptance/merge of its CONTROL PR makes it durable.

## 10. Validation

```text
python3 02_REGISTRY/research/certificates/a4d_q0_harmonic_lift_obstruction_check.py
```

Exact checks include the Gram lift, all six complementary areas, 24-entry
independent edge-Euler comparison, degree-six polynomial identity, all six
parallelism minors, arbitrary harmonic scalar on all 15 active supports,
real quarter-wave two-jet at all four phases, real null path with the correct
factor two, constant conjugate-product telescoping, and hostile frozen-character
and sign controls. The certificate writes no release artifacts.

The terminal is bounded to the identities and restricted families proved
above. No general stationary response, unique connection, classical
Kerr-Schild equivalence, or nonlinear Einstein theorem is asserted.
