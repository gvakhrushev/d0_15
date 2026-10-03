# Fixed warp: exact nonlinear response after eliminating the transverse mean

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.  
Background owner: [warped designated rescue](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md).  
Status: analytic reduction for arbitrary small four-dimensional fields on the fixed warp; task remains `PARTIAL / OPEN`.

The mean connection can be eliminated using the owned one-coordinate
inverse. This yields an exact nonlinear identity for the remaining metric
memory. Vanishing of just its leading quadratic correlation is insufficient
for the unweighted owner-sum target; Section 6 makes that distinction precise.

## 1. Fixed background, norm, and exact root

Fix

\[
S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\quad
f(y)=1+\frac{1-\cos(2\pi y)}{50},\quad h=1/L.
\]

Let `K_h^*(x_1)` be the exact designated connection from the background owner.
It is invariant in x_0,x_2,x_3 and satisfies `E_K(Q_h,K_h^*)=0`.
Use the componentwise relative-log coordinates

\[
K_h=K_h^*\exp u,\qquad
F_h(u)=E_K(Q_h,K_h^*e^u),\quad
G_h(u)=\Xi(Q_h,K_h^*e^u).
\tag{1}
\]

All arrays are defined on the full physical L^4 lattice. The p=1 norm is
the **unweighted** component sum. A field invariant in the three transverse
coordinates has norm L^3 times its one-coordinate sum; it is not assigned
a smaller norm after reduction.

Let P be the normalized average over x_0,x_2,x_3 at fixed x_1, followed by
lifting the result back to the full lattice. The same definition applies
componentwise to connection and metric rows. It is a contraction on every
`ell^p`, including the raw owner p=1 norm. Write

\[
u=m+v,\qquad m=Pu,\quad Pv=0.
\tag{2}
\]

No Fourier support, derivative bound, four-phase pattern, or smooth envelope
is assumed for v.

## 2. The mean inverse is uniform; no transverse inverse is assumed

At every mean field m, transverse translation equivariance gives

\[
P\,DF_h(m)v=0,\qquad P\,DG_h(m)v=0\quad(Pv=0).
\tag{3}
\]

The background owner bounds the one-coordinate derivative inverse at the
smooth comparator by 18 in every ell^p. The exact root differs from that
comparator super-algebraically, and the relative-log coordinate derivative
differs from the additive-log derivative by `I+O(h)`. A further Neumann
perturbation therefore gives, for sufficiently fine meshes, a uniform bound

\[
\|(DF_h(0)|_{\operatorname{im}P})^{-1}\|_{p\to p}\le\Lambda,
\qquad \Lambda=36\ \text{may be used}.
\tag{4}
\]

The constant lift multiplicity L^3 cancels in the operator norm. It is not
silently dropped from any response estimate.

Finite incidence and analyticity on a fixed compact log/coframe chart give
uniform tame bounds, for example

\[
\|D^2F_h(w)[a,b]\|_p+\|D^2G_h(w)[a,b]\|_p
\le C_g\|a\|_\infty\|b\|_p,
\tag{5}
\]

after increasing C_g to cover the symmetric terms. The same argument gives
the higher derivative bounds needed below. These constants do not depend
on the number of sites.

## 3. Exact elimination of the mean variables

For every sufficiently small v with Pv=0, the projected equation

\[
P F_h(m+v)=0
\tag{6}
\]

has a unique small mean solution `m=Gamma_h(v)`. This solves only the mean
equations. The nonmean connection equations remain to be imposed.

For completeness, put `H=DF_h(0)|_(im P)` and
`N(u)=F_h(u)-DF_h(0)u`. The fixed-point equation
`m=-H^-1 P N(m+v)` is a contraction on a ball of radius
`C ||v||_infinity^2`, uniformly in h: its m-derivative has norm
`O(||m||_infinity+||v||_infinity)` by (5). Absorbing the m term in the
same estimate in ell^p gives

\[
\|\Gamma_h(v)\|_\infty\le C\|v\|_\infty^2,\qquad
\|\Gamma_h(v)\|_p\le C\|v\|_\infty\|v\|_p.
\tag{7}
\]

In particular, every exact full connection solution with `||u||_infinity=O(h)`
has `Pu=O(h^2)` in sup norm. The leading correction has zero transverse
mean, even when it is arbitrarily rough. This is a consequence of (6), not
a connection selector imposed on the full solution set.

## 4. One exact response identity retaining all nonlinear orders

At `m=Gamma_h(v)`, define the mean operators

\[
\mathcal A_m=\int_0^1DF_h(sm)|_{\operatorname{im}P}\,ds,
\qquad
\mathcal C_m=\int_0^1DG_h(sm)|_{\operatorname{im}P}\,ds,
\tag{8}
\]

