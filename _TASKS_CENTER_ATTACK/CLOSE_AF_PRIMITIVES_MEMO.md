# CLOSE_AF_PRIMITIVES_MEMO — closing forge for the AF-tower residual primitives (DRAFT v1)

**Author:** closing-forge pass. **Status:** DRAFT; **no registry row edited, no book edited, no
`.lean` added, `053040` untouched, no commit.** Deliverables: this memo +
`close_af_primitives_check.py` (main 19/19 PASS rc=0; `--selftest` die-path battery 6/6, rc=0;
mutation-tested — frozen-literal and wrong-conclusion mutants all trip). Every load-bearing number is
recomputed from the adjacency of `K(9,11,13)`; nothing is read off a cert literal. All ownership
citations verified verbatim on disk (file:line below), read past ±10.

**Mandate.** CLOSE the AF-tower's remaining open objects by CONSTRUCTING them from owned material,
attacking all four routes. The residues (from `CLOSE_AFTOWER_MEMO` + `DEEP_V_VNEXT`/`_VNEXT2`):
(R1) `PRIM-COMPARISON-MAP-XI-N` — the Ξ_N intertwiner (measure leg owned = PF eigenvector; comparison
map Φ exists but not CE-typeable); (R2) `PRIM-DIRAC-SCALE-SELECTION` — row 445 OPEN, family-dependent;
(R3) the class-D carrier-size ansatz (Σd²=15708 vs Σd(d−1)=14990); (R4) break each — find the smuggle.

---

## 0. Owned material, verified verbatim on disk

| owned fact | location (verified) | verbatim / recomputed |
|---|---|---|
| measure leg = PF eigenvector | `BOOK_02:1291` | "The endpoint conditional-expectation owner's **measure** blocker is removable (the Perron–Frobenius eigenvector is the canonical `Aut`-invariant measure) but its **carrier** blocker is genuine" |
| Ξ typing = compression CE onto scene | `BOOK_02:1303` | "the intertwining hierarchy is typed exactly: scene compression (`C_n L J_n = L_scene`) < spectral < heat < Feshbach" |
| carrier gap | recomputed | `W=Σd²=15708`, `NB=Σd(d−1)=14990`, `W−NB=718=2\|E\|`, `\|E\|=359` (prime), `33≠718` |
| Φ intertwiner | `t1_xi_operator_check.py` 11/11 re-run + here | `Φ(B+tJ)=(M+tσ)Φ` ∀t; `ΦΦᵀ=[[D,A],[A,D]]` rank 65<66 singular; `[ΦΦᵀ,M]≠0` |
| Perron scale flow forces φ | `CanonicalRefinementScaleFlow.lean:30-44` | `perron_scale_flow_owner`: `Λ_{N+1}/Λ_N = φ` for every internally-defined refinement scale |
| internal-sourcing ⇒ φ-ladder | `CanonicalMartingaleDiracScale.lean:29,50` | `InternallySourced lam := ∀N, lam(N+1)/lam N = φ`; `internallySourced_forces_phiLadder` |
| rival `2^N` is external | `CanonicalMartingaleDiracScale.lean:39-46` | `scaleTwo_not_internallySourced`: ratio `2 ≠ φ`, "admissible-but-external, imported scale the Perron flow forbids" |
| M1 dichotomy blade | `BOOK_00:475-480` | (A) K changes distinguishable class ⇒ must be derived; (B) K neutral-but-mandatory ⇒ external catalogue ⇒ banned |
| exogenous-parameter DEF | `BOOK_00:455-459` | not-derived ∧ affects-result ∧ not-part-of-distinguishability-protocol |
| row 445 gating | `vp_vnext2_scene_dirac_covariance_selection.py` | load-bearing assert = the **carrier gap** `9·24²+…≠9·24·23+…` (15708≠14990) and `33≠718` |

---

## Route 1 — Ξ_N intertwiner via re-typing

**Construction attempted.** The measure leg is owned (PF eigenvector, `BOOK_02:1291`). The comparison
map Φ = [S;T] exists and is **hierarchy-complete**: `Φ(B+tJ)=(M+tσ)Φ` for all t (verified here at
t∈{−3,0,1,2,5}), so compression < spectral < heat < Feshbach are all met by the *same* explicit integer
operator. The re-typing hope: `PRIM-COMPARISON-MAP-XI-N` does not need a CE — it needs an
identity-family intertwiner, which Φ IS, hence it closes by correct typing.

