# EXP-ASOURCE-ACTION-NATURALITY-SELECTOR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Condition on the missing scene matter amplitude already identified by A-STRESS and answer one precise question:

> Does any currently owned D0 cochain/action/naturality principle reduce the exact three-dimensional H-equivariant quadratic source class
> `Hom_H(Sym² C0, Z)`
> to a unique line (up to overall scale), or is the two-essential-parameter selector freedom terminal?

Do **not** re-audit whether the matter carrier exists. A-STRESS already classified that arrow as
`SOURCE-CARRIER-MISSING`. This task is conditional:

```text
ASSUME an abstract scene matter amplitude J : SceneC0 is supplied.
QUESTION: is the quadratic source selector into the tensor block Z internally forced?
```

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Research baseline:
`ec5c9340499a8f4f09a07796cf4992c81fbdb470`

Treat this task as fully stateless. Do not assume any prior conversational memory.

## Required CONTROL context

Read first:

- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/RESEARCH_LEDGER.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/research/ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/CLOSURE_CONTRACT.md

## Required repository files

Read literally:

1. Literal scene complex and Euclidean Hodge pairing
   - `03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean`
   - `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean`
   - `03_FORMALIZATION/D0/Topology/GenericTripartiteHomology.lean`

2. Scene spectral action
   - `03_FORMALIZATION/D0/Synthesis/SceneSpectralAction.lean`

3. Generic quadratic/bilinear operator origins
   - `03_FORMALIZATION/D0/Geometry/EdgeStiffnessOrigin.lean`
   - `03_FORMALIZATION/D0/Matter/VectorOperatorOrigin.lean`
   - `03_FORMALIZATION/D0/Matter/TraceDecompositionSigns.lean`

4. A1 action research integration
   - `02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md`

5. Current source-stratification formalization brief
   - `00_WORK/tasks/WRK-SOURCE-STRATIFICATION-NOGO.md`

6. Affected registry rows
   - `D0-HODGE-LINKS-001`
   - `D0-SPECTRAL-EINSTEIN-001`
   - `D0-SCENE-SPECTRAL-ACTION-001`
   - `D0-OPERATOR-EDGE-STIFFNESS-ORIGIN-001`

from:
https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/claims.csv

## Required attached research inputs

If available, attach:

- `MEMO_13_ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`
- `MEMO_12_ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`
- `MEMO_10_ASEL_EXHAUSTIVE_DYNAMICS_CLASSIFICATION.md`

These are research evidence, not proof owners.

---

# Frozen starting facts

Do not spend research time re-proving these from scratch except as consistency checks.

Let

[
H=S_a	imes S_b	imes S_c
]

act on the complete tripartite scene.

Let `C0` be the vertex permutation representation and

[
Z=
A_aoxtimes A_b
oplus
A_aoxtimes A_c
oplus
A_boxtimes A_c
]

be the blockwise-zero-marginal tensor sector.

Accepted A-STRESS research gives the exact character-theoretic result

[
dim Hom_H(Sym^2 C0,Z)=3.
]

The three directions are exactly the block maps

[
sigma_{AB},sigma_{AC},sigma_{BC}.
]

Thus the general H-equivariant quadratic source is

[
sigma_c(J)
=
c_{AB}sigma_{AB}(J)
+
c_{AC}sigma_{AC}(J)
+
c_{BC}sigma_{BC}(J).
]

After quotienting overall scale, two essential ratios remain.

A-STRESS also found that:

- the quadratic image spans all of `Z`;
- triangle/2-cochain sources can realise tensor-block vectors;
- H-equivariance, zero block marginals, signed divergence-freedom and total neutrality do NOT distinguish the block weights;
- three explicit completions `(1,1,1)`, `(1,2,3)`, `(1,1,0)` survive those constraints.

The question is whether **stronger owned structure** removes this degeneracy.

---

# Research programme

## 1. Triangle-factorisation classification

A-STRESS found that a tensor-block vector can be realised through the owned triangle differential.

