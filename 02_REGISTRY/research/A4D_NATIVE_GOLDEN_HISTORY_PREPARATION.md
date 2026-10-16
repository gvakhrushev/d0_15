# Complete retained golden preparation and cylinder refinement

Research parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, [#310](https://github.com/gvakhrushev/d0_15/pull/310).
Input head: `1093df6bbd2f7a0fb91204e87240ad035256d661`.
Base: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Date: 2026-10-09.

## Result and critical dependency

The prior [scene/history realization](A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md#69-owned-scene-history-realization-and-its-full-return-action)
constructs the actual scene readouts and reversal. Its endpoint Hilbert
isometry has, at vertex v, the equal-amplitude ray on its d_v incoming
histories, where d_v is 20, 22 or 24. Mathematical readout matrices alone
do not prepare that ray from the primitive golden factors. This packet
constructs and verifies a complete finite preparation experiment from
those factors, with every raw record and unsuccessful outcome retained.

The literal seed, complete recursive word, every-coordinate coefficients,
scene-fiber binding, error rate, expanded word cost and prefix-cylinder
extension are kernel-proved. The complex phase in the recursive word
has a real two-coordinate realization as the eighth power of the same
owned golden gate. No fitted angle or fair splitter is assumed.

Two issues that would otherwise invalidate the transfer are made explicit:
retained stopped retries do not provide a uniform coherent history lift,
and the coherent word's successful phases differ between degrees 20 and
24. The latter is proved for the actual golden value. The normalized
successful vector used in the error estimate includes that phase; it is
not advertised as an implemented positive-phase history isometry.

This is a complete declared finite experiment and its compatible cylinder
extension, not a proof that M1 admits its Boolean routing controller,
chooses its program, or binds its cost to a physical mesh. It advances
G0b without closing G0b. Native heat-carrier ownership, full tangents,
physical source/Ward, contrast/stationarity, curved roots and GR stay open.
The original #310 fixed-source/raw-owner terminal and #202/#317 criteria
remain intact.

## 1. Independently owned inputs

Use p=primitiveRoot=phi^{-1} and a=sqrt(p). The actual core identity is
p+p^2=1, so a^2+p^2=1. The existing golden gate is

    G = [[a,-p],[p,a]].

`D0.Representation.GoldenOrderInterferometer` owns this gate and its blank
column (a,p). `GoldenCoherentMemory.fullStep` owns the reversible recorded
four-state evolution. Removing the system golden gate from fullStep gives
the retained CNOT recording permutation. All these identities are proved
against those definitions, not against a replacement action.

`D0.CondensedAnchor.DetectorSupportGoldenWeight` owns cylinder weights
mu(A)=phi^{-1}, mu(B)=phi^{-2} and their exact refinement consistency.
The operational bit convention is false=A, true=B; the anchor's letter
convention is true=A, false=B. The explicit complement of the bit binds
these conventions. Their squared amplitudes are proved equal to the
actual `cylWeight` values. Refinement below is consequently the normalized
cylinder inclusion, not an independently selected splitting ratio.

The scene input is the actual `Adj31` and `fullDegreeValue`, with its
incoming histories. The packet recomputes every incoming cardinality
with kernel `decide` and proves its equality to the actual rational
degree by finite-sum algebra. It does not consume the owner's compiler
trusted counting theorem. Transitive axiom audit is supplied for every
new printed proposition.

## 2. Whole retained seed, not postselected probabilities

For n pairs, Word(n) contains all 4^n raw pair words. Their positive seed
amplitude is the product of the corresponding a and p factors. Read the
first odd pair. Flipping that pair exchanges its two possible labels
without changing amplitude. The complete routing on (word, record-bit)
is the composition of two involutions:

1. XOR the first odd label into the record bit, with false on no odd pair.
2. Flip the first odd pair controlled by that record bit.

This is a full permutation on all 2*4^n states. It retains all earlier
pairs, the odd-pair position and every suffix, and leaves every failed
raw word unchanged. If the routed retained word w has firstLabel(w)=false,
then the two successful labels have exactly the same amplitude and the
same entire retained w. Thus the factorization is coherent and pointwise,
stronger than equality of diagonal probabilities.

With q=a^4+p^4=3-4p, the full failure mass is q^n and each successful label
has mass (1-q^n)/2. These identities hold by induction for every n.

Take five disjoint streams, each with n=4 pairs. The actual seed is the
40-factor tensor golden gate, identity on five blank record bits, followed
by the tensor routing permutation. Its matrix acts on 2^45 states. A
generic tensor-unitarity theorem and its actual blank column construct
both-sided unitarity; that matrix is not numerically enumerated.

For any accepted five-bit code set S, the validity mask requires all
retained streams successful and code in S. Complete accepted and rejected
masses are

    s_d = (d/32)*(1-q^4)^5,
    epsilon_d = 1-s_d,                  d=card(S).

All invalid codes and failed pair streams remain present. For d=20,22,24,
0<=epsilon_d<=11/16 follows from the primitive golden preparation.

For the real scene, `SceneIncoming(v)` is the actual incoming-neighbor
subtype. Its members inject into the 32 five-bit codes, and the image
`sceneAcceptedCodes(v)` has exactly the actual degree. The displayed
injection is a coordinate enumeration. Every successful neighbor has the
same retained-word amplitude, independently of that enumeration. The
finite injection is not claimed as physical addressability.

## 3. Why retained stopping does not suffice

For a declared stopped-retry assembly, the overlap of complete rejected
records for two acceptance sets is the rejection mass of their union.
It is no larger than the rejection mass of the larger acceptance set.
The corresponding retained-prefix Gram is

    sqrt(s_small*s_large) * sum_{j<K} c^j.

Its overlap is bounded by sqrt(s_small/s_large). For degrees 20 and 24
this is sqrt(5/6)<1, at every K; nested sets approach that bound. Shrinking
the failure probability therefore does not, in this declared retry class,
remove the degree-dependent retained record. The packet prints the
assembly hypothesis: it does not claim that every possible native
controller is covered by this obstruction.

## 4. Literal coherent recursion with the owned phase

Define omega=(a+i*p)^2. The owned recording and golden gates give

    (I tensor G) CNOT (I tensor G^transpose) CNOT = diag(I,G^2).

The realification of omega is exactly G^2. Set w=omega^4. Realification
commutes with powers, so w is exactly G^8 in real two-coordinate form.
Its norm is one, and

    Re(w)=673-1088*p,
    r=2*Re(w)-1=1345-2176*p,             0<r<1/6.

This exponent specifies this preparation experiment. It neither selects
physical dynamics nor adds a phase angle to the core. Arbitrary Boolean
validity/address controls remain a separate admission obligation.

For any complete unitary seed U, blank basis vector z and validity mask
chi, let B be phase w on z and identity elsewhere, and Q phase w on all
valid coordinates. The literal recursion is

    U_0=U,
    U_{k+1}=U_k B U_k^adjoint Q U_k.

Every U_k is two-sided unitary. For its complete column psi_k=U_k z and
full rejected mass epsilon_k, every rejected coordinate gets the common
multiplier

    b(w,epsilon)=w*(r+(1-r)*epsilon),

and every accepted coordinate gets

    g(w,epsilon)=w^2-(w-1)^2*epsilon.

The whole recorded directions are preserved pointwise. Summing every
rejected coordinate proves, rather than assumes, the actual recurrence

    epsilon_{k+1}=epsilon_k*(r+(1-r)*epsilon_k)^2.

The successful coefficient alpha_k and failed coefficient beta_k are
explicit recursive products. The all-coordinate theorem is

    psi_k(i)=psi_0(i)*(chi(i) ? alpha_k : beta_k).

For every actual incoming scene history and every successful retained
word, the successful amplitude is its original golden product times
alpha_k(epsilon_d). No measurement, reset or discarded record enters.

## 5. Quantitative rate and its real cost scope

The owned initial error lies in [0,11/16]. At r<=1/6, the first complete
step takes error to <=2/5 and the second to <=1/10. Thereafter the bad
amplitude multiplier is at most 1/4. For all k,

    epsilon_{k+2} <= (1/16)^k/10.

This is proved for the actual full routed seed and every actual scene
vertex, not only for a scalar recurrence postulated as a hypothesis.

If a literal seed word costs seed operations and each supplied phase
word costs phase operations, expansion of this recursive syntax gives

    C(0)=seed,
    C(k+1)=3*C(k)+2*phase,
    C(k)+phase=3^k*(seed+phase).

Consequently

    epsilon_{k+2}*(C(k+2)+phase)^2 <= (81/10)*(seed+phase)^2.

The earlier G^2 contraction rate alone has 9*q^2>1, and does not supply
this inverse-square word-cost bound. G^8 removes that specific rate/cost
mismatch. Counts for full Boolean routing/address compilation, native
minimum-description length, the Book 03 kappa budget, and any identification
with physical mesh are not supplied by this syntax theorem.

For a complete normalized output x with nonzero accepted mass s, define
y(i)=x(i)/sqrt(s) on accepted coordinates and zero on rejected coordinates.
The complete-vector identity and bound are

    sum_i |x(i)-y(i)|^2=(1-sqrt(s))^2+epsilon <= 2*epsilon.

It counts every rejected record. For the literal native scene experiment,
s>0, y has norm one and the squared error is <=(1/16)^k/5. y keeps the
successful phase of x. It is a mathematical comparison vector, not a
reset/postselection operation silently installed in the core.

## 6. Relative phase is a remaining real obligation

The success coefficient's phase depends on epsilon_d. For arbitrary unit
w, the exact area between two successful coefficients is

    Im(g(w,e)*conj(g(w,f)))=(2-2*Re(w))*(f-e)*Im(w).

The owned fast phase has Re(w)!=1 and Im(w)!=0, derived from its norm and
r bounds. The actual golden epsilon_20 and epsilon_24 differ. Their area
is therefore nonzero in the kernel. One common phase cannot align their
first-step successful rays. Equal-amplitude codes within a vertex do not
remove the relative phase between vertices.

The next preparation obligation is a real implementation of the derived
relative phase, or a proved readout/operator covariance that makes its
basis change admissible. Declaring it gauge, changing the readout, or
using y as an unconditional native preparation is insufficient. No
positive physical history-isometry transfer is promoted at this point.

## 7. Whole-cylinder refinement, with a hostile singleton control

Normalized golden inclusion appends the owned factor:

    iota_phi(x)=x tensor (a,p).

For every already-declared prefix operator A, its extension is A tensor I.
The packet proves the full matrix multiplication/adjoint laws, isometry,
rejected-weight preservation and intertwining. Extending U, B and Q by
identity on the entire suffix gives, at every recursive depth k,

    U_k^fine iota_phi = iota_phi U_k.

The full failure rate is exactly the same after refinement. This constructs
naturality for this explicit prefix program; it is not the assertion that
all native operators have these extensions, or that M1 forces the program.

B^fine must phase the complete coarse blank cylinder, not just one fine
blank basis state. The singleton rule diag(w,1) and the proper cylinder
rule w*I act differently on the actual factor (a,p). Their squared defect
is p^2*|1-w|^2=p^2*(1-r)>0. The kernel also proves the two matrices unequal
for every w!=1. Refinement that quietly marks each new factor blank fails
this test. Retained memory and phi refinement are used in the proof, not
introduced later as an interpretation.

## 8. Certificate, audit and unchanged parent obligations

Standalone [Lean capsule](certificates/a4d_native_golden_history_preparation.lean),
[printed types and axiom transcript](certificates/a4d_native_golden_history_preparation_output.txt),
[source receipt](certificates/a4d_native_golden_history_preparation_results.json),
[exact checker](certificates/a4d_native_golden_history_preparation_check.py)
and [ledger](certificates/a4d_native_golden_history_preparation_certificate.json)
are hash-pinned. There are 151 actual propositions; every type and
transitive axiom list is printed. Only Classical.choice, Quot.sound and
propext occur. There are 12 transitive D0 source pins and 239 exact controls.
The actual checker rejects all 32 false-scope and 15 false-exact ledgers.
The exact controls check all raw words through four pairs,
full routing/inverse fibers, both-sided seed unitarity and every coordinate
of complete eight-state steps including an empty validity fiber, golden
G^8, complete mass and relative phase, cost and singleton-refinement
failures. The 2^45 seed and all-depth/all-suffix statements have separate
kernel proofs and are not claimed as numerically enumerated.

Run the checker with `--expect` for its frozen ledger and compile the
capsule with the pinned source toolchain. False scope/exact ledgers must
be rejected. Printed propositions show which conclusions consume generic
seed unitarity and which construct the actual routed golden seed.

Open G0b inputs are Boolean controller/address and relative-phase admission,
native cost/refinement-budget ownership, and the real scene/history heat
carrier with its complete tangent and action law. Then derive own
metric/matter source and physical Ward, quantitative contrast, native
stationarity, joint curved roots, soundness/recovery and physical
constraints. No original parent, global closure or positive GR is closed
by this finite construction. No new action, temperature law, selector,
coupling, source prescription or physical postulate is installed.
