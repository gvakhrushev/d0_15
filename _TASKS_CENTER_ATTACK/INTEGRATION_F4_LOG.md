# INTEGRATION_F4_LOG — applying the F4 Lean-wave flip-proposals + held R-A ledger row

Date: 2026-07-06. Discipline mirrors `INTEGRATION_FABLE_LOG.md`. Serial, incremental, small tool calls.
Source of flips: `F4_LEAN_WAVE_LOG.md` FINAL section (authoritative) + `F3_HONEST_BRIDGES_PACKAGE.md` §1.2/§1.3
(the BATCH-3(a)/(b) items HELD in the Fable pass, now unblocked by the F4 carrier file).

**Canonical** = `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (hand-edit ONLY this, then regen via
`tools/sync_theory_status_map.py` + `tools/generate_lean_aggregates.py`). **Ledger** =
`09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv`, hand-maintained canonical (writer-absence verified in the
Fable pass; unchanged since — md5 baseline below matches the Fable pristine backup). All row edits by claim_id via
csv.reader (NEVER line numbers). **`053040` NEVER touched. No git commit.**

Pristine backups (byte-identical, md5-verified) in session scratchpad `f4_backups/`:
- `CLAIM_TO_LEAN_MAP.csv` md5 `379c208862ac9b26be04441dbd2cc3b8` (555 canonical rows, post-Fable)
- `LEAN_ASSUMPTION_LEDGER.csv` md5 `ed320d6004ea03668ce057d6703322a1` (24 rows — byte-identical to Fable baseline)

**Guard board** (ALL green after every batch; BACK OUT on any real red):
- `tools/validate_csv.py` PASS (row count)
- `05_CERTS/vp_status_inflation_audit.py` PASS_NO_INFLATION + negative control FAIL_PLANTED fires
- `tools/check_book_ledger_sync.py` PASS · `09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py --core` PASS
- `09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py` PASS · `tools/generate_lean_aggregates.py --check` PASS
- `05_CERTS/vp_assumption_ledger_green.py` PASS (+3 negative controls) · `tools/check_assumption_ledger_ownership.py` PASS

Per-flip Lean pre-verification (HARD RULE): targeted `lake build` of the cited module + `#print axioms` clean
(no sorryAx) BEFORE any CSV flip that cites it.

## Planned batches (from F4 log FINAL flip-proposals; ledger moved FIRST — see BASELINE rationale)

| batch | flip | target row(s) | change class |
|---|---|---|---|
| 1 | FP-6(ledger) | `LEAN_ASSUMPTION_LEDGER.csv` append `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE` (F3 §1.2 row, type→`D0_INTERNAL_FORCING_TARGET`) | ledger 24→25 rows |
| 2 | FP-1 | `D0-INVARIANT-GENERATION-BRIDGE-001` | lean fields + OPEN→LEAN_PROVED (release stays PROOF-TARGET) |
| 3 | FP-2 | `D0-P-INVARIANT-MINIMAL-001` | lean fields + OPEN→LEAN_PROVED + caveat note |
| 4 | FP-3+FP-4 | `D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001`, `D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001` | notes-only + theorem-list appends, no status change |
| 5 | FP-5 | `D0-GAP-W-WITNESS-PLUS-ONE-001` | OPEN→LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS + assumption_ids + §1.3 note (guard-gated) |

---

## BASELINE (before any edit)

- validate_csv: PASS, **555** canonical rows (post-Fable state confirmed)
- status-inflation: **PASS_NO_INFLATION** 555 claims (0/0/0), planted negative control fires
- book-ledger-sync: PASS (0 PROSE-OVERCLAIM / 0 DEMOTED-CLOSURE-PROSE)
- no-sorry-core `--core`: PASS · claim-map-coverage: PASS · aggregates `--check`: PASS (rc=0, idempotent)
- assumption-ledger ownership: PASS_ASSUMPTION_LEDGER_OWNERSHIP (the F4 carrier file EXISTS on disk — the
  Fable-pass red 3 "owner file does not exist" is CLEARED by the F4 wave)
- **ONE expected pre-existing red, exactly as F4_LEAN_WAVE_LOG.md FINAL predicted (handoff by design):**
  `05_CERTS/vp_assumption_ledger_green.py` rc=1 and `check_no_sorry_in_core.py` (default bridge+ledger mode)
  rc=1, identical message `D0/Bridge/Assumptions/ClassRecordIsAddressable.lean: BridgeAssumption structure
  missing from ledger` — the chicken-and-egg the F4 log hands to THIS pass; it goes green the moment the
  ledger row lands. **Rationale for reorder: ledger append promoted to BATCH 1** so every post-batch guard
  board in this pass is fully green (no batch rides on a known red).
