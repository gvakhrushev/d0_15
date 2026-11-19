# Full H+J+R under an explicit forward clock: exact transport, uniqueness, and the clock-source remainder

21 October 2026. Supporting application to the existing research owner #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input snapshot: `086fab99d8aaed7f712e9a3d2858c516b61901fc`.
No new physical action, task, information law, gravitational coupling, or assembly acceptance.
`GR_closed=false`.

## 0. Precise consumer and change from the previous results

The existing forward-window owner already proves
`J_window=(M-d)_+ J_data-min(M,d) rank(active) log(1-z)`
WHEN its actual compressed corner is a single-delay tensor product.
The original v8 owner and full-Lorentz extension already give a complete
specified H+J+R function, its operator source, and a certified flat joint
critical point. The paired-epoch owner ALREADY proves conditional whole-stack
transport and a stationary clock-cut section for a supplied product word and
spectator heat. Those are reused results, not discoveries of this packet.
The changed application here is a literal autonomous STAGE schedule plus a
separate elapsed register, full ambient clock heat, and the uniqueness and
quantitative source test at the owned original HJR critical point.

This application supplies that construction for a supplied fixed finite
unitary schedule, retaining separate stage and elapsed-time registers.
It then transports H, J, and R together. The source-preserving elapsed
window is M=T+1 for a T-stage schedule. On the old native HJR critical point
it is the UNIQUE consecutive elapsed-window size preserving stationarity
within this class. The uniqueness follows from the original positive
radial feedback derivative, not a choice of an Einstein coefficient.

The result is exact for the stated clock lift of the EXISTING HJR
matrix-programme interface. It does not establish that foundational D0
selects this clock lift, the active cut, the original moving matrix gates,
or the apparatus heat extension. In particular it does not turn the
configured Golden-J2 nonvacuum solution into an HJR solution. It is not
a new proof of the old forward-window determinant identity.

## 1. Original programme, source variables, and all retained work

Let K be the full original finite Hilbert space, including all actual
work registers and the purifying reference. Let i:H->K be its original
active isometry, P=i i*, and r=dim H. All dimensions are fixed on the
field chart. A supplied finite schedule of complete unitary operators is

    U(y)=U_(T-1)(y) ... U_0(y),       T>=1.

All products are chronological; no measurement or erasure is inserted.
The active block and genuine complementary feedback are

    A=i* U i,   F=I_H-A*A,   J=-log det_H(I-zF),    0<z<1.       (1)

The original reference multiplicity is ALREADY in H. When
`F=F_data tensor I_128`, (1) equals `-128 Tr_data log(I-zF_data)`;
there is no additional hidden factor128 in the formulas below.

Write the specified complete HJR function as

    S(y,Psi)=H_th(y)+J(y)+R(y,Psi),
    H_th=beta^-1 log Tr_K exp(-beta L(y)),
    R=<Psi,Q(y)Psi>,  ||Psi||=1.                                (2)

L and Q are the OWNED thermal and matter operators, not invented to
obtain a desired response. In v8, L=Lambda_alpha tensor apparatus identity,
Q=Delta tensor apparatus identity,
Lambda_alpha=-alpha^-1 log(I-alpha Delta), Delta=D^2,
and the original full apparatus trace contains C=128*128^n.
The usual field chart holds beta, z, the integer programme, and dimensions
fixed. Section6 retains derivatives when these continuous parameters move.

A moving original i is included in DA by differentiating i*Ui. The clock
isometry itself is fixed on this chart. Changes of discrete schedule,
window size, or alphabet are NOT treated as smooth derivatives.

## 2. Explicit stage + elapsed-clock realization

Use a stage counter Z/TZ, and a padded elapsed counter Z/LZ with
L>=M+T. Define the complete one-stage unitary

    W = Shift_L tensor sum_(j=0)^(T-1) |j+1 mod T><j| tensor U_j. (3)

The autonomous execution of T stages is W^T. Each executed stage advances
the elapsed counter by ONE. The stage counter wraps reversibly after a
completed schedule; it is not the elapsed-time record. For every start
0<=tau<M and every prefix length 0<=k<=T,

    tau+k <= M-1+T < L.

Therefore no elapsed wrap occurs in ANY history or intermediate state
used in this active window. The finite cyclic completion outside this
visited region only makes the ambient operator unitary. No trajectory
is claimed to return to an earlier elapsed time.

The pointed active embedding is

    i_M: |tau> tensor h -> |tau> tensor |stage0> tensor i h,
    0<=tau<M.                                                (4)

