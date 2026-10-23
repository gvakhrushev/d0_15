# Unique native preparation and the full reduced field source

21 October 2026. Bounded research continuation of existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Inspected source head: `92c00ccbf39e6e21e4383f7a7b573ab7c7c6f1be`.

**Status.** New analytical proof with narrow exact/numerical controls;
independent review and repository CI have not yet been performed. The result
concerns the original full128 cap2 coherent conditional-information price,
not the different N=1 two-query CQ programme. No Book/CORE/assembly claim is
promoted. Physical Book valuation, native admissibility, full joint GR and
refinement-uniform bounds remain open.

## 1. The actual new consumer

The earlier logarithmic-preparation packet established a restricted minimum
and its value asymptotics. A small value correction is not a bound on its
field derivative. This proof supplies the missing differentiated reduction:

* the restricted preparation is locally **unique**, even through new rank
  births; a finite preparation Hessian is not assumed;
* the reduced price is C1 and its complete source is the envelope source;
* all geometric and both material types of variations are retained;
* a new mixed term, invisible on the former special waveform, is necessary;
* the geometric correction is O(||Psi||^2/log(1/||Psi||)), while the material
  correction is O(||Psi||/log(1/||Psi||)); their coefficients are derived;
* at the matter-free centre the actual linearized field Euler operator is
  unchanged, not merely the second Taylor value along a single path.

These are statements about ONE specified net-price component. They cannot
be substituted into the distinct N=1 CQ source theorem without its missing
same-execution/cut/valuation transport.

## 2. Fixed-mesh carrier and full ambient parameters

Use the original 256-site, CAR16, oldRIGHT128 instrument. Write r=128,
p=phi^-1, p+p^2=1. Keep the actual unequal cost20 density in D, all positive
adjoints, clocks and every cap2 leaf. Let g range over a small finite open
chart of the independent real coframe and proper-Lorentz-link coordinates
(with the original fixed collar). The strict Julia inequalities make every
Kraus amplitude analytic in g. There are 255 literal histories:

    L_gamma(g) in {K_eta(g), K_eta(g) B(g), B(g)^2 : eta != 0},
    B=I-epsilon D(g)^2/2,       sum_gamma L_gamma^* L_gamma = I.

128 leaves are identically dark Walsh operators. Every other old RIGHT
Gram at the specified vacuum centre is positive definite by the inherited
cap2 support certificate. This gives a common positive old-support gap on
one sufficiently small fixed-mesh chart. No mesh-uniform gap is asserted.

Let m=(c_z,b_z)_z be the TWO original real scalar/top amplitudes, independently
varied subject only to the open slack condition near zero. The original
normalized preparation dictionary is

    C_m(z,:) = [sqrt(p)|1> + c_z|0> + b_z|15>
                  + sqrt(p^2-c_z^2-b_z^2)|14>] f(z)^T/sqrt(r),
    C_m^* C_m=I_r/r,       ||f(z)||^2=1/2.

Thus m is not only the former one-parameter waveform. The calibrated
physical scalar differs by its already fixed Golden scale; no scale is
changed here. Holding the preparation dictionary fixed while varying g is
an ordinary independent field variation, not a claim of physical free
state preparation.

Choose k distinct sites in the former u=1/4 slice (k<=64 suffices). Use the
literal rank-eight high-CAR generators

    J_w = sum_{j=6,10,12,14} (|w,j+1><w,j|-|w,j><w,j+1|),
    U(a)=prod_w exp(a_w J_w),     C_{m,a}=U(a)C_m.

All generators commute because their DATA site supports are disjoint.
Their continuous closure is the mathematical preparation chart. Actual
finite Golden controls at all chosen addresses and their full work remain
admission conditions. We do not replace the full rank-eight operator by
one occupied two-dimensional plane in any Book trace.

For the original coherent selector define

    rho(g,m,a)=p C_m C_m^*+p^2 C_{m,a} C_{m,a}^*,
    A(g,m,a)=S_phi(direct_sum_gamma L_gamma rho L_gamma^*)-log_phi r.

