# GAP-W FORGING — the witness "+1": why the graph-birth base is `V₉ = Ω₈ ⊔ {ω₀}` with exactly ONE distinguished witness vertex (DRAFT v2, post-skeptic-#1: WOUNDED → all repairs applied accept-in-full)

**Status:** DRAFT candidate; no registry row edited; no .lean file added to the built tree (Lean drafts live as code blocks in this memo only). This is OB-1 of `WINDOW_9_13_FORCING_MEMO.md` (Route B obligations ledger) — the EASY half of the dissolve-window residual. GAP-E (extension completeness) is NOT attempted here.

**Pre-flight run:** `WITNESS`, `OMEGA8`, `HALT`, `FIRST-INSTANCE` — owners found: D0-OMEGA8-001 (`omega8_cardinality`), D0-OMEGA8-CENTER-001 (`omega8_center_collapse`), D0-IM-004 (`witness_halting_cert`, `D0.Topology.WitnessHalting`), D0-IM-005 (`fractal_continuum_witness_halting_corrected`); FIRST-INSTANCE has **no registry row** (`first_instance_canonical` is a Lean-only lemma inside D0-TOWER-STOP-NOEXT-001's module). No existing row owns "witness +1 necessity". Cross-references only; no duplication.

**Companion check:** `_TASKS_CENTER_ATTACK/gap_w_witness_check.py` — **10/10** check() calls PASS, rc=0 (~7 independent: checks 8/9/10 re-read the dichotomy-sweep function of check 7; count taken from the script's own counter, stated per the E1 miscount lesson of the window memo).

**Verdict in one line (post-skeptic-#1):** `|V_base| = |Ω₈| + 1 = 9` is **FORCED GIVEN THREE named joints** — **W-BRIDGE-1′** (the contract's *stable re-detection class* `:1166.5` realized as **≥ 1** stationary marked base element; narrated ×3 A1/A2/A3; uniqueness NOT in this joint — delivered by the kill matrix), **W-T1** (copy-catalogue schema instantiated on marks; Lean arithmetic owned, instantiation named), and **W-BIT** (the `:1539` no-further-bit quote scope-transferred to labels on adjoined marks; load-bearing by toggle; fallback narration `:1556`). The 8-kill and 10-kill are separate and separately grounded; the halt-QUOTIENT layer is CONTRACT-owned (§II.1), but the halt-proper lands at **+0** in two owned texts (`:846`, `:858` — adverse, repair E-GW-1): GW-E survives on the re-detection sliver. WOUNDED, not killed — repair log at end.

## Claim GW (DEF-0.2.2 form, candidate)

**GW.** A role-complete reusable base must contain **exactly one** distinguished stationary (halt/witness) element beyond the signed role shell: `|V_base| = |Ω₈| + 1 = 9`. Decomposed into two independent kill obligations plus one existence obligation:

- **GW-E (existence, ≥ 1 — the "8-kill"):** a base with NO witness (`V₈ = Ω₈`, card 8) is inadmissible — the halt/readout event has nothing stationary to close against, because the owned circulation acts on Ω₈ without fixed points.
- **GW-U (uniqueness, ≤ 1 — the "10-kill"):** a base with TWO witnesses (card 10) is inadmissible — a second stationary marked element is either an indistinguishable copy (⇒ nontrivial copy-symmetry ⇒ external catalogue ⇒ ⊥M1, reusing CASE-2 of the no-extension no-go — joint W-T1) or a distinguishable one (⇒ a further marking bit beyond the sign bit ⇒ exogenous orientation catalog, BOOK_01:1539 — **scope-transfer joint W-BIT**, repair E-GW-2).
- **GW-H (halt necessity):** the readout/halt event itself is required (reusability/record) — the layer below GW-E; ownership status established in §I.B/§II.1. NB (repair E-GW-1): the halt-proper lands at +0 in `:846`/`:858`; the vertex realization belongs to the RE-DETECTION layer, not the halt layer.

*Honest scope declared upfront:* this memo FORGES the argument from owned parts and marks every non-owned joint by name. It does not claim GW is Lean-proved; the Lean skeleton (§IV) enumerates what would be. Candidate language throughout.

## I. Owned pre-facts (verbatim, file:line)

### A. The witness-necessity narrations (the layer the window memo called "one-line")

**A1.** `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:1541-1545` (§01.20):

> "A reusable shell also requires a stationary marked witness section `ω0`. Hence
> V_9=\Omega_8\sqcup\{\omega_0\}, \qquad |V_9|=9."

**A2.** `BOOK_01…md:1987-1990` (§01.24 "Mobius-Witness topological halting"):

> "The witness/basepoint \(\omega_0\) gives the first addressable graph-birth shell \[ V_9=\Omega_8\sqcup\{\omega_0\}. \]"

**A3.** `BOOK_01…md:1993` (§01.24 — richer than the window memo recorded):

> "Continuous circulation inside \(\Omega_8\) accumulates the logarithmic trace gradient. The finite event occurs when the circulation closes against \(\omega_0\); this is the terminal halt quotient."

**A4.** `BOOK_01…md:1996` (§01.24, Witness Halt Proof — the full-cycle traversal, load-bearing for §II):

> "Because the trace gradient has traversed the full signed role cycle before halt, the emitted archive trace is an orbit-averaged shell emission over the group \(G_8\) of symmetries of \(\Omega_8\)"

**A5.** The alternatives narration, `BOOK_01…md:1556` (§01.20):

> "The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10` without losing direct/return capacity, and `V13` cannot be replaced by `V12` without losing one terminal role."

**A6.** Cross-memo pre-owners (cited, not re-derived): `M2_PHASE_LABELING_MEMO.md:94-96` (pre-fact 3 quotes A1+A3 as the basepoint owners); `T2_PRIME_TYPE_FORCING.md:15` ("**P1.** `V₉ = Ω₈ ⊔ {ω₀}` — zone 9 is the unique zone hosting the terminal role cycle").

### B. The halt-quotient CONTRACT layer (sweep finding: the necessity is NOT only narration)

The window memo recorded GAP-W's necessity as "one sentence of necessity each; no Lean owner". The sweep finds the *halt* half of the necessity sits in the admissibility CONTRACT, in five places:

**B1.** `BOOK_01…md:296` (§01.4, D0-admissible morphisms — the contract sentence):

> "A morphism is D0-admissible only if it is visible through finite stages, has a halt quotient, produces a positive quadratic response, respects direct/return asymmetry, and does not introduce a second hidden calibration section."

**B2.** `BOOK_01…md:360-367` (descent obligations, numbered list):

> "5. **halt quotient:** the comparison has a terminal finite quotient, rather than an infinite request for metadata;
> 6. **single section:** dimensionful external representatives factor through the declared D0 section, not through a hidden second scale."

**B3.** `BOOK_01…md:465` (§01.5):

> "The halt quotient is the statement that a registration is completed when further refinement cannot change the finite event class without violating the D0 admissibility constraints."

**B4.** `BOOK_01…md:1166` (finite obligations list): "5. halt quotient and stable re-detection class;" — the halt class must be *stably re-detectable* (addressable).

**B5.** `BOOK_01…md:858` (§01.7 apparatus, **Quotient** paragraph) — **RECLASSIFIED ADVERSE per skeptic #1 (repair E-GW-1):** the halt LANDS on the 8-element signed terminal role algebra (+0 capacity); V₉ is constructed "only after" — a sequencing text, not a +1-realization text:

> "The quotient is the halt from unresolved continuum metadata to the finite signed terminal role algebra.  The construction of the finite incidence graph marker `V_9` comes only after this quotient."

**B5a (adverse, found by skeptic #1).** `BOOK_01…md:846` (§01.7 apparatus, **Support** paragraph) — a second +0-landing text: the halt-quotient output is the FOUR-role algebra, no witness vertex:

> "**Support.**  The support is the terminal four-role readout algebra obtained after the `\varphi` halt quotient."

**B6.** `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:177` (Finite Holographic Self-Reading Principle):

> "The detector must read itself autonomously — hidden states and external memory backgrounds are strictly forbidden."

**B7.** Corroborating pattern only (NOT a vertex-count owner): `BOOK_01…md:491`: "**Single halt.** The primitive audit has one direct exposure and one positive self-return." — "single" here is about the audit `p+p²=1`, cited as pattern, nothing more.

### C. The bit-inventory owner (load-bearing for the 10-kill)

**C1.** `BOOK_01…md:1530-1537` (§01.20): "The four roles are not a list to be chosen — they are forced as the minimal self-sufficient act of record: reading (A), read (B), trace (C), reference (D). Fewer than four leaves the act without a distinguishable record, or requires an external memory to hold the missing role. That is the catalog M1 forbids."

**C2.** `BOOK_01…md:1539`:

> "The sign bit `{+,−}` is the irreversibility of write/erase; it is the one bit that distinguishes the act from its undo, and no further bit can be added without an exogenous orientation catalog. Hence `Ω8 = ABCD × {±}`, `|Ω8|=8`"

Owned bit inventory: exactly 3 bits (two role dyads + sign), and `|Ω₈| = 2³ = 8` **exhausts** it — any owned-bit-distinguishable element IS a signed-role element.

### D. The reusable Lean lemmas — located, quoted, and what they ACTUALLY prove

**D1.** `09_LEAN_FORMALIZATION/D0/Tower/NoExtension.lean:44-48`:

```
/-- **CASE 2 / repeat needs a catalogue.** `≥2` identical copies carry a nontrivial copy-
permutation symmetry: `|S_2| = 2 > 1`, so there is no canonical copy and selecting one is an
external catalogue ⇒ `⊥M1`. -/
theorem repeat_has_nontrivial_copy_symmetry : 1 < Fintype.card (Equiv.Perm (Fin 2)) := by
  native_decide
```

Lean content: the arithmetic `1 < |S₂|`. The `⊥M1` step (copy-choice = external catalogue) is the **docstring-declared reading**, owned at module level (`NoExtension.lean:15-17`, which itself declares the schema cross-class: "Same forcing as `Ω₈≅Q₈` via Dedekind, BOOK_01 §01.7.1A").

**D2.** `NoExtension.lean:50-52`:

```
/-- A single first instance is canonical: `|S_1| = 1` (no catalogue) — the no-go bites only on
repeats `(n≥2)`, not on first instances. -/
theorem first_instance_canonical : Fintype.card (Equiv.Perm (Fin 1)) = 1 := by native_decide
```

**Precision (answers a pre-registered parent attack):** `first_instance_canonical` does **NOT** kill the second witness. It proves `|S₁| = 1`: the *single* witness needs no catalogue — the **no-overfire certificate** (without it, the copy-kill logic would threaten V₉ itself). The V10-kill is carried by D1 (copy branch) + C2 (bit branch). The window memo's phrase "one witness is canonical by `first_instance_canonical`" is correct only in this no-overfire sense.

**D3.** `D0/Core/FiniteTypes.lean:9-16, 24-28`: `Witness := PUnit`, `V9 := Sum Omega8 Witness`; `card_omega8 = 8` (:24), `card_v9 = 9` (:27). The decomposition is type-level owned; the necessity of the `Witness` summand is what this memo forges. Also `D0/Core/DyadABCD.lean:17` (`omega8_cardinality`, D0-OMEGA8-001).

**D4.** `D0/Topology/WitnessHalting.lean` (D0-IM-004) — read in full. What it proves: `emissionDiag = diag(1..8)`, `shiftMat k` = cyclic shift matrices (:33-37), orbit average `E = (9/2)·I` (:54-55), shift invariance (:57-59), packaged as `witness_halting_cert` (:64-70). Its own scope clause (:22-24):

> "**Scope (honest).** The finite linear-algebra core (the orbit average is the scalar `(9/2)·I`, and is shift-invariant) is proved here. The *interpretation* — that this fixed point IS a "topological halting quotient" of the Möbius witness dynamics — is the modeling reading and stays in the cert."

Two facts matter for GAP-W: (i) its fixed point lives in **operator space**, not a stationary vertex — it exists over pure `Fin 8` with NO witness, so it cannot force the `+1` (computed as NC in §III); (ii) its `shiftMat` is the **owned Lean model of the circulation** — the translation action — which §II's freeness computation consumes.

### E. Negative sweep — what does NOT own witness necessity (confirming and extending skeptic #1)

- `WitnessHalting.lean` — interpretation clause quoted in D4; orbit-average arithmetic only.
- `05_CERTS/vp_mobius_witness_topological_halting.py:9-10` — builds `v9 = omega8 + [("omega0","witness")]` **by hand** and asserts `len(v9) == 9`; the witness enters by construction, necessity untested.
- `05_CERTS/vp_v1141_abcd_omega8_v9_phi_capacity.py:63-64` — the V8/V10 exclusion checks are `8==Omega8 and V9==Omega8+1` and `10>V9` — content-free on necessity (window memo trap (b)/(f), confirmed).
- `05_CERTS/vp_continuum_from_fractal_tick.py` (D0-IM-005 "fractal continuum witness halting") — **zero** occurrences of "witness" in the cert body; despite the registry title, it does not touch witness necessity.
- Registry pre-flight: no row owns "witness +1 necessity"; FIRST-INSTANCE has no row at all.

## II. The forging — every step tagged {OWNED-CONTRACT / OWNED-NARRATED / OWNED-LEAN / COMPUTED / NAMED-NEW}

### II.1 GW-H — halt necessity: contract-owned, not narration

The parent's pre-registered question "is the halt element's necessity owned physics or narration?" **splits**:

- The necessity of a **halt quotient** is an admissibility *criterion* of the theory — the contract sentence B1 (`:296`), descent obligation 5 (B2, `:366`), the registration-completion reading (B3, `:465`), and the re-detection obligation (B4, `:1166`). **Tag: OWNED-CONTRACT.** A D0 object without a halt quotient is not inadmissible-by-argument, it is inadmissible-by-definition-of-admissible.
- **BUT (repair E-GW-1): the halt-proper does NOT deliver the vertex.** Two owned texts land the halt quotient at **+0 capacity**: B5a `:846` (output = the four-role readout algebra) and B5 `:858` (output = the signed terminal role algebra; V₉ "only after" — sequencing). Any bridge from "halt quotient" directly to "+1 vertex" is contradicted by these texts.
- What the contract couples to the halt is a **stable re-detection class** (B4 `:1166.5`), and THAT layer is where the +1 is narrated: A1 (`:1541` "REUSABLE shell … stationary marked witness section"), A2 (`:1987-1990` "first ADDRESSABLE graph-birth shell"), A3 (`:1993` "closes against ω₀"). The realization of the re-detection class as ≥ 1 stationary marked base element is the joint. **Tag: OWNED-NARRATED ×3, named `W-BRIDGE-1′` below.**

### II.2 GW-E — the 8-kill (`V₈ = Ω₈` inadmissible), forged chain

| step | statement | tag | owner |
|---|---|---|---|
| E1 | any admissible registration has a halt quotient | OWNED-CONTRACT | B1 `:296`, B2 `:366.5` |
| E2 | the halt class must be stably re-detectable (addressable) *within* the finite support — no external memory may hold it | OWNED-CONTRACT | B4 `:1166.5` ("stable re-detection class") + B6 BOOK_00`:177` ("external memory backgrounds are strictly forbidden") |
| E3 | **W-BRIDGE-1′ (restated per E-GW-1/E-GW-3):** the stable RE-DETECTION class (E2) is realized as **≥ 1** stationary marked base element ω₀ ("requires a stationary marked witness section"; "first addressable graph-birth shell"; "the circulation closes against ω₀") — uniqueness NOT part of this joint (delivered by §II.3); the halt-proper is NOT the realizer (it lands +0: B5a `:846`, B5 `:858` — adverse, logged) | **OWNED-NARRATED (the load-bearing joint)** | A1 `:1541`, A2 `:1987-1990`, A3 `:1993` (×3); adverse: B5a `:846`, B5 `:858` |
| E4 | the circulation traverses the FULL signed role cycle before halt | OWNED-NARRATED (§01.24 Witness Halt Proof) + OWNED-LEAN model (`shiftMat`, the translation action) | A4 `:1996`; `WitnessHalting.lean:35-37` |
| E5 | a full-cycle (8-cycle) action on Ω₈ is fixed-point-free: NO element of Ω₈ is stationary under any nontrivial circulation step | **COMPUTED** (checks 3, 4; Lean-able by `decide`, §IV) | `gap_w_witness_check.py` FULL_CYCLE_FIXED_POINT_FREE, Q8_LEFT_TRANSLATION_FREE |
| E6 | hence the stationary marked element exists (E1–E3) and lies OUTSIDE Ω₈ (E4–E5): `V_base ⊋ Ω₈`, `\|V_base\| ≥ 9`; V₈ dies | forced GIVEN E3 | — |

**Status: GW-E = FORCED-GIVEN-W-BRIDGE-1′.** The computable half (E5) is new but decidable; the contract half (E1–E2) is owned; only E3 is narrated (three anchors A1/A2/A3 — with TWO adverse +0 texts on the halt-proper side logged, so the joint rides the re-detection sliver, not the halt).

### II.3 GW-U — the 10-kill (two witnesses inadmissible), forged dichotomy

Setup: suppose the base is `Ω₈ ⊔ {ω₀, ω₁}` with both adjoined elements stationary marked sections. Excluded middle on distinguishability:

| branch | statement | tag | owner |
|---|---|---|---|
| U1 (copies) | ω₁ indistinguishable from ω₀ ⇒ the pair carries the copy-symmetry `S₂`; `1 < \|S₂\|` ⇒ no canonical copy ⇒ copy-choice = external catalogue ⇒ `⊥M1` | **OWNED-LEAN** (arithmetic) + docstring-owned reading; schema transfer to marks = **NAMED-NEW `W-T1`** | `repeat_has_nontrivial_copy_symmetry` (`NoExtension.lean:47`); reading `:44-46,:15-17`. **NB (skeptic strengthening S3): A5 `:1556` does NOT back this branch** — its "extra hidden MARKER" wording fits the bit/marker branch (U2b); the copy branch rests on W-T1 alone |
| U2a (distinguished by owned bits) | the owned bit inventory is 3 bits, exhausted by `\|Ω₈\| = 2³`; an owned-bit-distinguishable element IS a signed-role element, and every signed-role element is on the full cycle (E4), hence NOT stationary ⇒ ω₁ is not a witness — contradiction | OWNED (C2 inventory + E5 freeness) + assembly **NAMED-NEW** | C2 `:1539`; check 1 (`8 = 2·2·2`); checks 3-4 |
| U2b (distinguished by a new bit) | a 4th distinguishing bit is exogenous: "no further bit can be added without an exogenous orientation catalog" ⇒ `⊥M1` | **NAMED-NEW joint `W-BIT` (retagged per E-GW-2):** the `:1539` quote is owned for Ω₈'s CONSTRUCTION (adding bits to the signed-role space); applying it to LABELS on adjoined marks is a scope transfer this memo makes — load-bearing by toggle (drop it ⇒ labeled-V₁₀ survives) | C2 `:1539` (transferred); fallback narration A5 `:1556` ("extra hidden marker" — fits THIS branch, S3); corroborated by B6 `:177` and — pattern-level only — B1 `:296` + B2 `:367` |
| U3 | in all branches `⊥` ⇒ at most one witness; with GW-E: **exactly one**; `\|V_base\| = 8 + 1 = 9` | forced GIVEN W-T1 (U1) — U2a/U2b close the escape routes | — |

**No-overfire check (essential):** the kill must not fire at `m = 1`: `\|S₁\| = 1` — **OWNED-LEAN** `first_instance_canonical` (`NoExtension.lean:52`). The single witness needs no catalogue; V₉ survives its own kill criterion (check 9).

**Status: GW-U = FORCED-GIVEN-{W-T1, W-BIT}** (repair E-GW-2: TWO joints here, not one). W-T1: the CASE-2 schema instantiated on marks instead of zones — a *third* instance of a schema the module itself already applies cross-class; `:1556` does NOT back it (S3). W-BIT: the `:1539` scope transfer, load-bearing by toggle, with `:1556` as its fallback narration. U2a uses only owned inventory + computed freeness (no new joint).

### II.4 Net verdict on GW (post-repair)

`|V_base| = |Ω₈| + 1 = 9` is **FORCED GIVEN THREE named joints** (repair E-GW-2):

- **W-BRIDGE-1′** (8-kill side): the contract couples the halt quotient with a stable re-detection class (`:1166.5`, contract-owned); the joint is the realization of THAT class as **≥ 1** stationary marked base element (narrated ×3: A1, A2, A3). The halt-proper lands at +0 (`:846`, `:858` — adverse texts, logged, E-GW-1). Uniqueness is NOT in this joint (E-GW-3).
- **W-T1** (10-kill, copy branch): the copy-catalogue schema (`≥2` indistinguishable copies ⇒ `⊥M1`) instantiated on adjoined marks (Lean arithmetic owned; reading owned at module level; instantiation named; `:1556` does NOT back this branch — S3).
- **W-BIT** (10-kill, bit branch): `:1539`'s no-further-bit scope-transferred from Ω₈'s construction to labels on adjoined marks (load-bearing by toggle; fallback narration `:1556`).

Ownership remains stronger than the window memo recorded (the halt-QUOTIENT layer is CONTRACT; the computable halves are computed and Lean-able), but weaker than this memo's v1 claimed (repair log): the halt-proper is +0 in two owned texts, and the bit branch is a transfer, not a direct quote application. **Not claimed: unconditional forcing.**

## III. Computation — `gap_w_witness_check.py`, 10/10 check() calls PASS (rc=0)

Count from the script's own counter: **10** `check()` calls; **~7 independent** (checks 8, 9, 10 re-read the sweep function of check 7 — stated to avoid an E1-style miscount). Exact integer/rational arithmetic throughout (`fractions.Fraction`, no floats).

Conclusion-failing power, per check:

1. `OWNED_CARD_CHAIN` — **definition mirror** of `card_omega8`/`card_v9` (labeled so per E-GW-4); fails only if the mirror is miscoded or the type model changes — no independent conclusion-failing power.
2. `Q8_TABLE_IS_GROUP` — the explicit Q₈ table: closure, associativity (512 triples), identity, inverses, non-abelian, `Z(Q₈) = {±1}`. Fails if the owned identification's object is mis-built.
3. `FULL_CYCLE_FIXED_POINT_FREE` — **the 8-kill core**: every nontrivial shift on the 8 signed roles has zero fixed points; any 8-cycle is fixed-point-free. A single fixed point would break GW-E.
4. `Q8_LEFT_TRANSLATION_FREE` — same conclusion in the group model, computed on the table (`g·x = x` has no solution, `g ≠ 1`).
5. `NC_CONJUGATION_MODEL_BREAKS_8KILL` — registered model-dependence: under a CONJUGATION reading of "circulation", the center `{±1}` is stationary INSIDE Ω₈ and the +1 would be unforced. Documents what GW-E leans on (the owned translation/full-cycle model). Defense in §V ATT-4.
6. `NC_OPERATOR_FIXED_POINT_NEEDS_NO_WITNESS` — over-claim guard, exact rationals: `E = (1/8)ΣP_kFP_kᵀ = (9/2)·I`, shift-invariant, over PURE Ω₈ (no witness vertex). So `witness_halting_cert` does NOT force the +1 — computational confirmation of skeptic #1's finding; any stronger reading of D0-IM-004 dies here.
7. `TEN_KILL_DICHOTOMY_SWEEP` — bases `B_m = Ω₈ ⊔ {m marks}`, m = 0..3, criteria C-HALT (m ≥ 1), C-COPY (`m! = 1` for unlabeled marks), C-BIT (labels need a 4th bit, `:1539`): survivors = `{m=1}` exactly; kills: m=0 by C-HALT, m=2,3 by C-COPY. **The criteria are the memo's forging** — a skeptic who rejects a criterion rejects the sweep (registered honestly in the script docstring).
8. `NC_FAKE_TEN_MUST_FAIL` — the mandated negative control: 10-as-copies dies by C-COPY, 10-as-labeled dies by C-BIT (NB per E-GW-4: re-reads check 7's criteria — fails only via a criteria-encoding bug, not independently).
9. `FIRST_INSTANCE_NO_OVERFIRE` — `|S₁| = 1`; the copy-kill does not fire at m = 1 (same E-GW-4 caveat: a re-read of the sweep function).
10. `KILLS_ARE_INDEPENDENT` — V₈ dies ONLY by C-HALT; V₁₀ dies ONLY by C-COPY/C-BIT (halt satisfied): the 8-kill and 10-kill are separate obligations, mirroring §II.2/§II.3's separate treatment.

## IV. Lean skeleton (candidate DRAFT — memo-only, NOT added to the built tree)

The honest target is **not** an unconditional `card_base_forced : |V_base| = 9` — that would smuggle W-BRIDGE-1′, W-T1 and W-BIT. The achievable statement is the conditional shell plus the decidable new lemma, with the three joints as *named hypotheses*:

```lean
-- GAP-W skeleton (OB-1 of WINDOW_9_13_FORCING_MEMO Route B). Status: DRAFT, pre-skeptic,
-- not built, not registered. Obligations OB-W0..OB-W5 enumerated below.
import D0.Core.FiniteTypes
import D0.Tower.NoExtension
import Mathlib.Tactic

namespace D0.Core.WitnessForcing
open D0

/-- OB-W0 (OWNED, reuse): pointed-shell arithmetic — `|V₉| = |Ω₈| + 1`.
    Reuses `card_v9` (FiniteTypes.lean:27) and `card_omega8` (:24; = `omega8_cardinality`,
    DyadABCD.lean:17, D0-OMEGA8-001). -/
theorem base_card_arith : Fintype.card V9 = Fintype.card Omega8 + 1 := by
  rw [card_v9, card_omega8]

/-- OB-W1 (NEW, decidable — the computable half of the 8-kill): the full signed role
    cycle is fixed-point-free on Ω₈ — nothing inside Ω₈ is stationary. Owned circulation
    model: `WitnessHalting.shiftMat` (translation), BOOK_01:1996 (full-cycle traversal).
    Mirrors checks 3-4 of gap_w_witness_check.py. -/
theorem no_stationary_in_omega8 : ∀ k : Fin 8, k ≠ 0 → ∀ x : Fin 8, x + k ≠ x := by
  decide

/-- OB-W2 (OWNED, reuse — no-overfire): `first_instance_canonical :
    Fintype.card (Equiv.Perm (Fin 1)) = 1` (NoExtension.lean:52). The single adjoined
    witness needs no catalogue: the copy-kill does not fire at m = 1. -/
-- reuse D0.Tower.first_instance_canonical

/-- OB-W3 (OWNED, reuse — copy branch of the 10-kill): `repeat_has_nontrivial_copy_symmetry :
    1 < Fintype.card (Equiv.Perm (Fin 2))` (NoExtension.lean:47); ⊥M1 reading owned in the
    module docstring (CASE-2 schema). Instantiation on witness marks = W-T1 (named). -/
-- reuse D0.Tower.repeat_has_nontrivial_copy_symmetry

/-- OB-W4 = W-BRIDGE-1′ (NAMED, not Lean-owned; restated per E-GW-1/E-GW-3): the contract
    couples the halt quotient with a STABLE RE-DETECTION CLASS (BOOK_01:1166.5; the halt-
    quotient necessity itself is contract-owned :296/:366.5). The halt-PROPER lands at +0
    (:846/:858 — adverse). What is narrated (:1541, :1987-1990, :1993 — ×3) is the
    realization of the re-detection class as ≥ 1 stationary marked base element.
    Enters below as (h_halt : 1 ≤ m) ONLY — uniqueness is OB-W3 + OB-W5, NOT this joint. -/

/-- OB-W5 = W-BIT (NAMED — third joint, per E-GW-2, NOT a direct quote application):
    BOOK_01:1539's "no further bit" is owned for Ω₈'s CONSTRUCTION; applying it to LABELS
    on adjoined marks is a scope transfer this memo makes. Toggle: drop W-BIT ⇒ labeled-V₁₀
    survives (load-bearing). Fallback owner: :1556 "extra hidden marker" (fits this branch,
    S3). Branch U2a still closes by OB-W1 (owned-bit elements are on the cycle, hence not
    stationary). -/

/-- **Conditional capstone (honest form).** GIVEN the joints as hypotheses on the number
    `m` of adjoined stationary marks — `1 ≤ m` (re-detection realization, W-BRIDGE-1′) and
    `m < 2` (copy/bit kills, OB-W3 + OB-W5) — the base cardinal is forced:
    `|Ω₈| + m = 9`. The arithmetic shell is trivial BY DESIGN: all forcing content
    lives in the named joints, none is hidden in the proof. -/
theorem card_base_forced_conditional (m : ℕ)
    (h_halt : 1 ≤ m)      -- W-BRIDGE-1′: at least one stationary mark (8-kill)
    (h_nocopy : m < 2) :  -- W-T1 + W-BIT: at most one (10-kill)
    Fintype.card Omega8 + m = 9 := by
  rw [card_omega8]; omega

/-- Sanity corollary: the forced base IS the owned V₉ count. -/
theorem forced_base_is_v9 (m : ℕ) (h1 : 1 ≤ m) (h2 : m < 2) :
    Fintype.card Omega8 + m = Fintype.card V9 := by
  rw [card_base_forced_conditional m h1 h2, card_v9]

end D0.Core.WitnessForcing
```

**Obligations ledger (owned vs new):**

| OB | Content | Status |
|---|---|---|
| OB-W0 | `\|V₉\| = \|Ω₈\| + 1` arithmetic | **OWNED-Lean reuse**: `card_v9`, `card_omega8` / `omega8_cardinality` (D0-OMEGA8-001) |
| OB-W1 | no stationary element inside Ω₈ (full-cycle freeness) | **NEW-decidable** (`decide`); model owned: `WitnessHalting.shiftMat` + BOOK_01:1996; computed (checks 3-4) |
| OB-W2 | no-overfire at m = 1 | **OWNED-Lean reuse**: `first_instance_canonical` (NoExtension.lean:52; no registry row of its own) |
| OB-W3 | copy branch of 10-kill | **OWNED-Lean reuse**: `repeat_has_nontrivial_copy_symmetry` (NoExtension.lean:47) + module-docstring ⊥M1 reading; instantiation = W-T1 (NAMED) |
| OB-W4 | re-detection class realized as ≥ 1 stationary mark | **NAMED (W-BRIDGE-1′)**: coupling contract-owned (B4 `:1166.5`; halt-quotient necessity B1/B2); realization NARRATED ×3 (A1-A3); adverse +0 texts B5a `:846`/B5 `:858` logged (E-GW-1); uniqueness NOT here (E-GW-3) |
| OB-W5 | labels on marks need a further bit — kill | **NAMED (W-BIT, third joint, E-GW-2)**: scope transfer of owned quote C2 `:1539`; fallback narration A5 `:1556`; U2a leg closes via OB-W1 |

## V. Named risks & PRE-REGISTERED attack surface

- **ATT-1 (strongest self-attack): W-BRIDGE-1′ — "the halt QUOTIENT is contract-owned, but who says the quotient is a stationary VERTEX counted in base capacity?"** The operator-space control (check 6) sharpens this attack maximally: a shift-invariant halt-like fixed point (`E = (9/2)·I`) exists over pure Ω₈ with NO witness vertex — so "some fixed point exists" cannot be the forcing content. **ATTACK LANDED (error of record E-GW-1):** v1's closing sentence here — "the sweep found none (the only owned halt-realization texts are A1/A2/A3/B5, all +1)" — was **FALSIFIED** by skeptic #1: `:846` realizes the halt-quotient output as the four-role readout algebra (**+0**) and B5 `:858` itself lands the halt on the signed terminal role algebra with V₉ "only after" (sequencing, adverse). By the letter of the pre-registered kill condition, GW-E *as originally bridged* TRIGGERED. Repaired bridge: W-BRIDGE-1′ rides the **re-detection sliver** — the contract couples "halt quotient AND stable re-detection class" (`:1166.5`), forbids external memory for the record (BOOK_00`:177`), and the re-detection-layer texts are the +1 narrations (A1 "REUSABLE shell", A2 "first ADDRESSABLE shell", A3 "closes against ω₀"). Corrected sweep sentence: **the owned +1-realization texts are A1/A2/A3 (re-detection layer); the owned halt-proper texts `:846`/`:858` are +0 (adverse).** New kill condition, pre-registered: **if the skeptic produces an owned text realizing the RE-DETECTION class at +0 base capacity, W-BRIDGE-1′ dies and GW-E with it.**
- **ATT-2 (parent's second pre-registered attack, answered in §I.D2): "does `first_instance_canonical` kill the second witness or just canonicalize the first?"** Resolved by division of labor: it does NOT kill V₁₀ — it is the no-overfire certificate at m = 1 (`|S₁| = 1`). The V10-kill is `repeat_has_nontrivial_copy_symmetry` (copy branch) + `:1539` (bit branch). Any draft that cites `first_instance_canonical` as a V10-killer over-claims and dies at check 9's semantics.
- **ATT-3 (W-T1 instantiation license):** CASE-2's ⊥M1 reading is declared for zones; marks are a new object class. Mitigation: the module docstring itself already applies the schema cross-class ("Same forcing as `Ω₈≅Q₈` via Dedekind"). **Weakened per S3:** v1's second mitigation (A5 `:1556` as direct narration of THIS kill) is withdrawn — `:1556`'s "extra hidden MARKER" wording fits the bit/marker branch (U2b/W-BIT), not the copy branch; **the copy branch rests on W-T1 alone.** Residual: a skeptic may demand a per-class schema owner; then GW-U's copy branch downgrades to Lean-arithmetic-supported-only.
- **ATT-4 (model-dependence of freeness, registered by check 5):** under a conjugation reading of "circulation", the center `{±1}` is stationary inside Ω₈ and the 8-kill fails. Owned defense: `:1996` says the trace gradient "traversed the full signed role cycle" — a full traversal visits all 8 signed roles, and conjugation CANNOT do that (its orbits on Q₈ have sizes 1,1,2,2,2 — max 2 < 8; derivable from the same table as checks 2/5, stated here as a remark, not a separate check). So the conjugation reading contradicts the owned full-traversal text; translation/shift is both the owned Lean model (`shiftMat`) and the only reading compatible with `:1996`. Residual: `:1996` is narration.
- **ATT-5 ("stationary" polysemy):** does "stationary" in `:1541` mean fixed-under-circulation (this memo's reading, backed by `:1993` "closes against" and WitnessHalting's fixed-point language) or something else (e.g., scale-stationary)? If scale-stationary, E5 mis-targets. **Narrowed per skeptic strengthening S4:** "stationary" occurs exactly ONCE in BOOK_01 (`:1541`), is undefined, and no adverse (non-circulation) reading was found in the corpus — the risk is single-occurrence indeterminacy, not a competing owned reading. The §01.24 co-location of circulation, closure-against-ω₀, and halt keeps the circulation reading the natural one.
- **ATT-6 (corroboration discipline):** B1's "second hidden calibration section" and B2's "single section" clauses concern the *scale/calibration* section; identifying ω₀ with THAT section is NOT owned. This memo cites them as pattern-level corroboration only (U2b row says so explicitly); the kill chains do not lean on them. An attack on that identification hits nothing load-bearing.
- **ATT-7 (fork hygiene, inherited):** this memo forges the `8+1` decomposition only. The `4+5` route to 9 (BOOK_03/04) is NOT touched; per the window memo's ATT-2, the two nines remain unidentified — GW must not be quoted as "9 forced" simpliciter, only as "the witness `+1` over Ω₈ forced given the named joints".

## VI. What this does NOT show

- It does NOT prove `card_base_forced` unconditionally in Lean; the THREE joints (W-BRIDGE-1′, W-T1, W-BIT) are named hypotheses, exactly as displayed in §IV.
- It does NOT bridge from the halt-proper to the vertex — that bridge is CONTRADICTED by two owned texts (`:846`, `:858`); only the re-detection-layer bridge survives (E-GW-1).
- It does NOT close GAP-E (extension completeness `{D₂, ABCD}`) — the hard half of the dissolve-window residual, untouched here.
- It does NOT upgrade `WitnessHalting`/D0-IM-004 — on the contrary, check 6 BOUNDS it: the orbit-average fixed point cannot force the +1.
- It does NOT identify the `8+1` and `4+5` decompositions of 9 (ATT-7).
- It does NOT edit the registry or the built Lean tree; DRAFT candidate material pending repair verification.

## Skeptic pass #1 — verdict and repair log (accepted in full, no defense)

**Overall verdict (relayed 2026-07-05): GW WOUNDED, not killed** — kill matrix, Lean quotes, computations, and the `first_instance_canonical` precision correction all independently verified (skeptic rebuilt Q₈ as 2×2 Gaussian-integer matrices; conjugation orbit sizes `[1,1,2,2,2]` confirmed, validating ATT-4's defense arithmetic). All repairs applied in this revision (v2):

- **E-GW-1 (strongest — W-BRIDGE-1 grounding).** The ATT-1 sweep sentence "the only owned halt-realization texts are A1/A2/A3/B5, all +1" was **FALSIFIED**: `:846` (halt-quotient output = four-role readout algebra, +0) and B5 `:858` (halt lands on the signed terminal role algebra; V₉ "only after" — +0-leaning sequencing, adverse not supporting). GW-E triggered by the letter of its own pre-registered kill condition; it survives ONLY on the re-detection sliver (`:1166.5`). Repairs: W-BRIDGE-1 → **W-BRIDGE-1′** (realizes the RE-DETECTION class, not the halt, as a vertex); narration count ×4 → ×3; B5 reclassified adverse throughout (§I.B5/B5a, §II.1, §II.2 E3, §II.4, OB-W4, ATT-1); sweep sentence rewritten precisely; new kill condition pre-registered (re-detection class at +0).
- **E-GW-2 (joint count).** The `:1539` scope transfer (Ω₈-construction bits → labels on adjoined marks) was an UNNAMED third joint; the toggle matrix shows it load-bearing (drop it ⇒ labeled-V₁₀ survives). Named **W-BIT**; headline restated "FORCED GIVEN THREE named joints"; U2b retagged from "OWNED-NARRATED (direct quote)" to scope-transfer joint with `:1556` as fallback narration.
- **E-GW-3 (hygiene — joint contained the conclusion).** W-BRIDGE-1 was stated with "ONE / EXACTLY ONE" in three places (verdict line, E3 row, OB-W4) although the deduction (E6) only ever uses ≥ 1 — read literally, the joint smuggled the 10-kill. All three restated as **≥ 1**, with uniqueness delivered by the kill matrix (W-T1 + W-BIT).
- **E-GW-4 (script docstring inflation).** "checks 1-4, 8, 9 can fail the CONCLUSION directly" was wrong for 8/9 (they re-read check 7's criteria function — fail only via a criteria-encoding bug) and unlabeled for 1 (a definition mirror). Script docstring de-inflated; §III aligned; 10/10 rc=0 unchanged after edit.

Skeptic verifications that STRENGTHEN GW (logged): independent Q₈ rebuild (2×2 Gaussian-integer matrix representation) confirms group axioms, center, translation-freeness; conjugation orbits `[1,1,2,2,2]` confirm ATT-4's max-orbit-2 defense; **S3:** `:1556`'s "extra hidden marker" fits the BIT/marker branch only — copy branch rests on W-T1 alone (now stated at U1, ATT-3); **S4:** "stationary" occurs exactly once in BOOK_01 (`:1541`), undefined, no adverse reading found — ATT-5 narrowed to single-occurrence indeterminacy.
