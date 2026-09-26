# EXP-A4D-RESOLVED-AFFINE-QUOTIENT-VARIATION

Class: \`EXPENSIVE\`
State on registration: \`IN_PROGRESS\`
Parent: \`ROOT\`

Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`exp/a4d-resolved-affine-quotient-variation\`
Primary artifact: \`02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_QUOTIENT_VARIATION.md\`
Execution: \`GitHub-first\`

## Why delegated

The new gauge-image resolution introduces a Grassmannian incidence datum.
Whether that datum is fixed memory, a constrained endpoint variable or a
history-derived object changes the Euler family.  This is a genuine variational
classification problem and cannot be decided by process convention.

## Research question

For a positive edge metric \(h\), node-gauge image \(J=\operatorname{im}D_L\),
and supplied incidence subspace

\[
J\subseteq\mathcal I\subseteq\mathcal E,
\]

classify the first variation of

\[
E_{\mathcal I}(b)
=
\|P_{\mathcal I^\perp}b\|_h^2
\]

and the combined trial action

\[
S_{\rm trial}
=
\alpha S_{\widehat\star}
+
\beta E_{\mathcal I}.
\]

Compare:

1. frozen \(\mathcal I\);
2. constrained Grassmannian \(\mathcal I\) of fixed rank containing
   \(\operatorname{im}D_L\);
3. history-germ-derived \(\mathcal I\).

## KILL-FIRST gates

1. TYPE: tangent space to the incidence fibre.
2. VARIATION: exact formula for \(\delta E\) under \(\delta b,\delta\mathcal I\).
3. INCIDENCE CONSTRAINT: linearize
   \(\operatorname{im}D_L\subseteq\mathcal I\) under \(\delta L\).
4. FROZEN MEMORY: determine which \(\delta L\) remain admissible if
   \(\delta\mathcal I=0\).
5. GRASSMANNIAN CONTRACT: classify the free incidence tangent and its Euler
   equation.
6. INTRINSIC STRATUM: verify that when
   \(\mathcal I=\operatorname{im}D_L\) and rank is constant, no extra incidence
   degree is present.
7. RESOLVED RANK-DROP STRATUM: classify the extra equations when
   \(\dim\mathcal I>\operatorname{rank}D_L\).
8. HISTORY CONTRACT: decide whether endpoint memory alone determines the
   variational tangent; construct same-endpoint/same-\(\mathcal I\) histories
   with different first incidence tangents if possible.
9. ACTION FAMILY: state only justified \(d_A,d_E,d_P\) consequences.

## Mandatory exact controls

- finite Euclidean projector model for the Grassmannian derivative;
- one intrinsic branch with no free incidence tangent;
- one resolved branch with nonzero lost subspace \(G\);
- explicit \(\delta L\) rejected by frozen-memory variation;
- explicit incidence tangent producing nonzero \(\delta E\);
- same endpoint and same \(\mathcal I_*\) but different incidence tangent
  histories, if history nonreconstruction occurs;
- no pseudoinverse hidden as a global smooth object;
- no Lean edits and no physical interpretation.

## Desired terminals

Preferred classification terminal:
\[
\texttt{RESOLVED-AFFINE-QUOTIENT-VARIATION-CLASSIFIED}.
\]

If endpoint incidence memory is insufficient even to define first variation:
\[
\texttt{FIRST-VARIATION-REQUIRES-INCIDENCE-TANGENT-MEMORY}.
\]

## Scope

Research only. No Lean edits, no claim promotion, no BOOK/public edits.

## GitHub execution contract

Open Draft before durable research edits. Work only in this PR. Before Ready,
record the terminal in the research ledger, self-retire the task, remove this
brief, and run repository guards. Do not self-merge.

## Chat handoff

Return PR link, terminal verdict, exact first-variation formula, whether a new
Euler constraint appears, and the next blocker.
