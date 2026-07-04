# TASK W6 — T2′: the E₀-block restriction and what the X5 lepton contract actually postulates

**Date:** 2026-07-02  **Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`
**Discipline:** READ-ONLY audit. No repo file edited outside `_TASKS_CENTER_ATTACK/`. No
status/claim editing. No promotion language ("derived"/"confirmed"/"forced"/"closed") applied to
T2′. Every verdict carries a file:line citation. Arithmetic re-run under python3 3.9.6.

**Object under audit — T2′ (the refinement of T2 that survived W3's skeptic gate):**
the 7-point no-go carrier is the *restriction of the (1,4,3) Q₈-Fourier system with the rank-1
trivial-rep block E₀ removed*, and E₀ **is** the unramified electron entry already declared "exact
and THE" elsewhere. The tension: if the (1,4,3) row is already THE, what is the X5 postulate FOR?
Hypothesis: the residual gap is not the *existence* of the third branch (it exists internally as E₀)
but the *identification* of the intrinsically-ordered Q₈ triple (1,4,3) with the unordered
scene-side generation triple (Tr(T²)=3).

---

## (a) Verbatim X5 content — what `D0-X5-LEPTON-CONTRACT-001` actually postulates

### The Lean object, verbatim

`09_LEAN_FORMALIZATION/D0/Extensions/X5/Lepton.lean:18-24`:

```lean
/-- The LeptonBranchFixer contract (HYP, D0-X5). -/
def branchContract : PrimitiveContract :=
  ⟨"PRIM-LEPTON-BRANCH-FIXING-OPERATOR", "D0-X5",
   ["three-row-complete", "monodromy-covariant", "terminal-compatible", "full-group-equivariant",
    "nonzero-selective"], 3⟩
