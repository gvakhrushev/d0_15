# WRK-A4D-REFERENCE-LOCAL-CANDIDATE-NOGO

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Objective

Lean-own the scoped local-candidate obstruction from PR #114.

Formalize the fact that the natural constant source/target/shift linear ansatz

\[
q
=
a\,v_y
+
c\,L^{-1}v_x
+
d\,L^{-1}b
\]

cannot simultaneously satisfy flat normalization, the exact pure-gauge
control on the explicit L=3 witness, and nonzero pure affine-shift visibility.

This is a candidate-class no-go only.

## Read first

- \`02_REGISTRY/research/MEMO_A4D_SOLDER_REFERENCE_LEG_SECTION.md\`, candidate classes III–IV and theorem-ready handoff A/B;
- \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
- existing finite L=3 coframe/gauge witness owners used by the memo.

## Preferred module

\`03_FORMALIZATION/D0/Geometry/A4DReferenceLocalCandidateNoGo.lean\`

## Mandatory theorem package

### 1. Candidate definition

Define the constant-coefficient source-typed ansatz

\[
q_{a,c,d}
=
a\,v_y+c\,L^{-1}v_x+d\,L^{-1}b.
\]

Keep the exact RoleSpace typing visible.

### 2. Flat normalization equation

At flat,

\[
v_x=v_y=e_r,\quad L=I,\quad b=0,
\]

derive the coefficient condition

\[
a+c=1
\]

for the chosen exact basis witness.

### 3. L=3 exact pure-gauge witness

Use or package the explicit PR #114 equal-neighbour exact gauge witness with

\[
L=I,\qquad v_x=v_y=v,\qquad b\ne0.
\]

Under flat normalization, exact cancellation requires

\[
d=-1.
\]

Make the nonzero coordinate witness explicit rather than relying on informal
scalar cancellation.

### 4. Pure-shift contradiction

For

\[
e=0,\quad L=I,\quad v_x=v_y=e_r,\quad b\ne0,
\]

show that the forced coefficients imply

\[
q=e_r-b
\]

and therefore

\[
\kappa_q=0.
\]

This contradicts the required pure-shift visibility.

### 5. Predecessor endpoint corollaries

If straightforward, Lean-own the two exact endpoint candidates:

\[
q=L^{-1}v_x \implies \kappa=b,
\]

\[
q=L^{-1}(v_x-b) \implies \kappa=0.
\]

These are useful controls and explain the two ends of the interpolation.

## Scope

State the result explicitly as:

\[
\text{no constant linear combination in this candidate class closes all controls}.
\]

Do **not** claim no nonlinear/nonlocal/observer/path selector exists.

## Firewalls

Do not:

- choose a physical \(q\);
- generalize the no-go beyond the formalized candidate class;
- start finite E dressing;
- replace raw solder with centered data;
- identify \(A=A(e)\);
- touch stress/time/golden work.

## Exit condition

Lean owns the exact scoped no-go for the constant source/target/shift linear
reference ansatz and the predecessor endpoint controls, with an explicit L=3
pure-gauge witness and pure-shift contradiction.

## GitHub-first flow

Fresh branch → lifecycle start → Draft PR immediately → narrow build →
incremental \`D0.All\` → support registration → self-retire → \`Lifecycle:
REVIEW\` → Ready → do not self-merge.

No \`sorry\`, no new axioms, no \`lake clean\`.
