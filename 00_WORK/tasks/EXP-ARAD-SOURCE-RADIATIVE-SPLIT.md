# EXP-ARAD-SOURCE-RADIATIVE-SPLIT

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective
Determine whether the newly observed source stratification of the K(9,11,13) common carrier is a scene-specific arithmetic coincidence or the specialization of a general ordered-tripartite theorem, and decide whether the 296-dimensional tensor block can honestly be interpreted as a finite radiative carrier.

The central test is stronger than “which sector looks TT-like”:

> If a physical vertex source enters only through the unique A_middle defect sector and all admissible linear H-equivariant dynamics preserve irreducible sectors, can vertex matter excite the tensor/radiative sectors at all?

A terminal answer may therefore be a positive source/radiation bridge or a linear-radiation NO-GO requiring symmetry breaking, nonlinearity, or a different source type.

## Repository and baseline

Repository:
https://github.com/gvakhrushev/d0_15

Canonical branch:
`main`

Mathematical baseline before the recent research:
`e6d9d4b7f17a4cf2f478cb737c90a98487939eaa`

Current CONTROL research ledger:
https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/RESEARCH_LEDGER.md

Do not assume any conversational memory. Treat this brief as self-contained.

PR #44 (`work/c1-common-carrier`) is currently a draft engineering/formalization branch and is NOT a clean canonical proof owner. Do not depend on its build status. Re-derive research identities independently when needed.

## Required repository reading

Read these exact files before doing new mathematics:

1. Literal scene cochains and incidence:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean

2. Literal Euclidean Hodge structure:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean

3. Registered three-level Hodge spectrum:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/03_FORMALIZATION/D0/Synthesis/HodgeThreeLevelSpectrum.lean

4. Owned two-tick algebra:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/03_FORMALIZATION/D0/Dynamics/TwoTickSymplectic.lean

5. Existing finite TT algebra:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/03_FORMALIZATION/D0/Geometry/FiniteSpin2WaveOperator.lean
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/03_FORMALIZATION/D0/Claims/Spin2TT.lean

6. C1 reduced research certificate:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/04_CERTIFICATES/vp_c1_common_carrier_reduced.py

7. A1 compensator research certificate:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/04_CERTIFICATES/vp_a2_compensator_noether.py

8. Existing Hodge-links no-go certificate:
   https://github.com/gvakhrushev/d0_15/blob/e6d9d4b7f17a4cf2f478cb737c90a98487939eaa/04_CERTIFICATES/vp_hodge_links_carrier_nogo.py

9. Current registry targets:
   https://github.com/gvakhrushev/d0_15/blob/main/02_REGISTRY/claims.csv
   Relevant rows: `D0-HODGE-001`, `D0-HODGE-LINKS-001`,
   `D0-C1-COMMON-CARRIER-RESEARCH-001`, `D0-SPECTRAL-EINSTEIN-001`,
   `D0-SPIN2-001`.

## Required external research attachments

When this task is run by a stateless expensive model, attach at minimum:

- `MEMO_08_ACPL_WEIGHTED_SOURCE_ACTION_COUPLING.md`
- `MEMO_10_ASEL_EXHAUSTIVE_DYNAMICS_CLASSIFICATION.md`
- `MEMO_11_AMTT_MODE_LABELLED_SPIN2_READOUT.md`

If available also attach the latest exact-check script used for A-SEL/A-MTT.

These memos are research inputs, not repository-owned theorems. Where they disagree with the repository or with each other, resolve the discrepancy explicitly.

## Frozen research facts to re-check, not blindly assume

On the literal scene `K(9,11,13)` let

- `H = S9 × S11 × S13`;
- `B+` = unsigned endpoint-sum incidence;
- `B-` = signed incidence with transitive orientation `V9 -> V11`, `V9 -> V13`, `V11 -> V13`;
- `K+ = ker B+`, dim 326;
- `K- = ker B-`, dim 327.

