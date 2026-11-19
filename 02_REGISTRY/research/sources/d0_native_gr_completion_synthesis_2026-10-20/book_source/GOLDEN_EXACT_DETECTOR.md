# Exact Golden detector with retained retries and complete first source

20 October 2026. Existing Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`native-programme-v1`. Phase: native realization.

Consumer: [two original 8D queries](TWO_NATIVE_8D_DETERMINANT_SOURCE.md),
sections 2–3, and the [paid preparation bank](DETERMINANT_PREPARATION_BANK.md).
Input snapshot: `5966f9cedb3ed80a8e7d563ee9731d133cb6b2f6`;
the reviewed preparation application was published at
`946ff6e5bef6658656794fc12aefa3139764569b`.

## 1. Statement, interface and substitution

The remaining coherent Boolean detector can be implemented **exactly on
every successful transcript** by addressed Golden gates, CNOT, computational
measurements, classical feedforward and the already generated fair/known-one
resources. All failed trials, work, clock and a final finite-cap abort remain.
Success and abort probabilities of each gate implementation are independent
of its data, including external entanglement.

The new complete experiment has a different stopping law from the former
fixed-stage verifier. Its actual full CQ price, derived below, is

```text
S_total(y) = S_pre + alpha [kappa - beta h_phi(q(y))] E_N(beta q(y)),
E_N(x) = sum_{j=0}^{N-1} x^j,   q(y) = 1 - exp(-j_b(y)).
```

Here alpha is the paid initial bank readiness, beta is the probability that
all gate implementations in one detector stage finish, and kappa is the
expected complete stage cost minus the entropy of its internal records.
They are field independent on the declared fixed chart. For the explicit
caps and charged native word below, alpha>=1/2, beta>1/2 and kappa>53. On the
original primary family, for every N>=2 and every mesh/multiplicity,

```text
D S_full = alpha c_N DJ2,        alpha c_N > 6.
```

This replaces the **exact coherent AND/OR gate assumption within the declared
addressed interface**, including its complete CQ source application. It
does not merely approximate a gate or condition away unsuccessful executions.
It is not a deterministic no-abort realization of the old task.

The physical admission of addressability, blanks, computational measurements,
feedforward, the moving original 8D queries and their field jets remains
required. Every literal G/CNOT occurrence is charged at least one native
clock unit. All additional reading, routing, storage and controller charges
are included and nonnegative; their law is field independent in this
interface. Cost is measured in those same units and entropy in base phi.
Identifying that declared complete CQ price with compulsory Book03 Info
and the complete physical action remains open.

The original midpoint fields, 16 coframe, 24 link and two matter variations,
fixed cut and source ratio are unchanged. The consuming equality is a first
source identity, not a Hessian, stability, full physical GR or raw216 theorem.
Root owns this proof and its parent application; the bounded checker has a
disjoint write path. The decisive checks are the full Kraus identities,
literal word costs, retained finite renewal law and its nonzero source.

## 2. Controlled phases: identity on failure

Write p=phi^(-1), a=sqrt(p), G=R(theta)=[[a,-p],[p,a]].
The owned known-one resource supplies X through one CNOT and hence
G^(-1)=XGX through three charged letters. No inverse is free.

Let W_0=G on a target t. For k>=1 introduce a fresh control c_k and
define W_k in chronological order by

```text
CX(c_k,t), W_(k-1)^(-1), CX(c_k,t), W_(k-1).
```

Since XGX=G^(-1), W_k is exactly the k-controlled G^(2^k).
If any control is zero it is identity; otherwise its target block is
G^(2^k). This is a full matrix identity. Inverses of words reverse their
letters and invert each G; CNOT is self-inverse.

Set m=2^(k-1). On a fresh target |0>, first apply G^(-m), then W_k,
then measure that target in the computational basis. With
Z_k=I-2|1...1><1...1| on the controls, the two Kraus operators are

```text
K_0 = cos(m theta) I,
K_1 = -sin(m theta) Z_k.
```

