# MECHANICAL REPAIR BATCH — punch-list items 4–5 (release audit)

Date: 2026-07-05. Serial execution, incremental log after EACH step.
Constraints: no git commit; never touch any row containing 053040.

Tasks:
1. Lean refactor D0/Foundation/CanonicalSelectorNoGo.lean (compile-hang fix) + registry flip if green.
2. Retirement banners on 4 retired fake CVFT certs in 05_CERTS/.
3. Adjudicate GENERATED vs hand-maintained for D0_PUBLICATION_EVIDENCE_MATRIX.csv + TOTAL_FINAL_CLAIM_INDEX.csv; regen or surgical REFORGED swap.
4. Extend tools/check_book_ledger_sync.py with CORE_BRIDGE_SPLIT closure-prose flagging; acceptance test = BOOK_07:1780 Einstein passage.

---

## TASK 1 — CanonicalSelectorNoGo.lean refactor

### Step 1.0 — diagnosis refinement (pre-edit)

- Read current file: the 9/11/13 theorems ALREADY route through the general lemma
  `no_equivariant_section` (no decide at n=9/11/13 anywhere). So the SELECTOR_NOGO_MINT_LOG
  hypothesis (decide instantiating Perm(Fin 13)) is half-right: the explosion is in the
  SMALL-n kernel `decide` calls (`control_n1_has_section`, `no_section_n2`, `no_section_n3`).
  Kernel reduction of `Fintype (Equiv (Fin n) (Fin n))` (built via embeddings + Trunc) is
  known-catastrophic even for n=1..3 — consistent with a 2.5h elaboration hang.
- Secondary fragilities found in the same file (would surface as errors once the hang is fixed):
  (a) `Fin.val_one''` lemma-name roulette in `no_equivariant_section`;
  (b) `simpa [Equiv.trans_assoc]` in `fixed_forces_all_identity` rewrites in the wrong
      associativity direction;
  (c) `scene_zones_no_section` applies `hc (Finset.mem_univ b) hb` without the explicit `b`
      binder and relies on a postponed metavariable for `n`;
  (d) trailing `simp` in the product step (replaceable by deterministic `zero_mul` rws).
- FIX PLAN: keep statements IDENTICAL (theorem names + types unchanged so the registry row
  stays valid); switch n=1..4 concrete checks to `native_decide` (compiled evaluation, minutes
  not hours; repo precedent: 10+ core modules incl. Phase/Capacity use native_decide); make
  `fixed_forces_all_identity` a group-cancellation proof (`mul_right_cancel` + `inv_eq_one`);
  add pointwise helper `no_fixed_labeling` (swap 0 1 contradiction, omega-only, no name
  roulette) and route `no_equivariant_section` + `scene_zones_no_section` through it;
  replace final `simp` with `rw [..., zero_mul, zero_mul]`. NOTHING evaluates
  `Perm (Fin n)` as a Finset for n > 4.
- 053040: absent from CLAIM_TO_LEAN_MAP.csv (re-verified below at flip time).

### Step 1.1 — refactor applied, targeted build launched

- Edits to D0/Foundation/CanonicalSelectorNoGo.lean (all theorem NAMES and STATEMENTS unchanged):
  * control_n1_has_section / no_section_n2 / no_section_n3: decide -> native_decide
    (n4 already native_decide). Doc block updated to state the n<=4 cap explicitly.
  * fixed_forces_all_identity: fragile `simpa [Equiv.trans_assoc]` -> group cancellation
    (`one_mul` + `Equiv.Perm.mul_def` rw, then `inv_eq_one.mp (mul_right_cancel h)`).
  * NEW helper theorem no_fixed_labeling (hn : 2 <= n) (b) : pointwise no-go via
    swap ⟨0,_⟩ ⟨1,_⟩ + `Equiv.swap_apply_left` + `Equiv.Perm.one_apply`; distinctness by
    `congrArg Fin.val` + omega — no `Fin.val_one''` name roulette.
  * no_equivariant_section: now 2 lines through no_fixed_labeling (card_eq_zero +
    filter_eq_empty_iff). Still fully abstract, no decide.
  * scene_zones_no_section: term-mode triple of `no_fixed_labeling (by omega)` — kills the
    postponed-metavariable + missing-explicit-binder bugs.
  * canonical_within_zone_selector_nogo product step: `simp` -> `rw [..., zero_mul, zero_mul]`.
- Source-clean check: grep -nwE "sorry|admit|axiom" = NONE (exit 1).
- Targeted build launched in background: `lake build D0.Foundation.CanonicalSelectorNoGo`
  (log: scratchpad/lean_build_selector.log, markers BUILD_STARTED / DONE exit=N).
