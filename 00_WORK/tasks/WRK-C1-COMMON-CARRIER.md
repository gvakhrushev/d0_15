# WRK-C1-COMMON-CARRIER

## Class
WORKER

## Priority
**1 — IN_PROGRESS. This is now the only ordinary WORKER task authorized for execution.**

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Repository
https://github.com/gvakhrushev/d0_15

## Restart decision
PR #44 is closed and superseded as an implementation attempt. Do **not** reopen it, branch from it, cherry-pick its proof scripts wholesale, or treat its local-build reports as evidence.

The mathematical C1 result is not rejected. `D0.Geometry.SceneSourceStratification` is now accepted on main, so the new implementation must start from a fresh branch off current `origin/main` and reuse that stable owner where appropriate.

Preferred branch:
```text
work/c1-common-carrier-v2
```

The old branch may be read only as mathematical/proof-engineering reference.

## Objective
Own the literal common-carrier theorem on `K(9,11,13)`:

- unsigned endpoint-sum operator `BPlus`;
- signed incidence `BMinus` identified exactly with `sceneBoundary1`;
- kernel dimensions 326 and 327;
- explicit involutive Euclidean isometry `U`;
- 10-dimensional centered-row correction;
- omega complement/decomposition.

## Stable inputs
Read first:

- `02_REGISTRY/frontier/C1_COMMON_CARRIER_RESULT.md`
- `04_CERTIFICATES/vp_c1_common_carrier_reduced.py`
- `02_REGISTRY/research/ARAD_SOURCE_STRATIFIED_RADIATIVE_CARRIER.md`
- accepted `D0.Geometry.SceneSourceStratification` module on current main
- `D0.Geometry.SceneCochainComplex`
- `D0.Geometry.SceneHodgeDecomposition`

Do not depend on stale frontier task prose when it conflicts with the current research ledger or accepted source-stratification owner.

## Required core statements

1. Literal `BPlus` and `BPlusLin`.
2. Literal `BMinus` with theorem:
   ```text
   BMinus X = sceneBoundary1.mulVec X
   ```
   or equality of the actual linear maps.
3. `finrank ker BPlusLin = 326`.
4. `finrank ker BMinusLin = 327`.
5. Explicit `U`, identity on two edge blocks and centered-row reflection on the 11–13 block.
6. `U_involutive`.
7. `U_isometry`.
8. `U` maps `ker BPlus` to `ker BMinus`.
9. Exact linear equivalence:
   [
   ker B_+ simeq ker B_- cap omega^perp.
   ]
10. Exact rank-10 centered row-correction owner.
11. Signed-kernel decomposition:
   [
   Y=P_{mg}Y+rac{langle Y,omegaangle}{42471}omega.
   ]

Prefer reusing the accepted literal `omega_scene` from `SceneSourceStratification` rather than redefining the same signed object.

## Proof-engineering constraints
- Use matrix-backed linear maps where possible; do not hand-prove scalar linearity with fragile Finset rewrites.
- Build incrementally after each theorem group.
- Never continue after a declaration fails and then cite `#print axioms`; failed elaboration can introduce `sorryAx`.
- No general `K(a,b,c)` development in this worker.
- No TT, Q_H selector, alpha or continuum imports.

## Semantic firewall
`BPlus` is the unsigned A1 Weyl/Ward endpoint-sum operator. It is **not** the signed Hodge/current divergence `BMinus`.

C1 is a carrier isometry/decomposition theorem. It does not by itself derive physical gravity coupling, TT dynamics, Einstein equations or a propagating omega mode.

## Gates
Fresh branch, clean tree:

```bash
lake clean
lake build D0.Geometry.SignlessSignedCommonCarrier
lake build D0.All
python tools/validate_repo.py
python tools/generate_lean_views.py --check
python tools/validate_work.py --self-test
python tools/validate_work.py
python tools/render_work_status.py --check
git diff --check
git status --porcelain
```

No `sorry`, and both GitHub workflows must be green before REVIEW.

## Exit condition
A fresh current-main implementation owns the literal 326→327 common-carrier theorem, rank-10 correction and omega complement/decomposition with reproducible clean CI and no signed/unsigned semantic collapse.

## Delivery discipline
This is the only active ordinary-worker task. After opening a green PR and moving this task to REVIEW, stop and return to CONTROL. Do not start the compensator, CAR parity, or certificate-freshness PLANNED tasks.