```

The concrete model (`Lepton.lean:26-31`):

```lean
/-- Concrete `B₃` model: the branch→row bijection (identity assignment). -/
def B3 : Fin 3 → Fin 3 := ![0, 1, 2]
/-- The deletion alternative bijection. -/
def B3alt : Fin 3 → Fin 3 := ![0, 2, 1]
/-- The three-row exponent triple `(0, 1/4, 1/3)`. -/
def rowExponents : Fin 3 → ℚ := ![0, 1 / 4, 1 / 3]
```

The module docstring (`Lepton.lean:6-11`), verbatim:

> "The lepton branch-fixing primitive POSTULATED (HYP, D0-X5), acting on the FULL three-row triple
> `(0, 1/4, 1/3)` (including the `0`/electron branch). Concrete model: **a bijection
> `B₃ : Fin 3 → Fin 3` assigning the three branches (0-branch, 4-cycle, 3-cycle) to the three
> rows**, with the row-exponent triple `(0,1/4,1/3)` pairwise distinct. Deletion of the
> full-group-equivariance law admits a second bijection (`[0,2,1] ≠ [0,1,2]`) — the law is
> necessary."

### Stated non-vacuous model and axiom-deletion minimality argument

- **Non-vacuous model** (`Lepton.lean:37-38`): `branchModel : ModelWitness := ⟨3, 5, true⟩`; complete
  when non-vacuous, all 5 laws verified, carrierDim = 3. The "non-vacuous" flag is a decidably-checked
  `Bool`, per the pattern module `X5/PrimitiveContract.lean:28-38`.
- **Deletion-minimality** (`Lepton.lean:40-43`): dropping the `"full-group-equivariant"` law admits
  `≥ 2` bijections (`B3 = [0,1,2]` and `B3alt = [0,2,1]`, `B3 ≠ B3alt` by `decide`) — so the law is
  "necessary" in the sense `2 ≤ survivingModels` (`PrimitiveContract.lean:47`). This is a
  necessity-of-*a*-law argument, **not** a forcing of the assignment itself; the two surviving
  bijections `[0,1,2]` vs `[0,2,1]` differ precisely by an **S₃ transposition of the μ↔τ rows**.

### VERDICT — existence vs assignment

The X5 contract postulates the **ASSIGNMENT**, not the existence, of the branches.

- The postulated object is a **bijection `B₃ : Fin 3 → Fin 3`** (`Lepton.lean:27`, docstring
  `Lepton.lean:8` "**a bijection** … **assigning** the three branches … to the three rows"). Its type
  is a *map between two 3-element index sets*, not the construction of a branch/orbit.
- The three branches it assigns — "(0-branch, 4-cycle, 3-cycle)" (`Lepton.lean:8`) and the row
  `(0, 1/4, 1/3)` (`Lepton.lean:31`) — are named as **already-existing** inputs. The `0`/electron
  branch is present *inside the triple the operator acts on*: "acting on the FULL three-row triple
  `(0, 1/4, 1/3)` (**including the `0`/electron branch**)" (`Lepton.lean:7-8`). The contract does not
  build the `0`-branch; it receives it and maps it to a row.
- The carrierDim is 3 (`Lepton.lean:22`), and the model laws are all about a *3→3 map* being
  complete/covariant/equivariant/selective — never about *producing* a third orbit.

So: the electron branch's **existence** is supplied upstream (as E₀, see (b)/(c)); what the X5
contract adds is the **branch→generation-row assignment map**. This is exactly the reading T2′
predicts. (Caveat retained for the skeptic, §f: the contract's *header attribution* elsewhere in the
corpus says the third *datum* is "genuinely external" — see the tension flagged in (c) and (f).)

---

## (b) Where the (1,4,3)→(4,3) restriction enters — locus + classification

### The chain, traced

| Stage | File:line | Content | Carries E₀? |
|---|---|---|---|
| Q₈ Fourier system | `UnifiedFiniteCore/Q8Terminal.lean:13-17,24,68-70` | `E₀,E₄,E₃` orthogonal idempotents, ranks `(1,4,3)`, `E₀ = ⅛Σ_q L_q` "trivial-rep projector (rank 1)", `Q₉↔E₀ (rank 1, unramified)` = electron | **YES — all three** |
| Unified spine | `UnifiedFiniteCore/UnifiedTheorem.lean:31-36,39` | "branch orders `(1,4,3)` … appear simultaneously in the Q₈ Fourier ranks and the return orders"; `E0.trace=1 ∧ E4.trace=4 ∧ E3.trace=3` | **YES — all three** |
| Typed rep functor | `Representation/TypedRepresentationFunctor.lean:35-40` | `q8Ranks : Fin 3 → ℕ` = `1,4,3` reused as data | **YES — all three** |
| Branch-row minimal ext | `LeptonClosure/BranchRowMinimalExtension.lean:110-113` | `blockRanks := [1, 4, 3]`, `exponentRow := [0, 1/4, 1/3]` | **YES — all three** |
| Selector extension | `Extensions/LeptonSelectorExtension.lean:19-20` | `orbitSizes : List ℕ := [4, 3]` — "the two cycle/orbit sizes of the shell-torus `Ueff = blockdiag(4-cycle, 3-cycle)`" | **NO — E₀/rank-1 absent** |
| Branch-fixing no-go | `Extensions/LeptonBranchFixingNoGo.lean:30,37,41` | `numBranches := orbitSizes.length` = 2; `sigmaShell = ![1,2,3,0,5,6,4]` on `Fin 7`; `shell_no_fixed_point` | **NO — 7-point carrier, 2 orbits** |

### The exact restriction locus

**The rank-1 block is dropped at `09_LEAN_FORMALIZATION/D0/Extensions/LeptonSelectorExtension.lean:20`:**

```lean
/-- The two cycle/orbit sizes of the shell-torus `Ueff = blockdiag(4-cycle, 3-cycle)`. -/
def orbitSizes : List ℕ := [4, 3]
```

This is the first module in the chain where the block list drops from `[1,4,3]` (still present at
`BranchRowMinimalExtension.lean:111` as `blockRanks`) to `[4,3]`. Everything downstream
(`numBranches = orbitSizes.length = 2` at `LeptonBranchFixingNoGo.lean:30,32`; the 2<3 pigeonhole at
`LeptonBranchFixingNoGo.lean:45-55`) inherits the drop from this one line. The rank-1 `1` is simply
not written into `orbitSizes`.

### Classification: **SILENT** (with a downstream CONVENTION dressing, no FORCED derivation)

- **SILENT at the locus.** Line 20 is a bare definitional literal `[4, 3]`. No comment on the line,
  and no clause in the module header (`LeptonSelectorExtension.lean:3-14`), records *why* the `1` is
  excluded. The header explains the *orbit-keyed exponent* facts (`4-cycle ↦ 1/4`, `3-cycle ↦ 1/3`,
  `1/4 ≠ 1/3`) and the circularity of the "unique selector" route, but never states a reason for
  omitting the trivial block from the orbit list. (Grep for `exclude|drop|remove|discard` in this
  file returns only line 7's unrelated "excludes the (4,3) block swap"; there is no statement of the
  E₀-exclusion reason.)

- **What plays the role of a reason, downstream, is a CONVENTION dressing — not a derivation.** The
  carrier is *inherited by name* as "the shell-torus `Ueff = blockdiag(4-cycle, 3-cycle)`"
  (`LeptonSelectorExtension.lean:19`, `LeptonBranchFixingNoGo.lean` header line 9). The nearest thing
  to a justification is the observation, one module later, that this 7-point σ "has NO fixed point,
  so there is no regular/unramified (electron index-`0`) third orbit inside the 7-point shell-torus"
  (`LeptonBranchFixingNoGo.lean:39-41`, `shell_no_fixed_point`). But this is a **consequence** of
  having already chosen the 7-point (4,3) carrier, not a **cause** of excluding E₀: the "no fixed
  point" fact *detects* that E₀ is absent from the chosen carrier; it does not *derive* that E₀ must
  be excluded. The choice to build the no-go on the 7-point (4+3) carrier rather than the 8-point
  (1+4+3) full Q₈ system is made — silently — at `orbitSizes := [4, 3]`.

- **Not FORCED.** No derivation is cited anywhere in the chain for *why the carrier is the 7-point
  restriction rather than the full 8-dimensional Q₈ regular representation.* W3 already recorded
  (`TASK_W3_REPORT.md` §A.3, lines 74-88) that `1+4+3 = 8 = dim ℂ[Q₈]`, `4+3 = 7` = the carrier, and
  `8−7 = 1` = exactly the dropped E₀; and that the two-cycle carrier is "primitive as a pair of
  return cycles, not a quotient." The corpus supplies the (4,3) carrier as a *given* (the
  companion-cover `C4 × R3`, `RamificationFromUeEffCompanion.lean:26-33`), and separately supplies
  the full (1,4,3) system with E₀ (`Q8Terminal.lean`). It never records a step that takes (1,4,3) and
  *derives* the deletion of E₀ to reach (4,3). The two objects sit side by side; the no-go picks the
  smaller one without a cited reason.

**Restriction-locus verdict: SILENT.** `LeptonSelectorExtension.lean:20` drops the rank-1 block with
no recorded reason. The downstream `shell_no_fixed_point` (`LeptonBranchFixingNoGo.lean:41`) is a
*confirmation that E₀ is absent from the already-chosen 7-point carrier*, not a *derivation that E₀
must be dropped* — so it does not upgrade the locus to FORCED, and at best supplies a post-hoc
CONVENTION rationale.

---

## (c) What survives of the no-go against Branch(3) = {E₀, E₄, E₃}

The no-go (`LeptonBranchFixingNoGo.lean:45-55`) proves three impossibilities *for Branch(2)*:
no injection `Gen(3) ↪ Branch(2)`, no surjection `Branch(2) ↠ Gen(3)`, no bijection
`Branch(2) ≃ Gen(3)`. Restate each for Branch(3) = {E₀,E₄,E₃} (the full Q₈ system,
`Q8Terminal.lean:13-17`) vs Gen(3):

1. **Cardinality (inj/surj/bij).** With |Branch| = 3 = |Gen|, *all three maps become
   cardinality-admissible*. A bijection `Fin 3 ≃ Fin 3` now exists (re-verified: three distinct
   sizes, count 3 = count 3, python3 above). The entire pigeonhole content of
   `LeptonBranchFixingNoGo.lean` — which turns entirely on `numBranches = 2 < 3 = numGenerations`
   (`LeptonBranchFixingNoGo.lean:32-33,64`) — **evaporates the moment E₀ is re-admitted.** Nothing of
   the cardinality no-go survives against Branch(3).

2. **Size-keyed labelling on the Q₈ side is label-free.** The sizes `(1,4,3)` are pairwise distinct
   (`TypedRepresentationFunctor.lean:53-55` `q8_ranks_distinct`; `Q8Terminal.branch_orders`
   traces `1,4,3`), and the exponent row `(0,1/4,1/3)` is pairwise distinct
   (`Lepton.lean:34-35`, `BranchRowMinimalExtension.lean:113`). So the size→exponent map
   `{1↦0, 4↦1/4, 3↦1/3}` is canonical and needs no choice on the Q₈ side. The
   exhaustive 3! test confirms exactly one size-compatible assignment
   (`BranchRowMinimalExtension.lean:128-129`, `exhaustive_row_test` = 1). The Q₈ triple is thus an
   **intrinsically-ordered** object (ordered by rank).

3. **Is there scene-side structure distinguishing the three generations beyond count 3?** The
   scene-side generation triple is **rank-only / S₃-symmetric**:
   - `PhasonStrainGenerations.lean:27-29,41-43` gives `Fintype.card PhasonMode = 3` and
     `GenerationPhasonMode = PhasonMode` — a bare 3-element carrier, **no order, no distinguishing
     label** attached to the three modes.
   - `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`
     (`FinitePathRepresentation.lean:34-57`) states it outright: the generation count 3 is "the
     multiplicity of the trivial isotype — a rank-only number," the block is `M₃` with commutant
     `dim 9 > 1` = "`GL(3)` basis freedom," and it exhibits two admissible role assignments
     `assignA = [0,1,2] ≠ assignB = [1,0,2]` (`FinitePathRepresentation.lean:46-49`). Header
     (`LeptonBranchFixingNoGo.lean:20-21`) cites this as "the 3 generations are rank-only with
     `GL(3)`/`S₃` label-freedom."

   **Countervailing note (a partial distinguisher exists on the *typed* side).**
   `TypedRepresentationFunctor.lean:31-73` claims that adding the typed degree operator
   `D = diag(24,22,20)` (the zone degrees) collapses the commutant from `dim 9` to `dim 3`
   (`typed_frame_reduces_commutant`, line 73), i.e. on the *typed* source the three generation lines
   ARE pairwise distinguished by an ordered tag (24>22>20). This is a scene-side ordered triple that
   could, in principle, be matched to the Q₈-ordered triple — so the "purely S₃-symmetric" reading is
   true of the *raw* R1 rep but **not** of the *typed* frame. Whether the zone-degree order is itself
   canonical, and whether it is licensed to key the generation↔branch map, is not established in the
   chain (the typed functor module is flagged CORE/decidable for the *linear-algebra* facts only,
   `TypedRepresentationFunctor.lean:22-25`).

**What survives:** *nothing of the cardinality pigeonhole* survives against Branch(3). What remains is
a **matching / naming** question: the Q₈ triple is intrinsically ordered by rank `(1,4,3)`; the raw
scene triple is unordered/S₃-symmetric (`FinitePathRepresentation.lean:41,49`); a *typed* scene
ordering exists (`TypedRepresentationFunctor.lean:73`) but its canonicity and its right to key the map
are not established. So the residual object is a bijection between an ordered triple and an
(un- or ambiguously-)ordered triple — a naming freedom, consistent with the T2′ reading — **not** an
existence gap.

---

## (d) Residual-gap statement (one sentence)

Once the full (1,4,3) Q₈ system is used, the electron branch E₀ exists internally and the cardinality
pigeonhole vanishes, so the only thing the X5 contract still adds is a **canonical bijection between
the intrinsically-rank-ordered Q₈ triple (1,4,3) and the S₃-symmetric scene generation triple
(Tr(T²)=3)** — an identification/naming map, not an existence proof.

---

## (e) Step-4 minimality re-test — PLAN ONLY (do NOT enact)

If the (c) reading holds, the X5 contract's content would reduce from "postulate the third branch /
the full branch→row assignment operator" to the strictly weaker "postulate the Q₈-triple ↔
scene-triple identification." Assessment of whether it is strictly weaker, and what a re-scope would
touch — **as a plan only, no edits proposed to any repo file:**

**Is it strictly weaker?** Plausibly yes on the Q₈ side: the current contract postulates a
`Fin 3 → Fin 3` bijection over 5 laws with a `3!`-space collapsed to 1 by size-keying only *after*
E₀ is re-admitted; a bare "identify the two triples" postulate would drop the existence/absence
concern entirely and reduce to fixing the residual S₃ (or, if the typed order is admitted, to
verifying a single order-match). But it is **not unconditionally weaker**: it *adds* an obligation the
current contract hides — namely that E₀ (a rank-1 *projector/isotype*, `Q8Terminal.lean:24`) is the
same object as a scene *generation mode* (`PhasonStrainGenerations.lean:38`), which is itself an
unpaid identification (W3 §(d) mode-2 caveat, `TASK_W3_REPORT.md:189-205`).

**Lean files/claims a re-scope would touch (inventory only):**

- `09_LEAN_FORMALIZATION/D0/Extensions/X5/Lepton.lean` — the contract `laws` list
  (`Lepton.lean:20-22`), the `B3` bijection model (`Lepton.lean:27-29`), the deletion test
  (`Lepton.lean:40-43`), and the terminal theorem (`Lepton.lean:46-51`): a re-scope would change the
  postulated object from "branch→row bijection" to "Q₈-triple↔scene-triple identification."
- `09_LEAN_FORMALIZATION/D0/Extensions/LeptonSelectorExtension.lean:20` (`orbitSizes := [4,3]`) and
  `09_LEAN_FORMALIZATION/D0/Extensions/LeptonBranchFixingNoGo.lean:30-70` — the entire 2<3 pigeonhole
  would be superseded (it is *about* the restricted carrier); a re-scope onto Branch(3) would
  need these re-expressed against `[1,4,3]` or explicitly retained as "true on the restricted carrier
  only" (the W2 report already flags this posture, `TASK_W2_REPORT.md:161-165`).
- `09_LEAN_FORMALIZATION/D0/Matter/PhasonStrainGenerations.lean:27-43` and
  `09_LEAN_FORMALIZATION/D0/Representation/FinitePathRepresentation.lean:34-57` — the scene-side
  triple; a re-scope's identification target lives here, and the S₃ label-freedom
  (`FinitePathRepresentation.lean:49`) is exactly the residual to be fixed.
- `09_LEAN_FORMALIZATION/D0/Representation/TypedRepresentationFunctor.lean:31-73` — if the typed
  zone-degree order is admitted as the scene-side ordering, this module supplies the ordered
  distinguisher the identification would rely on; its status (canonicity of the order) would have to
  be settled first.
- Prose/status: `01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY/0001__04.v15__…md:170-171`
  and `04_VERIFICATION/X5_CLAIM_OWNER_MATRIX.csv:5` (`D0-X5-LEPTON-CONTRACT-001,…,CERT-CLOSED`) both
  describe the third datum as "genuinely external" — a re-scope would put these prose owners in
  tension with the "E₀ exists internally" reading, so they are in scope for the *statement* of any
  re-scope even though **this audit edits none of them.**

This is a re-scope inventory only. No claim is made that the re-scope is correct, and no file is
touched.

---

## (f) Skeptic's paragraph — the strongest reason T2′ is still wrong (mandatory)

The strongest case against T2′ is that **E₀ and the third *generation* are not the same kind of
object, and the corpus's "external" bookkeeping is right for a reason the T2′ reading papers over.**
E₀ is the *trivial isotype* of `Q₈ = Ω₈` — a rank-1 projector `⅛Σ_q L_q` living inside the terminal
alphabet's regular representation (`Q8Terminal.lean:24`), whose defining property is that it is
*group-invariant* (the trivial rep). The three *generations*, by contrast, are the multiplicity-3
trivial-isotype block of the **scene** automorphism group `S₉×S₁₁×S₁₃` acting on `ℂ³³`
(`FinitePathRepresentation.lean:34-41`) — a different group, a different carrier, and (crucially) a
block that is *itself* rank-only with full `GL(3)`/`S₃` freedom. So "E₀ exists internally, therefore
the third generation exists internally" quietly conflates *a rank-1 sub-block of the Q₈ terminal
Fourier system* with *one of three indistinguishable copies inside a completely different scene rep* —
exactly the mode-2 double-count W3 already flagged (`TASK_W3_REPORT.md:186-205`). On this reading the
X5 postulate is NOT reducible to a mere naming map: the honest gap is precisely the assertion that
these two "3"s are the same 3, and that assertion carries an *existence-of-a-canonical-identification*
burden (there is no scene-native map from Q₈-Fourier ranks to `S₉×S₁₁×S₁₃` isotypes anywhere in the
chain), not just an S₃-labelling burden. Worse, the one place the scene triple *is* ordered — the
typed zone-degrees `24,22,20` (`TypedRepresentationFunctor.lean:33,73`) — is a *typed* addition whose
own canonicity is unestablished, and matching `(1,4,3)` to `(24,22,20)` is itself a further unpaid
choice of *which* order-preserving convention (rank-ascending? descending?) applies. Finally, the
corpus's own prose still books the third datum as "genuinely external (postulated HYP)"
(`BOOK_04 …0001__04.v15__…md:170`), and `D0-X5-LEPTON-CONTRACT-001` is carried as `CERT-CLOSED`
(`X5_CLAIM_OWNER_MATRIX.csv:5`) *with* that externality — so T2′ must argue that a machine-checked,
CERT-CLOSED owner is mis-describing its own content, which is a heavy burden the (a)-level reading
(the contract postulates an *assignment*, `Lepton.lean:8`) supports but does not by itself discharge.

---

## Appendix — source ledger (file : line)

| Item | Source |
|---|---|
| X5 contract = bijection `B₃`, "assigning branches to rows", "including electron branch" | `09_LEAN_FORMALIZATION/D0/Extensions/X5/Lepton.lean:6-11,18-31` |
| X5 model non-vacuous + deletion-minimal (μ↔τ transposition) | `…/X5/Lepton.lean:37-43`; pattern `…/X5/PrimitiveContract.lean:28-47` |
| X5 owner status CERT-CLOSED, external attribution | `04_VERIFICATION/X5_CLAIM_OWNER_MATRIX.csv:5`; `01_BOOKS/…/0001__04.v15__…md:170-171` |
| Full (1,4,3) system incl. E₀ = trivial-rep rank-1 electron | `…/UnifiedFiniteCore/Q8Terminal.lean:13-17,24,68-70` |
| (1,4,3) simultaneous in Fourier ranks + return orders | `…/UnifiedFiniteCore/UnifiedTheorem.lean:31-36,39` |
| `blockRanks := [1,4,3]`, `exponentRow := [0,1/4,1/3]` (E₀ still present) | `…/LeptonClosure/BranchRowMinimalExtension.lean:110-113` |
| **Restriction locus — `orbitSizes := [4,3]` (E₀ dropped, SILENT)** | `…/Extensions/LeptonSelectorExtension.lean:19-20` |
| Downstream 2<3 pigeonhole + `shell_no_fixed_point` (detects, not derives) | `…/Extensions/LeptonBranchFixingNoGo.lean:30-41,45-55,64` |
| Scene triple = bare 3-element carrier | `…/Matter/PhasonStrainGenerations.lean:27-43` |
| Scene triple rank-only / S₃ / GL(3) label-free, 2 admissible assignments | `…/Representation/FinitePathRepresentation.lean:34-57` |
| Typed zone-degree ordering `(24,22,20)` distinguishes generations (typed only) | `…/Representation/TypedRepresentationFunctor.lean:31-33,53-55,73` |
| Row "exact and THE (electron unramified, muon 1/4, tau 1/3)" | `…/Matter/LeptonPuiseuxUniquenessObstruction.lean:73` |

*Arithmetic re-run (python3 3.9.6):* `1+4+3 = 8 = dim ℂ[Q₈]`; `4+3 = 7` = restricted carrier;
`8−7 = 1` = dropped E₀; sizes `(1,4,3)` pairwise distinct; `|Branch(3)| = 3 = |Gen(3)|` ⇒ bijection
cardinality-admissible.

*Discipline note:* READ-ONLY. No repo file edited outside `_TASKS_CENTER_ATTACK/`. No status/claim
edits. No "derived/confirmed/forced/closed" promotion applied to T2′.
