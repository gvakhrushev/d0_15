# PR #334: original full128 retained-history source delta

This packet is an intake into the existing proof-architecture PR #402. The
scientific owner remains [PR #334](https://github.com/gvakhrushev/d0_15/pull/334).
It adds no execution task, source selector, claim status, or GR closure.

## Pinned source

The packet covers the three-commit owner range from `46ebed17` through
`716387e3`. The ordered full commit IDs, changed paths, source snapshots,
byte counts, SHA-256 values and Git blob IDs are in [`MANIFEST.json`](MANIFEST.json).
The exact proof and checker are preserved under [`upstream/`](upstream/); the
task-brief and main-memo edits are preserved as a pinned patch based on the
already archived `46ebed17` source in
[`patches/owner_delta_from_46ebed17.patch`](patches/owner_delta_from_46ebed17.patch).

The `716387e3` proof applies the direct source of the original full128 return
to the complete retained chronological history. For possibly noncommuting
one-tick operators, it derives the all-blank endpoint product, the complete
return defect, and the full source weights for each tick. Its two-tick control
uses the original CAR128 instruments and all 16,384 fine histories; it checks
that the actual consecutive Gram operators do not commute, that the complete
defect and source agree with the endpoint formulas, and that an independent
finite difference agrees. The source is not the sum of isolated one-tick
sources. The proof also records a cumulative source bound and exact repeated
fixture controls.

This removes no remaining physical premise by itself. The same-execution map
from the original full128 row to the owned geometric/all42 source is still
unproved, as are its actual gain and error norm through refinement. The new
checker explicitly reports no full-history heat replay, no Lean/repository-CI
run, no 42-field source transport, and `GR_closed=false`.

## Replay

The pinned checker passed 163 internal controls in ordinary and optimized
Python modes. Their stdout and stderr are byte-identical on this machine. The
run used Python 3.9.6, NumPy 2.0.2 and SymPy 1.14.0. Its stderr contains 102
retained `RuntimeWarning` lines: 34 each for divide-by-zero, overflow, and
invalid matrix multiplication. The warnings are preserved in
[`replay/observed/`](replay/observed/) and were not suppressed. The full
machine-readable receipt is [`replay/receipt.json`](replay/receipt.json).

Verify the pinned source and replay record without executing the research
checker:

```bash
python3 02_REGISTRY/research/sources/d0_334_retained_history_full_delta_2026-10-28/verify_retained_history_delta.py
```

Replay the exact source checker with the Python and scientific packages used
for the stored result:

```bash
python3 02_REGISTRY/research/sources/d0_334_retained_history_full_delta_2026-10-28/upstream/02_REGISTRY/research/sources/d0_original_retained_history_source_2026-10-28/check_history_source.py
python3 -O 02_REGISTRY/research/sources/d0_334_retained_history_full_delta_2026-10-28/upstream/02_REGISTRY/research/sources/d0_original_retained_history_source_2026-10-28/check_history_source.py
```

The local replay verifies the published mathematical controls under its
stated numeric tolerances; it is not an exhaustive physical-history replay,
Lean proof, scientific acceptance, or CI result for PR #334.
