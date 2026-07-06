# CLOSE_AFTOWER_MEMO — closing forge for the AF-tower / vNext2 refinement no-go cluster (DRAFT v1)

**Author:** closing-forge pass. **Status:** DRAFT; **no registry row edited, no book edited, no
`.lean` added, `053040` untouched, no commit.** Deliverables: this memo + `close_aftower_check.py`
(22/22 PASS, rc=0; `--selftest` die-path battery 4/4; mutation-tested 4/4 conclusion mutations fail).
All ownership claims verified verbatim on disk (file:line below), read past ±10.

**Mandate:** genuinely CLOSE as much of the refinement / AF-tower / vNext2 cluster as possible by
CONSTRUCTING the missing object — not cataloguing boundaries. Boundary only as fallback after real
construction attempts. Five closing targets, each attacked as a construction; then the author breaks
his own closures (§SELF-BREAK), then an independent skeptic (§SKEPTIC).

---

## 0. The single owned ledger (verified) and what rides on it

**The weighted-history ledger is OWNED and forced** (BOOK_03 §03.3.0, verified verbatim):

- `BOOK_03:141`: `Z_D(k) := Σ_{γ∈Γ_D(k)} w(γ) [q(γ)]` — the CORE statistical sum over histories.
- `BOOK_03:144`: `Γ_D(k)` = admissible histories at level `k`; `w(γ)` = history weight; `[q(γ)]` =
  memory class in the role algebra `𝒜`.
- `BOOK_03:150,153`: `w(γ) = φ^{−S(γ)}` is **CORE-FORCING** (multiplicativity + unique
  sum-to-product ⇒ exponential; a non-exponential weight would need an exogenous table, ⊥M1).

The three vNext2 families are readings of THIS one ledger (T1 Addendum 2 §2, re-verified here):

```
one weighted history ledger (owned, §03.3):  Z_D = Σ_γ φ^{−S(γ)} [q(γ)]
 ├─ vertex presentation   W :  det(I − uA)                              carrier dim 33
 ├─ edge presentation     E :  det(I − u(B+R)) = det(I − uA)            carrier dim 718 (same nonzero spectrum)
 └─ factored presentation NB:  det(I − uB) = (1−u²)^326 · det(I−uA+u²(D−I))   carrier dim 718
```

**Computed here (`close_aftower_check.py`, all from adjacency, not literals):**
W-carrier `Σd² = 15708`; NB-carrier `Σd(d−1) = 14990`; excess `= 718 = 2|E| = NE`; vertex dim
`33 ≠ 718`. The vacuum cubic `x³ − 359x − 2574` divides `charpoly(A)` exactly (the nonzero spectrum
`{21.837, −9.758, −12.079}` is the shared invariant of all three presentations).

---

## Target 1 — FLAGSHIP: construct PRIM-SCENE-HISTORY-REFINEMENT-RULE by presentation-covariance

### The construction (assembled + machine-verified, not merely sketched)

**Step A — one map covers the whole family (VERIFIED, `t1_xi_operator_check.py` 11/11 + re-run here).**
`Φ = [S;T] : ℂ^718 → ℂ^66` intertwines the ENTIRE Bartholdi family:
`Φ(B + tJ) = (M + tσ)Φ for ALL t` (M = [[A,−I],[D−I,0]], σ = [[0,I],[I,0]]). Verified exactly at
`t ∈ {−3,0,1,2,5}` here; `ΦB^k = M^kΦ` ⇒ heat/Feshbach levels for free (T1_XI_THEOREM). So the three
presentations are not merely spectrally linked (Ihara–Bass/Bartholdi determinants) — they are linked
by **one explicit integer operator, uniform in the fork parameter t**.

**Step B — the presentation label is M1-inadmissible (the X″ forcing, Addendum 2 §3).**
Assume a refinement rule must SELECT one presentation as physical. The selection label
("which presentation") changes no distinguishable outcome: the determinant/spectral/operator
identities of Step A are *proved equalities*. A mandatory-but-outcome-neutral structure is, by the
dichotomy blade (BOOK_00 §00.9), exactly a hidden external catalogue: ⊥M1. Hence **no presentation
selection is admissible**; the M1-forced object is the *presentation-covariant class*, and its
canonical comparison map is Φ (Step A). ∎ (for the presentation-label question)

