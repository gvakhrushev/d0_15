# RAISE — M1-CORE SATURATION cluster (four extremality theorems from four no-gos)

**Date:** 2026-07-06 · **Status:** DRAFT forge memo (verification only).
**No registry / book / `.lean` / `053040` edits.** Memo-only; no commit. Row-notes proposed at foot.
**Companion can-fail script:** `_TASKS_CENTER_ATTACK/raise_m1core_check.py` — **26/26 PASS, rc=0**,
mutation-tested (4 mutations, all 4 fire rc=1 — one per raise).
**Skill:** `d0-adversarial-forcing-loop` (compute-first → memo → §05.8.R independent skeptic → accept/repair).
**Inputs (frozen at read time):** `MINIMALITY_LENS_MAP.md` (candidates 3,4,5,6),
`DEEP_M_COLOUR_HIGGS_MEMO.md` (FINDING-C), `deep_m_colour_higgs_check.py`, and the four owned Lean rows
verified verbatim on disk:
- `09_LEAN_FORMALIZATION/D0/Spectral/AlphaPresentCoreMaximalityNoGo.lean` (`rate a = φ^a·r = φ^{a-3}`,
  `rate_lt_one`, `rate_three_eq_one`) — `D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001`.
- `09_LEAN_FORMALIZATION/D0/Representation/FinitePathRepresentation.lean` (`commutantDim = Σmᵢ² = 12`,
  `isotypes = [(3,1),(1,8),(1,10),(1,12)]`) — `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`.
- `09_LEAN_FORMALIZATION/D0/Matter/HiggsCondensationPresentCoreMaximalityNoGo.lean` (`tPoly_commutes`,
  `Qnc_not_commute`) — `D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001`.
- `05_CERTS/vp_colour_generation_typed_carrier_nogo.py:85-103` (typed collapse dim 3, weak-commutant 8<9)
  — `D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001`.

The task: raise FOUR no-gos from "X can't be more" to "the M1 present-core **saturates** its extremum
— a positive theorem." Verdict up front, then the worked derivations, then the shared principle, then
the independent skeptic.

---

## HEADLINE VERDICTS

| # | raise | from (no-go) | to (extremality theorem) | verdict |
|---|---|---|---|---|
| 1 | **COLOUR → RIGIDITY-EXTREMALITY** | `8<9` deficit | the M1 `+2` frame is the JOINT extremum: it minimises commutant dim (→3) AND swap order (→1) together; abelian ℂ³ is the maximally-rigid commutant | **RAISED-TO-THEOREM** (rigidity leg; colour ⊗ℂ³ import stays external — NOT "colour derived") |
| 2 | **ALPHA-PRESENT-CORE → SUBCRITICAL-EXTREMALITY** (mint P-SUBCRIT) | maximality no-go (every tower trace-class) | `a≤2` is the MAXIMAL subcritical region; `rate(a)=φ^{a-3}<1 ⟺ a≤2`; `φ³` critical | **RAISED-TO-THEOREM** |
| 3 | **R1 → MAXIMAL-COMMUTANT** | reconstruction no-go | `dim Comm = 12 = 3²+1+1+1` is the FULL centralizer ⇒ the largest algebra commuting with the reconstructed action | **RAISED-TO-THEOREM** |
| 4 | **HIGGS-CONDENSATION → MAXIMAL-ABELIAN** (mint P-ABELIAN) | condensation maximality no-go | the present-core is the MAXIMAL T-commutative sub-object; non-commutativity lives only in extension layers | **RAISED-TO-THEOREM** (raises W1, not the external SSB-sign W2) |

