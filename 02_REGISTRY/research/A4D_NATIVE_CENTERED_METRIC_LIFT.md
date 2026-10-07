# Native centered metric fibers, smooth variations and the literal vacuum boundary

Input: `dae0ec13f9f885ff945c45613ae38becbc097d18`.
Parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Status: constructive metric/variation part and exact stated finite-fiber
criterion, pending CONTROL. **Native action transfer, independent matter,
physical Ward, nonlinear GR, soundness/recovery for a successful native system
and global closure remain OPEN.**

This uses the actual `LocalCoframeField`, `backwardAverage`,
`centeredCoframeMatrix` and `solderMetricMatrix`. It supplies no new action,
field equation, selector, projection law or physical postulate. A constructive
section of an existing readout is a proof of its range, not a selected law
of state preparation. The four-Role field carrier is not the positive
point-state algebra classified in the preceding measure proof.

## 1. Actual map and the already known finite rank boundary

Put L=N+2, h=1/L and X_L=(Z/L)^Role. Let U_r f(x)=f(x+r),
A_r=(1+U_r^{-1})/2. The real native field is e_r^a(x), with 16L^4
coordinates. Write C(e)_ra=A_r(e_ra), eta=diag(1,-1,-1,-1), and

    Theta(e)=eta+C(e),       G(e)=Theta(e) eta Theta(e)^T.       (1)

These are the literal supported owner definitions. The frozen linear
readout is R(e)=C(e)+C(e)^T, the derivative of G at zero.
The existing [staggered-carrier result](A4D_STAGGERED_PRIMAL_DUAL_HODGE_CARRIER.md)
already gives its odd/even ranks. Those ranks are reused here, with a full
explicit range inverse, nonlinear fiber criterion and smooth preparation
bounds; they are not presented as a newly discovered dimensional obstruction.
No coframe equation or local Lorentz gauge symmetry follows from (1).

Use normalized counting Euclidean norms on raw fields and the full
Frobenius norm on symmetric matrices. In ten independent coordinates the
latter weights each off-diagonal slot by two. These choices are stated
because omitting that factor changes the sharp range-inverse constant.

## 2. Complete scalar centering solution, including the required even sizes

On a one-coordinate L-cycle, let S=U^{-1}. For odd L,

    A^{-1}=sum_{k=0}^{L-1} (-1)^k S^k.                        (2)

Multiplication by (1+S)/2 telescopes to identity, since S^L=1 and L is odd.
For even L, including every L in 4N, put

    P=(1/L) sum_{k=0}^{L-1} (-1)^k S^k,
    C=(1/L) sum_{k=0}^{L-1} (-1)^k (L-1-2k) S^k.              (3)

P is the orthogonal projector onto the alternating mode. Comparing each
cyclic coefficient gives

    P^2=P=P*,  AP=PA=0,  AC=CA=1-P,  PC=CP=0.                (4)

Thus Af=b iff Pb=0; all solutions are f=Cb+n with Pn=n.
On the four-torus the same formulas act along each r-line, leaving the
other coordinates fixed. The kernel has dimension L^3 per scalar row.
In particular, zero centering is not zero raw data.

The finite Fourier vectors exp(2 pi i k j/L) form a complete orthogonal
basis: summing the geometric progression gives their inner products, and
there are L vectors. The multiplier of A is

    a(k)=(1+exp(-2 pi i k/L))/2,
    |a(k)|=|cos(pi k/L)|.

This also proves that (3) is the least-norm range inverse. Its exact norm
is 1/sin(pi/L) for even L, including L=2; for odd L the inverse norm is
1/sin(pi/(2L)). Neither family has a uniform inverse on its whole range.
This is a statement about the readout, not the coupled Euler operator.

## 3. Full metric range, kernel and all ten packed components

At a four-frequency k write a_r=a(k_r). The independent rows are

    R_rr=2 a_r e_rr,
    R_rs=a_r e_rs+a_s e_sr,       r<s.                        (5)

A supplied symmetric m is in the range exactly when its diagonal slot
vanishes at a_r=0 and its (r,s) slot vanishes wherever a_r=a_s=0.
On that range its unique least-norm preimage is

    e_rr=m_rr/(2 a_r)                    if a_r != 0,
    e_rs=conj(a_r)m_rs/(|a_r|^2+|a_s|^2),
    e_sr=conj(a_s)m_rs/(|a_r|^2+|a_s|^2)  if the denominator is nonzero,

with zero on absent rows. The formula respects conjugate frequencies, so
real input has a real lift. Each diagonal or unordered pair uses disjoint
raw variables; this proves both minimality and completeness, not just a
rank count. All remaining preimages differ by the full kernel of (5).

