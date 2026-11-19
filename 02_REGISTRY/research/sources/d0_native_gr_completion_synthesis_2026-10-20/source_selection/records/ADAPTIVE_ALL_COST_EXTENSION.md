# Adaptive stopped envelope for general fixed costs, ties, and the full source

20 October 2026. Read-only synthesis for existing PR #334.

This consumes the exact scalar-port and retained-pointer interface in
[STOPPED_ADAPTIVE_EXTENSION.md](STOPPED_ADAPTIVE_EXTENSION.md)
and the new fixed-branch theorem at
`45372df30740f4e75c8b58013652a7665bf833cd`:
`02_REGISTRY/research/A4D_NATIVE_STOPPED_MINIMUM_TO_J2_SOURCE_2026_10_20.md`.
The new owner's nonzero-source domain is **T>=5, ell>=1**, not all positive
costs. The mathematical adaptive-envelope estimate below has the larger
domain T>0, ell>0. These two statements must remain distinct.

All costs are finite constants under the field variations. The same physical
task, complete classical-pointer or stated cq information cut, fresh-work
query, fixed oldRIGHT marginal, preparation, and remaining-ledger hypotheses
are retained. Each policy is a deterministic decision rule pi(h), fixed before
execution and fixed under field variation. It chooses only a nonnegative
integer k from previous retained outcomes and stops at the first actual
port1. There is no direct field/t lookup or auxiliary randomization. The
pointwise infimum is over this family of fixed rules; selecting a mathematical
minimizer at each parameter does not provide an executor with that parameter.
Additional scheduler
cost is nonnegative; the fixed-k controllers used as upper bounds are fully
included in the stated ledger. No additional controls or free information
rebates are admitted.

## 1. General finite active set

Write

    a_k(t)=T+k ell+D_phi(Bern(q_k(t))||Bern(p²)),
    R_k(t)=a_k(t)/q_k(t),              q_k(t)>0,
    R(t)=min_k R_k(t),
    R*=R(0),                         A=argmin_{k>=1} R_k(0).

The original exact scalar port probabilities q_k(t) are smooth. At zero
q_k is strictly between zero and one for every positive k; q_0(0)=0.
For every fixed positive T,ell,

    R_k(t)>=T+k ell.

The fixed k=2 competitor stays bounded on some neighborhood of zero.
Consequently all competing k belong to a single finite set on that
neighborhood. The k=0 ratio diverges as t tends to zero. Thus a minimum
exists, A is finite and nonempty, and every inactive finite competitor is
separated by a positive gap at zero. Shrinking the neighborhood if needed,

    R(t)=min_{k in A} R_k(t).

This is finite reduction of the fixed-action competition; it is not a
uniform gap over all adaptive policies.

## 2. The uniform adaptive envelope survives for every positive fixed cost

Let V(y,rho) be the infimum of actual complete adaptive prices and t=t(y).
The value can depend on the full query and preparation beyond t.
For each policy, let s_h be the probability of a live history h and k_h its
next choice. The exact fresh-work entropy defect satisfies

    0<=beta_h<=B(t)=h_phi(r(t))+r(t)log_phi N_g,
    r(t)=4t⁴(1-t²),                  B(t)=O(t⁴|log|t||).

At every parameter where the policy stops almost surely with finite
expected actual cost, sum_h s_h q_{k_h}=1, and the complete price is

    S_policy=sum_h s_h(a_{k_h}-beta_h)+C_scheduler.

Since a_k>=T, for B(t)<T,

    S_policy >= (1-B(t)/T)sum_h s_h a_{k_h}
             >= (1-B(t)/T)R(t).

Terms with q=0 only add nonnegative cost to the second inequality.
The policy-specific finite expectation justifies its entropy chain rule;
no uniform expected running-time bound over policies is required.

For each fixed t a minimizing fixed action exists and supplies an admitted
upper-bound policy. Its nonnegative fine-pointer entropy implies
V(y,rho)<=R(t(y)). Therefore

    (1-B(t(y))/T)R(t(y)) <= V(y,rho) <= R(t(y)),
    V(y,rho)=R(t(y))+O(t(y)⁴|log|t(y)||).                 (E)

The bound is uniform in the supplied finite chart and normalized preparation.
The infimum defining V need not be attained.
At Sigma it is attained by every fixed action in A, and equals R*.
Terminal-node weighting shows that every optimal adaptive policy uses only
actions in A at every positive-probability reached node, with no additional
positive scheduler cost. Choices on impossible garbage histories remain
unconstrained by optimality at Sigma.

## 3. Exact first-order envelope at ties

Define the fixed-branch coefficients

    kappa_k=-(T+k ell+log_phi((1-q_k)/p)) q'_k/q_k²,
    q'_k=4 cos(k theta)sin(k theta).

The new owner proves that these are the full actual retained-branch
coefficients at Sigma, not just derivatives of a truncated scalar ledger.
Since A is finite,

    R_k(t)=R*+kappa_k t+O(t²)                  (k in A).

Combining this with (E), at any y0 in Sigma,

    V(y,rho)=R*+min_{k in A}[kappa_k t(y)]+o(||y-y0||).

More precisely the scalar remainder is O(t²)+O(t⁴|log|t||), and smoothness
of t transports it to the ambient chart. The positive-parameter Hadamard
directional derivative is consequently

    D⁺V(y0,rho0;v)=min_{k in A}[kappa_k Dt(y0)[v]].       (J)

Preparation directions with no Dt contribution have zero first derivative.
If Dt is nonzero, V is Frechet differentiable at y0 exactly when all active
kappa_k coincide. Its derivative is then their common value times Dt.
If Dt=0, V has zero Frechet derivative even when the coefficients differ.
The unique-action case is the special case of a singleton A.

