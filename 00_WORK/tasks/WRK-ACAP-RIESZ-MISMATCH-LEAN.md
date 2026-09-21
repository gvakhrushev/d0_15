# WRK-ACAP-RIESZ-MISMATCH-LEAN

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Branch
`work/acap-riesz-mismatch-lean`

## Baseline
Start from the current canonical `main` containing this brief.

## Objective

Formalize the theorem-ready algebraic residue of accepted A-CAP research on the literal
[
K(9,11,13)
]
common carrier.

This task owns **only the algebraic bare-metric mismatch theorem**.

It must not promote the mismatch to a physical memory leak, archive-capacity cost, Bianchi law, TT object, or selector principle.

## Required reading

Read literally:

- `02_REGISTRY/research/ACAP_A1_RIESZ_LEAKAGE_CAPACITY_SELECTOR.md`
- `02_REGISTRY/research/AWEIGHT_A1_CONFORMAL_WEIGHT_SELECTOR.md`
- `03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean`
- `03_FORMALIZATION/D0/Geometry/SceneSourceStratification.lean`
- `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean`
- `03_FORMALIZATION/D0/Gravity/A2CompensatorNoether.lean`
- `03_FORMALIZATION/D0/Spectral/DarkArchiveStructure.lean`
- `03_FORMALIZATION/D0/Topology/TypedSceneEulerReading.lean`
- `03_FORMALIZATION/D0/SelfReading/TypedCapacityRawScene.lean`

Do not reimplement the literal scene or `BPlus` if the current owner already supplies it.

## Target module

Preferred:

`03_FORMALIZATION/D0/Gravity/A1RieszMismatch.lean`

A nearby name is acceptable only if repository naming constraints require it.

## Mathematical target

Let
[
K_+=\ker B_+.
]

Rather than introducing rational inverses too early, it is acceptable to parameterize the bare inverse block metric directly by scalars
[
a=1/x,qquad b=1/y,qquad c=1/z.
]

Define the block-scalar edge map
[
R_{a,b,c}
=
aI_{9,11}\oplus bI_{9,13}\oplus cI_{11,13}
]
and the mismatch
[
L_{a,b,c}
=
B_+R_{a,b,c}\big|_{K_+}.
]

Then prove the exact standard-sector formulas corresponding to
[
143(a-b),qquad
117(a-c),qquad
99(b-c).
]

## Minimum required package

### 1. Reuse literal common carrier

Use:

- `SignlessSignedCommonCarrier.EdgeCochain`;
- `VertexCochain`;
- `BPlus` / `BPlusLin`.

No second signless incidence implementation.

### 2. Block inverse-metric operator

Define a linear map on the literal edge sum carrier that multiplies:

- (9\times11) block by (a);
- (9\times13) block by (b);
- (11\times13) block by (c).

Prove the blockwise application lemmas.

### 3. Balanced vertex standard spaces

Define or reuse the three zero-sum vertex standard carriers:

[
A_9^V,quad A_{11}^V,quad A_{13}^V.
]

Preferred representation: subtype/submodule of functions on each `Fin n` with total sum zero.

Prove their finranks:
[
8,quad10,quad12.
]

Do not identify them definitionally with the separate `Fin 33` dark archive type.

### 4. Standard edge embeddings

Define linear embeddings of balanced vectors into (K_+):

For (f:\mathrm{Fin},9\to\mathbb Q), (sum f=0):
[
h_{9,11}(i,j)=13f_i,qquad
h_{9,13}(i,k)=-11f_i.
]

For (g:\mathrm{Fin},11\to\mathbb Q), (sum g=0):
[
h_{9,11}(i,j)=13g_j,qquad
h_{11,13}(j,k)=-9g_j.
]

For (k:\mathrm{Fin},13\to\mathbb Q), (sum k=0):
[
h_{9,13}(i,ell)=11k_ell,qquad
h_{11,13}(j,ell)=-9k_ell.
]

Prove each embedding lands in (ker B_+).

