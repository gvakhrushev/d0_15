# Exact native detector, complete information, and the compulsory Q8 comparison

Bounded read-only synthesis for the existing PR #334, 20 October 2026.
Input head: 29ee8a1b0d669f0a93d0933c0c063612bee6eae6.
Phase: native realization and same-execution price composition. No new task,
physical action, primitive admission, or publication is claimed.

The new exact detector removes a real implementation premise. Its finite
Golden/CNOT instruments implement the required Boolean logic exactly on
completed branches, with data-independent finite-cap aborts and all work
retained. The useful further conclusions are:

1. A complete data-independent compiler preserves the information about
   unknown input data, although its transcript adds entropy. This gives an
   exact distinction between the declared CQ price and task information.
2. The new native X measurement, composed with the already paid fair
   preparation, solves the original relative-sign Q8 comparison exactly
   on every completed transcript. This construction has no moving
   geometric query and therefore has zero geometric source.
3. A data-independent pre-comparison abort compiler also preserves the
   nonzero source of the separately owned Q8/full-J2 interface, when that
   interface is actually required. The complete stopped MI inequality
   survives, with an explicit nonzero coefficient.

The second and third statements distinguish two actual task bindings.
Perfectly implementing a Q8 sign question does not establish that the
full-J2 query belongs to that question.

## 1. Exact input ownership and the premises now closed

All paths below are inside
02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/.

| Input | Git blob at the input head |
|---|---|
| GOLDEN_EXACT_DETECTOR.md | 92b9003d783c24b1883a2a21f8b30625078afff7 |
| GOLDEN_EXACT_DETECTOR_REVIEW.md | 0452d757fb054267f114d1e3cf77d64c7fa57542 |
| TWO_NATIVE_8D_DETERMINANT_SOURCE.md | 85e9d19012d543873269e3584b6ec2763b868637 |
| DETERMINANT_PREPARATION_BANK.md | e7b92fae0d6f3dc3e60499f0dd041c18003da872 |
| FIXED_CLOCK_PREPARATION_BANK.md | b36d96cf1698ecafd2319ac697f3c8fa2bedefc2 |
| Q8_CONDITIONAL_INFO_SOURCE.md | 6abac8f8dd05cc31badcb37aae233090ad61080a |
| MINIMAL_GOLDEN_COMPLETE_SOURCE.md | bce112de77a694809e0a9a7fa769731296148ca2 |

The first two files are consumed at their independently accepted scope;
the parity, Kraus, Boolean and Toffoli checks are not repeated here.

The supplied exact detector closes the coherent AND/OR/Toffoli assumption
within the addressed Golden/CNOT, fresh-reading and measured-feedforward
interface. Its successful H transfer is exact, and its finite aborts have
an explicitly retained law. The paid bank supplies its 128N known fair
resources and the preserved computational-one echo control. These facts
replace supplied fixed H/Toffoli and fair-state resources; they do not
provide a deterministic no-abort compiler or a moving field gate from a
fixed gate palette.

The new total price is the actual capped one:

\[
\mathcal S_{\rm CQ}
 =S_{\rm pre}+\alpha[\kappa-\beta h_\varphi(q)]E_N(\beta q),
\quad
E_N(x)=\sum_{j=0}^{N-1}x^j.
\tag{1}
\]

Here the fixed chart supplies
\(\alpha\ge1/2\), \(\beta>1/2\), \(\kappa>53\), and
\(q=1-(1-zA)(1-zB)\), \(z=2^{-20}\).
The owned exact source is
\(D\mathcal S_{\rm CQ}=\alpha c_NDJ_2\), \(\alpha c_N>6\).
This is not the old deterministic integer-stage price.

Physical addressability, blanks, readout/feedforward, the moving original
8D query and its matter input, the complete Book03 valuation, and
independently variable upstream preparations remain explicit inputs.
In particular the price of additional moving physical terms is not
included by calling them gate work.

### 1.1 Fixed preparation time for the actual 128N bank

