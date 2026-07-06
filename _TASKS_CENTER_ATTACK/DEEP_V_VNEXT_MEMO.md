# DEEP_V_VNEXT_MEMO — batch V-a: seven VNEXT / VNEXT+1 AF-tower no-gos (DRAFT v2, post-skeptic)

> **Post-skeptic banner (2026-07-06, verdict ACCEPTED IN FULL, no defense).** Six of seven verdicts
> SURVIVE. **NG-1 (33-SCENE-ANCHOR-OWNER) was WOUNDED-fixable** — the draft called the anchor "forced"
> without separating the two senses of *anchor* (dimension-level vs algebra-level); repaired to
> **DECOMPOSED-OWNED-SPLIT** with the exact boundary drawn (dimension-anchor forced & owned; algebra-anchor
> refuted & owned). One genuine registry-hygiene find escalated by the skeptic: **two book-cited,
> Lean-proved, cert-passing forcing owners have NO registry rows** (`D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001`,
> `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001`). Verdict + errors of record at §V.SKEPTIC.
> **Independent skeptic (2026-07-06): NO-KILL on all four load-bearing headlines (NG-1 split, the desync
> find, NG-6 Feshbach, NG-4 boundary-moved); check re-observed 36/36 + 11/11 mutations. Two honest
> observations folded in (B1.7 hedge; D0- prefixed ids).** Closing-pass addendum at §V.CLOSE.
> **No PROOF-TARGET is closed by the seven-no-go analysis itself; the closing pass proposes minting the two
> already-proven forcing owners (that is closure by registration, not by new proof).**

**Status:** DRAFT v2. No registry row edited; no book edited; no `.lean` added; `053040` untouched.
Deliverable check: `_TASKS_CENTER_ATTACK/deep_v_vnext_check.py` — **36/36 PASS, rc=0**, exact
integer/Fraction only; **mutation-tested 11/11 killed** (`--selftest`). All six existing certs for these
rows re-run green (`vp_vnext_af_scene_anchor_dimension_audit`, `vp_vnext_af_d0_spectral_invariant_comparison`,
`vp_vnext_af_one_dimensional_reduction_classification`, `vp_vnext_canonical_xi_anchor`,
`vp_vnext_joint_dirac_scale_selection`, `vp_vnext33_no_overclaim`), plus the two newer forcing certs
(`vp_scene_dim_even_fibonacci_forcing`, `vp_scene_laplacian_spectrum_forced`) — all rc=0.

**Pre-flight honored.** `preflight`-style greps of `CLAIM_TO_LEAN_MAP.csv` for all seven claim-IDs +
the cited modules; read-past of every book citation ±10 lines (BOOK_02:1285–1303, the `02.vnext33` /
`02.v2` cells). The prior cluster-tagging (UPLIFT_MAP §Cluster C/E/F/I) is treated as SUPERSEDED where the
book's Iter23–25 constructive attack has since moved the objects — flagged inline per row. This is NOT a
tagging pass: each verdict below is re-derived against the owned Lean + book text as it stands 2026-07-06.

**Ground truth (from W4_DECOMPOSITION_MEMO calibration).** The AF/Fibonacci tower is a correct FORMALISM
object that is NOT the scene's inductive completion. Every verdict here respects that frame; none reopens
it. The co-tower "read differently" template (W4 Target 1) is applied adversarially, not promotionally.

---

## The owned two-carrier picture (verbatim pre-facts, verified on disk)

Both carriers are built independently in `deep_v_vnext_check.py` Block 0; no check reuses a conclusion.

**Scene carrier** — complete tripartite `K(9,11,13)`, `|V| = 33`, parts `(9,11,13)` a `+2` progression.
- `SceneLaplacianSpectrumForced.lean:44-53`: the WHOLE Laplacian spectrum is the multipartite closed form
  `0¹, (N−nᵢ)^{nᵢ−1}, N^{k−1}` = `{0:1, 24:8, 22:10, 20:12, 33:2}`; multiplicity multiset `{1,2,8,10,12}`,
  trace `718 = 2|E|`, `|E| = 359` (prime).
- `SceneSpectralFingerprint.lean:53-59`: within-part difference subspace `K_i` (dim `n_i−1`) is the
  eigenspace for eigenvalue `= degree = 33 − n_i`. `K_9↔24, K_11↔22, K_13↔20`. Structural
  `H = R(3) ⊕ K(8,10,12)`.

**AF carrier** — Fibonacci AF/GNS, `dim A_N = 2,5,13,34,89,233,610` (odd-indexed `F(2n+3)`,
`VNEXT_DIRAC_TOWER_FROZEN_INPUTS.json`), scale ratio `φ`.
- `AFD0SpectralInvariantComparison.lean:32-36`: reduced martingale Dirac² multiplicities = Fibonacci
  increments with trace line removed = `{1,3,8,21}` (4 distinct), summing to `33`.
