# Flat-record synthesis: readable preservation and continuation

Repository: `gvakhrushev/d0_15`. User-requested text intake in existing #323; #324 owns operational flow and #310 owns scientific execution. No new branch, task, claim, physical law or independent acceptance is created by this intake.

Read [the complete supplied synthesis](SYNTHESIS_RU.md), [its exact executable checker](check_flat_record.py), and [the original output](result.json). All are ordinary UTF-8 Git files: no ZIP, XZ, capsule decoder or notebook is needed.

The source establishes a conditional twelve-channel record model: flat metric, rank-ten metric variation, two retained internal directions, and an intrinsic quadratic second-form classifier. It does not derive native admission, physical Cost-Info, Lorentz dynamics, a nonzero Einstein coefficient or GR closure. Historical publication statements inside the supplied text retain their source-time meaning.

## Provenance and replay

- Supplied proof SHA256: `102790104debda459b3d0dae8d84575233ab9bdbe99f689afb15f04d974154c6` (29,007 bytes).
- This readable proof has exactly one notation-only character addition: `1-2w0=s0` becomes `1-2*w0=s0`. All other bytes are preserved. Replacing that single occurrence restores the supplied proof and its hash. Published blob: `c09ab24dc8cdfbae393252c6387c788038eddbd0`.
- Original checker is byte-identical: SHA256 `acc5f43bc652f111ab46ea090357a9e9289b1153aca1cbdc4892ec893c9de1a2`, Git blob `06f465874f07fae82111ee9453f4b5ca0b963267`.
- Original output is byte-identical: SHA256 `08f969e9f272f3b846721611f48b88491b84a53373ae2a6d6970815945e2b839`, Git blob `8de5c4ea39f18f58afd933a715d67e7787bdcfe8`.

Both ordinary and optimized Python replay were completed during this intake. Their newly computed outputs equal each other and the original output byte-for-byte. No full repository replay, new Lean compilation, physical acceptance or all-mesh result follows.

```sh
python check_flat_record.py --output /tmp/d0-flat-replay.json
python -O check_flat_record.py --output /tmp/d0-flat-replay-O.json
cmp result.json /tmp/d0-flat-replay.json
cmp /tmp/d0-flat-replay.json /tmp/d0-flat-replay-O.json
```

Dependency: Python 3 and SymPy. Output files are directed outside the immutable source tree.

## Consumer and current scientific context

Use the [existing full source evaluator](https://github.com/gvakhrushev/d0_15/blob/fe2fc53fb9479aba6c8c99c8294d25b444f7a27a/02_REGISTRY/research/A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md), not a new fitted material term. The newer [actual AF amplitude-source owner](https://github.com/gvakhrushev/d0_15/blob/34f4e68de0e7d917d80d6c139b39dcc44f010b70/02_REGISTRY/research/A4D_NATIVE_AMPLITUDE_SOURCE_REGULARITY.md) has distinct actual-state/source scopes and must not be overwritten with this interface example.

Prior complete text packet: [record geometry and expensive-AI brief](../d0_record_geometry_2026-10-15/README.md). The next result belongs in a separately labelled continuation in this directory. It must distinguish exact finite-amplitude record geometry from the still-unproved native field/action binding.
