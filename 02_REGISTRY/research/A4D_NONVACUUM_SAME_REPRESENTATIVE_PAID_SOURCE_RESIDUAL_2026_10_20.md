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


## 7k. Recover the original spatial operator from the same complete recorded clock

24 October 2026. Same owner, input01f099ee. This supplies an explicit
missing map in section7j: the ORIGINAL complete Julia128 execution has
a geometric operator readout from its own chronological Hodge. It uses
all retained columns, a fixed structural sector and an actual Julia
root. It does not identify the scalar reporter with the original full128
price, replace whole heat by a boundary trace, or select a physical cut.

### One real clock, three different boundary operations

Let g_0,...,g_(N-1) be the actual complete unitary schedule, including
copies and closing stages, T its cyclic shift and V its monodromy.
For the existing chronological operator retain

    L_clk=I-(T+T^dagger)/2=d_g^dagger d_g,
    (d_g psi)_t=(psi_(t+1)-g_t psi_t)/sqrt(2).

Keep the WHOLE internal fibre at stage0 and minimize the quadratic
energy over the other N-1 fibres. Their Dirichlet block is positive
invertible: a zero-energy vector vanishing at stage0 vanishes along
every edge. Gauge the interior edges to identities using the actual
prefixes. The remaining N-edge problem has endpoints v and V^dagger v.
Cauchy-Schwarz, attained by equal increments, gives exactly

    <v,S_0(V)v>=||v-V^dagger v||^2/(2N),
    S_0(V)=(I-Re V)/N.                                (101)

This is a genuine Schur operator of L_clk on the complete one-stage
fibre. It retains zero modes of the full cycle and uses the TRUE N.
Compression to a prepared subspace and further elimination of that
subspace's complement are different operations, as shown below.

