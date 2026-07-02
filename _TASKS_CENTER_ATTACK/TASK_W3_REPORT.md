# TASK W3 — Adversarial provenance audit of the 7-point shell-torus carrier

**Mandate:** determine, with citations, where the 7-point carrier `Ueff = blockdiag(4-cycle, 3-cycle)`
comes from, and the exact forcing scope of the witness rule `Ω₈ + ω₀ = V₉`. This audit GATES candidate
theorem **T2** (README lines 10–12: "the third lepton generation is internal: the witness/addressability
rule (Ω₈+ω₀=V₉) extends the 7-point shell-torus to 8 points with a forced fixed point"). Run with intent
to **refute**. No promotion language (BOOK_00 §00.8/§00.9). Every claim carries a file + line citation.

---

## (a) Provenance chain of the 7-point carrier

### A.1 The carrier as it enters the no-go chain

The frozen carrier is defined identically in three Lean modules as `σ = (0 1 2 3)(4 5 6)` on `Fin 7`:

- `09_LEAN_FORMALIZATION/D0/Matter/LeptonBranchAssignmentNoGo.lean:22`
  — `def sigmaA : Fin 7 → Fin 7 := ![1, 2, 3, 0, 5, 6, 4]` ("4-cycle on `{0,1,2,3}`, 3-cycle on `{4,5,6}`").
- `09_LEAN_FORMALIZATION/D0/Extensions/LeptonBranchFixingNoGo.lean:37` — `def sigmaShell` (same vector).
- `09_LEAN_FORMALIZATION/D0/Matter/LeptonFiniteGreenResolventOwner.lean:31–38`
  — `Ueff : Matrix (Fin 7) (Fin 7) ℚ`, the `7×7` permutation `diag(P₄, P₃)`.

Its invariants: `det(I − z·Ueff) = (1 − z⁴)(1 − z³)`, order `lcm(4,3) = 12`
(`LeptonFiniteGreenResolventOwner.lean:14–16,40–41`); cycle type `(4,3)` is the **unique** partition of 7
with lcm 12 (`BranchRowMinimalExtension.lean:38–50`, `return_orders_forced`; independently re-checked in
this audit — the only order-12 partition of 7 is `[4,3]`). It has **no fixed point**
(`LeptonBranchFixingNoGo.lean:39–41`, `shell_no_fixed_point`), so the electron/index-0 branch is not
inside the carrier: "there is no in-carrier third (electron, index-`0`) branch — while `numGenerations = 3`
… the third datum is genuinely EXTERNAL (postulated HYP in `D0-X5-LEPTON-CONTRACT-001`)"
(`LeptonBranchFixingNoGo.lean:14–22`).

### A.2 Why "4" and "3"? — the two block sources (NOT a basepoint deletion)

The two cycle lengths trace to `D0-EDGE-RAMIFICATION-001`, the companion cover `C4 × R3`:

- `09_LEAN_FORMALIZATION/D0/Edge/RamificationFromUeEffCompanion.lean:26–33` — `companionC4` (charpoly
  `x⁴ − λ`, the **"4-cycle terminal-capacity block"**) and `companionR3` (charpoly `x³ − λ`, the
  **"3-cycle scene-rank block"**).
- `09_LEAN_FORMALIZATION/D0/Matter/LeptonGreenPuiseuxOwner.lean:10–16,58–62` — the cover "yields the
  exponent row `(p_e, p_μ, p_τ) = (0, 1/4, 1/3)`: the electron is **unramified** (regular, index 0)".

The **"4"** is *terminal role capacity* (the four A,B,C,D roles, `|ABCD| = D₂×D₂ = 4`, BOOK_01 §01.20 line 3–8);
the **"3"** is *scene rank* (`rank(A) = 3`, BOOK_01 §01.8 lines 60–66). Neither number is obtained by
removing a point from a bigger set. The theory map is explicit that `7 = 4+3` is an **auxiliary** cover,
not a quotient/restriction of a larger physical carrier:

> "It is not a claim that the 359-edge Hilbert space itself has dimension 359+4+3… The physical edge
> dimension remains 359; the companion blocks are auxiliary for the ramification cover attached to the
> resolvent." — `03_THEORY_MAP/D0_RAMIFICATION_FROM_EDGE_UEFF_COMPANION_OPERATOR.md:22–24`

**Negative-provenance result (searched, not found):** no file anywhere near the carrier describes the 7
points as produced by *removing a basepoint/witness*. A corpus-wide grep for basepoint/witness/point
deletion adjacent to torus/carrier/lepton returned only the scene-construction usages of ω₀ (§00.5, §01.8,
§01.20) and the TASK_W* briefs themselves — no `7+1`, "delete", "quotient by ω₀", or "restrict" against the
lepton carrier. So on the literal reading, **step (a) of the T2 legitimacy test passes: the 7-point carrier
was not itself produced by removing a basepoint.**

### A.3 The decisive structural fact — the "1" (electron) already exists one level up, from Ω₈, WITHOUT ω₀

There is a *second, independent* construction of the same branch data that already contains a third,
rank-1 branch — and it does so from `Q₈ = Ω₈` alone, with the witness ω₀ playing **no** role in producing it:

- `09_LEAN_FORMALIZATION/D0/UnifiedFiniteCore/Q8Terminal.lean:10–17,68–80`:
  `ℂ[Q₈] ≅ ℂ⁴ ⊕ M₂(ℂ)` gives **three** orthogonal idempotents `E₀,E₄,E₃` summing to `I`, with
  **ranks `(1,4,3)`** (`branch_orders`, traces `1,4,3`). "This is the branch-order signature `(1,4,3)` of
  the chain, **derived from `Q₈` alone**." The rank-1 block is `E₀ = ⅛Σ_q L_q`, the **"trivial-rep
  projector (rank 1)"** (line 24), fixed as `Q₉ ↔ E₀ (rank 1, unramified)` = the electron (line 16).
- `09_LEAN_FORMALIZATION/D0/UnifiedFiniteCore/UnifiedTheorem.lean:31–36`: "the branch orders `(1,4,3)`
  … appear **simultaneously** in the `Q₈` Fourier ranks and the return orders."
- The same `(1,4,3)` is consumed as data in `Representation/TypedRepresentationFunctor.lean:13,35` and
  `LeptonClosure/BranchRowMinimalExtension.lean:110–113` (`blockRanks := [1, 4, 3]`,
  `exponentRow := [0, 1/4, 1/3]`).

Arithmetic (re-verified in this audit): `1 + 4 + 3 = 8 = |Ω₈| = dim ℂ[Q₈]`; the two nontrivial return
cycles `4 + 3 = 7` = the shell-torus carrier; and `8 − 7 = 1` = exactly the dropped rank-1 trivial-rep
block `E₀`.

**So the 7-point carrier IS the restriction of the `(1,4,3)` Q₈-Fourier system with the rank-1 trivial-rep
block E₀ removed.** The "missing electron" that T2 wants to re-supply is precisely `E₀`, the trivial
isotype of `ℂ[Q₈]`. Crucially, **`E₀` is NOT the witness `ω₀`**: `ω₀` is a separate 9th point,
`V₉ = Ω₈ ⊔ {ω₀}` (`Q8Terminal.lean:10`; BOOK_01 §01.20 line 24), whereas `E₀` is a rank-1 projector *inside*
the 8-dimensional regular representation of `Ω₈` itself. The electron block and the witness point are two
different objects, of two different sizes (both happen to equal 1), living at two different levels.

**Provenance verdict.** The 7-point carrier is **primitive as a *pair of return cycles* (4 = terminal
roles, 3 = scene rank), not a quotient obtained by deleting the witness ω₀.** It is, however, a
*trace-level restriction* of the pre-existing `(1,4,3)` Q₈-Fourier system that already carries the rank-1
electron block E₀ — a block sourced from Ω₈, not from ω₀.

---

## (b) Witness-rule scope verdict: **SCENE-ONLY**

Every corpus instance of the rule instantiates it on exactly one alphabet, `Ω₈ → V₉`, as a graph-birth /
shell-basepoint step. There is no instance in which ω₀ is attached to an arbitrary terminal or branch
readout register.

**Strongest (most general-sounding) statement** — BOOK_00 §00.5 (identical wording in the source file and
the compiled book):
> "Observed addressability requires a witness/basepoint: `Ω₈ + ω₀ = V₉`."
> — `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/0008__00.5__terminal-alphabet-and-scene-orientation.md:18–22`
> (also `…/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:302–306`).

Read in isolation, "Observed addressability requires a witness" *sounds* like a general law. But it is
stated only of the scene alphabet `Ω₈`, and its own owner-section immediately narrows it:

**Narrowest (owning) statement** — BOOK_01 §01.20:
> "A reusable **shell** also requires a stationary marked witness section `ω₀`. Hence `V₉ = Ω₈ ⊔ {ω₀}`,
> `|V₉| = 9`. … The construction rules out alternatives: **`V₈` has no basepoint**…"
> — `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH/0023__01.20__…md:21–36`

And BOOK_01 §01.8 fixes ω₀ as a *scene-construction* object, not a downstream law:
> "the `+1` is the **graph-birth basepoint marker** `V₉ = Ω₈ + ω₀` (this section)… Book 01 stops at
> construction of the finite incidence graph. The action, boundary, matter, gravity and cosmology books may
> use this scene, but they may not refit it."
> — `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH/0010__01.8__…md:39,69`

The one Lean appearance ties ω₀ to the scene as well — `V₉ = {ω₀} ⊔ Ω₈` used to *set up* the Q₈ Fourier
system (`Q8Terminal.lean:10`), not to add a point to any lepton branch register.

**Verdict: SCENE-ONLY.** The rule is stated for the scene alphabet `Ω₈`/`V₉` (graph-birth of `K(9,11,13)`).
The general-law reading is *available as a rhetorical phrasing* in §00.5 ("Observed addressability
requires a witness") but is (i) never once applied to a branch/terminal readout carrier anywhere in the
corpus, and (ii) explicitly scoped by its owner sections to the reusable shell / graph birth. There is a
residual ambiguity — §00.5's wording is generic enough that a reader *could* try to extend it — but the
weight of the owning sections (§01.8, §01.20) is SCENE-ONLY, and T2 would have to *manufacture* the general
reading, which the corpus does not supply.

---

## (c) Prior-art verdict: a rank-1 / trivial / unramified third branch WAS present and IS handled — as external, not internal

**Was a fixed point / trivial orbit / unramified branch ever tried?** Yes — repeatedly, and it is *already*
the electron branch in the (1,4,3) reading:

1. **It exists as the trivial-rep block `E₀` (rank 1, unramified).** `Q8Terminal.lean:16,24` — "`Q₉ ↔ E₀`
   (rank 1, unramified)", "the trivial-rep projector (rank 1)". This is the `p_e = 0` unramified electron
   entry, and it is declared **exact/THE**: `LeptonGreenPuiseuxOwner.lean:14`, and
   `LeptonPuiseuxUniquenessObstruction.lean:73` — "the row is exact and THE (electron unramified, muon
   `1/4`, tau `1/3`)".

2. **Inside the 7-point carrier it was checked for and found absent — by design, then declared external.**
   `LeptonBranchFixingNoGo.lean:39–41` proves `σ` has no fixed point, so there is "no regular/unramified
   (electron index-`0`) third orbit inside the 7-point shell-torus: the third datum is external." The X5
   postulate then supplies the full three-row triple `(0, 1/4, 1/3)` **including** the electron branch,
   explicitly as a POSTULATE (HYP): `09_LEAN_FORMALIZATION/D0/Extensions/X5/Lepton.lean:6–11,18–24` —
   `PRIM-LEPTON-BRANCH-FIXING-OPERATOR`, "acting on the FULL three-row triple `(0, 1/4, 1/3)` (including
   the `0`/electron branch)."

