# PR #334: return boundary and conditional rigidity delta

This immutable intake preserves the 21 files changed between PR #334 commits
`c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a` and
`c80d3dd2a917bbb2db2e2b1ab61d5216877c05e6`. The source copies are under
[`upstream/`](upstream/); [`MANIFEST.json`](MANIFEST.json) pins each Git blob,
byte count, and SHA-256. The local replay is separate under [`replay/`](replay/).

## What the delta establishes

- The unchanged finite return functional has an exact endpoint mixed-Hessian
  formula. Its coefficients separate Hermitian and anti-Hermitian endpoint
  components, and a finite difference control detects incorrect coefficient
  or mode-gap substitutions.
- Differentiating the complete thermal-plus-return source retains moving-cut,
  moving-unitary, and moving-heat contributions. The full matrix source and
  word-adjoint chain agree with bounded derivative controls.
- A Schur reduction of the stationary internal coordinate yields a boundary
  Hessian and a symplectic boundary relation only on a regular, twisted chart;
  determinant sewing retains the internal determinant source.
- The conditional canonical classification obtains coefficient constraints
  from its stated canonical variables, curvature potential, kinetic class,
  and strong deformation-algebra hypotheses.

These are finite algebraic identities, matrix controls, and a conditional
continuum classification. The matrix chart is not the original D0 causal
boundary. This intake does not construct the D0 symplectic form or native lapse
generators, prove their source map, replay the original all42 system, or select
the hypotheses from an admitted execution. It adds no Lean result or physical
selector. `GR_closed=false` remains unchanged.

## Local checker replay

[`replay/receipt.json`](replay/receipt.json) records four checkers run in
ordinary and optimized modes using Python 3.13.14, NumPy 2.3.5, SciPy 1.18.1,
SymPy 1.14.0, and CPU PyTorch 2.10.0. Every run returned its declared PASS
status; ordinary and optimized outputs were byte-identical for each checker.
The exact canonical/scalar checker matched its published output byte-for-byte.
The numerical matrix checkers differed slightly from the published JSON under
the local macOS arm64 environment: maximum numeric differences were
`3.49e-11` for the endpoint-Hessian control, `2.75e-11` for the complete-source
control, and `2.53e-8` for the implicit-map Jacobian error in the boundary
control. Their internal bounds still passed. These runs do not certify the
physical source map, D0 boundary, or GR closure.

Re-run the source verifier from the repository root:

```bash
python3 02_REGISTRY/research/sources/d0_334_boundary_rigidity_delta_2026-10-28/verify_boundary_rigidity_source_delta.py
```
