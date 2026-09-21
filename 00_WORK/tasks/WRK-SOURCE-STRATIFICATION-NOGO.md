# WRK-SOURCE-STRATIFICATION-NOGO

## Class
WORKER

## Priority
**1 — the only WORKER task currently authorized for execution.**

Do not start any PLANNED worker task after this one. Finish this task, open the PR, move it to REVIEW, and stop for CONTROL.

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Repository / launch protocol
Repository: https://github.com/gvakhrushev/d0_15

At launch:
```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git status --porcelain
```
The tree must be clean.

Create a fresh branch from the fetched `origin/main`:
```text
work/source-stratification-nogo
```

Report the exact base SHA before editing.

Do not reuse any local dirty worktree, stale branch, or generated olean state as evidence.

## Objective
Formalize the smallest theorem-ready part of accepted A-RAD/A-STRESS research without depending on the failed C1 attempt.

Own directly from the stable literal scene complex:

1. a blockwise-zero-marginal tensor subspace on `SceneC1`;
2. its inclusion in the signed kernel;
3. carrier-free orthogonality of every signed vertex gradient/source to that subspace;
4. the literal uniform triangle-source identity for the block-constant omega pattern.

This task is intentionally small. The goal is a fast green theorem owner, not the full 296-dimensional representation theory.

## Required context
Read before editing:

- `02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`
- `02_REGISTRY/research/ASTRESS_QUADRATIC_MATTER_TENSOR_SOURCE.md`
- `02_REGISTRY/RESEARCH_LEDGER.md`
- `02_REGISTRY/claims.csv` row `D0-HODGE-LINKS-001`

Stable Lean owners:

- `D0.Topology.GenericTripartiteHomology`
- `D0.Geometry.SceneCochainComplex`
- `D0.Geometry.SceneHodgeDecomposition`

PR #44 is a **closed failed attempt** and is not an implementation dependency. Do not import `D0.Geometry.SignlessSignedCommonCarrier`.

## Target module
Preferred:
```text
03_FORMALIZATION/D0/Geometry/SceneSourceStratification.lean
```

Add it to `D0.All` only after the module builds by itself.

## Required theorem package

### A. SceneTensorBlock
Define a `Submodule ℚ SceneC1` whose elements have zero row and column sums separately in all three literal edge blocks.

The public API must expose the actual marginal equations; do not hide the meaning behind an opaque predicate only.

### B. Signed-kernel inclusion
Prove:
[
SceneTensorBlock le ker(sceneBoundary1.mulVecLin).
]

Use the literal signed incidence already owned by `SceneCochainComplex`.

### C. Carrier-free vertex-source orthogonality
For every `f : SceneC0` and `z : SceneTensorBlock`, prove the Euclidean pairing of the signed vertex gradient with `z` is zero.

Prefer the already-owned adjointness theorem rather than re-expanding the matrix if that keeps the proof small.

Suggested semantic theorem name:
```text
vertex_source_orthogonal_to_tensorBlock
```

This is a source/tensor orthogonality theorem, **not** a TT theorem.

### D. Literal uniform triangle source
Define
[
omega_{scene}=(13,-11,9)
]
blockwise on the three edge zones.

Prove:
[
sceneBoundary1.mulVec,omega_{scene}=0.
]

Then prove the repository-convention identity:
[
sceneBoundary2.mulVec(mathbf 1_{SceneTriangle})=omega_{scene}.
]

**Normalization firewall:** with `omega_scene=(13,-11,9)` there is NO extra factor 13. If a normalized vector
[
omega=(1,-11/13,9/13)
]
is introduced, then and only then `sceneBoundary2.mulVec 1 = 13 • omega`.

### E. Optional dimension theorem
Only if clean and short:
[
operatorname{finrank} SceneTensorBlock=296.
]

Do not hold the PR hostage to this dimension proof. The load-bearing exit condition is A–D.

## Explicitly out of scope
Do not formalize in this task:

- general `K(a,b,c)`;
- the character-theoretic `dim Hom_H(Sym² C0,Z)=3`;
- quadratic matter sources;
- source-carrier selection;
- TT/readout;
- C1 common carrier;
- Hodge kinetic selector;
- Einstein interpretation.

## Semantic firewall
Allowed conclusion:

> the literal blockwise-zero-marginal scene sector is signed-divergence-free, is orthogonal to all linear signed vertex sources, and the block-constant omega pattern is a uniform triangle source.

Forbidden:
`SceneTensorBlock = TT`, graviton, physical radiation, Einstein equation, nonlinear matter coupling owned, or C1 closed.

## Gates
Run from the clean branch:

```bash
lake clean
lake build D0.Geometry.SceneSourceStratification
lake build D0.All

python tools/validate_repo.py
python tools/generate_lean_views.py --check
python tools/validate_work.py --self-test
python tools/validate_work.py
python tools/render_work_status.py --check
git diff --check
git status --porcelain
```

No `sorry`.

Run `#print axioms` for the load-bearing theorems only after the clean build succeeds.

## Delivery
Push the branch and open a PR against current `main`.

Only after GitHub `D0 Lean build` and `D0 guards` are green:

- set this task to `REVIEW`;
- report PR URL, head SHA, exact theorem signatures, axiom audit and CI results;
- **stop**. Do not begin C1 or any other PLANNED task until CONTROL accepts this PR.

## Exit condition
The stable literal cochain complex owns a typed blockwise-zero-marginal tensor subspace, signed-kernel inclusion, carrier-free vertex-source orthogonality, and the correctly normalized uniform-triangle-source omega identity, with clean `D0.All` and GitHub CI.