**Was it rejected, and why?** It was not rejected as *false*; it was ruled **not constructible from the
2-orbit carrier data** and therefore booked as **external/postulated**, not internal. The recorded reason
is cardinality pigeonhole, quoted from the owning book:
> "The frozen shell-torus `Ueff = blockdiag(4-cycle, 3-cycle)` supplies exactly `numBranches = 2`
> orbit-branches … and has **no fixed point** — so there is no in-carrier third (electron, index-`0`)
> branch — while `numGenerations = 3`. … all three [inj/surj/bij] are impossible by cardinality … Hence
> `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` is *not constructible* from the frozen 2-orbit data; the third
> datum is genuinely external (postulated HYP in `D0-X5-LEPTON-CONTRACT-001`)."
> — `01_BOOKS/BOOK_04_…/0001__04.v15__active-matter-sector-law.md:170`
> (same text `…/0010__04.8__…md` block and `BOOK_04_SPECTRUM_MATTER…md:188`).

So the prior art is not "a fixed point was tried and killed as wrong" but "a fixed point was found *absent
from the 7-point carrier* and its data was moved to an external postulate." T2 is precisely a bid to
*internalize* that postulate. The prior-art record does not forbid T2, but it does show T2 must supply a
*forcing* for the third block that the corpus currently books as external.

