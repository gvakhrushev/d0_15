# WRK-A4D-REGULAR-AE-PASSPORT

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the **regular nondegenerate relative A/e passport** isolated by PR #120.

This is a positive theorem on an explicitly restricted invertible branch.

It is not a global selector and must not be presented as one.

## Read first

- \`02_REGISTRY/research/MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW.md\`,
  §§30–31 and theorem-ready L;
- raw solder matrix / solder-leg owners;
- affine Cartan shift/link owners;
- exact Lorentz metric \(\eta\) conventions.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DRegularAEPassport.lean\`

A matrix-level theorem over \(4\times4\) real matrices is acceptable and
preferred if it cleanly captures the owned geometry.

## Mandatory definitions

Define/identify:

\[
B_e(x)e_s=v_s(e,x),
\]

\[
C_A(x)e_s=b_{x,s}.
\]

On the branch with invertible \(B_e\), define

\[
K=B_e^{-1}C_A.
\]

For the translation chart use

\[
B=I+\eta D,\qquad C=D.
\]

Define the reconstruction operator

\[
\mathcal L_K(X)=X-\eta XK.
\]

## Mandatory theorem package

### 1. Pure-linear transformation

Under

\[
B'_e=gB_e,\qquad C'_A=gC_A,
\]

prove

\[
K'=K.
\]

This is literal frame invariance of the regular passport.

### 2. Translation-chart identity

Assuming

\[
B=I+\eta D,\qquad C=D,\qquad K=B^{-1}C,
\]

prove

\[
D-\eta DK=K.
\]

### 3. Equivalent B-hat identity

Prove the equivalent form

\[
B-\eta BK=I.
\]

Use the repository sign/convention literally.

### 4. Reconstruction uniqueness

If

\[
\mathcal L_K
\]

is injective/invertible, prove that the equation

\[
X-\eta XK=K
\]

has at most/exactly one solution, and identify it with \(D\).

### 5. Explicit regularity boundary

Package the assumptions separately:

- \(B_e\) invertible;
- \(\mathcal L_K\) invertible.

Do not bury them in simplification.

### 6. Singular-locus firewall

State/prove a scoped theorem that the regular passport construction is
undefined or non-unique outside those hypotheses.

Do not claim the singular locus is physically excluded.

### 7. Optional vectorization

If existing APIs make it short, prove that the matrix of
\(\mathcal L_K\) under vectorization is

\[
I-K^T\otimes\eta.
\]

Do not block the task on this optional statement.

## Exact controls

Include at least:

- flat \(D=0\Rightarrow K=0\);
- one nonzero rational/small exact \(D\) example where all regularity
  assumptions hold;
- one explicit singular \(K\) example if easy.

## Scope firewalls

Do not:

- extend \(K=B^{-1}C\) across singular \(B\) by fiat;
- choose a generalized inverse;
- claim a global \(\mathfrak J\);
- use observer \(h_n\) to patch singularity;
- start finite E dressing;
- infer \(A=A(e)\);
- touch stress/time/golden work.

## Exit condition

Lean owns the frame-invariant regular passport \(K=B^{-1}C\), the exact
translation-chart reconstruction equations, and the explicit invertibility
boundary under which the representative is unique, while the singular/
degenerate extension remains open for the heavy research task.

## GitHub-first flow

Fresh main → lifecycle start → Draft PR → narrow build → incremental
\`D0.All\` → support registration → self-retire → \`Lifecycle: REVIEW\` →
Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
