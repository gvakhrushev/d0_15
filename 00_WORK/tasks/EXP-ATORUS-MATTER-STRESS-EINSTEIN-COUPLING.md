# EXP-ATORUS-MATTER-STRESS-EINSTEIN-COUPLING

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Move from the geometric Einstein estimator to the sourced equation.

Audit whether D0 owns any nonzero matter/archive object that can be transported onto the **same fixed-T4 symmetric-tensor carrier** as the gravity response and converge to a conserved continuum stress tensor
[
T_{ab}.
]

If not, terminally identify the first exact matter bridge and do not hide A-STRESS/A-SOURCE no-gos.

Repository edits: **NONE**.

## Frozen gravity side

Read:

- `02_REGISTRY/research/ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`
- `02_REGISTRY/research/ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md`

The gravity-side research target is now explicit:
[
R_x^{F,resp}E_{\eta,N}
\to
-2G[g](x).
]

The matter task must land on that same geometric target type:
[
S^2T_x^*T^4.
]

## Required matter inputs

Read fully:

- `02_REGISTRY/research/ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`
- `02_REGISTRY/research/ASOURCE_ACTION_NATURALITY_SELECTOR.md`
- `03_FORMALIZATION/D0/Matter/ArchiveStressCoupling.lean`
- `03_FORMALIZATION/D0/Matter/GeneratedMatterSource.lean`
- `03_FORMALIZATION/D0/Frozen/ConservedStressProjection.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveStressRepresentative.lean`
- `03_FORMALIZATION/D0/Geometry/ArchiveBianchiIdentity.lean`
- localization/nonuniqueness owners relevant to nonzero matter sources.

## Main audit

For every plausible owned matter/source object, classify:

1. carrier;
2. whether it is nonzero for anomaly-free physical matter;
3. symmetry;
4. conservation notion;
5. locality;
6. refinement index / tower availability;
7. map into finite `SymRoleTensor` or local gravity response carrier;
8. pointwise reconstruction into (S^2T_x^*T^4);
9. possible continuum conservation;
10. coefficient/selector freedom.

## Mandatory frozen no-gos

Do not erase:

### A-STRESS
The scene quadratic matter source has
[
\dim\operatorname{Hom}_H(\operatorname{Sym}^2C^0,Z)=3,
]
so after overall scale two projective selector ratios remain.

Its primary blocker is `SOURCE-CARRIER-MISSING`:
no owned matter variable maps into the required scene amplitude.

### A-SOURCE
Owned action/naturality/Hodge conditions do not select those three block coefficients.

A universal endpoint-only action would conditionally pick ((1:1:1)), but that action is not owned.

### Existing ArchiveStressCoupling
The minimal anomaly-based archive matter source vanishes for anomaly-free matter and therefore cannot silently become the desired nonzero physical (T_{ab}).

## Central question

Can any other owned object bypass these no-gos and supply a nonzero same-carrier tensor source?

Candidates include:

- localized matter source owners;
- conserved archive stress representatives/projections;
- trace-density objects;
- quadratic finite matter operators;
- generation/charge amplitudes;
- any newly landed matter carrier.

If the answer is no, state the smallest new primitive required.

## Sourced equation target

The positive endpoint would be a finite equation on one common carrier:
[
E_N[m_N]
=
\kappa_N T_N[\psi_N],
]
with both sides reconstructing to the same (S^2T_x^*T^4) fibre and
[
-2G[g](x)
=
\kappa T[g,\psi](x)
]
in the continuum limit.

Do not assume the normalization (\kappa), Newton's constant, or (8\pi).

## Conservation firewall

Archive row-sum conservation, scene signed divergence and finite centered Role divergence are different operators.

A continuum matter tensor must eventually satisfy
[
\nabla^aT_{ab}=0.
]

State the exact intertwining theorem required.

## Cosmological/vacuum source

Audit separately whether any owned finite source could produce a metric-proportional vacuum term
[
\Lambda g_{ab}.
]

Do not interpret absence from the pure second-difference gravity estimator as a derivation of (\Lambda=0).

## Terminal verdict

Return exactly one:

- `SAME-CARRIER-MATTER-STRESS-BRIDGE-REACHED`
- `MATTER-SOURCE-CARRIER-MISSING-TERMINAL`
- `MATTER-STRESS-SELECTOR-NOGO-TERMINAL`
- `MATTER-STRESS-RECONSTRUCTION-BRIDGE-OPEN`
- `MATTER-CONSERVATION-INTERTWINING-BRIDGE-OPEN`
- `ONLY-ZERO-ANOMALY-FREE-SOURCE-OWNED`

## Deliverable

`MEMO_32_ATORUS_MATTER_STRESS_EINSTEIN_COUPLING.md`
