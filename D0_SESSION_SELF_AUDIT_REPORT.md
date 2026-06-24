# D0 Session Self-Audit Report (autonomous hardening window, 2026-06-24)

**Mandate.** Asked to "дорабатывай по максимуму" while away. Under the standing truth discipline, the maximal
*honest* work in an unsupervised window is **not** to manufacture new claims — it is to **harden and
adversarially self-audit** everything built this session, fix any over-claim found, and confirm full
reproducibility. No new speculative claims were minted; the open missing primitives were **not** fabricated.

## 1. Reproducibility baseline (all green, tree clean)
`lake build D0.All` clean; `validate_csv`; `check_cert_can_fail`; `check_no_tautology_proofs`;
`check_physical_bridge_discipline`; `check_book_assembly`; `check_book_publication`;
`check_assumption_ledger_ownership`; `check_claim_map_coverage`; `check_no_sorry_in_core`;
`d0_score` (integrity demotions **0**). All 9 session certs re-pass independently. Registry consistency:
no duplicate ids; every session module on disk + imported into `D0.All`; every cert present.

## 2. Adversarial self-audit (8 skeptic buckets re-deriving the math + challenging every status)
**24 session claims audited; 22 CONFIRMED honest; 2 over-claims found and fixed; `overall_honest = True`;
no forbidden imports as a DEFINING engine anywhere** (external papers — PRL Barrios-Hita, Geng-Marshak,
Davis-Kahan 1970, AMS — are consistently walled as owner-edges/passports; PDG/fitted data never defines a
CORE theorem).

### Defect 1 — `D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001` (FIXED)
**Found:** the `ℬ_row` *sufficiency* and *deletion-minimality* were proven only over a **cherry-picked
2-element list** `{σ_A, σ_B}`. Over the declared admissible class (all **420** order-12 cycle-type-`(4,3)`
permutations of `Fin 7`), `ℬ_row` ("point 0 in the size-4 orbit") is satisfied by **240**, not 1
(re-derived independently; `σ_A`, `σ_C` both pass). So `ℬ_row` is **not** sufficient alone.
**Fix:** rewrote the module + cert + registry notes — `ℬ_row` is now stated as a **necessary separating bit**
(distinguishes the two canonical completions) that is **NOT sufficient** over the full class; the **sufficient**
row-fixing operator (`= PRIM-LEPTON-BRANCH-FIXING-OPERATOR`) is the full orbit-labeling `C(7,4)=35→1`, of which
`ℬ_row` (`35→20`) is one bit. The two-completion NO-GO core is unchanged (genuine).

### Defect 2 — `D0-PRESENT-CORE-LIMITS-REGRESSION-V15` (DOWNGRADED)
**Found:** registered NO-GO, but the mapped theorem `regression_owners_present : regressionOwners.length = 6`
is a **tautological list-count** — no admissible class, no negative content.
**Fix:** downgraded `NO-GO → CORE-FORMALIZED` with honest notes — it is a regression **citation index**, not a
new negative theorem; the actual limits are owned by the cited claims.

### Minor caveats (CONFIRMED honest, non-status-breaking; recorded, not rebuilt)
- `D0-BRANCH-CP-READOUT-NOGO-V15`: the `commutantDim := 3` conjunct is decorative (asserted from
  `X5.Grading.SymmetryGroups`, not re-derived here); the NO-GO rests on the genuine `ρ₁≠ρ₂` equal-marginal
  control, which is sound.
- `D0-P1-PHYSICAL-EOS`: the Lean models equal-*sum* rather than an explicit equal-*response* predicate; honest
  delegation to `D0-ARCHIVE-CONTRACTION-NOGO-001`, not an over-claim.

## 3. Corpus status after fixes (523 claims)
CORE-FORMALIZED 173+1, CERT-CLOSED 162, NO-GO 66−2, PROOF-TARGET 50, BRIDGE-ASSUMPTIONS-EXPLICIT 25,
PASSPORT-CLOSED 20, NO_GO_PROVED 8, EMPIRICAL-PASSPORT 7, … (net: one NO-GO→CORE-FORMALIZED move from Defect 2).

