# Literal code prices: the resolution required by all metric probes

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing #310.
Input: `f55bea04beed7aab18141e4284e49fe66cd397ed`.
Status: **complete arithmetic obstruction for the stated code-price
interface; no native joint preparation or GR closure**.

## 1. The primary route being tested

BOOK_03 §03.10(f) defines a geometry sum
`Z_k = sum_(G,J) phi^(-A(G,J))`, with A the length of a minimal code.
It explicitly distinguishes this sum from the heat/feedback partition.
For literal finite-word length, A is a natural number, whatever the
decoder, admissible graph family or readout. Weighted noninteger costs
are a different interface. The present result does not define a decoder,
change the admitted family or equate this A to the bootstrap action.

Suppose a proposed direct reading of this code price is

\[
 I_h^N(\omega)=\nu_h A_h(\omega)+b_h,
 \qquad A_h:\Omega_h\to\mathbb N,\quad\nu_h\ne0.       \tag{1}
\]

The level constant b_h cancels in a centered contrast. The multiplier
nu_h must be derived by that proposed native reading; none is selected
here. For the one fixed calibration a!=0 and any admitted endpoint pair,

\[
 a^{-1}\Delta I_h^N
 =\frac{\nu_h}{2a}(A_h(\omega_+)-A_h(\omega_-))
 \in\delta_h\mathbb Z,\qquad
 \delta_h=\frac{|\nu_h|}{2|a|}.                         \tag{2}
\]

This includes every state space, constraint, graph grammar, endpoint
preparation and refinement whose scalar price has form (1). It does not
require a smooth finite state space or an independent hidden variation.
Completeness is only for (1), not for the full native price or core.

The unit lower bound in `EndogenousActionQuantum.ActionProtocol` is
weaker: two allowed real costs 1 and 1+epsilon can have arbitrarily small
difference. Integrality in (1) must not be inferred from that lower bound.

## 2. A fixed code unit cannot pass a nonzero small contrast

For every real s,b and integer k,

\[
 2|b|\le |s|\quad\Longrightarrow\quad |sk-b|\ge |b|.    \tag{3}
\]

For k=0 this is equality. Otherwise |k|>=1 and the triangle inequality
gives |sk-b|>=|s|-|b|>=|b|. If a recorded value r has |r-sk|<=e, then

\[
 |r-b|\ge |b|-e.                                      \tag{4}
\]

These are generic compiled inequalities, including their application
to two natural-valued endpoint prices. They do not rely on a finite
search over integer costs.

Take a physical half-contrast B_h=c epsilon_h+O(h), with c!=0,
epsilon_h=h^(1/3), and recording/refinement errors O(h). A fixed
nonzero nu gives a fixed lattice spacing. For small h, (3)--(4) imply
an error at least |c| epsilon_h/2. Thus the required O(h) transfer fails.
The same conclusion holds when the spacing eventually exceeds twice
the target magnitude, with the explicit bound (4).