**What Step B genuinely CLOSES:** the question "which of the three *presentations* {W, E, NB} is the
physical refinement?" is dissolved — it is a contentless label. The refinement RULE, at the level of
*presentation*, IS forced: "take the presentation-covariant invariant content of the owned §03.3
ledger, transported by Φ."

**What is NEW here vs the prior boundary catalog (novelty, honest).** The presentation/measure-vs-
carrier SPLIT and the naming of `PRIM-SCENE-HISTORY-REFINEMENT-RULE` were *already* in DEEP_V_VNEXT2
§0/§1.1 before this memo — the downgrade is NOT the new content. The genuinely new content of this
target is **Step A: the OPERATOR-LEVEL intertwiner Φ**. Prior passes had only the *determinant/
spectral*-level covariance (Ihara–Bass/Bartholdi identities, which BOOK_02:1291 explicitly caps at
"spectra, not the operator"). Φ upgrades that to `Φ(B+tJ)=(M+tσ)Φ` for ALL t — a single explicit
integer operator, fork-uniform, hierarchy-complete (compression<spectral<heat<Feshbach) — which is
strictly stronger than the spectral link the corpus conceded, and is what lets the presentation-label
M1-blade actually bite at the operator level rather than only the determinant level.

### Where it stops — the carrier residue (SELF-BREAK, honest)

Step B does NOT dissolve everything the no-go named. The deep pass (DEEP_V_VNEXT2 §1.1) had already
sharpened 438 to the **carrier** level: state-space size `15708` (W) vs `14990` (NB). My check
confirms the exact gap covariance leaves:

- Φ intertwines the *operators/spectra*, but the **carrier COUNT is presentation-DEPENDENT**:
  `15708 ≠ 14990` is not equated by any covariance identity (they are different-dimensional state
  spaces, `Σd²` vs `Σd(d−1)`).
- Both counts are **Aut-invariant** (family-canonical) yet **distinct** — computed. So the covariant
  class does not single out a carrier size; a *tower construction* (which needs an actual state
  space, not just a spectrum) still faces two inequivalent carriers.

**Verdict T1: PARTIAL — the presentation-label leg CLOSES (X″ forcing holds, machine-verified Φ +
M1-blade); the carrier-count leg does NOT.** The refinement rule is forced *as a presentation-
covariant class* but not *as a state-space carrier*. See Target 3 for the re-typing of the residue
(it is NOT a torsor gauge; it carries class-D content). **This reduces the no-go from "no canonical
refinement rule (missing object)" to "canonical presentation-covariant rule OWNED (= Φ + §03.3
invariant), residual carrier-size selection is a class-D ansatz import" — a genuine downgrade, not a
full closure.**

---

## Target 2 — Ξ_N intertwiner: is it the owned measure-induced map, already assembled?

### The construction attempt

**Measure leg — OWNED (verified verbatim).** `BOOK_02:1291`: "the endpoint conditional-expectation
owner's **measure** blocker is removable (the Perron–Frobenius eigenvector is the canonical
`Aut`-invariant measure)". Computed here: the PF eigenvector of A exists, is sign-definite, and is
**constant on each zone** (Aut-invariant) — the canonical measure leg is assembled and owned.

**Comparison-map leg — candidate owner = Φ (Step A above).** Φ is the explicit, fork-uniform
intertwiner between edge and vertex carriers, hierarchy-complete (compression < spectral < heat <
Feshbach all met by the same map). So the natural closure is: Ξ_N = Φ, measure = PF eigenvector,
both owned → SCENE-XI-INTERTWINER + XI-MAXIMALITY close.

### The wall (SELF-BREAK — this is the smuggled premise, caught)

**Φ is an intertwiner but is provably NOT a CE-typed Ξ.** The owned Ξ typing demands a
conditional-expectation (a co-isometric compression onto the scene carrier). Computed here:

