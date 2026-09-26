# EXP-A4D-AFFINE-RELATIVE-SOLDER-ACTION-COMPLETION

Class: \`EXPENSIVE\`
State on registration: \`IN_PROGRESS\`
Parent: \`ROOT\`

Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`exp/a4d-affine-relative-solder-action-completion\`
Primary artifact: \`02_REGISTRY/research/MEMO_A4D_AFFINE_RELATIVE_SOLDER_ACTION_COMPLETION.md\`
Execution: \`GitHub-first\`

## Why this is EXPENSIVE

The first Cartan-Hodge on-shell rescue class is terminally closed.  The next
question is whether translation symmetry forces an enlarged action and, if so,
whether the smallest enlargement is already latent in the owned independent
affine-shift and observer data.

A positive answer would change the action carrier and reopen d_A -> d_E -> d_P,
so it must be classified rather than guessed.

## Candidate family

For the raw solder row \(\Theta_{x,r}\), affine link shift
\(b_{x,r}\in V_x\), and owned observer form \(h_{n_x}\), classify

\[
\widehat\Theta^{(\lambda)}_{x,r}
=
\Theta_{x,r}
-
\lambda\, b_{x,r}^{T}h_{n_x}.
\]

Use the already-constructed observer-completed full affine solder law and the
owned affine connection gauge law.

The candidate completed density is the same canonical star insertion with the
complementary bivector built from \(\widehat\Theta^{(\lambda)}\), while the
curvature remains the exact odd extraction of the linear plaquette.

## KILL-FIRST gates

1. TYPE: verify target-fibre and row/vector typing.
2. REPRESENTATION: derive the exact full affine transformation of
   \(\widehat\Theta^{(\lambda)}\).
3. SELECTOR: determine whether affine covariance forces a unique \(\lambda\).
4. SYMMETRY: test the complete finite cell density under genuinely
   site-dependent Lorentz + translation gauges.
5. FLAT LIMIT: require exact reduction to the accepted star density at
   \(b=0\), and exact invariance on the owned flat translation-gauge chart.
6. INDEPENDENT SHIFT: a nonzero pure affine shift must remain visible; the
   completion must not identify \(b\) with \(e\) or erase it.
7. ROLE NATURALITY: preserve the already-accepted oriented Role selector.
8. VARIATION/QUOTIENT: state only the d_A/d_E/d_P consequences actually forced
   by the completed action.  Do not import the old Hessian result without
   checking its b=0 specialization.

## Hostile controls

- \(\lambda=0\) recovers the already-failed untranslated action;
- \(\lambda\ne1\) under a curved pure translation;
- site-dependent mixed Lorentz+translation gauge;
- pure nonzero affine shift with \(e=0\);
- exact flat translation gauge with \(e,b\ne0\) but relative solder unchanged;
- independent affine shift and raw solder remain separate inputs;
- no supplied reference section \(q\);
- no Euler/Hessian-dependent repair.

## Desired terminals

Positive:
\[
\texttt{AFFINE-RELATIVE-SOLDER-STAR-COMPLETION-UNIQUE-IN-LAMBDA-CLASS}
\]

Negative:
\[
\texttt{AFFINE-RELATIVE-SOLDER-ACTION-COMPLETION-NOGO}
\]

with the first exact failed gate.

## Scope

Research only.  No Lean source edits, no claims/release promotion, no
BOOK/public edits.  Do not identify the completed action with Einstein gravity,
diffeomorphisms, torsion-free geometry, waves or physical time.

## Lifecycle

Draft PR before substantive research.  Before Ready, self-retire this EXPENSIVE
task from manifest/status and remove this executable brief; retain durable
memo/certificates.

## Handoff

PR number, terminal verdict, exact finite covariance result, and the next
variation/quotient blocker.  Do not self-merge.