and the full quadratic Taylor remainders

\[
\mathcal N_F(m;v)=\int_0^1(1-s)D^2F_h(m+sv)[v,v]\,ds,
\]
\[
\mathcal N_G(m;v)=\int_0^1(1-s)D^2G_h(m+sv)[v,v]\,ds.
\tag{9}
\]

These remainders contain all powers of v; no truncation is made. For small
m, (4)--(5) give a uniform inverse for A_m, for example `2 Lambda` in
each ell^p. Equations (3) and (6), with F_h(0)=0, imply exactly

\[
\mathcal A_m m=-P\mathcal N_F(m;v).
\tag{10}
\]

Taylor's formula for G and (3) now give the exact reduced response

\[
\boxed{
\begin{split}
\mathcal R_h(v)
&:=P\,[G_h(\Gamma_h(v)+v)-G_h(0)]\\
&=P\mathcal N_G(m;v)
-\mathcal C_m\mathcal A_m^{-1}P\mathcal N_F(m;v).
\end{split}}
\tag{11}
\]

This derives the nonlinear memory from the actual Euler maps and the proved
mean inverse. It eliminates every mean coordinate while retaining arbitrary
full-lattice transverse fields. It requires no inverse on those fields.
From (5), (8)--(11),

\[
\|\mathcal R_h(v)\|_p\le C\|v\|_\infty\|v\|_p.
\tag{12}
\]

If the independently prescribed source is transverse-invariant, as tau=0
or tau(hx_1), an exact joint field also satisfies
`(I-P)G_h(m+v)=0`. Since G_h(0) is invariant, its **full** response difference
then equals R_h(v), not just its average. The remaining exact equations are

\[
(I-P)F_h(\Gamma_h(v)+v)=0,\quad
(I-P)G_h(\Gamma_h(v)+v)=0,\quad
G_h(0)+\mathcal R_h(v)=h^2\tau_h.
\tag{13}
\]

The last equation retains the source fixed before v. The comparator has not
been assigned that source, so no tautological equality of two sourced roots
is being used. For sources with transverse dependence the corresponding
nonzero source term must remain in the second equation of (13).

## 5. Precise owner-sum target

The designated owner proves
`h^-2 ||G_h(0)-Xi(K_h^sm)||_owner1=O(h^infinity)`.
Thus for exact joint fields obeying the transverse-invariant source convention,
the requested full owner-norm target is equivalent to

\[
\boxed{\|\mathcal R_h(v_h)\|_{\rm owner,1}=o(h^2)
\quad\text{on the exact admissible set (13)}.}
\tag{14}
\]

Equation (11) is the exact object still needing a cancellation or estimate.
Equation (12) alone is not enough: the bound `||v||_infinity=O(h)` permits
`||v||_owner1=O(h L^4)`.

## 6. The leading correlation law has a weaker topology

Expanding (11) at zero gives the familiar reduced quadratic form

\[
\mathcal R_h(v)=\frac12P D^2G_h(0)[v,v]
-\frac12DG_h(0)|_{\operatorname{im}P}\,
H^{-1}P D^2F_h(0)[v,v]+\mathcal E_h(v),
\tag{15}
\]
\[
\|\mathcal E_h(v)\|_1\le C\|v\|_\infty^2\|v\|_1.
\tag{16}
\]

For v=O(h) in sup norm, (16) can be as large as `O(h^3 L^4)=O(h^-1)`
in the raw owner sum. Even a uniform sitewise `O(h^3)` response gives
`h^-2 ||Delta Xi||_owner1=O(h^-3)`, not convergence to zero.
A sitewise expansion starting at `O(h^q)` would need q>6 for this simple
uniform counting argument to suffice in four dimensions.

Therefore vanishing of the limiting quadratic joint-kernel correlation
controls a leading weak/volume-normalized continuum response, provided its
compactness hypotheses are justified. It does not close (14). Inferring
microlocal support on frozen joint kernels also requires a stated
localization/two-scale theorem; the elementary O(h) residual estimate alone
is not such a theorem. No spectral classification is added here.

The previous quadratic-only terminal formulation is superseded for the
raw owner target by the all-order identity (11) and estimate obligation (14).
An admissible nonzero exact response would be a negative terminal only with
the fixed source and all equations (13) satisfied.

Verdict: `WARPED-FULL4D-EXACT-MEAN-SCHUR-RESPONSE-REDUCTION`.
This is an analytic consequence of the owned one-coordinate inverse,
finite-stencil derivative bounds, and Taylor's integral identity. It is
not a machine-certified continuum closure or a universal response theorem.

