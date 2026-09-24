# WRK-A4D-AFFINE-SHIFT-EXTERIOR-BLINDNESS

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

SATISFIED on current \`main\` after merged PR #103 and PR #107.

Read completely, in this order:

- \`02_REGISTRY/research/SYNTHESIS_A4D_ELEMENTARY_MATTER_LINK_THREE_CHANNEL.md\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
- \`02_REGISTRY/research/MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md\`;
- \`02_REGISTRY/research/MEMO_A4D_PATH_GROUPOID_CROSSED_MATTER_LIFT.md\`.

## Role in the current synthesis

The next matter letter has three typed inputs/channels:

1. linear Cartan / exterior transport;
2. raw coframe amplitude / constitutive tangent;
3. affine translational/site response.

This worker classifies **Channel L only**.

PR #103 already gives the positive linear exterior transport on the existing 16-state carrier. The heavy research task must not waste effort rediscovering whether that transport sees affine translation.

This worker turns the blindness into a literal Lean boundary.

It does **not** say that the final elementary matter letter is blind to affine translation.

## Objective

Lean-own the exact statement that the current PR #103

\`exteriorPathTransport\`

depends only on the linear part of affine Cartan path transport and therefore cannot, by itself, detect a pure translational affine holonomy.

## Mandatory results

### 1. Dependence only on linear path data

Prove that equality of the relevant linear path values implies equality of

\`exteriorPathTransport\`.

State the theorem as close as possible to the existing \`covariantLin\` / \`affinePath\` API.

Do not create a new representation just to state the boundary.

### 2. Identity linear part gives identity exterior transport

Prove a scoped theorem:

if the affine path value has linear part identity, then the current 16-state exterior path transport is identity.

Keep the theorem about the existing representation.

### 3. Exact nonzero affine-shift witness

Construct or reuse an exact finite archive witness, preferably at \`L=3\`, with affine path/loop value

\`\`\`text
linear part = I
affine shift ≠ 0
\`\`\`

and prove simultaneously:

\`\`\`text
exteriorPathTransport = I.
\`\`\`

Prefer an existing Cartan/path witness over an ad hoc matrix fixture.

The witness should be useful directly by the heavy research task as its Channel-B hostile control.

### 4. Same-endpoint comparison if natural

If the existing API makes this short, exhibit two same-endpoint labelled paths with:

- equal linear transport;
- unequal affine shifts;

and prove the current exterior transport evaluates them equally.

Do not force this if it requires a large new path normal form.

### 5. Capstone channel theorem

Package a theorem or small theorem family whose precise reading is:

\`\`\`text
the PR #103 exterior path transport represents Channel L
and factors through the linear affine path part;
pure affine translation belongs to a different missing channel.
\`\`\`

The last clause is a typing interpretation of the proved factorization boundary, not a universal impossibility theorem.

## Truth firewall

Do not claim:

- no affine-sensitive matter representation exists;
- translations cannot act on the existing global site/path-expression carrier;
- a 32-state or site-corner extension is impossible;
- the final elementary letter must factor as a product of independent channel matrices;
- the 16-state carrier must be abandoned;
- #108 cycle/plaquette constraints are consequences of this linear channel;
- stress, Einstein, physical time, Pisot time, golden/phi, or second-jet closure.

## Suggested module

\`D0/Geometry/A4DAffineShiftExteriorBlindness.lean\`

## Validation

Narrow build first, then one final D0 build and normal repository guards.

No \`sorry\`, no new axiom.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start WRK-A4D-AFFINE-SHIFT-EXTERIOR-BLINDNESS\`;
3. open Draft PR immediately before source edits;
4. implement and validate;
5. before Ready self-retire the task;
6. set \`Lifecycle: REVIEW\`;
7. Ready for review;
8. do not self-merge.

## Exit condition

The current 16-state exterior path transport is Lean-proved to factor through the linear affine path part, with an exact nonzero affine-translation witness on which the exterior transport is identity, thereby closing Channel L and leaving the site-aware affine translation response as the genuinely missing channel.
