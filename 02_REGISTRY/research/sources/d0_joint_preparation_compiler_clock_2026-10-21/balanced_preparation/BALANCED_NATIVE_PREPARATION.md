# Balanced native preparation: exact joint critical points and zero Hessian correction

21 October 2026. Bounded continuation of existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input snapshot: `dfc0275eea67ebc21ffe539de9b6ea96713863a5`.

## 0. Exact conclusion and consuming step

The previously derived logarithmic preparation minimum was taken while
holding the original material preparation fixed. The original material
coordinates and the selected preparation rotations are, however, coupled
coordinates of the **same two prepared arms**. Rewriting them as a weighted
mean angle and a relative angle supplies an exact new identity.

For the specified original full128 cap2 coherent conditional-entropy
functional, on its already declared small native chart:

* the relative preparation has its unique local minimum at coincidence
  for **every** nearby mean material field, not only at vacuum;
* all full joint stationary points have coincident arms and are exactly
  the stationary points of the coincident-arm functional;
* the old fixed-anchor reduced functional has exactly the same full
  critical set, despite its nonzero off-shell logarithmic correction;
* its full field Hessian at every such stationary point equals the
  coincident-arm Hessian. No finite preparation Hessian is assumed.

Thus this particular preparation extension contributes no additional
independent equation at a genuine full material/field root of the same
functional. The old nonzero preparation source on a prescribed waveform
is a selected material Euler source in another coordinate, rather than
an independently adjustable force. It remains a real source off shell.

The consuming step is the full joint-source application of
`sources/d0_native_logarithmic_source_reduction_2026-10-21/PROOF.md`.
The result does **not** prove that its coincident-arm functional is the
configured Golden-J2 action, that the primary GR family is stationary for
it, or that a separate N=1 CQ or Book03 price has the same information cut.

## 1. Original carrier, chart and retained assumptions

Keep the literal original 256-site CAR16 instrument and all128 RIGHT
columns, the actual unequal cost20 density, positive adjoints, fixed
clock/normalization and all255 cap2 histories. In the notation of the
existing logarithmic owner,

    r=128, p=phi^(-1), p+p^2=1,
    sum_gamma L_gamma(g)* L_gamma(g)=I,

where g contains the genuine independent coframe/link and any already
included geometric coordinates. The instrument depends analytically on
g in the original strict Julia chart. Its128 structurally dark leaves
remain zero. Every active old RIGHT Gram at the vacuum centre is positive
definite. This inherited finite-mesh support result supplies a common
positive old-support gap after shrinking the parameter chart.

The normalized preparation is exactly

    C_(c,b)(z,:) = [sqrt(p)|1> + c_z|0> + b_z|15>
                       + d_z|14>] f(z)^T/sqrt(r),
    d_z=sqrt(p^2-c_z^2-b_z^2)>0,
    C* C=I_r/r, ||f(z)||^2=1/2.

No grade, site, output or RIGHT column is removed. In particular the
coherent selector remains quantum and the complete leaf remains the
same classical register as in the original specified cut.

Choose the same k distinct actuated sites as in that owner, with k<=64
and original complete rank-eight generators

    J_w=sum_(j=6,10,12,14)(|w,j+1><w,j|-|w,j><w,j+1|).

They commute because their site supports are disjoint. Their other
high-CAR planes remain in the full operator; those planes have zero
input amplitude on this preparation dictionary. Their action on the
actual populated dictionary is therefore exactly rotation of14/15,
while |0> and |1> remain fixed.

The theorem requires the b_w material coordinate at each selected site
to be among the actual independent free coordinates of the mathematical
joint variational problem. The selected sites must be free interior
sites, or the boundary constraints must admit the equivalent coordinate
change. It does not convert a fixed boundary value or a fixed waveform
parameter into a free material variation. All other original collar
values remain fixed. The original site w=(1,1,2,2) is the existing local
interior test; the theorem never asserts global periodicity of the
unwrapped primary geometric family.

As before, continuous closure of these finite native controls is a
mathematical parameter chart, not an automatically admitted free physical
preparation or a uniform finite-word synthesis. Actual upstream preparation,
addressing and control costs retain their own contracts.

## 2. Exact angle coordinates on both complete arms

For every site set

    R_z=sqrt(p^2-c_z^2),
    b_z=R_z sin(theta_z), d_z=R_z cos(theta_z).

The positive-slack chart gives cos(theta_z)>0, so this is an analytic
local coordinate change in the original real material variables. At a
selected site the ACTUAL full generator obeys

    exp(a_w J_w) C(c,theta)=C(c,theta+a_w e_w).

