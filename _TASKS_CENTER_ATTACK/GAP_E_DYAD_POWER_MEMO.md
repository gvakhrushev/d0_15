# GAP_E_DYAD_POWER — is "every admissible zone-extension is a dyad-power `D₂^k`" OWNED? (forge → own skeptic → verdict)

**Status:** DRAFT candidate. NO registry row edited; NO `.lean` added to the built tree; NO edit to `CLAIM_TO_LEAN_MAP.csv` / `theory_status_map.csv` / any `053040` row / LEAN_ASSUMPTION_LEDGER. All Lean/mechanism references below are read-only verifications. Companion can-fail script: `_TASKS_CENTER_ATTACK/gap_e_dyad_power_check.py` (run clean 2026-07-05).
**Parent:** `GAP_E_EB_FORGE_MEMO.md` §RES — which pinned the residual to a single missing sentence and *flagged* the dyad-power sentence as "NOT owned; candidate sketch". This memo executes the ownership test that parent deferred, on primary sources.

---

## VERDICT UP FRONT — **UNDERDETERMINED. The dyad-power principle is NOT owned. GAP-E stays OPEN, with this as THE exact missing sentence.**

The candidate closing sentence —
> *"every admissible zone-extension object is a dyad-power `D₂^k` (size `2^k`), and `2^k` for `k≥3` repeats the signed square ⇒ CASE-2 copy-symmetry kill (`NoExtension.lean:47`), leaving exactly `{D₂(=2), ABCD=D₂×D₂(=4)}` and excluding size 6 (=`+4`→V₁₅, not a power of 2)"*

— has **two** load-bearing clauses, and **both fail ownership**:

1. **The generator clause** ("*every* admissible extension is a dyad-power `2^k`") is **not an owned principle.** The corpus owns a **closed two-item LIST** — the dyad and the role-square (BOOK_01:1548, verbatim below) — not a **generative rule** that every admissible extension must be a power of the dyad. The two owned sizes are each forced by a **separate singleton mechanism** (role-count = 4; sign-bit = 2), and `|ABCD| = D₂² = 4` (BOOK_01:1812) is a *re-description of 4 as 2²*, **not** the forcing that produces it. Nothing owned quantifies over "every extension".

2. **The `:47` kill clause** ("`2^k` for `k≥3` triggers the copy-symmetry kill") **misreads `NoExtension.lean:47`.** That theorem (`repeat_has_nontrivial_copy_symmetry`) proves `1 < Fintype.card (Equiv.Perm (Fin 2))`, i.e. **`|S₂| = 2 > 1`** — it bites on **≥2 indistinguishable COPIES OF ONE TYPE** (docstring `:15-17`, `:44-46`, verbatim below). It says **nothing** about sizes, and nothing about powers of 2. There is **no owned bridge** from "the extension has size `2³`" to "it is a repeated copy of the signed square". The `k≥3`-repeats-the-square step is a *coinage*, not a theorem `:47` supplies.

Because size 6 (the `+4`→V₁₅ escape) is excluded **only by the absence of a generator that would produce it** — not by any owned forbidding sentence — the exclusion is by **silence, not by forcing**. That is precisely GAP-E, unmoved. **No leap:** owned ⇒ "{2,4} are the two named extensions and each is singly forced"; it does **NOT** ⇒ "{2,4} is the complete admissible set." The gap between those two is the missing sentence.

**Do not manufacture ownership.** The honest outcome is UNDERDETERMINED; the exact missing sentence is stated in §RES.

---

## OWN-1. The owned extension material is a LIST, not a GENERATOR (verbatim)

`BOOK_01…md:1548` (§01.20, verbatim, read this pass):
> "The next two shell extensions are **the only primitive unresolved capacities** over the pointed shell: **the direct/return dyad and the full terminal role square.**"

`BOOK_01…md:1551-1553` (verbatim):
> `V₁₁ = V₉ ⊔ D₂` , `V₁₃ = V₉ ⊔ four terminal roles A,B,C,D`