The already reviewed fixed-duration bank is parametrized by the number
of resources. Apply the same all-trials/reverse-routing schedule with
\(m=128N\): there are \(N\) minus query inputs and \(127N\) plus resources.
The first plus supplies the known-one control. With K slots per resource,
the literal schedule has

\[
\#G=256NK,\qquad
\#\mathrm{CNOT}=(770N+3)K,\qquad
\#\mathrm{parity\ reads}=128NK,\qquad
\#\mathrm{report\ symbols}=256NK.
\tag{2}
\]

Indeed the general CNOT inventory is
\((6m+2n_-+3)K\), where \(n_-=N\). This includes actual dummy routing,
the inverse echoes and seed-control routing. Controller, storage and
measurement charges remain additional paid terms.

Readiness is still
\(\alpha=(1-(1-2p^3)^K)^{128N}\), \(p=\varphi^{-1}\);
all preparation transcripts and unused resources remain present.
Under the owned equal-duration addressing/controller interface,
every ready branch launches its first query at the same operational
clock position. This closes random preparation delay for this enlarged
bank. It does not fix random detector-retry delays, global sequential
sampling, or the map from operational time to physical \(u\).

## 2. A complete data-independent compiler is information-preserving

Let D be arbitrary input data, possibly entangled with a protected reference
R. For each full internal transcript t, include every unmeasured output,
old slot, archive and abort work in its output space. The exact detector's
data-independent probability assertion means

\[
K_t^\dagger K_t=w_t I_D,\qquad
w_t\ge0,\qquad \sum_t w_t=1.
\tag{3}
\]

Discard zero-probability labels. Then
\(V_t=K_t/\sqrt{w_t}\) is an isometry. The complete flagged channel is

\[
\mathcal E(\rho_D)
 =\bigoplus_t w_t V_t\rho_DV_t^\dagger.
\tag{4}
\]

This applies to failures and aborts as well as successes. An abort need
not restore the input to its initial location: retaining the entire
conditional pure operation is enough. In the H gadget, for example,
abort after a successful CZ retains the entangled input/resource pair.

For any finite input state,

\[
S_\varphi(\mathcal E(\rho_D))
 =H_\varphi(w)+S_\varphi(\rho_D).
\tag{5}
\]

For every fixed cq ensemble \(XDR\), including noncommuting conditional
states on R,

\[
\boxed{
I_\varphi(X:\mathcal E(D)\mid R)
 =I_\varphi(X:D\mid R).
}
\tag{6}
\]

Both identities follow directly from the entropy formula for orthogonal
blocks: each block is an isometric copy of its input, and the classical
weights are independent of X and R. Equivalently, the flagged channel has
a mathematical recovery channel applying \(V_t^\dagger\) on the
corresponding image, with an arbitrary trace-preserving extension on
unused output subspaces. This does not claim a free physical inverse.

The identities compose through adaptive circuits. Each completed
transcript has a product of data-independent probabilities and a
composition of isometries. The prefix that ends at a finite abort has
the same property. No outcome is renormalized away.

**Price consequence.** The retry transcript entropy \(H_\varphi(w)\)
is a real increase of the complete CQ entropy. It is not information
newly learned about X. The compiler's internal labels have zero
conditional information about X at each reached node, and its complete
quantum record preserves the input information by (6). Consequently
subtracting this entropy in \(\kappa=EC-H_\varphi(T)\) and subtracting
actual conditional information about X define distinct objectives.
Their distinction is exact on the same physical implementation.

The detector's final measured report is not covered by (3): its
probabilities deliberately depend on the query data. Its pinching and
its place in the actual task must be evaluated separately. Equation (6)
does not silently promote the final pointer entropy into Book03 Info.

## 3. Exact native solution of the original Q8 sign question

Use the already owned matched Q8 comparison. On the coherent comparison
port it supplies the relative alternatives \(I\) and \(Z\), possibly
times one common quaternion operation on held logical data. That
common operation is retained and does not depend on which sign is
present. The new fair bank prepares the port in \(|+\rangle\).
Thus the actual two hypotheses give

