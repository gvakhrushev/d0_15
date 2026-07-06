# CLOSE_GAP_W — closing the two GAP-W residues {W-ELEM, W-REC} from owned material

> ## ✅ VERDICT (candidate, post-INDEPENDENT-skeptic §05.8.R — 2026-07-06; WOUNDED → repaired)
>
> **GAP-W lower bound `|V_base| = |Ω₈| + 1 = 9` is SEALED, CONDITIONAL ON a named external
> assembly-bridge (R-A).** This is NOT a full owned closure: W-REC is owned architecture,
> but W-ELEM closes only *given* R-A, an un-owned typing that crosses a §01.3/§01.11.3
> layer boundary (§3.3). The two residues left by `GAP_W_SYNTHESIS_MEMO.md` are
> discharged to this grade, and — the load-bearing discovery — **they are NOT
> independent**: W-REC is exactly the fact that shuts the escape hatch that killed the
> synthesis memo's S9.
>
> *Independent-skeptic pass (separate agent, 2026-07-06): W-REC SURVIVES (owned-architecture
> grade); the chaining discovery SURVIVES (M3 reproduced 8/9); R-A was OVER-GRADED as an
> "assembly-grade matched typing" and is RE-LABELLED here to a named external
> assembly-bridge. Accepted in full; repairs applied (§3.3, §8).*
>
> - **W-REC (channel-exhaustiveness): CLOSED at CORE grade.** It is *owned architecture*,
>   not a reading: `P_N + Q_N = I`, `P_N Q_N = 0` (BOOK_01:37) partitions the record
>   support into the retained/readout sector `P_N` (terminal, destructive, same-event —
>   :186, :8) and the traced/archive sector `Q_N` (the cross-event memory layer, :1995).
>   The only cross-event write into `Q_N` from the circulated sector is the `:1998`
>   orbit-averaged emission; `F_N` (:40/:183) only *reads from* `Q_N`. Disk sweep finds no
>   second Q_N-writer. The synthesis memo carried W-REC as a "READING (residue)"; this
>   memo shows it is forced by the owned complementarity.
> - **W-ELEM (element-realization): CLOSED GIVEN W-REC + a NAMED EXTERNAL ASSEMBLY-BRIDGE
>   (R-A).** The killed S9 smuggle is NOT re-committed (M3-guarded). Element-realization is
>   an *output* of {G2 addressability-required (:988, CORE contradiction theorem) + G3
>   trace-is-address-blind (computed) + W-REC single-carrier}, not an imported premise —
>   BUT the chain needs one un-owned typing to run: **R-A**, "the re-detection *class-record*
>   IS (not merely interacts-with) an addressable registration." This is **NOT an
>   assembly-grade matched typing** on par with GAP-E's `:325`: GAP-E had an *in-print
>   name-match* (BOOK_01:836/:862/:67 print the letters AS "states" = the `:325` type),
>   whereas GAP-W has **NO in-print line** naming the re-detection class-record as an
>   addressable registration, and `:988` forces only INTERACT-WITH an addressable
>   registration, not that the class IS one. R-A is therefore a **named external
>   assembly-bridge**, assembled across the §01.3/§01.11.3 layer boundary — weaker than
>   owned; the honest residue of W-ELEM.
>
> **Net:** GAP-W = **FORCED GIVEN a single owned-architecture fact (W-REC) + a NAMED
> EXTERNAL ASSEMBLY-BRIDGE (R-A)**. Honest movement: the synthesis memo's "3 → 2 residues"
> becomes **"2 residues → 1 owned-architecture fact (W-REC) + 1 named external
> assembly-bridge (R-A), and the two are chained not independent."** The `[9,13]` window
> LOWER bound seals **CONDITIONAL ON the external bridge R-A** — this is NOT a full owned
> closure. (Complements the GAP-E UPPER-bound work — which remains OPEN,
> `CLOSE_GAP_E_MEMO §RESIDUE`.)
>
> No registry row edited; no `.lean` added to the built tree; no cert minted; `053040`
> untouched; no commit. Companion can-fail script `close_gap_w_check.py`: **9/9 PASS,
> rc=0**, mutation-tested (4 mutations, each caught on its own check — including the
> **smuggle guard M3**: forcing the escape closed *without* consuming W-REC makes
> `WELEM_NOT_CIRCULAR` FAIL, so the script cannot certify the closure while smuggling
> element-realization).