- `AFSceneAnchorDimensionAudit.lean:20-27`: `dim A_3 = 5²+3² = 34 = F₉`; scene `= 33`; excess `1`.

**The two objects are typed-distinct**, and that is the whole cluster's spine (P-TYPED). What the book's
Iter23–25 attack ADDED, and what re-types six of these seven rows, is below.

---

## NG-1. D0-VNEXT-33-SCENE-ANCHOR-OWNER-001 (row 428) + D0-VNEXT-33-SCENE-ANCHOR-NOGO-001 (row 434)

**Decisive owned statement (verbatim).**
- Owner (428): `AFSceneAnchorDimensionAudit.lean:41-45` `typed_audit_not_numerology`:
  "`dimAFanchor = dimScene + 1 ∧ afBlocks.length = 2 ∧ sceneParts.length = 3 ∧ afBlocks ≠ sceneParts`".
  Book BOOK_02:1301: "`34−1=33` is forbidden as a quotient proof."
- No-go (434): `AFD0SpectralInvariantComparison` — "double obstruction (structural Outcome D +
  scale-independent spectral mismatch `{1,3,8,21} != {1,2,8,10,12}`)".

**The two-sided object.** The pair is a single object read two ways. What is OWNED as anchor vs what is
BLOCKED as anchor sits on a sharp boundary that the standing task flags: *"33 = |K(9,11,13)| is owned; the
question is whether the ANCHORING of the AF tower at 33 is forced or selected."* Answer, in two senses:

1. **Algebra-level anchor (`PRIM-CANONICAL-33-SCENE-ANCHOR`): REFUTED and owned.** 33 is never an AF
   *algebra* dimension (`33 ∉ {2,5,13,34,89,…}`, check B1.8); the nearest is `dim A_3 = 34`, and
   `34−1=33` is a forbidden quotient. Two matrix blocks `(5,3)` ≠ three graph parts `(9,11,13)` (B1.5-6).
   This is the no-go (434) and it stands.

2. **Dimension-level anchor: FORCED and owned — but by a DIFFERENT, newer object.** BOOK_02:1295 (Iter25):
   the scene dimension `33` and the AF Dirac² eigenspace dimension coincide **and it is forced**:
   `33 = F₂+F₄+F₆+F₈` (even-indexed Fibonacci) `= F₉ − 1`, owned in `SceneDimEvenFibonacci.lean:47-49`
   `scene_dim_even_fibonacci_forcing`. The forcing root is the shared `+2` grading: zones are a `+2`
   progression (`SceneLaplacianSpectrumForced.lean:42`), even powers step `+2`; a `+1` step would import an
   external `ℤ₂` orientation bit, `⊥M1`. **On the anchor LEVEL `N⋆=3` (honest hedge, per skeptic):** `N⋆=3`
   is the *first* AF level with `dim A_N ≥ 33` (`dim A_2 = 13 < 33 ≤ 34 = dim A_3`, B1.7) — but the tower
   SKIPS 33 (lands on 34), so this is a dimension *crossing*, not a clean anchoring. B1.7 is the weakest leg
   of the split: it pins where the crossing happens, not that 33 is an AF dimension (it is not, B1.8). The
   forced/owned content lives in the even-Fibonacci EIGENSPACE dimension (`SceneDimEvenFibonacci`), which is
   `33` exactly; the algebra dimension is `34 = 33+1` (the `+1` kernel mode).

