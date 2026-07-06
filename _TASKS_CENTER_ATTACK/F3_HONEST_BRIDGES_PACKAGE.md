# F3 HONEST-BRIDGES PACKAGE — consolidation deliverables (memo-only)

> **Status: PREPARED, NOT APPLIED.** Every text below is ready-to-apply by a later
> guarded integration. No registry row edited, no ledger row added, no `.lean` written,
> `053040` untouched, no commit. Prepared 2026-07-06. Every claim re-verified verbatim
> on disk this pass (file:line cited throughout).
>
> **No skeptic pass run** — consolidation of already-skepticked material, no new physics
> claim. Two source-tension flags found (FLAG-1 substantive wording, FLAG-2 minor line
> cite) — see §FLAGS at top because FLAG-1 changes the requested justification text.

---

## FLAGS (read first)

**FLAG-1 (substantive — the requested justification wording contradicts the source memo).**
The task brief suggested the justification phrase *"assembly-grade typing transfer across
§01.3/§01.11.3"*. The source memo's independent-skeptic pass **explicitly struck that
grade**: `CLOSE_GAP_W_MEMO.md:438-445` (E-CW-1, "the wound"): *"The memo called R-A an
'assembly-grade matched typing … the same grade the GAP-E skeptic granted for `:325`'.
FALSE parity … *Fix:* R-A re-graded to a **named external assembly-bridge** across the
§01.3/§01.11.3 layer boundary; the parity claim struck throughout"*. And
`CLOSE_GAP_W_MEMO.md:36-37`: *"R-A is therefore a **named external assembly-bridge**,
assembled across the §01.3/§01.11.3 layer boundary — weaker than owned"*. The package
below uses the **post-skeptic wording** ("named external assembly-bridge", NOT
"assembly-grade typing transfer"); re-introducing the struck grade in a ledger row would
re-commit exactly the over-grade the skeptic killed. The rest of the requested
justification ("no in-print name-match, unlike GAP-E's :836/:862/:67") matches the memo
verbatim and is kept.

**FLAG-2 (minor — a 4-line cite drift, content verified).** The memo's banner
(`CLOSE_GAP_W_MEMO.md:19`) and the GAP-W registry row's GROUPE tag
(`CLAIM_TO_LEAN_MAP.csv:545`) both cite the partition algebra as "`P_N + Q_N = I`,
`P_N Q_N = 0` (BOOK_01:37)". On disk the **algebra** is at `BOOK_01:33-34`
(`33: P_N + Q_N = I,` / `34: P_N Q_N = 0.`) and `:37` is the **naming** sentence
("`P_N` is the retained/readout projection. `Q_N` is the traced/archive projection.").
The memo's own P1 (`CLOSE_GAP_W_MEMO.md:109-113`) is internally correct ("with the
algebra stated three lines above (`:33-34`)"). Not a contradiction of substance —
content verified at the correct lines; the texts below cite `:33-34` (algebra) + `:37`
(naming) precisely.

---

## Verification base (all re-read on disk this pass)

