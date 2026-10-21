# Paid rational resource writer: coherent failures, protected RIGHT, and finite source limits

Date: 2026-10-21. Existing scientific owner: Draft #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive/native-programme-v1.
Read snapshot: b60a111b43f723a841d253b1d5bd9650c46b2cf8.
Status: author-proved finite construction and bounded author checks. Independent
mathematical review and repository CI have not been performed. GR_closed=false.

## 0. Exact consumer and what this does not assume

The fixed-processor theorem starts with supplied programme and material banks.
It proves stationarity of their DOWNSTREAM processing source on a product of
independently variable complete resources, but does not supply their creation
from blanks or their preparation price. This note constructs a finite writer
for RATIONAL ORTHOGONAL approximants of those resources and computes its entire
counted-cost/CQ-entropy price in the same explicitly declared gate interface.
It is not an implementation of the rejected nonunitary full128 cost tilt.

The interface is the owned addressed Golden/CNOT grammar with computational
measurements, finite feedforward, fresh blanks and paid fair/known-one banks.
Exact H and Toffoli are the owned finite, heralded Golden factories. Their
complete transcript laws are independent of the data, including external
entanglement. All their aborts, quantum work, clock and reference registers
are retained. Actual routing/reading/storage charges must obey the owned fixed
charged-circuit interface. A state- or code-dependent additional charge has its
own source and is not declared zero by the construction.

The conclusions concern executable WORD FAMILIES and, separately, an explicitly
recorded finite selector realization. They do not identify different controller
programmes with one unchanged complete initial controller. They do not provide
an exact continuously parameterized finite-word writer, a physical policy
selecting its words, or the compulsory Book03 valuation. Section 9 retains this
important distinction; the finite-difference theorem is NOT an exact finite
Euler theorem or a proof of the original raw216 limit.

Consumed sources (no reproof of their older results):

1. `A4D_FIXED_PROCESSOR_JOINT_RESOURCE_SOURCE_2026_10_21.md`, blob
   `91ecd208b346665f38f268d2e39d7dd16b57cab6`: fixed paid processor,
   shared-address programme state, normal first sources and transitive banks.
2. `sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/GOLDEN_EXACT_DETECTOR.md`,
   blob `92b9003d783c24b1883a2a21f8b30625078afff7`: addressed gate factories,
   their complete state-independent transcripts, exact logical actions,
   pure-conditional CQ convention, and real primitive charges.
3. `A4D_NEXT_COMMON_MAP_CONSTRUCTION_GATE_2026_10_21.md`, blob
   `c5f4471d91e28fc1483a22c55f2cf1f1bb62192a`: same-execution writer,
   information, control/admission and full-price obligations.
4. `D0_GR_PRIMARY_POSITIVE_CASE.md`, blob
   `99d35958a4cd46646e151b0c25b8f042f73e6f78`: the already constructed
   configured all16+24+2 nonvacuum family and its retained limitations.
5. The supplied `D0_native_absolute_completion_2026-10-21` packet: the
   full128 normalization filter can steer RIGHT and change the full HJR
   source. We do not rerun it or identify its price with the writer below.

Comparator-based amplitude loading is established quantum-algorithm machinery,
not an invention claimed here: Sanders, Low, Scherer, Berry, *Black-Box Quantum
State Preparation without Arithmetic*, Phys. Rev. Lett. 122, 020502 (2019),
arXiv:1807.03206. The elementary construction is proved below without an oracle
assumption. The present application is its paid finite Golden realization,
common-denominator success law, protected RIGHT, and its scope-correct source
composition with the existing D0 processor.

## 1. Writing classical coefficients without a target-dependent gate inventory

Let c be a paid known-one wire, a a scratch wire, and b a zero table wire.
Set A=CNOT(c,a), B=CNOT(a,b). On ALL eight columns,

    chronological A A B B = I,
    chronological A B A B = CNOT(c,b).

For c=1 these write, respectively, 0 and 1 into b while restoring a and
preserving c. Both execute exactly the same two A and two B instructions on
the same addressed wires. Thus any fixed-width signed integer table can be
written by four charged CNOTs per bit, without a free variable-angle gate.
The word order is retained. Equal inventory does not imply equal Book memory
amplitude or feedback; section 9 gives a concrete control.

