# D0 v15 Publication Refactor Plan

This document records the hardening steps taken to turn the v15 corpus into a finished, publishable mathematical physics theory.

## Goals achieved
- Deduplication of Phase-Unfolding (master only in Book 01/02 + cross-ref).
- Centralization of no-go ledger into Book 05 (D0_NOGO_LEDGER).
- Removal of all sync anchors, v14/v15 tokens, runner markers from main books → 06_AUDIT/internal_sync_anchors.md.
- Defensive tone replaced by formal Definitions.
- q_mass retired → Boundary Residual Eigenvalue r_∂ (with migration note).
- ∂V algebra defined and used (rank(P_N), pressure law update).
- δ_0^{12} explicitly Shannon readout noise-floor.
- Archive modes separated (Determinant Expansion vs Archive Strain).
- Script logs removed from books; results moved to _RESULTS/ or audit manifests.
- Nuclear SRC integrated via F_N trace on pair overlap.
- Grand Synthesis (D0_v15_GRAND_SYNTHESIS.md) added as v15 sector-law layer.
- New closure classes in Book 05.
- Lightweight cert scaffolds for remaining operator targets.
- Publication cleanup docs created.
- All checks run (clean corpus, bridge, claim coverage, glossary, standard language).

## Positive tone rule
Books 04/07/08 now read as sector laws with explicit finite objects, operators, and theorem targets. Warnings are pointers to Book 05.

## Remaining external layers
All numerical PDG/survey/spectroscopy comparisons remain passport layer (never feed back into finite definitions).

## Version note
This refactor produces the finished v15 treatise form. No new audit reports were created; all changes are direct edits to books + the two required publication documents.
