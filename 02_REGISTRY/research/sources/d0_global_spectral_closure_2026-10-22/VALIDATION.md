# Validation and scope — 2026-10-22

## Newly executed

`OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python check_spectral_closure.py` and the same command with `python -O` both pass **190 active checks**. Their complete JSON stdout is byte-identical.

The new checker's conditions are explicit `require` calls, not disabled Python assertions. The handwritten interval first/second derivatives are separately compared to high-precision differentiation of a directly written scalar expression at four nonzero/zero fixtures: 32 tests, maximum scalar-jet error `4.59e-82`.

### Evidence classes

| Component | Actual evidence | Boundary |
|---|---|---|
| Whole nonlinear operand chart | 100-digit outward `mpmath.iv`, analytic interval formulas, strict signs | Covers the stated rectangle and thermal range, not arbitrary fields or unknown physical maps |
| Thermal scalar elimination | Analytical identity; 80-digit comparison of six independent operand sources and 36 Hessian entries | Not another numerical full42 lattice root |
| Source normalization | 72 exact rational curvature-basis checks, two nondegenerate coframes, using the pinned original `pair` | General normalization also follows from the epsilon/adjugate identity; finite sample checks alone are not its general proof |
| Literal scene | Exact rational 3x3 characteristic polynomial; complete 33-mode numerical trace and derivative | General edge/source theorem analytic; floating trace outputs not intervals |
| Noncommuting heat | Actual matrix-exponential mixed derivative versus logarithmic-mean formula | Independent fixture, not a computation of the unprovided physical scene-field map |
| Source limit | Analytic norm estimates; off-null fixed-positive-PF scalar diagnostic | Not generic finite-root existence or unconstrained high-frequency convergence |

## Reused original geometric theorem, actually replayed

The complete unchanged file `inputs/check_all40_arbitrary_brinkmann.py` has Git blob SHA-1
`e502807955321465903d7ab1a248e0456ac69f60`.

Its symbolic theorem and discrete harmonic calculation were executed with assertions enabled. All 16 unrestricted coframe and 24 unrestricted link components reduce to the three original rows; the two Cartan rows determine the stated staggered connection. Complete stdout is in `GEOMETRY_REPLAY.txt`.

The original checker uses Python `assert`; it is **not** replayed with `-O` as evidence.

## Previous global package

`previous/MANIFEST.json` pins the original `GLOBAL_SYNTHESIS.md`, scalar checker and saved results. Those files remain byte-identical to the prior attachment. The original scalar checker was rerun; its complete stdout equals the previously saved receipt. The replay is not promoted to an independent external review.

The separate earlier native65 causal-source patch, when included in the delivery archive, is an **unchanged archival import**. Its old numerical receipts are preserved and are not represented as a fresh native65 replay in this pass.

## Read-only acceptance

`run_validation.py` checks this packet's `MANIFEST.json`, validates prior pins, runs the four stated commands and checks source hashes again. It never rewrites expected results. `VALIDATION_RESULT.json` is the output of that wrapper and is intentionally excluded from the manifest to avoid a circular/self-modifying receipt.

`py_compile` is only a syntax check. Git whitespace checks and patch application are delivery checks, not mathematical or physical proofs.

## Not performed / not claimed

- New Lean compilation or formalization of the newly derived theorem.
- New external reviewer or independent agent audit.
- GitHub write, push, PR update, merge or remote CI.
- Physical derivation of the selected full Book03 execution and every independent input equation.
- Generic mesh-uniform source inverse, arbitrary-solution recovery, or physical universal GR closure.

The local Git delivery commit has its own real hash but is not an uploaded commit in `gvakhrushev/d0_15`. The patch contains new paths only and must be applied against the actual current branch without overwriting parallel work.