| fact | where verified |
|---|---|
| Ledger schema `assumption_id,lean_name,lean_file,used_by_theorem,claim_id,assumption_type,status,justification,external_source_or_cert,failure_meaning` | `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv:1` |
| Ledger has **25 lines** (header + 24 rows); last = `ASSUMP-KERNEL-CHARGE-LOCALIZATION` at **line 25** | `wc`/`awk` on ledger, 2026-07-06 |
| **ASSUMP-\* ids do NOT get their own registry claim rows** — `grep '^ASSUMP' CLAIM_TO_LEAN_MAP.csv` = 0 hits over 558 lines; consumers reference them via `assumption_ids` + `uses_bridge_assumptions=True` (e.g. row 517) | `CLAIM_TO_LEAN_MAP.csv` (header line 1; row 517) |
| ASSUMP-KERNEL-CHARGE-LOCALIZATION row verbatim (the PHYSICS_DICTIONARY precedent) | `LEAN_ASSUMPTION_LEDGER.csv:25` |
| ASSUMP-WITHINZONE-LABELING-EXTERNAL is **DRAFT, memo-only** (not in the ledger); typed class C gauge-fixing | `SELECTOR_MECHANISM_REPORT.md:82,92`; `TORSOR_GAUGE_SYNTHESIS_MEMO.md:312-315` |
| GAP-W registry row (OPEN / PROOF-TARGET, EXACT-MISSING(2) = joints need registered ASSUMP ids; GROUPE[2026-07-06] CLOSE-GAP-W tag present) | `CLAIM_TO_LEAN_MAP.csv:545` |
| R-A definition + re-grade + reopening hook | `CLOSE_GAP_W_MEMO.md:299-307, 361-371, 438-445` |
| Hypercharge NO-GO row verbatim | `CLAIM_TO_LEAN_MAP.csv:361` |
| Hypercharge BL-bridge row verbatim (`LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, `uses_bridge_assumptions=True`, `assumption_ids=ASSUMP-KERNEL-CHARGE-LOCALIZATION`) | `CLAIM_TO_LEAN_MAP.csv:517` |
| Certs exist: `vp_hypercharge_anomaly_variety.py`, `vp_hypercharge_bl_direction_bridge.py` | `05_CERTS/` |
| `P_N + Q_N = I` / `P_N Q_N = 0` / naming / `F_N` | `BOOK_01:33-34, :37, :40` (+ `:183`) |
| Built Lean capstone `card_base_forced_conditional (m) (h_halt : 1 ≤ m) (h_nocopy : m < 2)` | `09_LEAN_FORMALIZATION/D0/Core/WitnessForcing.lean:69-73` |
| Assumption-Lean pattern (`structure …Assumption where statement : Prop; cited : statement`) | `D0/Bridge/Assumptions/KernelChargeLocalization.lean:22-24` |
| `close_gap_w_check.py` checks 0-8 (names + semantics) | `close_gap_w_check.py:48-103` |

---

# TASK 1 — R-A as an explicit ASSUMP row (ready-to-apply package)

## 1.0 Name decision — `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`

Recommended over the brief's `ASSUMP-CLASS-RECORD-ADDRESSABLE`. Justification: the
**entire content of R-A is the copula**. `CLOSE_GAP_W_MEMO.md:299-302` (the R-A box):
*"The un-owned typing that the re-detection class-record **IS** — not merely
**interacts-with** — an addressable registration … `:988` forces INTERACT-WITH, not IS"*.
A name without "IS" reads as "the class-record is addressable-adjacent/interacts with an
address", which is exactly the part that IS owned (`:988`) and needs no assumption. The
"IS" makes the id self-documenting about what is being imported. Sibling-style check:
matches the verb-phrase pattern of `ASSUMP-WITHINZONE-LABELING-EXTERNAL` /
`ASSUMP-KERNEL-CHARGE-LOCALIZATION` (noun-phrase-of-the-imported-fact), length in family
range. Fallback: the brief's name is acceptable; nothing below changes except the id
string.

## 1.1 Convention findings (checked, not assumed)

1. **Ledger-only, no registry claim row.** ASSUMP-\* ids never appear as `claim_id` rows
   in `CLAIM_TO_LEAN_MAP.csv` (grep `^ASSUMP` = 0/558). They live ONLY in
   `LEAN_ASSUMPTION_LEDGER.csv`; consuming registry rows carry
   `uses_bridge_assumptions=True` + the id in `assumption_ids` (dominant convention,
   e.g. `CLAIM_TO_LEAN_MAP.csv:517`). → Package = (b) ledger row + (c) consumer-row note;
   there is NO separate registry ASSUMP row to mint.
2. **Status column is uniformly `EXPLICIT`** (all 24 rows). Followed.
3. **`assumption_type` is a free-form vocabulary.** Closest precedents:
   `PHYSICS_DICTIONARY` (ledger:25 — an identification, not a forced identity) and
   `D0_INTERNAL_FORCING_TARGET` (ledger:21-23 — a D0-internal named target whose
   derivation is the open work, "not an external classical theorem"). R-A is a
   D0-internal **typing** target (an un-owned join inside BOOK_01, not an external
   theorem citation), so: **`D0_INTERNAL_TYPING_TARGET`** (new coinage, one word off the
   Iter20 pattern). Conservative fallback if the integrator wants zero new vocabulary:
   `D0_INTERNAL_FORCING_TARGET`.
4. **Lean carrier pattern**: `D0/Bridge/Assumptions/<Name>.lean` with
   `structure <Name>Assumption where statement : Prop; cited : statement`
   (verbatim pattern `KernelChargeLocalization.lean:22-24`). The lean_file below follows
   it; the file itself is a later F4-wave artifact (NOT written now), consistent with
   ledger rows 21-23 whose Lean carriers are structure fields.

## 1.2 (a)+(b) The ledger row — exact CSV, ready to append as line 26 of `LEAN_ASSUMPTION_LEDGER.csv`

```csv
ASSUMP-CLASS-RECORD-IS-ADDRESSABLE,D0.Bridge.BridgeAssumption.ClassRecordIsAddressableAssumption,D0/Bridge/Assumptions/ClassRecordIsAddressable.lean,card_base_forced_conditional,D0-GAP-W-WITNESS-PLUS-ONE-001,D0_INTERNAL_TYPING_TARGET,EXPLICIT,"[R-A, CLOSE_GAP_W_MEMO.md §3.3, post-independent-skeptic 2026-07-06] The re-detection class-record IS (not merely interacts-with) an addressable registration. A NAMED EXTERNAL ASSEMBLY-BRIDGE assembled across the BOOK_01 §01.3/§01.11.3 layer boundary: :253 types the record atom q as addressable at the primitive-dyad layer, :996 types the re-detection class as a physical object over records; the IS-join spanning the two layers is un-owned. :988 (CORE contradiction theorem) forces only INTERACT-WITH an addressable registration, never IS. NOT an assembly-grade matched typing (skeptic E-CW-1): no in-print name-match exists, unlike GAP-E's :836/:862/:67 (probe-confirmed). W-REC (owned architecture: P_N+Q_N=I :33-34/:37, single :1998 Q_N-writer) removes the alternative carrier but does NOT close the IS-gap. This is the forced-explicit-external-bridge honest closure (selector-M1-forbidden pattern), not an open-unattempted.",close_gap_w_check.py 9/9 rc=0 mutation-tested (checks 5-7 certify only the DERIVED entailment G1&G2&G3&W-REC=>W-ELEM; R-A itself is deliberately UN-certified - external bridge not computed fact),"If the class-record is NOT an addressable registration, W-ELEM reopens (demotes to narrated) and the window lower bound |V_base|=|Omega8|+1=9 loses its CONDITIONAL seal, reverting to GAP_W_SYNTHESIS_MEMO v2's narrated-W-ELEM state (no regression below that). Reopening hook: a maintainer scoping :253's q strictly to the primitive dyad blocks the bridge and demotes W-ELEM to narrated; conversely, owning the IS-typing or finding an in-print name-match upgrades the GAP-W seal to a full owned closure and retires this row."
```

Field-by-field verbatim anchors: assumption text = `CLOSE_GAP_W_MEMO.md:299-302`
(R-A box, quoted §1.0); ":988 forces INTERACT-WITH, not IS" = memo `:279-281, :364`;
layer-boundary assembly = memo `:287-289`; no in-print name-match ("the probe confirmed
NO in-print name-match exists", GAP-E's `:836/:862/:67` contrast) = memo `:291-297,
:440-443`; failure meaning + "no regression" = memo `:367-369` (ATT-W3: "the window
lower bound then rests on the synthesis memo's narrated W-ELEM — no regression");
reopening hook = memo `:304-307`; upgrade clause = memo `:369-371, :462-464`;
forced-external-bridge pattern = `SELECTOR_MECHANISM_REPORT.md:104` ("the honest closure
… is a FORCED explicit external bridge") — the precedent typing the brief calls the
"honest closure" pattern. `used_by_theorem` = the built capstone
`card_base_forced_conditional` (`WitnessForcing.lean:69`), whose `h_halt` support the
memo re-attributes to "W-REC … + R-A" (`CLOSE_GAP_W_MEMO.md:402-406`).

## 1.3 (c) GAP-W row cross-ref note — text to APPEND to `CLAIM_TO_LEAN_MAP.csv:545` notes field

```
R-A-REGISTERED[2026-07-06]: [F3 honest-bridges] the CLOSE-GAP-W residue R-A is promoted
to a registered ledger id ASSUMP-CLASS-RECORD-IS-ADDRESSABLE (LEAN_ASSUMPTION_LEDGER.csv
line 26, D0_INTERNAL_TYPING_TARGET, EXPLICIT): the un-owned IS-typing 'the re-detection
class-record IS (not merely interacts-with) an addressable registration', assembled
across the S01.3/S01.11.3 layer boundary; :988 forces INTERACT-WITH only; no in-print
name-match (unlike GAP-E's :836/:862/:67). This partially discharges EXACT-MISSING(2)
of the three-joint accounting UNDER THE GROUPE[2026-07-06] SUPERSESSION: the current
accounting is 1 owned-architecture fact (W-REC, needs the F4 Lean lift, NOT an ASSUMP)
+ 1 registered ASSUMP (this id). Upgrade path: once the F4 wave lands the W-REC lift
(partition + decidable OB-W1/OB-W2/OB-W3 legs) and the re-attributed capstone consumes
ASSUMP-CLASS-RECORD-IS-ADDRESSABLE explicitly, this row may move OPEN ->
LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS with uses_bridge_assumptions=True /
assumption_ids=ASSUMP-CLASS-RECORD-IS-ADDRESSABLE (precedent: row
D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001); until then lean_status stays OPEN /
release_status PROOF-TARGET. Reopening hook: maintainer scoping :253's q to the
primitive dyad blocks the bridge (W-ELEM demotes to narrated; no regression below the
synthesis-memo state).
```

(Registry hygiene per `MEMORY`/`d0-registry-source-of-truth`: apply to
`CLAIM_TO_LEAN_MAP.csv` + regen `theory_status_map.csv`/`theory_graph.json` via
`sync_theory_status_map.py`; never edit the generated files.)

## 1.4 (d) Consumers list

| consumer | how it consumes | change at integration time |
|---|---|---|
| `D0-GAP-W-WITNESS-PLUS-ONE-001` (`CLAIM_TO_LEAN_MAP.csv:545`) | its GROUPE[2026-07-06] state = lower bound SEALED CONDITIONAL ON R-A | append §1.3 note; later (F4) `assumption_ids` + `uses_bridge_assumptions=True` |
| `D0.Core.WitnessForcing.card_base_forced_conditional` (`WitnessForcing.lean:69-73`) | `h_halt : 1 ≤ m` — memo re-attributes its backing to "W-REC (owned architecture) + G2 (:988 CORE) + G3 (computed) + R-A" (`CLOSE_GAP_W_MEMO.md:402-406`); "R-A stays an explicit, un-discharged Lean hypothesis" (`:406, :417`) | F4 wave: docstring re-attribution + explicit `ClassRecordIsAddressableAssumption` hypothesis in the rewired capstone (§TASK-3 skeleton) |
| `close_gap_w_check.py` (checks 5-7) | certifies the DERIVED entailment; check 7 records "sealed GIVEN W-REC + the NAMED EXTERNAL ASSEMBLY-BRIDGE R-A … R-A itself is un-owned and NOT certified by this script" (`close_gap_w_check.py:90-96`) | none — already R-A-honest; becomes the `external_source_or_cert` |
| `D0-WINDOW-9-13-DISSOLVE-001` (`CLAIM_TO_LEAN_MAP.csv:546`) — **indirect** | carries `hbase=GAP-W (D0-GAP-W-WITNESS-PLUS-ONE-001)` as a named joint | inherits the conditionality automatically; no text change required (optional one-line pointer) |

---

# TASK 2 — Hypercharge F7 consolidation note (clean typed interface)

## 2.0 Probe facts, re-verified verbatim on disk (2026-07-06)

1. **`D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`** (`CLAIM_TO_LEAN_MAP.csv:361`) —
   `LEAN_PROVED`, release `NO-GO`, cert `vp_hypercharge_anomaly_variety.py` (exists,
   `05_CERTS/`). Verbatim: *"NO-GO: anomaly-freedom + the proposed {grav,su2,su3 linear,
   cubic} constraints leave a >=2-dim variety span{Y, B-L}, so the SM hypercharge row is
   NOT forced."* Rank fact verbatim: *"linear anomaly matrix … has rank 3 … => 6-3=3-dim
   solution space"*; independence verbatim: *"Y=(1/6,-2/3,1/3,-1/2,1,0) and
   B-L=(1/3,-1/3,-1/3,-1,1,1) BOTH satisfy grav=su2=su3=cubic=0 … and are Q-independent"*;
   the question-begging guard: *"Removing B-L requires imposing Y_nuRc=0 (SM convention,
   question-begging)."*
2. **`D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001`** (`CLAIM_TO_LEAN_MAP.csv:517`) —
   `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, `uses_bridge_assumptions=True`,
   `assumption_ids=ASSUMP-KERNEL-CHARGE-LOCALIZATION`, release
   `BRIDGE-ASSUMPTIONS-EXPLICIT`, cert `vp_hypercharge_bl_direction_bridge.py` (exists).
   Verbatim: *"Closes the hypercharge-direction obligation as a minimal bridge (NOT
   THE). Bridge Xi_Y = nu^c uncharged = nu_R in ker(A) = R2 graph->physics localization
   (MECH-LIMIT, not forced). Proven NECESSARY … + SUFFICIENT … + MINIMAL … Collapses
   2-dim span{Y,B-L} to hypercharge ray."* Second-assumption caveat present in-row:
   *"Caveat ASSUMP-NO-EXOTIC-FERMIONS (Costa PRD102(2020)115006 …; D0 excludes via fixed
   K(9,11,13))"* — note this caveat id is **named in the row but NOT a registered ledger
   id** (ledger grep: absent) — carried here honestly, see interface text.
