# WRK-A4D-PRIMAL-DUAL-PARENT-ALGEBRA

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## State
IN_PROGRESS

This task has completed the cloud-first draft phase and is now the **sole active local verification worker**.

## Objective

Formalize the theorem-ready pieces of E-PDH-PARENT that do **not** require inventing the missing Cartan/chain connection.

Target packages:

1. parent-constraint transport no-go;
2. exact small-lattice centered-Cartan closure/radius-one no-go;
3. abstract mixed primal/dual Hodge parent algebra;
4. conditional metric-stress divergence descent.

Do not select or invent the actual connection group or physical Hodge constitutive law.

## Preferred cloud draft branch

\`draft/a4d-primal-dual-parent-algebra\`

## Suggested modules

Add:

- \`D0/Geometry/A4DCoframeParentConstraint.lean\`
- \`D0/Geometry/A4DCenteredCartanClosureNoGo.lean\`
- \`D0/Geometry/FinitePrimalDualHodgeParent.lean\`
- \`D0/Gravity/A4DParentWardStressDescent.lean\`

Reuse current centered-difference, cubical differential/Cartan, Role-pair metric carrier and adjoint owners.

## Package A — parent constraint

Define the abstract/typed coframe metric readout and parent constraint needed for the theorem.

Prove the generic identity:
\[
\delta m=K\xi,\quad
\delta e=d_f\xi+T,\quad
\delta n=0
\Longrightarrow
R(T)=0.
\]

Formalize an odd one-role finite restriction where the centering/readout is invertible and derive the capstone:
\[
T=0.
\]

Keep this a carrier-compatibility theorem, not a physical no-go beyond its hypotheses.

## Package B — centered-Cartan closure no-go

On an exact finite small cycle (prefer the \(L=5\) rational control from the research memo), define the scalar centered generator and prove that two local generators have a commutator with a nonzero distance-two matrix entry.

Capstones should state:

- the original local centered-generator family is not closed under commutator;
- a radius-one first-order correction cannot cancel the exhibited distance-two curvature under the explicitly formalized support assumptions.

Do not overgeneralize beyond the typed support class.

## Package C — abstract mixed primal/dual parent

Create generic finite primal/dual graded carriers with incidence maps and a constitutive \(\star\).

Introduce an auxiliary codifferential field and multiplier so no explicit inverse \(\star^{-1}\) is needed.

Define the mixed action algebraically and prove exact covariance/invariance under hypotheses:

\[
[d_P,G_P]=0,\qquad
[d_D,G_D]=0,
\]
pairing invariance, and
\[
\delta\star=G_D\star-\star G_P.
\]

The theorem should be purely finite linear algebra and should not claim D0 has supplied the actual \(\star(e,n,\Omega)\).

## Package D — stress descent

Parameterize the missing parent Ward identity and auxiliary EOM as explicit hypotheses.

Use the parent constraint plus coframe EOM to derive
\[
\langle\Lambda,K\xi\rangle=0.
\]

Then reuse the owned \`symmetricRoleGradient\` adjoint/integration-by-parts theorem to conclude
\[
\operatorname{centeredRoleDivergence}\Lambda=0.
\]

## Firewalls

Do not claim:

- the connection group is derived;
- the Hodge constitutive law is selected;
- local Lorentz gauge is owned;
- nonzero Nyquist stress;
- continuum diffeomorphism invariance;
- nonlinear Einstein dynamics.

## Cloud draft policy

Keep this task \`PLANNED\`.

The cloud formalizer may create/push the draft branch and owner modules but must not edit:

- \`00_WORK/manifest.json\`;
- \`00_WORK/STATUS.md\`;
- generated work views;
- claim statuses;
- release metadata.

No cold build is required. Do not run \`lake clean\`.

End cloud work with \`CLOUD_DRAFT_READY\`.

A local worker later rebases the draft onto fresh canonical main, compiles/fixes it, performs one incremental \`lake build D0.All\`, normal guards/no-sorry/axiom checks, updates metadata, moves the task to REVIEW and opens the PR.

## Completion

Cloud phase: \`CLOUD_DRAFT_READY\`, task stays PLANNED.

Local phase: REVIEW, PR, STOP.


## Integration evidence

The exit condition is met by the landed modules, without a constitutive selection:

- `parentConstraint_transport_in_readout_kernel` and `odd_one_role_transport_zero`
- `centered_generator_family_not_closed` and `radius_one_correction_cannot_cancel_distance_two`
- `mixedPrimalDualWard_invariant`
- `centeredRoleDivergence_zero_of_parentWard`, which still assumes `readout (df xi) = symmetricRoleGradient xi`

State: REVIEW.

## Local verification handoff

Cloud draft branch: `draft/a4d-primal-dual-parent-algebra`

Observed draft head: `594210ce521f72a8296b28732eb323caa1064a0d`

The draft adds only the four intended owner modules. Start from fresh current `origin/main`, create/update `work/a4d-primal-dual-parent-algebra`, and rebase/cherry-pick the draft source commit. Compile the draft before redesigning. Do not run `lake clean` and do not delete the warm Mathlib/Lake cache. Use narrow builds for the four owner modules, concrete Lean/API fixes only, then one incremental `lake build D0.All`, normal guards/no-sorry/#print axioms, task -> REVIEW, PR, STOP. Do not invent the missing Cartan connection/constitutive law.
