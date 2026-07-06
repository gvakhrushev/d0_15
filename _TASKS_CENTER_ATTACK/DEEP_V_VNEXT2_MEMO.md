# DEEP_V_VNEXT2_MEMO — batch V-b deep synthesis of the vNext2 + refinement no-gos (DRAFT v1)

**Author:** deep-synthesis pass. **Status:** DRAFT; **no registry row edited, no book edited, no
`.lean` added, `053040` untouched, no commit.** Deliverables: this memo + `deep_v_vnext2_check.py`
(can-fail-HARDENED, mutation-tested 5/5, rc=0). Row-notes are PROPOSED only (§ROW-NOTES).

**Scope:** genuine per-no-go synthesis (not a tagging pass) of the seven no-gos:
TRIPARTITE-PATH-TOWER-OWNER-001, SCENE-XI-INTERTWINER-OWNER-001, XI-MAXIMALITY-NOGO-001,
SCENE-NATIVE-MAXIMALITY-OWNER-001, SCENE-NATIVE-CLOSURE-BOUNDARY-001, ARCHIVE-REGULAR-REFINEMENT-NOGO-001,
STURMIAN-REFINEMENT-DISCHARGE-NOGO-001. All at `CLAIM_TO_LEAN_MAP.csv` rows 438/441/442/447/448/511/542.

**Method (d0-adversarial-forcing-loop):** preflight grep of all seven IDs (found + cross-referenced,
never duplicated); compute-first — every load-bearing number re-derived FROM the K(9,11,13) graph object
by `deep_v_vnext2_check.py`, not read off literals; verbatim decisive citations verified on disk;
five+ attack lines per no-go on the (a)LIFT (b)CLOSE (c)DECOMPOSE (d)GENUINE-BOUNDARY ladder;
independent skeptic pass on the headlines (§SKEPTIC).

---

## 0. The single structural fact that governs six of the seven

The registry ITSELF (row 437 UPLIFT[2026-07-06]) states the vNext2 cluster is **one moduli object with
several registrations**: "SAME OBJECT as csv:439 + csv:490 (H3) — single moduli, three registrations."
The moduli is the **refinement-family 3-point moduli {W (all-walks), NB (non-backtracking), E
(directed-edge)}**, and the shared completion class is **PRIM-SCENE-HISTORY-REFINEMENT-RULE** (B-ext
gauge-fixing under the row-550 within-zone organizing lemma). The ξ-cluster adds
**PRIM-COMPARISON-MAP-XI-N**; the Dirac-cluster adds **PRIM-DIRAC-SCALE-SELECTION**.

**The load-bearing computed fact (re-derived from the graph, `deep_v_vnext2_check.py` C1–C5):**

| quantity | value | derivation (from A of K(9,11,13), NOT a literal) |
|---|---|---|
| degrees | (24,22,20)=(33−n_i) | `sum(row)` of adjacency |
| all-walks depth-2 carrier W | **15708** | `Σ_v deg(v)²` |
| non-backtracking carrier NB | **14990** | `Σ_v deg(v)(deg(v)−1)` |
| excess W−NB | **718 = 2\|E\|** | one backtrack per directed edge |
| vertex vs directed-edge dim | **33 ≠ 718** | N vs 2\|E\| |
| Laplacian spectrum | {0:1,20:12,22:10,24:8,33:2}, trace 718 | eigen-count of L=D−A |

These are the numbers on which ALL of rows 438/441/442/447/448 rest. Before this pass they were
**hardcoded integer literals** in both the Python certs and the Lean `def`s (Finding F1 below); this
pass supplies the first graph-derived, mutation-tested computation of them.