---

## (d) Adversarial conclusion — the single weakest step of T2

**T2 does not die at the provenance gate (step-a survives): the 7-point carrier is not literally the result
of deleting the witness ω₀.** But T2 survives step (a) only by relabeling, and it fails at step (b). The
weakest step is stated plainly:

> **Single weakest step of T2: the witness rule `Ω₈ + ω₀ = V₉` is SCENE-ONLY, so using it to add an 8th
> point to a *lepton branch register* is an unlicensed transport of a scene-construction step to a
> different carrier — and even if that transport were granted, the point it adds (ω₀) is the wrong object:
> the electron block is the trivial-rep `E₀` sourced from Ω₈, not the witness ω₀.**

Two independent failure modes, either of which is fatal:

1. **Scope failure (b).** T2's premise ("the same rule applies to any terminal readout/branch register",
   README §W3 lines 16–18) is not supported. The rule is owned by §01.20/§01.8 as the *shell/graph-birth*
   basepoint and is never once applied to a branch register in the corpus. T2 needs the GENERAL-LAW reading;
   the corpus gives SCENE-ONLY. This is the weakest link.

2. **Wrong-object / double-count failure (a′).** The rank-1 "electron" block already exists as `E₀`, the
   trivial rep of `Q₈ = Ω₈`, with `1 + 4 + 3 = 8` and the carrier being the `4 + 3 = 7` nontrivial part
   (`Q8Terminal.lean:24,68–70`; `UnifiedTheorem.lean:31–36`). The correct "third branch" is therefore
   `E₀`, recovered by *un-restricting to the full Q₈ regular representation* — not by adding the separate
   9th witness point ω₀ (`V₉ = Ω₈ ⊔ {ω₀}`). T2 as phrased ("extends the 7-point shell-torus to 8 points…
   electron = witness branch", README lines 11–12) conflates `E₀` (size-1, from Ω₈) with `ω₀` (size-1,
   the 9th scene point). If T2 instead re-runs the Q₈-Fourier route it gets the electron for free — but
   then the "witness/addressability rule" is doing no work, and T2's headline mechanism (`Ω₈+ω₀=V₉`) is
   idle. Either the mechanism is scene-only and inapplicable (mode 1), or it is superfluous because the
   `(1,4,3)` block already supplies the electron without it (mode 2).

