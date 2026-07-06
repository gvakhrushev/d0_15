# W7 — FINAL GATE (uplift sweep, wave 7)

Serial log, written incrementally. Constraints honored: NO git commit (owner-only), 053040
never touched, registry row 549 verdict/content NOT changed (certs are secondary evidence
behind the LEAN_PROVED row; hardening only).

## Task 1 — cert-can-fail hardening of the 4 selector no-go certs

### 1.0 Guard criterion (read first)

`tools/check_cert_can_fail.py` scans every registered `vp_*.py` line-by-line for
FAIL_EVIDENCE = `^\s*assert\s` | non-entrypoint `raise` | `sys.exit(1)` | `ok = False` |
`else 1` | `return 1`, SKIPPING docstring blocks with a crude line-based `"""` toggle
(a line that *starts* with `"""`, odd quote count, len>3 toggles `in_doc`).

### 1.1 Root cause on the 4 selector certs (diagnosed before editing)

All 4 certs DO end in a conditional non-zero exit, but the guard never sees it:

- `vp_selector_obstruction_nogo.py:108` — inner docstring `"""Every S_n-invariant...`
  opens at line-start, closes MID-line (`...constant)."""`) → `in_doc` stuck True →
  the `raise SystemExit(1)` at :212 is skipped.
- `vp_selector_ssb_nogo.py:453` — the closing `""")` of the final `print("""...` verdict
  block toggles `in_doc` True → the `sys.exit(0 if FAIL == 0 else 1)` at :454 is skipped;
  no `assert` anywhere before it.
- `vp_selector_dynamical_nogo.py:80` — docstring of `commutes_with_all_perms` opens at
  line-start, closes mid-line → everything after skipped, incl. `sys.exit(... else 1)`.
- `vp_selector_basepoint_nogo.py:95` — docstring of `orbit_of_vertex_under_stab` same
  pattern → `sys.exit(1)` at :177 skipped.

Additionally the guard's summary shows `4 missing-on-disk` (pre-existing, non-blocking:
missing certs are reported but do not fail the guard; carried on the wave-2 ledger).

Fix direction chosen per task: harden the CERTS (not the guard) — genuine computed
negative controls that can fail the CONCLUSION, `assert`-grade gating (which also gives
the guard unambiguous FAIL_EVIDENCE at line-start), parser-hostile inner docstrings
converted to `#` comments (cosmetic only). Verdicts unchanged.

### 1.2 Hardening applied (verdicts UNCHANGED — row 549 secondary evidence intact)

Each cert got (i) parser-hostile inner docstrings converted to `#` comments (cosmetic),
(ii) a GENUINE computed negative control that can fail the CONCLUSION, with `assert`
gating and a `NEGATIVE_CONTROL_CAUGHT` token printed only from computed values:

- `vp_selector_obstruction_nogo.py` — section counter refactored to a SHARED
  `count_fixed_bijections_under(group, n)` code path; control = the SAME count on the
  TRIVIAL group {id} (free orbits of size 1) for n=2,3: must find n! > 0 sections
  (computed 2 and 6). Plus a group-action law gate on `act` (composition + identity
  asserts). 25/25 → **27/27 PASS, exit 0**.
- `vp_selector_ssb_nogo.py` — NC5: NON-transitive action H = Stab(vertex 0) < S9
  (orbits {0}, {1..8} both computed) with H-invariant potential p = 1 − 1_{v0}: the same
  extremum analysis finds a UNIQUE (computed argmin) NON-S9-symmetric (computed orbit
  size 9) minimizer — outcome (c) reachable. 26/26 → **29 PASS / 0 FAIL, exit 0**
  (28 checks pre-NC5 incl. the 3 scene-invariant checks; NC5 adds 1).
- `vp_selector_dynamical_nogo.py` — NEG-CONTROL-4b: a T genuinely COUPLED to the
  spatial lattice (distinct per-vertex rational contraction weights on zone 9); exact
  Fraction flow iteration ×64 from the uniform state; attractor selects vertex 0 with
  computed share 0.999468 > 0.99; the coupled diagonal fails the SAME
  `commutes_with_all_perms` test the owned uniform tick passes. 10/10 → **12/12, exit 0**.
- `vp_selector_basepoint_nogo.py` — all-zones control graph (ω₀—("9",1) within-zone
  edge; ω₀→zone-11 only ("11",0); ω₀→zone-13 only ("13",0)); computed |E|=338; the same
  transposition-generator orbit machinery finds PROPER orbits in ALL THREE zones
  (computed 1/8, 1/11, 1/13). 4/4 → **8 checks PASS, exit 0**.

NOTE (owner): row-549 notes cite the old per-cert check counts (25/25, 26/26, 10/10,
4/4); counts are now 27/27, 29, 12/12, 8. Verdicts identical; note-count refresh is a
registry edit = owner-gated, queued in the final report.