It does not include all stage phases as active inputs. Those phases stay
in the full ambient carrier and heat trace. It is therefore NOT the
clock-spanning phase cut whose off-seed windows were shown to have
different monodromies in the original order-memory experiment.

Direct application of (3) T times gives

    W^T(|tau,0> tensor v)=|tau+T,0> tensor U v,
    A_M=i_M* W^T i_M=T_(M,T) tensor A,
    T_(M,T)=P_[0,M-1] Shift^T P_[0,M-1].                     (5)

This proves, rather than assumes, the single-delay factor for this
fixed-duration schedule. The output work, record, and reference all stay
inside v. It does not identify a selected abort-event effect with A*A.
If an extra retained unresolved-status bit is orthogonal to the input
blank, its true A is zero; (5) remains zero and does not repair it.
The theorem concerns a fixed-horizon word. A variable-duration stopped
controller requires its actual controlled schedule, or a delay sum.

## 3. Complete feedback including the clock boundary

Put

    q_M=max(M-T,0),   b_M=M-q_M=min(M,T).

T_(M,T)*T_(M,T) is the rank-q_M coordinate projection. Hence, up to a
permutation of active basis vectors,

    F_M = direct_sum_(q_M copies) F
          direct_sum_(b_M copies) I_H.

On the complementary INPUT space the feedback operator is zero, just
as in the original definition. Its zero modes contribute determinant1;
no retained OUTPUT history is deleted. Consequently

    J_M=q_M J-b_M r log(1-z).                               (6)

This consumes the old forward-window identity on the now explicit
chronological lift. At fixed z its entire field differential is q_M DJ.
For moving z the boundary term contributes b_M r dz/(1-z).

The boundary value is positive and remains part of the absolute price.
It is not subtracted as an unpaid reference. In particular,
`det(I-u A_M)=1` from nilpotency is NOT the feedback determinant in (6).

## 4. Transport H and R on the same full carrier

For the original tested spectator-apparatus heat convention, extend
L and Q by identity over the two clock registers. Then

    H_M=H_th+log(T L)/beta,    R_M=R                         (7)

on the lifted original state `|elapsed0,stage0> tensor Psi`.
Every one of the T L clock basis states is included in the heat trace.
Equation(7) is an exact trace identity, not a deletion of unused modes.

A more general allowed mathematical heat extension is

    L_ext=I_clock tensor L + H_clock tensor I_K.             (8)

For any specified field-independent Hermitian H_clock,

    H_M=H_th+beta^-1 log Z_clock,
    Z_clock=Tr_clock exp(-beta H_clock).                    (9)

H_clock need not commute with elapsed translation. Only the Kronecker
separation in (8) is used. This extends the tested heat model; it does
not prove that real native clock heat has that separation. An interaction
term is retained and bounded in section7.

Q_ext=I_clock tensor Q is still the original matter reading. If the
original normalization-sphere equation Q Psi=R Psi holds, then

    Q_ext(|0,0> tensor Psi)=R(|0,0> tensor Psi).

Thus EVERY extra normalized clock/data-entangling preparation tangent
also has zero matter source at that lifted point. This is not merely a
check of variations along product states. The same statement on a
fixed-RIGHT Stiefel domain follows from QC=C Lambda. It does not assert
Euler equations for an independently varied clock Hamiltonian.

Combining (6) and (9) gives the WHOLE specified action

    S_M = S+(q_M-1)J+beta^-1 log Z_clock-b_M r log(1-z).     (10)

For fixed beta,z and specified field-independent clock heat,

    D S_M=D S+(q_M-1)DJ                                    (11)

on ALL original field, preparation, observer and reference directions
actually present in (2), with any original constraints pulled back.
No information convention is changed. In particular no CQ entropy is
identified with Book03 to obtain (10).

### Exact matched window

For M=T+1 choose the smallest padded elapsed dimension L=2T+1. Then

    S_(T+1)=S+beta^-1 log Z_clock-T r log(1-z).              (12)

With identity clock heat, Z_clock=T(2T+1). For fixed beta,z,
(12) is equality up to a field-independent, RETAINED absolute constant.
It preserves every original first variation, every existing second
variation, and the original constrained stationary set. Additional
normalization-sphere preparation rows vanish at every lifted original
sphere-critical state as above.

This is a construction of a source-faithful full-action clock extension.
It is not an assertion that M1 chooses M=T+1 among every possible clock,
that a physical clock resets, or that a new rank variable is stationary.

### The constructed clock-cut section also satisfies its first equations

