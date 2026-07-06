# REGISTER EXHAUSTIVENESS MEMO — the open-joints register is NOT yet exhaustive (cert-built)

**Date:** 2026-07-05 · **Status:** CANDIDATE / DRAFT · **Outcome:** cert-built, currently **FAILING** (expected).
**Cert:** `_TASKS_CENTER_ATTACK/vp_register_exhaustiveness.py` (runnable; exit 1 = FAIL = the finding).
**Baseline manifest:** `_TASKS_CENTER_ATTACK/register_exhaustiveness_manifest.json` (C5 monotonicity anchor).
**Discipline honored:** PROPOSALS ONLY. NO edit applied to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`,
the LEAN_ASSUMPTION_LEDGER, any built `.lean`, or the generated `frontier_dag.json`. Every registry/atlas
change below is an owner-gated proposal. Owned NO-GOs are cited, never re-opened.

---

## 0. What this closes (the blind spot)

Nobody had certified that the open-joints register captures **every** open forcing obligation. The register was
declared "exhaustive by intent", but new PROOF-TARGETs and new `PRIM-*` primitives kept appearing at each vNext
*after* that declaration — so "exhaustive" was unfalsifiable. This cert makes it **machine-checkable**: five
failable checks over the canonical registry + atlases, reusing the measured DAG and the
`tools/build_frontier_dag.py` machinery. **The cert FAILS today**, and that failing state IS the finding: it is
the first mechanical proof that the register is not yet exhaustive, and it names exactly which obligations are
uncaptured.

Reused verbatim (no re-implementation): `build_frontier_dag.load_registry / is_frontier / is_nogo /
extract_registry_edges / load_atlas_edges / load_primitive_catalog / parse_nogo_flags`, and the canonical
`d0_status_model.canonical_release`. Source of truth = `CLAIM_TO_LEAN_MAP.csv` (registry) as declared in
[`d0-registry-source-of-truth`]; atlases and boards are secondary.

## 1. Current verdict (as printed by the cert)

```
registry rows=538  frontier(OPEN/PROOF-TARGET)=41  no-gos=82  catalog_primitives=11  refuted_candidates=1
[FAIL] C1  every OPEN/PROOF-TARGET claim is primitive-gated OR an explicit passport   — 5 unhomed
[FAIL] C2  every named PRIM-* has a completion object AND a consumer (no orphans)       — 12 orphans (1 refuted-exempt)
[PASS] C3  every no-go admissible completion class names an existing primitive
[FAIL] C4  every atlas claim_id has a registry home (no Class-2 desyncs)                — 50 missing
[PASS] C5  MONOTONICITY guard: no un-baselined primitive/proof-target additions
OVERALL: FAIL  (2/5 checks pass; negative-controls intact)
```

Negative controls (run inline every invocation): planting an orphan primitive is caught by C2; planting an
unhomed proof-target is caught by C1. A check that cannot fail is worthless — both fire, so the checks have teeth.

## 2. C1 gaps — 5 unhomed forcing obligations (OPEN/PROOF-TARGET, no primitive, no passport marker)

These frontier claims are OPEN or PROOF-TARGET yet name **no** blocking primitive and carry **no**
passport/external/`ASSUMP-*` marker in their notes. Each is a forcing obligation the register does not currently
home. Verified: `grep` of each registry row for any `PRIM-`/`passport`/`external`/`ASSUMP-` token returns empty.

| # | claim_id | registry line | status (lean/release) | why it is a genuine gap |
|---|---|---|---|---|
| G-C1.1 | `D0-CVFT-F3` | `CLAIM_TO_LEAN_MAP.csv:135` | OPEN / CERT-CLOSED | lean OPEN but release CERT-CLOSED with a passing cert — a **status-inflation-shaped** row; either it is closed (then lean_status should not be OPEN) or the residual obligation must be named. This is the same row DESYNC_FIXLIST F-02 judged "legitimate", but it still fails C1 because no forcing obligation is named for its OPEN leg. |
| G-C1.2 | `D0-HBAR-SYMPLECTIC-CAPACITY-MECH-LIMIT-001` | `CLAIM_TO_LEAN_MAP.csv:344` | OPEN / PROOF-TARGET | a MECH-LIMIT proof-target with no named missing artifact and no primitive; the residual (what closes it) is unstated. |
| G-C1.3 | `D0-HODGE-LINKS-001` | `CLAIM_TO_LEAN_MAP.csv:178` | OPEN / PROOF-TARGET | notes self-describe an honest Iter5 demotion ("the former cert was a print-only stub…no computation") but never name the missing finite-cochain artifact as a primitive or external leg. |
| G-C1.4 | `D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001` | `CLAIM_TO_LEAN_MAP.csv:332` | OPEN / PROOF-TARGET | an `-OWNER-` proof-target with a cert file but no named blocking primitive; the GAUGE_MATTER atlas chain that would gate it is itself unregistered (see §4). |
| G-C1.5 | `D0-ISOTROPIZATION-MECH-001` | `CLAIM_TO_LEAN_MAP.csv:524` | LEAN_PROVED / PROOF-TARGET | "A1 R2 MECH-LIMIT" with a Lean module + cert, yet PROOF-TARGET with no named residual primitive/passport. |

**Verbatim anchors (quoted from the registry):**

- `CLAIM_TO_LEAN_MAP.csv:135` — `D0-CVFT-F3,BOOK_04,CVFT hadron resonance pole transfer program,,,OPEN,False,,vp_cvft_baryon_s3_scaffold.py,CERT-CLOSED,Finite carrier/symmetrizer scaffold is certified…`
- `CLAIM_TO_LEAN_MAP.csv:178` — `D0-HODGE-LINKS-001,BOOK_04/07,Hodge matter-gravity archive links,,,OPEN,False,,,PROOF-TARGET,"[8C orphan-harvest] matter on C1, TT gravity on symmetric C1, shared finite cochain carrier. [Iter5 demote] HONEST demotion: the former cert was a print-only stub with no computation (could not FAIL)…"`
- `CLAIM_TO_LEAN_MAP.csv:524` — `D0-ISOTROPIZATION-MECH-001,BOOK_01,isotropization mechanism + residual,D0.Foundation.IsotropizationResidual,isotropization_residual,LEAN_PROVED,False,,vp_isotropization_residual.py,PROOF-TARGET,"A1 R2 MECH-LIMIT. Cubic lambda^3-359lambda-2574 coeffs = scene symmetric functions…"`

**Exact fix (proposal, owner-gated):** for each of the 5, append to the registry notes EITHER (a) the blocking
primitive `; completion class = PRIM-…` when one exists (e.g. G-C1.4 → `PRIM-EDGE-HOLONOMY-SELECTOR` per the
GAUGE_MATTER chain), OR (b) an explicit `EXACT-MISSING: <external leg>` / `passport` marker when the residual is
external, OR (c) reconcile the lean/release status when there is in fact no residual (G-C1.1: if CERT-CLOSED is
correct, lean_status must not stay OPEN — this is the F-02 reconciliation). No status is changed here; these are
notes proposals only.

## 3. C2 orphans — 12 primitives named with NO completion object in `TOTAL_EXTENSION_PRIMITIVES.csv`

The catalog has **11 rows**; the register names **24** distinct `PRIM-*` tokens. Twelve are orphans (one refuted
candidate is exempt — see §5). The desync sweep (DESYNC_FIXLIST.md:36, F-14) already found **9** of these and
flagged `PRIM-STURMIAN-REFINEMENT-OWNER` as a probable **misnomer**; the cert independently reproduces those and
surfaces **3 more** that come from a second, drifted primitive catalog.

### 3a. The 9 registry-consumed orphans (F-14) — real, add catalog rows

Each is named in the canonical registry notes AND has ≥1 DAG-gate consumer, so it is a live forcing obligation
missing only its completion object:

| # | primitive | DAG-gate consumers | note |
|---|---|--:|---|
| G-C2.1 | `PRIM-BRANCH-ISOTROPIC-READOUT` | 1 | gates `D0-BRANCH-CP-READOUT-NOGO-V15` |
| G-C2.2 | `PRIM-CANONICAL-SELF-READING-FUNCTOR` | 2 | gates the two self-reading minimality owners |
| G-C2.3 | `PRIM-EDGE-HOLONOMY-SELECTOR` | 2 | gates `D0-EDGE-COVER-FAMILY-001`, `D0-UNIFIED-EDGE-SPINE-001` |
| G-C2.4 | `PRIM-EFT-IR-MATCHING-FUNCTIONAL` | 1 | gates `D0-LEPTON-DECIMAL-MASS-RATIOS` |
| G-C2.5 | `PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR` | 2 | gates the grading-neutral maximality no-go + X5 contract |
| G-C2.6 | `PRIM-ISOMETRIC-DIRAC-J` | 3 | gates the vNext Dirac-tower owners/no-go |
| G-C2.7 | `PRIM-PHASON-COORDINATE-FUNCTOR` | 3 | gates postcore phason extension + X5 contract |
| G-C2.8 | `PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT` | 8 | highest fan-out orphan; DESYNC_FIXLIST F-13 confirms it is used by the ROOT board yet absent from the catalog |
| G-C2.9 | `PRIM-STURMIAN-REFINEMENT-OWNER` | 2 | **MISNOMER** — see §3c |

**Verbatim anchor (F-14, DESYNC_FIXLIST.md:36):** "9 primitives named in registry notes/boards are uncataloged
(catalog has only 11 rows): BRANCH-ISOTROPIC-READOUT, CANONICAL-SELF-READING-FUNCTOR, EDGE-HOLONOMY-SELECTOR,
EFT-IR-MATCHING-FUNCTIONAL, GRADING-NEUTRAL-CURRENT-OPERATOR, ISOMETRIC-DIRAC-J, PHASON-COORDINATE-FUNCTOR,
PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT, STURMIAN-REFINEMENT-OWNER … add catalog rows; flag
PRIM-STURMIAN-REFINEMENT-OWNER as probable misnomer (-OWNER is claim-style suffix)".

**Exact fix (proposal):** add one row per primitive to `04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv` with the
existing schema columns (`primitive_id, mathematical_type, minimal_input, why_core_cannot_derive,
admissible_completion_class, necessary_conditions, sufficient_conditions, counterexample_witness,
negative_controls, lane`). The `why_core_cannot_derive` + `admissible_completion_class` content already exists in
the consuming claims' notes and can be lifted verbatim (e.g. G-C2.5 from the `X5_FINAL_BLOCKERS.csv` row).

### 3b. The 3 second-catalog orphans — a DRIFTED PARALLEL CATALOG (new sub-finding)

`04_VERIFICATION/D0_FINAL_NEW_PRIMITIVES.csv` is a **second primitive catalog** with different names for
overlapping objects. It shares 5 rows with `TOTAL_EXTENSION_PRIMITIVES.csv` but adds 4 uniquely-named rows,
three of which have **0 DAG-gate consumers** (they are named only in `D0_FINAL_NEW_PRIMITIVES.csv` and
`D0_FINAL_RELEASE_READINESS.json`):

| # | primitive (in `D0_FINAL_NEW_PRIMITIVES.csv`) | canonical-catalog counterpart? |
|---|---|---|
| G-C2.10 | `PRIM-CANONICAL-MARKOV-PARTITION` | none — the toral symbolic-conjugacy owner is registered as a NO-GO/external (Adler-Weiss passport), not a completion object |
| G-C2.11 | `PRIM-EFT-IR-FUNCTOR` | **name-desync** with the registry's `PRIM-EFT-IR-MATCHING-FUNCTIONAL` (G-C2.4) — same object, two names |
| G-C2.12 | `PRIM-SYMMETRY-BREAKING-SELECTOR` | none in canonical catalog; CKM/role-functor selector |

Also note `D0_FINAL_NEW_PRIMITIVES.csv` writes `PRIM-ISOMETRIC-DIRAC-J_N` (with `_N`) while the registry writes
`PRIM-ISOMETRIC-DIRAC-J` (G-C2.6) — a suffix-desync between the two catalogs for the same primitive.

**Exact fix (proposal, owner-gated):** designate `TOTAL_EXTENSION_PRIMITIVES.csv` as the SOLE canonical primitive
catalog (matching the cert's assumption and the task spec). Then EITHER (a) fold `D0_FINAL_NEW_PRIMITIVES.csv`
into it, reconciling the name-desyncs (`PRIM-EFT-IR-FUNCTOR`→`PRIM-EFT-IR-MATCHING-FUNCTIONAL`,
`PRIM-ISOMETRIC-DIRAC-J_N`→`PRIM-ISOMETRIC-DIRAC-J`), and register `PRIM-CANONICAL-MARKOV-PARTITION` /
`PRIM-SYMMETRY-BREAKING-SELECTOR` as completion objects OR retire them if superseded; OR (b) mark
`D0_FINAL_NEW_PRIMITIVES.csv` as a historical snapshot, planning-only, and exclude it from the catalog namespace.
The cert scans it today only to SURFACE the drift; it treats `TOTAL_EXTENSION_PRIMITIVES.csv` as authoritative.

### 3c. `PRIM-STURMIAN-REFINEMENT-OWNER` — probable misnomer (candidate)

The `-OWNER` suffix is claim-style, not primitive-style; the object is a genuine M1-forced substitution owner. It
gates `D0-STURMIAN-REFINEMENT` (a non-standard claim_id lacking the `-\d{3}` suffix) and the discharge no-go.

- `CLAIM_TO_LEAN_MAP.csv:510` — `D0-STURMIAN-REFINEMENT,BOOK_06,v15 Sturmian refinement,D0.Integration.V15.Refinement,sturmian_golden_tower,LEAN_PROVED,False,,,PROOF-TARGET,"v15 WP-F2 CONDITIONAL-EXTENSION. golden incidence det=-1,trace=1 (phi). Missing PRIM-STURMIAN-REFINEMENT-OWNER. No CFT/Virasoro import."`
- `09_LEAN_FORMALIZATION/D0/Integration/V15/Refinement.lean:30` — "owner `PRIM-STURMIAN-REFINEMENT-OWNER`. Hence CONDITIONAL, not present-core. No CFT/Virasoro is imported."

**Owned NO-GO respected:** the discharge is proved impossible internally by
`D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001` (field disjointness `√10 ∉ ℚ(√5)` + orientation trace `+1` vs `−1`).
That NO-GO says an external owner *could postulate* the primitive as a passport — so the primitive is a legitimate
**external completion object**, not a phantom. It must be cataloged (with `lane = external/passport`), not deleted.

**Exact fix (proposal, owner-gated):** add the catalog row under a corrected primitive-style id
(candidate: `PRIM-STURMIAN-REFINEMENT-BONDING-MAP`) with `admissible_completion_class` = the frozen-archive
bonding-map identification, `lane = external`, and correct the two citing notes (registry:510 and Refinement.lean
prose is a Lean draft — proposed as a code-block change only, not applied). Alternatively keep the `-OWNER` id if
the owner rules the suffix acceptable; the misnomer flag is a naming candidate, not a forced rename.

## 4. C4 desyncs — 50 atlas claim_ids absent from the registry (the Class-2 desyncs)

Fifty well-formed `D0-…-\d{3}` / `CVFT-F\d` claim_ids appear as `*BLOCKERS*.csv` atlas rows but have **no** row in
the canonical registry. Since the registry is the source of truth ([`d0-registry-source-of-truth`]), these are
planned-chain rows that were never registered — the atlases silently extend the frontier past what the register
records. Breakdown by atlas file:

| atlas | missing claim_ids |
|---|--:|
| `COSMOLOGY_CLOSURE_BLOCKERS.csv` | 11 |
| `GAUGE_MATTER_BLOCKERS.csv` | 11 |
| `FINAL_CONTINUATION_BLOCKERS.csv` | 8 |
| `HIGGS_PHASON_ORBIT_BLOCKERS.csv` | 6 |
| `TORAL_MARKOV_BLOCKERS.csv` | 6 |
| `ALPHA_DIXMIER_BLOCKERS.csv` | 5 |
| `ROLE_TO_OPERATOR_BLOCKERS.csv` | 5 |
| **total** | **50** |

This corroborates DESYNC_FIXLIST.md's Class-2 count ("43 unique missing D0 ids (planned-chain rows)"); the cert
counts 50 because it also folds in the HIGGS_PHASON_ORBIT and ROLE_TO_OPERATOR rows that F-07/F-08 discuss
separately. Representative examples the fixlist already adjudicated:

- **α-Dixmier chain (5 ids)** — DESYNC_FIXLIST F-16: the α-front is CLOSED at the eight-pass NO-GO v2.1
  (`ALPHA_SEAM_NOGO_V2.md`). Fix: **RETIRE/annotate** these atlas rows as superseded by the α-closure rather than
  registering new PROOF-TARGETs. **Owned NO-GO respected** — do not re-open the α-seam.
- **HIGGS chain (5 ids)** — F-08: planned global-blocker chain, `is_global_blocker=True`, not registered; also
  resolve the `-FINITE-CONDENSATION` vs registered `D0-HIGGS-PHASON-CONDENSATION-OWNER-001` name overlap first.
- **TORAL_MARKOV chain** — F-03/F-17: `D0-TORAL-LUCAS-VORONOI-PARTITION-OWNER-001` is a rename trap
  (OWNER-GATED — see DESYNC_CORRECTIONS.md F-03), the rest are planned chain.
- **COSMOLOGY chain** — F-04/F-18: `D0-PHASON-CONTINUUM-INTERPOLATION-OWNER-001` is a real rename to the
  registered CERT-CLOSED `D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001` (OWNER-GATED, status change).

**Exact fix (proposal, per-id owner call):** for each atlas id, EITHER (a) register it as a PROOF-TARGET row in
the registry (registry-canonical policy, F-08), OR (b) correct it to the already-registered id when it is a rename
(F-03/F-04/F-18 — OWNER-GATED because those inherit CERT-CLOSED/NO-GO), OR (c) retire the atlas row as superseded
(F-16 α-closure). The full per-id adjudication already exists in `DESYNC_FIXLIST.md` (F-01…F-18) and
`DESYNC_CORRECTIONS.md`; this cert is the machine check that will go GREEN once those proposals are applied.

## 5. The refuted-candidate exception (why C3 passes and one C2 orphan is exempt)

`PRIM-CANONICAL-33-SCENE-ANCHOR` is named in the corpus but is **not** an orphan: it is a tested-and-**refuted**
candidate, proven not to exist. Demanding a completion object for it would silently contradict its owning NO-GO.
The cert detects this data-driven from the registry's own phrasing (`REFUTED_RE = "PRIM-… does NOT exist"` on a
NO-GO row), exempts it from C2, and treats it in C3 as a legitimate "this completion class does not exist" no-go.

- `CLAIM_TO_LEAN_MAP.csv:428` — `D0-VNEXT-33-SCENE-ANCHOR-OWNER-001,…,NO-GO,"[vNext+1 master, Outcome D + spectral] … PRIM-CANONICAL-33-SCENE-ANCHOR does NOT exist (no scene-structure-preserving reduction; scale-independent spectral obstruction) … 34-1=33 is NOT a quotient."`
- `BOOK_02_MATHEMATICAL_PROOF_SPINE…:1301` — "So `PRIM-CANONICAL-33-SCENE-ANCHOR` does not exist
  (`D0-VNEXT-33-SCENE-ANCHOR-NOGO-001`); the scale and Xi primitives stay independent."

**Owned NO-GO respected:** cited and worked within — the cert never demands this refuted candidate be cataloged,
and never re-opens the no-go. This is exactly the kind of nuance that a naive "every named PRIM must be cataloged"
check would get wrong (an earlier draft did flag it as an orphan; the fix moved it to a documented exemption).

## 6. Fix summary (all proposals, none applied)

| gap set | count | fix class | risk / gate |
|---|--:|---|---|
| C1 unhomed proof-targets | 5 | append primitive/passport/external marker OR reconcile lean-vs-release status | low–med; G-C1.1 is a status reconciliation (F-02) |
| C2 orphans (F-14, registry-consumed) | 9 | add catalog rows to `TOTAL_EXTENSION_PRIMITIVES.csv` | low (content already in consuming notes) |
| C2 orphans (drifted parallel catalog) | 3 | declare a single canonical catalog; fold/rename or retire | med (policy call) |
| C2 misnomer | 1 (subset) | catalog under corrected id + `lane=external`; fix 2 citing notes (Lean = code-block draft) | low |
| C4 atlas ids absent from registry | 50 | per-id: register / rename / retire, per DESYNC_FIXLIST F-01…F-18 | mixed; several OWNER-GATED |
| C5 monotonicity | 0 (now PASS) | baseline pinned; keep it updated CONSCIOUSLY on every legitimate addition | — |

**After the fixes are applied and `frontier_dag.json` is regenerated,** re-run
`python3 _TASKS_CENTER_ATTACK/vp_register_exhaustiveness.py`. C3 and C5 already pass; C1/C2/C4 go green once the
proposals land. The cert is the acceptance test for "the register is now exhaustive."

## 7. Self-attack (skeptic pass — where this cert could be wrong)

- **"C4's 50 is over-counted."** Partly true by intent: some of the 50 are RENAMES (the id exists under a
  different name), not truly-missing obligations — DESYNC_FIXLIST reduces its Class-2 to "43 unique + 4 free-text".
  The cert deliberately reports the raw atlas-vs-registry gap and defers the rename/register/retire adjudication to
  the (already-written) fixlist. It is an over-approximation of the gap, never an under-approximation — safe for an
  exhaustiveness check whose failure mode must be "flags too much", not "misses a real gap".
- **"C1 accepts a prose `passport`/`external`/`ASSUMP` marker as sufficient homing."** This is a weak homing test:
  a claim could carry the word "external" for an unrelated reason and pass C1 spuriously. It trades false-negatives
  (spurious passes) for zero false-positives on the 5 it flags (each verified to carry NO such token). Tightening
  C1 to require a *named* external leg (the DAG's `EXACT-MISSING` rule) would raise the count toward the DAG's 11
  independent-residual claims — a stricter future variant, flagged here, not forced now.
- **"Scanning `D0_FINAL_NEW_PRIMITIVES.csv` is scope creep."** The task fixes `TOTAL_EXTENSION_PRIMITIVES.csv` as
  THE completion catalog; scanning the second file only SURFACES a drift (§3b), it never treats that file as
  authoritative. A reviewer could argue the 3 zero-consumer names should be dropped entirely rather than reported;
  the cert reports them because a silently-diverging second catalog is itself an exhaustiveness hazard.
- **"C5 baselines the failures too."** Correct and intended: the monotonicity guard pins the *current* set
  (including today's orphans) so that FUTURE vNext additions are the thing detected. It is not a closure claim; it
  is a drift alarm. When the §6 fixes retire/rename entries, C5 reports them as *removals* (noted, not failed).
- **Honest residual:** this cert proves the register is NOT exhaustive today; it does NOT prove that fixing the
  named gaps makes it exhaustive — only that these specific obligations are currently uncaptured. Exhaustiveness in
  the strong sense (no obligation exists anywhere outside the register) is not decidable from the corpus; C5 is the
  practical surrogate (nothing new enters unseen). This is a bridge assumption, labelled: **"the register namespace
  = registry ∪ atlases ∪ two primitive catalogs"** is the closed world the cert checks; obligations expressed in
  pure prose outside those files are out of scope and named here as the boundary of the guarantee.