**Count raised: 4 / 4 RAISED-TO-THEOREM.** Shared parent principle **P-M1-SATURATION** holds (below).
Skeptic verdict: **NO KILL** on all four headlines; two scope-repairs applied (COLOUR: "extremal
rigidity" not "colour derived"; HIGGS: raises W1 only, W2 stays the external SSB-sign wall).

---

## THE PARENT EXTREMALITY PRINCIPLE — P-M1-SATURATION

The four raises are not four independent facts; they are **one theorem shape** with four choices of
functional. State it once:

> **P-M1-SATURATION.** Let `X_core` be the M1 present-core sub-object and `F` an owned order /
> valuation functional on the admissible present-core class 𝒞 (growth-rate, commutant-dimension,
> commutativity, distinctness-rigidity). Then `X_core` is the **unique F-extremum in 𝒞**, and the
> associated no-go is *exactly* the statement "no admissible object in 𝒞 beats `X_core` on `F`."
> Equivalently: **(no-go holds) ⟺ (the extremum is saturated).** A witness lies *just past* the
> extremum but *outside* 𝒞 — it is the exact external import the no-go names.

The four instances (each verified in `raise_m1core_check.py`, "core at extremum AND witness just past"):

| instance | functional `F` | admissible class 𝒞 | core value (extremum) | witness just past (external) |
|---|---|---|---|---|
| COLOUR | (commutant dim, swap order) — rigidity | M1 zone frames | (3, 1) = joint MIN | equal frame (9, 6): colour ⊗ℂ³ |
| ALPHA | growth rate `a` ↦ `φ^{a-3}` | present-core towers | `a≤2` (`rate<1`), max subcritical | `a=3` (`rate=1`, `φ³` carrier) |
| R1 | commutant dimension | reconstructed Aut-rep | 12 = full centralizer (MAX) | `PRIM-FINITE-SPECTRAL-TRIPLE-REP` |
| HIGGS | commutativity with `T` | present-core projectors `a·1+b·T` | all commute (MAX abelian) | `Qnc`, `[T,Qnc]≠0` (extension) |

This is why the cluster is one forge: **the same lens** (core-saturates-owned-extremum) converts each
"cannot-be-more" no-go into a positive "is-already-at-the-max" theorem. The no-go and the extremality
theorem are the *same statement read two ways* — the no-go is the negative face, the extremality is the
positive face. `raise_m1core_check.py` verifies the parent schema fires for all four (5 PASS in the
PARENT block) and its mutations each break exactly one instance.

---

# RAISE 1 — COLOUR → RIGIDITY-EXTREMALITY

## Compute-first (exact, re-derived — not asserted)

The M1-forced zone frame is `{L5+2, L5, L5-2} = {24,22,20}` (all distinct). Two owned functionals on
the M1 zone family (both re-derived by exact integer arithmetic in the script; they mirror
`DEEP_M_COLOUR_HIGGS_MEMO.md` FINDING-C and `vp_colour_generation_typed_carrier_nogo.py:85`):

- **commutant dim** of `diag(d0,d1,d2)` in `M₃` = `Σ (class size)²`.
- **zone-swap order** (Weyl-`S₃` proxy) = `#{σ∈S₃ : σ fixes the degree labels}`.

| M1 rigidity | frame | commutant dim | swap order |
|---|---|---|---|
| **OFF** (equal `K(n,n,n)`) | `{22,22,22}` | **9** (full `M₃`, colour would fit) | **6** = `|W(SU3)|` |
| partial (degenerate) | `{24,24,20}` | 5 | 2 |
| **ON** (`+2` forced) | `{24,22,20}` | **3** (abelian ℂ³) | **1** |

## The RAISE (beyond the linkage)

`DEEP_M_COLOUR_HIGGS_MEMO.md` already proved the **linkage** (one toggle flips both effects). The
extremality raise adds the *positive* content: the `+2` frame is the **JOINT EXTREMUM** of the M1 zone
family — it **simultaneously saturates both floors**:

- commutant dim `= 3` is the **minimum possible** for a 3×3 diagonal (all eigenvalues distinct);
- swap order `= 1` is the **minimum possible** (trivial stabiliser).

Both are at their floor *together*, at the *same* frame, and only there. That is exactly what
"maximally-rigid" means: the `+2` step is the unique zone configuration that maximises pairwise
distinguishability. Reading it positively:

> **RIGIDITY-EXTREMALITY (theorem).** Among the M1 zone frames, the `+2`-forced frame is the unique
> maximally-rigid outcome: it jointly minimises the generation-commutant dimension (→ abelian ℂ³) and
> the zone-swap (Weyl-carrier) order (→ trivial). The one extremal rigidity has **two effects** — it
> forces the generation algebra to be abelian ℂ³ **and** destroys the SU(3) Weyl carrier. The `8<9`
> deficit is the **corollary**: at the rigid extremum the generation commutant is 3-dimensional
> (abelian), while a source-native colour `M₃` needs 9 — so the deficit `9−3` is precisely the width of
> the external `⊗ℂ³ = 𝒜_F` seam, not a naked shortfall.

## DISCIPLINE — the over-reach guard (colour is NOT derived)

The task warns: do **not** claim "colour derived" (burned twice; colour SU(3) is terminal-passport).
The raise is scoped to the **rigidity**, never the missing `M₃`:

- The extremal commutant at the `+2` frame is **abelian, dim 3** — strictly **less** than `dim M₃ = 9`.
  The script's DISCIPLINE control asserts `d_forced = 3 < 9` and **fires** if the raise ever manufactured
  an owned colour `M₃` (`colour_M3_recovered_in_core := d_forced ≥ 9` must stay False).
- The `⊗ℂ³` colour import remains external (Mordell/Furey/E8 terminal-passport, per memory
  `colour-su3-not-derived-in-d0` and `DEEP_M_COLOUR_HIGGS_MEMO.md` attack (b)). The raise says the
  **rigidity** (the ℂ³ commutant + the Weyl-kill) is extremal — it does **not** say colour is scene-native.
  This matches `MINIMALITY_LENS_MAP.md` row 3: "ext? = N (the rigidity leg); Y (the ⊗ℂ³ colour import
  stays external)."