## 4. Open obligations (named missing primitives — NOT fabricated)
- `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` = full orbit-labeling (`Fin 7 → {4-orbit,3-orbit}`), `ℬ_row` is one bit.
- `Ξ_Y` / `ASSUMP-KERNEL-CHARGE-LOCALIZATION` (= `ν_R∈ker`, R2 graph→physics MECH-LIMIT) — hypercharge direction.
- `Ξ_CKM` ∈ {up/down pairing, common-left-carrier id, holonomy→mismatch} — CKM magnitude.
- `Ξ_U1 = Φ` (`PRIM-FINITE-SPECTRAL-TRIPLE-REP`) — graph-flow → Weyl coupling map.
- `PRIM-EDGE-HOLONOMY-SELECTOR`, `PRIM-STURMIAN-REFINEMENT-OWNER`, the isotropization gap→amplitude map,
  the AMS internal nuclear-flux transfer operator.

## 5. Bottom line
The session's output is **honest after two corrections the self-audit forced** — both were status-packaging
inflations (a sufficiency claim over a cherry-picked universe; a NO-GO label on a bookkeeping count), neither a
laundered physics result. The self-audit is itself the evidence that the discipline holds: it was run with
maximum skepticism against my own work and it caught real defects, which were fixed rather than defended.

## 6. Phase 2 — loop-engineering advancement (after feedback "could have advanced via loops")
A single audit pass is not the maximum honest use of an unsupervised window. Two standing honest loops were
run (the no-fabrication rule forbids inventing claims, not *working*):