Thus outcome zero does nothing to arbitrary data; outcome one applies the
exact controlled phase, up to one transcript-wide sign. Their probabilities
are independent of the data and all its external correlations. For k=2,3:

```text
Z_2 = CZ,     s_2 = sin²(2 theta) = 4p³,
Z_3 = CCZ,    s_3 = sin²(4 theta) = 16p⁹.
```

Repeat after outcome zero, at most L times. Every failure is identity,
success applies the desired gate, and the cap abort is identity with
probability (1-s_k)^L. This is a finite trace-preserving instrument with
retained failure records, not an unbounded postselection prescription.

W_k has 2^k signed G letters and 2^(k+1)-2 CNOTs; half the G letters
have each sign. The initial G^(-m) and every inverse echo give the
following **expanded forward-word** counts per trial:

```text
number of G     = 3 * 2^(k-1),
number of CNOT  = 2^(k+2) - 2.
CZ:  6 G + 14 CNOT = 20 gate ticks, plus reading/other actual charges.
CCZ: 12 G + 30 CNOT = 42 gate ticks, plus reading/other actual charges.
```

The known-one record is preserved by every echo.

If the admitted reading interface measures only a fresh parity flag,
copy the active target's computational bit into a fresh blank by CNOT
and measure that flag. Keep the original target as well. This realizes
the identical Kraus instrument, adds one charged CNOT per reading, and
does not measure an old RIGHT record. The same construction applies to
each ancilla reading below. The counts above are lower bounds before
these additional reading-interface letters.

## 3. Exact X measurement and Hadamard without a new rotation

An X measurement is itself obtained by two weak tests. In each test,
prepare a fresh ancillary G|0>, use it as control in CNOT to the data,
apply G (first test) or G^(-1) (second test) to that ancilla and measure it.
The single-test Kraus operators on the data are

```text
A_0 = p I - p² X,       A_1 = ap (I+X),
B_0 = p I + p² X,       B_1 = -ap (I-X).
```

**Always execute both tests**, including after first-test outcome one.
Their complete cycle is

```text
B_0 A_1 =  ap (I+X),       transcript (1,0),
B_1 A_0 = -ap (I-X),       transcript (0,1),
B_0 A_0 =  p³ I,           transcript (0,0),
B_1 A_1 =  0,              transcript (1,1).
```

The two success effects are 4p³ P_+ and 4p³ P_-, and the failure
effect is p⁶ I; 4p³+p⁶=1. The failure preserves arbitrary entangled
data. Conditional on completion this is the **exact projective X
measurement**, with its actual outcome retained. With at most L cycles,
the unresolved instrument is p^(3L) I and has probability p^(6L).
Each full cycle has four forward G and four CNOT letters after expanding
the inverse echo: eight gate ticks, two measured bits, and all actual
additional charges. Stopping after the first half of a cycle would change
the clock/record law and is not this implementation.

For H, use a supplied |+> resource R and an arbitrary input D:

1. Apply the finite CZ implementation to D,R; abort if it does not finish.
2. Apply the finite X measurement to D; abort if it does not finish.
3. For the minus X outcome apply X to R using the known-one control.
4. Swap D,R by three CNOTs to restore the canonical output location.

On success the output is H|psi>. The two X outcomes have probability
1/2 for every input, including one entangled with an external system.
Indeed their transfer maps before correction are H/sqrt(2) and
XH/sqrt(2). Conditional on either outcome, the measured old input is a
known |+> or |->; the correction and swap retain it as work.
All success/failure histories of this H instrument are therefore
data independent. Its abort retains a pure joint state; it need not
pretend that the input has been restored after successful CZ.

Put b_2=1-(1-s_2)^L and b_3=1-(1-s_3)^L.
An H succeeds with probability b_2². Applying H to a target, CCZ on
two controls and that target, then H to the target gives exact Toffoli.
Its completion probability is b_2^4 b_3. All intermediate records and
any abort remain data independent, including on a coherent superposition
of Boolean inputs. No R(pi/8), exact Walsh primitive, Toffoli primitive
or discarded phase has been introduced.

