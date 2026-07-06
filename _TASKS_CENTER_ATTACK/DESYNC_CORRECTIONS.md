# DESYNC CORRECTIONS — verified fix table

**Date:** 2026-07-05 · **Status:** PROPOSALS ONLY — no edits applied to any source, registry, atlas, board, builder, or `.lean`.
**Scope:** the F-03/F-04/F-05 renames+mention, the 43 Class-2 missing ids (PLANNED-CHAIN vs REAL-RENAME),
the 9 uncataloged primitives (add vs misnomer), and the SPECTRAL-EINSTEIN-001 inverse desync.
**Method:** every load-bearing fact carries an owned `file:line` citation quoted verbatim below the table.
**Tag legend:** `SAFE-CORRECTION` = rename/typo/add-missing-mention with **no status change** ·
`OWNER-GATED` = touches or implies a status change (PROOF-TARGET↔CERT-CLOSED/NO-GO), needs owner bless.

**Binding constraint honored:** NO edit to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` or any built `.lean`.
All registry-status changes below are proposals in THIS memo only.

---

## Headline table

| # | tag | file | old → new | verified? |
|---|---|---|---|---|
| F-03 | **OWNER-GATED** (NOT a safe rename — status inflation) | `04_VERIFICATION/TORAL_MARKOV_BLOCKERS.csv:7` | `D0-TORAL-LUCAS-VORONOI-PARTITION-OWNER-001` → **do NOT rename to** `D0-LUCAS-VORONOI-MARKOV-PARTITION-001` | target EXISTS (registry:322) but is CERT-CLOSED/LEAN_PROVED while the atlas row is PROOF-TARGET for a *different* object (canonical Markov partition, external/no-go) — rename would silently inflate |
| F-04 | **OWNER-GATED** (real rename, but PROOF-TARGET→CERT-CLOSED) | `04_VERIFICATION/COSMOLOGY_CLOSURE_BLOCKERS.csv:17` (claim_id cell) **AND** `:19` (depends_on cell) | `D0-PHASON-CONTINUUM-INTERPOLATION-OWNER-001` → `D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001` | target EXISTS (registry:452, CERT-CLOSED); atlas itself (row 20) already says "continuum interpolation CLOSED (…ENVELOPE-OWNER-001, CERT)". Rename inherits CERT-CLOSED → status change → owner bless |
| F-05 | **SAFE-CORRECTION** (add missing mention, no status change) | `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:407` notes — *proposal only, no CSV edit* | append `; completion class = PRIM-NONCOMMUTING-TRIPLE` after `…No T^44=I.` | primitive IS in catalog; notes already describe the `(U,Q0,Pi_H)` completion class but never name the primitive |
| F-15 | **OWNER-GATED** (inverse desync: stale notes+audit vs live field) | `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:175` notes **AND** `04_VERIFICATION/STATUS_INFLATION_AUDIT.csv:170` — *proposals only* | notes/audit narrate `PROOF-TARGET/OPEN, cert cleared, G_A2 does NOT exist` → reconcile to the live field `LEAN_PROVED/CERT-CLOSED` | Lean module + theorems exist AND cert PASSES (exit 0) proving the exact object the notes call missing |

---

## Evidence (verbatim citations)

### F-03 — TORAL-LUCAS-VORONOI-PARTITION-OWNER — NOT a safe rename (OWNER-GATED)

The atlas row is an OPEN proof-target for the *canonical Markov partition*, which the registry explicitly
declares external / closed-negative-by-no-go. The proposed rename target is a CERT-CLOSED *scaffold* — a
DIFFERENT object. Renaming would flip PROOF-TARGET → CERT-CLOSED (status inflation).

- Atlas row (source of the desync), `04_VERIFICATION/TORAL_MARKOV_BLOCKERS.csv:7` — status is **PROOF-TARGET**:
  > `D0-TORAL-LUCAS-VORONOI-PARTITION-OWNER-001,B,PROOF-TARGET,,,BOOK_06,D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001,seed stable/unstable separations,"a canonical seed-determined partition whose cells are Markov rectangles; the 3-point seed does not canonically fix rectangle boundaries (Adler-Weiss non-unique) … a canonical partition is an EXTERNAL Adler-Weiss/Williams passport, not present-core.",True`
- Proposed target, `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:322` — status **CERT-CLOSED**, and it
  explicitly scopes OUT the exact Markov property the atlas row is about:
  > `D0-LUCAS-VORONOI-MARKOV-PARTITION-001,BOOK_06,06.31,D0.Geometry.LucasVoronoiMarkovPartition,…,CERT-CLOSED,"… OPERATOR-SCAFFOLD: the Voronoi-cell-exact MARKOV property and full topological conjugacy stay external (D0-ADLER-WEISS-PARTITION-OWNER-001, ASSUMP-ADLER-WEISS). NOT an import of Adler-Weiss as CORE."`
- Wrong id is absent from the registry: `grep -c D0-TORAL-LUCAS-VORONOI-PARTITION-OWNER-001 <registry> = 0` (verified).
- **Recommended action:** treat as PLANNED-CHAIN (F-17 policy — register as PROOF-TARGET or mark planning-only),
  NOT a rename. If the owner still wants a rename, it MUST NOT point at the CERT-CLOSED scaffold.

### F-04 — PHASON-CONTINUUM-INTERPOLATION → ENVELOPE — real rename, OWNER-GATED (status change)

The atlas already records the interpolation as delivered by the envelope; the INTERPOLATION-OWNER id is a
stale placeholder. The rename is semantically correct but flips PROOF-TARGET → CERT-CLOSED, and must fix **two
cells** (the claim_id row AND the downstream depends_on cell).

- Atlas claim_id cell, `04_VERIFICATION/COSMOLOGY_CLOSURE_BLOCKERS.csv:17` — PROOF-TARGET, missing-artifact = the envelope's content:
  > `D0-PHASON-CONTINUUM-INTERPOLATION-OWNER-001,B,PROOF-TARGET,,,BOOK_08/08.COSMOLOGY-CLOSURE,D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001,continuum interpolation w_N -> w_D0(u) agreeing with the discrete archive windows,True`
- Atlas depends_on cell (second occurrence — rename must fix this too), `…:19`:
  > `D0-PHASON-WZ-EXPLICIT-FUNCTION-001,C,PROOF-TARGET,,,…,D0-PHASON-CONTINUUM-INTERPOLATION-OWNER-001,explicit continuum w_DE(z) function …`
- Atlas SELF-ATTESTS the delivery, `…:20`:
  > `… "RESOLVED: continuum interpolation CLOSED (D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001, CERT); …"`
- Target registry row, `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:452` — CERT-CLOSED, content matches ("restricts at integer s=N to w_N"):
  > `D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001,BOOK_08,08.51,D0.Cosmology.PhasonContinuumEnvelope,…,CERT-CLOSED,"[P3-A] The closed phi-semigroup FORCES … w_D0(s)=1/[phi(1-exp(-s log phi))], which restricts at integer s=N to w_N=phi^(N-1)/(phi^N-1) …"`
- Wrong id absent from registry: `grep -c = 0` (verified). Target does not already appear in this atlas as a
  claim_id, so no collision (it appears only inside the prose of row 20).
- **Recommended action:** RENAME both cells (rows 17 and 19), tagged OWNER-GATED because it inherits CERT-CLOSED.

### F-05 — Higgs no-go: add PRIM-NONCOMMUTING-TRIPLE mention — SAFE-CORRECTION

Pure add-missing-mention; no status change. The primitive is already in the catalog; the notes describe the
completion class in prose but never name it.

- Registry row tail, `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:407` (NO-GO, unchanged):
  > `… A non-commuting witness Qnc=[[1,0],[0,0]] has [T,Qnc]!=0 but is NOT a polynomial in T (not present-core). … a new independently-forced (U,Q0,Pi_H) is required (extension). No T^44=I."`
