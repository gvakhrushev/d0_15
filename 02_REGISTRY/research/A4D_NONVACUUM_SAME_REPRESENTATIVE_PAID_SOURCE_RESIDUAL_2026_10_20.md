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


## 7t. Construct the executable domain and test an actual native readiness variation

24 October 2026. Same owner; inputcb2f0874. The user directed that an
absent definition be constructed from the repository. We therefore replace
an unspecified execution-membership predicate by the explicit finite
operational sector below, and compute a previously unbound source on it.
This is a construction and an application, not a claim that naming a
domain proves the physical stationary solution. The consumer is7s's
remaining native configuration/variation map and the whole budget(129).

The implementation and independent bounded checks are in
[d0_native_execution_domain_2026-10-24](sources/d0_native_execution_domain_2026-10-24/).
No action, Einstein equation, desired root or fitted source is inserted
into its membership test.

### A finite membership algorithm with literal preparation and inverse

Fix finite integer bounds on qubits and EXPANDED primitive stages. A
code records its register count, initial zero-blank wires, immutable
oldRIGHT wires, chronological primitive list, apparatus profile and final
readout-bit names. Every remaining input wire is an arbitrary protected
input, possibly entangled with the others and oldRIGHT. Preparations of
fresh coordinates, references, flags and keys are gates INSIDE the list;
they are not additional supplied amplitudes. Final readout names do not
authorize a reset or a postselection operation.

The G_CX profile admits precisely addressed positive G and CX letters.
The G_CX_SOURCE_I profile additionally names ONE source port and the
two-bit representation of its original quaternion spin4. Its only extra
primitive is SourceI=diag(I4,L_i) in that same port frame. No individual
G/CX addressing of the spin is admitted. These are the explicit matrices
and availability interface already consumed in7j(94)-(95), not an arbitrary
orthogonal gate set or the distinct full RawZone/regular8 carrier.
Its actual source-local implementation obligation remains the one in7j;
membership does not prove availability from abstract algebra generation.

Reject unknown primitives, invalid/repeated addresses, overlapping port
and spin, any gate touching oldRIGHT, a blank labelled oldRIGHT, and any
resource-bound excess. In particular an oldRIGHT CONTROL is forbidden:
controlled use can change its quantum coherences. Generated coherent
factory flags are not relabelled immutable oldRIGHT; an already measured
history cannot be silently put back inside an inverse.

Call the resulting finite set X_run(b,profile). Its elements are the
parsed finite records, represented by canonical JSON codes; arbitrary
whitespace presentations are not distinct apparatuses. Its predicate is an
algorithm on finite codes, with no numerical tolerance. Finiteness follows
because both wire names and word length are bounded and the primitive
alphabet is finite. Membership, inventory, initial isometry i0 and
P0=i0 i0^dagger are computed directly. In particular

    D_full=2^n,   r0=rank P0=2^(n-number_of_blank_wires).       (185)

The source-spin and all failed/unused columns occur once in D_full;
protected inputs occur in r0 as well. A blank and an unknown input are
different data. The grammar contains no uncharged allocation or idle.
The empty word is an identity boundary code; its N=0 object is not
mistaken for a positive-stage Book clock. The Book action below uses
the nonempty-word subdomain.

Every admitted letter is orthogonal on ALL columns and is identity on
oldRIGHT. Therefore every admitted word has these properties, including
arbitrary input/reference entanglement. For the source-I profile its
inverse is generated mechanically: reverse the list, keep CX, replace
SourceI inverse by THREE SourceI letters, and replace G inverse by
SourceI;SourceI;G;SourceI;SourceI. If G acts away from the source port,
route the WHOLE five-letter block by two SWAPs, SIX additional CX.
All intermediate port/spin work is retained. The expanded inverse must
itself satisfy the actual resource bound. This proves a full-column
inverse, not only the c0=1 column of a heralded word. The G_CX profile
does not receive this inverse macro by definition.

The finite constructors in7p-r supply actual codes of this grammar:
each W_(L,k) source uses integer n_+=(L+k)/2,n_-=(L-k)/2, with
L>=|k| and equal parity; all Bernstein counters and all rows are finite;
fixed readouts expand by the owned factories. Thus each fixed-accuracy
7s programme has a finite resource bound and is an endpoint in this
sector on its declared source-port interface. This is not a continuous
word selector for arbitrary real fields or a compiler for additional
unproved moving geometric operations.

### The actual clock, cut and Book action are functions of the code

For a nonempty expanded word g_0,...,g_(N-1), let W_0=I,
W_j=g_(j-1)...g_0, W=W_N. On the ENTIRE N-stage carrier set

    T=sum_j |j+1 mod N><j| tensor g_j,
    d=(I-T)/sqrt(2),
    Delta_pair=diag(d^dagger d,d d^dagger),
    P_hist=direct_sum_(j<N) W_j P0 W_j^dagger,
    F_hist=P_hist T^dagger(I-P_hist)T P_hist.                (186)

These are the already owned chronological connection Hodge and
transported input-return cut, now generated from one validated code.
The terminal wrap uses the last ACTUAL primitive; an extra uncharged
closing stage is not inserted. Every interior leakage block is zero.
The only remaining block is unitarily equivalent to

    E_W=P0 W^dagger(I-P0)W P0.                            (187)

Indeed an interior g_j maps range(W_j P0) onto range(W_(j+1) P0);
on the wrap its failure to return is exactly(187). Thus F_hist has
rank at most r0, although P_hist has rank N r0. Pair the cut as
diag(P_hist,0) if the return is represented on the paired Hodge carrier.
The other grade then has zero feedback; it still contributes to heat.

The unchanged Book functional on this explicit clock sector is

    B(e)=beta^(-1) log Tr_full exp(-beta Delta_pair)
                 -log det_(range P0)(I-z E_W),
    beta>0, 0<z<1.                                      (188)

All 2 N D_full thermal modes remain. There is no factor N in the
feedback, no division by r0 and no replacement of the full trace by
the selected initial column. Positivity 0<=E_W<=P0 and Delta_pair>=0
make this a finite real price. For fixed computable beta,z it is computable from the code:
matrix entries are algebraic in the positive a with a^4+a^2-1=0;
matrix exponential and positive logarithm have convergent series with
effective finite-dimensional norm bounds. More explicitly the feedback
series sum_(m>=1) z^m Tr(E_W^m)/m has tail at most
r0 z^(M+1)/[(M+1)(1-z)]. Transcendental price comparison is not part
of the syntactic membership decision.

Equation(188) implements the full PAIRED CLOCK Hodge. It is not an
identification of that clock alone with the original spatial scene or
its physical metric. An application using the complete homogeneous
scene-clock operator keeps its actual scene factor and ALL its modes,
as in7j-k. Extra scene, boundary or other selected stack sources are
not set to zero by this definition. Likewise this bootstrap valuation
is not a proof identifying every physical Cost-Info component with it.
The readiness application below uses7j's already proved WHOLE heat
conjugacy, not a clock-only replacement of that action.

Programme storage is included among the ordinary physical registers.
If one actual autonomous word decodes many internally stored keys,
its T and full heat include ALL those key blocks. A sharp input key
does not restrict the thermal trace to its selected block. Different
hardwired words instead describe different operator configurations;
they must not be presented as a free key change of one decoder.

### Actual code changes do not silently become smooth native controls

At fixed layout, profile and input boundary, one can enumerate literal
insertions, deletions and substitutions whose resulting word passes
the same predicate. Equal-inventory comparison is the decidable
subrelation having equal counts of EACH primitive and equal N.
Changed inventory or carrier has its actual absolute price. The
generated intermediate states and prefix cuts in(186) change with
the code; they are not independently frozen matrices.

This supplies concrete finite variations and their exact price
differences. It does not itself produce nonconstant continuous curves
in a finite set. Nor does a finite local minimum imply Euler equality:
it gives inequalities and would generally exclude stationary saddles.
Use Book02's declared finite-difference convention with its actual
endpoints and scale, or prove a consistent source limit. For a supplied
smooth MATRIX comparison the ordinary derivative formula in BOOK_MAP.md
applies, retaining generated-cut derivatives and every genuinely
independent source. That comparison is not asserted to be a native
smooth gate primitive.

Consequently the formerly opaque membership question is now testable
on this operational sector. The next question is substantive: does a
given family satisfy the proposed Book stationarity tests for its
ACTUAL native edits? Merely choosing the semantic fibre in(184) as the
entire domain would omit valid raw-code changes. The following edit
calculates one such row rather than assuming it away.

### An actual resource edit preserves the logical query and changes readiness

Take ONE fresh fair/plus resource in the existing7s processor, in
addition to its existing independent root c0. On three initially blank
bits a,b,c, the chronological word

    G_alpha(a);G_alpha(b);CX(a,c);CX(b,c);CX(a,b)

has exact column

    cos(alpha)^2 |000> +sin(alpha)^2 |100>
       +sin(alpha)cos(alpha)(|011>+|111>).                (189)

Thus its genuine flag c=1 has probability s0(alpha)=2sin^2(alpha)cos^2(alpha),
and conditional resource |+>_a tensor |11>_(b,c), independent of alpha.
No branch is discarded in the actual word. Every later raw gate is
executed on failure too. On success this resource is exactly the one
consumed by the owned H factory, for arbitrary DATA/oldRIGHT input,
not merely for the original geometric field section.

There is NO new variable-angle primitive in this test. Let theta be
the ORIGINAL Golden angle, sin(theta)=p, cos(theta)=sqrt(p). Replace
both displayed G_alpha by the actual W_(L,k) cells controlled by the
existing c0. On c0=1 they give G^k, so alpha=k theta; on c0=0 the
whole G^L complement remains. Each cell has exactly L G and2L CX,
independent of k. All inverse/source/routing letters are generated
as above. Therefore k=1 and k=1+/-2Q share any odd L>=1+2Q,
the same complete carrier, primitive inventory and actual clock LENGTH
within each chosen stencil. The full clock operators T_k themselves
change. Finer stencils generally increase L and N; their
absolute prices are not equated. The owned irrational-angle theorem
supplies Q with G^(2Q) arbitrarily
close to I on either side. These are finite code endpoints approaching
the original source, with a two-sided limit; no finite angle oracle
or equality of different clocks is used.

Use the algebraic raw feature u=cos(2alpha), rather than an externally
assigned pulse derivative. At the original source,

    u0=p-p^2=p^3,
    s0(u)=(1-u^2)/2,
    s0(u0)=2p^3,    (d/du)log s0(u0)=-1/2.             (190)

Every other logical factory and conditional output channel is unchanged.
With their actual remaining success factor gamma_rest, including c0
ONCE, the same forward report therefore has

    gamma(u)=gamma_rest s0(u),
    x(u)=gamma(u) q,        q independent of this edit.    (191)

This statement preserves the normalized query, not the full unnormalized
instrument: readiness is separately readable and genuinely changes.
It is precisely the component not fixed by a normalized correctness
contract. A contract fixing BOTH full F_i effects would prohibit this
edit; that stronger physical constraint has to be justified independently.

Put the complete edited forward word and its actual full-column inverse
inside the SAME fixed balanced middle and recording construction. Its
endpoint is V_k^dagger M V_k; the entire spectrum of M, including the
failed c0/factory/complement modes, is unchanged. Equal inventory gives
the same finite N. The WHOLE heat theorem(97), with the actual scene
and source-spin carrier, therefore gives EXACTLY

    B_k=H_ref(N,D_full)+j_K(x(u_k)).                      (192)

No heat or determinant anchor has been removed. On the owned interior
source chart, j'_K>0, q>0 and gamma_rest>0. For two actual distinct
endpoint features u_a,u_b sufficiently near u0, let A_ab be the ACTUAL positive divided
difference of j_K between x(u_a),x(u_b). Then

    (B_b-B_a)/[A_ab(u_b-u_a)]
           =-gamma_rest q(u_a+u_b)/2.                   (193)

This exact finite-code identity uses algebraic report differences;
it does not need a transcendental equality test or assume a continuous
admissible angle. At u_a,u_b->u0 its source is -gamma0 q/2, nonzero.
With the SAME field-source calibration Gamma_ab=A_ab gamma0 a0 tau/Omega,
gamma0=gamma_rest 2p^3, it becomes

    (B_b-B_a)/[Gamma_ab(u_b-u_a)]
       =-Omega q(u_a+u_b)/(4p^3 a0 tau)
           ->-Omega q/(2a0 tau) !=0.                    (194)

The genuine readiness row survives collective bank averaging. If q
has a positive fixed floor while the report aperture tau tends to0,
this normalized row grows rather than vanishing. Its physical test
norm must still use the actual code/readout lift; the displayed
nonzero value is on the declared unit-u source test, not a claim that
every physical norm gives that unit test for free.

### What this construction changes in the parent argument

X_run and its native edits now have an explicit membership procedure,
resource inventory, full-column semantics, generated return cut and
computable Book valuation. Undefined membership is no longer the
reason to stop this CONCRETE operational application. The actual
same-inventory resource test(189)-(194) supplies a specific non-small
additional source rather than an arbitrary effect variation.

It also prevents a false positive: opening the domain to these raw
programme variations does NOT make the current interior source-bearing
7s family a joint stationary family. Its covered field/bank estimates
and neutral encoder fibre remain true, but do not annul this readiness
row. A different legitimate physical task may fix the full response
including readiness; merely preserving its conditional logical answer
is insufficient. The remaining positive route must derive that actual
constraint/variation image, solve the retained complete source by
another admitted mechanism, or change this scoped physical application
while preserving the original action. This result neither chooses an
Einstein task nor claims an unrestricted full-D0 no-go. Physical source
availability, spatial geometry identification and compatible stationary
refinement keep their declared scope. GR_closed=false; raw216 is open.


## 7u. Suppress the native readiness source by a fully paid coherent operation

24 October 2026. Same owner; input90fc7009. The exact additional readiness
row(193)-(194) now has a constructive consumer. A finite coherent
amplifier suppresses that row without imposing its zero value or fixing
the raw factory probability as a new constraint. The logical query and
the unchanged Book functional retain their original definitions.

The proof, exact native phase compiler, expanded-word constructor and
bounded independent checks are in
[d0_native_readiness_amplification_2026-10-24](sources/d0_native_readiness_amplification_2026-10-24/).
The mathematical guide is the known
[fixed-point quantum search construction](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.150501).
Here the implemented phases are EXACT Golden powers in the original
coefficient field. No pi/3 gate, complex physical primitive, probability
oracle, adaptive reset or additional physical selector is admitted.

### Consume all-input readiness, rather than the desired report outcome

Let A be the complete actual forward preparation/query word. Consume
the owned raw-factory factorization of paid-writer9.1 and7p-s on its
declared input interface:

    P_ref A^dagger R A P_ref=gamma P_ref,
    R A P_ref=sqrt(gamma) S,   S^dagger S=P_ref,
    0<gamma<1.                                          (195)

R is the conjunction of GENUINE READY flags; it EXCLUDES the report b.
Every corrected successful factory transcript factors coherently with
its logical isometry on all protected DATA/oldRIGHT inputs, not just
one prepared field state. The physical raw failures remain in A.
The source-I spin is the same existing dirty spin; the base forward
G/CX programme is identity on it, and completed inverse blocks restore
it. The all-input statement thus permits the algorithmic input
projector P_ref to leave that spin arbitrary. A programme having only
state-specific success or inaccessible spin-selective input constraints
does not satisfy this application by declaration.

Add ONE fresh realification rebit. It is physically initialized blank
and counted in the Book input cut, while the algorithmic P_ref is
identity on it. Define the selective phase on an actual computational
predicate P by its real orthogonal matrix exp(beta J_rebit tensor P).
Only addressed logical bits, excluding oldRIGHT/spin/rebit, control it.
The actual Book cut P_Book may be smaller than this enlarged P_ref;
they are not identified. The final READY/report test ignores the rebit.

For one common phase beta, write R_P(beta) for this selective rotation.
The recursively generated operator, in matrix order, is

    A_(r+1)=A_r R_(P_ref)(beta) A_r^dagger R_R(beta) A_r,
    A_0=A.                                              (196)

It uses the literal reverse of the SAME raw word, on the same retained
active work. No previously measured history is reversed. oldRIGHT is
untouched at every primitive. This is a top-level amplification of the
completed forward processor; it is not identified with a controlled
call of A against an external idle/reference branch.

### One exact native phase gives a contracting readiness law

For K computational controls and prescribed bit pattern v, the native
Walsh/parity construction gives on EVERY column

    product_(S subset controls)
      CX_S G_rebit^((-1)^(v.S) k) CX_S^dagger
        =exp[2^K k theta J_rebit tensor P_v].             (197)

Each parity is actual CX, and every negative G is expanded by7j's
source-I inverse, including dirty-port routing. No H, Toffoli,
known-one input or heralded phase factory is used. Choose
Kmax=max(K_input,K_READY) and one positive integer k for which

    sin(beta)>0,   1/2<cos(beta)<17/32,
    beta=2^Kmax k theta.                                 (198)

The owned irrational Golden-angle theorem makes the search terminate
with enough finite integer/precision budget. Membership in this open
interval is certified with rational bounds on algebraic Golden powers.
For a smaller predicate use k_v=2^(Kmax-K_v)k. Both implemented phases
are then EXACTLY the same native rotation, not merely approximations
to the same target. One bounded certificate is G^624: Kmax=2,k=156;
Kmax=3,k=78; Kmax=4,k=39 all represent that same rotation.

Put c=2cos(beta)-1 and a=1-c. Thus 0<c<1/16 and a in(15/16,1).
The interval is chosen for a generic amplifier stability estimate,
independently of the geometry, target field or Book coefficient ratio.
If epsilon_r=1-gamma_r, projector algebra in(195)-(196) gives EXACTLY

    epsilon_(r+1)=h(epsilon_r),
    h(e)=e(c+a e)^2,
    h'(e)=(c+a e)(c+3a e),
    gamma_r=1-h^r(1-gamma).                              (199)

To verify the identity, decompose A_r psi=g+f into READY and failed
parts. With w=exp(i beta) as a mathematical notation for the real
rebit rotation, (w-1)^2=-a w. The next failed component is
w(c+a epsilon_r) f. The successful component is one scalar times
g for EVERY input. Therefore its normalized logical CP/isometry
channel is the original S exactly. Its scalar phase is retained in
the rebit and may depend on gamma; there is no assertion of equality
of all retained future profiles.

For every 0<gamma<1, h(e)<e for 0<e<1 and the failure tends to0.
This alone would be an insufficient C0 argument. On an actual
gamma>=gamma_min>0 chart set e_max=1-gamma_min and
lambda=(c+a e_max)^2<1. Then epsilon_r<=e_max lambda^r.
Choose a finite warmup R0 with e_max lambda^R0<=1/48. Thereafter

    epsilon_(R0+s)<=(1/48) 144^(-s),
    0<=D_gamma gamma_(R0+s)<=3^R0 96^(-s).               (200)

Indeed h/e<(1/12)^2 and h'<(1/12)(1/8) once e<=1/48;
before warmup h'<=3. The proof is uniform on the stated positive
readiness chart. Its constants depend on the ACTUAL gamma_min;
no mesh-uniform resource efficiency is asserted. Higher shared-control
jets retain their actual chain-rule factors as in the packet proof.

### All repetitions, phases and inverses count in the actual clock

The constructor emits A_r;R_READY;inverse(A_r);R_initial;A_r in
chronological order and validates the ENTIRE expanded list. If a word
has g G, n CX and i SourceI primitives, with t<=g G acting away
from the source port, its literal inverse has

    g_inverse=g, n_inverse=n+6t, i_inverse=4g+3i.

For W=5g+n+i this gives W_inverse<=3W. Both phase words have a
fixed finite total weighted inventory C_phase on the fixed interface.
Consequently

    W_r<=5^r W_0+C_phase(5^r-1)/4,
    N_r<=W_r.                                           (201)

The semantic count 3^r of base A/A^dagger occurrences is NOT the
raw stage count. Inverses, SourceI and routing really execute. Work
is reused coherently, so no extra copy or fresh spin is allocated at
each recursion; the autonomous clock still has its NEW full N_r
modes. The outer Book echo adds its full actual inverse, middle and
balanced recording, with the same O(5^r) inventory bound.

This duration bound also controls readiness beyond the tied-u test.
At the scalar-ready base, with algorithmic P_ref and R fixed,
Q=A_r^dagger R A_r is a projection and
P_ref Q P_ref=gamma_r P_ref, so its off-diagonal block has norm
sqrt(gamma_r epsilon_r). For any unitary MATRIX comparison tangent,

    Gamma_READY=P_ref A_r^dagger R A_r P_ref,
    ||D Gamma_READY||_op
       <=2sqrt(gamma_r epsilon_r)||D A_r||_op.           (202)

The comparison is not asserted to be a free native pulse. For actual
per-stage generator lifts K_j=g_j^dagger D g_j,
||D A_r||<=sum_j||K_j||. Thus the logarithmic-readiness bounds are
2sqrt(N_r epsilon_r/gamma_r) for the Euclidean generator norm and
2N_r sqrt(epsilon_r/gamma_r) for the maximum per-stage norm.
Both tend to0, since N_r^2 epsilon_r=O((25/144)^s) after warmup.
This retains the time-summed norm rather than replacing the enlarged
process by one uncharged macro. Finite endpoints keep the packet's
actual quadratic norm remainder as well as their first source.

Equation(202) bounds READY only. Independent raw controls can also
change the successful logical query. Their Dq is not bounded by
calling its readiness small; the free full-preparer obstruction7g
still applies to the complete report source.

### The exact same Book calibration consumes the 7t source

Put the ENTIRE amplified forward word A_r inside the owned complete
balanced echo A_r^dagger M A_r, with its true primitive clock and
transported cuts. M and the final report ignore the rebit. Its new
whole heat is field constant by the same7j conjugacy theorem, including
all scene/clock/work/failure modes, not only a selected READY block.
Choose the recorder C_new=C_old tensor I_rebit, retaining the SAME
old recording bank. On the returned old-work block, the rebit-blind
report and scalar success give corner(1-d_K gamma_r q)I_rebit. Thus
an initial rebit0 has no hidden rebit1 component when those old labels
return; no extra rebit-copy bank is needed for this declared recording.
The rebit itself remains physical coherent work. This choice doubles
the full fibre and leaves the protected input rank unchanged. A task
requiring a further classical rebit copy must count that added bank
and its actual gates separately. Retain the resulting absolute heat.

