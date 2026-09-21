# EXP-ASTRESS-QUADRATIC-MATTER-TENSOR-SOURCE

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Determine whether the **owned D0 matter/source layer** already contains, or can canonically generate,
the quadratic matter-to-edge tensor source required by accepted A-RAD research.

A-RAD proved a structural boundary:

- every linear H-equivariant vertex source is orthogonal to the canonical zero-marginal tensor block;
- the tensor block is nevertheless reached by triangle sources and by a quadratic map of the form
  `J ↦ P_K+ (J ⊗ J)`;
- no owned A1 action currently derives that quadratic map.

This task asks whether that positive route can be derived from existing D0 matter/stress structures,
or whether a new typed bridge/assumption is unavoidable.

## Repository

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Baseline commit for this research:
`5155fe8b7bab2e4ceda4a67e705db1194dc9e0b1`

Do not assume any conversational memory. Treat this brief as self-contained.

## Required CONTROL context

Read first:

- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/RESEARCH_LEDGER.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md
- https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/CLOSURE_CONTRACT.md

The A-RAD packet is research evidence, not yet a formal owner.

## Required repository files

Read these literal owners before proposing any coupling:

1. Matter stress:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Matter/ArchiveStressCoupling.lean

2. Generated matter source:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Matter/GeneratedMatterSource.lean

3. Local trace source:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Matter/LocalTraceSource.lean

4. Matter localization interface:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Interface/MatterLocalization.lean

5. Localization non-uniqueness no-go:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Matter/MatterLocalizationNonuniquenessNoGo.lean

6. Archive Poisson / weak-field source interface:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Geometry/ArchivePoissonEquation.lean
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Geometry/ArchiveWeakField.lean

7. Literal scene cochains:
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean
   https://github.com/gvakhrushev/d0_15/blob/main/03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean

8. Current affected registry rows:
   `D0-MATTER-STRESS-COUPLING-001`
   `D0-MATTER-SOURCE-NEUTRALITY-001`
   `D0-MATTER-LOCALIZATION-001`
   `D0-HODGE-LINKS-001`
   `D0-SPECTRAL-EINSTEIN-001`

Read them from:
https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/claims.csv

## Required attached research inputs

When this task is run by a stateless expensive model, attach if available:

- `MEMO_12_ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`
- `MEMO_10_ASEL_EXHAUSTIVE_DYNAMICS_CLASSIFICATION.md`
- `MEMO_08_ACPL_WEIGHTED_SOURCE_ACTION_COUPLING.md`

The repo packet above is mandatory even if these attachments are unavailable.

---

# Known owned facts that must constrain the research

## A. Existing ArchiveStressCoupling is not a radiative stress source

The current owner literally defines

[
T_{ij}=(R.anomalySum),L^{archive}_{ij}.
]

For anomaly-free matter:

[
R.anomalySum=0 Longrightarrow T=0.
]

Therefore do NOT cite `D0-MATTER-STRESS-COUPLING-001` as already supplying a nonzero local
matter stress capable of sourcing the A-RAD tensor block.

## B. Existing matter localization owns neutrality, not shape

The localization layer controls total source / anomaly neutrality, but the repository also owns a
non-uniqueness theorem showing that zero total source does not select a unique local source profile.

So a nonzero local tensor source cannot be inferred from neutrality alone.

## C. A-RAD boundary

For the literal scene, and more generally ordered `K(a,b,c)`:

- the blockwise-zero-marginal tensor block `Z` is canonical;
- every linear H-equivariant vertex source lies outside `Z`;
- quadratic vertex data can reach `Z`;
- triangle/2-cochain sources can reach `Z`.

The present research gap is therefore **not** “find any map into C1”.
It is:

> derive a physically owned quadratic / stress-type source with the correct carrier, symmetry,
> conservation and coupling semantics.

---

# Research programme

## 1. Inventory every owned matter source

Build a literal table:

```text
owner/module
input type
output type
linear/quadratic/higher in matter variables
neutrality/conservation property
local/nonlocal
scene carrier compatible?
archive carrier compatible?
nonzero for anomaly-free matter?
```

Include at least:

- generated matter source;
- local trace density;
- archive stress matrix;
- localized matter sources;
- any stress representative / variation-dual object;
- any gauge-current or archive-current owner that could feed gravity.

Do not infer a quadratic stress tensor from names.

## 2. Identify the actual matter variables

Determine what D0 presently owns as a matter field/state variable from which a quadratic stress could
be formed.

Candidates may include:

- representation carriers;
- local densities;
- archive operators;
- generation-indexed matter states;
- gauge fields;
- localized source functions.

For each candidate answer:

