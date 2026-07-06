# DEEP SYNTHESIS PASS — batch M — COLOUR + HIGGS no-gos

**Date:** 2026-07-06 · **Status:** DRAFT synthesis memo (verification only).
**No registry/book/`.lean`/`053040` edits.** Row-notes proposed at foot for owner to bless.
**Companion can-fail script:** `_TASKS_CENTER_ATTACK/deep_m_colour_higgs_check.py`
— **12/12 PASS, rc=0**, mutation-tested (4 mutations: 3 fire, 1 is a correct no-op documented below).
**Skill:** `d0-adversarial-forcing-loop` (compute-first → memo → independent skeptic → accept/repair).

Two no-gos, genuine per-no-go depth (not a tagging pass). Verdict up front, then the work.

- **COLOUR** (`D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001`): **GENUINE-BOUNDARY-PROVEN.**
  The `8 < 9` gap is the *sharp owned interface*, not a defect. New owned depth: the `8<9` collapse
  and the flow→Weyl NO-GO are **one mechanism** (the M1-forced `+2` zone step), verified numerically.
- **HIGGS** (`D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001`): **SHARPENED OPEN SLOT (does NOT decompose).**
  New owned depth: condensation has **TWO independent walls** (orbit *and* SSB-sign); the missing
  non-commuting `Q0` is **necessary-but-not-sufficient**. The decompose route (central-extension
  layer) is *blocked as an owned lever* by the GAP-E fork.

---

## PREFLIGHT (mandatory)

`preflight.sh "COLOUR-GENERATION-TYPED-CARRIER HIGGS-PHASON-ORBIT colour phason condensation"` → no
row owns the two new **linkage** findings below. Rows cross-referenced (cited, never duplicated):

- `theory_status_map.csv:528` `D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001` (PYTHON_CERTIFIED, NO-GO)
- `theory_status_map.csv:397` `D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001` (LEAN_PROVED, NO-GO)
- `theory_status_map.csv:407` `D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001` (LEAN_PROVED, NO-GO)
  — the `tPoly_commutes` maximality strengthening.
