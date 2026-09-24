# WRK-A4D-REFERENCE-JUNCTION-COMPRESSION-BOUNDARY

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the exact two-link reference-junction identity from PR #114 and the
precise iff criterion for compressing two conditional edge mismatches to one
endpoint-origin mismatch.

This is theorem-ready algebra.  Do not invent the missing selector \(q\).

## Read first

- \`02_REGISTRY/research/MEMO_A4D_SOLDER_REFERENCE_LEG_SECTION.md\`, especially the path-composition section;
- \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
- \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DReferenceJunctionCompressionBoundary.lean\`

Keep the main algebra generic over a field \(K\) and vector space \(V\) if
practical.

## Mandatory theorem package

For affine maps

\[
A_1=(L_1,b_1),\qquad A_2=(L_2,b_2),
\]

references \(q_1,q_2\), and target legs \(v_1,v_2\), define

\[
\kappa_1=A_1(q_1)-v_1,\qquad
\kappa_2=A_2(q_2)-v_2.
\]

### 1. Exact junction identity

Prove literally

\[
\kappa_1+L_1\kappa_2
=
(A_1A_2)(q_2)-v_1+L_1(q_1-v_2).
\]

Use the repository affine multiplication/apply convention.

### 2. Telescoping sufficient condition

If

\[
q_1=v_2,
\]

prove

\[
\kappa_1+L_1\kappa_2
=
(A_1A_2)(q_2)-v_1.
\]

### 3. Exact iff compression criterion

Because \(L_1\) is a linear equivalence, prove

\[
\kappa_1+L_1\kappa_2=(A_1A_2)(q_2)-v_1
\iff
q_1=v_2.
\]

This is the main boundary.

### 4. Mixed-Role flat witness

Give an exact Role-space witness with two distinct Roles \(r\ne s\):

\[
A_1=A_2=I,\quad
q_1=v_1=e_r,\quad
q_2=v_2=e_s.
\]

Then

\[
\kappa_1=\kappa_2=0
\]

but

\[
q_1-v_2=e_r-e_s\ne0.
\]

Show explicitly that the endpoint term and junction defect cancel.

This demonstrates why zero edge mismatch does not imply naive endpoint-origin
compression across a mixed labelled junction.

### 5. Optional n-link induction

If short, derive the finite path expansion as endpoint term plus transported
sum of junction defects.  Do not build a new path evaluator if the existing
one can be reused.

## Firewalls

Do not:

- select \(q(A,e)\);
- impose \(q_1=v_2\) as a physical law;
- claim endpoint compression generally holds;
- start finite E dressing;
- quotient labelled holonomy;
- touch stress/time/golden work.

## Exit condition

Lean owns the exact two-link junction identity, endpoint-compression iff
criterion, and a mixed-Role flat witness showing why the additional junction
condition is non-generic.

## GitHub-first flow

Fresh branch → lifecycle start → Draft PR immediately → narrow build →
incremental \`D0.All\` → support registration → self-retire → \`Lifecycle:
REVIEW\` → Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