The finite table can be obtained by a finite classical compiler. Its actual
computation and storage are not free. For a finite code set one may compute
ALL tables and their common denominator in a common prefix, retaining the
work and padding to a fixed finite bound. The proof below keeps this common
prefix's charge. It neither postulates an unpriced real-number oracle nor
proves that D0 must select the code set or controller.

## 2. Literal coherent writer for an arbitrary rational orthogonal block

Let d=2^q>=2 and let U_a be real d-by-d orthogonal matrices, controlled by a
possibly coherent address a. Fix one positive integer R such that

    n_(a,i,j)=R (U_a)_(i,j) is an integer for every a,i,j.

Choose B=2^b>=R minimally; hence R/B is in (1/2,1], except the harmless
R=1 case which also satisfies the same lower bound. Store signed n in a
fixed b+2 bit width. No measurement of the address is performed.

Use registers J (input index), I (fresh output index), L (b uniform bits),
a comparison flag f, the integer table, and reversible scratch. Starting
from arbitrary input psi_J, possibly entangled with all protected references:

1. Prepare I and L uniformly by the exact logical H factories.
2. Coherently look up n_(a,i,j). Compute f=[L<|n_(a,i,j)|]. Apply phase -1
   iff f=1 and n_(a,i,j)<0. Uncompute only the lookup/comparator scratch;
   the comparison flag and the integer table remain.
3. Apply H to L and J. Copy the aggregate predicate
   `J=0, L=0, f=1` into ONE final herald flag. Only that flag is read.
4. On success route I to the designated data output using paid swaps.
   On failure retain every data/work/reference register. In particular,
   do not read the individual failed J,L,f values as additional classical
   records. They remain coherent quantum work.

For fixed a,i,j, projection of L back to its uniform state gives exactly
n_(a,i,j)/B. Preparing I uniformly and projecting J onto its uniform state
supply two factors 1/sqrt(d). Therefore the successful Kraus block is

    K_s = c U,                  c=R/(d B),
    U = direct_sum_a U_a.                                      (1)

Every operation before the final herald is unitary on the full work space,
so its full isometry V satisfies V*V=I. Consequently

    K_s* K_s = s I,       V_f* V_f = (1-s) I,
    s=c^2,               1/(4 d^2) < s <= 1/d^2.               (2)

Here V_f is the entire COHERENT failure map, not one selected failed outcome.
All addresses remain. The local dimension d, not the number of addresses,
appears in (2). The address controls a lookup; it is not uniformly projected
away. This distinction prevents a spurious success factor 1/A^2.

There is no primitive comparator or lookup oracle hidden in this description.
Equality to one fixed index is a reversible AND chain. For each table row,
compute that equality, XOR each stored value bit into an accumulator controlled
by the equality, and uncompute the equality. Enumerating all rows gives a fixed
finite Toffoli/CNOT circuit regardless of their values. A comparator uses
high-to-low equality bits and the mutually exclusive predicates
`higher bits equal AND threshold_bit=1 AND L_bit=0`; scratch is uncomputed.
The sign phase is an ordinary CZ assembled from the owned H/CNOT gates.
The logical gate count is polynomial in the finite table size and bit width.
It is not claimed optimal or small.

The native implementation replaces every logical H/Toffoli by its original
finite Golden factory. It performs the aggregate comparison measurement only
if all those factories complete. Each factory transcript has data-independent
probability. Its abort keeps pure joint work and all failure records. Thus the
complete flag law is identical for all orthogonal tables with the SAME R,d,b
and charged logical circuit. The literal successful action (1) is multiplied
by the already computed factory amplitude for that transcript.

## 3. Protected RIGHT is preserved even conditional on failure

For an arbitrary purification matrix C and arbitrary external RIGHT, the
unnormalized RIGHT matrices on the two coarse writer branches are

    C* K_s* K_s C = s C*C,
    C* V_f* V_f C = (1-s) C*C.                                (3)