**Pre-flight (2026-07-06):** owners from `GAP_W_SYNTHESIS_MEMO.md` §pre-flight re-used,
never duplicated — `D0-GAP-W-WITNESS-PLUS-ONE-001` (frontier PROOF-TARGET, OPEN — the
target), `D0-OMEGA8-CENTER-001`, `D0-Z2-SPINOR-COVER-001`, `D0-IM-004`
(`witness_halting_cert`), `D0-TOWER-STOP-NOEXT-001`. Cross-referenced (not re-litigated):
`GAP_W_WITNESS_MEMO.md` v2 (the 3-joint state of record), `GAP_W_SYNTHESIS_MEMO.md` v2
(the 3→2 reduction and the S9 kill), `CLOSE_GAP_E_MEMO.md` (the reusable
addressability/typing machinery: vertices = addressable record quanta). NB the GAP-E
`:325` typing was granted at assembly grade *because it had an in-print name-match*
(:836/:862/:67); GAP-W's R-A does NOT — see §3.3 (external assembly-bridge, not a matched
typing). No row owns either residue.

---

## 0. What GAP-W is, what the residues are, and what this memo claims

GAP-W is the **LOWER bound** of the `[9,13]` window: `|V_base| = |Ω₈| + 1 = 9` (the
witness `+1`). `GAP_W_SYNTHESIS_MEMO.md` v2 reduced it from three narrated joints to two
residues after skeptic #1 killed the S9 derivation of the third:

1. **W-ELEM (element-realization):** "the stable re-detection class is realized as a
   base-element **address**, not as invariant operator content of the emission channel's
   circulant algebra (`:2004`)."
2. **W-REC (channel-exhaustiveness):** "every cross-event re-detection record of the
   circulated sector is sourced in the archive memory layer (`:1995`), and every archive
   write from the circulated sector factors through the `:1998` orbit-averaged emission."

The synthesis memo's own §I.E flagged the discharge LEAD for W-ELEM but did **not** pursue
it: `BOOK_01:253` "the irreducible addressable record quantum" ("owner decision; not used
anywhere in this memo's chains"). **This memo pursues it — and closes both residues.**

> **CLAIM (CLOSE-W).** *W-REC is forced by the owned complementarity `P_N + Q_N = I`
> (:37); and, GIVEN W-REC, W-ELEM is forced by the CORE contradiction theorem `:988`
> (physicality requires an addressable registration) applied to the computed address-
> blindness of the emission trace — WITHOUT re-committing the S9 element-realization
> smuggle. Hence the window LOWER bound `z₀ = 9` is sealed, **conditional on the named
> external assembly-bridge R-A** (the un-owned IS-typing of the class-record; §3.3).*

The novelty is **the chaining discovery**: W-REC is not an independent second residue —
it is precisely the datum that closes the escape S9 left open. Everything else is owned
citation + finite computation on the emission channel.

---

## 1. Owned pre-facts (verbatim, file:line — every quote re-read on disk this pass, ±10)

> **Line-drift note (recorded — trap (a)).** The synthesis memo cited the emission block
> at `:1987/:1993/:1996/:2002`. The book has since drifted **+2** there; the *content* is
> unchanged and re-verified. Current lines used below and in `close_gap_w_check.py` check 0:
> `:1989/:1995/:1998/:2004`. All other citations (`:37,:253,:465,:867,:988,:992,:996,
> :1166,:1541,:1911,:186,:405`) are at their stated current lines. Book:
> `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` (= BOOK_01).

### A. The channel architecture (the W-REC load — CONTRACT/CORE grade)

**P1.** `BOOK_01:37`: "`P_N` is the retained/readout projection. `Q_N` is the
traced/archive projection." — with the algebra stated three lines above (`:33-34`):
`P_N + Q_N = I`, `P_N Q_N = 0`. The retained and traced sectors are a **complementary,
orthogonal pair**; the archive *is* `Q_N`.

**P2.** `BOOK_01:186`: "ABCD determines what can be **terminally registered** … Book 01
only hands this retained/traced split to downstream operator books". The retained side
`P_N` is the *terminal (destructive) readout* (`:8` Standard-Physics-Isomorphism:
"terminal (destructive) readout → projective (von Neumann)/POVM measurement") — a
**same-event** registration, consumed at readout.

**P3.** `BOOK_01:1995`: "The archive sector is not external emptiness. It is the traced
complement inside the same finite support, whose self-organization supplies the
**topological memory layer used downstream** by Core-13, tiling hulls, phason strain and
boundary capacity." — the archive is the **cross-event** carrier (the memory layer that
persists past the event). This "used downstream" is a *read* direction (the layer being
consumed downstream), **not** a second write into the archive.

