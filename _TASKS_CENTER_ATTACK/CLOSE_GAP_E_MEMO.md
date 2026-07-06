# CLOSE_GAP_E — deriving the alphabet-grammar clause (partition-as-added-vertices) from owned M1 + scene structure

> ## ⛔ VERDICT: **KILLED-AS-CLOSURE → FAILED-BOUNDARY** (Skeptic #1, independent pass, 2026-07-06 — ACCEPTED IN FULL, no defense)
>
> **CLOSE-E does NOT close GAP-E.** The partition rule (D1–D4) is real and excludes `Sub(Q₈)`, `Out(Q₈)`,
> and the nested chain — but the SIZE clause (D5–D6) is dead: a **named second object escapes** —
> the **Aut-orbit partition `X₃ = {{+1}, {−1}, {±i,±j,±k}}`** (verified on disk: a genuine partition,
> Aut-invariant, size 3 → **z₃ = 12**). It passes D3 (it IS a partition) AND D5's stated "canonical/
> Aut-invariant" clause, so the window UPPER bound is **NOT sealed** against a size-3 alphabet. My D5
> "canonical clause" silently narrowed "Aut-invariant partition" to "coset partition of a characteristic
> subgroup" — a narrowing that is **not owned**, and that inconsistently keeps my own size-2 center-split
> (itself not a coset partition of a characteristic subgroup) while excluding `X₃`. That asymmetry is
> exactly the fiat the derivation claimed to remove. Also: the original script hardcoded
> `admissible_sizes = {2,4}` (a compute-first violation — fixed mid-pass but the deeper narrowing survived
> the fix), and the `:1616` characteristic citation is from the flavour-window `(ℤ/44)*` section, a
> different object from Q₈ role material (SELF-ATT-2's transfer is fatal for D5, not cautionary).
> See §SKEPTIC-#1 (verdict + errors of record) and §RESIDUE (the sharpened minimal missing lemma) at foot.
> **No closure language in this memo is operative.**
>
> **What SURVIVES:** D1–D4 (the partition rule as an assembly-grade owned-schema transfer) + the exclusion
> of the three original counter-objects. What is DEAD: D5 (size ⟹ {2,4}) and D6 (upper bound z₃ ≤ 13).
>
> No registry row edited; no `.lean` added to the built tree; no cert minted; `053040` untouched.
> Companion can-fail script `close_gap_e_check.py` was REPAIRED per the kill (§SKEPTIC-#1 repairs): it now
> ENUMERATES all 4140 set-partitions of Q₈ (filtered to Aut-invariant), EXHIBITS `X₃` as the size-3 survivor,
> and its verdict flipped to **KILLED** (47/47 checks, **rc=2** = intended KILLED). It is mutation-tested: the
> exact "coset-only" smuggle the skeptic caught makes `R5.X3_in_enumeration` FAIL (rc=1) — the script cannot be
> made to certify the closure without either exhibiting `X₃` (kills it) or smuggling (fails). It now proves the
> gap OPEN, not closed.

**Pre-flight (2026-07-06):** `preflight.sh GAP-E partition vertex "extension alphabet"` — rows 545/546/547
(GAP-W / WINDOW-DISSOLVE / READING-FORK, all OPEN/PROOF-TARGET), 549 (within-zone selector NO-GO,
LEAN_PROVED). **No row owns the exhaustiveness clause** `∀X (AdmExt(X) → |X| ∈ {2,4})`. Cross-referenced,
never duplicated: `GAP_E_SYNTHESIS_MEMO.md` (the KILLED E-SYNTH — this memo discharges its sharpened
missing object), `GAP_E_DYAD_POWER_MEMO §RES` (owns "the missing sentence"), `GAP_E_COMPLETENESS_MEMO`
(R3 two-route spec), `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (row 549, used as a fingerprint,
not re-litigated), `D0-TOWER-STOP-NOEXT-001` (row 257, COUNT-3).

---

## 0. What GAP-E is, and what this memo claims

GAP-E is the **extension-alphabet completeness clause** of the `[9,13]` window: the sentence that the
owned extension list `{D₂ (size 2), ABCD (size 4)}` is **complete** — no admissible third alphabet of
any other size (in particular no size-6 `z₃ = 15`, no size-3 `z₃ = 12`) exists. The window's LOWER
bound is GAP-W's business (witness `+1`, row 545); this clause is its **UPPER** bound.

Four prior campaigns confirmed the clause open and **sharpened its missing object** to a single sentence
(`GAP_E_SYNTHESIS_MEMO §SKEPTIC-#1`, verbatim):

> **(MISSING — the alphabet-grammar clause.)** An owned rule stating which canonical role-objects can
> serve as extension ALPHABETS: the letters of an extension alphabet are **states realized as added
> vertices** — elements or cosets, i.e. **blocks of a partition** of the role material — and not derived
> families (subgroups, which pairwise overlap in the identity; automorphism classes, which are not vertex
> material; nested chains).

The E-SYNTH ownership-check found this grammar **verbatim-owned at the instance level** at every definition
site but **not** owned as a quantified rule, and left the one-quantifier lift as an "OWNER DECISION."

**This memo takes that decision by DERIVING the quantifier** — not asserting it. The claim:

> **CLAIM (CLOSE-E).** *The partition-as-added-vertices grammar is not a fiat rule but a forced consequence
> of three owned M1 theorems applied to the owned fact that an extension adds vertices. Hence*
>
> > `AdmExt(X) ⟹ X is a partition-block family of the role material realized as pairwise-disjoint added
> > vertices ⟹ (with the owned canonical/characteristic restriction) |X| ∈ {2, 4} ⟹ X ∈ {D₂, ABCD}.`
>
> *The three named counter-objects (`Sub(Q₈)`, `Out(Q₈)`, the chain `{1,Z,Q₈}`) are excluded by the derived
> rule, computationally (script R4b.*). The window UPPER bound is sealed.*

The novelty is **one derivation**, not one assertion: the partition quantifier is obtained by *instantiating
three M1 schemata the corpus already owns and proves* on the extension-vertex material. Everything else is
computation on Q₈.

---

## 1. Owned pre-facts (verbatim, file:line, every quote re-read on disk this pass, read past ±10 lines)

Book paths: `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md` (= BOOK_00),
`01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` (= BOOK_01),
`01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` (= BOOK_03).

### P1 — Vertices ARE addressable record quanta (the typing of extension material)

- **BOOK_01:253** (§01.3): "The symbol `𝔮` is the **irreducible addressable record quantum**. The dyad closes
  only when the comparison produces a finite registration." The atomic unit of the record is an *addressable*
  quantum.
- **BOOK_01:1989** (§01.20 close): "The witness/basepoint `ω₀` gives the first **addressable** graph-birth
  shell." Vertices of the shell are the addressable positions.
- **BOOK_01:1911** (§01.21): "In the base zone the **address count is `D = 9`** (the defect shell `V₉`),
  giving `9` **distinguishable address positions by definition of the address**. The internal addressor …
  must visit those positions." — a vertex = one distinguishable address position, *by definition of the
  address*.
- **BOOK_01:836 / :862 / :67** (the TYPING anchor — the letters ARE states of the profinite support):
  "eight oriented terminal-role **states** `Ω8`" (§01.7.2 header :836, §01.8 :862); ":67" lists "`four
  terminal roles A,B,C,D`" among the "quotient **data on this profinite/condensed support**" `S_{D0}`. So the
  alphabet letters (the four roles / the eight signed states) are **states `x ∈ S_{D0}`** — exactly the type
  THE 01.4.0 (:325) quantifies over. This is the owned bridge that makes P2 apply to letters, not a transfer.

### P2 — M1 identity-of-indiscernibles (THEOREM): two things at the same address ARE one

- **BOOK_01:325** (§01.4, forcing, verbatim): "Suppose … `x≠y` yet `π_k(x)=π_k(y)` for all `k` … To keep
  `x≠y` one must therefore **adjoin an external label** — an index `ℓ(x)≠ℓ(y)` not produced by any
  finite-stage readout. That label is an **External Catalog of differences** … exactly the object M1
  forbids … Contradiction. **Hence `x=y`.** ∎" — if two putative letters are read out identically at every
  finite stage (same address, no other distinguishing readout), they are **equal**; distinctness needs an
  external catalog = ⊥M1.

### P3 — No-subaddress / no-hidden-marker (general obligation on the addressing)

- **BOOK_01:1574** (§01.20, obligation C3, verbatim): "**No-subaddress.** No new distinguishable sub-address
  of connectivity may be introduced inside a part, or the addresses `9/11/13` stop being minimal."
- **BOOK_01:1579** (the discharge, verbatim): "any within-part edge creates the distinguishable binary
  property … **not codable in the original addressing without an extra marker (an external distinguishability
  catalog)**." — introducing a distinction that the addressing cannot code requires an extra marker = external
  catalog = ⊥M1. This is stated as a **general** obligation on additions to the scene, not a per-instance remark.
- **BOOK_01:1616** (grammar 01.11C reference): "using a role-address as a flavour winding is a **scene pointer
  collision = hidden memory**." — two things claiming one address = pointer collision = hidden memory = ⊥M1.

### P4 — An extension ADDS VERTICES, as disjoint unions of the alphabet set (the instance grammar, verbatim)

- **BOOK_01:867** (§01.8): "`V₉ = Ω₈ + ω₀`." The nine vertices ARE the eight signed roles plus the witness.
- **BOOK_01:1541-1546** (§01.20): "`V₉ = Ω₈ ⊔ {ω₀}`, `|V₉| = 9`."
- **BOOK_01:1548-1554** (§01.20, verbatim): "The next two shell extensions are the only primitive unresolved
  capacities over the pointed shell … Therefore `V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ four terminal roles A,B,C,D`."
  — **the added vertices ARE the alphabet letters**: the two vertices of `V₁₁` are the dyad's two elements,
  the four vertices of `V₁₃` are the four roles. Disjoint union (`⊔`) at both sites.
- **BOOK_01:1530** (§01.20, verbatim): "The four roles are not a list to be chosen — they are forced as the
  minimal self-sufficient act of record … Fewer than four leaves the act without a distinguishable record, or
  **requires an external memory to hold the missing role. That is the catalog M1 forbids.**" — the alphabet's
  own completeness is already tied to M1's catalog-forbiddance *in print*.

### P5 — The M1 catalog schema itself, and the exogeneity test (the engine)

- **BOOK_00:380-398** (DEF-0.2.2, forcing-by-contradiction): "assume `¬X`; show `¬X` requires extra structure
  `θ` … `θ` affects distinguishable outcomes, hence is an exogenous parameter; that contradicts M1; therefore
  `X`." + **BOOK_00:398** (DEF 0.3.1 exogeneity test): "`θ` counts as exogenous iff it (1) is not derived
  inside the corpus, (2) affects a distinguishable result …, and (3) is not an unavoidable part of the
  distinguishability protocol."
- **BOOK_00:166**: "*Why 4 roles?* Fewer — the act leaves no distinguishable record, or **requires external
  memory**." + **BOOK_00:177**: "**hidden states and external memory backgrounds are strictly forbidden.**"

### P6 — The characteristic/canonical restriction (owned, for the size read-off)

- **BOOK_01:1616** (§01.20 THE-B, verbatim): "The **catalog-free (characteristic) subgroups** are exactly …;
  **every other subgroup … requires choosing an instance = a catalog.**" — the corpus EQUATES catalog-free
  with characteristic and uses it to prune non-canonical objects. (Cross-domain transfer flagged SELF-ATT-2.)

---

## 2. THE DERIVATION — the partition quantifier, forced (the ONE new step)

**Setup.** Let `R := Ω₈ ≅ Q₈` be the owned role group (BOOK_01:782, THEOREM). An admissible zone-extension
over the pointed shell `V₉` **adds vertices** (P4), and each added vertex is an **addressable record quantum
= one distinguishable address position** (P1). An extension **alphabet** `X` is the set of added letters; by
P4's instance grammar each letter is realized as an added vertex carrying role material. Write each letter as
the set of role-elements it occupies (its "address block").

**Step D1 — letters occupy addresses (owned typing).** By P1, an added vertex is an addressable position;
by P4 the added vertices ARE the alphabet letters. So each letter has an address footprint ⊆ the role
material. This is not a modelling choice: it is what the two extension definition sites *do* in print
(`V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ ABCD` — the union is OF the letters).

**Step D2 — no two letters may share an address (forced by P2 + P3).** Suppose two distinct letters `a ≠ b`
of `X` share an address position `p` (their footprints overlap: `p ∈ a ∩ b`). Two sub-cases, both ⊥M1:
- *(they are otherwise indistinguishable at `p`)* — then at address `p` the readout cannot separate `a` from
  `b`; to keep them distinct one must adjoin an external label `ℓ(a) ≠ ℓ(b)` — **exactly BOOK_01:325's
  External Catalog of differences** — ⊥M1, and by the theorem `a = b` (the two "letters" collapse to one,
  so `X` was not a family of distinct letters).
- *(they carry a further distinguishing marker at `p`, "which letter owns this shared position")* — that
  marker is a **new distinguishable sub-address inside the addressing that the addressing cannot itself code**
  — **exactly BOOK_01:1579's extra marker = external distinguishability catalog**, and BOOK_01:1616's pointer
  collision = hidden memory — ⊥M1.

Either horn is ⊥M1. Therefore **the letters of an admissible alphabet occupy pairwise-disjoint addresses.**

**Step D3 — the alphabet is a partition-block family (conclusion of D1+D2).** A set of nonempty,
pairwise-disjoint address-blocks of the role material IS a partition of their union. Hence:

> **DERIVED-RULE.** `AdmExt(X) ⟹ X is a partition of (a subset of) the role material, realized as
> pairwise-disjoint added vertices.`

**Nothing here is fed in.** D1 is P4's print grammar; D2 is P2 (a THEOREM) + P3 (a general obligation)
instantiated at "two letters share an address"; D3 is the definition of a partition. The quantifier the
missing-object spec demanded is exactly D3, and it is a *consequence*, not a premise.

**Step D4 — the three counter-objects fall to DERIVED-RULE (computed, script R4b.*):**
- **`Sub(Q₈)` (size 6, the escaped headline object).** The 6 subgroups, taken as letters, **pairwise share
  the identity element `1`** (every subgroup contains `1`). Computed `R4b.Sub_overlaps_at_identity = True`.
  So `Sub(Q₈)` is **not** a partition (two letters at address `1`) — excluded by D2. Excluded by the *rule*,
  not by size-fiat: `R4b.Sub_EXCLUDED = True`, `R4b.Sub_size6 = True`.
- **`Out(Q₈) ≅ S₃` (size 6).** Its elements are **automorphisms**, not role-material subsets — they are not
  addressable record quanta (fail D1's typing). Computed `R4b.Out_not_role_material = True`. The `Out`
  partition is of `Aut(Q₈)`, not of the role material — a different set entirely.
- **The chain `{1, Z, Q₈}` (size 3).** **Nested** (`{1} ⊂ Z ⊂ Q₈`), so its letters share addresses
  (`1 ∈` all three; the elements of `Z ⊂ Q₈`). Computed `R4b.chain_nested = True`,
  `R4b.chain_EXCLUDED = True`.

**Step D5 — the surviving sizes are `{2,4}` (partition + owned canonical restriction, script R4c/PC).**
Partition-hood alone does not fix the size (a size-3 partition of Q₈ exists abstractly — `NC2.size3_partition_exists`).
The size read-off needs the owned **canonical/characteristic** clause (P6, D.1 :1616): among Aut-invariant
partitions of the role material realized from characteristic data, the coset partitions of the characteristic
subgroups `{1, Z, Q₈}` have sizes `{8, 4, 1}` (script R4c.char_coset_sizes) — the proper nontrivial one is
`Q₈/Z` (size 4 = ABCD), and the center's own split `Z = {+1}⊔{−1}` gives the size-2 dyad (script
`R4c.Z_split_partition`). Both are Aut-invariant families (`NC2.ABCD_IS_canonical`, `NC2.Zsplit_IS_canonical`);
the abstract size-3 partition is NOT (`NC2.size3_not_canonical`) — so it is excluded by the canonical clause,
honestly a *second* owned clause, not by partition-hood. **Admissible sizes = `{2,4}`, exactly two**
(`R4c.admissible_sizes_2_4`, `PC.exactly_two_admissible`). No canonical size-6 partition exists
(`PC.no_canonical_size6_partition`): the Aut-orbits on Q₈-elements are `{1},{−1},{±i,±j,±k}` (sizes 1,1,6);
a canonical 6-block partition would have to split the transitive 6-orbit into invariant singletons — impossible.

**Step D6 — the tower and window upper bound (positive control, script PC).** `base = 9`; the two admissible
alphabets add `2` and `4` vertices → zone sizes `9, 11, 13` (`PC.tower_9_11_13`). No admissible alphabet of
size 6 (→ 15) or 3 (→ 12) survives. **The window UPPER bound `z₃ ≤ 13` is sealed.** Combined with GAP-W's
lower bound (row 545), the `[9,13]` capstone closes. `13` and the tower appear here for the FIRST time — never
as an input.

∎ (candidate)

---

## 3. The five construction routes (task item: "просеять руду" — all attempted, each landed)

| # | Route | Verdict | Where it lands in §2 |
|---|-------|---------|----------------------|
| **1** | **FLAGSHIP — M1 + addressability ⟹ partition** | **LANDS (the derivation).** Letters = addressable quanta (P1) + no shared address (P2 identity-of-indiscernibles + P3 no-subaddress/hidden-marker) ⟹ disjoint blocks ⟹ partition. Sub(Q₈) shares address `1` → the shared address IS the M1-forbidden catalog (D2 horn 2). Out = automorphisms → not addressable (D1 typing). Chain nested → shared addresses. | D1–D4 |
| **2** | **Role/coset grammar** | **LANDS as a corollary, not needed as a premise.** The four roles = the four **cosets of Z(Q₈)** (script Q3.*, S-5 of E-SYNTH; owned BOOK_01:830 abelianization). Cosets of a subgroup **partition** the group — so the owned alphabet ABCD is literally a partition, confirming DERIVED-RULE on the corpus's own first extension. "Extension letters are roles/acts of record" is verbatim-owned (BOOK_01:1530). But the *rule* does not depend on the coset reading — it depends on addressability (route 1); coset-hood is a fingerprint (§4 F-2). | D5, Q3.* |
| **3** | **Disjoint-union forcing** | **LANDS — and is the SAME step as D2.** `V₁₁ = V₉ ⊔ D₂` uses `⊔` (disjoint) in owned print (P4). Is disjointness *forced* or incidental? Forced: BOOK_01:325 (two vertices at one address ARE equal) makes `⊔` the ONLY admissible union of vertices — a non-disjoint "union" would have a shared vertex, which collapses by identity-of-indiscernibles or needs a hidden marker (P3). So `⊔` is not notation-choice; it is the M1-forced union. Overlapping alphabets (non-partitions) are excluded structurally. | D2 |
| **4** | **Size-from-partition** | **FAILED — this is where the closure dies (skeptic EoR-0/2/3).** Given partition-hood, sizes are NOT pinned. Pinning `{2,4}` needed a "canonical" clause I silently narrowed to "coset-partition-of-characteristic-subgroup" — NOT owned, and inconsistent (my kept size-2 dyad is not such a coset partition either). The genuinely canonical **Aut-orbit partition `X₃` (size 3 → z₃=12)** survives partition-hood AND Aut-invariance. The characteristic citation (:1616/:1618) is from the flavour-window `(ℤ/44)*`, wrong domain. **DEAD.** | §SKEPTIC-#1 |
| **5** | **Self-break (find a fifth object that breaks routes 1–4)** | **SUCCEEDED — the skeptic found it: `X₃`.** My own route-5 sweep looked only for *non-partition* addressable objects (found none — the Born-overlap `O_ij` hits BOOK_01:1962/BOOK_04:1246 are inner products, a different sense; the nested `9-11-13` at BOOK_03:908 is the tower). **But I aimed the self-break one level too low** (exactly the E-SYNTH failure mode): the breaking object is not a *non-partition* — it is a **canonical partition of a bad SIZE** (the Aut-orbit partition), which escapes route 4, not routes 1–3. The independent skeptic aimed correctly and found it. | §SKEPTIC-#1, R5 |

---

## 4. FINGERPRINTS (convergence noted, NOT summed as proof; trap-j respected)

- **F-1 (COUNT).** Two admissible alphabets + base = 3 zones = owned COUNT-3 (`D0-TOWER-STOP-NOEXT-001`).
- **F-2 (coset partition).** ABCD = cosets of Z, computed to partition Q₈ (Q3.cosetsZ_partition_Q8) — the
  owned first extension is *already* a DERIVED-RULE partition, so the rule is not tuned to exclude, it is
  satisfied by the corpus's own instances.
- **F-3 (selector no-go corollary).** DERIVED-RULE predicts zones canonical as objects but within-zone letters
  not individually selectable (the Aut-action on the `Q₈/Z` letters is the transitive `S₃` — Q2.C4_triple_transitive),
  which is exactly `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (row 549, LEAN_PROVED). A separately-paid
  no-go falls out as a corollary.
- **F-4 (the rule is falsifiable / Q₈-specific).** DERIVED-RULE is not a size template: dropping the rule
  READMITS Sub(Q₈) as a size-6 alphabet (`NC1.sub6_readmits_without_rule` = True), collapsing the whole GAP-E
  kill. So the rule is exactly the load-bearing datum, mutation-confirmed (§script MUT + external mutation test:
  drop the predicate → 6 checks fail, rc=1).

---

## 5. NAMED RISKS & PRE-REGISTERED ATTACK SURFACE (the smuggle hunt, aimed at myself)

- **SELF-ATT-1 (THE STRONGEST — is "addressable ⟹ partition" a real derivation or a gloss importing the
  conclusion?).** The whole closure rests on Step D2. The honest worry: does "letters are addressable quanta"
  ALREADY mean "letters are disjoint" (in which case D2 is a tautology dressed as a derivation, and the missing
  quantifier is *smuggled*)? **My defense:** D2 does NOT assume disjointness; it assumes only (i) letters are
  addressable (P1, owned) and (ii) two things at one address either collapse (P2, a THEOREM with a ∎) or need
  a marker (P3, a general obligation). Disjointness is the *output* of applying two owned M1 theorems to the
  hypothesis "two letters share an address." The load is carried by BOOK_01:325 and :1579, both owned and both
  proved *for vertices/addresses in general*, not coined here. **The typing bridge is OWNED, not assumed:**
  BOOK_01:325 (THE 01.4.0) quantifies over **states `x,y ∈ S_{D0}`** ("two states equal under every `π_k` are
  the same state"); and BOOK_01:836/:862/:67 name the alphabet letters exactly this — "eight oriented
  terminal-role **states** `Ω8`", "`four terminal roles A,B,C,D`" as "quotient data on this profinite/condensed
  support" `S_{D0}`. So an extension letter IS a state `x ∈ S_{D0}`, the very type :325 governs — the
  application of P2 to letters is a **matched typing**, not a transfer. **Residual (honestly retained):** the
  :1579 leg (within-part sub-address) is a narrower context than "any two states"; but D2 needs only ONE of its
  two horns, and horn 1 (the collapse `a=b` by :325) stands on the matched typing alone without :1579 — so :1579
  is a *reinforcing* second horn, not the load-bearer. The closure does not fall if a maintainer scopes :1579
  narrowly. **This is the exact point the independent skeptic attacks — verdict appended in §SKEPTIC-#1.**
- **SELF-ATT-2 (the :1616 characteristic transfer, inherited from E-SYNTH).** Step D5's size read-off uses
  ":1616 catalog-free = characteristic" outside the flavour-window section where it is printed. Owned at 3+
  sites (A.2 Inn-level, D.1 Aut-level, row-549 no-go) but a genuine cross-domain transfer. **Scope honesty:**
  the PARTITION conclusion (D1–D4, the counter-object exclusions) does NOT use :1616 — it uses only P1/P2/P3.
  Only the SIZE `{2,4}` read-off (D5) leans on :1616. So even if a maintainer rejects the :1616 transfer, the
  partition rule and the exclusion of Sub/Out/chain STAND; what weakens is only "sizes are exactly {2,4}" vs
  "sizes are the characteristic-coset sizes" (same numbers, different justification grade).
- **SELF-ATT-3 (D₂ = which ℤ₂?).** The size-2 alphabet's identity (center-split vs two-port role pair) is
  fork-open (E-SYNTH EoR-6). **Does not touch this closure:** DERIVED-RULE fixes that the size-2 alphabet is a
  2-block partition regardless of which ℤ₂; the fork is about *labeling*, not *partition-hood or size*.
- **SELF-ATT-4 (is DERIVED-RULE just the old "extensions come from the role group" begging-point recoated?).**
  No: the old gap was *provenance* (why role-group?). DERIVED-RULE is *grammar* (why partition?), and it is
  discharged by addressability (P1) + two M1 theorems (P2/P3) that hold for ANY added vertices, not by asserting
  role-group provenance. Provenance is separately owned (P4 print grammar: the extensions ARE role material).
- **SELF-ATT-5 (canonical clause smuggles the size).** Priced in D5 and NC2: "partition" alone does NOT give
  `{2,4}` (size-3 partition exists); the canonical clause is a SEPARATE owned datum, disclosed, not hidden.
- **SELF-ATT-6 (Out(Q₈) typing dodge).** "You excluded Out by fiat — calling automorphisms 'not addressable'."
  Defense: an automorphism is a *map* Q₈→Q₈, not an *element/coset* of the role material; the vertices/record
  quanta are the role states (P1, P4 — the letters of `V₁₁`/`V₁₃` are the dyad's elements / the four roles,
  which ARE elements/cosets). An automorphism is not among them. This is a typing consequence of P1+P4, not a
  fiat — but it IS the weakest of the three exclusions and is flagged for the skeptic.

**Reopening hooks carried:** (i) an owned extension letter shown to be a DIFFERENT type from :325/:1579
addresses (breaks D2 → assembly-grade); (ii) a maintainer ruling against the :1616 transfer (demotes the size
read-off only, not the partition rule); (iii) an owned non-partition addressable alphabet anywhere in the corpus
(route-5 residue — none found this pass).

---

## 6. What this memo does NOT do

- Does NOT mint. CLOSE-E is a candidate until the independent skeptic pass and `VERIFIED_CLOSURE_PROTOCOL.md`.
- Does NOT force the extension ORDER (rides on row 530 + `+2` parity, as E-SYNTH §ORDER).
- Does NOT edit any registry row / cert / built Lean file / `053040`.
- Does NOT re-derive the E-SYNTH computation layer (cross-referenced, reused: Q₈ subgroup lattice, Aut=24,
  characteristic chain, coset reading — all recomputed independently in the script's Q0–Q3 blocks).

---

## 7. Lean sketch (code block ONLY — not added to the tree)

```lean
-- DRAFT SKETCH ONLY. Documents the mintable package; do NOT add to 09_LEAN_FORMALIZATION.
namespace D0.Tower.PartitionAlphabet
-- reuse UQuat, uqmul, Q8 from D0.Foundation.Omega8Center
-- (1) letters as address-blocks; AdmExt X := PairwiseDisjoint blocks ∧ CanonicalFamily X
--     PairwiseDisjoint is the Lean image of D2 (owned P2 :325 + P3 :1579 discharge in prose)
-- (2) Sub(Q8) is NOT pairwise-disjoint: every subgroup contains 1  — by native_decide
theorem sub_not_partition : ¬ PairwiseDisjoint (subgroupsAsBlocks Q8) := by native_decide
-- (3) the chain {1,Z,Q8} is nested ⇒ not pairwise-disjoint  — by native_decide
theorem chain_not_partition : ¬ PairwiseDisjoint charChain := by native_decide
-- (4) admissible canonical partitioned alphabet sizes = [2,4]  — by native_decide
theorem admissible_sizes : admissibleSizes = [2,4] := by native_decide
-- (5) upper bound: no admissible alphabet of size 6 ⇒ z3 ≤ 13
theorem window_upper_bound : ∀ X, AdmExt X → 9 + X.card ≤ 13 := by decide
end D0.Tower.PartitionAlphabet
```

**Minting package (ONLY if the skeptic pass is survived — NOT performed here):** claim-ID candidate
`D0-GAP-E-PARTITION-ALPHABET-001`; Lean module as above; cert = `close_gap_e_check.py` promoted to `05_CERTS/vp_*`
with its negative controls; registry: new row + note-updates to rows 546 (WINDOW-DISSOLVE: upper bound
candidate-closed) and 547 (fork). Maintainer actions.

---

## §SKEPTIC-#1 — INDEPENDENT PASS (2026-07-06, ACCEPTED IN FULL, no defense)

**VERDICT: KILLED.** By §05.8.R standard (i) — a named second object — AND (ii) — a smuggled premise.

### The named second object (the kill)
`X₃ = {{+1}, {−1}, {±i,±j,±k}}` — the **Aut-orbit partition** of the role material. Verified independently
on disk (this pass, re-run): it is a partition (pairwise-disjoint, covers Q₈); it is **Aut-invariant** (its
three blocks are exactly the three Aut-orbits `{+1}, {−1}, {±i,±j,±k}`, sizes 1,1,6); its size is **3 → z₃ = 12**.
It passes D3 (partition) AND D5's stated "canonical/Aut-invariant" clause. **The window upper bound is not sealed.**
D5 and the script's `NC2` both asserted "no canonical size-3 partition exists" — FALSE, and false by cherry-pick:
`NC2` tested exactly one hand-built non-invariant size-3 partition (`part3`) and over-generalized. Full
enumeration returns canonical block-counts including 3.

### Errors of record (enumerated, no defense)
- **EoR-0 (FATAL — the kill):** D5's canonical clause does not exclude `X₃`; the "no canonical size-3/size-6"
  claim is false. *Fix:* banner + this section; §RESIDUE below states the true minimal missing lemma.
- **EoR-1 (the smuggle):** the original `close_gap_e_check.py:228` was `admissible_sizes = sorted({2,4})` — a
  hardcoded literal, the exact compute-first violation the discipline exists to catch. *Fix applied:* replaced
  by a genuine enumeration; but the deeper narrowing (next EoR) survived that fix, so the fix did not save the
  closure — it only exposed the narrowing.
- **EoR-2 (prose/script equivocation on "canonical"):** memo D5 prose licenses "Aut-invariant partitions"; the
  script silently narrows to "coset partitions of characteristic subgroups `{1,Z,Q₈}`" (sizes {8,4,1}). These
  are different objects: `X₃` is Aut-invariant (prose admits) but not a coset space (script excludes). Worse —
  my own kept size-2 center-split is ALSO not a coset partition of a characteristic subgroup, so the coset
  criterion cannot be applied consistently. *Fix:* accepted; the coset criterion is retracted as unowned.
- **EoR-3 (the :1616 citation domain):** the "catalog-free (characteristic)" quote is at BOOK_01:1618 (THE-B)
  and is about the flavour-window unit group `(ℤ/44)*`, NOT Q₈ role material. SELF-ATT-2's cross-domain flag is
  **fatal for D5**, not merely cautionary. *Fix:* accepted; D5's size read-off has no owned support.
- **EoR-4 (the :1579 scope):** C3 (BOOK_01:1574-1579) is a within-part *connectivity/edge* obligation on the
  ALREADY-FIXED partition, not a general "no two letters share an address" law. The memo overread "general."
  *Fix:* D2's :1579 leg demoted; D2 now rests only on the :325 horn (which the skeptic granted survives at
  assembly grade via the matched state-typing).

### What survives, and at what grade
- **D1–D4 (partition rule + exclusion of Sub(Q₈), Out(Q₈), nested chain):** SURVIVES at **assembly-grade
  owned-schema transfer**. The :325 state-typing (BOOK_01:836/:862/:67 name letters as states `x∈S_{D0}`) makes
  horn-1 of D2 a matched typing, not a bare transfer — the skeptic granted this. Sub(Q₈) (overlap at `1`) and
  the nested chain are correctly excluded by the partition rule; Out(Q₈) by the state-typing (weakest, but
  defensible). This is a real, reusable structure result — but a transfer, not a theorem.
- **D5 (size ⟹ {2,4}) and D6 (upper bound z₃ ≤ 13):** **DEAD.** `X₃` is a canonical size-3 survivor; z₃ = 12
  is admissible under every clause this memo owns; the "no size-3" sentence GAP-E needed is false as derived.

## §RESIDUE — the SHARPENED minimal missing lemma (what this kill bought)

This is the **FIFTH** independent confirmation GAP-E's completeness clause is open (R3 → E-b → dyad-power →
E-SYNTH → CLOSE-E). The partition rule (D1–D4) is now the first part of the missing object that IS derived; the
kill sharpens the *remaining* residue to a single precise question:

> **(MISSING — the block-shape clause.)** *An owned rule that admits the coset partition `Q₈/Z` (size 4) and
> the center-split `Z = {+1}⊔{−1}` (size 2) but FORBIDS the Aut-orbit partition `X₃` (size 3), WITHOUT fiat.*

**The computed separation (script R5/R6, full enumeration of ALL 4140 set-partitions of Q₈ filtered to the
Aut-invariant ones):** the canonical **proper** partitions **of Q₈** have block-counts `{2,3,4,5,7}` — and among
them the **UNIQUE uniform-block** one is size **4** (the ABCD cosets, blocks `2,2,2,2`). Tabulated:

| alphabet | partitions… | size | Aut-invariant | uniform blocks | canonical partition **of Q₈**? |
|----------|-------------|------|---------------|----------------|--------------------------------|
| `Q₈/Z` (ABCD) | …Q₈ | 4 | ✓ | ✓ (2,2,2,2) | ✓ (the unique uniform one) |
| `X₃` orbit | …Q₈ | **3** | ✓ | ✗ (1,1,6) | ✓ — **the killing survivor** |
| `D₂`/`Z`-split | …the **center Z**, not Q₈ | 2 | ✓ (family) | ✓ (1,1) | ✗ — **does not cover Q₈** |

**This is sharper — and firmer for the boundary — than a first "uniform blocks" guess.** Two computed facts:
1. A **uniform-block** clause over partitions **of Q₈** DOES exclude `X₃` (blocks 1,1,6 non-uniform) — good —
   but gives **only size {4}**, NOT `{2,4}`: it also **loses the size-2 dyad** (script `R6.uniform_clause_gives_only_4_not_2and4`,
   `PC.uniform_alone_loses_dyad`). So "uniform blocks" is necessary-but-not-sufficient.
2. The size-2 dyad is **not a partition of Q₈ at all** — it partitions the **center `Z`** (or the two-port
   dyad, a different universe). The canonical size-2 partitions *of Q₈* all have blocks `{1,7}` or `{2,6}` —
   non-uniform (script `R6.Zsplit_does_NOT_cover_Q8`, `R6.Zsplit_covers_center_Z`).

So the minimal missing lemma is a **two-part** clause, and neither part is owned as an alphabet rule:

> **(MISSING — the two-universe block-shape clause.)** An owned rule that (a) each extension alphabet is a
> **uniform-block** (equal-cardinality) partition — excluding the Aut-orbit partition `X₃` — AND (b) admits the
> **two owned universes** the alphabets live on (`Q₈` for ABCD, the center `Z`/two-port dyad for `D₂`), pinning
> the surviving sizes to `{2,4}`.

The nearest owned support for (a) is **C1 Exchangeability** (BOOK_01:1572): "No permutation inside a part may
change the physics … A part-internal exception would name a **privileged vertex** — an exogenous parameter —
violating M1." A non-uniform partition (`X₃`) has a distinguished size-6 block = a privileged sub-object.
**BUT** C1 is owned for *within-part permutations of scene-graph vertices* (`S₉×S₁₁×S₁₃`), NOT for *block-sizes
of an extension alphabet* — applying it here is the SAME typing transfer the skeptic killed on :1579. Part (b)
(the two-universe licence) has **no** owned support this pass. Owning either is a **sixth forge** and an
**OWNER DECISION**, not forged here.

> **GAP-E's completeness clause is OPEN.** The upper bound is NOT sealed: `z₃ = 12` (the Aut-orbit alphabet) is
> admissible under every clause this memo owns. The minimal missing lemma is the **two-universe uniform-block
> clause** above. What IS in hand: the partition rule (D1–D4), which kills the three ORIGINAL counter-objects.
> What is missing: the block-shape + universe clause that kills the NEW one (`X₃`).

Reopening/closing hook: if a maintainer rules C1 exchangeability licenses uniform-block-hood for alphabets AND
supplies the two-universe licence (or an independent owned "equal-capacity letters on the owned universes"
sentence is found), CLOSE-E's D5–D6 revive and GAP-E closes — the partition rule (D1–D4) is already derived.

> **[EoR — GAPE-1011 integration 2026-07-06]** [EoR 2026-07-06, 10th pass] X₃'s tower image (9,11,12) dies on the owned parity clause (odd step; B01:1903/B03 §03.23.6(3)/row 522) — the D-filter set omitted the tower-level parity filter; 'z₃ = 12 admissible' is retracted. Partition rule unaffected.