- Ledger: 25 lines = header + 24 rows, last = ASSUMP-KERNEL-CHARGE-LOCALIZATION; md5 byte-identical to the
  Fable pristine backup (`ed320d6004ea03668ce057d6703322a1`).
- `053040`: grep = 0 hits in CSV + ledger targets of this pass (never touched).

Target rows resolved by claim_id (grep-confirmed present, 1 hit each): `D0-INVARIANT-GENERATION-BRIDGE-001`
(OPEN/PROOF-TARGET, lean fields empty), `D0-P-INVARIANT-MINIMAL-001` (OPEN/PROOF-TARGET, lean fields empty),
`D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001` (LEAN_PROVED/NO-GO), `D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001`
(LEAN_PROVED/NO-GO), `D0-GAP-W-WITNESS-PLUS-ONE-001` (OPEN/PROOF-TARGET, module D0.Core.WitnessForcing).

---

## LEAN PRE-VERIFICATION (HARD RULE — done BEFORE any flip; all targeted foreground `lake build` green)

- `lake build D0.Bridge.Assumptions.ClassRecordIsAddressable` → green (2 jobs; file EXISTS on disk, 3172 bytes)
- `lake build D0.Claims.InvariantGenerationBridge D0.Foundation.InvariantMinimal` → green (2954 jobs)
- `lake build D0.VNext.AFD0LaplacianComparisonNoGo D0.Extensions.LeptonSelectorExtension D0.Core.WRecArchitecture` → green (2961 jobs)

`#print axioms` (scratch import file via `lake env lean`) — **NO sorryAx anywhere**, matches F4 log exactly:
- `D0.Claims.InvariantGenerationBridge.bridge_projector_eq` / `invariant_generation_bridge`: propext, Classical.choice, Quot.sound + native_decide reduceBool axioms only
- `D0.Foundation.InvariantMinimal.invariant_minimal_meet` / `orbit_count_three` / `deg_classifies_orbits`: same class (native_decide only where used)
- `D0.VNext.AFD0LaplacianComparisonNoGo.af_skips_d0_dim_total` / `laplacian_tower_compatibility_no_go_total`: **propext/Classical.choice/Quot.sound ONLY** (kernel-grade, zero native_decide — as logged)
- `D0.Extensions.LeptonSelectorExtension.numGenerations_eq_trace` (inherits `D0.Dynamics.trace_T2` native_decide) / `numGenerations_eq_zone_count` (own native_decide): clean
- `D0.Core.WRecArchitecture.card_base_forced_wrec`: **propext/Classical.choice/Quot.sound ONLY** (axiom-pure capstone, as logged)

Namespace note for the CSV lean_theorem fields: the declarations live under module-named namespaces
(`D0.Claims.InvariantGenerationBridge.bridge_projector_eq` etc.); CSV convention stores module in `lean_module`
and bare theorem names in `lean_theorem` (precedent: existing rows).

---

## BATCH 1 — R-A LEDGER ROW (F4 FP-6; the Fable BATCH-3(a) HELD item, now unblocked) — APPLIED

Pre-flight (script `f4_batch1_ledger.py`, all asserted in-code):
- Row extracted PROGRAMMATICALLY from `F3_HONEST_BRIDGES_PACKAGE.md` §1.2 fenced block (zero transcription);
  parsed as CSV: 10 fields = ledger header width; id/status(EXPLICIT)/lean_file/claim_id verified.
