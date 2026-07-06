# GAP_E_CLOSE — attempt to FORGE the extension-completeness clause (E-b no-skip) from owned empty-slot material, or sharpen the underdetermination to its irreducible residual (DRAFT — retraction OVERTURNED, see counter-correction)

> ## 🔴 COUNTER-CORRECTION (2026-07-05, main-loop primary-source verification) — the RETRACTION below is itself WRONG; GAP-E R3 STANDS
>
> The skeptic that produced the "KILLED — z₃=13 is owned" verdict **over-read the sources**. Verified by hand:
> - `CarrierForcing.lean:81-82` `address_ladder : (4+5=9) ∧ (9+2=11) ∧ (11+2=13) := by decide` is **pure arithmetic** — it does NOT force the step choice; "11+2=13" true does not exclude "11+4=15".
> - `SceneTripleUnique.lean:74-77` takes `hladder₂ : z₂ = z₁+2` **and** the window `9 ≤ z₁ ≤ 13` as **HYPOTHESES** — conditional on exactly what the window campaign exists to justify (circular if cited as justification).
> - `BOOK_01:1889` forces even ("+2, never +1") by holonomy-**PARITY** (`L_n=φ^n+ψ^n` ⇒ Z₂). Parity excludes ODD steps only — **nothing about +4.** `(9,11,15)` (steps +2,+4, both even) is a 3-zone tower TOWER-STOP-NOEXT-001 (count-3) does NOT exclude.
>
> So the top step's **uniformity** (+2 vs non-minimal even +4) is **narrated (minimality/"strictly"), not owned-forced** — exactly the original GAP-E R3 verdict (two prior passes). The KILL is refuted; **GAP-E remains OPEN**; the E-b no-skip clause is still the object to forge, begging-point (pre-laid address space) intact. The retraction was an orchestration error caught by primary-source re-reading.

> ## ⛔ RETRACTION BANNER (2026-07-05) — Skeptic #1 verdict: **KILLED**, accepted in full — **[OVERTURNED by the counter-correction above]**
>
> **The load-bearing headline of this memo — that GAP-E's top-zone upper bound (`z₃ ≤ 13`) is "UNFORGEABLE from current owned material" and that the M1-admissible top-zone value `z₃` is "unconstrained above 13" — is FALSE and is hereby RETRACTED.**
>
> An owned, Lean-proved (0 sorry, rc=0), cert-backed, CORE-FORMALIZED forcing of `z₃ = 13` already EXISTS and is registered:
> - **`D0.VNext2.SceneTripleUnique.scene_triple_unique`** — registry `CLAIM_TO_LEAN_MAP.csv:530`, status CORE-FORMALIZED / LEAN_PROVED, cert `05_CERTS/vp_scene_triple_unique.py` rc=0, `09_LEAN_FORMALIZATION/D0/VNext2/SceneTripleUnique.lean:74-85`. Proves: **any `+2` ladder `(z₀,z₁,z₂)` whose centre `z₁` is a Lucas number in `[9,13]` is uniquely `(9,11,13)`** — via `unique_lucas_in_window` (`SceneTripleUnique.lean:59`) forcing `z₁ = 11`, hence top zone `z₂ = 13`. Verbatim (`SceneTripleUnique.lean:74-85`): `theorem scene_triple_unique … (hladder₂ : z₂ = z₁ + 2) (hcentre : z₁ = lucas n) (hlo : 9 ≤ z₁) (hhi : z₁ ≤ 13) : (z₀, z₁, z₂) = (9, 11, 13)`.
> - **`D0.Synthesis.CarrierForcing.address_ladder`** — registry row 215, `CarrierForcing.lean:81`, verbatim: `theorem address_ladder : (4 + 5 = 9) ∧ (9 + 2 = 11) ∧ (11 + 2 = 13) := by decide`. The **top rung is pinned** (`11 + 2 = 13`), not free.
> - **`D0-TOWER-STOP-NOEXT-001`** — registry row 257 — no 4th zone.
>
> The memo cannot call the bound "unforgeable" while it is already **forged and registered**. `scene_triple_unique` literally names and proves the bound this memo declared unownable. **This is the KILL.** The memo's ONLY structurally-available escape (the residual's non-uniform `+4` top step, `11→15`, evading `hladder₂`) does **not** survive, because the `+2` top step / centred window is itself owned (`address_ladder`; and the very orientation argument this memo cites as OWN-1, `BOOK_01:1889-1899`, is the owned derivation that the ladder advances by `+2` "never `+1`"). The `+4` step therefore **breaks the owned window** centred at the forced centre 11; it is not an owned open gap. The memo never mounted (let alone won) an argument that `scene_triple_unique` begs the `+2` top step, so the escape is unmade.
>
> **Everything below the banner that asserts `z₃` is open, unforgeable, or underdetermined at the top-zone size is RETRACTED.** What survives (demoted to leads, not conclusions): the located empty-slot analysis (NEG-1) as a *note on why the empty-slot route was the wrong instrument*, the v17 phase-lock dead-derivation (independent of the headline), and the citation/inventory hygiene. See **§SKEPTIC-#1** at the foot for the full repair log and errors of record. Companion script `gap_e_close_check.py` now carries the owned-forcing KILL control (§VII) and prints **VERDICT: KILLED**.

