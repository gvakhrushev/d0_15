# INTEGRATION_FABLE_LOG — applying the Fable-finalization fronts F1+F2+F3 to the canonical corpus

Date: 2026-07-06. Discipline mirrors `INTEGRATION_MINIMALITY_LOG.md` / `INTEGRATION_GROUPE_LOG.md`.
Serial, incremental, small tool calls.

**Canonical** = `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (hand-edit ONLY this file, then
regen via `tools/sync_theory_status_map.py` + `tools/generate_lean_aggregates.py`; generated files
NEVER hand-edited). **`053040` NEVER touched. No git commit.**

**Assumption ledger canonicity verified BEFORE any edit:** `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv`
is HAND-MAINTAINED CANONICAL — grep over `tools/` + `05_CERTS/`: every reference is a READER
(`sync_theory_status_map.py` input; `check_assumption_ledger_ownership.py`, `validate_csv.py`,
`vp_assumption_ledger_green.py`, `check_no_sorry_in_core.py` validators); NO writer/generator exists.
`tools/validate_csv.py` docstring confirms: canonical = CLAIM_TO_LEAN_MAP.csv "(+ LEAN_ASSUMPTION_LEDGER.csv)".

Pristine backups (byte-identical, md5-verified):
- `scratchpad/fable_backups/CLAIM_TO_LEAN_MAP.csv` (md5 2860cc932034099f6ddf5d395840cf18)
- `scratchpad/fable_backups/LEAN_ASSUMPTION_LEDGER.csv` (md5 ed320d6004ea03668ce057d6703322a1)

**Guard board** (must ALL stay green after every batch; BACK OUT on any real red):
- `tools/validate_csv.py` → PASS (row count)
- `05_CERTS/vp_status_inflation_audit.py` → PASS_NO_INFLATION + negative control FAIL_PLANTED fires
- `tools/check_book_ledger_sync.py` → PASS (0 PROSE-OVERCLAIM, 0 DEMOTED-CLOSURE-PROSE)
- `09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py --core` → PASS
- `09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py` → PASS
- `tools/generate_lean_aggregates.py --check` → PASS (idempotent)
- assumption-ledger guards (both exist, both run): `05_CERTS/vp_assumption_ledger_green.py` →
  PASS_ASSUMPTION_LEDGER_GREEN (+ 3 negative controls fire); `tools/check_assumption_ledger_ownership.py`
  → PASS_ASSUMPTION_LEDGER_OWNERSHIP

## BASELINE (before any edit) — ALL GREEN
- validate_csv: PASS, **554** canonical rows
- status-inflation: **PASS_NO_INFLATION** 554 claims (0/0/0), negative control FAIL_PLANTED fires
- book-ledger-sync: PASS (342 sections vs 554 claims, 0/0)
- no-sorry-core: PASS
- claim-map-coverage: PASS
- aggregates --check: PASS (idempotent)
- assumption-ledger-green: PASS (+3 negative controls fire); ownership: PASS
- ledger: 25 lines = header + 24 rows, last = ASSUMP-KERNEL-CHARGE-LOCALIZATION (line 25)

Target rows resolved by claim_id BEFORE editing (grep-confirmed; line# quoted for orientation only —
edits go by claim_id via csv.reader because embedded newlines make line# != row#):
- csv:51  = `D0-MATTER-REP-001` (LEAN_PROVED / CORE-FORMALIZED) — F1 M2 target
- csv:460 = `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` (LEAN_PROVED / NO-GO) — F1 M3 target
- csv:546 = `D0-WINDOW-9-13-DISSOLVE-001` (OPEN / PROOF-TARGET) — F2 target
- csv:545 = `D0-GAP-W-WITNESS-PLUS-ONE-001` (OPEN / PROOF-TARGET) — F3(b) target
- csv:361 = `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` (LEAN_PROVED / NO-GO) — F3(c) target
- csv:517 = `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001` (LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS) — F3(c) target

---
## BATCH 1 — F1 BRIDGE MINT (BRIDGE_INVARIANT_GENERATION_MEMO.md §7, post-skeptic v2) — APPLIED

Pre-flight:
- `bridge_invariant_generation_check.py` run from `_TASKS_CENTER_ATTACK/`: **rc=0, ALL CHECKS PASS**
  (output archived `scratchpad/f1_cert_out.txt`). Cited as bare filename per mint-cert precedent
  (`gap_w_witness_check.py`, `raise_selector_minimal_check.py` pattern).
- M1/M2/M3 texts extracted PROGRAMMATICALLY from the memo (lines 272/275/278, `> \`...\`` stripped) —
  zero transcription; script `scratchpad/fable_batch1.py`.