This is precisely the complete coherent P--leaf--RIGHT conditional
component owned by NATIVE_COHERENT_CHOICE_SOURCE.md. It is not the pointer
entropy alone. Both ports, all failed attempts, terminal abort and the
entire oldRIGHT are present. Geometry and m are independent here; the
primary geometry g=g_primary(t), m=t m_primary may be substituted later.

## 3. Analytic small-cluster amplitudes, without an inverse on the new kernel

For each active leaf set X=L_gamma C_m and DeltaX=L_gamma(C_{m,a}-C_m).
A fixed selector rotation gives a rectangular amplitude

    V_gamma=[X+p^2 DeltaX, sqrt(p^3) DeltaX].

Its Gram has exactly the nonzero spectrum of the actual leaf state.
At a=0 its old r eigenvalues are bounded away from zero and the other r
are zero. Let E_old and E_new be the analytic spectral projectors onto
these two separated clusters of V_gamma^* V_gamma. Define

    Z_gamma=V_gamma E_new,       Z_gamma(g,m,0)=0.

Analyticity follows from the finite-dimensional resolvent contour around
the old positive cluster, not from differentiating an eigenvector at a
new zero. The entropy splits into a smooth old-cluster part and
sum_gamma S_phi(Z_gamma^* Z_gamma). Individual small eigenvalues may still
change rank. There is no eigenvalue deletion or probability floor.

Put delta C(v)=sum_w v_w J_w C_m and

    P_gamma=X (X^*X)^-1 X^*.

Differentiating the spectral projector at coincidence, or directly taking
the Schur complement of the positive old Gram, gives

    Q_{g,m}(v)=sum_gamma ||D_a Z_gamma(g,m,0)[v]||_HS^2
              =p^3 sum_gamma ||(I-P_gamma)L_gamma delta C(v)||_HS^2.   (1)

Only old faithful Grams are inverted. Formula (1) concerns the actual
small spectral mass, not a newly chosen divergence.

Every native Kraus leaf has definite CAR parity. At m=0, C_0 is odd and
J_w C_0 is even. Consequently X^*L_gamma delta C=0 for EVERY leaf and
EVERY g in the strict parity-preserving geometric chart. Completeness and
the Fourier-row norm give the exact identity

    Q_{g,0}(v)=nu ||v||^2,           nu=p^5/256.                     (2)

This is not merely an equality at one flat geometry. It implies
D_g Q_{g,0}=0 for all independent coframe/link directions.

For arbitrary small m, C_m^*delta C(v)=0 (all amplitudes are real and J_w
is skew). Disjoint site supports yield the stronger exact defect formula

    Q_{g,m}(v)=nu||v||^2
       -(p^3/256) sum_w c_w^2 v_w^2
       -p^3 sum_gamma ||P_gamma L_gamma delta C(v)||_HS^2.           (3)

The projected amplitudes in (3) vanish at m=0 and are analytic. Therefore,
uniformly on a smaller compact g chart,

    Q_{g,m}=nu I+O(||m||^2),  D_g Q_{g,m}=O(||m||^2),
    D_m Q_{g,m}=O(||m||),    Q_{g,m} >= (nu/2)I.                    (4)

Equation (3) retains the local scalar contribution, which would be lost
by extending the old special b-only waveform without recomputing its jet.

## 4. Why the preparation minimum is unique

The relevant fact is convexity in an AMPLITUDE, not in the density.
For a rectangular matrix Z with ||Z||_op<=epsilon, regularize its entropy
in natural units by

    E_eta(Z)=-Tr(Z^*Z log(Z^*Z+eta I)),     eta>0.

Its scalar singular-value function is f_eta(s)=-s^2 log(s^2+eta). With
u=s^2/(s^2+eta) in [0,1], direct differentiation gives

    f_eta''(s)=-2 log(s^2+eta)-10u+4u^2
              >= -2 log(epsilon^2+eta)-6=:c_eta,
    f_eta'(s)/s >= c_eta.

The inequality is exact: 6-10u+4u^2=(1-u)(6-4u)>=0. Hence on this ball
E_eta(Z)-(c_eta/2)||Z||_HS^2 is convex. One way to see this is to extend
the scalar difference beyond epsilon as an even convex nondecreasing
singular-value function; its spectral sum is convex. This generic matrix
convexity theorem is recorded in A.S. Lewis, Journal of Convex Analysis 2
(1995), 173--183, https://journalofconvexanalysis.com/articles/jca02012/ .
The inequality and its constants above are derived here.

