# DEEP-M synthesis memo — D0-GEN-MASS-001 & D0-GENERATION-RAYS-001

Deep campaign, batch M. Genuine per-no-go synthesis (not a re-tag). Compute-first,
every ownership claim verbatim-cited and verified on disk. Can-fail check:
`_TASKS_CENTER_ATTACK/deep_m_genmass_check.py` (base PASS + 6/6 mutants killed).

Date: 2026-07-06. No git commit, no registry/book edits — row-note text proposed only.

---

## NO-GO 1 — D0-GENERATION-RAYS-001

### Decisive proved content (verbatim, file:line)

Lean `09_LEAN_FORMALIZATION/D0/Spectrum/GenerationSpectralRays.lean`:

- `:20-21` `def isCanonical : CandidateOperator → Prop | _ => False`
- `:23-26` `theorem no_canonical_operator_among_candidates : ∀ op : CandidateOperator, ¬ isCanonical op`
- `:49-50` `def searchResult : SearchResult := SearchResult.NoCanonicalOperator`
- `:61-66` `theorem NO_GO_GENERATION_RAYS_UNDEFINED : GenerationSpectralRayNoGo`

The 5 candidates (`:12-18`): `graphLaplacian, signedIncidenceDirac, cliqueHodge,
orientedBoundary, chargeWeightedDirac`. Each has `candidateSpectrum … = none` (`:28-34`).

Headline: **the bare `K(9,11,13)` spectral-cluster route to a generation operator is a
no-go — no canonical operator among the five candidates, and none has an exact
(φ-cluster) spectrum.**

### Five distinct attack lines

**(a) LIFT — turn the border into a positive result.** The negative result *is already
lifted* by the corpus, and the lift is the correct owned object: the generation index is
not read off any bare spectral operator but off the **projective closure `P¹(F₂)` of the
minimal two-branch defect plane** (`D0-GEN-INDEX-001`, CORE-FORMALIZED). Lean
`BranchDefectProjectiveGeneration.lean:52-53` `exactly_three_projective_branch_defect_generations : Fintype.card BranchRay = 3`
and `:49-50 defectAction_order_three`. So RAYS is the *record of the route that had to be
abandoned* to reach the owned index — a genuine boundary, not a lift of its own. **LIFT
does not apply to RAYS itself; the positive object it points at is already owned elsewhere.**

**(b) CLOSE — is the missing "canonical generation operator" owned anywhere?** Hard grep.
The only positive-looking hit is `D0-CANONICAL-OP-001` (`vp_canonical_operator_search.py`,
CERT-CLOSED). Reading it (`:1-10` verbatim) shows it is the *same* negative result, exactly
gated: *"a finite search over candidate operators on `K(9,11,13)` concludes that none is
forced by D0's algebraic rules alone (each candidate still needs an auxiliary sign / gauge /
orientation / embedding choice), and the bare graph spectrum cannot realise the irrational
phi-scaling cluster rule the generation claim would require."* **CLOSE fails — the missing
object is not owned; a second independent certificate confirms its non-existence.**

**(c) DECOMPOSE — is it a constituent of an owned structure read differently?** Yes, and this
is the sharpest reading. The bare Laplacian spectrum of `K(9,11,13)` has the exact closed form
(complete multipartite, `vp_canonical_operator_search.py` verbatim + verified numerically):
`{0¹, 20¹², 22¹⁰, 24⁸, 33²}` — **5 distinct *integer* eigenvalues**. A φ-scaling generation
cluster is irrational (Q(√5)). An integer spectrum can never host it. So the RAYS no-go
*decomposes* into a concrete integer-vs-irrational obstruction on an owned object (the scene
Laplacian). This is the mechanism, but it is still an obstruction, not a construction.

