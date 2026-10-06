# Repository claim-scope and CI audit — recovery checkpoint 2026-10-06

Repository: `gvakhrushev/d0_15`
Task: `CONTROL-PLANE`
Base: `e80a3b1ccf615fb4f70bf5900181592604928497`
Working PR: #318, Draft.

## Recovery provenance

The local worktree and unpublished commit `1df6fcc6` from the preceding execution were unavailable in this execution. This checkpoint reconstructs a bounded, independently tested subset from the actual published source at `263e29ef17151a21a89a24e8284dcae308332b56`. It does not claim to publish that old SHA or reproduce the old full validation record.

## Implemented and tested here

`03_FORMALIZATION/tools/check_claim_map_coverage.py` now accepts `UNPROVED` as an honest proof status. An OPEN/UNPROVED bridge remains admissible only with an explicitly open release status and registered, nonempty assumption IDs. Neither OPEN nor UNPROVED can be released as CORE, and an open bridge cannot be presented as BRIDGE-CLOSED. A Lean-proved row still requires its module and theorem. Empty and duplicate claim IDs are rejected. The checker does not mutate the registry or infer scientific promotion.

The pure validator has 25 local unittest cases in `tools/test_claim_map_coverage.py`, including hostile closed/core promotions, missing owners, missing assumptions, duplicates, and preservation of a proved intermediate fact whose release is still PROOF-TARGET. All 25 tests passed during reconstruction.

The existing guards workflow now runs those tests and the full metadata coverage checker, followed by the existing `check_no_sorry_in_core.py --all` check. No former gate, certificate, timeout or skip condition was weakened or removed.

## Remaining original acceptance scope

The following prior local changes have not yet been recovered or validated in this checkpoint:

- README wording for the Yukawa qualitative-selector no-go, Pisot/time scope and the determinant-minus-one Fibonacci matrix;
- separate raw proof/release fields and correct open-release priority in the generated ClaimMap;
- full regeneration and the associated generator regression suite;
- exact Lean-declaration binding beyond string metadata.

These remain review obligations, not completed changes. The audit PR stays Draft. No claim/release label, Lean theorem, physical selector, continuum bridge, or active research lifecycle is promoted.

## Validation limits

The newly reconstructed validator and its 25 fixture tests ran locally. The complete repository was not available in the local execution environment; the full registry, full no-shortcuts scan and remote guards must be assessed on the new GitHub head. No full Lean build or current-head CI PASS is claimed by this document.

## Follow-up implementation in CONTROL #321

The deferred README Yukawa/Pisot/Fibonacci corrections, independent proof/release metadata, open-target precedence, generated-view regeneration and regression suite are now implemented in the #321 change set. The detailed owner is [CONTROL_AUDIT_TAIL_CLOSURE.md](CONTROL_AUDIT_TAIL_CLOSURE.md); acceptance still requires its actual current-head CI. Exact claim-to-declaration reconciliation is separately enumerated in [CONTROL_CLAIM_REFERENCE_AUDIT.md](CONTROL_CLAIM_REFERENCE_AUDIT.md), not passed off as string validation. Historical recovery limitations above describe the earlier #318 execution, not a loss of its now-published files.
