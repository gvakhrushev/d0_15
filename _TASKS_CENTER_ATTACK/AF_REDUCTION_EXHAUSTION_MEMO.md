# AF-REDUCTION EXHAUSTION — the anchor no-go upgraded from witness to the whole su-reduction
# family (no-go-synthesis pass #3; DRAFT, pre-skeptic)

**Date:** 2026-07-18 · **Status:** DRAFT candidate; no ledger row edited (mint package §4).
**Program:** "no-go как источник прорывов", pass #3 (pass #1 = grading argmin; pass #2 = E1
residual location).
**Pre-flight:** full read of `AFSceneAnchorDimensionAudit.lean` (afBlocks (5,3), dim 34,
scene 33, excess 1, typed-not-numerology) and `AFOneDimensionalReductionClassification.lean`
(Outcome D: canonical trace/cyclic line exists; reduction `su(5)⊕su(3)⊕u(1)` parts (24,8,1);
witness mismatch vs (9,11,13); 2 blocks ≠ 3 parts); registry rows 429/434 (the 33-anchor
scale-invariant mismatch `{1,3,8,21} ≠ {1,2,8,10,12}` — a SEPARATE no-go, not touched);
no row named AF-REDUCTION-EXHAUSTION (id free).
**Companion Lean:** `D0/VNext/AFReductionExhaustion.lean` — compiles exit 0, kernel-only
(no native_decide), NOT wired, NOT minted.

## §0. Claim (witness → family, two machine-checked upgrades)

1. **Diophantine uniqueness of the witness' class** (`two_block_dim33_unique`):
   `a² + b² = 34 ∧ a ≥ b ≥ 1 ⟹ (a,b) = (5,3)`. The owned witness `M₅ ⊕ M₃` is the ONLY
   two-block matrix algebra whose canonical trace-zero reduction totals the scene dimension
   33. The no-go's example was secretly its entire class.
2. **Universal residue obstruction** (`scene_parts_avoid_su_lattice` +
   `no_su_reduction_matches_scene`): every part of a canonical trace-zero reduction of
   `⊕ᵢ M_{dᵢ}` is `dᵢ²−1` (su-part) or `1` (u(1) from center minus trace line); the scene
   parts `9, 11, 13` are neither (`d² ∈ {10,12,14}` has no square; none equals 1). Hence for
   EVERY block list — any length, any sizes, infinitely many candidates — the reduction parts
   ≠ scene parts even as MULTISETS. Witness no-go ⟹ family-wide no-go, in one residue step.
3. Sanity leg (`reduction_parts_witness`): the general grammar reproduces the owned witness
   parts `[24, 8, 1]` at `afBlocks` — the generalization is anchored, not free-floating.

**Positive/selector face:** the scene fingerprint `(9,11,13) = (L₅−2, L₅, L₅+2)` is DISJOINT
from the su-dimension lattice `{d²−1}` — the Lucas frame is structurally invisible to
su-type reductions. The `34→33` near-miss is now LOCATED: it lives exactly at the unique
Fibonacci two-block `(5,3)` and nowhere else. This converts "the AF route fails here" into
"the AF route fails everywhere, and here is the unique place it ever came close".

## §1. What this does NOT claim

- NOT a new physical no-go: the owned Outcome-D row is untouched; this is its strength
  upgrade (witness → family) inside the SAME reduction grammar.
- The exhaustion is over the CANONICAL-REDUCTION SHAPE (su-parts + u(1)s — the grammar the
  owned no-go itself uses, reproduced at the witness by the sanity leg). Non-canonical
  carryings (arbitrary linear maps, non-reduction embeddings) are OUTSIDE the class — they
  stay with the owned no-go's own boundary and the 33-anchor row's scale-invariant mismatch
  (rows 429/434, separate, untouched).
- NOT a claim about the spectral fingerprint `{1,3,8,21} ≠ {1,2,8,10,12}` (row 434's
  content) — different invariant, different row; cross-referenced only.
- The Lucas reading of the disjointness (`L₅±2` vs `d²−1`) is presentation; the theorem is
  the bare arithmetic.

## §2. Pre-registered attack surface