\[
I|+\rangle=|+\rangle,\qquad
Z|+\rangle=|-\rangle.
\tag{7}
\]

They are orthogonal. This uses a paid fair resource, not an assumed
Hadamard primitive or a copied unknown state.

Consume the exact X-cycle from the new detector. Put
\(s=4p^3\), \(r=p^6\), so \(s+r=1\). Its full cycle has Kraus maps

\[
K_+=\sqrt{s}\,P_+,\qquad
K_-=-\sqrt{s}\,P_-,\qquad
K_f=\sqrt r\,I,\qquad K_{\rm impossible}=0.
\tag{8}
\]

The actual retained success labels are respectively (1,0) and (0,1);
the failure label is (0,0). Both weak tests are always executed.
There are eight expanded gate ticks per cycle before actual reading,
reporting, routing and controller charges. Each success label identifies
the sign exactly. Each failure leaves either sign state unchanged.

With at most L cycles, the certified success probability is
\(\eta=1-r^L\), independent of X, and the cap abort has probability
\(r^L\). On abort the orthogonal port state remains retained. Let
\(\alpha\) be the readiness probability of the paid fair preparation.
The complete programme therefore has

\[
\Pr(\text{registered correct sign})=\alpha\eta,\qquad
\Pr(\text{unresolved})=1-\alpha\eta,\qquad
\Pr(\text{wrong registered sign})=0.
\tag{9}
\]

The unknown-sign Q8 query is not executed after preparation abort.
Every quantum input and work register is retained on every later failure.
Every prescribed positive unresolved tolerance can be met by finite K,L.
No deterministic no-abort claim is made. A task requiring a decision on
every execution would need to count or resolve the aborts.

### 3.1 Full oldRIGHT and both actual information cuts

Let the old task data be any fixed cq state
\(\rho_{XR}=\sum_x\pi_x|x\rangle\langle x|\otimes\rho_R^x\).
Include all previously available logical information in R. Let Y denote
the entire newly registered classical transcript, and A all retained
fresh quantum work, including the comparison port on abort.
All preparation and retry times have laws independent of X.
If X is already perfectly available in R, then \(H(X\mid R)=0\);
these formulas do not force an additional comparison in that case.

For the purely registered transcript, the output is an erasure channel
which reveals X with probability \(\alpha\eta\). Therefore

\[
I_\varphi(X:Y\mid R)=\alpha\eta\,H_\varphi(X\mid R).
\tag{10}
\]

For the complete newly retained quantum record, the ready comparison
port already carries orthogonal X states. The X-cycle never destroys
that distinction, including on its failure and cap-abort outputs.
Hence the full oldRIGHT-preserving identity is

\[
\boxed{
I_\varphi(X:YA\mid R)=\alpha\,H_\varphi(X\mid R).
}
\tag{11}
\]

Thus the finite X-readout cap affects the availability of an actually
registered certificate, but not the complete quantum information of
a ready comparison. This is why replacing a full quantum work cut by
its registered pointer requires an explicit task/algebra statement.

For the declared uniform cycle prices, let \(C_{\rm pre}\) be the
complete expected preparation cost, \(C_{\rm pair}\) the actual matched
Q8 comparison cost, and \(\mu\) the entire expected cost of one reached
X-cycle. Then

\[
EC_{\rm total}
 =C_{\rm pre}+\alpha\left[C_{\rm pair}+\mu E_L(r)\right].
\tag{12}
\]

This counts both weak tests, all reached failed cycles, finite aborts
and reporting. If actual addresses give sign-dependent costs, replace
the bracket by their fixed prior average; none is silently free.
The native bit-report price \(1+b\) is compatible with (12): the two
success labels each contain one zero and one one, and failure contains
two zeros. All such charges remain actual constants in the fixed task.

The entire programme uses fixed Golden gates, the fixed Q8 words and
fixed task data. It does not invoke \(U(E,b)\), the determinant detector,
the scalarizer W, or any moving coframe/matter query. Consequently