Keep the full clock Hilbert space and its heat fixed. Allow an orthonormal
clock-isometry variation E'=K E, K*=-K, of the M active clock columns.
Initially these columns are |tau,stage0>, 0<=tau<M. W^T preserves each
stage phase. Components of E' in other stage phases therefore have zero
first contribution to E* W^T E. Within stage0 the clock compression is
the partial permutation T_(M,T).

For any surviving column j, Shift^T e_j=e_(j+T) is another active column.
The derivative of its ONE unit entry satisfies

    Re (delta T)_(j+T,j)
      =Re[<delta e_(j+T),e_(j+T)>+<e_j,delta e_j>]=0.

For every nonsurviving column the original compressed column is zero.
Thus every clock-diagonal entry of delta(T*T) vanishes. The feedback
resolvent is diagonal in these clock blocks, and its trace source is zero.
Consequently D_E J_M=0 for EVERY original data field in the chart. The
full ambient heat is independent of the active embedding E, and normalized
clock-only preparation changes leave Q_ext=I_clock tensor Q unchanged.
All pure clock-cut first sources and their mixed data derivatives vanish
on this explicit section. No inverse clock Hessian is used.

This does not imply a clock minimum. Arbitrary joint DATA/work-cut
variations, independently variable clock Hamiltonians, and programme/rank
changes are different equations and are not declared solved here.

## 5. The actual HJR root fixes the overlap uniquely in this clock class

At an original critical point y_* with DS(y_*)=0, (11) becomes

    D S_M(y_*)=(q_M-1)DJ(y_*).                              (13)

Thus if DJ(y_*) is nonzero on at least one genuinely allowed direction,
then the lifted field point is critical IF AND ONLY IF q_M=1, equivalently
M=T+1. This is uniqueness within the declared consecutive-window lift.
A different disconnected cut or different execution is not classified.
If DJ vanishes on every allowed direction, the uniqueness conclusion
is unavailable. In particular it must not be copied onto a configured
J2 Einstein root merely because its J2 source vanishes there.

For the original v8/full-Lorentz HJR source the required nonzero direction
is already available. Keep alpha,m,beta=m alpha,z fixed and make the
allowed homogeneous dilation D_s=exp(s)D, with normalized preparation
held fixed on this one test curve. Write

    Delta=D^2, B=I-alpha Delta>0,
    Z=Tr_data B^m, F_z=(1-z)I+zB^m,
    T1=Tr_data Delta B^(m-1),
    T2=Tr_data Delta B^(m-1) F_z^-1,
    r_ref=128.

Direct differentiation of the unchanged original J gives

    d_s J|0=2 r_ref z beta T2 >0                           (14)

whenever Delta!=0. Every factor in its spectral summands is nonnegative,
and at least one is positive. This does not assume simultaneous
commutation of arbitrary field jets; it evaluates this particular
admissible scale curve.

The published v8 exact root is enclosed by a radius10^-12 rectangle
about

    d=.063635191594344535042829697433316630182693569761541,
    o=.0040167350432317252873844519148251220686807163526359,

with L_grid=8, n=8192, m=16384, alpha=p^2/8192,
beta=2p^2 and z=2^-20. The first shell carries the original full pure
128-reference eigenpreparation. The full-Lorentz owner has already proved
its additional proper-link/observer equations. We CONSUME those root
and gap theorems, rather than search for a new root.

The new bounded interval calculation evaluates (14) over this entire
inherited rectangle, retaining all4096 momenta and all16 CAR grades
through their119 exact Q(sqrt2) feature classes. It certifies a strictly
positive coefficient near0.02205400814236. Consequently one EXTRA
surviving clock start, M=T+2 instead of T+1, gives an actual nonzero
full-action dilation source of that size at the owned exact root.
The numerical centre is not silently substituted for the exact root.

### Why making the clock large is NOT a route to selecting gravity

For any stationary point in this same factorized-heat clock class,
the full dilation equation is

    -T1/Z + q_M r_ref z beta T2 + R=0.                     (15)

Here R>=0 and T2>T1>0 when Delta!=0 and0<z<1. Necessarily

    q_M r_ref z beta Z <1.                                (16)

Thus arbitrary clock magnification cannot preserve stationary solutions
on a fixed compact strict spectral chart with positive lower bound on Z.
Multiplying the full equation by 1/M does not remove this condition.
Equation(16) is the existing full-HJR scale inequality with the now
DERIVED actual clock multiplicity; it is not an independently chosen
window cutoff. At the old exact root (13)-(14) are sharper: q_M=1 exactly.

## 6. Moving clock, beta and z: the complete residual is explicit