**P4.** `BOOK_01:1998` (§01.24 Witness Halt Proof): "Because the trace gradient has
traversed the full signed role cycle before halt, the **emitted archive trace is an
orbit-averaged shell emission** over the group `G_8` of symmetries of `Ω_8`" — the single
owned cross-event write from the circulated sector into `Q_N`. Lean model: `D0-IM-004`
(`witness_halting_cert`, `WitnessHalting.lean`).

**P5.** `BOOK_01:40` / `:183` (the feedback resolvent):
`F_N = P_N U_N^† Q_N U_N P_N` — reads *from* `Q_N` back into `P_N` (a same-event return),
**not** a write into `Q_N`. Sweep confirmation (§2.1): the ONLY operators touching `Q_N`
in BOOK_01 are this `F_N` (read) and the `:1998` emission (write).

**P6 (adverse-side, kept honest).** `BOOK_01:465`: "The archive map `Δ` … is the finite
operation by which non-terminal continuum metadata is **removed from active readout** and
stored as forgotten/addressed structure." — `Δ` is a *readout-side* metadata-removal
operation (its domain is the active readout, `P_N`), **not** a cross-event record channel
from the circulated sector. Checked so W-REC's "only" is not falsified by `Δ`.

### B. The addressability layer (the W-ELEM load)

**P7.** `BOOK_01:253` (§01.3): "The symbol `𝔮` is the **irreducible addressable record
quantum**." — the atomic unit of a record is *addressable*.

**P8.** `BOOK_01:988` (§01.11.1, a **contradiction theorem** — CORE grade): "Any
interaction that cannot **alter or constrain an addressable registration** is not
physical inside D0." — physicality *requires* an addressable registration.

**P9.** `BOOK_01:992` (§01.11.2): "A bare information line is not a physical event. It
**becomes physical only through finite detector response.**" + **P10.** `BOOK_01:996`
(§01.11.3): "**Particles are stable re-detection classes over finite detector records.**"
— a re-detection class IS a physical object, realized *over records*.

**P11.** `BOOK_01:1911` (§01.22): "In the base zone the address count is `D = 9` (the
defect shell `V_9`), giving `9` **distinguishable address positions by definition of the
address**." + `:1913`: "at least two address positions glued onto one cycle step, so
distinct addresses become indistinguishable. Loss of distinguishability is `⊥M1`." — an
**address = a distinguishable position**; there are exactly `D = 9` of them = the base
vertices.