**CRITICAL PRE-FLIGHT FINDING (CERT_CANFAIL_SWEEP §2 Finding F1, verified on disk):** the five vNext2
certs `vp_vnext2_tripartite_path_tower_classification.py`, `vp_vnext2_tripartite_scene_xi_intertwiner.py`,
`vp_vnext2_scene_native_maximality.py` (+ `_scene_native_refinement_category.py`, `_scale_cocycles.py`)
are **STUB-SUSPECT**: their asserts are arithmetic on integer literals, `SURVIVED` the mutation probe
(flip line 9 int → still rc=0), and two even print `FAIL_*` lines inside the success branch. The Lean
module `SceneNativeRefinementClassification.lean` is `by decide` over the same literals (`allWalksDepth2
:= 9*24^2+...`). **Mitigation on record:** all rows carry `LEAN_PROVED`, so no claim is *solely* cert-
backed — but the numbers were never computed from the object. `deep_v_vnext2_check.py` closes exactly
this: the self-test shows a literal cert would pass all 5 mutant graphs (content-free), while the
hardened check flips because W/NB are re-derived from perturbed adjacency.

---

## 1. Per-no-go worked verdicts

### 1.1 D0-VNEXT2-TRIPARTITE-PATH-TOWER-OWNER-001 (row 438, NO-GO)
**Decisive statement (registry 438, verbatim):** "The path/history tower is family-dependent (W/NB/E
inequivalent); no unique tower. Missing PRIM-SCENE-HISTORY-REFINEMENT-RULE."
**Owned object:** the three families as M1-admissible carriers (Lean `SceneNativeRefinementClassification`,
docstring lists the M1 conditions each satisfies: Aut(K)-equivariant, part-preserving via intrinsic
degree/role, basepoint-free, computable, deterministic endpoint). **External:** a selector among them.
**Attack ladder:**
- (a) LIFT — the strongest LIFT ON RECORD is `T1_FORCING_MEMO` + ADDENDUM_2: claim NB is the unique
  M1 family (returns are the typed p²-channel, not a free history letter; a return-containing family
  needs an exogenous "which-copy" register θ ⊥M1). **Verdict of that campaign (CAMPAIGN_FINAL:56,
  UPLIFT_SWEEP_FINAL_REPORT):** the LIFT did NOT mint — it resolved into "presentation covariance"
  (candidate X″), filed as a **B-ext reading-layer candidate, un-minted**; PRIM-SCENE-HISTORY-
  REFINEMENT-RULE **stands**. The reason it cannot close: even granting X″, selecting the physical
  *carrier* (state-space size 15708 vs 14990 for tower construction) is Addendum-2 residual #3, NOT
  dissolved by any identity.
- (b) CLOSE (read past citations) — BOOK_02:1291 (verified): "the endpoint operator lives on the
  history carrier, and the admissible families give different carriers (all-walks vertex dim 33 vs
  non-backtracking/directed-edge dim 2|E|=718); **Ihara–Bass links only their *spectra*, not the
  operator.**" This is the corpus's OWN statement that the closure route is spectral-only. Reading
  further does not close it.
- (c) DECOMPOSE — this IS a decomposition already (registry: single moduli, three registrations); the
  no-go is the correct name for "the moduli has ≥2 points."
- (d) GENUINE-BOUNDARY — YES, at the CARRIER level. **Exact external import:** a rule selecting one
  history carrier (= PRIM-SCENE-HISTORY-REFINEMENT-RULE). The T1 campaign SHARPENS this: the boundary
  is not "no relation between families" (they ARE presentations of one owned §03.3 weighted-history
  ledger — see C6) but specifically "no M1-forced choice of *state-space carrier* for the tower."
**VERDICT: GENUINE-BOUNDARY (carrier-selection), decomposition-into-owned-presentations SHARP.**