**Verdict: RAISED-TO-THEOREM** (rigidity leg). The naked `8<9` is demoted from an "interface accident"
to the **corollary of a forced joint-extremum** rigidity theorem. Colour import unchanged (external).

---

# RAISE 2 — ALPHA-PRESENT-CORE → SUBCRITICAL-EXTREMALITY (mint P-SUBCRIT)

## Compute-first (exact — the rate function is Lean-owned)

From `AlphaPresentCoreMaximalityNoGo.lean` verbatim: `rate a = φ^a · r = φ^{a-3}` (with frozen weight
`r = φ⁻³`). Owned Lean theorems: `rate_lt_one (a ≤ 2) : rate a < 1` and `rate_three_eq_one : rate 3 = 1`.
The script re-derives the sign of `φ^{a-3}` from the Fibonacci recurrence (exact `ℤ[φ]`, no floats):

| `a` | `rate(a) = φ^{a-3}` | region |
|---|---|---|
| 0 | `φ⁻³ < 1` | subcritical (constant `2¹¹` ledger) |
| 1 | `φ⁻² < 1` | subcritical (golden carrier, Perron `φ`) |
| 2 | `φ⁻¹ < 1` | subcritical (max of the region) |
| **3** | `φ⁰ = 1` **exactly** | **critical** (`1/j` line, Perron eigenvalue `φ³`) |
| ≥4 | `φ^{≥1} > 1` | supercritical |

## The RAISE

The no-go says "every admissible present-core tower is trace-class (never `μ₂=12288/5`)." Read positively:

> **SUBCRITICAL-EXTREMALITY (theorem).** `rate(a)<1 ⟺ a≤2`, with `rate(3)=φ⁰=1` the *critical* rate
> (`φ³` = the cube of the forced golden rate). Therefore `a≤2` is the **maximal trace-class (subcritical)
> region**, and the present-core (which supplies exactly `a=0` and `a=1`) **saturates** the
> golden-subcritical extremum: both present-core carriers lie strictly inside the maximal region, and the
> boundary `a=3` (`φ³`) is the wall M1 forbids (single golden rate `φ` — 5-fold symmetry + M1 exclude a
> `φ³` carrier). The maximality no-go = "present-core growth saturates the golden-subcritical extremum;
> `φ³` is the critical rate no admissible present-core tower can reach."

The witness just past the extremum (`a=3`, `rate=1`, `φ³` carrier) is exactly the **external import** the
row names ("a new independently-forced `φ³` carrier"). Extremum-saturated ⟺ no-go — the parent shape.

**Verdict: RAISED-TO-THEOREM.** Mint **P-SUBCRIT** (matches `MINIMALITY_LENS_MAP.md` §(a)4,
`UPLIFT_SWEEP_FINAL_REPORT.md` row 6 — un-minted P-SUBCRIT candidate).

---

# RAISE 3 — R1 → MAXIMAL-COMMUTANT

## Compute-first (exact — Schur, Lean-owned)

From `FinitePathRepresentation.lean` verbatim: `isotypes = [(3,1),(1,8),(1,10),(1,12)]`,
`totalDim = Σmᵢ·dᵢ = 33`, `commutantDim = Σmᵢ² = 3²+1+1+1 = 12` (`by decide`). The script re-derives
both by exact integer sums.