**Why it does not close (the carrier mismatch, computed).** The primitive's declared target is the
scene-carrier compression `C_n L J_n = L_scene` onto the **dim-33 scene carrier** (`BOOK_02:1303`,
verbatim). But:
- Φ maps into the **66-dim companion double** `ℂ³³_S ⊕ ℂ³³_T` (2N = 66), *not* the 33-dim scene
  carrier. `Φ.shape[0] = 66 ≠ 33` (computed).
- `ΦΦᵀ = [[D,A],[A,D]]` has **rank 65 < 66** → Φ is not a co-isometry, so it defines no CE, and
  `[ΦΦᵀ, M] ≠ 0` (computed) → even its induced compression does not commute with the vertex dynamics.
- Control: `[A,A] = 0` — the obstruction is Φ-specific, a real CE wall, not a check artifact.

So the re-typing does not *construct* the object the primitive names — it **relabels** the primitive
onto a **different carrier** (the companion double), which is **owned nowhere**. The identity-family
intertwiner genuinely exists and is owned; but it is not a comparison map onto the scene carrier.

**Verdict R1: PARTIAL.** The intertwiner EXISTS and is owned (Φ, hierarchy-complete). Closure of
`PRIM-COMPARISON-MAP-XI-N` requires an **owner decision to re-type the primitive's target** from
"CE / compression onto the dim-33 scene carrier" to "identity-family intertwiner into the 66-dim
companion double." That is a genuine change of the wanted object, not a construction of the wanted
object — so this is a re-type PROPOSAL (as `CLOSE_AFTOWER` already filed, REFRAMING-GRADE), not a
closure. **Exact missing lemma:** a CE/co-isometry `Ξ: ℂ⁷¹⁸ → ℂ³³` with `Ξ L_carrier Ξ† = L_scene`
and `Ξ Ξ† = I₃₃` — provably absent for Φ (`ΦΦᵀ` singular), and no owned substitute exists.

---

## Route 2 — Dirac scale via internal-sourcing

**Two distinct legs — this is the decisive disentangling of this pass.** `PRIM-DIRAC-SCALE-SELECTION`
appears in two rows that are gated on **different** underdeterminations:

**Leg (a) — the scale-LAW leg (Outcome C, `AFMartingaleDiracScaleNoGo`).** The original no-go: by the AF
axioms *alone*, both `λ_N=φ^N` and `λ_N=2^N` are admissible (each strictly increasing → compact
resolvent), so the scale is not forced. **Construction:** apply the M1 dichotomy blade to the rival
`2^N`. Its step ratio is `2`, which is **not derived** inside the corpus (the Perron flow forces φ,
`CanonicalRefinementScaleFlow.lean`), **affects the result** (it changes the Dirac spectrum), and is
**not part of any distinguishability protocol** — all three clauses of the exogenous-parameter DEF
(`BOOK_00:455-459`) fire. By the blade branch (A) (`BOOK_00:475-478`), a contentful K must be derived
inside the corpus; ratio-2 is not, so `2^N` is an M1-forbidden external catalog. Hence **internal
sourcing is M1-forced, and `λ_N = λ_0·φ^N` is the unique scale-law** (up to the dimensionless base λ₀,
the standard overall-scale freedom of any spectral triple). **Leg (a) CLOSES.**

**Leg (b) — the covariance-owner leg (row 445, `SCENE-DIRAC-COVARIANCE-OWNER-001`, OPEN PROOF-TARGET).**
This is the smuggle trap, and it is caught. Row 445 says "Scale cocycle is **refinement-family**-
dependent; with the family underdetermined no unique cocycle." Reading the cert on disk
(`vp_vnext2_scene_dirac_covariance_selection.py`): its **load-bearing assert is the carrier gap**
`9·24²+11·22²+13·20² ≠ 9·24·23+11·22·21+13·20·19` (i.e. `15708 ≠ 14990`) and `33 ≠ 718`. So the
"family" that underdetermines the row-445 covariance system C1–C5 is the **W/NB/E history-refinement
family**, *not* the φ^N-vs-2^N scale-law family. Leg (a)'s M1 argument closes the scale LAW; it does
**not** touch the covariance-per-history-family object of row 445, which is gated on the *carrier*
(= `PRIM-SCENE-HISTORY-REFINEMENT-RULE`, the R3 residue).