For the matched window, differentiation of (12) with moving beta,z and
actual H_clock(y) gives

    D(S_(T+1)-S)
       =-Tr(tau_clock D H_clock)
        -S_vN(tau_clock) D beta / beta^2
        +T r D z/(1-z),                                   (17)
    tau_clock=exp(-beta H_clock)/Z_clock.

Proof: differentiate the finite exponential under the trace. Its
noncommuting derivative cycles to -beta Tr(exp(-beta H) DH).
Using S_vN(tau)=log Z+beta Tr(tau H) gives the beta coefficient.
There is no basis or spectral-projector freeze.

For the spectator clock, (17) reduces to

    -log[T(2T+1)] D beta/beta^2+T r D z/(1-z).

These terms must be retained if a proposed physical clock or calibration
moves them. The theorem does not declare a free clock/cut/temperature
stationary. Discrete T changes belong to different actual programmes.

## 7. A quantitative test for nonseparable actual clock heat

Suppose the true thermal extension on the SAME carrier is

    L_true=I tensor L+H_clock tensor I+E(y),

where E is the actual Hermitian interaction, not a fitted counterterm.
Hold beta fixed for the following estimate. Let tau_true and tau_sep be
the Gibbs states of L_true and its separated part. For an admitted
unit tangent v put X=D_v(I tensor L+H_clock tensor I).
The exact extra thermal source is

    e_heat(v)=-Tr[(tau_true-tau_sep)X]-Tr[tau_true D_vE].   (18)

The Duhamel derivative of a Gibbs state along L_s=L_sep+sE is

    d_s tau_s=-beta integral_0^1 tau_s^(1-u)
                       (E-Tr(tau_s E)I) tau_s^u du.

Schatten Holder and Tr tau_s=1 imply

    ||tau_true-tau_sep||_1 <= min(2,2 beta ||E||).

Therefore

    |e_heat(v)| <= ||D_vE||
              +min(2,2 beta||E||) ||X||.                  (19)

No spectral gap, commuting interaction, dimension-dependent constant,
or probability cutoff is required. This supplies an actual same-source
error bound when E and DE have been computed from a real clock. Merely
asserting they are small would not discharge the physical application.
Additional matter/clock work not already in (2) retains its own source.

## 8. Native order-memory application and hostile controls

For the owned full16 arm/spin/record fixed-programme blocks use the literal16-stage
identity and order schedules. They are not asserted to be same-complete-initial
prospective alternatives; a stored programme bit is retained by the original owner. Its pointed spin embedding is arm0,record0.
Direct exact Golden/quaternion multiplication gives

    A_identity=I4,   A_order=p^3 I4,
    F_order=(1-p^6)I4=4p^3 I4.

The new construction uses stage dimension16, elapsed dimension33 and
active elapsed window17. All active starts are followed for all16 stages
without elapsed wrap. Its active rank is68: four returned spin directions
plus64 genuine boundary-complement directions. Hence

    J_identity=-64 log(1-z),
    J_order=-64 log(1-z)-4 log(1-4zp^3).

The absolute boundary is retained. This is the original pointed trial
contrast, NOT the fourfold contrast of the older all-stage-phase active
cut. That older calculation remains correct for its different cut.

The checker also verifies M<=T blindness, M=T+2 doubling, nilpotency
versus the true feedback determinant, a genuinely orthogonal unresolved
status, moving-beta/z residuals, and a noncommuting clock-heat interaction.
A second small complete HJR matrix fixture tests gradients and mixed
second variations by differentiating the full clock matrix independently.
It is labelled as a numerical fixture, not a replay of the native full spatial
operator or the full quantum workspace.

## 9. What is closed here and what is NOT

Closed mathematical application: a supplied finite complete programme has
an explicit forward-only elapsed-clock extension for which the entire
specified HJR field source, and its stationary roots, are preserved
exactly. The only root-preserving consecutive window at the owned native
HJR root is M=T+1. Its full constant price and moving-clock residual are
known. This removes the need for an unexplained returned elapsed-clock
factor IN THIS CONSTRUCTED INTERFACE.

Still open: compulsory physical selection of this clock/cut and its heat
law; native finite primitive realization of the field-dependent query;
all actually additional execution/Info/work terms; physical clock-to-Book06
transport; the common-source nonvacuum Einstein application and uniform
refinement. The existing primary Golden-J2 family is not a root of the
separate full HJR merely by this construction. Indeed its already known
nonzero HJR preparation source is preserved, not cancelled, at M=T+1.

No independent review, whole native source replay, main merge or full
physics closure is claimed by this author packet. The proof and the small
new computations have separate provenance in SOURCES.json and RESULT.json.