**Ladder worked.**
- (a) LIFT → positive result: the DIMENSION anchor IS lifted and forced — but this is already owned by
  `SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (book Iter25 + `SceneDimEvenFibonacci.lean`). This memo does not
  re-own it; it identifies it as the correct reading of the "anchor forced?" question.
- (b) CLOSE: is the anchor object owned somewhere? **Yes** — the dimension anchor is owned by the Iter25
  forcing module; the algebra anchor is owned-as-refuted by row 434. The pair is fully owned on both sides.
- (c) DECOMPOSE: the single word "anchor" decomposes into **dimension-anchor ⊕ algebra-anchor** — the
  former forced+owned, the latter refuted+owned. This IS the missing-object-is-a-constituent read: the
  "34 vs 33 coincidence" is a constituent (the `+1` kernel-mode gap) of the owned even-Fibonacci forcing,
  `dim(M₅⊕M₃) = F₉ = 33+1` (`SceneDimEvenFibonacci.lean:62-64`).

### VERDICT NG-1: **DECOMPOSED-OWNED-SPLIT** (owner 428 + no-go 434 jointly)
The boundary sits exactly at *dimension vs algebra*: **dimension-anchor = FORCED, owned by
`SCENE-DIM-EVEN-FIBONACCI-FORCING-001`** (Iter25, Lean-proved, cert-passing); **algebra-anchor = REFUTED,
owned by row 434.** The `34−1=33` "typed coincidence" of rows 428/434 is not a bare anti-numerology
capstone (as UPLIFT_MAP §126 GENUINE-BOUNDARY had it) — it is a *constituent* of the owned even-Fibonacci
forcing, the `+1` kernel-mode gap. **No status change proposed; the no-go is correctly scoped to the
algebra level and the positive dimension-forcing already has its own (unregistered) owner.**
⚠ The UPLIFT_MAP GENUINE-BOUNDARY tag for 428 is SUPERSEDED by Iter25 and should read
DECOMPOSED-OWNED-SPLIT.

---

## NG-2. D0-VNEXT-AF-ONE-DIMENSIONAL-REDUCTION-CLASSIFICATION-001 (row 429)

**Decisive owned statement (verbatim).** `AFOneDimensionalReductionClassification.lean:41-45`
`canonical_one_dimensional_reduction_no_go`: "`reducedParts.sum = 33 ∧ sceneParts.sum = 33 ∧
reducedParts ≠ sceneParts ∧ afBlocks.length ≠ sceneParts.length`" — i.e. `(24,8,1)` from 2 blocks ≠
`(9,11,13)` from 3 parts (Outcome D).

**Ladder worked.**
- (a) LIFT: does a canonical line exist? Yes — the trace/cyclic line `C·1` is canonical for the tracial
  Perron state (`:28-35`). So the object is not absent; the *reduction* it induces is what mismatches.
- (b) CLOSE: is the `(24,8,1)` object owned? Yes, as the su(5)⊕su(3)⊕u(1) trace-zero reduction, owned in
  this same module. The mismatch is owned.
- (c) DECOMPOSE / (d) BOUNDARY: the mismatch `2 blocks ≠ 3 parts` is a genuine typed structural fact, not
  a missing constituent. **Non-vacuity control (B2.5):** the control scene `K(11,11,11)` also sums to 33
  but is *regular* (single nonzero degree 22) — so the mismatch is scene-SPECIFIC to the `+2`-graded
  `(9,11,13)`, not a generic artifact of "sum = 33". This is the honest boundary.

### VERDICT NG-2: **GENUINE-BOUNDARY-PROVEN (sharpened)** — the `2 matrix blocks vs 3 graph parts`
structural mismatch is real, owned, and scene-specific (control-verified). I/O typing: **input** = a
partition-respecting encoding `χ: (24,8,1)→(9,11,13)` (does not exist: 2<3 blocks, B3.1); **output** = the
owned Outcome-D no-go. Consistent with UPLIFT_MAP §127 GENUINE-BOUNDARY; sharpened by the `K(11,11,11)`
control showing it is not generic. No status change.

---

## NG-3. D0-VNEXT-CANONICAL-XI-ANCHOR-OWNER-001 (row 430)

**Decisive owned statement (verbatim).** Row 430: "No canonical scene-encoding chi: AF-reduced (24,8,1) ->
V9 ⊔ V11 ⊔ V13 (incompatible finite structure) ... a dimension-only Xi is ruled out by the spectral
invariant obstruction. PRIM-COMPARISON-MAP-XI-N remains independent." Cites
`AFOneDimensionalReductionClassification`.

**Ladder worked.**
- (a)/(b): is a canonical Ξ owned anywhere? The primitive dependence matrix
  (`VNEXT33_PRIMITIVE_DEPENDENCE_MATRIX.csv`) records `PRIM-COMPARISON-MAP-XI-N` as **NEW (independent; not
  derived from the anchor)**, with `minimal_new_data = "a canonical scene-encoding chi to V9⊔V11⊔V13
  compatible with the 9/11/13 partition AND the scene Laplacian multiplicity structure"`. So the Ξ object
  is NOT owned — it is a named external primitive whose exact missing data is registered.
- (c) DECOMPOSE: Ξ would need to satisfy TWO owned constraints simultaneously — partition-respect (NG-2
  kills it: 2<3 blocks) AND multiplicity-preservation (NG-6 kills it: `{1,3,8,21}≠{1,2,8,10,12}`,
  scale-independent). A "dimension-only Ξ" evades neither. The absence factorizes into the two owned
  obstructions — this is the T6 corollary read (UPLIFT_MAP §128 had it as corollary-of AF-reduction +
  spectral obstruction; CONFIRMED here with the exact two-constraint factorization).

### VERDICT NG-3: **DECOMPOSED-OWNED (corollary)** — the missing canonical Ξ is not a new gap; it is the
conjunction of two owned no-gos (NG-2 partition-respect + NG-6 multiplicity-preservation), and its exact
missing data is registered in the primitive dependence matrix. `PRIM-COMPARISON-MAP-XI-N` stays an
independent named primitive (external import). No status change; matches UPLIFT_MAP corollary tag.

