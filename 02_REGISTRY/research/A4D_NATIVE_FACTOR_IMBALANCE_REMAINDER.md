# Constrained factor imbalance: the whole two-tick remainder and its ten-slot defect

Parent: existing #310, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input SOURCE: `1555a67779d42a78108a0525dd5dc1a3a580c136`.
Main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`. Date: 2026-10-12.

**Result.** At the literal recorded golden operation, the first derivative of
its **complete two-tick feedback price**, allowing every orthogonal operator
jet and every constant-rank orthogonal readout jet, factors through one
explicit eigenphase jet. Readout motion and isospectral operator motion give
zero. This is stronger than the previous fixed-compression calculation.
A moving positive pairing contributes through the same formula in an actual
orthonormal frame; mere frame transport cannot supply a missing stress.

For the existing positive Hodge binding on the volume-preserving factor
curve, the full two-term bootstrap derivative is

\[
 \boxed{\mathcal B'_{\rm tf}=2(E_1-E_2)+C_\varphi\sigma_{\rm tf}.}       \tag{1}
\]

Here the energies use **one-based** axes 1,2 (axes 0,1 in the checker),
not a new spectrum. The recorded golden remainder is
\(R'_{\rm tf}=C_\varphi\sigma_{\rm tf}\), not the heat derivative.
For a preparation transporting the fixed native gate, \(\sigma_{\rm tf}=0\)
and the actual full remainder is zero. At the specified anisotropic flat
metric the first term is uniformly greater than \(1/10000\). The flat
Einstein covector is zero in all ten slots. Thus this prepared class fails
the flat first-jet comparison. A coupled preparation has to supply a
**nonzero, explicitly quantified eigenphase/source jet**, or another genuinely
owned remainder; it cannot obtain it by moving a frame or readout alone.

The named missing module is the pullback of that eigenphase covector from
an independently admitted joint preparation on `(q,D,b,m)`, together with
any other actually present price terms. The calculation does not construct
that preparation, prove its nonexistence in the whole core, or install the
required jet as a definition. T0, GR and the original terminals remain open.

There is also a **moving-record** continuation, using the previously built
actual normalized input curve of the same golden gate. Its observer moves
with the factor probe. The complete reference remainder is then
\(-4E_1E_4/(apL^2)\), rather than zero. It cannot cancel the order-one shape
response; the total derivative is still greater than \(1/10000\), uniformly
in L. Section 5 derives a uniform finite contrast from this explicit component.

## 1. The action and the complete local operator domain

Consume BOOK_03's bootstrap in its already used two-tick experiment:

\[
 H_Q=\beta^{-1}\log\left(16\sum_{k\in(\mathbb Z/L)^4}
                 e^{-\beta z(k)^*Q^{-1}z(k)}\right),\qquad
 J(P,U)=-\log\det(I-z F),
\]
\[
 Z=U^2,\qquad F=PZ^*(I-P)ZP,\qquad \mathcal B=H_Q+J.                \tag{2}
\]

The heat is the **full** constant-positive-metric Hodge/CAR heat already
proved in [the positive heat owner](A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md).
All sixteen grades, every site, every Fourier and zero mode remain.
Use the same full cochain space for both terms. In a W_Q-orthonormal frame,
choose four fixed coordinate slots (for example the four degree-one slots
at one fixed site), put the recorded block on them, and retain an arbitrary
orthogonal operator on all remaining slots. The heat is still the complete
Hodge operator; it is not block-filtered to those four slots. The feedback
projector below has rank two and its complement is the entire remaining
space. No cochain or determinant factor is removed or added. This is a
fully specified mathematical common preparation class for the existing
bootstrap, with the actual recorded matrix as its block. Its physical
admission, locality and matter/apparatus binding are not inferred from that
embedding. Equation (2) is not an identification of every D0 action term
with this bootstrap.

Fix \(a>0,p>0,a^2=p,p+p^2=1\), and \(0<z<1\); then
\(4zp^3<1\). The actual native matrix in order `(00,01,10,11)` is

\[
 U_\varphi=\begin{pmatrix}
 a&0&-p&0\\0&a&0&-p\\0&p&0&a\\p&0&a&0
 \end{pmatrix}.                                                   \tag{3}
\]

The feedback projector used by the previous price calculation is
\(P=\operatorname{diag}(1,1,0,0)\). It is **not** the owned blank-input
plane \(P_{\rm blank}=\operatorname{diag}(1,0,1,0)\). The latter remains
an independently checked control; no operational identification of these
projectors is inferred. Include any additional archive as
\(U_0=U_\varphi\oplus U_A\), with arbitrary orthogonal \(U_A\), and
\(P_0=P\oplus0\). This covers all sizes of this block base, not all possible
native base operators.

Allow an arbitrary differentiable curve of orthogonal U and orthogonal
constant-rank P through this base. Write

\[
 \dot U=K U_0,\quad K^T=-K,\qquad
 \dot P=[G,P_0],\quad G^T=-G.                                    \tag{4}
\]

These parameterize all such first jets. For the projector, differentiating
\(P^2=P=P^T\) gives a symmetric off-diagonal block; conversely every such
block is a commutator (4). No fixed-compression restriction is imposed here.
The curve is in a declared finite operator domain; native operation
admission is not obtained by parameterizing it.

## 2. Whole-remainder derivative, including a moving projector

Let \(v=(e_0+e_1)/\sqrt2\), \(w=(e_2+e_3)/\sqrt2\), extended by zero
on the additional archive. Define the rank-two projector
\(\Pi_+=vv^T+ww^T\) and

\[
 \sigma=w^T K v
        =-\tfrac12(K_{02}+K_{03}+K_{12}+K_{13}).                    \tag{5}
\]

On span(v,w), (3) is the rotation
\(\left(\begin{smallmatrix}a&-p\\p&a\end{smallmatrix}\right)\);
on its two-dimensional complement in the native block it is a symmetric
reflection. Thus \(\cos(2\theta)=p-p^2=p^3\),
\(\sin(2\theta)=2ap\). At the base

\[
 F_0=4p^3 vv^T,
 \quad M^{-1}:=(I-zF_0)^{-1}=I+{z\over1-4zp^3}F_0.                \tag{6}
\]

The determinant on the whole carrier is \(1-4zp^3>0\); all other factors
are one and retained. Differentiate the **actual** expression (2):

\[
 \dot Z=K U_0^2+U_0KU_0,
\]
\[
\begin{split}
 \dot F={}&\dot P Z^T(I-P)ZP+P\dot Z^T(I-P)ZP
       -PZ^T\dot P ZP\\
      &+PZ^T(I-P)\dot ZP+PZ^T(I-P)Z\dot P .                       \tag{7}
\end{split}
\]

Jacobi's determinant formula and the positive log domain give
\(\dot J=z\operatorname{tr}(M^{-1}\dot F)\).
The three projector terms in (7) have total contraction zero for every G.
For the operator terms, direct multiplication gives

\[
 \boxed{\dot J=C_\varphi\sigma,\qquad
 C_\varphi={8zap(p-p^2)\over1-4zp^3}>0.}                          \tag{8}
\]

Here is a dimension-independent contraction proof. Put s=2ap and c=p-p^2.
Then \((I-P)Zv=sw\), while the other active basis vector has zero leakage.
For the operator jet, \(w^T\dot Zv=2c\sigma\), so the Jacobi contraction is
\(2zs(2c\sigma)/(1-zs^2)\), which is (8). For the projector jet put
\(d=w^T\dot Pv\). The two outer projector terms contribute \(2scd\)
in this only nonzero channel and the middle term contributes \(-2scd\).
The other active diagonal contraction is zero. The additional archive is
orthogonal to this base channel, so it contributes zero in both arguments.

This is a full covector calculation, not a source defined by its intended
answer. An explicit verification without a numerical spectrum is obtained
by writing the six upper-triangle entries of the native block of K: the
entries 02,03,12,13 each have coefficient
\(-4zap(p-p^2)/(1-4zp^3)\), and 01,23 have coefficient zero.
All entries touching the additional archive have coefficient zero because
(6) and the base cross blocks are supported on the native block. This support
argument proves the assertion for arbitrary finite archive size and arbitrary
\(U_A\); finite cases are independent checks of that analytic proof.

There is also the basis-independent expression on this base

\[
 \sigma=-{1\over2p}\operatorname{tr}(\Pi_+\dot U).                 \tag{9}
\]

For \(\dot U=[K_0,U_0]\), this trace is zero by cyclicity and
\(\Pi_+U_0=U_0\Pi_+\). This includes all isospectral frame-conjugation
jets; it does not include arbitrary eigenphase-changing orthogonal jets.
Changing P alone is already covered by (7). For the blank-input projector,
**the different** feedback is \(F_0=p^2P_{\rm blank}\), and the full derivative
is \(4zap\sigma/(1-zp^2)\). The two prices/projectors may not be substituted
for each other, although both readout derivatives vanish at this base.

For a positive pairing W(t), take a differentiable frame B(t) with
\(W=B^TB\) and use \(\widetilde U=BUB^{-1}\),
\(\widetilde P=BPB^{-1}\). Weighted adjoints become transposes; the feedback
pencil is conjugated and has the same determinant on the whole space.
Equations (4)--(9) apply to these **actual framed jets**, including B'.
If U and P are simply transported from fixed matrices, their framed price
is constant and \(\sigma=0\). Positivity of W alone does not prove that the
native preparation transports fixed matrices or preserves their spectrum.

For the literal native block there is a further forced statement, not an
extra spectral assumption. Differentiating its two golden identities gives
\(2a\dot a=\dot p\) and \((1+2p)\dot p=0\). Since a,p are positive,
\(\dot a=\dot p=0\). A new freely varied gate angle would leave that native
golden family. A nonzero \(\sigma\) must therefore be derived from the actual
**whole** field-dependent preparation/composition or another owned term;
changing the primitive golden root to meet (17) is not an available repair.

## 3. Actual joint carrier and the factor tangent

On every identity dressed link use the same Lorentz metric at both endpoints:

\[
 q(t)=\operatorname{diag}(4e^{2t},-e^{-2t}/4,-1,-1),\quad D_e(t)=I,
 \quad b_e(t)=0,\quad m_x(t)=0.                                  \tag{10}
\]

It lies in the complete [joint kinematic image](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md).
Its first jet \(V_q=\operatorname{diag}(8,1/2,0,0)\) satisfies

\[
 DV_{q,t}D^T+\dot Dq_tD^T+Dq_t\dot D^T=V_{q,s},
 \qquad\operatorname{tr}(q^{-1}V_q)=0.                            \tag{11}
\]

Thus this is not an ambient metric partial with a frozen endpoint. The
transported readout is unchanged by the identity link and is spatially
constant; its Levi-Civita curvature and the finite flat-link Palatini action
are exactly zero. Consequently the completed probe density
\(\rho_0=-\tfrac12\sqrt{|g|}\operatorname{pack}(G^{\mu\nu})\)
is zero in every slot for these constant Lorentz metrics. This uses the
fixed normalization of [the finite probe owner](A4D_NATIVE_FINITE_PROBE_COMPLETION.md),
not a fitted source or an on-shell example.

There is an explicit kinematic positive-pairing realization of the same
factor curve without mistaking positive Q for Lorentz q. Keep the actual
recorded output `(a,0,0,p)` and its previously derived observer
\(n=(1,0,0,p^3)/(2ap)\). Set

\[
 B=\begin{pmatrix}\gamma&0&0&-\gamma p^3\\0&1&0&0\\
 0&0&1&0\\-\gamma p^3&0&0&\gamma\end{pmatrix},\quad
 \gamma=(2ap)^{-1},\quad h(n)=B^TB.
\]

Then \(B\eta B^T=\eta\) and \(Bn=e_0\). In the raw row convention put
\(F(t)=\operatorname{diag}(2e^t,e^{-t}/2,1,1)B\). Direct substitution gives

\[
 F\eta F^T=q(t),\quad Q(t)=Fh(n)^{-1}F^T
    =\operatorname{diag}(4e^{2t},e^{-2t}/4,1,1).                   \tag{12}
\]

The inverse h is compulsory in this convention: if the observer transforms
contragrediently, \(h'=\Lambda^Th\Lambda\), so \(Fh^{-1}F^T\) is invariant.
The positive compound pairing W_Q may then be used in the already named
Hodge test. The heat differential is unchanged on this identity-link path.
This proves a nonempty **kinematic component**, not physical admission of the
compound heat or a law joining the recording apparatus to sixteen-component
matter. The retained record is not silently identified with m=0. That
apparatus/matter/action preparation is still a missing native arrow.

## 4. All ten coefficients and the full trace-free remainder

At positive diagonal \(Q=\operatorname{diag}(q_1,q_2,q_3,q_4)\), consume the
whole Fourier calculation, now with its full feedback covector:

\[
 d\mathcal B[V]=\operatorname{tr}(A_H V)+C_\varphi\,\sigma[V],
 \quad (A_H)_{rr}=E_r/q_r,\quad
 (A_H)_{rs}=E_rE_s/(4L^2)\ (r\ne s).                             \tag{13}
\]

Here \(\sigma[V]\) is the derivative (5) of an actual preparation, if one is
owned; it is not a freely added angle. For a constant-metric chart, denote
its symmetric covector by \(A_\sigma\). There are ten independent coefficients
of this pullback, despite the operator derivative factoring through one
scalar. One may not infer a one-dimensional physical source space from (8).
The covector's packed off-diagonal entries are **twice** its matrix entries.

The metric trace-free part is

\[
 A_{\rm tf}=A-\tfrac14\operatorname{tr}(AQ)Q^{-1},\qquad
 (A_{\mathcal B})_{\rm tf}=(A_H)_{\rm tf}
                         +C_\varphi(A_\sigma)_{\rm tf}.          \tag{14}
\]

Coordinate trace zero is not the condition. On (12),
\(V_Q=\operatorname{diag}(8,-1/2,0,0)\), so

\[
 H'_{\rm tf}=2(E_1-E_2)>1/10000\quad
    (\beta=\log2,\ L\ge2),\qquad R'_{\rm tf}=C_\varphi\sigma[V_Q]. \tag{15}
\]

The strict all-L bound is twice the already proved analytic bound; the checker
recomputes the exact full-mode coefficients for L=2,4. The bound does not
select beta as a native temperature. The earlier scaling extends the test
to each fixed positive beta, with its specified beta-dependent test metric.

**All ten Lorentz q probes on one specified joint lift.** A Q covector is
not automatically a q covector. At the base of (10)--(12), for each symmetric
Lorentz Gram probe V put \(H_V=\tfrac12Vq^{-1}\) and use the actual global
raw-solder curve \(F_V(t)=e^{tH_V}F(0)\), with the same fixed recorded
observer and dressed links D=I. Its endpoint Grams agree on every edge and
have derivative V. Its pairing derivative is

\[
 \delta Q=\tfrac12(Vq^{-1}Q+Qq^{-1}V)
          =\tfrac12(V\eta+\eta V),\qquad
 A_H^q=\tfrac12(\eta A_H+A_H\eta).                               \tag{15a}
\]

This computes all ten coefficients on these genuine joint tangent lifts:
the time diagonal is E_1/4, the three spatial diagonals are -E_r/q_r,
the three time-space coefficients are zero, and the three spatial mixed
packed coefficients are -2E_rE_s/(4L^2). Every physical q curve is spatially
constant, so all ten physical rho0 coefficients on the same probes are zero.
The shape contraction is still 2(E_1-E_2), and
\(\operatorname{tr}(A_H^q q)=\sum_r E_r\). The zero time-space entries are
properties of this **specified observer/coframe lift**, not a theorem
discarding those three native equations. A different matter/observer lift
has its own delta-h contribution. This component does not fix that native
choice or identify the retained record with the sixteen-component matter.

For fixed-gate frame preparations the right side of the remainder is **zero**.
Both scalar prices have really been differentiated. This whole two-term
bootstrap is neither stationary on (11) nor equal to the zero flat Einstein
covector. Fixed binary-passport scene prices and the literal fixed-depth
archive action have zero derivative by their owners; adding them leaves
this result unchanged. Any volume-only term has zero contraction on (11).
A variable weighted scene outside its binary passport, other feedback words,
a matter/source action, temperature/fugacity/normalization variations, or
other retained contributions require their **own** derivative. They are
not silently included in the computed zero remainder.

In the positive-Q chart, if such extra terms have covector \(A_\xi\), the
exact necessary condition for a flat match with any fixed nonzero calibration is

\[
 C_\varphi(A_\sigma)_{\rm tf}+(A_\xi)_{\rm tf}
                         =-(A_H)_{\rm tf},                     \tag{16}
\]
\[
 C_\varphi\sigma[V_Q]+\xi[V_Q]=-2(E_1-E_2).                       \tag{17}
\]

Equations (16)--(17) name the missing source module, not a constitutive law.
For the actual Lorentz Gram probes (15a), use instead
\(C_\varphi(A_\sigma^q)_{\rm tf}+(A_\xi^q)_{\rm tf}
=-(A_H^q)_{\rm tf}\), with trace subtraction using q. The checker records
both ten-slot tables separately and rejects identifying them. The same
factor contraction (17) is valid in both charts.
A first-jet mismatch alone is not a uniform finite secant bound. The prior
uniform half-contrast obstruction applies when the remainder is actually
constant on the full paired probe (for example fixed framed P,U and
volume-only terms); it may not be inferred merely from \(\sigma[V_Q]=0\).
Native h-dependent normalization and admission retain their old boundaries.

For the general joint preparation use the previous intrinsic normal form.
If \(\sigma\) or another actual term has ambient coefficients
\((A_s,A_t,B_D)\), let \(M=B_D(q_s^{-1}D)^T\). Its restricted coefficients are

\[
 \operatorname{sym}(A_s+M/2),\quad
 \operatorname{sym}(A_t-D^TMD/2),\quad \operatorname{skew}(M),       \tag{18}
\]

plus all b,m coefficients. Thus (16) is applied **after** substitution in
(18), not to an ambient q partial. Its link part and the b,m equations remain;
lift independence cannot be asserted before those equations or an owned
lift law. The checker verifies all 24 link basis directions (six per axis),
all ten symmetric metric slots and conormal invariance in this chart.
This does not compute their unknown native operator pullback.

## 5. An actual moving-record coupling: remainder, refinement order and contrast

The fixed observer is not the only existing component available for this
test. Use the genuine normalized input curve already owned in
[the recorded observer packet](A4D_NATIVE_RECORDED_OBSERVER_PREPARATION.md):

\[
 u(t)={1-t^2\over1+t^2},\quad v(t)={2t\over1+t^2},\quad
 \Psi(t)=(au(t)-pv(t),0,0,pu(t)+av(t)).                            \tag{19}
\]

It stays faithful on \(|t|\le1/10\), with both nonzero output amplitudes
at least \(\ell=217/505\). Its own positive observer form h(t) is smooth,
\(\ell^2 I\le h(t)\le\ell^{-2}I\), and its already derived jet has
\(h'_{00}=h'_{33}=-2a/p^2\),
\(h'_{03}=h'_{30}=2a(1+p^2)/p^3\). In the **fixed base rest frame** B of
(12), direct substitution gives

\[
 B^{-T}h'(0)B^{-1}={4\over ap}(e_0e_3^T+e_3e_0^T),
 \quad \nu:=B n'(0)=(0,0,0,-2/(ap)).                             \tag{20}
\]

This rest-frame differentiation uses B at zero, not a moving rest frame
that would erase the physical observer jet. Keep the raw solder factor
curve and set \(Q_{\rm coupled}(t)=F(t)h(t)^{-1}F(t)^T\).
Relative to the fixed-observer heat, its extra Q jet has only
\(\delta Q_{03}=\delta Q_{30}=-8/(ap)\). Define a **decomposition of the
same existing price**, not a counterterm,

\[
 R_{\rm ref}(t):=J(t)+H(Q_{\rm coupled}(t))-H(Q_{\rm fixed}(t)).
\]

The framed gate is fixed, so J'=0. The whole remainder on the factor tangent
and the complete bootstrap derivative are exactly

\[
 \boxed{R'_{\rm ref,tf}=-{4E_1E_4\over apL^2},\qquad
 \mathcal B'_{\rm coupled,tf}
       =2(E_1-E_2)-{4E_1E_4\over apL^2}.}                       \tag{21}
\]

Thus the archive/record response has actually been included; it was not
declared fixed to obtain the first class. This is a correlated kinematic
preparation component, not a native law forcing the correlation t in (19)
to equal the factor parameter. It does not supply a matter action or source
subtraction, or identify its four-coordinate record with the full m fibre.

There is an all-L proof that this actual coupling cannot cancel the shape
source. The existing bounds a>3/4, p>3/5 give \(|\nu_3|<5\).
For the fourth axis q_4=1, the same complete-mode estimates as before give

\[
 E_4\le128{r_{16}(1+r_{16})\over(1-r_{16})^3}<1/256,
 \quad r_{16}=2^{-16}.
\]

Since L>=2, \(|R'_{\rm ref,tf}|\le(5/2)E_1E_4<(5/512)E_1\).
With the already proved E_1 lower and E_2 upper bounds,

\[
 \mathcal B'_{\rm coupled,tf}\ge{1019\over512}E_1-2E_2
 >{1019\over512}{60\over17\,2^{16}}
       -{1024r_{64}(1+r_{64})\over(1-r_{64})^3}
 >1/10000.                                                      \tag{22}
\]

More generally, at this observer rest base **every** bounded unit-observer
jet has \(\nu_0=0\), \(\delta h_{0i}=-2\nu_i\), and

\[
 dH_{\rm observer}
       ={1\over L^2}\sum_{i=2}^4\sqrt{q_1q_i}\,E_1E_i\,\nu_i.    \tag{23}
\]

Each E_i is uniformly bounded at fixed positive beta and fixed positive
q_i, by the same geometric-series estimate. Thus bounded observer jets
give O(L^-2), and cannot cancel (15) in a refining family. A derivative
growing like L^2 or a different heat/field law falls outside this bound;
native preparation bounds are not inferred from kinematic compatibility.
For the explicit curve (19) its regularity and bound are proved, not assumed.

**Actual finite contrast.** To use precisely linear physical probes replace
the factor exponential in F by
\(S_{\rm lin}(t)=\operatorname{diag}(2\sqrt{1+2t},
\sqrt{1-2t}/2,1,1)\), and let \(F_{\rm lin}=S_{\rm lin}B\).
Then the physical Gram is exactly q(0)+tV_q; its +/- endpoints have the
same determinant. The first jets and (21)--(22) are unchanged. Couple (19)
on the same \(|t|\le1/10\) interval. Its full positive Q and Q^-1 have
uniform matrix bounds and derivatives through order three, independent of L,
because the recorded amplitudes have the explicit positive lower bound ell.

Here is the required uniform spectral argument. If k has folded coordinates
j_r=min(k_r,L-k_r), put x_k=|z(k)|^2. Uniform positivity supplies
\(\lambda_k(t)\ge\kappa x_k\ge16\kappa\sum_rj_r^2\) for one kappa>0.
The three mode derivatives obey \(|\lambda_k^{(r)}|\le C_r x_k\).
Also \(x_k\le4\pi^2\sum j_r^2\), with at most 16 modes per folded tuple.
The zero mode keeps the partition at least one after the common grade factor.
Every normalized moment needed for the first three heat derivatives is
therefore bounded by a convergent sum of a fixed polynomial in \(\sum j_r^2\)
times \(e^{-16\beta\kappa\sum j_r^2}\). The convergence follows directly
from \(j^2\ge j\) and the polynomial-weighted geometric series. This proves
\(\sup_L\sup_{|t|\le1/10}|\mathcal B_L'''(t)|<\infty\).
The framed feedback is constant throughout, so no omitted feedback jet
enters this bound. Taylor's theorem now gives

\[
 \Delta\mathcal B_L(\epsilon):=
   {\mathcal B_L(\epsilon)-\mathcal B_L(-\epsilon)\over2}
   =\epsilon\mathcal B_L'(0)+O(\epsilon^3),
 \quad \Delta\mathcal B_L(h^{1/3})\ge {h^{1/3}\over20000}           \tag{24}
\]

for all sufficiently fine h=1/L (including the required L in 4N).
The fixed-zero-source physical flat Palatini half contrast is exactly zero.
For one fixed calibration a_cal!=0 the literal unrescaled bootstrap has a
gap at least \(h^{1/3}/(20000|a_{\rm cal}|)\); O(h) recording errors cannot
remove it. Physical admission, own matter/source subtraction and native
normalization remain conditions for applying this comparison to D0.
In particular multiplying the price by h^2 changes the estimate, and an
unproved source may not be fitted to it. This quantitative result closes
the proposed bounded recorded-observer compensator **in this named binding**,
not every joint preparation or the original raw-owner task.

## 6. Hostile controls and what must now be solved

The actual orthogonal curve
\(U(t)=e^{tJ_+}U_\varphi\),
\(J_+=wv^T-vw^T\), has \(\sigma=1\) and \(J'=C_\varphi>0\).
It keeps every carrier coordinate and the positive pencil locally, but
changes the golden eigenphase. It is a **mathematical control**, not an admitted
native operation or a new phase law. Choosing its speed to cancel (15) proves
only that orthogonality and the carrier constraint do not force (16); it
prevents promotion of the fixed-gate result to a whole-core obstruction.
The checker uses this independent curve and arbitrary nonzero ten-slot
first jets to reject a ledger claiming that cancellation was derived.

The next theoretical step is specific: obtain the actual framed operator
jet from the already owned joint preparation on `(q,D,b,m)`, evaluate (5),
and (if other terms are present) evaluate their intrinsic remainder in (18).
For a spectrum-preserving recorded-golden preparation, the feedback side is
now fully settled and cannot cancel the Hodge shape source. For a genuine
non-isospectral native preparation, its eigenphase covector must meet (16)
from its own equations; it cannot be assigned from rho0. This is the remaining
binding question, without a new role, word census, archive minimum or free
spectral selector. The curved comparison, own matter/Ward, native Euler
stationarity, soundness/recovery and physical limitations are downstream.

Run `python3 02_REGISTRY/research/certificates/a4d_native_factor_imbalance_remainder_check.py`.
The generic determinant, arbitrary-archive support, positive-pairing frame,
kinematic Lorentz/observer and all-L arguments above are analytic. The checker
is exact finite algebra with pinned existing Lean inputs; it introduces no
new Lean theorem and makes no kernel-formalized all-size claim. Original
#310 fixed-source/raw-owner, #202 and #317 contracts stay unchanged.
