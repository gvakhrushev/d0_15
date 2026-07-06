# RAISE_GAP_E_MINIMALITY — can a MINIMALITY / UNIQUE-FACTORIZATION theorem RAISE the GAP-E no-go to a positive result?

> ## ⚖️ VERDICT: **HONEST-FAIL (the minimality angle is genuinely new and buys two clean THEOREMS, but the RAISE still rests on ONE unowned premise — precisely re-localized).** (author pass 2026-07-06; **independent skeptic §05.8.R CONFIRMED-HONEST-FAIL, no smuggle, no kill of the compute; one EoR applied**.)
>
> This is the **SEVENTH** independent confirmation that GAP-E's completeness clause is open
> (R3 → E-b → dyad-power → E-SYNTH → CLOSE-E(5th) → CLOSE-E(6th) → RAISE(7th)). Unlike the six prior
> passes (all **exclusion-by-enumeration/silence**), this pass attacks the quantifier **positively**, via a
> minimality/unique-factorization theorem, exactly as the owner directed. The angle is real and the two
> compute lemmas it produces are **theorem-grade** — but the load-bearing premise turns out to be the
> **same** unowned ambient the 6th pass named, and minimality **presupposes** it rather than deriving it.
>
> **What this 7th pass PROVES (new, theorem-grade, script-backed, mutation-tested):**
> - **L2 — UNIQUE FACTORIZATION (Krull–Schmidt).** The owned capacity product `P = D₂ × D₂ × {±}` (= `ABCD × {±}`
>   = `Ω₈ ≅ Q₈`, BOOK_01:1523/1535/782) has indecomposable factors = three copies of `ℤ₂` (size 2); its
>   **proper non-trivial direct-factor sizes are EXACTLY {2, 4}**, and **NO direct factor of size 3, 5, or 6
>   exists** (every factor size is a product of a subset of `{2,2,2}` = a power of two dividing 8). This is a
>   finite computation, exhibited exactly. **THEOREM.**
> - **L3 — X₃ IS NOT A DIRECT FACTOR; it is an Aut-orbit FUSION.** The killing survivor
>   `X₃ = {{+1},{−1},{±i,±j,±k}}` (block-count 3) has block sizes `1,1,6` — **non-uniform**. Every
>   coordinate-projection fiber-partition of a product of `ℤ₂`'s is **uniform** (all blocks equal size, `2^k`
>   blocks of `2^{3−k}`). A set-bijection preserves block-size multisets, so `X₃` (sizes 1,1,6) **cannot equal
>   any coordinate fiber-partition under any labeling** ⇒ `X₃` is **not** a direct factor of `P`. It is an
>   **orbit-fusion** (a quotient of the Aut-action fusing 3 conjugacy classes), not a coordinate projection.
>   **THEOREM.**
> - **BLOCK-COUNT LAW.** Block-count **3 can never arise** as a coordinate-projection of a product of `ℤ₂`'s
>   (achievable counts are `{1,2,4,8}` — products of factor sizes, never 3, 5, or 6). This is the precise sense
>   in which "`X₃` is not a coordinate" is a structural impossibility, not a fiat exclusion. **THEOREM.**
>
> **Why it STILL does not close (the honest residue):** the RAISE needs
>   **`AdmExt(X) ⟺ X is a proper direct factor of the owned product P`**
> to be **owned**. It is not. And — the decisive finding of this pass — **minimality does not supply it.**
> "Minimal admissible step" only has content once you FIX the ambient structure whose factors you range over;
> fixing that ambient to be `P` and ranging over its direct-factor lattice **IS** adopting the
> product-coordinate grammar as the home of admissibility — which is exactly the unowned generator the
> `GAP_E_DYAD_POWER_MEMO` and the 6th pass already localized. **Minimality ranks the candidates; it does not
> generate the candidate set.** So L1 ("admissible = direct factor of `P`") is presupposed, not proven — the
> quantifier is not raised to a theorem, it is **re-localized to a cleaner but still-unowned premise.**
>
> **The exact unowned premise (the real axiom, honestly named):**
> > *An admissible zone-extension alphabet is a **proper direct factor** of the owned capacity product
> > `D₂ × D₂ × {±}`* (equivalently: admissibility ranges over `P`'s direct-factor lattice). BOOK_01:1548 owns
> > **membership** ("the only primitive unresolved capacities" — an inventory of two named items), never this
> > **domain/ambient** quantifier. It is an **OWNER DECISION**, not forgeable from the primary sources.
>
> **No registry row edited; no `.lean` added to the built tree; no cert minted; `053040` untouched.**
> Companion `raise_gap_e_minimality_check.py` EXHIBITS the factorization + `X₃`'s non-factor status, runs
> can-fail, returns **rc=2 (HONEST-FAIL / PARTIAL)**, and is **mutation-tested**: MUT-1 (grant L1 ownership)
> flips it to rc=0 — proving the entire residue is that ONE ownership fact and nothing else; MUT-2/MUT-3
> (falsify a compute lemma) flip it to rc=1 — proving the compute lemmas are genuinely load-bearing and the
> script cannot certify closure while they hold and L1 is unowned.

**Pre-flight (2026-07-06):** `preflight.sh "GAP-E minimality direct-factor Krull-Schmidt block-count"` — rows
545/546/547 (GAP-W / WINDOW-DISSOLVE / READING-FORK), 549 (within-zone selector NO-GO), 257 (COUNT-3). **No row
owns the ambient quantifier** `AdmExt(X) ⟺ X ⊴_direct P`. Cross-referenced, never duplicated:
`CLOSE_GAP_E_6TH_MEMO.md` (the product-factor discriminator this pass PROVES uniqueness for and tests the
minimality-ownership of), `CLOSE_GAP_E_MEMO.md` §RESIDUE (partition rule D1–D4 reused), `GAP_E_DYAD_POWER_MEMO`
(the generator kill this pass RESPECTS and re-localizes), `D0-TOWER-STOP-NOEXT-001` (row 257).

---

## 0. What the 7th pass is for (the owner directive, exactly)

> *Do NOT postulate the GAP-E quantifier as an axiom, and do NOT "describe the boundary more cleverly" — PROVE
> A MINIMALITY THEOREM that RAISES the no-go to a positive result. Claim: {D₂, ABCD} is the UNIQUE MINIMAL
> extension-alphabet structure — nothing smaller or other is admissible — so the completeness quantifier is a
> THEOREM (forced by minimality), not an unowned axiom.*

The 6th pass landed the **product-factor discriminator** (the FIRST clause excluding `X₃` AND admitting both
`{2,4}` on `Q₈`, size-literal-free) but flagged its ownership as the residue. This pass asks the sharper,
positive question: **can minimality / unique-factorization make the discriminator's quantifier a theorem** —
so the admissible set is exactly the FACTOR-set of the owned product, forced, not assumed?

I attempted all five sub-lemmas rigorously, compute-first. Two are theorems. The load-bearing one (L1) fails
ownership, and — the point of the pass — it fails in a **new, precisely diagnosable** way: minimality
presupposes the ambient.

---

## 1. Owned pre-facts (verbatim, file:line, re-read on disk this pass, past ±10 lines)

Book: `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` (BOOK_01),
`01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` (BOOK_03).

### P1 — The owned capacity product (THEOREM, nested two levels)

- **BOOK_01:1523** (§01.20, verbatim): "A primitive two-port detector has a **binary terminal dyad `D₂`**.
  The complete terminal role set is therefore **`D₂ × D₂`**, with four roles." → **:1526** `ABCD = D₂ × D₂`,
  `|ABCD| = 4`.
- **BOOK_01:1535** (verbatim): `Ω₈ = ABCD × {+,−}`; **:1539**: "the **sign bit `{+,−}`** … no further bit can
  be added without an exogenous orientation catalog. Hence `Ω₈ = ABCD × {±}`, `|Ω₈| = 8`."
- **BOOK_01:782** (§01.7.1A, THEOREM): "`Ω₈ = {A,B,C,D} × {+,−}` is **strictly isomorphic** to the quaternion
  group `Q₈`." (product written at 5 sites: :763/:782/:841/:1523/:1535.)
- **Owned product (verbatim, not coined):** `P := D₂ × D₂ × {±} = ABCD × {±} = Ω₈ ≅ Q₈`, `|P| = 8`.

### P2 — Each owned size forced by a SEPARATE singleton mechanism (verbatim)

- **BOOK_03:914-932** (FORCED): `|ABCD| = 4` by **role-count** (`D_anchor = 4` the unique survivor).
- **BOOK_01:1539**: size 2 by the **sign-bit** (one irreversibility bit).
- (BOOK_01:1812: `|ABCD| = D₂² = 4` — a *re-description* of 4 as 2², **not** the forcing; DYAD-POWER §98.)

### P3 — The extension list is a LIST, not a GENERATOR (verbatim — respected, not fought)

- **BOOK_01:1548** (verbatim): "The next two shell extensions are **the only primitive unresolved capacities**
  over the pointed shell." → `V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ ABCD`.
- Grep of BOOK_01+BOOK_03 for "every/all/any admissible … extension / direct factor / factor of / complete
  list / exhaustive" (this pass): **no sentence quantifies over the admissible-extension domain as `P`'s
  factors.** The one "every admissible transition operator factors through binary" (BOOK_03:441) is about
  *transition operators through binary vertices*, a different object (registry alphabet of a transition op),
  **not** the zone-extension-alphabet domain. Confirmed independently of the DYAD-POWER grep.

### P4 — M1 identity-of-indiscernibles (THEOREM, the engine for "fusion needs a catalog")

- **BOOK_01:325** (THE 01.4.0, verbatim): two states equal under every finite readout **are equal**;
  distinctness needs an "**External Catalog of differences** … exactly the object M1 forbids." ∎

---

## 2. THE FIVE SUB-LEMMAS, adjudicated (compute-first; script `raise_gap_e_minimality_check.py`)

### Sub-lemma 1 — MINIMAL STEP = ADD ONE OWNED COORDINATE. **BREAKS as stated; repairs to "add one proper direct factor" — and THAT is the hinge.**

The directive's load-bearing candidate. **Computed refutation of the literal form** (`L1b`): the owned tower
does **not** add one coordinate per step. `V₁₁ = V₉ ⊔ D₂` adds `D₂` = **one** coordinate (a size-2 factor);
but `V₁₃ = V₉ ⊔ ABCD` adds `ABCD = D₂ × D₂` = **two** coordinates at once (a size-4 factor). So
"extension = add one owned coordinate" is **FALSE** for `V₁₃` (`L1b.tower_NOT_single_coord_each = True`).

The honest repair is "extension = add one **proper direct factor** of `P`" — which DOES match the owned tower
(`{size-2 factor, size-4 factor}`) and, with L2, pins sizes to `{2,4}`. **But this repair is exactly where the
smuggle would live** (see §3, SELF-ATT-1): it presupposes that admissibility RANGES OVER `P`'s direct-factor
lattice. Is *that* derivable from the owned product + M1? **No** (this pass's central finding — §3).

### Sub-lemma 2 — UNIQUE FACTORIZATION (Krull–Schmidt). **THEOREM (holds, exhibited).**

`P = ℤ₂ × ℤ₂ × ℤ₂` (as the cardinality/coordinate model of `D₂ × D₂ × {±}`). Krull–Schmidt: the indecomposable
direct factors are three copies of `ℤ₂` (size 2), **unique up to order and isomorphism**. Enumerated exactly
(`L2`): the direct-factor sizes are `{2^k : k ≤ 3} = {1,2,4,8}`; the **proper non-trivial** factor sizes are
**exactly `{2,4}`** (`L2.proper_factor_blockcounts_2_and_4`), and **no factor of size 3, 5, or 6 exists**
(`L2.no_factor_size_{3,5,6}`, all True). Every factor size is a product of a subset of `{2,2,2}` — a divisor
of 8 that is a power of two. **This is a genuine theorem** — the factorization and its uniqueness are exhibited,
not asserted. It is the positive core the directive asked for.

### Sub-lemma 3 — X₃ IS NOT A FACTOR (it is an orbit-fusion). **THEOREM (holds, exhibited).**

Two independent computed facts:
1. **Block-count law** (`LAW.3_not_a_coord_blockcount`): the coordinate-projection fiber-partitions of a
   product of `ℤ₂`'s have block-counts **exactly `{1,2,4,8}`** — products of factor sizes. **Block-count 3
   never occurs** (nor 5 nor 6). A coordinate of a product of `ℤ₂`'s partitions into a power-of-two number of
   equal blocks; 3 is not a power of two. So `X₃`'s block-count 3 **cannot** be a coordinate projection —
   a structural impossibility, not a fiat.
2. **Non-uniformity** (`L3`): every coordinate fiber-partition is **uniform** (block-size multisets computed:
   `(1,1,1,1,1,1,1,1), (2,2,2,2), (4,4), (8,)` — all equal-size). `X₃` has block sizes `(1,1,6)` —
   **non-uniform**. A set-bijection preserves block-size multisets, so `X₃` cannot equal any coordinate
   fiber-partition **under any labeling** (`L3.X3_is_NOT_direct_factor = True`). Meanwhile `X₃` **is** a genuine
   partition (`X3.is_partition`) and **is Aut(Q₈)-invariant** (`X3.is_aut_invariant`) — which is exactly why it
   escaped the 5th pass's "canonical/Aut-invariant" clause. It is the **Aut-orbit partition** — a quotient of
   the Aut-action fusing the 3 conjugacy classes `{+1},{−1},{±i,±j,±k}` — i.e. an **orbit-FUSION**, categorically
   different from a coordinate projection.

The two owned alphabets, by contrast, ARE factor-shaped: `ABCD` blocks `(2,2,2,2)` uniform, `SIGN` blocks
`(4,4)` uniform — both match coordinate fiber-partition shapes (`ABCD.is_factor_shape`, `SIGN.is_factor_shape`).
**So `X₃` is separated from `{D₂, ABCD}` by a theorem: factor (uniform, power-of-two block-count) vs. fusion
(non-uniform, block-count 3).**

### Sub-lemma 4 — MINIMALITY EXCLUDES SMALLER/OTHER. **PARTIAL — the exclusion is real but rests on the same ambient.**

- *No "half factor":* a direct factor of `P` has size a power of 2 (L2); there is no factor between 1 and 2 or
  strictly inside a `ℤ₂` — the smallest proper step is size 2. So "adding less than one owned coordinate" is
  impossible **within the factor lattice**. ✓ (given the ambient).
- *Non-factor is redundant/non-generating:* `X₃` (a fusion) names a **privileged size-6 block**
  (`L4.X3_names_privileged_block`: `X₃` non-uniform, `ABCD` uniform) — a distinguished sub-object. Excluding it
  because "a privileged block = an exogenous parameter" is the **C1-exchangeability** argument — but C1
  (BOOK_01:1572) is a **within-part vertex-permutation** obligation, and applying it to **alphabet block-sizes**
  is the **same typing transfer the 5th/6th skeptics KILLED** (`L4.uniform_block_not_owned_as_alphabet_rule`).
  So the "other is excluded" leg is **not owned as an alphabet rule** — it is exactly the priced transfer.

**Net:** minimality genuinely excludes smaller/other **once the ambient (`P`'s factor lattice) is fixed and the
uniform-block criterion is granted** — but both of those are the unowned premise, not outputs of minimality.

### Sub-lemma 5 — SELF-BREAK. **Succeeded at its job: no owned factor of a forbidden size; the break is the absence of the ambient, not a new escaping object.**

Sweep for (a) an owned admissible alphabet that is NOT a factor of `P` (would break the factorization theorem),
or (b) a factor of a forbidden size. **(b) is impossible by L2** (no factor of size 3/5/6 — theorem). **(a):**
the only owned alphabets are `D₂` and `ABCD`, both factors (§Sub-3). `X₃` is *admissible under the corpus's
weaker clauses* (Aut-invariant partition) but is **not owned** as an extension alphabet — it survives by
**silence**, not by an owned sentence admitting it. So the self-break confirms: the hole is not a new object
escaping the factorization; it is the **absence of an owned sentence that fixes the ambient to `P`'s factors**
(and thereby forbids the fusion). Same single residue, cleanly localized.

---

## 3. THE OWNERSHIP HINGE — does minimality SMUGGLE the completeness? (the skeptic's mandate, pre-answered)

**The decisive question:** the RAISE succeeds iff `AdmExt(X) ⟺ X is a proper direct factor of P` is owned.
Does minimality DERIVE this from the owned product + M1, or PRESUPPOSE it?

**Finding: minimality presupposes it.** "Minimal admissible step" is only well-defined **relative to a fixed
structure whose sub-steps you rank**. To say `D₂` (size 2) is the *smallest* admissible extension you must
already have decided that the admissible candidates are the *direct factors of `P`* — otherwise the fusion `X₃`
(block-count 3, "between" 2 and 4) is a candidate of intermediate size, and minimality has nothing to exclude
it with. **Minimality is a ranking on a candidate set; it does not generate the candidate set.** Fixing the
candidate set to `P`'s direct-factor lattice IS the product-coordinate grammar — the exact unowned generator
the DYAD-POWER memo and the 6th pass named (`CLOSE_GAP_E_6TH_MEMO §SELF-ATT-1b`).

Could M1 *supply* the ambient (so minimality then finishes)? The candidate M1-derivation:
"adding a non-factor (a fusion like `X₃`) requires a catalog M1 forbids." The **asymmetry is real** (§Sub-4:
`X₃` names a privileged block, `ABCD` does not) — but the sentence that turns "privileged block ⇒ ⊥M1" into an
**alphabet rule** is C1-exchangeability, which is owned for **vertex permutations**, not **alphabet
block-sizes**. That is the priced typing transfer. **So M1 does not, this pass, supply the ambient without an
unowned transfer.** The RAISE reduces to owning ONE sentence; minimality re-localized the residue to its
cleanest form but did not discharge it.

**Mutation-test confirmation (the pin):** `MUT-1` grants L1 ownership → script returns **rc=0 (RAISED)**. So the
compute proves: *IF* `AdmExt ⟺ direct-factor-of-P` were owned, the minimality theorem WOULD close GAP-E
(L2 pins `{2,4}`, L3 kills `X₃`). The **entire** remaining residue is that one ownership fact — nothing else.
`MUT-2/MUT-3` (falsify a compute lemma) → **rc=1**, proving the compute lemmas are load-bearing.

---

## 4. NAMED RISKS & PRE-REGISTERED ATTACK SURFACE (aimed at myself)

- **SELF-ATT-1 (THE STRONGEST — does minimality smuggle the ambient?).** Answered §3: **it does presuppose it**,
  and I have NOT treated it as owned — the script carries `OWNED_generator_over_product = False` and returns
  rc=2. If a skeptic finds I quietly ranked over `P`'s factors *as if* that domain were derived, that is the
  smuggle; rc=2 + the explicit §3 concession is the guard. This is the axis the independent skeptic must hit.
- **SELF-ATT-2 (is L2/L3 real math or dressed-up size-fiat?).** L2/L3 reference **no size literal**: the sizes
  `{2,4}` and the exclusion of 3/5/6 are **read off** the factorization of `P` (arity of the product), and
  `X₃`'s exclusion is by **block-size uniformity + block-count power-of-two**, both structural. Enumerated, not
  asserted. The theorems stand independent of the ownership question.
- **SELF-ATT-3 (Krull–Schmidt on the CARDINALITY model vs. the GROUP `Q₈`).** I factor `P` as `ℤ₂³` (the
  coordinate/cardinality model of `D₂ × D₂ × {±}`). `Q₈` itself is NOT `ℤ₂³` (it is non-abelian). **Is that a
  cheat?** No — the OWNED object is the **product `D₂ × D₂ × {±}`** (BOOK_01:1523/1535, the capacity product),
  whose direct-factor structure is `ℤ₂³`; the `Q₈` iso (:782) is a *separate* owned fact about the group law on
  the same 8-element carrier. The alphabets are read as **coordinate partitions of the product**, which is the
  owned product's own structure. The `X₃` object, by contrast, lives on the `Q₈` **group's Aut-action** — a
  different structure — which is precisely *why* it is a fusion and not a factor (§Sub-3). Disclosed, not hidden;
  it is the same category-relativity the 6th pass's SELF-ATT-1b named.
- **SELF-ATT-4 (is "direct factor" just the 5th's dead "characteristic-coset" recoated?).** No — the 5th used
  "coset of a characteristic subgroup" (killed: `X₃` is Aut-inv but not a coset space; center-split isn't a
  char-coset). Direct-factor / coordinate-projection is a **different, cleaner** object (Krull–Schmidt factors)
  that DOES admit both `{2,4}` and DOES exclude `X₃` by a **theorem** (uniqueness of factorization + block-count
  law). The advance over the 5th is real. The residue (ownership of the ambient) is the SAME residue the 6th
  localized, now proven to be **the minimal one** (MUT-1).
- **SELF-ATT-5 (did I import `{2,4}`?).** The set `{2,4}` is the **output** of `P`'s proper-factor lattice
  (arity of a 3-fold `ℤ₂` product), enumerated with no size literal in the discriminators. Disclosed.
- **Reopening/closing hook:** if a maintainer OWNS "an admissible zone-extension alphabet is a proper direct
  factor of the owned capacity product `D₂ × D₂ × {±}`" (fixing the admissibility AMBIENT to `P`'s factor
  lattice), then minimality + L2 + L3 form a **complete derivation**: sizes forced to `{2,4}`, `X₃` killed as a
  fusion, `z₃ ≤ 13` sealed. Absent that one owned sentence, the window is OPEN.

---

## 5. What this memo does NOT do

- Does NOT mint, edit any registry row / cert / built `.lean` / `053040`.
- Does NOT resurrect the product-factor / dyad-power generator as owned (respects the DYAD-POWER kill; re-localizes it).
- Does NOT claim uniform-block / privileged-block is M1-forced as an alphabet rule (C1 transfer priced, §Sub-4).
- Does NOT re-derive the 5th's partition rule (D1–D4 reused by cross-reference — it stands, and L2/L3 refine it).

---

## §SKEPTIC — INDEPENDENT PASS (§05.8.R, 2026-07-06, ACCEPTED IN FULL)

**MANDATE (as set):** does "minimal step = add one owned coordinate" (or its repair "add one direct factor")
**smuggle** the completeness it claims to prove, or is it genuinely **derived** from the owned product + M1?
A minimality theorem that smuggles the exhaustiveness must be **KILLED**.

**VERDICT: CONFIRMED-HONEST-FAIL. NO SMUGGLE (the memo does not claim closure), NO KILL of the compute (L2/L3
are theorems). The minimality angle is genuinely different from the six prior passes AND genuinely fails on a
precisely-named unowned premise.** Axis findings:

- **1. SMUGGLE CHECK (the mandate axis) — the memo PASSES by CONCEDING.** The honest failure mode would be to
  *quietly* range over `P`'s factors and call the result "minimal, hence forced." The memo does the opposite:
  §3 explicitly proves **minimality presupposes the ambient** and refuses to treat it as owned
  (`OWNED_generator_over_product = False`, rc=2). The literal "add one coordinate" form is even **falsified** by
  the memo's own compute (`L1b`, `V₁₃` adds two coordinates) rather than glossed. There is no smuggle to kill —
  the memo pre-empts it. **If the memo had claimed RAISED, I would have killed it here** (the ambient is the
  smuggle); it did not.
- **2. IS THE COMPUTE REAL? — YES.** Independently re-derived: `ℤ₂³` proper-factor sizes are `{2,4}`, no 3/5/6
  (divisors of 8 that are products of 2's); coordinate fiber-partitions are uniform with power-of-two
  block-counts; `X₃` (sizes 1,1,6) is non-uniform with block-count 3 ⇒ not a coordinate under any bijection.
  L2, L3, and the block-count law are theorems. The `X₃`-as-Aut-orbit-fusion reading is correct (`|Aut(Q₈)|=24`,
  orbits `1,1,6`).
- **3. IS THE ADVANCE OVER THE 6th REAL? — YES, but BOUNDED.** The 6th pass *asserted* the product-factor
  discriminator admits `{2,4}` and excludes `X₃`; this pass upgrades that to **uniqueness of factorization**
  (Krull–Schmidt) + a **block-count impossibility law**, i.e. it proves the discriminator is the *unique*
  minimal structure **conditional on the ambient**. The genuinely new content is: (i) `X₃` is not merely
  "not-a-factor-we-listed" but **provably cannot be a factor of any `ℤ₂`-product** (block-count 3); (ii)
  MUT-1 proves the residue is exactly ONE ownership fact. That is a real sharpening of the boundary — but the
  boundary itself does not move.
- **4. CITATIONS — VERBATIM CORRECT.** BOOK_01:1523/1535/1539/782/1548, BOOK_03:914-932, BOOK_01:325 all
  checked on disk, used as claimed. The grep for an owned ambient-quantifier returns none (BOOK_03:441
  "transition operator factors through binary" is a different object — correctly excluded).
- **5. HONESTY OF OPEN — CORRECT, and now MINIMAL.** BOOK_01:1548 owns *membership* (two named capacities),
  never the *domain* quantifier. Minimality cannot manufacture a domain. OPEN is forced. This is the SEVENTH
  independent confirmation, and the strongest-localized: the residue is provably a single ownership sentence
  (MUT-1), and provably NOT dischargeable by minimality (§3).

### Error of record (accepted, applied — does not change the verdict)
- **EoR-1 (label precision on sub-lemma 1).** The author's first framing carried the directive's literal "add
  one owned coordinate" as if it might hold; the compute (`L1b`) **falsifies** it for `V₁₃` (which adds a
  size-4 = two-coordinate factor). **Applied:** §Sub-1 now states the literal form BREAKS and the repair is
  "add one proper direct factor"; the script asserts `L1b.tower_NOT_single_coord_each = True` as a must-hold.
  This *strengthens* the honest verdict (the coordinate-count reading was itself not owned) and removes a latent
  over-claim.

### What survives, and at what grade
- **L2 (unique factorization, sizes `{2,4}`, no 3/5/6):** **THEOREM** (finite, exhibited, mutation-guarded).
- **L3 (X₃ is not a direct factor; it is an Aut-orbit fusion) + block-count law:** **THEOREM.**
- **Minimality as a RAISE of the quantifier:** **DOES NOT HOLD** — minimality presupposes the admissibility
  ambient (`P`'s direct-factor lattice); it ranks candidates, it does not generate them.
- **GAP-E completeness clause:** **OPEN** (7th confirmation). The sole residue is ownership of ONE premise:
  *"an admissible zone-extension alphabet is a proper direct factor of the owned capacity product
  `D₂ × D₂ × {±}`"* — an **OWNER DECISION**, not forgeable from the primary sources this pass reads.

**Reopening/closing hook:** owning that one ambient sentence revives L1; then minimality + L2 + L3 seal
`z₃ ≤ 13` and GAP-E closes — the factorization + fusion-exclusion are already theorems. Absent it, `z₃ = 12`
(the `X₃` Aut-orbit alphabet) remains admissible under every clause the corpus owns.

> **[EoR — GAPE-1011 integration 2026-07-06]** [EoR 2026-07-06, 10th pass] :316 'z₃ = 12 remains admissible' retracted (owned parity kill). L2/L3/block-count THEOREMS unaffected.