## 7. An exact stationary action identity for the full four-dimensional field

This step uses the same naked action and the same fixed coframe, and does
not restrict the candidate to a connection sector. Let

\[
\mathscr A_h(S,K)=\sum_x\ell(S_x,C(K)_x),\qquad
Q:\Xi=\sum_{a\le b}Q_{ab}\,(\operatorname{pack}\Xi)_{ab}.
\tag{17}
\]

The off-diagonal factor is already in pack Xi; it is not inserted again.
Each cell action is homogeneous of degree two in S. For the true Gram
variation dot Q=Q, the lift is dot S=S/2. Therefore, exactly and even
before imposing connection stationarity,

\[
\boxed{\mathscr A_h(S,K)=\sum_x Q_x:\Xi(S,K)_x.}
\tag{18}
\]

This follows from the literal complementary wedge weights, not from an
assumed continuum Einstein equation. On E_K=0, Xi is the genuine descended
metric Euler, as proved by the response-memory owner.

Take any second exact full connection root K=K_h^* exp u and put
a_h(t)=mathscr A_h(S,K_h^* exp(tu)). Every one of the 24 L^4 independent
connection Euler rows is assumed zero at both endpoints. Hence
a_h'(0)=a_h'(1)=0. Two integrations by parts give, for any C^3 scalar a,

\[
a(1)-a(0)=\tfrac12[a'(0)+a'(1)]
-\tfrac12\int_0^1t(1-t)a'''(t)\,dt.
\tag{19}
\]

Using the stationary endpoints and (18) yields the all-order identity

\[
\boxed{
\sum_xQ_x:\bigl[\Xi(S,K)_x-\Xi(S,K_h^*)_x\bigr]
=-\tfrac12\int_0^1t(1-t)a_h'''(t)\,dt.}
\tag{20}
\]

No quadratic truncation, transverse inverse, translation invariance of
the candidate, or source assignment is used in (20). Only the comparator
comes from the already owned designated construction.

### A uniform bound in the original physical sum

Write A_star=||log K_h^*||_infinity and A=||u||_infinity in the six-generator
coordinate sup norm, and assume A_star+A<=1/48. For the fixed warp,
each literal face weight has nuclear norm at most 676/625. Along the
relative-log path, a third face derivative is bounded by

\[
\frac{676}{625}e^{24(A_\star+A)}
\left(\sum_{\text{four face positions}}\|u_{\text{link}}\|_{\rm op}\right)^3.
\]

Every generator has operator norm one, so the parenthesized sum is at
most 24 A. Each independent physical link occurs in exactly six based
faces. Summing all positions, using e^(1/2)<2, gives

\[
|a_h'''(t)|
\le 6912\frac{676}{625}A^2\|u\|_{\rm owner,1}
<8192 A^2\|u\|_{\rm owner,1}.
\tag{21}
\]

The inverse factors in the odd plaquette have the same bound, and their
factor 1/2 is retained. The count is over the full L^4 carrier, regardless
of roughness or frequency. Since integral_0^1 t(1-t) dt=1/6, (20) implies

\[
\left|\sum_xQ_x:[\Xi(K)-\Xi(K_h^*)]_x\right|
\le\frac{8192}{12}A^2\|u\|_{\rm owner,1}.
\tag{22}
\]

In particular, if A<=M_u h, then ||u||_owner1<=24 L^4 M_u h and

\[
\left|h^4\sum_xQ_x:h^{-2}[\Xi(K)-\Xi(K_h^*)]_x\right|
\le16384 M_u^3 h.
\tag{23}
\]

This proves convergence of one integrated scalar trace for every exact
full-lattice log-O(h) connection-stationary family. It is not convergence
of the full tensor or of the raw owner norm.

An exact comparator root is not needed for this one observable. With
an approximate comparator K_bar, residual r_h=E_K(S,K_bar), and exact
stationarity only at K=K_bar exp u, (19) instead gives exactly

\[
\sum_xQ_x:[\Xi(K)-\Xi(K_{\rm bar})]_x
=\tfrac12\langle r_h,u\rangle
-\tfrac12\int_0^1t(1-t)a_h'''(t)\,dt.
\tag{23a}
\]

The first pairing uses all independent physical link coordinates. Its
absolute value is at most ||r_h||_infinity ||u||_owner1. Thus a log-O(h)
candidate and comparator with ||r_h||_infinity=O(h^2) still give an O(h)
normalized integrated trace difference. The owned super-algebraic smooth
comparator residual is more than sufficient. For any other fixed
nondegenerate coframe in a compact solder chart, the same argument holds
with its finite weight constant in place of 8192. This conditional
full-field lemma needs no connection inverse or proof of an exact
four-dimensional comparator root. It supplies neither that existence
theorem nor a tensor owner-norm estimate.