There is also a direct readout from the OWNED whole homogeneous
scene-clock operator of [paid-writer13 and recorded-clock theorem](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#13-the-literal-two-fresh-julia128-word-on-the-complete-scene-clock-carrier):

    L_hist=I-B_S-R_S(T+T^dagger)R_S,
    R_S=(D_S+2I)^(-1/2),
    g_t=-R_S^(-1)(L_hist)_(t+1,t)R_S^(-1).             (102)

Scene identity factors are understood on the right. For N>=3 the two
oriented clock blocks are distinct, including the cyclic closing edge;
N=2 needs its separate combined-edge formula. The actual schedules have
N>=3. Thus one can extract the actual T, then compute (101), from the
SAME full L_hist. This is an operator readout, NOT a claim that (101)
is the Schur complement of L_hist with its horizontal scene terms.
The complete Book heat continues to trace L_hist. Since max degree+2=26,
the fixed-scene block extraction has norm at most26 on first variations.
Moving scene/normalization data retain their derivatives.

### The recorded full128 still contains the entire original reflection

Consume [paid-writer13.1(59)-(60)](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#131-keep-the-actual-row-of-q-including-every-unprepared-column).
For the actual signed32-word Julia palette, with original p=phi^-1,

    L_(l,c,0)=p R_(l,c)^dagger,
    L_(l,c,1)=sqrt(p) R_(l,c)^dagger,
    L^dagger L=I_DATA,  U=I-2LL^dagger=U^dagger.       (103)

The full carrier is App128 tensor DATA:32 labels times coefficient2
times port2. DATA contains all sites/CAR16; passive oldRIGHT and other
actual factors stay. This is not the smaller Julia coefficient block,
minimal64 dilation, or an invented App8 completion.

Let V_n be the actual n-round copied word with fresh App128 and retained
bank128 for EACH round, n>=1. Each pair of adjacent signed words in the
original palette is identical. Therefore R_(l,c)=0 for every ODD WALSH
label l, both coefficients c, identically on the full field chart.
The corresponding App sector is a reducing identity sector of U.
For example l=1,c=0,b=0 is a fixed dark label, not an omitted outcome.

For a chosen round i define a fixed mathematical isometry J_i: keep its
entire App128 and DATA; put every other App in that dark label and each
bank in Omega_128=128^(-1/2) sum_b |b>. XOR-copy fixes Omega_128 for
EVERY App label. Consequently, for each COMPLETE reflection round and
each XOR-copy, in forward and adjoint order,

    V_n J_i=J_i U_i,   V_n^dagger J_i=J_i U_i,
    U_i=I-N_n J_i^dagger S_0(V_n)J_i.                 (104)

Internal Walsh/SELECT primitive prefixes need not preserve this fixed
sector; their real clock stages remain present in (101). All field
derivatives obey the same fixed-isometry identity. Re V_n
need not determine an arbitrary unitary, but it determines THIS actual
U_i through its genuine reducing sector. All other recorded columns
remain in V_n and in its price. This does not change the actual blank
initial state, discard records or execute a free Omega/dark preparation.
A physical tomography protocol using those inputs must pay its own real
preparation/access costs and prove admission in the native future tests.

### The original negative Julia root fixes the full operator gauge

The missing inverse leg from U to the owned spatial inverse is explicit.
Set Pi_minus=(I-U)/2 and apply the FIXED Walsh H_32 on the output labels:
Pi_hat=(H_32 tensor I) Pi_minus (H_32 tensor I)^dagger. In the literal
[source rows](sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py),

    L_hat_(j,c,0)=(p/sqrt(32)) (W_j)_(0,c)^dagger.

Choose a known unstarred onsite word W_(j*)=-J(C_r), c=1,b=0, and call
that complete App index a. Its block is the NEGATIVE LEFT Julia root:

    L_hat_a=-(p/sqrt(32)) sqrt(I-C_r C_r^dagger),
    L_hat_a=-sqrt((Pi_hat)_aa),
    L_hat_b=(Pi_hat)_ba (L_hat_a)^(-1) for EVERY b.    (105)

The strict original chart ||C_r||<=k<1 makes the root invertible.
Equation(105) follows from (Pi_hat)_ba=L_hat_b L_hat_a^dagger and the
known negative sign. It fixes the right-unitary ambiguity of a projector
factorization using an ACTUAL labelled block. No new reference vector,
polar decomposition of the signed Dirac, or inversion of A is introduced.
Dirac zero modes and null legs are allowed.

For the known positive word J(P_r), the corresponding c=0,b=0 block gives

    P_r=(sqrt(32)/p) (L_hat_(j_r,0,0))^dagger.          (106)

The negative onsite blocks likewise recover C_r; undo-Walsh recovers
all original R_(l,c), including A=R_(0,0)=h D_sp/16. Known shifts,
addresses, grades and endpoint frames give the raising blocks
X_r=C(v_r)Lambda(U_r). Now apply, WITHOUT re-proving it, the
[labelled inverse8.4-8.5 and null-safe rational inverse6.25](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md),
with [paid-writer12.1(51)-(53)](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#121-one-field-to-operator-map-with-the-actual-density-and-matter).
This recovers all16+24 geometric directions on its actual chart. The
actual density, frame/Gram/calibration and two material readouts accompany
the map as before; D_sp alone does not recover them or affine translations.

The conditioning is explicit. Let delta=p sqrt(1-k^2)/sqrt(32).
Then ||L_hat_a^(-1)||<=delta^(-1). The existing principal-root Sylvester
calculus gives, for epsilon=||D Pi_hat||,

    ||D L_hat|| <= epsilon [delta^(-1)+(2delta^2)^(-1)],
    ||D Pi_minus|| <= (N_n/2)||D S_0(V_n)||.           (107)

The second bound uses fixed J_i and real N_n. Restoring D_sp from A
also retains its factor16/h and the known p factor. Fixed-scene (102)
retains26, while differentiating a product of N_n real gates retains
its actual product-derivative bound. All higher jets follow on the same
strict chart from root/inverse/product differentiation, followed by the
already owned field inverse. No mesh-uniform bound, scale cancellation
or free access to unprepared columns is inferred from exact invertibility.

### The cold compression and the full physical source keep their own types

For one original reflection, on the true cold Appblank DATA isometry i_0,
write Delta=A^dagger A with the original A=h D_sp/16. Then

    i_0^dagger S_0(U)i_0=(2p^2/N)Delta.                (108)

For n copied rounds the same cold corner is instead
[I-(I-2p^2 Delta)^n]/N_n. On the original positive-B chart its known
spectral inverse is available, but that corner alone need not recover
all signed/ordered Julia data. Equations(104)-(106) use the WHOLE
one-stage response and preserve those data, including their jets.

The composite field map is now

    same full L_hist -> actual clock -> S_0(V_n)
    -> original U_i -> literal Julia raising blocks
    -> owned coframe/link/density/material interpretation.          (109)

At the operator-readout level this removes the need to supply a second,
unrelated geometric operator for the original full128 family. It is not
an equality of the full clock/scene Connes distance with the decoded
spacetime metric. Nor does it turn the stationary positive-writer price
of section7i into the price of this DIFFERENT original full128 programme.

Compute the full covector on this SAME original family: its real whole
heat, literal feedback cut, Info/work/preparation, clock, oldRIGHT and
independent rows remain. Equations(101)-(109) transport that covector
through a proved operator/field map; they do not replace it with a chosen
boundary action. In particular no logdet or heat trace is normalized away.
The existing nonzero full-price residuals remain where their hypotheses
apply. Source equivalence or a controlled residual/inverse application
is still required before the existing nonvacuum recovery can consume it.

### Why the scalar reporter cannot replace this full boundary

This distinguishes a viable rich readout from a losing composition. For
section7e-j's U=V^dagger M0 V, let alpha=2m theta, c=cos(alpha),
E=V^dagger(Pi tensor I_port)V and x=gamma q. On its prepared blank-work,
port0 cut P, including actual protected factors, EVERY power obeys

    P U^k P=[1-x+x cos(k alpha)]P,
    P(I-sU)^(-1)P=g_x(s)P,
    g_x(s)=(1-x)/(1-s)+x(1-sc)/(1-2sc+s^2).           (110)

These are identities for |s|<1, not an unsupported s=1 Neumann limit.
Balanced recording preserves them because its copy conjugation fixes P.
The actual stage0 clock resolvent uses g_x(s^N), retaining N. By the owned
active/archive block elimination, the MACRO-U prepared return transfer
is [1-g_x(s)^(-1)]/s, with its analytic value at0. The primitive clock
stage0 transfer instead uses [1-g_x(s^N)^(-1)]/s. Thus at common gamma,
alpha,N the primary connected family with constant q has identical
prepared return dynamics even when its geometric metrics differ.
Other retained records, intermediate tests and the whole operator are
NOT thereby indistinguishable.

There is also no zero-energy escape by further eliminating work. For any
projection E and input isometry i with T=i^dagger E i<I, the vector

    v=(I-E)i(I-T)^(-1)u

has i^dagger v=u and Ev=0. Hence the full positive short of E to that
input is ZERO. This applies to (101) for the scalar reporter, where
T=xI<1, and to the original reflection cold corner, where T=p^2 Delta<1.
The nonzero expressions (108) and P S_0 P are COMPRESSIONS, not that
further short. No inverse of a singular archive block is smuggled in.
This does not prohibit finite-frequency response, the rich boundary
(104), or native geometry on a different proved active quotient.

### Apply the marked-clock inverse to the existing stationary reporter

The insufficiency in (110) concerns ONLY the prepared scalar return.
It does not exclude a geometric readout from the WHOLE marked operator
of the SAME section7i-j reporter. That programme already contains its
paid SIGN preparation, before its fixed logical encoder:

    V(t)=A_n(S(t) tensor I),
    S(t)|0>=beta(t)^n,
    beta(t)=tensor_j[sqrt((1+t_j)/2)|+>
                         +sqrt((1-t_j)/2)|->].        (111)

The deduplicated t_j are the actual coframe/Cayley/material operands
of sections7h-i, not newly appended geometric labels. Extract their
existing preparation stages by (102) and multiply that marked prefix.
Include its actual routing and return to the logical SIGN carrier;
keep the fixed initial blank, protected factors and chosen sharp-key
block. For the prepared density rho_* and the existing SIGN tests,

    rho_*=S rho_0 S^dagger,
    t_j=(1/n) sum_(a=1)^n Tr(rho_* Z_(j,a)).           (112)

Here rho_0 includes the actual normalized protected input and blank
SIGN/work. The completed preparation acts trivially on the protected
factor. Reading one packet gives the same value; averaging makes no
new independence assumption for the prepared product section (111).
For a perturbed native word, (112) reads its ACTUAL moments instead.

Now apply the ALREADY owned field decoder in
[collective preparation, equation(1)](A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md#1-one-equation-for-fields-and-joint-preparations):

    D_ar=B_D t_ar,       E=(D^T eta_R T)^(-1),
    K_e=B_K sum_(a<b) t_(e,ab) G_ab,
    U_e=(I+K_e/2)(I-K_e/2)^(-1),
    psi_(x,A)=(p/4)t_(x,A).                           (113)

All shared coordinates, collar, original calibration and the strict
inverse/Cayley chart are those of that owner. Its section4 proves the
coframe/link diagnostic identity V_diag^dagger O V_diag=Z and the
corresponding material diagnostic factor. Thus (113) reuses actual
operand/readout maps; it does not insert a second spatial Julia query
or assume that the scalar final report is informationally complete.

For the ideal finite OPERATOR family of section7i, let Y denote the
deduplicated free 16+24+2 fields at their original free sites. Equations
(102),(111)-(113) give the exact local left inverse

    R_clock(L_hist(Y); marked stages, rho_0)=Y,
    D R_clock o D L_hist=I_Y.                         (114)

The same full operator therefore carries every original field tangent,
including variations along the primary family for which q_h is constant.
Uncomputing SIGN later does not remove these marked prefix blocks from
L_hist. This is a relational operator readout with its specified stage
and input data; it is not a spectral invariant or the scalar boundary
resolvent. No physical intermediate measurement has been appended to
the programme, and executing additional tomography is not declared free.

The inverse has an explicit finite norm. With fixed scene data, a
preparation segment of ell actual unitary stages obeys

    ||delta S|| <= 26 ell ||delta L_hist||_op,
    ||delta t||_infty <= 52 ell ||delta L_hist||_op.

The first inequality is the unitary product rule and (102); the second
uses ||Z_(j,a)||=1 and the two density-product terms. Let
K_h=||D Dec_h||_(ell-infinity -> V_h), or its supremum on the declared
compact chart, for decoder(113) and the original field norm V_h.
Multiplication gives 52 ell K_h in that norm. Moving
initial/marking/scene data keep their own derivatives.
No bound uniform in clock length or spatial refinement is inferred.

Consequently the SAME section7i price, without any new gate or term,
now has an explicit marked-operator geometry consumer:

Here B(L_hist(Y)) is shorthand for the SAME complete Book pair with
P_clock(Y)=direct_sum_t Q_t(Y)P_0 Q_t(Y)^dagger, reconstructed from
the actual full prefixes Q_t and genuine blank P_0. Its one-step
feedback retains the single closing-wrap contribution as in section7d;
there is no extra factor N. The cut is not independently frozen, and
B is not a functional only of the heat spectrum.

    B(L_hist(Y))=H_ref+j_K(gamma_0 q_h(t(Y))),
    D_Y B(Y_h)=0                                     (115)

on its original constrained operator chart at every primary mesh.
Its full heat, failures, oldRIGHT, bank and clock remain unchanged.
The semantic encoder-fibre and pure sharp-key equations, and all
generated-state adjoints, are exactly those already solved in section7i.
Arbitrary independent SIGN/work controls remain outside that statement
and retain their sources. The actual nonlinear metric and midpoint
matter recovery are the same ones decoded by (113), with their original
boundary and O(h^2) scope. This does not assert universal off-shell
Einstein source equality or stationarity under unrestricted cut changes.

For the current finite G/CX/X words, (102),(112) recover the implemented
moments, while forward/Bernstein and source-secant errors retain their
existing budgets. Section7j removes the inverse debt, not those errors.
There is no new exact smooth word-selector or exact finite-root claim.

### An executed coframe change with its complete price

The decoder now gives a concrete physical use of the original Golden
gate, rather than identifying an address ratio with a metric scale.
Use the ORIGINAL component SIGN operands D_ar=B_D t_ar of (113).
For each physical coframe SIGN bit s in every packet, use a separate
internal flag f, already present with its paid blank preparation in
the SAME complete initial inventory. Execute only the existing word

    B_s=CX_(f->s) G_f,
    B_s(|0>_f |chi>_s)
       =sqrt(p)|0>_f |chi>_s+p|1>_f X_s|chi>_s.

No flag is measured, reset or discarded. Compressing the Heisenberg
observable against its actual initial flag0 gives

    N^*(Z_s)=(p-p^2)Z_s=p^3 Z_s,
    N^*(Z_J)=(p^3)^(#coframe bits in J) Z_J.          (116)

The second identity uses independent flags for distinct PHYSICAL bits;
repeated polynomial factors retain the existing distinct packet slots.
It holds as an effect identity before choosing a SIGN input. At the
output of B_s, BEFORE the later inverse, <Z_s Z_f>=<Z_s>_input. This
closed interaction produces a new readout while retaining the old
physical trace at that stage, not preparing pure beta(p^3 t). The later
full echo may uncompute this ACTIVE correlation; it is not asserted
as a terminal-bank correlator.

Write kappa=p^3 and T_D t=(kappa t_D,t_link,t_material). Extend the
existing diagonal encoder and READY/click test as identity on the new
flags: READY does NOT require flag0. Insert B=product_s B_s before
A_n in the actual preparation, reverse the ENTIRE new forward word
by section7j, and include all flags in the balanced final bank. Then

    V'=A_n B(S tensor I_flags),
    q_B(rho)=Tr[rho N^*(E_n)],
    q_B(beta(t)^n)=q(T_D t),
    B_new(t)=H_ref(N',H_full')+j_K(gamma_0 q(T_D t)),
    d B_new=T_D^* d[j_K(gamma_0 q)].                  (117)

The last equality is at fixed real clock/specification on this
generated preparation family; it is the full source pullback, not
an equality of absolute prices. Correlated SIGN inputs retain the
effect formula in (117), not a substitution of their marginal means.
The same protected rank, middle and gamma_0 remain. The transported
Book cut is rebuilt from ALL new prefixes. Generated flag/state rows
use the same adjoint; an independently varied extra controller would
retain its own equation.

For M flags the complete echo and two bank copies add 2M G, 4M X,
and 4M CX calls before routing. Routing both flag rotations through
the original equipped port adds 12M CX when required. At the SAME
new N', flags and their bank multiply the full thermal dimension by
4^M, while the protected rank is unchanged. A comparison programme
must include these reserved modes in its original inventory too.
Neither the added heat nor a primitive clock occupation is removed.

On the original centered component decoder, fixed calibration gives

    D'=kappa D, E'=kappa^(-1)E, g'=kappa^(-2)g.        (118)

This applies to the represented free coframes. A fixed collar stays
fixed; a GLOBAL homothety requires an actual transformation of the
collar too, or a proved local restriction. On a Bernstein AFFINE box,
flipping its u-coins instead gives D'=D_mid+kappa(D-D_mid), not (118).
Keep the actual encoding and its chart before transporting a source.

This supplies a finite field-changing operation and its whole-price
map within the inherited addressed G/CX/X interface. It does NOT
supply the Golden source weight sigma_lambda^* dB=lambda dB with
lambda=kappa^(-2). In particular the existing area polynomial P_5
from paid-writer(6) has, at Z=I and r=kappa^2,

    P_5(rI)-(rI)^(-1)=-r^(-1)(r-1)^6 I != 0.         (119)

Thus its exact two-jet application on the original nilpotent primary
centres cannot be reused at this scaled endpoint without a new valid
source transport. Equation(117) keeps the actual price instead of
assigning it the desired weight. The global rigidity theorem remains
conditional, and physical admission of this entire task/cut remains.

The same application rules out a stronger shortcut on an OPEN chart.
Reuse the analytic dilation-coefficient argument of
[Golden constitutive section7](A4D_GOLDEN_SCALE_CONSTITUTIVE_NO_GO_AND_NATIVE_H2_APERTURE_2026_10_22.md#7-sharp-strengthened-theorem-no-constant-admixture-of-the-original-book-j₂-can-repair-native-golden-scale-homogeneity),
now on the ACTUAL map (116)-(117). Fix h,n, the other field operands,
calibration, encoder, protected rank, middle and readiness. With D
standing here for the complete centered coframe SIGN tuple, set

    f(D)=j_K(gamma_0 q(D,other)), kappa=p^3,
    d_D[f(kappa D)]=lambda d_D f(D), lambda=kappa^(-2)>1. (120)

The proposed equality is the full ACTION-source weight, including the
kappa in the pullback derivative; it is not a bare covariant-tensor
weight. Assume its boundary variation vanishes on these directions,
or that an actual boundary transport has proved precisely this law.
Equation(56) makes f real-analytic on the connected SIGN cube,
INCLUDING D=0: q is a finite polynomial and its logarithm argument is
1-zeta+zeta(1-d_K gamma_0 q)^2 >= 1-zeta > 0. The true two programmes'
H_ref terms may differ, but each is field-independent at this fixed
specification; their absolute prices have not been equated.

If (120) holds on any nonempty open coframe chart, the real-analytic
identity theorem extends its derivative identity to this cube.
Integration gives f(kappa D)-lambda f(D)=C. Write the Taylor expansion
f(D)=sum_alpha a_alpha D^alpha at zero. For every |alpha|>=1,

    (kappa^|alpha|-lambda) a_alpha=0,

so ALL positive-degree coframe coefficients vanish. Analyticity then
makes f coframe-independent throughout the connected cube. Hence any
nonzero coframe price/source on this reporter excludes (120) on an
open chart. With other fields fixed this conclusion is on that fibre;
a full-field open hypothesis extends it over those other fields.
A finite stencil or the primary solution family alone is insufficient.
No physical inverse metric at D=0, nor physical admission of repeated
scale steps, was used: D=0 is only the regular operator continuation
point. This applies the owned generic argument; it adds no new selector
or numerical certificate.

Consequently (116) cannot supply the positive action weight required
by the Golden full-action shortcut for this nontrivial fixed reporter.
Its actual metric factor is phi^6, not literally phi^2. A physical
scale step that changes the collar, calibration, source rank, readiness
or actual clock-dependent field term has a DIFFERENT full source to
compute. A separately controlled refinement limit can also lose this
finite analytic extension. Neither possibility is excluded or supplied
here. The direct Book03 stationary-section route remains: prove native
admission of (111)-(117) into its original joint action domain, with
every genuine remaining source retained.

### One complete off-null operand, tag, geometry and Book source

24 October2026, input95ad336f. This consumes the existing
[paid-writer10.1-10.4](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#10-open-chart-weak-query-consumption-by-the-complete-native-book-word),
[positive partition factory, section6](sources/d0_causal_native_weighted_synthesis_2026-10-21/native_source/NATIVE_POLYNOMIAL_FIRST_JET.md),
[coherent operand refinement](sources/d0_global_native_gr_closure_2026-10-22/COHERENT_OPERAND_REFINEMENT.md)
and the fixed positive
[ten-sign table](A4D_FULL_TWO_BAND_FIXED_TEN_SIGN_CAR_CHOI_SOURCE_2026_10_21.md).
Weak operands and the absence of an operand-error/strength amplification
were already proved there for their declared interfaces. The application
here binds the ORIGINAL off-null operands and a real normalized tag
compiler to THIS complete Book price, exact inverse and marked geometry.
It does not identify the older counted-CQ price with Book.

Fix h and a compact actual affine coordinate box u=c_h(Y) strictly inside
the regular inverse-coframe/Cayley/material chart. Use the original
six-face operands f_s,q_s of paid-writer10.1, the actual positive density
rho_s(Y), fixed mu_s>0 and constant Omega=sum_s mu_s rho_s. Set

    a_s=f_s/rho_s, b_s=q_s/rho_s, pi_s=mu_s rho_s/Omega,
    Lambda_h >= max(1,2 sup_s |a_s|,2 sup_s |b_s|).


The density convention is an exact binding, not a second division.
The older native-query formulas call a_s,b_s themselves f_z,q_z.
Their real raw coframe is e_raw=T E/(s sqrt(rho)), whereas the
density-dressed operational coframe is e_op=sqrt(rho)e_raw=T E/s.
The original six-face functional is degree TWO in its coframe legs.
Thus, with the original EPS_PLUS orientation transported with T,

    f_s=rho_s a_s=h^-4 P_EPS_PLUS(h e_op,U),
    q_s=rho_s b_s
       =s^2 sum_(a,r,t,A) eta_R,aa D_ar D_at
                       D_h,r psi_A D_h,t psi_A
       =sum_A ghat^(rt) D_h,r psi_A D_h,t psi_A,
    ghat=s^-2 E^T eta_null E.

These identities hold as full field functions, including moving rho
and their derivatives. They follow from paid-writer(3),(6),(8) and
native-first-jet4-5 with the inverse used exactly. The fixed conversion
T carries its inherited orientation; a new REST epsilon is not inserted.
If using Psi_read=s^2 psi, retain the resulting s^-4 in the material
quadratic form. No density, matter calibration or area factor is fitted.

Lambda_h is a fixed finite Q(p) upper bound on this box, not a moving
calibration. The two target sign probabilities
(1+a_s/Lambda_h)/2,(1+b_s/Lambda_h)/2 lie in[1/4,3/4].
Compile them SEPARATELY by the existing Bernstein counter/row circuit.
At each node also compile the positive normalized vector (pi_s)_s by
the same owned finite-partition factory, using an independent coordinate
packet. With B_(d,i) the tensor Bernstein basis, its ACTUAL probabilities
and sign means satisfy

    tilde pi_s=sum_i B_(d,i)(u) pi_(s,i),  sum_s pi_(s,i)=1,
    sum_s tilde pi_s=1 EXACTLY,
    <Z_a,s>=tilde a_s/Lambda_h, <Z_b,s>=tilde b_s/Lambda_h. (121)

All node vectors are strictly positive. Exact Q(p) nodes are available
when the specified maps preserve Q(p); otherwise use positive rational
node vectors with EXACT sum1 and arbitrary uniform accuracy. Such vectors
exist by density in the interior of the finite simplex. Every node probability for the TWO OPERAND BERNOULLI rows, including
rounded rows, is chosen in[1/4,3/4]. This preserves approximation and
the margin used below. The tag entries only obey their strictly positive
normalized simplex constraint; they need not lie in that interval.
The owned Bernstein derivative formula and node rounding bound prove
C1 convergence of tilde a,tilde b,tilde pi to a,b,pi at fixed h.
For fixed finite dimension, choose the node error o(1/d); higher source
differences can use the already owned o(d^-3) choice.

Prepare EVERY coefficient row before live selection, including every
tag row. The tag and EACH of the two geometric and eight material SIGN
occurrences use fresh coordinate coins, counters, rows and factory work.
They share the sharp field key, not an unknown quantum input or the same
binomial samples. Conditional on that sharp key, the common ALL-READY
event and the selected tag, these actual logical operands are independent.
All failures, unselected rows, original material/reference resources,
OLD RIGHT and purifiers stay in the full word and price. Conditioning
describes the logical marginal; its physical weight is gamma times that
marginal. No failure is discarded or free classical density loader added.

Now apply (116) to the COMPUTED query signs, after those operands and
before the unchanged ten-sign report. Use m fresh blank flags in sequence
for EACH physical SIGN occurrence. Reusing one flag is not this channel.
The original field-preparation prefix and its decoded geometry are
unchanged. With the fixed table scale1/64, define

    kappa=p^3, tau_0=1/(64 Lambda_h), tau_m=tau_0 kappa^m,
    Q_m(Y)=sum_s tilde pi_s(Y)
                   r(tau_m tilde a_s(Y),tau_m tilde b_s(Y)).       (122)

Here r is the original sigma-minus polynomial (34); its material sign
is already included. The ten-sign multilinear identity proves (122)
exactly on the generated product sector. It is not the completed-report
mixture (1-kappa^m)r0+kappa^m r(tau_0 tilde a,tau_0 tilde b).
For correlated or superposed key/bank inputs retain the complete
Heisenberg effect; their marginal means need not give (122).

This reuses the exact inverse and balanced recording of sections7f-j
on the ENTIRE new raw word, including failed columns. Attenuation flags
are blank in the real initial inventory but are NOT required to be zero
by READY. Thus they leave the baseline gamma_(h,d)>0 and protected rank
unchanged. The actual tag/operand factories already contribute their own
READY factors and work. If M flags are executed, their additional complete
inventory is exactly that following(117), with any actual routing.
All new prefixes enter the transported cut and the true N_(h,d,m).
Consequently the same complete Book term and its first field source are

    B_(h,d,m)=H_ref(N_(h,d,m),H_full)+j_K(gamma_(h,d) Q_m),
    Gamma_(h,d,m)(Y)
        =j_K'(gamma_(h,d) Q_m) gamma_(h,d) a0 tau_m/Omega >0,
    D B_(h,d,m)/Gamma_(h,d,m)=Omega DQ_m/(a0 tau_m).     (123)

The strict table bounds give Q_m<=q_max<1/2 and
|tau_m tilde a_s|,|tau_m tilde b_s|<=1/128<0.01.
H_ref retains the true full dimension and duration and may change with
d or m. It is field constant only at this fixed complete specification.
Equation(123) divides ONE covector by its actual nonzero gain; it does
not differentiate B/Gamma, normalize the physical price, or solve an
independently varied aperture/clock equation. No I D Gamma term is
missing. Generated state/flag rows have the same causal adjoint as before;
truly independent preparation/controller directions keep their sources.

The operator readout (102),(111)-(114) still uses the ACTUAL original
coordinate-preparation prefix, including its finite-field key and
recoding when needed. Its old signs have not been attenuated. Hence
the same marked complete operator supplies the geometry consumed by
(123), with its true decoder/lift norm. Finite words recover their
actual discrete moments; the smooth comparison section is not a new
continuous selector of finite words.

### Source accuracy without a hidden inverse-aperture error

For the Taylor calculation define

    tilde rho_s=Omega tilde pi_s/mu_s,
    tilde w_s=tilde rho_s(tilde a_s,tilde b_s),
    tilde I_h=Omega sum_s tilde pi_s(tilde a_s+lambda_- tilde b_s),
    epsilon_geo,h,d=||D tilde I_h-D I_h||_(V_h^*),
    I_h=sum_s mu_s(f_s+lambda_- q_s).

tilde rho is the realized REPORT weight, not a redefinition of the
physical PF density or of the original geometric decoder. Its error
is included in epsilon_geo. Substitute these actual quantities in
paid-writer(36)-(37). Because sum mu_s D tilde rho_s=0 EXACTLY,
the r0 term cancels, with no negative counterterm or removed Book anchor.
In the same full field dual norm the result is

    ||D B/Gamma-E_PC,h|| <= epsilon_geo,h,d
                               +(M_r tau_m/a0) tilde T_(h,d),
    tilde T_(h,d)=sup_(||V||<=1) sum_s mu_s
      [||tilde w_s|| ||D tilde w_s[V]||/tilde rho_s
       +||tilde w_s||^2 |D tilde rho_s[V]|/(2 tilde rho_s^2)].
                                                               (124)

Here M_r=2*10^-5 is the owned Hessian bound, E_PC,h=D I_h,
and every shared coframe/link/material coordinate is differentiated.
For a genuinely moving total Omega the leading source instead contains
D I_h-(I_h/Omega)D Omega; (124) does not erase that direction.

Operand and tag C1 errors in(124) are NOT amplified by1/tau_m.
Thus the fixed Bernstein tables can be reused while m grows, unlike
approximating the final weak report independently at each strength.
At fixed h, first choose degree/rounding for epsilon_geo, then increase
m until tau_m tilde T_(h,d) reaches the required budget. This finite
ordering needs no h-uniform assertion about a fixed P5/C8 approximation.
Taking the smallest m with tau_0 kappa^m<=h^2 uses
m<=ceil(2 log_phi L/3), h=1/L, Lambda_h>=1. A larger true T may
require further depth. If m>0, kappa h^2<tau_m<=h^2 for that smallest
choice; if m=0 only the upper bound is asserted. Neither logarithmic
depth in a growing norm budget nor physical optimality follows without
its actual bounds.

The same cancellation controls actual price secants. At fixed h,d and
the specified compact coordinate norm, (122) is a finite polynomial
with Q_tau-r0=tau P(tau,u). Hence

    A_j=sup_(0<tau<=tau_0) ||D^j Q_tau||/tau < infinity,
    j=1,2,3.                                            (125)

Let b=1-zeta, R=rank P, d_K in(0,2), and
eta=1-d_K gamma q_max>0. Directly from(56),
j_K'>=2R zeta d_K eta,
|j_K'|<=2R zeta d_K/b,
|j_K''|<=2R zeta d_K^2/b and
|j_K'''|<=12R zeta^2 d_K^3/b^2.
The complete chain rule therefore improves(63) to

    M3,B/inf Gamma <= Omega/[a0(1-2q_max)]
      [(A3+6 tau A1 A2)/(1-zeta)
                   +24 zeta tau^2 A1^3/(1-zeta)^2].      (126)

The extra gamma powers are <=1 and d_K<2; the common nonzero
R zeta d_K gamma cancels. There is no implicit1/tau or1/gamma
loss in this fixed-catalogue third-derivative bound. Central secants
multiply it by delta^2/6 and their ACTUAL coordinate-to-field lift
norm. No uniformity in h, degree or lift is inferred. The inverse-word
debt is zero only on the exact source-X interface of section7j;
forward finite-code, stencil and all other real errors remain in
their correctly gain-normalized budget.

### Consume the existing global Euler theorem

This is an application of the
[whole-action consumer12(41)](A4D_ORIGINAL_BOOK_BOOLEAN_TRACE_CLOCK_AND_GLOBAL_EINSTEIN_2026_10_22.md#12-the-precise-global-einstein-consumer-of-these-whole-process-results),
not another microscopic scale-weight argument. Write delta_h for the
right side of(124) plus the actual normalized finite-word/secant debt,
and eta_h=||D B_h composed with its actual field lift||/|Gamma_h|
for THIS complete Book execution. For a different selected full action,
its same-execution first-source binding must be proved and any extra
paid-source mismatch included in delta_h. On the stated admitted test
space,

    ||E_PC,h(Y_h)|| <= delta_h+eta_h.                     (127)

Thus, when the FULL testwise error tends to zero, including the actual
quadrature normalization and sampled-test norm specified in(129), and
the decoded sequence has a regular limit with geometric source consistency,
EVERY limiting coframe, independent-connection and matter Euler row
of I_PC vanishes. The full vacuum consumer then gives the entire
Ricci-flat class on that regular chart, including nonzero Weyl
curvature. Its nonvacuum conclusion keeps the actual two-scalar
density/current/volume conditions; it is not arbitrary matter.

Keep CurvatureConvention=EPS_PLUS for the original Brinkmann source.
The already proved
[all-order sign retyping](A4D_ORIGINAL_STAR_NULL_CART_SIGN_AND_ALL_ORDER_CQ_RETYPE_2026_10_21.md)
gives f_null=-f_canonical and the SAME price in canonical coordinates
r(-x,y), not a newly selected sigma-plus detector. The standard
positive-oriented leading geometry is +vol_g R/2 for this EPS_PLUS
owner. No sign, factor of two, material coupling or source norm may
be transferred without this owned map.


For the actual regular four-dimensional mesh sector this geometric
consistency premise can be supplied directly. Require uniformly C3
interpolants Z_h=(e_op,h,omega_h,psi_h), with native samples
Y_h=Sample_h Z_h, and compactly supported C3 tests on
a fixed enlarged slab, a uniform inverse-coframe gap, convergence to
Z=(e_op,omega,psi) in C2, and every varied stencil inside that slab.
Use the existing Cayley links
U_(r,h)=(I+h omega_r/2)(I-h omega_r/2)^(-1), in the original plaquette
order. Require the ACTUAL quadrature mu_s=c_quad,h h^4 with c_quad,h>0
field-independent; this includes the owned uniform reference weights
and a known global normalization. General spatially varying quadrature
requires its own typed continuum measure, not this replacement.

Here is the whole first-source argument. Put Z(epsilon)=Z+epsilon v
inside the same uniform regular chart. Taylor's formula for matrix
multiplication/inversion on that compact family gives, with its
epsilon derivative bounded at the same order,

    U_(r,h)=I+h omega_r+(h^2/2)omega_r^2+O_C1(epsilon)(h^3),
    P_(rs,h)=I+h^2 F_rs+O_C1(epsilon)(h^3),
    f_h=vol_ghat R(ghat,omega)/2+O_C1(epsilon)(h),
    q_h=sum_A ghat^(rt) partial_r psi_A partial_t psi_A
                                           +O_C1(epsilon)(h).   (128)

Here vol_ghat=det(E)/s^4>0 on the original oriented component.
Since det(T)=-1, this is the transported volume -det(e_op), not
the uncorrected REST determinant. The inherited epsilon is retained.
The second line uses the owned ordered plaquette and inverse convention;
the third uses its exact EPS_PLUS complementary-wedge identity and
the h^2 coframe area. Forward material differences use the very same
sampled scalar history. Applying Taylor to the varied family, not just
differentiating a bare O(h) value claim, proves the displayed derivative
remainders. Compact C3 bounds give one constant for all cells and tests.
The true h^4 Riemann sum and its differentiated density therefore have
error at most C h ||v||_C3. Smooth field discrepancy adds
C ||Z_h-Z||_C2 ||v||_C3. Independent connection tests are
delta U=D Cayley_(h omega)[h delta omega]; bare unit-link tests do
not have this normalization.

Consequently define
I_PC=int [vol_ghat R(ghat,omega)/2
            +lambda_- sum_A ghat^(rt) partial_r psi_A partial_t psi_A] dx
in this fixed-calibration EPS_PLUS chart. The corresponding native
field test is v_h=D Sample_h(Z_h)[v], the derivative of the actual
nonlinear coframe/link sampling map. Combining(124),(127),(128) gives the explicit
global estimate

    |D I_PC(Z)[v]|
       <= C(h+||Z_h-Z||_C2)||v||_C3
                    +[(delta_h+eta_h)/c_quad,h] ||v_h||_(V_h).        (129)

The actual lift/test norm is retained. Equivalently the geometric
continuum source has gain c_quad,h Gamma_h, not Gamma_h when c_quad,h!=1;
both approximation and stationary residual must use that gain.
An unnormalized L^4-cell sum has c_quad,h=h^-4 and is not mistaken for
a Riemann sum. In particular the exact uniform-test condition is

    [(delta_h+eta_h)/c_quad,h]
       sup_(||v||_C3<=1) ||D Sample_h(Z_h)[v]||_(V_h) -> 0.

No uniform sampling/decoder bound is assumed without proof.
This supplies source consistency for the stated smooth sampled families. It supplies no compactness of arbitrary finite roots
and no stationary-root existence. Its vacuum conclusion is full
Ricci-flatness on the covered chart; the material conclusion retains
the original constrained scalar current and volume equations.

Equation(129) supplies forward source soundness, not existence or
compactness of a stationary refining sequence. The exact primary
Brinkmann/midpoint family remains its independently proved consumer,
with its O(h^2) matter recovery; it does not prove arbitrary all42
compactness. This approximate operand compiler does not inherit its
exact finite roots or the earlier exact primary two-jet identity. The constructed finite words alone do not establish the
original Book03 physical tangent domain, its compulsory self-return
cut, or zero sources on additional admitted controls. Fixing the entire realized marked operator AND its initial readout
data across field comparisons removes this chart's field tangents;
a fixed programme law alone does not do so. These are the remaining native applications,
not permission to repeat operand, inverse or fixed-report scale searches.

**Parent application.** The configured stationary reporter no longer
needs a separate supplied geometry or a scalar-return inverse: (114)
binds its own complete marked operator to its original full field chart
and (115) to its existing price. This is distinct from the original
Julia128 inverse (104)-(109), whose actual nonzero price residuals remain.
Equations(121)-(129) now add a same-operator, complete-Book open-chart
source construction and a smooth full-field continuum consumer. Its
normalized approximation and stationary-residual budgets stay explicit.
The remaining physical premise is the native admission of THIS joint
task/cut/control image and compatible stationary refinement, including any truly
independent stack sources. Exact Connes-metric equality and selection
of one unique microscopic schedule are not additional prerequisites
for the stated TheoryTransfer interpretation. No physical action,
selector, GR_closed/raw216 promotion or standalone certificate is added.


## 7l. Bind the cut and source to the original operational task

24 October 2026. Same native-realization/global-composition owner, input
885bdd54. This consumes Books00-01, the ORIGINAL Book03 order task and
sections7e-k together. The parent is the native task/cut/control image in
(129), not a new gravitational ansatz. It removes a separate mathematical
input-cut choice WITHIN the supplied complete task and identifies exactly
which implementation variations its existing correctness law controls.

### The input family and actual return event determine the constructed cut

Let S_task be the physically supplied family of complete INITIAL density
operators in one native Hilbert space with its actual Gram. Its input cut is

    P_in = join_{rho in S_task} supp(rho).

This is the unique smallest orthogonal projector containing every allowed
input. In finite dimension a finite support-spanning subfamily suffices;
the support of any positively weighted sum of that subfamily is P_in.
No distribution over the inputs or new price is selected by this formula.
If i is the calibrated isometry, i^dagger i=I_K, the inputs are
i rho_K i^dagger, and their supports span the allowed protected K, then
P_in=i i^dagger. One actual pure state generally does
NOT supply that task span.

Apply this to the ALREADY supplied input in (54)-(56), extended by the
actual bank blanks in (64). The initial work, SIGN, port and bank are
blank; the allowed spin input is arbitrary, as in
[Book03 section03.26.1](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md#03261-forward-only-order-comparison-with-an-internal-stage-register).
Retain only the actually allowed protected past/seed span, including the
actual INITIAL key where specified; a sharp key generated inside the
word stays inside its real preparer. Then this construction gives exactly
P_new of (64), with the same protected rank. In particular S(t) and the
resource preparation are executed INSIDE the word. Their generated SIGN
states are not extra arbitrary initial inputs. Hence a fixed P_in is
compatible with all42 variations of the existing operator chart.
The larger complete thermal Hilbert space, unsuccessful columns and
oldRIGHT remain in the trace; input rank is not thermal dimension.

Let W_j be the actual prefixes before the closing clock edge. The same
unconditioned closed input family at stage j has support

    P_j=W_j P_in W_j^dagger,
    delta P_j=W_j(delta P_in)W_j^dagger
                 +[delta W_j W_j^dagger,P_j].

Thus the intermediate cuts and their moving-source terms are generated
by the SAME execution. With fixed input task delta P_in=0; this does
not set delta W_j or delta S(t) to zero. No external diary is introduced.
These supports must not be replaced by the reducing hull of all separately
conditioned pointer branches: that is a different input/readout family.

An INITIAL support alone does not say what is compared at the end.
Here (65)-(66) already supply the real recorded bank0/return-corner
intertwiner on the protected invariant sector. Consume THAT paid
comparison as the task's return boundary, with both terminal records
retained. Completion of either record is not a return to the blank;
Pi_done=I does not replace P_in. The noncomputational seed case retains
its exact leakage L and debt (69)-(71). On the exact source-X branch,
use the whole raw inverse of section7j and the same protected-sector
hypothesis, rather than silently extending bank0 to a larger cut.

For this input/return task, the existing stage-active cut is therefore
fixed by its input span, actual prefixes and actual closing comparison.
Interior leakage is zero and the previously computed SINGLE wrap carries
the feedback. Transporting P_in through the closing edge as well would
instead identify the final subspace with a new one and erase the very
return comparison. It is not the same task. There is no extra factor N
in J, while the whole heat keeps its real N and full carrier.
This removes a separate projector selector for THIS constructed task;
it does not prove that M1 selects the task, its blanks or this stage-active
interpretation as the physical Book03 boundary.

### Primitive Golden return is not a new constraint on the whole programme

[Book01 section01.6](../../01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md#016-minimal-positive-response-closure-and-the-equation-pp21)
uses one direct primitive exposure and its first positive self-return.
Book03 section03.26 has F=p^2 P on the DECLARED splitter block.
The very next original construction has complete record weights (1,0)
and (p^6,4p^3). Thus the books already distinguish that primitive law
from a compound programme's return. Algebraically, with Q=I-P,

    P B A P=(P B P)(P A P)+P B Q A P.

The second term is a real internal return, not an external memory.
Consequently (56)/(115)'s macro feedback is not required to equal p^2P.
This does not remove the need to bind the actual task boundary to Book03.
It removes only the extra, unsupported demand that every full programme
repeat its primitive splitter's leakage.

### Consume an actual original correctness law before moving its source

The original order task supplies programme c=0,1, arbitrary spin v,
blank port/record, and two fixed chronological words. Its record1 laws
are 0 and f=4p^3 respectively. For a REAL positive symmetric input effect e on programme
and spin these laws force

    e_Q8=f |1><1|_programme tensor I_spin.

Indeed the zero diagonal block on c=0 makes the corresponding off-diagonal
blocks zero by positivity, while the law for every v fixes the other
block. Thus changes implementing this SAME original response law have
delta e_Q8=0. This is a concrete native application of (83)-(85); no
Einstein output table has been prescribed. The nonzero dark probability
p^6 on c=1 remains part of the complete law.

The original source-local X/routing and actual preparation premises
remain; a common two-port palette alone does not implement this task.
Its scope matters to the full-source composition. Feed the actual
coherently computed c=(READY AND click) bit into that programme port,
retaining its preparation, conjunction work and every other register.
If that bit is not yet present, its real admitted Boolean computation
and work must be included in A and the complete clock. The Q8 arm, spin
and output record occupy separately admitted WORK factors; A retains
the inherited identity on the final M0 target port and protected past.
Reusing those factors without its own carrier/source proof would not
satisfy the scalar-corner hypothesis (56). Pulling the Q8 effect back
through this whole preparer A gives

    e_total=f e_report,   e_report=i_0^dagger A^dagger P_bit1 A i_0.

In the same complete exact-inverse/balanced Book construction, at its NEW
real clock and carrier, the original encoder contribution is therefore

    delta_A B=j'_K(x) f Tr(rho delta_A e_report),
    x=f Tr(rho e_report).

Here P_bit1 tests that conjunction bit, so the original READY factors
are INSIDE e_report. They are not assigned a new value or divided out.
Feeding an unqualified click bit instead would include failure-column
clicks and would be a different effect. The outer Q8 implementation row is
zero, but the upstream report/preparation row is merely multiplied by f>0.
Leaving fields as spectators instead makes this task independent of them.
The original task therefore supplies a genuine implementation fibre;
it does not automatically supply the different fibre of the ten-sign
geometric report. An additional correct audit cannot be substituted for
that missing upstream source binding.

For the existing REAL addressed ACTIVE interface, the whole-input test
in (85) can also use actual native preparation contexts. The owned
[Golden/CNOT Lie closure, sections1-2](A4D_LITERAL_GOLDEN_CNOT_ACTIVE_LIE_COMPLETENESS_AND_C2_SOURCE_2026_10_19.md#1-буквальный-fullstep-без-нового-управляемого-оператора)
contains SO(2^n), n>=1. It assumes legal placement/routing on ACTIVE,
never scratch access to immutable oldRIGHT. Finite words from the blank
are dense on the real unit sphere, so their rank-one states span Sym_d(R).
Therefore their Hermitian response annihilator is i so_d(R), and its
intersection with REAL symmetric encoder-effect tangents is zero.
Equality of the SAME response function on these contexts suffices for
(85) on this real interface. This is a use of the owned closure theorem,
not a continuously variable finite-word actuator, free tomography, or
an extension to a CAR-only or differently routed interface.

### The exact remaining map in the global Einstein consumer

The owned FutureExecution quotient preserves all supplied actions and
future tests. Its signature itself does not specify a Hilbert/Gram input
span, return boundary or smooth field map. The construction above applies
AFTER those physical task data have been supplied; it does not extract
them from the abstract quotient.

Moreover, where the actual admitted future contexts include the prefix
readouts needed in (111)-(114), the composed decoder obeys

    Decode_h pr_geom R_full = Y,
    ker D R_full subset ker D Y.

Fixing the full response profile then fixes the decoded geometry. Without
that context coverage, the operator reconstruction (114) alone cannot be
called an executed observational experiment. In neither case does mere
preservation of a full profile create an open42 physical field variation.
The correct task relation, for varying input t and implementation a, is

    R_full(C(t,a))=R_task(t),
    D R_full DC(delta t,delta a)=D_t R_task delta t.

Vertical implementation changes preserve the task's answers; horizontal
input changes may change them. Sections7i-k already supply the ideal C,
its real preparation/adjoint terms, operational decoder and gain bounds.
A full source descending to Y would require dB=0 on ker DY; neutrality
on the possibly smaller ker D R_full alone does not prove that descent.
Keep every additional admitted control row from (79)/(84)/(86).

The global consumer now asks for ONE actual admitted input/return task
and its joint physical variation map, rather than independent guesses of
P, generated prefixes and encoder neutrality. For its declared source-X
operator realization the input cut, generated cut derivatives, recorded
return and ideal joint stationary tower are already composed above with
(99)-(115); (121)-(129) supply the complete approximate source and full
smooth-field limit with their actual error/lift norm. A native variation
lift and a regular stationary spatial refinement still have to be
established for the physically selected execution, with any other stack
source included. One faithful realization suffices for the first physical
bridge; uniqueness among all microscopic programmes is not its premise.
Compulsory universal selection is a stronger claim. This substitution
neither upgrades the approximate compiler to exact finite roots nor
promotes physical GR, positive_gr or raw216 closure.

## 7m. Compose the exact spatial roots in one retained execution and its full price

24 October 2026. Same owner; published input9d18c148. This applies
sections7e-l to the already owned all-mesh nonvacuum roots. It supplies
a compatible family of finite, cumulative executions with retained old
records and exact joint stationarity on the DECLARED operator chart.
The price is recomputed on each whole execution. This is stronger than
separate per-mesh roots, but it is not a price-preserving projective
quotient, an infinite finite-resource machine, or native task selection.

### A single complete word and return boundary at each finite prefix

Choose a cofinal h_j=2^(-j) sequence starting at a valid j0, with the
owned primary chart, CAR slack and stencil collar on every used mesh.
For these meshes take the exact source-X operator branch of section7i,
with its original full42 field chart, generated resources, complete
inverse, semantic implementation fibre and sharply generated pure key.
Denote its complete balanced, recorded monodromy by u_j. All private
WORK, SIGN resources, factories, target ports, keys and record banks
are disjoint. There is one shared protected factor H_R on which EVERY
COMPLETED block acts as identity on ALL columns. Immutable oldRIGHT/past
is untouched throughout; the reused Q8 spin may genuinely couple to the
port inside the source-X inverse(94)-(95). Only that completed inverse
restores its identity action. Keep those real intermediate interactions
in the paid prefixes and clock. No extra spin is allocated per mesh.
Scalar compression on a prepared column alone would not imply the
completed-block factorization. No unknown resource is copied between meshes.

In the actual private input sector let p_j=|0_j><0_j|, including its
bank blanks and actual initial key. A generated key remains inside its
preparer. Let P_R be the supplied protected input support from section7l.
The complete private monodromy is conjugate to a field-independent
middle, u_j=w_j^dagger m_j w_j, with the balanced-record conjugation
included. Its blank corner is the owned scalar

    p_j u_j p_j=s_j p_j,
    s_j=1-d_j gamma_j q_j,  0<d_j<2,
    0<gamma_j<=1,  0<=q_j<=q_max,j<1/2.

Thus 0<s_j<=1. Keep d_j and the actual readiness gamma_j fixed on this
chart, exactly as in section7i. Independent changes of them are treated
below, not discarded. For a block with a larger private protected input
support, replace p_j by that supplied support and use its true rank.

Concatenate the complete paid stage lists, including every real copy,
conjunction, inverse, routing stage, retained bank and scheduled idle.
All resources for a finite prefix M are present in its initial closed
system. Its endpoint and input support are

    U_M=I_R tensor (tensor_(j<=M) u_j),
    P_M=P_R tensor (tensor_(j<=M) p_j),
    a_M=product_(j<=M) s_j,   R_M=rank P_M,
    P_M U_M P_M=a_M P_M.                                (130)

The shared protected rank occurs ONCE; input rank is not full thermal
dimension. Extending M changes the finite input carrier. Comparisons to
the previous subsystem can embed the extra registers as initially idle
blanks, but this does not identify their complete initial tasks or prices.
No apparatus or resource is created from outside during an execution.

Use the actual transported input supports at every interior stage and
ONE global closing input-return comparison. A previous standalone
closing comparison is now an interior transported stage; its retained
record remains readable. If a different physical task keeps a separate
closing cut at every block, it has a different feedback and is not (130).
This choice of cumulative task boundary is stated, not inferred from M1.
The old record of block return and the new event that ALL blocks return
are distinct internally readable events.

The actual cumulative clock length N_M is the complete stage-list length.
Use the homogeneous whole-scene realization and the owned chronological
holonomy gauge theorem, with all its scene, clock and fibre modes.
Equation(130) gives joint conjugacy to I_R tensor tensor_j m_j. Therefore
the COMPLETE heat H_M at this new N_M and full Hilbert dimension is field
constant. Its value is generally NOT sum_j H_j. A fixed clock chart
means the paid schedule is fixed; discrete changes of the schedule do
not acquire a fictitious zero derivative.

With the same original 0<zeta<1 and ordinary counting trace, the macro
return defect on the initial FIBRE and complete Book action are exactly

    F_M=(1-a_M^2)P_M,
    B_M=H_M-R_M log(1-zeta+zeta a_M^2).                   (131)

The actual primitive-clock feedback has F_M as its one nonzero wrap block
up to prefix transport and zero on the interior blocks; P_M in(130) is
not the entire stage-active projector. These zero blocks add nothing to J.
There is no normalization of J, removed absolute anchor or extra factor
N_M. This follows from the original whole-word return formula, not a sum
of standalone block prices. The shared scene is counted once as well.

### Exact joint roots survive the genuinely coupled full price

At fixed ranks, middle and readiness, write b=1-zeta. Differentiating
(131) on the product operator chart yields

    D B_M=sum_(j<=M) c_(M,j) Dq_j,
    c_(M,j)=2 R_M zeta a_M^2 d_j gamma_j
                  /[(b+zeta a_M^2)s_j] >0.              (132)

For independent block variables its critical set is exactly the product
of the critical sets of q_j. Under any common generated parameterization,
all block critical points still pull back to a critical point; the
converse need not hold when parameterization constrains the variations.
Although the critical sets factor, the action generally has nonzero
mixed derivatives. Replacing it by sum_j B_j is false.

Consume the OWNED exact primary roots Dq_j(t_j^*)=0 on every mesh,
including every independent coframe, proper-Lorentz link and matter row.
The original semantic encoder fibre preserves the full response and its
separately readable readiness. Its rows remain zero after (132).
Each sharp pure key has zero first derivative by(89)-(91), so those rows
remain zero as well. Apply the owned terminal cotangent and backward
prefix recursion to this ONE cumulative word. It solves its generated
preparation/state/flag/copy equations with the new terminal covector.
There is no requirement that independent state gradients vanish before
the causal multipliers are included.

Consequently the entire declared product field/control chart has an
EXACT constrained joint root for every finite M. This uses the original
exact operator report, not the later approximate Bernstein compiler.
It removes the separate mathematical need to construct spatially
compatible stationary finite executions on THAT chart. The same primary
curved metric and O(h_j^2) midpoint matter recovery are retained.

For the additional controls that the chart did not cover, the exact
formula is instead

    Ds_j=-d_j gamma_j Dq_j-d_j q_j Dgamma_j
                                  -gamma_j q_j Dd_j.   (133)

Independent readiness or middle changes have genuine sources. Equation(133)
is the corner differential, not the complete row for a moving middle:
its spectrum may also vary and generate D H_M. Any induced heat/cut/rank
source is retained; constant heat was proved only on the fixed chart.
Normalized tag motions at the common primary value q_j=r0 contribute
r0 D(sum pi)=0, but this does not cancel(133). Independent entangled
resource normals retain(79); unrestricted work controls retain section7g.
Cross-block controls are not made stationary by correct marginal answers.
They require the actual joint task-response fibre or a native proof of
their exclusion from the variation domain. No such exclusion is assumed
as a consequence of closedness alone. An independently free mixed-key
simplex also keeps its different one-sided tangent.

### What precisely refines: retained records and marked geometry

For an arbitrary joint input density, even correlated across old and
fresh factors, disjoint all-column action gives the exact channel identity

    Tr_new composed Ad_(U_(M+1))
       =Ad_(U_M) composed Tr_new.                       (134)

Any old retained pointer effect is embedded as E_old tensor I_new.
Summing over a complete set of new terminal outcomes therefore recovers
the entire old terminal instrument/record marginal. The actual old marked
prefixes and their geometry decoders(111)-(114) are retained in the stage
list. Earlier measured transcripts, if required, must already be in
those banks; a final-label bank does not retroactively store them.
This is internal physical retention, with no external history primitive.

The cofinal dyadic subsequence now has compatible retained observations
and exact roots of its new cumulative prices. This is NOT the stronger
static-coisometry condition for a whole operator tower. Already for
blank embedding i_in=I_old tensor |0_new> and the genuinely evolved
embedding i_out=I_old tensor u_new|0_new>,

    U_(M+1) i_in=i_out U_M,
    i_in^dagger U_(M+1) i_in=s_new U_M.

The latter differs from U_M when the new return is nontrivial. Neither
the new thermal clock nor its cyclic wrap is obtained by tracing away
fresh WORK. Thus(134) is an exact observation/channel compatibility map,
not proof of every Book01 static operator-refinement condition or of
B_(M+1)=B_M. The old local return outcome and the new conjunction return
must not be conflated. Existing address refinement(99)-(100) may also
be used at each finite level; address depth is not spatial mesh size.

### Existing source and secant bounds survive the history factor

Fix all blocks except j, set C^2=product_(k!=j) s_k^2, and write

    A=b+zeta C^2,  zeta_eff=zeta C^2/A,  0<zeta_eff<=zeta,
    J_M=-R_M log A
        -R_M log(1-zeta_eff+zeta_eff s_j^2).             (135)

This is an exact factorization of the ORIGINAL price. It chooses no new
physical feedback parameter. The absolute first term stays in B_M.
A and zeta_eff are constant only for this single-block variation; when
other blocks vary, differentiate them too and use(132).

On the weak-operand branch q_j=Q_j of(121)-(126), with its actual fixed
Omega_j and positive a0,tau_j, the block continuum-source gain is

    G_(M,j)=c_(M,j) a0 tau_j/Omega_j,
    D_j B_M/G_(M,j)=Omega_j DQ_j/(a0 tau_j).

Therefore the entire error bound(124) survives unchanged for that block
in its declared field dual norm. Equation(126) also applies with the
DERIVED zeta_eff; its bound is no larger when zeta_eff is replaced by
zeta. All common rank/readiness/history factors cancel in the ratio.
There is no hidden inverse old-history probability in these normalized
source or central-secant bounds. The actual lift norm, delta^2/6,
quadrature normalization and growth with h/degree still remain.

No uniform nonzero absolute gain as M grows follows. The product a_M
can tend to zero; there is no asserted infinite-price limit. For exact
roots this does not affect the finite-prefix zero equations. For
approximate words every old block's normalized residual remains: adding
finer blocks does not repair a fixed nonzero error in an old variable.
To apply(129), use the actual block gain and the stated uniform-test
budget on the selected mesh. Approximation cannot inherit exact roots
merely from this composition.

### The precise original operational admission consumed here

[Book00 section00.3e](../../01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md#003e-popperian-bootstrap-falsifiability-forces-the-functional-tuple)
requires injective retention until independent inspection.
[Book01 section01.4](../../01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md#014-condensedprofinite-support)
requires finite factorization, an operator lift, positive response,
projection-compatible readout, finite halt and one calibration;
section01.6 permits finite channel composition and runtime descendants.
Equation(134) is the actual old-record readout map for this supplied
finite extension, while the original operator placement, calibration
and finite-quotient premises remain those of sections7j-l. It does not
turn an arbitrary matrix family into an admitted native finite word.

For the supplied disjoint preparers the product state
Psi(Y)=tensor_j S_j(Y_j)|0_j> is actually generated. Its tangent is
D Psi(Y)[v], and its source is handled by the same causal adjoint.
This is not an independent postulate that all preparation states factor.
Book00 section00.3c makes independence a measured defect whose vanishing
characterizes factorization. Book01's tensor Born uniqueness applies
AFTER a finite product response has been fixed. Furthermore, every
I_old tensor w commutes with every retained test E_old tensor I_new.
Thus preserving the old record algebra alone neither excludes arbitrary
new-WORK correlations nor proves that they are admitted physical controls.
The exact outstanding map is the native task/constraint tangent image
into this generated field/preparer chart, or the actual additional source
if that image is larger. Closure and physical memory have not been
replaced by a third comparison primitive.

**Parent substitution and remaining physical application.** The ideal
all-mesh roots, full paid inverse/recording, original task cut, operational
geometry and whole-clock Book action now have a single cumulative
application, with exact retained-record maps and explicit full sources.
A separate mathematical spatial retained-execution construction is no
longer an input on this operator chart. The original native admission of
THIS task/boundary/control domain and any additionally admitted source
rows remain the physical premise. Static whole-operator refinement, if
the intended interpretation requires it, still needs its own map; record
compatibility alone does not prove it. Books00-01's closure and internal
memory principles are respected without declaring this supplied task
compulsory. No new selector, minimum, universal Einstein equation class,
positive_gr or raw216 closure is claimed.


## 7n. Use the owned uniform Julia-query compiler inside the complete Book execution

24 October 2026. Same owner; published inputf410ea2f. The changed input is
an existing constructive result, not a new choice of an Einstein action:
[the labelled source owner, section8.6](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md#86-когерентная-сборка-запроса-из-julia-операций-и-её-полный-первый-источник)
already builds one fixed coherent programme from the ACTUAL moving Julia
queries. Its stated unresolved whole-price issue was the field-dependent
operator on the off-dark storage complement. Sections7e-j now supply the
complete conjugate return that prices that entire complement. This gives
the missing same-programme full-Book consumer of that existing compiler.

### Original stationarity is consumed, rather than introduced again

Book03 section03.3.0b explicitly calls finite stationarity primitive;
sections03.8 and03.25 state the stack and master-bootstrap equations.
The owned [stationary execution bridge, section2](sources/d0_native_gr_completion_synthesis_2026-10-20/stationary_information/STATIONARY_EXECUTION_BRIDGE.md#2-distinguish-two-legitimate-composition-routes)
already proves their first-source pullback through an ADMITTED execution
map. It needs no full-field minimum, positive Hessian, or surjectivity
onto the entire stack. This application does not seek a second least-action
principle from the endpoint ActionProtocol or ProspectiveExecution.optimal.
It constructs an execution map on the declared source-query interface;
its physical admission and any other stack sources keep their scope.

### A uniform generated preparer from the actual geometric queries

Fix one mesh and a compact regular window inside the original strict
Julia contraction, coframe-inverse and Cayley charts. Let Y_g denote the
40 geometric coordinates, including their actual incidence sharing and
collar. The owned source map Phi(Y_g) consists of the original full-Lorentz
Julia queries J(X_r(Y_g)), with the original frame/Gram/density/calibration
premises. Its labelled inverse in sections8.4-8.5 recovers Y_g smoothly;
section7k also reconstructs it from the marked complete clock operator.
Independently moving frame/density data must be supplied as augmented
source inputs with their own jets; the40 queries alone do not reconstruct
them. A single scalar port response supplies neither this geometry nor
those additional inputs.

The SIGN coordinate functions t_j(Y_g) of(113) are therefore smooth
functions of those actual entry queries on the chosen window. Keep their
strict |t_j|<1 margin. The target angle preparing
sqrt((1+t_j)/2)|0>+sqrt((1-t_j)/2)|1> is analytic there.
Apply the ALREADY proved polynomial/entry-word/rotation construction
of source8.6(32)-(34) to these coordinate angles. It approximates them
and their first two field jets uniformly. For each desired accuracy,
all polynomial coefficients, schedules, constant controls and widths
are selected ONCE for the entire field window. Only the actual Julia
queries move with Y_g. No field-dependent external code selector,
tomography table, separately supplied geometric S(t), or re-preparation
chosen after reading a desired metric is used.

For a fixed finite packet count n this gives an actual complete orthogonal
word Q_epsilon(Phi(Y_g)), acting on the true work blanks, whose generated
GEOMETRIC SIGN factor approaches beta_g(t(Y_g))^n with its first jets.
Polynomial degree, product-formula depth and constant-gate precision are
chosen in the order of source8.6, with their actual finite constants.
Its real storage, addressing, source calls and work leakage are retained.
There is no claim of efficient complexity or mesh-uniform bounds.
The fixed logical source encoder is the existing one in(75)-(76);
it is not refitted to a target Einstein output table.

This invocation of8.6 is on its declared addressed Julia-query interface.
Coherent query access and actual work/control preparation are inputs of
that owner. In particular, matrix reconstruction alone does not execute
a query. The native single-boost compiler does not supply arbitrary
full40 query access: its remaining source-dependent Julia block is itself
an input, with all heralded failures retained.

### Protect the original material and price the entire stored complement

The source compiler temporarily parks the unknown physical CAR input,
with all its oldRIGHT correlations, in genuine prepared work storage.
When an address register also moves, park the FULL changing address/CAR
register. Fixed onsite access may use the smaller stated storage.
The original oldRIGHT is never scratch. Between the two unconditional
parking swaps the stored original register is untouched. Hence the exact
full-column identity is

    Swap_(D,S) [Q_(D,W)(Y_g) tensor I_S] Swap_(D,S)
                  =I_D tensor Q_(S,W)(Y_g).            (136)

This holds on arbitrary dirty S columns as well as on the real blank.
It is a relabelling identity for an actually executed pair of swaps,
not an assertion that the physical swaps cost nothing. In particular,
finite compiler leakage ends in S/W; the original D and all its retained
correlations are restored EXACTLY, even before epsilon tends to zero.
This requires that the circuit between the swaps never addresses S.

Use the owned controlled-query implementation if provided. Otherwise
source8.6's dark-state parking construction has its REAL field-dependent
off-dark complement; retain it literally. The full128 reflection also
has the already proved common odd-Walsh identity sector in(103)-(104).
These constructions can remove an additional controlled-query input
when the underlying query and actual controlled swaps are admitted.
They do not prove native exposure of that underlying source operator.
A READY-only Fredkin/Toffoli cannot silently replace an all-column swap.

In vacuum the material slots below are fixed at their stated vacuum input.
For the nonvacuum extension, Q_epsilon below must ALSO include the supplied
same-physical-material preparer, with its genuine work and two field jets,
while respecting the protected-factor identity(136). The geometric query
compiler alone supplies no such preparer.

Let rho_epsilon(Y_g) be the normalized density on the relevant SIGN and ALL
query work after this actual generated preparation. The subsequent original
encoder A_n acts on SIGN and its own fresh, explicitly paid factory work.
Its READY test ignores the new query garbage: that garbage is retained,
not required to be blank. Extend E_n by identity on it. Equation(76) then
holds even when SIGN and query work are correlated. Write

    q_epsilon=Tr(rho_epsilon E_n),
    V_epsilon=A_n Q_epsilon,
    U_epsilon=V_epsilon^dagger M0 V_epsilon,
    U_bal,epsilon=C_copy(U_epsilon tensor I_bank)C_copy.             (137)

Include the ENTIRE physical inverse, not only the code-subspace ideal
inverse. On the Julia access version, source8.6 gives the matrix identity
J(X)^dagger=J_c J(X) J_c. Exact physical use requires its actually admitted
J_c/adjoint placement; approximate constant-control availability alone
does not establish that exact inverse word. Section7j reverses the actual
compiled G/CX/source-X constant letters, not an unavailable query adjoint.

There is an existing exact-inverse source version requiring no additional
moving inverse oracle: take the ORIGINAL full128 reflection(103),
U(Y_g)=I-2L(Y_g)L(Y_g)^dagger, so U^dagger=U on every column. The smooth
labelled inverse(105)-(109) expresses the same geometric coordinates in
its entries. Apply source8.6's entry-polynomial/rotation construction to
THOSE entries and reverse each U-call by the SAME U-call. Its common
odd-Walsh identity sector supplies the stated dark parking state if a
controlled query is needed; actual controlled swaps/storage still need
the inherited placement interface. Fixed readout matrix operations in
the coordinate formula are coefficients of the compiler, not new moving
source oracles. Real-space real coframe/link matrices are the chart here.
This uses the original all-column reflection before pointer measurement,
not merely access to its measured Kraus instrument.

The exact implemented assertions(137)-(138) use either this involutive
source version or the Julia version with exact admitted adjoint placement.
If only approximate inverse access is supplied, retain the existing
full-word/source error and read exact conjugacy as the comparison theorem.
The completed preparer/encoder acts as identity on the protected original
D/oldRIGHT; the reused Q8 spin can move inside an inverse block as in7j
and is restored at its endpoint. It is not counted again per query.

Every operator in(137) is the REAL finite implementation, including
failure and off-dark columns. At its actual full clock N_epsilon and
thermal dimension, U_bal,epsilon is conjugate to the SAME fixed middle
M0 tensor I_bank. Consequently its WHOLE heat is EXACTLY field constant,
not merely close on an initialized code. The scalar input-return formula
and balanced-bank intertwiner give

    B_epsilon(Y_g)=H_ref(N_epsilon,D_full)
                          +j_K(gamma q_epsilon(Y_g)),
    D B_epsilon=j_K'(gamma q_epsilon) gamma Dq_epsilon.             (138)

Here gamma is the actual fixed encoder/factory readiness, with all its
failed columns, and the same fixed input rank is used in j_K. The query
work's thermal dimensions remain in H_ref. No Shannon identification,
normalization of the trace, source-fitted Info, dropped vacuum anchor
or cancellation by an added term occurs. Changing epsilon generally
changes both absolute H_ref and the real schedule; only field derivatives
inside that fixed schedule vanish. Any separate genuinely selected price
component retains its own derivative.

This is the new substitution into source8.6's outstanding heat-complement
premise: its full logical operator need NOT converge to an identity on
dirty storage. The complete implemented conjugation prices that storage
with field-independent spectrum, exactly. The conclusion concerns this
new full recorded return execution, not the old unmodified full128 price.
Previously measured histories cannot be erased by moving their gates
inside V_epsilon and reversing them.

### Structured error transfer with no inverse weak-query loss

The needed operator estimate is ALREADY owned by
[the coherent injection source, section6](sources/d0_nonvacuum_collective_preparation_2026-10-22/joint_source/PAID_COHERENT_INJECTION_AND_WHOLE_TAPE_SOURCE.md)
and used in(80)-(81). For the original weak report, on the ENTIRE
correlated SIGN space,

    E_(n,tau)=r0 I+tau T_(n,tau),
    ||T_(n,tau)||<=Xi_click.                           (139)

Fixed normalized tags and averaging over injections preserve this bound.
Extend it by I on query garbage. For the current Bernstein report use
its ACTUAL coefficient bound ||E_n-b I||<=tau Xi, with a field-independent
scalar b and the realized coefficients. Its degree/rounding can be
chosen with the owned weak coefficient error O(tau); this is not exact
Hermite matching at the primary roots. Moving geometric weights must
be encoded in the original fixed coordinate processor, or their explicit
source must be retained. An independently moving tag cannot be frozen.

Let rho_0 be the corresponding ideal prepared SIGN density with its
specified blank query work, and define the actual trace-norm derivative
error, in the chosen geometric tangent norm V_h,

    e_1,h=sup_(||v||_(V_h)<=1)
          ||D(rho_epsilon-rho_0)[v]||_1.

Both densities are normalized. Since E_n is fixed with respect to Y_g,
D Tr(rho_epsilon-rho_0)=0 and(139) give EXACTLY

    D(q_epsilon-q_0)/tau
                    =Tr[T_(n,tau) D(rho_epsilon-rho_0)],
    ||D(q_epsilon-q_0)||_(V_h*)<=tau Xi e_1,h.          (140)

If the actual state-vector comparison satisfies ||psi_epsilon-psi_0||
<=e_0 and sup||Dpsi_epsilon-Dpsi_0||<=e_1, with sup||Dpsi_0||<=B_h,
then e_1,h<=2e_1+2B_h e_0 by the rank-one trace norm and product rule.
Thus source8.6's uniform C1 compiler supplies(140), retaining the genuine
n,h,degree and inverse-map constants. Partial trace to SIGN can only
improve that norm. No independent copies of an unknown material state
are made by this argument.

Define the gain at the ACTUAL compiled return, not at an idealized one:

    Gamma_epsilon=j_K'(gamma q_epsilon) gamma a0 tau/Omega>0.

The fixed compact window and sufficiently accurate compiler keep
q_epsilon<1/2; the original middle has 0<d_K<2. Equations(138)-(140) imply

    D B_epsilon/Gamma_epsilon=Omega Dq_epsilon/(a0 tau),
    ||D B_epsilon/Gamma_epsilon-Omega Dq_0/(a0 tau)||
                                      <=(Omega Xi/a0)e_1,h.        (141)

There is no hidden inverse tau, readiness or history-return factor.
This differs from applying a generic O(epsilon) price bound and then
dividing it by a small gain. If T, initial input, gamma, rank or the
real schedule are also varied, retain their actual additional derivatives;
(140)-(141) make no assertion that those rows vanish.

The field-coordinate source bound(124) therefore composes with this
uniform source compiler by ADDING (Omega Xi/a0)e_1,h in the same dual
norm, after the actual coordinate/source Jacobian is included. For a
cumulative execution as in7m, the same assertion uses its actual block
gain from(132),(135); the inherited-history factor still cancels.
In the continuum estimate(129), use this added error and the ACTUAL
D Sample_h(Z_h)[v], quadrature and any remaining inverse/word debt.
The fixed-clock source-X route has no heat-complement error to amplify.

### Exact parent use and the material/admission boundary

The composed map now has the form

    Y_g -> original Phi(Y_g) -> ONE fixed query programme
        -> generated SIGN/work -> complete (L_hist,P_clock,B),

with all preparation derivatives generated by the same moving queries.
The actual query stages remain marked in L_hist; (102) and the owned
labelled inverse recover their geometric source, including its full40
jets. Thus the geometric fields need not be independently supplied to
this reporter as both an external S(t) and a separate readout operator.
The causal adjoint already applies to this complete word. Its generated
storage/preparation states are not free independent variables. If the
physical task admits extra changes of the query/control apparatus, their
full source equations still have to be imposed.

The original Julia geometric query does NOT determine two independent
scalar/top preparation amplitudes. Parking an unknown material state
preserves it; it does not extract or clone the scalar data needed for
an unrelated nonlinear material report. The new application therefore
supplies the GEOMETRIC uniform input map. It combines with the existing
all42 reporter only when the SAME actual material source/preparation
map is also supplied, with its original two Euler rows and price. In
vacuum the material branch is fixed at its declared vacuum input, so
the full vacuum Einstein consumer of(129) applies on its stated regular
stationary-limit assumptions. The original exact nonvacuum family stays
available on its own exact chart; finite query approximation does not
inherit its exact roots or prove arbitrary compactness.

Remaining physical application: admit the original moving source queries,
actual storage/control placement and this return task in ONE native
execution; bind any other selected stack term; then supply its full
physical variation image and stationary refinement. This is fewer
independent inputs than external geometric preparation plus an unrelated
operator/price, but it is not their physical derivation from M1. No native
query is obtained just by declaring a matrix unitary. No physical GR,
positive_gr or raw216 closure is promoted.


## 7o. Feed the original generated material into the same complete Book query

24 October 2026. Same owner; input `d7b85112f17412ceda8543ecdbdc13e3cab5ce77`.
The changed input is the complete conjugate-return price of7j/n. It removes
precisely7c's earlier whole-operator heat/complement limitation, and gives
7n's nonvacuum material-preparer premise a concrete composition on the
inherited addressed, repeatable-preparation interface. The physical action
is unchanged; this is not a new scalar score or an import of the different
unpadded CQ critical root.

### Extract the owned material moments by a fixed coherent operation

Use the ORIGINAL normalized pure-material/address/RIGHT section(3),(32)-(34).
Let Z_seed=||C_seed||_HS^2, w_x=||chi_x||^2/Z_seed>0, and let rho be its normalized
ACTIVE density, with its actual RIGHT purification retained. For A=0,15 set

    A_(x,A)=|x,1><x,A|+|x,A><x,1|,
    Pi_(x,A)=|x,1><x,1|+|x,A><x,A|.

These are fixed coordinate operators, not new moving physical queries.
The already owned moment dictionary(52) gives

    s_(x,A)=Tr(rho A_(x,A))=2 sqrt(p) w_x psi_(x,A),
    psi_(x,A)=s_(x,A)/(2 sqrt(p) w_x).                  (142)

Off-diagonal address/RIGHT coherences have not been measured away: this
identity is a diagonal-address matrix contraction on the whole state.
It holds on the entire regular material disk, including nonzero fields.
For genuinely moving weights its exact derivative is
Ds=2 sqrt(p)(w_x Dpsi+psi Dw_x). Do not set Dw_x=0 except on the
inherited fixed-seed chart. Any independently changing seed/reference
keeps its source and, when needed, its augmented input coordinate.

Here is an explicit field-INDEPENDENT coherent extractor for this moment.
Write P_plus=(Pi+A)/2, P_minus=(Pi-A)/2, P_rest=I-Pi, and

    C_A=P_plus+P_rest/sqrt(2),
    S_A=P_minus+P_rest/sqrt(2),
    W_A=[[C_A,-S_A],[S_A,C_A]].                         (143)

The new two-dimensional factor is a real SIGN/work flag, initially blank.
Because C_A,S_A commute and C_A^2+S_A^2=I, W_A is real orthogonal.
On the +1,-1,0 eigenspaces of A it is respectively a flag rotation by
0,pi/2,pi/4; hence det W_A=1. For EVERY input column, with arbitrary
retained reference, its blank-flag effect is exactly

    <0|W_A^dagger (|0><0| tensor I) W_A|0>
                    =C_A^2=(I+A)/2.                  (144)

Thus the unmeasured SIGN flag has probabilities (1+s)/2,(1-s)/2.
The matter, normalization grade14, address and every work/reference
factor remain present. It is not a projective preparation or a scalar
amplitude read from a classical table.

W_A is the ideal CONSTANT comparison matrix. It is not asserted to be
an exactly available finite native sqrt(2) gate. The already owned
Golden/CNOT closure and7c plane construction approximate this one fixed
SO matrix on every data/flag column of its ACTUAL prepared sharp-control
sector by finite raw words W_A,nu. Choose each word once for the entire
material/geometry window, with actual legal address placement and its
paid known-one/control factors. Write i_c for that sector embedding:
the comparison bound is ||(W_A,nu-W_A)i_c||<=epsilon. The real c=0
complement of7c need not approximate W_A; its literal full unitary is
retained in the price and inverse. The chart fixes c=1; independently
allowed control-sector motions retain their additional source. Reverse the actual raw
word through7j's admitted source-X inverse interface; do not reverse
only its ideal code action or a previously measured heralded factory.

### Regenerate material inputs; preserve the protected original state

For each raw material SIGN occurrence of the fixed coordinate processor,
execute the SAME actual7c material preparation word on a fresh, genuinely
supplied seed/work bank, then its fixed W_A,nu extractor. For(145), the
ACTUAL seed-source preparation and its retained purifier must themselves
be generated from the task blanks inside Q_epsilon, with their admitted
full unitary extension and physical raw inverse. This means a genuinely
EXECUTED coherent source word; a formal purification or Stinespring
extension does not reverse an already measured preparation. Every such
measured history instead keeps its full source outside this echo unless
its own transport is proved. These actual coherent preparations keep the scalar
input-corner hypothesis(56); supplying a mixed seed state with a wider
protected input support would not suffice. Keep its SIGN flag coherent. Repeat calls use the same classical programme settings;
they do not copy an unknown physical material state. Every bank, seed
purifier, rejected or unused column and its full word is included in the
execution. There is no interaction with immutable original oldRIGHT.
If that original material register is also used as a geometric query
carrier, retain the all-column parking identity(136).

This construction requires an ACTUAL repeatable seed/preparation source
on the addressed interface. Section7c constructs the material word from
its supplied seed; it does not manufacture independent copies of an
unknown correlated address/RIGHT input. With only one such unknown input,
independence of multiple material SIGN trials is not established here.
An externally supplied seed without that preparation/inverse binding
also retains its original input-cut/preparation source debt; the scalar
return formula(145) is not established on that larger input family.
The same issue applies if banks share an unconditioned quantum code
rather than the declared common sharp programme setting. Those cases
retain their actual joint law and need their own source transport.

For the declared independent fresh preparation calls, conditioned on that
common sharp setting, the SIGN diagonals are exactly the Bernoulli product
in the ideal extractor model. They may be entangled with their individual
retained work. For M regenerated material banks, their true density derivative contains
the SUM over all M differentiated factors. In trace norm it is bounded
by M times the one-bank derivative bound. Shared programme settings
therefore retain multiplicity; they do not make additional copies free.
The existing encoder effect E_(n,tau) is DIAGONAL on these
SIGN coordinates and ignores that work; hence it needs their product
diagonal law, not a pure product SIGN state. All failure/outcome and
factory factors remain in its actual fixed readiness gamma.

Apply the existing fixed coordinate/Bernstein construction to the SAME
original geometric and material operands, using the typed dictionary(142).
Its relation to the former coordinate t_old=4psi/p is

    t_old=2s/(p sqrt(p) w_x).

This is a coordinate map, not a new material coupling. For fixed supplied
w_x it is fixed and full rank in both material directions; otherwise
encode the actual weight input too. Restrict to the compact original
material disk/weight window and its true stencil domain. Compose the
original operand functions with this map BEFORE choosing their polynomial
degree and coefficient envelope. Bounds on an extended SIGN cube must be
proved for that chosen extension: do not reuse old Lambda, coefficient,
readiness or aperture constants if the coordinate range changes. One may
use any fixed smooth bounded extension agreeing on a neighborhood of the
actual compact window; its approximation is paid and its source error is
included in epsilon_geo of(124). It cannot alter the physical operands
there. No exact previous finite table, two-jet root or arbitrary scalar
source identity is inherited by this re-encoding.

### The entire material compiler now has the already proved full price

Put all these ACTUAL material preparations, coherent extractors and the
uniform geometric query compiler inside the single Q_epsilon of(137).
Their source settings, actual work and controller complements are part
of V_epsilon=A_n Q_epsilon. At fixed catalogue, whole clock, input rank,
readiness and fixed middle, the complete physical raw inverse gives

    B_epsilon=H_ref(N_epsilon,D_full)
                    +j_K(gamma q_epsilon),
    q_epsilon=Tr(rho_epsilon E_(n,tau)).                (145)

This is the SAME exact full-conjugacy theorem(138), now applied to the
original generated material. H_ref is field constant on this chart even
when its real dirty-controller spectrum changes inside Q_epsilon. All
storage dimensions and durations remain in H_ref. Its value may change
between catalogues; no such absolute price is subtracted. Any other
selected stack term keeps its independent derivative.

The original barrier stated after(36) was that matching the material
state did not control the whole Book heat on unused controller columns.
Equation(145) supplies that control exactly for this new full return
execution. It does not identify it with the older unmodified full128
H+J action(38)-(48) or erase any previously measured histories.

For a smooth ideal material/control comparison, write E_(n,tau)=bI+tau T
with its ACTUAL fixed coefficient bound ||T||<=Xi. Normalization makes
all differentiated identity terms vanish as in(140). Thus geometric AND
material preparation errors contribute the same

    ||DB_epsilon/Gamma_epsilon-Omega Dq_0/(a0 tau)||
           <=(Omega Xi/a0) sup_||v||<=1
                         ||D_v(rho_epsilon-rho_0)||_1,             (146)

with the actual Gamma_epsilon of(141) and actual common field norm.
For m fixed extractor placements, ||(W_A,nu-W_A)i_c||<=epsilon gives,
by telescoping and trace duality, an extractor-only density jet error
<=2m epsilon sup_||v||<=1||D_v sigma||_1, where sigma is the normalized
complete moving input bank density, supported with its differentiated
tangents in that actual sharp-control sector. Preparation/compiler errors and
the weight-to-field Jacobian are additional explicit terms.

The true material words of7c have finite code settings. They do NOT
thereby become a continuously tunable finite native word. Their source
is recovered by the original equal-inventory central secants. Fix one
such catalogue and its entire echo clock. Let rho_+,rho_- be actual
normalized prepared densities at the two paid settings, with ideal
smooth comparison rho_0(theta+delta),rho_0(theta-delta). Let
k(q)=j_K(gamma q), and define the positive ACTUAL divided difference

    a_+,-=[k(q_+)-k(q_-)]/(q_+-q_-)>0,
    Gamma_sec=a_+,- a0 tau/Omega.                      (147)

At equal q use k'(q). The original q<1/2,0<d_K<2 regime supplies
positivity; all actual readiness/return factors remain in a_+,-.
Using the SAME fixed E, rank, middle, clock and heat at both settings,

    (B_+-B_-)/(2delta Gamma_sec)
            =(Omega/a0) Tr[T (rho_+-rho_-)/(2delta)].   (148)

If eta_+,eta_- bound the endpoint trace errors and M3 bounds the ideal
third density derivative on the real stencil, its error from
(Omega/a0)Tr[T D_theta rho_0] is at most

    (Omega Xi/a0)[(eta_++eta_-)/(2|delta|)
                                      +M3 delta^2/6].              (149)

Retain the actual center discrepancy and the inverse Jacobian(33) when
converting these angle covectors to psi. Choose endpoint precision
o(|delta|), then shrink the actual attainable stencil. This ordering
is possible at fixed finite mesh/compact chart using7c's dense common
catalogues and arbitrarily accurate CONSTANT extractor words. It is
not a mesh-uniform efficiency bound, a freely differentiable discrete
code, or a physical programme-choice law. A fixed extractor error cannot
be divided by successively smaller steps without this error budget.
There is no inverse tau, readiness or inherited-history probability
loss in(146) or(149).

### Apply the nonvacuum consumer at its real scope

Equations(142)-(149) supply a concrete material-to-SIGN/preparation-source
map for7n on the inherited repeatable native-word interface. Together
with its geometric query map and(124), they give the all40 PLUS TWO
material source comparison for the SAME complete Book execution on its inherited
fixed-positive-seed-weight chart. For genuinely moving weights, an actual
augmented weight query/preparer, its lower gap w_min>0 and complete
Jacobian/source still have to be supplied; the derivative identity(142)
does not itself execute that operation. For regular sampled nonvacuum
fields, the continuum estimate(129) uses this joint error, its actual
material secant/lift norms, quadrature and any remaining augmented-weight
or stack-source debt. The existing scalar
current/density/volume conditions of that consumer are unchanged.

Sharp common-code programme settings are not a proof that every physical
upstream control must move them together. Independent bank/code/readiness,
seed, other exterior-grade, mixed-resource, input-cut, reference or
cross-block variations retain
the actual additional equations identified in7f/m and the causal adjoint.
No extra selectable preparation is frozen merely because the repeated
word has been specified. The source comparison above is on the declared
shared-input chart; it does not prove stationarity in those normal rows.

What has changed is the mathematical nonvacuum input map: the existing
original material generator and fixed moment extractor now work inside
the same full-price echo as the geometric compiler. What remains is
actual repeatable seed/source/control and task admission, the full physical
variation image and its independent equations, any additional selected
stack source, and a compatible regular stationary refining family.
No exact finite roots, compactness, compulsory selection, positive_gr,
GR_closed or raw216 closure is promoted.


## 7p. Generate the original fresh reference and control the actual CAR preparation source

24 October 2026. Same native-realization owner; input4489d4fd.
This consumes7o, the already owned [raw F-source of paid-writer9.1](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#91-one-literal-coherent-forward-word-including-its-failed-branches),
[original Fourier128 reference](sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_FOUR_COPY_MATTER_RESPONSE.md#2-an-exact-original-fourier128-subfamily-with-nonzero-stencil-overlaps)
and [collective overlap theorem](A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md).
The new application supplies7o's known repeatable seed on that inherited
interface and transports the collective source theorem from artificial
kind/sign inputs to the ACTUAL full CAR/site/reference banks.

### The required pure seed is already generated by an owned raw word

Use ONLY the original F-reference component of the paid source, not its
mixed moment-preparation marginal C_mom. On the explicit real dyadic
reference subfamily, L=2^ell>=4, S=L^4, the supplied owner prepares

    F=sum_x |x> chi_x,
    ||chi_x||^2=1/S,   sum_x chi_x chi_x^dagger=I_128/128.

At each L, choose the EXACT original reference subfamily of the cited
four-copy owner: its fixed64 residue labels kappa_j have frequencies
k_j=(L/4)kappa_j. Prepare4ell fair site-label bits and six fair pair-index
bits, then compute b=kappa_j.X mod4 from the FINE site X, its type and
real sign, and reversibly return the lookup scratch. The64 original
cosine/sine pairs have values0,+1,-1. At L4 the full coefficients
are0,+1/128,-1/128. This fixed finite Boolean lookup has the same owned
raw expansion9.1 at every finite L. A different refinement that reads
coarse site bits is not identified with these Fourier frequencies.
No equality of their full off-diagonal references or physical interlevel
map is claimed. This supplies one permitted original reference subfamily;
it does not convert an arbitrary previous unknown reference.

The paid-writer raw expansion starts from computational blanks. Its
2G+3CX parity source has, on its unmeasured flag c0=1,

    Pi_c0=1 R_plus|000>
             =sqrt(2p^3) |+> |1> |1>,   p+p^2=1.     (150)

Use that actual c0 in7c's one-G/three-fanout-CX/one-CX(c0,bit0)
material seed preparation. It gives exactly sqrt(p)|1>+p|14> on
c0=1. The complete c0=0 columns remain in the raw word. Expand every
logical H/Boolean/phase gate of the F-source through the OWNED finite
raw G/CX construction9.1. Include a fresh actual plus resource for
every H, all copied syndrome flags and corrections, and run every
subsequent raw gate also on failed columns. Nothing is measured inside
this source and no failed transcript is replaced by an abort state.

Each successful fine factory transcript is a scalar times the SAME
logical isometry, also on externally entangled inputs. Thus its coherent
all-READY component factorizes. After the actual7c material rotations,

    Pi_READY R_seed,mat|blank>
        =sqrt(gamma_seed) C(alpha,beta) tensor eta_seed,
    C(alpha,beta)=sum_x |x> m_x(alpha,beta) chi_x,
    ||eta_seed||=1,   D_alpha,beta gamma_seed=0.         (151)

The raw fixed resource work eta_seed is retained. On a finite common
catalogue, the material setting is written once and its original
all-column rotation words are executed; their unused control sector
is still part of the operator. Distinct banks are regenerated by these
actual calls on disjoint fresh work, not copied from an unknown state.
The original immutable oldRIGHT stays separate from the fresh128-mode
purifiers of these banks.

The actual success factor is the joint readiness of the literal word.
For one-attempt building blocks its factors include s0=2p^3 for the
parity resource, s2=4p^3 for the owned CZ/X-success component and
s3=16p^9 for CCZ, with the actual repetitions and extra acceptance bits.
Count a shared root c0 resource ONCE and then the conditional products;
do not charge its probability again for every use. Literal lookup,
pointer-copy, inactive-control, storage and routing operations count
in the real n_G,n_CX and clock. No numeric total is inferred from the
number of logical fair bits alone.

For all banks and the actual selector/encoder, include their success
flags in the same final READY test. Let gamma_N>0 denote that actual
JOINT factor, including seed readiness. On the declared source chart
it is field independent. The full raw source, its failed columns and
its actual inverse are now inside V of(145), not external preparation:

    B_N=H_ref(N_clock,D_full)+j_K(gamma_N q_N).          (152)

The exact raw reverse uses7j's source-X/port/spin/routing interface.
This consumes an owned physical IMPLEMENTATION premise; that selective
source placement is not proved compulsory by naming its matrix.
For a varying gamma_N, the additional source is
j'_K(gamma_N q_N) q_N Dgamma_N. Equation(152) keeps that row.

### The collective first conditional now acts on actual CAR states

Fix the true boundary collar and the downstream geometric/control
channel. Each material raw SIGN occurrence reads ONE A_(x,a) of(142)
from one complete fresh CAR/site/RIGHT bank. The subsequent effect is
diagonal on SIGN and ignores the retained matter work. Pulling it back
therefore gives an operator K on k banks whose one-slot alphabet is
I,A_(x,a), identity on the complete RIGHT factor. A bank is used once;
repeated occurrences of one coordinate use different banks. This is
the missing operator-alphabet premise of the owned collective theorem.
It follows from the all-reference EFFECT(144), not from replacing a
CAR density by a list of measured means.

Use that theorem's coherent without-replacement injection into N>=k
complete banks, with all labels, unsuccessful factory work and unused
banks retained. Its ideal normalized effect is

    K_N=1/(N)_k sum_injections iota K_iota,
    q=<C^tensor k,K C^tensor k>
                     =<C^tensor N,K_N C^tensor N>.

This average is a weight of alternatives, not a probability1/(N)_k
of successful execution. The actual selector is included inside the
same full raw echo, with its own readiness and finite implementation
error below. The total fresh RIGHT carrier is128^N; it is not one
original RIGHT register used N times.

Let s_a=Tr(rho A_a), rho=Tr_RIGHT |C><C|, and g_a=partial_(s_a)q,
summing EVERY raw occurrence of the same material coordinate. The first
conditional of the symmetrized k-bank effect is exactly

    E1=q I+(1/k) sum_a g_a(A_a-s_a I).                 (153)

To verify the application, expand K in its one-slot alphabet and
contract all but one slot against rho. Each remaining monomial is
linear in that slot's A_a. Summing its k possible retained positions
gives the ordinary derivative of the same polynomial q(s); its scalar
part is fixed by Tr(rho E1)=q. This identity is on the ENTIRE original
CAR/site space, with identity on RIGHT, rather than only the original
four-grade input section.

Only FREE material moments belong in(153) when using an interior Euler
root. In this application the fixed-collar values enter the processor
as the actual task's fixed coefficients, with their real finite-code
errors. If an implementation instead READS independently varying
collar A_a, its corresponding g_a is a boundary reaction and must
remain. An interior root does not annul that larger first conditional.

### The true CAR covariance is uniformly positive in its physical material coordinates

Here the covariance is NOT the independent sign-bit covariance of the
older kind-input theorem. For the actual state(3), with arbitrary
retained original chi_x, write psi_x=(psi_0,x,psi_4,x), w_x=||chi_x||^2.
The normalized F-source has sum_x w_x=1 and w_x=1/S. Direct contraction
gives

    s_x=2 sqrt(p) w_x psi_x,
    C_mat=blockdiag_x w_x(p I_2+psi_x psi_x^T)-s s^T.   (154)

Indeed A_xa A_yb=0 for x!=y; at one site its real expectation is
w_x(p delta_ab+psi_xa psi_xb). The original RIGHT coherences have
not been replaced: all these operators act as identity on that factor.

For any real covector g define A=sum_x w_x||g_x||^2,
D=sum_x w_x(psi_x.g_x)^2 and z=sum_x w_x psi_x.g_x.
On the original material disk ||psi_x||^2<=p^2, one has
D<=p^2 A, z^2<=D, and g^T C_mat g=p A+D-4p z^2. Therefore

    p^6 sum_x w_x||g_x||^2 <= G^2:=g^T C_mat g
                          <=sum_x w_x||g_x||^2,
    p^6=5-8p=9-4sqrt(5)>0.                            (155)

For the lower bound use p A-(4p-1)D and p+p^2=1;
for the upper use p A+D<=A. The argument also holds for a free-site
subset with sum_free w_x<=1. In actual matter-source units it reads

    p^6/(4p) sum_x ||D_psi_x q||^2/w_x <= G^2
                         <=1/(4p) sum_x ||D_psi_x q||^2/w_x.       (156)

Thus the SAME original material Euler source controls the first
conditional on the true native carrier, including its actual spatial
weights. At a genuine ideal free-material root g=0, (153) gives E1=qI
as a FULL operator. Every one-bank pure-preparation normal then has
zero first source, including directions outside the four-grade section.
The base state remains that section; the perturbation space is not
silently restricted to it. The present approximate Bernstein report
has its actual g and(146)/(149) error; g=0 is not asserted for it.

### Consume the owned overlap estimate with the actual complete Book gain

At the IID pure bank base Psi_N=C^tensor N, let B_osc=||K-bI|| and
use the actual weak effect bound B_osc<=tau Xi. The already proved
overlap estimate gives, now with the native covariance(154),

    G <=sqrt(N)||(K_N-q)Psi_N||
      <=sqrt[G^2+B_osc^2 k^2(k-1)^2/(2(N-1))].         (157)

This concerns all correlated normalized PURE preparation tangents AT
that IID base. It is not a claim about arbitrary correlated base states
or one-sided mixed-density cone stationarity. Keep the original Gram
constraints and physical tangent norm. At fixed downstream channel and
readiness, the exact pure-bank covector norm is
2 beta_N||(K_N-q)Psi_N||, where

    beta_N=j'_K(gamma_N q) gamma_N>0,
    Gamma_N=beta_N a0 tau/Omega.

Consequently define E_CAR=Omega G/(a0 tau) and
Q_CAR=sqrt(N)||D_bank B_N||/(2 Gamma_N). Equations(152),(157) give

    E_CAR <= Q_CAR
       <=sqrt[E_CAR^2+C_h^2/(N-1)],
    C_h=Omega Xi k(k-1)/(sqrt(2) a0).                  (158)

The actual seed/selector readiness and Book-return factor occur ONCE
in Gamma_N. The normalized-bank bound introduces no inverse readiness or weak-tau
loss; the actual physical lift in(159) must still be bounded. At an
ideal material root the ordinary unit-sphere source is O(1/N) at fixed
h,k; the scaled Q_CAR is O(1/sqrt(N)). At a nonroot its nonzero material
source survives the sqrt(N) scaling, by(155)-(158).

For any actual admitted correlated bank tangent with NORMALIZED
conditional-bank speed L_N,

    |D_bank B_N[v]|/Gamma_N
       <=2L_N/sqrt(N) sqrt[E_CAR^2+C_h^2/(N-1)].        (159)

This speed is ||D(C_bank,N)[v]|| after the actual fixed-success-channel
pullback. It is not automatically the norm of the full RAW prepared-state
derivative. If only a raw derivative norm L_raw is known, projecting its
ready component gives at best L_N<=L_raw/sqrt(gamma_seed,N) at fixed
readiness and success isometry; moving source/isometry terms are additional.
A direct bound through the actual repeated preparation word can be better,
but it must be proved. An arbitrarily fast conditional lift or an inverse
readiness factor cannot be hidden inside O(1/N).
In particular L_N=O(sqrt(N)) and vanishing E_CAR,C_h/sqrt(N)
suffice for this normalized source to vanish. The real h-dependent
copy count k, covariance weights and test/lift norm remain.

The ideal W/exact-selector comparison is not a new finite gate axiom.
At the sharp-control source inputs, let the actual implemented material
effect obey ||K_impl-K||<=tau epsilon_op. The fixed identity part
cancels under trace-preserving extractor/selector channels. Telescoping
raw extractor errors and selector-state errors supplies this weak
bound, with their actual k-dependent constants. Since both q and the
centered vector can move, the actual scaled Q in(158) has additional
debt at most2 Omega sqrt(N) epsilon_op/a0, with its ACTUAL gain.
Choose precision after k,N and the actual tangent bound; keep the
original finite-code/secant error(149) too. No fixed finite constant
word becomes an exact arbitrary rotation or selector.

### What has actually been substituted in the nonvacuum argument

The Fourier128 source now supplies7o's previously external known fresh
seed for the explicitly owned real reference subfamily. The full echo
prices its entire failed complement. Equations(153)-(159) then supply
an actual-CAR bank-preparation source bound and converse, rather than
an assumption that the two material equations exhaust arbitrary pure
CAR-preparation variations. They can be inserted directly into the
independent-input source budget of(129). On the approximate reporter,
use its true E_CAR, implementation errors and actual L_N; an ideal
primary root is only the comparison input.

The physical source budget uses this actual conditional-bank lift,
including any readiness amplification; the abstract unit-sphere norm in
(158) alone is not a full-raw-input source estimate.

The proof holds the downstream seed-flag/readiness/encoder/clock channel
fixed. Arbitrary RAW factory-work, success-amplitude or controller
variations are different directions: q Dgamma_N and the other rows of
(79)/(84)/(86) still apply. Generated-state rows use the owned causal
adjoint, while independently admitted source/control rows retain their
full equations. Physical source-X/query/placement/task admission and
an endogenous configuration map into the actual Book X_N, with its
compatible joint stationary spatial refinement, remain open. This
result does not claim finite all-Euler stationarity, a selected field
minimum, positive_gr, GR_closed or raw216 closure.


## 7q. Supply the actual conditional material lift in the collective source budget

24 October 2026. Same owner; inputa1fbb785. This applies the ACTUALLY
executed coherent factorization(151) to the open speed L_N in(159).
It neither replaces the exact reference by an approximate deterministic
seed nor assumes a generic success projection has bounded inverse.
The consumed parent is the material/input COMPONENT of the source
budget(129), not the missing physical configuration domain X_N.

### The original normalized material section fixes its own lift norm

Keep the same real reference chi_x, fixed weights w_x and genuine fixed
collar. Let v_x=Dpsi_x be a real material variation on the original disk,
and write d_x=sqrt(p^2-||psi_x||^2)>0. Equation(3) gives exactly

    Dm_x=v_x0 |0>+v_x4 |15>-(psi_x.v_x)/d_x |14>,
    <m_x,Dm_x>=0,
    ||DC[v]||^2=sum_x w_x[||v_x||^2+(psi_x.v_x)^2/d_x^2].            (160)

Here the clock grade has its unchanged coefficient sqrt(p), the grade14
normalization derivative is retained, and the original full16 CAR and
RIGHT factors remain in C. Orthogonal site labels remove cross-site
terms; no reference decoherence or deletion of other grades is used.
On the fixed compact material chart d_x>=d_min>0, define
||v||_w^2=sum_x w_x||v_x||^2. Since d_x^2+||psi_x||^2=p^2,

    ||DC[v]||<=p/d_min ||v||_w,
    <C,DC[v]>=0.                                      (161)

The second equality is a REAL equality on this actual section, stronger
than only Re<C,DC>=0. This matters for the tensor norm below.

At each material setting the actual factorization(151) supplies the
normalized CAR bank C(psi)^tensor N to the SAME report effect, which
ignores the remaining source work. Readiness is field independent on
this common catalogue. Differentiating this conditional BANK map,
rather than applying a generic inverse projection, proves

    L_N[v]^2=||D(C^tensor N)[v]||^2
            =N ||DC[v]||^2
            <=N p^2/d_min^2 ||v||_w^2.                (162)

All cross terms contain <C,DC> and vanish. The N real copies are counted;
the bound is not a free-copy or independent-material-setting assumption.
The same primitive material setting is executed in every fresh call.
The scalar seed success factor multiplies the raw successful component
but is constant in these directions. The KNOWN endpoint/source
factorizations(151)-(152) recover(162) as the bank lift exactly. Different
programme/key work states eta_+,eta_- need not be equal or differentiable
across settings; this calculation does not give their full-state norm. No norm estimate that replaces
this map by the inverse of an arbitrary raw projection is invoked.

### Use the computed speed in the complete physical source component

Substitute(162) into the SAME whole-Book bound(159), with the actual
Gamma_N including every seed/selector/encoder readiness:

    |D_bank B_N[v]|/Gamma_N
      <=(2p/d_min)||v||_w
                      sqrt[E_CAR^2+C_h^2/(N-1)].       (163)

This is an actual bound for the shared-material direction through the
supplied repeated source word, not only an abstract unit-sphere bound.
It retains the real material slack, spatial weights, downstream effect,
clock and all additional first-source debts. The ordinary raw field
source has not been redefined by dropping its preparation.

If E_CAR,h->0, C_h/sqrt(N_h-1)->0 and the actual implementation/secant
errors of7p vanish in this same lifted norm, this material bank component
vanishes on bounded ||v_h||_w tests. At an ideal material root the
right side is bounded by2p C_h||v||_w/(d_min sqrt(N-1)); an approximate
Bernstein report keeps its actual nonzero E_CAR. No new finite root,
full stationary execution or mesh-uniform gate-count estimate follows.
### Finite paid material words obey the same tensor secant estimate

Let C_+,C_- be any two actual normalized real material sections of7c
on the SAME seed/reference. Their overlap is

    r=<C_+,C_->
      =sum_x w_x[p+psi_+,x.psi_-,x+d_+,x d_-,x],
    p^3=p-p^2<=r<=1.                                  (164)

The lower bound uses that (psi_x,d_x) has length p; the upper bound
uses normalization. Consequently, for EVERY finite N,

    ||C_+^tensor N-C_-^tensor N||^2
        =2(1-r^N)<=2N(1-r)=N||C_+-C_-||^2.            (165)

Thus the original equal-inventory paid central comparisons, with their
actual attainable angle step delta, have conditional-bank secant speed
at most sqrt(N) times the true one-bank secant speed. The real angle to
material Jacobian(33), its center discrepancy and(149)'s endpoint and
central remainders are retained. Choose the stencil/precision after
h,N and its actual derivative constants; no uniform interchange of
limits has been assumed.

These are CONDITIONAL BANK vectors. Complete retained raw endpoints
can have different orthogonal sharp programme/key records; their full
norms need not obey(165) or approach each other. The actual price/source
transport uses the proved equal-inventory divided-difference identity
(147)-(149), not a false differentiable finite-word or full-raw-state
map. Those code, flag, clock and independently changing control sources
remain in their original equations.

### Source-safe post-seed CAR interventions have a direct norm too

There is another concrete class of source tests for(159). Insert an
actually supplied real unitary T(theta) on the regenerated CAR/site
banks AFTER seed preparation and BEFORE the fixed selector/report.
Take T(0)=I and evaluate its source at theta=0, the original IID base;
(157)-(159) do not control a finitely moved correlated base.
It does not act on seed READY flags or any fresh/immutable RIGHT.
On the declared source interface it therefore preserves readiness and
the original reference Gram, including on entangled bank inputs.
Its actual full word and raw inverse are included in V; the new actual
clock and entire thermal complement are retained in(152).

For its normalized conditional bank state, with H=T^dagger Dtheta T,

    H^dagger=-H,
    L_N[partial_theta]=||H C^tensor N||<=||H||.         (166)

For real one-bank generators H_j on DISTINCT banks at the product base,
<C,H_j C>=0, so instead
L_N^2=sum_j||H_j C||^2. A genuinely entangling generator uses its actual
operator norm in(166); locality or a small norm is not assumed.
For a complete supplied actuator word, product differentiation bounds
that norm by the sum of its actual generator speeds, or by the true
control-to-operator Jacobian. This keeps its real control count.

The existing Golden/CNOT plane construction supplies paid finite secant
versions on its addressed active sector. The physical source-X inverse
reverses the implemented word exactly, while all approximation, routing
and common-inventory requirements remain. Matrix SO closure alone does
not supply arbitrary physical access or a smooth finite-word controller.
Under THESE source-preserving interventions, the additional q Dgamma_N
term is exactly zero; no general readiness-normal equation is asserted.
At an ideal root, (159),(166) bound a fixed-norm entangling bank direction
by O(1/N). All correlated pure-bank directions remain subject to their
actual admissible actuator/lift norm; no mixed-density or arbitrary
raw-work stationarity has been added.

For the original uniform source w_x=1/S, ||v||_w is its true normalized
site norm, not the unweighted sum over S sites. More explicitly let
M_h=sup_(||v||_test<=1)||Dpsi_h[v]||_w for the ACTUAL sampling and
calibration map. The contribution to the continuum budget(129) is
bounded by

    [2p M_h/(d_min,h c_quad,h)]
                   sqrt[E_CAR,h^2+C_h^2/(N_h-1)],                 (167)

plus its genuine implementation/secant debts in the same norm. At fixed
h these constants are finite on the stated chart: after computing
M_h,d_min,h,k_h and the approximation error, choose N_h for this actual
budget. If M_h already includes a sampling/test Jacobian, do not apply
it twice. No uniform bound on M_h, native cost or source gain is inferred.

### The remaining physical transition is separate and now explicit

Equations(160)-(166) fill the conditional material lift which7p left
open: shared original material code comparisons have the actual sqrt(N)
speed, and source-preserving post-seed bank interventions have their
real generator norm. These estimates use the existing exact seed;
there is no Fourier-Gram approximation or inverse-readiness penalty
for these named directions. They do not extend to a moving seed
isometry, source flags, independently changing encoder or clock.

The full geometric/query domain is still an input. Book03 names
stationarity on X_N without an execution-to-X_N variable map; its
rank variation alone does not define independent original coframe and
proper-link directions. The already owned incidence embedding cannot
by itself supply that map. A source-local original field-to-query
interaction, its actual admissible tangents and complete selected
source remain the next physical parent substitution. This result
neither inserts that missing law nor promotes positive_gr, GR_closed
or raw216 closure.


## 7r. Compile the original moving Julia query channel from native coordinate programmes

24 October 2026. Same owner; input336d6aab. The changed input is the
existing regenerated coordinate/moment programme together with the full
raw inverse and complete-Book conjugacy of7j/p. The target is the ORIGINAL
Julia operation(5) of the full-Lorentz source, acting on arbitrary unknown
DATA and its oldRIGHT. This constructs a query ACTION from the coordinate
programmes, rather than assuming a moving Julia gate. The preparation and
physical selection of those programmes keep their existing hypotheses.

The earlier exact finite programming obstruction is preserved. The new
finite processor has an approximation parameter, genuinely fresh programme
banks and controlled channel/source errors. It is not an exact replacement
of the old all-column Julia/full128 operator or its thermal action.

### One programme coordinate produces a controlled rotation channel

Let Y be a fixed real skew target generator, ||Y||<=1, and theta a fixed
real constant. For EVERY elementary use prepare a fresh programme bit z
with actual diagonal mean s=Tr(rho_prog Z), |s|<=1. It can be mixed or
entangled with its own retained work; no pure square-root programme is
required. Complete programme banks must be independent of DATA/oldRIGHT
and of one another, conditional on the same sharp field setting.
Execute

    W_j=exp[(theta/m) Y tensor Z_j],   j=1,...,m.        (168)

Keep every programme bit and its purifier. Each coupling preserves Z_j.
Tracing them only for the logical comparison gives the target channel

    Phi_(m,s)=T_s^m,
    T_s=cosh(A/m)+s sinh(A/m),   A=theta ad_Y,
    Psi_s=exp(s A)=Ad_(exp(theta s Y)).                 (169)

No physical trace, measurement or reset occurs between the couplings.
The target can be entangled with an arbitrary reference: use diamond
norms throughout, so this includes original oldRIGHT. The logical
comparison ignores the retained programme work, which remains in the
actual complete word and price.

Here are quantitative source jets, uniform on the CLOSED interval |s|<=1.
Put a=||A||_diamond<=2|theta|||Y||. For m>=2,

    ||Phi-Psi||_diamond <=a^2/(2m),
    ||partial_s(Phi-Psi)||_diamond <=(a^2+a^3/2)/m,
    ||partial_s^2(Phi-Psi)||_diamond
                                  <=(a^2+2a^3+a^4/2)/m.            (170)

For proof let U_s=exp(sA/m), B=sinh(A/m). T_s and U_s are CPTP,
with diamond norm one. Taylor about the mean of z=+/-1 gives
||T_s-U_s||<=a^2(1-s^2)/(2m^2). Also
B=(1/2)int_(-1)^1 (A/m)exp(tA/m)dt, so
||B-(A/m)U_s||<=a^2(1+s^2)/(2m^2), ||B||<=a/m.
These estimates use norm-one unitary channels along the real integral,
not an unproved inverse bound near s=+/-1. Since all maps are functions
of A, partial_s^j T_s^m=(m)_j B^j T_s^(m-j), j=0,1,2.
CPTP telescoping gives the first two estimates. For the second derivative,
write D=(A/m)U_s and split
m(m-1)[(B^2-D^2)T_s^(m-2)+D^2(T_s^(m-2)-U_s^(m-2))]
-m D^2 U_s^(m-2).
Its norm is at most
2a^3(m-1)/m^2+a^4(m-1)(m-2)/(2m^3)+a^2/m,
which proves(170). These bounds include genuinely controlled Givens
with eigenvalues0,+i,-i and the actual gaps0,+/-1,+/-2.

An uncontrolled DATA-channel bound is insufficient for coherent SELECT:
Ad_U=Ad_(-U), while controlled-U and controlled-(-U) are distinguishable.
For every controlled query below use Y=|1><1|_algorithm tensor Y_plane
and apply(168)-(170) on the ENTIRE algorithm-control/DATA register.
Thus the bound preserves its interference as well as oldRIGHT.

### The small sign-controlled interaction is a literal native word

The constant interaction(168) is not a new primitive. Consume7c's
commuting plane construction. On n target bits, K=2^(n-1), it supplies
CNOT words Q_b with Q_b G_0^k Q_b^dagger=exp(k theta0 W_b),
[W_b,W_c]=0 and sum_b W_b=K J_(0,a). Here theta0 is the ORIGINAL
Golden angle, and J_(0,a)=|a><0|-|0><a|. The programme bit z lies
outside those target bits. Insert its two CNOTs in each factor:

    P_k(z)=X^x product_b
       [Q_b CX(z,0) G_0^k CX(z,0) Q_b^dagger] X^x
       =exp[Kk theta0 J_(x,x+a) tensor Z_z]            (171)

on the actual sharp known-one sector c0=1. The translations X^x are
exactly7c's paid CX(c0,bit) words. On c0=0 the literal untranslated
plane remains, rather than a silently removed identity block.
Equation(171) follows from XG^kX=G^(-k), the commuting W_b and their
sum. The programme bit is preserved EXACTLY on both z columns.
For each use its real inventory is
Kk Golden gates and K(2l_M+n+1)+2|x| CNOTs, before preparation,
routing, flags and the complete inverse. Every inactive control is paid.

The original irrational-angle owner makes K theta0/(2pi) irrational.
Choose positive k and integer l ONCE at the desired accuracy, with
alpha_eff=Kk theta0-2pi l close to theta/m. The implemented conditional
structure is exact at that native angle. Set theta_m=m alpha_eff and
Delta_a<=2m|alpha_eff-theta/m|||Y||. With
R=max(||theta_m ad_Y||,||theta ad_Y||), the ideal-angle mismatch in
channel jets j=0,1,2 is bounded by
Delta_a times respectively1,1+R,2R+R^2. Add this to(170) evaluated at
theta_m. In particular per-use angle precision O(m^-2) gives overall
O(m^-1). Keep its actual finite integer k and full clock cost; no
uniform complexity or free continuously variable native rotation is
asserted. Algorithm control is implemented by including its0/1 label
in the target plane addresses, not by assuming controlled-G.

### The original strict Julia matrix has an explicit analytic generator

Use the original REAL full16 contraction X(Y), ||X||<=kappa<1, on a
fixed compact regular field/programme chart. It contains the true
coframe and proper-link coordinates and any genuinely moving frame,
Gram or density inputs; those augmented jets must not be frozen.
The prescribed Julia matrix is
J(X)=[[X,sqrt(I-XX^T)],[sqrt(I-X^TX),-X^T]].
There is a global analytic formula on this strict contraction window:

    f(z)=arcsin(sqrt(z))/sqrt(z),   f(0)=1,
    T(X)=X f(X^T X),
    B(X)=[[0,-T(X)^T],[T(X),0]],
    S=[[0,I_16],[I_16,0]],   J(X)=S exp B(X).           (172)

For verification only, take a singular-value decomposition of X.
Then T has the same left/right factors with singular values arcsin(sigma),
and exp B has blocks sqrt(I-X^TX),-X^T,X,sqrt(I-XX^T).
Multiplication by S gives the original J. The processor does NOT execute
a singular-vector catalogue or a supplied logarithm. It uses the series
f(z)=sum_(r>=0) binom(2r,r)z^r/[4^r(2r+1)], which and its matrix/field
first two derivatives converge uniformly for ||X||<=kappa<1.

B(X) is the sum of256 FIXED cross-block skew planes with real analytic
coefficient functions b_l(Y)=T_ij(X(Y)). Choose fixed bounds B_l>0
strictly larger than sup|b_l| on the actual chart. One explicit uniform
choice is B_l=2, since ||T(X)||<=arcsin(kappa)<pi/2<2. This is a
programme-coordinate bound; theta s still equals the prescribed target
coefficient and no action coefficient is fitted. The owned fixed
coordinate/Bernstein/row processor of7h-o can produce programme SIGN
means s_l(Y) approximating b_l(Y)/B_l with their first two source jets.
Its coefficient rounding, range extension, source weights and real
field-to-coordinate Jacobian remain in that approximation error.
The tables derive from the ORIGINAL prescribed X-to-J function(172),
not from a desired Einstein output law.

At finite native code settings these are regenerated paid programmes;
the C2 functions are their declared smooth comparison section and the
old finite-code/secant obligations remain. A single unknown field or
programme specimen cannot supply extra copies. If the actual coordinate
banks or their repeatable source are unavailable, this construction does
not manufacture them. It consumes their already owned explicit source.

Use a product formula for exp(sum_l b_l Y_l), with each factor's
coefficient obtained from its own programme mean and(168)-(171).
Fix the original outer query algorithm, call count M and actual field
window BEFORE taking these inner implementation limits. Only afterwards
choose a diagonal sequence of outer accuracies or meshes, retaining all
its actual constants. At each finite time slice, all gates, lookup tables
and integer powers
are fixed for the ENTIRE field window. Only the regenerated programme
states change with the native field setting. First choose the analytic
coefficient/row approximation, then the fixed product-formula depth,
then programme count and native angle precision. Finite Taylor/product
rules and(170) give convergence with both field jets on that compact
chart. Constants retain kappa, actual coefficient/field derivatives,
plane count and circuit depth. No claim is made for unbounded boosts.

The fixed S is X on the Julia coefficient bit. Its controlled version
is exactly CX(algorithm,coefficient); its unconditioned version uses the
actual known-one control. Thus this construction supplies CONTROLLED
J(X) on arbitrary target inputs as well. A logical J^dagger request
uses its own fresh programmes for exp(-B)S. It does not reverse the
programme work of a preceding logical J call.

### Compare the entire logical network, then price its actual full word

Fix one of the original finite coherent query networks consumed by7n.
Replace EVERY J/J^dagger/controlled-query occurrence by the processor
above, using fresh complete programme banks even for consecutive calls.
Its reduced channel on all logical registers approaches that same ideal
network with C2 source jets. The new programme/seed garbage is retained
but not read or reused by subsequent logical gates or final READY/report.
Genuine source/factory success flags DO remain in READY; they are not
confused with irrelevant quantum garbage. Already measured history is
not erased, deferred anew or placed inside an unavailable inverse.

For clarity, an explicit first-jet composition budget suffices for the
field source. Suppose there are M query calls, each reduced channel
error bounded by epsilon0 and first field-jet error by epsilon1 in
the chosen diamond/operator norm. Let L bound the first jets of BOTH
actual and ideal calls, and B_in the trace-norm jet of the actual common
input state. Fixed intervening unitaries add no derivative. Hybrid
CPTP telescoping gives

    e0<=M epsilon0,
    e1<=M epsilon1+M epsilon0[B_in+(M-1)L].             (173)

Here e1 bounds the derivative of the REDUCED final logical density.
For heterogeneous calls use their actual summed bounds; coefficient
bias, product-formula, native-angle and finite-code errors are included.
Second-jet convergence follows by the same finite product rule, retaining
second channel and input jets. A growing M or field-test norm must not
be absorbed into a fixed O(1/m) constant.

Let V_m be the ENTIRE actually executed forward word, including every
programme source, interaction, logical inverse simulation, failure column
and raw flag. In7n retain its exact full-register parking(136); source
programmes do not use protected oldRIGHT or stored unknown DATA as scratch.
The closing Book echo uses V_m^dagger on the SAME registers.
It is obtained by7j's physical reverse of the raw G/CX list, with all
source-X/routing requirements and its new clock counted. A fresh-bank
approximate inverse CHANNEL is not that closing inverse.
Consequently U_m=V_m^dagger M0 V_m has the exact full spectrum required
by the balanced-return theorem, independently of its logical error.
The actual complete price is

    B_m=H_ref(N_m,D_full)+j_K(gamma_m q_m).

All programme/garbage dimensions and failed columns remain in H_ref.
This is the price of this actual expanded execution; it is not the old
unmodified spatial/full128 HJR action.

Use the ORIGINAL weak final effect E_tau=bI+tau T, ||T||<=Xi, on the
logical registers, tensor identity on new programme garbage. If rho_m
and rho_0 are actual and ideal REDUCED normalized logical states, then

    D(q_m-q_0)=tau Tr[T D(rho_m-rho_0)],
    Gamma_m=j'_K(gamma_m q_m)gamma_m a0 tau/Omega,
    ||DB_m/Gamma_m-Omega Dq_0/(a0 tau)||
                                    <=(Omega Xi/a0)e1.             (174)

Gamma_m is the ACTUAL gain on the positive-return chart; all seed and
factory readiness occurs once. Trace preservation cancels the identity
part, giving no inverse tau or readiness loss. The actual programme
source/coordinate Jacobian and physical test norm enter e1, not a free
external derivative. Moving gamma, rank, cut, input, middle or clock
retains its own source. Any other selected Info/work/stack contribution
needs its actual first-source binding as before.

Add(174) to the existing error in(124), then use(129) with its actual
sampling lift and c_quad,h. Programme counts and native precision can
be chosen after the finite network and its true field/source norm are
fixed. This is a concrete replacement of the supplied moving query
CHANNEL in that consumer; it does not re-run geometric roots or change
the original Palatini/CAR comparator.

### Hostile controls fix the scope of the new substitution

Using one programme bit m times instead of fresh bits yields the mixture
[(1+s)/2]Ad_(exp(theta Y))+[(1-s)/2]Ad_(exp(-theta Y)), not the limit
in(169). At s=0 this generally differs from the identity target channel.
Fresh regenerated copies are an actual load-bearing requirement.

Reduced C2 convergence does not imply retained joint C1 convergence.
For a real two-dimensional rotation, DATA |0> and pure programmes
beta(s)^tensor m, beta(s)=(sqrt((1+s)/2),sqrt((1-s)/2)), compare the
actual full state with exp(theta sY)|0> tensor beta(s)^tensor m.
At s=0, put h=theta/m. Their joint state-error squared and joint
first-derivative-error squared are respectively

    2[1-cos(h)^m] ->0,
    theta^2+(m/2)[1-cos(h)^m]
      +m(m-1)sin(h)^2 cos(h)^(m-2)/2
      -theta m sin(h)cos(h)^(m-1) ->3theta^2/4.         (175)

Thus the full retained-state e1 premise of(140) is NOT supplied by
this query simulator. Equation(174) uses its separately proved reduced
channel jet and the effect's genuine blindness to new garbage.
Likewise reduced-query approximation does not supply the old all-column
Julia/reflection identities(103)-(109), an identical marked full future
profile or equality of the old spatial thermal operators. Those original
exact owners retain their independent scope.

What is removed is the extra unknown-input moving-query ACTION on the
supplied native coordinate-programme interface. This is stronger than
the earlier coordinate-to-report effect writer and opposite to8.6's
query-to-coordinate compiler: it acts on arbitrary unknown target and
oldRIGHT with controlled source errors. The native origin/selection
of the field programme, its independently admitted control/seed/cut
variations and the map to actual Book X_N remain separate physical
premises. No complete stationary refinement, physical GR, positive_gr
or raw216 closure is claimed.


## 7s. Compose the full query programme with joint input and encoder equations

24 October 2026. Same owner; input5e01fd35. This uses7r's fixed native
query processor, rather than treating each of its coefficient programmes
as an unrelated physical input. The consumers are the independent-input
and implementation terms in the complete source budget(129).

Two applications are distinct. First, pull the WHOLE query/report network
back to one canonical geometry/matter bank and apply the owned collective
source theorem there. Second, identify actual encoder/work directions
which preserve the complete programme-response operators. Neither
application asserts that these exhaust the native Book X_N domain.

### One canonical bank supplies every coefficient programme

At fixed h, chart, actual inventory and approximation accuracy, choose
ONE independent feature for each deduplicated free coordinate. The geometry
features t_j encode the original16 coframe and24 proper-link variables;
the material features are s_(x,a)=2sqrt(p)w_x psi_(x,a) of(142).
All coefficient programmes of(172), direct reports and repeated queries
are computed from these canonical features by the SAME fixed processor.
There is no separately preloaded independent bank for b_l(Y), no second
unlinked encoding of one field, and no later direct read of a field key
outside the source bank. Thus the downstream operator below is field
independent; field dependence enters its input state alone. Logical
WORK starts from the common declared blanks; any independently moving
DATA/input state not carried by this bank keeps its separate source.

Use real pure geometry SIGN states beta(t)=(sqrt((1+t)/2),sqrt((1-t)/2))
in the COMPUTATIONAL Z basis. This is an actual available source on the
dense native code grid, not a new angle gate. The owned equal-inventory
cell W_(L,k) has c0=1 block G^k and c0=0 block G^L, using L forward G
and2L CX for |k|<=L of the same parity. From a blank it prepares exactly
beta(t) when k theta0 modulo2pi lies in(0,pi/2), t=cos(2k theta0).
The existing fixed-parity density and common-catalogue construction cover
all finite endpoints/stencils on a compact interior feature window.
Retain the paid root c0, its full complement and actual raw inverse.
For the material factor use the original real Fourier/CAR source of7p.
The complete normalized conditional bank is

    xi=big_tensor_j beta(t_j) tensor C_psi,
    r=(t,s),   J_r=D_Y r.                             (176)

The real field-to-feature Jacobian is locally invertible on the declared
free42 chart, with its actual inverse-coframe/Cayley/material factors.
Fixed collar data are supplied processor coefficients, as in7p. A
moving frame, Gram, density, clock input or independently read collar
adds another feature/source row; the42 equations do not annul it.

Every RAW feature occurrence in the entire finite7r network is assigned
a DISTINCT complete bank, including all samples used in Bernstein counters
for coefficient programmes and every final report occurrence. One bank is
read in at most ONE coordinate: Z_j on a geometry factor or A_(x,a) on
the full original CAR factor. All other factors/purifiers of that bank
travel with it and remain retained. For k occurrences prepare N>=k
complete banks from fresh work using the same actual source setting.
This counts real copies, reference128^N, code and storage; it does not
clone an unknown input or identify them with original immutable oldRIGHT.

### Read-only raw coordinates give the required operator identity

Consume the ACTUAL Bernstein implementation of paid-writer10.2 and7h
(75)-(76): raw coordinate SIGNs are retained read-only controls of
reversible counters and preprepared-row lookup. They are not targets
of H, swaps with data, or later raw readout reversal inside the FORWARD
word. Programme/algorithm/work bits can interfere quantum mechanically.
For the material moment we can now consume the OWNED exact fixed-pair
readout of NATIVE_POLYNOMIAL_FIRST_JET sections2,5. Write A for the pair
swap with zero complement and R=I-A^2. The two fixed signed permutation
involutions V_+=A+R,V_-=A-R satisfy A=(V_++V_-)/2. A coherent fair
selector and a Hadamard test of its selected FIXED involution give the
raw SIGN effect(I+/-A)/2 on every original CAR/reference input. Expand
all fair/H/Boolean/phase operations by paid-writer9.1, retaining their
input-independent raw success flags, work and physical inverse. Fixed
address/predicate scratch is reversibly uncomputed BEFORE the final
Hadamard interference; retained input-independent factory syndrome work
is not substituted for that scratch return. The whole successful effect
is EXACT; this does not assert that the ideal
constant matrix W_A of(143) is itself an exact finite Golden word.
The raw SIGN is then retained and used only in the control role. Each later7r coupling preserves its
derived programme Z. The closing whole-word inverse is a separate stage.

Hence the entire completed logical word is block diagonal in the raw
SIGN labels: U=sum_z |z><z| tensor U_z. Pulling back the final effect and
compressing each fixed raw readout gives exactly(I+/-A_a)/2, or(I+/-Z_j)/2.
Quantum target/control interference changes U_z and its coefficients,
but cannot create an extra input operator on a slot. The full normalized successful
kernel K therefore has the one-slot alphabet

    I,   Z_j tensor I_material,
         I_geometry tensor A_(x,a),                  (177)

on the ENTIRE geometry-kind/CAR/site/reference bank. This is an operator
identity, including correlated pure bank inputs, rather than equality of
probabilities only on the prepared field section. It uses the new exact
successful readout above. The alternative finite W_A,nu approximation
keeps its actual A_nu and the stated K_impl-K implementation debt. Logical factory success
is input independent on this domain, also for entangled inputs. This uses
its owned all-input Kraus identities and preparing ALL coefficient rows
before live selection. Thus the normalized successful Heisenberg map is
unital: the final weak effect pulls back as K=bI+tau T_K, ||T_K||<=Xi.
Its actual common success factor remains in the physical Book price.

The read-only condition is necessary. If a raw A-readout is followed by
H on its raw SIGN and then reading0, the pulled-back effect is
I/2+P_rest/2 for the extractor(143), outside span{I,A}. Preserving only
the later programme Z would not justify(177). Such an implementation
keeps that additional operator and its own source; it is not covered by
the canonical kernel claim.

Use the OWNED coherent without-replacement injection to average K over
N complete banks. Include its actual labels, flags, lookup work and all
unused banks inside the same full raw echo. Conditional on the genuine
common success, its kernel is K_N=(N)_k^(-1)sum_iota K_iota. On xi^tensor N
it preserves the entire original logical output channel and all its
reported probabilities; different injections see the same k input banks.
The factor1/(N)_k is an alternative weight, not a physical success rate.
The actual additional readiness is counted separately and exactly once.

### All field and cross-bank preparation rows share one source bound

Let q=<xi^tensor k,K xi^tensor k>, g=D_r q, with EVERY repeated raw
use of each feature included in the derivative. The owned first-conditional
formula now applies to the ENTIRE new query programme:

    E1=qI+(1/k)[sum_j g_tj(Z_j-t_j I)
                         +sum_a g_sa(A_a-s_a I)].      (178)

It acts as identity on all unused factors and RIGHT. At the actual product
bank(176), geometry and material covariance cross terms vanish, and

    Sigma=diag(diag_j(1-t_j^2), C_mat),
    G_all^2=g^T Sigma g,
    g=J_r^(-T) D_Y q.                                 (179)

Here C_mat is the TRUE native covariance(154), with its p^6 weighted
lower bound(155), not an assumed independent material-bit covariance.
On compact interior geometry features and positive material weights,
Sigma is positive. Equation(179) gives the actual comparison with the
declared physical field-dual norm through J_r and Sigma; no mesh-uniform
norm bound or replacement of the raw216 norm is inferred.

If the EXACT same comparison kernel has all original free field rows
zero, J_r's invertibility forces g=0, so E1=qI as a FULL bank operator.
The owned primary family supplies the ZERO REFERENCE geometric
covector to(124)/(174); use those inequalities and the actual J_r^(-T)
to bound this kernel's g. Do not assign it that reference root. The
finite7r processor keeps its actual D_Y q and all(124)/(173)/(174) and
finite-code errors. A field root of another price,
redundantly constrained feature curve or read augmented normal does
not imply g=0 here.

The full-variable implication uses only the canonical feature map. If
two independently supplied encodings r1(Y),r2(Y) are BOTH read, then
D_Y q=J1^T g1+J2^T g2=0 need not annul either gradient. Those extra
normal reactions cannot be discarded by calling both encodings the
same field. In(176) every coefficient branch derives from the one
canonical source, instead of imposing such a hidden equality constraint.

Put the ENTIRE source/injection/query/report word and its actual inverse
inside the balanced echo. At its new actual clock and carrier,
B_N=H_ref+j_K(gamma_N q), with all root/factory/injection readiness in
gamma_N once. Define the ACTUAL gain Gamma_N=j'_K(gamma_N q)gamma_N a0 tau/Omega,
and E_all=Omega G_all/(a0 tau). The already proved overlap estimate gives

    E_all <=sqrt(N)||D_bank B_N||/(2 Gamma_N)
       <=sqrt[E_all^2+C_h^2/(N-1)],
    C_h=Omega Xi k(k-1)/(sqrt(2)a0).                   (180)

The derivative norm in(180) is the AMBIENT normalized pure-bank sphere
norm AT the IID base, including correlated geometry/material, extra
exterior grades and retained reference directions. This is not a claim
that its full tangent sphere is physically admitted. Fixed-RIGHT-Gram
or other boundary restrictions inherit its UPPER bound through their
actual lift; the lower bound/converse is not automatically true for a
smaller constrained norm. The same ambient-norm reading applies to
(157)-(158). There is no claim about arbitrary correlated base states
or one-sided mixed-density cone changes. At an exact comparison
root its ordinary bank source is O(1/N); away from it the sqrt(N)-scaled
source retains the nonzero complete field gradient through(179).
Actual implementation effects with ||K_impl-K||<=tau epsilon_op keep
the existing additional2Omega sqrt(N)epsilon_op/a0 debt.

The actual pure conditional source chosen in(176) also supplies the
joint lift, without assuming a fixed purifier for an old mixed packet:

    ||Dxi||^2=sum_j (Dt_j)^2/[4(1-t_j^2)]
           +sum_x w_x[||Dpsi_x||^2+(psi_x.Dpsi_x)^2/d_x^2],
    <xi,Dxi>=0,   L_N^2=N||Dxi||^2.                  (181)

This preparation metric is DISTINCT from Sigma: in particular C_mat
contains the global -ss^T term, while the material term in(181) does
not. Both keep their true field Jacobians. For any declared test v,
(159) becomes2||Dxi[v]||sqrt(E_all^2+C_h^2/(N-1)), plus actual errors.
Use its true sampling/calibration map and c_quad,h in(129), once.
Different raw programme/key histories can be orthogonal; finite field
code comparisons use the actual endpoint price identity(147)-(149),
not a C1 norm claim about those full histories.

For an existing exact curved reference family, one may therefore choose
finite native code points approximating its chart coordinates, then
outer/inner source accuracies as in7r, then N_h for this joint budget.
The local source continuity/Jacobian/slack constants, k_h and test norm
are computed or retained BEFORE choosing each tolerance. This constructs
controlled versions of these FIELD and BANK source components on that
family. It is not an exact native all-Euler root or a proof that other
selected stack components vanish.

### Actual programme-response effects identify neutral encoder directions

There is a complementary application to implementation work. Let A_i be
an ACTUAL finite programme encoder with blank-work isometry i0, programme
bit z_i and genuine success flag R_i. Define its UNNORMALIZED effects
on its whole source-input space:

    F_i^+=i0^dagger A_i^dagger(R_i P_z=0)A_i i0,
    F_i^-=i0^dagger A_i^dagger(R_i P_z=1)A_i i0.        (182)

These are the actual finite catalogue's effects, including rounded
coefficients and raw readiness, rather than an exact continuous mean
function imposed as a new axiom. Fixing them still lets xi(Y) and the
field vary; changing catalogue degree, caps or inventory has its OWN
price/error. The flags commute as the actual computational tests. Encoders use
disjoint source/work factors; programme bits and these flags are not
subsequently altered. A shared root c0 is conditioned ONCE on its actual
prepared support, with its success factor retained once. If encoders
share further work, use the actual JOINT effects instead of multiplying
individual F_i. No factorization of unknown quantum inputs is assumed.

For a single encoder and any source/DATA entangled density rho, its
subsequent fixed native Z-controlled collision has successful reduced
channel

    N_suc(rho)=U_+ Tr_source[(F_i^+ tensor I)rho]U_+^dagger
                +U_- Tr_source[(F_i^- tensor I)rho]U_-^dagger.       (183)

For many fresh encoders the Heisenberg map is the sum over sign strings
of (tensor_i F_i^(sigma_i)) tensor U_sigma^dagger O U_sigma, where
U_sigma is the actual ordered target/algorithm branch with all fixed
interleavings. This fixes algorithm-control coherences and unknown-DATA/
oldRIGHT action AFTER ignoring the retained programme garbage; it does
not fix that garbage or the programme-state coherences themselves. It concerns the ACTUAL
finite processor, not only its ideal unitary-channel limit.

Consequently an implementation tangent with delta F_i^+=delta F_i^-=0
for every component, or the analogous zero joint-effect tangent, has
exactly delta q=0. At fixed actual inventory, cut, middle and other
source data, full-word conjugacy gives delta H_ref=0 and hence

    delta_encoder B_N=0.                              (184)

This includes changes on unused/failure/garbage columns, rather than
requiring delta A_i=0. A concrete native family appends literal CX(z,g), or sector-preserving
G/CX words, on fresh retained garbage g
ignored by R_i. They commute with both flag tests and preserve(182)
exactly. Their work, common-inventory cells and actual inverses count
in the whole word; no costless operation is asserted. Their additional
future distinctions can remain readable even though this Book source
is neutral. This is an actual source fibre, not a claim that the full
future profiles or every physical law agree.

The full effects in(182) are essential. Fixing only normalized mean
allows F_i^+/- ->c F_i^+/-, changing readiness and giving the genuine
source j'_K(gamma_N q)q Dgamma_N. Even with fixed success, equal means
on a selected product/field curve do not generally determine F_i.
For example J=[[0,-1],[1,0]], F=J tensor J is real symmetric, F^2=I.
Effects I4/2 and I4/2+eta F,0<eta<1/2, agree on every real product
state but differ on the Bell+ input. Their unknown-input programme
channels can differ. Even two DIAGONAL effects can agree when repeated
inputs are tied: I4/2+eta(Z1-Z2),0<eta<1/4, agrees with I4/2 at u1=u2, but not
on independently varied input means.

For this sufficient calibration test choose the encoder INPUT interface
AFTER its fixed material-moment readout. On the actual read-only class
the successful compressed F_i^+/- are diagonal in those raw SIGN labels,
even though raw failure columns need not preserve them. Pullback through
the fixed readout gives the corresponding I,A operators on CAR, not
computationally diagonal CAR matrices. Equality of BOTH complete
response laws on an open cube of INDEPENDENT raw-slot means then fixes
the full effects by the multiaffine Walsh polynomial identity. Equality
only on the physical shared-field curve is insufficient. This gives a
usable sufficient correctness test when that input family belongs to
the same supplied task; it does not prove the task is compulsory or
that every physically allowed encoder variation lies in this fibre.
For approximate equality retain delta F, the induced delta q and its
actual gain-normalized source, rather than asserting(184) unchanged.

### The combined source application and its remaining normal

Equations(177)-(181) now control the joint canonical programme input,
including geometry/matter correlations, while(182)-(184) solve the
actual channel-preserving encoder/work directions. Generated programme
states themselves use the existing full causal adjoint. These are
compatible components of the SAME actual expanded Book execution,
with unchanged reference equation and physical source normalization.

Independent changes of F_i^+/- themselves, seed flags, middle, cut,
clock, raw source frame or genuinely read extra coordinates retain
their own complete sources. In particular readiness variation is not
killed by the42 field rows. The remaining physical transition is the
original endogenous configuration/variation map: show that the actual
Book X_N has this generated/task tangent image, or compute the full
source on every extra admitted direction. No selected field minimum,
complete finite stationary solution, physical GR, positive_gr or
raw216 closure is promoted by this joint source result.


## 8. Reproduction

Run from this directory:

    OPENBLAS_NUM_THREADS=1 python check_same_brinkmann_paid_source.py --output /tmp/paid_source.json

The NumPy/SciPy script reconstructs all16 exterior grades, all32 paired Julia factors and their true derivatives; verifies the finite configured source equation and actual midpoint CAR increments; computes the complete two-round port source, all40 column variations and full two material rows; checks the normalized preparation finite difference; reads the same Ricci/Weyl via the covariantly transported probes; and checks the exact parity controls. On the smaller L4 fixture it reconstructs all64 original Walsh controller rows and all128 port maps, and compares the direct two-round conditional-port sum with (5). The latter includes all16384 ordered records by exact contraction, not an independence assumption.

Author replay: Python3.13.5, NumPy2.3.5, SciPy1.17.0. The complete receipt contains the actual source vector and explicit false status flags for unproved physical identifications. This packet adds no BOOK/claim/assembly status or workflow change. Independent scientific review is required before an accepted parent substitution.