**Remaining honest caveat for the defence of T2.** Even granting SCENE-ONLY, T2 is not *logically*
impossible: a proponent could try to *prove* an addressability law for branch registers de novo (that is
what sibling task `TASK_W2` attempts — an 8-point witness monodromy). But nothing in the current corpus
forces it, and W2's brief already flags that "nothing here proves the 8-point carrier is forced"
(`_TASKS_CENTER_ATTACK/TASK_W2_witness_monodromy.md:48`). And even a proven 8-point extension would still
have to explain why its added point behaves like the *trivial-rep* rank-1 block `E₀` rather than a fixed
witness ω₀; the σ̂-fixing-ω₀ construction in T2's sketch yields a `{1,4,3}` orbit-size set by *fixing a
point*, which is a different object from the *trivial isotype* `E₀` (a rank-1 projector, not a fixed
carrier point). That identification is an additional unpaid obligation.

### One-line adversarial conclusion
T2 clears the narrow provenance gate (the 7-point carrier was not literally made by deleting ω₀), but it
**fails the scope gate**: the witness rule `Ω₈+ω₀=V₉` is SCENE-ONLY, so extending it to a lepton branch
register is unlicensed — and where a third electron block genuinely exists it is the trivial-rep `E₀` of
`Ω₈`, not the witness `ω₀`, so T2's stated mechanism is either inapplicable or idle.