### The designated action on the same nonconstant warp

The owned one-coordinate inverse determines the first smooth log
coefficient uniquely. With p=f' and q=f'', direct shared-face assembly
gives the leading forcing

\[
F^{(1)}_{0,K_1}=2fp,\qquad
F^{(1)}_{2,J_{12}}=F^{(1)}_{3,J_{13}}=-p
\]

and the leading smooth logs

\[
\log K^{\rm sm}_2=-hpJ_{12}+O(h^2),\qquad
\log K^{\rm sm}_3=-hpJ_{13}+O(h^2);
\quad \log K^{\rm sm}_{0,1}=O(h^2).
\tag{24}
\]

The complete h^2 curvature/action calculation keeps all 24 arbitrary
second log coefficients. They cancel from this coefficient. The six
literal face action coefficients in face order are

\[
(0,0,0,-fq,-fq,-p^2),\qquad
\ell_h(K_h^{\rm sm})=h^2[-2ff''-(f')^2]+O(h^3).
\tag{25}
\]

Thus no global Hilbert-density normalization is being inferred merely
from a metric-normal point. Periodicity gives

\[
\int_0^1[-2ff''-(f')^2]\,dy
=\int_0^1(f')^2\,dy=\frac{\pi^2}{1250}
\tag{26}
\]

for f(y)=1+(1-cos(2*pi*y))/50. The leading sampled average is also exactly
pi^2/1250 for every allowed L: its only trigonometric terms have degrees
one and two. The super-algebraic rescue from K_h^sm to K_h^* preserves this
leading coefficient in the actual physical sum. Consequently

\[
h^2\mathscr A_h(S,K_h^*)=\frac{\pi^2}{1250}+O(h).
\tag{27}
\]

The [existing response-memory certificate](certificates/a4d_stationary_response_memory_check.py)
now verifies the complete literal first 24-row equation and (25) with
independent symbolic f,p,q and all 24 second log coefficients. It also
checks the endpoint kernel, its sign/factor controls, and all normalization
constants. The uniform analytic remainder and exact-root comparison use
the already owned smooth-comparator and designated-rescue results.

### A necessary condition on a source specified before the field

For an exact joint field with the predeclared source Xi=h^2 tau_h,
equations (18), (23), and (27) require

\[
\boxed{h^4\sum_xQ_h(x):\tau_h(x)
=\frac{\pi^2}{1250}+O(h).}
\tag{28}
\]

If a fixed smooth tau is sampled, this gives
integral Q(y):tau(y) dy=pi^2/1250. For tau=0, (28) is impossible.
Therefore, for every fixed log-O(h) bound, sufficiently fine meshes have
no exact joint vacuum on this same nonconstant warp, even with all
generators, all spatial links, and arbitrary four-dimensional patterns.
The usual absolute-log O(h) condition is equivalent here to relative-log
O(h), since the designated root itself has logarithm O(h).

This is a source-feasibility obstruction, not a response-gap witness.
It excludes the independently declared vacuum class; it does not close
the task by a vacuous response statement. Sources satisfying the trace
condition still require the full owner estimate (14), or an admissible
counterexample. The integral trace controls neither sitewise trace
oscillations nor the other metric readouts. The existing flat boost
control has zero integrated trace and nonzero owner response; its
connection-only status still cannot establish a joint negative terminal.
The flat response-null control also remains consistent: when f is
constant, the geometric integral (26) is zero.

Additional verdict: **FULL4D-LOG-O(h)-STATIONARY-TRACE-COMPATIBILITY**.
The independent vacuum on this fixed warp is unrealizable in that class.
The general task and its raw owner-sum target remain **PARTIAL / OPEN**.

## 8. The fixed continuum Einstein source is also exactly infeasible

The subsequent [full-link arithmetic theorem](A4D_FIXED_SOURCE_ALGEBRAIC_COMPATIBILITY.md)
now excludes the predeclared continuum Einstein source on this same cosine
warp at every allowed finite mesh, without the log-O(h) hypothesis. It uses
the original finite action, the exact identity (18), and the algebraicity of
every full connection-stationary critical value at an algebraic sampled
coframe. The source would require `A_h=pi^2*L^2/1250`, a transcendental value.

Thus existence of K_h^* here is existence of a connection-stationary root
with a mesh-dependent output source. It cannot establish a joint root for
the prescribed continuum source. On that fixed pair the admissible set
of (13) is empty, so (14) supplies no nonvacuous closure. The new theorem
retains the original action, sampling, physical Lorentz carrier and norm;
it does not demand a transverse inverse or a microstructure classification.
