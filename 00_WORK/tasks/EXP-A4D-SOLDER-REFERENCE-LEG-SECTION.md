# EXP-A4D-SOLDER-REFERENCE-LEG-SECTION

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

SATISFIED on current \`main\` after merged PR #112.

The worker

\`WRK-A4D-NILPOTENT-AFFINE-LIFT-GRADING-BOUNDARY\`

may continue in parallel. Do not wait for it.

## Read first

Read completely:

1. \`02_REGISTRY/research/MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH.md\`;
2. \`02_REGISTRY/research/SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md\`;
3. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
4. \`03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean\`;
5. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`;
7. merged PR #109/#110/#111/#112 artifacts.

## Frozen result from PR #112

The literal row/vector ambiguity is closed.

The owned target-site solder vector is

\[
v_r(e,x)=\operatorname{solderLegVector}(e,x,r)\in V_x.
\]

For any supplied source-fibre reference leg

\[
q_r(y)\in V_y,\qquad y=x+r,
\]

the transported-reference mismatch is well typed:

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(q_r(y))-v_r(e,x)
=
b_{x,r}+L_{x,r}q_r(y)-v_r(e,x).
\]

Under the owned pure-linear frame subgroup, if

\[
q'_r(y)=g_yq_r(y),
\]

then

\[
\kappa'_{q}=g_x\kappa_q.
\]

The missing datum is the rule selecting/constructing \(q\).

Do not reopen the row/vector conversion.

## Objective

Construct, classify, or terminally obstruct a **reference-leg / affine-origin section**

\[
q_N(A,e;y,r)\in V_y
\]

that is sufficient to make

\[
\kappa_N(A,e;x,r)
=
A_{x,r}(q_N(A,e;x+r,r))-v_r(e,x)
\]

a function of \((A,e)\) rather than of an independently supplied \(q\).

The task must determine whether \(q\) is:

- derivable from existing \((A,e)\) data;
- selected only after one additional geometric principle;
- intrinsically nonunique;
- better typed as an affine point/origin rather than a vector;
- or impossible to make fully affine-covariant without extending the solder action.

## Mandatory controls

### A. Literal source-site typing

Keep

\[
q_N(A,e;y,r)\in V_y
\]

or, if the correct object is affine rather than linear,

\[
\widehat q_N(A,e;y,r)\in \operatorname{Aff}(V_y).
\]

Do not silently identify a target-site value with a source-site value.

### B. Flat normalization

Require exactly

\[
q(A_{\rm flat},0;y,r)=e_r.
\]

This must imply

\[
\kappa(A_{\rm flat},0;x,r)=0.
\]

### C. Exact translation-gauge specialization

On the exact PR #70 translation-gauge chart,

\[
L=I,\qquad b=d_f\phi,\qquad e=d_f\phi,
\]

require

\[
q(A_\phi,d_f\phi;x+r,r)
=
v_r(d_f\phi,x)-b_{x,r}.
\]

This must give

\[
\kappa(A_\phi,d_f\phi;x,r)=0.
\]

Do not replace this with the noncovariant fixed-coordinate formula unless it is used only as a chart check.

### D. Pure affine-shift control

For

\[
e=0,\qquad L=I,\qquad b\ne0,
\]

the section must **not** absorb the physical affine shift.

Require

\[
\kappa((I,b),0;x,r)\ne0,
\]

preferably exactly

\[
\kappa=b.
\]

This excludes the tautological choice \(q=A^{-1}v\), which would force \(\kappa=0\) on every background.

### E. Pure-linear frame covariance

Under the owned local frame convention,

\[
q(A^g,e^g;y,r)=g_y q(A,e;y,r)
\]

or the exact affine-point analogue must hold.

Then derive

\[
\kappa(A^g,e^g;x,r)=g_x\kappa(A,e;x,r).
\]

Use the exact rational A/B boost.

### F. Full affine gauge question

Audit separately whether \(q\) should transform as an affine point