- The compression Gram matrix has a closed form: `Φ Φᵀ = [[D,A],[A,D]]` (computed). Its
  `rank = 65 < 66` → `Φ Φᵀ` is **SINGULAR**: Φ is not a co-isometry, so it does not define a
  CE onto the 66-dim vertex carrier (a CE needs `Φ Φᵀ = I` up to the compression projector).
- `[Φ Φᵀ, M] ≠ 0` (computed nonzero) → even the compression Φ does induce does NOT commute with the
  vertex dynamics M. **Integer intertwining and CE-typing are mutually exclusive for this map**
  (CAMPAIGN_FINAL:27–30, confirmed on disk and recomputed).
- Control: `[A,A] = 0` — the obstruction is Φ-specific (a real CE-typing wall), not a universal
  artifact of the check.

So Φ realizes the *comparison* (identity-family / spectral / heat / Feshbach) but Ξ_N as the corpus
TYPES it (a CE / correspondence onto the scene carrier / AF tower) is **not** Φ. Φ intertwines into
the *companion double* — a carrier owned nowhere.

**Verdict T2: PARTIAL — measure leg CLOSED/OWNED (PF eigenvector, assembled here); comparison-map leg
has an explicit owned CANDIDATE (Φ) that is provably NOT CE-typeable.** The honest closure is a
**re-typing proposal** (already on the table, CAMPAIGN_FINAL REFRAMING-GRADE): if the owner re-types
`PRIM-COMPARISON-MAP-XI-N` from "CE onto the scene carrier" to "identity-family operator intertwiner",
then Φ closes it. Until that owner decision, the no-go stands on the CE-typing wall — but its prose
should record that the map EXISTS (Φ), only its TYPE is contested, and the measure leg is not a
blocker. **XI-MAXIMALITY (442) is correctly a boundary at the CE-type level, not the existence level.**

---

## Target 3 — is the history carrier a GAUGE (class C) or a missing object (class D)?

### The test (organizing lemma, TORSOR_GAUGE_SYNTHESIS_MEMO v2.1, four-cell classification)

The organizing lemma's computable test: **class C** = point-choice on an OWNED torsor (Aut acts;
contentless gauge); **class D** = choice of un-owned ansatz structure (injects a family-canonical
invariant; falsifiable content). I apply it to the carrier choice.

**Class-C is REFUTED (computed).** A class-C gauge would require the owned within-zone torsor group
`Aut = S₉×S₁₁×S₁₃` to act (transitively) between the carriers. But:

- Every within-zone Aut element **fixes A** and **preserves the carrier dimension** (33 stays 33,
  718 stays 718) — verified over 5 random Aut elements. A group action preserves the dimension of
  the space it acts on; the owned torsor group can NEVER map a dim-33 object to a dim-718 object.
- Therefore the carrier choice `{W:33, NB/E:718}` is **NOT a point on the owned within-zone torsor**
  — it is a different object. **The naive "carrier = gauge" closure (Target 3 as posed) FAILS.**

**Class-D is CONFIRMED (computed).** The carrier count, if selected, injects a **family-canonical**
state-space size (`15708` or `14990`, each Aut-invariant) that is **NOT determined by the invariant
ring** (the shared spectrum). Family-canonical + un-owned = the exact class-D signature (organizing
lemma D1: "injects a determined-looking invariant conditional on structure the scene does not own").

**Verdict T3: the carrier residue RE-TYPES from "missing object (class ?)" to class-D ansatz import
— NOT a class-C gauge closure.** This is a genuine sharpening but NOT the closure the target hoped
for: class-D imports are *falsifiable content*, not contentless gauge. So the carrier leg does not
close "for free." **However** this is exactly what makes T1's PARTIAL honest: the residual object is
precisely named — *a canonical class-D refinement ansatz selecting the history carrier size* — and
the organizing lemma tells us its cost (a structural hypothesis that can be wrong), not a gauge
(contentless) and not a within-zone torsor point (owned).

---

## Target 4 — MINT the un-registered forcing owners (closure by owned rows)

