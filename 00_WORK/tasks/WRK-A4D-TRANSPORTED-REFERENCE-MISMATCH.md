# WRK-A4D-TRANSPORTED-REFERENCE-MISMATCH

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the theorem-ready **conditional transported-reference mismatch** from merged PR #112.

This task does **not** select the missing reference section \(q\).

It formalizes the already-derived statement that, once a source-fibre reference leg is supplied,

\[
q_r(y)\in V_y,\qquad y=x+r,
\]

the B/E comparison

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(q_r(y))
-
\operatorname{solderLegVector}(N,e,x,r)
\]

is well typed and has the exact flat / pure-shift / cancellation / nilpotent-response controls.

## Read first

Read completely:

1. \`02_REGISTRY/research/MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH.md\`;
2. \`02_REGISTRY/research/SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md\`;
3. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
4. \`03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean\`;
5. \`03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean\`.

Use current \`main\` at task start.

## Frozen inputs

The repo already owns:

\[
A_{x,r}:V_{x+r}\to_{\rm aff}V_x
\]

through \`AffineCartanMap\` / \`AffineCartanConnection\`;

\[
v_r(e,x)
=
\operatorname{solderLegVector}(N,e,x,r)\in V_x;
\]

and the nilpotent translation response

\[
T_b=I+C^\dagger(b)P_0.
\]

Do not reconstruct these objects.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`

Use a uniquely named local \`LinearOrder Role\` instance if one is required; do not recreate the #113 instance-name collision.

## Mandatory definitions

Introduce a typed reference field, e.g.

\[
\operatorname{ReferenceLegField}(N)
=
X_N\to \mathrm{Role}\to V.
\]

Then define

\[
\operatorname{transportedReferenceMismatch}(A,e,q,x,r)
=
\operatorname{AffineCartanMap.apply}(A_{x,r},q(x+r,r))
-
\operatorname{solderLegVector}(N,e,x,r).
\]

Keep the source site \(x+r\) literal.

## Mandatory theorems

### 1. Exact expansion

Own literally

\[
\kappa_q
=
(A_{x,r}).\mathrm{shift}
+
(A_{x,r}).\mathrm{lin}(q(x+r,r))
-
v_r(e,x).
\]

### 2. Flat control

For

\[
A=A_{\rm flat},\qquad e=0,\qquad q(y,r)=e_r
\]

prove

\[
\kappa_q=0.
\]

Reuse \`solderLegVector_zero\`.

### 3. Pure affine-shift control

For a one-link affine map with

\[
L=I,\qquad \mathrm{shift}=b,\qquad e=0,\qquad q=e_r,
\]

prove exactly

\[
\kappa_q=b.
\]

Use a generic \(b\); include one nonzero witness.

### 4. Exact cancellation criterion for trivial linear part

If

\[
(A_{x,r}).\mathrm{lin}=I
\]

and

\[
q(x+r,r)=v_r(e,x)-(A_{x,r}).\mathrm{shift},
\]

prove

\[
\kappa_q=0.
\]

This is the Lean owner for the PR #112 pure-gauge reference condition at the algebraic edge level.

### 5. Flat fixed-reference failure under nonzero shift

For \(e=0\), \(q=e_r\), \(L=I\), \(b\ne0\),

\[
\kappa_q\ne0.
\]

This is the firewall against absorbing Channel B into the reference.

### 6. Nilpotent matter response

Define the conditional matter letter

\[
T_{\kappa_q}
=
\operatorname{nilpotentAffineTranslation}(\kappa_q).
\]

Prove:

- flat \(\Rightarrow T_{\kappa_q}=I\);
- cancellation condition \(\Rightarrow T_{\kappa_q}=I\);
- pure shift \(\Rightarrow T_{\kappa_q}=T_b\);
- if \(\kappa_q\ne0\), then \(T_{\kappa_q}\ne I\).

Reuse PR #113 theorems. Do not re-prove nilpotence.

### 7. No fake commutator cancellation

Retain the existing firewall:

\[
[I,T_{\kappa_q}]=0.
\]

Do not introduce \([H,T_b]\) as a mechanism.

## Optional theorem if straightforward

A generic covariance lemma of the form:

if one independently knows

\[
A'(q')-v'=g_x(A(q)-v),
\]

then the corresponding nilpotent matter letters are related by the owned exterior-frame conjugation theorem.

Do not make this optional lemma depend on selecting \(q(A,e)\).

## Scope firewalls

Do not:

- define an intrinsic \(q_N(A,e)\);
- claim \(\kappa_N(A,e)\) exists without supplied \(q\);
- start finite graded E dressing;
- identify \(A=A(e)\);
- add a second row→vector conversion after \`solderLegVector\`;
- touch stress, Einstein, physical time or golden refinement;
- weaken the pure-shift visibility condition.

## Exit condition

Lean owns the conditional edge comparison \(\kappa_q\), exact flat/pure-shift/cancellation controls, and the induced nilpotent response \(T_{\kappa_q}\), while the missing selection of \(q\) remains explicitly outside this worker.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start WRK-A4D-TRANSPORTED-REFERENCE-MISMATCH\`;
3. open Draft PR immediately;
4. implement only this worker;
5. narrow builds during development;
6. one incremental \`lake build D0.All\` before Ready;
7. register support/imports through canonical generators;
8. self-retire task;
9. PR body \`Lifecycle: REVIEW\`;
10. Ready for review;
11. do not self-merge.

No \`sorry\`. No new axioms. Do not run \`lake clean\`.