\[
D_y\left(EC_{\rm total}
   -I_\varphi(X:Y\mid R)\right)=0,\qquad
D_y\left(EC_{\rm total}
   -I_\varphi(X:YA\mid R)\right)=0.
\tag{13}
\]

More generally any well-defined valuation depending only on this held
record has zero geometric/matter source. Moving initial priors,
physical durations or separately priced upstream fields would be
additional inputs, not exceptions hidden in (13).

This is a constructive native competitor for the original Q8 sign
task, now with exact registered answers on every completed history.
It is not a simulator of a prescribed continuous geometric query.
The two distinctions must not be identified.

## 4. Positive transport of the owned full-J2 Q8 source through finite aborts

The source-preserving interface remains useful when the actual task
requires it. The following composition consumes the owned clean
first-jet construction and the data-independent compiler structure.

Assume that before each Q8 comparison an actual finite prefix:

* has a field- and X-independent transcript/cost law;
* completes with probability \(\beta>0\);
* on completion supplies the owned clean full-query first jet
  \(V=|0\rangle J\), \(DV=2|1\rangle J\,Dt\);
* on abort retains all work, before the unknown Q8 sign has interacted
  with this attempt's fresh apparatus, with the held logical input
  and R as spectators and no fresh X-dependent record.

The last condition makes the aborted current work X-independent.
It holds for the owned fresh known trace-probe realization of the
clean query, with all old logical data and oldRIGHT spectators.
It is not automatic for a compiler which aborts after an unknown-sign
measurement. The exact X-abort in Section 3 illustrates that distinction.

Let \(\mu\ge1\) be the actual expected price of this pre-report prefix
per reached attempt. Include every compilation attempt and abort
charge. The native final report, only on completion, costs \(1+b\).
Put \(a=\mu+\beta\), \(q=q_-\), \(s=1-q\), and \(x=\beta s\).
At the owned common-null stratum,

\[
q_+=0,\quad Dq_+=0,\quad
q_-=q_*=4p^3,\quad
Dq_-=8p^{9/2}Dt,\quad Dt=\gamma_hDJ_2.
\tag{14}
\]

Stop after the first bright, the first prefix abort, or N attempted
stages. Under the plus hypothesis a reached stage continues with
probability \(\beta\); under minus it continues with probability x.
The exact expected cost, with \(\pi=\Pr(X=-)>0\), is

\[
C_N(q)
 =(1-\pi)aE_N(\beta)
   +\pi[a+\beta q]E_N(\beta(1-q)).
\tag{15}
\]

The complete retained stopped record, not just its bright/no-bright
flag, is used for information. Write its conditional quantum
oldRIGHT information as \(I_N(q)\).

For \(q_2\ge q_1\), the \(q_1\) record is a channel of the \(q_2\)
record. Keep every no-bright terminal record. On the first bright,
keep that bright with probability \(q_1/q_2\). Otherwise relabel it
dark and simulate the remaining \(q_1\) experiment with the now known
minus hypothesis, including fresh prefix transcripts and finite abort.
Before this first bright, the retained histories agree. Under plus
no bright is possible, so its law is unchanged. Under minus this is
ordinary Bernoulli thinning until the first known-minus event,
followed by the correct conditional continuation. The construction
also retains every actual prefix label in the generated output.
It is a mathematical comparison channel, not a free physical simulator.

