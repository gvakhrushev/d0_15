# SOURCE #310: byte-preserving v4/v5 intake and replay

Date: 14 October 2026. Input branch head checked: `c25de08740debd31b4ddac887c9c9ba05f9c077d`.
Research only. Original task and Draft lifecycle stay open. No CORE, BOOK,
claim, Lean owner, task row or old immutable certificate is edited.

The previously local v4 and v5 payloads are now preserved as a hash-pinned
source capsule under `sources/d0_v4_v5_verified_capsule_2026-10-14/`.
This is NOT a claim that 83 individual expanded Git blobs were uploaded:
the eight binary parts encode 82 original UTF-8 files and the deterministic
recipe for the one original v4 ZIP. `restore.py` reconstructs every one of
all 83 original patch paths and verifies its SHA256 before writing anything.
Original text, proofs, programs, input receipts, logs and the nested v4 ZIP
were verified byte-identically after restoration. No network is required.
The redundant outer transport ZIP is not stored; its source hash is pinned.

Restore for inspection without changing the research tree:

```
python 02_REGISTRY/research/sources/d0_v4_v5_verified_capsule_2026-10-14/restore.py --destination .build/v4-v5-originals
```

Default CI-safe replay:

```
python 02_REGISTRY/research/certificates/a4d_v4_v5_verified_capsule_check.py
```

Use `--full-replay` for the original interval, simulator, optimized and hostile
program suites. Temporary restoration keeps legacy result-writing programs
away from the versioned source. Restoration rejects differing existing files,
escaping paths, modified parts and a ZIP encoder that does not reproduce the
original hash; it never silently normalizes or replaces original evidence.

## Independently repeated checks in this execution

The original v4 full suite passed five groups: exact normal/optimized,
interval normal/optimized, and hostile replay (seven modified programs and
two false-scope receipts). The original v5 full suite passed fourteen groups,
including optimized runs and actual program mutants. Both original source
and receipt trees remained unchanged. The new capsule default wrapper passes
and its restoration checks all 83 file hashes. A separate combined wrapper
full run hit the container's external timeout; this is NOT presented as a
successful combined wrapper run. The separate original full suites did pass.
No fresh Lean compilation or current-head GitHub CI is inferred from this.

## Preserved scientific boundaries

V4 constructs a full reversible first-success selector with a nonzero all-fail
branch and an explicit preparation/selection source. V5 compiles the selector
approximately inside an addressed golden/CNOT palette, retaining relative
phases and full-state jet error. Its extremely large declared word is an
existence budget, not an executed 10^68-gate simulation or practical device.
Addressing, blank resources, physical capacity, pi0 placement, the physical
full action and native refinement are not thereby derived.

The all-data archive action differs from the selected-output action.
Negativity of the prior radial witness assumes the stated trace preparation,
not every normalized state. A cold archive is a countercontrol, as the parallel
`A4D_NATIVE_UNCONDITIONAL_ARCHIVE_ACTION.md` correctly records. The full moving
mixture retains its c*dR0 term. Neither J_program nor its radial invariance is
silently identified with the original state-conditioned chronological J.
The separate #322 448-artifact snapshot remains unchanged and does not
retroactively accept this intake. Independent CONTROL review remains required.
