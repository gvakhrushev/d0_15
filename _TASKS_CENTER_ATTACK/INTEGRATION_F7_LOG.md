# INTEGRATION_F7_LOG — guarded consolidation of the F7 (hypercharge) selector-child edge

Date: 2026-07-07. Owner-authorized GUARDED INTEGRATION. Notes-only + one ledger annotation.
**NO status flip** (F7 stays NO-GO / BRIDGE-ASSUMPTIONS-EXPLICIT). No new mathematics.
Discipline mirrors `INTEGRATION_DEGREE2_LOG.md`. Serial, incremental, small tool calls.

Source: `_TASKS_CENTER_ATTACK/ATTACK_F7_SELECTOR_CHILD_MEMO.md` §6 (row-notes section).
Skeptic-clean CONSOLIDATED result (memo §4 NO-KILL, one repair applied).

**Canonical** = `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (hand-edit ONLY by `claim_id`,
then regen `tools/sync_theory_status_map.py` + `tools/generate_lean_aggregates.py`; generated files
never hand-edited). **Assumption ledger** = `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv`
(hand-maintained canonical, edit by `assumption_id`). **`053040` NEVER touched. No git commit.**

## Dialect ground-truth (measured on disk this session, pre-edit)
- Canonical CSV: **498551 bytes, CR = 0, LF lines = 562** (558 rows + header + multi-line notes newlines).
  True dialect **pure LF**. Any `\r` post-write = a real red.
- Ledger: **18155 bytes, CR = 0** (26 rows incl header). Pure LF.

Pristine backups: `_TASKS_CENTER_ATTACK/_f7_backups/CLAIM_TO_LEAN_MAP.csv.pristine`,
`_TASKS_CENTER_ATTACK/_f7_backups/LEAN_ASSUMPTION_LEDGER.csv.pristine` (both byte-identical to disk at start).

## Targets verified VERBATIM on disk (claim_id / assumption_id)
- `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` — canonical line 361, release=NO-GO, lean=LEAN_PROVED. (memo names row 361 ✓)
- `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001` — canonical line 517, release=BRIDGE-ASSUMPTIONS-EXPLICIT,
  lean=LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS. (memo names row 517 ✓)
- `ASSUMP-KERNEL-CHARGE-LOCALIZATION` — ledger line 25, type=PHYSICS_DICTIONARY, status=EXPLICIT. (memo names ledger:25 ✓)
- corollary-of parents exist: `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (3 hits),
  `D0-P-INVARIANT-MINIMAL-001` (27 hits). Present.
- `053040`: 0 hits in canonical CSV, 0 hits in ledger (a BOOK section artifact only). Untouched by construction.

## BASELINE (before any edit) — ALL GREEN
- validate_csv PASS, **558** canonical rows
- status-inflation PASS_NO_INFLATION (558, 0/0/0) + FAIL_PLANTED control fires
- book-ledger-sync PASS · physical-bridge PASS (558) · aggregates --check PASS (idempotent)
- assumption-ledger-green PASS (+ negative controls) · ownership PASS
- **53-set: 53/53 PASS, 0 FAIL**
- `053040`: 0 hits in CSV / ledger.

---

## BATCH 1 — CHARGE-leg corollary-of edge (notes-only append, 2 rows) — APPLIED

