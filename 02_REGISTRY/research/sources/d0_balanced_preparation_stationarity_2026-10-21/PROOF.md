# Exact joint stationary equivalence of the native coherent preparation

21 October 2026. Continuation of existing Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Inspected source checkpoint: `dfc0275eea67ebc21ffe539de9b6ea96713863a5`.

**Status:** analytical research with an authored bounded checker; no independent
review, whole-native replay, Book/CORE/assembly acceptance or physical GR
closure is asserted. This is the original full128/cap2 coherent conditional
price, not the different N=1 two-query Cost-minus-entropy execution.

## 1. The stronger question now answered

The preceding logarithmic-source reduction found a nonzero off-shell source
correction after minimizing preparation at FIXED first-arm matter. That does
not imply a changed set of fully stationary fields. The actual preparation
orbit is already inside the same original material dictionary.

On the declared full, independently varied material chart, this fact gives
an exact all-order result:

    Crit_(g,m,a) A = { (g,m,0) : D_(g,m) A0 = 0 },                 (1)

locally near the vacuum preparation, where A0(g,m)=A(g,m,0).
All geometric and material equations on the right remain the genuine
one-arm equations. Neither their existence nor their equality to the
configured J2/Einstein equations is assumed or proved by (1).

The new proof does not invert a field Hessian, discard gauge directions,
assume a finite entropy Hessian at rank birth, or identify unlike prices.
It proves that the relative coherent preparation supplies no extra nearby
stationary branch when the corresponding original matter entries are free.

A material boundary or task constraint which freezes those entries removes
this premise: the earlier fixed-matter shifted minimum can then remain the
appropriate result. This distinction is essential, not a change of the
physical admissible set.

## 2. Native carrier and a literal material-orbit identity

Retain the original 256 sites, all CAR16 grades, oldRIGHT dimension r=128,
actual nonuniform density in D(g), strict Julia domain, and all255 cap2 leaves,
including abort and the128 identically dark Walsh leaves. In particular

    L_gamma in {K_eta, K_eta B, B^2 : eta != 0},
    B=I-epsilon D(g)^2/2,    sum_gamma L_gamma^*L_gamma=I.          (2)

The active old RIGHT Grams are positive on the inherited small fixed-mesh
chart. This is an imported support premise from the cap2 certificate, not
newly inferred from a numerical cutoff. The strict chart makes the amplitudes
analytic. Every L_gamma has definite CAR parity.

Put p=phi^-1, p+p^2=1. At site z write the two REAL original material entries
as c_z,b_z, and set

    R_z=sqrt(p^2-c_z^2),
    b_z=R_z sin(theta_z),    d_z=R_z cos(theta_z)>0,
    C(c,theta)_(z,:),alpha =
       [sqrt(p)|1> + c_z|0> + b_z|15> + d_z|14>] f(z)^T/sqrt(r).
                                                                    (3)

This is just the existing positive-slack preparation. The Fourier rows obey
||f(z)||^2=1/2 and give C^*C=I_r/r. The original fixed metric/material
calibration is unchanged. The angular chart is a local diffeomorphism because
d_z>0; its use does not add a controllable primitive.

Choose a set W of sites where BOTH the preparation coordinates and the
corresponding top-material entries are independently allowed by the original
field chart. Its size can be at most64 on the previously selected u=1/4 slice.
Only free sites are included; a fixed material collar may not be moved.
Keep the full native rank-eight generator at each selected site:

    J_w=sum_(j=6,10,12,14)(|w,j+1><w,j|-|w,j><w,j+1|),
    U(a)=product_w exp(a_w J_w).

Disjoint sites commute. The other high-grade planes have zero amplitude in
(3), but remain in the full operator. Direct substitution gives the EXACT
identity, not just a first jet:

    U(a) C(c,theta) = C(c,theta+E_W a).                            (4)

E_W inserts the selected angles into the complete site field. The reference
columns, clock-grade amplitude and scalar c are unchanged. The small angular
chart of the native finite-word closure is used analytically; exact arbitrary
angles are not claimed to be new finite native instructions.

## 3. One actual coherent record and its balanced coordinates

