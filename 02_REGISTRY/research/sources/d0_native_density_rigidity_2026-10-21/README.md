# Density rigidity, common stationary sets and common Jacobi kernels

Derived continuum result inside the existing PR #334 research programme.
`PROOF.md` gives the analytical theorem, assumptions, geometric dust
converses and limits. `SOURCE_PINS.json` records the exact inherited input
bytes. The checker verifies the new symbolic identities, rational bounds,
input hashes and a small set of actual-detector numerical fixtures; it does
not replay the old compiler, all40, Bianchi or Lean suites.

## Run

Dependencies: Python 3, SymPy and mpmath. From the repository root:

```sh
python3 02_REGISTRY/research/sources/d0_native_density_rigidity_2026-10-21/check_density_rigidity.py
```

The default repository path is inferred from that canonical packet
location. From any scratch location, specify the repository explicitly:

```sh
python3 /path/to/packet/check_density_rigidity.py --repo /path/to/d0_15
```

The program prints a JSON result and raises an exception on a failed
condition, including under `python3 -O`. `RESULT.json` is the recorded
normal run; `RESULT_OPTIMIZED.json` is its byte-identical optimized replay.
`FROZEN.json` records final artifact hashes.

## Preserved input snapshot

The spatial-weights source acquired an append-only Section 7 pointer during
concurrent work after this packet's recorded `dfc0275e` read head. Its
original evidence is preserved byte-for-byte in `inputs/`, with the original
repository path, git blob and SHA256 unchanged in `SOURCE_PINS.json`.
For that entry the checker reads `snapshot_path` relative to this packet;
the other seven source pins still read their repository paths. This keeps
the reviewed proof reproducible after the concurrent merge without silently
repinning it to a newer source version.

## Scope

The conclusion concerns the specified constant-parameter, fixed-measure
continuum action and its full independent coframe, connection and two-real-
scalar variations. It gives identical complete stationary sets for every
admitted fixed finite cap, and identical full Jacobi kernels with a fixed
collar. It also constructs local timelike/null irrotational Einstein-dust
representatives in specified mass coordinates. It does not make the
nonlinear action diffeomorphism invariant or prove finite native-lattice
admission, internal source equations, physical Book selection or GR closure.
