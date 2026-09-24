# WRK-A4D-CROSSED-PATH-ALGEBRA-BOUNDARY

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED.

Primary durable input:

`02_REGISTRY/research/MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md`.

Required existing owners:

- `D0.Geometry.ArchivePathWordAlgebra`;
- `D0.Geometry.A4DDiscreteEnergyKernel`;
- `D0.Geometry.A4DScalarAdvectiveGroupoidObstruction`;
- `D0.Geometry.A4DPathCovariantHodge`;
- PR #98 endpoint/overlap comparison boundary.

This worker formalizes theorem-ready algebraic consequences of PR #95.

It does **not** construct the missing crossed constitutive representation.

It is intentionally independent of `WRK-A4D-OBSERVER-FRAME-CAR-LIFT`: do not duplicate exterior/frame/link/path transport, observer, or located-`J` modules.

## Objective

Lean-own three facts that now bound the next research layer:

1. vertical background action mixes spatial word lengths;
2. the complete owned first jet `H(e)` is an additive path-expression/CAR kernel of spatial word length at most two;
3. exact horizontal composition still admits quadratic endpoint dressing that preserves the flat first jet while changing the second jet.

Target terminal:

`CROSSED-PATH-ALGEBRA-BOUNDARY-LEAN-OWNED-CONSTITUTIVE-LAW-MISSING`.

## Mandatory packages

### 1. `A4DScalarBackgroundWordMixing.lean`

Formalize the scalar identity on the accepted cycle:

```text
G_xi U - U G_xi
  = -(1/2) M_(h_xi) (U^2 - I)
```

with the repository's literal orientation conventions.

Required:

- generic theorem for the accepted period range;
- exact delta and non-delta controls;
- a precise theorem that the commutator need not stay in the one-letter shift sector;
- an explicit support/path-expression statement showing the empty and length-two words appear.

Do not merely restate the equality as a definition.

Do not claim that the full crossed action is constructed.

### 2. `A4DStaggeredFirstJetPathExpansion.lean`

Package the already-owned `flatStaggeredH` as an explicit additive path expansion.

Use the literal identities:

```text
A_r = (I + U_r^-1)/2
M_e U_s A_r E_sr
  = (1/2) M_e (U_s + U_s U_r^-1) E_sr
```

and the existing symmetric scalar link term.

Prove an exact theorem equivalent to `flatStaggeredH` whose terms expose:

- empty/on-site terms where present;
- one-edge terms;
- mixed two-edge corner terms;
- CAR endomorphisms and adjoints.

Add a bounded-support/path-cost capstone stating that the first jet uses word length at most two.

Retain:

- L=2 raw Nyquist control;
- L=3 corner control;
- degree/parity.

Do not claim path functoriality selects the coefficients.

### 3. `A4DHorizontalDressingSecondJetFreedom.lean`

Formalize the exact horizontal endpoint-dressing mechanism.

For an endpoint/path representation `T` and invertible endpoint dressing `P`, prove a typed statement of the form

```text
T^P_(x<-y) = P_x T_(x<-y) P_y^-1
```

preserves:

- identity;
- exact composition;
- reversal/inverse where supplied.

Then formalize a polynomial/rational quadratic family with:

- `P(0)=I`;
- zero linear coefficient;
- nonzero quadratic coefficient;
- exact composition after dressing.

Conclude, in the stated class, that horizontal path composition plus the flat first jet does not determine the second jet.

This is the formal shadow of the PR #95 dressing argument; it is not a universal constitutive nonuniqueness theorem.

### 4. `A4DCrossedPathAlgebraBoundary.lean`

Package the three theorem families into one explicit boundary:

- bare spatial words are not closed under the vertical scalar action;
- the owned first jet belongs to an additive length-≤2 path-expression/CAR sector;
- horizontal composition alone does not select the quadratic constitutive extension.

Do not define a placeholder physical structure with fields `pi`, `R`, `alpha`, `W` and call the research task solved.

## Registry

Register bounded claims for the actual proved content, for example:

- scalar background word mixing;
- first-jet path-expression support;
- horizontal dressing second-jet nonselection.

Keep nonselection scoped to the explicit dressing class.

## Throughput

Follow GitHub-first flow.

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-CROSSED-PATH-ALGEBRA-BOUNDARY`;
3. immediately open Draft PR before Lean edits;
4. narrow builds per module;
5. one final `python tools/lean_task_build.py final`;
6. no-sorry, repo/work validators, generated views, `git diff --check`;
7. `#print axioms` principal capstones;
8. self-retire in the same PR;
9. Ready / `Lifecycle: REVIEW`;
10. do not self-merge.

No `lake clean`, `sorry`, `sorryAx`, or new axioms.

## Truth firewall

Do not:

- construct or claim the physical crossed constitutive law;
- duplicate observer/frame/path transport from the other worker;
- select `S`, universal `K` or a nonlinear `Q(e)`;
- reinterpret located `J`;
- use golden refinement;
- promote to stress/Einstein closure.

## Exit condition

The scalar vertical word-mixing identity, full first-jet path-expression support, and quadratic horizontal-dressing nonselection are Lean-owned, while the crossed constitutive representation remains explicitly research-owned.
