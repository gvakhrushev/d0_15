# EXP-AWEIGHT-A1-CONFORMAL-WEIGHT-SELECTOR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Terminally classify the remaining A1 conformal-weight ambiguity.

A-CPL established only a conditional statement:

> if the A1 conformal weight is identified with the unit scene weight, then W=I and the Euclidean C1 map U is already the physically relevant source/carrier isometry.

That identification is not owned.

This task asks one precise question:

> What do the currently owned D0 symmetries, pairings, C1/Hodge compatibility conditions and action principles actually force about the positive vertex weight rho in
>
> [
> W_{ij}=rac1{ho_iho_j},
> ]
>
> and is `rho ≡ 1` internally derivable, or does a genuine finite weight-selector freedom remain?

A terminal NO-GO is fully acceptable.

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Research baseline:
`892f01bf2fe5a5412683e1df1a356536b355b74b`

Treat this task as fully stateless.

## Required CONTROL context

Read first:

- `02_REGISTRY/RESEARCH_LEDGER.md`
- `02_REGISTRY/research/ANORM_FINITE_GRAVITY_NORMALIZATION.md`
- `02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`
- `02_REGISTRY/CLOSURE_CONTRACT.md`

Do not reopen A-STRESS/A-SOURCE or A-NORM.

Frozen boundaries:

- matter→SceneC0: `SOURCE-CARRIER-MISSING`;
- quadratic source selector: `SELECTOR-NOGO-TERMINAL`;
- finite Hodge+A1+two-tick normalization: two independent moduli `(m^2,gamma)` remain after all genuine quotients.

This task is only about the A1 vertex/edge weight `rho/W`.

## Required literal repository files

Read literally:

1. A1 research owner / implementation target
   - `02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md`
   - `04_CERTIFICATES/vp_a2_compensator_noether.py`

2. Current A1 worker brief
   - `00_WORK/tasks/WRK-GRAV-COMPENSATOR-NOETHER.md`

3. Literal C1 owner
   - `03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean`

4. Literal source/Hodge owners
   - `03_FORMALIZATION/D0/Geometry/SceneSourceStratification.lean`
   - `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean`
   - `03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean`

5. Scene spectral action
   - `03_FORMALIZATION/D0/Synthesis/SceneSpectralAction.lean`

6. Endogenous action scale
   - `03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean`

7. Registry rows
   - `D0-A2-COMPENSATOR-NOETHER-RESEARCH-001`
   - `D0-C1-COMMON-CARRIER-RESEARCH-001`
   - `D0-SCENE-SPECTRAL-ACTION-001`
   - `D0-HODGE-LINKS-001`

from `02_REGISTRY/claims.csv`.

## Required attached research inputs

If available:

- `MEMO_08_ACPL_WEIGHTED_SOURCE_ACTION_COUPLING.md`
- `MEMO_15_ANORM_FINITE_GRAVITY_NORMALIZATION.md`
- previous C1/A-Omega memo if relevant.

These are research evidence, not proof owners.

---

# Frozen algebra

A1 uses

[
S_{A1}(h,ho)
=
2sum_{{i,j}}
rac{h_{ij}^2}{ho_iho_j},
qquad
W_{ij}=rac1{ho_iho_j}.
]

The compensator completion preserves the same positive diagonal edge weight W.

For fixed positive W, compensator elimination gives the W-orthogonal physical representative and

[
G_{m phys}=4Ww,
qquad
B_+G_{m phys}=0.
]

The A1 gauge/Noether mechanism itself works for arbitrary positive rho.

The literal scene Hodge/C1 pairing currently owned in Lean is Euclidean/counting.

`SceneSpectralAction` defines a separate unit conformal background

[
ho_1equiv1.
]

No owned theorem currently identifies the A1 rho with that rho1.

---

# Research programme

## 1. Classify H-invariant positive vertex weights

Let

[
H=S_9	imes S_{11}	imes S_{13}.
]