After dividing by their actual probabilities, BOTH branches have exactly
the original RIGHT state. The statement covers all its coherences and every
column. It holds for an arbitrary input, not only a selected preparation.
Each state-independent factory transcript has the same property.

This is the relevant contrast with the previous nonunitary normalization
candidate: an effect N which is not scalar need not preserve RIGHT under
conditioning. Here scalarity follows from exact rational orthogonality before
normalization. There is no inverse N^(1/2) filter, erased rejection, or new
normalization chosen to fit a source.

## 4. Exact complete preparation price in the owned CQ interface

Keep the entire quantum work and its purifiers. Conditional on a full measured
factory/herald transcript it is pure. The table for a specified code is a
retained computational-basis record; it is not an entropy-bearing random
variable within that conditional experiment. Different code choices are
handled separately in section 9.

All factory transcript probabilities are common. On every completed logical
writer branch the final probabilities are s,1-s by (2). Expected charged
instruction count is also common: the table bit words have identical addressed
inventories, lookup and comparison circuits are fixed, and factory stopping
laws are common. Thus, for the stated fixed cost table and CQ entropy,

    P_write = E C_write - H_phi(factory transcript, final herald)

is exactly the same for every table in the declared common-denominator finite
code set. It is a real paid value. Nothing is subtracted from the full physical
bill. Equality is not inferred from a successful subensemble alone.

If failure work is additionally measured, its fine classical probabilities
can depend on U and the conclusion need not hold. If a cost depends on input
state, integer value, or ordered memory in addition to the specified ledger,
that cost has not been proved common. The construction therefore does NOT
prove that Book03 Info is CQ entropy or that its entire action is constant.

## 5. Supply of the original processor's program and material banks

### 5.1 Programs

For the original full32 Julia blocks J_a(y), first prepare the fixed address
uniform state and an EPR pair of dimension32 by the paid logical factories.
Apply the addressed writer with d=32 to one half of that EPR pair. On success
its exact state is

    Omega_hat = (32 A)^(-1/2) sum_(a,i) |a,i> U_a |i>,          (4)

where U_a is the chosen rational orthogonal approximant to J_a. Shared
coframe/link addresses are deduplicated exactly as in the parent. All uses of
a shared block use the same table entry. No inverse of an unknown J_a and no
arbitrary continuously variable physical gate is called.

At a fixed strict real chart, rational orthogonal matrices are dense. A direct
proof uses Givens plane rotations with rational unit-circle coordinates
`cos t=(1-r^2)/(1+r^2), sin t=2r/(1+r^2)` and rational r. On a neighborhood of a
rational base J_0 one may instead round the skew Cayley coordinate of
`J J_0^T`, then apply `(I-A)^(-1)(I+A)J_0` by CLASSICAL rational arithmetic.
The inverse is used to compute a finite integer table, not as a quantum oracle.
All approximants are orthogonal exactly. Their approximation errors are
separate numerical/analytical estimates, not exact equality to arbitrary J.

For a finite set of chart points and addresses, clear all denominators with
one R. This does not alter any U_a and makes s common across the entire set.
Changing precision changes the finite computation, bit width and total price;
it does not license ignoring those costs when comparing precisions.

### 5.2 Material and reference

The actual material resource has fixed RIGHT Gram I_128/128. On the original
strict local preparation chart, a LEFT orthogonal rotation of the full16 CAR
space at each site maps the common material seed to the target normalized
material vector. For unit real vectors v,w with v dot w>-1, one explicit map is

    K=w v^T-v w^T,       O=I+K+K^2/(1+v dot w),       Ov=w.

It acts as identity on the orthogonal complement of their span. It does not
remove unused CAR components from the instrument. Approximate the site's
full O by rational orthogonal U_x and use the addressed writer with local
d=16. Site superpositions remain coherent. The complete Fourier128/reference
matrix is multiplied on LEFT only; its RIGHT Gram remains exact even when
the material target is only approximated. No unknown state is cloned.

The common initial seed/reference preparation must itself be given or created
by a separately specified, paid, field-independent prefix. When it is not
part of the owned initial boundary, its cost and feasibility remain an input;
the present theorem does not declare it free. Fresh copies used for retries
are independently prepared known resources with their own retained purifiers,
not repeated fresh copies of an arbitrary unknown external state.