This is an equality of the complete 4096-by128 preparation matrices,
not merely of one probability or of a normalized marginal. It preserves
the full fixed RIGHT Gram. For a vector a of selected-site angles, write
theta+a for this selected-coordinate shift.

The original coherent density and functional are

    rho(g,c,theta,a)
       =p C(c,theta) C(c,theta)*
          +p^2 C(c,theta+a) C(c,theta+a)*,

    A(g,c,theta,a)
       =S_phi(direct_sum_gamma L_gamma(g) rho L_gamma(g)*)
          -log_phi r.

At a=0 set A0(g,c,theta)=A(g,c,theta,0).

Introduce mean and relative coordinates ONLY at the selected sites:

    mu=theta+p^2 a,       delta=a,
    theta_-=mu-p^2 delta, theta_+=mu+p delta.                 (1)

Unselected angles are unchanged. This is an invertible coordinate
change, since theta=mu-p^2 delta and p+p^2=1. Let

    Phi(c,theta)=C(c,theta) C(c,theta)*,
    rhobar(g,c,mu,delta)
       =p Phi(c,mu-p^2 delta)+p^2 Phi(c,mu+p delta).

Then the fundamental exact identity is

    D_delta rhobar(g,c,mu,0)[v]
       =[-p p^2+p^2 p] D_theta Phi(c,mu)[v]=0.              (2)

It holds for every nearby g,c,mu and every selected-site vector v. It
does not use vacuum, parity, a field equation or a special waveform.
Both prepared arms move, and both of their genuine derivatives appear.

The complete entropy has a C1 amplitude extension at the new zero
eigenvalues. Consequently

    D_delta Abar(g,c,mu,0)=0,
    Abar(g,c,mu,0)=A0(g,c,mu).                              (3)

Equation (3) is not obtained by freezing a record-dependent logarithm.
The following spectral-cluster argument gives its regularity and the
strict relative minimum on the complete original cut.

## 3. Moving-both-arms spectral clusters and positive relative curvature

For an active leaf put

    X_-=L_gamma C(c,mu-p^2 delta),
    X_+=L_gamma C(c,mu+p delta).

Its rectangular amplitude is `[sqrt(p) X_-, p X_+]`. Right multiplication
by the constant orthogonal selector rotation with columns
`(sqrt(p),p)` and `(-p,sqrt(p))` gives the equivalent amplitude

    V_gamma=[ Xbar_gamma, sqrt(p^3)(X_+-X_-) ],
    Xbar_gamma=p X_-+p^2 X_+.                              (4)

At delta=0 this is `[X_gamma,0]`. The old r positive eigenvalues of its
Gram are separated from the r zero eigenvalues. The cluster projectors
are analytic by a resolvent contour around the old positive cluster;
individual newborn eigenvectors are not differentiated.

Write E_new for the analytic new-cluster projector and
Z_gamma=V_gamma E_new. Then Z_gamma(g,c,mu,0)=0. Equation (2) is already
visible at amplitude level:

    D_delta Xbar_gamma|0=0,
    D_delta[sqrt(p^3)(X_+-X_-)]|0[v]
       =sqrt(p^3) L_gamma sum_w v_w J_w C(c,mu).

For

    P_gamma=X_gamma(X_gamma* X_gamma)^(-1)X_gamma*,

the old faithful-block Schur calculation therefore gives exactly

    Q_(g,c,mu)(v)
       :=sum_gamma ||D_delta Z_gamma|0[v]||_HS^2
       =p^3 sum_gamma ||(I-P_gamma)L_gamma
                            sum_w v_w J_w C(c,mu)||_HS^2.   (5)

Only the old faithful Grams are inverted. At the original vacuum,
C0 has odd CAR parity, whereas every J_w C0 has even parity. Every
literal native Kraus leaf has definite parity, so each projected term
P_gamma L_gamma J_w C0 vanishes. Completeness and the original normalized
Fourier-row leverage give

    Q_(g,0,0)(v)=nu ||v||^2,
    nu=p^5/256>0,                                         (6)

for every g in the stated parity-preserving geometric chart. By
continuity, Q>=nu I/2 on a sufficiently small common material chart.
This is the same exact native small-mass coefficient as the previous
owner, now derived for both moving arms rather than assuming its reuse.

For clarity, the inherited amplitude-convexity proof applies to (4)
without change of sign or loss of a branch. The regularized new entropy
uses the singular-value function

    f_eta(s)=-s^2 ln(s^2+eta),
    f_eta''(s)>=-2 ln(epsilon^2+eta)-6