If kappa_min<0<kappa_max and Dt is nonzero, (J) has a descending direction
on either side of t=0:

    t>0: first slope kappa_min<0;
    t<0: first slope kappa_max>0.

Thus such a tie is a downward cusp in the transverse scalar direction,
not a minimum. Zero lies in the convex hull of active branch covectors,
but that convex-hull fact cannot replace genuine local minimality.

For the finite smooth coarse envelope R, its Clarke subdifferential at zero
is the interval [kappa_min,kappa_max]. The pointwise remainder estimate (E)
alone does **not** establish local Lipschitz regularity or identify the Clarke
subdifferential of the complete optimized fine-pointer value V. We therefore
claim the directional first jet (J), not an unproved generalized-gradient
formula for V.

## 4. Necessary full source at a true adaptive field minimum

Now assume the new owner's domain T>=5, ell>=1. Every k in A has

    B_k>=2,                         kappa_k!=0.

Let the complete adaptive infimum V have a genuine local minimum at y0 in
Sigma over the full open admissible field neighborhood. For every active
fixed k, its actual complete price F_k remains admissible near y0 and

    F_k(y)>=V(y)>=V(y0)=F_k(y0).

That actual fixed branch therefore has a local minimum. Its first derivative
exists by the retained-work bound, giving

    0=DF_k(y0)=kappa_k Dt(y0)=kappa_k gamma_h DJ2(y0).

Since kappa_k and gamma_h are nonzero,

    genuine full-field local minimum of V at Sigma ==> DJ2=0.

This conclusion holds at ties, without differentiability of V, any
convex-hull argument, or differentiability of every optimal adaptive policy.
It is stronger in programme coverage than the fixed-k envelope consequence
in the new owner and uses the same scientific assumptions.
Two-sided variation in the claimed directions is necessary. A minimum
restricted to Sigma or a constrained boundary supplies only the corresponding
restricted conditions.

This is a necessary condition only: it establishes neither existence of a
field minimum nor stability or sufficiency of DJ2=0. The original full
16+24+2 source and its ratio are inherited only under the complete J2 and
remaining-ledger hypotheses. No physical task, Book Info, total H+J+R price,
continuum normalization or positive GR selection has been derived here.

## 5. Exact hostile control below the new owner's domain

The positivity restrictions cannot simply be removed from the nonzero-source
conclusion. At T=3, ell=1, fixed k=2 is the unique global optimizer, yet

    B_2=T+2ell-5=0,                 kappa_2=0.

Here is an all-k proof, not a finite numerical scan. Put

    A0=4+log_phi4,                  q_2=4p³.

The binary Gibbs inequality gives

    D(q)-A0 q >= -log_phi(p+p² phi^A0)=-5,

with equality exactly at q=q_2, because

    p+p² phi^A0=p+4phi²=phi⁵,
    (p² phi^A0)/phi⁵=4p³=q_2.

For every k>=3,

    R_k-A0=[3+k+D(q_k)-A0 q_k]/q_k >= (k-2)/q_k>0.

For k=1, D(q_1)=0, q_1=p²<1/2 and A0<7 (phi³>4), so

    R_1=4/p²>8>A0.

The k=2 Gibbs equality gives R_2=A0. Thus k=2 is the unique global optimizer
at this positive cost pair. Section 3 then shows that the complete adaptive
optimized value also has zero first derivative, regardless of DJ2.
This excludes an extension of the nonzero-source theorem to all T>0,ell>0.

## 6. Differentiating individual optimal adaptive policies requires care

At Sigma, optimality restricts only reached histories. A policy can put
arbitrary choices on garbage histories that have probability zero at Sigma
and positive probability nearby. Its own price need not inherit a first jet
without an appropriate local integrability bound. This does not affect (E)
or the true-minimum argument, which use uniform lower bounds and fixed-action
upper competitors.

For the smaller class of policies using only the finite active action set A
on every possible history in a neighborhood, and with no scheduler charge
beyond the stated T+k ell ledger, q_min>0 gives a uniform geometric tail.
An additional scheduler term would need its own zero first jet and suitable
local domination for the following individual-policy derivative statement;
nonnegativity alone is insufficient for that statement.
Such a policy agrees with a deterministic failure-count schedule until
the first nonclean work outcome. The probability of any nonclean outcome is
at most r E[N]<=r/q_min. Conditional remaining expected costs are uniformly
bounded because both the finite action costs and 1/q_min are bounded.
Replacing the policy after its first nonclean outcome by that failure-count
schedule therefore changes its coarse expected price by O(r)=O(t⁴).
The fine-pointer entropy changes it by at most O(B(t)).
Its first derivative is consequently the derivative of that deterministic
coarse schedule:

    sum_h s_h(0)q_{k_h}(0) kappa_{k_h} Dt,

a convex combination of active branch covectors. To derive this, subtract
R* using sum_h s_h(t)q_{k_h}(t)=1:

    S_coarse(t)-R*
       =sum_h s_h(t)[a_{k_h}(t)-R* q_{k_h}(t)].

Every bracket vanishes at zero. Differentiation therefore gives the displayed
weighted coefficients; the finite smooth scalar port family and geometric
tail justify termwise differentiation for that coarse process.
A convex combination containing zero does not by itself prove that some
deterministic schedule realizes that combination; its weights are constrained
by the actual stopping tree. In particular, if the initial action is i then
the coefficient must lie in

    q_i kappa_i+(1-q_i)conv{kappa_k:k in A}.

The union of these sets over i in A can exclude zero even when the full
convex hull contains zero. No external randomizer is part of this theorem.