Classify all positive functions

[
ho:SceneVertex	omathbb R_{>0}
]

fixed by H.

Expected form:

[
ho=
(r_9,r_{11},r_{13})
]

constant on each zone.

Prove this exactly.

Then quotient any genuine global normalization redundancy and count the projective weight moduli.

Do not assume a global scale is redundant until its effect on the A1 action and response is audited.

## 2. Induced edge-weight class

For zone-constant rho compute the three edge-block weights

[
w_{9,11}=rac1{r_9r_{11}},
quad
w_{9,13}=rac1{r_9r_{13}},
quad
w_{11,13}=rac1{r_{11}r_{13}}.
]

Determine whether every positive triple of block weights arises from a positive vertex triple, and give the inverse formulas.

This tells whether the vertex factorisation itself imposes any real selector relation.

## 3. A1 gauge/Noether constraints

Determine whether any of the following constrain rho:

- finite shift invariance;
- off-shell Ward identity;
- compensator solvability;
- positivity of W;
- uniqueness of the projected physical field w;
- zone-constant pure-gauge theorem;
- sign-indefiniteness no-go.

If all hold for arbitrary positive rho, prove the non-selection explicitly.

## 4. H-equivariance of the A1 action

If rho is treated as fixed background data, require the A1 action and response to be H-equivariant.

Does this force exactly zone-constancy and nothing more?

Construct two non-proportional positive zone-weight triples satisfying full H-equivariance and all A1 identities.

## 5. C1 U as a weighted isometry

This is load-bearing.

The accepted C1 map U is Euclidean-isometric and acts nontrivially only through the centered-row reflection on the 11–13 block.

For a general positive edge-diagonal metric W induced by rho, compute exactly when

[
langle UX,UYangle_W=langle X,Yangle_W
]

on the relevant carrier.

Classify:

- arbitrary vertex-dependent rho;
- zone-constant rho;
- block-scalar edge weights;
- fully uniform weight.

Key question:

> Does weighted C1 compatibility force all three zone weights equal, or does U remain an isometry for every block-scalar W?

Give a theorem, not numerical examples.

## 6. Hodge pairing compatibility

The literal `SceneHodgeDecomposition` uses Euclidean/counting pairings.

Distinguish at least three notions:

1. C1 map U is an isometry for the A1 W-pairing;
2. A1 W-pairing is proportional to the Hodge edge pairing;
3. the A1 and Hodge actions are terms of one common parent action using one edge metric.

Determine what each condition forces.

Expected possibility:

- condition 1 may leave all block-scalar W;
- condition 2 may force W=cI and hence uniform rho up to one scale;
- condition 3 may additionally require a relative-action theorem not currently owned.

Do not collapse these levels.

## 7. Does W=cI imply uniform rho?

For positive zone constants prove the exact implication

[
rac1{r_9r_{11}}
=
rac1{r_9r_{13}}
=
rac1{r_{11}r_{13}}
Longrightarrow
r_9=r_{11}=r_{13}.
]

Then classify the remaining common scale.

Does overall action normalization or field normalization remove that scale?

If yes, state precisely how; if no, count it.

## 8. SceneSpectralAction unit background

Audit whether the owned fact

[
ho_1equiv1
]

is:

- a definition chosen for one spectral-action instantiation;
- a canonical theorem selecting the unique scene conformal weight;
- or a background convention independent of A1.

Search for any theorem linking the spectral-action rho argument to the A1 rho argument.

If none exists, construct two A1 rho choices that preserve every owned SceneSpectralAction theorem unchanged.

This is required for a terminal no-go.

## 9. Perron/degree profiles

The old registry blocker asked for a Perron profile. A-CPL classified that as a category error.

Audit the relevant repository definitions only enough to prove the distinction:

- what type/carrier is the Perron object?
- what role does it own?
- does any theorem make it an A1 conformal weight?

Do not revive Perron as a candidate unless a literal typed bridge exists.

## 10. Endogenous action scale