**Verdict R2: PARTIAL.** The scale-LAW leg CLOSES (M1 forbids the external ratio-2 catalog; internal
sourcing forced; `λ_N=λ_0·φ^N`) — this is the leg `CanonicalDiracCovariance.lean` already Lean-owns
*conditionally on* `InternallySourced`, and Route 2 supplies the missing M1 reason the condition is
forced, not assumed. But row 445 stays OPEN because its covariance owner is gated on the **history
carrier**, a different primitive. **Exact missing lemma for row 445:** a forced selection among the
W/NB/E history carriers (= `PRIM-SCENE-HISTORY-REFINEMENT-RULE`), NOT a scale-law lemma.

> **NB — book↔registry desync confirmed (sibling of `d0-vnext2-corpus-fork-desyncs`).**
> `BOOK_02:1289` reads the Dirac scale as "resolved to `λ_N=λ_0·φ^N`, cocycle `ω=φ` determined"; that
> is TRUE for leg (a) (scale-law), which this memo closes. Registry row 445 reads OPEN; that is TRUE
> for leg (b) (history-family covariance). The two are **not contradictory** once the legs are split —
> they describe different objects. The desync is purely that neither text names *which* leg it means.

---

## Route 3 — carrier-size ansatz via capacity

**Construction attempted.** `W−NB = 718 = 2|E| = CAP` (recomputed). The hope: CAP (owned) SELECTS the
carrier — one of `W`, `NB` is the owned Hashimoto/backtracking count and the other is excluded by an
owned rule keyed to CAP.

**Why it fails (the smuggle, caught by computation).** `W = Σd²` is the all-walks depth-2 count and
`NB = Σd(d−1)` is the non-backtracking count; **both are owned adjacency invariants** (Hashimoto: NB is
the non-backtracking carrier, W the full one). CAP `= 2|E| = 718` is exactly their **difference**
(`W − NB`, one backtrack per directed edge) — computed. A difference does **not** select a side:
`CAP ≠ W` and `CAP ≠ NB` (718 ∉ {15708, 14990}). Capacity **measures the backtrack gap**; it provides
no owned rule that keeps one carrier and excludes the other. Both carriers are Aut-invariant and
survive.

**Verdict R3: FAILED as closure (route broken).** "The capacity selects the carrier" is the smuggled
external choice — false. CAP is the gap, not a selector. The class-D carrier-size ansatz stays an
**un-owned selection** (falsifiable structural content, not gauge, not owned-torsor point — as
`CLOSE_AFTOWER` §T3 established). **Exact missing lemma:** an owned rule that maps CAP (or any owned
invariant) to a *single* carrier value ∈ {15708, 14990}; none exists — the two are related only by
subtraction of CAP, which is symmetric in the sense that it privileges neither.

---

## Route 4 — break each (the smuggle points)

| route | smuggled datum | status |
|---|---|---|
| R1 | "the primitive needs only an identity-family intertwiner (Φ suffices)" | **Φ exists but on the wrong carrier** (66-dim companion double, not the dim-33 scene CE). Re-typing relabels the target; it does not construct the declared object. Caught. |
| R2 | "M1 forces internal sourcing ⇒ row 445 closes" | **Half-true.** M1 forces internal sourcing for the scale-LAW leg (closes). But row 445 is gated on the **history carrier**, not the scale law (cert assert = 15708≠14990). Over-claiming "row 445 closes" would smuggle the carrier selection. Caught. |
| R3 | "capacity selects the carrier" | **False.** CAP = 718 = W−NB is the *gap*, not a selector; `CAP ∉ {W,NB}`. Caught. |

---

## §SKEPTIC — independent adversarial pass (§05.8.R), verdict ACCEPTED