**(d)/(e) GENUINE-BOUNDARY-PROVEN.** After (a)-(c), the honest verdict. The exact owned no-go
that establishes impossibility is the **`2 < 3` carrier-count wall**, the same one that closes
the Lane-L NO-GO (`BOOK_04 …:188` verbatim): the frozen shell-torus
`Ueff = blockdiag(4-cycle, 3-cycle)` supplies `numBranches = 2` orbit-branches (Puiseux
exponents `1/4 ≠ 1/3`), while `numGenerations = 3` (Lean `numGenerations_eq_three`, `:33`;
= the `Tr(T²)=3` trivial-isotype multiplicity in `BOOK_04:188` — two distinct facts, not one
Lean object). A branch→generation full-row
operator would be an injection `Gen(3)↪Branch(2)`, surjection `Branch(2)↠Gen(3)`, or bijection
`Branch(2)≃Gen(3)` — **all three impossible by cardinality**, machine-checked in Lean by `decide`
(`D0/Extensions/LeptonBranchFixingNoGo.lean:46,51,55`; `numBranches_eq_two` `:32`,
`numGenerations_eq_three` `:33`), with the Python shadow `vp_five_primitive_no_branch_to_generation_shortcut.py:20-23`
(`assert F(1,4)≠F(1,3) and 2<3` — a Python assert, *not* a Lean `decide`). RAYS is the
*spectral-route* face of this one wall (the bare integer spectrum
carries no φ-cluster; the branch data carries only 2 orbits): the third generation datum is
genuinely **external**.

- **Owned no-go object:** `no_canonical_operator_among_candidates` + `D0-CANONICAL-OP-001`
  (K-Laplacian `{0,20,22,24,33}` integer spectrum) + the `2<3` cardinality wall
  (`vp_five_primitive_no_branch_to_generation_shortcut.py`).
- **Honest external datum imported (I/O typing):** the *choice of generation operator* /
  the third (electron, index-0) branch is a postulated HYP — `D0-X5-LEPTON-CONTRACT-001`,
  the "third datum is genuinely external" of `BOOK_04:188`. **Input:** scene `K(9,11,13)` +
  2-orbit shell-torus data (owned). **Output blocked:** a canonical φ-cluster generation
  operator (external).

### WORKED VERDICT — GENUINE-BOUNDARY-PROVEN (route abandoned in favour of owned `P¹(F₂)` index)

Exact object: `no_canonical_operator_among_candidates` (integer-spectrum obstruction, cert
`vp_canonical_operator_search.py`) ⊕ the `2<3` carrier-count wall. Not open — the count-3 is
owned (`D0-GEN-INDEX-001`), only the *spectral-operator route* is closed.

---

## NO-GO 2 — D0-GEN-MASS-001

### Decisive proved content (verbatim, file:line)

Registry `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:37`:
> "Core index is proved; physical masses/Yukawa hierarchy/PDG clustering require additional
> physical input and are not core theorems."

Lean `BranchDefectProjectiveControls.lean:5-14` closes only the *index* structure
(`exactlyThree`, `actionOrderThree`, `cardDefectGen = 3`) via
`branch_defect_projective_proof_closed`. The `realLift` (`BranchDefectProjectiveGeneration.lean:61-64`)
sends the 3 generations to `(pPlus, pMinus, branchGap)` but proves **no** ratio.

### Five distinct attack lines

**(a) LIFT — can the border become a positive property?** *Partially, and this is the real
find.* The three generations are NOT weight-blind: Lean `D0.Defect.Pi0BranchDefect` proves
two exact scene facts about the lift targets — `pPlus_add_pMinus : pPlus + pMinus = 1`
(`:14-17`, golden closure `φ⁻¹+φ⁻²=1`) and `branchGap_eq_two_delta0 : branchGap = 2·δ₀`
(`:19-22`). So the *branch-weight structure* `(φ⁻¹, φ⁻², φ⁻¹−φ⁻²)` is derived-core. **But**
these are branch/defect weights, **not** the physical mass ratios `m_μ/m_e, m_τ/m_μ`. The lift
reaches a real 3-weight structure; it does **not** reach the PDG hierarchy. Over-claiming the
former as the latter is exactly the trap the owner rejects — so LIFT succeeds only for the
weight-triple, and that is a *different object* from the no-go's target.

**(b) CLOSE — is the mass hierarchy owned anywhere?** Hard grep for derived Yukawa / mass
ratio. Two honest hits, both bounded: (i) the mass=1/period **ontology** `m_rest = m_0·W`
(`04.6.π.6`) — the per-particle winding `W` is stated verbatim as *"a physical input
(a passport/bridge), not core theorems … W is not recovered from any internal derivation"*
(`0008__04.6…:96`). (ii) exactly **one** ratio is group-cardinality-forced: `m_s/m_d = 20`
via `φ_E(44) = |(ℤ/44)*| = 20` (`04.5.5`, THE 04.5.5.D). That is a *counting invariant*, not
the generation mass hierarchy — a single Cabibbo-sector integer, cross-checked (not supported)
by FLAG. **CLOSE fails for the generation hierarchy: `W` is provably not owned; the one owned
ratio is a group order, not a Yukawa spectrum.**