- Primitive is cataloged: `PRIM-NONCOMMUTING-TRIPLE` is row-present in `04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv` (verified in the 11-row id list).
- `grep -c NONCOMMUTING-TRIPLE` on row 407 = **0** (verified — not yet mentioned).
- **Proposed one-liner (memo-only, no CSV edit):** append `; completion class = PRIM-NONCOMMUTING-TRIPLE`
  immediately before the closing quote, i.e. `…No T^44=I.; completion class = PRIM-NONCOMMUTING-TRIPLE"`.

### F-15 — SPECTRAL-EINSTEIN-001 inverse desync — OWNER-GATED reconciliation

Exact notes-vs-field mismatch: the FIELD is `lean_status=LEAN_PROVED`, `lean_module=D0.VNext2.SpectralEinsteinResponse`,
`lean_theorem=einstein_response_symmetric_and_conserved;einstein_response_eq`, `release_status=CERT-CLOSED`; the NOTES
still narrate a demotion and declare the proved object nonexistent.

- Field vs notes, `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:175`:
  > `D0-SPECTRAL-EINSTEIN-001,BOOK_07/08,…,D0.VNext2.SpectralEinsteinResponse,einstein_response_symmetric_and_conserved;einstein_response_eq,LEAN_PROVED,…,vp_spectral_einstein_response.py,CERT-CLOSED,"… [Iter5 demote] … Demoted CERT-CLOSED -> PROOF-TARGET, cert cleared. [Iter21 P2 audit …] … that object does NOT exist anywhere in D0/ (no G_A2/EinsteinTensor). … EXACT-MISSING: the G_A2 tensor + d-forcing (architecture-blocked …)."`
  → The notes say **PROOF-TARGET / cert cleared / object does NOT exist**; the field says **LEAN_PROVED / CERT-CLOSED**. Direct contradiction.