when |s|<=epsilon. The same lower bound applies to the radial divided
difference f_eta'(s)/s. Thus its matrix spectral sum is strongly convex
on a small amplitude ball. On ||delta||<=R, analyticity and (5)–(6)
give, after shrinking the common chart,

    ||D_delta Z[v]||_HS^2>=nu ||v||^2/4,
    ||Z||<=C R,

with all second derivatives of Z bounded. The nonlinear-composition
curvature error is bounded below by
`-C R(1+|ln R|)||v||^2`, uniformly as eta decreases to zero. The old
cluster contributes a bounded smooth Hessian. Combining these terms
leaves a lower relative curvature of the form

    c1 ln(1/R)-c2-c3 R|ln R|>0.

Integrate the regularized Hessian inequality on line segments and let
eta decrease to zero. This proves strong convexity of the actual C1
function delta↦Abar on the closed small relative ball, including all
newborn rank changes. No finite Hessian at delta=0 is assigned.

Together with the EXACT zero source (3), this proves

    delta=0 is the UNIQUE relative stationary point and minimum
    for every fixed nearby (g,c,mu).                       (7)

One may use nested parameter neighborhoods and a common small angle
ball so that (1), the positive slack and all support gaps stay within
their original charts. All constants here are fixed-mesh constants.

## 4. Exact full joint stationary set

Let y=(g,c,b) denote the original independent field coordinates, with
their actual fixed collar and the selected b_w among the free rows.
All unselected material coordinates are retained. The change to
(g,c,mu,delta) is an invertible change of these SAME coordinates and a.
Therefore vanishing of the full covector is invariant under it.

If D_(y,a) A=0 at a point of the small joint chart, its relative source
also vanishes. By (7), delta=a=0. At coincidence, (3) implies that the
remaining full covector is precisely D_y A0. Conversely every zero of
D_y A0 lifts to a joint zero of A at a=0. Thus

    Crit(A) = { (y,0) : D_y A0(y)=0 }                       (8)

locally, with EVERY genuine geometric and both material types of rows
included. There is no restriction of the action to a null ansatz before
variation and no deletion of an off-ansatz matter source.

The equality (8) does not assert that Crit(A0) is nonempty, nor that a
known root of another action belongs to it. Its positive content is
the removal of the selected independent relative-preparation equations
from this same full stationary system.

## 5. Exact relation to the original fixed-anchor reduction

The original owner defines

    F(y)=min_(||a||<=R) A(y,a),

holding the original anchor material y fixed. Its strong convexity and
interiority give a unique local a_*(y), and the C1 envelope identity

    D_y F(y)=D_y A(y,a_*(y)),  D_a A(y,a_*(y))=0.            (9)

Shrink the anchor chart so that every such minimizer lies in the joint
chart used in (8). Then a critical point of F is a full joint critical
point of A. Equation (8) forces a_*=0 and D A0=0. Conversely if D A0=0,
then A(y,0) is joint stationary; uniqueness of the anchor minimum forces
a_*(y)=0, and (9) gives DF=0. Hence, in the ORIGINAL y coordinates,

    Crit(F)=Crit(A0),
    a_*(y)=0 and F(y)=A0(y) at every such root.              (10)

This is exact equality of stationary sets. The generally nonzero
off-shell correction F-A0 is preserved. Eliminating relative preparation
at fixed mean and eliminating it at fixed anchor are different maps,
so their off-shell values need not agree.

There is a more precise exact source identity before any expansion.
At a=0 only the second arm moves under the original fixed-anchor
preparation derivative. The full entropy derivative is p^2 times the
coincident-arm angle derivative. Since db_w/dtheta_w=d_w,

    (D_a A(y,0))_w
       =p^2 partial_(theta_w) A0(y)
       =p^2 d_w partial_(b_w) A0(y),
    d_w=sqrt(p^2-c_w^2-b_w^2)>0.                           (11)

The factor is the actual slack d_w, not R_w away from b_w=0.
In particular

    a_*(y)=0  iff  partial_(b_w)A0(y)=0 for every selected w. (12)

Indeed (11) gives anchor stationarity at zero, and the inherited anchor
strong convexity gives its uniqueness. This criterion requires neither
geometric stationarity nor vanishing of unselected matter rows.

## 6. The former logarithmic term is a squared selected material source