Classify all H-equivariant bilinear maps

[
eta:C0	imes C0	o C2
]

for which

[
d_1eta(J,J)in Z.
]

Then compute the image of the induced map

[
etamapsto d_1circeta
in Hom_H(Sym^2 C0,Z).
]

Key question:

> Does factorisation through the owned triangle carrier reduce the 3-dimensional selector class?

Expected control: try a general triangle cochain of the schematic form

[
phi_{abc}
=
u,J_aJ_b
+
v,J_aJ_c
+
w,J_bJ_c.
]

Do not assume the answer.

If every block-weight triple is realised, prove surjectivity and record a clean NO-GO:
**triangle factorisation does not select the coupling**.

## 2. Exactness / Hodge constraints

Impose every meaningful owned cochain condition:

- `d1 d0 = 0`;
- exact/coexact orthogonality;
- `H^1=0`;
- Euclidean adjointness;
- membership in `ker B_-`;
- zero block marginals.

Determine whether any of these produce an equation among

[
c_{AB},c_{AC},c_{BC}.
]

A constraint already automatic for every `Z`-valued source does not count as selection.

## 3. SceneSpectralAction unit weight

The scene spectral action is instantiated with unit conformal weight

[
ho_1equiv1
]

and its EH proxy counts all scene edges uniformly.

Test very carefully whether this owned fact is enough to force

[
c_{AB}=c_{AC}=c_{BC}.
]

Distinguish:

1. “the background spectral action treats edges with unit weight”;
2. “the matter coupling coefficient on all edge orbits is forced equal”.

The second does NOT follow from the first without a theorem connecting the actions.

If no such theorem exists, say so explicitly.

## 4. Edge-local universal action

Classify quadratic matter-edge interactions satisfying a **single universal local edge law**:

[
S_{int}
=
sum_{e={x,y}} F(J_x,J_y,h_e)
]

with the same polynomial/form on every edge.

At lowest nontrivial degree, test candidates such as

[
h_{xy}J_xJ_y,
qquad
h_{xy}(J_x-J_y)^2,
qquad
w_{xy}(J_x-J_y)^2.
]

After variation with respect to the edge/gravity variable and projection to `Z`, compute the resulting block-weight triple.

Questions:

- Does “same local law on every edge” select a unique line in the 3D class?
- Is that principle already owned anywhere in D0?
- Or is it a new modelling axiom equivalent to choosing the line by hand?

Do not confuse mathematical uniqueness *inside an assumed action ansatz* with ownership of the ansatz.

## 5. Dirichlet-energy / metric-variation route

Given an abstract scalar-like `Jin C0`, study the canonical finite Dirichlet energy

[
E(J;w)
=
rac12sum_{e={x,y}}w_e(J_x-J_y)^2.
]

Ask whether variation with respect to edge weights, edge lengths, or a scene metric variable yields a source whose `Z`-projection defines one distinguished block-weight triple.

Compute it exactly on `K(a,b,c)`.

If the result lies outside the A-STRESS `J_xJ_y` family before projection but becomes a fixed member after `P_Z`, state the exact relation.

Then audit whether D0 owns the required matter scalar action and metric variable.

## 6. Cochain-product route

Search the repository for an owned cup product, Alexander–Whitney product, wedge product, or graded cochain multiplication.

If none is owned, that absence itself is relevant.

Independently test standard finite-cochain candidates:

[
dJsmile dJ,
qquad
Jsmile dJ,
qquad
delta(dJsmile dJ),
]

or the correct degree-compatible analogues.

The goal is not to import algebraic topology jargon but to determine whether a standard **canonical cochain product** would select one of the three block directions or one fixed combination.

If such a construction works only after adding a new cup-product primitive, classify it as a bridge/modelling primitive, not CORE.

## 7. Naturality under zone relabelling

H-equivariance does not exchange the three unequal edge orbits.

Strengthen the notion of naturality to the family of ordered scenes `K(a,b,c)`.