- **ATT-1 (grammar scope).** "Every part is `d²−1` or `1`" encodes the canonical reduction
  grammar as a DEF (`reductionParts`). A skeptic can ask: is that grammar owned for arbitrary
  block lists, or only at the witness? PRICED: the sanity leg anchors it at the owned witness;
  the generalization is the standard trace-zero decomposition of `⊕ M_{dᵢ}` (su(dᵢ) summands
  + center/trace); if the skeptic rules the general grammar assembly-grade, the universal leg
  is graded assembly-anchored while the Diophantine leg (pure arithmetic on the owned class
  definition) is unaffected.
- **ATT-2 (multiset vs structure).** Matching "parts as multisets" is NECESSARY for any
  carrying, so its failure kills all carryings; but a skeptic should confirm the owned no-go's
  mismatch is also multiset-grade (it is: `(24,8,1) ≠ (9,11,13)` as lists AND multisets).
- **ATT-3 (triviality).** The proofs are elementary (squares mod small numbers). PRICED: per
  trap (m), the content is the ATTRIBUTION — that the owned witness no-go extends family-wide
  — plus the located near-miss; the memo claims exactly that.
- **ATT-4 (duplication).** Rows 429/434 already kill AF routes. PRICED: 429 = the witness
  classification (this upgrades it), 434 = the spectral-multiplicity anchor (different
  invariant); neither states the Diophantine uniqueness nor the universal residue obstruction;
  id free; cross-refs required both ways.

## §3. Verification

`lake env lean D0/VNext/AFReductionExhaustion.lean` exit 0; kernel-only; the universal leg is
a genuine ∀ over `List ℕ` (not a finite scan). Negative controls (REWRITTEN per skeptic #22
R3 — the draft's (8,11,13)/(9,11,1) claim was machine-REFUTED, trap f: those defeat only the
avoidance LEMMA, not the conclusion): the honest conclusion-failing controls are
FULLY-LATTICE scenes — `reductionParts [5,3] = (24,8,1)` and `reductionParts [2,2] = (3,3,1)`
ARE matched by their own block lists, so the exhaustion theorem is false for those scenes;
it is the scene (9,11,13) specifically that no list reaches. Grammar faithfulness controls:
`reductionParts [1,1] = [1]`, `[2,1] = [3,1]` (su(1) phantom parts filtered — R1; matches the
owned tower levels A₀/A₁).

## §4. Ready-to-mint package (owner-authorized; apply after skeptic)

1. New row `D0-AF-REDUCTION-EXHAUSTION-001` (both ledgers): BOOK_02 §02.vnext33 anchor;
   `D0.VNext.AFReductionExhaustion` / `af_reduction_exhaustion;two_block_dim33_unique;
   scene_parts_avoid_su_lattice;no_su_reduction_matches_scene;reduction_parts_witness;
   reduction_parts_witness_owned;reduction_parts_tower_levels`;
   lean_status LEAN_PROVED; release **NO-GO** (skeptic #22 adjudication: strength note on an
   existing NO-GO, grammar now the faithful standard rendering post-R1, anchored by theorem
   to the owned reducedParts post-R2; grammar-scope clause in the note).
2. Note append to `D0-VNEXT-AF-ONE-DIMENSIONAL-REDUCTION-CLASSIFICATION-001`:
   "EXHAUST[2026-07-18]: witness → family. The (5,3) witness is Diophantine-UNIQUE in the
   two-block class at scene dimension (a²+b²=34); and the residue obstruction (scene parts
   avoid the su-lattice {d²−1} ∪ {1}: squares 10/12/14 do not exist) kills EVERY block list
   at multiset grade — the Outcome-D mismatch is family-wide (D0-AF-REDUCTION-EXHAUSTION-001).
   34→33 near-miss located exactly at the unique Fibonacci two-block."
3. Cross-ref note on row 434 (33-anchor): "the reduction-parts exhaustion is complementary
   (different invariant: parts vs spectral multiplicities); both now family-grade." PLUS
   cross-ref to row 551 `D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001` (owns "34 = F₉ = 33+1, the
   +1 is the kernel mode" — the near-miss narrative sits in its territory; skeptic #22 R4)
   and the 429-note wording: "witness mismatch at MULTISET grade machine-checked here (429's
   own Lean is list-grade)".
4. Wire into `D0/All.lean`; full build; guards. NO book edits (parallel session owns 01_BOOKS).
