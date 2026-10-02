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