\[
q'_y=g_yq_y+c_y.
\]

If so, determine what transformation law the target solder leg would need for

\[
A'(q')-v'
\]

to transform homogeneously.

Current repo does not own the inhomogeneous solder law.

Classify whether a **full affine solder/origin action** is genuinely the next primitive, or whether linear-frame covariance plus the exact translation-gauge chart are sufficient.

### G. Test local candidate classes before declaring a primitive

At minimum test:

1. fixed flat reference \(q=e_r\);
2. source solder \(q=v_r(e,y)\);
3. target-predecessor constructions using the unique edge \(x=y-r\);
4. linear combinations of source/target solder legs compatible with frame covariance;
5. one-edge functions using \(A_{x,r}\), \(v_r(e,x)\), \(v_r(e,y)\);
6. affine-point/origin formulations.

Do not use a centered coframe as the only input.

### H. Nonselection audit

If one \(q\) exists, determine whether the mandatory controls select it uniquely.

Look explicitly for deformations

\[
q\mapsto q+z
\]

where \(z\) is frame covariant and vanishes on:

- flat;
- exact pure-gauge controls;

while changing generic curl/harmonic backgrounds.

If such \(z\) exist, classify the surviving family rather than claiming uniqueness.

### I. Path compatibility

Test whether a chosen \(q\) is compatible with labelled path composition.

For consecutive links, determine whether transported origins compose naturally or whether an edge-by-edge \(q\) introduces extra path dependence.

Use the merged labelled-path skeleton. Do not quotient nontrivial holonomy.

### J. Raw-data controls

The section must not erase:

- \(L=2\) raw Nyquist;
- \(L=3\) off-diagonal corner;
- one plaquette curl witness;
- one nonzero harmonic cycle.

These need not make \(\kappa=0\); they must remain distinguishable.

## Important firewalls

Do not:

- start finite graded E dressing;
- identify \(A=A(e)\);
- reintroduce a row→vector map after \`solderLegVector\`;
- choose endpoint weights aesthetically;
- use \(q=A^{-1}v\) as a solution without confronting pure-shift invisibility;
- use \([H,T_b]\) to define \(q\);
- introduce stress, Einstein, physical time, golden/AF refinement.

## Preferred terminals

Positive:

- \`SOLDER-REFERENCE-LEG-SECTION-CONSTRUCTED\`;
- \`AFFINE-SOLDER-ORIGIN-SECTION-CONSTRUCTED\`.

Scoped classification:

- \`SOLDER-REFERENCE-LEG-SECTION-CONSTRUCTED-NONUNIQUE-FAMILY\`;
- \`SOLDER-REFERENCE-LEG-REQUIRES-FULL-AFFINE-SOLDER-ACTION\`;
- \`SOLDER-REFERENCE-LEG-REQUIRES-NEW-GEOMETRIC-SELECTION-PRINCIPLE\`.

Do not claim a universal no-go unless candidate classes are actually exhausted.

## Deliverable

One durable theorem-ready memo with:

1. exact type contract;
2. candidate-class audit;
3. flat theorem;
4. pure-gauge theorem;
5. pure-shift theorem;
6. frame covariance;
7. full-affine boundary;
8. path-composition audit;
9. Nyquist/corner/curl/harmonic controls;
10. uniqueness/nonselection classification;
11. terminal;
12. theorem-ready handoff;
13. exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start EXP-A4D-SOLDER-REFERENCE-LEG-SECTION\`;
3. immediately open Draft PR;
4. research only inside the PR;
5. durable memo;
6. self-retire before Ready;
7. \`Lifecycle: REVIEW\`;
8. do not self-merge.

## Exit condition

A source-fibre reference-leg/affine-origin section is constructed from the available edge data with flat, exact pure-gauge, pure-shift and frame-covariance controls, or the earliest additional full-affine-solder/selection primitive required to choose such a section is terminally identified, with nonuniqueness explicitly classified before finite graded E dressing is allowed to start.