Classify coefficient functions

[
(c_{AB},c_{AC},c_{BC})
=
F(a,b,c)
]

compatible with relabelling the three zone labels.

Does functoriality reduce the freedom to:

- one universal constant;
- a finite-dimensional family of symmetric/rational functions of `a,b,c`;
- or still an infinite family?

Be explicit.

A zone relabelling that changes `K(a,b,c)` to an isomorphic relabelled presentation is allowed; do not invent an internal `S_3` automorphism when `a,b,c` are unequal.

## 8. Compatibility with A1 source normalization

A1 has a finite quadratic action with edge weight

[
W_e=1/(ho_iho_j).
]

Condition on the A-CPL unit-weight completion `W=I` and ask whether sharing the same edge pairing between A1 and the new matter source would force equal block weights.

Then remove the unit-weight assumption and classify the weighted case.

Does A1 compatibility select the source coupling, or merely transfer the same unresolved weight choice?

## 9. Compatibility with Hodge kinetic operator

Impose compatibility with the accepted Hodge candidate `Q_H`.

Test possible requirements such as:

[
Q_Hsigma_c(J)
=
sigma_c(mathcal L J)
]

for some owned vertex operator `mathcal L`, or action reciprocity with the Hodge energy.

Classify whether any nontrivial intertwining equation fixes ratios among `c_{AB},c_{AC},c_{BC}`.

If no canonical vertex operator is owned, do not invent one silently.

## 10. EdgeStiffnessOrigin

Audit whether the owned generic bilinear object

[
edgeStiffness(P,H)
]

can select the three block coefficients after literal scene specialization.

Required answer:

- exact types;
- what must be chosen for `P,H`;
- whether those choices are owned;
- resulting block weights;
- whether the construction is genuinely new information or simply hides the three free coefficients inside `P,H`.

## 11. Strong negative control

If no owned principle selects a line, prove the strongest possible terminal NO-GO.

Construct at least two inequivalent block-weight triples that survive **all** tested owned principles:

- triangle factorisation;
- exactness/Hodge constraints;
- unit scene metric where relevant;
- any genuinely owned locality/naturality condition;
- A1 pairing compatibility if applicable.

The negative control must survive the *strongest* internally justified condition set, not merely H-equivariance.

## 12. Strong positive target

If a selector is found, give:

[
(c_{AB}:c_{AC}:c_{BC})
]

exactly.

Then distinguish:

- forced by an owned theorem;
- forced conditional on a new action ansatz;
- forced conditional on a new cochain-product primitive.

Only the first is `CORE-CLOSABLE`.

## 13. Terminal classification

Return exactly one primary verdict:

- `CORE-SELECTOR-FOUND`
- `ACTION-SELECTOR-CONDITIONAL`
- `COCHAIN-PRODUCT-BRIDGE`
- `SELECTOR-NOGO-TERMINAL`
- `NATURALITY-STILL-UNDERDETERMINED`

## 14. Required final block

```text
starting quadratic selector dimension:
triangle-factorisation image dimension:
does triangle factorisation fix ratios:
does Hodge exactness fix ratios:
does SceneSpectralAction unit weight fix ratios:
universal edge-local action result:
Dirichlet variation result:
owned cochain product available:
cochain-product selector result:
zone-relabel naturality residual dimension:
A1 compatibility result:
Q_H compatibility result:
EdgeStiffnessOrigin relevance:
strongest surviving inequivalent completions:
selected block ratio, if any:
is the selecting principle owned or new:
impact on A-STRESS selector NO-GO:
impact on D0-HODGE-LINKS-001:
smallest future theorem/certificate:
terminal verdict:
```

## Deliverable

`MEMO_14_ASOURCE_ACTION_NATURALITY_SELECTOR.md`

No repository edits.

This task is **not** allowed to reopen the missing matter-carrier question. Work conditionally on an abstract
scene matter amplitude and decide only whether the quadratic selector is internally forced.
