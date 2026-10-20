# Independent addendum: uniform B bound, active-branch minimum, and checker correction

Reviewer: `cost_variation`, bounded read-only subtask of PR #334.
Date: 20 October 2026. This is a separate addition; no previously reviewed
or published file was changed.

Companion review: `STOPPED_ALL_PREFIX_SECOND_REVIEW.md`, SHA-256
`c9734b128e631226e37e1208adaa930ae8c2d96d28c0b35285c21b32f74c5ea0`.

**Verdict:** both proposed mathematical strengthenings are correct under
their stated component-model and local-admissibility hypotheses. The
reported factor-of-two error in the upstream checker's final target is
confirmed independently. Equations (8) and (11) of the upstream proof
already give the correct coefficient.

## 1. Uniform B_k >= 2 for every minimizing branch and every T >= 5

Write D_2=D_phi(Bern(q_2)||Bern(p^2)) and q_2=4p^3=8p-4.
Both probabilities are strictly between 0 and 1. The cross entropy is
1+q_2<2 and the Shannon entropy is positive, so D_2<2 strictly.
The exact root bound p>8/13 gives q_2>12/13.

If k minimizes the stipulated stopped score at the common-null stratum,

    T+k <= S_k(T) <= S_2(T) < (T+4)/q_2 < 13(T+4)/12.

Consequently

    k < T/12+13/3.

Combining this with the independently proved algebraic-norm inequality
B_k>T-4k+1 gives

    B_k > (2T-49)/3.

For T>=50 this is B_k>17. On 5<=T<=50 the inherited global minimizer
theorem gives the unique branch k=2 and B_2=T-3>=2. Thus

    for every real T>=5 and every minimizing k: B_k>=2.

The bound is attained at T=5, k=2. This uniform lower bound concerns B_k;
it does not give a positive uniform bound on the full source multiplier,
because q'_k may become small along large indices.

## 2. An actual local minimum forces the active branch to be stationary

Let F(y)=inf_j S_j(y) over the common admissible programmes. Suppose:

1. F has a genuine finite local minimum at y_0 in the full admissible field
   neighbourhood, not merely on the common-null stratum Sigma.
2. k is active at y_0: F(y_0)=S_k(y_0).
3. This same programme k is admissible and S_k is defined throughout that
   neighbourhood and differentiable at y_0 in the considered field directions.

For every sufficiently nearby admissible y,

    S_k(y) >= F(y) >= F(y_0) = S_k(y_0).

Therefore y_0 is a local minimum of S_k itself. On an open field chart,
or on every two-sided admissible tangent variation, Fermat's elementary
necessary condition gives D S_k(y_0)=0. No differentiability, continuity,
or choice of derivative of F is required for this implication.

For the stopped Golden branch at y_0 in Sigma,

    D S_k(y_0) = kappa_k Dt(y_0)
              = kappa_k gamma_h D J_2(y_0),
    kappa_k = -B_k q'_k/q_k^2 != 0,   gamma_h>0.

Hence D J_2(y_0)=0 in every direction included in that full differentiable
source identity. The conclusion applies independently to every active
admissible branch, so index ties do not obstruct this necessary condition.

Exact limits of the statement:

* A minimum only on Sigma gives only the derivative restricted to Sigma;
  it does not force all transverse Euler sources to vanish.
* A constrained or boundary minimum gives the corresponding restricted
  first-order condition, not an unconstrained vanishing covector.
* The conclusion is about a genuine local minimum. A zero Clarke
  generalized gradient alone is weaker and cannot be substituted: the
  elementary example min(y,-y)=-|y| has 0 in its Clarke generalized
  gradient at 0 while neither active smooth branch is stationary.
* No local minimum is proved to exist; no Hessian or sufficient condition
  is supplied; and the converse D J_2=0 implies a local minimum is not claimed.
* The fixed stopped task, pointer-Info cut, unit Golden charge, full source
  identity, and absence of additional moving residuals remain assumptions.

This implication can consume a proved actual minimum of the complete
stipulated objective. It cannot replace the proof that the native physical
programme realizes or minimizes that objective.

## 3. Independently confirmed upstream checker factor of two

Fetched read-only from commit
`f22c1864bd85e097166abd75dc048164d8d63c65`:

`02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/check_stopped_source_minimum.py`

Git blob: `51dece5e5f6cf5fa2c0b66d455fe5cdbd7b4c093`.
The final decimal section computes the source for T=5, k=2, but sets

    target=-D(2)/(pp**D("1.5"))

The exact direct derivation is

    q_2=4p^3,  q'_2=8p^(9/2),  B_2=5-3=2,
    -B_2 q'_2/q_2^2
       = -2*8p^(9/2)/(16p^6)
       = -p^(-3/2).

Thus the correct target is

    target=-D(1)/(pp**D("1.5"))

and the unchanged upstream final assertion is false. The exact formula
-(T-3)/(2p^(3/2)) in the proof, and its stated T=5 specialization, are
correct. The error is confined to the checker's final numerical expected
value; it is not an alternative normalization of Dt.

A separate 80-digit standard-library Decimal computation evaluated the
generic source formula, including its logarithmic bracket, independently:

    B_2(5)                  = 2  (error < 1e-78),
    direct source           = -2.0581710272714922503219810475804504212...,
    corrected target        = -2.0581710272714922503219810475804504212...,
    original target         = -4.1163420545429845006439620951609008425...,
    corrected residual      = 5e-79,
    original residual       = 2.0581710272714922503219810475804504212....

This addendum does not claim the unchanged upstream checker passed. The
native-selector agent owns preservation of its original bytes, reproduction
of the whole-file failure, and any separately labelled corrected replay.
This reviewer changed neither the upstream artifact nor its expectations.
