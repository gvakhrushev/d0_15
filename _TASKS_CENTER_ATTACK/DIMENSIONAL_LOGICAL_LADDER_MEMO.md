# DIMENSIONAL-LOGICAL LADDER FORGE — what is REAL, what is READING, what lands on the external bridge

Date: 2026-07-07. Owner conceptual synthesis. **Memo-only. No registry / book / `.lean` edit. `053040` untouched.**
Verifier: `close_dim_logical_check.py` (can-fail, 7 mutations, each flips a CONCLUSION; clean = all-PASS).

Owner proposal (verbatim of the directive): the master equation's `1` is a **0-dimensional logical
boolean** (existence yes/no); the ladder is `0D existence (boolean) → 1D membership (vector, term p)
→ 2D value (area, term p²)`; logic resting on probabilities → the path to qubits/QM.

**This is the highest over-claim-risk area in the corpus** (QM burned twice: `D0-M1-QM-nonunitary`
demoted, colour "forced" demoted). The memo holds the honesty line HARD and pre-registers the QM
over-claim as the primary self-attack. Its net result is a **reading/correspondence + one honest
external-bridge deepening**, NOT a new closure.

---

## 0. Pre-flight (done, §05.8.U) — prior art that this memo must NOT duplicate

- **`DIMENSIONAL_LENS_MAP.md`** (2026-07-07) already sweeps the degree-2/p³ cap UPWARD (every no-go as
  a degree/dimension exhaustion). This memo is orthogonal: it extends the ladder DOWNWARD by one
  (the `0D` question) and forges the two NEW payoffs (2D-complex correspondence, qubit skeleton). No
  overlap of claims; cross-reference, not re-derivation.
- **`D0-DETECTION-QUADRATIC-001`** (BOOK_01:1130, CORE-FORMALIZED, LEAN_PROVED) already owns the
  degree ladder `{membership p, value p²}`. The parent.
- **THE 02.19B** (BOOK_02 §02.19B: header :1620, theorem statement :1624, strata :1626/:1627/:1628)
  already reads the scene as a `0-1-2 skeleton` (points/lines/areas) and already ties the 2-skeleton
  to QM (ħ). **This is the REAL owned find of item 2** — an owned 0-1-2 topological stratification —
  and it also forces an honesty correction (see §2, RISK-C).
- **`D0-M1-INFO-RECONSTRUCTION-001`** (BOOK_00:473, `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`,
  `ASSUMP-M1-INFO-RECONSTRUCTION`) is the external M1⇒complex-QM bridge. **The qubit/QM path lands
  here; this memo does not move it.**
- **`D0-COMPOSITION-REAL-QUOTIENT-EQUIVALENCE-001`** (BOOK_02, PASSPORT-CLOSED) — the existing
  2-qubit passport (external PRL owner). Confirms "qubit" content is already externally owned, never
  present-core.

---

## 1. THE 0-D BOOLEAN LAYER — GRADE: **AUTHORED-GLOSS** (not an owned reading)

### Owned anchors, re-read verbatim on disk (±10)

- **BOOK_01:1130** (the parent, CORE): *"A detection has exactly two comparison kinds: by
  **membership** (∈) — levels 'existence-class' vs 'event-in-class' are different categories
  (Russell hierarchy), so they compare linearly, against a reference of belonging (degree 1, the
  term p); and by **value** … (degree 2, the term p²). Unity is exhausted by the direct and the
  mutual contribution, p+p²=1 … a would-be third is a degree-3 term p³=2p−1, which reduces into
  span{1,p} … So the tower closes on three levels by exhaustion of comparison kinds."*
- **BOOK_01:253** (record quantum): *"The symbol 𝔮 is the irreducible addressable record quantum.
  The dyad closes only when the comparison produces a finite registration."*
- **BOOK_01:1539** (sign bit): *"The sign bit {+,−} is the irreversibility of write/erase; it is the
  one bit that distinguishes the act from its undo."*
