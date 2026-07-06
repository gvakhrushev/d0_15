# SELECTOR NO-GO MINT LOG

Minting: D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001
Protocol: VERIFIED_CLOSURE_PROTOCOL, protocol-guarded with back-out.
Concurrency rule: NEVER touch any CLAIM_TO_LEAN_MAP.csv / LEAN_ASSUMPTION_LEDGER row containing "053040".
No git commit.

---

## Step 0 — recon (in progress)

- Located VERIFIED_CLOSURE_PROTOCOL.md at 04_VERIFICATION/VERIFIED_CLOSURE_PROTOCOL.md — read.
- Located D0_CLAIM_CLOSURE_CONTRACT.md at repo root — read. Allowed closure status token = `NO-GO-CLOSED`.
- Read all 4 memos + 4 scripts + SELECTOR_MECHANISM_REPORT.md.

## Step 0 findings (recon complete)

- Core theorem-grade fact for Lean: S_n acts FREELY-TRANSITIVELY on Bij(V_n,L_n); count of S_n-fixed bijections = 0 for n>=2 (invariant fn constant on single vertex-orbit => not injective). n=1 control = 1 section. Joint over S9xS11xS13 = product => 0.
- Script run results (2026-07-05):
  - selector_obstruction_check.py: exit 0, 25/25 PASS. OK.
  - selector_dynamical_check.py: exit 0, 10/10 PASS. OK.
  - selector_basepoint_check.py: exit 0, 4/4 PASS. OK.
  - selector_ssb_check.py: **exit 1, 26 PASS / 2 FAIL**. NOT 26/26 as task stated.
    The 2 FAILs are the supplementary Reynolds-averaged general-commutant checks (lines 271-276):
    400 random samples of a group of order ~1e19 => Ugen is APPROXIMATE, not exact commutant
    element => commutes=False, ||P Ugen Q||~0.50 = sampling noise. Documented as EoR-A in
    SELECTOR_MECHANISM_REPORT.md:95. The LOAD-BEARING F2 no-go (class-function trichotomy, exact
    equivariant-poly-in-L check) stands; these 2 are non-load-bearing supplementary diagnostics.
  - RESOLUTION NEEDED: a cert copied to 05_CERTS/ must exit 0 (register/cert-can-fail guards). Will
    fix the copied vp_selector_ssb_nogo.py to make the general-commutant witness EXACT (build the
    exact block projector / Reynolds over exact generators) rather than 400-sample approximate, per
    EoR-A's recommended fix. Will NOT alter the load-bearing checks. Log the diff.

## Step 1 — Lean module (in progress)

- Read neighbouring style: CarrierNotIcosahedral.lean (native_decide on Finset.univ.filter(...).card),
  Q8Anisotropy.lean (decide over Fin/ZMod), M1Predicate.lean (namespace D0.Foundation).
- Aggregation: D0/All.lean is AUTO-GLOB (generate_lean_aggregates.all_modules() rglobs D0/**/*.lean),
  so a new module auto-imports on regen; ClaimMap.lean is CSV-driven.
- DESIGN: labelings of zone V_n = Equiv.Perm (Fin n). S_n acts g•b = b ∘ g⁻¹. An Aut-equivariant
  section is a b fixed by ALL g. Count of such fixed b:
    * abstract theorem: b∘g⁻¹ = b ∀g ⇒ g = id ∀g ⇒ for n≥2 (∃ non-id g) contradiction ⇒ 0 sections.
    * concrete decidable surrogate (matches selector_obstruction_check.py): card of fixed set = 0 for
      n=2,3,4 via decide/native_decide; = 1 for n=1 (control, a section exists).
  Theorem name: canonical_within_zone_selector_nogo. Writing module now.
- WROTE 09_LEAN_FORMALIZATION/D0/Foundation/CanonicalSelectorNoGo.lean (namespace
  D0.Foundation.CanonicalSelectorNoGo). Key theorems:
    * equivariantSections n : Finset (Perm (Fin n)) filter of b fixed by all g (b.trans g⁻¹ = b).
    * control_n1_has_section : card = 1 (decide) — the n=1 control (section exists).
    * no_section_n2/n3 : card = 0 (decide); no_section_n4 : card = 0 (native_decide).
    * fixed_forces_all_identity : b fixed ⇒ ∀ g, g = 1 (abstract).
    * no_equivariant_section (2 ≤ n) : card = 0 (general, via swap 0 1 ≠ 1 contradiction).
    * scene_zones_no_section : n=9,11,13 each have no fixed b.
    * canonical_within_zone_selector_nogo : 9/11/13 counts = 0, product = 0, n=1 control = 1.
  Style matches CarrierNotIcosahedral (Finset.univ.filter card, native_decide) + Q8Anisotropy (decide).
- lake build D0.Foundation.CanonicalSelectorNoGo running (background, mathlib compile in progress).

## Step 2 — certs (COMPLETE)

