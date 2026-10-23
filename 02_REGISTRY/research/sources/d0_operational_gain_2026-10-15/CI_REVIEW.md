# Current-head CI review, 15 October 2026

Read head: `dcb7f76db27a849b3e33034dac176b6b306b4ecd`, existing SOURCE #310.
This is a read-only diagnosis, NOT a claim that the whole repository was replayed.

- D0 Lean build run `38676868929`: SUCCESS.
- D0 guards run `38676868927`, job `116232360152`: FAILURE.
- All earlier fast architecture/protocol/claim/no-shortcut stages passed.
- The changed-certificate executor stopped at
  `a4d_native_condensed_price_naturality_check.py`, `controls()`, line 46:
  `AssertionError: pinned_input_primary_and_prior_input_sha256`.
  Thus later certificates in that same run did not all execute.

The consumed `a4d_native_condensed_price_naturality_results.json` still pins:

| Input | Historical expected SHA256 |
|---|---|
| `a4d_native_constrained_price_source_certificate.json` | `aa2dbae962450fa1aa358553758ce22dfdc37947bb5878193ad895d4187f2614` |
| `a4d_native_constrained_price_source_results.json` | `e8bb8f7e777637034a9945a5ec7671dd872f5fa4c61f6ec7a5ad218088797f37` |

Both paths are under `02_REGISTRY/research/certificates/`.
The read current constrained-price certificate (Git blob
`3cc40ecdff5ad6f898057608c7cebe29cf31820a`) instead pins its result by SHA256
`1cb0db0934b59c25a236bd43d69581e5f41b27e2434b4a6029b7db451c3a9f6d`.
The historical certificate blob at `1f9a1e8c...` is
`a27d5973ca9adab82333b2527a1af0d26fffb7dd`.
The two certificate JSON values differ at `lean_receipt_sha256`.

Commit `c4f91bb65f9d892ed9fbc52928c8aeab0163c6b4` changed the constrained
result's two consumed joint-field-quotient receipt pins, preserving the
nearby checker and Lean output pins. This explains the first stale nested
receipt dependency. It does not prove that no other stale input exists.

No historical compilation receipt has been silently relabelled current;
no validator was disabled, and no old hash was blindly replaced. A complete
repair needs the transitive receipt dependency closure and either reviewed
current replay or byte-preserving snapshots of the actually consumed inputs.
The new `audit_pins.py` can list all mismatches of this specific receipt on
a real checkout, read-only. It reports paths rather than the old generic error.
It is not a general automatic acceptance/rehashing tool.

The separately new operational-gain packet passes its local mathematics,
optimized run, and actual mathematical mutations. This does not change the
failure state of the old repository run above.
