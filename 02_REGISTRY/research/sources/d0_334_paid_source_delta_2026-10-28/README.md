# PR #334: unpadded source row and complete QUERY/cut balance

This intake captures PR #334 commit
`172876cdf38bfce6f87fdd4a059d524b60c10eb9`, the latest head observed during
this checkpoint, relative to `c80d3dd2a917bbb2db2e2b1ab61d5216877c05e6`.
The two full changed files are byte-pinned in [`MANIFEST.json`](MANIFEST.json)
and [`upstream/`](upstream/). The three checker programs are exact extracts
from the memo; their expected JSON, seven exact replay inputs, and observed
ordinary/optimized outputs are stored under [`replay/`](replay/).

## Result and remaining application

1. On the original unpadded 42-field root and its specified source-continuation
   cube, the first CAR row of the two actual clicks is strictly negative. A
   direct-click comparison using that finite chart's original `tau=0.05` is
   nonzero even though the literal price's weighted stationary row vanishes.
   This rules out transferring the pointwise-null result to that distinct
   rank-two root by notation. It does not compute the selected complete Book
   source or identify its different paid-writer scale `tau_h=p^8`.
2. On the separate common-null QUERY construction, a global QUERY-orbit
   direction has a strictly positive fixed-cut feedback row and a finite
   comparison control. This is an ambient matrix variation, not proof that
   the corresponding continuous direction is an admitted local D0 operation.
3. Applying the full moving-cut differential to that same orbit gives a cut
   row that cancels the QUERY row under joint conjugation. The rational
   rank-one control returns `+16/35`, `-16/35`, and `0`; full heat invariance
   additionally requires the actual `Delta` transport or its own proved law.

The root, QUERY, and cut comparisons remain distinct carriers and source
normalizations. The same-execution maps for selected `F_N`, `Delta_N`, input
writer, clock, Info/work, and independent controls are still missing. The
memo's narrow source rows therefore remove a false transfer but do not prove
physical nonexistence, physical selection, or a GR solution. `GR_closed=false`.

## Replay

[`replay/receipt.json`](replay/receipt.json) records the exact PR source tree,
the seven copied input files, Python 3.13.14 with NumPy 2.3.5, SciPy 1.18.1,
SymPy 1.14.0, CPU PyTorch 2.10.0, and mpmath 1.3.0. All three embedded
controls passed in ordinary and optimized modes. Both outputs for each
control matched its published JSON byte-for-byte, and the two modes matched
each other. The recorded scope remains mathematical and finite; no physical
admission, full Book residual, or GR closure is implied.

Run the byte and input verifier from the repository root:

```bash
python3 02_REGISTRY/research/sources/d0_334_paid_source_delta_2026-10-28/verify_paid_source_delta.py
```
