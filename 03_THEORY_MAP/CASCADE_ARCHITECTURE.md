# D0 Cascade Architecture — single source of truth, no manual sync

## Problem (diagnosed 2026-07-01)
The repo has the right instruments (canonical registry, graph, status maps, assembled
books) but they are updated **pointwise**, so prose drifts from the verified core:
- 31 prose↔ledger status desyncs (29 books under-state what Lean proved; 2–3 over-state it)
- 278 / 523 registered claims have **no book prose** at all (131 of them CORE-FORMALIZED)

This is structural, not per-claim: two independent generation chains that never cross-check.

## The two existing cascades (already correct — do not replace)
```
CLAIM_TO_LEAN_MAP.csv  ──regen_graph──▶  theory_status_map.csv
   (SINGLE SOURCE                        theory_graph.{json,dot,html}
    OF TRUTH; +                          theory_semantic_index.md
    LEAN_ASSUMPTION_                      LEAN_CORE_THEOREM_INDEX.md
    LEDGER.csv)                          (GENERATED — never hand-edit)

01_BOOKS/<book>/<seq>__<id>__<slug>.md  ──assemble_books──▶  01_BOOKS/BOOK_0N.md
   (per-section SOURCE)                                       (GENERATED view)
```
`d0_status_model.py` already keeps the release-status enum identical across
validate_csv / check_firewall / d0_score, mirroring `StatusTaxonomy.lean`.

## The missing link (added here)
The two chains never met. `assemble_books.py` itself notes the plan:
*"Status-table injection … NOT done here yet … added once a normalized book_section
ownership column exists."* We supply the **join** (claim↔section by id-citation) and
the **guard** that closes the loop, so the whole thing is one cascade:

```
CLAIM_TO_LEAN_MAP.csv ─▶ graph/status (regen_graph)
                      ─▶ books (assemble_books)
                      ─▶ check_book_ledger_sync.py   ← NEW: books ⟂ ledger consistent
```

### `tools/check_book_ledger_sync.py` (read-only CI guard, like validate_csv)
Joins every claim-id cited in a per-section source to its ledger row and compares
**closure tier** (closed / mid / open over the canonical enum):
- **PROSE-OVERCLAIM** (prose asserts closure the ledger denies) → **always FATAL**.
- **PROSE-UNDERCLAIM** (prose calls open what the ledger closed) → warning; FATAL under `--strict`.

Run after regen_graph + assemble_books. The lexicons are DISCLAIMER-AWARE: a closure
word that is negated ('not a closed theorem') or adjacent to a MECH-LIMIT / NO-GO /
'named open' / 'missing artifact' marker is not counted (the D0 corpus hedges
scrupulously, so a naive keyword match false-positives). Verified v15 baseline:
**1 borderline overclaim, 70 real underclaims** across 8 books (excluding the
05.6 status-vocabulary reference section, which lists ids to DEFINE the terms).
Manual read confirmed the 2 suppressed 'overclaims' (D0-HBAR-SYMPLECTIC-...,
the adjacent-NO-GO case) were false positives — the sections are correctly hedged.

### `tools/stamp_book_status.py` (generative half — the BR2/BR3 step)
For every section that owns claims, injects/refreshes a ledger-generated status block
between `<!-- D0-STATUS-STAMP:BEGIN/END -->` markers (claim | release | Lean | cert).
Because the block is regenerated from the SSOT, book status cannot drift — update the
CSV, re-run `--write`, every stamp refreshes; `--check` fails CI on drift (like
regen_graph --check-only). Dry-run on v15: 51 sections / 498 claim-stamps. This is the
generative complement to the guard: the stamp keeps STATUS in sync automatically; the
guard catches PROSE (argument-level) contradictions a stamp can't express. DEFAULT is
dry-run; --write required to modify.

## Cascade discipline (how updates propagate, so desync cannot re-accumulate)
1. A claim's status changes in **one place only**: `CLAIM_TO_LEAN_MAP.csv`.
2. `regen_graph` regenerates graph + status maps (idempotent, CI-checked).
3. Prose that cites the claim lives in a per-section source; the guard fails CI if a
   section's closure language contradicts the new ledger tier → prose is updated in the
   same PR, never later. Update becomes **cascading, not pointwise**.
4. `assemble_books` regenerates the monolithic books from sections.

## Ownership join (reusable)
claim_id → owning section file(s) = the sections whose text cites that id
(245/523 today). The 278 uncited claims are the prose-coverage frontier
(`d0_prose_coverage_gap.csv`) — CORE-FORMALIZED-without-prose first.
