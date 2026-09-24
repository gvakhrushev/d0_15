# WRK-A4D-OBSERVER-FRAME-CAR-LIFT

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Execution model

This task predates the GitHub-first workflow, but the next execution must use the new contract.

The old PR #87 is a pre-flow migration source only. Do not continue development on its stale branch.

Start from current `main` and:

1. create a fresh execution branch;
2. run
   ```bash
   python tools/task_lifecycle.py start WRK-A4D-OBSERVER-FRAME-CAR-LIFT
   ```
3. open a **Draft PR before porting or writing Lean code**;
4. only after the Draft PR exists, port useful code from old PR #87;
5. keep PR lifecycle synchronized with the branch task state;
6. when all theorem gaps are closed and validation is green, run
   ```bash
   python tools/task_lifecycle.py retire WRK-A4D-OBSERVER-FRAME-CAR-LIFT
   ```
7. mark the same PR Ready with `Lifecycle: REVIEW`;
8. do not self-merge.

The GitHub PR number is the execution ID.

## Start gate

SATISFIED.

Durable theorem-ready input:

- `02_REGISTRY/research/MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT.md`.

Additional fixed-level synthesis/boundary inputs:

- `02_REGISTRY/research/MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW.md`;
- `02_REGISTRY/research/SYNTHESIS_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md`.

Located `J` is merged via PR #76.

The missing all-order path-resolved comparison/action is research task
`EXP-A4D-PATH-RESOLVED-MATTER-WORD-ACTION`.

This worker prepares the theorem-level frame/CAR/path-transport substrate for that research. It does **not** construct the missing constitutive `C_N`, select nonlinear `Q(e)`, or solve the staggered cell-energy law.

## Three-star dictionary

Keep these objects distinct.

| Name | Meaning |
|---|---|
| `J` | located two-color topological primal/dual placement/pairing; not a metric selector |
| `h_n` / metric `*_eta` | observer/Lorentz metric structure |
| scalar reverse-star | one-color scoped inverse/reverse stencil from the locality no-go |

Never transfer a theorem/no-go across these rows without a typed bridge.

## Objective

Lean-own the complete generic exterior/frame/observer/link substrate already derived in the durable frame memo, strengthen the partial old PR #87 implementation to the literal canonical theorem packages, and extend the positive link lift to the already-owned PR #70 path words where this follows functorially.

The worker must end with a clean boundary:

```text
generic exterior/frame/observer/link/path transport substrate — Lean-owned
path-resolved constitutive matter word action C_N — still research
full staggered all-order cell energy / nonlinear Q(e) — still research
```

## Mandatory packages

### 1. `ArchiveExteriorFrameLift.lean`

Formalize on the existing 16-state `ArchiveFockState`:

- exterior lift by minors;
- degree preservation;
- identity law;
- **generic composition law**;
- inverse corollary under an explicit inverse hypothesis;
- creator covariance for general vectors;
- algebraic contraction covariance for general covectors;
- CAR compatibility;
- explicit documentation/theorem boundary: exterior representation is not a Spin representation.

Do not satisfy composition/inverse only with a finite rational boost witness.

### 2. `A4DObserverPositiveExterior.lean`

Formalize:

```text
h_n = -eta + 2 n^flat ⊗ n^flat
```

with:

- positivity for a generic supplied unit timelike observer `n`;
- `n=e_A` gives counting `I` only as a reference observer gauge;
- all-degree exterior Gram/congruence law;
- observer adjoint of creators and contractions;
- Lorentz covariance with moving observer;
- exact rational A/B boost as a control, not the only theorem;
- no physical-time interpretation.

Avoid vacuous truth-boundary theorems such as `: True`; keep interpretive boundaries in documentation unless there is a literal proposition to prove.

### 3. `A4DRawSolderFrameAction.lean`

Formalize:

- raw row/covector and vector conventions;
- local frame action on the full uncentered solder;
- exact centered-frame defect;
- a specified transported-center construction;
- **prove the transported-center repair covariance identity**, not only define the repaired center;
- keep raw Nyquist information available separately;
- exact L=2 witness showing centered-only blindness.

### 4. `ArchiveAffineExteriorLink.lean`

Formalize the Lorentz-restricted lift of PR #70 linear pull links:

- typed exterior link lift;
- generic creator intertwining;
- generic algebraic contraction intertwining;
- same-leg solder intertwining under the explicit parallel-solder hypothesis;
- distinguish affine coframe translation from exterior matter transport;
- distinguish link curvature from nonparallel-solder defect.

Construct an actual link-dependent finite differential from the lifted links and moving creators.

Prove:

- frame covariance of that differential;
- observer-adjoint covariance where required;
- flat specialization to owned `dForward`;
- corresponding Dirac specialization to owned `D_H`.

A definition such as `exteriorFlatDifferential := dForward` without deriving it from the link-dependent operator does not satisfy this package.

### 5. `A4DLocatedFrameCompatibilityBoundary.lean`

Formalize:

- common-fiber complementary-minor/cofactor identity;
- exact shifted-anchor obstruction to a naïve sitewise Lorentz action on both located colors;
- fixed located `J` unchanged;
- endpoint-aware contragredient dual link law where the types permit it;
- parity/sign boundaries.