**Status:** DRAFT — headline RETRACTED (KILLED by Skeptic #1). NO registry row edited; NO .lean added to the built tree; NO edit to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`. Lean sketches below are code blocks only. Companion can-fail script: `_TASKS_CENTER_ATTACK/gap_e_close_check.py` (now KILLED, §VII owned-forcing control, 45/45 checks, rc=0).
**Parent:** `GAP_E_COMPLETENESS_MEMO.md` (v2 post-skeptic-#1) — that memo delivered the R3 two-route missing-object spec (E-a capacity route / E-b step route). This memo attacks the cheapest route (E-b) at its pre-registered begging-point and reports the outcome honestly.
**Pre-flight:** `preflight.sh "junction step minimal no-skip empty slot"` → no existing row owns the no-skip/extension-completeness clause (confirmed 2026-07-05). Cross-ref owners unchanged from parent memo §3.

## VERDICT UP FRONT — **RETRACTED** (was: "GAP-E does not close / z₃ unforgeable"; now KILLED, see banner + §SKEPTIC-#1)

> **RETRACTED.** The original verdict-up-front claimed GAP-E's top-zone bound is unforgeable from owned material and the residual `z₃` is unconstrained above 13. **This is false**: `scene_triple_unique` (row 530, CORE-FORMALIZED) forges `z₃ = 13` from an owned `+2` centred-Lucas window. GAP-E's top-zone **upper bound is OWNED, not open.** The paragraphs originally here are struck; the corrected residual is in §RES (also rewritten) and the full accounting is in §SKEPTIC-#1.

**Corrected standing (candidate, honest partial):** What this pass actually produced, once the false headline is removed:
1. **The top-zone bound is OWNED** (`z₃ = 13`, `scene_triple_unique`/`address_ladder`/`TOWER-STOP-NOEXT-001`). GAP-E's *upper-bound clause* is therefore **not** the open residual the memo took it to be.
2. **The empty-slot route (E-b) was the wrong instrument.** NEG-1's finding — that the empty-slot schema has no owned step-inventory that forges the bound — remains *arithmetically* correct, but is now re-read as: *the empty-slot schema is not how the bound is owned; `scene_triple_unique` owns it via a centred-Lucas-window uniqueness, a route the memo never checked.* NEG-1 is demoted from "located obstruction to closure" to "a note on why one particular instrument failed while another (owned) instrument succeeds."
3. **v17 phase-lock seed remains DEAD** on re-derivation (independent of the headline; §v17 stands).
4. **Genuinely open residual (if any):** NOT the top-zone size. See §RES-CORRECTED for the one narrow thing that may still be open (whether the `+2` top step / centred window is itself begged inside `scene_triple_unique` — a question the memo would have had to WIN to keep anything open, and did not even raise).

The forge fails at a specific, newly-pinned seam: the owned empty-slot pattern is a **"surplus-over-a-closed-inventory"** schema (both instances), and transferring it to junction steps requires an owned *closed inventory of junction addresses* against which a skipped address (13, when stepping 11→15) counts as a "significant but empty" slot. **No such inventory is owned; worse, the only owned enumerated index in the step domain (the Lucas layer index `n`) makes the owned ladder itself a skipping ladder** (9 and 13 are not Lucas layers; only 11 = L₅ is), so the pattern, if transferred literally, would fire against the owned tower. This is a stronger obstruction than "coined predicate": the natural owned material actively resists the transfer.

Honest partial gain (this is real, not a consolation): the parent memo's begging-point was stated as a *risk* ("close to assuming the ladder"). This memo **discharges it to a theorem-shaped negative** (NEG-1: the empty-slot schema is inventory-relative, and the step domain has no owned inventory), and extracts one genuinely new owned kill the parent memo did not have (the odd-step kill, §OWN-1), which narrows — but does not close — the residual family.

## What is genuinely OWNED after this pass (verbatim, file:line)

### OWN-1. The orientation argument kills EXACTLY the odd steps — in the Lucas index `n`, not in address value

`BOOK_01…md:1891-1899` (§01.22), verbatim (line range corrected per Skeptic #1 EoR-2: the quoted sentence begins at **1891**, not 1893; 1893-1897 is the math block, 1899 is the "So the sign…" prose):

> "In the discrete CORE world the powers `φ^n` are approximated by the integer Lucas numbers `L_n`, and the approximation defect carries an exact `Z₂`-orientation class: … `ε_n := φ^n − L_n = −ψ^n = (−1)^{n+1} φ^{−n}`. So the sign of the defect alternates with `n`: at `n=5` the holonomy parity is `+`, at `n=6` it is `−`. Now attempt a unit junction step `5 → 6`. The orientation/torsion class flips, and to splice the two layers across that flip one must supply an external orientation bit (an element of `Z₂`) that is **not** contained in the address itself. … The step `5 → 7` preserves the orientation class, so the splice closes with no exogenous parameter."

**Exact owned content (computed, script §I):** the defect parity is `(−1)^{n+1}`; a step `Δn` preserves parity **iff `Δn` is even**. The corpus *writes* only the `+1` attempt (`5→6`); the printed *mechanism* (parity flip ⇒ external sign bit ⇒ ⊥M1) then kills **every odd Δn** (`+1` written; `+3, +5, …` by the same mechanism extended — flagged as extension, not corpus-written) and is **silent on every even Δn ≥ 2** (`+2, +4, +6, …`, all preserve parity ⇒ ⊥ never reached). The word "minimal" in "the minimal admissible junction step is `+2`" (1899) is a **conclusion-word the printed argument does not reach**: it selects `+2` over `+4` with no ⊥-proof. This is the parent memo's F1/E-GE-2, now pinned to its exact domain (`Δn` parity, not address-value parity).

### OWN-2. The two owned empty-slot instances are BOTH "surplus-over-closed-inventory", not "skip-in-a-ladder"

**Instance A — role slots**, `BOOK_03…md:931-932` (§03.23.1), verbatim (line range corrected per Skeptic #1 EoR-1: the quoted string is at **931-932**; 926-930 hold different text — "The 4 is the minimal count of realizable roles…" and the `D_anchor < 4` bullet):

> "`D_anchor > 4`: empty address slots appear; to tell an empty slot from a significant one you must import an exogenous significance catalog. Banned."

The inventory it counts emptiness against is the **owned closed role alphabet {A,B,C,D}, |roles| = 4** (owned completeness: `BOOK_01 §01.7` operator-role table; `roles_card_four`, `CarrierForcing.lean`). Empty ⇔ `D_anchor` exceeds the owned count 4.

**Instance B — cycle steps**, `BOOK_01…md:1912-1913` (§01.22 cycle-normalization), verbatim:

> "`N > 9`: the cycle has 'empty' steps that correspond to no address. To tell an empty step from a significant one the cycle would need an external **catalog of significance**, which is `⊥M1`."

The inventory it counts emptiness against is the **owned closed address count `D = 9`** (the defect shell `V₉`, owned). Empty ⇔ `N` exceeds the owned count 9.

**Schema (both instances, exact):** given an owned finite inventory `I` of significant positions, a structure providing `k > |I|` positions produces `k − |I|` empty positions, distinguishable-from-significant only via an exogenous catalog ⇒ ⊥M1. **Emptiness is defined by exceeding a closed owned count. Neither instance is a "skipped step in a pre-laid ladder"; both are "too many positions for the owned inventory".**

## NEG-1 — the empty-slot transfer to junction steps FAILS (arithmetic intact; **closure-reading RETRACTED**)

> **DEMOTED (Skeptic #1).** The arithmetic below (the empty-slot schema has no owned step-inventory that is non-circular, contains 13, spares 12, and spares the owned rungs) is correct and preserved. **What is RETRACTED is the reading that this constitutes a "located obstruction to closure" implying `z₃` is open.** It does not: the top-zone bound is owned by a *different* instrument (`scene_triple_unique`'s centred-Lucas window), which the memo never checked. NEG-1 now reads as: "the empty-slot schema is the wrong instrument for this bound," not "the bound is unforgeable." Read every "the begging-point is NOT ownable" below as scoped to *the empty-slot route only*, which is not the route that owns the bound.

To forge E-b, the empty-slot schema (OWN-2) must apply to the claim "stepping 11→15 (a `+4`) skips address 13, and 13 is an empty-but-significant slot ⇒ exogenous catalog ⇒ ⊥M1." For the schema to fire, there must be an **owned closed inventory of junction addresses** `I_step` such that 13 ∈ `I_step` is "significant" and the `+4` step leaves it empty. Three attempts to supply `I_step` from owned material, each fails for a different owned reason:

- **Attempt (a): `I_step` = the address VALUES `{9, 11, 13}`.** Circular — this IS the ladder whose completeness is GAP-E. The begging-point in its bluntest form: to call 13 a "significant slot" you must already own that 13 is a rung, which is the conclusion. **Blocked (assumes the ladder).**

- **Attempt (b): `I_step` = the Lucas layer index `n`.** This is the ONLY owned enumerated index in the step domain (OWN-1: parity lives on `n`). But then "significant address" = "Lucas layer `L_n`", and among the owned rungs only `11 = L₅` is a Lucas number: `L_4 = 7, L_5 = 11, L_6 = 18, L_7 = 29` (computed, script §II). So `9` and `13` are **not** Lucas layers — under this inventory the OWNED ladder `9→11→13` is itself a non-Lucas, skipping walk. The schema, applied honestly with the only owned step-index, **fires against the owned tower**, not against `(9,11,15)`. **Blocked (kills the owned tower — the P_broad pathology of the parent memo §III, now reproduced in the step domain).**

- **Attempt (c): `I_step` = the integers ℤ (every even address is "significant").** Then 13 is significant, but so is EVERY odd/even value, and the schema would ban any step > +1 as "leaving significant slots empty" — including the owned `+2` step (11→13 skips 12). **Blocked (kills the owned step too, and contradicts OWN-1 which explicitly admits `+2`).**

- **Attempt (d) (added post-skeptic): `I_step` = the owned 9-position cycle** (`ν* = 1/9`, "9 distinguishable address positions", BOOK_01…md:1911). This is a genuinely owned closed enumerated inventory. But it has **exactly 9 positions and does not contain 13** — it cannot make 13 a "significant slot" at all. **Blocked (13 ∉ inventory ⇒ schema cannot even reference the skipped address).** This closes the skeptic's "you only checked three inventories" gap: the fourth owned enumerated set is also blocked, by a different owned fact (cardinality 9).

**The located obstruction (NEG-1, candidate):** the empty-slot schema is **inventory-relative**, and the step domain has **no owned closed inventory** that (i) is non-circular, (ii) contains 13 as significant, and (iii) does not also condemn the owned ladder or the owned `+2` step. Every owned candidate inventory either assumes the ladder, or fires against the owned tower, or bans the owned step. **The begging-point is therefore NOT ownable: it cannot be discharged by any owned inventory.** This is strictly stronger than the parent memo's "coined predicate" — the natural transfer does not merely lack an owner, it is actively **inconsistent with the owned tower** under the only two non-circular inventories available.

*Falsification/reopening hook for NEG-1:* produce an owned closed inventory `I_step` of junction addresses (a defined predicate "address `a` is a significant junction position") that contains 13, excludes 12 and 14 as non-positions (so `+2` is admissible but `+4` is not), and is not the ladder itself. The sweep of BOOK_00/01/03 for "junction" (script §II printout) found the word only at 1899, in the orientation argument, which enumerates over `n` — route (b), which self-refutes. If such an inventory is later minted, NEG-1 falls and E-b reopens as closable.

## OWN-3 — the odd-step kill (owned but non-discriminating) — **residual framing MOOT (post-KILL)**

> **DEMOTED (Skeptic #1).** OWN-3's arithmetic (the odd-step kill is non-discriminating on the even-spaced family) is fine, but its framing — "narrows the residual family `{(9,11,z₃): z₃ odd ≥ 13}`" — presupposes an open residual family that does not exist. `z₃ = 13` is owned; there is no `z₃ ≥ 15` residual to narrow. Read OWN-3 as: "the odd-step kill is owned but adds nothing," full stop.

OWN-1 is a real owned kill the parent memo did not credit as owned: **every odd address-index step is ⊥M1** by the printed parity argument. But the residual towers `(9,11,z₃)` with `z₃ > 13` all differ from 13 by an EVEN amount (`15 = 13+2, 17 = 13+4, …`) because base parity is fixed (9 odd, +2 to 11 odd, +2 to 13 odd — all rungs odd, so any admissible `z₃` is odd, forcing `z₃ − 11` even). So OWN-1 kills nothing in the residual family that survives OWN-1's own even-step admission. **Net: OWN-1 is owned but non-discriminating on the residual** (it re-confirms the family is even-spaced, which the parent memo already had). The residual is unchanged by promoting the odd-step kill to owned. Reported for completeness and to forestall an over-credit (ATT-C below).

## v17 KILL-SKETCH RE-DERIVED FROM SCRATCH — "larger gaps introduce rational phase-locking"

The parent memo (F2) names this as the one unmined E-b lead, and flags that its cited cert `vp_minimal_holographic_carrier.py` is a phantom (git-verified absent — re-confirmed this pass: `git log --all -- '*minimal_holographic_carrier*'` empty, `find` empty). So it must be re-derived from scratch, owning nothing from the phantom. Attempt (script §III):

The one owned periodic structure is the cycle normalization `ν* = 1/9`, `40° = 2π/9` (BOOK_01:1918-1922, owned CORE-FORCING). A junction step `+g` between address-cycles of sizes `d` and `d+g` phase-locks iff the combined return is rational with small denominator. Computed for the owned welds (`q_T = lcm(4, V₁₁)`): stepping to the OWNED `z₃ = 13` gives `lcm(4,11) = 44`, `φ(44) = 20 = d₁₃` (owned weld). Stepping to `z₃ = 15`: `lcm(4,11) = 44` **unchanged** (the weld `q_T` reads `V₁₁ = 11`, never `z₃` — reproduced from parent §V, R2-dead). So the "larger gap" does NOT change the phase-lock quantity that is owned; the phase-lock story would need a weld that reads `z₃`, and **no owned weld reads `z₃`** (script §III exhaustively lists the §01.22 welds and their inputs; `z₃` appears in none). 

**Verdict on the v17 seed (candidate): DEAD on re-derivation.** "Larger gaps introduce rational phase-locking" has no owned computational content — the owned phase quantities (`44, φ(44)=20, 710, 113, ν*=1/9`) are all functions of `{4, 9, 11}` and the operator count, none of `z₃`. The v17 sketch is not merely uncited (phantom cert); it is **non-reconstructible from owned periodic data**. This closes the last named E-b lead as a dead end and REMOVES it from the follow-up queue (was rank-3 in the parent memo).

## RES — **RETRACTED** (the "unconstrained above 13 / unforgeable by either route" residual is false)

> **RETRACTED IN FULL.** Every claim in the original §RES that `z₃` is "unconstrained above 13," that the top-zone bound is "UNFORGEABLE from current owned material by either named route," and that the residual family is `{(9,11,z₃) : z₃ odd, z₃ ≥ 13}` "one free odd parameter, unbounded" is **FALSE**. The top-zone value is **forced to 13** by `scene_triple_unique` (row 530). The family `(9,11,15), (9,11,17), …` is not a residual; each such tower violates the owned `+2` centred-Lucas window (`hladder₂ : z₂ = z₁+2`, `SceneTripleUnique.lean:78`; `address_ladder`, `CarrierForcing.lean:81`). The paragraphs originally here are struck.

## RES-CORRECTED — what actually stays open (candidate; honest, may be nothing at the headline)

- **Top-zone SIZE: OWNED, not open.** `z₃ = 13` is forced. There is no free odd parameter. GAP-E's upper-bound clause is discharged by `scene_triple_unique` + `address_ladder` + `TOWER-STOP-NOEXT-001`.

- **v17 phase-lock seed: DEAD** (independent of the retraction; §v17 stands as a genuine dead-end result).

- **The ONE narrow question the memo would have needed to WIN to keep anything open (raised now, NOT resolved, NOT claimed as open):** does `scene_triple_unique` **beg** its own `+2` top step? Its statement takes `hladder₂ : z₂ = z₁ + 2` as a *hypothesis*. If that `+2` top step were an unowned assumption smuggled into the theorem, a `+4` top step (`11→15`) might live outside its scope. **But this escape is not available**, because the `+2` step is separately owned:
  - `address_ladder` (`CarrierForcing.lean:81`) proves `11 + 2 = 13` by `decide` — the top rung is pinned, not hypothesised;
  - the orientation/holonomy-parity argument at `BOOK_01:1889-1899` (this memo's OWN-1 source) is the owned derivation that "the address ladder is forced to advance by `+2`, never `+1`" (`BOOK_01:1889`, verbatim). The memo cited this as OWN-1 while its headline denied the very bound it establishes.
  So a won beg-the-top-step attack is **not on the table** from current owned material: the `+2` centred window is owned, and a `+4` top step breaks it rather than inhabiting an owned gap. **Absent a won beg-the-top-step argument (which the memo never even mounted), the top-zone bound is OWNED and this residual is empty at the headline.**

- **Residual statement (corrected, candidate):** *GAP-E's top-zone upper bound is **owned** (z₃ = 13, `scene_triple_unique`). The only conceivable reopening is a future proof that `scene_triple_unique` begs its `+2` top step (`hladder₂`) — but that step is itself owned by `address_ladder` and the `BOOK_01:1889` orientation forcing, so the reopening hook requires overturning an owned CORE-FORMALIZED theorem, not filling an empty slot.* This is mint-or-motion-ready as a **negative housekeeping note** (the empty-slot route is not the instrument that owns the bound), NOT as a new forcing.

## E-a note — **MOOT (post-KILL)**: there is no top-zone-size closure left to reach

> **DEMOTED (Skeptic #1).** This whole note, and the "E-a is the strictly better follow-up route" re-ranking below, presupposed the top-zone bound is OPEN and needs a closure route. It is NOT open — `scene_triple_unique` owns it. E-a is therefore **not** a route to close a top-zone-size gap, because that gap does not exist. The primitivity-seed reading below is retained only as a note on the branch-equation domain; it is **not** a live closure lead for GAP-E's upper bound.

`BOOK_01…md:491` / `BOOK_02…md:670`, verbatim (BOOK_02):

> "`p+p^k=1` with `k>2` is not primitive: it contains the quadratic return plus additional unresolved iterations, hence extra hidden memory before halt."

This is a genuine owned **decomposability-rejection** principle in the branch-equation domain: a composite "contains" a smaller resolved object plus surplus, and the surplus is unowned/hidden ⇒ excluded. It is exactly the shape E-a(ii) needs ("`6 = 2 ⊔ 4` contains D₂ plus surplus"). **But (this pass's finding) using it for capacities is the identical unowned transfer NEG-1 blocks for E-b:** the principle is owned about *iterated branch powers `p^k`*, not about *zone-extension composites*, and no owned text licenses the move from "return-iteration composite" to "capacity-size composite". Deploying it would be coining a transfer, not owning one. So E-a stays a candidate (parent memo's status), not upgraded here.

*One asymmetry worth recording (candidate lead, NOT a closure):* the E-a primitivity transfer is **less** self-refuting than E-b's. E-b's transfer fires against the owned tower under its only non-circular inventory (NEG-1(b)); E-a's primitivity, if transferred, would kill `6` and `8` (composites) while sparing `2` and `4` (primitive) — i.e. it does not obviously fire against the owned extensions. So of the two routes, **E-a is the strictly better follow-up target** after this pass (reversing the parent memo's cost ranking, which put E-b first). The blocker is the same *kind* (unowned transfer) but E-a's transfer at least survives the anti-fit control (§III P_narrow residue), whereas E-b's does not survive NEG-1. This is the one place the cost ranking should move.

## Named risks & PRE-REGISTERED attack surface

- **ATT-A (strongest, pre-registered — the begging-point turned on ME): "NEG-1(b) is itself a coined inventory, so your 'located obstruction' is as coined as the thing you're refuting."** Confronted head-on: NEG-1 does NOT claim the Lucas-index inventory is THE owned inventory; it claims the OPPOSITE — that the *only owned enumerated index in the step domain* (which the owned orientation argument itself uses, 1899) yields a self-refuting inventory, and that the other two candidates are circular or over-broad. The strength of NEG-1 is that it is an EXHAUSTION over the owned candidates (a, b, c), each blocked by an owned fact, not a positive claim that any one of them is correct. If the skeptic produces a FOURTH owned inventory not in {values, Lucas-n, ℤ} that is non-circular, contains 13, excludes 12, and does not condemn the owned ladder — NEG-1 falls and E-b reopens. The reopening hook is stated. This is a real forcing of the negative, failable exactly there.

- **ATT-B: "the odd-step kill (OWN-1) is over-credited as owned."** Guarded: OWN-1 is credited only as "the printed ⊥-proof reaches odd Δn"; §OWN-3 explicitly records it is NON-discriminating on the residual (all residual towers are even-spaced already). If the skeptic strips OWN-1 to "narration only" (arguing the `n`-vs-address domain confusion voids even the odd-step kill): the residual is UNCHANGED (script §IV prints identical family with and without OWN-1). Costless attack, pre-absorbed.

- **ATT-C: "n-vs-address is a strawman; the corpus means +2 in address value, and everyone knows it."** Answer: precisely — the corpus MEANS address value, but PROVES over Lucas `n` (1893-1899 is entirely in `n`; `L_n` parity), and the two coincide only at `n=5 ↔ 11`. The domain gap is not my invention; it is the exact reason the printed argument reaches only parity (odd/even) and not "minimal". If the skeptic supplies an owned address-value orientation argument (not routed through `L_n`), OWN-1 strengthens and possibly E-b's route (b) gains a non-Lucas inventory — welcomed, would reopen. Sweep found none (only 1899 carries the parity argument, and it is `L_n`-based).

- **ATT-D: "v17 phase-locking dead-derivation is premature — you only checked `q_T`."** Guarded: script §III lists ALL owned §01.22 weld inputs (`q_T=lcm(4,V₁₁)`, `m_T`, `φ(q_T)`, `q_EW`, `m_EW`, `φ(q_EW)`, `ν*=1/9`, `B=5`, `L`) and checks each for `z₃`-dependence; NONE reads `z₃` (all functions of `{4,9,11, |Ω₈|=8, operator-count}`). The dead-derivation is an exhaustion over owned periodic quantities, printed. If an owned weld reading `z₃` is produced, the seed reopens.

- **ATT-E: fork-mixing (inherited).** This memo works the CONSECUTIVE fork (E-b's home, F3-consecutive). It does NOT identify it with the over-base fork. NEG-1 is stated for the consecutive/step reading; the over-base/capacity reading is E-a, handled separately and NOT closed. No cross-fork identification is asserted (trap d/i/j).

## Lean sketch (code block only — NOT added to the built tree; a DRAFT of what E-b WOULD need, showing the unfillable hole)

```lean
-- DRAFT ONLY. Illustrates the hole NEG-1 pins: `SignificantJunctionAddr` has no owned instance.
-- Do NOT add to 09_LEAN_FORMALIZATION; this is documentation of the missing object.
namespace D0.GapE.Draft

/-- The empty-slot schema, abstracted from OWN-2 (both owned instances). -/
def SurplusOverInventory (I : Finset ℕ) (k : ℕ) : Prop := k > I.card
-- ⊥M1 fires when SurplusOverInventory holds (exogenous catalog needed). OWNED.

/-- The UNOWNED object E-b needs: a closed inventory of significant junction addresses. -/
class SignificantJunctionAddr where
  I_step : Finset ℕ
  contains_13 : (13 : ℕ) ∈ I_step        -- needed so +4 (11→15) leaves 13 empty
  excludes_12 : (12 : ℕ) ∉ I_step         -- needed so +2 (11→13) leaves nothing empty
  not_the_ladder : I_step ≠ {9, 11, 13}   -- non-circularity (NEG-1(a))
-- NEG-1 (arithmetic, intact): NO owned term inhabits `SignificantJunctionAddr`.
--   • {9,11,13} violates not_the_ladder.
--   • {L_n} = {…,7,11,18,29,…} violates contains_13 (13 ∉ Lucas) AND admits 9,13 ∉ ⇒ kills owned tower.
--   • ℤ (all) violates excludes_12 ⇒ kills owned +2 step.
-- *** RETRACTED CONCLUSION (Skeptic #1, 2026-07-05): the ORIGINAL comment here said
--     "Therefore E-b's forcing z₃ ≤ 13 is unprovable; its key premise class is uninhabited."
--     THIS IS FALSE. z₃ ≤ 13 (indeed z₃ = 13) IS proved from owned data by a DIFFERENT
--     construction that needs NO SignificantJunctionAddr: scene_triple_unique
--     (SceneTripleUnique.lean:74-85) forces it from a +2 centred-Lucas WINDOW, and
--     address_ladder (CarrierForcing.lean:81) pins 11+2=13. The empty-slot premise class
--     being uninhabited says only that ONE instrument fails, not that the bound is unforgeable.
-- The correct owned forcing (already registered, row 530) — reproduced as reference:
--   theorem scene_triple_unique (z₀ z₁ z₂ n : ℕ)
--     (hladder₁ : z₁ = z₀ + 2) (hladder₂ : z₂ = z₁ + 2)
--     (hcentre : z₁ = lucas n) (hlo : 9 ≤ z₁) (hhi : z₁ ≤ 13) :
--     (z₀, z₁, z₂) = (9, 11, 13)
-- i.e. z₂ (the top zone) = 13 is FORCED. The memo's hole was looking in the wrong place.

end D0.GapE.Draft
```

## Registry proposal — **RETRACTED / CORRECTED** (in-memo only — NO csv edit)

> **RETRACTED.** The original proposal asserted GAP-E "stays OPEN" with "upper bound underdetermined by one clause." That is false; the top-zone upper bound is owned.

**Corrected proposal (candidate, in-memo only — NO csv edit):**
- Do **not** carry GAP-E's *top-zone upper-bound clause* as open. It is discharged by `scene_triple_unique` (row 530, CORE-FORMALIZED), `address_ladder` (row 215), `TOWER-STOP-NOEXT-001` (row 257). If the parent memo's W-HI.2 (GAP-E) row was tracking the top-zone size as underdetermined, that sub-claim should be marked **RESOLVED-BY-EXISTING-ROW** (a duplicate of the already-registered forcing), pending a maintainer's confirmation that the parent memo's GAP-E scope is exactly the top-zone size and not some other completeness clause.
- **Pre-flight failure to record:** this memo's pre-flight (`preflight.sh "junction step minimal no-skip empty slot"`) searched the wrong keyword set and missed the owning row. A corrected pre-flight would key on `scene_triple_unique`, `unique_lucas_in_window`, `address_ladder`, `centred window`, `Lucas window` — which surface row 530/215 immediately. This is the mechanical reason the memo went wrong (see errors of record, §SKEPTIC-#1 EoR-4).
- v17 phase-lock seed: DEAD (this survives; may be recorded as a closed dead-end lead).

## What this pass does and does NOT show — **CORRECTED (post-KILL)**

> **RETRACTED** the original bullets' claim that GAP-E is "OPEN at the owned-formal layer at exactly one coordinate (`z₃`)" with "both candidate closure routes … unowned." The top-zone coordinate `z₃` is **not** open; it is forced to 13 by an owned CORE-FORMALIZED theorem.

- **What this pass ACTUALLY produced (net, after the KILL):** (i) a re-derived **DEAD** verdict on the v17 phase-lock seed (survives, genuine dead-end); (ii) a correct but mis-framed empty-slot analysis (NEG-1), now re-read as *"empty-slot is the wrong instrument"*; (iii) two citation-line corrections (EoR-1, EoR-2); (iv) a corrected pre-flight keyword set that would have surfaced the owning row (EoR-4); (v) a check script upgraded with an owned-forcing KILL control (§VII).
- **What this pass FAILED to do:** it declared the top-zone bound unforgeable **without checking the registry for a forcing of it**, and an owned one (`scene_triple_unique`, row 530) existed the whole time. It never cited `scene_triple_unique`, `unique_lucas_in_window`, `address_ladder`, or `TOWER-STOP-NOEXT-001`, despite opening `CarrierForcing.lean` (whose line 81 proves `11+2=13`). This is the KILL.
- **Owned-formal standing (corrected):** the `(9,11,13)` tower is **owned** at all three coordinates — base 9, centre 11 (`unique_lucas_in_window`), top 13 (`scene_triple_unique`/`address_ladder`). There is **no open coordinate**. The narration guards noted in the parent memo are a separate (narration-layer) matter and are untouched by this pass.
- **Unchanged:** no registry row, cert, or built Lean file edited; the two forks not identified.

## SELF-SKEPTIC (pre-#1, self-adversarial pass) — **SUPERSEDED / WRONG VERDICT; see §SKEPTIC-#1 below**

> **This block is the memo's OWN self-skeptic pass, which concluded "SURVIVES." It was WRONG** — it never checked the registry for an owned forcing of the bound (the fatal miss). It is retained unedited below as the record of the error. The binding verdict is the independent **Skeptic #1 = KILLED**, logged in **§SKEPTIC-#1** immediately after this block. Do not read "SURVIVES" here as operative.

**Overall (SUPERSEDED — WRONG): NEG-1 SURVIVES as a located obstruction; the honest-underdetermination-sharpened verdict STANDS. Three wounds repaired (scope narrowings + one added inventory); no kill.** Script re-run after repairs: 39/39 PASS, rc=0 (count printed by the script's own counter, not hand-tallied — E1 discipline).

- **W-CE-1 (headline over-scope) — REPAIRED.** Original headline "the begging-point is NOT ownable" over-claimed: NEG-1 kills the *empty-slot route* to E-b, not *all conceivable routes*. Narrowed in the verdict-up-front scope box and in RES. The empty-slot route is exactly the one the charter and parent memo named as the E-b material, so the narrowing does not weaken the task-relevant result; it makes the claim exactly co-extensive with the owned material attacked.
- **W-CE-2 (inventory exhaustion incomplete) — REPAIRED.** Original NEG-1 checked three inventories {values, Lucas-n, ℤ}. Added the fourth owned enumerated set — the 9-position cycle `ν*=1/9` (BOOK_01:1911) — blocked by cardinality (13 ∉ a 9-set). Exhaustion is now 4-way over every owned enumerated index in the step/address domain. Script §V updated; the located-obstruction check is now 4-way.
- **W-CE-3 (+3/+5 over-credit) — REPAIRED.** The corpus writes only the `+1` attempt (`5→6`). OWN-1 now credits "+1 corpus-written; +3/+5 by the same parity mechanism extended" — labelled as mechanism-extension, not corpus-text. Script §I labels renamed ("printed MECHANISM kills"). Does not affect the load-bearing fact (silence on +4).

**Attacks that did NOT land (recorded for the next skeptic):**
- The `n`-vs-address domain reading (OWN-1/ATT-C) was probed hardest. Verified: BOOK_01:1893-1899 computes parity on the Lucas index (`ε_n=(−1)^{n+1}φ^{−n}`, evaluated at n=5,6), and `5→7` in `n` maps to `L₅=11 → L₇=29`, NOT to `11→13`. So the parity argument, taken literally in its own domain, does not even reach the address-value `+2` step cleanly — which **strengthens** NEG-1 (the owned step-forcing is domain-confused, giving even less owned traction for a junction-address inventory). Recorded as a strengthening, not folded into the load-bearing count to avoid over-reach.
- R2-death / v17-seed-death: the exhaustion over owned weld inputs (script §III) was re-checked for a `z₃`-reading weld; none. No new owned periodic quantity surfaced. SURVIVES.

**Net after repairs (SUPERSEDED — WRONG):** E-b (empty-slot route) CLOSED as unforgeable and self-refuting under owned inventories; v17 phase-lock seed DEAD; E-a re-ranked as the sole surviving candidate route (still blocked at an unowned but anti-fit-consistent transfer); residual = the odd `z₃ ≥ 13` family, one free parameter. GAP-E stays OPEN at the owned-formal layer; the WHY is now sharp. *(Every clause of this "Net" except the v17-DEAD clause is FALSE — see §SKEPTIC-#1.)*

---

## SKEPTIC #1 verdict + repair log (INDEPENDENT pass, ACCEPTED IN FULL, no defense) — 2026-07-05

**VERDICT: KILLED.** Accepted in full. No defense mounted. The load-bearing headline ("GAP-E's top-zone upper bound is unforgeable from owned material; `z₃` unconstrained above 13; both candidate closure routes require an unowned domain-transfer") is retracted. An owned, Lean-proved (0 sorry, rc=0), cert-backed, CORE-FORMALIZED forcing of `z₃ = 13` exists and is registered.

### Strongest finding (the named second object)

`D0.VNext2.SceneTripleUnique.scene_triple_unique` — registry `CLAIM_TO_LEAN_MAP.csv:530`, status CORE-FORMALIZED / LEAN_PROVED, cert `05_CERTS/vp_scene_triple_unique.py` (rc=0), narrated `BOOK_01:1502` (§01.19a capstone), proved at `SceneTripleUnique.lean:74-85` — proves that **any `+2` ladder `(z₀,z₁,z₂)` whose centre `z₁` is a Lucas number in `[9,13]` is UNIQUELY `(9,11,13)`**, via `unique_lucas_in_window` (`SceneTripleUnique.lean:59`) forcing `z₁ = 11`, hence top zone `z₂ = 13`. This is an OWNED forcing of exactly `z₃ = 13`, directly falsifying the memo's headline. The memo never cited it, `unique_lucas_in_window`, `TOWER-STOP-NOEXT-001`, `address_ladder`, or the `BOOK_01:1502` capstone — despite opening `CarrierForcing.lean` (memo cited `roles_card_four` from that file), whose line 81 Lean-proves `address_ladder: 11+2=13`.

### Why the ONLY structural escape does not survive

The memo's residual uses a NON-uniform step (`9 →+2→ 11 →+4→ 15`), whereas `scene_triple_unique` takes `hladder₂ : z₂ = z₁ + 2` (a uniform `+2` top step) as a hypothesis. The only way to keep a residual open was to (a) cite the three owned rows and (b) mount and WIN an argument that they BEG the `+2` top step (i.e. that `z₂ = z₁+2` is an unowned assumption inside them). **The memo does neither.** And the escape is not available anyway: the `+2` top step is separately owned — `address_ladder` (`CarrierForcing.lean:81`) pins `11+2=13`, and `BOOK_01:1889` states the ladder "is forced to advance by `+2`, never `+1`." The construction is a `+2`-SYMMETRIC window centred at the forced centre 11 (`unique_center_in_window`), so a `+4` top step **breaks the owned window** rather than living in an owned gap. Absent a won beg-the-top-step attack, GAP-E's upper bound is OWNED, not open; the memo's premise collapses.

### Repairs APPLIED (this pass)

1. **FATAL / structural — headline retracted and re-scoped.** Added a top-of-memo RETRACTION BANNER; rewrote VERDICT-UP-FRONT, §RES→§RES-CORRECTED, the registry proposal, the Lean-sketch comment, and "What this pass does/does NOT show." NEG-1's arithmetic is preserved but demoted to "the empty-slot route is the wrong instrument"; its closure-reading is retracted. Every "unforgeable / unconstrained / open at `z₃`" assertion is struck and corrected.
2. **Engaged the three owned rows head-on.** The banner and §RES-CORRECTED now cite `scene_triple_unique` (row 530), `address_ladder` (row 215), `TOWER-STOP-NOEXT-001` (row 257) verbatim, and confront the only escape (non-uniform `+4` step), showing it fails because the `+2` window is itself owned. The memo did NOT win a beg-the-top-step argument (it did not even raise one), so the escape is unmade; this is recorded honestly, not defended.
3. **Citation-line audit (EoR-1, EoR-2) — both fixed.** See errors of record below.
4. **Script control (§VII) added.** `gap_e_close_check.py` now encodes the owned `scene_triple_unique` forcing (`scene_triple_unique_model`) and a KILL control that FAILS the memo's headline; NC1 annotated as redundant with §II (not an independent control); top docstring records the KILL. Re-run: **45/45 PASS, rc=0, VERDICT: KILLED** (the sub-facts I–VI are arithmetically intact; §VII proves the CONCLUSION they supported is false). Verified by the script's own counter, not hand-tallied.

### Errors of record (enumerated, no defense)

- **EoR-0 (FATAL, the KILL):** the memo declared `z₃ ≤ 13` "UNFORGEABLE from current owned material" and `z₃` "unconstrained above 13," while an owned CORE-FORMALIZED / LEAN_PROVED theorem named `scene_triple_unique` (row 530) forges exactly `z₃ = 13`. The bound was already forged and registered. The class the memo declared uninhabited has a named inhabitant.
- **EoR-1 (citation line, integrity-grade):** §OWN-2 Instance A cited `BOOK_03…md:926-930` for the verbatim string "`D_anchor > 4`: empty address slots appear; …". That string is at `BOOK_03:931-932`; lines 926-930 hold different text ("The 4 is the minimal count of realizable roles…" and the `D_anchor < 4` bullet). Quote verbatim-correct, line range wrong. **FIXED → 931-932.**
- **EoR-2 (citation line):** §OWN-1 cited `BOOK_01…md:1893-1899` and quoted "In the discrete CORE world the powers `φ^n` are approximated by the integer Lucas numbers `L_n`…". That sentence begins at `BOOK_01:1891`, not 1893 (1893-1897 is the math block, 1899 is the "So the sign…" prose). **FIXED → 1891-1899.**
- **EoR-3 (script scope):** `gap_e_close_check.py` section V (`inventory_ok`, line ~238-254) is genuinely failable and does NOT smuggle (e.g. `{9,11,13,15}` passes it), but it exhausts only FOUR hand-curated inventories and tests the WRONG universe — it never encoded the `+2`-symmetric centre-Lucas window (`scene_triple_unique`) that actually owns the top-zone bound. A green 39/39 therefore did NOT license the CONCLUSION. **FIXED:** §VII added (owned-forcing control); verdict now KILLED.
- **EoR-4 (redundant control):** NC1 (script, formerly lines 266-269) hardcodes `closing_inv={9,11,13}` and reuses "13 not Lucas" from §II — it is redundant, not an independent control. **FIXED:** NC1 annotated as redundant; the real control is §VII.
- **EoR-5 (process, pre-flight miss):** the pre-flight keyword set `"junction step minimal no-skip empty slot"` did not surface the owning row 530. A corrected pre-flight keyed on `scene_triple_unique / unique_lucas_in_window / address_ladder / Lucas window / centred window` surfaces rows 530 and 215 immediately. Recorded as the mechanical cause; corrected-pre-flight noted in the registry-proposal section.

### Leads extracted from the KILL (for the record; NOT reopened claims)

- **Lead-1 (housekeeping):** the empty-slot schema (OWN-2) is genuinely NOT the instrument that owns the top-zone bound; the centred-Lucas-window uniqueness is. Useful negative note for anyone re-attacking completeness clauses: check `scene_triple_unique` FIRST.
- **Lead-2 (v17 DEAD survives):** the v17 "larger gaps ⇒ rational phase-locking" seed is dead on re-derivation, independent of the KILL — no owned weld reads `z₃`. This is a genuine closed dead-end and may be recorded as such.
- **Lead-3 (the only conceivable reopening):** a future proof that `scene_triple_unique` begs its `+2` top step (`hladder₂`) — but that step is owned by `address_ladder` + `BOOK_01:1889`, so reopening requires overturning an owned CORE-FORMALIZED theorem, not filling an empty slot. Not a live lead; recorded for completeness.

### Residual after the KILL

- **Top-zone size:** OWNED (`z₃ = 13`). Not open. Nothing to mint here — the bound is already registered (row 530).
- **v17 seed:** DEAD (may be recorded as a closed dead-end lead — mint-or-motion-ready as housekeeping only).
- **Mint-or-motion-ready:** nothing new is forcing-ready from this pass; the only motion-ready items are (i) the citation/pre-flight corrections above and (ii) an optional registry housekeeping note that GAP-E's top-zone-size sub-clause is a duplicate of the already-registered row 530 (maintainer confirmation required; NO csv edit made here).