Define rho0=C(c,theta)C(c,theta)^* and rho1=U(a)rho0 U(a)^*. The original
coherent cut has V_gamma=[sqrt(p)L_gamma C, p L_gamma U(a)C] and the FULL
transpose of V_gamma^*V_gamma on selector/RIGHT. Its spectrum is the spectrum
of L_gamma rho L_gamma^*, where

    rho=p rho0+p^2 rho1,
    A(g,c,theta,a)=S_phi(direct_sum_gamma L_gamma rho L_gamma^*)
                     -log_phi r.                                (5)

This equality computes the complete P--leaf--RIGHT conditional entropy; it
does not classicalize P, reset RIGHT, replace the pointer basis, or suppress
failure histories. In particular the two-arm state is not a single pure
preparation away from a=0.

Define the weighted angular coordinate

    theta_bar=theta+p^2 E_W a,
    theta0=theta_bar-p^2 E_W a,
    theta1=theta_bar+p E_W a.                                   (6)

Since p+p^2=1, this is an invertible coordinate change on the SAME joint
field/preparation space. It is not a newly chosen physical mean, task, price
or reset. At a=0 it is the identity on the original material readout.
Let y=(g,c,theta_bar) and write the original functional in these coordinates
as B(y,a).

The balanced input density is exactly

    rho_bal=p U(-p^2 a) rho_bar U(-p^2 a)^*
                 +p^2 U(p a) rho_bar U(p a)^*.

At coincidence its derivative vanishes for EVERY y:

    D_a rho_bal(y,0)[v]
       =[-p*p^2+p^2*p][J(v),rho_bar]=0.                         (7)

The full coherent selector/RIGHT density need not have zero derivative;
its off-diagonal support/kernel blocks can move. We use (7) only for the
spectrum in (5), not to claim equality of all quantum states or references.

Amplitude entropy is C1 through rank birth. The old supported eigenvalues
have zero first jet by (7); newborn eigenvalues have O(||a||^2) mass. Thus

    D_a B(y,0)=0,       B(y,0)=A0(y),       D_y B(y,0)=D A0(y).    (8)

No derivative of log at a zero eigenvalue is used.

Equivalently, in the ORIGINAL coordinates the exact source identity is

    partial_(a_w) A(g,c,theta,0)=p^2 partial_(theta_w) A0,
       =p^2 d_w partial_(b_w) A0.                              (9)

This is the key missing composition with the full material equations.
A nonzero preparation force on a fixed profile is not an independent force
at a simultaneous one-arm material root.

## 4. Positive relative mass survives the coordinate change

For an active leaf put X=L_gamma C(c,theta_bar), G=X^*X and
P_X=X G^-1 X^*. Only the inherited positive OLD support is inverted.
The coefficient of newborn spectral mass in a direction v is

    Q_y(v)=p^3 sum_gamma ||(I-P_X)L_gamma J(v)C||_HS^2.           (10)

For example, in the fixed selector basis e=(sqrt(p),p), the balanced amplitude
jet obeys (D_a V)e=0 and its orthogonal selector component is
sqrt(p^3)L_gamma J(v)C. Removing the old DATA range gives (10).
It is the same relative mass as in the predecessor, now at fixed balanced
matter; a common first-order rotation has disappeared.

At c=theta_bar=0, C is odd and J(v)C is even. Definite parity of each native
leaf gives X^*L_gamma J(v)C=0. Using completeness of ALL leaves and the actual
Fourier-row normalization,

    Q_(g,0,0)(v)=p^3 ||J(v)C0||_HS^2
                  =nu ||v||^2,       nu=p^5/256.                (11)

This is exact for every g in the strict parity-preserving chart. By continuity,
a smaller compact parameter chart has Q_y >= (nu/2)I. No uniformly positive
new eigenvalue, no mesh-uniform old gap and no independence of the RIGHT
rows at different sites is assumed.

## 5. A logarithmic radial proof of exact relative stationarity

For each leaf, separate its old positive spectral cluster from the zero
cluster by an analytic contour projector in V_gamma^*V_gamma. If E_new is
the latter projector, Z_gamma=V_gamma E_new is an analytic amplitude and
Z_gamma(y,0)=0. The old-cluster entropy is analytic. Equation (8) makes its
first a-derivative zero.