The accepted research decomposition is

[
K_+ cong
(A_9oxtimes A_{11})_{80}oplus
(A_9oxtimes A_{13})_{96}oplus
(A_{11}oxtimes A_{13})_{120}oplus
(A_9)_8oplus(A_{11})_{10}oplus(A_{13})_{12}.
]

The first three “tensor sectors” have total dimension 296. The last three “singlet/standard sectors” have total dimension 30.

Recent rev.5 exact calculations, NOT YET IN THE MEMOS, report:

1. Each tensor sector is supported in one edge block and has zero row and column partial sums.

2. As an H-representation the 30-dimensional singlet block is
   [
   A_9oplus A_{11}oplus A_{13}cong C^0/mathbb R^3_{m zone}.
   ]

3. Hence
   [
   dimoperatorname{Hom}_H(C^0,K_+)=3.
   ]

4. Define the projected signed vertex-source channel
   [
   R_V:=P_{K_+}B_-^T:C^0	o K_+.
   ]
   On the literal scene the reported result is
   [
   operatorname{im}R_V=A_{11},
   ]
   and
   [
   R_V^*R_V=B_-P_{K_+}B_-^T=rac{234}{11}C_{11}.
   ]
   Thus a signed point source `B-^T e_i` meets `K+` only for `i in V11`, and only through the 10-dimensional `A11` sector.

5. Dually, on `U(K+)`, the projected unsigned source `B+^T` again reaches only the corresponding `A11` defect sector.

6. The C1 mismatch itself is only `A11`:
   [
   K_+cap K_-
   =
   (A_9oxtimes A_{11})oplus
   (A_9oxtimes A_{13})oplus
   (A_{11}oxtimes A_{13})oplus
   A_9oplus A_{13},
   ]
   dimension `296+8+12=316`.

7. The repeated arithmetic is
   [
   234=2cdot9cdot13,qquad
   rac{234}{11}=rac{2cdot9cdot13}{11},
   ]
   and
   [
   B_+omega=234,1_{V_{11}},
   qquad
   omega=(13,-11,9).
   ]

8. The triangle-source channel `D^T:C^2->C^1`, after projection to `K+`, reaches the tensor sectors; rev.5 suggests it may reach all of `K+`.

9. A-SEL found the intrinsic degree-1 kinetically local operator class
   [
   operatorname{span}{I,Q_H,arepsilon_{A_{11}}},
   ]
   where the unique non-Hodge direction `arepsilon_{A11}` acts only on this same 10-dimensional defect/source sector.

10. Every H-equivariant linear spatial operator is block-diagonal on the six irreducible sectors. Therefore linear H-equivariant evolution cannot mix `A11` into the 296-dimensional tensor block.

These are starting targets for proof/generalisation, not permissions to overclaim “A11 is TT”.

---

# Research programme

## 1. Generalise from K(9,11,13) to ordered K(a,b,c)

Take three positive zone sizes `a,b,c` and the transitive orientation

[
A	o B,qquad A	o C,qquad B	o C.
]

Assume whatever inequalities are actually needed, and state them explicitly. In particular test the degree-ordered case `a<b<c`.

Derive exact symbolic formulas for:

- `rank B+`, `rank B-`;
- `dim ker B+`, `dim ker B-`;
- the full H=`S_a×S_b×S_c` decomposition of both kernels;
- `ker B+cap ker B-`;
- the unique mismatched irreducible sector;
- the common-carrier isometry U;
- the extra signed line `omega`.

Do NOT specialize to 9/11/13 until after the theorem is established.

## 2. Test the “middle-zone theorem”

The expected pattern is

[
omega=(c,-b,a)
]

on the three edge blocks and

[
B_+omega=(0,2ac,0).
]

Prove or refute this for general `K(a,b,c)`.

Likewise test the expected compressed vertex-source identity

[
B_-P_+B_-^T
=
rac{2ac}{b},C_b
]

