# A-RAD — Source-Stratified Radiative Carrier

CONTROL disposition: **ACCEPT AS RESEARCH**  
Primary verdict: **LINEAR-VERTEX-RADIATION-NOGO**  
Audited baseline: `e6d9d4b7f17a4cf2f478cb737c90a98487939eaa`

This packet is a durable research summary, not a claim owner. The detailed source memo was
`MEMO_12_ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`; companion exact checks reported 437 + 36 PASS.

## Repository-owned inputs

- `GenericTripartiteHomology.boundary1` fixes the literal transitive orientation `9→11→13`.
- `SceneCochainComplex` owns the literal 33/359/1287 cochain complex, ranks, and exactness.
- `SceneHodgeDecomposition` owns the Euclidean cochain pairing used by the finite projection arguments.
- Existing Fin4 TT code owns a 2-polarization algebra on `Role4`, but no scene-edge → TT map.

Everything below remains research until separately formalized/registered.

## General ordered-tripartite theorem

For `K(a,b,c)`, with a transitive orientation whose middle zone has size `m` and whose two outer
zones have sizes `p,q`:

1. The zero-block-marginal tensor sector is
   [
   Z=(A_a\boxtimes A_b)\oplus(A_a\boxtimes A_c)\oplus(A_b\boxtimes A_c),
   ]
   with dimension
   [
   (a-1)(b-1)+(a-1)(c-1)+(b-1)(c-1).
   ]
   It is orientation-independent and lies in both signed and unsigned kernels.

2. For a transitive orientation, the signed/unsigned kernel mismatch occurs in exactly the standard
   representation of the **middle orientation zone**. For a cyclic orientation, all three singlet
   sectors are defects.

3. For the repository orientation `A→B→C`, the H-fixed signed-kernel line has block coefficients
   [
   \omega=(c,-b,a),
   ]
   and
   [
   B_+\omega=(0,2ac,0).
   ]
   Thus the literal `234=2·9·13` is the outer-zone product written on the middle zone; it is not an
   independent selection of 11.

4. The projected signed vertex-source channel
   [
   R_V=P_{K_+}B_-^T
   ]
   has image exactly the middle standard sector and Gram
   [
   B_-P_{K_+}B_-^T=\frac{4pq}{p+q}C_{mid}.
   ]
   The previously conjectured `2pq/m` holds only when `2m=p+q`; `9,11,13` satisfies this arithmetic
   progression identity accidentally.

5. On the literal scene:
   [
   \frac{4·9·13}{9+13}=\frac{234}{11}.
   ]
   The C1 overlap, Hodge up/down split and source Gram are one single-angle geometry:
   [
   \cos\theta=\frac{13-9}{13+9}=\frac2{11},\quad
   down=\frac{234}{11},\quad up=\frac8{11},\quad down+up=22.
   ]

6. The extra signed line is a uniform triangle source:
   [
   D^T\mathbf1_T=13\,\omega
   ]
   on `K(9,11,13)` (general formula up to the chosen normalization/orientation).
   Therefore `omega` is vertex-invisible but triangle-sourced; the old phrase “matter-only omega”
   must not be used.

## Carrier-free source no-go

The strongest robust result does not need C1:

[
\operatorname{im}B_-^T\perp Z
]

already in all of `C^1`. Equivalently,

[
\operatorname{Hom}_H(C^0,Z)=0.
]

Therefore a **linear H-equivariant vertex source cannot excite the tensor sector**, regardless of
whether one later works on `K_+`, `K_-`, or the C1 common carrier.

For a linear H-equivariant evolution, a vertex-sourced excitation remains in the middle standard
sector; no sector mixing into `Z` occurs.

This is stronger and cleaner than trying to identify the tensor block with TT.

## Positive escape routes

The no-go is source-type specific, not an absolute radiation no-go.

- Triangle source `D^T J_T` reaches the tensor sector always and reaches all of `K_+` iff the two
  outer zone sizes differ. The literal scene has `9≠13`, so its projected triangle channel is full.
- A quadratic vertex coupling
  [
  J\mapsto P_{K_+}(J\otimes J)
  ]
  reaches tensor sectors; in particular the `A_a⊕A_b` input spans `A_a\boxtimes A_b`.
- Linear alternatives require symmetry breaking/non-H-equivariant background/new source data.

No owned A1 action currently derives the quadratic `J⊗J` coupling.

## Interpretation boundary

The 296-dimensional literal tensor block is the unique canonical blockwise-zero-marginal sector and
is a **radiative candidate**, not an owned TT/spin-2/graviton carrier.

Why it is a better candidate than the singlets:

- it is vertex-source invisible;
- triangle/quadratic sources reach it;
- it is preserved by H-equivariant sector-diagonal dynamics;
- after the A-MTT symmetry reduction it is the piece that carries mode-labelled rank-2 fibres.

Still missing: metric/covector/frame/readout identifying those fibres with physical TT polarizations.

## Roadmap consequences

- `V11` is not intrinsically selected by a new arithmetic principle; it is the middle zone of the
  repository-owned transitive orientation.
- The `A11` C1 defect, projected vertex-source image, compressed down-Laplacian support, and
  `eps_A11` kinetic direction are the same structural object.
- Source stratification fixes neither the mass-like shift `m²` nor temporal `alpha`.
- The next formal target should be the carrier-free source/tensor orthogonality and the uniform
  triangle-source identity, not a global TT construction.