For a=r v, ||v||=1, write Z_gamma=r Zhat_gamma(y,v,r). The hatted amplitudes
and their first derivatives are bounded on the finite compact chart. The
function E(Z)=-Tr Z^*Z log(Z^*Z) and its amplitude gradient are bounded on
bounded sets, continuously through zero singular values. One elementary
way to see the last assertion is s log(s^2)->0. The inherited regularized
source bound supplies the same rank-birth-safe conclusion.

The identity

    E(r Zhat)=r^2[||Zhat||_HS^2 log(1/r^2)+E(Zhat)]

therefore yields, uniformly,

    B(y,a)-A0(y)=Q_y(a) log(1/||a||^2)/ln(phi)+R(y,a),
    |R(y,a)| <= C ||a||^2,
    |a dot D_a R(y,a)| <= C ||a||^2.                           (12)

To justify the derivative estimate rather than differentiate a value-only
big-O: ||Zhat||^2=Q_y(v)+O(r) with bounded radial derivative. Its error gives
O(r^3 log(1/r)) in the value AND radial derivative. The remaining r^2 E(Zhat)
has radial derivative O(r^2) since the amplitude entropy and its gradient
are bounded. The old analytic cluster contributes O(r^2) as well.

Consequently

    a dot D_a B
      =2Q_y(a)[log(1/||a||^2)-1]/ln(phi)+O(||a||^2).             (13)

From Q_y >= nu I/2 there is a radius R0>0 such that, for every y in the
chosen chart and 0<||a||<R0,

    B(y,a)>A0(y),            a dot D_a B(y,a)>0.                (14)

Thus a=0 is the UNIQUE minimum on this balanced ball and the ONLY relative
stationary point there. This proof uses no finite entropy Hessian and no
invertibility of the baseline field equations. Strong convexity from the
preceding source-reduction proof is compatible but is not needed for (14).

## 6. Exact complete critical set and the fixed-first-arm envelope

An invertible coordinate change preserves the condition that the ENTIRE
covector vanishes. If (g,m,a) is jointly stationary for (5), it is stationary
in (6), so (14) forces a=0. At a=0, (8) says that the remaining equations are
exactly D A0=0. Conversely a root of D A0 with a=0 satisfies all equations.
This proves (1), preserving the original readout, geometry and material data
on the solutions themselves.

The result includes every independent geometric direction retained in g,
both material types, and all selected preparation coordinates. It neither
restricts the solution search to Sigma nor turns the Einstein equation into
an admission constraint. Degenerate field Hessians and gauge families do not
obstruct this equivalence.

The previously defined fixed-FIRST-arm envelope

    F(g,m)=min_a A(g,m,a)                                     (15)

is a different off-shell scalar from the balanced minimum A0. It keeps its
nonzero logarithmic correction and the previously computed full source.
On the common smaller chart its interior unique minimizing preparation and
C1 envelope identity are supplied by the predecessor (or the amplitude
convexity argument there). Nevertheless (1) implies the exact identity

    Crit F = Crit A0;  at every such point a_*=0 and F=A0.      (16)

Indeed DF=0 together with D_a A=0 is a full joint root. Conversely a root
of A0 has D_a A=0 by (9), and uniqueness of the fixed-first-arm minimum
identifies its optimizer with zero. No claim DF=c D A0 on a neighborhood,
no equality of the off-shell prices and no redefinition of physical fields
away from their stationary solutions is made.

## 7. Every nearby stationary Hessian is also preserved

The predecessor established this only at matter-free centers. Let y0 be
ANY critical point of A0 in the chart of (16), including nonzero matter.
In original coordinates s(y)=D_a A(y,0) is analytic and s(y0)=0 by (9).
The old/new-cluster expansion is

    A(y,a)-A0(y)=s(y) dot a+Q_y(a)log(1/||a||^2)/ln(phi)+R(y,a).

