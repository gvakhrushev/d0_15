# Validation of the new boundary/rigidity packet

The analytic proofs are the mathematical arguments. The three checkers are
bounded independent controls of their new matrix and symbolic formulas.
Every checker uses explicit exceptions rather than Python assertions, and
its ordinary and `python -O` stdout are byte-identical.

## Reproduction

From this directory with NumPy and SymPy available:

```bash
python check_cut_boundary.py
python check_full_boundary_source.py
python check_canonical_rigidity.py
```

Repeat each with `python -O` to check optimization-mode invariance. Exact
interpreter, dependency versions, commands, timings, script hashes and output
hashes are recorded in `RUN_LOG.json`. SymPy was reused from a preexisting
read-only dependency directory, whose location is recorded there. No runtime
dependency or original scientific source was modified.

## Executed results

| New control | Result |
|---|---|
| Original determinant mixed Hessian, ranks 1/2/3, three z values and arbitrary/Hermitian/anti-Hermitian tangents | 27 comparisons; max absolute finite-difference discrepancy for S_fb/z is 4.096624373062241e-9 |
| Golden one-return versus actual two-return/stationary-sum composition | Exact algebraic positive value difference; opposite mixed-Hessian signs at z=2^-20 |
| Full noncommuting heat mixed derivative, dimensions 3/4/6/8 | Max discrepancy 3.8685304959429345e-11; omission of either BKM or Delta_XY is detected |
| Simultaneous moving P/U/Delta full source | Max discrepancy 5.185296636511794e-13 |
| Five unitary word-slot adjoints | Max discrepancy 1.6686652060116103e-13 |
| Fixed-endpoint internal-frame word telescoping | Source residual 1.0061396160665481e-16 in absolute value |
| Ricci principal symbol, full six-component kinetic identity, trace shift, curvature anomalies, scalar flux and nonseparable control | 19 exact SymPy identities/negative controls passed |

The first integrated symbolic scalar check needed rational cancellation of
exact expressions rather than testing equality of merely expanded rational
expressions. The final checker uses SymPy `cancel` for exact algebra; no
numerical tolerance or mathematical statement was weakened.

The new files were checked with `git diff --check`; the repository validator
passed with 889 claims, 31 assumptions, 58 aliases, 183 formal-support entries,
918 Lean closure modules and zero warnings. This is structural evidence, not
a new build of those Lean modules or a scientific coverage claim.

No historical full42 solve, native lattice HDA replay, full Lean build,
physical price/admission acceptance, or GR closure was run or inferred.
`REVIEW.md` records the independent, source-specific analytic reviews.