Both forcings are **Lean-PROVED (`by decide`, no `sorry`) + cert-passing on disk**, yet have **NO
dedicated registry row** (grep: they appear only in-prose inside row 433). Minting them is closure
(owned rows) and supplies the anchor the dimension leg needs.

**(4a) `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001`.** Lean `D0.VNext2.SceneDimEvenFibonacci`
(`SceneDimEvenFibonacci.lean`, theorems `scene_dim_eq`, `even_fib_sum_eq`, `f9_minus_one_eq`,
`scene_dim_even_fibonacci_forcing`, `even_fib_partial_sums`, all `by decide`); cert
`vp_scene_dim_even_fibonacci_forcing.py`. Recomputed here: `{F₂,F₄,F₆,F₈}={1,3,8,21}`, sum `= 33 =
|V| = F₉ − 1`; AF algebra dim `5²+3² = 34 = F₉` (the `+1` kernel mode). **Ready to mint.**

**(4b) `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001`.** Lean `D0.VNext2.SceneLaplacianSpectrumForced`
(no `sorry`); cert `vp_scene_laplacian_spectrum_forced.py`. Recomputed here from `L = D − A`: the
complete-multipartite closed form `{0:1, 20:12, 22:10, 24:8, 33:2}`, trace `= 718 = 2|E|`.
**Ready to mint.**

**Verdict T4: CLOSED (mint-ready).** Two Lean-proved, cert-passing forcings become owned rows. These
are the anchor that makes the **dimension+grading leg** of the whole cluster OWNED (the scene
dimension 33 and its even-`+2`-graded partition are forced), leaving only the *spectral-refinement*
leg (the carrier residue of T1/T3) external. Mint proposals in §MINT below.

---

## Verdict table

The five ξ/refinement rows 437/438/439/441/442 are NOT five independent no-gos: they bind the **same
Lean module** `D0.VNext2.SceneNativeRefinementClassification`, and four of them (437/439/441/442) share
the **identical theorem** `scene_native_refinement_underdetermined` — only 438 carries a distinct
theorem, `walk_families_carriers_differ` (the carrier leg). So the cluster is **ONE moduli object with
two distinct facts**: (i) `scene_native_refinement_underdetermined` (presentation/ξ leg, 4 rows) and
(ii) `walk_families_carriers_differ` (carrier leg, 1 row). The verdicts below act on those two facts,
NOT on five separate objects (attack E, accepted).

| target | object | verdict | fact it touches |
|---|---|---|---|
| T1 flagship | PRIM-SCENE-HISTORY-REFINEMENT-RULE via presentation-covariance | **PARTIAL** — presentation-label leg CLOSES (NEW: operator-level Φ + M1-blade, verified); carrier-count leg re-typed class-D | fact (i) presentation leg + fact (ii) carrier leg |
| T2 | Ξ_N intertwiner = PF measure ⊕ Φ | **PARTIAL** — measure CLOSED; map Φ owned but not CE-typeable (re-type proposal) | fact (i) ξ/measure leg |
| T3 | carrier = gauge? | class-C **REFUTED** (any owned group); carrier is **class-D** ansatz (sharpening, not closure) | fact (ii) carrier leg |
| T4 | even-Fib + Laplacian forcings | **CLOSED (mint-ready)** — Lean-proved, cert-passing, unregistered | dimension leg of 447/448 |

**Honest reduction count:** see §NET below (ONE moduli object, not five no-gos).

---

## §MINT — proposed motions (owner decision; NOT executed)

