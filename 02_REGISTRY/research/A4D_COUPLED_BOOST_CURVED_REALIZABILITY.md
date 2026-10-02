# Coupled boost on the nonconstant coframe: exact exclusion

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.  
Input head: `3708ccddc9f249760eab7ca7aa3d7108850a427e`.  
Requested gate: `JOINT-CRITICAL-REALIZABILITY-AND-OWNER-SUM-CONTROL`.  
Result: **outcome 1, `COUPLED_BOOST_EXCLUDED`**, for the original family below.

The continuation in Sections 6--8 removes the amplitude-pattern restriction:
every temporal link may have its own independent real B amplitude. A single
joint flux identity expresses the necessary connection row through three
metric readouts. On the same fixed coframe it gives
`||E_K||_owner1 >= (102/625)*L^3-90*M^2` whenever
`||Xi_diag||_infinity <= h^2*M`. Thus no amplitude retuning of this same
temporal B family is joint-admissible for a uniformly bounded prescribed
source on sufficiently fine meshes; tau=0 is excluded at every mesh.

The exact identity is

\[
\boxed{
(E_K)_{x,0;J_{12}}(S_h,K(t))
=-\frac{2t}{4-3t^2}
\left[f(hx_1)^2-f(h(x_1-1))^2\right],
\qquad \sum_r x_r=0\pmod4.
}
\tag{1}
\]

This is a component of the full shared-link Euler equation, with its actual
neighboring face bases. It excludes every nonzero amplitude in the real
Cayley chart on the fixed curved coframe below. No metric-response
discrepancy of a nonstationary field is used as a joint-source counterexample.

## 1. Data fixed before the candidate

Let `Lambda_L=(Z/LZ)^4`, `L in 4*N`, and `h=1/L`. Fix, independently of L
and of the candidate amplitude,

\[
\begin{split}
&\eta=\operatorname{diag}(1,-1,-1,-1),\qquad
f(y)=1+\frac{1-\cos(2\pi y)}{50},\\
&S(y)=\operatorname{diag}(1,1,f(y_1),f(y_1)),\qquad
g=S^T\eta S,\qquad S_h(x)=S(hx),\\
&\tau(y)\equiv0\in\mathbb R^{10},\qquad
E_K(S_h,K)=0,\quad E_Q(S_h,K)=h^2\tau(hx).
\end{split}
\tag{2}
\]

The ten source slots are `(00,01,02,03,11,12,13,22,23,33)`, with the
off-diagonal convention of the response-memory owner. This is a prescribed
smooth vacuum source, not a response assigned after constructing K.
The coframe is exactly the fixed warp used in
[the designated curved continuation owner](A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md).
It is positive and nondegenerate, and genuinely curved:
`f''(0)=2*pi^2/25 != 0`; the spatial warped sectional curvature includes
`-f''/f`. In particular this is not the constant eta control.

The comparator remains the #216 `K_h^sm` on this same g. The owner topology,
if the second outcome were reached, is the unweighted sum
`sum_x sum_(j=0)^9 |Xi_j(K)-Xi_j(K_h^sm)|`, with no cell-volume or phase
averaging factor. The first outcome below fails before this comparison is
needed. It also holds for any other metric source specified independently,
because that source does not enter E_K.

## 2. The unchanged candidate and the Euler convention

Use the owner's generators `K_i=E_(0i)+E_(i0)` and
`J_12=E_12-E_21`. Set

\[
B=K_1+K_2+K_3,\qquad B^3=3B,\qquad D=4-3t^2,
\]
\[
U(t)=(I-tB/2)^{-1}(I+tB/2)
=I+\frac{4tB+2t^2B^2}{D},\qquad |t|<2/\sqrt3.
\tag{3}
\]

Writing `p(x)=sum_r x_r mod 4`, define the original #227 shared-link family

\[
L_{x,0}=(U,I,U^{-1},I)_{p(x)},\qquad L_{x,r}=I\quad(r=1,2,3).
\tag{4}
\]

K(t) denotes this entire link field. In particular K(0)=I; no smooth
comparator or uncomputed correction has been inserted into (4).
The derivative in (1) varies just one genuine lattice link by
`L_(x,0) -> L_(x,0) exp(epsilon J_12)`. All incident faces contribute.

