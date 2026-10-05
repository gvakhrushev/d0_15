# Conformal forward-response bridge without an unknown-field derivative bound

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `cc6cc38f3e7053b6473cdeee65c17fadad6275d7`.
Status: analytic forward-response theorem on the declared amplitude class,
independently audited with exact finite controls. The original
fixed-chart/raw-owner terminal remains PARTIAL / OPEN.

## 1. Statement

Let g be one fixed smooth nondegenerate periodic metric with the owned smooth
oriented Lorentz solder E. Let A_h be arbitrary log fields on the actual finite
lattice such that all 24 literal physical connection Euler rows vanish and

    sup |A_h| <= R h.

There is no spatial derivative, C7, Fourier, phase, or curvature assumption on
the unknown A_h. For every fixed smooth scalar probe psi,

    h^2 sum_x Xi(g_h,exp A_h)_x : [psi(hx) g(hx)]
        = integral rho0[g] : (psi g) + O_psi(h^(2/3)).       (C1)

The error is uniform over the entire declared stationary log-O(h) class.
In particular, if the original exact metric equation also holds with ONE
independently fixed smooth ten-slot density tau,

    Xi(g_h,exp A_h)_x = h^2 tau(hx),

then

    g : (tau-rho0[g]) = 0 pointwise.                         (C2)

This is a local trace constraint, not merely the existing integrated radial
Ward constraint. It leaves the nine traceless source directions unclassified.
The parent's fixed sufficiently small chart does not itself imply log-O(h),
so (C1) cannot be claimed for that entire parent class.

## 2. Exact weighted Hessian transport identity

Use log-coordinate F_h=grad_A scriptA_h and H_h(q)=D_A F_h(q,0), the true
finite symmetric Hessian. Full physical EK and F_h differ by the uniformly
bounded invertible differential of exp in a shrinking log ball. The following
argument retains all 24 rows and every face/shared-link incidence.

For lambda(y)>0 and the exact conformal metric q_lambda=lambda g, choose
E_lambda=sqrt(lambda) E. Each literal naked-star face weight at its base z
is EXACTLY lambda(hz) times its weight for E. Hence every contribution to
the Hessian row of a link based at x is multiplied by its face-base lambda_z.
Locality gives, for every arbitrary field D,

    [H_h(q_lambda) D]_x
      = lambda(hx) [H_h(g) D]_x + T_h(lambda)D_x,
    |T_h(lambda)D_x| <= C h |D|_infty.                       (C3)

Indeed subtract the two sums term by term: the difference is a sum of the
same bounded local Hessian coefficients multiplied by lambda_z-lambda_x.
All face bases z in that row lie a uniformly bounded number of steps from x.
Thus |lambda_z-lambda_x|<=C h. No unknown-field derivative is used.

The analogous identity for F_h at identity contains an O(h) identity forcing;
one must retain it. Simply freezing A_h and declaring the conformal endpoints
prepared would be wrong.

## 3. Explicit same-central-state approximate horizontal continuation

Fix lambda_s=1+s psi, |s|<=s0, positive. Let

    q_s=lambda_s g,
    B_h(s)=h omega_LC[q_s],
    D_h=A_h-B_h(0),
    A_h(s)=B_h(s)+D_h.                                     (C4)

Here the coefficient convention is precisely the owner's full leading
smooth Palatini preparation. The existing all-coframe / arbitrary-first-jet
Palatini calculation gives

    |B_h(s)| <= C h,       |F_h(q_s,B_h(s))| <= C h^2,

uniformly on the fixed smooth metric pencil. Also |D_h|<=C h. Finite-stencil
analyticity gives, for every arbitrary such D,

    F_h(q_s,B_h(s)+D) = F_h(q_s,B_h(s))+H_h(q_s)D+O(h^2).

At s=0, exact stationarity of A_h implies H_h(g)D_h=O(h^2). Applying (C3)
then gives H_h(q_s)D_h=O(h^2). Therefore

    |EK(q_s,exp A_h(s))| <= M_psi h^2,                     (C5)

uniformly in s, h, and the arbitrary rough central root. This explicitly
inhabits the already declared completed preparation domains through EACH
retained central exact root. No inverse Hessian and no selector is added.
The endpoints are approximate stationary preparations, not exact endpoints.

## 4. Uniform smooth-parameter bounds