**Owned content:** exactly **two** extensions are named, and the justification word is **"primitive unresolved capacities"** — an inventory reason (these are the capacities left unresolved over the pointed shell), NOT "these are the powers of the dyad." A grep of `BOOK_01`+`BOOK_03` for `power of two / power of 2 / 2^k / dyad-power / dyadic power` returns **exactly one hit — line 1548 itself** (the "primitive unresolved capacities" sentence). **No owned sentence states a `2^k` generator.** (`gap_e_dyad_power_check.py` §RULE-SET-1 encodes the list.)

## OWN-2. `|ABCD| = D₂² = 4` is a re-DESCRIPTION; the FORCING is role-count, not power-of-2 (verbatim)

`BOOK_01…md:1809-1812` (§01.22, verbatim):
> "Let the direct/return dyad have cardinality `D₂ = 2`. Then the terminal role square has cardinality `|four terminal roles A,B,C,D| = D_2^2 = 4`."

This *writes* 4 as `2²`. But the **forcing** for "why exactly 4" is elsewhere and is **role-count**, not power-of-2:

`BOOK_03…md:914-932` (§03.23.1, verbatim):
> "`|Tr(T³)| = 4` is the ABCD capacity; the forcing says *why a closed scene needs exactly 4*. A minimal closed scene must realize exactly the four ABCD roles… `D_anchor < 4`: some role is unrealized → … external prop… Banned. `D_anchor > 4`: empty address slots appear; … exogenous significance catalog. Banned. Both deviations re-introduce the external catalog M1 forbids, so `D_anchor = 4` is the unique survivor."

**Owned content:** `|ABCD| = 4` is forced because there are **exactly four roles A,B,C,D** and any other count is `⊥M1` — a **counting/empty-slot** argument, not a **dyad-power** argument. The `= D₂²` label is downstream bookkeeping. **So the corpus does not own "the role-square is admissible *because* it is a dyad-power"; it owns "the role-square is size 4 *because* there are 4 roles."** A size-6 extension is not rejected by this mechanism-as-stated (it names only "≠4 for the anchor", about the role-count, not about a generic extension size).

## OWN-3. `NoExtension.lean:47` is a COPY-symmetry kill on a REPEATED TYPE — NOT a "size 2^k" kill (verbatim Lean)

`NoExtension.lean:44-48` (verbatim, read on disk this pass):
```lean
/-- **CASE 2 / repeat needs a catalogue.** `≥2` identical copies carry a nontrivial copy-
permutation symmetry: `|S_2| = 2 > 1`, so there is no canonical copy and selecting one is an
external catalogue ⇒ `⊥M1`. -/
theorem repeat_has_nontrivial_copy_symmetry : 1 < Fintype.card (Equiv.Perm (Fin 2)) := by
  native_decide
```
Docstring `:15-17` (verbatim): "**CASE 2 — `Z4` repeats an existing type.** `≥2` indistinguishable copies carry a nontrivial copy-permutation symmetry (`|S_2|=2>1`)…"

**Owned content:** the theorem proves the *set-theoretic fact* `1 < |Perm(Fin 2)|` and is applied to **two indistinguishable copies of one already-existing type**. Its trigger is **"is this a repeat of an existing type?"** — decided by TYPE-identity, not by SIZE. **There is no owned predicate "has size `2^k` with `k≥3`" and no owned lemma mapping such a size to "is a repeat of the signed square".** The candidate sentence's clause "`2^k` for `k≥3` repeats the signed square ⇒ `:47` kill" **imports** the bridge (size→repeat) that `:47` does not contain. This is the sharper of the two failures: even if the generator clause were granted, `:47` would not deliver the `k≥3` prune it is cited for.

**Note (against a leap the other way):** `NoExtension.lean` (`no_extension_theorem`, D0-TOWER-STOP-NOEXT-001) genuinely proves the **COUNT-3** stop (no 4th ZONE). That is owned and untouched. But a `+4` top step `(9,11,15)` is a **3-zone** tower — COUNT-3 does **not** speak to it (parent memo OWN-0.3, re-confirmed). So `:47`/`no_extension_theorem` owns "no fourth zone", not "no third zone of size 15."

## OWN-4. The parity route owns EVEN, and says "minimal" not "unique" (verbatim)

