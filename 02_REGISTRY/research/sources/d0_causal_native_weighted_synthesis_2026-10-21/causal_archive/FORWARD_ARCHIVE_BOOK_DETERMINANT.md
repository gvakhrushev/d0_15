# Complete forward archive return realizes the original full128 Book determinant

21 October 2026. Bounded continuation of existing PR #334 at input
`086fab99d8aaed7f712e9a3d2858c516b61901fc`; no new task or physical-action
selection. All work here is scratch. The finite determinant/source identity
below is the new parent substitution. The generic reflection Schur identity
is consumed from the existing archive owner, not claimed again.

## 1. Exact advance and the execution it concerns

The forward-window owner computes the corner of ONE returning history,
`T_(M,d) tensor D`, and obtains a source multiplicity `M-d`. Book06
§06.8.F already prescribes a different, complete operation: the direct
active amplitude plus EVERY coherent archive-return amplitude. Lifting
that entire series onto a forward time record gives a lower-triangular
time-bin operator. Its defect is a finite archive Gram, not one copy of
the data defect per surviving start time.

For the ORIGINAL full128 Golden comparator unitary, let its active blank
corner be the already-owned positive operator

    B = I - 2 p^2 A_native^2 = I - alpha Delta,
    alpha=p^2 ell^2/128,    p=phi^-1.

For n aligned input/output bins, its full coherent return corner T_n obeys

    det(I-z(I-T_n* T_n))
       = det_H[(1-z)I+z B^(2n)].                         (1)

With an actual positive one-round advance and the SAME active clock
window of M=n+1 bins, the corner is instead f(S_M), with f(0)=0, and

    J_clock,n+1
      = -r_RIGHT dim(H) log(1-z)
        -r_RIGHT Tr_H log[(1-z)I+z B^(2n)].              (2)

The second term is exactly the original v8 `J_program`, including its
absolute scale, all CAR/site modes and oldRIGHT multiplicity. The first
term is a real clock-boundary price and is retained. No division by M,
postselection, reset, fitted counterterm, Perron trace or newly selected
clock measure occurs. At fixed z, every finite smooth field, cut or
normalization jet entering the SAME B agrees between the two feedback
functions, at fixed horizon and active-cut rank. This does not require a
fixed bright/dark rank. The Book feedback is evaluated on the declared
active embedding, whose initial archive component is zero; it is not an
expectation in an arbitrary preparation density. Independent archive or
data preparation sources not encoded in this embedding and B remain in
the actual ledger. Moving z retains the displayed boundary derivative.

This is a complete coherent return execution of the same native one-round
unitary. It is not the original sequence of fresh, individually recorded
128-outcome rounds. Those programmes have different memory/cost/Info
contracts. Equation (2) transports their identical FEEDBACK FUNCTION,
not the remaining full price. In particular it supplies no equality of
their measured CQ entropies.

## 2. Original definitions and which existing archive mechanism is used

Book03 §§03.3.0–03.3.0a defines the algebra-valued sum of history weights
`phi^(-Cost+Info)`. It does not equate Info to any chosen pointer entropy.
Its §03.3.2 defines the complementary feedback on an actual active cut:

    F=P U* (I-P) U P,    J=-Tr log(I-zF).

Book03 §03.3.0c excludes hand-chosen counterterms. Section 03.25 retains
the separate heat term. These definitions are respected by (1)–(2).

Book06 §§06.4–06.5 fixes the active/archive split and the retained algebra.
Section 06.8.F gives

    A + B_off (I-D)^(-1) C
      = A + sum_(k>=0) B_off D^k C,

where `U=[[A,B_off],[C,D]]`. The number k counts INTERNAL archive
circulations. The complete elapsed word contains one U for A and k+2
U's for `B_off D^k C`; these counts must not be conflated. The Lean owner
`FeshbachSchurTimeDelayOwner` explicitly certifies path grammar, with
Neumann convergence a separate premise. The finite construction below
requires no infinite-series convergence.

Book06 §06.6.B also describes a normalized shift-invariant golden-cylinder
trace and a crossed-product passport. That trace is on the specified
golden history system, not automatically on the present reporting counter.
The same section retains the unresolved identification with frozen archive
refinement maps. Section 06.8.M explicitly has no modular-flow certificate
of its own. Neither passage selects a trace state or rescales the present
absolute feedback. The useful already-owned mechanism here is the finite
archive-return series itself; no toral-to-nilpotent identification is
needed.

The original 718-edge reflection owner already proves `DC=-CA` and its
archive self-energy. Its carrier is not full128. The new application is
the finite forward-return determinant and its original full128 realization.

## 3. Finite causal colligation, all output bins and final archive retained

Let U be ANY finite unitary on `H_active direct_sum H_archive`, with
dimensions h,q and blocks

    U = [[A, B_off], [C, D]].