- The Lean module exists and proves exactly the "missing" object, `09_LEAN_FORMALIZATION/D0/VNext2/SpectralEinsteinResponse.lean`:
  > `def einsteinResponse (L : Matrix N N ℝ) : Matrix N N ℝ := (2 : ℝ) • L`
  > `theorem einstein_response_symmetric_and_conserved (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) : …`
- The cert PASSES (run `python3 05_CERTS/vp_spectral_einstein_response.py`, exit 0):
  > `PASS_SPECTRAL_EINSTEIN_RESPONSE — the finite rank-2 Einstein-tensor variational response G = dS_a2/dh = 2L EXISTS on the EH-proxy carrier, is exactly SYMMETRIC and DIVERGENCE-FREE …`
- Cross-atlas stale copy, `04_VERIFICATION/STATUS_INFLATION_AUDIT.csv:170` — also carries the stale demotion state:
  > `D0-SPECTRAL-EINSTEIN-001,PROOF-TARGET,OPEN,no,no,none,none`
- **Correct reconciliation:** the FIELD is current and CORRECT (module + passing cert deliver the G_A2=2L tensor,
  symmetric + divergence-free). The Iter5/Iter21 demotion narrative in the notes AND the STATUS_INFLATION_AUDIT
  row are STALE (they predate the re-closure). Proposal (memo-only): append a dated re-closure tag to the notes
  (e.g. `[2026-07 re-closure: G_A2=2L now realized in D0.VNext2.SpectralEinsteinResponse (symmetric+divergence-free),
  cert vp_spectral_einstein_response.py passes; the Iter21 "does NOT exist" block is superseded; smooth-limit + Fin-4
  TT linkage stay open under D0-HODGE-LINKS-001]`) and correct the audit row to `CERT-CLOSED,LEAN_PROVED,yes`.
  Tagged OWNER-GATED because it resolves a status contradiction. Note: the desync DETECTOR misses this because it
  only flags `lean_status=OPEN` rows; here lean_status=LEAN_PROVED, so the stale prose slips through.

---

## The 43 missing Class-2 D0 ids — PLANNED-CHAIN vs REAL-RENAME

**Verified globally:** all 43 ids are absent from the registry (`grep -c "^<id>," <registry> = 0` for every one — present-in-reg=0/43).
So none is a live claim; each is either a future/planned proof-target row (leave) or an atlas typo of a registered id (rename).
**Classification rule:** REAL-RENAME only if (a) a registered id owns the SAME object AND (b) the near-match target actually
exists in the registry. Where the target's status differs from the atlas row (PROOF-TARGET vs NO-GO/CERT-CLOSED), the rename
is tagged **OWNER-GATED** because it changes status.