The original conditional query q is unchanged on(195)'s interface,
including all its internal algorithm-control coherences. The resulting
price and ACTUAL gain are

    B_r=H_ref(N_echo,r,D_full,new)+j_K(gamma_r q),
    Gamma_r=j'_K(gamma_r q) gamma_r a0 tau/Omega.         (203)

Here N_echo,r is the full outer-echo schedule, including its
inverse/middle/recording; it is not just the forward count in(201).
For the7t endpoint stencils, G counts on EACH wire, the source frame
and phase predicates stay fixed, so the inverse and amplified schedules
have matching actual lengths by the literal count recurrence. Aggregate
primitive counts alone need not fix routing for unrelated programmes.
If gamma is field independent on the owned chart, the complete field
source divided by Gamma_r is exactly the old normalized Dq. The
conditional bank/operator estimates can likewise be reused on their
SAME input interface. Truly additional input/constraint equations
are not supplied by an input-dependent success law.

For the ACTUAL 7t source, D_u q=0 and D_u gamma=-gamma0/2 at u0=p^3.
Writing F_r(gamma)=1-h^r(1-gamma), its normalized extra source is

    D_u B_r/Gamma_r
      =-Omega q/(2a0 tau) *[gamma0 F'_r(gamma0)/F_r(gamma0)]
          ->0.                                         (204)

This suppresses the named non-small term(194) by an actual finite
native construction. For each physical mesh/copy/aperture budget,
choose the finite amplification depth using its true gamma_min,
source norm and tolerance. The original weak-aperture calibration
is retained; its factor1/tau is not silently cancelled.

For finite code endpoints the exact identity is instead

    (B_b-B_a)/[A_ab(u_b-u_a)]
       =q [F_r(gamma(u_b))-F_r(gamma(u_a))]/(u_b-u_a),    (205)

with the actual positive divided difference A_ab of j_K. Use the
common real clock length at EACH stencil and the actual source lift.
Equation(200) makes this readiness secant small uniformly on the
declared positive-readiness chart; no continuous native word selector
or zero-priced comparison of unequal durations is presumed.

The component substitution is precise: the constructed domain7t now
has a native operation controlling its exhibited readiness source,
with full inverse/clock costs and an actual norm. It does not establish
stationarity under every code change in X_run. Effects changing the
conditional query, independent inverse/frame/cut/middle/source and any genuinely
selected extra Info/work terms retain their sources. Physical source
availability and the original spatial operator/geometry identification
remain at their stated scope. No Einstein task is imposed; no complete
joint stationary refinement, positive_gr, GR_closed or raw216 closure
is claimed by the readiness operation alone.


## 7v. Transport the actual query test, and retain the source when that test is fixed

25 October 2026; native realization / source composition, same constitutive
owner and native-programme-v1 interface. Input is the published7u checkpoint
17905011461b946302fa90a144538940bdb52356. The parent premise is the
remaining conditional-query source Dq in(202)-(204). The changed input is
one literal native report recoding AND its paid inverse test map, rather
than another readiness operation or another geometric stationary root.
The bounded executable witness and its receipt are in
[d0_native_query_control_2026-10-25](sources/d0_native_query_control_2026-10-25/check_query_control.py).

### A READY-preserving native edit has a non-small source at a fixed test

Let A_r be the actual complete forward programme of7u, with its genuine
READY projector R, root bit c0, final report b and all unknown protected
DATA/reference/oldRIGHT. READY excludes b and satisfies R<=P_(c0=1).
Append one initially blank ORDINARY coin a, with chronological tail

    T_(L,k)=W_(L,k)(c0,a);CX(a,b),
    u_k=cos(2k theta),  |k|<=L, L-k even.                (206)

The W cell is the SAME literal G/CX construction used in7t. On c0=1
it gives G^k on a; the c0=0 block is G^L, not a deleted failure block.
Every tail commutes with R. For the original conditional report effect E,
on EVERY protected input and arbitrary external reference, the new effect
and its unnormalized version are exactly

    E_out(u)=I/2+u(E-I/2),
    F_out(u)=gamma_r E_out(u).                           (207)

The tail acts on a,b and reads c0. It preserves the old geometric/source
bank marginal, even when that bank is entangled with b. It preserves
readiness exactly. It does change the bare report response and some
retained correlations. These distinctions matter: equality of normalized
geometry after calibration is not equality of the complete physical task.

At the original k=1, u0=p^3>0. If E=b0 I+tau T_geom, its new offset is
1/2+u0(b0-1/2) and its field aperture is u0 tau. All42 field gradients
are multiplied by u0. Thus the old normalized geometric source and its
field stationary roots survive, while an independent controller row can
still be nonzero. Put the whole edited word, its actual inverse, the SAME
fixed middle and balanced recording into the Book construction(97).
At each common-inventory stencil its absolute price is

    B_k=H_ref(N_new,D_new)+j_K(gamma_r q_out(u_k)),
    q_out(u)=1/2+u(q-1/2).                              (208)

For the ACTUAL positive divided gain A_ab of j_K, take
Gamma_out,ab=A_ab gamma_r u0 a0 tau/Omega. Then

    (B_b-B_a)/[Gamma_out,ab (u_b-u_a)]
       =Omega(q-1/2)/(u0 a0 tau).                       (209)

This is an exact finite-code equality. It is nonzero when q!=1/2 and
does not decrease with readiness-amplification depth. The existing
Q=33,580 native returns give codes(-65,67),(-1159,1161), with a common
k=1 base at L=67,1161 respectively; their exact algebraic u endpoints
straddle u0. The receipt checks the positive-return j_K chart on its
declared q=1/4,tau=2^-10 examples and two configured gamma values. The
symbolic identity(209) does not assert those examples exhaust all sources.

The conditional endpoint lift is explicit. For any purified old output
Psi, including its protected reference, the successful state is

    Phi(alpha)=cos(alpha)|0>_a Psi+sin(alpha)|1>_a X_b Psi,
    <Phi,D_u Phi>=0,
    ||D_u Phi||^2=1/[4(1-u^2)]=1/(16p^3) at u0.         (210)

Actual endpoint distance is 2|sin((alpha_b-alpha_a)/2)|. The raw forward
state lift has squared norm Pr(c0=1)/[4(1-u^2)], with
gamma_r<=Pr(c0=1)<=1. These are endpoint-state norms, not a declaration
of a continuous native pulse or a C1 curve of full retained code/clock
histories. Those histories retain their own topology and finite secants.

Both the new coin AND one new coin-recording-bank bit are initially blank
work. They multiply the full thermal fibre by4 and leave protected input
rank unchanged. For a coin away from the source port, literal tail and
inverse counts, including the two balanced recording CX, are

    Delta n_G=2L, Delta n_CX=10L+4, Delta n_SourceI=4L,
    Delta N_fixed_test=16L+4.                            (211)

The inverse retains dirty source-port/spin columns. This is not the7u
special phase rebit; no old-bank identity justifies omitting its recording
cost here. All added modes and all primitive clock stages enter(208).
Different L values have different absolute prices.

### A concrete paid test transport exactly restores the old source

The coin is retained. The ORIGINAL report can therefore be read as the
parity a XOR b_out, since b_old=b_out XOR a. This has an actual native
test map. Write C=CX(a,b), T=CW in operator order. The old middle M
ignores a and PRESERVES the c0 sectors: [M,P_(c0=1)]=0. Its target meter
is distinct from c0, a and b; READY/report are controls. Consequently
[M,W]=0 on ALL columns, including c0=0 and every failure sector.
Coin-blindness alone would not suffice if M changed c0. Execute

    M_parity=C M C,
    T^dagger M_parity T=W^dagger M W=M.                 (212)

Both new C are real native stages. Equation(212) is an exact full-operator
identity, not equality of one prepared expectation or a successful block.
It supplies the explicit observe-commutes map for this report recoding,
consuming the owned correctness/transport interface of7l and(83)-(85).
For another old endpoint observable O, the corresponding endpoint test
is T O T^dagger; its implementation must be paid when actually executed.
An old future context containing further actions requires transport of
those actions too, not just its final test while keeping incompatible
intermediate actions fixed.
This does not identify the complete new clock/history profile with the
old one or make their durations equal.

For this particular Book middle, the additional2 CX give
Delta N_transported_test=16L+6 with the SAME full fibre/rank accounting
as(211). This is the declared common recorder; it is not a proof that
the extra coin-copy bank is necessary for the compensated programme.
Before recording, the full echo equals the old echo tensor I_coin.
Balanced coin recording commutes with this endpoint and cancels there
on all columns. The full balanced endpoint is consequently the old
balanced endpoint tensor I_coin tensor I_newbank. The old rank-r0
return corner is unchanged, so feedback is
exactly the old j_K(gamma_r q), not the affine bare-report version.
At the NEW actual N and D the whole-clock theorem(97) gives

    B_parity,k=H_ref(N_new,D_new)+j_K(gamma_r q),
    D_u B_parity=0,
    Gamma_parity=j'_K(gamma_r q) gamma_r a0 tau/Omega.    (213)

Here M and the physical bootstrap parameters are fixed; all field
dependence is inside A_r. The field source is therefore exactly the old
one with its real new gain. This does not identify sources of arbitrary
independently moving middles or clocks. No arbitrary compensating price, reference function or negative
counterterm was added. The actual inverse of the record recoding carries
the test. Heat at this common N is independent of k by full endpoint
conjugacy, not because the moving prefixes were frozen. Its absolute
baseline can differ from the shorter old execution and stays paid.

### The substituted premise and the remaining physical application

Equations(212)-(213) remove the apparent query source for this explicitly
co-transported implementation of the SAME old report. Equations(208)-(209)
retain its genuine source when the physical middle is instead fixed.
They are two specified processes. A generic self-check that verifies a
programme against its own decoded word accepts both; it does not select
one physical query, input family or middle. Likewise the accepted generic
TheoryTransfer supplies a transport once its interpretation/test map is
given; it does not supply the different spatial scene interpretation.
No correctness fibre is declared to be the entire native execution domain.

The source-bearing reporter still has independent upstream queries that
are not mere reversible recodings of the old report, and independent
inverse/cut/frame/middle/source choices. Readiness control7u, sharp stored
keys and a verifier do not by themselves discharge those equations.
The next positive parent application remains an admitted joint original
graded-CAR/solder/pairing/link step with its complete operator/price map,
or an independently native stationary/constraint law. The existing original
field-to-operator dictionary and complete full42 source equations are inputs
to that application, rather than claims established by an encoded report.
This checkpoint changes no action or physical admission rule and supplies
no unrestricted no-go, joint stationary refinement, GR_closed or raw216
completion. The bounded checker tests the new operator/source maps; it
does not replay the unchanged large root, full128 or Lean suites.


## 7w. Transfer the original operator and finite heat through full native words

25 October 2026; same constitutive owner/native-programme-v1 carrier,
input05c7df3a894ee8141bbd01c66b91e1435e4bc899. This addresses a
particular remaining application of7k and paid-writer12.3(55)-(57): the
original spatial operator must affect the ENTIRE native thermal spectrum,
not merely a scalar report or an initialized channel. The changed input is
a nonconstant full clock monodromy. The construction, source bounds and
bounded native witness are in
[d0_native_operator_holonomy_2026-10-25](sources/d0_native_operator_holonomy_2026-10-25/PROOF.md).
It constructs a native sector and does not select its physical temperature,
cut, reachable field writer or complete stationary section by definition.

### Preserve the original finite spatial heat exactly before compiling it

Let D be the SAME finite real positive-frame spatial Dirac of7k and
paid-writer12.1, with its actual density/observer/calibration data. The
original stopped spatial heat uses B=I-alpha D^2>0, beta_sp=m alpha,
Z_sp=Tr B^m and H_sp=log(C Z_sp)/beta_sp, not an independently substituted
continuous heat. On a strict chart alpha||D||^2<=rho<1 define

    K=K_alpha(D)=D sqrt[-log(I-alpha D^2)/(alpha D^2)],
    exp(-beta_sp K^2)=B^m,
    D=K sqrt[(I-exp(-alpha K^2))/(alpha K^2)].            (214)

Both quotients have their removable value1 on zero modes. This is an
invertible odd analytic operator map; it does not lose the signed raising
blocks needed by the owned all16+24 decoder(51)-(53). Density, frames and
the separate two material coordinates keep their existing roles. Its actual
Frechet derivative Kdot=DK_alpha[Ddot] is retained. It is not Ddot. The
proof gives a finite bound on the strict chart and verifies the exact
original partial

    D H_sp=-2 Tr[D B^(m-1) Ddot]/Z_sp.                  (215)

Fixed alpha,m,C and positive-frame data are the declared partial here.
Additional independent parameter, preparation and frame equations remain.

### Compile the entire monodromy with actual inverse and clock lengths

With J=[[0,-1],[1,0]] on ONE realification rebit, take the full target

    U_delta=exp(delta J tensor K) tensor I_aux.           (216)

It is a real special orthogonal matrix on every scene/rebit column.
It acts on arbitrary scene input, not just a resource success subspace.
The source-local inverse of7j realizes each G_i^dagger on ALL columns,
including dirty source-spin, using at most11 actual primitives with
routing. Use its declared G_CX_SOURCE_I interface, not an unsupported
inverse on a smaller physical palette. The source-spin is restored by
each complete inverse macro; it remains in every primitive prefix and
in the full heat.

For at least three legally addressed ACTIVE bits, the owned Golden/CX
Lie closure supplies density in SO(2^n). The finite macro palette
G_i,G_i^dagger,CX_ij is inverse closed. Applying the external
[Kuperberg theorem2.4 and bounded-region remark](https://toc.cs.uchicago.edu/articles/v011a006/v011a006.pdf)
to this compact group gives polylogarithmic word length in operator error.
It requires FPTEAS target entries: fixed finite rational or algebraic D
data on the strict chart, with FPTEAS alpha,delta parameters (in particular
rational/algebraic ones), supply them through the analytic functions.
Its constants depend on the fixed dimension and layout;
no bound uniform in the refining mesh is inferred.
This analytic compiler input is not a new Lean theorem or an installed
general compiler.

Thus, at fixed mesh/dimension and for a finite bounded target catalogue,
choose actual words with full operator error epsilon and expanded length
at most C_h(1+log(1/epsilon))^c_h. No extra prepared ancilla or initialized
isometry replaces this FULL-column approximation. OldRIGHT is never a
scratch/control. Source-spin lies in the retained auxiliary carrier.

Common duration is physically realizable. On three distinct ACTIVE wires,
A=CX(a,b), Bc=CX(b,c), Cc=CX(a,c), the chronological five-CX word
A;Bc;A;Bc;Cc is exactly identity on every column. Together with two
equal CX, it pads any length gap>=4. Pad the catalogue to the maximum
expanded length+4 using these REAL stages. This yields

    N<=C_h(1+log(1/epsilon))^c_h+4                      (217)

after adjusting the fixed constant for the inverse macros. Padding is
not a free idle. The resulting prefix cuts and clock contain every stage.
These are finite hardwired configurations in7t's executable domain.
For one autonomous stored-program decoder instead, its whole key carrier,
all branches and physical preparation must be included separately. The
construction does not read an unknown physical field through an oracle.

### All clock modes recover the finite heat with its true gain

Apply the OWNED whole-clock Fourier/holonomy theorem to the paired bare
incidence clock of7t, retaining all prefixes, zero modes and full fibre.
It is not the different33-scene Cartesian incidence of paid-writer13.
For beta_sp fixed, delta||K||<=pi/2, set

    beta_clk=2N^2 beta_sp/delta^2,
    Gamma_clk=beta_sp/beta_clk=delta^2/(2N^2).           (218)

If c_H is the full auxiliary dimension, the exact paired heat partition
of the target monodromy is

    Z_clk=4 c_H sum_i sum_(k mod N)
      exp[-beta_clk(1-cos((2pi k+delta lambda_i(K))/N))]. (219)

The factor4 is paired Hodge degrees times realification. There is no
extra multiplier N outside the COMPLETE clock-mode sum. The proof bounds
the source error by an O(delta^2/N^2) low-mode error and an exponentially
small winding tail, uniformly in the actual N. After dividing the raw
heat by the ACTUAL Gamma_clk, its field source converges to(215), with
its actual Kdot norm. At fixed ranks the absolute baseline includes
log(4 c_H/C)/beta_sp in those units; it is retained, not subtracted from
the physical action. For c_H=C only the known log4/beta_sp remains.
An input cut's auxiliary rank r_P need not equal c_H.

For a power-of-two scene the construction uses exactly that scene.
If a q-dimensional zero block is needed to embed a different scene into
qubits, its q zero modes stay in(219). The limiting partition is Z_sp+q,
and the old heat partial is multiplied by Z_sp/(Z_sp+q). This is the
owned harmonic-normalizer correction, not permission to delete modes.

A sufficiently small full native monodromy error epsilon, with the
proof's strict small-angle margin, has heat value error
O_h(epsilon/delta), in the units of(215), uniformly in N. This avoids
the false estimate obtained by multiplying a crude operator bound by
beta_clk without its heat weights. For actual finite field stencils,
divide endpoint price-error bounds by their true stencil separation and
operator/field lift. There is no nonconstant continuous selector of
finite native words, nor a free native pulse. The proof's smooth target
derivative and the implemented finite-code covectors retain this distinction.

### The same word's genuine feedback is not the original spatial feedback

Take the actual initial rebit0, arbitrary scene input and auxiliary
projector P_aux of rank r_P, with generated prefix cuts as in7t. Its
SINGLE-wrap return defect and bootstrap feedback are exactly

    E_U=sin^2(delta K) tensor P_aux,
    J_clk=-r_P Tr log[I-z sin^2(delta K)],
    D J_clk/Gamma_clk=(2r_P z N^2/delta)
       Tr[(I-z sin^2(delta K))^-1 sin(2delta K) Kdot].   (220)

At small delta the last row is
4 r_P z N^2 Tr(K Kdot)+O_h(N^2 delta^2||Kdot||).
It is generically non-small at fixed z. A proof controlling the heat
does not cancel this return source. In particular it is NOT the original
128-fold spatial term -128 Tr log[(1-z)I+zB^m], and it supplies no genuine
Rayleigh/preparation equation. Setting z or an added price by a desired
Einstein source would not prove the missing physical binding.

The compiler error can nevertheless be controlled rather than hidden.
Writing E_U=C_U^dagger C_U with C_U=(I-P)U P gives

    ||E_V-E_U||<=2delta||K|| epsilon+epsilon^2.          (221)

The normalized feedback value error retains its actual input rank and
factor O_h(N^2 epsilon/delta+N^2 epsilon^2/delta^2). Density alone would
give no length/accuracy conclusion. The full-column inverse-closed
compiler bound(217) DOES make this error tend to0 at fixed h,delta and
fixed stencil/gain scales. For changing meshes or extra decaying gains,
retain their real constants and choose/check the actual schedule; no
uniform efficient refinement follows. Approximation of the TRUE
feedback is not removal of its nonzero source(220).

The full operator map also has a signed readout. On the principal-log
chart of(216), before its identity auxiliary factor,

    K=-(1/(2delta)) Tr_rebit[(J tensor I)log U_delta].   (222)

The same extraction from a nearby actual real orthogonal word gives a
real symmetric K_hat with error O(epsilon/delta). Apply(214)'s inverse
and the owned spatial decoder with their real local conditioning. This
keeps signs and zero modes, unlike a scalar heat spectrum alone. It is
a mathematical operator readout, not a free logarithm/tomography gate.
Other components of the compiled word's logarithm remain in the full
thermal/feedback error bounds; this extraction does not discard them.

There is a decisive full-price check WHERE the uniform coframe variation
is actually admitted. At fixed density/calibration/observer/links,
E(t)=exp(-t)E gives Ddot=D by paid-writer(57). Put
T_D=Tr[D^2 B^-1]>0 for D!=0 and
A_H=2Tr[D^2 B^(m-1)]/Z_sp. For delta||K||<=pi/4, the exact identity
K Kdot=D^2 B^-1 and sin(2delta k)/k>=4delta/pi give

    D(H_clk+J_clk)[scale]/Gamma_clk
      >=(8r_P zN^2/pi)T_D-A_H-E_N C_rho||D||.           (223)

Here E_N and C_rho are the proof's explicit heat-source and Frechet
bounds. E_N is bounded independently of N, so this row is strictly
positive at large actual N, fixed z>0 and D!=0. Its strict sign transfers
to sufficiently accurate paid finite-code stencils with their actual
separation/norm budget. Thus the direct whole H+J stationary application
fails on this free-global-scale chart even though its heat transfer works.
This does NOT apply the same test to a fixed collar: a global rescaling
would change that boundary. Nor does it exclude cancellation by genuinely
derived additional physical source terms. It identifies the component
that the next complete-source construction must address.

The precise positive substitution is now an all-column native-word and
whole-finite-heat realization of the ORIGINAL signed spatial operator,
with its inverse map, real norm/gain, primitive length and complete
feedback explicitly bound. It strengthens7r's query-channel application
and7k's operator readout; it does not replace their owned results. The
remaining parent application is the selected same-execution complete
source, including(220), true Info/work/Rayleigh and independent apparatus
equations, then stationary/refinement and physical theory transfer.
The auxiliary carrier, temperature and task are supplied for this
constructed sector; their compulsory original physical selection remains
unproved. Neither another exact GR root nor GR_closed/raw216 completion
is asserted by this operator/heat construction.


## 7x. Bind an actual retained record to its information and preparation source

25 October 2026; same constitutive/native-programme-v1 owner, input
feeffbfe01ddbd01c4ec931ade04d58fe573ac36. The parent application is
7w's remaining Info/work and independent preparation reaction. The
changed input is a literal copied record, an explicit prefix/suffix
archive handoff and a native same-initial-state preparation orbit.
The [proof and bounded implementation](sources/d0_native_recorded_info_source_2026-10-25/PROOF.md)
consume the owned future-memory, canonical registered-algebra and
complete-CQ source results; no new information axiom is introduced.

### Actual copying supplies a future-memory map without erasing coherence

Let V be the ENTIRE actual native forward word on report h and WORK,
with h initially0; WORK includes DATA and every retained reference.
Write M_b=<b_h|V|0_h>, so sum_b M_b^dagger M_b=I. Add a blank bit a
and execute the balanced copy C(V tensor I_a)C, C=CX(h,a). The first
C acts trivially on this prepared column but remains a real stage.
Its complete output on input Omega is

    Theta=sum_(b,c) |b_h,b_a><c_h,c_a|
                       tensor M_b Omega M_c^dagger,
    Tr_a Theta=sum_b |b_h><b_h| tensor X_b,
    X_b=M_b Omega M_b^dagger.                           (224)

Theta retains global cross-record coherences. The second line is an
exact marginal of the ACTUAL word, not a physical dephasing operation.
The copy doubles the full thermal fibre, adds two actual CX stages,
and leaves the original protected input rank unchanged. Full endpoint
conjugacy, rather than a prepared-column argument, gives its whole
heat spectrum; the return corner retains the actual initial blanks.
The new absolute clock/carrier price remains paid.

The archive handoff occurs AFTER this complete prefix, including any
actual padding. Its suffix keeps the SAME correlated Theta and enlarges
the immutable mask by a; it does not reinitialize any prefix register.
Suffix input blanks are not inferred from the old prefix's blank list.
The validator rejects any later gate touching a, even as a control.
The prefix inverse cannot be executed after sealing if it touches a.
This is an explicit future-execution boundary, not a new unitary, reset,
or permission to mark a fresh blank as old throughout its creation.

For terminal tests ignoring a, every allowed suffix acts as I_a tensor S,
so(224)'s marginal determines all their future probabilities. If terminal
tests also read a in its registered basis, their effects are block diagonal
in a; the decoder uses the same two X_b blocks and the known initial h=b.
A joint coherence-sensitive test mixing a sectors would require a different
future algebra. This supplies the actual sufficient-memory/test map to the
owned FutureExecution/VerificationCore consumer. It does not infer access
to a purifying oldRIGHT reference or select a minimal physical observer
algebra from the gate mask alone.

### Keep all conditional quantum work and its true source

For the declared reference-complete CQ component Gamma=direct_sum_b X_b,
its information GAIN in natural units is

    I_ref=S(Gamma)-S(Omega)
      =h(p_1)+sum_b p_b S(X_b/p_b)-S(Omega),
    p_b=Tr X_b.                                        (225)

The redundant record copy is not a second independent entropy. Global
coherent output entropy is still S(Omega). On a PURE complete Omega,
including all actual purifying oldRIGHT, every conditional block is rank1
and I_ref=h(p_1). A mixed DATA marginal does not contradict this fact.
For a genuinely mixed complete input, the conditional entropies and initial
subtraction in(225) remain. No arbitrary purification is supplied for free.

If the real future also ignores oldRIGHT, use the further marginal and
I_act=S(Gamma_DATA)-S(rho_DATA), not(225) without its conditional terms.
Their exact difference is the loss of DATA/oldRIGHT mutual information
under this channel. For pure complete input it is
S(rho_DATA)-sum_b p_b S(rho_DATA|b), which need not vanish. Sealing a new
record therefore does not choose the treatment of the already retained
reference, or identify either gain with compulsory Book03 branch Info.

There is also an actual read-only CLASSICAL oldRIGHT contract: both the
historical bit r and the new report b are readable only in their recorded
bases. On the witness below their joint law is
P(r,b)=p_r Bern(q_r)_b, p_r=(p,p^2), with
q_0=(e_0+e_1)/2+(e_0-e_1)u/2 and
q_1=(e_0+e_1)/2-(e_0-e_1)u/2. Conditional DATA work is pure, hence the
window gain is I_reg=p h(q_0)+p^2 h(q_1). This is another specified future
algebra, not h(q) assigned to an inaccessible quantum reference. Bringing
the original generation of r inside the full initial-blank execution adds
its actual constant h(p) to this registered gain; its value is retained.

On a faithful fixed-support chart, differentiating the SAME actual instrument
gives, for normalized input tangents,

    G_Omega=log Omega-sum_b M_b^dagger(log X_b)M_b,
    D I_ref=Tr(G_Omega DOmega)
      -sum_b Tr[(DM_b Omega M_b^dagger
                       +M_b Omega DM_b^dagger)log X_b]. (226)

Constants cancel by the actual completeness relation. At the ideal7w
operator M_0=cos(delta K), M_1=sin(delta K), these derivatives are FULL
matrix divided differences. Compose Kdot=DK_alpha(D)[Ddot] from(214);
replacing it by Ddot or a scalar sine derivative would omit source rows.
For pure inputs use the actual rank-one formula h'(q)Dq on its positive
chart; logarithms of a singular Omega are not substituted into a faithful
ambient derivative. Support births retain the existing C1/entropy boundary.

If an actual fixed fine-history charge ledger supplies an effect C_eff,
keep all extra genuine prices in C_ext. In natural units define the
candidate gain-price component only by

    P_nat=ell[C_ext+Tr(Omega C_eff)]-I_ref,
    ell=log phi,
    D P_nat=ell D C_ext+ell Tr[(DOmega)C_eff+Omega DC_eff]
                                                       -D I_ref. (227)

This does not prescribe C_eff or assert every physical work term is a
fixed linear expectation. On the native real chart the local DATA-unitary
preparation row contains Tr_RIGHT[Omega,ell C_eff-G_Omega], together with
ell D C_ext. It preserves the true oldRIGHT marginal. A smaller admitted
preparation domain inherits only its actual tests; a larger affine input
domain is not inferred from local unitary access.

### The supplied-input window has a nonzero registered source at constant Book price

There is an exact native witness for this remaining row. Let theta be the
original Golden angle, Q=33, and phi_Q the small principal angle of
G^(2Q). Execute, chronologically,

    U_Q=G_h^(4Q);CX(d,h);G_h^(2Q);CX(d,h),
    A_n=G_d^n,
    C;A_n;U_Q;actual_inverse(A_n);C.                    (228)

The gates act on ACTIVE DATA d, report h, the new bank and the declared
source apparatus. Inverse source-spin is restored on every column;
the existing oldRIGHT is untouched. Before
the current immutable boundary the fixed initial state
Omega_0=|psi_0><psi_0| was generated by the native history
G_d;CX(d,RIGHT), with |psi_0>=sqrt(p)|00>+p|11>. That historical record
was still fresh then. The current word never uses it as a gate target
or control, and every n uses this SAME complete initial state.

U_Q's two DATA blocks have angles3phi_Q and phi_Q. Put
e_0=sin^2(3phi_Q), e_1=sin^2(phi_Q); the owned exact return certificate
gives 0<e_1<e_0<1/2. On the marked interaction the operator is fixed;
A_n changes its actual incident preparation and is undone before the
terminal comparison. At a common paid N the FULL balanced endpoints
are conjugate by A_n. The actual input projector contains all DATA and
commutes with A_n. Hence the complete heat and return determinant have
exactly the SAME values for every n, while

    B_window,n=H_ref(N,D_full)+J_ref,
    q_n=(e_0+e_1)/2+(e_0-e_1)p^3 u_n/2,
    u_n=cos(2n theta).                                  (229)

Here H_ref denotes that common full thermal value, not7j's unrelated
fixed-middle reporter price. This window starts with Omega_0 supplied
at its initial boundary. It does not include the earlier generation of
that input in its clock. Its real historical preparation and price are
not assigned zero; the FULL initial-blank clock is computed below.
All actual modes of each declared window are retained. The example
is a native apparatus/source witness, not a claim that its diagonal
two-mode matrix is the original nonvacuum42-field geometry.

Its ACTUAL reference-complete registered gain is h(q_n). Its comparison
source and finite nonzero contrasts are therefore

    D_u I_ref=log[(1-q)/q](e_0-e_1)p^3/2>0,
    (I_b-I_a)/(u_b-u_a)
      =(e_0-e_1)p^3/2 * [h(q_b)-h(q_a)]/(q_b-q_a)>0.    (230)

The finite native codes n=1,67,1161 give a two-sided comparison about
u_1=p^3. All inverses, source routing, copies and real identity padding
are counted. At Q=33 their unpadded stage totals are202+12n; the paid
common clock is14138. No continuously variable native pulse or equality
between unequal-duration clocks is used. The benchmark uses exact native
operator identities and algebraic endpoint probabilities, with separately
labelled numerical logarithms; it does not simulate a huge heat matrix.

These are hardwired native configuration comparisons on the same declared
quantum input boundary. Their use as physical variation tests retains
the actual controller-admission premise. They do not claim that different
programmes are unpriced alternatives inside one fixed autonomous decoder;
that application needs its entire stored-program carrier and preparation.

The read-only CLASSICAL oldRIGHT contract also has a strictly nonzero
gain source. Put b_e=(e_0-e_1)/2. On the local interval containing all
three native u values,

    D_u I_reg=b_e[p h'(q_0)-p^2 h'(q_1)]>0.

The exact algebraic bounds are49/50000<e_0<1/1000,
e_1>1/10000 and1/5<u<3/10. They imply q_0<1/1000,
q_1>1/2500, hence h'(q_0)>6 and h'(q_1)<8. The elementary inequalities
8/3<exp(1)<3 prove these logarithmic bounds. The derivative is therefore
greater than b_e(14p-8)>0. No inaccessible oldRIGHT phase test is needed
for this specified classical-record component.

### The complete source now has an explicit required work reaction

Equations(229)-(230) expose the WINDOW price-binding application. If a
proposed binding on that supplied-input task identifies its Book covector with a
nonzero multiple of the gain-price covector, then on this allowed
prep/controller comparison its genuine total Cost source must obey

    ell D C_actual=D I_ref.                             (231)

For a full value/divided-difference binding the corresponding finite
condition is ell(C_b-C_a)=h(q_b)-h(q_a). A merely asymptotic source
binding instead needs its real normalized secant/lift error budget;
it does not imply an exact value equality between arbitrary code words.
The work reaction(231) is a result to derive from the actual ledger,
not a compensator inserted into it. A task can exclude this relative
preparation orbit only through its genuine admissibility/correctness map.

Equal primitive inventory or a common N alone does not establish
D C_actual=0. Minimal description length, executed stages and actual
physical work keep their owned distinct meanings. Nor does a fixed-width
CX bit archive execute the original variable-length0/10 writer; its
one/two charge and branch durations cannot be assigned here. The books'
feedback partition log Z=beta H+J and bare master H+J also keep their
different relative coefficients at beta!=1.

### Include the actual historical preparation inside the full clock as well

Do not extend the window plateau to an uncomputed physical prefix.
Execute P=G_d;CX(d,r) while historical r is still fresh, then seal r
and execute the complete word W_n of(228), including its real padding.
The same full initial boundary now has d,r,h,a blank and arbitrary
protected source-spin. Its full monodromy is F_n=W_n P, its common
actual clock length14140, and its actual initial cut rank4. No later
gate touches r. The old supplied-input window instead had rank16.
Both cuts are derived from their explicitly different input tasks.

Let c_0=cos(3phi_Q), c_1=cos(phi_Q),
g(u)=(c_0+c_1)/2+(c_0-c_1)u/2. With i_initial the actual blank-input
embedding, the exact full return corner and defect are

    i_initial^dagger F_n i_initial=sqrt(p)g(u_n) I_spin,
    E_full=[1-p g(u_n)^2] I_spin,
    J_full=-4 log[1-z(1-p g(u_n)^2)].                   (232)

This includes the failure to return the historical preparation itself,
not only the new binary report. It is generally NOT constant in n.

The entire full-clock heat has a small exact spectral evaluation.
Put c_n=cos((1-2n)theta),
chi_+=acos(sqrt(p)cos(phi_Q)) and
chi_-,n=asin(c_n sin(phi_Q)). Define the four phase representatives

    omega_1=2phi_Q+chi_+,       omega_2=2phi_Q-chi_+,
    omega_3=2phi_Q+chi_-,n,     omega_4=2phi_Q+pi-chi_-,n.
    Z_full=32 sum_(j=1)^4 K_N(omega_j),
    K_N(t)=sum_(k mod N) exp[-beta_clk(1-cos((2pi k+t)/N))]. (233)

The complete eight signed phases each have multiplicity8 from the
bank sectors and source-spin. Pairing Hodge degrees gives the factor32
in(233), because K_N is even. All2N*64 modes remain. The decomposition
uses mathematical Fourier frames of the historical bit and bank, not
free physical preparations or detectors. It is checked against the
actual native small word before using the long-clock spectral formula.

On the local positive-sine u-chart,
c(u)=sqrt(p)u+p sqrt(1-u^2) and
chi_-'(u)=sin(phi_Q)c'(u)/sqrt[1-c(u)^2 sin^2(phi_Q)].
With S_K=sum_j K_N(omega_j), the WHOLE prefix source is

    D_u H_full=chi_-'[K_N'(omega_3)-K_N'(omega_4)]
                                                    /(beta_clk S_K),
    D_u J_full=4z[-p g(u)(c_0-c_1)]/[1-z(1-p g(u)^2)],
    D_u B_full=D_u H_full+D_u J_full.                  (234)

K_N' differentiates its actual complete clock-mode sum. The historical
prefix is fixed as a word, but its full thermal/return cross-source
in(234) cannot be set to zero; in particular D_u J_full>0. A cancellation
in the total source at other beta,z would need its own calculation.
In particular this is not obtained by putting a
constant preparation charge beside the old window heat. The native
probabilities q_n are unchanged; only the price boundary has been enlarged.

For the actual configured comparison delta=1/16, beta_clk=512N^2,
z=1/4, N=14140, nonflatness of the FULL Book price is certified without
relying on the numerical heat sum. Both exact Q(p) return-defect gaps
E_67-E_1 and E_1-E_1161 exceed10^-6. The feedback derivative with
respect to E exceeds1. Every clock mode is retained in the upper heat
bound and one genuine low branch gives its lower bound, yielding
heat oscillation<561/(12800N^2)<10^-8. Consequently

    B_full,67-B_full,1>9*10^-7,
    B_full,1-B_full,1161>9*10^-7.                       (234a)

These are strict bounds on THIS specified finite native family, not a
nonzero-total-source theorem at arbitrary beta,z or a GR root test.

For the chosen registered oldRIGHT-Z algebra the FULL gain is
h(p)+I_reg,window. The DATA-only full gain is likewise its window value
plus h(p), while the reference-complete gain stays h(q_n): any independent
mixed protected-spin entropy cancels from gain. OldRIGHT was not a
passive input reference before P created it, so the window reference-DPI
identity is not applied across that preparation. All input/conditional
entropy baselines and actual initial masks remain explicit.

For a PROVED nonzero covector gain kappa_src, the complete source-binding
test DB_full=kappa_src D(ell C_actual-I_chosen) therefore requires

    ell D C_actual=D I_chosen+D B_full/kappa_src.        (235)

I_chosen must use the actual specified future algebra. The gain is not
fitted on this one plane; an action-level field-dependent multiplier
would retain its product derivative as usual. A finite value binding
with constant gain has the corresponding full DB increment, whereas an
asymptotic covector binding retains its actual secant/lift errors.
Equation(231) is recovered only for the old supplied-input window or
after a genuine proof eliminating the full-prefix source. The source
map(234), rather than an omitted preparation, is now available to the
same-execution physical price consumer.

The substituted component is precise: the actual copied native word now
has a checked future-memory handoff, its full registered quantum gain and
independent preparation cotangent, with a same-initial-state nonzero
native source witness. The remaining complete-price application must
supply the REAL full reaction(235), justify a different physical information
algebra, or prove the actual constraint excluding that comparison.
It must also address7w's geometric feedback source(220)/(223); a pointer
gain computed here is not permission to append -h(q) to an already
complete Book action. Native physical valuation/selection and full joint
stationary refinement remain open. No GR_closed/raw216 promotion follows.


## 7y. Execute the terminal 0/10 code and retain its complete new Book source

**25 October native-realization application.** The missing output operation
named in7x is now constructed, using only the existing native operations:
append `CX(h,t0);CX(h,lambda)` BEFORE the final archive seal, with THREE
actual fresh blank wires `t0,t1,lambda`. The unchanged tail `t1=0` is a real
retained wire. A typed parser reads the legal containers `000` and `101`
as the original binary codewords `0` and `10`. It recovers one RAW
direct/return letter `[not b]`; Lean's `weightExp` consumes those RAW
letters, not the encoded binary digits. Thus its encoded length is
exactly1+b. The same all-input programme, historical preparation, protected
spin and oldRIGHT remain. No gate touches oldRIGHT after its original seal.

The implementation, complete sources and source conventions are in
[the writer proof](sources/d0_native_terminal_code_writer_2026-10-25/WRITER_PROOF.md)
and [the full Book proof](sources/d0_native_terminal_code_writer_2026-10-25/BOOK_PROOF.md),
with [literal native helper](sources/d0_native_terminal_code_writer_2026-10-25/terminal_code_writer.py)
and [bounded checker](sources/d0_native_terminal_code_writer_2026-10-25/check_terminal_code_writer.py).
This is an application of the owned Golden code/refinement and actual7x
execution, not a new geometric/root search. It supplies an implemented
code/readout effect; physical inclusion of that effect in full Cost remains
a separate binding obligation.

Write `Y_n=E(F_n tensor I_8)`, with the two actual CX in `E`. For ANY old
64-dimensional input, with only the NEW container initialized, the exact
pullback of its declared length is

\[
 j^\dagger Y_n^\dagger(I+\Pi_{\lambda1})Y_nj
       =I+F_n^\dagger\Pi_{h1}F_n,\qquad
 j=I_{64}\otimes|000\rangle,\qquad C_{\rm code}=1+q_n.       (236)
\]

This all-input identity includes incident coherences; its preparation and
operator derivatives are explicit, with moving cut/report terms retained
when those interfaces move. It does not assign this tariff to a bare G,
CX or SourceI. The complete output remains coherent. Its redundant code
copies contribute ONE report; tracing them and the original bank gives
exactly7x's CQ blocks. Reference-complete, DATA-only and registered-oldR-Z
Info are individually preserved, with their different conditional entropies
and full historical h(p) baseline. No extra Info is credited for the copies.

The new complete fibre is512, the initial cut rank is4, and the actual
common expanded clock is14142. All1024N=14481408 paired modes are retained.
Two primitive CX stages are executed in BOTH branches: encoded length1/2
is not their runtime or a proved physical proper time. A consumer requiring
serial emission/stopping must supply its real cursor, pending0/done states
and paid transitions. No physical decoder/work cost is declared zero.

There is a useful exact full-source simplification, and a necessary change.
Since the full blank return row already fixes h=0, its corner is unchanged:
`i_new†Y_n i_new=i_full†F_n i_full`. Thus at the same z the rank4 feedback
is still `J_Y=-4 log[1-z(1-p g(u)^2)]`. In contrast, diagonalizing the
ACTUAL parity `X_t0 X_lambda` gives TWO full sectors, each multiplicity4:
`spec(Y_n)=4 spec(F_n)+4 spec(Z_h F_n)`. The unused tail and every invalid
unprepared container column remain in those multiplicities. In particular,
the old heat cannot be reused as a free constant or multiplied by8.

The existing four +/- phases omega_j of F_n and the four NEW +/- phases
nu_j of Z_hF_n give the exact complete partition

\[
 Z_Y=128\left[\sum_{j=1}^{4}K_N(\omega_j)
                    +\sum_{j=1}^{4}K_N(\nu_j)\right],\quad
 K_N(t)=\sum_{k\bmod N}e^{-\beta_{\rm clk}[1-\cos((2\pi k+t)/N)]},
 \qquad H_Y=\beta_{\rm clk}^{-1}\log Z_Y.                    (237)
\]

Here `nu=(psi_+,pi-psi_+,psi_-,pi-psi_-)`,
`psi_+=acos(p-p² cos(2phi_Q))/2`,
`psi_-=acos(c(u)²+[1-c(u)²]cos(2phi_Q))/2`, and
`c(u)=sqrt(p)u+p sqrt(1-u²)` on the same positive-sine chart.
The two additional CX change the true full spectrum, despite preserving
the blank-return corner and the observed registered law. The exact small
native factors independently confirm both old and new phase sectors;
the long calculation uses their proved reduction, rather than claiming
an unrolled14142-stage512-dimensional simulation.

Put `B_Y=H_Y+J_Y`. On the WHOLE mathematical comparison interval
u in[1/5,3/10], with Q33, actualN14142, fixed z1/4 and configured
`beta_clk=512N²`, the complete raw H+J source obeys

\[
 D_uJ_Y>1/5000,\qquad |D_uH_Y|<1/10000,\qquad
 D_uB_Y>1/10000.                                          (238)
\]

This is an analytical inequality, not a floating sign test. The original
exact Q(p) cosine bounds give `cos(phi_Q)-cos(3phi_Q)>39/100000`,
g>.999 and p>.6. The rank4 derivative of J then exceeds1/5000.
For the complete heat, every eigenphase speed is bounded by
`||D_uY|| <=1/sqrt(1-u²)`. Differentiating ALL clock roots bounds the
raw heat source by `1/[N sqrt(1-u²)]<1/10000`; repeated eigenvalues
do not invalidate this trace bound. Both full native finite gaps also
remain strict: B_67-B_1 and B_1-B_1161 exceed9*10^-7. The NEW all-mode
heat oscillation is below `159/(3200N²)<10^-8`; no old-N heat bound is
silently reused. These bounds are scoped to this configuration/chart.

The actual declared code length does not supply the missing Info reaction.
For b_e=(e0-e1)/2>0 and ell=log(phi), the same registered algebra gives

\[
 R_{\rm code}:=D_u\mathcal I_{\rm reg,full}-\ell D_uq
  =b_e\{p h'(q_0)-p^2h'(q_1)-\ell p^3\}
  >b_e(14p-8-\ell p^3)>3b_e/20>0.                         (239)
\]

Thus the registered code-minus-Info component has strictly NEGATIVE source
on that interval, whereas this full H+J component has strictly POSITIVE
source. The implemented encoder does not erase the work/normalization
problem exposed in(235). For example at native n1 the numerical unit-u
sources are `DI_reg-ell Dq=0.00064777381763829...` and
`DB_Y=0.00030092514630344...`; their strict signs follow from(238)–(239),
independently of the displayed non-interval decimal evaluations.

There is NO theorem here that `C_actual=C_rest+1+q`. A physical additive
ledger binding, identifying this declared code length with an actually
charged component and independently deriving all other charges, must be
supplied. `C_rest` cannot be defined by subtracting a desired source.
If that binding and a genuine source transport with nonzero derived gain
kappa are established, the exact remaining equation is

\[
 \ell DC_{\rm rest}
   =D\mathcal I_{\rm chosen}-\ell Dq
      +\kappa^{-1}(DB_Y+DB_{\rm other}).                    (240)
\]

`B_other` retains original Rayleigh/other Book terms and every additional
real source absent from the displayed H+J calculation. If the consumer
binds precisely B_Y, its other source must actually vanish or be absent;
then positive kappa forces a strictly positive rest-cost reaction on this
registered preparation plane. An uncomputed R is not set to zero. A
variable action-level multiplier retains its product derivative; kappa
is not fitted from this plane. Alternate physical Info algebras retain
their actual separate sources and future tests.

**Parent substitution and remaining application.** The explicit terminal
code operation, typed original parser, full-input length effect and
complete new H+J source replace an unspecified output-code construction
in7x. The zero-other-source shortcut fails on this actual model. The next
application must derive the real all-input primitive/controller/decoder
charge and its physical additive ledger/Info binding, then include every
other Book term and independent upstream equation. This is supporting
native realization, not selection of an action by a code label. The
u-source is NOT the physical42-covector: its actual map, norm and gain
remain necessary before either strict unpadded root tolerance can be used.
No comparison with1e-22 or global GR no-go is inferred. Hardwired native
configuration comparisons do not establish continuous pulse or autonomous
controller-variation admission. Same-execution physical selection, full
joint stationary refinement, GR_closed and raw216 remain open.

Reproduce this changed operation from repository root:

    python3 02_REGISTRY/research/sources/d0_native_terminal_code_writer_2026-10-25/check_terminal_code_writer.py --output /tmp/native_terminal_code_writer.json


## 7z. The same clock-Rayleigh source cannot supply the missing compensation

**25 October direct-Book application.** Full identification of Cost−Info
is NOT a universal prerequisite for a faithful native GR realization.
The independently owned direct route in
[paid-writer19.1](A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#191-correct-the-parent-route-before-applying-it)
uses the actual selected Book03§03.25 operators and admitted variations.
That bare master is H+J. A Rayleigh term R is a DIFFERENT binding, with
its own state/operator and independent preparation equation. This section
applies the owned same-clock HJR interface(72) of that writer to the
implemented7y clock; it does not append R to the original bare master.

The missing operand in(240) therefore cannot be filled by naming it
Rayleigh without computing its source. For the literal clock of7y, the
two natural proposals can now be decided. At the actual stage0 birth,
its clock energy is constant. Even if that fixed birth preparation is
relaxed to ANY full fixed-spectrum preparation orbit and its independent
Euler equations solved, its energy source is too small to cancel7y's
strict H+J source. This is a new application of the owned all-clock-root
bound and preparation Euler, not another Cost-assignment ambiguity proof.

Let T be the actual primitive cyclic unitary shift, retaining every gate
and wire, with T^N containing Y_n. Its bare paired Hodge operator is
`Delta_clk=I-(T+T†)/2`, on BOTH degrees. Keep7y's full512 fibre,
actualN14142, rank4return cut, fixed z1/4 and beta512N². A normalized
Rayleigh density gives

\[
 R_{\rm clk}(u)=\operatorname{Tr}[\sigma(u)\Delta_{\rm clk}(u)],
 \qquad
 DR_{\rm clk}=\operatorname{Tr}(\sigma D\Delta_{\rm clk})
                         +\operatorname{Tr}(\Delta_{\rm clk}D\sigma).
                                                               (241)
\]

All operators and states are in the ORIGINAL stage coordinates. For
N>1 the stage0 diagonal block of Delta_clk is identity. Consequently
`sigma=|0><0| tensor rho`, with ANY normalized incident rho, has
R_clk=1 and D_uR_clk=0, including moving rho and its correlations.
Both Hodge degrees retain this identity for a normalized density on
their direct sum. No factor2 is inserted in this expectation. Thus
THIS stage0 term leaves the strict source(238) unchanged. Such a birth
state need not solve an unrestricted preparation Euler; this is a
separate exact application on the fixed birth constraint.

### All independently stationary preparations on one fixed-spectrum orbit

For the alternative preparation domain, assume explicitly that sigma(u)
stays on ONE normalized fixed-spectrum unitary orbit across u, and is
stationary with respect to EVERY independent full unitary preparation
at fixed operators/cut. The already-owned Euler then gives

\[
 [\sigma,\Delta_{\rm clk}]=0,\qquad
 D\sigma=[A,\sigma]\ (A^\dagger=-A),\qquad
 \operatorname{Tr}(\Delta_{\rm clk}D\sigma)=0.            (242)
\]

Commutation alone is insufficient if occupation weights change along
the proposed section. The fixed orbit, or a separate proof that the
last trace vanishes, is essential. For example, transferring occupation
between two distinct clock eigenvalues preserves commutation at every
point but adds their energy difference times the transfer velocity.
The equation is therefore not imposed on a changing RIGHT Gram.

The COMPLETE clock eigenvalues are

\[
 \lambda_{jk}(u)=1-\cos[(2\pi k+\theta_j(u))/N],
 \qquad k\bmod N,
 \qquad e^{i\theta_j(u)}\in\operatorname{spec}Y(u).       (243)
\]

Every local phase speed is bounded by ||Y′||. Thus every eigenvalue
speed of Delta_clk is at most ||Y′||/N, including all repeated modes.
At an eigenvalue of multiplicity>1, the first-order speeds are the
eigenvalues of the compression of DDelta_clk to that eigenspace.
Since sigma commutes with Delta_clk, only those spectral diagonal
blocks contribute to Tr(sigma DDelta_clk). Their positive normalized
weights give the bound

\[
 |D_uR_{\rm clk}|
       \le {\|Y'(u)\|\over N}
       \le {1\over N\sqrt{1-u^2}}.                    (244)
\]

This uses the existing phase-speed theorem of
[BOOK_PROOF(B14–B15)](sources/d0_native_terminal_code_writer_2026-10-25/BOOK_PROOF.md#5-a-strict-configured-source-bound-including-every-heat-mode).
It is NOT a bound on the norm of the derivative of an arbitrary
matrix Nth root; noncommuting directions need not obey that bound.
Gauging actual prefixes to a closing holonomy is only a calculation
basis. Its moving commutator has zero trace against stationary sigma;
the state is transported too. It is not frozen or replaced physically.
Without preparation stationarity, a moving prefix gauge can produce
a large R derivative even when the whole monodromy is constant. The
bounded checker retains exactly this hostile control.

On the WHOLE comparison interval u in[1/5,3/10], N14142 gives
`1/[N sqrt(1-u²)] <=10/(14142 sqrt(91)) <1/13000`.
The same bound applies to raw H by the already-owned complete thermal
trace identity. Combining it with the actual rank4 return lower bound
J′>1/5000, every smooth section satisfying(242) therefore obeys

\[
 D_u(H_Y+J_Y+R_{\rm clk})
 >{1\over5000}-{2\over13000}
 ={3\over65000}>0.                                    (245)
\]

This keeps the genuine unit-coefficient Rayleigh interface when that
interface is actually selected. A different coefficient, operator,
moving clock/cut/temperature or additional stack term keeps its own
source; it is not absorbed into this estimate.

### Optimized preparations, including eigenvalue crossings

Fix any normalized nonnegative density spectrum w once for the whole
interval. Its Rayleigh minimum over the full unitary orbit is exactly

\[
 E_w(u)=\min_{\sigma\in\mathcal O_w}\operatorname{Tr}(\sigma\Delta_{\rm clk})
       =\sum_j w_j^\downarrow\lambda_j^\uparrow(u).       (246)
\]

For pure preparations, or minimization over all densities, this is
lambda_min(Delta_clk). For a fixed MIXED spectrum it is the displayed
weighted ordered sum, not in general lambda_min. Every ordered clock
eigenvalue has the same Lipschitz bound(244); normalized positive
weights preserve it. Hence H+J+E_w is strictly increasing, even at
crossings where no differentiable eigenvector/preparation selector
exists. More explicitly, for u<v in this common chart,

\[
 (H_Y+J_Y+E_w)(v)-(H_Y+J_Y+E_w)(u)
             >{3\over65000}(v-u).                        (247)
\]

No physical ground-state preparation or reset is claimed. This is the
value of the stated mathematical relaxation and an all-orbit bound.
The same fixed-spectrum hypothesis is crucial here too.

The native Q33 endpoints n1,67,1161 satisfy the exact Q(p) inequalities
`u_67-u_1>1/50` and `u_1-u_1161>1/100`, on the same positive-sine
branch. Consequently BOTH corresponding optimized HJR gaps exceed
4*10^-7 for EVERY fixed w, including the pure relaxation. These are
finite configuration comparisons at the actual common clock, not a
claim that an autonomous programme already varies a hardwired n.
The full modes underlying(246) remain the original14481408; evaluating
the pure ground via principal phases deletes none of them.

**Parent route change.** Under the actual same-clock Rayleigh binding,
neither stage0 birth nor independently stationary FULL fixed-spectrum
clock preparations supply the unknown cancellation in(240). This rules
out those two proposed completions of THIS execution. It does not prove
that its physical preparation domain is that full orbit. Sealed internal
oldRIGHT, source-spin-only operations, a fixed stage/blank sector and
causally generated states can restrict variations and need not imply
(242). A genuinely external spectator reference with fixed Gram may
realize the orbit only after that active/reference map is proved; no
rotation of the internal immutable records is thereby authorized.

The next direct-Book application must exhibit its actual selected X_N,
one admitted field/cut/preparation tangent and the complete source on
that tangent. A spatial residual operator, moving RIGHT Gram, actual
constraint reaction or another original stack term may differ; those
sources must be computed on the same process. Cost−Info remains one
separate sufficient route rather than a newly imposed universal gate.
No flat/global-scale argument is transplanted to a fixed curved collar.
This unit-u theorem is not the physical42-covector or its tiny-source
budget, and is not a no-go for other native actions or GR. Selection,
all independent equations and common GR refinement remain open.

The new [bounded application checker](sources/d0_native_clock_rayleigh_source_2026-10-25/check_clock_rayleigh_source.py)
uses small full clock controls and consumes the frozen7y source
receipt. It does not replay the old42 checks or unroll a long512/clock
matrix. Its floating examples are distinct from the analytical bound
and exact native u-gap arithmetic. Reproduce from repository root:

    python3 02_REGISTRY/research/sources/d0_native_clock_rayleigh_source_2026-10-25/check_clock_rayleigh_source.py --output /tmp/native_clock_rayleigh_source.json


## 7aa. Feedback first: complete original-query Book source and an exact sourced family

**25 October positive direct-Book composition.** A different missing
application can now be completed: use the ORIGINAL two-tick Golden query
as the whole return monodromy, rather than7w's heat-matching holonomy.
Its actual complementary determinant is already J2. Compute its WHOLE
clock heat, including the unmatched scene columns, and consume the
existing common-null all40+2 theorem. The result is an exact curved
nonvacuum family of THIS complete H+J operator chart, with its coupling
derived from the action and controlled recovery to the original family.
It is not a physically selected native X_N or a closure of independent
off-dictionary control equations.

The [full proof](sources/d0_query_feedback_first_book_2026-10-25/PROOF.md)
and [bounded source checker](sources/d0_query_feedback_first_book_2026-10-25/check_query_book.py)
consume the actual query/cut of
[the original local LEFT-controlled source](A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md),
the [full all40 arbitrary-Brinkmann reduction](../gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md)
and [midpoint recovery](A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md).
No new geometric action, density, root search, detector, entropy assignment
or fitted coefficient is used.

### One full query carrier, rather than a selected output law

For each actual old LEFT/regular/reference copy retain the original
four-tail by22976-scene carrier. It has Q=528 matched scene pairs,
each carrying the FULL8 query, and d0=21920 unmatched scene columns,
each still carrying the FULL4 tail. At a matched pair let

\[
 U_q=T_E^2\otimes G_s^2,\qquad
 E=p^2(1+x),\quad s=p-p^2y,\quad x=\tau_h f,\quad y=\tau_h q,
 \qquad p=\varphi^{-1},\quad\tau_h>0.                  (248)
\]

Here f,q are the original source-compatible star and two-real-CAR
densities, including the exact inverse-PF map. Use ONE common fixed
weakening scale tau_h per mesh. The old integer multiplicities c_i,
including inactive addresses, are not replaced by measured probabilities;
C=sum_i c_i is their actual positive integer total. Vary only the
original active f_i,q_i. Inactive addresses keep f_i=q_i=0.

The original rank2 cut is span{|0>,|2>} in each matched8 block and
zero on unmatched scene directions. Thus its full feedback is exactly
the owned J2, with its true528 and c_i factors. If b=s² and
`L_E=4E(1-E)`, its two effect eigenvalues are
`B=4b(1-b)` and `A=L_E+(1-L_E)B`, and
`j=-log(1-zeta A)-log(1-zeta B)`, with the ORIGINAL zeta=2^-20.
The cut rank is2QC, not the number of occupied prepared input states.
That global rank need not be a power of two: implementing the actual
scene/address predicate is distinct from naming a local blank-wire mask.

Six CONFIGURED operator slots factor U_q: tail rotation, tail CX,
scene rotation, repeated twice. The local8 common-null value has its
four-G/two-CX word. A matched-only scene rotation on the complete scene
is not automatically one global bare G/CX primitive. For the stated
operator-clock chart, choose any even N>=6 by actual two-CX identity
stages. A genuine global native compiler retains its full expanded N,
all source/controller wires and its own admission. All heat formulas
below depend on the endpoint and the TRUE clock length; they do not
identify configured slots with an unproved primitive counter.
Use the owned transported-prefix return cut: its only leakage is the
closing wrap and its determinant is that same fixed-input-cut J2.
The generated intermediate cut is not frozen during differentiation.

Put theta_E=asin(sqrt(E)), theta_s=asin(s). The local8 eigenphases are
`+/-2(theta_E+theta_s)`, `+/-2(theta_E-theta_s)`, and
`+/-2theta_s` each twice. The unmatched4 phases are0,0,+/-2theta_E.
The latter modes have zero feedback but a NONZERO geometric heat source.
For the full paired clock define

\[
 K_N(t)=\sum_{k\bmod N}e^{-\beta[1-\cos((2\pi k+t)/N)]},
\]
\[
 Z_8=4\{K_N[2(\theta_E+\theta_s)]
        +K_N[2(\theta_E-\theta_s)]+2K_N(2\theta_s)\},
 \quad Z_4=4\{K_N(0)+K_N(2\theta_E)\},
\]
\[
 Z=\sum_i c_i[Q Z_{8,i}+d_0 Z_{4,i}],\quad
 H=\beta^{-1}\log Z,\qquad J=Q\sum_i c_i j_i.          (249)
\]

Every `2N*4*22976*C` clock mode occurs. No output-only thermal trace,
postselection or omitted unmatched/source sector is used. This is the
declared four-tail continuation of the original query sector. Any
additional AF/frame/implementation complement in a larger physical
execution needs its actual operator and source; it is not made a
field-independent identity by calling it work. Likewise extra spin or
reference dimensions have their true cut ranks and thermal factors.

### The complete first source on the positive common-null family

On Sigma, f_i=q_i=0 at every active address, so theta_E=theta_s=theta
with sin(theta)=p. Define

\[
 R_0=1-\zeta+\zeta p^{12},\qquad Q_0=1-\zeta+\zeta p^6,
 \quad a_0={4\zeta p^{11}\over R_0}>0,
 \quad b_0=-8\zeta p^6\left({p^6\over R_0}+{1\over Q_0}\right).
\]

These are the ORIGINAL j_x,j_y; lambda_minus=b0/a0 is the already
owned exact finite-zeta coefficient. Let Z_Sigma denote the FULL(249)
partition at this same point, including all C copies. Since K_N'(0)=0,
the per-copy heat coefficients in the x,y source are exactly

\[
 h_x={4\sqrt p[QK_N'(4\theta)+d_0K_N'(2\theta)]\over\beta Z_\Sigma},
 \quad
 h_y={-8p^{3/2}Q[K_N'(4\theta)+2K_N'(2\theta)]\over\beta Z_\Sigma}.
\]
\[
 a_N=Qa_0+h_x,\qquad b_N=Qb_0+h_y,
 \quad\lambda_N={b_N\over a_N},\qquad
 D(H+J)|_\Sigma=\tau_h\sum_i c_i(a_NDf_i+b_NDq_i).     (250)
\]

This identity is on EVERY ambient field direction before using the
Brinkmann ansatz. The global log partition is not silently made a sum
of local heats: its actual GLOBAL denominator Z_Sigma is retained.
In particular h_x,h_y have one inverse C, while J has its extensive
copy count. Omitting the21920 unmatched tails changes h_x and the
derived lambda_N. Arbitrary fixed true nonuniform LEFT counts preserve
the common coefficients and use the owned inverse-PF density identity;
arbitrary site-dependent tau_i would require its own corrected dictionary.

At fixed beta and N, independent preparation-state variations have no
source in this bare operator functional. Changes of a causal factorization
preserving the ENTIRE monodromy, cut and N likewise preserve H and J.
Preserving just an effect, prepared mean or reduced query channel does
not suffice. A field-dependent preparation prefix inside the actual
clock changes the endpoint to U_q P_field and can change both(249) and
the true corner; its source must be computed rather than removed.

### Nonzero source gain and exact recovery schedule

The owned all-phase speed bound applies to all modes. Under a homogeneous
x or y variation on this original chart,
`||U_x||<=sqrt(p)` and `||U_y||<=2p^(3/2)`. Hence, for ANY fixed beta>0,

\[
 |h_x|\le{\sqrt p\over CN},\qquad
 |h_y|\le{2p^{3/2}\over CN}.                            (251)
\]

If CNQa0>=2, then a_N>Qa0/2 and its operator-chart field-source gain is
nonzero. The actual ratio, rather than an independently chosen matter
term, satisfies the conservative uniform bound

\[
 |\lambda_N-\lambda_-|
       <{52\over C Q a_0 N}.                            (252)
\]

The exact rational inequalities309/500<p<619/1000 give
`|lambda_minus|<24`, `a0>4 zeta(309/500)^11`, and
`52/[528*4 zeta(309/500)^11]<2^23`. They prove the gain and recovery
bounds without relying on floating heat values or a tiny source fit.

Now CONSUME the original all40+2 reduction with its source coefficient
replaced by the DERIVED lambda_N. It gives, exactly at each finite mesh,

\[
 \Delta_h^\perp H(u_{j+1},x,y)=-4\lambda_N E_j,
 \qquad E_j=\|D_u^+\Psi_j\|^2,
\]
\[
 H(u_j,x,y)=-\lambda_N E_{j-1}(x^2+y^2)+W_{h,j}(x,y),
 \qquad \Delta_h^\perp W_{h,j}=0,                       (253)
\]

with the SAME original advanced Cartan links. All16 coframe,24 proper
link and two independent real material Euler rows of THIS H+J chart
are zero. The field is curved and nonvacuum for nonzero allowed Psi
and the original wave profiles. The supporting theorem allows arbitrary
constant lambda and therefore needs no fresh gravity-root search.
The finite collars must match THIS lambda_N; old fixed lambda_minus
collars are not reused as if the metrics were equal.

For h=1/L choose actual even clock lengths

\[
 N_h\ge2^{23}L^2.
 \quad\Longrightarrow\quad
 a_{N_h}>Qa_0/2,\qquad|\lambda_{N_h}-\lambda_-|<h^2.    (254)
\]

The six-slot operator chart can use equality in this schedule through
its explicit identity padding. A real native body can be longer; use
an even common N_h at least both this bound and its actual body length
plus4, with the owned2/5-CX padding. The source bound only improves.
This is a resource bound, not free padding or an unproved efficient
global compiler. The old midpoint construction and harmonic correction
then give the SAME O(h²) metric/curvature/matter recovery to the fixed
continuum Einstein-null-scalar solution with lambda_minus. At finite
h these exact metrics use lambda_N, rather than being one identical
continuum metric sampled on every grid.

**Precise substitution and remaining physical map.** The formerly
uncomputed whole original-query heat source is now evaluated and used
in a positive exact all-field solution and its recovery. This extends
the original J2-only solution to the complete direct Book H+J on the
declared full query operator carrier. It does not transfer the strict
unpadded CQ interval root, which belongs to another scalar price.

The missing arrow is still admission/selection of this smooth query
chart and its field/control/cut tangents as the actual physical X_N.
The constant Golden word on Sigma proves its value, not its nonzero
transverse source. Hardwired all-column native catalogues can approximate
values and finite source secants with actual error/gain/stencil budgets;
their countable word domain does not itself supply a continuous native
Euler equation or an exact stationary finite-code execution. Genuine
birth-to-field preparation, off-dictionary controls, moving cut, clock/
fugacity/observer and other selected stack equations remain explicit.
No physical selector, arbitrary matrix tangent, reset, new action or
GR_closed/raw216 promotion is inferred from this positive operator result.


## 7ab. A literal native return adapter and its independent correlation source

**25 October native-operation substitution.** The moving RETURN operation
of the original J2 query has a short exact implementation in the already
declared G/CX/SourceI profile. No moving target gate, fixed-table compiler,
fair factory or herald is needed for the processor. The new execution
reproduces the full rank2 returned matrix and both complementary bands.
It also makes the remaining programme-law problem concrete: an exact
native edit preserves both marginal inputs and changes the complete
Book price. Field-to-programme admission and joint stationarity therefore
remain separate from this implemented return map.

The [proof](sources/d0_native_bilinear_return_echo_2026-10-25/PROOF.md),
[literal constructor](sources/d0_native_bilinear_return_echo_2026-10-25/native_echo.py)
and [all-column checker](sources/d0_native_bilinear_return_echo_2026-10-25/check_native_echo.py)
consume the original returned matrix of7aa and the owned all-column
SourceI inverse. The factorization/conjugacy method is reused from7j/m;
the new application is the ORIGINAL two-band matrix return, rather than
a scalar engineered report or only a reduced DATA channel.

### The complete fixed processor and its actual raw word

Use fresh programme bits e=0,B=1, unknown DATA d=2, and arbitrary active
source-spin(3,4). The source port is e. Let X swap the DATA basis and
put

\[
 V=Z_eZ_BCX(e,d)\otimes I_{\rm spin},\qquad
 (V_{00},V_{01},V_{10},V_{11})=(I,-I,-X,X).            (255)
\]

Two SourceI operations give Z_e on ALL spin inputs. To get Z_B, route
the WHOLE programme bit through the source port using a three-CX SWAP,
apply two SourceI, and undo that SWAP. Then execute CX(e,d). Thus the
fixed V has EXACTLY11 raw stages:4SourceI and7CX. It restores spin
on all32 columns; all intermediate source interactions stay in the clock.
No operation acts on genuine oldRIGHT, even as control.

For product programme preparation A, with diagonal means E,b and no
initial correlation with DATA, execute A;V;the ACTUAL raw inverse of A.
The blank-programme isometry i retains DATA and all four spin inputs,
so its rank is8, full fibre dimension32. The exact return is

\[
 C=i^\dagger A^\dagger VAi
     =(1-2b)[(1-E)I-EX]\otimes I_4,
 \quad F=I_8-C^\dagger C=F_{\rm original,2}\otimes I_4,
 \quad J=4j(E,b).                                     (256)
\]

The factor4 is the real protected input rank, counted once. Programme
leakage is in the genuine complement and is not postselected away.
This reproduces the original RETURN operation on arbitrary DATA and
reference-entangled input; it does not reproduce its full8D logical
query or every subsequent test on failed/work branches.

There are actual finite codes, not just matrix values. Take
`A=G_e^kE;G_B^kB`, giving E=sin²(kE theta), b=sin²(kB theta),
sin(theta)=p. The owned raw inverse uses5 stages per port-G and11 per
off-port G, with its actual SWAP route. The completed body counts are
`G=2(kE+kB)`, `SourceI=4(kE+kB+1)`, `CX=7+6kB`, hence
`N_body=6kE+12kB+11`. The four pairs(1,1),(2,1),(1,2),(2,2) have
lengths29,35,41,47. Real cancelling CX pairs pad all four to N51.
There is no independently supplied programme state whose inverse is
assumed available: these exact native words prepare it and reverse it.

The fixed V is a symmetric involution, with eigenvalues+1 and−1 each
multiplicity16. Every WHOLE echo is conjugate to it. Therefore the
complete paired primitive-clock heat, including every programme,
source-spin, unused column and paid stage, is exactly

\[
 Z_N=32[K_N(0)+K_N(\pi)],\quad
 K_N(t)=\sum_{k\bmod N}e^{-\beta[1-\cos((2\pi k+t)/N)]},
 \qquad\mathcal B=\beta^{-1}\log Z_N+4j(E,b).         (257)
\]

All64N modes occur, or3264 at N51. The heat SOURCE is zero at this
actual common clock. The actual price changes when the clock/rank or
middle changes; neither is treated as an independent zero-source row.
Selective source-I availability keeps the existing apparatus-profile
premise; syntactic membership does not prove that physical availability.

### Exact original source, and the independent programme equation

At kE=kB=1 both programmes are ordinary G from genuine blanks and
E=b=p². The original two effect bands are exactly1−p12 and1−p6.
On the explicitly stated OPERATOR comparison
`E=p²(1+x)`, `b=(p-p²y)²`, the actual returned matrix gives

\[
 D\mathcal B|_\Sigma=4Dj=4(a_0Dx+b_0Dy),             (258)
\]

with the original a0,b0 and lambda_minus of7aa. Conditional on the
original physical field-to-product-programme map, the same inverse-PF
and all40+2 source theorem therefore applies with its unchanged ratio.
No thermal correction or fitted matter coefficient is inserted.
The continuous comparison is not an exact continuous finite-word
selector: native values and native finite edits are checked separately.

Independent programme controls do NOT become stationary. At the same
point both J_E and J_b are positive. The original all42 field-source
cancellation occurs only after their genuine field pullback; it cannot
annul a freely varied controller bias. For a real or complex pure
programme with probabilities p_w, let C=sum_w p_w V_w and
`Q=(1-zeta)I+zeta C†C`. Its actual preparation adjoints are
`o_w=-8zeta ReTr(Q^-1 C†V_w)`. At the product G programme every
p_w is positive, C has positive eigenvalues p6,p³, and o00<0 while
o01=−o00>0. Thus the programme's normalized pure-state covector is
nonzero even in real amplitude directions. Generated programme states
instead need their true causal constraints and terminal adjoints.

There are also finite native controls. At common N51, changing(1,1)
to(2,1) lowers J exactly. Nearer E-only native codes kE=67,1,1161,
kB=1 have E67<E1<E1161 in(.37,.4). Their actual body lengths425,29,
6989 pad to common N6993; exact band monotonicity gives B67<B1<B1161.
Long-word verification uses literal inventories and exact Q(p) arithmetic,
not an unrolled large32-column or6993-stage clock simulation. Whether
these code edits preserve a REQUIRED field/query task is a separate
admission statement; membership alone is not that statement.

### A native same-marginal correlation edit changes the full Book price

Independence in(256) is an actual hypothesis. V is programme-diagonal,
but a general joint law with t=p11−Eb has corner

\[
 C(E,b,t)=\{(1-2b)[(1-E)I-EX]+2t(I+X)\}\otimes I_4.   (259)
\]

The product preparer gives t=0. The equally literal native preparer
`A_corr=G_e;CX(e,B)` gives the pure state
`sqrt(p)|00>+p|11>`, with the SAME E=b=p² but t=p³. Its complete
echo has19 raw stages(2G,9CX,8SourceI);32 cancelling CX pad it to
the SAME N51 and input cut. The exact return, bands and price gap are

\[
 C_{\rm corr}=(pI+p^2X)\otimes I_4,\quad
 \operatorname{spec}F_{\rm corr}=\{0,1-p^6\}\text{ each four times},
\]
\[
 \mathcal B_{\rm product}-\mathcal B_{\rm corr}
       =-4\log[1-\zeta(1-p^{12})]>0.                 (260)
\]

The WHOLE heat is identical. Numerically this strict configured gap is
3.802852073155...*10^-6; its sign follows from the exact formula.
The local fixed-marginal correlation source is already nonzero:

\[
 \partial_t\mathcal B|_{E=b=p^2,t=0}
          =-32\zeta p^6/(1-\zeta+\zeta p^{12})\ne0.  (261)
\]

This is a concrete native obstruction to identifying the complete
programme by its two marginal means. The two preparations have different
joint/future laws and different return effects, so(260) does not claim
an admissible edit under an independently established product-law task.
That law must be generated or required by the real field/control map,
or the extra correlation source must remain in the physical equations.

**Precise substitution.** A literal all-column native processor and its
paid closing echo now supply the original two-band return; no moving
query-return oracle is left in this adapter. Its missing physical arrow
is the actual source of the two joint programme laws from the same
coframe/link/CAR record and its permitted variations. A full scene/AF
extension keeps every true cut rank, spectator and predicate; local
rank8 is not the global scene selector. Independent controller/cut/
clock/birth equations and the complete future-test map remain open.
The exact new return map does not by itself prove full physical GR.

Reproduce only this changed operation from repository root:

    python3 02_REGISTRY/research/sources/d0_native_bilinear_return_echo_2026-10-25/check_native_echo.py --output /tmp/native_bilinear_return_echo.json


## 7ac. Generate the two-band return from one canonical bank, retaining its matrix source

**25 October joint-source application.** Consume7ab's literal return
processor and7s's canonical geometry/CAR bank, read-only polynomial
encoder and first-conditional theorem. The changed mathematical input is
the FULL two-band matrix return, rather than7s's scalar weak reporter.
This construction generates the joint programme law on the prepared
section and controls arbitrary correlated pure-bank tangents there.
It does not infer independence from stationarity or discard7ab's native
correlation edit. Independent processor/control variations remain.

The [proof](sources/d0_native_matrix_collective_return_2026-10-25/PROOF.md)
and [bounded check](sources/d0_native_matrix_collective_return_2026-10-25/check_matrix_collective.py)
use the existing same-owner source interfaces. This is native realization
and source composition; the parent substitution is the previously
uncontrolled joint programme-input source of the implemented J2 return.
It is supporting work, not acceptance of the full native X_N domain.

### The actual return averages amplitudes before taking its determinant

Let a complete fresh ACTIVE bank be the deduplicated canonical state
xi(r) of7s, with its true geometry/material covariance and field
Jacobian. This ONE rank8-cut construction uses the explicit GLOBAL
aggregates A_h(Y)=sum_i c_i f_i(Y), M_h(Y)=sum_i c_i q_i(Y), with the
owned original fields, inverse-PF dictionary and actual fixed integer
counts c_i. Set X_h=tau_h A_h, Y_h=tau_h M_h and
E=p^2(1+X_h), b=(p-p^2 Y_h)^2. On a fixed compact chart choose a
computable constant tau_h>0 keeping both probabilities strictly inside
(0,1). These are the functions approximated by the encoder. There is
one global determinant; it is not a sum of local determinants off Sigma.

Every raw coordinate occurrence in the fixed E,b encoder uses
a distinct bank slot, as in7s(177); pad to a common finite k. Keep all
unused factors, source purifiers and scratch. Prepare n>=k fresh banks
from the SAME classical source setting; this does not clone an unknown
input or use immutable oldRIGHT as work.

A fixed finite real orthogonal A_* coherently prepares the uniform
ordered-injection label, routes distinct banks to these slots, and
executes the read-only coefficient encoders. On its logical comparison,
these encoders generate the two programme bits with the full joint
response on every raw input. Their polynomial/C1 approximation error
is retained; two mean values on a tied field curve are insufficient.
DATA and protected source-spin are untouched by A_*.

All injection labels are ACTIVE work, starting in real blanks. With
V the actual11-stage middle of7ab, the complete echo is

    S_Psi ; A_* ; V ; A_* inverse ; S_Psi inverse.      (262)

Here S_Psi prepares the ENTIRE bank from blanks inside this same echo.
It is not an independently supplied state outside the clock. Its
inverse also returns the label/encoder/source work to the fixed cut.
All failed return amplitudes remain in the complement. The cut retains
DATA2 and the original arbitrary spin4, hence rank8. In particular the
injection label is not added to the protected input rank.

For the Hermitian DATA-valued k-bank kernel K of the fixed encoder,
orthogonality of the injection labels gives the true return

    K_n = (n)_k^(-1) sum_iota K_iota,
    C_n(Psi) = <Psi,K_n Psi>_banks tensor I4,
    J_n(Psi) = -4 log det[(1-zeta)I2+zeta C_n,2^2].     (263)

On xi(r)^n, C_n,2 equals the unsymmetrized generated return, including
both bands. It equals the original C2(E,b) only to the accuracy of the
actual canonical encoder. Equation(263) is an AMPLITUDE compression:
neither the defects F_iota nor their log determinants are averaged.
The finite checks retain a correlated direction on which these
substitutions give different answers.

### A fixed native compiler supplies the processor without a free herald

A_* is one finite, computable, field-INDEPENDENT real orthogonal map.
The owned7w Golden/CX density on at least three legally addressed active
bits applies to its full active block. If needed, tensor one unused
ACTIVE blank bit with identity to obtain determinant+1. Its entire
two-dimensional complement remains in the heat. Positive G powers
approximate G inverse by compact rotation recurrence, so positive
G/CX words have the same dense closure. Enumerate those finite
words and certified error bounds until ||Ahat-A_*||<delta;
density and computability prove termination. No efficient installed
compiler or mesh-uniform complexity bound is asserted.

This deterministic full-column approximation replaces the fixed
selector/Boolean/coefficient circuit, including its preparation columns.
There is no conditional READY normalization in(263). Compiling this
fixed circuit does NOT itself prepare xi. For the source bank use actual
unconditional native preparations from fresh active blanks approximating
the full pure target at finite COMPUTABLE field points, with their state
error eta retained. The same fixed-dimension density argument supplies
such finite endpoint words;
it does not erase the old raw CAR seed's READY flag by conditioning.
An immutable unknown reference cannot be used in those preparations.
S_point acts only on the complete source bank and its own source
ancillas; the distinct injection/programme/encoder-work blanks stay
exactly zero before Ahat. Their independently admitted variation would
be an additional initial-work equation, outside this bank estimate.
The compiler acts only on active bank/programme/work bits, tensor
identity on DATA, source-spin and immutable oldRIGHT. The inverse
macros may use dirty source-spin but restore it on every column.

Reverse each ACTUAL raw word with7j's all-column SourceI inverse. A
finite comparison catalogue has one carrier and a common primitive
clock T, padded by the owned real two/five-CX identities. Every forward,
inverse, routing and padding stage is paid. No C1 finite-word selector
is inferred from the catalogue.
If the whole forward bank/encoder word has g_port port-G, g_off other
G and c CX letters, its closed body has exactly
6g_port+12g_off+2c+11 primitive stages before real padding.

The actual whole endpoint remains conjugate to V tensor I_allwork,
even when Ahat is imperfect. If D_full is its complete fibre dimension,
the two spectral multiplicities are D_full/2 each, and the paired heat is

    Z_T = D_full [K_T(0)+K_T(pi)].                      (264)

All2T D_full modes, including det-fix, unused banks and label work, are
present. This absolute heat has zero source at fixed actual T and
carrier; changing the clock, cut or fixed middle retains its own source.
The selective SourceI profile is the same conditional apparatus premise
as7ab, not a newly derived physical primitive.

### The full matrix logdet has a controlled correlated preparation normal

For the finite IDEAL encoder at a stated IID base, freeze its actual
return matrix C and Q=(1-zeta)I+zeta C^2. The compiled encoder generally
loses the exact one-slot alphabet; its gradient includes the separate
implementation debt below.
For one local spin4 copy, define the Hermitian bank score

    L = -8 zeta Sym_k Tr_DATA[(Q^(-1) C) K].           (265)

Its first differential is dJ=2 Re<dPsi,L_n Psi>, where L_n is the
ordered-injection average of L. Freezing this cotangent is only the
evaluation of the first derivative; no derivative of L is omitted from
a second-derivative claim. The site counts c_i are INSIDE the aggregate
encoder. Additional physically protected copies, if supplied, multiply
the price, score and gain once; they are not inferred from those counts.

The exact one-slot alphabet of7s gives its first conditional
L1=<L>I+(1/k) sum_a g_a(O_a-r_a I), where g is the complete canonical
feature differential d_r J. The true covariance is Sigma of7s(179),
including CAR correlations. Put G^2=g^T Sigma g, choose
B_L>=||L-bI|| for a fixed scalar b, and use the actual comparison
field-source gain Gamma_h=4a0 tau_h>0. The owned overlap theorem gives

    G/Gamma_h <= sqrt(n)||D_Psi J_n||/(2 Gamma_h)
      <= sqrt[G^2/Gamma_h^2
            + B_L^2 k^2(k-1)^2/(2 Gamma_h^2(n-1))].   (266)

This is the ambient normalized PURE-bank norm at the IID base,
including cross-bank entangled directions. Its sqrt(n) normalization
prevents false suppression of a nonzero field source. A directly
supplied E,b bank has G!=0 at7ab's product point and fails this test.
Only the canonical invertible field/feature map can transport the
GLOBAL all42 zero to G=0; vanishing along an ansatz curve is insufficient.

For the exact C2 aggregate comparison on Sigma, all f_i=q_i=0 and
the GLOBAL source is exactly
4a0 tau_h D[sum_i c_i(f_i+lambda_minus q_i)], retaining EVERY ambient
field direction. Apply the original inverse-PF density and16+24+2
theorem ON THAT comparison. Its G=0 then controls the entire
correlated bank source by(266). The actual finite Bernstein/native
encoder keeps its nonzero C1 field error. That error, transported by
the real canonical Jacobian and Sigma, supplies the nonzero first term
of(266); it is never assigned an exact finite all42 root.

There is a useful uniform implementation bound. If the complete n-bank
Hermitian kernel changes by epsilon in operator norm, its full score changes by at
most32 zeta epsilon/(1-zeta)^2. Thus ||Ahat-A_*||<=delta contributes
at most128 zeta delta/(1-zeta)^2 to the pure gradient norm. Multiply
by the actual total copy weight W for the global price. Define eta as
the norm distance of the ENTIRE normalized n-bank/purifier/work input
from its ideal product state (with its own source work, excluding the
fixed encoder blanks); per-bank error eta0 gives, for example,
eta<=n eta0. This whole-state error contributes at most
256 zeta W eta/(1-zeta)^2. Here W=1 for the one-cut construction;
any larger W requires actual extra protected copies. Divide
by the SAME gain and keep the sqrt(n) factor in(266). These errors can
be chosen after h,n,k and all norms are fixed; their longer actual
clock changes(264)'s value but not its field source.

Choose the existing polynomial/source accuracy to bound G/Gamma_h,
then n for the second term, then fixed-processor and unconditional
bank accuracy for these implementation debts. Ideal comparison tests
retain the preparation lift of7q/s. Pointwise native preparer words do
not inherit that C1 lift: actual endpoint/secant tests keep their own
norm and source-normalized word/mesh error divided by the actual
stencil spacing. Neither sphere differentiability nor smooth
admissibility of the full native programme space follows.

**Parent consequence.** The implemented two-band return now has a
generated joint-law construction and a full matrix preparation-source
budget, consuming the original nonvacuum all42 source and its existing
curved recovery. This supplies controlled source recovery, rather than
an exact finite joint stationary execution. The aggregate determinant
does not inherit the original local action's Hessian, off-shell
equivalence or generic Einstein equation class. The original scene/AF
embedding, full future-test and physical X_N tangent map, independent
encoder/middle/cut/clock equations and same-process refinement remain.
No product-law postulate, new action, fitted subtraction or physical
GR acceptance is added. GR_closed=false; raw216 remains open.


## 7ad. Full task-preserving native edits retain a controlled cyclic heat source

**25 October controller-source application.** The correlated bank bound
of7ac does not dilute a genuine independent processor variation. At an
IID bank, delta C=<xi^k,delta K xi^k>, with no1/n. The corresponding
matrix-feedback source is

    delta J=-8 zeta ReTr(Q^(-1) C delta C).             (267)

On a true complete-return implementation fibre delta C=0, this source
vanishes. At7ac's actual involutive endpoint, the WHOLE primitive-clock
heat FIRST source also vanishes on every unitary endpoint tangent,
including changes outside the fixed-middle conjugacy. Finite whole-price
neutrality is stronger and fails even for a terminally identical task.
The new [proof](sources/d0_native_task_clock_source_2026-10-25/PROOF.md)
and [check](sources/d0_native_task_clock_source_2026-10-25/check_task_clock.py)
supply an actual native counterexample and a controlled replacement
for that stronger premise. Phase: same native realization / source
composition owner, not a new admissibility or geometry campaign.

### Same initial cut and complete terminal answer, different full price

Start with the literal29-stage7ab echo at kE=kB=1. Give BOTH configurations
two new ACTIVE blank work bits c,t, keeping DATA/spin protected and all
unused thermal columns. Append to one echo the native tail

    G_t ; CX(c,t) ; actual raw inverse G_t ; CX(c,t).

The completed tail is I for c=0 and G_t^2 for c=1. Its14 primitive stages
include the dirty-port/source-spin routing and inverse; it is not a
free inverse gate. Append14 REAL cancelling CX to the baseline instead.
Both words have the same actual T=43, whole fibre D=128 and input rank8.
The edited endpoint acts identically to the baseline on EVERY allowed
input column, including unknown DATA/spin and a passive entangled past.
Thus the whole terminal output isometry, every subsequent test on that
same output, and J agree exactly. Intermediate primitive histories,
programme headers and additional input contexts are not thereby equated.

Let K_T denote the actual full clock character, theta satisfy sin(theta)=p,
and S_T(alpha)=K_T(alpha)+K_T(pi+alpha). The exact heat ratio is

    Z_edit/Z_base=(1+S_T(2theta)/S_T(0))/2 < 1.         (268)

The positive winding expansion gives

    S_T(0)-S_T(alpha)
      =4T exp(-beta) sum_r>=1 I_(2rT)(beta)
                                [1-cos(2r alpha)].    (269)

Its first term is strictly positive because1-cos(4theta)=8p^3>0.
This proves a strict price difference even though it is extremely small
at beta1,T43; low precision equality is not an exact source-neutrality
test. Both degrees and ALL2TD modes remain in Z. The comparison is on
one common padded clock, not a subtraction of old unequal-clock prices.

### Exact first-source cancellation at the actual involutive base

Every7ac endpoint, including an imperfect native encoder with its EXACT
raw inverse, is conjugate to V11 and has phases only0 andpi. The full
character is even and2pi-periodic, so K_T'(0)=K_T'(pi)=0. Functional
calculus therefore gives DH=0 for EVERY unitary endpoint tangent at
that base, not merely conjugacy directions. On a true task fibre
delta C=0, or delta F=0, the feedback source is also zero. Thus the
complete H+J first controller source vanishes EXACTLY there at any
fixed actual T and carrier. No long-clock approximation is needed for
this particular base conclusion. A moving cut/task, beta, clock or
extra physical stack term retains its own equation.

The strict finite edit(268) is consistent with this cancellation: it
detects higher-order/finite-price dependence. Stationarity is not
task-wise price invariance or prospective minimality. The following
bounds control general neighbourhoods and finite code contrasts.

### Retain the controller source with its actual norm and gain

Consume the owned complete-clock Gibbs/winding bounds, retaining all
unprepared modes. For ANY unitary endpoint U at fixed beta,T and carrier,

    |DH[delta U]| <= L_T ||delta U||_op,
    L_T=min{1/T, (2 exp(beta)/beta)
                       sum_m>=1 m I_(mT)(beta)}.      (270)

The elementary1/T bound follows from the actual Gibbs clock marginal;
the paired Hodge factor2 cancels in that normalized marginal. For fixed
beta and q=[beta/(2(T+1))]^T<1, a computable majorant is

    L_T <= (2 exp(beta+beta^2/4)/beta)
                 (beta/2)^T/[T! (1-q)^2].             (271)

Do not infer this factorial limit when beta also grows with T. The1/T
bound remains available. These are existing heat estimates used here
for a NEW controller-source consumer, not re-proved gravity equations.

For a comparison varying all T primitive unitaries, the literal product
rule gives ||delta U||<=sum_j||delta g_j||. Therefore a true task fibre
has complete H+J controller dual norm bounded by sqrt(T)L_T for the
gate-ell2 norm, or T L_T for gate-ell-infinity. If a physical control
parameterization is supplied instead, retain its actual endpoint/gate
lift norm. These smooth matrix bounds do not supply a continuous native
angle primitive; fixed G, CX and SourceI remain their literal alphabet.

There is also a finite-word version. Two same-T real-SO endpoints with
U_a P_in=U_b P_in differ by an orthogonal map fixing P_in pointwise.
A complementary real skew logarithm of norm<=pi gives an analytic path
of the SAME terminal fibre. Integrating(270) proves

    |B_b-B_a| <= pi L_T,
    |B_b-B_a| <= (pi/2)L_T ||U_b-U_a||_op.             (272)

This is a bound between actual code endpoints. The comparison path is
a proof device, not an admitted native actuator. Native source secants
keep the actual stencil spacing in the denominator. Equality only of
one chosen input density, one marginal effect, or a normalized report
does not imply the pointwise isometry condition used here.

For7ac's comparison use its SAME Gamma_h=4a0 tau_h>0 (and any actual
protected multiplicity once). The bank/source errors stay exactly as
in7ac. At the exact involutive base the additionally admitted true
task-preserving controller row is zero. In a neighbourhood or a finite
code secant, add the relevant heat bound DIVIDED by Gamma_h, with its
real lift/spacing.
One may choose a sufficiently long permitted common clock AFTER these
norms are fixed, using actual identity stages. This consumes resources:
the absolute heat/value and complete time/work ledger remain paid.
It does not solve a free clock, cut, beta or stopping equation or prove
that a task with a fixed duration permits such padding. Outside the
genuine task fibre, keep(267); the bank-copy count does not remove it.

### Observable admission and refinement do not erase those equations

Book01's six finite-section conditions admit a fixed supplied experiment
without requiring M1 to choose its programme uniquely. For a frozen
finite operator D0 its idle-cylinder extension D_m=D0 tensor I, with
the ORIGINAL Golden vector q0=(sqrt(p),p) and projection
P_(m+1,m)=I tensor<q0|, gives exactly P D_(m+1)=D_m P and
P R_(m+1)=R_m P for R=D dagger D. The finite quotient forgets the last
binary cylinder coordinate; its conditional expectation in the original
Golden weighted L2 uses weights(p,p^2) and has precisely this Hilbert
coisometry. This readout representation does NOT replace the full
counting heat trace or pay for a physically executed extra preparation.
Its finite support, actual terminal
registration and unchanged single calibration retain the other declared
conditions. This is observation of THAT frozen experiment, conditional
on its existing primitive/interface premises. It is not a proof that
different geometry-refining codes have the same intertwiners.

Nor does correct task verification make every physical controller a
correct implementation. Four complete JOINT programme effects on the
whole legal input family determine K; two means on a tied field curve
do not. A controller generated by an actual fixed correct process uses
the owned causal adjoint. An independently selectable controller keeps
its source unless an actual task/kinematic constraint or priced
accept/reject process supplies that fibre. These alternatives need an
explicit request/source-to-prefix map, not a universal extra selector.

There is already a decisive new refinement warning. With private DATA
for two7ac blocks, the retained old channel can be preserved, but the
ONE cumulative closing cut has underlying DATA return c1 tensor c2,
with the shared protected spin4 counted ONCE. Its determinant is

    J_total=-4Tr log[(1-zeta)I+zeta
                                  (c1^2 tensor c2^2)]. (273)

This is not J1+J2. Put A=p^6,B=p^12,a=1-zeta, Q=a+zeta A,
R=a+zeta B, S_A=A/(a+zeta A^2)+B/(a+zeta AB),
S_B=A/(a+zeta AB)+B/(a+zeta B^2). At the identical common-null
values the standalone ratio is lambda1=-2p^(-5)(R/Q+A), whereas
the two-block old-field ratio is lambda2=-2p^(-5)(S_A/S_B+A).
Indeed S_A/S_B is a positive weighted average of
r(t)=(a+zeta tB)/(a+zeta tA), t=A,B. Since r is strictly decreasing
and0<A,B<1, R/Q<S_A/S_B<1, so lambda2<lambda1 strictly.
The old nontrivial source balance Df+lambda1 Dq=0 need not annul
the new old-block source a2(lambda2-lambda1)Dq, with a2>0.
Thus7m's scalar-corner stationary composition cannot be copied into
this two-band process. A same-process price/source transport or an
actually justified different closing boundary is still required.

**Parent consequence.** The7ac involutive base has exact first-source
neutrality on every true task-preserving controller direction, beyond
fixed-V conjugacy. Full terminal task equality remains insufficient for
finite whole-price neutrality even in literal native code; the general
cyclic heat residual is uniformly controlled with the true clock, norm
and gain. This neither imposes a task fibre on native X_N nor
supplies exact finite joint stationarity or an admissible geometric
refinement. The actual generated-controller graph and cumulative
two-band source transport remain. GR_closed=false; raw216 remains open.


## 7ae. A native adjugate pair repairs the cumulative field-source ratio

**25 October changed-operation application.** The obstruction in7ad(273)
has a constructive scalar-return repair. Execute TWO identical source
preparations, flip the DATA bands in the second interaction, and close
their actual work inside one real echo. The complete return becomes the
determinant amplitude of the original2DATA corner. This makes7m's
scalar-corner hypothesis true for a new native operation; it does not
declare two-band tensors additive or change their closing cut.

The [proof](sources/d0_native_adjugate_pair_prefix_2026-10-25/PROOF.md),
[literal constructors](sources/d0_native_adjugate_pair_prefix_2026-10-25/paired_return.py)
and [bounded check](sources/d0_native_adjugate_pair_prefix_2026-10-25/check_paired_return.py)
consume7ab's native return,7ac's canonical bank/score and7ad's exact
whole-clock source. Phase: SAME native realization / source composition
owner. The parent is cumulative source transport, with all physical
admission and genuine independent-source boundaries retained.

### One fixed native middle implements the adjugate

For ANY actual DATA-blind real processor/preparer A, the original V
has return C=alpha I-beta X. This follows from its I,X DATA alphabet,
even with correlated programmes or finite compiler error. Execute the
SAME actual A twice on fresh private banks/work, and use

    M=V(e1,b1;d)[Z_d V(e2,b2;d) Z_d]
     =Z_e1 Z_b1 Z_b2 CX(e1,d)CX(e2,d).                (274)

The second equality cancels Z_e2; it is the physical implementation,
so no extra moving DATA gate is assumed. The completed middle is a
fixed symmetric involution. Its prepared/unprepared return is

    C_pair=C Z C Z=(alpha^2-beta^2)I=det(C)I.          (275)

Independence here is generated by two real fresh calls from the same
known setting. Unknown DATA is neither copied nor reset. Arbitrary
INTRA-copy programme correlation is allowed. A general cross-copy
entangled base or two unequal preparers does not satisfy(275).
In particular scalarity survives an imperfect compiled encoder only
when the SAME actual DATA-blind word is duplicated on separate banks;
one joint approximation mixing both groups would not prove it.

All forward compiler wires exclude DATA, the shared helper and spin.
They also exclude shared within-macro request keys unless an EXACT
read-only controlled construction is supplied. The native cells below
provide that construction; a generic approximate key-mixing compiler
would not prove independent duplicate calls.
SourceI inverse/phase macros may borrow the ACTIVE helper and dirty
spin and restore them on ALL columns. With sourceport=e1, the middle
costs6SourceI+14CX=20 actual stages. Four ordinary G preparers and their
real inverses give a62-stage example(8G,32CX,22SourceI), D128,cut8.
For a reserved helper outside every private bank, the middle costs26
and the completed example74 stages(8G,44CX,22SourceI), D256,cut8.
The extra helper stays in the full heat; it is an initialized work
bit, not another uncounted or protected input. Later macros never
borrow an already sealed oldRIGHT port.

### A concrete request generates both copies, with all branches priced

There is also a bounded actual controller graph. From a read-only
request bit c the native cell

    D_t(c)=G_t;G_t;CX(c,t);InvG(t);CX(c,t)
          =|0><0|_c tensor G_t+|1><1|_c tensor G_t^3  (276)

uses only the current primitive alphabet and its expanded inverse.
Apply the SAME private qE to e1,e2 and the SAME private qB to b1,b2.
The two generated preparations are conditionally identical products
at a sharp request; no equality constraint or Boolean decoder is added.
Port/off-port cells have lengths9/15 and inverses13/25. The whole
two-request echo therefore costs162 stages for source=e1, or186 with
the dedicated helper. The corresponding whole dimensions are512 and
1024. A known initial request00 has cutrank8; allowing all request
inputs widens the cut to32 and changes J to its actual block trace.
Every unprepared request branch is already in the complete heat.

Each macro has its OWN keys; new macros never control gates by sealed
old keys. If a pure request is itself prepared and unprepared inside
the word,7i's sharp-key first-source theorem applies to this concrete
block-diagonal native controller. Finite key edits are not smooth
variations and need not preserve price. This bounded graph does not
implement a universal field compiler or replace its source interface.

### The new coupling is derived from the actual scalar price

For the product reference E=p^2(1+X_h), b=(p-p^2Y_h)^2, with7ac's
single-cut aggregates X_h=tau_h sum_i c_i f_i,
Y_h=tau_h sum_i c_i q_i, the paired return is

    s=(1-2E)(1-2b)^2,
    s|Sigma=p^9,  s_X=-2p^8,  s_Y=8p^9,
    J_pair=-8log[1-zeta+zeta s^2].                    (277)

Thus a_pair=32zeta p^17/(1-zeta+zeta p^18)>0 and the genuine
material/geometric coefficient is lambda_pair=-4p. It is neither the
old finite-zeta lambda_minus nor a fitted counterterm. The action
formula is unchanged; the new paid operation has a different return
and its own derived source and compatible collars.

### One cumulative cut now preserves every old field-source zero

Give each completed macro private DATA/programmes/keys/source work.
Share only the dedicated ACTIVE helper and spin, on which each
COMPLETED macro is exactly identity on all columns. Then the actual
retained-channel projection is

    U_M=I_helper,spin tensor big_tensor_(j<=M) U_j,
    Tr_new Ad_(U_(M+1))=Ad_(U_M) Tr_new.              (278)

This holds for arbitrary entangled old/new input density operators.
At completed boundaries, actually retained old provenance and future
tests supported on old private registers are preserved; no later
primitive touches them. It does not identify
the new paired task with the old full8D query or its future profile.

With known private request00/work blanks and arbitrary private DATA,
the one REAL cumulative cut has rank r_M=4*2^M. It gives

    C_M=S I,  S=product_j s_j,
    J_M=-r_M log[1-zeta+zeta S^2].                    (279)

This is NOT sum_j J_j. The shared spin4 is counted once. Its full
field-source gain at Sigma is nevertheless

    Gamma_(M,j)=16*2^M zeta p^(18M-1) tau_j
                           /[1-zeta+zeta p^(18M)]>0,
    D_(Yj)J_M=Gamma_(M,j)
                      D sum_i c_i(f_i-4p q_i).        (280)

The ratio lambda_pair is independent of M, so a new completed macro
no longer changes the normalized OLD block field equation. More
generally at nonzero actual scalar returns, the true differential is
-w Dlog|s_j|, with w=2r_M zeta S^2/(1-zeta+zeta S^2)>0. This gives
the exact positive pointwise multiplier relating a block's cumulative
and standalone covectors. It is a derivative of(279), not an action
identity whose multiplier derivative has been dropped.

Actual imperfect scalar returns can be used in this SAME w and gain
2w tau_j/p. Their local Dlog|s_hat_j|-Dlog|s_ref_j| error then stays
explicit. Tiny actual gains are never replaced by the single-block
gain; no lower bound uniform in M is asserted. Later blocks do not
repair any already frozen field/preparation/implementation error.

Every whole prefix is still a symmetric involution. At its actual
common primitive clock and full dimension D_M, the heat partition
is D_M[K_T(0)+K_T(pi)], including every old work and request branch.
Its field source is zero, and7ad's ambient unitary first-source
theorem applies as well. Adding stages or varying beta/cut/stopping
still has its own actual equation and price. No historical cost is
removed from this cumulative trace.

### Consume the old universal equations at the new derived coefficient

The original full40 geometric identities(6)-(9) and CAR source
identities(11)-(12) in the owned arbitrary-Brinkmann proof are linear
in the material source coefficient. Apply them to the ACTUAL complete
ambient first-source identity(280), before the null ansatz. They give
the same forced proper-null links and

    Delta_h^perp H=-4lambda_pair |D_u^+Psi|^2.

Consequently H=-lambda_pair|Psi'|^2(x^2+y^2)+W, with the owned midpoint
sampling/material increments and harmonic W, supplies exact all16+24+2
REFERENCE field-source zeros at every admissible mesh and every finite
prefix M. The SAME fixed continuum metric/coupling works throughout.
The old midpoint O(h^2) recovery is reused with this coefficient and
its corrected collar. No new geometry search or claimed root-certificate
replay is required. The old configured J2 lambda_minus metric/collar,
its interval inverse and unrestricted Hessian are not transplanted.

Finite canonical Bernstein/native encoders retain their C1/endpoint
source errors; the analytical reference zero is not assigned to them.
For free pure banks the full TWO-copy score must be used. At the
identical product base its traced cotangent is copy symmetric, so
each first conditional is one half of the full canonical field source.
The all-field zero therefore kills both first conditionals. The
two-group overlap estimate controls the remaining arbitrary cross-copy
entangled directions at fixed finite layout; they are not a sum of
unrelated local gradient norms. Fixed-M multiple-group bounds retain
the total bank count, true gain and operator/state/field-lift debts.

This does not erase the old correlation control: duplicated correlated
programmes with the SAME E=b=p^2 have s=p^3 rather than p^9, and the
common-copy correlation source is nonzero. The canonical source map
and its actual preparation budget remain load-bearing. Nor does a
finite-prefix error estimate prove one infinite stationary execution
when previously executed source words have nonzero frozen errors.

**Parent consequence.** A literal native operation now supplies the
scalar-return hypothesis and positive cumulative source transport
that failed for7ad's unpaired tensor. Its generated request and private
prefix map are explicit. Full native field/preparation admission,
independent non-fibre controls, actual geometry/future-test binding,
and a compatible complete joint refinement remain. Generic Einstein
universality, physical GR and raw216 are not promoted. GR_closed=false.


## 7af. Reuse the exact original report and compose fresh reflected cohorts

25 October, SAME PR334/constitutive owner, input793558a8. The named
parent is7ae's frozen finite encoder/preparation error: a wrapper of
one old price cannot remove its normalized source direction. The changed
mathematical input is the ALREADY OWNED exact primary report jet, a
new literal native reflection, and fresh cohorts generated by the SAME
field source. This section constructs that process. It does not assert
that an already executed7ae word is its unchanged prefix.

The complete native construction is in
[PROOF.md](sources/d0_exact_report_reflected_cohorts_2026-10-25/PROOF.md);
the unrestricted joint-bank/source argument is in
[COHORT_THEOREM.md](sources/d0_exact_report_reflected_cohorts_2026-10-25/COHORT_THEOREM.md).
The bounded new calculation is
[check_reflected_report.py](sources/d0_exact_report_reflected_cohorts_2026-10-25/check_reflected_report.py),
using [reflected_report.py](sources/d0_exact_report_reflected_cohorts_2026-10-25/reflected_report.py).
These consume the paid-writer4/9, exact polynomial and7u amplifier
owners. They neither repeat their large compilation nor introduce a
new action, selector, counterterm, fair coin or ideal Boolean gate.

### The original source can be retained exactly on its primary family

Paid-writer4 already proves that P5 of the inverse-area moment and C8
of the nilpotent Cayley link have the full ambient TWO-jet of the
original geometric maps. With the exact LEFT CAR moment polynomial,
positive signed-polynomial/odd-majority construction and fixed Q(p)
tables, this gives one FINITE logical report q_h on the current pure
canonical bank. This is a use of the existing theorem, not a new
Hermite fit or another Bernstein limit. On the original primary
nilpotent family Sigma,

    q_h=q0=1-(1-zeta L)(1-zeta M),  0<q0<2zeta<1/2,
    L=1-p6,  M=1-p12,
    Dq_h=g_h E_ref,h,  E_ref,h=D Phi_h,
    Phi_h=sum_i c_i(f_i+lambda_minus q_i),
    lambda_minus=-2p^(-5)[(1-zeta M)/(1-zeta L)+p6].     (281)

Here every one of the16+24+2 independent ambient variations is taken
BEFORE restricting to the solution ansatz. The actual inverse-PF,
orientation, density, collar, matter and source calibration remain.
If E_ref,h^c is the old complete weighted J2 covector, its coefficient
is instead g_h^J=d0/W_h, d0=1-q0. Writing E_ref,h^c=A_h E_ref,h gives
g_h=(d0/W_h)A_h>0. In the common-tau/count convention this is the
actual click coefficient4zeta p11(1-zeta L)tau_h/W_h. These source
units are not interchanged. A moving reference, normalizer or genuinely
independent density still has its own row.

The original all40 Cartan and two CAR equations therefore supply the
same exact nonvacuum reference roots and midpoint recovery as before,
with the ORIGINAL lambda_minus. The new operation below consumes that
first source. It does not transfer an off-shell action or Hessian, nor
prepare an arbitrary continuous field by an exact finite native word.

At fixed h the report has fixed finite order k_h. Coherent uniform
ordered injections into n fresh complete packets give the effect
P_n with <P_n>_(xi^n)=q_h exactly for every n>=k_h. Its full correlated
kernel and all labels/flags remain. The actual raw word A has scalar
readiness on its whole logical input, and genuine R excludes the report:

    P_ref A^dagger R A P_ref=gamma P_ref,
    P_ref A^dagger R P_b A P_ref=gamma P_n tensor I.   (282)

P_ref fixes genuine private factory/logical INITIAL blanks, including
initial report0, but is identity on the bank, helper, source-spin,
meter and amplification rebit. It is not the smaller physical Book
cut. The owned7u coherent native amplifier preserves(282) and reaches
gamma>=1/2 at finite paid depth. All failed branches and the actual
G/CX/SourceI phase/inverse words remain. A measured retry probability
or normalized successful expectation is not substituted for(282).

### One native reflection preserves the feedback and fixes the whole heat

After the actual K READY/report controls are known, choose an integer
L_j>=1 and m_j=L_j2^(K-1). The existing native recursion gives

    M_rot=(I-Pi) tensor G^(-m_j)+Pi tensor G^m_j,
    Pi=R P_b.

Now execute Z_meter BEFORE this middle, with actual routed SourceI²:

    M_ref=M_rot Z_meter,   M_ref^dagger=M_ref,
    M_ref²=I on EVERY raw column.                     (283)

No ideal AND or negative-G primitive is added. The signed recursion
W_0=G^L, W_k=W_(k-1);CX;W_(k-1)^(-1);CX is expanded into actual
letters. With a dedicated helper the reflected middle costs
23m_j+2^(K+1)+6 primitive stages: G=3m_j,
SourceI=8m_j+2, CX=12m_j+2^(K+1)+4. All helper/spin inputs are restored
on all columns. The original irrational Golden angle permits a finite
certified integer search with1<alpha_j=4sin²(m_j theta)<2; no new
angle or field-dependent calibration is introduced.

Let the actual source preparation S_j act ONLY on its bank/source
ancillas, leaving distinct factory/amplifier inputs exact blanks.
The word S_j;A_j;M_ref,j;A_j^dagger;S_j^dagger has true returned
meter corner

    B_j=[cos(m_j theta)I+(2x_j-1)sin(m_j theta)J]Z,
    x_j=gamma_j <Psi_j,P_(n_j) Psi_j>,
    B_j^dagger B_j=t_j I,
    t_j=1-alpha_j x_j(1-x_j)>=1/2.                    (284)

Thus the old rotation feedback is preserved exactly, while the complete
prepared endpoint becomes an involution. The operator identity before
bank compression is also identity on the amplifier rebit; no returned
rebit1 amplitude is silently discarded. Its whole carrier stays in the
heat and its actual input blank stays in the cut. At the canonical
reference x_j=gamma_j q0,

    Dlog t_j=-kappa_j E_ref,h,
    kappa_j=alpha_j gamma_j(1-2gamma_j q0)g_h/t_j,
    (1-2q0)g_h/2<=kappa_j<=4g_h.                      (285)

Independent Dgamma_j,Dalpha_j and apparatus inputs keep their actual
feedback rows. Readiness bounds alone do not set those sources to zero.

Give every cohort private meter DATA2, bank, keys, source/factory work
and rebit. Only the ACTIVE helper/source-spin are shared, restored as
identity on all columns. Old sealed registers are never addressed.
The completed endpoints factor, giving exact old-channel compatibility
under partial trace even for entangled old/new inputs. They do not
identify the whole growing cyclic operators or absolute prices.

At prefix M the single real closing cut has rank r_M=4*2^M and

    T_M=product_j t_j,  Q_M=1-zeta+zeta T_M,
    J_M=-r_M log Q_M,
    w_M=r_M zeta T_M/Q_M,
    DJ_M=Gamma_M E_ref,h,
    Gamma_M=w_M sum_j kappa_j.                       (286)

This is NOT sum_j J_j. The true spin4 rank is counted once. Since
t_j>=1/2, w_M>=4zeta and
Gamma_M>=2zeta(1-2q0)g_h M at fixed h. No uniform upper bound or
mesh-uniform lower bound is asserted. Every error uses this actual
gain, not a standalone or nominal source coefficient.

Every whole prefix is a balanced symmetric involution. At its actual
expanded clock N_M and full dimension D_M the original paired heat is
D_M[K_(N_M)(0)+K_(N_M)(pi)], including all2N_MD_M modes. Its field
source is zero;7ad also gives zero FIRST heat source for any ambient
unitary tangent at that endpoint. Source preparation, amplification,
inverses, failures and padding all count in N_M. Free clock, beta,
cut, stopping or additional selected-stack rows retain their equations.

### The complete preparation score converges without erasing old cohorts

The field key is the SAME generated source Y of paid-writer10.2.
There is no equality constraint imposed on independently free Y_j.
For the product generated bank base, allow EVERY joint pure-bank
tangent, including cross-cohort entangling directions. Define

    R_j=Tr_meter(B_j K_j)/(2t_j)
       =I-[kappa_j/(2g_h)](P_(n_j)-q0 I),
    <R_j>=1,  v_j=Var(R_j),
    L_M=-2w_M tensor_j R_j,
    ||D_Psi J_M||=4w_M sqrt[product_j(1+v_j)-1].      (287)

K_j is the actual bank-operator return kernel before preparing Psi_j.
Equation(287) is the full matrix-logdet cotangent and its exact sphere
norm. A sum of one-cohort scores loses genuine multi-cohort excitations
and is not used. At the original all42 root, complete canonical
criticality plus the invertible feature Jacobian kills each first raw
conditional as an OPERATOR. The owned overlap estimate then gives
v_j=O_h(k_h^4/n_j²), retaining the higher entangled excitations.

Choose actual fresh packet counts n_j asymptotic to C_h j^b with
1/2<b<1. Then V=sum_j v_j<infinity and the ACTUAL total count is
N_bank,M=sum_j n_j=O_h(M^(1+b)). Therefore

    sqrt(N_bank,M)||D_Psi J_M||/(2Gamma_M)
      =2sqrt(N_bank,M)/sum_j kappa_j
                         *sqrt[product_j(1+v_j)-1]
      =O_h(M^((b-1)/2)) ->0.                         (288)

For b=3/4 the rate is M^(-1/8). Finitely many inaccurate early cohorts
OF THIS PROCESS contribute a finite factor, not an asymptotic floor;
their actual words/records are not modified. Repeating an unchanged
small bank forever generally fails the summable-variance premise.
At a noncritical report the true first-excitation bound instead gives

    sqrt(N_bank,M)||D_Psi J_M||/(2Gamma_M)>=G_q/g_h,  (289)

where G_q²=(D_r q_h)^T Sigma_packet(D_r q_h) uses the genuine packet
covariance. Cauchy-Schwarz and the same total count/gain prove this
guard. Away from the primary family it is a REPORT-source norm,
not an inferred off-shell Einstein equation. Normalization cannot
hide a nonzero genuine field covector.

For actual native source states retain the WHOLE-bank/purifier/source-
work norm errors eta_j. A compact q_j<q_max<1/2 collar and
sum_j eta_j²<infinity preserve summable variance with actual q_j,t_j
and actual positive slopes. Pointwise state approximation does not
provide a native C1 field map. If genuine source lifts satisfy
Dq_j=g_h E_ref,h+e_j, the EXACT field remainder is

    DJ_M/Gamma_hat,M-E_ref,h
      =sum_j a_j e_j/[g_h sum_j a_j],
    a_j=alpha_j gamma_j(1-2gamma_j q_j)/t_j,
    Gamma_hat,M=w_M g_h sum_j a_j.                   (290)

Uniformly vanishing e_j give the bounded-positive weighted Cesaro
limit; finite earlier errors then disappear in this actual source
mean. Repeating a fixed bias does not. Independently moving readiness,
rotation and other apparatus sources must first be added. The theorem
also proves the exact divided-price/code-secant identity, with true
positive divided gain, common actual clock/carrier and every state/word
error divided by its field stencil spacing. Density/countability of
finite words is not promoted to smooth native admissibility.

**Parent consequence.** The old primary report jet is now used by a
literal reflected native processor; its scalar Gram, full involutive
heat and cumulative full-bank score give a fixed-h shared-source
process with vanishing normalized bank remainder, including finite
early cohort errors. This removes the named frozen-error obstruction
for that process. It is an analytical application to the owned original
nonvacuum family, not a new finite root certificate.

Actual source/field-controller admission and its independent input
rows, complete scene/future-test binding, and one compatible whole
spatial/profinite refinement remain. The bank norm covers its declared
packets/purifiers, not every independently selectable raw factory or
clock input. Cost/Info/work/Rayleigh and free stopping/cut rows retain
their own physical selection/application obligations. No exact finite
native all-joint stationary execution, full physical X_N domain,
generic Einstein universality, positive_gr or raw216 is obtained from
(288). GR_closed=false.


## 7ag. One cofinal native endpoint process with a real request decoder and physical norm

25 October, SAME PR334/constitutive owner, input6eb11a2f. The parent is
7af's fixed-mesh restriction and its supplied finite source-request
implementation. Section7m already gives private-prefix composition on
the declared ideal source-X chart; that theorem is consumed, not repeated.
The changed input is7af's literal native reflected processor, exact report,
uniform rotation/readiness, and full product score for imperfect banks.
It now permits ONE cofinal native-ENDPOINT process with a quantified
physical lift at every completed prefix. It does not supply a continuous
native controller or all independent apparatus stationary equations.

The detailed consumers are [GEOMETRIC_MAP.md](sources/d0_native_cofinal_reflected_source_2026-10-25/GEOMETRIC_MAP.md),
[COFINAL_THEOREM.md](sources/d0_native_cofinal_reflected_source_2026-10-25/COFINAL_THEOREM.md)
and [NATIVE_REQUEST.md](sources/d0_native_cofinal_reflected_source_2026-10-25/NATIVE_REQUEST.md).
The new bounded code is [cofinal_source.py](sources/d0_native_cofinal_reflected_source_2026-10-25/cofinal_source.py)
and [check_cofinal_source.py](sources/d0_native_cofinal_reflected_source_2026-10-25/check_cofinal_source.py).

### A finite read-only request decoder is an executed native word

Consume the star-plane operation D_(a,k) of7c(29), with
K=2^(n-1) and generator J_(0,a). For d genuinely retained request bits
q and subset S, replace EVERY G_0^k slot by its conjugation with the
literal parity-CX word from S to data wire0. At request q the generator
changes by chi_S(q)=(-1)^(S.q). Products over all S with integer exponent
sign chi_S(q*) therefore give exactly

    D_(a,k,q*)|_q
      =exp[K k theta sum_S chi_S(q*)chi_S(q) J_(0,a)]
      =I (q!=q*),
       exp[K 2^d k theta J_(0,a)] (q=q*).              (291)

Negative G letters use the actual7j SourceI inverse. The request is NEVER
a gate target. All data, dirty helper/spin and nonselected request columns
remain in the exact word. No known-one, ideal Boolean predicate, Toffoli
or new controlled rotation is needed. The old irrational-angle theorem
and a finite product of star-plane rotations then approximate any fixed
finite real SO request catalogue uniformly on ALL its input columns,
while keeping the request read-only EXACTLY. This is a constructive finite
decoder, with all primitive powers, controls, routing and inverse stages
paid. It is not an efficient or installed cost-free universal compiler.

Inside the reflected echo, a known request0 is a genuine private input
blank; its WHOLE key carrier remains in the heat. It does not multiply
the cut rank as an arbitrary-input key would. All other keys still act
through their actual decoder blocks. A generated distribution over keys
must use its actual coherent state and full price, not a chosen sharp
conditional branch. The source of key birth, physical code selection,
independent decoder controls and native smooth actuation are not inferred
from(291). The finite decoder removes that construction premise only.

### Use the existing exact roots and the actual full ambient sampling

For a nonempty concrete member of the owned original family take affine
null scalar Psi and quadratic transverse H, including a nonzero harmonic
quadratic part if desired. The owned midpoint right inverse supplies exact
all16+24+2 roots Y_h on each sufficiently fine permitted mesh with its real
collar and material slack. No new metric, coupling or root search occurs.
For this member there are explicit uniformly C3 centres
Z_h=(e_op,h,omega_h,psi_prepared,h)
with Y_h=Sample_h Z_h and Z_h->Z in C2; the link coefficients are the
original backward differences divided by h. The affine material is its
actual midpoint history, not an independently assigned scalar source.
The fixed calibration is Psi_read=s² psi_prepared, so H uses
||Psi_read'||²=s4||psi_prepared'||² with the original lambda_minus.

Use7k(128)-(129)'s FULL ambient map at those centres:

    F_h(v)=Sample_h(Z_h+v),
    delta U_r=D Cayley_(h omega_r)[h delta omega_r].    (292)

All independent coframe/connection/CAR directions remain; v is a common
compactly supported physical C3 test, not a tangent to the pp-wave ansatz.
The corrected inverse-coframe, actual density/calibration and material
data of paid-writer12 remain. The finite source quadrature is
mu_h=c_quad,h h4. Thus define

    E_h^cont=(D Phi_h composed with D Sample_h)/c_quad,h,
    bar_g_h=c_quad,h g_h>0.                            (293)

This is the actual source-unit transport. Substituting g_h alone into a
continuum gain silently drops quadrature. The owned exact trace-count/
inverse-PF identity gives sum_(a anchored at x)c_a/rho_x=m_h independent
of x, with m_h=nu*528*K_AF*wbar. Thus the actual unequal-PF source is
Phi_h=m_h sum_x(fhat_x+lambda_minus qhat_x) and
c_quad,h=m_h h^(-4) in this counting convention. No uniform Born
weights are substituted. Rescaling Phi_h changes g_h inversely, leaving
bar_g_h invariant. The source identity of7af is
used only at its primary two-jet family. Neither P5/C8 nor this section
asserts generic off-shell Einstein-source equality.

Let xi_h be the SAME pure canonical packet, including its actual CAR
purifier/reference. Extra source work is a fixed blank TARGET factor,
with zero derivative here, and its actual leakage is included in the
whole-state eta_j. Independently moving source work keeps its own lift.
The calibrated packet speed is

    ell_h=||D(xi_h composed with F_h)(0)||_(C3->sphere).

Its square contains sum_a dot(t_a)^2/[4(1-t_a²)] for the geometry factors
WITHOUT a normalized site weight, plus the actual weighted CAR term
sum_x w_x[||dot(psi_x)||²+(psi_x.dot(psi_x))²/d_x²]. Positive slack/gaps
give a finite computable upper bound at each h. A growing number of
geometry features can make ell_h grow. The spatial operator transport
also retains its real decoder norm kappa_h and operator chord scale;
neither injectivity nor the five/nine-point profile inverse bounds this
full ambient norm uniformly.

### Slow cofinal execution controls the full product normal at every prefix

For each permitted mesh h_m choose a monotone finite bound C_m>=1 on
k_hm², ell_hm², bar_g_hm^(-1) and any additional actual readout/decoder
constants used by the consumer, also requiring C_m>=m. Define integer
thresholds J_m=C_m^64. For each cohort j use
m(j)=max({1} union {m:J_m<=j}), with the initial finite segment
treated separately. Equal thresholds may skip redundant coarse levels.
This one computable schedule is fixed upfront. It is nondecreasing and
cofinal, and its used constants are at most j^(1/64). It can be extremely
slow. No physical efficient runtime or externally forced mesh clock is
claimed. At every j append actual native centre preparation and reflected
report words on fresh private resources, with whole-bank errors eta_j
chosen square-summably and inside the actual q_max<1/2 collar.

Take n_j=ceil(k_hj² j^(3/4)), enlarged to at least2. Every old word stays
executed at its original accuracy. There is one finite-prefix stage list,
one true closing cut, r_M=4*2^M in the spin-only protected sector,
and the same actual full heat formula as
7af with its new total clock/dimension. Full request/key complements stay
in that heat; a decoder is never replaced by its one selected block.
An additional independently supplied oldRIGHT support of rank r_old
multiplies this cut rank, w_M and Gamma_M ONCE by r_old; it is never
silently omitted or allocated anew at each cohort.

At the canonical centres put

    a_j=alpha_j gamma_j(1-2gamma_j q0)/t_j,
    A_M=sum_(j<=M) a_j bar_g_hj,
    Gamma_M^phys=w_M A_M,
    DJ_M composed with the common lift
             =w_M sum_j a_j bar_g_hj E_hj^cont.         (294)

Use actual q_j and its positive slope for actual prepared states and
retain any genuine first-source/lift errors. All source gains are derived
from the one cumulative determinant; no multiplier derivative is omitted.
The exact product score and ambient bank norm of7af remain

    R_j=I-(a_j/2)(P_(n_j)-q0 I),
    ||D_Psi J_M||=4w_M sqrt[product_j(1+v_j)-1].       (295)

Complete first-conditionals vanish at the owned all42 centres. Hence
v_j=O(k_hj^4/n_j²), summable by the chosen schedule. Whole-bank/source-
work errors add their actual O(eta_j²) variance debt; they are not treated
as per-packet errors or a C1 controller theorem. To compare THROUGH an
actual endpoint, a fixed orthogonal transport can take its target whole
cohort state to its actual prepared state. Applying that same fixed
transport to the local smooth state chart preserves its speed. This is
a mathematical state comparison, not a supplied native continuous actuator.
For real normalized states at distance eta_j<1 the transport can satisfy
||T_j-I||=eta_j. Its whole-cohort report-jet error is at most
4eta_j sqrt(n_j)ell_hj in the stated physical dual norm. Exponentially
small chosen eta_j therefore controls both variance and the error divided
by bar_g_hj under the same slow envelope.

The calibrated common comparison speed K_M obeys

    K_M²=sup_(||v||C3<=1) sum_j n_j
                 ||D(xi_hj composed with F_hj)(0)[v]||²
         <=sum_j n_j ell_hj².                         (296)

It cannot be replaced by total packet count N_M=sum_j n_j. The envelope
gives N_M=O(M^(113/64)), K_M=O(M^(57/64)), A_M>=c M^(63/64).
With V=sum_j v_j<infinity, the TRUE-gain-normalized full preparation
source therefore satisfies

    K_M ||D_Psi J_M||/Gamma_M^phys
       =4K_M/A_M sqrt[product_j(1+v_j)-1]
       =O(M^(-3/32)) ->0                              (297)

at EVERY prefix, including finite early inaccuracies. This bounds any
genuine admitted physical field lift with that speed bound. It does not
manufacture such a native lift; any additional actual lift contribution
must be budgeted separately. If a genuine pulled-back report source is
Dq_j=bar_g_hj(E_hj^cont+e_j), its remainder is the actual positive weighted
mean with weights a_j bar_g_hj; normalized errors must tend to0 in that
same physical dual norm. Independent readiness/rotation/controller rows are
added before applying this mean. A nonzero limiting genuine report
source cannot be hidden: its pairing with an actual unit-speed physical
test is bounded by the left side of(297). This is not an off-shell GR
claim about the polynomial report.

Arbitrary cofinal h_j is insufficient. If bar_g_hj decays like2^(-j),
sum_j a_j bar_g_hj can stay finite; any retained nonzero early preparation
variance then leaves a floor, amplified by growing physical speed. The
slow mesh schedule addresses precisely that failure mechanism, while
preserving the true rank/gain and all old errors.

### Retained records have one limit; the absolute heat is not that limit

Consume7m's private-factor prefix map with the new scalar-GRAM blocks.
Completed old observables embed by A->A tensor I; the completed dynamics
commutes with these embeddings on all columns. Finite cylinder tests and
their retained states therefore define one consistent local record tower.
This is a single upfront sequence, not separately selected fixed-h limits.
The newest decoded primary geometry converges to the SAME curved
nonvacuum metric through the owned exact-root/midpoint readout, with
native state/readout errors chosen using their actual finite decoder bounds.

Old samples do not determine arbitrary finer smooth fields; a smooth bump
can vanish on every coarse node and remain nonzero on a new fine node.
The common smooth comparison in(292) supplies the shared parent, not a
new coarse-sample oracle. Nor does the record tower identify all growing
cyclic Hodge operators or their absolute heat/determinant prices. Every
finite price is computed on its actual new full carrier and clock.

**Parent consequence.** The fixed-h endpoint/source-normal result of7af
now has one spatially cofinal native-word consumer with a convergent
curved readout and the actual physical lift/gain at every prefix. The
finite read-only decoder is explicitly constructed. This removes those
two construction premises within the declared native profile. Physical
port/primitive admission, key/source birth and same-process C1 or actual
finite-secant variation graph, all independent apparatus/cut/clock/stopping
equations and complete selected-action binding remain. No old catalogue
is retroactively refined; pointwise native density does not prove those
missing controls. Full physical joint stationarity, generic GR,
positive_gr and raw216 remain open. GR_closed=false.


## 7ah. Actual native coordinate forks give a linear price cofield at the same base gain

25 October, SAME PR334/constitutive owner, inputfd2226a7. The named
parent is7ag's actual finite source-comparison graph. Its constant
orthogonal chart through native points was explicitly a mathematical
comparison, not a native C1 actuator. This section constructs finite
native PRICE tests instead. It consumes the exact reflected processor,
unconditional point preparation, physical sampling and product-normal
theorems; it does not repeat a geometric root or introduce a new action.

The full native fork construction is in
[NATIVE_GRAPH.md](sources/d0_native_price_cofield_forks_2026-10-25/NATIVE_GRAPH.md),
the field/readout map in
[STENCIL_MAP.md](sources/d0_native_price_cofield_forks_2026-10-25/STENCIL_MAP.md),
and the exact common-gain proof in
[COFIELD_THEOREM.md](sources/d0_native_price_cofield_forks_2026-10-25/COFIELD_THEOREM.md).
The bounded new code is
[price_cofield.py](sources/d0_native_price_cofield_forks_2026-10-25/price_cofield.py)
and [check_price_cofield.py](sources/d0_native_price_cofield_forks_2026-10-25/check_price_cofield.py).

### Predeclare real alternatives before the baseline is executed

At each new cohort j use the full independent chart
c=chi_h(Y)=(D_16,K_24,psi_prepared,2), on all free sites, with its
original fixed collar, density/calibration and reference. The exact
affine-scalar/quadratic-wave centres of7ag have c_j in Q(p). Choose ONCE
the finite catalogue

    c_j^0=c_j,  c_(j,a)^±=c_j±delta_j e_a,
    a=1,...,D_h,  delta_j>0 in Q.                      (298)

These are all finite independent field coordinates, not a pp-wave
parameterization. Eventually delta_j=1/j; finitely many initial chart
exceptions use smaller certified rational steps. Decode the actual
inverse coframe and proper Cayley links, not a label declared to be a
metric. Native targets are the same full pure canonical banks and their
purifiers. Approximate each entire target by an unconditional native
SOURCE preparer from the SAME zero blanks, with error eta_j uniform over
the catalogue. The separate report/AA/factory blanks are untouched.
No exact sharp-one key, chosen successful factory branch, unknown-state
clone or continuously selected native gate is used. An internal request
implementation retains the full key carrier and its real preparation;
the direct finite word family already suffices.

Use one common hardware support for the finite catalogue and include
each actual source inverse. All source-plus-inverse lengths have the
same parity. Real two-CX identities therefore match clocks; the owned
two/five-CX padding also covers the more general case. Padding is part
of the actual word, full heat and stage count. Choose the common T_j
BEFORE the baseline word u_j^0 is executed. This constructs a new
catalogue-ready realization; it does not pad an already completed7ag
history retroactively.

For fixed beta=(j,a,±), the compared full word is

    W_M^beta=u_1^0...u_(j-1)^0 u_(j,a)^±
                                      u_(j+1)^0...u_M^0.           (299)

Each fixed fork and the baseline are themselves append-only families.
The fork preserves its actual prefix through j-1 and every record
generated within that branch. It is a counterfactual execution from
the same complete initial blanks, not an operation rewriting the
already sealed baseline past. When the physical task fixes a later
prefix through floor(M/2), use only j>floor(M/2). The main full-history
certificate below retains all j; those are distinct boundary scopes.

The template keeps the actual carrier, cut rank, clock, beta and all
report parameters identical between compared nodes at every M. Shared
helper/spin are identity on all completed columns, immutable oldRIGHT
is never addressed, and the whole endpoint remains a balanced involution.
Consequently the COMPLETE paired heat is the same actual absolute value
at every node. All unused work/key/failure/old-column modes stay. A free
clock/cut/stopping row is not declared zero by this fixed-template test.

### One changed row has a gain uniform in the size of the old history

Let q_j^0 and q_(j,a)^± be the ACTUAL prepared report means, not ideal
values assigned to their codes. Keep their scalar Grams and whole price:

    t_j(q)=1-alpha_j gamma_j q(1-gamma_j q),
    T_M^0=product_j t_j(q_j^0),  r_M=4*2^M,
    J_M^0=-r_M log(1-zeta+zeta T_M^0),
    w_M^0=r_M zeta T_M^0/(1-zeta+zeta T_M^0),
    a_j^0=alpha_j gamma_j(1-2gamma_j q_j^0)/t_j(q_j^0).             (300)

Additional independently supplied protected support multiplies r_M,
w_M and every gain once; its full thermal dimension is counted separately.
The ordinary spin-only sector uses the displayed r_M. On the actual
q_max<1/2 collar the slope a_j(q) stays between positive constants.
For ONE coordinate/cohort edge define its true divided coefficient

    beta_(M;j,a)=(B_(M;j,a)^+-B_(M;j,a)^-)
                                      /(q_(j,a)^+-q_(j,a)^-).      (301)

At coincident q values use the continuous positive divided value. The
complete heat cancels, so beta is the divided slope of the ONE cumulative
determinant, with every other factor fixed at its actual base value.
It is not a standalone price or a sum of block actions. With z=log T,
0<d log w/dz<=1. Also

    d log a_j/dq=-2gamma_j/(1-2gamma_j q)+a_j(q).

Thus, for C_beta=8+2/(1-2q_max) and
u_(j,a)=max_±|q_(j,a)^±-q_j^0|,

    exp(-C_beta u_(j,a))
      <=beta_(M;j,a)/(w_M^0 a_j^0)
      <=exp(C_beta u_(j,a)).                         (302)

This is uniform in M, r_M, all old Grams and how small the actual gain
is. Only ONE log t changes. At the primary all-field zero,
u_(j,a)<=M_(2,h)delta_j²/2+4eta_j. There is no accumulating Mdelta²
shift in(302), unlike a simultaneous change of the entire tail.

### Reconstruct a genuine finite cofield from the actual price values

Define the price-coordinate vector and its physical sampling map by

    (b_(M,j))_a=(B_(M;j,a)^+-B_(M;j,a)^-)/(2delta_j),
    B_h=D chi_h D Sample_h,  L_h=||B_h||_(C3->l1),
    Fhat_M[(v_j)]=sum_(j<=M) b_(M,j)[B_hj v_j],
    Gamma_M=w_M^0 A_M,
    A_M=sum_(j<=M) a_j^0 gbar_hj,
    gbar_h=c_quad,h g_h.                              (303)

Fhat is a LINEAR finite cofield because its finite coordinate entries
are now fixed price data. It is not a nonlinear menu of simultaneous
finite changes silently called a covector. For independent physical
block tests use max_j||v_j||_C3; its dual norm is the SUM of block norms.
All16+24+2 rows are taken before the physical pullback or root ansatz.
The actual source-copy/inverse-PF identity, density, s4 material
calibration and all operator/readout norms of7ag remain in B_h and gbar.

Let Q_h(c) be the TRUE exact logical polynomial report on the finite
chart. P5/C8 is used only for its full first jet at the primary centre;
Q_h is not replaced by the original inverse/Cayley action off that family.
Uniform whole-bank node errors give the actual central-difference bound

    |Delta q_actual/(2delta_j)-D_a Q_h(c_j)|
       <=M_(3,h)delta_j²/6+2eta_j/delta_j.             (304)

At the exact all-field centre DQ_h=0. Combining(302)-(304) bounds each
physical block by w_M^0 a_j^0 gbar_hj epsilon_j, where

    epsilon_j<=C (L_hj/gbar_hj)
                        [M_(3,hj)delta_j²/6+2eta_j/delta_j].      (305)

The constant uses the actual compact q collar; no history-length factor
is discarded. Actual averaged canonical moments also approximate the
prepared field chord. Their coordinate decoder error is O(R_h eta_j),
so the divided chord keeps O(R_h eta_j/delta_j), followed by the real
inverse/operator norm if that readout is used. Mathematical labels are
not substituted for these observable means or physical chord scales.

Expand7ag's slow envelope to include gbar_h BOTH above and below,
L_h M_(3,h)/gbar_h, L_h/gbar_h, M_(2,h), the chart/physical extension
radius and actual readout constants. Keep epsilon=1/64 and the same
n_j=ceil(k_hj² j^(3/4)) construction. Rational delta_j=1/j after the
initial exceptions and eta_j=O(2^-j) give

    epsilon_j=O(j^(1/64-2)+2^-j j^(1+1/64)),
    sum_j a_j^0 gbar_hj epsilon_j<infinity,
    ||Fhat_M/Gamma_M||_(block-dual)=O(M^(-63/64)).     (306)

Finite inaccurate early field stencils stay in the numerator. Their
individual locally normalized errors need not vanish; this is the
stated GLOBAL block norm with the true cumulative gain. A genuine
nonzero source on a set carrying a positive asymptotic FRACTION of A_M
is not hidden by that normalization. Mere cofinality or positive
individual weights do not suffice. An isolated frozen historical error
is a different claim.

The SAME base Gamma_M is used by7ag's full preparation certificate.
For independent block lifts use K_ind,M²=sum_j n_j ell_hj²; its bound
also covers arbitrary old/cross-bank pure-state normals. Therefore

    K_ind,M ||D_Psi B_M^0||/Gamma_M=O(M^(-3/32)).      (307)

Equations(306)-(307) are one common-gain endpoint/finite-code certificate.
No derivative of a native word selector is assumed. They do not assert
exact finite-N stationarity or close an independently free decoder,
middle, birth-state, clock, observer, cut or stopping equation.

### Why simultaneous tail secants cannot replace these coordinate edges

If all young blocks move at once, the true divided price coefficient is
Wbar times sum_j abar_j delta_j gbar_j. It keeps EVERY stencil spacing
and the old product. At a critical positive two-slot report
q(u)=q0+d u², the symmetric probes even have equal plus/minus prices,
yet their common log Gram differs from the base by
D_M comparable to sum_young delta_j². The ratio w_base/Wbar can grow
like exp(D_M). With a retained nonzero old preparation variance this
mean-value gain does not control the full old/cross-bank source, for
any choice of the tail spacings in that model. This is a scoped
positive-effect countercontrol, not a contradiction to the original
GR family. The actual single-row tests(301)-(302) avoid its mechanism.

**Parent consequence.** Full-field finite stencils now have literal
native words, matched paid clocks, actual field chords and a linear
whole-price cofield with the same gain as the preparation estimate.
This removes the supplied finite native comparison-construction premise
within the declared operational profile. Physical source/port admission,
the original task's permitted counterfactual boundaries, common-source
control law, all remaining independently admitted apparatus/initial/
clock/cut/stopping rows and full selected-action binding retain their
own application obligations. The reconstructed cofield is not itself
one executed simultaneous common-Y motion or a physical C1 controller.
Full physical joint stationarity, generic GR, positive_gr and raw216
remain open. GR_closed=false.


## 7ai. Apply the native source and cofield bounds on the original known-port input

25 October, SAME PR334/constitutive owner, inputeadb0272. The parent is
7af–ah's need for a genuine unknown private meter2 at every cohort.
The required positive known-input operation is ALREADY7e(54)–(58),
with7j's exact raw inverse and7m's retained private-prefix construction.
Here the new exact report, full bank norms and actual finite-price
cofields are applied to that owned operation. No complex phase compiler,
new action, geometry root or extra unknown DATA input is needed.

The explicit consumer is [NATIVE_IMPLEMENTATION.md](sources/d0_known_port_native_cofield_2026-10-25/NATIVE_IMPLEMENTATION.md),
with [INPUT_AND_RECORD_MAP.md](sources/d0_known_port_native_cofield_2026-10-25/INPUT_AND_RECORD_MAP.md)
and [SOURCE_TRANSFER.md](sources/d0_known_port_native_cofield_2026-10-25/SOURCE_TRANSFER.md).
The bounded new code is [known_port.py](sources/d0_known_port_native_cofield_2026-10-25/known_port.py)
and [check_known_port.py](sources/d0_known_port_native_cofield_2026-10-25/check_known_port.py).

### The physical input cut and the algorithmic input predicate are different

Use the original conditional apparatus input |0_ACTIVE> tensor v_spin,
with arbitrary v in the SAME Q8 spin4. All private source/work/port/key/
rebit inputs are genuine known blanks. Only one shared unknown spin is
provided, together with any actual retained oldRIGHT support. Thus the
declared initial-family cut and rank are

    P_M=|0_all ACTIVE><0_all ACTIVE| tensor I_spin4 tensor P_old,
    r_M=4 r_old.                                      (308)

There is no2^M private-DATA multiplier. Fresh known ports still cost
real qubits, source actions and clock stages and remain in the FULL
thermal carrier. A shared helper has its own initial blank support;
its Hilbert dimension belongs in heat, not in the unknown input rank.
Additional oldRIGHT Hilbert dimension and protected support rank are
counted separately, once, as in7ag.

Reuse7af's SAME all-input report/amplifier A_j. Its algorithmic predicate
leaves SOURCE, helper, spin, target port and amplifier rebit free; its
report effect on SOURCE is gamma_j P_(n_j), with gamma_j>=1/2. The
physical cut(308) may additionally initialize that target port0. We do
not add port0 to the old amplification predicate or change its proved
operator interface merely because it is known in the physical input.
This strict support is a sufficient reuse contract, not a claim that
every other separately proved port-controlled amplifier is impossible.

### Use the owned controlled rotation, without the old reflection

On the actual K_j READY/report controls use their literal native word

    W_j=(I-Pi_j)tensor I_port+Pi_j tensor G_port^(2m_j),
    m_j=2^(K_j-1)L_j,
    d_j=1-cos(2m_j theta)=alpha_7af,j/2 in(1/2,1).     (309)

There is NO leading G^(-m_j) and NO Z. All inverse G letters in W_j
are the exact7j macros, with shared helper/spin restored on every
completed column. Its expanded counts are G=2m_j, SourceI=4m_j,
CX=6m_j+2^(K_j+1)-2. Every failed control receives I, rather than a
selected successful branch being normalized into a new primitive.
Known target port0 gives the operator kernel and actual corner

    K_j^bank=I-d_j gamma_j P_(n_j),
    C_j=s_j I_spin,  s_j=1-d_j gamma_j q_j,
    t_j=s_j².                                        (310)

Here q_j is the mean in the ENTIRE actual source-bank state. At a
compact actual q_max<=1/4, s_j>=3/4 and t_j>=9/16. The source preparer
and its inverse use the same complete private source support, excluding
separate factory inputs and immutable oldRIGHT. All old moments,
CAR/reference purifiers, SOURCE leakage and eta/delta budgets remain.

This is a different native middle, not a relabelling of the cut of7af's
reflected word. Blindly using that reflected word with port0 would give
corner cos(m_j theta)I independent of q_j and lose the field source.
The existing7e operation supplies the required nonzero known-cut map.

Completed blocks are I on shared helper/spin on ALL columns. The strong
old-channel/instrument/record map of7m therefore applies directly, even
on entangled old/new input. There is no live-spin covariance detour,
inverse of a measured success tape or reset of sealed data. Transient
source-spin interactions inside inverse macros still occur and are paid.

### Keep the fixed input rank and recompute the full paired heat

The ONE cumulative closing cut gives, with S_M=product_j s_j,

    J_M=-r_M log(1-zeta+zeta S_M²),
    w_M=r_M zeta S_M²/(1-zeta+zeta S_M²),
    a_j=2d_j gamma_j/s_j,
    D J_M=w_M sum_j a_j Dq_j,
    Gamma_M=w_M sum_j a_j gbar_hj.                    (311)

This is the actual price and positive first-source gain, not a sum
of local actions. For q_max<=1/4, 1/2<=a_j<=8/3. The ORIGINAL
lambda_minus and gbar_h=c_quad,h g_h come from the unchanged exact
r_poly first jet, inverse-PF copy counts and fixed s4 material map.
Thus the owned all16+24+2 nonvacuum reference zeros and curved readout
remain the same. No new source coefficient is fitted.

Let D_j be the complete private ACTIVE dimension, including its known
port, and let D_shared include the actual helper/spin/past Hilbert factors
ONCE. The middle W_j has phases0,±Theta_j, Theta_j=2m_j theta, with

    m_(j,0)=D_j(1-2^(-K_j)),
    m_(j,±)=D_j 2^(-K_j-1).

At the real WHOLE clock N_M the full PAIRED heat trace is

    Z_M=2D_shared sum_(sigma in {0,+,-}^M)
              [product_j m_(j,sigma_j)]
                        K_(N_M)(sum_j sigma_j Theta_j).            (312)

It counts exactly2N_M D_shared product_j D_j modes. No input projector,
success fraction or rank normalization is inserted into the heat.
This paired convention includes a factor2 relative to the old single-
Hodge-block formula7e(58). All node words have fixed middle spectra and
matched actual clocks, so their whole source/preparer heat is constant
by conjugacy. The global entangled SOURCE-preparer comparison also
has that conjugacy. The new endpoint is generally NOT an involution;
the ambient first-heat-zero theorem of7ad is NOT transferred. Other
middle/clock/beta/cut/readiness variations keep their real equations.

### The normalized estimates survive; a nonvanishing absolute gain does not

The new Hermitian kernel has the normalized exact product score

    R_j=(I-d_j gamma_j P_(n_j))/s_j
       =I-(a_j/2)(P_(n_j)-q_j I),  <R_j>=1,
    L_M=-2w_M tensor_j R_j,
    ||D_Psi J_M||=4w_M sqrt[product_j(1+v_j)-1],
    v_j=(a_j²/4)Var_actual(P_(n_j)).                   (313)

This retains all old and cross-bank entangling normals. The safe bound
is ||R_j||<=1/(1-q_max), not an untyped reuse of the former sqrt2.
Use the canonical critical-overlap bound, whole-state eta errors,
actual packet/source lift and enlarged slow envelope of7ag–ah. Since
the same w_M occurs in(311),(313), the controlled normalized bank and
native-coordinate cofield rates remain respectively

    K_ind,M ||D_Psi B_M||/Gamma_M=O(M^(-3/32)),
    ||Fhat_M||_(block-dual)/Gamma_M=O(M^(-63/64)).     (314)

The one-coordinate relative-gain proof also holds: now

    d log(w a_j)/dq
       =a_j[1/2-(1-zeta)/(1-zeta+zeta T_M)],
    |d log(w a_j)/dq|<=4/3.                           (315)

Every actual old product, coordinate spacing, field/readout norm and
global-vs-local old error qualification of7ah stays. These estimates
are not exact finite-N stationarity or a native C1 source selector.
Exact IID noncritical first-projection guards require their IID base;
approximate actual points retain the actual variance/eta lower debt.

Crucially, the old w_M>=4zeta bound is FALSE here. A common positive
q_min gives S_M²<= (1-q_min/4)^(2M), so w_M decays exponentially.
The enlarged upper-gbar envelope permits Gamma_M to decay too. Raw
source values can consequently tend to0 even for a nonzero report
source; only the explicit division by the ACTUAL Gamma_M distinguishes
it. For Dq_j=gbar_j E with E nonzero, (311) gives DJ_M/Gamma_M=E,
not0. Any additional physical residual must meet its true R/Gamma_M
budget. This is no assertion of a nondegenerate continuum coupling or
a rescaling of the native action. Absolute heat and feedback are kept.

**Parent consequence.** The literal cofinal/source-cofield construction
now has a known-ACTIVE-input consumer with ONE original unknown Q8
input. It removes the growing private unknown-meter requirement while
retaining the paid fresh known work, full old-record maps and actual
small gain. Physical primitive/preparation admission, the original
task's compulsory closing P_N and permitted edit image, independently
admitted apparatus/initial/observer/cut/clock/stopping rows and full
selected-action binding remain. Generic GR, positive_gr, raw216 and
full physical joint stationarity are not promoted. GR_closed=false.


## 7aj. Bind the known-port return test and control the complete task-source heat

25 October2026, SAME PR334/constitutive owner, input054d5eeb. The parent
is7ai's remaining implementation-source component outside fixed-middle
conjugacy. Its endpoint is not involutive and its absolute gain may
vanish. The OWNED general all-mode heat bound7ad/TC9–12 nevertheless
applies. The additional application is the literal input/return map,
not a new geometric action, field selector or independent execution.

The exact operational map and remaining admission hypotheses are in
[TASK_MAP.md](sources/d0_known_port_task_source_2026-10-25/TASK_MAP.md),
and the source estimate is in
[HEAT_TRANSFER.md](sources/d0_known_port_task_source_2026-10-25/HEAT_TRANSFER.md).
The changed bounded certificate is
[check_task_source.py](sources/d0_known_port_task_source_2026-10-25/check_task_source.py).

### The actual palette fixes a stronger return algebra than commutation

Keep the SAME G/CX/SourceI profile, source frame and protected Q8 input.
After reordering ACTIVE, spin and passive oldRIGHT factors, EVERY
validated native word has the form

    U=(A tensor I4+B tensor L_i) tensor I_old,
    (A+iB)(C+iD)=(AC-BD)+i(AD+BC),                    (316)

with REAL work matrices over the original Golden number field. This
follows from the actual generators: G/CX act as I on spin, while
SourceI=P_port0 tensor I4+P_port1 tensor L_i and L_i²=-I4.
It does not follow merely from commuting with L_i; its full centralizer
is larger. No SourceJ, free spin pulse or complex work coefficient is
added to the grammar.

For ALL ACTIVE initially known blank and only spin plus passive old
support unknown, write a=A_00,b=B_00. The actual protected corner and
return defect are therefore

    C=(aI4+bL_i) tensor I_oldsupport,
    C^dagger C=tau I_r,  tau=a²+b²,
    F=(1-tau)I_r,  r=4r_old,
    J=-r log(1-zeta+zeta tau).                        (317)

Consequently ONE unconditional COMPLETE blank-return probability fixes
the entire F on this physical input in this palette. No spin tomography
or external distribution over unknown spin inputs is needed. This
special statement does not hold for a different cut, extra arbitrary
ACTIVE inputs, spin-addressing primitives or an arbitrary-bank logical
subroutine. In particular it does not turn7ai's known-input cut into
the all-bank algorithmic P_ref used by the report/amplifier proof.

### Supply the complete record event and distinguish its actual task fibre

A readout-bit name alone is not a physical operation. Apply the OWNED
balanced final-label recording of7f/7l to a new private cohort BEFORE
its work is sealed. For k copied private labels, use actual fresh blank
record wires and the real CX product D_j on BOTH legs:

    U'_j=D_j(U_j tensor I_record)D_j,
    N'_j=N_j+2k,  D'_full,j=2^k D_full,j.             (318)

The initial copy fixes the supplied blank input. The final copy records
the actual labels, with every failed branch retained. Thus its protected
corner is unchanged. At the7ai base, completed helper/spin identity and
private support preserve the strong old-record maps and append-only
cohort process; earlier measured records are never inverted or copied
as quantum scratch. The full spectrum is that of U_j tensor I_record
at the NEW clock. Both record columns stay in the absolute heat. The
shared-helper return boundary must remain part of the actual complete
event; a private record0 test alone cannot hide helper leakage.

The joint record's all-zero label is an ordinary outcome of the complete
record family, not a free coherent AND gate, conditioned successful
state or postselected reset. Its identification with the full return
uses the copied support and actual helper boundary stated in TASK_MAP.
Additional observer/predicate/Cost/Info work keeps its own price. This
constructs the supplied recorded Book experiment; it does not prove that
the original physical problem compulsorily selects this experiment.

At fixed native bounds, cut/frame/carrier/clock and a supplied actual
full-return law tau_* given exactly in the Golden field or by a native
reference word, the set of codes with tau(U)=tau_* is a decidable
algebraic feedback fibre. Equality to an arbitrary computable real law
is not asserted decidable. No Einstein equation or desired
field root occurs in this membership predicate. Preservation of the
SAME actual task/future profile implies preservation of its already
available return event and hence (317), so DJ=0 on those directions.
The feedback fibre can be larger than full future-profile equality.
It is not declared to be the whole X_run or the selected physical X_N.
Native field-coordinate branches generally CHANGE tau and retain their
source; they are not silently absorbed into this vertical fibre.

The new exact native controls make these distinctions concrete. On
four qubits, the matched9-stage words G_port;SourceI^(+/-1);InvG_port
(with real CX padding) have C_+=pI+p²L_i and C_-=pI-p²L_i. Both have
tau=p²+p4. A real27-stage PRE-readout future context, the raw inverse of
the plus word, makes their return probabilities1 and p6; it never
reverses an already sealed or measured record. Thus the same full
return does not imply the same future profile. A separate N1 native
pair agrees on every known-work input but differs when a bank wire is
made an arbitrary subroutine input. A real13-stage balanced-copy word
on64 full columns verifies (318) and its actual joint record0 effect.
These are interface controls, not new GR field roots.

### The existing clock estimate now dominates the actual inverse gain

On7ai's actual collar s_j>=3/4, a_j>=1/2 and Q_M<=1. Its enlarged
cofinal envelope gives gbar_j>=j^(-1/64) after a fixed finite exception.
For all sufficiently large M,

    A_M=sum_j a_j gbar_j >= M^(63/64)/4,
    Gamma_M=w_M A_M
       >=(r zeta/4)(9/16)^M M^(63/64).               (319)

This is an exponential LOWER bound on the actual positive gain; it
does not undo its possible exponential decay. The recorded realization
uses its true expanded N_M, including all copying, with N_M>=M.
No new padding or change in stopping duration is used for this estimate.

Consume TC9–10 at fixed beta>0, fixed cut/carrier/clock and unitary
endpoint variations. With q_N=[beta/(2(N+1))]^N<1,

    |DH_N[dot U]|<=L_N(beta)||dot U||,
    L_N<=min{1/N,
       2 exp(beta+beta²/4)(beta/2)^N/[beta N!(1-q_N)²]}.

For an ACTUAL comparison-space norm V let B_infty,M be the operator
norm of its map v -> (g_l^dagger Dg_l[v])_l with gate maximum norm.
The literal product rule and (319) give

    ||DH_M||_(V*)/Gamma_M
       <=N_M L_(N_M)(beta) B_infty,M/Gamma_M
       <=C_beta B_infty,M N_M M^(-63/64)
                              (8beta/9)^(N_M)/(N_M!),              (320)

where C_beta=32 exp(beta+beta²/4)/(r zeta beta) after the finite
exception. The gate-ell2 form replaces N_M B_infty,M by
sqrt(N_M)B_2,M; the endpoint form keeps its actual B_U,M. All full
carrier and paired factors cancel in the derivative estimate only,
remaining in the absolute heat. At fixed beta the right side tends
to zero faster than any inverse power in gate unit norm. An actual
physical lift with log(max(1,B_infty,M))=o(N_M log N_M) also suffices.
No physical norm is assigned by decoding a field or enumerating words.

On the genuine full-return task fibre, DJ=0, so (320) controls the
complete H+J implementation source beyond fixed-middle conjugacy.
For two actual same-clock/carrier/cut codes with the same F, TC12 also
gives |Delta B|<=pi L_N, with their TRUE controller secant spacing kept
in the denominator. If that declared spacing is the actual counted
number d_edit>=1 of primitive code edits, the bound is uniform over
the entire same-F code fibre: |Delta B|/(Gamma_M d_edit)<=pi L_N/Gamma_M.
This is a code-comparison norm, not a physical42 norm or an equality
of action Cost with edit distance. Endpoint J equality suffices; an intervening smooth
SO comparison path is a proof device and need not preserve the task
or be a native actuator. Conditional report equality alone is insufficient.

This supplies a third controlled component beside7ai's complete-bank
O(M^(-3/32)) and finite-coordinate cofield O(M^(-63/64)) estimates.
A sum in one combined dual norm requires the actual comparison/lift map;
the three norms are not identified by terminology. Fixed old local rows
need not vanish in their own units, and no finite prefix becomes exactly
stationary merely from these globally normalized estimates.

**Parent consequence.** The non-involutive known-port process now has
an explicit scalar feedback/test map and a controlled whole-clock
implementation remainder at its actual gain. Fixed-spectrum conjugacy
is no longer needed to bound that heat component. Growing beta,
uncontrolled physical lift, moving input/cut/Gram/carrier/clock, non-task
feedback, an independently selected spatial scene and extra Cost/Info/
work/stopping sources retain their actual equations. The physical
selection of the supplied task/edit domain, full native stationary law
and stronger GR realization/refinement obligations remain. No full
physical stationary root, positive_gr, raw216 or GR_closed promotion
is made. GR_closed=false.


## 8. Reproduction

Run from this directory:

    OPENBLAS_NUM_THREADS=1 python check_same_brinkmann_paid_source.py --output /tmp/paid_source.json

The NumPy/SciPy script reconstructs all16 exterior grades, all32 paired Julia factors and their true derivatives; verifies the finite configured source equation and actual midpoint CAR increments; computes the complete two-round port source, all40 column variations and full two material rows; checks the normalized preparation finite difference; reads the same Ricci/Weyl via the covariantly transported probes; and checks the exact parity controls. On the smaller L4 fixture it reconstructs all64 original Walsh controller rows and all128 port maps, and compares the direct two-round conditional-port sum with (5). The latter includes all16384 ordered records by exact contraction, not an independence assumption.

Author replay: Python3.13.5, NumPy2.3.5, SciPy1.17.0. The complete receipt contains the actual source vector and explicit false status flags for unproved physical identifications. This packet adds no BOOK/claim/assembly status or workflow change. Independent scientific review is required before an accepted parent substitution.