---

## NG-4. D0-VNEXT-JOINT-DIRAC-SCALE-SELECTION-OWNER-001 (row 431)

**Decisive owned statement (verbatim).** Row 431: "The anchor does NOT co-select the Dirac scale: with no
canonical Xi there is no anchored spectral-matching condition. PRIM-DIRAC-SCALE-SELECTION remains the
independent primitive."

**READ-PAST — a BOOK↔REGISTRY CONTRADICTION (the decisive find here; corrects the draft).** BOOK_02:1289
(Iter24) *claims* `D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001`: "its `PRIM-DIRAC-SCALE-SELECTION` blocker
was resolved to `λ_N = λ_0·φ^N` ... the covariance cocycle `ω(N)=φ` is determined." **But the registry row
445 says the OPPOSITE, verbatim:** row 445 is `status=OPEN, PROOF-TARGET`, text = *"Scale cocycle is
refinement-family-dependent; with the family underdetermined no unique cocycle. Missing
PRIM-DIRAC-SCALE-SELECTION."* This matches the memory note `d0-vnext2-corpus-fork-desyncs` (row 445 STAYS
OPEN; its cert is content-free/float/phantom-citation). The Lean `CanonicalDiracCovariance.lean:35`
`cocycle_constant_phi` proves `ω=φ` **only conditionally on `InternallySourced lam`** — i.e. IF the scale
is already the φ-ladder THEN the cocycle is φ (near-tautological); it does NOT force the φ-ladder. So the
honest registry-truth is: **the scale-law leg is NOT closed** — it is family-dependent and PROOF-TARGET.
Row 431's narrow claim (the *anchor* does not co-select the scale via Ξ) stands independently and is true.

**Ladder worked.**
- (b) CLOSE: is the scale-selection object owned? **NO (registry-honest).** Only the conditional cocycle
  identity `InternallySourced ⇒ ω=φ` is Lean-owned; the *selection of the family/law itself* is OPEN
  (row 445 PROOF-TARGET). This is a genuine external import, not a closed leg.
- (c) DECOMPOSE: `PRIM-DIRAC-SCALE-SELECTION` splits into **conditional-cocycle-identity (Lean-owned,
  tautological given the ladder) ⊕ family/law-selection (OPEN, external `PRIM-SCENE-HISTORY-REFINEMENT-RULE`
  dependent, row 445)**. Row 431 owns the anchor-co-selection statement; neither row closes the law.

### VERDICT NG-4: **OPEN-sharpened** (⚠ draft's "boundary-moved / scale-law owned" RETRACTED). The scale-law
is NOT owned: BOOK_02:1289's optimistic prose is contradicted by registry row 445 (OPEN/PROOF-TARGET,
"family-dependent ... no unique cocycle"), and the Lean identity is conditional-on-the-ladder. `PRIM-DIRAC-
SCALE-SELECTION` splits into a tautological conditional cocycle (owned) ⊕ the family/law selection (OPEN,
external, refinement-family-dependent). Row 431's own narrow claim (anchor ⊮ scale via Ξ) stands. This is a
book↔registry desync to flag, NOT a closure. No status change to row 431 itself (its narrow claim
stands).

---

## NG-5. D0-VNEXT-JOINT-DIRAC-ANCHOR-NOGO-001 (row 435)

**Decisive owned statement (verbatim).** Row 435: "PRIM-DIRAC-SCALE-SELECTION and PRIM-COMPARISON-MAP-XI-N
are NOT unified by one anchor (D0-VNEXT-33-SCENE-ANCHOR-NOGO-001); they remain INDEPENDENT primitives
(Phase F result 4)." Cites `AFD0SpectralInvariantComparison`.

**Ladder worked.** This is the capstone of the pair NG-4/NG-3: the two primitives are independent because
the would-be unifier (the anchor via Ξ) does not exist. The independence is *witnessed decisively* by the
scale-INDEPENDENCE of the spectral obstruction (B5.3): the multiplicity mismatch `{1,3,8,21}≠{1,2,8,10,12}`
holds for ANY Dirac scale (multiplicities are scale-invariant; scale sets only eigenvalues), so no choice
of scale can be made to induce a matching Ξ — the anchor cannot couple the two primitives.

### VERDICT NG-5: **DECOMPOSED-OWNED (corollary/capstone)** — independence-of-two-primitives is the
conjunction of NG-3 (no Ξ) and the scale-independence of NG-6; it introduces no new object. This is the
T6 corollary read (UPLIFT_MAP §132), CONFIRMED. The one refinement: independence is *decisive*, not merely
unwitnessed, because the blocking invariant (multiplicities) is provably orthogonal to the free parameter
(scale). No status change.