- M1 parsed as CSV: 11 fields = header width; claim_id/OPEN/PROOF-TARGET/cert verified; honesty
  clause ("HONESTY:") + RR-inheritance ("INHERITANCE (RR-1/RR-2)") asserted PRESENT in notes.
- Mint absent before (grep D0-INVARIANT-GENERATION-BRIDGE-001 = 0); M2/M3 targets resolved by
  claim_id; neither carried a `BRIDGE[2026-07-06]` note; statuses asserted byte-unchanged.

Applied:
1. **MINT** `D0-INVARIANT-GENERATION-BRIDGE-001` appended as canonical row 555
   (BOOK_04 / 04.R1 bridge / OPEN / PROOF-TARGET / cert=bridge_invariant_generation_check.py) — memo M1 text EXACT.
2. **M2** note suffix ` BRIDGE[2026-07-06]: ...` appended to `D0-MATTER-REP-001` notes (notes-only).
3. **M3** note suffix ` BRIDGE[2026-07-06]: ...` appended to `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` notes (notes-only).

Regen: `sync_theory_status_map.py` → Synced **555** claims into 03_THEORY_MAP;
`generate_lean_aggregates.py` → ClaimMap.lean + ActiveClosureIndex.lean rewritten.

**Guard board after BATCH 1 — ALL GREEN. KEPT.**
- validate_csv PASS (555) · status-inflation PASS_NO_INFLATION (555, 0/0/0, planted control fires)
- book-ledger-sync PASS (0/0) · no-sorry-core PASS · coverage PASS · aggregates --check PASS
- assumption-ledger-green PASS · ownership PASS
- Row count 554 → **555** (the one mint). `053040` untouched.

---
## BATCH 2 — F2 GAP-E FINAL NOTE (CLOSE_GAP_E_META_MEMO.md §7) — APPLIED

Pre-flight:
- §7 blockquote (memo lines 156-166) extracted programmatically, joined to ONE line
  (script `scratchpad/fable_batch2.py`); content asserted: 9th-pass KILLED (META-9th KILLED §05.8.R),
  campaign CLOSED with STOP-RULE, final residue = the one H7 sentence, the two adjudicated doors
  ((a) owner banning-sentence à la B01:1539 narrowest-candidate coset form; (b) algebraic exhaustion
  à la row 257 CASE 1), what-the-9th-bought (grammar closed-world = non-promotion force only, never
  negation). Cert cited in-note `close_gap_e_meta_check.py` verified PRESENT in `_TASKS_CENTER_ATTACK/`
  (rc=2 = the honest final state, per memo — NOT the row's python_cert column, which stays
  `window_forcing_check.py`).
- Target `D0-WINDOW-9-13-DISSOLVE-001` resolved by claim_id; pre-state asserted OPEN / PROOF-TARGET;
  no prior `FABLE[2026-07-06]` marker.

Applied: notes-only suffix ` FABLE[2026-07-06]: [GAP-E FINAL, 9-pass campaign closed 2026-07-06] ...`
(1044 chars) appended to the GAP-E row. Status columns byte-unchanged (asserted in-script):
stays **OPEN / PROOF-TARGET**.

