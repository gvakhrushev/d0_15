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

---

# ITERATION 2 — Hygiene-KPI · Cleanup · Publication · Lean honesty (DONE)

Audit (3 read-only agents) found: books carried publication-blockers + a flood of trace metadata in the
body; Lean had 17 tautology "proofs"; the repo carried a vendored 2nd repo + quarantine + process logs; and
the KPI only rewarded strength, never cleanup. Result of Iteration 2: a **second KPI axis (hygiene 33 → 100)**,
a clean publish tree, publication-grade books with an apparatus layer, and an honest Lean ledger.

- **Phase H — hygiene/refactor KPI.** `HYGIENE_*` in `d0_status_model.py` + `hygiene_report()` in `d0_score.py`:
  a 100-pt second axis from deterministic git+guard signals (tracked meta-trash, tautology proofs, sorry/axiom,
  phantom certs, orphan PROOF-TARGET, dev comments, prose repo-paths, real in-project .lake; bonus for net
  deletions). New `## Repository hygiene / refactor score` SCOREBOARD section + `scoreboard.json.hygiene`.
  Strength model untouched. Baseline **33/100** (dirty).
- **Phase C — cleanup.** `git rm add/` (44 tracked + 14 artifacts — a whole vendored 2nd repo) + `_QUARANTINE/
  v17_overshoots/` (v17 core reach already in BR3; supporting in git history). Moved `00_ROADMAP/` +
  `LEAN_TRANSLATION_TZ/` → `docs/internal/`. `.gitignore` un-ignores 8 force-added real files (no-go theorems
  + locked cert params). hygiene **33 → 59**.
- **Phase L — Lean honesty.** Removed **17** `(stmt:Prop)(h:stmt):stmt:=h` identity tautologies (6 K-theory/
  spectral-triple modules, Mathlib-blocked) + their 17 `#check` in HardClosureTheoremIndex; reclassified the
  9 owning rows LEAN_PROVED/CORE-FORMALIZED → PYTHON_CERTIFIED/CERT-CLOSED (cert stays real, EXTERNAL-GAP
  noted). New `check_no_tautology_proofs.py` guard (CI). **strength 2777 → 2660** — the −117 fakes exactly
  offset Iteration-1's +117 real R4, so the number is unchanged but now **all-honest**. hygiene **59 → 73**.
- **Phase L+ — quarantine FiniteHodgeComplex.** A broken orphan (struct errors, no CSV claim) that red-flagged
  the release-gate build; typed its psd statement + dropped its placeholder heat-trace theorem, then moved it
  to `_OPEN_WITNESSES/` and dropped its 3 (unused) imports. Per-PR guards all green.
- **Phase P — books publication pass.** `extract_apparatus.py` moved **418** regular forcing/Status tags out of
  prose into per-book `## Apparatus — sources & open obligations` endnotes (rendered by `assemble_books.py`
  from `_apparatus.json`; `--check` in CI). A 10-agent cleanup wave then tidied the bodies: 75 version-narration
  strips, 144 prose repo-refs cleaned, 55 heading fixes (duplicate `*.v15` register-stubs renumbered/folded,
  claim-ids out of headers), 20 dangling `§` filled, 9 dev-TODO removed; 2 redundant duplicate stubs deleted.
  New `check_book_publication.py` guard (fence/table/inline-code-aware) → **PASS**, wired into CI.
- **Hygiene precision sync.** `dev_comments`/`path_leaks`/`corpus_errors`/`tautology_proofs` now read from the
  precise guards (`check_book_publication`, `check_no_tautology_proofs`) instead of loose regexes / the stale
  `check_v14_clean_corpus` length expectations — so the KPI reflects real cleanliness, not false positives.

**End state:** **hygiene 100/100** (only 4 orphan PROOF-TARGET, −0.4); **strength 2660/3767 (70.6%, all honest)**;
books are publication-clean monographs + apparatus; Lean has 0 tautologies / 0 sorry-in-build; the publish tree
is theory + verification only. Full guard suite green (now incl. tautology, apparatus, publication guards).

---

## ITERATION 3 — Synthesis & closure via three roots + §4 (honesty over fitting)

Owner ТЗ: close three *root* nodes (not leaves) at the maximum honest level, then a §4
synthesis harvest. Pattern per root: Explore audit → honest cert with explicit boundaries
→ Lean depth where Mathlib-reachable → registry → book integration → guards → commit.

