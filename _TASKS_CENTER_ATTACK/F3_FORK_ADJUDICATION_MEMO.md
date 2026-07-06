# F3_FORK_ADJUDICATION — the zone-tower extension-layer fork (over-base vs consecutive vs nested)

**Status:** DRAFT candidate; adjudication finding, pre-skeptic. No registry row edited; no `.lean`
file added to the built tree; proposed Lean and proposed registry FORK row appear as code blocks
only. Candidate/DRAFT language throughout; nothing is "forced/closed" until the skeptic pass runs.

**Task:** adjudicate the three corpus readings of the zone tower `{9,11,13}` the way the corpus
adjudicated `8+1` vs `4+5` one layer down. Determine: owned identification (functor/iso) making
them ONE structure, OR genuine distinctness → canonical-per-purpose map + proposed FORK row + what
breaks if conflated (esp. M2's `1+1+3+4` and the tick carrier).

**Verdict (candidate):** **DISTINCTNESS.** No owned identification exists. Three readings, two
distinct owned structures (over-base *type* structure vs consecutive *numeral* ladder) plus one
narration-only structure (nested) that **structurally contradicts** the over-base types. They agree
only via the arithmetic coincidence `|Role| = 2·|Dyad|` (`4 = 2+2`). Canonical-per-purpose map +
proposed registry FORK row below. This mirrors the parent `8+1` vs `4+5` ruling exactly (trap i/d:
two objects until an owner proves them one), as the GAP-E memo's ATT-5 already prescribed.

---

## §0 The three readings, quoted verbatim (load-bearing citations)

**Reading A — OVER-BASE (Lean *types*).** `09_LEAN_FORMALIZATION/D0/Core/FiniteTypes.lean:14-16`
verbatim:

```lean
abbrev V9  := Sum Omega8 Witness
abbrev V11 := Sum V9 Dyad
abbrev V13 := Sum V9 Role
```

with `abbrev Dyad := Fin 2` (`:9`), `abbrev Role := Dyad × Dyad` (`:10`). Cardinalities are Lean
THEOREMS: `card_v11 : Fintype.card V11 = 11` (`:30-31`), `card_v13 : Fintype.card V13 = 13`
(`:33-34`). **Structure: `V11` and `V13` are two SIBLING extensions of the common base `V9`** —
`V11 = V9 ⊔ Dyad`, `V13 = V9 ⊔ Role`. As *types*, `V11 ⊄ V13` (there is no term-level inclusion
`V11 ↪ V13`; the only owned inclusions are `Sum.inl : V9 ↪ V11` and `Sum.inl : V9 ↪ V13`). This is
verified independent of narration by the parallel V12-variant file
`09_LEAN_FORMALIZATION/D0/Capacity.lean:15-16`: `V11V12 := Sum V9V12 D2`, `V13V12 := Sum V9V12 ABCD2`
(`:14` is the base `V9V12 := Option Omega8V12`) — same sibling-over-base pattern, same
`V11V12 ⊄ V13V12`.

**Reading B — CONSECUTIVE (Lean *numerals*).** `09_LEAN_FORMALIZATION/D0/Synthesis/CarrierForcing.lean:79-82`
verbatim:

```lean
/-- The `+2` address ladder from `(D_anchor=4, D_Σ=5)` is `[9, 11, 13]` — exactly 3 rungs
for the 3 forced zones (defect, memory, shell). -/
theorem address_ladder :
    (4 + 5 = 9) ∧ (9 + 2 = 11) ∧ (11 + 2 = 13) := by decide
```

**Structure: a linear ladder `9 →(+2) 11 →(+2) 13`** — 11 is reached FROM 9, and 13 is reached
FROM 11 (not from 9). This is *literal numeral arithmetic* (`by decide` on `Nat`); `D_anchor`/`D_Σ`
appear only in the docstring — as WINDOW_9_13_FORCING_MEMO.md:92 records verbatim: "**literal
numeral arithmetic**; `D_anchor`/`D_Σ` appear only in its docstring."

**Reading C — NESTED (BOOK_03 narration).** `01_BOOKS/BOOK_03_…SCENE_DYNAMICS.md:1064-1081` verbatim
(§03.23.7, heading `:1064` "Nested three-zone: Shell(13) ⊃ Torus(11) ⊃ Defect(9)", `:1066`
"Status: FORCED [^b03-46]"):

```text
Shell (13)  ⊃  Memory-torus (11)  ⊃  Defect (9)     (:1072)
R+r            R                     R-r             (:1073)
```

`:1076-1081`: "forced by closing the scale *from outside inward* … the only self-consistent
assignment is the relative nesting where the outer Closure shell (13) contains the memory zone (11)
which contains the defect core (9). This nesting is a structural reading of the aspect ratio."
Footnote `[^b03-46]` (`:1191`): "forcing: GOLDEN THE 3.12.B". **Structure: a totally-ordered
containment chain `Defect(9) ⊂ Torus(11) ⊂ Shell(13)`** — each zone contains the previous.

## §1 Is there an owned identification (functor/iso)?

**Finding: NO.** Exhaustive search of the built Lean tree found no functor, embedding, iso, or
inclusion relating the three readings into one structure.

- **No `V11 ↪ V13`.** `grep` over `09_LEAN_FORMALIZATION/D0/` for every file mentioning `V11`/`V13`
  (`FiniteTypes`, `CapacityChain`, `Capacity`, `Phase`, `PhaseTower*`, `Xi5TorusDefect`,
  `YukawaShellOverlapMatrix`, `SceneCenterSpacetimeConvergence`, `AlphaProfiniteSpectralTower`,
  `ClaimMap`) yields **no** `Embedding`, no `Sum.inl : V11 → V13`, no `⊆`/`⊂` relation between the
  zone types. `CapacityChain.lean:5-11` (`capacity_chain_cards`) bundles the three cardinalities but
  asserts NO map between the carriers.
- **The only owned bundling is numeric.** `CarrierForcing.carrier_full_forcing` (`:108-117`) and
  `capacity_chain_cards` conjoin `card`-facts; a conjunction of cardinalities is NOT an
  identification of structures (two objects of the same finite cardinality are not thereby the same
  object — trap d).
- **The corpus itself denies the identification, twice, verbatim.** GAP_E_COMPLETENESS_MEMO.md:18:
  "They agree numerically **only because** `|ABCD| = 2·|D₂|` (4 = 2+2 = 2×2; script §I). **No owned
  statement identifies them** (trap i/d: two objects until proven one)." And
  GAP_E_COMPLETENESS_MEMO.md:123: "F3 fork confirmed REAL (`FiniteTypes.lean:15-16` Sum-types vs
  `CarrierForcing.lean:81-82` `address_ladder`, plus BOOK_03:1064 nesting `Shell(13)⊃Torus(11)⊃
  Defect(9)` structurally contradicting the Sum types — agree only via `4=2+2`; **corpus must
  adjudicate**)."

