# #334 §7fi: born full128 history and independent readout reduction

This is a **pinned owner-source intake**, not independent scientific or
physical acceptance. It preserves the full diff
`c4dfd283348093ede9c1ebacefa731abad75d3bd..800701f84b0d8b2970556421afd2b0887be68561`,
both complete resulting owner blobs, the exact embedded checker and owner
receipt, and all 19 pre-insertion input blob and SHA-256 pins. The
[manifest](MANIFEST.json) records these. The earlier
[§7fh intake](../d0_334_post_201_c4d_intake_2026-11-05/README.md) retains the
previous argument. Source hashes are checked against local Git objects.

The owner constructs the target history from five canonical births, including
the live phase, with seven fresh record births per tick and all old records
retained. On the stated complete fine-record CQ component this gives a pure
active input and Shannon-gain expression, without a stationary mixed bank.
The supplied fixed-chart mixing theorem and compilation bounds give a
conditional intensive source approximation. Finite preparation rows need not
vanish; this does not establish a physically admitted execution or full price.

The negative result is essential: independently varied ordinary-pair output
rotors have nonzero full temporal source when the stated occupation is
positive. In the owner's two-tick fixture the two rows are about `0.0406765`
and `0.0406759`. On the component's own stationary rotor section, the owner
computes a strictly positive diagonal Hessian for positive occupations and a
reduced field source `Ds_* - p^3 Dw_*`; using the unreduced source after
eliminating those rows would lose that correction. Zero-occupation rows remain
degenerate. Whether these rotations are admissible free variables of the same
task, or guarded with an actual reaction, is not selected by the calculation.
Other components of the true ledger can alter the full stationary section.
The independent retention obstruction of §7fg also remains; neither decaying
initial source nor this component calculation removes it. Actual admission,
preparation/field map, complete clock/work and physical Cost−Info, nuisance
rows, Einstein-source comparison and reverse recovery remain open.
`scientific_promotion=false`, `GR_closed=false`.

## Reproduction and limits

[check_born_history.py](check_born_history.py) is extracted byte for byte. It
uses the exact preceding `7fh.G1` checker as an AST loader and the original
uniform constructor. Both separate dependencies are retained and hashed.
The replay creates a synthetic scratch primary containing only the exact
predecessor code block at its required heading, plus the unchanged original
constructor at its original relative path; it does not claim the synthetic
container is the full original primary. The verification script compares the
full source snapshots, original embedded blocks and 19 input pins separately.

The owner checker records 65 conditions: 42 **nominal numerical**, 11 exact
symbolic, 8 structural and 4 provenance. The numerical controls are not
interval certificates; the two-tick fixture does not establish the all-horizon
analytical claims or physical admission.

Normal and `-O` runs with `-Werror`, Python 3.12.13, NumPy 2.5.4, SciPy
1.18.1 and SymPy 1.14.0 passed with identical stdout SHA-256
`f1c8d9edaf6dee7842a40a406d4b8fec6e166ec9e04a96ad49fc91ec9971cf40`
and empty stderr. This differs from the owner receipt because the available
Python/NumPy/SciPy versions differ; selected floating results and maximum
residual differ as recorded in [comparison.json](results/comparison.json).
The owner's exact dependency stack was unavailable offline.

Python 3.9.6 / NumPy 2.0.2 / SciPy 1.13.1 / SymPy 1.14.0 failed in both
modes under `-Werror` on a divide-by-zero warning in the original constructor's
matrix multiplication; stderr is retained in [results](results/). The run did
not complete the 65 checks, and no warning was suppressed.

Integrity verification without executing owner code:

```sh
python3 02_REGISTRY/research/sources/d0_334_post_c4d_800_intake_2026-11-05/verify_intake.py --verify-source-objects
```

Replay executes pinned owner code in scratch, **not a sandbox**; checker and
both dependency hashes are checked before each invocation, nonempty stderr
fails the run, and normal/optimized receipts must match:

```sh
uv run --offline --python 3.12 --with numpy --with scipy --with sympy python 02_REGISTRY/research/sources/d0_334_post_c4d_800_intake_2026-11-05/replay_bounded.py
```

Hostile file and stderr controls run without executing owner code:

```sh
python3 02_REGISTRY/research/sources/d0_334_post_c4d_800_intake_2026-11-05/test_replay_bounded.py
```