There is an already proved physical test with c!=0: the c=1 warped
metric in [the coupled-Hodge proof, §4](A4D_NATIVE_COUPLED_HODGE_SCALE_BOUNDARY.md#4-quantitative-contrast-obstruction-including-every-separate-volume-term)
has I(g)=-3*pi^2/50. Its homothetic probe s g satisfies
I_h(s)=s I_h(1), I_h(1)=I(g)+O(h), with all 24 connection residual rows
controlled there. A proposed native transfer must first admit the
corresponding endpoints; their physical existence is not native admission.
This metric is a probe control, not an asserted sourced native solution.
If the declared comparison class has only c=0, this argument does not
exclude it. No source is fitted to make c nonzero.

## 3. All scalar probes force a sharper normalization bound

**Theorem.** Let h_j>0 tend to zero, epsilon_j=h_j^(1/3), c!=0 and
delta_j>0. Suppose that for every fixed t in [0,1] there are C_t<infinity,
N_t and integers k_j(t) such that, for every j>=N_t,

\[
 |\delta_j k_j(t)-c\,\epsilon_j t|\le C_t h_j.          \tag{5}
\]

Then delta_j=O(h_j). The constants and starting levels may depend on t;
no uniformity, continuity or measurability of the chosen preparations
k_j(t) is assumed. Conversely, delta_j=O(h_j) allows (5) by rounding
on the unrestricted integer lattice. This converse supplies no admitted
codes, level budgets, physical readout or native preparation.

**Proof of necessity.** Let d_j(t) be the distance from c epsilon_j t
to delta_j Z. For positive integers M,N put

\[
 E_{M,N}=\bigcap_{j\ge N}\{t\in[0,1]:d_j(t)\le M h_j\}.
\]

These are closed, measurable sets; (5) says their countable union is
[0,1]. If delta_j/h_j were unbounded, choose an increasing subsequence
along which it tends to infinity. Fix M,N. Eventually on that subsequence
delta_j>2 M h_j. In the interval of physical values of length
|c| epsilon_j, at most |c| epsilon_j/delta_j+3 lattice-centered intervals
of radius M h_j meet the interval. Therefore their preimage in [0,1]
has Lebesgue measure at most

\[
 \frac{2 M h_j}{\delta_j}
   +\frac{6 M h_j}{|c|\epsilon_j}\longrightarrow0.     \tag{6}
\]

E_(M,N) is contained in every such preimage, so it has measure zero.
Their countable union cannot be [0,1], a contradiction. This also shows
that along an unbounded-spacing subsequence almost every fixed t fails
an O(h) bound. The proof concerns fixed probes, not a probe selected
separately at every mesh.

For sufficiency, choose the nearest integer to c epsilon_j t/delta_j;
the error is at most delta_j/2. The generic rounding bound is compiled.

For the actual transfer contract, apply the physical probe theorem to
the fixed probes t V. Its O_t(h) remainder and any O_t(h) recording or
refinement error are absorbed into C_t. Thus, in class (1), coverage of
all these probes with nonzero c requires

\[
                       |\nu_h|=O(h).                  \tag{7}
\]

The same statement follows from the secant error O(h^(2/3)) after
multiplication by epsilon_h. A finite list of probes is insufficient:
on {0,1/2,1}, spacing delta_h=epsilon_h/2 gives exact readings although
delta_h/h diverges. The fixed missing probe t=1/3 already detects that
example. The zero-response exception and the positivity of delta_j
are essential; rounding cannot approximate a nonzero target with a
collapsed lattice {0}.

## 4. The golden history sum escapes the integer-price premise

Put p=phi^(-1). The owned identity p+p^2=1 makes the total product
weight of all n binary records equal to one. Keep the entire record
space, and consider the event excluding only the all-second-branch
word. Its probability is

\[
 Z_n=1-p^{2n},\qquad C_n=-\log_\varphi Z_n.
\]

For n>=2, p<Z_n<1, hence 0<C_n<1, and C_n tends to zero. Indeed,
for u=p^(2n),

\[
 \frac{u}{\log\varphi}\le C_n
 \le\frac{u}{(1-u)\log\varphi}.
\]

The bounds follow by integrating 1/(1-v) from zero to u. The identity
at two ticks, p^2+2p^3=1-p^4, is compiled using the actual Phi owner;
exact finite record sums check it independently. Excluding a word from
an observed event does not delete that word or its memory from the
system. These are probability calculations on the existing golden
weights, not a physical apparatus/admission theorem.

Consequently a log of a sum, a full heat/logdet price, a non-lattice
weighted cost, or a derived shrinking unit is not excluded by (3) or
(7). A minimum code length cannot be substituted for the log of the
sum over its histories. Identifying a geometry/history statistic with
the actual bootstrap price and physical probes still needs its own
native law. No marginal action, normalization or temperature is installed.

## 5. Proof status and next consumer

The all-probe theorem (5)--(7) has the analytic measure proof above;
it is not inferred from finite samples or claimed fully Lean-formalized.
The [capsule](certificates/a4d_native_code_price_resolution.lean) proves
the exact lattice, error and rounding inequalities, the unit-bound
countercontrol and the owned golden algebra. Its
[printed propositions](certificates/a4d_native_code_price_resolution_output.txt),
[compiler receipt](certificates/a4d_native_code_price_resolution_results.json),
[exact checker](certificates/a4d_native_code_price_resolution_check.py) and
[ledger](certificates/a4d_native_code_price_resolution_certificate.json)
retain the analytic/formal boundary and primary input hashes.
The checker passes 185 exact controls, executes and rejects six altered
mathematical rules, and rejects eighteen false scope ledgers. Those finite
controls do not replace the measure proof of the all-probe theorem.

This closes the direct, fixed-unit minimal-code substitution and gives
a necessary resolution bound for every normalization in the stated
interface. It does not construct Omega/A/R or exclude every such law.
For a genuine geometry-sum route the next input is its actual admitted
graph/history family and its price/readout relation, retaining the full
archive. The full heat/feedback bootstrap remains separate until that
relation is proved. T0--T3, the 44 dependency nodes, own source/Ward,
curved roots, soundness/recovery and #310/#202/#317 retain their statuses.
