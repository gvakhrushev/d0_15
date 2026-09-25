# WRK-A4D-RESOLVED-CORRELATED-ACTION-PASSPORT

## Class

WORKER

## Parent

`CTRL-A4D-EQUIVARIANT-MIXED-BACKGROUND-CLOSURE`

## State

PLANNED

## Objective

Lean-own the **algebraic resolved correlated-action passport** isolated by research
PR #130 (`MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md`, §§27–32).

Do **not** formalize topology / limits / sequence continuity here. Own the finite-
dimensional exact algebraic layer on which a later continuity worker can stand
without reopening the research.

## Read first

- `02_REGISTRY/research/MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md` §§27–32;
- landed `03_FORMALIZATION/D0/Geometry/A4DRelativeAEComparisonSpan.lean` (do not fork);
- PR #130 research statements on projector-incidence resolution.

## Preferred module

`03_FORMALIZATION/D0/Geometry/A4DResolvedCorrelatedActionPassport.lean`

Namespace: `D0.Geometry.A4DResolvedCorrelatedActionPassport`

Reuse ComparisonSpan names for kernel / complement / canonical correlated action
/ residual. If #132 is not yet merged, do not depend on its new names.

## Frozen definitions

For `B,S : LabelCoeff →ₗ[ℝ] V` the repo already owns

- `K = coefficientKernel B`, `H = coefficientComplement B`,
- canonical correlated action `C = canonicalOnCoeff B S = S ∘ P_H`,
- residual action `D = canonicalResidual B S = S ∘ P_K`,
- and `S = C + D`.

PR #130 introduces an incidence projector `Π` with `B ∘ Π = B`. On an admissible
orthogonal resolution lift

```
im Π = H ⊕ W,   W ≤ K,
```

one has `Π = P_H + P_W`. Define the resolved correlated action

```
resolvedCorrelatedAction B S Π := S ∘ Π.
```

## Mandatory theorem package

1. Incidence: `B ∘ (P_H + P_W) = B` for `W ≤ K`.
2. Jump identity: `resolvedCorrelatedAction − C = S ∘ P_W`.
3. Since `W ≤ K`, `S ∘ P_W = D ∘ P_W`, hence
   ```
   resolvedCorrelatedAction − C = D ∘ P_W.
   ```
4. Intrinsic lift (`W = ⊥`, `Π = P_H`): resolved action equals `C`.
5. Maximal lift (`W = K`, `Π = id`): resolved action equals `S`, and
   ```
   resolvedCorrelatedAction − C = D.
   ```
   Formal owner of: "`D` is the maximal full-rank jump operator."
6. Role residual form: with `R_r = D (EuclideanSpace.single r 1)`,
   ```
   (resolvedCorrelatedAction − C) (EuclideanSpace.single r 1) = R_r
   ```
   on the maximal lift. Keep the ComparisonSpan / memo sign convention.
7. Exact-gauge invisibility: if `S = T ∘ B` (equivalently SpanCalibration /
   exact chart), then for every admissible incidence projector `S ∘ Π = S`.
8. Coframe-only boundary (`B = 0`): intrinsic `Π = 0` gives resolved `0`;
   maximal `Π = id` gives resolved `S`. Algebraic witness of approach-dependence
   only — not a continuity theorem.

## Hostile controls (exact Lean)

1. intrinsic lift;
2. maximal lift;
3. nonzero `D` produces a distinct resolved action;
4. exact gauge makes the lift invisible;
5. `B = 0`, `S ≠ 0` separates intrinsic and maximal resolutions.

## Firewalls

No convergence, Moore–Penrose continuity, cluster projectors, all-sequence
criterion, selector `Q_o`, finite dressing `F`, stress/Einstein, continuum,
physical time, golden refinement, or a new physical quotient.

## Exit condition

Lean owns `Ĉ = SΠ`, `Ĉ − C = D P_W`, maximal jump `= D`, Role-residual
specialization, exact-gauge resolution independence, and coframe-only
intrinsic/maximal separation. No `sorry`. No new axioms. No self-merge.

## GitHub-first

1. fresh branch from current main (≥ `4527bd8937fd4888704197b571e9a3f94dfa6f29`);
2. `python tools/task_lifecycle.py start WRK-A4D-RESOLVED-CORRELATED-ACTION-PASSPORT`;
3. commit lifecycle-only changes;
4. open Draft PR;
5. only then add Lean;
6. narrow build; full `D0.All`;
7. self-retire before Ready;
8. `Lifecycle: REVIEW`;
9. do not self-merge.