Supply n active time bins u_0,...,u_(n-1), and initial archive x_0=0.
At the kth encounter use this SAME U, retain its output bin y_k, and
continue with its actual archive x_(k+1):

    y_k=A u_k+B_off x_k,
    x_(k+1)=C u_k+D x_k.                                (3)

This is a finite unitary circuit on `H_active^direct-sum n` plus the
archive: U acts on the kth bin and the shared archive, and leaves every
already emitted bin untouched. There is no archive reset between steps.
The product remains unitary on arbitrary input archive as well; x_0=0
specifies the active input embedding, not a discarded subsystem.

The active-to-active corner is the lower-triangular block Toeplitz matrix

    (T_n)_(k,j)=0                    if k<j,
                 A                  if k=j,
                 B_off D^(k-j-1) C  if k>j.

Its final archive map is

    W_n=[D^(n-1)C, D^(n-2)C, ..., C].

Unitarity of EACH actual encounter gives the exact full energy balance

    sum ||u_k||^2 = sum ||y_k||^2+||x_n||^2,

and hence

    I-T_n* T_n=W_n* W_n.                                (4)

Every output bin and x_n is retained in the unitary realization. The
trace/determinant does not condition on successful exit. From
`CC*+DD*=I` the actual archive Gram telescopes:

    W_n W_n*=sum_(j=0)^(n-1) D^j CC* (D*)^j
             =I-D^n(D*)^n.                             (5)

Sylvester's determinant identity therefore yields, on this SAME finite
unitary and cut,

    det_(nh)[I-z(I-T_n* T_n)]
       =det_q[(1-z)I+z D^n(D*)^n].                      (6)

This is a reduction of the actual complete determinant, not a deletion of
archive modes. A unitary reducing dark archive contributes eigenvalue 1
to the determinant. It need not be removed by hand.

For a nonzero independently supplied initial archive, (3) additionally
contains `B_off D^k x_0`. Its actual preparation, price and entropy sources
are still present. The fixed-blank theorem is not a stationary equation
for every possible upstream archive preparation.

## 4. True elapsed time and the compulsory one-step boundary

Introduce the formal delay variable xi only to label actual elapsed
rounds. The aligned transfer and the positive-delay first return are

    Theta(xi)=A+xi B_off(I-xi D)^(-1)C,
    f(xi)=xi Theta(xi).                                  (7)

Thus A returns after ONE full U, and the kth internal-archive term after
k+2 full U's. In a same-cut forward counter of M=n+1 slots, the actual
truncation f(S_M) has an initial zero output row, the T_n block mapping
the first n input bins to the next n output bins, and a last input bin
whose entire output lies beyond the active window. Consequently

    I-f(S_M)*f(S_M) = diag(I-T_n*T_n, I_h),               (8)

up to a fixed ordering of the input bins. Its full determinant is

    (1-z)^h det_q[(1-z)I+zD^n(D*)^n].                   (9)

All time bins beyond the cut are complementary OUTPUT, not lost records.
For a finite unitary realization, apply (3) to ALL M=n+1 input bins,
retain all M output bins and the final archive, and route y_k to clock
slot k+1. The terminal output y_(M-1) lies in one padded guard slot,
beyond the active window. Thus the last input also pays a full native
encounter; its output is not bypassed. The routing on these output bins
is injective and moves only forward. An arbitrary unitary completion on
unoccupied complement columns changes neither (8) nor (9). No occupied
clock wrap is used.

This specifies a mathematical causal time-bin execution. Native admission
and payment of its routing and controls are the same kind of remaining
implementation obligations as in the original forward-window owner.
It does not silently identify the effective Book06 archive clock with
every additional implementation/controller clock. If an implementation
adds another advancing register, its actual corner must also be included.

One U denotes one COMPLETE supplied native word. If that word takes q
primitive ticks, bins above denote its registration boundaries; all q
primitive stages and their cost remain. They are not derived from a 0/10
report code. If every primitive phase rather than only the registration
phase is active, the actual clock decomposes into its q residue classes;
their separate determinants/multiplicities must be retained. An integer
duration is not varied as a smooth field coordinate.

For M=1 the corner is zero and J is exactly `-r_RIGHT h log(1-z)`, in
agreement with the initial-time-only control. Treating Theta's direct
term as a zero-duration physical return would fail this control.

## 5. ORIGINAL full128 unitary and exact reflection reduction

Consume the literal SELECT blank row from the full128 owners:

    N=(N_0,...,N_63),    N N*=I,
    N_0=A_native=A_native*.

On all64 workspace blocks the ORIGINAL full reflection is

    W=I-2N*N.

The actual Golden matrix is `G=[[sqrt(p),-p],[p,sqrt(p)]]`. On both
controller ports and all64 workspace blocks its complete comparator is

    U=(G* tensor I) diag(I,W) (G tensor I)
      =I-2 V V*,
    V=[p N*; sqrt(p) N*],    V*V=(p^2+p)I=I.            (10)

