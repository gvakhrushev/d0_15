# Paid Golden resource bank for the original two-query determinant source

20 October 2026. Existing PR #334 and
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Phase: native realization, bounded composition inside the existing owner.
Consumer: [the two original 8D queries](TWO_NATIVE_8D_DETERMINANT_SOURCE.md),
sections2–3, then the primary all40+2/midpoint source map.

## 1. The exact premise replaced

The two-query experiment requires two fixed input states, `|+>` and `|->`,
and two independent20-bit efficiency registers per attempted stage.
Its previous interface supplied these states. The following finite
programme generates them from computational blanks using the **owned**
Golden parity-heralding construction, while retaining preparation failures,
their actual costs and the final abort outcome.

It realizes a new complete experiment with an explicit preparation-abort
branch. It is not a deterministic exact compiler of the old experiment:
conditional on readiness, the old experiment is recovered; the unconditioned
full CQ price has a proved first-source relation. No successful branch is
renormalized away when computing that price.

Owned inputs, read at source head
`2fd755f9073bfba425070319c721278893b69ca4`:

- [Golden coherent Bell preparation](../../../A4D_NATIVE_GOLDEN_COHERENT_BELL64_EXACT_P18_PROGRAMME_AND_BOOK_WORK_2026_10_20.md),
  sections1 and3: the actual parity gadget, its retained failure, and the
  finite readiness law. We apply these results, not re-prove a new extractor.
- [Native Golden programme compilation](../../../A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md),
  section1: a supplied known-one control gives the exact forward echo
  `X G X=G^T`, preserving that control.
- [Compiler/source/resource boundary](../../../A4D_NATIVE_COMPILER_SOURCE_AND_RESOURCE_BOUNDARY.md),
  sections2–4: the integral-blank obstruction and the distinction between
  fixed control preparation and a moving field-query interface.
- [Finite future determinant price](FINITE_FUTURE_DETERMINANT_MINIMUM.md),
  sections3,6–8, with its [independent review](FINITE_FUTURE_DETERMINANT_REVIEW.md):
  the full monitored CQ price and integer-cost source gap.
- [Two-query source](TWO_NATIVE_8D_DETERMINANT_SOURCE.md): the original
  fixed rank-two basis, literal8D queries and their entire first-source map.

All addressability, fresh blank supply, measured feedforward and reading
operations below belong to the declared active Golden/CNOT interface.
Their physical G0 admission is not inferred from the matrix identities.

## 2. Delivered states and retained transcripts

Write `a=sqrt(p)`, `p=phi^(-1)`, `s=2p^3`, `r=1-s`.
On three fresh blanks A,B,C, execute G on A and B, then
`CX(A,C), CX(B,C), CX(A,B)`. The already-owned odd-parity success gives

```text
ap (|0,1,1> + |1,1,1>) = sqrt(s) |+>_A |1>_B |1>_C.
```

Only the parity flag C is measured. Failure retains the complete coherent
AB state and its recorded flag. Reserve the first such successful resource
as a plus input; its separable known-one byproduct supplies the exact X
control for subsequent inverse uses.

For a minus input, replace the second G by its forward echo `X G X`.
The same odd-parity circuit gives

```text
ap (-|0,1,1> + |1,1,1>) = -sqrt(s) |->_A |1>_B |1>_C.
```

The overall sign is immaterial to this separate prepared input.
The success probability is again s. The echo uses the retained known-one
control twice and leaves it unchanged. It does not copy an unknown input.
The success branches provide the actual fair pure qubits; a deterministic
Walsh unitary has not been constructed.

For each requested resource, use at most K fresh attempts, stopping at
its first success. If all K fail, retain that transcript and abort the
remaining bank. If successful, route the delivered state to its canonical
output slot before beginning the next resource. The first plus resource
also supplies a canonical known-one control slot. A known measured address
can be routed by a paid SWAP word of three addressed CNOTs; the permission
to choose and execute that addressed word remains part of the controller
interface. All old slots, blank replacements and failure states remain.

With `M=42N` resources for one local N-stage detector, the ready probability is

\[
 R=1-r^K,\qquad \alpha=R^M.                       \tag{1}
\]

Sequential abort does not change this product: conditioned on each earlier
success, the next fresh trials have the same s and r. No controller must
run a minus preparation without first obtaining the known-one control.