## 4. The actual two-query detector and finite resource count

Use the parent's fixed original 8D basis. Its retained positions are
0=000 and 2=010; thus its complementary Q predicate is x_2 OR x_0.
An OR into a fresh zero target is two CNOTs and one Toffoli. For each
of the two original queries:

- compute Q in a fresh flag: one Toffoli and two CNOTs;
- compute AND of its twenty distinct |+> efficiency bits using a
  retained chain of nineteen Toffoli scratch outputs;
- compute Q AND that efficiency result into a new flag: one Toffoli.

Define the efficient event to be all twenty bits equal to one, of
probability z=2^-20. This is an explicit event convention on the same
fair coherent resource; it has the parent's effect I-zF. No efficiency
bit or intermediate Boolean flag is measured. Two independent coin
registers are used.

Finally compute the OR of the two flags into the final report bit using
one Toffoli and two CNOTs. The whole detector uses 43 Toffolis and six
additional CNOTs, with every scratch value retained. On completion,
measure **only the final report bit**, besides the data-independent
gate implementation records already described.

There are 86 H resource qubits per stage, in addition to the original
two query inputs and forty efficiency qubits. The same paid preparation
bank therefore supplies M=128N fair signed resources for N possible
stages. Its first plus also supplies the known-one echo control. Generate
them all before queries, with the existing finite cap K chosen so
M(53/100)^K<=1/2. The bank law gives

```text
alpha = (1-(1-2p³)^K)^(128N) >= 1/2.
```

For every detector gate choose L=20. The stage completion probability is

```text
beta = (b_2^4 b_3)^43.
```

The rational inequalities 1-s_2=p⁶<3/50 and
1-s_3=1-16p⁹<4/5, together with

```text
43 [4(3/50)^20 + (4/5)^20] < 1/2,
```

give beta>1/2 by the union bound. Separate banks and complete detectors
are used per actual local b; there is no global readiness event whose
probability decays with the number of lattice blocks.

The construction specifies an actual finite algorithm on the addressed
interface. It is expensive: every attempted controlled phase expands to
its stated forward word, and each measurement cycle costs its own
letters. Fast matrix powering in a checker does not reduce that price.

## 5. Complete internal records and the actual stopped price

Let T be the entire internal transcript of one stage, including every
gate retry, X sign, success time, first abort position and actual clock.
Use the parent's complete pure input convention, with every purifying
reference and old archive retained as spectators. A separately varying
initial mixed-state entropy is an additional source, not set to zero
by the following conditional-purity calculation.
The preceding Kraus identities show that its law is field independent
for arbitrary pure query data, with any external spectator included.
On every ready transcript, its normalized final quantum work is the
same ideal detector state tensored with known retained work, up to
transcript-dependent field-independent isometries. On an abort it
remains pure. Consequently the final reported click probability is
q(y)=1-det(I-zF_b(y)) on every ready transcript, and

```text
H_phi(T, report) = H_phi(T) + beta h_phi(q).
```

This retains the full CQ state. In particular the efficiency bits remain
coherent; replacing them by classical observed coins would give a
different information source, as already proved in the parent.

Write C for the actual cost of this entire stage, including its two
original queries, retained work, preparation-independent routing, all
gate attempts and reporting charges. The same query/clock interface as
the parent supplies its field-independent law. Set

```text
kappa = E C - H_phi(T).
```

The stage abort stops the experiment. A ready no-click also stops it.
A ready click continues to a fresh stage if fewer than N have run.
The continuation probability is therefore beta q, not q. The full
finite chronological entropy and cost chain rules give exactly

```text
S_N(y) = [kappa - beta h_phi(q(y))] E_N(beta q(y)).
```

The horizon-N unresolved record, gate-abort records and every old record
are present. A capped implementation is not renormalized on completion.
The preceding bank gives S_total=S_pre+alpha S_N, where its complete
S_pre is field independent under the declared stationary-delay chart.
Moving initial-record, physical sampling-time and other independently
priced upstream sources are still separate obligations.

