# WRK-A4D-ACTIVE-SPAN-EXTENSION-INDEPENDENCE

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the theorem-ready claim that **full-fibre extension freedom of the
relative A/e comparison is physically irrelevant to the already-owned sourced
diagonal chain**.

This worker is a pressure test against the accidental assumption that
\(\operatorname{rank}\mathcal B=4\) is required merely because a full
endomorphism is convenient.

## Start inputs

Use the then-current merged owners when available:

- \`A4DRelativeAEComparisonSpan\` from PR #126;
- \`A4DConditionalSourcedDiagonalTransport\` from PR #125.

If either PR is still open at task start, use its reviewed head only for
development and rebase/reconcile onto merged \`main\` before Ready.

Do not duplicate either module.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DActiveSpanExtensionIndependence.lean\`

## Setup

Let

\[
U\le V
\]

be the active affine-increment span and let

\[
J_1,J_2:V\to V
\]

be two full extensions satisfying

\[
J_1|_U=J_2|_U.
\]

Every actual increment obeys

\[
\Delta b_r\in U.
\]

## Mandatory theorems

### 1. Generator action independence

For every Role,

\[
J_1\Delta b_r=J_2\Delta b_r.
\]

### 2. Relative-defect independence

\[
\Delta v_r-J_1\Delta b_r
=
\Delta v_r-J_2\Delta b_r.
\]

### 3. Seed independence

For the PR #120 / #125 seed,

\[
a_r(J_1)=a_r(J_2).
\]

### 4. Predecessor-decomposition independence

The exact predecessor defect decomposition is identical for both extensions.

### 5. Path-source independence

For every labelled path,

\[
S_p(J_1)=S_p(J_2).
\]

### 6. Sourced-solution-space independence

The equation

\[
P_p\delta(y')-\delta(y)=S_p
\]

has exactly the same solution set for \(J_1\) and \(J_2\).

### 7. Mismatch independence

Where the selected \(\delta\) is supplied, the resulting conditional
\(\kappa\) is identical.

### 8. Quotient statement

Package the result as:

the downstream sourced-diagonal construction factors through the restriction

\[
J|_U,
\]

or equivalently through the quotient of full endomorphisms by maps vanishing
on \(U\).

### 9. Full-rank corollary

If \(U=V\), extension freedom vanishes.

State this as a stronger identifiability condition, not as a physical
requirement.

### 10. Rank-deficient exact witness

Give a rank-one or rank-zero witness with two distinct full extensions that
produce identical downstream sourced data.

This is mandatory.

## Firewalls

Do not:

- choose a new \(J\);
- claim full rank is unnecessary for every future observable;
- extend the theorem beyond the already-owned sourced-diagonal chain;
- start finite \(F\);
- identify \(A=A(e)\);
- touch stress/time/golden work.

## Exit condition

Lean proves that all currently owned sourced-diagonal observables and equations
depend only on the active-span restriction of the relative A/e comparison,
with an explicit rank-deficient witness showing distinct full extensions give
identical downstream data.

## GitHub-first flow

Fresh current main or reviewed dependency heads → Draft PR immediately →
narrow build → incremental \`D0.All\` → support registration → self-retire →
\`Lifecycle: REVIEW\` → Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
