# What matched information can see in the actual cleaned whole-J2 record

20 October 2026. Bounded read-only continuation of existing PR #334.
Initial inspected worktree HEAD `024e7fd382e0fe5c5e0330f63ad367cd8e78babf`;
the new live-CAR scope was then checked at
`20d976647fa52e247d15139d3f4f14351f175b70`.
Inputs are the existing `book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md`,
`source_selection/records/STOPPED_ADAPTIVE_EXTENSION.md`, the accepted
`STOPPED_FIELD_SADDLE.md`, and the distinct full128 QGT/Jones owners.

## 1. Exact same-carrier conclusion

For the supplied three-query coherent cleanup, EVERY full-output first
derivative at the common-null stratum factors through the one scalar dt.
This includes all work, actual report/clock and arbitrary fixed input
entangled with retained oldRIGHT. At an Einstein stationary point dt=0,
the entire output state has zero field tangent. There is no hidden linear
work response from which a matched Fisher term could repair the saddle.

The stronger exact calculations below show:

    one trial:     root fidelity = 1-2t^2;
    fixed-k stop:  root fidelity = 1-2t^2/d_k(t),
    d_k(t)=1-c^2(1-2t^2)+2cs t(1-t^2),  d_k(0)=q=s^2>0.

Here root fidelity means Tr sqrt(sqrt(sigma*) sigma_y sqrt(sigma*)).
The formulas hold near t=0, where the displayed expressions are positive.
For pure complete dilations these are the actual state overlaps. They
also hold for the actual complete fine-pointer/CQ tape at its clean
reference. Hence its Bures squared distance is O(t^2), which is O(||v||^4)
on the stationary coframe/shared-link slice t=O(||v||^2).

Every C2 fixed valuation of this full state has field Hessian c H_t at
such a root. A smooth matched divergence has c=0 and therefore ZERO field
Hessian. Adding it preserves the existing root but cannot repair the
nonzero indefinite quadratic form. A nonsmooth/rank-singular functional,
moving preparation/reference, extra raw measurement or different record
interface is outside that conclusion and must carry its own native law.
The reverse relative entropy calculated below is an exactly evaluable
candidate valuation of the actual tape, not a derivation that Book03
selects it as physical Info or adds it to the actual price.

## 2. Complete one-trial isometry, including oldRIGHT

Keep the owner's fixed clean embedding J, P=JJ*, Q=I-P, real signal t,
and full supplied unitary W(y) satisfying J*WJ=t I. Write L_y=QW(y)J.
The ENTIRE cleaned output isometry is

    V_y=f0 |0>J + f1 |1>J - 2t^2 |1>L_y,
    f0=1-2t^2,              f1=2t(1-t^2),
    J*L_y=0,               L_y*L_y=(1-t^2)I.

At any reference point in Sigma, V*=|0>J. Directly,

    V*^* V_y=f0 I,
    (V_y-V*)^*(V_y-V*)=4t^2 I.                       (1)

Thus for ANY fixed normalized input purification |psi> including oldRIGHT,

    <Psi*|Psi_y>=1-2t^2,
    Fidelity(Psi*,Psi_y)=(1-2t^2)^2,
    half|| |Psi_y><Psi_y|-|Psi*><Psi*| ||_1
       =2|t|sqrt(1-t^2).                              (2)

Fixed Golden postrotation and the actual retained 0/10 report/clock
isometry preserve (1)-(2). Any physically accessible field-independent
CPTP readout can only reduce the trace-distance bound. No coherent
access to a dephased history is assumed by using a purification as a bound.

Differentiating at Sigma gives

    D_v V=2 dt[v] |1>J,             V*^* D_v V=0,
    QGT(v,w)=4 dt[v]dt[w] I,
    QFI(v,w)=16 dt[v]dt[w].                           (3)

The last equation uses the standard quantum Fisher normalization four
times the horizontal pure-state metric. For an arbitrary fixed mixed
logical/oldRIGHT input the same value follows from the orthogonal port
rotation: its SLD may be taken as 4 dt[v] X_port on the input support.
Other output readouts have Fisher metric bounded above by this one.

The field dependence of W is NOT frozen: DL_y can be nonzero while dt=0.
Its coefficient in V_y is t^2. Along a stationary root, t=O(||v||^2),
so that part first appears in the output amplitude at order ||v||^4.
The finite checker explicitly varies the leakage direction while keeping
the clean compression fixed; the raw W output changes but V has no tangent.

## 3. Exact complete fixed-k stopped tape

Fix an admitted k with c=cos(k theta), s=sin(k theta), c s!=0, and stop at
the first actual port1. No policy, query, reference or input preparation
depends on an external field value. Fresh work is supplied and charged
at each trial; all previous records remain. Put

    alpha0=c f0-s f1,          alpha1=s f0+c f1,
    K0=alpha0 J+2s t^2 L_y,
    K1=alpha1 J-2c t^2 L_y.