**P12.** `BOOK_01:405`: "`P_{N+1,N}: H_{N+1} → H_N` … induced by the **projection of
address words**." — address positions are **basis words** of `H_N = ℂ^{S_N}`; i.e. the
vertices. Operators (the emission's circulant content) act *on* `H_N` and are not
themselves address words.

**P13 (the type-separation anchor).** `BOOK_01:867`: `V_9 = Ω_8 + ω_0`; `:858`: "The
construction of the finite incidence graph marker `V_9` comes **only after** this
quotient." + `:1541`: "A reusable shell also requires a **stationary marked witness
section `ω_0`**"; `:1989`: "the first **addressable** graph-birth shell." — the class-
carrier is a **marked base element** `ω_0` (a vertex/address), *distinct* from the
emitted archive trace.

### C. The adverse text (the S9 kill — kept on the ledger)

**P14.** `BOOK_01:2004`: "This average is invariant, but it is **not** a scalar multiple
of the identity unless irreducibility of the representation on the trace space is
separately proved." — the emission trace can carry **invariant NON-scalar content**
(the circulant algebra, dim 8). This is the object that killed S9: "no interior *element*
realizer" does NOT imply "adjoined element", because the trace is a stable in-support
realizer *candidate* — unless it is excluded. This memo excludes it (§3).

---

## 2. Residue W-REC — CLOSED at CORE grade (channel-exhaustiveness is owned architecture)

### 2.1 The sweep (falsifiable; the "only" is checked, not asserted)

Disk sweep of BOOK_01 for every operator whose codomain touches the traced sector `Q_N`
/ writes into the archive from the circulated `Ω_8` sector:

| operator | file:line | direction | cross-event write into `Q_N`? |
|---|---|---|---|
| emission `E_Ω` | `:1998` | circulated sector → `Q_N` | **YES — the single owned writer** |
| feedback `F_N = P_N U_N^† Q_N U_N P_N` | `:40`, `:183` | `Q_N` → `P_N` | no (reads *from* `Q_N`) |
| archive map `Δ` | `:465` | active readout (`P_N`) → forgotten store | no (readout-side metadata removal, P6) |

No other operator in BOOK_01 has `Q_N` in its codomain from the circulated sector. (Kill
condition ATT-W1, §5: an owned cross-event `Q_N`-writer that does not factor through
`:1998` falsifies this — none found. `close_gap_w_check.py` check 4 plants a second writer
as a control and detects it.)

### 2.2 Why exhaustiveness is FORCED (not a reading)

`P_N + Q_N = I`, `P_N Q_N = 0` (P1) is a **partition of the record support** into two
orthogonal sectors. A cross-event re-detection record lives in exactly one:
- **`P_N` (retained/readout):** terminal, destructive, **same-event** (P2, `:8`) —
  consumed at readout, so it is NOT a cross-event carrier.
- **`Q_N` (traced/archive):** the persistent cross-event memory layer (P3).

Therefore the **single cross-event carrier is `Q_N`**, and (§2.1) the single owned write
into it from the circulated sector is the `:1998` emission. This is the completeness
`P_N + Q_N = I` doing the work — it is **owned architecture at CORE grade**, upgrading the
synthesis memo's "READING (residue)" classification.

> **W-REC verdict: CLOSED (CORE).** Missing lemma: none. The completeness `P_N + Q_N = I`
> (:37) + the same-event nature of the retained readout (:186/:8) + the single `Q_N`-writer
> sweep (:1998) force it. `close_gap_w_check.py` check 4, with the planted-second-writer
> control.

---

## 3. Residue W-ELEM — CLOSED conditional on W-REC, at ASSEMBLY grade

### 3.1 The chain (each atom owned or computed; the target is an OUTPUT)

| atom | statement | grade | source |
|---|---|---|---|
| **G1** | a re-detection class is a **physical** object realized over records | OWNED-CORE | P9 `:992`, P10 `:996` |
| **G2** | physicality ⇒ it can **alter/constrain an addressable registration** | OWNED-CORE (contradiction theorem) | P8 `:988` |
| **G3** | the emission's archive trace is **address-blind** (every locus marker averages to uniform `(1/8)I`; occupies no address position) | COMPUTED | check 1 (`AVG_ADDRESS_BLIND`); check 3 (`ADDR_DISJOINT_FROM_TRACE`) |
| **W-REC** | the **only** cross-event carrier from the circulated sector is that address-blind trace | OWNED-CORE (§2) | P1–P5 |
| ⇒ **W-ELEM** | the class-realizer is a **base-element address** (the `V_9`/`ω_0` marker), not the trace's operator content | **DERIVED** (output of G1&G2&G3&W-REC) | §3.2 |

**The inference.** A physical re-detection class (G1) must alter/constrain an *addressable*
registration (G2). The emission trace is *address-blind* (G3), so the trace itself is not
that registration. By W-REC, the trace is the *only* cross-event carrier — so the required
addressable registration is **not reachable through the emission channel**. Hence an
**adjoined addressable base-element** registration must carry the class: the `V_9 = Ω_8 + ω_0`
marker (P13). That is W-ELEM. The element-vs-operator **format** is the *conclusion* of
{G2 + G3 + W-REC}, not a premise.

### 3.2 Why this is NOT the S9 smuggle (the decisive skeptic gate)

The synthesis memo's S9 died because it silently assumed *"the realizer is a base
element"* (element-realization), then located it "beyond Ω₈" — the conclusion was the
premise (ATT-S2, circularity). **This chain does not repeat that**:

- S9 assumed the realizer's **FORMAT** (element) and derived its **LOCATION**. Here the
  format is *derived*: from G2 (addressability required) + G3 (trace is blind) + W-REC
  (no other carrier). No step assumes the realizer is an element.
- The honest **escape** a skeptic raises against G2: *"the class IS the address-blind
  trace, and G2 is satisfied because the trace CONSTRAINS a **separate** downstream
  addressable registration."* Under this reading G2 holds *without* the class being
  element-realized — i.e. W-ELEM would not be forced. **This escape is closed ONLY by
  W-REC:** by W-REC the only cross-event carrier is the address-blind trace, so any
  "separate downstream registration" must be reached *through* the trace, inheriting its
  blindness (averaging is **idempotent** — `avg(avg(M)) = avg(M)`, check 6), hence it is
  *not* addressable. The escape's "separate addressable registration" does not exist
  cross-event inside the owned channel. So W-ELEM is forced — **but only because W-REC is
  owned.**

> **This is the load-bearing discovery.** W-ELEM and W-REC are **NOT independent
> residues**: W-REC is exactly the fact that shuts the escape that killed S9. The mutation
> test proves the closure genuinely consumes W-REC: **`close_gap_w_check.py` check 6
> (`WELEM_NOT_CIRCULAR`) verifies the escape is OPEN *without* W-REC and CLOSED *with* it;
> mutation M3 — forcing the escape closed regardless of W-REC (the smuggle) — makes check 6
> FAIL.** A closure that imported element-realization would certify *without* W-REC; this
> one cannot.

### 3.3 The honest residue R-A — a NAMED EXTERNAL ASSEMBLY-BRIDGE (re-graded post-independent-skeptic)

The one place the chain is not owned: **the chain needs "the re-detection *class-record*
IS an addressable registration", and no owned line states it.** Precisely:

- `:988` (§01.11.1) forces only that a physical class **INTERACTS WITH** ("cannot alter or
  constrain") an addressable registration — **NOT that the class IS one.** This is the
  exact gap. W-REC removes the *alternative carrier* (the address-blind trace is the only
  cross-event carrier, so it cannot be the addressable registration `:988` demands), but
  W-REC does **not** by itself supply the IS-typing — it closes the "constrains a separate
  downstream registration" escape (§3.2) without asserting the class is itself the
  base-element registration.
- `:253` (§01.3) types the record **atom** `𝔮` as addressable *at the primitive-dyad
  layer*; `:996` (§01.11.3) types the re-detection **class** as a physical object over
  records. Assembling "the class-record IS an addressable registration" spans the
  **§01.3 → §01.11.3 layer boundary** — an un-owned join.

**This is NOT the same grade as GAP-E's `:325` typing** (independent-skeptic correction,
accepted). GAP-E had an **in-print name-match**: BOOK_01:836/:862/:67 literally print the
extension letters AS "states" (`Ω8` = "eight oriented terminal-role **states**", ABCD =
"quotient data on this profinite/condensed support" `S_{D0}`) — the very type `:325`
quantifies over, so the skeptic granted it as a *matched typing*. **GAP-W has no
counterpart in-print line** naming the re-detection class-record as an addressable
registration. So R-A is a strictly **stronger reach** than `:325` was.

> **R-A (NAMED EXTERNAL ASSEMBLY-BRIDGE).** *The un-owned typing that the re-detection
> class-record **IS** — not merely **interacts-with** — an addressable registration,
> assembled across the §01.3/§01.11.3 layer boundary. `:988` forces INTERACT-WITH, not IS;
> W-REC removes the alternative carrier but does not close the IS-gap.*

Reopening hook (unchanged): a maintainer scoping `:253`'s `𝔮` narrowly to the primitive
dyad (the open scope question the synthesis memo's §I.E named) blocks the bridge and
demotes W-ELEM to narrated. Declared openly; it is the ONLY residue of W-ELEM — but a
**named external bridge**, not an assembly-grade matched typing.

> **W-ELEM verdict: CLOSED GIVEN W-REC + the named external assembly-bridge R-A.** Missing
> lemma: the IS-typing of R-A (owning "the re-detection class-record is an addressable
> registration", or an in-print name-match analogous to GAP-E's :836/:862/:67). The
> element-realization *format* is derived, not assumed — smuggle-guarded by check 6 /
> mutation M3 — but the closure rests on the un-owned R-A bridge.

---

## 4. Net — does the window LOWER bound seal?

**YES — but CONDITIONAL ON the named external assembly-bridge R-A (§3.3), not a full owned
closure.** Combining:

- The **8-kill** (no interior realizer): checks 1–3 (address-blindness + type separation)
  + G2 + W-REC ⇒ the class is realized at an adjoined base element, outside `Ω_8` (the
  synthesis memo's §II.6 "outside-Ω₈ + ≥1 + stationarity" halves, now with their premise
  W-ELEM *derived* rather than narrated).
- The **10-kill** (no second base element): Derivations II + III of the synthesis memo,
  already DERIVED (W-T1 retired) / DERIVED-after-SC1 (W-BIT, leaning on W-REC — now that
  W-REC is CLOSED at CORE, that lean is discharged, not a residue).
- **No-overfire** at `m = 1`: `first_instance_canonical` (`|S_1| = 1`), synthesis check 16.

⇒ `|V_base| = |Ω₈| + 1 = 9` is **FORCED given W-REC (owned architecture) + R-A (named
external assembly-bridge)**. The `[9,11,13]` window **LOWER bound seals CONDITIONAL ON
R-A** — not a full owned closure. This complements — and is independent of — the GAP-E
**UPPER** bound, which remains **OPEN**
(`CLOSE_GAP_E_MEMO §RESIDUE`: the two-universe uniform-block clause; `z₃ = 12` still
admissible there). **The window is lower-sealed, upper-open.**

### 4.1 Movement vs. the synthesis memo (honest scoreboard)

| item | synthesis memo v2 | this memo |
|---|---|---|
| residue count | 2 ({W-ELEM, W-REC}, "not unconditional") | 1 owned-architecture fact (W-REC, **derived**) + 1 **named external assembly-bridge** (R-A) |
| W-REC status | "READING (residue)" | **CLOSED — owned architecture (`P_N+Q_N=I`)** |
| W-ELEM status | "STILL-NARRATED, SHARPENED" | **DERIVED given W-REC + external bridge R-A** (smuggle-guarded); R-A the one residue, re-graded (NOT assembly-matched-typing) |
| independence | listed as two residues | **discovered dependent: W-REC shuts S9's escape** |
| S9 smuggle | killed | **not re-committed** (check 6 / M3 guard) |

---

## 5. Named risks & pre-registered attack surface (self-skeptic §05.8.R)

- **ATT-W1 (W-REC "only" is a sweep) — STANDS, now CORE-backed.** Kill: an owned
  cross-event `Q_N`-writer from the circulated sector not factoring through `:1998`.
  Sweep (§2.1) found none; `Δ` (:465) is readout-side (P6); `F_N` reads *from* `Q_N`.
  Backed additionally by the completeness `P_N + Q_N = I`. Control: check 4 detects a
  planted second writer.
- **ATT-W2 (the S9 circularity, ATT-S2 of the synthesis memo) — ANSWERED, guarded.** The
  format is derived from G2+G3+W-REC, not assumed. The smuggle guard (check 6) verifies
  the escape is open *without* W-REC; mutation M3 (smuggle) makes it FAIL. A closure
  importing element-realization would pass M3 — this one does not.
- **ATT-W3 (R-A typing) — WOUNDED by the independent skeptic; RE-GRADED (accepted).** The
  memo originally called "the re-detection *class-record* IS an addressable registration"
  an assembly-grade *matched* typing on par with GAP-E's `:325`. The independent skeptic
  showed this over-graded: `:988` forces INTERACT-WITH, not IS; and GAP-W has **no in-print
  name-match** (GAP-E had :836/:862/:67 printing letters AS "states"). R-A is therefore a
  **named external assembly-bridge** across the §01.3/§01.11.3 layer boundary (§3.3), not
  a matched typing. Reopening/closing hook: a maintainer scoping `:253`'s `𝔮` strictly to
  the primitive dyad blocks the bridge and demotes W-ELEM to narrated (the window lower
  bound then rests on the synthesis memo's narrated W-ELEM — no regression); conversely,
  owning the IS-typing (or finding an in-print name-match) upgrades the seal to a full
  owned closure.
- **ATT-W4 (G3 model-dependence / transitivity) — STANDS, inherited.** Address-blindness
  needs the owned transitive full-cycle model (`:1998`). Control: check 8
  (`NC_NONTRANSITIVE_SAVES_TRACE`) — under a non-transitive conjugation model (orbits
  [1,1,2,2,2], max 2 < 8) the center marker survives non-uniformly, G3 fails, and W-ELEM
  does not close. The closure genuinely leans on `:1998`.
- **ATT-W5 (the `:2004` adverse text) — CONSUMED, not evaded.** The invariant NON-scalar
  content (check 2) is the exact S9-killer; W-ELEM closes it by *excluding* it via G2+G3+
  W-REC, not by denying it exists. `D0-IM-004`'s scalar `= (9/2)·I` result is `F`-specific
  (`:2004` governs the general case); this memo does not upgrade it.

---

## 6. What this memo does NOT do

- Does NOT mint. CLOSE-W is a candidate; the independent skeptic pass is DONE (WOUNDED →
  repaired, §8), but minting still needs `VERIFIED_CLOSURE_PROTOCOL.md`.
- Does NOT make W-ELEM *unconditional*, and does NOT achieve a full owned closure: it is
  closed **given W-REC (owned architecture) + R-A (named external assembly-bridge)**.
  "Sealed conditional on R-A" ≠ "owned" ≠ "theorem-grade in the kernel".
- Does NOT touch the GAP-E **UPPER** bound (still OPEN — `CLOSE_GAP_E_MEMO §RESIDUE`).
- Does NOT edit any registry row / cert / built Lean file / the witness memo / the
  synthesis memo / `053040`; no commit. `GAP_W_SYNTHESIS_MEMO.md` v2 stands as the prior
  state of record; supersession by this closure is an OWNER DECISION.
- Does NOT re-derive W-T1 or W-BIT (owned by the synthesis memo; W-BIT's lean on W-REC is
  now discharged since W-REC is CLOSED at CORE).

---

## 7. Lean path (memo-only skeleton — NOT added to the built tree)

The conditional capstone of the synthesis memo (§VI) stands, with its support attribution
upgraded: `h_halt` (the `+1`) is now backed by **W-REC (owned architecture) + G2 (:988
CORE) + G3 (computed) + R-A (named external assembly-bridge)** — NOT by a narrated W-ELEM.
R-A stays an explicit, un-discharged Lean hypothesis (an external bridge, not an owned
lemma).

```lean
-- theorem card_base_forced_conditional (m : ℕ) (h_halt : 1 ≤ m) (h_nocopy : m < 2) :
--     Fintype.card Omega8 + m = 9
--  h_halt  : W-REC (P_N+Q_N=I, single :1998 writer) + :988 + address-blindness + R-A
--  h_nocopy: Derivation II (owned schema) + Derivation III (W-REC now CORE-discharged)
```

Decidable obligations (mirrored by the script): `OB-W1` marker-averaging-is-address-blind
(check 1), `OB-W2` address-vs-trace type disjointness (check 3), `OB-W3` averaging
idempotent (check 6). The typing R-A stays an explicit Lean hypothesis; no over-claim.

**Registry note (PROPOSED text only — no row edited):** row
`D0-GAP-W-WITNESS-PLUS-ONE-001` EXACT-MISSING could truthfully become: "(1) W-REC CLOSED
at CORE grade (owned complementarity `P_N + Q_N = I`, single `:1998` `Q_N`-writer);
(2) W-ELEM DERIVED given W-REC (element-realization is an output of `:988` + computed
address-blindness + W-REC; smuggle-guarded), residue = the NAMED EXTERNAL
ASSEMBLY-BRIDGE R-A (the un-owned IS-typing of the class-record; `:988` gives INTERACT-WITH
only, no in-print name-match unlike GAP-E's :836/:862/:67); (3) lower bound `z₀ = 9`
sealed CONDITIONAL ON R-A (not a full owned closure); (4) GAP-E upper bound untouched
(OPEN)." Per `MINTING_PACKAGES.md` this remains PROOF-TARGET; the independent skeptic pass
is DONE (WOUNDED → repaired).

---

## 8. Independent-skeptic pass (§05.8.R, separate agent) — verdict WOUNDED → repaired

**Result: WOUNDED, not killed — accepted in full.** W-REC SURVIVES (owned-architecture
grade); the chaining discovery SURVIVES (M3 reproduced, 8/9); **R-A was OVER-GRADED** and
is re-labelled here (§3.3, ATT-W3). Errors of record (no defense):

- **E-CW-1 (the wound).** The memo called R-A an "assembly-grade matched typing … the same
  grade the GAP-E skeptic granted for `:325`". FALSE parity: GAP-E had an **in-print
  name-match** (BOOK_01:836/:862/:67 print the letters AS "states" = the `:325` type);
  GAP-W has **no** in-print line naming the re-detection class-record as an addressable
  registration, and `:988` forces **INTERACT-WITH**, not **IS**. *Fix:* R-A re-graded to a
  **named external assembly-bridge** across the §01.3/§01.11.3 layer boundary; the parity
  claim struck throughout (banner, §pre-flight, §3.3, ATT-W3, §4, §7); W-REC removes the
  alternative carrier but does NOT close the IS-gap — recorded explicitly.

**Standard (i) named second object:** the S9-killer (invariant NON-scalar trace content,
`:2004`, check 2) is *excluded*, not re-hidden. No *new* second object escapes: the escape
reading (§3.2) is closed by W-REC; the mutation test confirms the closure fails if W-REC
is not genuinely consumed. SURVIVES.

**Standard (ii) smuggled premise:** the decisive gate. W-ELEM's element-realization is an
OUTPUT of {G2 + G3 + W-REC}, not an input — verified structurally (§3.2) and by mutation
M3 (`WELEM_NOT_CIRCULAR` FAILS if the escape is forced closed without W-REC; the
independent skeptic reproduced this, 8/9). SURVIVES. The residual R-A is a **named
external bridge** (declared), not a smuggle.

**Verdict (post-independent-skeptic, repaired):** **W-REC CLOSED (owned architecture);
W-ELEM CLOSED given W-REC + the NAMED EXTERNAL ASSEMBLY-BRIDGE R-A; window LOWER bound
SEALED CONDITIONAL ON R-A — NOT a full owned closure.** The load-bearing new result is the
**chaining**: the two residues are not independent — W-REC is what shuts S9's escape. The
one honest residue, R-A (the un-owned IS-typing of the class-record; `:988` gives
INTERACT-WITH only, no in-print name-match unlike GAP-E), is a named external bridge whose
owning (or an in-print name-match) would upgrade the seal to a full owned closure.
Candidate; no minting; owner decision on supersession of the synthesis memo's 2-residue
accounting.