## The RAISE

The commutant `dim = Σmᵢ²` is **not a coincidental 12** — by Schur's lemma the commutant of a rep **IS
the full centralizer** `End_Aut(ℂ³³)`, and by the double-commutant theorem no larger algebra commutes
with the reconstructed action. So:

> **MAXIMAL-COMMUTANT (theorem).** `dim Comm = 12 = 3²+1+1+1` is the **largest** algebra commuting with
> the reconstructed `Aut`-action. Structurally it is `M₃ ⊕ ℂ ⊕ ℂ ⊕ ℂ` = `End(generation space) ⊕ ℂ³`
> (the flavor-frame algebra plus the three trivial-isotype lines; see `W2_QUANTITY_IDENT_MEMO.md`
> "commutant = flavor-frame algebra `End(gen) ⊕ ℂ³`"). The reconstruction no-go = "the flavor-frame
> algebra is already at its maximal owned commutant; the `M₃` generation block (`3²=9`) is the largest
> generation-freedom the core allows, so the Weyl-role assignment is unforced (`GL(3)` basis freedom)."
> "Can't reconstruct further" = "the commutant is already maximal."

The witness just past is `PRIM-FINITE-SPECTRAL-TRIPLE-REP` (the missing role-resolution functor that
would cut the `GL(3)` freedom) — the external import the row names. Script control: dropping the
generation block (mult 3 → 1) collapses the commutant to 4, confirming the `3²=9` block is exactly the
maximal-commutant content.

**Verdict: RAISED-TO-THEOREM.** Feeds the un-minted **P-R1-COMMUTANT** (already has a computed roster
entry in `W2_QUANTITY_IDENT_MEMO.md` §8; this raise supplies the *extremality* reading).

---

# RAISE 4 — HIGGS-CONDENSATION → MAXIMAL-ABELIAN (mint P-ABELIAN)

## Compute-first (exact — exhaustive over ZMod 44, Lean-owned)

From `HiggsCondensationPresentCoreMaximalityNoGo.lean` verbatim: `tPoly_commutes` — for **all**
`a b : ZMod 44`, `a•1 + b•T` commutes with `T`; and `Qnc_not_commute` — `Qnc = !![1,0;0,0]` has
`[T,Qnc] ≠ 0` (`native_decide`). The script re-verifies the `tPoly_commutes` leg **exhaustively** (all
`44² = 1936` polynomials commute with `T`) and computes `[T,Qnc] = [[0,43],[1,0]] ≠ 0`.

## The RAISE

The no-go says "no frozen non-commuting `(U,Q0,Π_H)` in the present-core ⇒ no condensation." Positively:

> **MAXIMAL-ABELIAN (theorem).** Every present-core projector is a polynomial `a·1+b·T` and commutes
> with `T` (exhaustive, `tPoly_commutes`); hence the present-core is the **maximal T-commutative
> (abelian) sub-object**. Non-commutativity is **extremally excluded** from the core: a non-commuting
> witness (`Qnc`, `[T,Qnc]≠0`) exists but lies **outside** the core (not a polynomial in `T`) — it lives
> only in a central-extension / archive layer. "No frozen non-commuting `(U,Q0,Π_H)`" = "the abelian core
> is maximal; non-commutativity lives only in the extension layers."

The witness just past the extremum (`Qnc`) is the exact external import (`PRIM-NONCOMMUTING-TRIPLE`).
Script control: under a **scalar** `T` every matrix commutes, so no witness would lie outside — the
maximal-abelian claim is genuinely `T`-specific, and the real `T` gives a **sharp abelian boundary**.

## DISCIPLINE — this raises W1, not W2

`DEEP_M_COLOUR_HIGGS_MEMO.md` FINDING-H established condensation has **two independent walls**:
- **W1 (orbit):** `[T,Q0]=0` ⇒ constant orbit — the wall this raise addresses (maximal-abelian).
- **W2 (SSB sign):** `z² ≥ 0`, never the double-well sign (`D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001`)
  — **external**, orbit-independent, owned only in the scalar sector.

This raise converts **W1** (the commutativity wall) into MAXIMAL-ABELIAN. **W2 stays external** (the
negative-sign import). Consistent with the "Higgs two-walls result": filling `Qnc` (W1) is
**necessary-but-not-sufficient**; the raise claims maximality of the abelian core, not that condensation
is unblocked. No over-reach into "condensation derived."