### A lower bound for the genuine gate price

The golden entropy of a bit is at most log_phi(2)<2. Conditional on
reaching any trial, the CZ, CCZ and X-cycle net contributions are
therefore respectively greater than 18, 40 and 4. This counts all
measurement entropy even if its physical reading overhead were zero.
Nonnegative actual overheads only increase the bounds.
There are no additional independent stochastic controller records in
this specified implementation: addresses, corrections and clock values
are deterministic functions of the retained measured bits. If a
different physical controller creates additional random distinctions,
their full entropy and cost must be added to its actual kappa before
using a source bound.

Every stage reaches its first Toffoli, whose first H begins with a CZ
trial. That alone contributes more than 18. The first H finishes with
probability b_2²>=s_2²>(47/50)²>22/25, so the first CCZ trial
contributes more than (22/25)*40 in expectation. Every other reached
cycle has positive net price; deterministic corrections, swaps, ordinary
CNOTs and fixed queries add nonnegative cost. Hence

```text
kappa > 18 + (22/25)*40 = 266/5 > 53.
```

This is a lower bound on the actual expanded programme, not an artificial
padding charge. The retry and teleport records cannot make its price
equal to the old integer stage cost. No old integer-cost minimum theorem
is used for this new implementation.

## 6. Exact substitution into every original source row

For d=1-q=exp(-j_b) differentiation gives

```text
D S_N = c_N Dj_b,
c_N = d beta [(kappa-beta h_phi(q)) E'_N(beta q)
                       - h'_phi(q) E_N(beta q)].
```

At the primary family all original local blocks have the same d=d_0,
q=q_0. The parent proves by exact rational inequalities that
q_0<2^-19 and

```text
h_phi(q_0) + (1+q_0) h'_phi(q_0) < 27.5.
```

For x>=0,N>=2, E_N(x)/E'_N(x)<=1+x, by coefficient comparison.
Since 0<beta<=1 and h_phi(q_0),h'_phi(q_0)>0, the new cancellation
threshold obeys

```text
beta h_phi(q_0) + h'_phi(q_0) E_N(beta q_0)/E'_N(beta q_0) < 27.5.
```

With kappa>53, beta>1/2, alpha>=1/2, d_0>99/100 and E'_N>=1,

```text
alpha c_N > (1/2)(1/2)(99/100)(53-27.5) > 6.
```

Thus identical local implementations at every original multiplicity give

```text
D S_full|Sigma = alpha c_N sum_b Dj_b = alpha c_N DJ2.
```

This preserves all 16+24+2 original stationary Euler equations and their
original matter/geometric ratio on the configured nonvacuum midpoint
family. The nonzero multiplier is not a nonzero stationary covector.
Common address loading/query prices are necessary: unequal local
kappa_b would introduce unequal source weights and require a different
application. The map is exact at each finite mesh; this statement does
not bound the total clock uniformly under refinement.

The native moving query, actual matter-difference input map, compulsory
future task, complete Book03 valuation, independently selectable
preparations and any additional H/R price remain open. Selection among
different capped programmes is also open. This proof establishes the
source of one explicit complete programme; it does not assert that it
is the minimum among all native alternatives.

## 7. Narrow validation and input ownership

The [exact checker](check_golden_exact_detector.py) checks the literal
phase words, their expanded counts, all four X-cycle Kraus operators,
H transfer on both input basis columns, Boolean detector composition,
rational cap bounds and a complete finite renewal ledger with its first
jet. Its finite controls supplement the displayed identities; they do
not establish physical admission.

The old geometry, all40+2 theorem, original two-query first-source
contact and preparation proof are consumed unchanged. The approximate
v5 controller remains valid in its own scope; this construction uses
measurement and finite abort to replace its approximate fixed logical
rotations for this particular detector. It does not refute the
computational-blank integral obstruction or manufacture a moving
field-query jet from a fixed gate palette.