If z coordinates are Nyquist, the symbol rank is 10-z(z+1)/2. Summing its
missing slots over all frequencies recovers the existing even-L result:

    rank R = 10 L^4 - 4 L^3 - 6 L^2,
    dim ker R = 6 L^4 + 4 L^3 + 6 L^2,
    dim coker R = 4 L^3 + 6 L^2.                              (6)

For odd L, rank R=10L^4 and dim ker R=6L^4. For even L the raw centering
kernel alone has dimension 16L^3; its quotient in ker R is the skew
centered-row sector of dimension 6 L^2 (L-1)^2. Indeed each skew pair must
have both of its row multipliers nonzero. These dimensions add to (6).
The kernel is retained. Calling all its elements physical gauge would
require invariance of the actual action and matter readout, not (5).

In the declared Frobenius pairing, the nonzero squared singular values are

    4 |a_r|^2;       2 (|a_r|^2+|a_s|^2).                    (7)

For even L their smallest value is 2 sin^2(pi/L): take one pair with one
Nyquist coordinate and the other one step away. For odd L it is
4 sin^2(pi/(2L)), attained on a diagonal (and on two nearest-Nyquist rows).
The sharp least-norm inverse bounds are consequently

    ||R^+|| = 1/(sqrt(2) sin(pi/L))        for even L,
    ||R^{-1}_{range}|| = 1/(2 sin(pi/(2L))) for odd L.          (8)

A loss on high-frequency grid data does not preclude uniformly controlled
lifts of fixed smooth metric probes. Section 5 constructs those lifts
without a frequency cutoff or deletion of kernel modes.

## 4. Exact nonlinear fibers and actual metric covectors

For an arbitrary invertible sitewise reference solder Theta_0 with
G_0=Theta_0 eta Theta_0^T, all invertible solders having Gram G_0 are
Theta=Theta_0 Lambda, where Lambda eta Lambda^T=eta. This follows in both
directions by multiplying with Theta_0^{-1} and its transpose.
It uses the whole Lorentz matrix group; if a component is separately part
of a declared state class, the same formula is restricted to that component.

For even L, G(e)=G_0 therefore has exactly the following fibers:

    choose Lambda(x) with Lambda eta Lambda^T=eta and
      P_r (Theta_0 Lambda)_ra=0 for every r,a;
    e_ra=C_r((Theta_0 Lambda)_ra-eta_ra)+n_ra,
      P_r n_ra=n_ra.                                        (9)

For odd L there is no P constraint and (2) replaces C_r, with n=0.
The constants eta have zero even-L alternating projection. Equations
(3)--(4) prove sufficiency, while the preceding Lorentz factorization and
the complete centering solution prove necessity. Formula (9) is a full
criterion for this nonlinear fiber; it does not claim that its Lambda
constraint is always solvable, or install a choice of Lambda in the core.
An arbitrary sitewise Lorentz change need not preserve those row constraints.
The existing raw and transported-center frame owners already distinguish
that centering defect from an actual field-space gauge action.

At a general e, with H=C(v), the exact polynomial identity is

    G(e+t v)=G(e)+t[H eta Theta^T+Theta eta H^T]+t^2 H eta H^T. (10)

For a freely supplied centered solder the pointwise derivative is onto all
symmetric V, with right inverse

    H=(1/2) V Theta^{-T} eta.                                (11)

Its kernel is exactly H=Theta a, a eta+eta a^T=0. Centering changes that
lifting question: an actual v exists iff every row of H obeys the range
criterion (3), possibly after adding such a frame-type kernel element.
A pointwise submersion theorem cannot silently invert A_r.

For a symmetric metric covector T the exact counting adjoint is

    (DG_e)^* T |_ra = 2 A_r^*((T Theta eta)_ra),
    A_r^*=(1+U_r)/2.                                        (12)

Expand the Frobenius pairing, use T_ab=T_ba to combine its two terms,
and shift the remote-site sum; this proves (12) with all ten packed slots.
It is the pullback of a supplied metric covector. It does not manufacture
a matter action or stress source. A covector in its cokernel is not a
gauge direction in the state space.

## 5. Constructive smooth metric and probe lifts, with no ultraviolet selector

Declare the continuum class explicitly: smooth periodic global invertible
solders Theta on the unit four-torus with uniform bounds on Theta,
Theta^{-1} and the derivatives used below. Set g=Theta eta Theta^T.
This is a nonempty metric class already admitted by the completed-probe
owner. The bounds below follow from the given smooth preparation; they are
not asserted for arbitrary native roots.

Define actual raw field data by rowwise midpoint samples:

    e_L(x)_ra=Theta_ra(hx+(h/2)e_r)-eta_ra.                   (13)

Then the owned centered solder is exactly

    Theta_L(x)_ra=[Theta_ra(hx+(h/2)e_r)
                   +Theta_ra(hx-(h/2)e_r)]/2.               (14)