### 5.3 Finite banks and signal

Execute L attempts for each required known resource, INCLUDING after a success.
Keep every failure. Choose a first successful output by paid controlled routing,
retaining the success index and all original purifier registers. That index
is not removed by a mathematical renaming of references.

The owned finite factory caps can be raised so each complete attempt has
factory readiness at least1/2: there are finitely many logical gates and their
failure tails are geometric. Every enlarged cap is charged. Hence each trial
has success at least1/(8d^2). For M resources, local dimension at most d_max,

    L >= ceil(8 d_max^2 log(2M))

makes the probability eta of the complete bank at least1/2 by the union bound.
Eta is common across the finite code set because every transcript law is.
This is an existence/resource bound, not a claim of low runtime. No physical
copy reservoir, selection of caps, or raw216-uniform complexity is inferred.

## 6. Same-programme price composition, with its exact interpretation

For a SPECIFIED finite code, append the existing fixed processor to the bank.
Writer failures have an actual fixed abort continuation. On bank readiness,
use the exact supplied rational resources (4) and their material counterparts.
All unused/failing resources remain as pure conditional spectator work. The
quantum-CQ entropy chain rule and the actual charged ledger give

    S_code = B_write + eta Phi(resource_hat_code),             (5)

where Phi is the parent's COMPLETE downstream processing price on its declared
CQ interface. B_write includes every prefix, aborted bank and routing charge;
it is common across the padded code set. Readiness eta is also common. This
is not equality of Book03 actions and not a retroactive price subtraction.
Additional actual information or charge terms are added with their own jets.

At ideal program and material resources chi(y), the parent proves
`D Phi(chi(y0))=0` on the declared product resource manifold at its existing
primary root, and transports the existing field first/second jet. We consume
that theorem. We do not claim a new exact finite root at arbitrary rational
approximants, and we do not extend product-resource stationarity to arbitrary
entangling variations of the entire bank.

## 7. Controlled finite source limits; not a fictitious derivative of words

A finite word code is discrete. There is no claim that code(y) is a smooth
map into a finite set or that a fixed word has a nonzero field derivative.
Instead fix a finite symmetric stencil about an admitted ideal chart point
and construct all its resources to norm error at most epsilon, with one R and
one charged inventory. Equation (5) supplies its actual conditional programme
prices, from which finite differences can be taken. A statistical estimate
of these prices has an additional sampling cost, not included in a symbolic
finite-difference identity.

For the sharper stationary estimate, use local product-manifold coordinates
near chi0=chi(y0). Suppose the real downstream price Phi is C2 there with
bounded Hessian H, D Phi(chi0)=0, and ||chi(y)-chi0||<=K||y-y0||. If
||chi_hat-chi||<=epsilon at a stencil point, integration of the gradient gives

    |Phi(chi_hat)-Phi(chi)|
       <= H [K ||y-y0|| epsilon + epsilon^2/2].                (6)

Constants absorb an equivalent local chart norm. For a C4 ideal field price,
central first and second differences of the ACTUAL prices (5), divided by
the RECORDED eta, differ from the ideal derivatives by

    first:   O(delta^2 + epsilon + epsilon^2/delta),
    second:  O(delta^2 + epsilon/delta + epsilon^2/delta^2).    (7)

Thus epsilon=O(delta^3) gives second-order convergence of both finite jets.
The proof is the ordinary central-difference Taylor remainder plus (6).
At a nonstationary test point the safe value bound is O(epsilon), so use
`epsilon=o(delta^2)` for a Hessian limit; the included native numerical test
uses a finer delta^-5 coefficient rounding schedule.

If dark outcome births prevent a bounded Hessian, do not use (6)-(7). For a
fixed finite CQ output dimension, entropy continuity instead gives a bound
`O(epsilon log(D_out/epsilon))` on values, with the true ledger bound retained.
Taking epsilon sufficiently small still controls a specified finite stencil,
but does not establish an improved C2 theorem or a refinement-uniform estimate.