```text
typed object:
symmetry:
carrier:
normalization:
is there a multiplication/tensor product:
is positivity meaningful:
is locality meaningful:
```

If there is no owned matter amplitude/state corresponding to the A-RAD abstract vertex variable `J`,
say so explicitly.

## 3. Can the A-RAD map J⊗J be typed from owned objects?

A-RAD used the schematic quadratic source

[
(Jotimes J)_{xy}=J_xJ_y
]

on cross-zone edges.

Find the closest owned D0 object `J`.

Then determine whether the map can be written canonically as an existing algebraic operation:

- tensor product;
- outer product;
- matrix element;
- bilinear pairing;
- partial trace;
- covariance;
- stress matrix.

If yes, give the exact typed construction.

If not, identify the minimum new primitive required.

## 4. Conservation / neutrality compatibility

A physically useful source must not merely land in the tensor block.

Check compatibility with every relevant owned constraint:

- anomaly neutrality;
- archive divergence conservation;
- signed edge divergence;
- zero block marginals;
- Ward identity;
- H-equivariance.

Determine whether a naive `J⊗J` automatically satisfies any of them.

If not, classify the necessary projection/counterterm.

## 5. Variational origin

The strongest positive result would be an action-level derivation.

Search for an owned or minimal quadratic/bilinear matter-gravity interaction whose variation with
respect to the edge/gravity variable produces the A-RAD tensor source.

Try forms schematically analogous to

[
S_{int}(h,J)=langle h,;P_Z(Jotimes J)angle,
]

but do not assume this form is owned.

Ask:

- what is the actual typed pairing?
- what transformation properties force the projection?
- is the coefficient fixed?
- is the coupling local?
- does gauge invariance constrain it?

Return the smallest action principle that would generate the source if one exists.

## 6. Relationship to ordinary stress-energy structure

Without importing continuum GR as an axiom, determine whether the A-RAD quadratic route is the finite
analogue of a stress tensor in the precise algebraic sense:

- bilinear/quadratic in matter;
- symmetric in the relevant indices;
- conserved after equations of motion;
- source for a rank-2/tensor-like sector.

Separate genuine structural analogy from interpretation.

## 7. Does existing ArchiveStressCoupling help at all?

Because the current archive stress is anomalySum times a Laplacian, test whether it can be:

- refined before taking anomalySum;
- decomposed into local contributions;
- pulled back to the scene;
- replaced by a partial-trace/local-trace representative already present elsewhere in the repo.

A positive result must reuse literal owned data, not reinterpret a zero source as hidden stress.

If impossible, state a sharp no-go:

> current anomaly-generated stress ownership cannot source the radiative candidate sector.

## 8. Source carrier map

If a nonzero quadratic matter source exists on an archive or vertex carrier, determine the exact typed
map needed to reach:

- SceneC0;
- SceneC1 tensor block;
- SceneC2 triangle source.

Do not hide this as “identify carriers”.

Give source and target types, dimensions, and symmetry.

## 9. Coefficient / normalization count

If a coupling exists, count independent coefficients after quotienting obvious scale conventions.

Does the construction introduce:

- one Newton-like coupling;
- multiple zone couplings;
- no new coefficient;
- an arbitrary bilinear form?

This must be explicit.

## 10. Strong negative control

If the coupling is not forced, construct at least two inequivalent quadratic source maps that satisfy
all currently owned symmetry/conservation constraints.

This proves selector non-uniqueness rather than merely asserting it.

## 11. Impact on gravity closure

At the end, classify the matter→radiative-candidate arrow as one of:

- `CORE-CLOSABLE`
- `ONE-COUPLING-MODULUS`
- `SELECTOR-NOGO`
- `BRIDGE-MISSING`
- `SOURCE-CARRIER-MISSING`
- `NO-NONZERO-ANOMALYFREE-SOURCE`

Choose exactly one primary verdict.

## 12. Required final block

```text
closest owned matter variable to A-RAD J:
owned nonzero anomaly-free local source:
owned quadratic matter object:
can J⊗J be typed canonically:
does current ArchiveStressCoupling contribute:
required conservation projection:
smallest action-level coupling:
source carrier:
target carrier:
number of new coefficients:
whether tensor block is reached:
whether triangle-source route is more natural:
first missing primitive:
impact on D0-HODGE-LINKS-001:
smallest future Lean/certificate artifact:
terminal verdict:
```

## Deliverable

`MEMO_13_ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`

No repository edits.

The memo must distinguish:

- repository-owned theorem;
- accepted prior research;
- new theorem;
- modelling choice;
- external physical analogy.

Do not call any constructed source the physical stress-energy tensor unless the action/conservation
semantics actually justify that name.