Therefore U is the ORIGINAL full self-adjoint involution, not a
postulated minimal dilation reconstructed from B. Its blank-input column
has EVERY one of the original128 outcomes:

    K_(0,j)=delta_(j,0)I-2p^2 N_j* A_native,
    K_(1,j)=-2p sqrt(p) N_j* A_native.                   (11)

The active cut is exactly controller0/workspace0, with all site/CAR
coordinates and the oldRIGHT spectator retained. Its corner is

    A=B=I-2p^2 A_native^2.

Writing the other blocks of (10) as C,D, involutivity supplies the owned
relations

    C*C=I-B^2,    DC=-CB,    B_off=C*.

They determine EVERY delayed return, without changing the full U:

    B_off D^j C=(-1)^j (I-B^2) B^j,
    Theta(xi)=(B+xi I)(I+xi B)^(-1).                   (12)

For the finite determinant, one need not choose or differentiate a bright
eigenbasis. With `R_n=sum_(j=0)^(n-1) B^(2j)`,

    W_n W_n*=C R_n C*,
    det_Q(I-z C R_n C*)
      =det_H[I-z R_n C*C]
      =det_H[(1-z)I+z B^(2n)].                         (13)

This proves (1) and (2). It is valid at dark eigenvalues B=1 and under
smooth changes of dark rank. All unused original archive directions
remain in the full unitary and contribute determinant factors 1. No
factor128,16, spatial-volume or clock gain is inserted or discarded.
The oldRIGHT spectator multiplies the log determinant by r_RIGHT=128.

The original one-round source is therefore enough to construct a concrete
Book06 all-return transfer whose finite feedback agrees with the original
v8 feedback. This is a source-preserving bridge for that feedback component;
it does not make the two distinct executions' other prices equal.

## 6. Every finite source jet, including moving fugacity and moving cut

Put `E_n=B^(2n)`, `G_n=(1-z)I+zE_n`, and retain the actual strict-clock
boundary. The complete first derivative of (2) is

    dJ_clock = r_RIGHT h dz/(1-z)
               +r_RIGHT Tr[G_n^(-1)(I-E_n)] dz
               -r_RIGHT z Tr[G_n^(-1) dE_n],
    dE_n=sum_(j=0)^(2n-1) B^j (dB) B^(2n-1-j).          (14)

At fixed z, cyclicity gives

    dJ_clock=-2n r_RIGHT z
               Tr[G_n^(-1) B^(2n-1) dB].               (15)

No commutation between dB and B is assumed. If B=I-alpha Delta,
`dB=-alpha dDelta-Delta d alpha`; the true moving normalization is retained.
If the initial cut i moves, `B=i*U i` includes both di terms. The finite
reflection identity holds for every smoothly moving fixed-rank i, so
this derivative is not frozen by the reduction.

For any two tangents u,v and `G=G_n`, the reduced part has

    D²J[u,v]=r_RIGHT Tr[G^(-1) DG[v] G^(-1) DG[u]]
              -r_RIGHT Tr[G^(-1) D²G[u,v]].             (16)

Add the actual boundary second derivative of `-r_RIGHT h log(1-z)`.
Higher finite jets agree by differentiating the exact identity of smooth
matrix functions. Since G>=(1-z)I, no probability floor, invertible B,
constant bright rank or differentiable polar decomposition is needed.

## 7. Uniform cap removal, dark scope, and the live joint refinement

For a general fixed-dimensional archive chart assume

    ||D^n||<=K rho^n,  0<rho<1,
    ||D' ||<=L1, ||D''||<=L2.

Ordered product differentiation, with no commuting-tangent assumption,
gives for E_n=D^n(D*)^n:

    e0=K² rho^(2n),
    ||E_n'||<=e1=2n K³ rho^(2n-1)L1,
    ||E_n''||<=e2=2n K³ rho^(2n-1)L2
                   +2n(2n-1)K⁴ rho^(2n-2)L1².          (17)

Let t=z/(1-z), and let t1,t2 bound its first and second derivatives on a
compact z chart. The exact difference from the strict-clock limiting price
`J_inf=-r_RIGHT(h+q)log(1-z)` is

    J_clock-J_inf=-r_RIGHT Tr log(I+t E_n).

In operator norms of first and second source maps,

    |J_clock-J_inf|<=r_RIGHT q t e0,
    ||D(J_clock-J_inf)||<=r_RIGHT q(t1 e0+t e1),
    ||D²(J_clock-J_inf)||<=r_RIGHT q[
       t2 e0+2t1 e1+t e2+(t1 e0+t e1)²].                (18)