3. **The gate** `ASSUMP-KERNEL-CHARGE-LOCALIZATION` (`LEAN_ASSUMPTION_LEDGER.csv:25`,
   `PHYSICS_DICTIONARY`, `EXPLICIT`). Justification verbatim: *"nu^c uncharged = nu_R
   localized in ker(A) is the R2 graph->physics map (MECH-LIMIT,
   D0-GRAPH-SPACE-NO-ISOMETRY); a physics-dictionary identification, NOT a forced D0
   identity; named explicitly, not promoted to Core."* Failure meaning verbatim: *"If
   nu_R is not kernel-localized, B-L stays gaugeable and the hypercharge direction is
   not fixed (2-dim anomaly-free freedom returns)."*
4. **Recent raises supply no localization datum — probe-verified 2026-07-06.** Row 361's
   two recent tags: `UPLIFT[2026-07-06]` (organizing-lemma filing: moduli =
   "charge-direction moduli span{Y,B-L} in the rank-3 anomaly kernel"; gauge-fixing leg
   explicitly typed *"B-ext: BL-DIRECTION bridge (ASSUMP-KERNEL-CHARGE-LOCALIZATION)"*;
   ends "row unchanged") and `RAISE[2026-07-06]` ("corollary-of
   D0-P-INVARIANT-MINIMAL-001") — neither supplies a kernel-localization datum. Row 517
   carries NO raise tag at all. The gate is untouched by the raise wave.

## 2.1 Ready-to-apply note — APPEND to `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` notes (`CLAIM_TO_LEAN_MAP.csv:361`)

```
F7-INTERFACE[2026-07-06]: [F3 honest-bridges consolidation] EXACT CURRENT STATE of the
hypercharge F7 slot, typed: (i) the NO-GO stands and is the floor - anomaly matrix rank
3, charge-direction freedom = 2-dim span{Y,B-L}, hypercharge NOT forced by
anomaly-freedom alone (this row, LEAN_PROVED, exact-Q); (ii) the ONLY discrete gate
between the 2-dim freedom and the hypercharge ray is the single registered assumption
ASSUMP-KERNEL-CHARGE-LOCALIZATION (LEAN_ASSUMPTION_LEDGER.csv:25, PHYSICS_DICTIONARY:
'nu^c uncharged = nu_R localized in ker(A)' - a physics-dictionary identification, NOT
a forced D0 identity), consumed by D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001
(LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS, proven NECESSARY+SUFFICIENT+MINIMAL - the gate is
single and minimal, not one-of-many); (iii) failure meaning: if nu_R is not
kernel-localized, B-L stays gaugeable and the 2-dim freedom returns (ledger:25
verbatim); (iv) recent raises supply no localization datum - probe-verified 2026-07-06
(this row's UPLIFT/RAISE[2026-07-06] tags re-file and cross-link only, 'row unchanged';
the bridge row carries no raise). NET: F7 = variety NO-GO + one named ASSUMP gate + its
failure meaning = a clean typed interface, NOT a vague open. Residual second caveat
lives on the bridge row (ASSUMP-NO-EXOTIC-FERMIONS, named in-row, not ledger-registered;
D0 excludes exotics via fixed K(9,11,13)).
```

## 2.2 Ready-to-apply note — APPEND to `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001` notes (`CLAIM_TO_LEAN_MAP.csv:517`)

```
F7-INTERFACE[2026-07-06]: [F3 honest-bridges consolidation] This row IS the single
discrete gate of the hypercharge F7 slot: it collapses the NO-GO's 2-dim span{Y,B-L}
(D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001, LEAN_PROVED) to the hypercharge ray through
exactly ONE registered assumption, ASSUMP-KERNEL-CHARGE-LOCALIZATION
(LEAN_ASSUMPTION_LEDGER.csv:25, PHYSICS_DICTIONARY - 'a physics-dictionary
identification, NOT a forced D0 identity'). Gate properties already proven in-row:
NECESSARY (Y,B-L independent anomaly-free, B-L charges nu^c) + SUFFICIENT (nu^c=0 =>
b=0 => span{Y}) + MINIMAL (nu^c unique coord reading b alone) - so the F7 residue is
EXACTLY this one localization datum, nothing else. Failure meaning (ledger:25): if nu_R
is not kernel-localized, B-L stays gaugeable, the 2-dim anomaly-free freedom returns.
Recent raises supply no localization datum - probe-verified 2026-07-06 (no
UPLIFT/RAISE tag on this row; the variety row's 2026-07-06 tags re-file only). Open
hygiene item carried honestly: the in-row caveat ASSUMP-NO-EXOTIC-FERMIONS is named but
NOT a registered ledger id (candidate for a later ledger registration or an explicit
K(9,11,13)-exclusion cross-ref; no new physics either way). NET: F7 = clean typed
interface (NO-GO floor + this single ASSUMP gate), not a vague open.
```

Both notes are additive (append-only to the `notes` field), change no status/cert/lean
columns, and per the registry rule apply to `CLAIM_TO_LEAN_MAP.csv` with regen of the
generated maps.

---

# TASK 3 — W-REC Lean-lift statement draft for the F4 wave (memo-only; NO .lean written)

## 3.0 Sources verified

- `BOOK_01:31-34` (code block): `H_N = H_N^ret direct_sum H_N^tr,` / `P_N + Q_N = I,` /
  `P_N Q_N = 0.` — the partition algebra. `:37`: "`P_N` is the retained/readout
  projection. `Q_N` is the traced/archive projection. `U_N` is the finite tick."
  `:40`: `F_N = P_N U_N^dagger Q_N U_N P_N.` (repeated `:183`).
- `close_gap_w_check.py:66-71` check 4 `WREC_CHANNEL_EXHAUSTIVE`: partition +
  retained-is-same-event (`:186`, `:8`) + "the single cross-event carrier is Q_N,
  written by the :1998 emission … a planted SECOND writer is DETECTED (control)".
- Decidable obligations named by the memo (`CLOSE_GAP_W_MEMO.md:414-417`): "OB-W1
  marker-averaging-is-address-blind (check 1), OB-W2 address-vs-trace type disjointness
  (check 3), OB-W3 averaging idempotent (check 6). The typing R-A stays an explicit
  Lean hypothesis; no over-claim."
- Existing capstone to rewire: `WitnessForcing.lean:69-73`
  `card_base_forced_conditional (m) (h_halt : 1 ≤ m) (h_nocopy : m < 2)`; precedent for
  kernel-cheap `decide` on `Fin 8`: `no_stationary_in_omega8` (`WitnessForcing.lean:47-48`).

## 3.1 Leg classification — what is decide-able vs what must stay a hypothesis

| leg | content | recommendation | why |
|---|---|---|---|
| L1 partition algebra | `P + Q = 1`, `P * Q = 0` on a CONCRETE finite model | **PROVABLE (decide/simp)** | fix the model (0/1 diagonal projections on the finite record support); the algebra is then kernel-decidable. The *identification* of `P`/`Q` with retained/traced (`:37`) is a book-contract CITATION (docstring), not a Lean claim — same style as OB-W1's docstring citation of `:1996` in the built module |
| L2 OB-W1 address-blindness | C8 orbit-average sends every `diag(e_a)` to uniform | **DECIDE-ABLE** — recommend ℤ-scaled: `∀ a, 8 • cAvg (marker a) = 1` over `Matrix (Fin 8) (Fin 8) ℤ` | avoids `ℚ` in `decide`; 8×8 over `Fin 8` is the exact size class of the built `no_stationary_in_omega8` precedent; mirrors check 1 |
| L3 OB-W2 type disjointness | no address marker is shift-invariant ∧ no nonzero shift-invariant matrix is a marker | **DECIDE-ABLE** (finite quantifiers over `Fin 8` markers + the 8-dim circulant basis) | mirrors check 3; both quantifiers finite |
| L4 OB-W3 idempotence | `cAvg (cAvg M) = cAvg M` on the matrix-unit basis | **DECIDE-ABLE** (ℤ-scaled: `8 • cAvg (8 • cAvg E) = 8 • (8 • cAvg E)` or prove `cAvg` is a projection by `Finset` algebra) | mirrors check 6's `avg_idempotent` leg; finite basis `Fin 8 × Fin 8` |
| L5 single-writer sweep | "the ONLY cross-event write into Q_N from the circulated sector is the `:1998` emission" | **EXPLICIT HYPOTHESIS** (`h_single_writer`), NEVER a Lean theorem | it is a CORPUS-EXHAUSTIVENESS fact (disk sweep, `CLOSE_GAP_W_MEMO.md §2.1`) — Lean cannot decide what BOOK_01 does not contain. Optionally a decidable SHADOW over a frozen in-file operator list (`E_Ω`, `F_N`, `Δ` with typed directions — uniqueness of the Q-codomain writer then decides), but list-completeness itself remains the hypothesis; do NOT let the shadow masquerade as the sweep |
| L6 G2 (`:988`) application | physicality ⇒ alters/constrains an addressable registration | **EXPLICIT HYPOTHESIS** (CORE contradiction theorem cited, not formalized this wave) | same treatment the built module gives W-BRIDGE-1′ |
| L7 R-A | the class-record IS an addressable registration | **EXPLICIT HYPOTHESIS** = the TASK-1 assumption structure `ClassRecordIsAddressableAssumption` | per memo `:406, :417`: "R-A stays an explicit, un-discharged Lean hypothesis (an external bridge, not an owned lemma)" |

## 3.2 Skeleton statement draft (memo-only — F4 wave writes the file)

```lean
-- D0/Core/WRecArchitecture.lean  (F4-wave target; NOT written this pass)
-- W-REC lift: CLOSE_GAP_W_MEMO §2 (owned architecture) + §7 (obligations OB-W1..OB-W3).
-- Module docstring must carry: partition algebra BOOK_01:33-34, naming :37, F_N :40/:183,
-- retained-is-same-event :186/:8, archive-is-cross-event :1995, single writer :1998,
-- Δ readout-side :465. Mirrors close_gap_w_check.py checks 1,3,4,6.

namespace D0.Core.WRecArchitecture

-- L1 (PROVABLE on the concrete model): the record-support partition.
-- Model: record support = retained ⊕ traced index set; P,Q the 0/1 diagonal projections.
theorem retained_traced_partition :
    P + Q = (1 : Matrix RecordSupport RecordSupport ℤ) ∧ P * Q = 0 := by decide
    -- (or `simp [P, Q, Matrix.diagonal]` if RecordSupport is larger than decide-cheap)

-- L2 = OB-W1 (DECIDE-ABLE, ℤ-scaled): the C8 orbit-average is address-blind.
theorem marker_average_address_blind :
    ∀ a : Fin 8, 8 • cAvg (marker a) = (1 : Matrix (Fin 8) (Fin 8) ℤ) := by decide

-- L3 = OB-W2 (DECIDE-ABLE): address positions and trace content are type-disjoint.
theorem addr_disjoint_from_trace :
    (∀ a : Fin 8, ¬ ShiftInvariant (marker a)) ∧
    (∀ c : CirculantBasis, c ≠ 0 → ¬ IsMarker c.toMatrix) := by decide

-- L4 = OB-W3 (DECIDE-ABLE): averaging is idempotent — the escape-closure leg (§3.2 of
-- the memo: a "separate downstream registration" reached through the trace inherits
-- blindness).
theorem avg_idempotent :
    ∀ e : Fin 8 × Fin 8, cAvg (cAvg (stdBasis e)) = cAvg (stdBasis e) := by decide

-- L5 (HYPOTHESIS — corpus sweep, not decidable): single Q_N-writer.
-- Optional decidable SHADOW over the frozen operator list {E_Ω:1998, F_N:40, Δ:465}:
--   theorem single_writer_shadow : (ownedOps.filter writesQFromCirculated) = [emission]
--     := by decide   -- honest ONLY with the docstring: list-completeness is the sweep.
def SingleQNWriter : Prop := ...  -- carried as hypothesis h_wrec

-- Capstone rewire (replaces the support attribution of h_halt; statement unchanged):
-- h_halt is now DERIVED-shaped from the W-REC legs + two explicit bridges, matching
-- CLOSE_GAP_W_MEMO §7: "h_halt : W-REC (P_N+Q_N=I, single :1998 writer) + :988 +
-- address-blindness + R-A".
theorem card_base_forced_wrec (m : ℕ)
    (h_wrec   : SingleQNWriter)                                -- L5, sweep
    (h_g2     : PhysicalityRequiresAddressable)                -- L6, :988 cited
    (h_ra     : D0.Bridge.ClassRecordIsAddressableAssumption)  -- L7, TASK-1 ASSUMP
    (h_halt   : 1 ≤ m)   -- now documented as backed by h_wrec + h_g2 + h_ra + L2/L3/L4
    (h_nocopy : m < 2) :
    Fintype.card Omega8 + m = 9 :=
  D0.Core.WitnessForcing.card_base_forced_conditional m h_halt h_nocopy

end D0.Core.WRecArchitecture
```

**Recommendations, explicit:** decide-able legs = **L2, L3, L4** (all `Fin 8`-finite,
ℤ-scaled to keep `decide` off `ℚ`; size class proven cheap by the built
`no_stationary_in_omega8`) **+ L1** on the concrete model. Hypothesis legs = **L5, L6,
L7** — L5 because corpus-exhaustiveness is not a Lean fact (shadow allowed, labelled),
L6/L7 because they are the declared bridges (L7 = the TASK-1 ledger id; wiring it as the
structure hypothesis is what later flips `D0-GAP-W-WITNESS-PLUS-ONE-001` to
`uses_bridge_assumptions=True` per §1.3). The capstone stays a thin re-export of the
built `card_base_forced_conditional` (`WitnessForcing.lean:69`) so `D0.All` sees ONE
forcing statement, not two competing ones. Honesty guard for the F4 implementer: do NOT
promote `h_halt` to a proved term — the derivation chain G1&G2&G3&W-REC⇒W-ELEM is
certified propositionally by `close_gap_w_check.py` check 5, but its Lean form needs the
un-owned R-A discharge and MUST stay hypothesis-shaped (memo `:406`).

---

# FINAL SUMMARY

- **TASK 1 (§1):** `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE` — full ledger CSV row (append as
  `LEAN_ASSUMPTION_LEDGER.csv:26`), convention verified (ledger-only; consumers via
  `assumption_ids`), GAP-W cross-ref note text, 4-entry consumers list.
- **TASK 2 (§2):** both hypercharge F7 rows re-verified verbatim; two append-only
  F7-INTERFACE note texts (variety NO-GO row + BL-bridge row) typing the slot as
  NO-GO floor + single ASSUMP gate + failure meaning + raises-supply-no-datum
  (probe-verified 2026-07-06); one hygiene item surfaced (`ASSUMP-NO-EXOTIC-FERMIONS`
  named in-row but not ledger-registered).
- **TASK 3 (§3):** W-REC lift legs classified (L1 provable-on-model; L2/L3/L4
  decide-able ℤ-scaled; L5 sweep-hypothesis with optional labelled shadow; L6/L7
  explicit bridges), skeleton statement drafted, capstone rewire = thin re-export of the
  built `card_base_forced_conditional`.
- **FLAG-1 (substantive):** the brief's suggested justification phrase "assembly-grade
  typing transfer" was struck by the memo's independent skeptic (E-CW-1); package uses
  the post-skeptic grade "named external assembly-bridge".
- **FLAG-2 (minor):** partition-algebra cite is `:33-34` (not `:37`, which is the naming
  sentence); banner/registry shorthand drift only, content verified.

Nothing applied: no registry/ledger/lean/cert edits, `053040` untouched, no commit.
