# A-STRESS — Quadratic Matter-to-Tensor Source

CONTROL disposition: **ACCEPT AS RESEARCH**  
Primary verdict: **SOURCE-CARRIER-MISSING**  
Secondary verdict: **SELECTOR-NOGO**  
Audited baseline: `5155fe8b7bab2e4ceda4a67e705db1194dc9e0b1`

This packet is a durable research summary, not a proof owner. The source memo was
`MEMO_13_ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`.

## Repository-owned facts

- `D0.Matter.ArchiveStressCoupling` defines
  [
  T=(R.anomalySum),L_{archive}.
  ]
  For anomaly-free matter this source is exactly zero.
- `D0.Matter.GeneratedMatterSource` owns neutrality but no nonzero scene source.
- `D0.Matter.MatterLocalizationNonuniquenessNoGo` owns a no-go: total neutrality does not select a unique local profile.
- The scene cochain complex owns `SceneC0/C1/C2`, signed incidence, exactness and Euclidean pairings, but no matter-valued scene carrier.
- Existing scene and matter lanes are not connected by a typed theorem-level map from owned matter data into `SceneC0/C1/C2`.

## Accepted research result

The A-RAD quadratic route can be sharpened as follows.

Let `Z` be the blockwise-zero-marginal tensor sector of `SceneC1`.

For a scene vertex variable `J`, the quadratic block product followed by blockwise marginal projection gives an H-equivariant map

[
Q(J)=P_Z(Jotimes J)in Z.
]

On the literal `K(9,11,13)` scene its bilinear span is all of `Z`:

[
operatorname{span}{P_Z(Jotimes J')}=Z,
qquad
dim Z=296.
]

The same rank statement was checked on non-arithmetic control scenes.

## Exact selector count

For `H=S_a	imes S_b	imes S_c` and
[
Z=A_aoxtimes A_boplus A_aoxtimes A_coplus A_boxtimes A_c,
]
exact character theory gives

[
dimoperatorname{Hom}_H(C^0otimes C^0,Z)=6,
]
[
dimoperatorname{Hom}_H(operatorname{Sym}^2C^0,Z)=3,
]
[
dimoperatorname{Hom}_H(wedge^2C^0,Z)=3.
]

Therefore the general H-equivariant **quadratic** map `C0 -> Z` is exactly a three-parameter block family

[
(c_{AB},c_{AC},c_{BC}).
]

After quotienting a common scale, two essential selector parameters remain.

This is not an ansatz: the three block directions exhaust the equivariant quadratic class.

## Primary obstruction: source carrier

The repository does not own the matter variable required to instantiate this map.

There is no owned arrow

[
	ext{D0 matter data}longrightarrow SceneC0
]

and no owned scene-valued matter amplitude that can be squared.

The closest owned objects are:

- anomaly/charge aggregates in `MatterRep`;
- local trace densities on archive indices;
- non-canonical neutral localization profiles;
- generic archive matrices.

None is typed into the scene cochain complex.

Therefore the matter-to-tensor arrow is presently classified:

[
oxed{	ext{SOURCE-CARRIER-MISSING}}.
]

## Existing archive stress does not close the arrow

The currently registered matter stress coupling cannot be reinterpreted as the missing quadratic source:

1. it vanishes for anomaly-free matter;
2. it is linear in `anomalySum`, not quadratic in a matter amplitude;
3. it lives on the archive matrix carrier;
4. no owned map sends it into the scene tensor sector.

Its `CORE-FORMALIZED` status remains correct for its actual statement.

## Conservation and target side

Once a scene variable `J` is supplied, the blockwise-zero-marginal projection automatically gives:

- zero block marginals;
- signed divergence zero;
- unsigned endpoint-sum zero at the research level;
- total zero sum.

Thus the target/conservation side is not the main missing primitive.

The scene triangle channel also reaches `Z`; this is cheaper on the carrier side but does not solve the matter typing problem.

## Minimal positive completion

The smallest action-like modelling completion would be

[
S_{int}[h,J]
=
kappalangle h,Q(J)angle_1,
]

with a new scene matter amplitude `J` and a scene edge/gravity variable `h`.

This is a modelling construction, not owned D0 physics.

It introduces:

- a missing typed matter carrier;
- a missing scene gravity variable if interpreted variationally;
- three block coefficients, two essential after overall scale;
- an overall interaction normalization at action level.

## Roadmap consequence

The old phrase “missing nonlinear/quadratic matter-to-tensor coupling” was too coarse.

Research now separates it into:

1. **source carrier missing** — no owned matter→scene amplitude;
2. **quadratic selector no-go** — even after supplying the carrier, H-equivariance alone leaves exactly two essential block-ratio choices;
3. **target geometry available** — the tensor block and triangle route are mathematically explicit.

No status flip to TT, graviton, Einstein, or physical radiation is justified.

## Formalization caution discovered during audit

For the literal repository boundary convention,

[
sceneBoundary2cdot mathbf1_{SceneTriangle}
=
omega_{scene},
qquad
omega_{scene}=(13,-11,9).
]

Equivalently, if one defines the normalized research vector

[
omega=(1,-11/13,9/13),
]

then

[
sceneBoundary2cdotmathbf1=13,omega.
]

Do not combine the unnormalized ((13,-11,9)) definition with an extra factor 13.
