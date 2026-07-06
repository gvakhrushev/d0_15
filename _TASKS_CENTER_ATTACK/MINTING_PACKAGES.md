# MINTING PACKAGES — three post-skeptic center-attack candidates (PROPOSALS, not applied)

**Status:** DRAFT proposal ledger. **No registry row edited, no cert minted, no `.lean` added to the built tree.**
Every proposed row below is a *memo-only* proposal; the exact source-edit + regen commands are given (§ "Source-edit + regen") but **DELIBERATELY NOT RUN**. Lean drafts referenced here already live as code blocks inside the three source memos; none is added to `09_LEAN_FORMALIZATION`.

**Inputs located and read (owned file:line where load-bearing):**
- Protocol: `04_VERIFICATION/VERIFIED_CLOSURE_PROTOCOL.md` (Phases 0–6; Verify-then-build rule; PROOF-TARGET rows use `lean_status = OPEN`, `:51`).
- Contract: `D0_CLAIM_CLOSURE_CONTRACT.md` — allowed closure statuses (`:14-22`), forbidden list (`:5-12`: "`bridge` is not a positive closure status", "`CONDITIONAL-CLOSED` as a status upgrade" is FORBIDDEN, "`external theorem applies` without proof that all external hypotheses hold" FORBIDDEN), reduction statuses (`:24-31`), the Rule (`:33-39`: "Any remaining bridge is a proof obligation"), development/release split (`:55-84`).
- Memos: `M2_PHASE_LABELING_MEMO.md` v2, `GAP_W_WITNESS_MEMO.md` v2, `WINDOW_9_13_FORCING_MEMO.md`.

**Registry schema (verified, header `CLAIM_TO_LEAN_MAP.csv:1`):**
`claim_id,book,section,lean_module,lean_theorem,lean_status,uses_bridge_assumptions,assumption_ids,python_cert,release_status,notes`
(NB: the task brief lists the columns in a different order; the CANONICAL on-disk order is the one above — `uses_bridge_assumptions` and `assumption_ids` sit *before* `python_cert`, and `release_status` sits *before* `notes`. Proposed rows below follow the on-disk order.)

**Registry is source-of-truth** (`tools/sync_theory_status_map.py:11` reads `CLAIM_MAP`; `:295-475` writes `theory_status_map.csv`/`theory_graph.*` — the generated files, never edited by hand). Confirmed against MEMORY.

---

## Vocabulary decision (binding, from the contract)

The contract **forbids** `CONDITIONAL-CLOSED` as a status (`D0_CLAIM_CLOSURE_CONTRACT.md:8`) and forbids `bridge` as a positive closure (`:3`). Therefore a candidate that narrates a joint/G_res/named-gap **must not** carry a closure status. Two honest registry shapes exist for such candidates, both already in use on-disk:

