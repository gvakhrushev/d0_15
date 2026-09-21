# WRK-SOURCE-STRATIFICATION-NOGO

## Class
WORKER

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective
Formalize the smallest theorem-ready part of accepted A-RAD research without depending on the unstable C1 branch.

The worker must own the literal-scene source/tensor separation directly from the already-stable cochain complex:

1. a zero-block-marginal tensor subspace on SceneC1;
2. its inclusion in the signed Hodge kernel;
3. orthogonality of every signed vertex gradient/source to that tensor subspace;
4. the uniform triangle-source identity producing the H-fixed omega pattern.

This is deliberately narrower than the full A-RAD memo. Do not formalize TT, the six-sector commutant, nonlinear source maps, or the general K(a,b,c) classification in this worker.

## Repository
https://github.com/gvakhrushev/d0_15

## Required research packet
Read first:
- `02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`
- `02_REGISTRY/RESEARCH_LEDGER.md`

## Stable owners to reuse
- `D0.Topology.GenericTripartiteHomology`
- `D0.Geometry.SceneCochainComplex`
- `D0.Geometry.SceneHodgeDecomposition`

Do NOT import the draft `SignlessSignedCommonCarrier` module from PR #44.

## Target module
Preferred:
`03_FORMALIZATION/D0/Geometry/SceneSourceStratification.lean`

Use stable imports only.

## Required objects and theorems

### A. Literal block-marginal tensor subspace
Define the literal SceneC1 submodule whose row and column sums vanish separately in each of the three edge blocks.

A good API may use six families of linear marginal maps. The exact internal representation is up to the worker, but the public statement must make the blockwise-zero-marginal meaning explicit.

Name suggestion:
`SceneTensorBlock`.

### B. Tensor block lies in the signed kernel
Prove:
[
SceneTensorBlock \le \ker(sceneBoundary1.mulVecLin).
]

This follows because signed vertex divergence is a signed row/column marginal.

If the unsigned operator is available without importing the draft C1 module, you may also prove the unsigned-kernel inclusion. It is optional in this worker.

### C. Carrier-free vertex-source orthogonality
For every vertex cochain `f : SceneC0` and every `z : SceneTensorBlock`, prove the Euclidean pairing
[
\langle sceneBoundary1^T f, z\rangle = 0.
]

Prefer deriving this from the already-owned adjointness identity when possible:
[
\langle d_0 f,z\rangle_1=\langle f,\delta_1 z\rangle_0
]
and the result from B.

This theorem is the load-bearing formal core of the linear vertex-radiation no-go.

Do NOT call it a graviton/TT theorem. Suggested semantic name:
`vertex_source_orthogonal_to_tensorBlock`.

### D. Literal uniform triangle source
Define the literal block-constant edge vector
[
\omega_{scene}=(13,-11,9)
]
on the three edge blocks.

Prove:
[
sceneBoundary1.mulVec\,\omega_{scene}=0.
]

Then prove the stronger source identity
[
sceneBoundary2.mulVec(\mathbf1_{SceneTriangle})=13\,\omega_{scene}
]
with the repository boundary2 convention.

This supplies a stable meaning of the omega pattern independent of C1 formalization:
it is the image of the uniform triangle 2-cochain.

### E. Dimension 296 — only if clean
If Mathlib/submodule rank APIs make it straightforward, prove:
[
\operatorname{finrank} SceneTensorBlock=296.
]

Do not block acceptance on a long generic rank development. If dimension proof becomes disproportionate, expose the tensorBlock API and orthogonality theorem first and report the exact remaining rank lemma.

## Semantic firewall
The worker may conclude only:

- linear signed vertex sources are orthogonal to the blockwise-zero-marginal tensor sector;
- the omega pattern is a uniform triangle source;
- this supports the research classification of the tensor block as a vertex-source-decoupled candidate sector.

Forbidden claims:
- `SceneTensorBlock = TT`;
- tensor block = graviton;
- Einstein equation;
- physical radiation has been derived;
- nonlinear matter coupling is owned;
- C1 is closed.

## Acceptance gates
Run:
```bash
lake build D0.Geometry.SceneSourceStratification
lake build D0.All
python tools/validate_repo.py
python tools/generate_lean_views.py --check
python tools/validate_work.py --self-test
python tools/validate_work.py
python tools/render_work_status.py --check
git diff --check
```

No `sorry`.

Return exact theorem signatures and `#print axioms` for the load-bearing theorems.

## Exit condition
The stable literal cochain complex owns a typed blockwise-zero-marginal tensor subspace, signed-kernel inclusion, carrier-free vertex-source orthogonality, and the uniform-triangle-source omega identity, with clean `D0.All` build and no physical TT overclaim.
