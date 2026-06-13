# D0 v14 Integration Log

Append-only journal of the whole-repo refactor + scoring + Lean-integration work.
Plan: `C:\Users\kmeze\.claude\plans\sharded-humming-stallman.md`.
Canonical registry: `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (generated:
`03_THEORY_MAP/theory_status_map.csv`, `theory_graph.*`, index markdowns).

---

## Phase 0 — git snapshot + guards

- `git init` + initial commit `base-v14` (1144 files; the four over-ignored
  `05_CERTS/*.json` schema/locked-param files force-added). base-v14 is the
  revert point for all deletes and the `--base` for `check_firewall`.
- Fixed `tools/sync_theory_status_map.py`: `modules_exist()` splits
  semicolon/comma-joined `lean_module` lists before existence checks (the 8
  multi-module LEAN_PROVED rows now resolve True); `cert_path()` strips a leading
  `05_CERTS/` (double-prefix false-negatives). Verified: 8 multi-module rows OK,
  0 missing certs, 0 LEAN_PROVED rows with an absent module.
- New shared status model `tools/d0_status_model.py`: canonical 12 `release_status`
  enum + collapse map, Lean `D0Status` firewall mapping + `canPromoteTo`, and the
  track-fair scoring ladder (spine 1/2/4/7/12/20; track ceilings 20/12/11/7/2/0).
- New guards: `tools/validate_csv.py` (schema/enum/artifacts/FK/staleness),
  `tools/check_firewall.py` (anti-promotion vs base-v14), `tools/regen_graph.ps1`
  (regenerate + delta sanity + `--check-only` idempotence).
- New `00_ROADMAP/INTEGRATION_LOG.md` (this file).

Known worklist surfaced by `validate_csv.py` (handled in Phase 3): ~30 non-canonical
`release_status` values to collapse; `D0-PUB-001` is PYTHON_CERTIFIED with an empty
`python_cert`; generated `theory_status_map.csv` (156) / graph (139) are stale vs
canonical (164) — regenerated in Phase 4.

---

## Phase 1 — activate ignores

- `.gitignore`: added `05_CERTS/outputs/`; untracked the two leaked output files.
- Force-added 4 source `NO_GO_*.md` docs (companions to real no-go theorems) that
  the over-broad `NO_GO_*.md` ignore pattern wrongly excluded.

## Phase 2 — quarantine v17, dedup, surgical delete

- Quarantined `add/v17 books` -> `_QUARANTINE/v17_overshoots/` + `QUARANTINE_LEDGER.md`
  (3 overshoots documented; harvested + deleted in Phase 8E).
- Deleted `99_PRESERVED_SOURCE/` entirely (legacy GOLDEN copy + v13 raw; git-preserved).
- `06_AUDIT/`: deleted ~33 stale v15/v16/cvft changelogs; **kept** the active audit
  set (`standard_language_audit.csv/.md`, `standard_language_progress.json`,
  `glossary_consistency_pass.md`, `internal_sync_*.md`) — consumed by
  `audit_standard_language_terms.py`, `check_standard_language_audit_budget.py`,
  `check_glossary_consistency.py`.
- Relocated `D0_LEAN_FULL_TRANSLATION_TZ_20260528/` ->
  `09_LEAN_FORMALIZATION/docs/LEAN_TRANSLATION_TZ/` (live integration scaffolding,
  not stale — kept with the Lean docs it serves).
- Deleted `03_THEORY_MAP/BOOK_SECTION_MAP_RAW.txt` (the generated `.md` is canonical).
- CI promotion deferred to Phase 7 (the GOLDEN `certs.yml` targets add/d0-main paths).
- Regenerated `D0_CANONICAL_FILE_MAP.csv` (888 rows); 0 references to deleted dirs.
- Verified: `validate_csv` artifact failures unchanged (still only D0-PUB-001);
  no canonical module/cert path resolved into a deleted/moved dir.
- Deferred: prose references to deleted/moved paths in books/README/roadmap
  (stale links, non-breaking) -> swept in Phase 5.

## Phase 3 — reconcile canonical registry

- Collapsed 26 drifted `release_status` values -> canonical 12 via
  `d0_status_model.RELEASE_STATUS_COLLAPSE` (provenance preserved as `[was:X]` in
  notes). Fixed `D0-PUB-001` (was PYTHON_CERTIFIED + empty cert) -> OPEN / PROOF-TARGET.
- 27 rows changed (clean 1-line-per-row diff). All 164 rows now canonical.
- `validate_csv.py` PASS (exit 0; only non-fatal staleness warnings remain);
  `check_firewall.py` PASS. Distribution: CORE-FORMALIZED 89, CERT-CLOSED 30,
  PROOF-TARGET 14, NO_GO_PROVED 8, NO-GO 7, BRIDGE-ASSUMPTIONS-EXPLICIT 7,
  CORE_BRIDGE_SPLIT 4, BRIDGE-CALIBRATION 2, EMPIRICAL-PASSPORT 1,
  EXTERNAL-BACKGROUND 1, DEPRECATED 1.

## Phase 4 — regenerate view + graph

- Ran `sync_theory_status_map.py`: regenerated `theory_status_map.csv`,
  `theory_graph.{json,dot,html}`, `theory_semantic_index.md`,
  `LEAN_CORE_THEOREM_INDEX.md` from the canonical CSV.
- Drift resolved: graph claims = generated csv rows = canonical rows = **164**
  (was 139 / 156 / 164). `validate_csv.py` PASS with zero staleness warnings.
- `regen_graph.ps1 --check-only` PASS (idempotent, 164=164).

## Phase 5 — prose<->registry phantom-cert sync

- New guard `tools/check_book_cert_references.py`: flags `vp_*.py` cited in books
  that are absent on disk and not a declared OPEN/PROOF-TARGET row.
- Remediated 6 phantom citations (the backed claims are Lean-owned or unregistered,
  so no demotion needed): in BOOK_00 §00.8 and BOOK_01 §01.13 coverage tables,
  replaced phantom cert filenames with `(see canonical registry)`; dropped the
  phantom `vp_calibration_dag_lambda_section_*` (kept the real
  `vp_c_time_length_single_section_closure.py`); BOOK_02 §02.27 corrected the
  mis-numbered ward cert `vp_v1134_...` -> the real `vp_v1132_gauge_matter_ward_anomaly.py`.
- `check_book_cert_references.py` PASS.

## Phase 6 — scoring tree (`tools/d0_score.py`)

- Track-fair scorer reading the canonical CSV + on-disk artifacts; outputs
  `03_THEORY_MAP/SCOREBOARD.md` + `scoreboard.json`. Anti-gaming: verified level =
  min(declared, disk-supported); bridge/passport/external capped by the firewall;
  deprecated excluded.
- **Baseline strength: 2335 / 2992 = 78.0%**; core spine 2013 / 2660 (headroom
  **647** to take every core claim to L5); 163 active claims; 0 integrity demotions.
- "Where to gain points next" surfaces the Lean-closure worklist: **25
  PYTHON_CERTIFIED claims** each +5 to write the Lean proof (D0-IM-*, D0-ARCHIVE-*,
  D0-GRAV-004/005/006, D0-EDGE-*, D0-BARYON-POLES-001, D0-IM-COSMO-*, ...). Biggest
  per-domain headroom: frontier 247, formal_core 234; per-book: BOOK_07 135, BOOK_04 111.
- `d0_score.py --strict` exit 0.

## Phase 7 — CI wiring

- Authored `.github/workflows/guards.yml` (ubuntu): validate_csv -> check_firewall
  (--base base-v14) -> check_no_sorry_in_core -> check_claim_map_coverage ->
  check_physical_bridge_discipline -> check_book_cert_references ->
  regen_graph.ps1 -CheckOnly (pwsh) -> d0_score.py --strict. `lake build` stays in a
  deferred/manual workflow.
- Fixed two pre-existing guard failures (both honestly, not by suppression):
  - `check_claim_map_coverage.py`: module requirement now keyed off `lean_status`
    (only LEAN_PROVED* needs a Lean module), not the stale pre-collapse
    `release_status` list -> resolves D0-CVFT-F3/F3B (now CERT-CLOSED, cert-level).
  - The two orphan `sorry` witnesses (`FiniteBianchiEinsteinTensor.lean`,
    `BlackHoleA4EntropyWitness.lean`) -> relocated out of `D0/` to
    `09_LEAN_FORMALIZATION/_OPEN_WITNESSES/` (nothing imports them, no claim
    references them) so the core tree is genuinely sorry-free under `--all`.
    Tracked as gravity-sector open obligations for Phase 8.
- Froze `00_PUBLICATION/` (`_FROZEN.md`). Fixed README guard paths + added the
  guard/scoreboard suite to getting-started. Regenerated `D0_CANONICAL_FILE_MAP.csv`.
- **Full local CI dry-run green: all 7 python guards + regen_graph -CheckOnly PASS.**

## Phase 8A — integrate first forced claims (cert level)

Note on scope: per `LEAN_DEFERRED_RUN_POLICY.md` the Lean toolchain is deferred
(`.lake` not materialized), so this session integrates **certs** (verifiable here)
-> claims reach PYTHON_CERTIFIED (L3). The Lean proofs (L3->L4) are the deferred
queue the scoreboard now tracks under "where to gain points next".

Integrated 4 forced claims end-to-end (registry row -> cert PASS -> validate ->
regen -> score), each exact (no floats), each able to FAIL:
- `D0-XI5-TORUS-DEFECT-001` -> `vp_xi5_torus_defect.py` (phi^5=11+phi^-5; Tr(T^5)=-11; Z[phi]).
- `D0-VIETA-GALOIS-ABCD-001` -> `vp_vieta_galois_abcd.py` (ABCD=Vieta=Galois of x^2-x-1; delta0 forced).
- `D0-KERNEL-ZONE-SPLIT-001` -> `vp_kernel_zone_split.py` (ker K(9,11,13)=30=8+10+12; rank 3).
- `D0-DIM-LADDER-COMPACT-001` -> `vp_dim_ladder_compact.py` (Q(D)=phi^(D-4); quantum=1 at D=4).

Registry 164 -> **168 rows**; all guards PASS. Strength **2335 -> 2363** (realized
+28); core headroom **647 -> 699** (the new claims add 13 points of Lean-proof
potential each). The four appear in SCOREBOARD "cheapest promotions" as +5 write-Lean-proof targets.

## Phase 8B — cert-execution guard

- `tools/run_registered_certs.py`: runs every registered cert, requires exit 0 + PASS
  (SKIP-aware for data-gated passports; forces UTF-8 in children). Wired into CI.
- First run found + fixed a cp1251 crash (`vp_phason_flip_entropy_sde.py`, via UTF-8
  env) and a data-gated passport (`vp_qnm_*` -> SKIP). 66 certs -> 64 PASS, 2 SKIP, 0 FAIL.
  **PYTHON_CERTIFIED now means the cert actually passes**, not just exists.

## Phase 8C — curated orphan harvest

- 143 orphan certs (on disk, unregistered); ran all -> 97 PASS. A classification agent
  curated 44 registrations (9 LINK + 35 NEW) and 53 SKIP (aliases, wrappers,
  sub-components, versioned execution cells). Applied 6 LINK + 36 NEW (D0-METRO-002 was
  NEW not LINK; CVFT-F2/F6 kept PROOF-TARGET as supporting-evidence, F4/F7 -> CERT-CLOSED).
- Fixed `cert_path` to fall back to a recursive basename lookup (cached) so ported
  `05_CERTS/ported_legacy_primary/<ID>/` certs resolve in validate/score, not just the runner.
- Registry **168 -> 204 rows**; `run_registered_certs` 110 certs -> 108 PASS / 2 SKIP / 0 FAIL;
  all guards green. Strength **2363 -> 2625** (+262 realized); core headroom **699 -> 1027**.
  Passports + the LIGO negative-control registered as EMPIRICAL-PASSPORT/NO-GO (firewall-blocked).

## Phase 8D — Tier-1 forced-claim certs

Five new deterministic certs (exact, no floats, each able to FAIL), registered CERT-CLOSED:
- `D0-Q8-DEDEKIND-MINIMALITY-001` (`vp_q8_dedekind_minimality.py`) — Omega8=Q8 forced:
  group enumeration shows Q8 has 0 non-normal subgroups vs S3=3, D4=4; triple identity
  [Q8,Q8]=Z=Phi={+-1}. (Cert caught my wrong D4=2 expectation -> correct 4.)
- `D0-WINDOW44-GROUP-SPECTRUM-001` ((Z/44)*=Z2xZ2xZ5, |.|=20=d13, char subgroups {1,4,5,20}, 20=4x5).
- `D0-TIME-2D-PISOT-001` (phi Pisot => deg Q(phi)=2 => time = T^2).
- `D0-MIXING-HIERARCHY-INVERSION-001` (rank-3 nondegenerate vs nullity-30 degenerate; the
  nonzero-spectrum cubic is exactly lambda^3-359 lambda-2574 = the vacuum cubic, 359=|E|, 2574=2*1287).
- `D0-SIGNATURE-31-SPLIT-001` (3=rank(adj) space + 1 Pisot modular-flow time; distinct objects).

Registry 204 -> 209; all guards green. Strength **2625 -> 2660**; core headroom **1027 -> 1092**.

## R — Lean architecture refactor (parallel per-claim formalization)

Goal: stop one Lean edit forcing a ~20-min rebuild; let agents close proofs in parallel.

- **R1 (lean_dev.ps1):** fixed the PowerShell native-stderr trap (`$ErrorActionPreference=Stop`
  was aborting builds on lake's `info:` progress lines — now `Continue`, rely on `$LASTEXITCODE`);
  added one-time auto `lake exe cache get` so mathlib is downloaded oleans, not recompiled.
- **R2 (generated aggregators):** `tools/generate_lean_aggregates.py` regenerates `All.lean`,
  `ClaimMap.lean`, `ActiveClosureIndex.lean` deterministically from the canonical CSV — killing
  the two hand-edited merge points. **Idempotence proven** (regenerate twice = byte-identical),
  which is the property that lets N agents append a CSV row / add a `D0/Claims/<id>.lean` without
  index merge conflicts. Committed the regenerated `ClaimMap.lean` (the *critical* merge point;
  it had drifted — 81 hand-edited entries vs 154 CSV claims-with-a-module — generation makes it
  complete + consistent) and `ActiveClosureIndex.lean`. CI wired with `--check`.
  `claim_map_coverage` + `primitive_text_sync` + full guard suite PASS on the regenerated ledger.

**Environment block (honest):** the Lean **build** could not be warmed this session — github
access was flaky (lake timed out fetching `aesop`), then mathlib built **from source** (no olean
cache) which is the ~1-hr path. So **All.lean regeneration is held** (reverted to the known-good
hand-edited file) until a warm build validates the glob-all import set, and the **R4 parallel
proof wave is deferred** (it needs the warm `.lake`). To warm it: run `tools/lean_dev.ps1 build
D0.Core.Phi` on a networked machine (one-time), then per-claim builds are seconds.

### Phase 8 backlog (tracked, scoreboard-visible)

Remaining forced-claim certs to write (then Lean L4): Q8-Dedekind minimality,
window-44 group spectrum, icosian->E8 carrier (exact Z[sqrt5] Gram/Mordell; +Leech
BRIDGE), toral time operator + h_KS=log phi, mixing-hierarchy-inversion, time-2D-Pisot,
signature-3+1-split, Z2-registry (seven incarnations). Typed bridges/passports
(firewall-blocked from core): CKM Wolfenstein quad (out-of-sample gamma falsifier),
PMNS delta0-family (JUNO), m_s/m_d=20 Cabibbo, vacuum-cubic-window; passport manifests
E8_QUANTUM_CRITICAL / NUFIT_PMNS / H0_EVOLVING_W; D0-ARCHIVE-NOT-STERILE-NU-001 (no-go).
Lean L3->L4 for all 25 existing PYTHON_CERTIFIED claims (the +5 worklist). Harvest v17
legitimate reach then delete `_QUARANTINE/v17_overshoots/` (8E). The two `_OPEN_WITNESSES`
sorry files are gravity-sector L4 obligations.

---

## BR0 — GOLDEN→v14 coverage audit (chunk-by-chunk; the "nothing-missed" gate)

Root cause the books refactor must fix: much of GOLDEN's *forcing engine* was silently dropped
from v14 (M1 itself among it) — v14 keeps downstream *facts* but not the *why*. A structure-first
refactor would re-lose it, so coverage comes FIRST, by code, with an explicit verdict per chunk.

- **`tools/chunk_sources.py`** (deterministic): splits the three co-primary source layers —
  GOLDEN `add/d0-main/books/BOOK_I..VI`, v17 `_QUARANTINE/v17_overshoots/01_BOOKS/` (more
  idea-rich), transfer docs `add/files/` — into **1029 chunks / 47 uniform ~18 KB batches**,
  one chunk per `[DEF/THE/LEM/COR/BRIDGE]` formal statement (~335) + heading span. Idempotent;
  scratch under `03_THEORY_MAP/coverage_audit/` (gitignored).
- **Audit Workflow** (`br0-coverage-audit`, 68 agents): 47 audit agents (one per batch, each
  greps the v14 books to judge present/partial/absent) → barrier → 21 per-source-book
  **completeness critics** that re-check `already-present` (weaker restatement? the M1 failure
  mode) and `skip` (dropped value?). 4.6M subagent tokens, ~51 min.
- **`tools/build_coverage_ledger.py`** (deterministic): aggregates the agent row files against
  the chunk manifest and **FAILS if any chunk lacks a verdict** (the nothing-missed guarantee is
  a checkable property, not a hope). Output: canonical `03_THEORY_MAP/GOLDEN_COVERAGE_LEDGER.csv`
  (1 row/chunk) + `.md` view (integrate worklist, core-forcing first; partial/weaker table).

**Result (every chunk has a verdict; exit 0):** 1029 rows = **562 integrate** (198 core-forcing),
338 skip, 129 already-present. present_in_v14: **289 absent · 285 partial/weaker (M1 failure
mode) · 132 fully present**. Integrate by source: golden 410, transfer 78, v17 74 (v17+transfer
surfaced 152 real items beyond GOLDEN — co-primary call paid off). Core-forcing integrate by
target book: BOOK_02 39, BOOK_04 37, BOOK_06 29, BOOK_01 27, BOOK_00 20, BOOK_03 18, BOOK_07 16,
BOOK_05 9, BOOK_08 3 (the BR3/BR4 distribution). All **3 v17 overshoots quarantined** (22 skips
naming Immutable/Grand-Singularity-Lock, Golod–Shafarevich 1/160, fabricated OpenAI-2026). Critic
applied **12 revisions** (caught both failure modes: weaker-restatement mislabeled already-present;
real concepts over-skipped). Headline drops confirmed: M1 (THE 0.4.1) + DEF-0.2.2 forcing schema +
M1+ canonization machinery absent/partial; the topological forcing chain (distinguishable-return
memory → two loops → torus → defect-necessity → shell+φ → step+2) kept as *results* in v14, not as
*forcing arguments*. This ledger's `integrate` rows are the exact BR3 worklist.

---

## BR1 — per-section book infrastructure (split + assemble + guard)

Mirror the Lean refactor for the books: per-section files = source, the monolithic book
= a generated view. So agents rewrite one section with zero merge conflict (same property
as per-claim Lean modules), and the book never drifts from its sections.

- **`tools/split_books.py`** (idempotent): byte-lossless split of each `01_BOOKS/BOOK_0X_*.md`
  on `## ` (level-2) boundaries into `01_BOOKS/<book>/<seq>__<sectionid>__<slug>.md` —
  **10 books → 341 section files**. Self-checks losslessness (concat == original) and refuses
  to write a lossy split.
- **`tools/assemble_books.py`** (`--check`): regenerates `BOOK_0X.md` = deterministic banner +
  section files in document order. Verified lossless: every book diffs **exactly `+1 -0`** vs
  pre-split (only the `<!-- AUTO-ASSEMBLED … -->` banner; all prose byte-identical). Status-table
  injection deliberately deferred until a normalized `book_section` column exists (keeps the
  round-trip verifiable through BR2/BR3).
- **`tools/check_book_assembly.py`** (CI guard, wired into `guards.yml`): fails if any book is
  stale vs its sections (idempotence), on orphan book/dir, or on malformed/non-contiguous section
  filenames. PASS: 10 books, 341 sections, all idempotent.

Full Python guard suite stays green; `d0_score` strength unchanged at **2660/3767 (70.6%)**
(pure restructure, no claim-status change). The 341 section files are the BR4 parallel-rewrite
unit; BR2 (dedup/ordering/stale) and BR3 (integrate the BR0 forcing rows) operate on them next.

---

## BR2 — book token firewall (preventive)

`tools/check_book_tokens.py` (CI): **fails** on the v17 overshoots + deprecated δ0 form
(Immutable / Grand-Singularity-Lock, Golod-Shafarevich, OpenAI-2026, δ0=φ⁻³ — all 0 now,
so the firewall stays green while BR3 pulls content from v17 where those live); **reports**
51 stale tokens (dangling `(marker moved to 06_AUDIT/…)` refs to the deleted dir + `v16
publication-proofread` boilerplate) as the rewrite-wave cleanup worklist. ("atlas" was checked
and KEPT — it is the real `D0_HIGH_GAIN_HOSTILE_UNIQUENESS_ATLAS.md`, not cruft.)

## BR3 — forcing integration, per-book waves (BOOK_02 done)

Infra: `tools/group_coverage_by_section.py` turns the BR0 ledger's `integrate` rows into a
per-book worklist — each row routed to an existing section file and enriched with its GOLDEN/v17
**source path + line range** so a rewrite agent reads the *actual* forcing argument. Worklists
pre-generated for all 10 books (core-forcing counts: 02→39, 04→37, 06→29, 01→27, 00→20, 03→18,
07→16, 05→9, 08→3 ≈ 198).

**BOOK_02 wave** (`br3-book-wave`, 15 agents): planner routed all 39 core-forcing rows to 14
existing sections (the 8 "complexity" conceptual rows grouped into 02.10); 14 section workers
integrated **39/39** forcing arguments in place (+984/−6 lines). Highlights: the **second
independent φ-forcing** (S1 self-similarity `r²−r−1=0`, derivationally distinct from Route-1
`p+p²=1`), M1 test-extensionality + no-math-without-M1 ⊥-proof, the exact ℤ[√5] **Q8<2T<2I→E8**
chain via Mordell even-unimodular uniqueness, the α gluing-anomaly seam, homological unification
(Tr₀→gravity / Tr₁→EM / Tr₂→QM). Guard catch: 2 workers fabricated cert filenames
(`vp_holographic_commutator_jy`, `vp_homological_unification_012`) — `check_book_cert_references`
flagged them; demoted to honest `PROOF-TARGET (cert obligation open)` per the closure contract.
Full guard suite green (firewall 0 forbidden, assembly idempotent, cert-refs clean, validate_csv,
firewall-vs-base). `d0_score` unchanged (prose-only; new claims not yet registered).

### BR3 complete — all 8 priority books integrated

Ran the per-book wave (`tools/group_coverage_by_section.py` → `br3-book-wave` Workflow → assemble + guards
+ commit) for every book carrying core-forcing rows, in the chosen order. **198/198 core-forcing arguments
integrated** (one commit per book):

| book | sections | forcing args | net lines |
|---|---|---|---|
| BOOK_02 proof-spine | 14 | 39 | +984 |
| BOOK_04 spectrum/matter | 10 | 37 | +1328/−134 |
| BOOK_06 evolution/time | 11 | 29 | +1070 |
| BOOK_01 foundations (owner) | 10 | 27 | +1134 |
| BOOK_00 entry/admissibility | 6 | 20 | +428 |
| BOOK_03 finite-action | 4 | 18 | +736 |
| BOOK_07 gravity | 9 | 16 | +1036 |
| BOOK_05 verification | 5 | 9 | +734 |
| BOOK_08 cosmology | 3 | 3 | +140 |

The dropped GOLDEN forcing engine is back: M1 as the single named law + DEF-0.2.2 forcing schema (BOOK_00/01),
the two independent φ-forcings (`p+p²=1` and S1 self-similarity `r²−r−1=0`), the topological chain
(distinguishable-return → torus → defect → shell+φ → step+2), heat-trace time + arrow, mass=closure-density,
Q8<2T<2I→E8 via Mordell, Born=Gleason, DarkRatio=nullity/rank, percolation-as-t=0. **Cert discipline held:**
the no-fabricate-cert rule + `check_book_cert_references` caught every invented `vp_*.py` (2 in BOOK_02,
demoted to PROOF-TARGET); workers across later books correctly refused v17-named certs absent on disk and
tagged them `PROOF-TARGET (cert obligation open)`. The token firewall kept all 3 v17 overshoots out.

Scope note: this wave took the **core-forcing** rows (198). The ledger's `supporting`/`peripheral` integrate
rows (~364 more) remain a tracked follow-up.

### BR2 stale-token cleanup — corpus is clean, guard now strict

`br2-stale-cleanup` Workflow (9 per-book agents + verify): removed **9** `v16 publication-proofread` version
stamps and repaired **20** `(marker moved to 06_AUDIT/…)` corruptions (06_AUDIT was deleted in Phase 2). The
corruption had *substituted* real cert PASS-tokens; **12 were recovered** by reading the `vp_*.py` source
(e.g. `PASS_BORN_QUADRATIC_ORIGIN`, `PASS_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN`,
`PASS_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026`), the rest dropped as dangling notes. `tools/check_book_tokens.py`
is now **strict-by-default** (stale fails CI, not just forbidden); `--allow-stale` opts out. Corpus: 0
forbidden, **0 stale**. ("atlas" kept — real artifact, not cruft.) Books are −44 net lines (boilerplate out,
tokens restored); `d0_score` steady at **2660/3767 (70.6%)**.

---

## R4 — Lean per-claim wave (warm cache + 9 modules promoted to CORE-FORMALIZED)

**Cache fix first.** The Xi5 build had been recompiling mathlib *from source* (~2600-module cone, hours)
because the session-start dep-checkout (aesop/Qq/batteries/Cli) invalidated the local olean cache. Fixed by
`lake exe cache get` (downloaded 8472 valid mathlib oleans); the rebuild then compiled only the D0 modules —
Xi5 + ToralAutomorphism in ~8 min — and all of mathlib is now warm.

**Xi5 (the rails gate).** `D0/Claims/Xi5TorusDefect.lean` builds sorry-free (`xi5_torus_defect` via
`native_decide`, reusing `D0.Dynamics.ToralAutomorphism.trace_T_pow_eq_signed_lucas`): `lucas 5 = 11 ∧
Matrix.trace (T^5) = −11`. Promoted L3→L5 (LEAN_PROVED / CORE-FORMALIZED), +13.

**R4 first wave (`r4-lean-wave` Workflow, 8 agents).** lake is on PATH in the agents' Bash, so each agent
wrote its `D0/Claims/<id>.lean`, **built it itself** (`lake build`, warm cache), and iterated to a genuine
sorry-free green — with the hard rule *delete the file and report `built=false` rather than fake it with
sorry/axiom/`admit`/native_decide-on-a-weakened-goal*. All 8 closed. **Adversarially verified before
promotion:** grep found 0 real sorry/axiom (only comment text, scrubbed); an independent rebuild of all 8
returned exit 0 / `Build completed successfully (2963 jobs)`; the two hardest were read by hand —
- **Q8-Dedekind:** explicit Q8/S3/D4 multiplication tables on `Fin n` (verbatim from the cert), decidable
  subgroup/normality machinery, `native_decide` proving `nonNormalCount` = 0/3/4 and the triple identity
  `[Q8,Q8]=Z(Q8)=Φ(Q8)={±1}` — a real finite-group proof, not a restatement.
- **kernel-zone:** the real 33×33 integer adjacency of K(9,11,13); rank ≤ 3 (every row is one of 3 zone
  patterns) + 30 zone-difference kernel vectors (`native_decide` on `A.mulVec v = 0`) + split 30=8+10+12,
  reusing `D0.Combinatorics.CompleteTripartite`.

The other six (signature-3+1 — proves `Adj31.rank = 3` directly via `Matrix.rank`; vieta-galois φ/ψ; dim-ladder
φ-cascade; time-2D-Pisot `x²−x−1`; window-44; mixing-hierarchy-inversion) are likewise decide/native_decide on
real finite content. All promoted LEAN_PROVED / CORE-FORMALIZED. Aggregates regenerated (**104** leanCoreProved
entries in ClaimMap), idempotent; full guard suite green (validate/firewall/no_sorry/coverage/aggregates/
book-guards). **`d0_score` 2660 → 2777 (70.6% → 73.7%)**: Xi5 +13, the 8 +104.
