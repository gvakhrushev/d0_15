# Same nonvacuum Brinkmann representative: exact paid-port residual and its CAR-parity location

20 October 2026. Existing scientific Draft #334 / EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE; `native-programme-v1`, consumer `constitutive` -> `native_sector` -> `gr_operational_realization`. Scientific inputs frozen at `313923d2dad60bff4038d8f4414528c9f3e5ad7a`; main input `0bf309b6260cf5b63e54d6ccabdcdae6734b950a`.

**Result:** the actual known two-round port-cost source is evaluated on the exact nonvacuum J2 Brinkmann fields, with the corrected coframe/link map and the full normalized scalar/top/clock section. Its explicit coherent counting-site lift has a nonzero *material* Euler residual. All 16 coframe and 24 independent Lorentz directions on one free transverse column, and the two material rows, are computed without freezing the Julia roots, the second round, or normalization. A separate analytic theorem explains the leading residual at every mesh and every finite port horizon: the null scalar/top perturbation is even, the vacuum clock section is odd, and the positive native Dirac operator is odd. The mixed material/geometry Hessian vanishes while the material Hessian is positive. Thus a connection-only Schur correction cannot remove this particular source in the known port-plus-independent-geometric component model.

This is NOT an identification of port cost with complete Book03 Cost-Info. The coherent site lift is an explicit conditional comparison map, not a derived compulsory G0 preparation or the old full-rank128 Riesz branch. No new selected action, source cancellation, gauge constraint, independent acceptance, or GR closure is asserted.

## 1. Existing results composed, not repeated

| Owned input | Exact use here |
|---|---|
| `D0_GR_PRIMARY_POSITIVE_CASE.md` and the original `arbitrary_brinkmann_all40.md` | Supply the actual configured 16+24+2 zero-source family, the advanced Cartan link and the null scalar/top source; no new search for Einstein solutions |
| `check_exact_null_marked_curvature_readout.py` at 313923d2 | The same positive null-dual probe reads Ricci and Weyl separately on the chosen finite representative |
| `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` §§1-5 | Supplies the actual 128-outcome channel, its paired Julia recycling, port code and flat energy conservation |
| `A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md` §§1-4,7 | Supplies the exact paid-history source, real clock bookkeeping and corrected map `e_N=nu^-1 S e_J2`, `U_N=S U_J2 S^-1` |
| Its full24 stationary connection calculation | Is retained at its protected8 Fourier input, not falsely transplanted to this scalar/top preparation. The parity theorem below determines whether connection relaxation can supply the missing material source |

The difference from the previous protected8 sine-profile test is substantive: the new fields are already a configured **nonvacuum Einstein solution**, and the preparation is the actual four-grade scalar/top/clock section of that positive case, not an excited protected8 eigenshell. The comparison remains conditional on its explicitly stated site lift.

## 2. One finite representative and its preparation map

Use the original null basis with eta_(+-)=eta_(-+)=1, eta_xx=eta_yy=-1. Let k=2*pi and sigma>0 be small. On h=1/L, define

    lambda = lambda_-(2^-20),
    E = k^2 sigma^2,
    H(x,y) = -lambda E (x^2+y^2) + A_W (x^2-y^2),
    r_h = kh / (2 sin(kh/2)),
    Psi_j^h = sigma r_h (cos(k u_j), sin(k u_j)).                  (1)

This is an actual midpoint history: `Psi_(j+1)^h-Psi_j^h = h Psi'(u_j+h/2)` for the fixed continuum field `Psi(u)=sigma(cos ku,sin ku)`. Its finite norm is constant and its genuine difference energy is EXACTLY E for every h. The transverse five-point Laplacian gives `Delta_perp,h H = -4 lambda E`; the quadratic Weyl term is exactly discrete harmonic. The owned all40+2 reduction therefore makes every free interior configured J2 Euler row zero. Use periodic u/v as a mathematical regulator and a fixed transverse collar; no periodic physical causal time is claimed.

The true advanced Cartan link has

    K_x(z) = [H(z+u)-H(z+u-x)]/2,
    K_y(z) = [H(z+u)-H(z+u-y)]/2.

Here H is u independent, so the advance is literal but numerically unchanged. Set `S=diag(1,1,-1,-1)`, `nu=3/5`. The native positive-spatial creator legs and proper links are

    V_u=nu e_-, V_v=nu(e_+-H e_-/2), V_x=nu e_x, V_y=nu e_y,
    U_u=exp(-K_x N_2-K_y N_3), U_v=U_x=U_y=I.                    (2)

The minus sign in (2) is the corrected physical coframe map, not the earlier mislabeled LC sign. The observer `n=(1,1,0,0)/sqrt(2)` gives its positive Gram I in this null basis. The proper exterior lift of S fixes all four masks 1,0,15,14 used in the original material section.

Retain that complete normalized section:

    m_j=sqrt(p)|1> + psi_0,j|0> + psi_4,j|15>
        +sqrt(p^2-|Psi_j|^2)|14>,       p+p^2=1.                 (3)

The explicitly supplied comparison lift is

    Omega_h = L^-2 sum_(u,v,x,y) |u,v,x,y> tensor m_j.            (4)

It has norm one on the full `L^4 x CAR16` data carrier. This is a **coherent counting-site lift**. It is not an assertion that the actual unequal Golden LEFT/AF preparation or full fixed-Gram reference128 purification is already (4). The known channel tensors identity on an arbitrary untouched oldRIGHT; a selected correlated full128 preparation still needs its actual map. Neither pure-state normalization nor a spectator reference supplies that missing physical admission.

For this static geometry, all native Kraus operators and the source directions used below preserve u/v translation. The input (4) has u Fourier modes 0,+1,-1 and v mode0. The cost effect is block diagonal in those modes. Computing its trace from three blocks is therefore an **exact contraction** on the full carrier, not deletion of unoccupied modes, thermal modes, cross-mode memory, or failure records. The full state remains coherent; this argument concerns the stated prepared observable and its variation only.

## 3. Exact full two-round paid-source operator

Use the original definitions with the actual shifted positive adjoint:

    C_r=C(V_r), P_r=C_r Lambda(U_r) shift_r,
    D=h^-1 sum_r(P_r-C_r) + adjoint,
    Delta=D^2, epsilon=p^2 h^2/64.

The original paired recycling map is `T(X)=(1/16) sum_(i=1)^32 W_i X W_i*`, with, for each role, `W=(P,P*,sqrt(I-PP*),sqrt(I-P*P),C,C*,sqrt(I-CC*),sqrt(I-C*C))`. The paired list is also self-adjoint as a superoperator. Every actual native label/coefficient/port is retained.

The already-derived price identity becomes the exact finite operator

    E C_port,2 = 2 + <Omega, H_2 Omega>,
    H_2 = 2p epsilon Delta
          + p epsilon^2 [D T(Delta) D-Delta^2].                 (5)

There is NO truncation in native time in (5). It is the full two-round expectation, including all 128^2 ordered outcomes, via the proven channel contraction. The number 2 is the paid baseline, not a field source at fixed clock. Two native port rounds are not silently identified with two configured scene-J2 steps.

At fixed fields, the complete preparation source is

    d C_port,2 = 2 Re <dOmega,H_2 Omega>.                        (6)

For a real matter variation, the last amplitude of (3) changes:

    d m_14 = -(psi_0 dpsi_0+psi_4 dpsi_4)/sqrt(p^2-|Psi|^2).     (7)

Thus the full material covector contains the subtraction from the actual grade14 component; a frozen normalization is not used. Field sources differentiate D and every W. The positive-root derivative is computed by its Sylvester equation `R dR+dR R=d(R^2)` on a verified strict positive chart. No square root, recycling term, or second-round preparation response is frozen.

## 4. Actual nonvacuum evaluation: explicit internal residual, not another spectrum catalogue

The default replay uses L=10, sigma=1/100, A_W=3/100, nu=3/5. Its full carrier has 10,000 sites and all16 CAR grades. The smallest tested Julia-defect eigenvalue is >0.6372. All configured interior geometric/matter residuals vanish by the exact original theorem; the replay's reduced-stencil error is below 2e-15.

The same two fixed null-dual probes are transported with S together with the plaquettes. At probe strength 1/4 the two actual positive marks are

    m_x=0.3818491007992323, m_y=0.38190638577041647,

and invert to

    a_ux=-0.0012244426845455791,
    a_uy=-0.0006244426845434248,
    Ric_uu=0.18488853690890036, A_W=0.03000000000010771.          (8)

The actual two-round port calculation gives

    R=<Omega,Delta Omega>=0.0020502578011074154,
    Gamma=<Omega,[D T(Delta)D-Delta^2]Omega>
         =-2.6310969212725577e-7,
    E C_port,2=2.000000151250066.                               (9)

Gamma need not have the sign of the old protected8 calculation: its preparation and physical family are now different. Both terms in (9) are retained.

Take a compactly supported transverse material tangent at the central free column:

    dPsi_j = chi(x,y) Psi_j,   chi=1 only at the central x/y site,

with (7), fixed geometry and unchanged original clock amplitude sqrt(p). It is a real normalized variation, not a change of the initial-state norm or the outer boundary. Then

    D_chi E C_port,2 = 2.0969052019918353e-9,
    D_chi E C_port,2 / (2p epsilon) = 2.842442552963308e-5.      (10)

An independent central finite difference on the normalized preparation curve gives `2.0969052021472137e-9`. All configured scalar/top Euler rows are zero on the same fields: `q=0` and their full first variation is killed by the genuine v-Stokes identity, not by varying only an ansatz. The existing Palatini term has no material dependence. Therefore (10) is an explicit residual against **any scalar multiple** of their zero material covector, under map (4).

The receipt also contains all 16 native-leg and 24 independent proper-link covectors on that free transverse column. These are genuine variations constant in u/v, NOT a claim to have computed every unsymmetrized site row of the full four-dimensional Jacobian. The two material Euler components are reconstructed on every u/transverse site, with their complete normalization correction. Their contraction exactly reproduces (10). Changing the far fixed collar changes (10) by zero at displayed precision.

These decimal values are an author numerical replay, **not** an independently accepted interval enclosure. The next section supplies a separate exact structural statement and a nonzero small-amplitude conclusion without inferring a theorem merely from floating-point sign.

## 5. Exact all-mesh material coefficient and why the existing connection Schur cannot screen it

For the analytic small-amplitude family set `A_W(sigma)=300 sigma^2`. This contains (8)-(10) at sigma=.01 and tends to the native flat background. At sigma=0,

    m_0=sqrt(p)|1>+p|14>        (odd CAR parity),
    d m/dsigma = r_h[cos(ku)|0>+sin(ku)|15>] (even parity),
    D_0 m_0=0,
    Delta_0(k)=4nu^2 h^-2 sin^2(kh/2) I16.                     (11)

The forward difference and the forced r_h factor give, exactly,

    ||D_0 (dOmega/dsigma)||^2 = nu^2 k^2                       (12)

on every mesh. The flat original full128 channel conserves this Delta energy; its full n-round paid excess operator is `n p epsilon Delta_0`.

**Theorem.** For every finite integer n and every permitted h on this explicit smooth field/preparation family,

    (d^2/dsigma^2) E C_port,n |_(sigma=0)
       = 2 n p epsilon_h nu^2 k^2 > 0.                        (13)

Proof: H and the true links first change at order sigma^2, while the even material amplitudes first change at order sigma. The initial odd clock is dark. For the known positive port observable, the cost of changing only that dark state’s geometry by O(sigma^2) is O(sigma^4): every nonzero-port amplitude is O(sigma^2). Its contribution to the second variation is zero. The normalized baseline n stays constant. The remaining quadratic coefficient is exactly `n p epsilon ||D_0 dOmega||^2`, by the already-owned flat energy conservation. Equation (12) finishes the proof. This is a finite-history statement, not a continuum assumption.

**Connection and coframe mixing.** At the same flat seed, every proper-Lorentz exterior action preserves CAR parity, and the actual creator-minus-shift Dirac operator, with its positive adjoint, is odd. Thus any independent coframe/link/observer variation has odd `dD`. Since m_0 is odd, `(dD)m_0` is even, whereas `D_0 dOmega_material` is odd. Consequently

    H_(material,geometry) = 0                                 (14)

for this port-cost Hessian, including all24 connection components. The finite-history quadratic identity can also be seen from the native Kraus words: the base is dark, and at first order the even and odd amplitudes in every paid branch remain orthogonal. The original recycling has `T_0(Delta_0)=Delta_0`; hence its energy-production correction has no total-degree-two term at a dark background.

Additional internal *even* preparation directions which do not change the prescribed scalar/top amplitudes are orthogonal to the material wave. Because Delta_0 is scalar on that Fourier sector, their quadratic energy cross term also vanishes. Odd preparation directions can couple to geometry, but not to this even material block. Thus, on any regular stationary quotient of these internal directions, Schur elimination of the **known port component plus an independent purely geometric Palatini form** leaves the coefficient (13) intact. This is not a theorem about a yet-unspecified full Book Info, whose mixed material source may differ. A constraint changing the admitted material variation must be proved from the physical programme.

This is the useful composition with the earlier full24 result: solving its geometric sourced block is valuable, but cannot by itself supply the missing massless scalar/top equation on this family. No new rank census is needed to decide that question.

If a chosen native positive clock satisfies `beta_h=n_h epsilon_h -> beta>0`, the exact Hessian values obey

    lim_h d_sigma^2 E C_port,n_h(0) = 2p beta nu^2 k^2 > 0.     (15)

Only this exact linearized coefficient is transported. No uniform finite-amplitude expansion, source-to-solution inverse, relation to scene ticks, or nonlinear GR refinement is inferred. In contrast, the configured J2 action has f=q=0 on the complete solution family and zero material Euler there.

## 6. The two new advances now meet in one quantitative equation

For the compact relative-amplitude tangent of (10), the leading small-sigma source is

    D_chi C_port,n/(n p epsilon)
       = 2 nu^2 k^2 sigma^2 mean(chi) + O_h,n(sigma^4)
       = -nu^2 Ric_uu/lambda * mean(chi) + O_h,n(sigma^4).      (16)

The order statement uses the fixed Golden parity-covariant channel and the specified family; its remainder is not asserted uniform at growing n. The Ricci in (16) is recovered from the **same actual two positive null probes** in (8). No Newton coefficient, free source scale or fitted stress was inserted. At the replay point, the leading right side is `2.8424460675141278e-5`, while the complete finite two-round left side is the value in (10). Weyl is independently measured but does not supply a compensating leading scalar source.

Equation (16) is a comparison of a measurable curvature with an explicitly paid residual, NOT an assertion that Fisher information, port cost or measured curvature is the mandatory action. The h^4 single-probe information budget remains the original observation theorem's independent sampling statement.

## 7. Exact missing substitution, rather than an invented repair

Write only as a bookkeeping split of an ACTUALLY derived complete action

    S_full = C_port + C_remaining - I_actual.