Taylor's formula with the integral second-derivative remainder gives, entry
by entry, |Theta_L-Theta(hx)| <= h^2 ||partial_r^2 Theta||_infty/8.
The same estimate holds after any fixed number of continuum derivatives
when applied to the smooth interpolation in (14). Matrix multiplication
then gives G(e_L)=g(hx)+O(h^2), with constants determined by the preparation
bounds. For small h, ||Theta^{-1}(Theta_L-Theta)||<1/2; the elementary
Neumann series proves nondegeneracy and ||Theta_L^{-1}||<=2||Theta^{-1}||.
Thus these are nonempty native metric fibers with the allowed vanishing
metric corrections, without an exact-sampling requirement.

For each smooth symmetric probe V use (11) at the continuum Theta and
sample H at the same row midpoints to define v_L. Equation (10) gives

    DG_{e_L}(v_L)=V(hx)+O_V(h^2),
    ||v_L||_infty <= (1/2)||V Theta^{-T} eta||_infty.         (15)

The derivative remainder follows from (14) applied separately to Theta
and H. All ten symmetric components are admitted. No global inverse bound
on arbitrary near-Nyquist data is asserted or required in (15).

There is also an exact straight-metric pencil before sampling. Put
K=Theta^{-1} V Theta^{-T}, and, on a fixed interval |t| ||K eta||<q<1,

    S_t=sum_{j>=0} binom(1/2,j) t^j (K eta)^j,
    Theta_t=Theta S_t.                                      (16)

The absolutely convergent power series has S_t^2=1+tK eta by the scalar
binomial Cauchy product. Since K is symmetric, S_t eta=eta S_t^T.
Consequently Theta_t eta Theta_t^T=g+tV exactly. The convergence and its
fixed finite number of derivatives are uniform on a smaller compact
interval, by the geometric factor q. S_0=1 and S_t is invertible there.
Applying (13) to Theta_t gives one native family with

    G(e_L(t))=(g+tV)(hx)+O_V(h^2),
    partial_t G(e_L(t))=V(hx)+O_V(h^2),                     (17)

uniformly on that interval. This is a constructive metric/variation map;
there is still no native action-contrast equality attached to it.

## 6. A genuine native zero-field root family with a non-Einstein limit

The published [literal flux gate proof](A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md)
derives the first variations of the actual standalone fluxEnergy. Its full
free coframe/field Euler gate is exactly psi=0, with arbitrary e. At psi=0
the actual coframe source, field Euler term and action vanish for every N.
The new construction makes the consequence explicit for the centered metric,
on all required sizes and with corrected metrics rather than exact samples.

Take b=1/10,

    s(y)=1+b cos(2 pi y_A),     Theta(y)=s(y) eta,
    g(y)=s(y)^2 eta,           psi_L=0.                       (18)

Use (13). Writing s_j=1+b cos(2 pi j/L) and
s_{h,j}=1+b cos(pi/L)cos(2 pi j/L), the exact owned readout is

    Theta_L=diag(s_h,-s,-s,-s),
    Q_L=diag(s_h^2,-s^2,-s^2,-s^2).                         (19)

Every (e_L,0) is an exact full root of this standalone native action. Its
source is its own zero-field coframe derivative, not a fitted stress.
These are solutions of the actual finite Euler equations at every level;
compatibility with an additional native interlevel field constraint is not
asserted. The counterexample tests the full levelwise free-gate class.
The field is bounded, and s,s_h>=9/10. The only metric correction is

    |Q_L-g(hx)|_max <= b(1+b) pi^2 h^2.                      (20)

Use 1-cos(pi/L)<=pi^2/(2L^2), and |s_h+s|<=2(1+b).
The smooth interpolated metrics converge in every fixed C^k norm.
At the origin the standard-convention scalar curvature of g is
2400 pi^2/1331; the consumed Einstein-owner convention reverses this sign.
The standard covariant Ricci entries there are

    Ric_00=12 pi^2/11,       Ric_ii=-4 pi^2/11,
    G_00=0,                 G_ii=8 pi^2/11 (i=1,2,3).         (21)

Thus the vacuum Einstein equation fails, in either convention.

This family also tests the requested completed contrast, rather than only
pointwise curvature. Use the fixed straight probe V=g and g_t=(1+t)g,
|t|<=1/2. Multiplying the entire raw solder in (13) by sqrt(1+t)
(including its eta background before returning to e coordinates) makes
Q_L(t)=(1+t)Q_L(0) exactly. The actual scale identity is compiled. The
physical positive-determinant representative is E_L(t)=Theta_L(t) eta;
its diagonal entries are positive. The native field remains zero, so both
native endpoint actions and its source subtraction are exactly zero.