For complementary legs `u,v`, let W_rs(S) be the literal star-action
weight, so the cell term is `sum_ab W_rs(S)_ab P_rs,ab`, where
`P_rs=L_(x,r)L_(x+r,s)L_(x+s,r)^(-1)L_(x,s)^(-1)`.
This is equal to pairing W with `(P-P^(-1))/2`: W annihilates the
eta-symmetric part. For (2), the weights of faces 01, 02 and 03 are the
identity-coframe weights multiplied by `f^2`, `f`, and `f`, respectively.

## 3. Direct derivation of the identity

Put `f_n=f(hx_1)` and `f_-=f(h(x_1-1))`. At phase zero the six incident
face contributions to the selected Euler component are exactly:

| Face | Base x | Base x-e_s |
|---|---:|---:|
| 01 | `-2t f_n^2/D` | `+2t f_-^2/D` |
| 02 | `+2t f_n/D` | `-2t f_n/D` |
| 03 | `0` | `0` |

For a forward occurrence use `delta L=L J_12`; for an inverse occurrence
use `delta(L^(-1))=-J_12 L^(-1)`. Substitution of (3) into these six
products gives the table and its sum (1). The 02 terms cancel because
shifting x by e_2 leaves f unchanged. The 01 terms retain the distinct
values at the two true face bases. Freezing both weights at x would
incorrectly erase exactly the obstruction being checked.

This calculation is an identity in independent values f_n, f_- and t.
To verify it without symbolic simplification, give every link the same
denominator D. Each link numerator has degree two; the four factors of
each differentiated plaquette have complete degree at most eight. The
full numerator of (1) is

\[
D^4(E_K)_{x,0;J_{12}}
=-2tD^3(f_n^2-f_-^2),\qquad
-2tD^3=-128t+288t^3-216t^5+54t^7.
\tag{5}
\]

The certificate checks every coefficient, including the vanishing even
powers and degree eight. It is not a truncated jet in t or h.

## 4. Outcome 1 at every mesh and every nonzero amplitude

At the lattice origin, `p=0`, `f_n=1` and
`f_-=1+(1-cos(2*pi/L))/50>1`. Thus

\[
(E_K)_{0,0;J_{12}}
=\frac{2t}{4-3t^2}
\left[\left(1+\frac{1-\cos(2\pi/L)}{50}\right)^2-1\right]\ne0
\tag{6}
\]

for every `L in 4*N` and every `0<|t|<2/sqrt(3)`. This excludes arbitrary
nonzero refinement-dependent t_h as well, regardless of how fast t_h
tends to zero. Small residual is not exact stationarity.

More generally (1) excludes (4) on every positive sampled profile with
an unequal adjacent pair: choose that x_1 and choose x_0 to make p=0.
This is a whole-profile exclusion, not a test at selected wavelengths.
Nonvanishing of E_K is preserved under the genuine simultaneous local
Lorentz action on coframe and links, so taking that quotient cannot make
the candidate admissible.

The requested two-outcome test therefore terminates at **outcome 1**:
the original coupled boost is removed from the admissible joint class on
the declared nonconstant coframe. No owner-norm claim is required for
this rejected candidate, and tau has never been fitted to Xi.

### Owner-sum consequence of the same identity

Retain the full unweighted connection residual norm
`||E_K||_(owner,1)=sum_x sum_(r=0)^3 sum_(a=0)^5 |(E_K)_(x,r;a)|`.
Keeping only the nonnegative contributions of the selected J12 row at phase
zero, each fixed x1=n has exactly `L^3/4` such sites: for every pair x2,x3,
there are `L/4` possible x0 of the required residue. Thus (1) gives

\[
\|E_K(S_h,K(t))\|_{\rm owner,1}
\ge \frac{2|t|}{4-3t^2}\frac{L^3}{4}
\sum_{n=0}^{L-1}|f_n^2-f_{n-1}^2|.
\tag{7}
\]

For the fixed profile (2), its sampled positive square is monotone on each
half-circle, with minimum 1 and maximum `(26/25)^2`. For every `L in 4*N`
these extrema are sampled, so its total variation is exactly
`2[(26/25)^2-1]=102/625`. Consequently

\[
\boxed{
\|E_K(S_h,K(t))\|_{\rm owner,1}
\ge \frac{51|t|L^3}{625(4-3t^2)}.
}
\tag{8}
\]

