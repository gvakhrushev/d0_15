# Nonregular quarter fields: exact isolation on a fixed curved one-coordinate background

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `15b4e8d7481552bc174da003339ffdc1ba094f7a`.
Authoritative contract: 2026-10-01 v2, with Targets D and U separate.
The action, Lorentz quotient and independently prescribed source convention
are unchanged. This is a research-level analytic theorem with exact finite
inputs, not a Lean/BOOK/CORE promotion or the task-level terminal.

The regular h-expansion assumption in the preceding warped-quarter result
can be removed. The proof uses the already owned **all-frequency** estimate,
exact fast-parity equivariance, and two differently normalized weak limits.
It does not assume a smooth envelope or an asymptotic expansion of a candidate.

## 1. Statement and exact solution class

There is an epsilon0>0 such that the following holds. Fix a smooth positive
nonconstant one-periodic f with `||f-1||_infinity<epsilon0`, independently of
h, and set

\[
S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\qquad g=S^T\eta S,
\quad h=1/L,\quad L\in4\mathbb N.
\]

Shrink epsilon0 to lie in the coframe neighborhoods of the continuous
four-phase circle estimate, the quadratic/first-slow transversality theorem,
and the exact designated continuation. Its value is existential; the
finite epsilon=1/50 numerical warp has not been certified inside this new
neighborhood.

Let K_h^*(n), n=x1, be the **exact**, phase-common designated connection from
[A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md).
It obeys every full-carrier connection Euler equation, and differs from
the #216 comparator by O(h^infinity). It also has

\[
K_h^*(n)=I+hB(f(hn),f'(hn))+O(h^2)
\tag{1}
\]

uniformly, with the same first smooth coefficient used in the literal
shared-link certificate. This follows from the #216 expansion and the
super-algebraically small exact correction.

Allow **arbitrary lattice fields**

\[
K_h(n,p)=K_h^*(n)\exp u_h(n,p),\qquad
p=(x_0+x_1+x_2+x_3)\bmod4.
\]

There are 96 real independent Lorentz link coordinates at each n. No
restriction on n frequencies, normalized derivatives, expansions, fractional
powers, or the dependence of these coordinates on L is imposed. All eight
real quarter-center coordinates are retained. A role-1 shift changes
`(n,p)` to `(n+1,p+1)`; the other role shifts change p only. This is the
same nonlinear invariant sector whose every frozen frequency was covered
by the continuous circle certificate.

Require

\[
E_K(Q_h,K_h)=0,\qquad \Pi_{p\ne0}E_Q(Q_h,K_h)=0.
\tag{2}
\]

The second equation is the thirty nonconstant-phase metric rows. It is a
necessary condition for any independently prescribed source depending
only on y1. The phase-common metric response is **not** specified in (2),
so response agreement below is not a comparison of two solutions to an
already identical full source equation.

**Theorem (exact shrinking-neighborhood isolation).** There are constants
c_g>0 and h_g>0, depending on this fixed metric, such that for h<h_g,

\[
\boxed{(2),\quad \|u_h\|_\infty\le c_g\sqrt h
\quad\Longrightarrow\quad u_h=0.}\tag{3}
\]

In particular, every exact family in this sector with
`||log((K_h^sm)^(-1)K_h)||_infinity<=C h` equals K_h^* for all sufficiently
fine meshes. The designated correction and the bounded BCH change of
coordinates place such a family inside (3). Hence, in the full L^4
unweighted owner sum,

\[
\boxed{h^{-2}\|E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\rm sm})\|_1
=O(h^\infty).}\tag{4}
\]

The owner reconstruction therefore gives `-G[g]/2+O(h)` for every such
family. Exact designated existence and the scoped extra-center response
question are both settled in this class. The theorem does not assert
existence of a solution for an arbitrary prescribed phase-common source.

## 2. Linear input on the actual background

Define the joint map, in relative logarithm coordinates,