| atlas id (source) | atlas file | verdict | registered target (verified) | tag |
|---|---|---|---|---|
| D0-TORAL-LUCAS-VORONOI-PARTITION-OWNER-001 | TORAL_MARKOV_BLOCKERS.csv:7 | **PLANNED-CHAIN** (NOT rename — see F-03; would inflate) | — (scaffold `D0-LUCAS-VORONOI-MARKOV-PARTITION-001` is a *different* object) | leave / register |
| D0-PHASON-CONTINUUM-INTERPOLATION-OWNER-001 | COSMOLOGY_CLOSURE_BLOCKERS.csv:17,19 | **REAL-RENAME** (F-04) | `D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001` EXISTS (CERT-CLOSED) | **OWNER-GATED** |
| D0-CMB-PHASON-TRANSFER-OWNER-001 | COSMOLOGY_CLOSURE_BLOCKERS.csv:24 (+depends_on :25) | **DECIDE-RENAME** (same WZ-transfer object) | `D0-PHASON-WZ-TRANSFER-OWNER-001` EXISTS (NO-GO) | **OWNER-GATED** |
| D0-CMB-PHASON-SPECTRUM-PASSPORT-001 | COSMOLOGY_CLOSURE_BLOCKERS.csv | **PLANNED-CHAIN** (distinct stage) | `D0-CMB-PHASON-SPECTRUM-OWNER-001` exists (PROOF-TARGET) but is the OWNER stage, not this passport | leave / register |
| D0-LEPTON-SHELL-GREEN-RESOLVENT-001 | GAUGE_MATTER_BLOCKERS.csv | **DECIDE-RENAME** (≈ finite-green-resolvent) | `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001` EXISTS (CERT-CLOSED) | **OWNER-GATED** |
| D0-LEPTON-BRANCH-PROJECTOR-OWNER-001 | GAUGE_MATTER_BLOCKERS.csv | **DECIDE-RENAME** (≈ branch-fixing-operator) | `D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001` EXISTS (NO-GO) | **OWNER-GATED** |
| D0-HIGGS-FINITE-CONDENSATION-OWNER-001 | HIGGS_PHASON_ORBIT_BLOCKERS.csv | **DECIDE-RENAME** (overlaps registered condensation owner) | `D0-HIGGS-PHASON-CONDENSATION-OWNER-001` EXISTS (PROOF-TARGET) | **OWNER-GATED** |
| D0-HIGGS-PHASON-HESSIAN-SIGN-OWNER-001 | GAUGE_MATTER_BLOCKERS.csv | **PLANNED-CHAIN** (Hessian-sign, no exact registered owner) | none (nearest is the condensation owner, distinct object) | leave / register |
| D0-DSIGMA-ROLE-CYCLE-CARRIER-001 | GAUGE_MATTER_BLOCKERS.csv | **PLANNED-CHAIN** (positive owner next to the NO-GO — NOT a rename) | `D0-DSIGMA-ROLE-CANONICAL-NOGO-001` is the *negative* neighbor, not this positive owner | leave / register |
| D0-HIGGS-PHASON-ORBIT-CLOSURE-001 | HIGGS_PHASON_ORBIT_BLOCKERS.csv:6 (has cert) | **DECIDE** (fold into registered NO-GO or register wrapper) | `D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001` EXISTS (NO-GO); atlas row is the decision-wrapper over it | **OWNER-GATED** |
| **ALPHA_DIXMIER (5):** D0-ALPHA-REFINEMENT-INCREMENT-OWNER-001, D0-ALPHA-CRITICAL-IDEAL-OWNER-001, D0-ALPHA-LOG-CESARO-TRACE-OWNER-001, D0-ALPHA-PAIRING-CANONICALIZATION-OWNER-001, D0-ALPHA-DIXMIER-PAIRING-CLOSURE-001 | ALPHA_DIXMIER_BLOCKERS.csv | **PLANNED-CHAIN** — α-front already CLOSED at NO-GO v2.1 → prefer retire/annotate as superseded, not register | none | leave (retire-annotate) |
| **TORAL chain (5):** D0-TORAL-MARKOV-RECTANGLE-OWNER-001, D0-TORAL-SYMBOLIC-CODING-OWNER-001, D0-TORAL-BOUNDARY-QUOTIENT-CONJUGACY-001, D0-TORAL-WILLIAMS-SSE-OWNER-001, D0-TORAL-LUCAS-MARKOV-CLOSURE-001 | TORAL_MARKOV_BLOCKERS.csv | **PLANNED-CHAIN** | none | leave / register |
| **COSMOLOGY remainder (8):** D0-PHASON-TWOMODE-PRESSURE-ENERGY-WINDOW-001, D0-PHASON-PHYSICAL-BRANCH-MAP-001, D0-CMB-HEATKERNEL-SPECTRAL-TILT-OWNER-001, D0-CMB-NS-INTERNAL-EXPRESSION-001, D0-CMB-PHASON-COVARIANCE-TO-POWER-001, D0-COSMOLOGY-FROZEN-PASSPORTS-OWNER-001, D0-COSMOLOGY-REHEATING-TO-CMB-CLOSURE-001, D0-DARK-RATIO-PASSPORT-001 | COSMOLOGY_CLOSURE_BLOCKERS.csv | **PLANNED-CHAIN** | none | leave / register |
| **GAUGE_MATTER remainder (7):** D0-GAUGE-MATTER-ROLE-FUNCTOR-001, D0-GAUGE-MATTER-FUNCTOR-OWNER-001, D0-HYPERCHARGE-FLOW-TO-WEYL-MAP-001, D0-HYPERCHARGE-DSIGMA-ROLE-ORTHOGONALITY-001, D0-CKM-ORDER-STEP-DET-SELECTOR-001, D0-CKM-FINITE-OVERLAP-INVARIANT-001, D0-CABIBBO-INTERNAL-READOUT-001 | GAUGE_MATTER_BLOCKERS.csv | **PLANNED-CHAIN** | none | leave / register |
| **HIGGS orbit remainder (4):** D0-HIGGS-CANONICAL-PHASON-ORBIT-OWNER-001, D0-HIGGS-ARCHIVE-PROJECTOR-ORBIT-OWNER-001, D0-HIGGS-DISCRETE-LOGDET-EOM-OWNER-001, D0-HIGGS-DISCRETE-HESSIAN-OWNER-001 | HIGGS_PHASON_ORBIT_BLOCKERS.csv | **PLANNED-CHAIN** | none | leave / register |
| **ROLE_TO_OPERATOR (4):** D0-ROLE-TO-OPERATOR-FUNCTOR-OWNER-001, D0-CKM-ROLE-ADDRESS-ACTION-001, D0-ROLE-BOUND-SHELL-GREEN-OPERATOR-001, D0-CANONICAL-PHASON-PROJECTOR-ORBIT-001 | ROLE_TO_OPERATOR_BLOCKERS.csv | **PLANNED-CHAIN** | none | leave / register |