`BOOK_01…md:1899` (§01.22, verbatim, read this pass):
> "…The step `5 → 7` preserves the orientation class, so the splice closes with no exogenous parameter. Hence **the minimal admissible junction step is `+2`**… Any other step requires an external splice-control parameter, hence `⊥M1`."

**Owned content:** the ⊥-mechanism fires **iff the step flips the `ℤ₂` orientation class**, i.e. iff the step is **ODD**. `+2` and `+4` are **both even**, both preserve the class, both reach **no `⊥`**. "Minimal" (verbatim) is a conclusion-word; "Any other step … `⊥M1`" is asserted but the printed mechanism only reaches `⊥` for the **odd/flip** case. So parity owns **step-evenness**, not **`+2`-over-`+4`**. (`GAP_E_EB_FORGE_MEMO` OWN-1, re-verified verbatim; the `+4`→V₁₅ escape survives.)

## OWN-5. Size 6 is excluded by ABSENCE, not by an owned sentence (script §GAP)

`BOOK_01…md:1556` (§01.20, verbatim): the only named exclusions are
> "`V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10`…, `V13` cannot be replaced by `V12`…"

**All named exclusions — V8, V10, V12 — are BELOW 13.** No owned sentence names a size-6 extension, a `V₁₅`, or "any size above 13." The script's `[GAP]` line confirms `6 ∉ {8,10,12}`: size 6 is excluded only because **no owned generator produces it** — an argument from **silence**, which is exactly what a forcing must replace. A closure clause `∀X (AdmExt(X) → |X| ∈ {2,4})` is **not owned.**

---

## RES — THE EXACT MISSING SENTENCE (candidate language, flagged, NOT owned)

GAP-E closes iff the corpus gains **one** owned sentence of the form:

> **(MISSING)** *The admissible extension alphabets over the pointed shell `V₉` are closed: `∀X (AdmExt(X) → |X| ∈ {2,4})`. Equivalently, the only primitive unresolved capacities are the dyad `D₂` and the role-square `D₂×D₂`, and this list is EXHAUSTIVE — no third primitive capacity of any size (in particular no size-6 extension) is admissible.*

This is a **completeness/exhaustiveness** claim about the capacity inventory. The corpus owns the **membership** side (`D₂` and `ABCD` are admissible, each singly forced) but owns **no exhaustiveness clause**. The candidate "dyad-power `2^k`" phrasing is **one possible** way to state (MISSING), but:
- it over-generates (must first admit `8 = 2³`, then delete it) where the owned mechanism never proposes 8 at all — a **tell** that the generator is imported (script `[TELL]` lines); and
- its deletion step leans on `:47`, which (OWN-3) proves a copy-symmetry fact about repeated types, not a size-`2^k` fact.

**A cleaner candidate** (also flagged, also NOT owned) would be an M1-forcing directly on the inventory: *"any capacity not equal to `D₂` or `ABCD` either duplicates one of them (⇒ CASE-2 repeat, `:47`) or introduces an unrealized/empty role (⇒ the `D_anchor≠4` fork, BOOK_03:929-932); size 6 = `ABCD ⊔ D₂` is a duplicate-composite, hence a repeat."* — This at least routes 6 through **owned** kills. But it requires an **owned lemma** "every extension is a sum of `{D₂, ABCD}` blocks", which is itself the un-owned exhaustiveness claim in disguise. **The circle does not open from owned material.**

---

## SKEPTIC PASS (self-run)