At vacuum the whole first material derivative of A0 vanishes by parity.
The fixed-anchor source s(g,m)=D_a A(g,m,0) was written in the previous
owner as M(g)m+O(||m||^3), where m contains BOTH scalar/top amplitudes at
all sites. Differentiating the exact identity (11), with d_w=p at vacuum,
identifies its full matrix:

    M_(w,i)(g)=p^3 partial_(b_w) partial_(m_i) A0(g,0).      (13)

Thus the missing `J_w T` terms in the old explicit leaf formula are
required by an exact material-Hessian identity. They are not an
independent additional force to be cancelled by geometry or clock work.

The existing asymptotic

    F-A0= -[ln(phi)/(8nu)] ||M(g)m||^2 / ln(1/||m||)
              +o(||m||^2/ln(1/||m||))                     (14)

is therefore a negative square of SELECTED linearized material Euler
components, with its already-derived logarithmic denominator. It is
not an arbitrary square of the full Einstein equation or a counterterm
chosen to obtain GR. Equations (8)–(12), rather than differentiation of
the little-o term in (14), prove exact protection of the joint roots.

A prescribed primary waveform with the old strictly nonzero s_w remains
off shell for this same material source. The argument does not change
that measured sign or convert the configured J2 root into an A0 root.

## 7. Full Hessian preservation at every nearby source-zero point

Let y_* be any point in the common chart with s(y_*)=0, including every
full stationary point of A0. The same separated-cluster expansion,
now centered at y_* rather than only at vacuum, gives

    A(y,a)-A0(y)
      =s(y).a + Q_y(a) ln(1/||a||^2)/ln(phi)+R(y,a),

    Q_y>=q_* I>0,
    |R(y,a)|+||D_y R(y,a)||<=C||a||^2,                    (15)

locally uniformly. The old cluster is analytic; the new amplitude has
Z(y,a)=||a|| Zhat(y,a/||a||,||a||). Amplitude entropy and its first
derivative are bounded on bounded sets, including zero singular values.
These facts give the parameter-derivative remainder bound in (15)
without differentiating individual newborn eigenvalues. The coefficient
Q_y and s(y) are analytic on this finite old-support chart.

Write h=y-y_*. Since s(y_*)=0, s(y)=O(||h||). Comparing the minimizing
value with a=0 in (15) first gives

    ||a_*(y)|| ln(1/||a_*(y)||)<=C ||s(y)||,

and therefore

    ||a_*(y_*+h)||=O(||h||/ln(1/||h||)).                   (16)

The zero-source case has a_*=0 by (12). Differentiate (15) in y while
holding a fixed, and then use the envelope identity. It gives

    DF-DA0
      =(D_y s).a_*+(D_y Q)(a_*) ln(1/||a_*||^2)/ln(phi)
          +O(||a_*||^2)=o(||h||).                         (17)

Unlike the special vacuum calculation, D_y Q need not vanish: its
boundedness is enough because the term is quadratic in a_*.
The analytic A0 has a finite Hessian. Equation (17) therefore proves

    D^2 F(y_*)=D^2 A0(y_*)                                (18)

as a derivative of the complete gradient at that point. This applies
at every nearby true joint root, including nonzero matter, and even at
every point where the selected material source (11) vanishes.

It does not assert C2 regularity on an entire punctured neighborhood or
assign a finite invertible preparation Hessian. In particular (18) does
not turn a field saddle into a field minimum. It is the rigorous sense
in which the preparation correction to the field Hessian vanishes at
these source-zero points.

## 8. Actual same-density prices that inherit the theorem

The proof extends if the declared SAME execution adds a genuinely
derived C2 price W(g,c,rho), with bounded second derivatives on this
finite chart. The selected material angles enter W only through this
SAME density. The crucial fact is (2):

    D_delta W(g,c,rhobar)|delta=0=0.

The logarithmic positive curvature dominates bounded smooth relative
curvature. Thus the relative minimum and full joint critical-set
identity (7)–(8) hold with A replaced by A+W and A0 replaced by its
actual coincident-arm restriction. The fixed-anchor conclusions
(9)–(12) and (18) also hold wherever the unique interior anchor minimum
lies in the same common chart. This is available locally around any
coincident point whose COMPLETE selected material source is zero. An
arbitrary W can have a nonzero material force at the original vacuum;
its interior anchor section there must not be silently inherited from
the unextended entropy.

The C2 regularity sufficient for Hessian preservation is detailed in
section 9. The original parity-specific cubic remainder and special
vacuum expansion (13)–(14) require their corresponding parity and
regularity hypotheses for an added price; they are not asserted for
every C2 W. Whenever those expansions do apply, their source and Hessian
are those of this SAME complete functional.