The original scalar effects make the coarse stop geometric even when
conditional logical states change. In a neighborhood of zero q_k(t)>0,
so this countable halted tape is well defined and has finite expected
attempts. A Stinespring dilation of the full stopped instrument is a
direct sum over terminal histories; it is a mathematical bound, not an
extra physically admitted coherent erasure or superposition of histories.

At the reference all work is clean. For length n the reference amplitude
is s c^(n-1); projection of the actual full branch onto that clean tape
is alpha1 alpha0^(n-1) times the unchanged input. Therefore the exact
full-dilation overlap is the convergent series

    eta_k(t)=sum_(n>=1) s alpha1 (c alpha0)^(n-1)
            =s alpha1/(1-c alpha0)
            =1-2t^2/d_k(t),
    d_k(t)=1-c alpha0.                                 (4)

This is independent of every unobserved block of W and of the fixed input
or oldRIGHT entanglement. The identity d_k-s alpha1=1-f0=2t^2 proves the
last equality. In particular

    1-eta_k=2t^2/q+O(t^3),
    Bures^2=2(1-eta_k)=4t^2/q+O(t^3),
    QFI|Sigma=(16/q) dt tensor dt,        q=s^2.         (5)

For the actual full fine-pointer/CQ tape, baseline support consists of
clean histories only. In the length-n clean block the input density is
unchanged and its weight is alpha1^2 alpha0^(2n-2). All dirty histories
lie in orthogonal retained blocks. Hence its root fidelity is exactly
the sum of the positive square roots of these clean weights against
q(1-q)^(n-1). Near zero the signs of alpha_b agree with c,s, giving
precisely eta_k in (4). Thus (5) is also the actual CQ metric, not merely
an upper bound from an inaccessible purification.

Equivalently, the geometric coarse law has Fisher information
I_q=1/[q^2(1-q)]. Since q_k'(0)=4cs, its t-Fisher information is 16/q.
The complete fine tape supplies no extra first-order Fisher direction.
The exceptional k=0 has no finite stopped baseline at t=0 and is not
silently included in this theorem.

## 4. A finite exact full-record matched relative entropy

The reverse CQ relative entropy is well defined near zero, with ALL
dirty branches retained in sigma_y:

    D_phi(sigma* || sigma_y)
      = [ln(q/alpha1^2)
         +(1-q)/q ln((1-q)/alpha0^2)]/ln(phi)
      = 8 t^2/[q ln(phi)] + O(t^3).                    (6)

Proof: only clean reference blocks contribute. Their conditional logical
and oldRIGHT density is unchanged, so the quantum relative entropy reduces
exactly to the displayed classical cross likelihood. Sum n-1 under the
reference geometric law, whose mean is (1-q)/q. No failure postselection
or renormalization of the actual law is made. The classical full-pointer
version is the same formula.

For completeness, the probability of at least one dirty work event is
EXACTLY

    1-alpha1^2/(1-alpha0^2)
       =r(t)/(1-alpha0^2),     r(t)=4t^4(1-t^2).        (7)

Thus the forward relative entropy D_phi(sigma_y || sigma*) is INFINITE
for every sufficiently small nonzero t: the reference assigns zero to
genuinely present dirty outcomes. A pure coherent reference likewise has
rank-one support and generally gives infinite Umegaki relative entropy
in either direction when the pure states differ. Neither infinity has
a finite Fisher Hessian. Bures fidelity is finite despite those support
changes; the reverse CQ formula is finite because the old clean support
is contained in the new support.

A full-rank noisy reference can remove that singularity only as an actual
separately declared reference. No noise floor or extra cost is inserted
here. Formula (6) already supplies a finite same-record test without one.

## 5. All smooth fixed record valuations have the same second-form shape

Let y0 be an owned stationary root with t(y0)=0 and Dt(y0)=0. Keep the
actual input, oldRIGHT marginal, observer frame, query compiler, paid
primitive counts and reporting interface fixed under the coframe/link
variations. The accepted saddle slice has

    H_t=[[0,-g],[-g,-2gD]],    g,D>0,    det H_t=-g^2.

One trial has the operator expansion V_y=V*+t A+O(t^2), A=2|1>J.
The stopped fixed-k dilation has the same form with a fixed bounded A_k.
To justify the latter without differentiating a divergent series, split
into its clean scalar series and dirty orthogonal part. The clean sequence
alpha1 alpha0^(n-1) is analytic in ell^2 near zero since |alpha0|<1. By
(7) the dirty vector norm is O(t^2). Thus the remainder estimate is uniform
over the actual local W chart and fixed normalized input. On density
operators, after any fixed CPTP readout,

    sigma_y=sigma*+t L+O(t^2)                         (8)

in trace norm, with a fixed traceless Hermitian tangent L. The input may
be mixed or entangled; its purification supplies the same bound.

For any real C2 functional Phi of that state, with no explicit extra
field dependence and bounded local Frechet derivatives,

    Phi(sigma_y)=Phi(sigma*)+c t+O(t^2),
    c=D Phi(sigma*)[L].

