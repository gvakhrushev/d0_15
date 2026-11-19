# Paid monitored random choice preserves the stopped source envelope

20 October 2026. Supporting extension in existing PR #334.

## 1. Consumed owner and the one additional programme class

The deterministic adaptive theorem, uniform complete-work estimate and
directional envelope are already owned by
[ADAPTIVE_ALL_COST_EXTENSION.md](../source_selection/records/ADAPTIVE_ALL_COST_EXTENSION.md),
blob 62bd1f4b9186883f521e363d17f023c4ab4ac760 at head 7620c0.
They are consumed here without a second adaptive or all-budget proof.
That owner in turn consumes the fixed-branch source theorem
A4D_NATIVE_STOPPED_MINIMUM_TO_J2_SOURCE_2026_10_20.md.

The additional class consists of fresh **monitored classical** controller
choices, generated after a retained history, with the full choice leaf and
its actual native prefix cost retained. The required task, source-bound
query, scalar ports, fixed initial oldRIGHT marginal and complete pointer
information cut are unchanged. Policies and their choice mechanisms are
fixed before execution and under field variation; they receive no external
field-value lookup. A pointwise mathematical infimum is not an executor
that can inspect that parameter.

As in the consumed owner, put \(p=\varphi^{-1}\), \(T>0\), \(\ell>0\), and

\[
a_k(t)=T+k\ell+
D_\varphi(\operatorname{Bern}(q_k(t))\Vert\operatorname{Bern}(p^2)),
\qquad
R(t)=\min_{q_k(t)>0}\frac{a_k(t)}{q_k(t)}.
\tag{1}
\]

The reporter has actual words \(0\) and \(10\), with lengths 1 and 2.
Thus its mean cost minus its new-record entropy is precisely the
relative-entropy term in (1), using \(p+p^2=1\).
In particular \(a_k\ge T+k\ell\ge T\).
The available constant-action competitors and every cost already included
in \(T+k\ell\) remain exactly those of the consumed owner.

## 2. The full native choice word pays for its mixing entropy

At a reached history \(h\), let \(w\) be the complete fresh monitored
choice leaf, with conditional probability \(\pi_h(w)\), selecting action
\(k=k_h(w)\). Distinct completed leaves are prefix free in the original
\(0/10\) tree. Let \(L_h(w)\) be the number of original binary symbols in
that word. The Golden cylinder weights give

\[
\sum_w p^{L_h(w)}\le 1.
\tag{2}
\]

This follows directly by putting probabilities \(p,p^2\) on the two
outgoing native tokens; disjoint completed leaf cylinders have total
probability at most one. A field-dependent or controller-dependent
selection law need not equal these reference cylinder weights.

Charge actual choice cost \(C_h(w)\ge L_h(w)\), including all selector
calls, writing, addressing and work that the asserted implementation
charges. This is **separate** from (1): work already charged there is not
charged twice, and an extra choice operation is not declared included
without an implementation. Any additional monitored choice randomness
must be in \(w\), or independently satisfy the same paid-record bound;
coarsening \(w\) to the chosen integer \(k\) is not the complete record.

For nonempty support set
\[
\mu_h(w)=p^{C_h(w)},\qquad
Z_h=\sum_w\mu_h(w)\le1.
\]
On finite support, or when both expected cost and entropy are finite,

\[
\boxed{
\eta_h:=\mathbb E[C_h(W)\mid h]-H_\varphi(W\mid h)
=D_\varphi(\pi_h\Vert\mu_h/Z_h)-\log_\varphi Z_h
\ge0.}
\tag{3}
\]

All logarithms use base \(\varphi\). The displayed price is never defined
by subtracting two infinities. Equality requires both \(Z_h=1\) and
\(\pi_h=\mu_h\) on the full leaf space. If the literal implementation
additionally pays \(C_h(w)\ge L_h(w)+c\) for every leaf, then
\(\eta_h\ge c\). In particular an additional unit-cost selector call
gives the stronger lower bound 1 only when that decomposition is actual.
Calling a choice random does not prove that extra charge.

Equation (3) includes optimal mixing entropy. Explicitly, for a finite
leaf set and a proposed continuation value \(v\), the relaxation over
all probability laws has exact value

\[
\inf_\pi\left\{
 \mathbb E_\pi[
 C_h(W)+a_{k_h(W)}+(1-q_{k_h(W)})v]-H_\varphi(\pi)
 \right\}
=-\log_\varphi\sum_w
\mu_h(w)\varphi^{-a_{k_h(w)}-(1-q_{k_h(w)})v}.
\tag{4}
\]

At \(v=R(t)\), each
\(a_k+(1-q_k)R\ge R\), including \(q_k=0\).
Consequently (4) is at least \(R-\log_\varphi Z_h\ge R\).
This is a lower bound for every actually admitted selector; it does not
assert that an arbitrary optimizing probability law has a native
implementation.