### 1.3 Mutation tests — 2 per cert, all 8 flip exit 0 → 1

Copies in scratchpad (`mut/`), mechanical sed mutations, never touching the originals:

| cert | mutation | result |
|---|---|---|
| obstruction M1 | `act()` → identity action | exit 1 (NO_EQUIVARIANT_SECTION_n* fail) |
| obstruction M2 | counter `fixed += 1` → `+= 0` | exit 1 (trivial-group control catches rigged counter) |
| ssb M1 | adjacency → complete graph | exit 1 (scene invariants fail) |
| ssb M2 | NC5 potential flattened | exit 1 (NC5 check + assert fire) |
| dynamical M1 | owned tick made non-uniform | exit 1 (commutation checks fail) |
| dynamical M2 | coupled control made uniform | exit 1 (4b control catches it) |
| basepoint M1 | adjacency rule inverted | exit 1 (SCENE_INVARIANTS fails) |
| basepoint M2 | control's within-zone edge deleted | exit 1 (edge-count assert + all-zones control fire) |

### 1.4 Gate re-run

- All 4 certs re-run: **exit 0** each, PASS tokens present (runner-compatible:
  exit 0 + "PASS" in stdout per tools/run_registered_certs.py).
- `tools/check_cert_can_fail.py`: **PASS** — "393 registered certs; 0 print-stub(s),
  0 unallowed; 4 missing-on-disk", exit 0.
- The 4 missing-on-disk (non-blocking, guard passes): `gap_w_witness_check.py`,
  `m2_phase_labeling_check.py`, `torsor_gauge_check.py`, `window_forcing_check.py` —
  all four EXIST in `_TASKS_CENTER_ATTACK/`, awaiting owner promotion into `05_CERTS/`
  per VERIFIED_CLOSURE_PROTOCOL (already flagged in row 550 notes). → owner queue.

## Task 2 — FULL battery (final gate board)

Run 2026-07-06, macOS, python3, 120s/guard timeout (Python wrapper; coreutils `timeout`
absent on darwin).

- **53/53 `tools/check_*.py` guards: ALL PASS. Zero FAIL.**
  - 52 run directly (incl. `check_cert_can_fail.py`, now PASS: "393 registered certs;
    0 print-stub(s), 0 unallowed; 4 missing-on-disk").
  - `check_lean_builds.py` run after the lake build: PASS ("lake build D0.All is green").
  - W6 board was 51 PASS / 1 SKIP(lake) / 1 FAIL(cert_can_fail) → W7 board is **53 PASS /
    0 SKIP / 0 FAIL**. The last real gate FAIL of the sweep is cleared.
- `cd 09_LEAN_FORMALIZATION && lake build D0.All` (foreground):
  **Build completed successfully — 4011 jobs**, `[4011/4011] Built D0.All`. Green.
- `tools/generate_lean_aggregates.py --check`: **PASS (aggregates idempotent)**.
- `tools/sync_theory_status_map.py` regen-check: re-ran the generator; md5 of
  `theory_status_map.csv` + `theory_graph.json` identical before/after
  ("Synced 546 claims") → **IDEMPOTENT, no drift** vs the canonical
  CLAIM_TO_LEAN_MAP.csv. (Pre-existing uncommitted working-tree deltas in
  03_THEORY_MAP/ from earlier waves left untouched; no git commit — owner-only.)

## Task 3 — FINAL SWEEP REPORT written

`_TASKS_CENTER_ATTACK/UPLIFT_SWEEP_FINAL_REPORT.md` — the architecture scoreboard:
(a) 8 principles/organizing objects on record (1 MINTED: row 550 organizing lemma,
OPEN/PROOF-TARGET; CAP clause computed with six-face table + REQUIRED clause; the rest
un-minted candidates with rosters); (b) negative-object ledger counted programmatically:
84 no-gos = 38 UPLIFT/instance-of annotated (`UPLIFT[` 32 · `T1-UPLIFT` 6 · `instance-of`
19 · `corollary-of` 8, overlapping) + 4 genuine-boundary (W0 roster) + 42 still-flat
(mostly the T6 fan + T5 interface cluster whose classifications live in UPLIFT_MAP/W5,
not yet in row notes — deliberate, follow-on batch is owner-gated); (c) 8-entry honest-
boundary roster + W5 counts (N=12 inputs, 22 ASSUMP ids, M=16 outputs, 39 bridge rows);
(d) consolidated owner-decision queue = **20 items**; (e) final gate board all green.

## W7 FINAL BOARD

- 53/53 guards PASS (0 FAIL, 0 SKIP) — cert-can-fail cleared by Task 1
- lake build D0.All: green, 4011/4011 jobs
- generate_lean_aggregates --check: PASS · sync_theory_status_map regen: idempotent (546)
- 4 selector certs: exit 0, verdicts unchanged, 8/8 mutations flip, guard PASS
- No git commit · 053040 untouched · registry statuses untouched