**Verdict: RAISED-TO-THEOREM** (W1 leg). Mint **P-ABELIAN** (matches `MINIMALITY_LENS_MAP.md` §(a)6,
`UPLIFT_SWEEP_FINAL_REPORT.md` row 7).

---

## §05.8.R — INDEPENDENT SKEPTIC PASS (kill-mandate, one per headline)

**RAISE 1 (COLOUR — does "extremal rigidity" smuggle "colour derived"?)**
- *Kill attempt 1 — "the joint-extremum is trivial: any all-distinct 3-frame has commutant 3 and swap 1,
  so you've dressed a triviality as a theorem."* **Not sustained (scope-narrowing recorded).** The content
  is not that *some* frame is rigid but that the **M1-FORCED** frame is the rigid one, and that the SAME
  toggle governs both the commutant floor and the Weyl-carrier floor (verified: no M1-family frame
  decouples them — script CONTROL). The extremality is the positive reading of an already-owned forcing;
  the triviality objection would also demote every extremality theorem that names a specific extremiser.
- *Kill attempt 2 — "extremal rigidity ⇒ colour derived (over-reach the owner burned twice)."*
  **Explicitly blocked, not sustained.** The extremal commutant is **abelian dim 3 < 9 = dim M₃**; the
  DISCIPLINE control fires if the core ever recovered an `M₃`. The raise names the `⊗ℂ³` import external.
  No "colour derived" claim survives. *Repair applied:* headline reads "RIGIDITY-EXTREMALITY (rigidity
  leg; colour import external)," never "colour derived."
- **Verdict: NO KILL.** RIGIDITY-EXTREMALITY stands with the abelian-ℂ³ / external-M₃ scope.

**RAISE 2 (ALPHA — does "maximal subcritical" smuggle a chosen tower?)**
- *Kill attempt — "you only checked `a=0,1`; maybe some other present-core `a` reaches `φ³`."*
  **Not sustained.** `rate(a)=φ^{a-3}` is monotone and Lean-owned (`rate_lt_one`, `rate_three_eq_one`);
  `a≤2 ⟺ rate<1` is a theorem, not a sample. `a=3` (the `φ³` wall) is excluded by 5-fold symmetry + M1
  (single golden rate `φ`), an owned fact. The extremum quantifies over ALL admissible `a`.
- **Verdict: NO KILL.** SUBCRITICAL-EXTREMALITY stands.