- The ONE sanctioned correction applied: `assumption_type` `D0_INTERNAL_TYPING_TARGET` → **`D0_INTERNAL_FORCING_TARGET`**
  (F3 §1.1(3) sanctioned fallback; F4 log FP-6 confirms the primary coinage is NOT in the validators' whitelist).
  All other fields verbatim §1.2.
- Ledger pre-state: header + 24 rows, id absent, trailing newline present, no 053040.
- Owner file `D0/Bridge/Assumptions/ClassRecordIsAddressable.lean` EXISTS + built green + carrier-pattern module
  (pre-verification above) — clears the Fable red 3.

Applied: row appended as ledger row 25 (file line 26), QUOTE_MINIMAL/`\n` dialect matching the file; post-assert:
26 lines, last row = the new id with type `D0_INTERNAL_FORCING_TARGET`, all prior rows byte-undisturbed.
Regen: `sync_theory_status_map.py` → Synced 555 · `generate_lean_aggregates.py` → ClaimMap/ActiveClosureIndex rewritten.

**Guard board after BATCH 1 — ALL GREEN (both handoff reds cleared as the F4 log predicted). KEPT.**
- validate_csv PASS (555) · status-inflation PASS_NO_INFLATION (555, 0/0/0, planted control fires)
- book-ledger-sync PASS (0/0) · no-sorry-core `--core` PASS · **no-sorry-core default (bridge+ledger) rc=1→rc=0 PASS**
- coverage PASS · aggregates --check PASS (idempotent)
- **assumption-ledger-green rc=1→rc=0 PASS_ASSUMPTION_LEDGER_GREEN** — PASS_ALL_ROWS_CONFORMANT **25 rows**
  (21 external BridgeAssumptions + 4 internal EXPLICIT forcing targets), + 3 negative controls fire
  (CORE-typed / unknown-type / external-outside-bridge all rejected)
- ownership PASS_ASSUMPTION_LEDGER_OWNERSHIP
- Ledger rows 24 → **25**. CSV rows 555 unchanged. `053040` untouched.

---

## DIALECT INCIDENT (caught + fully backed out before regen/guards; no residue)

First BATCH-2 write used `lineterminator='\n'`; byte-diff vs pristine backup showed the canonical CSV is
**CRLF-terminated** (556 CRLF rows + 3 embedded bare-LF inside quoted notes) — whole file would have been
normalized. **BACKED OUT** immediately: restored from pristine backup, md5 re-verified byte-identical
(`379c208862ac9b26be04441dbd2cc3b8`). Ledger checked too: pure-LF file, so the BATCH-1 append (LF) was
dialect-correct and is a pure byte-suffix of the pristine ledger (verified `startswith(backup)=True`) — stands.
Discipline note for future passes: **canonical CSV = CRLF rows, ledger = LF rows; verify byte-delta vs backup
after every write.**

---

## BATCH 2 — FP-1 BRIDGE ROW `D0-INVARIANT-GENERATION-BRIDGE-001` — APPLIED

Pre-flight (script `f4_batch2_bridge.py`, asserts in-code): resolved by claim_id (1 hit); pre-state asserted
OPEN / PROOF-TARGET / lean fields EMPTY / cert `bridge_invariant_generation_check.py`; no prior `F4-LEAN[2026-07-06]` marker.
Lean pre-verification: module built green + axioms clean (see LEAN PRE-VERIFICATION).

Applied (CRLF dialect, byte-delta verified confined to the target row — 556 CRLF / 3 embedded LF preserved):
- `lean_module` ← `D0.Claims.InvariantGenerationBridge`; `lean_theorem` ← `bridge_projector_eq;invariant_generation_bridge`
  (semicolon convention, 105 precedent rows)
- `lean_status` **OPEN → LEAN_PROVED** (native_decide/ofReduceBool grade — precedent row 549)
- `release_status` **byte-unchanged PROOF-TARGET** per the memo inheritance clause (tied to `D0-P-INVARIANT-MINIMAL-001`)
- notes += ` F4-LEAN[2026-07-06]: …` (+1014 chars: R3b literal-gens anti-circularity, axiom class, no-sorryAx,
  count-3-not-re-derived / Weyl-freedom / gens-generate-Aut-cited caveats carried)

Regen: sync 555 · aggregates rewritten (ActiveClosureIndex).

**Guard board after BATCH 2 — ALL GREEN. KEPT.** validate_csv PASS (555) · status-inflation PASS_NO_INFLATION
(planted control fires) · book-ledger-sync PASS · no-sorry-core --core PASS + default PASS · coverage PASS ·
aggregates --check PASS · assumption-ledger-green PASS · ownership PASS. Rows 555, ledger 25. `053040` untouched.

---

## BATCH 3 — FP-2 `D0-P-INVARIANT-MINIMAL-001` — APPLIED

Pre-flight (script `f4_batch3_invmin.py`): resolved by claim_id (1 hit); pre-state asserted OPEN / PROOF-TARGET /
lean fields EMPTY / cert `raise_selector_minimal_check.py`; no prior F4-LEAN marker. Lean pre-verified (build green,
`invariant_minimal_meet` axioms = propext/choice/Quot.sound + `deg_classifies_orbits` native_decide only; the
abstract `classifier_constant_on_orbits` leg axiom-pure).

Applied (CRLF preserved 556/3; byte-delta confined to the target row):
- `lean_module` ← `D0.Foundation.InvariantMinimal`; `lean_theorem` ← `invariant_minimal_meet;orbit_count_three;deg_classifies_orbits`
- `lean_status` **OPEN → LEAN_PROVED**; `release_status` byte-unchanged PROOF-TARGET
- notes += ` F4-LEAN[2026-07-06]: …` (+1239 chars) carrying the FP-2 REQUIRED caveats: quantification = partition
  classifiers; RR-1 single-witness clause upgraded to a UNIVERSAL over partitions and NOTHING ELSE;
  algebra↔partition equivalence + "gens generate Aut" cited-not-formalized; class-function-universality stays
  EVIDENCE-grade (row-549 scope). This is row-550's EXACT-MISSING item (1).

Regen: sync 555 · aggregates rewritten.

**Guard board after BATCH 3 — ALL GREEN. KEPT.** (same 9-guard board, all PASS; planted controls fire.)
Rows 555, ledger 25. `053040` untouched.

---

## BATCH 4 — FP-3 + FP-4 (row 412 totality + lepton typing) — APPLIED

Pre-flight (script `f4_batch4_notes.py`): both rows resolved by claim_id (1 hit each); pre-states asserted
LEAN_PROVED / NO-GO both; no prior F4-LEAN markers; Lean pre-verified (kernel-grade axioms for the VNext totality
theorems; native_decide-only for the lepton typing theorems; no sorryAx).

Applied (byte-delta = exactly 2 physical lines, statuses asserted byte-unchanged in-script):
- `D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001` (FP-3): `lean_theorem` +=
  `;laplacian_tower_compatibility_no_go_total;af_skips_d0_dim_total` (the FP-3 "may append" taken); notes +=
  ` F4-LEAN[2026-07-06]: …` (+609 chars — N≤3 quantifier CLOSED TOTALLY, dimA_eq_fib=F(2n+3) separator,
  KERNEL-GRADE zero-native_decide, W4 §2a named lift DONE). Status/release byte-unchanged (LEAN_PROVED / NO-GO).
- `D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001` (FP-4): **notes-only** (+510 chars —
  `numGenerations_eq_trace` = tr T² via `D0.Dynamics.trace_T2` + `numGenerations_eq_zone_count` = #zones via
  `D0.Claims.zone31` the owned root; lean_theorem field asserted unchanged per the log's FP-4).
  Status/release byte-unchanged (LEAN_PROVED / NO-GO).

Regen: sync 555 · aggregates rewritten.

**Guard board after BATCH 4 — ALL GREEN. KEPT.** (9/9 PASS; planted controls fire.) Rows 555, ledger 25.
No status inflation possible (notes/theorem-list only). `053040` untouched.

---

## BATCH 5 — FP-5 GAP-W ROW `D0-GAP-W-WITNESS-PLUS-ONE-001` UPGRADE (the Fable BATCH-3(b) HELD item) — APPLIED

Both F3 §1.3 upgrade-path conditions verified met BEFORE the flip:
1. W-REC lift LANDED: `D0.Core.WRecArchitecture` built green; capstone `card_base_forced_wrec` consumes
   `ClassRecordIsAddressableAssumption` explicitly (`h_ra`); axioms propext/Classical.choice/Quot.sound ONLY,
   no sorryAx (pre-verification above); `h_halt` NOT promoted (memo :406 honesty guard intact).
2. Ledger id `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE` REGISTERED (BATCH 1, ledger line 26) — the §1.3 cross-ref
   note's registration claim is now TRUTHFUL (the Fable pass's falsity objection dissolved).

Pre-flight (script `f4_batch5_gapw.py`): row resolved by claim_id; pre-state asserted OPEN / PROOF-TARGET /
`D0.Core.WitnessForcing` / `card_base_forced_conditional` / False / empty; no prior R-A-REGISTERED or
F4-UPGRADE-APPLIED markers. §1.3 note extracted PROGRAMMATICALLY from the F3 fenced block, joined to one line,
with the SAME sanctioned taxonomy correction as the ledger row (`D0_INTERNAL_TYPING_TARGET` →
`D0_INTERNAL_FORCING_TARGET` — keeps the in-registry type claim consistent with the actually-registered row).

Applied (byte-delta = exactly 1 physical line; CRLF 556/3 preserved):
- `lean_status` **OPEN → LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS** (this status requires the Lean module — present)
- `uses_bridge_assumptions` **False → True**; `assumption_ids` ← `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`
- `lean_module` ← `D0.Core.WitnessForcing;D0.Core.WRecArchitecture`; `lean_theorem` ←
  `card_base_forced_conditional;card_base_forced_wrec` (multi-module `;` = 10-row precedent;
  bridge-status precedent row `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001`)
- `release_status` **byte-unchanged PROOF-TARGET** per F3 ("until R-A is owned"; NOT promoted to
  BRIDGE-ASSUMPTIONS-EXPLICIT — conservative, log-sanctioned)
- notes += §1.3 `R-A-REGISTERED[2026-07-06]` cross-ref (+1342 chars, taxonomy-corrected) +
  ` F4-UPGRADE-APPLIED[2026-07-06]` marker (+1142 chars) recording that the upgrade path was TAKEN this pass

Regen: sync 555 · aggregates rewritten.

**Guard board after BATCH 5 — ALL GREEN (status-inflation guard ACCEPTED the flip: PASS_NO_INFLATION 555,
0/0/0, planted control fires). KEPT — no back-out needed.** All 9 guards PASS. Rows 555, ledger 25.

---

## FINAL

### Per-flip verdict table

| FP | target | change | verdict |
|---|---|---|---|
| 6(ledger) | `LEAN_ASSUMPTION_LEDGER.csv` | `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE` appended (F3 §1.2 verbatim, type→`D0_INTERNAL_FORCING_TARGET`); owner file exists+builds | **APPLIED** (BATCH 1) |
| 1 | `D0-INVARIANT-GENERATION-BRIDGE-001` | lean fields + OPEN→LEAN_PROVED; release stays PROOF-TARGET; F4-LEAN note | **APPLIED** (BATCH 2) |
| 2 | `D0-P-INVARIANT-MINIMAL-001` | lean fields + OPEN→LEAN_PROVED; RR-1 universal-∀ + caveats in note | **APPLIED** (BATCH 3) |
| 3 | `D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001` | theorem-list += totality theorems + note; statuses unchanged | **APPLIED** (BATCH 4) |
| 4 | `D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001` | notes-only numGenerations typing; statuses unchanged | **APPLIED** (BATCH 4) |
| 5 | `D0-GAP-W-WITNESS-PLUS-ONE-001` | OPEN→LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS + assumption wiring + §1.3 note; release stays PROOF-TARGET | **APPLIED** (BATCH 5, guard-green) |

Nothing HELD. The Fable pass's two HELD items (3(a)/3(b)) are both discharged; its documented unblock path (i)
was exactly the route taken (F4 carrier landed → fallback-typed ledger row → atomic note+flip).

### Final state

- Canonical rows: **555** (unchanged — no mints this pass; the 555th row was minted in the Fable pass).
  Ledger rows: **24 → 25** (last = `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`, `D0_INTERNAL_FORCING_TARGET`, EXPLICIT).
- Exact change list: `CLAIM_TO_LEAN_MAP.csv` — 5 rows edited by claim_id (2 lean-lift status flips, 1
  bridge-assumption upgrade, 2 note/theorem-list-only); `LEAN_ASSUMPTION_LEDGER.csv` — 1 row appended;
  generated files regenerated ONLY via tools (theory_status_map.csv, theory_graph.json, ClaimMap.lean,
  ActiveClosureIndex.lean). Byte-delta verified per batch (CRLF 556 / embedded-LF 3 invariant throughout).
- Final guard board: 9/9 GREEN (validate_csv 555 · PASS_NO_INFLATION + planted control · book-ledger-sync ·
  no-sorry-core --core AND default · coverage · aggregates idempotent · PASS_ASSUMPTION_LEDGER_GREEN 25 rows
  conformant + 3 negative controls · PASS_ASSUMPTION_LEDGER_OWNERSHIP). Extra: `check_no_dangling_lean_module.py`
  PASS (0 new dangling).
- **`053040`: 0 hits in CSV + ledger (confirmed post-pass; never touched). No git commit made.**
- Incident record: one dialect near-miss (LF normalization) caught by byte-diff and fully backed out to
  pristine md5 before any regen/guard ran — see DIALECT INCIDENT section; discipline note minted for future passes.
