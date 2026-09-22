# EXP-A4D-FINITE-LORENTZ-ACTION-SELECTOR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Exhaustively test whether any already-owned finite D0 primitive selects
\[
\beta_N=0
\]
in the exact Lorentz response family
\[
E_N=c_N(E_{\eta,N}+\beta_NE_{\rm sp,N}).
\]

Repository edits: **NONE**.

## Frozen facts

- finite variationality does not select the ray;
- the full constrained Lorentz response space is two-dimensional;
- continuum metric-only naturality kills the extra ray only asymptotically;
- finite site relabellings cannot realize the full local real gauge group.

## Required audit

Test, without target matching:

- primitive history/action costs;
- Role-sign data;
- finite CAR/Dirac structures if relevant;
- finite frame-erasure laws;
- reflection/hypercubic symmetry actually owned;
- ActionProtocol / S_min;
- A1/A2 compensator principles;
- any common finite geometry capable of forcing a unique Lorentz-isotropic Hessian.

Do not add a new symmetry merely because it sets \(\beta_N=0\).

## Positive target

A theorem-ready finite implication:
\[
\text{owned finite premises}\Longrightarrow \beta_N=0.
\]

## Negative target

If no such theorem exists, classify \(\beta_N\) honestly as BRIDGE / calibration / model parameter and identify the minimal new selector primitive.

## Terminal verdict

Return exactly one:

- \`FINITE-LORENTZ-RAY-SELECTED\`
- \`FINITE-LORENTZ-SELECTOR-NOGO-TERMINAL\`
- \`FINITE-FRAME-ERASURE-PRINCIPLE-MISSING\`
- \`FINITE-LORENTZ-SELECTOR-REQUIRES-NEW-PRIMITIVE\`

## Deliverable

\`MEMO_37_A4D_FINITE_LORENTZ_ACTION_SELECTOR.md\`