**Tally:** 43 ids → **1 REAL-RENAME** (F-04, OWNER-GATED), **5 DECIDE-RENAME** (registered near-match exists, status differs → OWNER-GATED),
**37 PLANNED-CHAIN** (no registered owner of the same object → leave as future rows, subject to the F-08/F-16/F-17 register-or-retire policy).
None is a SAFE-CORRECTION rename: every registered near-match target carries a status (NO-GO/CERT-CLOSED/PROOF-TARGET) that differs from
the atlas PROOF-TARGET source, so all renames imply a status change and are OWNER-GATED.

Status of each verified registered target (for the DECIDE rows):
- `D0-PHASON-WZ-TRANSFER-OWNER-001` → LEAN_PROVED / **NO-GO** (registry).
- `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001` → LEAN_PROVED / **CERT-CLOSED**.
- `D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001` → LEAN_PROVED / **NO-GO**.
- `D0-HIGGS-PHASON-CONDENSATION-OWNER-001` → OPEN / **PROOF-TARGET**.
- `D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001` → LEAN_PROVED / **NO-GO**; atlas row `D0-HIGGS-PHASON-ORBIT-CLOSURE-001` (HIGGS_PHASON_ORBIT_BLOCKERS.csv:6) is a decision-wrapper WITH a cert `vp_higgs_phason_orbit_nontriviality.py`.
- `D0-CMB-PHASON-SPECTRUM-OWNER-001` → OPEN / PROOF-TARGET (the OWNER stage; the atlas `-SPECTRUM-PASSPORT-001` is a distinct passport stage, so PLANNED-CHAIN not rename).