The remaining terms include real labels, preparation, reference, observer, controller, clock and work. No term is defined by subtracting the answer. If that action is to have the same first source as the configured Einstein-scalar family under (2)-(4), then on the tested material tangent it necessarily satisfies

    D_chi(C_remaining-I_actual) = -D_chi C_port.                (17)

On a common stationary internal section retaining the physical material field, the corresponding null-sector second source must cancel (13), or a proved equation/observation transport must explain why the physical tangent or preparation differs. The actual source/normalizer/preparation jets, not an arbitrary negative term, decide this.

The task has therefore been reduced from 'compare two impressive constructions' to a specific same-representative conditional source equation with a nonzero computed operand and an exact parity explanation. The next executable scientific step is to derive `D(C_remaining-I_actual)` from the real signed Book/Golden record on the same scalar/top sector, or prove a different native preparation/clock interpretation. It is not another construction of a nonflat metric, an extra scalar curvature invariant, or a re-fit of the geometric coefficient.

**Remaining scope boundaries:** coherent counting-site map (4) is supplied, not physically forced; complete fixedRIGHT128 pure preparation is not selected by this calculation; native port rounds and scene-J2 ticks are different unless a clock map is proved; the complete Book action is still unknown; the numerical witness is not interval acceptance; no whole-action joint stationary recovery or GR/raw216 closure is claimed. `GR_closed=false`.

## 7a. Apply the complete recorded information to the SAME material source