Conditional mutual-information data processing therefore gives
\(I_N'(q)\ge0\). The owned clean first-jet factorization handles every
fresh quantum register and newborn zero-probability branch just as in
the reviewed Q8 theorem; the ideal complete-state remainder is
\(O(\|dy\|^2)\), with entropy remainder \(o(\|dy\|)\).

Differentiating (15) gives

\[
C_N'(q)
 =\pi\beta\bigl[E_N(x)-(a+\beta q)E_N'(x)\bigr].
\tag{16}
\]

For \(x\ge0\) and \(N\ge2\), coefficient comparison gives
\(E_N(x)\le(1+x)E_N'(x)\) and \(E_N'(x)\ge1\).
At \(q_*=1-p^6\), the complete score \(S_N=C_N-I_N\) obeys

\[
\boxed{
S_N'(q_*)\le
-\pi\beta\bigl[\mu-1+2\beta q_*\bigr]<0.
}
\tag{17}
\]

For \(\beta=1\), \(\mu=T\), this reduces to the previously reviewed
bound \(-\pi[(T+1)-2p^6]\). A data-independent paid initial bank
of readiness \(\alpha>0\) multiplies the new source by \(\alpha\):

\[
\boxed{
D S_{\rm total}
 =\alpha\,8p^{9/2}\gamma_h S_N'(q_*)DJ_2.
}
\tag{18}
\]

Thus finite heralding and aborts need not destroy the complete
conditional-information source. Equation (18) is an attained source
for a supplied complete implementation satisfying the listed
interface, not a proof that the local determinant apparatus is itself
the coherent clean scalarizer W. Its finite measured success map
cannot be silently substituted for a deterministic unitary oracle
inside W and W-dagger.

The fixed gate parts of an admitted word may be replaced by the
new exact compiler where its palette actually applies. Moving
controlled field queries, complete trace-address preparation and
other operations outside that palette still need their own admission.
No claim that all of MINIMAL_GOLDEN_COMPLETE_SOURCE is now compiled
follows merely from an exact Toffoli.

## 5. What this says about the actual Book action and minimum

The literal Book03 boundary is unchanged: its Info is uncertainty
reduction but does not fix the tested variable, prior, future readout
algebra or the complete chronological functional. The new compiler
does not add that missing definition. It supplies enough exact
structure to compare proposed definitions on one real execution:

* complete compiler CQ entropy gains the independent transcript
  entropy \(H(T)\);
* complete information about unknown data is preserved by (6);
* for the actual Q8 comparison the classical certificate and full
  quantum-work gains are respectively (10) and (11).

These are different finite quantities, even with every oldRIGHT and
work register present. Their equality is not a consequence of
chronological retention or of a minimum-description principle.

The exact Q8 programme in Section 3 is a completed constructive
application of the new native instrument. Its presence prevents
deriving a continuous Einstein source merely from requiring that
sign question to be answerable. A true continuous-profile task could
exclude it: for example a replacement required to preserve both
original probabilities A(E,b), B(E,b) on a field neighbourhood cannot
use a field-independent sign-only programme. That is a different,
explicit future-test contract, not a condition obtained from the
present Golden gate identities.

Even such a profile does not, by itself, choose the final measurement
cut or the absolute complete price. The source-bearing all42 roots
of (1) are preserved at their declared scope. Establishing that a
physical optimum attains this monitored programme, rather than a
different instrument with the same required future profile, requires
the actual allowed future algebra and value/clock boundary data.
No unrestricted field minimum follows from a first-source identity.

There is therefore one concrete remaining binding: the native
compulsory future task and its full priced information instrument must
be identified with an implementation carrying the moving 8D/full-J2
input, with its actual preparation and clock equations. The present
exact detector closes the measurement compiler, and the explicit
comparisons above show precisely which additional physical selection
it cannot supply by itself.

## 6. Verification scope

This note consumes the already reviewed gate, parity and full-detector
identities. It does not run those checkers again. New claims are the
finite isometry/entropy identities (3)-(6), the literal Q8 application
(7)-(13), and the analytic abort-source transport (15)-(18).
The enlarged fixed bank (2) is direct substitution into the reviewed
general inventory. No historical detector or all42 result is re-certified. This supports
the same existing task; no acceptance registry, lifecycle or GR status
is promoted.


## 7. Current-field actuation consumer

[NATIVE_CAR_ACTUATED_METRIC.md](NATIVE_CAR_ACTUATED_METRIC.md) now supplies
the missing small field actuator from the original K/G record word,
without a new coframe gate. With the supplied LIVE material-query
binding, its future contexts separate the primary H profile at fixed
matter. It consumes the concurrent material-copy information bound
rather than treating an unknown CAR amplitude as free query CODE.
This closes the additional-actuator comparison premise, not Book03's
compulsory task, input mechanism or absolute valuation.
