# EXP-A4D-GOLDEN-ROLE-PHASE-CORRESPONDENCE-INDEX-RULE

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED once PR #104 lands on `main`.

Primary durable input:

`02_REGISTRY/research/MEMO_A4D_GOLDEN_ROLE_PHASE_CARRIER_OPERATOR_WELD.md`.

Also read completely:

- `02_REGISTRY/research/MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD.md`;
- `02_REGISTRY/research/ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`;
- `03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DGoldenRolePhaseRGDefect.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DGoldenCarrierWeldBoundary.lean`;
- the Role-phase product carrier/projection owners.

The parallel Lean worker
`WRK-A4D-GOLDEN-CARRIER-WELD-BOUNDARY`
may proceed independently. Do not wait for it, but treat the repaired PR #104 statements as
the truth firewall and do not outrun their scope.

## Frozen boundary

Keep distinct:

```text
k = Bratteli / AF depth
n = Role-phase period
L = n+2
```

Do not set `k=n`.
Do not impose `L=F_m` or another Fibonacci/Lucas period law by definition.

Frozen negative results:

- PR #99 `c=phi` is scalar only;
- owned consecutive Role-phase bonding is set-level, not a nontrivial group hom;
- no unital `A_k -> C(B_n)` hom exists for `k>=2`;
- reverse representations `C(B_n)->A_k` can exist noncanonically;
- Tower C has no owned `S_4` action;
- finite cardinality/GNS mismatch is only a bounded control, not a global arithmetic no-go.

## Objective

Construct or terminally classify the first **refinement-compatible finite-dimensional
`A_k`–`C(B_n)` correspondence family** and determine whether its compatibility equations
derive a non-ad-hoc relation between `k` and `n`.

The task is not to invent an abstract `Correspondence` record.

Exploit the actual classification of finite-dimensional correspondences.

For finite `B_n`:

```text
C(B_n) = product_{x in B_n} C.
```

A finite right Hilbert `C(B_n)`-module decomposes fiberwise:

```text
X_{k,n} = direct_sum_{x in B_n} X_x.
```

A left representation of

```text
A_k = M_{a_k}(C) oplus M_{b_k}(C)
```

on each fiber is classified by a multiplicity pair

```text
m_{k,n}(x) = (p_x, q_x) in N^2.
```

Use this concrete multiplicity data as the primary research coordinate system.

## Central questions

1. What is the exact finite-dimensional classification of
   `A_k`–`C(B_n)` Hilbert correspondences up to unitary equivalence?
2. What does the Role permutation action on `B_n` require of the multiplicity field?
3. With a trivial Tower-C action as a control, are multiplicities exactly constant on
   `S_4` orbits? What information survives?
4. Is there any already-owned nontrivial automorphism/action of the two Bratteli vertices
   or AF stage that can serve as an `S_4` action without arbitrary choices?
5. How does restriction along the AF inclusion
   `A_k -> A_{k+1}` transform multiplicity vectors?
6. How do pullback and pushforward along
   `p_n : B_{n+1} -> B_n` transform the fiber multiplicities?
7. Can either refinement orientation give a commuting/base-change square?
8. Do the resulting integer equations force or obstruct a relation between `k` and `n`?
9. Does Role-phase nonuniform fiber multiplicity `1/2` per coordinate obstruct a
   Bratteli-incidence law with matrix `M_phi`?
10. Can a stochastic/weighted correspondence repair the integer obstruction without merely
    inserting `phi` as an external scalar?
11. If an index rule emerges, does `phi` follow from the correspondence/refinement law,
    or does it remain an independent probe?
12. Only after a derived finite comparison exists: can it supply the `P` consumed by
    PR #99's operator/energy residual interface?

## Mandatory attack order

### A. Classify one finite stage exactly

Write a theorem-level mathematical classification:

```text
finite A_k-C(B_n) correspondence
<-> multiplicity field B_n -> N^2
```

with all needed nondegeneracy/fullness qualifications stated explicitly.

Separate:

- bare correspondence existence;
- faithful left action;
- full right module;
- imprimitivity/Morita equivalence.

Do not conflate these classes.

### B. Role action audit

The Role action on `B_n` is owned.

First use the trivial action on `A_k` as a hostile control.

Derive the exact condition for an equivariant correspondence. Expected control:

```text
m(sigma.x) = m(x)
```

up to the correct notion of unitary equivalence, so multiplicity data descend to
`S_4` orbits.

Then search the repository for any nontrivial canonical action on the two Bratteli
vertices / AF blocks. If none exists, record that as a missing datum rather than a
universal no-go.

### C. AF refinement equation

Use the literal Fibonacci inclusion orientation.

If a stage-`k+1` representation is restricted along
`A_k -> A_{k+1}`, compute the exact transformation of its two multiplicities by the
incidence matrix `M_phi` (or its transpose according to the verified convention).

Do not guess the orientation.

Write the resulting recurrence explicitly.

Audit the inverse-incidence positivity issue:

```text
M_phi^{-1} = [[0,1],[1,-1]]
```

and determine exactly which refinement orientation, if any, forces negative
multiplicities after iteration.