\[
F_h(u)=\bigl(E_K(Q_h,K_h^*e^u),\Pi_{p\ne0}E_Q(Q_h,K_h^*e^u)\bigr),
\qquad H_h=DF_h(0).
\]

Crucially, **F_h(0)=0 exactly**. This uses the previously constructed
connection root and its phase-common symmetry. A merely super-algebraic
residual would not suffice when dividing by the square of an arbitrarily
small candidate amplitude.

The background is independent of p, so H_h preserves every fast harmonic.
Use the involution `(Tu)(n,p)=u(n,p+2)` and write

\[
u=e+o,\quad Te=e,\quad To=-o,\qquad
 o=N_f a+B_\perp w.\tag{5}
\]

Here e consists of the phase-common and alternating channels (48 real
coordinates), a of the four complex quarter amplitudes (eight real), and
w of their twenty complex normal coordinates. The transported center map
N_f and its complement have uniformly bounded coordinate changes. The
actual envelope difference is `Delta a(n)=a(n+1)-a(n)`.

The continuous-circle owner
[A4D_IDENTITY_FOURPHASE_CIRCLE_CONTROL.md](A4D_IDENTITY_FOURPHASE_CIRCLE_CONTROL.md)
proves, on the varying comparator and uniformly in the period,

\[
\|e\|_\infty\le C_g\|H_{h,e}e\|_\infty,\qquad
\|w\|_\infty+\|\Delta a\|_\infty
\le C_g(\|H_{h,o}o\|_\infty+h\|o\|_\infty).
\tag{6}
\]

The first bound is the center-free specialization with its h term
absorbed. Its operator is rectangular joint, not an invented
connection-only inverse of the alternating channel. Replacing the
comparator by K_h^* changes the derivative by O(h^infinity) and preserves
(6). The relative-log coordinates used here are the same coordinates as
in the first-slow certificate; uniformly bounded near-identity coordinate
changes preserve these estimates.

All longitudinal frequencies and all literal neighboring coframes are
already included in (6). No smooth-frequency cutoff is introduced here.

## 3. Parity supplies the nonlinear bounds with no regularity assumption

Translation p->p+2 commutes with every incident-face operation and with
phase projection. Thus F_h is equivariant under T, exactly. For the even
and odd output projections,

\[
F_{h,e}(e,-o)=F_{h,e}(e,o),\qquad
F_{h,o}(e,-o)=-F_{h,o}(e,o).
\]

The exponential, inverse, face products and Gram readout are analytic on
a fixed small log/coframe chart. Each row uses a uniformly bounded number
of neighboring inputs. Taylor derivative bounds in the sup norm are
therefore independent of L. For some C_g and a fixed small log radius,

\[
\begin{aligned}
F_{h,e}(e,o)&=H_{h,e}e+R_{h,e}(e,o),&
\|R_{h,e}\|_\infty&\le C_g(\|e\|_\infty^2+\|o\|_\infty^2),\\
F_{h,o}(e,o)&=H_{h,o}o+R_{h,o}(e,o),&
\|R_{h,o}\|_\infty&\le C_g(\|e\|_\infty\|o\|_\infty+\|o\|_\infty^3).
\end{aligned}\tag{7}
\]

The absence of a pure o-squared term in the odd row is an exact parity
statement; it is the essential gain over a norm-only quadratic estimate.
Mixed terms involve actual neighboring e and o values and satisfy the
same bounds. Applying (6) to an exact root and absorbing the e-squared
term gives, with A=||o||_infinity,

\[
\boxed{\|e\|_\infty\le C_g A^2,\qquad
\|w\|_\infty+\|\Delta a\|_\infty
\le C_g(hA+A^3).}\tag{8}
\]

If A=0, the same estimate and smallness imply e=0. Thus every nonzero
small root has A>0. These are nonlinear, refinement-uniform estimates
for arbitrary arrays. No derivative estimate for e or w is asserted.

## 4. A hypothetical sub-square-root branch has a nonzero compact limit

First exclude any sequence of nonzero exact roots with