24 October 2026; input a28019143fe4d302770e5a42df8533f89aa85794.
This is an application to (17), not another choice of detector or a
derivation of compulsory Book Info. It consumes the original full128
blank-word identity, the exact primary preparation (4), and the complete
CQ/Gibbs source identity in
[A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md, section14.3a](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#143a-spatial-heat-complete-cq-information-and-the-actual-recycling-defect).
All statements below are at fixed finite mesh h and positive integer n.
Use the small-amplitude family of section5, including A_W=300 sigma^2,
a strict Julia chart and B=I-alpha_h Delta>0, with
alpha_h=epsilon_h/2=p^2 h^2/128.

### Exact complete-history birth without enumerating the tape

Write xi=partial_sigma Omega|_0. By (11)-(12),

    ||xi||^2 = r_h^2,
    Delta_0 xi = lambda_h xi,
    lambda_h = 4 nu^2 h^-2 sin^2(kh/2) = nu^2 k^2/r_h^2,
    D_0 Omega_0 = 0.

For the ACTUAL chronological fine Kraus words M_omega, the all-blank word
is M_(0^n)=B^n; completeness retains every other word, including zeros.
Put b_h=1-alpha_h lambda_h and

    a_(h,n) = r_h^2 (1-b_h^(2n)) > 0.                         (18)

At the dark flat input every nonblank word annihilates Omega_0.
For omega different from 0^n its output vector therefore has the expansion

    v_omega(sigma) = M_omega(sigma) Omega(sigma)
                  = sigma M_omega(0) xi + O_(h,n)(sigma^2).

The geometry starts changing only at order sigma^2. Completeness gives

    sum_(omega != 0^n) ||M_omega(0)xi||^2
      = <xi,(I-B_0^(2n))xi> = a_(h,n).

Consequently q_(0^n)=1-a_(h,n)sigma^2+O(sigma^3), and the Shannon
entropy of the COMPLETE fine record, in natural logarithms, is

    H_fine(sigma) = -a_(h,n) sigma^2 log(sigma^2)
                   + O_(h,n)(sigma^2).                      (19)

No positive-support assumption is imposed on each individual word.
A word with zero leading vector has probability O(sigma^4) and does
not contribute to the leading logarithm. No reset, coarsening of
labels, or restriction to the occupied input Fourier modes changes
the actual instrument in this argument.

### The actual compact material Euler direction

Use exactly the variation in (10),(16): at the given geometry set
delta_chi Psi=chi(x,y)Psi, with chi supported in the free transverse
interior, and differentiate the grade14 square root as in (7).
The physical coframe, links, clock amplitude and collar stay fixed
in THIS derivative. Then

    delta_chi Omega = sigma chi xi + O(sigma^2).

For a nonblank word the corresponding leading output derivative is
sigma M_omega(0)chi xi. Hence the total leading probability derivative is

    2 Re <xi,(I-B_0^(2n))chi xi>
      = 2 a_(h,n) mean(chi).

This uses B_0 xi=b_h xi and self-adjointness; chi need not commute
with B_0. The mean is the original counting-site mean, the same
normalization as (16). The complete first source is thus

    D_chi H_fine
      = -2 a_(h,n) mean(chi) sigma^2 log(sigma^2)
        + O_(h,n,chi)(sigma^2).                              (20)

For a word with vanishing leading vector, its entropy derivative is
bounded by
2 ||v_omega|| ||delta_chi v_omega|| |log ||v_omega||^2|
=O(sigma^3 |log sigma|)=o(sigma^2).
At exact zeros use the continuous extension of the entropy derivative
along this smooth amplitude curve. Thus (20) does not differentiate
log0 or discard a support birth. Branch-by-branch parity is unnecessary.

### Which information (20) actually computes

Let Theta_n be the complete coherent output of the same Stinespring
execution and Gamma_n its restriction/pinching to the full declared
fine-pointer algebra, retaining conditional DATA and oldRIGHT.
For the supplied pure DATA input (4) and an untouched PRODUCT
oldRIGHT state rho_R, every conditional DATA branch is pure. Exactly,

    S(Gamma_n)-S(Omega_in) = H_fine,
    Omega_in = |Omega><Omega| tensor rho_R.

The oldRIGHT entropy, including its derivative if rho_R moves
independently, cancels on the two sides. This does not identify
the full fixed-Gram pure reference128 lift with (4): its nonlocal
density kernel and Rayleigh source differ even when its local CAR
readouts agree. The owned fixedRIGHT preparation source is preserved.

The pinching here can be restriction to the specified readable
record algebra; it is not an uncharged physical erasure operation.
The entropy of the ENTIRE coherent closed system is instead
preserved by its isometry. Its coherent record subsystem entropy
also need not equal H_fine. Thus internal physical memory and
closedness, as required by Books00-01, do not authorize replacing
one of these entropies by another or identifying any of them
with compulsory Book03 Info.

### Substitute into the existing full-price equation

For the DECLARED fine-CQ information component
I_fine=H_fine/log(phi), equations (16),(20) give

    D_chi(C_port,n-I_fine)
      = [2 a_(h,n) mean(chi)/log(phi)]
          sigma^2 log(sigma^2) + O_(h,n,chi)(sigma^2).          (21)

For nonnegative nonzero chi this is nonzero for all sufficiently
small positive sigma. The exact configured Einstein-CAR material
source is zero there. Equation (17), under this information
interpretation, now has a computed second operand: the actual
remaining ledger would have to satisfy

    D_chi C_remaining
      = -[2 a_(h,n) mean(chi)/log(phi)]
           sigma^2 log(sigma^2) + O_(h,n,chi)(sigma^2).         (22)

The exact requirement is D_chi C_remaining =
D_chi I_fine-D_chi C_port,n; the bounded remainder in (22) must
not be mistaken for a known missing analytic price coefficient.
A fixed finite inventory of real-analytic native charges has an
analytic expected source across this dark seed and cannot supply
the nonzero logarithm in (22). A genuine nonanalytic information
valuation, changing stopping programme or different actual
preparation is not excluded. Their complete source must be derived
from that execution, not assigned from (22).

This also applies the new spatial Gibbs identity82b to its actual
primary input. At fixed h,n, the original full spatial H+J+R,
port cost, energy defect and heat reference are smooth analytic
functions on this strict chart. Since that reference is faithful,

    D(Gamma_n || tau_sp)
      = -H_fine - S(rho_R) - Tr Gamma_n log(tau_sp).

The terms involving the product oldRIGHT cancel with the actual
input entropy as in82b. The material logarithm (21) is retained
in this relative-entropy operand; cancelling the recycling sum,
or bounding the stopped-log/Rayleigh difference, does NOT cancel it.
The spatial source identity therefore does not yet identify the
fine-CQ price with the original spatial master action.

For the separately owned amplitude-Born plus expected-Shannon
Bellman binding, the mean remains C-H_phi and the negative
Bellman root potential is -f_2=C-3H_phi/2=-log_phi(Z_2)/2.
The squared-norm partition pressure -log_phi(Z_2) is twice this
quantity; the literal sum of positive amplitudes is a different
partition and is not used here. Thus (20) also fixes their nonzero
half-entropy source difference on this same preparation.
Those two binding premises and the absolute Book anchor remain
explicit; no likelihood, amplitude pressure or coherent whole-state
information is silently substituted for fine-CQ information.

**Parent route change.** The complete fine-record operand in (17)
has now been evaluated analytically on the SAME primary material
direction for every fixed finite h,n. Its logarithm rules out an
automatic cancellation by the known analytic port price and finite
analytic completion. This removes the proposed fine-CQ shortcut to
source equality, while retaining the exact nonvacuum solution family,
the positive source constructions and all conditional universality
theorems. The remaining application is the actual Book valuation
and its same-initial preparation/constraint map, not another
Einstein witness or another entropy coefficient. No uniform
growing-horizon estimate, compulsory preparation, admitted field
writer, stationary solution, or physical GR/raw216 closure follows.

## 7b. Apply the owned preparation envelope before replacing the actual input

24 October 2026; input 71de007610429be2bdad2745879112e9f2232fb3.
The [whole-HJR fixed-collar owner](A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md#3-exact-preparation-section-on-the-whole-field-neighborhood)
already gives a genuine fixedRIGHT Riesz preparation and its exact
envelope source. It must be applied, not reproved or substituted for
(4) solely because both states retain RIGHT. The following application
uses the CURRENT isotropic inverse-coframe map (2),(11), the full
periodic native operator, and even L>=4. The transverse collar fixes
field variations; the actual shift matrices still wrap periodically.
No Dirichlet/masked replacement operator is used.

### A real rank128 stationary preparation exists on these fields

At the flat seed, in the unitary four-dimensional discrete Fourier basis,

    Delta_0(a) = lambda(a) I16,
    lambda(a) = 4 nu^2 h^-2 sum_r sin^2(pi a_r/L),
    lambda_1 = 4 nu^2 h^-2 sin^2(pi/L).                       (23)

The first nonzero shell consists of the eight momenta +/-e_r, with
all16 CAR grades, hence has rank128. Its gap to zero and every other
energy is at least lambda_1: two occupied coordinate components cost
at least 2lambda_1, and
sin^2(2pi/L)>=2sin^2(pi/L) for L>=4. The owned Riesz construction
therefore applies to every sufficiently small fixed-L perturbation
of the actual primary geometry. It supplies P_sigma of rank128,
rho_sigma=P_sigma/128 and a frame C_sigma with
C_sigma^dagger C_sigma=I128/128.

This is a positive application of the existing preparation theorem,
not application of the different certified v8 stationary-field base.
It establishes preparation stationarity on these prescribed fields,
not their geometric Euler equations or a uniform nonlinear radius.

Every proper exterior link and the actual positive observer pairing
preserves CAR parity. D is odd and Delta=D^2 is even; consequently
every whole-band spectral projector P_sigma is parity-even.
The required clock/scalar coherences rho_(0,1) and rho_(15,1) are
parity-odd and vanish on this Riesz branch. At the flat seed its
local density is I16/(16 L^4), rather than the rank-one four-grade
density of (4). Thus existence of this stationary preparation does
not give the required primary matter readout.

### The first material harmonic excludes ALL smooth Rayleigh-stationary lifts here

The [curved fixedRIGHT preparation owner](A4D_EXACT_CURVED_NATIVE_DIRAC_FIXED_RIGHT_PREPARATION_AND_SOURCE_2026_10_20.md)
already proves the full LEFT-unitary fixed-Gram criterion

    [rho,Delta]=0.                                           (24)

It is the preparation Euler of the DECLARED H+J+R when H,J are
preparation-independent and R=Tr(rho Delta). Indeed an arbitrary
LEFT anti-Hermitian generator K preserves the complete RIGHT Gram,
delta rho=[K,rho], and delta R=Tr([rho,Delta]K). This is not an
Euler equation of bare Book03 H+J, nor of a full Cost-Info functional
with additional preparation dependence. Restricted physically
admitted preparation tangents also require their own Euler condition.

Let rho_sigma be ANY C1 family of reduced densities satisfying
(24) on the small-amplitude geometry of section5. No particular
rank, fixed spectrum, factorized site lift or local purity is needed
for the next implication. Since that geometry changes by O(sigma^2),

    Delta_sigma=Delta_0+O(sigma^2),
    [rho_1,Delta_0]=0,     rho_1=partial_sigma rho_sigma|_0.   (25)

Here x and a are integer site/momentum indices modulo L; the
physical u-coordinate is h u_x. Normalize the local CAR density
as r_rho(x)=L^4 <x|rho|x>.
For q=(1,0,0,0), its Fourier coefficient is exactly

    rhat_rho(q)=L^-4 sum_x exp(-2pi i u_x/L) r_rho(x)
              =sum_a rhohat(a,a-q).

Every contributing block of rho_1 in (25) requires equal energies.
But on the actual symbol (23),

    lambda(a)-lambda(a-q)
       =4 nu^2 h^-2 sin(pi/L) sin(pi(2a_u-1)/L).              (26)

For even L this never vanishes, since 2a_u-1 cannot be divisible
by L. Hence rhat_rho_1(q)=0 as an entire CAR16 matrix.

The primary section (3),(4), in contrast, requires

    partial_sigma [rhat(q)]_(0,1)|_0 = sqrt(p) r_h/2,
    partial_sigma [rhat(q)]_(15,1)|_0 = sqrt(p) r_h/(2i).      (27)

These are already-owned linear density readings, not an extra
purity axiom on mixed preparations. For example the first coefficient
is the expectation of the finite norm-one diagnostic operator

    O_q=sum_x exp(-2pi i u_x/L)|x><x| tensor |1><0|.

Its Hermitian real/imaginary parts contract the same local readouts;
no free physical Fourier measurement/compiler is thereby assumed.
Equation (27) is nonzero and tends to sqrt(p)/2 in the first row
as h tends to zero. The mismatch is not a vanishing per-site
L^-4 artifact.

Therefore no C1 Rayleigh-preparation-stationary family on this
even periodic carrier has the required primary first material
readout. This strengthens the application beyond the old
factorized-lift obstruction: merely choosing another stationary
purification or a polarized eigenspace cannot supply this particular
first harmonic. The conclusion also prevents C1 convergence of
these normalized readout jets along even-mesh refinement; it does
not prevent singular/nonuniform-derivative limits or value-only
convergence.

There is no contradiction with the existing polarized equal-energy
preparations in the full-source owner, sections6.68-6.69 and6.82:
their k versus -k coherences have different harmonics (including
2k), and are not the q=e_u first harmonic of (27). Odd L, changed
spin/boundary operators, different physical readings or an additional
actual preparation-price source remain outside this application.

### Consume the causal constraint at its actual scope

The surviving owned mechanism is
[causal boundary completion](sources/d0_native_gr_completion_synthesis_2026-10-20/causal_boundary_completion.md):
X_0=iM and X_(j+1)=V_j(y)X_j with every clock/work/output retained.
For its supplied history price
J=sum_j Tr(X_j^dagger O_j X_j)+W, the backward adjoint removes
independent Euler rows of GENERATED intermediate X_j. Its remaining
field source includes every dO_j, dV_j, di and dW. For a nonquadratic
actual price the same elimination uses that price's actual state
gradient; it does not assign an Info law.

Thus (24) must NOT be imposed separately on every executed prefix.
An independently selectable initial M still has its genuine source.
In the current comparison (4), the values indexed by site-u are
part of the initial DATA preparation; they have not been identified
with those generated X_j. The literal proper-Lorentz transport alone
cannot supply the identification: exterior degrees0 and4 transform
by 1 and det(U)=1, so it leaves the scalar/top coefficients constant.
The native clock starts at its specified initial stage; imposing a
new cyclic invariant history state would add a boundary condition.

**Parent substitution and route change.** The existing stationary
preparation construction has now been applied to the actual primary
operator. A legitimate rank128 branch exists, but its matter
readings fail; (25)-(27) exclude the whole smooth Rayleigh-stationary
replacement class at the required first harmonic. Consequently
the same-primary argument must use an actually derived additional
price/preparation source, or the existing causal constraint with
a proved clock-conditioned matter map and its full source. Neither
a free Gibbs input nor another Riesz/Schur theorem supplies that map.
The exact primary all42 solutions, separate whole-HJR curved roots
and their original proofs are unchanged. No physical D0 no-go,
new constraint, whole-action GR equality or goal closure is asserted.

## 7c. Generate the original pure matter section with the existing native words

24 October 2026; input 2df9eeecf5ecd4f1d423199f91270604d3bd4146.
This consumes the addressed Golden/recording palette of
[A4D_NATIVE_GOLDEN_HISTORY_PREPARATION](A4D_NATIVE_GOLDEN_HISTORY_PREPARATION.md)
and the equal-inventory cells of
[A4D_PAID_GOLDEN_WORD_QUERY_SOURCE_LIMIT](A4D_PAID_GOLDEN_WORD_QUERY_SOURCE_LIMIT_2026_10_21.md#2-equal-cost-forward-cells-including-every-controller-complement).
It supplies a concrete missing map in section7b: a coherent preparation
of the ORIGINAL pure four-grade matter section, including its full
site/RIGHT lift and material-control comparisons. The prior paid moment
writer instead realizes specified moments with a generally mixed active
CAR state; it cannot silently substitute for this preparation.

The result is exact on a dense set of finite programme settings and
approximates any prescribed finite matter section to arbitrary accuracy.
It is not an exact finite-word compiler for arbitrary real amplitudes.
The physical admission and pricing of the inherited addressed palette,
fixed basis inputs and known-one resource remain its original hypotheses.

### One all-column identity supplies every required local rotation

Write G=exp(theta Y), Y=|1><0|-|0><1|,
cos(theta)=sqrt(p), sin(theta)=p. On n>=2 binary registers let
X^a|z>=|z+a> and Z^b|z>=(-1)^(b.z)|z>, with bit addition modulo2.
For any nonzero a put H_a={b:b.a=1} and K=2^(n-1). Then

    W_b=X^a Z^b,       W_b^2=-I,
    [W_b,W_c]=0       (b,c in H_a),
    sum_(b in H_a) W_b=K (|a><0|-|0><a|).                 (28)

These are algebraic names for the proof, not newly admitted Pauli gates.
For the sum, the character sum over H_a is K at z=0, -K at
z=a, and zero at every other basis input. The commutation follows
because both b.a and c.a equal1.

Choose a reversible binary linear map M with M e0=a, expressed as a
finite CNOT word of length l_M. Such an M is obtained by extending a
to a binary basis and elementary row operations; swaps use three CNOT.
For each b set v=M^T b-e0, so v0=0, and use the actual CNOT word

    N_v=I+e0 v^T=product_(j>0, v_j=1) CX(j -> 0),
    Q_b=M N_v.

Since N_v^2=I, Q_b e0=a and Q_b^(-T)e0=b. Thus

    Q_b G_0^m Q_b^dagger=exp(m theta W_b),
    D_(a,m):=product_(b in H_a) Q_b G_0^m Q_b^dagger
             =exp(K m theta J_(0,a)),
    J_(0,a)=|a><0|-|0><a|.                                (29)

Every one of the other 2^n-2 basis columns is fixed exactly.
All factors use forward G and CNOT; the inverse of a CNOT word is
its reversed word. For m>=1 the literal inventory is

    K m Golden gates + K(2 l_M+n-1) CNOT.                 (30)

Indeed b -> v is a bijection onto the vectors v0=0, whose total
Hamming weight is (n-1)2^(n-2). This is a finite, potentially very
expensive construction, not an efficient or compulsory compiler.

Conjugating by X^x gives the plane (x,x+a). Implement each bit of
X^x by CNOT from the EXISTING paid known-one c, adding 2|x| CNOT.
On the actual c=1 input the rotation is precisely J_(x,x+a).
The c=0 block is the UNTRANSLATED rotation J_(0,a), not identity.
It remains part of the full unitary and any whole-operator Book price.

The owned irrational-angle proof applies without change:
2cos(2theta)=2sqrt(5)-4 has a conjugate below -2, so theta/pi
is irrational. Consequently the positive angles K m theta are
dense modulo2pi for every fixed finite n. Equations(28)-(30) prove
the needed native pair rotation, rather than assuming controlled-G,
a new arbitrary-angle gate or an unpriced address multiplexer.

For n=4,a=15 one may take M=CX(0->1)CX(0->2)CX(0->3).
This gives exactly 8m G+72 CNOT for the (0,15) plane. In
particular it fixes the clock |1> and normalization |14> columns.
Unlike proper exterior Lorentz transport, this actual Golden word
can rotate the scalar/top pair.

### A coherent generator for the whole original material chart

Prepare the fixed CAR seed

    m_seed=sqrt(p)|1>+p|14>.                              (31)

From the existing paid blank |0> this is one G on bit0, the three
fan-out CNOTs above, then CX(c->bit0) on the paid c=1 sector.
The whole c=0 complement is retained. Preparation of the blank,
known-one, address and RIGHT seed is not declared free or derived here.

Embed the finite physical site set in r address bits and apply (29)
with n=r+4 to the TWO pairs at each actual site x:

    (x,14) -> (x,0) by angle alpha_x,
    (x,14) -> (x,15) by angle beta_x, in this order.

On c=1, each pair construction fixes every other address/CAR basis vector,
including unused address labels. Any binary address padding remains in
the complete physical carrier and price. Their product therefore implements
a genuinely coherent address-diagonal unitary, with no measured
address selection. On c=1 its output at x is exactly

    m_x(alpha,beta)=sqrt(p)|1>
       +p sin(alpha_x)|0>
       +p cos(alpha_x)sin(beta_x)|15>
       +p cos(alpha_x)cos(beta_x)|14>.                    (32)

For psi_0,x^2+psi_4,x^2<p^2, the original positive-grade14 section
has the regular coordinate map

    alpha_x=arcsin(psi_0,x/p),
    beta_x=arcsin(psi_4,x/sqrt(p^2-psi_0,x^2)).            (33)

The material Jacobian determinant is
p^2 cos(alpha_x)^2 cos(beta_x)>0. Thus two control angles cover
both original material directions at every free site, including
compact material variations with the field collar held fixed.
This is more than matching one sinusoidal trajectory or one moment.

For any ACTUAL supplied address/RIGHT seed with coefficients chi_x,
the complete map is

    C_seed=sum_x |x> m_seed chi_x^dagger
      -> C(alpha,beta)=sum_x |x> m_x(alpha,beta) chi_x^dagger.  (34)

It preserves C^dagger C exactly and transports every off-diagonal
site block by U_x rho_xy U_y^dagger. Those coherences are retained
and transformed, not measured away or asserted numerically unchanged.
It applies both to the counting-site input(4) and to the different
fixedRIGHT128 lift at their respective supplied chi_x. It does NOT
identify those two input states, construct a free uniform counting
seed, or prove their native initial preparation.

Equations(32)-(34) hold literally for all compiled angle settings;
density gives arbitrary finite-section accuracy. In particular the
primary psi=(sigma r_h cos(ku),sigma r_h sin(ku)) lies in this
chart for small sigma. Its approximate preparations need only this
native pair construction, not a supplied continuously tunable matter
gate. The complete finite input error is controlled by the maximum
per-site angle error: the two rotations are norm-Lipschitz, hence
||C_tilde-C||_HS <= (eta_alpha+eta_beta)||C_seed||_HS.
This bound includes the real RIGHT lift.

A more economical sequential word (29) with n=4 generates
sqrt(p)|1>+c cos(j delta)|0>+c sin(j delta)|15>+d|14>
at native delta=8m theta, from its actual generated first state.
It is useful inside the stage-clock executor, but does not identify
its execution-stage index with the primary null coordinate u.
Indeed the existing all40 proof makes the scalar Euler vanish for
ANY u-profile by v-Stokes; it does not select this waveform.
The timelike Cauchy owner assumes g^{00}>0, whereas this chart has
g^{uu}=0. Neither Cauchy evolution nor a cyclic-history boundary is
being inserted by calling the address u a clock.

### Material source comparisons use paid programmes, not derivatives of one fixed word

Replace every G^k slot in (29) by the owned equal-inventory echo
cell W_(N,k), with N,k of the SAME parity and |k|<=N. This is the identical
cell-count formula; even N,k additionally allow the exact vacuum
center k=0. It uses N forward G and
2N CNOT at the same addresses and has full operator

    |0><0|_c tensor G^N + |1><1|_c tensor G^k.

After the pair translation the complete plane compiler is

    |0><0|_c tensor exp(K N theta J_(0,a))
    +|1><1|_c tensor exp(K k theta J_(x,x+a)).             (35)

Its literal inventory is

    K N G + [2KN+K(2 l_M+n-1)+2|x|] CNOT.                (36)

Every controller column is present. A common N of the chosen parity covers any finite
catalogue of centers and stencil endpoints on the fixed finite mesh.
The c=0 block, full duration and additive per-address inventory are
then the SAME across those settings. There is no uncharged inverse
or omitted compiler clock.

Let Q_j be integer returns with
epsilon_j=2K Q_j theta-2pi l_j ->0, epsilon_j !=0.
For a center k_j of that parity, the exponents k_j+/-2Q_j give precisely the
two neighboring angles alpha_j+/-epsilon_j. Density permits centers
alpha_j approaching any target alpha, and a common N_j pays every
required endpoint. The same construction is used independently in
all free alpha_x,beta_x slots. Prepared-state secants converge to the full
material derivative through (33),(34). They are not the ordinary
derivative of a fixed finite word or of nearest-programme rounding.

The prepared-state statement uses the actual c=1 input. The c=0
block is fixed across settings at one resolution but may change when
N changes; it is not thereby negligible in the Book functional.
No full-operator heat/source limit follows from material accuracy.

For an actually fixed finite downstream execution whose ENTIRE price
is a C1 function of these prepared states, the price secants converge
to its true material covector as well. For the finite complete CQ tree,
q log q=||X||^2 log||X||^2 is C1 even at a born-zero leaf, so this
statement includes all outcomes without a probability floor. The
inherited deterministic additive preparation charge is common at each
resolution and cancels in its secant, while every downstream charge
and probability remains. This uses one fixed downstream price function,
not an uncontrolled sequence of changing whole Book valuations. It
asserts no uniform second-derivative bound at the dark seed.
On a controlled C3 chart, central error is O(epsilon_j^2), plus
the error from the approximated center. The physical field-source
norm must also include the actual inverse Jacobian of (33), true
spatial weights, source gain and the downstream pullback norm.

Here equal inventories make only the INHERITED additive fixed
primitive ledger constant. They do not make minimal programme
description, whole Book heat, a moving initial preparation,
order-dependent work or an arbitrary stopping price constant.
Different endpoints are different deterministic programmes with
their retained actual codes; a mixture or coherent superposition
of code settings requires its own complete price. There is no
physical same-initial programme selector asserted in (35).

### The same-source adjoint makes the gain and the remaining obstruction explicit

Consume the already proved
[N1 constrained causal completion](sources/d0_same_execution_spatial_source_2026-10-21/execution/N1_CONSTRAINED_CAUSAL_COMPLETION.md),
rather than adding free preparation Euler equations.
For the actual full finite CQ tree, X_w=K_e X_v, with all charges
already included once in C_omega, it gives

    P_omega=[C_omega+(ln p_omega+1)/ln(phi)]X_omega,
    P_v=sum_(e:v->w) K_e^dagger P_w,
    DS=sum_omega p_omega DC_omega
       +2 Re sum_(e:v->w)<P_w,(DK_e)X_v>
       +2 Re<P_root,DX_root>.                            (37)

The zero-amplitude entropy gradient is its continuous zero limit.
Generated material states (32) are among the internal X_v; their
independent Rayleigh Euler is not imposed. Every actual preparation
gate/control derivative remains in (37), together with the genuine
initial boundary. A programme spanning a previously free preparation
direction still has that source through its control; generating its
state does not solve the corresponding stationarity equation. On
finite native programme grids, (37) is the
limiting secant covector just described, not a fictitious derivative
of a countable processor.

This is a positive substitution for the pure-material preparation
oracle on the inherited addressed interface. It does NOT repair
section7a's full-price mismatch simply by moving the preparation
inside the apparatus. If the same pure counting-site input is
prepared, its subsequent full128 fine-record probabilities are the
same; deterministic retained preparation does not erase their entropy.
For the actual analytic material extension its logarithmic source
in (20)-(22) is pulled back through (33) and (37). At fixed positive
sigma the native secants recover that source; no uniform
sigma->0/precision interchange is claimed. Actual extra measured
preparation histories or a different valuation add their real source,
rather than a subtraction chosen to cancel the logarithm.

Likewise, the existing N1 identity DS=gamma_1 DJ2+D B applies only
after its actual query/preparation/baseline map has been identified.
The current material compiler neither equates the original full128
suffix with that different N1 detector nor proves D B=0 for Book03.

The original operational books do provide a DIRECT variational route:
Book00's admissible subfunctor includes gate stationarity, and
Book03 sections03.8 and03.25 state finite/master stationarity.
It need not be inferred anew from reversible computation or Shannon
entropy. Book01 F0=|D_min|, its subadditive pairing rule and the
internal trace F=(QUP)^dagger QUP remain the owned definitions;
they do not identify the whole executed price with gate count.
The remaining physical substitution is the original master/Cost-Info
functional and admissible controls of THIS complete execution,
including the unshifted controller blocks in (35), initial
address/RIGHT preparation, actual clock and every independent
upstream source. No new selection principle, independent task,
certificate catalogue, native minimum or physical GR closure follows.

## 7d. Apply the generated matter to the full primitive Book master

24 October 2026; input ebc7c9a312d14bbd381006c971267bad5761db74.
This consumes section7c and the already proved
[complete clock and return maps, sections13.3,14.4,19](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#19-direct-book03-stationarity-the-actual-all-n-primitive-programme-and-two-different-memory-boundaries).
The changed input is the ORIGINAL pure material preparation, with its
whole controller complement, on the CORRECT physical inverse-coframe
map(2),(11),(23). Neither the old shrinking-leg box nor the different
local CAR fixture of that owner's section19.4 is used.

Book00 gate stationarity and Book03's direct master are legitimate
owned inputs. Their application still requires the actual operator,
cut, clock and admissible variations. Here the declared price sector
is precisely H+J on the owned homogeneous 33-scene primitive clock.
It is not the spatial stopped heat or the complete independently
supplied Book stack. Upstream seed/known-one/address/RIGHT preparation
and any additional stack sources are retained as separate obligations.

### The original return is exactly invariant under this material prefix

Write R_theta for the complete address/CAR/controller compiler(35),
and V_n(g)=(C_n U_n)...(C_1 U_1) for the original copied full128 body.
R_theta preserves c and touches none of its fresh Apps or banks.
Use the actual protected support

    P0=I_DATA,oldRIGHT tensor P_blank Apps,banks tensor P_C,

with any genuine spectator/scene factors counted once. P_C may
protect the c=1 sector or both sectors, with actual rank r_C=1 or2.
Then [R_theta,P0]=0 on ALL columns, so for M_theta=V_n R_theta,

    F(M_theta,P0)=R_theta^dagger F(V_n,P0) R_theta.          (38)

This follows directly from F(M,P)=P M^dagger(I-P) M P.
No inverse preparation is executed, no prepared probability replaces
the operator, and no c=0 column is discarded. Consequently the full
return determinant is exactly independent of theta, at every finite
mesh and round number:

    J_n(g,theta)=-kappa Tr_DATA log[(1-z)I+z B(g)^(2n)],
    B(g)=I-alpha_h Delta_DATA(g), alpha_h=p^2 h^2/128.       (39)

Here kappa is the REAL protected scene/RIGHT/controller/bank
multiplicity. For blank banks it is r_S d_R r_C; a wider protected
bank support has its actual additional factor. DATA includes all
physical sites and CAR16. Unused address labels, if needed, are
retained as the actual padded identity extension. They do not add
a field derivative to(39), but remain in the whole heat.

Use the actual primitive expansion of M_theta and its counted final
idle, of total length N. On the already owned coherent transported
cut P_t=Q_t P0 Q_t^dagger, every interior leakage block vanishes.
The single idle wrap is unitarily equivalent to(38). Thus (39) is
also the ONE-step Book feedback on that full stage cut; there is
no extra factor N. This invokes, rather than selects, that cut.
Primitive admission of the original moving full128 gates is not
proved by their supplied matrix formula.

### Whole-clock source estimates include the compiler complement

At a fixed common catalogue in(35), the actual N, all fibre ranks
and the c=0 operator are common to its settings. The complete
33-scene heat is a function H_N(M) of the full unitary monodromy.
Its owned Fourier coefficients satisfy

    c_l>=0, c_l<=33 exp(12 beta/13) I_l(beta/11),
    C1(N)=2 exp(beta)/(33 beta) sum_(q>=1) q c_(qN).         (40)

For ANY two full unitaries on that same fibre and clock,

    |H_N(M_+)-H_N(M_-)|
          <=C1(N)||M_+-M_-||_op,
    |D H_N(M)[dot M]|<=C1(N)||dot M||_op.                 (41)

For completeness the endpoint estimate uses the original whole trace
Z_N=N exp(-beta)[D c0+2 sum c_(qN) Re Tr(M^q)].
Telescoping gives |Tr(M_+^q-M_-^q)|<=D q||M_+-M_-||.
The owned lower bound Z_N>=33 N D exp(-2beta) and
|log a-log b|<=|a-b|/min(a,b) give(41). The real D cancels
in this inequality; no trace mode was deleted or normalized away.

At beta=2p^2 the existing Bessel estimate gives

    C1(N)<64 22^(-N)/N!,     C1(N)->0.                    (42)

This estimate applies to the actual compiler length, not an unpaid
waiting interval. At fixed finite h,n the common catalogues can
have N_j->infinity as their source precision improves. That is a
property of this implementation sequence, not a selected physical
horizon, an efficiency claim or an allowed change of a prescribed
stopping task.

For two settings in ONE such catalogue, equations(38)-(41) imply

    |(mathcal B_+-mathcal B_-)/(2 delta)|
       <= C1(N) ||(R_+-R_-)/(2 delta)||_op,
    mathcal B=H_N(V_n R)+J_n.                             (43)

The c=0 block cancels EXACTLY in the full operator secant. On c=1,
R is the address-diagonal product of the two rotations in(32).
Hence on a compact interior of the material disk,

    ||D_psi R[v]||_op
       <= max_x (|D alpha_x[v]|+|D beta_x[v]|).             (44)

The inverse Jacobian(33), actual field norm and any source gain
remain in this bound. Applying(43) to the actual angle secants of
section7c proves suppression of the material source by C1(N_j).
It does not take a derivative of one fixed discrete native word.
Across different j the c=0 block may change; (41) holds uniformly
over those blocks and does not assume they converge.

There is also a useful whole geometric-covector comparison. At
fixed g, for two material compilers R_a,R_b independent of the
geometric tangent, let A_h,n=||D_g V_n|| in its actual lifted norm.
Their feedback covectors are identical by(39), and(41) gives

    ||D_g mathcal B(g,R_a)-D_g mathcal B(g,R_b)||
                         <=2 C1(N) A_h,n.                (45)

This is a finite comparison of complete geometric covectors, not
a mixed material derivative without its step denominator. In a
gain-normalized claim every right-hand side must be divided by
the actual nonzero gain; no lower bound on that gain is presumed.
By contrast, the original scalar action has a real off-shell
backreaction: on the primary metric a compact delta g^(uu)=chi
gives D_g sum q[chi]=sum chi |D_u^+Psi|^2. Two material sections
that agree on the collar and differ on this interior stencil can
therefore have different geometric sources. The unnormalized
decay in(45) cannot silently supply that nonzero source map.

### A decisive flat-field row on the correct physical carrier

The source test can be made pointwise, without a gain or an
off-shell source-map assumption. Take the exact vacuum material
center k=0 allowed by the even catalogues in section7c. The c=1
preparation is then exactly the constant m_seed, even while its
full c=0 complement and real compiler duration remain.

At the flat physical coframe vary E_s=s^-1 E_0, holding
nu=3/5, h, p, n, beta and z fixed. This is a geometric variation:
the inverse legs scale by s, hence D_s=s D_0 and
Delta_s=s^2 Delta_0. The calibration alpha_h is FIXED.
Put B=I-alpha_h Delta_0 and M=(1-z)I+z B^(2n).
Exact differentiation of(39) gives

    dJ_n/ds|_1
      =4 kappa n z alpha_h Tr[M^-1 B^(2n-1) Delta_0]>0.    (46)

For the actual symbol(23),
alpha_h lambda_max<=p^2 nu^2/8<1/50, so B>49/50.
All factors in(46) are commuting positive operators; exact dark
modes contribute zero and the nonzero Fourier modes give strict
positivity. There is no small-gap or inverse-Dirac assumption.

The full CAR16 trace is

    Tr Delta_0=128 nu^2 L^6,
    alpha_h Tr Delta_0=p^2 nu^2 L^4.                      (47)

The flat original V_n and P0 are translation covariant. Therefore
the single-site inverse-leg radial row of J_n is exactly the
global row(46) divided by L^4. Since M<=I and
4p^2 nu^2>27/50>1/2, each such row obeys

    D_x J_n > (kappa n z/2) (49/50)^(2n-1)>0.             (48)

Choose x in the free interior bounded by the fixed field collar,
with its local variation supported there. This is an allowed ambient source
test of the supplied field chart, not an assumption of physical
continuous control admission.

The compiler need NOT be translation invariant on all columns.
Do not divide its global heat derivative by L^4. Instead apply
(41) directly to this SAME local tangent. Since D_x R_j=0,

    |D_x H_(N_j)(V_n R_j)|
          <=C1(N_j)||D_x V_n||_op ->0.                   (49)

The finite full-column norm on the right is fixed in j. Equations
(48)-(49) prove D_x mathcal B>0 for all sufficiently fine compiler
catalogues at fixed h,n. The configured Palatini-plus-scalar action
has every field row zero at this flat, constant-matter seed.

Thus prefixing the pure material compiler to the original copied
word, with this declared transported cut and 33-scene master,
does not produce even the required flat stationary point in this
implementation limit. This correct physical-carrier application
does not revive the invalid shrinking-leg application, claim a
sign for every finite compiler, or exclude other Book realizations,
genuine constraints or additional actual stack sources.

### Preserve the positive return-query route and its internal matter reading

The [existing positive construction, sections9-10](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#9-forward-native-words-supply-the-owned-coherent-return-query-source)
already realizes the complete declared H+J source with explicit
forward words, paid approximate global inverses, all clock modes,
the original source gain and all42 covector errors. It is a
DIFFERENT execution/cut, not the source-free material prefix(38).

Its ideal comparison word is U_k=V_k^dagger M V_k, with M the
fixed READY/report-controlled meter word. Add a section7c compiler
Q_k on an actual additional CAR seed, using disjoint material
registers or shared address/control registers ONLY after verifying
[Q_k,M]=0. Then with V'_k=Q_k V_k,

    V'_k^dagger M V'_k=V_k^dagger M V_k                   (50)

on every column of the enlarged carrier. The real new seed/cut
and spectator ranks must be included. A fixed added pure CAR seed
does not itself multiply the protected rank; identity-protected
extra factors do. This does not replace a supplied entangled
address/RIGHT seed by a fictitious product state.

The existing all-column forward-inverse construction applies to
V'_k with its ACTUAL increased G/CX counts. It approximates(50)
with the same telescoping error rule and recomputed actual length,
gain and source-error budget. The c=1 identity XGX=G^dagger is not
a global inverse on the other controller columns. The whole heat
comparison remains conjugate to the fixed middle spectrum at a
fixed new N; its absolute value, physical duration and paid seed
are retained.

At the real forward checkpoint t* after Q_k, let i0 be the actual
initial isometry and T_t* the actual prefix. The map
J_t*=|t*> tensor T_t* i0 satisfies J_t*^dagger J_t*=I.
For any supplied actual matter diagnostic O at that stage,

    J_t*^dagger (|t*><t*| tensor O) J_t*
                     =i0^dagger T_t*^dagger O T_t* i0.    (51)

This is the existing causal execution at one REAL clock stage,
not an added cyclic invariant state or a superposition of all
histories. When its incoming address/RIGHT seed is(34), it gives
the original pure material readings with all coherences retained.
Later uncomputation does not invalidate the earlier internal
reading. The existing GR source consumer asks for the SAME
field/clock/weight/matter map, not permanent final-output matter.

The SAME matter dictionary is explicit. The existing
[fixed-processor material map, section4](A4D_FIXED_PROCESSOR_JOINT_RESOURCE_SOURCE_2026_10_21.md#4-от-общей-вариации-к-каждой-независимой-копии)
reads, on the supplied fixed c=1 input of section7c and an actual
uniform site mass 1/S,

    Psi_(x,A)(rho)=S/(2 sqrt(p)) Tr rho
        (|x,1><x,A|+|x,A><x,1|),  A=0,15.                (52)

On the pure checkpoint(32) it is exactly psi_(A,x), the SAME
coordinate consumed by the existing moment reporter. For a
nonuniform actual site mass w_x the factor is instead
1/(2 sqrt(p) w_x), with every genuine weight derivative retained;
a nonexistent uniform seed is not inserted. Before Q the required
factorization is only sum_x |x> m_seed tensor xi_x: xi_x may contain
all report work and oldRIGHT. If the borrowed control instead is the raw READY parity of V_k,
include P_(c=1) in the numerator and use the actual joint mass
w_(x,c=1)>0 in the denominator. Its failed c=0 branches remain
in the full price; this conditional readout does not remove them.
No product between address and RIGHT
or between the whole Q and V is needed. On c=1 the local rotations
therefore produce sum_x |x> m_x tensor xi_x exactly. The two pair
differences have zero address component; their c=0 completions
also preserve address labels, although every micro-gate and all
address coherences remain in the real execution.

At a common source catalogue choose Q_k for the SAME material
coordinate psi(c_k) used by V_k. If eta_j is the maximum actual
readout error at its center and endpoints, choose the finite
native angle accuracy so eta_j/delta_j->0. The readout secants
then approach the same material-coordinate differential; combine
this with the existing full-price bound(41) of paidwriter section10,
its actual gain and pullback norm. Continuity of the finite
Palatini/scalar source on the fixed compact chart transports the
covector to these approaching physical readings. The real
mesh-dependent constants remain in a refinement claim. This
constructs a commuting SOURCE-LIMIT dictionary, not an exact
finite continuous actuator or a finite native stationary root.

Direct interaction of the reporter with this additional pure CAR
is not an extra hypothesis of the all42 source consumer. Generated
moment copies and the pure checkpoint can interpret the same
field when(52), the common key and the complete pulled-back price
are verified. Conversely, this does not identify the old full128
instrument's input with an unrelated copy. Actual independently
variable codes/resources still require their own equations; the
linked catalogue does not prove the physical constraint linking them.

Equation(51) makes no diagnostic an admitted unpaid measurement.
Actual subsequent tests keep their operations and full price.
The existing future-profile identity transports a later test w
from Q seed to the PAID prefix Q;w at seed. It does not equate
their original future classes, which also include the empty test.
The checkpoint stage projector is a clock-conditioned READOUT,
not a selection of the physical active Book projector P_N.

**Parent application.** The original bare-master prefix route is
now tested on the current physical metric, with every controller
column and primitive-clock source retained. The positive full-Book
return-query route survives and admits an explicit internal
pure-matter checkpoint; an artificial requirement of terminal
matter persistence is unnecessary. Neither result selects the
active cut, initial task, controller, full stack or physical
field variation from Book00-01. The next substitution is their
same-execution selection/transport and actual source application,
not another generic compiler, heat estimate or geometric root.
The exact nonvacuum family and conditional global GR consumers
retain their original assumptions. No physical GR closure or
scientific-status promotion is asserted.

## 7e. Original initialized port and arbitrary Q8 spin: one complete source word

24 October 2026. Native-realization application of section7d, the
[positive paid-writer sections9-10](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#9-forward-native-words-supply-the-owned-coherent-return-query-source)
and [Book03 section03.26.1](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#03261-forward-only-order-comparison-with-an-internal-stage-register),
at input publication 26968f5154e4f91df9050bede73f387a0f3f8325.
The existing writer used an arbitrary two-state meter input. The
original detector instead supplies a KNOWN port0 and an arbitrary
real Q8 spin v. The following actual word realizes the same all42
source consumer on THAT input family. It keeps the inherited active
work/port G/CX placement and genuine blank preparation assumptions;
it does not infer physical Book cut or task selection.

### The native input changes the required middle word

Keep the original native embedding and all genuine fresh work:

    i_native(v)=|0_W,port0> tensor v,  v in R4.           (54)

An untouched past factor is included only when actually present.
The original calibrated detector record can be one of these fresh
blanks; no archived record is reset. The Q8 spin is untouched by
EVERY primitive operation below, so arbitrary spin and past
entanglement is allowed. No addressable spin-bit operation or change
of the native compatible complex structure is assumed.

Let V_k be the existing full-column positive G/CX work writer,
Pi its fixed conjunction of K READY/report flags, m=2^(K-1), and

    x_k=<0_W|V_k^dagger Pi V_k|0_W>=gamma_h Q_h(c_k).

Simply restricting the old symmetric middle G^(-m) W_K to port0
would FAIL: its compressed amplitude is cos(m theta), independent
of x_k, hence its feedback source is zero. Here G=R(theta) is the
original Golden gate. Instead execute the ALREADY constructed
controlled word itself, with no leading G^(-m):

    M0=W_K=(I-Pi) tensor I_port+Pi tensor G_port^(2m),
    U_k=V_k^dagger M0 V_k.                              (55)

This is a change of the real programme, not an assigned F=f(x).
V acts on work and M0 on the original port. On the task's input
projector P=|0_W,port0><0_W,port0| tensor I_spin (and its actual
protected past), write r=rank(P). Then

    P U_k P=(1-d_K x_k)P,
    d_K=1-cos(2m theta),       0<d_K<2,
    F_k=[1-(1-d_K x_k)^2]P,
    j_K(x)=-r log[1-zeta+zeta(1-d_K x)^2].              (56)

These identities hold on the WHOLE input family. They follow by
taking the 00 port entry of I and G^(2m), then using F=P-A^dagger A.
Irrationality of theta/pi, already owned for G, gives the strict
bounds on d_K. On the bare clock with no protected past or scene
factor, r=4, not two. An actually protected scene projector of rank
r_S and past projector of rank r_p instead give r=4 r_S r_p; full
thermal scene dimension33 does not by itself set r_S. A fixed added
pure material seed does not multiply r; true protected identity
factors do. The four-real-coordinate trace is retained,
without halving it by a complex-coordinate renaming.

### All primitive costs, failed work and the new reference heat

The literal W_K has m positive and m negative G letters and
2^(K+1)-2 CX letters. Replace EVERY negative G in V_k^dagger and W_K
by the same positive G^q, with eta_q=||G^q-G^dagger||. The actual
forward word therefore has

    N_G=(1+q)(n_G,h+m),
    N_CX=2 n_CX,h+2^(K+1)-2,
    ||Uhat_k-U_k|| <= (n_G,h+m)eta_q=:epsilon_q.        (57)

All counts and flags are common to the finite field stencil.
If only the physical port supplies G, route each work G through it
by SWAP;G_port;SWAP. This needs SIX additional addressed work/port
CX calls per routed letter, on all columns even when the port is
not blank. Add 6 n_route to N_CX and use that TRUE primitive N.
When all work G letters are routed, n_route=(1+q)n_G,h. This does
not assume spin addressing; work/port addressing itself remains
the inherited physical admission premise.

Construct the actual clock shift and its transported cuts from
these expanded prefixes. The ideal monodromy U_k is conjugate to
the FIXED M0, so its full heat is field independent at common N.
It is NOT the old symmetric-middle reference heat. For example,
let D=dim(work), R=rank(Pi), and let D_past be the dimension of an
actual untouched whole past factor (one if absent). With the bare
clock character

    T_N(omega)=sum_(j=0)^(N-1)
      exp[-beta(1-cos((2pi j+omega)/N))],

the whole new ideal trace is exactly

    Z_ref=4 D_past {2(D-R)T_N(0)
              +R[T_N(2m theta)+T_N(-2m theta)]}.        (58)

Every failed/unprepared work column and native spin coordinate is
counted. For the declared homogeneous 33-scene times clock carrier,
replace each scalar clock character by its actual 33-mode character;
do not replace that scene or normalize its trace. The fixed ordinary
past dimension in (58) need not equal its protected rank in (56).
At a changed N evaluate (58) at that new N. A moving beta, rank or
clock comparison retains the corresponding absolute-price change.

The existing whole-clock norm bound and determinant bound give

    |B_actual-H_ref(N)-j_K(x_k)| <= C_B epsilon_q,
    C_B=1+2r zeta/(1-zeta).                            (59)

The spin identity factor cancels only between numerator and
denominator of the HEAT DERIVATIVE, not from the absolute heat.
All transported-prefix adjoints of paid-writer section10.5 apply
to this actual whole word. Generated work, flags and cuts therefore
need no separate free preparation Euler equation.

### The original Book contract already supplies the finite two-cell section

At the finite OPERATOR/TEST level the register placement is explicit.
Take one closed carrier

    H=R2_x tensor R2_y tensor R4_sA tensor R4_sB,
    i(v)=|0_x,0_y> tensor v,    v in R16.

Cell A has port x and record y; cell B has port y and record x.
The complete original matrices give G_x, G_y, CX_(x->y), CX_(y->x),
with the two real Q8 spins untouched. Both compatible spin complex
structures are preserved. Both initial blank conditions hold at t=0.
After an overlapping operation a record need not still be blank:
this constructs one full-column word, not two independently completed
fresh-record detector tasks. No old record is reset by a projection.

Consume the exact two-direction exchange of
[verified archive actuation section3](A4D_NATIVE_VERIFIED_ARCHIVE_ACTUATION.md#3-the-minimal-basis-implementation-is-the-existing-registration)
and the already proved
[Books00-01 section application](A4D_ORIGINAL_BOOK_BOOLEAN_TRACE_CLOCK_AND_GLOBAL_EINSTEIN_2026_10_22.md#132-books00-01-application-admissible-test-sections-and-an-actual-return-boundary).
For the supplied finite word and complete terminal projectors, the
owned Golden-cylinder extension preserves the whole channel and
positive outcome effects. This64-coordinate carrier starts at binary
stage6 and extends to its cofinal tower, not every coarser stage.
It therefore gives the six-condition finite operator/test section;
no new rotation proof, gate palette or unique microscopic task is
required merely for this representation.

The second detector spin is an ACTUAL retained factor: the bare
initialized input now has r=16, and its factor4 remains in the whole
heat trace. Use the resulting rank, inventory and reference heat in
(57)-(63); do not identify its normalized response with the old
absolute price. This is the two-cell realization of the register
interface, not a claim of minimum hardware.

This closes a missing matrix representation only at the declared
finite-section interface. It does not identify the section with an
already executed physical task or authorize reuse of both placements
in that task. Book00's physical phi self-return, actual active/archive
cut, full action, admitted field variations and stationarity remain
the application. In particular this cylinder tower is not spatial
h-refinement. A separate unexplained matrix-admission premise should
not be added on top of the original six-condition section contract.

### Substitute the new gain in the entire all42 source estimate

For 0<=x<=q_max<1/2, put b=1-zeta and a_min=1-2q_max.
The exact derivative is

    j_K'(x)=2r zeta d_K(1-d_K x)
             /[1-zeta+zeta(1-d_K x)^2] >0.            (60)

Consequently the original weak-query/polynomial source calculation
is unchanged after replacing its scalar j and gain by

    Gamma_K(y)=j_K'(gamma_h Q_h(y))
                 gamma_h a0 tau_h/Omega >0.           (61)

In particular the SAME full42 error estimate (41) applies with
Gamma_K, this programme's M3,B and (59). There is no D Gamma term:
the exact FIRST source is j_K'(x) gamma_h DQ_h. This is not a claim
of equality of the two old and new actions or Hessians.

The required accuracy ordering survives arbitrarily small gamma_h
AND d_K. Direct differentiation of (56) gives

    j_K' >= 2r zeta d_K a_min,
    |j_K^(s)| <= r zeta d_K L_s, s=1,2,3,
    L1=2/b,     L2=4/b^2,     L3=48 zeta/b^3.           (62)

For example j_K'''=4r zeta^2 d_K^3 a
[zeta a^2-3(1-zeta)]/[1-zeta+zeta a^2]^3, a=1-d_Kx.
With the existing pure-coordinate polynomial derivative bounds M_s,Q,
the chain rule therefore gives

    M3,B/inf Gamma_K <= Omega/(2 a0 tau_h a_min)
      [L1 M3,Q+3 L2 M1,Q M2,Q+L3 M1,Q^3].             (63)

Use gamma_h<=1 for the extra chain powers. Thus the catalogue can
still be chosen before inverse accuracy without an invented lower
bound on its READY probability or its d_K. The final inverse choice
uses the ACTUAL nonzero Gamma_K, actual pullback norm and stencil.
No finite native stationary root is inferred from a source limit.

The pure CAR compiler of section7d acts on registers disjoint from
the port and Q8 spin and satisfies its same full-column commutation:
because it commutes with G_port^(-m), commuting with the old middle
is equivalent to commuting with W_K. Its added work, real checkpoint
and common material dictionary therefore compose with (55)-(63).
The existing all42 primary roots and weak-query source-limit consumer
are reused, without a fresh metric root or an independent matter input.

**Parent substitution.** The source-bearing whole-Book return now
works with the original KNOWN port and arbitrary Q8-spin input.
This removes the extra unknown-meter calibration requirement and
the proposed spin-addressing detour. It does not prove that Book
selects the minimal projector onto this initialized input family,
admit its complete task/scene/action identification, or supply the
actual field-variation and stationary-refinement law. Independent
boundary variations require their own sources if the native task
allows them. GR_closed and raw216 remain open.

## 7f. One internally recorded return task, with its complete price and all42 source

24 October2026. Same native-realization owner, input publication
f81f5e5c969c757777ec7639d8cb9dc44a7652b7. This applies section7e to
an actual internal final-record operation and consumes the
[original Book task boundary](A4D_ORIGINAL_BOOK_BOOLEAN_TRACE_CLOCK_AND_GLOBAL_EINSTEIN_2026_10_22.md#132-books00-01-application-admissible-test-sections-and-an-actual-return-boundary),
its equation(48), and the ALREADY owned arbitrary-monodromy heat
estimate. A new heat theorem, a joint-return oracle, a free output
flag and a second independent matter input are unnecessary.

### The input/output intertwiner and the actual internal bank

Let A be the w COMPUTATIONAL-BLANK work/port bits of section7e,
and K the true protected spin/past/seed carrier. Keep the actual
fixed input projector

    P=|0_A><0_A| tensor P_K,       r=rank(P).

Unknown spin and oldRIGHT are not copied. A supplied noncomputational
seed is not relabelled as blank. Include a genuine fresh bank of
w blank bits in the COMPLETE INITIAL state, and execute the actual
full-column copy

    C_copy |a,k,b> = |a,k,b XOR a>.

It is the product of w addressed native CX operations, including
all dirty-bank columns; C_copy^2=I. For the existing actual positive
word Uhat and its ideal comparison U, the new complete word and cut are

    Urec=C_copy(Uhat tensor I_bank),
    Pnew=P tensor |0_bank><0_bank|.                    (64)

C_copy Pnew=Pnew=Pnew C_copy, so EXACTLY, without a limit,

    Pnew Urec Pnew=(P Uhat P) tensor |0_bank><0_bank|,
    F(Urec,Pnew)=F(Uhat,P) tensor |0_bank><0_bank|,
    J(Urec,Pnew)=J(Uhat,P),       rank(Pnew)=r.          (65)

The cut on the bank is blank, not identity. Its FULL thermal dimension,
in contrast, is multiplied by 2^w. All nonreturn/failure components
remain. This bank records the final complete computational label; it
does not recreate factory outcomes coherently uncomputed earlier.
Only basis labels are recorded: the operation retains coherences as
internal system-bank correlations, not as independent cloned states.

For a task whose other protected factors are invariant under Uhat,
let i be the calibrated input isometry with i^dagger i=I and
ii^dagger=Pnew, and let Pi_b project onto bank label b. Then

    Pi_0 Urec i=i(i^dagger Urec i),
    K_b=Pi_b Urec i,       sum_b K_b^dagger K_b=I.       (66)

Both return and nonreturn complete ONE task; Pi_done=I. The return
embedding and its native Gram are thus explicit. This is not two
independently completed detector tasks and does not use minimum
actual-state support. Section7e's ideal return is (1-d_K x)I; the
actual return is its exact compression, with its original error bound.
A moving genuine input projector or seed retains its own source.

### Every copy is paid; its new whole heat need not be field constant

With directly admitted addressed CX, Nrec=Nold+w and the new CX
count is N_CX,old+w; G counts are unchanged. Keep the already counted
idle once, at the final wrap. If physical routing is required, include
its real added stages and resources in Nrec. Rebuild ALL clock prefixes
and transported cuts. The fresh bank is not an external reservoir.
The inherited two-direction placement remains a constructed finite
section; this does not select its execution in a pre-existing task.

The old fixed-middle heat argument cannot be reused: Urec generally
has a different spectrum. Instead consume
[paidwriter section16.4, equation102](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#164-the-full-primitive-heat-cannot-cancel-that-contrast)
and section7d equations(40)-(42), which hold for ANY complete unitary
monodromy on the SAME fixed33-scene/fibre/clock. With the actual full
fibre dimension Drec, the full trace is

    Z_N(M)=N exp(-beta)[Drec c0
                 +2 sum_(l>=1) c_(lN) Re Tr(M^l)],
    H0(N,Drec)=beta^(-1) log[N exp(-beta)Drec c0].

Every bank, spin, failed-work, seed and past mode occurs in Drec.
For t_N=2 sum_(l>=1)c_(lN)/c0<1 the owned estimate gives

    |H_N(M)-H0(N,Drec)| <= -log(1-t_N)/beta,
    |H_N(M_+)-H_N(M_-)| <= 2 C1(N),
    C1(N)<64*22^(-N)/N! at the actual beta=2p^2.         (67)

The first bound is an absolute comparison, not a subtraction from the
physical price. The true log Drec and N remain. The second is the
owned endpoint Lipschitz estimate and ||M_+-M_-||<=2. No derivative
of a discrete programme selector is assumed. Fields being compared
have the SAME complete carrier, scene, beta, ranks and actual N;
changes of these data keep their additional price/source.

### The complete source survives actual final-label recording

On input families for which section7e's ideal scalar compression(56)
and its all42 field pullback are proved, fix a common catalogue and
central stencil delta_h. Equation(65) leaves the whole feedback
secants unchanged. Equation(67) bounds each new
heat secant by C1(Nrec)/delta_h. Therefore the original all42 estimate
(paidwriter equation41), with section7e's actual gain Gamma_K, becomes

    ||ell_rec-E_PC,h||_(V_h*) <=
       (M_r tau_h/a0) T_h
       +(Omega L_h/(a0 tau_h)) e1,h
       +(L_h/Gamma_K)[M3,j delta_h^2/6
          +(C_J epsilon_q+C1(Nrec))/delta_h],
    C_J=2r zeta/(1-zeta).                              (68)

Here M3,j bounds the third derivative of the IDEAL feedback composition
j_K(gamma_h Q_h); its heat is not being differentiated or substituted.
The definition of L_h, all finite-coordinate dual-norm factors and the
ambient42 pullback are exactly those of the original estimate. The
old C_B>=C_J can also be used as a conservative error constant. At the
primary common-null centres, use original Book equation(49) to remove
the weak-query remainder; do not differentiate along the null family
instead of in the full ambient fields.

Fix the mesh, approximation catalogue, actual positive gain, material
readout accuracy, stencil and bank BEFORE the final inverse choice.
The already owned positive powers G^q approaching G^dagger have an
unbounded subsequence. Along it epsilon_q->0 and

    Nrec(q)>=(1+q)(n_G,h+m)+N_CX,old+w -> infinity.

Use the actual inventory if routing adds more stages. Consequently
BOTH epsilon_q/(Gamma_K delta_h) and
C1(Nrec(q))/(Gamma_K delta_h) tend to zero. These stages implement
the inverse and recording; no idle padding or new clock law is added.
The existing material-checkpoint condition eta_h/delta_h->0 and all
mesh-dependent constants remain. This transports the ENTIRE native
source-limit construction, not just a selected coframe row.

### A noncomputational protected seed keeps an explicit leakage debt

Equation(65) remains exact even with a noncomputational P_K. But the
bank tests only A=0, so bank0 need not be exact return to all of P_K.
Define R0=|0_A><0_A| tensor I_K, so P<=R0, and use the actual word:

    E_full=P Uhat^dagger P Uhat P,
    E_bank=P Uhat^dagger R0 Uhat P,
    L=(R0-P)Uhat P,
    E_bank-E_full=L^dagger L >=0.                     (69)

Under the EXACT ideal identity (R0-P)U P=0 and the common operator
error ||Uhat-U||<=epsilon_q, ||L||<=epsilon_q and the effect error is
at most epsilon_q^2. This ideal identity holds for section7d's
commuting added-CAR construction WHEN its entire protected carrier
is untouched by the original return word: equation(50) cancels the
added compiler on every column. It is not inferred for an arbitrary
entangled address/RIGHT projector; such a projector needs the same
full identity or retains the exact L in (69).

The bank0 effect supplies a comparison determinant
J_bank=-Tr_P log[(1-zeta)I_P+zeta E_bank]. The literal Book determinant
of (64) is J_full with E_full. Integrating the trace-log gives

    0 <= J_full-J_bank
       <= [r zeta/(1-zeta)] epsilon_q^2.              (70)

Its conservative additional normalized central-secant error is

    L_h r zeta epsilon_q^2
       /[(1-zeta) Gamma_K delta_h].                   (71)

It is controlled by the SAME final inverse choice. This is an effect
and finite-secant estimate: output-state/Kraus leakage is generally
O(epsilon_q), not O(epsilon_q^2). No derivative bound follows from
value accuracy alone. No seed oracle, widened protected identity,
fictitious product seed, assigned Shannon Info or new Book cut is used.
The original pure matter checkpoint is before this final bank copy;
its causal reading and common field dictionary are preserved.

**Parent substitution.** The constructed section now has a paid internal
record of its final labels, the exact calibrated Book compression and
a controlled report discrepancy for protected noncomputational seeds.
Its ACTUAL complete copied-word heat is accounted for in the same all42
source limit. This consumes the execution/price part of the proposed
return readout rather than treating a test projector as a free physical
gate. It does not derive the physical task, actual Book retained cut,
full stack or field-variation domain. The original source-identification
and stationary-refinement application remain; GR_closed/raw216 are open.
A continuous same-carrier complete source is still required before an
owned finite-root/degree theorem may be applied. Neither secants nor a
Palatini/CQ carrier change supplies that hypothesis.

## 7g. Apply the complete preparation equation before promoting the smooth source

24 October 2026. Same native-realization owner, input eebc28c1.
The proposed shortcut is to replace the finite field-key comparison by a
smooth work preparer and then apply Book03 stationarity. Test its ENTIRE
source before making that replacement. This consumes sections7e-f,
[the owned balanced internal comparison](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#152-an-actual-internal-return-event-fixes-a-comparison-cut)
and [the existing generated-prefix adjoint](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#105-every-generated-prefix-row-has-an-explicit-whole-book-adjoint).
It neither reopens the generic operator-variation theorem nor imposes a
smooth selector of discrete words as an extra physical requirement.

Book01 sections01.4.1 and01.15 allow compatible finite operator/test
families. For example the owned interior sign-resource preparation
beta(t) in the [collective-preparation source](A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md)
has an explicit smooth orthogonal completion on every |t_j|<1. The
all42 inverse/Cayley readout supplies its field coordinates. Such a
family has genuine mathematical tangents. Its inclusion in the SAME
physical configuration domain X_N, with actual controls and their
price, is a further application of Book00 section00.4 and Book03
sections03.8/25. Finite operator admission is not that application.

First remove a distraction using an ALREADY owned construction. With
C=C_copy from (64), execute both copies and put

    Ubal=C(Uhat tensor I_bank)C,  Nbal=Nold+2w.          (72)

Add actual routing stages when needed. C Pnew=Pnew implies
Ubal Pnew=Urec Pnew, so every declared terminal output/effect and
(65) are unchanged. On ALL columns Ubal is conjugate to
Uhat tensor I_bank. Thus at this SAME longer physical Nbal its heat
partition function is exactly D_bank times that of Uhat. This is
not equality to the old heat at Nold; its dimension and duration
prices remain. The original internal bank stays at the final output.
For the ideal U=V^dagger M0 V, the full spectrum and heat are field
constant at common Nbal. For the ACTUAL positive-power inverse word,
its existing approximation error remains: copying does not make that
word exactly conjugate to M0 or supply its missing continuous tangents.
No minimum or compulsory choice of the two-copy programme is asserted.

Now test the most favorable EXACT smooth case. Fix the input projector
of (54)-(56), native M0, protected spin/past, scene, beta, zeta and the
whole clock inventory. Allow V to vary as a work-only orthogonal or
unitary preparer, together with its actual coherent inverse in U.
Put phi=V|0_W>, ||phi||=1 and x=<phi,Pi phi>. The compression (56)
still holds on every Q8-spin column. The entire declared H+J source
of the ideal balanced family therefore satisfies, for a real sphere
tangent eta with Re<phi,eta>=0,

    D_phi B[eta]=2 j_K'(x) Re<eta,(Pi-x)phi>,
    ||D_phi B||=2 j_K'(x) sqrt[x(1-x)].                 (73)

Here the norm is the Euclidean tangent dual norm on the unit sphere,
not the all42 field norm. Indeed g=(Pi-x)phi is tangent,
||g||^2=x(1-x), and eta=g/||g|| attains the bound. Every such
real tangent is realized by a skew work-generator; it leaves the
native spin, fixed initial P and the controlled middle untouched.
This is variation of the PREPARER AND ITS INVERSE, not variation
of the input state in one fixed processor. It applies when that
preparer orbit is actually free; it does not declare this orbit
native-admitted merely from its matrix representation.

On the source-bearing chart x=gamma_h Q_h, 0<Q_h<=q_max<1/2,
j_K'(x)>0. Thus a freely varying normalized preparer cannot satisfy
its independent Euler equation there, even when all pulled-back
geometric rows vanish. Equivalently its equation forces
(Pi-x)phi=0, which has x in {0,1}; neither is in this interior chart.
No claim about other critical points outside the chart is needed.
Using the SAME nonzero source gain (61), evaluated at the base,

    ||D_phi B||/Gamma_K
      =2 Omega/(a0 tau_h)
          sqrt[Q_h(1-gamma_h Q_h)/gamma_h].             (74)

There is no derivative of Gamma_K in (74). With Q_h>=b_h>0,
the right side is at least
2 Omega sqrt[b_h(1-q_max)/gamma_h]/(a0 tau_h).
At fixed h and a uniform positive report floor, reducing READY
probability makes this normalized independent source grow as
at least gamma_h^(-1/2). A small unnormalized preparation source
does not remove this ideal row. Where the actual comparison
stencils admit it, inverse compilation with the existing accuracy
condition epsilon/(Gamma_K delta)->0 preserves its secant limit;
C0 word accuracy alone is not a derivative estimate.
If other terms of the same full stack cancel this direction, their
preparer covector must have at least the norm (73), or (74) after
the same normalization. No such compensating term is assigned here.

This is a scoped exclusion of the FREE smooth-preparer shortcut,
not an obstruction to generated fields. If phi is produced by the
actual causal word from fixed initial data, the existing adjoint
eliminates its generated state row. The remaining source is the
pullback to the genuinely admitted controls, INCLUDING any actual
upstream control variation. In particular a proved constrained
field-to-configuration section could have DQ_h=0 while the ambient
sphere covector (73) is nonzero; its normal reaction is then retained
by the constraints. One may neither impose (73) on a generated state
nor silently declare a free preparer generated.

**Parent consequence.** The next application must derive this causal
field/control section and its complete pullback from the SAME native
process. Simply introducing smooth beta(t) resources, or replacing
section7f by balanced copies, cannot supply joint stationarity.
Conversely a C1 discrete-word selector is unnecessary when an actual
smooth configuration map is proved. The unpadded CQ root and primary
refining Palatini family retain their separate source contracts;
(73)-(74) do not identify them or supply an exact stationary native
refining sequence. GR_closed and raw216 remain open.


## 7h. Compose collective preparation with the literal complete Book source

24 October 2026. Same native-realization/GR-composition owner, input
2b3ac3af. Consume the [nonvacuum collective source theorem](A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md),
its [actual coherent injection](sources/d0_nonvacuum_collective_preparation_2026-10-22/joint_source/PAID_COHERENT_INJECTION_AND_WHOLE_TAPE_SOURCE.md),
paid-writer9.1's raw/deferred word, and sections7e-g here. The collective
owner previously retained an unbounded replacement by a different full
Book price. The following application supplies its literal H+J source on
one specified coherent return programme, including a full internal bank.
It does not identify that programme with every compulsory Book execution.

### One fixed encoder retains the actual correlated input effect

Let a packet contain the D deduplicated free SIGN coordinates, with
beta(t)=tensor_j[sqrt((1+t_j)/2)|+>+sqrt((1-t_j)/2)|->], |t_j|<1.
The fixed geometry/Cayley/material encoders and their actual RIGHT
factors are the owned ones. A raw moment occurrence has one packet
slot and queries at most one coordinate in that slot. Use k slots,
including repeated occurrences and all global report multiplicities.
No assumption of independence is made about a general input to these
slots. Product beta(t) is a section at which the source is evaluated.

Let E be the symmetrized positive CLICK effect of this fixed report,
0<=E<=q_max I with q_max<1/2. There are two already constructed inputs:

* The original weak report uses a genuine positive tag selecting a
  local click R_l with the SAME normalized site/PF/trace weights as
  the global source. The tag, coefficient rows and acceptance are paid.
  Only fixed actual weights are covered here. Moving weights need their
  true encoding and their source; they cannot be frozen into this tag.
* The current paid-writer10 Bernstein report has exactly its existing
  coefficients q_i and polynomial Q_h(u). Assign a separate packet
  slot to each coordinate-coin occurrence; retain its counters,
  selector and all coefficient rows. On basis SIGN inputs its effect
  is diagonal with entries q_i. Thus, before symmetrization,
  ||E-r0 I||<=max_i|q_i-r0|. No geometric polynomial is changed.

Prepare n>=k packets and execute the owned uniform coherent ordered
injection of k slots into these n packets. Retain the injection labels,
all unselected packets, purifiers and appropriate original RIGHT
systems. The exact effect on ARBITRARY correlated SIGN input is

    E_n=1/(n)_k sum_injections iota E^(iota),
    q(t)=<beta(t)^k,E beta(t)^k>
        =<beta(t)^n,E_n beta(t)^n>.                    (75)

Use one raw attempt per factory and defer its pointer readings as in
paid-writer9.1. Uniform-label acceptance, every raw failure flag and
later gates on failure branches remain present. This is a new complete
coherent schedule with its own true success gamma_{h,n}>0, not the old
measured/capped schedule or its entropy ledger. Its input-independent
logical factory laws and orthogonal retained labels give the OPERATOR
identity

    i_0^dagger A_n^dagger Pi_READY,click A_n i_0
         =gamma_{h,n} E_n                              (76)

on the entire correlated SIGN space. Here i_0 appends the actual blank
scratch. This is an EFFECT compression, not an amplitude compression.
The scalar gamma includes every real raw factory and row/label acceptance.
No uniform lower bound or success-conditioned removal of columns is used.

### Put preparation into the same return word and price it there

For the smooth comparison let S_Psi be a full-column work preparer on
SIGN alone, S_Psi|0_SIGN>=Psi; its scratch and original spin are untouched.
Include BOTH this preparation and its coherent inverse in

    V_Psi=A_n(S_Psi tensor I_scratch),
    U_Psi=V_Psi^dagger M0 V_Psi,
    Ubal_Psi=C(U_Psi tensor I_bank)C.                   (77)

The initial cut is the fixed genuine blank-work/port0 cut of section7e,
with its actual protected spin/past rank r. It is NOT I_SIGN tensor P.
If SIGN were instead an arbitrary input state to a fixed processor with
that larger identity cut, Book would trace a return OPERATOR on SIGN;
its action would not be j_K of one state's expectation. Equation(77)
is the preparation-control family, with fixed input, used here.

Count every preparer, encoder, injection, inverse and copy stage in the
actual common clock T_{h,n}, and keep every thermal dimension. On the
exact coherent-inverse comparison, (56), (72) and (76) give

    B_n(Psi)=H_ref(T_{h,n},D_full)
                +j_K(gamma_{h,n}<Psi,E_n Psi>).        (78)

H_ref is the full field-constant heat of this conjugacy family, including
its bank multiplicity and longer clock. No entropy is substituted for
Book, and no baseline is subtracted from the physical price. A varying
S_Psi is a mathematical comparison unless its actual native control map
is supplied. In finite native positive words its exact inverse is replaced
by the owned positive-power approximation, with all actual costs/errors.
Do not turn that pointwise word approximation into a smooth actuator.

For resource-only normalized pure tangents eta, at Psi=beta(t)^n,
put x=gamma_{h,n}q(t). Since the encoder/factory controls are fixed,

    D_SIGN B_n[eta]
       =2 j_K'(x) gamma_{h,n} Re<eta,(E_n-q)Psi>,
    ||D_SIGN B_n||_sphere
       =2 j_K'(x) gamma_{h,n} ||(E_n-q)Psi||.           (79)

This includes arbitrary ENTANGLED tangents of the n input packets,
not only product-state variations. It is not section7g's much larger
free sphere of ALL encoder, readiness and report work. Those extra
independent controls retain their equations if physically admitted.
The restriction here is the unchanged fixed logical encoder, not an
independence axiom imposed to remove the old correlation witness.

### The existing overlap theorem now controls literal Book and fields together

The owned one-moment-per-slot operator alphabet is I,Z_j on the ENTIRE
kind input, including the material calibration. Its first conditional is

    E_1=q I+(1/k) sum_j (partial_tj q)(Z_j-t_j I).

For the Bernstein version this follows from the same one-coordinate
slot assignment before the fixed Boolean counting/lookup. Therefore
k^2||(E_1-q)beta||^2=sum_j(1-t_j^2)(partial_tj q)^2=:G_h(t)^2.
Apply the ALREADY proved orthogonal one-excitation lower bound and
shared-slot upper bound to E_n. For B_E>=||E-b I||, with a fixed scalar b,

    G_h <= sqrt(n)||(E_n-q)beta^n||
        <=sqrt[G_h^2+B_E^2 k^2(k-1)^2/(2(n-1))].       (80)

Define the actual click-to-field gain g_h=a0 tau_h/Omega>0 and
Gamma_{h,n}=j_K'(gamma_{h,n}q) gamma_{h,n} g_h.
Use the native click coefficient a0, NOT the counted-CQ coefficient
(1-h_phi'(r0))a0. Combining (79)-(80) gives

    E_click,h := G_h/g_h,
    Q_B,h,n := sqrt(n)||D_SIGN B_n||_sphere/(2 Gamma_{h,n}),
    C_h := B_E k(k-1)/(sqrt(2) g_h),

    E_click,h <= Q_B,h,n
       <=sqrt[E_click,h^2+C_h^2/(n-1)].                (81)

READY probability, protected rank and the native middle's small angle
cancel in this source comparison EXACTLY ONCE. Their clock, absolute
price, preparation and statistical costs do not disappear. The sqrt(n)
factor prevents a false zero caused merely by averaging more packets.
The lower bound shows that nonzero global field source is retained.
The geometric norm is obtained through the actual original all42
inverse/Cayley/material Jacobian and interior sign margins, as in the
collective owner(20); the sphere norm is not relabelled that norm.

For the original weak report, the existing attenuation operator bound
is B_E<=tau_h Xi_click, with

    Xi_click=128 zeta sum_l omega_l(2 Lambda_u,l+8 Lambda_v,l).

Thus C_h<=Omega Xi_click k(k-1)/(sqrt(2) a0), retaining actual weights
and scales. For the current Bernstein report, use its ACTUAL coefficient
bound B_E<=max_i|q_i-r0|. On a fixed regular chart, the owned weak-query
formula gives max|R_h-r0|=O(tau_h), so coefficient error O(tau_h) suffices
for B_E=O(tau_h). Constants and degree/k dependence remain explicit;
no uniformity over unbounded or degenerate charts is asserted.

### Consume the primary root without inventing exact finite stationarity

On the original common-null primary, every local report value equals r0,
but its individual field derivative need not vanish. The collective owner
proves GLOBAL all42 cancellation with its real weights. At this common
value its whole counted-CQ score is scalar I plus the SAME weighted sum
of click effects times the common nonzero number 1-h_phi'(r0). It follows
that D_t q=0 and E_1=r0 I for that original report. This uses the old score
only to identify its already proved zero; it does not assign its entropy
or baseline to the new Book action. Hence (81) gives Q_B<=C_h/sqrt(n-1)
on the same nonvacuum fields, preserving the owned midpoint recovery.

For the CURRENT Bernstein report, do NOT assert exact Hermite matching.
Its q=Q_h(u), t_j=2u_j-1, has the existing error
 e_1,h=max_j||partial_uj(Q_h-R_h)||.
At a primary centre D_u R_h=0 by the exact original common-null source,
so E_click,h<=sqrt(D)e_1,h/(2g_h). Off the primary, (81) controls the
actual click source; only the owned open-chart weak-query/C1 estimate
transports it to Palatini. It does not identify it with the off-null
unpadded N1 CQ source or borrow that root's inverse/Hessian tolerance.

Given epsilon_h>0, choose the existing report accuracy so the first
term of (81) is <=epsilon_h, fix k and its true B_E, then choose
n>=max(k,2,1+(C_h/epsilon_h)^2). This gives Q_B<=sqrt(2)epsilon_h.
Include the actual physical tangent-lift norm when one is available;
it can require a larger n. Finite native field-key/decoder errors and
material errors retain their own source-normalized budgets. Taking
those errors and epsilon_h to zero composes with the SAME existing
curved metric/material recovery. This is a controlled joint-source
recovery sequence, not exact finite joint Euler roots or stability.

For actual paid secants, fix h, report table, n, common catalogue,
T_{h,n}, all gains and an admitted contained stencil before choosing
inverse precision. The scaled preparation comparison requires

    sqrt(n) L_prep,h,n epsilon_word/(Gamma_{h,n} delta)->0,  (82)

with the actual finite dimensional contraction/lift factor L_prep,h,n;
also retain the scaled central-difference truncation and preparation
errors. The old unscaled all42 error condition is insufficient for
(81). On any specified finite set of actually implemented comparisons,
the old unbounded positive-inverse subsequence permits this strengthened
finite accuracy after those quantities are fixed. No general native
sphere actuator, smooth word selector or uniform polynomial cost follows.

**Parent substitution.** The collective preparation-source result now
has a literal full-Book H+J consumer on the known-port, recorded, paid
return family. It suppresses its correlated resource-preparation source
while preserving its global field source, without a Book/Shannon equality
or a free negative term. Section7g still applies to any additionally
free ALL-work control. Physical admission of the SAME field/preparer
control domain, other independently selected stack sources, process
refinement and exact stationary refining executions remain to be proved.
GR_closed and raw216 are unchanged.


## 7i. Joint stationary reduction: semantic encoder fibres, sharp code and causal fields

24 October 2026. Same native-realization/global-composition owner, input
a0a12aee. This application combines section7h with the ORIGINAL operational
quantifiers, the owned causal adjoint and an internally represented finite
compiler choice. Its consumer is the independent-apparatus premise of the
nonvacuum source recovery, not a new geometric root or a new action.

### The original books do not impose an independent Euler row on every state

[Book03 section03.8](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#038-finite-equations-of-motion)
varies the actual finite variables x in X_N. Section03.25 states delta B=0;
its V_N is rank(P_N), not a declaration that every preparer or generated
state is an independent coordinate. Book00 section00.4 retains gate
stationarity. Book01 sections01.4.1/01.15 admit compatible finite OPERATOR
families; they neither restrict physics to one discrete compiler nor make
all unitary/preparation directions physically free.

Consequently two different statements in the existing owner must remain
available. A genuinely independent arbitrary SIGN preparation has the
source (79). A preparation GENERATED by specified t-dependent controls
has its true chain-rule source, with generated state rows eliminated by
[paid-writer10.5](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#105-every-generated-prefix-row-has-an-explicit-whole-book-adjoint).
Demanding that the former vanish is not a condition for the latter unless
that larger variation domain is actually admitted. Conversely, a causal
notation does not remove an independently selectable control.

### Preserve the operational effect, not every encoder column

At fixed h,n, true complete clock, thermal carrier, initial blank cut,
protected rank, beta,zeta and native middle, let A be the FULL unitary
encoder in (77), with its inherited work-only placement and identity
action on protected spin/past. Let i_0 append its genuine blank scratch
and Pi be the same READY/click projector. All encoder-fibre directions
below retain that placement. Allowing protected mixing would instead
require the FULL tensor effect identity gamma_0 E_n tensor I_protected
on every protected column; one chosen protected state is insufficient.
Define the operator on the whole SIGN space

    e(A)=i_0^dagger A^dagger Pi A i_0,
    rho=|Psi><Psi|,   x=Tr(rho e(A)).                    (83)

The full comparison return remains conjugate to the fixed M0 for EVERY
A, including changes on failure/complement columns. Thus its WHOLE heat
is constant at this same paid clock. For Re<Psi,eta>=0 the exact complete
Book differential is

    delta B=j'_K(x){2 Re<eta,(e(A)-xI)Psi>
                         +<Psi,delta e(A)Psi>},
    delta e=i_0^dagger[(delta A)^dagger Pi A
                           +A^dagger Pi delta A]i_0.  (84)

Section7h assumed the encoder fixed. The weaker constraint

    e(A)=gamma_0 E_n,   gamma_0>0 fixed                 (85)

suffices: ALL tangent directions to this operator fibre have zero encoder
source. They may change phases, amplitudes, scratch and unused columns;
there is no delta A=0 assumption. This is neutrality of the literal H+J
on this conjugacy family, not a claim that every other observable or every
additional physical price is unchanged.

There is an existing semantic consumer for (85). The owned
[future-profile interface](../../03_FORMALIZATION/D0/Foundation/FutureExecution.lean)
and [TheoryTransfer.observe_commutes/profile_commutes](../../03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean)
quantify over the supplied states and tests. If the SAME task already
requires preservation of the READY/click response on the whole SIGN input
family, equality of its quadratic forms implies equality of e(A) by
polarization. Preserving a separately readable READY effect gamma_0 I
also preserves gamma_0. Hence full task-preserving implementation changes
lie in (85). The converse is false: one effect does not determine the
fine retained histories or all future tests. This argument adds no new
calibration experiment, test price or chosen outcome law. A task with a
smaller input family does not automatically supply this operator identity.

For an actually moving specification e=gamma E, keep instead

    delta B=j'_K(x){2 gamma Re<eta,(E-qI)Psi>
                       +q delta gamma+gamma<Psi,delta E Psi>},
    q=<Psi,E Psi>.                                    (86)

Moving i_0 or Pi adds their real product-rule terms to (84). Moving cut,
clock, dimension, protected rank, beta,zeta or middle has its own source.
Neither normalization nor the word 'calibration' cancels these terms.

### Include an internal sharp compiler key and its full thermal trace

Let C be a finite internal code register with an actual orthogonal basis.
Book00 section00.3a already supplies orthogonality of exactly distinguishable
registration supports; it does not choose a code or declare all coherent
superpositions to be registered classical alternatives. Consider one FULL
key-preserving schedule, with every decoded, unused and failed code column:

    W= sum_a |a><a| tensor U_a,
    B_a=P_0 U_a P_0 |_(ran P_0).                       (87)

Here U_a is the true restriction of THAT complete schedule. It is not an
unpaid list of separately run programmes. All conditional gates, routing,
factory attempts and zero-control stages count in the common actual N.
On the ideal comparison, each U_a is a conjugate of a fixed middle on the
common full fibre. All code blocks, including unused labels, therefore
contribute their real fixed-spectrum heat. More generally

    Z_N(W)=sum_a Z_N(U_a)                              (88)

at that SAME longer N. A sharp input never selects just one block from
the thermal trace. If actual positive inverse words spoil the ideal
conjugacies, keep their complete source/error as in sections7e-h.

To represent a variable pure key c without an unknown-state inverse,
use a declared full operator R_c with R_c|0_C>=c and include BOTH legs:

    U_tilde=(R_c^dagger tensor I) W (R_c tensor I),
    p_a=|c_a|^2,   Bbar=sum_a p_a B_a.                 (89)

The initial cut is the genuine fixed key0/work/port0 cut, including its
real protected spin/past. Append the BALANCED copy of section7g, copying
all FINAL computational key and work labels AFTER R_c^dagger. Both
copies, the key bank, routing and any key-preparation stages are paid.
The first copy fixes that initial blank cut, so the complete return
corner is exactly Bbar. The whole heat is c-independent by conjugacy
at its actual common clock. Explicitly, after both copies and key legs,
H=beta^(-1) log[D_bank sum_a Z_(N_total)(U_a)], including the fixed
scene if used. N_total is the NEW paid length, not the pre-copy clock.
The feedback is exactly

    J(c)=-Tr log Q_c,
    Q_c=(1-zeta)I+zeta Bbar^dagger Bbar.                (90)

These finite operator identities do not assert a native smooth actuator
for every R_c. Finite native approximations retain the paid-secant boundary
of section7h. A moving-cut representation without executing the two legs
is a different price comparison and cannot silently replace (89).

At a sharp key c=|a0>, EVERY normalized pure tangent has delta p_a=0.
Therefore delta Bbar=0 and D_c(H+J)=0 EXACTLY. This covers all pure
controller directions, not just changes within the chosen basis ray,
and works for arbitrary matrices B_a, including nonideal compiled blocks.
The selected field source is still D_t J_{a0}, together with the heat
source of ALL blocks if it is nonconstant. The key equation was solved;
it was not frozen.

For completeness its general feedback equation is

    g_a=-2 zeta Re Tr(Q_c^(-1) Bbar^dagger B_a),
    gbar=sum_a p_a g_a,
    D_cJ[eta]=2 Re<eta,(diag(g_a)-gbar I)c>.            (91)

The pure controller is stationary iff (g_a-gbar)c_a=0 for every a.
Along c(s)=cos(s)|a0>+sin(s)|b>,

    J''(0)=-4 zeta Re Tr[Q_0^(-1) B_a0^dagger
                                      (B_b-B_a0)].   (92)

It can have either sign. In the scalar case B_a=(1-d_K x_a)I it is
2 j'_K(x_a0)(x_b-x_a0). Thus no programme minimum or preferred code
follows. An independently free mixed probability simplex has a different
one-sided tangent and is not covered by pure-ray stationarity.

The final key MUST be part of the stated final bank. With that copy,
bank0 tests key0 as well as work0, so its effect equals Bbar^dagger Bbar
when the genuine protected-factor invariance of section7f holds. Any
remaining protected leakage retains its actual L^dagger L. A DIFFERENT
bank omitting the final key would instead acquire the additional debt

    sum_a p_a B_a^dagger B_a-Bbar^dagger Bbar
      =sum_a p_a(B_a-Bbar)^dagger(B_a-Bbar).            (93)

This debt is zero with zero first jet at a sharp key, but is generally
positive away from it. Copying the key before R_c^dagger gives another
execution; do not substitute it into (89)-(90). As in section7f, the bank
records final labels, not all intermediate factory/key transcripts.
If the task retains an earlier measured code transcript, its unchanged
record and price must be carried explicitly; no such measured history is
silently uncomputed here.

### Exact nonvacuum stationary application on the causal operator chart

Now use the ORIGINAL report branch of section7h, its actual positive
global weights, and its already proved all42 identity D_t q_h(t_h)=0
on the primary nonvacuum family. Use the actual map of deduplicated
inverse-coframe/Cayley/material coordinates, with its stated interior
margins and regularity. Let the product resource state be generated by
S(t)|0>=beta(t)^n, keep its inverse tied to that same S(t), allow the
ENTIRE encoder fibre (85), and set the internal compiler key sharply.
For every finite n>=k the complete reduced scalar is

    B(t)=H_ref(N,D_full)+j_K(gamma_0 q_h(t)),
    D_t B(t_h)=j'_K(gamma_0 q_h(t_h)) gamma_0 D_t q_h(t_h)=0.

The encoder-fibre source vanishes by (84)-(85); the pure key source
vanishes by (89)-(91). Apply the owned whole-Book terminal cotangent
and backward prefix recursion, paid-writer10.5(43)-(44), to this SAME
complete word including preparation, inverse, key and balanced copy.
It gives all generated-prefix/state multipliers explicitly. Hence every
generated preparation/flag/copy/clock state equation and the declared
independent t, encoder-fibre and pure-key equations vanish together.
This is an EXACT constrained joint stationary lift on the ideal finite
OPERATOR chart for every mesh of the existing primary family. It reuses
its same metric readout and O(h^2) midpoint material recovery.

This conclusion needs no n->infinity suppression for GENERATED resources.
If arbitrary entangled resource controls are additionally independent,
their equation is still (79), with the controlled approximate recovery
(81), not an exact zero. If ALL work controls are free, section7g still
applies. Simultaneous-frame Ward covariance cannot remove either genuine
relative source. The sharp key is only the compiler-choice row: its
own diagonally decoded field has zero first differential, so it cannot
replace the nonzero SIGN/control-to-field map or its actual gain.

The CURRENT Bernstein/native-positive-word branch keeps its existing
first-jet and paid-inverse errors. It is not the exact original report
in the preceding application. There is no inference from small source
to exact finite native roots, and no use of the different unpadded CQ
root tolerance. Different complete field-stack terms retain their source.

**Parent substitution.** An independently fixed encoder on every column,
independently zero generated-state gradients, and a frozen pure compiler
key are no longer needed for this ideal Book application. Their replacement
is the explicit effect-preserving semantic implementation fibre, causal
control map and solved sharp-key equation on one fully counted carrier.
The remaining physical application is to derive the SAME native joint
variation image and task from the original closed process, with its genuine
boundary/cut/clock/refinement, and to realize its required exact source
or a compatible exact-root continuation. Book01's fixed-detector time
ladder alone does not do this: with an identity SIGN input cut it traces
a return OPERATOR, whereas (83)-(90) require the real blank cut and paid
preparation-control legs. No compulsory task, code selection, new physical
constraint, universal GR class or raw216 closure is asserted.


## 7j. Consume the original source inverse and complete the stationary address tower

24 October 2026. Same owner, input4c890fd4. The local inverse used below
is ALREADY proved in the original books. The new application is to the
entire raw encoder and literal recorded Book source of sections7e-i,
including every unsuccessful column. Separately, the existing Golden
refinement law now applies to the joint stationary point of section7i.
Neither application selects an Einstein action by assigning a new price.

### Use the original variational contract at its actual breadth

[Book02, immediately before section02.CVFT.v5](../../01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md#02cvftv5-refined-feedback-bounds-and-compressed-pole-discipline)
explicitly permits either a declared finite difference on a finite matrix
family OR ordinary differentiation of a smooth finite-dimensional matrix
family. Book01's six finite-section obligations likewise concern operators
and tests. Thus an exact positive-G word for every smooth coefficient is
NOT a universal prerequisite for the operator-family stationarity theorem
of section7i. That stronger implementation question belongs to the actual
word route. Its still-open application must not be reimposed as a new
axiom of the books or confused with an unproved smooth word selector.

This correction does not turn any operator model into the physical native
scene. It keeps the actual return/cut, path-algebra/geometry and full
source/refinement identifications at the end of this section explicit.

### The owned local source action reverses every raw letter exactly

Consume [Book03 sections03.26.1-2](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#03261-forward-only-order-comparison-with-an-internal-stage-register),
[OrderMemoryControl.reverse_mixer_from_forward/local_i_squared](../../03_FORMALIZATION/D0/Representation/OrderMemoryControl.lean),
and [SourcePortPreparation.local_gate_from_generator/coupled_square](../../03_FORMALIZATION/D0/Representation/SourcePortPreparation.lean).
On the SAME active port times original Q8 spin4 carrier they give

    X=diag(I_4,L_i),   X^2=Z=diag(I_4,-I_4),
    Z G Z=G^dagger,
    G^dagger = X X G X X.                              (94)

No inverse primitive, fitted rotation, known spin eigenstate or spin-bit
addressing is introduced. This uses the declared selective source-local
X in the SAME port frame as G. Its physical availability remains the
explicit implementation premise retained by Book03 and its Lean owner;
it is not inferred merely from closure of an abstract matrix algebra.

On section7e's two-cell carrier use the existing spin of the physical
port cell. For a rotation on a work bit q, the inherited routing gives

    SWAP(q,port); X X G_port X X; SWAP(q,port).          (95)

The two swaps are SIX CX calls around the WHOLE five-call inverse block.
The block equals G_q^dagger tensor I on ALL columns, with arbitrary dirty
port, arbitrary spin and past entanglement. Intermediate X calls really
couple the spin to the port; only the completed block restores its identity
action. Reuse that SAME spin for every block. There is no new spin factor,
reset, postselection or discarded complement. Intermediate tests are those
of this actual new schedule, not asserted identical to a different history.

The full RawZone source operator instead lives on scene3 times spin4.
Its neutral sector is also present: coupled_square is reversal tensor I
on all12 columns and reversal preserves that sector. A literal RawZone
application must retain its actual neutral modes and prove its routing
extension. Do not count RawZone as a new independent port factor beside
an already counted whole scene. Likewise (94) is not the same equation
on an unrestricted regular8 path-memory module: its central-even sector
has R_i^2=+I. The present application stays on the inherited active
port/spin4 interface; other carriers require their actual map.

This changes the input of the current inverse problem. The older
[paid logical echo](sources/d0_paid_writer_echo_source_2026-10-22/PROOF.md#1-separate-the-logical-word-from-its-preparation-and-factory-histories)
reversed an AFTER-BANK logical word with fresh factories. It explicitly
left preparation and measured factory tapes outside that reversal. Here
reverse the LITERAL complete raw G/CX list, replace each negative G by
(94), and use CX^dagger=CX. This is an application of the owned inverse
to every column, including coherent raw-failure and scratch columns.
No already measured/dephased transcript is thereby erased or reversed.

### The whole paid Book source is exact at a finite clock

Let V have n_G positive G and n_CX CX letters, as in section7e, and let
m=2^(K-1). The signed middle W_K has m positive and m negative G letters.
For the COMPLETE echo V^dagger W_K V the new literal inventory is

    N_G=2(n_G+m),   N_X=4(n_G+m),
    N_CX=2 n_CX+2^(K+1)-2.                            (96)

If all work rotations are routed through the one X-equipped port, add
12 n_G CX: there are 2 n_G routed work rotations, each with one SWAP
pair. Middle rotations already use the physical port. Add the actual
key, balanced-copy and closing/idle stages of the chosen complete
schedule; do not insert an uncharged idle or identify its new N with
an old clock. General raw encoders/key preparations are covered by
reversing their full literal list in the same way.

Its endpoint is now EXACTLY U=V^dagger M0 V. In (57)-(59), the inverse
error is zero, rather than small along a positive-power subsequence.
Append the actual balanced recording C(U tensor I_bank)C of section7g.
Rebuild all transported prefix cuts with the actual X/routing letters.
The existing whole-clock spectral identity at this NEW finite N gives

    B_native=H_ref(N,D_full)+j_K(gamma Q),
    epsilon_inverse=0.                               (97)

Every failed work column and native spin/past/bank mode remains in
H_ref. No subtraction or normalization changes the physical price.
The protected rank in j_K is the original actual rank: the reused spin
in (94) does not multiply it. The generated prefix/source adjoint of
paid-writer10.5 applies to this actual word, including the intermediate
spin interactions and all new clock occupations.

Use BALANCED recording in this application. The ONE-copy section7f
word C(U tensor I_bank) is generally not isospectral to U tensor I;
its additional heat source is not cured by exact inverse access.

For a finite common catalogue with its real common N, gamma and middle,
two actual field-code entries obey the exact finite-difference identity

    B_b-B_a=j_K(gamma Q_b)-j_K(gamma Q_a)
           =a_ab (Q_b-Q_a),   a_ab>0.                 (98)

For Q_b!=Q_a use the displayed divided difference; at equality define
a_ab=gamma j'_K(gamma Q_a)>0. Positivity follows from the actual
0<=Q<=q_max<1/2 chart and section7e's 0<d_K<2. Thus zero/nonzero
report differences are preserved without an inverse-precision limit.
For genuinely supplied smooth control maps the derivative is exactly
j'_K(gamma Q)gamma DQ. If gamma, N or any other specification moves,
its genuine source remains as in (86); common-cost hypotheses may not
be dropped when applying (98).

The inverse part of the source-normalized debts in (63)/(82) therefore
vanishes identically on this X-interface. Forward resource/row accuracy,
Bernstein first-jet error, actual field-key stencil error and any genuine
other stack contribution remain. In particular the CURRENT finite
Bernstein programme is not silently replaced by the ORIGINAL exact report,
and (97) does not assert an exact Einstein root for that approximation.
The narrower G/CX-only route retains its earlier positive-power theorem;
(94) does not prove the extra selective source control is mandatory there.

### Consume the complete Golden tower, including its unnormalized price

Apply the already owned [Golden-cylinder construction and whole-action law](A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md#66-whole-bootstrap-joint-thermal-source-and-refinement-balance)
and the [Books00-01 finite-section application](A4D_ORIGINAL_BOOK_BOOLEAN_TRACE_CLOCK_AND_GLOBAL_EINSTEIN_2026_10_22.md#132-books00-01-application-admissible-test-sections-and-an-actual-return-boundary)
to the COMPLETE stationary operator family of section7i. At fixed physical
mesh, iterate chi=(sqrt(p),p), J=I tensor |chi>, pi=J^dagger and
L(A)=A tensor I_2 for all operators and outcome projectors. Retain the
literal P tensor I_2 and replicated heat spectrum. After d address levels,

    H_d=H_0+d beta^(-1) log 2,
    J_d=2^d J_0,
    D B_d=D H_0+2^d D J_0.                            (99)

Section7i has D H_0=0 on its whole fixed-spectrum control chart and
D J_0=0 at its primary stationary point on every declared field,
encoder-fibre and pure-key direction. Consequently

    D B_d=0 for EVERY finite d>=0                     (100)

on those lifted directions, with the causal generated-state equations
transported by the same maps. This is the missing application of the
existing refinement-balance theorem, not a new scaling law. A root based
only on cancellation D H_0=-D J_0 would NOT generally survive (99).

The full-column projection/intertwining, positive response and complete
terminal tests are exactly those of the owned cylinder extension. Together
with the supplied internal coefficient data and single section they give
a nonempty EXACT stationary cofinal finite-operator/test tower. Its starting
binary depth depends on the actual complete carrier. Where needed, first
use U#=U direct_sum I, P#=P direct_sum P_idle and
Delta#=Delta direct_sum Delta_idle, with fixed idle data and a complete
fixed extension of the terminal outcomes. Then F#=F direct_sum 0, J#=J,
Z#=Z+Z_idle and D H#=Z/(Z+Z_idle) D H=0. Retain that absolute padded
price as the starting H_0 in (99). The old prepared inputs/tests embed
isometrically. This finite operator/test padding does not itself extend
the native faithful path-algebra representation. No descent to arbitrary
coarser stages, new physical control directions, or extension of the exact
report to the approximate Bernstein branch is asserted.

The rank/feedback multiplicity is real. P tensor I_2 has twice the rank;
it is not the rank-r P tensor |chi><chi| preparation projector. The added
heat constant and doubled determinant stay in the absolute action. On the
corresponding lifted comparison the feedback source gain also multiplies
by 2^d, so the properly normalized field-source comparison is unchanged.
This address refinement is not yet the spatial h->0 refinement. Neither
normalized Born readout nor exact address stationarity identifies those
two maps or supplies their physical clock/record/oldRIGHT transport.

### The next physical substitution is the native return and geometry map

The published ideal joint roots and their admissible operator tower can
now be consumed without asking again for a generic exact-word selector.
On the explicit source-X implementation, whole raw inversion is also
finite and exact. The remaining physical application has concrete data:

* Identify the task's real self-return with the SAME input-family cut and
  operator corner, preserving its Gram and all moving-source terms as in
  Boolean/clock13.2(48). Correct completion alone does not mean blank return.
  A transported current-state support has zero forward leakage; reusing
  the prepared input as return reference is a separate identification.
* Identify the SAME action's native scene/path-algebra distinguishability
  operator and geometry. Book03 sections03.1.1-2 use the scene spectral
  triple and Delta=D^2. The decoded coframe in a report is not by itself
  the metric of that D. The existing paid-writer11.1 computes the current
  fixed-site clock seminorm and shows its code-independent metric; that
  scoped result survives the exact inverse substitution, whose common
  primitive inventory likewise does not depend on the field code.
* Supply the compatible spatial refinement and all actually independent
  field/boundary/source rows on that common native family. A nonempty
  faithful physical realization suffices for the first positive bridge;
  compulsory universal GR selection retains its stronger hypotheses.

These are the consumers of the new exact source/tower composition, not
extra conditions invented for a convenient circuit. Arbitrary G/CX/X
actuation, a sharp programme choice and a supplied decoder do not establish
them. No new physical gate, cut, action, status or GR/raw216 promotion is
introduced. The original results and their independent routes are preserved.


## 8. Reproduction

Run from this directory:

    OPENBLAS_NUM_THREADS=1 python check_same_brinkmann_paid_source.py --output /tmp/paid_source.json

The NumPy/SciPy script reconstructs all16 exterior grades, all32 paired Julia factors and their true derivatives; verifies the finite configured source equation and actual midpoint CAR increments; computes the complete two-round port source, all40 column variations and full two material rows; checks the normalized preparation finite difference; reads the same Ricci/Weyl via the covariantly transported probes; and checks the exact parity controls. On the smaller L4 fixture it reconstructs all64 original Walsh controller rows and all128 port maps, and compares the direct two-round conditional-port sum with (5). The latter includes all16384 ordered records by exact contraction, not an independence assumption.

Author replay: Python3.13.5, NumPy2.3.5, SciPy1.17.0. The complete receipt contains the actual source vector and explicit false status flags for unproved physical identifications. This packet adds no BOOK/claim/assembly status or workflow change. Independent scientific review is required before an accepted parent substitution.
