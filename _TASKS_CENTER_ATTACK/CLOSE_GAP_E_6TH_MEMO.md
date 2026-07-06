# CLOSE_GAP_E_6TH — deriving the block-shape / two-universe clause to exclude X₃ (Aut-orbit partition)

> ## ⚖️ VERDICT: **PARTIAL → X₃ mapped and structurally excluded by three independent clauses, but the
> window stays OPEN: the discriminating quantifier is NOT owned.** (author pass 2026-07-06; **independent
> skeptic §SKEPTIC-#1 CONFIRMED-PARTIAL-OPEN, no kill — honest, non-smuggled; two minor EoR applied**.)
>
> This is the **SIXTH** independent confirmation that GAP-E's completeness clause is open
> (R3 → E-b → dyad-power → E-SYNTH → CLOSE-E(5th) → CLOSE-E(6th)). The 5th attempt (`CLOSE_GAP_E_MEMO.md`)
> derived the **partition rule** (D1–D4, kills `Sub(Q₈)`/`Out(Q₈)`/nested-chain) at assembly grade, and its
> kill sharpened the residue to a **two-part clause**: (a) uniform-block + (b) a two-universe licence, to
> exclude the Aut-orbit partition `X₃ = {{+1},{−1},{±i,±j,±k}}` (blocks 1,1,6 → z₃ = 12).
>
> **What this 6th pass BUYS (new, real):** (1) a **fourth** structural discriminator — the **product-factor**
> clause, derived from the OWNED product `Ω₈ = ABCD × {±} = D₂ × D₂ × {±}` (BOOK_01:763/782/841/1523/1535)
> — that is the FIRST clause to cleanly **exclude X₃ AND admit BOTH owned sizes {2,4} on Q₈, size-literal-free**
> (the 5th attempt's uniform-block gave only {4}). (2) A **decisive negative mapping**: the compute proves the
> size-2 sign-split of Q₈ is **NOT Aut(Q₈)-invariant** — which is exactly why "uniform-block Aut-invariant
> partitions of Q₈" collapse to {4} and lose the dyad. (3) The residue is now pinned to **ONE quantifier**
> (mutation test M2): *"an admissible extension alphabet is a factor of the owned capacity product."*
>
> **Why it still does NOT close:** that ONE quantifier is the **SAME unowned generative rule** the
> `GAP_E_DYAD_POWER_MEMO` already KILLED — the corpus owns a **two-item LIST** (`{D₂, ABCD}`, BOOK_01:1548
> "the only primitive unresolved capacities"), **not a generator** ("every admissible extension is a
> product-factor / dyad-power"). X₃'s block-count 3 is excluded by the **absence of a generator that produces
> it — silence, not forcing.** Owning the generator is a genuine OWNER DECISION, not forgeable from the
> primary sources this pass reads.
>
> **No registry row edited; no `.lean` added to the built tree; no cert minted; `053040` untouched.**
> Companion can-fail script `close_gap_e_6th_check.py` EXHIBITS `X₃`, runs all 5 task routes against it over a
> full enumeration of the Aut-invariant partitions of Q₈, and returns **rc=2 (window OPEN)** — the honest
> compute verdict. It is mutation-tested: M2 shows that if the product-factor quantifier were granted owned,
> the route WOULD seal (so the entire residue is that one ownership fact); M3 shows X₃ is structurally
> separable. No route both-excludes-and-admits-without-a-smuggle, so the script CANNOT be made to certify
> closure — it proves the gap OPEN.

**Pre-flight (2026-07-06):** `preflight.sh "GAP-E uniform-block product-factor block-count"` — no row owns the
exhaustiveness quantifier `∀X (AdmExt(X) → |X| ∈ {2,4})`. Cross-referenced, never duplicated:
`CLOSE_GAP_E_MEMO.md` §RESIDUE (the two-part clause this pass discharges the FIRST part of and maps the
second), `GAP_E_DYAD_POWER_MEMO.md` (the generator-clause kill this pass RESPECTS and does not resurrect),
`GAP_E_SYNTHESIS_MEMO.md` (computation layer reused), `D0-TOWER-STOP-NOEXT-001` (row 257, COUNT-3),
`D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (row 549).

---

## 0. What the 6th pass is for (the exact residue inherited from the 5th kill)

The 5th attempt's §RESIDUE (verbatim) named the minimal missing lemma as a **two-universe uniform-block clause**:

> *An owned rule that (a) each extension alphabet is a **uniform-block** partition — excluding X₃ — AND
> (b) admits the two owned universes (`Q₈` for ABCD, the center `Z`/two-port dyad for `D₂`), pinning the
> surviving sizes to `{2,4}`.*

The 5th kill's own compute showed the trouble: **uniform-block over partitions of Q₈ gives only size {4}**,
because the size-2 dyad is not a partition of Q₈ at all (it partitions the center `Z`, a *different universe*).
So the 5th residue is genuinely TWO things: a block-shape clause AND a universe-licence. This pass attacks both.

---

## 1. Owned pre-facts (verbatim, file:line, re-read on disk this pass, past ±10 lines)

Book: `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` (BOOK_01),
`01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` (BOOK_03).

### P1 — The role material is an OWNED DIRECT PRODUCT (THEOREM), nested two levels

- **BOOK_01:1523** (§01.20, verbatim): "A primitive two-port detector has a **binary terminal dyad `D₂`**.
  The complete terminal role set is therefore **`D₂ × D₂`**, with four roles. This is the four terminal roles
  A,B,C,D alphabet:" → **BOOK_01:1526**: `ABCD = D₂ × D₂,  |ABCD| = 4`.
- **BOOK_01:1535** (§01.20, verbatim): `Ω₈ = ABCD × {+,−}`, and **:1539**: "The **sign bit `{+,−}`** is the
  irreversibility of write/erase; it is the one bit that distinguishes the act from its undo, and **no further
  bit can be added without an exogenous orientation catalog**. Hence `Ω₈ = ABCD × {±}`, `|Ω₈| = 8`."
- **BOOK_01:782** (§01.7.1A, THEOREM): "The signed terminal role space `Ω₈ = {A,B,C,D} × {+,−}` is
  **strictly isomorphic** to the quaternion group `Q₈`." (also :763, :841, :1986 — the product is written at
  five sites.)

> **Owned generative tower (verbatim, not coined here):**
> `D₂` (size 2, the two-port dyad) → `ABCD = D₂ × D₂` (size 4) → `Ω₈ = ABCD × {±} = D₂ × D₂ × {±}` (size 8).
> **The two owned extension alphabets `{D₂, ABCD}` are exactly the two proper factors of this capacity product.**

### P2 — The two owned sizes are each forced by a SEPARATE singleton mechanism (verbatim)

- **BOOK_03:914-932** (§03.23.1, FORCED): "`|ABCD| = 4` … A minimal closed scene must realize exactly the
  four ABCD roles … `D_anchor < 4`: some role unrealized → external prop. Banned. `D_anchor > 4`: empty
  address slots … exogenous significance catalog. Banned. … `D_anchor = 4` is the unique survivor." — size 4
  forced by **role-count**.
- **BOOK_01:1539** (above) — size 2 forced by the **sign-bit** (one irreversibility bit, no further bit).
- **These are the two owned "block-generating cardinals": role-count = 4, sign-bit = 2.** (Task Route 2.)

### P3 — The extension list is a LIST, not a GENERATOR (the known constraint, verbatim — respected, not fought)

- **BOOK_01:1548** (§01.20, verbatim): "The next two shell extensions are **the only primitive unresolved
  capacities** over the pointed shell: the direct/return dyad and the full terminal role square." →
  `V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ ABCD` (:1551-1553).
- **`GAP_E_DYAD_POWER_MEMO §VERDICT` (owned prior kill):** the corpus owns this closed **two-item list**, NOT
  a **quantified generator** ("every admissible extension is a dyad-power / product-factor"). Size 6 (→ V₁₅)
  and size 3 (→ V₁₂) are "excluded by the **absence of a generator that would produce them** — silence, not
  forcing." **This memo does NOT resurrect the generator; it maps exactly where the generator would be needed.**

---

## 2. THE COMPUTE — X₃ exhibited, all 5 routes run against it (script `close_gap_e_6th_check.py`)

Full enumeration: the Aut(Q₈)-invariant set-partitions of Q₈ have **block-counts `{1,2,3,4,5,7,8}`**
(`R0.inv_blockcounts`). `X₃` (blocks 1,1,6, count 3) is among them (`X3.in_enumeration = True`) and is
Aut-invariant — this is why it escaped the 5th attempt's "canonical/Aut-invariant" clause.

| route | clause | excludes X₃ | admits size-4 | admits size-2 | size-literal-free | **owned as a quantifier?** |
|-------|--------|:---:|:---:|:---:|:---:|:---:|
| **1** | uniform-block partition **of Q₈** | ✓ | ✓ (ABCD 2,2,2,2) | **only via a non-Aut-inv or off-Q₈ object** | ✓ | — |
| **2** | block-count ∈ owned cardinals {4,2} | ✓ (3∉) | ✓ | ✓ | ✗ (imports {2,4}) | **NO — silence, not forcing (DYAD-POWER)** |
| **3** | no conjugacy-class fusion | ✓ | **✗ mis-excludes ABCD** | ✓ | ✓ | — (not a clean discriminator) |
| **4** | **product-factor of the owned capacity product** | ✓ | ✓ | ✓ (SIGN on Q₈) | ✓ | **NO — same unowned generator (DYAD-POWER)** |
| **5** | self-break sweep | — | — | — | — | confirms Route 1 loses the dyad |

**Decisive computed facts (all exact, script-backed):**

1. **`R1`/`R5` — uniform-block on Q₈ loses the dyad.** The uniform-block **Aut-invariant proper** partitions of
   Q₈ are **ONLY size 4** (`R5.uniform_on_Q8_loses_dyad`, proper counts `= [4]`). The size-2 **sign-split**
   `{+1,+i,+j,+k}|{−1,−i,−j,−k}` is a product-factor but is **NOT Aut(Q₈)-invariant**
   (`R1.SIGN_is_aut_invariant = False`: the automorphism `i ↦ −i` moves `+i` across blocks); the
   **center-split** `{+1}|{−1}` is Aut-invariant but partitions only `Z`, not Q₈. So "uniform-block on Q₈"
   alone gives `{4}`, confirming the 5th finding: uniform-block is **necessary but not sufficient** for `{2,4}`.
2. **`R4` — the product-factor clause is the FIRST to admit BOTH {2,4} on Q₈, literal-free, and exclude X₃.**
   Both factor partitions (`part_role` = ABCD, blocks 2,2,2,2; `part_sign` = SIGN, blocks 4,4) are fibers of a
   coordinate projection of the owned product `ABCD × {±}`; X₃ is **not** the fiber-partition of any coordinate
   projection (`D.X3_is_NOT_factor = True`). The discriminator `is_fiber_partition_of_product` references **no
   size literal** (`S.pred_factor_size_free`). **This is the genuine advance of the 6th pass** — it resolves
   the 5th residue's part-(a)+(b) *structurally* in ONE clause on ONE universe (Q₈), no second universe needed.
3. **`R2` — the owned-cardinal clause excludes X₃ but is exclusion-by-silence.** `|X₃| = 3 ∉ {role-count 4,
   sign-bit 2}`, so it is excluded; but "admissible block-count ∈ {owned cardinals}" is exactly the quantifier
   the DYAD-POWER memo showed is **not owned** — nothing owned forbids a size-3 alphabet; 3 simply has no owned
   generator. Flagged `owned_as_quantifier = False`.
4. **`R3` — conjugacy-class fusion is NOT a clean discriminator.** X₃'s big block fuses 3 conjugacy classes;
   but the ABCD block `{+1,−1} = Z` **itself fuses the two classes `{+1}`, `{−1}`**, so a "no class-fusion"
   rule wrongly kills ABCD too (`R3.class_fusion_admits_ABCD = False`). Route 3 is dead as a discriminator.

**Mutation test M2 (the pin):** if the product-factor quantifier (R4) were granted owned, R4 **would seal** —
it excludes X₃, admits {2,4}, is literal-free. Therefore **the entire remaining residue = ownership of that ONE
quantifier**: *"an admissible extension alphabet is a factor of the owned capacity product `D₂ × D₂ × {±}`."*

---

## 3. The five routes, adjudicated (task item "просеять руду" — all attempted, each landed)

- **Route 1 (uniform-block from indistinguishability).** *Aimed at:* "unequal blocks import a size-label =
  M1-forbidden catalog." **Result: LANDS as necessary, FAILS as sufficient.** Non-uniform X₃ has a
  distinguished size-6 block — a *privileged sub-object*, the exact shape C1 Exchangeability (BOOK_01:1572)
  forbids ("a part-internal exception names a **privileged vertex** — an exogenous parameter — violating M1").
  BUT (i) C1 is owned for *within-part permutations of scene-graph vertices* `S₉×S₁₁×S₁₃`, applying it to
  *block-sizes of an extension alphabet* is the SAME typing transfer the 5th skeptic killed on :1579; and
  (ii) even granted, uniform-block **on Q₈** gives only `{4}` (compute `R5`) — it loses the dyad. So Route 1
  cannot pin `{2,4}` alone. **Necessary, not sufficient, and the sufficiency step is unowned.**
- **Route 2 (block-count = owned cardinal: role-count 4, sign-bit 2).** **LANDS numerically, FAILS ownership.**
  `3 ∉ {2,4}` excludes X₃; but this is the DYAD-POWER quantifier — owned as two *singleton* forcings (why 4,
  why 2), NOT as a *closed set* ("admissible ⟹ ∈ {2,4}"). Exclusion-by-silence. **Not owned as a quantifier.**
- **Route 3 (conjugacy-class fusion).** **FAILS — not a clean discriminator.** Kills ABCD's own `Z`-block.
- **Route 4 (product-factor / group-theoretic enumeration).** **STRONGEST — the real advance.** Uniquely
  excludes X₃ AND admits both {2,4} on Q₈ literal-free. But "admissible = product-factor" IS the DYAD-POWER
  generator (a factor of `D₂×D₂×{±}` is a `D₂`-power) — **unowned.** The clause is *true of the two owned
  alphabets* (fingerprint) but not *owned as the rule that admits only them.*
- **Route 5 (self-break).** **SUCCEEDED at its job:** confirmed uniform-on-Q₈ loses the dyad, and confirmed
  the size-2 sign-split is not Aut-invariant — so there is no owned uniform Aut-invariant partition of Q₈ of a
  forbidden size that survives (block-counts reduce to {4}), and no owned non-partition that survives. The
  break is not a NEW escaping object; it is the **absence of an owned generator** — the same hole.

---

## 4. FINGERPRINTS (noted, NOT summed as proof)

- **F-1.** The two owned alphabets are the two coordinate-projections of `D₂ × D₂ × {±}` — a clean,
  Q₈-specific structure. Convention (EoR-1): "size-N alphabet" = **N letters = N blocks** (block-COUNT), since
  the zone arithmetic adds the letter-count (`V₁₁ = V₉ + |D₂|` adds 2 letters, `V₁₃ = V₉ + |ABCD|` adds 4).
  So ABCD = **4 blocks** of 2 elements → a 4-letter alphabet; SIGN = **2 blocks** of 4 → a 2-letter alphabet.
  The product-factor partitions have block-COUNTS **exactly {2, 4}** (`R4`, enumerated — not a literal). The
  rule is *satisfied by the corpus's own instances* and *excludes X₃* — right shape; only its ownership is missing.
- **F-2.** COUNT-3: base + two factor-alphabets = 3 zones = `D0-TOWER-STOP-NOEXT-001` (row 257).
- **F-3.** The sign-split's non-Aut-invariance is itself a fingerprint of the "two-universe" problem the 5th
  attempt named: the size-2 alphabet genuinely lives on a *finer* structure (the product coordinate / the
  center), not on Q₈-as-a-group — which is why no single-universe Aut-invariant clause reaches it.

---

## 5. NAMED RISKS & PRE-REGISTERED ATTACK SURFACE (aimed at myself)

- **SELF-ATT-1 (THE STRONGEST — is the product-factor clause a smuggle of {2,4}?).** The clause admits exactly
  the two coordinate-projections of a 2-factor product (role factor → 4 letters, sign factor → 2 letters), so
  `{2,4}` is the OUTPUT of the product's arity, not an input literal (`S.pred_factor_size_free` passes;
  block-counts are read off fibers). **BUT the honest worry:** "admissible alphabet = product-factor" is
  precisely the generative quantifier `GAP_E_DYAD_POWER_MEMO` KILLED as unowned. I have NOT re-derived it; I
  have *pre-registered* that R4's `owned_as_quantifier = False` and let the script return OPEN. If a skeptic
  finds I quietly treated R4 as owned anywhere, that is the smuggle — and the script's rc=2 is the guard.
- **SELF-ATT-1b (is admitting the non-Aut-invariant SIGN split as the size-2 alphabet a hidden escape?).**
  The compute shows SIGN (blocks 4,4) is NOT Aut(Q₈)-invariant, yet R4 admits it. **This is NOT a second
  escape — it is category-relative and disclosed.** R4 admits SIGN as a **product COORDINATE** (a fiber of
  the sign-projection of `D₂ × D₂ × {±}`), NOT as an Aut(Q₈)-invariant partition of Q₈. Coordinates of a
  product are invariant under the product's OWN coordinate symmetries, not under Aut(Q₈) (which scrambles the
  coordinates). So R4 lives in the "product-coordinate" category, a DIFFERENT category from the 5th attempt's
  "Aut-invariant partitions of Q₈." Crucially, **adopting the product-coordinate category as the owned home of
  alphabets IS the unowned generative quantifier** (the DYAD-POWER generator). Hence the skeptic-worry and the
  concession coincide: the non-Aut-invariance of SIGN is not an extra hole, it is the SAME single residue
  (ownership of the product-coordinate grammar), correctly localized. The window stays OPEN for exactly one reason.
- **SELF-ATT-2 (C1 transfer for uniform-block).** Route 1 leans on C1 (privileged-vertex ⊥M1) to motivate
  uniform-block; that is a within-part-permutation obligation transferred to alphabet block-sizes — the exact
  transfer killed on :1579/:1572 in the 5th pass. **Priced:** Route 1 is flagged necessary-not-sufficient and
  the sufficiency is NOT claimed owned; the closure does not rest on C1.
- **SELF-ATT-3 (did I smuggle {2,4} via OWNED_CARDINALS?).** The set `{2,4}` appears in Route 2 as a *lookup*
  of the two owned singleton mechanisms, and is flagged `size_literal_free = False, owned_as_quantifier =
  False` — explicitly NOT counted toward closure. It is disclosed, not hidden, and the smuggle-audit
  (`S.*_size_free`) covers only the structural discriminators (Routes 1,3,4), which are literal-free.
- **SELF-ATT-4 (is "product-factor" different from "characteristic-coset", the 5th attempt's dead clause?).**
  Partly: the 5th used "coset of a characteristic subgroup" (killed: X₃ is Aut-inv but not a coset space; and
  the center-split isn't a char-coset either). Product-factor is a DIFFERENT and cleaner object (fibers of a
  product projection) that DOES admit both {2,4} on Q₈ and does exclude X₃. The advance is real. The residue
  (ownership of the generator) is the SAME residue, correctly re-localized.
- **Reopening/closing hook:** if a maintainer OWNS the generative quantifier "an admissible zone-extension
  alphabet is a factor of the owned capacity product `D₂ × D₂ × {±}`" (equivalently the dyad-power generator),
  then R4 seals, X₃ dies, and GAP-E's upper bound `z₃ ≤ 13` closes — the partition rule (5th D1–D4) plus this
  factor clause is a complete derivation. Absent that one owned sentence, the window is OPEN.

---

## 6. What this memo does NOT do

- Does NOT mint, edit any registry row / cert / built `.lean` / `053040`.
- Does NOT resurrect the dyad-power / product-factor generator as owned (respects the DYAD-POWER kill).
- Does NOT claim uniform-block is M1-forced (Route 1 flagged necessary-not-sufficient; C1 transfer priced).
- Does NOT re-derive the 5th attempt's partition rule (D1–D4 reused by cross-reference — it stands).

---

## §SKEPTIC-#1 — INDEPENDENT PASS (2026-07-06, ACCEPTED IN FULL)

**VERDICT: CONFIRMED-PARTIAL-OPEN (honest, non-smuggled). NO KILL.** The independent skeptic attempted to
KILL on all five axes and could not. The memo's own verdict — *window OPEN, residue = ownership of ONE
quantifier* — is correct. Axis findings:

- **1. SMUGGLE CHECK (the fatal axis) — PASSES.** `pred_factor` is genuinely size-literal-free; independent
  enumeration confirms EXACTLY two partitions of Q₈ satisfy it (ABCD 2,2,2,2 and SIGN 4,4), so "block-counts
  EXACTLY {2,4}" is a real computation, not circular. The only `{2,4}` literal (`OWNED_CARDINALS`, Route 2) is
  honestly flagged `size_literal_free=False, owned_as_quantifier=False` and excluded from closure. No smuggle.
- **2. OVER-CLAIM — PASSES, advance honestly bounded.** Route 4 really does admit BOTH {2,4} on Q₈ (5th got
  only {4}). The SIGN-non-Aut-invariance is disclosed (F-3, SELF-ATT-1b) and uses a different (product-fiber)
  invariance, not a hidden move. "Residue re-localized, not discharged" is the correct label.
- **3. CITATIONS — ALL VERBATIM CORRECT, none reversed:** BOOK_01:1523 (D₂×D₂), :1535/:1539 (Ω₈=ABCD×{±},
  sign bit), :782 (Q₈ strict iso), :1548 (the LIST / "primitive unresolved capacities"), BOOK_03:914-932
  (D_anchor=4 role-count). Each used as the memo claims.
- **4. HONESTY OF OPEN — CORRECT.** The DYAD-POWER §RES defines the missing sentence as the exhaustiveness
  quantifier; Route 4's "admissible = product-factor" is that generator in disguise. BOOK_01:1548 owns
  *membership* (two named extensions), never *exhaustiveness*. OPEN is forced, not needless.
- **5. RESPECTS DYAD-POWER KILL — YES.** Every "closes/seals" is conditional; `route_seals()` requires
  `owned_as_quantifier is True`; R4 carries False; `sealing=NONE`; rc=2. Generator mapped, not resurrected.

### Errors of record (accepted, both applied — neither changes the verdict)
- **EoR-0 (smuggle-audit under-strong, latent, NOT exploited).** The old audit `' 2 ' not in s …` relied on
  surrounding-space matching, so a spaceless smuggle `len(p) in {2,4}` would have falsely passed. **REPAIRED:**
  the audit now TOKENIZES each discriminator (`size_literals_in`) and rejects any forbidden size-literal
  {2,3,4,6,8} regardless of spacing; a new mutation test `S.audit_catches_spaceless_smuggle` proves the audit
  fires on `len(p) in {2,4}`. Re-run clean (rc=2), all `S.*_size_free` still pass (the real discriminators
  carry no size-literal).
- **EoR-1 (label ambiguity "size-N alphabet").** "size-N" now explicitly means **N letters = N blocks**
  (block-COUNT), per the zone arithmetic (`V₁₁=+2 letters`, `V₁₃=+4 letters`): ABCD = 4 blocks of 2 = a
  4-letter alphabet; SIGN = 2 blocks of 4 = a 2-letter alphabet. **REPAIRED** in the script (convention comment
  + `assert len(ABCD)==4 and len(SIGN)==2`) and in memo F-1.

### What survives, and at what grade
- **The partition rule (5th D1–D4):** unchanged, assembly-grade, cross-referenced (kills Sub/Out/chain).
- **The product-factor discriminator (6th, NEW):** a real structural advance — the FIRST clause excluding X₃
  AND admitting both {2,4} on Q₈ literal-free. Grade: **STRUCTURAL FINGERPRINT**, not owned as a rule.
- **The window UPPER bound / X₃ exclusion:** OPEN. The sole residue is ownership of ONE generative quantifier
  ("an admissible zone-extension alphabet is a factor/coordinate of the owned capacity product `D₂×D₂×{±}`"),
  equivalent to the DYAD-POWER generator — an **OWNER DECISION**, not forgeable from the primary sources.

**Reopening/closing hook (unchanged):** owning that one quantifier revives R4 (and the 5th D1–D4), sealing
`z₃ ≤ 13`. Absent it, `z₃ = 12` (the X₃ alphabet) remains admissible under every clause the corpus owns —
GAP-E's completeness clause is OPEN (sixth independent confirmation).

> **[EoR — GAPE-1011 integration 2026-07-06]** [EoR 2026-07-06, 10th pass] P3 (:96-97) misquotes the DYAD-POWER verdict — 'size 3 (→V₁₂)' is an interpolation absent from the source (which names size 6 only, and whose OWN-4 adjudicates odd steps owned-killed); the final line's 'z₃ = 12 remains admissible under every clause the corpus owns' is retracted. Product-factor discriminator and the ownership verdict on the quantifier unaffected.