---

## The 9 primitives missing from TOTAL_EXTENSION_PRIMITIVES.csv — add vs misnomer

**Catalog state (verified):** `04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv` has exactly **11** rows:
PRIM-SCENE-HISTORY-REFINEMENT-RULE, PRIM-COMPARISON-MAP-XI-N, PRIM-DIRAC-SCALE-SELECTION, PRIM-PHYSICAL-MAGNITUDE-MAP,
PRIM-PHYSICAL-REDSHIFT-OBSERVABLE, PRIM-FORCED-SMOOTHING-WINDOW, PRIM-LEPTON-BRANCH-FIXING-OPERATOR, PRIM-PERRON-PHI3-CARRIER,
PRIM-NONCOMMUTING-TRIPLE, PRIM-FINITE-SPECTRAL-TRIPLE-REP, PRIM-BARYON-PHYSICAL-LABEL-TRANSFER.
**Each of the 9 below is cited in registry notes but absent from that catalog** (verified `grep -c` on the registry — count in table).

| primitive | registry-notes count (verified) | verdict | tag |
|---|---|---|---|
| PRIM-BRANCH-ISOTROPIC-READOUT | 1 | REAL — add catalog row (cited by D0-BRANCH-CP-READOUT-NOGO-V15) | SAFE-CORRECTION (add-to-catalog) |
| PRIM-CANONICAL-SELF-READING-FUNCTOR | 2 | REAL — add catalog row | SAFE-CORRECTION |
| PRIM-EDGE-HOLONOMY-SELECTOR | 2 | REAL — add catalog row | SAFE-CORRECTION |
| PRIM-EFT-IR-MATCHING-FUNCTIONAL | 1 | REAL — add catalog row | SAFE-CORRECTION |
| PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR | 2 | REAL — add catalog row | SAFE-CORRECTION |
| PRIM-ISOMETRIC-DIRAC-J | 3 | REAL — add catalog row | SAFE-CORRECTION |
| PRIM-PHASON-COORDINATE-FUNCTOR | 3 | REAL — add catalog row | SAFE-CORRECTION |
| PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT | 7 | REAL — add catalog row (most-cited of the 9) | SAFE-CORRECTION |
| PRIM-STURMIAN-REFINEMENT-OWNER | 2 | **MISNOMER-FLAG** — `-OWNER` is claim-style; no `PRIM-STURMIAN-REFINEMENT` exists to be a typo-of | **OWNER-GATED** (naming decision) |

**Notes on the 8 "add" primitives:** these are SAFE catalog-completeness adds — adding a row to
`TOTAL_EXTENSION_PRIMITIVES.csv` mints no claim and changes no claim status. (They also drive several Class-4 `[no-cat]` edges
in the fixlist Appendix C.) Adding them is orthogonal to the registry and to any `.lean`.

**PRIM-STURMIAN-REFINEMENT-OWNER — misnomer verification:**
- Used in exactly two places outside the generated JSON: `tools/append_v15_registry.py:28` and `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:344`; and cited (as the same string) in two registry rows.
- The book text names it deliberately as a primitive:
  > `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:344`: "… its step 2 would identify the Sturmian bonding maps with the frozen *archive* maps (a new primitive `PRIM-STURMIAN-REFINEMENT-OWNER`)."
- Registry citations (both write the `-OWNER` form):
  > `CLAIM_TO_LEAN_MAP.csv:510` (D0-STURMIAN-REFINEMENT): "… golden incidence det=-1,trace=1 (phi). Missing PRIM-STURMIAN-REFINEMENT-OWNER. No CFT/Virasoro import."
  > `CLAIM_TO_LEAN_MAP.csv:542` (D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001): the CONDITIONAL-EXTENSION of D0-STURMIAN-REFINEMENT (parent stays PROOF-TARGET) — discharge is NO-GO by field disjointness Q(√5) vs Q(√10).