\[
h_j\longrightarrow0,\qquad \|u_{h_j}\|_\infty/\sqrt{h_j}\longrightarrow0.
\tag{9}
\]

By (8), A_j>0 and `A_j^2/h_j->0`. Normalize the center amplitudes by
`c_j=a_j/A_j` and interpolate them linearly on the envelope circle.
Their neighboring slopes obey

\[
\|\Delta c_j/h_j\|_\infty
\le C_g(1+A_j^2/h_j),\qquad \|c_j\|_\infty\le C_g.
\tag{10}
\]

Also `||w_j/A_j||_infinity<=C_g(h_j+A_j^2)->0`. Since
`||o_j/A_j||_infinity=1` and the transported center maps are uniformly
bounded, the sup norms of c_j are bounded below by a fixed positive
constant for large j. Uniform boundedness and equi-Lipschitz continuity
therefore give a subsequence converging uniformly to a nonzero periodic
Lipschitz function c.

At the same time (8) bounds the two distinct normalized normal fields

\[
v_j=e_j/A_j^2,\qquad z_j=w_j/(h_jA_j)
\tag{11}
\]

in L-infinity. They admit weak-* subsequential limits as piecewise
constant interpolants. We require no strong convergence or smoothness
of either normal field.

For clarity, the only shift-limit fact used below is elementary. If
v_j is uniformly bounded and phi is a fixed smooth test function, a
change of summation index gives

\[
h_j\sum_n\phi(h_jn)[v_j(n+k)-v_j(n)]=O_\phi(h_j)
\tag{12}
\]

for each fixed integer k. Smooth variable coefficients may be included
in phi. Thus any fixed finite stencil on a weakly convergent bounded
normal field tends, in distributions, to its frozen zero-envelope
symbol. This prevents an unproved regularity bootstrap from entering
either limit argument.

## 5. Odd rows give the full first-slow compatibility equation

Divide the odd equation by h_j A_j. From (7)--(8),

\[
\|R_{h_j,o}/(h_jA_j)\|_\infty
\le C_g A_j^2/h_j\longrightarrow0.\tag{13}
\]

At the frozen quarter character, let R_f be the fourteen-row cokernel
map obtained by eliminating the owned twenty-column normal chart.
It annihilates the **entire** frozen joint matrix J_f(i), not merely a
selected subset of its equations. By (11)--(12), the normal term has
weak limit `R_f J_f(i)B_perp z=0`.

For the center term, Taylor-expand only the smooth stencil coefficients,
S, and the exact background (1). Their remainders are O(h_j^2).
The c_j fields are not Taylor-expanded twice. Their uniformly bounded
first differences pass to the distributional derivative of c; summation
by parts with a smooth test gives this directly. The first-order
coefficient is consequently exactly the literal shared-link jet already
certified in
[A4D_WARPED_QUARTER_REGULAR_RESPONSE.md](A4D_WARPED_QUARTER_REGULAR_RESPONSE.md):

\[
D_f\alpha'+f'B_f\alpha=0,\qquad \alpha=c_a-i c_b.
\tag{14}
\]

This includes every neighboring face weight, the derivative of the
transported role generators, and the first comparison connection. There
is no replacement of varying links by cellwise constants in (14).

The certified rank-four minor of D_f stays invertible near f=1. Put
`L_f=(D_f)_I^(-1) Pi_I` and `K_f=B_f-D_f L_f B_f`. Then

\[
\alpha'=-f'L_fB_f\alpha,\qquad f'K_f\alpha=0.
\tag{15}
\]

The first equation upgrades the Lipschitz limit to a C1 solution of a
linear ODE with smooth coefficients, hence to a smooth solution. This
regularity is a consequence of the exact equations in the limit, not
an assumption on the lattice family.

## 6. Even rows give the quadratic metric gate at a different scale

