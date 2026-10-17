# Native retained-record admission: a quantitative controller boundary

Research parent: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, [#310](https://github.com/gvakhrushev/d0_15/pull/310).
Input head: `b09a822a1c9701309dd2e7c53fb5e451bd054689`.
Base: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Date: 2026-10-09.

The [retained golden compiler](A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md)
constructs a route in an explicitly addressed G/CNOT class. The native
admission question is whether the independently owned dynamics actually
supply the required operations. This packet tests the recording arrow
before adding another implementation, action or selector.

## 1. The owner interfaces and the class being tested

`Foundation.VerifiabilityNecessity.VerificationProtocol` owns states,
records, verification lines and catalogue-parametrized comparisons.
Correctness forces injective retention and class-level M1 independence;
physical implementation remains an application obligation in its owner.
`Foundation.EndogenousActionQuantum.ActionProtocol` owns an endpoint
cost with identity cost zero and nonidentity cost at least one. It does
not contain a program decoder or an actuation predicate. Its canonical
cost is a witness of that interface, not the history-composition law
needed by the field action.

BOOK_03 §03.10 bounds a test's *minimal description* by floor(phi^k).
That bound limits finite tests; it does not by itself supply an
instruction decoder, arbitrary gate placement, or a bound on executed
path length. BOOK_03 §03.26.1–4 supplies golden matrices and reversible
recording, while explicitly retaining physical preparation and actuation
obligations. These different owner interfaces are not silently identified.

The test class is specified by its generators. Let A be any finite
active carrier and R a finite abelian record group (bit records use
R=(Z/2Z)^r). Admit:

* every complete orthogonal U_A on the active carrier, acting as U_A tensor I_R;
* every one-way reversible recording C_f:(a,r)->(a,r+f(a)), with an arbitrary
  supplied function f:A->R;
* arbitrary finite words in those operations, and their reversals;
* faithful complete extensions which retain the same old-record probe.

This is deliberately more generous than a single golden active gate.
It permits any active computation and any controlled XOR record update.
The generators do not include an old record controlling the active
computation, coherent rotation of that old record, or arbitrary nonlinear
archive permutations. Those operations require their own admission.
The class is not asserted to exhaust D0. No output equation is inserted
as a native gate; the invariant below is a consequence of the generators.

## 2. A retained-record invariant holds for every word

For any record translation X_t:(a,r)->(a,r+t), all generators commute
with its complete permutation matrix. The recording proof is just
(r+f(a))+t=(r+t)+f(a); active orthogonal operations leave the record
coordinate alone. Orthogonality and commutation survive every word.
For the complete real state x define

    chi_X(x)=x^T X x.

Then, for every complete orthogonal U with UX=XU,

    chi_X(Ux)=chi_X(x).

The actual four-coordinate native golden system gate, recording CNOT
and `GoldenCoherentMemory.fullStep` commute with I tensor X. In contrast,
the same golden gate placed on the old record does not commute when
p is nonzero. Thus matrix ownership of a golden gate is distinct from
admission of its placement on retained memory.

The generic generating class and every-length invariant are kernel
proved. Reversal is covered for symmetric flip probes. In the literal
four-pair history, the last-bit flip is the corresponding Z/2 translation:
read seven bits as the other coordinates and the eighth as the retained
bit. The five-stream carrier is a product of those bit groups. This
coordinate reading adds neither an operation nor a scale.

## 3. The actual target requires a different old-record correlation

Use the same raw golden pair histories and first-unequal routing as the
pinned preparation. Write

    p=p0=phi^-1, a=sqrt(p), q=a^4+p^4=3-4p,
    s_n=(1-q^n)/2.

For one stream of n pairs, toggle the last bit of the whole raw record.
The unfiltered, normalized product golden state has flip correlation
2ap for every n>=1. The unnormalized first-label-false state has cross sum

    K_(n+1)=q K_n+(ap)^2*(2ap), K_1=0,
    K_n=2ap*s_(n-1).

The equality is proved over every raw coordinate, with failures retained
in the complete carrier. It does not invoke postselection as dynamics.
At n=4, the normalized common accepted record therefore has

    chi_target=2ap*(1-q^3)/(1-q^4).

For five streams, the very same common record eta from the previous
packet is a product of the normalized accepted stream factors. Flipping
one old bit in its first stream gives that same correlation. Tensoring
with each actual normalized incoming code ray preserves it. All 33
actual vertices, including degrees 20,22,24, are kernel bound.

The fixed, independently prepared initial state is the complete
40-bit product golden raw record and a blank five-bit label. Both this
state and each complete target have norm one. Their old-record defect is

    Delta=2ap-chi_target
         =2ap*q^3/(1+q+q^2+q^3)>0.

The literal p0 corollary proves positivity, rather than inserting Delta
as a free source, angle or selector. Approximate decimal diagnostics are
chi_initial=0.9717365435, chi_target=0.8985752072,
Delta=0.0731613363. Exact symbolic identities own the result.
Starting directly with eta would remove this defect by changing the
initial preparation. It is not the declared experiment. Likewise the
unfiltered raw target is a valid zero-defect control, not this target.

## 4. There is a full-state floor, independent of program or record size

An orthogonal flip has norm one. For unit x,y,

    |chi_X(x)-chi_X(y)| <= 2*||x-y||.

Consequently every complete commuting preparation from the declared
initial state to any actual scene target obeys

    ||U x_initial-t_v|| >= Delta/2 > 0.

The bound is kernel proved on the actual complete 2^45 carrier. It holds
for every word length, not a bounded enumeration. No sequence of such
words converges to the target.

The extension statement is also generic. Let J:E->F be a complete linear
isometry, with S J=J X, and let U on F be an isometry commuting with S.
The initial and target states are Jx and Jt, with all additional records
retained. Inner products and the same charge are preserved, so

    ||U Jx-Jt|| >= Delta/2.

This applies to normalized fresh ancillary records and the earlier
whole golden cylinder inclusions. The floor cannot be diluted by
increasing carrier size. It does not cover resetting, tracing out,
changing the old observable, or changing the prepared initial state.
Those are different experiments and retain their own scope obligations.

X is used as a mathematical norm witness. This packet does not declare
it an independently physically admitted detector or a gravitational
observable. The complete-state obstruction does not require such a
promotion.

## 5. The missing actuation has a quantitative test

For a complete isometry U and unit input x,

    |chi_X(Ux)-chi_X(x)| <= ||[X,U]||.

If ||Ux-t||<=epsilon and the target changes the same archive charge by
Delta, then

    ||[X,U]|| >= Delta-2epsilon.

These statements are kernel proved. Faithful extensions use the
transported old probe. A programme attaining the previous vanishing
error cannot be admitted by the one-way generators alone: it needs an
operation with genuine old-record actuation, with a commutator that
remains nonzero in the small-error limit.

The actual retained first-unequal routing used by the preparation already
breaks the old last-bit flip. A concrete complete input is all four pairs
11 and a blank label. Toggling the last bit before routing changes the
label to true; routing first and then toggling keeps it false. The
inequality is kernel checked. The broader addressed G/CNOT compiler
includes operations that can break the invariant; its conditional result
is not contradicted by this restricted-class obstruction.

## 6. Validation and scope

The standalone capsule prints 62 new actual propositions and their
transitive axiom lists. The pinned earlier preparation/calibration/
compiler bodies are inputs, not new propositions. The checker binds the
actual p0 gate, fullStep, raw pair masses, all raw cross sums, first-odd
route witness, complete tensor target and state-norm floor. It checks
scientific negative controls as well as ledger and scope freshness.

All 296 exact controls pass. The actual checker rejects all 22 false-scope
and 13 false-exact ledgers. The complete standalone capsule has compiler
exit zero; only Classical.choice, Quot.sound and propext occur in its
transitive axiom union, with several elementary propositions requiring no
axioms. Twelve D0 source pins, toolchain and prior packet pins are verified.

This class has a quantitative preparation obstruction. Neither an M1
failure of the entire D0 core nor a new physical no-go is concluded.
Decoder/admission of two-way or coherent old-record actuation, native
budget and the full-word internal schedule remain required. The first
G0b task is now a concrete operator arrow with a nonzero-defect test,
rather than an unspecified demand for more accurate compilation.

After that admission, the same independently owned joint Delta/P/U,
complete variations and condensed refinement must retain the 653
complementary histories and both thermal-memory source defects. Own
metric/matter source and Ward, quantitative metric contrast, native
stationarity, curved joint roots, soundness/recovery and physical
constraints remain required. G0b/G0, GR/global closure, original #310
fixed-source/raw-owner and independent #202/#317 terminals remain open.
No action, selector, temperature, coupling/source prescription or physical
postulate is introduced.