Do not replace located `J` by a metric star.

### 6. `A4DMetricStarSignatureBoundary.lean`

Formalize:

- compound/Jacobi complementary-minor identity on a nondegenerate Lorentz fiber;
- flat Lorentz exterior-star coefficient `epsilon(S) * eta_S`;
- double-star sign `(-1)^(k*(4-k)+3)`;
- degree-one flat Lorentz metric form is `eta`, not counting `I`;
- **scoped pointwise obstruction theorem**: a purely pointwise coefficient operator cannot realize the accepted neighboring scalar first derivative;
- centered-solder pointwise blindness to the existing L=2 Nyquist witness.

The constant-factor identity alone is not the required pointwise obstruction theorem.

### 7. `ArchiveExteriorPathTransport.lean`

New mandatory synthesis-support package.

Do **not** define the missing constitutive comparison law `C_N`.

Instead, lift the already-owned PR #70 **linear path transport** to the exterior/Fock carrier and prove the functorial substrate that follows from the link lift:

- source/target typed exterior transport along an owned path word;
- identity/empty-word transport;
- concatenation/composition law;
- reversal/inverse when the underlying path transport is invertible;
- exterior lift of open/relative holonomy;
- frame covariance inherited from link transport;
- observer transport compatibility when the observer is parallel/moved according to the frame law;
- common-fiber dual contragredience and the located-anchor boundary.

Name this object as path transport (for example `TPath`, `exteriorPathTransport`), **not** as the physical constitutive `C_N`.

The research EXP decides whether this substrate can be extended to the single matter comparison/energy law.

## Migration audit from old PR #87

Old PR #87 contained useful partial implementations of:

- `ArchiveExteriorFrameLift`;
- `A4DObserverPositiveExterior`;
- `A4DRawSolderFrameAction`;
- `ArchiveAffineExteriorLink`;
- `A4DLocatedFrameCompatibilityBoundary`;
- `A4DMetricStarSignatureBoundary`.

It was blocked because several canonical requirements were only special controls or aliases.

Before reusing any code, audit it against the seven packages above.

Do not assume “old file builds” means “canonical task complete”.

## Exact capstones

At minimum provide theorem capstones for:

- generic exterior composition;
- inverse;
- generic creator covariance;
- generic contraction covariance;
- generic observer positivity;
- all-degree observer congruence;
- observer creator/contraction adjoints;
- transported-center repair covariance;
- link-dependent differential frame covariance;
- flat `dForward` specialization;
- flat `D_H` specialization;
- path-word concatenation;
- lifted relative holonomy;
- located-anchor obstruction;
- pointwise neighboring-first-jet obstruction;
- L=2 Nyquist blindness.

Add `#print axioms` for the principal capstones or the repository-accepted equivalent.

No `sorry`, `sorryAx`, or new axioms.

## Exact controls

Keep exact rational controls for:

- A/B Lorentz boost;
- all Fock degrees;
- parity;
- L=2 shifted-anchor and Nyquist witnesses;
- signed Role permutations where already relevant.

Finite exact matrices already independently checked may use `native_decide` under the repository's accepted certificate pattern.

## Lean throughput protocol

Use the new serialized helper.

During iteration:

```bash
python tools/lean_task_build.py narrow D0.Geometry.ArchiveExteriorFrameLift
python tools/lean_task_build.py narrow D0.Geometry.A4DObserverPositiveExterior
...
```

Rules:

- one execution agent/worktree owns this PR;
- no second concurrent `lake` process against the same `.lake`;
- fix the useful first error cascade before rerunning;
- if a module repeatedly takes about a minute or more, move stable base lemmas into a lower imported module before continuing;
- do not run full `D0.All` while a narrow target is red;
- do not edit a source file while a build of that file is running.

Final validation only after all narrow targets are green:

```bash
python tools/lean_task_build.py final
python 03_FORMALIZATION/tools/check_no_sorry_in_core.py --all-modules
python tools/validate_repo.py
python tools/validate_work.py
python tools/generate_lean_views.py --check
git diff --check
```

Use the literal current repository paths/flags if a validator has moved; do not resurrect obsolete commands.

Do not run `lake clean` or delete the cache.

## Truth boundaries

Do not:

- call the exterior representation Spin/Dirac spinor;
- identify `n=e_A` with physical causal time;
- identify positive `h_n` with the Lorentzian exterior form;
- modify or reinterpret located `J`;
- claim the path transport substrate is the missing physical `C_N`;
- define `H(e)` as an axiom to force the target;
- select nonlinear `Q(e)`;
- claim the missing staggered cell-energy law is solved;
- use `phi` or Tower-C data to build the fixed-level path transport;
- promote anything here to stress/Einstein dynamics.

## Exit condition

This task is complete only when all seven mandatory packages are Lean-owned, all blocking gaps from old PR #87 are closed, validation is green, the task self-retires in the same PR, and the final boundary is explicit:

`FRAME-CAR-PATH-TRANSPORT-SUBSTRATE-OWNED-CONSTITUTIVE-WORD-ACTION-MISSING`.

That terminal means the formal substrate is complete while `EXP-A4D-PATH-RESOLVED-MATTER-WORD-ACTION` still owns the missing constitutive research.