As t=O(||y-y0||^2), its field Hessian is EXACTLY

    Hess_y(Phi composed with sigma)|y0 = c H_t.        (9)

This is a second-order value identity; no unsupported smoothness of an
optimized policy envelope or entropy at a rank birth is assumed. A C2
record valuation with c!=0 has the same indefinite two-dimensional
second form. If c=0 its quadratic form vanishes. It cannot supply an
independent positive-semidefinite matrix on this slice.

For a smooth matched divergence at its minimum, its first derivative
annihilates normalized-state tangents, so c=0. The explicitly computable
reverse divergence (6) confirms this even without assuming smoothness
on all neighboring density matrices: it is O(t^2)=O(||y-y0||^4).
Adding it to the existing stopped price leaves its nonzero kappa H_t
unchanged. Choosing a valuation whose c cancels kappa cancels the entire
quadratic source; it does not derive a positive quadratic stabilizer.

Every point of Sigma gives exactly the same final state for the fixed
input and ledger, including the flat-link coframes a!=1 where DJ2 need
not vanish. Replacing the original price by a matched divergence alone
therefore creates a zero-value minimum on this whole indistinguishable
stratum, not only on the Einstein roots. Adding the finite divergence
preserves the original first source on Sigma but leaves the saddle.

## 6. Preparation, selector and unbounded-policy limits of the result

If the initial state/preparation has its own y-dependent tangent, (8)
acquires that independent term. If the reference or measuring apparatus
moves with y, its derivative must also be included. These are potential
native sources, not terms canceled by the theorem. The existing saddle
test intentionally holds those inputs fixed and varies the original
coframe/shared link, with constant original CAR matter.

A fixed finite field-independent monitored selector or finite mixture of
the admitted fixed-k programmes has blockwise the same factorization
(8). Its initial choice record and exact costs remain. It adds no new
first-order field direction. This does NOT assert a common differentiable
state for arbitrary unbounded adaptive programmes or their pointwise
price infimum. In particular no free randomizer, field-value lookup,
unpriced measurement of the internal query or early information tap is
included. Capturing an intermediate W record before coherent cleanup
changes the experiment and may change its scalar cancellation.

The newly owned `book_source/NATIVE_CAR_ACTUATED_METRIC.md` is a genuine
different access path: its original paid K/G word changes the LIVE
scalar/top matter before the field query, keeping its four-mask norm and
oldRIGHT. The query responds to that new material input and can expose
Brinkmann H that the unactuated null query did not distinguish. This is
not postprocessing the cleaned output above. Likewise an actual retained
programme register that already encodes the moving coframe or query
parameters has its own tangent. This note does not claim that such a
register is fixed, invisible, or included at zero price. Its real
preparation/controller/clock/Info derivatives must be added to a claim
about the FULL physical action. Only the supplied coherent-query output
and its complete three-query work/tape are treated here; original
field/CAR data in larger native interfaces are not declared unobservable.

## 7. Positive route and the separate full128/Jones interface

For an independently ADMITTED retained readout Z(y), a matched smooth
divergence can contribute K=(DZ)^* G DZ>=0, where G is its information
metric. This can stabilize a point without being a constant multiple of
the original source. A necessary condition is that ker DZ contain no
direction on which the old Hessian is negative. For a fixed reference
this argument preserves the matched point; preserving an entire family
of roots additionally requires the divergence first source to vanish
at each member, not only at that one reference.

The actual full128 QGT owner proves

    Q(v,w)=p^3 B_v^*B_w+p^2 W_v^*W_w,

with B_v=M^*d_vM and W_v=(I-MM^*)d_vM for its ORIGINAL reflector output.
The separate two-round Jones experiment has the published 34-dimensional
metric/link probability chart on its fixed homogeneous Fourier fixture.
Those are genuine possible sources of nonzero retained information.
They are not the cleaned whole-J2 state. A field-independent processing
of (8) cannot produce their nonzero field tangent at this stationary root.
One must instead prove and price the actual same-field preparation,
readout and carrier transport. The existing homogeneous Jones rank does
not by itself prove injectivity on this localized curved shared-link
slice or preserve all of its stationary roots.

Changing logarithm base to phi rescales (6) by 1/ln(phi); it cannot restore
a missing tangent. The Bianconi action previously inspected in
`source_selection/RESIDUAL_AND_AVERAGING.md` contains unnormalized volume,
trace and induced-metric terms. It is not a normalized matched relative
entropy of this final tape. Such additional native quantities could escape
(9) only through their actual independent field dependence, which remains
a required same-execution substitution.

No new action or fitted stabilizing term is proposed. The usable criterion
is exact: the needed stabilizer must come from information with a nonzero
first field response BEFORE it is compressed to this scalar cleaned tape,
or from a genuinely different declared non-smooth variational law. It
cannot be recovered by revaluing the same final record smoothly.