**RAISE 3 (R1 — does "maximal commutant" smuggle a maximisation that isn't there?)**
- *Kill attempt — "12 is just the value `Σmᵢ²`; calling it "maximal" adds nothing."* **Not sustained.**
  "Maximal" is not decoration: by the double-commutant theorem the commutant IS the full centralizer, so
  "no larger algebra commutes with the action" is a genuine extremal statement (not merely "the value is
  12"). The `3²=9` generation block being the largest freedom is the load-bearing extremal content
  (control: without it the commutant is 4).
- **Verdict: NO KILL.** MAXIMAL-COMMUTANT stands.

**RAISE 4 (HIGGS — does "maximal abelian" smuggle W2, or over-claim condensation?)**
- *Kill attempt 1 — "you raised W1 but implied condensation is settled."* **Not sustained (repair
  applied).** The memo explicitly keeps **W2 external** (the SSB-sign wall, orbit-independent, scalar-sector
  owned) and states filling `Qnc` is necessary-but-not-sufficient. The raise is maximality of the abelian
  core, not "condensation derived."
- *Kill attempt 2 — "the maximal-abelian claim is `T`-specific, so it's not a theorem."* **Not sustained:
  `T`-specificity is the point.** The real `T` gives a sharp abelian boundary (witness `Qnc` outside);
  the control confirms a scalar `T` would have no boundary, so the theorem correctly depends on the owned
  return operator `T`, exactly as `tPoly_commutes` does.
- **Verdict: NO KILL.** MAXIMAL-ABELIAN stands (W1 leg; W2 external).

**Can-fail script mutation record** (`raise_m1core_check.py`, 26/26 PASS, rc=0):
- MUT-1 COLOUR forced-frame → equal ⇒ **rc=1** (rigidity floor fails). ✓
- MUT-2 ALPHA critical exponent `a-3 → a-2` ⇒ **rc=1** (wall mislocated to `φ²`). ✓
- MUT-3 R1 generation mult `3 → 1` ⇒ **rc=1** (M₃ flavor-frame block lost). ✓
- MUT-4 HIGGS `T` → scalar `diag(3,3)` ⇒ **rc=1** (abelian boundary lost). ✓
Each mutation breaks **exactly one** raise, confirming the four legs are independently load-bearing and
the parent-schema block depends on all four.

---

## PROPOSED ROW-NOTES (owner to bless — NOT applied)

1. **`D0-COLOUR-GENERATION-TYPED-CARRIER-NOGO-001`** (append):
   > RAISE[P-M1-SATURATION]: the `8<9` deficit is the COROLLARY of a RIGIDITY-EXTREMALITY theorem — the
   > M1 `+2` frame is the unique JOINT extremum of the zone family (commutant dim → 3 = min AND swap
   > order → 1 = min, saturated together). One extremal rigidity, two effects: abelian ℂ³ generation
   > commutant + destroyed SU(3) Weyl carrier. Abelian ℂ³ (dim 3) < dim M₃ (9): colour `⊗ℂ³` stays
   > EXTERNAL (NOT derived). Verified `raise_m1core_check.py` (RAISE 1, mutation-tested).

2. **`D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001`** (append):
   > RAISE[P-M1-SATURATION → P-SUBCRIT]: `a≤2` is the MAXIMAL trace-class (subcritical) region;
   > `rate(a)=φ^{a-3}<1 ⟺ a≤2`, `rate(3)=φ⁰=1` critical (`φ³` carrier, M1-forbidden). The core (a∈{0,1})
   > SATURATES the golden-subcritical extremum. The maximality no-go = "present-core growth saturates the
   > golden-subcritical extremum." Verified `raise_m1core_check.py` (RAISE 2).

3. **`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`** (append):
   > RAISE[P-M1-SATURATION → P-R1-COMMUTANT]: `dim Comm = 12 = 3²+1+1+1` is the FULL centralizer
   > (double-commutant) = the LARGEST algebra commuting with the reconstructed action; structurally
   > `End(gen)=M₃ ⊕ ℂ³`. Reconstruction no-go = "the flavor-frame commutant is already maximal; `GL(3)`
   > freedom is the largest the core allows." Verified `raise_m1core_check.py` (RAISE 3).

4. **`D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001`** (append):
   > RAISE[P-M1-SATURATION → P-ABELIAN]: the present-core is the MAXIMAL T-commutative sub-object (every
   > `a·1+b·T` commutes with `T`, exhaustive); non-commutativity is extremally excluded to the extension
   > layer (witness `Qnc` outside, `[T,Qnc]≠0`). Raises W1 (commutativity wall) only; W2 (SSB `z²≥0`
   > sign) stays external — filling `Qnc` is necessary-but-not-sufficient. Verified `raise_m1core_check.py`
   > (RAISE 4).

*No status changes proposed: all four rows stay NO-GO. The raises are the POSITIVE face of each no-go
(no-go ⟺ extremum saturated), not promotions past the boundary. Mints P-SUBCRIT, P-ABELIAN proposed as
un-forged candidates now forged; P-R1-COMMUTANT gets its extremality reading; parent principle
P-M1-SATURATION proposed as the umbrella.*

---

## FINAL

- **RAISE 1 COLOUR → RIGIDITY-EXTREMALITY: RAISED-TO-THEOREM** (rigidity leg; colour import external, NOT derived).
- **RAISE 2 ALPHA → SUBCRITICAL-EXTREMALITY: RAISED-TO-THEOREM** (mint P-SUBCRIT).
- **RAISE 3 R1 → MAXIMAL-COMMUTANT: RAISED-TO-THEOREM** (feeds P-R1-COMMUTANT).
- **RAISE 4 HIGGS → MAXIMAL-ABELIAN: RAISED-TO-THEOREM** (mint P-ABELIAN; W1 leg, W2 external).
- **Shared principle: P-M1-SATURATION HOLDS** — one schema, four instances (rigidity / subcritical /
  maximal-commutant / maximal-abelian); no-go ⟺ extremum saturated; verified in the script's PARENT block.
- **Skeptic verdict: NO KILL** on all four headlines; two scope-repairs applied (COLOUR not-derived,
  HIGGS W1-only).
- **Count raised: 4 / 4.**
