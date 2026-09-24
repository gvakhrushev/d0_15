# EXP-A4D-GOLDEN-ROLE-PHASE-CARRIER-OPERATOR-WELD

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED.

Required landed inputs:

- PR #86 `MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD.md`;
- PR #99 `A4DGoldenRolePhaseRGDefect` and `A4DGoldenCarrierWeldBoundary`;
- `ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`;
- existing Tower-B Role-phase projection/RG owners;
- existing Tower-C Fibonacci/Bratteli/AF/Perron owners.

## Frozen terminal

The scalar interface is now Lean-owned:

```text
goldenScaleProbe k = phi
goldenRGResidual n k P = 0
  iff RenormalizedProjectiveCompatibility n P phi
```

with Bratteli depth `k` and Role-phase period `n` kept distinct.

This is not a carrier weld.

Current terminal:

`GOLDEN-RG-DEFECT-INTERFACE-LEAN-OWNED-CARRIER-WELD-MISSING`.

## Objective

Construct or terminally classify the **first actual typed Tower-C ↔ Tower-B carrier/operator comparison** beyond a shared scalar probe.

The task must first decide the correct comparison layer.

Possible layers include:

- finite carrier map/correspondence;
- map between function spaces;
- algebra representation;
- trace/GNS correspondence;
- bimodule/correspondence;
- reindexed subsequence/functor.

Do not assume a pointwise carrier map is the correct object.

Do not identify the natural-number indices of the two towers.

## Central questions

1. What are the literal finite-stage objects of Tower C and Tower B that can actually be compared?
2. Is there any canonical or geometrically forced index relation `k -> n`, subsequence, or correspondence?
3. Can Tower-C cylinder/AF data induce functions, measures, modules or operators on the Role-phase carrier without arbitrary label choices?
4. Can such a comparison commute with the owned refinements/bondings?
5. Can the owned golden scalar probe arise as a consequence of the comparison rather than being inserted independently?
6. Does the Tower-B operator residual vanish for any derived comparison?
7. Is Role permutation/equivariance compatible with the proposed weld?
8. What do cardinality, fiber and representation-dimension constraints exclude?
9. Is a representation-level or GNS-level weld possible even when point-carrier identification is not?
10. What is the earliest object needed before one can even ask for inter-level `D_H`, located-`J`, or `H(e)` naturality?

## Mandatory attack order

### A. Literal tower audit

Write down exact current owners and types for:

Tower B:

- `ArchiveRolePhaseGroup n`;
- coordinate projection;
- scalar Laplacian/RG residual;
- Role action.

Tower C:

- Bratteli/cylinder finite stages;
- AF inclusions;
- Perron vector/trace;
- scale flow;
- available GNS/module structure.

Do not use Tower A record/profinite carrier as a substitute.

### B. Index separation

Keep distinct:

- Role-phase period `n`;
- Bratteli depth `k`;
- record depth;
- history tick.

If an index relation is proposed, derive it from a commuting diagram or structural invariant.

### C. Direct carrier/correspondence candidates

Try the strongest natural finite candidates.

Audit:

- cardinalities;
- fibers;
- equivariance;
- composition with refinement;
- dependence on arbitrary labels/orderings.

A cardinality mismatch rules out only the corresponding class of bijective maps, not every correspondence.

### D. Function-space / algebra candidates

If point carriers do not match, test:

- pull/push maps on functions;
- stochastic/Markov correspondences;
- algebra homomorphisms;
- modules/bimodules;
- GNS isometries/intertwiners.

State exactly which structure is preserved.

### E. Refinement square

A positive candidate must give a typed commuting or defect-bearing square between the two tower refinements.

Measure the defect explicitly.

Do not define the map by forcing the defect to vanish.

### F. Golden scalar emergence

Only after a comparison exists, ask whether its normalization/trace/operator scaling forces the scalar `phi`.

Using `goldenScaleProbe = phi` as a supplied parameter does not construct the weld.

### G. Operator test

Feed the derived comparison into the already-owned Tower-B residual interface.

Determine:

- exact zero;
- explicit nonzero defect;
- required correction;
- restricted subsequence behavior.

Keep operator-entry and energy residuals distinct.

### H. Role equivariance

Test the finite Role permutation action and coordinatewise projection.

A comparison that requires a distinguished Role without an owned reason is noncanonical.

### I. Downstream firewall

Do not attempt `J`, corrected `D_H`, or `H(e)` inter-level intertwining until a genuine carrier/function/algebra comparison exists.

They may be listed as later obligations, not used to define the first weld.

## Exact hostile controls

At minimum:

- first several Bratteli depths;
- first several Role-phase periods;
- exact finite cardinalities/dimensions;
- first-step fiber data;
- Role permutations;
- Perron trace identities;
- scalar `phi` probe;
- nearest-neighbor exact-projective negative control;
- operator residual entries;
- energy residual separately.

Use exact arithmetic.

## Allowed terminal forms

Examples:

- `GOLDEN-ROLE-PHASE-CARRIER-WELD-CONSTRUCTED`;
- `GOLDEN-ROLE-PHASE-REPRESENTATION-WELD-CONSTRUCTED-POINT-CARRIER-MISSING`;
- `GOLDEN-ROLE-PHASE-CARRIER-WELD-SCOPED-NOGO`;
- `GOLDEN-ROLE-PHASE-WELD-NEW-PRIMITIVE-REQUIRED`.

Use scoped wording matching the class actually exhausted.

## Deliverable

One durable theorem-ready memo with:

- exact tower types;
- attempted comparison classes;
- positive maps/correspondences;
- commuting/defect diagrams;
- exact finite controls;
- operator/energy residual results;
- index and Role-equivariance audit;
- terminal verdict;
- theorem-ready handoff;
- exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch;
2. `python tools/task_lifecycle.py start EXP-A4D-GOLDEN-ROLE-PHASE-CARRIER-OPERATOR-WELD`;
3. immediately open Draft PR before research edits;
4. keep all durable research inside that PR;
5. self-retire before Ready;
6. `Lifecycle: REVIEW`;
7. do not self-merge.

## Truth firewall

Do not infer:

- `k=n`;
- physical time from golden depth;
- a carrier weld from `c=phi`;
- Tower-A/Tower-B identity;
- located-`J`, `D_H`, or `H(e)` naturality before the carrier/function-space weld;
- stress or Einstein dynamics.