**(c) DECOMPOSE — read as a constituent of an owned structure.** Yes — and this yields the
precise I/O split. The GEN-MASS object decomposes into:
  - **DERIVED-CORE:** generation **count = 3** (Lean `defect_generation_card : card = 3` by
    `rfl`, `BranchDefectProjectiveGeneration.lean:66-68`; = the *separate* `Tr(T²)=3` trivial-
    isotype reading in `BOOK_04:188`, not the same Lean object; `D0-GEN-INDEX-001`); the
    **mass=inverse-period ontology** `mass = τ⁻¹` with the certified quantum `m_0·t_0 = 1`
    exact in Q(φ), `m_0 = 2π_0 = (12/5)φ²`, `t_0 = (5/12)φ⁻²` (`04.6.π.5`, cert
    `vp_mass_chain_alpha.py`); the branch-weight triple `(φ⁻¹, φ⁻², gap)` with `Σ=1` and
    `gap = 2δ₀`.
  - **IMPORTED (passport):** the per-particle winding `W`, hence every numeric rest mass and
    every Yukawa/PDG ratio.

**(d)/(e) GENUINE-BOUNDARY-PROVEN with sharpened I/O.** The border is real and its exact
location is: *the map* `generation ↦ W` (winding count). Core owns the **form** `m_rest = m_0·W`
and the **ontology** (mass is a frequency), but not the **section** `W(·)`. There is no owned
internal functional producing the `W` values; supplying them requires an external catalogue,
which is ⊥M1 at the core level — so importing them is forced to be a passport, by construction.

- **Owned no-go object:** the honest scope line `CLAIM_TO_LEAN_MAP.csv:37` + the ontology
  boundary `04.6.π.6` (`"W is not recovered from any internal derivation"`). The
  count/ontology are Lean/cert-owned (`defect_generation_card`, `m_0·t_0=1`).
- **External datum imported (I/O typing):** **Input** — generation count 3, mass-quantum
  `m_0`, mass=τ⁻¹ ontology (all core). **Output blocked** — per-generation winding `W`, hence
  the numeric mass spectrum and Yukawa ratios (PDG passport). The single exception
  `m_s/m_d=20` is a group cardinality, not part of the blocked hierarchy.

### WORKED VERDICT — GENUINE-BOUNDARY-PROVEN, sharpened to the exact missing object

DERIVED: count=3, mass=τ⁻¹ ontology, quantum `m_0·t_0=1`, branch-weight triple.
IMPORTED: the section `generation ↦ W`. The no-go is *correctly a no-go* — it does **not**
hide a derivable mass ratio; the honest I/O split is count/ontology (in) vs winding/spectrum
(out). This matches the memory prior verbatim (ratios = terminal-passport; count = trivial-
isotype `Tr(T²)=3` owned). No over-claim manufactured.

---

## Cross-cutting finding

Both no-gos are **two faces of one carrier-count wall** (`2 < 3` / integer-spectrum-vs-
φ-cluster). RAYS is the spectral-operator face; GEN-MASS is the mass-weight face. The single
external datum both import is the **third generation label / its winding** — the same object
Lane-L (`BOOK_04:188`) and the hypercharge-flow no-go (`BOOK_04:1383`, `rank 3 < 4`) import.
This is consistent with the D0-selector-M1-forbidden memory: the cement is proven-necessarily-
external.

## Can-fail check

`_TASKS_CENTER_ATTACK/deep_m_genmass_check.py` — 10 base checks PASS; 6 mutation twins all
KILL (break_closure, break_ray_count, break_action, break_cardinality, break_ontology,
claim_ratio_derived). The `claim_ratio_derived` mutant proves the check would catch any
attempt to smuggle in a derived mass ratio.

---

## Independent skeptic (§05.8.R kill-mandate) — VERDICT: NO-KILL