The `L^3/4` factor counts the selected physical sites; it is not an average
or a norm normalized by the lattice volume. This is a connection-residual
bound, not a claim about the metric response gap. It may tend to zero if t_h
does so sufficiently fast, but (6) still forbids **exact** stationarity at
every mesh with nonzero t_h. Outcome 1 therefore has no small-amplitude
exception. The all-L bound follows from the same identity; it introduces no
additional family or sector.

## 5. Replay and scope

```sh
python3 02_REGISTRY/research/certificates/a4d_coupled_boost_curved_realizability_check.py
```

The checker verifies the complete polynomial (5) and independently
differentiates the full periodic L=4 action at three rational t values,
using exact cosine-profile samples. It differentiates the odd curvature
itself, enumerates every based face, and detects both an inverse-variation
sign mutation and replacement of neighboring coframes by the origin's
coframe. The continuum/all-mesh conclusion is (6), not extrapolation from
those rational controls.
The owner-sum control additionally differentiates the full action at each
of the four slow-coordinate values, counts every phase-zero site at L=4,
and checks the coefficient `51/625`. The all-mesh count and variation
formula are the analytic arguments above, not a finite-grid extrapolation.

Verdict: `COUPLED_BOOST_CURVED_REALIZABILITY_EXCLUDED`.
The requested `JOINT-CRITICAL-REALIZABILITY-AND-OWNER-SUM-CONTROL` check for
this candidate is closed by nonrealizability. The parent response-decoupling
task still quantifies over arbitrary exact joint fields, including fields
different from (4); this one identity does not prove its universal terminal.
Its status remains `PARTIAL / OPEN`, Draft / `IN_PROGRESS`. No additional
sector, selector, action term, or BOOK/CORE claim is introduced.

## 6. Remove every amplitude-pattern assumption in the same B family

Follow-up input: `0c7cce3b6e69cb39d638eb5d57c9bc37794f2ced`.
Keep the coframe (2), the same generator B, and the identity spatial links.
Allow every temporal link to have its own independent amplitude:

\[
L_{x,0}=U(a_x),\qquad |a_x|<2/\sqrt3,\qquad L_{x,i}=I\ (i=1,2,3).
\tag{9}
\]

The original four-phase field is included. No sign pattern, slow envelope,
regularity, phase decomposition, or uniform distance from the Cayley-chart
boundary is imposed. This tests all amplitude retunings of the same
candidate family, without introducing a frequency sector. The fixed source
tau=0 remains the primary case. The theorem below additionally permits any
source specified before the candidate with uniformly bounded diagonal
components `|tau_ii(x)|<=M`.

For independent real a,b in the chart, put

\[
\begin{split}
D(a)&=4-3a^2,\\
z(a,b)&=\frac{4(a-b)(4-3ab)}{D(a)D(b)},\\
c(a,b)&=1+\frac{24(a-b)^2}{D(a)D(b)}.
\end{split}
\tag{10}
\]

Direct multiplication using `B^3=3B` gives

\[
\frac{U(a)U(b)^{-1}-U(b)U(a)^{-1}}2=z(a,b)B,
\qquad c(a,b)^2-3z(a,b)^2=1.
\tag{11}
\]

Because `D(a)D(b)>0`, we have `c>=1`, so the branch is exactly
`c=sqrt(1+3z^2)`. These identities hold at arbitrary amplitude, not only
near a=b or zero. The temporal plaquettes of (9) therefore have
`C_0i(x)=z_i(x) B`, with `z_i(x)=z(a_x,a_(x+e_i))`; spatial plaquettes
are identity. All curvatures here are made from shared links.

Let `m=(Xi_11,Xi_22,Xi_33)^T`, where Xi is the actual Gram memory of the
action. True Gram differentiation at `S=diag(1,1,f,f)` gives

\[
m=\begin{pmatrix}
0&-f/2&-f/2\\
-1/2&0&-1/(2f)\\
-1/2&-1/(2f)&0
\end{pmatrix}z,
\qquad \det=-\frac14.
\tag{12}
\]

In particular the three actual plaquette coefficients are determined by
these three existing response components:

\[
\boxed{
z=T_fm,\qquad
T_f=\begin{pmatrix}
f^{-2}&-1&-1\\
-f^{-1}&f&-f\\
-f^{-1}&-f&f
\end{pmatrix}.}
\tag{13}
\]