So the honest state is exactly the parent-fork state one layer down (`8+1` vs `4+5`): numerically
convergent, structurally unidentified. **This memo does NOT manufacture an identification** — none
is owned and (§2) one of the pairs is not merely unidentified but mutually contradictory.

## §2 The structural contradiction: over-base types vs nested narration

The three readings do **not** stand in a symmetric three-way disagreement. There are two *different*
kinds of relation:

**(a) A over-base vs B consecutive — DISTINCT but COMPATIBLE (not contradictory).** Both are
Lean-owned; they disagree about *where 13 attaches*, not about set-membership.
- Over-base: `V13 = V9 ⊔ Role`. 13's new part (`Role`, 4 elements) attaches to `V9` (the 9-base),
  in parallel with 11's new part (`Dyad`, 2 elements). The two extensions are siblings; the pair
  `(11-part, 13-part)` = `(Dyad, Role)` = `(2, 4)` **over the same base 9**.
- Consecutive: `13 = 11 + 2`. 13's increment (`+2`) attaches to `11`, and 11's increment (`+2`)
  attaches to `9`. The increments are `(+2, +2)` in series.
- These reconcile **only** through `|Role| = 4 = 2 + 2 = 2·|Dyad|`: the over-base 13-jump of `+4`
  equals two consecutive `+2` steps. That is an arithmetic coincidence of the cardinals, not a
  structural identity (a 4-element set is not canonically two glued 2-element steps). Verbatim owner:
  GAP_E_COMPLETENESS_MEMO.md:18 (quoted §1). WINDOW_9_13_FORCING_MEMO.md:129 owns the over-base side
  as "**D1. Capacity route (Lean-typed)**"; :127-137 owns the consecutive/`+2` side as the ladder.
  So A and B are two Lean-owned *channels* whose agreement is computed, not forced — same status as
  G-CAP vs G-STEP (GAP_E ATT-5, `:105`).