---

## NG-6. D0-VNEXT-AF-D0-SPECTRAL-COMPRESSION-OWNER-001 (row 432)

**Decisive owned statement (verbatim).** `AFD0SpectralInvariantComparison.lean:55-57`
`spectral_invariant_obstruction`: "`afReducedMults ≠ sceneMults ∧ afReducedMults.length ≠
sceneMults.length`". Book row: "the scale sets eigenvalues not multiplicities, so NO unitary Xi and NO
scale can match" — DECISIVE, scale-independent.

**Ladder worked — this is the richest row; UPLIFT_MAP §130 tagged it T1 (multiplicity fingerprints ARE
typed separators). CONFIRMED and DEEPENED via the book's Iter23–25 sharpening:**
- (a) LIFT — the obstruction quantity IS an owned object. The AF multiset `{1,3,8,21}` is exactly the
  **even-indexed Fibonacci** numbers `{F₂,F₄,F₆,F₈}` (B6.4), i.e. the reduced multiplicities ARE the
  forced dimension grading of NG-1. The scene multiset `{1,2,8,10,12}` is the multipartite closed-form
  fingerprint (`SceneLaplacianSpectrumForced`). Both are owned typed invariants; the no-go is the
  statement that no intertwiner crosses between two owned typed fingerprints (P-TYPED).
- (b) CLOSE — is a compression object owned? **YES, and this is the key read-past find.** BOOK_02:1297 +
  registry **row 433 `D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001` (CERT-CLOSED)**: the canonical
  Feshbach compression against the scene's own Aut-invariant zone split (bulk 20 / traced boundary 13,
  `D_tt = 20·I₁₃` because boundary degree `33−13=20`, B7.3) performs **exactly the `5→4` distinct-eigenvalue
  reduction a unitary cannot**, dropping eigenvalue 20 to give `{0,22,24,33}` (B7.2). So the "compression"
  the no-go says no *unitary* achieves IS achieved by a *projection split* — owned, cert-closed.
- (d) BOUNDARY — what genuinely stays external. Even the Feshbach-compressed spectrum `{0,22,24,33}` is
  NOT the AF geometric ladder `φ²:φ⁴:φ⁶` (B7.4), and the root obstruction sharpens (Iter24, BOOK_02:1291)
  from "no unitary" to a **UCP/interlacing binding inequality**: the AF corner embeds for `k≤4` but is
  infeasible for `k≥5` because `20/φ² > 33/φ⁴ ⇔ 20φ > 13` (B8.1), i.e. the scene's dynamic range
  `d₁/d_top = 20/33 ≈ 0.606 > 1/φ² ≈ 0.382` (B8.2, exact via `20/33 > 5/13 ≥ 1/φ²`) is too bunched to host
  the geometric ladder. This depends only on the eigenvalue RANGE, controlled two ways in the book's cert
  (spread control admits `k=5`; multiplicity permutation does not) — a genuine, sharp, owned boundary.

### VERDICT NG-6: **DECOMPOSED-OWNED + GENUINE-BOUNDARY (layered)** — three layers, each owned:
(i) the multiplicity fingerprints `{1,3,8,21}` (= even-Fibonacci, NG-1 grading) and `{1,2,8,10,12}` (=
multipartite closed form) are owned typed separators [T1, UPLIFT_MAP §130 CONFIRMED]; (ii) the `5→4`
compression the *unitary* cannot do IS owned by a *projection split*, row 433 CERT-CLOSED; (iii) what
remains a true boundary is spectral CONGRUENCE — the interlacing inequality `20φ>13` proves the scene is
too bunched for the `φ`-ladder at every `k≥5`, scale-independently. The row is correctly a NO-GO for
*congruence*; the weaker *compression* it seemed to also block is owned positively. No status change to
row 432.

---

## NG-7 (paired restatement). D0-VNEXT-33-SCENE-ANCHOR-NOGO-001 as the double-obstruction capstone

Row 434 is the capstone conjoining NG-2 (structural Outcome D) + NG-6 (spectral mismatch). Its verdict is
inherited: **DECOMPOSED-OWNED-SPLIT** on the anchor axis (NG-1) with both legs owned. It is not an
independent object; it is the `AND` of two owned no-gos, exactly as its own text says ("double
obstruction"). Confirmed; no status change.

---

## §V.SKEPTIC — independent pass (2026-07-06, ACCEPTED IN FULL, no defense)

**Per-row verdicts (skeptic):** NG-2, NG-3, NG-5, NG-6, NG-7 SURVIVE. **NG-1 WOUNDED-fixable** — repaired
(dimension/algebra split). **NG-4 re-graded during the CLOSING pass** from "DECOMPOSED-OWNED/boundary-moved"
to **OPEN-sharpened** after a book↔registry contradiction was found (row 445 OPEN says the OPPOSITE of
BOOK_02:1289) — see §V.CLOSE and the corrected NG-4 verdict. Independent skeptic returned **NO-KILL on all
four load-bearing headlines** (NG-1 split, EoR-V-2 desync, NG-6 Feshbach, NG-4), re-observing 36/36 +
11/11.

### Errors of record (enumerated, no defense; repairs applied inline)

- **EoR-V-1 (NG-1, the wound):** the pre-skeptic draft wrote "the 33-anchor is FORCED" without splitting
  the two senses of *anchor*. That is an over-read exactly of the kind the standing 33-anchor NO-GO (434)
  punishes: the ALGEBRA anchor is refuted. *Fix:* verdict re-graded to **DECOMPOSED-OWNED-SPLIT** with the
  boundary drawn at dimension-vs-algebra; the forced claim restricted to the dimension anchor and
  attributed to its actual owner `SCENE-DIM-EVEN-FIBONACCI-FORCING-001`, not claimed as this memo's result.
- **EoR-V-2 (registry hygiene, escalated by skeptic — the substantive find):** the two forcing owners that
  carry the positive dimension-lift — `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` and
  `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001` (D0- prefixed, matching BOOK_02:1295) — are **cited as owned in
  BOOK_02:1295**, have **Lean modules**
  (`SceneDimEvenFibonacci.lean`, `SceneLaplacianSpectrumForced.lean`) and **passing certs**
  (`vp_scene_dim_even_fibonacci_forcing.py`, `vp_scene_laplacian_spectrum_forced.py`, both rc=0), but have
  **ZERO registry rows** (`grep` field-1 count = 0 for both). Their cited upstream owners (BRATTELI row 411,
  PERRON-SCALE-FLOW row 413) DO have rows. This is a book↔registry desync (the positive Iter25 result is
  un-minted). *Fix:* flagged as a hygiene item for integration; NO row added here (task: propose row-notes
  only). Sibling of the memory note `d0-vnext2-corpus-fork-desyncs`.
- **EoR-V-3 (NG-4, RETRACTED over-read — found in the closing pass):** the draft claimed the scale-law leg
  was "owned (`λ_N=λ_0φ^N`)" per BOOK_02:1289. That is contradicted by registry row 445, which is
  `OPEN/PROOF-TARGET` with text *"Scale cocycle is refinement-family-dependent ... no unique cocycle.
  Missing PRIM-DIRAC-SCALE-SELECTION."* The Lean `cocycle_constant_phi` is CONDITIONAL on
  `InternallySourced lam` (tautological given the φ-ladder). *Fix:* NG-4 re-graded **OPEN-sharpened**; the
  scale-law is a genuine external import, not a closed leg. The book↔registry contradiction is itself flagged
  as a desync (sibling of `d0-vnext2-corpus-fork-desyncs`).
- **EoR-V-4 (NG-6, near-conflation check):** verified the Feshbach compression (row 433) is a *sample-z
  projection split*, NOT a unitary and NOT a proof of congruence — row 433's own text warns "the compressed
  spectrum is not the geometric φ-ladder." *Fix:* congruence kept strictly as the residual boundary; no
  over-read that row 433 dissolves NG-6.

### Pre-registered attack surface (author, before skeptic)

- **ATT-1 (NG-1, strongest self-attack, FIRED):** "the 33-anchor is forced" is an algebra→dimension
  equivocation; the algebra anchor is owned-refuted. Tripwire: if the skeptic finds the forced claim lives
  on a *different* object than the no-go blocks, drop to DECOMPOSED-OWNED-SPLIT. FIRED (EoR-V-1).
- **ATT-2 (NG-6):** does B6.4 (`{1,3,8,21}` = even-Fibonacci) construct the AF multiset from the NG-1
  grading conclusion? No — `af_reduced` is built in Block 0 from `dimA` increments independently; `even_fib`
  is built from `fib(2j)` independently; B6.4 COMPARES them. Trap-(f) avoided.
- **ATT-3 (NG-6, Feshbach over-read):** claiming row 433 dissolves NG-6 would be a category error
  (projection-split ≠ unitary intertwiner). Pre-registered as NOT claimed; congruence stays the boundary.
- **ATT-4 (B8 exactness):** the interlacing inequality is checked via integer/rational surrogates
  (`500>9`, `20/33 > 5/13`), never float — `1/φ² = 2−φ < 5/13` since `φ² > 13/5 = 2.6` (`2.618>2.6`).

### Mutation log (11/11 killed, `deep_v_vnext_check.py --selftest`)

B1.1 (dim 33→34); B1.2 (algebra 34→35); B2.1 (reduced (24,8,1)→(24,8,2)); B4.1 (AF multiset shift);
B4.2 (scene top-mult k→k+1); B6.1 (even→odd Fibonacci); B7.2 (compression keeps 20); B1.7 (anchor level
2 not 3); B8.2 (dynamic-range flip); B6.2 (sum 33→34); B7.3 (boundary degree 21).

---

## Proposed ROW-NOTES (no registry motion made — proposals only)

1. **Row 428 (33-SCENE-ANCHOR-OWNER):** add note — "The dimension-anchor is FORCED and owned by
   `SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (33=F₂+F₄+F₆+F₈=F₉−1, shared +2 grading); this row's refuted
   `PRIM-CANONICAL-33-SCENE-ANCHOR` is strictly the ALGEBRA-level anchor. The `34−1=33` typed coincidence is
   the `+1` kernel-mode gap of that owned forcing, not a bare numerology capstone."