Thus the absolute price, its first source and its second source converge
uniformly, with no normalization or subtraction. At fixed z the limiting
DATA source is zero; with moving z the absolute limiting boundary source
`r_RIGHT(h+q)dz/(1-z)` remains.

For the original reflection, the true full D contains a unitary dark
sector. Apply this statement on the reachable archive only, or use (13)
directly on a chart with a fixed-rank dark subspace and a uniform bright
gap. In that case q=rank(I-B²), not the entire 127h archive. A moving
bright/dark rank does not invalidate any FINITE formula, but prevents the
uniform limiting assertion: for example B(a)=1-a² changes the limiting
price at a=0. This is a genuine boundary, not a reason to drop dark modes.

Most importantly, n->infinity at fixed gapped B is NOT the original
heat/refinement limit. The owned native scaling is

    B_h=I-alpha_h Delta_h,   2n_h alpha_h -> beta>0.

Its bright gap closes as h decreases. On the already-owned spectral/source
domain `B_h^(2n_h)` approaches `exp(-beta Delta)` and retains its nonzero
feedback source. Equation (2) holds EXACTLY before that limit, so every
owned finite/refining feedback-source result can be consumed without a
new `(M-d)` multiplier. No new full-UV, all42, Lorentz or metric-descent
theorem is inferred from this observation.

If dim(H_h) grows along refinement, the absolute clock-boundary value
`-r_RIGHT dim(H_h) log(1-z_h)` can itself diverge. Equation (2) retains it.
Fixed-z field-source transport does not assert convergence of the full
absolute price or provide a renormalization.

## 8. The complete remaining ledger is retained, not identified by the determinant

Let U_k be the actual lifted native encounter and let R_k=U_(k-1)...U_0
be its prefix. If L_k is its actual supplied cost effect, the complete
encounter cost on the initial input is

    C_run=sum_(k=0)^(M-1) R_k* L_k R_k,

with M=n+1 for the strict-clock realization, plus the true preparation,
forward-routing, storage and terminal costs. In particular the final
encounter whose output lies beyond the cut is fully counted.
Every derivative of R_k and L_k is retained. This is the owned causal
price pullback applied to this explicit execution. It is not the port-code
cost of fresh128 pointer trials. Any selected information functional is
evaluated on the actual retained outputs and final archive, including its
real preparation and cut. No CQ/Book identification is made.

Consequently, for an actually supplied remaining ledger L_actual,

    S_new = J_clock + L_actual
          = -r_RIGHT h log(1-z) + J_v8,n + L_actual.      (19)

This is the complete price identity available here. It is not legitimate
to set L_actual to the old fresh-workspace ledger by matching (1). The
physical full-price selection, every extra implementation clock, native
routing admission and the independent upstream equations remain separate
parent premises. The new result removes the unspecified clock overlap for
the DECLARED coherent all-return realization, not for arbitrary programmes.

## 9. Narrow validation and original source owners

The companion checker pins and consumes:

* `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md`,
  §§03.3.0–03.3.2, 03.25–03.26;
* `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md`,
  §§06.4–06.6.B, 06.8.F;
* `A4D_EXECUTION_CLOCK_PRICE_ARCHITECTURE_2026_10_21.md`, §§3–5,8;
* `A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md`, §1;
* `sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md`, §§2–5,7;
* `A4D_ARCHIVE_FUTURE_CAUSAL_SELF_ENERGY_AND_DETECTOR_TIME_2026_10_19.md`, §2;
* `sources/d0_execution_clock_source_2026-10-21/check_execution_clock_source.py`,
  its literal native full128 row constructor only;
* `03_FORMALIZATION/D0/Evolution/FeshbachSchurTimeDelayOwner.lean`,
  its finite path grammar and separate convergence premise.

The focused checker reports **68 PASS**. Normal Python and `python -O`
produce byte-identical result receipts. Exact arithmetic checks the
general unitary archive identity, a finite causal unitary network, the
reflection determinant through a dark mode, the compulsory first tick,
and a changing bright/dark rank. The literal native constructor checks
all 128 original Kraus blocks, the full128 reflection and archive
identities, delayed returns, noncommuting first and second source jets,
and both fixed and moving z. Its largest finite-identity numerical error
is `1.31e-18`; independent native-row finite differences give first- and
second-source errors below `2.82e-14` and `3.73e-11`, respectively.

Run `python3 check_forward_archive_book.py --repo /path/to/d0_15` with
NumPy and SymPy available. The checker also discovers a repository
ancestor when embedded beneath the repository; no scratch path is coded
into it. `SOURCE_PINS.json` fixes all eight inputs at the stated commit.

No old suite, continuum root search, all42 validation, remote CI or Lean
build is rerun. The analytical proof is (3)–(16); narrow exact polynomial
and original-carrier numerical controls check the new application and its
clock/cut boundaries. Native numerical checks are tolerance checks, not
interval-certified numerical digits. GR_closed=false.