In addition to |R|<=C||a||^2 it has ||D_yR||<=C||a||^2 and
||D_aR||<=C||a||; these follow from the same amplitude factorization,
including bounded angular amplitude derivatives. Uniform positivity of Q
and minimizer comparison give

    ||a_*(y)|| log(1/||a_*(y)||) <= C ||s(y)||,
    ||a_*(y)||=O(||y-y0||/log(1/||y-y0||)).                    (17)

For example, comparison with a=0 first bounds
c r^2 log(1/r)-C r^2 <= ||s||r, which proves (17) after shrinking the chart.
The parameter-differentiated source, not differentiation of an unbounded
value remainder, now gives

    DF(y)-D A0(y)=O(||y-y0||/log(1/||y-y0||))=o(||y-y0||).

Hence the gradient is Frechet differentiable at y0 and

    D^2 F(y0)=D^2 A0(y0).                                    (18)

The full finite linearized field operator, its kernel, and its positive
and negative inertia are unchanged AT EVERY nearby baseline root. This is
not a global C2 assertion and not uniform refinement. In particular, the
relative preparation does not cure a genuine full-field saddle by turning
it into a minimum.

## 8. The old mixed matrix is a selected material Hessian, not a new coupling

Let H_m(g)=D_m^2 A0(g,0) in the ORIGINAL real (c,b) coordinates, and let P_b
select the top-field rows at W. Differentiating the exact identity (9),
using d_w=p and D_m d_w=0 at m=0, gives

    M(g)=p^3 P_b H_m(g).                                     (19)

This is exactly the mixed matrix previously computed from all four terms
in the full native Gram jet. It explains both the required J_w D_m C terms
and their cancellation for a scalar instrument. Omitting them violates (9).

Therefore a material zero mode H_m v=0 satisfies Mv=0. The leading reduced
term -K||M m||^2/log(1/||m||), K=ln(phi)/(8nu), is a squared selected
one-arm field-gradient contribution, not an independently selectable mass
term. It does not by itself generate a new small-amplitude matter branch.
Equations (1) and (16), stronger than this leading statement, settle the
stationary set exactly in the stated neighborhood.

### 8.1 A concrete inherited primary material equation

At the previously certified address w0=(1,1,2,2), the primary profile has
c_w0=b_w0=0 and d_w0=p exactly. Its published coherent preparation source
is -kappa t+O(t^3), with

    -kappa in [-0.000000484198646894237340726684,
               -0.000000484198646476459455171882].

Equation (9) therefore identifies an ACTUAL one-arm top-material Euler row:

    partial_(b_w0) A0 = -(kappa/p^3)t+O(t^3),
    -kappa/p^3 approximately -2.0511e-6.                       (19a)

The checker encloses the division by exact rational Golden brackets. It does
not rerun or strengthen the inherited finite spectral source certificate.
Thus that particular configured J2 representative is not a root of this
one-arm conditional price, and allowing only the relative coherent control
cannot turn the SAME matter representative into a full joint root. This is
consistent with the exact equivalence: it preserves true one-arm roots, not
roots of a different functional. It pinpoints the missing material/source
transport rather than claiming that logarithmic stabilization alone closes GR.

## 9. Actual extra prices: one exact balanced-source test

Let a genuinely derived additional ledger W(g,c,theta,a) be C2 with bounded
preparation curvature. Put S=A+W, S0=A0+W(y,0). The precise relative source
on the diagonal is

    e_w(y)=[partial_(a_w) W-p^2 partial_(theta_w) W]_(a=0)
          =[partial_(a_w) W-p^2 d_w partial_(b_w) W]_(a=0).      (20)

If e(y)=0 IDENTICALLY on the neighborhood, its balanced expansion has no
linear term; its radial value/source is O(||a||^2). The logarithmic term
still dominates. Thus the exact critical-set equivalence and stationary
Hessian preservation extend from A,A0 to S,S0.

If e is only zero at one point, that suffices to check that particular
diagonal stationary point, not to exclude other off-diagonal roots nearby.
If e!=0, it is a real independent upstream source. Neither this proof nor
a matched instruction inventory allows it to be deleted or tuned away.

There is a positive SAME-EXECUTION application. For the already owned
stopped actual-port/central-gain trial with fixed positive complete label
reference mu_gamma and actual port prices c_gamma,

    P=E c_port-D_phi(Omega||Tau_mu)
       =A-log_phi2+sum_gamma q_gamma(c_gamma+log_phi mu_gamma).