The remaining seven source equations are retained in the joint system;
three necessary equations already suffice for exclusion. For a putative
exact stationary field, the genuine descended metric Euler equals Xi by
the Ward/section argument in the response-memory owner. Hence a prescribed
joint source implies `m=h^2*(tau_11,tau_22,tau_33)`.

## 7. One joint flux identity, with all neighboring coframes

For each temporal face, right variation of its outgoing temporal link
along B gives `w_i c_i`, and variation of its incoming link gives its
negative at the incoming face base. Here

`w_1=f^2`, `w_2=w_3=f`, and `c_i=sqrt(1+3z_i^2)`.

Indeed B commutes with both links, the literal star weight annihilates
the eta-symmetric B^2 term, and its pairing with B is w_i. Summing the
six actual face incidences yields the exact necessary joint identity

\[
\boxed{
E_K(x,0)[B]
=\sum_{i=1}^3D_i^-\!left[
w_i\sqrt{1+3\bigl((T_f\Xi_{\rm diag})_i\bigr)^2}\right](x),
\quad D_i^-F(x)=F(x)-F(x-e_i).
}
\tag{14}
\]

This identity is independent of the temporal-link amplitudes once their
metric readout is known. It uses no solution selection and no replacement
of neighboring cells by a frozen vacuum.

For the prescribed vacuum `tau=0`, (13) forces z=0 for every actual face;
(14) then reduces exactly to

\[
E_K(x,0)[B]=f_n^2-f_{n-1}^2.
\tag{15}
\]

There is no compatible joint root on the nonconstant profile, regardless
of the choice of the amplitudes a_x. The implication used the true metric
equations; it did not assign their values as a new source.

## 8. Uniformly bounded independent sources: raw owner-sum exclusion

More generally suppose the three diagonal source equations hold with
`||tau_diag||_infinity<=M`. Since `1<=f<=26/25`, (13) gives

\[
|z_1|\le3h^2M,\qquad |z_2|,|z_3|\le\frac{77}{25}h^2M.
\tag{16}
\]

Write (14) as `E_K(x,0)[B]=F(x)+R(x)`, with
`F=D_1^-(f^2)` and `R=sum_i D_i^-[w_i(c_i-1)]`.
The bound

\[
0\le\sqrt{1+3z^2}-1
=\frac{3z^2}{\sqrt{1+3z^2}+1}\le\frac32z^2
\tag{17}
\]

and periodic translation invariance of the **unweighted** sum give

\[
\begin{split}
\|R\|_1
&\le3\sum_{x,i}w_i(x)z_i(x)^2\\
&\le3\frac{1976}{625}\left(\frac{77}{25}\right)^2
   h^4 L^4 M^2
=\frac{35147112}{390625}M^2<90M^2.
\end{split}
\tag{18}
\]

Here `h^4 L^4=1` comes from the squared source scale; no lattice-volume
factor has been removed from the norm. All L^3 sites above each slow
coordinate contribute, so the same exact sampled variation as before gives
`||F||_1=(102/625)L^3`.
Since B is the sum of the three boost basis generators, the triangle
inequality bounds its Euler evaluation by the component owner norm.
Consequently

\[
\boxed{
\|E_K\|_{\rm owner,1}
\ge\frac{102}{625}L^3-90M^2.
}
\tag{19}
\]

An exact joint member of (9) is therefore impossible whenever
`L^3>(9375/17)M^2`. In particular the independently prescribed vacuum
M=0 is excluded at **every** mesh. No upper bound on any rapidity or
amplitude derivative was used. The conclusion covers arbitrary
refinement-dependent amplitude arrays and every bounded smooth source
specified before them.

The existing certificate now verifies all coefficients of (11), the
full Laurent identities (12)--(13), and independent based-face action
assembly at all 256 sites for an arbitrary four-coordinate amplitude
array and for arbitrary time-only links. It checks the raw owner count
in the zero-curvature control and the exact constant in (18).
All-period and continuum conclusions follow from (14)--(19), not from
the finite replay.

Follow-up verdict: `COUPLED_BOOST_ALL_AMPLITUDE_JOINT_EXCLUSION`.
The possible rescue by amplitude retuning is removed as a whole class.
Nonidentity spatial links or other Lorentz generators are outside (9);
no universal statement about those fields is inferred. The parent PR
remains Draft / `IN_PROGRESS`, with task status `PARTIAL / OPEN`.