on the middle zone and zero on the outer zones.

If true, prove:

[
operatorname{im}(P_+B_-^T)=A_b.
]

This is the key theorem.

Then repeat for all six transitive orientations. Determine whether the defect/source sector is always the zone that is **middle in the orientation order**.

## 3. Decide whether V11 is intrinsically special

For the actual scene, orientation is chosen by degree/size order

[
9<11<13.
]

Determine exactly which of the following is true:

A. `V11` is selected independently by scene arithmetic, even without choosing an orientation;

B. `V11` is selected because it is the unique middle zone in the canonical degree-ordered transitive orientation;

C. several orientation conventions are equally natural, so “V11 is special” is not canonical.

This distinction is load-bearing. Do not use repeated appearances of `234` as evidence of independent selection if they are all consequences of one orientation theorem.

## 4. Vertex-source channel as a partial isometry

For general ordered `K(a,b,c)`, define

[
R_V=P_+B_-^T.
]

Determine its singular values and prove the exact relationship between the vertex `A_b` standard representation and the edge `A_b` defect sector.

Is

[
R_V|_{A_b}
]

a scalar multiple of an isometry?

Find the scalar exactly.

Give both

[
R_V^*R_V
]

and

[
R_VR_V^*
]

as explicit projectors.

## 5. Tensor carrier as the zero-marginal sector

Define the 296-dimensional scene tensor block intrinsically, without mentioning representation names first.

Candidate:

> edge fields whose row and column partial sums vanish separately in every bipartite block.

Prove its dimension for general `a,b,c`:

[
(a-1)(b-1)+(a-1)(c-1)+(b-1)(c-1).
]

Then prove it equals

[
A_aoxtimes A_b
oplus
A_aoxtimes A_c
oplus
A_boxtimes A_c.
]

Determine whether it is canonical before an orientation is chosen.

## 6. Complete source stratification

Do not use the word “source” generically.

Classify at least:

### vertex source
[
B_-^T:C^0	o C^1
]

### unsigned/Weyl vertex source
[
B_+^T:C^0	o C^1
]

### triangle/2-cochain source
[
D^T:C^2	o C^1.
]

After projection onto `K+` and onto `U(K+)`, determine the exact image of each channel in the six irreducible sectors.

In particular prove or refute:

[
operatorname{im}(P_{K_+}D^T)=K_+.
]

If it is full only under `a<c` or other conditions, state the exact criterion.

Produce a table

```text
source type | tensor 296 | A_a | A_b | A_c | omega
```

with exact yes/no/rank statements.

## 7. The real “radiative carrier” test

The tensor 296 block is attractive because it is zero-marginal and vertex-invisible. That is NOT sufficient to call it TT or radiative.

Test four properties:

1. invariant under `Q_H`;
2. invariant under the full kinetically-local class `span{I,Q_H,eps_A_middle}`;
3. invariant under the stable two-tick temporal evolution;
4. orthogonal to all vertex-source excitations.

If all hold, call it a **vertex-source-decoupled dynamical sector**, not yet TT.

Then determine what further property would be needed to justify the word “radiative”.

## 8. Linear radiation from vertex matter: possible or impossible?

This is the highest-value question.

Suppose initial/source forcing enters only through the vertex channel and the evolution operator is linear and H-equivariant.

If the source image is only `A_b` and the dynamics preserves irreducible sectors, prove or refute:

[
	ext{vertex source cannot excite any tensor sector}.
]

If true, state a clean theorem:

> No linear H-equivariant finite dynamics on the frozen tripartite scene can convert a pure vertex source into the tensor/radiative candidate sector.

Then classify the minimal escape routes:

- triangle/2-cochain source;
- explicit H-symmetry breaking;
- nonlinear mode mixing;
- time-dependent/non-H-equivariant background;
- additional carrier/source map.

This may be a much more important NO-GO than the old “no 2D TT target” result.