These are limits in PREPARATION PRECISION and STENCIL SPACING at a fixed mesh.
To infer a physical continuum source one must additionally control the original
mesh norm, physical field writer, source gain, collars and Book residual.
If the parent's source coefficient is small, errors must also be divided by
that actual coefficient. The lower bound on eta removes only the NEW writer
readiness loss. It does not normalize away the old processor gain.

## 8. Bounded decisive tests actually run

The accompanying Python program verifies:

- both literal four-CNOT bit words on all columns, not only the prepared bit;
- every row of two complete 1024-by-2 coherent writer isometries, with common
  denominator65 and B128, exact success4225/65536, all failure effects and a
  nondiagonal RIGHT density;
- a 128-column exact RIGHT Gram instance (the general proof already tensors
  arbitrary RIGHT); this is not a full-site spectral replay;
- a hostile nonunitary target and additional fine measurement of failure work;
- literal CAR16 generators in the existing ACDB order, a genuine proper-link
  boost and its full32 Julia matrix, exactly orthogonal rational approximants;
- a nonzero native coefficient-report first and second source after the
  prepared program is consumed by a Bell processor, with the actual writer
  and Bell gains retained;
- a separate exact polynomial control of the stationarity-assisted estimate
  and the surviving effect of an extra moving upstream price.

The native source test is deliberately narrow: for X=(3/5) C_1 exp(theta Gamma)
with Gamma the original01 boost lift, the coefficient-zero report on a trace
CAR input has probability r=9 cosh(theta)^2/50. Its exact probability is not
the full parent GR detector. We test its nonzero information-source transport,
not the all42 proof again. Wrong Bell labels and writer failures use a paid
fair report in this diagnostic and stay present. All matrix-orthogonality and
writer-completeness equalities are exact; floating log/approximation checks
have stated tolerances and are diagnostics, not interval certificates.

## 9. Controller, full memory and physical-selection boundary

There are two different legitimate uses of the finite code set:

(A) separately specified executable words, each starting from the same quantum
blank/reference template, with its complete controller/word description priced;
(B) ONE fixed controller which generates or reads a finite selector label,
retains it, and coherently executes a reversible table-lookup circuit.

For (B), the selector must be actually generated and paid. If it is uniform
with N labels and every conditional programme has (5), the full CQ price is

    S_all = B_selector - log_phi(N)
             + (1/N) sum_code S_code,                         (8)

with the real convention for costs already kept. It is NOT any one S_code.
Conditioning on the selector does not prove a physical field-stationarity law.
An initially supplied differing controller tape is not a common COMPLETE
initial state. These facts are not solved by equal gate counts.

The construction therefore supplies concrete finite native-gate resource
preparations and their conditional counted-CQ price, not the compulsory
field-to-programme dynamics from one physical initial state. The tables are
finite derived data of an explicit compiler, not a new continuum gate or a
price chosen to give Einstein. Their use as physical D0 field codes and the
law selecting them are still separate obligations.

Finally, identical counted inventories do not force identical Book action.
The four-CNOT zero/one words above already supply a control: on a fixed
known-one/blank input corner, their return amplitudes are1 and0, respectively.
Their true complement feedback values are0 and -log(1-z), despite equal
counted cost and pure final states. Thus neither (4) nor (5) proves the
compulsory Book03/Info/memory valuation. Its full same-execution residual
must still be computed; no unproved scalar anchor is introduced.

## 10. Precise substitution and remaining work

The mathematical availability of finitely encoded program/material resources
can now be supplied by an explicit all-outcome Golden-gate writer, instead of
an arbitrary variable-angle state-preparation oracle. Within the declared
fixed-cost/CQ interface, its preparation charge is exactly common across a
padded finite code set, it preserves protected RIGHT even upon rejection, and
its finite price jets converge to the existing processor's jets with the
explicit true gains in (7). These statements remove a particular resource
realization and pricing premise in that conditional model.

They do NOT close native selection, a common continuously varying physical
controller/initial-state map, literal Book03 valuation, independent extra
upstream operators, exact finite GR stationarity of the approximants, or the
original uniform raw216 refinement. No task, lifecycle, main acceptance or
physical closure is promoted. The published parent remains Draft.
