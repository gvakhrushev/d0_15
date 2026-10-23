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

## 8. Reproduction

Run from this directory:

    OPENBLAS_NUM_THREADS=1 python check_same_brinkmann_paid_source.py --output /tmp/paid_source.json

The NumPy/SciPy script reconstructs all16 exterior grades, all32 paired Julia factors and their true derivatives; verifies the finite configured source equation and actual midpoint CAR increments; computes the complete two-round port source, all40 column variations and full two material rows; checks the normalized preparation finite difference; reads the same Ricci/Weyl via the covariantly transported probes; and checks the exact parity controls. On the smaller L4 fixture it reconstructs all64 original Walsh controller rows and all128 port maps, and compares the direct two-round conditional-port sum with (5). The latter includes all16384 ordered records by exact contraction, not an independence assumption.

Author replay: Python3.13.5, NumPy2.3.5, SciPy1.17.0. The complete receipt contains the actual source vector and explicit false status flags for unproved physical identifications. This packet adds no BOOK/claim/assembly status or workflow change. Independent scientific review is required before an accepted parent substitution.