### 5. Exact mismatch formulas

Prove literally:

[
L_{a,b,c}(A_9)=143(a-b)A_9^V,
]

[
L_{a,b,c}(A_{11})=117(a-c)A_{11}^V,
]

[
L_{a,b,c}(A_{13})=99(b-c)A_{13}^V.
]

Theorems should be entrywise/equality-of-functions, not only numerical spot checks.

### 6. Tensor-sector annihilation

For the existing blockwise-zero-marginal tensor sector, prove that every block-scalar (R_{a,b,c}) still has zero unsigned divergence:
[
B_+R_{a,b,c}z=0
]
for all tensor-block (z).

### 7. Zero mismatch iff uniform

Define the mismatch on the actual unsigned kernel.

Prove:
[
L_{a,b,c}=0	ext{ on }K_+
iff
a=b=c.
]

The converse direction may use explicit nonzero balanced witnesses in the three standard embeddings.

Then provide the positive-weight corollary:
[
B_+W^{-1}|_{K_+}=0
iff
x=y=z
]
for nonzero/positive rational (x,y,z), if the inverse formulation remains clean.

### 8. Exact image/rank theorem — required if technically reachable

Target:
[
\operatorname{rank}L
=
8\mathbf1[a\ne b]
+
10\mathbf1[a\ne c]
+
12\mathbf1[b\ne c].
]

Equivalent exact strata:
[
a=b=c\to0,
]
[
a=b\ne c\to22,
]
[
a=c\ne b\to20,
]
[
b=c\ne a\to18,
]
[
a,b,c	ext{ pairwise distinct}\to30.
]

A clean proof may proceed by:

1. showing every mismatch output is zone-balanced;
2. showing each zone image is contained in its (A_n^V);
3. using the standard embeddings for surjectivity whenever the corresponding scalar difference is nonzero;
4. using disjoint zone support for directness;
5. summing finranks (8,10,12).

If the full conditional-rank theorem creates excessive Lean machinery, the minimum acceptance is:
- all three exact sector formulas;
- tensor annihilation;
- zero mismatch iff (a=b=c);
- three individual image/finrank theorems under the corresponding inequality hypotheses.

Do **not** weaken mathematical content merely to obtain one compact theorem name.

### 9. Optional edge-space defect

If cleanly available from current matrix owners, define
[
P_+=I-B_+^T(B_+B_+^T)^{-1}B_+
]
or an equivalent projector and prove
[
C=(I-P_+)R|_{K_+}
]
has the same zero locus/rank as the vertex mismatch.

This is optional. Do not introduce matrix inversion complexity if it obscures the core theorem.

## Semantic firewall

The module must state explicitly:

- this is **bare-metric non-closure**, not physical reduced-Hessian leakage;
- the accepted compensator-reduced (A_W) preserves (K_+);
- no rank-to-memory theorem is claimed;
- no archive occupancy/saturation theorem is claimed;
- no capacity selector is claimed;
- no generation-count maximality is claimed;
- `BPlus` remains the unsigned Ward operator, not `BMinus`.

## Repository integration

If the module is accepted support rather than a new claim owner:

- add it to `02_REGISTRY/formal_support.csv` as explicit support for `D0-HODGE-LINKS-001`;
- regenerate Lean views with `python tools/generate_lean_views.py`;
- do not hand-edit generated `D0.All` beyond the generator result.

Update:

- `00_WORK/manifest.json`: this task `IN_PROGRESS -> REVIEW`;
- `00_WORK/STATUS.md` accordingly.

Do not promote `D0-HODGE-LINKS-001`.

## Acceptance

Required:

- no `sorry`, `admit`, `axiom`, or `sorryAx`;
- target build succeeds;
- `lake build D0.All` succeeds;
- repository guards pass;
- generated Lean views are fresh;
- working tree clean;
- theorem names/signatures reported;
- `#print axioms` for load-bearing capstone theorem(s) shows only standard Mathlib axioms.

Stop at `REVIEW`.

Do not start any planned worker automatically.
