# EXP-A4D-AFFINE-TRANSLATION-CURVATURE-ACTION-COMPLETION

Class: \`EXPENSIVE\`
State on registration: \`IN_PROGRESS\`
Parent: \`ROOT\`

Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`exp/a4d-affine-translation-curvature-action-completion\`
Primary artifact: \`02_REGISTRY/research/MEMO_A4D_AFFINE_TRANSLATION_CURVATURE_ACTION_COMPLETION.md\`
Execution: \`GitHub-first\`

## Why this is EXPENSIVE

The previous action-completion pressure discovered a uniquely affine-covariant
relative solder but also a large accidental common-edge diagonal kernel.  A
faithful completion therefore needs an additional invariant that detects
nongauge affine-shift curvature.

The owned affine connection already has open torsion and based affine holonomy,
but neither translation component transforms as an ordinary vector on a curved
background.  Whether they admit a local scalar action without a supplied affine
reference point is a genuine invariant-theory question.

## Question

Classify the lowest-locality single-plaquette / single-based-loop full-affine
scalar dependence on translational holonomy.

Use literally:

\[
T'_{rs}(x)
=
g_x T_{rs}(x)
-
F'_{rs}(x)c_{\mathrm{far}},
\]

and for based affine holonomy \(H=(P,t)\),

\[
P'=g_xPg_x^{-1},
\qquad
t'=g_xt+(I-P')c_x.
\]

Determine whether a continuous algebraic/rational local scalar built from the
owned Lorentz metric/orientation, observer, relative solder, \(P\), \(F\),
\(T\), or \(t\) can:

1. be invariant under arbitrary affine node translations;
2. be nontrivially sensitive to translational residual data;
3. vanish on pure node-gauge exact shifts;
4. detect at least one nongauge common-edge/cycle residual.

## KILL-FIRST gates

1. TYPE: distinguish open torsion, based-holonomy shift and residual class
   \([t]\in\mathrm{coker}(I-P)\).
2. REPRESENTATION: classify translation conjugacy orbits
   \(t\sim t+(I-P)c\) for fixed \(P\).
3. MODULI: determine generic/singular ranks of \(I-P\) in
   \(SO^+(1,3)\).
4. CONTINUITY/ALGEBRA: test whether any continuous or polynomial invariant can
   depend on \(t\) across the generic invertible-\(I-P\) stratum.
5. OBSERVER: check whether \(h_n\) changes that conclusion without an affine
   point.
6. OPEN-TORSION: test whether the far-site curvature shift can be cancelled by
   any already-owned same-plaquette datum.
7. EXACT FINITE: use rational proper-Lorentz matrices with both invertible and
   rank-deficient \(I-P\), and explicit affine conjugation witnesses.
8. If single-plaquette terms die, state the minimum surviving next carrier:
   joint/multi-holonomy invariant, supplied affine point/reference, or
   discontinuous rank-stratified quotient datum.

## Hostile controls

- generic loxodromic \(P\) with \(I-P\) invertible;
- pure boost/rotation rank-deficient \(P\);
- \(P=I\) where translation holonomy is an honest vector;
- observer metric present but no affine point;
- polynomial matrix-representation traces;
- no silent pseudoinverse/rank threshold unless declared as discontinuous /
  stratified;
- no identification of open torsion with solder torsion;
- no generic \(T^2\) term unless its affine gauge law is actually invariant.

## Desired terminals

Positive:
\[
\texttt{AFFINE-TRANSLATION-CURVATURE-SCALAR-CONSTRUCTED}
\]

Negative:
\[
\texttt{SINGLE-PLAQUETTE-AFFINE-TRANSLATION-SCALAR-NOGO-IN-CONTINUOUS-CLASS}
\]

with the surviving multi-holonomy/reference boundary stated exactly.

## Scope

Research only. No Lean edits, no claims/release promotion, no BOOK/public edits.
No Einstein/diffeomorphism/torsion-free/time/wave interpretation.

## Lifecycle

Draft before substantive research; self-retire before Ready. Durable memo and
exact certificates remain. Do not self-merge.