Adversarial pass on both headline verdicts. Could not kill either. **The cardinal sin
(a derived mass-ratio / Yukawa hierarchy) is absent.** Verified against disk, kill-target
by kill-target: (A) no over-claimed ratio; (B) branch-weight triple is backed by real Lean
theorems `pPlus_add_pMinus` (`:14-17`, `exact D0.p_unit_closure`) + `branchGap_eq_two_delta0`
(`:19-22`, `ring`) and correctly typed as *defect* weights not masses; (C) `defect_generation_card`
+ `branchRay_card` own count=3; (D) `{0,20,22,24,33}` integer spectrum + `2<3` wall faithful;
(E) can-fail check discriminates by execution (10/10 base, 6/6 mutants incl. the
`claim_ratio_derived` sentinel), exact Q(φ) not float; (F) `m_s/m_d=20` correctly excluded as
a group cardinality.

**Two required citation repairs — APPLIED IN FULL:**
1. The Lean `decide` no-inject/surject/biject proofs are at
   `D0/Extensions/LeptonBranchFixingNoGo.lean:46,51,55` (with `numBranches_eq_two:32`,
   `numGenerations_eq_three:33`), *not* in the Python cert — the `.py` line is a Python
   `assert`, relabelled accordingly.
2. `defect_generation_card` is `card = 3` by `rfl` (a 3-constructor inductive), distinct from
   the book's `Tr(T²)=3` trivial-isotype reading — the two are no longer conflated into one
   Lean object (RAYS §(d/e) and GEN-MASS DECOMPOSE both fixed).

Minor (no repair): the Lean `no_canonical_operator_among_candidates` is a definitional scaffold
(`isCanonical := False`); the load-bearing content is `vp_canonical_operator_search.py`
(integer-spectrum obstruction) + `LeptonBranchFixingNoGo` (cardinality wall). The memo does not
over-lean on the scaffold — noted for transparency.

---

## Proposed row-notes (PROPOSALS ONLY — no CSV/book edits made)

**D0-GENERATION-RAYS-001** (append to notes):
> DEEP-M verdict: GENUINE-BOUNDARY-PROVEN. Route abandoned in favour of the owned index
> `D0-GEN-INDEX-001` (`P¹(F₂)` = 3, `branchRay_card`). Two independent obstructions:
> (i) `vp_canonical_operator_search.py` — the bare `K(9,11,13)` Laplacian spectrum is exactly
> `{0¹,20¹²,22¹⁰,24⁸,33²}`, five distinct *integers*, which can never host an irrational
> φ-scaling generation cluster, and no candidate operator is forced (each needs an auxiliary
> sign/gauge/orientation/embedding); (ii) the `2<3` carrier-count wall (Lean `decide`,
> `LeptonBranchFixingNoGo.lean:46,51,55`). I/O: input = scene + 2-orbit shell-torus (owned);
> blocked output = a canonical φ-cluster generation operator (external HYP,
> `D0-X5-LEPTON-CONTRACT-001`). The `no_canonical_operator_among_candidates` Lean is a
> definitional scaffold; the content is carried by the cert + cardinality wall.

**D0-GEN-MASS-001** (append to notes):
> DEEP-M verdict: GENUINE-BOUNDARY-PROVEN, sharpened to the exact missing object = the section
> `generation ↦ W` (per-particle memory winding). DERIVED-CORE: count=3 (`defect_generation_card`);
> the mass=τ⁻¹ *ontology* with certified quantum `m_0·t_0=1` exact in Q(φ) (`04.6.π.5`,
> `vp_mass_chain_alpha.py`); the branch-weight triple `(φ⁻¹,φ⁻²,gap)` with `φ⁻¹+φ⁻²=1`
> (`pPlus_add_pMinus`) and `gap=2δ₀` (`branchGap_eq_two_delta0`) — these are *defect* weights,
> NOT physical mass ratios. IMPORTED (passport): the winding `W`, hence every numeric rest mass
> and Yukawa/PDG ratio ("W is not recovered from any internal derivation", `04.6.π.6`). The
> single owned Cabibbo-sector ratio `m_s/m_d=20 = φ_E(44)` is a *group cardinality*, not part of
> the blocked generation hierarchy. The no-go hides no derivable ratio — the honest split is
> count/ontology (in) vs winding/spectrum (out). Skeptic NO-KILL.