### 1.2 D0-VNEXT2-SCENE-XI-INTERTWINER-OWNER-001 (row 441, NO-GO)
**Decisive (441, verbatim):** "Xi_n=C_n is family/measure-dependent -> no canonical Xi.
PRIM-COMPARISON-MAP-XI-N remains independent."
**Sharpening this pass adds (BOOK_02:1291, verified verbatim):** the two legs of Ξ's dependence are NOT
symmetric — **"The endpoint conditional-expectation owner's *measure* blocker is removable (the
Perron–Frobenius eigenvector is the canonical Aut-invariant measure) but its *carrier* blocker is
genuine."** So "family/measure-dependent" in row 441 is loose: the **measure** leg is CLOSED (canonical
PF-eigenvector measure); only the **carrier** leg (= same object as 1.1) survives.
**Attack ladder:** (a) LIFT the measure leg → SUCCEEDS and is owned (PF eigenvector). (a′) LIFT the
carrier leg → reduces to 1.1's NB-forcing, un-minted. (b) CLOSE → BOOK_02:1291 caps it at spectral-
level. (d) GENUINE-BOUNDARY → YES but ONLY on the carrier leg; the measure leg should not be cited as
a blocker.
**VERDICT: GENUINE-BOUNDARY (carrier leg only; measure leg CLOSED/owned).** Row-note proposed to record
the measure/carrier split so the no-go is not over-stated as "measure-dependent."

### 1.3 D0-VNEXT2-XI-MAXIMALITY-NOGO-001 (row 442, NO-GO) — THE LOAD-BEARING ONE
**Decisive (442, verbatim):** "Maximality: >=2 admissible families give inequivalent Xi; no canonical
comparison map. Missing PRIM-COMPARISON-MAP-XI-N."
This is the maximality (capstone) form of 1.2: it asserts no Ξ is canonical over the WHOLE admissible
family space, not just for a named pair. **Attack ladder, hardest first:**
- (a) LIFT — would need a family-space-wide selector. The T1 dichotomy (return vs advance) covers only
  **step-generated (Markov-on-edges) families** — T1_FORCING_MEMO §2 open obligation names this
  explicitly: "Non-step-generated (history-dependent) families need either exclusion by the same M1
  blade (memory-of-history = register) or an explicit scope restriction of X." So even the strongest
  LIFT does not reach maximality over the full family space; it reaches it over the step-generated
  class ONLY, and even there stays un-minted.
- (b) CLOSE — the measure leg closes (PF eigenvector, 1.2); the carrier/operator leg does not.
- (c) DECOMPOSE — maximality = "the moduli of 1.1 has >1 point AND no M1 functional selects a point."
- (d) GENUINE-BOUNDARY — YES. **Exact external import: PRIM-COMPARISON-MAP-XI-N**, and it is INDEPENDENT
  of PRIM-SCENE-HISTORY-REFINEMENT-RULE (per TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX). The
  independence is real: even given a forced history rule (1.1), Ξ additionally needs a canonical
  endpoint-conditional-expectation intertwiner at Ξ_N-level (BOOK_02:1291: compression<spectral<heat<
  Feshbach; C6 gives only spectral).
**VERDICT: GENUINE-BOUNDARY (maximality over step-generated class; full family space is a stated scope
gap in the ONLY LIFT attempt). Missing object = PRIM-COMPARISON-MAP-XI-N, INDEPENDENT.**

### 1.4 D0-VNEXT2-SCENE-NATIVE-MAXIMALITY-OWNER-001 (row 447, NO-GO)
**Decisive (447, verbatim):** "Capstone: refinement/Xi/operator/tick/Feshbach/scale all underdetermined
or blocked. PRIM-COMPARISON-MAP-XI-N and PRIM-DIRAC-SCALE-SELECTION remain INDEPENDENT; new upstream
PRIM-SCENE-HISTORY-REFINEMENT-RULE."
This is the conjunction capstone over the whole cluster. It is TRUE iff each leg is genuinely blocked —
which 1.1–1.3 (history, ξ) and the Dirac-cluster (row 445, PRIM-DIRAC-SCALE-SELECTION) establish.
**Attack:** (a) LIFT the conjunction → requires lifting EVERY leg; the ξ measure-leg lifts (owned) but
the carrier and Dirac-scale legs do not; conjunction stays blocked. (d) GENUINE-BOUNDARY → YES, as a
conjunction of 1.1/1.3 + Dirac-scale. **The only sharpening:** the capstone prose "all underdetermined"
slightly over-states — the ξ *measure* sub-leg is owned; the correct capstone is "the history-carrier
leg, the Ξ_N-intertwiner leg, and the Dirac-scale leg are blocked; the endpoint-measure leg is owned."
**VERDICT: GENUINE-BOUNDARY (conjunction). Missing = {PRIM-SCENE-HISTORY-REFINEMENT-RULE,
PRIM-COMPARISON-MAP-XI-N, PRIM-DIRAC-SCALE-SELECTION}, all three INDEPENDENT.**