A no-go here must be scoped to that orientation/class.

### D. Role-phase pullback and pushforward

For

```text
p_n : B_{n+1} -> B_n
```

derive separately:

- pullback/base-change of a Hilbert module;
- pushforward/direct-image fiber sum.

For pushforward, use the literal nonuniform fibers of the coordinatewise modulo map.
Track the full four-Role fiber multiplicities (products of one- and two-point coordinate
fibers).

Do not replace them by an average `phi`.

### E. Refinement squares

Test at least these candidate squares:

1. AF restriction vs B pullback;
2. AF induction/extension vs B pullback;
3. AF restriction vs B pushforward;
4. AF induction/extension vs B pushforward.

For each, state the exact integer/multiplicity equation.

Use small exact stages to determine whether the equation is:

- solvable canonically;
- solvable noncanonically;
- obstructed;
- solvable only on a restricted orbit/subsequence.

### F. Index-rule extraction

An index relation is accepted only if it is forced by one of the exact refinement
equations or another owned invariant.

Forbidden shortcuts:

- `k=n`;
- `n+2=F_m`;
- choosing the nearest cardinality;
- matching dimensions only asymptotically;
- using `phi` to define the relation.

If the equations select a subsequence, prove why that subsequence is canonical in the
comparison class.

### G. Weighted/stochastic repair

If integer correspondences fail, test a strictly weaker class:

- Markov kernel;
- measured correspondence;
- positive `C(B_n)`-module weights;
- CP map compatible with the AF trace.

State exactly what structure is lost when moving away from a Hilbert bimodule with
integer representation multiplicities.

A weighted repair is not allowed to hide the desired `phi` in its definition.

### H. Residual interface

Only after an actual comparison law has been derived, ask whether it induces a
one-dimensional phase comparison `P` of the type required by PR #99.

Then evaluate separately:

- operator residual;
- energy residual.

Do not infer one from the other.

### I. Downstream firewall

Do not touch:

- located `J`;
- `D_H`;
- `H(e)`;
- physical time;
- stress;
- Einstein dynamics.

This lane is a Tower-C/Tower-B representation/refinement problem only.

## Exact hostile controls

At minimum compute exactly:

- `k=0..6` AF block sizes and incidence;
- `n=0..6` Role-phase carriers;
- `S_4` orbit decomposition for small `L`;
- pullback multiplicity transport;
- pushforward fiber-size patterns;
- the `M_phi` and `M_phi^{-1}` multiplicity recurrences;
- delta/orbit-local multiplicity fields;
- constant multiplicity fields;
- faithful-left-action controls;
- full-right-module controls;
- at least one nontrivial Bratteli step crossed with one literal Role-phase step.

Use exact integer/rational arithmetic.

## Allowed terminal forms

Examples:

- `GOLDEN-ROLE-PHASE-CORRESPONDENCE-REFINEMENT-WELD-CONSTRUCTED`;
- `GOLDEN-ROLE-PHASE-CORRESPONDENCE-CONSTRUCTED-INDEX-RULE-MISSING`;
- `GOLDEN-ROLE-PHASE-INTEGER-CORRESPONDENCE-SCOPED-NOGO-WEIGHTED-CLASS-OPEN`;
- `GOLDEN-ROLE-PHASE-CORRESPONDENCE-NEW-ACTION-PRIMITIVE-REQUIRED`;
- `GOLDEN-ROLE-PHASE-CORRESPONDENCE-INDEX-PRIMITIVE-REQUIRED`.

Use the strongest wording justified by the exact exhausted class.

## Deliverable

One durable theorem-ready memo in `02_REGISTRY/research/` containing:

- exact correspondence classification;
- Role action/equivariance law;
- exact AF multiplicity refinement;
- exact B pullback/pushforward law;
- all tested commuting squares;
- index-rule result;
- weighted/stochastic fallback if needed;
- PR #99 residual test only if a derived comparison exists;
- hostile controls;
- terminal verdict;
- theorem-ready handoff;
- exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start EXP-A4D-GOLDEN-ROLE-PHASE-CORRESPONDENCE-INDEX-RULE`;
3. immediately open Draft PR before research edits;
4. research and durable memo only inside that PR;
5. keep PR metadata synchronized;
6. before Ready: self-retire with `tools/task_lifecycle.py`;
7. Ready with `Lifecycle: REVIEW`;
8. do not self-merge.

## Truth firewall

Do not infer:

- `k=n`;
- `n+2=F_m`;
- a Tower-C `S_4` action that is not owned;
- nonexistence of reverse representations `C(B_n)->A_k`;
- global perfect-power arithmetic from finite checks;
- a carrier weld from `c=phi`;
- operator residual zero from energy residual zero;
- `J`, `D_H`, `H(e)` naturality;
- physical time, stress, or Einstein closure.

## Exit condition

The surviving finite-dimensional correspondence class is reduced to explicit multiplicity
data and exact refinement equations, and those equations either produce a canonical
Role-compatible index rule/comparison or identify the earliest additional action/index
primitive without ad-hoc Fibonacci period insertion.
