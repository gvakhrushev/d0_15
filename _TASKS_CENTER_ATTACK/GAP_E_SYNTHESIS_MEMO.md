# GAP_E_SYNTHESIS — the extension alphabet IS the canonical-subquotient list of the owned role group Q₈: a positive closure candidate for GAP-E (DRAFT — **KILLED AS CLOSURE**, see banner; computation layer survives)

> ## ⛔ VERDICT: **KILLED-AS-CLOSURE** (Skeptic #1, independent pass, 2026-07-05 — ACCEPTED IN FULL, no defense)
>
> **E-SYNTH does NOT close GAP-E.** The forcing trichotomy (§FORCING) is **not total**: it quantified rival candidates over Aut-invariant **element-subsets** of Q₈ (script SSJ) while its own survivor list contains a **non-subset** object (`Q₈/Z`, a set of cosets) — a frame-level instance of trap (f). Once the candidate space is widened to what the survivors themselves inhabit (canonical role-**derived** objects), THREE named counter-objects escape all four prongs:
>
> 1. **`Sub(Q₈)` — the subgroup family, size 6.** Canonical (Aut-invariant as a family), role-derived, and closed **by the owned Dedekind/Hamiltonian property itself** (§01.7.1A — every subgroup normal; the family is intact under meet/join). It realizes a catalog-free size-6 role-derived object, i.e. a `z₃ = 15` candidate — **the headline kill (a) ("no size-6 object in the role algebra AT ALL") is FALSIFIED as stated.** Only the **subquotient-scoped** claim survives (no size-6 SUBQUOTIENT — that stays computed and true).
> 2. **`Out(Q₈) ≅ S₃` — size 6.** A second canonical role-derived size-6 object.
> 3. **The characteristic chain `{1, Z, Q₈}` — size 3.** A canonical role-derived size-3 object (a nested family, escaping the Lagrange scope the same way).
>
> Further wounds (all accepted): the **prong-4 CASE-2 use is a fourth-zone docstring transferred to a third zone** (assembly-grade, the class the completeness memo's skeptic tagged E-GE-3) — the schema-transfer residue is **≥ 2 transfers, not 1** as §BEGGING-POINT(3) priced it; prong-1's inventory was cited as "skeptic-confirmed" — **error of record** (the completeness memo's skeptic did not confirm exhaustiveness of that inventory); the **`D₂ = Z(Q₈)` identification is WOUNDED** — an owned rival reading exists (the two-port dyad `C₊/D₋`, i.e. the role-pair reading, BOOK_01:854/:1523), and on that face-value reading the memo's OWN computation K2 (S₃ transitive on `{B,C,D}` ⇒ the pair `{C,D}` is not Aut-invariant) makes **prong 2 kill the corpus's own first extension** — the biconditional of Claim E-SYNTH fails right-to-left.
>
> **What SURVIVES (computation layer — arithmetically intact, kill-controls added to the script):** the canonical-layer computation (characteristic subgroups of Q₈ = `{1,Z,Q₈}`; proper nontrivial characteristic subquotients = exactly `{ℤ₂, V₄}`, sizes `{2,4}`); the subquotient-order set `{1,2,4,8}` (no size-6 **subquotient**); Out(Q₈) ≅ S₃ transitive on the C₄-triple; the census (Q₈ uniquely clean among the five order-8 groups — the F-4 fingerprint); the no-size-prune property of the generator (the dyad-power TELL is absent). These are real, computed, reusable — as **structure results**, not as a GAP-E closure.
>
> **Honest landing:** GAP-E's completeness clause **stays OPEN** — this is its **FOURTH independent confirmation** (R3 underdetermination; E-b forge; dyad-power; E-SYNTH). The missing object is **SHARPENED** by this kill: what is missing is no longer "a generator" but the **alphabet-grammar clause** — the owned rule saying *which canonical role-objects are extension ALPHABETS*: letters must be **states realized as vertices** (elements or cosets — blocks of a partition of the role material), not derived families (subgroups, automorphism classes, nested chains). See §SKEPTIC-#1 and §OWNERSHIP-CHECK at the foot. **No closure language anywhere in this memo is operative.**

**Status:** DRAFT — **closure headline KILLED by Skeptic #1, accepted in full** (verdict + repair log §SKEPTIC-#1, ownership check §OWNERSHIP-CHECK, both at foot). Retained value: computation layer + the sharpened missing-object spec. NO registry row edited; NO `.lean` added to the built tree; NO edit to `CLAIM_TO_LEAN_MAP.csv` / `theory_status_map.csv` / any `053040` row / `LEAN_ASSUMPTION_LEDGER`. Lean material below is a code-block sketch only. Companion can-fail script: `_TASKS_CENTER_ATTACK/gap_e_synthesis_check.py` — **71/71 PASS, rc=0, VERDICT: KILLED-AS-CLOSURE** (65 structure checks SSA-SSM + 6 Skeptic-#1 kill-controls SSN confirming the counter-objects; count printed by the script's own counter, not hand-tallied; exact integer arithmetic only; scan bound declared `z₃ ≤ 21`; census bound declared = ALL five groups of order 8).
**Pre-flight (2026-07-05):** `preflight.sh GAP-E Q8 subquotient characteristic extension ABCD V15` — no existing row owns the exhaustiveness clause `∀X (AdmExt(X) → |X| ∈ {2,4})`. Cross-referenced owners (cited, never duplicated): D0-OMEGA8-CENTER-001 (row 8, CORE-FORMALIZED), D0-Q8-DEDEKIND-MINIMALITY-001 (row 207, CORE-FORMALIZED), D0-Z2-SPINOR-COVER-001 (row 213, CORE-FORMALIZED), D0-TOWER-STOP-NOEXT-001 (row 257, CORE-FORMALIZED), D0-SCENE-TRIPLE-UNIQUE-001 (row 530, CORE-FORMALIZED), D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 (row 549, NO-GO), frontier rows 545/546/547 (GAP-W / WINDOW-DISSOLVE / READING-FORK, all OPEN).
**Parents (cross-referenced, NOT re-litigated):**
- `GAP_E_COMPLETENESS_MEMO.md` (R3 two-route spec; this memo executes route **E-a**, the capacity/over-base fork, and supplies the type-identity predicate its §III dilemma demanded);
- `GAP_E_EB_FORGE_MEMO.md` (owns "13 is a cardinality, not a maximum"; this memo supplies the maximality);
- `GAP_E_DYAD_POWER_MEMO.md` (killed the `2^k`-generator candidate; its §RES names the exact missing sentence — this memo's claim is that sentence, with a different and computable generator);
- `GAP_E_CLOSE_MEMO.md` (empty-slot route dead; counter-correction confirms GAP-E open at the completeness clause).

---

## VERDICT UP FRONT — **RETRACTED AS CLOSURE (see banner).** Original text retained below as the record; read every closure claim as struck

**Claim in one sentence:** the two owned zone-extensions are not a bare list — they are **exactly the two canonical layers of the owned role group's own central extension** `1 → Z(Q₈) → Q₈ → Q₈/Z(Q₈) → 1`, i.e. the **proper nontrivial characteristic subquotients of Q₈**, and that list is computed (not asserted) to be exactly `{Z(Q₈) ≅ ℤ₂ (size 2), Q₈/Z(Q₈) ≅ V₄ (size 4)}` — whence:

- **(a) ~~size 6 is IMPOSSIBLE — arithmetic, not narration~~ → SCOPED (EoR-3): no size-6 SUBQUOTIENT.** ~~There is NO size-6 object in the role algebra at all.~~ **FALSIFIED AS STATED (Skeptic #1): `Sub(Q₈)` (the memo's own `subs_q8`, 6 subgroups, composition-closed via the owned Dedekind property) and `Out(Q₈) ≅ S₃` (the memo's own C5, 24/4 = 6) are canonical role-derived size-6 objects.** What survives is the scoped claim only: the subquotient orders of Q₈ are `{1,2,4,8}`, so no size-6 **subquotient** exists (computed, SSI — true and retained); the "arithmetic, not narration" tag applies to the scoped claim only.
- **(b) no canonical alternative exists at either size.** The only other order-4 subgroups — the three `C₄`s `⟨i⟩,⟨j⟩,⟨k⟩` — form a SINGLE Aut-orbit: `|Aut(Q₈)| = 24`, the induced action on the triple is the full `S₃`, transitive (computed, SSC/SSD). Choosing one is **"choosing an instance = a catalog"** — the corpus's OWN forcing schema, verbatim owned at `BOOK_01:1616`. The characteristic subgroups of Q₈ are exactly `{1, Z, Q₈}` (computed).
- **(c) the tower STOPS because the canonical list is exhausted.** The characteristic subgroups form a chain `1 < Z < Q₈` of length 2; its two successive quotients are the two extensions; after both are consumed there is no third canonical layer (computed, SSF/M8) — matching the owned COUNT-3 (`D0-TOWER-STOP-NOEXT-001`) instead of merely deferring to it.

**What is genuinely NEW (one step, stated in DEF-0.2.2 grammar, §FORCING):** *an admissible extension alphabet must be a canonical role-group object.* Everything else is computation on owned objects. The new step is not a new KIND of move: each of its prongs instantiates an M1 schema the corpus already owns and uses (`BOOK_01:792` conjugate-catalog ⇒ Hamiltonian; `BOOK_01:1616` catalog-free = characteristic; `NoExtension.lean:47` CASE-2 copy kill; `BOOK_01:1556` hidden-marker; DEF-0.3.1 exogeneity hinge).

**Why this is not the dyad-power candidate reborn (the prior kill respected):** `GAP_E_DYAD_POWER` killed the `2^k` generator for two reasons — it over-generated (`8 = 2³` must be pruned by an unowned bridge) and it misread `:47`. The canonical-subquotient generator produces **exactly the two owned extensions with NO pruning step** (computed F1/F2: the proper nontrivial characteristic-subquotient list of Q₈ has precisely two members, non-isomorphic, sizes 2 and 4). The one exclusion that resembles a prune — the improper `Q₈/1 = Q₈` itself — was claimed excluded "by the owned CASE-2 kill read exactly as its docstring states it". **CORRECTED (EoR-2): the docstring (`NoExtension.lean:15-17`) scopes CASE-2 to a hypothetical FOURTH zone; applying it to a THIRD zone is a transfer, assembly-grade (E-GE-3/OWN-3 class) — the exclusion stands only at that grade, not as verbatim-owned.**

**Honest scope:** this closes the **completeness** clause of GAP-E (W-HI.2's "extension list `{D₂, ABCD}` complete") in the **over-base fork (E-a)**. The **order** clause ("& ordered") is NOT claimed as forced by this memo — see §ORDER for the honest split. The F3 reading fork (over-base vs consecutive) is respected, not identified (§SELF-ATT-5).

---

## Claim E-SYNTH (DEF-0.2.2 form — candidate forcing)

Let `R := Ω₈ ≅ Q₈` be the owned role group (`D0-Q8-DEDEKIND-MINIMALITY-001`, BOOK_01 §01.7.1A) and `V₉ = R ⊔ {ω₀}` the owned pointed shell. Call `X` a **canonical layer of R** iff `X = H/K` with `H, K` characteristic subgroups of `R`, `K ≤ H`, and `1 < |H/K| < |R|` (proper, nontrivial).

**E-SYNTH.** *The admissible zone-extension alphabets over the pointed shell are exactly the canonical layers of the role group:*

> `AdmExt(X)  ⟺  X ∈ {Z(R), R/Z(R)}  =  {direct/return dyad D₂ (size 2), terminal role square ABCD (size 4)}.`

*Consequently:* (i) `∀X (AdmExt(X) → |X| ∈ {2,4})` — the exact missing sentence of `GAP_E_DYAD_POWER §RES`; (ii) no tower `(9,11,z₃)` with `z₃ > 13` exists (unique survivor of the computed kill matrix); (iii) the extension count is 2 and the tower stops at 3 zones, coinciding with owned COUNT-3.

*Direction of derivation (trap-f discipline):* the right-hand list `{Z(R), R/Z(R)}` and its sizes `{2,4}` are OUTPUTS of the subgroup/automorphism computation on `Q₈` built from integer quaternion tuples; at no point is `{2,4}`, `13`, or the tower fed in as an input. The tower `(9,11,13)` appears only in the final comparison (script SSM, positive control M5).

---

## Owned pre-facts (verbatim, file:line — every quote re-read on disk this pass)

### OWN-A. The role group and its forced identification (CORE-FORMALIZED / THEOREM)

**A.1** `BOOK_01…md:782-788` (§01.7.1A): "The signed terminal role space `Ω₈={A,B,C,D}×{+,−}` is *strictly isomorphic* to the quaternion group `Q₈={±1,±i,±j,±k}` under `A↦1, B↦i, C↦j, D↦k`, and this isomorphism is **forced by M1**, not picked from a menu. Status: **THEOREM**."

**A.2** `BOOK_01…md:792` — the corpus's catalog-forbiddance schema, applied at the Inn level: "A non-normal subgroup carries distinct conjugate copies `gHg⁻¹`. Telling those copies apart requires an external catalog of conjugates — exactly the catalog M1 (DEF-0.2.2) forbids. So *every* subgroup of the role group must be normal: the group is **Hamiltonian** (Dedekind sense)."

**A.3** `BOOK_01…md:794` — "**Order memory forbids commutativity.** A completed readout records the *order* of its operations…; that order-memory obligation, **already carried by the forward/return split `C₊/D₋`**, forces the role group to be **non-abelian**."

**A.4** `BOOK_01…md:802` — "`Q₈` is the **unique** non-abelian group of order `≤8` with zero non-normal subgroups… Hence `Ω₈≅Q₈` is a theorem, and the `+/-` orientation bit is the central `{±1}`."

### OWN-B. The triple identity and the abelianization (THEOREM + CORE-FORMALIZED)

**B.1** `BOOK_01…md:806-810` (§01.7.1B): "Inside `Q₈` the three canonical structural subgroups collapse to a single copy of `ℤ₂`: `[Q₈,Q₈] = Z(Q₈) = Φ(Q₈) = {±1}`. Status: **THEOREM** [^b01-31]." Table `:814-818`: "`[Q₈,Q₈]` (commutator) | **order memory** — the non-commutativity remainder of read/write order"; "`Z(Q₈)` (center) | the **orientation** `+/-` bit of `Ω₈`"; "`Φ(Q₈)` (Frattini) | the **non-generating remainder**".

**B.2** `BOOK_01…md:830` (§01.7.1C, the CORE-FORMALIZED paragraph, `D0-OMEGA8-CENTER-001`, Lean `D0.Foundation.Omega8Center`, cert `vp_omega8_center_collapse.py`): "in exact ℤ-quaternion arithmetic over `Q₈=\{±1,±i,±j,±k\}` the center is exactly `Z(Q₈)={±1}`, every commutator `[a,b]` lands in `{±1}` with `[i,j]=−1` realizing it, and (**the abelianization `Q₈/[Q₈,Q₈]` being the Klein four-group**, `g²∈{±1}`) the Frattini subgroup coincides… Status of that last step: **CORE-FORMALIZED**."

### OWN-C. The extension construction is the role-group route — the capacity text, quoted exactly as the task demands

**C.1** `BOOK_01…md:1523-1527` (§01.20): "A primitive two-port detector has a binary terminal dyad `D2`. The complete terminal role set is therefore `D2 × D2`, with four roles… `four terminal roles A,B,C,D = D₂×D₂`, `|ABCD| = 4`."

**C.2** `BOOK_01…md:1535-1539`: "`Ω₈ = four terminal roles A,B,C,D × {+,−}`, `|Ω₈| = 8`. The sign bit `{+,−}` is the irreversibility of write/erase… no further bit can be added without an exogenous orientation catalog."

**C.3** `BOOK_01…md:1548-1554`: "**The next two shell extensions are the only primitive unresolved capacities over the pointed shell: the direct/return dyad and the full terminal role square.** Therefore `V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ ABCD`."

**C.4** `BOOK_01…md:1889` (§01.22) — the sentence that names the construction route: "The capacity construction above lands the scene on the spectrum `9, 11, 13` **through the `Ω₈`-plus-basepoint / dyad `D₂` / terminal-role-square route.**" And `:1809-1812`: "Let the direct/return dyad have cardinality `D2=2`. Then the terminal role square has cardinality `|ABCD| = D₂² = 4`"; `:1827`: "The first **dyadic extension** and **terminal-role extension**…"

*Reading check (task item 1): is the capacity text compatible with "layers of the role group's own structure"?* Yes, and more than compatible — **the extension material is literally the role material**: the second extension IS the role alphabet ("the full terminal role square", C.3), and the first is the dyad whose square IS the role alphabet (C.1) and which carries the order-memory obligation (A.3). No owned sentence introduces any extension object from outside the role structure. What the text does NOT do by itself is state the *exhaustiveness rule* — that is the gap, and §FORCING is its candidate discharge.

### OWN-D. The corpus already OWNS "canonical = characteristic" as an M1 schema — the load-bearing find

**D.1** `BOOK_01…md:1616` (§01.20, THE-B, the `(ℤ/44)*` window group): "**The catalog-free (characteristic) subgroups** are exactly `{1}`, the 2-torsion `T` (order **4**), the squares `F` (order **5**), and `G` (**20**); **every other subgroup (three ℤ2, three ℤ10) requires choosing an instance = a catalog.** The M1-admissible symmetry-class spectrum is `{1, 4, 5, 20}`…"

This sentence does three things at once: (i) it EQUATES "catalog-free" with "characteristic" in so many words; (ii) it applies the equation to derive an admissibility spectrum (`{1,4,5,20}`) by EXCLUDING the non-characteristic subgroups; (iii) its exclusion clause — "choosing an instance = a catalog" — is exactly the kill this memo needs for the `C₄` triple. The schema is the same one as A.2 (conjugate-catalog ⇒ normal), one level up: A.2 forbids Inn-orbits of copies, D.1 forbids Aut-orbits of copies. *Domain honesty:* D.1 lives in the flavour-window section, not the extension section — this is a genuine transfer-of-schema and is pre-registered as SELF-ATT-2 below, not hidden.

**D.2** `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (row 549, PYTHON_CERTIFIED NO-GO): no canonical within-zone element selector exists. Same grammar again — canonical choices among Aut-indistinguishable instances are impossible; the synthesis USES this direction (objects canonical, letters not), see §FINGERPRINTS F-2.

### OWN-E. The CASE-2 copy kill and the first-instance rule (Lean-owned)

**E.1** `NoExtension.lean:44-48` (verbatim): "**CASE 2 / repeat needs a catalogue.** `≥2` identical copies carry a nontrivial copy-permutation symmetry: `|S_2| = 2 > 1`, so there is no canonical copy and selecting one is an external catalogue ⇒ `⊥M1`." Docstring `:15-17`: "**CASE 2 — `Z4` repeats an existing type.**… (Same forcing as `Ω₈≅Q₈` via Dedekind, BOOK_01 §01.7.1A.)" — the Lean file ITSELF cross-declares CASE-2 to be the same forcing as the conjugate-catalog schema.

**E.2** `NoExtension.lean:52` (verbatim): "A single first instance is canonical: `|S_1| = 1` (no catalogue) — the no-go bites only on repeats `(n≥2)`, not on first instances." (`first_instance_canonical`.)

### OWN-F. The exclusions below the tower and the exogeneity hinge

**F.1** `BOOK_01…md:1556`: "The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10` without losing direct/return capacity, and `V13` cannot be replaced by `V12` without losing one terminal role." (Used here for: trivial/marker-only extensions are owned-excluded; nothing above 13 is excluded by this sentence — that remains GAP-E's job.)

**F.2** DEF 0.3.1 exogeneity hinge (BOOK_00, verbatim via `TRICHOTOMY_V2_MEMO.md:19-23`): "θ counts as exogenous iff it (1) is not derived inside the corpus, (2) affects a distinguishable result or a law's formulation, and (3) is not an unavoidable part of the distinguishability protocol."

### OWN-G. The one-ℤ₂ concentrator (SYNTHESIS-status owned node)

`BOOK_02…md:2087-2097` (§02.34): "These are **not** independent two-element groups that happen to coincide numerically. They are **seven faces of the *same* ℤ₂**… **[THE] One ℤ₂, seven incarnations.**" Faces include: "#3 The center = commutator = Frattini subgroup of Q₈, all equal to `{±1}`" and "#5 The `±` orientation sign read off `Ω₈`". Four of the seven faces are Lean-proved (`BOOK_02:2410`; `D0-Z2-SPINOR-COVER-001`, row 213, CORE-FORMALIZED).

---

## THE COMPUTATION (script `gap_e_synthesis_check.py`, 65/65 PASS — headline outputs)

All from integer quaternion tuples and generic finite-group machinery; nothing read from the corpus except the group presentation the corpus itself owns (A.1):

1. **Subgroup lattice of Q₈:** exactly 6 subgroups, orders `[1,2,4,4,4,8]`; unique order-2 subgroup `= {±1}`; all subgroups normal (Dedekind, re-verified); **no Klein subgroup** (B1-B6).
2. **Aut/Inn/Out:** `|Aut(Q₈)| = 24` by exhaustive enumeration of unit-fixing homomorphic bijections; `|Inn| = 4`; the induced action on the `C₄`-triple is the **full S₃, transitive**; `Inn` = the kernel of that action, so **Out(Q₈) ≅ S₃ acts faithfully and transitively on `{⟨i⟩,⟨j⟩,⟨k⟩}`** (C1-C6). Task item 2's "verify on the actual group" — done, exhaustively.
3. **Characteristic subgroups: exactly `{1, Z, Q₈}`** (D1-D3). The `C₄`s are one Aut-orbit of size 3.
4. **Triple identity recomputed from scratch:** center, commutator closure, Frattini (= intersection of the three maximal `C₄`s) all equal `{±1}` (E1-E5) — independent re-derivation of the CORE-FORMALIZED B.2, not a citation of it.
5. **The canonical-layer list: EXACTLY TWO entries** — `(H,K) = (Z,1)`: `ℤ₂`, size 2; `(H,K) = (Q₈,Z)`: `V₄`, size 4; non-isomorphic; the characteristic subgroups form a chain `1 < Z < Q₈` whose successive quotients they are (F1-F5). **This chain is simultaneously the derived series, the upper central series, and the Frattini series of Q₈** (by the triple identity) — the corpus's three "canonical structural subgroups" (B.1) name one filtration, and the tower's extensions are its two graded pieces.
6. **The four cosets of `Z` in `Q₈` are the four sign-pairs `{x,−x}` = the four roles A,B,C,D under the owned iso** (G1-G3); `Q₈/Z` has exponent 2, i.e. IS the Klein four-group of the owned sentence B.2 (G4). So "the full terminal role square" = `Q₈/Z(Q₈)` is not a reading imposed from outside: **a role IS a coset of the center** — `A↦{+1,−1}=Z`, `B↦{+i,−i}=iZ`, `C↦jZ`, `D↦kZ` — element for element, by the owned identification A.1.
7. **Non-splitness:** `Q₈` has exactly ONE involution; no `V₄` subgroup ⇒ **no section of `Q₈ → Q₈/Z` exists** ⇒ the central extension `1→Z→Q₈→V₄→1` does NOT split (H1-H4). Consequence: the owned "`Ω₈ = ABCD × {±}`" (C.2) is verified as a SET bijection `(role, sign) ↦ sign·role` and CANNOT be a group product (`V₄×ℤ₂` is abelian; `Q₈` is not). **The unique group-theoretic content of the owned `×` is the central extension** — the synthesis is not one reading among several; the split reading is computationally false.
8. **Subquotient orders of Q₈ (ALL pairs, not just characteristic): `{1,2,4,8}`.** No 3, no 5, no 6, no 7 (I1-I3). **Kill (a) is arithmetic.**
9. **Census over ALL FIVE groups of order 8** (`ℤ₈, ℤ₄×ℤ₂, ℤ₂³, D₄, Q₈`, same pipeline): only `Q₈` has a **clean** canonical alphabet (exactly two layers, non-isomorphic, each realized once). `D₄`: 5 pairs including a rival `ℤ₄` size-4 alphabet and three `ℤ₂` realizations; `ℤ₈`/`ℤ₄×ℤ₂`: 5 pairs each with repeated iso-types; **`ℤ₂³`: ZERO canonical layers** — `Aut = GL(3,2)` is transitive on involutions, nothing is characteristic (L1-L7). See §FINGERPRINTS F-4 for why this census is the deepest part of the result.
10. **Tower kill matrix (`z₃ ≤ 21`, over-base fork):** unique survivor `(9,11,13)`; every rival dies by a NAMED prong; positive control (the owned tower passes) and a pipeline-level negative control (with `D₄` as role group the typing is NOT forced — the conclusion can fail and does fail off-target) both fire correctly (M1-M8).

---

## §FORCING — the ONE new step, as a DEF-0.2.2 forcing-by-contradiction (candidate)

**The step:** *any admissible zone-extension alphabet is a canonical layer of the role group.* Suppose not: let `X` be an admissible extension alphabet that is not one. Trichotomy over the provenance of `X` (each prong ends in an owned ⊥-schema):

- **Prong 1 (fresh alphabet).** `X` is not derived from the owned structure. Then `X` satisfies DEF 0.3.1 (1) (not derived inside the corpus) and (2) (it changes the scene: `|V| ≠ 33`, all downstream welds move — `q_EW`, `m_EW` recomputed in `GAP_E_COMPLETENESS §E3` change under `z₃=15`), and it is not part of the distinguishability protocol (3): `X` is **exogenous** — an imported alphabet catalog, `⊥M1`. *Ownership status of this prong:* DEF 0.3.1 is the owned hinge; what is new is only its application to extension alphabets. The owned derivational inventory at the extension point — `{ω₀(1), D₂(2), {±}(2), ABCD(4), Ω₈(8)}` — is the completeness memo's §III inventory, ~~skeptic-confirmed there~~ **CORRECTED (EoR-1): that memo's ATT-1 labels the inventory "this memo's constructions"; its skeptic confirmed the R3 verdict, NOT inventory exhaustiveness. The inventory is a coinage, and Prong 1's totality is therefore inventory-relative** — the exact weakness through which the skeptic's counter-objects (`Sub(Q₈)`, `Out(Q₈)`, the characteristic chain — role-DERIVED objects outside any element-inventory) entered.

- **Prong 2 (role-derived but non-canonical).** `X` is built from role material but requires selecting one realization out of several Aut-indistinguishable ones — one `C₄` of the triple `⟨i⟩,⟨j⟩,⟨k⟩` (computed: a single transitive `S₃`-orbit), one `ℤ₂`-factor of `V₄` (computed SSK: `Aut(V₄) ≅ S₃`, transitive on the three involutions — the SAME `S₃`), or any non-Aut-invariant subset. Selecting the instance **"= a catalog"** — the owned D.1 schema verbatim, which is the owned A.2 schema at Aut level, which is the owned E.1 CASE-2 schema ("no canonical copy… external catalogue"), which is the owned row-549 no-go one level down. `⊥M1`.

- **Prong 3 (role-derived, canonical, but not an alphabet).** `X` is Aut-invariant but not composition-closed. Computed exhaustively (SSJ): the Aut-orbits on elements are `{1}, {−1}, {±i,±j,±k}`; the invariant subsets have sizes `{0,1,2,6,7,8}`; the composition-closed invariant subsets are EXACTLY the characteristic subgroups `{1}, Z, Q₈`. The unique invariant candidate at size 6 — the six imaginaries — is not closed (`i·i = −1 ∉ X`): its products leak into a **hidden 2-element remainder** `{±1}` and its generated closure is ALL of Q₈. An alphabet whose readout products must be stored outside the alphabet is the owned **hidden-marker/hidden-memory** exclusion (F.1 `V₁₀` clause; `BOOK_01:1617` "scene pointer collision = hidden memory", grammar 01.11C). `⊥M1`.

- **Prong 4 (canonical, closed, but improper or trivial).** `X ≅ Q₈` (or the improper quotient `Q₈/1`): a new zone typed by the base zone's own alphabet is a **repeat of an existing type** — CASE-2, E.1. **CORRECTED (EoR-2): the CASE-2 docstring scopes the kill to a FOURTH zone; this third-zone application is an assembly-grade transfer, not a verbatim-owned kill.** **CORRECTED (EoR-5): "V₉ is Q₈-typed" was cited to the M2 campaign result — row 543 (`D0-M2-PHASE-LABELING-V9-SHELL-001`) is OPEN/PROOF-TARGET, not owned; the correct owned citations are `BOOK_01:1541-1544` (`V₉ = Ω₈ ⊔ {ω₀}`) + `:782` (`Ω₈ ≅ Q₈`, THEOREM).** `|X| = 1`: a marker-only extension is the owned `V₁₀` "extra hidden marker" exclusion (F.1).

- **Survivors** (computed, not asserted): the proper nontrivial characteristic subgroups and characteristic quotients of `Q₈` = `{Z(Q₈), Q₈/Z(Q₈)}`, sizes `{2,4}`. These ARE the two owned extensions, under the owned identifications (§IDENT below). ∎(candidate)

**Composite/bag escape (`|X| = 6` as `ABCD ⊔ D₂`), handled explicitly:** a third zone whose alphabet is the disjoint bag of both layers puts a second realization of the dyad capacity into a tower that already carries it at `V₁₁` — `≥2` realizations of ONE canonical capacity ⇒ owned CASE-2 (E.1), same prong as the `(9,11,11)` kill (script M4). A bag in a 2-zone tower `(9,15)` instead collides with owned COUNT-3 (three slots, `no_extension_theorem` docstring) and the owned slot↔type bijection (`vp_member_zone_isomorphism.py:20-22`). *Flag:* the bijection is owned-written as a fact about the tower; using it as an admissibility rule is assembly (same status the completeness memo gave once-only, E-GE-3) — recorded, not hidden.

## §IDENT — the owned identifications: the two extensions ARE the two layers

- **ABCD = Q₈/Z(Q₈), element for element.** Owned iso A.1 + computed G1-G4: the four roles are the four cosets of the center (each coset is a sign-pair `{x,−x}`, i.e. a role with its two orientations — exactly C.2's `Ω₈ = ABCD × {±}` read as the coset decomposition). The owned sentence B.2 ("the abelianization Q₈/[Q₈,Q₈] being the Klein four-group") is the same statement, CORE-FORMALIZED, since `[Q₈,Q₈] = Z` (B.1).
- **D₂ = Z(Q₈) = [Q₈,Q₈], by the owned order-memory chain.** A.3: the order-memory obligation is "already carried by the forward/return split `C₊/D₋`" — the direct/return dyad. B.1 table: order memory = `[Q₈,Q₈]`. B.1/B.2: `[Q₈,Q₈] = Z(Q₈) = {±1}`, THEOREM + CORE-FORMALIZED. OWN-G: the corpus's own concentrator THE declares all the spine's ℤ₂'s to be ONE group ("seven faces of the same ℤ₂"), so there is no owned SECOND ℤ₂ for the dyad to be. *Honesty:* no single owned sentence prints "the direct/return dyad = the center"; the identification is a two-link owned-prose chain + one owned theorem + the owned concentrator. **Fallback if the identification is rejected (pre-registered):** the completeness result does NOT need it. The canonical-layer list has exactly ONE size-2 member (computed F1/F4); whatever ℤ₂ the dyad "is", the admissible size spectrum is still `{2,4}`, size 6 still has no realization, and the kill matrix is unchanged. The identification upgrades the claim from "the extension SIZES are the layer sizes" to "the extensions ARE the layers"; only the upgrade leans on the chain.

## §BEGGING-POINT — the prior campaigns' gap, confronted (task item 3)

The prior verdicts' irreducible objection: *"no owned rule says extensions must come from the role group"* (COMPLETENESS ATT-1; DYAD_POWER OWN-1: "a LIST, not a GENERATOR"). Three answers, in decreasing ownership grade:

1. **The owned text builds them from the role group** (C.1-C.4, quoted): the extension objects are introduced ONLY as role-structure objects — the dyad (whose square is the role set) and the role square itself; §01.22:1889 names the whole route "`Ω₈`-plus-basepoint / dyad / terminal-role-square". For the MEMBERSHIP direction, provenance is not a reading — it is what the construction does, in print.
2. **For the EXHAUSTIVENESS direction, provenance is Prong 1** — a single application of the owned DEF-0.3.1 hinge: an extension alphabet not derived in-corpus is definitionally exogenous. What a skeptic can still resist is the *implicit totality* claim ("the in-corpus derivable alphabets are exactly the canonical role-objects"). ~~That totality is discharged not by assertion but by the **computed exhaustion**…~~ **KILLED (EoR-0, the fatal finding): the "computed exhaustion" was NOT total.** SSJ exhausted Aut-invariant **element-subsets**, but the survivor list itself contains a non-subset (`Q₈/Z` — a set of cosets), so the candidate space demonstrably includes role-DERIVED objects that no element-subset scan reaches — and there `Sub(Q₈)` (size 6, closed by the owned Dedekind property itself), `Out(Q₈)` (size 6), and the characteristic chain `{1,Z,Q₈}` (size 3) all live: canonical, role-derived, untouched by every prong. The exhaustion-over-owned-candidates method that made `GAP_E_CLOSE` NEG-1 survive worked there because NEG-1 was a NEGATIVE (a missed candidate only strengthens a no-go); run in the positive direction, a missed candidate class is fatal. That asymmetry is the method-lesson of this kill.
3. ~~**The remaining honest residue is exactly ONE schema-transfer**~~ **RE-PRICED (EoR-4): the residue is ≥ TWO transfers** — (i) D.1's "catalog-free (characteristic)" equation used outside the flavour-window where it is printed (SELF-ATT-2), AND (ii) the CASE-2 fourth-zone docstring used on a third zone (Prong 4, EoR-2). Each is a transfer of a schema the corpus owns elsewhere (A.2 Inn-level, D.1 Aut-level, E.1 copy-level, row-549 no-go direction) — still not the coining of a new predicate (contrast: P_narrow and the dyad-power generator had NO owned instance anywhere) — but "one transfer" was a mis-price, and with the trichotomy's totality killed (banner) the transfer count is moot for closure: the assembly does not force even if both transfers are granted.

**~~Why the begging-point DISSOLVES rather than relocates~~ — RETRACTED (Skeptic #1): the begging-point RELOCATED, it did not dissolve.** The totality claim moved from "owned inventory of junction addresses" (NEG-1's gap) to "owned grammar of alphabet-hood" (this memo's gap — the sharpened missing object, §SKEPTIC-#1). Original over-claim retained as the record: the prior routes needed an owned inventory in a domain that had none (junction addresses — NEG-1) or an owned generator the corpus never states (`2^k`). The synthesis needs neither: its inventory is the role group itself — **the single most-owned object in the corpus** (THEOREM + CORE-FORMALIZED ×2 + Dedekind bridge) — and its selection rule is the corpus's own catalog-forbiddance schema. The extension list stops being a brute list exactly when one notices the two list entries are the two graded pieces of the role group's own (owned, CORE-FORMALIZED) canonical filtration.

## §FINGERPRINTS — retro-dictions the synthesis did not input (convergence noted, NOT summed as proof; trap-j respected)

- **F-1 (COUNT).** The computed number of canonical layers (2) + base = 3 zones = owned COUNT-3 (`D0-TOWER-STOP-NOEXT-001`). The synthesis MEANS what the NoExtension docstring calls "the operational reading" of its 3 slots — and CASE-2's own docstring already cross-declares itself "the same forcing as `Ω₈≅Q₈` via Dedekind".
- **F-2 (selector no-go).** Computed K4: the induced Aut-action on the layer `Z` is trivial (letters `±1` canonical), on the layer `Q₈/Z` it is `S₃` on `{B,C,D}` (letters NOT individually selectable). The synthesis therefore PREDICTS: zones canonical as objects, within-zone letters not selectable — which is precisely the owned row-549 NO-GO. A no-go the corpus paid for separately falls out as a corollary of the layer structure.
- **F-3 (dyad-power EOR-1).** `GAP_E_DYAD_POWER` recorded as its strongest guard that "`|ABCD| = D₂²` is bookkeeping, not the forcing." Computed SSK: `V₄` has NO canonical `ℤ₂×ℤ₂` factorization (`Aut(V₄) ≅ S₃` transitive on the involutions — and these involutions are exactly the images of the three `C₄`s: the same `S₃` upstairs and downstairs). The synthesis derives the prior memo's honesty-guard as a theorem.
- **F-4 (the census — why Q₈ and only Q₈ can carry the tower).** Only `Q₈` among the five order-8 groups has a clean canonical alphabet (L6). And the two properties that make it clean are EXACTLY the two M1 reads that forced `Ω₈ ≅ Q₈` in §01.7.1A: *Hamiltonian* (all subgroups normal — kills the conjugacy catalogs) and *non-abelian* (order memory — the extension does not split, which is what makes `Z` characteristic and the layers rigid; the split/abelian `ℤ₂³` has ZERO canonical layers and could not grow a tower at all). The corpus forced the role group by M1 and the SAME two forcings are what make the extension tower well-defined. The scene did not get lucky twice; it is one forcing seen at two scales.
- **F-5 (W8 holomorph).** The owned campaign artifact `w8_holomorph_check.py` (PASS) exhibits `α = (i j k)` 3-cycling the character idempotents `e_B → e_C → e_D` in `ℂ[Q₈]` — the same `S₃`-orbit structure this memo computes on the subgroup triple, already realized in an owned exact-ℚ certificate.

## §ORDER — the honest split on W-HI.2's "& ordered"

E-SYNTH forces the extension SET `{Z, Q₈/Z}` (sizes `{2,4}`), hence the zone-size set `{9,11,13}`. The ORDER (dyad first: `9→11→13`, not `9→13→15`-relabelled) is:
- *supported* by the filtration direction (the chain `1 < Z < Q₈` ascends; `Q₈/Z` is defined by quotienting Z out, so the Z-layer is the prior object in the canonical series) — a reading, NOT claimed as a forcing here;
- *independently owned* at the size level by `D0-SCENE-TRIPLE-UNIQUE-001` (row 530: centre = unique Lucas in window ⇒ `z₂ = 11`) and narrated by the `+2`-parity route (`BOOK_01:1899`).
No order claim is minted from this memo. GAP-E's completeness clause is the claim; order rides on existing owners.

## Named risks & PRE-REGISTERED attack surface (six, incl. the strongest self-attack)

- **SELF-ATT-1 (STRONGEST, computed before the skeptic can find it): the invariant 6-subset.** "Your Lagrange kill is a strawman — a catalog-free size-6 role-object EXISTS: the six imaginaries `{±i,±j,±k}`, a single Aut-orbit, perfectly canonical. `V₁₅ = V₉ ⊔ {±i,±j,±k}` escapes prongs 1 and 2." Pre-answered by computation (SSJ, M6): it is the UNIQUE invariant 6-subset; it is not composition-closed (`i·i = −1 ∉ X`); its closure is ALL of Q₈ with hidden remainder `{±1}`. The composition-closed invariant subsets are exactly `{1}, Z, Q₈` (J6). **BUT (EoR-0, Skeptic #1): "UNIQUE invariant 6-subset" was true only inside the ELEMENT-SUBSET frame — the pre-registered attack was aimed one level too low. The skeptic's actual size-6 objects (`Sub(Q₈)`, `Out(Q₈)`) are not element-subsets and were never scanned; the self-attack answered the weaker rival and missed the stronger one. Recorded as the exact mechanism of the kill.** *Residual risk:* "composition-closed" as an alphabet requirement is itself a reading (owned support: every owned alphabet IS closed — `D₂`, `ABCD` (as `Q₈/Z`), `Ω₈` are groups; and the corpus's readout grammar records products of operations). If a skeptic produces an owned NON-closed alphabet anywhere in the corpus, prong 3 weakens and the 6-set reopens — named reopening hook.
- **SELF-ATT-2 (the schema transfer):** ":1616's 'catalog-free (characteristic)' is about the flavour window group `(ℤ/44)*`, not about extension alphabets — you are transferring, exactly what killed E-b." Priced in §BEGGING-POINT (3): the transfer is of a schema owned at THREE other sites (A.2, E.1, row 549), including one (A.2) inside the very section that forces the role group, and one (E.1) whose Lean docstring self-identifies with A.2. The E-b kills were of transfers whose schema had ZERO owned instances in the target domain AND self-refuted on the owned tower (NEG-1(b)); this transfer has multiple owned instances and the computed application REPRODUCES the owned tower (positive control M5). If the corpus's maintainer rules that schema-instances do not license cross-domain use even at count 4, E-SYNTH demotes from "closure candidate" to "the unique surviving candidate closure sentence with owned-schema support" — the honest downgrade path, stated in advance.
- **SELF-ATT-3 (the D₂ = Z identification):** "the forward/return split is a dyad of BRANCH OPERATORS (`C₊/D₋`), not the group element `−1`; your chain conflates a role-pair with a subgroup." Pre-answered: the fallback in §IDENT — the size-completeness result survives rejection of the identification outright, because the canonical layer list pins the SIZES regardless of which owned ℤ₂ the dyad is; and the concentrator THE (OWN-G) is the corpus's own declaration that there is only one ℤ₂ to be. What would genuinely wound: an owned sentence assigning the direct/return dyad to a ℤ₂ PROVABLY DISTINCT from the center. **WOUNDED AS PREDICTED (EoR-6, Skeptic #1): the wound landed, and worse than priced.** The owned rival reading is not "a distinct ℤ₂ group" but the **role-pair reading** — the two-port dyad whose square is the role set (`BOOK_01:1523`) and the forward/return split `C₊/D₋` named over two of the four ROLES (`BOOK_01:854`), i.e. `{C,D}` — a 2-element set of roles, not a subgroup at all. On that face-value reading the memo's OWN K2 computation (S₃ transitive on `{B,C,D}` ⇒ `{C,D}` not Aut-invariant) makes Prong 2 kill the corpus's own first extension: **the E-SYNTH biconditional fails right-to-left.** The fallback ("sizes survive any ℤ₂ reading") does NOT cover this, because `{C,D}` is not a ℤ₂ — it is size 2 without being the canonical layer. Also corrected: "the concentrator asserts the opposite" over-stated OWN-G — the concentrator lists seven ℤ₂ FACES and does not mention the direct/return dyad among them; it is silent, not opposite-asserting.
- **SELF-ATT-4 (provenance prong is the old gap in a new coat):** treated head-on in §BEGGING-POINT. The falsifiable content that distinguishes it from a coat of paint: (i) NO pruning step (the generator hits the owned list exactly — the dyad-power TELL is absent, computed F1/F2); (ii) the census (F-4): the rule is not tuned to output `{2,4}` — fed the wrong group it outputs the wrong/ambiguous/empty answer (D₄: rivals; `ℤ₂³`: nothing), so the conclusion is falsifiable and Q₈-specific; (iii) the cleanliness criterion is "zero instance freedom" (M1-natural), not a size template — dropping the size clause from the criterion changes nothing (only Q₈ still passes).
- **SELF-ATT-5 (fork discipline):** this memo closes the OVER-BASE fork (E-a). It does NOT identify over-base with consecutive (F3, row 547 stays OPEN as a fork), and does not claim the `+2`-step no-skip clause as owned — it derives the consecutive fork's CONCLUSION (`z₃ = 13`) inside the over-base reading, where `GAP_E_COMPLETENESS` §E4's computed kill matrix already showed G-CAP alone pins `(9,11,13)`. Cross-cite, no identification (trap d/i/j).
- **SELF-ATT-6 (census criterion post-hoc):** "CLEAN was defined to make Q₈ win." Pre-answered in SELF-ATT-4(iii) and computable: the criterion's clauses are (count = 2 = owned extension count) ∧ (pairwise non-isomorphic = zero instance freedom = the M1 criterion, D.1) — the size clause `{2,4}` is a READ-OFF, not a filter (removing it leaves the census verdict unchanged: the other four groups fail on count/multiplicity alone: 5, 5, 0, 5 pairs).

## What this memo does NOT show

- It does NOT mint anything. E-SYNTH is a candidate until the independent skeptic pass and `VERIFIED_CLOSURE_PROTOCOL.md`; status language throughout is candidate/DRAFT.
- It does NOT force the extension ORDER (§ORDER: supported + separately owned, not synthesized).
- It does NOT identify the F3 forks, does NOT touch GAP-W (the witness `+1`, row 545), does NOT upgrade the `+2`-parity narration, and does NOT edit any registry row, cert, or built Lean file.
- It does NOT claim the schema-transfer residue (SELF-ATT-2) is zero — ~~it prices it at "one transfer of a 4×-owned schema"~~ **re-priced to ≥ two transfers (EoR-4)**; the downgrade path stated there has been TAKEN (banner: killed as closure).
- The `nullity-30`/octonion/Leech adjacencies of §01.7.1 are NOT used (the corpus itself marks them overshoot-adjacent, `BOOK_01:834`).

## Theorem-candidate + what would MINT it (Lean sketch — code block ONLY, not added to the tree)

The entire load-bearing computation is finite and `decide`-able: the subgroup lattice of Q₈ lives on 8 integer 4-tuples; Aut-enumeration is a bounded search (24 hits among ≤ 6×4 generator-image candidates); the census is five explicit tables. The existing `D0.Foundation.Omega8Center` module (UQuat lists + `native_decide`) is the pattern to extend.

```lean
-- DRAFT SKETCH ONLY — documents the mintable package; do NOT add to 09_LEAN_FORMALIZATION.
namespace D0.Tower.CanonicalLayers
-- reuse UQuat, uqmul, Q8 from D0.Foundation.Omega8Center

-- (1) the subgroup lattice: the six mult-closed inverse-closed sublists of Q8 — by native_decide
-- (2) Aut(Q8) as the 24 hom-bijections (enumerated by images of i, j) — by native_decide
-- (3) characteristic := invariant under all 24 — proves char = [{1}, {±1}, Q8]
theorem characteristic_subgroups_are_chain : ... := by native_decide
-- (4) THE LAYER THEOREM: proper nontrivial characteristic subquotients = [Z2-layer, V4-layer]
--     with sizes [2, 4]  — the exhaustiveness sentence ∀X (AdmExt X → |X| ∈ {2,4}),
--     with AdmExt DEFINED as canonical-layer-of-Q8 (the §FORCING trichotomy is the
--     narration-layer discharge of that definition; the Lean layer owns the computation).
theorem canonical_layer_sizes : layerSizes = [2, 4] := by native_decide
-- (5) the Lagrange kill: 6 ∉ subquotientOrders Q8 (= [1,2,4,8]) — by native_decide
theorem no_size_six_subquotient : (6 : ℕ) ∉ subquotientOrders := by native_decide
-- (6) the C4-triple: Aut-orbit {⟨i⟩,⟨j⟩,⟨k⟩} of size 3, induced image = S3 — by native_decide
-- (7) census: the five order-8 tables; only Q8 is clean — by native_decide
end D0.Tower.CanonicalLayers
```

**Minting package — ~~(if the skeptic pass is survived)~~ WITHDRAWN (the pass was NOT survived; banner). Retained below only as the record of what a future successful closure would need; nothing here is proposed for minting:** claim-ID candidate `D0-GAP-E-CANONICAL-SUBQUOTIENT-001`; Lean module as above (all `native_decide`, zero sorry); cert = `gap_e_synthesis_check.py` promoted to `05_CERTS/vp_*` form with its negative controls; registry: new row + note-updates to rows 546 (WINDOW-DISSOLVE: GAP-E completeness clause candidate-closed) and 547 (fork: over-base leg gains an owner) — **maintainer actions, NOT performed here.** Reopening hooks carried: (i) an owned non-composition-closed alphabet anywhere in the corpus (reopens the 6-set); (ii) a maintainer ruling against schema-transfer at count 4 (demotes to candidate-sentence status); (iii) an owned ℤ₂ provably distinct from the center assigned to the direct/return dyad (breaks §IDENT's strong form, leaves sizes intact).

---

## SELF-SKEPTIC (pre-independent-pass, author-adversarial)

- Probed hardest: **Prong 3's "composition-closed"** (the only clause with no verbatim owned sentence). Held because (i) the exclusion it performs (the imaginary 6-set) ALSO dies as "whole group with hidden remainder" — the closure computation routes it into prong 4 + the owned hidden-marker grammar even if "closed" is struck as a requirement; struck-clause variant re-checked: the survivor list is unchanged (any invariant non-closed set has closure `Q₈` ⇒ prong 4). So prong 3 is a convenience clause, not a load-bearing one. Recorded so the skeptic need not spend the finding.
- Probed: **does E-SYNTH quietly re-open `(9,13,...)` (ABCD first)?** No claim either way — §ORDER split is honest; the SET result plus owned row 530 covers the tower; order-of-consumption is outside this memo's claim.
- Probed: **is the census's `ℤ₂³` row an artifact of my Aut computation?** `|Aut(ℤ₂³)| = 168 = |GL(3,2)|` (L7 sanity) — correct; transitivity on the 7 involutions is classical and reproduced by the enumeration.
- Verified the script counts its own checks (65 printed = 65 in ledger), rc=0; negative controls L2-L5/M7 can fail the CONCLUSION (they target cleanliness/forcedness, not technique), and two of my own hand-predictions about D₄ were CORRECTED by the computation (5 pairs, not 4; three size-2 realizations, not two) — evidence the controls are live, logged here as the compute-first discipline working.

**Next step (this memo's own demand):** independent skeptic pass (§05.8.R kill-mandate) targeting, at minimum: Prong 1's totality, the D₂=Z chain, the :1616 transfer, and any owned sentence contradicting the coset-reading of ABCD. Verdict and repairs appended below. *(The pass was run; the demand was met; the memo was killed. The self-skeptic above probed prong 3 and the census and missed the frame error entirely — retained unedited as the record of where author-adversarial review stopped short of an independent one.)*

---

## §SKEPTIC-#1 — verdict + repair log (INDEPENDENT pass, 2026-07-05/06, ACCEPTED IN FULL, no defense)

**VERDICT: KILLED-AS-CLOSURE.** E-SYNTH is not a closure of GAP-E. The banner at the head of this memo is the operative summary; this section is the accounting.

### The named second objects (§05.8.R standard — all three escape all four prongs)

1. **`Sub(Q₈)`** — the subgroup family of the role group: exactly the memo's own computed `subs_q8`, **6 members**. Aut-invariant as a family (every automorphism permutes subgroups); role-derived (nothing but Q₈ enters); and structurally closed **by the owned Dedekind/Hamiltonian property itself** (`BOOK_01:792-802` — the very §01.7.1A forcing the memo leans on guarantees every member is normal, the family stable). A catalog-free, size-6, role-derived object — the memo's headline (a) declared this impossible "in the role algebra AT ALL." It is not a subquotient — and nothing in the trichotomy requires an extension alphabet to be one; that requirement was the conclusion, not a premise.
2. **`Out(Q₈) ≅ S₃`** — **6 elements** (the memo's own C5: 24/4). Canonical and role-derived by construction.
3. **The characteristic chain `{1, Z, Q₈}`** — **3 members** (the memo's own D1). A canonical role-derived size-3 object, escaping the "no odd sizes" corollary the same way.

### The root cause (frame-level trap (f))

The totality scan (SSJ) quantified over Aut-invariant **element-subsets** of Q₈. But the survivor list itself contains `Q₈/Z` — a set of **cosets**, not an element-subset. The candidate space the memo actually needed ("canonical role-derived objects") was therefore never scanned; the scan frame was narrower than the memo's own survivors. The key quantity (the rival space) was implicitly constructed from the conclusion (the survivor type). This is trap (f) operating at the level of the FRAME rather than a formula — a new entry for the traps list.

### Errors of record (enumerated, no defense; inline corrections applied at the cited sites)

- **EoR-0 (FATAL — the kill):** the §FORCING trichotomy is not total; the §BEGGING-POINT(2) "computed exhaustion" claim is false as stated. Named counter-objects above. *Fix applied:* banner; §BEGGING-POINT(2) struck and corrected; SELF-ATT-1 annotated with the miss mechanism.
- **EoR-1:** Prong 1 cited the owned-inventory `{ω₀, D₂, {±}, ABCD, Ω₈}` as "skeptic-confirmed" in `GAP_E_COMPLETENESS`. False — that memo's ATT-1 calls the inventory "this memo's constructions," and its skeptic confirmed the R3 verdict, not inventory exhaustiveness. *Fix applied:* Prong 1 corrected; inventory re-labelled a coinage.
- **EoR-2:** Prong 4 (and the "not dyad-power reborn" paragraph) presented the CASE-2 kill as "read exactly as its docstring states it." The docstring (`NoExtension.lean:15-17`) scopes CASE-2 to a **fourth** zone; the third-zone application is an assembly-grade transfer (E-GE-3/OWN-3 class). *Fix applied:* both sites corrected.
- **EoR-3:** headline (a) "no size-6 object in the role algebra at all" over-claimed beyond the computed fact (no size-6 **subquotient**). *Fix applied:* headline scoped.
- **EoR-4:** §BEGGING-POINT(3) priced the schema-transfer residue at ONE; it is ≥ TWO (the :1616 characteristic transfer + the CASE-2 zone transfer). *Fix applied:* re-priced at both sites.
- **EoR-5:** Prong 4 cited "V₉ is Q₈-typed" to the M2 campaign result — registry row 543 (`D0-M2-PHASE-LABELING-V9-SHELL-001`) is OPEN/PROOF-TARGET, not an owner. Correct owned citations: `BOOK_01:1541-1544` + `:782`. *Fix applied.*
- **EoR-6:** SELF-ATT-3's dismissal ("the concentrator asserts the opposite") over-stated OWN-G — the concentrator's seven faces do not include the direct/return dyad; it is silent. And the genuine rival reading (the role-pair `{C,D}`, `BOOK_01:854/:1523`) is live: under it the memo's own K2 makes Prong 2 kill the corpus's first extension — the E-SYNTH biconditional fails right-to-left. *Fix applied:* SELF-ATT-3 corrected; §IDENT's strong form demoted to a fork (center-reading vs role-pair-reading, unadjudicated).

### What SURVIVES the kill (structure results — computed, reusable, NOT closure claims)

- **S-1 (canonical-layer computation).** Characteristic subgroups of Q₈ = `{1, Z, Q₈}`; proper nontrivial characteristic subquotients = exactly `{ℤ₂, V₄}`, sizes `{2,4}`; `Out(Q₈) ≅ S₃` transitive on the C₄-triple; triple identity recomputed. (Sections SSB-SSK, arithmetically untouched by the kill.)
- **S-2 (scoped Lagrange fact).** No size-6 **subquotient** of Q₈ exists (orders `{1,2,4,8}`). True and computed; insufficient for GAP-E only because subquotient-hood is not owned as the alphabet grammar.
- **S-3 (the census / F-4 fingerprint).** Q₈ is the UNIQUE order-8 group with a clean canonical-layer alphabet, and the cleanliness is produced by exactly the two owned §01.7.1A forcings (Hamiltonian + non-abelian). This Q₈-specialness result stands on its own as a structure observation.
- **S-4 (no-size-prune property).** The canonical-subquotient generator hits the owned list `{2,4}` with no pruning step — the dyad-power TELL is absent. Survives as a comparative fact about candidate generators.
- **S-5 (the coset reading of ABCD).** The four roles = the four cosets of the center, element for element under the owned iso (computed G1-G4) — unchallenged by the skeptic and consistent with `BOOK_01:830`.

### The SHARPENED missing object (what this kill bought)

Four independent confirmations now agree GAP-E's completeness clause is open (R3 underdetermination → E-b forge → dyad-power → E-SYNTH), and each narrowed the missing object. After this kill it is at its sharpest yet:

> **(MISSING — the alphabet-grammar clause.)** *An owned rule stating which canonical role-objects can serve as extension ALPHABETS: the letters of an extension alphabet are **states realized as added vertices** — elements or cosets, i.e. blocks of a partition of the role material — and not derived families (subgroups, which pairwise overlap in the identity; automorphism classes, which are not vertex material; nested chains).* Given that clause, the computation of this memo DOES close GAP-E: the partition-realizable canonical role-objects of Q₈ are exactly `Z` (elements) and `Q₈/Z` (cosets), sizes `{2,4}`, and `Sub(Q₈)`/`Out(Q₈)`/the chain are excluded by grammar, not by fiat.

The clause is NOT owned as a quantified rule (see §OWNERSHIP-CHECK below for exactly what IS owned). Whether its owned instances license a fifth forge is an **OWNER DECISION** — explicitly not forged here.

---

## §OWNERSHIP-CHECK — the one targeted verification (performed on disk 2026-07-06; quotes verbatim; NO forge attempted)

**Question:** do the extension definition sites verbatim own "the added vertices ARE the letters (elements/cosets/roles)" — i.e. is the partition/vertex-realization grammar owned, or fiat?

**What IS owned — the instance level (the identity is printed in the definitions themselves, as set-equalities whose right-hand sides are the alphabet sets):**

- `BOOK_01…md:867` (§01.8): "The signed detector cycle must acquire a graph-birth marker: `V₉ = Ω₈ + ω₀`." — the nine vertices ARE the eight signed roles plus the witness; no "a set of size 9" indirection.
- `BOOK_01…md:1541-1546` (§01.20): "A reusable shell also requires a stationary marked witness section `ω₀`. Hence `V₉ = Ω₈ ⊔ {ω₀}`, `|V₉| = 9`."
- `BOOK_01…md:1548-1554`: "Therefore `V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ four terminal roles A,B,C,D`." — **the disjoint unions are OF the alphabet sets themselves**: the two added vertices of `V₁₁` are the dyad's two elements; the four added vertices of `V₁₃` are the four roles. The vertex-realization identity is verbatim at both extension definition sites.
- `BOOK_01…md:1530`: "The four roles are not a list to be chosen — they are forced as the minimal self-sufficient act of record: reading (A), read (B), trace (C), reference (D)." — letters are **acts/states of record** (vertex-realizable state material, not structural families).
- `BOOK_01…md:782-786`: the roles are element/coset material of the role group under the owned iso (`A↦1, B↦i, C↦j, D↦k`; with S-5's computed coset reading, a role = a coset of the center).

**What is NOT owned — the rule level:** a sweep of BOOK_01 + BOOK_03 for a quantified vertex-letter identification ("vertices are …", "as vertices", "vertex set is", "added/new vertices") finds **no general sentence**; the only hit (`BOOK_03:436` "vertices are binary…") concerns refinement arity, not alphabet grammar. No printed clause quantifies over extensions: *"any extension's added vertices must be the letters of a state alphabet (elements/cosets), never a derived family."* The three counter-objects are excluded by every printed INSTANCE (all owned alphabets are partition-block families realized as vertices — computed in the companion script's kill-control section: the cosets of `Z` partition `Q₈`; `Sub(Q₈)` members pairwise overlap in the identity, hence never a partition; the chain is nested; `Out` partitions `Aut(Q₈)`, not the role material) — but excluded by INSTANCES, not by an owned RULE.

**Resolution (per the two-branch protocol):** the vertex-realization grammar is **verbatim-owned at the instance level at every definition site** (all five quotes above), and **NOT owned as the quantified type-identity clause**. The sharpened missing-object spec (§SKEPTIC-#1) is therefore exactly a **one-quantifier lift of owned instance-grammar** — the smallest gap GAP-E has ever been reduced to, with its ownership base cited. Recorded as: **candidate 5th forge — OWNER DECISION, do not forge now.** Until and unless that decision is taken and survives its own adversarial pass: **GAP-E's completeness clause is OPEN — this memo changes nothing in the registry and asserts no closure.**