---

## Appendix — source ledger (file : line)

| Claim | Source |
|---|---|
| 7-point carrier `σ=(0123)(456)` | `09_LEAN_FORMALIZATION/D0/Matter/LeptonBranchAssignmentNoGo.lean:22`; `…/Extensions/LeptonBranchFixingNoGo.lean:37`; `…/Matter/LeptonFiniteGreenResolventOwner.lean:31–38` |
| `(4,3)` is unique order-12 partition of 7 | `…/LeptonClosure/BranchRowMinimalExtension.lean:38–50` |
| No fixed point ⇒ electron external | `…/Extensions/LeptonBranchFixingNoGo.lean:14–22,39–41` |
| "4" = terminal roles; "3" = scene rank | `…/Edge/RamificationFromUeEffCompanion.lean:26–33`; BOOK_01 §01.20:3–8; §01.8:60–66 |
| `7=4+3` auxiliary, not a physical quotient | `03_THEORY_MAP/D0_RAMIFICATION_FROM_EDGE_UEFF_COMPANION_OPERATOR.md:22–24` |
| `(1,4,3)` Q₈-Fourier, E₀ = trivial rep rank-1 electron | `…/UnifiedFiniteCore/Q8Terminal.lean:10–17,24,68–80`; `…/UnifiedTheorem.lean:31–36` |
| `V₉ = Ω₈ ⊔ {ω₀}` (ω₀ is the 9th point, not E₀) | `…/UnifiedFiniteCore/Q8Terminal.lean:10`; BOOK_01 §01.20:21–26 |
| Witness rule, strongest phrasing | BOOK_00 §00.5:18–22 (`0008__00.5__…md`); `BOOK_00…md:302–306` |
| Witness rule, narrowest/owning phrasing | BOOK_01 §01.20:21–36; §01.8:39,69 |
| Electron row `(0,1/4,1/3)` declared exact/THE | `…/Matter/LeptonGreenPuiseuxOwner.lean:14`; `…/LeptonPuiseuxUniquenessObstruction.lean:73` |
| Third row POSTULATED (HYP), includes electron `0` | `…/Extensions/X5/Lepton.lean:6–11,18–24` |
| Reason for externalizing the third datum (pigeonhole) | BOOK_04 `0001__04.v15__…md:170`; `BOOK_04_SPECTRUM_MATTER…md:188` |
| W2 concedes 8-point carrier not forced | `_TASKS_CENTER_ATTACK/TASK_W2_witness_monodromy.md:48` |

*Discipline note:* read-only audit; no repo file edited outside `_TASKS_CENTER_ATTACK/`. No
"confirmed/derived/forced/closed" promotion applied to T2. Numeric arithmetic (`1+4+3=8`, `4+3=7`,
`8−7=1`, unique order-12 partition of 7 = `[4,3]`) re-derived independently under python3 3.9.6.
