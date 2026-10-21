# Exact native radial minimization and all-order matter normal form

**Date:** 2026-10-21.  
**Status:** explicit native algebraic continuation of the
[complete-price stationary normal form](A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md).  
**Closure flag:** GR_closed = false.

This proof consumes the displayed native detector and the unit-charge
premises of the preceding compiler packet. A fresh checkout of the
original source interfaces was unavailable. In particular the premise
κ > 53 is explicitly consumed, not independently reattributed to an
unread current source file.

## 1. What is new

The literal native detector is quadratic in its geometric query. Its
coframe trace equation therefore has an explicit algebraic branch,
independent of the outer cap valuation. We prove:

1. A nonzero trace branch on the constructive interval |y| ≤ 2⁻¹².
2. An exact all-order parametric formula for the derived matter function
   K, on a common target interval |Y| < 2⁻¹³ for every admitted fixed
   finite cap.
3. Exact partial minimization of the original price over free coframe
   radii. The minimizing representative is independent of the outer
   valuation within each monotonicity class.
4. A separate full-field transfer theorem at uniform detector response.

The trace branch alone is not a solution of the remaining shape, link,
matter or internal equations. Its nonzero densities and its actual
radial minima must not be confused with full-field stationarity or a
minimum over all physical variables.

## 2. The native quadratic identity

Let

\[
\varphi=(1+\sqrt5)/2,\quad p=\varphi^{-1},\quad z=2^{-20},
\quad \ell(E)=4E(1-E).
\]

The literal response is

\[
\begin{aligned}
B(y)&=4(p+p^2y)^2[1-(p+p^2y)^2],\\
A_{\rm det}(x,y)&=\ell(p^2(1+x))
       +[1-\ell(p^2(1+x))]B(y),\\
r(x,y)&=1-[1-zB(y)][1-zA_{\rm det}(x,y)].
\end{aligned}
\tag{1}
\]

Define functions of y by

\[
\begin{aligned}
v&=p+p^2y,&w&=1-2v^2,&c&=1-z+zw^2,\\
A(y)&=4p^5z\,cw^2,\\
R(y)&=1-c(1-z+zp^6w^2).
\end{aligned}
\tag{2}
\]

Here A(y) is a quadratic coefficient and is distinct from the detector
A_det(x,y). The identities B = 1 − w²,
1 − ℓ(p²) = p⁶ and

\[
\ell(p^2(1+x))=4p^3+4p^5x-4p^4x^2
\]

give the exact formula

\[
\boxed{r(x,y)=R(y)+A(y)(x-x^2/p).}
\tag{3}
\]

On the actual carrier, an independent free-site radial coframe change
e → exp(t/2)e sends (x,y) to (exp(t)x,exp(−t)y). Thus, for
F = g(r) − g(r₀),

\[
\frac{dF}{dt}=g'(r)T(x,y),\qquad
T(x,y)=xr_x-yr_y.
\tag{4}
\]

Where g′ is nonzero, the full coframe Euler trace is exactly T = 0,
independent of g. This uses an actual coframe variation; it never
assumes that x and y are independent physical field coordinates.

## 3. The explicit branch and a proved domain

Put

\[
\epsilon=2^{-12},\qquad C(y)=R'(y)/A(y),\qquad
k(y)=-yA'(y)/A(y).
\]

Then

\[
T/A=(1+k)x-\frac{2+k}{p}x^2-yC.
\tag{5}
\]

Define

\[
\Delta(y)=(1+k(y))^2-\frac{4(2+k(y))}{p}\,yC(y).
\tag{6}
\]

The branch through zero is

\[
\boxed{\tau(y)=\frac{2yC(y)}{1+k(y)+\sqrt{\Delta(y)}}.}
\tag{7}
\]

### 3.1 Bounds and uniqueness

For |y| ≤ ε, the elementary inequalities
8/13 < p < 5/8, p⁵ > 3/40 and p⁶ < 1/16 imply

\[
\frac35<v<\frac{63}{100},\quad
\frac15<w<\frac13,\quad |w'|,|w''|<1,\quad
\frac{15}{16}<c<1.
\tag{8}
\]

