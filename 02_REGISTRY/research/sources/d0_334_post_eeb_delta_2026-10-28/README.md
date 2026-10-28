# PR #334 continuation after `eebcb5e` — exact source intake

This packet extends the earlier #334 snapshots already integrated in PR #402.
It preserves the exact source range `eebcb5e467742df3e9cf7fa9702042d7294aa742` to `726192353504a81a9ab2b751f9b6c7866271e75a` from the same open Draft
PR, the changed-file inventory, every complete changed file at the head, and
the full binary-capable Git patch. Source snapshots and patch are losslessly
compressed so their original whitespace and bytes stay intact. It does not replace the nine-package chat
intake, the moving-projector source, or the earlier retained-history and
nonlinear-dust packets.

## What this continuation adds

- **Original retained-history source and geometry.** It adds the direct
  noncommuting source, its pullback through the original all40 geometric map,
  and the full chronological heat/record/read-right accounting. The exact
  `W_j` factors and independent Lorentz-link rows stay in the source; the
  identity-weight shortcut is explicitly shown to lose link variation.
- **Changing-history scale balance.** The `7db` application retains eight
  different original full128 spatial connections, all Fourier/CAR modes,
  records, oldRIGHT and clock stages on one fixed carrier. Its complete scale
  source changes sign across the stated interval, so continuity supplies one
  scale-critical point. This is one source equation on that family, not a
  minimum, all-field stationarity, physical programme selection, or GR
  recovery.
- **Absolute price of one retained append.** The `7dc` comparison prices an
  actual three-stage record append with the original full heat and feedback.
  The owner proves a positive contrast on its stated homogeneous INTERNAL
  clock; after embedding the earlier word into the same complete carrier, the
  lower bound remains positive. For the incoming generated dust gain, the
  contrast divided by the gain diverges. This corrects that history-growth
  route only when different durations are genuine alternatives; it does not
  contradict fixed-duration stationarity or show that a task may stop before
  its required record.
- **Boundary and clock applications.** The remaining packets derive a full
  moving-cut Hessian and conditional canonical/HDA results, classify a free
  reflection QUERY orbit, and bound complete clock heat beyond a reflection
  sector. They keep the native symplectic boundary, lapse, phase descent,
  physical task domain, and same-execution field map as explicit premises.
- **Positive and negative controls are preserved together.** The direct
  nonlinear Einstein–dust result, its source and embedding controls, the
  boundary no-go results, and the changing-history balance retain their own
  carriers and do not get merged into one action or price.

## Verification boundary

At the live source check, PR #334 was open and Draft at `726192353504a81a9ab2b751f9b6c7866271e75a`. GitHub
returned no checks or status rows for that head. The packet verifier checks
only the 70 source snapshots, Git blob identifiers, manifest and exact patch;
it does not replay the owner's mathematical checkers, run Lean, establish
physical admission, or accept the result scientifically.

The owner material itself records its positive/negative checks and their
specific environments. Some updated checkers are replayed separately and
reported in `REPLAY_REPORT.md`; failures caused by unavailable dependencies
remain explicit. No new task, claim, selector or physical postulate is added.
`GR_closed=false` remains unchanged.

## Files

- `UPSTREAM_SOURCES.zip` — complete byte-exact head versions of all 70 changed paths.
- `UPSTREAM.patch.gz` — gzip-compressed exact `git diff --binary --full-index` for the range.
- `COMMITS.tsv` — the ordered 34-commit source range and subjects.
- `MANIFEST.json` — per-file path, mode, Git blob SHA-1, byte count and SHA-256.
- `verify_source_delta.py` — read-only byte/blob and optional source-object check.
- `REPLAY_REPORT.md` — exact results of this integration checkpoint.

## Packet digests

These digests pin the index, byte-exact source archive, patch storage and
replay record in this intake:

- `MANIFEST.json`: `a48683d9079508fc0a4c3caa9d4194096ac506c1114ffb0428201d97208146ef`
- `UPSTREAM_SOURCES.zip`: `abbc4125f8be39a36d9c6bdaef135f5e34a179403adbd577c228e9b6b34f164a`
- `UPSTREAM.patch.gz`: `6009d742de448711aadf7b19a5cfb975867608bb194f536e29528a32e19a7b80`
- Uncompressed patch bytes: `a7ad8b29739dff5e2290c6a44f0804dede70251c2b5759ba83021e595d4dba63`
- `replay/REPLAY_RECEIPT.json`: `927b7a8fd1a8572e2b3d1ed9b4c71fbbd8c6aa351050218e1e6834d871455a7d`
- `replay/REPLAY_REPORT.md`: `79e974f076f3e721305e15443ece9f26debf2dcb423811e63f9b17f2e4713ab2`

Run `python3 verify_source_delta.py` for archive/member integrity. Add
`--verify-source-objects` when both source commits are available in the local
Git object database; this also compares every extracted member and the
decompressed full patch with those exact Git objects. For direct inspection,
extract `UPSTREAM_SOURCES.zip` with a standard ZIP tool and decompress the
patch with `gzip -dc UPSTREAM.patch.gz`.
