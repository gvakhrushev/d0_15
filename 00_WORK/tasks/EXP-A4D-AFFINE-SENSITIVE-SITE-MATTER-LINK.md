# EXP-A4D-AFFINE-SENSITIVE-SITE-MATTER-LINK

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED on current `main` after merged PR #103, PR #107 and PR #108.

The two parallel workers

- `WRK-A4D-LABELLED-PATH-HOLONOMY-DESCENT`;
- `WRK-A4D-AFFINE-SHIFT-EXTERIOR-BLINDNESS`

may run concurrently. Do not wait for them. Treat their statements as theorem-ready until merged.

Read completely:

- `02_REGISTRY/research/MEMO_A4D_PATH_GROUPOID_CROSSED_MATTER_LIFT.md`;
- `02_REGISTRY/research/MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md`;
- `02_REGISTRY/research/MEMO_A4D_CROSSED_CONSTITUTIVE_REPRESENTATION.md`;
- `03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DLocatedFrameCompatibilityBoundary.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DCrossedDerivationIntegrability.lean`;
- PR #70 path/affine Cartan owners;
- PR #101/#102 crossed first-jet/path-expression owners.

## Frozen boundary

The repository now owns:

1. exact affine path geometry and free path words;
2. exact exterior/frame/observer lift of the **linear** path transport on the existing 16-state Fock carrier;
3. full uncentered first jet `H(e)` as a finite additive path-expression with CAR blocks;
4. scalar crossed first-jet integrability constraints in the compressed endpoint algebra;
5. a free-path descent/holonomy classification showing that generic curl/harmonic data must remain path-resolved unless holonomy trivializes;
6. fixed located `J` and its shifted-anchor boundary.

The earliest missing datum is therefore no longer "some comparison law" in the abstract.

It is one explicit **site-aware affine-sensitive positive matter link**

```text
ell_N^+(A,e,n; x,r)
```

whose products define a free labelled path transport and whose assembled constitutive first derivative reproduces the already-owned full `H(e)`.

The task must either construct such a link in a mathematically honest target, or identify the earliest additional primitive needed to do so.

## Objective

Construct or terminally classify one fixed-N affine-sensitive matter-link package with all of the following typed simultaneously:

```text
ell_N^+(A,e,n; x,r)
Pi_{A,e,n}(x; p)
site / coefficient action
frame-observer covariance
fixed-J dual action
constitutive first-jet assembly
```

The target may be larger than a same-site `16 x 16` matrix, but every enlargement must be explicit and justified.

A vague "take a representation of the affine group" is not a solution.

## Mandatory attack

### A. Start from the literal positive link

Give the exact source and target of

```text
ell_N^+(A,e,n;x,r)
```

including:

- site anchor;
- Fock degree/parity behavior;
- any path-expression/site-idempotent component;
- whether the map acts on one local Fock fiber, a site corner of the global cochain carrier, or an enlarged typed fiber.

Define the negative link only as the shifted inverse if the positive link is invertible.

### B. Recover the landed linear exterior transport

In the zero affine-shift / flat-coframe limit, the link must reduce exactly to the PR #103 exterior lift of the linear Cartan link.

For a general affine path with zero translational part, products of the new letters must agree with `exteriorPathTransport`.

### C. Be genuinely affine-shift sensitive

The construction must distinguish an affine path with value

```text
(I,b),  b != 0
```

from the identity whenever the claimed physical/mathematical interpretation says translation should be visible.

Use exact finite witnesses, preferably at `L=3`.

If the construction cannot make affine translations visible while preserving the other laws, isolate the precise obstruction.

### D. Keep raw coframe and affine connection distinct

Inputs are

```text
(A,e,n)
```

with no silent identification `A=A(e)`.

A solder/Cartan compatibility map may only appear if derived inside this task from an explicit new principle.

Do not smuggle it in as notation.

### E. Reproduce the complete owned first jet

The full

```text
H(e)
```

is an **additive path-expression kernel**, not one multiplicative word value.

Therefore define an explicit assembly rule from the elementary links/site corners to the constitutive/global operator whose flat derivative is tested.

Require:

```text
W_0 = I
D_e W_0[e] = H(e)
```

for arbitrary uncentered raw coframe directions in the scope actually constructed.

This must include:

- scalar edge polarization;
- both half-average terms;
- mixed CAR blocks;
- both corner paths;
- L=2 Nyquist sensitivity;
- L=3 corner coefficient.

Do not define the nonlinear law by simply writing `W(e)=I+H(e)` unless the task is explicitly ending at that independent seed and proves why no stronger link-derived law exists.

### F. Pure-gauge benchmark

For `e=d_f phi`, compare with the exact pure-gauge crossed construction from PR #101.

The new link/path action must either:

- specialize to the same pure-gauge transport up to an explicitly proved gauge/conjugacy equivalence; or
- explain exactly why the targets differ and what extra comparison map is needed.

### G. Respect the compressed-algebra obstruction

PR #108 proves that the owned scalar vertical first-jet law descends to the compressed endpoint crossed algebra only under zero-period and plaquette constraints for `L>=3`, with `L=2` degenerate.

