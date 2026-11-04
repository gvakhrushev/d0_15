# PR #402 cold-start pin-window recheck — 4 November 2026

## Result

The complete runner finished on clean snapshot `a8ca4d8974b14ee332554268fce275f58ebbf6c3`. The result window remains 18; 49/50 scenarios still find every required source. The 51 benchmark controls pass, including the exact-source-versus-unrelated-prose impact regression. `pr334-native-kappa-owner-delta` remains incomplete.

The previous receipt grouped all 44 owner-source misses under a single “not enough matching query terms” description. The new content-status field distinguishes the actual cases without changing search acceptance:

- **23/67** owner texts appear as direct-content results inside the 18-item window.
- **40/67** exact pinned texts pass direct-content matching but rank outside the returned window; they remain `found=false` for this search case.
- **4/67** exact pinned texts fail the existing lexical threshold.
- The 17/17 query-to-pin locator files remain present. The separate owner-manifest test verifies all 68 changed paths by exact `commit:path` Git blob, byte count, and SHA-256. The 5,061,506-byte memo remains pin-only because it exceeds the 4 MB content-search cap.

The new receipt adds `content_status` to pin references while preserving the established `pin_status` field. No query threshold, ranking window, required-source scope, claim status, or physical interpretation was relaxed.

## Validation

- Full cold-start: 49/50 scenarios; 51/51 benchmark controls; window 18.
- Compacted output: 2,834,280 bytes; SHA-256 `9a835af703e7cc6b280441972fdd2a8fb460734bcf9b096e74d8a2dfd03ed65c`.
- Full output remains outside Git at `/tmp/d0_pr402_cold_start_2026-11-04_a8ca4d89.json`; SHA-256 `149ed43fe9f30255220e5548ab9881814a1243ecf93fca72e34129e1eb5de910`.
- The focused receipt/search tests, cyclic-AF pin boundary, Julia default search window, and 68-path owner pin regression passed. CI `lean-build` and `guards` passed on the snapshot.

This classification correction does not change the finite Lean result or bind it to admitted physical execution. `GR_closed=false`.