- Proceeding to TASK 2 while the build runs (tasks are file-disjoint; registry flip for
  TASK 1 remains GATED on green build + #print axioms).

---

## TASK 2 — retirement banners on 4 retired fake CVFT certs

### Step 2.1 — banners added + verified (COMPLETE)

- Added `print("RETIRED_2026-07-05_SEE_REFORGED: ... NON-LOAD-BEARING")` as the FIRST statement
  of main() in each of:
    05_CERTS/vp_cvft_boundary_channel_rank.py        (banner names ..._boundary_channel_rank_REFORGED.py)
    05_CERTS/vp_cvft_refined_logdet_rank_bound.py    (..._refined_logdet_rank_bound_REFORGED.py)
    05_CERTS/vp_cvft_ueff_pole_discipline.py         (..._ueff_pole_discipline_REFORGED.py)
    05_CERTS/vp_cvft_uv_feedback_tail_bound_refined.py (..._uv_feedback_tail_bound_refined_REFORGED.py)
  The `vp_cvft_*_REFORGED.py` placeholder in the prescribed banner was instantiated with the
  concrete superseding filename per cert (all 4 REFORGED files confirmed present in 05_CERTS/).
- NO exit-code change, NO content removed (indexes still reference these certs).
- Verified by running all 4: banner prints FIRST, then the historical PASS tokens, exit=0
  unchanged for every one. TASK 2 LANDED.

---

## TASK 3 — REFORGED swap in the two publication CSVs

### Step 3.1 — generated-vs-hand-maintained adjudication + surgical swap (COMPLETE)

- Writer search: `grep -rln "D0_PUBLICATION_EVIDENCE_MATRIX|TOTAL_FINAL_CLAIM_INDEX" --include="*.py"`
  over the WHOLE repo hits only 05_CERTS/vp_total_publication_readiness.py, which only READS
  (existence assert + row parse) — never writes. No generator exists in tools/ or anywhere.
  VERDICT: both CSVs are HAND-MAINTAINED -> surgical row edits (per task branch B).
- 053040 pre-check: 0 occurrences in both files.
- Rows 136 (D0-CVFT-F4) and 139 (D0-CVFT-F7) in BOTH
  03_THEORY_MAP/D0_PUBLICATION_EVIDENCE_MATRIX.csv and 04_VERIFICATION/TOTAL_FINAL_CLAIM_INDEX.csv:
  retired cert filenames swapped for the _REFORGED versions, exactly mirroring the registry
  (CLAIM_TO_LEAN_MAP.csv rows 137/140 python_cert fields):
    F4: vp_cvft_uv_feedback_tail_bound_refined_REFORGED.py;vp_cvft_ueff_pole_discipline_REFORGED.py
    F7: vp_cvft_boundary_channel_rank_REFORGED.py;vp_cvft_refined_logdet_rank_bound_REFORGED.py
  Edit performed with count==1 asserted replacements (no other fields/rows touched; newline
  style preserved via newline="").
- Post-check: grep confirms only _REFORGED names remain on those rows in both files. TASK 3 LANDED.
- Guard: 05_CERTS/vp_total_publication_readiness.py re-run after the swap ->
  PASS_TOTAL_PUBLICATION_READINESS, exit=0 (all 7 artifacts still present, parse intact).

---

## TASK 4 — check_book_ledger_sync.py demoted-row extension

### Step 4.1 — extension wired + acceptance test (COMPLETE)

- tools/check_book_ledger_sync.py extended with a DEMOTED-CLOSURE-PROSE class:
  * demoted set = release_status in {CORE_BRIDGE_SPLIT} OR lean_status in
    {LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS} (lean-side demotion marker);
  * flags ONLY exact claim_id mentions (or exact lean_theorem-name mentions incl. bare
    after-dot names >= 6 chars) with closure vocabulary \b(proved|proven|CERT-CLOSED|
    divergence-free)\b within +-3 lines; NEG_CLOSE-negations excluded; allowlist honored;
  * findings print [DEMOTED-CLOSURE-PROSE] cid ledger=rs/ls file:line and are FATAL (exit 1),
    same contract as PROSE-OVERCLAIM (coordinator-accepted default).
- FIRST RUN: 7 flags. Einstein flag present (acceptance) but 6 lean-side flags inspected
  one-by-one = ALL benign-attachment (closure token belongs to an ADJACENT CERT-CLOSED claim;
  the demoted rows themselves cited honestly: D0-CVFT-F1 "stays the closed-negative no-go",
  D0-DIXMIER-RESIDUE-OWNER-001 / D0-ADLER-WEISS-PARTITION-OWNER-001 /
  D0-RIEFFEL-GHP-CONTINUUM-OWNER-001 owner-edge prose). Storm condition met -> accepted
  fallback applied, gentler variant: lean-side branch KEPT but skips rows whose release tier
  already discloses the hedge itself (DEMOTED_LEAN_EXEMPT_RS = CLOSED tiers +
  {BRIDGE-ASSUMPTIONS-EXPLICIT, NO-GO, NO_GO_PROVED, BRIDGE-CALIBRATION, DEPRECATED}).
  Rationale in code comment: hedged tiers are honest labels (only benign-attachment hits);
  CLOSED tiers make prose closure ledger-CONSISTENT (lean-vs-release inflation is
  vp_status_inflation_audit's jurisdiction, not book-ledger sync). Branch stays alive for
  future lean-demoted rows on unhedged mid tiers.
- ACCEPTANCE RUN (final): exactly 1 flag —
    [DEMOTED-CLOSURE-PROSE] D0-SPECTRAL-EINSTEIN-001 ledger=CORE_BRIDGE_SPLIT/LEAN_PROVED
      in 0043__07.41__trace-heat-capacity-gravity.md:49
  = the known BOOK_07:1780 Einstein passage ("proved object", "CERT-CLOSED",
  "divergence-free" against a CORE_BRIDGE_SPLIT row). ZERO spurious flags. PROSE-OVERCLAIM
  still 0; --strict mode still functional (pre-existing underclaims unchanged). NO allowlist
  entry added for the Einstein flag (it is the genuine desync the check exists to catch).
- Guard is now legitimately RED (exit 1) pending the separate BOOK_07 prose repair. TASK 4 LANDED.

### Step 1.2 — first refactored build: killed at 21 min, kernel-grind diagnosed by sampling

- Targeted build of the refactored module ran 21 min wall / ~6 min CPU, RSS 2.2 GB, then
  CPU accumulation slowed to a crawl (~8%/s) — same hang signature as the 2.5h run.
- `sample` of the lean worker (scratchpad/lean_sample.txt): ONE elaboration snapshot thread
  stuck inside `Lean.addDecl -> Environment.addDeclCore -> lean::catch_kernel_exceptions ->
  lean::type_checker::whnf / whnf_core / reduce_recursor / reduce_proj / reduce_bin_nat_op`
  = the KERNEL type-checker is doing an exploding recursor reduction while checking ONE
  declaration. So the blowup survives the decide->native_decide swap; theorizing about which
  declaration is unreliable -> switching to empirical bisection with fast `lake env lean`
  runs on scratch fragments (Mathlib deps cached; import load ~1 min per probe).
- Build + lean worker killed (pids 33565/33599).

### Step 1.3 — root cause found by bisection; module GREEN in seconds (2026-07-06)

- Bisection probes (lake env lean, Mathlib deps cached, each probe seconds):
    ProbeA n=1 native_decide ................ PASS 2.0s
    ProbeB abstract lemmas .................. 13s, exposed LATENT ERROR: `Finset.filter_eq_empty_iff`
        cannot rewrite `equivariantSections n = ∅` without unfolding the def first (this error
        was in the ORIGINAL file too, masked by the hang). FIX: `unfold equivariantSections`
        between `card_eq_zero` and `filter_eq_empty_iff`.
    ProbeC n=2,3,4 native_decide ............ PASS 2.0s
    ProbeD scene_zones_no_section 9/11/13 ... PASS (seconds)
    ProbeE + canonical_within_zone_selector_nogo ... HANG (killed at 3 min) -> exploder isolated
    ProbeF = E minus canonical .............. PASS -> canonical theorem itself is the exploder
    ProbeG canonical w/ literal-first rewrites PASS 1.8s
- ROOT CAUSE (matches the step-1.2 kernel sample exactly): in the product bullet
  `rw [no_equivariant_section (n := 9) …, zero_mul, zero_mul]`, the kernel is pushed to
  normalize a still-symbolic `(equivariantSections n).card` inside a Nat multiplication to a
  literal (reduce_bin_nat_op needs literal args) — i.e. to ENUMERATE `Perm (Fin 11)` (~4*10^7)
  in the kernel. NOT the small-n decides (they were a second, independent hazard, now
  native_decide), NOT the general lemma. FIX: `have h9/h11/h13 : … = 0` then
  `exact ⟨h9, h11, h13, by rw [h9, h11, h13], control_n1_has_section⟩` — the product goal
  becomes literal `0 * 0 * 0 = 0`.
- Real module elaborates in 1.9s; TARGETED BUILD GREEN:
  `lake build D0.Foundation.CanonicalSelectorNoGo` -> "Built D0.Foundation.CanonicalSelectorNoGo
  (2.5s); Build completed successfully (2946 jobs)".
- #print axioms (scratchpad/AxiomsCheckSelector.lean): NO sorryAx anywhere.
  fixed_forces_all_identity / no_fixed_labeling / no_equivariant_section / scene_zones_no_section
  = [propext, Classical.choice, Quot.sound] ONLY. canonical_within_zone_selector_nogo + the four
  n<=4 concrete checks additionally carry their auto-generated `*._native.native_decide.ax_1_1`
  evaluator axioms (repo precedent: 17 modules use native_decide). Source grep
  sorry/admit/axiom = clean.

### Step 1.4 — registry flip + regen + guards (COMPLETE)

- Aggregates regen #1 (post-green): All.lean gained `import D0.Foundation.CanonicalSelectorNoGo`.
- 053040 re-check at flip time: 0 occurrences in CLAIM_TO_LEAN_MAP.csv. Row 549
  D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 flipped surgically (count==1 asserted
  replacements, all other fields verbatim):
    lean_module  "" -> D0.Foundation.CanonicalSelectorNoGo
    lean_theorem "" -> canonical_within_zone_selector_nogo
    lean_status  PYTHON_CERTIFIED -> LEAN_PROVED
    notes clause "COMPILE PENDING (build-infra flaky this session), so lean_status stays
    PYTHON_CERTIFIED not LEAN_PROVED until a green lake build" -> "compiled green 2026-07-05"
    (string per coordinator instruction; NOTE: the actual green build timestamp is 2026-07-06
    00:5x MSK — one-day cosmetic discrepancy, recorded here for honesty).
- Aggregates regen #2 (post-flip): ClaimMap.lean row 846 now carries the claim with
  moduleName D0.Foundation.CanonicalSelectorNoGo. Targeted build of D0.All +
  D0.TheoremLedger.ClaimMap + D0.TheoremLedger.ActiveClosureIndex: GREEN,
  "Build completed successfully (4011 jobs)" (+1 vs the 4010 of the CVFT lift wave = this module).
- sync_theory_status_map.py: "Synced 545 claims into 03_THEORY_MAP" (generated files only,
  source CSV is the single edit point, per registry discipline).
- Guards, all PASS:
    vp_status_inflation_audit.py ........ PASS_STATUS_INFLATION_AUDIT (545 claims, 0/0/0)
    check_no_sorry_in_core.py (+ --all) . PASS
    check_claim_map_coverage.py ......... PASS
    check_no_dangling_lean_module.py .... PASS (0 new dangling)
- TASK 1 LANDED.

---

## FINAL — per-task status + guard board

- TASK 1 (CanonicalSelectorNoGo compile + registry flip): **LANDED.**
  Root cause of both hangs (2.5h + 21min): kernel forced to normalize a symbolic
  `(equivariantSections n).card` inside Nat arithmetic => enumerate Perm(Fin 11) in-kernel;
  second independent hazard: kernel `decide` on the Equiv-Fintype instance at ANY n (now
  native_decide, n<=4 only); third latent bug: filter_eq_empty_iff needed the def unfolded.
  Module builds in 2.5s; D0.All 4011 jobs GREEN; #print axioms: no sorryAx (core lemmas
  standard-axioms-only; flagship + small-n controls carry their native_decide evaluator
  axioms, repo precedent). Row 549 = LEAN_PROVED.
- TASK 2 (retirement banners on 4 fake CVFT certs): **LANDED.** Banner first line of main(),
  concrete REFORGED successor named, exit codes + content untouched, all 4 verified by run.
- TASK 3 (evidence-matrix + final-claim-index REFORGED swap): **LANDED.** Both CSVs adjudicated
  HAND-MAINTAINED (no writer in repo; readiness cert only reads). Rows 136/139 in both files
  now cite the REFORGED certs, mirroring registry rows 137/140.
- TASK 4 (check_book_ledger_sync demoted-row closure-prose class): **LANDED.**
  [DEMOTED-CLOSURE-PROSE] fatal class added; acceptance test EXACT: 1 flag =
  D0-SPECTRAL-EINSTEIN-001 (CORE_BRIDGE_SPLIT) in 0043__07.41__trace-heat-capacity-gravity.md:49
  (assembled BOOK_07:~1780), 0 spurious after the accepted lean-side-exempt tightening.

Guard board (2026-07-06):
  vp_total_publication_readiness.py ...... PASS (exit 0)
  vp_status_inflation_audit.py ........... PASS (545 claims)
  check_no_sorry_in_core.py / --all ...... PASS
  check_claim_map_coverage.py ............ PASS
  check_no_dangling_lean_module.py ....... PASS
  lake build D0.All ...................... GREEN (4011 jobs)
  check_book_ledger_sync.py .............. RED (exit 1) BY DESIGN: 1 legitimate
    DEMOTED-CLOSURE-PROSE flag on the BOOK_07 Einstein passage; stays red until the
    separate BOOK_07 prose repair lands. No allowlist suppression added (intentional).

No git commit made anywhere (per batch constraint). 053040 never touched (absent from all
edited files, re-checked before every CSV write).
