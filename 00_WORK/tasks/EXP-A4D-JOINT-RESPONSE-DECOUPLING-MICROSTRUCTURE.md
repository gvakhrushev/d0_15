# EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `exp/a4d-joint-response-decoupling-microstructure`  
Primary artifact: `02_REGISTRY/research/MEMO_A4D_JOINT_RESPONSE_DECOUPLING_MICROSTRUCTURE.md`  
Execution: `GitHub-first`

## Why delegated

The exact curved nongauge joint-vacuum family in merged #232 destroys connection uniqueness and the C1-compactness route, but has exactly zero metric response on the flat background. The unresolved question is whether such ultraviolet connection moduli remain invisible to the normalized metric Euler response over smooth nonconstant backgrounds, or whether a smooth-background counterexample exists. This requires a response quotient / homogenization or compensated-compactness argument, or an exact hostile sequence; it cannot be settled by another connection compactness or uniqueness proof.

## Runtime / collision gate

Before starting, use current `main`, confirm this row is still `PLANNED`, and search open PRs for this exact task ID. Continue an existing execution if one exists; do not create a duplicate. Pin the launch SHA and the current merged/live state and head of every cited input. Do not recompute delegated results except for narrow consistency checks that the response argument needs.

## Objective

For mesh size `h=1/L`, a fixed smooth nondegenerate background sampled as `Q_h`, the designated smooth comparison branch `K_h^sm` from #216, and exact joint-critical sequences `K_h` satisfying the task's declared connection and metric source equations, determine whether

\[
h^{-2}\left[E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\rm sm})\right]\longrightarrow 0
\]

continues to hold when `K_h` contains curved, nongauge, grid-scale microstructure such as the exact family in #232.

The first page of the memo must make this expression well-typed: specify the finite-site metric-response object, its component convention, the spatial/testing norm or topology in which the limit is asserted, the normalization, the smooth-branch residual/source convention, and all uniformity hypotheses. Do not hide these choices behind pointwise notation.

A comparison of two exact solutions satisfying the identical prescribed metric-source equation makes the displayed difference zero by substitution. Record this as an exact tautological control, not as the requested scientific theorem. The research target is a non-tautological response-decoupling statement relative to the #216 smooth comparison branch, or a counterexample under the same explicitly declared source convention. Keep the geometric Euler response and any matter/source term distinct throughout.

## Required analysis

1. Consume, with launch-time SHA/status pins, #216, #223, #226, #227, #232, and #237. Reuse their owned computations; do not repeat a full symbol census, compactness argument, or connection-uniqueness proof.
2. Treat #232's exact period-four curved nongauge joint vacuum as the mandatory response-null microstructure control. State its curvature/gauge status and its exact `E_Q(eta,K)=0` conclusion. Do not infer its behavior on a nonconstant `Q_h` from the flat identity.
3. Use #226's sensitivity bound only under its actual link-log chart and sum-norm hypotheses; retain its sharp raw exponent `0` and normalized `h^-2` loss. Use #223's normal-coordinate locality only under its smooth/analytic vertex hypotheses. Identify explicitly why neither result controls grid-scale Young measures by itself.
4. Use #227 as the hostile metric-response control: it is exact connection-stationary and curved, has nonzero normalized metric response at its stated scale, but is not thereby a joint-critical metric solution. Explain whether it can or cannot be converted into a valid counterexample to this task.
5. Build and test the proposed response quotient / homogenized description. A Young-measure or compensated-compactness passage must identify the moments/commutators actually controlled by the finite Euler equations and justify passage through the nonlinear metric variation; weak convergence or bounded energy alone is insufficient.
6. Preserve local Lorentz gauge and the genuine nondegenerate solder quotient. Do not call a response-invisible connection direction gauge merely because its metric response vanishes.

## Terminal and stopping rule

Close positively with `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED` only after proving the normalized response convergence for a class that includes the #232 grid-scale microstructure and after stating the precise topology and source/comparator assumptions.

Use `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO` only with a smooth-background sequence that satisfies the declared joint-critical equations, remains in the genuine Lorentz quotient, and has a certified nonzero normalized response gap (liminf or exact limit). A response discrepancy from a merely connection-stationary #227 sequence is not sufficient.

If neither terminal is established, keep the task Draft/Blocked and name the single first missing estimate or exact identity. Do not replace this task with connection compactness, connection uniqueness, an added selector, or a new action term.

## Scope fences

No new action density, Holst term, torsion equation, spectral filter, boundary selector, or connection-selection principle. No Lean-owner edits, claim/release-status promotion, BOOK/public-claim edits, or downstream task creation. Use exact rational/symbolic certificates where they materially support a finite claim; keep finite exact facts, conditional arguments, and open continuum steps separate.

## GitHub execution contract

Start from current `main`; run `python tools/task_lifecycle.py start EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE` as the first task-branch change; open a Draft PR before research edits; write the memo and any task-specific certificate in that PR; run the required exact controls and repository guards; refresh against current `main`; run `python tools/task_lifecycle.py retire EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE` before Ready; set `Lifecycle: REVIEW`; never self-merge.

## Chat handoff

Return the execution PR number, the exact theorem/no-go verdict, the validated response norm and source convention, the certificate/guard results, and the single smallest remaining blocker if the target is not closed.