- Copied 4 scripts to 05_CERTS/:
    vp_selector_obstruction_nogo.py (direct copy) — exit 0, 25/25 PASS.
    vp_selector_dynamical_nogo.py  (direct copy) — exit 0, 10/10 PASS.
    vp_selector_basepoint_nogo.py  (direct copy) — exit 0, 4/4 PASS.
    vp_selector_ssb_nogo.py        (FIXED copy)  — exit 0, 28 PASS / 0 FAIL.
- SSB FIX (per SELECTOR_MECHANISM_REPORT.md EoR-A): replaced the 400-sample reynolds_average
  (which left Ugen a NON-exact commutant element ⇒ 2 sampling-noise FAILs) with an EXACT Reynolds
  projector onto the S9xS11xS13 commutant (closed-form per-(zone-pair, diag/offdiag) mean fill),
  seeded asymmetrically. Result: Ugen genuinely non-symmetric (||Ugen-Ugen^T||=79.97) AND exactly
  in the commutant (commutes=True), so PUQ=0 exactly (5.77e-14). NO load-bearing check altered; the
  class-function F2 no-go and the exact equivariant-poly-in-L checks are untouched. Diff is confined
  to the two supplementary general-commutant checks (lines ~251-276 of the original).
- can-fail guard: all 4 certs have assert/sys.exit(1)/else-1 machinery (verified against
  check_cert_can_fail FAIL_EVIDENCE regex — all CAN-FAIL). STRUCTURE_FIXED_BEFORE_NUMBER marker not
  required for these (check_structure_before_number.py gates only a fixed 6-cert holonomy batch).

## Step 3/4 — staged (pending Lean build green)

- CSV schema (11 cols): claim_id,book,section,lean_module,lean_theorem,lean_status,
  uses_bridge_assumptions,assumption_ids,python_cert,release_status,notes
- 053040 token: ABSENT from the entire CLAIM_TO_LEAN_MAP.csv and LEAN_ASSUMPTION_LEDGER.csv
  (grep -c = 0). No concurrency collision possible; will still avoid any such row if one appears.
- Row to APPEND (matches DSIGMA/REPRESENTATION NO-GO format exactly):
    claim_id = D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001
    lean_module = D0.Foundation.CanonicalSelectorNoGo
    lean_theorem = canonical_within_zone_selector_nogo
    lean_status = LEAN_PROVED ; release_status = NO-GO ; uses_bridge_assumptions = False
    python_cert = vp_selector_obstruction_nogo.py;vp_selector_ssb_nogo.py;vp_selector_dynamical_nogo.py;vp_selector_basepoint_nogo.py
- Frontier rows to annotate (Step 4, notes-only cross-ref, NO status flip). Confirmed statuses:
    * D0-WINDOW-9-13-DISSOLVE-001                          PROOF-TARGET  -> annotate (GAP-E)
    * D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001               PROOF-TARGET  -> annotate (lane-A Dirac/triple)
    * D0-VNEXT2-ENDPOINT-CONDITIONAL-EXPECTATION-OWNER-001 PROOF-TARGET  -> annotate (lane-A, PRIM-SCENE-HISTORY-REFINEMENT-RULE)
    * D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001              PROOF-TARGET  -> annotate (lane-A Xi lift)
    * Rule-R / membership row: DOES NOT EXIST as a registry row (RULE_R_MEMBERSHIP_MEMO.md is a memo
      only). -> HELD (nothing to annotate).
    * Already-terminal lane-A rows (D0-VNEXT-MARTINGALE-DIRAC-OWNER-001 NO-GO,
      D0-VNEXT2-SCENE-XI-INTERTWINER-OWNER-001 NO-GO, D0-VNEXT2-SCENE-FINGERPRINT-OWNER-001
      CERT-CLOSED): NOT frontier rows; leaving untouched (annotating a closed row risks a guard and
      is a separate owner decision).
  All 4 annotate-targets confirmed 053040-free.

## Step 1 build — RESTART (2026-07-05)

- First background build process was terminated (session cleanup on an earlier interrupt); no .olean,
  empty log, no error. NOT a compile failure — just a lost process.
- Restarted: lake build D0.Foundation.CanonicalSelectorNoGo -> /tmp/lean_build2.log (markers:
  BUILD_STARTED at head, DONE exit=N at tail). Fresh mathlib module ~10-15 min is normal.
- Module source confirmed clean: grep -nwE "sorry|admit|axiom" = NONE; no ":= True" shells.
- WAITING for build to finish before appending the registry row (mint gated on green build).

## Compile diagnosis (2026-07-05, main loop)
- lean worker ran ~2.5h on the module without finishing; killed. Hypothesis: a `decide`/`native_decide` term explodes combinatorially (any decidable instance touching Perm(Fin n) for n>=5-6 in kernel mode). The registry row 549 correctly stays PYTHON_CERTIFIED. FIX PATH (later): route ALL concrete instances through the general lemma `no_equivariant_section` (proved via fixed_forces_all_identity, no decide) and keep decide only for n<=4; then targeted build should take minutes.
