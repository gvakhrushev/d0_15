# EXP-A4D-AFFINE-GAUGE-IMAGE-RESOLUTION-MEMORY

Class: \`EXPENSIVE\`
State on registration: \`IN_PROGRESS\`
Parent: \`ROOT\`

Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`exp/a4d-affine-gauge-image-resolution-memory\`
Primary artifact: \`02_REGISTRY/research/MEMO_A4D_AFFINE_GAUGE_IMAGE_RESOLUTION_MEMORY.md\`
Execution: \`GitHub-first\`

## Why delegated

This is a genuine rank-stratified invariant-theory problem.  The answer is not
known in advance: the already-landed A/e resolution memory may or may not be
sufficient for the rank-changing affine node-gauge quotient, and the minimum
extra memory must be classified rather than guessed.

## Research question

For fixed linear links \(L\), let

\[
D_L:C^0(X,V)\to C^1_+(X,V),
\qquad
(D_Lc)_{x,r}=c_x-L_{x,r}c_{x+r}.
\]

The physical affine-shift quotient is

\[
Q_L=C^1_+(X,V)/\operatorname{im}D_L.
\]

Across the flat-to-curved seam, \(\operatorname{rank}D_L\) changes.  Classify
the exact finite resolution needed for this quotient.

In particular compare it to the landed PR #135 structural memory

\[
\Xi_{\rm str}=((W_y)_y,\mathcal K).
\]

## KILL-FIRST gates

1. TYPE: distinguish node-gauge kernel memory from gauge-image memory.
2. REPRESENTATION: derive frame/Role/site covariance of \(D_L\), its image,
   quotient and any resolution datum.
3. SUFFICIENCY: test whether \(\Xi_{\rm str}\) determines the limiting
   gauge-image subspace at a rank transition.
4. HOSTILE APPROACHES: construct two Lorentz-Cayley approaches to the same
   flat endpoint with the same \(\Xi_{\rm str}\) but different limiting
   gauge-image directions, or prove impossible.
5. MINIMAL RESOLUTION: if needed, classify the image-incidence datum
   \[
   \mathcal I_*\supseteq\operatorname{im}D_{L_0}
   \]
   or its quotient-space equivalent.
6. RESOLVED QUOTIENT: construct the finite quotient/action carrier on supplied
   resolution memory and prove exact gauge invariance.
7. FLAT/GENERIC COUNTS: reproduce the L=2 ranks
   \(60/196\) at flat and \(64/192\) on generic curved backgrounds.
8. CONTINUITY: separate intrinsic flat quotient from generic-limit resolved
   quotients.  Do not erase this distinction by declaring orbit closure to be
   gauge without an explicit choice.
9. ACTION BOUNDARY: state what a positive quadratic action can use, but do not
   select coefficients or claim \(d_E,d_P\) before variation.

## Mandatory controls

- exact flat \(L=I\);
- rational proper-Lorentz Cayley paths to \(I\);
- at least two same-endpoint approaches with identical PR #135 memory;
- exact rank of \(D_L\), augmented/lost image spaces and quotient dimensions;
- frame covariance;
- intrinsic versus maximal/resolved flat lifts;
- no supplied affine point;
- no pseudoinverse hidden as a continuous pointwise object;
- no Einstein/diffeomorphism/time/wave interpretation.

## Desired terminals

Positive new-resolution terminal:
\[
\texttt{AFFINE-GAUGE-IMAGE-RESOLUTION-CONSTRUCTED}.
\]

If PR #135 already suffices:
\[
\texttt{EXISTING-RESOLUTION-MEMORY-SUFFICES-FOR-AFFINE-QUOTIENT}.
\]

If no finite structural resolution of the stated class is enough, return the
first exact obstruction.

## Scope

Research only. No Lean edits, no claim promotion, no BOOK/public edits.

## GitHub execution contract

Work only on this branch/PR.  Open Draft before durable research edits.
Keep exact witnesses and certificates under \`02_REGISTRY/research/\`.
Before Ready, record the terminal in the research ledger, self-retire this
task from manifest/status, delete this brief, set PR lifecycle to REVIEW, and
run repository guards.  Do not self-merge.

## Chat handoff

Return only the PR number/link, terminal verdict, exact rank/minimality result,
and the next blocker after Ready.
