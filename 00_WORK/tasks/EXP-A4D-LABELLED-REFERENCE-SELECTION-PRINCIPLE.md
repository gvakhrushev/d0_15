# EXP-A4D-LABELLED-REFERENCE-SELECTION-PRINCIPLE

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

Open after the durable result of PR #114 is merged.

This task supersedes further blind ansatz-search for \(q\).  PR #114 has already
classified the natural local candidate classes and exhibited explicit
nonselection directions.

## Read first

Read completely:

1. \`02_REGISTRY/research/MEMO_A4D_SOLDER_REFERENCE_LEG_SECTION.md\`;
2. \`02_REGISTRY/research/MEMO_A4D_SOLDER_CARTAN_EDGE_MISMATCH.md\`;
3. \`02_REGISTRY/research/SYNTHESIS_A4D_SOLDER_CARTAN_EDGE_MISMATCH_AND_GRADED_DRESSING.md\`;
4. \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\` once merged;
5. \`03_FORMALIZATION/D0/Geometry/A4DAffineOriginSolderBoundary.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`;
7. \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorObserverForm.lean\` and the merged observer/frame substrate from PR #103.

## Frozen frontier

For a supplied source reference leg \(q_r(y)\), D0 has the typed mismatch

\[
\kappa_q(A,e;x,r)=A_{x,r}(q_r(x+r))-v_r(e,x).
\]

PR #114 shows that the mandatory controls do **not** select \(q\):

- fixed/source/predecessor/local-linear natural classes fail;
- one node origin is too small;
- the exact two-link junction contains a nonzero overlap defect;
- if one admissible seed \(q\) exists, then
  \[
  q_{\lambda,\mu}=q+\lambda z_{\rm curl}+\mu z_{\rm harm}
  \]
  preserves flat, exact pure-gauge, pure-shift and pure-linear frame controls while changing transverse curl/harmonic response.

Therefore the missing input is no longer a formula.  It is a **geometric selection principle**.

## Objective

Construct or terminally classify one independently motivated labelled-edge
selection principle that chooses a reference section

\[
q_N(A,e,n;y,r)
\]

or an equivalent affine-origin/path object, and that removes the PR #114
nonselection without silently quotienting labelled-path provenance.

The principle may depend on already-owned observer data \(n\) only through the
owned positive observer form \(h_n\).  It may not introduce a second physical
clock or identify \(A=A(e)\).

## Mandatory acceptance tests

A successful principle must imply all of:

### 1. Flat normalization

\[
q(A_{\rm flat},0,n;y,r)=e_r.
\]

### 2. Exact pure-gauge diagonal

For \(A=A_\phi\), \(e=d_f\phi\),

\[
\kappa_q=0.
\]

### 3. Pure affine-shift visibility

For \(e=0,L=I,b\ne0\),

\[
\kappa_q\ne0,
\]

preferably exactly \(\kappa_q=b\).

### 4. Pure-linear frame covariance

\[
q(A^g,e^g,n^g;y,r)=g_yq(A,e,n;y,r)
\]

with the literal observer/frame convention already owned.

### 5. Labelled junction / overlap law

The selector must give an explicit rule for consecutive labelled edges.  It
must confront the exact identity

\[
\kappa_1+L_1\kappa_2
=
((A_1A_2)(q_2)-v_1)+L_1(q_1-v_2).
\]

Do not impose \(q_1=v_2\) blindly: PR #114 shows it already fails for generic
mixed Role junctions at flat.  Derive the correct Role-labelled overlap
comparison or prove that additional junction data are required.

### 6. Curl deformation rejection

Explain exactly why

\[
q\mapsto q+\lambda z_{\rm curl}
\]

is no longer admissible, or else the principle has not selected \(q\).

### 7. Harmonic deformation rejection

Explain exactly why

\[
q\mapsto q+\mu z_{\rm harm}
\]

is no longer admissible.  A purely local principle that cannot distinguish the
harmonic family is insufficient unless it derives a separate global overlap
law.

### 8. Raw finite controls

Keep visible:

- L=2 raw Nyquist;
- L=3 off-diagonal corner;
- one plaquette curl witness;
- one harmonic cycle.

### 9. Path provenance

Do not quotient nontrivial labelled holonomy.  If a basepoint, spanning tree,
path family or orbit representative is required, classify that datum explicitly
as part of the selector rather than hiding it.

## Required principle classes to test

At minimum audit these classes before terminal:

### A. Junction/overlap principle

Ask whether a Role-labelled transition object at path junctions can replace
the impossible naive condition \(q_1=v_2\) and make the reference assignment
functorial.

### B. Observer-positive variational principle

The repo owns a positive observer form \(h_n\).  Test whether \(q\) can be
selected as the unique minimizer of an explicitly stated finite positive
functional built from:

- \(\kappa_q\);
- junction defects;
- optional curl/harmonic penalties;

with coefficients derived from existing geometry rather than chosen to kill
the known deformations by hand.

Prove uniqueness or exhibit its remaining kernel.

Do not reinterpret \(n\) as a new clock.

### C. Basepoint/path gauge fixing

Test whether a canonical basepoint/path or spanning-tree rule can select the
harmonic component.  If it works only after arbitrary tree/basepoint choice,
state that as new external data, not an intrinsic solution.

### D. Full affine-origin structure

Use the PR #115 boundary.  A full affine point law may repair covariance, but
PR #114 shows covariance alone does not select \(q\).  Determine whether an
additional affine-origin overlap/cocycle law changes that conclusion.

### E. Orbitwise/equivariant selection

If all local/variational/path principles fail, classify whether a
frame-equivariant section exists only after choosing orbit representatives or
other noncanonical data.

## Nonselection firewall

It is not enough to propose one \(q\) and verify the four old controls.

Every positive candidate must be tested against the explicit PR #114
deformations \(z_{\rm curl}\) and \(z_{\rm harm}\).  If both deformations remain
allowed, selection has failed.

## Finite-E firewall

Do **not** start \`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING\` in this task.

The gate opens only if a usable selection principle actually lands, or if the
repo explicitly adopts the additional geometric datum required by the
terminal.

## Other firewalls

Do not:

- identify \(A=A(e)\);
- reopen row→vector typing;
- reopen affine representability;
- use \([H,T_b]\) as a selector;
- insert golden/AF data or tower \(\phi\);
- start stress/Einstein;
- turn observer \(n\) into a second time variable.

## Preferred terminals

Positive:

- \`LABELLED-REFERENCE-SELECTION-PRINCIPLE-CONSTRUCTED\`;
- \`OBSERVER-POSITIVE-REFERENCE-MINIMIZER-CONSTRUCTED\`;
- \`REFERENCE-OVERLAP-COCYCLE-SELECTS-SECTION\`.

Scoped:

- \`REFERENCE-SELECTION-REQUIRES-BASEPOINT-PATH-GAUGE-DATUM\`;
- \`REFERENCE-SELECTION-REQUIRES-NEW-JUNCTION-OVERLAP-PRIMITIVE\`;
- \`OWNED-GEOMETRY-DOES-NOT-SELECT-REFERENCE-SECTION\`.

Use only the strongest result actually established.

## Deliverable

One durable theorem-ready memo containing:

1. frozen PR #114 nonselection theorem;
2. explicit selection principle(s) tested;
3. junction/overlap derivation;
4. observer-positive/minimality audit;
5. curl deformation test;
6. harmonic deformation test;
7. L=2/L=3/curl/harmonic controls;
8. covariance and full-affine boundary;
9. uniqueness/kernel classification;
10. exact terminal;
11. theorem-ready handoff;
12. exactly one next step.

No Lean source.

## GitHub-first flow

1. fresh branch from then-current \`main\`;
2. \`python tools/task_lifecycle.py start EXP-A4D-LABELLED-REFERENCE-SELECTION-PRINCIPLE\`;
3. open Draft PR immediately;
4. research only inside that PR;
5. durable memo;
6. self-retire before Ready;
7. \`Lifecycle: REVIEW\`;
8. do not self-merge.

## Exit condition

A labelled-edge geometric selection principle chooses the source reference
section while eliminating both known curl and harmonic deformation freedoms
and supplying an explicit path-junction law, or the earliest additional
junction/basepoint/observer-minimality datum required for such selection is
terminally identified without starting finite E dressing.
