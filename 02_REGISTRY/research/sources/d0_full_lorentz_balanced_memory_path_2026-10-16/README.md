# Balanced full-Lorentz q3300: inherited 13D restriction

The exact conclusion and interval margins are in [`RESULT.json`](RESULT.json).
The consuming theorem is
[`A4D_FULL_LORENTZ_BALANCED_MEMORY_PATH.md`](../../A4D_FULL_LORENTZ_BALANCED_MEMORY_PATH.md).

Replay from the repository root with Python3, NumPy, SciPy and mpmath:

```sh
python3 02_REGISTRY/research/sources/d0_full_lorentz_balanced_memory_path_2026-10-16/check_balanced_path.py
```

The checker pins the full-Lorentz exact source result and the fixed interval
owner, and evaluates the q3300 Hessian restriction to the complete
13-coordinate section returned by the inherited `pure_memory_interval`
stored-source owner. This is not the full transverse Hessian of the enlarged
full-Lorentz matrix interface; additional directions and their Schur
coupling are not eliminated or classified. A pinned finite-decimal matrix is
used only as a coordinate preconditioner, with its left inverse checked by
interval arithmetic; no coordinate inside the 13D section is removed. The
balanced `K=S_chi-I` is recomputed
from the owned CAR generators using exact Gaussian-integer arithmetic. The
checker encloses both endpoint forms over the entire owned root box. A
single basis, chosen at the midpoint only to propose a witness, is then
checked by outward interval arithmetic. Strict negative scalar and
positive-complement signs at both endpoints imply the same signs along the
affine pencil; the Schur complement within that section gives inertia
`12+/1-` over the complete segment. No full-interface q3300-kernel
exclusion follows.

The old unbalanced pure witness is an explicit hostile control: its exact
occupation counts fail the full-Lorentz balance, as independently recorded
by the pinned source theorem. This packet does not transfer that old
crossing inside this section, infer an all-mode or full-interface statement,
or establish admission by the original native D0 primitives. See
[`INPUTS.json`](INPUTS.json) for source hashes and [`VALIDATION.json`](VALIDATION.json)
for the executed replay.