Therefore:

- do not force generic harmonic/curl raw backgrounds into endpoint-compressed relations;
- keep the generic construction on the free labelled path/path-expression parent;
- treat compressed descent only as a derived quotient criterion.

### H. Labelled path composition

Products of the positive/negative links must give exact:

- empty path;
- append;
- reverse/inverse;
- relative labelled holonomy.

At `L=2`, `.fwd r` and `.bwd r` must remain distinct labels until the local period relation is actually proved.

If the labelled-path worker lands during the task, use it. Otherwise reproduce only the research statement and cite it as pending formalization.

### I. Observer/frame covariance

Use the merged PR #103 owners literally.

Required checks:

- exterior/frame covariance;
- moving observer-positive form;
- creator/contraction covariance where the link acts on those blocks;
- rational A/B boost control.

Observer covariance is a transport law, not permission to select an arbitrary constitutive modulus.

Do not identify the rest observer with physical time.

### J. Fixed located-J dualization

Only after the primal link/path law exists, derive the dual action through the fixed located `J`.

Preserve:

- degree/parity;
- complement signs;
- shifted dual anchors;
- distinction between common-fibre contragredience and sitewise located covariance.

A generic degree-mixing action may yield a finite sum of shifted dual blocks; do not force it into one bare dual word.

### K. Test the obvious candidate carriers honestly

At minimum test:

1. current 16-state exterior carrier;
2. the PR #101 nilpotent 16-state affine translation candidate;
3. the homogeneous 32-state `Lambda*(V+R e_*)` affine lift;
4. a site-corner/path-expression enlargement on the existing global archive cochain carrier.

For each candidate record exactly:

- affine translation sensitivity;
- degree preservation;
- parity preservation;
- normalization of the owned degree algebra;
- compatibility with site projectors;
- pure-gauge specialization;
- full first-jet support;
- labelled path invertibility;
- observer/frame covariance;
- fixed-J behavior.

Do not reject a candidate for failing a property that the final target does not actually require; state the type change explicitly instead.

## Hostile controls

Use exact symbolic/rational controls for at least:

- flat background;
- one pure-gauge background;
- L=3 pure affine translation loop;
- L=3 plaquette curl;
- L=3 mixed corner;
- L=5 constant harmonic period;
- L=2 Nyquist and parallel labelled slots;
- all five Fock degrees;
- parity;
- exact rational A/B Lorentz boost;
- one same-endpoint pair with different affine shifts;
- one background where compressed descent holds;
- one where free-path transport is necessary.

## Second-order firewall

Do not try to solve the whole constitutive Hessian before the positive link exists.

If a constructed link canonically induces a second jet, record it and compare with the already-owned nonselection/dressing family.

If not, stop at the first-order/link boundary.

Do not select `S`, `K`, or a scalar coefficient by hand.

## Allowed terminal forms

Examples:

- `AFFINE-SENSITIVE-SITE-MATTER-LINK-CONSTRUCTED-FIRST-JET-OWNED`;
- `AFFINE-SENSITIVE-LINK-CONSTRUCTED-CONSTITUTIVE-ASSEMBLY-MISSING`;
- `SITE-CORNER-PATH-EXPRESSION-TARGET-REQUIRED-16-AND-32-FIBER-LIFTS-INSUFFICIENT`;
- `AFFINE-MATTER-LINK-REQUIRES-SOLDER-CARTAN-COMPATIBILITY-PRIMITIVE`;
- `AFFINE-MATTER-LINK-REQUIRES-NEW-SITE-ACTION-PRIMITIVE`.

Use only the strongest wording actually derived.

## Downstream firewall

Do not promote:

- stress tensor;
- Einstein equations;
- physical time;
- golden/phi matching;
- inter-level refinement;
- a metric reinterpretation of located `J`;
- a universal second jet;
- endpoint-only transport on nontrivial holonomy backgrounds.

## Deliverable

One durable theorem-ready memo in `02_REGISTRY/research/` containing:

- exact carrier/target type;
- positive link and shifted inverse;
- free labelled path law;
- affine translation sensitivity result;
- linear exterior limit;
- pure-gauge comparison;
- full first-jet assembly calculation;
- observer/frame covariance;
- fixed-J dual result;
- compressed-descent boundary;
- hostile controls;
- candidate comparison table;
- terminal verdict;
- theorem-ready handoff;
- exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start EXP-A4D-AFFINE-SENSITIVE-SITE-MATTER-LINK`;
3. immediately open Draft PR before research edits;
4. research and durable memo only inside that PR;
5. before Ready self-retire the task;
6. set `Lifecycle: REVIEW`;
7. Ready for review;
8. do not self-merge.

## Exit condition

One fixed-N site-aware affine-sensitive elementary matter link is either explicitly constructed on a typed free-path/path-expression carrier with exact path laws and complete owned first-jet recovery, or the earliest additional primitive required for such a link is terminally identified without hiding affine translation, curl, harmonic or L=2 labelled information in an endpoint quotient.