1. **PROOF-TARGET** — `lean_status = OPEN`, `release_status = PROOF-TARGET`, residual stated with the on-disk **`EXACT-MISSING:`** grammar (protocol `:50-51`; e.g. rows `D0-CVFT-F6`, `D0-EDGE-002`, `D0-QUANT-MET-003`). Used when the honest object is not yet Lean-closed.
2. **BRIDGE-ASSUMPTIONS-EXPLICIT** — `lean_status = LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, `uses_bridge_assumptions = True`, `assumption_ids = <ledger ids>`, `release_status = BRIDGE-ASSUMPTIONS-EXPLICIT`. Used ONLY when a real Lean theorem is built with the joints isolated as *explicit Lean hypotheses* registered in `LEAN_ASSUMPTION_LEDGER.csv` (e.g. rows `D0-RG-001`, `D0-QM-BORN-001`). Per the contract this is a *reduction*, not a closure — the ledger row states the failure meaning.

**Neither candidate below is eligible for a bare closure status** (`LEAN-THEOREM-CLOSED` / `CERT-CLOSED` / `NO-GO-CLOSED` / etc.) on its *full headline claim*, because all three headlines carry narrated joints. Where a *narrow sub-part* is genuinely closable (M2's Fourier pre-owner already CORE; GAP-W's decidable freeness lemma; Route B's zero-hypothesis chain theorem), that sub-part is called out separately and can carry a real status — but it is NOT the candidate's headline.

**Over-claim guard (binding):** "mint-ready NOW" below means *only* that a PROOF-TARGET / reduction row can be added truthfully today. It NEVER means the headline forcing is closed. All three headlines remain candidate/DRAFT.

---

## Candidate 1 — M2 (phase-labeling of the detector-layer pointed shell V₉)

**Source:** `M2_PHASE_LABELING_MEMO.md` v2 (skeptic #1: SURVIVES; companion `m2_phase_labeling_check.py`, 50/50 PASS — file present, `12320`-byte sibling, `01:12`).

### What is actually being claimed (three separable objects)

The memo bundles a POSITIVE, a NEGATIVE, and a CONSUMER result. They mint differently:

- **X1 (positive, torsor):** the owned data forces a labeling ℓ: V₉ → Q₈ ⊔ {∗} **canonical only up to G_res**, where G_res ∈ {1, V₄, (ℤ/2)³} depending on an **un-adjudicated 3-way reading** (memo `:41-51`; A3 risk `:238-243`). The reading adjudication is explicitly NOT made (`:261`, "no 'G_res = V₄' headline is claimed").
- **X2 (negative, impossibility):** no canonical cyclic (μ₉/μ₈) labeling of V₉ exists from owned data — three computed walls (`:53-68`). This is a NO-GO-shaped result.
- **X4 (consumer split):** all spectral-tick consumers are G_res-invariant AND torsor-invariant (`:79-83`); per-slot (M2-membership) consumers are NOT torsor-invariant and need a graph-bridge C1 forbids resolving.

**Pre-ownership wound W1 (accepted, `:281-285`):** the E₀/E₃/E₄ Fourier system on ℂ[Q₈] is ALREADY `D0-Q8-TERMINAL-FOURIER-001` (CORE-FORMALIZED, verified on-disk: `q8_terminal_fourier`, `D0.UnifiedFiniteCore.Q8Terminal`, ranks (1,4,3)). The genuinely-new remainder is narrowed to {pointed-shell extension ℂω₀⊕…, std₉-refinement statement, reading-independence packaging, carrier application}. **None of that remainder has a Lean module.**

### Proposed registry row(s) — PROOF-TARGET (no Lean module exists)

The headline (X1 torsor "forced up to G_res") carries the un-adjudicated reading as an OPEN joint; there is no `.lean` for the pointed-shell extension. Honest shape = PROOF-TARGET with `EXACT-MISSING`.

```csv
D0-M2-PHASE-LABELING-V9-SHELL-001,BOOK_01,01.7/01.8 detector-layer pointed shell,,,OPEN,False,,m2_phase_labeling_check.py,PROOF-TARGET,"[center-attack M2 v2 candidate; skeptic#1 SURVIVES] Owned labeling of the DETECTOR-LAYER pointed shell V9=Omega8 ⊔ {omega0} into Q8 ⊔ {*} is FORCED ONLY UP TO a residual group G_res ∈ {1 (R-strong), V4 (R-mid), (Z/2)^3 (R-weak)} — the 3-way reading is UN-ADJUDICATED (JOINT, not closed). Companion m2_phase_labeling_check.py 50/50 (fraction-exact tick fingerprint {80/81,|ratio|=1/9}). PRE-OWNER cited not duplicated: the E0/E3/E4 Fourier idempotents on C[Q8] (ranks 1,4,3) are D0-Q8-TERMINAL-FOURIER-001 (CORE). Cross-ref D0-OMEGA8-CENTER-001, D0-Q8-DEDEKIND-MINIMALITY-001, D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001 (per-vertex analogue, computed independently). EXACT-MISSING: (1) a Lean module for the pointed-shell extension C^{V9}=C.omega0 ⊕ (E0⊕E3⊕E4) with the std9-refinement statement and reading-independence (all four block projectors (Z/2)^3-invariant); (2) the R-strong/mid/weak reading adjudication (JOINT G_res); (3) transport of the labeling onto K(9,11,13) graph slots is the UN-OWNED torsor datum (C1-forbidden internally, memo X4). No closure status: joints narrated."
```

Optional companion NEGATIVE row for X2 (the μ₉ impossibility) — ALSO PROOF-TARGET, because the three walls are computed in the companion script but **have no Lean no-go module**; a `NO-GO` release_status requires a formal no-go theorem (contract `:12`: "negative controls passed without a stated failure theorem" is FORBIDDEN):

```csv
D0-M2-NO-CANONICAL-CYCLIC-LABELING-V9-001,BOOK_01,01.7/01.24 impossibility branch,,,OPEN,False,,m2_phase_labeling_check.py,PROOF-TARGET,"[center-attack M2 v2 candidate] NO canonical cyclic (mu9/mu8, Z/9 or Z/8) per-vertex labeling of V9 exists from owned data — three COMPUTED walls: (i) type wall (Q8 exponent 4, no order-8 element); (ii) relation wall (typed partition A/B/C/D, no successor order; emission orbit-averaged over G8, BOOK_01:1996); (iii) invariance wall (under R-mid/R-weak G_res has 2-elt orbits so no bijective phase labeling is statable). Companion controls CTRL_NO_ORDER8, MU9_NO_INVARIANT_BIJECTION. EXACT-MISSING: a formal NO-GO Lean theorem (e.g. no_canonical_cyclic_labeling) discharging the three walls by decide/Fintype — the walls are script-computed, not Lean-proved, so this is NOT NO-GO-CLOSED (contract forbids negative-controls-as-closure). Adjacent NO-GO owner (different object, cross-ref only): D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001."
```

### RELEASE-gate checklist (contract §"Required release loop" `:68-75`; protocol Phase 6 `:53-54`)

| gate step | M2 X1/X2 status |
|---|---|
| build `HardClosureTheoremIndex` | **N/A / FAILS** — no Lean module exists to build. |
| run all hard certificates | companion `m2_phase_labeling_check.py` is a **memo-sibling script**, NOT a registered `05_CERTS/vp_*.py` cert; not in the hard-cert set. Protocol Phase 4 (`:41-46`) requires `STRUCTURE_FIXED_BEFORE_NUMBER:` first line + reachable `FAIL_*` — not verified here (script not read line-by-line; would need audit before registration). |
| check claim-map coverage | proposed rows have empty `lean_module`/`lean_theorem` (PROOF-TARGET) — coverage-valid as OPEN, but contributes no proved theorem. |
| no forbidden `sorry`/`axiom`/`Float` in protected layers | **N/A** (no Lean). Script uses `fractions.Fraction`; floats demoted to 1e-9 corroboration (memo `:209-213`) — acceptable for a script, not gate-scored. |
| rebuild release ledger | nothing to add (no theorem). |

**Verdict: needs-module (PROOF-TARGET-mintable NOW).**
- **NOT LEAN-CLOSED**, **NOT eligible for CONDITIONAL/BRIDGE-ASSUMPTIONS-EXPLICIT** (there is no built Lean theorem to attach the G_res joint to as an explicit hypothesis).
- **Mint-ready NOW** only as the two **PROOF-TARGET** rows above (registry proposal), which honestly record: X1 forced-up-to-G_res, X2 computed-not-proved, the un-adjudicated reading + graph-bridge as `EXACT-MISSING`.
- **Upstream needed to upgrade** beyond PROOF-TARGET: a Lean module `D0.<...>.M2PhaseLabeling` proving (a) the pointed-shell decomposition `ℂ^{V₉} = ℂω₀ ⊕ E₀ ⊕ E₃ ⊕ E₄` with dims 1+1+3+4 reusing `D0.UnifiedFiniteCore.Q8Terminal`, and (b) reading-independence (projectors (ℤ/2)³-invariant, `decide`-able). Even then the **reading adjudication stays a joint** → the row could at best become `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` with an `ASSUMP-M2-READING` ledger entry (G_res selection), NEVER a bare closure. The μ₉ NO-GO could reach `NO-GO` release_status only with a formal no-go theorem.

**Conservatism note:** do NOT mint a `NO-GO` row for X2 today (walls are script-computed); do NOT mint `CORE-FORMALIZED` for X1 (joint narrated — forbidden by contract `:8`). The Fourier pre-owner is CITED, never re-minted (W1).

---

## Candidate 2 — GAP-W (the witness "+1": |V_base| = |Ω₈| + 1 = 9)

**Source:** `GAP_W_WITNESS_MEMO.md` v2 (skeptic #1: **WOUNDED → repaired**, all wounds accepted in full; verdict "WOUNDED, not killed"). Companion `gap_w_witness_check.py` 10/10 (present, `01_TASKS` sibling). This is **OB-1 of Route B** (candidate 3).

### What is actually being claimed

`|V_base| = |Ω₈| + 1 = 9` is **FORCED GIVEN THREE NAMED JOINTS** (memo verdict `:9`, `:171-177`):
- **W-BRIDGE-1′** — the contract's *stable re-detection class* (`BOOK_01:1166.5`) realized as **≥ 1** stationary marked base element; narrated ×3 (A1 `:1541`, A2 `:1987-1990`, A3 `:1993`). The halt-QUOTIENT is contract-owned (`:296`/`:366.5`) BUT the **halt-proper lands at +0** in two owned adverse texts (`:846`, `:858`) — so the +1 rides the re-detection sliver ONLY (skeptic wound E-GW-1).
- **W-T1** — CASE-2 copy-catalogue schema instantiated on marks (Lean arithmetic `repeat_has_nontrivial_copy_symmetry` owned; instantiation NAMED; `:1556` does NOT back this branch — S3).
- **W-BIT** — `BOOK_01:1539`'s no-further-bit quote **scope-transferred** from Ω₈-construction to labels on adjoined marks; load-bearing by toggle (E-GW-2).

**Honest scope declared upfront by the memo itself (`:19`):** "It does not claim GW is Lean-proved; the Lean skeleton (§IV) enumerates what would be." The memo's own §VI: "It does NOT prove `card_base_forced` unconditionally in Lean; the THREE joints are named hypotheses" (`:289`).

### What IS genuinely Lean-closable (the narrow parts) vs the headline

| piece | Lean status | verdict |
|---|---|---|
| OB-W0 `base_card_arith : card V9 = card Omega8 + 1` | **OWNED reuse** (`card_v9`, `card_omega8`/`omega8_cardinality`, D0-OMEGA8-001) | already owned; not new content |
| OB-W1 `no_stationary_in_omega8` (`∀ k≠0, x+k≠x` on Fin 8) | **NEW-decidable** (`decide`); model owned (`WitnessHalting.shiftMat`) | genuinely new, honestly closable |
| OB-W2 `first_instance_canonical` (|S₁|=1, no-overfire) | **OWNED reuse** (`NoExtension.lean:52`) | owned; NOT a V10-killer (memo D2/ATT-2 — precision correction) |
| OB-W3 `repeat_has_nontrivial_copy_symmetry` (|S₂|>1) | **OWNED reuse** (`NoExtension.lean:47`) | owned; instantiation-on-marks = W-T1 joint |
| OB-W4 = W-BRIDGE-1′ | **NAMED joint** (narrated; +0 adverse texts) | NOT Lean-owned |
| OB-W5 = W-BIT | **NAMED joint** (scope-transfer) | NOT Lean-owned |
| capstone `card_base_forced_conditional (m) (h_halt:1≤m)(h_nocopy:m<2)` | conditional shell, joints as hypotheses; **the arithmetic is trivial by design** (`rw;omega`) | this is the BRIDGE-ASSUMPTIONS shape — but NOT YET BUILT |

The capstone theorem is honest precisely because it is **trivial**: "all forcing content lives in the named joints, none is hidden in the proof" (memo `:250-251`). That is the correct design for a BRIDGE-ASSUMPTIONS-EXPLICIT row — but the module is **memo-only, not in the built tree** (`:196`, `:294`).

### Proposed registry row — PROOF-TARGET now; BRIDGE-ASSUMPTIONS-EXPLICIT only after the skeleton is built

Because no `.lean` is in the built tree yet, the truthful row TODAY is PROOF-TARGET:

```csv
D0-GAP-W-WITNESS-PLUS-ONE-001,BOOK_01,01.20/01.24 witness +1,,,OPEN,False,,gap_w_witness_check.py,PROOF-TARGET,"[center-attack GAP-W v2 candidate; OB-1 of Route B; skeptic#1 WOUNDED->repaired] |V_base|=|Omega8|+1=9 is FORCED GIVEN THREE NAMED JOINTS: W-BRIDGE-1' (stable re-detection class BOOK_01:1166.5 realized as >=1 stationary marked witness; narrated x3 A1:1541/A2:1987-1990/A3:1993; halt-QUOTIENT contract-owned :296/:366.5 BUT halt-PROPER lands +0 in adverse texts :846/:858, so +1 rides re-detection sliver only), W-T1 (CASE-2 copy schema on marks; :1556 does NOT back it), W-BIT (:1539 no-further-bit scope-transferred to mark labels, load-bearing by toggle). 8-kill: contract + re-detection bridge + COMPUTED full-cycle freeness. 10-kill: copy branch reuses repeat_has_nontrivial_copy_symmetry (NoExtension.lean:47), bit branch = W-BIT. No-overfire: first_instance_canonical (|S1|=1, NoExtension.lean:52) — NOT a V10-killer. Companion gap_w_witness_check.py 10/10 rc=0 (~7 independent). EXACT-MISSING: (1) the DRAFT Lean module D0.Core.WitnessForcing (memo §IV) added to the built tree — decidable OB-W1 no_stationary_in_omega8 + conditional capstone card_base_forced_conditional(m)(h_halt:1<=m)(h_nocopy:m<2); (2) the three joints promoted to registered ASSUMP ledger ids before any BRIDGE-ASSUMPTIONS-EXPLICIT upgrade; (3) GAP-E (extension completeness {D2,ABCD}) is NOT attempted here. Not claimed: unconditional forcing."
```

### RELEASE-gate checklist

| gate step | GAP-W status |
|---|---|
| build `HardClosureTheoremIndex` | **FAILS today** — `D0.Core.WitnessForcing` is DRAFT/memo-only (`:196`, `:294`), not in the built tree. |
| run all hard certificates | `gap_w_witness_check.py` is a memo sibling, not a registered `05_CERTS/vp_*.py`. Phase 4 negative-control shape (`STRUCTURE_FIXED_BEFORE_NUMBER:` + `FAIL_*`) not verified here. |
| check claim-map coverage | PROOF-TARGET row is coverage-valid (empty module ⇒ OPEN). |
| no forbidden `sorry`/`axiom`/`Float` | the memo's Route-B skeleton contains `witness_plus_one_forced : True := by sorry` (Route B memo `:276`) — **that `sorry` must NEVER enter the built tree**; the GAP-W §IV capstone itself is `sorry`-free (conditional, `rw;omega`), which is the correct version to build. |
| rebuild release ledger | nothing until built. |

**Verdict: needs-module (PROOF-TARGET-mintable NOW).**
- **NOT LEAN-CLOSED.** The headline is FORCED-GIVEN-THREE-JOINTS — a *reduction*, not a closure (contract Rule `:39`: "Any remaining bridge is a proof obligation").
- **Mint-ready NOW** only as the **PROOF-TARGET** row above.
- **Cleanest upgrade path of the three candidates:** once `D0.Core.WitnessForcing` (GAP-W §IV, sorry-free conditional capstone + decidable `no_stationary_in_omega8`) is **built and green**, and the three joints are registered as ledger assumptions (`ASSUMP-W-REDETECTION`, `ASSUMP-W-COPY-ON-MARKS`, `ASSUMP-W-BIT-TRANSFER`), the row becomes:
  `lean_module=D0.Core.WitnessForcing, lean_theorem=card_base_forced_conditional, lean_status=LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS, uses_bridge_assumptions=True, assumption_ids=ASSUMP-W-REDETECTION;ASSUMP-W-COPY-ON-MARKS;ASSUMP-W-BIT-TRANSFER, release_status=BRIDGE-ASSUMPTIONS-EXPLICIT`.
  This is a **reduction status, still not a closure** (contract `:24-31`). The decidable `no_stationary_in_omega8` sub-lemma could carry its own `CORE-FORMALIZED`/`LEAN_PROVED` row (it is genuinely unconditional), but that is the 8-kill's *computable half*, NOT the +1 headline.

**Conservatism note:** the memo is WOUNDED-then-repaired and *self-declares* it is not Lean-proved. Do NOT mint any closure status. The `sorry`-marked `witness_plus_one_forced` from the Route-B memo is a statement-TBD placeholder and must be excluded from any build.

---

## Candidate 3 — Route B (dissolve-window: the interval [9,13] is a projection, not a primitive)

**Source:** `WINDOW_9_13_FORCING_MEMO.md` (skeptic #1: **Claim W SURVIVES as candidate; Route B SURVIVES as candidate direction, BLOCKED from minting until repairs verified**, `:319`). Companion `window_forcing_check.py` 11/11 rc=0 (present).

### What is actually being claimed

The capstone `D0-SCENE-TRIPLE-UNIQUE-001`'s window hypotheses (`SceneTripleUnique.lean:77` `hlo:9≤z₁`, `hhi:z₁≤13`) are **outputs** of the owned capacity chain, not primitive inputs. Restated capstone consumes the chain and derives (9,11,13) with **zero window hypotheses**.

**Crucially, ¬W is NOT ⊥M1** (skeptic repair E5, `:17`, `:326`): the status quo is *Lean-backed unconsumed ownership*, not catalog-import. W is a **consumption-hygiene upgrade**, not a rescue from contradiction. This bounds how strong any mint can be.

**Residual (pre-registered, `:19`):** two necessity joints are narrated-only — **GAP-W** (= candidate 2 above) and **GAP-E** (extension completeness `{D₂, ABCD}`, the HARD half, untouched). Route B *dissolves the interval residual* and *relocates* the referee pressure onto these two joints; it does not close them.

### What IS genuinely Lean-closable vs the headline (from the §"Lean skeleton" ledger `:280-289`)

| skeleton theorem | hypotheses | Lean status | verdict |
|---|---|---|---|
| `scene_triple_from_owned_chain` (chain form) | **ZERO** | consumes only owned `card_*` (OB-0) | **genuinely closable NOW** — about the owned types themselves |
| `window_endpoints_derived : card V9 = 9 ∧ card V13 = 13` | none | `⟨card_v9, card_v13⟩` | **genuinely closable NOW** (trivial reuse) |
| `lucas_ge_of_six_le`, `lucas_le_of_le_four`, `unique_lucas_in_derived_window`, `level_five_minimal_all_parities` | none | Mathlib `Nat.fib_mono`+`omega`/`decide` | **closable** (re-proofs of owned tails; centre = L₅ derived) |
| `scene_triple_unique_v2 (hbase)(hstep₁)(hstep₂)` (uniqueness form) | **THREE** (`hbase`=GAP-W, `hstep₁/hstep₂`=GAP-E) | conditional; joints as hypotheses | this is the BRIDGE-ASSUMPTIONS shape — NOT unconditional |
| `witness_plus_one_forced : True := by sorry` | — | **`sorry` placeholder** | **MUST NOT enter the built tree** (`:276`) |

So Route B splits cleanly: the **chain-form + window-endpoints-derived + Lucas tails are unconditionally closable NOW** (they are the honest deliverable that "the endpoints are outputs"); the **uniqueness-form headline carries GAP-W + GAP-E as joints** and is a reduction, not a closure.

### Proposed registry row(s)

**Row A — the genuinely-closable chain projection (mint-ready as a real theorem AFTER the module is built):** this is the strongest honest content — that the endpoints are owned-cardinality theorems. But it too needs a *built* `D0.VNext2.SceneTripleForced`. Until built, PROOF-TARGET; the notes name the closable sub-theorems explicitly.

```csv
D0-WINDOW-9-13-DISSOLVE-001,BOOK_01,01.20/01.22 capstone window,,,OPEN,False,,window_forcing_check.py,PROOF-TARGET,"[center-attack Route B candidate; skeptic#1 SURVIVES, BLOCKED from minting] The capstone interval [9,13] (SceneTripleUnique.lean:77 hlo/hhi) is a PROJECTION of the owned graph-birth capacity chain V9=Omega8⊔{omega0}(=9), V11=V9⊔D2(=11), V13=V9⊔ABCD(=13), already Lean-typed with proved cardinalities (FiniteTypes.lean card_v9/card_v11/card_v13). NOT ⊥M1 (repair E5): status quo is Lean-backed UNCONSUMED ownership, not catalog-import; W is a consumption-hygiene upgrade. Companion window_forcing_check.py 11/11 rc=0 (kill matrix: new BASE-9+STEP-SET+COUNT-3 and old ladder+Lucas+window both admit only (9,11,13)). CLOSABLE-NOW sub-theorems (memo §skeleton, zero-hypothesis): scene_triple_from_owned_chain, window_endpoints_derived (card V9=9 ∧ card V13=13), unique_lucas_in_derived_window (centre L5=11 derived), level_five_minimal_all_parities. EXACT-MISSING: (1) module D0.VNext2.SceneTripleForced added to the built tree (sorry-free; the memo skeleton's witness_plus_one_forced:=sorry MUST be excluded); (2) the uniqueness-form capstone scene_triple_unique_v2 carries hbase=GAP-W (D0-GAP-W-WITNESS-PLUS-ONE-001) and hstep1/hstep2=GAP-E (extension completeness {D2,ABCD}, HARD, untouched) as NAMED joints — reduction not closure; (3) the 8+1 vs 4+5 nine-fork stays unidentified (ATT-2, separate task). Strands 4 texts on adoption (ATT-6): vp_scene_triple_unique.py, row D0-SCENE-TRIPLE-UNIQUE-001, BOOK_01:1501-1502, D0_REFEREE_ASSESSMENT.md:146-152."
```

**Note on D0-SCENE-TRIPLE-UNIQUE-001 (the existing capstone row):** Route B, if adopted, would *rewrite* that row (skeptic ATT-6 stranded-text cascade, `:308`). **This memo proposes NO edit to that existing CORE-FORMALIZED row** — the discipline forbids editing built/registry content; the dissolve is a candidate. Adoption is a separate, larger change that must rewrite the cert, the row, and two prose/assessment texts *in one unit*.

### RELEASE-gate checklist

| gate step | Route B status |
|---|---|
| build `HardClosureTheoremIndex` | **FAILS today** — `D0.VNext2.SceneTripleForced` is DRAFT/memo-only (`:183`, `:315`). The zero-hypothesis sub-theorems would build cleanly (they reuse `card_*`), but nothing is in the tree yet. |
| run all hard certificates | `window_forcing_check.py` is a memo sibling; the *registered* cert `vp_scene_triple_unique.py` guards the OLD route and (per skeptic) miscounts the `[9,29]` control (`L₆=18` also enters) — a text Route B must fix on adoption, not now. |
| check claim-map coverage | PROOF-TARGET row coverage-valid. |
| no forbidden `sorry`/`axiom`/`Float` | the skeleton's `witness_plus_one_forced := by sorry` (`:276`) is the tripwire — the buildable subset is the sorry-free chain/endpoint/Lucas theorems only. |
| rebuild release ledger | nothing until built. |

**Verdict: needs-module (PROOF-TARGET-mintable NOW), with a real closable sub-core pending the module.**
- **NOT LEAN-CLOSED** as a headline; the uniqueness form is CONDITIONAL on GAP-W + GAP-E.
- The **chain-projection sub-core** (`scene_triple_from_owned_chain`, `window_endpoints_derived`, `unique_lucas_in_derived_window`) is unconditionally true and would be `LEAN_PROVED` once built — but it proves "the endpoints are outputs of the owned cardinalities", NOT "the window is M1-derived" (memo ATT-4 `:306`: `Witness:=PUnit` is posited; the +1 forcing lives in GAP-W).
- **Mint-ready NOW** only as the **PROOF-TARGET** row above.
- **Upstream needed:** (i) GAP-W (candidate 2) as OB-1; (ii) GAP-E completeness (no owner, hard M1 meta-step, memo OB-2/3 `:286` "sketch only, not claimed"); (iii) the built `D0.VNext2.SceneTripleForced` module. Route B is explicitly **BLOCKED from minting** by its own skeptic verdict until the repairs are verified in a follow-up pass (`:319`).

**Conservatism note:** Route B's own skeptic verdict is "SURVIVES as candidate, BLOCKED from minting". Honor that: PROOF-TARGET only, no edit to the existing capstone row, `sorry` excluded.

---

## Source-edit + regen commands (DO NOT RUN — proposal only)

The registry is the single source of truth; `theory_status_map.csv` / `theory_graph.json` are **generated** (MEMORY: "edit the source + regen, never the generated file"; confirmed `sync_theory_status_map.py:11` reads `CLAIM_MAP`, `:309` writes `theory_status_map.csv`). To apply ANY of the proposed PROOF-TARGET rows, the operator would:

1. **Edit the canonical registry** — append the proposed row(s) to
   `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`
   (the on-disk column order: `claim_id,book,section,lean_module,lean_theorem,lean_status,uses_bridge_assumptions,assumption_ids,python_cert,release_status,notes`). PROOF-TARGET rows leave `lean_module`,`lean_theorem`,`assumption_ids` empty, `lean_status=OPEN`, `uses_bridge_assumptions=False`.

2. **Validate, then regenerate the derived files** (run from repo root `/Users/grigorijvahrusev/Downloads/d0_15`):

```bash
# 1. structural validation of the canonical CSV
python tools/validate_csv.py

