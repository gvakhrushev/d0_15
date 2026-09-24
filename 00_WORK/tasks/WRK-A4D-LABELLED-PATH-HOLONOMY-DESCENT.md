# WRK-A4D-LABELLED-PATH-HOLONOMY-DESCENT

## Class

WORKER

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Start gate

SATISFIED on current \`main\` after merged PR #103, PR #107 and PR #108.

Read completely, in this order:

- \`02_REGISTRY/research/SYNTHESIS_A4D_ELEMENTARY_MATTER_LINK_THREE_CHANNEL.md\`;
- \`02_REGISTRY/research/MEMO_A4D_PATH_GROUPOID_CROSSED_MATTER_LIFT.md\`;
- \`03_FORMALIZATION/D0/Geometry/ArchivePathWordAlgebra.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean\`;
- \`03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean\`.

## Role in the current synthesis

This worker owns only the **word skeleton** of the next physical letter.

It does not construct the physical matter link.

The surviving fixed-N primitive is expected to be one positive labelled letter

\`\`\`text
ell_N^+(A,e,n; x,r)
\`\`\`

with negative letter given by shifted inverse. Once such a letter exists, the path transport is just its product over \`List ChainStep\`.

This worker must make that product/descent skeleton exact before the physical link is inserted.

The key new finite relation is the labelled \`L=2\` period. It is not a minor corner case: it is the first exact periodic relation that any physical letter must satisfy if it descends to endpoints.

## Objective

Lean-own the **slot-faithful labelled-path descent theorem** that PR #107 left theorem-ready.

The existing theorem

\`pathEval_factors_pairGroupoid_iff_trivial_holonomy\`

is literal ownership for \`ChainPath E\` with a Prop-valued edge relation. Its scope must not be widened by prose.

The new owner must work on the archive's literal labelled step words

\`\`\`text
List ChainStep
\`\`\`

so that at \`L=2\` the parallel labels \`.fwd r\` and \`.bwd r\` remain different even when they have the same ordered endpoints.

## Mandatory results

### 1. Generic positive edge family

Use a generic family of invertible positive edge maps.

Define or package evaluation on

\`\`\`text
(x, steps : List ChainStep)
\`\`\`

with source \`x\` and target \`pathEnd N steps x\`.

The negative step is **defined** by the shifted inverse of the positive edge.

Do not introduce a second independent backward link.

Do not specialize the evaluator to the unknown physical \`ell_N^+\`.

### 2. Exact word laws

Prove in the literal repository pull order:

- empty word;
- append;
- reverse with \`reverseStep\`;
- inverse transport.

Prefer reusing existing \`ChainStep\`, \`pathEnd\` and reverse infrastructure.

### 3. Labelled endpoint-descent iff trivial labelled holonomy

Prove the exact slot-faithful theorem:

\`\`\`text
all labelled paths with the same source and target evaluate equally
iff
every labelled loop evaluates to identity.
\`\`\`

The cancellation pattern may mirror PR #70, but the theorem must be new and typed over the labelled step carrier.

### 4. Explicit L=2 parallel-slot theorem

For \`N=0\`, prove both facts:

1. \`.fwd r\` and \`.bwd r\` from the same site have the same endpoint;
2. they remain distinct \`ChainStep\` labels.

Then derive from endpoint descent the exact positive-link period relation

\`\`\`text
ellPlus x r * ellPlus (x + roleStep 0 r) r = 1
\`\`\`

or the definitionally equivalent formula in the repository's actual pull order.

This relation is the important deliverable.

It is exact word-level structure, not a centered/Nyquist approximation.

### 5. Finite torus skeleton — only if short

If the existing path combinatorics makes it genuinely short, also prove a generic labelled finite-torus presentation:

- oriented plaquette relations;
- four fundamental cycle-period relations;

imply trivial labelled loop holonomy and hence endpoint descent.

If this needs a large new normal-form theory, do **not** inflate this worker. Stop after the iff theorem and the exact \`L=2\` period consequence.

## Relation to PR #108

PR #108 owns scalar **infinitesimal** cycle-sum and plaquette constraints for the landed first-jet law.

This worker does not re-prove them.

The future physical link research must instantiate this labelled skeleton with exact finite cycle/plaquette word relations whose derivative reproduces #108.

Keep that separation explicit.

## Truth firewall

Do not claim:

- PR #70 already owns the labelled \`L=2\` theorem;
- the unknown physical link exists;
- generic physical holonomy is trivial;
- #108 is already an exact nonlinear matter-link theorem;
- endpoint descent on generic curl/harmonic backgrounds;
- Spin, stress, Einstein, physical time, Pisot time, golden/phi statements.

## Suggested module

\`D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`

## Validation

Narrow build first, then one final D0 build and normal repository guards.

No \`sorry\`, no new axiom.

## GitHub-first flow

1. fresh branch from current \`main\`;
2. \`python tools/task_lifecycle.py start WRK-A4D-LABELLED-PATH-HOLONOMY-DESCENT\`;
3. open Draft PR immediately before source edits;
4. implement and validate;
5. before Ready self-retire the task;
6. set \`Lifecycle: REVIEW\`;
7. Ready for review;
8. do not self-merge.

## Exit condition

The literal \`List ChainStep\` evaluator has exact empty/append/reverse/inverse laws and endpoint-independence iff trivial labelled holonomy, with the \`L=2\` parallel-slot collision and resulting exact length-two positive-link period Lean-owned as the generic word skeleton for the next matter-link construction.