### 1.5 D0-VNEXT2-SCENE-NATIVE-CLOSURE-BOUNDARY-001 (row 448, NO-GO) — task flags: MAKE THE PROOF SHARP
**Decisive (448, verbatim):** "Closure boundary: the scene-native route does not lift the physical scene
dynamics from present core; all downstream alpha/CMB/Higgs/smooth-geometry gates STAY CLOSED."
This is the **genuine boundary** the memory anchor + task flagged. My job: make its owned proof SHARP,
not force it open. **Sharp proof (assembled from owned facts):**
1. Any physical lift downstream (α, CMB n_s, Higgs vev, smooth geometry) consumes a canonical scene
   operator / Ξ / Dirac scale (the intertwining hierarchy, BOOK_02:1303).
2. Each of those inputs is blocked by 1.1–1.4: the history-carrier is unselected (1.1), Ξ_N is
   non-canonical (1.3), the Dirac scale is family-dependent (row 445). These are THREE INDEPENDENT
   external primitives (independence matrix), so no single owned move discharges the conjunction.
3. Therefore the downstream gates cannot be opened by the scene-native route from present core. ∎
The current cert `vp_vnext2_no_false_physical_promotion.py` proves the DUAL (no book contains an
affirmative overclaim phrase) — it is a **negation-aware prose guard**, genuinely can-fail (it plants
an overclaim and requires the scan to catch it; verified rc=0 with the control firing). This is the
RIGHT kind of cert for a closure-boundary: it enforces that nothing downstream is silently promoted.
**VERDICT: GENUINE-BOUNDARY, proof SHARP** = (physical lift needs canonical operator/Ξ/scale) ∧ (all
three blocked by independent primitives 1.1/1.3/445). Cert is a correct dual guard, KEEP.

### 1.6 D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001 (row 511, NO-GO; Lean-only, empty cert field)
**Decisive (Lean `Refinement.lean:archive_window_not_measure_preserving`, verified):** `archiveWindow =
359/160`, `regularCoverRatio = 1`, `359/160 ≠ 1` (norm_num). A regular double cover is measure-preserving
(ratio 1, constant fibre 2); the frozen archive bonding map carries the contraction window 359/160 ≠ 1,
so it is contracting, NOT a regular cover. **This is a refinement-DISCHARGE no-go: it forbids
substituting a regular mod-N cover for the real archive bonding map.**
**Attack:** (a) LIFT (make the archive map a regular cover) → REFUTED by exact rational 359/160≠1;
`deep_v_vnext2_check.py` C7 re-derives 359 = |E| and the window discriminant 640=64·10 from scene
counts. (d) GENUINE-BOUNDARY / rather a clean IMPOSSIBILITY: the archive map is intrinsically contracting.
**Is the refinement rule here the un-owned PRIM-SCENE-HISTORY-REFINEMENT-RULE?** NO — checked. This
no-go concerns the ARCHIVE bonding map (owned: D0-ARCHIVE-CONTRACTION-NOGO-001), a *different* object
from the K(9,11,13) history refinement of 1.1. The 359/160 window is scene-forced (|E|=359, product-of-
degrees/(2V)=160), not a named-missing rule. **VERDICT: PROVEN NO-GO (exact rational impossibility);
the refinement rule IS owned (archive contraction), NOT the missing history primitive.** Row-note: this
row currently has an EMPTY python_cert field — `deep_v_vnext2_check.py` C7 supplies an optional
graph-derived corroboration of 359 and the window; Lean already suffices.