Divide the even equation by A_j^2. The bounded fields v_j in (11)
contribute their frozen even linear symbols in the weak limit. The
odd quadratic forcing converges strongly, because c_j converges
uniformly, shifted c_j have the same limit, and w_j/A_j tends uniformly
to zero. All other terms vanish: e_j^2/A_j^2=O(A_j^2), the higher
Taylor terms tend to zero, and the background/stencil coefficient
errors are O(h_j).

At zero envelope frequency the phase-common and alternating
**connection** matrices are invertible near f=1. Their limit equations
therefore determine the two even correction fields pointwise as the
same frozen quadratic normal corrections used by the owned certificate.
The remaining alternating metric equation is

\[
Q_{2,f}(c)=0.\tag{16}
\]

Only zero-envelope connection invertibility is used at this identification
step; the global even estimate in (6) used all joint rows. This distinction
avoids assuming a nonexistent full-circle connection inverse.
There is no uncontrolled `h*A_j/A_j^2` term: linear even/odd mixing is
forbidden exactly by fast parity. Nor is there a comparator residual
divided by A_j^2, since F_h(0)=0 exactly.

## 7. New exact coercivity certificate and the contradiction

The new [certificate](certificates/a4d_warped_quarter_isolation_check.py)
and [pinned ledger](certificates/a4d_warped_quarter_isolation_results.json)
rebuild the full shared-link first-slow matrices and the literal quadratic
metric gate on the entire compatible plane. They do not load the old
quadratic coefficient ledger as an oracle and do not need the cubic-axis
classification.

At f=1 the complete compatible plane is

\[
\alpha_3=-\alpha_2,\qquad
2\alpha_2=(1+i)\alpha_0-(1-i)\alpha_1.
\]

Write `alpha0=x-i*z`, `alpha1=y-i*t`, and c=M(x,y,z,t).
The real map M has rank four, and its Gram matrix obeys
`(M^T M-I)(M^T M-3I)=0`. Thus `|c|_2^2<=3|(x,y,z,t)|_2^2`.
Exact reconstruction and rational row elimination of the ten metric
quadratics give the five equivalent forms

\[
\begin{aligned}
F_1&=x^2-z^2,&F_2&=xy-3yt-zt,&F_3&=xz-yt,\\
F_4&=xt+yz-yt,&F_5&=y^2-6yt-t^2.
\end{aligned}\tag{17}
\]

The pinned matrix taking Q2(Mv) to these forms has maximum absolute row
sum 21. A full degree-four rational ideal calculation checks all 35
monomial coefficients of

\[
(x^2+y^2+z^2+t^2)^2=\sum_{j=1}^5 P_j(x,y,z,t)F_j(x,y,z,t),
\tag{18}
\]

where the five P_j are the quadratic polynomials pinned in the ledger.
Their total absolute coefficient sum is exactly 707/3. Cauchy's
inequality, or the direct bound `|v_i v_j|<=|v|_2^2`, now gives the
explicit finite coercivity statement

\[
\boxed{K_1\alpha(c)=0\quad\Longrightarrow\quad
\|Q_{2,1}(c)\|_\infty\ge\frac1{14847}\|c\|_2^2.}\tag{19}
\]

In particular Q2 and K have no common nonzero real zero. On the full
real unit sphere, `||Q2_1(c)||^2+||K_1 alpha(c)||^2` has a positive
minimum. The charts, the gate, and the compatibility map depend
smoothly on f, so a sufficiently small fixed coframe neighborhood has

\[
Q_{2,f}(c)=0,\quad K_f\alpha(c)=0\quad\Longrightarrow\quad c=0.
\tag{20}
\]

A nonconstant f has an interval where f' is nonzero. Equations
(15)--(16) and (20) force c=0 there. Uniqueness for the linear ODE in
(15) propagates zero around the whole circle, including critical points
and plateaus. This contradicts the nonzero uniform limit in Section 4.
Thus the sequence (9) cannot exist.

If (3) were false for every positive c_g and every h_g, choose a
nonzero root with `h_j<1/j` and `||u_j||_infinity<=sqrt(h_j)/j`.
This is precisely the excluded sequence (9). Therefore (3) follows.
The proof supplies positive constants but not their numerical values.
It also does not claim the existence of a new branch at the square-root
scale; that scale is where the odd cubic term could first balance the
h-linear transport term.

