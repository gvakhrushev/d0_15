# MEMO A4D — resolved affine research/formalization program

**Control:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
**Execution:** PR #190  
**Status:** PROGRAM / no new scientific theorem  
**Baseline:** `297067714e7c1a246b06ed981578105c58d9f3db`

## 0. Purpose

This memo turns the current A4D affine frontier into a durable sequence of
research and Lean formalization tasks.  It is a control-plane artifact, not a
claim promotion.

The program separates three kinds of input:

- **MERGED / repository-owned:** results already on `main`;
- **READY / unmerged:** exact research results in Ready PRs, not yet repository truth;
- **ACTIVE / provisional:** Draft/In-Progress results that may still change.

Lean workers may formalize only MERGED results unless their task has an explicit
dependency gate that has been satisfied.

## 1. Merged scientific base

The following are already safe inputs for formalization:

1. the selected star-density channel has survived finite variation and flat
   quotient pressure tests;
2. nonlinear site-dependent proper-Lorentz invariance survives cell-by-cell;
3. on the nondegenerate solder sector the Lorentz action is free and the
   quotient is nontrivial;
4. the observer-completed affine translation is not an off-shell symmetry of
   the selected star action on the exact curved witness;
5. the first bounded-locality Cartan-Hodge translation/on-shell rescue class is
   obstructed by the exact rank condition
   `rank(A)=6 < rank([A|-c])=7`.

These are the immediate Lean targets.

## 2. Ready but unmerged affine-completion frontier

Current Ready research PRs report, pending merge/review:

- #184: the unique relative-solder coefficient is `lambda=1`;
  `ThetaHat = Theta - b^T h_n` is affine-covariant but overquotients the
  edge diagonal by 192 nongauge directions on the curved L=2 control.
- #185: continuous single-loop translational scalars are generically blind;
  the first surviving polynomial translation carrier requires two based loops,
  with
  [
  R_{2|1}=det(I-P_1)t_2-(I-P_2)operatorname{adj}(I-P_1)t_1.
  ]
- #188: the flat/curved gauge-image seam requires an incidence memory
  [
  mathcal I_*supseteqoperatorname{im}D_L,
  qquad
  G_*=mathcal I_*/operatorname{im}D_L.
  ]
- #189: the resolved quotient energy variation is classified under several
  endpoint contracts and the constrained-Grassmannian contract gives an
  independent Euler channel for the two-channel action family.

These results must not be treated as merged theorem inputs until their PRs land.

## 3. Active research frontier

Draft PRs #182, #186 and #187 remain active.

The next unresolved architecture is:

[
Llongmapsto operatorname{im}D_L
]

changes rank at the flat seam.  The program therefore tests whether the correct
resolved carrier is the closure of the generic image graph inside an
appropriate Grassmannian/incidence space, rather than arbitrary external
memory.

The research chain is:

1. `EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION`;
2. `EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT`;
3. `EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`.

No later stage may be started by pretending the earlier stage is already
selected.

## 4. Formalization chain

Lean formalization is split by mathematical stability, not by chronology.

### Immediate workers — merged science only

1. `WRK-A4D-FORMALIZE-NONLINEAR-LORENTZ-QUOTIENT`.
2. `WRK-A4D-FORMALIZE-CARTAN-HODGE-TRANSLATION-NOGO`.

### Dependency-gated workers

3. `WRK-A4D-FORMALIZE-AFFINE-RELATIVE-SOLDER` — after #184 lands.
4. `WRK-A4D-FORMALIZE-JOINT-HOLONOMY-RESIDUAL` — after #185 and the relevant
   completeness result from #186 land.
5. `WRK-A4D-FORMALIZE-GAUGE-IMAGE-SEAM-RESOLUTION` — after #188 plus the
   graph-closure research task stabilize the resolved carrier.
6. `WRK-A4D-FORMALIZE-RESOLVED-ENERGY-VARIATION` — after #189 and the carrier
   contract are stable.
7. `WRK-A4D-FORMALIZE-CHECKERBOARD-NONLINEAR-OBSTRUCTION` — after #187 reaches
   a stable terminal and its current second-order obstruction survives review.

## 5. Formalization policy

For each worker:

- reuse existing finite carrier, Role/Lorentz, observer and affine-Cartan modules;
- prefer theorem-level algebra over hard-coded numerical enumeration;
- finite L=2 exact certificates may be reflected as theorem witnesses only when
  the finite data are explicitly typed in Lean;
- do not turn Python rank output into an axiom;
- if a large rank theorem is not yet practical in Lean, formalize the structural
  statement and an exact small witness first, and record the remaining rank
  computation as an explicit formalization blocker;
- update `D0.All` only when the new module is stable;
- no claim/release/BOOK promotion unless a separate CONTROL task authorizes it.

## 6. Collision plan

The immediate workers must write disjoint new modules.

Suggested module ownership:

- Lorentz quotient:
  `D0.Geometry.A4DStarFiniteLorentzQuotient`;
- Cartan-Hodge no-go:
  `D0.Geometry.A4DStarTranslationCartanHodgeNoGo`;
- relative solder:
  `D0.Geometry.A4DAffineRelativeSolderCompletion`;
- joint holonomy:
  `D0.Geometry.A4DJointHolonomyResidual`;
- gauge-image seam:
  `D0.Geometry.A4DGaugeImageResolution`;
- resolved energy:
  `D0.Geometry.A4DResolvedAffineEnergy`;
- checkerboard obstruction:
  `D0.Geometry.A4DCheckerboardNonlinearObstruction`.

Existing modules are imported and strengthened only when ownership is clear.
Avoid simultaneous edits to the same theorem-ledger/generated files.

## 7. Program terminal

The program is successful when the moving research frontier and Lean lag are
kept within one stable layer: every merged structural result receives a
formalization task, while no unmerged conjectural architecture is frozen into
Lean as if selected.