An independent skeptic reproduced the computation (`close_af_primitives_check.py` main 19/19,
`--selftest` 6/6 die-path; `t1_xi_operator_check.py` 11/11; carrier numbers recomputed), verified every
quote verbatim (`BOOK_02:1291` measure/carrier; `BOOK_02:1303` the `C_n L J_n = L_scene` CE typing;
`BOOK_00:455-480` the exogenous DEF + dichotomy blade; `CanonicalRefinementScaleFlow.lean` /
`CanonicalMartingaleDiracScale.lean` the φ-forcing and the `2^N`-external statement; row-445 cert), and
hunted the two flagged smuggle points.

**Verdict: NO-KILL on the three verdicts (R1 PARTIAL, R2 PARTIAL, R3 FAILED-as-closure).** Findings:
- **On "M1 forces internal sourcing" (R2):** SOUND but SCOPED. The blade genuinely forbids the ratio-2
  catalog (contentful-yet-underivable ⇒ branch (A) ⇒ must be derived ⇒ it is not ⇒ banned). The skeptic
  confirmed the memo does **not** let this reach row 445 — row 445's cert is the carrier gap, a
  different object. No over-claim. The one repair demanded and applied: state explicitly that leg (a)
  is exactly the condition `CanonicalDiracCovariance.lean` already assumes (`InternallySourced`), so
  Route 2's genuine NEW content is the **M1 reason** that condition is forced (not the cocycle
  algebra, which was owned). Reworded above.
- **On "capacity selects the carrier" (R3):** the skeptic confirmed CAP = W−NB is a difference and
  `CAP ∉ {W,NB}`, so the selection claim is false; the route is correctly reported BROKEN, not partial.
- **On R1:** the skeptic confirmed the primitive's typed target is the dim-33 scene CE (`BOOK_02:1303`),
  that Φ's image is the 66-dim companion double, and that `ΦΦᵀ` is singular — so re-typing changes the
  object. Correctly PARTIAL (re-type proposal), not closure.

No wound changed a verdict. No headline demoted or promoted.

---

## §NET — scoreboard for the AF residues

**Of the ~3 named AF residues: 0 fully CLOSE; 1 leg closes cleanly inside a PARTIAL; the other legs are
proven-necessarily-external.**

1. **`PRIM-COMPARISON-MAP-XI-N` (R1): PARTIAL — re-type proposal, not closure.** Intertwiner Φ exists
   and is owned (hierarchy-complete), but on the 66-dim companion double, not the primitive's dim-33
   scene CE (`ΦΦᵀ` singular). Closes only under an owner re-type of the primitive's target.
2. **`PRIM-DIRAC-SCALE-SELECTION` (R2): PARTIAL — scale-LAW leg CLOSES; covariance-owner leg stays
   open.** The M1 blade forces internal sourcing ⇒ `λ_N=λ_0·φ^N` (leg a, closed). Row 445 stays OPEN
   because it is gated on the history carrier (leg b), the R3 residue. Book↔registry desync clarified,
   not a contradiction.
3. **class-D carrier-size ansatz (R3): FAILED as closure — route broken.** Capacity measures the
   backtrack gap `CAP=718=W−NB`; it does not select a carrier. The selection stays un-owned (class-D).
   This is the **hard residue**: it is the common gate under both R1 (Ξ needs a carrier) and R2 leg (b)
   (row-445 covariance needs a carrier).

**Structural reading.** The three AF residues collapse to **one** genuinely-external object — the
**history-carrier selection** (`PRIM-SCENE-HISTORY-REFINEMENT-RULE` at the carrier level) — plus **one**
owner re-type decision (R1). The Dirac scale-LAW is no longer a separate external primitive: M1 forces
it. So the AF frontier reduces to: **(i)** the un-selected history carrier (Σd² vs Σd(d−1)) — proven
un-owned, capacity does not break it; **(ii)** an owner decision on Ξ's target carrier. Consistent with
the `d0-selector-m1-forbidden` finding (the within-zone selector all frontiers converge on is
M1-forbidden ⇒ honest closure is a FORCED explicit external bridge, not open-unattempted).

## What this memo does NOT show
- No registry row status changed; no primitive discharged by fiat; `053040`, the α-seam, the M2 torsor
  untouched.
- R2's scale-LAW closure does NOT close row 445 (different leg — the carrier). Claiming it would be the
  caught smuggle.
- R1 does NOT construct the scene-carrier CE (proven absent for Φ); it is a re-type proposal.
- R3 is BROKEN as a construction: capacity does not select the carrier.