1. **Two new CORE/CERT rows** (T4): `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (LEAN_PROVED + cert)
   and `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001` (LEAN_PROVED + cert). Both artifacts exist on disk;
   this is a registration-hygiene closure (analogous to the W4 memo's "registry-unregistered
   theorems" finding).
2. **Row-note on 437/438/439** (T1): record that the *presentation-selection* leg is M1-inadmissible
   (presentation-covariant class is forced; Φ is its comparison map, `t1_xi_operator_check.py` 11/11)
   — the no-go's operative content is the **carrier-size** leg, re-typed as a class-D ansatz import
   (not a class-C gauge, not a within-zone torsor point — computed).
3. **Row-note on 441/442** (T2): the map EXISTS (Φ, explicit integer operator, hierarchy-complete);
   the blocker is the **CE-TYPE** (`Φ Φᵀ` singular, `[Φ Φᵀ, M] ≠ 0`), not existence; the **measure**
   leg is OWNED (PF eigenvector) and should not be cited as a blocker. Re-type proposal for
   `PRIM-COMPARISON-MAP-XI-N` (CAMPAIGN_FINAL REFRAMING-GRADE) carried forward.

## §Lean skeletons (proposed; NOT added to the build)

```lean
-- (T1) presentation-covariance: the identity-family intertwiner exists for all t (raw-graph grade)
-- D0.VNext2.PresentationCovariance
theorem phi_intertwines_bartholdi_family (t : ℤ) :
    Φ * (B + t • J) = (M + t • σ) * Φ := by decide   -- integer matrices, finite
-- consequence typing: refinement rule = presentation-covariant class (M1-blade, prose-level)

-- (T2) the CE-typing obstruction (why Φ is an intertwiner but not a CE-typed Ξ)
-- D0.VNext2.PhiNotCotype
theorem phiPhiT_singular : (Φ * Φᵀ).det = 0 := by decide
theorem phiPhiT_not_commuting : Φ * Φᵀ * M ≠ M * (Φ * Φᵀ) := by decide
```

---

## §SELF-BREAK — the author hunts his own smuggled choices

1. **"Presentation-covariance forces a canonical refinement" — does it import the choice?** The X″
   forcing is honest at the *presentation-label* level: the identities are proved equalities, so
   selecting a label is genuinely outcome-neutral ⇒ ⊥M1. But it does NOT reach the *carrier* level
   — and the memo does NOT claim it does. The smuggle would be to let "presentation" silently
   include "carrier size"; §Target 1 SELF-BREAK + Target 3 keep them separate (15708 ≠ 14990 is not
   an equated identity). **No smuggle; verdict is PARTIAL, not CLOSED.**
2. **"Ξ_N = Φ" — smuggled type coercion?** Yes, that WOULD be a smuggle, and Target 2 catches it:
   Φ is not CE-typeable (`Φ Φᵀ` singular, `[Φ Φᵀ,M]≠0`). The memo files T2 as PARTIAL + re-type
   proposal, not closure. **Caught.**
3. **"Carrier = gauge" — the tempting free closure.** Refuted by computation (Aut preserves carrier
   dimension; the carrier is not a within-zone torsor point). The memo does NOT claim the gauge
   closure; it downgrades to class-D. **Refuted, not smuggled.**
4. **T4 minting — is it real closure or bookkeeping?** It is registration of already-proved
   artifacts (Lean `by decide`, cert-passing) — genuine owned-row closure of the *dimension* leg,
   but explicitly NOT the *spectral-refinement* leg. No over-claim: the memo's own §Target 4 states
   "leaving only the spectral-refinement leg external."

## §NET — the honest scoreboard for this cluster

**Do NOT count registrations as independent reductions.** Rows 437/438/439/441/442 are ONE moduli
object (same Lean module; 4 share one theorem, 1 has the carrier theorem). The honest tally:

**(a) Owned rows to MINT — count 2** (T4, genuine closure to owned rows):
- `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (Lean `by decide`, cert PASS) — the scene dimension
  `33 = F₉−1` and its even-`+2`-graded partition, forced.
- `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001` (Lean, cert PASS) — the complete-multipartite spectrum
  `{0:1,20:12,22:10,24:8,33:2}`, forced.
These close the **dimension+grading leg** of the whole refinement cluster (and of 447/448's
capstones): the scene dimension and its grading are no longer external.

**(b) Moduli objects DISSOLVED (or partly) — count 1** (the refinement/ξ cluster, all five rows):
- Its **presentation-label leg** (fact (i)) is dissolved: selecting a presentation is M1-inadmissible
  (NEW operator-level Φ + dichotomy blade). The refinement rule, as a *presentation-covariant class*,
  is OWNED (Φ + §03.3 invariant).
