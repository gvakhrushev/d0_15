# Native Golden herald for the actual port cost

21 October 2026. Native realization within existing PR #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE,
constitutive/native-programme-v1. Local input f7a8a534564be14d3f3f22874e6deb21ea2610d5.
Consumer: the analysis-only cost marker in
[the original all128 paid-port transfer](sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md),
then Gate A and the complete-price Gate B in the
[common native map](A4D_NEXT_COMMON_MAP_CONSTRUCTION_GATE_2026_10_21.md).
Write paths are this proof and the associated checker/receipt in the
existing source_selection/metric directory. No new task or price law.

The actual analysis marker at x=exp(-t)=p=phi^(-1) has a finite coherent
implementation using the original Golden gate and retained port controls.
All failure flags are explicit. Where its input effect is noncentral,
it rules out a free scalar normalization on the full admitted input space. The added
information source is calculable for two specified readout cuts; it is
not assigned as compulsory Book Info.

## 1. The actual instrument and the original Golden gate

Keep every original alpha=(b,k), all CAR16/site coordinates and oldRIGHT.
The original complete history has

    V_n psi=sum_omega |omega> K_omega psi,
    C_port(omega)=sum_j(1+b_j)=n+N_port1(omega).

The owned Kraus completeness gives V_n*V_n=I. The original Golden gate is

    G=[[a,-p],[p,a]],   a²=p, p²+p=1.

After each recorded round append two fresh flag qubits. Apply G to the
first flag, and controlled-G to the second with the STORED port b as
control. Both gates are forward operations. For b=0 the flags are
(a|0>+p|1>) tensor |0>; for b=1 they are
(a|0>+p|1>) tensor (a|0>+p|1>).
All original and flag records are retained. The circuit never reads or
resets data, and tensors the identity on oldRIGHT.

The herald accepts precisely when all flag registers are zero. The actual
success amplitude on a history is a^(C_port)=p^(C_port/2). Therefore

    V_success psi=sum_omega p^(C_port(omega)/2)
                              |omega> K_omega psi,
    P_success=Z_n(log(phi))
             =Tr Phi_log(phi)^n(rho).                    (1)

This realizes the owner's EXACT all128 cost transform at one native
Golden point. It does not supply a coherent coin with an arbitrary
real x, or convert the previously diagnostic t-family into free physical
variations. Controlled Golden access, fresh flag preparation, routing
and their full native costs remain implementation premises.

## 2. Full complement and the noncentral normalization test

Every rejected flag string remains an ordinary output of the same
unitary circuit. Its total effect is I-G_p,n, where

    G_p,n=(Phi_log(phi)*)^n(I).

For n=1 the already-owned paid-port identity gives EXACTLY

    G_p=p[I+epsilon p(p-1)Delta]
       =p I-epsilon p^4 Delta,                           (2)
    p² I<=G_p<=p I.

The bounds follow without a spectral ansatz: the full port effects
E0,E1 sum to I, and G_p=p E0+p² E1. Failure has effect
I-G_p=p² I+epsilon p^4 Delta. No failure effect was chosen after seeing
the desired response, and no square-root dilation primitive was added;
the actual Golden flags construct that complement.

A state-independent scalar normalization c V_success is an isometry on
an admitted input fibre precisely when c² G_p,n=I there. On the full
one-round fibre, (2) permits this only if Delta is scalar (apart from
trivial epsilon=0). A genuine restricted cut must test its actual
compressed Gram instead; it cannot be inferred from a full-space
counterexample.

Even a scalar BASE value is insufficient for a scalar first-jet
normalization. At Delta=lambda I,

    (dG_p)_traceless=-epsilon p^4(dDelta)_traceless.       (3)

Thus a nonzero traceless admitted dDelta obstructs normalization in that
direction, although the base Gram is scalar. The actual complete fields,
clock epsilon and preparation are retained.

This is a concrete type test before using the
[single absolute-anchor inverse](A4D_ABSOLUTE_LOOP_ANCHOR_AND_GR_ERROR_BUDGET_2026_10_21.md).
That inverse assumes a proved common scalar factorization on the actual
relative operator. It does not normalize an arbitrary paid Kraus family.
The present construction supplies a physically heralded candidate with
leakage, rather than silently installing a state-dependent denominator.

For one round, the actual calibrated success statistic also satisfies

    P_success=p-p^3(E C_port-1),
    d E C_port=-p^(-3) d P_success.                     (4)

This recovers the KNOWN port-cost mean/source, not unknown label, work,
or Book information prices. For all n, (1) and its complete causal
derivative use the owned CP recursion, without enumerating 128^n paths.

## 3. The marker is an extra amplitude operation

One Golden flag per code unit gives amplitude p^(C/2), hence probability
marker p^C. TWO flags per code unit instead give amplitude p^C and
probability marker p^(2C). Both multiply the ALREADY EXECUTED Kraus vector.
Neither identifies its factors with the absolute Book coefficients
before the native memory-algebra binding is proved. This keeps the
amplitude, probability and extra-marker types of
[BOOK_SOURCE_BINDING section 3](sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md).

The coherent physical schedule in section 1 has TWO executed gate slots
per original round, including controlled-G when b=0. Its number of slots
is 2n, not the random logical enabled-rotation count C_port. A protocol
which measures b first and skips a gate has a different coherence,
clock and price. The two-flags-per-unit implementation has 4n such slots.
Primitive decompositions of controlled-G and all preparation/work remain
in the actual ledger.

## 4. The exact new information source

Choose a declared final FULL pointer measurement of original histories
and every challenge flag. Padding flags for disabled rotations stay
zero. Conditional on omega, the enabled flags are independent Golden
draws and their number is C_port(omega). Hence exactly

    H_phi(original history,all flags)
        =H_phi(original history)+h_phi(p) E C_port,
    h_phi(p)=p+2p²=2-p.                                 (5)

