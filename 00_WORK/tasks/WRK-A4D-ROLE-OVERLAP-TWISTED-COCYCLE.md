# WRK-A4D-ROLE-OVERLAP-TWISTED-COCYCLE

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own theorem-ready overlap algebra from PR #117.

This worker formalizes only the algebraic relation between a supplied reference
section \(q\), solder legs \(v\), diagonal overlaps \(\delta\), and Role-labelled
overlaps \(\Omega\).

It does not choose the diagonal law.

## Read first

- \`02_REGISTRY/research/MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md\`;
- \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`;
- \`03_FORMALIZATION/D0/Geometry/A4DReferenceJunctionCompressionBoundary.lean\`;
- raw solder/frame owners.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DRoleOverlapTwistedCocycle.lean\`

## Mandatory definitions

For a supplied Role-labelled reference field \(q\), define at one site

\[
\delta_r=q_r-v_r,
\qquad
\Omega_{rs}=q_r-v_s.
\]

## Mandatory theorems

### 1. Overlap decomposition

\[
\Omega_{rs}=v_r-v_s+\delta_r.
\]

### 2. Solder-difference compatibility

\[
\Omega_{rs}-\Omega_{rt}=v_t-v_s.
\]

### 3. Twisted Role cocycle

\[
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
\]

### 4. Diagonal identity

\[
\Omega_{rr}=\delta_r.
\]

### 5. Strict-cocycle obstruction

If the ordinary cocycle

\[
\Omega_{rs}+\Omega_{st}=\Omega_{rt}
\]

holds for all labels, prove

\[
\delta_s=0
\]

and hence

\[
q_s=v_s.
\]

Keep the conclusion scoped: the ordinary cocycle is too strong for a generic
nonzero diagonal overlap.

### 6. Reference reconstruction

For any \(s\),

\[
q_r=v_s+\Omega_{rs}.
\]

Prove independence of \(s\) from solder-difference compatibility.

### 7. Mismatch in diagonal variables

For \(y=x+r\), prove

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(v_r(e,y))-v_r(e,x)
+
L_{x,r}\delta_r(y).
\]

Reuse \`A4DTransportedReferenceMismatch\`.

### 8. Minimum primitive statement

Package a theorem/structure-level equivalence showing that once the off-diagonal
solder-difference law is fixed, the overlap field is determined by its
diagonal \(\delta_r\).

Do not claim the repo selects that diagonal.

## Optional

If short, package the transported junction variable

\[
J_{rs}=L_r\Omega_{rs}
\]

and relate it to the PR #118 junction defect.

## Firewalls

Do not:

- choose \(\delta(A,e,n)\);
- impose the ordinary cocycle physically;
- start finite E dressing;
- quotient labelled holonomy;
- infer \(A=A(e)\);
- touch stress/time/golden work.

## Exit condition

Lean owns overlap decomposition, solder-difference compatibility, the twisted
Role cocycle, strict-cocycle obstruction, reconstruction of \(q\), and the
diagonal-overlap form of the conditional mismatch, while the physical diagonal
selection law remains open.

## GitHub-first flow

Fresh main → lifecycle start → Draft PR → narrow build → incremental
\`D0.All\` → support registration → self-retire → \`Lifecycle: REVIEW\` →
Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
