# Native implementation of the concurrent all128 causal weld

Existing owner: Draft PR #334. Read [THEOREM.md](THEOREM.md).

This consumes the concurrent minimal Halmos/63-row proof and implements
its entire original Stinespring column inside the old Julia/Walsh register.
An exact forward adjoint identity, moving-source intertwiner and full
paired-heat zero-mode completion are provided. No new geometric root,
physical valuation selection or GR closure is claimed.

Reproduce without rewriting stored evidence:

```sh
OPENBLAS_NUM_THREADS=1 python check_native_weld.py
OPENBLAS_NUM_THREADS=1 python -O check_native_weld.py
```

Dependencies: Python, NumPy, SciPy, SymPy. The native constructor excerpt
is an unchanged pinned input, not a full repository checkout. Both runs
passed 71 explicit checks and printed byte-identical full JSON. The full
stdout SHA256 and selected results are in [RECEIPT.json](RECEIPT.json).
They include all128 Kraus/jet and all16384 two-tick operator/jet comparisons,
the real moving stationary preparation, the actual oldRIGHT trace factor,
and the exact minimal-to-native carrier/heat transport.

Numerical matrix controls are double-precision; general identities are
proved algebraically. No interval certification, Lean, external review or
remote CI success is asserted. Paired-cut Hodge is not identified with the
compulsory scene Hodge. `GR_closed=false`.