This is a chain-rule identity for the complete stored record. The
original data may have arbitrary correlations and oldRIGHT entanglement.
With p fixed its additional entropy source is

    dH_extra=(2-p) d E C_port.                          (6)

For this specified Cost-minus-pointer-entropy valuation, let W_extra be
the actual full cost/preparation/routing/work of the added circuit, with
all independently moving input terms. Then

    dS_new-dS_old=dW_extra-(2-p) d E C_port.             (7)

A fixed gate-slot count is not a proof dW_extra=0. If field-independent
unit prices and all other required costs really are supplied, its fixed
2n schedule has zero field-cost derivative while (6) can remain nonzero.

A different final binary projective measurement that reads ONLY the
herald bit from a fully coherent pure input, preserving coherence within
each unresolved flag subspace, has two pure conditional global blocks and
entropy h_phi(P_success). Its source is h_phi'(P_success)dP_success.
That is a different information cut from (5). Original records measured
earlier require their joint entropy instead. These actual distinctions
prevent using the calibration probe as an unpaid source-neutral anchor.
No equality with compulsory Book03 Info is asserted.

## 5. Finite Golden samples recover the complete port-cost distribution

For fixed n, retain the original complete instrument and define only its
reported cost-sector probabilities

    Q_r=sum_{omega:C_port=n+r} q(omega),  r=0,...,n,
    P_n(x)=sum_r Q_r x^r.

No history is erased from the execution. Apply k copies of the flag
construction per round, k=0,...,n, retaining every copy and failure.
Their success probabilities are

    Z_k=Z_n(k log(phi))=p^(kn) P_n(p^k).                 (8)

The k=0 value is the already-owned normalization Z_0=1. Since the n+1
Golden nodes x_k=p^k are distinct, elementary polynomial interpolation
gives the exact structural inverse

    ell_k(x)=product_{j!=k}(x-p^j)/(p^k-p^j),
    P_n(x)=sum_{k=0}^n p^(-kn) Z_k ell_k(x).            (9)

Thus these finite native-Golden experiments determine every Q_r, its
full admitted source dQ_r, E C_port=n+P_n'(1), and the whole analytical
transform x^n P_n(x). This reconstructs an analytical function from
physical samples; it does not implement a freely variable real-x coin.
At fixed n,p the same linear inverse applies to every admitted field,
preparation and compatible clock jet, using the owner's complete dZ.

For n>=2, one Golden sample is insufficient even for the cost source.
For n=2 the normalized cost-sector direction

    dQ=(p,-(1+p),1)

has sum dQ=0 and dP_2(p)=0, while d E C_port=1-p=p²!=0.
It is admitted as a probability-distribution direction near a strictly
positive Q, not asserted as an independently writable native field jet.
This excludes recovering every source from a single scalar statistic
without an additional actual native constraint. It does not contradict
the exact one-round calibration (4).

Each experiment still has its own extra 2kn coherent gate slots, full
preparation/work and k(2-p) E C_port pointer entropy. Summing k=1,...,n
uses n²(n+1) added abstract gate slots per collection of one run of each
experiment, before repetitions needed to estimate probabilities.
This is a mathematical resource count, not an optimal physical price.
The experiments require reproducible copies of the same complete input;
they are not alternate endings of one unrepeatable unknown state.

The inverse can amplify measurement errors. With
c_rk=[x^r]ell_k(x), the explicit bound is

    |delta Q_r|<=sum_k |c_rk| p^(-kn) |delta Z_k|.       (10)

The identical coefficient bound holds for errors in dQ_r reconstructed
from dZ_k at fixed n,p. No uniform-in-n conditioning or finite-sample
exactness is claimed. Full Book amplitude/Info/work and the metric-source
map remain separate obligations; learning the known port-cost statistics
does not choose their physical valuation.

## 6. Exact remaining application

The former analytical paid-port marker now has an explicit finite
Golden-point herald with its full complement, actual schedule and two
typed information sources. This removes an arbitrary-marker primitive
from that specified mathematical implementation. It does not select
the probe as compulsory, determine the full Book gain, or identify this
execution with the distinct N=1 CQ source construction.

Use (1)-(10) to price this SAME extension, if it is admitted, before
reading an absolute anchor or using the previous GR error budget.
Repeat-until-success, when required by a task, has its actual failure
probability and additional clocks; postselection is not free. All42
source compatibility, independent upstream equations, native field
stationarity, physical refinement and GR_closed remain open.

The [checker](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/check_golden_paid_cost_herald.py)
tests the complete eight-dimensional Golden controller, both herald
amplitudes, all flag outputs, the original full128 effect identities,
noncentral value/first-jet controls, the exact entropy/cost coefficients,
the n=2 interpolation inverse and the single-sample negative control. Its
[receipt](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/GOLDEN_PAID_COST_HERALD_CERTIFICATE.json)
does not reclassify a two-dimensional diagnostic effect as the original
full128 Kraus replay.

Author's bounded replay: 43 exact controls pass under Python 3.11.9 /
SymPy 1.12.1, with byte-identical normal and `-O` receipts and no stderr.
The six local Markdown links resolve; `tools/validate_repo.py` passes
with zero warnings. The receipt SHA256 is
`2b377e9405f43aa3ba9baf3c723a0364e116bb11cdc1c1dc9102e219ad744fe6`;
checker SHA256 is
`441337ab7773d5485152ab60af894060ec67d774d8e2e6cf425ecf6c63a73123`.
This is an author replay, not independent acceptance or a full128 rerun.
