# WRK-A4D-Y-SLOW-JOINT-CONTINUATION

Class: \`WORKER\`  
State on registration: \`PLANNED\`  
Parent: \`CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE\`  
Research lane: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`

Repository: \`gvakhrushev/d0_15\`  
Base: \`main\`  
Branch: \`wrk/a4d-y-slow-joint-continuation\`  
Primary artifact: \`02_REGISTRY/research/A4D_Y_SLOW_JOINT_CONTINUATION.md\`  
Execution: \`GitHub-first\`

## Dependency

Consume only merged owners:

- #232 / \`A4D_JOINT_PALATINI_LOCAL_UNIQUENESS\`: exact curved nongauge Y-family at flat metric;
- #241 / \`A4D_DIAGONAL_MICROSTRUCTURE_SLOW_BACKGROUND_RESPONSE\`: raw slow-background response obstruction;
- #259 / \`A4D_DIAGONAL_MICROSTRUCTURE_CONNECTION_STATIONARY_SLOW_LIFT\`: exact order-h connection-stationary correction that cancels the #241 order-h metric response;
- #270 / \`A4D_METRIC_NULL_HESSIAN_COMPLEX\`: exact metric-null transport;
- #273 / \`A4D_SCHUR_EINSTEIN_DIRECT_IDENTIFICATION\`: direct flat Schur symbol \`K_Schur=-1/2 K_G^(1)\`.

Do not consume live #240 calculations as theorem inputs except for comparison after the worker result is complete.

## Why delegated

The raw #241 pointwise normalized obstruction at \`z_h=h\` disappears after the exact #259 connection-stationary lift. The first unresolved question is now one order higher and is bounded: does the same explicit Y carrier admit the next connection correction without generating an order-h^2 response defect that survives the final h^-2 normalization?

This is narrower than #240's global homogenization problem and can be decided by finite exact Taylor/Fredholm algebra.

## Objective

Use the exact #232 Y family on the exact #241/#259 valued slow background

\[
Q_h=\eta+h\alpha+h^2x_0\beta,
\qquad
\alpha=E_{12}+E_{21},
\quad
\beta=E_{01}+E_{10},
\]

with the #259 order-h link correction already fixed.

Continue the connection Euler equation through the first unresolved order and then recompute the metric Euler response from the same corrected link jet.

Primary scaling:

\[
z_h=h.
\]

The \`z_h=h^2\` control may be retained, but must not replace the \`z_h=h\` target.

## Required gates

1. Reproduce #232 flat exact stationarity and #259 order-h forcing/lift exactly.
2. Expand the literal all-edge connection Euler through order \`h^2\` after the #259 lift.
3. Form the exact linear operator for the next link correction and compute its rank, right kernel and left/Fredholm kernel on the declared period-4 carrier.
4. Project the order-h^2 forcing to the left kernel:
   - if nonzero, publish the exact first obstruction coefficient and stop;
   - if zero, solve one canonical range correction and record the residual freedom.
5. Recompute the ten-component metric Euler from the same corrected link jet through the first order capable of surviving \`h^-2\` at \`z=h\`.
6. Test the exact factorization target
   \[
   \Delta E_Q=h^2z\,R(h,z,x_0)
   \]
   (componentwise on the declared carrier) or give the exact component/coefficient where it fails.
7. At \`z=h\`, certify either
   \[
   h^{-2}\Delta E_Q=O(h)\to0
   \]
   on this corrected branch, or the exact nonzero normalized leading term.
8. Separate metric-null transport from connection correction. A raw fixed-vector character detune is not an obstruction after #270.
9. Compare the surviving low-frequency metric component, if any, against the #273 standard Schur/Einstein quotient. Do not infer a nonlinear Einstein theorem from agreement of one Taylor coefficient.
10. Keep the source contract honest: this worker constructs a higher-order connection-stationary lift. It does not call it an exact same-source joint solution unless the metric equation is also solved to the claimed order.

## Preferred terminals

Positive:
\`J2-Y-SLOW-CONNECTION-STATIONARY-RESPONSE-FACTOR-PERSISTS\`

Negative:
\`J2-Y-SLOW-NEXT-ORDER-FREDHOLM-RESPONSE-OBSTRUCTION\`

A partial terminal must identify the first unresolved order and the exact missing map.

## Collision fence

Do not modify #240's primary memo or its shear/chain census certificates. This worker owns only the explicit #232 Y carrier on the #241/#259 slow profile and its next-order correction.

Do not reopen:
- FUGU fixed-q detune A/B tables;
- the finite affine/coframe quotient;
- local uniqueness;
- \`E_sp\`;
- the period-2 shear/chain \`-432\` branch.

## Forbidden

No new action term, Holst term, torsion constraint, \(\varphi\), boundary selector, Fourier cutoff, or fitted source. No BOOK/claim promotion. No declaration that finite coframe directions are exact diffeomorphism gauge.

## GitHub execution contract

Open a Draft PR before substantive science edits. Keep all arithmetic exact. Publish the checker under \`02_REGISTRY/research/certificates/\`. Self-retire the task only at a stated terminal and never self-merge.

## Chat handoff

Return the PR link, head SHA, exact terminal, order-h^2 connection forcing projection, rank/kernel data of the correction operator, the solved correction or obstruction coefficient, the corrected metric-response factorization, the \`z=h\` normalized limit, and the exact certificate command.