# 2. regenerate the generated status map + theory graph FROM the canonical CSV
python tools/sync_theory_status_map.py

# (optional, per protocol Phase 5 :47-52 — only if a book fragment / aggregate is touched)
python tools/generate_lean_aggregates.py
python tools/assemble_books.py
python tools/d0_score.py --strict
```

**These commands are NOT run in this pass.** All three candidates are PROOF-TARGET proposals; running the regen now would publish rows for objects that have no built Lean module — premature. Register only after (a) the operator accepts the row text, and for any upgrade beyond PROOF-TARGET, (b) the corresponding module is built green and its joints are entered in `LEAN_ASSUMPTION_LEDGER.csv`.

---

## Summary scoreboard

| candidate | headline object | honest status | mint-ready NOW? | needs upstream |
|---|---|---|---|---|
| **M2** (`D0-M2-PHASE-LABELING-V9-SHELL-001` + `D0-M2-NO-CANONICAL-CYCLIC-LABELING-V9-001`) | labeling forced UP TO G_res (un-adjudicated reading) + μ₉ impossibility | **needs-module** — PROOF-TARGET only | PROOF-TARGET rows: **YES** | Lean module for pointed-shell ℂω₀⊕E₀⊕E₃⊕E₄ + reading-independence; then at best BRIDGE-ASSUMPTIONS (G_res joint), never bare closure. μ₉ NO-GO needs a formal no-go theorem. Fourier core already owned (D0-Q8-TERMINAL-FOURIER-001, cited). |
| **GAP-W** (`D0-GAP-W-WITNESS-PLUS-ONE-001`) | \|V_base\|=9 FORCED GIVEN 3 joints (W-BRIDGE-1′/W-T1/W-BIT) | **needs-module** — PROOF-TARGET; cleanest upgrade path | PROOF-TARGET row: **YES** | build `D0.Core.WitnessForcing` (sorry-free conditional capstone + decidable `no_stationary_in_omega8`) + register 3 ASSUMP ids ⇒ BRIDGE-ASSUMPTIONS-EXPLICIT (reduction, still not closure). |
| **Route B** (`D0-WINDOW-9-13-DISSOLVE-001`) | interval [9,13] is a chain projection; window-free capstone | **needs-module** — PROOF-TARGET; has a real closable sub-core | PROOF-TARGET row: **YES** | GAP-W (OB-1) + GAP-E completeness (no owner, hard) + built `D0.VNext2.SceneTripleForced`. Self-declared BLOCKED-from-minting until repairs verified. |

**Bottom line (conservative):** all three are **needs-module** — NONE is LEAN-CLOSED, and NONE is even eligible for a CONDITIONAL/BRIDGE-ASSUMPTIONS-EXPLICIT reduction *row* today, because that shape requires a **built** Lean theorem with the joints as explicit hypotheses, and no candidate has a module in the tree. Each is **mint-ready NOW only as a PROOF-TARGET row** carrying its joints/G_res/named-gaps in `EXACT-MISSING` grammar. GAP-W has the cleanest upgrade path (a sorry-free conditional capstone already drafted); Route B has a genuinely-closable zero-hypothesis sub-core (endpoints-are-outputs) but its headline uniqueness form depends on GAP-W + GAP-E; M2's headline forcing is irreducibly reading-dependent (G_res joint) and its Fourier core is already owned elsewhere.

Over-claiming a mint is the worst outcome; accordingly every proposed row above is OPEN/PROOF-TARGET, no closure vocabulary is attached to any narrated-joint headline, and no source file or built `.lean` is edited.


---

## Skeptic #1 verdict + repair log (accepted in full)

**Verdict: SURVIVES.** Attack mode: ACCEPT-IN-FULL (no defense mounted). The deliverable is a conservative PROOF-TARGET-only proposal ledger; no proposed row over-claims (every row carries `lean_status=OPEN` / `release_status=PROOF-TARGET`, all joints narrated in `EXACT-MISSING` grammar, no closure vocabulary on any narrated-joint headline). Nothing in the deliverable itself was killed or wounded. Two items are logged below: one hygiene fix (applied + re-verified), one operator precondition (audited + recorded, not a defect in this memo).

### Strongest finding (the weakest point — NOT a kill)

The M2 companion `m2_phase_labeling_check.py` final SUMMARY printed the **opposite adjective** to the deliverable's headline: `... FORCED up to G_res in {1, V4, (Z/2)^3} "(reading-adjudicated)"` (was `m2_phase_labeling_check.py:507`), whereas the deliverable narrates the reading as **UN-adjudicated** (`MINTING_PACKAGES.md:40`, `:51`). Verified this is **script-internal loose wording, not a defect in the deliverable**:
- the script's own PASS lines compute ALL THREE readings as valid single-orbit torsors and select none — `report(f"TORSOR_{r...}", k == n and k // n == 1, "... labeling FORCED up to G_res ({r})")` looped over `GRES = {"R-strong":1,"R-mid":4,"R-weak":8}` (`m2_phase_labeling_check.py:164-168`), emitting `TORSOR_R_strong`/`TORSOR_R_mid`/`TORSOR_R_weak` all PASS;
- the memo declares the adjudication OPEN: "adjudication NOT made here" (`M2_PHASE_LABELING_MEMO.md:38`), "**A3: the reading adjudication is OPEN.** This memo does not adjudicate R-strong/mid/weak" (`:238`), "Does NOT adjudicate among the three G_res readings (A3) — no \"G_res = V₄\" headline is claimed" (`:261`);
- the deliverable reads the artifact **correctly** and narrates G_res as an OPEN joint inside `EXACT-MISSING` — the conservative, safe direction.

No named second object and no named gap in the deliverable itself; the finding **cannot kill by `BOOK_05` §05.8.R** (or by any section). It resolves to a one-word script-summary nit.

### Repairs applied

**Repair 1 (hygiene, APPLIED + re-verified) — script SUMMARY wording.** Changed `m2_phase_labeling_check.py` SUMMARY from `"(reading-adjudicated)"` to `"(reading UN-adjudicated; all three G_res readings computed as valid torsors, none selected)"`, so the script's own summary matches its PASS torsor lines (`:164-168`) and memo `:261`. Re-ran the script: **ALL 50 CHECKS PASS, RC=0**, corrected SUMMARY prints. This is a script-hygiene fix only; **no change to `MINTING_PACKAGES.md` proposed rows** (which already narrated UN-adjudicated correctly). Load-bearing changed text re-verified = the SUMMARY line + the 50/50 PASS invariant; both green.

**Repair 2 (operator precondition, AUDITED + RECORDED — not a correction to the deliverable).** The deliverable already flags (per candidate) that the three companion `*_check.py` are **memo-sibling scripts, NOT registered `05_CERTS/vp_*.py` certs**, and that Phase-4 registration shape is "not verified here … would need audit before registration" (`MINTING_PACKAGES.md:65`, `:119`, `:174`). Carrying that forward: line-audited all three for the protocol Phase-4 shape (`VERIFIED_CLOSURE_PROTOCOL.md:41-46`: `STRUCTURE_FIXED_BEFORE_NUMBER:` as the FIRST output line + at least one reachable `FAIL_*` that fires + no bare `PASS`). Result — **none is registration-shaped as-is:**

| script | `STRUCTURE_FIXED_BEFORE_NUMBER:` first line? | reachable `FAIL_*` control? | Phase-4-registrable as-is? |
|---|---|---|---|
| `m2_phase_labeling_check.py` | **NO** (line 1 = shebang; line 2 = docstring) | has `CTRL_*` (5) but **NO `FAIL_*`** | **NO** — would need the cert header line + a firing `FAIL_*` |
| `gap_w_witness_check.py` | **NO** (shebang + docstring) | **neither `CTRL_*` nor `FAIL_*`** | **NO** |
| `window_forcing_check.py` | **NO** (shebang + docstring) | **neither `CTRL_*` nor `FAIL_*`** | **NO** |

This confirms the deliverable's own EXACT-MISSING statement rather than contradicting it: it is a **precondition on the operator before any actual registration run**, not a correction to `MINTING_PACKAGES.md`. The PROOF-TARGET rows as proposed do NOT depend on these scripts being registered certs (a PROOF-TARGET row's `python_cert` field may name a memo-sibling script; the row is coverage-valid as `OPEN`). The registration-shape work is owed **only** if/when a candidate is upgraded and its companion is promoted into `05_CERTS/` — at which point each script needs (i) `STRUCTURE_FIXED_BEFORE_NUMBER:` as its first printed line and (ii) at least one mutation-tested `FAIL_*` control. No script was mutated into cert shape in this pass (that is a registration task, out of scope for a mint decision).

