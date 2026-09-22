# WRK-A4D-CUBICAL-DIFFERENTIAL-CARTAN

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
PLANNED

Do not dispatch this worker until a current worker slot is free.

Dispatch it separately, never bundled with another worker prompt.

If two workers are active simultaneously they must use separate git worktrees/checkouts. Sharing the external Lake/Mathlib cache is allowed and preferred.

## Cloud draft phase

A cloud formalizer MAY prepare a candidate implementation for this PLANNED task before a local worker slot is free.

Rules:

- keep this task \`PLANNED\`;
- use branch \`draft/a4d-cubical-differential-cartan\` (or an equivalent clearly draft-named branch) from the stated current canonical baseline;
- do not edit \`manifest.json\`, \`STATUS.md\`, generated views, claim statuses, or release metadata;
- implement the owner modules and theorem proofs as far as possible;
- run only narrow Lean checks if affordable; full \`D0.All\` is not required in the cloud;
- do not claim \`LEAN_PROVED\` or move the task to \`REVIEW\`;
- commit/push the branch and finish with a \`CLOUD_DRAFT_READY\` handoff listing base/head SHA, changed files, intended capstones, checks actually run, unchecked gates, and known proof/API risks.

When a local worker slot opens, the worker should start from this draft rather than reimplementing from scratch, rebase/merge onto fresh canonical main, compile first, fix concrete failures, then perform the normal local verification and metadata update.

## Objective

Formalize the finite algebraic package identified by E-CDIFF:

1. full literal CAR anticommutators;
2. actual cochain amplitude carrier;
3. canonical forward cubical differential with \(d^2=0\) and degree raising;
4. exact forward-to-centered averaging;
5. forward CAR Cartan operator;
6. exact reconstruction of \`symmetricRoleGradient\`.

Stop before Hodge-action Ward invariance or physical matter interpretation.

## Preferred branch

\`work/a4d-cubical-differential-cartan\`

## Main files

Strengthen:
- \`D0/Geometry/ArchiveCARRelations.lean\`

Add:
- \`D0/Geometry/ArchiveCubicalDifferential.lean\`
- \`D0/Geometry/ArchiveCubicalCartan.lean\`

## Required CAR theorems

Prove the literal matrix/operator forms of:

\[
\{c_r,c_s\}=0,
\]
\[
\{c_r^\dagger,c_s^\dagger\}=0,
\]
\[
\{c_r,c_s^\dagger\}=\delta_{rs}I.
\]

Also prove support/degree raise/lower lemmas.

## Cochain carrier

Define:
\[
ArchiveCochainBasis(N)=ArchiveRolePhaseGroup(N)\times ArchiveFockState,
\]
\[
ArchiveCochain(N)=ArchiveCochainBasis(N)\to\mathbb R.
\]

Define vacuum and one-form singleton Fock states plus scalar embedding.

## Forward differential

Define:
\[
\nabla_r^+=L(U_r-I),
\qquad
d_f=\sum_r\nabla_r^+C_r^\dagger.
\]

Prove:

- directional commutation;
- radius-one support/locality;
- degree raising;
- \(d_f^2=0\);
- flat forward/backward adjoint identity.

## Centering

Define:
\[
A_r=(I+U_r^{-1})/2
\]
and prove exactly:
\[
D_r=A_r\nabla_r^+.
\]

Define one-form centering and prove:
\[
\mathcal C_1(d_ff)=Df.
\]

## Centered diagnostic

Optionally define \(d_c=\sum_rD_rC_r^\dagger\).

Prove \(d_c^2=0\) and \`dCentered 0 = 0\`, explicitly preventing its promotion as the topological cubical owner.

## Cartan

Define:
\[
\iota_\xi=\sum_rM_{\xi^r}C_r,
\]
\[
\mathcal L_\xi^f=d_f\iota_\xi+\iota_\xi d_f.
\]

Prove:

- degree preservation;
- radius one;
- \(d_f\mathcal L_\xi^f=\mathcal L_\xi^fd_f\);
- constant-vector reduction using mixed CAR;
- constant coframe identity;
- centered coframe reconstruction.

Capstone:
\[
\texttt{cartanMetricVariation N xi}
=
\texttt{symmetricRoleGradient N xi}.
\]

## Firewalls

Do not claim:

- Hodge-action Ward invariance;
- stress conservation;
- physical state selection;
- continuum diffeomorphism covariance;
- Einstein coupling.

## Build policy

Preserve the Lean/Mathlib cache.

Use narrow target builds while iterating, one incremental \`lake build D0.All\` before REVIEW, then normal guards/no-sorry/axiom checks and remote CI.

Do not run \`lake clean\` for routine evidence.

## Completion

Task -> REVIEW, PR, STOP.