## 9. Relation to A-MTT

Restrict the A-MTT readout problem separately to:

- tensor block `296`;
- outer singlets `A_a ⊕ A_c`;
- middle source sector `A_b`.

Determine whether symmetry reduction to an `S_3` subgroup behaves differently on these pieces.

Do NOT conclude that `A_b` is TT merely because it admits a 2D piece after symmetry reduction.

The desired question is whether the **tensor block** has a natural mode/fibre interpretation after the minimal symmetry reduction.

## 10. Meaning of the outer singlets

The vertex-invisible complement of `A_b` is 316-dimensional, not 296-dimensional:

[
296oplus A_aoplus A_c.
]

So explain what distinguishes `A_aoplus A_c` from the tensor block.

Are they:

- longitudinal boundary modes;
- source-free singlets;
- additional propagating sectors;
- removable by a stronger marginal condition;
- artifacts of the finite tripartite geometry?

Give an intrinsic characterization.

## 11. Relation to epsilon_A_middle

A-SEL found

[
mathcal K_1=operatorname{span}{I,Q_H,arepsilon_{A_b}}.
]

If the same `A_b` is exactly the vertex-source image, prove the equivalence:

> the unique non-Hodge degree-1 kinetically-local operator direction is supported exactly on the unique projected vertex-source / C1-defect sector.

This would turn three formerly separate observations into one theorem.

## 12. Relative normalization and A1

Do not assume `m^2=4`.

Use the strongest honest conditional statement:

[
Q=cQ_H+sI+d,arepsilon_{A_b}
]

before Hodge restriction, and

[
Q=c(Q_H+m^2I)
]

after Hodge restriction.

Determine whether the source stratification yields any NEW equation fixing `d`, `m^2`, or the temporal `alpha`.

If not, say so.

## 13. Orientation robustness controls

Run all key formulas under:

- reversed total order;
- all six transitive orders;
- at least one cyclic orientation.

Determine exactly which parts are:

- orientation invariant;
- conjugate under relabelling/sign changes;
- genuinely dependent on the chosen order.

Especially test whether “middle-source sector” survives only for transitive orientations.

## 14. Exact symbolic result first, computation second

Use exact rational/integer computation as a verifier.

But the deliverable must contain symbolic proofs for the general family where claimed.

A finite 9/11/13 check is not a proof of the `K(a,b,c)` theorem.

## 15. Terminal classification

Return exactly one primary verdict:

- `CANONICAL-RADIATIVE-SPLIT`
- `LINEAR-VERTEX-RADIATION-NOGO`
- `ORIENTATION-DEPENDENT-SPLIT`
- `SOURCE-TYPE-DEPENDENT-SPLIT`
- `NO-CANONICAL-RADIATIVE-CARRIER`

Multiple secondary boundaries may be listed, but choose one primary verdict.

## 16. Required final block

```text
general K(a,b,c) defect sector:
general omega:
general B+ omega:
general projected vertex-source Gram operator:
is the defect always the middle orientation zone:
what is intrinsically special about V11:
vertex-source image on K+:
triangle-source image on K+:
dimension of zero-marginal tensor carrier:
dimension of vertex-invisible carrier:
does Q_H preserve the tensor carrier:
does the full kinetic-local class preserve it:
can linear H-equivariant vertex matter excite tensor modes:
minimal escape route if not:
meaning of A9 and A13 singlets:
relation to eps_A11:
does this fix m^2:
does this fix alpha:
strongest honest “radiative” statement:
smallest future Lean theorem package:
terminal verdict:
```

## Deliverable

`MEMO_12_ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`

No repository edits.

The memo must clearly separate:

- repository-owned facts;
- accepted prior research;
- new theorem/proof;
- finite exact checks;
- physical interpretation.

Do not call any sector “TT”, “graviton”, or “physical radiation” unless the required tensor/readout structure has actually been constructed.