Let f_h(s)=I_h(q_s,A_h(s))=h^2 scriptA_h(q_s,A_h(s)). The field D_h is
independent of s. Each derivative up to order three of A_h(s) is O(h),
because only the known smooth LC preparation varies.

Expand the literal local analytic action at identity:

    scriptA_h(q_s,A)=ell_h(s).A + (1/2) A^T H_h(s) A + R_h(s,A).

The action at identity vanishes exactly. Its full identity gradient ell_h
and every fixed smooth-parameter derivative up to order three are O(h):
for a constant solder the incident identity-link variations cancel, and
smooth solder differences across the finite stencil are O(h). The Hessian
and its smooth-parameter derivatives have bounded finite row multiplicity
and bounded coefficients. The cubic remainder and its first three s
derivatives, evaluated on A_h(s), are bounded by C N_h h^3, N_h=h^-4.
All derivatives of the linear and quadratic terms are bounded by C N_h h^2.
Multiplying by h^2 yields

    sup_|s|<=s0 |f_h'''(s)| <= C_psi,                       (C6)

independently of h and of unknown-field spatial derivatives. This is an
ordinary third parameter derivative; it is not a lattice derivative.

## 5. Identification of the actual forward derivative

By (C5), the already proved rough-preparation action stability theorem gives

    sup_|s|<=s0 |f_h(s)-I(q_s)| <= C_psi h.

At the central state s=0, the full chain rule and exact EK=0 give

    f_h'(0)=h^2 sum_x Xi_x : [psi(hx) g(hx)],               (C7)

because the connection derivative paired with A_h'(0) is zero exactly.
Thus this construction keeps the actual retained root's forward response;
it is different from differentiating independently re-prepared action values.

The centered secant Taylor estimate using (C6), together with the uniform
action limit, gives

    |f_h'(0)-DI(g)[psi g]| <= C_psi (h/epsilon+epsilon^2).

Choosing epsilon=h^(1/3) proves (C1). Substituting the exact source equation
and using the smooth Riemann-sum limit gives

    integral psi g:(tau-rho0) = 0 for every smooth psi.

The fundamental lemma proves (C2).

## 6. Why this does not close all ten components

The decisive algebraic property was face weights multiplying by the SAME
local scalar lambda across all six faces. For a general traceless metric
pencil the constant-solder Hessian changes its high-phase kernel; the error
H_s D-lambda H_0 D can have O(h), rather than O(h^2), magnitude. The existing
exact hostile coframe congruence control already checks this failure:
at phase (1,i,1,1), E=diag(1,1,t,t), the attempted all-phase coframe congruence
has eight nonzero entries, including -i t^2(t-1) at (12,13).

Therefore neither (C4) nor (C5) extends by that calculation to arbitrary
metric probes. The remaining task is an actual traceless horizontal transport
or a different forward-normal theorem. Scalar critical values alone still
miss singular conormal channels, exactly as in the retained toy control.

## 7. Exact finite control

The [checker](certificates/a4d_conformal_forward_response_check.py) imports the unchanged
literal naked-star generator/weight owner, assembles every full physical Euler
row with independently weighted face bases, and replays degree-two jets with
arbitrary rough first-order link perturbations. It verifies coefficientwise
that after subtracting the identity forcing the weighted-Hessian commutator
starts at degree two, and that omitting the identity forcing gives a nonzero
degree-one residual. Constant conformal scale rescales every full row exactly.
These finite controls check (C3)'s incidence algebra; the h-dependent analytic
bounds (C1)-(C6) are the proof above and are not extrapolated from samples.


## 8. A legal amplitude enlargement and exact scope owner

The original H-DOMAIN is A4D_J2_METRIC_RESPONSE_SENSITIVITY.md Section 1:
its dimensionless logarithms satisfy |A|<=rho, with rho independent of mesh;
it explicitly says that no formula in that chart divides by h. Thus a fixed
UV amplitude cannot be covered by the preceding h-scaled hypothesis.

The same proof DOES extend to an arbitrary amplitude schedule r_h>=h with

    |A_h|<=r_h,     r_h^3/h^2 -> 0.                         (C8)

For instance r_h=R h^alpha, alpha>2/3. Use the same explicit path (C4).
Then H_0 D=O(r_h^2+h^2), and (C3) gives endpoint residual
O(r_h^2+h r_h+h^2), with no derivative of D. The existing trapezoidal
identity (not the special Rh preparation theorem) compares its action with
the smooth LC preparation and gives

    sup_s |f_h(s)-I(q_s)| <= C r_h^3/h^2.                  (C9)

All incidence constants remain uniform in the original fixed analytic chart.
The parameter third derivative remains bounded under (C8). To see this without
an incorrect r_h/h bound, use that q_s=(1+s psi)g makes ell_s and H_s EXACTLY
linear in s. Hence the potentially large ell_s.D and D^T H_s D terms have
zero third derivative. For the cross term D^T H_s B_s, use H_s D bounded by
C(r_h^2+h r_h+h^2); after pairing with B_s derivatives O(h), its normalized
third derivative is O(r_h^2/h+r_h+h). Explicitly, because the conformal weights are linear in s,

    H_s D=(1+s psi_x) H_0 D+s T_h(psi)D,
    H_s' D=psi_x H_0 D+T_h(psi)D=O(r_h^2+h r_h+h^2).

The cross term's third derivative is

    (H_s D):B_s''' + 3(H_s' D):B_s'',

which has exactly the bound just stated. The analytic cubic remainder derivatives
are O(r_h^2/h+r_h+h) as well, because every parameter derivative hitting a
link supplies an O(h) factor and third differentiation cannot all fall on the
linear conformal weight. Condition (C8) implies r_h^2/h->0. The remaining
known smooth LC terms have uniformly bounded derivatives.

Taking epsilon=(r_h^3/h^2)^(1/3) proves the stronger estimate

    | h^2 sum Xi:psi g - integral rho0:psi g |
        <= C r_h^2/h^(4/3).                               (C10)

Thus fixed-source local trace compatibility (C2) holds throughout (C8),
including amplitudes substantially larger than h, but not fixed amplitude.
No endpoint is claimed to belong to the narrower Rh,Mh^2 domain when r_h>>h.

An immediate scoped impossibility corollary is: an exact fixed-source vacuum
tau=0 in (C8) forces R[g]=0 pointwise. In particular a nonconstant periodic
positive conformal factor depending on one non-null coordinate cannot support
such vacuum roots: scalar-flatness reduces to the one-dimensional equation
phi''=0, so periodic phi is constant. For general Lorentz conformal factors,
wave-harmonic null-dependent factors can remain nonconstant; no global
constant-factor statement is claimed.


## 9. Fixed-chart Weyl-spin correction: exact first obstruction

The [full finite hostile control](certificates/a4d_y_weyl_spin_transport_check.py) retains the
owned exact flat Y(t) joint vacuum at arbitrary small FIXED t. Its physical
Role0 links have four phases (U,I,U^-1,I), U=Cayley(tY), other links identity.
For a slow conformal first jet lambda=1+epsilon y1, the ordinary continuum
Weyl spin correction is

    W0=J01/2, W1=0, W2=-J12/2, W3=-J13/2.

Compute the COMPLETE connection Euler after each of the three standard
multiplicative transports U exp(epsilon Wr), exp(epsilon Wr) U, and their
symmetric first variation (U Wr+Wr U)/2. At t=0 each cancels the entire
identity forcing in all 24 rows and all four phases. For every one of the
three transports, phase 0, Role1, spin generator J12 instead has

    EK[phase0,Role1,J12] = epsilon t(2+t)/(2(4+3t^2)) + O(epsilon^2).

After clearing D^4=(4+3t^2)^4 on EVERY link, the full first slow-gradient
Euler is a COMPLETE degree-eight polynomial, and all its coefficients in t
and every phase and full Euler row are pinned in the adjacent immutable ledger.
The closed formula above is checked as an exact polynomial identity, rather
than extrapolated from low-degree samples. Its leading coefficient 1/4 is exact. Thus for any sufficiently small fixed nonzero t the ordinary
Weyl correction leaves O(h t), not O(h^2), at a mesh-scale smooth gradient
 epsilon=O(h). For t=O(h) that same obstruction is O(h^2), exactly consistent
with the theorem's amplitude threshold. Frozen links without any correction
already leave a nonzero degree-zero-in-t slow-gradient forcing.

This is an exact obstruction to these universal standard corrections, NOT
a proof that no UV-dependent correction exists. Such a stronger conclusion
would require the full UV Hessian solvability pairing or nonlinear horizontal
obstruction, which this check does not compute. It identifies concretely why
one cannot silently extend (C5) to all fixed-chart #232 amplitudes.