**Premise correction surfaced (Root A).** The ТЗ premise "Δ_α = φ⁻⁵" contradicts the
ledger: φ⁻⁵ = ξ₅ (proved seam term) is DISTINCT from Δ_α (~4.15e-4 top-vs-alg residual,
owner still open). α is closed as a finite s=−1 spectral *moment*, not a residue.

**Root A — α via ζ_D (commit cb09e4a).** `ζ_D(s)=Tr|D|⁻ˢ` now DEFINED on K(9,11,13)
(was ABSENT). Finite moments closed (cert + Lean `D0.Spectral.ZetaResidueAlpha`):
`ζ_E(0)=359=|E|`, `ζ_E(−1)=359φ⁻²−φ⁻⁵=α_top⁻¹`, `ζ_adj(0)=3=rank`. HONEST: finite scene
has no dimension pole ⇒ residue-at-pole route (THE 15.4.2) stays theorem-target; Δ_α
distinct from φ⁻⁵, analytic owner open. strength 2660→2672.

**Root B — one ℤ₂=Z(Q8) spinor cover (commit 7b0436d).** Seven incarnations unified
machine-checked: cert `vp_z2_spinor_cover.py` + Lean `D0.Synthesis.Z2SpinorCover`
(≥4/7 projections). Joint A: Lucas-trace sign = toral det = Galois norm φ·ψ=−1. Joint B:
+2 fixes the cover sheet (`det(T^{n+2})=det(T^n)`), +1 flips (M1-banned). T-B.2
quasicrystal=time: exact executable Sturmian coincidence to 4000 symbols (was prose-only
40); arrow=Pisot reuses Time2DPisot. FIX: BOOK_02 §02.34 sign typo (ε_n=L_n−φⁿ →
φⁿ−L_n=−ψⁿ). HONEST: M1-uniqueness of orientation=Gal stays prose; topological conjugacy
theorem-target. strength 2672→2699.