Stack the actual Z_gamma in a block-diagonal amplitude. On ||a||<=R,
||Z||_op<=C R. From (1)--(4), after shrinking the common parameter chart,

    ||D_a Z[v]||_HS^2 >= (nu/4)||v||^2.

All second amplitude derivatives are bounded. Moreover
||grad E_eta(Z)||<=C_1 R(1+|log R|), uniformly for sufficiently small eta;
this follows from the bounded singular-value function s|log(s^2+eta)|.
The chain-rule curvature from the nonlinearity of Z is thus bounded below
by -C_2 R(1+|log R|)||v||^2. The old-cluster entropy has a bounded Hessian.
Combining the three terms gives, in Golden units, a lower preparation
curvature of the form

    c_1 log(1/R)-c_2-c_3 R|log R| >0

for sufficiently small R, uniformly as eta decreases to zero. Integrating
the regularized Hessian inequality along every line segment and then
passing to eta=0 proves strong convexity of the ACTUAL C1 entropy on the
small preparation ball. This argument remains valid through newborn rank
changes; it does not assign a finite Hessian at a=0.

At m=0, parity gives D_a A=0 at a=0. Strong convexity makes it the unique
minimum. The boundary gap persists for small m, so compactness gives a
unique interior minimum a_*(g,m). It is continuous in (g,m). All k genuine
preparation equations on this declared chart vanish there.

The same conclusion holds after a genuinely derived C2 extra ledger with
bounded preparation curvature and zero preparation force at m=0. This is
not permission to append a new price or to change the sign of entropy.

## 5. The full mixed material source: the missing J_w T term

Write T_m=D_m C_0[m], an even DATA amplitude. At a=0 the coherent source
is p^2 times the one-arm source. Let E_gamma=L_gamma^*L_gamma and
G_gamma=C_0^*E_gamma C_0. At m=0 both first Gram jets G_a and G_m vanish by
parity. Therefore the actual linear source matrix M(g), defined by

    s(g,m):=D_a A(g,m,0)=M(g)m+O(||m||^3),                          (5)

has the explicit rows

    (M(g)m)_w = -(p^2/ln phi) sum_gamma Tr(R_gamma,w(m) log G_gamma),
    R_gamma,w(m)=T_m^* E_gamma J_w C_0
                 +(J_w C_0)^* E_gamma T_m
                 +(J_w T_m)^* E_gamma C_0
                 +C_0^* E_gamma J_w T_m.                          (6)

The +I entropy terms cancel only in the complete leaf sum. Oddness in m
follows from simultaneous parity (m,a)->(-m,-a). The old active Gram logs
are analytic on their common positive chart.

The LAST TWO terms in (6) are essential. They vanish on the old chosen
primary waveform because its top amplitude vanishes at the actuated
site. They do not vanish for arbitrary ambient material variations.
For the hostile control E_gamma=q_gamma I, they cancel the first two
terms exactly, as they must: the one-arm entropy is then input independent.
Keeping only the first two would create a fictitious material source.

Differentiating (6) in any actual coframe/link direction keeps BOTH D R
and D log G. The latter has the full noncommuting derivative

    D log G[H]=integral_0^infinity (G+xI)^-1 H (G+xI)^-1 dx.         (7)

No simultaneous diagonalization, frozen density, or fitted coefficient is
used. The certified old source at w0 and m=t m_primary is the corresponding
entry of M m_primary; the new matrix's other entries are given by (6), not
by an invented common-site number.

## 6. Differentiated expansion, not differentiation of a little-o claim

Put r_a=||a||. The separated spectral clusters give, uniformly,

    A(g,m,a)-A(g,m,0)
       =s(g,m).a + Q_{g,m}(a) log(1/r_a^2)/ln phi + R(g,m,a),       (8)
    |R|<=C r_a^2,        ||D_(g,m) R||<=C r_a^2.                  (9)