Every ready transcript delivers the **same tensor of states in the same
canonical slots**: one plus input, one minus input and40 independent fair
coin qubits for each potential query stage. The20-bit all-zero event has
the original exact efficiency `z=2^-20`, separately on each query.
These are40 independent fair qubits, not one shared efficiency switch.
The original retained basis consists of two fixed computational addresses
inside the8D unit. Embedding the delivered input qubit at those addresses
uses a fixed binary affine encoding with CNOT and known-one-controlled X,
with its actual preparation/routing cost retained.

The readiness event depends only on fixed p, N and K. Neither the field y
nor the old logical input/RIGHT participates in this preparation.
Every conditional complete preparation work state is pure; its classical
success/failure/time transcript remains readable.

## 3. Complete price, with the actual preparation paid once

Let X be the entire preparation transcript, including early aborts, first
success times, routing and actual preparation clock. Write its probability
as pi_x, its complete cost as C_pre(x), and the ready event as A.
The bank uses only fixed operations, so these data are independent of y.
Define its full declared CQ price by

\[
 S_{\rm pre}=\sum_x\pi_x C_{\rm pre}(x)-H_\varphi(X).
                                                               \tag{2}
\]

This is an actual ledger term, not a discarded constant or free resource.
No particular numerical G0 price is asserted for measurement, addressing,
storage or fresh blanks. Their charges must be included in C_pre.
The source theorem only requires their field independence on the chart.

On abort, terminate with the explicit abort record. On readiness, run the
old finite N-stage monitored two-query experiment. Its post-readiness
stage cost is the same positive integer `tau_run` for **every** ready
transcript. It includes the query, detector, reporting and continuation
operations. It excludes seed preparation/routing already paid in (2).
Unused prepared resources remain in the final work if verification stops
early.

The old preparation archive, oldRIGHT and elapsed preparation clock are
spectators to this stage. The same fixed field y and addressed original
query are used after every ready transcript; a change of physical sampling
time caused by preparation delays is not silently ignored. A native clock
map that reads the elapsed delay would need a separate source calculation.
If the old input density itself varies with y, its genuine initial
entropy/price source must also be added; being a spectator to these gates
does not make a moving initial record field independent.

For local determinant success d, put q=1-d and
`E_N(q)=sum_{j=0}^{N-1} q^j`. The existing theorem gives

\[
 S_N(y)=[\tau_{\rm run}-h_\varphi(q(y))]E_N(q(y)).   \tag{3}
\]

Conditional on any ready x, the entire query-history distribution and
conditional pure work are the same. On abort there is no query history.
The entropy chain rule and the executed-cost ledger therefore give

\[
\begin{split}
 H_\varphi(X,H)&=H_\varphi(X)+\alpha E_N(q)h_\varphi(q),\\
 E C_{\rm total}&=E C_{\rm pre}+\alpha\tau_{\rm run}E_N(q),\\
 \boxed{S_{\rm total}(y)=S_{\rm pre}+\alpha S_N(y).} \tag{4}
\end{split}
\]

All failed preparations, successful but unused resources, query failures
and the unresolved horizon-N record are included. Microscopic pure work
is not dephased in addition to the specified measured transcript. A
different information algebra requires its own calculation.

In particular,

\[
 DS_{\rm total}|_\Sigma
   =\alpha\,c_N(a_0,\tau_{\rm run})\,Dj_b,\qquad
 a_0=(1-zL)(1-zM_0).                              \tag{5}
\]

Here `L=4p^3`, `M_0=L(1+p^6)` are the original feedback bands; M in (1)
denotes resource count, not a feedback eigenvalue. Equation (5) is a
component source on the specified field chart. It does not discharge
independently varied upstream preparation or a different physical Book
valuation by declaring them constant.

## 4. Uniform readiness without a global all-ready penalty

The original positive numbers obey `r=3-4p<53/100`. Choose the least
positive integer K satisfying

\[
 M(53/100)^K\le1/2.                               \tag{6}
\]

Then Bernoulli's inequality gives

\[
 \alpha=(1-r^K)^M\ge1-Mr^K\ge1/2.                 \tag{7}
\]

This is finite, with K of order log M. The actual finite worst-case bank
uses at most MK parity trials, plus routing. All those resources remain
paid; the estimate concerns readiness, not a claim that storage is free.