### 1.7 D0-STURMIAN-REFINEMENT-DISCHARGE-NOGO-001 (row 542, PYTHON_CERTIFIED NO-GO)
**Decisive (cert `vp_sturmian_refinement_discharge_nogo.py`, 6/6 PASS incl. wrong-object control;
re-run rc=0 this pass):** the CONDITIONAL-EXTENSION of D0-STURMIAN-REFINEMENT (parent, stays
PROOF-TARGET) cannot be discharged internally, for TWO independent EXACT reasons:
(i) **FIELD DISJOINTNESS (load-bearing):** golden tower lives in Q(√5)=Q(φ); archive/window scale
359/160 = roots of 160λ²−480λ+359 (disc 640=64·10) lives in Q(√10); √10 ∉ Q(√5) (√10=a+b√5 ⟹ a²+5b²=10
∧ ab=0, no rational solution — re-derived independently `deep_v_vnext2_check.py` C7 `sqrt_in_Qsqrt5`).
No canonical intertwiner ties a Q(√5) carrier to a Q(√10) carrier. Same structural reason the
neighbouring phason-WZ transfer closed NO-GO; explained by WINDOW-SCALE-DISCRIMINANT-FORCED-001 (√10 is
the size-fingerprint of 9,11,13, not a golden near-miss).
(ii) **ORIENTATION:** centre-11 convergence forces T=[[0,1],[1,−1]] (trace −1, orientation-reversed) via
|Tr(T⁵)|=L₅=11; Sturmian uses S=[[1,1],[1,0]] (trace +1); trace is a conjugacy invariant so S≁T; scene
pins T~−S; periodic offset L_n−|Fix(T^n)|=[0,2,0,2,…].
**Attack ladder:** (a) LIFT (identify golden tower with archive) → REFUTED twice, exact, with a
numerology guard (φ^k=359/160 ⟹ k=1.679 non-integer). (b) CLOSE the parent → the HONEST boundary is
stated: an EXTERNAL owner could POSTULATE PRIM-STURMIAN-REFINEMENT-OWNER as a passport; that is a named
external choice, not an internal discharge. (c) DECOMPOSE → the discharge = (field-tie) ∧ (orientation-
tie), both refuted. (d) GENUINE-BOUNDARY → YES, and it is the STRONGEST of the seven: a two-obstruction
field-theoretic impossibility, not merely "no forced choice."
**Is the missing rule PRIM-SCENE-HISTORY-REFINEMENT-RULE?** NO — it is PRIM-STURMIAN-REFINEMENT-OWNER
(distinct; a Q(√5)↔Q(√10) intertwiner postulate), correctly named and distinct from the history rule.
**VERDICT: PROVEN NO-GO (two independent exact obstructions); this is the cleanest boundary in the
batch. Cert is SOLID (real computation + wrong-object control), NOT stub-suspect.**

---

## 2. Verdict table

| # | no-go (row) | class | owned object (decomposition) | external import | cert quality |
|---|---|---|---|---|---|
| 1.1 | TRIPARTITE-PATH-TOWER (438) | GENUINE-BOUNDARY (carrier) | W/NB/E = presentations of one §03.3 weighted-history ledger | PRIM-SCENE-HISTORY-REFINEMENT-RULE | STUB→hardened here |
| 1.2 | SCENE-XI-INTERTWINER (441) | GENUINE-BOUNDARY (carrier leg only) | endpoint-measure leg OWNED (PF eigenvector) | PRIM-COMPARISON-MAP-XI-N | STUB→hardened here |
| 1.3 | XI-MAXIMALITY (442) **load-bearing** | GENUINE-BOUNDARY (step-generated class) | measure leg owned; spectral-level identities owned (C6) | PRIM-COMPARISON-MAP-XI-N (indep.) | STUB→hardened here |
| 1.4 | SCENE-NATIVE-MAXIMALITY (447) | GENUINE-BOUNDARY (conjunction) | ξ-measure leg owned | {history, XI, DIRAC-SCALE} indep. | STUB→hardened here |
| 1.5 | CLOSURE-BOUNDARY (448) | GENUINE-BOUNDARY, proof SHARP | lift needs canonical op/Ξ/scale, all blocked | 3 indep. primitives | SOLID (prose dual guard) |
| 1.6 | ARCHIVE-REGULAR-REFINEMENT (511) | PROVEN NO-GO (rational impossibility) | archive contraction 359/160 OWNED | none (rule owned) | Lean-only (SOLID) |
| 1.7 | STURMIAN-DISCHARGE (542) | PROVEN NO-GO (2 exact obstructions) | golden tower + archive scale each M1-fixed | PRIM-STURMIAN-REFINEMENT-OWNER | SOLID (+wrong-obj control) |

