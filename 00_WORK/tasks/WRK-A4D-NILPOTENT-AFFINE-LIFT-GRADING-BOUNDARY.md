# WRK-A4D-NILPOTENT-AFFINE-LIFT-GRADING-BOUNDARY

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

SATISFIED on current main after merged PR #109/#110/#111.

Read completely:

- \`02_REGISTRY/research/SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md\`;
- \`02_REGISTRY/research/MEMO_A4D_AFFINE_SENSITIVE_SITE_MATTER_LINK.md\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveCARDegreePreserving.lean\`.

## Objective

Lean-own the theorem-ready affine translation response constructed by PR #109 and the exact grading firewall around it.

This task closes the research-only status of

\[
T_b=I+C^\dagger(b)P_0,
\qquad
R_{\rm nil}(L,b)=T_b\rho(L).
\]

It must also make literal that a degree-preserving dressing cannot erase a nonzero degree-mixing affine translation response.

## Mandatory results

### 1. Vacuum projector and nilpotent translation generator

Define the rank-one vacuum projector \(P_0\) on the existing 16-state Fock amplitude carrier and

\[
N_b=C^\dagger(b)P_0.
\]

Prove exactly:

\[
N_bN_c=0.
\]

### 2. Exact additive translation representation

Define

\[
T_b=I+N_b.
\]

Prove:

\[
T_bT_c=T_{b+c},
\qquad
T_b^{-1}=T_{-b}.
\]

### 3. Exterior covariance

Using the merged exterior-frame owners, prove

\[
\rho(L)T_b\rho(L)^{-1}=T_{Lb}.
\]

### 4. Affine semidirect representation

Define

\[
R_{\rm nil}(L,b)=T_b\rho(L)
\]

and prove

\[
R_{\rm nil}(L,b)R_{\rm nil}(M,c)
=
R_{\rm nil}(LM,b+Lc).
\]

### 5. Genuine pure-shift visibility

Give an exact nonzero \(b\), preferably a Role basis vector, and prove that \(T_b\) is not identity.

Prefer a vacuum witness:

\[
T_b|0\rangle=|0\rangle+C^\dagger(b)|0\rangle.
\]

### 6. Degree/parity boundary

Prove a precise theorem showing that nonzero \(T_b\) mixes Fock degree and parity.

Do not merely state that it lies outside a named algebra; give a concrete matrix/vector witness.

### 7. Dressing cannot erase the shift

For any invertible degree-preserving linear equivalence \(F\), prove a scoped theorem:

\[
b\ne0
\Longrightarrow
F T_b F^{-1}\ne I.
\]

Prefer also a theorem that the conjugated nonidentity part remains off-diagonal between different degree sectors.

This is the key firewall for the next research pass.

### 8. Commutator truth firewall

Lean-own or package the trivial but important identity

\[
[I,T_b]=0.
\]

If convenient, prove that for a degree-preserving \(H\), the commutator

\[
[H,N_b]
\]

still has only degree-changing support and therefore is not an identity/degree-preserving replacement for \(N_b\).

Do not overclaim a no-go for arbitrary non-degree-preserving dressing.

### 9. Optional site-aware weighted shift

If short with current APIs, package the one-edge global weighted shift

\[
M_{R_{\rm nil}(A(x,r))}U_r
\]

and its inverse/product law.

This is optional; the local affine representation and grading boundary are the required exit.

## Truth firewall

Do not claim:

- no full B/E matter letter exists;
- \(\kappa\) is unique;
- any arbitrary-background finite graded dressing is impossible;
- \(W_{\rm flux}\) is a group action;
- \(D\mathcal F=H\);
- stress/Einstein/time/golden statements.

## Suggested module

\`D0/Geometry/A4DNilpotentAffineMatterLift.lean\`

## Validation

Narrow build first, then one final D0.All build and normal repository guards.

No \`sorry\`, no new axiom.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start WRK-A4D-NILPOTENT-AFFINE-LIFT-GRADING-BOUNDARY\`;
3. open Draft PR immediately before source edits;
4. implement and validate;
5. before Ready self-retire task;
6. set \`Lifecycle: REVIEW\`;
7. Ready;
8. do not self-merge.

## Exit condition

The PR #109 nilpotent affine translation response is Lean-owned as an exact affine semidirect representation on the existing 16-state carrier, with explicit nonzero pure-shift visibility, degree/parity mixing, and a theorem that degree-preserving conjugation cannot erase a nonzero translation response.