In particular A > 0. Let
H = (1−z)(1+p⁶)+2zp⁶w². Direct differentiation gives

\[
\frac{R'}A=-\frac{w'}{2p^5w}\frac Hc,\qquad
\frac{A'}A=\frac{2w'}w\left(1+\frac{zw^2}{c}\right),
\tag{9}
\]

and

\[
\frac{15}{16}<\frac Hc
=1+p^6-\frac{z(1-p^6)w^2}{c}<\frac{17}{16}.
\]

Since −w′ = 4p²v > 108/125, these bounds yield

\[
\boxed{12<C<36,\quad |A'/A|<11,\quad |k|<1/256.}
\tag{10}
\]

Indeed the upper bound for C is 425/12 < 36, and the lower bound is
larger than (108/125)·15·(15/16) = 243/20 > 12. Consequently

\[
\Delta>
\left(\frac{255}{256}\right)^2-720\epsilon
=\frac{53505}{65536}>\frac34.
\tag{11}
\]

The denominator in (7) is greater than 3/2. Therefore

\[
\boxed{|\tau(y)|<48|y|\le3/256,\qquad
\operatorname{sgn}\tau(y)=\operatorname{sgn}y.}
\tag{12}
\]

The other quadratic root obeys

\[
\frac{p(1+k)}{2+k}-\tau
>\frac{17}{57}-\frac3{256}>\frac14.
\tag{13}
\]

Thus τ is the unique trace root with |x| < 1/4 for every |y| ≤ ε,
and it is real analytic on a neighborhood of that closed interval.
Both densities are nonzero whenever y is nonzero.

### 3.2 Derivative estimates

Further differentiation of (2) gives

\[
\begin{aligned}
A''/A
 &=\frac{2(w'^2+ww'')}{w^2}
       \left(1+\frac{zw^2}{c}\right)+\frac{8zw'^2}{c},\\
R''/A
 &=-\frac{(w'^2+ww'')H+4zp^6w^2w'^2}{2p^5cw^2}.
\end{aligned}
\]

The bounds (8) make their absolute values respectively less than

\[
425/6+128z/15<72,\qquad
(500/3)(17/12+4z/135)<256.
\]

Using P(x)=x−x²/p and (12), this implies on the trace branch

\[
\begin{aligned}
123/128&<r_x/A<133/128,\\
|r_{xy}|/A&<12,\qquad 11<r_y/A<37,\qquad |r_{yy}|/A<260.
\end{aligned}
\tag{14}
\]

At x=τ(y),

\[
T_x=A\sqrt\Delta>3A/4,\qquad
T_y=\tau r_{xy}-r_y-y r_{yy}<0.
\]

For the latter sign, the sum of the two possible positive errors is
less than A(36/256+260/4096)<A, whereas r_y>11A.
Also |T_y|<75A/2. Thus

\[
\boxed{0<\tau'(y)<50.}
\tag{15}
\]

Let r̄(y)=r(τ(y),y). It follows that

\[
\left|\frac d{dy}\log r_x(\tau(y),y)\right|
<11+\frac{(10/3)50}{123/128}<192.
\tag{16}
\]

Since A<2z/45 and r̄′=r_xτ′+r_y>0,

\[
\boxed{0<\bar r'(y)<5z.}
\tag{17}
\]

### 3.3 Native probability domain

On the whole rectangle |x|<1/4, |y|≤ε, the geometric argument
p²(1+x) lies in (1/4,1/2), while v² lies in (1/3,2/5).
Consequently ℓ(p²(1+x))>3/4 and B>4/5; both are less than one.
Also A_det>3/4 and A_det<1. Hence

\[
\boxed{z<r(x,y)<2z,}
\tag{18}
\]

because
r=z(B+A_det)−z²BA_det>z(31/20−z)>z.
The entire trace branch therefore remains in the same native
probability chart.

## 4. Uniform control of every fixed finite cap

At fixed actual internal parameters let

\[
\begin{aligned}
g_N(r)&=\alpha[\kappa-\beta h_\varphi(r)]E_N(\beta r),\\
E_N(t)&=\sum_{j=0}^{N-1}t^j,\\
h_\varphi(r)&=-r\log_\varphi r-(1-r)\log_\varphi(1-r).
\end{aligned}
\tag{19}
\]

The consumed unit-charge premises are α>0, 0<β≤1 and κ>53.
They are not assumed for arbitrary reassigned physical prices.
Different caps may have different actual parameters satisfying these
premises; no infinite bank or common lower bound on α is used.

For z<r<2z,

\[
0<h<2,\qquad 18<h'<40,\qquad |h''|<6/z.
\tag{20}
\]

For the lower bound on h′, use
(1−r)/r>2¹⁹−1>2¹⁸ and log_φ2>1.
For h″, use ln φ>1/3 and (1−r)⁻¹<2.

For N=1, g₁′=−αβh′<0. For all finite N≥2,

\[
\frac{g_N'}{\alpha\beta}
=[\kappa-\beta h]E_N'-h'E_N
>51-\frac{40}{1-2^{-19}}>10.
\tag{21}
\]

Thus every fixed cap has nonzero slope throughout (18), not only at
the null point.

For the logarithmic derivative, N=1 gives
|g₁″/g₁′|=|h″|/h′<1/(3z).
For N≥2, set J=κ−βh>51 and D_N=JE_N′−h′E_N. On the chart,

\[
E_N<51/50,\quad E_N'\ge1,\quad E_N''/E_N'<9/4,\quad
D_N>JE_N'/5,\quad D_N>10.
\]

The penultimate inequality follows from
h′E_N<40·51/50≤(4/5)JE_N′. Also

\[
g_N''/(\alpha\beta)=\beta J E_N''-2\beta h'E_N'-h''E_N.
\]

The three absolute-value contributions after division by D_N are
less than 45/4, 400/51<8, and 1/z respectively. Therefore

\[
\boxed{|g_N''/g_N'|<2/z}
\tag{22}
\]

for every admitted finite cap throughout the same chart.

## 5. Exact all-order K on a common cap-independent interval

Let F_N(x,y)=g_N(r(x,y))−g_N(r₀), r₀=r(0,0), and define

\[
\begin{aligned}
a_N&=g_N'(r_0)r_x(0,0)\ne0,\\
M_N(y)&=g_N'(\bar r(y))r_x(\tau(y),y),\\
u_N(y)&=M_N(y)/a_N.
\end{aligned}
\tag{23}
\]

M_N has the same sign as a_N throughout the interval. Equations
(16), (17), (22) imply

\[
\left|\frac d{dy}\log|M_N(y)|\right|<202.
\tag{24}
\]

Since u_N(0)=1, 202ε<1/16 and exp(1/16)<16/15,

\[
\boxed{15/16<u_N(y)<16/15.}
\tag{25}
\]

Define

\[
\boxed{Y_N(y)=a_Ny/M_N(y)=y/u_N(y).}
\tag{26}
\]

Then

\[
Y_N'(y)=u_N^{-1}\left[1-y\frac d{dy}\log u_N\right]>0,
\tag{27}
\]

with the bracket between 15/16 and 17/16. Its range contains
(−15ε/16,15ε/16), hence the common target interval |Y|<2⁻¹³.
The inverse y(Y) is real analytic.

The exact matter function from the previous complete-price normal
form now has the constructive all-order parametrization

\[
\boxed{
\begin{aligned}
Y&=Y_N(y),\\
K_N(Y_N(y))
 &=g_N(\bar r(y))-g_N(r_0)-M_N(y)\tau(y).
\end{aligned}}
\tag{28}
\]

Its auxiliary section is explicitly

\[
s_N(Y)=\tau(y(Y)),\qquad \pi_N(Y)=M_N(y(Y)),\qquad
\widetilde e=\sqrt{u_N(y(Y))}\,e.
\tag{29}
\]

To verify it, let Q_N=g_N′(r̄)r_y. The trace gives τM_N=yQ_N,
so π_N=F_{N,x}(s_N,y) and
(Y/a_N)F_{N,y}(s_N,y)=τ=s_N, exactly.

There is also an exact derivative formula on the whole interval:

\[
\boxed{
K_N'(Y_N(y))
=\frac{[g_N'(\bar r(y))]^2}{a_N}
 r_x(\tau(y),y)r_y(\tau(y),y).
}
\tag{30}
\]

Indeed the derivative of the right side of (28) with respect to y is
Q_N−τM_N′; division by (27) and use of τM_N=yQ_N gives (30).
The identity extends analytically through y=0.

This is an explicit parametrization, not a Taylor approximation, a
new fitted interaction, or a declaration that densities are free
coordinates. Uniformity is proved in the dimensionless density chart
and the derived auxiliary section. It does not supply a uniform
physical-preparation Hessian inverse, uniform full-field neighborhoods
for all lattice sizes, or a continuation across a change of record
support. For a genuinely factorized finite ledger the construction
applies separately at each site, with its actual fixed cap.

## 6. The invariant xy and a unique radial representative

A positive radial coframe scaling acts as

\[
(x,y)\longmapsto(ux,y/u),\qquad u>0.
\tag{31}
\]

It preserves I=xy and the signs of x and y. The product alone does
not distinguish the two sign quadrants. On the trace branch,

\[
I(y)=y\tau(y)>0\quad(y\ne0),\qquad
I'(y)=\tau(y)+y\tau'(y).
\tag{32}
\]

The sign of I′ is the sign of y. Consequently each

\[
0<I<I_*:=\min\{\epsilon\tau(\epsilon),(-\epsilon)\tau(-\epsilon)\}
\tag{33}
\]

has a unique trace representative in each same-sign quadrant,

\[
y=y_\sigma(I),\qquad x=\tau(y_\sigma(I)),\qquad
\sigma=\operatorname{sgn}y.
\]

The endpoints in (33) are explicit algebraic numbers from (7).
For an original pair on the same admissible orbit, its required
coframe scale is

\[
\boxed{u_{\rm orbit}=y_{\rm original}/y_\sigma(I)>0.}
\tag{34}
\]

This representative is independent of the outer valuation. The scale
u_orbit should not be confused with the auxiliary normalization u_N
in (23).

The signed quantity y√(τ(y)/y) is analytic through zero and squares
to I. Thus I itself is not a nonsingular coordinate at the null point.
No independent-density assumption is hidden in this orbit construction.

## 7. Exact partial minimization of the actual price

At a trace representative, the second radial derivative of r is

\[
\frac{d^2r}{dt^2}
=xT_x-yT_y=T_x[\tau(y)+y\tau'(y)].
\tag{35}
\]

Its sign is the sign of y. Since dr/dt=0 there,

\[
\boxed{
\operatorname{sgn}\frac{d^2g_N(r)}{dt^2}
=\operatorname{sgn}(g_N'(\bar r)y).
}
\tag{36}
\]

These signs refer to the actual original price, before dividing by a
curvature coefficient:

| Branch | N=1, with g₁′<0 | N≥2, with g_N′>0 |
|---|---|---|
| y>0, x>0 | Strict radial maximum | Strict radial minimum |
| y<0, x<0 | Strict radial minimum | Strict radial maximum |

The extremum is unique on the connected orbit segment inside
|x|<1/4, |y|≤ε. Indeed the other quadratic root exceeds 1/4, so
sign T=sign(x−τ(y)) there. On x=I/y, the monotonicity of I(y)
shows a single sign change of T: from negative to positive on a
positive orbit as the radius increases, and the reverse on a negative
orbit. Each g_N remains strictly monotone throughout the rectangle
by (18), (21). Thus these are also the unique global extrema on the
specified connected orbit segments, not over arbitrary coframe shapes
or over the full model.

For a genuinely factorized ledger

\[
S=B_{\rm tot}+\sum_i m_i g_{N_i}(r_i),\qquad m_i>0,
\tag{37}
\]

assume the previous theorem's independent sitewise homogeneity and
product domain of actually free coframes. Held collar coframes remain
unchanged; the baseline may retain other sources but is independent
of these free radial directions. If every site lies on its minimizing
sign branch, (34) gives the unique joint minimum on the corresponding
product of admitted orbit segments. The exact profiled price is

\[
\boxed{
S_{\rm radial}
=B_{\rm tot}+\sum_i m_i g_{N_i}(\mathcal R_{\sigma_i}(I_i)),
\quad
\mathcal R_\sigma(I)=r(\tau(y_\sigma(I)),y_\sigma(I)).
}
\tag{38}
\]

The minimizing representatives are common to all cap valuations in
the same monotonicity class. At nonzero I, stationary envelope
differentiation yields the remaining full sources. It does not show
that those sources vanish.

If the actual query is y=ση²q_mat, the sign must come from that
dictionary. Positive y cannot be identified with timelike or
positive-energy matter by convention. The one-stage sign reversal
prevents an unconditional all-cap minimization claim.

### 7.1 The controlled null endpoint

Let r_x0=r_x(0,0)>0 and r_y0=r_y(0,0)>0. Since
τ′(0)=r_y0/r_x0 and r̄′(0)=2r_y0,

\[
\boxed{
\mathcal R_\sigma(I)
=r_0+2\sigma\sqrt{r_{x0}r_{y0}}\,\sqrt I+O(I).
}
\tag{39}
\]

For the minimizing sign σ=sign g_N′(r₀),

\[
g_N(\mathcal R_\sigma(I))-g_N(r_0)
=2|g_N'(r_0)|\sqrt{r_{x0}r_{y0}}\,\sqrt I+O(I)>0
\]

for sufficiently small I>0. This is an exact nonlinear continuation
of the leading constrained AM–GM minimum. The profile is generally
not analytic in I at zero; its signed-root parameter is analytic.
This does not conflict with analytic K_N(Y), which uses a different
coordinate and a stationary representation.

## 8. Uniform response as a full-field consumer

Fix internal parameters, the admitted full field manifold, actual
fixed weights m_i, and the complete functions r_i on it. Define

\[
S_0=\sum_i m_i r_i,\qquad S_g=\sum_i m_i g(r_i).
\]

At a configuration q_* where r_i(q_*)=r_* for every site,

\[
\boxed{dS_g(q_*)=g'(r_*)dS_0(q_*).}
\tag{40}
\]

This holds for every ambient admitted variation, not only variations
preserving uniform response. Therefore an actual full critical point
of S₀ with uniform response is common to all such S_g; conversely
when g′(r_*)≠0. It applies also at r_*≠r₀ if an actual full
configuration has been constructed.

The full Hessian identity at that point is

\[
\boxed{
H_{S_g}=g'(r_*)H_{S_0}
       +g''(r_*)\sum_i m_i\,dr_i\otimes dr_i.
}
\tag{41}
\]

Thus common critical points need not have common stability.
With an additional source-bearing baseline B the source is
dB+g′(r_*)dS₀; separate vanishing is sufficient, while a cancellation
for one cap does not automatically persist for another.

Different sitewise outer valuations require their actual derivatives
at r_* to have the common proportionality of the seed weights.
Uniform response does not equalize arbitrary readiness factors.
If internal parameters vary, their price, weight and dictionary
derivatives must also be retained. Equation (40) is explicitly a
fixed-internal-parameter field theorem.

## 9. Result and boundary of the result

The literal detector supplies an explicit nonzero trace branch,
an all-order complete-price matter function on a common cap-independent
density interval, and exact partial minimization over actual free
coframe radii. The shared optimizing orbit representative is determined
by xy and its sign branch; its endpoint behavior is controlled.

All remaining original fields and sources remain part of the problem.
No matter connection, altered measure, new information law or physical
field was introduced. A new full finite-lattice nonnull solution has
not been obtained from the trace equation alone. The separate
[nonnull continuum construction](A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE_2026_10_21.md)
provides a concrete full-field consumer under its explicitly declared
continuum dictionary; it does not assert original lattice binding.