An already retained classical random seed receives no second fresh
entropy credit. Condition on its complete initial value, apply the
deterministic result and then average, with its unchanged initial
entropy kept as a common baseline. If the declared cut also conditions
on a fixed quantum oldRIGHT system \(R_{\rm old}\), classical
conditional entropy satisfies
\[
H_\varphi(W\mid hR_{\rm old})\le H_\varphi(W\mid h).
\]
Hence (3) remains a lower bound with that conditional entropy.
A moving initial entropy or a newly measured quantum seed requires its
own actual information/cost account.
In the application below, \(\eta_h\) denotes the actual net choice
price: (3) for the classical cut, or the larger
\(\mathbb E C_h-H_\varphi(W\mid hR_{\rm old})\) for the stated
conditional cut. It is nonnegative in both cases.

## 3. Application to the owned stopping theorem

Consider a proper policy stopping at the first actual port1, with finite
expected executed cost and finite complete-record entropy. At each live
history apply (3) before the original trial. Scalar port effects give the
same \(q_k(t)\) for the actual conditional logical state. The full
conditional chain rule, with every choice leaf retained, replaces the
owner's deterministic stage \(a_{k_h}\) by

\[
\mathbb E_{\pi_h}a_{k_h(W)}+\eta_h.
\tag{5}
\]

If \(s_h\) is the probability of reaching \(h\), the unique first success
gives
\[
\sum_hs_h\,\mathbb E_{\pi_h}q_{k_h(W)}=1.
\tag{6}
\]
Since \(a_k\ge Rq_k\) and \(\eta_h\ge0\), the actual scalar-record price
is at least \(R(t)\). The already admitted deterministic constant
minimizer remains available without inserting a fresh selector.
Therefore

\[
\boxed{\inf_{\text{proper policies with paid monitored choices}}
 S^{\rm scalar}=R(t).}
\tag{7}
\]

This includes history-dependent choices and laws that vary through the
retained history. Nonnegative additional scheduler charges preserve the
lower bound. Attainment of (7) still uses the owner's actual fixed-action
implementations, including their setup and controller prices.
For a fixed policy, a strictly positive \(\eta_h\) at a positive-probability
history gives a strict loss against the lower bound; this does not imply
a uniform gap for all nonoptimal policies.

For the complete fine-work price, consume the owner's uniform
per-trial classical conditional-entropy defect
\[
0\le\beta_h\le B(t),\qquad
B(t)=O(t^4|\log|t||).
\tag{8}
\]
The only change in its proof is the nonnegative summand \(\eta_h\) in
(5). In a neighbourhood where \(B(t)<T\), the enlarged infimum
\(V_{\rm paid}(y,\rho)\) therefore satisfies the same estimate:

\[
\boxed{
(1-B(t(y))/T)R(t(y))
\le V_{\rm paid}(y,\rho)\le R(t(y)).}
\tag{9}
\]

The upper bound is the same actual constant-action competitor. No
uniform running-time bound over all policies is assumed, and the full
infimum need not be attained. Garbage orientation and rare-work
control may depend on the full field \(y\), not only on \(t(y)\).
Equation (9) does **not** assert equality of the deterministic and
randomized complete fine-work infima away from the primary family.
It proves the same first-order envelope. A selector's extra work entropy
is already covered by its complete leaf in (3); it is not placed in
the small \(B(t)\) term without proof.

The sign in (8) is about the declared classical monitored new records,
possibly conditioned on the fixed quantum oldRIGHT. It is not a claim
about the conditional entropy of an arbitrary unmeasured quantum
subsystem. Interfering coherent superpositions of different programmes
are outside this monitored-choice theorem.

## 4. Source inherited without a new physical selector

Let \(A\) be the finite active set in the consumed owner at \(t=0\),
and let \(\kappa_k\) be its actual fixed-branch source coefficients.
Equations (3) and (9) extend its directional-envelope formula unchanged:

\[
D^+V_{\rm paid}(y_0,\rho_0;\xi)
=\min_{k\in A}\{\kappa_k\,Dt(y_0)[\xi]\}.
\tag{10}
\]

Here \(D^+\) is the positive-parameter directional derivative. In the
owned source domain \(T\ge5,\ell\ge1\), every active
\(\kappa_k\ne0\). Under the same complete-source binding
\(Dt=\gamma_h DJ_2\), \(\gamma_h\ne0\), a genuine local minimum of
the enlarged complete value in the full open admissible field
neighbourhood consequently requires \(DJ_2=0\), by the owner's
active-fixed-competitor argument. The original 16 coframe, 24 link
and two matter rows, and their original signed ratio, are unchanged.

No existence, stability or sufficiency of such a field minimum follows.
The optimized value at a tie is distinct from a preselected mixture of
tied implementations: such an implementation may have cancelling
source coefficients if its stopped derivative exists. Neither (10)
nor the minimum implication asserts a nonzero source for every
individual minimizing controller, or a Clarke-subgradient criterion.

This extension removes free mixing entropy as a loophole **within the
specified native paid-record class**. It does not derive the compulsory
future comparison, the Book03 identification of Info with this cut,
the native source-query implementation, the fixed costs, or the
remaining moving preparation/clock/H+J+R terms. In particular a
field-independent programme that solves a weaker first-bright task
remains a separate prospective competitor unless the actual task
requires the source-dependent comparison.

The mathematical change is the one-history identity (3), its
conditional chain-rule application (5), and the preservation of the
already owned bound (9). No new Golden norm estimate, geometric
calculation, arithmetic census or deterministic adaptive replay is
required.