- **Attack A — "coextensive ⇒ owned":** the script shows dyad-power and the owned list AGREE on `{2,4}` across the whole scan. Does agreement make it owned? **No.** Two rules can coincide on a range for different reasons; ownership is about the **mechanism**, not the extension. The owned mechanism reaches `{2,4}` by two singleton forcings; the candidate reaches it by generate-`2^k`-then-prune. Coincidence on values is not ownership of the rule. **Attack fails to rescue.**
- **Attack B — "`Ω₈ = 8 = 2³` is owned, so `2^k` is owned":** `Ω₈ = ABCD × {±} = 8` (BOOK_01:1539) is owned — but `Ω₈` is the **shell interior**, NOT a zone-extension, and its 8 is `4×2` (role-square times sign), owned by role-count×sign-bit, again **not** by a "power of 2" generator. So `2³` appearing in the corpus is bookkeeping, not a generative principle. **Attack fails.**
- **Attack C — "the parity 'any other step ⊥M1' already excludes +4":** the *words* say so (BOOK_01:1899) but the *mechanism* only reaches `⊥` for orientation-FLIP (odd) steps (OWN-4). Reading "any other step" as covering the even `+4` is **narration beyond the printed forcing**. **Attack fails** (this is the same seam the parent memo pinned).
- **Skeptic's strongest surviving finding:** the single most defensible over-claim to guard against is treating `|ABCD| = D₂²` (BOOK_01:1812) as *the forcing*. It is not — BOOK_03:929-932 is the forcing and it is a role-count/empty-slot argument. Anyone closing GAP-E must supply the **exhaustiveness** sentence (§RES); re-labeling 4 as `2²` does not supply it.

## HEADLINE (exactly what is owned)

**Owned:** `{D₂(=2), ABCD(=4)}` are the two named shell-extensions (BOOK_01:1548-1553); `|ABCD|=4` is forced by role-count (BOOK_03:929-932); the dyad is size 2 by the sign-bit (BOOK_01:1539); the tower has COUNT 3 (`no_extension_theorem`); the junction step is EVEN by orientation-parity (BOOK_01:1899); `NoExtension.lean:47` proves `|S₂|>1` (copy-symmetry of a repeated TYPE).

**NOT owned (the gap):** any exhaustiveness clause `∀X(AdmExt(X)→|X|∈{2,4})`; any "extensions are dyad-powers `2^k`" generator; any bridge "size `2^k`, `k≥3` ⇒ repeat of the signed square" (`:47` does not prove this); any sentence excluding a size-6 extension / `V₁₅` / "size above 13" by name.

**Outcome:** UNDERDETERMINED. GAP-E remains OPEN. The dyad-power sentence is the exact **missing** sentence, a coinage, not an owned theorem. The window upper bound is owned as a **cardinality** (`V₁₃ = V₉ ⊔ ABCD`) but **not as a maximum**.

---

## Independent skeptic verdict + repair log (accepted in full)

**Verdict: ACCEPT-IN-FULL. The UNDERDETERMINED headline SURVIVES.** Attacked both directions independently; the verdict holds. No repair is load-bearing / integrity-critical.

**(1) UNDER-claim attack — is GAP-E secretly CLOSED?** The word **"only"** at `BOOK_01:1548` ("the only primitive unresolved capacities") is the sole place that could own exhaustiveness. Reading the full section **01.20 (lines 1521–1548)** on disk this pass: the section FORCES the interior construction — `ABCD = 4` (`:1530` "Fewer than four … catalog M1 forbids"), the sign-bit `Ω₈` (`:1539`), the witness `ω₀` (`:1541`) — but supplies **NO bottom-M1 mechanism** for exhaustiveness of the two EXTENSIONS. The "only" at `:1548` is a **bare assertion** followed by a "Therefore" that merely writes `V₁₁, V₁₃`. So the memo's reading (owns **membership**, not **exhaustiveness**) is **correct**. Attack fails to close GAP-E.

**(2) OVER-claim attack — does the memo under-scope GAP-E?** Registry `CLAIM_TO_LEAN_MAP.csv` row for `D0-ZONE-TOWER-READING-FORK-001` states GAP-E is **TWO-guarded** ("GAP-E is two-guarded: capacity-completeness AND +2 no-skip", verified verbatim on disk). The memo covers **BOTH**: capacity-completeness via OWN-1/OWN-4/OWN-5, and +2-no-skip via **Attack C** — and it names the surviving alternative: the even **`+4` → V₁₅** escape that the orientation-parity mechanism (fires only on **ODD/flip** steps, `BOOK_01:1899`, verified verbatim: `⊥M1` on the flip `5→6`; `5→7` even "preserves the orientation class"; "Hence the minimal admissible junction step is `+2`") never reaches. That is exactly the "**+4 step that survived the parity argument**" the LEAP test asks for. Attack fails to under-scope; the memo's scope is correct.

