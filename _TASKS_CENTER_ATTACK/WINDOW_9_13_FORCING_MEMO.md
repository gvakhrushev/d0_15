# WINDOW_9_13_FORCING — the capstone window `[9,13]` is a projection of the owned capacity chain, not a primitive input (DRAFT; skeptic pass #1 done, all repairs applied)

**Status:** DRAFT candidate; no registry row edited; no .lean file added to the built tree (Lean drafts live as code blocks in this memo only). Pre-flight run: `window`, `tower`, `TOWER-STOP`, `SceneTripleUnique`, `Omega8`, `maturity` — no existing row owns "window bounds forced"; owners cross-referenced below are D0-SCENE-TRIPLE-UNIQUE-001 (row: `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`), D0-TOWER-STOP-NOEXT-001, D0-CAPACITY-V11-001, D0-OMEGA8-001.
**Companion check:** `_TASKS_CENTER_ATTACK/window_forcing_check.py` — **11/11** check() calls PASS, rc=0 (~10 independent: WINDOW_ENDPOINTS_DERIVED is a projection of OWNED_CHAIN_TRIPLE; kill matrix + negative controls, §V). *(Error of record E1: an earlier draft of this line claimed "13/13" — a miscount, integrity-grade in this corpus; caught by skeptic #1, repaired here and in §V.)*
**Referee context (G1, pressure-point-1 residual):** `D0_REFEREE_ASSESSMENT.md:153-156`:

> "The residual a referee can still press: the *window* `[9,13]` and the odd-return parity are themselves motivated by `Ω₈=8` and the `det T=−1` orientation — well-argued and Lean-backed, but they are the layer below the capstone, and a maximally-conservative referee will trace the forcing one level further to the admissibility criteria (role=orbit, the maturity threshold `Ω₈`)."

## Claim W (DEF-0.2.2 form, candidate)

**W.** The interval hypotheses of the capstone (`SceneTripleUnique.lean:77`: `hlo : 9 ≤ z₁`, `hhi : z₁ ≤ 13`) are not primitive admissibility inputs. Both endpoints are *outputs* of the owned graph-birth capacity chain

`V₉ = Ω₈ ⊔ {ω₀}` (9 = 8+1), `V₁₁ = V₉ ⊔ D₂` (11 = 9+2), `V₁₃ = V₉ ⊔ {A,B,C,D}` (13 = 9+4),

which is already Lean-typed with proved cardinalities (`D0/Core/FiniteTypes.lean`). A restated capstone that consumes this chain derives `(9,11,13)` with **zero window hypotheses**; the Lucas-centre and parity legs survive as proved convergences instead of inputs.

*Consumption-hygiene fork (¬W) — demoted from an M1 claim per skeptic repair E:* the numerals `9, 13` are **not** exogenous in the corpus — `CarrierForcing.address_ladder` (Lean, `:81-82`) proves `4+5=9 ∧ 9+2=11 ∧ 11+2=13`, BOOK_01 §01.22 owns the chain narratively, and the referee itself grants the status quo is "well-argued and Lean-backed" (`D0_REFEREE_ASSESSMENT.md:154`). So ¬W is **not** `⊥M1`; it is *unconsumed ownership*: the capstone's formal statement imports as bare numeral hypotheses what the corpus owns as structure one layer down. W is a consumption-hygiene upgrade (make the theorem consume its owners), not a rescue from contradiction. No owned document asserts the interval itself as primitive (sweep below); every owned occurrence of `9` and `13` decomposes them.

*Honest residual (pre-registered, not hidden):* two necessity joints of the chain are narrated-only — **GAP-W** (the witness `+1`) and **GAP-E** (extension completeness `{D₂, ABCD}`). These labels are coined **by this memo, not by the corpus** (skeptic repair A-1): the corpus's own soft-joint register `BOOK_01…md:1617` lists {aliasing step, role lists, `+2` parity} — the same declaratory practice, but neither of W's gaps appears in that list. W dissolves the *interval* residual and relocates the referee's pressure onto these two narrated joints; it does not close them. Candidate language throughout.

## Owned pre-facts (verbatim, file:line)

### A. The capstone and what it consumes

**A1.** `SceneTripleUnique.lean:74-78` (repo-root copy; built copy `09_LEAN_FORMALIZATION/D0/VNext2/SceneTripleUnique.lean` identical):

```
theorem scene_triple_unique
    (z₀ z₁ z₂ n : ℕ)
    (hladder₁ : z₁ = z₀ + 2) (hladder₂ : z₂ = z₁ + 2)
    (hcentre : z₁ = lucas n) (hlo : 9 ≤ z₁) (hhi : z₁ ≤ 13) :
    (z₀, z₁, z₂) = (9, 11, 13)
```

The bounds enter as bare numerals. Nothing upstream in this file derives them.

**A2.** The capstone's own cert states the window is load-bearing for its route — `05_CERTS/vp_scene_triple_unique.py:15-16`:

> "widening the window to [9,29] admits a SECOND Lucas centre (29=L_7), breaking uniqueness — so the window bound [9,13] is load-bearing, not decorative"

(Checked: widening to `[9,29]` in fact admits levels `{5, 6, 7}` — including the **even** level 6, `L₆=18`. The Lean statement `unique_lucas_in_window` quantifies over ALL `n`, so the odd-parity leg is decorative *in the Lean capstone as written*; the window carries even the parity's load. §V, control NC_OLD_ROUTE_NEEDS_WINDOW.)

**A3.** Registry row (`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`, D0-SCENE-TRIPLE-UNIQUE-001): "[Iter26 CAPSTONE] (9,11,13) is the UNIQUE admissible scene triple proved as a SINGLE statement composing four previously-distinct forcing legs: 3 zones (CarrierForcing.admissible_unique) + +2 address ladder (address_ladder) + centre L5=11 + odd-return parity. NEW content: unique_lucas_in_window…"

### B. Why 9 — the lower end

**B1. Lean-owned decomposition (definition + cardinality theorems).** `09_LEAN_FORMALIZATION/D0/Core/FiniteTypes.lean:9-16`:

```
abbrev Dyad := Fin 2
abbrev Role := Dyad × Dyad
abbrev Orient := Bool
abbrev Omega8 := Role × Orient
abbrev Witness := PUnit
abbrev V9 := Sum Omega8 Witness
abbrev V11 := Sum V9 Dyad
abbrev V13 := Sum V9 Role
```

with `card_dyad = 2` (:18), `card_role = 4` (:21), `card_omega8 = 8` (:24), `card_v9 = 9` (:27), `card_v11 = 11` (:30), `card_v13 = 13` (:33), `scene_card_total = 33` (:36). Also `D0/Core/DyadABCD.lean:17`: `theorem omega8_cardinality : Fintype.card Omega8 = 8 := card_omega8`. **So "8+1=9" is a Lean THEOREM about a Lean DEFINITION**: the decomposition `V9 := Sum Omega8 Witness` is type-level owned; what is *not* Lean-owned is the *necessity* of the `Witness` summand (`Witness := PUnit` is posited). That necessity is narrated:

**B2. Witness necessity (narrated).** `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:1541-1545` (§01.20 "Capacity closure of four terminal roles A,B,C,D, Ω8 and V9", heading :1521):

> "A reusable shell also requires a stationary marked witness section `ω0`. Hence
> V_9=\Omega_8\sqcup\{\omega_0\}, \qquad |V_9|=9."

and `:1987-1990` (§01.19a apparatus): "The witness/basepoint \(\omega_0\) gives the first addressable graph-birth shell \[ V_9=\Omega_8\sqcup\{\omega_0\}. \]" — one sentence of necessity each; no Lean owner (`D0.Topology.WitnessHalting` was checked: its theorems are orbit-average emission arithmetic over `Fin 8`, not witness necessity).

**B3. What forces 8.** `BOOK_01…md:1539`:

> "The sign bit `{+,−}` is the irreversibility of write/erase; it is the one bit that distinguishes the act from its undo, and no further bit can be added without an exogenous orientation catalog. Hence `Ω8 = ABCD × {±}`, `|Ω8|=8`"

and the group-theoretic owner `BOOK_01…md:802`:

> "`Q_8` is the **unique** non-abelian group of order `\le8` with zero non-normal subgroups. Dedekind (1897) then globalizes: *every* Hamiltonian group contains `Q_8` as a factor, so the minimality is not an artifact of stopping the scan at order `8` — it is absolute. Hence `\Omega_8\cong Q_8` is a theorem, and the `+/-` orientation bit is the central `\{\pm1\}`"

(M1 side at `:792`: non-normal subgroup ⇒ conjugate catalog ⇒ ⊥M1 ⇒ Hamiltonian; BOOK_00 §00.2 lists "Why Q₈?" among worked forcings, `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/0004__00.2__primitive-thesis.md:35-36`.) Honest cap: `BOOK_01…md:832` — the octonion route to the same `8` is "**HYP, not a forcing** — `\dim\mathbb O=8` (algebra dimension) and `|\Omega_8|=|Q_8|=8` (group order) are two *different* eights".

**B4. The SECOND owned decomposition of 9 (the fork).** `01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md:299-310` (§04.1.START "Why the shell ladder starts at 9"):

> "**Start = anchor + operationality level [^b04-16].** The operationality level is `D_Σ = 5`, because a self-distinguishing language needs five separable roles — `Code`, `Canon`, `Test`, `History`, `Access` — and so at least five distinguishable address classes. With fewer than five, two roles collide onto one address and resolving the collision needs an external catalog, which M1 forbids. Hence
> \mathfrak{D}_1 = \mathfrak{D}_{\rm anchor} + D_\Sigma = 4 + 5 = 9 .
> The anchor `4` and the level `5` are both forced (not fitted), so the first shell is `9`"

with `D_anchor = 4` forced at `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md:910-935` (§03.23.1, M1 fork: `<4` role unrealized / `>4` empty-slot significance catalog), and the ladder at `BOOK_03…md:1049-1056`: "Starting from `D_anchor = 4` (03.23.1) plus the operational start `D_Sigma = 5` … Defect : 4 + 5 = 9, Memory : 9 + 2 = 11, Shell : 11 + 2 = 13". The Lean trace of THIS route is `D0/Synthesis/CarrierForcing.lean:81-82`:

```
theorem address_ladder :
    (4 + 5 = 9) ∧ (9 + 2 = 11) ∧ (11 + 2 = 13) := by decide
```

— **literal numeral arithmetic**; `D_anchor`/`D_Σ` appear only in its docstring. **Fork finding (trap i):** the corpus owns TWO decompositions of 9 — `8+1` (Ω₈⊔ω₀; BOOK_01 §01.20/§01.8, Lean-typed) and `4+5` (anchor+operationality; BOOK_03/04, numeral-level in Lean). They agree numerically; **no owned statement identifies their summand structures** (the five maturity levels `L1..L5 = Code/Canon/Test/History/Access` are "organization levels, not space dimensions", `BOOK_01…md:112` — not the 4+1 of `ABCD+ω₀`). The current capstone docstring cites `4+5` (`SceneTripleUnique.lean:11-12`) while the centre cert cites the `Ω₈` threshold (8-side) — the capstone currently *mixes the fork*. **Corroboration (skeptic C-1 bonus): §01.22 mixes the fork within one section** — the chain enters as `V_9=|\Omega_8|+1=9` (`BOOK_01…md:1821-1824`) while the same section's `+2`-forcing subsection writes the ladder as `\underbrace{4+5=9}_{\text{defect}}` (`:1903`).

### C. Why "stop at 13" — the upper end

**C1. BOOK_00's own answer is about COUNT, not size.** `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/0004__00.2__primitive-thesis.md:38` (mirrored `BOOK_00…md:169`; NOTE: this lives in **§00.2**, not §00.8 — the traps-checklist's "§00.8 mis-address" strikes again):

> "*Why stop at 13?* **Not** "because 15 is worse." Three zones because there are exactly three structural necessities (defect, memory, shell); there is no fourth role, so no fourth zone."

**C2. What D0-TOWER-STOP-NOEXT-001 actually PROVES.** `09_LEAN_FORMALIZATION/D0/Tower/NoExtension.lean:61-65`:

```
theorem no_extension_theorem :
    (phi⁻¹ + phi⁻¹ ^ 2 = 1) ∧
    (phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1) ∧
    (1 < Fintype.card (Equiv.Perm (Fin 2)))
```

Three algebra facts (quadratic closure; `p³` reduction into `span{1,p}`; `|S₂|>1`). The zone reading is *declared* in its docstring, `:25-27`: "the tower stops at the three rungs `[9,11,13]`. The COUNT (3 slots, no 4th) is proved here; the role-NAMES (distinguish/preserve/close) are the operational reading of the 3 forced slots". **It contains no statement about zone SIZES.** Registry row (CLAIM_TO_LEAN_MAP.csv): "M1 no-extension: tower stops at 3 zones, no 4th (05.6 obligation 5)".

**C3. What actually caps the size at 13 (narrated).** `BOOK_01…md:1548-1556` (§01.20):

> "The next two shell extensions are the only primitive unresolved capacities over the pointed shell: the direct/return dyad and the full terminal role square. Therefore V_{11}=V_9\sqcup D_2, \qquad V_{13}=V_9\sqcup four terminal roles A,B,C,D."
> "…The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10` without losing direct/return capacity, and `V13` cannot be replaced by `V12` without losing one terminal role."

So `13 = 9 + |ABCD|` is the LARGEST owned extension; "no zone > 13" is the *completeness* of the extension list `{D₂, ABCD}` — narrated, not Lean. Its cert is content-free on exactly this point — `05_CERTS/vp_v1141_abcd_omega8_v9_phi_capacity.py:63-64`:

```python
check('V8 lacks witness', 8==Omega8 and V9==Omega8+1, 'no basepoint')
check('V10 duplicates witness/hidden state', 10>V9, 'extra state')
```

— the "V10 exclusion" check is literally `10 > 9` (trap (b)/(f): cannot fail). **Mis-attribution finding:** the distance-to-done map's "upper by tower-stop (D0-TOWER-STOP-NOEXT-001)" is wrong as stated — tower-stop caps the *count*; the *size* cap is §01.20 extension-completeness. Kill-matrix demo (§V): `(9,11,15)` passes BASE-9 + PARITY + COUNT-3 and is killed **only** by the narrated extension list.

**C4. Co-owner of the whole chain (added per skeptic C-1 — the strongest finding of pass #1): BOOK_01 §01.22.** Heading `:1805`: "## 01.22 Forced return windows and non-post-hoc phase unfolding"; `:1807`: "The phase-unfolding windows used by D0 are not chosen by searching for rational approximants to a circle.  They are forced by terminal capacity." The section restates the full chain in count form (`:1817-1833`): `|four terminal roles A,B,C,D|=D_2^2=4`, `|\Omega_8|=2|four terminal roles A,B,C,D|=8`, `V_9=|\Omega_8|+1=9`, `V_{11}=V_9+D_2=11, \qquad V_{13}=V_9+|four terminal roles A,B,C,D|=13`. Co-ownership is declared at `:900`: "the two `+2` capacity steps to `11` and `13` are owned by the capacity ladder (§01.20) and the return-window argument (§01.22)".

### D. The `+2` ladder

**D1. Capacity route (Lean-typed).** `FiniteTypes.lean:15-16`: `V11 := Sum V9 Dyad`, `V13 := Sum V9 Role` — steps `+2` and `+4` over the base are the owned cardinalities `|D₂|=2`, `|ABCD|=4`; consecutive gaps `(2,2)` follow arithmetically (`card_v11`, `card_v13`).

**D2. The corpus's PRIMARY narrated `+2`-forcing (added per skeptic C-1): BOOK_01 §01.22, Status CORE-FORCING.** Subsection heading `:1887`: "### The address step is forced to `+2` — the orientation-class no-sign-catalog argument (forcing: GOLDEN THE 3.11.B / COR 3.13.B(1), BOOK-I-ARCHITECTURE)". The argument (`:1889-1907`): the Lucas defect `ε_n = φ^n − L_n = (−1)^{n+1}φ^{−n}` alternates sign; a `+1` junction step flips the orientation class and "to splice the two layers across that flip one must supply an external orientation bit … Importing that bit is exactly importing an external significance/sign catalog, and is forbidden by M1"; "The step `5 → 7` preserves the orientation class … Hence the minimal admissible junction step is `+2`". Closing status (`:1907`): "Status: CORE-FORCING (forcing: GOLDEN THE 3.11.B and COR 3.13.B(1)–(2), BOOK-I-ARCHITECTURE; ⊥-proof via `(-1)^n` orientation parity, no sign catalog)" — and, key for W: "capacity sets the cardinalities, orientation-parity sets the increment, and neither leans on the other." Note the *minimality* step ("minimal admissible junction step") is still narrated — a `+4` splice also preserves the class; minimality = no-skip.

**D3. Parity route (Lean + narration) and the DUAL status — no cherry-pick.** `BOOK_03…md:1044-1047`: "the address step is the identity element of the double cover `Z(Q8)`, proved as `det(T^{n+2}) = det(T^n)` (with the `+1` flip `det(T^{n+1}) = -det(T^n)` as the negative control)". Lean owner `D0/Dynamics/ToralAutomorphism.lean:47-49`: `det_T_pow : Matrix.det (T ^ n) = (-1)^n`. **Honest cap: the Lean-owned part forces step EVENNESS, not `+2`** — every even step preserves the orientation class (`+4` passes; §V control NC_PARITY_ADMITS_PLUS4). The narrowing to exactly `+2` is narrated twice: §01.22 `:1901-1907` (D2 above, CORE-FORCING) and `BOOK_03…md:1058`: "Any step other than `+2` re-imports an external gluing parameter, so `{9,11,13}` is the unique M1-admissible spectrum." **The corpus carries BOTH statuses for `+2` simultaneously** — CORE-FORCING (`:1907`) *and* soft-joint (`BOOK_01…md:1617`):

> "**The aliasing step is stated but not formalized — this is a soft joint of the corpus, alongside the role lists and the +2 parity.**"

Both must be cited together; W's gap map records the `+2` narrowing as narrated-CORE-FORCING with the formalization gap the soft-joint register declares.

**D4. 2δ₀ link — negative finding.** `BOOK_01…md:669`: "The factor `2` is structural: `\delta_0` is half of the branch asymmetry, while `2\delta_0` is the full one-dimensional branch gap." — this owns the factor 2 of the *branch gap* (δ₀ sector). **No owned statement links it to the zone-address step `+2`.** The task's conjectured link is unsupported in the corpus; do not cite it.

### E. The Lucas centre and the maturity threshold

**E1.** `D0/VNext2/SceneCenterSpacetimeConvergence.lean:15-16` (docstring): "The centre is forced as the unique intersection `{ L_n } ∩ [9,13] = {11}` (`L₃ = 4`, `L₇ = 29` fall outside), at the forced level `5` (smallest odd `n` with `L_n > Ω₈ = 8`)." Lean: `unique_center_in_window` (:53-56) — six `decide` facts against the *hypothesized* window; `level_five_forced` (:59-61) — checks odd levels 1,3 only:

```
theorem level_five_forced :
    (Nat.fib 0 + Nat.fib 2 = 1) ∧ (Nat.fib 2 + Nat.fib 4 = 4) ∧ ¬(1 > 8) ∧ ¬(4 > 8) ∧ (11 > 8)
```

**E2.** `BOOK_01…md:1500` ([Iter25]): "The centre is *forced* as the unique intersection `{Lucas returns Lₙ} ∩ [9,13] = {11}` … at the forced level `5` (the smallest odd return with `Lₙ > Ω₈ = 8`, and the `L5 = Access` closure of the maturity levels). Since the `±2` half-width is the already-owned orientation step … the whole triple `{9,11,13} = {L₅−2, L₅, L₅+2}` has *both* centre and width forced — zero free integers."

**E3. The maturity threshold's operational content.** `05_CERTS/vp_scene_center_spacetime_convergence.py:22-24`: "Level 5 is itself forced: it is the smallest odd return whose Lucas value exceeds the shell Omega8 = 8 (L_1=1, L_3=4, L_5=11 > 8), i.e. the first return able to host the full shell + basepoint + terminal roles, and the closure level of the five functional maturity levels L1..L5 (Code/Canon/Test/History/Access)." Two defects: (i) "host the full shell + basepoint + terminal roles" read additively is `8+1+4=13 > 11 = L₅` — sloppy; the clean threshold is `Lₙ > 8 ⇔ Lₙ ≥ 9 = |V₉|` (host the *pointed shell*); (ii) the threshold cites the 8-side of the fork while the ladder cites 4+5 (see B4). Maturity-levels naming: `BOOK_01…md:112`: "The five functional maturity levels are `L1` Code (`C`), `L2` Canon (`D_min`), `L3` Test (`Δ`), `L4` History (`R`), `L5` Access (`O`) — organization levels, not space dimensions."

**E4. Minimality is parity-free (new observation, §V check).** The full Lucas sequence has `L₂=3, L₄=7 ≤ 8`, so the *smallest* level with `Lₙ > 8` is 5 with or without the odd restriction. The "odd" clause in `level_five_forced` is consistent but not load-bearing for minimality (it matters only for the return-*class* reading, det `T^n = −1`).

## Gap map — "window forced" decomposed into atomic obligations

| # | Obligation | Owner status | Where |
|---|---|---|---|
| W-LO.1 | `\|Ω₈\| = 8` | **OWNED-Lean** (cardinality); forcing narrative owned (Q₈/Dedekind, M1-normality) | `FiniteTypes.lean:24`, `DyadABCD.lean:17`; `BOOK_01:792,802`; `BOOK_00 §00.2:35` |
| W-LO.2 | the `+1`: witness `ω₀` exists, is unique, is forced (**GAP-W**) | *Decomposition* Lean-typed (`V9 := Sum Omega8 Witness`); *necessity* NARRATED one-liner; cert check arithmetic-only | `FiniteTypes.lean:13-14`; `BOOK_01:1541,1987-1990`; `vp_v1141:63` |
| W-LO.3 | centre zone contains the pointed shell (`9 ≤ z₁`) | Definitional in Lean (`V11 := Sum V9 Dyad`); necessity narrated (§01.20) | `FiniteTypes.lean:15`; `BOOK_01:1548` |
| W-HI.1 | zone COUNT = 3, no 4th | **OWNED-Lean with named reading** (3 algebra facts + declared count-reading) | `NoExtension.lean:61-65,25-27`; `BOOK_00 §00.2:38` |
| W-HI.2 | extension list `{D₂, ABCD}` complete & ordered ⇒ max zone = 13 (**GAP-E**) | NARRATED; cert content-free (`10>9`); **the actual size-cap owner** | `BOOK_01:1548-1556`; `vp_v1141:63-64` |
| W-HI.3 | tower-stop is NOT a size bound (mis-attribution guard) | Established here: `(9,11,15)` passes count-3+parity+base-9 | §V kill matrix |
| W-STEP | steps: evenness OWNED-Lean; "exactly +2" narrated (CORE-FORCING status, formalization gap in the soft-joint register); capacity route makes steps = owned cardinalities | `det_T_pow` (evenness); `BOOK_01 §01.22:1887-1907` (PRIMARY narrated forcing, "Status: CORE-FORCING") + `BOOK_03:1058` (narr.) + `BOOK_01:1617` (soft joint); `FiniteTypes.lean:15-16` (capacity) | D1-D3 |
| W-INT | the INTERVAL `[9,13]` as an object | **Never primitive in any owned source**: endpoints are outputs (`9 = card V9`, `13 = card V13`); the interval appears only in the capstone/centre statements as hypothesis | A1, E1 |

## The two routes

**Route A — DERIVE-BOUNDS (keep the capstone shape, prove `9 ≤ z₁` and `z₁ ≤ 13` as lemmas).**
Lower leg: provable from W-LO.1 + W-LO.2 + W-LO.3 — but W-LO.2's necessity is narrated, so the lemma still bottoms out in a named hypothesis. Upper leg: there is **no owned object to derive `z₁ ≤ 13` from** — the only owned size-cap is GAP-E (extension-list completeness), whose formalization is a genuine M1 meta-step (same difficulty class as the §05.6 no-extension obligation was). Route A is longer, keeps the numerals in the statement, and after all that work the interval would *still* be a derived-from-named-hypotheses object. Rejected as the primary route.

**Route B — DISSOLVE-WINDOW (restate the capstone to consume the owned chain). RECOMMENDED.**
The capstone never needed an interval: if it consumes base = pointed signed shell, extensions = the two owned primitives, then `(9,11,13)` follows arithmetically from owned cardinalities, and:
- the window hypotheses `hlo/hhi` **disappear** from the formal statement;
- the endpoints come back as theorems (`card_v9 = 9`, `card_v13 = 13`), and `unique_lucas_in_window` survives as a *corollary against derived bounds* — now actually present in the skeleton as `unique_lucas_in_derived_window`, with both Lucas tails carried over (skeptic repair A-2; the Lucas leg turns from selector into convergence — consistent with its cert's "load-bearing" control, which guarded the *old* route);
- the parity leg is recorded honestly as evenness (`det_T_pow`), no longer asked to select `+2`;
- the referee residual **changes type**: from "two unexplained numerals" to two narrated-necessity joints (GAP-W, GAP-E — *this memo's* labels; the corpus's soft-joint register `BOOK_01:1617` shows the declaratory practice but lists {aliasing, role lists, `+2` parity}, not these two — skeptic repair A-1).

Cost comparison: Route B is ~40 lines of Lean consuming only already-proved cardinality theorems; Route A requires formalizing GAP-E *first* and still ends with a weaker statement.

## Lean skeleton (Route B, candidate DRAFT — memo-only, NOT added to the built tree)

```lean
-- CANDIDATE v2 capstone (window-free). Status: DRAFT, pre-skeptic, not built, not registered.
-- Obligations: OB-0 owned; OB-1..OB-3 named joints (GAP-W, GAP-E) — see ledger below.
import D0.Core.FiniteTypes
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Tactic

namespace D0.VNext2.SceneTripleForced
open D0

/-- Lucas indexing as in `SceneTripleUnique` (`L₅ = fib 4 + fib 6 = 11`). -/
def lucas (n : ℕ) : ℕ := Nat.fib (n - 1) + Nat.fib (n + 1)

/-- **Chain form (zero hypotheses).** The owned graph-birth capacities are `(9,11,13)`;
    the steps are the owned cardinalities `|D₂| = 2`, `|ABCD| = 4`; the centre is `L₅`.
    Consumes ONLY `card_*` theorems (OB-0). -/
theorem scene_triple_from_owned_chain :
    (Fintype.card V9, Fintype.card V11, Fintype.card V13) = (9, 11, 13) ∧
    Fintype.card V11 = Fintype.card V9 + Fintype.card Dyad ∧
    Fintype.card V13 = Fintype.card V9 + Fintype.card Role ∧
    Fintype.card V11 = lucas 5 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    simp [card_v9, card_v11, card_v13, card_dyad, card_role, lucas]

/-- **Uniqueness form (window-free capstone).** Any triple whose base is the pointed
    signed shell and whose two extensions are the owned primitives is `(9,11,13)`;
    the centre `= L₅ = 11` is DERIVED, not hypothesized. The three hypotheses are the
    owned decompositions; their necessity is the named narrated layer (GAP-W, GAP-E). -/
theorem scene_triple_unique_v2 (z₀ z₁ z₂ : ℕ)
    (hbase  : z₀ = Fintype.card Omega8 + 1)     -- OB-1: witness "+1" (GAP-W)
    (hstep₁ : z₁ = z₀ + Fintype.card Dyad)      -- OB-2: D₂ is the first extension (GAP-E)
    (hstep₂ : z₂ = z₀ + Fintype.card Role) :    -- OB-3: ABCD is the second & last (GAP-E)
    (z₀, z₁, z₂) = (9, 11, 13) ∧ z₁ = lucas 5 := by
  subst hbase hstep₁ hstep₂
  norm_num [card_omega8, card_dyad, card_role, lucas]
  -- expected to close by computation; if `lucas` unfolding resists, `decide` the numeral leg

/-- **Window recovered as output.** The old interval's endpoints are theorems, so the old
    `unique_lucas_in_window` becomes a corollary about DERIVED bounds. -/
theorem window_endpoints_derived :
    Fintype.card V9 = 9 ∧ Fintype.card V13 = 13 := ⟨card_v9, card_v13⟩

/-- Monotone tail, as in the old module (`SceneTripleUnique.lean:40-46`, re-proved). -/
theorem lucas_ge_of_six_le {n : ℕ} (hn : 6 ≤ n) : 18 ≤ lucas n := by
  unfold lucas
  have h1 : Nat.fib 5 ≤ Nat.fib (n - 1) := Nat.fib_mono (by omega)
  have h2 : Nat.fib 7 ≤ Nat.fib (n + 1) := Nat.fib_mono (by omega)
  have : Nat.fib 5 = 5 := by decide
  have : Nat.fib 7 = 13 := by decide
  omega

/-- Low tail, as in the old module (`SceneTripleUnique.lean:48-55`, re-proved). -/
theorem lucas_le_of_le_four {n : ℕ} (hn : n ≤ 4) : lucas n ≤ 7 := by
  unfold lucas
  have h1 : Nat.fib (n - 1) ≤ Nat.fib 3 := Nat.fib_mono (by omega)
  have h2 : Nat.fib (n + 1) ≤ Nat.fib 5 := Nat.fib_mono (by omega)
  have : Nat.fib 3 = 2 := by decide
  have : Nat.fib 5 = 5 := by decide
  omega

/-- **Old capstone recovered as corollary (skeptic repair A-2).** Against the DERIVED
    bounds `card V9 = 9 ≤ Lₙ ≤ 13 = card V13`, the level is uniquely 5 — the old
    `unique_lucas_in_window` with its interval endpoints now theorems, not hypotheses. -/
theorem unique_lucas_in_derived_window {n : ℕ}
    (hlo : Fintype.card V9 ≤ lucas n) (hhi : lucas n ≤ Fintype.card V13) : n = 5 := by
  rw [card_v9] at hlo
  rw [card_v13] at hhi
  by_contra hne
  rcases Nat.lt_or_ge n 5 with h | h
  · have := lucas_le_of_le_four (by omega : n ≤ 4); omega
  · have h6 : 6 ≤ n := by omega
    have := lucas_ge_of_six_le h6; omega

/-- **Cheap strengthening (new, optional).** Level-5 minimality is parity-free:
    `L₂ = 3` and `L₄ = 7` also fail `> 8`, so 5 is minimal in the FULL Lucas sequence.
    (Repairs the odd-only check in `level_five_forced`.) -/
theorem level_five_minimal_all_parities :
    lucas 1 = 1 ∧ lucas 2 = 3 ∧ lucas 3 = 4 ∧ lucas 4 = 7 ∧ lucas 5 = 11 ∧
    (∀ m, m ≤ 4 → lucas m ≤ 8) ∧ 8 < lucas 5 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, ?_, by decide⟩
  intro m hm
  interval_cases m <;> decide
  -- NB: with this def and ℕ-subtraction, `lucas 0 = fib 0 + fib 1 = 1` ≠ true L₀ = 2;
  -- the bound `≤ 8` holds either way, but any lemma naming L₀ must use the real value 2.

/-- GAP-W formalization target (sorry-marked, NOT claimed): a witness-selector owner in the
    style of `D0.Matter.CKMClass5SelectorOwner`. Candidates {V8: no marker, V9: one marked
    witness, V10: two markers}; V10 is killed by the ALREADY-OWNED copy-symmetry lemma
    (`D0.Tower.repeat_has_nontrivial_copy_symmetry : 1 < card (Equiv.Perm (Fin 2))`), and
    one witness is canonical by `D0.Tower.first_instance_canonical`. What has NO Lean owner
    yet is EXISTENCE (≥ 1 witness = the halt-closure necessity, BOOK_01:1987-1990). -/
theorem witness_plus_one_forced : True := by sorry -- OB-1 target; statement TBD via skeptic
end D0.VNext2.SceneTripleForced
```

**Obligations ledger (owned vs new):**

| OB | Content | Status |
|---|---|---|
| OB-0 | all cardinalities (`2,4,8,9,11,13,33`) | **OWNED-Lean**: `FiniteTypes.lean:18-36`, `DyadABCD.lean:15-17` |
| OB-1 | witness `+1` necessity (GAP-W) | **NEW**. Partial reuse available: uniqueness ← `first_instance_canonical` (`NoExtension.lean:52`), V10-kill ← `repeat_has_nontrivial_copy_symmetry` (`NoExtension.lean:47`); *existence* has no Lean owner (narrated `BOOK_01:1541,1987-1990`) |
| OB-2/3 | extension completeness & order `{D₂, then ABCD}` (GAP-E) | **NEW**, hard: an M1 completeness meta-step; candidate sketch — any extension alphabet is dyadic (non-dyadic ⇒ exogenous alphabet catalog), powers `2^k, k≥3` repeat the signed square (⇒ CASE-2 copy-symmetry kill, reusing `NoExtension`); **sketch only, not claimed** |
| OB-4 | count = 3, no 4th | **OWNED-Lean with named reading** (`no_extension_theorem` + docstring `:25-27`) |
| OB-5 | centre convergence `11 = L₅ = \|Tr T⁵\|` | **OWNED-Lean** (`lucas_five`, `trace_T5`, `spacetime_center_convergence`) |
| OB-6 | parity = step evenness | **OWNED-Lean** (`det_T_pow`); explicitly NOT `+2`-selecting; not load-bearing in v2 |

## Verification: `window_forcing_check.py` — 11/11 check() calls PASS (rc=0)

Count corrected per skeptic repair B-1 (error of record E1: previously misreported as "13/13"); ~10 independent (WINDOW_ENDPOINTS_DERIVED is a projection of OWNED_CHAIN_TRIPLE). Failability honesty: the OWNED_CHAIN_* and NC_* checks can fail the conclusion; the *new-criteria half* of KILL_MATRIX_AGREEMENT mirrors the owned chain by construction, so on its own it is failable mainly through a mirror-coding error — its conclusion-failing power lives in the OLD-criteria column plus the agreement requirement.

Kill matrix (new criteria = BASE-9 + STEP-SET + COUNT-3 vs old = ladder+Lucas+window): both admit exactly `{(9,11,13)}` over candidates incl. `(8,10,12)`, `(9,11,15)`, `(9,13,17)`, `(9,12,15)`, `(11,13,15)`, `(7,9,11)`, `(9,11,13,15)`, `(9,29,49)`. Negative controls:
- `NC_MUTATED_OMEGA8_FAILS_CONCLUSION`: `|Ω₈| → 10` ⇒ chain gives `(11,13,15) ≠ (9,11,13)` — the chain is falsifiable by the owned count;
- `NC_OLD_ROUTE_NEEDS_WINDOW`: `[9,29]` admits Lucas levels `{5,6,7}` — old-route uniqueness breaks AND the even level 6 is admitted (the old Lean capstone's parity leg was decorative; the window carried its load); the new route consumes no window;
- `NC_PARITY_ADMITS_PLUS4`: `(9,13,17)` passes parity — evenness, not `+2`, is what `det_T_pow` owns;
- `WEAKEST_LINK_DEMO`: `(9,11,15)` passes BASE-9+PARITY+COUNT-3; only GAP-E kills it.

## Named risks & PRE-REGISTERED attack surface

- **ATT-1 (strongest self-attack): "you renamed the gap, not closed it."** `hbase/hstep₁/hstep₂` are still hypotheses; a hostile reading says `z₀ = card Ω₈ + 1` is the same move as `9 ≤ z₁`. Prepared answer, in candidate language: (i) the chain-form theorem has *zero* hypotheses (it is about the owned types themselves); (ii) in the uniqueness form the hypotheses change TYPE — from two bare exogenous numerals to owned structured decompositions, each with an M1-forcing narrative, a falsifiable count-cert, and partially owned kill-lemmas; (iii) the untyped residue is exactly GAP-W-existence + GAP-E — pre-registered **here** (the labels are this memo's, not the corpus's; `BOOK_01:1617`'s soft-joint list covers the `+2` parity and role lists, not these two — repair A-1). If the skeptic produces an owned statement that the interval itself is primitive, W dies; the sweep found none, and skeptic #1's independent D2/D3/D4 sweeps found none either. **Verdict of pass #1: SURVIVES as candidate — the interval residual dissolves; the necessity residual is honestly relocated, not erased.**
- **ATT-2 (the 9-fork, trap i).** `8+1` vs `4+5`: numerically equal, structurally unidentified; the current capstone docstring cites `4+5` while the centre cert thresholds on the 8-side. v2 must consume ONLY the `8+1` chain and cross-cite `4+5` (BOOK_03 03.23.6 / `address_ladder`) as a separate owned route — presenting them as "two independent channels to 9" would need an identification owner first (trap d: two different nines until proven one).
- **ATT-3 (tower-stop smuggle).** `no_extension_theorem` proves algebra facts; "no 4th zone" is its declared reading. v2 consumes it only as COUNT-3 and must cite the docstring's own admission (`:25-27`). The kill matrix shows tower-stop cannot cap sizes — this *corrects* the distance-to-done map's "upper by tower-stop" attribution rather than relying on it.
- **ATT-4 ("8+1=9 is itself a naming").** In Lean, yes: `V9 := Sum Omega8 Witness` is a definition and `Witness := PUnit` is posited (trap j: naming freedom = passport). The forcing content of the `+1` lives in the narrated halt-closure necessity. v2's claim is scoped accordingly: it dissolves the WINDOW as input; it does not claim the base is M1-derived in Lean.
- **ATT-5 (cert wording).** `vp_scene_center…py:23` "host the full shell + basepoint + terminal roles" is additively wrong for `L₅ = 11 < 13`; repair to "host the pointed shell (`≥ |V₉| = 9`)" if v2 lands. Does not affect v2 (threshold not consumed).
- **ATT-6 (adoption cost — the full stranded-text list, completed per skeptic repair F).** "window bound [9,13] is load-bearing, not decorative" (`vp_scene_triple_unique.py:16`) guards the OLD Lucas-selector route; v2 retires that route as selector and keeps it as convergence — no owned statement is contradicted, but adopting v2 strands FOUR texts that must be rewritten in the same change (single-source guard cascade): (1) the capstone cert `vp_scene_triple_unique.py` (docstring + the [9,29] control, which also *undercounts* — it claims "a SECOND Lucas centre (29=L_7)" but `L₆=18` enters too, verified independently by skeptic #1); (2) registry row `D0-SCENE-TRIPLE-UNIQUE-001` ("[Iter26 CAPSTONE] … +2 ladder + centre L5=11 + odd-return parity … unique_lucas_in_window", `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`); (3) `BOOK_01…md:1501-1502` — "the scene is not chosen, it is the unique fixed point of its own admissibility window" (the "its own … window" phrasing presumes the interval formulation); (4) `D0_REFEREE_ASSESSMENT.md:146-152` (the Iter26 update note describing the capstone as Lucas-in-window).

## What this does NOT show

- It does NOT derive `9` or `13` from M1 axioms in Lean. GAP-W (witness existence) and GAP-E (extension completeness) remain narrated; they are the honest layer below, now named as the exact residual.
- It does NOT reconcile the `8+1` / `4+5` fork (flagged for a separate task; candidate identification would need its own forcing memo).
- It does NOT upgrade odd-return parity beyond evenness, and records that the old capstone's Lean statement never used parity at all.
- It does NOT edit the registry or the built Lean tree; everything here is DRAFT candidate material pending verification of the pass-#1 repairs and `VERIFIED_CLOSURE_PROTOCOL.md` minting.

## Skeptic pass #1 — verdict and repair log (accepted in full, no defense)

**Overall verdict (relayed 2026-07-05): Claim W SURVIVES as candidate** (no second object produced; endpoints confirmed as outputs of the owned chain; independent sweeps found no owned interval-primitive and no owned size-cap). **Route B SURVIVES as candidate direction, BLOCKED from minting** until the repairs below are verified in a follow-up pass.

Errors of record, enumerated (all repaired in this revision):
- **E1 (integrity-grade).** Memo claimed "13/13 PASS"; the script contains exactly **11** `check()` calls (~10 independent). Repaired at header + §V + script docstring. In a corpus that quarantined v17 over a fabricated citation, a wrong count is mandatory-fix-first.
- **E2.** GAP-W/GAP-E were attributed to the corpus's soft-joint register; `BOOK_01:1617` lists {aliasing step, role lists, +2 parity} — neither gap is in that list. Attribution rescoped at Claim W, Route B, ATT-1: the labels are this memo's.
- **E3.** Route B promised `unique_lucas_in_window` as a corollary that the skeleton did not contain. Added `unique_lucas_in_derived_window` + both Lucas tails to the skeleton.
- **E4 (strongest content finding).** The sweep missed **BOOK_01 §01.22's own subsection "The address step is forced to `+2`" (`:1887-1907`, Status: CORE-FORCING)** — the corpus's primary narrated `+2`-forcing — and §01.22's chain restatement (`:1807-1833`). Added as C4 + D2; W-STEP row now shows the DUAL status (CORE-FORCING narration + soft-joint formalization gap) with no cherry-pick. Bonus corroboration: §01.22 itself mixes the 9-fork (`:1821-1824` vs `:1903`).
- **E5.** The ¬W fork clause over-claimed `⊥M1`; the status quo is Lean-backed unconsumed ownership, not catalog-import. Demoted to consumption-hygiene language.
- **E6.** Adoption-cost list was incomplete; ATT-6 now lists all four stranded texts (cert, registry row 530, `BOOK_01:1501-1502`, `D0_REFEREE_ASSESSMENT.md:146-152`).
- **E7.** Skeleton comment "L₀ = 2 included" was false under the memo's own `lucas` def (ℕ-truncation gives `lucas 0 = 1`); self-caught and fixed pre-verdict; skeptic concurs.

Skeptic verifications that STRENGTHEN W (logged): the old cert's `[9,29]` control *undercounts* (claims one extra centre `L₇=29`; `L₆=18` also enters — memo's `{5,6,7}` confirmed); the V10-exclusion check is literally `10>9` (confirmed content-free); `WitnessHalting` is orbit-average arithmetic, not witness necessity (confirmed — GAP-W has no Lean owner).

## Cross-link (2026-07-05, updated post-skeptic): GAP-W forging pass done; skeptic #1 WOUNDED → repaired

OB-1 (GAP-W, the witness `+1`) now has a dedicated forging memo: `_TASKS_CENTER_ATTACK/GAP_W_WITNESS_MEMO.md` (v2, post-skeptic-#1) + `gap_w_witness_check.py` (10/10, rc=0). Result (DRAFT): `|V_base| = |Ω₈|+1 = 9` FORCED GIVEN **THREE** named joints — **W-BRIDGE-1′** (the contract's *stable re-detection class* `BOOK_01:1166.5` realized as ≥1 stationary marked vertex; the halt-QUOTIENT is CONTRACT-owned at `:296/:366.5`, BUT the halt-proper lands at **+0** in `:846`/`:858` — skeptic-found adverse texts, so the +1 rides the re-detection layer only), **W-T1** (CASE-2 schema on marks; `:1556` does NOT back this branch), and **W-BIT** (`:1539` scope-transferred to mark labels; load-bearing by toggle). 8-kill: contract + narrated re-detection bridge + COMPUTED full-cycle freeness (nothing in Ω₈ is stationary). 10-kill: copy branch reuses `repeat_has_nontrivial_copy_symmetry`; bit branch is the W-BIT transfer with `:1556` fallback. **Corrections to THIS memo's OB-1 row (`:285`):** (i) "uniqueness ← `first_instance_canonical`" is imprecise — it is the **no-overfire certificate at m=1**, NOT a V10-killer (the V10-kill is copy-symmetry + W-BIT); (ii) "existence has no Lean owner (narrated `BOOK_01:1541,1987-1990`)" understates BOTH ways — the halt-quotient layer is contract-owned, but two owned +0 texts (`:846`/`:858`) cut against the naive halt→vertex bridge. GAP-E remains untouched.