- Its **measure leg** (fact (i), ξ side) is dissolved: the PF eigenvector is the canonical measure
  (owned; should not be cited as a blocker on 441/442).
- Net: the ONE moduli object shrinks from "no canonical refinement rule + no canonical Ξ (missing
  objects)" to "presentation-covariant rule + measure OWNED, residual below."

**(c) Genuine residual PRIMITIVES — count 2 (both precisely named, both sharpened, neither eliminated):**
1. **A class-D carrier-size ansatz** (fact (ii), `walk_families_carriers_differ`): selecting the
   history-carrier state-space size `Σd²=15708` (W) vs `Σd(d−1)=14990` (NB). Re-typed from "missing
   object" to a **class-D un-owned ansatz** — NOT a class-C gauge (refuted for *any* owned group:
   carriers have different dims 33≠718, a bijection preserves dimension). This is falsifiable
   structural content, not contentless gauge.
2. **The CE-typing question** for `PRIM-COMPARISON-MAP-XI-N`: the comparison map EXISTS (Φ) but is
   NOT CE-typeable (`ΦΦᵀ=[[D,A],[A,D]]` singular; `[ΦΦᵀ,M]≠0`). Closes only under an owner re-typing
   of the primitive from "CE onto the scene carrier" to "identity-family operator intertwiner."

**Bottom-line scoreboard: 2 owned rows to mint (T4) + 1 moduli object dissolved (presentation +
measure legs, via the new operator-level Φ) + 2 named residual primitives (class-D carrier-size
ansatz; CE-typing of Ξ_N).** `PRIM-SCENE-HISTORY-REFINEMENT-RULE` does NOT fully discharge, but it is
reduced from "missing rule (whole object)" to "OWNED presentation-covariant class + one residual
class-D carrier ansatz" — materially smaller, with the residue named exactly and its cost typed
(falsifiable ansatz, not gauge, not owned-torsor point).

---

## §SKEPTIC — independent adversarial pass (verdict ACCEPTED, no defense)

An independent skeptic (§05.8.R mandate: kill by named-second-object or precise-named-gap) reproduced
the computation (`close_aftower_check.py` 23/23, `t1_xi_operator_check.py` 11/11), verified every
primary quote verbatim (BOOK_02:1291 measure/carrier split; BOOK_00:475–480 dichotomy blade;
BOOK_03:141–153 `w(γ)=φ^{−S}` CORE-FORCING; CAMPAIGN_FINAL:27–30 CE-typing exclusion), and confirmed:
the M1-blade is non-circular at the presentation-*label* level; the class-D re-typing is sound; the
T4 forcings are genuinely unregistered and mint-ready.

**Verdict: NO-KILL on all four targets** (T1/T2/T3/T4 SURVIVE). Two wounds (bookkeeping, both
repaired here, no defense):
- **W1 (strongest finding) — §NET count.** The draft counted "5 no-gos downgrade"; the five rows are
  ONE moduli object (same module, 4 share one theorem). *Repair:* §NET + verdict table rewritten to
  the honest count — 2 mint-ready rows + 1 moduli object dissolved (presentation+measure) + 2 named
  residual primitives (class-D carrier ansatz; CE-typing).
- **W2 — T1 novelty framing.** The presentation/carrier split + primitive naming pre-dated this memo
  (DEEP_V_VNEXT2 §0/§1.1); the genuinely NEW content is the operator-level Φ (all-t intertwiner),
  strictly stronger than the prior determinant/spectral covariance. *Repair:* Step A novelty reworded.

## What this does NOT show

- No registry row status changed; no PROOF-TARGET closed; no primitive discharged by fiat.
- The X″ forcing closes the presentation-LABEL leg only; the carrier-count leg is re-typed
  (class-D), not eliminated. `PRIM-SCENE-HISTORY-REFINEMENT-RULE` stands as a residual class-D
  ansatz, materially reduced.
- Φ is NOT a CE-typed Ξ (proved); `PRIM-COMPARISON-MAP-XI-N` closes only under an owner re-typing.
- T4 mints the *dimension* leg; the *spectral refinement* leg (carrier) stays external.