In the completed probe owner's sign and normalization,

    I(g)=(1/2) integral sqrt(|det g|) R_owner
        =-3 integral (s')^2=-3 pi^2/50,
    I((1+t)g)=(1+t)I(g).                                   (22)

The factor one-half is retained. The action correction can also be bounded
directly, without differentiating an asymptotic estimate. For a smooth
periodic metric diag(a^2,-s^2,-s^2,-s^2), with a,s>0, the complete
Christoffel/Ricci contraction gives

    R_std=-6[s''/(a^2 s)+(s')^2/(a^2 s^2)-a's'/(a^3 s)],
    (1/2) a s^3 R_owner = 3(s^2 s'/a)' - 3s(s')^2/a.

Consequently the smooth interpolant of the exact corrected metric (19)
has

    I(Q_L)=-3 integral s(s')^2/s_h,
    |I(Q_L)| >= 27 pi^2/550,
    |I(Q_L)-I(g)| <= pi^4 h^2/300.                         (22a)

For the lower bound use s/s_h>=9/11 and integral (s')^2=pi^2/50.
For the error use |s/s_h-1|<=b(1-cos(pi/L))/(1-b), then
1-cos(pi/L)<=pi^2 h^2/2. Periodicity kills the displayed total derivative.
This calculation retains every nonzero first-jet contribution and is
independently checked in all 64 connection and 16 Ricci slots.

The [published finite-probe theorem](https://github.com/gvakhrushev/d0_15/blob/dae0ec13f9f885ff945c45613ae38becbc097d18/02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md),
with all 24 connection residual rows, now gives for epsilon=h^(1/3)

    Delta I_h(V)=epsilon I(g)+O(h),   Delta I_h^N(V)=0.       (23)

Its preparation bounds hold on this explicit compact smooth pencil.
The interpolated Q_L(t) form a uniformly smooth, nondegenerate two-parameter
family and differ in C^k by O(h^2); using those actual readout metrics
instead changes the continuum half-contrast by O(epsilon h^2). The same
uniform finite-preparation estimate then proves (23) with the metric
correction included. No derivative of an asymptotic error is used.
For all sufficiently small h the discrepancy is at least
(3 pi^2/100) h^(1/3), so it cannot obey a C_V h bound for any fixed
nonzero calibration. Even changing the calibration with h cannot change
the exactly zero native half-contrast. This is an inhabited native
stationary branch, not a definition that builds in Einstein stationarity.

This is a **scoped soundness counterexample for the literal standalone
full-gate flux action with its actual centered Gram metric readout**, when
admissibility consists of those levelwise equations. A stricter refinement-
compatible class must establish its own nonempty admissible fibers; this
sequence is not offered as proof of that missing compatibility.
It is not an off-shell coframe probe or an empty-fiber argument. It does
not classify combined native actions, constrained sectors, a different
readout or the original #310 fixed-source/raw-owner terminal. A connection
variable is absent from this standalone action; it is not supplied by this
metric construction.

## 7. Remaining arrow and verification boundary

The field-to-metric and smooth-variation parts are now constructive for the
specified existing readout and smooth class. This removes an existence
ambiguity about (13)--(17), but does not select these fields as physical
solutions of a successful joint theory. The native refinement/action/source
maps must still be constructed together. The former cochain and point-state
refinement obstructions keep their exact scopes; midpoint sampling does
not change the native transition law or prove commuting readouts.

The actual centering kernel/adjoint, metric polynomial/tangent bindings,
raw scaling and literal zero-field Euler controls are compiled where indicated in the
accompanying capsule. The all-size Fourier classification, nonlinear fiber
criterion and quantitative smooth preparation/limit proofs above are
analytical; exact finite checks do not substitute for them. The previous
rank theorem and previously proved full flux gate are reused with explicit
source pins. The exact nonlinear fiber criterion retains the explicit
Lorentz representative constraints; it does not claim to solve their
feasibility for every arbitrary finite metric.

The capsule checks 17 new propositions and two existing packed-metric/raw
Nyquist propositions, with 53 transitive D0 source pins. Their 19 printed
axiom reports contain only propext, Classical.choice and Quot.sound.
Five actual declaration types are printed. The older nonzero-H Nyquist
declaration is only type-checked here; its separate native_decide evaluation
dependency is not disguised as a new standard-axiom proof. The earlier full
flux-gate derivation and the published physical-probe proof are separately
pinned. The checker replays 88 grouped exact controls, including every
metric slot, its factor-two packing, variable-background adjoint, midpoint
samples, full Ricci/Einstein jet contraction, half-action sign and the
explicit action bound for the corrected finite metrics.
Five hostile ledgers falsify the inverse bound, Einstein source, action
normalization, global GR status or interlevel compatibility; each is rejected.