**Headline reading of the WATCH (ξ-pair + tripartite-path-tower):** the scene NATIVELY owns the
*presentations* (all three families are readings of one §03.3 weighted-history ledger, connected by
the Ihara–Bass/Bartholdi identities, C6) AND natively owns the endpoint *measure* (PF eigenvector).
What it does NOT own is (i) a forced choice of history *carrier* (state-space size), and (ii) the
Ξ_N-level intertwiner. So the ξ/tripartite no-gos are **genuine boundaries at the carrier/operator
level, riding on a real owned decomposition at the presentation/measure level** — not pure external
formalism, not fully owned. The XI-MAXIMALITY no-go (1.3) is load-bearing and correctly a boundary; the
only correction is that its measure leg should not be cited as a blocker.

---

## 2.5 Independent skeptic pass (§05.8.R) — VERDICT + repair

An independent skeptic was tasked to KILL the five headlines by named-second-object or precise-named-gap,
verifying every load-bearing citation verbatim on disk and running the cert.

**Result: NO-KILL on all five headlines (1.1, 1.2, 1.3, 1.5, 1.7).** Confirmed verbatim on disk:
- (A) BOOK_02:1291 does say the measure blocker is "removable (the Perron–Frobenius eigenvector is the
  canonical Aut-invariant measure)" and the carrier blocker is "genuine" — 1.2's measure/carrier split
  is an exact paraphrase, not a misread.
- (B) T1_FORCING_MEMO:79–81 does contain the "step-generated (Markov-on-edges)" scope restriction —
  1.3's maximality-scoping is supported.
- (C) CAMPAIGN_FINAL:56 does say "PRIM-SCENE-HISTORY-REFINEMENT-RULE stands" — the un-minted claim holds.
- (D/E) the cert genuinely computes W/NB from adjacency (5/5 mutants differ) and C6 is a real 718×718
  B+R eigen-computation; A's three nonzero eigenvalues genuinely embed. Not a stub.

**Single weakest point (accepted + REPAIRED):** the skeptic flagged that `--selftest` originally proved
graph-dependence via an in-process side computation rather than exercising the K-branch `die()` failure
paths its docstring advertised. *Repair applied:* `selftest()` now includes a DIE-PATH block that
evaluates the frozen-literal assertion (`W == 15708`) on mutant graph-derived carriers and confirms it
trips (2/2), exercising the real failure path a literal cert would not. Re-run: main rc=0, selftest
rc=0, DIE-PATH 2/2 + 5/5 graph-dependence. No headline changed.

**Minor label fixes accepted:** 1.3 cites T1's scope as "§2 open obligation"; it is item 2 of the
"Named open obligations" section (benign).

## 3. What this pass does NOT show
- No registry row changes status; no PROOF-TARGET closed; no primitive discharged.
- The T1 NB-forcing / presentation-covariance X″ remains an **un-minted reading-layer candidate**; it
  does NOT close 1.1–1.4. PRIM-SCENE-HISTORY-REFINEMENT-RULE stands.
- C6 (presentation covariance) is det/spectral-level ONLY; it does not supply the Ξ_N intertwiner.
- The carrier-count difference 15708 vs 14990 is a genuine STATE-SPACE difference; M1 forbids promoting
  either to physical content without the (missing) intertwiner.