Run a separate bank and verifier for **each** true original local unit b,
including every regular/reference/LEFT multiplicity. Do not impose one
global all-ready condition across the lattice. With the common N,K and
query-stage template, the complete independent local CQ prices add:

\[
 DS_{\rm full}|_\Sigma
    =\alpha c_N(a_0,\tau_{\rm run})\sum_bDj_b
    =\alpha c_N(a_0,\tau_{\rm run})DJ_2.            \tag{8}
\]

The owned integer-cost result gives, for every N>=2,

\[
 |\alpha c_N(a_0,\tau_{\rm run})|>0.195.            \tag{9}
\]

Thus readiness introduces no lattice-multiplicity suppression of the
common source coefficient. All42 original field Euler rows, the original
matter/geometric ratio and the same exact midpoint representatives are
preserved. Their stationary covectors are zero; it is the multiplier in
(8) that is nonzero. The coefficient bound does not remove mesh factors
already present in DJ2 or establish the original raw216 norm estimate.

For a common fixed bank, minimizing over the old admitted query compiler
class commutes with (4), since alpha>0 and S_pre is common. The existing
integer-cost noncancellation therefore applies to its winning tau.
This does **not** compare different banks, readiness probabilities, CQ
cuts or future tasks. If a compiler changes them, its objective becomes
`S_pre,c + alpha_c S_N(tau_c)` and needs a new justified comparison.

## 5. Necessary controls and remaining native interface

The integral-blank obstruction is respected. A single ready fair resource
has unconditional one-outcome probability

\[
 R/2=p^3\sum_{j=0}^{K-1}r^j\ \in\mathbb Z[p].      \tag{10}
\]

There is no unconditional rational half-probability with all other outputs
discarded. The nonintegral conditional state is supplied by an actual
retained heralding history. Reading only the ready branches and assigning
them total probability one would lose the factor alpha in (4)–(8).

The concurrent two-query input at
`1736a02f10f2f3352f7758e53356506ffe44787c`, section4a, establishes a
different obstruction: measuring the efficiency coin itself changes the
full information from `h_phi(z lambda)` to
`h_phi(z)+z h_phi(lambda)`, with a nonzero field-source difference.
This bank does not make that substitution. It measures the seed parity
and preparation times; the delivered fair qubits remain pure and coherent.
Their computational values and the efficiency event are not observed
before the final query flag. Equation (4) includes the measured
preparation archive while preserving the original coherent efficiency
instrument on every ready branch.

The canonical-slot and common-stage conditions are essential. If ready
transcript x instead runs a stage of cost tau_x, the source uses the mean
`E[tau_x | ready]`. This mean need not be an integer. Since the owned
cancellation threshold lies between27.4 and27.5, a suitable mixture of
integer costs27 and28 could cancel it. Unknown routing cannot be hidden
inside a claimed integer common stage.

Likewise, arbitrary independently varied input states are not covered by
the field-source map. For the full one-particle projection
`A_full=U^*QU`, a normalized retained eigenvector psi with eigenvalue
lambda of `P A_full P` has
`v=(I-P)A_full psi`, `||v||^2=lambda(1-lambda)`.
The normalized preparation tangent psi+t v changes its no-click
probability by `-2z lambda(1-lambda)` at zero. It is nonzero at the
original interior bands. This prevents treating unrestricted preparation
Euler rows as consequences of the compressed determinant identity.
Here the resource states are generated by fixed words; any independent
physical preparation freedom must still be identified and priced.

The specific removed supply assumption is an external exact Walsh/fair
resource bank for the two-query source experiment. What remains:

- native admission of the actual **moving** `E(f),b(q)` 8D query and its
  full first jets; the literal Golden anchor matrix alone does not supply it;
- coherent AND/OR detection or an admitted equivalent coarse projection,
  canonical paid address/routing and the required monitored operations;
- a compulsory future task allowing these complete abort/unresolved
  records, the physical clock map and actual Book03 Info binding;
- all separately priced original H/R/controller/upstream sources.

The existing approximate control compiler does not by itself prove exact
AND/OR words. This packet asserts no new impossibility or approximate
source transport there. It supplies no physical GR promotion, new task,
assembly acceptance or lifecycle retirement.

Companion bounded checker: [check_determinant_preparation_bank.py](check_determinant_preparation_bank.py).