- BOOK_04 §04.11 (`0013__04.11`): flow→Weyl `Φ` four-wall NO-GO (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`),
  role-cycle carrier NO-GO, colour-vs-generation paragraph.
- BOOK_04 §04.16 (`0018__04.16`): Higgs F6 stationary condition, `z²≥0` never-SSB, Outcome-B.
- `HIGGS_PHASON_ORBIT_BLOCKERS.csv` (10-row downstream chain), `HIGGS_PHASON_ORBIT_FROZEN_INPUTS.json`.
- `J2_HIGGS_NONCOMMUTE_CHECK.md` (the TorusCore13 piece-to-hole check — already KILLED as a direct fit).
- `GAP_E_SYNTHESIS_MEMO.md` §SKEPTIC-#1 — central-extension `{D₂,ABCD}` identification is **fork-open /
  killed-as-closure**; NOT owned. **This memo does not lean on it** (respected per the task constraint).

---

# NO-GO 1 — COLOUR

## 1. Decisive proved statement, verbatim (`vp_colour_generation_typed_carrier_nogo.py`)

> `05_CERTS/vp_colour_generation_typed_carrier_nogo.py:99-103`
> ```
> print(f"[B] dim Commutant(weak) on C^8=C[Q8] = dim R(Q8) = {comm}")
> assert comm == 8, "commutant of the Q8 left-regular algebra must be the 8-dim right-regular algebra"
> assert comm < 9, "the commutant (8) is strictly below dim M3(C) = 9"
> ```
> Output: `[B] dim Commutant(weak) on C^8=C[Q8] = dim R(Q8) = 8` →
> `PASS_COMMUTANT_GAP  dim Comm(weak)=8 < 9=dim M3(C): a source-native colour M3 does NOT fit`.

And part (A), `:85-87`:
> `assert typed == 3, "D_zone with distinct eigenvalues must collapse M3 to the 3-dim diagonal"`
> → `PASS_TYPED_COLLAPSE  raw M3 (9) -> typed abelian C^3 (3): three zones = GENERATIONS, not colour`.

**Exact arithmetic (re-derived, not asserted):** commutant of `diag(24,22,20)` in `M₃(ℂ)` =
`Σ (class size)² = 1²+1²+1² = 3`; commutant of `ℂ[Q₈]` left-regular = right-regular `R(Q₈)`, dim `8`;
`8 < 9 = dim M₃(ℂ)`. Both reproduced by hand in the can-fail script (exact integer sums).

## 2. Five attack lines (ladder of ambition)

**(a) LIFT border→defining property.** Attempt: promote `8<9` from "on these two carriers" to "on *any*
source carrier". *Result — does not lift as stated, and correctly so.* The `8` is carrier-specific
(`dim R(Q₈)`); a different terminal carrier could have a larger commutant. The honest lift is **not**
dimension-counting but the **root/Weyl** obstruction (attack c), which IS carrier-intrinsic to the
M1-forced zone data. LIFT redirected to (c), not claimed on (b).

**(b) CLOSE — is colour `M₃` owned elsewhere?** Read the octonion/E8/Furey/Mordell neighbourhood
(`theory_status_map.csv:92,226,236,242`; `EXTERNAL_ASSUMPTION_REGISTRY.csv:10`):
- `D0-HURWITZ-INTERNAL-DIMENSION-SELECTOR-001`: "octonion witness is **finite composition data**, NOT
  an associative Matrix 8 8 algebra." → octonions do not supply an internal `M₃`.
- `D0-ICOSIAN-E8-GRAM-001`, `D0-DIM8-NETWORK-001`: E8 enters via **Mordell genus-uniqueness**
  (`ASSUMP-MORDELL-E8`, EXPLICIT external); `dim8_network` **REJECTS** the "3 generations = #D4 reps"
  forcing-link out loud (anti-numerology). → E8 is an *external* owner, forces the number 8 only.
- **CLOSE FAILS by ownership, decisively:** there is **no owned source-native colour `M₃`** anywhere.
  The colour factor is the **inserted `𝒜_F` completion `ℋ_q = W₃⊗V₂`** (cert `:103`), an external
  `⊗ℂ³`. This is not a gap to be filled — it is the honest terminal-passport interface (memory:
  `colour-su3-not-derived-in-d0`).

**(c) DECOMPOSE into owned structure — THE DEEP FINDING.** The `8<9` collapse is **not an isolated
dimension accident**; it is the SAME M1 rigidity that appears one dimension up as the flow→Weyl NO-GO.
BOOK_04 §04.11 states it in prose ("the M1-forced `+2` progression … is precisely what destroys the
`SU(3)` Weyl carrier … one cause, two effects"). **I verified the linkage numerically** (script FINDING C):
one toggle — the `+2` zone step — flips BOTH:

| M1 rigidity | zone frame | colour commutant | zone-swap (Weyl proxy) |
|---|---|---|---|
| **OFF** (equal `K(n,n,n)`) | `{22,22,22}` | **dim 9** (full `M₃`, colour would fit) | order **6** = `\|W(SU(3))\|` |
| degenerate | `{24,24,20}` | dim 5 (a block survives) | order 2 |
| **ON** (`+2` forced) | `{24,22,20}` | **dim 3** (abelian → generations) | order **1** (Weyl destroyed) |

The control fires if the two effects ever decoupled — they never do across the M1 family. **This is the
sharp owned reason `8<9` is not a defect:** the same rigidity that makes the three zones pairwise
distinguishable (⇒ they are the abelian **generation** lines) is what forbids the non-abelian colour
`M₃`. Colour-absence and generation-distinctness are the *same theorem read two ways*.

**(d) PROVE GENUINE BOUNDARY + honest I/O typing.** With (b) closed-by-ownership and (c) decomposed:
- **Owned (INPUT the scene provides):** the abelian `ℂ³` generation algebra (typed collapse), the
  `dim R(Q₈)=8` weak-commutant ceiling, the M1 `+2` rigidity.
- **External (INPUT that must be imported):** the colour `⊗ℂ³` = `𝒜_F` completion `ℋ_q=W₃⊗V₂`
  (terminal-passport, octonion/E8 route, **Mordell/Furey-owned**, never scene-native).
- **The interface is `8 = 9 − 1`:** the scene owns an 8-dim weak-commutant; colour needs a 9-dim `M₃`;
  the **1-dimensional deficit is exactly the external `⊗ℂ³` seam**. Sharp, owned, honest.

**(e) Adversarial self-attack (pre-registered, strongest I can build).** "The `H_edge / P·Q` feedback
carrier is neither scene-zone nor terminal-`ℂ⁸`; colour could be source-native there — so the boundary
is not genuine, only unproven on two carriers." **Concession, recorded:** correct — the no-go's own
scope line (`:20-23`, `:111-112`) says exactly this ("does NOT classify colour on `H_edge`/`P·Q`
globally"). The boundary is **genuine on the two frozen carriers where colour was most tempting**, and
**open (not decided) globally**. I do NOT claim global colour-absence. The verdict is
GENUINE-BOUNDARY-PROVEN *at the tempting carriers* + honest OPEN-global, which matches memory
(`colour-su3-not-derived-in-d0`) and is the anti-over-claim landing the owner wants.

## 3. WORKED VERDICT — COLOUR

**GENUINE-BOUNDARY-PROVEN (sharpened).** Exact owned object: the abelian generation collapse
`dim Comm(D_zone)=3` and the ceiling `dim R(Q₈)=8 < 9` (`vp_colour_generation_typed_carrier_nogo.py`),
now **decomposed** into the single M1 `+2` mechanism shared with the flow→Weyl NO-GO
(`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`, BOOK_04 §04.11). Exact external object: the imported colour
`⊗ℂ³ = 𝒜_F` completion `ℋ_q=W₃⊗V₂`, terminal-passport (Mordell-`ASSUMP-MORDELL-E8` / Furey octonion
route). **The `8<9` deficit IS the interface**, one dimension wide. No derivation manufactured.

---

# NO-GO 2 — HIGGS

## 1. Decisive proved statement, verbatim

`vp_higgs_phason_orbit_nontriviality.py:34-42`:
> `assert conj_orbit_size(Qc) == 1, "commuting Q0 must give a constant orbit"`
> `PASS_COMMUTING_TRIVIAL  a Q0 commuting with T (e.g. identity) has a CONSTANT conjugation orbit.`
> … `PASS_NONTRIVIAL_NEEDS_NONCOMMUTING  a nontrivial orbit (size 30) exists ONLY for a non-commuting
> Q0 -- which is a CHOICE, not a frozen canonical projector.`

Maximality strengthening (`D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001`, verbatim registry):
> "every present-core frozen projector is a polynomial `a*1+b*T` in the return operator `T`
> (theorem `tPoly_commutes`) and commutes with `T` => constant orbit => no double-well => no condensation."

## 2. Five attack lines

**(a) LIFT border→defining property.** The no-go's border is "no *canonically-frozen* non-commuting
`(U,Q0,Π_H)`." Maximality already lifted it from "on the chosen `T`" to "on the whole present-core
polynomial class `a·1+b·T`" (`tPoly_commutes`). I verified **exhaustively** over `ZMod 44` (script Wall 1:
all `44×44` polynomials commute with `T`). The border is a **defining property of present-core**, not a
sampling artifact. LIFT SUCCEEDS (already owned; I re-verified exhaustively).

**(b) CLOSE — is the non-commuting `Q0` owned elsewhere?** Best candidate on record: the TorusCore13
noncommutation `radial_hopping_phase_drift_noncommute` (`D0-TORUS-CORE13-GEOMETRY-001`).
**Already KILLED** by `J2_HIGGS_NONCOMMUTE_CHECK.md` — five independent mismatch axes (carrier `Fin3/ℚ`
vs `Fin2/ZMod44`; wrong `T`; `phaseDrift` not idempotent; no triple/`Π_H`/flow; free passport parameter).
CLOSE FAILS. No other owned non-commuting frozen projector exists (blocker atlas rows
`D0-HIGGS-ARCHIVE-PROJECTOR-ORBIT-OWNER-001`, `-FINITE-CONDENSATION-OWNER-001` are both PROOF-TARGET).

**(c) DECOMPOSE — does condensation live in an extension layer (like `D₂/ABCD`)?** The tempting move: the
non-commuting `Q0` is supplied by the role group's central extension `1→Z(Q₈)→Q₈→V₄→1` (`Q₈` is
non-abelian, so *its* structure is genuinely non-commuting). **BLOCKED as an owned lever:** the
central-extension identification of the two zone-layers `{D₂,ABCD}` is **fork-open / killed-as-closure**
per `GAP_E_SYNTHESIS_MEMO.md` §SKEPTIC-#1 — the alphabet-grammar clause is OPEN, so I cannot cite the
extension layer as an *owned* source of the frozen non-commuting triple. DECOMPOSE FAILS **on ownership
grounds** (exactly the caveat the task flagged). The extension layer is a *lead*, not an owner.

**(d) PROVE GENUINE BOUNDARY / sharpen the OPEN slot — THE DEEP FINDING.** Condensation is not blocked by
one wall but **TWO logically independent** ones (script FINDING H):
- **Wall 1 (orbit):** present-core `⇒ [T,Q0]=0 ⇒` constant orbit `⇒` no double-well
  (`tPoly_commutes`; verified exhaustively).
- **Wall 2 (SSB sign):** *even given* a nontrivial orbit, the log-det quadratic coefficient is `z² ≥ 0`,
  **never the negative (double-well) sign** (`D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001`, F6, BOOK_04
  §04.16: `assert sp.simplify(quad_coeff - z**2) == 0`). I verified Wall 2 is **orbit-independent**: the
  `z²` sign carrier does not depend on which `Q0` drives the orbit (script: coefficient exactly `1>0`,
  unchanged by a hypothetical non-commuting `Q0`).
- **Consequence (new, owned by neither row explicitly):** filling the missing non-commuting `Q0` is
  **NECESSARY-BUT-NOT-SUFFICIENT.** Two distinct external imports are required: (i) a frozen
  non-commuting `(U,Q0,Π_H)` with `[T,Q0]≠0`, AND (ii) a negative-sign input flipping `z²`. This
  **sharpens** the OPEN slot: the corpus phrasing "a new independently-forced non-commuting action"
  understates the gap by one wall.

**(e) Adversarial self-attack (pre-registered).** "Wall 2 is a strawman: a non-commuting `Q0` changes
the *effective* potential, so the `z²` computation (done for the trivial/commuting profile) need not
survive — you cannot assert Wall 2 stands once Wall 1 is filled." **Partial concession, scoped:** the
`z²` result is proved for the log-det functional's *series structure* (`−2log(1−zf)`), which is
`Q0`-free at the coefficient level (script INDEPENDENCE check). BUT — honest limit — a genuinely
non-commuting `Q0` would make `f` matrix-valued and the reduction `f'(θ)=0` (F6) was proved in the
*scalar* sector. So Wall 2 is **proven independent in the scalar reduction** and is a **strong
conjecture (not a theorem) in the full non-commuting sector**. I therefore claim
NECESSARY-BUT-NOT-SUFFICIENT as **owned in the scalar sector, flagged-conditional in the matrix sector**
— named reopening hook. This is the honest ceiling; I do not over-claim a two-wall theorem globally.

## 3. WORKED VERDICT — HIGGS

**SHARPENED OPEN SLOT — does NOT decompose.** Exact owned object: the trivial-orbit no-go
(`tPoly_commutes`, `vp_higgs_phason_orbit_nontriviality.py` + maximality cert) PLUS the orbit-independent
`z²≥0` non-SSB wall (`D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001`). Exact missing external object:
**TWO** imports, not one — a frozen non-commuting `(U,Q0,Π_H)` with `[T,Q0]≠0` (`derived not chosen`),
**and** a negative-quadratic-sign input. Decompose route (central-extension layer) is
**not available as an owner** (GAP-E fork). The slot stays PROOF-TARGET
(`D0-HIGGS-FINITE-CONDENSATION-OWNER-001`), now with a **second named wall**.

---

## §05.8.R — INDEPENDENT SKEPTIC PASS (kill-mandate)

Run against the two headline findings. Verdicts below; repairs applied inline above where accepted.

**COLOUR headline ("`8<9` = flow→Weyl are one M1 mechanism").**
- *Kill attempt 1 — "the zone-swap function is not the real Weyl group; you proxied it."* **Sustained as a
  scope-narrowing, not a kill.** My `zone_swap_order` is a **proxy** for the geometric Weyl carrier, not
  the full spectral Weyl analysis (BOOK_04 §04.11 does the real four-wall version: rank 3<4, eigenvector
  action trivial, `120°` geometry, pigeonhole). *Repair applied:* memo now says "Weyl proxy" explicitly
  and defers the *authoritative* Weyl claim to the owned four-wall NO-GO; my numerical contribution is
  only the **linkage** (same toggle flips colour-collapse and swap-symmetry together), which is exactly
  what I certified. No over-claim survives.
- *Kill attempt 2 — "CLOSE-fails-by-ownership is just absence of evidence."* **Not sustained.** It is
  positive owned content: `D0-HURWITZ…` states octonions are not an associative `M₈`; `dim8_network`
  explicitly REJECTS the generation-from-D4 forcing-link. The absence is *asserted by the owners*, not
  merely unfound.
- **Verdict: NO KILL.** Colour verdict GENUINE-BOUNDARY-PROVEN stands, with the Weyl-proxy scope repair.

**HIGGS headline ("two independent walls; `Q0` necessary-but-not-sufficient").**
- *Kill attempt 1 — "Wall 2 was proved in the scalar sector; a non-commuting `Q0` breaks the scalar
  reduction, so you cannot assert two walls once Wall 1 is filled."* **Sustained (wounded, repaired).**
  This is the correct kill of a *global* two-wall theorem. *Repair applied* (attack e): claim demoted to
  **owned-in-scalar-sector / flagged-conditional-in-matrix-sector**, with a named reopening hook. The
  NECESSARY-BUT-NOT-SUFFICIENT conclusion survives *as sharpening the open slot* (it lists two external
  imports the corpus currently conflates into one) but NOT as a closed two-wall no-go. Registry-safe:
  the row stays PROOF-TARGET regardless.
- *Kill attempt 2 — "you used the central extension after all."* **Not sustained.** I explicitly did NOT:
  attack (c) records DECOMPOSE as FAILING on the GAP-E fork; the extension is named a lead, not an owner.
- **Verdict: WOUNDED-REPAIRED.** Higgs verdict SHARPENED-OPEN-SLOT stands; the scalar-vs-matrix scope of
  Wall 2 is now explicit.

**Can-fail script mutation record** (`deep_m_colour_higgs_check.py`, 12/12 PASS):
- M1 forced-frame→degenerate ⇒ **rc=1** (colour linkage fires). ✓
- M2 Wall-2 coeff→0 ⇒ **rc=1** (sign wall fires). ✓
- M3 `T` off-diagonal `1→2` ⇒ **rc=0** *(correct no-op: `tPoly_commutes` is structural — any matrix
  commutes with its own polynomials, independent of `T`'s entries; documented, not a defect).*
- M4 `T`→scalar `diag(3,3)` ⇒ **rc=1** (Wall-1 witness `[T,Qnc]≠0` fires — the T-specific content). ✓

---

## PROPOSED ROW-NOTES (owner to bless — NOT applied)

1. **`D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001`** (append to Notes):
   > DEEP-M linkage: the `8<9` / `M₃→ℂ³` collapse and the flow→Weyl NO-GO
   > (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`) are ONE mechanism — the M1-forced `+2` zone step: at equal
   > zones `K(n,n,n)` colour fits (commutant dim 9) AND a Weyl `S₃` proxy exists (order 6); the `+2`
   > rigidity simultaneously collapses colour to the abelian generation `ℂ³` (dim 3) and kills the swap
   > symmetry (order 1). `8<9` is therefore not a defect but generation-distinctness; the 1-dim deficit
   > IS the external `⊗ℂ³` = `𝒜_F` interface (terminal-passport, `ASSUMP-MORDELL-E8`/Furey).
   > Verified `_TASKS_CENTER_ATTACK/deep_m_colour_higgs_check.py` (FINDING C, mutation-tested).

2. **`D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001`** (append to Notes):
   > DEEP-M sharpening: condensation faces TWO independent walls, so the missing non-commuting `Q0` is
   > NECESSARY-BUT-NOT-SUFFICIENT — (W1) present-core `[T,Q0]=0` trivial orbit (`tPoly_commutes`), and
   > (W2) the log-det quadratic coefficient is `z²≥0`, never the SSB sign
   > (`D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001`). Two external imports are required, not one: a frozen
   > non-commuting `(U,Q0,Π_H)` AND a negative-sign input. W2 owned in the scalar sector,
   > flagged-conditional in the full matrix sector (reopening hook). Decompose-via-central-extension is
   > NOT an owned lever (GAP-E fork, `GAP_E_SYNTHESIS_MEMO.md` §SKEPTIC-#1). TorusCore13 fit already
   > killed (`J2_HIGGS_NONCOMMUTE_CHECK.md`). Verified `deep_m_colour_higgs_check.py` (FINDING H).

*No status changes proposed: COLOUR stays NO-GO (GENUINE-BOUNDARY), HIGGS stays NO-GO + PROOF-TARGET
downstream. Both verdicts are sharpenings, not promotions.*