Regen: sync 555 → aggregates rewritten (ActiveClosureIndex.lean).

**Guard board after BATCH 2 — ALL GREEN. KEPT.**
- validate_csv PASS (555) · status-inflation PASS_NO_INFLATION (555, 0/0/0, planted control fires)
- book-ledger-sync PASS · no-sorry-core PASS · coverage PASS · aggregates --check PASS
- assumption-ledger-green PASS · ownership PASS. Row count 555 unchanged. `053040` untouched.

---
## BATCH 3 — F3 R-A ASSUMP + F7 NOTES (F3_HONEST_BRIDGES_PACKAGE.md) — PARTIALLY APPLIED

### (a) ASSUMP-CLASS-RECORD-IS-ADDRESSABLE ledger append — **HELD (guards reject; backed out)**

Canonicity re-verified FIRST: `LEAN_ASSUMPTION_LEDGER.csv` is hand-maintained canonical — every
reference in `tools/` + `05_CERTS/` is a READER/validator; no writer/generator exists (see BASELINE).

The packaged row (package §1.2, line 107) was appended EXACTLY as packaged (ledger row 25 / file
line 26; script `scratchpad/fable_batch3a_attempt.py`) and the assumption-ledger guards run.
**THREE REAL REDS, empirically captured:**
1. `05_CERTS/vp_assumption_ledger_green.py` → AssertionError
   `"ASSUMP-CLASS-RECORD-IS-ADDRESSABLE: bad type 'D0_INTERNAL_TYPING_TARGET'"` — the new coinage is
   NOT in the frozen type taxonomy (EXTERNAL_TYPES ∪ INTERNAL_TYPES).
2. `09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py` (default = bridge+ledger mode) → FAIL,
   same bad-type rejection (taxonomy duplicated at `ALLOWED_TYPES | INTERNAL_TARGET_TYPES`).
3. `tools/check_assumption_ledger_ownership.py` → FAIL
   `"owner file does not exist: D0/Bridge/Assumptions/ClassRecordIsAddressable.lean"`.

Variant probe (package §1.1.3's OWN sanctioned conservative fallback `D0_INTERNAL_FORCING_TARGET`)
also tested: reds 1-2 clear (green cert + no-sorry PASS), **red 3 persists** — the ownership guard
requires the `lean_file` to EXIST, and the packaged carrier
`D0/Bridge/Assumptions/ClassRecordIsAddressable.lean` is explicitly "a later F4-wave artifact (NOT
written now)" (package §1.1.4). Writing it is on this pass's HOLD list (Lean lifts = F4); pointing
`lean_file` at any other existing file would fabricate a carrier the package does not sanction.

**BACKED OUT** per discipline: ledger restored from pristine backup, md5 re-verified byte-identical
(`ed320d6004ea03668ce057d6703322a1`); both assumption guards re-run green after restore.

**Unblock path for the owner (either): (i)** land the F4 carrier file (4-line
`ClassRecordIsAddressableAssumption` structure, `KernelChargeLocalization.lean:22-24` pattern) in the
F4 wave, then append the row with the sanctioned fallback type `D0_INTERNAL_FORCING_TARGET` (or
**(ii)** extend the taxonomy with `D0_INTERNAL_TYPING_TARGET` in BOTH validators — a guard edit,
out of scope for this pass) — then apply (a)+(b) together.

### (b) GAP-W row (D0-GAP-W-WITNESS-PLUS-ONE-001) — **HELD (two independent reasons)**

- The status/columns change (`assumption_ids=ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`,
  `uses_bridge_assumptions=True`, OPEN → LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS) is NOT guard-safe per
  the package itself — §1.3: "Upgrade path: once the F4 wave lands the W-REC lift … until then
  lean_status stays OPEN / release_status PROOF-TARGET". F4-gated → HELD as instructed.