2. **Row 431 (JOINT-DIRAC-SCALE-SELECTION):** add note — "`PRIM-DIRAC-SCALE-SELECTION` splits into a
   conditional cocycle identity (`InternallySourced ⇒ ω=φ`, Lean `CanonicalDiracCovariance`, tautological
   given the φ-ladder) ⊕ the family/law SELECTION, which is OPEN (row 445 PROOF-TARGET,
   refinement-family-dependent). This row owns only the anchor-co-selection statement. NB book↔registry
   desync: BOOK_02:1289 reads the scale as resolved; registry row 445 reads it OPEN — flag for reconcile."
3. **Row 432 (AF-D0-SPECTRAL-COMPRESSION):** add note — "The `5→4` distinct-eigenvalue reduction that a
   unitary Ξ cannot perform IS owned by the projection-split `D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001`
   (row 433, CERT-CLOSED); this row is a NO-GO for spectral CONGRUENCE only. Root sharpened to the
   interlacing inequality `20φ>13` (scene too bunched for the φ-ladder, k≥5)."
4. **Registry hygiene (HIGH) — MINT PROPOSAL (this is CLOSURE by registration):** add rows for
   `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` and `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001` — both are
   book-cited (BOOK_02:1295), Lean-proved (`SceneDimEvenFibonacci`, `SceneLaplacianSpectrumForced`),
   cert-passing (rc=0), but have no registry rows. Proposed rows: status `LEAN_PROVED`, no-go field n/a
   (these are POSITIVE owners), cert `vp_scene_dim_even_fibonacci_forcing.py` /
   `vp_scene_laplacian_spectrum_forced.py`, module `D0.VNext2.SceneDimEvenFibonacci` /
   `D0.VNext2.SceneLaplacianSpectrumForced`, book `BOOK_02` cell `02.v2`. This is the ONE genuine closure the
   closing pass produces: the positive dimension-lift is already proven; it only needs minting.

