# CLOSE_TWO_SENTENCES — consolidation of the two D0 sentence-closure campaigns on the GAP-E top-zone upper bound

**Date:** 2026-07-05
**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15`
**Scope:** consolidate the two center-attack campaigns that each tried to forge the *one* missing sentence closing GAP-E's top-zone upper bound `z₃ = 13` (excluding the `+4` step `11 → 15 = V₁₅`), and report per-gap whether the sentence turned out OWNED (gap closes) or narrated/coined (gap stays open, sentence named exactly).
**Governing constraint (all facts below verified verbatim on disk this pass):** NO registry row edited, NO `.lean` added to the built tree, NO edit to `CLAIM_TO_LEAN_MAP.csv` / `theory_status_map.csv` / any `053040` row / `LEAN_ASSUMPTION_LEDGER`. This is a read-only consolidation.

---

## 0. The two campaigns and their relationship

Both campaigns attack the **same** residual, from two sides, and both memos state outright that the two sentences are **the same missing sentence** (`GAP_E_EB_FORGE_MEMO.md:24`: "E-b and E-a are not two routes; under the fork-identification `4 = 2·2` they are one gap seen from two sides"). The residual is: `z₃ = 13` is owned as a **cardinality** (`V₁₃ = V₉ ⊔ ABCD`, size 13) but **NOT as a maximum** — nothing owned forbids a size-6 extension `→ V₁₅` (the even `+4` top step).

| # | Campaign (item) | Missing sentence attacked | Deliverables | Skeptic cycle | Final |
|---|---|---|---|---|---|
| 1 | **E-b no-skip / `+2`-uniqueness** | "*the top step is `+2` and NOT `+4`; `+2` is the unique admissible even step*" (step-side / consecutive-fork view) | `GAP_E_EB_FORGE_MEMO.md`, `gap_e_eb_check.py` | main-loop verification banner only; §SKEPTIC line **left unfilled** (`[filled after the skeptic pass]`, line 28) — superseded before a full self-skeptic completed | **UNDERDETERMINED** (verified, superseded by #2) |
| 2 | **dyad-power** | "*every admissible zone-extension is a dyad-power `D₂^k` (size `2^k`); `2^k` for `k≥3` repeats the signed square ⇒ `NoExtension.lean:47` kill*" (generator / extension-completeness view) | `GAP_E_DYAD_POWER_MEMO.md`, `gap_e_dyad_power_check.py` | **full** forge → own-skeptic → verdict → repair; **SURVIVES / ACCEPT-IN-FULL** | **UNDERDETERMINED** (adjudicated) |

Campaign #2 is the child of #1 (`GAP_E_DYAD_POWER_MEMO.md` **Parent:** line names `GAP_E_EB_FORGE_MEMO.md §RES`, which "*flagged* the dyad-power sentence as 'NOT owned; candidate sketch'"). #2 executes the ownership test #1 deferred. Lineage upstream of both: `GAP_E_COMPLETENESS_MEMO.md` (v2, R3 two-route spec) → `GAP_E_CLOSE_MEMO.md` (empty-slot route, KILL retracted/OVERTURNED) → `GAP_E_EB_FORGE_MEMO.md` (#1) → `GAP_E_DYAD_POWER_MEMO.md` (#2).

**Net:** the two campaigns collapse to **one gap and one exact missing sentence**. Neither side owned it.

---

## 1. Per-gap adjudication

### GAP #1 — E-b no-skip / `+2`-uniqueness (step-side)

**Missing sentence (exact, coined):** *"the top junction step is `+2` and not `+4`; `+2` is the **unique** admissible even step."*

**Verdict: NARRATED, not owned. Gap STAYS OPEN.**

What is owned (verified verbatim on disk):
- `BOOK_01:1899` — "*Hence the **minimal** admissible junction step is `+2`*", derived by an **orientation-parity** argument: the `5 → 6` step flips the `ℤ₂` orientation class and needs an external orientation bit (⊥M1); `5 → 7` preserves the class. **The mechanism kills a step iff it is ODD (flips parity).** `+2` AND `+4` both preserve the class → both reach NO contradiction.
- `BOOK_01:1556` — the construction "rules out alternatives: `V8`, `V10`, `V11←V10`, `V13←V12`" — **all interior / below 13. None names V₁₅ or any size above 13.**

The tell: the printed word is **"minimal"**, not **"unique."** "Minimal" is satisfied by `+2` without excluding the larger even `+4`. The narrowing from "even" to "`+2`-over-`+4`" is a conclusion-word the parity mechanism never reaches. The even `+4 → V₁₅` escape survives the parity argument untouched. (Corroborated: `GAP_E_CLOSE_MEMO.md` counter-correction banner independently established the KILL of this bound was itself over-read; `GAP_E_COMPLETENESS_MEMO.md` F1 already flagged G-STEP as "one-sentence-killable.")

Empty-slot route also excluded (`GAP_E_EB_FORGE_MEMO.md` OWN-4, verified `BOOK_03:931-932`, `BOOK_01:1911-1913`): the empty-slot pattern is a **surplus** detector (fires when `k > |I|` for a closed inventory `I`); E-b needs a **skip** detector (a `+4` leaping over a pre-laid slot 13). The only owned laid-out address space is the 9 positions of `V₉` — no owned space of size ≥13 exists for a skip to occur in. The route does not transfer.

### GAP #2 — dyad-power generator (extension-completeness side)

**Missing sentence (exact, coined):** *"every admissible zone-extension object is a dyad-power `D₂^k` (size `2^k`), and `2^k` for `k≥3` repeats the signed square ⇒ CASE-2 copy-symmetry kill (`NoExtension.lean:47`), leaving exactly `{D₂=2, ABCD=4}` and excluding size 6."*

**Verdict: COINED, not owned. Gap STAYS OPEN.** (Skeptic SURVIVES, ACCEPT-IN-FULL.)

The sentence has **two** load-bearing clauses; **both fail ownership** (both verified verbatim on disk this pass):

1. **Generator clause** ("*every* admissible extension is a dyad-power `2^k`"). The corpus owns a **closed two-item LIST** — `BOOK_01:1548` verbatim: "*The next two shell extensions are **the only primitive unresolved capacities** over the pointed shell: the direct/return dyad and the full terminal role square.*" — **not a generative rule**. The two owned sizes are each forced by a **separate singleton** mechanism: `D₂ = 2` by the sign-bit (`BOOK_01:1539`); `|ABCD| = 4` by role-count / empty-slot fork (`BOOK_03:929-932`). `|ABCD| = D₂² = 4` (`BOOK_01:1812`) is a **re-description of 4 as 2²**, downstream bookkeeping — NOT the forcing. Nothing owned quantifies over "every extension." **Owned ⇒ membership; NOT ⇒ exhaustiveness.**

2. **`:47` kill clause** ("`2^k` for `k≥3` triggers the copy-symmetry kill"). `NoExtension.lean:47` (`repeat_has_nontrivial_copy_symmetry`) proves `1 < Fintype.card (Equiv.Perm (Fin 2))` = `|S₂| = 2 > 1` — verified verbatim, docstring `:44-46`: "*`≥2` identical copies carry a nontrivial copy-permutation symmetry ... selecting one is an external catalogue ⇒ ⊥M1.*" It bites on **≥2 indistinguishable COPIES OF ONE TYPE**, decided by **type-identity, not size**. There is **no owned bridge** from "size `2³`" to "repeated copy of the signed square." The `k≥3`-repeats-the-square step is a **coinage** `:47` does not supply.

Consequence: size 6 (`+4 → V₁₅`) is excluded **only by the absence of a generator that would produce it** — argument from silence, not a forcing. That is exactly GAP-E, unmoved.

**Skeptic self-attack that was answered (from the adjudicated record):** the can-fail script shows the dyad-power rule and the owned list AGREE on `{2,4}` and both kill size 6, so doesn't the principle just re-describe what's owned (⇒ effectively closed)? **Rebuttal (holds):** coextension-on-values ≠ ownership-of-the-rule. The owned mechanism says False for size 8 at every stage (never proposes it); the dyad-power rule must first GENERATE `8 = 2³` then prune it via a `:47`-reading `:47` does not prove. Excluding size 6 by "no generator produces it" is the argument from silence a forcing must replace. `gap_e_dyad_power_check.py` ran clean (rc=0); its `[TELL]` and `[GAP]` lines make the generate-then-prune vs never-proposed distinction non-tautologically.

---

## 2. Did either gap close?

**NO. Neither gap closed.** Both missing sentences turned out narrated/coined, not owned. GAP-E stays **OPEN / HARD / untouched**. `z₃ = 13` remains owned as a **cardinality** (`V₁₃ = V₉ ⊔ ABCD`) but **NOT as a maximum**. The `+4 → V₁₅` escape is un-killed by any owned text.

**The exact missing sentence (single, both sides identical):**
> *"the admissible extension alphabets of `V₉` are exactly `{D₂ (size 2), ABCD (size 4)}`; there is no admissible extension of size 6 (or any size ∉ {2,4})"* — equivalently, an M1-forcing that *any extension alphabet is a power of the dyad `2^k`, and `2^k` for `k≥3` repeats the signed square.*

The corpus owns **membership** of `{D₂, ABCD}` and owns **why each of 2 and 4 is forced**; it owns **NO exhaustiveness / closure clause** `∀X (AdmExt(X) → |X| ∈ {2,4})`, no `2^k` generator, and no bridge size-`2^k`⇒repeat-of-square.

---

## 3. Registry proposals (safe vs owner-gated)

**No new mint is warranted; the gap is already logged as OPEN.** Independent registry-side corroboration (verified verbatim this pass in `CLAIM_TO_LEAN_MAP.csv`):

- **Row `D0-WINDOW-9-13-DISSOLVE-001`** (status **OPEN**, PROOF-TARGET): "*skeptic#1 SURVIVES, BLOCKED from minting*"; the capstone interval `[9,13]` is a **PROJECTION** of the owned capacity chain, not an independent maximum. Already records the gap.
- **Row `D0-ZONE-TOWER-READING-FORK-001`** (status **OPEN**, PROOF-TARGET): records the three-reading fork (over-base TYPES / consecutive NUMERALS / nested narration), **NO owned identification**. This is the fork under which E-a and E-b are "one gap seen from two sides."
- **Row `D0-SCENE-TRIPLE-UNIQUE-001`** (row 530, CORE-FORMALIZED): `scene_triple_unique` takes `hladder₂ : z₂ = z₁ + 2` as a **HYPOTHESIS** — a `+4` tower `(9,11,15)` lives *outside* its scope, not inside its conclusion. Cannot substitute for the gap.
- **Row `D0-TOWER-STOP-NOEXT-001`** (row 257): owns the COUNT-3 (no 4th ZONE) only — **silent on extension SIZE**, so does not speak to a `+4` third zone of size 15.

**Proposal — SAFE (no owner gate needed):** append a one-line cross-reference note on `D0-WINDOW-9-13-DISSOLVE-001` (or `D0-ZONE-TOWER-READING-FORK-001`) pointing at the two consolidated deliverables (`GAP_E_EB_FORGE_MEMO.md`, `GAP_E_DYAD_POWER_MEMO.md`) and recording that **both** the step-side (`+2`-unique) and generator-side (`2^k`) forgings of the missing sentence were attempted and **both returned UNDERDETERMINED** — so the exhaustiveness clause is the single named missing object. This changes no status (row already OPEN), adds no claim, cites only on-disk memos. Deferred to the owner as a book-keeping edit, since even a notes-only registry edit is out of this read-only consolidation's mandate.

**Proposal — OWNER-GATED (do NOT do without owner sign-off):** any mint of the dyad-power sentence or the `+2`-uniqueness sentence as an owned forcing. Both are **coinages**; minting either would manufacture the exhaustiveness the corpus does not own. Explicitly blocked.

---

## 4. Residual over-claim risk

Two errors-of-record are guarded (carried from the adjudicated dyad-power record; a future pass must not commit them):

- **EOR-1** — treating `|ABCD| = D₂² = 4` (`BOOK_01:1812`) as **THE forcing** would be an over-claim; the forcing is the role-count / empty-slot argument (`BOOK_03:929-932`) and `= D₂²` is downstream bookkeeping. Risk: a future closure re-labels 4 as 2² and calls the exhaustiveness gap filled. (Flagged in dyad-power OWN-2.)
- **EOR-2** — reading "*any other step ... bottom-M1*" (`BOOK_01:1899`) as covering the EVEN `+4` is narration beyond the printed mechanism, which reaches bottom only on the ODD/flip step. The even `+4 → V₁₅` escape is un-killed by parity. (Flagged in dyad-power OWN-4 / E-b OWN.)

**Standing over-claim guard:** coextension-on-values (`{2,4}` agreed by owned list, dyad-power rule, and can-fail controls) must never be reported as ownership-of-the-rule. Excluding size 6 by "no generator produces it" is an argument from silence — the thing a forcing must replace, not the forcing itself. Residual risk that cannot be fully discharged: if a cleaner un-cited owner lemma "*every extension is a sum of `{D₂, ABCD}` blocks*" existed, it would route 6 through owned kills — but that lemma **is** the exhaustiveness claim in disguise, and grep of `BOOK_01` + `BOOK_03` for `power-of-two / 2^k / dyad-power` returns exactly one hit (line 1548, the two-item LIST, not a generator). No such owner found.

---

## 5. Files

- `/Users/grigorijvahrusev/Downloads/d0_15/_TASKS_CENTER_ATTACK/GAP_E_EB_FORGE_MEMO.md` — campaign #1 (E-b, UNDERDETERMINED; skeptic line unfilled, superseded)
- `/Users/grigorijvahrusev/Downloads/d0_15/_TASKS_CENTER_ATTACK/GAP_E_DYAD_POWER_MEMO.md` — campaign #2 (dyad-power, UNDERDETERMINED; skeptic SURVIVES / ACCEPT-IN-FULL)
- `/Users/grigorijvahrusev/Downloads/d0_15/_TASKS_CENTER_ATTACK/gap_e_dyad_power_check.py` — companion can-fail (rc=0)
- Lineage: `GAP_E_COMPLETENESS_MEMO.md` → `GAP_E_CLOSE_MEMO.md` → `GAP_E_EB_FORGE_MEMO.md` → `GAP_E_DYAD_POWER_MEMO.md`
- Registry (unedited, OPEN): rows `D0-WINDOW-9-13-DISSOLVE-001`, `D0-ZONE-TOWER-READING-FORK-001`, `D0-SCENE-TRIPLE-UNIQUE-001` (530), `D0-TOWER-STOP-NOEXT-001` (257)

**Bottom line:** two campaigns, one gap, one exact missing sentence — the extension-alphabet exhaustiveness clause `∀X (AdmExt(X) → |X| ∈ {2,4})`. Neither the step-side (`+2`-unique) nor the generator-side (`2^k` dyad-power) forging owned it. **GAP-E stays OPEN. No sentence closed.**