Examples include actual expected fixed finite-history or port charges

    W=sum_gamma c_gamma(g) Tr[L_gamma(g) rho L_gamma(g)*]

with the true supplied moving costs retained. In particular, on the
specified cap2 counting/central-gain contract from the old owner,

    Price_count=A-log_phi 2-log_phi 64 E T,
    E T=1+Tr[B(g) rho B(g)*],

the extra term is a smooth linear functional of that SAME rho. The
original parity gives zero material force at vacuum for this actual
counting ledger, so the local interior anchor section is retained after
shrinking the chart. The theorem applies to this already declared price
and its actual coincident-arm restriction; no second copy of port Cost
is added.

This is not permission to add another execution's CQ entropy, Book
return determinant or external preparation law. An additional entropy
with its own rank birth need not have bounded relative curvature and
can change the conclusion. The sign of the original coherent entropy
has not been reversed.

## 9. Exact test for genuinely independent upstream terms

Let U(y,a) be an actually supplied additional C2 upstream ledger in the
original anchor coordinates. In balanced variables it becomes

    Ubar(g,c,mu,delta)=U(g,c,theta=mu-p^2 delta,a=delta).

At coincidence its relative source is exactly

    (D_delta Ubar)_w|0
       =partial_(a_w) U(y,0)
           -p^2 d_w partial_(b_w) U(y,0).                  (19)

For the unextended coherent entropy that source was identically zero.
Thus (19), not the mere name “preparation cost,” is the exact missing
same-initial interface test for a real upstream term.

If (19) vanishes throughout the relevant neighborhood and its relative
curvature is bounded, the same relative-convexity and full critical-set
proof extends to A+U, with its complete coincident-arm functional. Its
fixed-anchor conclusions have the same interior-section qualification
as in section 8. If (19) vanishes only at a proposed root, the zero
relative section is stationary at that root, but neighborhood-wide
critical-set equivalence has not been established. A nonzero (19) is a
real force and must be retained.

For an added C2 ledger, the literal parameter-derivative remainder
bound ||D_y R||=O(||a||^2) in (15) need not extend to that ledger without
stronger regularity. It is not needed. Taylor's formula in a gives

    U(y,a)-U(y,0)=D_a U(y,0).a+O(||a||^2),
    ||D_y U(y,a)-D_y U(y,0)||<=C||a||.

The first bound retains the logarithmic minimizer estimate (16) at a
zero of the COMPLETE selected source. For the gradient, use the second
bound directly, together with the entropy part of (15): every added
term is O(||a_*||)=o(||h||), and the entropy's parameter term remains
O(||a_*||^2 ln(1/||a_*||)). Hence (18) holds for the complete coincidence
functional with only C2 regularity of U. No stronger Taylor remainder
for D_y U is being assumed.

For example, an anchor-only material price generally has U_a=0 but
U_b!=0 and therefore does not pass (19). A separately given geometric/
matter action cannot simply be placed beside the coherent entropy and
declared covered by the balanced-arm theorem. Likewise a constraint
fixing selected anchor b_w destroys the needed invertible variational
coordinate change unless its genuine reaction is included.

## 10. Scope of the new reduction

The theorem uses the actual original CAR preparation dictionary, all
RIGHT128 columns, the complete cap2 record, the genuine scalar/top
variables and the old finite spectral support certificate. The only
new reparameterization is the exact invertible weighted mean/relative
angle map (1). It changes neither the action nor the information cut.

It removes the selected relative-preparation obstruction from the
mathematical full stationary system of that same functional. The
remaining target is the true coincident-arm field/material source,
together with whatever real upstream ledger fails or has not yet been
shown to satisfy (19).

All neighborhood radii, old-support gaps and derivative constants are
fixed-mesh. No uniform h limit, actual finite-word attainment of arbitrary
angles, compulsory Book03 valuation or physical GR closure is proved.
No claim, task lifecycle or assembly acceptance is promoted.

### Original inputs consumed

* `02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/PROOF.md`,
  particularly sections2–7 and9: native dictionary, active-support gap,
  amplitude strong convexity, source bounds and fixed-anchor envelope.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_COHERENT_CHOICE_SOURCE.md`:
  same coherent selector, retained PR/leaf cut and exact p^2 source factor.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE.md`:
  the original complete cap2 source and faithful old RIGHT blocks.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/PRIMARY_STOPPED_PORT_PRICE_AND_PREPARATION_EULER.md`:
  the actual counting/central-gain price, retained full preparation source
  and separate physical valuation boundary.