Appended text (identical on both hypercharge rows), prefix ` F7[2026-07-07]: corollary-of `:
> F7[2026-07-07]: corollary-of D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 / D0-P-INVARIANT-MINIMAL-001 --
> the Y_{nu^c}=0 charge residue is the selector-M1-no-go in the charge sector (single-vertex covector,
> not Aut-invariant, vanishes on ker A; the only Aut-invariant covectors are the 3 zone-indicators, all
> zero on the 30-dim kernel).
(ASCII transliteration nu <- ν, matching the anomaly-variety row's own `nu_R`/`nu^c` style.)

Applied to: `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` (line 361) + `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001` (line 517)
via `scratchpad/f7_batch1.py --apply` (csv roundtrip, deep-snapshot confinement):
- Field-confinement asserted: exactly **2 rows** differ, **`notes` field only** on each; append-only
  (new notes startswith old); all other fields byte-identical. `release_status` + `lean_status`
  asserted **byte-unchanged** on both (NO-GO / BRIDGE-ASSUMPTIONS-EXPLICIT; LEAN_PROVED /
  LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS preserved).
- Note carries NONE of the inflation markers (`open inside` / `not yet closed` / `proof-target still open`).
- Whole-file diff vs pristine: exactly 2 changed rows (leading claim_id confirmed) — the third
  `GRAPH-FLOW-OWNER` hit is a substring inside the variety row's own notes, NOT a changed row.
- byte-delta **+676** = 2 x 338; dialect **CR 0 / LF 562** (pure LF); row count unchanged **558**;
  `053040`: 0 hits.
Regen: `sync_theory_status_map.py` -> Synced 558 claims; `generate_lean_aggregates.py` rewrote
All.lean + ClaimMap.lean + ActiveClosureIndex.lean.

**Guard board after BATCH 1 — ALL GREEN. KEPT.** validate PASS (558) · status-inflation PASS_NO_INFLATION
(558, 0/0/0, planted control fires) · book-ledger PASS · physical-bridge PASS (558) · aggregates --check
PASS · ledger-green PASS + 3 controls · ownership PASS · **53-set 53/53 PASS 0 FAIL**. Row count 558 (notes-only).

---

## BATCH 2 — assumption-ledger LOC/CHG split annotation (justification-only, 1 row) — APPLIED

Target: `ASSUMP-KERNEL-CHARGE-LOCALIZATION` (ledger:25). Appended to the `justification` field:
> SPLIT (F7 attack 2026-07-07): bundles (a) LOCALIZATION nu_R in ker A -- kernel structure CERT-CLOSED
> owned, physical kernel=neutrino identification is R2 MECH-LIMIT (D0-GRAPH-SPACE-NO-ISOMETRY);
> (b) CHARGE Y_{nu^c}=0 -- corollary of the selector-M1-no-go (M1-forbidden single-vertex label).
> Different codimensions (3 vs 1, not equivalent, BOOK_04:1408).
(ASCII transliteration nu <- ν, matching the ledger row's own `nu^c`/`nu_R` style.)

Applied via `scratchpad/f7_batch2.py --apply` (csv roundtrip, deep-snapshot confinement):
- Field-confinement asserted: exactly **1 row** differs, **`justification` field only**; append-only;
  all other fields byte-identical. `assumption_type` = **PHYSICS_DICTIONARY** and `status` = **EXPLICIT**
  asserted **byte-unchanged** (annotation only, NOT a type/status change; NOT a structural split into
  two rows).
- byte-delta **+354**; dialect **CR 0** (pure LF); ledger row count **unchanged (26 incl header)**;
  `053040`: 0 hits.
- NOTE: the ledger is the hand-maintained canonical (no regen needed for the ledger itself; it feeds
  the ledger-green / ownership guards directly).

**Guard board after BATCH 2 — ALL GREEN. KEPT.** assumption-ledger-green PASS + 3 reachable controls ·
ownership PASS · validate PASS (558) · status-inflation PASS_NO_INFLATION (558, 0/0/0) · book-ledger PASS ·
physical-bridge PASS (558) · aggregates --check PASS · **53-set 53/53 PASS 0 FAIL**.

---

## HOLD (owner-gated — NOT done this pass; logged)
- Any `release_status` / `lean_status` flip on the F7 rows — **HELD**; F7 stays NO-GO /
  BRIDGE-ASSUMPTIONS-EXPLICIT (all statuses byte-unchanged).
- Splitting `ASSUMP-KERNEL-CHARGE-LOCALIZATION` into TWO separate assumption rows (LOC + CHG) — **HELD**.
  A true split is a structural ledger change (new assumption_id, new lean/cert owners) — owner decides.
  This pass is **annotation-only** inside the existing single row.
- Optional `theory_graph.json` `corollary-of` edge `BL-DIRECTION-BRIDGE --charge-leg--> SELECTOR-M1-NOGO`
  (memo §6.3) — **HELD**; the generated graph is regen-only from the CSV, and no dedicated edge primitive
  was authored. The corollary-of relation is already recorded in the CSV notes (BATCH 1).
- Book edits (BOOK_04:1408 anchor prose) — **HELD** (not authored/applied).

## FINAL STATE

| batch | scope | verdict |
|---|---|---|
| 1 | CHARGE-leg corollary-of edge (notes-only) on ANOMALY-VARIETY-2DIM (361) + BL-DIRECTION-BRIDGE (517) | **APPLIED** |
| 2 | LOC/CHG split annotation (justification-only) on ASSUMP-KERNEL-CHARGE-LOCALIZATION (ledger:25) | **APPLIED** |
| — | status flips · two-row ledger split · graph.json edge · book edits | **HELD (owner-gated)** |

- **NO status flip.** F7 rows stay NO-GO (variety) / BRIDGE-ASSUMPTIONS-EXPLICIT (bridge);
  ledger row stays PHYSICS_DICTIONARY / EXPLICIT. All statuses byte-unchanged.
- **Canonical CSV:** 558 rows unchanged (notes-only on 2 rows). byte 498551 -> 499227 (+676).
- **Ledger:** 26 rows unchanged (justification-only on 1 row). byte 18155 -> 18509 (+354).
- **Total byte-delta +1030** = 676 (b1) + 354 (b2), fully accounted, zero unexplained bytes.
- **Confinement:** canonical CHANGED = exactly {ANOMALY-VARIETY-2DIM-001, BL-DIRECTION-BRIDGE-001}, notes only;
  ledger CHANGED = exactly {ASSUMP-KERNEL-CHARGE-LOCALIZATION}, justification only. No ADD, no REMOVE.
- **Dialect PRESERVED (pure LF):** CSV CR 0 / LF 562; ledger CR 0. Zero CR asserted after every write.
- **`053040`:** 0 hits in CSV and ledger; no 053040-named file touched.
- **Generated files** (theory_status_map.csv, theory_graph.json, All.lean, ClaimMap.lean,
  ActiveClosureIndex.lean) regenerated via `sync_theory_status_map.py` + `generate_lean_aggregates.py`
  tools ONLY — never hand-edited.
- **Guard board GREEN after every batch** (validate · status-inflation PASS_NO_INFLATION + planted control ·
  book-ledger · physical-bridge · aggregates --check · ledger-green + controls · ownership · 53-set 53/53).
- **No git commit.**
