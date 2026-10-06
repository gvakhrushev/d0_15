# CONTROL: reviewed arithmetic resonance checkpoint

Repository: `gvakhrushev/d0_15`
Task: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
Base: `02f4db9afd785457974c09907ef2cfdf76dcc386`
Execution: PR #320, `control/a4d-resonance-reviewed-checkpoint`.
Status: finite/arithmetic artifact intake; original classification remains OPEN.

## Source and acceptance boundary

The user authorized integration of accumulated reviewed results. This is a
CONTROL artifact checkpoint, not a relabeling or merge of EXPENSIVE PR #317.
Its task row, original brief and unresolved terminal are retained on main.
The existing CONTROL scope is extended only by the explicit checkpoint clause
in its brief. No claim/release/BOOK/Lean promotion is made.

Source: #317 at `6853ce4c0563392f78a6c5ee6cf898941e8d448a`, with the independent
SD/ASD replay repair at `3b75c11ac4dec7687801ee559fa7fc7687ccdfaf`.

Accepted mathematical scope: exact reconstruction of the 24-by-24 A symbol;
Hodge similarity/congruence identities with their different normalizations;
additive complex rank and physical-unit-torus-only rank doubling; exact
univariate restrictions; degree-18 671-coefficient chiral determinant;
irreducibility over Q(i), nonassociate conjugate factors and generic arithmetic
prime-divisor rank 23. The complex rank-23 control, physical intersection point
and diagonal Smith data retain their explicit carrier restrictions.

Still OPEN in #317: absolute factorization over C and complete higher-codimension
rank-drop ideals/strata. This checkpoint proves no stationary continuation,
response-universality, sufficient-memory or nonlinear Einstein theorem.

## Imported files and provenance

All paths below are relative to `02_REGISTRY/research/`. Eight original blobs
and the repaired SD/ASD checker form the reviewed mathematical slice:

| Path | Imported Git blob |
|---|---|
| A4D_RESONANCE_DIVISOR_STRATIFICATION.md | b8f78ab89131161b73b5e0b82da0ce6222e4fa46 |
| certificates/A_and_mixed_symbol_entries.json | 8e72ba08cacc9fc7a3c5638532a86b963a5f346b |
| certificates/a4d_hodge_structural_review_check.py | 13e0f66f32ebceb88336a0ae4e71e879458d792a |
| certificates/a4d_hodge_structural_review_results.json | df4e9a15f5ddca75bd822b4a2051d2c18132eb20 |
| certificates/a4d_resonance_divisor_chiral_numerator.json | a7bceb43214c5410d91305613ba157930f167484 |
| certificates/a4d_resonance_divisor_slice_check.py | a08f9df125473130ef20bfad0d75cf18675aa89b |
| certificates/a4d_resonance_divisor_slice_results.json | a525463b484ed6ec3b24acaa7b0bef8ebe044f73 |
| certificates/a4d_sd_asd_reduction_check.py | 4c3409787789966c7b00a32f445bacf34ba48d9a |
| certificates/a4d_sd_asd_reduction_results.json | e7692f86a469f5f21aaaecd24969b5a2ca461cad |

The three existing HANDOFF, MASTER_BRIEF and PUBLICATION_CHECKPOINT documents
are also preserved byte-for-byte for historical references and provenance.
They are research dispatches, NOT additional accepted theorems or current
execution authorization. Where an old dispatch differs, follow the exact task
brief and `CONTROL_RESPONSE_MEMORY_CONSOLIDATION.md`, especially its fixed-source
identity and finite-stencil/memory limitations. Do not restart #310 from an old
pinned head.

## Replay and integrity

The original #317 run 37422182140 passed the Hodge and global arithmetic
factorization checks but timed out in SD/ASD at its default 180-second limit.
The repair changes two determinant computations to exact domain-ge elimination,
prints stage progress, and compares the SD/ASD result with the immutable original
JSON instead of rewriting it. No rank test, determinant identity or source input
was removed. The repaired complete SD/ASD replay passed all 21 checks locally,
including equality with the original JSON. The Hodge replay passed 19 checks.
The complete global divisor replay also reached its terminal locally with the
671-term coefficient ledger and all original outputs unchanged.

The legacy Hodge/divisor replays currently serialize their recomputed JSON.
The checkpoint adds `zz_a4d_resonance_checkpoint_integrity_check.py`, which pins
the three original result hashes plus source table/coefficient ledger and fails
if any differs after replay. Existing outputs are not silently updated for a
PASS. This integrity check is not a replacement for running the three owners;
all four changed scripts are run by the existing guards loop. No timeout or
skip condition is relaxed.

Before merge use Ready/current-head CI, not a historical run. The scope is
research-only: no mathematical Lean source or registry claim changes, no task
retirement and no public physical promotion. Future #317 changes should compare
against these imported blobs and preserve the unresolved classification task.