## 8. An open class with all ten metric components

The argument is not limited to exactly diagonal coframes. Choose any
fixed nonconstant warped coframe S0(y1) as above, sufficiently small that
`sup||S0-I||_op<1/10000`, strictly inside the separate general
one-coordinate designated theorem's radius. There is a C1-open
neighborhood of S0 among smooth one-coordinate coframes S(y1) for which
the same isolation conclusion holds, with constants depending on S.
All ten Gram-metric components can vary in this neighborhood.

Here are the inputs for this openness assertion. The designated root
exists by the general one-coordinate connection theorem. The four
transported quarter role lines and the all-frequency circle estimate
persist near I. The first-slow envelope derivative D_S stays injective.
The other first-slow term is a smooth matrix B_(S,S'), obtained from
the same finite stencil and the first smooth comparison coefficient;
that coefficient depends smoothly on (S,S') because its phase-common
connection matrix is invertible. Hence the limit system becomes

\[
D_S\alpha'+B_{S,S'}\alpha=0,\qquad Q_{2,S}(c)=0.
\]

Choose a point y0 with f0'(y0)!=0. At (S0(y0),S0'(y0)), the compatibility
map `(I-D_S L_S)B_(S,S')` and Q2 have no common unit zero by (20).
Compactness of the unit sphere preserves this at y0 for all sufficiently
small C1 perturbations. The limit amplitude is zero at y0; the linear
ODE `alpha'=-L_S B_(S,S') alpha` then gives zero everywhere. Sections
2--6 and the final contradiction are unchanged.

This is openness within the one-coordinate metric class. Adding
dependence on a second spatial coordinate destroys the invariant sector
and is not covered by this argument.

## 9. Boundaries of this closure and hostile controls

The nonregular gap is removed **in the declared product-closed sector**.
Its arbitrary arrays include all one-envelope mesh oscillations and
concentrations; compactness of normalized centers is proved by (8), not
postulated. The passage to the raw owner sum in (4) uses exact equality
with K_h^* and its already owned O(h^infinity) correction, so no fixed
pointwise O(h^2) estimate is multiplied into a false vanishing sum.

Several scope restrictions remain essential:

* For constant f, the f' compatibility obstruction disappears. The owned
  flat exact quarter axes are then genuine countercontrols to isolation.
  The constants in (3) are not asserted uniform as f approaches a constant.
* Dropping the nonconstant-phase metric equations removes (16); this
  proof then does not exclude connection-only extra branches.
* The source is not defined from a candidate. A prescribed common source
  unequal to the designated readout can have no root in this neighborhood;
  no general source-existence claim has been made.
* The continuous circle covers Sigma_L, not the full four-dimensional
  frequency torus. The six continuous physical rank-23 circles enter Sigma_L only
  at its quarter pair; their remaining characters and other possible
  torus components are outside this sector. The physical circle audit
  supersedes the former isolated-points interpretation. The finite-amplitude
  Y H_TORUS problem is also a separate symbol.
* For a general fixed four-dimensional g, exact designated center
  compatibility and a sufficient range estimate remain unproved. The
  unrestricted Target-U transfer also remains unproved. A normal-coordinate
  argument or tiling of this one-coordinate theorem does not resolve them.

The analytic theorem and the exact finite certificate are separate
artifacts. The latter checks first-slow rank, all restricted quadratic
coefficients, the complete quartic identity, a dense literal readout,
and a sign-mutation rejection. It does not machine-check compactness or
the global continuum conclusion. PR #310 remains Draft / IN_PROGRESS,
with task-level status PARTIAL / OPEN.

## Replay

```sh
python3 02_REGISTRY/research/certificates/a4d_warped_quarter_isolation_check.py --expect 02_REGISTRY/research/certificates/a4d_warped_quarter_isolation_results.json
```
