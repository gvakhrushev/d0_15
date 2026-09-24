# EXP-A4D-SOLDER-CARTAN-EDGE-MISMATCH

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

SATISFIED on current main after merged PR #109/#110/#111.

The worker

\`WRK-A4D-NILPOTENT-AFFINE-LIFT-GRADING-BOUNDARY\`

may run in parallel. Do not wait for it; treat the PR #109 affine representation as theorem-ready until the worker lands.

## Read first

Read completely, in this order:

1. \`02_REGISTRY/research/SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md\`;
2. \`02_REGISTRY/research/MEMO_A4D_AFFINE_SENSITIVE_SITE_MATTER_LINK.md\`;
3. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
4. \`03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean\`;
5. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean\`;
7. \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean\`;
8. \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`;
9. \`02_REGISTRY/research/MEMO_A4D_CROSSED_CONSTITUTIVE_REPRESENTATION.md\`.

## Updated thesis

Do not search for another affine matter representation.

PR #109 already constructs an exact site-aware affine translation response.

The missing object is the **covariant comparison between the affine translation leg and the raw solder/coframe leg on the same archive edge**.

Use the notation

\[
\kappa_N(A,e;x,r)\in V_x
\]

only as a candidate packaging.

Current ownership forces the need for such a comparison law, but does not yet prove that every successful matter letter must factor through a unique vector-valued \(\kappa\).

## Objective

Construct or terminally classify the earliest solder–Cartan edge comparison that simultaneously explains:

\[
\kappa(A_{\rm flat},0)=0,
\]

\[
\kappa(A_\phi,d_f\phi)=0
\]

on the exact joint pure-gauge orbit,

\[
\kappa((I,b),0)\ne0
\]

for nonzero pure affine shift, and target-fibre frame covariance.

The task is about **one edge and its two already-owned descriptions**.

It must keep \(A\) and \(e\) independent.

## Mandatory attack

### A. Audit the literal types before proposing a formula

Write the exact repository types and conventions for:

- affine shift \((A x r).shift\);
- affine linear pull \((A x r).lin\);
- raw coframe row \(e(x,r,\cdot)\);
- \`rawSolderMatrix\`;
- \`solderLegVector\`;
- \`archiveRoleBasis r\`;
- local frame matrix/right action;
- affine node-gauge linear action.

Determine explicitly which objects are rows, covectors, vectors, target-fibre values and source-fibre values.

Do not use \(b=e_r\) after a frame change unless the type conversion is proved.

### B. Test the transported-reference-leg hypothesis

The first candidate to test is not the flat subtraction \(b-e_r\).

Let

\[
v_r(e,x)=\operatorname{solderLegVector}(e,x,r).
\]

Introduce only if needed a source-fibre reference leg \(q_r(x+r)\) and test

\[
\sigma_q(A,e;x,r)
=
v_r(e,x)-L_{x,r}q_r(x+r).
\]

Audit whether a candidate of the form

\[
\kappa=b-\iota(\sigma_q)
\]

can satisfy the required controls, where \(\iota\) is **not** assumed: derive the necessary row/vector or metric identification from literal repository conventions.

If \(\iota\) is identity in the correct typed convention, prove it.

If a metric raise/lower is required, state it exactly.

If no canonical \(\iota\) exists, that is a possible terminal.

### C. Flat normalization

Require exactly:

\[
\kappa(A_{\rm flat},0;x,r)=0.
\]

This must be a theorem of the candidate formula, not a normalization inserted afterward.

### D. Exact joint pure-gauge diagonal

Use the owned exact identity

\[
(\operatorname{affineGauge}(\operatorname{translationGauge}\phi)A_{\rm flat})(x,r).shift
=
d_f\phi(x,r)
\]

in the repository's literal convention.

Determine whether the same converted solder displacement equals this affine shift.

Require:

\[
\kappa(A_\phi,d_f\phi;x,r)=0.
\]

If it fails because of a row/vector/sign/reference mismatch, isolate the precise missing map.

### E. Pure affine-shift visibility

At \(e=0\), \(L=I\), and \(b\ne0\), require:

\[
\kappa((I,b),0;x,r)\ne0.
\]

Use an exact finite witness.

### F. Target-fibre frame covariance

Derive the exact transformation law under the owned local frame conventions.

The desired form is schematically

\[
\kappa(A^h,e^h;x,r)
=
h_x^{\rm lin}\kappa(A,e;x,r),
\]

but only state this exact equation after proving that the chosen solder/reference leg transforms in the same target fibre.

The research must reconcile:

- \`rawFullSolderFrameAction\`;
- \`solderLegVector\`;
- \`affineGauge_lin\`;
- the linear part of \`affineGauge_shift\`.

A rational A/B Lorentz boost is mandatory as an exact control.

### G. Separate linear-frame covariance from affine translation gauge

Current repo owns a linear/local frame law for the raw solder and a separate affine node-gauge law for \(A\).

Do not pretend a full affine action on raw \(e\) is already owned.

If the mismatch can be frame covariant and pure-gauge normalized without a full affine action on \(e\), state that scope.

If full affine covariance is required, identify the exact missing transformation law as a terminal primitive.

### H. Endpoint/reference freedom

Classify whether the comparison requires:

- target-site reference leg only;
- source-site reference leg transported by \(L\);
- an endpoint average;
- a pair of endpoint legs;
- an independent reference-leg section.

Do not choose endpoint weights by aesthetics.

Use L=2 Nyquist and L=3 corner/path controls to reject any comparison that silently centers away raw data required by \(H(e)\).

### I. Interaction with the nilpotent affine matter response

Once a candidate \(\kappa\) exists, insert it only into

\[
T_{\kappa}.
\]

Check:

- flat: \(T_\kappa=I\);
- pure gauge diagonal: \(T_\kappa=I\);
- pure shift: \(T_\kappa=T_b\) or the precisely derived equivalent;
- Lorentz/frame covariance of \(T_\kappa\).

Do not attempt the arbitrary-background finite E dressing in this task.

### J. Commutator firewall

Explicitly verify the algebraic correction:

\[
[I,T_b]=0.
\]

Do not use \([H,T_b]\) as a mechanism for eliminating the degree-mixing B response.

The mixed commutator may be recorded only as a downstream diagnostic after the mismatch is typed.

### K. No false uniqueness

Even if one valid \(\kappa\) is constructed, test whether the four controls uniquely select it.

If a family of covariant mismatch laws survives, classify that freedom.

Do not upgrade one convenient formula to uniqueness without proof.

## Hostile controls

At minimum use:

- flat \(A_{\rm flat},e=0\);
- exact pure translation gauge orbit;
- nonzero pure affine shift at \(e=0\);
- exact rational A/B Lorentz boost;
- one varying-frame endpoint pair if needed;
- L=2 raw Nyquist;
- L=3 mixed corner;
- one plaquette/curl background;
- one harmonic/cycle background.

The last two need not make \(\kappa\) vanish; they test that the comparison does not silently quotient away path-resolved data.

## Truth firewall

Do not:

- set \(A=A(e)\);
- assume \(b=e_r\) as a frame-covariant identity;
- identify \(W_{\rm flux}\) with a group action;
- assert \(D\mathcal F=H\);
- search for stress/Einstein/time/golden data;
- open a second-jet selector;
- use the mixed commutator to bypass the mismatch.

## Allowed terminals

Preferred positive:

- \`SOLDER-CARTAN-EDGE-MISMATCH-CONSTRUCTED-TARGET-FIBRE-COVARIANT\`.

Scoped terminals:

- \`SOLDER-CARTAN-MISMATCH-REQUIRES-REFERENCE-LEG-SECTION\`;
- \`SOLDER-CARTAN-MISMATCH-REQUIRES-ROW-VECTOR-COMPARISON-PRIMITIVE\`;
- \`SOLDER-CARTAN-MISMATCH-REQUIRES-FULL-AFFINE-SOLDER-ACTION\`;
- \`SOLDER-CARTAN-MISMATCH-CONSTRUCTED-NONUNIQUE-FAMILY\`.

Use only the strongest wording actually derived.

## Deliverable

One durable theorem-ready memo containing:

1. exact type audit;
2. transported-reference-leg calculation;
3. flat theorem;
4. exact pure-gauge theorem or precise obstruction;
5. pure-shift witness;
6. exact frame law;
7. rational boost control;
8. L=2/L=3 controls;
9. endpoint/reference freedom classification;
10. interaction with \(T_\kappa\);
11. terminal;
12. theorem-ready handoff;
13. exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start EXP-A4D-SOLDER-CARTAN-EDGE-MISMATCH\`;
3. immediately open Draft PR before research edits;
4. research and durable memo only inside the PR;
5. before Ready self-retire task;
6. set \`Lifecycle: REVIEW\`;
7. Ready;
8. do not self-merge.

## Exit condition

The independent affine translation and raw solder/coframe descriptions of one Role edge are either joined by an explicit target-fibre covariant mismatch law satisfying flat, exact pure-gauge and pure-shift controls, or the earliest additional reference-leg/index/full-affine-solder datum required for such a comparison is terminally identified without reopening affine representability or finite E dressing.