**(b) A over-base vs C nested — STRUCTURALLY CONTRADICTORY.** This is the sharp finding.
- Over-base makes `V11` and `V13` **siblings** of `V9`: `V9 ↪ V11` and `V9 ↪ V13`, but there is
  **no** `V11 ↪ V13`. In the type reading, `V11` is *not* a subobject of `V13`.
- Nested (C) asserts the **opposite** relation: `Torus(11) ⊂ Shell(13)` — 11 IS a subobject of 13
  (`BOOK_03:1078` "the outer Closure shell (13) **contains** the memory zone (11)").
- These cannot both be the literal structure of one object: over-base says `11 ⊄ 13`; nested says
  `11 ⊂ 13`. GAP_E_COMPLETENESS_MEMO.md:123 states exactly this verbatim: nesting "**structurally
  contradicting the Sum types**". The contradiction is real at the *structural* (membership) level,
  even though all three agree at the *cardinal* level (`9 < 11 < 13`).

**Reading the contradiction away is NOT available for free.** One could try to rescue C by reading
"⊃" as radius-ordering (R+r ⊃ R ⊃ R−r is a *geometric* nesting of shells in a metric picture, per
`:1073` "R+r / R / R−r"), i.e. as an order on *radii* rather than an inclusion of *vertex sets*.
Under that charitable reading C is not a claim about `Sum` types at all — it is a claim about a
metric embedding of three concentric shells, which the type layer neither owns nor forbids. But
**the corpus text itself uses set-containment language** ("contains the memory zone", `⊃`), and no
owned map turns the radius order into a vertex-set inclusion. So the charitable reading is a
*candidate repair*, not an owned fact; until an owner supplies the radius→vertex functor, C stands
as narration that contradicts the over-base types as written. (Flagged for the skeptic, §6 ATT-C.)

## §3 Canonical-per-purpose map

Since no identification is owned, canonicity is **per consumer**, assigned by which structure that
consumer actually reads. Rule (inherited from GAP_E ATT-5, `:105`): a consumer picks ONE reading and
cross-cites the others; presenting them as "one tower" requires an identification owner first.

| Purpose / consumer | Canonical reading | Why (the fact it consumes) | Owner citation |
|---|---|---|---|
| **Carrier types / any per-vertex structure** (M2 tick carrier, `1+1+3+4` block decomposition, membership per-slot values) | **A over-base** | needs the actual *type* `V9`/`V11`/`V13` and its `Sum.inl` base, not numerals | `FiniteTypes.lean:14-16`; M2 `:159` "identity on 11/13" |
| **Address/window forcing** (WINDOW_9_13, centre `L₅=11`, the `+2`-minimality no-skip clause) | **B consecutive** | needs the `+2` step structure to run the orientation-parity ⊥-proof and the no-skip clause | `CarrierForcing.address_ladder:81-82`; WINDOW `:127-137` |
| **Cardinality-only facts** (`|V|=33`, `|E|=359`, `card`-chain) | **A and B agree; either** | consumes only `card`, on which A and B are equal theorems | `CapacityChain.lean:5-11`; `CarrierForcing.vertex_count_33 :69-70` |
| **Geometric shell picture** (radii `R±r`, aspect ratio, ξ₅ torus/defect) | **C nested — as a SEPARATE metric object**, cross-cited, NOT identified with A's types | radius ordering; owns no vertex-set inclusion | `BOOK_03:1064-1081`; `Xi5TorusDefect.lean` |

**Key ruling:** the *type* reading (A) is canonical for every per-vertex/carrier consumer, because
those consumers dereference the carrier type, and only A supplies a type. The *numeral* ladder (B) is
canonical for address/window forcing, because that forcing runs on the `+2` increment structure. The
nested reading (C) is canonical **only** for the metric/geometric shell picture and must be carried
as a distinct object cross-cited to A — never substituted for A's types (it contradicts them, §2b).

## §4 What breaks if conflated (M2 `1+1+3+4`, tick carrier, membership, GAP-E)