Here is the additional proof needed for the second bound. The old cluster
has a uniform analytic Taylor expansion. For the new cluster,
Z(g,m,a)=r_a Zhat(g,m,a/r_a,r_a), where Zhat and its parameter derivatives
are uniformly bounded, including all angular directions. The coefficient
of log(1/r_a^2) is Tr Z^*Z=Q(a)+O(r_a^3), with the same parameter-derivative
bound. The remaining entropy equals r_a^2 E(Zhat). The amplitude entropy
E and its first derivative are bounded on bounded finite-dimensional sets,
including zero singular values (s log s^2 tends to zero). This proves (9).
It does not require differentiable individual small eigenvalues.

In particular, holding a FIXED during a parameter derivative,

    D_y A = D_y A(g,m,0) + (D_y s).a
       +(D_y Q)(a) log(1/r_a^2)/ln phi + O(r_a^2),                 (10)

for every geometric or material y. This is the complete source estimate
that could not be inferred from the old value-only asymptotic.

## 7. Exact elimination and its full leading source

Define F(g,m)=min_{||a||<=R} A(g,m,a), and A0(g,m)=A(g,m,0).
Uniqueness and interiority give the C1 envelope theorem directly:

    D F(g,m)=D_(g,m) A(g,m,a_*(g,m)).                             (11)

The derivative does NOT contain a neglected D a_* term: D_a A=0, and a
comparison of the unique minimizers proves (11) without assuming a_* is
differentiable. Continuity of the source follows from amplitude C1
regularity and continuity of a_*.

Let r_m=||m||>0, L=ln(1/r_m), and K=ln(phi)/(8nu). Uniform minimization
of (8) gives

    a_* = -2K M(g)m/L + o(r_m/L),
    F-A0 = -K ||M(g)m||^2/L + o(r_m^2/L).                        (12)

For clarity, the scale follows first from the lower quadratic-log bound:
a minimizing radius satisfies r_a log(1/r_a)<=C r_m, so r_a=O(r_m/L).
Substitute a=r_m v/L into (8), uniformly over unit m-directions and
bounded v. The limiting strictly convex quadratic is
M(g)(m/r_m).v +2nu||v||^2/ln(phi). Its unique minimizer proves (12),
including directions in ker M.

Now use (10), not a formal derivative of the error in (12). Equations
(4)--(5) yield the FULL geometric and material first-source formulas

    D_g(F-A0) = -(K/L) D_g ||M(g)m||^2 + o(r_m^2/L),              (13)
    D_m(F-A0) = -(2K/L) M(g)^T M(g)m + o(r_m/L).                  (14)

The extra derivative of 1/L in a formal value differentiation would be
of order r_m/L^2; it is correctly below (14)'s leading order. In (13),
D_g Q=O(r_m^2) is crucial. Freezing M would wrongly erase this entire
geometric response. All these estimates are uniform in the finite g
chart, but are NOT estimates uniform in mesh size.

At every (g,0), F=A0 and D F=D A0. Moreover the gradient correction in
(13)--(14) is o(||(delta g,m)||). Thus, wherever A0 is twice differentiable,
D F itself is differentiable at the vacuum and

    D^2 F(g,0)=D^2 A0(g,0).                                    (15)

This preserves the ACTUAL linearized field Euler operator on this chart.
It does not assert C2 regularity throughout a punctured neighbourhood.
At a nonzero matter amplitude the residual (13) is generally nonzero.
The old exact nonvacuum root is not automatically an exact root after
this internal elimination.

## 8. Scalar finite constant and a useful closed inversion

For one selected address at m=0, put X_gamma=L_gamma C_0,
Y_gamma=L_gamma J_w C_0, Z_gamma^(2)=L_gamma J_w^2 C_0. The at-most-one
new eigenvalue has coefficient

    b_gamma=p^3 ||Y_gamma||_HS^2,
    H_gamma=p^4 Y_gamma^*Y_gamma
          +(p^2/2)(X_gamma^*Z_gamma^(2)+Z_gamma^(2)*X_gamma).

Parity kills X_gamma^*Y_gamma. Hence sum b_gamma=nu and sum Tr H_gamma=-nu.
The complete constant at order a^2, in the same Golden entropy units, is

    B(g)=[nu-sum_gamma Tr(H_gamma log G_gamma)
                  -sum_gamma b_gamma log b_gamma]/ln(phi),      (16)