- **BOOK_01:496 / 312**: the master equation `p+p²=1` (and `x²=x+1` at :171); the `1` is the **unit
  section / unit probability capacity** being exhausted (`:608` "normalized to unit probability
  capacity").

### The finding (why AUTHORED-GLOSS, stated against the owner's own reading)

The owner's ladder wants `0D = existence boolean` as a graded slot **below** membership. The owned
text places existence in the OPPOSITE spot: at **:1130** "existence-class vs event-in-class" is the
content of the **degree-1 membership comparison itself** — existence is the reference of belonging
*against which* the degree-1 term `p` compares, not a separate degree-0 term. And the master-equation
`1` is the **RHS unit section** (the total probability being partitioned), not a graded LHS term.

So the honest algebra has exactly **two graded p-terms** (`p`, `p²`) resting on **one unit** — three
*levels* `{unit, p, p²}` but only two *graded slots*. Calling the unit a "0-D existence boolean" is a
**mnemonic re-label of the RHS**, not a distinct owned degree.

Two genuine "boolean/bit" objects DO exist in the corpus, but neither is the master-equation `1`:
1. the **orientation sign bit** `{+,−} = Z(Q₈) = [Q₈,Q₈] = {±1}` (BOOK_01:830, `D0-OMEGA8-CENTER-001`,
   LEAN_PROVED) — a genuine ℤ₂, but it is the **phase** bit, and it is added at the terminal/orientation
   layer, not "below membership";
2. the **record quantum 𝔮** (:253) — the atomic yes/no of registration — which is the closest thing
   to an "existence boolean," but the text types it as the *dyad's registration output*, not as a
   degree-0 term in the `p`-ladder.

**Honest ladder:** `{unit section (1) ; membership (p, deg 1) ; value (p², deg 2)}` = three levels,
**all owned as such** at :1130 — but the "0D = existence boolean" naming of the unit is a **gloss**.
It is a *legitimate, evocative* gloss (registration IS boolean-flavoured, via 𝔮 and the sign bit),
so it is safe as a **note/analogy**, unsafe as a "derived degree-0 level."

**GRADE 1: AUTHORED-GLOSS.** (Mintable only as an analogy note on `D0-DETECTION-QUADRATIC-001`
recording that the unit section is registration-typed — never as a new graded level.)

---

## 2. THE SCENE AS A 2-D SIMPLICIAL COMPLEX — GRADE: **SUGGESTIVE-BUT-UNOWNED** (owned skeleton, unowned dimensional link)

### The exact computation (independently built, in `close_dim_logical_check.py`)

- `K(9,11,13)` is tripartite ⇒ a clique picks **one vertex per part**, so maximal cliques are
  **triangles**; a 4-clique would need two vertices in one part (adjacent ⇒ contradiction, parts are
  independent sets). **No K₄.** Hence the clique complex is **2-dimensional by construction**:
  `top face dim = (#parts) − 1 = 3 − 1 = 2`. (Verified; mutation 4 "K₄ exists" FAILS.)
- **f-vector** `(V, E, T) = (33, 359, 1287)` = the 0/1/2-dimensional faces = the elementary
  **symmetric functions of the zones**: `V = Σnᵢ = 33`, `E = e₂ = n₁n₂+n₁n₃+n₂n₃ = 359`,
  `T = e₃ = n₁n₂n₃ = 1287`. All three owned verbatim: BOOK_01:915 (`|T|=1287`), BOOK_01:1604
  (`|V|=33; edges 359; triangles 1287`), and the symmetric-function identity is `D0-RANK3-CUBIC-
  SYMMETRIC-FUNCTIONS-001` (LEAN_PROVED: `359=|E|`, `2574=2∏`). (Verified.)

### Does owned text read the scene DIMENSIONALLY? — YES, strongly.

- **BOOK_02 §02.27, cochain block :1817** (prose lead-in :1814): *"the clique complex of K(9,11,13):
  C⁰ ⟵∂₁ C¹ ⟵∂₂ C², ∂₁∂₂=0"* — the scene is explicitly a **cochain complex with top degree C²**.
  This is OWNED.
- **BOOK_02 §02.19B (:1620/:1624), THE 02.19B "Homological unification 0-1-2":** *"The carrier carries
  exactly three orthogonal homological strata — points, lines, areas"* (:1624), then *"0-skeleton
  (vertices, |V|=33)"* (:1626), *"1-skeleton (edges, |E|=359)"* (:1627), *"2-skeleton (plaquettes/
  faces) … quantum mechanics … ħ"* (:1628). The `0-1-2` faces are named, counted, and used. **This
  owned 0-1-2 topological stratification is the real find.**

### What is OWNED vs what is the memo's own reading (be exact)

**OWNED (2 of 3 sub-facts):**
1. **f-vector = zone elementary symmetric functions:** `(V,E,T)=(33,359,1287)=(e₁,e₂,e₃)`
   (BOOK_01:915, :1604; `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001` LEAN_PROVED). Owned.
2. **the scene is a 0-1-2 cochain/homological complex:** C⁰←C¹←C² (:1817) and the named 0/1/2-strata
   (§02.19B). Owned.

**SOUND-BUT-UNOWNED (the load-bearing dimensional claim):**
3. **"tripartite ⇒ top face dim = 2, no K₄":** TRUE and computed here (`(#parts)−1=2`; a 4-clique needs
   two vertices in one part, forbidden). But **no owned sentence states the scene is 2-dimensional
   *because* tripartite, calls out "no K₄", or says "top dimension = 2".** §02.19B *works with* three
   strata; it never asserts there are no higher faces. So the "2D" claim is the memo's own (sound)
   computation, not owned text.

### The correspondence being proposed (a reading, NOT a certified identity)

**READING (not owned):** the scene's top simplicial dimension (2) and the detection degree cap (2)
are *numerically equal*, and their mechanisms are *parallel* — "3 tripartite parts ⇒ cap 2 via
`(#parts)−1`" alongside "3 comparison-levels {1,p,p²} ⇒ cap 2 via `p³∈span{1,p}`." **The checker
verifies only the numeric equality `2=2` (check `2c`); it does NOT certify that the two caps share
one root.** The "same M1 root" is a mechanism-parallel *reading*, not a proven identity — the two `2`s
could be structurally parallel yet distinct objects. Stated plainly so no downstream reader mistakes
`2c` for a certification of the correspondence.

### RISK-C (the honesty correction that survives the skeptic)

Two independent unowned steps sit under the proposed correspondence: (i) the "2D" claim itself
(SOUND-BUT-UNOWNED, above), and (ii) the "face-dimension = detection-degree" link. What IS owned
(§02.19B :1624–:1628) is a *different* 0-1-2 mapping: `0→gravity, 1→EM, 2→QM(ħ)`. The owner's ladder
`0→existence, 1→membership, 2→value` is a **DIFFERENT labelling of the same three cells** — a
*co-reading*, not THE reading. The memo must NOT conflate them.

**GRADE 2: SUGGESTIVE-BUT-UNOWNED.** The f-vector=symmetric-functions and the C⁰←C¹←C² 0-1-2 cochain
stratification are **OWNED** (record this as the genuine find). But the whole *correspondence*
(scene-is-2D **and** dim=detection-degree) rests on **two of the memo's own readings**, so it is
suggestive, not owned. Filed only as a flagged reading proposal (see §5), never as a core theorem.

---

## 3. THE QUBIT SKELETON — GRADE: **OWNED-DISCRETE-SKELETON + EXTERNAL-CONTINUUM-BRIDGE** (the honest ceiling)

### The owned DISCRETE skeleton (all verified verbatim)

- **Magnitude — THE 6.1.2** (BOOK_06:296–308, `⊥`-proved): *"W_ext=φ⁻¹, W_int=φ⁻²"* with
  **`W_ext + W_int = 1`** (two probabilities summing to 1, demand 1) and **`W_int = W_ext²`**
  (demand 2). External = "where am I?" (address), internal = "who am I?" (phase/holonomy). The proof
  is exactly `p+p²=1` again. (Verified: `W_ext+W_int=1`, `W_int=W_ext²`.)
- **Phase — the one ℤ₂ orientation:** `{+,−} = Z(Q₈) = [Q₈,Q₈] = {±1}` (BOOK_01:830,
  `D0-OMEGA8-CENTER-001`, LEAN_PROVED). One discrete sign/phase bit. (Verified: `|Z(Q₈)|=2`.)

So `{φ⁻¹, φ⁻²}`-magnitude × `{±}`-phase is a **genuine DISCRETE two-outcome, signed object** — a
**qubit-SKELETON**: two weights that partition unity (the "probabilities" of a measurement) plus one
relative phase bit. This much is **OWNED**.

### The continuum completion — EXTERNAL, pre-registered as the primary self-attack

A **genuine qubit** is a continuous complex amplitude `α|0⟩+β|1⟩`, `|α|²+|β|²=1`, `α,β ∈ ℂ`. The
discrete skeleton has ONE magnitude pair and ONE sign — **no continuum of amplitudes and no continuous
U(1) phase**. Getting from the skeleton to a real qubit requires **continuity**, which in D0 is a
**hypothesis of the external bridge**:

- **BOOK_00:473**, `D0-M1-INFO-RECONSTRUCTION-001`: *"a finite information capacity of an elementary
  system, **plus continuity and tomographic locality**, uniquely yields the complex Hilbert-space
  structure of QM … owner edge D0-M1-INFO-RECONSTRUCTION-001, ASSUMP-M1-INFO-RECONSTRUCTION … these
  are cited external owners … corroborating the D0 axiomatic base, not derived inside D0 — BRIDGE,
  never core."* (Hardy / Masanes–Müller [NJP 13, **053040**, 2011] / CDP.)
- Complexity (ℂ not ℝ) is likewise external: `D0-COMPLEX-QM-FORCING-001`, `ASSUMP-COMPLEX-QM`
  (Renou et al.).

### The one honest deepening this forge adds (NOT a closure)

This forge gives the **microscopic reading of why the M1 atoms are qubit-shaped**: the bridge's
"finite-capacity elementary system" is, concretely, **the THE 6.1.2 weight-split + the Ω₈ orientation
bit** — a `{φ⁻¹,φ⁻²}`-weighted signed two-outcome cell. That is a *deepening of the existing bridge's
input* (it says what the elementary system IS), **not** a new derivation of QM. The continuity that
completes the skeleton to a qubit remains exactly the bridge's own hypothesis.

### PRE-REGISTERED PRIMARY SELF-ATTACK (the burn history line)

The memo does **NOT** claim: "D0 derives qubits", "D0 derives QM", "qubits forced/derived", or that
continuity is owned. The verifier ENFORCES this: check `3d` asserts `continuum_is_owned = False` and
**FAILS** (mutation 6) if anyone marks continuity owned. Any sentence upgrading the bridge from
external-conditional to internal-derived is a KILL.

**GRADE 3: OWNED-DISCRETE-SKELETON-plus-EXTERNAL-CONTINUUM-BRIDGE.** (The honest ceiling. Anything
stronger = KILL. The qubit/QM path lands on the pre-existing `D0-M1-INFO-RECONSTRUCTION-001`, not on a
new result.)

---

## 4. PER-ITEM HONEST GRADES (summary)

| item | claim | GRADE | what is OWNED | what is reading / external |
|---|---|---|---|---|
| 1 | 0D existence boolean below membership | **AUTHORED-GLOSS** | 3 levels `{1, p, p²}`; membership(1)+value(2); 𝔮 record-quantum; sign bit ℤ₂ | "unit = a 0D graded level" is a re-label; existence lives INSIDE deg-1 at :1130 |
| 2 | scene = 2D simplicial complex, top-dim = detection-degree | **SUGGESTIVE-BUT-UNOWNED** | **OWNED:** f-vec (33,359,1287)=(e₁,e₂,e₃) symm funcs; C⁰←C¹←C² 0-1-2 cochain (§02.27 :1817) + THE 02.19B 0-1-2 strata (§02.19B :1624) | **READING:** "tripartite⇒2D/no-K₄" sound-but-unowned; "dim=degree" link unwritten; text reads cells as *forces* (grav/EM/QM). checker certifies only 2=2, NOT same-root |
| 3 | qubit / QM path | **OWNED-DISCRETE-SKELETON + EXTERNAL-CONTINUUM-BRIDGE** | THE 6.1.2 `(φ⁻¹,φ⁻²)` split summing to 1; ℤ₂ orientation phase | continuum/complex amplitude = continuity+tomographic-locality hypotheses of `D0-M1-INFO-RECONSTRUCTION-001` (external) |

## 5. THE ONE REAL MINTABLE SYNTHESIS (if any)

**One flagged reading PROPOSAL (NOT a mint candidate):** `D0-SCENE-DIMENSION-DETECTION-DEGREE-BRIDGE`
— records the **numeric equality** that the tripartite carrier's top simplicial dimension (2, no K₄)
equals the detection-degree cap (2, p³∈span{1,p}), with a *parallel* mechanism reading. It borrows the
*shape* of `D0-PORT-GOLDEN-SPLIT-BRIDGE-001`, but is **strictly weaker and lower-confidence**: that
template's BOTH legs are owned, whereas this proposal rests on **TWO unowned readings** — (i) the
scene's 2-dimensionality (SOUND-BUT-UNOWNED) and (ii) the dim=degree link (unwritten). It must carry
RISK-C verbatim (the cells are owned as *force strata*, not comparison-kinds — a *co-reading*, not THE
reading), must NOT absorb THE 02.19B's gravity/EM/QM mapping, and must NOT claim the "same root"
(the checker certifies only `2=2`). This is a flagged reading proposal for the owner's judgement, not
a §05.8.R mint candidate.

**A safe note (not a new row):** annotate `D0-DETECTION-QUADRATIC-001` that its unit section is
registration/𝔮-typed (the "existence" flavour) — as an analogy, explicitly NOT a degree-0 level.

**Everything qubit/QM lands on the existing external bridge `D0-M1-INFO-RECONSTRUCTION-001`
(conditional, ASSUMP-gated); this forge produces NO new QM result — only its microscopic reading.**

---

## 6. Verifier

`close_dim_logical_check.py`: 11 checks (items 1/2/3), exact ℚ(φ) arithmetic, independently built
quantities (no check builds its key quantity from the conclusion). 7 mutations, each flips a
CONCLUSION and must break ≥1 check — confirmed. Two guards matter most: **mutation 6** (continuity
smuggled as owned ⇒ "qubit derived") is caught by `3d`; **mutation 7** (the two caps collapsed into
one operation, i.e. the "same-root" identity asserted without proof) is caught by `2d` and by `2d`
ALONE (2c stays green), which is the mechanical statement that `2c` certifies only the numeric
equality `2=2` while `2d` carries — and only as a falsifiable *reading* — the mechanism-parallelism.
Clean run: all-PASS. This makes both the QM over-claim and the "same-root" over-claim mechanically
un-writable without turning the verifier red.

---

## 7. Skeptic pass (§05.8.R) — verdict and repairs applied

**Verdict: WOUNDED-REPAIRABLE — NO KILL on the primary QM/qubit target.** The independent skeptic
confirmed: (a) item 3's honest ceiling holds and is code-enforced (`3d`/mutation 6); (b) BOOK_00:473,
BOOK_06:296–308, BOOK_01:1130 quotes are verbatim-accurate and item 1's AUTHORED-GLOSS verdict is
well-founded; (c) the checker runs clean and every mutation fires. Four repairs were required and
**all applied**:

- **R1 (citation drift, top priority given burn history):** BOOK_02 line cites tightened to exact
  quoted-token lines / section anchors — §02.19B header :1620, THE 02.19B :1624, strata :1626/:1627/
  :1628; §02.27 cochain block :1817 (prose lead-in :1814). Re-verified on disk.
- **R2 (over-generous item-2 grade):** downgraded to **SUGGESTIVE-BUT-UNOWNED**. The f-vector=symm-funcs
  and the C⁰←C¹←C² 0-1-2 cochain stratification are recorded as the genuine OWNED find; "tripartite⇒2D
  /no-K₄" is flagged SOUND-BUT-UNOWNED; "OWNED-CORRESPONDENCE" removed from the table.
- **R3 (the "same-root" trap, mirror of `zA=mu2*zvol`):** added check `2d` — two distinct 3s each
  independently yielding cap 2 via two distinct operations — and demoted `2c` to "numeric equality
  only." Memo now states plainly the checker certifies `2=2`, NOT a shared root. Mutation 7 breaks
  `2d` alone.
- **R4 (mintable scope):** `D0-SCENE-DIMENSION-DETECTION-DEGREE-BRIDGE` filed as a strictly-weaker,
  lower-confidence, flagged reading proposal (two unowned legs) — explicitly NOT a §05.8.R mint
  candidate.

*End of memo. No registry rows modified; the one candidate is a flagged reading proposal, not a mint
candidate. Status: candidate/DRAFT (skeptic-hardened WOUNDED→REPAIRED), pending owner judgement.
`053040` untouched throughout.*
