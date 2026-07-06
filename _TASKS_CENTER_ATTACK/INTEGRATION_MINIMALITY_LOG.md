# INTEGRATION_MINIMALITY_LOG — applying the MINIMALITY-RAISE campaign to the canonical corpus

Date: 2026-07-06. Discipline mirrors `INTEGRATION_GROUPE_LOG.md` + `INTEGRATION_CLOSING_LOG.md`
+ `STATUS_RAISE_LOG.md`. Serial, incremental, small tool calls.

**Canonical** = `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (hand-edit ONLY this file, then
regen via `tools/sync_theory_status_map.py` + `tools/generate_lean_aggregates.py`; generated files
NEVER hand-edited). **`053040` NEVER touched. No git commit.**

Pristine backup: `scratchpad/CLAIM_TO_LEAN_MAP.csv.BEFORE-MINIMALITY` (created first).

**Guard board** (must ALL stay green after every batch; BACK OUT on any real red):
- `tools/validate_csv.py` → PASS (row count)
- `05_CERTS/vp_status_inflation_audit.py` → PASS_NO_INFLATION (0/0/0) + negative control FAIL_PLANTED fires
- `tools/check_book_ledger_sync.py` → PASS (0 PROSE-OVERCLAIM, 0 DEMOTED-CLOSURE-PROSE)
- `09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py --core` → PASS
- `09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py` → PASS
- `tools/generate_lean_aggregates.py --check` → PASS (idempotent)

## BASELINE (before any edit) — ALL GREEN
- validate_csv: PASS, **550** canonical rows
- status-inflation: **PASS_NO_INFLATION** 550 claims (0/0/0), negative control FAIL_PLANTED fires
- book-ledger-sync: PASS (0/0)
- no-sorry-core: PASS
- claim-map-coverage: PASS
- aggregates --check: PASS (idempotent)

Cert scripts for BATCH 2 verified run-clean (precedent: mint certs live in `_TASKS_CENTER_ATTACK/`,
cited as bare filenames — same as `gap_w_witness_check.py`, `m2_phase_labeling_check.py`,
`torsor_gauge_check.py` already in the registry green):
- `_TASKS_CENTER_ATTACK/raise_selector_minimal_check.py` → rc=0 (21/21)
- `_TASKS_CENTER_ATTACK/raise_m1core_check.py` → rc=0 (26/26)

---

## BATCH 1 — RAISE NOTES (notes-only, statuses byte-unchanged; prefix `RAISE[2026-07-06]:`)

9 rows resolved by claim_id (grep-confirmed exact id + line, none already carrying `RAISE[`):

| row | claim_id | positive face appended |
|----:|----------|------------------------|
| 549 | D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 | P-INVARIANT-MINIMAL |
| 528 | D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001 | RIGIDITY-EXTREMALITY |
| 403 | D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001 | SUBCRITICAL-EXTREMALITY |
| 460 | D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001 | MAXIMAL-COMMUTANT |
| 407 | D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001 | MAXIMAL-ABELIAN (W1) |
| 395 | D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001 | HOMOGENEITY-MINIMALITY |
| 350 | D0-ISING-ANYON-EXCLUSION-001 | TWO-BRANCH-MINIMALITY |
| 516 | D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001 | UNIQUE-PARTITION-EXTREMALITY |
| 546 | D0-WINDOW-9-13-DISSOLVE-001 | GAP-E factorization {2,4}+X3-non-factor THEOREMS |

**APPLIED.** All 9 notes verified attached to the correct claim_id (by csv.reader, not line#,
because embedded newlines in other rows make line# != row#). All 8 no-go rows keep their status
(NO-GO); GAP-E stays OPEN/PROOF-TARGET. Statuses byte-unchanged.

**Regen + guard board after BATCH 1 (all green):** sync 550 -> aggregates rewritten (All.lean +
ClaimMap.lean + ActiveClosureIndex.lean) -> validate_csv PASS (550) -> status-inflation
**PASS_NO_INFLATION** (550, 0/0/0, negative control FAIL_PLANTED fires) -> book-ledger-sync PASS
-> no-sorry-core PASS -> coverage PASS -> aggregates --check PASS (idempotent). **KEPT.**
Row count unchanged at 550. `053040` untouched.

---

## BATCH 2 — MINT 4 PRINCIPLE ROWS (POSITIVE extremality theorems, PROOF-TARGET/OPEN)

Pre-flight grep: all 4 names have **0** pre-existing claim_id rows (loose hits = only the
BATCH-1 note references I just added). Clear to mint.

Format matched to recent PROOF-TARGET cert-bearing mints (D0-DUSTY-PLASMA-001,
D0-PASSPORT-ICECUBE-HESE-001): `claim_id, book, section, "", "", OPEN, False, "", raise_*.py,
PROOF-TARGET, notes`. lean_module + lean_theorem EMPTY, lean_status=OPEN, release=PROOF-TARGET
(NOT LEAN_PROVED/CERT-CLOSED — no Lean module yet, owner-gated). Cert = bare filename per the
precedent (mint certs live in `_TASKS_CENTER_ATTACK/`, same as gap_w_witness_check.py etc.).
Each memo's residual-risk (RR) notes carried into the mint row.

Minted (appended textually; existing rows byte-for-byte unchanged, verified by prefix-diff):
| claim_id | python_cert | RR carried |
|----------|-------------|------------|
| D0-P-INVARIANT-MINIMAL-001 | raise_selector_minimal_check.py | RR-1 single-witness refinement, RR-2 EVIDENCE-grade universality |
| D0-P-M1-SATURATION-001 | raise_m1core_check.py | rows stay NO-GO; COLOUR-not-derived; HIGGS W1-only |
| D0-P-SUBCRIT-001 | raise_m1core_check.py | rate monotone/quantified, no chosen-tower smuggle |
| D0-P-ABELIAN-001 | raise_m1core_check.py | W2 external, Qnc necessary-but-not-sufficient, T-specific |

**Regen + guard board after BATCH 2 (all green):** sync 554 -> aggregates rewritten ->
validate_csv PASS (554) -> status-inflation **PASS_NO_INFLATION** (554, 0/0/0, negative control
FAIL_PLANTED fires — the 4 PROOF-TARGET positives own a cert, are NOT closed-without-owner) ->
book-ledger-sync PASS -> no-sorry-core PASS -> coverage PASS -> aggregates --check PASS
(idempotent). **KEPT.** Row count now **554** (550 baseline + 4 mints). `053040` untouched.

---

## BATCH 3 — CORROLLARY-OF TAGS on the 22 P-GAUGE-M1 T3 torsor rows

Roster resolved to exact claim_ids from UPLIFT_MAP.md:295 (T3 = 22 members) cross-checked against
the per-row T3 table (lines 94-190 legend for the coded abbreviations R4/E3/G2/P1-C/P1-EOS/H3/
MARTINGALE-DIRAC/VNEXT2-trio). All 22 mapped 1:1, all present in CSV, none pre-tagged.

Appended (notes-only, no status change): ` RAISE[2026-07-06]: corollary-of D0-P-INVARIANT-MINIMAL-001
(one free Aut-orbit of the extremal-minimal observable algebra)`.

The 22 claim_ids (abbrev -> id):
- CMB-CANONICAL -> D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001
- PHASON-MAGNITUDE -> D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001
- CKM-OVERLAP -> D0-CKM-OVERLAP-UNDERDETERMINATION-NOGO-001
- TORAL-SEED -> D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001
- LEPTON-PUISEUX -> D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001
- R4 -> D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001
- E3 -> D0-POSTCORE-PHASON-EXTENSION-MAXIMALITY-NOGO-001
- MARTINGALE-DIRAC -> D0-VNEXT-MARTINGALE-DIRAC-OWNER-001
- VNEXT2-REFINEMENT-OWNER -> D0-VNEXT2-SCENE-NATIVE-REFINEMENT-OWNER-001
- VNEXT2-REFINEMENT-NOGO -> D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001
- VNEXT2-DIRAC-COVARIANCE -> D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001
- EDGE-COVER -> D0-EDGE-COVER-FAMILY-001
- HYPERCHARGE-VARIETY -> D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001
- G2 -> D0-GRADING-NEUTRAL-CURRENT-MAXIMALITY-NOGO-001
- P1-C -> D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001
- WZ-TRANSFER -> D0-PHASON-WZ-TRANSFER-OWNER-001
- ALPHA-RESIDUE-DELTA -> D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001
- BRANCH-CP -> D0-BRANCH-CP-READOUT-NOGO-V15
- P1-EOS -> D0-P1-PHYSICAL-EOS
- BRANCH-ROW -> D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001 (also carries its BATCH-1 UNIQUE-PARTITION note)
- ARCHIVE-LAPLACIAN-PHASE -> D0-ARCHIVE-LAPLACIAN-PHASE-NATURALITY
- H3 -> D0-SCENE-HISTORY-REFINEMENT-RULE-OWNER-001

Semantic diff vs pre-batch3 snapshot: **exactly 22 rows changed**, each ONLY by the appended tag
(cols 0-9 byte-identical); 0 rows added/dropped; the whole-file csv rewrite left every other row
semantically identical.

**Regen + guard board after BATCH 3 (all green):** sync 554 -> aggregates rewritten -> validate_csv
PASS (554) -> status-inflation **PASS_NO_INFLATION** (554, 0/0/0, negative control fires) ->
book-ledger-sync PASS -> no-sorry-core PASS -> coverage PASS -> aggregates --check PASS
(idempotent). **KEPT.**

---

## HOLD (owner-gated, not executed — logged per task)
- GAP-E domain-sentence postulation (the one unowned ambient quantifier `AdmExt(X) <=> X direct-factor of P`).
- Lean lifts of the 4 principles (row-550 Fin-33 orbit-minimality lemma + cert promotion via
  VERIFIED_CLOSURE_PROTOCOL); the 4 mints stay PROOF-TARGET/OPEN, python-cert-owned.
- Any NO-GO -> CLOSED status flips: the raises are the POSITIVE SHADOWS; all 8 no-gos KEEP their status.
- Book edits: none made.

## FINAL TALLY
- BATCH 1: 9 RAISE notes applied (8 no-go rows status-unchanged + GAP-E OPEN unchanged). Board green. KEPT.
- BATCH 2: 4 principle rows minted PROOF-TARGET/OPEN. Board green (status-inflation PASS). KEPT.
- BATCH 3: 22 corollary-of tags applied (notes-only). Board green. KEPT.
- Final row count: **554** (550 baseline + 4 principle mints). No back-outs.
- `053040` untouched (confirmed: no file in the 053040 namespace modified). No git commit.
- Files touched: canonical CSV (hand-edit) + its generated derivatives (03_THEORY_MAP/*, D0/All.lean,
  ClaimMap.lean, ActiveClosureIndex.lean, LEAN_CORE_THEOREM_INDEX.md — regen only) + this log.