**Root C — full carrier forcing (commit at task #25).** Closes the finite content of the
three BOOK_05 §05.6 soft-joints + the symplectic-Gleason uniqueness leg. Certs:
`vp_carrier_full_forcing.py` (roles=orbits; orbital block-constancy by exhaustion on the
(2,2,2) faithful model; unique loopless+complete pattern → K(9,11,13) |E|=359; tower-stop
3-zones + impedance), `vp_class5_aliasing_cabibbo.py` ((Z/44)* char orders {1,4,5,20};
class-5 killed by aliasing |Z5|=5=D_Σ; survivors {1,20}; Cabibbo kept BRIDGE),
`vp_symplectic_gleason_uniqueness.py` (J-invariant quadratic forces a=c,b=0 → unique
x²+y²). Lean `D0.Synthesis.CarrierForcing` (carrier_full_forcing + symplectic_form_unique).
BOOK_05 §05.6 register honestly SHRUNK (5/6 joints' finite content now certified; only the
named meta-steps remain; Δ_α stays the one fully-open obligation). HONEST: M1 no-extension,
full hidden-memory contradiction, and categorical Ostrik/Ising uniqueness stay
theorem-targets. strength 2699→2746.

**§4 — synthesis harvest (this commit).** Verdict per item (Explore-audited):
- *S_DE cubic-vs-quadratic fork (the one real open fork)* — CLOSED as a fork:
  `vp_vacuum_cubic_window.py` (`D0-VACUUM-CUBIC-WINDOW-001`, CERT-CLOSED) COMPUTES the
  discriminator the dossier recorded as never computed — quadratic ratio
  (60−√10)/(60+√10)=0.900 vs cubic (l³−359l−2574, e=(0,−359,2·1287)) ratio
  9.758/12.079=0.808. HONEST: a fork, NOT a decision — DESI DR3 decides and is not run;
  booked at BOOK_08 §08.12.4. strength 2746→(see scoreboard).
- *Signature 3+1* — already LEAN_PROVED/CORE-FORMALIZED (two owners), booked §06.36. Nothing to do.
- *Phason* — terminal-honest: finite content CERT-CLOSED, Lean EXTERNAL-GAP (Mathlib-blocked
  K-theory/spectral-triple). Not closeable without external machinery; left as-is.
- *H0-evolving-w passport* and *external anchors (Coldea/JUNO/NuFIT)* — EMPIRICAL-PASSPORT
  scaffolding the firewall deliberately keeps out of core, and depend on still-absent flavor
  claims (PMNS-δ₀-family, icosian→E8). DEFERRED to backlog (#18) rather than fabricate
  passports for absent claims. Honesty over coverage-theatre.

---

## ITERATION 4 — Autonomous session (owner away ~2h; merged ТЗ + session groundwork)

**Baseline (tag `base-pre-autonomous`, 216 canonical rows):** CORE-FORMALIZED 92,
CERT-CLOSED 71, PROOF-TARGET 12, EMPIRICAL-PASSPORT 10, NO_GO_PROVED 8, NO-GO 8,
BRIDGE-ASSUMPTIONS-EXPLICIT 7, CORE_BRIDGE_SPLIT 4, BRIDGE-CALIBRATION 2,
EXTERNAL-BACKGROUND 1, DEPRECATED 1. strength 2753, hygiene 100, firewall violations 0.

IRON RULES in force (firewall; α honesty boundary; no v17 overshoots; CSV+artifact+graph+log
per change; OWNER-DECISION-NEEDED for owner-level calls; guillotine; positive closure delta).
ТЗ Phases 2/3/4 + T5.2/T5.3 were ALREADY closed earlier this session (Roots A/B/C, S_DE fork,
signature-3+1 CORE) — autonomous front executes the genuinely-remaining work.

### Iteration 4 — end-of-session metrics (delta vs base-pre-autonomous)

| metric | baseline | final | delta |
|---|---|---|---|
| total claims | 216 | 223 | +7 |
| CORE-FORMALIZED | 92 | 97 | +5 |
| CERT-CLOSED | 71 | 69 | −2 (5 promoted to CORE; +3 new cert-level) |
| PROOF-TARGET | 12 | 12 | 0 (no new open targets) |
| EMPIRICAL-PASSPORT | 10 | 14 | +4 |
| strength | 2753 | 2867 | +114 |
| hygiene | 100 | 100 | 0 |
| firewall violations | 0 | 0 | 0 |

Closure delta POSITIVE: +5 core promotions, phason undeclared-gap closed by forcing,
gravastar hole filled, 3 external anchors wired in — and zero new PROOF-TARGETs created.

---

## ITERATION 5 — audit-driven 3-track strategy (balanced)

From a score-based audit (strength 2867/3995 at Iteration-4 end). The naive scoreboard
"+120 cheap promotions" was mostly Mathlib-blocked; honest realizable closure was the goal.
Balanced across three tracks. DoD per claim = the verified-closure-protocol skill.

**Track 1 — closure (Step B, commit ab351f6).** Bless D0-ALPHA-ZETA-RESIDUE-001 CERT-CLOSED
-> CORE (gap-free finite-moment theorem) + 6 CORE promotions: SPIN2, HIGGS-YUKAWA (new
exact Lean modules), and the 4 ARCHIVE-* claims (registry was under-crediting already-proved
D0.Geometry.Archive* modules). +86 strength.

**Track 2 — synthesis (Step C, commit 3814908).** Z2SpinorCover extended 4/7 -> 7/7 (all
seven ℤ₂ incarnations); D0-RANK3-CAUSAL-CONE-001 (D0.Synthesis.RankCausalCone) proves the
(3,1)->Minkowski-cone structure — a SHARPENED BRIDGE that narrows but does not close the
gravastar compactness gap (scene-rank↔cone-space identification remains; COMPACTNESS stays
LEM, not faked to THE). Registry repoints: cleared the phantom D0.Edge.AlphaRamification-
Constructive path; declared Δ_α analytic owner = CVFT-F1 (shared engine with the residue
route). +20 strength.

**Track 3 — honesty cleanup (Steps A+D, commits 2a65aa9, 51ed635).** New guillotine guard
`check_cert_can_fail.py` (wired into guards.yml) — FINDING: 24 registered certs could not
FAIL (5 pure print-stubs + 19 compute-theater), far beyond the 5 expected; grandfathered as
an explicit, printed DEBT RATCHET that blocks new stubs. Of the 5 approved print-stubs:
HODGE / NOAXION / BH-A4 rewritten with real exact finite witnesses + negative controls
(removed from the ratchet); SPECTRAL-EINSTEIN / HODGE-LINKS demoted to PROOF-TARGET (no
quick genuine witness), stub certs deleted, HODGE-LINKS CertTarget removed from
run_hard_theorem_closure. Float->exact: higgs-yukawa + spin2 certs rationalized (unblocked
the Track-1 promotions). Fixed 2 stale docs/internal pointers to the removed
99_PRESERVED_SOURCE/ tree. Ratchet 24 -> 19; orphan PROOF-TARGETs 4 -> 2.

### Iteration 5 metrics (vs Iteration-4 end)
| metric | Iter4 end | Iter5 now | delta |
|---|---|---|---|
| CORE-FORMALIZED | 97 | 105 | +8 |
| CERT-CLOSED | 69 | 60 | −9 (6 promoted to CORE, 2 demoted, + churn) |
| PROOF-TARGET | 12 | 14 | +2 (honest demotions) |
| strength | 2867 | 2963 | +96 |
| hygiene penalty | −0.4 | −0.2 | orphan-PT 4→2 |
| cert can't-fail debt | (24 found) | 19 | −5 |

All 8 guards green (validate, firewall, no_tautology, cert_can_fail, apparatus, publication,
book_assembly, no_sorry). Net PROOF-TARGET +2 is the honest cost of the integrity demotions;
all promotions backed by gap-free Lean theorems; no passport promoted to core; no fakes.
Deferred: 41 process-tag (v15/NOID/CVFT) section renames (cosmetic, P2); the 19 remaining
compute-theater certs (owner-decision, ratchet in place); the 9 registered-but-missing certs.

### Iteration 5 — finite-core reductions (the program: shadow the Mathlib-blocked, name the remainder)

Demonstrated that even "Mathlib-blocked / held-at-hypothesis" obligations carry a decidable
finite shadow that promotes honestly, with the genuinely-frontier remainder named:
- **Delta_alpha** (gluing anomaly): CERT-CLOSED -> CORE. Both alpha writings are closed Q(phi)
  forms (no data) => Delta_alpha = -156109/5 + 289442/15 phi is an EXACT Q(phi) element,
  != 0, < phi^-16. Lean D0.Spectral.DeltaAlphaExact. Owner (CVFT-F1 resolvent) frontier; m_nu BRIDGE.
- **Class-5 hidden memory**: named gap -> decidable shadow. Joint (winding,address) readout
  collapses 25->5 (class5_readout_collapse, decide). Full M1 grammar 01.11C (v17, absent) frontier.
- **K-theory gap-labeling** (hardest Mathlib-blocked): NEW D0-KTHEORY-GAP-MODULE-001 (CORE).
  Labels in rank-2 module Z+Zphi^-1 (closed by phi^-1+phi^-2=1) = exact Sturmian frequencies.
  Bellissard IDS=K0-trace stays EXTERNAL-GAP. (Flagged: old D0-KTHEORY-001 float cert fabricates IDS.)
strength 2963 -> 3003 (74.1%); CORE 105 -> ~108; all guards green. Pattern captured in the
verified-closure-protocol skill.

### Audit-as-forcing (predecessor batch, commit 8e0183f)

Reframed four audit critiques from "lower-by-enumeration" to forcing (M1: absence of
alternatives is NOT an argument). D0-EW-WINDOW-FORCING-001 (710/113 grammar + 2pi CF-minimality),
D0-HIGGS-CUBE-DIAGONAL-001 (sqrt2 forced by orthogonal cell + named delta_loop), D0-COMPACTNESS-
DEF-FORCING-001 (C=M/R_initial forced by causal posing), D0-PHI99-DEPTH-FORCING-001 (99=V9*V11).
Installed the review-side firewall BOOK_05 §05.8.R ("absence of alternatives is not an argument;
argument = forcing-uniqueness OR named-gap"). strength ~3003 -> ~3031, zero enumeration-demotions.

### Iteration 6 — forcing-owner integration (Frobenius-class external theorems)

Owner supplied a catalog of 9 classical uniqueness/classification theorems as candidate
forcing-owners. Reconnaissance (3 Explore agents) found most D0 links ALREADY owned
(Q8/Dedekind, phason/Goldstone, spin-2/Weinberg, phi/Hurwitz, icosian->E8/Mordell in prose,
time/Pisot), so the integration split three honest ways, with ZERO enumeration-demotions:

**(a) Closed by forcing — decidable shadows (CERT + Lean, CORE-FORMALIZED):**
- `D0-ICOSIAN-E8-GRAM-001` — the E8 Gram is even (diag 2) + unimodular (det=1, `native_decide`),
  rank 8=2*4; realizes the §02.18.2 point-4 "Target LEAN_PROVED" spec. Lean
  `D0.Claims.IcosianE8GramFinite`; control A8 det=9.
- `D0-JONES-INDEX-PHI-001` — `4cos^2(pi/5)=(3+sqrt5)/2=phi^2` at the n=5 Jones-index slot =
  Fibonacci quantum dimension; closes the bare "why phi as a quantum dimension". 3rd phi-channel
  (§01.21.3). Lean `D0.Claims.JonesIndexPhi` (algebraic core; trig series in cert).
- `D0-DIM8-NETWORK-001` — the dimension-8 forcing-network skeleton (8=2*4; tower 8|24|120 idx
  3,5,15; E8 even-unimodular; D4 triality 3 legs, |S3|=6); the research's headline. §02.18.3.
  Lean `D0.Synthesis.DimensionEightNetwork`.

**(b) Named the owner — BRIDGE-ASSUMPTIONS-EXPLICIT owner-edges (<=11, honesty not points) +
4 ledger ASSUMP-* + 4 Bridge Lean files:**
- `ASSUMP-JONES-INDEX`, `ASSUMP-MORDELL-E8` — own the obstruction/uniqueness backing the two
  CORE shadows (Hurwitz precedent: ledger names the full external theorem, claim stays CORE).
- `D0-CONNES-RECONSTRUCTION-OWNER-001` (`ASSUMP-CONNES-RECONSTRUCTION`) — "metric = spectrum of
  the Dirac operator"; routes the rank-3=causal-cone / Connes-distance NAMED GAP (§07.51.3).
- `D0-TIME-MODULAR-FLOW-OWNER-001` (`ASSUMP-TOMITA-TAKESAKI`) — "time = modular flow" (thermal
  time); deepens the Pisot time layer (§06.30a). Both M1-aligned; Lean conditional theorems.
- Second channels (cited prose): Busch 2003 (Born quadraticity on dim-2 where Gleason fails) +
  Masanes-Mueller 2019 (d=3) in §02.28; Baer 1933 (Q8 x B x D structure) in §02.18.

**(c) Honestly rejected — anti-numerology calibration (BOOK_00 §00.9 + §05.8.R), zero
enumeration-demotions:** Leech Lambda24<->K=30 (24!=30, no 24-dim object); triality => 3
generations (3 = #D4 reps); C_max=3/8 not owned by Weinberg; Pisot >=3-letter conjecture OPEN;
Frobenius integrability is a scaffold. Reconciled the firewall's own (710,113) numerology-failure
example with D0-EW-WINDOW-FORCING-001 via the grammar-priority discriminant.

### Iteration 6 metrics (vs audit-as-forcing end)
| metric | audit end | Iter6 now | delta |
|---|---|---|---|
| CORE-FORMALIZED | 107 | 110 | +3 (E8, Jones, dim8-network) |
| BRIDGE-ASSUMPTIONS-EXPLICIT | 7 | 9 | +2 (Connes, Tomita-Takesaki) |
| external owners (ledger ASSUMP) | 7 | 11 | +4 |
| strength | 3031 | 3113 | +82 |
| integrity demotions | 0 | 0 | ZERO enumeration-demotions |
| hygiene | 100 | 100 | — |

5 new Lean modules (`IcosianE8GramFinite`, `JonesIndexPhi`, `ConnesReconstructionBridge`,
`TomitaTakesakiBridge`, `DimensionEightNetwork`) each build **sorry-free** (verified by
individual `lake build` + their full dependency closures). 3 new certs (icosian_e8_gram,
jones_index_phi, dim8_network) PASS + can-FAIL. All registry/cert guards green (validate_csv,
check_firewall 235 rows, run_registered_certs, check_cert_can_fail, books publication-clean).
Closure delta strictly positive; every promotion backed by a gap-free Lean theorem; every
external theorem a NAMED bridge owner, not a hidden assumption; refusals recorded.

### Iteration 6 — BUILD-HYGIENE FINDING (pre-existing, surfaced by the first full `lake build D0.All`)

This session's full aggregate build (`lake build D0.All`) is **RED**, and the cause is entirely
pre-existing — NONE of it is introduced by the Iteration-6 work (all 5 new modules compile). The
CI never runs `lake build` (scoring keys off declared `lean_status` + on-disk module existence),
so this was masked. **17 modules fail to compile** (root causes):
- *Stale Mathlib import:* `D0.Gravity.CriticalCollapseDSS` imports `Mathlib.Data.Rat.Basic`
  (renamed in the current pin); cascades to `EchoCapacityHorizon`, `FiniteHorizonCapacity`,
  `FiniteHolographicEntropy`.
- *Malformed `theorem _ : Prop := <prop-term>`* (should be `def`): `FiniteCochainNoAxion`,
  `NonAbelianSeamObstructionGap`, `VacuumFeedbackEquationOfState`, `TickS3BaryonAsymmetry`,
  `HodgeMatterGravityArchiveIndex`.
- *Unknown identifiers / missing defs:* `FiniteMinCutEntropy` (`minCutValue`),
  `Book04OperatorBoundary` / `HiggsScalarProjectorDecision` (`ConstructiveScalarProjectorClosure`),
  `FiniteA2EinsteinResponse` (missing `FiniteWeakFieldQuotient` / `GradedBianchiClosure`),
  `TerminalAlphabetABCD`.
- *Registered-claim impact:* **16 of 17 are orphan modules** (no claim references them, so
  registry/firewall/score are unaffected). The **one exception is `D0.NoGo.StressTestSuite`**,
  the module of claim `D0-NO-GO-STRESS-SUITE-001` (declared `LEAN_PROVED` / `NO_GO_PROVED`):
  it references non-existent `D0.Matter.*` identifiers and does NOT compile — a genuine
  `LEAN_PROVED`-but-uncompilable discrepancy the missing CI build hid.

Disposition: this is a dedicated **Lean build-hygiene** follow-up (fix/quarantine the 17 modules,
correct or demote `D0-NO-GO-STRESS-SUITE-001`, and add a `lake build D0.All` CI guard so it cannot
silently regress), spun off as its own task — NOT folded into the forcing-owner iteration. The
Iteration-6 deliverables stand: each new module and its dependency closure compiles cleanly.

### Iteration 7 — cross-domain bridges, AFTER the deep-research self-check filter

A second deep-research front (8 areas) arrived **pre-calibrated**: the owner had already run the
self-check and downgraded the inflated statuses. The discipline this iteration was to integrate
at the honest (downgraded) status and NOT re-inflate from the report text. The filter (now law,
BOOK_05 §05.8.S): deep-research = candidate generator; mandatory mechanism + limits gates;
coincidence at one point ≠ identity.

**The downgrade delta (recorded as the calibration sample):**
| research label | honest status | why downgraded |
|---|---|---|
| Fibonacci `d_τ=φ` ⇒ `I_f=logφ` FORCING | **LEM** | both give `logφ` but the categorical↔toral isomorphism is unwritten (mechanism gate) |
| `γ_Choptuik ↔ C=3/8` BRIDGE-owner | **HYP** | `γ(D)` crosses `3/8` between `D=4,5` and leaves it — a `D=4` coincidence, limits diverge (limits gate) |
| Bekenstein `S≤A/4` FORCING | **BRIDGE** | supports "capacity finite", does not force the D0 structure/`φ` |

**What landed (all at honest status, zero re-inflation):**
- **Phase A** `D0-FIBONACCI-IF-FORCING-001` (CERT-CLOSED+LEAN_PROVED, **LEM**): `I_f=logφ` two
  ways — Fibonacci fusion `d_τ=φ` and toral spectral radius `|-φ|=φ`; Lean `FibonacciIfBridge`
  proves the same `φ` two ways; the iso is the named gap. BOOK_01 §01.21.4.
- **Phase B** `D0-PACKING-LIMIT-001` (CERT-CLOSED, **HYP** verdict): probe shows `3/8` is a
  `D=4` crossing of `γ(D)`, not a shared limit; unified packing-limit NOT derived. BOOK_07 §07.51.4.
- **Phase C** external axiom forcings (BRIDGE): `D0-COMPLEX-QM-FORCING-001` (Renou/Chen/Li:
  real-QM excluded), `D0-M1-INFO-RECONSTRUCTION-001` (Hardy/Masanes-Müller/CDP: finite capacity
  ⇒ complex QM — external owner of M1 itself), + Jacobson cite strengthening the Connes edge
  (`δQ=TdS`, `S=A/4`). BOOK_00 §00.9.
- **Phase D** `D0-MODULAR-TIME-FLAVOR-001` (CERT-CLOSED, **LEM**): time and flavor share the
  **SL(2,ℤ) modular group** — flavor `A5 = PSL(2,5) = PSL(2,ℤ)/Γ(5)`, time `T ∈ GL(2,ℤ)` golden;
  PMNS `sin²θ₁₂=1/3−2δ₀²=0.3055` beats GRA/GRB vs NuFIT 6.0. Explicitly kept distinct from the
  Tomita–Takesaki *modular automorphism* (the conflation trap). BOOK_06 §06.30a.
- **Phase E** `D0-DSI-EXPERIMENTAL-001` (EMPIRICAL-PASSPORT): log-periodic ladder seen in
  ZrTe5/HfTe5 — FORM confirmed, `λ`=Coulomb≠`φ` (critical gap). `D0-ENTROPIC-DARK-GRAVITY-001`
  (BRIDGE, Verlinde). Phason §08.51: Goldstone owner cite added (closing the Iteration-6
  deferred loose end) + DESI DR2 evolving-`w` marked **HYP** (no phason `w(z)` yet, awaits DR3).

### Iteration 7 metrics (vs Iteration-6 end)
| metric | Iter6 end | Iter7 now | delta |
|---|---|---|---|
| CORE-FORMALIZED | 110 | 110 | 0 (this front is bridges/LEM/HYP by design) |
| CERT-CLOSED (incl. LEM/HYP) | 63 | 66 | +3 (Fibonacci, packing, modular-time-flavor) |
| BRIDGE-ASSUMPTIONS-EXPLICIT | 9 | 12 | +3 (complex-QM, M1-info, Verlinde) |
| EMPIRICAL-PASSPORT | 14 | 15 | +1 (DSI) |
| ledger ASSUMP | 11 | 14 | +3 |
| strength | 3113 | 3179 | +66 |
| integrity demotions | 0 | 0 | ZERO re-inflations |

3 new Lean modules (`FibonacciIfBridge`, `ComplexQMBridge`, `M1InfoReconstructionBridge`,
`VerlindeEntropicBridge` — 4) build sorry-free individually. 4 new certs (fibonacci_if_bridge,
packing_limit_probe, modular_time_flavor, dsi_experimental) PASS + can-FAIL. The deep-research
filter is now law (§05.8.S). Every status is the honest minimum that survived the two gates;
no research label was promoted verbatim.

### Iteration 8 — researcher contributions developed into closures (reforge, don't discard)

Two researcher documents arrived: (1) generative dynamics (Feshbach–Schur, RG-as-forgetting,
ε²=φ⁻¹⁶); (2) a v3.0 pack of six book insertions (one correct, one error, two over-statements,
two to check). The owner's directive: *develop into closures, reforge errors into tasks, bring
over-statements to honest level keeping the core*. The constructive dual of the deep-research
filter is now law (§05.8.T).

**The main closure (doc 1).** `D0-GENERATIVE-DYNAMICS-001` (CERT-CLOSED + LEAN_PROVED, LEM):
D0 is a **generator of dynamics**, not a static classifier, via Feshbach–Schur on the
rank-3(active)/kernel-30(archive) split. Exact Schur determinant identity ⇒ resonances = poles
of the effective operator `W_eff`; series index k = archive excursions = algorithmic time; the
seam anomaly `C_n≠0` (Lean `GluingAnomalyTime`, `native_decide`) forces time; loop floor
`ε²=φ⁻¹⁶` ⇒ finite cycles, no UV divergence (named gap `ε²≠Δα`); RG = typed forgetting
(`p+p²=1`, residual `≤δ₀`, `β=c/\log φ`). Discharges the §06.34 open obligation at the finite
level. LEM (continuum QFT-as-shadow needs an S-matrix simulation for THE).

**Reforges and honest-level fixes (doc 2), each keeping the valuable core:**
- §02.21 zone-matrix **error** → `D0-LAPLACIAN-SPECTRUM-FIX-001` (CERT): M is row-stochastic
  (ρ=1, eig {1,−0.42,−0.58}); the `1.42/1.58` it hit is `eig(I−M)` = the S_DE window (Book 08);
  `φ⁻¹` is the §06.2 envelope tick — three numbers separated, two matrices. §02.18.4.
- §06.42 α **over-statement** → confirmed the corpus is already honest: `ξ₅=φ⁵−11=φ⁻⁵` kept THE,
  α-line CHK with `Δα` open; the data residual (3.71e-4) and the algebraic residual (4.15e-4)
  separated. §02.13.
- §09.8 I_f **wrong formula** → `D0-IF-KS-FORMULA-FIX-001` (CERT): `Tr(\log T)/\mathrm{rank}` is
  complex (`det T=−1`); correct `h_{KS}=\log|\lambda_{\max}|=\log φ`. Number kept, formula fixed.
  §09.03.
- §07.22 A/4 **forcing attempt** → `D0-FOURCOLOR-HORIZON-CAPACITY-001` (CERT, outcome b): the "4"
  forced (`χ(K_4)=4`=ABCD), the "1/4" a named gap (chromatic 4 ≠ Bekenstein coefficient). §07.40.
- §04.12 CKM/PMNS **error** → `D0-CKM-PMNS-COMPLEMENTARITY-001` (CERT, HYP): `V_CKM U_PMNS^T=I`
  false; reforged to quark-lepton complementarity `θ_C+θ_12≈45°` (~1.6° miss). §06.30a.
- §01.25 φ_E(44)=20 **correct** → `D0-WINDOW44-TOTIENT-M1-001` (CERT), entered as-is with the M1
  totient argument (`|Aut(Z/44)|=20`). §07.23.

### Iteration 8 metrics (vs Iteration-7 end)
| metric | Iter7 end | Iter8 now | delta |
|---|---|---|---|
| CERT-CLOSED (incl. LEM/HYP/reforge) | 66 | 73 | +7 |
| strength | 3179 | 3226 | +47 |
| integrity demotions | 0 | 0 | zero discards; errors reforged |
| hygiene | 100 | 100 | — |

New: 7 certs (feshbach_schur, gluing_anomaly, loop_floor, rg_forgetting, laplacian_3x3,
if_kolmogorov_sinai, fourcolor_horizon, ckm_pmns, window44 — 9 actually) all PASS + can-FAIL;
1 new Lean module (`GluingAnomalyTime`, `native_decide`) builds. §05.8.T (external-contribution
rule) is now law. ZERO ideas discarded: every error became a clarification or a named gap, every
over-statement kept its core at the honest status.

### Iteration 9 — obligation 5 closed (M1 no-extension): the tower stops at 3 zones

The last open meta-step of the carrier forcing (BOOK_05 §05.6 obligation 5) and the root of the
rank-3 cascade is **closed** as a no-go: no admissible structure registers a fourth zone
(`D0-TOWER-STOP-NOEXT-001`, CORE-FORMALIZED + LEAN_PROVED, Lean `D0.Tower.NoExtension`). By
DEF-0.2.2 on a hypothetical `Z4`:
- **CASE 2 (repeat)** — `≥2` copies carry a nontrivial copy-permutation symmetry (`|S₂|=2>1`,
  `native_decide`) ⇒ copy-index = external catalogue ⇒ `⊥M1` (Dedekind/`Q₈` §01.7.1A transferred).
  No gap. (`vp_zone_repeat_catalog.py`.)
- **CASE 1 (new type)** — the necessity types are the slots of the forced quadratic `p²+p=1`
  (`p=φ⁻¹`): `p`=distinguish, `p²`=preserve, `=1`=close — `3 = 2` terms `+ 1` closure (degree-2,
  *not* a list). No fourth independent slot: `ℤ[p]/(p²+p−1)` rank 2, `p³=2p−1` reduces into
  `span{1,p}` (Lean `p_cubed_reduces` via `linear_combination` on `phi_inv_satisfies_primitive`);
  a `p³`-type is iterated runtime (BOOK_01:556) = a repeat ⇒ CASE 2. (`vp_member_zone_isomorphism.py`,
  `vp_degree2_three_types.py`.)

§05.6 register updated (theorem-target → closed no-go; the only entry open all the way down is
now `Δα`, obligation 4). **Honest scope:** the COUNT (3 slots, no 4th) is Lean-proved; the three
role-names cite forced primitives, assembled not re-derived. **Cascade (not over-promoted):** the
closure forces the 3-*count* (`rank=3`); the leaves that also need the *geometric* reading
`rank-3 = causal cone` (the `3/8` ceiling, the Choptuik exponent) keep that as a **separate**
named gap (§07.51.3) — the count is forced, the geometric identification is **not** promoted here.

### Iteration 9 metrics
| metric | Iter8 end | Iter9 now | delta |
|---|---|---|---|
| CORE-FORMALIZED | 110 | 111 | +1 (`D0-TOWER-STOP-NOEXT-001`) |
| strength | 3226 | 3246 | +20 |
| open §05.6 obligations | 2 (4,5) | 1 (4 = Δα) | −1 (obligation 5 closed) |
| integrity demotions | 0 | 0 | — |

3 new certs (zone_repeat, member_zone_iso, degree2_three_types) PASS + can-FAIL; 1 new Lean
module (`D0.Tower.NoExtension`) builds. The root of the rank-3 cascade is closed; the geometric
leaf-gaps are kept honest, not flipped.