Test whether `S_min=1` can remove the remaining common rho scale.

The question is subtle:

[
homapsto cho
Longrightarrow
Wmapsto c^{-2}W
]

rescales the A1 action.

Does the endogenous action quantum fix this scale for A1 specifically, or only the global unit after a physical action is already selected?

Separate global action-unit calibration from relative/field-background selection.

## 11. Source duality / reciprocity

A-CPL discussed a source dual map induced by W.

Determine whether requiring source-response reciprocity, C1 transport and the owned Euclidean signed-current carrier imposes any condition on the zone ratios.

If reciprocity simply uses the chosen W and works for every positive block triple, prove that route non-selecting.

## 12. Local scale symmetry

A1 research distinguishes the preferred C' completion from a normalized-variable C'' alternative with local scale symmetry.

Determine whether demanding local scale covariance/invariance selects rho, or instead enlarges the gauge freedom so that rho becomes less physical.

Do not select C'' merely because it has more symmetry; classify the consequence.

## 13. Naturality across K(a,b,c)

As a secondary control, classify zone-constant weight assignments

[
(r_a,r_b,r_c)=F(a,b,c)
]

natural under relabelling of the three zones.

Does family naturality select uniform weights, degree weights, Perron-like weights, or an infinite function family?

This prevents accidental selection from one frozen triple.

## 14. Strong negative control

If no owned theorem fixes rho, provide at least two explicit positive rho choices on K(9,11,13) satisfying all genuinely owned A1/C1 symmetry and gauge constraints.

Prefer one uniform and one nonuniform zone-constant choice.

Show an observable A1 quantity differs:

- block response scaling;
- W-inner product;
- reduced action;
- source dual map.

Thus the choices are not merely notational.

## 15. Strong positive target

If a selector exists, give the exact theorem chain that forces

[
hopropto1
]

or (ho=1) exactly.

Classify the selecting principle as:

- already owned CORE;
- conditional on identifying A1 and Hodge edge metrics;
- conditional on a new common parent action;
- external calibration.

Only the first permits `CORE-WEIGHT-FOUND`.

## 16. Impact on A-NORM

Determine whether resolving rho changes either of the A-NORM finite moduli

[
m^2,gamma.
]

Possibilities:

- rho selection is independent and leaves both;
- one normalization modulus is partly a hidden rho choice;
- the moduli count changes.

Prove the relationship.

## 17. Terminal verdict

Return exactly one primary verdict:

- `CORE-WEIGHT-FOUND`
- `UNIFORM-WEIGHT-BRIDGE`
- `ONE-WEIGHT-MODULUS-LEFT`
- `TWO-WEIGHT-MODULI-LEFT`
- `WEIGHT-SELECTOR-NOGO-TERMINAL`

## 18. Required final block

```text
H-invariant rho class:
raw positive weight parameters:
projective/global-scale quotient:
induced edge-block weights:
does vertex factorisation constrain edge weights:
does A1 gauge invariance constrain rho:
does full H-equivariance constrain beyond zone constancy:
weighted-isometry condition for U:
does C1 compatibility force uniform weight:
does Hodge-pairing identification force uniform weight:
is Hodge-pairing identification owned:
does SceneSpectralAction rho1=1 select A1 rho:
does Perron/degree data select A1 rho:
does S_min=1 fix the remaining scale:
does reciprocity fix zone ratios:
local-scale symmetry consequence:
naturality residual family:
strongest two inequivalent surviving rho choices:
number of genuine A1 weight moduli:
impact on A-NORM (m^2,gamma):
smallest future theorem/certificate:
impact on D0-HODGE-LINKS-001:
terminal verdict:
```

## Deliverable

`MEMO_16_AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`

No repository edits.

Separate:

- repository-owned theorem;
- accepted research;
- new theorem;
- convention/gauge;
- modelling bridge;
- external calibration.

Do not identify a unit spectral background with the A1 physical weight without a typed theorem.