with 0 log 0=0. Thus A(g,0,a)-A0(g,0)=(nu/ln phi)a^2 log(1/a^2)+B(g)a^2
+o(a^2). The old support, every new mass and normalization term are kept.
No replacement of B(g) by an unspecified tuning constant is necessary.

For a chosen material ray with s=-kappa t+O(t^3), kappa>0, write
q=nu/ln(phi), c=(B/q-1)/2. The exact small positive solution of the
linear-plus-quadratic-log normal-form equation is

    a_L(t)=-kappa t/[4q W_{-1}(-kappa t exp(-c)/(4q))].           (17)

It follows by setting u=log(1/a)+c in kappa t=4q a u. W_{-1} is the real
branch with u tending to +infinity. Equation (17) includes the finite
constant and log-log correction missed by t/log(1/t).

This is an exact inversion of the NORMAL FORM, not an exact solution of
the finite nonlinear native problem. The scalar analytic small-cluster
expansion gives a_* / a_L=1+o(1/L) under the same fixed-chart assumptions:
its derivative error at a~t/L is o(a), and preparation curvature is of
order L. No numerical value for the original 255-leaf B(g) is asserted;
(16) supplies the explicit required calculation. The checker evaluates
(16)--(17) only on its declared four-dimensional two-leaf fixture.

## 9. Relation to the other already owned prices

For the owned port-counting/central-gain trial,

    Price_count=A-log_phi 2-log_phi 64 E T,

E T is an analytic finite-instrument expectation. Its bounded derivatives
do not change nu or local preparation uniqueness. Its real mixed source
must be added to M in (6). No second copy of port Cost is added. More
generally a genuinely derived C2 ledger with the same parity and vanishing
vacuum preparation force changes the actual M and bounded regular terms.
A different information cut or a nonanalytic additional price needs its
own analysis and can change the conclusion.

The separate recombined Book complement has a real O(a^2) determinant
penalty under its own clock/cut hypothesis. If a same-execution physical
price actually contains it additively, it affects B and later orders,
not the positive logarithmic coefficient. We do not assert that two
functionals with different amplitude/gain contracts may simply be added.

The newer N=1 spatial-weight theorem concerns Cost MINUS a complete CQ
entropy on a different two-query execution, with generated states handled
by its causal adjoint. Its generated states are not free preparation
variables. Neither its full42 equality nor its negative entropy sign is
silently imported here. Conversely, this theorem does not repair its
remaining compulsory-query/Book-valuation hypotheses.

For a refining family with S sites and the same flat row leverage 1/S,
the purely finite normalization becomes nu_S=p^5/S. If s_w=j_w/S,
then sum_w s_w^2/nu_S=(1/p^5)sum_w j_w^2/S exactly. This shows how the
induced source-square is normalized; it is NOT a refinement theorem.
Uniform support gaps, derivative budgets, field norms, control costs and
an actual common selected action would still have to be proved.

## 10. Validation and remaining conclusion

The accompanying checker has 78 explicit checks, including exact Golden
and convexity identities, the missing mixed-term hostile control, a
full-record noncommuting parity-preserving test channel, and value,
geometric-source and material-source asymptotics. Its matrix fixture has
DATA dimension4, one reference column and two leaves. It does not rerun or
stand in for the original DATA4096/RIGHT128/255-leaf certificate.

At t=10^-3 the leading-log angle alone differs by about50%; the
constant-corrected normal form differs by about7.9e-7 in the test fixture.
This illustrates slow logarithmic convergence, not a finite-t error
bound for D0. The 180-digit trial was insufficient for the deliberately
strict final Lambert-error check at t=10^-48. Raising arithmetic precision
to300 digits, without loosening that check, resolves the cancellation.
Normal/-O replay and artifact hashes are recorded separately.

Closed mathematical application: the original specified coherent component
has a unique restricted internal preparation, a C1 reduced price and the
explicit complete geometric/material source above. Its vacuum linearized
operator is preserved. Physical admission of this independent preparation
family, its actual full Book price, exact joint nonvacuum roots and uniform
continuum transfer are not proved by this result. No final GR closure is
claimed.
