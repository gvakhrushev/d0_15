# PR #334: full clock source and final composition intake

This is a source intake into the existing proof-architecture PR #402. The
scientific owner remains [PR #334](https://github.com/gvakhrushev/d0_15/pull/334);
this packet creates no new task, claim status, physical selector, or GR
closure.

## Pinned source

The packet preserves every changed file from the five-commit range beginning
at `5fe5203da2439d325dc9ef70f52c1111822fc22b` and ending at
`22e729996b70a699710a2d1120a0caa7a08decf8`. The full ordered commit list,
upstream paths, byte counts, SHA-256 values, and Git blob IDs are in
[`MANIFEST.json`](MANIFEST.json). It contains 31 files and 248,546 source
bytes. Manifest SHA-256:
`81ca9ca6d07ca1101924c1c29be41c2ab4adbb447f797e22a02e47499b443d69`.

The packet preserves the added full-clock proof and checker, the final
composition proof, its six mathematical/control checkers and receipts, and
the updated boundary and Hessian source notes. The exact upstream files are
under [`upstream/`](upstream/).

## Results consumed

- The full `K(9,11,13)` INTERNAL clock trace keeps both Hodge grades, the
  harmonic complement, and the full logarithmic trace. Its all-unitary C1/C2
  estimates do not require reflection endpoints. For the fixed homogeneous
  scene and beta in the stated interval, the C1 source is bounded by
  `A1_N ||DW||`, and the second source retains both the `||W_ab||` term and
  the quadratic first-derivative term. The actual field source transfer is
  controlled by `A1_(N_h) N_h ||L_h||/|Gamma_h|`; the bound does not choose
  `L_h`, `Gamma_h`, a physical execution, or any other changing price.
- The final composition classifies stationarity of the original QUERY return
  on its complete matrix reflection orbit. Free stationary elimination makes
  the reduced return constant; with the stated stagewise INTERNAL and fixed
  scene hypotheses, the full reduced source and boundary Schur block vanish.
  This excludes that elimination route as a source of a nonzero geometric
  equation; it does not establish that the full matrix orbit is physically
  admitted.
- The same composition checks a nonzero moment of the original boundary
  two-form, failure of arbitrary independent source-weighting to be closed,
  and four same-inventory words whose full return retains an unbounded-in-time
  memory interaction. It excludes only the specified bounded-window
  gate-only elimination; spatially local dynamics with retained state remain
  possible.
- For the separate archive-phase carrier, Hamiltonian descent has an exact
  Fourier support criterion. The native eight-stage example fails it away
  from the real base point, while positive cases remain. Continuous phase
  directions are mathematical controls and are not declared admitted native
  operations.

The remaining application is the actual same-execution map from admitted
preparation, relative QUERY/cut variations, clock and controller into
`U_N,P_N,Delta_N`, with its complete Cost-Info source, gain, norm, independent
equations, and compatible refinement. The packet neither supplies that map
nor selects a lapse/shift algebra. `GR_closed=false`.

## Replays

Run the byte verifier without executing source code:

```bash
python3 02_REGISTRY/research/sources/d0_334_final_composition_delta_2026-10-28/verify_final_composition_delta.py
```

Replay the seven pinned checkers in ordinary and optimized Python modes:

```bash
python3 02_REGISTRY/research/sources/d0_334_final_composition_delta_2026-10-28/replay/run_replays.py
```

The local replay passed all seven checkers, with ordinary and `-O` stdout
byte-identical. The six final-composition checks had no stderr; their common
published JSON fields matched exactly. The full-clock control matched its
published JSON on common fields with maximum numeric difference
`5.684341886080802e-14`. It emitted three NumPy `RuntimeWarning` categories
(`divide by zero`, `overflow`, and `invalid value` in a matrix product) in
both modes from its auxiliary scene-matrix calculation. Those warnings and
their exact stderr bytes are retained under `replay/observed/`; they were not
suppressed. The rational C1/C2 majorants and exact sign controls pass, and the
reported scene matrices and spectral controls remain finite. The checker's
analytic full-trace bound, not a diagonalization of the 530,400-mode carrier,
supports its heat-source estimate.

Replay environment: Python 3.9.6, SymPy 1.14.0, NumPy 2.0.2, SciPy 1.13.1,
and mpmath 1.3.0. The owner input `native_execution.py` is reused from the
already-pinned paid-source packet at SHA-256
`222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c`.
The [replay receipt](replay/receipt.json) records output and stderr hashes.
The [read-only verifier](verify_final_composition_delta.py) checks source
bytes, replays and scope flags without executing the mathematical checkers.