**Strongest independent corroboration (registry-side, verified on disk).** The registry itself logs GAP-E as OPEN / HARD / untouched — matching the memo's verdict from artifacts the memo does not author:
- `CLAIM_TO_LEAN_MAP.csv` row `D0-TOWER-STOP-NOEXT-001` (row 257): HONEST note proves only "the COUNT (3 slots) + NO-4th are Lean-proved exactly" — i.e. **no fourth ZONE**; **silent on extension SIZE**. It does not speak to a `+4` third zone of size 15 (a 3-zone tower).
- `CLAIM_TO_LEAN_MAP.csv` row `D0-WINDOW-9-13-DISSOLVE-001` (row 546, **status OPEN**): independently registers "GAP-E (extension completeness {D2,ABCD}, HARD, untouched) … reduction not closure."
- `CLAIM_TO_LEAN_MAP.csv` row `D0-GAP-W-WITNESS-PLUS-ONE-001` (row 545, GAP-W): "GAP-E … is **NOT attempted here**."

**No-leap check.** Owned ⇒ "{2,4} are the two named extensions, each singly forced (role-count = 4; sign-bit = 2)"; it does **NOT** ⇒ "{2,4} is the complete admissible set." The gap between those two is the exact missing sentence in §RES. `NoExtension.lean:47` proves `1 < |Perm(Fin 2)|` (copy-symmetry of a repeated TYPE) — it is **not** a "size `2^k`" predicate; the candidate's `k≥3`-repeats-the-square bridge is a coinage `:47` does not supply. No φ-power-to-physical-number numerology is asserted; the object is judged by its MECHANISM, and the mechanism for exhaustiveness is **absent**.

### Errors of record
- **EOR-1 (guarded, not committed).** Treating `|ABCD| = D₂²` (`BOOK_01:1812`) as *the forcing* would be an over-claim. The forcing is the role-count / empty-slot argument (`BOOK_03:929–932`); `= D₂²` is downstream bookkeeping. The memo already flags this (OWN-2, skeptic "strongest surviving finding") — recorded here so no future closure re-labels `4` as `2²` and calls the exhaustiveness gap filled.
- **EOR-2 (guarded, not committed).** Reading "any other step … `⊥M1`" (`BOOK_01:1899`) as covering the **even** `+4` is narration beyond the printed mechanism, which reaches `⊥` only on the **odd/flip** step. The even `+4`→V₁₅ escape is un-killed by parity. The memo already flags this (OWN-4, Attack C).

### Final status
- **Headline unchanged:** UNDERDETERMINED — the dyad-power principle is NOT owned; GAP-E stays OPEN, with the §RES sentence as the exact missing sentence. No closure was claimed, so no closed→underdetermined downgrade is needed; no demotion of an owned fact is needed.
- **Repairs applied:** none load-bearing. Appended this verdict + repair log + errors of record; no headline edit required.
- **Residual — owned:** `{D₂(=2), ABCD(=4)}` named (`BOOK_01:1548–1553`); `|ABCD|=4` by role-count (`BOOK_03:929–932`); dyad size 2 by sign-bit (`BOOK_01:1539`); COUNT-3 (`no_extension_theorem`); junction step EVEN by parity (`BOOK_01:1899`); `NoExtension.lean:47` = `|S₂|>1` (copy-symmetry of a repeated TYPE).
- **Residual — open (the gap):** any exhaustiveness clause `∀X(AdmExt(X)→|X|∈{2,4})`; any dyad-power `2^k` generator; any bridge "size `2^k`, `k≥3` ⇒ repeat of the signed square"; any sentence excluding a size-6 extension / `V₁₅` / "size above 13" by name. GAP-E remains OPEN / HARD / untouched.

**Registry hygiene:** no edit to `CLAIM_TO_LEAN_MAP.csv` / `theory_status_map.csv` / any `053040` row / `LEAN_ASSUMPTION_LEDGER` / built `.lean`. This memo remains a DRAFT candidate; all citations are read-only verifications performed 2026-07-05.