---

## §V.CLOSE — closing pass: which VNEXT no-gos CLOSE (both sides owned) vs retain external import

**Closure test (strict):** an object CLOSES iff EVERY leg is owned internally (Lean-proved or CERT-CLOSED)
with **nothing routed through a live external primitive** (`PRIM-*` POSTULATED / `ASSUMP-*` / OPEN
PROOF-TARGET). One more question was asked of each row: *can the owned decomposition be connected to the
missing piece to make it two-sided-owned?*

**(a) The 33-anchor (NG-1 / NG-7): CLOSED — two-sided owned, nothing external.**
The "boundary" between dimension-anchor and algebra-anchor is not a hole; it is two owned facts sitting
side by side:
- dimension-anchor = FORCED + owned: `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (`SceneDimEvenFibonacci.lean`,
  Lean-PROVED, cert rc=0). `33 = F₂+F₄+F₆+F₈ = F₉−1`, shared `+2` grading.
- algebra-anchor = REFUTED + owned: rows 428/434 (`AFSceneAnchorDimensionAudit`,
  `AFD0SpectralInvariantComparison`, both LEAN_PROVED). `34−1=33` forbidden quotient; `33∉` AF algebra dims.
Both legs are internal, Lean-owned, cert-passing. Nothing is imported. **RE-GRADE NG-1/NG-7:
DECOMPOSED-OWNED → CLOSED (two-sided owned)**, contingent ONLY on the hygiene mint of the dimension-forcing
row (row-note 4). No external physics enters.

**(b) The two forcing owners: CLOSE by minting (closure, not a hole).** `D0-SCENE-DIM-EVEN-FIBONACCI-
FORCING-001` and `D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001` are Lean-PROVED + cert-passing already — the only
"gap" is a missing registry row. Minting them (row-note 4) is closure by registration. **+2 closed rows.**

**(c) The others — do they close?**
- **NG-2 (AF-ONE-DIM-REDUCTION):** both sides owned (canonical line exists; `(24,8,1)≠(9,11,13)`
  control-verified). No external import — the mismatch is a *proven internal structural fact*.
  **CLOSED as GENUINE-BOUNDARY-PROVEN** (a boundary that is itself a closed theorem, not an open hole).
- **NG-3 (CANONICAL-Ξ-ANCHOR):** does NOT close. The missing Ξ is the conjunction of NG-2 + NG-6 (both
  owned), BUT `PRIM-COMPARISON-MAP-XI-N` remains a NEW external primitive whose `minimal_new_data` (a
  canonical scene-encoding χ) is genuinely absent. **Retains external import.**
- **NG-6 (SPECTRAL-COMPRESSION):** the compression leg CLOSES (row 433 CERT-CLOSED does the 5→4 reduction);
  the *congruence* leg is a **proven internal boundary** (`20φ>13`, scale-independent, no external input).
  So NG-6 has NO live external import — every leg is either owned-positive or owned-impossible.
  **CLOSED (layered: owned compression + proven-impossible congruence).**
- **NG-4 (JOINT-DIRAC-SCALE-SELECTION) + NG-5 (JOINT-DIRAC-ANCHOR):** do NOT close. NG-4's scale-law leg is
  OPEN (row 445 PROOF-TARGET, family-dependent) — a **genuine external import** (`PRIM-DIRAC-SCALE-SELECTION`
  / `PRIM-SCENE-HISTORY-REFINEMENT-RULE`). NG-5 (independence capstone) inherits NG-3's missing Ξ.
  **Both retain external import.**

### Closure scoreboard (the exact count that drops)

| no-go | before (boundary/open count) | after closing pass | closes? |
|---|---|---|---|
| NG-1 33-ANCHOR-OWNER (428) | GENUINE-BOUNDARY (UPLIFT_MAP) | **CLOSED** (two-sided owned) | ✅ |
| NG-7 33-ANCHOR-NOGO (434) | boundary capstone | **CLOSED** (inherits NG-1) | ✅ |
| NG-2 AF-ONE-DIM-REDUCTION (429) | GENUINE-BOUNDARY | **CLOSED** (boundary = proven theorem) | ✅ |
| NG-6 SPECTRAL-COMPRESSION (432) | NO-GO (owner) | **CLOSED** (owned compression + proven-impossible congruence) | ✅ |
| NG-3 CANONICAL-Ξ-ANCHOR (430) | corollary | **retains external import** (PRIM-Ξ) | ❌ |
| NG-4 JOINT-DIRAC-SCALE (431) | (draft: owned) → | **OPEN-sharpened, external** (scale-law PROOF-TARGET) | ❌ |
| NG-5 JOINT-DIRAC-ANCHOR (435) | corollary | **retains external import** (inherits Ξ) | ❌ |
| + mint DIM-EVEN-FIB owner | (no row) | **CLOSED by minting** | ✅ |
| + mint LAPLACIAN-SPECTRUM owner | (no row) | **CLOSED by minting** | ✅ |

**Count that drops:** of the 7 filed AF-tower no-gos, **4 CLOSE** (NG-1, NG-7, NG-2, NG-6 — both sides
owned / proven-impossible, nothing external) and **3 retain a genuine external import** (NG-3, NG-4, NG-5,
all gated on the single missing object `PRIM-COMPARISON-MAP-XI-N` and the OPEN scale-law
`PRIM-DIRAC-SCALE-SELECTION`). Plus **2 positive forcing owners close by minting**. Net: the cluster's
open frontier collapses from "7 AF-tower boundaries" to **exactly two external primitives** (Ξ and the
scale-law), both already named and registered as PROOF-TARGET. The scene↔AF story is closed on the
DIMENSION + COMPRESSION + STRUCTURAL axes; it stays open only on the CONGRUENCE-enabling Ξ and the scale
selection — and congruence itself is proven impossible (`20φ>13`), so the residual external import is
strictly the *encoding* Ξ and the *scale law*, not the congruence.

## What this memo does NOT show

- No new PROOF-TARGET is *proven* closed by fresh proof; the 4 CLOSED rows close because their legs were
  already owned (Lean/cert) — the closing pass RE-READS them as two-sided owned, and proposes minting the 2
  un-registered forcing owners (closure by registration).
- No third generation; no scene↔AF spectral congruence (proven-impossible boundary via `20φ>13`).
- The scale-law is NOT owned (registry row 445 OPEN contradicts BOOK_02:1289 — flagged as desync).
- The `{1,3,8,21}`/`{1,2,8,10,12}` fingerprints remain typed separators; no intertwiner crosses them.
- Nothing here touches `053040`, the α-seam, or the M2 torsor.