**M2's `1+1+3+4` does NOT depend on the fork — it lives entirely inside zone-9.** This is the
decisive check, and it comes out clean. M2_PHASE_LABELING_MEMO.md:149-150 verbatim: the new content
is "(i) the extension to the POINTED shell — `ℂ^{V₉} = ℂω₀ ⊕ (E₀ ⊕ E₃ ⊕ E₄)`, dims **1+1+3+4**".
The `1+1+3+4 = 9` decomposition is a representation-theoretic split of `ℂ^{V₉}` (the zone-9 carrier)
under the Q₈/`G_res` action — it never touches `V11` or `V13`. So the fork (which is entirely about
*how 11 and 13 attach to 9*) cannot perturb it. Confirmation that M2 treats 11/13 as inert:
- M2 `:159` verbatim: owned carriers are "`U = diag(zone-9 values from the canonical system;
  **identity on 11/13**)`". The tick carrier is a zone-9 diagonal padded by the identity on 11 and 13.
- M2 `:197` verbatim: M2-membership is "**NOT fed**, twice over". The zone-11/13 emptiness it turns
  on is X3 — defined at M2 `:70` ("**(X3) Zones 11/13.** NOTHING owned labels vertices within V₁₁ or
  V₁₃") and re-affirmed at M2 `:275` ("zone-11/13 emptiness (X3)"). Zones 11 and 13 "own nothing
  per-vertex" (M2 `:191`).

**Therefore the tick carrier does NOT depend on which reading of 11/13 is canonical** — it depends
only that 11 and 13 are *some* 2 and 4 extra slots on which the carrier acts as identity, which BOTH
A (as `Sum.inr` summands `Dyad`, `Role`) and B (as `+2`, `+2` increments) supply. The spectral
fingerprint M2 computes — `‖PUQ‖²_F = 80/81`, ratio `−1/9` (M2 `:161-167`) — is a zone-9 quantity;
it is fork-invariant. **No M2 result breaks under either A or B.** (This is a *positive* robustness
finding, not a fit forced onto the data.)

**What WOULD break if C (nested) were conflated INTO A (types) as an identity:**
- Any consumer that dereferences `V13` expecting `V11` to be a *subtype* (`V11 ↪ V13`) would type-error
  in Lean: `FiniteTypes.lean` provides no such inclusion, and providing one would *contradict*
  `V13 := Sum V9 Role` (whose only injections are from `V9` and from `Role`). So a memo that wrote
  "zone-11 ⊂ zone-13" as a *type* fact would be importing a map the corpus does not own and the types
  forbid — an M1-style external-catalog import. GAP_E ATT-5 (`:105`) is exactly the guard against this.
- Membership/shell-rule consumers (SHELL_MEMBERSHIP, SHELL_RULE_R): these read the *radius* picture
  (`SHELL_MEMBERSHIP_PREREG_V2.md:12` "13=terminal shell … 3-shell radii (1,(a+1)/2,a)") — i.e. they
  legitimately consume C, but as the *metric* object, cross-cited, NOT as A's vertex-set inclusion.
  They are safe **as long as they do not silently promote the radius nesting to a vertex-set
  inclusion of the `Sum` types.**

**What breaks in GAP-E / WINDOW if A and B are conflated (the milder, already-flagged hazard):**
- GAP_E_COMPLETENESS_MEMO.md:16-18 splits the missing-object spec by reading: under over-base the gap
  is "a *capacity-list completeness clause*"; under consecutive it is "a *no-skip clause*." These are
  DIFFERENT missing objects. Conflating A and B would collapse two distinct open joints (GAP-E's
  `{D₂,ABCD}` completeness vs the `+2` no-skip minimality) into one, hiding a real gap. WINDOW `:304`
  (ATT-2) already rules: "v2 must consume ONLY the `8+1` chain and cross-cite `4+5` … presenting them
  as 'two independent channels to 9' would need an identification owner first (trap d)."
- So conflation does not produce a *wrong number* (they agree on `9,11,13`), but it produces a **false
  sense of closure**: it would report one guarded joint where the corpus honestly has two narrated
  joints (capacity-completeness AND no-skip). That is the exact over-claim the D0 discipline forbids.

## §5 Proposed registry FORK row (candidate — NOT applied)

Proposed addition to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (a FORK/status row; **this
memo does NOT edit the CSV** — the row is a candidate for the registry owner to apply). Format mirrors
the existing desync/fork rows.

```csv
claim_id,status,lean_ref,note
D0-ZONE-TOWER-READING-FORK-001,FORK-OPEN,"FiniteTypes.lean:14-16; CarrierForcing.lean:79-82; BOOK_03:1064-1081","F3: the zone tower {9,11,13} has THREE corpus readings — (A) over-base TYPES V11:=Sum V9 Dyad, V13:=Sum V9 Role (siblings of V9; V11 NOT subtype of V13); (B) consecutive NUMERAL ladder 9->+2->11->+2->13 (address_ladder); (C) nested narration Defect(9) subset Torus(11) subset Shell(13) (BOOK_03 03.23.7). NO owned identification. A and B are DISTINCT-but-compatible (agree only via |Role|=4=2+2=2|Dyad|). C STRUCTURALLY CONTRADICTS A (C asserts 11 subset 13; A gives V11 not-subtype-of V13). Canonical-per-purpose: A for carrier/per-vertex/M2/1+1+3+4; B for address/window/+2 forcing; C for the METRIC shell picture only, cross-cited never identified with A. Adjudication: F3_FORK_ADJUDICATION_MEMO.md. Any closure memo MUST pick one reading and cross-cite (GAP_E ATT-5)."
```

**Consumer-safety note for the registry (candidate):** M2's `1+1+3+4` and tick carrier are
**fork-invariant** (zone-9-internal; 11/13 enter only as identity-padding); this fork does NOT block
M2. It DOES block any future claim that writes "zone-11 ⊂ zone-13" as a *type/vertex-set* fact
(forbidden by the `Sum` types) and any memo that reports GAP-E as single-guarded (it is
two-guarded: capacity-completeness AND `+2` no-skip).

## §6 Pre-registered attack surface (for the skeptic)

- **ATT-A (charitable-radius rescue of C).** Could C be read as a metric/radius ordering (`R+r > R >
  R−r`) that is *compatible* with A rather than contradictory? If an owner supplies a radius→vertex
  functor, the §2b contradiction dissolves and C becomes a metric refinement of A. **Status:** no such
  functor is owned; the corpus text uses set-containment words ("contains"). So the contradiction
  stands as-written, but the rescue is a legitimate candidate an owner could mint. This memo does not
  claim C is *permanently* contradictory — only that it contradicts A *as currently written*.
- **ATT-B (is "distinctness" itself over-claimed?).** Have I proved A and B are NOT identifiable, or
  only failed to find the identification? Honest answer: the latter for *impossibility*, the former
  for *ownership*. The claim is "no OWNED identification" (verified by grep + the corpus's own trap-i/d
  statements), NOT "no identification is POSSIBLE." An owner could still construct one (e.g. a functor
  sending the `+2,+2` series to the `Dyad,Role` siblings via `Role ≅ Dyad ⊕ Dyad` = `Fin 2 × Fin 2`
  as `Fin 2 ⊕ Fin 2`? — but there is **no CANONICAL / structure-preserving** iso `Role ≅ Dyad ⊕ Dyad`.
  As *bare types* they ARE isomorphic — any two 4-element types are (`Fin 2 × Fin 2 ≃ Fin 2 ⊕ Fin 2`
  holds up to *some* bijection; both are `Fin 4`). The load-bearing point is that no such bijection is
  the *identity of structure*: it exists only by a non-canonical relabeling and does not respect the
  product-vs-coproduct data — `Role = Dyad × Dyad` (a **product**, two independent Fin-2 factors) is
  not the **coproduct** `Dyad ⊕ Dyad` (two disjoint Fin-2 copies). So the arithmetic `4=2+2` does not
  lift to a *canonical* type iso `Role ≅ Dyad ⊕ Dyad` — reinforcing distinctness. Flag for
  skeptic to break.
- **ATT-C (M2 independence — did I check the right thing?).** I claim `1+1+3+4` and the tick carrier
  are fork-invariant because they are zone-9-internal (`ℂ^{V₉}`, M2 `:149-150`, `:159` "identity on
  11/13"). Skeptic should verify no M2 sub-result *silently* reads an `11⊂13` inclusion — e.g. the
  cross-zone CKM lane (M2 `:190-192`) needs "cross-zone up/down basis carriers B_up/B_down". If any
  such carrier assumes `V11 ↪ V13`, M2 is NOT fork-invariant there. Current read: M2 `:191` says zones
  11/13 "own nothing per-vertex" and the CKM lane is explicitly NOT-fed, so no inclusion is consumed —
  but this is the sharpest place the invariance could fail.
- **ATT-D (registry-status honesty).** FORK-OPEN is proposed, not FORK-CLOSED: the memo *adjudicates*
  (distinctness + canonical-per-purpose map) but does NOT close the fork by minting an identification.
  If the skeptic judges an identification owner is cheaply available (ATT-B rescue fails to hold), the
  status should stay FORK-OPEN; if the ATT-A radius functor is minted, it could move to
  IDENTIFIED-METRIC. Neither is claimed here.

**Outcome honesty:** this is a DISTINCTNESS finding with a canonical-per-purpose map and a proposed
FORK-OPEN row — a valid, non-forced outcome. No fit was manufactured; the one place a fit would have
mattered (M2's `1+1+3+4`) turned out fork-*invariant*, so no reading needed to be privileged there.


---

## §7 Skeptic #1 verdict + repair log (accepted in full)

**Verdict: WOUNDED** — adjudication substance survives; a systematic Reading-C citation
misattribution (integrity-grade, repairable) plus four smaller citation/wording defects blocked
acceptance until repaired. Accepted in full, no defense. Status stays **FORK-OPEN** post-repair.

**Errors of record (EoR):**

- **EoR-1 (integrity-grade, strongest finding) — SYSTEMATIC READING-C CITATION MISATTRIBUTION.**
  Every §0 line-number for Reading C (the nested/BOOK_03 reading, on which the §2b structural
  contradiction — the memo's sharpest finding — entirely depends) pointed 5–13 lines too high; the
  actual content sits further down in
  `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md`. Verified true locations by
  `awk`-printed line numbers:
  - heading "### 03.23.7 Nested three-zone: Shell(13) ⊃ Torus(11) ⊃ Defect(9)" → **:1064** (memo
    said :1062; :1062 actually reads "06.37 for the `phi^5 = 11 + xi5` split)").
  - "Status: FORCED [^b03-46]" → **:1066** (memo said :1064).
  - code block: `Shell (13) ⊃ Memory-torus (11) ⊃ Defect (9)` → **:1072**, `R+r R R−r` → **:1073**
    (memo said :1067 for the R+r line; :1067 is a blank line).
  - prose "forced by closing the scale *from outside inward* … the only self-consistent assignment
    is the relative nesting …" → **:1076-1081** (memo said :1069-1073).
  - "the outer Closure shell (13) contains the memory zone (11)" (the §2b back-reference) → **:1078**
    (memo said :1063; :1063 is a BLANK LINE).
  - §0 range header → **:1064-1081** (memo said :1062-1073).
  - Footnote `[^b03-46]` at :1191 ("forcing: GOLDEN THE 3.12.B") was the ONE Reading-C citation
    already correct.
  Quoted WORDING was faithful throughout (grep-confirmed: no fabrication, no opposite-meaning), so
  this is **misattribution, not a phantom citation** — but given the corpus's phantom-citation
  quarantine precedent and that a skeptic checking file:line lands on blank lines, it failed the
  VERBATIM CITATION AUDIT gate and blocked acceptance until repaired. Seed traced to
  GAP_E_COMPLETENESS_MEMO.md:123 (cites "BOOK_03:1064" — correct for the heading), which the memo
  then shifted further wrong. **Repaired** in §0 (heading/Status/code-block/prose/range-header),
  §2 (R+r → :1073), §2b (contains → :1078), §3 (table lean_ref → :1064-1081), §5 (proposed registry
  row lean_ref → :1064-1081). The GAP_E quote at §1:91 ("BOOK_03:1064 nesting") was left verbatim —
  it faithfully reproduces GAP_E:123 and :1064 is the correct heading line.

- **EoR-2 (citation-stitch, secondary) — M2 §4 two-fragments-as-one-quote.** The memo presented
  `M2 :197-199 verbatim: "NOT fed, twice over … zone-11/13 emptiness (X3)"` as one contiguous quote,
  but "NOT fed, twice over" is at **M2:197** while "zone-11/13 emptiness (X3)" is at **M2:275** (and
  X3 is defined at **M2:70**: "**(X3) Zones 11/13.** NOTHING owned labels vertices within V₁₁ or
  V₁₃"). **Repaired** into three correctly-located citations (:197 / :70 / :275).

- **EoR-3 (over-tight range, low severity) — Capacity.lean cited :14-16.** The quoted
  `V11V12 := Sum V9V12 D2`, `V13V12 := Sum V9V12 ABCD2` live at **:15-16**; `:14` is the base
  `V9V12 := Option Omega8V12` (not a sibling). **Repaired** to `:15-16` with a parenthetical noting
  :14 is the base — aligning to the FiniteTypes citation style. (FiniteTypes.lean:14-16 is correct
  as-is: its :14 is `V9 := Sum Omega8 Witness`, part of the three-line quoted block.)

- **EoR-4 (wording over-statement) — ATT-B "Fin 2 × Fin 2 ≇ Fin 2 ⊕ Fin 2 as the SAME 4-element
  set".** As *bare types* they ARE isomorphic (any two 4-element types are; both are `Fin 4` up to
  some bijection). The load-bearing statement is "**no CANONICAL / structure-preserving iso**
  `Role ≅ Dyad ⊕ Dyad`" — the bijection exists only by non-canonical relabeling and does not respect
  the product-vs-coproduct data (`Role = Dyad × Dyad` is a product, not the coproduct
  `Dyad ⊕ Dyad`). Substance (product ≠ coproduct, distinctness reinforced) was fine; **repaired** the
  wording only.

**Re-verification of the load-bearing changed text (only the changed claims re-checked):**
- **No owned `V11 ↪ V13`** — independent grep of the built `.lake` tree
  (`09_LEAN_FORMALIZATION/.lake/`) plus all `.lean` source: **empty** for any
  Embedding/`Sum.inl`/`↪`/`⊆`/`⊂` between V11 and V13. §2b contradiction survives.
- **GAP_E 4=2+2 two-guard split** — re-ran `gap_e_completeness_check.py`: **27/27 PASS, rc=0**;
  verdict prints "missing object = owned type-identity/enumeration clause **OR** owned +2-no-skip
  clause; EITHER pins (9,11,13) uniquely." Two-guard split intact.
- **CKM lane fork-invariance** — M2:190-192 verified NOT-fed ("cross-zone up/down basis carriers
  B_up/B_down; zones 11/13 own nothing per-vertex … a value-freedom, not a label-freedom"), so no
  `V11 ↪ V13` inclusion is consumed. M2 fork-invariance (ATT-C) holds.
- **product ≠ coproduct** — sound (`Role = Dyad × Dyad` at FiniteTypes.lean:10; the coproduct
  `Dyad ⊕ Dyad` is a distinct type). ATT-B distinctness reinforced.
- **CarrierForcing.lean:79-82 address_ladder** — verified verbatim (Reading B unchanged, was
  already correct).

**Residual after repair:**

- **Verdict stays FORK-OPEN** (not FORK-CLOSED). The adjudication substance survives skeptic: no
  owned identification, C structurally contradicts A at the membership level, A/B distinct-but-
  compatible via `4=2+2`, M2 fork-invariant. Once citations are truthful the proposed registry row
  does not over-claim. No registry CSV edit and no built `.lean` edit were made — the row and Lean
  drafts remain proposals in this memo only.
- **Open (mint-ready hooks, unchanged by this pass):**
  - **ATT-A radius→vertex functor** — if an owner mints a `radius → vertex-set` functor turning the
    metric shell order (`R+r ⊃ R ⊃ R−r`) into a vertex-set inclusion, C's §2b contradiction with A
    dissolves and C becomes a metric refinement of A; status could move to IDENTIFIED-METRIC. Not
    owned today.
  - **A/B identification owner** — an owner could still construct a (non-canonical) `Role ≅ Dyad ⊕
    Dyad`-based functor; distinctness is "no OWNED identification," not "no identification POSSIBLE."
    The canonical-per-purpose map holds until such an owner appears.
- **Mint-or-motion-ready:** the proposed FORK-OPEN registry row
  (`D0-ZONE-TOWER-READING-FORK-001`) is now citation-clean and ready to be handed to the registry
  owner for application (motion, not mint — it records an open fork, it does not close one). The
  consumer-safety note (M2 fork-invariant; blocks any future "zone-11 ⊂ zone-13" type-fact and any
  single-guarded GAP-E report) travels with it.