- The §1.3 cross-ref NOTE text asserts "promoted to a registered ledger id … LEAN_ASSUMPTION_LEDGER.csv
  line 26" — with (a) held, appending it would put a FALSE registration claim in the registry.
  → note HELD together with (a); apply both atomically once (a) unblocks. Row untouched this pass
  (still OPEN / PROOF-TARGET with its GROUPE[2026-07-06] state).

### (c) F7-INTERFACE notes — **APPLIED**

Both note texts extracted programmatically from package §2.1/§2.2 fenced blocks
(script `scratchpad/fable_batch3c.py`), joined to one line, appended notes-only by claim_id:
- `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` (csv:361): +1389 chars ` F7-INTERFACE[2026-07-06]: …`
  — statuses byte-unchanged (LEAN_PROVED / NO-GO).
- `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001` (csv:517): +1308 chars ` F7-INTERFACE[2026-07-06]: …`
  — statuses byte-unchanged (LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS / BRIDGE-ASSUMPTIONS-EXPLICIT).

Regen: sync 555 → aggregates rewritten. Guard board after (c): ALL GREEN (see below). **KEPT.**

### (d) HYGIENE ITEM — flagged for owner (NO ledger entry invented)

`ASSUMP-NO-EXOTIC-FERMIONS` is NAMED in the notes of `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001`
(csv:517, "Caveat ASSUMP-NO-EXOTIC-FERMIONS (Costa PRD102(2020)115006 …)") but is **NOT a registered
id** in `LEAN_ASSUMPTION_LEDGER.csv` (grep = 0). Unregistered-ASSUMP-id reference. Owner options per
the package: later ledger registration, or an explicit K(9,11,13)-exclusion cross-ref; no new physics
either way. Carried honestly in-note by the applied §2.1/§2.2 texts; NOT invented here.

**Guard board after BATCH 3 — ALL GREEN. KEPT.**
- validate_csv PASS (555) · status-inflation PASS_NO_INFLATION (555, 0/0/0, planted control fires)
- book-ledger-sync PASS · no-sorry-core PASS · coverage PASS · aggregates --check PASS
- assumption-ledger-green PASS (+3 negative controls fire) · ownership PASS
- Row count 555 · ledger 25 lines (24 rows) byte-identical to baseline. `053040` untouched.

---

## HOLD LIST (this pass)

| item | reason |
|---|---|
| BATCH 3(a) ledger row `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE` | guards reject (bad-type × 2 validators + nonexistent F4 carrier file); attempt + back-out evidence above |
| BATCH 3(b) GAP-W cross-ref note + `assumption_ids`/`uses_bridge_assumptions` | F4-gated per package §1.3; note depends on (a) |
| Book edits (F5) | out of scope per task |
| Lean lifts (F4): W-REC lift (`WRecArchitecture.lean` skeleton), `ClassRecordIsAddressable.lean` carrier | out of scope per task |

## FINAL STATE

- **Applied:** BATCH 1 (F1 mint `D0-INVARIANT-GENERATION-BRIDGE-001` + M2/M3 cross-refs),
  BATCH 2 (F2 GAP-E FABLE final note), BATCH 3(c) (two F7-INTERFACE notes), 3(d) hygiene flag logged.
- **Held:** 3(a), 3(b) (evidence + unblock path above); F4/F5 untouched.
- **Exact change list:** `CLAIM_TO_LEAN_MAP.csv` — 1 new row (555th), 5 rows notes-appended
  (`D0-MATTER-REP-001`, `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`,
  `D0-WINDOW-9-13-DISSOLVE-001`, `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`,
  `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001`); zero status/cert/lean-column changes on existing rows.
  Generated files regenerated only via tools (theory_status_map.csv, theory_graph.json, ClaimMap.lean,
  ActiveClosureIndex.lean). `LEAN_ASSUMPTION_LEDGER.csv` byte-identical to baseline.
- Counts: canonical rows 554 → **555**; ledger rows **24** (unchanged).
- `053040`: 0 hits in CSV + ledger (confirmed post-pass). **No git commit made.**