**Loop B — corpus-wide over-claim census** (lean-stub-audit over all 521 D0 files; 1725 theorems: 1225
load-bearing, 377 weak-definitional, 30 vacuous, 39 flagged-but-real). Of 164 non-load-bearing theorems
backing active CORE/LEAN_PROVED claims, 161 were heuristic-conservative (`decide`/`ring` on real finite
content). **3 genuine vacuous over-claims found and fixed** (commit `8be7445`):
- `D0.Gauge.WilsonLinkGaugeCovariance`: removed `GaugeGroupDerivable : True` shell (asserted "gauge group
  derivable", not proved); claim was already on the genuine `wilson_loop_covariance`, CORE unaffected.
- `D0.Tower.NoExtension.no_extension_theorem`: dropped the decorative `3=2+1` conjunct; rests on its 3
  substantive conjuncts.
- (`gamma_anticomm_entries`/`D0-CARRIER-003`: a helper, not the registered `clifford_relation`; left, noted.)

**Loop A — PROOF-TARGET frontier derive-or-rule-out** (8 targets, each decided + adversarially verified). **6
NO-GO + 1 EXTERNAL-PASSPORT confirmed ok=true; 1 (`PHASON-WZ-EXPLICIT`) REJECTED by its skeptic (already-
covered/split) and HELD at PROOF-TARGET.** Two flipped this window with genuine owners:
- `D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001` PROOF-TARGET→**NO-GO** (commit `81d396c`): frozen raw graph forces
  the skeleton (Lucas 206, exponents (0,1/4,1/3), order-12 resolvent) but the coefficient is underdetermined
  over the full 420-element class (branch freedom + companion non-uniqueness). Owner: new can-FAIL cert
  `vp_lepton_raw_graph_coefficient_nogo.py` (the cert's own control caught — and I removed — a brittle/vacuous
  "misses every fraction" check). EXACT-MISSING: PRIM-LEPTON-BRANCH-FIXING-OPERATOR.
- `D0-PHASON-WZ-TRANSFER-OWNER-001` PROOF-TARGET→**NO-GO** (commit `fc650d5`): NEW decidable Lean theorem
  `sde_window_root_not_archive_eigenvalue` proves the integer L_archive spectrum {24,22,20} is spectrally
  disjoint from the S_DE window spectrum (roots of x²−3x+359/160) over ℚ → no canonical intertwiner; with
  role-orientation freedom the transfer is underdetermined. EXACT-MISSING:
  PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT.

**Verified-ready frontier build-queue (documented, not yet flipped — each adversarially ok=true):**
- `D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001` — NO-GO but **redundant** with RAW-GRAPH (same assignment-level
  obstruction); cite rather than mint a duplicate cert.
- `D0-LEPTON-PUISEUX-DECIMAL-SECTION-001` — EXTERNAL-PASSPORT; already documented external EFT/IR in its notes;
  optional formal `ASSUMP-EFT-IR-MATCHING-SCHEME` ledger row (touches the ownership gate — do with care).
- `D0-ALPHA-FESHBACH-DIXMIER-OWNER-001` — NO-GO (present-core maximality, class a≤2) + external Dixmier-trace
  passport; needs a Lean bundling theorem (α modules are dense — guard against collision).
- `D0-PMNS-DELTACP-PI0-001` — exact decimal ruled out (external) + a forced qualitative Z₂ CP-near-conservation
  lemma (buildable, reuse phason Z₂).
- `D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001` — NO-GO; citation-binding lemma (obstruction already formalized under
  the R4/E4 ids).

Gates after every flip: `lake build D0.All` clean (3978); `validate_csv`; `check_cert_can_fail`;
`check_no_tautology_proofs`; `check_no_sorry_in_core`; `check_physical_bridge_discipline` (523);
`d0_score` integrity demotions **0** throughout. Net frontier movement this window: **2 PROOF-TARGET→NO-GO**,
**3 vacuous over-claims removed**, **1 new decidable separator theorem**, all with real owners.

## 7. Phase 3 — design-and-verify cycles ("делай по максимуму циклами", ultracode)
Three further adversarial cycles (verify-then-build Workflows) mapped the rest of the frontier; each candidate
owner was **designed + adversarially verified** before any implementation, which deliberately **prevented
over-claims** rather than maximizing the flip count.

**One more genuine flip** (`0e67b69`): `D0-CKM-CLASS5-PARITY-EXCLUSION-001` PROOF-TARGET→**NO-GO** — orientation
parity alone cannot exclude CKM winding class 5 (the parity selector is degenerate on the odd classes
`{1,5}`: `parityOnlySelector(5)=parityOnlySelector(1)`, a finite contradiction with `sel(5)≠sel(1)`). Owner is
the claim's own already-`LEAN_PROVED` `ckm_class5_parity_exclusion_status`; its cert was reframed from a
PROOF-TARGET manifest to a consistent can-FAIL NO-GO cert. The substantive exclusion is owned on the aliasing
axis (`D0-CLASS5-ALIASING-001` CORE + `D0-CKM-CLASS5-SELECTOR-OWNER-001` CERT-CLOSED).

**The cycles' main value was negative — they stopped me over-claiming.** Across the queue (cycle 1) and 20
fresh targets (cycles 2–3), the adversarial layer + my own skepticism rejected the rest as **external-gated,
already-owned, split, or skeptic-failed** — i.e. NOT new closures:
- **CALIBRATION FIXED:** a NO-GO requires a genuine machine-checked **impossibility** over the full class — NOT
  mere not-yet-built or external-dependence. On that bar: `ADLER-WEISS` (cell-exact Markov property = external
  classical Adler-Weiss 1967, no present-core impossibility proof) stays PROOF-TARGET/external, **not** NO-GO.
- **Discarded an agent-written over-claim:** a workflow agent created `PMNSDeltaCPZ2.lean` bundling a trivial
  `1/2`-is-fixed-point-of-`1−x` fact with already-owned lemmas under an interpretive "CP near-conservation"
  label, to justify a CORE flip. Same decorative-conjunct pattern as the Loop-B fixes → **discarded**, PMNS
  stays PROOF-TARGET (exact δ_CP is an external NuFIT passport).
- **Already-owned (CITE, no new NO-GO):** `ALPHA-FESHBACH-DIXMIER` (every obstruction owned + external Dixmier
  passport), `LEPTON-INDIRECT` (redundant with RAW-GRAPH), `LEPTON-YUKAWA-HIERARCHY` (owned under R4/E4),
  `HYPERCHARGE-GRAPH-FLOW` (span{Y,B-L} 2-dim owned; value-route external), `PHASON-WDE-Z-MAP`.
- **External / MECH-LIMIT / held:** `PUISEUX-DECIMAL`, `TORAL-TIME-MARKOV` (Williams SSE), `HBAR-SYMPLECTIC`,
  `INDUCTIVE-SPECTRAL-TRIPLE`, `PHASON-WZ-EXPLICIT` (skeptic-rejected), `LEPTON-BRANCH-FIXING-OPERATOR` (ok=false),
  `ISOTROPIZATION` (Layer-1 THE already stands).

**Bottom line of Phase 3:** maximum *honest* cycling converges, not to a long list of flips, but to **3 genuine
new NO-GO closures + 3 over-claim removals this session**, and a verified map showing the remaining frontier is
external-gated or already-owned. Forcing those would be the inflation the discipline forbids — the cycles' job
was to find that out rigorously, and they did. Full map: memory `d0-frontier-loop-queue`.

## 8. Phase 4 — completion and convergence (Cycles 3–4)
**Cycle 3** added one more genuine flip: `D0-EDGE-COVER-FAMILY-001` PROOF-TARGET→**NO-GO** (`27b5ca8`) — the
edge cover is a `U(1)` λ-family with an injective separating observable (`EdgeAudit.cover_coeff_injective`);
node C's v15 `cardC` was reclassified `provedImpossibleInClass=true → NO_GO` to align it with its
structurally-identical siblings B/D/E2. **Cycle 4** (metrology, CVFT remainder, EDGE-002, the VNEXT/VNEXT2
spectral-triple tower) produced **zero** genuine flips: the 4 VNEXT/VNEXT2 owners drafted as NO-GO all have
their impossibility already owned by sibling `-NOGO`/`-MAXIMALITY-NOGO` claims (double-own → cite, not flip; 2
were adversarially rejected), EDGE-002 is a MINIMAL-EXTENSION owned by siblings, and the rest are
external-passport / STAY-OPEN.

**Convergence.** Four derive-or-rule-out cycles + the census + the self-audit have now exhaustively swept the
frontier. Maximal *honest* cycling delivers:
- **4 genuine new frontier NO-GO closures**, each with a real owner and full gate sweep:
  `LEPTON-RAW-GRAPH-COEFFICIENT` (`81d396c`), `PHASON-WZ-TRANSFER` + new Lean separator (`fc650d5`),
  `CKM-CLASS5-PARITY` (`0e67b69`), `EDGE-COVER-FAMILY` (`27b5ca8`);
- **3 vacuous over-claims removed** (`8be7445`) + **2 tightenings** (`49380e9`) + **2 self-audit fixes** (`1739148`);
- a verified map proving the remaining ~22 PROOF-TARGETs stay open **by necessity, not neglect**
  (external-data-gated, already-owned-by-sibling, MINIMAL-EXTENSION, or architecture-blocked) — forcing any of
  them is inflation. The pure external passports (DESI-BAO, ICECUBE, LIGO, SPARC) and the architecture-blocked
  pair (SPECTRAL-EINSTEIN, HODGE-LINKS) are external/blocked by inspection.

The cycles' adversarial layer (plus my own skepticism) rejected **~19** would-be flips and discarded one
agent-written over-claim. That is the headline: maximal cycling did not mean maximal flipping — it meant a
rigorous, exhaustive frontier map with every genuine closure taken and every over-claim refused.
`d0_score` integrity demotions remained **0** across all 9 commits.