The last sum is Tr(rho T), T=sum_gamma(c_gamma+log_phi mu_gamma)E_gamma.
It is genuinely affine in the same input mixture, so (7) makes e=0 exactly.
The capacity offset remains and no port charge is counted twice. Therefore
THIS specified coherent price and ITS one-arm baseline have exactly the
same nearby joint critical set and field Hessians. The complete central
reference, spectral-readout admission and physical Book binding are still
premises; this does not repair that trial's previously proved mismatch
with literal absolute amplitude weights.

More generally an actually priced term
p W0(theta0)+p^2 W0(theta1), or a smooth functional of the same rho, is
balanced-neutral. A direct first-arm charge W=f(theta) is NOT neutral:
e=-p^2 D_theta f, even though W has no explicit a-dependence. A noncentral
selector/RIGHT reference may see the nonzero off-diagonal quantum state
jet noted after (7). It cannot be inferred neutral from the DATA mixture.

The true recombined Book-feedback component from its own clock/cut owner
has zero first relative derivative at coincidence and a preparation-independent
diagonal value, so it passes this component-level test when its stated
interface applies. It is NOT automatically a term of the scalar-gain price
above. The actual moving clock/work/reference and source transport must
still establish one common full functional before any sum is used.

## 10. What this changes in the GR route

The preparatory logarithmic correction is no longer an unspecified threat
to every nonlinear root: on this same complete material chart it preserves
ALL nearby one-arm joint roots exactly, and their full linearized operator.
One does not need a nondegenerate Einstein Hessian to make that conclusion.

This is a genuine equation-level equivalence, the kind of transport allowed
by the earlier global synthesis even when scalar source proportionality on
an open chart is false. The old off-shell correction is retained; a different
price may have the same critical set. The configuration must still solve
its one-arm price, not merely the configured J2 equations of another model.

The newer N=1 spatial/full42-source theorem is a different execution, price
sign and cut, with generated states constrained by the paid program. Those
states are not freely minimized here. Identifying its physical Book law with
the present one-arm law remains an actual missing application. None of the
present identities establishes that transport by matching dimensions or
names. Likewise, the new quaternion-clock return calculation concerns another
arm/spin/record instrument and does not supply the missing CAR clock map.

If a task fixes the first-arm material profile, or lacks these independent
material variations, (6) is not an allowed variation of that task. Its
fixed-profile shifted minimum and abort constraint remain valid. A moving
query depending separately on theta0 rather than on g and the prepared
state has its own extra derivative; (9) cannot simply be imported there.

Unresolved: compulsory physical Cost/Info and addressing, actual finite-word
attainment versus continuous closure, task/boundary variation image, one
same-source geometric application, and mesh-uniform estimates. The exact
stationary equivalence is local at a fixed mesh and does not itself construct
a new nonvacuum root. GR_closed=false.

## 11. Verification and provenance

The checker tests orbit identities with the full rank-eight CAR generator,
actual Fourier-row normalization, balanced density jets, noncommuting complete
instrument Gram spectra, the full mixed-Hessian identity, logarithmic radial
positivity, a finite stationary baseline and exact failure cases for missing
abort, frozen first-arm work and separately moving queries. Its small
instruments are controls for this proof, NOT a replay of the original4096-D
native Dirac or255-leaf support calculation.

The predecessor PROOF has Git blob c00e533a56050bab649d987d85b8695c33ce4f5e,
SHA256 4b2ab4a0d80aa75dca4cd952b25e03827630cf6796e36cf6fb521aabe2eccb94.
Original coherent record: e5841990c5becf562928115012a4dcafd25f6a87;
strict native/material dictionary: ed00d6609c6f9f88391c7ff076abc65a3524dbd1;
cap2 support owner: 6afab2c3d5c8361639f2c58bddeffdfce91b3098;
actual-port nonlinear price: 829c2fafcf390f6d2d6246b46fb22cc8655756f2.
All refer to published earlier sources on the inspected branch. Detailed
refs are in SOURCES.json. No claimed independent review is manufactured.