### Errors of record (enumerated)

1. **EOR-1 (hygiene, FIXED).** `m2_phase_labeling_check.py:507` SUMMARY said `"(reading-adjudicated)"` — the opposite adjective to the script's own PASS torsor lines and to memo `:261` ("adjudication NOT made here"). Corrected to `"(reading UN-adjudicated; all three G_res readings computed as valid torsors, none selected)"`; re-ran 50/50 PASS RC=0. **Not a defect in `MINTING_PACKAGES.md`** — the deliverable already narrated UN-adjudicated correctly.
2. **EOR-2 (operator precondition, RECORDED — not a deliverable defect).** All three companion `*_check.py` fail the protocol Phase-4 registration shape as-is (no `STRUCTURE_FIXED_BEFORE_NUMBER:` first line; M2 has `CTRL_*` but no `FAIL_*`; GAP-W and window have neither). The deliverable already declared this as not-gate-verified (`:65`, `:119`, `:174`); the audit confirms it. Precondition on any future registration run, not a correction to this memo.

### Residual (what stays open / what is now mint-or-motion-ready)

- **Mint-ready NOW (unchanged by the skeptic):** all three PROOF-TARGET rows — `D0-M2-PHASE-LABELING-V9-SHELL-001` (+ optional NEGATIVE `D0-M2-NO-CANONICAL-CYCLIC-LABELING-V9-001`), `D0-GAP-W-WITNESS-PLUS-ONE-001`, `D0-WINDOW-9-13-DISSOLVE-001` — remain truthfully addable today as `lean_status=OPEN` / `release_status=PROOF-TARGET` rows carrying their joints/G_res/named-gaps in `EXACT-MISSING`. NO registry CSV was edited (proposals stay in this memo); NO built `.lean` was touched; the source-edit + regen commands (`§"Source-edit + regen"`) remain DO-NOT-RUN.
- **Motion-ready (upgrade paths, unchanged):** GAP-W has the cleanest path (build sorry-free `D0.Core.WitnessForcing` conditional capstone + decidable `no_stationary_in_omega8`, then register 3 ASSUMP ledger ids ⇒ BRIDGE-ASSUMPTIONS-EXPLICIT, a reduction not a closure). Route B has a genuinely closable zero-hypothesis sub-core (endpoints-are-outputs) pending its module. M2's headline forcing stays irreducibly reading-dependent (G_res joint).
- **Still open (unchanged):** every headline forcing (M2 G_res reading adjudication, GAP-W's three joints W-BRIDGE-1′/W-T1/W-BIT, Route B's GAP-W + GAP-E) remains a narrated joint — none is closed. GAP-E completeness `{D₂, ABCD}` has no owner. Route B is self-declared BLOCKED-from-minting until its repairs are verified.
- **Operator precondition before any registration run (from EOR-2):** promote the relevant companion script(s) into Phase-4 cert shape (`STRUCTURE_FIXED_BEFORE_NUMBER:` first line + firing `FAIL_*`) before any script is registered as a `05_CERTS/vp_*.py` cert. Not required for the PROOF-TARGET proposal rows to be truthful.

**Bottom line:** deliverable **SURVIVES** the skeptic. One hygiene fix applied and re-verified (script SUMMARY, 50/50 PASS RC=0). One operator precondition audited and recorded (Phase-4 shape of the three sibling scripts). All three candidates remain **needs-module / PROOF-TARGET-mintable-NOW**; no over-claim introduced or found; no registry or built-`.lean` edit made.