- **Why it is not a safe add or a safe typo-fix:** the 11 catalog primitives all use the bare `PRIM-<CONCEPT>` form; `-OWNER` is the D0 *claim-id* suffix (as in the neighboring claim `D0-STURMIAN-REFINEMENT`). So the name conflates claim-style with primitive-style. But there is **no** existing `PRIM-STURMIAN-REFINEMENT` catalog row for it to be a typo *of*, and the discharge is a NO-GO (the primitive would never be needed as a live completion class). Two owner-choices, both status-neutral-in-fact but naming-load-bearing:
  1. Add as-is (`PRIM-STURMIAN-REFINEMENT-OWNER`) to the catalog, accepting the `-OWNER` suffix — mirrors book/registry text.
  2. Rename in the two registry notes + book line to `PRIM-STURMIAN-REFINEMENT` (drop `-OWNER`) and add THAT to the catalog.
  Tagged **OWNER-GATED** because it edits registry-note text and picks a canonical primitive name; not a mechanical SAFE add.

---

## Summary counts

| tag | count | items |
|---|---|---|
| **SAFE-CORRECTION** (no status change) | 9 | F-05 (add PRIM-NONCOMMUTING-TRIPLE mention) + 8 catalog adds (BRANCH-ISOTROPIC-READOUT, CANONICAL-SELF-READING-FUNCTOR, EDGE-HOLONOMY-SELECTOR, EFT-IR-MATCHING-FUNCTIONAL, GRADING-NEUTRAL-CURRENT-OPERATOR, ISOMETRIC-DIRAC-J, PHASON-COORDINATE-FUNCTOR, PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT) |
| **OWNER-GATED** (implies a status change) | 9 | F-04 rename; F-15 SPECTRAL-EINSTEIN reconciliation; 5 DECIDE-renames (CMB-PHASON-TRANSFER, LEPTON-SHELL-GREEN-RESOLVENT, LEPTON-BRANCH-PROJECTOR, HIGGS-FINITE-CONDENSATION, HIGGS-PHASON-ORBIT-CLOSURE); STURMIAN naming decision; **F-03 explicitly REJECTED as a rename** (would inflate) |
| **PLANNED-CHAIN** (leave / future register-or-retire) | 37 | the Class-2 remainder (ALPHA_DIXMIER 5 → retire per α-closure; TORAL 5; COSMOLOGY 8; GAUGE_MATTER 7+HESSIAN-SIGN+DSIGMA-CYCLE; HIGGS orbit 4; ROLE_TO_OPERATOR 4; SPECTRUM-PASSPORT; TORAL-VORONOI-PARTITION per F-03) |

## Honest partial-outcome notes (no fit forced)

- **F-03 does NOT close as a rename.** The fixlist proposed it "low-med", but verification shows the rename target is a
  CERT-CLOSED *scaffold* that explicitly scopes OUT the Markov property the atlas PROOF-TARGET row is about. Correcting the
  atlas id to that target would be status inflation. It stays PLANNED-CHAIN. This is the one place the fixlist's optimistic
  RENAME suggestion did not survive verification.
- **F-15 reconciliation direction is confirmed by a passing cert**, not assumed: `vp_spectral_einstein_response.py` exits 0
  and prints the object the Iter21 notes call nonexistent. Still OWNER-GATED because it resolves a status contradiction and
  touches a second atlas (STATUS_INFLATION_AUDIT.csv:170).
- **STURMIAN primitive is a genuine naming ambiguity**, not a clean typo — there is no bare `PRIM-STURMIAN-REFINEMENT` to
  correct toward, so it needs an owner naming call.
- **No SAFE rename exists among the 43 Class-2 ids.** Every registered near-match carries a differing status, so all renames
  are OWNER-GATED; the safe subset is limited to catalog adds + the one no-status mention (F-05).

## Discipline / provenance

- No edits applied to any file. `DESYNC_CORRECTIONS.md` is the only artifact written.
- No edit to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` or any `.lean` — all registry/notes/audit changes are proposals in this memo.
- Every load-bearing fact above is backed by a verbatim `file:line` quote or a re-run command (`grep -c`, cert exit code).
- Language is candidate/proposal throughout; nothing is declared "forced/closed" — the skeptic pass has not been run on the owner-gated status changes.
