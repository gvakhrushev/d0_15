# WRK-A4D-AFFINE-ORIGIN-COVARIANCE-BOUNDARY

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the exact **affine-origin covariance boundary** isolated by PR #112.

The research memo observed that a full affine covariance theorem works naturally when both the source reference leg and the target solder leg are treated as affine points:

\[
q'_y=h_y(q_y),\qquad v'_x=h_x(v_x).
\]

Then

\[
A'_{x,r}(q'_y)-v'_x
=
g_x\bigl(A_{x,r}(q_y)-v_x\bigr),
\]

where \(g_x=(h_x).\mathrm{lin}\).

But if \(q\) transforms affinely while the solder leg is transformed only by its current linear law,

\[
v'_x=g_xv_x,
\]

an uncancelled node-translation defect remains.

Formalize this boundary generically. Do not select a physical affine solder law.

## Read first

Read completely:

1. \`02_REGISTRY/research/MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH.md\`, especially §§18–21;
2. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
3. \`03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean\`;
4. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean\`;
5. \`00_WORK/tasks/EXP-A4D-SOLDER-REFERENCE-LEG-SECTION.md\`.

Use current \`main\` at task start.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DAffineOriginSolderBoundary.lean\`

Keep the core theorem generic over \(K,V\) where practical. Specialize to \(K=\mathbb R\), \(V=\mathrm{Role}\to\mathbb R\) only for the D0 edge statement.

## Mandatory theorem package

### 1. Affine conjugation evaluation

For

\[
A'_{xy}=h_xA_{xy}h_y^{-1}
\]

prove directly from the owned affine multiplication/apply laws:

\[
A'_{xy}\bigl(h_y(q)\bigr)
=
h_x\bigl(A_{xy}(q)\bigr).
\]

This is a point-level evaluation theorem, not just a theorem about \`lin\` and \`shift\`.

### 2. Difference of two affine points transforms linearly

For any affine node map \(h=(g,c)\),

\[
h(u)-h(v)=g(u-v).
\]

Make this a reusable theorem for \`AffineCartanMap.apply\`.

### 3. Full affine origin/solder covariance

Combining the two, prove:

if

\[
q'_y=h_y(q_y),\qquad
v'_x=h_x(v_x),
\]

then

\[
A'_{xy}(q'_y)-v'_x
=
(h_x).\mathrm{lin}(A_{xy}(q_y)-v_x).
\]

This is the exact positive theorem behind the affine-point interpretation.

### 4. Linear-only solder defect

Prove the hostile control:

if

\[
q'_y=h_y(q_y)
\]

but

\[
v'_x=(h_x).\mathrm{lin}(v_x),
\]

then

\[
A'_{xy}(q'_y)-v'_x
=
(h_x).\mathrm{lin}(A_{xy}(q_y)-v_x)
+
(h_x).\mathrm{shift}.
\]

The exact sign/convention must follow the repository's \`AffineCartanMap.apply\`.

### 5. Pure translation witness

Specialize \(h_x=(I,c_x)\).

Show that the linear-only solder law leaves the exact residual

\[
c_x.
\]

Give a concrete nonzero Role-basis witness.

### 6. Pure-linear subgroup recovery

If

\[
(h_x).\mathrm{shift}=0,
\]

the defect theorem must reduce to homogeneous vector covariance.

This is the Lean boundary matching PR #112's pure-linear frame result.

### 7. Separation from current raw solder owner

State/prove a scoped theorem or typed corollary showing:

the existing \`rawFullSolderFrameAction\` supplies a **linear right-frame action** on the raw solder matrix; it does not by itself provide the affine translation term needed by theorem 3.

Do not encode this as a universal no-go. A theorem with explicit hypotheses is preferred.

## Optional if straightforward

Add an abstract interface structure for a future affine solder/origin action, containing:

- affine-point transformation law for target solder legs;
- affine-point transformation law for source reference legs.

Do not instantiate it physically in this worker.

## Scope firewalls

Do not:

- claim D0 already owns a full affine solder action;
- choose \(q(A,e)\);
- identify the solder perturbation with an affine point without an explicit new structure;
- start finite E dressing;
- infer uniqueness;
- use centered solder as replacement for raw solder;
- touch stress, Einstein, physical time or golden refinement.

## Exit condition

Lean owns the exact algebraic fact that full affine covariance of the transported-reference mismatch requires matching affine-point transformation of both reference and solder legs, while a linear-only solder law leaves the explicit node-translation defect.

This worker must leave the research question “should D0 adopt such an affine solder/origin structure?” open for \`EXP-A4D-SOLDER-REFERENCE-LEG-SECTION\`.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start WRK-A4D-AFFINE-ORIGIN-COVARIANCE-BOUNDARY\`;
3. open Draft PR immediately;
4. implement only this boundary;
5. narrow builds during development;
6. one incremental \`lake build D0.All\` before Ready;
7. register support/imports through canonical generators;
8. self-retire task;
9. PR body \`Lifecycle: REVIEW\`;
10. Ready for review;
11. do not self-merge.

No \`sorry\`. No new axioms. Do not run \`lake clean\`.
