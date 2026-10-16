# Balanced full-Lorentz q3300 path

The exact conclusion and interval margins are in [`RESULT.json`](RESULT.json).
The consuming theorem is
[`A4D_FULL_LORENTZ_BALANCED_MEMORY_PATH.md`](../../A4D_FULL_LORENTZ_BALANCED_MEMORY_PATH.md).

Replay from the repository root with Python3, NumPy, SciPy and mpmath:

```sh
python3 02_REGISTRY/research/sources/d0_full_lorentz_balanced_memory_path_2026-10-16/check_balanced_path.py
```

The checker pins the full-Lorentz exact source result and the fixed interval
owner, and evaluates the direct q3300 block on the complete native
13-coordinate mean slice. A pinned finite-decimal matrix is used only as a
coordinate preconditioner, with its left inverse checked by interval
arithmetic; no field mode is removed. The balanced `K=S_chi-I` is recomputed
from the owned CAR generators using exact Gaussian-integer arithmetic. The
checker encloses both endpoint forms over the entire owned root box. A
single basis, chosen at the midpoint only to propose a witness, is then
checked by outward interval arithmetic. Strict negative scalar and
positive-complement signs at both endpoints imply the same signs along the
affine pencil; the Schur complement gives inertia `12+/1-` over the complete
segment.

The old unbalanced pure witness is an explicit hostile control: its exact
occupation counts fail the full-Lorentz balance, as independently recorded
by the pinned source theorem. This packet does not transfer that old
crossing, infer an all-mode statement, or establish admission by the
original native D0 primitives. See [`INPUTS.json`](INPUTS.json) for source
hashes and [`VALIDATION.json`](VALIDATION.json) for the executed replay.
